# Edge Runtime and more

# Edge Runtime

> API Reference for the Edge Runtime.

[Pages Router](https://nextjs.org/docs/pages)[API Reference](https://nextjs.org/docs/pages/api-reference)Edge RuntimeYou are currently viewing the documentation for Pages Router.

# Edge Runtime

Last updated  April 15, 2025

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

# instrumentation.js

> API reference for the instrumentation.js file.

[API Reference](https://nextjs.org/docs/pages/api-reference)[File-system conventions](https://nextjs.org/docs/pages/api-reference/file-conventions)instrumentation.jsYou are currently viewing the documentation for Pages Router.

# instrumentation.js

Last updated  April 15, 2025

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

Was this helpful?

supported.

---

# Proxy

> Learn how to use Proxy to run code before a request is completed.

[API Reference](https://nextjs.org/docs/pages/api-reference)[File-system conventions](https://nextjs.org/docs/pages/api-reference/file-conventions)ProxyYou are currently viewing the documentation for Pages Router.

# Proxy

Last updated  October 17, 2025

> **Note**: The `middleware` file convention is deprecated and has been renamed to `proxy`. See [Migration to Proxy](#migration-to-proxy) for more details.

The `proxy.js|ts` file is used to write [Proxy](https://nextjs.org/docs/app/getting-started/proxy) and run code on the server before a request is completed. Then, based on the incoming request, you can modify the response by rewriting, redirecting, modifying the request or response headers, or responding directly.

Proxy executes before routes are rendered. It's particularly useful for implementing custom server-side logic like authentication, logging, or handling redirects.

> **Good to know**:
>
>
>
> Proxy is meant to be invoked separately of your render code and in optimized cases deployed to your CDN for fast redirect/rewrite handling, you should not attempt relying on shared modules or globals.
>
>
>
> To pass information from Proxy to your application, use [headers](#setting-headers), [cookies](#using-cookies), [rewrites](https://nextjs.org/docs/app/api-reference/functions/next-response#rewrite), [redirects](https://nextjs.org/docs/app/api-reference/functions/next-response#redirect), or the URL.

Create a `proxy.ts` (or `.js`) file in the project root, or inside `src` if applicable, so that it is located at the same level as `pages` or `app`.

If you’ve customized [pageExtensions](https://nextjs.org/docs/app/api-reference/config/next-config-js/pageExtensions), for example to `.page.ts` or `.page.js`, name your file `proxy.page.ts` or `proxy.page.js` accordingly.

 proxy.tsJavaScriptTypeScript

```
import { NextResponse, NextRequest } from 'next/server'

// This function can be marked `async` if using `await` inside
export function proxy(request: NextRequest) {
  return NextResponse.redirect(new URL('/home', request.url))
}

export const config = {
  matcher: '/about/:path*',
}
```

## Exports

### Proxy function

The file must export a single function, either as a default export or named `proxy`. Note that multiple proxy from the same file are not supported.

 proxy.js

```
// Example of default export
export default function proxy(request) {
  // Proxy logic
}
```

### Config object (optional)

Optionally, a config object can be exported alongside the Proxy function. This object includes the [matcher](#matcher) to specify paths where the Proxy applies.

### Matcher

The `matcher` option allows you to target specific paths for the Proxy to run on. You can specify these paths in several ways:

- For a single path: Directly use a string to define the path, like `'/about'`.
- For multiple paths: Use an array to list multiple paths, such as `matcher: ['/about', '/contact']`, which applies the Proxy to both `/about` and `/contact`.

 proxy.js

```
export const config = {
  matcher: ['/about/:path*', '/dashboard/:path*'],
}
```

Additionally, the `matcher` option supports complex path specifications using regular expressions. For example, you can exclude certain paths with a regular expression matcher:

 proxy.js

```
export const config = {
  matcher: [
    // Exclude API routes, static files, image optimizations, and .png files
    '/((?!api|_next/static|_next/image|.*\\.png$).*)',
  ],
}
```

This enables precise control over which paths to include or exclude.

The `matcher` option accepts an array of objects with the following keys:

- `source`: The path or pattern used to match the request paths. It can be a string for direct path matching or a pattern for more complex matching.
- `locale` (optional): A boolean that, when set to `false`, ignores locale-based routing in path matching.
- `has` (optional): Specifies conditions based on the presence of specific request elements such as headers, query parameters, or cookies.
- `missing` (optional): Focuses on conditions where certain request elements are absent, like missing headers or cookies.

 proxy.js

```
export const config = {
  matcher: [
    {
      source: '/api/:path*',
      locale: false,
      has: [
        { type: 'header', key: 'Authorization', value: 'Bearer Token' },
        { type: 'query', key: 'userId', value: '123' },
      ],
      missing: [{ type: 'cookie', key: 'session', value: 'active' }],
    },
  ],
}
```

Configured matchers:

1. MUST start with `/`
2. Can include named parameters: `/about/:path` matches `/about/a` and `/about/b` but not `/about/a/c`
3. Can have modifiers on named parameters (starting with `:`): `/about/:path*` matches `/about/a/b/c` because `*` is *zero or more*. `?` is *zero or one* and `+` *one or more*
4. Can use regular expression enclosed in parenthesis: `/about/(.*)` is the same as `/about/:path*`
5. Are anchored to the start of the path: `/about` matches `/about` and `/about/team` but not `/blog/about`

Read more details on [path-to-regexp](https://github.com/pillarjs/path-to-regexp#path-to-regexp-1) documentation.

> **Good to know**:
>
>
>
> - The `matcher` values need to be constants so they can be statically analyzed at build-time. Dynamic values such as variables will be ignored.
> - For backward compatibility, Next.js always considers `/public` as `/public/index`. Therefore, a matcher of `/public/:path` will match.

## Params

### request

When defining Proxy, the default export function accepts a single parameter, `request`. This parameter is an instance of `NextRequest`, which represents the incoming HTTP request.

 proxy.tsJavaScriptTypeScript

```
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Proxy logic goes here
}
```

> **Good to know**:
>
>
>
> - `NextRequest` is a type that represents incoming HTTP requests in Next.js Proxy, whereas [NextResponse](#nextresponse) is a class used to manipulate and send back HTTP responses.

## NextResponse

The `NextResponse` API allows you to:

- `redirect` the incoming request to a different URL
- `rewrite` the response by displaying a given URL
- Set request headers for API Routes, `getServerSideProps`, and `rewrite` destinations
- Set response cookies
- Set response headers

To produce a response from Proxy, you can:

1. `rewrite` to a route ([Page](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts) or [Edge API Route](https://nextjs.org/docs/pages/building-your-application/routing/api-routes)) that produces a response
2. return a `NextResponse` directly. See [Producing a Response](#producing-a-response)

## Execution order

Proxy will be invoked for **every route in your project**. Given this, it's crucial to use [matchers](#matcher) to precisely target or exclude specific routes. The following is the execution order:

1. `headers` from `next.config.js`
2. `redirects` from `next.config.js`
3. Proxy (`rewrites`, `redirects`, etc.)
4. `beforeFiles` (`rewrites`) from `next.config.js`
5. Filesystem routes (`public/`, `_next/static/`, `pages/`, `app/`, etc.)
6. `afterFiles` (`rewrites`) from `next.config.js`
7. Dynamic Routes (`/blog/[slug]`)
8. `fallback` (`rewrites`) from `next.config.js`

## Runtime

Proxy defaults to using the Node.js runtime. The [runtime](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#runtime) config option is not available in Proxy files. Setting the `runtime` config option in Proxy will throw an error.

## Advanced Proxy flags

In `v13.1` of Next.js two additional flags were introduced for proxy, `skipMiddlewareUrlNormalize` and `skipTrailingSlashRedirect` to handle advanced use cases.

`skipTrailingSlashRedirect` disables Next.js redirects for adding or removing trailing slashes. This allows custom handling inside proxy to maintain the trailing slash for some paths but not others, which can make incremental migrations easier.

 next.config.js

```
module.exports = {
  skipTrailingSlashRedirect: true,
}
```

 proxy.js

```
const legacyPrefixes = ['/docs', '/blog']

export default async function proxy(req) {
  const { pathname } = req.nextUrl

  if (legacyPrefixes.some((prefix) => pathname.startsWith(prefix))) {
    return NextResponse.next()
  }

  // apply trailing slash handling
  if (
    !pathname.endsWith('/') &&
    !pathname.match(/((?!\.well-known(?:\/.*)?)(?:[^/]+\/)*[^/]+\.\w+)/)
  ) {
    return NextResponse.redirect(
      new URL(`${req.nextUrl.pathname}/`, req.nextUrl)
    )
  }
}
```

`skipMiddlewareUrlNormalize` allows for disabling the URL normalization in Next.js to make handling direct visits and client-transitions the same. In some advanced cases, this option provides full control by using the original URL.

 next.config.js

```
module.exports = {
  skipMiddlewareUrlNormalize: true,
}
```

 proxy.js

```
export default async function proxy(req) {
  const { pathname } = req.nextUrl

  // GET /_next/data/build-id/hello.json

  console.log(pathname)
  // with the flag this now /_next/data/build-id/hello.json
  // without the flag this would be normalized to /hello
}
```

## Examples

### Conditional Statements

 proxy.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/about')) {
    return NextResponse.rewrite(new URL('/about-2', request.url))
  }

  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.rewrite(new URL('/dashboard/user', request.url))
  }
}
```

### Using Cookies

Cookies are regular headers. On a `Request`, they are stored in the `Cookie` header. On a `Response` they are in the `Set-Cookie` header. Next.js provides a convenient way to access and manipulate these cookies through the `cookies` extension on `NextRequest` and `NextResponse`.

1. For incoming requests, `cookies` comes with the following methods: `get`, `getAll`, `set`, and `delete` cookies. You can check for the existence of a cookie with `has` or remove all cookies with `clear`.
2. For outgoing responses, `cookies` have the following methods `get`, `getAll`, `set`, and `delete`.

 proxy.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Assume a "Cookie:nextjs=fast" header to be present on the incoming request
  // Getting cookies from the request using the `RequestCookies` API
  let cookie = request.cookies.get('nextjs')
  console.log(cookie) // => { name: 'nextjs', value: 'fast', Path: '/' }
  const allCookies = request.cookies.getAll()
  console.log(allCookies) // => [{ name: 'nextjs', value: 'fast' }]

  request.cookies.has('nextjs') // => true
  request.cookies.delete('nextjs')
  request.cookies.has('nextjs') // => false

  // Setting cookies on the response using the `ResponseCookies` API
  const response = NextResponse.next()
  response.cookies.set('vercel', 'fast')
  response.cookies.set({
    name: 'vercel',
    value: 'fast',
    path: '/',
  })
  cookie = response.cookies.get('vercel')
  console.log(cookie) // => { name: 'vercel', value: 'fast', Path: '/' }
  // The outgoing response will have a `Set-Cookie:vercel=fast;path=/` header.

  return response
}
```

### Setting Headers

You can set request and response headers using the `NextResponse` API (setting *request* headers is available since Next.js v13.0.0).

 proxy.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Clone the request headers and set a new header `x-hello-from-proxy1`
  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-hello-from-proxy1', 'hello')

  // You can also set request headers in NextResponse.next
  const response = NextResponse.next({
    request: {
      // New request headers
      headers: requestHeaders,
    },
  })

  // Set a new response header `x-hello-from-proxy2`
  response.headers.set('x-hello-from-proxy2', 'hello')
  return response
}
```

Note that the snippet uses:

- `NextResponse.next({ request: { headers: requestHeaders } })` to make `requestHeaders` available upstream
- **NOT** `NextResponse.next({ headers: requestHeaders })` which makes `requestHeaders` available to clients

Learn more in [NextResponse headers in Proxy](https://nextjs.org/docs/app/api-reference/functions/next-response#next).

> **Good to know**: Avoid setting large headers as it might cause [431 Request Header Fields Too Large](https://developer.mozilla.org/docs/Web/HTTP/Status/431) error depending on your backend web server configuration.

### CORS

You can set CORS headers in Proxy to allow cross-origin requests, including [simple](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests) and [preflighted](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#preflighted_requests) requests.

 proxy.tsJavaScriptTypeScript

```
import { NextRequest, NextResponse } from 'next/server'

const allowedOrigins = ['https://acme.com', 'https://my-app.org']

const corsOptions = {
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}

export function proxy(request: NextRequest) {
  // Check the origin from the request
  const origin = request.headers.get('origin') ?? ''
  const isAllowedOrigin = allowedOrigins.includes(origin)

  // Handle preflighted requests
  const isPreflight = request.method === 'OPTIONS'

  if (isPreflight) {
    const preflightHeaders = {
      ...(isAllowedOrigin && { 'Access-Control-Allow-Origin': origin }),
      ...corsOptions,
    }
    return NextResponse.json({}, { headers: preflightHeaders })
  }

  // Handle simple requests
  const response = NextResponse.next()

  if (isAllowedOrigin) {
    response.headers.set('Access-Control-Allow-Origin', origin)
  }

  Object.entries(corsOptions).forEach(([key, value]) => {
    response.headers.set(key, value)
  })

  return response
}

export const config = {
  matcher: '/api/:path*',
}
```

### Producing a response

You can respond from Proxy directly by returning a `Response` or `NextResponse` instance. (This is available since [Next.js v13.1.0](https://nextjs.org/blog/next-13-1#nextjs-advanced-proxy))

 proxy.tsJavaScriptTypeScript

```
import type { NextRequest } from 'next/server'
import { isAuthenticated } from '@lib/auth'

// Limit the proxy to paths starting with `/api/`
export const config = {
  matcher: '/api/:function*',
}

export function proxy(request: NextRequest) {
  // Call our authentication function to check the request
  if (!isAuthenticated(request)) {
    // Respond with JSON indicating an error message
    return Response.json(
      { success: false, message: 'authentication failed' },
      { status: 401 }
    )
  }
}
```

### Negative matching

The `matcher` config allows full regex so matching like negative lookaheads or character matching is supported. An example of a negative lookahead to match all except specific paths can be seen here:

 proxy.js

```
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, sitemap.xml, robots.txt (metadata files)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
  ],
}
```

You can also bypass Proxy for certain requests by using the `missing` or `has` arrays, or a combination of both:

 proxy.js

```
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, sitemap.xml, robots.txt (metadata files)
     */
    {
      source:
        '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },

    {
      source:
        '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
      has: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },

    {
      source:
        '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
      has: [{ type: 'header', key: 'x-present' }],
      missing: [{ type: 'header', key: 'x-missing', value: 'prefetch' }],
    },
  ],
}
```

> **Good to know**:
>
>
>
> Even when `_next/data` is excluded in a negative matcher pattern, proxy will still be invoked for `_next/data` routes. This is intentional behavior to prevent accidental security issues where you might protect a page but forget to protect the corresponding data route.

 proxy.js

```
export const config = {
  matcher:
    '/((?!api|_next/data|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
}

// Proxy will still run for /_next/data/* routes despite being excluded
```

### waitUntilandNextFetchEvent

The `NextFetchEvent` object extends the native [FetchEvent](https://developer.mozilla.org/docs/Web/API/FetchEvent) object, and includes the [waitUntil()](https://developer.mozilla.org/docs/Web/API/ExtendableEvent/waitUntil) method.

The `waitUntil()` method takes a promise as an argument, and extends the lifetime of the Proxy until the promise settles. This is useful for performing work in the background.

 proxy.ts

```
import { NextResponse } from 'next/server'
import type { NextFetchEvent, NextRequest } from 'next/server'

export function proxy(req: NextRequest, event: NextFetchEvent) {
  event.waitUntil(
    fetch('https://my-analytics-platform.com', {
      method: 'POST',
      body: JSON.stringify({ pathname: req.nextUrl.pathname }),
    })
  )

  return NextResponse.next()
}
```

### Unit testing (experimental)

Starting in Next.js 15.1, the `next/experimental/testing/server` package contains utilities to help unit test proxy files. Unit testing proxy can help ensure that it's only run on desired paths and that custom routing logic works as intended before code reaches production.

The `unstable_doesProxyMatch` function can be used to assert whether proxy will run for the provided URL, headers, and cookies.

```
import { unstable_doesProxyMatch } from 'next/experimental/testing/server'

expect(
  unstable_doesProxyMatch({
    config,
    nextConfig,
    url: '/test',
  })
).toEqual(false)
```

The entire proxy function can also be tested.

```
import { isRewrite, getRewrittenUrl } from 'next/experimental/testing/server'

const request = new NextRequest('https://nextjs.org/docs')
const response = await proxy(request)
expect(isRewrite(response)).toEqual(true)
expect(getRewrittenUrl(response)).toEqual('https://other-domain.com/docs')
// getRedirectUrl could also be used if the response were a redirect
```

## Platform support

| Deployment Option | Supported |
| --- | --- |
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

Learn how to [configure Proxy](https://nextjs.org/docs/app/guides/self-hosting#proxy) when self-hosting Next.js.

## Migration to Proxy

### Why the Change

The reason behind the renaming of `middleware` is that the term "middleware" can often be confused with Express.js middleware, leading to a misinterpretation of its purpose. Also, Middleware is highly capable, so it may encourage the usage; however, this feature is recommended to be used as a last resort.

Next.js is moving forward to provide better APIs with better ergonomics so that developers can achieve their goals without Middleware. This is the reason behind the renaming of `middleware`.

### Why "Proxy"

The name Proxy clarifies what Middleware is capable of. The term "proxy" implies that it has a network boundary in front of the app, which is the behavior of Middleware. Also, Middleware defaults to run at the [Edge Runtime](https://nextjs.org/docs/app/api-reference/edge), which can run closer to the client, separated from the app's region. These behaviors align better with the term "proxy" and provide a clearer purpose of the feature.

### How to Migrate

We recommend users avoid relying on Middleware unless no other options exist. Our goal is to give them APIs with better ergonomics so they can achieve their goals without Middleware.

The term “middleware” often confuses users with Express.js middleware, which can encourage misuse. To clarify our direction, we are renaming the file convention to “proxy.” This highlights that we are moving away from Middleware, breaking down its overloaded features, and making the Proxy clear in its purpose.

Next.js provides a codemod to migrate from `middleware.ts` to `proxy.ts`. You can run the following command to migrate:

```
npx @next/codemod@canary middleware-to-proxy .
```

The codemod will rename the file and the function name from `middleware` to `proxy`.

```
// middleware.ts -> proxy.ts

- export function middleware() {
+ export function proxy() {
```

## Version history

| Version | Changes |
| --- | --- |
| v16.0.0 | Middleware is deprecated and renamed to Proxy |
| v15.5.0 | Middleware can now use the Node.js runtime (stable) |
| v15.2.0 | Middleware can now use the Node.js runtime (experimental) |
| v13.1.0 | Advanced Middleware flags added |
| v13.0.0 | Middleware can modify request headers, response headers, and send responses |
| v12.2.0 | Middleware is stable, please see theupgrade guide |
| v12.0.9 | Enforce absolute URLs in Edge Runtime (PR) |
| v12.0.0 | Middleware (Beta) added |

Was this helpful?

supported.

---

# public Folder

> Next.js allows you to serve static files, like images, in the public directory. You can learn how it works here.

[API Reference](https://nextjs.org/docs/pages/api-reference)[File-system conventions](https://nextjs.org/docs/pages/api-reference/file-conventions)publicYou are currently viewing the documentation for Pages Router.

# public Folder

Last updated  April 25, 2025

Next.js can serve static files, like images, under a folder called `public` in the root directory. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

For example, the file `public/avatars/me.png` can be viewed by visiting the `/avatars/me.png` path. The code to display that image might look like:

 avatar.js

```
import Image from 'next/image'

export function Avatar({ id, alt }) {
  return <Image src={`/avatars/${id}.png`} alt={alt} width="64" height="64" />
}

export function AvatarOfMe() {
  return <Avatar id="me" alt="A portrait of me" />
}
```

## Caching

Next.js cannot safely cache assets in the `public` folder because they may change. The default caching headers applied are:

```
Cache-Control: public, max-age=0
```

## Robots, Favicons, and others

The folder is also useful for `robots.txt`, `favicon.ico`, Google Site Verification, and any other static files (including `.html`). But make sure to not have a static file with the same name as a file in the `pages/` directory, as this will result in an error. [Read more](https://nextjs.org/docs/messages/conflicting-public-file-page).

Was this helpful?

supported.

---

# src Directory

> Save pages under the `src` folder as an alternative to the root `pages` directory.

[API Reference](https://nextjs.org/docs/pages/api-reference)[File-system conventions](https://nextjs.org/docs/pages/api-reference/file-conventions)src DirectoryYou are currently viewing the documentation for Pages Router.

# src Directory

Last updated  April 24, 2025

As an alternative to having the special Next.js `app` or `pages` directories in the root of your project, Next.js also supports the common pattern of placing application code under the `src` folder.

This separates application code from project configuration files which mostly live in the root of a project, which is preferred by some individuals and teams.

To use the `src` folder, move the `app` Router folder or `pages` Router folder to `src/app` or `src/pages` respectively.

 ![An example folder structure with the `src` folder](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-src-directory.png&w=3840&q=75)![An example folder structure with the `src` folder](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-src-directory.png&w=3840&q=75)

> **Good to know**:
>
>
>
> - The `/public` directory should remain in the root of your project.
> - Config files like `package.json`, `next.config.js` and `tsconfig.json` should remain in the root of your project.
> - `.env.*` files should remain in the root of your project.
> - `src/app` or `src/pages` will be ignored if `app` or `pages` are present in the root directory.
> - If you're using `src`, you'll probably also move other application folders such as `/components` or `/lib`.
> - If you're using Proxy, ensure it is placed inside the `src` folder.
> - If you're using Tailwind CSS, you'll need to add the `/src` prefix to the `tailwind.config.js` file in the [content section](https://tailwindcss.com/docs/content-configuration).
> - If you are using TypeScript paths for imports such as `@/*`, you should update the `paths` object in `tsconfig.json` to include `src/`.

Was this helpful?

supported.

---

# File

> API Reference for Next.js file-system conventions.

[Pages Router](https://nextjs.org/docs/pages)[API Reference](https://nextjs.org/docs/pages/api-reference)File-system conventionsYou are currently viewing the documentation for Pages Router.

# File-system conventions

Last updated  April 24, 2025[instrumentation.jsAPI reference for the instrumentation.js file.](https://nextjs.org/docs/pages/api-reference/file-conventions/instrumentation)[ProxyLearn how to use Proxy to run code before a request is completed.](https://nextjs.org/docs/pages/api-reference/file-conventions/proxy)[publicNext.js allows you to serve static files, like images, in the public directory. You can learn how it works here.](https://nextjs.org/docs/pages/api-reference/file-conventions/public-folder)[src DirectorySave pages under the `src` folder as an alternative to the root `pages` directory.](https://nextjs.org/docs/pages/api-reference/file-conventions/src-folder)

Was this helpful?

supported.

---

# getInitialProps

> Fetch dynamic data on the server for your React component with getInitialProps.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)getInitialPropsYou are currently viewing the documentation for Pages Router.

# getInitialProps

Last updated  November 24, 2025

> **Good to know**: `getInitialProps` is a legacy API. We recommend using [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) or [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props) instead.

`getInitialProps` is an `async` function that can be added to the default exported React component for the page. It will run on both the server-side and again on the client-side during page transitions. The result of the function will be forwarded to the React component as `props`.

 pages/index.tsxJavaScriptTypeScript

```
import { NextPageContext } from 'next'

Page.getInitialProps = async (ctx: NextPageContext) => {
  const res = await fetch('https://api.github.com/repos/vercel/next.js')
  const json = await res.json()
  return { stars: json.stargazers_count }
}

export default function Page({ stars }: { stars: number }) {
  return stars
}
```

> **Good to know**:
>
>
>
> - Data returned from `getInitialProps` is serialized when server rendering. Ensure the returned object from `getInitialProps` is a plain `Object`, and not using `Date`, `Map` or `Set`.
> - For the initial page load, `getInitialProps` will run on the server only. `getInitialProps` will then also run on the client when navigating to a different route with the [next/link](https://nextjs.org/docs/pages/api-reference/components/link) component or by using [next/router](https://nextjs.org/docs/pages/api-reference/functions/use-router).
> - If `getInitialProps` is used in a custom `_app.js`, and the page being navigated to is using `getServerSideProps`, then `getInitialProps` will **only** run on the server.

## Context Object

`getInitialProps` receives a single argument called `context`, which is an object with the following properties:

| Name | Description |
| --- | --- |
| pathname | Current route, the path of the page in/pages |
| query | Query string of the URL, parsed as an object |
| asPath | Stringof the actual path (including the query) shown in the browser |
| req | HTTP request object(server only) |
| res | HTTP response object(server only) |
| err | Error object if any error is encountered during the rendering |

## Caveats

- `getInitialProps` can only be used in `pages/` top level files, and not in nested components. To have nested data fetching at the component level, consider exploring the [App Router](https://nextjs.org/docs/app/getting-started/fetching-data).
- Regardless of whether your route is static or dynamic, any data returned from `getInitialProps` as `props` will be able to be examined on the client-side in the initial HTML. This is to allow the page to be [hydrated](https://react.dev/reference/react-dom/hydrate) correctly. Make sure that you don't pass any sensitive information that shouldn't be available on the client in `props`.

Was this helpful?

supported.
