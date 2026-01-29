# getServerSideProps and more

# getServerSideProps

> API reference for `getServerSideProps`. Learn how to fetch data on each request with Next.js.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)getServerSidePropsYou are currently viewing the documentation for Pages Router.

# getServerSideProps

Last updated  June 10, 2025

When exporting a function called `getServerSideProps` (Server-Side Rendering) from a page, Next.js will pre-render this page on each request using the data returned by `getServerSideProps`. This is useful if you want to fetch data that changes often, and have the page update to show the most current data.

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

You can import modules in top-level scope for use in `getServerSideProps`. Imports used will **not be bundled for the client-side**. This means you can write **server-side code directly ingetServerSideProps**, including fetching data from your database.

## Context parameter

The `context` parameter is an object containing the following keys:

| Name | Description |
| --- | --- |
| params | If this page uses adynamic route,paramscontains the route parameters. If the page name is[id].js, thenparamswill look like{ id: ... }. |
| req | TheHTTPIncomingMessage object, with an additionalcookiesprop, which is an object with string keys mapping to string values of cookies. |
| res | TheHTTPresponse object. |
| query | An object representing the query string, including dynamic route parameters. |
| preview | (Deprecated fordraftMode)previewistrueif the page is in thePreview Modeandfalseotherwise. |
| previewData | (Deprecated fordraftMode) Thepreviewdata set bysetPreviewData. |
| draftMode | draftModeistrueif the page is in theDraft Modeandfalseotherwise. |
| resolvedUrl | A normalized version of the requestURLthat strips the_next/dataprefix for client transitions and includes original query values. |
| locale | Contains the active locale (if enabled). |
| locales | Contains all supported locales (if enabled). |
| defaultLocale | Contains the configured default locale (if enabled). |

## getServerSideProps return values

The `getServerSideProps` function should return an object with **any one of the following** properties:

### props

The `props` object is a key-value pair, where each value is received by the page component. It should be a [serializable object](https://developer.mozilla.org/docs/Glossary/Serialization) so that any props passed, could be serialized with [JSON.stringify](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify).

```
export async function getServerSideProps(context) {
  return {
    props: { message: `Next.js is awesome` }, // will be passed to the page component as props
  }
}
```

### notFound

The `notFound` boolean allows the page to return a `404` status and [404 Page](https://nextjs.org/docs/pages/building-your-application/routing/custom-error#404-page). With `notFound: true`, the page will return a `404` even if there was a successfully generated page before. This is meant to support use cases like user-generated content getting removed by its author.

```
export async function getServerSideProps(context) {
  const res = await fetch(`https://.../data`)
  const data = await res.json()

  if (!data) {
    return {
      notFound: true,
    }
  }

  return {
    props: { data }, // will be passed to the page component as props
  }
}
```

### redirect

The `redirect` object allows redirecting to internal and external resources. It should match the shape of `{ destination: string, permanent: boolean }`. In some rare cases, you might need to assign a custom status code for older `HTTP` clients to properly redirect. In these cases, you can use the `statusCode` property instead of the `permanent` property, but not both.

```
export async function getServerSideProps(context) {
  const res = await fetch(`https://.../data`)
  const data = await res.json()

  if (!data) {
    return {
      redirect: {
        destination: '/',
        permanent: false,
      },
    }
  }

  return {
    props: {}, // will be passed to the page component as props
  }
}
```

## Version History

| Version | Changes |
| --- | --- |
| v13.4.0 | App Routeris now stable with simplified data fetching |
| v10.0.0 | locale,locales,defaultLocale, andnotFoundoptions added. |
| v9.3.0 | getServerSidePropsintroduced. |

Was this helpful?

supported.

---

# getStaticPaths

> API reference for `getStaticPaths`. Learn how to fetch data and generate static pages with `getStaticPaths`.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)getStaticPathsYou are currently viewing the documentation for Pages Router.

# getStaticPaths

Last updated  June 10, 2025

When exporting a function called `getStaticPaths` from a page that uses [Dynamic Routes](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes), Next.js will statically pre-render all the paths specified by `getStaticPaths`.

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

## getStaticPaths return values

The `getStaticPaths` function should return an object with the following **required** properties:

### paths

The `paths` key determines which paths will be pre-rendered. For example, suppose that you have a page that uses [Dynamic Routes](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes) named `pages/posts/[id].js`. If you export `getStaticPaths` from this page and return the following for `paths`:

```
return {
  paths: [
    { params: { id: '1' }},
    {
      params: { id: '2' },
      // with i18n configured the locale for the path can be returned as well
      locale: "en",
    },
  ],
  fallback: ...
}
```

Then, Next.js will statically generate `/posts/1` and `/posts/2` during `next build` using the page component in `pages/posts/[id].js`.

The value for each `params` object must match the parameters used in the page name:

- If the page name is `pages/posts/[postId]/[commentId]`, then `params` should contain `postId` and `commentId`.
- If the page name uses [catch-all routes](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes#catch-all-segments) like `pages/[...slug]`, then `params` should contain `slug` (which is an array). If this array is `['hello', 'world']`, then Next.js will statically generate the page at `/hello/world`.
- If the page uses an [optional catch-all route](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes#optional-catch-all-segments), use `null`, `[]`, `undefined` or `false` to render the root-most route. For example, if you supply `slug: false` for `pages/[[...slug]]`, Next.js will statically generate the page `/`.

The `params` strings are **case-sensitive** and ideally should be normalized to ensure the paths are generated correctly. For example, if `WoRLD` is returned for a param it will only match if `WoRLD` is the actual path visited, not `world` or `World`.

Separate of the `params` object a `locale` field can be returned when [i18n is configured](https://nextjs.org/docs/pages/guides/internationalization), which configures the locale for the path being generated.

### fallback: false

If `fallback` is `false`, then any paths not returned by `getStaticPaths` will result in a **404 page**.

When `next build` is run, Next.js will check if `getStaticPaths` returned `fallback: false`, it will then build **only** the paths returned by `getStaticPaths`. This option is useful if you have a small number of paths to create, or new page data is not added often. If you find that you need to add more paths, and you have `fallback: false`, you will need to run `next build` again so that the new paths can be generated.

The following example pre-renders one blog post per page called `pages/posts/[id].js`. The list of blog posts will be fetched from a CMS and returned by `getStaticPaths`. Then, for each page, it fetches the post data from a CMS using [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props).

 pages/posts/[id].js

```
function Post({ post }) {
  // Render post...
}

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

// This also gets called at build time
export async function getStaticProps({ params }) {
  // params contains the post `id`.
  // If the route is like /posts/1, then params.id is 1
  const res = await fetch(`https://.../posts/${params.id}`)
  const post = await res.json()

  // Pass post data to the page via props
  return { props: { post } }
}

export default Post
```

### fallback: true

 Examples

- [Static generation of a large number of pages](https://react-tweet.vercel.app/)

If `fallback` is `true`, then the behavior of `getStaticProps` changes in the following ways:

- The paths returned from `getStaticPaths` will be rendered to `HTML` at build time by `getStaticProps`.
- The paths that have not been generated at build time will **not** result in a 404 page. Instead, Next.js will serve a [“fallback”](#fallback-pages) version of the page on the first request to such a path. Web crawlers, such as Google, won't be served a fallback and instead the path will behave as in [fallback: 'blocking'](#fallback-blocking).
- When a page with `fallback: true` is navigated to through `next/link` or `next/router` (client-side) Next.js will *not* serve a fallback and instead the page will behave as [fallback: 'blocking'](#fallback-blocking).
- In the background, Next.js will statically generate the requested path `HTML` and `JSON`. This includes running `getStaticProps`.
- When complete, the browser receives the `JSON` for the generated path. This will be used to automatically render the page with the required props. From the user’s perspective, the page will be swapped from the fallback page to the full page.
- At the same time, Next.js adds this path to the list of pre-rendered pages. Subsequent requests to the same path will serve the generated page, like other pages pre-rendered at build time.

> **Good to know**: `fallback: true` is not supported when using [output: 'export'](https://nextjs.org/docs/pages/guides/static-exports).

#### When isfallback: trueuseful?

`fallback: true` is useful if your app has a very large number of static pages that depend on data (such as a very large e-commerce site). If you want to pre-render all product pages, the builds would take a very long time.

Instead, you may statically generate a small subset of pages and use `fallback: true` for the rest. When someone requests a page that is not generated yet, the user will see the page with a loading indicator or skeleton component.

Shortly after, `getStaticProps` finishes and the page will be rendered with the requested data. From now on, everyone who requests the same page will get the statically pre-rendered page.

This ensures that users always have a fast experience while preserving fast builds and the benefits of Static Generation.

`fallback: true` will not *update* generated pages, for that take a look at [Incremental Static Regeneration](https://nextjs.org/docs/pages/guides/incremental-static-regeneration).

### fallback: 'blocking'

If `fallback` is `'blocking'`, new paths not returned by `getStaticPaths` will wait for the `HTML` to be generated, identical to SSR (hence why *blocking*), and then be cached for future requests so it only happens once per path.

`getStaticProps` will behave as follows:

- The paths returned from `getStaticPaths` will be rendered to `HTML` at build time by `getStaticProps`.
- The paths that have not been generated at build time will **not** result in a 404 page. Instead, Next.js will SSR on the first request and return the generated `HTML`.
- When complete, the browser receives the `HTML` for the generated path. From the user’s perspective, it will transition from "the browser is requesting the page" to "the full page is loaded". There is no flash of loading/fallback state.
- At the same time, Next.js adds this path to the list of pre-rendered pages. Subsequent requests to the same path will serve the generated page, like other pages pre-rendered at build time.

`fallback: 'blocking'` will not *update* generated pages by default. To update generated pages, use [Incremental Static Regeneration](https://nextjs.org/docs/pages/guides/incremental-static-regeneration) in conjunction with `fallback: 'blocking'`.

> **Good to know**: `fallback: 'blocking'` is not supported when using [output: 'export'](https://nextjs.org/docs/pages/guides/static-exports).

### Fallback pages

In the “fallback” version of a page:

- The page’s props will be empty.
- Using the [router](https://nextjs.org/docs/pages/api-reference/functions/use-router), you can detect if the fallback is being rendered, `router.isFallback` will be `true`.

The following example showcases using `isFallback`:

 pages/posts/[id].js

```
import { useRouter } from 'next/router'

function Post({ post }) {
  const router = useRouter()

  // If the page is not yet generated, this will be displayed
  // initially until getStaticProps() finishes running
  if (router.isFallback) {
    return <div>Loading...</div>
  }

  // Render post...
}

// This function gets called at build time
export async function getStaticPaths() {
  return {
    // Only `/posts/1` and `/posts/2` are generated at build time
    paths: [{ params: { id: '1' } }, { params: { id: '2' } }],
    // Enable statically generating additional pages
    // For example: `/posts/3`
    fallback: true,
  }
}

// This also gets called at build time
export async function getStaticProps({ params }) {
  // params contains the post `id`.
  // If the route is like /posts/1, then params.id is 1
  const res = await fetch(`https://.../posts/${params.id}`)
  const post = await res.json()

  // Pass post data to the page via props
  return {
    props: { post },
    // Re-generate the post at most once per second
    // if a request comes in
    revalidate: 1,
  }
}

export default Post
```

## Version History

| Version | Changes |
| --- | --- |
| v13.4.0 | App Routeris now stable with simplified data fetching, includinggenerateStaticParams() |
| v12.2.0 | On-Demand Incremental Static Regenerationis stable. |
| v12.1.0 | On-Demand Incremental Static Regenerationadded (beta). |
| v9.5.0 | StableIncremental Static Regeneration |
| v9.3.0 | getStaticPathsintroduced. |

Was this helpful?

supported.

---

# getStaticProps

> API reference for `getStaticProps`. Learn how to use `getStaticProps` to generate static pages with Next.js.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)getStaticPropsYou are currently viewing the documentation for Pages Router.

# getStaticProps

Last updated  June 10, 2025

Exporting a function called `getStaticProps` will pre-render a page at build time using the props returned from the function:

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

You can import modules in top-level scope for use in `getStaticProps`. Imports used will **not be bundled for the client-side**. This means you can write **server-side code directly ingetStaticProps**, including fetching data from your database.

## Context parameter

The `context` parameter is an object containing the following keys:

| Name | Description |
| --- | --- |
| params | Contains the route parameters for pages usingdynamic routes. For example, if the page name is[id].js, thenparamswill look like{ id: ... }. You should use this together withgetStaticPaths, which we'll explain later. |
| preview | (Deprecated fordraftMode)previewistrueif the page is in thePreview Modeandfalseotherwise. |
| previewData | (Deprecated fordraftMode) Thepreviewdata set bysetPreviewData. |
| draftMode | draftModeistrueif the page is in theDraft Modeandfalseotherwise. |
| locale | Contains the active locale (if enabled). |
| locales | Contains all supported locales (if enabled). |
| defaultLocale | Contains the configured default locale (if enabled). |
| revalidateReason | Provides a reason for why the function was called. Can be one of: "build" (run at build time), "stale" (revalidate period expired, or running indevelopment mode), "on-demand" (triggered viaon-demand revalidation) |

## getStaticProps return values

The `getStaticProps` function should return an object containing either `props`, `redirect`, or `notFound` followed by an **optional** `revalidate` property.

### props

The `props` object is a key-value pair, where each value is received by the page component. It should be a [serializable object](https://developer.mozilla.org/docs/Glossary/Serialization) so that any props passed, could be serialized with [JSON.stringify](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify).

```
export async function getStaticProps(context) {
  return {
    props: { message: `Next.js is awesome` }, // will be passed to the page component as props
  }
}
```

### revalidate

The `revalidate` property is the amount in seconds after which a page re-generation can occur (defaults to `false` or no revalidation).

```
// This function gets called at build time on server-side.
// It may be called again, on a serverless function, if
// revalidation is enabled and a new request comes in
export async function getStaticProps() {
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  return {
    props: {
      posts,
    },
    // Next.js will attempt to re-generate the page:
    // - When a request comes in
    // - At most once every 10 seconds
    revalidate: 10, // In seconds
  }
}
```

Learn more about [Incremental Static Regeneration](https://nextjs.org/docs/pages/guides/incremental-static-regeneration).

The cache status of a page leveraging ISR can be determined by reading the value of the `x-nextjs-cache` response header. The possible values are the following:

- `MISS` - the path is not in the cache (occurs at most once, on the first visit)
- `STALE` - the path is in the cache but exceeded the revalidate time so it will be updated in the background
- `HIT` - the path is in the cache and has not exceeded the revalidate time

### notFound

The `notFound` boolean allows the page to return a `404` status and [404 Page](https://nextjs.org/docs/pages/building-your-application/routing/custom-error#404-page). With `notFound: true`, the page will return a `404` even if there was a successfully generated page before. This is meant to support use cases like user-generated content getting removed by its author. Note, `notFound` follows the same `revalidate` behavior [described here](#revalidate).

```
export async function getStaticProps(context) {
  const res = await fetch(`https://.../data`)
  const data = await res.json()

  if (!data) {
    return {
      notFound: true,
    }
  }

  return {
    props: { data }, // will be passed to the page component as props
  }
}
```

> **Good to know**: `notFound` is not needed for [fallback: false](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-false) mode as only paths returned from `getStaticPaths` will be pre-rendered.

### redirect

The `redirect` object allows redirecting to internal or external resources. It should match the shape of `{ destination: string, permanent: boolean }`.

In some rare cases, you might need to assign a custom status code for older `HTTP` clients to properly redirect. In these cases, you can use the `statusCode` property instead of the `permanent` property, **but not both**. You can also set `basePath: false` similar to redirects in `next.config.js`.

```
export async function getStaticProps(context) {
  const res = await fetch(`https://...`)
  const data = await res.json()

  if (!data) {
    return {
      redirect: {
        destination: '/',
        permanent: false,
        // statusCode: 301
      },
    }
  }

  return {
    props: { data }, // will be passed to the page component as props
  }
}
```

If the redirects are known at build-time, they should be added in [next.config.js](https://nextjs.org/docs/pages/api-reference/config/next-config-js/redirects) instead.

## Reading files: Useprocess.cwd()

Files can be read directly from the filesystem in `getStaticProps`.

In order to do so you have to get the full path to a file.

Since Next.js compiles your code into a separate directory you can't use `__dirname` as the path it returns will be different from the Pages Router.

Instead you can use `process.cwd()` which gives you the directory where Next.js is being executed.

```
import { promises as fs } from 'fs'
import path from 'path'

// posts will be populated at build time by getStaticProps()
function Blog({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li>
          <h3>{post.filename}</h3>
          <p>{post.content}</p>
        </li>
      ))}
    </ul>
  )
}

// This function gets called at build time on server-side.
// It won't be called on client-side, so you can even do
// direct database queries.
export async function getStaticProps() {
  const postsDirectory = path.join(process.cwd(), 'posts')
  const filenames = await fs.readdir(postsDirectory)

  const posts = filenames.map(async (filename) => {
    const filePath = path.join(postsDirectory, filename)
    const fileContents = await fs.readFile(filePath, 'utf8')

    // Generally you would parse/transform the contents
    // For example you can transform markdown to HTML here

    return {
      filename,
      content: fileContents,
    }
  })
  // By returning { props: { posts } }, the Blog component
  // will receive `posts` as a prop at build time
  return {
    props: {
      posts: await Promise.all(posts),
    },
  }
}

export default Blog
```

## Version History

| Version | Changes |
| --- | --- |
| v13.4.0 | App Routeris now stable with simplified data fetching |
| v12.2.0 | On-Demand Incremental Static Regenerationis stable. |
| v12.1.0 | On-Demand Incremental Static Regenerationadded (beta). |
| v10.0.0 | locale,locales,defaultLocale, andnotFoundoptions added. |
| v10.0.0 | fallback: 'blocking'return option added. |
| v9.5.0 | StableIncremental Static Regeneration |
| v9.3.0 | getStaticPropsintroduced. |

Was this helpful?

supported.

---

# NextRequest

> API Reference for NextRequest.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)NextRequestYou are currently viewing the documentation for Pages Router.

# NextRequest

Last updated  April 15, 2025

NextRequest extends the [Web Request API](https://developer.mozilla.org/docs/Web/API/Request) with additional convenience methods.

## cookies

Read or mutate the [Set-Cookie](https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie) header of the request.

### set(name, value)

Given a name, set a cookie with the given value on the request.

```
// Given incoming request /home
// Set a cookie to hide the banner
// request will have a `Set-Cookie:show-banner=false;path=/home` header
request.cookies.set('show-banner', 'false')
```

### get(name)

Given a cookie name, return the value of the cookie. If the cookie is not found, `undefined` is returned. If multiple cookies are found, the first one is returned.

```
// Given incoming request /home
// { name: 'show-banner', value: 'false', Path: '/home' }
request.cookies.get('show-banner')
```

### getAll()

Given a cookie name, return the values of the cookie. If no name is given, return all cookies on the request.

```
// Given incoming request /home
// [
//   { name: 'experiments', value: 'new-pricing-page', Path: '/home' },
//   { name: 'experiments', value: 'winter-launch', Path: '/home' },
// ]
request.cookies.getAll('experiments')
// Alternatively, get all cookies for the request
request.cookies.getAll()
```

### delete(name)

Given a cookie name, delete the cookie from the request.

```
// Returns true for deleted, false is nothing is deleted
request.cookies.delete('experiments')
```

### has(name)

Given a cookie name, return `true` if the cookie exists on the request.

```
// Returns true if cookie exists, false if it does not
request.cookies.has('experiments')
```

### clear()

Remove all cookies from the request.

```
request.cookies.clear()
```

## nextUrl

Extends the native [URL](https://developer.mozilla.org/docs/Web/API/URL) API with additional convenience methods, including Next.js specific properties.

```
// Given a request to /home, pathname is /home
request.nextUrl.pathname
// Given a request to /home?name=lee, searchParams is { 'name': 'lee' }
request.nextUrl.searchParams
```

The following options are available:

| Property | Type | Description |
| --- | --- | --- |
| basePath | string | Thebase pathof the URL. |
| buildId | string|undefined | The build identifier of the Next.js application. Can becustomized. |
| defaultLocale | string|undefined | The default locale forinternationalization. |
| domainLocale |  |  |
| -defaultLocale | string | The default locale within a domain. |
| -domain | string | The domain associated with a specific locale. |
| -http | boolean|undefined | Indicates if the domain is using HTTP. |
| locales | string[]|undefined | An array of available locales. |
| locale | string|undefined | The currently active locale. |
| url | URL | The URL object. |

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0 | ipandgeoremoved. |

Was this helpful?

supported.

---

# NextResponse

> API Reference for NextResponse.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)NextResponseYou are currently viewing the documentation for Pages Router.

# NextResponse

Last updated  April 15, 2025

NextResponse extends the [Web Response API](https://developer.mozilla.org/docs/Web/API/Response) with additional convenience methods.

## cookies

Read or mutate the [Set-Cookie](https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie) header of the response.

### set(name, value)

Given a name, set a cookie with the given value on the response.

```
// Given incoming request /home
let response = NextResponse.next()
// Set a cookie to hide the banner
response.cookies.set('show-banner', 'false')
// Response will have a `Set-Cookie:show-banner=false;path=/home` header
return response
```

### get(name)

Given a cookie name, return the value of the cookie. If the cookie is not found, `undefined` is returned. If multiple cookies are found, the first one is returned.

```
// Given incoming request /home
let response = NextResponse.next()
// { name: 'show-banner', value: 'false', Path: '/home' }
response.cookies.get('show-banner')
```

### getAll()

Given a cookie name, return the values of the cookie. If no name is given, return all cookies on the response.

```
// Given incoming request /home
let response = NextResponse.next()
// [
//   { name: 'experiments', value: 'new-pricing-page', Path: '/home' },
//   { name: 'experiments', value: 'winter-launch', Path: '/home' },
// ]
response.cookies.getAll('experiments')
// Alternatively, get all cookies for the response
response.cookies.getAll()
```

### has(name)

Given a cookie name, return `true` if the cookie exists on the response.

```
// Given incoming request /home
let response = NextResponse.next()
// Returns true if cookie exists, false if it does not
response.cookies.has('experiments')
```

### delete(name)

Given a cookie name, delete the cookie from the response.

```
// Given incoming request /home
let response = NextResponse.next()
// Returns true for deleted, false if nothing is deleted
response.cookies.delete('experiments')
```

## json()

Produce a response with the given JSON body.

 app/api/route.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
}
```

## redirect()

Produce a response that redirects to a [URL](https://developer.mozilla.org/docs/Web/API/URL).

```
import { NextResponse } from 'next/server'

return NextResponse.redirect(new URL('/new', request.url))
```

The [URL](https://developer.mozilla.org/docs/Web/API/URL) can be created and modified before being used in the `NextResponse.redirect()` method. For example, you can use the `request.nextUrl` property to get the current URL, and then modify it to redirect to a different URL.

```
import { NextResponse } from 'next/server'

// Given an incoming request...
const loginUrl = new URL('/login', request.url)
// Add ?from=/incoming-url to the /login URL
loginUrl.searchParams.set('from', request.nextUrl.pathname)
// And redirect to the new URL
return NextResponse.redirect(loginUrl)
```

## rewrite()

Produce a response that rewrites (proxies) the given [URL](https://developer.mozilla.org/docs/Web/API/URL) while preserving the original URL.

```
import { NextResponse } from 'next/server'

// Incoming request: /about, browser shows /about
// Rewritten request: /proxy, browser shows /about
return NextResponse.rewrite(new URL('/proxy', request.url))
```

## next()

The `next()` method is useful for Proxy, as it allows you to return early and continue routing.

```
import { NextResponse } from 'next/server'

return NextResponse.next()
```

You can also forward `headers` upstream when producing the response, using `NextResponse.next({ request: { headers } })`:

```
import { NextResponse } from 'next/server'

// Given an incoming request...
const newHeaders = new Headers(request.headers)
// Add a new header
newHeaders.set('x-version', '123')
// Forward the modified request headers upstream
return NextResponse.next({
  request: {
    // New request headers
    headers: newHeaders,
  },
})
```

This forwards `newHeaders` upstream to the target page, route, or server action, and does not expose them to the client. While this pattern is useful for passing data upstream, it should be used with caution because the headers containing this data may be forwarded to external services.

In contrast, `NextResponse.next({ headers })` is a shorthand for sending headers from proxy to the client. This is **NOT** good practice and should be avoided. Among other reasons because setting response headers like `Content-Type`, can override framework expectations (for example, the `Content-Type` used by Server Actions), leading to failed submissions or broken streaming responses.

```
import { type NextRequest, NextResponse } from 'next/server'

async function proxy(request: NextRequest) {
  const headers = await injectAuth(request.headers)
  // DO NOT forward headers like this
  return NextResponse.next({ headers })
}
```

In general, avoid copying all incoming request headers because doing so can leak sensitive data to clients or upstream services.

Prefer a defensive approach by creating a subset of incoming request headers using an allow-list. For example, you might discard custom `x-*` headers and only forward known-safe headers:

```
import { type NextRequest, NextResponse } from 'next/server'

function proxy(request: NextRequest) {
  const incoming = new Headers(request.headers)
  const forwarded = new Headers()

  for (const [name, value] of incoming) {
    const headerName = name.toLowerCase()
    // Keep only known-safe headers, discard custom x-* and other sensitive ones
    if (
      !headerName.startsWith('x-') &&
      headerName !== 'authorization' &&
      headerName !== 'cookie'
    ) {
      // Preserve original header name casing
      forwarded.set(name, value)
    }
  }

  return NextResponse.next({
    request: {
      headers: forwarded,
    },
  })
}
```

Was this helpful?

supported.

---

# useParams

> API Reference for the useParams hook in the Pages Router.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)useParamsYou are currently viewing the documentation for Pages Router.

# useParams

Last updated  January 14, 2026

`useParams` is a hook that lets you read a route's [dynamic params](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes) filled in by the current URL.

 pages/shop/[slug].tsxJavaScriptTypeScript

```
import { useParams } from 'next/navigation'

export default function ShopPage() {
  const params = useParams<{ slug: string }>()

  if (!params) {
    // Render fallback UI while params are not yet available
    return null
  }

  // Route -> /shop/[slug]
  // URL -> /shop/shoes
  // `params` -> { slug: 'shoes' }
  return <>Shop: {params.slug}</>
}
```

## Parameters

```
const params = useParams()
```

`useParams` does not take any parameters.

## Returns

`useParams` returns an object containing the current route's filled in [dynamic parameters](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes), or `null` during [pre-rendering](#behavior-during-pre-rendering).

- Each property in the object is an active dynamic segment.
- The property name is the segment's name, and the property value is what the segment is filled in with.
- The property value will either be a `string` or array of `string`s depending on the [type of dynamic segment](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes).
- If the route contains no dynamic parameters, `useParams` returns an empty object.

For example:

| Route | URL | useParams() |
| --- | --- | --- |
| pages/shop/page.js | /shop | {} |
| pages/shop/[slug].js | /shop/1 | { slug: '1' } |
| pages/shop/[tag]/[item].js | /shop/1/2 | { tag: '1', item: '2' } |
| pages/shop/[...slug].js | /shop/1/2 | { slug: ['1', '2'] } |

> **Good to know**: `useParams` is a [React Hook](https://react.dev/learn#using-hooks) and cannot be used with classes.

## Behavior

### Behavior during pre-rendering

For pages that are [statically optimized](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization), `useParams` will return `null` on the initial render. After hydration, the value will be updated to the actual params once the router is ready.

This is because params cannot be known during static generation for dynamic routes.

 pages/shop/[slug].tsxJavaScriptTypeScript

```
import { useParams } from 'next/navigation'

export default function ShopPage() {
  const params = useParams<{ slug: string }>()

  if (!params) {
    // Return a fallback UI while params are loading
    // This prevents hydration mismatches
    return <ShopPageSkeleton />
  }

  return <>Shop: {params.slug}</>
}
```

### Using withgetServerSideProps

When using [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props), the page is server-rendered on each request and `useParams` will return the actual params immediately:

 pages/shop/[slug].tsxJavaScriptTypeScript

```
import { useParams } from 'next/navigation'

export default function ShopPage() {
  const params = useParams<{ slug: string }>()

  // With getServerSideProps, this fallback is never rendered because
  // params is always available on the server. However, keeping
  // the fallback allows this component to be reused on other pages
  // that may not use getServerSideProps.
  if (!params) {
    return null
  }

  return <>Shop: {params.slug}</>
}

export async function getServerSideProps() {
  return { props: {} }
}
```

### Comparison withrouter.query

`useParams` only returns the dynamic route parameters, whereas [router.query](https://nextjs.org/docs/pages/api-reference/functions/use-router#router-object) from `useRouter` includes both dynamic parameters and query string parameters.

 pages/shop/[slug].tsxJavaScriptTypeScript

```
import { useRouter } from 'next/router'
import { useParams } from 'next/navigation'

export default function ShopPage() {
  const router = useRouter()
  const params = useParams()

  // URL -> /shop/shoes?color=red

  // router.query -> { slug: 'shoes', color: 'red' }
  // params -> { slug: 'shoes' }

  // ...
}
```

## Examples

### Sharing components with App Router

`useParams` from `next/navigation` works in both the Pages Router and App Router. This allows you to create shared components that work in either context:

 components/breadcrumb.tsxJavaScriptTypeScript

```
import { useParams } from 'next/navigation'

// This component works in both pages/ and app/
export function Breadcrumb() {
  const params = useParams<{ slug: string }>()

  if (!params) {
    // Fallback for Pages Router during pre-rendering
    return <nav>Home / ...</nav>
  }

  return <nav>Home / {params.slug}</nav>
}
```

> **Good to know**: When using this component in the App Router, `useParams` never returns `null`, so the fallback branch will not be rendered.

## Version History

| Version | Changes |
| --- | --- |
| v13.3.0 | useParamsintroduced. |

Was this helpful?

supported.

---

# useReportWebVitals

> useReportWebVitals

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)useReportWebVitalsYou are currently viewing the documentation for Pages Router.

# useReportWebVitals

Last updated  April 15, 2025

The `useReportWebVitals` hook allows you to report [Core Web Vitals](https://web.dev/vitals/), and can be used in combination with your analytics service.

New functions passed to `useReportWebVitals` are called with the available metrics up to that point. To prevent reporting duplicated data, ensure that the callback function reference does not change (as shown in the code examples below).

 pages/_app.js

```
import { useReportWebVitals } from 'next/web-vitals'

const logWebVitals = (metric) => {
  console.log(metric)
}

function MyApp({ Component, pageProps }) {
  useReportWebVitals(logWebVitals)

  return <Component {...pageProps} />
}
```

## useReportWebVitals

The `metric` object passed as the hook's argument consists of a number of properties:

- `id`: Unique identifier for the metric in the context of the current page load
- `name`: The name of the performance metric. Possible values include names of [Web Vitals](#web-vitals) metrics (TTFB, FCP, LCP, FID, CLS) specific to a web application.
- `delta`: The difference between the current value and the previous value of the metric. The value is typically in milliseconds and represents the change in the metric's value over time.
- `entries`: An array of [Performance Entries](https://developer.mozilla.org/docs/Web/API/PerformanceEntry) associated with the metric. These entries provide detailed information about the performance events related to the metric.
- `navigationType`: Indicates the [type of navigation](https://developer.mozilla.org/docs/Web/API/PerformanceNavigationTiming/type) that triggered the metric collection. Possible values include `"navigate"`, `"reload"`, `"back_forward"`, and `"prerender"`.
- `rating`: A qualitative rating of the metric value, providing an assessment of the performance. Possible values are `"good"`, `"needs-improvement"`, and `"poor"`. The rating is typically determined by comparing the metric value against predefined thresholds that indicate acceptable or suboptimal performance.
- `value`: The actual value or duration of the performance entry, typically in milliseconds. The value provides a quantitative measure of the performance aspect being tracked by the metric. The source of the value depends on the specific metric being measured and can come from various [Performance API](https://developer.mozilla.org/docs/Web/API/Performance_API)s.

## Web Vitals

[Web Vitals](https://web.dev/vitals/) are a set of useful metrics that aim to capture the user
experience of a web page. The following web vitals are all included:

- [Time to First Byte](https://developer.mozilla.org/docs/Glossary/Time_to_first_byte) (TTFB)
- [First Contentful Paint](https://developer.mozilla.org/docs/Glossary/First_contentful_paint) (FCP)
- [Largest Contentful Paint](https://web.dev/lcp/) (LCP)
- [First Input Delay](https://web.dev/fid/) (FID)
- [Cumulative Layout Shift](https://web.dev/cls/) (CLS)
- [Interaction to Next Paint](https://web.dev/inp/) (INP)

You can handle all the results of these metrics using the `name` property.

 pages/_app.js

```
import { useReportWebVitals } from 'next/web-vitals'

const handleWebVitals = (metric) => {
  switch (metric.name) {
    case 'FCP': {
      // handle FCP results
    }
    case 'LCP': {
      // handle LCP results
    }
    // ...
  }
}

function MyApp({ Component, pageProps }) {
  useReportWebVitals(handleWebVitals)

  return <Component {...pageProps} />
}
```

## Custom Metrics

In addition to the core metrics listed above, there are some additional custom metrics that
measure the time it takes for the page to hydrate and render:

- `Next.js-hydration`: Length of time it takes for the page to start and finish hydrating (in ms)
- `Next.js-route-change-to-render`: Length of time it takes for a page to start rendering after a
  route change (in ms)
- `Next.js-render`: Length of time it takes for a page to finish render after a route change (in ms)

You can handle all the results of these metrics separately:

pages/_app.js

```
import { useReportWebVitals } from 'next/web-vitals'

function handleCustomMetrics(metrics) {
  switch (metric.name) {
    case 'Next.js-hydration':
      // handle hydration results
      break
    case 'Next.js-route-change-to-render':
      // handle route-change to render results
      break
    case 'Next.js-render':
      // handle render results
      break
    default:
      break
  }
}

function MyApp({ Component, pageProps }) {
  useReportWebVitals(handleCustomMetrics)

  return <Component {...pageProps} />
}
```

These metrics work in all browsers that support the [User Timing API](https://caniuse.com/#feat=user-timing).

## Sending results to external systems

You can send results to any endpoint to measure and track
real user performance on your site. For example:

```
function postWebVitals(metrics) {
  const body = JSON.stringify(metric)
  const url = 'https://example.com/analytics'

  // Use `navigator.sendBeacon()` if available, falling back to `fetch()`.
  if (navigator.sendBeacon) {
    navigator.sendBeacon(url, body)
  } else {
    fetch(url, { body, method: 'POST', keepalive: true })
  }
}

useReportWebVitals(postWebVitals)
```

> **Good to know**: If you use [Google Analytics](https://analytics.google.com/analytics/web/), using the
> `id` value can allow you to construct metric distributions manually (to calculate percentiles,
> etc.)

> ```
> useReportWebVitals(metric => {
>   // Use `window.gtag` if you initialized Google Analytics as this example:
>   // https://github.com/vercel/next.js/blob/canary/examples/with-google-analytics
>   window.gtag('event', metric.name, {
>     value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value), // values must be integers
>     event_label: metric.id, // id unique to current page load
>     non_interaction: true, // avoids affecting bounce rate.
>   });
> }
> ```
>
>
>
> Read more about [sending results to Google Analytics](https://github.com/GoogleChrome/web-vitals#send-the-results-to-google-analytics).

Was this helpful?

supported.
