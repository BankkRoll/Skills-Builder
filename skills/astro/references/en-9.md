# Cosmic & Astro and more

# Cosmic & Astro

> Add content to your Astro project using Cosmic as a CMS

# Cosmic & Astro

[Cosmic](https://www.cosmicjs.com/) is a [headless CMS](https://www.cosmicjs.com/headless-cms) that provides an admin dashboard to manage content and an API that can integrate with a diverse range of frontend tools.

## Prerequisites

[Section titled “Prerequisites”](#prerequisites)

1. **An Astro project**- If you’d like to start with a fresh Astro project, read the [installation guide](https://docs.astro.build/en/install-and-setup/). This guide follows a simplified version of the [Astro Headless CMS Theme](https://astro.build/themes/details/cosmic-cms-blog/) with [Tailwind CSS](https://tailwindcss.com/) for styling.
2. **A Cosmic account and Bucket** - [Create a free Cosmic account](https://app.cosmicjs.com/signup) if you don’t have one. After creating your account, you’ll be prompted to create a new empty project. There’s also a [Simple Astro Blog template](https://www.cosmicjs.com/marketplace/templates/simple-astro-blog) available (this is the same template as the Astro Headless CMS Theme) to automatically import all of the content used in this guide.
3. **Your Cosmic API keys**  - From your Cosmic dashboard, you will need to locate both the **Bucket slug** and **Bucket read key** in order to connect to Cosmic.

## Integrating Cosmic with Astro

[Section titled “Integrating Cosmic with Astro”](#integrating-cosmic-with-astro)

### Installing Necessary Dependencies

[Section titled “Installing Necessary Dependencies”](#installing-necessary-dependencies)

Add the [Cosmic JavaScript SDK](https://www.npmjs.com/package/@cosmicjs/sdk) to fetch data from your Cosmic Bucket.

- [npm](#tab-panel-2759)
- [pnpm](#tab-panel-2760)
- [Yarn](#tab-panel-2761)

   Terminal window

```
npm install @cosmicjs/sdk
```

   Terminal window

```
pnpm add @cosmicjs/sdk
```

   Terminal window

```
yarn add @cosmicjs/sdk
```

### Configuring API Keys

[Section titled “Configuring API Keys”](#configuring-api-keys)

Create a `.env` file at the root of your Astro project (if it does not already exist). Add both the **Bucket slug** and **Bucket read key** available from your Cosmic dashboard as public environment variables.

 .env

```
PUBLIC_COSMIC_BUCKET_SLUG=YOUR_BUCKET_SLUGPUBLIC_COSMIC_READ_KEY=YOUR_READ_KEY
```

## Fetching Data from Cosmic

[Section titled “Fetching Data from Cosmic”](#fetching-data-from-cosmic)

1. Create a new file called `cosmic.js`. Place this file inside of the `src/lib` folder in your project.
2. Add the following code to fetch data from Cosmic using the SDK and your environment variables.
  The example below creates a function called `getAllPosts()` to fetch metadata from Cosmic `posts` objects:
   src/lib/cosmic.js
  ```
  import { createBucketClient } from '@cosmicjs/sdk'
  const cosmic = createBucketClient({  bucketSlug: import.meta.env.PUBLIC_COSMIC_BUCKET_SLUG,  readKey: import.meta.env.PUBLIC_COSMIC_READ_KEY})
  export async function getAllPosts() {  const data = await cosmic.objects    .find({      type: 'posts'    })    .props('title,slug,metadata,created_at')  return data.objects}
  ```
  Read more about [queries in the Cosmic documentation](https://www.cosmicjs.com/docs/api/queries).
3. Import your query function in a `.astro` component. After fetching data, the results from the query can be used in your Astro template.
  The following example shows fetching metadata from Cosmic `posts` and passing these values as props to a `<Card />` component to create a list of blog posts:
   src/pages/index.astro
  ```
  ---import Card from '../components/Card.astro'import { getAllPosts } from '../lib/cosmic'
  const data = await getAllPosts()---
  <section>  <ul class="grid gap-8 md:grid-cols-2">    {      data.map((post) => (        <Card          title={post.title}          href={post.slug}          body={post.metadata.excerpt}          tags={post.metadata.tags.map((tag) => tag)}        />      ))    }  </ul></section>
  ```
  [View source code for the Card component](https://github.com/cosmicjs/simple-astro-blog/blob/main/src/components/Card.astro)

## Building a Blog with Astro and Cosmic

[Section titled “Building a Blog with Astro and Cosmic”](#building-a-blog-with-astro-and-cosmic)

You can manage your Astro blog’s content using Cosmic and create webhooks to automatically redeploy your website when you update or add new content.

### Cosmic Content Objects

[Section titled “Cosmic Content Objects”](#cosmic-content-objects)

The following instructions assume that you have an **Object Type** in Cosmic called **posts**. Each individual blog post is a `post` that is defined in the Cosmic dashboard with the following Metafields:

1. **Text input** - Author
2. **Image** - Cover Image
3. **Repeater** - Tags
  - **Text input** - Title
4. **Text area** - Excerpt
5. **Rich Text** - Content

### Displaying a List of Blog Posts in Astro

[Section titled “Displaying a List of Blog Posts in Astro”](#displaying-a-list-of-blog-posts-in-astro)

Using the same [data-fetching method](#fetching-data-from-cosmic) as above, import the `getAllPosts()` query from your script file and await the data. This function provides metadata about each `post` which can be displayed dynamically.

The example below passes these values to a `<Card />` component to display a formatted list of blog posts:

 src/pages/index.astro

```
---import Card from '../components/Card.astro'import { getAllPosts } from '../lib/cosmic'
const data = await getAllPosts()---
<section>  <ul class="grid gap-8 md:grid-cols-2">    {      data.map((post) => (        <Card          title={post.title}          href={post.slug}          body={post.metadata.excerpt}          tags={post.metadata.tags.map((tag) => tag)}        />      ))    }  </ul></section>
```

### Generating Individual Blog Posts with Astro

[Section titled “Generating Individual Blog Posts with Astro”](#generating-individual-blog-posts-with-astro)

To generate an individual page with full content for each blog post, create a [dynamic routing page](https://docs.astro.build/en/guides/routing/#dynamic-routes) at `src/pages/blog/[slug].astro`.

This page will export a `getStaticPaths()` function to generate a page route at the `slug` returned from each `post` object. This function is called at build time and generates and renders all of your blog posts at once.

To access your data from Cosmic:

- Query Cosmic inside of `getStaticPaths()` to fetch data about each post and provide it to the function.
- Use each `post.slug` as a route parameter, creating the URLs for each blog post.
- Return each `post` inside of `Astro.props`, making the post data available to HTML template portion of the page component for rendering.

The HTML markup below uses various data from Cosmic, such as the post title, cover image, and the **rich text content** (full blog post content). Use [set:html](https://docs.astro.build/en/reference/directives-reference/#sethtml) on the element displaying the rich text content from Cosmic to render HTML elements on the page exactly as fetched from Cosmic.

 src/pages/blog/[slug].astro

```
---import { getAllPosts } from '../../lib/cosmic'import { Image } from 'astro:assets'
export async function getStaticPaths() {  const data = (await getAllPosts()) || []
  return data.map((post) => {    return {      params: { slug: post.slug },      props: { post }    }  })}
const { post } = Astro.props---
<article class="mx-auto max-w-screen-md pt-20">  <section class="border-b pb-8">    <h1 class="text-4xl font-bold">{post.title}</h1>    <div class="my-4"></div>    <span class="text-sm font-semibold">{post.metadata.author?.title}</span>  </section>  {    post.metadata.cover_image && (      <Image        src={post.metadata.cover_image.imgix_url}        format="webp"        width={1200}        height={675}        aspectRatio={16 / 9}        quality={50}        alt={`Cover image for the blog ${post.title}`}        class={'my-12 rounded-md shadow-lg'}      />    )  }  <div set:html={post.metadata.content} /></article>
```

### Publishing your site

[Section titled “Publishing your site”](#publishing-your-site)

To deploy your website, visit the [deployment guides](https://docs.astro.build/en/guides/deploy/) and follow the instructions for your preferred hosting provider.

#### Rebuild on Cosmic content updates

[Section titled “Rebuild on Cosmic content updates”](#rebuild-on-cosmic-content-updates)

You can set up a webhook in Cosmic directly to trigger a redeploy of your site on your hosting platform (e.g. Vercel) whenever you update or add content Objects.

Under “Settings” > “webhooks”, add the URL endpoint from Vercel and select the Object Type you would like to trigger the webhook. Click “Add webhook” to save it.

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

## Themes

[Section titled “Themes”](#themes)

- [Astro Headless CMS Blog](https://astro.build/themes/details/cosmic-cms-blog/)

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

# Craft CMS & Astro

> Add content to your Astro project using Craft CMS as a CMS

# Craft CMS & Astro

[Craft CMS](https://craftcms.com/) is a flexible open source CMS with an accessible authoring experience. It includes its own front end, but can also be used as a headless CMS to provide content to your Astro project.

## Official Resources

[Section titled “Official Resources”](#official-resources)

- Check out the official Craft CMS [GraphQL API guide](https://craftcms.com/docs/5.x/development/graphql.html)
- The official documentation for Craft’s [headlessModeconfig setting](https://craftcms.com/docs/5.x/reference/config/general.html#headlessmode)

## Community Resources

[Section titled “Community Resources”](#community-resources)

- [SSG Astro with Headless Craft CMS Content Fetched At Build Time](https://www.olets.dev/posts/ssg-astro-with-headless-craft-cms-content-fetched-at-build-time/)
- [SSG Astro with Headless Craft CMS Content Fetched At Build Time Or Cached In Advance](https://www.olets.dev/posts/ssg-astro-with-headless-craft-cms-content-fetched-at-build-time-or-cached-in-advance/)
- [SSR Astro With Headless Craft CMS](https://www.olets.dev/posts/ssr-astro-with-headless-craft-cms/)

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

# Craft Cross CMS & Astro

> Add content to your Astro project using Craft Cross CMS

# Craft Cross CMS & Astro

[Craft Cross CMS](https://ecosystem.plaid.co.jp/product/karte-craft/xcms) is an API-based headless CMS from the KARTE ecosystem.

## Official Resources

[Section titled “Official Resources”](#official-resources)

- Blog: [Build an Astro Website with Craft Cross CMS](https://solution.karte.io/blog/2025/10/build-website-with-astro-using-xcms/)
- Sample code (GitHub): [Craft Cross CMS with Astro (sample)](https://github.com/plaidev/craft-codes/tree/main/astro/cross-cms-astro-sample)

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

# Crystallize & Astro

> Add content to your Astro project using Crystallize as a CMS

# Crystallize & Astro

[Crystallize](https://crystallize.com/) is a headless content management system for eCommerce that exposes a GraphQL API.

## Example

[Section titled “Example”](#example) src/pages/index.astro

```
---// Fetch your catalogue paths from Crystallize GraphQL API
import BaseLayout from '../../layouts/BaseLayout.astro';import { createClient } from '@crystallize/js-api-client';
const apiClient = createClient({  tenantIdentifier: 'furniture'});
const query = `  query getCataloguePaths{    catalogue(language: "en", path: "/shop") {      name      children {        name        path      }    }  }`const { data: { catalogue } } = await apiClient.catalogueApi(query)---<BaseLayout>  <h1>{catalogue.name}</h1>  <nav>    <ul>      {catalogue.children.map(child => (        <li><a href={child.path}>{child.name}</a></li>      ))}    </ul>  </nav></BaseLayout>
```

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

# DatoCMS & Astro

> Add content to your Astro project using DatoCMS

# DatoCMS & Astro

[DatoCMS](https://datocms.com/) is a web-based, headless CMS to manage digital content for your sites and apps.

## Integrating with Astro

[Section titled “Integrating with Astro”](#integrating-with-astro)

In this guide, you will fetch content data from DatoCMS in your Astro project, then display it on a page.

## Prerequisites

[Section titled “Prerequisites”](#prerequisites)

To get started, you will need to have the following:

- **An Astro project** - If you don’t have an Astro project yet, you can follow the instructions in our [Installation guide](https://docs.astro.build/en/install-and-setup/).
- **A DatoCMS account and project** - If you don’t have an account, you can [sign up for a free account](https://dashboard.datocms.com/signup).
- **The read-only API Key for your DatoCMS project** - You can find it in the admin dashboard of your project, under “Settings” > “API Tokens”.

## Setting up the credentials

[Section titled “Setting up the credentials”](#setting-up-the-credentials)

Create a new file (if one does not already exist) named `.env` in the root of your Astro project. Add a new environment variable as follows, using the API key found in your DatoCMS admin dashboard:

 .env

```
DATOCMS_API_KEY=YOUR_API_KEY
```

For TypeScript support, declare the typing of this environment variable in the `env.d.ts` file in the `src/` folder. If this file does not exist, you can create it and add the following:

 src/env.d.ts

```
interface ImportMetaEnv {  readonly DATOCMS_API_KEY: string;}
```

Your root directory should now include these files:

- Directorysrc/
  - **env.d.ts**
- **.env**
- astro.config.mjs
- package.json

   Learn more about [environment variables](https://docs.astro.build/en/guides/environment-variables/) and `.env` files in Astro.

## Create a Model in DatoCMS

[Section titled “Create a Model in DatoCMS”](#create-a-model-in-datocms)

In the DatoCMS admin dashboard of your project, navigate to “Settings” > “Models” and create a new Model called “Home” with the “Single Instance” toggle selected. This will create a home page for your project. In this model, add a new text field for the page title.

Navigate to the “Content” tab in your project and click on your newly-created home page. You can now add a title. Save the page, and continue.

## Fetching data

[Section titled “Fetching data”](#fetching-data)

In your Astro project, navigate to the page that will fetch and display your CMS content. Add the following query to fetch the content for `home` using the DatoCMS GraphQL API.

This example displays the page title from DatoCMS on `src/pages/index.astro`:

 src/pages/index.astro

```
---const response = await fetch('https://graphql.datocms.com/', {  method: 'POST',  headers: {    'Content-Type': 'application/json',    Accept: 'application/json',    Authorization: `Bearer ${import.meta.env.DATOCMS_API_KEY}`,  },  body: JSON.stringify({    query: `query Homepage {          home {            title          }        }      `,  }),});
const json = await response.json();const data = json.data.home;---
<h1>{data.title}</h1>
```

This GraphQL query will fetch the `title` field in the `home` page from your DatoCMS Project. When you refresh your browser, you should see the title on your page.

## Adding Dynamic modular content blocks

[Section titled “Adding Dynamic modular content blocks”](#adding-dynamic-modular-content-blocks)

If your DatosCMS project includes [modular content](https://www.datocms.com/docs/content-modelling/modular-content), then you will need to build a corresponding `.astro` component for each block of content (e.g. a text section, a video, a quotation block, etc.) that the modular field allows in your project.

The example below is a `<Text />` Astro component for displaying a “Multiple-paragraph text” block from DatoCMS.

 src/components/Text.astro

```
---export interface TextProps {  text: string}
export interface Props {  item: TextProps}
const { item } = Astro.props;---
<div set:html={item.text} />
```

To fetch these blocks, edit your GraphQL query to include the modular content block you created in DatoCMS.

In this example, the modular content block is named **content** in DatoCMS. This query also includes the unique `_modelApiKey` of each item to check which block should be displayed in the modular field, based on which block was chosen by the content author in the DatoCMS editor. Use a switch statement in the Astro template to allow for dynamic rendering based on the data received from the query.

The following example represents a DatoCMS modular content block that allows an author to choose between a text field (`<Text />`) and an image (`<Image />`) rendered on the home page:

 src/pages/index.astro

```
---import Image from '../components/Image.astro';import Text from '../components/Text.astro';
const response = await fetch('https://graphql.datocms.com/', {  method: 'POST',  headers: {    'Content-Type': 'application/json',    Accept: 'application/json',    Authorization: `Bearer ${import.meta.env.DATOCMS_API_KEY}`,  },  body: JSON.stringify({    query: `query Homepage {          home {            title            content {              ... on ImageRecord {                _modelApiKey               image{                url               }              }              ... on TextRecord {                _modelApiKey                text(markdown: true)              }            }          }        }      `,  }),});
const json = await response.json();const data = json.data.home;---
<h1>{data.title}</h1>{  data.content.map((item: any) => {    switch (item._modelApiKey) {      case 'image':        return <Image item={item} />;      case 'text':        return <Text item={item} />;      default:        return null;    }  })}
```

## Publishing your site

[Section titled “Publishing your site”](#publishing-your-site)

To deploy your website, visit our [deployment guides](https://docs.astro.build/en/guides/deploy/) and follow the instructions for your preferred hosting provider.

## Publish on DatoCMS content changes

[Section titled “Publish on DatoCMS content changes”](#publish-on-datocms-content-changes)

If your project is using Astro’s default static mode, you will need to set up a webhook to trigger a new build when your content changes. If you are using Netlify or Vercel as your hosting provider, you can use its webhook feature to trigger a new build when you change content in DatoCMS.

### Netlify

[Section titled “Netlify”](#netlify)

To set up a webhook in Netlify:

1. Go to your site dashboard and click on **Build & deploy**.
2. Under the **Continuous Deployment** tab, find the **Build hooks** section and click on **Add build hook**.
3. Provide a name for your webhook and select the branch you want to trigger the build on. Click on **Save** and copy the generated URL.

### Vercel

[Section titled “Vercel”](#vercel)

To set up a webhook in Vercel:

1. Go to your project dashboard and click on **Settings**.
2. Under the **Git** tab, find the **Deploy Hooks** section.
3. Provide a name for your webhook and the branch you want to trigger the build on. Click **Add** and copy the generated URL.

### Adding a webhook to DatoCMS

[Section titled “Adding a webhook to DatoCMS”](#adding-a-webhook-to-datocms)

In your DatoCMS project admin dashboard, navigate to the **Settings** tab and click **Webhooks**. Click the plus icon to create a new webhook and give it a name. In the URL field, paste the URL generated by your preferred hosting service. As Trigger, select whichever option suits your needs. (For example: build every time a new record is published.)

## Starter project

[Section titled “Starter project”](#starter-project)

You can also check out the [Astro blog template](https://www.datocms.com/marketplace/starters/astro-template-blog) on the DatoCMS marketplace to learn how to create a blog with Astro and DatoCMS.

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

# Decap CMS & Astro

> Add content to your Astro project using Decap as a CMS

# Decap CMS & Astro

[Decap CMS](https://www.decapcms.org/) (formerly Netlify CMS) is an open-source, Git-based content management system.

Decap allows you to take full advantage of all of Astro’s features, including image optimization and content collections.

Decap adds a route (typically `/admin`) to your project that will load a React app to allow authorized users to manage content directly from the deployed website. Decap will commit changes directly to your Astro project’s source repository.

## Installing DecapCMS

[Section titled “Installing DecapCMS”](#installing-decapcms)

There are two options for adding Decap to Astro:

1. [Install Decap via a package manager](https://decapcms.org/docs/install-decap-cms/#installing-with-npm) with the following command:
  - [npm](#tab-panel-2762)
  - [pnpm](#tab-panel-2763)
  - [Yarn](#tab-panel-2764)
     Terminal window
  ```
  npm install decap-cms-app
  ```
     Terminal window
  ```
  pnpm add decap-cms-app
  ```
     Terminal window
  ```
  yarn add decap-cms-app
  ```
2. Import the package into a `<script>` tag in your page `<body>`
   /admin
  ```
  <body>    <script src="https://unpkg.com/decap-cms@^3.1.2/dist/decap-cms.js"></script></body>
  ```

## Configuration

[Section titled “Configuration”](#configuration)

1. Create a static admin folder at `public/admin/`
2. Add `config.yml` to `public/admin/`:
  - Directorypublic
    - Directoryadmin
      - config.yml
3. To add support for content collections, configure each schema in `config.yml`. The following example configures a `blog` collection, defining a `label` for each entry’s frontmatter property:
   /public/admin/config.yml
  ```
  collections:  - name: "blog" # Used in routes, e.g., /admin/collections/blog    label: "Blog" # Used in the UI    folder: "src/content/blog" # The path to the folder where the documents are stored    create: true # Allow users to create new documents in this collection    fields: # The fields for each document, usually in frontmatter      - { label: "Layout", name: "layout", widget: "hidden", default: "blog" }      - { label: "Title", name: "title", widget: "string" }      - { label: "Publish Date", name: "date", widget: "datetime" }      - { label: "Featured Image", name: "thumbnail", widget: "image" }      - { label: "Rating (scale of 1-5)", name: "rating", widget: "number" }      - { label: "Body", name: "body", widget: "markdown" }
  ```
4. Add the `admin` route for your React app in `src/pages/admin.html`.
  - Directorypublic
    - Directoryadmin
      - config.yml
  - Directorysrc
    - Directorypages
      - admin.html
   /src/pages/admin.html
  ```
  <!doctype html><html lang="en">  <head>    <meta charset="utf-8" />    <meta name="viewport" content="width=device-width, initial-scale=1.0" />    <meta name="robots" content="noindex" />    <link href="/admin/config.yml" type="text/yaml" rel="cms-config-url" />    <title>Content Manager</title>  </head>  <body>    <script src="https://unpkg.com/decap-cms@^3.1.2/dist/decap-cms.js"></script>  </body></html>
  ```
5. To enable media uploads to a specific folder via the Decap editor, add an appropriate path:
   /public/admin/config.yml
  ```
  media_folder: "src/assets/images" # Location where files will be stored in the repopublic_folder: "src/assets/images" # The src attribute for uploaded media
  ```

See [the Decap CMS configuration documentation](https://decapcms.org/docs/configure-decap-cms/) for full instructions and options.

## Usage

[Section titled “Usage”](#usage)

Navigate to `yoursite.com/admin/` to use the Decap CMS editor.

## Authentication

[Section titled “Authentication”](#authentication)

### Decap CMS with Netlify Identity

[Section titled “Decap CMS with Netlify Identity”](#decap-cms-with-netlify-identity)

Decap CMS was originally developed by Netlify and has first class support for [Netlify Identity](https://docs.netlify.com/security/secure-access-to-sites/identity/).

When deploying to Netlify, configure Identity for your project via the Netlify dashboard and include the [Netlify Identity Widget](https://github.com/netlify/netlify-identity-widget) on the `admin` route of your project. Optionally include the Identity Widget on the homepage of your site if you plan to invite new users via email.

### Decap CMS with External OAuth Clients

[Section titled “Decap CMS with External OAuth Clients”](#decap-cms-with-external-oauth-clients)

When deploying to hosting providers other than Netlify, you must create your own OAuth routes.

In Astro, this can be done with on-demand rendered routes in your project configured with [an adapter](https://docs.astro.build/en/guides/on-demand-rendering/) enabled.

See [Decap’s OAuth Docs](https://decapcms.org/docs/external-oauth-clients/) for a list of compatible community-maintained OAuth clients.

## Community Resources

[Section titled “Community Resources”](#community-resources)

- Netlify Identity Template: [astro-decap-ssg-netlify](https://github.com/OliverSpeir/astro-decap-ssg-netlify-identity)
- On-demand rendering OAuth Routes with Astro Template: [astro-decap-starter-ssr](https://github.com/OliverSpeir/astro-decap-starter-ssr)
- Blog Post: [Author your Astro site’s content with Git-based CMSs](https://aalam.vercel.app/blog/astro-and-git-cms-netlify) by Aftab Alam
- Youtube Tutorial: [Create a Custom Blog with Astro & NetlifyCMS in MINUTES!](https://www.youtube.com/watch?v=3yip2wSRX_4) by Kumail Pirzada

## Production Sites

[Section titled “Production Sites”](#production-sites)

The following sites use Astro + Decap CMS in production:

- [yunielacosta.com](https://www.yunielacosta.com/) by Yuniel Acosta — [source code on GitHub](https://github.com/yacosta738/yacosta738.github.io) (Netlify CMS)
- [portfolioris.nl](https://www.portfolioris.nl/) by Joris Hulsbosch – [source code on GitHub](https://github.com/portfolioris/portfolioris.nl)

## Themes

[Section titled “Themes”](#themes)

- [Astros](https://astro.build/themes/details/astros)
- [Enhanced Astro Starter](https://astro.build/themes/details/enhanced-astro-starter)
- [Astro Decap CMS Starter](https://astro.build/themes/details/astro-decap-cms-starter)

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

# Directus & Astro

> Add content to your Astro project using Directus as a CMS

# Directus & Astro

[Directus](https://directus.io/) is a backend-as-a-service which can be used to host data and content for your Astro project.

## Official Resources

[Section titled “Official Resources”](#official-resources)

- [Getting Started with Directus and Astro](https://docs.directus.io/blog/getting-started-directus-astro.html).

## Community Resources

[Section titled “Community Resources”](#community-resources)   [Using Directus CMS with Neon Postgres and Astro to build a blog](https://neon.tech/guides/directus-cms)

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
