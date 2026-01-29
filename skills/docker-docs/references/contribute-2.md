# Guidelines for writing Docker usage guides and more

# Guidelines for writing Docker usage guides

> Learn how to write guides for learning about Docker, with Docker.

# Guidelines for writing Docker usage guides

   Table of contents

---

This guide provides instructions and best practices for writing tutorial-style
usage guides that help users achieve specific goals using Docker. These guides
will be featured in the
[guides section](https://docs.docker.com/guides/) of the website,
alongside our product manuals and reference materials.

Our documentation is written in Markdown, with YAML front matter for metadata.
We use [Hugo](https://gohugo.io) to build the website. For more information
about how to write content for Docker docs, refer to our
[CONTRIBUTING.md](https://github.com/docker/docs/tree/main/CONTRIBUTING.md).

## Purpose of the guides

Our usage guides aim to:

- Educate users on how to leverage Docker in various contexts.
- Provide practical, hands-on experience through step-by-step tutorials.
- Help users achieve specific goals relevant to their interests or projects.

## Audience

- Experience levels: From beginners to advanced users.
- Roles: Developers, system administrators, DevOps engineers, and more.
- Technologies: Various programming languages and frameworks.

## Metadata for guides

Each guide must include a metadata section at the beginning of the document.
This metadata helps users discover and filter guides based on their interests
and needs.

### Example metadata format

```yaml
---
title: Deploy a machine learning model with Docker
linkTitle: Docker for ML deployment
description: Learn how to containerize and deploy a machine learning model using Docker.
summary: |
  This guide walks you through the steps to containerize a machine learning
  model and deploy it using Docker, enabling scalable and portable AI
  solutions.
tags: [machine-learning, deployment]
languages: [python]
params:
  time: 30 minutes
---
```

### Metadata fields

- `title` (required): The main title of the guide in sentence case.
- `linkTitle` (optional): A shorter title used in navigation menus.
- `description` (required): A concise description for SEO purposes.
- `summary` (required): A brief overview of the guide's content.
- `languages` * (optional): List of programming languages used.
- `tags` * (optional): Domains or subject areas covered.
- `params`
  - `time` (optional): Estimated reading or completion time.

* Do apply at least one of the `languages` or `tags` taxonomies. The values
are used to associate the page with the filter options on the guides landing
page.

## Document structure

Our guides emphasize learning by doing. Depending on the type of guide, the
structure may vary to best suit the content and provide a smooth learning
experience.

All guides live directly under the `content/guides/` directory in the Docker
docs repository. Guides can either be a single page or multiple pages. In the
case of multi-page guides, every page is a step in a sequential workflow.

If you're creating a single-page guide, create a single markdown file in the
guides directory:

```bash
# Create the file
touch content/guides/my-docker-guide.md
# or if you have Hugo installed:
hugo new content/guides/my-docker-guide.md
```

To create a multi-page guide, create a directory where each page is a markdown
file, with an `_index.md` file representing the introduction to the guide.

```bash
# Create the index page for the guide
mkdir content/guides/my-docker-guide.md
touch content/guides/my-docker-guide/_index.md
# or if you have Hugo installed:
hugo new content/guides/my-docker-guide/_index.md
```

Then create the pages for the guide under `content/guides/<dir>/<page>.md` as
needed. The [metadata](#metadata-for-guides) lives on the `_index.md` page (you
don't need to assign metadata to individual pages).

### Guides for specific frameworks or languages

For guides that demonstrate how to use Docker with a particular framework or
programming language, consider the following outline:

1. **Introduction**
  - Briefly introduce the framework or language in the context of Docker.
  - Explain what the user will achieve by the end of the guide.
  - List required software, tools, and knowledge.
2. **Development setup**
  - Guide the user through setting up a development environment.
  - Include instructions on writing or obtaining sample code.
  - Show how to run containers for local development.
3. **Building the application**
  - Explain how to create a Dockerfile tailored to the application.
  - Provide step-by-step instructions for building the Docker image.
  - If applicable, show how to test the application using Docker.
4. **Deploying with Docker**
  - Show how to run the application in a Docker container.
  - Discuss configuration options and best practices.
5. **Best practices and conclusions**
  - Offer tips for optimizing Docker usage with the framework or language.
  - Summarize key takeaways, suggest next steps, and further reading.

### Use-case guides

For guides focused on accomplishing a specific goal or use case with Docker
(e.g., deploying a machine learning model), use a flexible outline that ensures
a logical flow.

The following outline is an example. The structure should be adjusted to best
fit the content and ensure a clear, logical progression. Depending on the
subject matter of your use-case guide, the exact structure will vary.

1. **Introduction**
  - Describe the problem or goal.
  - Explain the benefits of using Docker in this context.
2. **Prerequisites**
  - List required tools, technologies, and prior knowledge.
3. **Setup**
  - Provide instructions for setting up the environment.
  - Include any necessary configuration steps.
4. **Implementation**
  - Walk through the process step by step.
  - Use code snippets and explanations to illustrate key points.
5. **Running or deploying the application**
  - Guide the user on how to execute or deploy the solution.
  - Discuss any verification steps to ensure success.
6. **Conclusion**
  - Recap what was achieved.
  - Suggest further reading or advanced topics.

## Example code

If you create an example repository with source code to accompany your guide,
we strongly encourage you to publish that repository under the
[dockersamples](https://github.com/dockersamples) organization on GitHub.
Publishing your source code under this organization, rather than your personal
account, ensures that the source code remains accessible to the maintainers of
the documentation site after publishing. In the event of a bug or an issue in
the guide, the documentation team can more easily update the guide and its
corresponding example repository.

Hosting the examples in the official samples namespace also helps secure trust
with users who are reading the guide.

### Publish a repository underdockersamples

To publish your repository under the `dockersamples` organization, use the
[dockersamples template](https://github.com/dockersamples/sample-app-template)
to initiate a sample repository under your personal namespace. When you've
finished drafting your content and opened your pull request for the
documentation, we can transfer the repository to the dockersamples
organization.

## Writing style

Use
[sentence case](https://docs.docker.com/contribute/style/formatting/#capitalization) for all
headings and titles. This means only the first word and proper nouns are
capitalized.

### Voice and tone

- **Clarity and conciseness**: Use simple language and short sentences to convey information effectively.
- **Active voice**: Write in the active voice to engage the reader (e.g., "Run the command" instead of "The command should be run").
- **Consistency**: Maintain a consistent tone and terminology throughout the guide.

For detailed guidelines, refer to our
[voice and tone documentation](https://docs.docker.com/contribute/style/voice-tone/).

### Formatting conventions

- **Headings**: Use H2 for main sections and H3 for subsections, following sentence case.
- **Code examples**: Provide complete, working code snippets with syntax highlighting.
- **Lists and steps**: Use numbered lists for sequential steps and bullet points for non-sequential information.
- **Emphasis**: Use bold for UI elements (e.g., **Button**), and italics for emphasis.
- **Links**: Use descriptive link text (e.g.,
  [Install Docker](https://docs.docker.com/get-started/get-docker/)).

For more details, see our
[content formatting guidelines](https://docs.docker.com/contribute/style/formatting/)
and
[grammar and style rules](https://docs.docker.com/contribute/style/grammar/).

## Best practices

- **Test all instructions**
  - Ensure all code and commands work as expected.
  - Verify that the guide can be followed successfully from start to finish.
- **Relevance**
  - Focus on real-world applications and scenarios.
  - Keep the content up-to-date with the latest Docker versions.
- **Troubleshooting tips**
  - Anticipate common issues and provide solutions or references.
- **Visual aids**
  - Include screenshots or diagrams where they enhance understanding.
  - Add captions and alt text for accessibility.
- **Third-party tools**
  - Avoid requiring the user to install third-party tools or modify their local development environment.
  - Prefer using containerized tools and methods where applicable (e.g. `docker exec`).
  - Some tools are reasonable to assume as installed or prerequisites for guides, such as Node.js and npm. Use your better judgement.

## Additional resources

- **Existing guides**
  - Refer to
    [Docker Guides](https://docs.docker.com/guides/) for examples and inspiration.
- **Style guides**
  - [Voice and tone](https://docs.docker.com/contribute/style/voice-tone/)
  - [Content formatting](https://docs.docker.com/contribute/style/formatting/)
  - [Grammar and style](https://docs.docker.com/contribute/style/grammar/)

## Submission process

- **Proposal**
  - Raise an issue on the [Docker documentation GitHub repository](https://github.com/docker/docs)
    with a request to add a new guide.
  - Once the proposal has been accepted, start writing your guide by forking
    the repository and creating a branch for your work.
    > Note
    >
    > Avoid contributing from the `main` branch of your fork, since it makes it
    > more difficult for maintainers to help you fix any issues that may arise.
- **Review**
  - Proofread your guide for grammar, clarity, and adherence to the guidelines.
  - Once your draft is ready, raise a pull request, with a reference to the
    original issue.
  - The Docker documentation team and subject matter experts will review your
    submission and provide feedback on the pull request directly.
- **Publishing**
  - Your guide will be published on the Docker documentation website when the
    reviewers have approved and merged your pull request.

Thank you for contributing to the Docker community. Your expertise helps users
worldwide harness the power of Docker.

---

# Formatting guide

> Formatting guidelines for technical documentation

# Formatting guide

   Table of contents

---

## Headings and subheadings

Readers pay fractionally more attention to headings, bulleted lists, and links, so it's important to ensure the first two to three words in those items "front load" information as much as possible.

### Best practice

- Headings and subheadings should let the reader know what they will find on the page.
- They should describe succinctly and accurately what the content is about.
- Headings should be short (no more than eight words), to the point and written in plain, active language.
- You should avoid puns, teasers, and cultural references.
- Skip leading articles (a, the, etc.)

## Page title

Page titles should be action orientated. For example: - *Enable SCIM* - *Install Docker Desktop*

### Best practice

- Make sure the title of your page and the table of contents (TOC) entry matches.
- If you want to use a ‘:’ in a page title in the table of contents (_toc.yaml), you must wrap the entire title in “” to avoid breaking the build.
- If you add a new entry to the TOC file, make sure it ends in a trailing slash (/). If you don't, the page won't show the side navigation.

## Images

Images, including screenshots, can help a reader better understand a concept. However, you should use them sparingly as they tend to go out-of-date.

### Best practice

- When you take screenshots:
  - Don’t use lorem ipsum text. Try to replicate how someone would use the feature in a real-world scenario, and use realistic text.
  - Capture only the relevant UI. Don’t include unnecessary white space or areas of the UI that don’t help illustrate the point.
  - Keep it small. If you don’t need to show the full width of the screen, don’t.
  - Review how the image renders on the page. Make sure the image isn’t blurry or overwhelming.
  - Be consistent. Coordinate screenshots with the other screenshots already on a documentation page for a consistent reading experience.
  - To keep the Git repository light, compress the images (losslessly). Be sure to compress the images before adding them to the repository. Compressing images after adding them to the repository actually worsens the impact on the Git repository (however, it still optimizes the bandwidth during browsing).
  - Don't forget to remove images from the repository that are no longer used.

For information on how to add images to your content, see [Useful component and formatting examples](https://docs.docker.com/contribute/components/images/).

## Links

Be careful not to create too many links, especially within body copy. Excess links can be distracting or send readers away from the current page.

When people follow links, they can often lose their train of thought and fail to return to the original page, despite not having absorbed all the information it contains.

The best links offer readers another way to scan information.

### Best practice

- Use plain language that doesn't mislead or promise too much.
- Be short and descriptive (around five words is best).
- Allow people to predict (with a fair degree of confidence) what they will get if they select a link. Mirror the heading text on the destination page in links whenever possible.
- Front-load user-and-action-oriented terms at the beginning of the link (Download our app).
- Avoid generic calls to action (such as click here, find out more).
- Don't include any end punctuation when you hyperlink text (for example, periods, question marks, or exclamation points).
- Don't make link text italics or bold, unless it would be so as normal body copy.

For information on how to add links to your content, see [Useful component and formatting examples](https://docs.docker.com/contribute/components/links/).

## Code and code samples

Format the following as code: Docker commands, instructions, and filenames (package names).

To apply inline code style, wrap the text in a single backtick (`).

For information on how to add code blocks to your content, see [Useful component and formatting examples](https://docs.docker.com/contribute/components/code-blocks/).

### Best practice for commands

- Command prompt and shell:
  - For a non-privileged shell, prefix commands in code blocks with the $ prompt symbol.
  - For a privileged shell, prefix commands in code blocks with the # prompt symbol.
  - For a remote shell, add the context of the remote machine and exclude the path. For example, `user@host $`.
  - Specify the Windows shell (Command Prompt, PowerShell, or Git Bash), when you add any Windows-specific command. It's not necessary to include a command for each Windows shell.
  - Use tabs when you add commands for multiple operating systems or shells. For information on how to add tabs to your content, see [Tabs](https://docs.docker.com/contribute/components/tabs/).
- Commands that users will copy and run:
  - Add a single command per code block if a command produces output or requires the user to verify the results.
  - Add command output to a separate code block from the command.
- Commands that users won't copy and run:
  - Use POSIX-compatible syntax. It's not necessary to include Windows syntax.
  - Wrap optional arguments in square brackets ( [ ] ).
  - Use pipes ( | ) between mutually exclusive arguments.
  - Use three dots ( ... ) after repeated arguments.

### Best practice for code

- Indent code blocks by 3 spaces when you nest a code block under a list item.
- Use three dots ( ... ) when you omit code.

## Callouts

Use callouts to emphasize selected information on a page.

### Best practice

- Format the word Warning, Important, or Note in bold. Don't bold the content within the callout.
- It's good practice to avoid placing a lot of text callouts on one page. They can create a cluttered appearance if used to excess, and you'll diminish their impact.

| Text callout | Use case scenario | Color or callout box |
| --- | --- | --- |
| Warning | Use a Warning tag to signal to the reader where actions may cause damage to hardware or software loss of data. | Red |
|  | ✅ Example: Warning: When you use the docker login command, your credentials are stored in your home directory in .docker/config.json. The password is base64-encoded in this file. |  |
| Important | Use an Important tag to signal to the reader where actions may cause issues of a lower magnitude. | Yellow |
|  | ✅ Example: Update to the Docker Desktop terms |  |
| Note | Use the Note tag for information that may not apply to all readers, or if the information is tangential to a topic. | Blue |
|  | ✅ Example: Deleting a repository deletes all the images it contains and its build settings. This action cannot be undone. |  |

For information on how to add callouts to your content, see [Useful component and formatting examples](https://docs.docker.com/contribute/components/call-outs/).

## Navigation

When documenting how to navigate through the Docker Desktop or Docker Hub UI:

- Always use location, then action. For example:
  *From theVisibilitydrop-down list (location), select Public (action).*
- Be brief and specific. For example:
  Do: *SelectSave.*
  Don't: *SelectSavefor the changes to take effect.*
- If a step must include a reason, start the step with it. This helps the user scan more quickly.
  Do: *To view the changes, in the merge request, select the link.*
  Don't: *Select the link in the merge request to view the changes*

## Optional steps

If a step is optional, start the step with the word Optional followed by a period.

For example:

*1. Optional. Enter a description for the job.*

## Placeholder text

You might want to provide a command or configuration that uses specific values.

In these cases, use < and > to call out where a reader must replace text with their own value. For example:

`docker extension install <name-of-your-extension>`

## Tables

Use tables to describe complex information in a straightforward manner.

Note that in many cases, an unordered list is enough to describe a list of items with a single, simple description per item. But, if you have data that’s best described by a matrix, tables are the best choice.

### Best practice

- Use sentence case for table headings.
- To keep tables accessible and scannable, tables shouldn't have any empty cells. If there is no otherwise meaningful value for a cell, consider entering N/A for ‘not applicable’ or None.

For information on how to add tables to your content, see [Useful component and formatting examples](https://docs.docker.com/contribute/components/tables/).

## Referring to file types

When you're discussing a file type, use the formal name of the type. Don't use the filename extension to refer generically to the file type.

```
| Correct | Incorrect |
| --- | --- |
| a PNG file | a .png file |
| a Bash file | an .sh file |
```

## Referring to units

When you're referring to units of measurement, use the abbreviated form in all caps, with a space between the value and the unit. For example:

```
| Correct | Incorrect |
| --- | --- |
| 10 GB | 10GB |
| 10 GB | 10 gb |
| 10 GB | 10 gigabytes |
```

---

# Grammar and style

> Grammar and style guidelines for technical documentation

# Grammar and style

   Table of contents

---

Docker documentation should always be written in US English with US grammar.

## Acronyms and initialisms

An acronym is an abbreviation you would speak as a word, for example, ROM (for read only memory). Other examples include radar and scuba, which started out as acronyms but are now considered words in their own right.

An initialism is a type of acronym that comprises a group of initial letters used as an abbreviation for a name or expression. If you were using the acronym in a spoken conversation, you would enunciate each letter: H-T-M-L for Hypertext Markup Language.

### Best practice

- Spell out lesser-known acronyms or initialisms on first use, then follow with the acronym or initialism in parentheses. After this, throughout the rest of your page or document, use the acronym or initialism alone.

> ‘You can use single sign-on (SSO) to sign in to Notion. You may need to ask your administrator to enable SSO.’

- Where the acronym or initialism is more commonly used than the full phrase, for example, URL, HTML, you don't need to follow this spell-it-out rule.
- Use all caps for acronyms of file types (a JPEG file).
- Don't use apostrophes for plural acronyms. ✅URLs ❌URL’S
- Avoid using an acronym for the first time in a title or heading. If the first use of the acronym is in a title or heading, introduce the acronym (in parentheses, following the spelled-out term) in the first body text that follows.

## Bold and italics

Unless you're referring to UI text or user-defined text, you shouldn't add emphasis to text. Clear, front-loaded wording makes the subject of a sentence clear.

### Best practice

- Don't use bold to refer to a feature name.
- Use italics sparingly, as this type of formatting can be difficult to read in digital experiences.
  Notable exceptions are titles of articles, blog posts, or specification documents.

## Capitalization

Use sentence case for just about everything. Sentence case means capitalizing only the first word, as you would in a standard sentence.

The following content elements should use sentence case:

- Titles of webinars and events
- Headings and subheadings in all content types
- Calls to action
- Headers in boxed text
- Column and row headers in tables
- Links
- Sentences (of course)
- Anything in the UI including navigation labels, buttons, headings

### Best practice

- As a general rule, it's best to avoid the use of ALL CAPITALS in most content types. They are more difficult to scan and take up more space. While all caps can convey emphasis, they can also give the impression of shouting.
- If a company name is all lowercase or all uppercase letters, follow their style, even at the beginning of sentences: DISH and bluecrux. When in doubt, check the company's website.
- Use title case for Docker solutions: Docker Extensions, Docker Hub.
- Capitalize a job title if it immediately precedes a name (Chief Executive Officer Scott Johnston).
- Don't capitalize a job title that follows a name or is a generic reference (Scott Johnston, chief executive officer of Docker).
- Capitalize department names when you refer to the name of a department, but use lower case if you are talking about the field of work and not the actual department.
- When referring to specific user interface text, like a button label or menu item, use the same capitalization that’s displayed in the user interface.

## Contractions

A contraction results from letters being left out from the original word or phrase, such as you're for you are or it's for it is.

Following our conversational approach, it's acceptable to use contractions in almost all content types. Just don't get carried away. Too many contractions in a sentence can make it difficult to read.

### Best practice

- Stay consistent - don't switch between contractions and their spelled-out equivalents in body copy or UI text.
- Avoid negative contractions (can't, don't, wouldn't, and shouldn't) whenever possible. Try to rewrite your sentence to align with our helpful approach that puts the focus on solutions, not problems.
- Never contract a noun with is, does, has, or was as this can make it look like the noun is possessive. Your container is ready. Your container’s ready.

## Dangling modifiers

Avoid [dangling modifiers](https://en.wikipedia.org/wiki/Dangling_modifier), where the subject of a clause's verb is unclear:

- ❌ After enabling auto-log-out, your users are logged out.
- ✅ When you enable auto-log-out, your users are logged out.

## Dates

You should use the U.S. format of month day, year format for dates: June 26, 2021.

When possible, use the month's full name (October 1, 2022). If there are space constraints, use 3-letter abbreviations followed by a period (Oct. 1. 2022).

## Decimals and fractions

In all UI content and technical documentation, use decimals instead of fractions.

### Best practice

- Always carry decimals to at least the hundredth place (33.76).
- In tables, align decimals on the decimal point.
- Add a zero before the decimal point for decimal fractions less than one (0.5 cm).

## Lists

Lists are a great way to break down complex ideas and make them easier to read and scan.

### Best practice

- Bulleted lists should contain relatively few words or short phrases. For most content types, limit the number of items in a list to five.
- Don’t add commas (,) or semicolons (;) to the ends of list items.
- Some content types may use bulleted lists that contain 10 items, but it's preferable to break longer lists into several lists, each with its own subheading or introduction.
- Never create a bulleted list with only one bullet, and never use a dash to indicate a bulleted list.
- If your list items are fragments, capitalize the list items for ease of scanning but don't use terminal punctuation.
  Example:
  I went to the shops to buy:
  - Milk
  - Flour
  - Eggs
- Make sure all your list items are parallel. This means you should structure each list item in the same way. They should all be fragments, or they should all be complete sentences. If you start one list item with a verb, then start every list item with a verb.
- Every item in your list should start with a capital letter unless they’re parameters or commands.
- Nested sequential lists are labeled with lowercase letters. For example:
  1. Top level
  2. Top level
    1. Child step
    2. Child step

## Numbers

When you work with numbers in content, the best practices include:

- Spell out the numbers one to nine, except in units of measure such as 4 MB.
- Represent numbers with two or more digits as numerals (10, 625, 773,925).
- Recast a sentence, rather than begin it with a number (unless it's a year).
- When you cite numbers in an example, write them out as they appear in any accompanying screenshots.
- Write numbers out as they appear on the platform when you cite them in an example.
- To refer to large numbers in abstract (such as thousands, millions, and billions), use a combination of words and numbers. Don't abbreviate numeric signifiers.
- Avoid using commas in numbers because they can represent decimals in different cultures. For numbers that are five digits or more, use a space to separate.
  | Correct | Incorrect |
  | --- | --- |
  | 1000 | 1,000 |
  | 14 586 | 14,586 |
  | 1 390 680 | 1,390,680 |

### Versions

When writing version numbers for release notes, use the following example:

- version 4.8.2
- v1.0
- Docker Hub API v2

## Punctuation

### Colons and semicolons

- Use colons to: introduce a list inline in a sentence; introduce a bulleted or numbered list; and provide an explanation.
- Don't use semicolons. Use two sentences instead.

### Commas

- Use the serial or Oxford comma - a comma before the coordinating conjunction (and, or) in a list of three or more things.
- If a series contains more than three items or the items are long, consider a bulleted list to improve readability.

### Dashes and hyphens

- Use the em dash (-) sparingly when you want the reader to pause, to create parenthetical statements, or to emphasize specific words or phrases. Always put a space on either side of the em dash.
- Use an en dash (-) to indicate spans of numbers, dates, or time.
- Use a hyphen to join two or more words to form compound adjectives that precede a noun. The purpose of joining words to form a compound adjective is to differentiate the meaning from the adjectives used separately (for example, ‘up-to-date documentation’ ‘lump-sum payment’, and ‘well-stocked cupboard’. You can also use a hyphen to:
  - Avoid awkward doubling of vowels. For example ‘semi-independence*’,* or ‘re-elect’.
  - Prevent misreading of certain words. For example ‘Re-collect’ means to collect again; without a hyphen the word recollect has a different meaning.

### Exclamation marks

Avoid the use of exclamation marks.

### Parentheses

Don't use parentheses in technical documentation. They can reduce the readability of a sentence.

---

# Recommended word list

> Recommended word list for Technical documentation

# Recommended word list

   Table of contents

---

To help ensure consistency across documentation, the Technical Writing team recommends these wording choices.

#### & (ampersand)

Don't use `&` instead of `and` in headings, text, navigation, UI copy, or tables of contents.

#### above

Try to avoid using `above` when referring to an example or table in a documentation page. If required, use `previous` instead.

For example:

*In the previous example, the dog had fleas.*

#### account name

Don't use. Instead, use `username`.

#### admin

Write out `administrator` on first use. Use `admin` if it's the name of a UI label or other element.

#### allows

Don't use. Instead, use `lets`.

#### as of this writing

Avoid because the writing itself implies this phrase. The phrase can also prematurely share product or feature strategy or inappropriately imply that a product or feature might change.

#### below

Try to avoid `below` when referring to an example or table on a documentation page. If required, use `following` instead.

For example:

*In the following example, the dog had fleas.*

#### checkbox

Use one word for `checkbox`. Don't use `check box`.

You select (not check or enable) and clear (not deselect or disable) checkboxes.

#### click

Don't use `click`. Instead, use `select` with buttons, links, menu items, and lists.

Select applies to more devices, while click is more specific to a mouse.

#### currently

Don't use `currently` when talking about the product or its features. The documentation describes the product as it is today.

#### disable

Don't use `disable`. Implies that disability is a less-desired or negative state.

Instead, use `turn off` or `toggle off`.

There are times with more technical features when the development team uses `disable`, and in these cases, it's OK to use the term.

#### earlier

Use `earlier` when talking about version numbers.

Use:

*In Docker Desktop 4.1 and earlier.*

Instead of:

*In Docker Desktop 4.1 and lower.*

#### easy, easily

What might be easy for you might not be easy for others. Try eliminating this word from the sentence because usually the same meaning can be conveyed without it.

#### e.g.

Don't use. Instead, use phrases like `for example` or `such as`.

#### enable

Don't use `enable`. Implies that disability is a less-desired or negative state.

Instead, use `turn on` or `toggle on`.

There are times with more technical features when the development team uses `enable`, and in these cases, it's OK to use the term.

#### execute

Avoid where possible. Use `run` instead.

#### later

Use `later` when talking about version numbers.

Use:

*In Docker Desktop 4.1 and later.*

Instead of:

*In Docker Desktop 4.1 and higher…* or *In Docker Desktop 4.1 and above…*

#### please

Don't use `please` in the normal course of explaining how to use a product, even if you're explaining a difficult task. Also don't use the phrase `please note`.

#### register

Use `sign up` instead of register when talking about creating an account.

#### repo

Don't use. Instead, use `repository`.

#### respectively

Avoid `respectively` and be more precise instead.

#### scroll

Avoid. Use a verb phrase such as *move through* or *navigate to* instead, if the context is clear.

#### sign in

Use `sign in` instead of `sign on`, `signon`, `log on`, `logon`, or `log in`, `login`. If the user interface uses different words, use those.

Use `sign in to` instead of `sign into`.

#### sign up

Use `sign up` or `create account` instead of `register` when talking about creating an account.

#### tab versus view

Use `view` when referring to a major section in a UI. Use `tab` when referring to a sub-section in the UI.

For example, in Docker Desktop, the **Images** view and the **Local** tab.

#### toggle

You turn on or turn off a toggle. For example:

*Turn on the dark mode toggle.*

#### upgrade

Use `upgrade` when describing a higher subscription tier

#### vs

Don't use `vs` or `vs.` as an abbreviation for versus; instead, use the unabbreviated `versus`.

#### we

Try to avoid `we` and focus instead on how the user can carry out something in Docker.

Use:

*Use widgets when you have work you want to organize.*

Instead of:

*We created a feature for you to add widgets.*

#### wish

Don't use. Use `want` instead.

---

# Docker terminology

> Docker specific terminology and definitions

# Docker terminology

   Table of contents

---

#### compose.yaml

The current designation for the Compose file, as it's a file, format as code.

#### Compose plugin

The compose plugin as an add-on (for Docker CLI) that can be enabled/disabled.

#### Digest

A long string that’s automatically created every time you push an image. You can pull an image by Digest or by Tag.

#### Docker Compose

Use when we talk about the application, or all the functionality associated with the application.

#### docker compose

Use code formatting for referring to the commands in text and command usage examples/code samples.

#### Docker Compose CLI

Use when referring to family of Compose commands as offered from the Docker CLI.

#### K8s

Don't use. Use `Kubernetes` instead.

#### Multi-platform

(broad meaning) Mac vs Linux vs Microsoft but also pair of platform architecture such as in Linux/amd64 and Linux/arm64; (narrow meaning) Windows/Linux/macOS.

#### Multi-architecture / multi-arch

To use when referring specifically to CPU architecture or something that is hardware-architecture-based. Avoid using it as meaning the same as multi-platform.

#### Member

A user of Docker Hub that is a part of an organization

#### Namespace

Organization or User name. Every image needs a namespace to live under.

#### Node

A node is a physical or virtual machine running an instance of the Docker Engine in swarm mode.
Manager nodes perform swarm management and orchestration duties. By default manager nodes are also worker nodes.
Worker nodes invoke tasks.

#### Registry

Online storage for Docker images.

#### Repository

Lets users share container images with their team, customers, or Docker community.

---

# Voice and tone

> Docker's voice and tone

# Voice and tone

   Table of contents

---

## Voice

At Docker, we've been the customer. We're developers developing for developers. We speak with experience and knowledge and without arrogance or ego. We want to inform and empower people without being confusing or pushy.

We're not afraid to use a bit of cheeky humor to lighten the conversation (and because we don't take ourselves too seriously) but we're always respectful. We communicate with clarity, empathy, and wit; everything we say should inform and encourage.

We align our tone of voice and content with our virtues. The most important principles we follow when we write are the 4Cs:

1. **Correct**
2. **Concise**
3. **Complete**
4. **Clear**

We ensure the information is accurate, succinct, thorough, and easy to understand. We keep sentences as simple as possible, but include enough detail for the user to complete the intended task.

All of this means that when we write documentation and UI copy:

1. **We are honest.** We give you all the facts and we don't use misdirection or make ambiguous statements. We don't always have all the answers, but we're doing our best to make life better for developers and we'll tell you how it's going.
2. **We are concise.** We understand the industry of complex and detailed messaging our users live in because we come from the same world. Docker doesn't bulk up our communication with fluffy words or complex metaphors. We're clear and to the point.
3. **We are relaxed.** Our demeanor is casual but not lazy, smart but not arrogant, and focused but not cold. Our voice should be welcoming and warm.
4. **We are inclusive.** Developers are developers no matter how much code they've written. Every person is as much a part of our community as the next. We are accepting of all developers from all industries and experience levels.

## Tone

Docker's tone is usually informal, but we believe it's always more important to be clear over comical. We're relaxed, but we're not inappropriate or unprofessional.

### Friendly tone

Use a tone that's natural, friendly, and respectful without being overly colloquial or full of jargon. Write to inform and empower developers without being confusing or pushy. It’s OK to use contractions as long as the sentence doesn’t become too slangy or informal.

**Avoid overdoing politeness.** It is good to be friendly and polite, but using ‘please’ in technical documentation or UI copy might be overdoing the politeness.

### Positive language

Use positive language. Instead of highlighting the limitations and what the users cannot do, emphasize the positive outcomes.

For example, **instead of**:

“*Features such as Single Sign-on (SSO), Image Access Management, Registry Access Management are not available in Docker Team subscription.”*

**Use**:

“*Features such as Single Sign-on (SSO), Image Access Management, Registry Access Management are available in Docker Business subscription*.”
