# How to handle redirects in Next.js and more

# How to handle redirects in Next.js

> Learn the different ways to handle redirects in Next.js.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)RedirectingYou are currently viewing the documentation for Pages Router.

# How to handle redirects in Next.js

Last updated  May 27, 2025

There are a few ways you can handle redirects in Next.js. This page will go through each available option, use cases, and how to manage large numbers of redirects.

| API | Purpose | Where | Status Code |
| --- | --- | --- | --- |
| useRouter | Perform a client-side navigation | Components | N/A |
| redirectsinnext.config.js | Redirect an incoming request based on a path | next.config.jsfile | 307 (Temporary) or 308 (Permanent) |
| NextResponse.redirect | Redirect an incoming request based on a condition | Proxy | Any |

## useRouter()hook

If you need to redirect inside a component, you can use the `push` method from the `useRouter` hook. For example:

app/page.tsxJavaScriptTypeScript

```
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()

  return (
    <button type="button" onClick={() => router.push('/dashboard')}>
      Dashboard
    </button>
  )
}
```

> **Good to know**:
>
>
>
> - If you don't need to programmatically navigate a user, you should use a [<Link>](https://nextjs.org/docs/app/api-reference/components/link) component.

See the [useRouterAPI reference](https://nextjs.org/docs/pages/api-reference/functions/use-router) for more information.

## redirectsinnext.config.js

The `redirects` option in the `next.config.js` file allows you to redirect an incoming request path to a different destination path. This is useful when you change the URL structure of pages or have a list of redirects that are known ahead of time.

`redirects` supports [path](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects#path-matching), [header, cookie, and query matching](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects#header-cookie-and-query-matching), giving you the flexibility to redirect users based on an incoming request.

To use `redirects`, add the option to your `next.config.js` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  async redirects() {
    return [
      // Basic redirect
      {
        source: '/about',
        destination: '/',
        permanent: true,
      },
      // Wildcard path matching
      {
        source: '/blog/:slug',
        destination: '/news/:slug',
        permanent: true,
      },
    ]
  },
}

export default nextConfig
```

See the [redirectsAPI reference](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects) for more information.

> **Good to know**:
>
>
>
> - `redirects` can return a 307 (Temporary Redirect) or 308 (Permanent Redirect) status code with the `permanent` option.
> - `redirects` may have a limit on platforms. For example, on Vercel, there's a limit of 1,024 redirects. To manage a large number of redirects (1000+), consider creating a custom solution using [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy). See [managing redirects at scale](#managing-redirects-at-scale-advanced) for more.
> - `redirects` runs **before** Proxy.

## NextResponse.redirectin Proxy

Proxy allows you to run code before a request is completed. Then, based on the incoming request, redirect to a different URL using `NextResponse.redirect`. This is useful if you want to redirect users based on a condition (e.g. authentication, session management, etc) or have [a large number of redirects](#managing-redirects-at-scale-advanced).

For example, to redirect the user to a `/login` page if they are not authenticated:

 proxy.tsJavaScriptTypeScript

```
import { NextResponse, NextRequest } from 'next/server'
import { authenticate } from 'auth-provider'

export function proxy(request: NextRequest) {
  const isAuthenticated = authenticate(request)

  // If the user is authenticated, continue as normal
  if (isAuthenticated) {
    return NextResponse.next()
  }

  // Redirect to login page if not authenticated
  return NextResponse.redirect(new URL('/login', request.url))
}

export const config = {
  matcher: '/dashboard/:path*',
}
```

> **Good to know**:
>
>
>
> - Proxy runs **after** `redirects` in `next.config.js` and **before** rendering.

See the [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) documentation for more information.

## Managing redirects at scale (advanced)

To manage a large number of redirects (1000+), you may consider creating a custom solution using Proxy. This allows you to handle redirects programmatically without having to redeploy your application.

To do this, you'll need to consider:

1. Creating and storing a redirect map.
2. Optimizing data lookup performance.

> **Next.js Example**: See our [Proxy with Bloom filter](https://redirects-bloom-filter.vercel.app/) example for an implementation of the recommendations below.

### 1. Creating and storing a redirect map

A redirect map is a list of redirects that you can store in a database (usually a key-value store) or JSON file.

Consider the following data structure:

```
{
  "/old": {
    "destination": "/new",
    "permanent": true
  },
  "/blog/post-old": {
    "destination": "/blog/post-new",
    "permanent": true
  }
}
```

In [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy), you can read from a database such as Vercel's [Edge Config](https://vercel.com/docs/edge-config/get-started) or [Redis](https://vercel.com/docs/redis), and redirect the user based on the incoming request:

 proxy.tsJavaScriptTypeScript

```
import { NextResponse, NextRequest } from 'next/server'
import { get } from '@vercel/edge-config'

type RedirectEntry = {
  destination: string
  permanent: boolean
}

export async function proxy(request: NextRequest) {
  const pathname = request.nextUrl.pathname
  const redirectData = await get(pathname)

  if (redirectData && typeof redirectData === 'string') {
    const redirectEntry: RedirectEntry = JSON.parse(redirectData)
    const statusCode = redirectEntry.permanent ? 308 : 307
    return NextResponse.redirect(redirectEntry.destination, statusCode)
  }

  // No redirect found, continue without redirecting
  return NextResponse.next()
}
```

### 2. Optimizing data lookup performance

Reading a large dataset for every incoming request can be slow and expensive. There are two ways you can optimize data lookup performance:

- Use a database that is optimized for fast reads
- Use a data lookup strategy such as a [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) to efficiently check if a redirect exists **before** reading the larger redirects file or database.

Considering the previous example, you can import a generated bloom filter file into Proxy, then, check if the incoming request pathname exists in the bloom filter.

If it does, forward the request to a   [API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) which will check the actual file and redirect the user to the appropriate URL. This avoids importing a large redirects file into Proxy, which can slow down every incoming request.

 proxy.tsJavaScriptTypeScript

```
import { NextResponse, NextRequest } from 'next/server'
import { ScalableBloomFilter } from 'bloom-filters'
import GeneratedBloomFilter from './redirects/bloom-filter.json'

type RedirectEntry = {
  destination: string
  permanent: boolean
}

// Initialize bloom filter from a generated JSON file
const bloomFilter = ScalableBloomFilter.fromJSON(GeneratedBloomFilter as any)

export async function proxy(request: NextRequest) {
  // Get the path for the incoming request
  const pathname = request.nextUrl.pathname

  // Check if the path is in the bloom filter
  if (bloomFilter.has(pathname)) {
    // Forward the pathname to the Route Handler
    const api = new URL(
      `/api/redirects?pathname=${encodeURIComponent(request.nextUrl.pathname)}`,
      request.nextUrl.origin
    )

    try {
      // Fetch redirect data from the Route Handler
      const redirectData = await fetch(api)

      if (redirectData.ok) {
        const redirectEntry: RedirectEntry | undefined =
          await redirectData.json()

        if (redirectEntry) {
          // Determine the status code
          const statusCode = redirectEntry.permanent ? 308 : 307

          // Redirect to the destination
          return NextResponse.redirect(redirectEntry.destination, statusCode)
        }
      }
    } catch (error) {
      console.error(error)
    }
  }

  // No redirect found, continue the request without redirecting
  return NextResponse.next()
}
```

Then, in the API Route:

pages/api/redirects.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'
import redirects from '@/app/redirects/redirects.json'

type RedirectEntry = {
  destination: string
  permanent: boolean
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const pathname = req.query.pathname
  if (!pathname) {
    return res.status(400).json({ message: 'Bad Request' })
  }

  // Get the redirect entry from the redirects.json file
  const redirect = (redirects as Record<string, RedirectEntry>)[pathname]

  // Account for bloom filter false positives
  if (!redirect) {
    return res.status(400).json({ message: 'No redirect' })
  }

  // Return the redirect entry
  return res.json(redirect)
}
```

> **Good to know:**
>
>
>
> - To generate a bloom filter, you can use a library like [bloom-filters](https://www.npmjs.com/package/bloom-filters).
> - You should validate requests made to your Route Handler to prevent malicious requests.

Was this helpful?

supported.

---

# How to use Sass in Next.js

> Learn how to use Sass in your Next.js application.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)SassYou are currently viewing the documentation for Pages Router.

# How to use Sass in Next.js

Last updated  April 25, 2025

Next.js has built-in support for integrating with Sass after the package is installed using both the `.scss` and `.sass` extensions. You can use component-level Sass via CSS Modules and the `.module.scss`or `.module.sass` extension.

First, install [sass](https://github.com/sass/sass):

 Terminal

```
npm install --save-dev sass
```

> **Good to know**:
>
>
>
> Sass supports [two different syntaxes](https://sass-lang.com/documentation/syntax), each with their own extension.
> The `.scss` extension requires you use the [SCSS syntax](https://sass-lang.com/documentation/syntax#scss),
> while the `.sass` extension requires you use the [Indented Syntax ("Sass")](https://sass-lang.com/documentation/syntax#the-indented-syntax).
>
>
>
> If you're not sure which to choose, start with the `.scss` extension which is a superset of CSS, and doesn't require you learn the
> Indented Syntax ("Sass").

### Customizing Sass Options

If you want to configure your Sass options, use `sassOptions` in `next.config`.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  sassOptions: {
    additionalData: `$var: red;`,
  },
}

export default nextConfig
```

#### Implementation

You can use the `implementation` property to specify the Sass implementation to use. By default, Next.js uses the [sass](https://www.npmjs.com/package/sass) package.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  sassOptions: {
    implementation: 'sass-embedded',
  },
}

export default nextConfig
```

### Sass Variables

Next.js supports Sass variables exported from CSS Module files.

For example, using the exported `primaryColor` Sass variable:

 app/variables.module.scss

```
$primary-color: #64ff00;

:export {
  primaryColor: $primary-color;
}
```

   pages/_app.js

```
import variables from '../styles/variables.module.scss'

export default function MyApp({ Component, pageProps }) {
  return (
    <Layout color={variables.primaryColor}>
      <Component {...pageProps} />
    </Layout>
  )
}
```

Was this helpful?

supported.

---

# How to load and optimize scripts

> Optimize 3rd party scripts with the built-in Script component.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)ScriptsYou are currently viewing the documentation for Pages Router.

# How to load and optimize scripts

Last updated  April 24, 2025

### Application Scripts

To load a third-party script for all routes, import `next/script` and include the script directly in your custom `_app`:

pages/_app.js

```
import Script from 'next/script'

export default function MyApp({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      <Script src="https://example.com/script.js" />
    </>
  )
}
```

This script will load and execute when *any* route in your application is accessed. Next.js will ensure the script will **only load once**, even if a user navigates between multiple pages.

> **Recommendation**: We recommend only including third-party scripts in specific pages or layouts in order to minimize any unnecessary impact to performance.

### Strategy

Although the default behavior of `next/script` allows you to load third-party scripts in any page or layout, you can fine-tune its loading behavior by using the `strategy` property:

- `beforeInteractive`: Load the script before any Next.js code and before any page hydration occurs.
- `afterInteractive`: (**default**) Load the script early but after some hydration on the page occurs.
- `lazyOnload`: Load the script later during browser idle time.
- `worker`: (experimental) Load the script in a web worker.

Refer to the [next/script](https://nextjs.org/docs/app/api-reference/components/script#strategy) API reference documentation to learn more about each strategy and their use cases.

### Offloading Scripts To A Web Worker (experimental)

> **Warning:** The `worker` strategy is not yet stable and does not yet work with the App Router. Use with caution.

Scripts that use the `worker` strategy are offloaded and executed in a web worker with [Partytown](https://partytown.qwik.dev/). This can improve the performance of your site by dedicating the main thread to the rest of your application code.

This strategy is still experimental and can only be used if the `nextScriptWorkers` flag is enabled in `next.config.js`:

 next.config.js

```
module.exports = {
  experimental: {
    nextScriptWorkers: true,
  },
}
```

Then, run `next` (normally `npm run dev` or `yarn dev`) and Next.js will guide you through the installation of the required packages to finish the setup:

 Terminal

```
npm run dev
```

You'll see instructions like these: Please install Partytown by running `npm install @qwik.dev/partytown`

Once setup is complete, defining `strategy="worker"` will automatically instantiate Partytown in your application and offload the script to a web worker.

 pages/home.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function Home() {
  return (
    <>
      <Script src="https://example.com/script.js" strategy="worker" />
    </>
  )
}
```

There are a number of trade-offs that need to be considered when loading a third-party script in a web worker. Please see Partytown's [tradeoffs](https://partytown.qwik.dev/trade-offs) documentation for more information.

#### Using custom Partytown configuration

Although the `worker` strategy does not require any additional configuration to work, Partytown supports the use of a config object to modify some of its settings, including enabling `debug` mode and forwarding events and triggers.

If you would like to add additional configuration options, you can include it within the `<Head />` component used in a [custom_document.js](https://nextjs.org/docs/pages/building-your-application/routing/custom-document):

_pages/document.jsx

```
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html>
      <Head>
        <script
          data-partytown-config
          dangerouslySetInnerHTML={{
            __html: `
              partytown = {
                lib: "/_next/static/~partytown/",
                debug: true
              };
            `,
          }}
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

In order to modify Partytown's configuration, the following conditions must be met:

1. The `data-partytown-config` attribute must be used in order to overwrite the default configuration used by Next.js
2. Unless you decide to save Partytown's library files in a separate directory, the `lib: "/_next/static/~partytown/"` property and value must be included in the configuration object in order to let Partytown know where Next.js stores the necessary static files.

> **Note**: If you are using an [asset prefix](https://nextjs.org/docs/pages/api-reference/config/next-config-js/assetPrefix) and would like to modify Partytown's default configuration, you must include it as part of the `lib` path.

Take a look at Partytown's [configuration options](https://partytown.qwik.dev/configuration) to see the full list of other properties that can be added.

### Inline Scripts

Inline scripts, or scripts not loaded from an external file, are also supported by the Script component. They can be written by placing the JavaScript within curly braces:

```
<Script id="show-banner">
  {`document.getElementById('banner').classList.remove('hidden')`}
</Script>
```

Or by using the `dangerouslySetInnerHTML` property:

```
<Script
  id="show-banner"
  dangerouslySetInnerHTML={{
    __html: `document.getElementById('banner').classList.remove('hidden')`,
  }}
/>
```

> **Warning**: An `id` property must be assigned for inline scripts in order for Next.js to track and optimize the script.

### Executing Additional Code

Event handlers can be used with the Script component to execute additional code after a certain event occurs:

- `onLoad`: Execute code after the script has finished loading.
- `onReady`: Execute code after the script has finished loading and every time the component is mounted.
- `onError`: Execute code if the script fails to load.

These handlers will only work when `next/script` is imported and used inside of a [Client Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) where `"use client"` is defined as the first line of code:

pages/index.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script
        src="https://example.com/script.js"
        onLoad={() => {
          console.log('Script has loaded')
        }}
      />
    </>
  )
}
```

Refer to the [next/script](https://nextjs.org/docs/pages/api-reference/components/script#onload) API reference to learn more about each event handler and view examples.

### Additional Attributes

There are many DOM attributes that can be assigned to a `<script>` element that are not used by the Script component, like [nonce](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/nonce) or [custom data attributes](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/data-*). Including any additional attributes will automatically forward it to the final, optimized `<script>` element that is included in the HTML.

   pages/index.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script
        src="https://example.com/script.js"
        id="example-script"
        nonce="XUENAJFW"
        data-test="script"
      />
    </>
  )
}
```

Was this helpful?

supported.

---

# How to self

> Learn how to self-host your Next.js application on a Node.js server, Docker image, or static HTML files (static exports).

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Self-HostingYou are currently viewing the documentation for Pages Router.

# How to self-host your Next.js application

Last updated  April 22, 2025

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

To read runtime environment variables, we recommend using `getServerSideProps` or [incrementally adopting the App Router](https://nextjs.org/docs/app/guides/migrating/app-router-migration).

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

## Manual Graceful Shutdowns

When self-hosting, you might want to run code when the server shuts down on `SIGTERM` or `SIGINT` signals.

You can set the env variable `NEXT_MANUAL_SIG_HANDLE` to `true` and then register a handler for that signal inside your `_document.js` file. You will need to register the environment variable directly in the `package.json` script, and not in the `.env` file.

> **Good to know**: Manual signal handling is not available in `next dev`.

package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "NEXT_MANUAL_SIG_HANDLE=true next start"
  }
}
```

pages/_document.js

```
if (process.env.NEXT_MANUAL_SIG_HANDLE) {
  process.on('SIGTERM', () => {
    console.log('Received SIGTERM: cleaning up')
    process.exit(0)
  })
  process.on('SIGINT', () => {
    console.log('Received SIGINT: cleaning up')
    process.exit(0)
  })
}
```

Was this helpful?

supported.

---

# How to create a static export of your Next.js application

> Next.js enables starting as a static site or Single-Page Application (SPA), then later optionally upgrading to use features that require a server.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Static ExportsYou are currently viewing the documentation for Pages Router.

# How to create a static export of your Next.js application

Last updated  May 12, 2025

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

You can utilize [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) and [getStaticPaths](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-paths) to generate an HTML file for each page in your `pages` directory (or more for [dynamic routes](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes)).

## Supported Features

The majority of core Next.js features needed to build a static site are supported, including:

- [Dynamic Routes when usinggetStaticPaths](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes)
- Prefetching with `next/link`
- Preloading JavaScript
- [Dynamic Imports](https://nextjs.org/docs/pages/guides/lazy-loading)
- Any styling options (e.g. CSS Modules, styled-jsx)
- [Client-side data fetching](https://nextjs.org/docs/pages/building-your-application/data-fetching/client-side)
- [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props)
- [getStaticPaths](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-paths)

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

## Unsupported Features

Features that require a Node.js server, or dynamic logic that cannot be computed during the build process, are **not** supported:

- [Internationalized Routing](https://nextjs.org/docs/pages/guides/internationalization)
- [API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes)
- [Rewrites](https://nextjs.org/docs/pages/api-reference/config/next-config-js/rewrites)
- [Redirects](https://nextjs.org/docs/pages/api-reference/config/next-config-js/redirects)
- [Headers](https://nextjs.org/docs/pages/api-reference/config/next-config-js/headers)
- [Proxy](https://nextjs.org/docs/pages/api-reference/file-conventions/proxy)
- [Incremental Static Regeneration](https://nextjs.org/docs/pages/guides/incremental-static-regeneration)
- [Image Optimization](https://nextjs.org/docs/pages/api-reference/components/image) with the default `loader`
- [Draft Mode](https://nextjs.org/docs/pages/guides/draft-mode)
- [getStaticPathswithfallback: true](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-true)
- [getStaticPathswithfallback: 'blocking'](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-blocking)
- [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props)

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

# Tailwind CSS

> Style your Next.js Application using Tailwind CSS.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Tailwind CSSYou are currently viewing the documentation for Pages Router.

# Tailwind CSS

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
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Add the Tailwind directives to your global CSS file:

styles/globals.css

```
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Import the CSS file in your `pages/_app.js` file:

pages/_app.js

```
import '@/styles/globals.css'

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}
```

## Using classes

After installing Tailwind CSS and adding the global styles, you can use Tailwind's utility classes in your application.

   pages/index.tsxJavaScriptTypeScript

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

> Learn how to set up Next.js with Cypress for End-to-End (E2E) and Component Testing.

[Guides](https://nextjs.org/docs/pages/guides)[Testing](https://nextjs.org/docs/pages/guides/testing)CypressYou are currently viewing the documentation for Pages Router.

# How to set up Cypress with Next.js

Last updated  April 24, 2025

[Cypress](https://www.cypress.io/) is a test runner used for **End-to-End (E2E)** and **Component Testing**. This page will show you how to set up Cypress with Next.js and write your first tests.

> **Warning:**
>
>
>
> - Cypress versions below 13.6.3 do not support [TypeScript version 5](https://github.com/cypress-io/cypress/issues/27731) with `moduleResolution:"bundler"`. However, this issue has been resolved in Cypress version 13.6.3 and later. [cypress v13.6.3](https://docs.cypress.io/guides/references/changelog#13-6-3)

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

   pages/index.js

```
import Link from 'next/link'

export default function Home() {
  return (
    <div>
      <h1>Home</h1>
      <Link href="/about">About</Link>
    </div>
  )
}
```

pages/about.js

```
import Link from 'next/link'

export default function About() {
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

   cypress/component/about.cy.js

```
import AboutPage from '../../pages/about'

describe('<AboutPage />', () => {
  it('should render and display expected content', () => {
    // Mount the React component for the About page
    cy.mount(<AboutPage />)

    // The new page should contain an h1 with "About page"
    cy.get('h1').contains('About')

    // Validate that a link with the expected URL is present
    // *Following* the link is better suited to an E2E test
    cy.get('a[href="/"]').should('be.visible')
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
