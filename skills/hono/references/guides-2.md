# RPC​ and more

# RPC​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# RPC​

The RPC feature allows sharing of the API specifications between the server and the client.

First, export the `typeof` your Hono app (commonly called `AppType`)—or just the routes you want available to the client—from your server code.

By accepting `AppType` as a generic parameter, the Hono Client can infer both the input type(s) specified by the Validator, and the output type(s) emitted by handlers returning `c.json()`.

NOTE

For the RPC types to work properly in a monorepo, in both the Client's and Server's tsconfig.json files, set `"strict": true` in `compilerOptions`. [Read more.](https://github.com/honojs/hono/issues/2270#issuecomment-2143745118)

## Server​

All you need to do on the server side is to write a validator and create a variable `route`. The following example uses [Zod Validator](https://github.com/honojs/middleware/tree/main/packages/zod-validator).

ts

```
const route = app.post(
  '/posts',
  zValidator(
    'form',
    z.object({
      title: z.string(),
      body: z.string(),
    })
  ),
  (c) => {
    // ...
    return c.json(
      {
        ok: true,
        message: 'Created!',
      },
      201
    )
  }
)
```

Then, export the type to share the API spec with the Client.

ts

```
export type AppType = typeof route
```

## Client​

On the Client side, import `hc` and `AppType` first.

ts

```
import type { AppType } from '.'
import { hc } from 'hono/client'
```

`hc` is a function to create a client. Pass `AppType` as Generics and specify the server URL as an argument.

ts

```
const client = hc<AppType>('http://localhost:8787/')
```

Call `client.{path}.{method}` and pass the data you wish to send to the server as an argument.

ts

```
const res = await client.posts.$post({
  form: {
    title: 'Hello',
    body: 'Hono is a cool project',
  },
})
```

The `res` is compatible with the "fetch" Response. You can retrieve data from the server with `res.json()`.

ts

```
if (res.ok) {
  const data = await res.json()
  console.log(data.message)
}
```

### Cookies​

To make the client send cookies with every request, add `{ 'init': { 'credentials": 'include' } }` to the options when you're creating the client.

ts

```
// client.ts
const client = hc<AppType>('http://localhost:8787/', {
  init: {
    credentials: 'include',
  },
})

// This request will now include any cookies you might have set
const res = await client.posts.$get({
  query: {
    id: '123',
  },
})
```

## Status code​

If you explicitly specify the status code, such as `200` or `404`, in `c.json()`. It will be added as a type for passing to the client.

ts

```
// server.ts
const app = new Hono().get(
  '/posts',
  zValidator(
    'query',
    z.object({
      id: z.string(),
    })
  ),
  async (c) => {
    const { id } = c.req.valid('query')
    const post: Post | undefined = await getPost(id)

    if (post === undefined) {
      return c.json({ error: 'not found' }, 404) // Specify 404
    }

    return c.json({ post }, 200) // Specify 200
  }
)

export type AppType = typeof app
```

You can get the data by the status code.

ts

```
// client.ts
const client = hc<AppType>('http://localhost:8787/')

const res = await client.posts.$get({
  query: {
    id: '123',
  },
})

if (res.status === 404) {
  const data: { error: string } = await res.json()
  console.log(data.error)
}

if (res.ok) {
  const data: { post: Post } = await res.json()
  console.log(data.post)
}

// { post: Post } | { error: string }
type ResponseType = InferResponseType<typeof client.posts.$get>

// { post: Post }
type ResponseType200 = InferResponseType<
  typeof client.posts.$get,
  200
>
```

## Not Found​

If you want to use a client, you should not use `c.notFound()` for the Not Found response. The data that the client gets from the server cannot be inferred correctly.

ts

```
// server.ts
export const routes = new Hono().get(
  '/posts',
  zValidator(
    'query',
    z.object({
      id: z.string(),
    })
  ),
  async (c) => {
    const { id } = c.req.valid('query')
    const post: Post | undefined = await getPost(id)

    if (post === undefined) {
      return c.notFound() // ❌️
    }

    return c.json({ post })
  }
)

// client.ts
import { hc } from 'hono/client'

const client = hc<typeof routes>('/')

const res = await client.posts[':id'].$get({
  param: {
    id: '123',
  },
})

const data = await res.json() // 🙁 data is unknown
```

Please use `c.json()` and specify the status code for the Not Found Response.

ts

```
export const routes = new Hono().get(
  '/posts',
  zValidator(
    'query',
    z.object({
      id: z.string(),
    })
  ),
  async (c) => {
    const { id } = c.req.valid('query')
    const post = await getPost(id)

    if (!post) {
      return c.json({ error: 'not found' }, 404) // Specify 404
    }

    return c.json({ post }, 200) // Specify 200
  }
)
```

Alternatively, you can use module augmentation to extend `NotFoundResponse` interface. This allows `c.notFound()` to return a typed response:

ts

```
// server.ts
import { Hono, TypedResponse } from 'hono'

declare module 'hono' {
  interface NotFoundResponse
    extends Response,
      TypedResponse<{ error: string }, 404, 'json'> {}
}

const app = new Hono()
  .get('/posts/:id', async (c) => {
    const post = await getPost(c.req.param('id'))
    if (!post) {
      return c.notFound()
    }
    return c.json({ post }, 200)
  })
  .notFound((c) => c.json({ error: 'not found' }, 404))

export type AppType = typeof app
```

Now the client can correctly infer the 404 response type.

## Path parameters​

You can also handle routes that include path parameters or query values.

ts

```
const route = app.get(
  '/posts/:id',
  zValidator(
    'query',
    z.object({
      page: z.coerce.number().optional(), // coerce to convert to number
    })
  ),
  (c) => {
    // ...
    return c.json({
      title: 'Night',
      body: 'Time to sleep',
    })
  }
)
```

Both path parameters and query values **must** be passed as `string`, even if the underlying value is of a different type.

Specify the string you want to include in the path with `param`, and any query values with `query`.

ts

```
const res = await client.posts[':id'].$get({
  param: {
    id: '123',
  },
  query: {
    page: '1', // `string`, converted by the validator to `number`
  },
})
```

### Multiple parameters​

Handle routes with multiple parameters.

ts

```
const route = app.get(
  '/posts/:postId/:authorId',
  zValidator(
    'query',
    z.object({
      page: z.string().optional(),
    })
  ),
  (c) => {
    // ...
    return c.json({
      title: 'Night',
      body: 'Time to sleep',
    })
  }
)
```

Add multiple `['']` to specify params in path.

ts

```
const res = await client.posts[':postId'][':authorId'].$get({
  param: {
    postId: '123',
    authorId: '456',
  },
  query: {},
})
```

### Include slashes​

`hc` function does not URL-encode the values of `param`. To include slashes in parameters, use [regular expressions](https://hono.dev/docs/api/routing#regexp).

ts

```
// client.ts

// Requests /posts/123/456
const res = await client.posts[':id'].$get({
  param: {
    id: '123/456',
  },
})

// server.ts
const route = app.get(
  '/posts/:id{.+}',
  zValidator(
    'param',
    z.object({
      id: z.string(),
    })
  ),
  (c) => {
    // id: 123/456
    const { id } = c.req.valid('param')
    // ...
  }
)
```

NOTE

Basic path parameters without regular expressions do not match slashes. If you pass a `param` containing slashes using the hc function, the server might not route as intended. Encoding the parameters using `encodeURIComponent` is the recommended approach to ensure correct routing.

## Headers​

You can append the headers to the request.

ts

```
const res = await client.search.$get(
  {
    //...
  },
  {
    headers: {
      'X-Custom-Header': 'Here is Hono Client',
      'X-User-Agent': 'hc',
    },
  }
)
```

To add a common header to all requests, specify it as an argument to the `hc` function.

ts

```
const client = hc<AppType>('/api', {
  headers: {
    Authorization: 'Bearer TOKEN',
  },
})
```

## initoption​

You can pass the fetch's `RequestInit` object to the request as the `init` option. Below is an example of aborting a Request.

ts

```
import { hc } from 'hono/client'

const client = hc<AppType>('http://localhost:8787/')

const abortController = new AbortController()
const res = await client.api.posts.$post(
  {
    json: {
      // Request body
    },
  },
  {
    // RequestInit object
    init: {
      signal: abortController.signal,
    },
  }
)

// ...

abortController.abort()
```

INFO

A `RequestInit` object defined by `init` takes the highest priority. It could be used to overwrite things set by other options like `body | method | headers`.

## $url()​

You can get a `URL` object for accessing the endpoint by using `$url()`.

WARNING

You have to pass in an absolute URL for this to work. Passing in a relative URL `/` will result in the following error.

`Uncaught TypeError: Failed to construct 'URL': Invalid URL`

ts

```
// ❌ Will throw error
const client = hc<AppType>('/')
client.api.post.$url()

// ✅ Will work as expected
const client = hc<AppType>('http://localhost:8787/')
client.api.post.$url()
```

ts

```
const route = app
  .get('/api/posts', (c) => c.json({ posts }))
  .get('/api/posts/:id', (c) => c.json({ post }))

const client = hc<typeof route>('http://localhost:8787/')

let url = client.api.posts.$url()
console.log(url.pathname) // `/api/posts`

url = client.api.posts[':id'].$url({
  param: {
    id: '123',
  },
})
console.log(url.pathname) // `/api/posts/123`
```

### Typed URL​

You can pass the base URL as the second type parameter to `hc` to get more precise URL types:

ts

```
const client = hc<typeof route, 'http://localhost:8787'>(
  'http://localhost:8787/'
)

const url = client.api.posts.$url()
// url is TypedURL with precise type information
// including protocol, host, and path
```

This is useful when you want to use the URL as a type-safe key for libraries like SWR.

## File Uploads​

You can upload files using a form body:

ts

```
// client
const res = await client.user.picture.$put({
  form: {
    file: new File([fileToUpload], filename, {
      type: fileToUpload.type,
    }),
  },
})
```

ts

```
// server
const route = app.put(
  '/user/picture',
  zValidator(
    'form',
    z.object({
      file: z.instanceof(File),
    })
  )
  // ...
)
```

## Customfetchmethod​

You can set the custom `fetch` method.

In the following example script for Cloudflare Worker, the Service Bindings' `fetch` method is used instead of the default `fetch`.

toml

```
# wrangler.toml
services = [
  { binding = "AUTH", service = "auth-service" },
]
```

ts

```
// src/client.ts
const client = hc<CreateProfileType>('http://localhost', {
  fetch: c.env.AUTH.fetch.bind(c.env.AUTH),
})
```

## Custom query serializer​

You can customize how query parameters are serialized using the `buildSearchParams` option. This is useful when you need bracket notation for arrays or other custom formats:

ts

```
const client = hc<AppType>('http://localhost', {
  buildSearchParams: (query) => {
    const searchParams = new URLSearchParams()
    for (const [k, v] of Object.entries(query)) {
      if (v === undefined) {
        continue
      }
      if (Array.isArray(v)) {
        v.forEach((item) => searchParams.append(`${k}[]`, item))
      } else {
        searchParams.set(k, v)
      }
    }
    return searchParams
  },
})
```

## Infer​

Use `InferRequestType` and `InferResponseType` to know the type of object to be requested and the type of object to be returned.

ts

```
import type { InferRequestType, InferResponseType } from 'hono/client'

// InferRequestType
const $post = client.todo.$post
type ReqType = InferRequestType<typeof $post>['form']

// InferResponseType
type ResType = InferResponseType<typeof $post>
```

## Parsing a Response with type-safety helper​

You can use `parseResponse()` helper to easily parse a Response from `hc` with type-safety.

ts

```
import { parseResponse, DetailedError } from 'hono/client'

// result contains the parsed response body (automatically parsed based on Content-Type)
const result = await parseResponse(client.hello.$get()).catch(
  (e: DetailedError) => {
    console.error(e)
  }
)
// parseResponse automatically throws an error if response is not ok
```

## Using SWR​

You can also use a React Hook library such as [SWR](https://swr.vercel.app).

tsx

```
import useSWR from 'swr'
import { hc } from 'hono/client'
import type { InferRequestType } from 'hono/client'
import type { AppType } from '../functions/api/[[route]]'

const App = () => {
  const client = hc<AppType>('/api')
  const $get = client.hello.$get

  const fetcher =
    (arg: InferRequestType<typeof $get>) => async () => {
      const res = await $get(arg)
      return await res.json()
    }

  const { data, error, isLoading } = useSWR(
    'api-hello',
    fetcher({
      query: {
        name: 'SWR',
      },
    })
  )

  if (error) return <div>failed to load</div>
  if (isLoading) return <div>loading...</div>

  return <h1>{data?.message}</h1>
}

export default App
```

## Using RPC with larger applications​

In the case of a larger application, such as the example mentioned in [Building a larger application](https://hono.dev/docs/guides/best-practices#building-a-larger-application), you need to be careful about the type of inference. A simple way to do this is to chain the handlers so that the types are always inferred.

ts

```
// authors.ts
import { Hono } from 'hono'

const app = new Hono()
  .get('/', (c) => c.json('list authors'))
  .post('/', (c) => c.json('create an author', 201))
  .get('/:id', (c) => c.json(`get ${c.req.param('id')}`))

export default app
```

ts

```
// books.ts
import { Hono } from 'hono'

const app = new Hono()
  .get('/', (c) => c.json('list books'))
  .post('/', (c) => c.json('create a book', 201))
  .get('/:id', (c) => c.json(`get ${c.req.param('id')}`))

export default app
```

You can then import the sub-routers as you usually would, and make sure you chain their handlers as well, since this is the top level of the app in this case, this is the type we'll want to export.

ts

```
// index.ts
import { Hono } from 'hono'
import authors from './authors'
import books from './books'

const app = new Hono()

const routes = app.route('/authors', authors).route('/books', books)

export default app
export type AppType = typeof routes
```

You can now create a new client using the registered AppType and use it as you would normally.

## Known issues​

### IDE performance​

When using RPC, the more routes you have, the slower your IDE will become. One of the main reasons for this is that massive amounts of type instantiations are executed to infer the type of your app.

For example, suppose your app has a route like this:

ts

```
// app.ts
export const app = new Hono().get('foo/:id', (c) =>
  c.json({ ok: true }, 200)
)
```

Hono will infer the type as follows:

ts

```
export const app = Hono<BlankEnv, BlankSchema, '/'>().get<
  'foo/:id',
  'foo/:id',
  JSONRespondReturn<{ ok: boolean }, 200>,
  BlankInput,
  BlankEnv
>('foo/:id', (c) => c.json({ ok: true }, 200))
```

This is a type instantiation for a single route. While the user doesn't need to write these type arguments manually, which is a good thing, it's known that type instantiation takes much time. `tsserver` used in your IDE does this time consuming task every time you use the app. If you have a lot of routes, this can slow down your IDE significantly.

However, we have some tips to mitigate this issue.

#### Hono version mismatch​

If your backend is separate from the frontend and lives in a different directory, you need to ensure that the Hono versions match. If you use one Hono version on the backend and another on the frontend, you'll run into issues such as "*Type instantiation is excessively deep and possibly infinite*".

![](https://github.com/user-attachments/assets/e4393c80-29dd-408d-93ab-d55c11ccca05)

#### TypeScript project references​

Like in the case of [Hono version mismatch](#hono-version-mismatch), you'll run into issues if your backend and frontend are separate. If you want to access code from the backend (`AppType`, for example) on the frontend, you need to use [project references](https://www.typescriptlang.org/docs/handbook/project-references.html). TypeScript's project references allow one TypeScript codebase to access and use code from another TypeScript codebase. *(source:Hono RPC And TypeScript Project References)*.

#### Compile your code before using it (recommended)​

`tsc` can do heavy tasks like type instantiation at compile time! Then, `tsserver` doesn't need to instantiate all the type arguments every time you use it. It will make your IDE a lot faster!

Compiling your client including the server app gives you the best performance. Put the following code in your project:

ts

```
import { app } from './app'
import { hc } from 'hono/client'

// this is a trick to calculate the type when compiling
export type Client = ReturnType<typeof hc<typeof app>>

export const hcWithType = (...args: Parameters<typeof hc>): Client =>
  hc<typeof app>(...args)
```

After compiling, you can use `hcWithType` instead of `hc` to get the client with the type already calculated.

ts

```
const client = hcWithType('http://localhost:8787/')
const res = await client.posts.$post({
  form: {
    title: 'Hello',
    body: 'Hono is a cool project',
  },
})
```

If your project is a monorepo, this solution does fit well. Using a tool like [turborepo](https://turbo.build/repo/docs), you can easily separate the server project and the client project and get better integration managing dependencies between them. Here is [a working example](https://github.com/m-shaka/hono-rpc-perf-tips-example).

You can also coordinate your build process manually with tools like `concurrently` or `npm-run-all`.

#### Specify type arguments manually​

This is a bit cumbersome, but you can specify type arguments manually to avoid type instantiation.

ts

```
const app = new Hono().get<'foo/:id'>('foo/:id', (c) =>
  c.json({ ok: true }, 200)
)
```

Specifying just single type argument make a difference in performance, while it may take you a lot of time and effort if you have a lot of routes.

#### Split your app and client into multiple files​

As described in [Using RPC with larger applications](#using-rpc-with-larger-applications), you can split your app into multiple apps. You can also create a client for each app:

ts

```
// authors-cli.ts
import { app as authorsApp } from './authors'
import { hc } from 'hono/client'

const authorsClient = hc<typeof authorsApp>('/authors')

// books-cli.ts
import { app as booksApp } from './books'
import { hc } from 'hono/client'

const booksClient = hc<typeof booksApp>('/books')
```

This way, `tsserver` doesn't need to instantiate types for all routes at once.

---

# Testing​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Testing​

Testing is important. In actuality, it is easy to test Hono's applications. The way to create a test environment differs from each runtime, but the basic steps are the same. In this section, let's test with Cloudflare Workers and [Vitest](https://vitest.dev/).

TIP

Cloudflare recommends using [Vitest](https://vitest.dev/) with [@cloudflare/vitest-pool-workers](https://www.npmjs.com/package/@cloudflare/vitest-pool-workers). For more details, please refer to [Vitest integration](https://developers.cloudflare.com/workers/testing/vitest-integration/) in the Cloudflare Workers docs.

## Request and Response​

All you do is create a Request and pass it to the Hono application to validate the Response. And, you can use `app.request` the useful method.

TIP

For a typed test client see the [testing helper](https://hono.dev/docs/helpers/testing).

For example, consider an application that provides the following REST API.

ts

```
app.get('/posts', (c) => {
  return c.text('Many posts')
})

app.post('/posts', (c) => {
  return c.json(
    {
      message: 'Created',
    },
    201,
    {
      'X-Custom': 'Thank you',
    }
  )
})
```

Make a request to `GET /posts` and test the response.

ts

```
describe('Example', () => {
  test('GET /posts', async () => {
    const res = await app.request('/posts')
    expect(res.status).toBe(200)
    expect(await res.text()).toBe('Many posts')
  })
})
```

To make a request to `POST /posts`, do the following.

ts

```
test('POST /posts', async () => {
  const res = await app.request('/posts', {
    method: 'POST',
  })
  expect(res.status).toBe(201)
  expect(res.headers.get('X-Custom')).toBe('Thank you')
  expect(await res.json()).toEqual({
    message: 'Created',
  })
})
```

To make a request to `POST /posts` with `JSON` data, do the following.

ts

```
test('POST /posts', async () => {
  const res = await app.request('/posts', {
    method: 'POST',
    body: JSON.stringify({ message: 'hello hono' }),
    headers: new Headers({ 'Content-Type': 'application/json' }),
  })
  expect(res.status).toBe(201)
  expect(res.headers.get('X-Custom')).toBe('Thank you')
  expect(await res.json()).toEqual({
    message: 'Created',
  })
})
```

To make a request to `POST /posts` with `multipart/form-data` data, do the following.

ts

```
test('POST /posts', async () => {
  const formData = new FormData()
  formData.append('message', 'hello')
  const res = await app.request('/posts', {
    method: 'POST',
    body: formData,
  })
  expect(res.status).toBe(201)
  expect(res.headers.get('X-Custom')).toBe('Thank you')
  expect(await res.json()).toEqual({
    message: 'Created',
  })
})
```

You can also pass an instance of the Request class.

ts

```
test('POST /posts', async () => {
  const req = new Request('http://localhost/posts', {
    method: 'POST',
  })
  const res = await app.request(req)
  expect(res.status).toBe(201)
  expect(res.headers.get('X-Custom')).toBe('Thank you')
  expect(await res.json()).toEqual({
    message: 'Created',
  })
})
```

In this way, you can test it as like an End-to-End.

## Env​

To set `c.env` for testing, you can pass it as the 3rd parameter to `app.request`. This is useful for mocking values like [Cloudflare Workers Bindings](https://hono.dev/getting-started/cloudflare-workers#bindings):

ts

```
const MOCK_ENV = {
  API_HOST: 'example.com',
  DB: {
    prepare: () => {
      /* mocked D1 */
    },
  },
}

test('GET /posts', async () => {
  const res = await app.request('/posts', {}, MOCK_ENV)
})
```

---

# Validation​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Validation​

Hono provides only a very thin Validator. But, it can be powerful when combined with a third-party Validator. In addition, the RPC feature allows you to share API specifications with your clients through types.

## Manual validator​

First, introduce a way to validate incoming values without using the third-party Validator.

Import `validator` from `hono/validator`.

ts

```
import { validator } from 'hono/validator'
```

To validate form data, specify `form` as the first argument and a callback as the second argument. In the callback, validates the value and return the validated values at the end. The `validator` can be used as middleware.

ts

```
app.post(
  '/posts',
  validator('form', (value, c) => {
    const body = value['body']
    if (!body || typeof body !== 'string') {
      return c.text('Invalid!', 400)
    }
    return {
      body: body,
    }
  }),
  //...
```

Within the handler you can get the validated value with `c.req.valid('form')`.

ts

```
, (c) => {
  const { body } = c.req.valid('form')
  // ... do something
  return c.json(
    {
      message: 'Created!',
    },
    201
  )
}
```

Validation targets include `json`, `query`, `header`, `param` and `cookie` in addition to `form`.

WARNING

When you validate `json` or `form`, the request *must* contain a matching `content-type` header (e.g. `Content-Type: application/json` for `json`). Otherwise, the request body will not be parsed and you will receive an empty object (`{}`) as value in the callback.

It is important to set the `content-type` header when testing using [app.request()](https://hono.dev/docs/api/request).

Given an application like this.

ts

```
const app = new Hono()
app.post(
  '/testing',
  validator('json', (value, c) => {
    // pass-through validator
    return value
  }),
  (c) => {
    const body = c.req.valid('json')
    return c.json(body)
  }
)
```

Your tests can be written like this.

ts

```
// ❌ this will not work
const res = await app.request('/testing', {
  method: 'POST',
  body: JSON.stringify({ key: 'value' }),
})
const data = await res.json()
console.log(data) // {}

// ✅ this will work
const res = await app.request('/testing', {
  method: 'POST',
  body: JSON.stringify({ key: 'value' }),
  headers: new Headers({ 'Content-Type': 'application/json' }),
})
const data = await res.json()
console.log(data) // { key: 'value' }
```

WARNING

When you validate `header`, you need to use **lowercase** name as the key.

If you want to validate the `Idempotency-Key` header, you need to use `idempotency-key` as the key.

ts

```
// ❌ this will not work
app.post(
  '/api',
  validator('header', (value, c) => {
    // idempotencyKey is always undefined
    // so this middleware always return 400 as not expected
    const idempotencyKey = value['Idempotency-Key']

    if (idempotencyKey == undefined || idempotencyKey === '') {
      throw new HTTPException(400, {
        message: 'Idempotency-Key is required',
      })
    }
    return { idempotencyKey }
  }),
  (c) => {
    const { idempotencyKey } = c.req.valid('header')
    // ...
  }
)

// ✅ this will work
app.post(
  '/api',
  validator('header', (value, c) => {
    // can retrieve the value of the header as expected
    const idempotencyKey = value['idempotency-key']

    if (idempotencyKey == undefined || idempotencyKey === '') {
      throw new HTTPException(400, {
        message: 'Idempotency-Key is required',
      })
    }
    return { idempotencyKey }
  }),
  (c) => {
    const { idempotencyKey } = c.req.valid('header')
    // ...
  }
)
```

## Multiple validators​

You can also include multiple validators to validate different parts of request:

ts

```
app.post(
  '/posts/:id',
  validator('param', ...),
  validator('query', ...),
  validator('json', ...),
  (c) => {
    //...
  }
```

## With Zod​

You can use [Zod](https://zod.dev), one of third-party validators. We recommend using a third-party validator.

Install from the Npm registry.

npmyarnpnpmbunsh

```
npm i zod
```

sh

```
yarn add zod
```

sh

```
pnpm add zod
```

sh

```
bun add zod
```

Import `z` from `zod`.

ts

```
import * as z from 'zod'
```

Write your schema.

ts

```
const schema = z.object({
  body: z.string(),
})
```

You can use the schema in the callback function for validation and return the validated value.

ts

```
const route = app.post(
  '/posts',
  validator('form', (value, c) => {
    const parsed = schema.safeParse(value)
    if (!parsed.success) {
      return c.text('Invalid!', 401)
    }
    return parsed.data
  }),
  (c) => {
    const { body } = c.req.valid('form')
    // ... do something
    return c.json(
      {
        message: 'Created!',
      },
      201
    )
  }
)
```

## Zod Validator Middleware​

You can use the [Zod Validator Middleware](https://github.com/honojs/middleware/tree/main/packages/zod-validator) to make it even easier.

npmyarnpnpmbunsh

```
npm i @hono/zod-validator
```

sh

```
yarn add @hono/zod-validator
```

sh

```
pnpm add @hono/zod-validator
```

sh

```
bun add @hono/zod-validator
```

And import `zValidator`.

ts

```
import { zValidator } from '@hono/zod-validator'
```

And write as follows.

ts

```
const route = app.post(
  '/posts',
  zValidator(
    'form',
    z.object({
      body: z.string(),
    })
  ),
  (c) => {
    const validated = c.req.valid('form')
    // ... use your validated data
  }
)
```

## Standard Schema Validator Middleware​

[Standard Schema](https://standardschema.dev/) is a specification that provides a common interface for TypeScript validation libraries. It was created by the maintainers of Zod, Valibot, and ArkType to allow ecosystem tools to work with any validation library without needing custom adapters.

The [Standard Schema Validator Middleware](https://github.com/honojs/middleware/tree/main/packages/standard-validator) lets you use any Standard Schema-compatible validation library with Hono, giving you the flexibility to choose your preferred validator while maintaining consistent type safety.

npmyarnpnpmbunsh

```
npm i @hono/standard-validator
```

sh

```
yarn add @hono/standard-validator
```

sh

```
pnpm add @hono/standard-validator
```

sh

```
bun add @hono/standard-validator
```

Import `sValidator` from the package:

ts

```
import { sValidator } from '@hono/standard-validator'
```

### With Zod​

You can use Zod with the Standard Schema validator:

npmyarnpnpmbunsh

```
npm i zod
```

sh

```
yarn add zod
```

sh

```
pnpm add zod
```

sh

```
bun add zod
```

ts

```
import * as z from 'zod'
import { sValidator } from '@hono/standard-validator'

const schema = z.object({
  name: z.string(),
  age: z.number(),
})

app.post('/author', sValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({
    success: true,
    message: `${data.name} is ${data.age}`,
  })
})
```

### With Valibot​

[Valibot](https://valibot.dev/) is a lightweight alternative to Zod with a modular design:

npmyarnpnpmbunsh

```
npm i valibot
```

sh

```
yarn add valibot
```

sh

```
pnpm add valibot
```

sh

```
bun add valibot
```

ts

```
import * as v from 'valibot'
import { sValidator } from '@hono/standard-validator'

const schema = v.object({
  name: v.string(),
  age: v.number(),
})

app.post('/author', sValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({
    success: true,
    message: `${data.name} is ${data.age}`,
  })
})
```

### With ArkType​

[ArkType](https://arktype.io/) offers TypeScript-native syntax for runtime validation:

npmyarnpnpmbunsh

```
npm i arktype
```

sh

```
yarn add arktype
```

sh

```
pnpm add arktype
```

sh

```
bun add arktype
```

ts

```
import { type } from 'arktype'
import { sValidator } from '@hono/standard-validator'

const schema = type({
  name: 'string',
  age: 'number',
})

app.post('/author', sValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({
    success: true,
    message: `${data.name} is ${data.age}`,
  })
})
```
