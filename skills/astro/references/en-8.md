# ButterCMS & Astro and more

# ButterCMS & Astro

> Add content to your Astro project using ButterCMS

# ButterCMS & Astro

[ButterCMS](https://buttercms.com/) is a headless CMS and blog engine that allows you to publish structured content to use in your project.

## Integrating with Astro

[Section titled “Integrating with Astro”](#integrating-with-astro)

In this section, we’ll use the [ButterCMS SDK](https://www.npmjs.com/package/buttercms) to bring your data into your Astro project.
To get started, you will need to have the following:

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

1. **An Astro project** - If you don’t have an Astro project yet, our [Installation guide](https://docs.astro.build/en/install-and-setup/) will get you up and running in no time.
2. **A ButterCMS account**. If you don’t have an account, you can [sign up](https://buttercms.com/join/) for a free trial.
3. **Your ButterCMS API Token** - You can find your API Token on the [Settings](https://buttercms.com/settings/) page.

### Setup

[Section titled “Setup”](#setup)

1. Create a `.env` file in the root of your project and add your API token as an environment variable:
   .env
  ```
  BUTTER_TOKEN=YOUR_API_TOKEN_HERE
  ```
2. Install the ButterCMS SDK as a dependency:
  - [npm](#tab-panel-2750)
  - [pnpm](#tab-panel-2751)
  - [Yarn](#tab-panel-2752)
     Terminal window
  ```
  npm install buttercms
  ```
     Terminal window
  ```
  pnpm add buttercms
  ```
     Terminal window
  ```
  yarn add buttercms
  ```
3. Create a `buttercms.js` file in a new `src/lib/` directory in your project:
   src/lib/buttercms.js
  ```
  import Butter from "buttercms";
  export const butterClient = Butter(import.meta.env.BUTTER_TOKEN);
  ```

**This authenticates the SDK using your API Token and exports it to be used across your project.**

### Fetching Data

[Section titled “Fetching Data”](#fetching-data)

To fetch content, import this client and use one of its `retrieve` functions.

In this example, we [retrieve a collection](https://buttercms.com/docs/api/#retrieve-a-collection) that has three fields: a short text `name`, a number `price`, and a WYSIWYG `description`.

 src/pages/ShopItem.astro

```
---import { butterClient } from "../lib/buttercms";const response = await butterClient.content.retrieve(["shopitem"]);
interface ShopItem {  name: string,  price: number,  description: string,}
const items = response.data.data.shopitem as ShopItem[];---<body>  {items.map(item => <div>    <h2>{item.name} - ${item.price}</h2>    <p set:html={item.description}></p>  </div>)}</body>
```

The interface mirrors the field types. The WYSIWYG `description` field loads as a string of HTML, and [set:html](https://docs.astro.build/en/reference/directives-reference/#sethtml) lets you render it.

Similarly, you can [retrieve a page](https://buttercms.com/docs/api/#get-a-single-page) and display its fields:

 src/pages/ShopItem.astro

```
---import { butterClient } from "../lib/buttercms";const response = await butterClient.page.retrieve("*", "simple-page");const pageData = response.data.data;
interface Fields {  seo_title: string,  headline: string,  hero_image: string,}
const fields = pageData.fields as Fields;---<html>  <title>{fields.seo_title}</title>  <body>    <h1>{fields.headline}</h1>    <img src={fields.hero_image} />  </body></html>
```

## Official Resources

[Section titled “Official Resources”](#official-resources)

- [Astro + ButterCMS Starter Project](https://buttercms.com/starters/astro-starter-project/)
- The [full ButterCMS API documentation](https://buttercms.com/docs/api/)
- ButterCMS’s [JavaScript Guide](https://buttercms.com/docs/api-client/javascript/)

## Community Resources

[Section titled “Community Resources”](#community-resources)

- Add yours!

## More CMS guides

- ![](https://docs.astro.build/logos/apostrophecms.svg)
  ### ApostropheCMS
- ![](https://docs.astro.build/logos/builderio.svg)
  ### Builder.io
- ![](https://docs.astro.build/logos/buttercms.svg)
  ### ButterCMS
- ![](https://docs.astro.build/logos/caisy.svg)
  ### Caisy
- ![](https://docs.astro.build/logos/cloudcannon.svg)
  ### CloudCannon
- ![](https://docs.astro.build/logos/contentful.svg)
  ### Contentful
- ![](https://docs.astro.build/logos/cosmic.svg)
  ### Cosmic
- ![](https://docs.astro.build/logos/craft-cms.svg)
  ### Craft CMS
- ![](https://docs.astro.build/logos/craft-cross-cms.svg)
  ### Craft Cross CMS
- ![](https://docs.astro.build/logos/crystallize.svg)
  ### Crystallize
- ![](https://docs.astro.build/logos/datocms.svg)
  ### DatoCMS
- ![](https://docs.astro.build/logos/decap-cms.svg)
  ### Decap CMS
- ![](https://docs.astro.build/logos/directus.svg)
  ### Directus
- ![](https://docs.astro.build/logos/drupal.svg)
  ### Drupal
- ![](https://docs.astro.build/logos/flotiq.svg)
  ### Flotiq
- ![](https://docs.astro.build/logos/frontmatter-cms.svg)
  ### Front Matter CMS
- ![](https://docs.astro.build/logos/ghost.png)
  ### Ghost
- ![](https://docs.astro.build/logos/gitcms.svg)
  ### GitCMS
- ![](https://docs.astro.build/logos/hashnode.png)
  ### Hashnode
- ![](https://docs.astro.build/logos/hygraph.svg)
  ### Hygraph
- ![](https://docs.astro.build/logos/jekyllpad.svg)
  ### JekyllPad
- ![](https://docs.astro.build/logos/keystatic.svg)
  ### Keystatic
- ![](https://docs.astro.build/logos/keystonejs.svg)
  ### KeystoneJS
- ![](https://docs.astro.build/logos/kontent-ai.svg)
  ### Kontent.ai
- ![](https://docs.astro.build/logos/microcms.svg)
  ### microCMS
- ![](https://docs.astro.build/logos/optimizely.svg)
  ### Optimizely CMS
- ![](https://docs.astro.build/logos/payload.svg)
  ### Payload CMS
- ![](https://docs.astro.build/logos/preprcms.svg)
  ### Prepr CMS
- ![](https://docs.astro.build/logos/prismic.svg)
  ### Prismic
- ![](https://docs.astro.build/logos/sanity.svg)
  ### Sanity
- ![](https://docs.astro.build/logos/sitecore.svg)
  ### Sitecore XM
- ![](https://docs.astro.build/logos/sitepins.svg)
  ### Sitepins
- ![](https://docs.astro.build/logos/spinal.svg)
  ### Spinal
- ![](https://docs.astro.build/logos/statamic.svg)
  ### Statamic
- ![](https://docs.astro.build/logos/storyblok.svg)
  ### Storyblok
- ![](https://docs.astro.build/logos/strapi.svg)
  ### Strapi
- ![](https://docs.astro.build/logos/studiocms.svg)
  ### StudioCMS
- ![](https://docs.astro.build/logos/tina-cms.svg)
  ### Tina CMS
- ![](https://docs.astro.build/logos/umbraco.svg)
  ### Umbraco
- ![](https://docs.astro.build/logos/wordpress.svg)
  ### Wordpress

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Caisy & Astro

> Add content to your Astro project using Caisy as a CMS

# Caisy & Astro

[Caisy](https://caisy.io/) is a headless CMS that exposes a GraphQL API to access content.

## Using Caisy CMS with Astro

[Section titled “Using Caisy CMS with Astro”](#using-caisy-cms-with-astro)

Use `graphql-request` and Caisy’s rich text renderer for Astro to fetch your CMS data and display your content on an Astro page:

 src/pages/blog/[...slug].astro

```
---import RichTextRenderer from '@caisy/rich-text-astro-renderer';import { gql, GraphQLClient } from 'graphql-request';
const params = Astro.params;
const client = new GraphQLClient(  `https://cloud.caisy.io/api/v3/e/${import.meta.env.CAISY_PROJECT_ID}/graphql`,  {    headers: {      'x-caisy-apikey': import.meta.env.CAISY_API_KEY    }  });const gqlResponse = await client.request(  gql`    query allBlogArticle($slug: String) {      allBlogArticle(where: { slug: { eq: $slug } }) {        edges {          node {            text {              json            }            title            slug            id          }        }      }    }  `,  { slug: params.slug });
const post = gqlResponse?.allBlogArticle?.edges?.[0]?.node;---<h1>{post.title}</h1><RichTextRenderer node={post.text.json} />
```

## Official Resources

[Section titled “Official Resources”](#official-resources)

- Check out the Caisy + Astro example on [GitHub](https://github.com/caisy-io/caisy-example-astro) or [StackBlitz](https://stackblitz.com/github/caisy-io/caisy-example-astro?file=src%2Fpages%2Fblog%2F%5B...slug%5D.astro)
- Query your documents in [draft mode](https://caisy.io/developer/docs/external-api/localization-and-preview#preview-mode-15) and multiple [locales](https://caisy.io/developer/docs/external-api/localization-and-preview#localization-in-a-graphql-query-8).
- Use [pagination](https://caisy.io/developer/docs/external-api/queries-pagination) to query large numbers of documents.
- Use [filter](https://caisy.io/developer/docs/external-api/external-filter-and-sorting) in your queries and [order](https://caisy.io/developer/docs/external-api/external-filter-and-sorting#sorting-8) the results

## More CMS guides

- ![](https://docs.astro.build/logos/apostrophecms.svg)
  ### ApostropheCMS
- ![](https://docs.astro.build/logos/builderio.svg)
  ### Builder.io
- ![](https://docs.astro.build/logos/buttercms.svg)
  ### ButterCMS
- ![](https://docs.astro.build/logos/caisy.svg)
  ### Caisy
- ![](https://docs.astro.build/logos/cloudcannon.svg)
  ### CloudCannon
- ![](https://docs.astro.build/logos/contentful.svg)
  ### Contentful
- ![](https://docs.astro.build/logos/cosmic.svg)
  ### Cosmic
- ![](https://docs.astro.build/logos/craft-cms.svg)
  ### Craft CMS
- ![](https://docs.astro.build/logos/craft-cross-cms.svg)
  ### Craft Cross CMS
- ![](https://docs.astro.build/logos/crystallize.svg)
  ### Crystallize
- ![](https://docs.astro.build/logos/datocms.svg)
  ### DatoCMS
- ![](https://docs.astro.build/logos/decap-cms.svg)
  ### Decap CMS
- ![](https://docs.astro.build/logos/directus.svg)
  ### Directus
- ![](https://docs.astro.build/logos/drupal.svg)
  ### Drupal
- ![](https://docs.astro.build/logos/flotiq.svg)
  ### Flotiq
- ![](https://docs.astro.build/logos/frontmatter-cms.svg)
  ### Front Matter CMS
- ![](https://docs.astro.build/logos/ghost.png)
  ### Ghost
- ![](https://docs.astro.build/logos/gitcms.svg)
  ### GitCMS
- ![](https://docs.astro.build/logos/hashnode.png)
  ### Hashnode
- ![](https://docs.astro.build/logos/hygraph.svg)
  ### Hygraph
- ![](https://docs.astro.build/logos/jekyllpad.svg)
  ### JekyllPad
- ![](https://docs.astro.build/logos/keystatic.svg)
  ### Keystatic
- ![](https://docs.astro.build/logos/keystonejs.svg)
  ### KeystoneJS
- ![](https://docs.astro.build/logos/kontent-ai.svg)
  ### Kontent.ai
- ![](https://docs.astro.build/logos/microcms.svg)
  ### microCMS
- ![](https://docs.astro.build/logos/optimizely.svg)
  ### Optimizely CMS
- ![](https://docs.astro.build/logos/payload.svg)
  ### Payload CMS
- ![](https://docs.astro.build/logos/preprcms.svg)
  ### Prepr CMS
- ![](https://docs.astro.build/logos/prismic.svg)
  ### Prismic
- ![](https://docs.astro.build/logos/sanity.svg)
  ### Sanity
- ![](https://docs.astro.build/logos/sitecore.svg)
  ### Sitecore XM
- ![](https://docs.astro.build/logos/sitepins.svg)
  ### Sitepins
- ![](https://docs.astro.build/logos/spinal.svg)
  ### Spinal
- ![](https://docs.astro.build/logos/statamic.svg)
  ### Statamic
- ![](https://docs.astro.build/logos/storyblok.svg)
  ### Storyblok
- ![](https://docs.astro.build/logos/strapi.svg)
  ### Strapi
- ![](https://docs.astro.build/logos/studiocms.svg)
  ### StudioCMS
- ![](https://docs.astro.build/logos/tina-cms.svg)
  ### Tina CMS
- ![](https://docs.astro.build/logos/umbraco.svg)
  ### Umbraco
- ![](https://docs.astro.build/logos/wordpress.svg)
  ### Wordpress

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# CloudCannon & Astro

> Add content to your Astro project using CloudCannon as a CMS

# CloudCannon & Astro

[CloudCannon](https://cloudcannon.com) is a Git-based headless content management system that provides a visual editor for your content and UI components, providing a rich, live editing experience.

## Integrating with Astro

[Section titled “Integrating with Astro”](#integrating-with-astro)

This guide will describe the process of configuring CloudCannon as a CMS for Astro using the CloudCannon Site Dashboard.

The Site Dashboard provides you with an organized view of your Astro files and the ability to edit them using:

- A [Data Editor](https://cloudcannon.com/documentation/articles/the-data-editor/) for managing structured data files and markup.
- A [Content Editor](https://cloudcannon.com/documentation/articles/the-content-editor/) for WYSIWYG rich text editing in a minimal view.
- A [Visual Editor](https://cloudcannon.com/documentation/articles/the-visual-editor/) for an interactive preview of your site, allowing you to edit directly on the page.

You can also configure role-based access to a minimal [Source Editor](https://cloudcannon.com/documentation/articles/the-source-editor/), an in-browser code editor for making minor changes to the source code of your files.

## Prerequisites

[Section titled “Prerequisites”](#prerequisites)

1. A CloudCannon account. If you don’t have an account, you can [sign up with CloudCannon](https://app.cloudcannon.com/register).
2. An existing Astro project stored locally, or on one of CloudCannon’s supported Git providers: GitHub, GitLab, or Bitbucket. If you do not have an existing project, you can start with CloudCannon’s [Astro Starter Template](https://cloudcannon.com/templates/astro-starter/).

## Configure a new CloudCannon Site

[Section titled “Configure a new CloudCannon Site”](#configure-a-new-cloudcannon-site)

The following steps will configure a new CloudCannon Site from your dashboard. This Site will connect to an existing Astro repository and allow you to manage and edit your content with CloudCannon’s WYSIWYG text editor.

1. In your CloudCannon Organization Home page, create a new Site.
2. Authenticate your Git provider and select the Astro repository you want to connect to.
3. Choose a name for your Site, then CloudCannon will create the Site and start syncing your files.
4. Follow CloudCannon’s guided tasks in your Site dashboard for completing your Site setup, including creating a CloudCannon configuration file (`cloudcannnon.config.yml`)
5. Save your configuration file to commit it with your CloudCannon preferences to your Git repository.

You can now explore your Site Dashboard to see your Astro files and edit them with the Content Editor.

You may also want to take advantage of some CloudCannon features, such as [organizing your files into collections](#cloudcannon-collections-and-schemas), [creating CloudCannon schemas](#create-a-cloudcannon-schema-for-a-collection), and setting up your project for [visual editing](#configure-visual-editing).

For more detailed instructions, see [CloudCannon’s Getting Started Guide](https://cloudcannon.com/documentation/guides/getting-started-with-cloudcannon/).

## CloudCannon collections and schemas

[Section titled “CloudCannon collections and schemas”](#cloudcannon-collections-and-schemas)

If you use [Astro’s content collections](https://docs.astro.build/en/guides/content-collections/), then you will be familiar with CloudCannon’s concepts of collections (used for organization/navigation in your Site Dashboard) and schemas (used to define the format of new content entries).

Your CloudCannon Site Dashboard allows you to organize your Astro project’s pages and content into collections: groups of related files with a similar format. This allows you to see similar types of content together for ease of editing and makes your content files easy to navigate, sort, and filter.

### Create a CloudCannon schema for a collection

[Section titled “Create a CloudCannon schema for a collection”](#create-a-cloudcannon-schema-for-a-collection)

To ensure that the data properties of your CloudCannon entries match the Zod validation `schema` defined in your content collection, you can create a [CloudCannon schema](https://cloudcannon.com/documentation/articles/what-is-a-schema/) (a blank template document for creating a new entry). Creating a template schema can ensure that any new documents created in CloudCannon will have the properties required by your content collection and avoid type errors in your project. Your CloudCannon schema can also include default values to start new documents, such as an author name for a single-person blog.

The following example will create a CloudCannon schema based on an Astro content collection (`blog`) for blog posts written in Markdown. This schema will be available when [creating a new entry](#creating-a-new-entry) from the CloudCannon “Posts” collection:

1. Create a folder at `.cloudcannon/schemas/` if it does not already exist.
2. Add an existing blank file in this folder to be used as a default blog post template. The name is unimportant, but the file must have the same file extension as your Astro content collection entries (e.g. `post.md`).
3. Provide the necessary frontmatter fields required by your content collection’s schema. You do not need to provide any values for these, but any content you do include will be automatically included when a new entry is created. These are fields that will be available in the sidebar of your Content Editor.
  The following example schema for a blog post has placeholders for the title, author, and date:
   .cloudcannon/schemas/post.md
  ```
  ---title:author:date:---
  ```
4. In your CloudCannon configuration file’s `collections_config` property, add the file path to your schema under the CloudCannon collection under the “Posts” collection.
   cloudcannon.config.yml
  ```
  collections_config:  posts:    path: content/blog    name: Posts    icon: post_add    schemas:      default:        path: .cloudcannon/schemas/post.md        name: Blog Post Entry
  ```

## Creating a new entry

[Section titled “Creating a new entry”](#creating-a-new-entry)

In your CloudCannon Site Dashboard, you can create new content using the “Add” button. You will be able to select an entry type from the schemas you have defined in `cloudcannon.config.yml`, depending on which collection you are currently in.

You can also upload files to CloudCannon, or create new files directly in your Astro project. When you save your Site changes, new files created in either location will be synchronized and available in both CloudCannon and your Astro project.

The following example will create a new blog post from the CloudCannon Site Dashboard “Posts” collection using the `post.md` template schema created to satisfy the `blog` Astro content collection:

1. In the CloudCannon Site Dashboard, navigate to the collection representing the kind of content you want to add. For example, navigate to the “Posts” collection to add a new blog post.
2. Use the “Add” button to create a new post. If you have configured CloudCannon’s `post.md` schema, then you can choose the default blog post entry to create a new post.
3. Fill the necessary fields in the sidebar of your Content Editor (e.g. `title`, `author`, `date`), and post content and save your post.
4. This post is saved locally in CloudCannon and should now be visible from your Site Dashboard in your “Posts” collection. You can view and edit all your individual posts from this dashboard page.
5. When you are ready to commit this new post back to your Astro repository, select “Save” in the Site navigation sidebar from your Site Dashboard. This will show you all unsaved changes made to your site since your last commit back to your repository and allow you to review and select which ones to save or discard.
6. Return to view your Astro project files and pull new changes from git. You will now find a new `.md` file inside the specified directory for this new post, for example:
  - Directorysrc/
    - Directorycontent/
      - Directoryblog/
        - **my-new-post.md**
7. Navigate to that file in your code editor and verify that you can see the Markdown content you entered. For example:
  ```
  ---title: My New Postauthor: Sarahdate: 2025-11-12---
  This is my very first post created in CloudCannon. I am **super** excited!
  ```

## Rendering CloudCannon content

[Section titled “Rendering CloudCannon content”](#rendering-cloudcannon-content)

Use Astro’s Content Collections API to [query and display your posts and collections](https://docs.astro.build/en/guides/content-collections/#querying-collections), just as you would in any Astro project.

### Displaying a collection list

[Section titled “Displaying a collection list”](#displaying-a-collection-list)

The following example displays a list of each post title, with a link to an individual post page.

 src/pages/blog.astro

```
---import { getCollection } from 'astro:content';
const posts = await getCollection('blog');---<ul>  {posts.map(post => (    <li>      <a href={`/posts/${post.slug}`}>{post.data.title}</a>    </li>  ))}</ul>
```

### Displaying a single entry

[Section titled “Displaying a single entry”](#displaying-a-single-entry)

To display content from an individual post, you can import and use the `<Content />` component to [render your content to HTML](https://docs.astro.build/en/guides/content-collections/#rendering-body-content):

 src/pages/blog/my-first-post.astro

```
---import { getEntry, render } from 'astro:content';
const entry = await getEntry('blog', 'my-first-post');const { Content } = await render(entry);---
<main>  <h1>{entry.data.title}</h1>  <p>By: {entry.data.author}</p>  <Content /></main>
```

For more information on querying, filtering, displaying your collections content, and more, see the full content [collections documentation](https://docs.astro.build/en/guides/content-collections/).

## Deploying CloudCannon + Astro

[Section titled “Deploying CloudCannon + Astro”](#deploying-cloudcannon--astro)

To deploy your website, visit our [deployment guides](https://docs.astro.build/en/guides/deploy/) and follow the instructions for your preferred hosting provider.

## Configure Visual Editing

[Section titled “Configure Visual Editing”](#configure-visual-editing)

CloudCannon’s [Visual Editor](https://cloudcannon.com/documentation/articles/the-visual-editor/) allows you to see and edit text, images, and other content in a live, interactive preview of your site. These updates can be made using editable regions, data panels, and the sidebar.

Follow [CloudCannon’s guide to set up visual editing](https://cloudcannon.com/documentation/guides/set-up-visual-editing/) (also available in your Site Dashboard). This will show you how to define [editable regions](https://cloudcannon.com/documentation/guides/set-up-visual-editing/an-overview-of-editable-regions/) of your live preview by setting HTML `data-` attributes on DOM elements, or by inserting web components.

For example, the following template creates an editable `author` value that can be updated in the live preview:

```
<p>By: <editable-text data-prop="author">{author}</editable-text></p>
```

### Visual Editing with components

[Section titled “Visual Editing with components”](#visual-editing-with-components)

CloudCannon allows you to [define Component Editable Regions](https://cloudcannon.com/documentation/guides/set-up-visual-editing/visual-editing-for-components/) for live re-rendering of Astro components in the Visual Editor. This gives you the same interactive editing experience for your Astro components.

1. Install the [@cloudcannon/editable-regions](https://github.com/CloudCannon/editable-regions) package.
  - [npm](#tab-panel-2753)
  - [pnpm](#tab-panel-2754)
  - [Yarn](#tab-panel-2755)
     Terminal window
  ```
  npm install @cloudcannon/editable-regions
  ```
     Terminal window
  ```
  pnpm add @cloudcannon/editable-regions
  ```
     Terminal window
  ```
  yarn add @cloudcannon/editable-regions
  ```
2. Add the `editableRegions` integration to your Astro config:
   astro.config.mjs
  ```
  import { defineConfig } from 'astro/config';import editableRegions from "@cloudcannon/editable-regions/astro-integration";
  export default defineConfig({  // ...  integrations: [editableRegions()],  // ...});
  ```
3. Follow [CloudCannon’s instructions to register your components](https://cloudcannon.com/documentation/guides/set-up-visual-editing/visual-editing-for-components/#register-your-components). This tells CloudCannon that those components should be bundled for client-side use in the Visual Editor.
4. Add the appropriate attributes to your components for visual editing. For example, the following `CTA.astro` component properties, such as description and button color, can be updated in CloudCannon’s Visual Editor:
   src/components/CTA.astro
  ```
  ---const { description, link, buttonText, buttonColor } = Astro.props;---
  <p data-editable="text" data-prop="description">{description}</p><a href={link}>    <span data-editable="text" data-prop="buttonText" style={`background-color: ${buttonColor}`}>{buttonText}</span></a>
  ```

## Official Resources

[Section titled “Official Resources”](#official-resources)

- [CloudCannon: The Astro CMS](https://cloudcannon.com/astro-cms/)
- [Astro Starter Template](https://cloudcannon.com/templates/astro-starter/)
- Video: [Getting started with Astro and CloudCannon CMS: WYSIWYG blogging](https://www.youtube.com/watch?v=VCbZV-SCr20)
- Blog: [How CloudCannon’s live editing works with Astro and Bookshop](https://cloudcannon.com/blog/how-cloudcannons-live-editing-works-with-astro-and-bookshop/)
- [Bookshop & Astro Guide](https://cloudcannon.com/documentation/guides/bookshop-astro-guide/)

## Community Resources

[Section titled “Community Resources”](#community-resources)

- Video: [Astro CMS for Visual Editing: Getting Started with CloudCannon](https://www.youtube.com/watch?v=YcH53e1YamE)

## More CMS guides

- ![](https://docs.astro.build/logos/apostrophecms.svg)
  ### ApostropheCMS
- ![](https://docs.astro.build/logos/builderio.svg)
  ### Builder.io
- ![](https://docs.astro.build/logos/buttercms.svg)
  ### ButterCMS
- ![](https://docs.astro.build/logos/caisy.svg)
  ### Caisy
- ![](https://docs.astro.build/logos/cloudcannon.svg)
  ### CloudCannon
- ![](https://docs.astro.build/logos/contentful.svg)
  ### Contentful
- ![](https://docs.astro.build/logos/cosmic.svg)
  ### Cosmic
- ![](https://docs.astro.build/logos/craft-cms.svg)
  ### Craft CMS
- ![](https://docs.astro.build/logos/craft-cross-cms.svg)
  ### Craft Cross CMS
- ![](https://docs.astro.build/logos/crystallize.svg)
  ### Crystallize
- ![](https://docs.astro.build/logos/datocms.svg)
  ### DatoCMS
- ![](https://docs.astro.build/logos/decap-cms.svg)
  ### Decap CMS
- ![](https://docs.astro.build/logos/directus.svg)
  ### Directus
- ![](https://docs.astro.build/logos/drupal.svg)
  ### Drupal
- ![](https://docs.astro.build/logos/flotiq.svg)
  ### Flotiq
- ![](https://docs.astro.build/logos/frontmatter-cms.svg)
  ### Front Matter CMS
- ![](https://docs.astro.build/logos/ghost.png)
  ### Ghost
- ![](https://docs.astro.build/logos/gitcms.svg)
  ### GitCMS
- ![](https://docs.astro.build/logos/hashnode.png)
  ### Hashnode
- ![](https://docs.astro.build/logos/hygraph.svg)
  ### Hygraph
- ![](https://docs.astro.build/logos/jekyllpad.svg)
  ### JekyllPad
- ![](https://docs.astro.build/logos/keystatic.svg)
  ### Keystatic
- ![](https://docs.astro.build/logos/keystonejs.svg)
  ### KeystoneJS
- ![](https://docs.astro.build/logos/kontent-ai.svg)
  ### Kontent.ai
- ![](https://docs.astro.build/logos/microcms.svg)
  ### microCMS
- ![](https://docs.astro.build/logos/optimizely.svg)
  ### Optimizely CMS
- ![](https://docs.astro.build/logos/payload.svg)
  ### Payload CMS
- ![](https://docs.astro.build/logos/preprcms.svg)
  ### Prepr CMS
- ![](https://docs.astro.build/logos/prismic.svg)
  ### Prismic
- ![](https://docs.astro.build/logos/sanity.svg)
  ### Sanity
- ![](https://docs.astro.build/logos/sitecore.svg)
  ### Sitecore XM
- ![](https://docs.astro.build/logos/sitepins.svg)
  ### Sitepins
- ![](https://docs.astro.build/logos/spinal.svg)
  ### Spinal
- ![](https://docs.astro.build/logos/statamic.svg)
  ### Statamic
- ![](https://docs.astro.build/logos/storyblok.svg)
  ### Storyblok
- ![](https://docs.astro.build/logos/strapi.svg)
  ### Strapi
- ![](https://docs.astro.build/logos/studiocms.svg)
  ### StudioCMS
- ![](https://docs.astro.build/logos/tina-cms.svg)
  ### Tina CMS
- ![](https://docs.astro.build/logos/umbraco.svg)
  ### Umbraco
- ![](https://docs.astro.build/logos/wordpress.svg)
  ### Wordpress

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Contentful & Astro

> Add content to your Astro project using Contentful as a CMS

# Contentful & Astro

[Contentful](https://www.contentful.com/) is a headless CMS that allows you to manage content, integrate with other services, and publish to multiple platforms.

## Integrating with Astro

[Section titled “Integrating with Astro”](#integrating-with-astro)

In this section, we’ll use the [Contentful SDK](https://github.com/contentful/contentful.js) to connect your Contentful space to Astro with zero client-side JavaScript.

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

To get started, you will need to have the following:

1. **An Astro project** - If you don’t have an Astro project yet, our [Installation guide](https://docs.astro.build/en/install-and-setup/) will get you up and running in no time.
2. **A Contentful account and a Contentful space**. If you don’t have an account, you can [sign up](https://www.contentful.com/sign-up/) for a free account and create a new Contentful space. You can also use an existing space if you have one.
3. **Contentful credentials** - You can find the following credentials in your Contentful dashboard **Settings > API keys**. If you don’t have any API keys, create one by selecting **Add API key**.
  - **Contentful space ID** - The ID of your Contentful space.
  - **Contentful delivery access token** - The access token to consume *published* content from your Contentful space.
  - **Contentful preview access token** - The access token to consume *unpublished* content from your Contentful space.

### Setting up credentials

[Section titled “Setting up credentials”](#setting-up-credentials)

To add your Contentful space’s credentials to Astro, create an `.env` file in the root of your project with the following variables:

 .env

```
CONTENTFUL_SPACE_ID=YOUR_SPACE_IDCONTENTFUL_DELIVERY_TOKEN=YOUR_DELIVERY_TOKENCONTENTFUL_PREVIEW_TOKEN=YOUR_PREVIEW_TOKEN
```

Now, you can use these environment variables in your project.

If you would like to have IntelliSense for your Contentful environment variables, you can create a `env.d.ts` file in the `src/` directory and configure `ImportMetaEnv` like this:

 src/env.d.ts

```
interface ImportMetaEnv {  readonly CONTENTFUL_SPACE_ID: string;  readonly CONTENTFUL_DELIVERY_TOKEN: string;  readonly CONTENTFUL_PREVIEW_TOKEN: string;}
```

Your root directory should now include these new files:

- Directorysrc/
  - **env.d.ts**
- **.env**
- astro.config.mjs
- package.json

### Installing dependencies

[Section titled “Installing dependencies”](#installing-dependencies)

To connect with your Contentful space, install both of the following using the single command below for your preferred package manager:

- [contentful.js](https://github.com/contentful/contentful.js), the official Contentful SDK for JavaScript
- [rich-text-html-renderer](https://github.com/contentful/rich-text/tree/master/packages/rich-text-html-renderer), a package to render Contentful’s rich text fields to HTML.

- [npm](#tab-panel-2756)
- [pnpm](#tab-panel-2757)
- [Yarn](#tab-panel-2758)

   Terminal window

```
npm install contentful @contentful/rich-text-html-renderer
```

   Terminal window

```
pnpm add contentful @contentful/rich-text-html-renderer
```

   Terminal window

```
yarn add contentful @contentful/rich-text-html-renderer
```

Next, create a new file called `contentful.ts` in the `src/lib/` directory of your project.

 src/lib/contentful.ts

```
import * as contentful from "contentful";
export const contentfulClient = contentful.createClient({  space: import.meta.env.CONTENTFUL_SPACE_ID,  accessToken: import.meta.env.DEV    ? import.meta.env.CONTENTFUL_PREVIEW_TOKEN    : import.meta.env.CONTENTFUL_DELIVERY_TOKEN,  host: import.meta.env.DEV ? "preview.contentful.com" : "cdn.contentful.com",});
```

The above code snippet creates a new Contentful client, passing in credentials from the `.env` file.

Finally, your root directory should now include these new files:

- Directorysrc/
  - env.d.ts
  - Directorylib/
    - **contentful.ts**
- .env
- astro.config.mjs
- package.json

### Fetching data

[Section titled “Fetching data”](#fetching-data)

Astro components can fetch data from your Contentful account by using the `contentfulClient` and specifying the `content_type`.

For example, if you have a “blogPost” content type that has a text field for a title and a rich text field for content, your component might look like this:

```
---import { contentfulClient } from "../lib/contentful";import { documentToHtmlString } from "@contentful/rich-text-html-renderer";import type { EntryFieldTypes } from "contentful";
interface BlogPost {  contentTypeId: "blogPost",  fields: {    title: EntryFieldTypes.Text    content: EntryFieldTypes.RichText,  }}
const entries = await contentfulClient.getEntries<BlogPost>({  content_type: "blogPost",});---<body>  {entries.items.map((item) => (    <section>      <h2>{item.fields.title}</h2>      <article set:html={documentToHtmlString(item.fields.content)}></article>    </section>  ))}</body>
```

You can find more querying options in the [Contentful documentation](https://contentful.github.io/contentful.js/).

## Making a blog with Astro and Contentful

[Section titled “Making a blog with Astro and Contentful”](#making-a-blog-with-astro-and-contentful)

With the setup above, you are now able to create a blog that uses Contentful as the CMS.

### Prerequisites

[Section titled “Prerequisites”](#prerequisites-1)

1. **A Contentful space** - For this tutorial we recommend starting with an empty space. If you already have a content model, feel free to use it, but you will need to modify our code snippets to match your content model.
2. **An Astro project integrated with theContentful SDK** - See [integrating with Astro](#integrating-with-astro) for more details on how to set up an Astro project with Contentful.

### Setting up a Contentful model

[Section titled “Setting up a Contentful model”](#setting-up-a-contentful-model)

Inside your Contentful space, in the **Content model** section, create a new content model with the following fields and values:

- **Name:** Blog Post
- **API identifier:** `blogPost`
- **Description:** This content type is for a blog post

In your newly created content type, use the **Add Field** button to add 5 new fields with the following parameters:

1. Text field
  - **Name:** title
  - **API identifier:** `title`
    (leave the other parameters as their defaults)
2. Date and time field
  - **Name:** date
  - **API identifier:** `date`
3. Text field
  - **Name:** slug
  - **API identifier:** `slug`
    (leave the other parameters as their defaults)
4. Text field
  - **Name:** description
  - **API identifier:** `description`
5. Rich text field
  - **Name:** content
  - **API identifier:** `content`

Click **Save** to save your changes.

In the **Content** section of your Contentful space, create a new entry by clicking the **Add Entry** button. Then, fill in the fields:

- **Title:** `Astro is amazing!`
- **Slug:** `astro-is-amazing`
- **Description:** `Astro is a new static site generator that is blazing fast and easy to use.`
- **Date:** `2022-10-05`
- **Content:** `This is my first blog post!`

Click **Publish** to save your entry. You have just created your first blog post.

Feel free to add as many blog posts as you want, then switch to your favorite code editor to start hacking with Astro!

### Displaying a list of blog posts

[Section titled “Displaying a list of blog posts”](#displaying-a-list-of-blog-posts)

Create a new interface called `BlogPost` and add it to your `contentful.ts` file in `src/lib/`. This interface will match the fields of your blog post content type in Contentful. You will use it to type your blog post entries response.

 src/lib/contentful.ts

```
import * as contentful from "contentful";import type { EntryFieldTypes } from "contentful";
export interface BlogPost {  contentTypeId: "blogPost",  fields: {    title: EntryFieldTypes.Text    content: EntryFieldTypes.RichText,    date: EntryFieldTypes.Date,    description: EntryFieldTypes.Text,    slug: EntryFieldTypes.Text  }}
export const contentfulClient = contentful.createClient({  space: import.meta.env.CONTENTFUL_SPACE_ID,  accessToken: import.meta.env.DEV    ? import.meta.env.CONTENTFUL_PREVIEW_TOKEN    : import.meta.env.CONTENTFUL_DELIVERY_TOKEN,  host: import.meta.env.DEV ? "preview.contentful.com" : "cdn.contentful.com",});
```

Next, go to the Astro page where you will fetch data from Contentful. We will use the home page `index.astro` in `src/pages/` in this example.

Import `BlogPost` interface and `contentfulClient` from `src/lib/contentful.ts`.

Fetch all the entries from Contentful with a content type of `blogPost` while passing the `BlogPost` interface to type your response.

 src/pages/index.astro

```
---import { contentfulClient } from "../lib/contentful";import type { BlogPost } from "../lib/contentful";
const entries = await contentfulClient.getEntries<BlogPost>({  content_type: "blogPost",});---
```

This fetch call will return an array of your blog posts at `entries.items`. You can use `map()` to create a new array (`posts`)  that formats your returned data.

The example below returns the `items.fields` properties from our Content model to create a blog post preview, and at the same time, reformats the date to a more readable format.

 src/pages/index.astro

```
---import { contentfulClient } from "../lib/contentful";import type { BlogPost } from "../lib/contentful";
const entries = await contentfulClient.getEntries<BlogPost>({  content_type: "blogPost",});
const posts = entries.items.map((item) => {  const { title, date, description, slug } = item.fields;  return {    title,    slug,    description,    date: new Date(date).toLocaleDateString()  };});---
```

Finally, you can use `posts` in your template to show a preview of each blog post.

 src/pages/index.astro

```
---import { contentfulClient } from "../lib/contentful";import type { BlogPost } from "../lib/contentful";
const entries = await contentfulClient.getEntries<BlogPost>({  content_type: "blogPost",});
const posts = entries.items.map((item) => {  const { title, date, description, slug } = item.fields;  return {    title,    slug,    description,    date: new Date(date).toLocaleDateString()  };});---<html lang="en">  <head>    <title>My Blog</title>  </head>  <body>    <h1>My Blog</h1>    <ul>      {posts.map((post) => (        <li>          <a href={`/posts/${post.slug}/`}>            <h2>{post.title}</h2>          </a>          <time>{post.date}</time>          <p>{post.description}</p>        </li>      ))}    </ul>  </body></html>
```

### Generating individual blog posts

[Section titled “Generating individual blog posts”](#generating-individual-blog-posts)

Use the same method to fetch your data from Contentful as above, but this time, on a page that will create a unique page route for each blog post.

#### Static site generation

[Section titled “Static site generation”](#static-site-generation)

If you’re using Astro’s default static mode, you’ll use [dynamic routes](https://docs.astro.build/en/guides/routing/#dynamic-routes) and the `getStaticPaths()` function. This function will be called at build time to generate the list of paths that become pages.

Create a new file named `[slug].astro` in `src/pages/posts/`.

As you did on `index.astro`, import the `BlogPost` interface and `contentfulClient` from `src/lib/contentful.ts`.

This time, fetch your data inside a `getStaticPaths()` function.

 src/pages/posts/[slug].astro

```
---import { contentfulClient } from "../../lib/contentful";import type { BlogPost } from "../../lib/contentful";
export async function getStaticPaths() {  const entries = await contentfulClient.getEntries<BlogPost>({    content_type: "blogPost",  });}---
```

Then, map each item to an object with a `params` and `props` property. The `params` property will be used to generate the URL of the page and the `props` property will be passed to the page component as props.

 src/pages/posts/[slug].astro

```
---import { contentfulClient } from "../../lib/contentful";import { documentToHtmlString } from "@contentful/rich-text-html-renderer";import type { BlogPost } from "../../lib/contentful";
export async function getStaticPaths() {  const entries = await contentfulClient.getEntries<BlogPost>({    content_type: "blogPost",  });
  const pages = entries.items.map((item) => ({    params: { slug: item.fields.slug },    props: {      title: item.fields.title,      content: documentToHtmlString(item.fields.content),      date: new Date(item.fields.date).toLocaleDateString(),    },  }));  return pages;}---
```

The property inside `params` must match the name of the dynamic route. Since our filename is `[slug].astro`, we use `slug`.

In our example, the `props` object passes three properties to the page:

- title (a string)
- content (a rich text Document converted to HTML using `documentToHtmlString`)
- date (formatted using the `Date` constructor)

Finally, you can use the page `props` to display your blog post.

 src/pages/posts/[slug].astro

```
---import { contentfulClient } from "../../lib/contentful";import { documentToHtmlString } from "@contentful/rich-text-html-renderer";import type { BlogPost } from "../../lib/contentful";
export async function getStaticPaths() {  const { items } = await contentfulClient.getEntries<BlogPost>({    content_type: "blogPost",  });  const pages = items.map((item) => ({    params: { slug: item.fields.slug },    props: {      title: item.fields.title,      content: documentToHtmlString(item.fields.content),      date: new Date(item.fields.date).toLocaleDateString(),    },  }));  return pages;}
const { content, title, date } = Astro.props;---<html lang="en">  <head>    <title>{title}</title>  </head>  <body>    <h1>{title}</h1>    <time>{date}</time>    <article set:html={content} />  </body></html>
```

Navigate to [http://localhost:4321/](http://localhost:4321/) and click on one of your posts to make sure your dynamic route is working!

#### On-demand rendering

[Section titled “On-demand rendering”](#on-demand-rendering)

If you’ve [opted into on-demand rendering with an adapter](https://docs.astro.build/en/guides/on-demand-rendering/), you will use a dynamic route that uses a `slug` parameter to fetch the data from Contentful.

Create a `[slug].astro` page in `src/pages/posts`. Use [Astro.params](https://docs.astro.build/en/reference/api-reference/#params) to get the slug from the URL, then pass that to `getEntries`:

 src/pages/posts/[slug].astro

```
---import { contentfulClient } from "../../lib/contentful";import type { BlogPost } from "../../lib/contentful";
const { slug } = Astro.params;
const data = await contentfulClient.getEntries<BlogPost>({  content_type: "blogPost",  "fields.slug": slug,});---
```

If the entry is not found, you can redirect the user to the 404 page using [Astro.redirect](https://docs.astro.build/en/guides/routing/#dynamic-redirects).

 src/pages/posts/[slug].astro

```
---import { contentfulClient } from "../../lib/contentful";import type { BlogPost } from "../../lib/contentful";
const { slug } = Astro.params;
try {  const data = await contentfulClient.getEntries<BlogPost>({    content_type: "blogPost",    "fields.slug": slug,  });} catch (error) {  return Astro.redirect("/404");}---
```

To pass post data to the template section, create a `post` object outside the `try/catch` block.

Use `documentToHtmlString` to convert `content` from a Document to HTML, and use the Date constructor to format the date. `title` can be left as-is. Then, add these properties to your `post` object.

 src/pages/posts/[slug].astro

```
---import Layout from "../../layouts/Layout.astro";import { contentfulClient } from "../../lib/contentful";import { documentToHtmlString } from "@contentful/rich-text-html-renderer";import type { BlogPost } from "../../lib/contentful";
let post;const { slug } = Astro.params;try {  const data = await contentfulClient.getEntries<BlogPost>({    content_type: "blogPost",    "fields.slug": slug,  });  const { title, date, content } = data.items[0].fields;  post = {    title,    date: new Date(date).toLocaleDateString(),    content: documentToHtmlString(content),  };} catch (error) {  return Astro.redirect("/404");}---
```

Finally, you can reference `post` to display your blog post in the template section.

 src/pages/posts/[slug].astro

```
---import Layout from "../../layouts/Layout.astro";import { contentfulClient } from "../../lib/contentful";import { documentToHtmlString } from "@contentful/rich-text-html-renderer";import type { BlogPost } from "../../lib/contentful";
let post;const { slug } = Astro.params;try {  const data = await contentfulClient.getEntries<BlogPost>({    content_type: "blogPost",    "fields.slug": slug,  });  const { title, date, content } = data.items[0].fields;  post = {    title,    date: new Date(date).toLocaleDateString(),    content: documentToHtmlString(content),  };} catch (error) {  return Astro.redirect("/404");}---<html lang="en">  <head>    <title>{post?.title}</title>  </head>  <body>    <h1>{post?.title}</h1>    <time>{post?.date}</time>    <article set:html={post?.content} />  </body></html>
```

### Publishing your site

[Section titled “Publishing your site”](#publishing-your-site)

To deploy your website, visit our [deployment guides](https://docs.astro.build/en/guides/deploy/) and follow the instructions for your preferred hosting provider.

#### Rebuild on Contentful changes

[Section titled “Rebuild on Contentful changes”](#rebuild-on-contentful-changes)

If your project is using Astro’s default static mode, you will need to set up a webhook to trigger a new build when your content changes. If you are using Netlify or Vercel as your hosting provider, you can use its webhook feature to trigger a new build from Contentful events.

##### Netlify

[Section titled “Netlify”](#netlify)

To set up a webhook in Netlify:

1. Go to your site dashboard and click on **Build & deploy**.
2. Under the **Continuous Deployment** tab, find the **Build hooks** section and click on **Add build hook**.
3. Provide a name for your webhook and select the branch you want to trigger the build on. Click on **Save** and copy the generated URL.

##### Vercel

[Section titled “Vercel”](#vercel)

To set up a webhook in Vercel:

1. Go to your project dashboard and click on **Settings**.
2. Under the **Git** tab, find the **Deploy Hooks** section.
3. Provide a name for your webhook and the branch you want to trigger the build on. Click **Add** and copy the generated URL.

##### Adding a webhook to Contentful

[Section titled “Adding a webhook to Contentful”](#adding-a-webhook-to-contentful)

In your Contentful space **settings**, click on the **Webhooks** tab and create a new webhook by clicking the **Add Webhook** button. Provide a name for your webhook and paste the webhook URL you copied in the previous section. Finally, hit **Save** to create the webhook.

Now, whenever you publish a new blog post in Contentful, a new build will be triggered and your blog will be updated.

## More CMS guides

- ![](https://docs.astro.build/logos/apostrophecms.svg)
  ### ApostropheCMS
- ![](https://docs.astro.build/logos/builderio.svg)
  ### Builder.io
- ![](https://docs.astro.build/logos/buttercms.svg)
  ### ButterCMS
- ![](https://docs.astro.build/logos/caisy.svg)
  ### Caisy
- ![](https://docs.astro.build/logos/cloudcannon.svg)
  ### CloudCannon
- ![](https://docs.astro.build/logos/contentful.svg)
  ### Contentful
- ![](https://docs.astro.build/logos/cosmic.svg)
  ### Cosmic
- ![](https://docs.astro.build/logos/craft-cms.svg)
  ### Craft CMS
- ![](https://docs.astro.build/logos/craft-cross-cms.svg)
  ### Craft Cross CMS
- ![](https://docs.astro.build/logos/crystallize.svg)
  ### Crystallize
- ![](https://docs.astro.build/logos/datocms.svg)
  ### DatoCMS
- ![](https://docs.astro.build/logos/decap-cms.svg)
  ### Decap CMS
- ![](https://docs.astro.build/logos/directus.svg)
  ### Directus
- ![](https://docs.astro.build/logos/drupal.svg)
  ### Drupal
- ![](https://docs.astro.build/logos/flotiq.svg)
  ### Flotiq
- ![](https://docs.astro.build/logos/frontmatter-cms.svg)
  ### Front Matter CMS
- ![](https://docs.astro.build/logos/ghost.png)
  ### Ghost
- ![](https://docs.astro.build/logos/gitcms.svg)
  ### GitCMS
- ![](https://docs.astro.build/logos/hashnode.png)
  ### Hashnode
- ![](https://docs.astro.build/logos/hygraph.svg)
  ### Hygraph
- ![](https://docs.astro.build/logos/jekyllpad.svg)
  ### JekyllPad
- ![](https://docs.astro.build/logos/keystatic.svg)
  ### Keystatic
- ![](https://docs.astro.build/logos/keystonejs.svg)
  ### KeystoneJS
- ![](https://docs.astro.build/logos/kontent-ai.svg)
  ### Kontent.ai
- ![](https://docs.astro.build/logos/microcms.svg)
  ### microCMS
- ![](https://docs.astro.build/logos/optimizely.svg)
  ### Optimizely CMS
- ![](https://docs.astro.build/logos/payload.svg)
  ### Payload CMS
- ![](https://docs.astro.build/logos/preprcms.svg)
  ### Prepr CMS
- ![](https://docs.astro.build/logos/prismic.svg)
  ### Prismic
- ![](https://docs.astro.build/logos/sanity.svg)
  ### Sanity
- ![](https://docs.astro.build/logos/sitecore.svg)
  ### Sitecore XM
- ![](https://docs.astro.build/logos/sitepins.svg)
  ### Sitepins
- ![](https://docs.astro.build/logos/spinal.svg)
  ### Spinal
- ![](https://docs.astro.build/logos/statamic.svg)
  ### Statamic
- ![](https://docs.astro.build/logos/storyblok.svg)
  ### Storyblok
- ![](https://docs.astro.build/logos/strapi.svg)
  ### Strapi
- ![](https://docs.astro.build/logos/studiocms.svg)
  ### StudioCMS
- ![](https://docs.astro.build/logos/tina-cms.svg)
  ### Tina CMS
- ![](https://docs.astro.build/logos/umbraco.svg)
  ### Umbraco
- ![](https://docs.astro.build/logos/wordpress.svg)
  ### Wordpress

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)
