# Changelogs and more

# Changelogs

> Create product changelogs with RSS feed support for subscribers.

Create a changelog for your docs by adding [Update components](https://mintlify.com/docs/components/update) to a page. Check out the [Mintlify changelog](https://mintlify.com/docs/changelog) as an example: you can include links, images, text, and demos of your new features in each update.

## ​Setting up your changelog

 1

Create a page for your changelog

1. Create a new page in your docs such as `changelog.mdx` or `updates.mdx`.
2. Add your changelog page to your navigation scheme in your `docs.json`.

2

Add Update components to your changelog

Add an `Update` for each changelog entry.Include relevant information like feature releases, bug fixes, or other announcements. Example changelog.mdx

```
---
title: "Changelog"
description: "Product updates and announcements"
---
<Update label="March 2025" description="v0.0.10">
  Added a new Wintergreen flavor.

  Released a new version of the Spearmint flavor, now with 10% more mint.
</Update>

<Update label="February 2025" description="v0.0.09">
  Released a new version of the Spearmint flavor.
</Update>
```

## ​Customizing your changelog

 Control how people navigate your changelog and stay up to date with your product information.

### ​Table of contents

 Each `label` property for an `Update` automatically creates an entry in the right sidebar’s table of contents. This is the default navigation for your changelog. ![Changelog with table of contents displayed in light mode.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/changelog-toc-light.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=3f3018782389da4ccab476fbecfaa84b)![Changelog with table of contents displayed in dark mode.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/changelog-toc-dark.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=d8e69af3525f597335e5d2dcb6ec8192)

### ​Tag filters

 Add `tags` to your `Update` components to replace the table of contents with tag filters. Users can filter the changelog by selecting one or more tags: Tag filters example

```
<Update label="March 2025" description="v0.0.10" tags={["Wintergreen", "Spearmint"]}>
  Added a new Wintergreen flavor.

  Released a new version of the Spearmint flavor, now with 10% more mint.
</Update>

<Update label="February 2025" description="v0.0.09" tags={["Spearmint"]}>
  Released a new version of the Spearmint flavor.
</Update>

<Update label="January 2025" description="v0.0.08" tags={["Peppermint", "Spearmint"]}>
  Deprecated the Peppermint flavor.

  Released a new version of the Spearmint flavor.
</Update>
```

 ![Changelog in light mode with the Peppermint tag filter selected.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/changelog-filters-light.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=1c6e5fc5902e27e520fa217924871589)![Changelog in dark mode with the Peppermint tag filter selected.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/changelog-filters-dark.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=5aad3dbe45acd21db99dfae04b4846f7) The table of contents and changelog filters are hidden when using `custom`, `center`, or `wide` page modes. Learn more about [page modes](https://mintlify.com/docs/organize/pages#page-mode).

### ​Subscribable changelogs

 RSS feeds are only available on public documentation. Use `Update` components to create a subscribable RSS feed at your page URL with `/rss.xml` appended. For example, `mintlify.com/docs/changelog/rss.xml`. The RSS feed publishes entries when you add new `Update` components and when modify headings inside of existing `Update` components. RSS feed entries contain pure Markdown only. Components, code, and HTML elements are excluded. Use the `rss` property to provide alternative text descriptions for RSS subscribers when your updates include content that is excluded. Example RSS feed

```
<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
  <channel>
    <title><![CDATA[Product updates]]></title>
    <description><![CDATA[New updates and improvements]]></description>
    <link>https://mintlify.com/docs</link>
    <generator>RSS for Node</generator>
    <lastBuildDate>Mon, 21 Jul 2025 21:21:47 GMT</lastBuildDate>
    <atom:link href="https://mintlify.com/docs/changelog/rss.xml" rel="self" type="application/rss+xml"/>
    <copyright><![CDATA[Mintlify]]></copyright>
    <docs>https://mintlify.com/docs</docs>
    <item>
      <title><![CDATA[June 2025]]></title>
      <link>https://mintlify.com/docs/changelog#june-2025</link>
      <guid isPermaLink="true">https://mintlify.com/docs/changelog#june-2025</guid>
      <pubDate>Mon, 23 Jun 2025 16:54:22 GMT</pubDate>
    </item>
  </channel>
</rss>
```

 RSS feeds can integrate with Slack, email, or other subscription tools to notify users of product changes. Some options include:

- [Slack](https://slack.com/help/articles/218688467-Add-RSS-feeds-to-Slack)
- [Email](https://zapier.com/apps/email/integrations/rss/1441/send-new-rss-feed-entries-via-email) via Zapier
- Discord bots like [Readybot](https://readybot.io) or [RSS Feeds to Discord Bot](https://rss.app/en/bots/rssfeeds-discord-bot)

 To make the RSS feed discoverable, you can display an RSS icon button that links to the feed at the top of the page. Add `rss: true` to the page frontmatter:

```
---
rss: true
---
```

 ![Changelog page in light mode with RSS feed button enabled.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/changelog-rss-button-light.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=088f41b7cdb5f701909d2c5cea5e52fd)![Changelog page in dark mode with RSS feed button enabled.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/changelog-rss-button-dark.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=67b22fea2a8411fe4c38caf569a8bf5f)

---

# Format code

> Display and style inline code and code blocks.

## ​Adding code samples

 You can add inline code snippets or code blocks. Code blocks support meta options for syntax highlighting, titles, line highlighting, icons, and more.

### ​Inline code

 To denote a `word` or `phrase` as code, enclose it in backticks (`).

```
To denote a `word` or `phrase` as code, enclose it in backticks (`).
```

### ​Code blocks

 Use [fenced code blocks](https://www.markdownguide.org/extended-syntax/#fenced-code-blocks) by enclosing code in three backticks. Code blocks are copyable, and if you have the assistant enabled, users can ask AI to explain the code. Specify the programming language for syntax highlighting and to enable meta options. Add any meta options, like a title or icon, after the language.

```
class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

## ​Code block options

 Add meta options to your code blocks to customize their appearance. You must specify a programming language for a code block before adding any other meta options.

### ​Option syntax

- **String and boolean options**: Wrap with `""`, `''`, or no quotes.
- **Expression options**: Wrap with `{}`, `""`, or `''`.

### ​Syntax highlighting

 Enable syntax highlighting by specifying the programming language after the opening backticks of a code block. We use [Shiki](https://shiki.style/) for syntax highlighting and support all available languages. See the full list of [languages](https://shiki.style/languages) in Shiki’s documentation. Customize code block themes globally using `styling.codeblocks` in your `docs.json` file. Set simple themes like `system` or `dark`, or configure custom [Shiki themes](https://shiki.style/themes) for light and dark modes. See [Settings](https://mintlify.com/docs/organize/settings#param-styling) for configuration options.

```
class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

Custom syntax highlighting theme

For custom themes, set your theme in `docs.json` to `"css-variables"` and override syntax highlighting colors using CSS variables with the `--mint-` prefix.The following variables are available:**Basic colors**

- `--mint-color-text`: Default text color
- `--mint-color-background`: Background color

**Token colors**

- `--mint-token-constant`: Constants and literals
- `--mint-token-string`: String values
- `--mint-token-comment`: Comments
- `--mint-token-keyword`: Keywords
- `--mint-token-parameter`: Function parameters
- `--mint-token-function`: Function names
- `--mint-token-string-expression`: String expressions
- `--mint-token-punctuation`: Punctuation marks
- `--mint-token-link`: Links

**ANSI colors**

- `--mint-ansi-black`, `--mint-ansi-black-dim`
- `--mint-ansi-red`, `--mint-ansi-red-dim`
- `--mint-ansi-green`, `--mint-ansi-green-dim`
- `--mint-ansi-yellow`, `--mint-ansi-yellow-dim`
- `--mint-ansi-blue`, `--mint-ansi-blue-dim`
- `--mint-ansi-magenta`, `--mint-ansi-magenta-dim`
- `--mint-ansi-cyan`, `--mint-ansi-cyan-dim`
- `--mint-ansi-white`, `--mint-ansi-white-dim`
- `--mint-ansi-bright-black`, `--mint-ansi-bright-black-dim`
- `--mint-ansi-bright-red`, `--mint-ansi-bright-red-dim`
- `--mint-ansi-bright-green`, `--mint-ansi-bright-green-dim`
- `--mint-ansi-bright-yellow`, `--mint-ansi-bright-yellow-dim`
- `--mint-ansi-bright-blue`, `--mint-ansi-bright-blue-dim`
- `--mint-ansi-bright-magenta`, `--mint-ansi-bright-magenta-dim`
- `--mint-ansi-bright-cyan`, `--mint-ansi-bright-cyan-dim`
- `--mint-ansi-bright-white`, `--mint-ansi-bright-white-dim`

**Custom syntax highlighting**Add syntax highlighting for languages not included in Shiki’s default set by providing custom TextMate grammar files. Create a JSON file following the [TextMate grammar format](https://macromates.com/manual/en/language_grammars), then reference it in your `docs.json`. You can add multiple custom languages by including additional paths in the array.docs.json

```
{
  "styling": {
    "codeblocks": {
      "languages": {
        "custom": ["/languages/my-custom-language.json"]
      }
    }
  }
}
```

### ​Twoslash

 In JavaScript and TypeScript code blocks, use `twoslash` to enable interactive type information. Users can hover over variables, functions, and parameters to see types and errors like in an IDE.

```
type Pet = "cat" | "dog" | "hamster";

function adoptPet(name: string, type: Pet) {
  return `${name} the ${type} is now adopted!`;
}

// Hover to see the inferred types
const message = adoptPet("Mintie", "cat");
```

### ​Title

 Add a title to label your code example. Use `title="Your title"` or a string on a single line.

```
const hello = "world";
```

### ​Icon

 Add an icon to your code block using the `icon` property. See [Icons](https://mintlify.com/docs/components/icons) for all available options.

```
const hello = "world";
```

### ​Line highlighting

 Highlight specific lines in your code blocks using `highlight` with the line numbers or ranges you want to highlight.

```
const greeting = "Hello, World!";
function sayHello() {
  console.log(greeting);
}
sayHello();
```

### ​Line focusing

 Focus on specific lines in your code blocks using `focus` with line numbers or ranges.

```
const greeting = "Hello, World!";
function sayHello() {
  console.log(greeting);
}
sayHello();
```

### ​Show line numbers

 Display line numbers on the left side of your code block using `lines`.

```
const greeting = "Hello, World!";
function sayHello() {
  console.log(greeting);
}
sayHello();
```

### ​Expandable

 Allow users to expand and collapse long code blocks using `expandable`.

```
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Book:
title: str
author: str
isbn: str
checked_out: bool = False
due_date: Optional[datetime] = None

class Library:
def **init**(self):
self.books: Dict[str, Book] = {}
self.checkouts: Dict[str, List[str]] = {} # patron -> list of ISBNs

    def add_book(self, book: Book) -> None:
        if book.isbn in self.books:
            raise ValueError(f"Book with ISBN {book.isbn} already exists")
        self.books[book.isbn] = book

    def checkout_book(self, isbn: str, patron: str, days: int = 14) -> None:
        if patron not in self.checkouts:
            self.checkouts[patron] = []

        book = self.books.get(isbn)
        if not book:
            raise ValueError("Book not found")

        if book.checked_out:
            raise ValueError("Book is already checked out")

        if len(self.checkouts[patron]) >= 3:
            raise ValueError("Patron has reached checkout limit")

        book.checked_out = True
        book.due_date = datetime.now() + timedelta(days=days)
        self.checkouts[patron].append(isbn)

    def return_book(self, isbn: str) -> float:
        book = self.books.get(isbn)
        if not book or not book.checked_out:
            raise ValueError("Book not found or not checked out")

        late_fee = 0.0
        if datetime.now() > book.due_date:
            days_late = (datetime.now() - book.due_date).days
            late_fee = days_late * 0.50

        book.checked_out = False
        book.due_date = None

        # Remove from patron's checkouts
        for patron, books in self.checkouts.items():
            if isbn in books:
                books.remove(isbn)
                break

        return late_fee

    def search(self, query: str) -> List[Book]:
        query = query.lower()
        return [
            book for book in self.books.values()
            if query in book.title.lower() or query in book.author.lower()
        ]

def main():
library = Library()

    # Add some books
    books = [
        Book("The Hobbit", "J.R.R. Tolkien", "978-0-261-10295-4"),
        Book("1984", "George Orwell", "978-0-452-28423-4"),
    ]

    for book in books:
        library.add_book(book)

    # Checkout and return example
    library.checkout_book("978-0-261-10295-4", "patron123")
    late_fee = library.return_book("978-0-261-10295-4")
    print(f"Late fee: ${late_fee:.2f}")

if **name** == "**main**":
main()
```

### ​Wrap

 Enable text wrapping for long lines using `wrap`. This prevents horizontal scrolling and makes long lines easier to read.

```
const greeting =
  "Hello, World! I am a long line of text that will wrap to the next line.";
function sayHello() {
  console.log(greeting);
}
sayHello();
```

### ​Diff

 Show a visual diff of added or removed lines in your code blocks. Added lines are highlighted in green and removed lines are highlighted in red. To create diffs, add these special comments at the end of lines in your code block:

- `// [!code ++]`: Mark a line as added (green highlight).
- `// [!code --]`: Mark a line as removed (red highlight).

 For multiple consecutive lines, specify the number of lines after a colon:

- `// [!code ++:3]`: Mark the current line plus the next two lines as added.
- `// [!code --:5]`: Mark the current line plus the next four lines as removed.

 The comment syntax must match your programming language (for example, `//` for JavaScript or `#` for Python).

```
const greeting = "Hello, World!";
function sayHello() {
  console.log("Hello, World!");
  console.log(greeting);
}
sayHello();
```

## ​CodeBlock component

 Use the `<CodeBlock>` component in custom React components to programmatically render code blocks with the same styling and features as markdown code blocks.

### ​Props

 [​](#param-language)languagestringThe programming language for syntax highlighting. [​](#param-filename)filenamestringThe filename to display in the code block header. [​](#param-icon)iconstringThe icon to display in the code block header. See [Icons](https://mintlify.com/docs/components/icons)
for available options. [​](#param-lines)linesbooleanWhether to show line numbers. [​](#param-wrap)wrapbooleanWhether to wrap the code block. [​](#param-expandable)expandablebooleanWhether to expand the code block. [​](#param-highlight)highlightstringThe lines to highlight. Provide a stringified array of numbers. Example:
`"[1,3,4,5]"`. [​](#param-focus)focusstringThe lines to focus on. Provide a stringified array of numbers. Example:
`"[1,3,4,5]"`.

### ​Example

```
export const CustomCodeBlock = ({
  filename,
  icon,
  language,
  highlight,
  children,
}) => {
  return (
    <CodeBlock
      filename={filename}
      icon={icon}
      language={language}
      lines
      highlight={highlight}
    >
      {children}
    </CodeBlock>
  );
};
```

---

# Files

> Serve static assets from your documentation.

Mintlify automatically serves static assets from your documentation repository at the appropriate path on your domain. For example, if you have `/images/my-logo.png` in your repo, the image file is available at `https://docs.your-project.com/images/my-logo.png`. You can make any supported file type available to your users, including OpenAPI specifications, images, videos, and more. Files must be less than 20 MB for images and 100 MB for other file types. File serving is not supported for documentation sites with authentication enabled. If your site requires authentication, static files will not be accessible at their direct URLs.

## ​Supported file types

 Supported file types for all plans:

- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.ico`
- **Video**: `.mp4`, `.webm`
- **Audio**: `.mp3`, `.wav`
- **Data**: `.json`, `.yaml`
- **Stylesheets**: `.css`
- **Scripts**: `.js`
- **Fonts**: `.woff`, `.woff2`, `.ttf`, `.eot`

 Supported file types for Custom plans:

- **Documents**: `.pdf`, `.txt`
- **Data**: `.xml`, `.csv`
- **Archives**: `.zip`

## ​File organization

 Organize your files using folders to keep your repository easy to navigate:

```
/your-project
  |- docs.json
  |- images/
    |- logo.png
    |- screenshots/
      |- dashboard.png
  |- assets/
    |- whitepaper.pdf
    |- demo-video.mp4
```

 Files are served from the root of your domain, so the structure in your repository directly maps to the URL structure. From the previous example, `assets/whitepaper.pdf` would be available at `https://docs.your-project.com/assets/whitepaper.pdf`.

---

# Images and embeds

> Add images, videos, andiframes.

Add images, embed videos, and include interactive content with iframes to your documentation. ![Photograph of a scenic landscape with purple flowers in the foreground, mountains in the background, and a blue sky with scattered clouds.](https://mintlify-assets.b-cdn.net/bigbend.jpg)

## ​Images

 Add images to provide visual context, examples, or decoration to your documentation.

### ​Basic image syntax

 Use [Markdown syntax](https://www.markdownguide.org/basic-syntax/#images) to add images to your documentation:

```
![Alt text describing the image](/path/to/image.png)
```

 Always include descriptive alt text to improve accessibility and SEO. The alt text should clearly describe what the image shows. Image files must be less than 20 MB. For larger files, host them on a CDN service like [Amazon S3](https://aws.amazon.com/s3) or [Cloudinary](https://cloudinary.com).

### ​HTML image embeds

 For more control over image display, use HTML `<img>` tags:

```
<img
  src="/images/dashboard.png"
  alt="Main dashboard interface"
  style={{height: "300px", width: "400px"}}
  className="rounded-lg"
/>
```

#### ​Resize images with inline styles

 Use JSX inline styles with the `style` attribute to resize images:

```
<img
  src="/images/architecture.png"
  style={{width: "450px", height: "auto"}}
  alt="Diagram showing the architecture of the system"
/>
```

#### ​Disable zoom functionality

 To disable the default zoom on click for images, add the `noZoom` property:

```
<img
  src="/images/screenshot.png"
  alt="Descriptive alt text"
  noZoom
/>
```

#### ​Link images

 To make an image a clickable link, wrap the image in an anchor tag and add the `noZoom` property:

```
<a href="https://mintlify.com" target="_blank">
  <img
    src="/images/logo.png"
    alt="Mintlify logo"
    noZoom
  />
</a>
```

 Images within anchor tags automatically display a pointer cursor to indicate they are clickable.

#### ​Light and dark mode images

 To display different images for light and dark themes, use Tailwind CSS classes:

```

<img
  className="block dark:hidden"
  src="/images/light-mode.png"
  alt="Light mode interface"
/>

<img
  className="hidden dark:block"
  src="/images/dark-mode.png"
  alt="Dark mode interface"
/>
```

## ​Videos

 Mintlify supports [HTML tags in Markdown](https://www.markdownguide.org/basic-syntax/#html), giving you flexibility to create rich content. Always include fallback text content within video elements for browsers that don’t support video playback.

### ​YouTube embeds

 Embed YouTube videos using iframe elements:

```
<iframe
  className="w-full aspect-video rounded-xl"
  src="https://www.youtube.com/embed/4KzFe50RQkQ"
  title="YouTube video player"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen
></iframe>
```

### ​Self-hosted videos

 Use the HTML `<video>` element for self-hosted video content:

```
<video
  controls
  className="w-full aspect-video rounded-xl"
  src="link-to-your-video.com"
></video>
```

### ​Autoplay videos

 To autoplay a video, use:

```
<video
  autoPlay
  muted
  loop
  playsInline
  className="w-full aspect-video rounded-xl"
  src="/videos/demo.mp4"
></video>
```

 When using JSX syntax, write double-word attributes in camelCase: `autoPlay`, `playsInline`, `allowFullScreen`.

## ​iframes

 Embed external content using iframe elements:

```
<iframe
  src="https://example.com/embed"
  title="Embedded content"
  className="w-full h-96 rounded-xl"
></iframe>
```

## ​Related resources

 [Frame component referenceLearn how to use the Frame component for presenting images.](https://mintlify.com/docs/components/frames)

---

# Lists and tables

> Format structured data with tables and lists.

## ​Lists

 Lists follow the official [Markdown syntax](https://www.markdownguide.org/basic-syntax/#lists-1).

### ​Ordered list

 To create an ordered list, add numbers followed by a period before list items.

1. First item
2. Second item
3. Third item
4. Fourth item

```
1. First item
2. Second item
3. Third item
4. Fourth item
```

### ​Unordered list

 To create an unordered list, add dashes (`-`), asterisks (`*`), or plus signs (`+`) before list items.

- First item
- Second item
- Third item
- Fourth item

```
- First item
- Second item
- Third item
- Fourth item
```

### ​Nested list

 Indent list items to nest them.

- First item
- Second item
  - Additional item
  - Additional item
- Third item

```
- First item
- Second item
  - Additional item
  - Additional item
- Third item
```

## ​Tables

 Tables follow the official [Markdown syntax](https://www.markdownguide.org/extended-syntax/#tables). To add a table, use three or more hyphens (`---`) to create each column’s header, and use pipes (`|`) to separate each column. For compatibility, you should also add a pipe on either end of the row.

| Property | Description |
| --- | --- |
| Name | Full name of user |
| Age | Reported age |
| Joined | Whether the user joined the community |

```
| Property | Description                           |
| -------- | ------------------------------------- |
| Name     | Full name of user                     |
| Age      | Reported age                          |
| Joined   | Whether the user joined the community |
```

### ​Column alignment

 Use colons in the separator row to align column content:

| Left aligned | Center aligned | Right aligned |
| --- | --- | --- |
| Left | Center | Right |
| Text | Text | Text |

```
| Left aligned | Center aligned | Right aligned |
| :----------- | :------------: | ------------: |
| Left         | Center         | Right         |
| Text         | Text           | Text          |
```

---

# Redirects

> Configure redirects for moved, renamed, or deleted pages.

When you change the path of a file in your docs folder, it also changes the URL path to that page. This may happen when restructuring your docs or changing the sidebar title.

## ​Redirects

 Set up 301 redirects by adding the `redirects` field to your `docs.json` file.

```
"redirects": [
  {
    "source": "/source/path",
    "destination": "/destination/path"
  }
]
```

 This permanently redirects `/source/path` to `/destination/path` so that you don’t lose any previous SEO for the original page.

### ​Wildcard redirects

 To match a wildcard path, use `*` after a parameter. In this example, `/beta/:slug*` matches `/beta/introduction` and redirects it to `/v2/introduction`.

```
"redirects": [
  {
    "source": "/beta/:slug*",
    "destination": "/v2/:slug*"
  }
]
```

### ​Partial wildcard redirects

 Use partial wildcards to match URL segments that start with a specific prefix.

```
"redirects": [
  {
    "source": "/articles/concepts-*",
    "destination": "/collections/overview"
  }
]
```

 This matches any URLs with the `/articles/concepts-` path, such as `/articles/concepts-getting-started` and `/articles/concepts-overview`, and redirects them all to `/collections/overview`. You can also substitute the captured wildcard value in the destination.

```
"redirects": [
  {
    "source": "/old/article-*",
    "destination": "/new/article-*"
  }
]
```

 This redirects `/old/article-123` to `/new/article-123`, preserving the captured value after the prefix.

### ​Avoid infinite redirects

 To avoid infinite loops, do not create circular redirects where paths redirect back to each other.

```
"redirects": [
  {
    "source": "/docs/:slug*",
    "destination": "/help/:slug*"
  },
  {
    "source": "/help/:slug*",
    "destination": "/docs/:slug*"
  }
]
```

## ​Check for broken links

 Find broken links with the [CLI](https://mintlify.com/docs/installation).

```
mint broken-links
```

---

# Reusable snippets

> Create reusable snippets to maintain consistency across pages.

One of the core principles of software development is DRY (Don’t Repeat Yourself), which applies to documentation too. If you find yourself repeating the same content in multiple places, create a custom snippet for that content. Snippets contain content that you can import into other files to reuse. You control where the snippet appears on a page. If you ever need to update the content, you only need to edit the snippet rather than every file where the snippet is used.

## ​How snippets work

 Snippets are any `.mdx`, `.md`, or `.jsx` files imported into another file. You can place snippet files anywhere in your project. When you import a snippet into another file, the snippet only appears where you import it and does not render as a standalone page. Any file in the `/snippets/` folder is always a snippet even if it is not imported into another file.

## ​Create snippets

 Create a file with the content you want to reuse. Snippets can contain all content types supported by Mintlify and they can import other snippets.

## ​Import snippets into pages

 Import snippets into pages using either an absolute or relative path.

- **Absolute imports**: Start with `/` for imports from the root of your project.
- **Relative imports**: Use `./` or `../` to import snippets relative to the current file’s location.

 Relative imports enable IDE navigation. Press CMD and click a snippet name in your editor to jump directly to the snippet definition.

### ​Import text

1. Add content to your snippet file that you want to reuse. shared/my-snippet.mdx
  ```
  Hello world! This is my content I want to reuse across pages.
  ```
2. Import the snippet into your destination file using either an absolute or relative path.
  ```
  ---
  title: "An example page"
  description: "This is an example page that imports a snippet."
  ---
  import MySnippet from "/shared/my-snippet.mdx";
  The snippet content displays beneath this sentence.
  <MySnippet />
  ```

### ​Import variables

 Reference variables from a snippet in a page.

1. Export variables from a snippet file. shared/custom-variables.mdx
  ```
  export const myName = "Ronan";
  export const myObject = { fruit: "strawberries" };
  ;
  ```
2. Import the snippet from your destination file and use the variable. destination-file.mdx
  ```
  ---
  title: "An example page"
  description: "This is an example page that imports a snippet with variables."
  ---
  import { myName, myObject } from "/shared/custom-variables.mdx";
  Hello, my name is {myName} and I like {myObject.fruit}.
  ```

### ​Import snippets with variables

 Use variables to pass data to a snippet when you import it.

1. Add variables to your snippet and pass in properties when you import it. In this example, the variable is `{word}`. shared/my-snippet.mdx
  ```
  My keyword of the day is {word}.
  ```
2. Import the snippet into your destination file with the variable. The passed property replaces the variable in the snippet definition. destination-file.mdx
  ```
  ---
  title: "An example page"
  description: "This is an example page that imports a snippet with a variable."
  ---
  import MySnippet from "/shared/my-snippet.mdx";
  <MySnippet word="bananas" />
  ```

### ​Import React components

1. Create a snippet with a JSX component. See [React components](https://mintlify.com/docs/customize/react-components) for more information. components/my-jsx-snippet.jsx
  ```
  export const MyJSXSnippet = () => {
    return (
      <div>
        <h1>Hello, world!</h1>
      </div>
    );
  };
  ```

 When creating JSX snippets, use arrow function syntax (`=>`) rather than function declarations. The `function` keyword is not supported in snippets.

1. Import the snippet. destination-file.mdx
  ```
  ---
  title: "An example page"
  description: "This is an example page that imports a snippet with a React component."
  ---
  import { MyJSXSnippet } from "/components/my-jsx-snippet.jsx";
  <MyJSXSnippet />
  ```

---

# Format text

> Learn how to format text, create headers, and style content.

## ​Headers

 Headers organize your content and create navigation anchors. They appear in the table of contents and help users scan your documentation.

### ​Creating headers

 Use `#` symbols to create headers of different levels:

```
## Main section header
### Subsection header
#### Sub-subsection header
```

 Use descriptive, keyword-rich headers that clearly indicate the content that follows. This improves both user navigation and search engine optimization.

### ​Disabling anchor links

 By default, headers include clickable anchor links that allow users to link directly to specific sections. You can disable these anchor links using the `noAnchor` prop in HTML or React headers.

```
<h2 noAnchor>
Header without anchor link
</h2>
```

 When `noAnchor` is used, the header will not display the anchor chip and clicking the header text will not copy the anchor link to the clipboard.

## ​Text formatting

 We support most Markdown formatting for emphasizing and styling text.

### ​Basic formatting

 Apply these formatting styles to your text:

| Style | Syntax | Example | Result |
| --- | --- | --- | --- |
| Bold | **text** | **important note** | important note |
| Italic | _text_ | _emphasis_ | emphasis |
| Strikethrough | ~text~ | ~deprecated feature~ | deprecated feature |

### ​Combining formats

 You can combine formatting styles:

```
**_bold and italic_**
**~~bold and strikethrough~~**
*~~italic and strikethrough~~*
```

 *bold and italic*
 **bold and strikethrough**
 *italic and strikethrough*

### ​Superscript and subscript

 For mathematical expressions or footnotes, use HTML tags:

| Type | Syntax | Example | Result |
| --- | --- | --- | --- |
| Superscript | <sup>text</sup> | example<sup>2</sup> | example2 |
| Subscript | <sub>text</sub> | example<sub>n</sub> | examplen |

## ​Links

 Links help users navigate between pages and access external resources. Use descriptive link text to improve accessibility and user experience.

### ​Internal links

 Link to other pages in your documentation using root-relative paths:

```
[Quickstart](/quickstart)
[Steps](/components/steps)
```

 [Quickstart](https://mintlify.com/docs/quickstart)
 [Steps](https://mintlify.com/docs/components/steps)

### ​External links

 For external resources, include the full URL:

```
[Markdown Guide](https://www.markdownguide.org/)
```

 [Markdown Guide](https://www.markdownguide.org/)

### ​Broken links

 You can check for broken links in your documentation using the [CLI](https://mintlify.com/docs/installation):

```
mint broken-links
```

## ​Blockquotes

 Blockquotes highlight important information, quotes, or examples within your content.

### ​Single line blockquotes

 Add `>` before text to create a blockquote:

```
> This is a quote that stands out from the main content.
```

> This is a quote that stands out from the main content.

### ​Multi-line blockquotes

 For longer quotes or multiple paragraphs:

```
> This is the first paragraph of a multi-line blockquote.
>
> This is the second paragraph, separated by an empty line with `>`.
```

> This is the first paragraph of a multi-line blockquote. This is the second paragraph, separated by an empty line with `>`.

 Use blockquotes sparingly to maintain their visual impact and meaning. Consider using [callouts](https://mintlify.com/docs/components/callouts) for notes, warnings, and other information.

## ​Mathematical expressions

 We support LaTeX for rendering mathematical expressions and equations. You can override automated detection by configuring `styles.latex` in your `docs.json` [settings](https://mintlify.com/docs/organize/settings#param-latex).

### ​Inline math

 Use single dollar signs, `$`, for inline mathematical expressions:

```
The Pythagorean theorem states that $(a^2 + b^2 = c^2)$ in a right triangle.
```

 The Pythagorean theorem states that (a2+b2=c2)(a^2 + b^2 = c^2) in a right triangle.

### ​Block equations

 Use double dollar signs, `$$`, for standalone equations:

```
$$
E = mc^2
$$
```

 E=mc2E = mc^2 LaTeX support requires proper mathematical syntax. Refer to the [LaTeX documentation](https://www.latex-project.org/help/documentation/) for comprehensive syntax guidelines.

## ​Line breaks and spacing

 Control spacing and line breaks to improve content readability.

### ​Paragraph breaks

 Separate paragraphs with blank lines:

```
This is the first paragraph.

This is the second paragraph, separated by a blank line.
```

 This is the first paragraph. This is the second paragraph, separated by a blank line.

### ​Manual line breaks

 Use HTML `<br />` tags for forced line breaks within paragraphs:

```
This line ends here.<br />
This line starts on a new line.
```

 This line ends here.

This line starts on a new line. In most cases, paragraph breaks with blank lines provide better readability than manual line breaks.

## ​Best practices

### ​Content organization

- Use headers to create clear content hierarchy
- Follow proper header hierarchy (don’t skip from H2 to H4)
- Write descriptive, keyword-rich header text

### ​Text formatting

- Use bold for emphasis, not for entire paragraphs
- Reserve italics for terms, titles, or subtle emphasis
- Avoid over-formatting that distracts from content

### ​Links

- Write descriptive link text instead of “click here” or “read more”
- Use root-relative paths for internal links
- Test links regularly to prevent broken references
