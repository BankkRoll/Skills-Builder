# What is the agent? and more

# What is the agent?

> Automate documentation updates with the agent. Create updates from Slack messages, PRs, or API calls.

Automate documentation updates with the agent. Create updates from Slack messages, PRs, or API calls.

---

# AI

> Learn how AI enhances reading, writing, and discovering your documentation

When you host your documentation on Mintlify, built-in AI features help your users find answers and your team maintain content more efficiently. Your content provides the context for these AI-native features to improve the experiences of reading, writing, and discovering your documentation.

## ​What makes your documentation AI-native

### ​Reading

 In addition to reading individual pages, users can chat with the [assistant](https://mintlify.com/docs/ai/assistant) in your documentation for immediate answers to their questions and links to relevant content. The assistant helps guide users through your product with accurate information from your documentation. Embed the assistant into custom apps with the [API](https://mintlify.com/docs/api-reference/assistant/create-assistant-message) to extend where users can access your documentation.

### ​Writing

 The [agent](https://mintlify.com/docs/agent) helps you write and maintain documentation. It creates pull requests with proposed changes based on your prompts, pull requests, and Slack threads. Add the agent to your Slack workspace so that anyone on your team can help maintain your documentation by chatting with the agent. Or embed the agent into custom apps via the [API](https://mintlify.com/docs/api-reference/agent/create-agent-job). You can configure the agent to monitor connected repositories and proactively [suggest](https://mintlify.com/docs/agent/suggestions) documentation updates when it identifies user-facing changes. Configure popular tools like [Cursor](https://mintlify.com/docs/guides/cursor), [Claude Code](https://mintlify.com/docs/guides/claude-code), and [Windsurf](https://mintlify.com/docs/guides/windsurf) to reference the Mintlify schema, your style guide, and best practices.

### ​Discovering

 Your site is automatically optimized for AI tools and search engines to help users discover your documentation. All pages send their content as Markdown to AI agents instead of HTML, which helps these tools process your content faster and use fewer tokens. Every page is also available to view as Markdown by appending `.md` to the URL. Mintlify hosts `llms.txt` and `skill.md` files for your documentation. These industry-standard files help LLMs respond efficiently with relevant information to user queries and provide a list of capabilities for agents to use, so that users are more successful with your product. Your documentation site also hosts an MCP server that lets users connect your documentation directly to their AI tools for up to date information about your product directly where they want it. Full-text search and semantic understanding help users and AI tools find relevant information quickly. Search understands user intent rather than just matching keywords. And if a user encounters a 404 error, your site suggests related pages to help them find what they’re looking for. No configuration required.

## ​Enable AI features

 Select any of the following cards for more information. [AssistantConfigure the assistant to search external sites or direct people to your support team if it can’t answer their questions.](https://mintlify.com/docs/ai/assistant)[AgentUse the agent in your dashboard to create documentation updates.](https://mintlify.com/docs/agent/quickstart)[SuggestionsMonitor Git repositories for changes and receive suggested documentation updates.](https://mintlify.com/docs/agent/suggestions)[Contextual menuAdd a menu to pages that lets users query AI tools, connect to your MCP server, and copy pages as context with one click.](https://mintlify.com/docs/ai/contextual-menu)

---

# Playground

> Let developers test API endpoints directly in your documentation.

## ​Overview

 The API playground is an interactive environment that lets users test and explore your API endpoints. Developers can craft API requests, submit them, and view responses without leaving your documentation. See [Trigger an update](https://mintlify.com/docs/api/update/trigger) for an example of the API playground in action. ![API playground for the trigger an update endpoint.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-light.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=f83551b5d84cf27a44ed1d9418ca61be)![API playground for the trigger an update endpoint.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/playground/API-playground-dark.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=5a0dc3fd3ca0a5766c599c00a5910dba) The playground generates interactive pages for your endpoints based on your OpenAPI specification or AsyncAPI schema. If you modify your API, the playground automatically updates the relevant pages. We recommend generating your API playground from an OpenAPI specification. However, you can manually create API reference pages after defining a base URL and authentication method in your `docs.json`.

## ​Get started

 1

Add your OpenAPI specification file.

Validate your OpenAPI specification file using the [Swagger Editor](https://editor.swagger.io/) or [Mint CLI](https://www.npmjs.com/package/mint) command `mint openapi-check <filename>`.

```
/your-project
  |- docs.json
  |- openapi.json
```

2

Generate endpoint pages.

Update your `docs.json` to reference your OpenAPI specification.**To automatically generate pages for all endpoints in your OpenAPI specification**, add an `openapi` property to any navigation element.This example generates a page for each endpoint specified in `openapi.json` and organizes the pages in the “API reference” group.Generate all endpoint pages

```
"navigation": {
  "groups": [
    {
      "group": "API reference",
      "openapi": "openapi.json"
    }
  ]
}
```

**To generate pages for only specific endpoints**, list the endpoints in the `pages` property of the navigation element.This example generates pages for only the `GET /users` and `POST /users` endpoints. To generate other endpoint pages, add additional endpoints to the `pages` array.Generate specific endpoint pages

```
"navigation": {
  "groups": [
      {
        "group": "API reference",
        "openapi": "openapi.json",
        "pages": [
          "GET /users",
          "POST /users"
        ]
      }
  ]
}
```

## ​Customize your playground

 Customize your API playground by defining the following properties in your `docs.json`. [​](#param-playground)playgroundobjectConfigurations for the API playground.

Hide playground

[​](#param-display)display"interactive" | "simple" | "none"The display mode of the API playground.

- `"interactive"`: Display the interactive playground.
- `"simple"`: Display a copyable endpoint with no playground.
- `"none"`: Display nothing.

Defaults to `interactive`.[​](#param-proxy)proxybooleanWhether to pass API requests through a proxy server. Defaults to `true`. [​](#param-examples)examplesobjectConfigurations for the autogenerated API examples.

Hide examples

[​](#param-languages)languagesarray of stringExample languages for the autogenerated API snippets.Languages display in the order specified.[​](#param-defaults)defaults"required" | "all"Whether to show optional parameters in API examples. Defaults to `all`.[​](#param-prefill)prefillbooleanWhether to prefill the API playground with data from schema examples. When enabled, the playground automatically populates request fields with example values from your OpenAPI specification. Defaults to `false`.[​](#param-autogenerate)autogeneratebooleanWhether to generate code samples for endpoints from API specifications. Defaults to `true`. When set to `false`, only manually-written code samples (from `x-codeSamples` in OpenAPI specifications or `<RequestExample>` components in MDX) appear in the API playground.

### ​Example configuration

 This example configures the API playground to be interactive with example code snippets for cURL, Python, and JavaScript. Only required parameters are shown in the code snippets, and the playground prefills the request body with example values.

```
{
 "api": {
   "playground": {
     "display": "interactive"
   },
   "examples": {
     "languages": ["curl", "python", "javascript"],
     "defaults": "required",
     "prefill": true
   }
 }
}
```

### ​Custom endpoint pages

 When you need more control over your API documentation, use the `x-mint` extension in your OpenAPI specification or create individual MDX pages for your endpoints. Both options allow you to:

- Customize page metadata
- Add additional content like examples
- Control playground behavior per page

 The `x-mint` extension is recommended so that all of your API documentation is automatically generated from your OpenAPI specification and maintained in one file. Individual MDX pages are recommended for small APIs or when you want to experiment with changes on a per-page basis.

## ​Further reading

- [OpenAPI setup](https://mintlify.com/docs/api-playground/openapi-setup) for more information on creating your OpenAPI document.
- [x-mint extension](https://mintlify.com/docs/api-playground/openapi-setup#x-mint-extension) for more information on customizing your endpoint pages.
- [MDX setup](https://mintlify.com/docs/api-playground/mdx-setup) for more information on manually creating individual API reference pages.
- [AsyncAPI setup](https://mintlify.com/docs/api-playground/asyncapi-setup) for more information on creating your AsyncAPI schema to generate WebSocket reference pages.
