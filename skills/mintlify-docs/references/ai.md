# Assistant and more

# Assistant

> Add AI-powered chat to your docs that answers questions, cites sources, and generates code examples.

The assistant is automatically enabled on [Pro and Custom plans](https://mintlify.com/pricing?ref=assistant).

## ​About the assistant

 The assistant answers questions about your documentation through natural language queries. Users access the assistant on your documentation site, so they can find answers quickly and succeed with your product even if they don’t know where to look. The assistant uses agentic RAG (retrieval-augmented generation) with tool calling. When users ask questions, the assistant:

- **Searches and retrieves** relevant content from your documentation to provide accurate answers.
- **Cites sources** and provides navigable links to take users directly to referenced pages.
- **Generates copyable code examples** to help users implement solutions from your documentation.

 You can view assistant usage through your dashboard to understand user behavior and documentation effectiveness. Export and analyze query data to help identify:

- Frequently asked questions that might need better coverage.
- Content gaps where users struggle to find answers.
- Popular topics that could benefit from additional content.

### ​How indexing works

 The assistant automatically indexes your published documentation to answer questions accurately. When you publish changes, the assistant immediately indexes new, updated, or deleted content. The assistant does not index draft branches or preview deployments. By default, the assistant does not index hidden pages. To include hidden pages in the assistant’s index, set `seo.indexing: "all"` in your `docs.json`. See [Hidden pages](https://mintlify.com/docs/organize/hidden-pages#search-seo-and-ai-indexing) for more information.

### ​How the assistant handles unknown questions

 The assistant only answers questions based on information in your documentation. If it cannot find relevant information after searching, it responds that it doesn’t have enough information to answer. You can [set a deflection email](https://mintlify.com/docs/ai/assistant#set-deflection-email) so that the assistant provides your support email to users whose questions it cannot answer. This gives users a path forward, even if the documentation doesn’t address their specific question.

## ​Configure the assistant

 The assistant is active on Pro and Custom plans by default. Manage the assistant from the [Assistant Configurations](https://dashboard.mintlify.com/products/assistant/settings) page of your dashboard. Enable or disable the assistant, configure response handling, add default questions, and manage your message allowance.

### ​Enable or disable the assistant

 Toggle the assistant status to enable or disable the assistant for your documentation site. ![The assistant status toggle in the dashboard.](https://mintcdn.com/mintlify/qxFvxlkWYrjV0OaV/images/assistant/status-light.png?fit=max&auto=format&n=qxFvxlkWYrjV0OaV&q=85&s=723881f19ac3ad665a774eeb6f3b8652)![The assistant status toggle in the dashboard.](https://mintcdn.com/mintlify/qxFvxlkWYrjV0OaV/images/assistant/status-dark.png?fit=max&auto=format&n=qxFvxlkWYrjV0OaV&q=85&s=8c7ae23c57d3db8f67a649b0f09d45c4)

### ​Set deflection email

 In the Response Handling section, enable the assistant to redirect unanswered questions to your support team. Specify an email address for the assistant to give to users if it cannot answer their question. You can also enable a persistent button to allow users to email your team directly from the assistant chat panel. ![The assistant deflection panel in the dashboard. Assistant deflection is toggled on and support@mintlify.com is set as the deflection email.](https://mintcdn.com/mintlify/2qBICQFhOKqkes42/images/assistant/deflection-light.png?fit=max&auto=format&n=2qBICQFhOKqkes42&q=85&s=701d04063abf0a1e58dca69c225fea82)![The assistant deflection panel in the dashboard. Assistant deflection is toggled on and support@mintlify.com is set as the deflection email.](https://mintcdn.com/mintlify/2qBICQFhOKqkes42/images/assistant/deflection-dark.png?fit=max&auto=format&n=2qBICQFhOKqkes42&q=85&s=8ab6ee5ef32952135b1ef37ba0573f9e)

### ​Search domains

 In the Response Handling section, configure domains that the assistant can search for additional context when answering questions.

- Domains must be publicly available.
- Domains that require JavaScript to load are not supported.

 ![The assistant search domains panel enabled in the dashboard. The assistant is configured to search the mintlify.com/pricing domain.](https://mintcdn.com/mintlify/2qBICQFhOKqkes42/images/assistant/search-domains-light.png?fit=max&auto=format&n=2qBICQFhOKqkes42&q=85&s=a15d483e0eee1b9a55a8ff6583a7d331)![The assistant search domains panel enabled in the dashboard. The assistant is configured to search the mintlify.com/pricing domain.](https://mintcdn.com/mintlify/2qBICQFhOKqkes42/images/assistant/search-domains-dark.png?fit=max&auto=format&n=2qBICQFhOKqkes42&q=85&s=ae032b581c467630c044b073b583dded) For more precise control over what the assistant can search, use filtering syntax.

- **Domain-level filtering**
  - `example.com`: Search only the `example.com` domain
  - `docs.example.com`: Search only the `docs.example.com` subdomain
  - `*.example.com`: Search all subdomains of `example.com`
- **Path-level filtering**
  - `docs.example.com/api`: Search all pages under the `/api` subpath
- **Multiple patterns**
  - Add multiple entries to target different sections of sites

### ​Add sample questions

 Help your users begin conversations with the assistant by adding starter questions. Add commonly asked questions or questions about topics that you want your users to know about. Click **Ask AI** for recommended questions based on your documentation. ![The search suggestions panel in the dashboard with starter questions enabled and populated with three questions.](https://mintcdn.com/mintlify/2qBICQFhOKqkes42/images/assistant/search-suggestions-light.png?fit=max&auto=format&n=2qBICQFhOKqkes42&q=85&s=f2e40f177d289259f24644e5f1372a7d)![The search suggestions panel in the dashboard with starter questions enabled and populated with three questions.](https://mintcdn.com/mintlify/2qBICQFhOKqkes42/images/assistant/search-suggestions-dark.png?fit=max&auto=format&n=2qBICQFhOKqkes42&q=85&s=6a9bdfcc55dbe36c1fe30c877bcb414d)

## ​Manage billing

 The assistant uses tiered message allowances. A message is any user interaction with the assistant that receives a correct response. If you have unused messages, up to half of your message allowance can carry over to the next billing cycle. For example, if you have a 1,000 message allowance and you use 300 messages, 500 messages carry over to the next billing cycle giving you a total of 1,500 messages for the next billing cycle. By default, the assistant allows overages. You can disable overages to avoid incurring additional costs for usage beyond your tier. If you reach your message allowance with overages disabled, the assistant is unavailable until your message allowance resets. If you allow overages, each message beyond your allowance incurs an overage charge, but occasional overages may be cheaper than upgrading to a higher tier depending on your usage.

### ​Change your assistant tier

 Assistant tiers determine your monthly message allowance and pricing. View and change your current tier on the [Billing tab](https://dashboard.mintlify.com/products/assistant/settings/billing) of the assistant page in your dashboard. In the **Spending Controls** section, select your preferred tier from the dropdown menu. **Upgrade your tier:**

- Your new message allowance is available immediately.
- You pay a prorated difference for the current billing cycle.

 **Downgrade your tier:**

- Your message allowance updates immediately.
- Pricing changes take effect at the start of your next billing cycle.
- Unused messages from your current tier **do not** carry over.

### ​Allow overages

 If you want to disallow overages, disable them in the **Billing Controls** section of the [Billing tab](https://dashboard.mintlify.com/products/assistant/settings/billing) of the assistant page in your dashboard.

### ​Set usage alerts

 In the Billing Controls section, set usage alerts to receive an email when you reach a certain percentage of your message allowance.

## ​Connect apps

 In the connect apps section, add the assistant to your [Discord](https://mintlify.com/docs/ai/discord) server and [Slack](https://mintlify.com/docs/ai/slack-bot) workspace to allow users to get answers from your documentation on those platforms.

## ​Assistant insights

 Use assistant insights to understand how users interact with your documentation and identify improvement opportunities. The [assistant page](https://dashboard.mintlify.com/products/assistant) shows usage trends for the month to date. View more detailed insights on the [analytics](https://mintlify.com/docs/optimize/analytics#assistant) page.

## ​Make content AI ingestible

 Structure your documentation to help the assistant provide accurate, relevant answers. Clear organization and comprehensive context benefit both human readers and AI understanding.

## Structure and organization

- Use semantic markup.
- Write descriptive headings for sections.
- Create a logical information hierarchy.
- Use consistent formatting across your docs.
- Include comprehensive metadata in page frontmatter.
- Break up long blocks of text into shorter paragraphs.

## Context

- Define specific terms and acronyms when first introduced.
- Provide sufficient conceptual content about features and procedures.
- Include examples and use cases.
- Cross-reference related topics.
- Add [hidden pages](https://mintlify.com/docs/organize/hidden-pages) with additional context that users don’t need, but the assistant can reference.

## ​Use the assistant

 Users have multiple ways to start a conversation with the assistant. Each method opens a chat panel on the right side of your docs. Users can ask any question and the assistant searches your documentation for an answer. If the assistant cannot retrieve relevant information, the assistant responds that it cannot answer the question. Add the assistant as a bot to your [Slack workspace](https://mintlify.com/docs/ai/slack-bot) or [Discord server](https://mintlify.com/docs/ai/discord) so that your community can ask questions without leaving their preferred platform.

### ​UI placement

 The assistant appears in two locations: as a button next to the search bar and as a bar at the bottom of the page. ![Search bar and assistant button in light mode.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/assistant/assistant-button-light.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=716582bc54eaea73cb53d26b36a74fb4)![Search bar and assistant button in dark mode.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/assistant/assistant-button-dark.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=34096a771f492853e59eef654567b081)![Assistant bar in light mode.](https://mintcdn.com/mintlify/Gt7y__uLw46fbQ_E/images/assistant/assistant-bar-light.png?fit=max&auto=format&n=Gt7y__uLw46fbQ_E&q=85&s=920b62e97a4a24a5aa7a29d9306b3762)![Assistant bar in dark mode.](https://mintcdn.com/mintlify/Gt7y__uLw46fbQ_E/images/assistant/assistant-bar-dark.png?fit=max&auto=format&n=Gt7y__uLw46fbQ_E&q=85&s=f597be3a1c8a95a8a72aaae4f799981f)

### ​Keyboard shortcut

 Open the assistant chat panel with the keyboard shortcut Command + I on macOS and Ctrl + I on Windows.

### ​Highlight text

 Highlight text on a page and click the **Add to assistant** pop up button to open the assistant chat panel and add the highlighted text as context. You can add multiple text snippets or code blocks to the assistant’s context. ![The Add to assistant button above highlighted text in light mode.](https://mintcdn.com/mintlify/Gt7y__uLw46fbQ_E/images/assistant/highlight-light.png?fit=max&auto=format&n=Gt7y__uLw46fbQ_E&q=85&s=13c93b72e4f6b21800e31a55f85c3690)![The Add to assistant button above highlighted text in dark mode.](https://mintcdn.com/mintlify/Gt7y__uLw46fbQ_E/images/assistant/highlight-dark.png?fit=max&auto=format&n=Gt7y__uLw46fbQ_E&q=85&s=73ef7699810025a73fce4dc125fea683)

### ​Code blocks

 Click the **Ask AI** button in a code block to open the assistant chat panel and add the code block as context. You can add multiple code blocks or text snippets to the assistant’s context. ![The Ask AI button in a code block in light mode.](https://mintcdn.com/mintlify/Gt7y__uLw46fbQ_E/images/assistant/code-block-light.png?fit=max&auto=format&n=Gt7y__uLw46fbQ_E&q=85&s=d9b3cbecca1416291915ded538315d05)![The Ask AI button in a code block in dark mode.](https://mintcdn.com/mintlify/Gt7y__uLw46fbQ_E/images/assistant/code-block-dark.png?fit=max&auto=format&n=Gt7y__uLw46fbQ_E&q=85&s=1e5ffae5032208ff67d2a725b48fdafd)

### ​URLs

 Open the assistant with a URL query parameter to create deep links that guide users to specific information or share assistant conversations with pre-filled questions.

- **Open the assistant**: Append `?assistant=open` to open the assistant chat panel when the page loads.
  - Example: [https://mintlify.com/docs?assistant=open](https://mintlify.com/docs?assistant=open)
- **Open with a pre-filled query**: Append `?assistant=YOUR_QUERY` to open the assistant and automatically submit a question.
  - Example: [https://mintlify.com/docs?assistant=explain webhooks](https://mintlify.com/docs?assistant=explain%20webhooks)

## ​Troubleshooting

Assistant chat bar not visible

If the assistant UI is not visible in specific browsers, you may need to submit a false positive report to [EasyList](https://easylist.to). Browsers that use the EasyList Cookies List like Brave and Comet sometimes block the assistant or other UI elements. The EasyList Cookies List includes a domain-specific rule that hides fixed elements on certain domains to block cookie banners. This rule inadvertently affects legitimate UI components.Submit a false positive report to [EasyList](https://github.com/easylist/easylist) to request removal of the rule. This resolves the issue for all users once the filter list updates.

---

# Contextual menu

> Add one-click AI integrations to your docs.

The contextual menu provides quick access to AI-optimized content and direct integrations with popular AI tools. When users select the contextual menu on any page, they can copy content as context for AI tools or open conversations in ChatGPT, Claude, Perplexity, or a custom tool of your choice with your documentation already loaded as context.

## ​Menu options

 The contextual menu includes several pre-built options that you can enable by adding their identifier to your configuration.

| Option | Identifier | Description |
| --- | --- | --- |
| Copy page | copy | Copies the current page as Markdown for pasting as context into AI tools |
| View as Markdown | view | Opens the current page as Markdown |
| Open in ChatGPT | chatgpt | Creates a ChatGPT conversation with the current page as context |
| Open in Claude | claude | Creates a Claude conversation with the current page as context |
| Open in Perplexity | perplexity | Creates a Perplexity conversation with the current page as context |
| Copy MCP server URL | mcp | Copies your MCP server URL to the clipboard |
| Connect to Cursor | cursor | Installs your hosted MCP server in Cursor |
| Connect to VS Code | vscode | Installs your hosted MCP server in VS Code |
| Custom options | Object | Add custom options to the contextual menu |

 ![The expanded contextual menu showing the Copy page, View as Markdown, Open in ChatGPT, and Open in Claude menu items.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/contextual-menu/contextual-menu.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=b37c2bfffdc0db86422a7f7e692adaf7)

## ​Enabling the contextual menu

 Add the `contextual` field to your `docs.json` file and specify which options you want to include.

```
{
 "contextual": {
   "options": [
     "copy",
     "view",
     "chatgpt",
     "claude",
     "perplexity",
     "mcp",
     "cursor",
     "vscode"
   ]
 }
}
```

## ​Adding custom options

 Create custom options in the contextual menu by adding an object to the `options` array. Each custom option requires these properties: [​](#param-title)titlestringrequiredThe title of the option. [​](#param-description)descriptionstringrequiredThe description of the option. Displayed beneath the title when the contextual menu is expanded. [​](#param-icon)iconstringrequiredThe icon to display.Options:

- [Font Awesome icon](https://fontawesome.com/icons) name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `fontawesome` in your `docs.json`
- [Lucide icon](https://lucide.dev/icons) name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `lucide` in your `docs.json`
- URL to an externally hosted icon
- Path to an icon file in your project

 [​](#param-icon-type)iconTypestringThe [Font Awesome](https://fontawesome.com/icons) icon style. Only used with Font Awesome icons.Options: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands`. [​](#param-href)hrefstring | objectrequiredThe href of the option. Use a string for simple links or an object for dynamic links with query parameters.

Show href object

[​](#param-base)basestringrequiredThe base URL for the option.[​](#param-query)queryobjectrequiredThe query parameters for the option.

Show query object

[​](#param-key)keystringrequiredThe query parameter key.[​](#param-value)valuestringrequiredThe query parameter value. We will replace the following placeholders with the corresponding values:

- Use `$page` to insert the current page content in Markdown.
- Use `$path` to insert the current page path.
- Use `$mcp` to insert the hosted MCP server URL.

 Example custom option:

```
{
    "contextual": {
        "options": [
            "copy",
            "view",
            "chatgpt",
            "claude",
            "perplexity",
            {
                "title": "Request a feature",
                "description": "Join the discussion on GitHub to request a new feature",
                "icon": "plus",
                "href": "https://github.com/orgs/mintlify/discussions/categories/feature-requests"
            }
        ]
    }
}
```

### ​Custom option examples

Simple link

```
{
  "title": "Request a feature",
  "description": "Join the discussion on GitHub",
  "icon": "plus",
  "href": "https://github.com/orgs/mintlify/discussions/categories/feature-requests"
}
```

Dynamic link with page content

```
{
  "title": "Share on X",
  "description": "Share this page on X",
  "icon": "x",
  "href": {
    "base": "https://x.com/intent/tweet",
    "query": [
      {
      "key": "text",
      "value": "Check out this documentation: $page"
      }
    ]
  }
}
```

---

# Discord bot

> Add a bot to your Discord server that answers questions based on your documentation.

Discord integrations are available on [Pro and Custom plans](https://mintlify.com/pricing?ref=discord) with access to the assistant. The Discord bot supports your community with real-time answers from your documentation. The bot uses the Mintlify assistant to search your docs and provide accurate, cited responses, so it is always up-to-date. The Discord bot only works in public channels. It replies to `@` mentions or to all messages in a specific channel. Each message sent by the Discord bot counts toward your assistant message usage.

## ​Add the Discord bot to your server

 You must have the “Manage Server” permission in Discord to add the bot.

1. Navigate to the [Assistant](https://dashboard.mintlify.com/products/assistant) page in your dashboard.
2. In the Discord card, click **Configure**. This opens Discord. ![The connected apps section of the assistant page.](https://mintcdn.com/mintlify/iWC1DRgIiF7skzGL/images/assistant/connected-apps-light.png?fit=max&auto=format&n=iWC1DRgIiF7skzGL&q=85&s=647b6ec148afcbb3177e536cba7f858e)![The connected apps section of the assistant page.](https://mintcdn.com/mintlify/iWC1DRgIiF7skzGL/images/assistant/connected-apps-dark.png?fit=max&auto=format&n=iWC1DRgIiF7skzGL&q=85&s=cc2ef191b665b1042d1130d28b9346f2)
3. In Discord, select the server you want to add the bot to.
4. Authorize the bot to access your server.
5. Mention the bot to add it to a channel. The bot’s default name is `@Mintlify Bot`.

## ​Create an#ask-aichannel

 To help your community quickly get answers to their questions, the bot can reply to every message in a channel that you choose. By default, the bot replies to every message in channels named `#ask-ai`. Create an `#ask-ai` channel and let your community know that the bot will reply to messages in that channel. If you want the bot to reply to messages in a different channel, select a channel in the Discord bot [configuration menu](https://dashboard.mintlify.com/products/assistant/settings/integrations). ![The Discord configuration panel in light mode.](https://mintcdn.com/mintlify/nZ_rhnFbeRPc80xO/images/assistant/discord-configure-light.png?fit=max&auto=format&n=nZ_rhnFbeRPc80xO&q=85&s=daeb71b6661d36ec7f64b4edc64222e2)![The Discord configuration panel in dark mode.](https://mintcdn.com/mintlify/nZ_rhnFbeRPc80xO/images/assistant/discord-configure-dark.png?fit=max&auto=format&n=nZ_rhnFbeRPc80xO&q=85&s=39c6abfb3380410858bd4e6ec84f3d16) See [Starting Your First Discord Server](https://discord.com/blog/starting-your-first-discord-server) on the Discord blog for more information on creating a channel.

## ​Manage the Discord bot

 After you add the Discord bot to your server, you can manage or remove the bot from the [Integrations](https://dashboard.mintlify.com/products/assistant/settings/integrations) tab in your dashboard. In the Discord bot configuration menu, customize the bot by changing its avatar or name, and choose which channel it automatically replies to all messages in.

---

# llms.txt

> Optimize your docs for LLMs to read and index.

The [llms.txt file](https://llmstxt.org) is an industry standard that helps LLMs index content more efficiently, similar to how a sitemap helps search engines. AI tools can use this file to understand your documentation structure and find content relevant to user queries. Mintlify automatically hosts an `llms.txt` file at the root of your project that lists all available pages in your documentation. This file is always up to date and requires zero maintenance. You can optionally add a custom `llms.txt` file to the root of your project. View your `llms.txt` by appending `/llms.txt` to your documentation site’s URL. [Open the llms.txt for this site.](https://mintlify.com/docs/llms.txt)

## ​llms.txt structure

 An `llms.txt` file is a plain Markdown file that contains:

- **Site title** as an H1 heading.
- **Structured content sections** with links and a description of each page in your documentation.

 Pages are listed alphabetically in the order they appear in your repository, starting from the root directory. Each page’s description comes from the `description` field in its frontmatter. Pages without a `description` field appear in the `llms.txt` file without a description. Example llms.txt

```
# Site title

## Docs

- [API](https://example.com/docs/api): Endpoint list and usage
- [Install](https://example.com/docs/install): Setup steps
- [Getting started](https://example.com/docs/start): Intro guide
```

 This structured approach allows LLMs to efficiently process your documentation at a high level and locate relevant content for user queries, improving the accuracy and speed of AI-assisted documentation searches.

## ​llms-full.txt

 The `llms-full.txt` file combines your entire documentation site into a single file as context for AI tools and is indexed by LLM traffic. Mintlify automatically hosts an `llms-full.txt` file at the root of your project. View your `llms-full.txt` by appending `/llms-full.txt` to your documentation site’s URL. [Open the llms-full.txt for this site.](https://mintlify.com/docs/llms-full.txt)

## ​Custom files

 To add a custom `llms.txt` or `llms-full.txt` file, create an `llms.txt` or `llms-full.txt` file at the root of your project. Adding a custom file will override the automatically generated file of the same name. If you delete a custom file, the default file will be used again. Your custom `llms.txt` or `llms-full.txt` file must have a site title as an H1 heading. Other content is optional. See [Format](https://llmstxt.org/#format) in the `llms.txt` specification for more information on optional sections and best practices.

---

# Markdown export

> Quickly get Markdown versions of pages for AI tools and integrations.

Markdown provides structured text that AI tools can process more efficiently than HTML, which results in better response accuracy, faster processing times, and lower token usage. Mintlify automatically generates Markdown versions of pages that are optimized for AI tools and external integrations.

## ​.md URL extension

 Add `.md` to any page’s URL to view a Markdown version. [Open this page as Markdown](https://mintlify.com/docs/ai/markdown-export.md)

## ​Keyboard shortcut

 Press Command + C (Ctrl + C on Windows) to copy a page as Markdown to your clipboard.

---

```
> ## Documentation Index
> Fetch the complete documentation index at: https://www.mintlify.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Markdown export

> Quickly get Markdown versions of pages for AI tools and integrations.

export const PreviewButton = ({children, href}) => {
  return <a href={href} className="text-sm font-medium text-white dark:!text-zinc-950 bg-zinc-900 hover:bg-zinc-700 dark:bg-zinc-100 hover:dark:bg-zinc-300 rounded-full px-3.5 py-1.5 not-prose">
        {children}
      </a>;
};

Markdown provides structured text that AI tools can process more efficiently than HTML, which results in better response accuracy, faster processing times, and lower token usage.

Mintlify automatically generates Markdown versions of pages that are optimized for AI tools and external integrations.

## .md URL extension

Add `.md` to any page's URL to view a Markdown version.

<PreviewButton href="https://mintlify.com/docs/ai/markdown-export.md">Open this page as Markdown</PreviewButton>

## Keyboard shortcut

Press <kbd>Command</kbd> + <kbd>C</kbd> (<kbd>Ctrl</kbd> + <kbd>C</kbd> on Windows) to copy a page as Markdown to your clipboard.
```

---

# Model Context Protocol

> Connect your documentation and API endpoints to AI tools with a hosted MCP server.

## ​About MCP servers

 The Model Context Protocol (MCP) is an open protocol that creates standardized connections between AI applications and external services, like documentation. Mintlify generates an MCP server from your documentation, preparing your content for the broader AI ecosystem where any MCP client like Claude, Cursor, Goose, ChatGPT, and others can connect to your documentation. Your MCP server exposes a search tool for AI applications to query your documentation. Your users must connect your MCP server to their tools.

### ​How MCP servers work

 When an AI application connects to your documentation MCP server, it can search your documentation directly instead of making a generic web search in response to a user’s prompt. Your MCP server provides access to all indexed content on your documentation site.

- The AI application can proactively search your documentation while generating a response, not just when explicitly asked.
- The AI application determines when to use the search tool based on the context of the conversation and the relevance of your documentation.
- Each search (tool call) happens during the generation process, so the AI application searches up-to-date information from your documentation to generate its response.

 Some AI tools like Claude support both MCP and Skills. MCP gives the AI access to your documentation content, while Skills instruct the AI how to use that content effectively. They’re complementary. MCP provides the data and Skills provide the instructions.

### ​Search filtering parameters

 The MCP search tool supports optional filtering parameters that AI applications can use to narrow search results.

- **version**: Filter results to a specific documentation version. For example, `'v0.7'`. Only returns content tagged with the specified version or content available across all versions.
- **language**: Filter results to a specific language code. For example, `'en'`, `'zh'`, or `'es'`. Only returns content in the specified language or content available across all languages.
- **apiReferenceOnly**: When set to `true`, only returns API reference documentation pages.
- **codeOnly**: When set to `true`, only returns code snippets and examples.

 AI applications determine when to apply these filters based on the context of the user’s query. For example, if a user asks about a specific API version or requests code examples, the AI application may automatically apply the appropriate filters to provide more relevant results.

### ​MCP compared to web search

 AI tools can search the web, but MCP provides distinct advantages for documentation.

- **Direct source access**: Web search depends on what search engines have indexed, which may be stale or incomplete. MCP searches your current indexed documentation directly.
- **Integrated workflow**: MCP allows the AI to search during response generation rather than performing a separate web search.
- **No search noise**: SEO and ranking algorithms influence web search results. MCP goes straight to your documentation content.

## ​Access your MCP server

 MCP servers are only available for public documentation. Documentation behind end-user authentication cannot generate an MCP server. Mintlify automatically generates an MCP server for your documentation and hosts it at your documentation URL with the `/mcp` path. For example, Mintlify’s MCP server is available at `https://mintlify.com/docs/mcp`. View and copy your MCP server URL on the [MCP server page](https://dashboard.mintlify.com/products/mcp) in your dashboard. ![MCP server page in the dashboard.](https://mintcdn.com/mintlify/l_uyIoyoCoduAB2a/images/mcp/mcp-server-page-light.png?fit=max&auto=format&n=l_uyIoyoCoduAB2a&q=85&s=fe99ba970692e913694abeda27db201f)![MCP server page in the dashboard.](https://mintcdn.com/mintlify/l_uyIoyoCoduAB2a/images/mcp/mcp-server-page-dark.png?fit=max&auto=format&n=l_uyIoyoCoduAB2a&q=85&s=81739348dcafa3573ecc588a8ca38fbe) Hosted MCP servers use the `/mcp` path in their URLs. Other navigation elements cannot use the `/mcp` path.

## ​Content filtering and indexing

 Your MCP server searches content that Mintlify indexes from your documentation repository. File processing and search indexing control what content is available through your MCP server.

### ​File processing with.mintignore

 If files match [.mintignore](https://mintlify.com/docs/organize/mintignore) patterns, Mintlify does not process or index them. These files are not available through your MCP server.

### ​Search indexing withdocs.json

 By default, Mintlify only indexes pages included in your `docs.json` navigation for search through your MCP server. Mintlify excludes [hidden pages](https://mintlify.com/docs/organize/hidden-pages) (pages not in your navigation) from the search index unless you choose to index all pages. To include hidden pages in your MCP server’s search results, add the `seo.indexing` property to your `docs.json`.

```
"seo": {
    "indexing": "all"
}
```

 To exclude a specific page from search indexing, add `noindex: true` to its frontmatter.

```
---
title: "Hidden page"
description: "This page is not in the navigation and is not available through search."
noindex: true
---
```

## ​Use your MCP server

 Your users must connect your MCP server to their preferred AI tools.

1. Make your MCP server URL publicly available.
2. Users copy your MCP server URL and add it to their tools.
3. Users access your documentation through their tools.

 These are some of the ways you can help your users connect to your MCP server:

- Contextual menu
- Claude
- Claude Code
- Cursor
- VS Code

Add options in the [contextual menu](https://mintlify.com/docs/ai/contextual-menu) for your users to connect to your MCP server from any page of your documentation.

| Option | Identifier | Description |
| --- | --- | --- |
| Copy MCP server URL | mcp | Copies your MCP server URL to the user’s clipboard. |
| Connect to Cursor | cursor | Installs your MCP server in Cursor. |
| Connect to VS Code | vscode | Installs your MCP server in VS Code. |

1

Get your MCP server URL.

Navigate to your [dashboard](https://dashboard.mintlify.com/products/mcp) and find your MCP server URL.2

Publish your MCP server URL for your users.

Create a guide for your users that includes your MCP server URL and the steps to connect it to Claude.

1. Navigate to the [Connectors](https://claude.ai/settings/connectors) page in the Claude settings.
2. Select **Add custom connector**.
3. Add your MCP server name and URL.
4. Select **Add**.
5. When using Claude, select the attachments button (the plus icon).
6. Select your MCP server.

See the [Model Context Protocol documentation](https://modelcontextprotocol.io/docs/tutorials/use-remote-mcp-server#connecting-to-a-remote-mcp-server) for more details.1

Get your MCP server URL.

Navigate to your [dashboard](https://dashboard.mintlify.com/products/mcp) and find your MCP server URL.2

Publish your MCP server URL for your users.

Create a guide for your users that includes your MCP server URL and the command to connect it to Claude Code.

```
claude mcp add --transport http <name> <url>
```

See the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/mcp#installing-mcp-servers) for more details.1

Get your MCP server URL.

Navigate to your [dashboard](https://dashboard.mintlify.com/products/mcp) and find your MCP server URL.2

Publish your MCP server URL for your users.

Create a guide for your users that includes your MCP server URL and the steps to connect it to Cursor.

1. Use Command + Shift + P (Ctrl + Shift + P on Windows) to open the command palette.
2. Search for “Open MCP settings”.
3. Select **Add custom MCP**. This opens the `mcp.json` file.
4. In `mcp.json`, configure your server:

```
{
  "mcpServers": {
    "<your-mcp-server-name>": {
      "url": "<your-mcp-server-url>"
    }
  }
}
```

See the [Cursor documentation](https://docs.cursor.com/en/context/mcp#installing-mcp-servers) for more details.1

Get your MCP server URL.

Navigate to your [dashboard](https://dashboard.mintlify.com/products/mcp) and find your MCP server URL.2

Publish your MCP server URL for your users.

Create a guide for your users that includes your MCP server URL and the steps to connect it to VS Code.

1. Create a `.vscode/mcp.json` file.
2. In `mcp.json`, configure your server:

```
{
  "servers": {
    "<your-mcp-server-name>": {
      "type": "http",
      "url": "<your-mcp-server-url>"
    }
  }
}
```

See the [VS Code documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more details.

### ​Example: Connect to the Mintlify MCP server

 Connect to the Mintlify MCP server to search this documentation site within your preferred AI tool. This gives you more accurate answers about how to use Mintlify in your local environment and demonstrates how you can help your users connect to your MCP server.

- Contextual menu
- Claude
- Claude Code
- Cursor
- VS Code

At the top of this page, select the contextual menu and choose **Connect to Cursor** or **Connect to VS Code** to connect the Mintlify MCP server to the IDE of your choice.To use the Mintlify MCP server with Claude:1

Add the Mintlify MCP server to Claude

1. Navigate to the [Connectors](https://claude.ai/settings/connectors) page in the Claude settings.
2. Select **Add custom connector**.
3. Add the Mintlify MCP server:

- Name: `Mintlify`
- URL: `https://mintlify.com/docs/mcp`

1. Select **Add**.

2

Access the MCP server in your chat

1. When using Claude, select the attachments button (the plus icon).
2. Select the Mintlify MCP server.
3. Ask Claude a question about Mintlify.

See the [Model Context Protocol documentation](https://modelcontextprotocol.io/docs/tutorials/use-remote-mcp-server#connecting-to-a-remote-mcp-server) for more details.To use the Mintlify MCP server with Claude Code, run the following command:

```
claude mcp add --transport http Mintlify https://mintlify.com/docs/mcp
```

Test the connection by running:

```
claude mcp list
```

See the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/mcp#installing-mcp-servers) for more details.[Install in Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=mintlify&config=eyJ1cmwiOiJodHRwczovL21pbnRsaWZ5LmNvbS9kb2NzL21jcCJ9)To connect the Mintlify MCP server to Cursor, click the **Install in Cursor** button. Or to manually connect the MCP server, follow these steps:1

Open MCP settings

1. Use Command + Shift + P (Ctrl + Shift + P on Windows) to open the command palette.
2. Search for “Open MCP settings”.
3. Select **Add custom MCP**. This opens the `mcp.json` file.

2

Configure the Mintlify MCP server

In `mcp.json`, add:

```
{
  "mcpServers": {
    "Mintlify": {
      "url": "https://mintlify.com/docs/mcp"
    }
  }
}
```

3

Test the connection

In Cursor’s chat, ask “What tools do you have available?” Cursor should show the Mintlify MCP server as an available tool.See [Installing MCP servers](https://docs.cursor.com/en/context/mcp#installing-mcp-servers) in the Cursor documentation for more details.[Install in VS Code](https://vscode.dev/redirect/mcp/install?name=mintlify&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fmintlify.com%2Fdocs%2Fmcp%22%7D)To connect the Mintlify MCP server to VS Code, click the **Install in VS Code** button. Or to manually connect the MCP server, create a `.vscode/mcp.json` file and add:

```
{
  "servers": {
    "Mintlify": {
      "type": "http",
      "url": "https://mintlify.com/docs/mcp"
    }
  }
}
```

See the [VS Code documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more details.

### ​Using multiple MCP servers

 Users can connect multiple MCP servers to their AI tools. Connected MCP servers do not consume context until the AI calls a search tool. The AI decides when to search based on query relevance, so it doesn’t search every connected server for every question. When the AI searches, each query returns multiple results that add to the conversation’s context. If the AI searches several servers for a single question, this can use up significant context. Best practices for using multiple MCP servers:

- Connect only the MCP servers relevant to your current work.
- Be specific in your prompts so the AI searches the most relevant server.
- Disconnect servers you’re not actively using to reduce potential context usage.

---

# skill.md

> Make your docs agent-ready with a structured capability file.

Mintlify hosts a `skill.md` file at the root of your project that describes what AI agents can do with your product. The [skill.md specification](https://agentskills.io/specification) is a structured, machine-readable format that makes capabilities, required inputs, and constraints for products explicit so that agents can use them more reliably. Mintlify automatically generates a `skill.md` file for your project by analyzing your documentation with an agentic loop. This file stays up to date as you make updates to your documentation and requires no maintenance. You can optionally add a custom `skill.md` file to the root of your project that overrides the automatically generated one. View your `skill.md` by appending `/skill.md` to your documentation site’s URL. Mintlify only generates `skill.md` files for documentation sites that are public. [Open the skill.md for this site.](https://mintlify.com/docs/skill.md) Both `llms.txt` and `skill.md` files help agents work with your documentation, but they serve different purposes.

- `llms.txt` is a directory. It lists all your documentation pages with descriptions so agents know where to find information.
- `skill.md` is a capability summary. It tells agents what they can accomplish with your product, what inputs they need, and what constraints apply.

## ​Useskill.mdfiles with agents

 If you use a [reverse proxy](https://mintlify.com/docs/deploy/reverse-proxy), configure it to forward `/skill.md` and `/.well-known/skills/*` paths (with caching disabled) to your Mintlify subdomain. Agents can process your `skill.md` with the [skills CLI](https://www.npmjs.com/package/skills).

```
npx skills add your-docs-domain.com
```

 This adds your product’s capabilities to the agent’s context so it can take actions on behalf of users. Teach your users how to use `skill.md` files with agents so that they have better results using your product with their AI tools.

## ​skill.mdstructure

 Mintlify generates a `skill.md` file following the [agentskills.io specification](https://agentskills.io/specification). The generated file includes:

- **Metadata**: Project name, description, and version.
- **Capabilities**: What agents can accomplish with your product.
- **Skills**: Specific actions organized by category.
- **Workflows**: Step-by-step procedures for common tasks.
- **Integration**: Supported tools and services.
- **Context**: Background on your product’s architecture.

## ​Customskill.mdfiles

 Add a `skill.md` file to the root of your project to override the automatically generated file. If you delete a custom file, Mintlify generates a new `skill.md` file. Write a custom file when you want precise control over how agents interact with your product. Follow the [agentskills.io specification](https://agentskills.io/specification) to ensure compatibility with agent tooling.

### ​Frontmatter fields

 Custom `skill.md` files must start with YAML frontmatter.

| Field | Type | Description |
| --- | --- | --- |
| name | string | The name of your skill. |
| description | string | A brief description of what your skill does. |
| license | string | The license for your skill (for example,MITorApache-2.0). |
| compatibility | string | Requirements or compatibility notes (for example, runtime dependencies). |
| metadata | object | Additional metadata as string key-value pairs (for example,authororversion). |
| allowed-tools | string | Space-delimited list of pre-approved tools the skill may use (experimental). |

 Example frontmatter

```
---
name: mintlify
description: Build and maintain documentation sites with Mintlify. Use when creating docs pages, configuring navigation, adding components, or setting up API references.
license: MIT
compatibility: Requires Node.js for CLI. Works with any Git-based workflow.
metadata:
  author: mintlify
  version: "1.0"
---
```

---

# Slack bot

> Add a bot to your Slack workspace that answers questions based on your documentation.

The Slack app is available for [Pro and Custom plans](https://mintlify.com/pricing?ref=slack-app) with access to the assistant. The Slack app adds a bot to your workspace that supports your community with real-time answers. The bot uses the Mintlify assistant to search your docs and provide accurate, cited responses, so it is always up-to-date. The bot can only see messages in channels you specifically add it to. It does not have global read access to your workspace. The bot responds to `@` mentions or to all messages in a specific channel that you configure. Each message sent by the bot counts toward your assistant message usage.

## ​Set up the Slack app

 You can only install the Slack app once per workspace. If you have multiple Mintlify deployments, you can only connect one deployment at a time to a workspace. You must disconnect the app from one deployment before connecting it to another. If your Slack Workspace Owner requires admin approval to install apps, ask them to approve the Mintlify Slack app before you add it.

1. Navigate to the [Assistant](https://dashboard.mintlify.com/products/assistant) page in your dashboard.
2. In the Slack card, click **Configure**. This opens Slack. ![The connected apps section of the assistant page.](https://mintcdn.com/mintlify/iWC1DRgIiF7skzGL/images/assistant/connected-apps-light.png?fit=max&auto=format&n=iWC1DRgIiF7skzGL&q=85&s=647b6ec148afcbb3177e536cba7f858e)![The connected apps section of the assistant page.](https://mintcdn.com/mintlify/iWC1DRgIiF7skzGL/images/assistant/connected-apps-dark.png?fit=max&auto=format&n=iWC1DRgIiF7skzGL&q=85&s=cc2ef191b665b1042d1130d28b9346f2)
3. Follow the Slack prompts to add the app to your workspace.
4. Mention the bot to add it to a channel. The bot’s default name is `@mintlify-assistant`.

## ​Create an#ask-aichannel

 To help your users quickly get answers to their questions, the bot can reply to every message in a channel that you choose. By default, the bot replies to every message in channels named `#ask-ai`. Create an `#ask-ai` channel and let your users know that the bot replies to messages in that channel. See [Create a channel](https://slack.com/help/articles/201402297-Create-a-channel) in the Slack Help Center for more information. If you want the bot to reply to messages in a different channel, select a channel in the Slack bot [configuration menu](https://dashboard.mintlify.com/products/assistant/settings/integrations). ![The Slack configuration panel in light mode.](https://mintcdn.com/mintlify/Cua8vliIsZB_FwDG/images/assistant/slack-configure-light.png?fit=max&auto=format&n=Cua8vliIsZB_FwDG&q=85&s=52112c0ed2e0d0767ef9ce9529e31b5b)![The Slack configuration panel in dark mode.](https://mintcdn.com/mintlify/Cua8vliIsZB_FwDG/images/assistant/slack-configure-dark.png?fit=max&auto=format&n=Cua8vliIsZB_FwDG&q=85&s=ac31230309042ad15238b57518038bf9)

## ​Manage the Slack app

 After you add the app to your workspace, you can manage or remove the app from the [Integrations](https://dashboard.mintlify.com/products/assistant/settings/integrations) tab. In the Slack bot configuration menu, customize the bot by changing its avatar or name, and choose which channel it automatically replies to all messages in.
