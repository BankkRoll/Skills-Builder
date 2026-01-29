# generateStaticParams and more

# generateStaticParams

> API reference for the generateStaticParams function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)generateStaticParams

# generateStaticParams

Last updated  December 12, 2025

The `generateStaticParams` function can be used in combination with [dynamic route segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) to [statically generate](https://nextjs.org/docs/app/guides/caching#static-rendering) routes at build time instead of on-demand at request time.

`generateStaticParams` can be used with:

- [Pages](https://nextjs.org/docs/app/api-reference/file-conventions/page) (`page.tsx`/`page.js`)
- [Layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout) (`layout.tsx`/`layout.js`)
- [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) (`route.ts`/`route.js`)

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
// Return a list of `params` to populate the [slug] dynamic segment
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())

  return posts.map((post) => ({
    slug: post.slug,
  }))
}

// Multiple versions of this page will be statically generated
// using the `params` returned by `generateStaticParams`
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // ...
}
```

> **Good to know**:
>
>
>
> - You can use the [dynamicParams](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamicparams) segment config option to control what happens when a dynamic segment is visited that was not generated with `generateStaticParams`.
> - You must return [an empty array fromgenerateStaticParams](#all-paths-at-build-time) or utilize [export const dynamic = 'force-static'](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamic) in order to revalidate (ISR) [paths at runtime](#all-paths-at-runtime).
> - During `next dev`, `generateStaticParams` will be called when you navigate to a route.
> - During `next build`, `generateStaticParams` runs before the corresponding Layouts or Pages are generated.
> - During revalidation (ISR), `generateStaticParams` will not be called again.
> - `generateStaticParams` replaces the [getStaticPaths](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths) function in the Pages Router.

## Parameters

`options.params` (optional)

If multiple dynamic segments in a route use `generateStaticParams`, the child `generateStaticParams` function is executed once for each set of `params` the parent generates.

The `params` object contains the populated `params` from the parent `generateStaticParams`, which can be used to [generate theparamsin a child segment](#multiple-dynamic-segments-in-a-route).

## Returns

`generateStaticParams` should return an array of objects where each object represents the populated dynamic segments of a single route.

- Each property in the object is a dynamic segment to be filled in for the route.
- The properties name is the segment's name, and the properties value is what that segment should be filled in with.

| Example Route | generateStaticParamsReturn Type |
| --- | --- |
| /product/[id] | { id: string }[] |
| /products/[category]/[product] | { category: string, product: string }[] |
| /products/[...slug] | { slug: string[] }[] |

## Single Dynamic Segment

 app/product/[id]/page.tsxJavaScriptTypeScript

```
export function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }, { id: '3' }]
}

// Three versions of this page will be statically generated
// using the `params` returned by `generateStaticParams`
// - /product/1
// - /product/2
// - /product/3
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  // ...
}
```

## Multiple Dynamic Segments

 app/products/[category]/[product]/page.tsxJavaScriptTypeScript

```
export function generateStaticParams() {
  return [
    { category: 'a', product: '1' },
    { category: 'b', product: '2' },
    { category: 'c', product: '3' },
  ]
}

// Three versions of this page will be statically generated
// using the `params` returned by `generateStaticParams`
// - /products/a/1
// - /products/b/2
// - /products/c/3
export default async function Page({
  params,
}: {
  params: Promise<{ category: string; product: string }>
}) {
  const { category, product } = await params
  // ...
}
```

## Catch-all Dynamic Segment

 app/product/[...slug]/page.tsxJavaScriptTypeScript

```
export function generateStaticParams() {
  return [{ slug: ['a', '1'] }, { slug: ['b', '2'] }, { slug: ['c', '3'] }]
}

// Three versions of this page will be statically generated
// using the `params` returned by `generateStaticParams`
// - /product/a/1
// - /product/b/2
// - /product/c/3
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string[] }>
}) {
  const { slug } = await params
  // ...
}
```

## Examples

### Static Rendering

#### All paths at build time

To statically render all paths at build time, supply the full list of paths to `generateStaticParams`:

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())

  return posts.map((post) => ({
    slug: post.slug,
  }))
}
```

#### Subset of paths at build time

To statically render a subset of paths at build time, and the rest the first time they're visited at runtime, return a partial list of paths:

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())

  // Render the first 10 posts at build time
  return posts.slice(0, 10).map((post) => ({
    slug: post.slug,
  }))
}
```

Then, by using the [dynamicParams](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamicparams) segment config option, you can control what happens when a dynamic segment is visited that was not generated with `generateStaticParams`.

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
// All posts besides the top 10 will be a 404
export const dynamicParams = false

export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then((res) => res.json())
  const topPosts = posts.slice(0, 10)

  return topPosts.map((post) => ({
    slug: post.slug,
  }))
}
```

#### All paths at runtime

To statically render all paths the first time they're visited, return an empty array (no paths will be rendered at build time) or utilize [export const dynamic = 'force-static'](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamic):

 app/blog/[slug]/page.js

```
export async function generateStaticParams() {
  return []
}
```

> **Good to know:**
>
>
>
> - You must always return an array from `generateStaticParams`, even if it's empty. Otherwise, the route will be dynamically rendered.

 app/changelog/[slug]/page.js

```
export const dynamic = 'force-static'
```

#### With Cache Components

When using [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) with dynamic routes, `generateStaticParams` must return **at least one param**. Empty arrays cause a [build error](https://nextjs.org/docs/messages/empty-generate-static-params). This allows Cache Components to validate your route doesn't incorrectly access `cookies()`, `headers()`, or `searchParams` at runtime.

> **Good to know**: If you don't know the actual param values at build time, you can return a placeholder param (e.g., `[{ slug: '__placeholder__' }]`) for validation, then handle it in your page with `notFound()`. However, this prevents build time validation from working effectively and may cause runtime errors.

See the [dynamic routes section](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#with-cache-components) for detailed walkthroughs.

### With Route Handlers

You can use `generateStaticParams` with [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) to statically generate API responses at build time:

 app/api/posts/[id]/route.tsJavaScriptTypeScript

```
export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }, { id: '3' }]
}

export async function GET(
  request: Request,
  { params }: RouteContext<'/api/posts/[id]'>
) {
  const { id } = await params
  // This will be statically generated for IDs 1, 2, and 3
  return Response.json({ id, title: `Post ${id}` })
}
```

### Route Handlers with Cache Components

When using [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components), combine with `use cache` for optimal caching:

 app/api/posts/[id]/route.ts

```
export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }, { id: '3' }]
}

async function getPost(id: Promise<string>) {
  'use cache'
  const resolvedId = await id
  const response = await fetch(`https://api.example.com/posts/${resolvedId}`)
  return response.json()
}

export async function GET(
  request: Request,
  { params }: RouteContext<'/api/posts/[id]'>
) {
  const post = await getPost(params.then((p) => p.id))
  return Response.json(post)
}
```

See the [Route Handlers documentation](https://nextjs.org/docs/app/api-reference/file-conventions/route#static-generation-with-generatestaticparams) for more details.

### Disable rendering for unspecified paths

To prevent unspecified paths from being statically rendered at runtime, add the `export const dynamicParams = false` option in a route segment. When this config option is used, only paths provided by `generateStaticParams` will be served, and unspecified routes will 404 or match (in the case of [catch-all routes](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#catch-all-segments)).

### Multiple Dynamic Segments in a Route

You can generate params for dynamic segments above the current layout or page, but **not below**. For example, given the `app/products/[category]/[product]` route:

- `app/products/[category]/[product]/page.js` can generate params for **both** `[category]` and `[product]`.
- `app/products/[category]/layout.js` can **only** generate params for `[category]`.

There are two approaches to generating params for a route with multiple dynamic segments:

#### Generate params from the bottom up

Generate multiple dynamic segments from the child route segment.

 app/products/[category]/[product]/page.tsxJavaScriptTypeScript

```
// Generate segments for both [category] and [product]
export async function generateStaticParams() {
  const products = await fetch('https://.../products').then((res) => res.json())

  return products.map((product) => ({
    category: product.category.slug,
    product: product.id,
  }))
}

export default function Page({
  params,
}: {
  params: Promise<{ category: string; product: string }>
}) {
  // ...
}
```

#### Generate params from the top down

Generate the parent segments first and use the result to generate the child segments.

 app/products/[category]/layout.tsxJavaScriptTypeScript

```
// Generate segments for [category]
export async function generateStaticParams() {
  const products = await fetch('https://.../products').then((res) => res.json())

  return products.map((product) => ({
    category: product.category.slug,
  }))
}

export default function Layout({
  params,
}: {
  params: Promise<{ category: string }>
}) {
  // ...
}
```

A child route segment's `generateStaticParams` function is executed once for each segment a parent `generateStaticParams` generates.

The child `generateStaticParams` function can use the `params` returned from the parent `generateStaticParams` function to dynamically generate its own segments.

 app/products/[category]/[product]/page.tsxJavaScriptTypeScript

```
// Generate segments for [product] using the `params` passed from
// the parent segment's `generateStaticParams` function
export async function generateStaticParams({
  params: { category },
}: {
  params: { category: string }
}) {
  const products = await fetch(
    `https://.../products?category=${category}`
  ).then((res) => res.json())

  return products.map((product) => ({
    product: product.id,
  }))
}

export default function Page({
  params,
}: {
  params: Promise<{ category: string; product: string }>
}) {
  // ...
}
```

Notice that the params argument can be accessed synchronously and includes only parent segment params.

For type completion, you can make use of the TypeScript `Awaited` helper in combination with either [Page Props helper](https://nextjs.org/docs/app/api-reference/file-conventions/page#page-props-helper) or [Layout Props helper](https://nextjs.org/docs/app/api-reference/file-conventions/layout#layout-props-helper):

 app/products/[category]/[product]/page.tsxJavaScriptTypeScript

```
export async function generateStaticParams({
  params: { category },
}: {
  params: Awaited<LayoutProps<'/products/[category]'>['params']>
}) {
  const products = await fetch(
    `https://.../products?category=${category}`
  ).then((res) => res.json())

  return products.map((product) => ({
    product: product.id,
  }))
}
```

> **Good to know**: `fetch` requests are automatically [memoized](https://nextjs.org/docs/app/guides/caching#request-memoization) for the same data across all `generate`-prefixed functions, Layouts, Pages, and Server Components. React [cachecan be used](https://nextjs.org/docs/app/guides/caching#react-cache-function) if `fetch` is unavailable.

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | generateStaticParamsintroduced. |

Was this helpful?

supported.

---

# generateViewport

> API Reference for the generateViewport function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)generateViewport

# generateViewport

Last updated  December 20, 2025

You can customize the initial viewport of the page with the static `viewport` object or the dynamic `generateViewport` function.

> **Good to know**:
>
>
>
> - The `viewport` object and `generateViewport` function exports are **only supported in Server Components**.
> - You cannot export both the `viewport` object and `generateViewport` function from the same route segment.
> - If you're coming from migrating `metadata` exports, you can use [metadata-to-viewport-export codemod](https://nextjs.org/docs/app/guides/upgrading/codemods#metadata-to-viewport-export) to update your changes.

## Theviewportobject

To define the viewport options, export a `viewport` object from a `layout.jsx` or `page.jsx` file.

 layout.tsx | page.tsxJavaScriptTypeScript

```
import type { Viewport } from 'next'

export const viewport: Viewport = {
  themeColor: 'black',
}

export default function Page() {}
```

## generateViewportfunction

`generateViewport` should return a [Viewportobject](#viewport-fields) containing one or more viewport fields.

 layout.tsx | page.tsxJavaScriptTypeScript

```
export function generateViewport({ params }) {
  return {
    themeColor: '...',
  }
}
```

In TypeScript, the `params` argument can be typed via [PageProps<'/route'>](https://nextjs.org/docs/app/api-reference/file-conventions/page#page-props-helper) or [LayoutProps<'/route'>](https://nextjs.org/docs/app/api-reference/file-conventions/layout#layout-props-helper) depending on where `generateViewport` is defined.

> **Good to know**:
>
>
>
> - If the viewport doesn't depend on runtime information, it should be defined using the static [viewportobject](#the-viewport-object) rather than `generateViewport`.

## Viewport Fields

### themeColor

Learn more about [theme-color](https://developer.mozilla.org/docs/Web/HTML/Element/meta/name/theme-color).

**Simple theme color**

 layout.tsx | page.tsxJavaScriptTypeScript

```
import type { Viewport } from 'next'

export const viewport: Viewport = {
  themeColor: 'black',
}
```

   <head> output

```
<meta name="theme-color" content="black" />
```

**With media attribute**

 layout.tsx | page.tsxJavaScriptTypeScript

```
import type { Viewport } from 'next'

export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: 'cyan' },
    { media: '(prefers-color-scheme: dark)', color: 'black' },
  ],
}
```

   <head> output

```
<meta name="theme-color" media="(prefers-color-scheme: light)" content="cyan" />
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="black" />
```

### width,initialScale,maximumScaleanduserScalable

> **Good to know**: The `viewport` meta tag is automatically set, and manual configuration is usually unnecessary as the default is sufficient. However, the information is provided for completeness.

 layout.tsx | page.tsxJavaScriptTypeScript

```
import type { Viewport } from 'next'

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  // Also supported but less commonly used
  // interactiveWidget: 'resizes-visual',
}
```

   <head> output

```
<meta
  name="viewport"
  content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"
/>
```

### colorScheme

Learn more about [color-scheme](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name#:~:text=color%2Dscheme%3A%20specifies,of%20the%20following%3A).

 layout.tsx | page.tsxJavaScriptTypeScript

```
import type { Viewport } from 'next'

export const viewport: Viewport = {
  colorScheme: 'dark',
}
```

   <head> output

```
<meta name="color-scheme" content="dark" />
```

## With Cache Components

When [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) is enabled, `generateViewport` follows the same rules as other components. If viewport accesses runtime data (`cookies()`, `headers()`, `params`, `searchParams`) or performs uncached data fetching, it defers to request time.

Unlike metadata, viewport cannot be streamed because it affects initial page load UI. If `generateViewport` defers to request time, the page would need to block until resolved.

If viewport depends on external data but not runtime data, use `use cache`:

 app/layout.tsx

```
export async function generateViewport() {
  'use cache'
  const { width, initialScale } = await db.query('viewport-size')
  return { width, initialScale }
}
```

If viewport genuinely requires runtime data, wrap the document `<body>` in a Suspense boundary to signal that the entire route should be dynamic:

 app/layout.tsx

```
import { Suspense } from 'react'
import { cookies } from 'next/headers'

export async function generateViewport() {
  const cookieJar = await cookies()
  return {
    themeColor: cookieJar.get('theme-color')?.value,
  }
}

export default function RootLayout({ children }) {
  return (
    <Suspense>
      <html>
        <body>{children}</body>
      </html>
    </Suspense>
  )
}
```

Caching is preferred because it allows static shell generation. Wrapping the document `body` in Suspense means there is no static shell or content to immediately send when a request arrives, making the entire route block until ready on every request.

> **Good to know**: Use [multiple root layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout) to isolate fully dynamic viewport to specific routes, while still letting other routes in your application generate a static shell.

## Types

You can add type safety to your viewport object by using the `Viewport` type. If you are using the [built-in TypeScript plugin](https://nextjs.org/docs/app/api-reference/config/typescript) in your IDE, you do not need to manually add the type, but you can still explicitly add it if you want.

### viewportobject

```
import type { Viewport } from 'next'

export const viewport: Viewport = {
  themeColor: 'black',
}
```

### generateViewportfunction

#### Regular function

```
import type { Viewport } from 'next'

export function generateViewport(): Viewport {
  return {
    themeColor: 'black',
  }
}
```

#### With segment props

```
import type { Viewport } from 'next'

type Props = {
  params: Promise<{ id: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export function generateViewport({ params, searchParams }: Props): Viewport {
  return {
    themeColor: 'black',
  }
}

export default function Page({ params, searchParams }: Props) {}
```

#### JavaScript Projects

For JavaScript projects, you can use JSDoc to add type safety.

```
/** @type {import("next").Viewport} */
export const viewport = {
  themeColor: 'black',
}
```

## Version History

| Version | Changes |
| --- | --- |
| v14.0.0 | viewportandgenerateViewportintroduced. |

## Next Steps

View all the Metadata API options.[Metadata FilesAPI documentation for the metadata file conventions.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)[Cache ComponentsLearn how to use Cache Components and combine the benefits of static and dynamic rendering.](https://nextjs.org/docs/app/getting-started/cache-components)[cacheComponentsLearn how to enable the cacheComponents flag in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)

Was this helpful?

supported.

---

# headers

> API reference for the headers function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)headers

# headers

Last updated  October 22, 2025

`headers` is an **async** function that allows you to **read** the HTTP incoming request headers from a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components).

 app/page.tsxJavaScriptTypeScript

```
import { headers } from 'next/headers'

export default async function Page() {
  const headersList = await headers()
  const userAgent = headersList.get('user-agent')
}
```

## Reference

### Parameters

`headers` does not take any parameters.

### Returns

`headers` returns a **read-only** [Web Headers](https://developer.mozilla.org/docs/Web/API/Headers) object.

- [Headers.entries()](https://developer.mozilla.org/docs/Web/API/Headers/entries): Returns an [iterator](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Iteration_protocols) allowing to go through all key/value pairs contained in this object.
- [Headers.forEach()](https://developer.mozilla.org/docs/Web/API/Headers/forEach): Executes a provided function once for each key/value pair in this `Headers` object.
- [Headers.get()](https://developer.mozilla.org/docs/Web/API/Headers/get): Returns a [String](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String) sequence of all the values of a header within a `Headers` object with a given name.
- [Headers.has()](https://developer.mozilla.org/docs/Web/API/Headers/has): Returns a boolean stating whether a `Headers` object contains a certain header.
- [Headers.keys()](https://developer.mozilla.org/docs/Web/API/Headers/keys): Returns an [iterator](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Iteration_protocols) allowing you to go through all keys of the key/value pairs contained in this object.
- [Headers.values()](https://developer.mozilla.org/docs/Web/API/Headers/values): Returns an [iterator](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Iteration_protocols) allowing you to go through all values of the key/value pairs contained in this object.

## Good to know

- `headers` is an **asynchronous** function that returns a promise. You must use `async/await` or React's [use](https://react.dev/reference/react/use) function.
  - In version 14 and earlier, `headers` was a synchronous function. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future.
- Since `headers` is read-only, you cannot `set` or `delete` the outgoing request headers.
- `headers` is a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) whose returned values cannot be known ahead of time. Using it in will opt a route into **dynamic rendering**.

## Examples

### Using the Authorization header

 app/page.js

```
import { headers } from 'next/headers'

export default async function Page() {
  const authorization = (await headers()).get('authorization')
  const res = await fetch('...', {
    headers: { authorization }, // Forward the authorization header
  })
  const user = await res.json()

  return <h1>{user.name}</h1>
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0-RC | headersis now an async function. Acodemodis available. |
| v13.0.0 | headersintroduced. |

Was this helpful?

supported.

---

# ImageResponse

> API Reference for the ImageResponse constructor.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)ImageResponse

# ImageResponse

Last updated  June 16, 2025

The `ImageResponse` constructor allows you to generate dynamic images using JSX and CSS. This is useful for generating social media images such as Open Graph images, Twitter cards, and more.

## Reference

### Parameters

The following parameters are available for `ImageResponse`:

```
import { ImageResponse } from 'next/og'

new ImageResponse(
  element: ReactElement,
  options: {
    width?: number = 1200
    height?: number = 630
    emoji?: 'twemoji' | 'blobmoji' | 'noto' | 'openmoji' = 'twemoji',
    fonts?: {
      name: string,
      data: ArrayBuffer,
      weight: number,
      style: 'normal' | 'italic'
    }[]
    debug?: boolean = false

    // Options that will be passed to the HTTP response
    status?: number = 200
    statusText?: string
    headers?: Record<string, string>
  },
)
```

> Examples are available in the [Vercel OG Playground](https://og-playground.vercel.app/).

### Supported HTML and CSS features

`ImageResponse` supports common CSS properties including flexbox and absolute positioning, custom fonts, text wrapping, centering, and nested images.

Please refer to [Satori’s documentation](https://github.com/vercel/satori#css) for a list of supported HTML and CSS features.

## Behavior

- `ImageResponse` uses [@vercel/og](https://vercel.com/docs/concepts/functions/edge-functions/og-image-generation), [Satori](https://github.com/vercel/satori), and Resvg to convert HTML and CSS into PNG.
- Only flexbox and a subset of CSS properties are supported. Advanced layouts (e.g. `display: grid`) will not work.
- Maximum bundle size of `500KB`. The bundle size includes your JSX, CSS, fonts, images, and any other assets. If you exceed the limit, consider reducing the size of any assets or fetching at runtime.
- Only `ttf`, `otf`, and `woff` font formats are supported. To maximize the font parsing speed, `ttf` or `otf` are preferred over `woff`.

## Examples

### Route Handlers

`ImageResponse` can be used in Route Handlers to generate images dynamically at request time.

 app/api/route.js

```
import { ImageResponse } from 'next/og'

export async function GET() {
  try {
    return new ImageResponse(
      (
        <div
          style={{
            height: '100%',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: 'white',
            padding: '40px',
          }}
        >
          <div
            style={{
              fontSize: 60,
              fontWeight: 'bold',
              color: 'black',
              textAlign: 'center',
            }}
          >
            Welcome to My Site
          </div>
          <div
            style={{
              fontSize: 30,
              color: '#666',
              marginTop: '20px',
            }}
          >
            Generated with Next.js ImageResponse
          </div>
        </div>
      ),
      {
        width: 1200,
        height: 630,
      }
    )
  } catch (e) {
    console.log(`${e.message}`)
    return new Response(`Failed to generate the image`, {
      status: 500,
    })
  }
}
```

### File-based Metadata

You can use `ImageResponse` in a [opengraph-image.tsx](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image) file to generate Open Graph images at build time or dynamically at request time.

 app/opengraph-image.tsx

```
import { ImageResponse } from 'next/og'

// Image metadata
export const alt = 'My site'
export const size = {
  width: 1200,
  height: 630,
}

export const contentType = 'image/png'

// Image generation
export default async function Image() {
  return new ImageResponse(
    (
      // ImageResponse JSX element
      <div
        style={{
          fontSize: 128,
          background: 'white',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        My site
      </div>
    ),
    // ImageResponse options
    {
      // For convenience, we can re-use the exported opengraph-image
      // size config to also set the ImageResponse's width and height.
      ...size,
    }
  )
}
```

### Custom fonts

You can use custom fonts in your `ImageResponse` by providing a `fonts` array in the options.

 app/opengraph-image.tsx

```
import { ImageResponse } from 'next/og'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'

// Image metadata
export const alt = 'My site'
export const size = {
  width: 1200,
  height: 630,
}

export const contentType = 'image/png'

// Image generation
export default async function Image() {
  // Font loading, process.cwd() is Next.js project directory
  const interSemiBold = await readFile(
    join(process.cwd(), 'assets/Inter-SemiBold.ttf')
  )

  return new ImageResponse(
    (
      // ...
    ),
    // ImageResponse options
    {
      // For convenience, we can re-use the exported opengraph-image
      // size config to also set the ImageResponse's width and height.
      ...size,
      fonts: [
        {
          name: 'Inter',
          data: interSemiBold,
          style: 'normal',
          weight: 400,
        },
      ],
    }
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v14.0.0 | ImageResponsemoved fromnext/servertonext/og |
| v13.3.0 | ImageResponsecan be imported fromnext/server. |
| v13.0.0 | ImageResponseintroduced via@vercel/ogpackage. |

Was this helpful?

supported.

---

# NextRequest

> API Reference for NextRequest.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)NextRequest

# NextRequest

Last updated  December 4, 2025

NextRequest extends the [Web Request API](https://developer.mozilla.org/docs/Web/API/Request) with additional convenience methods.

## cookies

Read or mutate the [Set-Cookie](https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie) header of the request.

### set(name, value)

Given a name, set a cookie with the given value on the request.

```
// Given incoming request /home
// Set a cookie to hide the banner
// request will have a `Set-Cookie:show-banner=false;path=/home` header
request.cookies.set('show-banner', 'false')
```

### get(name)

Given a cookie name, return the value of the cookie. If the cookie is not found, `undefined` is returned. If multiple cookies are found, the first one is returned.

```
// Given incoming request /home
// { name: 'show-banner', value: 'false', Path: '/home' }
request.cookies.get('show-banner')
```

### getAll()

Given a cookie name, return the values of the cookie. If no name is given, return all cookies on the request.

```
// Given incoming request /home
// [
//   { name: 'experiments', value: 'new-pricing-page', Path: '/home' },
//   { name: 'experiments', value: 'winter-launch', Path: '/home' },
// ]
request.cookies.getAll('experiments')
// Alternatively, get all cookies for the request
request.cookies.getAll()
```

### delete(name)

Given a cookie name, delete the cookie from the request.

```
// Returns true for deleted, false is nothing is deleted
request.cookies.delete('experiments')
```

### has(name)

Given a cookie name, return `true` if the cookie exists on the request.

```
// Returns true if cookie exists, false if it does not
request.cookies.has('experiments')
```

### clear()

Remove all cookies from the request.

```
request.cookies.clear()
```

## nextUrl

Extends the native [URL](https://developer.mozilla.org/docs/Web/API/URL) API with additional convenience methods, including Next.js specific properties.

```
// Given a request to /home, pathname is /home
request.nextUrl.pathname
// Given a request to /home?name=lee, searchParams is { 'name': 'lee' }
request.nextUrl.searchParams
```

The following options are available:

| Property | Type | Description |
| --- | --- | --- |
| basePath | string | Thebase pathof the URL. |
| buildId | string|undefined | The build identifier of the Next.js application. Can becustomized. |
| pathname | string | The pathname of the URL. |
| searchParams | Object | The search parameters of the URL. |

> **Note:** The internationalization properties from the Pages Router are not available for usage in the App Router. Learn more about [internationalization with the App Router](https://nextjs.org/docs/app/guides/internationalization).

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0 | ipandgeoremoved. |

Was this helpful?

supported.

---

# NextResponse

> API Reference for NextResponse.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)NextResponse

# NextResponse

Last updated  December 4, 2025

NextResponse extends the [Web Response API](https://developer.mozilla.org/docs/Web/API/Response) with additional convenience methods.

## cookies

Read or mutate the [Set-Cookie](https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie) header of the response.

### set(name, value)

Given a name, set a cookie with the given value on the response.

```
// Given incoming request /home
let response = NextResponse.next()
// Set a cookie to hide the banner
response.cookies.set('show-banner', 'false')
// Response will have a `Set-Cookie:show-banner=false;path=/home` header
return response
```

### get(name)

Given a cookie name, return the value of the cookie. If the cookie is not found, `undefined` is returned. If multiple cookies are found, the first one is returned.

```
// Given incoming request /home
let response = NextResponse.next()
// { name: 'show-banner', value: 'false', Path: '/home' }
response.cookies.get('show-banner')
```

### getAll()

Given a cookie name, return the values of the cookie. If no name is given, return all cookies on the response.

```
// Given incoming request /home
let response = NextResponse.next()
// [
//   { name: 'experiments', value: 'new-pricing-page', Path: '/home' },
//   { name: 'experiments', value: 'winter-launch', Path: '/home' },
// ]
response.cookies.getAll('experiments')
// Alternatively, get all cookies for the response
response.cookies.getAll()
```

### has(name)

Given a cookie name, return `true` if the cookie exists on the response.

```
// Given incoming request /home
let response = NextResponse.next()
// Returns true if cookie exists, false if it does not
response.cookies.has('experiments')
```

### delete(name)

Given a cookie name, delete the cookie from the response.

```
// Given incoming request /home
let response = NextResponse.next()
// Returns true for deleted, false if nothing is deleted
response.cookies.delete('experiments')
```

## json()

Produce a response with the given JSON body.

 app/api/route.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
}
```

## redirect()

Produce a response that redirects to a [URL](https://developer.mozilla.org/docs/Web/API/URL).

```
import { NextResponse } from 'next/server'

return NextResponse.redirect(new URL('/new', request.url))
```

The [URL](https://developer.mozilla.org/docs/Web/API/URL) can be created and modified before being used in the `NextResponse.redirect()` method. For example, you can use the `request.nextUrl` property to get the current URL, and then modify it to redirect to a different URL.

```
import { NextResponse } from 'next/server'

// Given an incoming request...
const loginUrl = new URL('/login', request.url)
// Add ?from=/incoming-url to the /login URL
loginUrl.searchParams.set('from', request.nextUrl.pathname)
// And redirect to the new URL
return NextResponse.redirect(loginUrl)
```

## rewrite()

Produce a response that rewrites (proxies) the given [URL](https://developer.mozilla.org/docs/Web/API/URL) while preserving the original URL.

```
import { NextResponse } from 'next/server'

// Incoming request: /about, browser shows /about
// Rewritten request: /proxy, browser shows /about
return NextResponse.rewrite(new URL('/proxy', request.url))
```

## next()

The `next()` method is useful for Proxy, as it allows you to return early and continue routing.

```
import { NextResponse } from 'next/server'

return NextResponse.next()
```

You can also forward `headers` upstream when producing the response, using `NextResponse.next({ request: { headers } })`:

```
import { NextResponse } from 'next/server'

// Given an incoming request...
const newHeaders = new Headers(request.headers)
// Add a new header
newHeaders.set('x-version', '123')
// Forward the modified request headers upstream
return NextResponse.next({
  request: {
    // New request headers
    headers: newHeaders,
  },
})
```

This forwards `newHeaders` upstream to the target page, route, or server action, and does not expose them to the client. While this pattern is useful for passing data upstream, it should be used with caution because the headers containing this data may be forwarded to external services.

In contrast, `NextResponse.next({ headers })` is a shorthand for sending headers from proxy to the client. This is **NOT** good practice and should be avoided. Among other reasons because setting response headers like `Content-Type`, can override framework expectations (for example, the `Content-Type` used by Server Actions), leading to failed submissions or broken streaming responses.

```
import { type NextRequest, NextResponse } from 'next/server'

async function proxy(request: NextRequest) {
  const headers = await injectAuth(request.headers)
  // DO NOT forward headers like this
  return NextResponse.next({ headers })
}
```

In general, avoid copying all incoming request headers because doing so can leak sensitive data to clients or upstream services.

Prefer a defensive approach by creating a subset of incoming request headers using an allow-list. For example, you might discard custom `x-*` headers and only forward known-safe headers:

```
import { type NextRequest, NextResponse } from 'next/server'

function proxy(request: NextRequest) {
  const incoming = new Headers(request.headers)
  const forwarded = new Headers()

  for (const [name, value] of incoming) {
    const headerName = name.toLowerCase()
    // Keep only known-safe headers, discard custom x-* and other sensitive ones
    if (
      !headerName.startsWith('x-') &&
      headerName !== 'authorization' &&
      headerName !== 'cookie'
    ) {
      // Preserve original header name casing
      forwarded.set(name, value)
    }
  }

  return NextResponse.next({
    request: {
      headers: forwarded,
    },
  })
}
```

Was this helpful?

supported.

---

# permanentRedirect

> API Reference for the permanentRedirect function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)permanentRedirect

# permanentRedirect

Last updated  January 23, 2026

The `permanentRedirect` function allows you to redirect the user to another URL. `permanentRedirect` can be used in Server Components, Client Components, [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data).

When used in a streaming context, this will insert a meta tag to emit the redirect on the client side. When used in a server action, it will serve a 303 HTTP redirect response to the caller. Otherwise, it will serve a 308 (Permanent) HTTP redirect response to the caller.

If a resource doesn't exist, you can use the [notFoundfunction](https://nextjs.org/docs/app/api-reference/functions/not-found) instead.

> **Good to know**: If you prefer to return a 307 (Temporary) HTTP redirect instead of 308 (Permanent), you can use the [redirectfunction](https://nextjs.org/docs/app/api-reference/functions/redirect) instead.

## Parameters

The `permanentRedirect` function accepts two arguments:

```
permanentRedirect(path, type)
```

| Parameter | Type | Description |
| --- | --- | --- |
| path | string | The URL to redirect to. Can be a relative or absolute path. |
| type | 'replace'(default) or'push'(default in Server Actions) | The type of redirect to perform. |

By default, `permanentRedirect` will use `push` (adding a new entry to the browser history stack) in [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data) and `replace` (replacing the current URL in the browser history stack) everywhere else. You can override this behavior by specifying the `type` parameter.

The `type` parameter has no effect when used in Server Components.

## Returns

`permanentRedirect` does not return a value.

## Example

Invoking the `permanentRedirect()` function throws a `NEXT_REDIRECT` error and terminates rendering of the route segment in which it was thrown.

 app/team/[id]/page.js

```
import { permanentRedirect } from 'next/navigation'

async function fetchTeam(id) {
  const res = await fetch('https://...')
  if (!res.ok) return undefined
  return res.json()
}

export default async function Profile({ params }) {
  const { id } = await params
  const team = await fetchTeam(id)
  if (!team) {
    permanentRedirect('/login')
  }

  // ...
}
```

> **Good to know**: `permanentRedirect` does not require you to use `return permanentRedirect()` as it uses the TypeScript [never](https://www.typescriptlang.org/docs/handbook/2/functions.html#never) type.

[redirectAPI Reference for the redirect function.](https://nextjs.org/docs/app/api-reference/functions/redirect)

Was this helpful?

supported.

---

# redirect

> API Reference for the redirect function.

[API Reference](https://nextjs.org/docs/app/api-reference)[Functions](https://nextjs.org/docs/app/api-reference/functions)redirect

# redirect

Last updated  January 23, 2026

The `redirect` function allows you to redirect the user to another URL. `redirect` can be used while rendering in [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data).

When used in a [streaming context](https://nextjs.org/docs/app/getting-started/linking-and-navigating#streaming), this will insert a meta tag to emit the redirect on the client side. When used in a server action, it will serve a 303 HTTP redirect response to the caller. Otherwise, it will serve a 307 HTTP redirect response to the caller.

If a resource doesn't exist, you can use the [notFoundfunction](https://nextjs.org/docs/app/api-reference/functions/not-found) instead.

## Reference

### Parameters

The `redirect` function accepts two arguments:

```
redirect(path, type)
```

| Parameter | Type | Description |
| --- | --- | --- |
| path | string | The URL to redirect to. Can be a relative or absolute path. |
| type | 'replace'(default) or'push'(default in Server Actions) | The type of redirect to perform. |

By default, `redirect` will use `push` (adding a new entry to the browser history stack) in [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data) and `replace` (replacing the current URL in the browser history stack) everywhere else. You can override this behavior by specifying the `type` parameter.

The `RedirectType` object contains the available options for the `type` parameter.

```
import { redirect, RedirectType } from 'next/navigation'

redirect('/redirect-to', RedirectType.replace)
// or
redirect('/redirect-to', RedirectType.push)
```

The `type` parameter has no effect when used in Server Components.

### Returns

`redirect` does not return a value.

## Behavior

- In Server Actions and Route Handlers, redirect should be called **outside** the `try` block when using `try/catch` statements.
- If you prefer to return a 308 (Permanent) HTTP redirect instead of 307 (Temporary), you can use the [permanentRedirectfunction](https://nextjs.org/docs/app/api-reference/functions/permanentRedirect) instead.
- `redirect` throws an error so it should be called **outside** the `try` block when using `try/catch` statements.
- `redirect` can be called in Client Components during the rendering process but not in event handlers. You can use the [useRouterhook](https://nextjs.org/docs/app/api-reference/functions/use-router) instead.
- `redirect` also accepts absolute URLs and can be used to redirect to external links.
- If you'd like to redirect before the render process, use [next.config.js](https://nextjs.org/docs/app/guides/redirecting#redirects-in-nextconfigjs) or [Proxy](https://nextjs.org/docs/app/guides/redirecting#nextresponseredirect-in-proxy).

## Example

### Server Component

Invoking the `redirect()` function throws a `NEXT_REDIRECT` error and terminates rendering of the route segment in which it was thrown.

 app/team/[id]/page.tsxJavaScriptTypeScript

```
import { redirect } from 'next/navigation'

async function fetchTeam(id: string) {
  const res = await fetch('https://...')
  if (!res.ok) return undefined
  return res.json()
}

export default async function Profile({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const team = await fetchTeam(id)

  if (!team) {
    redirect('/login')
  }

  // ...
}
```

> **Good to know**: `redirect` does not require you to use `return redirect()` as it uses the TypeScript [never](https://www.typescriptlang.org/docs/handbook/2/functions.html#never) type.

### Client Component

`redirect` can be directly used in a Client Component.

 components/client-redirect.tsxJavaScriptTypeScript

```
'use client'

import { redirect, usePathname } from 'next/navigation'

export function ClientRedirect() {
  const pathname = usePathname()

  if (pathname.startsWith('/admin') && !pathname.includes('/login')) {
    redirect('/admin/login')
  }

  return <div>Login Page</div>
}
```

> **Good to know**: When using `redirect` in a Client Component on initial page load during Server-Side Rendering (SSR), it will perform a server-side redirect.

`redirect` can be used in a Client Component through a Server Action. If you need to use an event handler to redirect the user, you can use the [useRouter](https://nextjs.org/docs/app/api-reference/functions/use-router) hook.

 app/client-redirect.tsxJavaScriptTypeScript

```
'use client'

import { navigate } from './actions'

export function ClientRedirect() {
  return (
    <form action={navigate}>
      <input type="text" name="id" />
      <button>Submit</button>
    </form>
  )
}
```

   app/actions.tsJavaScriptTypeScript

```
'use server'

import { redirect } from 'next/navigation'

export async function navigate(data: FormData) {
  redirect(`/posts/${data.get('id')}`)
}
```

## FAQ

### Why doesredirectuse 307 and 308?

When using `redirect()` you may notice that the status codes used are `307` for a temporary redirect, and `308` for a permanent redirect. While traditionally a `302` was used for a temporary redirect, and a `301` for a permanent redirect, many browsers changed the request method of the redirect, from a `POST` to `GET` request when using a `302`, regardless of the origins request method.

Taking the following example of a redirect from `/users` to `/people`, if you make a `POST` request to `/users` to create a new user, and are conforming to a `302` temporary redirect, the request method will be changed from a `POST` to a `GET` request. This doesn't make sense, as to create a new user, you should be making a `POST` request to `/people`, and not a `GET` request.

The introduction of the `307` status code means that the request method is preserved as `POST`.

- `302` - Temporary redirect, will change the request method from `POST` to `GET`
- `307` - Temporary redirect, will preserve the request method as `POST`

The `redirect()` method uses a `307` by default, instead of a `302` temporary redirect, meaning your requests will *always* be preserved as `POST` requests.

[Learn more](https://developer.mozilla.org/docs/Web/HTTP/Redirections) about HTTP Redirects.

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | redirectintroduced. |

[permanentRedirectAPI Reference for the permanentRedirect function.](https://nextjs.org/docs/app/api-reference/functions/permanentRedirect)

Was this helpful?

supported.
