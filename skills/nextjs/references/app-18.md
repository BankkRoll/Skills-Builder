# refresh and more

# refresh

> API Reference for the refresh function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)refresh

# refresh

Last updated  November 5, 2025

`refresh` allows you to refresh the client router from within a [Server Action](https://nextjs.org/docs/app/getting-started/updating-data).

## Usage

`refresh` can **only** be called from within Server Actions. It cannot be used in Route Handlers, Client Components, or any other context.

## Parameters

```
refresh(): void;
```

## Returns

`refresh` does not return a value.

## Examples

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { refresh } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  const content = formData.get('content')

  // Create the post in your database
  const post = await db.post.create({
    data: { title, content },
  })

  refresh()
}
```

### Error when used outside Server Actions

 app/api/posts/route.tsJavaScriptTypeScript

```
import { refresh } from 'next/cache'

export async function POST() {
  // This will throw an error
  refresh()
}
```

Was this helpful?

supported.

---

# revalidatePath

> API Reference for the revalidatePath function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)revalidatePath

# revalidatePath

Last updated  January 26, 2026

`revalidatePath` allows you to invalidate [cached data](https://nextjs.org/docs/app/guides/caching) on-demand for a specific path.

## Usage

`revalidatePath` can be called in Server Functions and Route Handlers.

`revalidatePath` cannot be called in Client Components or Proxy, as it only works in server environments.

> **Good to know**:
>
>
>
> - **Server Functions**: Updates the UI immediately (if viewing the affected path). Currently, it also causes all previously visited pages to refresh when navigated to again. This behavior is temporary and will be updated in the future to apply only to the specific path.
> - **Route Handlers**: Marks the path for revalidation. The revalidation is done on the next visit to the specified path. This means calling `revalidatePath` with a dynamic route segment will not immediately trigger many revalidations at once. The invalidation only happens when the path is next visited.

## Parameters

```
revalidatePath(path: string, type?: 'page' | 'layout'): void;
```

- `path`: Either a route pattern corresponding to the data you want to revalidate, for example `/product/[slug]`, or a specific URL, `/product/123`. Do not append `/page` or `/layout`, use the `type` parameter instead. Must not exceed 1024 characters. This value is case-sensitive.
- `type`: (optional) `'page'` or `'layout'` string to change the type of path to revalidate. If `path` contains a dynamic segment, for example `/product/[slug]`, this parameter is required. If `path` is a specific URL, `/product/1`, omit `type`.

Use a specific URL when you want to refresh a [single page](#revalidating-a-specific-url). Use a route pattern plus `type` to refresh [multiple URLs](#revalidating-a-page-path).

## Returns

`revalidatePath` does not return a value.

## What can be invalidated

The path parameter can point to pages, layouts, or route handlers:

- **Pages**: Invalidates the specific page
- **Layouts**: Invalidates the layout (the `layout.tsx` at that segment), all nested layouts beneath it, and all pages beneath them
- **Route Handlers**: Invalidates Data Cache entries accessed within route handlers. For example `revalidatePath("/api/data")` invalidates this GET handler:

 app/api/data/route.ts

```
export async function GET() {
  const data = await fetch('https://api.vercel.app/blog', {
    cache: 'force-cache',
  })

  return Response.json(await data.json())
}
```

## Relationship withrevalidateTagandupdateTag

`revalidatePath`, [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) and [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag) serve different purposes:

- **revalidatePath**: Invalidates a specific page or layout path
- **revalidateTag**: Marks data with specific tags as **stale**. Applies across all pages that use those tags
- **updateTag**: Expires data with specific tags. Applies across all pages that use those tags

When you call `revalidatePath`, only the specified path gets fresh data on the next visit. Other pages that use the same data tags will continue to serve cached data until those specific tags are also revalidated:

```
// Page A: /blog
const posts = await fetch('https://api.vercel.app/blog', {
  next: { tags: ['posts'] },
})

// Page B: /dashboard
const recentPosts = await fetch('https://api.vercel.app/blog?limit=5', {
  next: { tags: ['posts'] },
})
```

After calling `revalidatePath('/blog')`:

- **Page A (/blog)**: Shows fresh data (page re-rendered)
- **Page B (/dashboard)**: Still shows stale data (cache tag 'posts' not invalidated)

Learn about the difference between [revalidateTagandupdateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag#differences-from-revalidatetag).

### Building revalidation utilities

`revalidatePath` and `updateTag` are complementary primitives that are often used together in utility functions to ensure comprehensive data consistency across your application:

```
'use server'

import { revalidatePath, updateTag } from 'next/cache'

export async function updatePost() {
  await updatePostInDatabase()

  revalidatePath('/blog') // Refresh the blog page
  updateTag('posts') // Refresh all pages using 'posts' tag
}
```

This pattern ensures that both the specific page and any other pages using the same data remain consistent.

## Examples

### Revalidating a specific URL

```
import { revalidatePath } from 'next/cache'
revalidatePath('/blog/post-1')
```

This will invalidate one specific URL for revalidation on the next page visit.

### Revalidating a Page path

```
import { revalidatePath } from 'next/cache'
revalidatePath('/blog/[slug]', 'page')
// or with route groups
revalidatePath('/(main)/blog/[slug]', 'page')
```

This will invalidate any URL that matches the provided `page` file for revalidation on the next page visit. This will *not* invalidate pages beneath the specific page. For example, `/blog/[slug]` won't invalidate `/blog/[slug]/[author]`.

### Revalidating a Layout path

```
import { revalidatePath } from 'next/cache'
revalidatePath('/blog/[slug]', 'layout')
// or with route groups
revalidatePath('/(main)/post/[slug]', 'layout')
```

This will invalidate any URL that matches the provided `layout` file for revalidation on the next page visit. This will cause pages beneath with the same layout to be invalidated and revalidated on the next visit. For example, in the above case, `/blog/[slug]/[another]` would also be invalidated and revalidated on the next visit.

### Revalidating all data

```
import { revalidatePath } from 'next/cache'

revalidatePath('/', 'layout')
```

This will purge the Client-side Router Cache, and invalidate the Data Cache for revalidation on the next page visit.

### Server Function

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { revalidatePath } from 'next/cache'

export default async function submit() {
  await submitForm()
  revalidatePath('/')
}
```

### Route Handler

 app/api/revalidate/route.tsJavaScriptTypeScript

```
import { revalidatePath } from 'next/cache'
import type { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const path = request.nextUrl.searchParams.get('path')

  if (path) {
    revalidatePath(path)
    return Response.json({ revalidated: true, now: Date.now() })
  }

  return Response.json({
    revalidated: false,
    now: Date.now(),
    message: 'Missing path to revalidate',
  })
}
```

Was this helpful?

supported.

---

# revalidateTag

> API Reference for the revalidateTag function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)revalidateTag

# revalidateTag

Last updated  October 29, 2025

`revalidateTag` allows you to invalidate [cached data](https://nextjs.org/docs/app/guides/caching) on-demand for a specific cache tag.

This function is ideal for content where a slight delay in updates is acceptable, such as blog posts, product catalogs, or documentation. Users receive stale content while fresh data loads in the background.

## Usage

`revalidateTag` can be called in Server Functions and Route Handlers.

`revalidateTag` cannot be called in Client Components or Proxy, as it only works in server environments.

### Revalidation Behavior

The revalidation behavior depends on whether you provide the second argument:

- **Withprofile="max"(recommended)**: The tag entry is marked as stale, and the next time a resource with that tag is visited, it will use stale-while-revalidate semantics. This means the stale content is served while fresh content is fetched in the background.
- **With a custom cache life profile**: For advanced usage, you can specify any cache life profile that your application has defined, allowing for custom revalidation behaviors tailored to your specific caching requirements.
- **Without the second argument (deprecated)**: The tag entry is expired immediately, and the next request to that resource will be a blocking revalidate/cache miss. This behavior is now deprecated, and you should either use `profile="max"` or migrate to [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag).

> **Good to know**: When using `profile="max"`, `revalidateTag` marks tagged data as stale, but fresh data is only fetched when pages using that tag are next visited. This means calling `revalidateTag` will not immediately trigger many revalidations at once. The invalidation only happens when any page using that tag is next visited.

## Parameters

```
revalidateTag(tag: string, profile: string | { expire?: number }): void;
```

- `tag`: A string representing the cache tag associated with the data you want to revalidate. Must not exceed 256 characters. This value is case-sensitive.
- `profile`: A string that specifies the revalidation behavior. The recommended value is `"max"` which provides stale-while-revalidate semantics, or any of the other default or custom profiles defined in [cacheLife](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheLife). Alternatively, you can pass an object with an `expire` property for custom expiration behavior.

Tags must first be assigned to cached data. You can do this in two ways:

- Using the [next.tags](https://nextjs.org/docs/app/guides/caching#fetch-optionsnexttags-and-revalidatetag) option with `fetch` for caching external API requests:

```
fetch(url, { next: { tags: ['posts'] } })
```

- Using [cacheTag](https://nextjs.org/docs/app/api-reference/functions/cacheTag) inside cached functions or components with the `'use cache'` directive:

```
import { cacheTag } from 'next/cache'

async function getData() {
  'use cache'
  cacheTag('posts')
  // ...
}
```

> **Good to know**: The single-argument form `revalidateTag(tag)` is deprecated. It currently works if TypeScript errors are suppressed, but this behavior may be removed in a future version. Update to the two-argument signature.

## Returns

`revalidateTag` does not return a value.

## Relationship withrevalidatePath

`revalidateTag` invalidates data with specific tags across all pages that use those tags, while [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) invalidates specific page or layout paths.

> **Good to know**: These functions serve different purposes and may need to be used together for comprehensive data consistency. For detailed examples and considerations, see [relationship with revalidateTag and updateTag](https://nextjs.org/docs/app/api-reference/functions/revalidatePath#relationship-with-revalidatetag-and-updatetag) for more information.

## Examples

The following examples demonstrate how to use `revalidateTag` in different contexts. In both cases, we're using `profile="max"` to mark data as stale and use stale-while-revalidate semantics, which is the recommended approach for most use cases.

### Server Action

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { revalidateTag } from 'next/cache'

export default async function submit() {
  await addPost()
  revalidateTag('posts', 'max')
}
```

### Route Handler

 app/api/revalidate/route.tsJavaScriptTypeScript

```
import type { NextRequest } from 'next/server'
import { revalidateTag } from 'next/cache'

export async function GET(request: NextRequest) {
  const tag = request.nextUrl.searchParams.get('tag')

  if (tag) {
    revalidateTag(tag, 'max')
    return Response.json({ revalidated: true, now: Date.now() })
  }

  return Response.json({
    revalidated: false,
    now: Date.now(),
    message: 'Missing tag to revalidate',
  })
}
```

> **Good to know**: For webhooks or third-party services that need immediate expiration, you can pass `{ expire: 0 }` as the second argument: `revalidateTag(tag, { expire: 0 })`. This pattern is necessary when external systems call your Route Handlers and require data to expire immediately. For all other cases, it's recommended to use [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag) in Server Actions for immediate updates instead.

Was this helpful?

supported.

---

# unauthorized

> API Reference for the unauthorized function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)unauthorized

# unauthorized

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  January 23, 2026

The `unauthorized` function throws an error that renders a Next.js 401 error page. It's useful for handling authorization errors in your application. You can customize the UI using the [unauthorized.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/unauthorized).

To start using `unauthorized`, enable the experimental [authInterrupts](https://nextjs.org/docs/app/api-reference/config/next-config-js/authInterrupts) configuration option in your `next.config.js` file:

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

`unauthorized` can be invoked in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data), and [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route).

 app/dashboard/page.tsxJavaScriptTypeScript

```
import { verifySession } from '@/app/lib/dal'
import { unauthorized } from 'next/navigation'

export default async function DashboardPage() {
  const session = await verifySession()

  if (!session) {
    unauthorized()
  }

  // Render the dashboard for authenticated users
  return (
    <main>
      <h1>Welcome to the Dashboard</h1>
      <p>Hi, {session.user.name}.</p>
    </main>
  )
}
```

## Good to know

- The `unauthorized` function cannot be called in the [root layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout).

## Examples

### Displaying login UI to unauthenticated users

You can use `unauthorized` function to display the `unauthorized.js` file with a login UI.

 app/dashboard/page.tsxJavaScriptTypeScript

```
import { verifySession } from '@/app/lib/dal'
import { unauthorized } from 'next/navigation'

export default async function DashboardPage() {
  const session = await verifySession()

  if (!session) {
    unauthorized()
  }

  return <div>Dashboard</div>
}
```

   app/unauthorized.tsxJavaScriptTypeScript

```
import Login from '@/app/components/Login'

export default function UnauthorizedPage() {
  return (
    <main>
      <h1>401 - Unauthorized</h1>
      <p>Please log in to access this page.</p>
      <Login />
    </main>
  )
}
```

### Mutations with Server Actions

You can invoke `unauthorized` in Server Actions to ensure only authenticated users can perform specific mutations.

 app/actions/update-profile.tsJavaScriptTypeScript

```
'use server'

import { verifySession } from '@/app/lib/dal'
import { unauthorized } from 'next/navigation'
import db from '@/app/lib/db'

export async function updateProfile(data: FormData) {
  const session = await verifySession()

  // If the user is not authenticated, return a 401
  if (!session) {
    unauthorized()
  }

  // Proceed with mutation
  // ...
}
```

### Fetching data with Route Handlers

You can use `unauthorized` in Route Handlers to ensure only authenticated users can access the endpoint.

 app/api/profile/route.tsJavaScriptTypeScript

```
import { NextRequest, NextResponse } from 'next/server'
import { verifySession } from '@/app/lib/dal'
import { unauthorized } from 'next/navigation'

export async function GET(req: NextRequest): Promise<NextResponse> {
  // Verify the user's session
  const session = await verifySession()

  // If no session exists, return a 401 and render unauthorized.tsx
  if (!session) {
    unauthorized()
  }

  // Fetch data
  // ...
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.1.0 | unauthorizedintroduced. |

[unauthorized.jsAPI reference for the unauthorized.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/unauthorized)

Was this helpful?

supported.

---

# unstable_cache

> API Reference for the unstable_cache function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)unstable_cache

# unstable_cache

Last updated  June 16, 2025

> **Warning:** This API will be replaced by [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) when it reaches stability.

`unstable_cache` allows you to cache the results of expensive operations, like database queries, and reuse them across multiple requests.

```
import { getUser } from './data';
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (id) => getUser(id),
  ['my-app-user']
);

export default async function Component({ userID }) {
  const user = await getCachedUser(userID);
  ...
}
```

> **Good to know**:
>
>
>
> - Accessing dynamic data sources such as `headers` or `cookies` inside a cache scope is not supported. If you need this data inside a cached function use `headers` outside of the cached function and pass the required dynamic data in as an argument.
> - This API uses Next.js' built-in [Data Cache](https://nextjs.org/docs/app/guides/caching#data-cache) to persist the result across requests and deployments.

## Parameters

```
const data = unstable_cache(fetchData, keyParts, options)()
```

- `fetchData`: This is an asynchronous function that fetches the data you want to cache. It must be a function that returns a `Promise`.
- `keyParts`: This is an extra array of keys that further adds identification to the cache. By default, `unstable_cache` already uses the arguments and the stringified version of your function as the cache key. It is optional in most cases; the only time you need to use it is when you use external variables without passing them as parameters. However, it is important to add closures used within the function if you do not pass them as parameters.
- `options`: This is an object that controls how the cache behaves. It can contain the following properties:
  - `tags`: An array of tags that can be used to control cache invalidation. Next.js will not use this to uniquely identify the function.
  - `revalidate`: The number of seconds after which the cache should be revalidated. Omit or pass `false` to cache indefinitely or until matching `revalidateTag()` or `revalidatePath()` methods are called.

## Returns

`unstable_cache` returns a function that when invoked, returns a Promise that resolves to the cached data. If the data is not in the cache, the provided function will be invoked, and its result will be cached and returned.

## Example

 app/page.tsxJavaScriptTypeScript

```
import { unstable_cache } from 'next/cache'

export default async function Page({
  params,
}: {
  params: Promise<{ userId: string }>
}) {
  const { userId } = await params
  const getCachedUser = unstable_cache(
    async () => {
      return { id: userId }
    },
    [userId], // add the user ID to the cache key
    {
      tags: ['users'],
      revalidate: 60,
    }
  )

  //...
}
```

## Version History

| Version | Changes |
| --- | --- |
| v14.0.0 | unstable_cacheintroduced. |

Was this helpful?

supported.

---

# unstable_noStore

> API Reference for the unstable_noStore function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)unstable_noStore

# unstable_noStore

This is a legacy API and no longer recommended. It's still supported for backward compatibility.Last updated  June 16, 2025

**In version 15, we recommend usingconnectioninstead ofunstable_noStore.**

`unstable_noStore` can be used to declaratively opt out of static rendering and indicate a particular component should not be cached.

```
import { unstable_noStore as noStore } from 'next/cache';

export default async function ServerComponent() {
  noStore();
  const result = await db.query(...);
  ...
}
```

> **Good to know**:
>
>
>
> - `unstable_noStore` is equivalent to `cache: 'no-store'` on a `fetch`
> - `unstable_noStore` is preferred over `export const dynamic = 'force-dynamic'` as it is more granular and can be used on a per-component basis

- Using `unstable_noStore` inside [unstable_cache](https://nextjs.org/docs/app/api-reference/functions/unstable_cache) will not opt out of static generation. Instead, it will defer to the cache configuration to determine whether to cache the result or not.

## Usage

If you prefer not to pass additional options to `fetch`, like `cache: 'no-store'`, `next: { revalidate: 0 }` or in cases where `fetch` is not available, you can use `noStore()` as a replacement for all of these use cases.

```
import { unstable_noStore as noStore } from 'next/cache';

export default async function ServerComponent() {
  noStore();
  const result = await db.query(...);
  ...
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0 | unstable_noStoredeprecated forconnection. |
| v14.0.0 | unstable_noStoreintroduced. |

Was this helpful?

supported.

---

# unstable_rethrow

> API Reference for the unstable_rethrow function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)unstable_rethrow

# unstable_rethrow

This feature is currently unstable and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  July 1, 2025

`unstable_rethrow` can be used to avoid catching internal errors thrown by Next.js when attempting to handle errors thrown in your application code.

For example, calling the `notFound` function will throw an internal Next.js error and render the [not-found.js](https://nextjs.org/docs/app/api-reference/file-conventions/not-found) component. However, if used inside the `try` block of a `try/catch` statement, the error will be caught, preventing `not-found.js` from rendering:

 @/app/ui/component.tsx

```
import { notFound } from 'next/navigation'

export default async function Page() {
  try {
    const post = await fetch('https://.../posts/1').then((res) => {
      if (res.status === 404) notFound()
      if (!res.ok) throw new Error(res.statusText)
      return res.json()
    })
  } catch (err) {
    console.error(err)
  }
}
```

You can use `unstable_rethrow` API to re-throw the internal error and continue with the expected behavior:

 @/app/ui/component.tsx

```
import { notFound, unstable_rethrow } from 'next/navigation'

export default async function Page() {
  try {
    const post = await fetch('https://.../posts/1').then((res) => {
      if (res.status === 404) notFound()
      if (!res.ok) throw new Error(res.statusText)
      return res.json()
    })
  } catch (err) {
    unstable_rethrow(err)
    console.error(err)
  }
}
```

The following Next.js APIs rely on throwing an error which should be rethrown and handled by Next.js itself:

- [notFound()](https://nextjs.org/docs/app/api-reference/functions/not-found)
- [redirect()](https://nextjs.org/docs/app/guides/redirecting#redirect-function)
- [permanentRedirect()](https://nextjs.org/docs/app/guides/redirecting#permanentredirect-function)

If a route segment is marked to throw an error unless it's static, a Dynamic API call will also throw an error that should similarly not be caught by the developer. Note that Partial Prerendering (PPR) affects this behavior as well. These APIs are:

- [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies)
- [headers](https://nextjs.org/docs/app/api-reference/functions/headers)
- [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional)
- `fetch(..., { cache: 'no-store' })`
- `fetch(..., { next: { revalidate: 0 } })`

> **Good to know**:
>
>
>
> - This method should be called at the top of the catch block, passing the error object as its only argument. It can also be used within a `.catch` handler of a promise.
> - You may be able to avoid using `unstable_rethrow` if you encapsulate your API calls that throw and let the **caller** handle the exception.
> - Only use `unstable_rethrow` if your caught exceptions may include both application errors and framework-controlled exceptions (like `redirect()` or `notFound()`).
> - Any resource cleanup (like clearing intervals, timers, etc) would have to either happen prior to the call to `unstable_rethrow` or within a `finally` block.

Was this helpful?

supported.

---

# updateTag

> API Reference for the updateTag function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)updateTag

# updateTag

Last updated  October 16, 2025

`updateTag` allows you to update [cached data](https://nextjs.org/docs/app/guides/caching) on-demand for a specific cache tag from within [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data).

This function is designed for **read-your-own-writes** scenarios, where a user makes a change (like creating a post), and the UI immediately shows the change, rather than stale data.

## Usage

`updateTag` can **only** be called from within [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data). It cannot be used in Route Handlers, Client Components, or any other context.

If you need to invalidate cache tags in Route Handlers or other contexts, use [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) instead.

> **Good to know**: `updateTag` immediately expires the cached data for the specified tag. The next request will wait to fetch fresh data rather than serving stale content from the cache, ensuring users see their changes immediately.

## Parameters

```
updateTag(tag: string): void;
```

- `tag`: A string representing the cache tag associated with the data you want to update. Must not exceed 256 characters. This value is case-sensitive.

Tags must first be assigned to cached data. You can do this in two ways:

- Using the [next.tags](https://nextjs.org/docs/app/guides/caching#fetch-optionsnexttags-and-revalidatetag) option with `fetch` for caching external API requests:

```
fetch(url, { next: { tags: ['posts'] } })
```

- Using [cacheTag](https://nextjs.org/docs/app/api-reference/functions/cacheTag) inside cached functions or components with the `'use cache'` directive:

```
import { cacheTag } from 'next/cache'

async function getData() {
  'use cache'
  cacheTag('posts')
  // ...
}
```

## Returns

`updateTag` does not return a value.

## Differences from revalidateTag

While both `updateTag` and `revalidateTag` invalidate cached data, they serve different purposes:

- **updateTag**:
  - Can only be used in Server Actions
  - Next request waits for fresh data (no stale content served)
  - Designed for read-your-own-writes scenarios
- **revalidateTag**:
  - Can be used in Server Actions and Route Handlers
  - With `profile="max"` (recommended): Serves cached data while fetching fresh data in the background (stale-while-revalidate)
  - With custom profile: Can be configured to any cache life profile for advanced usage
  - Without profile: legacy behavior which is equivalent to `updateTag`

## Examples

### Server Action with Read-Your-Own-Writes

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { updateTag } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  const content = formData.get('content')

  // Create the post in your database
  const post = await db.post.create({
    data: { title, content },
  })

  // Invalidate cache tags so the new post is immediately visible
  // 'posts' tag: affects any page that displays a list of posts
  updateTag('posts')
  // 'post-{id}' tag: affects the individual post detail page
  updateTag(`post-${post.id}`)

  // Redirect to the new post - user will see fresh data, not cached
  redirect(`/posts/${post.id}`)
}
```

### Error when used outside Server Actions

 app/api/posts/route.tsJavaScriptTypeScript

```
import { updateTag } from 'next/cache'

export async function POST() {
  // This will throw an error
  updateTag('posts')
  // Error: updateTag can only be called from within a Server Action

  // Use revalidateTag instead in Route Handlers
  revalidateTag('posts', 'max')
}
```

## When to use updateTag

Use `updateTag` when:

- You're in a Server Action
- You need immediate cache invalidation for read-your-own-writes
- You want to ensure the next request sees updated data

Use `revalidateTag` instead when:

- You're in a Route Handler or other non-action context
- You want stale-while-revalidate semantics
- You're building a webhook or API endpoint for cache invalidation

## Related

- [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) - For invalidating tags in Route Handlers
- [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) - For invalidating specific paths

Was this helpful?

supported.

---

# useLinkStatus

> API Reference for the useLinkStatus hook.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)useLinkStatus

# useLinkStatus

Last updated  September 2, 2025

The `useLinkStatus` hook lets you track the **pending** state of a `<Link>`. Use it for subtle, inline feedback, for example a shimmer effect over the clicked link, while navigation completes. Prefer route-level fallbacks with `loading.js`, and prefetching for instant transitions.

`useLinkStatus` is useful when:

- [Prefetching](https://nextjs.org/docs/app/getting-started/linking-and-navigating#prefetching) is disabled or in progress meaning navigation is blocked.
- The destination route is dynamic **and** doesn't include a [loading.js](https://nextjs.org/docs/app/api-reference/file-conventions/loading) file that would allow an instant navigation.

 app/hint.tsxJavaScriptTypeScript

```
'use client'

import Link from 'next/link'
import { useLinkStatus } from 'next/link'

function Hint() {
  const { pending } = useLinkStatus()
  return (
    <span aria-hidden className={`link-hint ${pending ? 'is-pending' : ''}`} />
  )
}

export default function Header() {
  return (
    <header>
      <Link href="/dashboard" prefetch={false}>
        <span className="label">Dashboard</span> <Hint />
      </Link>
    </header>
  )
}
```

> **Good to know**:
>
>
>
> - `useLinkStatus` must be used within a descendant component of a `Link` component
> - The hook is most useful when `prefetch={false}` is set on the `Link` component
> - If the linked route has been prefetched, the pending state will be skipped
> - When clicking multiple links in quick succession, only the last link's pending state is shown
> - This hook is not supported in the Pages Router and always returns `{ pending: false }`
> - Inline indicators can easily introduce layout shifts. Prefer a fixed-size, always-rendered hint element and toggle its opacity, or use an animation.

## You might not needuseLinkStatus

Before adding inline feedback, consider if:

- The destination is static and prefetched in production, so the pending phase may be skipped.
- The route has a `loading.js` file, enabling instant transitions with a route-level fallback.

Navigation is typically fast. Use `useLinkStatus` as a quick patch when you identify a slow transition, then iterate to fix the root cause with prefetching or a `loading.js` fallback.

## Parameters

```
const { pending } = useLinkStatus()
```

`useLinkStatus` does not take any parameters.

## Returns

`useLinkStatus` returns an object with a single property:

| Property | Type | Description |
| --- | --- | --- |
| pending | boolean | truebefore history updates,falseafter |

## Example

### Inline link hint

Add a subtle, fixed-size hint that doesn’t affect layout to confirm a click when prefetching hasn’t completed.

 app/components/loading-indicator.tsxJavaScriptTypeScript

```
'use client'

import { useLinkStatus } from 'next/link'

export default function LoadingIndicator() {
  const { pending } = useLinkStatus()
  return (
    <span aria-hidden className={`link-hint ${pending ? 'is-pending' : ''}`} />
  )
}
```

   app/shop/layout.tsxJavaScriptTypeScript

```
import Link from 'next/link'
import LoadingIndicator from './components/loading-indicator'

const links = [
  { href: '/shop/electronics', label: 'Electronics' },
  { href: '/shop/clothing', label: 'Clothing' },
  { href: '/shop/books', label: 'Books' },
]

function Menubar() {
  return (
    <div>
      {links.map((link) => (
        <Link key={link.label} href={link.href}>
          <span className="label">{link.label}</span> <LoadingIndicator />
        </Link>
      ))}
    </div>
  )
}

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <Menubar />
      {children}
    </div>
  )
}
```

## Gracefully handling fast navigation

If the navigation to a new route is fast, users may see an unnecessary flash of the hint. One way to improve the user experience and only show the hint when the navigation takes time to complete is to add an initial animation delay (e.g. 100ms) and start the animation as invisible (e.g. `opacity: 0`).

 app/styles/global.css

```
.link-hint {
  display: inline-block;
  width: 0.6em;
  height: 0.6em;
  margin-left: 0.25rem;
  border-radius: 9999px;
  background: currentColor;
  opacity: 0;
  visibility: hidden; /* reserve space without showing the hint */
}

.link-hint.is-pending {
  /* Animation 1: fade in after 100ms and keep final opacity */
  /* Animation 2: subtle pulsing while pending */
  visibility: visible;
  animation-name: fadeIn, pulse;
  animation-duration: 200ms, 1s;
  /* Appear only if navigation actually takes time */
  animation-delay: 100ms, 100ms;
  animation-timing-function: ease, ease-in-out;
  animation-iteration-count: 1, infinite;
  animation-fill-mode: forwards, none;
}

@keyframes fadeIn {
  to {
    opacity: 0.35;
  }
}
@keyframes pulse {
  50% {
    opacity: 0.15;
  }
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.3.0 | useLinkStatusintroduced. |

## Next Steps

Learn more about the features mentioned in this page by reading the API Reference.[Link ComponentEnable fast client-side navigation with the built-in `next/link` component.](https://nextjs.org/docs/app/api-reference/components/link)[loading.jsAPI reference for the loading.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/loading)

Was this helpful?

supported.

---

# useParams

> API Reference for the useParams hook.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)useParams

# useParams

Last updated  June 16, 2025

`useParams` is a **Client Component** hook that lets you read a route's [dynamic params](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) filled in by the current URL.

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

import { useParams } from 'next/navigation'

export default function ExampleClientComponent() {
  const params = useParams<{ tag: string; item: string }>()

  // Route -> /shop/[tag]/[item]
  // URL -> /shop/shoes/nike-air-max-97
  // `params` -> { tag: 'shoes', item: 'nike-air-max-97' }
  console.log(params)

  return '...'
}
```

## Parameters

```
const params = useParams()
```

`useParams` does not take any parameters.

## Returns

`useParams` returns an object containing the current route's filled in [dynamic parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes).

- Each property in the object is an active dynamic segment.
- The properties name is the segment's name, and the properties value is what the segment is filled in with.
- The properties value will either be a `string` or array of `string`'s depending on the [type of dynamic segment](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes).
- If the route contains no dynamic parameters, `useParams` returns an empty object.
- If used in Pages Router, `useParams` will return `null` on the initial render and updates with properties following the rules above once the router is ready.

For example:

| Route | URL | useParams() |
| --- | --- | --- |
| app/shop/page.js | /shop | {} |
| app/shop/[slug]/page.js | /shop/1 | { slug: '1' } |
| app/shop/[tag]/[item]/page.js | /shop/1/2 | { tag: '1', item: '2' } |
| app/shop/[...slug]/page.js | /shop/1/2 | { slug: ['1', '2'] } |

## Version History

| Version | Changes |
| --- | --- |
| v13.3.0 | useParamsintroduced. |

Was this helpful?

supported.

---

# usePathname

> API Reference for the usePathname hook.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)usePathname

# usePathname

Last updated  October 22, 2025

`usePathname` is a **Client Component** hook that lets you read the current URL's **pathname**.

> **Good to know**: When [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) is enabled `usePathname` may require a `Suspense` boundary around it if your route has a dynamic param. If you use `generateStaticParams` the `Suspense` boundary is optional

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

import { usePathname } from 'next/navigation'

export default function ExampleClientComponent() {
  const pathname = usePathname()
  return <p>Current pathname: {pathname}</p>
}
```

`usePathname` intentionally requires using a [Client Component](https://nextjs.org/docs/app/getting-started/server-and-client-components). It's important to note Client Components are not a de-optimization. They are an integral part of the [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) architecture.

For example, a Client Component with `usePathname` will be rendered into HTML on the initial page load. When navigating to a new route, this component does not need to be re-fetched. Instead, the component is downloaded once (in the client JavaScript bundle), and re-renders based on the current state.

> **Good to know**:
>
>
>
> - Reading the current URL from a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) is not supported. This design is intentional to support layout state being preserved across page navigations.
> - If your page is being statically pre-rendered and your app has [rewrites](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites) in `next.config` or a [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) file, reading the pathname with `usePathname()` can result in hydration mismatch errors—because the initial value comes from the server and may not match the actual browser pathname after routing. See our [example](#avoid-hydration-mismatch-with-rewrites) for a way to mitigate this issue.

 Compatibility with Pages Router

If you have components that use `usePathname` and they are imported into routes within the Pages Router, be aware that `usePathname` may return `null` if the router is not yet initialized. This can occur in cases such as [fallback routes](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-true) or during [Automatic Static Optimization](https://nextjs.org/docs/pages/building-your-application/rendering/static#automatic-static-optimization) in the Pages Router.

To enhance compatibility between routing systems, if your project contains both an `app` and a `pages` directory, Next.js will automatically adjust the return type of `usePathname`.

## Parameters

```
const pathname = usePathname()
```

`usePathname` does not take any parameters.

## Returns

`usePathname` returns a string of the current URL's pathname. For example:

| URL | Returned value |
| --- | --- |
| / | '/' |
| /dashboard | '/dashboard' |
| /dashboard?v=2 | '/dashboard' |
| /blog/hello-world | '/blog/hello-world' |

## Examples

### Do something in response to a route change

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

import { useEffect } from 'react'
import { usePathname, useSearchParams } from 'next/navigation'

function ExampleClientComponent() {
  const pathname = usePathname()
  const searchParams = useSearchParams()
  useEffect(() => {
    // Do something here...
  }, [pathname, searchParams])
}
```

### Avoid hydration mismatch with rewrites

When a page is pre-rendered, the HTML is generated for the source pathname. If the page is then reached through a rewrite using `next.config` or `Proxy`, the browser URL may differ, and `usePathname()` will read the rewritten pathname on the client.

To avoid hydration mismatches, design the UI so that only a small, isolated part depends on the client pathname. Render a stable fallback on the server and update that part after mount.

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

import { useEffect, useState } from 'react'
import { usePathname } from 'next/navigation'

export default function PathnameBadge() {
  const pathname = usePathname()
  const [clientPathname, setClientPathname] = useState('')

  useEffect(() => {
    setClientPathname(pathname)
  }, [pathname])

  return (
    <p>
      Current pathname: <span>{clientPathname}</span>
    </p>
  )
}
```

| Version | Changes |
| --- | --- |
| v13.0.0 | usePathnameintroduced. |

Was this helpful?

supported.
