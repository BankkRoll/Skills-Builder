# Analytics and more

# Analytics

> Track documentation analytics and understand content effectiveness with visitor data.

The [analytics](https://dashboard.mintlify.com/products/analytics/v2/) page in your dashboard shows data about visitors to your docs, how they interact with the assistant, what they search for, and their feedback. Use this information to identify which pages are most valuable to your users and track trends over time. Use the range selector to adjust the time period for displayed data. ![The range selector expanded to show options for viewing different time periods of data.](https://mintcdn.com/mintlify/4a6DEBu5ODMCZacH/images/analytics/range-selector-light.png?fit=max&auto=format&n=4a6DEBu5ODMCZacH&q=85&s=978fd281985851ae04755348025dc2c2)![The range selector expanded to show options for viewing different time periods of data.](https://mintcdn.com/mintlify/4a6DEBu5ODMCZacH/images/analytics/range-selector-dark.png?fit=max&auto=format&n=4a6DEBu5ODMCZacH&q=85&s=cc98997901d0b9ceb237ecf3bab93aed)

## ​Visitors

 The visitors tab displays a bar chart of visitors over time, a list of popular pages, and a list of referrers. Review your visitors analytics to:

- **Monitor traffic trends**: Observe changes in traffic after updates or new content to understand the impact of your changes.
- **Identify popular pages**: Use popular pages to understand what content is most important to your users so that you can make sure it is up to date and comprehensive.
- **Track traffic sources**: Understand where your users are coming from to help you optimize your content for the right audience.

## ​Assistant

 The assistant tab displays a bar chart of assistant usage over time, a list of categories, and chat history. Review your assistant analytics to:

- **Monitor assistant usage**: Observe changes in assistant usage to understand how your users engage with your content.
- **Identify frequent categories**: Use high occurrence categories to understand what topics are most important to your users. Identify gaps in coverage and prioritize content updates.
- **Review chat history**: Get detailed high intent data about how your users think about your product by reviewing their chat history with the assistant. See what terms they use, what they need help with, and what tasks they try to accomplish.

### ​Categories

 The categories tab uses LLMs to automatically group conversations by topic or theme. ![The categories tab in the assistant analytics page.](https://mintcdn.com/mintlify/2qBICQFhOKqkes42/images/analytics/categories-light.png?fit=max&auto=format&n=2qBICQFhOKqkes42&q=85&s=9ae65d0272876aa91853663e1a60ba48)![The categories tab in the assistant analytics page.](https://mintcdn.com/mintlify/2qBICQFhOKqkes42/images/analytics/categories-dark.png?fit=max&auto=format&n=2qBICQFhOKqkes42&q=85&s=b6fac616cac58577e7399b0abe83f956) Use categories to identify common topics, patterns in user needs and behavior, and areas where documentation might need expansion or clarification. Click a category row to expand it and view related conversations grouped under that category. Click an individual conversation to view the complete chat thread, including the user’s question, the assistant’s response, and any sources cited.

### ​Chat history

 The chat history tab displays chronological records of all assistant conversations. Click any message to view the complete chat thread, including the user’s question, the assistant’s response, and any sources cited.

### ​Export queries

 For deeper analysis, export a CSV file of your queries, responses, and sources. Use your preferred tools to analyze the exported data. Sample analysis prompts:

- List any queries that had no sources cited.
- Find patterns in unsuccessful interactions.

## ​Searches

 The searches tab displays a bar chart of searches over time and specific queries. Review your searches analytics to:

- **Monitor search trends**: Observe changes in search queries to understand how your users are finding your content and what topics they want information on.
- **Identify frequent queries**: Use frequent queries to understand what topics are most important to your users. Identify gaps in coverage and prioritize content updates.
- **Identify low click through rates**: Click through rates (CTR) show how many users click a search result after typing in a query. Low CTR can indicate that the search results are not relevant to users’ queries. If you have frequent search terms with low CTR, consider improving the relevance of search results by adding keywords and updating your content.

## ​Feedback

 The feedback tab displays a bar chart of feedback over time and specific feedback items. See [Feedback](https://mintlify.com/docs/optimize/feedback) for more information on using feedback data to improve your content.

---

# Feedback

> Monitor user satisfaction and feedback on your documentation.

To collect and view feedback, you must enable feedback from the [Add-ons](https://dashboard.mintlify.com/products/addons) page in your dashboard. The [feedback](https://dashboard.mintlify.com/products/analytics/v2/feedback) tab displays quantitative thumbs up and thumbs down votes your docs have received and any qualitative feedback that users have provided. Use this information to gauge the quality of your docs and make improvements. View feedback on the analytics page in your dashboard. ![Feedback tab in the Analytics page.](https://mintcdn.com/mintlify/4a6DEBu5ODMCZacH/images/analytics/feedback-light.png?fit=max&auto=format&n=4a6DEBu5ODMCZacH&q=85&s=f245fdfd424e3cdea5c2de192fd705a1)![Feedback tab in the Analytics page.](https://mintcdn.com/mintlify/4a6DEBu5ODMCZacH/images/analytics/feedback-dark.png?fit=max&auto=format&n=4a6DEBu5ODMCZacH&q=85&s=a53e71fd830d3f6c530753cfec2f0930)

## ​Feedback types

 Contextual and code snippet feedback are in beta. To enable them for your documentation site, [contact our sales team](https://mintlify.com/cdn-cgi/l/email-protection#472f262f29252222072a2e29332b2e213e6924282a). The feedback tab displays information according to the [feedback add-ons](https://dashboard.mintlify.com/products/addons) that you enable. ![Feedback toggles in the Add-ons page.](https://mintcdn.com/mintlify/HLPaFoXqJBOwTqBr/images/analytics/feedback-addons-light.png?fit=max&auto=format&n=HLPaFoXqJBOwTqBr&q=85&s=ff03c179eaddde9d4beaa34ad4442ed4)![Feedback toggles in the Add-ons page.](https://mintcdn.com/mintlify/HLPaFoXqJBOwTqBr/images/analytics/feedback-addons-dark.png?fit=max&auto=format&n=HLPaFoXqJBOwTqBr&q=85&s=56aba5d2a5f86e89d857246d381c989c)

- **Thumbs rating**: Simple thumbs up/down voting to gauge overall satisfaction with pages.
- **Contextual feedback**: Free form feedback about the content of a page.
- **Code snippet feedback**: Feedback specifically on code snippets.

 If you disable telemetry in your `docs.json` file, feedback features are not available on your documentation pages.

## ​Manage feedback

 For contextual and code snippet feedback, you can set the status of a piece of feedback and add internal notes to track your work resolving user feedback.

### ​Change feedback status

 Select the status beside a piece of feedback to mark it as **Pending**, **In Progress**, **Resolved**, or **Dismissed**. Best practices for setting feedback statuses:

- **Pending**: Feedback is awaiting review.
- **In Progress**: Feedback has been validated and is being worked on.
- **Resolved**: Feedback has been resolved.
- **Dismissed**: Feedback has been dismissed as not actionable, irrelevant, or inaccurate.

### ​Filter by status

 Use the status filter to control which feedback is displayed. Clear a status to hide all feedback with that status. By default, all feedback is displayed.

### ​Add internal notes

 Click a piece of feedback to add an internal note. These notes are only visible to people with access to your dashboard. Use notes to add information for collaboration, link relevant support or engineering tickets, or remember any other useful information.

## ​Use feedback data

 Review your feedback data to:

- **Identify successful content**: Pages with the most positive feedback show what works well in your documentation.
- **Prioritize improvements**: Pages with the most negative feedback indicate what content might need attention.
- **Take action**: Make documentation updates based on direct user feedback.

---

# PDF exports

> Export your documentation as a single PDF file.

PDF exports are available on [Custom plans](https://mintlify.com/pricing). You can export your docs as a single PDF file for offline viewing. The PDF will contain all the content in the docs, including images and links, and a navigable table of contents.

## ​Exporting a PDF

1. Navigate to the [General](https://dashboard.mintlify.com/settings/deployment/general) page in the Project Settings section of your dashboard.
2. Select the **Export all content** button.
3. Optionally, customize the export options:
  - **Page format**: Choose the page size of the PDF.
  - **Scale percentage**: Adjust the scale of the PDF.
  - **Include footer**: Include a footer with the page number and total pages.
4. Select **Export** to start the export process.
5. Once the export is complete, you will receive an email with a download link.
6. Click the download link to download the PDF file.

 [View Example PDF](https://mintlify.com/docs/files/mint-full-docs.pdf)

---

# SEO

> Optimize SEO with meta tag configuration for better search visibility.

Mintlify automatically handles many SEO best practices, including:

- Meta tag generation
- Sitemap and `robots.txt` file generation
- Semantic HTML structure
- Mobile optimization

 You can fully customize your site’s meta tags by adding the `metatags` field to your `docs.json` or a page’s frontmatter.

## ​Automatically generated meta tags

 Mintlify generates the following meta tags for every page. You can override these meta tags by specifying them in your `docs.json` or a page’s frontmatter. **Basic metadata:**

- `charset: utf-8` - Character encoding
- `og:type: website` - Open Graph type
- `og:site_name` - Your documentation site name
- `twitter:card: summary_large_image` - Twitter card type

 **Page-specific metadata:**

- `title` - Page title, formatted as “Page Title - Site Name”
- `og:title` - Open Graph title, same as page title
- `twitter:title` - Twitter title, same as page title
- `description` - Page description
- `og:description` - Open Graph description, same as page description
- `twitter:description` - Twitter description, same as page description

 **URL and canonical:**

- `canonical` - Automatically built from page URL
- `og:url` - Set to canonical URL

 **SEO and indexing:**

- `robots` - Generated from page metadata
- `noindex` - Generated from page metadata
- `keywords` - Generated from page metadata

 **Images:**

- `og:image` - Open Graph image, `og:image:width` set to 1200 and `og:image:height` 630
- `twitter:image` - Twitter image, `twitter:image:width` set to 1200 and `twitter:image:height` 630

 **Browser and app metadata:**

- `applicationName` - Your documentation site name
- `generator: Mintlify` - Identifies the site generator as Mintlify
- `apple-mobile-web-app-title` - iOS home screen app name
- `msapplication-TileColor` - Windows tile color
- Favicons and icons from your config
- Sitemap reference link

 Any meta tags in your `docs.json` `seo.metatags` configuration are also automatically injected into every page, such as `google-site-verification` for search console validation.

## ​Global meta tags

 To set default meta tags for all pages, add the `metatags` field to your `docs.json`.

```
"seo": {
    "metatags": {
        "og:image": "link to your default meta tag image"
    }
}
```

### ​Set a canonical URL

 If you’re using a custom domain, set the `canonical` meta tag to ensure search engines index your preferred domain. A canonical URL tells search engines which version of your documentation is the primary one. This improves SEO when your documentation is accessible from multiple URLs and prevents issues with duplicate content.

```
"seo": {
    "metatags": {
        "canonical": "https://www.your-custom-domain-here.com"
    }
}
```

## ​Page-specific meta tags

 To set page-specific meta tags, add them to a page’s frontmatter. The following meta tags are supported at the page level:

- `title` - Page title
- `description` - Page description appears below the title on the page and in some search engine results
- `keywords` - Comma-separated keywords
- `og:title` - Open Graph title for social sharing
- `og:description` - Open Graph description
- `og:image` - Open Graph image URL
- `og:url` - Open Graph URL
- `og:type` - Open Graph type like “article” or “website”
- `og:image:width` - Open Graph image width
- `og:image:height` - Open Graph image height
- `twitter:title` - Twitter card title
- `twitter:description` - Twitter card description
- `twitter:image` - Twitter card image
- `twitter:card` - Twitter card type like “summary” or “summary_large_image”
- `twitter:site` - Twitter site handle
- `twitter:image:width` - Twitter image width
- `twitter:image:height` - Twitter image height
- `noindex` - Set to `true` to prevent search engine indexing
- `robots` - Robots meta tag value

```
---
title: "Your example page title"
description: "Page-specific description"
"og:image": "link to your meta tag image"
"og:title": "Social media title"
keywords: ["keyword1", "keyword2"]
---
```

 Meta tags with colons must be wrapped in quotes. The `keywords` field must be formatted as a YAML array.

## ​Common meta tags reference

 Below is a comprehensive list of meta tags you can add to your `docs.json`. These meta tags help improve your site’s SEO, social sharing, and browser compatibility. The `og:image` adds a background image that Mintlify automatically overlays with your logo, page title, and description when generating social media previews. You can preview how your meta tags will appear on different platforms using [metatags.io](https://metatags.io/).

```
"seo": {
    "metatags": {
      "robots": "noindex",
      "charset": "UTF-8",
      "viewport": "width=device-width, initial-scale=1.0",
      "description": "Page description",
      "keywords": "keyword1, keyword2, keyword3",
      "author": "Author Name",
      "robots": "index, follow",
      "googlebot": "index, follow",
      "google": "notranslate",
      "google-site-verification": "verification_token",
      "generator": "Mintlify",
      "theme-color": "#000000",
      "color-scheme": "light dark",
      "canonical": "https://your-custom-domain-here.com",
      "format-detection": "telephone=no",
      "referrer": "origin",
      "refresh": "30",
      "rating": "general",
      "revisit-after": "7 days",
      "language": "en",
      "copyright": "Copyright 2024",
      "reply-to": "email@example.com",
      "distribution": "global",
      "coverage": "Worldwide",
      "category": "Technology",
      "target": "all",
      "HandheldFriendly": "True",
      "MobileOptimized": "320",
      "apple-mobile-web-app-capable": "yes",
      "apple-mobile-web-app-status-bar-style": "black",
      "apple-mobile-web-app-title": "App Title",
      "application-name": "App Name",
      "msapplication-TileColor": "#000000",
      "msapplication-TileImage": "path/to/tile.png",
      "msapplication-config": "path/to/browserconfig.xml",
      "og:title": "Open Graph Title",
      "og:type": "website",
      "og:url": "https://example.com",
      "og:image": "https://example.com/image.jpg",
      "og:description": "Open Graph Description",
      "og:site_name": "Site Name",
      "og:locale": "en_US",
      "og:video": "https://example.com/video.mp4",
      "og:audio": "https://example.com/audio.mp3",
      "twitter:card": "summary",
      "twitter:site": "@username",
      "twitter:creator": "@username",
      "twitter:title": "Twitter Title",
      "twitter:description": "Twitter Description",
      "twitter:image": "https://example.com/image.jpg",
      "twitter:image:alt": "Image Description",
      "twitter:player": "https://example.com/player",
      "twitter:player:width": "480",
      "twitter:player:height": "480",
      "twitter:app:name:iphone": "App Name",
      "twitter:app:id:iphone": "12345",
      "twitter:app:url:iphone": "app://",
      "article:published_time": "2024-01-01T00:00:00+00:00",
      "article:modified_time": "2024-01-02T00:00:00+00:00",
      "article:expiration_time": "2024-12-31T00:00:00+00:00",
      "article:author": "Author Name",
      "article:section": "Technology",
      "article:tag": "tag1, tag2, tag3",
      "book:author": "Author Name",
      "book:isbn": "1234567890",
      "book:release_date": "2024-01-01",
      "book:tag": "tag1, tag2, tag3",
      "profile:first_name": "John",
      "profile:last_name": "Doe",
      "profile:username": "johndoe",
      "profile:gender": "male",
      "music:duration": "205",
      "music:album": "Album Name",
      "music:album:disc": "1",
      "music:album:track": "1",
      "music:musician": "Artist Name",
      "music:song": "Song Name",
      "music:song:disc": "1",
      "music:song:track": "1",
      "video:actor": "Actor Name",
      "video:actor:role": "Role Name",
      "video:director": "Director Name",
      "video:writer": "Writer Name",
      "video:duration": "120",
      "video:release_date": "2024-01-01",
      "video:tag": "tag1, tag2, tag3",
      "video:series": "Series Name"
  }
}
```

## ​Sitemaps and robots.txt files

 Mintlify automatically generates a `sitemap.xml` file and a `robots.txt` file. You can view your sitemap by appending `/sitemap.xml` to your documentation site’s URL. Only pages included in your `docs.json` are included by default. To include hidden links, add `seo.indexing` to your `docs.json`:

```
"seo": {
    "indexing": "all"
}
```

### ​Custom sitemaps and robots.txt files

 To add a custom `sitemap.xml` or `robots.txt` file, create a `sitemap.xml` or `robots.txt` file at the root of your project. Adding a custom file will override the automatically generated file of the same name. If you delete a custom file, the default file will be used again.

## ​Disabling indexing

 If you want to stop a page from being indexed by search engines, you can include the following in the [frontmatter](https://mintlify.com/docs/organize/pages) of your page:

```
---
noindex: true
---
```

 You can also specify `noindex` for all pages in your docs by setting the `metatags.robots` field to `"noindex"` in your `docs.json`:

```
"seo": {
    "metatags": {
      "robots": "noindex"
    }
  }
```

## ​SEO best practices

Write descriptive titles and descriptions

- Use clear, descriptive page titles (50-60 characters)
- Write compelling descriptions (150-160 characters)
- Include relevant keywords
- Make each page title and description unique

Optimize your content structure

- Use proper heading hierarchy (H1 → H2 → H3)
- Write for humans first, search engines second
- Include relevant keywords in headings and content
- Keep URLs short, descriptive, and organized hierarchically
- Break up long content with subheadings and lists

Internal linking strategy

- Link to related pages within your documentation
- Use descriptive anchor text instead of “click here”
- Create topic clusters by linking related concepts
- Use the automatic cross-referencing features

Image SEO

- Use descriptive file names for images
- Always include alt text for accessibility and SEO
- Optimize image file sizes for faster loading
- Use relevant images that support your content
