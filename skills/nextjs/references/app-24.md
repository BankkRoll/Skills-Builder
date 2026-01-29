# Updating Data and more

# Updating Data

> Learn how to mutate data using Server Functions and Server Actions in Next.js.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Updating Data

# Updating Data

Last updated  January 23, 2026

You can update data in Next.js using React's [Server Functions](https://react.dev/reference/rsc/server-functions). This page will go through how you can [create](#creating-server-functions) and [invoke](#invoking-server-functions) Server Functions.

## What are Server Functions?

A **Server Function** is an asynchronous function that runs on the server. They can be called from the client through a network request, which is why they must be asynchronous.

In an `action` or mutation context, they are also called **Server Actions**.

> **Good to know:** A Server Action is a Server Function used in a specific way (for handling form submissions and mutations). Server Function is the broader term.

By convention, a Server Action is an async function used with [startTransition](https://react.dev/reference/react/startTransition). This happens automatically when the function is:

- Passed to a `<form>` using the `action` prop.
- Passed to a `<button>` using the `formAction` prop.

In Next.js, Server Actions integrate with the framework's [caching](https://nextjs.org/docs/app/guides/caching) architecture. When an action is invoked, Next.js can return both the updated UI and new data in a single server roundtrip.

Behind the scenes, actions use the `POST` method, and only this HTTP method can invoke them.

## Creating Server Functions

A Server Function can be defined by using the [use server](https://react.dev/reference/rsc/use-server) directive. You can place the directive at the top of an **asynchronous** function to mark the function as a Server Function, or at the top of a separate file to mark all exports of that file.

 app/lib/actions.tsJavaScriptTypeScript

```
export async function createPost(formData: FormData) {
  'use server'
  const title = formData.get('title')
  const content = formData.get('content')

  // Update data
  // Revalidate cache
}

export async function deletePost(formData: FormData) {
  'use server'
  const id = formData.get('id')

  // Update data
  // Revalidate cache
}
```

### Server Components

Server Functions can be inlined in Server Components by adding the `"use server"` directive to the top of the function body:

 app/page.tsxJavaScriptTypeScript

```
export default function Page() {
  // Server Action
  async function createPost(formData: FormData) {
    'use server'
    // ...
  }

  return <></>
}
```

> **Good to know:** Server Components support progressive enhancement by default, meaning forms that call Server Actions will be submitted even if JavaScript hasn't loaded yet or is disabled.

### Client Components

It's not possible to define Server Functions in Client Components. However, you can invoke them in Client Components by importing them from a file that has the `"use server"` directive at the top of it:

 app/actions.tsJavaScriptTypeScript

```
'use server'

export async function createPost() {}
```

   app/ui/button.tsxJavaScriptTypeScript

```
'use client'

import { createPost } from '@/app/actions'

export function Button() {
  return <button formAction={createPost}>Create</button>
}
```

> **Good to know:** In Client Components, forms invoking Server Actions will queue submissions if JavaScript isn't loaded yet, and will be prioritized for hydration. After hydration, the browser does not refresh on form submission.

### Passing actions as props

You can also pass an action to a Client Component as a prop:

```
<ClientComponent updateItemAction={updateItem} />
```

 app/client-component.tsxJavaScriptTypeScript

```
'use client'

export default function ClientComponent({
  updateItemAction,
}: {
  updateItemAction: (formData: FormData) => void
}) {
  return <form action={updateItemAction}>{/* ... */}</form>
}
```

## Invoking Server Functions

There are two main ways you can invoke a Server Function:

1. [Forms](#forms) in Server and Client Components
2. [Event Handlers](#event-handlers) and [useEffect](#useeffect) in Client Components

> **Good to know:** Server Functions are designed for server-side mutations. The client currently dispatches and awaits them one at a time. This is an implementation detail and may change. If you need parallel data fetching, use [data fetching](https://nextjs.org/docs/app/getting-started/fetching-data#server-components) in Server Components, or perform parallel work inside a single Server Function or [Route Handler](https://nextjs.org/docs/app/guides/backend-for-frontend#manipulating-data).

### Forms

React extends the HTML [<form>](https://react.dev/reference/react-dom/components/form) element to allow a Server Function to be invoked with the HTML `action` prop.

When invoked in a form, the function automatically receives the [FormData](https://developer.mozilla.org/docs/Web/API/FormData/FormData) object. You can extract the data using the native [FormDatamethods](https://developer.mozilla.org/en-US/docs/Web/API/FormData#instance_methods):

 app/ui/form.tsxJavaScriptTypeScript

```
import { createPost } from '@/app/actions'

export function Form() {
  return (
    <form action={createPost}>
      <input type="text" name="title" />
      <input type="text" name="content" />
      <button type="submit">Create</button>
    </form>
  )
}
```

   app/actions.tsJavaScriptTypeScript

```
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  const content = formData.get('content')

  // Update data
  // Revalidate cache
}
```

### Event Handlers

You can invoke a Server Function in a Client Component by using event handlers such as `onClick`.

 app/like-button.tsxJavaScriptTypeScript

```
'use client'

import { incrementLike } from './actions'
import { useState } from 'react'

export default function LikeButton({ initialLikes }: { initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes)

  return (
    <>
      <p>Total Likes: {likes}</p>
      <button
        onClick={async () => {
          const updatedLikes = await incrementLike()
          setLikes(updatedLikes)
        }}
      >
        Like
      </button>
    </>
  )
}
```

## Examples

### Showing a pending state

While executing a Server Function, you can show a loading indicator with React's [useActionState](https://react.dev/reference/react/useActionState) hook. This hook returns a `pending` boolean:

 app/ui/button.tsxJavaScriptTypeScript

```
'use client'

import { useActionState, startTransition } from 'react'
import { createPost } from '@/app/actions'
import { LoadingSpinner } from '@/app/ui/loading-spinner'

export function Button() {
  const [state, action, pending] = useActionState(createPost, false)

  return (
    <button onClick={() => startTransition(action)}>
      {pending ? <LoadingSpinner /> : 'Create Post'}
    </button>
  )
}
```

### Refreshing

After a mutation, you may want to refresh the current page to show the latest data. You can do this by calling [refresh](https://nextjs.org/docs/app/api-reference/functions/refresh) from `next/cache` in a Server Action:

 app/lib/actions.tsJavaScriptTypeScript

```
'use server'

import { refresh } from 'next/cache'

export async function updatePost(formData: FormData) {
  // Update data
  // ...

  refresh()
}
```

This refreshes the client router, ensuring the UI reflects the latest state. The `refresh()` function does not revalidate tagged data. To revalidate tagged data, use [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag) or [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) instead.

### Revalidating

After performing an update, you can revalidate the Next.js cache and show the updated data by calling [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) or [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) within the Server Function:

 app/lib/actions.tsJavaScriptTypeScript

```
import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  'use server'
  // Update data
  // ...

  revalidatePath('/posts')
}
```

### Redirecting

You may want to redirect the user to a different page after performing an update. You can do this by calling [redirect](https://nextjs.org/docs/app/api-reference/functions/redirect) within the Server Function.

 app/lib/actions.tsJavaScriptTypeScript

```
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  // Update data
  // ...

  revalidatePath('/posts')
  redirect('/posts')
}
```

Calling `redirect` [throws](https://nextjs.org/docs/app/api-reference/functions/redirect#behavior) a framework handled control-flow exception. Any code after it won't execute. If you need fresh data, call [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) or [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) beforehand.

### Cookies

You can `get`, `set`, and `delete` cookies inside a Server Action using the [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies) API.

When you [set or delete](https://nextjs.org/docs/app/api-reference/functions/cookies#understanding-cookie-behavior-in-server-functions) a cookie in a Server Action, Next.js re-renders the current page and its layouts on the server so the **UI reflects the new cookie value**.

> **Good to know**: The server update applies to the current React tree, re-rendering, mounting, or unmounting components, as needed. Client state is preserved for re-rendered components, and effects re-run if their dependencies changed.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { cookies } from 'next/headers'

export async function exampleAction() {
  const cookieStore = await cookies()

  // Get cookie
  cookieStore.get('name')?.value

  // Set cookie
  cookieStore.set('name', 'Delba')

  // Delete cookie
  cookieStore.delete('name')
}
```

### useEffect

You can use the React [useEffect](https://react.dev/reference/react/useEffect) hook to invoke a Server Action when the component mounts or a dependency changes. This is useful for mutations that depend on global events or need to be triggered automatically. For example, `onKeyDown` for app shortcuts, an intersection observer hook for infinite scrolling, or when the component mounts to update a view count:

 app/view-count.tsxJavaScriptTypeScript

```
'use client'

import { incrementViews } from './actions'
import { useState, useEffect, useTransition } from 'react'

export default function ViewCount({ initialViews }: { initialViews: number }) {
  const [views, setViews] = useState(initialViews)
  const [isPending, startTransition] = useTransition()

  useEffect(() => {
    startTransition(async () => {
      const updatedViews = await incrementViews()
      setViews(updatedViews)
    })
  }, [])

  // You can use `isPending` to give users feedback
  return <p>Total Views: {views}</p>
}
```

## API Reference

Learn more about the features mentioned in this page by reading the API Reference.[revalidatePathAPI Reference for the revalidatePath function.](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)[revalidateTagAPI Reference for the revalidateTag function.](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)[redirectAPI Reference for the redirect function.](https://nextjs.org/docs/app/api-reference/functions/redirect)

Was this helpful?

supported.

---

# Upgrading

> Learn how to upgrade your Next.js application to the latest version or canary.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Upgrading

# Upgrading

Last updated  November 18, 2025

## Latest version

To update to the latest version of Next.js, you can use the `upgrade` command:

 Terminal

```
next upgrade
```

Next.js 15 and earlier do not support the `upgrade` command and need to use a separate package instead:

 Terminal

```
npx @next/codemod@canary upgrade latest
```

If you prefer to upgrade manually, install the latest Next.js and React versions:

 Terminal

```
pnpm i next@latest react@latest react-dom@latest eslint-config-next@latest
```

## Canary version

To update to the latest canary, make sure you're on the latest version of Next.js and everything is working as expected. Then, run the following command:

 Terminal

```
npm i next@canary
```

### Features available in canary

The following features are currently available in canary:

**Authentication**:

- [forbidden](https://nextjs.org/docs/app/api-reference/functions/forbidden)
- [unauthorized](https://nextjs.org/docs/app/api-reference/functions/unauthorized)
- [forbidden.js](https://nextjs.org/docs/app/api-reference/file-conventions/forbidden)
- [unauthorized.js](https://nextjs.org/docs/app/api-reference/file-conventions/unauthorized)
- [authInterrupts](https://nextjs.org/docs/app/api-reference/config/next-config-js/authInterrupts)

## Version guides

See the version guides for in-depth upgrade instructions.[Version 16Upgrade your Next.js Application from Version 15 to 16.](https://nextjs.org/docs/app/guides/upgrading/version-16)[Version 15Upgrade your Next.js Application from Version 14 to 15.](https://nextjs.org/docs/app/guides/upgrading/version-15)[Version 14Upgrade your Next.js Application from Version 13 to 14.](https://nextjs.org/docs/app/guides/upgrading/version-14)

Was this helpful?

supported.

---

# Getting Started

> Learn how to create full-stack web applications with the Next.js App Router.

[Next.js Docs](https://nextjs.org/docs)[App Router](https://nextjs.org/docs/app)Getting Started

# Getting Started

Last updated  May 2, 2025

Welcome to the Next.js documentation!

This **Getting Started** section will help you create your first Next.js app and learn the core features you'll use in every project.

## Pre-requisite knowledge

Our documentation assumes some familiarity with web development. Before getting started, it'll help if you're comfortable with:

- HTML
- CSS
- JavaScript
- React

If you're new to React or need a refresher, we recommend starting with our [React Foundations course](https://nextjs.org/learn/react-foundations), and the [Next.js Foundations course](https://nextjs.org/learn/dashboard-app) that has you building an application as you learn.

## Next Steps

[InstallationLearn how to create a new Next.js application with the `create-next-app` CLI, and set up TypeScript, ESLint, and Module Path Aliases.](https://nextjs.org/docs/app/getting-started/installation)[Project StructureLearn the folder and file conventions in Next.js, and how to organize your project.](https://nextjs.org/docs/app/getting-started/project-structure)[Layouts and PagesLearn how to create your first pages and layouts, and link between them with the Link component.](https://nextjs.org/docs/app/getting-started/layouts-and-pages)[Linking and NavigatingLearn how the built-in navigation optimizations work, including prefetching, prerendering, and client-side navigation, and how to optimize navigation for dynamic routes and slow networks.](https://nextjs.org/docs/app/getting-started/linking-and-navigating)[Server and Client ComponentsLearn how you can use React Server and Client Components to render parts of your application on the server or the client.](https://nextjs.org/docs/app/getting-started/server-and-client-components)[Cache ComponentsLearn how to use Cache Components and combine the benefits of static and dynamic rendering.](https://nextjs.org/docs/app/getting-started/cache-components)[Fetching DataLearn how to fetch data and stream content that depends on data.](https://nextjs.org/docs/app/getting-started/fetching-data)[Updating DataLearn how to mutate data using Server Functions and Server Actions in Next.js.](https://nextjs.org/docs/app/getting-started/updating-data)[Caching and RevalidatingLearn how to cache and revalidate data in your application.](https://nextjs.org/docs/app/getting-started/caching-and-revalidating)[Error HandlingLearn how to display expected errors and handle uncaught exceptions.](https://nextjs.org/docs/app/getting-started/error-handling)[CSSLearn about the different ways to add CSS to your application, including Tailwind CSS, CSS Modules, Global CSS, and more.](https://nextjs.org/docs/app/getting-started/css)[Image OptimizationLearn how to optimize images in Next.js](https://nextjs.org/docs/app/getting-started/images)[Font OptimizationLearn how to optimize fonts in Next.js](https://nextjs.org/docs/app/getting-started/fonts)[Metadata and OG imagesLearn how to add metadata to your pages and create dynamic OG images.](https://nextjs.org/docs/app/getting-started/metadata-and-og-images)[Route HandlersLearn how to use Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers)[ProxyLearn how to use Proxy](https://nextjs.org/docs/app/getting-started/proxy)[DeployingLearn how to deploy your Next.js application.](https://nextjs.org/docs/app/getting-started/deploying)[UpgradingLearn how to upgrade your Next.js application to the latest version or canary.](https://nextjs.org/docs/app/getting-started/upgrading)

Was this helpful?

supported.

---

# Next.js Glossary

> A glossary of common terms used in Next.js.

[Next.js Docs](https://nextjs.org/docs)[App Router](https://nextjs.org/docs/app)Glossary

# Next.js Glossary

Last updated  January 26, 2026

# A

## App Router

The Next.js router introduced in version 13, built on top of React Server Components. It uses file-system based routing and supports layouts, nested routing, loading states, error handling, and more. Learn more in the [App Router documentation](https://nextjs.org/docs/app).

# B

## Build time

The stage when your application is being compiled. During build time, Next.js transforms your code into optimized files for production, generates static pages, and prepares assets for deployment. See the [next buildCLI reference](https://nextjs.org/docs/app/api-reference/cli/next#next-build-options).

# C

## Cache Components

A feature that enables component and function-level caching using the ["use cache"directive](https://nextjs.org/docs/app/api-reference/directives/use-cache). Cache Components allows you to mix static, cached, and dynamic content within a single route by prerendering a static HTML shell that's served immediately, while dynamic content streams in when ready. Configure cache duration with [cacheLife()](https://nextjs.org/docs/app/api-reference/functions/cacheLife), tag cached data with [cacheTag()](https://nextjs.org/docs/app/api-reference/functions/cacheTag), and invalidate on-demand with [updateTag()](https://nextjs.org/docs/app/api-reference/functions/updateTag). Learn more in the [Cache Components guide](https://nextjs.org/docs/app/getting-started/cache-components).

## Catch-all Segments

Dynamic route segments that can match multiple URL parts using the `[...folder]/page.js` syntax. These segments capture all remaining URL segments and are useful for implementing features like documentation sites or file browsers. Learn more in [Dynamic Route Segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#catch-all-segments).

## Client Bundles

JavaScript bundles sent to the browser. Next.js splits these automatically based on the [module graph](#module-graph) to reduce initial payload size and load only the necessary code for each page.

## Client Component

A React component that runs in the browser. In Next.js, Client Components can also be rendered on the server during initial page generation. They can use state, effects, event handlers, and browser APIs, and are marked with the ["use client"directive](#use-client-directive) at the top of a file. Learn more in [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components).

## Client-side navigation

A navigation technique where the page content updates dynamically without a full page reload. Next.js uses client-side navigation with the [<Link>component](https://nextjs.org/docs/app/api-reference/components/link), keeping shared layouts interactive and preserving browser state. Learn more in [Linking and Navigating](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions).

## Code Splitting

The process of dividing your application into smaller JavaScript chunks based on routes. Instead of loading all code upfront, only the code needed for the current route is loaded, reducing initial load time. Next.js automatically performs code splitting based on routes. Learn more in the [Package Bundling guide](https://nextjs.org/docs/app/guides/package-bundling).

# D

## Dynamic rendering

See [Request-time rendering](#request-time-rendering).

## Dynamic route segments

[Route segments](#route-segment) that are generated from data at request time. Created by wrapping a folder name in square brackets (e.g., `[slug]`), they allow you to create routes from dynamic data like blog posts or product pages. Learn more in [Dynamic Route Segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes).

# E

## Environment Variables

Configuration values accessible at build time or request time. In Next.js, variables prefixed with `NEXT_PUBLIC_` are exposed to the browser, while others are only available server-side. Learn more in [Environment Variables](https://nextjs.org/docs/app/guides/environment-variables).

## Error Boundary

A React component that catches JavaScript errors in its child component tree and displays a fallback UI. In Next.js, create an [error.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/error) to automatically wrap a route segment in an error boundary. Learn more in [Error Handling](https://nextjs.org/docs/app/getting-started/error-handling).

# F

## Font Optimization

Automatic font optimization using [next/font](https://nextjs.org/docs/app/api-reference/components/font). Next.js self-hosts fonts, eliminates layout shift, and applies best practices for performance. Works with Google Fonts and local font files. Learn more in [Fonts](https://nextjs.org/docs/app/getting-started/fonts).

## File-system caching

A Turbopack feature that stores compiler artifacts on disk between runs, reducing work across `next dev` or `next build` commands for significantly faster compile times. Learn more in [Turbopack FileSystem Caching](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache).

# H

## Hydration

React's process of attaching event handlers to the DOM to make server-rendered static HTML interactive. During hydration, React reconciles the server-rendered markup with the client-side JavaScript. Learn more in [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components#how-do-server-and-client-components-work-in-nextjs).

# I

## Import Aliases

Custom path mappings that provide shorthand references for frequently used directories. Import aliases reduce the complexity of relative imports and make code more readable and maintainable. Learn more in [Absolute Imports and Module Path Aliases](https://nextjs.org/docs/app/getting-started/installation#set-up-absolute-imports-and-module-path-aliases).

## Incremental Static Regeneration (ISR)

A technique that allows you to update static content without rebuilding the entire site. ISR enables you to use static generation on a per-page basis while revalidating pages in the background as traffic comes in. Learn more in the [ISR guide](https://nextjs.org/docs/app/guides/incremental-static-regeneration).

> **Good to know**: In Next.js, ISR is also known as [Revalidation](#revalidation).

## Intercepting Routes

A routing pattern that allows loading a route from another part of your application within the current layout. Useful for displaying content (like modals) without the user switching context, while keeping the URL shareable. Learn more in [Intercepting Routes](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes).

## Image Optimization

Automatic image optimization using the [<Image>component](https://nextjs.org/docs/app/api-reference/components/image). Next.js optimizes images on-demand, serves them in modern formats like WebP, and automatically handles lazy loading and responsive sizing. Learn more in [Images](https://nextjs.org/docs/app/getting-started/images).

# L

## Layout

UI that is shared between multiple pages. Layouts preserve state, remain interactive, and do not re-render on navigation. Defined by exporting a React component from a [layout.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/layout). Learn more in [Layouts and Pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages).

## Loading UI

Fallback UI shown while a [route segment](#route-segment) is loading. Created by adding a [loading.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/loading) to a folder, which automatically wraps the page in a [Suspense boundary](#suspense-boundary). Learn more in [Loading UI](https://nextjs.org/docs/app/api-reference/file-conventions/loading).

# M

## Module Graph

A graph of file dependencies in your app. Each file (module) is a node, and import/export relationships form the edges. Next.js analyzes this graph to determine optimal bundling and code-splitting strategies. Learn more in [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components#reducing-js-bundle-size).

## Metadata

Information about a page used by browsers and search engines, such as title, description, and Open Graph images. In Next.js, define metadata using the [metadataexport](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) or [generateMetadatafunction](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) in layout or page files. Learn more in [Metadata and OG Images](https://nextjs.org/docs/app/getting-started/metadata-and-og-images).

## Memoization

Caching the return value of a function so that calling the same function multiple times during a render pass (request) only executes it once. In Next.js, fetch requests with the same URL and options are automatically memoized. Learn more about [React Cache](https://react.dev/reference/react/cache).

## Middleware

See [Proxy](#proxy).

# N

## Not Found

A special component shown when a route doesn't exist or when the [notFound()function](https://nextjs.org/docs/app/api-reference/functions/not-found) is called. Created by adding a [not-found.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/not-found) to your app directory. Learn more in [Error Handling](https://nextjs.org/docs/app/getting-started/error-handling#not-found).

# P

## Private Folders

Folders prefixed with an underscore (e.g., `_components`) that are excluded from the routing system. These folders are used for code organization and shared utilities without creating accessible routes. Learn more in [Private Folders](https://nextjs.org/docs/app/getting-started/project-structure#private-folders).

## Page

UI that is unique to a route. Defined by exporting a React component from a [page.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/page) within the `app` directory. Learn more in [Layouts and Pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages).

## Parallel Routes

A pattern that allows simultaneously or conditionally rendering multiple pages within the same layout. Created using named slots with the `@folder` convention, useful for dashboards, modals, and complex layouts. Learn more in [Parallel Routes](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes).

## Partial Prerendering (PPR)

A rendering optimization that combines static and dynamic rendering in a single route. The static shell is served immediately while dynamic content streams in when ready, providing the best of both rendering strategies. Learn more in [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components).

## Prefetching

Loading a route in the background before the user navigates to it. Next.js automatically prefetches routes linked with the [<Link>component](https://nextjs.org/docs/app/api-reference/components/link) when they enter the viewport, making navigation feel instant. Learn more in the [Prefetching guide](https://nextjs.org/docs/app/guides/prefetching).

## Prerendering

When a component is rendered at [build time](#build-time) or in the background during [revalidation](#revalidation). The result is HTML and [RSC Payload](#rsc-payload), which can be cached and served from a CDN. Prerendering is the default for components that don't use [Request-time APIs](#request-time-apis).

## Proxy

A file ([proxy.js](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)) that runs code on the server before request is completed. Used to implement server-side logic like logging, redirects, and rewrites. Formerly known as Middleware. Learn more in the [Proxy guide](https://nextjs.org/docs/app/getting-started/proxy).

# R

## Redirect

Sending users from one URL to another. In Next.js, redirects can be configured in [next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects), returned from [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy), or triggered programmatically with the [redirect()function](https://nextjs.org/docs/app/api-reference/functions/redirect). Learn more in [Redirecting](https://nextjs.org/docs/app/guides/redirecting).

## Request time

The time when a user makes a request to your application. At request time, dynamic routes are rendered, cookies and headers are accessible, and request-specific data can be used.

## Request-time APIs

Functions that access request-specific data, causing a component to opt into [request-time rendering](#request-time-rendering). These include:

- [cookies()](https://nextjs.org/docs/app/api-reference/functions/cookies) - Access request cookies
- [headers()](https://nextjs.org/docs/app/api-reference/functions/headers) - Access request headers
- [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) - Access URL query parameters
- [draftMode()](https://nextjs.org/docs/app/api-reference/functions/draft-mode) - Enable or check draft mode

## Request-time rendering

When a component is rendered at [request time](#request-time) rather than [build time](#build-time). A component becomes dynamic when it uses [Request-time APIs](#request-time-apis).

## Revalidation

The process of updating cached data. Can be time-based (using [cacheLife()](https://nextjs.org/docs/app/api-reference/functions/cacheLife) to set cache duration) or on-demand (using [cacheTag()](https://nextjs.org/docs/app/api-reference/functions/cacheTag) to tag data, then [updateTag()](https://nextjs.org/docs/app/api-reference/functions/updateTag) to invalidate). Learn more in [Caching and Revalidating](https://nextjs.org/docs/app/getting-started/caching-and-revalidating).

## Rewrite

Mapping an incoming request path to a different destination path without changing the URL in the browser. Configured in [next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites) or returned from [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy). Useful for proxying to external services or legacy URLs.

## Route Groups

A way to organize routes without affecting the URL structure. Created by wrapping a folder name in parentheses (e.g., `(marketing)`), route groups help organize related routes and enable per-group [layouts](#layout). Learn more in [Route Groups](https://nextjs.org/docs/app/api-reference/file-conventions/route-groups).

## Route Handler

A function that handles HTTP requests for a specific route, defined in a [route.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/route). Route Handlers use the Web Request and Response APIs and can handle `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, and `OPTIONS` methods. Learn more in [Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers).

## Route Segment

A part of the URL path (between two slashes) defined by a folder in the `app` directory. Each folder represents a segment in the URL structure. Learn more in [Project Structure](https://nextjs.org/docs/app/getting-started/project-structure).

## RSC Payload

The React Server Component Payload—a compact binary representation of the rendered React Server Components tree. Contains the rendered result of Server Components, placeholders for Client Components, and props passed between them. Learn more in [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components#how-do-server-and-client-components-work-in-nextjs).

# S

## Server Component

The default component type in the App Router. Server Components render on the server, can fetch data directly, and don't add to the client JavaScript bundle. They cannot use state or browser APIs. Learn more in [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components).

## Server Action

A [Server Function](#server-function) that is passed to a Client Component as a prop or bound to a form action. Server Actions are commonly used for form submissions and data mutations. Learn more in [Server Actions and Mutations](https://nextjs.org/docs/app/getting-started/updating-data).

## Server Function

An asynchronous function that runs on the server, marked with the ["use server"directive](https://nextjs.org/docs/app/api-reference/directives/use-server). Server Functions can be invoked from Client Components. When passed as a prop to a Client Component or bound to a form action, they are called [Server Actions](#server-action). Learn more in [React Server Functions](https://react.dev/reference/rsc/server-functions).

## Static Export

A deployment mode that generates a fully static site with HTML, CSS, and JavaScript files. Enabled by setting `output: 'export'` in `next.config.js`. Static exports can be hosted on any static file server without a Node.js server. Learn more in [Static Exports](https://nextjs.org/docs/app/guides/static-exports).

## Static rendering

See [Prerendering](#prerendering).

## Static Assets

Files such as images, fonts, videos, and other media that are served directly without processing. Static assets are typically stored in the `public` directory and referenced by their relative paths. Learn more in [Static Assets](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder).

## Static Shell

The prerendered HTML structure of a page that's served immediately to the browser. With [Partial Prerendering](#partial-prerendering-ppr), the static shell includes all statically renderable content plus [Suspense boundary](#suspense-boundary) fallbacks for dynamic content that streams in later.

## Streaming

A technique that allows the server to send parts of a page to the client as they become ready, rather than waiting for the entire page to render. Enabled automatically with [loading.js](https://nextjs.org/docs/app/api-reference/file-conventions/loading) or manual `<Suspense>` boundaries. Learn more in [Linking and Navigating - Streaming](https://nextjs.org/docs/app/getting-started/linking-and-navigating#streaming).

## Suspense boundary

A React [<Suspense>](https://react.dev/reference/react/Suspense) component that wraps async content and displays fallback UI while it loads. In Next.js, Suspense boundaries define where the [static shell](#static-shell) ends and [streaming](#streaming) begins, enabling [Partial Prerendering](#partial-prerendering-ppr).

# T

## Turbopack

A fast, Rust-based bundler built for Next.js. Turbopack is the default bundler for `next dev` and available for `next build`. It provides significantly faster compilation times compared to Webpack. Learn more in [Turbopack](https://nextjs.org/docs/app/api-reference/turbopack).

## Tree Shaking

The process of removing unused code from your JavaScript bundles during the build process. Next.js automatically tree-shakes your code to reduce bundle sizes. Learn more in the [Package Bundling guide](https://nextjs.org/docs/app/guides/package-bundling).

# U

## "use cache"Directive

A directive that marks a component or function as cacheable. It can be placed at the top of a file to indicate that all exports in the file are cacheable, or inline at the top of a function or component to mark that specific scope as cacheable. Learn more in the ["use cache"reference](https://nextjs.org/docs/app/api-reference/directives/use-cache).

## "use client"Directive

A special React directive that marks the boundary between server and client code. It must be placed at the top of a file, before any imports or other code. It indicates that React Components, helper functions, variable declarations, and all imported dependencies should be included in the [client bundle](#client-bundles). Learn more in the ["use client"reference](https://nextjs.org/docs/app/api-reference/directives/use-client).

## "use server"Directive

A directive that marks a function as a [Server Function](#server-function) that can be called from client-side code. It can be placed at the top of a file to indicate that all exports in the file are Server Functions, or inline at the top of a function to mark that specific function. Learn more in the ["use server"reference](https://nextjs.org/docs/app/api-reference/directives/use-server).

Was this helpful?

supported.

---

# How to add analytics to your Next.js application

> Measure and track page performance using Next.js Speed Insights

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Analytics

# How to add analytics to your Next.js application

Last updated  May 13, 2025

Next.js has built-in support for measuring and reporting performance metrics. You can either use the [useReportWebVitals](https://nextjs.org/docs/app/api-reference/functions/use-report-web-vitals) hook to manage reporting yourself, or alternatively, Vercel provides a [managed service](https://vercel.com/analytics?utm_source=next-site&utm_medium=docs&utm_campaign=next-website) to automatically collect and visualize metrics for you.

## Client Instrumentation

For more advanced analytics and monitoring needs, Next.js provides a `instrumentation-client.js|ts` file that runs before your application's frontend code starts executing. This is ideal for setting up global analytics, error tracking, or performance monitoring tools.

To use it, create an `instrumentation-client.js` or `instrumentation-client.ts` file in your application's root directory:

 instrumentation-client.js

```
// Initialize analytics before the app starts
console.log('Analytics initialized')

// Set up global error tracking
window.addEventListener('error', (event) => {
  // Send to your error tracking service
  reportError(event.error)
})
```

## Build Your Own

   app/_components/web-vitals.js

```
'use client'

import { useReportWebVitals } from 'next/web-vitals'

export function WebVitals() {
  useReportWebVitals((metric) => {
    console.log(metric)
  })
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

View the [API Reference](https://nextjs.org/docs/app/api-reference/functions/use-report-web-vitals) for more information.

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

   app/_components/web-vitals.tsxJavaScriptTypeScript

```
'use client'

import { useReportWebVitals } from 'next/web-vitals'

export function WebVitals() {
  useReportWebVitals((metric) => {
    switch (metric.name) {
      case 'FCP': {
        // handle FCP results
      }
      case 'LCP': {
        // handle LCP results
      }
      // ...
    }
  })
}
```

## Sending results to external systems

You can send results to any endpoint to measure and track
real user performance on your site. For example:

```
useReportWebVitals((metric) => {
  const body = JSON.stringify(metric)
  const url = 'https://example.com/analytics'

  // Use `navigator.sendBeacon()` if available, falling back to `fetch()`.
  if (navigator.sendBeacon) {
    navigator.sendBeacon(url, body)
  } else {
    fetch(url, { body, method: 'POST', keepalive: true })
  }
})
```

> **Good to know**: If you use [Google Analytics](https://analytics.google.com/analytics/web/), using the
> `id` value can allow you to construct metric distributions manually (to calculate percentiles,
> etc.)

> ```
> useReportWebVitals((metric) => {
>   // Use `window.gtag` if you initialized Google Analytics as this example:
>   // https://github.com/vercel/next.js/blob/canary/examples/with-google-analytics
>   window.gtag('event', metric.name, {
>     value: Math.round(
>       metric.name === 'CLS' ? metric.value * 1000 : metric.value
>     ), // values must be integers
>     event_label: metric.id, // id unique to current page load
>     non_interaction: true, // avoids affecting bounce rate.
>   })
> })
> ```
>
>
>
> Read more about [sending results to Google Analytics](https://github.com/GoogleChrome/web-vitals#send-the-results-to-google-analytics).

Was this helpful?

supported.
