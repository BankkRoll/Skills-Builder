# Client and more

# Client

> Learn about client-side data fetching, and how to use SWR, a data fetching React Hook library that handles caching, revalidation, focus tracking, refetching on interval and more.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Data Fetching](https://nextjs.org/docs/pages/building-your-application/data-fetching)Client-side FetchingYou are currently viewing the documentation for Pages Router.

# Client-side Fetching

Last updated  April 23, 2025

Client-side data fetching is useful when your page doesn't require SEO indexing, when you don't need to pre-render your data, or when the content of your pages needs to update frequently. Unlike the server-side rendering APIs, you can use client-side data fetching at the component level.

If done at the page level, the data is fetched at runtime, and the content of the page is updated as the data changes. When used at the component level, the data is fetched at the time of the component mount, and the content of the component is updated as the data changes.

It's important to note that using client-side data fetching can affect the performance of your application and the load speed of your pages. This is because the data fetching is done at the time of the component or pages mount, and the data is not cached.

## Client-side data fetching with useEffect

The following example shows how you can fetch data on the client side using the useEffect hook.

```
import { useState, useEffect } from 'react'

function Profile() {
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/profile-data')
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
  }, [])

  if (isLoading) return <p>Loading...</p>
  if (!data) return <p>No profile data</p>

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.bio}</p>
    </div>
  )
}
```

## Client-side data fetching with SWR

The team behind Next.js has created a React Hook library for data fetching called [SWR](https://swr.vercel.app/). It is **highly recommended** if you are fetching data on the client-side. It handles caching, revalidation, focus tracking, refetching on intervals, and more.

Using the same example as above, we can now use SWR to fetch the profile data. SWR will automatically cache the data for us and will revalidate the data if it becomes stale.

For more information on using SWR, check out the [SWR docs](https://swr.vercel.app/docs/getting-started).

```
import useSWR from 'swr'

const fetcher = (...args) => fetch(...args).then((res) => res.json())

function Profile() {
  const { data, error } = useSWR('/api/profile-data', fetcher)

  if (error) return <div>Failed to load</div>
  if (!data) return <div>Loading...</div>

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.bio}</p>
    </div>
  )
}
```

Was this helpful?

supported.

---

# getServerSideProps

> Fetch data on each request with `getServerSideProps`.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Data Fetching](https://nextjs.org/docs/pages/building-your-application/data-fetching)getServerSidePropsYou are currently viewing the documentation for Pages Router.

# getServerSideProps

Last updated  May 21, 2025

`getServerSideProps` is a Next.js function that can be used to fetch data and render the contents of a page at request time.

## Example

You can use `getServerSideProps` by exporting it from a Page Component. The example below shows how you can fetch data from a 3rd party API in `getServerSideProps`, and pass the data to the page as props:

 pages/index.tsxJavaScriptTypeScript

```
import type { InferGetServerSidePropsType, GetServerSideProps } from 'next'

type Repo = {
  name: string
  stargazers_count: number
}

export const getServerSideProps = (async () => {
  // Fetch data from external API
  const res = await fetch('https://api.github.com/repos/vercel/next.js')
  const repo: Repo = await res.json()
  // Pass data to the page via props
  return { props: { repo } }
}) satisfies GetServerSideProps<{ repo: Repo }>

export default function Page({
  repo,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  return (
    <main>
      <p>{repo.stargazers_count}</p>
    </main>
  )
}
```

## When should I usegetServerSideProps?

You should use `getServerSideProps` if you need to render a page that relies on personalized user data, or information that can only be known at request time. For example, `authorization` headers or a geolocation.

If you do not need to fetch the data at request time, or would prefer to cache the data and pre-rendered HTML, we recommend using [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props).

## Behavior

- `getServerSideProps` runs on the server.
- `getServerSideProps` can only be exported from a **page**.
- `getServerSideProps` returns JSON.
- When a user visits a page, `getServerSideProps` will be used to fetch data at request time, and the data is used to render the initial HTML of the page.
- `props` passed to the page component can be viewed on the client as part of the initial HTML. This is to allow the page to be [hydrated](https://react.dev/reference/react-dom/hydrate) correctly. Make sure that you don't pass any sensitive information that shouldn't be available on the client in `props`.
- When a user visits the page through [next/link](https://nextjs.org/docs/pages/api-reference/components/link) or [next/router](https://nextjs.org/docs/pages/api-reference/functions/use-router), Next.js sends an API request to the server, which runs `getServerSideProps`.
- You do not have to call a Next.js [API Route](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) to fetch data when using `getServerSideProps` since the function runs on the server. Instead, you can call a CMS, database, or other third-party APIs directly from inside `getServerSideProps`.

> **Good to know:**
>
>
>
> - See [getServerSidePropsAPI reference](https://nextjs.org/docs/pages/api-reference/functions/get-server-side-props) for parameters and props that can be used with `getServerSideProps`.
> - You can use the [next-code-elimination tool](https://next-code-elimination.vercel.app/) to verify what Next.js eliminates from the client-side bundle.

## Error Handling

If an error is thrown inside `getServerSideProps`, it will show the `pages/500.js` file. Check out the documentation for [500 page](https://nextjs.org/docs/pages/building-your-application/routing/custom-error#500-page) to learn more on how to create it. During development, this file will not be used and the development error overlay will be shown instead.

## Edge Cases

### Caching with Server-Side Rendering (SSR)

You can use caching headers (`Cache-Control`) inside `getServerSideProps` to cache dynamic responses. For example, using [stale-while-revalidate](https://web.dev/stale-while-revalidate/).

```
// This value is considered fresh for ten seconds (s-maxage=10).
// If a request is repeated within the next 10 seconds, the previously
// cached value will still be fresh. If the request is repeated before 59 seconds,
// the cached value will be stale but still render (stale-while-revalidate=59).
//
// In the background, a revalidation request will be made to populate the cache
// with a fresh value. If you refresh the page, you will see the new value.
export async function getServerSideProps({ req, res }) {
  res.setHeader(
    'Cache-Control',
    'public, s-maxage=10, stale-while-revalidate=59'
  )

  return {
    props: {},
  }
}
```

However, before reaching for `cache-control`, we recommend seeing if [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) with [ISR](https://nextjs.org/docs/pages/guides/incremental-static-regeneration) is a better fit for your use case.

Was this helpful?

supported.

---

# getStaticPaths

> Fetch data and generate static pages with `getStaticPaths`. Learn more about this API for data fetching in Next.js.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Data Fetching](https://nextjs.org/docs/pages/building-your-application/data-fetching)getStaticPathsYou are currently viewing the documentation for Pages Router.

# getStaticPaths

Last updated  April 15, 2025

If a page has [Dynamic Routes](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes) and uses `getStaticProps`, it needs to define a list of paths to be statically generated.

When you export a function called `getStaticPaths` (Static Site Generation) from a page that uses dynamic routes, Next.js will statically pre-render all the paths specified by `getStaticPaths`.

 pages/repo/[name].tsxJavaScriptTypeScript

```
import type {
  InferGetStaticPropsType,
  GetStaticProps,
  GetStaticPaths,
} from 'next'

type Repo = {
  name: string
  stargazers_count: number
}

export const getStaticPaths = (async () => {
  return {
    paths: [
      {
        params: {
          name: 'next.js',
        },
      }, // See the "paths" section below
    ],
    fallback: true, // false or "blocking"
  }
}) satisfies GetStaticPaths

export const getStaticProps = (async (context) => {
  const res = await fetch('https://api.github.com/repos/vercel/next.js')
  const repo = await res.json()
  return { props: { repo } }
}) satisfies GetStaticProps<{
  repo: Repo
}>

export default function Page({
  repo,
}: InferGetStaticPropsType<typeof getStaticProps>) {
  return repo.stargazers_count
}
```

The [getStaticPathsAPI reference](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths) covers all parameters and props that can be used with `getStaticPaths`.

## When should I use getStaticPaths?

You should use `getStaticPaths` if you’re statically pre-rendering pages that use dynamic routes and:

- The data comes from a headless CMS
- The data comes from a database
- The data comes from the filesystem
- The data can be publicly cached (not user-specific)
- The page must be pre-rendered (for SEO) and be very fast — `getStaticProps` generates `HTML` and `JSON` files, both of which can be cached by a CDN for performance

## When does getStaticPaths run

`getStaticPaths` will only run during build in production, it will not be called during runtime. You can validate code written inside `getStaticPaths` is removed from the client-side bundle [with this tool](https://next-code-elimination.vercel.app/).

### How does getStaticProps run with regards to getStaticPaths

- `getStaticProps` runs during `next build` for any `paths` returned during build
- `getStaticProps` runs in the background when using `fallback: true`
- `getStaticProps` is called before initial render when using `fallback: blocking`

## Where can I use getStaticPaths

- `getStaticPaths` **must** be used with `getStaticProps`
- You **cannot** use `getStaticPaths` with [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props)
- You can export `getStaticPaths` from a [Dynamic Route](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes) that also uses `getStaticProps`
- You **cannot** export `getStaticPaths` from non-page file (e.g. your `components` folder)
- You must export `getStaticPaths` as a standalone function, and not a property of the page component

## Runs on every request in development

In development (`next dev`), `getStaticPaths` will be called on every request.

## Generating paths on-demand

`getStaticPaths` allows you to control which pages are generated during the build instead of on-demand with [fallback](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-blocking). Generating more pages during a build will cause slower builds.

You can defer generating all pages on-demand by returning an empty array for `paths`. This can be especially helpful when deploying your Next.js application to multiple environments. For example, you can have faster builds by generating all pages on-demand for previews (but not production builds). This is helpful for sites with hundreds/thousands of static pages.

 pages/posts/[id].js

```
export async function getStaticPaths() {
  // When this is true (in preview environments) don't
  // prerender any static pages
  // (faster builds, but slower initial page load)
  if (process.env.SKIP_BUILD_STATIC_GENERATION) {
    return {
      paths: [],
      fallback: 'blocking',
    }
  }

  // Call an external API endpoint to get posts
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  // Get the paths we want to prerender based on posts
  // In production environments, prerender all pages
  // (slower builds, but faster initial page load)
  const paths = posts.map((post) => ({
    params: { id: post.id },
  }))

  // { fallback: false } means other routes should 404
  return { paths, fallback: false }
}
```

Was this helpful?

supported.

---

# getStaticProps

> Fetch data and generate static pages with `getStaticProps`. Learn more about this API for data fetching in Next.js.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Data Fetching](https://nextjs.org/docs/pages/building-your-application/data-fetching)getStaticPropsYou are currently viewing the documentation for Pages Router.

# getStaticProps

Last updated  October 17, 2025

If you export a function called `getStaticProps` (Static Site Generation) from a page, Next.js will pre-render this page at build time using the props returned by `getStaticProps`.

 pages/index.tsxJavaScriptTypeScript

```
import type { InferGetStaticPropsType, GetStaticProps } from 'next'

type Repo = {
  name: string
  stargazers_count: number
}

export const getStaticProps = (async (context) => {
  const res = await fetch('https://api.github.com/repos/vercel/next.js')
  const repo = await res.json()
  return { props: { repo } }
}) satisfies GetStaticProps<{
  repo: Repo
}>

export default function Page({
  repo,
}: InferGetStaticPropsType<typeof getStaticProps>) {
  return repo.stargazers_count
}
```

> Note that irrespective of rendering type, any `props` will be passed to the page component and can be viewed on the client-side in the initial HTML. This is to allow the page to be [hydrated](https://react.dev/reference/react-dom/hydrate) correctly. Make sure that you don't pass any sensitive information that shouldn't be available on the client in `props`.

The [getStaticPropsAPI reference](https://nextjs.org/docs/pages/api-reference/functions/get-static-props) covers all parameters and props that can be used with `getStaticProps`.

## When should I use getStaticProps?

You should use `getStaticProps` if:

- The data required to render the page is available at build time ahead of a user’s request
- The data comes from a headless CMS
- The page must be pre-rendered (for SEO) and be very fast — `getStaticProps` generates `HTML` and `JSON` files, both of which can be cached by a CDN for performance
- The data can be publicly cached (not user-specific). This condition can be bypassed in certain specific situation by using a Proxy to rewrite the path.

## When does getStaticProps run

`getStaticProps` always runs on the server and never on the client. You can validate code written inside `getStaticProps` is removed from the client-side bundle [with this tool](https://next-code-elimination.vercel.app/).

- `getStaticProps` always runs during `next build`
- `getStaticProps` runs in the background when using [fallback: true](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-true)
- `getStaticProps` is called before initial render when using [fallback: blocking](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-blocking)
- `getStaticProps` runs in the background when using `revalidate`
- `getStaticProps` runs on-demand in the background when using [revalidate()](https://nextjs.org/docs/pages/guides/incremental-static-regeneration#on-demand-revalidation-with-revalidatepath)

When combined with [Incremental Static Regeneration](https://nextjs.org/docs/pages/guides/incremental-static-regeneration), `getStaticProps` will run in the background while the stale page is being revalidated, and the fresh page served to the browser.

`getStaticProps` does not have access to the incoming request (such as query parameters or HTTP headers) as it generates static HTML. If you need access to the request for your page, consider using [Proxy](https://nextjs.org/docs/pages/api-reference/file-conventions/proxy) in addition to `getStaticProps`.

## Using getStaticProps to fetch data from a CMS

The following example shows how you can fetch a list of blog posts from a CMS.

 pages/blog.tsxJavaScriptTypeScript

```
// posts will be populated at build time by getStaticProps()
export default function Blog({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li>{post.title}</li>
      ))}
    </ul>
  )
}

// This function gets called at build time on server-side.
// It won't be called on client-side, so you can even do
// direct database queries.
export async function getStaticProps() {
  // Call an external API endpoint to get posts.
  // You can use any data fetching library
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  // By returning { props: { posts } }, the Blog component
  // will receive `posts` as a prop at build time
  return {
    props: {
      posts,
    },
  }
}
```

The [getStaticPropsAPI reference](https://nextjs.org/docs/pages/api-reference/functions/get-static-props) covers all parameters and props that can be used with `getStaticProps`.

## Write server-side code directly

As `getStaticProps` runs only on the server-side, it will never run on the client-side. It won’t even be included in the JS bundle for the browser, so you can write direct database queries without them being sent to browsers.

This means that instead of fetching an **API route** from `getStaticProps` (that itself fetches data from an external source), you can write the server-side code directly in `getStaticProps`.

Take the following example. An API route is used to fetch some data from a CMS. That API route is then called directly from `getStaticProps`. This produces an additional call, reducing performance. Instead, the logic for fetching the data from the CMS can be shared by using a `lib/` directory. Then it can be shared with `getStaticProps`.

 lib/load-posts.js

```
// The following function is shared
// with getStaticProps and API routes
// from a `lib/` directory
export async function loadPosts() {
  // Call an external API endpoint to get posts
  const res = await fetch('https://.../posts/')
  const data = await res.json()

  return data
}
```

 pages/blog.js

```
// pages/blog.js
import { loadPosts } from '../lib/load-posts'

// This function runs only on the server side
export async function getStaticProps() {
  // Instead of fetching your `/api` route you can call the same
  // function directly in `getStaticProps`
  const posts = await loadPosts()

  // Props returned will be passed to the page component
  return { props: { posts } }
}
```

Alternatively, if you are **not** using API routes to fetch data, then the [fetch()](https://developer.mozilla.org/docs/Web/API/Fetch_API) API *can* be used directly in `getStaticProps` to fetch data.

To verify what Next.js eliminates from the client-side bundle, you can use the [next-code-elimination tool](https://next-code-elimination.vercel.app/).

## Statically generates both HTML and JSON

When a page with `getStaticProps` is pre-rendered at build time, in addition to the page HTML file, Next.js generates a JSON file holding the result of running `getStaticProps`.

This JSON file will be used in client-side routing through [next/link](https://nextjs.org/docs/pages/api-reference/components/link) or [next/router](https://nextjs.org/docs/pages/api-reference/functions/use-router). When you navigate to a page that’s pre-rendered using `getStaticProps`, Next.js fetches this JSON file (pre-computed at build time) and uses it as the props for the page component. This means that client-side page transitions will **not** call `getStaticProps` as only the exported JSON is used.

When using Incremental Static Generation, `getStaticProps` will be executed in the background to generate the JSON needed for client-side navigation. You may see this in the form of multiple requests being made for the same page, however, this is intended and has no impact on end-user performance.

## Where can I use getStaticProps

`getStaticProps` can only be exported from a **page**. You **cannot** export it from non-page files, `_app`, `_document`, or `_error`.

One of the reasons for this restriction is that React needs to have all the required data before the page is rendered.

Also, you must use export `getStaticProps` as a standalone function — it will **not** work if you add `getStaticProps` as a property of the page component.

> **Good to know**: if you have created a [custom app](https://nextjs.org/docs/pages/building-your-application/routing/custom-app), ensure you are passing the `pageProps` to the page component as shown in the linked document, otherwise the props will be empty.

## Runs on every request in development

In development (`next dev`), `getStaticProps` will be called on every request.

## Preview Mode

You can temporarily bypass static generation and render the page at **request time** instead of build time using [Preview Mode](https://nextjs.org/docs/pages/guides/preview-mode). For example, you might be using a headless CMS and want to preview drafts before they're published.

Was this helpful?

supported.

---

# Data Fetching

> Next.js allows you to fetch data in multiple ways, with pre-rendering, server-side rendering or static-site generation, and incremental static regeneration. Learn how to manage your application data in Next.js.

[Pages Router](https://nextjs.org/docs/pages)[Building Your Application](https://nextjs.org/docs/pages/building-your-application)Data FetchingYou are currently viewing the documentation for Pages Router.

# Data Fetching

Last updated  April 15, 2025

Data fetching in Next.js allows you to render your content in different ways, depending on your application's use case. These include pre-rendering with **Server-side Rendering** or **Static Generation**, and updating or creating content at runtime with **Incremental Static Regeneration**.

## Examples

- [Agility CMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-agilitycms) ([Demo](https://next-blog-agilitycms.vercel.app/))
- [Builder.io Example](https://github.com/vercel/next.js/tree/canary/examples/cms-builder-io) ([Demo](https://cms-builder-io.vercel.app/))
- [ButterCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-buttercms) ([Demo](https://next-blog-buttercms.vercel.app/))
- [Contentful Example](https://github.com/vercel/next.js/tree/canary/examples/cms-contentful) ([Demo](https://app-router-contentful.vercel.app/))
- [Cosmic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-cosmic) ([Demo](https://next-blog-cosmic.vercel.app/))
- [DatoCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-datocms) ([Demo](https://next-blog-datocms.vercel.app/))
- [DotCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-dotcms) ([Demo](https://nextjs-dotcms-blog.vercel.app/))
- [Drupal Example](https://github.com/vercel/next.js/tree/canary/examples/cms-drupal) ([Demo](https://cms-drupal.vercel.app/))
- [Enterspeed Example](https://github.com/vercel/next.js/tree/canary/examples/cms-enterspeed) ([Demo](https://next-blog-demo.enterspeed.com/))
- [GraphCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-graphcms) ([Demo](https://next-blog-graphcms.vercel.app/))
- [Keystone Example](https://github.com/vercel/next.js/tree/canary/examples/cms-keystonejs-embedded) ([Demo](https://nextjs-keystone-demo.vercel.app/))
- [Kontent.ai Example](https://github.com/vercel/next.js/tree/canary/examples/cms-kontent-ai) ([Demo](https://next-blog-kontent-ai.vercel.app/))
- [Makeswift Example](https://github.com/vercel/next.js/tree/canary/examples/cms-makeswift) ([Demo](https://nextjs-makeswift-example.vercel.app/))
- [Plasmic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-plasmic) ([Demo](https://nextjs-plasmic-example.vercel.app/))
- [Prepr Example](https://github.com/vercel/next.js/tree/canary/examples/cms-prepr) ([Demo](https://next-blog-prepr.vercel.app/))
- [Prismic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-prismic) ([Demo](https://next-blog-prismic.vercel.app/))
- [Sanity Example](https://github.com/vercel/next.js/tree/canary/examples/cms-sanity) ([Demo](https://next-blog.sanity.build/))
- [Sitecore XM Cloud Example](https://github.com/vercel/next.js/tree/canary/examples/cms-sitecore-xmcloud) ([Demo](https://vercel-sitecore-xmcloud-demo.vercel.app/))
- [Storyblok Example](https://github.com/vercel/next.js/tree/canary/examples/cms-storyblok) ([Demo](https://next-blog-storyblok.vercel.app/))
- [Strapi Example](https://github.com/vercel/next.js/tree/canary/examples/cms-strapi) ([Demo](https://next-blog-strapi.vercel.app/))
- [TakeShape Example](https://github.com/vercel/next.js/tree/canary/examples/cms-takeshape) ([Demo](https://next-blog-takeshape.vercel.app/))
- [Tina Example](https://github.com/vercel/next.js/tree/canary/examples/cms-tina) ([Demo](https://cms-tina-example.vercel.app/))
- [Umbraco Example](https://github.com/vercel/next.js/tree/canary/examples/cms-umbraco) ([Demo](https://nextjs-umbraco-sample-blog.vercel.app/))
- [Umbraco Heartcore Example](https://github.com/vercel/next.js/tree/canary/examples/cms-umbraco-heartcore) ([Demo](https://next-blog-umbraco-heartcore.vercel.app/))
- [Webiny Example](https://github.com/vercel/next.js/tree/canary/examples/cms-webiny) ([Demo](https://webiny-headlesscms-nextjs-example.vercel.app/))
- [WordPress Example](https://github.com/vercel/next.js/tree/canary/examples/cms-wordpress) ([Demo](https://next-blog-wordpress.vercel.app/))
- [Blog Starter Example](https://github.com/vercel/next.js/tree/canary/examples/blog-starter) ([Demo](https://next-blog-starter.vercel.app/))
- [Static Tweet (Demo)](https://react-tweet.vercel.app/)

[getStaticPropsFetch data and generate static pages with `getStaticProps`. Learn more about this API for data fetching in Next.js.](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props)[getStaticPathsFetch data and generate static pages with `getStaticPaths`. Learn more about this API for data fetching in Next.js.](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-paths)[Forms and MutationsLearn how to handle form submissions and data mutations with Next.js.](https://nextjs.org/docs/pages/building-your-application/data-fetching/forms-and-mutations)[getServerSidePropsFetch data on each request with `getServerSideProps`.](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props)[Client-side FetchingLearn about client-side data fetching, and how to use SWR, a data fetching React Hook library that handles caching, revalidation, focus tracking, refetching on interval and more.](https://nextjs.org/docs/pages/building-your-application/data-fetching/client-side)

Was this helpful?

supported.

---

# Automatic Static Optimization

> Next.js automatically optimizes your app to be static HTML whenever possible. Learn how it works here.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Rendering](https://nextjs.org/docs/pages/building-your-application/rendering)Automatic Static OptimizationYou are currently viewing the documentation for Pages Router.

# Automatic Static Optimization

Last updated  April 15, 2025

Next.js automatically determines that a page is static (can be prerendered) if it has no blocking data requirements. This determination is made by the absence of `getServerSideProps` and `getInitialProps` in the page.

This feature allows Next.js to emit hybrid applications that contain **both server-rendered and statically generated pages**.

> **Good to know**: Statically generated pages are still reactive. Next.js will hydrate your application client-side to give it full interactivity.

One of the main benefits of this feature is that optimized pages require no server-side computation, and can be instantly streamed to the end-user from multiple CDN locations. The result is an *ultra fast* loading experience for your users.

## How it works

If `getServerSideProps` or `getInitialProps` is present in a page, Next.js will switch to render the page on-demand, per-request (meaning [Server-Side Rendering](https://nextjs.org/docs/pages/building-your-application/rendering/server-side-rendering)).

If the above is not the case, Next.js will **statically optimize** your page automatically by prerendering the page to static HTML.

During prerendering, the router's `query` object will be empty since we do not have `query` information to provide during this phase. After hydration, Next.js will trigger an update to your application to provide the route parameters in the `query` object.

The cases where the query will be updated after hydration triggering another render are:

- The page is a [dynamic-route](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes).
- The page has query values in the URL.
- [Rewrites](https://nextjs.org/docs/pages/api-reference/config/next-config-js/rewrites) are configured in your `next.config.js` since these can have parameters that may need to be parsed and provided in the `query`.

To be able to distinguish if the query is fully updated and ready for use, you can leverage the `isReady` field on [next/router](https://nextjs.org/docs/pages/api-reference/functions/use-router#router-object).

> **Good to know**: Parameters added with [dynamic routes](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes) to a page that's using [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) will always be available inside the `query` object.

`next build` will emit `.html` files for statically optimized pages. For example, the result for the page `pages/about.js` would be:

 Terminal

```
.next/server/pages/about.html
```

And if you add `getServerSideProps` to the page, it will then be JavaScript, like so:

 Terminal

```
.next/server/pages/about.js
```

## Caveats

- If you have a [customApp](https://nextjs.org/docs/pages/building-your-application/routing/custom-app) with `getInitialProps` then this optimization will be turned off in pages without [Static Generation](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props).
- If you have a [customDocument](https://nextjs.org/docs/pages/building-your-application/routing/custom-document) with `getInitialProps` be sure you check if `ctx.req` is defined before assuming the page is server-side rendered. `ctx.req` will be `undefined` for pages that are prerendered.
- Avoid using the `asPath` value on [next/router](https://nextjs.org/docs/pages/api-reference/functions/use-router#router-object) in the rendering tree until the router's `isReady` field is `true`. Statically optimized pages only know `asPath` on the client and not the server, so using it as a prop may lead to mismatch errors. The [active-class-nameexample](https://github.com/vercel/next.js/tree/canary/examples/active-class-name) demonstrates one way to use `asPath` as a prop.

Was this helpful?

supported.

---

# Client

> Learn how to implement client-side rendering in the Pages Router.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Rendering](https://nextjs.org/docs/pages/building-your-application/rendering)Client-side Rendering (CSR)You are currently viewing the documentation for Pages Router.

# Client-side Rendering (CSR)

Last updated  June 6, 2025

In Client-Side Rendering (CSR) with React, the browser downloads a minimal HTML page and the JavaScript needed for the page. The JavaScript is then used to update the DOM and render the page. When the application is first loaded, the user may notice a slight delay before they can see the full page, this is because the page isn't fully rendered until all the JavaScript is downloaded, parsed, and executed.

After the page has been loaded for the first time, navigating to other pages on the same website is typically faster, as only necessary data needs to be fetched, and JavaScript can re-render parts of the page without requiring a full page refresh.

In Next.js, there are two ways you can implement client-side rendering:

1. Using React's `useEffect()` hook inside your pages instead of the server-side rendering methods ([getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) and [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props)).
2. Using a data fetching library like [SWR](https://swr.vercel.app/) or [TanStack Query](https://tanstack.com/query/latest/) to fetch data on the client (recommended).

Here's an example of using `useEffect()` inside a Next.js page:

 pages/index.js

```
import React, { useState, useEffect } from 'react'

export function Page() {
  const [data, setData] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('https://api.example.com/data')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const result = await response.json()
      setData(result)
    }

    fetchData().catch((e) => {
      // handle the error as needed
      console.error('An error occurred while fetching the data: ', e)
    })
  }, [])

  return <p>{data ? `Your data: ${data}` : 'Loading...'}</p>
}
```

In the example above, the component starts by rendering `Loading...`. Then, once the data is fetched, it re-renders and displays the data.

Although fetching data in a `useEffect` is a pattern you may see in older React Applications, we recommend using a data-fetching library for better performance, caching, optimistic updates, and more. Here's a minimum example using [SWR](https://swr.vercel.app/) to fetch data on the client:

 pages/index.js

```
import useSWR from 'swr'

export function Page() {
  const { data, error, isLoading } = useSWR(
    'https://api.example.com/data',
    fetcher
  )

  if (error) return <p>Failed to load.</p>
  if (isLoading) return <p>Loading...</p>

  return <p>Your Data: {data}</p>
}
```

> **Good to know**:
>
>
>
> Keep in mind that CSR can impact SEO. Some search engine crawlers might not execute JavaScript and therefore only see the initial empty or loading state of your application. It can also lead to performance issues for users with slower internet connections or devices, as they need to wait for all the JavaScript to load and run before they can see the full page. Next.js promotes a hybrid approach that allows you to use a combination of [server-side rendering](https://nextjs.org/docs/pages/building-your-application/rendering/server-side-rendering), [static site generation](https://nextjs.org/docs/pages/building-your-application/rendering/static-site-generation), and client-side rendering, **depending on the needs of each page** in your application. In the App Router, you can also use [Loading UI with Suspense](https://nextjs.org/docs/app/api-reference/file-conventions/loading) to show a loading indicator while the page is being rendered.

Learn about the alternative rendering methods in Next.js.[Server-side Rendering (SSR)Use Server-side Rendering to render pages on each request.](https://nextjs.org/docs/pages/building-your-application/rendering/server-side-rendering)[Static Site Generation (SSG)Use Static Site Generation (SSG) to pre-render pages at build time.](https://nextjs.org/docs/pages/building-your-application/rendering/static-site-generation)[ISRLearn how to create or update static pages at runtime with Incremental Static Regeneration.](https://nextjs.org/docs/pages/guides/incremental-static-regeneration)

Was this helpful?

supported.

---

# Server

> Use Server-side Rendering to render pages on each request.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Rendering](https://nextjs.org/docs/pages/building-your-application/rendering)Server-side Rendering (SSR)You are currently viewing the documentation for Pages Router.

# Server-side Rendering (SSR)

Last updated  April 15, 2025

> Also referred to as "SSR" or "Dynamic Rendering".

If a page uses **Server-side Rendering**, the page HTML is generated on **each request**.

To use Server-side Rendering for a page, you need to `export` an `async` function called `getServerSideProps`. This function will be called by the server on every request.

For example, suppose that your page needs to pre-render frequently updated data (fetched from an external API). You can write `getServerSideProps` which fetches this data and passes it to `Page` like below:

```
export default function Page({ data }) {
  // Render data...
}

// This gets called on every request
export async function getServerSideProps() {
  // Fetch data from external API
  const res = await fetch(`https://.../data`)
  const data = await res.json()

  // Pass data to the page via props
  return { props: { data } }
}
```

As you can see, `getServerSideProps` is similar to `getStaticProps`, but the difference is that `getServerSideProps` is run on every request instead of on build time.

To learn more about how `getServerSideProps` works, check out our [Data Fetching documentation](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props).

Was this helpful?

supported.

---

# Static Site Generation (SSG)

> Use Static Site Generation (SSG) to pre-render pages at build time.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Rendering](https://nextjs.org/docs/pages/building-your-application/rendering)Static Site Generation (SSG)You are currently viewing the documentation for Pages Router.

# Static Site Generation (SSG)

Last updated  April 15, 2025Examples

- [Agility CMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-agilitycms) ([Demo](https://next-blog-agilitycms.vercel.app/))
- [Builder.io Example](https://github.com/vercel/next.js/tree/canary/examples/cms-builder-io) ([Demo](https://cms-builder-io.vercel.app/))
- [ButterCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-buttercms) ([Demo](https://next-blog-buttercms.vercel.app/))
- [Contentful Example](https://github.com/vercel/next.js/tree/canary/examples/cms-contentful) ([Demo](https://app-router-contentful.vercel.app/))
- [Cosmic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-cosmic) ([Demo](https://next-blog-cosmic.vercel.app/))
- [DatoCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-datocms) ([Demo](https://next-blog-datocms.vercel.app/))
- [DotCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-dotcms) ([Demo](https://nextjs-dotcms-blog.vercel.app/))
- [Drupal Example](https://github.com/vercel/next.js/tree/canary/examples/cms-drupal) ([Demo](https://cms-drupal.vercel.app/))
- [Enterspeed Example](https://github.com/vercel/next.js/tree/canary/examples/cms-enterspeed) ([Demo](https://next-blog-demo.enterspeed.com/))
- [GraphCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-graphcms) ([Demo](https://next-blog-graphcms.vercel.app/))
- [Keystone Example](https://github.com/vercel/next.js/tree/canary/examples/cms-keystonejs-embedded) ([Demo](https://nextjs-keystone-demo.vercel.app/))
- [Kontent.ai Example](https://github.com/vercel/next.js/tree/canary/examples/cms-kontent-ai) ([Demo](https://next-blog-kontent-ai.vercel.app/))
- [Makeswift Example](https://github.com/vercel/next.js/tree/canary/examples/cms-makeswift) ([Demo](https://nextjs-makeswift-example.vercel.app/))
- [Plasmic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-plasmic) ([Demo](https://nextjs-plasmic-example.vercel.app/))
- [Prepr Example](https://github.com/vercel/next.js/tree/canary/examples/cms-prepr) ([Demo](https://next-blog-prepr.vercel.app/))
- [Prismic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-prismic) ([Demo](https://next-blog-prismic.vercel.app/))
- [Sanity Example](https://github.com/vercel/next.js/tree/canary/examples/cms-sanity) ([Demo](https://next-blog.sanity.build/))
- [Sitecore XM Cloud Example](https://github.com/vercel/next.js/tree/canary/examples/cms-sitecore-xmcloud) ([Demo](https://vercel-sitecore-xmcloud-demo.vercel.app/))
- [Storyblok Example](https://github.com/vercel/next.js/tree/canary/examples/cms-storyblok) ([Demo](https://next-blog-storyblok.vercel.app/))
- [Strapi Example](https://github.com/vercel/next.js/tree/canary/examples/cms-strapi) ([Demo](https://next-blog-strapi.vercel.app/))
- [TakeShape Example](https://github.com/vercel/next.js/tree/canary/examples/cms-takeshape) ([Demo](https://next-blog-takeshape.vercel.app/))
- [Tina Example](https://github.com/vercel/next.js/tree/canary/examples/cms-tina) ([Demo](https://cms-tina-example.vercel.app/))
- [Umbraco Example](https://github.com/vercel/next.js/tree/canary/examples/cms-umbraco) ([Demo](https://nextjs-umbraco-sample-blog.vercel.app/))
- [Umbraco Heartcore Example](https://github.com/vercel/next.js/tree/canary/examples/cms-umbraco-heartcore) ([Demo](https://next-blog-umbraco-heartcore.vercel.app/))
- [Webiny Example](https://github.com/vercel/next.js/tree/canary/examples/cms-webiny) ([Demo](https://webiny-headlesscms-nextjs-example.vercel.app/))
- [WordPress Example](https://github.com/vercel/next.js/tree/canary/examples/cms-wordpress) ([Demo](https://next-blog-wordpress.vercel.app/))
- [Blog Starter Example](https://github.com/vercel/next.js/tree/canary/examples/blog-starter) ([Demo](https://next-blog-starter.vercel.app/))
- [Static Tweet (Demo)](https://react-tweet.vercel.app/)

If a page uses **Static Generation**, the page HTML is generated at **build time**. That means in production, the page HTML is generated when you run `next build`. This HTML will then be reused on each request. It can be cached by a CDN.

In Next.js, you can statically generate pages **with or without data**. Let's take a look at each case.

### Static Generation without data

By default, Next.js pre-renders pages using Static Generation without fetching data. Here's an example:

```
function About() {
  return <div>About</div>
}

export default About
```

Note that this page does not need to fetch any external data to be pre-rendered. In cases like this, Next.js generates a single HTML file per page during build time.

### Static Generation with data

Some pages require fetching external data for pre-rendering. There are two scenarios, and one or both might apply. In each case, you can use these functions that Next.js provides:

1. Your page **content** depends on external data: Use `getStaticProps`.
2. Your page **paths** depend on external data: Use `getStaticPaths` (usually in addition to `getStaticProps`).

#### Scenario 1: Your page content depends on external data

**Example**: Your blog page might need to fetch the list of blog posts from a CMS (content management system).

```
// TODO: Need to fetch `posts` (by calling some API endpoint)
//       before this page can be pre-rendered.
export default function Blog({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li>{post.title}</li>
      ))}
    </ul>
  )
}
```

To fetch this data on pre-render, Next.js allows you to `export` an `async` function called `getStaticProps` from the same file. This function gets called at build time and lets you pass fetched data to the page's `props` on pre-render.

```
export default function Blog({ posts }) {
  // Render posts...
}

// This function gets called at build time
export async function getStaticProps() {
  // Call an external API endpoint to get posts
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  // By returning { props: { posts } }, the Blog component
  // will receive `posts` as a prop at build time
  return {
    props: {
      posts,
    },
  }
}
```

To learn more about how `getStaticProps` works, check out the [Data Fetching documentation](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props).

#### Scenario 2: Your page paths depend on external data

Next.js allows you to create pages with **dynamic routes**. For example, you can create a file called `pages/posts/[id].js` to show a single blog post based on `id`. This will allow you to show a blog post with `id: 1` when you access `posts/1`.

> To learn more about dynamic routing, check the [Dynamic Routing documentation](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes).

However, which `id` you want to pre-render at build time might depend on external data.

**Example**: suppose that you've only added one blog post (with `id: 1`) to the database. In this case, you'd only want to pre-render `posts/1` at build time.

Later, you might add the second post with `id: 2`. Then you'd want to pre-render `posts/2` as well.

So your page **paths** that are pre-rendered depend on external data. To handle this, Next.js lets you `export` an `async` function called `getStaticPaths` from a dynamic page (`pages/posts/[id].js` in this case). This function gets called at build time and lets you specify which paths you want to pre-render.

```
// This function gets called at build time
export async function getStaticPaths() {
  // Call an external API endpoint to get posts
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  // Get the paths we want to pre-render based on posts
  const paths = posts.map((post) => ({
    params: { id: post.id },
  }))

  // We'll pre-render only these paths at build time.
  // { fallback: false } means other routes should 404.
  return { paths, fallback: false }
}
```

Also in `pages/posts/[id].js`, you need to export `getStaticProps` so that you can fetch the data about the post with this `id` and use it to pre-render the page:

```
export default function Post({ post }) {
  // Render post...
}

export async function getStaticPaths() {
  // ...
}

// This also gets called at build time
export async function getStaticProps({ params }) {
  // params contains the post `id`.
  // If the route is like /posts/1, then params.id is 1
  const res = await fetch(`https://.../posts/${params.id}`)
  const post = await res.json()

  // Pass post data to the page via props
  return { props: { post } }
}
```

To learn more about how `getStaticPaths` works, check out the [Data Fetching documentation](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-paths).

### When should I use Static Generation?

We recommend using **Static Generation** (with and without data) whenever possible because your page can be built once and served by CDN, which makes it much faster than having a server render the page on every request.

You can use Static Generation for many types of pages, including:

- Marketing pages
- Blog posts and portfolios
- E-commerce product listings
- Help and documentation

You should ask yourself: "Can I pre-render this page **ahead** of a user's request?" If the answer is yes, then you should choose Static Generation.

On the other hand, Static Generation is **not** a good idea if you cannot pre-render a page ahead of a user's request. Maybe your page shows frequently updated data, and the page content changes on every request.

In cases like this, you can do one of the following:

- Use Static Generation with **Client-side data fetching:** You can skip pre-rendering some parts of a page and then use client-side JavaScript to populate them. To learn more about this approach, check out the [Data Fetching documentation](https://nextjs.org/docs/pages/building-your-application/data-fetching/client-side).
- Use **Server-Side Rendering:** Next.js pre-renders a page on each request. It will be slower because the page cannot be cached by a CDN, but the pre-rendered page will always be up-to-date. We'll talk about this approach below.

Was this helpful?

supported.
