# Context​ and more

# Context​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Context​

The `Context` object is instantiated for each request and kept until the response is returned. You can put values in it, set headers and a status code you want to return, and access HonoRequest and Response objects.

## req​

`req` is an instance of HonoRequest. For more details, see [HonoRequest](https://hono.dev/docs/api/request).

ts

```
app.get('/hello', (c) => {
  const userAgent = c.req.header('User-Agent')
  // ...
})
```

## status()​

You can set an HTTP status code with `c.status()`. The default is `200`. You don't have to use `c.status()` if the code is `200`.

ts

```
app.post('/posts', (c) => {
  // Set HTTP status code
  c.status(201)
  return c.text('Your post is created!')
})
```

## header()​

You can set HTTP Headers for the response.

ts

```
app.get('/', (c) => {
  // Set headers
  c.header('X-Message', 'My custom message')
  return c.text('HellO!')
})
```

## body()​

Return an HTTP response.

INFO

**Note**: When returning text or HTML, it is recommended to use `c.text()` or `c.html()`.

ts

```
app.get('/welcome', (c) => {
  c.header('Content-Type', 'text/plain')
  // Return the response body
  return c.body('Thank you for coming')
})
```

You can also write the following.

ts

```
app.get('/welcome', (c) => {
  return c.body('Thank you for coming', 201, {
    'X-Message': 'Hello!',
    'Content-Type': 'text/plain',
  })
})
```

The response is the same `Response` object as below.

ts

```
new Response('Thank you for coming', {
  status: 201,
  headers: {
    'X-Message': 'Hello!',
    'Content-Type': 'text/plain',
  },
})
```

## text()​

Render text as `Content-Type:text/plain`.

ts

```
app.get('/say', (c) => {
  return c.text('Hello!')
})
```

## json()​

Render JSON as `Content-Type:application/json`.

ts

```
app.get('/api', (c) => {
  return c.json({ message: 'Hello!' })
})
```

## html()​

Render HTML as `Content-Type:text/html`.

ts

```
app.get('/', (c) => {
  return c.html('<h1>Hello! Hono!</h1>')
})
```

## notFound()​

Return a `Not Found` Response. You can customize it with [app.notFound()](https://hono.dev/docs/api/hono#not-found).

ts

```
app.get('/notfound', (c) => {
  return c.notFound()
})
```

## redirect()​

Redirect, default status code is `302`.

ts

```
app.get('/redirect', (c) => {
  return c.redirect('/')
})
app.get('/redirect-permanently', (c) => {
  return c.redirect('/', 301)
})
```

## res​

You can access the [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) object that will be returned.

ts

```
// Response object
app.use('/', async (c, next) => {
  await next()
  c.res.headers.append('X-Debug', 'Debug message')
})
```

## set() / get()​

Get and set arbitrary key-value pairs, with a lifetime of the current request. This allows passing specific values between middleware or from middleware to route handlers.

ts

```
app.use(async (c, next) => {
  c.set('message', 'Hono is cool!!')
  await next()
})

app.get('/', (c) => {
  const message = c.get('message')
  return c.text(`The message is "${message}"`)
})
```

Pass the `Variables` as Generics to the constructor of `Hono` to make it type-safe.

ts

```
type Variables = {
  message: string
}

const app = new Hono<{ Variables: Variables }>()
```

The value of `c.set` / `c.get` are retained only within the same request. They cannot be shared or persisted across different requests.

## var​

You can also access the value of a variable with `c.var`.

ts

```
const result = c.var.client.oneMethod()
```

If you want to create the middleware which provides a custom method, write like the following:

ts

```
type Env = {
  Variables: {
    echo: (str: string) => string
  }
}

const app = new Hono()

const echoMiddleware = createMiddleware<Env>(async (c, next) => {
  c.set('echo', (str) => str)
  await next()
})

app.get('/echo', echoMiddleware, (c) => {
  return c.text(c.var.echo('Hello!'))
})
```

If you want to use the middleware in multiple handlers, you can use `app.use()`. Then, you have to pass the `Env` as Generics to the constructor of `Hono` to make it type-safe.

ts

```
const app = new Hono<Env>()

app.use(echoMiddleware)

app.get('/echo', (c) => {
  return c.text(c.var.echo('Hello!'))
})
```

## render() / setRenderer()​

You can set a layout using `c.setRenderer()` within a custom middleware.

tsx

```
app.use(async (c, next) => {
  c.setRenderer((content) => {
    return c.html(
      <html>
        <body>
          <p>{content}</p>
        </body>
      </html>
    )
  })
  await next()
})
```

Then, you can utilize `c.render()` to create responses within this layout.

ts

```
app.get('/', (c) => {
  return c.render('Hello!')
})
```

The output of which will be:

html

```
<html>
  <body>
    <p>Hello!</p>
  </body>
</html>
```

Additionally, this feature offers the flexibility to customize arguments. To ensure type safety, types can be defined as:

ts

```
declare module 'hono' {
  interface ContextRenderer {
    (
      content: string | Promise<string>,
      head: { title: string }
    ): Response | Promise<Response>
  }
}
```

Here's an example of how you can use this:

ts

```
app.use('/pages/*', async (c, next) => {
  c.setRenderer((content, head) => {
    return c.html(
      <html>
        <head>
          <title>{head.title}</title>
        </head>
        <body>
          <header>{head.title}</header>
          <p>{content}</p>
        </body>
      </html>
    )
  })
  await next()
})

app.get('/pages/my-favorite', (c) => {
  return c.render(<p>Ramen and Sushi</p>, {
    title: 'My favorite',
  })
})

app.get('/pages/my-hobbies', (c) => {
  return c.render(<p>Watching baseball</p>, {
    title: 'My hobbies',
  })
})
```

## executionCtx​

You can access Cloudflare Workers' specific [ExecutionContext](https://developers.cloudflare.com/workers/runtime-apis/context/).

ts

```
// ExecutionContext object
app.get('/foo', async (c) => {
  c.executionCtx.waitUntil(c.env.KV.put(key, data))
  // ...
})
```

## event​

You can access Cloudflare Workers' specific `FetchEvent`. This was used in "Service Worker" syntax. But, it is not recommended now.

ts

```
// Type definition to make type inference
type Bindings = {
  MY_KV: KVNamespace
}

const app = new Hono<{ Bindings: Bindings }>()

// FetchEvent object (only set when using Service Worker syntax)
app.get('/foo', async (c) => {
  c.event.waitUntil(c.env.MY_KV.put(key, data))
  // ...
})
```

## env​

In Cloudflare Workers Environment variables, secrets, KV namespaces, D1 database, R2 bucket etc. that are bound to a worker are known as bindings. Regardless of type, bindings are always available as global variables and can be accessed via the context `c.env.BINDING_KEY`.

ts

```
// Type definition to make type inference
type Bindings = {
  MY_KV: KVNamespace
}

const app = new Hono<{ Bindings: Bindings }>()

// Environment object for Cloudflare Workers
app.get('/', async (c) => {
  c.env.MY_KV.get('my-key')
  // ...
})
```

## error​

If the Handler throws an error, the error object is placed in `c.error`. You can access it in your middleware.

ts

```
app.use(async (c, next) => {
  await next()
  if (c.error) {
    // do something...
  }
})
```

## ContextVariableMap​

For instance, if you wish to add type definitions to variables when a specific middleware is used, you can extend `ContextVariableMap`. For example:

ts

```
declare module 'hono' {
  interface ContextVariableMap {
    result: string
  }
}
```

You can then utilize this in your middleware:

ts

```
const mw = createMiddleware(async (c, next) => {
  c.set('result', 'some values') // result is a string
  await next()
})
```

In a handler, the variable is inferred as the proper type:

ts

```
app.get('/', (c) => {
  const val = c.get('result') // val is a string
  // ...
  return c.json({ result: val })
})
```

---

# HTTPException​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# HTTPException​

When a fatal error occurs, Hono (and many ecosystem middleware) may throw an `HTTPException`. This is a custom Hono `Error` that simplifies [returning error responses](#handling-httpexceptions).

## Throwing HTTPExceptions​

You can throw your own HTTPExceptions by specifying a status code, and either a message or a custom response.

### Custom Message​

For basic `text` responses, just set a the error `message`.

ts

```
import { HTTPException } from 'hono/http-exception'

throw new HTTPException(401, { message: 'Unauthorized' })
```

### Custom Response​

For other response types, or to set response headers, use the `res` option. *Note that the status passed to the constructor is the one used to create responses.*

ts

```
import { HTTPException } from 'hono/http-exception'

const errorResponse = new Response('Unauthorized', {
  status: 401, // this gets ignored
  headers: {
    Authenticate: 'error="invalid_token"',
  },
})

throw new HTTPException(401, { res: errorResponse })
```

### Cause​

In either case, you can use the [cause](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause) option to add arbitrary data to the HTTPException.

ts

```
app.post('/login', async (c) => {
  try {
    await authorize(c)
  } catch (cause) {
    throw new HTTPException(401, { message, cause })
  }
  return c.redirect('/')
})
```

## Handling HTTPExceptions​

You can handle uncaught HTTPExceptions with [app.onError](https://hono.dev/docs/api/hono#error-handling). They include a `getResponse` method that returns a new `Response` created from the error `status`, and either the error `message`, or the [custom response](#custom-response) set when the error was thrown.

ts

```
import { HTTPException } from 'hono/http-exception'

// ...

app.onError((error, c) => {
  if (error instanceof HTTPException) {
    console.error(error.cause)
    // Get the custom response
    return error.getResponse()
  }
  // ...
})
```

WARNING

**HTTPException.getResponseis not aware ofContext**. To include headers already set in `Context`, you must apply them to a new `Response`.

---

# App

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# App - Hono​

`Hono` is the primary object. It will be imported first and used until the end.

ts

```
import { Hono } from 'hono'

const app = new Hono()
//...

export default app // for Cloudflare Workers or Bun
```

## Methods​

An instance of `Hono` has the following methods.

- app.**HTTP_METHOD**([path,]handler|middleware...)
- app.**all**([path,]handler|middleware...)
- app.**on**(method|method[], path|path[], handler|middleware...)
- app.**use**([path,]middleware)
- app.**route**(path, [app])
- app.**basePath**(path)
- app.**notFound**(handler)
- app.**onError**(err, handler)
- app.**mount**(path, anotherApp)
- app.**fire**()
- app.**fetch**(request, env, event)
- app.**request**(path, options)

The first part of them is used for routing, please refer to the [routing section](https://hono.dev/docs/api/routing).

## Not Found​

`app.notFound` allows you to customize a Not Found Response.

ts

```
app.notFound((c) => {
  return c.text('Custom 404 Message', 404)
})
```

WARNING

The `notFound` method is only called from the top-level app. For more information, see this [issue](https://github.com/honojs/hono/issues/3465#issuecomment-2381210165).

## Error Handling​

`app.onError` allows you to handle uncaught errors and return a custom Response.

ts

```
app.onError((err, c) => {
  console.error(`${err}`)
  return c.text('Custom Error Message', 500)
})
```

INFO

If both a parent app and its routes have `onError` handlers, the route-level handlers get priority.

## fire()​

WARNING

**app.fire()is deprecated**. Use `fire()` from `hono/service-worker` instead. See the [Service Worker documentation](https://hono.dev/docs/getting-started/service-worker) for details.

`app.fire()` automatically adds a global `fetch` event listener.

This can be useful for environments that adhere to the [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API), such as [non-ES module Cloudflare Workers](https://developers.cloudflare.com/workers/reference/migrate-to-module-workers/).

`app.fire()` executes the following for you:

ts

```
addEventListener('fetch', (event: FetchEventLike): void => {
  event.respondWith(this.dispatch(...))
})
```

## fetch()​

`app.fetch` will be entry point of your application.

For Cloudflare Workers, you can use the following:

ts

```
export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext) {
    return app.fetch(request, env, ctx)
  },
}
```

or just do:

ts

```
export default app
```

Bun:

ts

```
export default app
export default {
  port: 3000,
  fetch: app.fetch,
}
```

## request()​

`request` is a useful method for testing.

You can pass a URL or pathname to send a GET request. `app` will return a `Response` object.

ts

```
test('GET /hello is ok', async () => {
  const res = await app.request('/hello')
  expect(res.status).toBe(200)
})
```

You can also pass a `Request` object:

ts

```
test('POST /message is ok', async () => {
  const req = new Request('Hello!', {
    method: 'POST',
  })
  const res = await app.request(req)
  expect(res.status).toBe(201)
})
```

## mount()​

The `mount()` allows you to mount applications built with other frameworks into your Hono application.

ts

```
import { Router as IttyRouter } from 'itty-router'
import { Hono } from 'hono'

// Create itty-router application
const ittyRouter = IttyRouter()

// Handle `GET /itty-router/hello`
ittyRouter.get('/hello', () => new Response('Hello from itty-router'))

// Hono application
const app = new Hono()

// Mount!
app.mount('/itty-router', ittyRouter.handle)
```

## strict mode​

Strict mode defaults to `true` and distinguishes the following routes.

- `/hello`
- `/hello/`

`app.get('/hello')` will not match `GET /hello/`.

By setting strict mode to `false`, both paths will be treated equally.

ts

```
const app = new Hono({ strict: false })
```

## router option​

The `router` option specifies which router to use. The default router is `SmartRouter`. If you want to use `RegExpRouter`, pass it to a new `Hono` instance:

ts

```
import { RegExpRouter } from 'hono/router/reg-exp-router'

const app = new Hono({ router: new RegExpRouter() })
```

## Generics​

You can pass Generics to specify the types of Cloudflare Workers Bindings and variables used in `c.set`/`c.get`.

ts

```
type Bindings = {
  TOKEN: string
}

type Variables = {
  user: User
}

const app = new Hono<{
  Bindings: Bindings
  Variables: Variables
}>()

app.use('/auth/*', async (c, next) => {
  const token = c.env.TOKEN // token is `string`
  // ...
  c.set('user', user) // user should be `User`
  await next()
})
```

---

# Presets​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Presets​

Hono has several routers, each designed for a specific purpose. You can specify the router you want to use in the constructor of Hono.

**Presets** are provided for common use cases, so you don't have to specify the router each time. The `Hono` class imported from all presets is the same, the only difference being the router. Therefore, you can use them interchangeably.

## hono​

Usage:

ts

```
import { Hono } from 'hono'
```

Routers:

ts

```
this.router = new SmartRouter({
  routers: [new RegExpRouter(), new TrieRouter()],
})
```

## hono/quick​

Usage:

ts

```
import { Hono } from 'hono/quick'
```

Router:

ts

```
this.router = new SmartRouter({
  routers: [new LinearRouter(), new TrieRouter()],
})
```

## hono/tiny​

Usage:

ts

```
import { Hono } from 'hono/tiny'
```

Router:

ts

```
this.router = new PatternRouter()
```

## Which preset should I use?​

| Preset | Suitable platforms |
| --- | --- |
| hono | This is highly recommended for most use cases. Although the registration phase may be slower thanhono/quick, it exhibits high performance once booted. It's ideal for long-life servers built withDeno,Bun, orNode.js. It is also suitable forFastly Compute, as route registration occurs during the app build phase on that platform. For environments such asCloudflare Workers,Deno Deploy, where v8 isolates are utilized, this preset is suitable as well. Because the isolations persist for a certain amount of time after booting. |
| hono/quick | This preset is designed for environments where the application is initialized for every request. |
| hono/tiny | This is the smallest router package and it's suitable for environments where resources are limited. |

---

# HonoRequest​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# HonoRequest​

The `HonoRequest` is an object that can be taken from `c.req` which wraps a [Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) object.

## param()​

Get the values of path parameters.

ts

```
// Captured params
app.get('/entry/:id', async (c) => {
  const id = c.req.param('id')
  // ...
})

// Get all params at once
app.get('/entry/:id/comment/:commentId', async (c) => {
  const { id, commentId } = c.req.param()
})
```

## query()​

Get querystring parameters.

ts

```
// Query params
app.get('/search', async (c) => {
  const query = c.req.query('q')
})

// Get all params at once
app.get('/search', async (c) => {
  const { q, limit, offset } = c.req.query()
})
```

## queries()​

Get multiple querystring parameter values, e.g. `/search?tags=A&tags=B`

ts

```
app.get('/search', async (c) => {
  // tags will be string[]
  const tags = c.req.queries('tags')
  // ...
})
```

## header()​

Get the request header value.

ts

```
app.get('/', (c) => {
  const userAgent = c.req.header('User-Agent')
  return c.text(`Your user agent is ${userAgent}`)
})
```

WARNING

When `c.req.header()` is called with no arguments, all keys in the returned record are **lowercase**.

If you want to get the value of a header with an uppercase name, use `c.req.header(“X-Foo”)`.

ts

```
// ❌ Will not work
const headerRecord = c.req.header()
const foo = headerRecord['X-Foo']

// ✅ Will work
const foo = c.req.header('X-Foo')
```

## parseBody()​

Parse Request body of type `multipart/form-data` or `application/x-www-form-urlencoded`

ts

```
app.post('/entry', async (c) => {
  const body = await c.req.parseBody()
  // ...
})
```

`parseBody()` supports the following behaviors.

**Single file**

ts

```
const body = await c.req.parseBody()
const data = body['foo']
```

`body['foo']` is `(string | File)`.

If multiple files are uploaded, the last one will be used.

### Multiple files​

ts

```
const body = await c.req.parseBody()
body['foo[]']
```

`body['foo[]']` is always `(string | File)[]`.

`[]` postfix is required.

### Multiple files or fields with same name​

If you have a input field that allows multiple `<input type="file" multiple />` or multiple checkboxes with the same name `<input type="checkbox" name="favorites" value="Hono"/>`.

ts

```
const body = await c.req.parseBody({ all: true })
body['foo']
```

`all` option is disabled by default.

- If `body['foo']` is multiple files, it will be parsed to `(string | File)[]`.
- If `body['foo']` is single file, it will be parsed to `(string | File)`.

### Dot notation​

If you set the `dot` option `true`, the return value is structured based on the dot notation.

Imagine receiving the following data:

ts

```
const data = new FormData()
data.append('obj.key1', 'value1')
data.append('obj.key2', 'value2')
```

You can get the structured value by setting the `dot` option `true`:

ts

```
const body = await c.req.parseBody({ dot: true })
// body is `{ obj: { key1: 'value1', key2: 'value2' } }`
```

## json()​

Parses the request body of type `application/json`

ts

```
app.post('/entry', async (c) => {
  const body = await c.req.json()
  // ...
})
```

## text()​

Parses the request body of type `text/plain`

ts

```
app.post('/entry', async (c) => {
  const body = await c.req.text()
  // ...
})
```

## arrayBuffer()​

Parses the request body as an `ArrayBuffer`

ts

```
app.post('/entry', async (c) => {
  const body = await c.req.arrayBuffer()
  // ...
})
```

## blob()​

Parses the request body as a `Blob`.

ts

```
app.post('/entry', async (c) => {
  const body = await c.req.blob()
  // ...
})
```

## formData()​

Parses the request body as a `FormData`.

ts

```
app.post('/entry', async (c) => {
  const body = await c.req.formData()
  // ...
})
```

## valid()​

Get the validated data.

ts

```
app.post('/posts', async (c) => {
  const { title, body } = c.req.valid('form')
  // ...
})
```

Available targets are below.

- `form`
- `json`
- `query`
- `header`
- `cookie`
- `param`

See the [Validation section](https://hono.dev/docs/guides/validation) for usage examples.

## routePath​

WARNING

**Deprecated in v4.8.0**: This property is deprecated. Use `routePath()` from [Route Helper](https://hono.dev/docs/helpers/route) instead.

You can retrieve the registered path within the handler like this:

ts

```
app.get('/posts/:id', (c) => {
  return c.json({ path: c.req.routePath })
})
```

If you access `/posts/123`, it will return `/posts/:id`:

json

```
{ "path": "/posts/:id" }
```

## matchedRoutes​

WARNING

**Deprecated in v4.8.0**: This property is deprecated. Use `matchedRoutes()` from [Route Helper](https://hono.dev/docs/helpers/route) instead.

It returns matched routes within the handler, which is useful for debugging.

ts

```
app.use(async function logger(c, next) {
  await next()
  c.req.matchedRoutes.forEach(({ handler, method, path }, i) => {
    const name =
      handler.name ||
      (handler.length < 2 ? '[handler]' : '[middleware]')
    console.log(
      method,
      ' ',
      path,
      ' '.repeat(Math.max(10 - path.length, 0)),
      name,
      i === c.req.routeIndex ? '<- respond from here' : ''
    )
  })
})
```

## path​

The request pathname.

ts

```
app.get('/about/me', async (c) => {
  const pathname = c.req.path // `/about/me`
  // ...
})
```

## url​

The request url strings.

ts

```
app.get('/about/me', async (c) => {
  const url = c.req.url // `http://localhost:8787/about/me`
  // ...
})
```

## method​

The method name of the request.

ts

```
app.get('/about/me', async (c) => {
  const method = c.req.method // `GET`
  // ...
})
```

## raw​

The raw [Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) object.

ts

```
// For Cloudflare Workers
app.post('/', async (c) => {
  const metadata = c.req.raw.cf?.hostMetadata?
  // ...
})
```

## cloneRawRequest()​

Clones the raw Request object from a HonoRequest. Works even after the request body has been consumed by validators or HonoRequest methods.

ts

```
import { Hono } from 'hono'
const app = new Hono()

import { cloneRawRequest } from 'hono/request'
import { validator } from 'hono/validator'

app.post(
  '/forward',
  validator('json', (data) => data),
  async (c) => {
    // Clone after validation
    const clonedReq = await cloneRawRequest(c.req)
    // Does not throw the error
    await clonedReq.json()
    // ...
  }
)
```

---

# Routing​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Routing​

Routing of Hono is flexible and intuitive. Let's take a look.

## Basic​

ts

```
// HTTP Methods
app.get('/', (c) => c.text('GET /'))
app.post('/', (c) => c.text('POST /'))
app.put('/', (c) => c.text('PUT /'))
app.delete('/', (c) => c.text('DELETE /'))

// Wildcard
app.get('/wild/*/card', (c) => {
  return c.text('GET /wild/*/card')
})

// Any HTTP methods
app.all('/hello', (c) => c.text('Any Method /hello'))

// Custom HTTP method
app.on('PURGE', '/cache', (c) => c.text('PURGE Method /cache'))

// Multiple Method
app.on(['PUT', 'DELETE'], '/post', (c) =>
  c.text('PUT or DELETE /post')
)

// Multiple Paths
app.on('GET', ['/hello', '/ja/hello', '/en/hello'], (c) =>
  c.text('Hello')
)
```

## Path Parameter​

ts

```
app.get('/user/:name', async (c) => {
  const name = c.req.param('name')
  // ...
})
```

or all parameters at once:

ts

```
app.get('/posts/:id/comment/:comment_id', async (c) => {
  const { id, comment_id } = c.req.param()
  // ...
})
```

## Optional Parameter​

ts

```
// Will match `/api/animal` and `/api/animal/:type`
app.get('/api/animal/:type?', (c) => c.text('Animal!'))
```

## Regexp​

ts

```
app.get('/post/:date{[0-9]+}/:title{[a-z]+}', async (c) => {
  const { date, title } = c.req.param()
  // ...
})
```

## Including slashes​

ts

```
app.get('/posts/:filename{.+\\.png}', async (c) => {
  //...
})
```

## Chained route​

ts

```
app
  .get('/endpoint', (c) => {
    return c.text('GET /endpoint')
  })
  .post((c) => {
    return c.text('POST /endpoint')
  })
  .delete((c) => {
    return c.text('DELETE /endpoint')
  })
```

## Grouping​

You can group the routes with the Hono instance and add them to the main app with the route method.

ts

```
const book = new Hono()

book.get('/', (c) => c.text('List Books')) // GET /book
book.get('/:id', (c) => {
  // GET /book/:id
  const id = c.req.param('id')
  return c.text('Get Book: ' + id)
})
book.post('/', (c) => c.text('Create Book')) // POST /book

const app = new Hono()
app.route('/book', book)
```

## Grouping without changing base​

You can also group multiple instances while keeping base.

ts

```
const book = new Hono()
book.get('/book', (c) => c.text('List Books')) // GET /book
book.post('/book', (c) => c.text('Create Book')) // POST /book

const user = new Hono().basePath('/user')
user.get('/', (c) => c.text('List Users')) // GET /user
user.post('/', (c) => c.text('Create User')) // POST /user

const app = new Hono()
app.route('/', book) // Handle /book
app.route('/', user) // Handle /user
```

## Base path​

You can specify the base path.

ts

```
const api = new Hono().basePath('/api')
api.get('/book', (c) => c.text('List Books')) // GET /api/book
```

## Routing with hostname​

It works fine if it includes a hostname.

ts

```
const app = new Hono({
  getPath: (req) => req.url.replace(/^https?:\/([^?]+).*$/, '$1'),
})

app.get('/www1.example.com/hello', (c) => c.text('hello www1'))
app.get('/www2.example.com/hello', (c) => c.text('hello www2'))
```

## Routing withhostHeader value​

Hono can handle the `host` header value if you set the `getPath()` function in the Hono constructor.

ts

```
const app = new Hono({
  getPath: (req) =>
    '/' +
    req.headers.get('host') +
    req.url.replace(/^https?:\/\/[^/]+(\/[^?]*).*/, '$1'),
})

app.get('/www1.example.com/hello', (c) => c.text('hello www1'))

// A following request will match the route:
// new Request('http://www1.example.com/hello', {
//  headers: { host: 'www1.example.com' },
// })
```

By applying this, for example, you can change the routing by `User-Agent` header.

## Routing priority​

Handlers or middleware will be executed in registration order.

ts

```
app.get('/book/a', (c) => c.text('a')) // a
app.get('/book/:slug', (c) => c.text('common')) // common
```

```
GET /book/a ---> `a`
GET /book/b ---> `common`
```

When a handler is executed, the process will be stopped.

ts

```
app.get('*', (c) => c.text('common')) // common
app.get('/foo', (c) => c.text('foo')) // foo
```

```
GET /foo ---> `common` // foo will not be dispatched
```

If you have the middleware that you want to execute, write the code above the handler.

ts

```
app.use(logger())
app.get('/foo', (c) => c.text('foo'))
```

If you want to have a "*fallback*" handler, write the code below the other handler.

ts

```
app.get('/bar', (c) => c.text('bar')) // bar
app.get('*', (c) => c.text('fallback')) // fallback
```

```
GET /bar ---> `bar`
GET /foo ---> `fallback`
```

## Grouping ordering​

Note that the mistake of grouping routings is hard to notice. The `route()` function takes the stored routing from the second argument (such as `three` or `two`) and adds it to its own (`two` or `app`) routing.

ts

```
three.get('/hi', (c) => c.text('hi'))
two.route('/three', three)
app.route('/two', two)

export default app
```

It will return 200 response.

```
GET /two/three/hi ---> `hi`
```

However, if they are in the wrong order, it will return a 404.

ts

```
three.get('/hi', (c) => c.text('hi'))
app.route('/two', two) // `two` does not have routes
two.route('/three', three)

export default app
```

```
GET /two/three/hi ---> 404 Not Found
```
