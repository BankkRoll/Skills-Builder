# Basic Auth Middleware​ and more

# Basic Auth Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Basic Auth Middleware​

This middleware can apply Basic authentication to a specified path. Implementing Basic authentication with Cloudflare Workers or other platforms is more complicated than it seems, but with this middleware, it's a breeze.

For more information about how the Basic auth scheme works under the hood, see the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#basic_authentication_scheme).

## Import​

ts

```
import { Hono } from 'hono'
import { basicAuth } from 'hono/basic-auth'
```

## Usage​

ts

```
const app = new Hono()

app.use(
  '/auth/*',
  basicAuth({
    username: 'hono',
    password: 'acoolproject',
  })
)

app.get('/auth/page', (c) => {
  return c.text('You are authorized')
})
```

To restrict to a specific route + method:

ts

```
const app = new Hono()

app.get('/auth/page', (c) => {
  return c.text('Viewing page')
})

app.delete(
  '/auth/page',
  basicAuth({ username: 'hono', password: 'acoolproject' }),
  (c) => {
    return c.text('Page deleted')
  }
)
```

If you want to verify the user by yourself, specify the `verifyUser` option; returning `true` means it is accepted.

ts

```
const app = new Hono()

app.use(
  basicAuth({
    verifyUser: (username, password, c) => {
      return (
        username === 'dynamic-user' && password === 'hono-password'
      )
    },
  })
)
```

## Options​

### requiredusername:string​

The username of the user who is authenticating.

### requiredpassword:string​

The password value for the provided username to authenticate against.

### optionalrealm:string​

The domain name of the realm, as part of the returned WWW-Authenticate challenge header. The default is `"Secure Area"`.
 See more: [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate#directives](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate#directives)

### optionalhashFunction:Function​

A function to handle hashing for safe comparison of passwords.

### optionalverifyUser:(username: string, password: string, c: Context) => boolean | Promise<boolean>​

The function to verify the user.

### optionalinvalidUserMessage:string | object | MessageFunction​

`MessageFunction` is `(c: Context) => string | object | Promise<string | object>`. The custom message if the user is invalid.

## More Options​

### optional...users:{ username: string, password: string }[]​

## Recipes​

### Defining Multiple Users​

This middleware also allows you to pass arbitrary parameters containing objects defining more `username` and `password` pairs.

ts

```
app.use(
  '/auth/*',
  basicAuth(
    {
      username: 'hono',
      password: 'acoolproject',
      // Define other params in the first object
      realm: 'www.example.com',
    },
    {
      username: 'hono-admin',
      password: 'super-secure',
      // Cannot redefine other params here
    },
    {
      username: 'hono-user-1',
      password: 'a-secret',
      // Or here
    }
  )
)
```

Or less hardcoded:

ts

```
import { users } from '../config/users'

app.use(
  '/auth/*',
  basicAuth(
    {
      realm: 'www.example.com',
      ...users[0],
    },
    ...users.slice(1)
  )
)
```

---

# Bearer Auth Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Bearer Auth Middleware​

The Bearer Auth Middleware provides authentication by verifying an API token in the Request header. The HTTP clients accessing the endpoint will add the `Authorization` header with `Bearer {token}` as the header value.

Using `curl` from the terminal, it would look like this:

sh

```
curl -H 'Authorization: Bearer honoiscool' http://localhost:8787/auth/page
```

## Import​

ts

```
import { Hono } from 'hono'
import { bearerAuth } from 'hono/bearer-auth'
```

## Usage​

NOTE

Your `token` must match the regex `/[A-Za-z0-9._~+/-]+=*/`, otherwise a 400 error will be returned. Notably, this regex accommodates both URL-safe Base64- and standard Base64-encoded JWTs. This middleware does not require the bearer token to be a JWT, just that it matches the above regex.

ts

```
const app = new Hono()

const token = 'honoiscool'

app.use('/api/*', bearerAuth({ token }))

app.get('/api/page', (c) => {
  return c.json({ message: 'You are authorized' })
})
```

To restrict to a specific route + method:

ts

```
const app = new Hono()

const token = 'honoiscool'

app.get('/api/page', (c) => {
  return c.json({ message: 'Read posts' })
})

app.post('/api/page', bearerAuth({ token }), (c) => {
  return c.json({ message: 'Created post!' }, 201)
})
```

To implement multiple tokens (E.g., any valid token can read but create/update/delete are restricted to a privileged token):

ts

```
const app = new Hono()

const readToken = 'read'
const privilegedToken = 'read+write'
const privilegedMethods = ['POST', 'PUT', 'PATCH', 'DELETE']

app.on('GET', '/api/page/*', async (c, next) => {
  // List of valid tokens
  const bearer = bearerAuth({ token: [readToken, privilegedToken] })
  return bearer(c, next)
})
app.on(privilegedMethods, '/api/page/*', async (c, next) => {
  // Single valid privileged token
  const bearer = bearerAuth({ token: privilegedToken })
  return bearer(c, next)
})

// Define handlers for GET, POST, etc.
```

If you want to verify the value of the token yourself, specify the `verifyToken` option; returning `true` means it is accepted.

ts

```
const app = new Hono()

app.use(
  '/auth-verify-token/*',
  bearerAuth({
    verifyToken: async (token, c) => {
      return token === 'dynamic-token'
    },
  })
)
```

## Options​

### requiredtoken:string|string[]​

The string to validate the incoming bearer token against.

### optionalrealm:string​

The domain name of the realm, as part of the returned WWW-Authenticate challenge header. The default is `""`. See more: [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate#directives](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate#directives)

### optionalprefix:string​

The prefix (or known as `schema`) for the Authorization header value. The default is `"Bearer"`.

### optionalheaderName:string​

The header name. The default value is `Authorization`.

### optionalhashFunction:Function​

A function to handle hashing for safe comparison of authentication tokens.

### optionalverifyToken:(token: string, c: Context) => boolean | Promise<boolean>​

The function to verify the token.

### optionalnoAuthenticationHeader:object​

Customizes the error response when the request does not have an authentication header.

- `wwwAuthenticateHeader`: `string | object | MessageFunction` - Customizes the WWW-Authenticate header value.
- `message`: `string | object | MessageFunction` - The custom message for the response body.

`MessageFunction` is `(c: Context) => string | object | Promise<string | object>`.

### optionalinvalidAuthenticationHeader:object​

Customizes the error response when the authentication header format is invalid.

- `wwwAuthenticateHeader`: `string | object | MessageFunction` - Customizes the WWW-Authenticate header value.
- `message`: `string | object | MessageFunction` - The custom message for the response body.

### optionalinvalidToken:object​

Customizes the error response when the token is invalid.

- `wwwAuthenticateHeader`: `string | object | MessageFunction` - Customizes the WWW-Authenticate header value.
- `message`: `string | object | MessageFunction` - The custom message for the response body.

---

# Body Limit Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Body Limit Middleware​

The Body Limit Middleware can limit the file size of the request body.

This middleware first uses the value of the `Content-Length` header in the request, if present. If it is not set, it reads the body in the stream and executes an error handler if it is larger than the specified file size.

## Import​

ts

```
import { Hono } from 'hono'
import { bodyLimit } from 'hono/body-limit'
```

## Usage​

ts

```
const app = new Hono()

app.post(
  '/upload',
  bodyLimit({
    maxSize: 50 * 1024, // 50kb
    onError: (c) => {
      return c.text('overflow :(', 413)
    },
  }),
  async (c) => {
    const body = await c.req.parseBody()
    if (body['file'] instanceof File) {
      console.log(`Got file sized: ${body['file'].size}`)
    }
    return c.text('pass :)')
  }
)
```

## Options​

### requiredmaxSize:number​

The maximum file size of the file you want to limit. The default is `100 * 1024` - `100kb`.

### optionalonError:OnError​

The error handler to be invoked if the specified file size is exceeded.

## Usage with Bun for large requests​

If the Body Limit Middleware is used explicitly to allow a request body larger than the default, it might be necessary to make changes to your `Bun.serve` configuration accordingly. [At the time of writing](https://github.com/oven-sh/bun/blob/f2cfa15e4ef9d730fc6842ad8b79fb7ab4c71cb9/packages/bun-types/bun.d.ts#L2191), `Bun.serve`'s default request body limit is 128MiB. If you set Hono's Body Limit Middleware to a value bigger than that, your requests will still fail and, additionally, the `onError` handler specified in the middleware will not be called. This is because `Bun.serve()` will set the status code to `413` and terminate the connection before passing the request to Hono.

If you want to accept requests larger than 128MiB with Hono and Bun, you need to set the limit for Bun as well:

ts

```
export default {
  port: process.env['PORT'] || 3000,
  fetch: app.fetch,
  maxRequestBodySize: 1024 * 1024 * 200, // your value here
}
```

or, depending on your setup:

ts

```
Bun.serve({
  fetch(req, server) {
    return app.fetch(req, { ip: server.requestIP(req) })
  },
  maxRequestBodySize: 1024 * 1024 * 200, // your value here
})
```

---

# Cache Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Cache Middleware​

The Cache middleware uses the Web Standards' [Cache API](https://developer.mozilla.org/en-US/docs/Web/API/Cache).

The Cache middleware currently supports Cloudflare Workers projects using custom domains and Deno projects using [Deno 1.26+](https://github.com/denoland/deno/releases/tag/v1.26.0). Also available with Deno Deploy.

Cloudflare Workers respects the `Cache-Control` header and return cached responses. For details, refer to [Cache on Cloudflare Docs](https://developers.cloudflare.com/workers/runtime-apis/cache/). Deno does not respect headers, so if you need to update the cache, you will need to implement your own mechanism.

See [Usage](#usage) below for instructions on each platform.

## Import​

ts

```
import { Hono } from 'hono'
import { cache } from 'hono/cache'
```

## Usage​

Cloudflare WorkersDenots

```
app.get(
  '*',
  cache({
    cacheName: 'my-app',
    cacheControl: 'max-age=3600',
  })
)
```

ts

```
// Must use `wait: true` for the Deno runtime
app.get(
  '*',
  cache({
    cacheName: 'my-app',
    cacheControl: 'max-age=3600',
    wait: true,
  })
)
```

## Options​

### requiredcacheName:string|(c: Context) => string|Promise<string>​

The name of the cache. Can be used to store multiple caches with different identifiers.

### optionalwait:boolean​

A boolean indicating if Hono should wait for the Promise of the `cache.put` function to resolve before continuing with the request. *Required to be true for the Deno environment*. The default is `false`.

### optionalcacheControl:string​

A string of directives for the `Cache-Control` header. See the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control) for more information. When this option is not provided, no `Cache-Control` header is added to requests.

### optionalvary:string|string[]​

Sets the `Vary` header in the response. If the original response header already contains a `Vary` header, the values are merged, removing any duplicates. Setting this to `*` will result in an error. For more details on the Vary header and its implications for caching strategies, refer to the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary).

### optionalkeyGenerator:(c: Context) => string | Promise<string>​

Generates keys for every request in the `cacheName` store. This can be used to cache data based on request parameters or context parameters. The default is `c.req.url`.

### optionalcacheableStatusCodes:number[]​

An array of status codes that should be cached. The default is `[200]`. Use this option to cache responses with specific status codes.

ts

```
app.get(
  '*',
  cache({
    cacheName: 'my-app',
    cacheControl: 'max-age=3600',
    cacheableStatusCodes: [200, 404, 412],
  })
)
```

---

# Combine Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Combine Middleware​

Combine Middleware combines multiple middleware functions into a single middleware. It provides three functions:

- `some` - Runs only one of the given middleware.
- `every` - Runs all given middleware.
- `except` - Runs all given middleware only if a condition is not met.

## Import​

ts

```
import { Hono } from 'hono'
import { some, every, except } from 'hono/combine'
```

## Usage​

Here's an example of complex access control rules using Combine Middleware.

ts

```
import { Hono } from 'hono'
import { bearerAuth } from 'hono/bearer-auth'
import { getConnInfo } from 'hono/cloudflare-workers'
import { every, some } from 'hono/combine'
import { ipRestriction } from 'hono/ip-restriction'
import { rateLimit } from '@/my-rate-limit'

const app = new Hono()

app.use(
  '*',
  some(
    every(
      ipRestriction(getConnInfo, { allowList: ['192.168.0.2'] }),
      bearerAuth({ token })
    ),
    // If both conditions are met, rateLimit will not execute.
    rateLimit()
  )
)

app.get('/', (c) => c.text('Hello Hono!'))
```

### some​

Runs the first middleware that returns true. Middleware is applied in order, and if any middleware exits successfully, subsequent middleware will not run.

ts

```
import { some } from 'hono/combine'
import { bearerAuth } from 'hono/bearer-auth'
import { myRateLimit } from '@/rate-limit'

// If client has a valid token, skip rate limiting.
// Otherwise, apply rate limiting.
app.use(
  '/api/*',
  some(bearerAuth({ token }), myRateLimit({ limit: 100 }))
)
```

### every​

Runs all middleware and stops if any of them fail. Middleware is applied in order, and if any middleware throws an error, subsequent middleware will not run.

ts

```
import { some, every } from 'hono/combine'
import { bearerAuth } from 'hono/bearer-auth'
import { myCheckLocalNetwork } from '@/check-local-network'
import { myRateLimit } from '@/rate-limit'

// If client is in local network, skip authentication and rate limiting.
// Otherwise, apply authentication and rate limiting.
app.use(
  '/api/*',
  some(
    myCheckLocalNetwork(),
    every(bearerAuth({ token }), myRateLimit({ limit: 100 }))
  )
)
```

### except​

Runs all middleware except when the condition is met. You can pass a string or function as the condition. If multiple targets need to be matched, pass them as an array.

ts

```
import { except } from 'hono/combine'
import { bearerAuth } from 'hono/bearer-auth'

// If client is accessing public API, skip authentication.
// Otherwise, require a valid token.
app.use('/api/*', except('/api/public/*', bearerAuth({ token })))
```

---

# Compress Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Compress Middleware​

This middleware compresses the response body, according to `Accept-Encoding` request header.

INFO

**Note**: On Cloudflare Workers and Deno Deploy, the response body will be compressed automatically, so there is no need to use this middleware.

## Import​

ts

```
import { Hono } from 'hono'
import { compress } from 'hono/compress'
```

## Usage​

ts

```
const app = new Hono()

app.use(compress())
```

## Options​

### optionalencoding:'gzip'|'deflate'​

The compression scheme to allow for response compression. Either `gzip` or `deflate`. If not defined, both are allowed and will be used based on the `Accept-Encoding` header. `gzip` is prioritized if this option is not provided and the client provides both in the `Accept-Encoding` header.

### optionalthreshold:number​

The minimum size in bytes to compress. Defaults to 1024 bytes.

---

# Context Storage Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Context Storage Middleware​

The Context Storage Middleware stores the Hono `Context` in the `AsyncLocalStorage`, to make it globally accessible.

INFO

**Note** This middleware uses `AsyncLocalStorage`. The runtime should support it.

**Cloudflare Workers**: To enable `AsyncLocalStorage`, add the [nodejs_compatornodejs_alsflag](https://developers.cloudflare.com/workers/configuration/compatibility-dates/#nodejs-compatibility-flag) to your `wrangler.toml` file.

## Import​

ts

```
import { Hono } from 'hono'
import {
  contextStorage,
  getContext,
  tryGetContext,
} from 'hono/context-storage'
```

## Usage​

The `getContext()` will return the current Context object if the `contextStorage()` is applied as a middleware.

ts

```
type Env = {
  Variables: {
    message: string
  }
}

const app = new Hono<Env>()

app.use(contextStorage())

app.use(async (c, next) => {
  c.set('message', 'Hello!')
  await next()
})

// You can access the variable outside the handler.
const getMessage = () => {
  return getContext<Env>().var.message
}

app.get('/', (c) => {
  return c.text(getMessage())
})
```

On Cloudflare Workers, you can access the bindings outside the handler.

ts

```
type Env = {
  Bindings: {
    KV: KVNamespace
  }
}

const app = new Hono<Env>()

app.use(contextStorage())

const setKV = (value: string) => {
  return getContext<Env>().env.KV.put('key', value)
}
```

## tryGetContext​

`tryGetContext()` works like `getContext()`, but returns `undefined` instead of throwing an error when the context is not available:

ts

```
const context = tryGetContext<Env>()
if (context) {
  // Context is available
  console.log(context.var.message)
}
```

---

# CORS Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# CORS Middleware​

There are many use cases of Cloudflare Workers as Web APIs and calling them from external front-end application. For them we have to implement CORS, let's do this with middleware as well.

## Import​

ts

```
import { Hono } from 'hono'
import { cors } from 'hono/cors'
```

## Usage​

ts

```
const app = new Hono()

// CORS should be called before the route
app.use('/api/*', cors())
app.use(
  '/api2/*',
  cors({
    origin: 'http://example.com',
    allowHeaders: ['X-Custom-Header', 'Upgrade-Insecure-Requests'],
    allowMethods: ['POST', 'GET', 'OPTIONS'],
    exposeHeaders: ['Content-Length', 'X-Kuma-Revision'],
    maxAge: 600,
    credentials: true,
  })
)

app.all('/api/abc', (c) => {
  return c.json({ success: true })
})
app.all('/api2/abc', (c) => {
  return c.json({ success: true })
})
```

Multiple origins:

ts

```
app.use(
  '/api3/*',
  cors({
    origin: ['https://example.com', 'https://example.org'],
  })
)

// Or you can use "function"
app.use(
  '/api4/*',
  cors({
    // `c` is a `Context` object
    origin: (origin, c) => {
      return origin.endsWith('.example.com')
        ? origin
        : 'http://example.com'
    },
  })
)
```

Dynamic allowed methods based on origin:

ts

```
app.use(
  '/api5/*',
  cors({
    origin: (origin) =>
      origin === 'https://example.com' ? origin : '*',
    // `c` is a `Context` object
    allowMethods: (origin, c) =>
      origin === 'https://example.com'
        ? ['GET', 'HEAD', 'POST', 'PATCH', 'DELETE']
        : ['GET', 'HEAD'],
  })
)
```

## Options​

### optionalorigin:string|string[]|(origin:string, c:Context) => string​

The value of "*Access-Control-Allow-Origin*" CORS header. You can also pass the callback function like `origin: (origin) => (origin.endsWith('.example.com') ? origin : 'http://example.com')`. The default is `*`.

### optionalallowMethods:string[]|(origin:string, c:Context) => string[]​

The value of "*Access-Control-Allow-Methods*" CORS header. You can also pass a callback function to dynamically determine allowed methods based on the origin. The default is `['GET', 'HEAD', 'PUT', 'POST', 'DELETE', 'PATCH']`.

### optionalallowHeaders:string[]​

The value of "*Access-Control-Allow-Headers*" CORS header. The default is `[]`.

### optionalmaxAge:number​

The value of "*Access-Control-Max-Age*" CORS header.

### optionalcredentials:boolean​

The value of "*Access-Control-Allow-Credentials*" CORS header.

### optionalexposeHeaders:string[]​

The value of "*Access-Control-Expose-Headers*" CORS header. The default is `[]`.

## Environment-dependent CORS configuration​

If you want to adjust CORS configuration according to the execution environment, such as development or production, injecting values from environment variables is convenient as it eliminates the need for the application to be aware of its own execution environment. See the example below for clarification.

ts

```
app.use('*', async (c, next) => {
  const corsMiddlewareHandler = cors({
    origin: c.env.CORS_ORIGIN,
  })
  return corsMiddlewareHandler(c, next)
})
```

## Using with Vite​

When using Hono with Vite, you should disable Vite's built-in CORS feature by setting `server.cors` to `false` in your `vite.config.ts`. This prevents conflicts with Hono's CORS middleware.

ts

```
// vite.config.ts
import { cloudflare } from '@cloudflare/vite-plugin'
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    cors: false, // disable Vite's built-in CORS setting
  },
  plugins: [cloudflare()],
})
```

---

# CSRF Protection​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# CSRF Protection​

This middleware protects against CSRF attacks by checking both the `Origin` header and the `Sec-Fetch-Site` header. The request is allowed if either validation passes.

The middleware only validates requests that:

- Use unsafe HTTP methods (not GET, HEAD, or OPTIONS)
- Have content types that can be sent by HTML forms (`application/x-www-form-urlencoded`, `multipart/form-data`, or `text/plain`)

Old browsers that do not send `Origin` headers, or environments that use reverse proxies to remove these headers, may not work well. In such environments, use other CSRF token methods.

## Import​

ts

```
import { Hono } from 'hono'
import { csrf } from 'hono/csrf'
```

## Usage​

ts

```
const app = new Hono()

// Default: both origin and sec-fetch-site validation
app.use(csrf())

// Allow specific origins
app.use(csrf({ origin: 'https://myapp.example.com' }))

// Allow multiple origins
app.use(
  csrf({
    origin: [
      'https://myapp.example.com',
      'https://development.myapp.example.com',
    ],
  })
)

// Allow specific sec-fetch-site values
app.use(csrf({ secFetchSite: 'same-origin' }))
app.use(csrf({ secFetchSite: ['same-origin', 'none'] }))

// Dynamic origin validation
// It is strongly recommended that the protocol be verified to ensure a match to `$`.
// You should *never* do a forward match.
app.use(
  '*',
  csrf({
    origin: (origin) =>
      /https:\/\/(\w+\.)?myapp\.example\.com$/.test(origin),
  })
)

// Dynamic sec-fetch-site validation
app.use(
  csrf({
    secFetchSite: (secFetchSite, c) => {
      // Always allow same-origin
      if (secFetchSite === 'same-origin') return true
      // Allow cross-site for webhook endpoints
      if (
        secFetchSite === 'cross-site' &&
        c.req.path.startsWith('/webhook/')
      ) {
        return true
      }
      return false
    },
  })
)
```

## Options​

### optionalorigin:string|string[]|Function​

Specify allowed origins for CSRF protection.

- **string**: Single allowed origin (e.g., `'https://example.com'`)
- **string[]**: Array of allowed origins
- **Function**: Custom handler `(origin: string, context: Context) => boolean` for flexible origin validation and bypass logic

**Default**: Only same origin as the request URL

The function handler receives the request's `Origin` header value and the request context, allowing for dynamic validation based on request properties like path, headers, or other context data.

### optionalsecFetchSite:string|string[]|Function​

Specify allowed Sec-Fetch-Site header values for CSRF protection using [Fetch Metadata](https://web.dev/articles/fetch-metadata).

- **string**: Single allowed value (e.g., `'same-origin'`)
- **string[]**: Array of allowed values (e.g., `['same-origin', 'none']`)
- **Function**: Custom handler `(secFetchSite: string, context: Context) => boolean` for flexible validation

**Default**: Only allows `'same-origin'`

Standard Sec-Fetch-Site values:

- `same-origin`: Request from same origin
- `same-site`: Request from same site (different subdomain)
- `cross-site`: Request from different site
- `none`: Request not from a web page (e.g., browser address bar, bookmark)

The function handler receives the request's `Sec-Fetch-Site` header value and the request context, enabling dynamic validation based on request properties.

---

# ETag Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# ETag Middleware​

Using this middleware, you can add ETag headers easily.

## Import​

ts

```
import { Hono } from 'hono'
import { etag } from 'hono/etag'
```

## Usage​

ts

```
const app = new Hono()

app.use('/etag/*', etag())
app.get('/etag/abc', (c) => {
  return c.text('Hono is cool')
})
```

## The retained headers​

The 304 Response must include the headers that would have been sent in an equivalent 200 OK response. The default headers are Cache-Control, Content-Location, Date, ETag, Expires, and Vary.

If you want to add the header that is sent, you can use `retainedHeaders` option and `RETAINED_304_HEADERS` strings array variable that includes the default headers:

ts

```
import { etag, RETAINED_304_HEADERS } from 'hono/etag'

// ...

app.use(
  '/etag/*',
  etag({
    retainedHeaders: ['x-message', ...RETAINED_304_HEADERS],
  })
)
```

## Options​

### optionalweak:boolean​

Define using or not using a [weak validation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests#weak_validation). If `true` is set, then `w/` is added to the prefix of the value. The default is `false`.

### optionalretainedHeaders:string[]​

The headers that you want to retain in the 304 Response.

### optionalgenerateDigest:(body: Uint8Array) => ArrayBuffer | Promise<ArrayBuffer>​

A custom digest generation function. By default, it uses `SHA-1`. This function is called with the response body as a `Uint8Array` and should return a hash as an `ArrayBuffer` or a Promise of one.

---

# IP Restriction Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# IP Restriction Middleware​

IP Restriction Middleware is middleware that limits access to resources based on the IP address of the user.

## Import​

ts

```
import { Hono } from 'hono'
import { ipRestriction } from 'hono/ip-restriction'
```

## Usage​

For your application running on Bun, if you want to allow access only from local, you can write it as follows. Specify the rules you want to deny in the `denyList` and the rules you want to allow in the `allowList`.

ts

```
import { Hono } from 'hono'
import { getConnInfo } from 'hono/bun'
import { ipRestriction } from 'hono/ip-restriction'

const app = new Hono()

app.use(
  '*',
  ipRestriction(getConnInfo, {
    denyList: [],
    allowList: ['127.0.0.1', '::1'],
  })
)

app.get('/', (c) => c.text('Hello Hono!'))
```

Pass the `getConninfo` from the [ConnInfo helper](https://hono.dev/docs/helpers/conninfo) appropriate for your environment as the first argument of `ipRestriction`. For example, for Deno, it would look like this:

ts

```
import { getConnInfo } from 'hono/deno'
import { ipRestriction } from 'hono/ip-restriction'

//...

app.use(
  '*',
  ipRestriction(getConnInfo, {
    // ...
  })
)
```

## Rules​

Follow the instructions below for writing rules.

### IPv4​

- `192.168.2.0` - Static IP Address
- `192.168.2.0/24` - CIDR Notation
- `*` - ALL Addresses

### IPv6​

- `::1` - Static IP Address
- `::1/10` - CIDR Notation
- `*` - ALL Addresses

## Error handling​

To customize the error, return a `Response` in the third argument.

ts

```
app.use(
  '*',
  ipRestriction(
    getConnInfo,
    {
      denyList: ['192.168.2.0/24'],
    },
    async (remote, c) => {
      return c.text(`Blocking access from ${remote.addr}`, 403)
    }
  )
)
```

---

# JSX Renderer Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# JSX Renderer Middleware​

JSX Renderer Middleware allows you to set up the layout when rendering JSX with the `c.render()` function, without the need for using `c.setRenderer()`. Additionally, it enables access to instances of Context within components through the use of `useRequestContext()`.

## Import​

ts

```
import { Hono } from 'hono'
import { jsxRenderer, useRequestContext } from 'hono/jsx-renderer'
```

## Usage​

jsx

```
const app = new Hono()

app.get(
  '/page/*',
  jsxRenderer(({ children }) => {
    return (
      <html>
        <body>
          <header>Menu</header>
          <div>{children}</div>
        </body>
      </html>
    )
  })
)

app.get('/page/about', (c) => {
  return c.render(<h1>About me!</h1>)
})
```

## Options​

### optionaldocType:boolean|string​

If you do not want to add a DOCTYPE at the beginning of the HTML, set the `docType` option to `false`.

tsx

```
app.use(
  '*',
  jsxRenderer(
    ({ children }) => {
      return (
        <html>
          <body>{children}</body>
        </html>
      )
    },
    { docType: false }
  )
)
```

And you can specify the DOCTYPE.

tsx

```
app.use(
  '*',
  jsxRenderer(
    ({ children }) => {
      return (
        <html>
          <body>{children}</body>
        </html>
      )
    },
    {
      docType:
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
    }
  )
)
```

### optionalstream:boolean|Record<string, string>​

If you set it to `true` or provide a Record value, it will be rendered as a streaming response.

tsx

```
const AsyncComponent = async () => {
  await new Promise((r) => setTimeout(r, 1000)) // sleep 1s
  return <div>Hi!</div>
}

app.get(
  '*',
  jsxRenderer(
    ({ children }) => {
      return (
        <html>
          <body>
            <h1>SSR Streaming</h1>
            {children}
          </body>
        </html>
      )
    },
    { stream: true }
  )
)

app.get('/', (c) => {
  return c.render(
    <Suspense fallback={<div>loading...</div>}>
      <AsyncComponent />
    </Suspense>
  )
})
```

If `true` is set, the following headers are added:

ts

```
{
  'Transfer-Encoding': 'chunked',
  'Content-Type': 'text/html; charset=UTF-8',
  'Content-Encoding': 'Identity'
}
```

You can customize the header values by specifying the Record values.

## Nested Layouts​

The `Layout` component enables nesting the layouts.

tsx

```
app.use(
  jsxRenderer(({ children }) => {
    return (
      <html>
        <body>{children}</body>
      </html>
    )
  })
)

const blog = new Hono()
blog.use(
  jsxRenderer(({ children, Layout }) => {
    return (
      <Layout>
        <nav>Blog Menu</nav>
        <div>{children}</div>
      </Layout>
    )
  })
)

app.route('/blog', blog)
```

## useRequestContext()​

`useRequestContext()` returns an instance of Context.

tsx

```
import { useRequestContext, jsxRenderer } from 'hono/jsx-renderer'

const app = new Hono()
app.use(jsxRenderer())

const RequestUrlBadge: FC = () => {
  const c = useRequestContext()
  return <b>{c.req.url}</b>
}

app.get('/page/info', (c) => {
  return c.render(
    <div>
      You are accessing: <RequestUrlBadge />
    </div>
  )
})
```

WARNING

You can't use `useRequestContext()` with the Deno's `precompile` JSX option. Use the `react-jsx`:

json

```
"compilerOptions": {
     "jsx": "precompile",
     "jsx": "react-jsx",
     "jsxImportSource": "hono/jsx"
   }
 }
```

## ExtendingContextRenderer​

By defining `ContextRenderer` as shown below, you can pass additional content to the renderer. This is handy, for instance, when you want to change the contents of the head tag depending on the page.

tsx

```
declare module 'hono' {
  interface ContextRenderer {
    (
      content: string | Promise<string>,
      props: { title: string }
    ): Response
  }
}

const app = new Hono()

app.get(
  '/page/*',
  jsxRenderer(({ children, title }) => {
    return (
      <html>
        <head>
          <title>{title}</title>
        </head>
        <body>
          <header>Menu</header>
          <div>{children}</div>
        </body>
      </html>
    )
  })
)

app.get('/page/favorites', (c) => {
  return c.render(
    <div>
      <ul>
        <li>Eating sushi</li>
        <li>Watching baseball games</li>
      </ul>
    </div>,
    {
      title: 'My favorites',
    }
  )
})
```

---

# JWK Auth Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# JWK Auth Middleware​

The JWK Auth Middleware authenticates requests by verifying tokens using JWK (JSON Web Key). It checks for an `Authorization` header and other configured sources, such as cookies, if specified. Specifically, it validates tokens using the provided `keys`, retrieves keys from `jwks_uri` if specified, and supports token extraction from cookies if the `cookie` option is set.

INFO

The Authorization header sent from the client must have a specified scheme.

Example: `Bearer my.token.value` or `Basic my.token.value`

## Import​

ts

```
import { Hono } from 'hono'
import { jwk } from 'hono/jwk'
import { verifyWithJwks } from 'hono/jwt'
```

## Usage​

ts

```
const app = new Hono()

app.use(
  '/auth/*',
  jwk({
    jwks_uri: `https://${backendServer}/.well-known/jwks.json`,
  })
)

app.get('/auth/page', (c) => {
  return c.text('You are authorized')
})
```

Get payload:

ts

```
const app = new Hono()

app.use(
  '/auth/*',
  jwk({
    jwks_uri: `https://${backendServer}/.well-known/jwks.json`,
  })
)

app.get('/auth/page', (c) => {
  const payload = c.get('jwtPayload')
  return c.json(payload) // eg: { "sub": "1234567890", "name": "John Doe", "iat": 1516239022 }
})
```

Anonymous access:

ts

```
const app = new Hono()

app.use(
  '/auth/*',
  jwk({
    jwks_uri: (c) =>
      `https://${c.env.authServer}/.well-known/jwks.json`,
    allow_anon: true,
  })
)

app.get('/auth/page', (c) => {
  const payload = c.get('jwtPayload')
  return c.json(payload ?? { message: 'hello anon' })
})
```

## UsingverifyWithJwksoutside of middleware​

The `verifyWithJwks` utility function can be used to verify JWT tokens outside of Hono's middleware context, such as in SvelteKit SSR pages or other server-side environments:

ts

```
const id_payload = await verifyWithJwks(
  id_token,
  {
    jwks_uri: 'https://your-auth-server/.well-known/jwks.json',
    allowedAlgorithms: ['RS256'],
  },
  {
    cf: { cacheEverything: true, cacheTtl: 3600 },
  }
)
```

## Options​

### optionalkeys:HonoJsonWebKey[] | (c: Context) => Promise<HonoJsonWebKey[]>​

The values of your public keys, or a function that returns them. The function receives the Context object.

### optionaljwks_uri:string|(c: Context) => Promise<string>​

If this value is set, attempt to fetch JWKs from this URI, expecting a JSON response with `keys`, which are added to the provided `keys` option. You can also pass a callback function to dynamically determine the JWKS URI using the Context.

### optionalallow_anon:boolean​

If this value is set to `true`, requests without a valid token will be allowed to pass through the middleware. Use `c.get('jwtPayload')` to check if the request is authenticated. The default is `false`.

### optionalcookie:string​

If this value is set, then the value is retrieved from the cookie header using that value as a key, which is then validated as a token.

### optionalheaderName:string​

The name of the header to look for the JWT token. The default is `Authorization`.

---

# JWT Auth Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# JWT Auth Middleware​

The JWT Auth Middleware provides authentication by verifying the token with JWT. The middleware will check for an `Authorization` header if the `cookie` option is not set. You can customize the header name using the `headerName` option.

INFO

The Authorization header sent from the client must have a specified scheme.

Example: `Bearer my.token.value` or `Basic my.token.value`

## Import​

ts

```
import { Hono } from 'hono'
import { jwt } from 'hono/jwt'
import type { JwtVariables } from 'hono/jwt'
```

## Usage​

ts

```
// Specify the variable types to infer the `c.get('jwtPayload')`:
type Variables = JwtVariables

const app = new Hono<{ Variables: Variables }>()

app.use(
  '/auth/*',
  jwt({
    secret: 'it-is-very-secret',
  })
)

app.get('/auth/page', (c) => {
  return c.text('You are authorized')
})
```

Get payload:

ts

```
const app = new Hono()

app.use(
  '/auth/*',
  jwt({
    secret: 'it-is-very-secret',
    issuer: 'my-trusted-issuer',
  })
)

app.get('/auth/page', (c) => {
  const payload = c.get('jwtPayload')
  return c.json(payload) // eg: { "sub": "1234567890", "name": "John Doe", "iat": 1516239022, "iss": "my-trusted-issuer" }
})
```

TIP

`jwt()` is just a middleware function. If you want to use an environment variable (eg: `c.env.JWT_SECRET`), you can use it as follows:

js

```
app.use('/auth/*', (c, next) => {
  const jwtMiddleware = jwt({
    secret: c.env.JWT_SECRET,
  })
  return jwtMiddleware(c, next)
})
```

## Options​

### requiredsecret:string​

A value of your secret key.

### optionalcookie:string​

If this value is set, then the value is retrieved from the cookie header using that value as a key, which is then validated as a token.

### optionalalg:string​

An algorithm type that is used for verifying. The default is `HS256`.

Available types are `HS256` | `HS384` | `HS512` | `RS256` | `RS384` | `RS512` | `PS256` | `PS384` | `PS512` | `ES256` | `ES384` | `ES512` | `EdDSA`.

### optionalheaderName:string​

The name of the header to look for the JWT token. The default is `Authorization`.

ts

```
app.use(
  '/auth/*',
  jwt({
    secret: 'it-is-very-secret',
    headerName: 'x-custom-auth-header',
  })
)
```

### optionalverifyOptions:VerifyOptions​

Options controlling verification of the token.

#### optionalverifyOptions.iss:string | RexExp​

The expected issuer used for token verification. The `iss` claim will **not** be checked if this isn't set.

#### optionalverifyOptions.nbf:boolean​

The `nbf` (not before) claim will be verified if present and this is set to `true`. The default is `true`.

#### optionalverifyOptions.iat:boolean​

The `iat` (not before) claim will be verified if present and this is set to `true`. The default is `true`.

#### optionalverifyOptions.exp:boolean​

The `exp` (not before) claim will be verified if present and this is set to `true`. The default is `true`.
