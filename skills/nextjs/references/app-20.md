# Cache Components and more

# Cache Components

> Learn how to use Cache Components and combine the benefits of static and dynamic rendering.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Cache Components

# Cache Components

Last updated  January 26, 2026

> **Good to know:** Cache Components is an opt-in feature. Enable it by setting the `cacheComponents` flag to `true` in your Next config file. See [Enabling Cache Components](#enabling-cache-components) for more details.

Cache Components lets you mix static, cached, and dynamic content in a single route, giving you the speed of static sites with the flexibility of dynamic rendering.

Server-rendered applications typically force a choice between static pages (fast but stale) and dynamic pages (fresh but slow). Moving this work to the client trades server load for larger bundles and slower initial rendering.

Cache Components eliminates these tradeoffs by prerendering routes into a **static HTML shell** that's immediately sent to the browser, with dynamic content updating the UI as it becomes ready.

 ![Partially re-rendered Product Page showing static nav and product information, and dynamic cart and recommended products](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Flearn%2Flight%2Fthinking-in-ppr.png&w=3840&q=75)![Partially re-rendered Product Page showing static nav and product information, and dynamic cart and recommended products](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Flearn%2Fdark%2Fthinking-in-ppr.png&w=3840&q=75)

## How rendering works with Cache Components

At build time, Next.js renders your route's component tree. As long as components don't access network resources, certain system APIs, or require an incoming request to render, their output is **automatically added to the static shell**. Otherwise, you must choose how to handle them:

- Defer rendering to request time by wrapping components in React's [<Suspense>](https://react.dev/reference/react/Suspense), [showing fallback UI](#defer-rendering-to-request-time) until the content is ready, or
- Cache the result using the [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) directive to [include it in the static shell](#using-use-cache) (if no request data is needed)

Because this happens ahead of time, before a request arrives, we refer to it as prerendering. This generates a static shell consisting of HTML for initial page loads and a serialized [RSC Payload](https://nextjs.org/docs/app/getting-started/server-and-client-components#on-the-server) for client-side navigation, ensuring the browser receives fully rendered content instantly whether users navigate directly to the URL or transition from another page.

Next.js requires you to explicitly handle components that can't complete during prerendering. If they aren't wrapped in `<Suspense>` or marked with `use cache`, you'll see an [Uncached data was accessed outside of <Suspense>](https://nextjs.org/docs/messages/blocking-route) error during development and build time.

> **Good to know**: Caching can be applied at the component or function level, while fallback UI can be defined around any subtree, which means you can compose static, cached, and dynamic content within a single route.

 ![Diagram showing partially rendered page on the client, with loading UI for chunks that are being streamed.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fserver-rendering-with-streaming.png&w=3840&q=75)![Diagram showing partially rendered page on the client, with loading UI for chunks that are being streamed.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fserver-rendering-with-streaming.png&w=3840&q=75)

This rendering approach is called **Partial Prerendering**, and it's the default behavior with Cache Components. For the rest of this document, we simply refer to it as "prerendering" which can produce a partial or complete output.

> **🎥 Watch:** Why Partial Prerendering and how it works → [YouTube (10 minutes)](https://www.youtube.com/watch?v=MTcPrTIBkpA).

## Automatically prerendered content

Operations like synchronous I/O, module imports, and pure computations can complete during prerendering. Components using only these operations have their rendered output included in the static HTML shell.

Because all operations in the `Page` component below complete during rendering, its rendered output is automatically included in the static shell. When both the layout and page prerender successfully, the entire route is the static shell.

 page.tsx

```
import fs from 'node:fs'

export default async function Page() {
  // Synchronous file system read
  const content = fs.readFileSync('./config.json', 'utf-8')

  // Module imports
  const constants = await import('./constants.json')

  // Pure computations
  const processed = JSON.parse(content).items.map((item) => item.value * 2)

  return (
    <div>
      <h1>{constants.appName}</h1>
      <ul>
        {processed.map((value, i) => (
          <li key={i}>{value}</li>
        ))}
      </ul>
    </div>
  )
}
```

> **Good to know**: You can verify that a route was fully prerendered by checking the build output summary. Alternatively, see what content was added to the static shell of any page by viewing the page source in your browser.

## Defer rendering to request time

During prerendering, when Next.js encounters work it can't complete (like network requests, accessing request data, or async operations), it requires you to explicitly handle it. To defer rendering to request time, a parent component must provide fallback UI using a Suspense boundary. The fallback becomes part of the static shell while the actual content resolves at request time.

Place Suspense boundaries as close as possible to the components that need them. This maximizes the amount of content in the static shell, since everything outside the boundary can still prerender normally.

> **Good to know**: With Suspense boundaries, multiple dynamic sections can render in parallel rather than blocking each other, reducing total load time.

### Dynamic content

External systems provide content asynchronously, which often takes an unpredictable time to resolve and may even fail. This is why prerendering doesn't execute them automatically.

In general, when you need the latest data from the source on each request (like real-time feeds or personalized content), defer rendering by providing fallback UI with a Suspense boundary.

For example, the `DynamicContent` component below uses multiple operations that are not automatically prerendered.

 page.tsx

```
import { Suspense } from 'react'
import fs from 'node:fs/promises'

async function DynamicContent() {
  // Network request
  const data = await fetch('https://api.example.com/data')

  // Database query
  const users = await db.query('SELECT * FROM users')

  // Async file system operation
  const file = await fs.readFile('..', 'utf-8')

  // Simulating external system delay
  await new Promise((resolve) => setTimeout(resolve, 100))

  return <div>Not in the static shell</div>
}
```

To use `DynamicContent` within a page, wrap it in `<Suspense>` to define fallback UI:

 page.tsx

```
export default async function Page(props) {
  return (
    <>
      <h1>Part of the static shell</h1>
      {/* <p>Loading..</p> is part of the static shell */}
      <Suspense fallback={<p>Loading..</p>}>
        <DynamicContent />
        <div>Sibling excluded from static shell</div>
      </Suspense>
    </>
  )
}
```

Prerendering stops at the `fetch` request. The request itself is not started, and any code after it is not executed.

The fallback (`<p>Loading...</p>`) is included in the static shell, while the component's content streams at request time.

In this example, since all operations (network request, database query, file read, and timeout) run sequentially within the same component, the content won't appear until they all complete.

> **Good to know**: For dynamic content that doesn't change frequently, you can use `use cache` to include the dynamic data in the static shell instead of streaming it. See the [during prerendering](#during-prerendering) section for an example.

### Runtime data

A specific type of dynamic data that requires request context, only available when a user makes a request.

- [cookies()](https://nextjs.org/docs/app/api-reference/functions/cookies) - User's cookie data
- [headers()](https://nextjs.org/docs/app/api-reference/functions/headers) - Request headers
- [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) - URL query parameters
- [params](https://nextjs.org/docs/app/api-reference/file-conventions/page#params-optional) - Dynamic route parameters (unless at least one sample is provided via [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params)). See [Dynamic Routes with Cache Components](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#with-cache-components) for detailed patterns.

 page.tsx

```
import { cookies, headers } from 'next/headers'
import { Suspense } from 'react'

async function RuntimeData({ searchParams }) {
  // Accessing request data
  const cookieStore = await cookies()
  const headerStore = await headers()
  const search = await searchParams

  return <div>Not in the static shell</div>
}
```

To use the `RuntimeData` component, wrap it in a `<Suspense>` boundary:

 page.tsx

```
export default async function Page(props) {
  return (
    <>
      <h1>Part of the static shell</h1>
      {/* <p>Loading..</p> is part of the static shell */}
      <Suspense fallback={<p>Loading..</p>}>
        <RuntimeData searchParams={props.searchParams} />
        <div>Sibling excluded from static shell</div>
      </Suspense>
    </>
  )
}
```

Use [connection()](https://nextjs.org/docs/app/api-reference/functions/connection) if you need to defer to request time without accessing any of the runtime APIs above.

> **Good to know**: Runtime data cannot be cached with `use cache` because it requires request context. Components that access runtime APIs must always be wrapped in `<Suspense>`. However, you can extract values from runtime data and pass them as arguments to cached functions. See the [with runtime data](#with-runtime-data) section for an example.

One approach for reading runtime data like cookies without blocking the static shell is to pass a promise to a client context provider. See [Sharing data with context and React.cache](https://nextjs.org/docs/app/getting-started/server-and-client-components#sharing-data-with-context-and-reactcache) for an example.

> **Good to know:** `React.cache` operates in an isolated scope inside `use cache` boundaries. See [React.cache isolation](https://nextjs.org/docs/app/api-reference/directives/use-cache#reactcache-isolation) for more information.

### Non-deterministic operations

Operations like `Math.random()`, `Date.now()`, or `crypto.randomUUID()` produce different values each time they execute. To ensure these run at request time (generating unique values per request), Cache Components requires you to explicitly signal this intent by calling these operations after dynamic or runtime data access.

```
import { connection } from 'next/server'
import { Suspense } from 'react'

async function UniqueContent() {
  // Explicitly defer to request time
  await connection()

  // Non-deterministic operations
  const random = Math.random()
  const now = Date.now()
  const date = new Date()
  const uuid = crypto.randomUUID()
  const bytes = crypto.getRandomValues(new Uint8Array(16))

  return (
    <div>
      <p>{random}</p>
      <p>{now}</p>
      <p>{date.getTime()}</p>
      <p>{uuid}</p>
      <p>{bytes}</p>
    </div>
  )
}
```

Because the `UniqueContent` component defers to request time, to use it within a route, it must be wrapped in `<Suspense>`:

 page.tsx

```
export default async function Page() {
  return (
    // <p>Loading..</p> is part of the static shell
    <Suspense fallback={<p>Loading..</p>}>
      <UniqueContent />
    </Suspense>
  )
}
```

Every incoming request would see different random numbers, date, etc.

> **Good to know**: You can cache non-deterministic operations with `use cache`. See the [with non-deterministic operations](#with-non-deterministic-operations) section for examples.

## Usinguse cache

The [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) directive caches the return value of async functions and components. You can apply it at the function, component, or file level.

Arguments and any closed-over values from parent scopes automatically become part of the [cache key](https://nextjs.org/docs/app/api-reference/directives/use-cache#cache-keys), which means different inputs produce separate cache entries. This enables personalized or parameterized cached content.

When [dynamic content](#dynamic-content) doesn't need to be fetched fresh from the source on every request, caching it lets you include the content in the static shell during prerendering, or reuse the result at runtime across multiple requests.

Cached content can be revalidated in two ways: automatically based on the cache lifetime, or on-demand using tags with [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) or [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag).

> **Good to know**: See [serialization requirements and constraints](https://nextjs.org/docs/app/api-reference/directives/use-cache#constraints) for details on what can be cached and how arguments work.

### During prerendering

While [dynamic content](#dynamic-content) is fetched from external sources, it's often unlikely to change between accesses. Product catalog data updates with inventory changes, blog post content rarely changes after publishing, and analytics reports for past dates remain static.

If this data doesn't depend on [runtime data](#runtime-data), you can use the `use cache` directive to include it in the static HTML shell. Use [cacheLife](https://nextjs.org/docs/app/api-reference/functions/cacheLife) to define how long to use the cached data.

When revalidation occurs, the static shell is updated with fresh content. See [Tagging and revalidating](#tagging-and-revalidating) for details on on-demand revalidation.

 app/page.tsx

```
import { cacheLife } from 'next/cache'

export default async function Page() {
  'use cache'
  cacheLife('hours')

  const users = await db.query('SELECT * FROM users')

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

The `cacheLife` function accepts a cache profile name (like `'hours'`, `'days'`, or `'weeks'`) or a custom configuration object to control cache behavior:

 app/page.tsx

```
import { cacheLife } from 'next/cache'

export default async function Page() {
  'use cache'
  cacheLife({
    stale: 3600, // 1 hour until considered stale
    revalidate: 7200, // 2 hours until revalidated
    expire: 86400, // 1 day until expired
  })

  const users = await db.query('SELECT * FROM users')

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

See the [cacheLifeAPI reference](https://nextjs.org/docs/app/api-reference/functions/cacheLife) for available profiles and custom configuration options.

### With runtime data

Runtime data and [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) cannot be used in the same scope. However, you can extract values from runtime APIs and pass them as arguments to cached functions.

 app/profile/page.tsx

```
import { cookies } from 'next/headers'
import { Suspense } from 'react'

export default function Page() {
  // Page itself creates the dynamic boundary
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ProfileContent />
    </Suspense>
  )
}

// Component (not cached) reads runtime data
async function ProfileContent() {
  const session = (await cookies()).get('session')?.value

  return <CachedContent sessionId={session} />
}

// Cached component/function receives data as props
async function CachedContent({ sessionId }: { sessionId: string }) {
  'use cache'
  // sessionId becomes part of cache key
  const data = await fetchUserData(sessionId)
  return <div>{data}</div>
}
```

At request time, `CachedContent` executes if no matching cache entry is found, and stores the result for future requests.

### With non-deterministic operations

Within a `use cache` scope, non-deterministic operations execute during prerendering. This is useful when you want the same rendered output served to all users:

```
export default async function Page() {
  'use cache'

  // Execute once, then cached for all requests
  const random = Math.random()
  const random2 = Math.random()
  const now = Date.now()
  const date = new Date()
  const uuid = crypto.randomUUID()
  const bytes = crypto.getRandomValues(new Uint8Array(16))

  return (
    <div>
      <p>
        {random} and {random2}
      </p>
      <p>{now}</p>
      <p>{date.getTime()}</p>
      <p>{uuid}</p>
      <p>{bytes}</p>
    </div>
  )
}
```

All requests will be served a route containing the same random numbers, timestamp, and UUID until the cache is revalidated.

### Tagging and revalidating

Tag cached data with [cacheTag](https://nextjs.org/docs/app/api-reference/functions/cacheTag) and revalidate it after mutations using [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag) in Server Actions for immediate updates, or [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) when delays in updates are acceptable.

#### WithupdateTag

Use `updateTag` when you need to expire and immediately refresh cached data within the same request:

 app/actions.ts

```
import { cacheTag, updateTag } from 'next/cache'

export async function getCart() {
  'use cache'
  cacheTag('cart')
  // fetch data
}

export async function updateCart(itemId: string) {
  'use server'
  // write data using the itemId
  // update the user cart
  updateTag('cart')
}
```

#### WithrevalidateTag

Use `revalidateTag` when you want to invalidate only properly tagged cached entries with stale-while-revalidate behavior. This is ideal for static content that can tolerate eventual consistency.

 app/actions.ts

```
import { cacheTag, revalidateTag } from 'next/cache'

export async function getPosts() {
  'use cache'
  cacheTag('posts')
  // fetch data
}

export async function createPost(post: FormData) {
  'use server'
  // write data using the FormData
  revalidateTag('posts', 'max')
}
```

For more detailed explanation and usage examples, see the [use cacheAPI reference](https://nextjs.org/docs/app/api-reference/directives/use-cache).

### What should I cache?

What you cache should be a function of what you want your UI loading states to be. If data doesn't depend on runtime data and you're okay with a cached value being served for multiple requests over a period of time, use `use cache` with `cacheLife` to describe that behavior.

For content management systems with update mechanisms, consider using tags with longer cache durations and rely on `revalidateTag` to mark static initial UI as ready for revalidation. This pattern allows you to serve fast, cached responses while still updating content when it actually changes, rather than expiring the cache preemptively.

## Putting it all together

Here's a complete example showing static content, cached dynamic content, and streaming dynamic content working together on a single page:

 app/blog/page.tsx

```
import { Suspense } from 'react'
import { cookies } from 'next/headers'
import { cacheLife } from 'next/cache'
import Link from 'next/link'

export default function BlogPage() {
  return (
    <>
      {/* Static content - prerendered automatically */}
      <header>
        <h1>Our Blog</h1>
        <nav>
          <Link href="/">Home</Link> | <Link href="/about">About</Link>
        </nav>
      </header>

      {/* Cached dynamic content - included in the static shell */}
      <BlogPosts />

      {/* Runtime dynamic content - streams at request time */}
      <Suspense fallback={<p>Loading your preferences...</p>}>
        <UserPreferences />
      </Suspense>
    </>
  )
}

// Everyone sees the same blog posts (revalidated every hour)
async function BlogPosts() {
  'use cache'
  cacheLife('hours')

  const res = await fetch('https://api.vercel.app/blog')
  const posts = await res.json()

  return (
    <section>
      <h2>Latest Posts</h2>
      <ul>
        {posts.slice(0, 5).map((post: any) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>
              By {post.author} on {post.date}
            </p>
          </li>
        ))}
      </ul>
    </section>
  )
}

// Personalized per user based on their cookie
async function UserPreferences() {
  const theme = (await cookies()).get('theme')?.value || 'light'
  const favoriteCategory = (await cookies()).get('category')?.value

  return (
    <aside>
      <p>Your theme: {theme}</p>
      {favoriteCategory && <p>Favorite category: {favoriteCategory}</p>}
    </aside>
  )
}
```

During prerendering the header (static) and the blog posts fetched from the API (cached with `use cache`), both become part of the static shell along with the fallback UI for user preferences.

When a user visits the page, they instantly see this prerendered shell with the header and blog posts. Only the personalized preferences need to stream in at request time since they depend on the user's cookies. This ensures fast initial page loads while still providing personalized content.

## Metadata and Viewport

`generateMetadata` and `generateViewport` are part of rendering your page or layout. During prerendering, their access to runtime data or uncached dynamic data is tracked separately from the rest of the page.

If a page or layout is prerenderable but only metadata or viewport accesses uncached dynamic data or runtime data, Next.js requires an explicit choice: cache the data if possible, or signal that deferred rendering is intentional. See [Metadata with Cache Components](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#with-cache-components) and [Viewport with Cache Components](https://nextjs.org/docs/app/api-reference/functions/generate-viewport#with-cache-components) for how to handle this.

## Enabling Cache Components

You can enable Cache Components (which includes PPR) by adding the [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) option to your Next config file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

> **Good to know:** When Cache Components is enabled, `GET` Route Handlers follow the same prerendering model as pages. See [Route Handlers with Cache Components](https://nextjs.org/docs/app/getting-started/route-handlers#with-cache-components) for details.

## Navigation uses Activity

When the [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) flag is enabled, Next.js uses React's [<Activity>](https://react.dev/reference/react/Activity) component to preserve component state during client-side navigation.

Rather than unmounting the previous route when you navigate away, Next.js sets the Activity mode to ["hidden"](https://react.dev/reference/react/Activity#activity). This means:

- Component state is preserved when navigating between routes
- When you navigate back, the previous route reappears with its state intact
- Effects are cleaned up when a route is hidden, and recreated when it becomes visible again

This behavior improves the navigation experience by maintaining UI state (form inputs, or expanded sections) when users navigate back and forth between routes.

> **Good to know**: Next.js uses heuristics to keep a few recently visited routes `"hidden"`, while older routes are removed from the DOM to prevent excessive growth.

## Migrating route segment configs

When Cache Components is enabled, several route segment config options are no longer needed or supported:

### dynamic = "force-dynamic"

**Not needed.** All pages are dynamic by default.

 app/page.tsx

```
// Before - No longer needed
export const dynamic = 'force-dynamic'

export default function Page() {
  return <div>...</div>
}
```

 app/page.tsx

```
// After - Just remove it
export default function Page() {
  return <div>...</div>
}
```

### dynamic = "force-static"

Start by removing it. When unhandled dynamic or runtime data access is detected during development and build time, Next.js raises an error. Otherwise, the [prerendering](#automatically-prerendered-content) step automatically extracts the static HTML shell.

For dynamic data access, add [use cache](#using-use-cache) as close to the data access as possible with a long [cacheLife](https://nextjs.org/docs/app/api-reference/functions/cacheLife) like `'max'` to maintain cached behavior. If needed, add it at the top of the page or layout.

For runtime data access (`cookies()`, `headers()`, etc.), errors will direct you to [wrap it withSuspense](#runtime-data). Since you started by using `force-static`, you must remove the runtime data access to prevent any request time work.

 app/page.tsx

```
// Before
export const dynamic = 'force-static'

export default async function Page() {
  const data = await fetch('https://api.example.com/data')
  return <div>...</div>
}
```

 app/page.tsx

```
import { cacheLife } from 'next/cache'

// After - Use 'use cache' instead
export default async function Page() {
  'use cache'
  cacheLife('max')
  const data = await fetch('https://api.example.com/data')
  return <div>...</div>
}
```

### revalidate

**Replace withcacheLife.** Use the `cacheLife` function to define cache duration instead of the route segment config.

```
// Before
export const revalidate = 3600 // 1 hour

export default async function Page() {
  return <div>...</div>
}
```

 app/page.tsx

```
// After - Use cacheLife
import { cacheLife } from 'next/cache'

export default async function Page() {
  'use cache'
  cacheLife('hours')
  return <div>...</div>
}
```

### fetchCache

**Not needed.** With `use cache`, all data fetching within a cached scope is automatically cached, making `fetchCache` unnecessary.

 app/page.tsx

```
// Before
export const fetchCache = 'force-cache'
```

 app/page.tsx

```
// After - Use 'use cache' to control caching behavior
export default async function Page() {
  'use cache'
  // All fetches here are cached
  return <div>...</div>
}
```

### runtime = 'edge'

**Not supported.** Cache Components requires Node.js runtime and will throw errors with [Edge Runtime](https://nextjs.org/docs/app/api-reference/edge).

## Next Steps

Learn more about the config option for Cache Components.[cacheComponentsLearn how to enable the cacheComponents flag in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)[use cacheLearn how to use the "use cache" directive to cache data in your Next.js application.](https://nextjs.org/docs/app/api-reference/directives/use-cache)[cacheLifeLearn how to use the cacheLife function to set the cache expiration time for a cached function or component.](https://nextjs.org/docs/app/api-reference/functions/cacheLife)[cacheTagLearn how to use the cacheTag function to manage cache invalidation in your Next.js application.](https://nextjs.org/docs/app/api-reference/functions/cacheTag)[revalidateTagAPI Reference for the revalidateTag function.](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)[updateTagAPI Reference for the updateTag function.](https://nextjs.org/docs/app/api-reference/functions/updateTag)

Was this helpful?

supported.

---

# Caching and Revalidating

> Learn how to cache and revalidate data in your application.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Caching and Revalidating

# Caching and Revalidating

Last updated  November 5, 2025

Caching is a technique for storing the result of data fetching and other computations so that future requests for the same data can be served faster, without doing the work again. While revalidation allows you to update cache entries without having to rebuild your entire application.

Next.js provides a few APIs to handle caching and revalidation. This guide will walk you through when and how to use them.

- [fetch](#fetch)
- [cacheTag](#cachetag)
- [revalidateTag](#revalidatetag)
- [updateTag](#updatetag)
- [revalidatePath](#revalidatepath)
- [unstable_cache](#unstable_cache) (Legacy)

## fetch

By default, [fetch](https://nextjs.org/docs/app/api-reference/functions/fetch) requests are not cached. You can cache individual requests by setting the `cache` option to `'force-cache'`.

 app/page.tsxJavaScriptTypeScript

```
export default async function Page() {
  const data = await fetch('https://...', { cache: 'force-cache' })
}
```

> **Good to know**: Although `fetch` requests are not cached by default, Next.js will [pre-render](https://nextjs.org/docs/app/guides/caching#static-rendering) routes that have `fetch` requests and cache the HTML. If you want to guarantee a route is [dynamic](https://nextjs.org/docs/app/guides/caching#dynamic-rendering), use the [connectionAPI](https://nextjs.org/docs/app/api-reference/functions/connection).

To revalidate the data returned by a `fetch` request, you can use the `next.revalidate` option.

 app/page.tsxJavaScriptTypeScript

```
export default async function Page() {
  const data = await fetch('https://...', { next: { revalidate: 3600 } })
}
```

This will revalidate the data after a specified amount of seconds.

You can also tag `fetch` requests to enable on-demand cache invalidation:

 app/lib/data.tsJavaScriptTypeScript

```
export async function getUserById(id: string) {
  const data = await fetch(`https://...`, {
    next: {
      tags: ['user'],
    },
  })
}
```

See the [fetchAPI reference](https://nextjs.org/docs/app/api-reference/functions/fetch) to learn more.

## cacheTag

[cacheTag](https://nextjs.org/docs/app/api-reference/functions/cacheTag) allows you to tag cached data in [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) so it can be revalidated on-demand. Previously, cache tagging was limited to `fetch` requests, and caching other work required the experimental `unstable_cache` API.

With Cache Components, you can use the [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) directive to cache any computation, and `cacheTag` to tag it. This works with database queries, file system operations, and other server-side work.

 app/lib/data.tsJavaScriptTypeScript

```
import { cacheTag } from 'next/cache'

export async function getProducts() {
  'use cache'
  cacheTag('products')

  const products = await db.query('SELECT * FROM products')
  return products
}
```

Once tagged, you can use [revalidateTag](#revalidatetag) or [updateTag](#updatetag) to invalidate the cache entry for products.

> **Good to know**: `cacheTag` is used with [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) and the [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) directive. It expands the caching and revalidation story beyond `fetch`.

See the [cacheTagAPI reference](https://nextjs.org/docs/app/api-reference/functions/cacheTag) to learn more.

## revalidateTag

`revalidateTag` is used to revalidate cache entries based on a tag and following an event. The function now supports two behaviors:

- **Withprofile="max"**: Uses stale-while-revalidate semantics, serving stale content while fetching fresh content in the background
- **Without the second argument**: Legacy behavior that immediately expires the cache (deprecated)

After tagging your cached data, using [fetch](#fetch) with `next.tags`, or the [cacheTag](#cachetag) function, you may call `revalidateTag` in a [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route) or Server Action:

 app/lib/actions.tsJavaScriptTypeScript

```
import { revalidateTag } from 'next/cache'

export async function updateUser(id: string) {
  // Mutate data
  revalidateTag('user', 'max') // Recommended: Uses stale-while-revalidate
}
```

You can reuse the same tag in multiple functions to revalidate them all at once.

See the [revalidateTagAPI reference](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) to learn more.

## updateTag

`updateTag` is specifically designed for Server Actions to immediately expire cached data for read-your-own-writes scenarios. Unlike `revalidateTag`, it can only be used within Server Actions and immediately expires the cache entry.

 app/lib/actions.tsJavaScriptTypeScript

```
import { updateTag } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  // Create post in database
  const post = await db.post.create({
    data: {
      title: formData.get('title'),
      content: formData.get('content'),
    },
  })

  // Immediately expire cache so the new post is visible
  updateTag('posts')
  updateTag(`post-${post.id}`)

  redirect(`/posts/${post.id}`)
}
```

The key differences between `revalidateTag` and `updateTag`:

- **updateTag**: Only in Server Actions, immediately expires cache, for read-your-own-writes
- **revalidateTag**: In Server Actions and Route Handlers, supports stale-while-revalidate with `profile="max"`

See the [updateTagAPI reference](https://nextjs.org/docs/app/api-reference/functions/updateTag) to learn more.

## revalidatePath

`revalidatePath` is used to revalidate a route and following an event. To use it, call it in a [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route) or Server Action:

 app/lib/actions.tsJavaScriptTypeScript

```
import { revalidatePath } from 'next/cache'

export async function updateUser(id: string) {
  // Mutate data
  revalidatePath('/profile')
```

See the [revalidatePathAPI reference](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) to learn more.

## unstable_cache

> **Good to know**: `unstable_cache` is an experimental API. We recommend opting into [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) and replacing `unstable_cache` with the [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) directive. See the [Cache Components documentation](https://nextjs.org/docs/app/getting-started/cache-components) for more details.

`unstable_cache` allows you to cache the result of database queries and other async functions. To use it, wrap `unstable_cache` around the function. For example:

 app/lib/data.tsJavaScriptTypeScript

```
import { db } from '@/lib/db'
export async function getUserById(id: string) {
  return db
    .select()
    .from(users)
    .where(eq(users.id, id))
    .then((res) => res[0])
}
```

   app/page.tsxJavaScriptTypeScript

```
import { unstable_cache } from 'next/cache'
import { getUserById } from '@/app/lib/data'

export default async function Page({
  params,
}: {
  params: Promise<{ userId: string }>
}) {
  const { userId } = await params

  const getCachedUser = unstable_cache(
    async () => {
      return getUserById(userId)
    },
    [userId] // add the user ID to the cache key
  )
}
```

The function accepts a third optional object to define how the cache should be revalidated. It accepts:

- `tags`: an array of tags used by Next.js to revalidate the cache.
- `revalidate`: the number of seconds after cache should be revalidated.

 app/page.tsxJavaScriptTypeScript

```
const getCachedUser = unstable_cache(
  async () => {
    return getUserById(userId)
  },
  [userId],
  {
    tags: ['user'],
    revalidate: 3600,
  }
)
```

See the [unstable_cacheAPI reference](https://nextjs.org/docs/app/api-reference/functions/unstable_cache) to learn more.

## API Reference

Learn more about the features mentioned in this page by reading the API Reference.[fetchAPI reference for the extended fetch function.](https://nextjs.org/docs/app/api-reference/functions/fetch)[cacheTagLearn how to use the cacheTag function to manage cache invalidation in your Next.js application.](https://nextjs.org/docs/app/api-reference/functions/cacheTag)[revalidateTagAPI Reference for the revalidateTag function.](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)[updateTagAPI Reference for the updateTag function.](https://nextjs.org/docs/app/api-reference/functions/updateTag)[revalidatePathAPI Reference for the revalidatePath function.](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)[unstable_cacheAPI Reference for the unstable_cache function.](https://nextjs.org/docs/app/api-reference/functions/unstable_cache)

Was this helpful?

supported.

---

# CSS

> Learn about the different ways to add CSS to your application, including Tailwind CSS, CSS Modules, Global CSS, and more.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)CSS

# CSS

Last updated  August 6, 2025

Next.js provides several ways to style your application using CSS, including:

- [Tailwind CSS](#tailwind-css)
- [CSS Modules](#css-modules)
- [Global CSS](#global-css)
- [External Stylesheets](#external-stylesheets)
- [Sass](https://nextjs.org/docs/app/guides/sass)
- [CSS-in-JS](https://nextjs.org/docs/app/guides/css-in-js)

## Tailwind CSS

[Tailwind CSS](https://tailwindcss.com/) is a utility-first CSS framework that provides low-level utility classes to build custom designs.

Install Tailwind CSS:

Terminal

```
pnpm add -D tailwindcss @tailwindcss/postcss
```

Add the PostCSS plugin to your `postcss.config.mjs` file:

postcss.config.mjs

```
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

Import Tailwind in your global CSS file:

app/globals.css

```
@import 'tailwindcss';
```

Import the CSS file in your root layout:

app/layout.tsxJavaScriptTypeScript

```
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

Now you can start using Tailwind's utility classes in your application:

app/page.tsxJavaScriptTypeScript

```
export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl font-bold">Welcome to Next.js!</h1>
    </main>
  )
}
```

> **Good to know:** If you need broader browser support for very old browsers, see the [Tailwind CSS v3 setup instructions](https://nextjs.org/docs/app/guides/tailwind-v3-css).

## CSS Modules

CSS Modules locally scope CSS by generating unique class names. This allows you to use the same class in different files without worrying about naming collisions.

To start using CSS Modules, create a new file with the extension `.module.css` and import it into any component inside the `app` directory:

app/blog/blog.module.css

```
.blog {
  padding: 24px;
}
```

app/blog/page.tsxJavaScriptTypeScript

```
import styles from './blog.module.css'

export default function Page() {
  return <main className={styles.blog}></main>
}
```

## Global CSS

You can use global CSS to apply styles across your application.

Create a `app/global.css` file and import it in the root layout to apply the styles to **every route** in your application:

app/global.css

```
body {
  padding: 20px 20px 60px;
  max-width: 680px;
  margin: 0 auto;
}
```

app/layout.tsxJavaScriptTypeScript

```
// These styles apply to every route in the application
import './global.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

> **Good to know:** Global styles can be imported into any layout, page, or component inside the `app` directory. However, since Next.js uses React's built-in support for stylesheets to integrate with Suspense, this currently does not remove stylesheets as you navigate between routes which can lead to conflicts. We recommend using global styles for *truly* global CSS (like Tailwind's base styles), [Tailwind CSS](#tailwind-css) for component styling, and [CSS Modules](#css-modules) for custom scoped CSS when needed.

## External stylesheets

Stylesheets published by external packages can be imported anywhere in the `app` directory, including colocated components:

app/layout.tsxJavaScriptTypeScript

```
import 'bootstrap/dist/css/bootstrap.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="container">{children}</body>
    </html>
  )
}
```

> **Good to know:** In React 19, `<link rel="stylesheet" href="..." />` can also be used. See the [Reactlinkdocumentation](https://react.dev/reference/react-dom/components/link) for more information.

## Ordering and Merging

Next.js optimizes CSS during production builds by automatically chunking (merging) stylesheets. The **order of your CSS** depends on the **order you import styles in your code**.

For example, `base-button.module.css` will be ordered before `page.module.css` since `<BaseButton>` is imported before `page.module.css`:

 page.tsxJavaScriptTypeScript

```
import { BaseButton } from './base-button'
import styles from './page.module.css'

export default function Page() {
  return <BaseButton className={styles.primary} />
}
```

   base-button.tsxJavaScriptTypeScript

```
import styles from './base-button.module.css'

export function BaseButton() {
  return <button className={styles.primary} />
}
```

### Recommendations

To keep CSS ordering predictable:

- Try to contain CSS imports to a single JavaScript or TypeScript entry file
- Import global styles and Tailwind stylesheets in the root of your application.
- **Use Tailwind CSS** for most styling needs as it covers common design patterns with utility classes.
- Use CSS Modules for component-specific styles when Tailwind utilities aren't sufficient.
- Use a consistent naming convention for your CSS modules. For example, using `<name>.module.css` over `<name>.tsx`.
- Extract shared styles into shared components to avoid duplicate imports.
- Turn off linters or formatters that auto-sort imports like ESLint’s [sort-imports](https://eslint.org/docs/latest/rules/sort-imports).
- You can use the [cssChunking](https://nextjs.org/docs/app/api-reference/config/next-config-js/cssChunking) option in `next.config.js` to control how CSS is chunked.

## Development vs Production

- In development (`next dev`), CSS updates apply instantly with [Fast Refresh](https://nextjs.org/docs/architecture/fast-refresh).
- In production (`next build`), all CSS files are automatically concatenated into **many minified and code-split** `.css` files, ensuring the minimal amount of CSS is loaded for a route.
- CSS still loads with JavaScript disabled in production, but JavaScript is required in development for Fast Refresh.
- CSS ordering can behave differently in development, always ensure to check the build (`next build`) to verify the final CSS order.

## Next Steps

Learn more about the alternatives ways you can use CSS in your application.[Tailwind CSS v3Style your Next.js Application using Tailwind CSS v3 for broader browser support.](https://nextjs.org/docs/app/guides/tailwind-v3-css)[SassStyle your Next.js application using Sass.](https://nextjs.org/docs/app/guides/sass)[CSS-in-JSUse CSS-in-JS libraries with Next.js](https://nextjs.org/docs/app/guides/css-in-js)

Was this helpful?

supported.

---

# Deploying

> Learn how to deploy your Next.js application.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Deploying

# Deploying

Last updated  December 4, 2025

Next.js can be deployed as a Node.js server, Docker container, static export, or adapted to run on different platforms.

| Deployment Option | Feature Support |
| --- | --- |
| Node.js server | All |
| Docker container | All |
| Static export | Limited |
| Adapters | Platform-specific |

## Node.js server

Next.js can be deployed to any provider that supports Node.js. Ensure your `package.json` has the `"build"` and `"start"` scripts:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

Then, run `npm run build` to build your application and `npm run start` to start the Node.js server. This server supports all Next.js features. If needed, you can also eject to a [custom server](https://nextjs.org/docs/app/guides/custom-server).

Node.js deployments support all Next.js features. Learn how to [configure them](https://nextjs.org/docs/app/guides/self-hosting) for your infrastructure.

### Templates

- [Flightcontrol](https://github.com/nextjs/deploy-flightcontrol)
- [Railway](https://github.com/nextjs/deploy-railway)
- [Replit](https://github.com/nextjs/deploy-replit)

## Docker

Next.js can be deployed to any provider that supports [Docker](https://www.docker.com/) containers. This includes container orchestrators like Kubernetes or a cloud provider that runs Docker.

Docker deployments support all Next.js features. Learn how to [configure them](https://nextjs.org/docs/app/guides/self-hosting) for your infrastructure.

> **Note for development:** While Docker is excellent for production deployments, consider using local development (`npm run dev`) instead of Docker during development on Mac and Windows for better performance. [Learn more about optimizing local development](https://nextjs.org/docs/app/guides/local-development).

### Templates

- [Docker](https://github.com/vercel/next.js/tree/canary/examples/with-docker)
- [Docker Multi-Environment](https://github.com/vercel/next.js/tree/canary/examples/with-docker-multi-env)
- [DigitalOcean](https://github.com/nextjs/deploy-digitalocean)
- [Fly.io](https://github.com/nextjs/deploy-fly)
- [Google Cloud Run](https://github.com/nextjs/deploy-google-cloud-run)
- [Render](https://github.com/nextjs/deploy-render)
- [SST](https://github.com/nextjs/deploy-sst)

## Static export

Next.js enables starting as a static site or [Single-Page Application (SPA)](https://nextjs.org/docs/app/guides/single-page-applications), then later optionally upgrading to use features that require a server.

Since Next.js supports [static exports](https://nextjs.org/docs/app/guides/static-exports), it can be deployed and hosted on any web server that can serve HTML/CSS/JS static assets. This includes tools like AWS S3, Nginx, or Apache.

Running as a [static export](https://nextjs.org/docs/app/guides/static-exports) **does not** support Next.js features that require a server. [Learn more](https://nextjs.org/docs/app/guides/static-exports#unsupported-features).

### Templates

- [GitHub Pages](https://github.com/nextjs/deploy-github-pages)

## Adapters

Next.js can be adapted to run on different platforms to support their infrastructure capabilities.

Refer to each provider's documentation for information on supported Next.js features:

- [Appwrite Sites](https://appwrite.io/docs/products/sites/quick-start/nextjs)
- [AWS Amplify Hosting](https://docs.amplify.aws/nextjs/start/quickstart/nextjs-app-router-client-components)
- [Cloudflare](https://developers.cloudflare.com/workers/frameworks/framework-guides/nextjs)
- [Deno Deploy](https://docs.deno.com/examples/next_tutorial)
- [Firebase App Hosting](https://firebase.google.com/docs/app-hosting/get-started)
- [Netlify](https://docs.netlify.com/frameworks/next-js/overview/#next-js-support-on-netlify)
- [Vercel](https://vercel.com/docs/frameworks/nextjs)

> **Note:** We are working on a [Deployment Adapters API](https://github.com/vercel/next.js/discussions/77740) for all platforms to adopt. After completion, we will add documentation on how to write your own adapters.

Was this helpful?

supported.
