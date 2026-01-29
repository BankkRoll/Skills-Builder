# Accessibility and more

# Accessibility

> Create documentation that as many people as possible can use with WCAG compliance.

When you create accessible documentation, you prioritize content design that makes your documentation usable by as many people as possible regardless of how they access and interact with your documentation. Accessible documentation improves the user experience for everyone. Your content is more clear, better structured, and easier to navigate. This guide offers some best practices for creating accessible documentation, but it is not exhaustive. You should consider accessibility an ongoing process. Technologies and standards change over time, which introduce new opportunities to improve documentation.

## ​What is accessibility?

 Accessibility (sometimes abbreviated as a11y for the number of letters between the first and last letters of “accessibility”) is intentionally designing and building websites and tools that as many people as possible can use. People with temporary or permanent disabilities should have the same level of access to digital technologies. And designing for accessibility benefits everyone, including people who access your website on mobile devices or slow networks. Accessible documentation follows web accessibility standards, primarily the [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG22/quickref/). These guidelines help ensure your content is perceivable, operable, understandable, and robust.

## ​Getting started with accessibility

 Making your documentation accessible is a process. You don’t have to fix everything all at once and you can’t do it only once. If you’re just beginning to implement accessibility practices for your documentation, consider a phased approach where you start with high-impact changes and build from there.

### ​First steps

 Here are three things you can do right now to improve the accessibility of your documentation:

1. **Runmint a11y** to identify accessibility issues in your content.
2. **Add alt text** to all images.
3. **Check your heading hierarchy** to ensure one H1 per page and headings follow sequential order.

### ​Plan your accessibility work

 The best workflow is the one that works for your team. Here is one way that you can approach accessibility work: **Phase 1: Images and structure**

- Review all images for descriptive alt text.
- Audit link text and replace generic phrases like “click here.”
- Fix heading hierarchy issues across your documentation.

 **Phase 2: Navigation and media**

- Test keyboard navigation on your documentation.
- Test screen reader support.
- Add captions and transcripts to embedded videos.
- Review color contrast.

 **Phase 3: Build it into your workflow**

- Run `mint a11y` before publishing new content.
- Include accessibility checks in your content review process.
- Test keyboard navigation when adding interactive features.
- Verify new external links and embeds include proper titles and descriptions.

 Starting small and building accessibility into your regular workflow makes it sustainable. Each improvement helps more users access your documentation successfully.

## ​Structure your content

 Well-structured content is easier to navigate and understand, especially for screen reader users who rely on headings to move through pages and people who use keyboard navigation.

### ​Use proper heading hierarchy

 Each page should have a single H1 heading, which is defined by the `title:` property in a page’s frontmatter. Use additional headings in order without skipping. For example, don’t skip from H2 to H4.

```

# Page title (H1)

## Main section (H2)

### Subsection (H3)

### Another subsection (H3)

## Another main section (H2)

# Page title (H1)

## Main section (H2)

#### Subsection (H4)

### Another subsection (H3)
```

 Headings at the same level should have unique names.

```

## Accessibility tips (H2)

### Write effective alt text (H3)

### Use proper color contrast (H3)

## Accessibility tips (H2)

### Tip (H3)

### Tip (H3)
```

### ​Write descriptive link text

 Link text should be meaningful and connected to the destination. Avoid vague phrases like “click here” or “read more.”

```

Learn how to [configure your navigation](/organize/navigation).

[Learn more](/organize/navigation).
```

### ​Keep content scannable

- Break up long paragraphs.
- Use lists for steps and options.
- Highlight information with callouts.

### ​Use proper table structure

 Use tables sparingly and only for tabular data that has meaning inherited from the column and row headers. When using tables, include headers so screen readers can associate data with the correct column:

```
| Feature | Status |
| ------- | ------ |
| Search  | Active |
| Analytics | Active |
```

## ​Write descriptive alt text

 Alt text makes images accessible to screen reader users and appears when images fail to load. Images in your documentation should have alt text that describes the image and makes it clear why the image is included. Even with alt text, you should not rely on images alone to convey information. Make sure your content describes what the image communicates.

### ​Write effective alt text

- **Be specific**: Describe what the image shows, not just that it’s an image.
- **Be concise**: Aim for one to two sentences.
- **Avoid redundancy**: Don’t start with “Image of” because screen readers will already know that the alt text is associated with an image. However, you should include descriptions like “Screenshot of” or “Diagram of” if that context is important to the image.

```

![Screenshot of the dashboard showing three active projects and two pending invitations](/images/dashboard.png)

![Dashboard screenshot](/images/dashboard.png)
```

### ​Add alt text to images

 For Markdown images, include alt text in the square brackets:

```
![Description of the image](/path/to/image.png)
```

 For HTML images, use the `alt` attribute:

```
<img
  src="/images/screenshot.png"
  alt="Settings panel with accessibility options enabled. The options are emphasized with an orange rectangle."
/>
```

### ​Add titles to embedded content

 Iframes and video embeds require descriptive titles:

```
<iframe
  src="https://www.youtube.com/embed/example"
  title="Tutorial: Setting up your first documentation site"
></iframe>
```

## ​Design for readability

 Visual design choices affect how accessible your documentation is to users with low vision, color blindness, or other visual disabilities.

### ​Ensure sufficient color contrast

 If you customize your theme colors, verify the contrast ratios meet WCAG requirements:

- Body text: minimum 4.5:1 contrast ratio
- Large text: minimum 3:1 contrast ratio
- Interactive elements: minimum 3:1 contrast ratio

 Test both light and dark mode. The `mint a11y` command checks for color contrast.

### ​Don’t rely on color alone

 If you use color to convey information, include a text label or icon as well. For example, don’t mark errors only with red text. Include an error icon or the word “Error.”

### ​Use clear, concise language

- Write in plain language.
- Define technical terms when first used.
- Avoid run-on sentences.
- Use active voice.

## ​Make code examples accessible

 Code blocks are a core part of technical documentation, but they require specific accessibility considerations to ensure screen reader users can understand them. In general, follow these guidelines:

- Break long code examples into smaller, logical chunks.
- Comment complex logic within the code.
- Consider providing a text description for complex algorithms.
- When showing file structure, use actual code blocks with language labels rather than ASCII art.

### ​Specify the programming language

 Always declare the language for syntax highlighting. This helps screen readers announce the code context to users:

```
```javascript
function getUserData(id) {
  return fetch(`/api/users/${id}`);
}
```
```

### ​Provide context around code

 Provide clear context for code blocks:

```
The following function fetches user data from the API:

```javascript
function getUserData(id) {
  return fetch(`/api/users/${id}`);
}
```

This returns a promise that resolves to the user object.
```

## ​Video and multimedia accessibility

 Videos, animations, and other multimedia content need text alternatives so all users can access the information they contain.

### ​Add captions to videos

 Captions make video content accessible to users who are deaf or hard of hearing. They also help users in sound-sensitive environments and non-native speakers:

- Use captions for all spoken content in videos.
- Include relevant sound effects in captions.
- Ensure captions are synchronized with the audio.
- Use proper punctuation and speaker identification when multiple people speak.

 Most video hosting platforms support adding captions. Upload caption files or use auto-generated captions as a starting point, then review for accuracy.

### ​Provide transcripts

 Transcripts offer an alternative way to access video content. They’re searchable, easier to reference, and accessible to screen readers:

```
<iframe
  src="https://www.youtube.com/embed/example"
  title="Tutorial: Setting up authentication"
></iframe>

<Accordion title="Video transcript">
In this tutorial, we'll walk through setting up authentication...
</Accordion>
```

 Place transcripts near the video or provide a clear link to access them.

### ​Consider alternatives to video-only content

 If critical information only appears in a video:

- Provide the same information in text form.
- Include key screenshots with descriptive alt text.
- Create a written tutorial that covers the same material.

 This ensures users who can’t access video content can still complete their task.

## ​Test your documentation

 Regular testing helps you catch accessibility issues before users encounter them.

### ​Check for accessibility issues withmint a11y

 Use the `mint a11y` CLI command to automatically scan your documentation for common accessibility issues:

```
mint a11y
```

 The command checks for:

- Missing alt text on images and videos.
- Insufficient color contrast.

 When the scan completes, review the reported issues and fix them in your content. Run the command again to verify your fixes. Use flags to check for specific accessibility issues.

```
# Check only for missing alt text
mint a11y --skip-contrast

# Check only for color contrast issues
mint a11y --skip-alt-text
```

### ​Basic keyboard navigation test

 Navigate through your documentation using only your keyboard:

1. Press Tab to move forward through interactive elements.
2. Press Shift + Tab to move backward.
3. Press Enter to activate links and buttons.
4. Verify all interactive elements are reachable and have visible focus indicators.

### ​Go deeper with accessibility testing

 For more comprehensive testing:

- **Screen readers**: Test with [NVDA (Windows)](https://www.nvaccess.org/) or [VoiceOver (Mac)](https://www.apple.com/accessibility/voiceover/).
- **Browser extensions**: Install [axe DevTools](https://www.deque.com/axe/browser-extensions/) or [WAVE](https://wave.webaim.org/extension/) to scan pages for issues.
- **WCAG guidelines**: Review the [Web Content Accessibility Guidelines](https://www.w3.org/WAI/WCAG22/quickref/) for detailed standards.

## ​Additional resources

 Continue learning about accessibility with these trusted resources:

- **WebAIM**: Practical articles and tutorials on web accessibility
- **The A11y Project**: Community-driven accessibility resources and checklist
- **W3C Web Accessibility Initiative (WAI)**: Official accessibility standards and guidance

---

# Tutorial: Build an in

> Embed the assistant in your application to answer questions with information from your documentation.

Embed the assistant in your application to answer questions with information from your documentation.

---

# Tutorial: Auto

> Use the agent API to automatically update your documentation.

## ​What you will build

 An automation that updates your documentation when code is pushed to your main branch. The workflow can be built on multiple platforms, including GitHub Actions and n8n. It watches your code repository and then calls the agent API to update your documentation in a separate documentation repository. This workflow connects two separate repositories:

- **Code repository**: Where you store application code. You’ll set up the automation trigger on this repository. Examples include a backend API, frontend app, SDK, or CLI tool.
- **Documentation repository**: Where you store your documentation and connect to your Mintlify project. The agent creates pull requests with documentation updates in this repository.

 This tutorial assumes your documentation is in a separate repository from your application code. If you have a monorepo, modify the workflow to target the directory where you store your documentation.

### ​Workflow overview

1. Someone pushes code to your main branch.
2. The workflow triggers.
3. The workflow calls the agent API to update your documentation.
4. The agent creates a pull request with documentation updates in your documentation repository.

## ​Choose your platform

- GitHub Actions
- n8n

GitHub Actions is the simplest option if your code is already on GitHub. No additional services required.

## ​Prerequisites

- GitHub Actions enabled on your code and documentation repositories
- [Mintlify GitHub App](https://mintlify.com/docs/deploy/github) installed in both your code and documentation repositories
- [Mintlify admin API key](https://dashboard.mintlify.com/settings/organization/api-keys)
- [Mintlify project ID](https://dashboard.mintlify.com/settings/organization/api-keys)
- [Mintlify Pro or Custom plan](https://mintlify.com/pricing)
- Admin access to the GitHub repositories for your code and documentation

### ​Install the Mintlify app on your code repository

The Mintlify app must be installed on your code repository so the agent can fetch context from your codebase. To add the app to new repositories:

1. Open the agent panel in your Mintlify dashboard. ![The agent panel in light mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-light.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=56ee8c375606ca4a50b9b889474fc769)![The agent panel in dark mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-dark.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=ad82516ec69eb247ac0475fd3397c338)
2. Click the **Settings** button. ![The settings button in light mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-settings-light.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=ecb555eecfddf7480baaaf7d2fd6bce9)![The settings button in dark mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-settings-dark.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=a3250fa23cac19e8914b7185ac24c6d0)
3. Click **Add to New Organization**. This will take you to the app installation page on GitHub.
4. Select the repositories you want to grant access to from the list.
5. Save your changes.

### ​Get your admin API key

1. Navigate to the [API keys](https://dashboard.mintlify.com/settings/organization/api-keys) page in your dashboard.
2. Select **Create Admin API Key**.
3. Copy the key and save it securely.

## ​Build the workflow

### ​Create the workflow file

1. In your code repository, create a new file: `.github/workflows/update-docs.yml`
2. Add this workflow:
  ```
  name: Update Docs
  on:
    push:
      branches:
        - main
  jobs:
    update-docs:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/github-script@v8
          env:
            MINTLIFY_API_KEY: ${{ secrets.MINTLIFY_API_KEY }}
            PROJECT_ID: ${{ secrets.MINTLIFY_PROJECT_ID }}
          with:
            script: |
              const { owner, repo } = context.repo;
              const projectId = process.env.PROJECT_ID;
              const apiKey = process.env.MINTLIFY_API_KEY;
              if (!projectId || !apiKey) {
                core.setFailed('Missing MINTLIFY_PROJECT_ID or MINTLIFY_API_KEY secrets');
                return;
              }
              const url = `https://api.mintlify.com/v1/agent/${projectId}/job`;
              const payload = {
                branch: `mintlify/docs-update-${Date.now()}`,
                messages: [
                  {
                    role: 'system',
                    content: 'You are an action runner that updates documentation based on code changes. You should never ask questions. If you are not able to access the repository, report the error and exit.'
                  },
                  {
                    role: 'user',
                    content: `Update the documentation for our recent pushes to main:\n\nRepository: ${owner}/${repo}`
                  }
                ],
                asDraft: false
              };
              try {
                const response = await fetch(url, {
                  method: 'POST',
                  headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                  },
                  body: JSON.stringify(payload)
                });
                if (!response.ok) {
                  throw new Error(`API request failed with status ${response.status}: ${await response.text()}`);
                }
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';
                while (true) {
                  const { done, value } = await reader.read();
                  if (done) break;
                  buffer += decoder.decode(value, { stream: true });
                  const lines = buffer.split('\n');
                  buffer = lines.pop() || '';
                  for (const line of lines) {
                    if (line.trim()) {
                      console.log(line);
                    }
                  }
                }
                if (buffer.trim()) {
                  console.log(buffer);
                }
                core.notice(`Documentation update job triggered for ${owner}/${repo}`);
              } catch (error) {
                core.setFailed(`Failed to create documentation update job: ${error.message}`);
              }
  ```

### ​Add secrets

1. In your code repository, go to **Settings** → **Secrets and variables** → **Actions**.
2. Click **New repository secret**.
3. Add the following secrets:
  - Name: `MINTLIFY_API_KEY`, Secret: Your Mintlify admin API key
  - Name: `MINTLIFY_PROJECT_ID`, Secret: Your Mintlify project ID (found on the [API keys](https://dashboard.mintlify.com/settings/organization/api-keys) page of your dashboard)

For more information, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets) in the GitHub documentation.

## ​Test the automation

1. Make a small change in your code repository and push to main:
  ```
  git add .
  git commit -m "Test: trigger docs automation"
  git push origin main
  ```
2. Check the **Actions** tab in your code repository to see the workflow running.
3. After the workflow runs, check your documentation repository for a new branch and pull request with documentation updates.

## ​Troubleshooting

### ​Workflow not running

- Verify GitHub Actions is enabled in your code repository.
- Check the **Actions** tab for error messages.
- Ensure the workflow file is in `.github/workflows/` with a `.yml` extension.

### ​401 error from agent API

- Verify your API key starts with `mint_`.
- Check the Authorization header is formatted as `Bearer mint_yourkey`.
- Confirm the API key is for the correct Mintlify organization.

### ​No documentation updates appearing

- Check that the documentation repository is connected to your Mintlify project.
- Verify the agent has write access to the documentation repository.
- Check the workflow logs for error messages from the agent.

n8n provides a visual workflow editor and can integrate with multiple services.

## ​Prerequisites

- n8n workspace
- [Mintlify Pro or Custom plan](https://mintlify.com/pricing)
- Mintlify app installed on your code repository
- Mintlify admin API key
- Admin access to the GitHub repositories for your code and documentation
- GitHub personal access token

### ​Install the Mintlify app on your code repository

The Mintlify app must be installed on your code repository so the agent can fetch context from your codebase. To add the app to new repositories:

1. Open the agent panel in your Mintlify dashboard. ![The agent panel in light mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-light.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=56ee8c375606ca4a50b9b889474fc769)![The agent panel in dark mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-dark.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=ad82516ec69eb247ac0475fd3397c338)
2. Click the **Settings** button. ![The settings button in light mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-settings-light.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=ecb555eecfddf7480baaaf7d2fd6bce9)![The settings button in dark mode.](https://mintcdn.com/mintlify/l1-TgESjTbrqcwOU/images/agent/dashboard-settings-dark.png?fit=max&auto=format&n=l1-TgESjTbrqcwOU&q=85&s=a3250fa23cac19e8914b7185ac24c6d0)
3. Click **Add to New Organization**. This will take you to the app installation page on GitHub.
4. Select the repositories you want to grant access to from the list.
5. Save your changes.

### ​Get your admin API key

1. Navigate to the [API keys](https://dashboard.mintlify.com/settings/organization/api-keys) page in your dashboard.
2. Select **Create Admin API Key**.
3. Copy the key and save it securely.

### ​Get your GitHub personal access token

1. In GitHub, navigate to **Settings**.
2. Click **Developer settings**.
3. Click **Personal access tokens**.
4. Click **Tokens (classic)**.
5. Click **Generate new token (classic)**.
6. Select these scopes:
  - `repo` (full control of private repositories)
  - `admin:repo_hook` (if you want n8n to create webhooks)
7. Generate and save the token securely.

For more information, see [Creating a personal access token (classic)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens?versionId=free-pro-team%40latest&productId=account-and-profile#creating-a-personal-access-token-classic) in the GitHub documentation.

## ​Build the workflow

### ​Create the webhook trigger

1. In n8n, create a new workflow.
2. Add a webhook node.
3. Configure the webhook:
  - HTTP Method: `POST`
  - Path: `auto-update-documentation` (or any unique path)
  - Authentication: None
  - Respond: Immediately
4. Save the workflow.
5. Copy the production webhook URL. It looks like: `https://your-n8n-instance.app.n8n.cloud/webhook/auto-update-documentation`

![Screenshot of the configurations for the webhook node.](https://mintcdn.com/mintlify/MUT1RZiseS3dwdrU/images/guides/n8n/webhook-node.png?fit=max&auto=format&n=MUT1RZiseS3dwdrU&q=85&s=165a57aed92aa90d90609c5d381d29b7)

### ​Set up the GitHub webhook

1. Navigate to your code repository on GitHub.
2. Click **Settings**.
3. Click **Webhooks**.
4. Click **Add webhook**.
5. Configure the webhook:
  - Payload URL: Paste your n8n webhook URL
  - Content type: `application/json`
  - Which events would you like to trigger this webhook?
    - Select **Let me select individual events.**
    - Select only **Push events**.
  - Select **Active**
6. Click **Add webhook**.

### ​Filter for main branch pushes

Add a code node after the webhook to filter for pushes to main and extract the relevant information.

1. Add a code node.
2. Name it “Filter main pushes.”
3. Set mode to **Run Once for All Items**.
4. Add this JavaScript:

```
const webhookData = $input.first().json.body;

// Only continue if this is a push to main
if (webhookData.ref !== "refs/heads/main") {
  return [];
}

// Extract information
const repository = webhookData.repository;
const pusher = webhookData.pusher;

// Build message for agent
const agentMessage = `Update documentation for changes pushed to main in ${repository.name}. Always edit files and create a pull request.`;

return {
  json: {
    codeRepoName: repository.full_name,
    codeRepoShortName: repository.name,
    agentMessage: agentMessage
  }
};
```

![Screenshot of the configurations for the filter main pushes node.](https://mintcdn.com/mintlify/MUT1RZiseS3dwdrU/images/guides/n8n/filter-merged-PRs-node.png?fit=max&auto=format&n=MUT1RZiseS3dwdrU&q=85&s=a7661a96b0a5c6272e8a284edb8eb8f5)This code stops the workflow if the push wasn’t to main, extracts all relevant information from the GitHub webhook, and creates a message for the agent API.

### ​Call the agent API

Add an HTTP request node to create a documentation job.

1. Add an HTTP request node.
2. Name it “Create agent job.”
3. Configure the request:
  - Method: `POST`
  - URL: `https://api.mintlify.com/v1/agent/YOUR_PROJECT_ID/job` (replace `YOUR_PROJECT_ID` with your project ID from the [API keys](https://dashboard.mintlify.com/settings/organization/api-keys) page)
  - Authentication: Generic Credential Type → Header Auth
    - Create a new credential:
      - Name: `Authorization`
      - Value: `Bearer mint_YOUR_API_KEY` (replace with your API key)
  - Send Body: On
  - Body Content Type: JSON
  - Specify Body: Using JSON
  - Add this JSON:
  ```
  {
  "branch": "docs-update-from-{{ $json.codeRepoShortName }}-{{ $now.toISOString() }}",
  "messages": [
      {
      "role": "system",
      "content": "{{ $json.agentMessage }}"
      }
  ],
  "asDraft": false
  }
  ```

![Screenshot of the configurations for the create agent job node.](https://mintcdn.com/mintlify/jW5VvzJALf7BW1X_/images/guides/n8n/create-agent-job-node.png?fit=max&auto=format&n=jW5VvzJALf7BW1X_&q=85&s=2bbb162905564f80a30bb7d75c917815)The agent creates a pull request in your documentation repository using a descriptive branch name that includes the source repository name and timestamp.

### ​Activate the workflow

1. Save your workflow.
2. Set it to active.

Your workflow is now monitoring your code repository for pushes to main.![Screenshot of the automation workflow in the n8n editor.](https://mintcdn.com/mintlify/MUT1RZiseS3dwdrU/images/guides/n8n/workflow.png?fit=max&auto=format&n=MUT1RZiseS3dwdrU&q=85&s=55120ad3ffc9b32d56aefe05c6431324)

## ​Test the automation

1. Create a test branch in your code repository:
  ```
  git checkout -b test-docs-automation
  ```
2. Make a small change and commit it:
  ```
  git add .
  git commit -m "Test: trigger docs automation"
  git push origin test-docs-automation
  ```
3. Open a pull request on GitHub.
4. Merge the pull request.

### ​Verify the automation

You should see a new n8n execution with all nodes completed successfully, and a new branch and pull request in your documentation repository.

## ​Troubleshooting

### ​Webhook not triggering

- Verify the workflow is active in n8n.
- Check GitHub repository Settings → Webhooks → Recent Deliveries for the response code.
- Confirm the webhook URL matches your n8n webhook URL exactly.

### ​401 error from agent API

- Verify your API key starts with `mint_`.
- Check the Authorization header is formatted as `Bearer mint_yourkey`.
- Confirm the API key is for the correct Mintlify organization.

### ​401 error from GitHub

- Verify your token has the `repo` scope.
- Check that the token hasn’t expired.
- Confirm you included the `User-Agent` header in the GitHub request.

---

# Work with branches

> Create branches to preview changes and collaborate before publishing.

Branches are a feature of version control that point to specific commits in your repository. Your deployment branch, usually called `main`, represents the content used to build your live documentation site. All other branches are independent of your live docs unless you choose to merge them into your deployment branch. Branches let you create separate instances of your documentation to make changes, get reviews, and try new approaches before publishing. Your team can work on branches to update different parts of your documentation simultaneously without affecting what users see on your live site. The following diagram shows an example of a branch workflow where a feature branch is created, changes are made, and then the feature branch is merged into the main branch. We recommend always working from branches when updating documentation to keep your live site stable and enable review workflows.

## ​Branch naming conventions

 Use clear, descriptive names that explain the purpose of a branch. **Use**:

- `fix-broken-links`
- `add-webhooks-guide`
- `reorganize-getting-started`
- `ticket-123-oauth-guide`

 **Avoid**:

- `temp`
- `my-branch`
- `updates`
- `branch1`

## ​Create a branch

- Using web editor
- Using local development

1. Click the branch name in the editor.
2. Click **New Branch**.
3. Enter a descriptive name.
4. Click **Create Branch**.

1

Create a branch from your terminal

```
git checkout -b branch-name
```

This creates the branch and switches to it in one command.2

Push the branch to GitHub

```
git push -u origin branch-name
```

The `-u` flag sets up tracking so future pushes just need `git push`.

## ​Save changes on a branch

- Using web editor
- Using local development

Select the **Save as commit** button in the top-right of the editor toolbar. This creates a commit and pushes your work to your branch automatically.Stage, commit, and push your changes.

```
git add .
git commit -m "Describe your changes"
git push
```

## ​Switch branches

- Using web editor
- Using local development

1. Select the branch name in the editor toolbar.
2. Select the branch you want to switch to from the dropdown menu.

Unsaved changes are lost when switching branches. Save your work first.Switch to an existing branch:

```
git checkout branch-name
```

Or create and switch in one command:

```
git checkout -b new-branch-name
```

## ​Merge branches

 Once your changes are ready to publish, create a pull request to merge your branch into the deployment branch.

---

# Claude Code

> Configure Claude Code to write, review, and update your documentation.

Claude Code is an agentic command line tool that can help you maintain your documentation. It can write new content, review existing pages, and keep docs up to date. You can train Claude Code to understand your documentation standards and workflows by adding a `CLAUDE.md` file to your project and refining it over time.

## ​Getting started

 **Prerequisites:**

- Active Claude subscription (Pro, Max, or API access)

 **Setup:**

1. Install Claude Code:

```
npm install -g @anthropic-ai/claude-code
```

1. Navigate to your docs directory.
2. (Optional) Add the `CLAUDE.md` file below to your project.
3. Run `claude` to start.

## ​CLAUDE.md template

 Save a `CLAUDE.md` file at the root of your docs directory to help Claude Code understand your project. This file trains Claude Code on your documentation standards, preferences, and workflows. See [Manage Claude’s memory](https://docs.anthropic.com/en/docs/claude-code/memory) in the Anthropic docs for more information. Copy this example template or make changes for your docs specifications:

```
# Mintlify documentation

## Working relationship
- You can push back on ideas-this can lead to better documentation. Cite sources and explain your reasoning when you do so
- ALWAYS ask for clarification rather than making assumptions
- NEVER lie, guess, or make up anything

## Project context
- Format: MDX files with YAML frontmatter
- Config: docs.json for navigation, theme, settings
- Components: Mintlify components

## Content strategy
- Document just enough for user success - not too much, not too little
- Prioritize accuracy and usability
- Make content evergreen when possible
- Search for existing content before adding anything new. Avoid duplication unless it is done for a strategic reason
- Check existing patterns for consistency
- Start by making the smallest reasonable changes

## docs.json

- Refer to the [docs.json schema](https://mintlify.com/docs.json) when building the docs.json file and site navigation

## Frontmatter requirements for pages
- title: Clear, descriptive page title
- description: Concise summary for SEO/navigation

## Writing standards
- Second-person voice ("you")
- Prerequisites at start of procedural content
- Test all code examples before publishing
- Match style and formatting of existing pages
- Include both basic and advanced use cases
- Language tags on all code blocks
- Alt text on all images
- Relative paths for internal links

## Git workflow
- NEVER use --no-verify when committing
- Ask how to handle uncommitted changes before starting
- Create a new branch when no clear branch exists for changes
- Commit frequently throughout development
- NEVER skip or disable pre-commit hooks

## Do not
- Skip frontmatter on any MDX file
- Use absolute URLs for internal links
- Include untested code examples
- Make assumptions - always ask for clarification
```

## ​Sample prompts

 Once you have Claude Code set up, try these prompts to see how it can help with common documentation tasks. You can copy and paste these examples directly, or adapt them for your specific needs.

### ​Convert notes to polished docs

 Turn rough drafts into proper Markdown pages with components and frontmatter. **Example prompt:**

```
Convert this text into a properly formatted MDX page: [paste your text here]
```

### ​Review docs for consistency

 Get suggestions to improve style, formatting, and component usage. **Example prompt:**

```
Review the files in docs/ and suggest improvements for consistency and clarity
```

### ​Update docs when features change

 Keep documentation current when your product evolves. **Example prompt:**

```
Our API now requires a version parameter. Update our docs to include version=2024-01 in all examples
```

### ​Generate comprehensive code examples

 Create multi-language examples with error handling. **Example prompt:**

```
Create code examples for [your API endpoint] in JavaScript, Python, and cURL with error handling
```

## ​Extending Claude Code

 Beyond manually prompting Claude Code, you can integrate it with your existing workflows.

### ​Automation with GitHub Actions

 Run Claude Code automatically when code changes to keep docs up to date. You can trigger documentation reviews on pull requests or update examples when API changes are detected.

### ​Multi-instance workflows

 Use separate Claude Code sessions for different tasks - one for writing new content and another for reviewing and quality assurance. This helps maintain consistency and catch issues that a single session might miss.

### ​Team collaboration

 Share your refined `CLAUDE.md` file with your team to ensure consistent documentation standards across all contributors. Teams often develop project-specific prompts and workflows that become part of their documentation process.

### ​Custom commands

 Create reusable slash commands in `.claude/commands/` for frequently used documentation tasks specific to your project or team.

---

# Content templates

> Copy and modify these templates to quickly create documentation for different content types.

Use these templates as starting points for creating documentation. Customize the templates for your documentation and your audience.

1. Copy the template that matches your content type.
2. Replace placeholders and example content with your actual content.
3. Adjust sections as needed.
4. Remove any sections that don’t apply.

 Not sure which template to use? Read about [content types](https://mintlify.com/docs/guides/content-types) to understand when to use each one.

## ​How-to guide template

 Use how-to guides when users need to accomplish a specific task and already have some familiarity with your product. How-tos are goal-driven and get straight to the solution. How-to guide template

```
---
title: "[Titles should start with a verb]"
description: "[Do specific task] to [achieve outcome]."
---

Start with a brief statement of what this guide helps users accomplish.

## Prerequisites (optional)

List only what's necessary:

- Required setup or configuration
- Permissions needed
- Related features that should be configured first

## [Action-oriented heading describing the task]

Provide direct instructions focused on achieving the goal.

1. Open [location] and navigate to [specific place]
2. Click [button or option]
3. Enter [required information]
4. Click [confirmation button]

```language
// Include code examples that users can copy and modify
```

<Tip>
  Include practical tips that help users avoid common mistakes or work more efficiently.
</Tip>

## Verify the result (optional)

If success is ambiguous, explain how users can confirm they completed the task successfully.

## Troubleshooting (optional)

Address common issues users might encounter:

- **Problem description**: Solution or workaround
- **Another common issue**: How to resolve it

## Related tasks

Link to related how-to guides or next steps.
```

## ​Tutorial template

 Use tutorials when you want to help new users learn through hands-on practice. Tutorials guide users step-by-step through a complete learning experience with a clear outcome. Tutorial template

```
---
title: "[Action verb] [specific outcome]"
description: "Learn how to [specific outcome] by [method or approach]."
---

Use an introduction paragraph to explain what users will learn and what they'll be able to do after completing this tutorial.

## Prerequisites

List what users need before starting:

- Required knowledge or skills
- Tools, accounts, or permissions
- Time commitment (optional)

## Step 1: [First action]

Provide clear, specific instructions for the first step.

```language
// Include code examples where helpful
```

Explain what this step accomplishes and why it matters.

## Step 2: [Second action]

Continue with sequential steps that build on previous work.

Point out milestones and progress markers so users know they're on track.

## Step 3: [Third action]

Keep steps focused on concrete actions rather than theory.

Minimize choices that users need to make.

## Next steps

Summarize what users learned and suggest logical next steps:

- Related tutorials to try
- How-to guides for common tasks
- Additional resources for deeper learning
```

## ​Explanation template

 Use explanations when users need to understand concepts, design decisions, or how complex features work. Explanations provide context and deepen understanding rather than giving step-by-step instructions. Explanation template

```
---
title: "About [concept or feature]"
description: "Understand [concept] and how it works within [product or context]."
---

Start with a clear statement of what this explanation covers and why understanding it matters.

Define the concept in plain language. Explain what it is, what it does, and why it exists.

Use analogies or comparisons to familiar concepts when helpful.

## How [concept] works

Explain the underlying mechanics, architecture, or process.

<Frame>
  <img src="/path/to/diagram.png" alt="Diagram showing how [concept] works" />
</Frame>

Break down complex ideas into digestible sections.

## Why [design decision or approach]

Provide context about why things work the way they do.

Discuss trade-offs, alternatives that were considered, or constraints that influenced the design.

## When to use [concept]

Help users understand when this concept or approach is most appropriate.

- **Use case 1**: When this approach makes sense
- **Use case 2**: Another scenario where this is the right choice
- **Not recommended for**: Situations where alternatives are better

## Relationship to other features

Draw connections to related concepts or features in your product.

Explain how this concept fits into the broader system or workflow.

## Common misconceptions

Address misunderstandings or clarify subtle distinctions.

## Further reading

Link to related explanations, tutorials, or reference documentation.
```

## ​Reference template

 Use reference documentation when users need to look up specific details about your product’s functionality. Reference docs prioritize accuracy, consistency, and scannability. Reference template

```
---
title: "[Feature or API name] reference"
description: "Complete reference for [feature or API] properties, parameters, and options."
---

Provide a one-sentence description of what this feature or API does.

## Properties

<ParamField body="property1" type="string" required>
  Brief description of the property.
</ParamField>

<ParamField body="property2" type="number">
  Brief description with default value if applicable.
</ParamField>

<ParamField body="property3" type="boolean" default="false">
  Brief description.
</ParamField>

## Parameters

<ParamField body="parameterName" type="string">
  Description of what this parameter does and when to use it.

```language
// Example showing typical usage
```
</ParamField>

<ParamField body="anotherParameter" type="object">
  Description of the parameter.

  Available options:

  - `option1`: Description of this option.
  - `option2`: Description of this option.
</ParamField>

## Examples

### Basic example

```language title="Basic usage"
// Minimal example showing common use case
```

### Advanced example

```language title="Advanced configuration"
// Example with multiple options configured
```

## Response

If documenting an API, describe the response structure.

<ResponseField name="field1" type="string" required>
  Description of the response field.
</ResponseField>

<ResponseField name="field2" type="number">
  Description of another response field.
</ResponseField>

Example response:

```json
{
  "field1": "value",
  "field2": 123
}
```

## Related references

Link to related reference documentation.
```

## ​Related pages

 [Content typesChoose the right content type for your documentation goals.](https://mintlify.com/docs/guides/content-types)[Style and toneWrite effective documentation with consistent style.](https://mintlify.com/docs/guides/style-and-tone)[Format textLearn how to format text and style content.](https://mintlify.com/docs/create/text)
