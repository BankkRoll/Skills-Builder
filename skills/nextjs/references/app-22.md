# Layouts and Pages and more

# Layouts and Pages

> Learn how to create your first pages and layouts, and link between them with the Link component.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Layouts and Pages

# Layouts and Pages

Last updated  November 17, 2025

Next.js uses **file-system based routing**, meaning you can use folders and files to define routes. This page will guide you through how to create layouts and pages, and link between them.

## Creating a page

A **page** is UI that is rendered on a specific route. To create a page, add a [pagefile](https://nextjs.org/docs/app/api-reference/file-conventions/page) inside the `app` directory and default export a React component. For example, to create an index page (`/`):

 ![page.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fpage-special-file.png&w=3840&q=75)![page.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fpage-special-file.png&w=3840&q=75) app/page.tsxJavaScriptTypeScript

```
export default function Page() {
  return <h1>Hello Next.js!</h1>
}
```

## Creating a layout

A layout is UI that is **shared** between multiple pages. On navigation, layouts preserve state, remain interactive, and do not rerender.

You can define a layout by default exporting a React component from a [layoutfile](https://nextjs.org/docs/app/api-reference/file-conventions/layout). The component should accept a `children` prop which can be a page or another [layout](#nesting-layouts).

For example, to create a layout that accepts your index page as child, add a `layout` file inside the `app` directory:

 ![layout.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Flayout-special-file.png&w=3840&q=75)![layout.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Flayout-special-file.png&w=3840&q=75) app/layout.tsxJavaScriptTypeScript

```
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {/* Layout UI */}
        {/* Place children where you want to render a page or nested layout */}
        <main>{children}</main>
      </body>
    </html>
  )
}
```

The layout above is called a [root layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout) because it's defined at the root of the `app` directory. The root layout is **required** and must contain `html` and `body` tags.

## Creating a nested route

A nested route is a route composed of multiple URL segments. For example, the `/blog/[slug]` route is composed of three segments:

- `/` (Root Segment)
- `blog` (Segment)
- `[slug]` (Leaf Segment)

In Next.js:

- **Folders** are used to define the route segments that map to URL segments.
- **Files** (like `page` and `layout`) are used to create UI that is shown for a segment.

To create nested routes, you can nest folders inside each other. For example, to add a route for `/blog`, create a folder called `blog` in the `app` directory. Then, to make `/blog` publicly accessible, add a `page.tsx` file:

 ![File hierarchy showing blog folder and a page.js file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fblog-nested-route.png&w=3840&q=75)![File hierarchy showing blog folder and a page.js file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fblog-nested-route.png&w=3840&q=75) app/blog/page.tsxJavaScriptTypeScript

```
// Dummy imports
import { getPosts } from '@/lib/posts'
import { Post } from '@/ui/post'

export default async function Page() {
  const posts = await getPosts()

  return (
    <ul>
      {posts.map((post) => (
        <Post key={post.id} post={post} />
      ))}
    </ul>
  )
}
```

You can continue nesting folders to create nested routes. For example, to create a route for a specific blog post, create a new `[slug]` folder inside `blog` and add a `page` file:

 ![File hierarchy showing blog folder with a nested slug folder and a page.js file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fblog-post-nested-route.png&w=3840&q=75)![File hierarchy showing blog folder with a nested slug folder and a page.js file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fblog-post-nested-route.png&w=3840&q=75) app/blog/[slug]/page.tsxJavaScriptTypeScript

```
function generateStaticParams() {}

export default function Page() {
  return <h1>Hello, Blog Post Page!</h1>
}
```

Wrapping a folder name in square brackets (e.g. `[slug]`) creates a [dynamic route segment](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) which is used to generate multiple pages from data. e.g. blog posts, product pages, etc.

## Nesting layouts

By default, layouts in the folder hierarchy are also nested, which means they wrap child layouts via their `children` prop. You can nest layouts by adding `layout` inside specific route segments (folders).

For example, to create a layout for the `/blog` route, add a new `layout` file inside the `blog` folder.

 ![File hierarchy showing root layout wrapping the blog layout](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fnested-layouts.png&w=3840&q=75)![File hierarchy showing root layout wrapping the blog layout](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fnested-layouts.png&w=3840&q=75) app/blog/layout.tsxJavaScriptTypeScript

```
export default function BlogLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <section>{children}</section>
}
```

If you were to combine the two layouts above, the root layout (`app/layout.js`) would wrap the blog layout (`app/blog/layout.js`), which would wrap the blog (`app/blog/page.js`) and blog post page (`app/blog/[slug]/page.js`).

## Creating a dynamic segment

[Dynamic segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) allow you to create routes that are generated from data. For example, instead of manually creating a route for each individual blog post, you can create a dynamic segment to generate the routes based on blog post data.

To create a dynamic segment, wrap the segment (folder) name in square brackets: `[segmentName]`. For example, in the `app/blog/[slug]/page.tsx` route, the `[slug]` is the dynamic segment.

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)

  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </div>
  )
}
```

Learn more about [Dynamic Segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) and the [params](https://nextjs.org/docs/app/api-reference/file-conventions/page#params-optional) props.

Nested [layouts within Dynamic Segments](https://nextjs.org/docs/app/api-reference/file-conventions/layout#params-optional), can also access the `params` props.

## Rendering with search params

In a Server Component **page**, you can access search parameters using the [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) prop:

 app/page.tsxJavaScriptTypeScript

```
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const filters = (await searchParams).filters
}
```

Using `searchParams` opts your page into [dynamic rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) because it requires an incoming request to read the search parameters from.

Client Components can read search params using the [useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params) hook.

Learn more about `useSearchParams` in [statically rendered](https://nextjs.org/docs/app/api-reference/functions/use-search-params#static-rendering) and [dynamically rendered](https://nextjs.org/docs/app/api-reference/functions/use-search-params#dynamic-rendering) routes.

### What to use and when

- Use the `searchParams` prop when you need search parameters to **load data for the page** (e.g. pagination, filtering from a database).
- Use `useSearchParams` when search parameters are used **only on the client** (e.g. filtering a list already loaded via props).
- As a small optimization, you can use `new URLSearchParams(window.location.search)` in **callbacks or event handlers** to read search params without triggering re-renders.

## Linking between pages

You can use the [<Link>component](https://nextjs.org/docs/app/api-reference/components/link) to navigate between routes. `<Link>` is a built-in Next.js component that extends the HTML `<a>` tag to provide [prefetching](https://nextjs.org/docs/app/getting-started/linking-and-navigating#prefetching) and [client-side navigation](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions).

For example, to generate a list of blog posts, import `<Link>` from `next/link` and pass a `href` prop to the component:

 app/ui/post.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default async function Post({ post }) {
  const posts = await getPosts()

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.slug}>
          <Link href={`/blog/${post.slug}`}>{post.title}</Link>
        </li>
      ))}
    </ul>
  )
}
```

> **Good to know**: `<Link>` is the primary way to navigate between routes in Next.js. You can also use the [useRouterhook](https://nextjs.org/docs/app/api-reference/functions/use-router) for more advanced navigation.

## Route Props Helpers

Next.js exposes utility types that infer `params` and named slots from your route structure:

- [PageProps](https://nextjs.org/docs/app/api-reference/file-conventions/page#page-props-helper): Props for `page` components, including `params` and `searchParams`.
- [LayoutProps](https://nextjs.org/docs/app/api-reference/file-conventions/layout#layout-props-helper): Props for `layout` components, including `children` and any named slots (e.g. folders like `@analytics`).

These are globally available helpers, generated when running either `next dev`, `next build` or [next typegen](https://nextjs.org/docs/app/api-reference/cli/next#next-typegen-options).

 app/blog/[slug]/page.tsx

```
export default async function Page(props: PageProps<'/blog/[slug]'>) {
  const { slug } = await props.params
  return <h1>Blog post: {slug}</h1>
}
```

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

> **Good to know**
>
>
>
> - Static routes resolve `params` to `{}`.
> - `PageProps`, `LayoutProps` are global helpers — no imports required.
> - Types are generated during `next dev`, `next build` or `next typegen`.

## API Reference

Learn more about the features mentioned in this page by reading the API Reference.[Linking and NavigatingLearn how the built-in navigation optimizations work, including prefetching, prerendering, and client-side navigation, and how to optimize navigation for dynamic routes and slow networks.](https://nextjs.org/docs/app/getting-started/linking-and-navigating)[layout.jsAPI reference for the layout.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/layout)[page.jsAPI reference for the page.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/page)[Link ComponentEnable fast client-side navigation with the built-in `next/link` component.](https://nextjs.org/docs/app/api-reference/components/link)[Dynamic SegmentsDynamic Route Segments can be used to programmatically generate route segments from dynamic data.](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes)

Was this helpful?

supported.

---

# Linking and Navigating

> Learn how the built-in navigation optimizations work, including prefetching, prerendering, and client-side navigation, and how to optimize navigation for dynamic routes and slow networks.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Linking and Navigating

# Linking and Navigating

Last updated  December 19, 2025

In Next.js, routes are rendered on the server by default. This often means the client has to wait for a server response before a new route can be shown. Next.js comes with built-in [prefetching](#prefetching), [streaming](#streaming), and [client-side transitions](#client-side-transitions) ensuring navigation stays fast and responsive.

This guide explains how navigation works in Next.js and how you can optimize it for [dynamic routes](#dynamic-routes-without-loadingtsx) and [slow networks](#slow-networks).

## How navigation works

To understand how navigation works in Next.js, it helps to be familiar with the following concepts:

- [Server Rendering](#server-rendering)
- [Prefetching](#prefetching)
- [Streaming](#streaming)
- [Client-side transitions](#client-side-transitions)

### Server Rendering

In Next.js, [Layouts and Pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages) are [React Server Components](https://react.dev/reference/rsc/server-components) by default. On initial and subsequent navigations, the [Server Component Payload](https://nextjs.org/docs/app/getting-started/server-and-client-components#how-do-server-and-client-components-work-in-nextjs) is generated on the server before being sent to the client.

There are two types of server rendering, based on *when* it happens:

- **Static Rendering (or Prerendering)** happens at build time or during [revalidation](https://nextjs.org/docs/app/getting-started/caching-and-revalidating) and the result is cached.
- **Dynamic Rendering** happens at request time in response to a client request.

The trade-off of server rendering is that the client must wait for the server to respond before the new route can be shown. Next.js addresses this delay by [prefetching](#prefetching) routes the user is likely to visit and performing [client-side transitions](#client-side-transitions).

> **Good to know**: HTML is also generated for the initial visit.

### Prefetching

Prefetching is the process of loading a route in the background before the user navigates to it. This makes navigation between routes in your application feel instant, because by the time a user clicks on a link, the data to render the next route is already available client side.

Next.js automatically prefetches routes linked with the [<Link>component](https://nextjs.org/docs/app/api-reference/components/link) when they enter the user's viewport.

 app/layout.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <nav>
          {/* Prefetched when the link is hovered or enters the viewport */}
          <Link href="/blog">Blog</Link>
          {/* No prefetching */}
          <a href="/contact">Contact</a>
        </nav>
        {children}
      </body>
    </html>
  )
}
```

How much of the route is prefetched depends on whether it's static or dynamic:

- **Static Route**: the full route is prefetched.
- **Dynamic Route**: prefetching is skipped, or the route is partially prefetched if [loading.tsx](https://nextjs.org/docs/app/api-reference/file-conventions/loading) is present.

By skipping or partially prefetching dynamic routes, Next.js avoids unnecessary work on the server for routes the users may never visit. However, waiting for a server response before navigation can give the users the impression that the app is not responding.

 ![Server Rendering without Streaming](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fserver-rendering-without-streaming.png&w=3840&q=75)![Server Rendering without Streaming](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fserver-rendering-without-streaming.png&w=3840&q=75)

To improve the navigation experience to dynamic routes, you can use [streaming](#streaming).

### Streaming

Streaming allows the server to send parts of a dynamic route to the client as soon as they're ready, rather than waiting for the entire route to be rendered. This means users see something sooner, even if parts of the page are still loading.

For dynamic routes, it means they can be **partially prefetched**. That is, shared layouts and loading skeletons can be requested ahead of time.

 ![How Server Rendering with Streaming Works](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fserver-rendering-with-streaming.png&w=3840&q=75)![How Server Rendering with Streaming Works](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fserver-rendering-with-streaming.png&w=3840&q=75)

To use streaming, create a `loading.tsx` in your route folder:

 ![loading.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Floading-special-file.png&w=3840&q=75)![loading.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Floading-special-file.png&w=3840&q=75) app/dashboard/loading.tsxJavaScriptTypeScript

```
export default function Loading() {
  // Add fallback UI that will be shown while the route is loading.
  return <LoadingSkeleton />
}
```

Behind the scenes, Next.js will automatically wrap the `page.tsx` contents in a `<Suspense>` boundary. The prefetched fallback UI will be shown while the route is loading, and swapped for the actual content once ready.

> **Good to know**: You can also use [<Suspense>](https://react.dev/reference/react/Suspense) to create loading UI for nested components.

Benefits of `loading.tsx`:

- Immediate navigation and visual feedback for the user.
- Shared layouts remain interactive and navigation is interruptible.
- Improved Core Web Vitals: [TTFB](https://web.dev/articles/ttfb), [FCP](https://web.dev/articles/fcp), and [TTI](https://web.dev/articles/tti).

To further improve the navigation experience, Next.js performs a [client-side transition](#client-side-transitions) with the `<Link>` component.

### Client-side transitions

Traditionally, navigation to a server-rendered page triggers a full page load. This clears state, resets scroll position, and blocks interactivity.

Next.js avoids this with client-side transitions using the `<Link>` component. Instead of reloading the page, it updates the content dynamically by:

- Keeping any shared layouts and UI.
- Replacing the current page with the prefetched loading state or a new page if available.

Client-side transitions are what makes a server-rendered apps *feel* like client-rendered apps. And when paired with [prefetching](#prefetching) and [streaming](#streaming), it enables fast transitions, even for dynamic routes.

## What can make transitions slow?

These Next.js optimizations make navigation fast and responsive. However, under certain conditions, transitions can still *feel* slow. Here are some common causes and how to improve the user experience:

### Dynamic routes withoutloading.tsx

When navigating to a dynamic route, the client must wait for the server response before showing the result. This can give the users the impression that the app is not responding.

We recommend adding `loading.tsx` to dynamic routes to enable partial prefetching, trigger immediate navigation, and display a loading UI while the route renders.

 app/blog/[slug]/loading.tsxJavaScriptTypeScript

```
export default function Loading() {
  return <LoadingSkeleton />
}
```

> **Good to know**: In development mode, you can use the Next.js Devtools to identify if the route is static or dynamic. See [devIndicators](https://nextjs.org/docs/app/api-reference/config/next-config-js/devIndicators) for more information.

### Dynamic segments withoutgenerateStaticParams

If a [dynamic segment](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) could be prerendered but isn't because it's missing [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params), the route will fallback to dynamic rendering at request time.

Ensure the route is statically generated at build time by adding `generateStaticParams`:

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())

  return posts.map((post) => ({
    slug: post.slug,
  }))
}

export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // ...
}
```

### Slow networks

On slow or unstable networks, prefetching may not finish before the user clicks a link. This can affect both static and dynamic routes. In these cases, the `loading.js` fallback may not appear immediately because it hasn't been prefetched yet.

To improve perceived performance, you can use the [useLinkStatushook](https://nextjs.org/docs/app/api-reference/functions/use-link-status) to show immediate feedback while the transition is in progress.

 app/ui/loading-indicator.tsxJavaScriptTypeScript

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

You can "debounce" the hint by adding an initial animation delay (e.g. 100ms) and starting as invisible (e.g. `opacity: 0`). This means the loading indicator will only be shown if the navigation takes longer than the specified delay. See the [useLinkStatusreference](https://nextjs.org/docs/app/api-reference/functions/use-link-status#gracefully-handling-fast-navigation) for a CSS example.

> **Good to know**: You can use other visual feedback patterns like a progress bar. View an example [here](https://github.com/vercel/react-transition-progress).

### Disabling prefetching

You can opt out of prefetching by setting the `prefetch` prop to `false` on the `<Link>` component. This is useful to avoid unnecessary usage of resources when rendering large lists of links (e.g. an infinite scroll table).

```
<Link prefetch={false} href="/blog">
  Blog
</Link>
```

However, disabling prefetching comes with trade-offs:

- **Static routes** will only be fetched when the user clicks the link.
- **Dynamic routes** will need to be rendered on the server first before the client can navigate to it.

To reduce resource usage without fully disabling prefetch, you can prefetch only on hover. This limits prefetching to routes the user is more *likely* to visit, rather than all links in the viewport.

 app/ui/hover-prefetch-link.tsxJavaScriptTypeScript

```
'use client'

import Link from 'next/link'
import { useState } from 'react'

function HoverPrefetchLink({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  const [active, setActive] = useState(false)

  return (
    <Link
      href={href}
      prefetch={active ? null : false}
      onMouseEnter={() => setActive(true)}
    >
      {children}
    </Link>
  )
}
```

### Hydration not completed

`<Link>` is a Client Component and must be hydrated before it can prefetch routes. On the initial visit, large JavaScript bundles can delay hydration, preventing prefetching from starting right away.

React mitigates this with Selective Hydration and you can further improve this by:

- Using the [@next/bundle-analyzer](https://nextjs.org/docs/app/guides/package-bundling#nextbundle-analyzer-for-webpack) plugin to identify and reduce bundle size by removing large dependencies.
- Moving logic from the client to the server where possible. See the [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) docs for guidance.

## Examples

### Native History API

Next.js allows you to use the native [window.history.pushState](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState) and [window.history.replaceState](https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState) methods to update the browser's history stack without reloading the page.

`pushState` and `replaceState` calls integrate into the Next.js Router, allowing you to sync with [usePathname](https://nextjs.org/docs/app/api-reference/functions/use-pathname) and [useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params).

#### window.history.pushState

Use it to add a new entry to the browser's history stack. The user can navigate back to the previous state. For example, to sort a list of products:

```
'use client'

import { useSearchParams } from 'next/navigation'

export default function SortProducts() {
  const searchParams = useSearchParams()

  function updateSorting(sortOrder: string) {
    const params = new URLSearchParams(searchParams.toString())
    params.set('sort', sortOrder)
    window.history.pushState(null, '', `?${params.toString()}`)
  }

  return (
    <>
      <button onClick={() => updateSorting('asc')}>Sort Ascending</button>
      <button onClick={() => updateSorting('desc')}>Sort Descending</button>
    </>
  )
}
```

#### window.history.replaceState

Use it to replace the current entry on the browser's history stack. The user is not able to navigate back to the previous state. For example, to switch the application's locale:

```
'use client'

import { usePathname } from 'next/navigation'

export function LocaleSwitcher() {
  const pathname = usePathname()

  function switchLocale(locale: string) {
    // e.g. '/en/about' or '/fr/contact'
    const newPath = `/${locale}${pathname}`
    window.history.replaceState(null, '', newPath)
  }

  return (
    <>
      <button onClick={() => switchLocale('en')}>English</button>
      <button onClick={() => switchLocale('fr')}>French</button>
    </>
  )
}
```

 [Link ComponentEnable fast client-side navigation with the built-in `next/link` component.](https://nextjs.org/docs/app/api-reference/components/link)[loading.jsAPI reference for the loading.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/loading)[PrefetchingLearn how to configure prefetching in Next.js](https://nextjs.org/docs/app/guides/prefetching)

Was this helpful?

supported.

---

# Metadata and OG images

> Learn how to add metadata to your pages and create dynamic OG images.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Metadata and OG images

# Metadata and OG images

Last updated  November 17, 2025

The Metadata APIs can be used to define your application metadata for improved SEO and web shareability and include:

1. [The staticmetadataobject](#static-metadata)
2. [The dynamicgenerateMetadatafunction](#generated-metadata)
3. Special [file conventions](https://nextjs.org/docs/app/api-reference/file-conventions/metadata) that can be used to add static or dynamically generated [favicons](#favicons) and [OG images](#static-open-graph-images).

With all the options above, Next.js will automatically generate the relevant `<head>` tags for your page, which can be inspected in the browser's developer tools.

The `metadata` object and `generateMetadata` function exports are only supported in Server Components.

## Default fields

There are two default `meta` tags that are always added even if a route doesn't define metadata:

- The [meta charset tag](https://developer.mozilla.org/docs/Web/HTML/Element/meta#attr-charset) sets the character encoding for the website.
- The [meta viewport tag](https://developer.mozilla.org/docs/Web/HTML/Viewport_meta_tag) sets the viewport width and scale for the website to adjust for different devices.

```
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

The other metadata fields can be defined with the `Metadata` object (for [static metadata](#static-metadata)) or the `generateMetadata` function (for [generated metadata](#generated-metadata)).

## Static metadata

To define static metadata, export a [Metadataobject](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#metadata-object) from a static [layout.js](https://nextjs.org/docs/app/api-reference/file-conventions/layout) or [page.js](https://nextjs.org/docs/app/api-reference/file-conventions/page) file. For example, to add a title and description to the blog route:

 app/blog/layout.tsxJavaScriptTypeScript

```
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My Blog',
  description: '...',
}

export default function Layout() {}
```

You can view a full list of available options, in the [generateMetadatadocumentation](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#metadata-fields).

## Generated metadata

You can use [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) function to `fetch` metadata that depends on data. For example, to fetch the title and description for a specific blog post:

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
import type { Metadata, ResolvingMetadata } from 'next'

type Props = {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export async function generateMetadata(
  { params, searchParams }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const slug = (await params).slug

  // fetch post information
  const post = await fetch(`https://api.vercel.app/blog/${slug}`).then((res) =>
    res.json()
  )

  return {
    title: post.title,
    description: post.description,
  }
}

export default function Page({ params, searchParams }: Props) {}
```

### Streaming metadata

For dynamically rendered pages, Next.js streams metadata separately, injecting it into the HTML once `generateMetadata` resolves, without blocking UI rendering.

Streaming metadata improves perceived performance by allowing visual content to stream first.

Streaming metadata is **disabled for bots and crawlers** that expect metadata to be in the `<head>` tag (e.g. `Twitterbot`, `Slackbot`, `Bingbot`). These are detected by using the User Agent header from the incoming request.

You can customize or **disable** streaming metadata completely, with the [htmlLimitedBots](https://nextjs.org/docs/app/api-reference/config/next-config-js/htmlLimitedBots#disabling) option in your Next.js config file.

Statically rendered pages don’t use streaming since metadata is resolved at build time.

Learn more about [streaming metadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#streaming-metadata).

### Memoizing data requests

There may be cases where you need to fetch the **same** data for metadata and the page itself. To avoid duplicate requests, you can use React's [cachefunction](https://react.dev/reference/react/cache) to memoize the return value and only fetch the data once. For example, to fetch the blog post information for both the metadata and the page:

 app/lib/data.tsJavaScriptTypeScript

```
import { cache } from 'react'
import { db } from '@/app/lib/db'

// getPost will be used twice, but execute only once
export const getPost = cache(async (slug: string) => {
  const res = await db.query.posts.findFirst({ where: eq(posts.slug, slug) })
  return res
})
```

   app/blog/[slug]/page.tsxJavaScriptTypeScript

```
import { getPost } from '@/app/lib/data'

export async function generateMetadata({
  params,
}: {
  params: { slug: string }
}) {
  const post = await getPost(params.slug)
  return {
    title: post.title,
    description: post.description,
  }
}

export default async function Page({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug)
  return <div>{post.title}</div>
}
```

## File-based metadata

The following special files are available for metadata:

- [favicon.ico, apple-icon.jpg, and icon.jpg](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons)
- [opengraph-image.jpg and twitter-image.jpg](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image)
- [robots.txt](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots)
- [sitemap.xml](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap)

You can use these for static metadata, or you can programmatically generate these files with code.

## Favicons

Favicons are small icons that represent your site in bookmarks and search results. To add a favicon to your application, create a `favicon.ico` and add to the root of the app folder.

 ![Favicon Special File inside the App Folder with sibling layout and page files](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ffavicon-ico.png&w=3840&q=75)![Favicon Special File inside the App Folder with sibling layout and page files](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ffavicon-ico.png&w=3840&q=75)

> You can also programmatically generate favicons using code. See the [favicon docs](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons) for more information.

## Static Open Graph images

Open Graph (OG) images are images that represent your site in social media. To add a static OG image to your application, create a `opengraph-image.jpg` file in the root of the app folder.

 ![OG image special file inside the App folder with sibling layout and page files](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fopengraph-image.png&w=3840&q=75)![OG image special file inside the App folder with sibling layout and page files](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fopengraph-image.png&w=3840&q=75)

You can also add OG images for specific routes by creating a `opengraph-image.jpg` deeper down the folder structure. For example, to create an OG image specific to the `/blog` route, add a `opengraph-image.jpg` file inside the `blog` folder.

 ![OG image special file inside the blog folder](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fopengraph-image-blog.png&w=3840&q=75)![OG image special file inside the blog folder](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fopengraph-image-blog.png&w=3840&q=75)

The more specific image will take precedence over any OG images above it in the folder structure.

> Other image formats such as `jpeg`, `png`, and `gif` are also supported. See the [Open Graph Image docs](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image) for more information.

## Generated Open Graph images

The [ImageResponseconstructor](https://nextjs.org/docs/app/api-reference/functions/image-response) allows you to generate dynamic images using JSX and CSS. This is useful for OG images that depend on data.

For example, to generate a unique OG image for each blog post, add a `opengraph-image.tsx` file inside the `blog` folder, and import the `ImageResponse` constructor from `next/og`:

 app/blog/[slug]/opengraph-image.tsxJavaScriptTypeScript

```
import { ImageResponse } from 'next/og'
import { getPost } from '@/app/lib/data'

// Image metadata
export const size = {
  width: 1200,
  height: 630,
}

export const contentType = 'image/png'

// Image generation
export default async function Image({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug)

  return new ImageResponse(
    (
      // ImageResponse JSX element
      <div
        style={{
          fontSize: 128,
          background: 'white',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {post.title}
      </div>
    )
  )
}
```

`ImageResponse` supports common CSS properties including flexbox and absolute positioning, custom fonts, text wrapping, centering, and nested images. [See the full list of supported CSS properties](https://nextjs.org/docs/app/api-reference/functions/image-response).

> **Good to know**:
>
>
>
> - Examples are available in the [Vercel OG Playground](https://og-playground.vercel.app/).
> - `ImageResponse` uses [@vercel/og](https://vercel.com/docs/og-image-generation), [satori](https://github.com/vercel/satori), and `resvg` to convert HTML and CSS into PNG.
> - Only flexbox and a subset of CSS properties are supported. Advanced layouts (e.g. `display: grid`) will not work.

## API Reference

Learn more about the Metadata APIs mentioned in this page.[generateMetadataLearn how to add Metadata to your Next.js application for improved search engine optimization (SEO) and web shareability.](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)[generateViewportAPI Reference for the generateViewport function.](https://nextjs.org/docs/app/api-reference/functions/generate-viewport)[ImageResponseAPI Reference for the ImageResponse constructor.](https://nextjs.org/docs/app/api-reference/functions/image-response)[Metadata FilesAPI documentation for the metadata file conventions.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)[favicon, icon, and apple-iconAPI Reference for the Favicon, Icon and Apple Icon file conventions.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons)[opengraph-image and twitter-imageAPI Reference for the Open Graph Image and Twitter Image file conventions.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image)[robots.txtAPI Reference for robots.txt file.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots)[sitemap.xmlAPI Reference for the sitemap.xml file.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap)[htmlLimitedBotsSpecify a list of user agents that should receive blocking metadata.](https://nextjs.org/docs/app/api-reference/config/next-config-js/htmlLimitedBots)

Was this helpful?

supported.
