# assetPrefix and more

# assetPrefix

> Learn how to use the assetPrefix config option to configure your CDN.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)assetPrefix

# assetPrefix

Last updated  June 16, 2025

> **Attention**: [Deploying to Vercel](https://nextjs.org/docs/app/getting-started/deploying) automatically configures a global CDN for your Next.js project.
> You do not need to manually setup an Asset Prefix.

> **Good to know**: Next.js 9.5+ added support for a customizable [Base Path](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath), which is better
> suited for hosting your application on a sub-path like `/docs`.
> We do not suggest you use a custom Asset Prefix for this use case.

## Set up a CDN

To set up a [CDN](https://en.wikipedia.org/wiki/Content_delivery_network), you can set up an asset prefix and configure your CDN's origin to resolve to the domain that Next.js is hosted on.

Open `next.config.mjs` and add the `assetPrefix` config based on the [phase](https://nextjs.org/docs/app/api-reference/config/next-config-js#async-configuration):

 next.config.mjs

```
// @ts-check
import { PHASE_DEVELOPMENT_SERVER } from 'next/constants'

export default (phase) => {
  const isDev = phase === PHASE_DEVELOPMENT_SERVER
  /**
   * @type {import('next').NextConfig}
   */
  const nextConfig = {
    assetPrefix: isDev ? undefined : 'https://cdn.mydomain.com',
  }
  return nextConfig
}
```

Next.js will automatically use your asset prefix for the JavaScript and CSS files it loads from the `/_next/` path (`.next/static/` folder). For example, with the above configuration, the following request for a JS chunk:

```
/_next/static/chunks/4b9b41aaa062cbbfeff4add70f256968c51ece5d.4d708494b3aed70c04f0.js
```

Would instead become:

```
https://cdn.mydomain.com/_next/static/chunks/4b9b41aaa062cbbfeff4add70f256968c51ece5d.4d708494b3aed70c04f0.js
```

The exact configuration for uploading your files to a given CDN will depend on your CDN of choice. The only folder you need to host on your CDN is the contents of `.next/static/`, which should be uploaded as `_next/static/` as the above URL request indicates. **Do not upload the rest of your.next/folder**, as you should not expose your server code and other configuration to the public.

While `assetPrefix` covers requests to `_next/static`, it does not influence the following paths:

- Files in the [public](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) folder; if you want to serve those assets over a CDN, you'll have to introduce the prefix yourself

Was this helpful?

supported.

---

# authInterrupts

> Learn how to enable the experimental `authInterrupts` configuration option to use `forbidden` and `unauthorized`.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)authInterrupts

# authInterrupts

This feature is currently available in the canary channel and subject to change. Try it out by  [upgrading Next.js](https://nextjs.org/docs/app/getting-started/upgrading#canary-version), and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

The `authInterrupts` configuration option allows you to use [forbidden](https://nextjs.org/docs/app/api-reference/functions/forbidden) and [unauthorized](https://nextjs.org/docs/app/api-reference/functions/unauthorized) APIs in your application. While these functions are experimental, you must enable the `authInterrupts` option in your `next.config.js` file to use them:

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

 [forbiddenAPI Reference for the forbidden function.](https://nextjs.org/docs/app/api-reference/functions/forbidden)[unauthorizedAPI Reference for the unauthorized function.](https://nextjs.org/docs/app/api-reference/functions/unauthorized)[forbidden.jsAPI reference for the forbidden.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/forbidden)[unauthorized.jsAPI reference for the unauthorized.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/unauthorized)

Was this helpful?

supported.

---

# basePath

> Use `basePath` to deploy a Next.js application under a sub-path of a domain.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)basePath

# basePath

Last updated  June 16, 2025

To deploy a Next.js application under a sub-path of a domain you can use the `basePath` config option.

`basePath` allows you to set a path prefix for the application. For example, to use `/docs` instead of `''` (an empty string, the default), open `next.config.js` and add the `basePath` config:

 next.config.js

```
module.exports = {
  basePath: '/docs',
}
```

> **Good to know**: This value must be set at build time and cannot be changed without re-building as the value is inlined in the client-side bundles.

### Links

When linking to other pages using `next/link` and `next/router` the `basePath` will be automatically applied.

For example, using `/about` will automatically become `/docs/about` when `basePath` is set to `/docs`.

```
export default function HomePage() {
  return (
    <>
      <Link href="/about">About Page</Link>
    </>
  )
}
```

Output html:

```
<a href="/docs/about">About Page</a>
```

This makes sure that you don't have to change all links in your application when changing the `basePath` value.

### Images

When using the [next/image](https://nextjs.org/docs/app/api-reference/components/image) component, you will need to add the `basePath` in front of `src`.

For example, using `/docs/me.png` will properly serve your image when `basePath` is set to `/docs`.

```
import Image from 'next/image'

function Home() {
  return (
    <>
      <h1>My Homepage</h1>
      <Image
        src="/docs/me.png"
        alt="Picture of the author"
        width={500}
        height={500}
      />
      <p>Welcome to my homepage!</p>
    </>
  )
}

export default Home
```

Was this helpful?

supported.

---

# browserDebugInfoInTerminal

> Forward browser console logs and errors to your terminal during development.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)browserDebugInfoInTerminal

# browserDebugInfoInTerminal

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  January 22, 2026

The `experimental.browserDebugInfoInTerminal` option forwards console output and runtime errors originating in the browser to the dev server terminal.

This option is disabled by default. When enabled it only works in development mode.

## Usage

Enable forwarding:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    browserDebugInfoInTerminal: true,
  },
}

export default nextConfig
```

### Serialization limits

Deeply nested objects/arrays are truncated using **sensible defaults**. You can tweak these limits:

- **depthLimit**: (optional) Limit stringification depth for nested objects/arrays. Default: 5
- **edgeLimit**: (optional) Max number of properties or elements to include per object or array. Default: 100

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    browserDebugInfoInTerminal: {
      depthLimit: 5,
      edgeLimit: 100,
    },
  },
}

export default nextConfig
```

### Source location

Source locations are included by default when this feature is enabled.

 app/page.tsx

```
'use client'

export default function Home() {
  return (
    <button
      type="button"
      onClick={() => {
        console.log('Hello World')
      }}
    >
      Click me
    </button>
  )
}
```

Clicking the button prints this message to the terminal.

 Terminal

```
[browser] Hello World (app/page.tsx:8:17)
```

To suppress them, set `showSourceLocation: false`.

- **showSourceLocation**: Include source location info when available.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    browserDebugInfoInTerminal: {
      showSourceLocation: false,
    },
  },
}

export default nextConfig
```

| Version | Changes |
| --- | --- |
| v15.4.0 | experimentalbrowserDebugInfoInTerminalintroduced |

Was this helpful?

supported.

---

# cacheComponents

> Learn how to enable the cacheComponents flag in Next.js.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)cacheComponents

# cacheComponents

Last updated  October 22, 2025

The `cacheComponents` flag is a feature in Next.js that causes data fetching operations in the App Router to be excluded from pre-renders unless they are explicitly cached. This can be useful for optimizing the performance of dynamic data fetching in Server Components.

It is useful if your application requires fresh data fetching during runtime rather than serving from a pre-rendered cache.

It is expected to be used in conjunction with [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) so that your data fetching happens at runtime by default unless you define specific parts of your application to be cached with `use cache` at the page, function, or component level.

## Usage

To enable the `cacheComponents` flag, set it to `true` in your `next.config.ts` file:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

When `cacheComponents` is enabled, you can use the following cache functions and configurations:

- The [use cachedirective](https://nextjs.org/docs/app/api-reference/directives/use-cache)
- The [cacheLifefunction](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheLife) with `use cache`
- The [cacheTagfunction](https://nextjs.org/docs/app/api-reference/functions/cacheTag)

## Notes

- While `cacheComponents` can optimize performance by ensuring fresh data fetching during runtime, it may also introduce additional latency compared to serving pre-rendered content.

## Version History

| Version | Change |
| --- | --- |
| 16.0.0 | cacheComponentsintroduced. This flag controls theppr,useCache, anddynamicIOflags as a single, unified configuration. |

Was this helpful?

supported.

---

# cacheHandlers

> Configure custom cache handlers for use cache directives in Next.js.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)cacheHandlers

# cacheHandlers

Last updated  November 18, 2025

The `cacheHandlers` configuration allows you to define custom cache storage implementations for ['use cache'](https://nextjs.org/docs/app/api-reference/directives/use-cache) and ['use cache: remote'](https://nextjs.org/docs/app/api-reference/directives/use-cache-remote). This enables you to store cached components and functions in external services or customize the caching behavior. ['use cache: private'](https://nextjs.org/docs/app/api-reference/directives/use-cache-private) is not configurable.

## When to use custom cache handlers

**Most applications don't need custom cache handlers.** The default in-memory cache works well in the typical use case.

Custom cache handlers are for advanced scenarios where you need to either share cache across multiple instances or change where the cache is stored. For example, you can configure a custom `remote` handler for external storage (like a key-value store), then use `'use cache'` in your code for in-memory caching and `'use cache: remote'` for the external storage, allowing different caching strategies within the same application.

**Sharing cache across instances**

The default in-memory cache is isolated to each Next.js process. If you're running multiple servers or containers, each instance will have its own cache that isn't shared with others and is lost on restart.

Custom handlers let you integrate with shared storage systems (like Redis, Memcached, or DynamoDB) that all your Next.js instances can access.

**Changing storage type**

You might want to store cache differently than the default in-memory approach. You can implement a custom handler to store cache on disk, in a database, or in an external caching service. Reasons include: persistence across restarts, reducing memory usage, or integrating with existing infrastructure.

## Usage

To configure custom cache handlers:

1. Define your cache handler in a separate file, see [examples](#examples) for implementation details.
2. Reference the file path in your Next config file

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheHandlers: {
    default: require.resolve('./cache-handlers/default-handler.js'),
    remote: require.resolve('./cache-handlers/remote-handler.js'),
  },
}

export default nextConfig
```

### Handler types

- **default**: Used by the `'use cache'` directive
- **remote**: Used by the `'use cache: remote'` directive

If you don't configure `cacheHandlers`, Next.js uses an in-memory LRU (Least Recently Used) cache for both `default` and `remote`. You can view the [default implementation](https://github.com/vercel/next.js/blob/canary/packages/next/src/server/lib/cache-handlers/default.ts) as a reference.

You can also define additional named handlers (e.g., `sessions`, `analytics`) and reference them with `'use cache: <name>'`.

Note that `'use cache: private'` does not use cache handlers and cannot be customized.

## API Reference

A cache handler must implement the [CacheHandler](https://github.com/vercel/next.js/blob/canary/packages/next/src/server/lib/cache-handlers/types.ts) interface with the following methods:

### get()

Retrieve a cache entry for the given cache key.

```
get(cacheKey: string, softTags: string[]): Promise<CacheEntry | undefined>
```

| Parameter | Type | Description |
| --- | --- | --- |
| cacheKey | string | The unique key for the cache entry. |
| softTags | string[] | Tags to check for staleness (used in some cache strategies). |

Returns a `CacheEntry` object if found, or `undefined` if not found or expired.

Your `get` method should retrieve the cache entry from storage, check if it has expired based on the `revalidate` time, and return `undefined` for missing or expired entries.

```
const cacheHandler = {
  async get(cacheKey, softTags) {
    const entry = cache.get(cacheKey)
    if (!entry) return undefined

    // Check if expired
    const now = Date.now()
    if (now > entry.timestamp + entry.revalidate * 1000) {
      return undefined
    }

    return entry
  },
}
```

### set()

Store a cache entry for the given cache key.

```
set(cacheKey: string, pendingEntry: Promise<CacheEntry>): Promise<void>
```

| Parameter | Type | Description |
| --- | --- | --- |
| cacheKey | string | The unique key to store the entry under. |
| pendingEntry | Promise<CacheEntry> | A promise that resolves to the cache entry. |

The entry may still be pending when this is called (i.e., its value stream may still be written to). Your handler should await the promise before processing the entry.

Returns `Promise<void>`.

Your `set` method must await the `pendingEntry` promise before storing it, since the cache entry may still be generating when this method is called. Once resolved, store the entry in your cache system.

```
const cacheHandler = {
  async set(cacheKey, pendingEntry) {
    // Wait for the entry to be ready
    const entry = await pendingEntry

    // Store in your cache system
    cache.set(cacheKey, entry)
  },
}
```

### refreshTags()

Called periodically before starting a new request to sync with external tag services.

```
refreshTags(): Promise<void>
```

This is useful if you're coordinating cache invalidation across multiple instances or services. For in-memory caches, this can be a no-op.

Returns `Promise<void>`.

For in-memory caches, this can be a no-op. For distributed caches, use this to sync tag state from an external service or database before processing requests.

```
const cacheHandler = {
  async refreshTags() {
    // For in-memory cache, no action needed
    // For distributed cache, sync tag state from external service
  },
}
```

### getExpiration()

Get the maximum revalidation timestamp for a set of tags.

```
getExpiration(tags: string[]): Promise<number>
```

| Parameter | Type | Description |
| --- | --- | --- |
| tags | string[] | Array of tags to check expiration for. |

Returns:

- `0` if none of the tags were ever revalidated
- A timestamp (in milliseconds) representing the most recent revalidation
- `Infinity` to indicate soft tags should be checked in the `get` method instead

If you're not tracking tag revalidation timestamps, return `0`. Otherwise, find the most recent revalidation timestamp across all the provided tags. Return `Infinity` if you prefer to handle soft tag checking in the `get` method.

```
const cacheHandler = {
  async getExpiration(tags) {
    // Return 0 if not tracking tag revalidation
    return 0

    // Or return the most recent revalidation timestamp
    // return Math.max(...tags.map(tag => tagTimestamps.get(tag) || 0));
  },
}
```

### updateTags()

Called when tags are revalidated or expired.

```
updateTags(tags: string[], durations?: { expire?: number }): Promise<void>
```

| Parameter | Type | Description |
| --- | --- | --- |
| tags | string[] | Array of tags to update. |
| durations | { expire?: number } | Optional expiration duration in seconds. |

Your handler should update its internal state to mark these tags as invalidated.

Returns `Promise<void>`.

When tags are revalidated, your handler should invalidate all cache entries that have any of those tags. Iterate through your cache and remove entries whose tags match the provided list.

```
const cacheHandler = {
  async updateTags(tags, durations) {
    // Invalidate all cache entries with matching tags
    for (const [key, entry] of cache.entries()) {
      if (entry.tags.some((tag) => tags.includes(tag))) {
        cache.delete(key)
      }
    }
  },
}
```

## CacheEntry Type

The [CacheEntry](https://github.com/vercel/next.js/blob/canary/packages/next/src/server/lib/cache-handlers/types.ts) object has the following structure:

```
interface CacheEntry {
  value: ReadableStream<Uint8Array>
  tags: string[]
  stale: number
  timestamp: number
  expire: number
  revalidate: number
}
```

| Property | Type | Description |
| --- | --- | --- |
| value | ReadableStream<Uint8Array> | The cached data as a stream. |
| tags | string[] | Cache tags (excluding soft tags). |
| stale | number | Duration in seconds for client-side staleness. |
| timestamp | number | When the entry was created (timestamp in milliseconds). |
| expire | number | How long the entry is allowed to be used (in seconds). |
| revalidate | number | How long until the entry should be revalidated (in seconds). |

> **Good to know**:
>
>
>
> - The `value` is a [ReadableStream](https://developer.mozilla.org/docs/Web/API/ReadableStream). Use [.tee()](https://developer.mozilla.org/docs/Web/API/ReadableStream/tee) if you need to read and store the stream data.
> - If the stream errors with partial data, your handler must decide whether to keep the partial cache or discard it.

## Examples

### Basic in-memory cache handler

Here's a minimal implementation using a `Map` for storage. This example demonstrates the core concepts, but for a production-ready implementation with LRU eviction, error handling, and tag management, see the [default cache handler](https://github.com/vercel/next.js/blob/canary/packages/next/src/server/lib/cache-handlers/default.ts).

 cache-handlers/memory-handler.js

```
const cache = new Map()
const pendingSets = new Map()

module.exports = {
  async get(cacheKey, softTags) {
    // Wait for any pending set operation to complete
    const pendingPromise = pendingSets.get(cacheKey)
    if (pendingPromise) {
      await pendingPromise
    }

    const entry = cache.get(cacheKey)
    if (!entry) {
      return undefined
    }

    // Check if entry has expired
    const now = Date.now()
    if (now > entry.timestamp + entry.revalidate * 1000) {
      return undefined
    }

    return entry
  },

  async set(cacheKey, pendingEntry) {
    // Create a promise to track this set operation
    let resolvePending
    const pendingPromise = new Promise((resolve) => {
      resolvePending = resolve
    })
    pendingSets.set(cacheKey, pendingPromise)

    try {
      // Wait for the entry to be ready
      const entry = await pendingEntry

      // Store the entry in the cache
      cache.set(cacheKey, entry)
    } finally {
      resolvePending()
      pendingSets.delete(cacheKey)
    }
  },

  async refreshTags() {
    // No-op for in-memory cache
  },

  async getExpiration(tags) {
    // Return 0 to indicate no tags have been revalidated
    return 0
  },

  async updateTags(tags, durations) {
    // Implement tag-based invalidation
    for (const [key, entry] of cache.entries()) {
      if (entry.tags.some((tag) => tags.includes(tag))) {
        cache.delete(key)
      }
    }
  },
}
```

### External storage pattern

For durable storage like Redis or a database, you'll need to serialize the cache entries. Here's a simple Redis example:

 cache-handlers/redis-handler.js

```
const { createClient } = require('redis')

const client = createClient({ url: process.env.REDIS_URL })
client.connect()

module.exports = {
  async get(cacheKey, softTags) {
    // Retrieve from Redis
    const stored = await client.get(cacheKey)
    if (!stored) return undefined

    // Deserialize the entry
    const data = JSON.parse(stored)

    // Reconstruct the ReadableStream from stored data
    return {
      value: new ReadableStream({
        start(controller) {
          controller.enqueue(Buffer.from(data.value, 'base64'))
          controller.close()
        },
      }),
      tags: data.tags,
      stale: data.stale,
      timestamp: data.timestamp,
      expire: data.expire,
      revalidate: data.revalidate,
    }
  },

  async set(cacheKey, pendingEntry) {
    const entry = await pendingEntry

    // Read the stream to get the data
    const reader = entry.value.getReader()
    const chunks = []

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        chunks.push(value)
      }
    } finally {
      reader.releaseLock()
    }

    // Combine chunks and serialize for Redis storage
    const data = Buffer.concat(chunks.map((chunk) => Buffer.from(chunk)))

    await client.set(
      cacheKey,
      JSON.stringify({
        value: data.toString('base64'),
        tags: entry.tags,
        stale: entry.stale,
        timestamp: entry.timestamp,
        expire: entry.expire,
        revalidate: entry.revalidate,
      }),
      { EX: entry.expire } // Use Redis TTL for automatic expiration
    )
  },

  async refreshTags() {
    // No-op for basic Redis implementation
    // Could sync with external tag service if needed
  },

  async getExpiration(tags) {
    // Return 0 to indicate no tags have been revalidated
    // Could query Redis for tag expiration timestamps if tracking them
    return 0
  },

  async updateTags(tags, durations) {
    // Implement tag-based invalidation if needed
    // Could iterate over keys with matching tags and delete them
  },
}
```

## Platform Support

| Deployment Option | Supported |
| --- | --- |
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | cacheHandlersintroduced. |

## Related

View related API references.[use cacheLearn how to use the "use cache" directive to cache data in your Next.js application.](https://nextjs.org/docs/app/api-reference/directives/use-cache)[use cache: remoteLearn how to use the "use cache: remote" directive for persistent, shared caching using remote cache handlers.](https://nextjs.org/docs/app/api-reference/directives/use-cache-remote)[use cache: privateLearn how to use the "use cache: private" directive to cache functions that access runtime request APIs.](https://nextjs.org/docs/app/api-reference/directives/use-cache-private)[cacheLifeLearn how to set up cacheLife configurations in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheLife)

Was this helpful?

supported.

---

# cacheLife

> Learn how to set up cacheLife configurations in Next.js.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)cacheLife

# cacheLife

Last updated  November 11, 2025

The `cacheLife` option allows you to define **custom cache profiles** when using the [cacheLife](https://nextjs.org/docs/app/api-reference/functions/cacheLife) function inside components or functions, and within the scope of the [use cachedirective](https://nextjs.org/docs/app/api-reference/directives/use-cache).

## Usage

To define a profile, enable the [cacheComponentsflag](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) and add the cache profile in the `cacheLife` object in the `next.config.js` file. For example, a `blog` profile:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
  cacheLife: {
    blog: {
      stale: 3600, // 1 hour
      revalidate: 900, // 15 minutes
      expire: 86400, // 1 day
    },
  },
}

export default nextConfig
```

You can now use this custom `blog` configuration in your component or function as follows:

 app/actions.tsJavaScriptTypeScript

```
import { cacheLife } from 'next/cache'

export async function getCachedData() {
  'use cache'
  cacheLife('blog')
  const data = await fetch('/api/data')
  return data
}
```

## Reference

The configuration object has key values with the following format:

| Property | Value | Description | Requirement |
| --- | --- | --- | --- |
| stale | number | Duration the client should cache a value without checking the server. | Optional |
| revalidate | number | Frequency at which the cache should refresh on the server; stale values may be served while revalidating. | Optional |
| expire | number | Maximum duration for which a value can remain stale before switching to dynamic. | Optional - Must be longer thanrevalidate |

## Related

View related API references.[use cacheLearn how to use the "use cache" directive to cache data in your Next.js application.](https://nextjs.org/docs/app/api-reference/directives/use-cache)[cacheHandlersConfigure custom cache handlers for use cache directives in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheHandlers)[cacheLifeLearn how to use the cacheLife function to set the cache expiration time for a cached function or component.](https://nextjs.org/docs/app/api-reference/functions/cacheLife)

Was this helpful?

supported.

---

# compress

> Next.js provides gzip compression to compress rendered content and static files, it only works with the server target. Learn more about it here.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)compress

# compress

Last updated  June 16, 2025

By default, Next.js uses `gzip` to compress rendered content and static files when using `next start` or a custom server. This is an optimization for applications that do not have compression configured. If compression is *already* configured in your application via a custom server, Next.js will not add compression.

You can check if compression is enabled and which algorithm is used by looking at the [Accept-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Encoding) (browser accepted options) and [Content-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding) (currently used) headers in the response.

## Disabling compression

To disable **compression**, set the `compress` config option to `false`:

 next.config.js

```
module.exports = {
  compress: false,
}
```

We **do not recommend disabling compression** unless you have compression configured on your server, as compression reduces bandwidth usage and improves the performance of your application. For example, you're using [nginx](https://nginx.org/) and want to switch to `brotli`, set the `compress` option to `false` to allow nginx to handle compression.

Was this helpful?

supported.

---

# crossOrigin

> Use the `crossOrigin` option to add a crossOrigin tag on the `script` tags generated by `next/script`.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)crossOrigin

# crossOrigin

Last updated  June 16, 2025

Use the `crossOrigin` option to add a [crossOriginattribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin) in all `<script>` tags generated by the [next/script](https://nextjs.org/docs/app/guides/scripts) component   , and define how cross-origin requests should be handled.

 next.config.js

```
module.exports = {
  crossOrigin: 'anonymous',
}
```

## Options

- `'anonymous'`: Adds [crossOrigin="anonymous"](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin#anonymous) attribute.
- `'use-credentials'`: Adds [crossOrigin="use-credentials"](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin#use-credentials).

Was this helpful?

supported.

---

# cssChunking

> Use the `cssChunking` option to control how CSS files are chunked in your Next.js application.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)cssChunking

# cssChunking

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

CSS Chunking is a strategy used to improve the performance of your web application by splitting and re-ordering CSS files into chunks. This allows you to load only the CSS that is needed for a specific route, instead of loading all the application's CSS at once.

You can control how CSS files are chunked using the `experimental.cssChunking` option in your `next.config.js` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig = {
  experimental: {
    cssChunking: true, // default
  },
} satisfies NextConfig

export default nextConfig
```

## Options

- **true(default)**: Next.js will try to merge CSS files whenever possible, determining explicit and implicit dependencies between files from import order to reduce the number of chunks and therefore the number of requests.
- **false**: Next.js will not attempt to merge or re-order your CSS files.
- **'strict'**: Next.js will load CSS files in the correct order they are imported into your files, which can lead to more chunks and requests.

You may consider using `'strict'` if you run into unexpected CSS behavior. For example, if you import `a.css` and `b.css` in different files using a different `import` order (`a` before `b`, or `b` before `a`), `true` will merge the files in any order and assume there are no dependencies between them. However, if `b.css` depends on `a.css`, you may want to use `'strict'` to prevent the files from being merged, and instead, load them in the order they are imported - which can result in more chunks and requests.

For most applications, we recommend `true` as it leads to fewer requests and better performance.

Was this helpful?

supported.

---

# devIndicators

> Configuration options for the on-screen indicator that gives context about the current route you're viewing during development.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)devIndicators

# devIndicators

Last updated  October 22, 2025

`devIndicators` allows you to configure the on-screen indicator that gives context about the current route you're viewing during development.

 Types

```
devIndicators: false | {
    position?: 'bottom-right'
    | 'bottom-left'
    | 'top-right'
    | 'top-left', // defaults to 'bottom-left',
  },
```

Setting `devIndicators` to `false` will hide the indicator, however Next.js will continue to surface any build or runtime errors that were encountered.

## Troubleshooting

### Indicator not marking a route as static

If you expect a route to be static and the indicator has marked it as dynamic, it's likely the route has opted out of static rendering.

You can confirm if a route is [static](https://nextjs.org/docs/app/guides/caching#static-rendering) or [dynamic](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) by building your application using `next build --debug`, and checking the output in your terminal. Static (or prerendered) routes will display a `○` symbol, whereas dynamic routes will display a `ƒ` symbol. For example:

 Build Output

```
Route (app)
┌ ○ /_not-found
└ ƒ /products/[id]

○  (Static)   prerendered as static content
ƒ  (Dynamic)  server-rendered on demand
```

There are two reasons a route might opt out of static rendering:

- The presence of [Dynamic APIs](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) which rely on runtime information.
- An [uncached data request](https://nextjs.org/docs/app/getting-started/fetching-data), like a call to an ORM or database driver.

Check your route for any of these conditions, and if you are not able to statically render the route, then consider using [loading.js](https://nextjs.org/docs/app/api-reference/file-conventions/loading) or [<Suspense />](https://react.dev/reference/react/Suspense) to leverage [streaming](https://nextjs.org/docs/app/getting-started/linking-and-navigating#streaming).

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | appIsrStatus,buildActivity, andbuildActivityPositionoptions have been removed. |
| v15.2.0 | Improved on-screen indicator with newpositionoption.appIsrStatus,buildActivity, andbuildActivityPositionoptions have been deprecated. |
| v15.0.0 | Static on-screen indicator added withappIsrStatusoption. |

Was this helpful?

supported.

---

# distDir

> Set a custom build directory to use instead of the default .next directory.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)distDir

# distDir

Last updated  June 16, 2025

You can specify a name to use for a custom build directory to use instead of `.next`.

Open `next.config.js` and add the `distDir` config:

 next.config.js

```
module.exports = {
  distDir: 'build',
}
```

Now if you run `next build` Next.js will use `build` instead of the default `.next` folder.

> `distDir` **should not** leave your project directory. For example, `../build` is an **invalid** directory.

Was this helpful?

supported.

---

# env

> Learn to add and access environment variables in your Next.js application at build time.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)env

# env

This is a legacy API and no longer recommended. It's still supported for backward compatibility.Last updated  June 16, 2025

> Since the release of [Next.js 9.4](https://nextjs.org/blog/next-9-4) we now have a more intuitive and ergonomic experience for [adding environment variables](https://nextjs.org/docs/app/guides/environment-variables). Give it a try!

> **Good to know**: environment variables specified in this way will **always** be included in the JavaScript bundle, prefixing the environment variable name with `NEXT_PUBLIC_` only has an effect when specifying them [through the environment or .env files](https://nextjs.org/docs/app/guides/environment-variables).

To add environment variables to the JavaScript bundle, open `next.config.js` and add the `env` config:

 next.config.js

```
module.exports = {
  env: {
    customKey: 'my-value',
  },
}
```

Now you can access `process.env.customKey` in your code. For example:

```
function Page() {
  return <h1>The value of customKey is: {process.env.customKey}</h1>
}

export default Page
```

Next.js will replace `process.env.customKey` with `'my-value'` at build time. Trying to destructure `process.env` variables won't work due to the nature of webpack [DefinePlugin](https://webpack.js.org/plugins/define-plugin/).

For example, the following line:

```
return <h1>The value of customKey is: {process.env.customKey}</h1>
```

Will end up being:

```
return <h1>The value of customKey is: {'my-value'}</h1>
```

Was this helpful?

supported.

---

# expireTime

> Customize stale-while-revalidate expire time for ISR enabled pages.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)expireTime

# expireTime

Last updated  June 16, 2025

You can specify a custom `stale-while-revalidate` expire time for CDNs to consume in the `Cache-Control` header for ISR enabled pages.

Open `next.config.js` and add the `expireTime` config:

 next.config.js

```
module.exports = {
  // one hour in seconds
  expireTime: 3600,
}
```

Now when sending the `Cache-Control` header the expire time will be calculated depending on the specific revalidate period.

For example, if you have a revalidate of 15 minutes on a path and the expire time is one hour the generated `Cache-Control` header will be `s-maxage=900, stale-while-revalidate=2700` so that it can stay stale for 15 minutes less than the configured expire time.

Was this helpful?

supported.

---

# exportPathMap

> Customize the pages that will be exported as HTML files when using `next export`.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)exportPathMap

# exportPathMap

This is a legacy API and no longer recommended. It's still supported for backward compatibility.Last updated  June 16, 2025

> This feature is exclusive to `next export` and currently **deprecated** in favor of `getStaticPaths` with `pages` or `generateStaticParams` with `app`.

`exportPathMap` allows you to specify a mapping of request paths to page destinations, to be used during export. Paths defined in `exportPathMap` will also be available when using [next dev](https://nextjs.org/docs/app/api-reference/cli/next#next-dev-options).

Let's start with an example, to create a custom `exportPathMap` for an app with the following pages:

- `pages/index.js`
- `pages/about.js`
- `pages/post.js`

Open `next.config.js` and add the following `exportPathMap` config:

 next.config.js

```
module.exports = {
  exportPathMap: async function (
    defaultPathMap,
    { dev, dir, outDir, distDir, buildId }
  ) {
    return {
      '/': { page: '/' },
      '/about': { page: '/about' },
      '/p/hello-nextjs': { page: '/post', query: { title: 'hello-nextjs' } },
      '/p/learn-nextjs': { page: '/post', query: { title: 'learn-nextjs' } },
      '/p/deploy-nextjs': { page: '/post', query: { title: 'deploy-nextjs' } },
    }
  },
}
```

> **Good to know**: the `query` field in `exportPathMap` cannot be used with [automatically statically optimized pages](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization) or [getStaticPropspages](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) as they are rendered to HTML files at build-time and additional query information cannot be provided during `next export`.

The pages will then be exported as HTML files, for example, `/about` will become `/about.html`.

`exportPathMap` is an `async` function that receives 2 arguments: the first one is `defaultPathMap`, which is the default map used by Next.js. The second argument is an object with:

- `dev` - `true` when `exportPathMap` is being called in development. `false` when running `next export`. In development `exportPathMap` is used to define routes.
- `dir` - Absolute path to the project directory
- `outDir` - Absolute path to the `out/` directory ([configurable with-o](#customizing-the-output-directory)). When `dev` is `true` the value of `outDir` will be `null`.
- `distDir` - Absolute path to the `.next/` directory (configurable with the [distDir](https://nextjs.org/docs/pages/api-reference/config/next-config-js/distDir) config)
- `buildId` - The generated build id

The returned object is a map of pages where the `key` is the `pathname` and the `value` is an object that accepts the following fields:

- `page`: `String` - the page inside the `pages` directory to render
- `query`: `Object` - the `query` object passed to `getInitialProps` when prerendering. Defaults to `{}`

> The exported `pathname` can also be a filename (for example, `/readme.md`), but you may need to set the `Content-Type` header to `text/html` when serving its content if it is different than `.html`.

## Adding a trailing slash

It is possible to configure Next.js to export pages as `index.html` files and require trailing slashes, `/about` becomes `/about/index.html` and is routable via `/about/`. This was the default behavior prior to Next.js 9.

To switch back and add a trailing slash, open `next.config.js` and enable the `trailingSlash` config:

 next.config.js

```
module.exports = {
  trailingSlash: true,
}
```

## Customizing the output directory

[next export](https://nextjs.org/docs/app/guides/static-exports) will use `out` as the default output directory, you can customize this using the `-o` argument, like so:

   Terminal

```
next export -o outdir
```

> **Warning**: Using `exportPathMap` is deprecated and is overridden by `getStaticPaths` inside `pages`. We don't recommend using them together.

Was this helpful?

supported.

---

# generateBuildId

> Configure the build id, which is used to identify the current build in which your application is being served.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)generateBuildId

# generateBuildId

Last updated  June 16, 2025

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

Was this helpful?

supported.

---

# generateEtags

> Next.js will generate etags for every page by default. Learn more about how to disable etag generation here.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)generateEtags

# generateEtags

Last updated  June 16, 2025

Next.js will generate [etags](https://en.wikipedia.org/wiki/HTTP_ETag) for every page by default. You may want to disable etag generation for HTML pages depending on your cache strategy.

Open `next.config.js` and disable the `generateEtags` option:

 next.config.js

```
module.exports = {
  generateEtags: false,
}
```

Was this helpful?

supported.
