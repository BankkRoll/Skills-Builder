# Addressing "App Container Deprecated" Error in Next.js and more

# Addressing "App Container Deprecated" Error in Next.js

> This document guides developers on how to resolve the "App Container Deprecated" error in Next.js by updating their custom App component.

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Addressing "App Container Deprecated" Error in Next.js

# Addressing "App Container Deprecated" Error in Next.js

This document guides developers on how to resolve the "App Container Deprecated" error in Next.js by updating their custom App component.

## Why This Error Occurred

The "App Container Deprecated" error usually occurs when you are using the `<Container>` component in your custom `<App>` (`pages/_app.js`). Prior to version `9.0.4` of Next.js, the `<Container>` component was used to handle scrolling to hashes.

From version `9.0.4` onwards, this functionality was moved up the component tree, rendering the `<Container>` component unnecessary in your custom `<App>`.

## Possible Ways to Fix It

To resolve this issue, you need to remove the `<Container>` component from your custom `<App>` (`pages/_app.js`).

**Before**

 pages/_app.js

```
import React from 'react'
import App, { Container } from 'next/app'

class MyApp extends App {
  render() {
    const { Component, pageProps } = this.props
    return (
      <Container>
        <Component {...pageProps} />
      </Container>
    )
  }
}

export default MyApp
```

**After**

 pages/_app.js

```
import React from 'react'
import App from 'next/app'

class MyApp extends App {
  render() {
    const { Component, pageProps } = this.props
    return <Component {...pageProps} />
  }
}

export default MyApp
```

After making this change, your custom `<App>` should work as expected without the `<Container>` component.

## Useful Links

- [Custom App](https://nextjs.org/docs/pages/building-your-application/routing/custom-app)

Was this helpful?

supported.

---

# Uncached data was accessed outside of `<Suspense>`

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Uncached data was accessed outside of `<Suspense>`

# Uncached data was accessed outside of `<Suspense>`

## Why This Error Occurred

When the `cacheComponents` feature is enabled, Next.js expects a parent `Suspense` boundary around any component that awaits data that should be accessed on every user request. The purpose of this requirement is so that Next.js can provide a useful fallback while this data is accessed and rendered.

While some data is inherently only available when a user request is being handled, such as request headers, Next.js assumes that by default any asynchronous data is expected to be accessed each time a user request is being handled unless you specifically cache it using `"use cache"`.

The proper fix for this specific error depends on what data you are accessing and how you want your Next.js app to behave.

## Possible Ways to Fix It

### Accessing Data

When you access data using `fetch`, a database client, or any other module which does asynchronous IO, Next.js interprets your intent as expecting the data to load on every user request.

If you are expecting this data to be used while fully or partially prerendering a page you must cache is using `"use cache"`.

Before:

 app/page.js

```
async function getRecentArticles() {
  return db.query(...)
}

export default async function Page() {
  const articles = await getRecentArticles(token);
  return <ArticleList articles={articles}>
}
```

After:

 app/page.js

```
import { cacheTag, cacheLife } from 'next/cache'

async function getRecentArticles() {
  "use cache"
  // This cache can be revalidated by webhook or server action
  // when you call revalidateTag("articles")
  cacheTag("articles")
  // This cache will revalidate after an hour even if no explicit
  // revalidate instruction was received
  cacheLife('hours')
  return db.query(...)
}

export default async function Page() {
  const articles = await getRecentArticles(token);
  return <ArticleList articles={articles}>
}
```

If this data should be accessed on every user request you must provide a fallback UI using `Suspense` from React. Where you put this Suspense boundary in your application should be informed by the kind of fallback UI you want to render. It can be immediately above the component accessing this data or even in your Root Layout.

Before:

 app/page.js

```
async function getLatestTransactions() {
  return db.query(...)
}

export default async function Page() {
  const transactions = await getLatestTransactions(token);
  return <TransactionList transactions={transactions}>
}
```

After:

 app/page.js

```
import { Suspense } from 'react'

async function TransactionList() {
  const transactions = await db.query(...)
  return ...
}

function TransactionSkeleton() {
  return <ul>...</ul>
}

export default async function Page() {
  return (
    <Suspense fallback={<TransactionSkeleton />}>
      <TransactionList/>
    </Suspense>
  )
}
```

### Headers

If you are accessing request headers using `headers()`, `cookies()`, or `draftMode()`. Consider whether you can move the use of these APIs deeper into your existing component tree.

Before:

 app/inbox.js

```
export async function Inbox({ token }) {
  const email = await getEmail(token)
  return (
    <ul>
      {email.map((e) => (
        <EmailRow key={e.id} />
      ))}
    </ul>
  )
}
```

 app/page.js

```
import { cookies } from 'next/headers'

import { Inbox } from './inbox'

export default async function Page() {
  const token = (await cookies()).get('token')
  return (
    <Suspense fallback="loading your inbox...">
      <Inbox token={token}>
    </Suspense>
  )
}
```

After:

 app/inbox.js

```
import { cookies } from 'next/headers'

export async function Inbox() {
  const token = (await cookies()).get('token')
  const email = await getEmail(token)
  return (
    <ul>
      {email.map((e) => (
        <EmailRow key={e.id} />
      ))}
    </ul>
  )
}
```

 app/page.js

```
import { Inbox } from './inbox'

export default async function Page() {
  return (
    <Suspense fallback="loading your inbox...">
      <Inbox>
    </Suspense>
  )
}
```

Alternatively you can add a Suspense boundary above the component that is accessing Request headers.

### Params and SearchParams

Layout `params`, and Page `params` and `searchParams` props are promises. If you await them in the Layout or Page component you might be accessing these props higher than is actually required. Try passing these props to deeper components as a promise and awaiting them closer to where the actual param or searchParam is required

Before:

 app/map.js

```
export async function Map({ lat, lng }) {
  const mapData = await fetch(`https://...?lat=${lat}&lng=${lng}`)
  return drawMap(mapData)
}
```

 app/page.js

```
import { cookies } from 'next/headers'

import { Map } from './map'

export default async function Page({ searchParams }) {
  const { lat, lng } = await searchParams;
  return (
    <Suspense fallback="loading your inbox...">
      <Map lat={lat} lng={lng}>
    </Suspense>
  )
}
```

After:

 app/map.js

```
export async function Map({ coords }) {
  const { lat, lng } = await coords
  const mapData = await fetch(`https://...?lat=${lat}&lng=${lng}`)
  return drawMap(mapData)
}
```

 app/page.js

```
import { cookies } from 'next/headers'

import { Map } from './map'

export default async function Page({ searchParams }) {
  const coords = searchParams.then(sp => ({ lat: sp.lat, lng: sp.lng }))
  return (
    <Suspense fallback="loading your inbox...">
      <Map coord={coords}>
    </Suspense>
  )
}
```

Alternatively you can add a Suspense boundary above the component that is accessing `params` or `searchParams` so Next.js understands what UI should be used when while waiting for this request data to be accessed.

#### generateStaticParams

For Layout and Page `params`, you can use [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params) to provide sample values for build-time validation, which allows you to await params directly without Suspense.

 app/blog/[slug]/page.js

```
export async function generateStaticParams() {
  return [{ slug: 'hello-world' }]
}

export default async function Page({ params }) {
  const { slug } = await params //  Valid with generateStaticParams
  return <div>Blog post: {slug}</div>
}
```

Note that validation is path-dependent. Runtime parameters may trigger conditional branches accessing runtime APIs without Suspense, or dynamic content without Suspense or `use cache`, resulting in errors. See [Dynamic Routes with Cache Components](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#with-cache-components).

### Short-lived Caches

`"use cache"` allows you to describe a [cacheLife()](https://nextjs.org/docs/app/api-reference/functions/cacheLife) that might be too short to be practical to prerender. The utility of doing this is that it can still describe a non-zero caching time for the client router cache to reuse the cache entry in the browser and it can also be useful for protecting upstream APIs while experiencing high request traffic.

If you expected the `"use cache"` entry to be prerenderable try describing a slightly longer `cacheLife()`.

Before:

 app/page.js

```
import { cacheLife } from 'next/cache'

async function getDashboard() {
  "use cache"
  // This cache will revalidate after 1 second. It is so short
  // Next.js won't prerender it on the server but the client router
  // can reuse the result for up to 30 seconds unless the user manually refreshes
  cacheLife('seconds')
  return db.query(...)
}

export default async function Page() {
  const data = await getDashboard(token);
  return <Dashboard data={data}>
}
```

After:

 app/page.js

```
import { cacheLife } from 'next/cache'

async function getDashboard() {
  "use cache"
  // This cache will revalidate after 1 minute. It's long enough that
  // Next.js will still produce a fully or partially prerendered page
  cacheLife('minutes')
  return db.query(...)
}

export default async function Page() {
  const data = await getDashboard(token);
  return <Dashboard data={data}>
}
```

Alternatively you can add a Suspense boundary above the component that is accessing this short-lived cached data so Next.js understands what UI should be used while accessing this data on a user request.

## Useful Links

- [SuspenseReact API](https://react.dev/reference/react/Suspense)
- [headersfunction](https://nextjs.org/docs/app/api-reference/functions/headers)
- [cookiesfunction](https://nextjs.org/docs/app/api-reference/functions/cookies)
- [draftModefunction](https://nextjs.org/docs/app/api-reference/functions/draft-mode)
- [connectionfunction](https://nextjs.org/docs/app/api-reference/functions/connection)
- [cacheLifefunction](https://nextjs.org/docs/app/api-reference/functions/cacheLife)
- [cacheTagfunction](https://nextjs.org/docs/app/api-reference/functions/cacheTag)

Was this helpful?

supported.

---

# Conflicting Public File and Page File

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Conflicting Public File and Page File

# Conflicting Public File and Page File

## Why This Error Occurred

One of your public files has the same path as a page file which is not supported. Since only one resource can reside at the URL both public files and page files must be unique.

## Possible Ways to Fix It

Rename either the public file or page file that is causing the conflict.

Example conflict between public file and page file

 Folder structure

```
public/
  hello
pages/
  hello.js
```

Non-conflicting public file and page file

 Folder structure

```
public/
  hello.txt
pages/
  hello.js
```

## Useful Links

- [Static file serving docs](https://nextjs.org/docs/pages/api-reference/file-conventions/public-folder)

Was this helpful?

supported.

---

# Empty generateStaticParams with Cache Components

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Empty generateStaticParams with Cache Components

# Empty generateStaticParams with Cache Components

## Why This Error Occurred

You're using [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) in your Next.js application, and one of your `generateStaticParams` functions returned an empty array, which causes a build error.

When Cache Components is enabled, Next.js performs build-time validation to ensure your routes can be properly prerendered without runtime dynamic access errors. If `generateStaticParams` returns an empty array, Next.js cannot validate that your route won't access dynamic values (like `await cookies()`, `await headers()`, or `await searchParams`) at runtime, which would cause errors.

This strict requirement ensures:

- Build-time validation catches potential runtime errors early
- All routes using Cache Components have at least one static variant to validate against
- You don't accidentally deploy routes that will fail at runtime

## Possible Ways to Fix It

### Option 1: Return at least one static param

Modify your `generateStaticParams` function to return at least one set of parameters. This is the most common fix and allows build-time validation to work properly.

 app/blog/[slug]/page.tsx

```
// This will cause an error with Cache Components
export async function generateStaticParams() {
  return [] // Empty array not allowed
}

// Return at least one sample param
export async function generateStaticParams() {
  return [{ slug: 'hello-world' }, { slug: 'getting-started' }]
}
```

These samples serve dual purposes:

1. **Build-time validation**: Verify your route structure is safe
2. **Prerendering**: Generate instant-loading pages for popular routes

The build process only validates code paths that execute with your sample params. If runtime parameters trigger conditional logic that renders branches accessing runtime APIs (like `cookies()`) without Suspense, or dynamic content without Suspense or `use cache`, those will cause runtime errors.

### Option 2: Use a placeholder param

If you don't know actual values at build time, you can use a placeholder for validation. However, this defeats the purpose of build-time validation and should be avoided:

 app/blog/[slug]/page.tsx

```
export async function generateStaticParams() {
  // Placeholder only validates one code path
  return [{ slug: '__placeholder__' }]
}

export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params

  // Handle placeholder case
  if (slug === '__placeholder__') {
    notFound()
  }

  // Real params may trigger code paths
  // that access dynamic APIs incorrectly, causing
  // runtime errors that cannot be caught by error boundaries
  const post = await getPost(slug)
  return <div>{post.title}</div>
}
```

Using placeholders provides minimal build-time validation and increases the risk of runtime errors for actual parameter values.

## Useful Links

- [Cache Components Documentation](https://nextjs.org/docs/app/getting-started/cache-components)
- [generateStaticParams API Reference](https://nextjs.org/docs/app/api-reference/functions/generate-static-params)
- [Dynamic Routes with Cache Components](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#with-cache-components)

Was this helpful?

supported.

---

# Google Font Display

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Google Font Display

# Google Font Display

> Enforce font-display behavior with Google Fonts.

## Why This Error Occurred

For a Google Font, the font-display descriptor was either missing or set to `auto`, `block`, or `fallback`, which are not recommended.

## Possible Ways to Fix It

For most cases, the best font display strategy for custom fonts is `optional`.

 pages/index.js

```
import Head from 'next/head'

export default function IndexPage() {
  return (
    <div>
      <Head>
        <link
          href="https://fonts.googleapis.com/css2?family=Krona+One&display=optional"
          rel="stylesheet"
        />
      </Head>
    </div>
  )
}
```

Specifying `display=optional` minimizes the risk of invisible text or layout shift. If swapping to the custom font after it has loaded is important to you, then use `display=swap` instead.

### When Not To Use It

If you want to specifically display a font using an `auto`, `block`, or `fallback` strategy, then you can disable this rule.

## Useful Links

- [Controlling Font Performance with font-display](https://developer.chrome.com/blog/font-display/)
- [Google Fonts API Docs](https://developers.google.com/fonts/docs/css2#use_font-display)
- [CSSfont-displayproperty](https://www.w3.org/TR/css-fonts-4/#font-display-desc)

Was this helpful?

supported.

---

# Google Font Preconnect

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Google Font Preconnect

# Google Font Preconnect

> **Note**: Next.js automatically adds `<link rel="preconnect" />` after version `12.0.1`.

> Ensure `preconnect` is used with Google Fonts.

## Why This Error Occurred

A preconnect resource hint was not used with a request to the Google Fonts domain. Adding `preconnect` is recommended to initiate an early connection to the origin.

## Possible Ways to Fix It

Add `rel="preconnect"` to the Google Font domain `<link>` tag:

 pages/_document.js

```
<link rel="preconnect" href="https://fonts.gstatic.com" />
```

> **Note**: a **separate** link with `dns-prefetch` can be used as a fallback for browsers that don't support `preconnect` although this is not required.

## Useful Links

- [Preconnect to required origins](https://web.dev/uses-rel-preconnect/)
- [Preconnect and dns-prefetch](https://web.dev/preconnect-and-dns-prefetch/#resolve-domain-name-early-with-reldns-prefetch)
- [Next.js Font Optimization](https://nextjs.org/docs/pages/api-reference/components/font)

Was this helpful?

supported.

---

# Inline script id

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Inline script id

# Inline script id

> Enforce `id` attribute on `next/script` components with inline content.

## Why This Error Occurred

`next/script` components with inline content require an `id` attribute to be defined to track and optimize the script.

## Possible Ways to Fix It

Add an `id` attribute to the `next/script` component.

 pages/_app.js

```
import Script from 'next/script'

export default function App({ Component, pageProps }) {
  return (
    <>
      <Script id="my-script">{`console.log('Hello world!');`}</Script>
      <Component {...pageProps} />
    </>
  )
}
```

## Useful links

- [Docs for Next.js Script component](https://nextjs.org/docs/pages/guides/scripts)

Was this helpful?

supported.

---

# Middleware Upgrade Guide

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Middleware Upgrade Guide

# Middleware Upgrade Guide

As we work on improving Middleware for General Availability (GA), we've made some changes to the Middleware APIs (and how you define Middleware in your application) based on your feedback.

This upgrade guide will help you understand the changes, why they were made, and how to migrate your existing Middleware to the new API. The guide is for Next.js developers who:

- Currently use the beta Next.js Middleware features
- Choose to upgrade to the next stable version of Next.js (`v12.2`)

You can start upgrading your Middleware usage today with the latest release (`npm i next@latest`).

> **Note**: These changes described in this guide are included in Next.js `12.2`. You can keep your current site structure, including nested Middleware, until you move to `12.2` (or a `canary` build of Next.js).

If you have ESLint configured, you will need to run `npm i eslint-config-next@latest --save-dev` to upgrade your ESLint configuration to ensure the same version is being used as the Next.js version. You might also need to restart VSCode for the changes to take effect.

## Using Next.js Middleware on Vercel

If you're using Next.js on Vercel, your existing deploys using Middleware will continue to work, and you can continue to deploy your site using Middleware. When you upgrade your site to the next stable version of Next.js (`v12.2`), you will need to follow this upgrade guide to update your Middleware.

## Breaking changes

1. [No Nested Middleware](#no-nested-middleware)
2. [No Response Body](#no-response-body)
3. [Cookies API Revamped](#cookies-api-revamped)
4. [New User-Agent Helper](#new-user-agent-helper)
5. [No More Page Match Data](#no-more-page-match-data)
6. [Executing Middleware on Internal Next.js Requests](#executing-middleware-on-internal-nextjs-requests)

## No Nested Middleware

### Summary of changes

- Define a single Middleware file next to your `pages` folder
- No need to prefix the file with an underscore
- A custom matcher can be used to define matching routes using an exported config object

### Explanation

Previously, you could create a `_middleware.ts` file under the `pages` directory at any level. Middleware execution was based on the file path where it was created.

Based on customer feedback, we have replaced this API with a single root Middleware, which provides the following improvements:

- **Faster execution with lower latency**: With nested Middleware, a single request could invoke multiple Middleware functions. A single Middleware means a single function execution, which is more efficient.
- **Less expensive**: Middleware usage is billed per invocation. Using nested Middleware, a single request could invoke multiple Middleware functions, meaning multiple Middleware charges per request. A single Middleware means a single invocation per request and is more cost effective.
- **Middleware can conveniently filter on things besides routes**: With nested Middleware, the Middleware files were located in the `pages` directory and Middleware was executed based on request paths. By moving to a single root Middleware, you can still execute code based on request paths, but you can now more conveniently execute Middleware based on other conditions, like `cookies` or the presence of a request header.
- **Deterministic execution ordering**: With nested Middleware, a single request could match multiple Middleware functions. For example, a request to `/dashboard/users/*` would invoke Middleware defined in both `/dashboard/users/_middleware.ts` and `/dashboard/_middleware.js`. However, the execution order is difficult to reason about. Moving to a single, root Middleware more explicitly defines execution order.
- **Supports Next.js Layouts (RFC)**: Moving to a single, root Middleware helps support the new [Layouts (RFC) in Next.js](https://nextjs.org/blog/layouts-rfc).

### How to upgrade

You should declare **one single Middleware file** in your application, which should be located next to the `pages` directory and named **without** an `_` prefix. Your Middleware file can still have either a `.ts` or `.js` extension.

Middleware will be invoked for **every route in the app**, and a custom matcher can be used to define matching filters. The following is an example for a Middleware that triggers for `/about/*` and `/dashboard/:path*`, the custom matcher is defined in an exported config object:

 middleware.ts

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  return NextResponse.rewrite(new URL('/about-2', request.url))
}

// Supports both a single string value or an array of matchers
export const config = {
  matcher: ['/about/:path*', '/dashboard/:path*'],
}
```

The matcher config also allows full regex so matching like negative lookaheads or character matching is supported. An example of a negative lookahead to match all except specific paths can be seen here:

 middleware.ts

```
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|favicon.ico).*)',
  ],
}
```

While the config option is preferred since it doesn't get invoked on every request, you can also use conditional statements to only run the Middleware when it matches specific paths. One advantage of using conditionals is defining explicit ordering for when Middleware executes. The following example shows how you can merge two previously nested Middleware:

 middleware.ts

```
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/about')) {
    // This logic is only applied to /about
  }

  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    // This logic is only applied to /dashboard
  }
}
```

## No Response Body

### Summary of changes

- Middleware can no longer produce a response body
- If your Middleware *does* respond with a body, a runtime error will be thrown
- Migrate to using `rewrite`/`redirect` to pages/APIs handling a response

### Explanation

To respect the differences in client-side and server-side navigation, and to help ensure that developers do not build insecure Middleware, we are removing the ability to send response bodies in Middleware. This ensures that Middleware is only used to `rewrite`, `redirect`, or modify the incoming request (e.g. [setting cookies](#cookies-api-revamped)).

The following patterns will no longer work:

```
new Response('a text value')
new Response(streamOrBuffer)
new Response(JSON.stringify(obj), { headers: 'application/json' })
NextResponse.json()
```

### How to upgrade

For cases where Middleware is used to respond (such as authorization), you should migrate to use `rewrite`/`redirect` to pages that show an authorization error, login forms, or to an API Route.

#### Before

 pages/_middleware.ts

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { isAuthValid } from './lib/auth'

export function middleware(request: NextRequest) {
  // Example function to validate auth
  if (isAuthValid(request)) {
    return NextResponse.next()
  }

  return NextResponse.json({ message: 'Auth required' }, { status: 401 })
}
```

#### After

 middleware.ts

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { isAuthValid } from './lib/auth'

export function middleware(request: NextRequest) {
  // Example function to validate auth
  if (isAuthValid(request)) {
    return NextResponse.next()
  }

  const loginUrl = new URL('/login', request.url)
  loginUrl.searchParams.set('from', request.nextUrl.pathname)

  return NextResponse.redirect(loginUrl)
}
```

#### Edge API Routes

If you were previously using Middleware to forward headers to an external API, you can now use [Edge API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes):

 pages/api/proxy.ts

```
import { type NextRequest } from 'next/server'

export const config = {
  runtime: 'edge',
}

export default async function handler(req: NextRequest) {
  const authorization = req.cookies.get('authorization')
  return fetch('https://backend-api.com/api/protected', {
    method: req.method,
    headers: {
      authorization,
    },
    redirect: 'manual',
  })
}
```

## Cookies API Revamped

### Summary of changes

| Added | Removed |
| --- | --- |
| cookies.set | cookie |
| cookies.delete | clearCookie |
| cookies.getWithOptions | cookies |

### Explanation

Based on beta feedback, we are changing the Cookies API in `NextRequest` and `NextResponse` to align more to a `get`/`set` model. The `Cookies` API extends Map, including methods like [entries](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Map/entries) and [values](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Map/entries).

### How to upgrade

`NextResponse` now has a `cookies` instance with:

- `cookies.delete`
- `cookies.set`
- `cookies.getWithOptions`

As well as other extended methods from `Map`.

#### Before

 pages/_middleware.ts

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // create an instance of the class to access the public methods. This uses `next()`,
  // you could use `redirect()` or `rewrite()` as well
  let response = NextResponse.next()
  // get the cookies from the request
  let cookieFromRequest = request.cookies['my-cookie']
  // set the `cookie`
  response.cookie('hello', 'world')
  // set the `cookie` with options
  const cookieWithOptions = response.cookie('hello', 'world', {
    path: '/',
    maxAge: 1000 * 60 * 60 * 24 * 7,
    httpOnly: true,
    sameSite: 'strict',
    domain: 'example.com',
  })
  // clear the `cookie`
  response.clearCookie('hello')

  return response
}
```

#### After

 middleware.ts

```
export function middleware() {
  const response = new NextResponse()

  // set a cookie
  response.cookies.set('vercel', 'fast')

  // set another cookie with options
  response.cookies.set('nextjs', 'awesome', { path: '/test' })

  // get all the details of a cookie
  const { value, ...options } = response.cookies.getWithOptions('vercel')
  console.log(value) // => 'fast'
  console.log(options) // => { name: 'vercel', Path: '/test' }

  // deleting a cookie will mark it as expired
  response.cookies.delete('vercel')

  return response
}
```

## New User-Agent Helper

### Summary of changes

- Accessing the user agent is no longer available on the request object
- We've added a new `userAgent` helper to reduce Middleware size by `17kb`

### Explanation

To help reduce the size of your Middleware, we have extracted the user agent from the request object and created a new helper `userAgent`.

The helper is imported from `next/server` and allows you to opt in to using the user agent. The helper gives you access to the same properties that were available from the request object.

### How to upgrade

- Import the `userAgent` helper from `next/server`
- Destructure the properties you need to work with

#### Before

 pages/_middleware.ts

```
import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const url = request.nextUrl
  const viewport = request.ua.device.type === 'mobile' ? 'mobile' : 'desktop'
  url.searchParams.set('viewport', viewport)
  return NextResponse.rewrite(url)
}
```

#### After

 middleware.ts

```
import { NextRequest, NextResponse, userAgent } from 'next/server'

export function middleware(request: NextRequest) {
  const url = request.nextUrl
  const { device } = userAgent(request)
  const viewport = device.type === 'mobile' ? 'mobile' : 'desktop'
  url.searchParams.set('viewport', viewport)
  return NextResponse.rewrite(url)
}
```

## No More Page Match Data

### Summary of changes

- Use [URLPattern](https://developer.mozilla.org/docs/Web/API/URLPattern) to check if a Middleware is being invoked for a certain page match

### Explanation

Currently, Middleware estimates whether you are serving an asset of a Page based on the Next.js routes manifest (internal configuration). This value is surfaced through `request.page`.

To make page and asset matching more accurate, we are now using the web standard `URLPattern` API.

### How to upgrade

Use [URLPattern](https://developer.mozilla.org/docs/Web/API/URLPattern) to check if a Middleware is being invoked for a certain page match.

#### Before

 pages/_middleware.ts

```
import { NextResponse } from 'next/server'
import type { NextRequest, NextFetchEvent } from 'next/server'

export function middleware(request: NextRequest, event: NextFetchEvent) {
  const { params } = event.request.page
  const { locale, slug } = params

  if (locale && slug) {
    const { search, protocol, host } = request.nextUrl
    const url = new URL(`${protocol}//${locale}.${host}/${slug}${search}`)
    return NextResponse.redirect(url)
  }
}
```

#### After

 middleware.ts

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const PATTERNS = [
  [
    new URLPattern({ pathname: '/:locale/:slug' }),
    ({ pathname }) => pathname.groups,
  ],
]

const params = (url) => {
  const input = url.split('?')[0]
  let result = {}

  for (const [pattern, handler] of PATTERNS) {
    const patternResult = pattern.exec(input)
    if (patternResult !== null && 'pathname' in patternResult) {
      result = handler(patternResult)
      break
    }
  }
  return result
}

export function middleware(request: NextRequest) {
  const { locale, slug } = params(request.url)

  if (locale && slug) {
    const { search, protocol, host } = request.nextUrl
    const url = new URL(`${protocol}//${locale}.${host}/${slug}${search}`)
    return NextResponse.redirect(url)
  }
}
```

## Executing Middleware on Internal Next.js Requests

### Summary of changes

- Middleware will be executed for *all* requests, including `_next`

### Explanation

Prior to Next.js `v12.2`, Middleware was not executed for `_next` requests.

For cases where Middleware is used for authorization, you should migrate to use `rewrite`/`redirect` to Pages that show an authorization error, login forms, or to an API Route.

See [No Response Body](#no-response-body) for an example of how to migrate to use `rewrite`/`redirect`.

Was this helpful?

supported.

---

# Missing Suspense boundary with useSearchParams

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Missing Suspense boundary with useSearchParams

# Missing Suspense boundary with useSearchParams

## Why This Error Occurred

Reading search parameters through `useSearchParams()` without a Suspense boundary will opt the entire page into client-side rendering. This could cause your page to be blank until the client-side JavaScript has loaded.

## Possible Ways to Fix It

You have a few options depending on your intent:

- To keep the route statically generated, wrap the smallest subtree that calls `useSearchParams()` in `Suspense`, for example you may move its usage into a child Client Component and render that component wrapped with `Suspense`. This preserves the static shell and avoids a full CSR bailout.
- To make the route dynamically rendered, use the [connection](https://nextjs.org/docs/app/api-reference/functions/connection) function in a Server Component (e.g. the Page or a wrapping Layout). This waits for an incoming request and excludes everything below from prerendering.

 app/page.tsxJavaScriptTypeScript

```
import { connection } from 'next/server'

export default async function Page() {
  await connection()
  return <div>...</div>
}
```

- Before the `connection` API was available setting `export const dynamic = 'force-dynamic'` in a Server Component `page.tsx`, or `layout.tsx`, opted the route into on-demand rendering. Note that setting `dynamic` in a Client Component (`'use client'`) `page.tsx` has no effect.

 app/layout.tsxJavaScriptTypeScript

```
export const dynamic = 'force-dynamic'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
```

- Alternatively, a Server Component Page can pass the `searchParams` value down to Client Components. In a Client Component, you can unwrap it with React's `use()` (ensure a surrounding `Suspense` boundary). See [What to use and when](https://nextjs.org/docs/app/getting-started/layouts-and-pages#what-to-use-and-when).

 app/page.tsxJavaScriptTypeScript

```
import { Suspense } from 'react'
import ClientSearch from './client-search'

export default function Page({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>
}) {
  return (
    <Suspense fallback={<>...</>}>
      <ClientSearch searchParams={searchParams} />
    </Suspense>
  )
}
```

 app/client-search.tsxJavaScriptTypeScript

```
'use client'

import { use } from 'react'

export default function ClientSearch({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>
}) {
  const params = use(searchParams)
  return <div>Query: {params.q}</div>
}
```

- Consider making the Page a Server Component again and isolating Client-only code (that uses `useSearchParams`) into child Client Components.

 app/search.tsxJavaScriptTypeScript

```
'use client'

import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react'

function Search() {
  const searchParams = useSearchParams()

  return <input placeholder="Search..." />
}

export function Searchbar() {
  return (
    // You could have a loading skeleton as the `fallback` too
    <Suspense>
      <Search />
    </Suspense>
  )
}
```

## Disabling

> **Note**: This is only available with Next.js version 14.x. If you're in versions above 14 please fix it with the approach above.

We don't recommend disabling this rule. However, if you need to, you can disable it by setting the `missingSuspenseWithCSRBailout` option to `false` in your `next.config.js`:

 next.config.js

```
module.exports = {
  experimental: {
    missingSuspenseWithCSRBailout: false,
  },
}
```

This configuration option will be removed in a future major version.

## Debugging

If you're having trouble locating where `useSearchParams()` is being used without a Suspense boundary, you can get more detailed stack traces by running:

```
next build --debug-prerender
```

This provides unminified stack traces with source maps, making it easier to pinpoint the exact component and route causing the issue.

## Useful Links

- [useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params)
- [connection](https://nextjs.org/docs/app/api-reference/functions/connection)
- [Dynamic Rendering guide](https://nextjs.org/docs/app/guides/caching#dynamic-rendering)
- [Debugging prerender errors](https://nextjs.org/docs/app/api-reference/cli/next#debugging-prerender-errors)

Was this helpful?

supported.

---

# `next/dynamic` has deprecated loading multiple modules at once

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)`next/dynamic` has deprecated loading multiple modules at once

# `next/dynamic` has deprecated loading multiple modules at once

## Why This Error Occurred

The ability to load multiple modules at once has been deprecated in `next/dynamic` to be closer to React's implementation (`React.lazy` and `Suspense`).

Updating code that relies on this behavior is relatively straightforward! We've provided an example of a before/after to help you migrate your application:

## Possible Ways to Fix It

Migrate to using separate dynamic calls for each module.

**Before**

 example.js

```
import dynamic from 'next/dynamic'

const HelloBundle = dynamic({
  modules: () => {
    const components = {
      Hello1: () => import('../components/hello1').then((m) => m.default),
      Hello2: () => import('../components/hello2').then((m) => m.default),
    }

    return components
  },
  render: (props, { Hello1, Hello2 }) => (
    <div>
      <h1>{props.title}</h1>
      <Hello1 />
      <Hello2 />
    </div>
  ),
})

function DynamicBundle() {
  return <HelloBundle title="Dynamic Bundle" />
}

export default DynamicBundle
```

**After**

 example.js

```
import dynamic from 'next/dynamic'

const Hello1 = dynamic(() => import('../components/hello1'))
const Hello2 = dynamic(() => import('../components/hello2'))

function HelloBundle({ title }) {
  return (
    <div>
      <h1>{title}</h1>
      <Hello1 />
      <Hello2 />
    </div>
  )
}

function DynamicBundle() {
  return <HelloBundle title="Dynamic Bundle" />
}

export default DynamicBundle
```

Was this helpful?

supported.

---

# Cannot access `cookies()` or `headers()` in `"use cache"`

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Cannot access `cookies()` or `headers()` in `"use cache"`

# Cannot access `cookies()` or `headers()` in `"use cache"`

## Why This Error Occurred

A function is trying to read from the current incoming request inside the scope of a function annotated with `"use cache"`. This is not supported because it would make the cache invalidated by every request which is probably not what you intended.

## Possible Ways to Fix It

Instead of calling this inside the `"use cache"` function, move it outside the function and pass the value in as an argument. The specific value will now be part of the cache key through its arguments.

Before:

 app/page.js

```
import { cookies } from 'next/headers'

async function getExampleData() {
  "use cache"
  const isLoggedIn = (await cookies()).has('token')
  ...
}

export default async function Page() {
  const data = await getExampleData()
  return ...
}
```

After:

 app/page.js

```
import { cookies } from 'next/headers'

async function getExampleData(isLoggedIn) {
  "use cache"
  ...
}

export default async function Page() {
  const isLoggedIn = (await cookies()).has('token')
  const data = await getExampleData(isLoggedIn)
  return ...
}
```

## Useful Links

- [headers()function](https://nextjs.org/docs/app/api-reference/functions/headers)
- [cookies()function](https://nextjs.org/docs/app/api-reference/functions/cookies)
- [draftMode()function](https://nextjs.org/docs/app/api-reference/functions/draft-mode)

Was this helpful?

supported.

---

# Using Google Analytics with Next.js (through `@next/third

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Using Google Analytics with Next.js (through `@next/third-parties/google`)

# Using Google Analytics with Next.js (through `@next/third-parties/google`)

> Prefer `@next/third-parties/google` when using the inline script for Google Analytics and Tag Manager.

## Why This Error Occurred

An inline script was used for Google Analytics which might impact your webpage's performance. Instead, we recommend using `next/script` through the `@next/third-parties` library.

## Possible Ways to Fix It

### Use@next/third-partiesto add Google Analytics

**@next/third-parties** is a library that provides a collection of components and utilities that improve the performance and developer experience of loading popular third-party libraries in your Next.js application. It is available with Next.js 14 (install `next@latest`).

The `GoogleAnalytics` component can be used to include [Google Analytics
4](https://developers.google.com/analytics/devguides/collection/ga4) to your page via the Google tag (`gtag.js`). By default, it fetches the original scripts after hydration occurs on the page.

> **Recommendation**: If Google Tag Manager is already included in your application, you can
> configure Google Analytics directly using it, rather than including Google Analytics as a separate component. Refer to the [documentation](https://developers.google.com/analytics/devguides/collection/ga4/tag-options#what-is-gtm)
> to learn more about the differences between Tag Manager and `gtag.js`.

To load Google Analytics for all routes, include the component directly in your root layout and pass in your measurement ID:

 app/layout.tsxJavaScriptTypeScript

```
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
      <GoogleAnalytics gaId="G-XYZ" />
    </html>
  )
}
```

To load Google Analytics for a single route, include the component in your page file:

 app/page.js

```
import { GoogleAnalytics } from '@next/third-parties/google'

export default function Page() {
  return <GoogleAnalytics gaId="G-XYZ" />
}
```

### Use@next/third-partiesto add Google Tag Manager

The `GoogleTagManager` component can be used to add [Google Tag Manager](https://developers.google.com/tag-manager/quickstart) to your page.

 app/layout.tsxJavaScriptTypeScript

```
import { GoogleTagManager } from '@next/third-parties/google'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <GoogleTagManager gtmId="GTM-XYZ" />
      <body>{children}</body>
    </html>
  )
}
```

To load Google Tag Manager for a single route, include the component in your page file:

 app/page.js

```
import { GoogleTagManager } from '@next/third-parties/google'

export default function Page() {
  return <GoogleTagManager gtmId="GTM-XYZ" />
}
```

## Good to know

- If you are using the Pages Router, please refer to the [pages/documentation](https://nextjs.org/docs/pages/guides/third-party-libraries).
- `@next/third-parties` also supports [other third parties](https://nextjs.org/docs/app/guides/third-party-libraries#google-tag-manager).
- Using `@next/third-parties` is not required. You can also use the `next/script` component directly. Refer to the [next/scriptdocumentation](https://nextjs.org/docs/app/guides/scripts) to learn more.

## Useful Links

- [@next/third-partiesDocumentation](https://nextjs.org/docs/app/guides/third-party-libraries)
- [next/scriptDocumentation](https://nextjs.org/docs/app/guides/scripts)

Was this helpful?

supported.

---

# No assign module variable

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No assign module variable

# No assign module variable

> Prevent assignment to the `module` variable.

## Why This Error Occurred

A value is being assigned to the `module` variable. The `module` variable is already used and it is highly likely that assigning to this variable will cause errors.

## Possible Ways to Fix It

Use a different variable name:

 example.js

```
let myModule = {...}
```

Was this helpful?

supported.
