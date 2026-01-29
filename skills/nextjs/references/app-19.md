# useReportWebVitals and more

# useReportWebVitals

> API Reference for the useReportWebVitals function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)useReportWebVitals

# useReportWebVitals

Last updated  June 16, 2025

The `useReportWebVitals` hook allows you to report [Core Web Vitals](https://web.dev/vitals/), and can be used in combination with your analytics service.

New functions passed to `useReportWebVitals` are called with the available metrics up to that point. To prevent reporting duplicated data, ensure that the callback function reference does not change (as shown in the code examples below).

   app/_components/web-vitals.js

```
'use client'

import { useReportWebVitals } from 'next/web-vitals'

const logWebVitals = (metric) => {
  console.log(metric)
}

export function WebVitals() {
  useReportWebVitals(logWebVitals)

  return null
}
```

app/layout.js

```
import { WebVitals } from './_components/web-vitals'

export default function Layout({ children }) {
  return (
    <html>
      <body>
        <WebVitals />
        {children}
      </body>
    </html>
  )
}
```

> Since the `useReportWebVitals` hook requires the `'use client'` directive, the most performant approach is to create a separate component that the root layout imports. This confines the client boundary exclusively to the `WebVitals` component.

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

   app/components/web-vitals.tsxJavaScriptTypeScript

```
'use client'

import { useReportWebVitals } from 'next/web-vitals'

type ReportWebVitalsCallback = Parameters<typeof useReportWebVitals>[0]

const handleWebVitals: ReportWebVitalsCallback = (metric) => {
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

export function WebVitals() {
  useReportWebVitals(handleWebVitals)
}
```

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

---

# useRouter

> API reference for the useRouter hook.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)useRouter

# useRouter

Last updated  October 22, 2025

The `useRouter` hook allows you to programmatically change routes inside [Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components).

> **Recommendation:** Use the [<Link>component](https://nextjs.org/docs/app/api-reference/components/link) for navigation unless you have a specific requirement for using `useRouter`.

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

import { useRouter } from 'next/navigation'

export default function Page() {
  const router = useRouter()

  return (
    <button type="button" onClick={() => router.push('/dashboard')}>
      Dashboard
    </button>
  )
}
```

## useRouter()

- `router.push(href: string, { scroll: boolean })`: Perform a client-side navigation to the provided route. Adds a new entry into the [browser's history stack](https://developer.mozilla.org/docs/Web/API/History_API).
- `router.replace(href: string, { scroll: boolean })`: Perform a client-side navigation to the provided route without adding a new entry into the browser’s history stack.
- `router.refresh()`: Refresh the current route. Making a new request to the server, re-fetching data requests, and re-rendering Server Components. The client will merge the updated React Server Component payload without losing unaffected client-side React (e.g. `useState`) or browser state (e.g. scroll position).
- `router.prefetch(href: string, options?: { onInvalidate?: () => void })`: [Prefetch](https://nextjs.org/docs/app/getting-started/linking-and-navigating#prefetching) the provided route for faster client-side transitions. The optional `onInvalidate` callback is called when the [prefetched data becomes stale](https://nextjs.org/docs/app/guides/prefetching#extending-or-ejecting-link).
- `router.back()`: Navigate back to the previous route in the browser’s history stack.
- `router.forward()`: Navigate forwards to the next page in the browser’s history stack.

> **Good to know**:
>
>
>
> - You must not send untrusted or unsanitized URLs to `router.push` or `router.replace`, as this can open your site to cross-site scripting (XSS) vulnerabilities. For example, `javascript:` URLs sent to `router.push` or `router.replace` will be executed in the context of your page.
> - The `<Link>` component automatically prefetch routes as they become visible in the viewport.
> - `refresh()` could re-produce the same result if fetch requests are cached. Other Dynamic APIs like `cookies` and `headers` could also change the response.
> - The `onInvalidate` callback is called at most once per prefetch request. It signals when you may want to trigger a new prefetch for updated route data.

### Migrating fromnext/router

- The `useRouter` hook should be imported from `next/navigation` and not `next/router` when using the App Router
- The `pathname` string has been removed and is replaced by [usePathname()](https://nextjs.org/docs/app/api-reference/functions/use-pathname)
- The `query` object has been removed and is replaced by [useSearchParams()](https://nextjs.org/docs/app/api-reference/functions/use-search-params)
- `router.events` has been replaced. [See below.](#router-events)

[View the full migration guide](https://nextjs.org/docs/app/guides/migrating/app-router-migration).

## Examples

### Router events

You can listen for page changes by composing other Client Component hooks like `usePathname` and `useSearchParams`.

 app/components/navigation-events.js

```
'use client'

import { useEffect } from 'react'
import { usePathname, useSearchParams } from 'next/navigation'

export function NavigationEvents() {
  const pathname = usePathname()
  const searchParams = useSearchParams()

  useEffect(() => {
    const url = `${pathname}?${searchParams}`
    console.log(url)
    // You can now use the current URL
    // ...
  }, [pathname, searchParams])

  return '...'
}
```

Which can be imported into a layout.

 app/layout.js

```
import { Suspense } from 'react'
import { NavigationEvents } from './components/navigation-events'

export default function Layout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}

        <Suspense fallback={null}>
          <NavigationEvents />
        </Suspense>
      </body>
    </html>
  )
}
```

> **Good to know**: `<NavigationEvents>` is wrapped in a [Suspenseboundary](https://nextjs.org/docs/app/api-reference/file-conventions/loading#examples) because[useSearchParams()](https://nextjs.org/docs/app/api-reference/functions/use-search-params) causes client-side rendering up to the closest `Suspense` boundary during [static rendering](https://nextjs.org/docs/app/guides/caching#static-rendering). [Learn more](https://nextjs.org/docs/app/api-reference/functions/use-search-params#behavior).

### Disabling scroll to top

By default, Next.js will scroll to the top of the page when navigating to a new route. You can disable this behavior by passing `scroll: false` to `router.push()` or `router.replace()`.

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

import { useRouter } from 'next/navigation'

export default function Page() {
  const router = useRouter()

  return (
    <button
      type="button"
      onClick={() => router.push('/dashboard', { scroll: false })}
    >
      Dashboard
    </button>
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.4.0 | OptionalonInvalidatecallback forrouter.prefetchintroduced |
| v13.0.0 | useRouterfromnext/navigationintroduced. |

Was this helpful?

supported.

---

# useSearchParams

> API Reference for the useSearchParams hook.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)useSearchParams

# useSearchParams

Last updated  October 22, 2025

`useSearchParams` is a **Client Component** hook that lets you read the current URL's **query string**.

`useSearchParams` returns a **read-only** version of the [URLSearchParams](https://developer.mozilla.org/docs/Web/API/URLSearchParams) interface.

 app/dashboard/search-bar.tsxJavaScriptTypeScript

```
'use client'

import { useSearchParams } from 'next/navigation'

export default function SearchBar() {
  const searchParams = useSearchParams()

  const search = searchParams.get('search')

  // URL -> `/dashboard?search=my-project`
  // `search` -> 'my-project'
  return <>Search: {search}</>
}
```

## Parameters

```
const searchParams = useSearchParams()
```

`useSearchParams` does not take any parameters.

## Returns

`useSearchParams` returns a **read-only** version of the [URLSearchParams](https://developer.mozilla.org/docs/Web/API/URLSearchParams) interface, which includes utility methods for reading the URL's query string:

- [URLSearchParams.get()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/get): Returns the first value associated with the search parameter. For example:
  | URL | searchParams.get("a") |
  | --- | --- |
  | /dashboard?a=1 | '1' |
  | /dashboard?a= | '' |
  | /dashboard?b=3 | null |
  | /dashboard?a=1&a=2 | '1'- usegetAll()to get all values |
- [URLSearchParams.has()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/has): Returns a boolean value indicating if the given parameter exists. For example:
  | URL | searchParams.has("a") |
  | --- | --- |
  | /dashboard?a=1 | true |
  | /dashboard?b=3 | false |
- Learn more about other **read-only** methods of [URLSearchParams](https://developer.mozilla.org/docs/Web/API/URLSearchParams), including the [getAll()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/getAll), [keys()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/keys), [values()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/values), [entries()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/entries), [forEach()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/forEach), and [toString()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/toString).

> **Good to know**:
>
>
>
> - `useSearchParams` is a [Client Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) hook and is **not supported** in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) to prevent stale values during [partial rendering](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions).
> - If you want to fetch data in a Server Component based on search params, it's often a better option to read the [searchParamsprop](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) of the corresponding Page. You can then pass it down by props to any component (Server or Client) within that Page.
> - If an application includes the `/pages` directory, `useSearchParams` will return `ReadonlyURLSearchParams | null`. The `null` value is for compatibility during migration since search params cannot be known during pre-rendering of a page that doesn't use `getServerSideProps`

## Behavior

### Static Rendering

If a route is [statically rendered](https://nextjs.org/docs/app/guides/caching#static-rendering), calling `useSearchParams` will cause the Client Component tree up to the closest [Suspenseboundary](https://nextjs.org/docs/app/api-reference/file-conventions/loading#examples) to be client-side rendered.

This allows a part of the route to be statically rendered while the dynamic part that uses `useSearchParams` is client-side rendered.

We recommend wrapping the Client Component that uses `useSearchParams` in a `<Suspense/>` boundary. This will allow any Client Components above it to be statically rendered and sent as part of initial HTML. [Example](https://nextjs.org/docs/app/api-reference/functions/use-search-params#static-rendering).

For example:

 app/dashboard/search-bar.tsxJavaScriptTypeScript

```
'use client'

import { useSearchParams } from 'next/navigation'

export default function SearchBar() {
  const searchParams = useSearchParams()

  const search = searchParams.get('search')

  // This will not be logged on the server when using static rendering
  console.log(search)

  return <>Search: {search}</>
}
```

   app/dashboard/page.tsxJavaScriptTypeScript

```
import { Suspense } from 'react'
import SearchBar from './search-bar'

// This component passed as a fallback to the Suspense boundary
// will be rendered in place of the search bar in the initial HTML.
// When the value is available during React hydration the fallback
// will be replaced with the `<SearchBar>` component.
function SearchBarFallback() {
  return <>placeholder</>
}

export default function Page() {
  return (
    <>
      <nav>
        <Suspense fallback={<SearchBarFallback />}>
          <SearchBar />
        </Suspense>
      </nav>
      <h1>Dashboard</h1>
    </>
  )
}
```

> **Good to know**:
>
>
>
> - In development, routes are rendered on-demand, so `useSearchParams` doesn't suspend and things may appear to work without `Suspense`.
> - During production builds, a [static page](https://nextjs.org/docs/app/guides/caching#static-rendering) that calls `useSearchParams` from a Client Component must be wrapped in a `Suspense` boundary, otherwise the build fails with the [Missing Suspense boundary with useSearchParams](https://nextjs.org/docs/messages/missing-suspense-with-csr-bailout) error.
> - If you intend the route to be dynamically rendered, prefer using the [connection](https://nextjs.org/docs/app/api-reference/functions/connection) function first in a Server Component to wait for an incoming request, this excludes everything below from prerendering. See what makes a route dynamic in the [Dynamic Rendering guide](https://nextjs.org/docs/app/guides/caching#dynamic-rendering).
> - If you're already in a Server Component Page, consider using the [searchParamsprop](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) and passing the values to Client Components.
> - You can also pass the Page [searchParamsprop](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) directly to a Client Component and unwrap it with React's `use()`. Although this will suspend, so the Client Component should be wrapped with a `Suspense` boundary.

### Dynamic Rendering

If a route is [dynamically rendered](https://nextjs.org/docs/app/guides/caching#dynamic-rendering), `useSearchParams` will be available on the server during the initial server render of the Client Component.

For example:

 app/dashboard/search-bar.tsxJavaScriptTypeScript

```
'use client'

import { useSearchParams } from 'next/navigation'

export default function SearchBar() {
  const searchParams = useSearchParams()

  const search = searchParams.get('search')

  // This will be logged on the server during the initial render
  // and on the client on subsequent navigations.
  console.log(search)

  return <>Search: {search}</>
}
```

   app/dashboard/page.tsxJavaScriptTypeScript

```
import { connection } from 'next/server'
import SearchBar from './search-bar'

export default async function Page() {
  await connection()
  return (
    <>
      <nav>
        <SearchBar />
      </nav>
      <h1>Dashboard</h1>
    </>
  )
}
```

> **Good to know**:
>
>
>
> - Previously, setting `export const dynamic = 'force-dynamic'` on the page was used to force dynamic rendering. Prefer using [connection()](https://nextjs.org/docs/app/api-reference/functions/connection) instead, as it semantically ties dynamic rendering to the incoming request.

### Server Components

#### Pages

To access search params in [Pages](https://nextjs.org/docs/app/api-reference/file-conventions/page) (Server Components), use the [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) prop.

#### Layouts

Unlike Pages, [Layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout) (Server Components) **do not** receive the `searchParams` prop. This is because a shared layout is [not re-rendered during navigation](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions) which could lead to stale `searchParams` between navigations. View [detailed explanation](https://nextjs.org/docs/app/api-reference/file-conventions/layout#query-params).

Instead, use the Page [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page) prop or the [useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params) hook in a Client Component, which is re-rendered on the client with the latest `searchParams`.

## Examples

### UpdatingsearchParams

You can use [useRouter](https://nextjs.org/docs/app/api-reference/functions/use-router) or [Link](https://nextjs.org/docs/app/api-reference/components/link) to set new `searchParams`. After a navigation is performed, the current [page.js](https://nextjs.org/docs/app/api-reference/file-conventions/page) will receive an updated [searchParamsprop](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional).

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

export default function ExampleClientComponent() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  // Get a new searchParams string by merging the current
  // searchParams with a provided key/value pair
  const createQueryString = useCallback(
    (name: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString())
      params.set(name, value)

      return params.toString()
    },
    [searchParams]
  )

  return (
    <>
      <p>Sort By</p>

      {/* using useRouter */}
      <button
        onClick={() => {
          // <pathname>?sort=asc
          router.push(pathname + '?' + createQueryString('sort', 'asc'))
        }}
      >
        ASC
      </button>

      {/* using <Link> */}
      <Link
        href={
          // <pathname>?sort=desc
          pathname + '?' + createQueryString('sort', 'desc')
        }
      >
        DESC
      </Link>
    </>
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | useSearchParamsintroduced. |

Was this helpful?

supported.

---

# useSelectedLayoutSegment

> API Reference for the useSelectedLayoutSegment hook.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)useSelectedLayoutSegment

# useSelectedLayoutSegment

Last updated  June 16, 2025

`useSelectedLayoutSegment` is a **Client Component** hook that lets you read the active route segment **one level below** the Layout it is called from.

It is useful for navigation UI, such as tabs inside a parent layout that change style depending on the active child segment.

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

import { useSelectedLayoutSegment } from 'next/navigation'

export default function ExampleClientComponent() {
  const segment = useSelectedLayoutSegment()

  return <p>Active segment: {segment}</p>
}
```

> **Good to know**:
>
>
>
> - Since `useSelectedLayoutSegment` is a [Client Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) hook, and Layouts are [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) by default, `useSelectedLayoutSegment` is usually called via a Client Component that is imported into a Layout.
> - `useSelectedLayoutSegment` only returns the segment one level down. To return all active segments, see [useSelectedLayoutSegments](https://nextjs.org/docs/app/api-reference/functions/use-selected-layout-segments)

## Parameters

```
const segment = useSelectedLayoutSegment(parallelRoutesKey?: string)
```

`useSelectedLayoutSegment` *optionally* accepts a [parallelRoutesKey](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes#with-useselectedlayoutsegments), which allows you to read the active route segment within that slot.

## Returns

`useSelectedLayoutSegment` returns a string of the active segment or `null` if one doesn't exist.

For example, given the Layouts and URLs below, the returned segment would be:

| Layout | Visited URL | Returned Segment |
| --- | --- | --- |
| app/layout.js | / | null |
| app/layout.js | /dashboard | 'dashboard' |
| app/dashboard/layout.js | /dashboard | null |
| app/dashboard/layout.js | /dashboard/settings | 'settings' |
| app/dashboard/layout.js | /dashboard/analytics | 'analytics' |
| app/dashboard/layout.js | /dashboard/analytics/monthly | 'analytics' |

## Examples

### Creating an active link component

You can use `useSelectedLayoutSegment` to create an active link component that changes style depending on the active segment. For example, a featured posts list in the sidebar of a blog:

 app/blog/blog-nav-link.tsxJavaScriptTypeScript

```
'use client'

import Link from 'next/link'
import { useSelectedLayoutSegment } from 'next/navigation'

// This *client* component will be imported into a blog layout
export default function BlogNavLink({
  slug,
  children,
}: {
  slug: string
  children: React.ReactNode
}) {
  // Navigating to `/blog/hello-world` will return 'hello-world'
  // for the selected layout segment
  const segment = useSelectedLayoutSegment()
  const isActive = slug === segment

  return (
    <Link
      href={`/blog/${slug}`}
      // Change style depending on whether the link is active
      style={{ fontWeight: isActive ? 'bold' : 'normal' }}
    >
      {children}
    </Link>
  )
}
```

   app/blog/layout.tsxJavaScriptTypeScript

```
// Import the Client Component into a parent Layout (Server Component)
import { BlogNavLink } from './blog-nav-link'
import getFeaturedPosts from './get-featured-posts'

export default async function Layout({
  children,
}: {
  children: React.ReactNode
}) {
  const featuredPosts = await getFeaturedPosts()
  return (
    <div>
      {featuredPosts.map((post) => (
        <div key={post.id}>
          <BlogNavLink slug={post.slug}>{post.title}</BlogNavLink>
        </div>
      ))}
      <div>{children}</div>
    </div>
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | useSelectedLayoutSegmentintroduced. |

Was this helpful?

supported.

---

# useSelectedLayoutSegments

> API Reference for the useSelectedLayoutSegments hook.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)useSelectedLayoutSegments

# useSelectedLayoutSegments

Last updated  June 16, 2025

`useSelectedLayoutSegments` is a **Client Component** hook that lets you read the active route segments **below** the Layout it is called from.

It is useful for creating UI in parent Layouts that need knowledge of active child segments such as breadcrumbs.

 app/example-client-component.tsxJavaScriptTypeScript

```
'use client'

import { useSelectedLayoutSegments } from 'next/navigation'

export default function ExampleClientComponent() {
  const segments = useSelectedLayoutSegments()

  return (
    <ul>
      {segments.map((segment, index) => (
        <li key={index}>{segment}</li>
      ))}
    </ul>
  )
}
```

> **Good to know**:
>
>
>
> - Since `useSelectedLayoutSegments` is a [Client Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) hook, and Layouts are [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) by default, `useSelectedLayoutSegments` is usually called via a Client Component that is imported into a Layout.
> - The returned segments include [Route Groups](https://nextjs.org/docs/app/api-reference/file-conventions/route-groups), which you might not want to be included in your UI. You can use the [filter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) array method to remove items that start with a bracket.

## Parameters

```
const segments = useSelectedLayoutSegments(parallelRoutesKey?: string)
```

`useSelectedLayoutSegments` *optionally* accepts a [parallelRoutesKey](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes#with-useselectedlayoutsegments), which allows you to read the active route segment within that slot.

## Returns

`useSelectedLayoutSegments` returns an array of strings containing the active segments one level down from the layout the hook was called from. Or an empty array if none exist.

For example, given the Layouts and URLs below, the returned segments would be:

| Layout | Visited URL | Returned Segments |
| --- | --- | --- |
| app/layout.js | / | [] |
| app/layout.js | /dashboard | ['dashboard'] |
| app/layout.js | /dashboard/settings | ['dashboard', 'settings'] |
| app/dashboard/layout.js | /dashboard | [] |
| app/dashboard/layout.js | /dashboard/settings | ['settings'] |

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | useSelectedLayoutSegmentsintroduced. |

Was this helpful?

supported.

---

# userAgent

> The userAgent helper extends the Web Request API with additional properties and methods to interact with the user agent object from the request.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)userAgent

# userAgent

Last updated  October 17, 2025

The `userAgent` helper extends the [Web Request API](https://developer.mozilla.org/docs/Web/API/Request) with additional properties and methods to interact with the user agent object from the request.

 proxy.tsJavaScriptTypeScript

```
import { NextRequest, NextResponse, userAgent } from 'next/server'

export function proxy(request: NextRequest) {
  const url = request.nextUrl
  const { device } = userAgent(request)

  // device.type can be: 'mobile', 'tablet', 'console', 'smarttv',
  // 'wearable', 'embedded', or undefined (for desktop browsers)
  const viewport = device.type || 'desktop'

  url.searchParams.set('viewport', viewport)
  return NextResponse.rewrite(url)
}
```

## isBot

A boolean indicating whether the request comes from a known bot.

## browser

An object containing information about the browser used in the request.

- `name`: A string representing the browser's name, or `undefined` if not identifiable.
- `version`: A string representing the browser's version, or `undefined`.

## device

An object containing information about the device used in the request.

- `model`: A string representing the model of the device, or `undefined`.
- `type`: A string representing the type of the device, such as `console`, `mobile`, `tablet`, `smarttv`, `wearable`, `embedded`, or `undefined`.
- `vendor`: A string representing the vendor of the device, or `undefined`.

## engine

An object containing information about the browser's engine.

- `name`: A string representing the engine's name. Possible values include: `Amaya`, `Blink`, `EdgeHTML`, `Flow`, `Gecko`, `Goanna`, `iCab`, `KHTML`, `Links`, `Lynx`, `NetFront`, `NetSurf`, `Presto`, `Tasman`, `Trident`, `w3m`, `WebKit` or `undefined`.
- `version`: A string representing the engine's version, or `undefined`.

## os

An object containing information about the operating system.

- `name`: A string representing the name of the OS, or `undefined`.
- `version`: A string representing the version of the OS, or `undefined`.

## cpu

An object containing information about the CPU architecture.

- `architecture`: A string representing the architecture of the CPU. Possible values include: `68k`, `amd64`, `arm`, `arm64`, `armhf`, `avr`, `ia32`, `ia64`, `irix`, `irix64`, `mips`, `mips64`, `pa-risc`, `ppc`, `sparc`, `sparc64` or `undefined`

Was this helpful?

supported.

---

# Functions

> API Reference for Next.js Functions and Hooks.

[App Router](https://nextjs.org/docs/app)[API Reference](https://nextjs.org/docs/app/api-reference)Functions

# Functions

Last updated  June 16, 2025[afterAPI Reference for the after function.](https://nextjs.org/docs/app/api-reference/functions/after)[cacheLifeLearn how to use the cacheLife function to set the cache expiration time for a cached function or component.](https://nextjs.org/docs/app/api-reference/functions/cacheLife)[cacheTagLearn how to use the cacheTag function to manage cache invalidation in your Next.js application.](https://nextjs.org/docs/app/api-reference/functions/cacheTag)[connectionAPI Reference for the connection function.](https://nextjs.org/docs/app/api-reference/functions/connection)[cookiesAPI Reference for the cookies function.](https://nextjs.org/docs/app/api-reference/functions/cookies)[draftModeAPI Reference for the draftMode function.](https://nextjs.org/docs/app/api-reference/functions/draft-mode)[fetchAPI reference for the extended fetch function.](https://nextjs.org/docs/app/api-reference/functions/fetch)[forbiddenAPI Reference for the forbidden function.](https://nextjs.org/docs/app/api-reference/functions/forbidden)[generateImageMetadataLearn how to generate multiple images in a single Metadata API special file.](https://nextjs.org/docs/app/api-reference/functions/generate-image-metadata)[generateMetadataLearn how to add Metadata to your Next.js application for improved search engine optimization (SEO) and web shareability.](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)[generateSitemapsLearn how to use the generateSiteMaps function to create multiple sitemaps for your application.](https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps)[generateStaticParamsAPI reference for the generateStaticParams function.](https://nextjs.org/docs/app/api-reference/functions/generate-static-params)[generateViewportAPI Reference for the generateViewport function.](https://nextjs.org/docs/app/api-reference/functions/generate-viewport)[headersAPI reference for the headers function.](https://nextjs.org/docs/app/api-reference/functions/headers)[ImageResponseAPI Reference for the ImageResponse constructor.](https://nextjs.org/docs/app/api-reference/functions/image-response)[NextRequestAPI Reference for NextRequest.](https://nextjs.org/docs/app/api-reference/functions/next-request)[NextResponseAPI Reference for NextResponse.](https://nextjs.org/docs/app/api-reference/functions/next-response)[notFoundAPI Reference for the notFound function.](https://nextjs.org/docs/app/api-reference/functions/not-found)[permanentRedirectAPI Reference for the permanentRedirect function.](https://nextjs.org/docs/app/api-reference/functions/permanentRedirect)[redirectAPI Reference for the redirect function.](https://nextjs.org/docs/app/api-reference/functions/redirect)[refreshAPI Reference for the refresh function.](https://nextjs.org/docs/app/api-reference/functions/refresh)[revalidatePathAPI Reference for the revalidatePath function.](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)[revalidateTagAPI Reference for the revalidateTag function.](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)[unauthorizedAPI Reference for the unauthorized function.](https://nextjs.org/docs/app/api-reference/functions/unauthorized)[unstable_cacheAPI Reference for the unstable_cache function.](https://nextjs.org/docs/app/api-reference/functions/unstable_cache)[unstable_noStoreAPI Reference for the unstable_noStore function.](https://nextjs.org/docs/app/api-reference/functions/unstable_noStore)[unstable_rethrowAPI Reference for the unstable_rethrow function.](https://nextjs.org/docs/app/api-reference/functions/unstable_rethrow)[updateTagAPI Reference for the updateTag function.](https://nextjs.org/docs/app/api-reference/functions/updateTag)[useLinkStatusAPI Reference for the useLinkStatus hook.](https://nextjs.org/docs/app/api-reference/functions/use-link-status)[useParamsAPI Reference for the useParams hook.](https://nextjs.org/docs/app/api-reference/functions/use-params)[usePathnameAPI Reference for the usePathname hook.](https://nextjs.org/docs/app/api-reference/functions/use-pathname)[useReportWebVitalsAPI Reference for the useReportWebVitals function.](https://nextjs.org/docs/app/api-reference/functions/use-report-web-vitals)[useRouterAPI reference for the useRouter hook.](https://nextjs.org/docs/app/api-reference/functions/use-router)[useSearchParamsAPI Reference for the useSearchParams hook.](https://nextjs.org/docs/app/api-reference/functions/use-search-params)[useSelectedLayoutSegmentAPI Reference for the useSelectedLayoutSegment hook.](https://nextjs.org/docs/app/api-reference/functions/use-selected-layout-segment)[useSelectedLayoutSegmentsAPI Reference for the useSelectedLayoutSegments hook.](https://nextjs.org/docs/app/api-reference/functions/use-selected-layout-segments)[userAgentThe userAgent helper extends the Web Request API with additional properties and methods to interact with the user agent object from the request.](https://nextjs.org/docs/app/api-reference/functions/userAgent)

Was this helpful?

supported.

---

# Turbopack

> Turbopack is an incremental bundler optimized for JavaScript and TypeScript, written in Rust, and built into Next.js.

[App Router](https://nextjs.org/docs/app)[API Reference](https://nextjs.org/docs/app/api-reference)Turbopack

# Turbopack

Last updated  January 27, 2026

Turbopack is an **incremental bundler** optimized for JavaScript and TypeScript, written in Rust, and built into **Next.js**. You can use Turbopack with both the Pages and App Router for a **much faster** local development experience.

## Why Turbopack?

We built Turbopack to push the performance of Next.js, including:

- **Unified Graph:** Next.js supports multiple output environments (e.g., client and server). Managing multiple compilers and stitching bundles together can be tedious. Turbopack uses a **single, unified graph** for all environments.
- **Bundling vs Native ESM:** Some tools skip bundling in development and rely on the browser's native ESM. This works well for small apps but can slow down large apps due to excessive network requests. Turbopack **bundles** in dev, but in an optimized way to keep large apps fast.
- **Incremental Computation:** Turbopack parallelizes work across cores and **caches** results down to the function level. Once a piece of work is done, Turbopack won’t repeat it.
- **Lazy Bundling:** Turbopack only bundles what is actually requested by the dev server. This lazy approach can reduce initial compile times and memory usage.

## Getting started

Turbopack is now the **default bundler** in Next.js. No configuration is needed to use Turbopack:

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

### Using Webpack instead

If you need to use Webpack instead of Turbopack, you can opt-in with the `--webpack` flag:

 package.json

```
{
  "scripts": {
    "dev": "next dev --webpack",
    "build": "next build --webpack",
    "start": "next start"
  }
}
```

## Supported features

Turbopack in Next.js has **zero-configuration** for the common use cases. Below is a summary of what is supported out of the box, plus some references to how you can configure Turbopack further when needed.

### Language features

| Feature | Status | Notes |
| --- | --- | --- |
| JavaScript & TypeScript | Supported | Uses SWC under the hood. Type-checking is not done by Turbopack (runtsc --watchor rely on your IDE for type checks). |
| ECMAScript (ESNext) | Supported | Turbopack supports the latest ECMAScript features, matching SWC’s coverage. |
| CommonJS | Supported | require()syntax is handled out of the box. |
| ESM | Supported | Static and dynamicimportare fully supported. |
| Babel | Supported | Starting in Next.js 16, Turbopack uses Babel automatically if it detectsa configuration file. Unlike in webpack, SWC is always used for Next.js's internal transforms and downleveling to older ECMAScript revisions. Next.js with webpack disables SWC if a Babel configuration file is present. Files innode_modulesare excluded, unless youmanually configurebabel-loader. |

### Framework and React features

| Feature | Status | Notes |
| --- | --- | --- |
| JSX / TSX | Supported | SWC handles JSX/TSX compilation. |
| Fast Refresh | Supported | No configuration needed. |
| React Server Components (RSC) | Supported | For the Next.js App Router. Turbopack ensures correct server/client bundling. |
| Root layout creation | Unsupported | Automatic creation of a root layout in App Router is not supported. Turbopack will instruct you to create it manually. |

### CSS and styling

| Feature | Status | Notes |
| --- | --- | --- |
| Global CSS | Supported | Import.cssfiles directly in your application. |
| CSS Modules | Supported | .module.cssfiles work natively (Lightning CSS). |
| CSS Nesting | Supported | Lightning CSS supportsmodern CSS nesting. |
| @import syntax | Supported | Combine multiple CSS files. |
| PostCSS | Supported | Automatically processespostcss.config.jsin a Node.js worker pool. Useful for Tailwind, Autoprefixer, etc. |
| Sass / SCSS | Supported(Next.js) | For Next.js, Sass is supported out of the box. Custom Sass functions (sassOptions.functions) are not supported because Turbopack's Rust-based architecture cannot directly execute JavaScript functions, unlike webpack's Node.js environment. Use webpack if you need this feature. In the future, Turbopack standalone usage will likely require a loader config. |
| Less | Planned via plugins | Not yet supported by default. Will likely require a loader config once custom loaders are stable. |
| Lightning CSS | In Use | Handles CSS transformations. Some low-usage CSS Modules features (like:local/:globalas standalone pseudo-classes) are not yet supported.See below for more details. |

### Assets

| Feature | Status | Notes |
| --- | --- | --- |
| Static Assets(images, fonts) | Supported | Importingimport img from './img.png'works out of the box. In Next.js, returns an object for the<Image />component. |
| JSON Imports | Supported | Named or default imports from.jsonare supported. |

### Module resolution

| Feature | Status | Notes |
| --- | --- | --- |
| Path Aliases | Supported | Readstsconfig.json'spathsandbaseUrl, matching Next.js behavior. |
| Manual Aliases | Supported | ConfigureresolveAliasinnext.config.js(similar towebpack.resolve.alias). |
| Custom Extensions | Supported | ConfigureresolveExtensionsinnext.config.js. |
| AMD | Partially Supported | Basic transforms work; advanced AMD usage is limited. |

### Performance and Fast Refresh

| Feature | Status | Notes |
| --- | --- | --- |
| Fast Refresh | Supported | Updates JavaScript, TypeScript, and CSS without a full refresh. |
| Incremental Bundling | Supported | Turbopack lazily builds only what’s requested by the dev server, speeding up large apps. |

## Known gaps with webpack

There are a number of non-trivial behavior differences between webpack and Turbopack that are important to be aware of when migrating an application. Generally, these are less of a concern for new applications.

### Filesystem Root

Turbopack uses the root directory to resolve modules. Files outside of the project root are not resolved.

For example, when linking dependencies outside the project root (via `npm link`, `yarn link`, `pnpm link`, etc.), those linked files will not be resolved by default. To resolve these files, you must configure the root option to the parent directory of both the project and the linked dependencies.

You can configure the filesystem root using [turbopack.root](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#root-directory) option in `next.config.js`.

### CSS Module Ordering

Turbopack will follow JS import order to order [CSS modules](https://nextjs.org/docs/app/getting-started/css#css-modules) which are not otherwise ordered. For example:

 components/BlogPost.jsx

```
import utilStyles from './utils.module.css'
import buttonStyles from './button.module.css'
export default function BlogPost() {
  return (
    <div className={utilStyles.container}>
      <button className={buttonStyles.primary}>Click me</button>
    </div>
  )
}
```

In this example, Turbopack will ensure that `utils.module.css` will appear before `button.module.css` in the produced CSS chunk, following the import order

Webpack generally does this as well, but there are cases where it will ignore JS inferred ordering, for example if it infers the JS file is side-effect-free.

This can lead to subtle rendering changes when adopting Turbopack, if applications have come to rely on an arbitrary ordering. Generally, the solution is easy, e.g. have `button.module.css` `@import utils.module.css` to force the ordering, or identify the conflicting rules and change them to not target the same properties.

### Sass node_modules imports

Turbopack supports importing `node_modules` Sass files out of the box. Webpack supports a legacy tilde `~` syntax for this, which is not supported by Turbopack.

From:

 styles/globals.scss

```
@import '~bootstrap/dist/css/bootstrap.min.css';
```

To:

 styles/globals.scss

```
@import 'bootstrap/dist/css/bootstrap.min.css';
```

If you can't update the imports, you can add a `turbopack.resolveAlias` configuration to map the `~` syntax to the actual path:

 next.config.js

```
module.exports = {
  turbopack: {
    resolveAlias: {
      '~*': '*',
    },
  },
}
```

### Build Caching

Webpack supports [disk build caching](https://webpack.js.org/configuration/cache/#cache) to improve build performance. Turbopack provides a similar feature, currently in beta. Starting with Next 16, you can enable Turbopack’s filesystem cache by setting the following experimental flags:

- [experimental.turbopackFileSystemCacheForDev](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache) is enabled by default
- [experimental.turbopackFileSystemCacheForBuild](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache) is currently opt-in

> **Good to know:** For this reason, when comparing webpack and Turbopack performance, make sure to delete the `.next` folder between builds to see a fair cold build comparison or enable the turbopack filesystem cache feature to compare warm builds.

### Webpack plugins

Turbopack does not support webpack plugins. This affects third-party tools that rely on webpack's plugin system for integration. We do support [webpack loaders](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#configuring-webpack-loaders). If you depend on webpack plugins, you'll need to find Turbopack-compatible alternatives or continue using webpack until equivalent functionality is available.

## Unsupported and unplanned features

Some features are not yet implemented or not planned:

- **Legacy CSS Modules features**
  - Standalone `:local` and `:global` pseudo-classes (only the function variant `:global(...)` is supported).
  - The `@value` rule (superseded by CSS variables).
  - `:import` and `:export` ICSS rules.
  - `composes` in `.module.css` composing a `.css` file. In webpack this would treat the `.css` file as a CSS Module, with Turbopack the `.css` file will always be global. This means that if you want to use `composes` in a CSS Module, you need to change the `.css` file to a `.module.css` file.
  - `@import` in CSS Modules importing `.css` as a CSS Module. In webpack this would treat the `.css` file as a CSS Module, with Turbopack the `.css` file will always be global. This means that if you want to use `@import` in a CSS Module, you need to change the `.css` file to a `.module.css` file.
- **sassOptions.functions**
  Custom Sass functions defined in `sassOptions.functions` are not supported. This feature allows defining JavaScript functions that can be called from Sass code during compilation. Turbopack's Rust-based architecture cannot directly execute JavaScript functions passed through `sassOptions.functions`, unlike webpack's Node.js-based sass-loader which runs entirely in JavaScript. If you're using custom Sass functions, you'll need to use webpack instead of Turbopack.
- **webpack()configuration** in `next.config.js`
  Turbopack replaces webpack, so `webpack()` configs are not recognized. Use the [turbopackconfig](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack) instead.
- **Yarn PnP**
  Not planned for Turbopack support in Next.js.
- **experimental.urlImports**
  Not planned for Turbopack.
- **experimental.esmExternals**
  Not planned. Turbopack does not support the legacy `esmExternals` configuration in Next.js.
- **Some Next.js Experimental Flags**
  - `experimental.nextScriptWorkers`
  - `experimental.sri.algorithm`
  - `experimental.fallbackNodePolyfills`
    We plan to implement these in the future.

For a full, detailed breakdown of each feature flag and its status, see the [Turbopack API Reference](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack).

## Configuration

Turbopack can be configured via `next.config.js` (or `next.config.ts`) under the `turbopack` key. Configuration options include:

- **rules**
  Define additional [webpack loaders](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#configuring-webpack-loaders) for file transformations.
- **resolveAlias**
  Create manual aliases (like `resolve.alias` in webpack).
- **resolveExtensions**
  Change or extend file extensions for module resolution.

 next.config.js

```
module.exports = {
  turbopack: {
    // Example: adding an alias and custom file extension
    resolveAlias: {
      underscore: 'lodash',
    },
    resolveExtensions: ['.mdx', '.tsx', '.ts', '.jsx', '.js', '.json'],
  },
}
```

For more in-depth configuration examples, see the [Turbopack config documentation](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack).

## Generating trace files for performance debugging

If you encounter performance or memory issues and want to help the Next.js team diagnose them, you can generate a trace file by appending `NEXT_TURBOPACK_TRACING=1` to your dev command:

```
NEXT_TURBOPACK_TRACING=1 next dev
```

This will produce a `.next/dev/trace-turbopack` file. Include that file when creating a GitHub issue on the [Next.js repo](https://github.com/vercel/next.js) to help us investigate.

By default the development server outputs to `.next/dev`. Read more about [isolatedDevBuild](https://nextjs.org/docs/app/api-reference/config/next-config-js/isolatedDevBuild).

## Summary

Turbopack is a **Rust-based**, **incremental** bundler designed to make local development and builds fast—especially for large applications. It is integrated into Next.js, offering zero-config CSS, React, and TypeScript support.

## Version Changes

| Version | Changes |
| --- | --- |
| v16.0.0 | Turbopack becomes the default bundler for Next.js. Automatic support for Babel when a configuration file is found. |
| v15.5.0 | Turbopack support forbuildbeta |
| v15.3.0 | Experimental support forbuild |
| v15.0.0 | Turbopack fordevstable |

Was this helpful?

supported.

---

# API Reference

> Next.js API Reference for the App Router.

[Next.js Docs](https://nextjs.org/docs)[App Router](https://nextjs.org/docs/app)API Reference

# API Reference

Last updated  June 16, 2025[DirectivesDirectives are used to modify the behavior of your Next.js application.](https://nextjs.org/docs/app/api-reference/directives)[ComponentsAPI Reference for Next.js built-in components.](https://nextjs.org/docs/app/api-reference/components)[File-system conventionsAPI Reference for Next.js file-system conventions.](https://nextjs.org/docs/app/api-reference/file-conventions)[FunctionsAPI Reference for Next.js Functions and Hooks.](https://nextjs.org/docs/app/api-reference/functions)[ConfigurationLearn how to configure Next.js applications.](https://nextjs.org/docs/app/api-reference/config)[CLIAPI Reference for the Next.js Command Line Interface (CLI) tools.](https://nextjs.org/docs/app/api-reference/cli)[Edge RuntimeAPI Reference for the Edge Runtime.](https://nextjs.org/docs/app/api-reference/edge)[TurbopackTurbopack is an incremental bundler optimized for JavaScript and TypeScript, written in Rust, and built into Next.js.](https://nextjs.org/docs/app/api-reference/turbopack)

Was this helpful?

supported.
