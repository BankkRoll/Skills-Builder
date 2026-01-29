# Error Handling and more

# Error Handling

> Learn how to display expected errors and handle uncaught exceptions.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Error Handling

# Error Handling

Last updated  June 26, 2025

Errors can be divided into two categories: [expected errors](#handling-expected-errors) and [uncaught exceptions](#handling-uncaught-exceptions). This page will walk you through how you can handle these errors in your Next.js application.

## Handling expected errors

Expected errors are those that can occur during the normal operation of the application, such as those from [server-side form validation](https://nextjs.org/docs/app/guides/forms) or failed requests. These errors should be handled explicitly and returned to the client.

### Server Functions

You can use the [useActionState](https://react.dev/reference/react/useActionState) hook to handle expected errors in [Server Functions](https://react.dev/reference/rsc/server-functions).

For these errors, avoid using `try`/`catch` blocks and throw errors. Instead, model expected errors as return values.

 app/actions.tsJavaScriptTypeScript

```
'use server'

export async function createPost(prevState: any, formData: FormData) {
  const title = formData.get('title')
  const content = formData.get('content')

  const res = await fetch('https://api.vercel.app/posts', {
    method: 'POST',
    body: { title, content },
  })
  const json = await res.json()

  if (!res.ok) {
    return { message: 'Failed to create post' }
  }
}
```

You can pass your action to the `useActionState` hook and use the returned `state` to display an error message.

 app/ui/form.tsxJavaScriptTypeScript

```
'use client'

import { useActionState } from 'react'
import { createPost } from '@/app/actions'

const initialState = {
  message: '',
}

export function Form() {
  const [state, formAction, pending] = useActionState(createPost, initialState)

  return (
    <form action={formAction}>
      <label htmlFor="title">Title</label>
      <input type="text" id="title" name="title" required />
      <label htmlFor="content">Content</label>
      <textarea id="content" name="content" required />
      {state?.message && <p aria-live="polite">{state.message}</p>}
      <button disabled={pending}>Create Post</button>
    </form>
  )
}
```

### Server Components

When fetching data inside of a Server Component, you can use the response to conditionally render an error message or [redirect](https://nextjs.org/docs/app/api-reference/functions/redirect).

 app/page.tsxJavaScriptTypeScript

```
export default async function Page() {
  const res = await fetch(`https://...`)
  const data = await res.json()

  if (!res.ok) {
    return 'There was an error.'
  }

  return '...'
}
```

### Not found

You can call the [notFound](https://nextjs.org/docs/app/api-reference/functions/not-found) function within a route segment and use the [not-found.js](https://nextjs.org/docs/app/api-reference/file-conventions/not-found) file to show a 404 UI.

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
import { getPostBySlug } from '@/lib/posts'

export default async function Page({ params }: { params: { slug: string } }) {
  const { slug } = await params
  const post = getPostBySlug(slug)

  if (!post) {
    notFound()
  }

  return <div>{post.title}</div>
}
```

   app/blog/[slug]/not-found.tsxJavaScriptTypeScript

```
export default function NotFound() {
  return <div>404 - Page Not Found</div>
}
```

## Handling uncaught exceptions

Uncaught exceptions are unexpected errors that indicate bugs or issues that should not occur during the normal flow of your application. These should be handled by throwing errors, which will then be caught by error boundaries.

### Nested error boundaries

Next.js uses error boundaries to handle uncaught exceptions. Error boundaries catch errors in their child components and display a fallback UI instead of the component tree that crashed.

Create an error boundary by adding an [error.js](https://nextjs.org/docs/app/api-reference/file-conventions/error) file inside a route segment and exporting a React component:

 app/dashboard/error.tsxJavaScriptTypeScript

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

Errors will bubble up to the nearest parent error boundary. This allows for granular error handling by placing `error.tsx` files at different levels in the [route hierarchy](https://nextjs.org/docs/app/getting-started/project-structure#component-hierarchy).

 ![Nested Error Component Hierarchy](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fnested-error-component-hierarchy.png&w=3840&q=75)![Nested Error Component Hierarchy](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fnested-error-component-hierarchy.png&w=3840&q=75)

Error boundaries don’t catch errors inside event handlers. They’re designed to catch errors [during rendering](https://react.dev/reference/react/Component#static-getderivedstatefromerror) to show a **fallback UI** instead of crashing the whole app.

In general, errors in event handlers or async code aren’t handled by error boundaries because they run after rendering.

To handle these cases, catch the error manually and store it using `useState` or `useReducer`, then update the UI to inform the user.

```
'use client'

import { useState } from 'react'

export function Button() {
  const [error, setError] = useState(null)

  const handleClick = () => {
    try {
      // do some work that might fail
      throw new Error('Exception')
    } catch (reason) {
      setError(reason)
    }
  }

  if (error) {
    /* render fallback UI */
  }

  return (
    <button type="button" onClick={handleClick}>
      Click me
    </button>
  )
}
```

Note that unhandled errors inside `startTransition` from `useTransition`, will bubble up to the nearest error boundary.

```
'use client'

import { useTransition } from 'react'

export function Button() {
  const [pending, startTransition] = useTransition()

  const handleClick = () =>
    startTransition(() => {
      throw new Error('Exception')
    })

  return (
    <button type="button" onClick={handleClick}>
      Click me
    </button>
  )
}
```

### Global errors

While less common, you can handle errors in the root layout using the [global-error.js](https://nextjs.org/docs/app/api-reference/file-conventions/error#global-error) file, located in the root app directory, even when leveraging [internationalization](https://nextjs.org/docs/app/guides/internationalization). Global error UI must define its own `<html>` and `<body>` tags, since it is replacing the root layout or template when active.

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

## API Reference

Learn more about the features mentioned in this page by reading the API Reference.[redirectAPI Reference for the redirect function.](https://nextjs.org/docs/app/api-reference/functions/redirect)[error.jsAPI reference for the error.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/error)[notFoundAPI Reference for the notFound function.](https://nextjs.org/docs/app/api-reference/functions/not-found)[not-found.jsAPI reference for the not-found.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/not-found)

Was this helpful?

supported.

---

# Fetching Data

> Learn how to fetch data and stream content that depends on data.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Fetching Data

# Fetching Data

Last updated  December 3, 2025

This page will walk you through how you can fetch data in [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), and how to [stream](#streaming) components that depend on data.

## Fetching data

### Server Components

You can fetch data in Server Components using any asynchronous I/O, such as:

1. The [fetchAPI](#with-the-fetch-api)
2. An [ORM or database](#with-an-orm-or-database)
3. Reading from the filesystem using Node.js APIs like `fs`

#### With thefetchAPI

To fetch data with the `fetch` API, turn your component into an asynchronous function, and await the `fetch` call. For example:

 app/blog/page.tsxJavaScriptTypeScript

```
export default async function Page() {
  const data = await fetch('https://api.vercel.app/blog')
  const posts = await data.json()
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

> **Good to know:**
>
>
>
> - `fetch` responses are not cached by default. However, Next.js will [pre-render](https://nextjs.org/docs/app/guides/caching#static-rendering) the route and the output will be cached for improved performance. If you'd like to opt into [dynamic rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering), use the `{ cache: 'no-store' }` option. See the [fetchAPI Reference](https://nextjs.org/docs/app/api-reference/functions/fetch).
> - During development, you can log `fetch` calls for better visibility and debugging. See the [loggingAPI reference](https://nextjs.org/docs/app/api-reference/config/next-config-js/logging).

#### With an ORM or database

Since Server Components are rendered on the server, you can safely make database queries using an ORM or database client. Turn your component into an asynchronous function, and await the call:

 app/blog/page.tsxJavaScriptTypeScript

```
import { db, posts } from '@/lib/db'

export default async function Page() {
  const allPosts = await db.select().from(posts)
  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### Client Components

There are two ways to fetch data in Client Components, using:

1. React's [usehook](https://react.dev/reference/react/use)
2. A community library like [SWR](https://swr.vercel.app/) or [React Query](https://tanstack.com/query/latest)

#### Streaming data with theusehook

You can use React's [usehook](https://react.dev/reference/react/use) to [stream](#streaming) data from the server to client. Start by fetching data in your Server component, and pass the promise to your Client Component as prop:

 app/blog/page.tsxJavaScriptTypeScript

```
import Posts from '@/app/ui/posts'
import { Suspense } from 'react'

export default function Page() {
  // Don't await the data fetching function
  const posts = getPosts()

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Posts posts={posts} />
    </Suspense>
  )
}
```

Then, in your Client Component, use the `use` hook to read the promise:

 app/ui/posts.tsxJavaScriptTypeScript

```
'use client'
import { use } from 'react'

export default function Posts({
  posts,
}: {
  posts: Promise<{ id: string; title: string }[]>
}) {
  const allPosts = use(posts)

  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

In the example above, the `<Posts>` component is wrapped in a [<Suspense>boundary](https://react.dev/reference/react/Suspense). This means the fallback will be shown while the promise is being resolved. Learn more about [streaming](#streaming).

#### Community libraries

You can use a community library like [SWR](https://swr.vercel.app/) or [React Query](https://tanstack.com/query/latest) to fetch data in Client Components. These libraries have their own semantics for caching, streaming, and other features. For example, with SWR:

 app/blog/page.tsxJavaScriptTypeScript

```
'use client'
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((r) => r.json())

export default function BlogPage() {
  const { data, error, isLoading } = useSWR(
    'https://api.vercel.app/blog',
    fetcher
  )

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data.map((post: { id: string; title: string }) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

## Deduplicate requests and cache data

One way to deduplicate `fetch` requests is with [request memoization](https://nextjs.org/docs/app/guides/caching#request-memoization). With this mechanism, `fetch` calls using `GET` or `HEAD` with the same URL and options in a single render pass are combined into one request. This happens automatically, and you can [opt out](https://nextjs.org/docs/app/guides/caching#opting-out) by passing an Abort signal to `fetch`.

Request memoization is scoped to the lifetime of a request.

You can also deduplicate `fetch` requests by using Next.js’ [Data Cache](https://nextjs.org/docs/app/guides/caching#data-cache), for example by setting `cache: 'force-cache'` in your `fetch` options.

Data Cache allows sharing data across the current render pass and incoming requests.

If you are *not* using `fetch`, and instead using an ORM or database directly, you can wrap your data access with the [Reactcache](https://react.dev/reference/react/cache) function.

 app/lib/data.tsJavaScriptTypeScript

```
import { cache } from 'react'
import { db, posts, eq } from '@/lib/db'

export const getPost = cache(async (id: string) => {
  const post = await db.query.posts.findFirst({
    where: eq(posts.id, parseInt(id)),
  })
})
```

## Streaming

> **Warning:** The content below assumes the [cacheComponentsconfig option](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) is enabled in your application. The flag was introduced in Next.js 15 canary.

When you fetch data in Server Components, the data is fetched and rendered on the server for each request. If you have any slow data requests, the whole route will be blocked from rendering until all the data is fetched.

To improve the initial load time and user experience, you can use streaming to break up the page's HTML into smaller chunks and progressively send those chunks from the server to the client.

 ![How Server Rendering with Streaming Works](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fserver-rendering-with-streaming.png&w=3840&q=75)![How Server Rendering with Streaming Works](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fserver-rendering-with-streaming.png&w=3840&q=75)

There are two ways you can leverage streaming in your application:

1. Wrapping a page with a [loading.jsfile](#with-loadingjs)
2. Wrapping a component with [<Suspense>](#with-suspense)

### Withloading.js

You can create a `loading.js` file in the same folder as your page to stream the **entire page** while the data is being fetched. For example, to stream `app/blog/page.js`, add the file inside the `app/blog` folder.

 ![Blog folder structure with loading.js file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Floading-file.png&w=3840&q=75)![Blog folder structure with loading.js file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Floading-file.png&w=3840&q=75) app/blog/loading.tsxJavaScriptTypeScript

```
export default function Loading() {
  // Define the Loading UI here
  return <div>Loading...</div>
}
```

On navigation, the user will immediately see the layout and a [loading state](#creating-meaningful-loading-states) while the page is being rendered. The new content will then be automatically swapped in once rendering is complete.

 ![Loading UI](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Floading-ui.png&w=3840&q=75)![Loading UI](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Floading-ui.png&w=3840&q=75)

Behind-the-scenes, `loading.js` will be nested inside `layout.js`, and will automatically wrap the `page.js` file and any children below in a `<Suspense>` boundary.

 ![loading.js overview](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Floading-overview.png&w=3840&q=75)![loading.js overview](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Floading-overview.png&w=3840&q=75)

This approach works well for route segments (layouts and pages), but for more granular streaming, you can use `<Suspense>`.

### With<Suspense>

`<Suspense>` allows you to be more granular about what parts of the page to stream. For example, you can immediately show any page content that falls outside of the `<Suspense>` boundary, and stream in the list of blog posts inside the boundary.

 app/blog/page.tsxJavaScriptTypeScript

```
import { Suspense } from 'react'
import BlogList from '@/components/BlogList'
import BlogListSkeleton from '@/components/BlogListSkeleton'

export default function BlogPage() {
  return (
    <div>
      {/* This content will be sent to the client immediately */}
      <header>
        <h1>Welcome to the Blog</h1>
        <p>Read the latest posts below.</p>
      </header>
      <main>
        {/* If there's any dynamic content inside this boundary, it will be streamed in */}
        <Suspense fallback={<BlogListSkeleton />}>
          <BlogList />
        </Suspense>
      </main>
    </div>
  )
}
```

### Creating meaningful loading states

An instant loading state is fallback UI that is shown immediately to the user after navigation. For the best user experience, we recommend designing loading states that are meaningful and help users understand the app is responding. For example, you can use skeletons and spinners, or a small but meaningful part of future screens such as a cover photo, title, etc.

In development, you can preview and inspect the loading state of your components using the [React Devtools](https://react.dev/learn/react-developer-tools).

## Examples

### Sequential data fetching

Sequential data fetching happens when one request depends on data from another.

For example, `<Playlists>` can only fetch data after `<Artist>` completes because it needs the `artistID`:

 app/artist/[username]/page.tsxJavaScriptTypeScript

```
export default async function Page({
  params,
}: {
  params: Promise<{ username: string }>
}) {
  const { username } = await params
  // Get artist information
  const artist = await getArtist(username)

  return (
    <>
      <h1>{artist.name}</h1>
      {/* Show fallback UI while the Playlists component is loading */}
      <Suspense fallback={<div>Loading...</div>}>
        {/* Pass the artist ID to the Playlists component */}
        <Playlists artistID={artist.id} />
      </Suspense>
    </>
  )
}

async function Playlists({ artistID }: { artistID: string }) {
  // Use the artist ID to fetch playlists
  const playlists = await getArtistPlaylists(artistID)

  return (
    <ul>
      {playlists.map((playlist) => (
        <li key={playlist.id}>{playlist.name}</li>
      ))}
    </ul>
  )
}
```

In this example, `<Suspense>` allows the playlists to stream in after the artist data loads. However, the page still waits for the artist data before displaying anything. To prevent this, you can wrap the entire page component in a `<Suspense>` boundary (for example, using a [loading.jsfile](#with-loadingjs)) to show a loading state immediately.

Ensure your data source can resolve the first request quickly, as it blocks everything else. If you can't optimize the request further, consider [caching](#deduplicate-requests-and-cache-data) the result if the data changes infrequently.

### Parallel data fetching

Parallel data fetching happens when data requests in a route are eagerly initiated and start at the same time.

By default, [layouts and pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages) are rendered in parallel. So each segment starts fetching data as soon as possible.

However, within *any* component, multiple `async`/`await` requests can still be sequential if placed after the other. For example, `getAlbums` will be blocked until `getArtist` is resolved:

 app/artist/[username]/page.tsxJavaScriptTypeScript

```
import { getArtist, getAlbums } from '@/app/lib/data'

export default async function Page({ params }) {
  // These requests will be sequential
  const { username } = await params
  const artist = await getArtist(username)
  const albums = await getAlbums(username)
  return <div>{artist.name}</div>
}
```

Start multiple requests by calling `fetch`, then await them with [Promise.all](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all). Requests begin as soon as `fetch` is called.

 app/artist/[username]/page.tsxJavaScriptTypeScript

```
import Albums from './albums'

async function getArtist(username: string) {
  const res = await fetch(`https://api.example.com/artist/${username}`)
  return res.json()
}

async function getAlbums(username: string) {
  const res = await fetch(`https://api.example.com/artist/${username}/albums`)
  return res.json()
}

export default async function Page({
  params,
}: {
  params: Promise<{ username: string }>
}) {
  const { username } = await params

  // Initiate requests
  const artistData = getArtist(username)
  const albumsData = getAlbums(username)

  const [artist, albums] = await Promise.all([artistData, albumsData])

  return (
    <>
      <h1>{artist.name}</h1>
      <Albums list={albums} />
    </>
  )
}
```

> **Good to know:** If one request fails when using `Promise.all`, the entire operation will fail. To handle this, you can use the [Promise.allSettled](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled) method instead.

### Preloading data

You can preload data by creating a utility function that you eagerly call above blocking requests. `<Item>` conditionally renders based on the `checkIsAvailable()` function.

You can call `preload()` before `checkIsAvailable()` to eagerly initiate `<Item/>` data dependencies. By the time `<Item/>` is rendered, its data has already been fetched.

 app/item/[id]/page.tsxJavaScriptTypeScript

```
import { getItem, checkIsAvailable } from '@/lib/data'

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  // starting loading item data
  preload(id)
  // perform another asynchronous task
  const isAvailable = await checkIsAvailable()

  return isAvailable ? <Item id={id} /> : null
}

const preload = (id: string) => {
  // void evaluates the given expression and returns undefined
  // https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/void
  void getItem(id)
}

export async function Item({ id }: { id: string }) {
  const result = await getItem(id)
  // ...
}
```

Additionally, you can use React's [cachefunction](https://react.dev/reference/react/cache) and the [server-onlypackage](https://www.npmjs.com/package/server-only) to create a reusable utility function. This approach allows you to cache the data fetching function and ensure that it's only executed on the server.

 utils/get-item.tsJavaScriptTypeScript

```
import { cache } from 'react'
import 'server-only'
import { getItem } from '@/lib/data'

export const preload = (id: string) => {
  void getItem(id)
}

export const getItem = cache(async (id: string) => {
  // ...
})
```

## API Reference

Learn more about the features mentioned in this page by reading the API Reference.[Data SecurityLearn the built-in data security features in Next.js and learn best practices for protecting your application's data.](https://nextjs.org/docs/app/guides/data-security)[fetchAPI reference for the extended fetch function.](https://nextjs.org/docs/app/api-reference/functions/fetch)[loading.jsAPI reference for the loading.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/loading)[loggingConfigure how data fetches are logged to the console when running Next.js in development mode.](https://nextjs.org/docs/app/api-reference/config/next-config-js/logging)[taintEnable tainting Objects and Values.](https://nextjs.org/docs/app/api-reference/config/next-config-js/taint)

Was this helpful?

supported.

---

# Font Optimization

> Learn how to optimize fonts in Next.js

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Font Optimization

# Font Optimization

Last updated  January 15, 2026

The [next/font](https://nextjs.org/docs/app/api-reference/components/font) module automatically optimizes your fonts and removes external network requests for improved privacy and performance.

It includes **built-in self-hosting** for any font file. This means you can optimally load web fonts with no layout shift.

To start using `next/font`, import it from [next/font/local](#local-fonts) or [next/font/google](#google-fonts), call it as a function with the appropriate options, and set the `className` of the element you want to apply the font to. For example:

app/layout.tsxJavaScriptTypeScript

```
import { Geist } from 'next/font/google'

const geist = Geist({
  subsets: ['latin'],
})

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={geist.className}>
      <body>{children}</body>
    </html>
  )
}
```

Fonts are scoped to the component they're used in. To apply a font to your entire application, add it to the [Root Layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout).

## Google fonts

You can automatically self-host any Google Font. Fonts are included stored as static assets and served from the same domain as your deployment, meaning no requests are sent to Google by the browser when the user visits your site.

To start using a Google Font, import your chosen font from `next/font/google`:

 app/layout.tsxJavaScriptTypeScript

```
import { Geist } from 'next/font/google'

const geist = Geist({
  subsets: ['latin'],
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={geist.className}>
      <body>{children}</body>
    </html>
  )
}
```

We recommend using [variable fonts](https://fonts.google.com/variablefonts) for the best performance and flexibility. But if you can't use a variable font, you will need to specify a weight:

 app/layout.tsxJavaScriptTypeScript

```
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  weight: '400',
  subsets: ['latin'],
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={roboto.className}>
      <body>{children}</body>
    </html>
  )
}
```

## Local fonts

To use a local font, import your font from `next/font/local` and specify the [src](https://nextjs.org/docs/app/api-reference/components/font#src) of your local font file. Fonts can be stored in the [public](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) folder or co-located inside the `app` folder. For example:

app/layout.tsxJavaScriptTypeScript

```
import localFont from 'next/font/local'

const myFont = localFont({
  src: './my-font.woff2',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={myFont.className}>
      <body>{children}</body>
    </html>
  )
}
```

If you want to use multiple files for a single font family, `src` can be an array:

```
const roboto = localFont({
  src: [
    {
      path: './Roboto-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: './Roboto-Italic.woff2',
      weight: '400',
      style: 'italic',
    },
    {
      path: './Roboto-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
    {
      path: './Roboto-BoldItalic.woff2',
      weight: '700',
      style: 'italic',
    },
  ],
})
```

## API Reference

See the API Reference for the full feature set of Next.js Font[FontOptimizing loading web fonts with the built-in `next/font` loaders.](https://nextjs.org/docs/app/api-reference/components/font)

Was this helpful?

supported.

---

# Image Optimization

> Learn how to optimize images in Next.js

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Image Optimization

# Image Optimization

Last updated  June 11, 2025

The Next.js [<Image>](https://nextjs.org/docs/app/api-reference/components/image) component extends the HTML `<img>` element to provide:

- **Size optimization:** Automatically serving correctly sized images for each device, using modern image formats like WebP.
- **Visual stability:** Preventing [layout shift](https://web.dev/articles/cls) automatically when images are loading.
- **Faster page loads:** Only loading images when they enter the viewport using native browser lazy loading, with optional blur-up placeholders.
- **Asset flexibility:** Resizing images on-demand, even images stored on remote servers.

To start using `<Image>`, import it from `next/image` and render it within your component.

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return <Image src="" alt="" />
}
```

The `src` property can be a [local](#local-images) or [remote](#remote-images) image.

> **🎥 Watch:** Learn more about how to use `next/image` → [YouTube (9 minutes)](https://youtu.be/IU_qq_c_lKA).

## Local images

You can store static files, like images and fonts, under a folder called [public](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) in the root directory. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

 ![Folder structure showing app and public folders](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fpublic-folder.png&w=3840&q=75)![Folder structure showing app and public folders](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fpublic-folder.png&w=3840&q=75) app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="/profile.png"
      alt="Picture of the author"
      width={500}
      height={500}
    />
  )
}
```

If the image is statically imported, Next.js will automatically determine the intrinsic [width](https://nextjs.org/docs/app/api-reference/components/image#width-and-height) and [height](https://nextjs.org/docs/app/api-reference/components/image#width-and-height). These values are used to determine the image ratio and prevent [Cumulative Layout Shift](https://web.dev/articles/cls) while your image is loading.

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'
import ProfileImage from './profile.png'

export default function Page() {
  return (
    <Image
      src={ProfileImage}
      alt="Picture of the author"
      // width={500} automatically provided
      // height={500} automatically provided
      // blurDataURL="data:..." automatically provided
      // placeholder="blur" // Optional blur-up while loading
    />
  )
}
```

## Remote images

To use a remote image, you can provide a URL string for the `src` property.

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="https://s3.amazonaws.com/my-bucket/profile.png"
      alt="Picture of the author"
      width={500}
      height={500}
    />
  )
}
```

Since Next.js does not have access to remote files during the build process, you'll need to provide the [width](https://nextjs.org/docs/app/api-reference/components/image#width-and-height), [height](https://nextjs.org/docs/app/api-reference/components/image#width-and-height) and optional [blurDataURL](https://nextjs.org/docs/app/api-reference/components/image#blurdataurl) props manually. The `width` and `height` are used to infer the correct aspect ratio of image and avoid layout shift from the image loading in. Alternatively, you can use the [fillproperty](https://nextjs.org/docs/app/api-reference/components/image#fill) to make the image fill the size of the parent element.

To safely allow images from remote servers, you need to define a list of supported URL patterns in [next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js). Be as specific as possible to prevent malicious usage. For example, the following configuration will only allow images from a specific AWS S3 bucket:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const config: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 's3.amazonaws.com',
        port: '',
        pathname: '/my-bucket/**',
        search: '',
      },
    ],
  },
}

export default config
```

## API Reference

See the API Reference for the full feature set of Next.js Image.[Image ComponentOptimize Images in your Next.js Application using the built-in `next/image` Component.](https://nextjs.org/docs/app/api-reference/components/image)

Was this helpful?

supported.

---

# Installation

> Learn how to create a new Next.js application with the `create-next-app` CLI, and set up TypeScript, ESLint, and Module Path Aliases.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Installation

# Installation

Last updated  December 9, 2025

Create a new Next.js app and run it locally.

## Quick start

1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000`.

Terminal

```
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dev
```

- `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind, ESLint, App Router, and Turbopack, with import alias `@/*`.

## System requirements

Before you begin, make sure your development environment meets the following requirements:

- Minimum Node.js version: [20.9](https://nodejs.org/)
- Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers

Next.js supports modern browsers with zero configuration.

- Chrome 111+
- Edge 111+
- Firefox 111+
- Safari 16.4+

Learn more about [browser support](https://nextjs.org/docs/architecture/supported-browsers), including how to configure polyfills and target specific browsers.

## Create with the CLI

The quickest way to create a new Next.js app is using [create-next-app](https://nextjs.org/docs/app/api-reference/cli/create-next-app), which sets up everything automatically for you. To create a project, run:

 Terminal

```
npx create-next-app@latest
```

On installation, you'll see the following prompts:

 Terminal

```
What is your project named? my-app
Would you like to use the recommended Next.js defaults?
    Yes, use recommended defaults - TypeScript, ESLint, Tailwind CSS, App Router, Turbopack
    No, reuse previous settings
    No, customize settings - Choose your own preferences
```

If you choose to `customize settings`, you'll see the following prompts:

 Terminal

```
Would you like to use TypeScript? No / Yes
Which linter would you like to use? ESLint / Biome / None
Would you like to use React Compiler? No / Yes
Would you like to use Tailwind CSS? No / Yes
Would you like your code inside a `src/` directory? No / Yes
Would you like to use App Router? (recommended) No / Yes
Would you like to customize the import alias (`@/*` by default)? No / Yes
What import alias would you like configured? @/*
```

After the prompts, [create-next-app](https://nextjs.org/docs/app/api-reference/cli/create-next-app) will create a folder with your project name and install the required dependencies.

## Manual installation

To manually create a new Next.js app, install the required packages:

 Terminal

```
pnpm i next@latest react@latest react-dom@latest
```

> **Good to know**: The App Router uses [React canary releases](https://react.dev/blog/2023/05/03/react-canaries) built-in, which include all the stable React 19 changes, as well as newer features being validated in frameworks. The Pages Router uses the React version you install in `package.json`.

Then, add the following scripts to your `package.json` file:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "lint:fix": "eslint --fix"
  }
}
```

These scripts refer to the different stages of developing an application:

- `next dev`: Starts the development server using Turbopack (default bundler).
- `next build`: Builds the application for production.
- `next start`: Starts the production server.
- `eslint`: Runs ESLint.

Turbopack is now the default bundler. To use Webpack run `next dev --webpack` or `next build --webpack`. See the [Turbopack docs](https://nextjs.org/docs/app/api-reference/turbopack) for configuration details.

### Create theappdirectory

Next.js uses file-system routing, which means the routes in your application are determined by how you structure your files.

Create an `app` folder. Then, inside `app`, create a `layout.tsx` file. This file is the [root layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout). It's required and must contain the `<html>` and `<body>` tags.

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

Create a home page `app/page.tsx` with some initial content:

app/page.tsxJavaScriptTypeScript

```
export default function Page() {
  return <h1>Hello, Next.js!</h1>
}
```

Both `layout.tsx` and `page.tsx` will be rendered when the user visits the root of your application (`/`).

![App Folder Structure](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fapp-getting-started.png&w=3840&q=75)![App Folder Structure](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fapp-getting-started.png&w=3840&q=75)

> **Good to know**:
>
>
>
> - If you forget to create the root layout, Next.js will automatically create this file when running the development server with `next dev`.
> - You can optionally use a [srcfolder](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder) in the root of your project to separate your application's code from configuration files.

### Create thepublicfolder (optional)

Create a [publicfolder](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) at the root of your project to store static assets such as images, fonts, etc. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

You can then reference these assets using the root path (`/`). For example, `public/profile.png` can be referenced as `/profile.png`:

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return <Image src="/profile.png" alt="Profile" width={100} height={100} />
}
```

## Run the development server

1. Run `npm run dev` to start the development server.
2. Visit `http://localhost:3000` to view your application.
3. Edit the `app/page.tsx` file and save it to see the updated result in your browser.

## Set up TypeScript

> Minimum TypeScript version: `v5.1.0`

Next.js comes with built-in TypeScript support. To add TypeScript to your project, rename a file to `.ts` / `.tsx` and run `next dev`. Next.js will automatically install the necessary dependencies and add a `tsconfig.json` file with the recommended config options.

### IDE Plugin

Next.js includes a custom TypeScript plugin and type checker, which VSCode and other code editors can use for advanced type-checking and auto-completion.

You can enable the plugin in VS Code by:

1. Opening the command palette (`Ctrl/⌘` + `Shift` + `P`)
2. Searching for "TypeScript: Select TypeScript Version"
3. Selecting "Use Workspace Version"

![TypeScript Command Palette](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ftypescript-command-palette.png&w=3840&q=75)![TypeScript Command Palette](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ftypescript-command-palette.png&w=3840&q=75)

See the [TypeScript reference](https://nextjs.org/docs/app/api-reference/config/typescript) page for more information.

## Set up linting

Next.js supports linting with either ESLint or Biome. Choose a linter and run it directly via `package.json` scripts.

- Use **ESLint** (comprehensive rules):

 package.json

```
{
  "scripts": {
    "lint": "eslint",
    "lint:fix": "eslint --fix"
  }
}
```

- Or use **Biome** (fast linter + formatter):

 package.json

```
{
  "scripts": {
    "lint": "biome check",
    "format": "biome format --write"
  }
}
```

If your project previously used `next lint`, migrate your scripts to the ESLint CLI with the codemod:

 Terminal

```
npx @next/codemod@canary next-lint-to-eslint-cli .
```

If you use ESLint, create an explicit config (recommended `eslint.config.mjs`). ESLint supports both [the legacy.eslintrc.*and the newereslint.config.mjsformats](https://eslint.org/docs/latest/use/configure/configuration-files#configuring-eslint). See the [ESLint API reference](https://nextjs.org/docs/app/api-reference/config/eslint#with-core-web-vitals) for a recommended setup.

> **Good to know**: Starting with Next.js 16, `next build` no longer runs the linter automatically. Instead, you can run your linter through NPM scripts.

See the [ESLint Plugin](https://nextjs.org/docs/app/api-reference/config/eslint) page for more information.

## Set up Absolute Imports and Module Path Aliases

Next.js has in-built support for the `"paths"` and `"baseUrl"` options of `tsconfig.json` and `jsconfig.json` files.

These options allow you to alias project directories to absolute paths, making it easier and cleaner to import modules. For example:

```
// Before
import { Button } from '../../../components/button'

// After
import { Button } from '@/components/button'
```

To configure absolute imports, add the `baseUrl` configuration option to your `tsconfig.json` or `jsconfig.json` file. For example:

 tsconfig.json or jsconfig.json

```
{
  "compilerOptions": {
    "baseUrl": "src/"
  }
}
```

In addition to configuring the `baseUrl` path, you can use the `"paths"` option to `"alias"` module paths.

For example, the following configuration maps `@/components/*` to `components/*`:

 tsconfig.json or jsconfig.json

```
{
  "compilerOptions": {
    "baseUrl": "src/",
    "paths": {
      "@/styles/*": ["styles/*"],
      "@/components/*": ["components/*"]
    }
  }
}
```

Each of the `"paths"` are relative to the `baseUrl` location.

Was this helpful?

supported.
