# Internationalization and more

# Internationalization

> Set up multi-language documentation to reach global audiences.

Internationalization (i18n) is the process of designing software or content to work for different languages and locales. This guide explains how to structure files, configure navigation, and maintain translations effectively so that you can help users access your documentation in their preferred language and improve global reach.

## ​File structure

 Organize translated content in language-specific directories to keep your documentation maintainable and structure your navigation by language. Create a separate directory for each language using [ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). Place translated files in these directories with the same structure as your default language.

Show supported language codes

- `ar` - Arabic
- `cs` - Czech
- `cn` or `zh-Hans` - Chinese (Simplified)
- `zh-Hant` - Chinese (Traditional)
- `de` - German
- `en` - English
- `es` - Spanish
- `fr` - French
- `he` - Hebrew
- `hi` - Hindi
- `id` - Indonesian
- `it` - Italian
- `jp` - Japanese
- `ko` - Korean
- `lv` - Latvian
- `nl` - Dutch
- `no` - Norwegian
- `pl` - Polish
- `pt` or `pt-BR` - Portuguese
- `ro` - Romanian
- `ru` - Russian
- `sv` - Swedish
- `tr` - Turkish
- `ua` - Ukrainian
- `uz` - Uzbek
- `vi` - Vietnamese

 Example file structure

```
docs/
├── index.mdx                    # English (default)
├── quickstart.mdx
├── fr/
│   ├── index.mdx               # French
│   ├── quickstart.mdx
├── es/
│   ├── index.mdx               # Spanish
│   ├── quickstart.mdx
└── zh/
    ├── index.mdx               # Chinese
    └── quickstart.mdx
```

 Keep the same file names and directory structure across all languages. This makes it easier to maintain translations and identify missing content.

## ​Configure the language switcher

 To add a language switcher to your documentation, configure the `languages` array in your `docs.json` navigation. docs.json

```
{
  "navigation": {
    "languages": [
      {
        "language": "en",
        "groups": [
          {
            "group": "Getting started",
            "pages": ["index", "quickstart"]
          }
        ]
      },
      {
        "language": "es",
        "groups": [
          {
            "group": "Comenzando",
            "pages": ["es/index", "es/quickstart"]
          }
        ]
      }
    ]
  }
}
```

 Each language entry in the `languages` array requires:

- `language`: ISO 639-1 language code
- Full navigation structure
- Paths to translated files

 The navigation structure can differ between languages to accommodate language-specific content needs. Translate navigation labels like group or tab names to match the language of the content. This creates a fully localized experience for your users.

### ​Global navigation

 To add global navigation elements that appear across all languages, configure the `global` object in your `docs.json` navigation. docs.json

```
{
  "navigation": {
    "global": {
      "anchors": [
        {
          "anchor": "Documentation",
          "href": "https://example.com/docs"
        },
        {
          "anchor": "Blog",
          "href": "https://example.com/blog"
        }
      ]
    },
    "languages": [
      // Language-specific navigation
    ]
  }
}
```

## ​Maintain translations

 Keep translations accurate and synchronized with your source content.

### ​Translation workflow

1. Update source content in your primary language.
2. Identify changed content.
3. Translate changed content.
4. Review translations for accuracy.
5. Update translated files.
6. Verify navigation and links work.

### ​Automated translations

 For automated translation solutions, [contact the Mintlify sales team](mailto:gtm@mintlify.com).

### ​Images and media

 Store translated images in language-specific directories.

```
images/
├── dashboard.png          # English version
├── fr/
│   └── dashboard.png     # French version
└── es/
    └── dashboard.png     # Spanish version
```

 Reference images using relative paths in your translated content. es/index.mdx

```
![Captura de pantalla del panel de control](/images/es/dashboard.png)
```

## ​SEO for multi-language sites

 Optimize each language version for search engines.

### ​Page metadata

 Include translated metadata in each file’s frontmatter: fr/index.mdx

```
---
title: "Commencer"
description: "Apprenez à commencer avec notre produit."
keywords: ["démarrage", "tutoriel", "guide"]
---
```

## ​Best practices

### ​Date and number formats

 Consider locale-specific formatting for dates and numbers.

- Date formats: MM/DD/YYYY vs DD/MM/YYYY
- Number formats: 1,000.00 vs 1.000,00
- Currency symbols: $100.00 vs 100,00€

 Include examples in the appropriate format for each language or use universally understood formats.

### ​Maintain consistency

- Maintain content parity across all languages to ensure every user gets the same quality of information.
- Create a translation glossary for technical terms.
- Keep the same content structure across languages.
- Match the tone and style of your source content.
- Use Git branches to manage translation work separately from main content updates.

### ​Layout differences

 Some languages require more or less space than English. Test your translated content on different screen sizes to ensure:

- Navigation fits properly.
- Code blocks don’t overflow.
- Tables and other formatted text remain readable.
- Images scale appropriately.

### ​Character encoding

 Ensure your development environment and deployment pipeline support UTF-8 encoding to properly display all characters in languages with different alphabets and special characters.

---

# Create a knowledge base

> Host your internal knowledge base on Mintlify to consolidate information for your team, improve search, and reduce maintenance burden.

Host your internal knowledge base on Mintlify to consolidate information for your team, improve search, and reduce maintenance burden.

---

# Linking

> Learn how to create internal links, reference API endpoints, and maintain link integrity across your documentation.

Learn how to create internal links, reference API endpoints, and maintain link integrity across your documentation.

---

# Maintenance

> Keep your documentation accurate and up-to-date over time.

This page explains strategies for keeping your documentation accurate and valuable over time, from automated checks to content lifecycles.

## ​Automate what you can

 Introduce automations where you can, such as:

- **Track stale content:** Run a script to flag important docs that haven’t been updated in the last three months. Are they still accurate?
- **Automate documentation updates:** Build a workflow to automatically update documentation when code is merged with the [agent API](https://mintlify.com/docs/guides/automate-agent).
- **Enforce standards with linters:** Use [Vale](http://Vale.sh) or [CI checks](https://mintlify.com/docs/deploy/ci) to automatically catch formatting issues, writing style deviations, or missing metadata on every pull request.

## ​Set up a review process

 Documentation might never be perfect, and that’s okay. You should have a threshold of acceptance where documentation is functional and useful. Balance efficiency with quality:

- **Focus on high-impact docs.** Not every page needs regular updates. Make sure the most important pages are reviewed regularly for accuracy and relevance.
- **Leverage your community.** If your docs are open-source, empower users to flag issues or submit fixes via pull requests. This builds trust and keeps content fresh.

## ​Know when to rewrite

 Over time, documentation naturally accumulates caveats and workarounds. When incremental fixes create more confusion than clarity, a full overhaul might be the best option.

- **Plan for periodic resets.** A major cleanup, especially if best practices or the product itself has evolved significantly, saves time for your team and your users.
- **Start with a structured audit.** Interview support teams, analyze user feedback, and document what is missing, misleading, or redundant before rewriting.
- **Complete rewrites in focused sprints.** A full overhaul doesn’t have to happen all at once. Prioritize sections with the biggest impact.

## ​Wrong docs can be worse than no docs

 Outdated or misleading documentation wastes users’ time and erodes trust. In cases where a page is completely inaccurate and unfixable in the short term, it’s often better to remove it entirely. Users will appreciate having less information over having wrong information.

---

# Media

> Use media effectively while managing maintenance burden.

This page explains best practices for using screenshots, GIFs, and videos in your documentation. Screenshots, GIFs, and videos can enhance documentation but require ongoing maintenance as UI elements change. Use them selectively to avoid unnecessary upkeep. Key guidelines:

- **Media should be supplementary.** If a workflow is clear in text alone, avoid adding visuals.
- **Ensure accessibility.** Add alt text for images, subtitles for videos, and transcripts for audio content. Many people use assistive technology and accessible content benefits all users.
- **Balance clarity with maintainability.** Frequent UI changes can make screenshots and videos outdated quickly. Consider whether the effort to update them is worth the value they add.

## ​When to use media

- **Screenshots** for tasks that are difficult to explain with words.
- **GIFs** for promotional purposes and short yet complex workflows.
- **Videos** for abstract concepts and long workflows.

 Use media sparingly and intentionally to avoid unnecessary documentation debt. When done right, it enhances comprehension without adding maintenance burdens or accessibility barriers.

---

# Migrating MDX API pages to OpenAPI navigation

> Migrate to automated OpenAPI generation with flexible navigation.

If you are currently using individual MDX pages for your API endpoints, you can migrate to autogenerating pages from your OpenAPI specification while retaining the customizability of individual pages. This can help you reduce the number of files you need to maintain and improve the consistency of your API documentation. You can define metadata and content for each endpoint in your OpenAPI specification and organize endpoints where you want them in your navigation.

## ​CLI migration

 The `mint migrate-mdx` command is the recommended way to migrate from MDX endpoint pages to autogenerated pages. This command:

- Parses your `docs.json` navigation structure.
- Identifies MDX pages that generate OpenAPI endpoint pages.
- Extracts content from MDX files and moves it to the `x-mint` extension in your OpenAPI specification.
- Updates your `docs.json` to reference the OpenAPI endpoints directly instead of MDX files.
- Deletes the original MDX endpoint files.

 If you already have `x-mint` defined for an endpoint and also have an MDX page with content for that endpoint, the MDX content will overwrite existing `x-mint` settings.If you have multiple MDX pages for the same endpoint with different content, the script will use the content from the page that appears last in your `docs.json`.The migration tool does not support previewing changes before applying them. 1

Prepare your OpenAPI specification.

Ensure your OpenAPI specification is valid and includes all endpoints you want to document.Any MDX pages you want to migrate must have the `openapi:` frontmatter referencing an endpoint.Validate your OpenAPI file using the [Swagger Editor](https://editor.swagger.io/) or [Mint CLI](https://www.npmjs.com/package/mint).2

Install the Mint CLI

If needed, install or update the [Mint CLI](https://mintlify.com/docs/installation).3

Run the migration command.

```
mint migrate-mdx
```

## ​Manual migration steps

 1

Prepare your OpenAPI specification.

Ensure your OpenAPI specification is valid and includes all endpoints you want to document.For any endpoints that you want to customize the metadata or content, add the `x-mint` extension to the endpoint. See [x-mint extension](https://mintlify.com/docs/api-playground/openapi-setup#x-mint-extension) for more details.For any endpoints that you want to exclude from your documentation, add the `x-hidden` extension to the endpoint.Validate your OpenAPI file using the [Swagger Editor](https://editor.swagger.io/) or [Mint CLI](https://www.npmjs.com/package/mint).2

Update your navigation structure.

Replace MDX page references with OpenAPI endpoints in your `docs.json`.

```
"navigation": {
  "groups": [
    {
      "group": "API Reference",
      "openapi": "/path/to/openapi.json",
      "pages": [
        "overview",
        "authentication",
        "introduction",
        "GET /health",
        "quickstart",
        "POST /users",
        "GET /users/{id}",
        "advanced-features"
      ]
    }
  ]
}
```

3

Remove old MDX files.

After verifying your new navigation works correctly, remove the MDX endpoint files that you no longer need.

## ​Navigation patterns

 You can customize how your API documentation appears in your navigation.

### ​Mixed content navigation

 Combine automatically generated API pages with other pages:

```
"navigation": {
  "groups": [
    {
      "group": "API Reference",
      "openapi": "openapi.json",
      "pages": [
        "api/overview",
        "GET /users",
        "POST /users",
        "api/authentication"
      ]
    }
  ]
}
```

### ​Multiple API versions

 Organize different API versions using tabs or groups:

```
"navigation": {
  "tabs": [
    {
      "tab": "API v1",
      "openapi": "specs/v1.json"
    },
    {
      "tab": "API v2",
      "openapi": "specs/v2.json"
    }
  ]
}
```

## ​When to use individual MDX pages

 Consider keeping individual MDX pages when you need:

- Extensive custom content per endpoint like React components or lengthy examples.
- Unique page layouts.
- Experimental documentation approaches for specific endpoints.

 For most use cases, OpenAPI navigation provides better maintainability and consistency.

---

# Organize navigation

> Design information architecture that aligns with user needs.

This page explains why and how to organize your documentation in a way that makes sense for your users.

## ​Why is navigation important?

 Navigation might seem unimportant because experienced users looking for specific answers typically navigate directly to pages via a search engine or your documentation site’s search bar. But the information architecture of your documentation helps people build a mental model for how to think about your product, and provides structure for people and AI tools that use your documentation. Well designed navigation helps people quickly grasp your product and succeed when using your documentation.

## ​Map the foundation with stakeholders

 Align with key stakeholders like your founders, product managers, or engineering leads on how your product works, what’s most important, and how users should interact with it. Example questions to ask:

- What’s the simplest way to explain how the product works?
- What are the product’s core building blocks?
- How do users typically adopt the product? Where do people most often get stuck?
- How does the product’s architecture influence how people use it?
- What are the most important integrations or dependencies?
- What is changing or evolving in the product?
- If the product was broken into different layers, what would they be? Would it be by tasks that people perform or by features that people use?

## ​Validate your assumptions

 Once you’ve established a structure, you need to validate whether it actually works for real users. The way people navigate your documentation often reveals gaps in your information architecture that internal teams might overlook.

### ​Track real user journeys

 Use tools like session replays (for example, [FullStory](https://www.fullstory.com), [Hotjar](https://www.hotjar.com)) or analytics (for example, [Mixpanel](https://mixpanel.com)) to study how users move through your docs. Pay attention to:

- **Entry points:** Where do users start their journey? Are they coming from search, a support ticket, or directly from your product?
- **Navigation patterns:** Do they follow the expected navigation structure, or do they take unexpected detours?
- **Friction points:** Where do users pause, loop back, or abandon their session? These could indicate unclear organization or missing content.
- **Search behavior:** Are users searching for terms that don’t exist in your documentation? This might highlight gaps in your content or misalignment in terminology.

### ​Test with real users

 Analytics help surface trends, but direct conversations provide deeper insights. Get on research calls where customers attempt to find answers to specific questions. Ask them to narrate their thought process as they navigate. New hires are also a great proxy for users since they don’t have as much prior context as tenured members of your team. Before they get too familiar with your product from the inside, ask them to complete a task using only the documentation. Have them outline in detail how they approached the task. Where they clicked first, how they interpreted section names, and where they got stuck. Their instincts can reveal whether your docs are intuitive or if they assume too much knowledge.

## ​Identify common challenges

 Based on your observations, look for these common navigation problems:

- **Overloaded categories:** Too many top-level sections can overwhelm users. Consider grouping related topics together.
- **Hidden essential content:** Don’t bury critical information. Prioritize frequently accessed content.
- **Unclear section names:** If users hesitate before clicking, your labels might not be intuitive. Align terminology with how your audience naturally thinks.

 Try to design an elegant and functional information architecture, but remember, it’s hard to make documentation that works for absolutely everyone. Consider the majority of your users and what will help them succeed.

## ​Iterate over time

 Above all, stay flexible. Your navigation should evolve with your product and user needs. You don’t have to be right on the first try.

---

# SEO

> Improve SEO to increase documentation discoverability.

This page explains fundamental strategies to optimize your documentation SEO.

## ​Content basics

 Make your writing and structure easy for search engines to scan.

- **Headings and subheadings:** Use sequential, meaningful headers to structure your content. Each page has an H1 created from the `title:` property in the frontmatter.
- **Short paragraphs and bullet points:** Break down large chunks of text into easily readable sections. Use bullet points and numbered lists where appropriate.
- **Internal linking:** Link to related content using descriptive anchor text. For example, “Learn more about rate limiting” instead of “Click here.”

## ​Technical SEO basics

 Once your content is optimized, ensure your documentation performs well from a technical standpoint. These basic technical SEO practices help make your docs more discoverable:

- **Meta tags and descriptions:** Craft SEO-friendly titles (50-60 characters) and descriptions (150-160 characters) for each page. Most [meta tags](https://mintlify.com/docs/optimize/seo) are automatically generated.
- **Alt text for images:** Provide descriptive alt text for images with relevant keywords. For example, “OAuth 2.0 API authentication flow” instead of just “diagram”. This enhances SEO and accessibility.
- **Sitemaps:** Ensure your sitemap is up-to-date. Mintlify automatically generates a sitemap. However, you can manually create a sitemap if you prefer a custom format. Once created, search engines index site maps over time, but you can submit your sitemap directly to Google Search Console to speed up the process.

## ​Page performance

 Use tools like [Google PageSpeed Insights](https://pagespeed.web.dev) to identify areas for technical SEO improvement. Examples of more advanced optimizations:

- **Optimize media for speed:** Compress images using formats like WebP or AVIF and ensure your pages load quickly (ideally under 3 seconds).
- **Structured data (schema markup):** Add schema markup (like HowTo, FAQ) to your pages to help search engines better understand and rank your content.

## ​Keyword research

 To increase organic traffic, invest time into understanding which keywords help users land on your documentation.

- **Keyword research:** Use free tools like [Google Keyword Planner](https://ads.google.com/intl/en_us/home/tools/keyword-planner/) or [Keywords Everywhere](https://keywordseverywhere.com) to identify common phrases or long-tail keywords.
- **Integrate keywords naturally:** Add keywords naturally into headings, subheadings, and throughout the body text. Don’t overstuff keywords. Your documentation should be written for your users, not search engines.

---

# Style and tone

> Write effective technical documentation with consistent style.

This page explains stylistic choices, common mistakes, and implementation tips for writing technical documentation.

## ​Writing principles

- **Be concise.** People are reading documentation to achieve a goal. Get to the point quickly.
- **Clarity over cleverness.** Be simple, direct, and avoid jargon or complex sentence structure.
- **Use active voice.** Instead of saying “A configuration file should be created,” use “Create a configuration file.”
- **Be skimmable.** Use headlines to orient readers. Break up text-heavy paragraphs. Use bullet points and lists to make it easier to scan.
- **Write in second person.** Referring to your reader makes it easier to follow instructions and makes the documentation feel more personal.

## ​Common writing mistakes

- **Spelling and grammar mistakes.** Even a few spelling and grammar mistakes in your documentation make it less credible and harder to read.
- **Inconsistent terminology.** Calling something an “API key” in one paragraph then “API token” in the next makes it difficult for users to follow along.
- **Product-centric terminology.** Your users don’t have the full context of your product. Use language that your users are familiar with.
- **Colloquialisms.** Especially for localization, colloquialisms hurt clarity.

## ​Tips for enforcing style

 Leverage existing style guides to standardize your documentation:

- [Microsoft Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- [Splunk Style Guide](https://docs.splunk.com/Documentation/StyleGuide/current/StyleGuide/Howtouse)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)

 When you know which writing principles you want to implement, automate as much as you can. You can use  [CI checks](https://mintlify.com/docs/deploy/ci) or linters like [Vale](https://vale.sh).

## ​Related pages

 [Content typesChoose the right content type for your documentation goals.](https://mintlify.com/docs/guides/content-types)[AccessibilityMake your documentation accessible to more users.](https://mintlify.com/docs/guides/accessibility)[Format textLearn text formatting and styling options.](https://mintlify.com/docs/create/text)[SEO best practicesImprove documentation discoverability.](https://mintlify.com/docs/guides/seo)

---

# Create a support center

> Build a self-service support center that helps customers find answers, reduces ticket volume, and improves customer satisfaction.

Build a self-service support center that helps customers find answers, reduces ticket volume, and improves customer satisfaction.

---

# Understand your audience

> Keep user goals at the center of your documentation.

This page explains how to identify your audience, conduct user research, and write with their needs in mind.

## ​Identify your primary audience

 Writing for multiple audiences leads to compromises that satisfy no one. Each piece of content should be focused on one specific user persona. Your audience might be:

- Technical decision makers evaluating your product who want to understand higher level details like architecture overviews.
- New users who want to start using your product for the first time.
- Developers responsible for integrating your product who need instructions for a specific task.

 Before writing any page, ask what is your reader trying to accomplish and what is their prior knowledge?

## ​User research is key

 Your team should agree on who your primary audience is, but don’t rely on intuition alone. The best insights come from talking directly to users. There can be a disconnect between how we think about our own products and how people actually use them. Talk to users to understand:

- How do they describe what your product does?
- Do they use any unexpected words or names to describe your product?
- What do they wish they had more knowledge of?
- What is explicitly missing from your documentation?

 Talking to users directly helps ground your writing from their perspective so that you write documentation that is helpful to them and gets them closer to their goals.

## ​Tips and tricks for understanding your audience

1. **Get embedded with support.** You’ll see the pain points that incomplete documentation causes. Ask your support team how people think about the product and what are the most common problems people encounter.
2. **Incorporate feedback mechanisms.** Whether it’s thumbs up/down or plain text fields, give users the opportunity to provide feedback as they read your documentation.
3. **Use analytics to guide you.** Review feedback and insights to understand where users are struggling and where they are successful. Make updates to the documentation that people struggle with or is most connected to the key tasks for your product.

 There will always be edge cases that are not covered by your documentation. Prioritize the most impactful pages to help the most people. Too much content becomes difficult to navigate and maintain, so trying to document every possible scenario can be counterproductive.

---

# Windsurf

> Configure Windsurf to be your writing assistant.

Transform Windsurf into a documentation expert that understands your style guide, components, and project context through workspace rules and memories.

## ​Use Windsurf with Mintlify

 Windsurf’s Cascade AI assistant can be tuned to write documentation according to your standards using Mintlify components. Workspace rules and memories provide persistent context about your project, ensuring more consistent suggestions from Cascade.

- **Workspace rules** are stored in your documentation repository and shared with your team.
- **Memories** provide individual context that builds up over time.

 We recommend setting up workspace rules for shared documentation standards. You can develop memories as you work, but since they are not shared, they will not be consistent across team members. Create workspace rules in the `.windsurf/rules` directory of your docs repo. See [Memories & Rules](https://docs.windsurf.com/windsurf/cascade/memories) in the Windsurf documentation for more information.

## ​Example workspace rule

 This rule provides Cascade with context about Mintlify components and general technical writing best practices. You can use this example rule as-is or customize it for your documentation:

- **Writing standards**: Update language guidelines to match your style guide.
- **Component patterns**: Add project-specific components or modify existing examples.
- **Code examples**: Replace generic examples with real API calls and responses for your product.
- **Style and tone preferences**: Adjust terminology, formatting, and other rules.

 Save your rule as a `.md` file in the `.windsurf/rules` directory of your docs repo.

```
# Mintlify technical writing rule

## Project context

- This is a documentation project on the Mintlify platform
- We use MDX files with YAML frontmatter
- Navigation is configured in `docs.json`
- We follow technical writing best practices

## Writing standards

- Use second person ("you") for instructions
- Write in active voice and present tense
- Start procedures with prerequisites
- Include expected outcomes for major steps
- Use descriptive, keyword-rich headings
- Keep sentences concise but informative

## Required page structure

Every page must start with frontmatter:

```yaml
---
title: "Clear, specific title"
description: "Concise description for SEO and navigation"
---
```

## Mintlify components

### docs.json

- Refer to the [docs.json schema](https://mintlify.com/docs.json) when building the docs.json file and site navigation

### Callouts

- `<Note>` for helpful supplementary information
- `<Warning>` for important cautions and breaking changes
- `<Tip>` for best practices and expert advice
- `<Info>` for neutral contextual information
- `<Check>` for success confirmations

### Code examples

- When appropriate, include complete, runnable examples
- Use `<CodeGroup>` for multiple language examples
- Specify language tags on all code blocks
- Include realistic data, not placeholders
- Use `<RequestExample>` and `<ResponseExample>` for API docs

### Procedures

- Use `<Steps>` component for sequential instructions
- Include verification steps with `<Check>` components when relevant
- Break complex procedures into smaller steps

### Content organization

- Use `<Tabs>` for platform-specific content
- Use `<Accordion>` for progressive disclosure
- Use `<Card>` and `<CardGroup>` for highlighting content
- Wrap images in `<Frame>` components with descriptive alt text

## API documentation requirements

- Document all parameters with `<ParamField>`
- Show response structure with `<ResponseField>`
- Include both success and error examples
- Use `<Expandable>` for nested object properties
- Always include authentication examples

## Quality standards

- Test all code examples before publishing
- Use relative paths for internal links
- Include alt text for all images
- Ensure proper heading hierarchy (start with h2)
- Check existing patterns for consistency
```

## ​Working with Cascade

 Once your rules are set up, you can use Cascade to assist with various documentation tasks. See [Cascade](https://docs.windsurf.com/windsurf/cascade) in the Windsurf documentation for more information.

### ​Example prompts

 **Writing new content**:

```
Create a new page explaining how to authenticate with our API. Include code examples in JavaScript, Python, and cURL.
```

 **Improving existing content**:

```
Review this page and suggest improvements for clarity and component usage. Focus on making the steps easier to follow.
```

 **Creating code examples**:

```
Generate a complete code example showing error handling for this API endpoint. Use realistic data and include expected responses.
```

 **Maintaining consistency**:

```
Check if this new page follows our documentation standards and suggest any needed changes.
```

## ​Enhance with MCP server

 Connect the Mintlify MCP server to Windsurf to give Cascade access to search the Mintlify documentation while helping you write. When you connect the MCP server, Cascade searches the up to date Mintlify documentation for context so you don’t have to leave your IDE to reference documentation. See [Model Context Protocol](https://mintlify.com/docs/ai/model-context-protocol#example%3A-connect-to-the-mintlify-mcp-server) for complete setup instructions.
