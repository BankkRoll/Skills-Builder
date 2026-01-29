# Benchmarks​ and more

# Benchmarks​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Benchmarks​

Benchmarks are only benchmarks, but they are important to us.

## Routers​

We measured the speeds of a bunch of JavaScript routers. For example, `find-my-way` is a very fast router used inside Fastify.

- @medley/router
- find-my-way
- koa-tree-router
- trek-router
- express (includes handling)
- koa-router

First, we registered the following routing to each of our routers. These are similar to those used in the real world.

ts

```
export const routes: Route[] = [
  { method: 'GET', path: '/user' },
  { method: 'GET', path: '/user/comments' },
  { method: 'GET', path: '/user/avatar' },
  { method: 'GET', path: '/user/lookup/username/:username' },
  { method: 'GET', path: '/user/lookup/email/:address' },
  { method: 'GET', path: '/event/:id' },
  { method: 'GET', path: '/event/:id/comments' },
  { method: 'POST', path: '/event/:id/comment' },
  { method: 'GET', path: '/map/:location/events' },
  { method: 'GET', path: '/status' },
  { method: 'GET', path: '/very/deeply/nested/route/hello/there' },
  { method: 'GET', path: '/static/*' },
]
```

Then we sent the Request to the endpoints like below.

ts

```
const routes: (Route & { name: string })[] = [
  {
    name: 'short static',
    method: 'GET',
    path: '/user',
  },
  {
    name: 'static with same radix',
    method: 'GET',
    path: '/user/comments',
  },
  {
    name: 'dynamic route',
    method: 'GET',
    path: '/user/lookup/username/hey',
  },
  {
    name: 'mixed static dynamic',
    method: 'GET',
    path: '/event/abcd1234/comments',
  },
  {
    name: 'post',
    method: 'POST',
    path: '/event/abcd1234/comment',
  },
  {
    name: 'long static',
    method: 'GET',
    path: '/very/deeply/nested/route/hello/there',
  },
  {
    name: 'wildcard',
    method: 'GET',
    path: '/static/index.html',
  },
]
```

Let's see the results.

### On Node.js​

The following screenshots show the results on Node.js.

![](https://hono.dev/images/bench01.png)

![](https://hono.dev/images/bench02.png)

![](https://hono.dev/images/bench03.png)

![](https://hono.dev/images/bench04.png)

![](https://hono.dev/images/bench05.png)

![](https://hono.dev/images/bench06.png)

![](https://hono.dev/images/bench07.png)

![](https://hono.dev/images/bench08.png)

### On Bun​

The following screenshots show the results on Bun.

![](https://hono.dev/images/bench09.png)

![](https://hono.dev/images/bench10.png)

![](https://hono.dev/images/bench11.png)

![](https://hono.dev/images/bench12.png)

![](https://hono.dev/images/bench13.png)

![](https://hono.dev/images/bench14.png)

![](https://hono.dev/images/bench15.png)

![](https://hono.dev/images/bench16.png)

## Cloudflare Workers​

**Hono is the fastest**, compared to other routers for Cloudflare Workers.

- Machine: Apple MacBook Pro, 32 GiB, M1 Pro
- Scripts: [benchmarks/handle-event](https://github.com/honojs/hono/tree/main/benchmarks/handle-event)

```
Hono x 402,820 ops/sec ±4.78% (80 runs sampled)
itty-router x 212,598 ops/sec ±3.11% (87 runs sampled)
sunder x 297,036 ops/sec ±4.76% (77 runs sampled)
worktop x 197,345 ops/sec ±2.40% (88 runs sampled)
Fastest is Hono
✨  Done in 28.06s.
```

## Deno​

**Hono is the fastest**, compared to other frameworks for Deno.

- Machine: Apple MacBook Pro, 32 GiB, M1 Pro, Deno v1.22.0
- Scripts: [benchmarks/deno](https://github.com/honojs/hono/tree/main/benchmarks/deno)
- Method: `bombardier --fasthttp -d 10s -c 100 'http://localhost:8000/user/lookup/username/foo'`

| Framework | Version | Results |
| --- | --- | --- |
| Hono | 3.0.0 | Requests/sec: 136112 |
| Fast | 4.0.0-beta.1 | Requests/sec: 103214 |
| Megalo | 0.3.0 | Requests/sec: 64597 |
| Faster | 5.7 | Requests/sec: 54801 |
| oak | 10.5.1 | Requests/sec: 43326 |
| opine | 2.2.0 | Requests/sec: 30700 |

Another benchmark result: [denosaurs/bench](https://github.com/denosaurs/bench)

## Bun​

Hono is one of the fastest frameworks for Bun. You can see it below.

- [SaltyAom/bun-http-framework-benchmark](https://github.com/SaltyAom/bun-http-framework-benchmark)

---

# Developer Experience​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Developer Experience​

To create a great application, we need great development experience. Fortunately, we can write applications for Cloudflare Workers, Deno, and Bun in TypeScript without having the need to transpile it to JavaScript. Hono is written in TypeScript and can make applications type-safe.

---

# Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Middleware​

We call the primitive that returns `Response` as "Handler". "Middleware" is executed before and after the Handler and handles the `Request` and `Response`. It's like an onion structure.

![](https://hono.dev/images/onion.png)

For example, we can write the middleware to add the "X-Response-Time" header as follows.

ts

```
app.use(async (c, next) => {
  const start = performance.now()
  await next()
  const end = performance.now()
  c.res.headers.set('X-Response-Time', `${end - start}`)
})
```

With this simple method, we can write our own custom middleware and we can use the built-in or third party middleware.

---

# Philosophy​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Philosophy​

In this section, we talk about the concept, or philosophy, of Hono.

## Motivation​

At first, I just wanted to create a web application on Cloudflare Workers. But, there was no good framework that works on Cloudflare Workers. So, I started building Hono.

I thought it would be a good opportunity to learn how to build a router using Trie trees. Then a friend showed up with ultra crazy fast router called "RegExpRouter". And I also have a friend who created the Basic authentication middleware.

Using only Web Standard APIs, we could make it work on Deno and Bun. When people asked "is there Express for Bun?", we could answer, "no, but there is Hono". (Although Express works on Bun now.)

We also have friends who make GraphQL servers, Firebase authentication, and Sentry middleware. And, we also have a Node.js adapter. An ecosystem has sprung up.

In other words, Hono is damn fast, makes a lot of things possible, and works anywhere. We might imagine that Hono could become the **Standard for Web Standards**.

---

# Routers​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Routers​

The routers are the most important features for Hono.

Hono has five routers.

## RegExpRouter​

**RegExpRouter** is the fastest router in the JavaScript world.

Although this is called "RegExp" it is not an Express-like implementation using [path-to-regexp](https://github.com/pillarjs/path-to-regexp). They are using linear loops. Therefore, regular expression matching will be performed for all routes and the performance will be degraded as you have more routes.

![](https://hono.dev/images/router-linear.jpg)

Hono's RegExpRouter turns the route pattern into "one large regular expression". Then it can get the result with one-time matching.

![](https://hono.dev/images/router-regexp.jpg)

This works faster than methods that use tree-based algorithms such as radix-tree in most cases.

However, RegExpRouter doesn't support all routing patterns, so it's usually used in combination with one of the other routers below that support all routing patterns.

## TrieRouter​

**TrieRouter** is the router using the Trie-tree algorithm. Like RegExpRouter, it does not use linear loops.

![](https://hono.dev/images/router-tree.jpg)

This router is not as fast as the RegExpRouter, but it is much faster than the Express router. TrieRouter supports all patterns.

## SmartRouter​

**SmartRouter** is useful when you're using multiple routers. It selects the best router by inferring from the registered routers. Hono uses SmartRouter, RegExpRouter, and TrieRouter by default:

ts

```
// Inside the core of Hono.
readonly defaultRouter: Router = new SmartRouter({
  routers: [new RegExpRouter(), new TrieRouter()],
})
```

When the application starts, SmartRouter detects the fastest router based on routing and continues to use it.

## LinearRouter​

RegExpRouter is fast, but the route registration phase can be slightly slow. So, it's not suitable for an environment that initializes with every request.

**LinearRouter** is optimized for "one shot" situations. Route registration is significantly faster than with RegExpRouter because it adds the route without compiling strings, using a linear approach.

The following is one of the benchmark results, which includes the route registration phase.

console

```
• GET /user/lookup/username/hey
----------------------------------------------------- -----------------------------
LinearRouter     1.82 µs/iter      (1.7 µs … 2.04 µs)   1.84 µs   2.04 µs   2.04 µs
MedleyRouter     4.44 µs/iter     (4.34 µs … 4.54 µs)   4.48 µs   4.54 µs   4.54 µs
FindMyWay       60.36 µs/iter      (45.5 µs … 1.9 ms)  59.88 µs  78.13 µs  82.92 µs
KoaTreeRouter    3.81 µs/iter     (3.73 µs … 3.87 µs)   3.84 µs   3.87 µs   3.87 µs
TrekRouter       5.84 µs/iter     (5.75 µs … 6.04 µs)   5.86 µs   6.04 µs   6.04 µs

summary for GET /user/lookup/username/hey
  LinearRouter
   2.1x faster than KoaTreeRouter
   2.45x faster than MedleyRouter
   3.21x faster than TrekRouter
   33.24x faster than FindMyWay
```

## PatternRouter​

**PatternRouter** is the smallest router among Hono's routers.

While Hono is already compact, if you need to make it even smaller for an environment with limited resources, use PatternRouter.

An application using only PatternRouter is under 15KB in size.

console

```
$ npx wrangler deploy --minify ./src/index.ts
 ⛅️ wrangler 3.20.0
-------------------
Total Upload: 14.68 KiB / gzip: 5.38 KiB
```

---

# Hono Stacks​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Hono Stacks​

Hono makes easy things easy and hard things easy. It is suitable for not just only returning JSON. But it's also great for building the full-stack application including REST API servers and the client.

## RPC​

Hono's RPC feature allows you to share API specs with little change to your code. The client generated by `hc` will read the spec and access the endpoint type-safety.

The following libraries make it possible.

- Hono - API Server
- [Zod](https://zod.dev) - Validator
- [Zod Validator Middleware](https://github.com/honojs/middleware/tree/main/packages/zod-validator)
- `hc` - HTTP Client

We can call the set of these components the **Hono Stack**. Now let's create an API server and a client with it.

## Writing API​

First, write an endpoint that receives a GET request and returns JSON.

ts

```
import { Hono } from 'hono'

const app = new Hono()

app.get('/hello', (c) => {
  return c.json({
    message: `Hello!`,
  })
})
```

## Validation with Zod​

Validate with Zod to receive the value of the query parameter.

![](https://hono.dev/images/sc01.gif)

ts

```
import { zValidator } from '@hono/zod-validator'
import * as z from 'zod'

app.get(
  '/hello',
  zValidator(
    'query',
    z.object({
      name: z.string(),
    })
  ),
  (c) => {
    const { name } = c.req.valid('query')
    return c.json({
      message: `Hello! ${name}`,
    })
  }
)
```

## Sharing the Types​

To emit an endpoint specification, export its type.

WARNING

For the RPC to infer routes correctly, all included methods must be chained, and the endpoint or app type must be inferred from a declared variable. For more, see [Best Practices for RPC](https://hono.dev/docs/guides/best-practices#if-you-want-to-use-rpc-features).

ts

```
const route = app.get(
  '/hello',
  zValidator(
    'query',
    z.object({
      name: z.string(),
    })
  ),
  (c) => {
    const { name } = c.req.valid('query')
    return c.json({
      message: `Hello! ${name}`,
    })
  }
)

export type AppType = typeof route
```

## Client​

Next. The client-side implementation. Create a client object by passing the `AppType` type to `hc` as generics. Then, magically, completion works and the endpoint path and request type are suggested.

![](https://hono.dev/images/sc03.gif)

ts

```
import { AppType } from './server'
import { hc } from 'hono/client'

const client = hc<AppType>('/api')
const res = await client.hello.$get({
  query: {
    name: 'Hono',
  },
})
```

The `Response` is compatible with the fetch API, but the data that can be retrieved with `json()` has a type.

![](https://hono.dev/images/sc04.gif)

ts

```
const data = await res.json()
console.log(`${data.message}`)
```

Sharing API specifications means that you can be aware of server-side changes.

![](https://hono.dev/images/ss03.png)

## With React​

You can create applications on Cloudflare Pages using React.

The API server.

ts

```
// functions/api/[[route]].ts
import { Hono } from 'hono'
import { handle } from 'hono/cloudflare-pages'
import * as z from 'zod'
import { zValidator } from '@hono/zod-validator'

const app = new Hono()

const schema = z.object({
  id: z.string(),
  title: z.string(),
})

type Todo = z.infer<typeof schema>

const todos: Todo[] = []

const route = app
  .post('/todo', zValidator('form', schema), (c) => {
    const todo = c.req.valid('form')
    todos.push(todo)
    return c.json({
      message: 'created!',
    })
  })
  .get((c) => {
    return c.json({
      todos,
    })
  })

export type AppType = typeof route

export const onRequest = handle(app, '/api')
```

The client with React and React Query.

tsx

```
// src/App.tsx
import {
  useQuery,
  useMutation,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import { AppType } from '../functions/api/[[route]]'
import { hc, InferResponseType, InferRequestType } from 'hono/client'

const queryClient = new QueryClient()
const client = hc<AppType>('/api')

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Todos />
    </QueryClientProvider>
  )
}

const Todos = () => {
  const query = useQuery({
    queryKey: ['todos'],
    queryFn: async () => {
      const res = await client.todo.$get()
      return await res.json()
    },
  })

  const $post = client.todo.$post

  const mutation = useMutation<
    InferResponseType<typeof $post>,
    Error,
    InferRequestType<typeof $post>['form']
  >({
    mutationFn: async (todo) => {
      const res = await $post({
        form: todo,
      })
      return await res.json()
    },
    onSuccess: async () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
    onError: (error) => {
      console.log(error)
    },
  })

  return (
    <div>
      <button
        onClick={() => {
          mutation.mutate({
            id: Date.now().toString(),
            title: 'Write code',
          })
        }}
      >
        Add Todo
      </button>

      <ul>
        {query.data?.todos.map((todo) => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
    </div>
  )
}
```

---

# Web Standards​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Web Standards​

Hono uses only **Web Standards** like Fetch. They were originally used in the `fetch` function and consist of basic objects that handle HTTP requests and responses. In addition to `Requests` and `Responses`, there are `URL`, `URLSearchParam`, `Headers` and others.

Cloudflare Workers, Deno, and Bun also build upon Web Standards. For example, a server that returns "Hello World" could be written as below. This could run on Cloudflare Workers and Bun.

ts

```
export default {
  async fetch() {
    return new Response('Hello World')
  },
}
```

Hono uses only Web Standards, which means that Hono can run on any runtime that supports them. In addition, we have a Node.js adapter. Hono runs on these runtimes:

- Cloudflare Workers (`workerd`)
- Deno
- Bun
- Fastly Compute
- AWS Lambda
- Node.js
- Vercel (edge-light)
- WebAssembly (w/ [WebAssembly System Interface (WASI)](https://github.com/WebAssembly/wasi) via [wasi:http](https://github.com/WebAssembly/wasi-http))

It also works on Netlify and other platforms. The same code runs on all platforms.

Cloudflare Workers, Deno, Shopify, and others launched [WinterCG](https://wintercg.org) to discuss the possibility of using the Web Standards to enable "web-interoperability". Hono will follow their steps and go for **the Standard of the Web Standards**.
