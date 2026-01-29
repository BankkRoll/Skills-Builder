# Route Segment Config and more

# Route Segment Config

> Learn about how to configure options for Next.js route segments.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)Route Segment Config

# Route Segment Config

Last updated  October 23, 2025

> **Good to know**:
>
>
>
> - The options outlined on this page are disabled if the [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) flag is on, and will eventually be deprecated in the future.
> - Route Segment options only take effect in Server Component Pages, Layouts, or Route Handlers.
> - `generateStaticParams` cannot be used inside a `'use client'` file.

The Route Segment options allows you to configure the behavior of a [Page](https://nextjs.org/docs/app/api-reference/file-conventions/layout), [Layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout), or [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route) by directly exporting the following variables:

| Option | Type | Default |
| --- | --- | --- |
| dynamic | 'auto' | 'force-dynamic' | 'error' | 'force-static' | 'auto' |
| dynamicParams | boolean | true |
| revalidate | false | 0 | number | false |
| fetchCache | 'auto' | 'default-cache' | 'only-cache' | 'force-cache' | 'force-no-store' | 'default-no-store' | 'only-no-store' | 'auto' |
| runtime | 'nodejs' | 'edge' | 'nodejs' |
| preferredRegion | 'auto' | 'global' | 'home' | string | string[] | 'auto' |
| maxDuration | number | Set by deployment platform |

## Options

### dynamic

Change the dynamic behavior of a layout or page to fully static or fully dynamic.

 layout.tsx | page.tsx | route.tsJavaScriptTypeScript

```
export const dynamic = 'auto'
// 'auto' | 'force-dynamic' | 'error' | 'force-static'
```

> **Good to know**: The new model in the `app` directory favors granular caching control at the `fetch` request level over the binary all-or-nothing model of `getServerSideProps` and `getStaticProps` at the page-level in the `pages` directory. The `dynamic` option is a way to opt back in to the previous model as a convenience and provides a simpler migration path.

- **'auto'** (default): The default option to cache as much as possible without preventing any components from opting into dynamic behavior.
- **'force-dynamic'**: Force [dynamic rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering), which will result in routes being rendered for each user at request time. This option is equivalent to:
  - Setting the option of every `fetch()` request in a layout or page to `{ cache: 'no-store', next: { revalidate: 0 } }`.
  - Setting the segment config to `export const fetchCache = 'force-no-store'`
- **'error'**: Force static rendering and cache the data of a layout or page by causing an error if any components use [Dynamic APIs](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) or uncached data. This option is equivalent to:
  - `getStaticProps()` in the `pages` directory.
  - Setting the option of every `fetch()` request in a layout or page to `{ cache: 'force-cache' }`.
  - Setting the segment config to `fetchCache = 'only-cache'`.
- **'force-static'**: Force static rendering and cache the data of a layout or page by forcing [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies), [headers()](https://nextjs.org/docs/app/api-reference/functions/headers) and [useSearchParams()](https://nextjs.org/docs/app/api-reference/functions/use-search-params) to return empty values. It is possible to [revalidate](#revalidate), [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath), or [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag), in pages or layouts rendered with `force-static`.

> **Good to know**:
>
>
>
> - Instructions on [how to migrate](https://nextjs.org/docs/app/guides/migrating/app-router-migration#step-6-migrating-data-fetching-methods) from `getServerSideProps` and `getStaticProps` to `dynamic: 'force-dynamic'` and `dynamic: 'error'` can be found in the [upgrade guide](https://nextjs.org/docs/app/guides/migrating/app-router-migration#step-6-migrating-data-fetching-methods).

### dynamicParams

Control what happens when a dynamic segment is visited that was not generated with [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params).

 layout.tsx | page.tsxJavaScriptTypeScript

```
export const dynamicParams = true // true | false
```

- **true** (default): Dynamic segments not included in `generateStaticParams` are generated on demand.
- **false**: Dynamic segments not included in `generateStaticParams` will return a 404.

> **Good to know**:
>
>
>
> - This option replaces the `fallback: true | false | blocking` option of `getStaticPaths` in the `pages` directory.
> - To statically render all paths the first time they're visited, you'll need to return an empty array in `generateStaticParams` or utilize `export const dynamic = 'force-static'`.
> - When `dynamicParams = true`, the segment uses [Streaming Server Rendering](https://nextjs.org/docs/app/getting-started/linking-and-navigating#streaming).

### revalidate

Set the default revalidation time for a layout or page. This option does not override the `revalidate` value set by individual `fetch` requests.

 layout.tsx | page.tsx | route.tsJavaScriptTypeScript

```
export const revalidate = false
// false | 0 | number
```

- **false** (default): The default heuristic to cache any `fetch` requests that set their `cache` option to `'force-cache'` or are discovered before a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) is used. Semantically equivalent to `revalidate: Infinity` which effectively means the resource should be cached indefinitely. It is still possible for individual `fetch` requests to use `cache: 'no-store'` or `revalidate: 0` to avoid being cached and make the route dynamically rendered. Or set `revalidate` to a positive number lower than the route default to increase the revalidation frequency of a route.
- **0**: Ensure a layout or page is always [dynamically rendered](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) even if no Dynamic APIs or uncached data fetches are discovered. This option changes the default of `fetch` requests that do not set a `cache` option to `'no-store'` but leaves `fetch` requests that opt into `'force-cache'` or use a positive `revalidate` as is.
- **number**: (in seconds) Set the default revalidation frequency of a layout or page to `n` seconds.

> **Good to know**:
>
>
>
> - The revalidate value needs to be statically analyzable. For example `revalidate = 600` is valid, but `revalidate = 60 * 10` is not.
> - The revalidate value is not available when using `runtime = 'edge'`.
> - In Development, Pages are *always* rendered on-demand and are never cached. This allows you to see changes immediately without waiting for a revalidation period to pass.

#### Revalidation Frequency

- The lowest `revalidate` across each layout and page of a single route will determine the revalidation frequency of the *entire* route. This ensures that child pages are revalidated as frequently as their parent layouts.
- Individual `fetch` requests can set a lower `revalidate` than the route's default `revalidate` to increase the revalidation frequency of the entire route. This allows you to dynamically opt-in to more frequent revalidation for certain routes based on some criteria.

### fetchCache

 This is an advanced option that should only be used if you specifically need to override the default behavior.

By default, Next.js **will cache** any `fetch()` requests that are reachable **before** any [Dynamic APIs](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) are used and **will not cache** `fetch` requests that are discovered **after** Dynamic APIs are used.

`fetchCache` allows you to override the default `cache` option of all `fetch` requests in a layout or page.

layout.tsx | page.tsx | route.tsJavaScriptTypeScript

```
export const fetchCache = 'auto'
// 'auto' | 'default-cache' | 'only-cache'
// 'force-cache' | 'force-no-store' | 'default-no-store' | 'only-no-store'
```

- **'auto'** (default): The default option to cache `fetch` requests before Dynamic APIs with the `cache` option they provide and not cache `fetch` requests after Dynamic APIs.
- **'default-cache'**: Allow any `cache` option to be passed to `fetch` but if no option is provided then set the `cache` option to `'force-cache'`. This means that even `fetch` requests after Dynamic APIs are considered static.
- **'only-cache'**: Ensure all `fetch` requests opt into caching by changing the default to `cache: 'force-cache'` if no option is provided and causing an error if any `fetch` requests use `cache: 'no-store'`.
- **'force-cache'**: Ensure all `fetch` requests opt into caching by setting the `cache` option of all `fetch` requests to `'force-cache'`.
- **'default-no-store'**: Allow any `cache` option to be passed to `fetch` but if no option is provided then set the `cache` option to `'no-store'`. This means that even `fetch` requests before Dynamic APIs are considered dynamic.
- **'only-no-store'**: Ensure all `fetch` requests opt out of caching by changing the default to `cache: 'no-store'` if no option is provided and causing an error if any `fetch` requests use `cache: 'force-cache'`
- **'force-no-store'**: Ensure all `fetch` requests opt out of caching by setting the `cache` option of all `fetch` requests to `'no-store'`. This forces all `fetch` requests to be re-fetched every request even if they provide a `'force-cache'` option.

#### Cross-route segment behavior

- Any options set across each layout and page of a single route need to be compatible with each other.
  - If both the `'only-cache'` and `'force-cache'` are provided, then `'force-cache'` wins. If both `'only-no-store'` and `'force-no-store'` are provided, then `'force-no-store'` wins. The force option changes the behavior across the route so a single segment with `'force-*'` would prevent any errors caused by `'only-*'`.
  - The intention of the `'only-*'` and `'force-*'` options is to guarantee the whole route is either fully static or fully dynamic. This means:
    - A combination of `'only-cache'` and `'only-no-store'` in a single route is not allowed.
    - A combination of `'force-cache'` and `'force-no-store'` in a single route is not allowed.
  - A parent cannot provide `'default-no-store'` if a child provides `'auto'` or `'*-cache'` since that could make the same fetch have different behavior.
- It is generally recommended to leave shared parent layouts as `'auto'` and customize the options where child segments diverge.

### runtime

We recommend using the Node.js runtime for rendering your application. This option cannot be used in [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy).

> **Good to know**: Using `runtime: 'edge'` is **not supported** for Cache Components.

 layout.tsx | page.tsx | route.tsJavaScriptTypeScript

```
export const runtime = 'nodejs'
// 'nodejs' | 'edge'
```

- **'nodejs'** (default)
- **'edge'**

### preferredRegion

 layout.tsx | page.tsx | route.tsJavaScriptTypeScript

```
export const preferredRegion = 'auto'
// 'auto' | 'global' | 'home' | ['iad1', 'sfo1']
```

Support for `preferredRegion`, and regions supported, is dependent on your deployment platform.

> **Good to know**:
>
>
>
> - If a `preferredRegion` is not specified, it will inherit the option of the nearest parent layout.
> - The root layout defaults to `all` regions.

### maxDuration

By default, Next.js does not limit the execution of server-side logic (rendering a page or handling an API).
Deployment platforms can use `maxDuration` from the Next.js build output to add specific execution limits.

**Note**: This setting requires Next.js `13.4.10` or higher.

 layout.tsx | page.tsx | route.tsJavaScriptTypeScript

```
export const maxDuration = 5
```

> **Good to know**:
>
>
>
> - If using [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data), set the `maxDuration` at the page level to change the default timeout of all Server Actions used on the page.

### generateStaticParams

The `generateStaticParams` function can be used in combination with [dynamic route segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) to define the list of route segment parameters that will be statically generated at build time instead of on-demand at request time.

See the [API reference](https://nextjs.org/docs/app/api-reference/functions/generate-static-params) for more details.

## Version History

| Version |  |
| --- | --- |
| v16.0.0 | export const experimental_ppr = trueremoved. Acodemodis available. |
| v15.0.0-RC | export const runtime = "experimental-edge"deprecated. Acodemodis available. |

Was this helpful?

supported.

---

# route.js

> API reference for the route.js special file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)route.js

# route.js

Last updated  December 12, 2025

Route Handlers allow you to create custom request handlers for a given route using the Web [Request](https://developer.mozilla.org/docs/Web/API/Request) and [Response](https://developer.mozilla.org/docs/Web/API/Response) APIs.

 route.tsJavaScriptTypeScript

```
export async function GET() {
  return Response.json({ message: 'Hello World' })
}
```

## Reference

### HTTP Methods

A **route** file allows you to create custom request handlers for a given route. The following [HTTP methods](https://developer.mozilla.org/docs/Web/HTTP/Methods) are supported: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, and `OPTIONS`.

 route.tsJavaScriptTypeScript

```
export async function GET(request: Request) {}

export async function HEAD(request: Request) {}

export async function POST(request: Request) {}

export async function PUT(request: Request) {}

export async function DELETE(request: Request) {}

export async function PATCH(request: Request) {}

// If `OPTIONS` is not defined, Next.js will automatically implement `OPTIONS` and set the appropriate Response `Allow` header depending on the other methods defined in the Route Handler.
export async function OPTIONS(request: Request) {}
```

### Parameters

#### request(optional)

The `request` object is a [NextRequest](https://nextjs.org/docs/app/api-reference/functions/next-request) object, which is an extension of the Web [Request](https://developer.mozilla.org/docs/Web/API/Request) API. `NextRequest` gives you further control over the incoming request, including easily accessing `cookies` and an extended, parsed, URL object `nextUrl`.

 route.tsJavaScriptTypeScript

```
import type { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const url = request.nextUrl
}
```

#### context(optional)

- **params**: a promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) for the current route.

 app/dashboard/[team]/route.tsJavaScriptTypeScript

```
export async function GET(
  request: Request,
  { params }: { params: Promise<{ team: string }> }
) {
  const { team } = await params
}
```

| Example | URL | params |
| --- | --- | --- |
| app/dashboard/[team]/route.js | /dashboard/1 | Promise<{ team: '1' }> |
| app/shop/[tag]/[item]/route.js | /shop/1/2 | Promise<{ tag: '1', item: '2' }> |
| app/blog/[...slug]/route.js | /blog/1/2 | Promise<{ slug: ['1', '2'] }> |

### Route Context Helper

You can type the Route Handler context using `RouteContext` to get strongly typed `params` from a route literal. `RouteContext` is a globally available helper.

 app/users/[id]/route.ts

```
import type { NextRequest } from 'next/server'

export async function GET(_req: NextRequest, ctx: RouteContext<'/users/[id]'>) {
  const { id } = await ctx.params
  return Response.json({ id })
}
```

> **Good to know**
>
>
>
> - Types are generated during `next dev`, `next build` or `next typegen`.
> - After type generation, the `RouteContext` helper is globally available. It doesn't need to be imported.

## Examples

### Cookies

You can read or set cookies with [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies) from `next/headers`.

 route.tsJavaScriptTypeScript

```
import { cookies } from 'next/headers'

export async function GET(request: NextRequest) {
  const cookieStore = await cookies()

  const a = cookieStore.get('a')
  const b = cookieStore.set('b', '1')
  const c = cookieStore.delete('c')
}
```

Alternatively, you can return a new `Response` using the [Set-Cookie](https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie) header.

 app/api/route.tsJavaScriptTypeScript

```
import { cookies } from 'next/headers'

export async function GET(request: Request) {
  const cookieStore = await cookies()
  const token = cookieStore.get('token')

  return new Response('Hello, Next.js!', {
    status: 200,
    headers: { 'Set-Cookie': `token=${token.value}` },
  })
}
```

You can also use the underlying Web APIs to read cookies from the request ([NextRequest](https://nextjs.org/docs/app/api-reference/functions/next-request)):

 app/api/route.tsJavaScriptTypeScript

```
import { type NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const token = request.cookies.get('token')
}
```

### Headers

You can read headers with [headers](https://nextjs.org/docs/app/api-reference/functions/headers) from `next/headers`.

 route.tsJavaScriptTypeScript

```
import { headers } from 'next/headers'
import type { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const headersList = await headers()
  const referer = headersList.get('referer')
}
```

This `headers` instance is read-only. To set headers, you need to return a new `Response` with new `headers`.

 app/api/route.tsJavaScriptTypeScript

```
import { headers } from 'next/headers'

export async function GET(request: Request) {
  const headersList = await headers()
  const referer = headersList.get('referer')

  return new Response('Hello, Next.js!', {
    status: 200,
    headers: { referer: referer },
  })
}
```

You can also use the underlying Web APIs to read headers from the request ([NextRequest](https://nextjs.org/docs/app/api-reference/functions/next-request)):

 app/api/route.tsJavaScriptTypeScript

```
import { type NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const requestHeaders = new Headers(request.headers)
}
```

### Revalidating Cached Data

You can [revalidate cached data](https://nextjs.org/docs/app/guides/incremental-static-regeneration) using the `revalidate` route segment config option.

 app/posts/route.tsJavaScriptTypeScript

```
export const revalidate = 60

export async function GET() {
  const data = await fetch('https://api.vercel.app/blog')
  const posts = await data.json()

  return Response.json(posts)
}
```

### Redirects

 app/api/route.tsJavaScriptTypeScript

```
import { redirect } from 'next/navigation'

export async function GET(request: Request) {
  redirect('https://nextjs.org/')
}
```

### Dynamic Route Segments

Route Handlers can use [Dynamic Segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) to create request handlers from dynamic data.

 app/items/[slug]/route.tsJavaScriptTypeScript

```
export async function GET(
  request: Request,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params // 'a', 'b', or 'c'
}
```

| Route | Example URL | params |
| --- | --- | --- |
| app/items/[slug]/route.js | /items/a | Promise<{ slug: 'a' }> |
| app/items/[slug]/route.js | /items/b | Promise<{ slug: 'b' }> |
| app/items/[slug]/route.js | /items/c | Promise<{ slug: 'c' }> |

#### Static Generation withgenerateStaticParams

You can use [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params) with dynamic Route Handlers to statically generate responses at build time for specified params, while handling other params dynamically at request time.

When using [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components), you can combine `generateStaticParams` with `use cache` to enable data caching for both prerendered and runtime params.

See the [generateStaticParams with Route Handlers](https://nextjs.org/docs/app/api-reference/functions/generate-static-params#with-route-handlers) documentation for examples and details.

### URL Query Parameters

The request object passed to the Route Handler is a `NextRequest` instance, which includes [some additional convenience methods](https://nextjs.org/docs/app/api-reference/functions/next-request#nexturl), such as those for more easily handling query parameters.

 app/api/search/route.tsJavaScriptTypeScript

```
import { type NextRequest } from 'next/server'

export function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('query')
  // query is "hello" for /api/search?query=hello
}
```

### Streaming

Streaming is commonly used in combination with Large Language Models (LLMs), such as OpenAI, for AI-generated content. Learn more about the [AI SDK](https://sdk.vercel.ai/docs/introduction).

 app/api/chat/route.tsJavaScriptTypeScript

```
import { openai } from '@ai-sdk/openai'
import { StreamingTextResponse, streamText } from 'ai'

export async function POST(req: Request) {
  const { messages } = await req.json()
  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
  })

  return new StreamingTextResponse(result.toAIStream())
}
```

These abstractions use the Web APIs to create a stream. You can also use the underlying Web APIs directly.

 app/api/route.tsJavaScriptTypeScript

```
// https://developer.mozilla.org/docs/Web/API/ReadableStream#convert_async_iterator_to_stream
function iteratorToStream(iterator: any) {
  return new ReadableStream({
    async pull(controller) {
      const { value, done } = await iterator.next()

      if (done) {
        controller.close()
      } else {
        controller.enqueue(value)
      }
    },
  })
}

function sleep(time: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, time)
  })
}

const encoder = new TextEncoder()

async function* makeIterator() {
  yield encoder.encode('<p>One</p>')
  await sleep(200)
  yield encoder.encode('<p>Two</p>')
  await sleep(200)
  yield encoder.encode('<p>Three</p>')
}

export async function GET() {
  const iterator = makeIterator()
  const stream = iteratorToStream(iterator)

  return new Response(stream)
}
```

### Request Body

You can read the `Request` body using the standard Web API methods:

 app/items/route.tsJavaScriptTypeScript

```
export async function POST(request: Request) {
  const res = await request.json()
  return Response.json({ res })
}
```

### Request Body FormData

You can read the `FormData` using the `request.formData()` function:

 app/items/route.tsJavaScriptTypeScript

```
export async function POST(request: Request) {
  const formData = await request.formData()
  const name = formData.get('name')
  const email = formData.get('email')
  return Response.json({ name, email })
}
```

Since `formData` data are all strings, you may want to use [zod-form-data](https://www.npmjs.com/zod-form-data) to validate the request and retrieve data in the format you prefer (e.g. `number`).

### CORS

You can set CORS headers for a specific Route Handler using the standard Web API methods:

 app/api/route.tsJavaScriptTypeScript

```
export async function GET(request: Request) {
  return new Response('Hello, Next.js!', {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}
```

> **Good to know**:
>
>
>
> - To add CORS headers to multiple Route Handlers, you can use [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy#cors) or the [next.config.jsfile](https://nextjs.org/docs/app/api-reference/config/next-config-js/headers#cors).

### Webhooks

You can use a Route Handler to receive webhooks from third-party services:

 app/api/route.tsJavaScriptTypeScript

```
export async function POST(request: Request) {
  try {
    const text = await request.text()
    // Process the webhook payload
  } catch (error) {
    return new Response(`Webhook error: ${error.message}`, {
      status: 400,
    })
  }

  return new Response('Success!', {
    status: 200,
  })
}
```

Notably, unlike API Routes with the Pages Router, you do not need to use `bodyParser` to use any additional configuration.

### Non-UI Responses

You can use Route Handlers to return non-UI content. Note that [sitemap.xml](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap#generating-a-sitemap-using-code-js-ts), [robots.txt](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots#generate-a-robots-file), [app icons](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons#generate-icons-using-code-js-ts-tsx), and [open graph images](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image) all have built-in support.

 app/rss.xml/route.tsJavaScriptTypeScript

```
export async function GET() {
  return new Response(
    `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
  <title>Next.js Documentation</title>
  <link>https://nextjs.org/docs</link>
  <description>The React Framework for the Web</description>
</channel>

</rss>`,
    {
      headers: {
        'Content-Type': 'text/xml',
      },
    }
  )
}
```

### Segment Config Options

Route Handlers use the same [route segment configuration](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config) as pages and layouts.

 app/items/route.tsJavaScriptTypeScript

```
export const dynamic = 'auto'
export const dynamicParams = true
export const revalidate = false
export const fetchCache = 'auto'
export const runtime = 'nodejs'
export const preferredRegion = 'auto'
```

See the [API reference](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config) for more details.

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0-RC | context.paramsis now a promise. Acodemodis available |
| v15.0.0-RC | The default caching forGEThandlers was changed from static to dynamic |
| v13.2.0 | Route Handlers are introduced. |

Was this helpful?

supported.

---

# src Folder

> Save pages under the `src` folder as an alternative to the root `pages` directory.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)src

# src Folder

Last updated  October 17, 2025

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

[Project StructureLearn the folder and file conventions in Next.js, and how to organize your project.](https://nextjs.org/docs/app/getting-started/project-structure)

Was this helpful?

supported.

---

# template.js

> API Reference for the template.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)template.js

# template.js

Last updated  October 17, 2025

A **template** file is similar to a [layout](https://nextjs.org/docs/app/getting-started/layouts-and-pages#creating-a-layout) in that it wraps a layout or page. Unlike layouts that persist across routes and maintain state, templates are given a unique key, meaning children Client Components reset their state on navigation.

They are useful when you need to:

- Resynchronize `useEffect` on navigation.
- Reset the state of a child Client Components on navigation. For example, an input field.
- To change default framework behavior. For example, Suspense boundaries inside layouts only show a fallback on first load, while templates show it on every navigation.

## Convention

A template can be defined by exporting a default React component from a `template.js` file. The component should accept a `children` prop.

 ![template.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ftemplate-special-file.png&w=3840&q=75)![template.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ftemplate-special-file.png&w=3840&q=75) app/template.tsxJavaScriptTypeScript

```
export default function Template({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

In terms of nesting, `template.js` is rendered between a layout and its children. Here's a simplified output:

 Output

```
<Layout>
  {/* Note that the template is given a unique key. */}
  <Template key={routeParam}>{children}</Template>
</Layout>
```

## Props

### children(required)

Template accepts a `children` prop.

 Output

```
<Layout>
  {/* Note that the template is automatically given a unique key. */}
  <Template key={routeParam}>{children}</Template>
</Layout>
```

## Behavior

- **Server Components**: By default, templates are Server Components.
- **With navigation**: Templates receive a unique key for their own segment level. They remount when that segment (including its dynamic params) changes. Navigations within deeper segments do not remount higher-level templates. Search params do not trigger remounts.
- **State reset**: Any Client Component inside the template will reset its state on navigation.
- **Effect re-run**: Effects like `useEffect` will re-synchronize as the component remounts.
- **DOM reset**: DOM elements inside the template are fully recreated.

### Templates during navigation and remounting

This section illustrates how templates behave during navigation. It shows, step by step, which templates remount on each route change and why.

Using this project tree:

```
app
├── about
│   ├── page.tsx
├── blog
│   ├── [slug]
│   │   └── page.tsx
│   ├── page.tsx
│   └── template.tsx
├── layout.tsx
├── page.tsx
└── template.tsx
```

Starting at `/`, the React tree looks roughly like this.

> Note: The `key` values shown in the examples are illustrative, the values in your application may differ.

 Output

```
<RootLayout>
  {/* app/template.tsx */}
  <Template key="/">
    <Page />
  </Template>
</RootLayout>
```

Navigating to `/about` (first segment changes), the root template key changes, it remounts:

 Output

```
<RootLayout>
  {/* app/template.tsx */}
  <Template key="/about">
    <AboutPage />
  </Template>
</RootLayout>
```

Navigating to `/blog` (first segment changes), the root template key changes, it remounts and the blog-level template mounts:

 Output

```
<RootLayout>
  {/* app/template.tsx (root) */}
  <Template key="/blog">
    {/* app/blog/template.tsx */}
    <Template key="/blog">
      <BlogIndexPage />
    </Template>
  </Template>
</RootLayout>
```

Navigating within the same first segment to `/blog/first-post` (child segment changes), the root template key doesn't change, but the blog-level template key changes, it remounts:

 Output

```
<RootLayout>
  {/* app/template.tsx (root) */}
  <Template key="/blog">
    {/* app/blog/template.tsx */}
    {/* remounts because the child segment at this level changed */}
    <Template key="/blog/first-post">
      <BlogPostPage slug="first-post" />
    </Template>
  </Template>
</RootLayout>
```

Navigating to `/blog/second-post` (same first segment, different child segment), the root template key doesn't change, but the blog-level template key changes, it remounts again:

 Output

```
<RootLayout>
  {/* app/template.tsx (root) */}
  <Template key="/blog">
    {/* app/blog/template.tsx */}
    {/* remounts again due to changed child segment */}
    <Template key="/blog/second-post">
      <BlogPostPage slug="second-post" />
    </Template>
  </Template>
</RootLayout>
```

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | templateintroduced. |

Was this helpful?

supported.

---

# unauthorized.js

> API reference for the unauthorized.js special file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)unauthorized.js

# unauthorized.js

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

The **unauthorized** file is used to render UI when the [unauthorized](https://nextjs.org/docs/app/api-reference/functions/unauthorized) function is invoked during authentication. Along with allowing you to customize the UI, Next.js will return a `401` status code.

 app/unauthorized.tsxJavaScriptTypeScript

```
import Login from '@/app/components/Login'

export default function Unauthorized() {
  return (
    <main>
      <h1>401 - Unauthorized</h1>
      <p>Please log in to access this page.</p>
      <Login />
    </main>
  )
}
```

## Reference

### Props

`unauthorized.js` components do not accept any props.

## Examples

### Displaying login UI to unauthenticated users

You can use [unauthorized](https://nextjs.org/docs/app/api-reference/functions/unauthorized) function to render the `unauthorized.js` file with a login UI.

 app/dashboard/page.tsxJavaScriptTypeScript

```
import { verifySession } from '@/app/lib/dal'
import { unauthorized } from 'next/navigation'

export default async function DashboardPage() {
  const session = await verifySession()

  if (!session) {
    unauthorized()
  }

  return <div>Dashboard</div>
}
```

   app/unauthorized.tsxJavaScriptTypeScript

```
import Login from '@/app/components/Login'

export default function UnauthorizedPage() {
  return (
    <main>
      <h1>401 - Unauthorized</h1>
      <p>Please log in to access this page.</p>
      <Login />
    </main>
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.1.0 | unauthorized.jsintroduced. |

[unauthorizedAPI Reference for the unauthorized function.](https://nextjs.org/docs/app/api-reference/functions/unauthorized)

Was this helpful?

supported.

---

# File

> API Reference for Next.js file-system conventions.

[App Router](https://nextjs.org/docs/app)[API Reference](https://nextjs.org/docs/app/api-reference)File-system conventions

# File-system conventions

Last updated  June 16, 2025[default.jsAPI Reference for the default.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/default)[Dynamic SegmentsDynamic Route Segments can be used to programmatically generate route segments from dynamic data.](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes)[error.jsAPI reference for the error.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/error)[forbidden.jsAPI reference for the forbidden.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/forbidden)[instrumentation.jsAPI reference for the instrumentation.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/instrumentation)[instrumentation-client.jsLearn how to add client-side instrumentation to track and monitor your Next.js application's frontend performance.](https://nextjs.org/docs/app/api-reference/file-conventions/instrumentation-client)[Intercepting RoutesUse intercepting routes to load a new route within the current layout while masking the browser URL, useful for advanced routing patterns such as modals.](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes)[layout.jsAPI reference for the layout.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/layout)[loading.jsAPI reference for the loading.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/loading)[mdx-components.jsAPI reference for the mdx-components.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/mdx-components)[not-found.jsAPI reference for the not-found.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/not-found)[page.jsAPI reference for the page.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/page)[Parallel RoutesSimultaneously render one or more pages in the same view that can be navigated independently. A pattern for highly dynamic applications.](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes)[proxy.jsAPI reference for the proxy.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)[publicNext.js allows you to serve static files, like images, in the public directory. You can learn how it works here.](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder)[route.jsAPI reference for the route.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/route)[Route GroupsRoute Groups can be used to partition your Next.js application into different sections.](https://nextjs.org/docs/app/api-reference/file-conventions/route-groups)[Route Segment ConfigLearn about how to configure options for Next.js route segments.](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config)[srcSave pages under the `src` folder as an alternative to the root `pages` directory.](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder)[template.jsAPI Reference for the template.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/template)[unauthorized.jsAPI reference for the unauthorized.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/unauthorized)[Metadata FilesAPI documentation for the metadata file conventions.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)

Was this helpful?

supported.

---

# after

> API Reference for the after function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)after

# after

Last updated  January 23, 2026

`after` allows you to schedule work to be executed after a response (or prerender) is finished. This is useful for tasks and other side effects that should not block the response, such as logging and analytics.

It can be used in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) (including [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)), [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data), [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy).

The function accepts a callback that will be executed after the response (or prerender) is finished:

 app/layout.tsxJavaScriptTypeScript

```
import { after } from 'next/server'
// Custom logging function
import { log } from '@/app/utils'

export default function Layout({ children }: { children: React.ReactNode }) {
  after(() => {
    // Execute after the layout is rendered and sent to the user
    log()
  })
  return <>{children}</>
}
```

> **Good to know:** `after` is not a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) and calling it does not cause a route to become dynamic. If it's used within a static page, the callback will execute at build time, or whenever a page is revalidated.

## Reference

### Parameters

- A callback function which will be executed after the response (or prerender) is finished.

### Duration

`after` will run for the platform's default or configured max duration of your route. If your platform supports it, you can configure the timeout limit using the [maxDuration](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#maxduration) route segment config.

## Good to know

- `after` will be executed even if the response didn't complete successfully. Including when an error is thrown or when `notFound` or `redirect` is called.
- You can use React `cache` to deduplicate functions called inside `after`.
- `after` can be nested inside other `after` calls, for example, you can create utility functions that wrap `after` calls to add additional functionality.

## Examples

### With request APIs

You can use request APIs such as [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies) and [headers](https://nextjs.org/docs/app/api-reference/functions/headers) inside `after` in [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data) and [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route). This is useful for logging activity after a mutation. For example:

 app/api/route.tsJavaScriptTypeScript

```
import { after } from 'next/server'
import { cookies, headers } from 'next/headers'
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // Perform mutation
  // ...

  // Log user activity for analytics
  after(async () => {
    const userAgent = (await headers().get('user-agent')) || 'unknown'
    const sessionCookie =
      (await cookies().get('session-id'))?.value || 'anonymous'

    logUserAction({ sessionCookie, userAgent })
  })

  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}
```

However, you cannot use these request APIs inside `after` in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components). This is because Next.js needs to know which part of the tree access the request APIs to support [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components), but `after` runs after React's rendering lifecycle.

## Platform Support

| Deployment Option | Supported |
| --- | --- |
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

Learn how to [configureafter](https://nextjs.org/docs/app/guides/self-hosting#after) when self-hosting Next.js.

 Reference: supporting `after` for serverless platforms

Using `after` in a serverless context requires waiting for asynchronous tasks to finish after the response has been sent. In Next.js and Vercel, this is achieved using a primitive called `waitUntil(promise)`, which extends the lifetime of a serverless invocation until all promises passed to [waitUntil](https://vercel.com/docs/functions/functions-api-reference#waituntil) have settled.

If you want your users to be able to run `after`, you will have to provide your implementation of `waitUntil` that behaves in an analogous way.

When `after` is called, Next.js will access `waitUntil` like this:

```
const RequestContext = globalThis[Symbol.for('@next/request-context')]
const contextValue = RequestContext?.get()
const waitUntil = contextValue?.waitUntil
```

Which means that `globalThis[Symbol.for('@next/request-context')]` is expected to contain an object like this:

```
type NextRequestContext = {
  get(): NextRequestContextValue | undefined
}

type NextRequestContextValue = {
  waitUntil?: (promise: Promise<any>) => void
}
```

Here is an example of the implementation.

```
import { AsyncLocalStorage } from 'node:async_hooks'

const RequestContextStorage = new AsyncLocalStorage<NextRequestContextValue>()

// Define and inject the accessor that next.js will use
const RequestContext: NextRequestContext = {
  get() {
    return RequestContextStorage.getStore()
  },
}
globalThis[Symbol.for('@next/request-context')] = RequestContext

const handler = (req, res) => {
  const contextValue = { waitUntil: YOUR_WAITUNTIL }
  // Provide the value
  return RequestContextStorage.run(contextValue, () => nextJsHandler(req, res))
}
```

## Version History

| Version History | Description |
| --- | --- |
| v15.1.0 | afterbecame stable. |
| v15.0.0-rc | unstable_afterintroduced. |

Was this helpful?

supported.
