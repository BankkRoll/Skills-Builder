# use cache and more

# use cache

> Learn how to use the "use cache" directive to cache data in your Next.js application.

[API Reference](https://nextjs.org/docs/app/api-reference)[Directives](https://nextjs.org/docs/app/api-reference/directives)use cache

# use cache

Last updated  January 26, 2026

The `use cache` directive allows you to mark a route, React component, or a function as cacheable. It can be used at the top of a file to indicate that all exports in the file should be cached, or inline at the top of function or component to cache the return value.

> **Good to know:**
>
>
>
> - To use cookies or headers, read them outside cached scopes and pass values as arguments. This is the preferred pattern.
> - If the in-memory cache isn't sufficient for runtime data, ['use cache: remote'](https://nextjs.org/docs/app/api-reference/directives/use-cache-remote) allows platforms to provide a dedicated cache handler, though it requires a network roundtrip to check the cache and typically incurs platform fees.
> - For compliance requirements or when you can't refactor to pass runtime data as arguments to a `use cache` scope, see ['use cache: private'](https://nextjs.org/docs/app/api-reference/directives/use-cache-private).

## Usage

`use cache` is a Cache Components feature. To enable it, add the [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) option to your `next.config.ts` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

Then, add `use cache` at the file, component, or function level:

```
// File level
'use cache'

export default async function Page() {
  // ...
}

// Component level
export async function MyComponent() {
  'use cache'
  return <></>
}

// Function level
export async function getData() {
  'use cache'
  const data = await fetch('/api/data')
  return data
}
```

> **Good to know**: When used at file level, all function exports must be async functions.

## Howuse cacheworks

### Cache keys

A cache entry's key is generated using a serialized version of its inputs, which includes:

1. **Build ID** - Unique per build, changing this invalidates all cache entries
2. **Function ID** - A secure hash of the function's location and signature in the codebase
3. **Serializable arguments** - Props (for components) or function arguments
4. **HMR refresh hash** (development only) - Invalidates cache on hot module replacement

When a cached function references variables from outer scopes, those variables are automatically captured and bound as arguments, making them part of the cache key.

 lib/data.ts

```
async function Component({ userId }: { userId: string }) {
  const getData = async (filter: string) => {
    'use cache'
    // Cache key includes both userId (from closure) and filter (argument)
    return fetch(`/api/users/${userId}/data?filter=${filter}`)
  }

  return getData('active')
}
```

In the snippet above, `userId` is captured from the outer scope and `filter` is passed as an argument, so both become part of the `getData` function's cache key. This means different user and filter combinations will have separate cache entries.

## Serialization

Arguments to cached functions and their return values must be serializable.

For a complete reference, see:

- [Serializable arguments](https://react.dev/reference/rsc/use-server#serializable-parameters-and-return-values) - Uses **React Server Components** serialization
- [Serializable return types](https://react.dev/reference/rsc/use-client#serializable-types) - Uses **React Client Components** serialization

> **Good to know:** Arguments and return values use different serialization systems. Server Component serialization (for arguments) is more restrictive than Client Component serialization (for return values). This means you can return JSX elements but cannot accept them as arguments unless using pass-through patterns.

### Supported types

**Arguments:**

- Primitives: `string`, `number`, `boolean`, `null`, `undefined`
- Plain objects: `{ key: value }`
- Arrays: `[1, 2, 3]`
- Dates, Maps, Sets, TypedArrays, ArrayBuffers
- React elements (as pass-through only)

**Return values:**

- Same as arguments, plus JSX elements

### Unsupported types

- Class instances
- Functions (except as pass-through)
- Symbols, WeakMaps, WeakSets
- URL instances

 app/components/user-card.tsx

```
// Valid - primitives and plain objects
async function UserCard({
  id,
  config,
}: {
  id: string
  config: { theme: string }
}) {
  'use cache'
  return <div>{id}</div>
}

// Invalid - class instance
async function UserProfile({ user }: { user: UserClass }) {
  'use cache'
  // Error: Cannot serialize class instance
  return <div>{user.name}</div>
}
```

### Pass-through (non-serializable arguments)

You can accept non-serializable values **as long as you don't introspect them**. This enables composition patterns with `children` and Server Actions:

 app/components/cached-wrapper.tsx

```
async function CachedWrapper({ children }: { children: ReactNode }) {
  'use cache'
  // Don't read or modify children - just pass it through
  return (
    <div className="wrapper">
      <header>Cached Header</header>
      {children}
    </div>
  )
}

// Usage: children can be dynamic
export default function Page() {
  return (
    <CachedWrapper>
      <DynamicComponent /> {/* Not cached, passed through */}
    </CachedWrapper>
  )
}
```

You can also pass Server Actions through cached components:

 app/components/cached-form.tsx

```
async function CachedForm({ action }: { action: () => Promise<void> }) {
  'use cache'
  // Don't call action here - just pass it through
  return <form action={action}>{/* ... */}</form>
}
```

## Constraints

Cached functions execute in an isolated environment. The following constraints ensure cache behavior remains predictable and secure.

### Runtime APIs

Cached functions and components **cannot** directly access runtime APIs like `cookies()`, `headers()`, or `searchParams`. Instead, read these values outside the cached scope and pass them as arguments.

### Runtime caching considerations

While `use cache` is designed primarily to include dynamic data in the static shell, it can also cache data at runtime using in-memory LRU (Least Recently Used) storage.

Runtime cache behavior depends on your hosting environment:

| Environment | Runtime Caching Behavior |
| --- | --- |
| Serverless | Cache entries typically don't persist across requests (each request can be a different instance). Build-time caching works normally. |
| Self-hosted | Cache entries persist across requests. Control cache size withcacheMaxMemorySize. |

If the default in-memory cache isn't enough, consider **use cache: remote** which allows platforms to provide a dedicated cache handler (like Redis or KV database). This helps reduce hits against data sources not scaled to your total traffic, though it comes with costs (storage, network latency, platform fees).

Very rarely, for compliance requirements or when you can't refactor your code to pass runtime data as arguments to a `use cache` scope, you might need [use cache: private](https://nextjs.org/docs/app/api-reference/directives/use-cache-private).

### React.cache isolation

[React.cache](https://react.dev/reference/react/cache) operates in an isolated scope inside `use cache` boundaries. Values stored via `React.cache` outside a `use cache` function are not visible inside it.

This means you cannot use `React.cache` to pass data into a `use cache` scope:

```
import { cache } from 'react'

const store = cache(() => ({ current: null as string | null }))

function Parent() {
  const shared = store()
  shared.current = 'value from parent'
  return <Child />
}

async function Child() {
  'use cache'
  const shared = store()
  // shared.current is null, not 'value from parent'
  // use cache has its own isolated React.cache scope
  return <div>{shared.current}</div>
}
```

This isolation ensures cached functions have predictable, self-contained behavior. To pass data into a `use cache` scope, use function arguments instead.

## use cacheat runtime

On the **server**, cache entries are stored in-memory and respect the `revalidate` and `expire` times from your `cacheLife` configuration. You can customize the cache storage by configuring [cacheHandlers](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheHandlers) in your `next.config.js` file.

On the **client**, content from the server cache is stored in the browser's memory for the duration defined by the `stale` time. The client router enforces a **minimum 30-second stale time**, regardless of configuration.

The `x-nextjs-stale-time` response header communicates cache lifetime from server to client, ensuring coordinated behavior.

## Revalidation

By default, `use cache` uses the `default` profile with these settings:

- **stale**: 5 minutes (client-side)
- **revalidate**: 15 minutes (server-side)
- **expire**: Never expires by time

 lib/data.ts

```
async function getData() {
  'use cache'
  // Implicitly uses default profile
  return fetch('/api/data')
}
```

### Customizing cache lifetime

Use the [cacheLife](https://nextjs.org/docs/app/api-reference/functions/cacheLife) function to customize cache duration:

 lib/data.ts

```
import { cacheLife } from 'next/cache'

async function getData() {
  'use cache'
  cacheLife('hours') // Use built-in 'hours' profile
  return fetch('/api/data')
}
```

### On-demand revalidation

Use [cacheTag](https://nextjs.org/docs/app/api-reference/functions/cacheTag), [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag), or [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) for on-demand cache invalidation:

 lib/data.ts

```
import { cacheTag } from 'next/cache'

async function getProducts() {
  'use cache'
  cacheTag('products')
  return fetch('/api/products')
}
```

 app/actions.ts

```
'use server'

import { updateTag } from 'next/cache'

export async function updateProduct() {
  await db.products.update(...)
  updateTag('products') // Invalidates all 'products' caches
}
```

Both `cacheLife` and `cacheTag` integrate across client and server caching layers, meaning you configure your caching semantics in one place and they apply everywhere.

## Examples

### Caching an entire route withuse cache

To pre-render an entire route, add `use cache` to the top of **both** the `layout` and `page` files. Each of these segments are treated as separate entry points in your application, and will be cached independently.

 app/layout.tsxJavaScriptTypeScript

```
'use cache'

export default async function Layout({ children }: { children: ReactNode }) {
  return <div>{children}</div>
}
```

Any components imported and nested in `page` file are part of the cache output associated with the `page`.

 app/page.tsxJavaScriptTypeScript

```
'use cache'

async function Users() {
  const users = await fetch('/api/users')
  // loop through users
}

export default async function Page() {
  return (
    <main>
      <Users />
    </main>
  )
}
```

> **Good to know**:
>
>
>
> - If `use cache` is added only to the `layout` or the `page`, only that route segment and any components imported into it will be cached.

### Caching a component's output withuse cache

You can use `use cache` at the component level to cache any fetches or computations performed within that component. The cache entry will be reused as long as the serialized props produce the same value in each instance.

 app/components/bookings.tsxJavaScriptTypeScript

```
export async function Bookings({ type = 'haircut' }: BookingsProps) {
  'use cache'
  async function getBookingsData() {
    const data = await fetch(`/api/bookings?type=${encodeURIComponent(type)}`)
    return data
  }
  return //...
}

interface BookingsProps {
  type: string
}
```

### Caching function output withuse cache

Since you can add `use cache` to any asynchronous function, you aren't limited to caching components or routes only. You might want to cache a network request, a database query, or a slow computation.

 app/actions.tsJavaScriptTypeScript

```
export async function getData() {
  'use cache'

  const data = await fetch('/api/data')
  return data
}
```

### Interleaving

In React, composition with `children` or slots is a well-known pattern for building flexible components. When using `use cache`, you can continue to compose your UI in this way. Anything included as `children`, or other compositional slots, in the returned JSX will be passed through the cached component without affecting its cache entry.

As long as you don't directly reference any of the JSX slots inside the body of the cacheable function itself, their presence in the returned output won't affect the cache entry.

 app/page.tsxJavaScriptTypeScript

```
export default async function Page() {
  const uncachedData = await getData()
  return (
    // Pass compositional slots as props, e.g. header and children
    <CacheComponent header={<h1>Home</h1>}>
      {/* DynamicComponent is provided as the children slot */}
      <DynamicComponent data={uncachedData} />
    </CacheComponent>
  )
}

async function CacheComponent({
  header, // header: a compositional slot, injected as a prop
  children, // children: another slot for nested composition
}: {
  header: ReactNode
  children: ReactNode
}) {
  'use cache'
  const cachedData = await fetch('/api/cached-data')
  return (
    <div>
      {header}
      <PrerenderedComponent data={cachedData} />
      {children}
    </div>
  )
}
```

You can also pass Server Actions through cached components to Client Components without invoking them inside the cacheable function.

 app/page.tsxJavaScriptTypeScript

```
import ClientComponent from './ClientComponent'

export default async function Page() {
  const performUpdate = async () => {
    'use server'
    // Perform some server-side update
    await db.update(...)
  }

  return <CachedComponent performUpdate={performUpdate} />
}

async function CachedComponent({
  performUpdate,
}: {
  performUpdate: () => Promise<void>
}) {
  'use cache'
  // Do not call performUpdate here
  return <ClientComponent action={performUpdate} />
}
```

   app/ClientComponent.tsxJavaScriptTypeScript

```
'use client'

export default function ClientComponent({
  action,
}: {
  action: () => Promise<void>
}) {
  return <button onClick={action}>Update</button>
}
```

## Troubleshooting

### Debugging cache behavior

#### Verbose logging

Set `NEXT_PRIVATE_DEBUG_CACHE=1` for verbose cache logging:

```
NEXT_PRIVATE_DEBUG_CACHE=1 npm run dev
# or for production
NEXT_PRIVATE_DEBUG_CACHE=1 npm run start
```

> **Good to know:** This environment variable also logs ISR and other caching mechanisms. See [Verifying correct production behavior](https://nextjs.org/docs/app/guides/incremental-static-regeneration#verifying-correct-production-behavior) for more details.

#### Console log replays

In development, console logs from cached functions appear with a `Cache` prefix.

### Build Hangs (Cache Timeout)

If your build hangs, you're accessing Promises that resolve to dynamic or runtime data, created outside a `use cache` boundary. The cached function waits for data that can't resolve during the build, causing a timeout after 50 seconds.

When the build timeouts you'll see this error message:

> Error: Filling a cache during prerender timed out, likely because request-specific arguments such as params, searchParams, cookies() or dynamic data were used inside "use cache".

Common ways this happens: passing such Promises as props, accessing them via closure, or retrieving them from shared storage (Maps).

> **Good to know:** Directly calling `cookies()` or `headers()` inside `use cache` fails immediately with a [different error](https://nextjs.org/docs/messages/next-request-in-use-cache), not a timeout.

**Passing runtime data Promises as props:**

 app/page.tsx

```
import { cookies } from 'next/headers'
import { Suspense } from 'react'

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Dynamic />
    </Suspense>
  )
}

async function Dynamic() {
  const cookieStore = cookies()
  return <Cached promise={cookieStore} /> // Build hangs
}

async function Cached({ promise }: { promise: Promise<unknown> }) {
  'use cache'
  const data = await promise // Waits for runtime data during build
  return <p>..</p>
}
```

Await the `cookies` store in the `Dynamic` component, and pass a cookie value to the `Cached` component.

**Shared deduplication storage:**

 app/page.tsx

```
// Problem: Map stores dynamic Promises, accessed by cached code
import { Suspense } from 'react'

const cache = new Map<string, Promise<string>>()

export default function Page() {
  return (
    <>
      <Suspense fallback={<div>Loading...</div>}>
        <Dynamic id="data" />
      </Suspense>
      <Cached id="data" />
    </>
  )
}

async function Dynamic({ id }: { id: string }) {
  // Stores dynamic Promise in shared Map
  cache.set(
    id,
    fetch(`https://api.example.com/${id}`).then((r) => r.text())
  )
  return <p>Dynamic</p>
}

async function Cached({ id }: { id: string }) {
  'use cache'
  return <p>{await cache.get(id)}</p> // Build hangs - retrieves dynamic Promise
}
```

Use Next.js's built-in `fetch()` deduplication or use separate Maps for cached and uncached contexts.

## Platform Support

| Deployment Option | Supported |
| --- | --- |
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

Learn how to [configure caching](https://nextjs.org/docs/app/guides/self-hosting#caching-and-isr) when self-hosting Next.js.

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | "use cache"is enabled with the Cache Components feature. |
| v15.0.0 | "use cache"is introduced as an experimental feature. |

## Related

View related API references.[use cache: privateLearn how to use the "use cache: private" directive to cache functions that access runtime request APIs.](https://nextjs.org/docs/app/api-reference/directives/use-cache-private)[cacheComponentsLearn how to enable the cacheComponents flag in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)[cacheLifeLearn how to set up cacheLife configurations in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheLife)[cacheHandlersConfigure custom cache handlers for use cache directives in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheHandlers)[cacheTagLearn how to use the cacheTag function to manage cache invalidation in your Next.js application.](https://nextjs.org/docs/app/api-reference/functions/cacheTag)[cacheLifeLearn how to use the cacheLife function to set the cache expiration time for a cached function or component.](https://nextjs.org/docs/app/api-reference/functions/cacheLife)[revalidateTagAPI Reference for the revalidateTag function.](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)

Was this helpful?

supported.

---

# use client

> Learn how to use the use client directive to render a component on the client.

[API Reference](https://nextjs.org/docs/app/api-reference)[Directives](https://nextjs.org/docs/app/api-reference/directives)use client

# use client

Last updated  June 16, 2025

The `'use client'` directive declares an entry point for the components to be rendered on the **client side** and should be used when creating interactive user interfaces (UI) that require client-side JavaScript capabilities, such as state management, event handling, and access to browser APIs. This is a React feature.

> **Good to know:**
>
>
>
> You do not need to add the `'use client'` directive to every file that contains Client Components. You only need to add it to the files whose components you want to render directly within Server Components. The `'use client'` directive defines the client-server [boundary](https://nextjs.org/docs/app/building-your-application/rendering#network-boundary), and the components exported from such a file serve as entry points to the client.

## Usage

To declare an entry point for the Client Components, add the `'use client'` directive **at the top of the file**, before any imports:

 app/components/counter.tsxJavaScriptTypeScript

```
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

When using the `'use client'` directive, the props of the Client Components must be [serializable](https://react.dev/reference/rsc/use-client#serializable-types). This means the props need to be in a format that React can serialize when sending data from the server to the client.

 app/components/counter.tsxJavaScriptTypeScript

```
'use client'

export default function Counter({
  onClick /* ❌ Function is not serializable */,
}) {
  return (
    <div>
      <button onClick={onClick}>Increment</button>
    </div>
  )
}
```

## Nesting Client Components within Server Components

Combining Server and Client Components allows you to build applications that are both performant and interactive:

1. **Server Components**: Use for static content, data fetching, and SEO-friendly elements.
2. **Client Components**: Use for interactive elements that require state, effects, or browser APIs.
3. **Component composition**: Nest Client Components within Server Components as needed for a clear separation of server and client logic.

In the following example:

- `Header` is a Server Component handling static content.
- `Counter` is a Client Component enabling interactivity within the page.

 app/page.tsxJavaScriptTypeScript

```
import Header from './header'
import Counter from './counter' // This is a Client Component

export default function Page() {
  return (
    <div>
      <Header />
      <Counter />
    </div>
  )
}
```

## Reference

See the [React documentation](https://react.dev/reference/rsc/use-client) for more information on `'use client'`.

Was this helpful?

supported.

---

# use server

> Learn how to use the use server directive to execute code on the server.

[API Reference](https://nextjs.org/docs/app/api-reference)[Directives](https://nextjs.org/docs/app/api-reference/directives)use server

# use server

Last updated  June 16, 2025

The `use server` directive designates a function or file to be executed on the **server side**. It can be used at the top of a file to indicate that all functions in the file are server-side, or inline at the top of a function to mark the function as a [Server Function](https://19.react.dev/reference/rsc/server-functions). This is a React feature.

## Usinguse serverat the top of a file

The following example shows a file with a `use server` directive at the top. All functions in the file are executed on the server.

 app/actions.tsJavaScriptTypeScript

```
'use server'
import { db } from '@/lib/db' // Your database client

export async function createUser(data: { name: string; email: string }) {
  const user = await db.user.create({ data })
  return user
}
```

### Using Server Functions in a Client Component

To use Server Functions in Client Components you need to create your Server Functions in a dedicated file using the `use server` directive at the top of the file. These Server Functions can then be imported into Client and Server Components and executed.

Assuming you have a `fetchUsers` Server Function in `actions.ts`:

 app/actions.tsJavaScriptTypeScript

```
'use server'
import { db } from '@/lib/db' // Your database client

export async function fetchUsers() {
  const users = await db.user.findMany()
  return users
}
```

Then you can import the `fetchUsers` Server Function into a Client Component and execute it on the client-side.

 app/components/my-button.tsxJavaScriptTypeScript

```
'use client'
import { fetchUsers } from '../actions'

export default function MyButton() {
  return <button onClick={() => fetchUsers()}>Fetch Users</button>
}
```

## Usinguse serverinline

In the following example, `use server` is used inline at the top of a function to mark it as a [Server Function](https://19.react.dev/reference/rsc/server-functions):

 app/posts/[id]/page.tsxJavaScriptTypeScript

```
import { EditPost } from './edit-post'
import { revalidatePath } from 'next/cache'

export default async function PostPage({ params }: { params: { id: string } }) {
  const post = await getPost(params.id)

  async function updatePost(formData: FormData) {
    'use server'
    await savePost(params.id, formData)
    revalidatePath(`/posts/${params.id}`)
  }

  return <EditPost updatePostAction={updatePost} post={post} />
}
```

## Security considerations

When using the `use server` directive, it's important to ensure that all server-side logic is secure and that sensitive data remains protected.

### Authentication and authorization

Always authenticate and authorize users before performing sensitive server-side operations.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { db } from '@/lib/db' // Your database client
import { authenticate } from '@/lib/auth' // Your authentication library

export async function createUser(
  data: { name: string; email: string },
  token: string
) {
  const user = authenticate(token)
  if (!user) {
    throw new Error('Unauthorized')
  }
  const newUser = await db.user.create({ data })
  return newUser
}
```

## Reference

See the [React documentation](https://react.dev/reference/rsc/use-server) for more information on `use server`.

Was this helpful?

supported.

---

# Directives

> Directives are used to modify the behavior of your Next.js application.

[App Router](https://nextjs.org/docs/app)[API Reference](https://nextjs.org/docs/app/api-reference)Directives

# Directives

Last updated  June 16, 2025

The following directives are available:

[use cacheLearn how to use the "use cache" directive to cache data in your Next.js application.](https://nextjs.org/docs/app/api-reference/directives/use-cache)[use cache: privateLearn how to use the "use cache: private" directive to cache functions that access runtime request APIs.](https://nextjs.org/docs/app/api-reference/directives/use-cache-private)[use cache: remoteLearn how to use the "use cache: remote" directive for persistent, shared caching using remote cache handlers.](https://nextjs.org/docs/app/api-reference/directives/use-cache-remote)[use clientLearn how to use the use client directive to render a component on the client.](https://nextjs.org/docs/app/api-reference/directives/use-client)[use serverLearn how to use the use server directive to execute code on the server.](https://nextjs.org/docs/app/api-reference/directives/use-server)

Was this helpful?

supported.

---

# Edge Runtime

> API Reference for the Edge Runtime.

[App Router](https://nextjs.org/docs/app)[API Reference](https://nextjs.org/docs/app/api-reference)Edge Runtime

# Edge Runtime

Last updated  October 17, 2025

Next.js has two server runtimes you can use in your application:

- The **Node.js Runtime** (default), which has access to all Node.js APIs and is used for rendering your application.
- The **Edge Runtime** which contains a more limited [set of APIs](#reference), used in [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy).

## Caveats

- The Edge Runtime does not support all Node.js APIs. Some packages may not work as expected.
- The Edge Runtime does not support Incremental Static Regeneration (ISR).
- Both runtimes can support [streaming](https://nextjs.org/docs/app/api-reference/file-conventions/loading) depending on your deployment adapter.

## Reference

The Edge Runtime supports the following APIs:

### Network APIs

| API | Description |
| --- | --- |
| Blob | Represents a blob |
| fetch | Fetches a resource |
| FetchEvent | Represents a fetch event |
| File | Represents a file |
| FormData | Represents form data |
| Headers | Represents HTTP headers |
| Request | Represents an HTTP request |
| Response | Represents an HTTP response |
| URLSearchParams | Represents URL search parameters |
| WebSocket | Represents a websocket connection |

### Encoding APIs

| API | Description |
| --- | --- |
| atob | Decodes a base-64 encoded string |
| btoa | Encodes a string in base-64 |
| TextDecoder | Decodes a Uint8Array into a string |
| TextDecoderStream | Chainable decoder for streams |
| TextEncoder | Encodes a string into a Uint8Array |
| TextEncoderStream | Chainable encoder for streams |

### Stream APIs

| API | Description |
| --- | --- |
| ReadableStream | Represents a readable stream |
| ReadableStreamBYOBReader | Represents a reader of a ReadableStream |
| ReadableStreamDefaultReader | Represents a reader of a ReadableStream |
| TransformStream | Represents a transform stream |
| WritableStream | Represents a writable stream |
| WritableStreamDefaultWriter | Represents a writer of a WritableStream |

### Crypto APIs

| API | Description |
| --- | --- |
| crypto | Provides access to the cryptographic functionality of the platform |
| CryptoKey | Represents a cryptographic key |
| SubtleCrypto | Provides access to common cryptographic primitives, like hashing, signing, encryption or decryption |

### Web Standard APIs

| API | Description |
| --- | --- |
| AbortController | Allows you to abort one or more DOM requests as and when desired |
| Array | Represents an array of values |
| ArrayBuffer | Represents a generic, fixed-length raw binary data buffer |
| Atomics | Provides atomic operations as static methods |
| BigInt | Represents a whole number with arbitrary precision |
| BigInt64Array | Represents a typed array of 64-bit signed integers |
| BigUint64Array | Represents a typed array of 64-bit unsigned integers |
| Boolean | Represents a logical entity and can have two values:trueandfalse |
| clearInterval | Cancels a timed, repeating action which was previously established by a call tosetInterval() |
| clearTimeout | Cancels a timed, repeating action which was previously established by a call tosetTimeout() |
| console | Provides access to the browser's debugging console |
| DataView | Represents a generic view of anArrayBuffer |
| Date | Represents a single moment in time in a platform-independent format |
| decodeURI | Decodes a Uniform Resource Identifier (URI) previously created byencodeURIor by a similar routine |
| decodeURIComponent | Decodes a Uniform Resource Identifier (URI) component previously created byencodeURIComponentor by a similar routine |
| DOMException | Represents an error that occurs in the DOM |
| encodeURI | Encodes a Uniform Resource Identifier (URI) by replacing each instance of certain characters by one, two, three, or four escape sequences representing the UTF-8 encoding of the character |
| encodeURIComponent | Encodes a Uniform Resource Identifier (URI) component by replacing each instance of certain characters by one, two, three, or four escape sequences representing the UTF-8 encoding of the character |
| Error | Represents an error when trying to execute a statement or accessing a property |
| EvalError | Represents an error that occurs regarding the global functioneval() |
| Float32Array | Represents a typed array of 32-bit floating point numbers |
| Float64Array | Represents a typed array of 64-bit floating point numbers |
| Function | Represents a function |
| Infinity | Represents the mathematical Infinity value |
| Int8Array | Represents a typed array of 8-bit signed integers |
| Int16Array | Represents a typed array of 16-bit signed integers |
| Int32Array | Represents a typed array of 32-bit signed integers |
| Intl | Provides access to internationalization and localization functionality |
| isFinite | Determines whether a value is a finite number |
| isNaN | Determines whether a value isNaNor not |
| JSON | Provides functionality to convert JavaScript values to and from the JSON format |
| Map | Represents a collection of values, where each value may occur only once |
| Math | Provides access to mathematical functions and constants |
| Number | Represents a numeric value |
| Object | Represents the object that is the base of all JavaScript objects |
| parseFloat | Parses a string argument and returns a floating point number |
| parseInt | Parses a string argument and returns an integer of the specified radix |
| Promise | Represents the eventual completion (or failure) of an asynchronous operation, and its resulting value |
| Proxy | Represents an object that is used to define custom behavior for fundamental operations (e.g. property lookup, assignment, enumeration, function invocation, etc) |
| queueMicrotask | Queues a microtask to be executed |
| RangeError | Represents an error when a value is not in the set or range of allowed values |
| ReferenceError | Represents an error when a non-existent variable is referenced |
| Reflect | Provides methods for interceptable JavaScript operations |
| RegExp | Represents a regular expression, allowing you to match combinations of characters |
| Set | Represents a collection of values, where each value may occur only once |
| setInterval | Repeatedly calls a function, with a fixed time delay between each call |
| setTimeout | Calls a function or evaluates an expression after a specified number of milliseconds |
| SharedArrayBuffer | Represents a generic, fixed-length raw binary data buffer |
| String | Represents a sequence of characters |
| structuredClone | Creates a deep copy of a value |
| Symbol | Represents a unique and immutable data type that is used as the key of an object property |
| SyntaxError | Represents an error when trying to interpret syntactically invalid code |
| TypeError | Represents an error when a value is not of the expected type |
| Uint8Array | Represents a typed array of 8-bit unsigned integers |
| Uint8ClampedArray | Represents a typed array of 8-bit unsigned integers clamped to 0-255 |
| Uint32Array | Represents a typed array of 32-bit unsigned integers |
| URIError | Represents an error when a global URI handling function was used in a wrong way |
| URL | Represents an object providing static methods used for creating object URLs |
| URLPattern | Represents a URL pattern |
| URLSearchParams | Represents a collection of key/value pairs |
| WeakMap | Represents a collection of key/value pairs in which the keys are weakly referenced |
| WeakSet | Represents a collection of objects in which each object may occur only once |
| WebAssembly | Provides access to WebAssembly |

### Next.js Specific Polyfills

- [AsyncLocalStorage](https://nodejs.org/api/async_context.html#class-asynclocalstorage)

### Environment Variables

You can use `process.env` to access [Environment Variables](https://nextjs.org/docs/app/guides/environment-variables) for both `next dev` and `next build`.

### Unsupported APIs

The Edge Runtime has some restrictions including:

- Native Node.js APIs **are not supported**. For example, you can't read or write to the filesystem.
- `node_modules` *can* be used, as long as they implement ES Modules and do not use native Node.js APIs.
- Calling `require` directly is **not allowed**. Use ES Modules instead.

The following JavaScript language features are disabled, and **will not work:**

| API | Description |
| --- | --- |
| eval | Evaluates JavaScript code represented as a string |
| new Function(evalString) | Creates a new function with the code provided as an argument |
| WebAssembly.compile | Compiles a WebAssembly module from a buffer source |
| WebAssembly.instantiate | Compiles and instantiates a WebAssembly module from a buffer source |

In rare cases, your code could contain (or import) some dynamic code evaluation statements which *can not be reached at runtime* and which can not be removed by treeshaking.
You can relax the check to allow specific files with your Proxy configuration:

 proxy.ts

```
export const config = {
  unstable_allowDynamic: [
    // allows a single file
    '/lib/utilities.js',
    // use a glob to allow anything in the function-bind 3rd party module
    '**/node_modules/function-bind/**',
  ],
}
```

`unstable_allowDynamic` is a [glob](https://github.com/micromatch/micromatch#matching-features), or an array of globs, ignoring dynamic code evaluation for specific files. The globs are relative to your application root folder.

Be warned that if these statements are executed on the Edge, *they will throw and cause a runtime error*.

Was this helpful?

supported.

---

# default.js

> API Reference for the default.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)default.js

# default.js

Last updated  October 9, 2025

The `default.js` file is used to render a fallback within [Parallel Routes](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes) when Next.js cannot recover a [slot's](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes#slots) active state after a full-page load.

During [soft navigation](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions), Next.js keeps track of the active *state* (subpage) for each slot. However, for hard navigations (full-page load), Next.js cannot recover the active state. In this case, a `default.js` file can be rendered for subpages that don't match the current URL.

Consider the following folder structure. The `@team` slot has a `settings` page, but `@analytics` does not.

 ![Parallel Routes unmatched routes](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fparallel-routes-unmatched-routes.png&w=3840&q=75)![Parallel Routes unmatched routes](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fparallel-routes-unmatched-routes.png&w=3840&q=75)

When navigating to `/settings`, the `@team` slot will render the `settings` page while maintaining the currently active page for the `@analytics` slot.

On refresh, Next.js will render a `default.js` for `@analytics`. If `default.js` doesn't exist, an error is returned for named slots (`@team`, `@analytics`, etc) and requires you to define a `default.js` in order to continue. If you want to preserve the old behavior of returning a 404 in these situations, you can create a `default.js` that contains:

 app/@team/default.js

```
import { notFound } from 'next/navigation'

export default function Default() {
  notFound()
}
```

Additionally, since `children` is an implicit slot, you also need to create a `default.js` file to render a fallback for `children` when Next.js cannot recover the active state of the parent page. If you don't create a `default.js` for the `children` slot, it will return a 404 page for the route.

## Reference

### params(optional)

A promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) from the root segment down to the slot's subpages. For example:

 app/[artist]/@sidebar/default.jsJavaScriptTypeScript

```
export default async function Default({
  params,
}: {
  params: Promise<{ artist: string }>
}) {
  const { artist } = await params
}
```

| Example | URL | params |
| --- | --- | --- |
| app/[artist]/@sidebar/default.js | /zack | Promise<{ artist: 'zack' }> |
| app/[artist]/[album]/@sidebar/default.js | /zack/next | Promise<{ artist: 'zack', album: 'next' }> |

- Since the `params` prop is a promise. You must use `async/await` or React's [use](https://react.dev/reference/react/use) function to access the values.
  - In version 14 and earlier, `params` was a synchronous prop. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future.

## Learn more about Parallel Routes

[Parallel RoutesSimultaneously render one or more pages in the same view that can be navigated independently. A pattern for highly dynamic applications.](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes)

Was this helpful?

supported.
