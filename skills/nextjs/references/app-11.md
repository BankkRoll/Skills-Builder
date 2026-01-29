# Dynamic Route Segments and more

# Dynamic Route Segments

> Dynamic Route Segments can be used to programmatically generate route segments from dynamic data.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)Dynamic Segments

# Dynamic Route Segments

Last updated  December 20, 2025

When you don't know the exact route segment names ahead of time and want to create routes from dynamic data, you can use Dynamic Segments that are filled in at request time or prerendered at build time.

## Convention

A Dynamic Segment can be created by wrapping a folder's name in square brackets: `[folderName]`. For example, a blog could include the following route `app/blog/[slug]/page.js` where `[slug]` is the Dynamic Segment for blog posts.

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <div>My Post: {slug}</div>
}
```

Dynamic Segments are passed as the `params` prop to [layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout), [page](https://nextjs.org/docs/app/api-reference/file-conventions/page), [route](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#generatemetadata-function) functions.

| Route | Example URL | params |
| --- | --- | --- |
| app/blog/[slug]/page.js | /blog/a | { slug: 'a' } |
| app/blog/[slug]/page.js | /blog/b | { slug: 'b' } |
| app/blog/[slug]/page.js | /blog/c | { slug: 'c' } |

### In Client Components

In a Client Component **page**, dynamic segments from props can be accessed using the [use](https://react.dev/reference/react/use) hook.

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
'use client'
import { use } from 'react'

export default function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = use(params)

  return (
    <div>
      <p>{slug}</p>
    </div>
  )
}
```

Alternatively Client Components can use the [useParams](https://nextjs.org/docs/app/api-reference/functions/use-params) hook to access the `params` anywhere in the Client Component tree.

### Catch-all Segments

Dynamic Segments can be extended to **catch-all** subsequent segments by adding an ellipsis inside the brackets `[...folderName]`.

For example, `app/shop/[...slug]/page.js` will match `/shop/clothes`, but also `/shop/clothes/tops`, `/shop/clothes/tops/t-shirts`, and so on.

| Route | Example URL | params |
| --- | --- | --- |
| app/shop/[...slug]/page.js | /shop/a | { slug: ['a'] } |
| app/shop/[...slug]/page.js | /shop/a/b | { slug: ['a', 'b'] } |
| app/shop/[...slug]/page.js | /shop/a/b/c | { slug: ['a', 'b', 'c'] } |

### Optional Catch-all Segments

Catch-all Segments can be made **optional** by including the parameter in double square brackets: `[[...folderName]]`.

For example, `app/shop/[[...slug]]/page.js` will **also** match `/shop`, in addition to `/shop/clothes`, `/shop/clothes/tops`, `/shop/clothes/tops/t-shirts`.

The difference between **catch-all** and **optional catch-all** segments is that with optional, the route without the parameter is also matched (`/shop` in the example above).

| Route | Example URL | params |
| --- | --- | --- |
| app/shop/[[...slug]]/page.js | /shop | { slug: undefined } |
| app/shop/[[...slug]]/page.js | /shop/a | { slug: ['a'] } |
| app/shop/[[...slug]]/page.js | /shop/a/b | { slug: ['a', 'b'] } |
| app/shop/[[...slug]]/page.js | /shop/a/b/c | { slug: ['a', 'b', 'c'] } |

### TypeScript

When using TypeScript, you can add types for `params` depending on your configured route segment — use [PageProps<'/route'>](https://nextjs.org/docs/app/api-reference/file-conventions/page#page-props-helper), [LayoutProps<'/route'>](https://nextjs.org/docs/app/api-reference/file-conventions/layout#layout-props-helper), or [RouteContext<'/route'>](https://nextjs.org/docs/app/api-reference/file-conventions/route#route-context-helper) to type `params` in `page`, `layout`, and `route` respectively.

Route `params` values are typed as `string`, `string[]`, or `undefined` (for optional catch-all segments), because their values aren't known until runtime. Users can enter any URL into the address bar, and these broad types help ensure that your application code handles all these possible cases.

| Route | paramsType Definition |
| --- | --- |
| app/blog/[slug]/page.js | { slug: string } |
| app/shop/[...slug]/page.js | { slug: string[] } |
| app/shop/[[...slug]]/page.js | { slug?: string[] } |
| app/[categoryId]/[itemId]/page.js | { categoryId: string, itemId: string } |

If you're working on a route where `params` can only have a fixed number of valid values, such as a `[locale]` param with a known set of language codes, you can use runtime validation to handle any invalid params a user may enter, and let the rest of your application work with the narrower type from your known set.

 /app/[locale]/page.tsx

```
import { notFound } from 'next/navigation'
import type { Locale } from '@i18n/types'
import { isValidLocale } from '@i18n/utils'

function assertValidLocale(value: string): asserts value is Locale {
  if (!isValidLocale(value)) notFound()
}

export default async function Page(props: PageProps<'/[locale]'>) {
  const { locale } = await props.params // locale is typed as string
  assertValidLocale(locale)
  // locale is now typed as Locale
}
```

## Behavior

- Since the `params` prop is a promise. You must use `async`/`await` or React's use function to access the values.
  - In version 14 and earlier, `params` was a synchronous prop. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future.

### With Cache Components

When using [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) with dynamic route segments, how you handle params depends on whether you use [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params).

Without `generateStaticParams`, param values are unknown during prerendering, making params runtime data. You must wrap param access in `<Suspense>` boundaries to provide fallback UI.

With `generateStaticParams`, you provide sample param values that can be used at build time. The build process validates that dynamic content and other runtime APIs are correctly handled, then generates static HTML files for the samples. Pages rendered with runtime params are saved to disk after a successful first request.

The sections below demonstrate both patterns.

#### WithoutgenerateStaticParams

All params are runtime data. Param access must be wrapped by Suspense fallback UI. Next.js generates a static shell at build time, and content loads on each request.

> **Good to know**: You can also use [loading.tsx](https://nextjs.org/docs/app/api-reference/file-conventions/loading) for page-level fallback UI.

 app/blog/[slug]/page.tsx

```
import { Suspense } from 'react'

export default function Page({ params }: PageProps<'/blog/[slug]'>) {
  return (
    <div>
      <h1>Blog Post</h1>
      <Suspense fallback={<div>Loading...</div>}>
        {params.then(({ slug }) => (
          <Content slug={slug} />
        ))}
      </Suspense>
    </div>
  )
}

async function Content({ slug }: { slug: string }) {
  const res = await fetch(`https://api.vercel.app/blog/${slug}`)
  const post = await res.json()

  return (
    <article>
      <h2>{post.title}</h2>
      <p>{post.content}</p>
    </article>
  )
}
```

#### WithgenerateStaticParams

Provide params ahead of time to prerender pages at build time. You can prerender all routes or a subset depending on your needs.

During the build process, the route is executed with each sample param to collect the HTML result. If dynamic content or runtime data are accessed incorrectly, the build will fail.

 app/blog/[slug]/page.tsx

```
import { Suspense } from 'react'

export async function generateStaticParams() {
  return [{ slug: '1' }, { slug: '2' }, { slug: '3' }]
}

export default async function Page({ params }: PageProps<'/blog/[slug]'>) {
  const { slug } = await params

  return (
    <div>
      <h1>Blog Post</h1>
      <Content slug={slug} />
    </div>
  )
}

async function Content({ slug }: { slug: string }) {
  const post = await getPost(slug)
  return (
    <article>
      <h2>{post.title}</h2>
      <p>{post.content}</p>
    </article>
  )
}

async function getPost(slug: string) {
  'use cache'
  const res = await fetch(`https://api.vercel.app/blog/${slug}`)
  return res.json()
}
```

Build-time validation only covers code paths that execute with the sample params. If your route has conditional logic that accesses runtime APIs for certain param values not in your samples, those branches won't be validated at build time:

 app/blog/[slug]/page.tsx

```
import { cookies } from 'next/headers'

export async function generateStaticParams() {
  return [{ slug: 'public-post' }, { slug: 'hello-world' }]
}

export default async function Page({ params }: PageProps<'/blog/[slug]'>) {
  const { slug } = await params

  if (slug.startsWith('private-')) {
    // This branch is never executed at build time
    // Runtime requests for 'private-*' slugs will error
    return <PrivatePost slug={slug} />
  }

  return <PublicPost slug={slug} />
}

async function PrivatePost({ slug }: { slug: string }) {
  const token = (await cookies()).get('token')
  // ... fetch and render private post using token for auth
}
```

For runtime params not returned by `generateStaticParams`, validation occurs during the first request. In the example above, requests for slugs starting with `private-` will fail because `PrivatePost` accesses `cookies()` without a Suspense boundary. Other runtime params that don't hit the conditional branch will render successfully and be saved to disk for subsequent requests.

To fix this, wrap `PrivatePost` with Suspense:

 app/blog/[slug]/page.tsx

```
import { Suspense } from 'react'
import { cookies } from 'next/headers'

export async function generateStaticParams() {
  return [{ slug: 'public-post' }, { slug: 'hello-world' }]
}

export default async function Page({ params }: PageProps<'/blog/[slug]'>) {
  const { slug } = await params

  if (slug.startsWith('private-')) {
    return (
      <Suspense fallback={<div>Loading...</div>}>
        <PrivatePost slug={slug} />
      </Suspense>
    )
  }

  return <PublicPost slug={slug} />
}

async function PrivatePost({ slug }: { slug: string }) {
  const token = (await cookies()).get('token')
  // ... fetch and render private post using token for auth
}
```

## Examples

### WithgenerateStaticParams

The [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params) function can be used to [statically generate](https://nextjs.org/docs/app/guides/caching#static-rendering) routes at build time instead of on-demand at request time.

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())

  return posts.map((post) => ({
    slug: post.slug,
  }))
}
```

When using `fetch` inside the `generateStaticParams` function, the requests are [automatically deduplicated](https://nextjs.org/docs/app/guides/caching#request-memoization). This avoids multiple network calls for the same data Layouts, Pages, and other `generateStaticParams` functions, speeding up build time.

### Dynamic GET Route Handlers withgenerateStaticParams

`generateStaticParams` also works with dynamic [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) to statically generate API responses at build time:

 app/api/posts/[id]/route.tsJavaScriptTypeScript

```
export async function generateStaticParams() {
  const posts: { id: number }[] = await fetch(
    'https://api.vercel.app/blog'
  ).then((res) => res.json())

  return posts.map((post) => ({
    id: `${post.id}`,
  }))
}

export async function GET(
  request: Request,
  { params }: RouteContext<'/api/posts/[id]'>
) {
  const { id } = await params
  const res = await fetch(`https://api.vercel.app/blog/${id}`)

  if (!res.ok) {
    return Response.json({ error: 'Post not found' }, { status: 404 })
  }

  const post = await res.json()
  return Response.json(post)
}
```

In this example, route handlers for all blog post IDs returned by `generateStaticParams` will be statically generated at build time. Requests to other IDs will be handled dynamically at request time.

## Next Steps

For more information on what to do next, we recommend the following sections[generateStaticParamsAPI reference for the generateStaticParams function.](https://nextjs.org/docs/app/api-reference/functions/generate-static-params)

Was this helpful?

supported.

---

# error.js

> API reference for the error.js special file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)error.js

# error.js

Last updated  September 22, 2025

An **error** file allows you to handle unexpected runtime errors and display fallback UI.

 ![error.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ferror-special-file.png&w=3840&q=75)![error.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ferror-special-file.png&w=3840&q=75) app/dashboard/error.tsxJavaScriptTypeScript

```
'use client' // Error boundaries must be Client Components

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button
        onClick={
          // Attempt to recover by trying to re-render the segment
          () => reset()
        }
      >
        Try again
      </button>
    </div>
  )
}
```

`error.js` wraps a route segment and its nested children in a [React Error Boundary](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary). When an error throws within the boundary, the `error` component shows as the fallback UI.

 ![How error.js works](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ferror-overview.png&w=3840&q=75)![How error.js works](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ferror-overview.png&w=3840&q=75)

> **Good to know**:
>
>
>
> - The [React DevTools](https://react.dev/learn/react-developer-tools) allow you to toggle error boundaries to test error states.
> - If you want errors to bubble up to the parent error boundary, you can `throw` when rendering the `error` component.

## Reference

### Props

#### error

An instance of an [Error](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Error) object forwarded to the `error.js` Client Component.

> **Good to know:** During development, the `Error` object forwarded to the client will be serialized and include the `message` of the original error for easier debugging. However, **this behavior is different in production** to avoid leaking potentially sensitive details included in the error to the client.

#### error.message

- Errors forwarded from Client Components show the original `Error` message.
- Errors forwarded from Server Components show a generic message with an identifier. This is to prevent leaking sensitive details. You can use the identifier, under `errors.digest`, to match the corresponding server-side logs.

#### error.digest

An automatically generated hash of the error thrown. It can be used to match the corresponding error in server-side logs.

#### reset

The cause of an error can sometimes be temporary. In these cases, trying again might resolve the issue.

An error component can use the `reset()` function to prompt the user to attempt to recover from the error. When executed, the function will try to re-render the error boundary's contents. If successful, the fallback error component is replaced with the result of the re-render.

 app/dashboard/error.tsxJavaScriptTypeScript

```
'use client' // Error boundaries must be Client Components

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

## Examples

### Global Error

While less common, you can handle errors in the root layout or template using `global-error.jsx`, located in the root app directory, even when leveraging [internationalization](https://nextjs.org/docs/app/guides/internationalization). Global error UI must define its own `<html>` and `<body>` tags, global styles, fonts, or other dependencies that your error page requires. This file replaces the root layout or template when active.

> **Good to know**: Error boundaries must be [Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components#using-client-components), which means that [metadataandgenerateMetadata](https://nextjs.org/docs/app/getting-started/metadata-and-og-images) exports are not supported in `global-error.jsx`. As an alternative, you can use the React [<title>](https://react.dev/reference/react-dom/components/title) component.

 app/global-error.tsxJavaScriptTypeScript

```
'use client' // Error boundaries must be Client Components

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    // global-error must include html and body tags
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  )
}
```

### Graceful error recovery with a custom error boundary

When rendering fails on the client, it can be useful to show the last known server rendered UI for a better user experience.

The `GracefullyDegradingErrorBoundary` is an example of a custom error boundary that captures and preserves the current HTML before an error occurs. If a rendering error happens, it re-renders the captured HTML and displays a persistent notification bar to inform the user.

 app/dashboard/error.tsxJavaScriptTypeScript

```
'use client'

import React, { Component, ErrorInfo, ReactNode } from 'react'

interface ErrorBoundaryProps {
  children: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}

interface ErrorBoundaryState {
  hasError: boolean
}

export class GracefullyDegradingErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  private contentRef: React.RefObject<HTMLDivElement | null>

  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
    this.contentRef = React.createRef()
  }

  static getDerivedStateFromError(_: Error): ErrorBoundaryState {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    if (this.props.onError) {
      this.props.onError(error, errorInfo)
    }
  }

  render() {
    if (this.state.hasError) {
      // Render the current HTML content without hydration
      return (
        <>
          <div
            ref={this.contentRef}
            suppressHydrationWarning
            dangerouslySetInnerHTML={{
              __html: this.contentRef.current?.innerHTML || '',
            }}
          />
          <div className="fixed bottom-0 left-0 right-0 bg-red-600 text-white py-4 px-6 text-center">
            <p className="font-semibold">
              An error occurred during page rendering
            </p>
          </div>
        </>
      )
    }

    return <div ref={this.contentRef}>{this.props.children}</div>
  }
}

export default GracefullyDegradingErrorBoundary
```

## Version History

| Version | Changes |
| --- | --- |
| v15.2.0 | Also displayglobal-errorin development. |
| v13.1.0 | global-errorintroduced. |
| v13.0.0 | errorintroduced. |

## Learn more about error handling

[Error HandlingLearn how to display expected errors and handle uncaught exceptions.](https://nextjs.org/docs/app/getting-started/error-handling)

Was this helpful?

supported.

---

# forbidden.js

> API reference for the forbidden.js special file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)forbidden.js

# forbidden.js

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

The **forbidden** file is used to render UI when the [forbidden](https://nextjs.org/docs/app/api-reference/functions/forbidden) function is invoked during authentication. Along with allowing you to customize the UI, Next.js will return a `403` status code.

 app/forbidden.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Forbidden() {
  return (
    <div>
      <h2>Forbidden</h2>
      <p>You are not authorized to access this resource.</p>
      <Link href="/">Return Home</Link>
    </div>
  )
}
```

## Reference

### Props

`forbidden.js` components do not accept any props.

## Version History

| Version | Changes |
| --- | --- |
| v15.1.0 | forbidden.jsintroduced. |

[forbiddenAPI Reference for the forbidden function.](https://nextjs.org/docs/app/api-reference/functions/forbidden)

Was this helpful?

supported.

---

# instrumentation

> Learn how to add client-side instrumentation to track and monitor your Next.js application's frontend performance.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)instrumentation-client.js

# instrumentation-client.js

Last updated  August 6, 2025

The `instrumentation-client.js|ts` file allows you to add monitoring, analytics code, and other side-effects that run before your application becomes interactive. This is useful for setting up performance tracking, error monitoring, polyfills, or any other client-side observability tools.

To use it, place the file in the **root** of your application or inside a `src` folder.

## Usage

Unlike [server-side instrumentation](https://nextjs.org/docs/app/guides/instrumentation), you do not need to export any specific functions. You can write your monitoring code directly in the file:

 instrumentation-client.tsJavaScriptTypeScript

```
// Set up performance monitoring
performance.mark('app-init')

// Initialize analytics
console.log('Analytics initialized')

// Set up error tracking
window.addEventListener('error', (event) => {
  // Send to your error tracking service
  reportError(event.error)
})
```

**Error handling:** Implement try-catch blocks around your instrumentation code to ensure robust monitoring. This prevents individual tracking failures from affecting other instrumentation features.

## Router navigation tracking

You can export an `onRouterTransitionStart` function to receive notifications when navigation begins:

 instrumentation-client.tsJavaScriptTypeScript

```
performance.mark('app-init')

export function onRouterTransitionStart(
  url: string,
  navigationType: 'push' | 'replace' | 'traverse'
) {
  console.log(`Navigation started: ${navigationType} to ${url}`)
  performance.mark(`nav-start-${Date.now()}`)
}
```

The `onRouterTransitionStart` function receives two parameters:

- `url: string` - The URL being navigated to
- `navigationType: 'push' | 'replace' | 'traverse'` - The type of navigation

## Performance considerations

Keep instrumentation code lightweight.

Next.js monitors initialization time in development and will log warnings if it takes longer than 16ms, which could impact smooth page loading.

## Execution timing

The `instrumentation-client.js` file executes at a specific point in the application lifecycle:

1. **After** the HTML document is loaded
2. **Before** React hydration begins
3. **Before** user interactions are possible

This timing makes it ideal for setting up error tracking, analytics, and performance monitoring that needs to capture early application lifecycle events.

## Examples

### Error tracking

Initialize error tracking before React starts and add navigation breadcrumbs for better debugging context.

 instrumentation-client.tsJavaScriptTypeScript

```
import Monitor from './lib/monitoring'

Monitor.initialize()

export function onRouterTransitionStart(url: string) {
  Monitor.pushEvent({
    message: `Navigation to ${url}`,
    category: 'navigation',
  })
}
```

### Analytics tracking

Initialize analytics and track navigation events with detailed metadata for user behavior analysis.

 instrumentation-client.tsJavaScriptTypeScript

```
import { analytics } from './lib/analytics'

analytics.init()

export function onRouterTransitionStart(url: string, navigationType: string) {
  analytics.track('page_navigation', {
    url,
    type: navigationType,
    timestamp: Date.now(),
  })
}
```

### Performance monitoring

Track Time to Interactive and navigation performance using the Performance Observer API and performance marks.

 instrumentation-client.tsJavaScriptTypeScript

```
const startTime = performance.now()

const observer = new PerformanceObserver(
  (list: PerformanceObserverEntryList) => {
    for (const entry of list.getEntries()) {
      if (entry instanceof PerformanceNavigationTiming) {
        console.log('Time to Interactive:', entry.loadEventEnd - startTime)
      }
    }
  }
)

observer.observe({ entryTypes: ['navigation'] })

export function onRouterTransitionStart(url: string) {
  performance.mark(`nav-start-${url}`)
}
```

### Polyfills

Load polyfills before application code runs. Use static imports for immediate loading and dynamic imports for conditional loading based on feature detection.

 instrumentation-client.tsJavaScriptTypeScript

```
import './lib/polyfills'

if (!window.ResizeObserver) {
  import('./lib/polyfills/resize-observer').then((mod) => {
    window.ResizeObserver = mod.default
  })
}
```

## Version history

| Version | Changes |
| --- | --- |
| v15.3 | instrumentation-clientintroduced |

Was this helpful?

supported.

---

# instrumentation.js

> API reference for the instrumentation.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)instrumentation.js

# instrumentation.js

Last updated  October 17, 2025

The `instrumentation.js|ts` file is used to integrate observability tools into your application, allowing you to track the performance and behavior, and to debug issues in production.

To use it, place the file in the **root** of your application or inside a [srcfolder](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder) if using one.

## Exports

### register(optional)

The file exports a `register` function that is called **once** when a new Next.js server instance is initiated. `register` can be an async function.

 instrumentation.tsJavaScriptTypeScript

```
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel('next-app')
}
```

### onRequestError(optional)

You can optionally export an `onRequestError` function to track **server** errors to any custom observability provider.

- If you're running any async tasks in `onRequestError`, make sure they're awaited. `onRequestError` will be triggered when the Next.js server captures the error.
- The `error` instance might not be the original error instance thrown, as it may be processed by React if encountered during Server Components rendering. If this happens, you can use `digest` property on an error to identify the actual error type.

 instrumentation.tsJavaScriptTypeScript

```
import { type Instrumentation } from 'next'

export const onRequestError: Instrumentation.onRequestError = async (
  err,
  request,
  context
) => {
  await fetch('https://.../report-error', {
    method: 'POST',
    body: JSON.stringify({
      message: err.message,
      request,
      context,
    }),
    headers: {
      'Content-Type': 'application/json',
    },
  })
}
```

#### Parameters

The function accepts three parameters: `error`, `request`, and `context`.

 Types

```
export function onRequestError(
  error: { digest: string } & Error,
  request: {
    path: string // resource path, e.g. /blog?name=foo
    method: string // request method. e.g. GET, POST, etc
    headers: { [key: string]: string | string[] }
  },
  context: {
    routerKind: 'Pages Router' | 'App Router' // the router type
    routePath: string // the route file path, e.g. /app/blog/[dynamic]
    routeType: 'render' | 'route' | 'action' | 'proxy' // the context in which the error occurred
    renderSource:
      | 'react-server-components'
      | 'react-server-components-payload'
      | 'server-rendering'
    revalidateReason: 'on-demand' | 'stale' | undefined // undefined is a normal request without revalidation
    renderType: 'dynamic' | 'dynamic-resume' // 'dynamic-resume' for PPR
  }
): void | Promise<void>
```

- `error`: The caught error itself (type is always `Error`), and a `digest` property which is the unique ID of the error.
- `request`: Read-only request information associated with the error.
- `context`: The context in which the error occurred. This can be the type of router (App or Pages Router), and/or (Server Components (`'render'`), Route Handlers (`'route'`), Server Actions (`'action'`), or Proxy (`'proxy'`)).

### Specifying the runtime

The `instrumentation.js` file works in both the Node.js and Edge runtime, however, you can use `process.env.NEXT_RUNTIME` to target a specific runtime.

 instrumentation.js

```
export function register() {
  if (process.env.NEXT_RUNTIME === 'edge') {
    return require('./register.edge')
  } else {
    return require('./register.node')
  }
}

export function onRequestError() {
  if (process.env.NEXT_RUNTIME === 'edge') {
    return require('./on-request-error.edge')
  } else {
    return require('./on-request-error.node')
  }
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0 | onRequestErrorintroduced,instrumentationstable |
| v14.0.4 | Turbopack support forinstrumentation |
| v13.2.0 | instrumentationintroduced as an experimental feature |

## Learn more about Instrumentation

[InstrumentationLearn how to use instrumentation to run code at server startup in your Next.js app](https://nextjs.org/docs/app/guides/instrumentation)

Was this helpful?

supported.

---

# Intercepting Routes

> Use intercepting routes to load a new route within the current layout while masking the browser URL, useful for advanced routing patterns such as modals.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)Intercepting Routes

# Intercepting Routes

Last updated  June 16, 2025

Intercepting routes allows you to load a route from another part of your application within the current layout. This routing paradigm can be useful when you want to display the content of a route without the user switching to a different context.

For example, when clicking on a photo in a feed, you can display the photo in a modal, overlaying the feed. In this case, Next.js intercepts the `/photo/123` route, masks the URL, and overlays it over `/feed`.

 ![Intercepting routes soft navigation](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fintercepting-routes-soft-navigate.png&w=3840&q=75)![Intercepting routes soft navigation](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fintercepting-routes-soft-navigate.png&w=3840&q=75)

However, when navigating to the photo by clicking a shareable URL or by refreshing the page, the entire photo page should render instead of the modal. No route interception should occur.

 ![Intercepting routes hard navigation](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fintercepting-routes-hard-navigate.png&w=3840&q=75)![Intercepting routes hard navigation](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fintercepting-routes-hard-navigate.png&w=3840&q=75)

## Convention

Intercepting routes can be defined with the `(..)` convention, which is similar to relative path convention `../` but for route segments.

You can use:

- `(.)` to match segments on the **same level**
- `(..)` to match segments **one level above**
- `(..)(..)` to match segments **two levels above**
- `(...)` to match segments from the **root** `app` directory

For example, you can intercept the `photo` segment from within the `feed` segment by creating a `(..)photo` directory.

 ![Intercepting routes folder structure](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fintercepted-routes-files.png&w=3840&q=75)![Intercepting routes folder structure](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fintercepted-routes-files.png&w=3840&q=75)

> **Good to know:** The `(..)` convention is based on *route segments*, not the file-system. For example, it does not consider `@slot` folders in [Parallel Routes](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes).

## Examples

### Modals

Intercepting Routes can be used together with [Parallel Routes](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes) to create modals. This allows you to solve common challenges when building modals, such as:

- Making the modal content **shareable through a URL**.
- **Preserving context** when the page is refreshed, instead of closing the modal.
- **Closing the modal on backwards navigation** rather than going to the previous route.
- **Reopening the modal on forwards navigation**.

Consider the following UI pattern, where a user can open a photo modal from a gallery using client-side navigation, or navigate to the photo page directly from a shareable URL:

 ![Intercepting routes modal example](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fintercepted-routes-modal-example.png&w=3840&q=75)![Intercepting routes modal example](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fintercepted-routes-modal-example.png&w=3840&q=75)

In the above example, the path to the `photo` segment can use the `(..)` matcher since `@modal` is a slot and **not** a segment. This means that the `photo` route is only one segment level higher, despite being two file-system levels higher.

See the [Parallel Routes](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes#modals) documentation for a step-by-step example, or see our [image gallery example](https://github.com/vercel-labs/nextgram).

> **Good to know:**
>
>
>
> - Other examples could include opening a login modal in a top navbar while also having a dedicated `/login` page, or opening a shopping cart in a side modal.

## Next Steps

Learn how to create modals with Intercepted and Parallel Routes.[Parallel RoutesSimultaneously render one or more pages in the same view that can be navigated independently. A pattern for highly dynamic applications.](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes)

Was this helpful?

supported.

---

# layout.js

> API reference for the layout.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)layout.js

# layout.js

Last updated  December 19, 2025

The `layout` file is used to define a layout in your Next.js application.

 app/dashboard/layout.tsxJavaScriptTypeScript

```
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <section>{children}</section>
}
```

A **root layout** is the top-most layout in the root `app` directory. It is used to define the `<html>` and `<body>` tags and other globally shared UI.

 app/layout.tsxJavaScriptTypeScript

```
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

## Reference

### Props

#### children(required)

Layout components should accept and use a `children` prop. During rendering, `children` will be populated with the route segments the layout is wrapping. These will primarily be the component of a child [Layout](https://nextjs.org/docs/app/api-reference/file-conventions/page) (if it exists) or [Page](https://nextjs.org/docs/app/api-reference/file-conventions/page), but could also be other special files like [Loading](https://nextjs.org/docs/app/api-reference/file-conventions/loading) or [Error](https://nextjs.org/docs/app/getting-started/error-handling) when applicable.

#### params(optional)

A promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) object from the root segment down to that layout.

 app/dashboard/[team]/layout.tsxJavaScriptTypeScript

```
export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ team: string }>
}) {
  const { team } = await params
}
```

| Example Route | URL | params |
| --- | --- | --- |
| app/dashboard/[team]/layout.js | /dashboard/1 | Promise<{ team: '1' }> |
| app/shop/[tag]/[item]/layout.js | /shop/1/2 | Promise<{ tag: '1', item: '2' }> |
| app/blog/[...slug]/layout.js | /blog/1/2 | Promise<{ slug: ['1', '2'] }> |

- Since the `params` prop is a promise. You must use `async/await` or React's [use](https://react.dev/reference/react/use) function to access the values.
  - In version 14 and earlier, `params` was a synchronous prop. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future.

### Layout Props Helper

You can type layouts with `LayoutProps` to get a strongly typed `params` and named slots inferred from your directory structure. `LayoutProps` is a globally available helper.

 app/dashboard/layout.tsx

```
export default function Layout(props: LayoutProps<'/dashboard'>) {
  return (
    <section>
      {props.children}
      {/* If you have app/dashboard/@analytics, it appears as a typed slot: */}
      {/* {props.analytics} */}
    </section>
  )
}
```

> **Good to know**:
>
>
>
> - Types are generated during `next dev`, `next build` or `next typegen`.
> - After type generation, the `LayoutProps` helper is globally available. It doesn't need to be imported.

### Root Layout

The `app` directory **must** include a **root layout**, which is the top-most layout in the root `app` directory. Typically, the root layout is `app/layout.js`.

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html>
      <body>{children}</body>
    </html>
  )
}
```

- The root layout **must** define `<html>` and `<body>` tags.
  - You should **not** manually add `<head>` tags such as `<title>` and `<meta>` to root layouts. Instead, you should use the [Metadata API](https://nextjs.org/docs/app/getting-started/metadata-and-og-images) which automatically handles advanced requirements such as streaming and de-duplicating `<head>` elements.
- You can create **multiple root layouts**. Any layout without a `layout.js` above it is a root layout. Two common approaches:
  - Using [route groups](https://nextjs.org/docs/app/api-reference/file-conventions/route-groups) like `app/(shop)/layout.js` and `app/(marketing)/layout.js`
  - Omitting `app/layout.js` so layouts in subdirectories like `app/dashboard/layout.js` and `app/blog/layout.js` each become root layouts for their respective directories.
  - Navigating **across multiple root layouts** will cause a **full page load** (as opposed to a client-side navigation).
- The root layout can be under a **dynamic segment**, for example when implementing [internationalization](https://nextjs.org/docs/app/guides/internationalization) with `app/[lang]/layout.js`.

## Caveats

### Request Object

Layouts are cached in the client during navigation to avoid unnecessary server requests.

[Layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout) do not rerender. They can be cached and reused to avoid unnecessary computation when navigating between pages. By restricting layouts from accessing the raw request, Next.js can prevent the execution of potentially slow or expensive user code within the layout, which could negatively impact performance.

To access the request object, you can use [headers](https://nextjs.org/docs/app/api-reference/functions/headers) and [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies) APIs in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) and Functions.

 app/shop/layout.tsxJavaScriptTypeScript

```
import { cookies } from 'next/headers'

export default async function Layout({ children }) {
  const cookieStore = await cookies()
  const theme = cookieStore.get('theme')
  return '...'
}
```

### Query params

Layouts do not rerender on navigation, so they cannot access search params which would otherwise become stale.

To access updated query parameters, you can use the Page [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) prop, or read them inside a Client Component using the [useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params) hook. Since Client Components re-render on navigation, they have access to the latest query parameters.

 app/ui/search.tsxJavaScriptTypeScript

```
'use client'

import { useSearchParams } from 'next/navigation'

export default function Search() {
  const searchParams = useSearchParams()

  const search = searchParams.get('search')

  return '...'
}
```

   app/shop/layout.tsxJavaScriptTypeScript

```
import Search from '@/app/ui/search'

export default function Layout({ children }) {
  return (
    <>
      <Search />
      {children}
    </>
  )
}
```

### Pathname

Layouts do not re-render on navigation, so they do not access pathname which would otherwise become stale.

To access the current pathname, you can read it inside a Client Component using the [usePathname](https://nextjs.org/docs/app/api-reference/functions/use-pathname) hook. Since Client Components re-render during navigation, they have access to the latest pathname.

 app/ui/breadcrumbs.tsxJavaScriptTypeScript

```
'use client'

import { usePathname } from 'next/navigation'

// Simplified breadcrumbs logic
export default function Breadcrumbs() {
  const pathname = usePathname()
  const segments = pathname.split('/')

  return (
    <nav>
      {segments.map((segment, index) => (
        <span key={index}>
          {' > '}
          {segment}
        </span>
      ))}
    </nav>
  )
}
```

   app/docs/layout.tsxJavaScriptTypeScript

```
import { Breadcrumbs } from '@/app/ui/Breadcrumbs'

export default function Layout({ children }) {
  return (
    <>
      <Breadcrumbs />
      <main>{children}</main>
    </>
  )
}
```

### Fetching Data

Layouts cannot pass data to their `children`. However, you can fetch the same data in a route more than once, and use React [cache](https://react.dev/reference/react/cache) to dedupe the requests without affecting performance.

Alternatively, when using [fetch](https://nextjs.org/docs/app/api-reference/functions/fetch)in Next.js, requests are automatically deduped.

 app/lib/data.tsJavaScriptTypeScript

```
export async function getUser(id: string) {
  const res = await fetch(`https://.../users/${id}`)
  return res.json()
}
```

 app/dashboard/layout.tsxJavaScriptTypeScript

```
import { getUser } from '@/app/lib/data'
import { UserName } from '@/app/ui/user-name'

export default async function Layout({ children }) {
  const user = await getUser('1')

  return (
    <>
      <nav>
        {/* ... */}
        <UserName user={user.name} />
      </nav>
      {children}
    </>
  )
}
```

   app/dashboard/page.tsxJavaScriptTypeScript

```
import { getUser } from '@/app/lib/data'
import { UserName } from '@/app/ui/user-name'

export default async function Page() {
  const user = await getUser('1')

  return (
    <div>
      <h1>Welcome {user.name}</h1>
    </div>
  )
}
```

### Accessing child segments

Layouts do not have access to the route segments below itself. To access all route segments, you can use [useSelectedLayoutSegment](https://nextjs.org/docs/app/api-reference/functions/use-selected-layout-segment) or [useSelectedLayoutSegments](https://nextjs.org/docs/app/api-reference/functions/use-selected-layout-segments) in a Client Component.

 app/ui/nav-link.tsxJavaScriptTypeScript

```
'use client'

import Link from 'next/link'
import { useSelectedLayoutSegment } from 'next/navigation'

export default function NavLink({
  slug,
  children,
}: {
  slug: string
  children: React.ReactNode
}) {
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
import { NavLink } from './nav-link'
import getPosts from './get-posts'

export default async function Layout({
  children,
}: {
  children: React.ReactNode
}) {
  const featuredPosts = await getPosts()
  return (
    <div>
      {featuredPosts.map((post) => (
        <div key={post.id}>
          <NavLink slug={post.slug}>{post.title}</NavLink>
        </div>
      ))}
      <div>{children}</div>
    </div>
  )
}
```

## Examples

### Metadata

You can modify the `<head>` HTML elements such as `title` and `meta` using the [metadataobject](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#the-metadata-object) or [generateMetadatafunction](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#generatemetadata-function).

 app/layout.tsxJavaScriptTypeScript

```
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Next.js',
}

export default function Layout({ children }: { children: React.ReactNode }) {
  return '...'
}
```

> **Good to know**: You should **not** manually add `<head>` tags such as `<title>` and `<meta>` to root layouts. Instead, use the [Metadata APIs](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) which automatically handles advanced requirements such as streaming and de-duplicating `<head>` elements.

### Active Nav Links

You can use the [usePathname](https://nextjs.org/docs/app/api-reference/functions/use-pathname) hook to determine if a nav link is active.

Since `usePathname` is a client hook, you need to extract the nav links into a Client Component, which can be imported into your layout:

 app/ui/nav-links.tsxJavaScriptTypeScript

```
'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'

export function NavLinks() {
  const pathname = usePathname()

  return (
    <nav>
      <Link className={`link ${pathname === '/' ? 'active' : ''}`} href="/">
        Home
      </Link>

      <Link
        className={`link ${pathname === '/about' ? 'active' : ''}`}
        href="/about"
      >
        About
      </Link>
    </nav>
  )
}
```

   app/layout.tsxJavaScriptTypeScript

```
import { NavLinks } from '@/app/ui/nav-links'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <NavLinks />
        <main>{children}</main>
      </body>
    </html>
  )
}
```

### Displaying content based onparams

Using [dynamic route segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes), you can display or fetch specific content based on the `params` prop.

 app/dashboard/layout.tsxJavaScriptTypeScript

```
export default async function DashboardLayout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ team: string }>
}) {
  const { team } = await params

  return (
    <section>
      <header>
        <h1>Welcome to {team}'s Dashboard</h1>
      </header>
      <main>{children}</main>
    </section>
  )
}
```

### Readingparamsin Client Components

To use `params` in a Client Component (which cannot be `async`), you can use React's [use](https://react.dev/reference/react/use) function to read the promise:

 app/page.tsxJavaScriptTypeScript

```
'use client'

import { use } from 'react'

export default function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = use(params)
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0-RC | paramsis now a promise. Acodemodis available. |
| v13.0.0 | layoutintroduced. |

Was this helpful?

supported.
