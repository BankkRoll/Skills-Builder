# Content types and more

# Content types

> Choose the right content type for your documentation goals.

This page explains different content types, when to use each one, and how to approach writing for each type. Documentation should be organized around the specific goal you’re trying to help people achieve.

## ​Categorize using the Diátaxis framework

 The [Diátaxis framework](https://diataxis.fr) is a helpful guide for categorizing content based on your audience’s needs. Documentation can generally be mapped into one of these types:

1. Tutorials: Learning-oriented content for new users
2. How-to guides: Task-oriented guidance for specific problems
3. Explanations: Understanding-oriented conceptual discussions
4. Reference: Information-oriented technical descriptions

 Defining content types helps you plan documentation with a clear purpose and makes it easier for users to find what they need. ![A diagram of the Diátaxis framework showing four quadrants that correspond to the four content types: Tutorials, How-To Guides, Reference, and Explanation.](https://mintcdn.com/mintlify/mgh6fYMQy9DM5E4a/images/guides/best-practices/diataxis.webp?fit=max&auto=format&n=mgh6fYMQy9DM5E4a&q=85&s=057c36ac97446a5d360871e41852520e)

## ​Picking a type

| Question | Tutorial | How-To | Reference | Explanation |
| --- | --- | --- | --- | --- |
| What is the user’s goal? | Learn through practice | Solve a specific problem | Find precise information | Understand concepts |
| What is the user’s knowledge? | Beginner | Intermediate | Experienced | Any level |
| What is the primary focus? | Learning by doing | Achieving a goal | Providing information | Deepening understanding |
| How is the content structured? | Step-by-step | Problem-solution | Organized facts | Conceptual discussions |
| Is it task-oriented? | Yes, guided tasks | Yes, specific tasks | No, informational | No, conceptual |
| Is it designed for linear progression? | Yes | No | No | No |

## ​Writing for each type

### ​Tutorials (Learning-oriented)

- **Audience goal**: Learn something new through step-by-step instructions.
- **Characteristics**: Sequential and assumes no prior knowledge.
- **Writing approach**:
  - Set expectations of what the user will achieve after reading.
  - Use clear, incremental steps. Minimize choices that need to be made by the user.
  - Point out milestones along the way.
  - Minimize theory and focus on concrete actions.

### ​How-To Guides (Problem-oriented)

- **Audience goal**: Perform a specific task correctly.
- **Characteristics**: Goal-driven and assumes some prior knowledge.
- **Writing approach**:
  - Write from the perspective of the user, not the product.
  - Describe a logical sequence and omit unnecessary details.
  - Minimize context beyond what is necessary.

### ​Reference (Information-oriented)

- **Audience goal**: Find details about a product’s functionality.
- **Characteristics**: Unambiguous, product-focused, scannable.
- **Writing approach**:
  - Be scannable and concise.
  - Prioritize consistency.
  - Avoid explanatory content. Focus on examples that are easy to copy and modify.

### ​Explanation (Understanding-oriented)

- **Audience goal**: Expand general understanding of a concept or highly complex feature.
- **Characteristics**: Theoretical, potentially opinionated, broad in scope.
- **Writing approach**:
  - Provide background context, such as design decisions or technical constraints.
  - Acknowledge opinions and alternatives.
  - Draw connections to other areas in the product or industry.

## ​Tips and tricks

1. **Maintain purpose**: Before writing, assign each page a specific content type and make it top of mind in the doc throughout your writing.
2. **Consider content freshness**: Regardless of content type, try to optimize for evergreen documentation. If something represents a moment in time of what a feature looks like on a specific date, it’s probably better suited for a changelog or blog post than in your documentation. Or if something changes very frequently avoid putting it in your docs.
3. **Think like your users**: Consider different user personas when organizing content. See [Understand your audience](https://mintlify.com/docs/guides/understand-your-audience) for more information.
4. **Use templates**: Start with [content templates](https://mintlify.com/docs/guides/content-templates) that provide the basic structure for each content type.

 While the Diátaxis framework provides a starting point, successful documentation requires contextual adaptation to your product. Start by understanding the framework’s principles, then adjust them to serve your users’ needs.

## ​Related pages

 [Content templatesCopy and modify templates for each content type.](https://mintlify.com/docs/guides/content-templates)[Style and toneWrite effective documentation with consistent style.](https://mintlify.com/docs/guides/style-and-tone)[Understand your audienceResearch and define your documentation audience.](https://mintlify.com/docs/guides/understand-your-audience)[NavigationOrganize your documentation structure effectively.](https://mintlify.com/docs/guides/navigation)[Improve your docsUse data and metrics to improve documentation.](https://mintlify.com/docs/guides/improving-docs)

---

# Cursor

> Configure Cursor to be your writing assistant.

Transform Cursor into a documentation expert that knows your components, style guide, and best practices.

## ​Use Cursor with Mintlify

 Cursor rules provide persistent context about your documentation, ensuring more consistent suggestions that fit your standards and style.

- **Project rules** are stored in your documentation repository and shared with your team.
- **User rules** apply to your personal Cursor environment.

 We recommend creating project rules for your docs so that all contributors have access to the same rules. Create rules files in the `.cursor/rules` directory of your docs repo. See the [Cursor Rules documentation](https://docs.cursor.com/context/rules) for complete setup instructions.

## ​Example project rule

 This rule provides Cursor with context to properly format Mintlify components and follow technical writing best practices. You can use this example as-is or customize it for your documentation:

- **Writing standards**: Update language guidelines to match your style guide.
- **Component patterns**: Add project-specific components or modify existing examples.
- **Code examples**: Replace generic examples with real API calls and responses for your product.
- **Style and tone preferences**: Adjust terminology, formatting, and other rules.

 Add this rule with any modifications as an `.mdc` file in the `.cursor/rules` directory of your docs repo.

```
# Mintlify technical writing rule

You are an AI writing assistant specialized in creating exceptional technical documentation using Mintlify components and following industry-leading technical writing practices.

## Core writing principles

### Language and style requirements

- Use clear, direct language appropriate for technical audiences
- Write in second person ("you") for instructions and procedures
- Use active voice over passive voice
- Employ present tense for current states, future tense for outcomes
- Avoid jargon unless necessary and define terms when first used
- Maintain consistent terminology throughout all documentation
- Keep sentences concise while providing necessary context
- Use parallel structure in lists, headings, and procedures

### Content organization standards

- Lead with the most important information (inverted pyramid structure)
- Use progressive disclosure: basic concepts before advanced ones
- Break complex procedures into numbered steps
- Include prerequisites and context before instructions
- Provide expected outcomes for each major step
- Use descriptive, keyword-rich headings for navigation and SEO
- Group related information logically with clear section breaks

### User-centered approach

- Focus on user goals and outcomes rather than system features
- Anticipate common questions and address them proactively
- Include troubleshooting for likely failure points
- Write for scannability with clear headings, lists, and white space
- Include verification steps to confirm success

## Mintlify component reference

### docs.json

- Refer to the [docs.json schema](https://mintlify.com/docs.json) when building the docs.json file and site navigation

### Callout components

#### Note - Additional helpful information

<Note>
Supplementary information that supports the main content without interrupting flow
</Note>

#### Tip - Best practices and pro tips

<Tip>
Expert advice, shortcuts, or best practices that enhance user success
</Tip>

#### Warning - Important cautions

<Warning>
Critical information about potential issues, breaking changes, or destructive actions
</Warning>

#### Info - Neutral contextual information

<Info>
Background information, context, or neutral announcements
</Info>

#### Check - Success confirmations

<Check>
Positive confirmations, successful completions, or achievement indicators
</Check>

### Code components

#### Single code block

Example of a single code block:

```javascript config.js
const apiConfig = {
  baseURL: 'https://api.example.com',
  timeout: 5000,
  headers: {
    'Authorization': `Bearer ${process.env.API_TOKEN}`
  }
};
```

#### Code group with multiple languages

Example of a code group:

<CodeGroup>
```javascript Node.js
const response = await fetch('/api/endpoint', {
  headers: { Authorization: `Bearer ${apiKey}` }
});
```

```python Python
import requests
response = requests.get('/api/endpoint',
  headers={'Authorization': f'Bearer {api_key}'})
```

```curl cURL
curl -X GET '/api/endpoint' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```
</CodeGroup>

#### Request/response examples

Example of request/response documentation:

<RequestExample>
```bash cURL
curl -X POST 'https://api.example.com/users' \
  -H 'Content-Type: application/json' \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```
</RequestExample>

<ResponseExample>
```json Success
{
  "id": "user_123",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```
</ResponseExample>

### Structural components

#### Steps for procedures

Example of step-by-step instructions:

<Steps>
<Step title="Install dependencies">
  Run `npm install` to install required packages.

  <Check>
  Verify installation by running `npm list`.
  </Check>
</Step>

<Step title="Configure environment">
  Create a `.env` file with your API credentials.

  ```bash
  API_KEY=your_api_key_here
  ```

  <Warning>
  Never commit API keys to version control.
  </Warning>
</Step>
</Steps>

#### Tabs for alternative content

Example of tabbed content:

<Tabs>
<Tab title="macOS">
  ```bash
  brew install node
  npm install -g package-name
  ```
</Tab>

<Tab title="Windows">
  ```powershell
  choco install nodejs
  npm install -g package-name
  ```
</Tab>

<Tab title="Linux">
  ```bash
  sudo apt install nodejs npm
  npm install -g package-name
  ```
</Tab>
</Tabs>

#### Accordions for collapsible content

Example of accordion groups:

<AccordionGroup>
<Accordion title="Troubleshooting connection issues">
  - **Firewall blocking**: Ensure ports 80 and 443 are open
  - **Proxy configuration**: Set HTTP_PROXY environment variable
  - **DNS resolution**: Try using 8.8.8.8 as DNS server
</Accordion>

<Accordion title="Advanced configuration">
  ```javascript
  const config = {
    performance: { cache: true, timeout: 30000 },
    security: { encryption: 'AES-256' }
  };
  ```
</Accordion>
</AccordionGroup>

### Cards and columns for emphasizing information

Example of cards and card groups:

<Card title="Getting started guide" icon="rocket" href="/quickstart">
Complete walkthrough from installation to your first API call in under 10 minutes.
</Card>

<CardGroup cols={2}>
<Card title="Authentication" icon="key" href="/auth">
  Learn how to authenticate requests using API keys or JWT tokens.
</Card>

<Card title="Rate limiting" icon="clock" href="/rate-limits">
  Understand rate limits and best practices for high-volume usage.
</Card>
</CardGroup>

### API documentation components

#### Parameter fields

Example of parameter documentation:

<ParamField path="user_id" type="string" required>
Unique identifier for the user. Must be a valid UUID v4 format.
</ParamField>

<ParamField body="email" type="string" required>
User's email address. Must be valid and unique within the system.
</ParamField>

<ParamField query="limit" type="integer" default="10">
Maximum number of results to return. Range: 1-100.
</ParamField>

<ParamField header="Authorization" type="string" required>
Bearer token for API authentication. Format: `Bearer YOUR_API_KEY`
</ParamField>

#### Response fields

Example of response field documentation:

<ResponseField name="user_id" type="string" required>
Unique identifier assigned to the newly created user.
</ResponseField>

<ResponseField name="created_at" type="timestamp">
ISO 8601 formatted timestamp of when the user was created.
</ResponseField>

<ResponseField name="permissions" type="array">
List of permission strings assigned to this user.
</ResponseField>

#### Expandable nested fields

Example of nested field documentation:

<ResponseField name="user" type="object">
Complete user object with all associated data.

<Expandable title="User properties">
  <ResponseField name="profile" type="object">
  User profile information including personal details.

  <Expandable title="Profile details">
    <ResponseField name="first_name" type="string">
    User's first name as entered during registration.
    </ResponseField>

    <ResponseField name="avatar_url" type="string | null">
    URL to user's profile picture. Returns null if no avatar is set.
    </ResponseField>
  </Expandable>
  </ResponseField>
</Expandable>
</ResponseField>

### Media and advanced components

#### Frames for images

Wrap all images in frames:

<Frame>
<img src="/images/dashboard.png" alt="Main dashboard showing analytics overview" />
</Frame>

<Frame caption="The analytics dashboard provides real-time insights">
<img src="/images/analytics.png" alt="Analytics dashboard with charts" />
</Frame>

#### Videos

Use the HTML video element for self-hosted video content:

<video
  controls
  className="w-full aspect-video rounded-xl"
  src="link-to-your-video.com"
></video>

Embed YouTube videos using iframe elements:

<iframe
  className="w-full aspect-video rounded-xl"
  src="https://www.youtube.com/embed/4KzFe50RQkQ"
  title="YouTube video player"
  frameBorder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
></iframe>

#### Tooltips

Example of tooltip usage:

<Tooltip tip="Application Programming Interface - protocols for building software">
API
</Tooltip>

#### Updates

Use updates for changelogs:

<Update label="Version 2.1.0" description="Released March 15, 2024">
## New features
- Added bulk user import functionality
- Improved error messages with actionable suggestions

## Bug fixes
- Fixed pagination issue with large datasets
- Resolved authentication timeout problems
</Update>

## Required page structure

Every documentation page must begin with YAML frontmatter:

```yaml
---
title: "Clear, specific, keyword-rich title"
description: "Concise description explaining page purpose and value"
---
```

## Content quality standards

### Code examples requirements

- Always include complete, runnable examples that users can copy and execute
- Show proper error handling and edge case management
- Use realistic data instead of placeholder values
- Include expected outputs and results for verification
- Test all code examples thoroughly before publishing
- Specify language and include filename when relevant
- Add explanatory comments for complex logic
- Never include real API keys or secrets in code examples

### API documentation requirements

- Document all parameters including optional ones with clear descriptions
- Show both success and error response examples with realistic data
- Include rate limiting information with specific limits
- Provide authentication examples showing proper format
- Explain all HTTP status codes and error handling
- Cover complete request/response cycles

### Accessibility requirements

- Include descriptive alt text for all images and diagrams
- Use specific, actionable link text instead of "click here"
- Ensure proper heading hierarchy starting with H2
- Provide keyboard navigation considerations
- Use sufficient color contrast in examples and visuals
- Structure content for easy scanning with headers and lists

## Component selection logic

- Use **Steps** for procedures and sequential instructions
- Use **Tabs** for platform-specific content or alternative approaches
- Use **CodeGroup** when showing the same concept in multiple programming languages
- Use **Accordions** for progressive disclosure of information
- Use **RequestExample/ResponseExample** specifically for API endpoint documentation
- Use **ParamField** for API parameters, **ResponseField** for API responses
- Use **Expandable** for nested object properties or hierarchical information
```

## ​Enhance with MCP server

 Connect the Mintlify MCP server to Cursor to give it access to search the Mintlify documentation while helping you write. When you connect the MCP server, Cursor searches the up to date Mintlify documentation for context so you don’t have to leave your IDE to reference documentation. See [Model Context Protocol](https://mintlify.com/docs/ai/model-context-protocol#example%3A-connect-to-the-mintlify-mcp-server) for complete setup instructions.

---

# Create developer documentation

> Build documentation that helps developers integrate with your APIs, SDKs, and tools.

Developer documentation helps people understand and integrate with your product. Good documentation helps people do more with your product, reduces support burden, speeds up adoption, and improves developer experience. Mintlify provides infrastructure built for developer documentation.

- **API reference generation**: Generate interactive [API references](https://mintlify.com/docs/api-playground/overview) from OpenAPI specifications that let developers test endpoints in your documentation.
- **Code blocks with explanations**: The [assistant](https://mintlify.com/docs/ai/assistant) explains code examples in context, helping developers understand implementation details.
- **Git sync**: Keep documentation in sync with your codebase using [GitHub](https://mintlify.com/docs/deploy/github) or [GitLab](https://mintlify.com/docs/deploy/gitlab).
- **Versioning**: Maintain documentation for multiple [versions](https://mintlify.com/docs/organize/navigation#versions) so developers on older versions can still find accurate information.

## ​Prerequisites

 If you haven’t created a Mintlify project yet, see the [Quickstart](https://mintlify.com/docs/quickstart) to deploy your site.

- Your API specification in OpenAPI format (if documenting an API)
- A Git repository for your documentation
- Admin access to your Mintlify organization

## ​Migrate existing documentation

 If you’re creating documentation from scratch, skip to [Plan your documentation structure](#plan-your-documentation-structure).

### ​Audit existing content

 Review your current documentation to understand what you have and what you need to migrate.

- **API reference**: Is it generated from a spec or hand-written? What endpoints do you document?
- **Guides and tutorials**: What integration guides exist? Are they current?
- **Code examples**: What languages and frameworks do you use?
- **SDK documentation**: Do you have separate documentation for each SDK?
- **Changelog**: Do you maintain a changelog or release notes?
- **Metadata**: Do you have metadata for your content like dates, authors, and tags?

### ​Export your existing content

- Export to **Markdown** for the simplest migration to Mintlify.
- Export **OpenAPI specs** for API reference content.
- Export to **HTML** if Markdown isn’t available, then convert to Markdown.

## ​Plan your documentation structure

 Developer documentation typically includes several content types. Structure your navigation around how your users understand your product. docs.json example

```
{
  "navigation": {
    "groups": [
      {
        "group": "Get Started",
        "pages": [
          "introduction",
          "quickstart",
          "authentication"
        ]
      },
      {
        "group": "Guides",
        "pages": [
          "guides/webhooks",
          "guides/error-handling",
          "guides/rate-limits",
          "guides/pagination"
        ]
      },
      {
        "group": "API Reference",
        "pages": [
          "api-reference/overview",
          "api-reference/users",
          "api-reference/orders",
          "api-reference/products"
        ]
      },
      {
        "group": "SDKs",
        "pages": [
          "sdks/javascript",
          "sdks/python",
          "sdks/go"
        ]
      }
    ]
  }
}
```

 See [Navigation](https://mintlify.com/docs/organize/navigation) for more configuration options.

## ​Set up your API reference

 If you have an API, generate an interactive reference from your OpenAPI specification. 1

Add your OpenAPI spec

Add your OpenAPI specification file to your project. You can use YAML or JSON format.

```
your-project/
├── docs.json
├── openapi.yaml
└── api-reference/
    └── overview.mdx
```

2

Configure the spec in docs.json

Reference your OpenAPI file in your `docs.json` configuration.Configuration example

```
{
  "openapi": "openapi.yaml"
}
```

3

Add endpoints to navigation

Add the endpoints to your `docs.json` navigation. See [OpenAPI setup](https://mintlify.com/docs/api-playground/openapi-setup) for configuration options.Navigation example

```
{
  "group": "API Reference",
  "pages": [
    "api-reference/overview",
    "api-reference/users/list-users",
    "api-reference/users/get-user",
    "api-reference/users/create-user"
  ]
}
```

## ​Set up the assistant

 The assistant helps developers find answers and understand code examples. Configure it from your [dashboard](https://dashboard.mintlify.com/products/assistant/settings).

- **Sample questions**: Add developer-focused questions like “How do I authenticate API requests?” or “Show me how to handle webhooks.”
- **Code explanations**: The assistant can explain code blocks in context when developers ask questions about specific examples.

## ​Set up versioning

 If you maintain multiple API versions, configure versioning so developers find documentation for their version. Versioning example

```
{
  "versions": ["v2", "v1"],
  "navigation": {
    "groups": [
      {
        "group": "API Reference",
        "version": "v2",
        "pages": ["v2/api-reference/users"]
      },
      {
        "group": "API Reference",
        "version": "v1",
        "pages": ["v1/api-reference/users"]
      }
    ]
  }
}
```

 See [Versions](https://mintlify.com/docs/organize/navigation#versions) for more information.

## ​Connect to your repository

 Install the Mintlify [GitHub App](https://mintlify.com/docs/deploy/github) to keep documentation in sync with your codebase and enable contributions. 1

Connect your repository

Link your GitHub repository in the [dashboard](https://dashboard.mintlify.com). This enables automatic deployments when you push changes.2

Configure branch settings

Set your production branch and enable preview deployments for pull requests. This lets you review documentation changes before they go live. If you use GitLab, see [GitLab](https://mintlify.com/docs/deploy/gitlab) for configuration instructions.

## ​Maintain your documentation

 Developer documentation needs regular updates so that information is accurate and usable. 1

Keep the API reference current

Update your OpenAPI specification whenever you release changes. If your specification is generated from code, automate this in your release process.2

Update code examples

Review code examples when you release new SDK versions or product updates. Outdated examples cause integration failures and support requests.3

Maintain a changelog

Document breaking changes, new features, and deprecations. Developers rely on changelogs to understand what changed between versions. See [Changelogs](https://mintlify.com/docs/create/changelogs) for more information.4

Monitor feedback

Review assistant conversations and search analytics to identify gaps in your documentation. If developers repeatedly ask about the same topic, improve that section. See [Maintenance](https://mintlify.com/docs/guides/maintenance) for more information.

## ​Next steps

 Your developer documentation is ready to launch. After deploying:

1. Announce the documentation to your developer community.
2. Monitor search patterns and assistant conversations for gaps.
3. Set up a process to update docs with each API release.
4. Gather feedback from developers to improve content over time.

---

# GEO guide: Optimize docs for AI search and answer engines

> Optimize your documentation for AI search and answer engines.

Optimize your documentation for both traditional search engines and AI-powered answer engines like ChatGPT, Perplexity, and Google AI Overviews. Generative Engine Optimization (GEO) focuses on being cited by AI systems through comprehensive content and structured information, while traditional SEO targets search result rankings.

## ​GEO quickstart

### ​Initial setup

1. **Make sure your docs are being indexed** in your `docs.json` settings
2. **Audit current pages** for missing descriptions and titles

### ​Content improvements

1. **Add comparison tables** to appropriate pages
2. **Audit headings** to ensure they answer common questions
3. **Improve internal linking** between related topics
4. **Test with AI tools** to verify accuracy

## ​GEO best practices

 In general, well written and well structured documentation will have strong GEO. You should still prioritize writing for your users, and if your content is meeting their needs, you will be well on your way to optimizing for AI tools. Creating genuinely helpful content rather than optimizing for optimization’s sake is rewarded by both traditional and AI search engines. Focus on:

- Content aligned to user needs rather than keyword matching
- Structured, scannable information
- Direct answers to questions

### ​Format for clarity

 These formatting practices help AI tools parse and understand your content:

- Don’t skip heading levels (H1 → H2 → H3)
- Use specific object names instead of “it” or “this”
- Label code blocks with their programming language
- Give images descriptive alt text
- Link to related concepts to help AI understand relationships

### ​Answer questions directly

 Write content that addresses specific user questions:

- Begin sections with the main takeaway
- Use descriptive headings that match common queries
- Break complex topics into numbered steps

## ​Mintlify configuration

 Use these features to improve GEO.

### ​Add descriptive page metadata

 Include clear titles and descriptions in your frontmatter:

```
---
title: "API authentication guide"
description: "Complete guide to implementing API authentication with code examples"
---
```

### ​Configure global indexing settings

 Add to your `docs.json`:

```
{
  "seo": {
    "indexing": "all",
    "metatags": {
      "og:type": "website",
      "og:site_name": "Your docs"
    }
  }
}
```

### ​LLMs.txt

 LLMs.txt files help AI systems understand your documentation structure, similar to how sitemaps help search engines. Mintlify automatically generates LLMs.txt files for your docs. No configuration is required.

## ​Testing your documentation

 Test various AI tools with questions about your product and documentation to see how well your docs are being cited. **Ask AI assistants specific questions about your docs:**

- “How do I set up authentication using this API?”
- “Walk me through the installation process step by step”

 **Check that tools provide:**

- Correct code samples
- Accurate step-by-step instructions

---

# Git concepts for documentation

> Learn version control and collaboration fundamentals for docs-as-code workflows.

Git is a version control system that tracks changes to your documentation and enables team collaboration. With Git, you can see what changed over time in files, who made the changes, when they made changes, and why. Git also makes it easy to revert to previous versions of files if you need to undo changes. The web editor performs Git operations behind the scenes. With an understanding of Git, you can work more effectively with the web editor and collaborate with team members who use local development.

## ​Why Git for documentation?

 Git provides essential capabilities for managing documentation.

- **Version history**: See what changed, when, and why for every file.
- **Collaboration**: Multiple people can work on different parts simultaneously.
- **Safety**: Experiment without breaking live documentation.
- **Review workflows**: Team members can review changes before publishing.
- **Recovery**: Undo mistakes or restore previous versions.

## ​New to Git?

 If you’re completely new to Git and version control, here’s a path to get started. 1

Use the web editor first.

The [web editor](https://mintlify.com/docs/editor/index) handles Git operations automatically.

- See any changes visually as you make them.
- Create branches with one click.
- Publish and create pull requests without using Git commands.

This lets you learn Git concepts without using the command line.2

Learn by doing.

As you use the web editor, you’re using Git.

- **Save changes** creates a commit.
- **Create branch** creates a Git branch.
- **Publish** opens a pull request for review.

3

Explore local development when it is useful.

You can manage your documentation entirely with the web editor and dashboard, but you can customize your workflow by working in your local environment.

- Create and edit files in your favorite editor.
- Use command line Git, GitHub desktop, or an extension in your editor.
- Preview changes locally before publishing.
- Integrate with other tools like support tickets, issue tracking, and design systems.

## ​Core Git concepts

Branch

A branch points to a specific commit in your repository. Your live documentation builds from a deployment branch. You can have any number of other branches with changes that are not yet published to your live documentation. If you want to incorporate the changes from a branch into your live documentation, you can merge the branch into your deployment branch through a pull request.Use branches to work on changes without affecting your live documentation, safely experiment with new features, and get reviews before publishing.

Clone

Download a complete copy of a repository to your computer, including all files and full history. When you clone, you get everything needed to work locally.

```
git clone https://github.com/your-org/your-repo
```

Commit

A saved snapshot of your changes at a specific point in time. Each commit includes a message describing what changed and creates a permanent record in your project history.

Conflict

Occurs when two people change the same part of a file differently. Git asks you to manually choose which change to keep or combine both changes.

Deployment branch

The primary branch of your project. Changes to this branch automatically publish to your documentation site. Often called `main`, but you can set any branch as your deployment branch.

Diff

A diff (or difference) shows the changes between two versions of a file. When reviewing pull requests, diffs highlight what is different from the original version of the file.

Merge

Combine changes from one branch into another. Usually done via pull request after review to incorporate feature work into your deployment branch.

Pull

Get the latest changes from the remote repository to your local copy. Keeps you up to date with other people’s work.

```
git pull
```

Pull request

A way to propose merging your changes on a branch into your live documentation. Allows for review and discussion before changes go live. Commonly called a PR, and also called a merge request in GitLab.

Push

Send your local commits to the remote repository. This makes your changes available to others and can trigger automatic deployments.

```
git push
```

Remote

A version of your repository hosted on a server. Your local repository connects to a remote repository to push and pull changes.

Repository

Your documentation’s source code with all the files, and their history, that make up the pages of your documentation site. The web editor connects to your documentation repository to access and modify content.

Stage

Prepare specific changes to include in your next commit. Staging lets you organize changes into logical commits.

```
git add filename.mdx
```

## ​How the web editor uses Git

 The web editor connects to your Git repository through the [GitHub App](https://mintlify.com/docs/deploy/github) or [GitLab integration](https://mintlify.com/docs/deploy/gitlab) and automates common Git operations. When you:

- **Open a file**: The editor fetches the latest version from your repository, ensuring you’re always working with up to date content.
- **Make changes**: The editor tracks your changes as a draft that can become a commit when you’re ready to save your work.
- **Save changes**: The editor makes a commit with your changes, preserving your work in the project history.
- **Create a branch**: The editor creates a new branch in your repository that anyone with access to the repository can use to collaborate and review changes.
- **Publish on your deployment branch**: The editor commits and pushes directly to your deployment branch, which publishes your changes immediately.
- **Publish on other branches**: The editor creates a pull request, which allows you to get feedback from others before merging your changes into your deployment branch.

## ​Common workflows

### ​Publish directly to your deployment branch

- Using web editor
- Using local development

1. Open file in the [web editor](https://dashboard.mintlify.com/editor).
2. Make changes.
3. Click **Publish**.
4. Changes appear in the repository and deploy automatically.

1. Pull the latest changes: `git pull`
2. Edit file in your editor.
3. Stage changes: `git add filename.mdx`
4. Commit: `git commit -m "Update documentation"`
5. Push: `git push`
6. Changes deploy automatically.

### ​Work on a feature branch

- Using web editor
- Using local development

To create pull requests from the web editor, you must have a branch protection rule enabled that requires pull requests before changes can merge into your deployment branch. Without branch protection rules, changes on branches merge to your deployment branch when published.

1. Create branch from the branch dropdown in the editor toolbar.
2. Make and save changes on the branch.
3. Click **Publish** to create a pull request.
4. Merge the pull request when ready.

1. Create a branch: `git checkout -b feature-name`
2. Make and commit changes.
3. Push branch: `git push -u origin feature-name`
4. Create a pull request.
5. Merge the pull request when ready.

### ​Review changes before publishing

 1

Create a feature branch.

Work on changes in a branch separate from your deployment branch so that you can share and review the changes before publishing.2

Make your changes.

Edit files and commit changes to the feature branch.3

Create a pull request.

Create a pull request to propose merging the changes on your feature branch into the deployment branch.4

Review the diff.

Check your changes. The pull request shows line-by-line differences from the original version of the file.5

Get team feedback.

Team members can comment on specific lines or overall changes. Make any changes and commit them to the feature branch.6

Merge when approved.

Merge the pull request to publish changes to your live documentation.

## ​Git best practices

 Every team develops their own workflows and preferences, but these are some general best practices to get started.

- **Write descriptive commit messages**: Be specific about what changed using active language. `Fix broken link in API docs` is more informative than `update page`.
- **Use descriptive branch names**: Branch names should explain the purpose the branch. Use informative names like `update-api-reference` instead of generic names like `temp` or `my-branch`.
- **Keep branches focused**: Keep the changes on a branch focused on a specific task or project. This makes reviews easier and reduces conflicts.
- **Delete branches after merging**: Delete branches when you no longer need them to keep your repository tidy.
- **Pull before you push**: Always pull the latest changes before pushing to avoid conflicts. The web editor does this automatically.
- **Review your own changes first**: Check the diff before creating a pull request.

---

# Improve your docs

> Use data and metrics to improve your documentation.

This page explains how to measure the success of your documentation with quantitative metrics, qualitative feedback, and alignment with business goals.

## ​Quantitative metrics

 Some examples to consider:

- **Page views**: Views can be a good proxy for success, but could be driven by bot traffic or repeat visitors. If you’re getting many views on an errors or explainer page, it might signal an issue with your broader product.
- **Time on page**: Longer time on page might signal engagement, but could also mean users are stuck trying to find the information they need.
- **Bounce rate**: A high bounce rate could mean users didn’t find what they needed, or it could mean they found exactly what they needed and left satisfied.

 The key is to compare these metrics over time or against a baseline to spot trends and understand if they align with users achieving their goals.

### ​Correlate traffic and satisfaction

 Use analytics to identify patterns:

- **High traffic and low feedback scores**: Popular pages with a poor user experience. Prioritize improving these pages.
- **Low traffic and high feedback scores**: Documentation that is working well, but might not be discoverable. Consider promoting these pages.
- **High traffic and high feedback scores**: Your documentation’s greatest hits. Review these pages for ideas to improve the rest of your content.

## ​Qualitative feedback

 Add context to your quantitative metrics with qualitative information:

- **User feedback**: Use [feedback](https://mintlify.com/docs/optimize/feedback) to capture user sentiment through ratings and open-ended comments, helping you understand what works and where users struggle.
- **Stakeholder input**: Get regular feedback from teams like support, engineering, and customer success to uncover common issues users face and areas for improvement.
- **User testing**: Conduct usability tests to validate whether users can find the answers they need and whether your documentation aligns with their expectations. See [Understand your audience](https://mintlify.com/docs/guides/understand-your-audience) for more on user research.

## ​Business alignment

 Measure documentation against broader business objectives:

- **Support efficiency**: Track whether your documentation reduces the volume of support tickets or improves satisfaction scores, indicating it’s meeting user needs.
- **Onboarding and adoption**: Monitor how well documentation supports new users in getting up to speed, contributing to faster product adoption.
- **Retention**: Well-maintained, easy-to-follow docs contribute to positive user experiences, helping to reduce churn and improve retention rates.

## ​Put analytics into action

 Use these patterns to prioritize your documentation improvements:

- **Fix high-impact problems first**: Popular pages with poor feedback scores affect the most users.
- **Respond to user feedback**: Contextual and code snippet feedback can identify specific areas for improvement.
- **Focus on key user journeys**: Prioritize pages connected to the most important tasks for your product.

## ​Related pages

 [Analytics overviewView analytics and track documentation performance.](https://mintlify.com/docs/optimize/analytics)[FeedbackCollect and analyze user feedback on your docs.](https://mintlify.com/docs/optimize/feedback)[Understand your audienceResearch and define your documentation audience.](https://mintlify.com/docs/guides/understand-your-audience)[SEOOptimize your documentation for search engines.](https://mintlify.com/docs/optimize/seo)
