# cacheLife and more

# cacheLife

> Learn how to use the cacheLife function to set the cache expiration time for a cached function or component.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)cacheLife

# cacheLife

Last updated  November 21, 2025

The `cacheLife` function is used to set the cache lifetime of a function or component. It should be used alongside the [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) directive, and within the scope of the function or component.

## Usage

### Basic setup

To use `cacheLife`, first enable the [cacheComponentsflag](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) in your `next.config.js` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

`cacheLife` requires the `use cache` directive, which must be placed at the file level or at the top of an async function or component.

> **Good to know**:
>
>
>
> - If used, `cacheLife` should be placed within the function whose output is being cached, even when the `use cache` directive is at file level
> - Only one `cacheLife` call should execute per function invocation. You can call `cacheLife` in different control flow branches, but ensure only one executes per run. See the [conditional cache lifetimes](#conditional-cache-lifetimes) example

### Using preset profiles

Next.js provides preset cache profiles that cover common caching needs. Each profile balances three factors:

- How long users see cached content without checking for updates (client-side)
- How often fresh content is generated on the server
- When old content expires completely

Choose a profile based on how frequently your content changes:

- **seconds** - Real-time data (stock prices, live scores)
- **minutes** - Frequently updated (social feeds, news)
- **hours** - Multiple daily updates (product inventory, weather)
- **days** - Daily updates (blog posts, articles)
- **weeks** - Weekly updates (podcasts, newsletters)
- **max** - Rarely changes (legal pages, archived content)

Import `cacheLife` and pass a profile name:

 app/blog/page.tsx

```
'use cache'
import { cacheLife } from 'next/cache'

export default async function BlogPage() {
  cacheLife('days') // Blog content updated daily

  const posts = await getBlogPosts()
  return <div>{/* render posts */}</div>
}
```

The profile name tells Next.js how to cache the entire function's output. If you don't call `cacheLife`, the `default` profile is used. See [preset cache profiles](#preset-cache-profiles) for timing details.

## Reference

### Cache profile properties

Cache profiles control caching behavior through three timing properties:

- **stale**: How long the client can use cached data without checking the server
- **revalidate**: After this time, the next request will trigger a background refresh
- **expire**: After this time with no requests, the next one waits for fresh content

#### stale

**Client-side:** How long the client can use cached data without checking the server.

During this time, the client-side router displays cached content immediately without any network request. After this period expires, the router must check with the server on the next navigation or request. This provides instant page loads from the client cache, but data may be outdated.

```
cacheLife({ stale: 300 }) // 5 minutes
```

#### revalidate

How often the server regenerates cached content in the background.

- When a request arrives after this period, the server:
  1. Serves the cached version immediately (if available)
  2. Regenerates content in the background
  3. Updates the cache with fresh content
- Similar to [Incremental Static Regeneration (ISR)](https://nextjs.org/docs/app/guides/incremental-static-regeneration)

```
cacheLife({ revalidate: 900 }) // 15 minutes
```

#### expire

Maximum time before the server must regenerate cached content.

- After this period with no traffic, the server regenerates content synchronously on the next request
- When you set both `revalidate` and `expire`, `expire` must be longer than `revalidate`. Next.js validates this and raises an error for invalid configurations.

```
cacheLife({ expire: 3600 }) // 1 hour
```

### Preset cache profiles

If you don't specify a profile, Next.js uses the `default` profile. We recommend explicitly setting a profile to make caching behavior clear.

| Profile | Use Case | stale | revalidate | expire |
| --- | --- | --- | --- | --- |
| default | Standard content | 5 minutes | 15 minutes | 1 year |
| seconds | Real-time data | 30 seconds | 1 second | 1 minute |
| minutes | Frequently updated content | 5 minutes | 1 minute | 1 hour |
| hours | Content updated multiple times per day | 5 minutes | 1 hour | 1 day |
| days | Content updated daily | 5 minutes | 1 day | 1 week |
| weeks | Content updated weekly | 5 minutes | 1 week | 30 days |
| max | Stable content that rarely changes | 5 minutes | 30 days | 1 year |

### Custom cache profiles

Define reusable cache profiles in your `next.config.ts` file:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
  cacheLife: {
    biweekly: {
      stale: 60 * 60 * 24 * 14, // 14 days
      revalidate: 60 * 60 * 24, // 1 day
      expire: 60 * 60 * 24 * 14, // 14 days
    },
  },
}

export default nextConfig
```

The example above caches for 14 days, checks for updates daily, and expires the cache after 14 days. You can then reference this profile throughout your application by its name:

 app/page.tsx

```
'use cache'
import { cacheLife } from 'next/cache'

export default async function Page() {
  cacheLife('biweekly')
  return <div>Page</div>
}
```

### Overriding the default cache profiles

While the default cache profiles provide a useful way to think about how fresh or stale any given part of cacheable output can be, you may prefer different named profiles to better align with your applications caching strategies.

You can override the default named cache profiles by creating a new configuration with the same name as the defaults.

The example below shows how to override the default `"days"` cache profile:

 next.config.ts

```
const nextConfig = {
  cacheComponents: true,
  cacheLife: {
    // Override the 'days' profile
    days: {
      stale: 3600, // 1 hour
      revalidate: 900, // 15 minutes
      expire: 86400, // 1 day
    },
  },
}

export default nextConfig
```

### Inline cache profiles

For one-off cases, pass a profile object directly to `cacheLife`:

 app/page.tsx

```
'use cache'
import { cacheLife } from 'next/cache'

export default async function Page() {
  cacheLife({
    stale: 3600,
    revalidate: 900,
    expire: 86400,
  })

  return <div>Page</div>
}
```

Inline profiles apply only to the specific function or component. For reusable configurations, define custom profiles in `next.config.ts`.

Using `cacheLife({})` with an empty object applies the `default` profile values.

### Client router cache behavior

The `stale` property controls the client-side router cache, not the `Cache-Control` header:

- The server sends the stale time via the `x-nextjs-stale-time` response header
- The client router uses this value to determine when to revalidate
- **Minimum of 30 seconds is enforced** to ensure prefetched links remain usable

This 30-second minimum prevents prefetched data from expiring before users can click on links. It only applies to time-based expiration.

When you call revalidation functions from a Server Action ([revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag), [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath), [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag), or [refresh](https://nextjs.org/docs/app/api-reference/functions/refresh)), the entire client cache is immediately cleared, bypassing the stale time.

> **Good to know**: The `stale` property in `cacheLife` differs from [staleTimes](https://nextjs.org/docs/app/api-reference/config/next-config-js/staleTimes). While `staleTimes` is a global setting affecting all routes, `cacheLife` allows per-function or per-route configuration. Updating `staleTimes.static` also updates the `stale` value of the `default` cache profile.

## Examples

### Using preset profiles

The simplest way to configure caching is using preset profiles. Choose one that matches your content's update pattern:

 app/blog/[slug]/page.tsx

```
import { cacheLife } from 'next/cache'

export default async function BlogPost() {
  'use cache'
  cacheLife('days') // Blog posts updated daily

  const post = await fetchBlogPost()
  return <article>{post.content}</article>
}
```

 app/products/[id]/page.tsx

```
import { cacheLife } from 'next/cache'

export default async function ProductPage() {
  'use cache'
  cacheLife('hours') // Product data updated multiple times per day

  const product = await fetchProduct()
  return <div>{product.name}</div>
}
```

### Custom profiles for specific needs

Define custom profiles when preset options don't match your requirements:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
  cacheLife: {
    editorial: {
      stale: 600, // 10 minutes
      revalidate: 3600, // 1 hour
      expire: 86400, // 1 day
    },
    marketing: {
      stale: 300, // 5 minutes
      revalidate: 1800, // 30 minutes
      expire: 43200, // 12 hours
    },
  },
}

export default nextConfig
```

Then use these profiles throughout your application:

 app/editorial/page.tsx

```
import { cacheLife } from 'next/cache'

export default async function EditorialPage() {
  'use cache'
  cacheLife('editorial')
  // ...
}
```

### Inline profiles for unique cases

Use inline profiles when a specific function needs one-off caching behavior:

 app/api/limited-offer/route.ts

```
import { cacheLife } from 'next/cache'
import { getDb } from '@lib/db'

async function getLimitedOffer() {
  'use cache'

  cacheLife({
    stale: 60, // 1 minute
    revalidate: 300, // 5 minutes
    expire: 3600, // 1 hour
  })

  const offer = await getDb().offer.findFirst({
    where: { type: 'limited' },
    orderBy: { created_at: 'desc' },
  })

  return offer
}

export async function GET() {
  const offer = await getLimitedOffer()

  return Response.json(offer)
}
```

### Caching individual functions

Apply caching to utility functions for granular control:

 lib/api.ts

```
import { cacheLife } from 'next/cache'

export async function getSettings() {
  'use cache'
  cacheLife('max') // Settings rarely change

  return await fetchSettings()
}
```

 lib/stats.ts

```
import { cacheLife } from 'next/cache'

export async function getRealtimeStats() {
  'use cache'
  cacheLife('seconds') // Stats update constantly

  return await fetchStats()
}
```

### Nested caching behavior

When you nest `use cache` directives (a cached function or component using another cached function or component), the outer cache's behavior depends on whether it has an explicit `cacheLife`.

#### With explicit outer cacheLife

The outer cache uses its own lifetime, regardless of inner cache lifetimes. When the outer cache hits, it returns the complete output including all nested data. An explicit `cacheLife` always takes precedence, whether it's longer or shorter than inner lifetimes.

 app/dashboard/page.tsx

```
import { cacheLife } from 'next/cache'
import { Widget } from './widget'

export default async function Dashboard() {
  'use cache'
  cacheLife('hours') // Outer scope sets its own lifetime

  return (
    <div>
      <h1>Dashboard</h1>
      <Widget /> {/* Inner scope has 'minutes' lifetime */}
    </div>
  )
}
```

#### Without explicit outer cacheLife

If you don't call `cacheLife` in the outer cache, it uses the `default` profile (15 min revalidate). Inner caches with shorter lifetimes can reduce the outer cache's `default` lifetime. Inner caches with longer lifetimes cannot extend it beyond the default.

 app/dashboard/page.tsx

```
import { Widget } from './widget'

export default async function Dashboard() {
  'use cache'
  // No cacheLife call - uses default (15 min)
  // If Widget has 5 min → Dashboard becomes 5 min
  // If Widget has 1 hour → Dashboard stays 15 min

  return (
    <div>
      <h1>Dashboard</h1>
      <Widget />
    </div>
  )
}
```

**It is recommended to specify an explicitcacheLife.** With explicit lifetime values, you can inspect a cached function or component and immediately know its behavior without tracing through nested caches. Without explicit lifetime values, the behavior becomes dependent on inner cache lifetimes, making it harder to reason about.

### Conditional cache lifetimes

You can call `cacheLife` conditionally in different code paths to set different cache durations based on your application logic:

 lib/posts.ts

```
import { cacheLife, cacheTag } from 'next/cache'

async function getPostContent(slug: string) {
  'use cache'

  const post = await fetchPost(slug)

  // Tag the cache entry for targeted revalidation
  cacheTag(`post-${slug}`)

  if (!post) {
    // Content may not be published yet or could be in draft
    // Cache briefly to reduce database load
    cacheLife('minutes')
    return null
  }

  // Published content can be cached longer
  cacheLife('days')

  // Return only the necessary data to keep cache size minimal
  return post.data
}
```

This pattern is useful when different outcomes need different cache durations, for example, when an item is missing but is likely to be available later.

#### Using dynamic cache lifetimes from data

If you want to calculate cache lifetime at runtime, for example by reading it from the fetched data, use an [inline cache profile](#inline-cache-profiles) object:

 lib/posts.ts

```
import { cacheLife, cacheTag } from 'next/cache'

async function getPostContent(slug: string) {
  'use cache'

  const post = await fetchPost(slug)
  cacheTag(`post-${slug}`)

  if (!post) {
    cacheLife('minutes')
    return null
  }

  // Use cache timing from CMS data directly as an object
  cacheLife({
    // Ensure post.revalidateSeconds is a number in seconds
    revalidate: post.revalidateSeconds ?? 3600,
  })

  return post.data
}
```

## Related

View related API references.[cacheComponentsLearn how to enable the cacheComponents flag in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)[use cacheLearn how to use the "use cache" directive to cache data in your Next.js application.](https://nextjs.org/docs/app/api-reference/directives/use-cache)[revalidateTagAPI Reference for the revalidateTag function.](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)[cacheTagLearn how to use the cacheTag function to manage cache invalidation in your Next.js application.](https://nextjs.org/docs/app/api-reference/functions/cacheTag)

Was this helpful?

supported.

---

# cacheTag

> Learn how to use the cacheTag function to manage cache invalidation in your Next.js application.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)cacheTag

# cacheTag

Last updated  October 22, 2025

The `cacheTag` function allows you to tag cached data for on-demand invalidation. By associating tags with cache entries, you can selectively purge or revalidate specific cache entries without affecting other cached data.

## Usage

To use `cacheTag`, enable the [cacheComponentsflag](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) in your `next.config.js` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

The `cacheTag` function takes one or more string values.

 app/data.tsJavaScriptTypeScript

```
import { cacheTag } from 'next/cache'

export async function getData() {
  'use cache'
  cacheTag('my-data')
  const data = await fetch('/api/data')
  return data
}
```

You can then purge the cache on-demand using [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) API in another function, for example, a [route handler](https://nextjs.org/docs/app/api-reference/file-conventions/route) or [Server Action](https://nextjs.org/docs/app/getting-started/updating-data):

 app/action.tsJavaScriptTypeScript

```
'use server'

import { revalidateTag } from 'next/cache'

export default async function submit() {
  await addPost()
  revalidateTag('my-data')
}
```

## Good to know

- **Idempotent Tags**: Applying the same tag multiple times has no additional effect.
- **Multiple Tags**: You can assign multiple tags to a single cache entry by passing multiple string values to `cacheTag`.

```
cacheTag('tag-one', 'tag-two')
```

- **Limits**: The max length for a custom tag is 256 characters and the max tag items is 128.

## Examples

### Tagging components or functions

Tag your cached data by calling `cacheTag` within a cached function or component:

 app/components/bookings.tsxJavaScriptTypeScript

```
import { cacheTag } from 'next/cache'

interface BookingsProps {
  type: string
}

export async function Bookings({ type = 'haircut' }: BookingsProps) {
  'use cache'
  cacheTag('bookings-data')

  async function getBookingsData() {
    const data = await fetch(`/api/bookings?type=${encodeURIComponent(type)}`)
    return data
  }

  return //...
}
```

### Creating tags from external data

You can use the data returned from an async function to tag the cache entry.

 app/components/bookings.tsxJavaScriptTypeScript

```
import { cacheTag } from 'next/cache'

interface BookingsProps {
  type: string
}

export async function Bookings({ type = 'haircut' }: BookingsProps) {
  async function getBookingsData() {
    'use cache'
    const data = await fetch(`/api/bookings?type=${encodeURIComponent(type)}`)
    cacheTag('bookings-data', data.id)
    return data
  }
  return //...
}
```

### Invalidating tagged cache

Using [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag), you can invalidate the cache for a specific tag when needed:

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { revalidateTag } from 'next/cache'

export async function updateBookings() {
  await updateBookingData()
  revalidateTag('bookings-data')
}
```

## Related

View related API references.[cacheComponentsLearn how to enable the cacheComponents flag in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)[use cacheLearn how to use the "use cache" directive to cache data in your Next.js application.](https://nextjs.org/docs/app/api-reference/directives/use-cache)[revalidateTagAPI Reference for the revalidateTag function.](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)[cacheLifeLearn how to use the cacheLife function to set the cache expiration time for a cached function or component.](https://nextjs.org/docs/app/api-reference/functions/cacheLife)

Was this helpful?

supported.

---

# connection

> API Reference for the connection function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)connection

# connection

Last updated  October 22, 2025

The `connection()` function allows you to indicate rendering should wait for an incoming user request before continuing.

It's useful when a component doesn't use [Dynamic APIs](https://nextjs.org/docs/app/guides/caching#dynamic-rendering), but you want it to be dynamically rendered at runtime and not statically rendered at build time. This usually occurs when you access external information that you intentionally want to change the result of a render, such as `Math.random()` or `new Date()`.

 app/page.tsxJavaScriptTypeScript

```
import { connection } from 'next/server'

export default async function Page() {
  await connection()
  // Everything below will be excluded from prerendering
  const rand = Math.random()
  return <span>{rand}</span>
}
```

## Reference

### Type

```
function connection(): Promise<void>
```

### Parameters

- The function does not accept any parameters.

### Returns

- The function returns a `void` Promise. It is not meant to be consumed.

## Good to know

- `connection` replaces [unstable_noStore](https://nextjs.org/docs/app/api-reference/functions/unstable_noStore) to better align with the future of Next.js.
- The function is only necessary when dynamic rendering is required and common Dynamic APIs are not used.

### Version History

| Version | Changes |
| --- | --- |
| v15.0.0 | connectionstabilized. |
| v15.0.0-RC | connectionintroduced. |

Was this helpful?

supported.

---

# cookies

> API Reference for the cookies function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)cookies

# cookies

Last updated  January 23, 2026

`cookies` is an **async** function that allows you to read the HTTP incoming request cookies in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), and read/write outgoing request cookies in [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data) or [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route).

 app/page.tsxJavaScriptTypeScript

```
import { cookies } from 'next/headers'

export default async function Page() {
  const cookieStore = await cookies()
  const theme = cookieStore.get('theme')
  return '...'
}
```

## Reference

### Methods

The following methods are available:

| Method | Return Type | Description |
| --- | --- | --- |
| get('name') | Object | Accepts a cookie name and returns an object with the name and value. |
| getAll() | Array of objects | Returns a list of all the cookies with a matching name. |
| has('name') | Boolean | Accepts a cookie name and returns a boolean based on if the cookie exists. |
| set(name, value, options) | - | Accepts a cookie name, value, and options and sets the outgoing request cookie. |
| delete(name) | - | Accepts a cookie name and deletes the cookie. |
| toString() | String | Returns a string representation of the cookies. |

### Options

When setting a cookie, the following properties from the `options` object are supported:

| Option | Type | Description |
| --- | --- | --- |
| name | String | Specifies the name of the cookie. |
| value | String | Specifies the value to be stored in the cookie. |
| expires | Date | Defines the exact date when the cookie will expire. |
| maxAge | Number | Sets the cookie’s lifespan in seconds. |
| domain | String | Specifies the domain where the cookie is available. |
| path | String, default:'/' | Limits the cookie's scope to a specific path within the domain. |
| secure | Boolean | Ensures the cookie is sent only over HTTPS connections for added security. |
| httpOnly | Boolean | Restricts the cookie to HTTP requests, preventing client-side access. |
| sameSite | Boolean,'lax','strict','none' | Controls the cookie's cross-site request behavior. |
| priority | String ("low","medium","high") | Specifies the cookie's priority |
| partitioned | Boolean | Indicates whether the cookie ispartitioned. |

The only option with a default value is `path`.

To learn more about these options, see the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies).

## Good to know

- `cookies` is an **asynchronous** function that returns a promise. You must use `async/await` or React's [use](https://react.dev/reference/react/use) function to access cookies.
  - In version 14 and earlier, `cookies` was a synchronous function. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future.
- `cookies` is a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) whose returned values cannot be known ahead of time. Using it in a layout or page will opt a route into [dynamic rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering).
- The `.delete` method can only be called:
  - In a [Server Function](https://nextjs.org/docs/app/getting-started/updating-data) or [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route).
  - If it belongs to the same domain from which `.set` is called. For wildcard domains, the specific subdomain must be an exact match. Additionally, the code must be executed on the same protocol (HTTP or HTTPS) as the cookie you want to delete.
- HTTP does not allow setting cookies after streaming starts, so you must use `.set` in a [Server Function](https://nextjs.org/docs/app/getting-started/updating-data) or [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route).

## Understanding Cookie Behavior in Server Components

When working with cookies in Server Components, it's important to understand that cookies are fundamentally a client-side storage mechanism:

- **Reading cookies** works in Server Components because you're accessing the cookie data that the client's browser sends to the server in the HTTP request headers.
- **Setting cookies** is not supported during Server Component rendering. To modify cookies, invoke a Server Function from the client or use a Route Handler.

The server can only send instructions (via `Set-Cookie` headers) to tell the browser to store cookies - the actual storage happens on the client side. This is why cookie operations that modify state (`.set`, `.delete`) must be performed in a Server Function or Route Handler where the response headers can be properly set.

## Understanding Cookie Behavior in Server Functions

After you set or delete a cookie in a Server Function, Next.js can return both the updated UI and new data in a single server roundtrip when the function is used as a [Server Action](https://nextjs.org/docs/app/getting-started/updating-data#what-are-server-functions) (e.g., passed to a form's `action` prop). See the [Caching guide](https://nextjs.org/docs/app/guides/caching#cookies).

The UI is not unmounted, but effects that depend on data coming from the server will re-run.

To refresh cached data too, call [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) or [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) inside the function.

## Examples

### Getting a cookie

You can use the `(await cookies()).get('name')` method to get a single cookie:

 app/page.tsxJavaScriptTypeScript

```
import { cookies } from 'next/headers'

export default async function Page() {
  const cookieStore = await cookies()
  const theme = cookieStore.get('theme')
  return '...'
}
```

### Getting all cookies

You can use the `(await cookies()).getAll()` method to get all cookies with a matching name. If `name` is unspecified, it returns all the available cookies.

 app/page.tsxJavaScriptTypeScript

```
import { cookies } from 'next/headers'

export default async function Page() {
  const cookieStore = await cookies()
  return cookieStore.getAll().map((cookie) => (
    <div key={cookie.name}>
      <p>Name: {cookie.name}</p>
      <p>Value: {cookie.value}</p>
    </div>
  ))
}
```

### Setting a cookie

You can use the `(await cookies()).set(name, value, options)` method in a [Server Function](https://nextjs.org/docs/app/getting-started/updating-data) or [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route) to set a cookie. The [optionsobject](#options) is optional.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { cookies } from 'next/headers'

export async function create(data) {
  const cookieStore = await cookies()

  cookieStore.set('name', 'lee')
  // or
  cookieStore.set('name', 'lee', { secure: true })
  // or
  cookieStore.set({
    name: 'name',
    value: 'lee',
    httpOnly: true,
    path: '/',
  })
}
```

### Checking if a cookie exists

You can use the `(await cookies()).has(name)` method to check if a cookie exists:

 app/page.tsJavaScriptTypeScript

```
import { cookies } from 'next/headers'

export default async function Page() {
  const cookieStore = await cookies()
  const hasCookie = cookieStore.has('theme')
  return '...'
}
```

### Deleting cookies

There are three ways you can delete a cookie.

Using the `delete()` method:

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { cookies } from 'next/headers'

export async function deleteCookie(data) {
  const cookieStore = await cookies()
  cookieStore.delete('name')
}
```

Setting a new cookie with the same name and an empty value:

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { cookies } from 'next/headers'

export async function deleteCookie(data) {
  const cookieStore = await cookies()
  cookieStore.set('name', '')
}
```

Setting the `maxAge` to 0 will immediately expire a cookie. `maxAge` accepts a value in seconds.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { cookies } from 'next/headers'

export async function deleteCookie(data) {
  const cookieStore = await cookies()
  cookieStore.set('name', 'value', { maxAge: 0 })
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0-RC | cookiesis now an async function. Acodemodis available. |
| v13.0.0 | cookiesintroduced. |

Was this helpful?

supported.

---

# draftMode

> API Reference for the draftMode function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)draftMode

# draftMode

Last updated  June 16, 2025

`draftMode` is an **async** function allows you to enable and disable [Draft Mode](https://nextjs.org/docs/app/guides/draft-mode), as well as check if Draft Mode is enabled in a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components).

 app/page.tsJavaScriptTypeScript

```
import { draftMode } from 'next/headers'

export default async function Page() {
  const { isEnabled } = await draftMode()
}
```

## Reference

The following methods and properties are available:

| Method | Description |
| --- | --- |
| isEnabled | A boolean value that indicates if Draft Mode is enabled. |
| enable() | Enables Draft Mode in a Route Handler by setting a cookie (__prerender_bypass). |
| disable() | Disables Draft Mode in a Route Handler by deleting a cookie. |

## Good to know

- `draftMode` is an **asynchronous** function that returns a promise. You must use `async/await` or React's [use](https://react.dev/reference/react/use) function.
  - In version 14 and earlier, `draftMode` was a synchronous function. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future.
- A new bypass cookie value will be generated each time you run `next build`. This ensures that the bypass cookie can’t be guessed.
- To test Draft Mode locally over HTTP, your browser will need to allow third-party cookies and local storage access.

## Examples

### Enabling Draft Mode

To enable Draft Mode, create a new [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route) and call the `enable()` method:

 app/draft/route.tsJavaScriptTypeScript

```
import { draftMode } from 'next/headers'

export async function GET(request: Request) {
  const draft = await draftMode()
  draft.enable()
  return new Response('Draft mode is enabled')
}
```

### Disabling Draft Mode

By default, the Draft Mode session ends when the browser is closed.

To disable Draft Mode manually, call the `disable()` method in your [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route):

 app/draft/route.tsJavaScriptTypeScript

```
import { draftMode } from 'next/headers'

export async function GET(request: Request) {
  const draft = await draftMode()
  draft.disable()
  return new Response('Draft mode is disabled')
}
```

Then, send a request to invoke the Route Handler. If calling the route using the [<Link>component](https://nextjs.org/docs/app/api-reference/components/link), you must pass `prefetch={false}` to prevent accidentally deleting the cookie on prefetch.

### Checking if Draft Mode is enabled

You can check if Draft Mode is enabled in a Server Component with the `isEnabled` property:

 app/page.tsJavaScriptTypeScript

```
import { draftMode } from 'next/headers'

export default async function Page() {
  const { isEnabled } = await draftMode()
  return (
    <main>
      <h1>My Blog Post</h1>
      <p>Draft Mode is currently {isEnabled ? 'Enabled' : 'Disabled'}</p>
    </main>
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0-RC | draftModeis now an async function. Acodemodis available. |
| v13.4.0 | draftModeintroduced. |

## Next Steps

Learn how to use Draft Mode with this step-by-step guide.[Draft ModeNext.js has draft mode to toggle between static and dynamic pages. You can learn how it works with App Router here.](https://nextjs.org/docs/app/guides/draft-mode)

Was this helpful?

supported.

---

# fetch

> API reference for the extended fetch function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)fetch

# fetch

Last updated  October 22, 2025

Next.js extends the [Webfetch()API](https://developer.mozilla.org/docs/Web/API/Fetch_API) to allow each request on the server to set its own persistent caching and revalidation semantics.

In the browser, the `cache` option indicates how a fetch request will interact with the *browser's* HTTP cache. With this extension, `cache` indicates how a *server-side* fetch request will interact with the framework's persistent [Data Cache](https://nextjs.org/docs/app/guides/caching#data-cache).

You can call `fetch` with `async` and `await` directly within Server Components.

 app/page.tsxJavaScriptTypeScript

```
export default async function Page() {
  let data = await fetch('https://api.vercel.app/blog')
  let posts = await data.json()
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

## fetch(url, options)

Since Next.js extends the [Webfetch()API](https://developer.mozilla.org/docs/Web/API/Fetch_API), you can use any of the [native options available](https://developer.mozilla.org/docs/Web/API/fetch#parameters).

### options.cache

Configure how the request should interact with Next.js [Data Cache](https://nextjs.org/docs/app/guides/caching#data-cache).

```
fetch(`https://...`, { cache: 'force-cache' | 'no-store' })
```

- **auto no cache** (default): Next.js fetches the resource from the remote server on every request in development, but will fetch once during `next build` because the route will be statically prerendered. If [Dynamic APIs](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) are detected on the route, Next.js will fetch the resource on every request.
- **no-store**: Next.js fetches the resource from the remote server on every request, even if Dynamic APIs are not detected on the route.
- **force-cache**: Next.js looks for a matching request in its Data Cache.
  - If there is a match and it is fresh, it will be returned from the cache.
  - If there is no match or a stale match, Next.js will fetch the resource from the remote server and update the cache with the downloaded resource.

### options.next.revalidate

```
fetch(`https://...`, { next: { revalidate: false | 0 | number } })
```

Set the cache lifetime of a resource (in seconds). [Data Cache](https://nextjs.org/docs/app/guides/caching#data-cache).

- **false** - Cache the resource indefinitely. Semantically equivalent to `revalidate: Infinity`. The HTTP cache may evict older resources over time.
- **0** - Prevent the resource from being cached.
- **number** - (in seconds) Specify the resource should have a cache lifetime of at most `n` seconds.

> **Good to know**:
>
>
>
> - If an individual `fetch()` request sets a `revalidate` number lower than the [defaultrevalidate](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#revalidate) of a route, the whole route revalidation interval will be decreased.
> - If two fetch requests with the same URL in the same route have different `revalidate` values, the lower value will be used.
> - Conflicting options such as `{ revalidate: 3600, cache: 'no-store' }` are not allowed, both will be ignored, and in development mode a warning will be printed to the terminal.

### options.next.tags

```
fetch(`https://...`, { next: { tags: ['collection'] } })
```

Set the cache tags of a resource. Data can then be revalidated on-demand using [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag). The max length for a custom tag is 256 characters and the max tag items is 128.

## Troubleshooting

### Fetch defaultauto no storeandcache: 'no-store'not showing fresh data in development

Next.js caches `fetch` responses in Server Components across Hot Module Replacement (HMR) in local development for faster responses and to reduce costs for billed API calls.

By default, the [HMR cache](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverComponentsHmrCache) applies to all fetch requests, including those with the default `auto no cache` and `cache: 'no-store'` option. This means uncached requests will not show fresh data between HMR refreshes. However, the cache will be cleared on navigation or full-page reloads.

See the [serverComponentsHmrCache](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverComponentsHmrCache) docs for more information.

### Hard refresh and caching in development

In development mode, if the request includes the `cache-control: no-cache` header, `options.cache`, `options.next.revalidate`, and `options.next.tags` are ignored, and the `fetch` request is served from the source.

Browsers typically include `cache-control: no-cache` when the cache is disabled in developer tools or during a hard refresh.

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | fetchintroduced. |

Was this helpful?

supported.

---

# forbidden

> API Reference for the forbidden function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)forbidden

# forbidden

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  January 23, 2026

The `forbidden` function throws an error that renders a Next.js 403 error page. It's useful for handling authorization errors in your application. You can customize the UI using the [forbidden.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/forbidden).

To start using `forbidden`, enable the experimental [authInterrupts](https://nextjs.org/docs/app/api-reference/config/next-config-js/authInterrupts) configuration option in your `next.config.js` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    authInterrupts: true,
  },
}

export default nextConfig
```

`forbidden` can be invoked in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data), and [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route).

 app/auth/page.tsxJavaScriptTypeScript

```
import { verifySession } from '@/app/lib/dal'
import { forbidden } from 'next/navigation'

export default async function AdminPage() {
  const session = await verifySession()

  // Check if the user has the 'admin' role
  if (session.role !== 'admin') {
    forbidden()
  }

  // Render the admin page for authorized users
  return <></>
}
```

## Good to know

- The `forbidden` function cannot be called in the [root layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout).

## Examples

### Role-based route protection

You can use `forbidden` to restrict access to certain routes based on user roles. This ensures that users who are authenticated but lack the required permissions cannot access the route.

 app/admin/page.tsxJavaScriptTypeScript

```
import { verifySession } from '@/app/lib/dal'
import { forbidden } from 'next/navigation'

export default async function AdminPage() {
  const session = await verifySession()

  // Check if the user has the 'admin' role
  if (session.role !== 'admin') {
    forbidden()
  }

  // Render the admin page for authorized users
  return (
    <main>
      <h1>Admin Dashboard</h1>
      <p>Welcome, {session.user.name}!</p>
    </main>
  )
}
```

### Mutations with Server Actions

When implementing mutations in Server Actions, you can use `forbidden` to only allow users with a specific role to update sensitive data.

 app/actions/update-role.tsJavaScriptTypeScript

```
'use server'

import { verifySession } from '@/app/lib/dal'
import { forbidden } from 'next/navigation'
import db from '@/app/lib/db'

export async function updateRole(formData: FormData) {
  const session = await verifySession()

  // Ensure only admins can update roles
  if (session.role !== 'admin') {
    forbidden()
  }

  // Perform the role update for authorized users
  // ...
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.1.0 | forbiddenintroduced. |

[forbidden.jsAPI reference for the forbidden.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/forbidden)

Was this helpful?

supported.

---

# generateImageMetadata

> Learn how to generate multiple images in a single Metadata API special file.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)generateImageMetadata

# generateImageMetadata

Last updated  October 8, 2025

You can use `generateImageMetadata` to generate different versions of one image or return multiple images for one route segment. This is useful for when you want to avoid hard-coding metadata values, such as for icons.

## Parameters

`generateImageMetadata` function accepts the following parameters:

#### params(optional)

An object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) object from the root segment down to the segment `generateImageMetadata` is called from.

 icon.tsxJavaScriptTypeScript

```
export function generateImageMetadata({
  params,
}: {
  params: { slug: string }
}) {
  // ...
}
```

| Route | URL | params |
| --- | --- | --- |
| app/shop/icon.js | /shop | undefined |
| app/shop/[slug]/icon.js | /shop/1 | { slug: '1' } |
| app/shop/[tag]/[item]/icon.js | /shop/1/2 | { tag: '1', item: '2' } |

## Returns

The `generateImageMetadata` function should return an `array` of objects containing the image's metadata such as `alt` and `size`. In addition, each item **must** include an `id` value which will be passed as a promise to the props of the image generating function.

| Image Metadata Object | Type |
| --- | --- |
| id | string(required) |
| alt | string |
| size | { width: number; height: number } |
| contentType | string |

 icon.tsxJavaScriptTypeScript

```
import { ImageResponse } from 'next/og'

export function generateImageMetadata() {
  return [
    {
      contentType: 'image/png',
      size: { width: 48, height: 48 },
      id: 'small',
    },
    {
      contentType: 'image/png',
      size: { width: 72, height: 72 },
      id: 'medium',
    },
  ]
}

export default async function Icon({ id }: { id: Promise<string | number> }) {
  const iconId = await id
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 88,
          background: '#000',
          color: '#fafafa',
        }}
      >
        Icon {iconId}
      </div>
    )
  )
}
```

## Image generation function props

When using `generateImageMetadata`, the default export image generation function receives the following props:

#### id

A promise that resolves to the `id` value from one of the items returned by `generateImageMetadata`. The `id` will be a `string` or `number` depending on what was returned from `generateImageMetadata`.

 icon.tsxJavaScriptTypeScript

```
export default async function Icon({ id }: { id: Promise<string | number> }) {
  const iconId = await id
  // Use iconId to generate the image
}
```

#### params(optional)

A promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) from the root segment down to the segment the image is colocated in.

 icon.tsxJavaScriptTypeScript

```
export default async function Icon({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // Use slug to generate the image
}
```

### Examples

#### Using external data

This example uses the `params` object and external data to generate multiple [Open Graph images](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image) for a route segment.

 app/products/[id]/opengraph-image.tsxJavaScriptTypeScript

```
import { ImageResponse } from 'next/og'
import { getCaptionForImage, getOGImages } from '@/app/utils/images'

export async function generateImageMetadata({
  params,
}: {
  params: { id: string }
}) {
  const images = await getOGImages(params.id)

  return images.map((image, idx) => ({
    id: idx,
    size: { width: 1200, height: 600 },
    alt: image.text,
    contentType: 'image/png',
  }))
}

export default async function Image({
  params,
  id,
}: {
  params: Promise<{ id: string }>
  id: Promise<number>
}) {
  const productId = (await params).id
  const imageId = await id
  const text = await getCaptionForImage(productId, imageId)

  return new ImageResponse(
    (
      <div
        style={
          {
            // ...
          }
        }
      >
        {text}
      </div>
    )
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | idpassed to the Image generation function is now a promise that resolves tostringornumber |
| v16.0.0 | paramspassed to the Image generation function is now a promise that resolves to an object |
| v13.3.0 | generateImageMetadataintroduced. |

## Next Steps

View all the Metadata API options.[Metadata FilesAPI documentation for the metadata file conventions.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)

Was this helpful?

supported.
