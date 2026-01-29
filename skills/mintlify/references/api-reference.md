# Create agent job and more

# Create agent job

> Creates a new agent job that can generate and edit documentation based on provided messages and branch information.

Creates a new agent job that can generate and edit documentation based on provided messages and branch information.

---

# Get agent job by ID

> Retrieves the details and status of a specific agent job by its ID.

$/$[Mintlifyhome page](https://mintlify.com/docs)[Documentation](https://mintlify.com/docs)[Guides](https://mintlify.com/docs/guides)[API reference](https://mintlify.com/docs/api/introduction)[Changelog](https://mintlify.com/docs/changelog)

Get agent job by ID

```
curl --request GET \
  --url https://api.mintlify.com/v1/agent/{projectId}/job/{id} \
  --header 'Authorization: Bearer <token>'
```

```
{
  "sessionId": "<string>",
  "subdomain": "<string>",
  "branch": "<string>",
  "haulted": true,
  "haultReason": "completed",
  "pullRequestLink": "<string>",
  "messageToUser": "<string>",
  "todos": [
    {
      "content": "<string>",
      "status": "pending",
      "priority": "high",
      "id": "<string>"
    }
  ],
  "createdAt": "2023-11-07T05:31:56Z"
}
```

GET/agent/{projectId}/job/{id}Get agent job by ID

```
curl --request GET \
  --url https://api.mintlify.com/v1/agent/{projectId}/job/{id} \
  --header 'Authorization: Bearer <token>'
```

```
{
  "sessionId": "<string>",
  "subdomain": "<string>",
  "branch": "<string>",
  "haulted": true,
  "haultReason": "completed",
  "pullRequestLink": "<string>",
  "messageToUser": "<string>",
  "todos": [
    {
      "content": "<string>",
      "status": "pending",
      "priority": "high",
      "id": "<string>"
    }
  ],
  "createdAt": "2023-11-07T05:31:56Z"
}
```

## ​Usage

 This endpoint retrieves the details and status of a specific agent job by its unique identifier. Use this to check the progress, status, and results of a previously created agent job.

## ​Job details

 The response includes information such as:

- Job execution status and completion state
- Branch information and pull request details
- Session metadata and timestamps

#### Authorizations

[​](#authorization-authorization)Authorizationstringheaderrequired

The Authorization header expects a Bearer token. Create an [Admin API Key](https://dashboard.mintlify.com/settings/organization/api-keys) here.

#### Path Parameters

[​](#parameter-project-id)projectIdstringrequired

Your project ID. Can be copied from the [API keys](https://dashboard.mintlify.com/settings/organization/api-keys) page in your dashboard.

[​](#parameter-id)idstringrequired

The unique identifier of the agent job to retrieve.

#### Response

200 - application/json

Agent job details retrieved successfully

[​](#response-session-id)sessionIdstring

The subdomain this session belongs to.

[​](#response-subdomain)subdomainstring

The subdomain this session belongs to.

[​](#response-branch-one-of-0)branchstring | null

Git branch name where changes were made.

[​](#response-haulted)haultedboolean

Whether the session execution was halted.

[​](#response-hault-reason)haultReasonenum<string>

Reason for session halt.

Available options :  `completed`,  `github_missconfigured`,  `error` [​](#response-pull-request-link)pullRequestLinkstring

Link to the created pull request.

[​](#response-message-to-user)messageToUserstring

Message for the user about the session outcome.

[​](#response-todos)todosobject[]

List of todo items from the session.

Show   child attributes

[​](#response-created-at)createdAtstring<date-time>

Timestamp when the session was created.

Ctrl +I$/$

---

# Get all agent jobs

> Retrieves all agent jobs for the specified domain, including their status and details.

$/$[Mintlifyhome page](https://mintlify.com/docs)[Documentation](https://mintlify.com/docs)[Guides](https://mintlify.com/docs/guides)[API reference](https://mintlify.com/docs/api/introduction)[Changelog](https://mintlify.com/docs/changelog)

Get all agent jobs

```
curl --request GET \
  --url https://api.mintlify.com/v1/agent/{projectId}/jobs \
  --header 'Authorization: Bearer <token>'
```

```
{
  "allSessions": [
    {
      "sessionId": "<string>",
      "subdomain": "<string>",
      "branch": "<string>",
      "haulted": true,
      "haultReason": "completed",
      "pullRequestLink": "<string>",
      "messageToUser": "<string>",
      "todos": [
        {
          "content": "<string>",
          "status": "pending",
          "priority": "high",
          "id": "<string>"
        }
      ],
      "createdAt": "2023-11-07T05:31:56Z"
    }
  ]
}
```

GET/agent/{projectId}/jobsGet all agent jobs

```
curl --request GET \
  --url https://api.mintlify.com/v1/agent/{projectId}/jobs \
  --header 'Authorization: Bearer <token>'
```

```
{
  "allSessions": [
    {
      "sessionId": "<string>",
      "subdomain": "<string>",
      "branch": "<string>",
      "haulted": true,
      "haultReason": "completed",
      "pullRequestLink": "<string>",
      "messageToUser": "<string>",
      "todos": [
        {
          "content": "<string>",
          "status": "pending",
          "priority": "high",
          "id": "<string>"
        }
      ],
      "createdAt": "2023-11-07T05:31:56Z"
    }
  ]
}
```

## ​Usage

 This endpoint retrieves all agent jobs for the specified domain, providing an overview of all agent activities and their current status. This is useful for monitoring and managing multiple concurrent or historical agent jobs.

## ​Response

 Use this endpoint to get a comprehensive view of all previous agent sessions.

#### Authorizations

[​](#authorization-authorization)Authorizationstringheaderrequired

The Authorization header expects a Bearer token. Create an [Admin API Key](https://dashboard.mintlify.com/settings/organization/api-keys) here.

#### Path Parameters

[​](#parameter-project-id)projectIdstringrequired

Your project ID. Can be copied from the [API keys](https://dashboard.mintlify.com/settings/organization/api-keys) page in your dashboard.

#### Response

200 - application/json

All agent jobs retrieved successfully

[​](#response-all-sessions)allSessionsobject[]

Array of all agent sessions for the domain.

Show   child attributes

Ctrl +I$/$

---

# Assistant message

> Generates a response message from the assistant for the specified domain.

$/$[Mintlifyhome page](https://mintlify.com/docs)[Documentation](https://mintlify.com/docs)[Guides](https://mintlify.com/docs/guides)[API reference](https://mintlify.com/docs/api/introduction)[Changelog](https://mintlify.com/docs/changelog)

Assistant message

```
curl --request POST \
  --url https://api.mintlify.com/discovery/v1/assistant/{domain}/message \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "fp": "<string>",
  "messages": [
    {
      "id": "foobar",
      "role": "user",
      "content": "how do i get started",
      "parts": [
        {
          "type": "text",
          "text": "How do I get started"
        }
      ]
    }
  ],
  "threadId": null,
  "retrievalPageSize": 5,
  "filter": null
}
'
```

```
{}
```

POST/assistant/{domain}/messageAssistant message

```
curl --request POST \
  --url https://api.mintlify.com/discovery/v1/assistant/{domain}/message \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "fp": "<string>",
  "messages": [
    {
      "id": "foobar",
      "role": "user",
      "content": "how do i get started",
      "parts": [
        {
          "type": "text",
          "text": "How do I get started"
        }
      ]
    }
  ],
  "threadId": null,
  "retrievalPageSize": 5,
  "filter": null
}
'
```

```
{}
```

## ​Integration withuseChat

 The `useChat` hook from Vercel’s AI SDK is the recommended way to integrate the assistant API into your application. The Mintlify assistant API is compatible with **AI SDK v4**. If you use AI SDK v5 or later, you must configure a custom transport. 1

Install AI SDK v4

```
npm i ai@^4.1.15
```

2

Use the hook

```
import { useChat } from 'ai/react';

function MyComponent({ domain }) {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: `https://api.mintlify.com/discovery/v1/assistant/${domain}/message`,
    headers: {
      'Authorization': `Bearer ${process.env.MINTLIFY_TOKEN}`,
    },
    body: {
      fp: 'anonymous',
      retrievalPageSize: 5,
      context: [
        {
          type: 'code',
          value: 'const example = "code snippet";',
          elementId: 'code-block-1',
        },
      ],
    },
    streamProtocol: 'data',
    sendExtraMessageFields: true,
  });

  return (
    <div>
      {messages.map((message) => (
        <div key={message.id}>
          {message.role === 'user' ? 'User: ' : 'Assistant: '}
          {message.content}
        </div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

**Required configuration for Mintlify:**

- `streamProtocol: 'data'` - Required for streaming responses.
- `sendExtraMessageFields: true` - Required to send message metadata.
- `body.fp` - Fingerprint identifier (use ‘anonymous’ or a user identifier).
- `body.retrievalPageSize` - Number of search results to use (recommended: 5).

**Optional configuration:**

- `body.context` - Array of contextual information to provide to the assistant. Each context object contains:
  - `type` - Either `'code'` or `'textSelection'`.
  - `value` - The code snippet or selected text content.
  - `elementId` (optional) - Identifier for the UI element containing the context.

 See [useChat](https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat) in the AI SDK documentation for more details.

## ​Rate limits

 The assistant API has the following limits:

- 10,000 uses per key per month
- 10,000 requests per Mintlify organization per hour
- 10,000 requests per IP per day

#### Authorizations

[​](#authorization-authorization)Authorizationstringheaderrequired

The Authorization header expects a Bearer token. See the [API authentication](https://mintlify.com/docs/api/introduction#authentication) documentation for details on how to get your API key.

#### Path Parameters

[​](#parameter-domain)domainstringrequired

The domain identifier from your `domain.mintlify.app` URL. Can be found at the end of your dashboard URL. For example, `dashboard.mintlify.com/organization/domain` has a domain identifier of `domain`.

#### Body

application/json[​](#body-fp)fpstringrequired

Fingerprint identifier for tracking conversation sessions. Use 'anonymous' for anonymous users or provide a unique user identifier.

[​](#body-messages)messagesobject[]required

Array of messages in the conversation. On the frontend, you will likely want to use the handleSubmit function from the @ai-sdk package's useChat hook to append user messages and handle streaming responses, rather than manually defining the objects in this array as they have so many parameters.

Show   child attributes

[​](#body-thread-id)threadIdstring

An optional identifier used to maintain conversation continuity across multiple messages. When provided, it allows the system to associate follow-up messages with the same conversation thread. The threadId is returned in the response as event.threadId when event.type === 'finish'.

[​](#body-retrieval-page-size)retrievalPageSizenumberdefault:5

Number of documentation search results to use for generating the response. Higher values provide more context but may increase response time. Recommended: 5.

[​](#body-filter)filterobject

Optional filter criteria for the search

Show   child attributes

#### Response

200 - application/json

Message generated successfully

Response object that streams formatted data stream parts with the specified status, headers, and content. This matches what is expected from the AI SDK as documented at [ai-sdk.dev/docs/ai-sdk-ui/streaming-data](https://ai-sdk.dev/docs/ai-sdk-ui/streaming-data). Instead of writing your own parser, it is recommended to use the [useChat hook from ai-sdk as documented here](https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat#usechat).

Ctrl +I$/$

---

# Search documentation

> Perform semantic and keyword searches across your documentation with configurable filtering and pagination.

Perform semantic and keyword searches across your documentation with configurable filtering and pagination.
