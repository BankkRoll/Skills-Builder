# How to self and more

# How to self

> Learn how to self-host your Next.js application on a Node.js server, Docker image, or static HTML files (static exports).

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Self-Hosting

# How to self-host your Next.js application

Last updated  December 12, 2025

When [deploying](https://nextjs.org/docs/app/getting-started/deploying) your Next.js app, you may want to configure how different features are handled based on your infrastructure.

> **🎥 Watch:** Learn more about self-hosting Next.js → [YouTube (45 minutes)](https://www.youtube.com/watch?v=sIVL4JMqRfc).

## Reverse Proxy

When self-hosting, it's recommended to use a reverse proxy (like nginx) in front of your Next.js server rather than exposing it directly to the internet. A reverse proxy can handle malformed requests, slow connection attacks, payload size limits, rate limiting, and other security concerns, offloading these tasks from the Next.js server. This allows the server to dedicate its resources to rendering rather than request validation.

## Image Optimization

[Image Optimization](https://nextjs.org/docs/app/api-reference/components/image) through `next/image` works self-hosted with zero configuration when deploying using `next start`. If you would prefer to have a separate service to optimize images, you can [configure an image loader](https://nextjs.org/docs/app/api-reference/components/image#loader).

Image Optimization can be used with a [static export](https://nextjs.org/docs/app/guides/static-exports#image-optimization) by defining a custom image loader in `next.config.js`. Note that images are optimized at runtime, not during the build.

> **Good to know:**
>
>
>
> - On glibc-based Linux systems, Image Optimization may require [additional configuration](https://sharp.pixelplumbing.com/install#linux-memory-allocator) to prevent excessive memory usage.
> - Learn more about the [caching behavior of optimized images](https://nextjs.org/docs/app/api-reference/components/image#minimumcachettl) and how to configure the TTL.
> - You can also [disable Image Optimization](https://nextjs.org/docs/app/api-reference/components/image#unoptimized) and still retain other benefits of using `next/image` if you prefer. For example, if you are optimizing images yourself separately.

## Proxy

[Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) works self-hosted with zero configuration when deploying using `next start`. Since it requires access to the incoming request, it is not supported when using a [static export](https://nextjs.org/docs/app/guides/static-exports).

Proxy uses the [Edge runtime](https://nextjs.org/docs/app/api-reference/edge), a subset of all available Node.js APIs to help ensure low latency, since it may run in front of every route or asset in your application. If you do not want this, you can use the [full Node.js runtime](https://nextjs.org/blog/next-15-2#nodejs-middleware-experimental) to run Proxy.

If you are looking to add logic (or use an external package) that requires all Node.js APIs, you might be able to move this logic to a [layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout) as a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components). For example, checking [headers](https://nextjs.org/docs/app/api-reference/functions/headers) and [redirecting](https://nextjs.org/docs/app/api-reference/functions/redirect). You can also use headers, cookies, or query parameters to [redirect](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects#header-cookie-and-query-matching) or [rewrite](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites#header-cookie-and-query-matching) through `next.config.js`. If that does not work, you can also use a [custom server](https://nextjs.org/docs/pages/guides/custom-server).

## Environment Variables

Next.js can support both build time and runtime environment variables.

**By default, environment variables are only available on the server**. To expose an environment variable to the browser, it must be prefixed with `NEXT_PUBLIC_`. However, these public environment variables will be inlined into the JavaScript bundle during `next build`.

You safely read environment variables on the server during dynamic rendering.

app/page.tsJavaScriptTypeScript

```
import { connection } from 'next/server'

export default async function Component() {
  await connection()
  // cookies, headers, and other Dynamic APIs
  // will also opt into dynamic rendering, meaning
  // this env variable is evaluated at runtime
  const value = process.env.MY_VALUE
  // ...
}
```

This allows you to use a singular Docker image that can be promoted through multiple environments with different values.

> **Good to know:**
>
>
>
> - You can run code on server startup using the [registerfunction](https://nextjs.org/docs/app/guides/instrumentation).

## Caching and ISR

Next.js can cache responses, generated static pages, build outputs, and other static assets like images, fonts, and scripts.

Caching and revalidating pages (with [Incremental Static Regeneration](https://nextjs.org/docs/app/guides/incremental-static-regeneration)) use the **same shared cache**. By default, this cache is stored to the filesystem (on disk) on your Next.js server. **This works automatically when self-hosting** using both the Pages and App Router.

You can configure the Next.js cache location if you want to persist cached pages and data to durable storage, or share the cache across multiple containers or instances of your Next.js application.

### Automatic Caching

- Next.js sets the `Cache-Control` header of `public, max-age=31536000, immutable` to truly immutable assets. It cannot be overridden. These immutable files contain a SHA-hash in the file name, so they can be safely cached indefinitely. For example, [Static Image Imports](https://nextjs.org/docs/app/getting-started/images#local-images). You can [configure the TTL](https://nextjs.org/docs/app/api-reference/components/image#minimumcachettl) for images.
- Incremental Static Regeneration (ISR) sets the `Cache-Control` header of `s-maxage: <revalidate in getStaticProps>, stale-while-revalidate`. This revalidation time is defined in your [getStaticPropsfunction](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) in seconds. If you set `revalidate: false`, it will default to a one-year cache duration.
- Dynamically rendered pages set a `Cache-Control` header of `private, no-cache, no-store, max-age=0, must-revalidate` to prevent user-specific data from being cached. This applies to both the App Router and Pages Router. This also includes [Draft Mode](https://nextjs.org/docs/app/guides/draft-mode).

### Static Assets

If you want to host static assets on a different domain or CDN, you can use the `assetPrefix` [configuration](https://nextjs.org/docs/app/api-reference/config/next-config-js/assetPrefix) in `next.config.js`. Next.js will use this asset prefix when retrieving JavaScript or CSS files. Separating your assets to a different domain does come with the downside of extra time spent on DNS and TLS resolution.

[Learn more aboutassetPrefix](https://nextjs.org/docs/app/api-reference/config/next-config-js/assetPrefix).

### Configuring Caching

By default, generated cache assets will be stored in memory (defaults to 50mb) and on disk. If you are hosting Next.js using a container orchestration platform like Kubernetes, each pod will have a copy of the cache. To prevent stale data from being shown since the cache is not shared between pods by default, you can configure the Next.js cache to provide a cache handler and disable in-memory caching.

To configure the ISR/Data Cache location when self-hosting, you can configure a custom handler in your `next.config.js` file:

 next.config.js

```
module.exports = {
  cacheHandler: require.resolve('./cache-handler.js'),
  cacheMaxMemorySize: 0, // disable default in-memory caching
}
```

Then, create `cache-handler.js` in the root of your project, for example:

 cache-handler.js

```
const cache = new Map()

module.exports = class CacheHandler {
  constructor(options) {
    this.options = options
  }

  async get(key) {
    // This could be stored anywhere, like durable storage
    return cache.get(key)
  }

  async set(key, data, ctx) {
    // This could be stored anywhere, like durable storage
    cache.set(key, {
      value: data,
      lastModified: Date.now(),
      tags: ctx.tags,
    })
  }

  async revalidateTag(tags) {
    // tags is either a string or an array of strings
    tags = [tags].flat()
    // Iterate over all entries in the cache
    for (let [key, value] of cache) {
      // If the value's tags include the specified tag, delete this entry
      if (value.tags.some((tag) => tags.includes(tag))) {
        cache.delete(key)
      }
    }
  }

  // If you want to have temporary in memory cache for a single request that is reset
  // before the next request you can leverage this method
  resetRequestCache() {}
}
```

Using a custom cache handler will allow you to ensure consistency across all pods hosting your Next.js application. For instance, you can save the cached values anywhere, like [Redis](https://github.com/vercel/next.js/tree/canary/examples/cache-handler-redis) or AWS S3.

> **Good to know:**
>
>
>
> - `revalidatePath` is a convenience layer on top of cache tags. Calling `revalidatePath` will call the `revalidateTag` function with a special default tag for the provided page.

## Build Cache

Next.js generates an ID during `next build` to identify which version of your application is being served. The same build should be used and boot up multiple containers.

If you are rebuilding for each stage of your environment, you will need to generate a consistent build ID to use between containers. Use the `generateBuildId` command in `next.config.js`:

 next.config.js

```
module.exports = {
  generateBuildId: async () => {
    // This could be anything, using the latest git hash
    return process.env.GIT_HASH
  },
}
```

## Version Skew

Next.js will automatically mitigate most instances of [version skew](https://www.industrialempathy.com/posts/version-skew/) and automatically reload the application to retrieve new assets when detected. For example, if there is a mismatch in the `deploymentId`, transitions between pages will perform a hard navigation versus using a prefetched value.

When the application is reloaded, there may be a loss of application state if it's not designed to persist between page navigations. For example, using URL state or local storage would persist state after a page refresh. However, component state like `useState` would be lost in such navigations.

## Streaming and Suspense

The Next.js App Router supports [streaming responses](https://nextjs.org/docs/app/api-reference/file-conventions/loading) when self-hosting. If you are using nginx or a similar proxy, you will need to configure it to disable buffering to enable streaming.

For example, you can disable buffering in nginx by setting `X-Accel-Buffering` to `no`:

next.config.js

```
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*{/}?',
        headers: [
          {
            key: 'X-Accel-Buffering',
            value: 'no',
          },
        ],
      },
    ]
  },
}
```

## Cache Components

[Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) works by default with Next.js and is not a CDN-only feature. This includes deployment as a Node.js server (through `next start`) and when used with a Docker container.

## Usage with CDNs

When using a CDN in front of your Next.js application, the page will include `Cache-Control: private` response header when dynamic APIs are accessed. This ensures that the resulting HTML page is marked as non-cacheable. If the page is fully prerendered to static, it will include `Cache-Control: public` to allow the page to be cached on the CDN.

If you don't need a mix of both static and dynamic components, you can make your entire route static and cache the output HTML on a CDN. This Automatic Static Optimization is the default behavior when running `next build` if dynamic APIs are not used.

As Partial Prerendering moves to stable, we will provide support through the Deployment Adapters API.

## after

[after](https://nextjs.org/docs/app/api-reference/functions/after) is fully supported when self-hosting with `next start`.

When stopping the server, ensure a graceful shutdown by sending `SIGINT` or `SIGTERM` signals and waiting. This allows the Next.js server to wait until after pending callback functions or promises used inside `after` have finished.

Was this helpful?

supported.

---

# How to build single

> Next.js fully supports building Single-Page Applications (SPAs).

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)SPAs

# How to build single-page applications with Next.js

Last updated  June 10, 2025

Next.js fully supports building Single-Page Applications (SPAs).

This includes fast route transitions with prefetching, client-side data fetching, using browser APIs, integrating with third-party client libraries, creating static routes, and more.

If you have an existing SPA, you can migrate to Next.js without large changes to your code. Next.js then allows you to progressively add server features as needed.

## What is a Single-Page Application?

The definition of a SPA varies. We’ll define a “strict SPA” as:

- **Client-side rendering (CSR)**: The app is served by one HTML file (e.g. `index.html`). Every route, page transition, and data fetch is handled by JavaScript in the browser.
- **No full-page reloads**: Rather than requesting a new document for each route, client-side JavaScript manipulates the current page’s DOM and fetches data as needed.

Strict SPAs often require large amounts of JavaScript to load before the page can be interactive. Further, client data waterfalls can be challenging to manage. Building SPAs with Next.js can address these issues.

## Why use Next.js for SPAs?

Next.js can automatically code split your JavaScript bundles, and generate multiple HTML entry points into different routes. This avoids loading unnecessary JavaScript code on the client-side, reducing the bundle size and enabling faster page loads.

The [next/link](https://nextjs.org/docs/app/api-reference/components/link) component automatically [prefetches](https://nextjs.org/docs/app/api-reference/components/link#prefetch) routes, giving you the fast page transitions of a strict SPA, but with the advantage of persisting application routing state to the URL for linking and sharing.

Next.js can start as a static site or even a strict SPA where everything is rendered client-side. If your project grows, Next.js allows you to progressively add more server features (e.g. [React Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data), and more) as needed.

## Examples

Let's explore common patterns used to build SPAs and how Next.js solves them.

### Using React’susewithin a Context Provider

We recommend fetching data in a parent component (or layout), returning the Promise, and then unwrapping the value in a Client Component with React’s [usehook](https://react.dev/reference/react/use).

Next.js can start data fetching early on the server. In this example, that’s the root layout — the entry point to your application. The server can immediately begin streaming a response to the client.

By “hoisting” your data fetching to the root layout, Next.js starts the specified requests on the server early before any other components in your application. This eliminates client waterfalls and prevents having multiple roundtrips between client and server. It can also significantly improve performance, as your server is closer (and ideally colocated) to where your database is located.

For example, update your root layout to call the Promise, but do *not* await it.

 app/layout.tsxJavaScriptTypeScript

```
import { UserProvider } from './user-provider'
import { getUser } from './user' // some server-side function

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  let userPromise = getUser() // do NOT await

  return (
    <html lang="en">
      <body>
        <UserProvider userPromise={userPromise}>{children}</UserProvider>
      </body>
    </html>
  )
}
```

While you can [defer and pass a single Promise](https://nextjs.org/docs/app/getting-started/fetching-data#streaming-data-with-the-use-hook) as a prop to a Client Component, we generally see this pattern paired with a React context provider. This enables easier access from Client Components with a custom React Hook.

You can forward a Promise to the React context provider:

 app/user-provider.tsJavaScriptTypeScript

```
'use client';

import { createContext, useContext, ReactNode } from 'react';

type User = any;
type UserContextType = {
  userPromise: Promise<User | null>;
};

const UserContext = createContext<UserContextType | null>(null);

export function useUser(): UserContextType {
  let context = useContext(UserContext);
  if (context === null) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}

export function UserProvider({
  children,
  userPromise
}: {
  children: ReactNode;
  userPromise: Promise<User | null>;
}) {
  return (
    <UserContext.Provider value={{ userPromise }}>
      {children}
    </UserContext.Provider>
  );
}
```

Finally, you can call the `useUser()` custom hook in any Client Component and unwrap the Promise:

 app/profile.tsxJavaScriptTypeScript

```
'use client'

import { use } from 'react'
import { useUser } from './user-provider'

export function Profile() {
  const { userPromise } = useUser()
  const user = use(userPromise)

  return '...'
}
```

The component that consumes the Promise (e.g. `Profile` above) will be suspended. This enables partial hydration. You can see the streamed and prerendered HTML before JavaScript has finished loading.

### SPAs with SWR

[SWR](https://swr.vercel.app) is a popular React library for data fetching.

With SWR 2.3.0 (and React 19+), you can gradually adopt server features alongside your existing SWR-based client data fetching code. This is an abstraction of the above `use()` pattern. This means you can move data fetching between the client and server-side, or use both:

- **Client-only:** `useSWR(key, fetcher)`
- **Server-only:** `useSWR(key)` + RSC-provided data
- **Mixed:** `useSWR(key, fetcher)` + RSC-provided data

For example, wrap your application with `<SWRConfig>` and a `fallback`:

 app/layout.tsxJavaScriptTypeScript

```
import { SWRConfig } from 'swr'
import { getUser } from './user' // some server-side function

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <SWRConfig
      value={{
        fallback: {
          // We do NOT await getUser() here
          // Only components that read this data will suspend
          '/api/user': getUser(),
        },
      }}
    >
      {children}
    </SWRConfig>
  )
}
```

Because this is a Server Component, `getUser()` can securely read cookies, headers, or talk to your database. No separate API route is needed. Client components below the `<SWRConfig>` can call `useSWR()` with the same key to retrieve the user data. The component code with `useSWR` **does not require any changes** from your existing client-fetching solution.

 app/profile.tsxJavaScriptTypeScript

```
'use client'

import useSWR from 'swr'

export function Profile() {
  const fetcher = (url) => fetch(url).then((res) => res.json())
  // The same SWR pattern you already know
  const { data, error } = useSWR('/api/user', fetcher)

  return '...'
}
```

The `fallback` data can be prerendered and included in the initial HTML response, then immediately read in the child components using `useSWR`. SWR’s polling, revalidation, and caching still run **client-side only**, so it preserves all the interactivity you rely on for an SPA.

Since the initial `fallback` data is automatically handled by Next.js, you can now delete any conditional logic previously needed to check if `data` was `undefined`. When the data is loading, the closest `<Suspense>` boundary will be suspended.

|  | SWR | RSC | RSC + SWR |
| --- | --- | --- | --- |
| SSR data |  |  |  |
| Streaming while SSR |  |  |  |
| Deduplicate requests |  |  |  |
| Client-side features |  |  |  |

### SPAs with React Query

You can use React Query with Next.js on both the client and server. This enables you to build both strict SPAs, as well as take advantage of server features in Next.js paired with React Query.

Learn more in the [React Query documentation](https://tanstack.com/query/latest/docs/framework/react/guides/advanced-ssr).

### Rendering components only in the browser

Client components are [prerendered](https://github.com/reactwg/server-components/discussions/4) during `next build`. If you want to disable prerendering for a Client Component and only load it in the browser environment, you can use [next/dynamic](https://nextjs.org/docs/app/guides/lazy-loading#nextdynamic):

```
import dynamic from 'next/dynamic'

const ClientOnlyComponent = dynamic(() => import('./component'), {
  ssr: false,
})
```

This can be useful for third-party libraries that rely on browser APIs like `window` or `document`. You can also add a `useEffect` that checks for the existence of these APIs, and if they do not exist, return `null` or a loading state which would be prerendered.

### Shallow routing on the client

If you are migrating from a strict SPA like [Create React App](https://nextjs.org/docs/app/guides/migrating/from-create-react-app) or [Vite](https://nextjs.org/docs/app/guides/migrating/from-vite), you might have existing code which shallow routes to update the URL state. This can be useful for manual transitions between views in your application *without* using the default Next.js file-system routing.

Next.js allows you to use the native [window.history.pushState](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState) and [window.history.replaceState](https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState) methods to update the browser's history stack without reloading the page.

`pushState` and `replaceState` calls integrate into the Next.js Router, allowing you to sync with [usePathname](https://nextjs.org/docs/app/api-reference/functions/use-pathname) and [useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params).

```
'use client'

import { useSearchParams } from 'next/navigation'

export default function SortProducts() {
  const searchParams = useSearchParams()

  function updateSorting(sortOrder: string) {
    const urlSearchParams = new URLSearchParams(searchParams.toString())
    urlSearchParams.set('sort', sortOrder)
    window.history.pushState(null, '', `?${urlSearchParams.toString()}`)
  }

  return (
    <>
      <button onClick={() => updateSorting('asc')}>Sort Ascending</button>
      <button onClick={() => updateSorting('desc')}>Sort Descending</button>
    </>
  )
}
```

Learn more about how [routing and navigation](https://nextjs.org/docs/app/getting-started/linking-and-navigating#how-navigation-works) work in Next.js.

### Using Server Actions in Client Components

You can progressively adopt Server Actions while still using Client Components. This allows you to remove boilerplate code to call an API route, and instead use React features like `useActionState` to handle loading and error states.

For example, create your first Server Action:

 app/actions.tsJavaScriptTypeScript

```
'use server'

export async function create() {}
```

You can import and use a Server Action from the client, similar to calling a JavaScript function. You do not need to create an API endpoint manually:

 app/button.tsxJavaScriptTypeScript

```
'use client'

import { create } from './actions'

export function Button() {
  return <button onClick={() => create()}>Create</button>
}
```

Learn more about [mutating data with Server Actions](https://nextjs.org/docs/app/getting-started/updating-data).

## Static export (optional)

Next.js also supports generating a fully [static site](https://nextjs.org/docs/app/guides/static-exports). This has some advantages over strict SPAs:

- **Automatic code-splitting**: Instead of shipping a single `index.html`, Next.js will generate an HTML file per route, so your visitors get the content faster without waiting for the client JavaScript bundle.
- **Improved user experience:** Instead of a minimal skeleton for all routes, you get fully rendered pages for each route. When users navigate client side, transitions remain instant and SPA-like.

To enable a static export, update your configuration:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'export',
}

export default nextConfig
```

After running `next build`, Next.js will create an `out` folder with the HTML/CSS/JS assets for your application.

> **Note:** Next.js server features are not supported with static exports. [Learn more](https://nextjs.org/docs/app/guides/static-exports#unsupported-features).

## Migrating existing projects to Next.js

You can incrementally migrate to Next.js by following our guides:

- [Migrating from Create React App](https://nextjs.org/docs/app/guides/migrating/from-create-react-app)
- [Migrating from Vite](https://nextjs.org/docs/app/guides/migrating/from-vite)

If you are already using a SPA with the Pages Router, you can learn how to [incrementally adopt the App Router](https://nextjs.org/docs/app/guides/migrating/app-router-migration).

Was this helpful?

supported.

---

# How to create a static export of your Next.js application

> Next.js enables starting as a static site or Single-Page Application (SPA), then later optionally upgrading to use features that require a server.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Static Exports

# How to create a static export of your Next.js application

Last updated  October 17, 2025

Next.js enables starting as a static site or Single-Page Application (SPA), then later optionally upgrading to use features that require a server.

When running `next build`, Next.js generates an HTML file per route. By breaking a strict SPA into individual HTML files, Next.js can avoid loading unnecessary JavaScript code on the client-side, reducing the bundle size and enabling faster page loads.

Since Next.js supports this static export, it can be deployed and hosted on any web server that can serve HTML/CSS/JS static assets.

## Configuration

To enable a static export, change the output mode inside `next.config.js`:

 next.config.js

```
/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  output: 'export',

  // Optional: Change links `/me` -> `/me/` and emit `/me.html` -> `/me/index.html`
  // trailingSlash: true,

  // Optional: Prevent automatic `/me` -> `/me/`, instead preserve `href`
  // skipTrailingSlashRedirect: true,

  // Optional: Change the output directory `out` -> `dist`
  // distDir: 'dist',
}

module.exports = nextConfig
```

After running `next build`, Next.js will create an `out` folder with the HTML/CSS/JS assets for your application.

## Supported Features

The core of Next.js has been designed to support static exports.

### Server Components

When you run `next build` to generate a static export, Server Components consumed inside the `app` directory will run during the build, similar to traditional static-site generation.

The resulting component will be rendered into static HTML for the initial page load and a static payload for client navigation between routes. No changes are required for your Server Components when using the static export, unless they consume [dynamic server functions](#unsupported-features).

app/page.tsxJavaScriptTypeScript

```
export default async function Page() {
  // This fetch will run on the server during `next build`
  const res = await fetch('https://api.example.com/...')
  const data = await res.json()

  return <main>...</main>
}
```

### Client Components

If you want to perform data fetching on the client, you can use a Client Component with [SWR](https://github.com/vercel/swr) to memoize requests.

app/other/page.tsxJavaScriptTypeScript

```
'use client'

import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((r) => r.json())

export default function Page() {
  const { data, error } = useSWR(
    `https://jsonplaceholder.typicode.com/posts/1`,
    fetcher
  )
  if (error) return 'Failed to load'
  if (!data) return 'Loading...'

  return data.title
}
```

Since route transitions happen client-side, this behaves like a traditional SPA. For example, the following index route allows you to navigate to different posts on the client:

app/page.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Page() {
  return (
    <>
      <h1>Index Page</h1>
      <hr />
      <ul>
        <li>
          <Link href="/post/1">Post 1</Link>
        </li>
        <li>
          <Link href="/post/2">Post 2</Link>
        </li>
      </ul>
    </>
  )
}
```

### Image Optimization

[Image Optimization](https://nextjs.org/docs/app/api-reference/components/image) through `next/image` can be used with a static export by defining a custom image loader in `next.config.js`. For example, you can optimize images with a service like Cloudinary:

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    loader: 'custom',
    loaderFile: './my-loader.ts',
  },
}

module.exports = nextConfig
```

This custom loader will define how to fetch images from a remote source. For example, the following loader will construct the URL for Cloudinary:

 my-loader.tsJavaScriptTypeScript

```
export default function cloudinaryLoader({
  src,
  width,
  quality,
}: {
  src: string
  width: number
  quality?: number
}) {
  const params = ['f_auto', 'c_limit', `w_${width}`, `q_${quality || 'auto'}`]
  return `https://res.cloudinary.com/demo/image/upload/${params.join(
    ','
  )}${src}`
}
```

You can then use `next/image` in your application, defining relative paths to the image in Cloudinary:

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return <Image alt="turtles" src="/turtles.jpg" width={300} height={300} />
}
```

### Route Handlers

Route Handlers will render a static response when running `next build`. Only the `GET` HTTP verb is supported. This can be used to generate static HTML, JSON, TXT, or other files from cached or uncached data. For example:

app/data.json/route.tsJavaScriptTypeScript

```
export async function GET() {
  return Response.json({ name: 'Lee' })
}
```

The above file `app/data.json/route.ts` will render to a static file during `next build`, producing `data.json` containing `{ name: 'Lee' }`.

If you need to read dynamic values from the incoming request, you cannot use a static export.

### Browser APIs

Client Components are pre-rendered to HTML during `next build`. Because [Web APIs](https://developer.mozilla.org/docs/Web/API) like `window`, `localStorage`, and `navigator` are not available on the server, you need to safely access these APIs only when running in the browser. For example:

```
'use client';

import { useEffect } from 'react';

export default function ClientComponent() {
  useEffect(() => {
    // You now have access to `window`
    console.log(window.innerHeight);
  }, [])

  return ...;
}
```

## Unsupported Features

Features that require a Node.js server, or dynamic logic that cannot be computed during the build process, are **not** supported:

- [Dynamic Routes](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) with `dynamicParams: true`
- [Dynamic Routes](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) without `generateStaticParams()`
- [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) that rely on Request
- [Cookies](https://nextjs.org/docs/app/api-reference/functions/cookies)
- [Rewrites](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites)
- [Redirects](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects)
- [Headers](https://nextjs.org/docs/app/api-reference/config/next-config-js/headers)
- [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)
- [Incremental Static Regeneration](https://nextjs.org/docs/app/guides/incremental-static-regeneration)
- [Image Optimization](https://nextjs.org/docs/app/api-reference/components/image) with the default `loader`
- [Draft Mode](https://nextjs.org/docs/app/guides/draft-mode)
- [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data)
- [Intercepting Routes](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes)

Attempting to use any of these features with `next dev` will result in an error, similar to setting the [dynamic](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamic) option to `error` in the root layout.

```
export const dynamic = 'error'
```

## Deploying

With a static export, Next.js can be deployed and hosted on any web server that can serve HTML/CSS/JS static assets.

When running `next build`, Next.js generates the static export into the `out` folder. For example, let's say you have the following routes:

- `/`
- `/blog/[id]`

After running `next build`, Next.js will generate the following files:

- `/out/index.html`
- `/out/404.html`
- `/out/blog/post-1.html`
- `/out/blog/post-2.html`

If you are using a static host like Nginx, you can configure rewrites from incoming requests to the correct files:

 nginx.conf

```
server {
  listen 80;
  server_name acme.com;

  root /var/www/out;

  location / {
      try_files $uri $uri.html $uri/ =404;
  }

  # This is necessary when `trailingSlash: false`.
  # You can omit this when `trailingSlash: true`.
  location /blog/ {
      rewrite ^/blog/(.*)$ /blog/$1.html break;
  }

  error_page 404 /404.html;
  location = /404.html {
      internal;
  }
}
```

## Version History

| Version | Changes |
| --- | --- |
| v14.0.0 | next exporthas been removed in favor of"output": "export" |
| v13.4.0 | App Router (Stable) adds enhanced static export support, including using React Server Components and Route Handlers. |
| v13.3.0 | next exportis deprecated and replaced with"output": "export" |

Was this helpful?

supported.

---

# How to install Tailwind CSS v3 in your Next.js application

> Style your Next.js Application using Tailwind CSS v3 for broader browser support.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Tailwind CSS v3

# How to install Tailwind CSS v3 in your Next.js application

Last updated  August 6, 2025

This guide will walk you through how to install [Tailwind CSS v3](https://v3.tailwindcss.com/) in your Next.js application.

> **Good to know:** For the latest Tailwind 4 setup, see the [Tailwind CSS setup instructions](https://nextjs.org/docs/app/getting-started/css#tailwind-css).

## Installing Tailwind v3

Install Tailwind CSS and its peer dependencies, then run the `init` command to generate both `tailwind.config.js` and `postcss.config.js` files:

 Terminal

```
pnpm add -D tailwindcss@^3 postcss autoprefixer
npx tailwindcss init -p
```

## Configuring Tailwind v3

Configure your template paths in your `tailwind.config.js` file:

 tailwind.config.js

```
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Add the Tailwind directives to your global CSS file:

app/globals.css

```
@tailwind base;
@tailwind components;
@tailwind utilities;
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

## Using classes

After installing Tailwind CSS and adding the global styles, you can use Tailwind's utility classes in your application.

 app/page.tsxJavaScriptTypeScript

```
export default function Page() {
  return <h1 className="text-3xl font-bold underline">Hello, Next.js!</h1>
}
```

## Usage with Turbopack

As of Next.js 13.1, Tailwind CSS and PostCSS are supported with [Turbopack](https://turbo.build/pack/docs/features/css#tailwind-css).

Was this helpful?

supported.

---

# How to set up Cypress with Next.js

> Learn how to set up Cypress with Next.js for End-to-End (E2E) and Component Testing.

[Guides](https://nextjs.org/docs/app/guides)[Testing](https://nextjs.org/docs/app/guides/testing)Cypress

# How to set up Cypress with Next.js

Last updated  August 19, 2025

[Cypress](https://www.cypress.io/) is a test runner used for **End-to-End (E2E)** and **Component Testing**. This page will show you how to set up Cypress with Next.js and write your first tests.

> **Warning:**
>
>
>
> - Cypress versions below 13.6.3 do not support [TypeScript version 5](https://github.com/cypress-io/cypress/issues/27731) with `moduleResolution:"bundler"`. However, this issue has been resolved in Cypress version 13.6.3 and later. [cypress v13.6.3](https://docs.cypress.io/guides/references/changelog#13-6-3)

## Quickstart

You can use `create-next-app` with the [with-cypress example](https://github.com/vercel/next.js/tree/canary/examples/with-cypress) to quickly get started.

Terminal

```
npx create-next-app@latest --example with-cypress with-cypress-app
```

## Manual setup

To manually set up Cypress, install `cypress` as a dev dependency:

 Terminal

```
npm install -D cypress
# or
yarn add -D cypress
# or
pnpm install -D cypress
```

Add the Cypress `open` command to the `package.json` scripts field:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "cypress:open": "cypress open"
  }
}
```

Run Cypress for the first time to open the Cypress testing suite:

 Terminal

```
npm run cypress:open
```

You can choose to configure **E2E Testing** and/or **Component Testing**. Selecting any of these options will automatically create a `cypress.config.js` file and a `cypress` folder in your project.

## Creating your first Cypress E2E test

Ensure your `cypress.config` file has the following configuration:

 cypress.config.tsJavaScriptTypeScript

```
import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {},
  },
})
```

Then, create two new Next.js files:

 app/page.js

```
import Link from 'next/link'

export default function Page() {
  return (
    <div>
      <h1>Home</h1>
      <Link href="/about">About</Link>
    </div>
  )
}
```

app/about/page.js

```
import Link from 'next/link'

export default function Page() {
  return (
    <div>
      <h1>About</h1>
      <Link href="/">Home</Link>
    </div>
  )
}
```

Add a test to check your navigation is working correctly:

 cypress/e2e/app.cy.js

```
describe('Navigation', () => {
  it('should navigate to the about page', () => {
    // Start from the index page
    cy.visit('http://localhost:3000/')

    // Find a link with an href attribute containing "about" and click it
    cy.get('a[href*="about"]').click()

    // The new url should include "/about"
    cy.url().should('include', '/about')

    // The new page should contain an h1 with "About"
    cy.get('h1').contains('About')
  })
})
```

### Running E2E Tests

Cypress will simulate a user navigating your application, this requires your Next.js server to be running. We recommend running your tests against your production code to more closely resemble how your application will behave.

Run `npm run build && npm run start` to build your Next.js application, then run `npm run cypress:open` in another terminal window to start Cypress and run your E2E Testing suite.

> **Good to know:**
>
>
>
> - You can use `cy.visit("/")` instead of `cy.visit("http://localhost:3000/")` by adding `baseUrl: 'http://localhost:3000'` to the `cypress.config.js` configuration file.
> - Alternatively, you can install the [start-server-and-test](https://www.npmjs.com/package/start-server-and-test) package to run the Next.js production server in conjunction with Cypress. After installation, add `"test": "start-server-and-test start http://localhost:3000 cypress"` to your `package.json` scripts field. Remember to rebuild your application after new changes.

## Creating your first Cypress component test

Component tests build and mount a specific component without having to bundle your whole application or start a server.

Select **Component Testing** in the Cypress app, then select **Next.js** as your front-end framework. A `cypress/component` folder will be created in your project, and a `cypress.config.js` file will be updated to enable Component Testing.

Ensure your `cypress.config` file has the following configuration:

 cypress.config.tsJavaScriptTypeScript

```
import { defineConfig } from 'cypress'

export default defineConfig({
  component: {
    devServer: {
      framework: 'next',
      bundler: 'webpack',
    },
  },
})
```

Assuming the same components from the previous section, add a test to validate a component is rendering the expected output:

 cypress/component/about.cy.tsx

```
import Page from '../../app/page'

describe('<Page />', () => {
  it('should render and display expected content', () => {
    // Mount the React component for the Home page
    cy.mount(<Page />)

    // The new page should contain an h1 with "Home"
    cy.get('h1').contains('Home')

    // Validate that a link with the expected URL is present
    // Following the link is better suited to an E2E test
    cy.get('a[href="/about"]').should('be.visible')
  })
})
```

> **Good to know**:
>
>
>
> - Cypress currently doesn't support Component Testing for `async` Server Components. We recommend using E2E testing.
> - Since component tests do not require a Next.js server, features like `<Image />` that rely on a server being available may not function out-of-the-box.

### Running Component Tests

Run `npm run cypress:open` in your terminal to start Cypress and run your Component Testing suite.

## Continuous Integration (CI)

In addition to interactive testing, you can also run Cypress headlessly using the `cypress run` command, which is better suited for CI environments:

 package.json

```
{
  "scripts": {
    //...
    "e2e": "start-server-and-test dev http://localhost:3000 \"cypress open --e2e\"",
    "e2e:headless": "start-server-and-test dev http://localhost:3000 \"cypress run --e2e\"",
    "component": "cypress open --component",
    "component:headless": "cypress run --component"
  }
}
```

You can learn more about Cypress and Continuous Integration from these resources:

- [Next.js with Cypress example](https://github.com/vercel/next.js/tree/canary/examples/with-cypress)
- [Cypress Continuous Integration Docs](https://docs.cypress.io/guides/continuous-integration/introduction)
- [Cypress GitHub Actions Guide](https://on.cypress.io/github-actions)
- [Official Cypress GitHub Action](https://github.com/cypress-io/github-action)
- [Cypress Discord](https://discord.com/invite/cypress)

Was this helpful?

supported.
