# Customize agent behavior and more

# Customize agent behavior

> Configure how the agent handles documentation tasks with AGENTS.md.

Create an `AGENTS.md` file in your repository to customize the agent’s behavior (`Agents.md` is also accepted). The agent reads this file and follows any instructions you provide. The agent searches for `AGENTS.md` files in two locations. It first checks the documentation directory, then the repository root. If you have `AGENTS.md` files in both locations, the agent uses the file in your documentation directory. Add any instructions that you want the agent to follow. The agent appends these instructions to its system prompt, so the instructions apply to all tasks, whether you use the agent in your dashboard, on Slack, or via the API.

## ​What to include in AGENTS.md

 Consider adding instructions for:

- **Style preferences**: Voice, tone, formatting, and terminology specific to your documentation.
- **Code standards**: Programming languages, frameworks, and coding conventions to use in examples.
- **Content requirements**: What sections or information to include for different types of pages.
- **Project context**: Specific details about your product, architecture, or user base that inform documentation decisions.

## ​Example AGENTS.md file

 AGENTS.md

```
# Documentation agent instructions

## Code examples
- Use TypeScript for all code examples. Our users are primarily TypeScript developers.
- Always include error handling in API call examples.
- Show both success and error response examples for all endpoints.
- Include import statements at the top of code examples.

## API documentation standards
- Every endpoint must document: authentication requirements, rate limits, and common error codes.
- Use real-world parameter values in examples (not foo/bar placeholders).
- Include a complete request/response cycle for each endpoint.

## Style and formatting
- Write for developers with 2-5 years of experience. Don't oversimplify, but explain non-obvious concepts.
- Use active voice and second person ("you").
- Date format: ISO 8601 (YYYY-MM-DD).
- When referencing UI elements, use bold: **Settings** button.

## What to include
- Add prerequisite sections to guides when users need API keys, environment setup, or dependencies.
- Include "Next steps" sections linking to related documentation.
- Add troubleshooting sections for common issues we see in support tickets.
```

---

# Write effective prompts

> Get better results from the agent with clear, focused prompts.

Think of the agent as a helpful assistant that needs your guidance to complete tasks. Give it clear instructions and context. More focused tasks are easier to complete, so break down complex projects into smaller steps.

## ​Make prompts specific and outcome-focused

 Generic prompts like `@mintlify Improve the onboarding page` apply general best practices, but may not improve content in the specific way that you were picturing. Try prompts based on outcomes you want your users to achieve or problems that they encounter.

- `@mintlify A lot of users have trouble installing the CLI. Review the onboarding page and update the docs so that users can easily install the CLI`
- `@mintlify Developers keep getting 401 errors when following our authentication guide. Review the auth docs and add clearer examples showing how to properly format the API key`

## ​Use broad prompts for maintenance tasks

 Use broad prompts for general content maintenance like fixing typos, updating redirects, or renaming a feature throughout your docs.

- `@mintlify Find and fix all typos in the docs`
- `@mintlify change all unordered lists to use * instead of -`

## ​Specify a domain name for multi-site organizations

 If you have multiple documentation sites, include the `subdomain` parameter in your message to specify which documentation set the agent should work on. To find your domain name, look at your dashboard URL for the documentation set you want to update. The domain name is the last part after your organization name. For example, if your dashboard URL is `https://dashboard.mintlify.com/org-name/domain-name`, your domain name is `domain-name`. Use the format `@mintlify subdomain=<your-domain-name> <your-prompt>` to prompt the agent to work on a specific documentation set.

- `@mintlify subdomain=public-docs Add a new section to the quickstart about inviting collaborators based on this PR`: Prompts the agent to update the quickstart only on the `public-docs` site.
- `@mintlify subdomain=customer-docs Update the auth docs for the new authentication method`: Prompts the agent to update the auth docs only on the `customer-docs` site.

---

# Quickstart

> Start using the agent in your dashboard to create documentation updates.

## ​Open the agent panel

 On desktop, the agent panel is resizable. On mobile devices, the agent opens in full-screen. To open the agent panel:

- From any page in your dashboard, use the keyboard shortcut ⌘+I (macOS) or Ctrl+I (Windows/Linux).
- On the [Overview](https://dashboard.mintlify.com/) page, click **Ask agent**.

### ​Agent panel views

 ![Views in the agent panel: new chat, suggestions, history, and settings.](https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-light.png?fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=1681b4b6cd03cf695f5dd6467965acaf)![Views in the agent panel: new chat, suggestions, history, and settings.](https://mintcdn.com/mintlify/lubmw3_7_2xANY_o/images/agent/views-dark.png?fit=max&auto=format&n=lubmw3_7_2xANY_o&q=85&s=25f8bac336a0a4bb0624ed8f70303fc3)

- **Chat**: Click the plus icon, , to start a new chat. In the chat view, send prompts to the agent to update or ask questions about your documentation. The agent creates pull requests based on your instructions and displays links to view the pull requests or open the changes in the web editor.
- **Suggestions**: If enabled, the suggestions panel shows suggested updates to your documentation based on pull request changes and users’ conversations with the assistant.
- **History**: Click the history icon, , to browse past conversations and continue working on previous requests. Click any conversation to load it in the chat view.
- **Settings**: Click the settings icon, , to configure the agent’s integrations and repository access.

 Start a new conversation with the agent for each task. This keeps the agent’s context focused and helps you associate conversations with specific projects.

## ​Connect your GitHub account

 By default, the agent opens pull requests attributed to the Mintlify bot. To attribute pull requests to you, connect your GitHub account on the [My profile](https://dashboard.mintlify.com/settings/account) page of the dashboard.

## ​Connect repositories as context

 The agent can only access repositories that you connect through the Mintlify GitHub App. Configure which repositories the agent can access in the agent panel **Settings** or in the [GitHub App settings](https://github.com/apps/mintlify/installations/new).

---

# Add the agent to Slack

> Use the agent in Slack to make documentation updates from conversations and capture team knowledge.

If your Slack Workspace Owner requires admin approval to install apps, ask them to approve the Mintlify app before you connect it.

## ​Connect your Slack workspace

1. Open the agent panel in your dashboard.
2. Click the **Settings** button. ![The settings button in light mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-settings-light.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=ecb555eecfddf7480baaaf7d2fd6bce9)![The settings button in dark mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-settings-dark.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=a3250fa23cac19e8914b7185ac24c6d0)
3. In the Slack integration section, click **Connect**.
4. Follow the Slack prompts to add the `mintlify` app to your workspace.
5. Follow the Slack prompts to link your Mintlify account to your Slack workspace.
6. Test that the agent is working and responds when you:
  - Send a direct message to it.
  - Mention it with `@mintlify` in a channel.

## ​Use the agent in Slack

 Once connected, you can:

- Send direct messages to the agent to use it privately to update your documentation.
- Mention `@mintlify` in a channel to use it publicly and collaboratively.
- Continue conversations in threads to iterate on changes.
- Share pull request links with the agent to update related documentation.

## ​Update documentation

 Use the agent to update your documentation with a new request or in an existing thread.

- **New request**: Send a direct message to the agent or mention `@mintlify` in a channel with instructions on what to update.
- **Existing thread**: Reply in the thread and mention `@mintlify` with instructions on what to update.

 The agent reads the context of the request or thread and creates a pull request in your connected repository with the updates.

## ​Best practices

- **Be specific**: Tell the agent exactly what you want documented and where it should go.
- **Add context**: If a thread doesn’t contain all the necessary information, include additional details in your message to the agent.
- **Review carefully**: You should always review pull requests that the agent creates before merging them.

---

# Agent suggestions

> Monitor Git repositories for changes and receive suggested documentation updates.

Agent suggestions are available on [Custom plans](https://mintlify.com/pricing?ref=autopilot). To enable suggestions for your organization, [contact our sales team](mailto:gtm@mintlify.com). You can allow the agent to suggest documentation updates from two sources.

- **Pull request changes**: Monitor selected Git repositories for code changes that require documentation updates.
- **Assistant conversations**: Analyze questions that users ask the assistant on your documentation site to identify content gaps.

 When the agent identifies potential documentation updates, it creates a suggestion in your dashboard with context to create a pull request. Use suggestions to proactively keep your documentation up to date when new features ship or to address common user questions.

## ​Prerequisites

 Before using suggestions, you must install the [Mintlify GitHub App](https://mintlify.com/docs/deploy/github) in your organization. The app must have access to your documentation repository and at least one other repository where code changes require documentation updates.

## ​Configure suggestions

 Configure which repositories the agent monitors and how you receive notifications in the agent settings. The settings page displays all the GitHub organizations and repositories the agent is monitoring. To access the agent settings:

1. Click the **Ask agent** button in your dashboard to open the agent panel.
2. Click the **Settings** button. ![The settings button in light mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-settings-light.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=ecb555eecfddf7480baaaf7d2fd6bce9)![The settings button in dark mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-settings-dark.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=a3250fa23cac19e8914b7185ac24c6d0)

### ​Monitor repositories

 The agent monitors all merged pull requests for each repository that you enable, regardless of which branch they’re merged into. A GitHub check named **Mintlify Autopilot** runs on pull requests in monitored repositories to analyze them for potential documentation updates. When you merge a pull request that requires documentation updates, the agent creates a suggestion in your dashboard. When you first enable monitoring for a repository, the agent creates suggestions for pull requests merged in the last seven days. This backfill only occurs if no suggestions already exist for that repository. You may see multiple suggestions appear immediately after enabling monitoring. If you disable monitoring, the agent immediately stops monitoring the repository. Any existing suggestions for that repository remain in your dashboard until you dismiss them.

### ​Conversation insights

 If you have access to the agent and the assistant, the agent creates suggestions from conversations that your users have with the assistant. The agent periodically analyzes assistant conversations and creates suggestions when it identifies patterns of questions that indicate missing or unclear documentation.

### ​Notifications

 Agent suggestions always appear in your dashboard. You can configure notifications to receive email or Slack direct messages when the agent creates new suggestions. If you don’t receive email notifications for suggestions, check your spam folder and add the email address `notifications@mintlify.com` to your safe sender list.

## ​Review suggestions

 The agent creates suggestions in your dashboard. Each suggestion shows the pull request or assistant conversation topic that triggered the suggestion, creation date, and proposed documentation updates. The **Ask agent** button in your dashboard displays the number of suggestions waiting for your review. ![The Ask agent button showing four suggestions in light mode.](https://mintcdn.com/mintlify/HWCrkYCTtCJkLU3u/images/suggestions/count-light.png?fit=max&auto=format&n=HWCrkYCTtCJkLU3u&q=85&s=ee43454f05cddd0e0a409d2fc62d32cc)![The Ask agent button showing four suggestions in dark mode.](https://mintcdn.com/mintlify/HWCrkYCTtCJkLU3u/images/suggestions/count-dark.png?fit=max&auto=format&n=HWCrkYCTtCJkLU3u&q=85&s=7077f4d4827154e6d73df75a6fb863e0)

### ​Create pull requests

 Add suggestions as context for the agent to create pull requests.

1. Click the **Ask agent** button in your dashboard to open the agent panel.
2. Click **Add to chat**.
3. Submit the prompt to the agent to open a pull request.

### ​Dismiss suggestions

 If a suggestion doesn’t require documentation updates or you’ve already addressed the changes, dismiss it to remove it from your dashboard.

1. Click the **Ask agent** button in your dashboard to open the agent panel.
2. Click the **Dismiss** button next to any suggestions that you want to dismiss.

 The suggestion is immediately removed from your dashboard. You cannot retrieve dismissed suggestions.

---

# Workflows

> Examples of using the agent in your documentation process.

The agent assists with many different documentation tasks. These workflows show some of the ways you can integrate the agent into your documentation process. Try an approach that fits how your team currently works and adapt it to your specific needs.

## ​Iterate on a prompt in a Slack thread

 Prompt the agent, then continue to mention it with `@mintlify` in the same thread to refine and iterate on the pull request that it creates. For example: `@mintlify Our quickstart page needs a new section on inviting collaborators`. Then `@mintlify The new section should be called "Inviting collaborators"`. Followed by any other iterations.

## ​Start with the agent, finish manually

 Prompt the agent to begin a project, then check out the branch it creates and finish the task in your local environment or the web editor. The agent can help you get started, then you can take over to complete the task. For example: `@mintlify Update the quickstart page to include information about inviting collaborators` and then checkout the branch to make any additional changes using your preferred method.

## ​Update docs when merging feature changes

 When you merge a feature pull request, share the PR link with the agent to update relevant docs. For example: `@mintlify This PR adds a new authentication method. Update the docs to include the new auth flow: [PR link]`.

## ​Generate release notes from a pull request

 Prompt the agent with a specific pull request to generate release notes or changelog updates based on the commit history. For example: `@mintlify Generate release notes for this PR: [PR link]`.

## ​Generate code examples

 Prompt the agent to generate code examples for features throughout your docs or on specific pages. For example: `@mintlify Generate a code example to make the authentication method easier to understand`.

## ​Review existing content

 Prompt the agent to review existing content for technical accuracy, style, grammar, or other issues. For example: `@mintlify Review the API rate limiting section. We changed limits last month`.

## ​Respond to user feedback

 Prompt the agent with feedback from your users to make focused updates to your docs. For example: `@mintlify Users are getting confused by step 3 in the setup guide. What might be making it unclear?`.

## ​Automate with the API

 Integrate the agent into your existing automation tools to automatically update documentation when code changes occur, trigger content reviews, or sync documentation updates across multiple repositories. Use the agent endpoints to [create jobs](https://mintlify.com/docs/api-reference/agent/create-agent-job), [get a specific job](https://mintlify.com/docs/api-reference/agent/get-agent-job), and [get all jobs](https://mintlify.com/docs/api-reference/agent/get-all-jobs). When creating jobs via the API, you can control whether pull requests open in draft mode using the `asDraft` parameter (defaults to `true`). Set `asDraft: false` to create non-draft pull requests ready for immediate review and merging in automated workflows. Learn how to set up API automation in the [Auto-update documentation when code is merged](https://mintlify.com/docs/guides/automate-agent) tutorial.
