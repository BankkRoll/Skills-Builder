# How to upgrade to version 15 and more

# How to upgrade to version 15

> Upgrade your Next.js Application from Version 14 to 15.

[Guides](https://nextjs.org/docs/app/guides)[Upgrading](https://nextjs.org/docs/app/guides/upgrading)Version 15

# How to upgrade to version 15

Last updated  July 10, 2025

## Upgrading from 14 to 15

To update to Next.js version 15, you can use the `upgrade` codemod:

 Terminal

```
npx @next/codemod@canary upgrade latest
```

If you prefer to do it manually, ensure that you're installing the latest Next & React versions:

 Terminal

```
npm i next@latest react@latest react-dom@latest eslint-config-next@latest
```

> **Good to know:**
>
>
>
> - If you see a peer dependencies warning, you may need to update `react` and `react-dom` to the suggested versions, or use the `--force` or `--legacy-peer-deps` flag to ignore the warning. This won't be necessary once both Next.js 15 and React 19 are stable.

## React 19

- The minimum versions of `react` and `react-dom` is now 19.
- `useFormState` has been replaced by `useActionState`. The `useFormState` hook is still available in React 19, but it is deprecated and will be removed in a future release. `useActionState` is recommended and includes additional properties like reading the `pending` state directly. [Learn more](https://react.dev/reference/react/useActionState).
- `useFormStatus` now includes additional keys like `data`, `method`, and `action`. If you are not using React 19, only the `pending` key is available. [Learn more](https://react.dev/reference/react-dom/hooks/useFormStatus).
- Read more in the [React 19 upgrade guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide).

> **Good to know:** If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their latest versions.

## Async Request APIs (Breaking change)

Previously synchronous Dynamic APIs that rely on runtime information are now **asynchronous**:

- [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies)
- [headers](https://nextjs.org/docs/app/api-reference/functions/headers)
- [draftMode](https://nextjs.org/docs/app/api-reference/functions/draft-mode)
- `params` in [layout.js](https://nextjs.org/docs/app/api-reference/file-conventions/layout), [page.js](https://nextjs.org/docs/app/api-reference/file-conventions/page), [route.js](https://nextjs.org/docs/app/api-reference/file-conventions/route), [default.js](https://nextjs.org/docs/app/api-reference/file-conventions/default), [opengraph-image](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image), [twitter-image](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image), [icon](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons), and [apple-icon](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons).
- `searchParams` in [page.js](https://nextjs.org/docs/app/api-reference/file-conventions/page)

To ease the burden of migration, a [codemod is available](https://nextjs.org/docs/app/guides/upgrading/codemods#150) to automate the process and the APIs can temporarily be accessed synchronously.

### cookies

#### Recommended Async Usage

```
import { cookies } from 'next/headers'

// Before
const cookieStore = cookies()
const token = cookieStore.get('token')

// After
const cookieStore = await cookies()
const token = cookieStore.get('token')
```

#### Temporary Synchronous Usage

 app/page.tsxJavaScriptTypeScript

```
import { cookies, type UnsafeUnwrappedCookies } from 'next/headers'

// Before
const cookieStore = cookies()
const token = cookieStore.get('token')

// After
const cookieStore = cookies() as unknown as UnsafeUnwrappedCookies
// will log a warning in dev
const token = cookieStore.get('token')
```

### headers

#### Recommended Async Usage

```
import { headers } from 'next/headers'

// Before
const headersList = headers()
const userAgent = headersList.get('user-agent')

// After
const headersList = await headers()
const userAgent = headersList.get('user-agent')
```

#### Temporary Synchronous Usage

 app/page.tsxJavaScriptTypeScript

```
import { headers, type UnsafeUnwrappedHeaders } from 'next/headers'

// Before
const headersList = headers()
const userAgent = headersList.get('user-agent')

// After
const headersList = headers() as unknown as UnsafeUnwrappedHeaders
// will log a warning in dev
const userAgent = headersList.get('user-agent')
```

### draftMode

#### Recommended Async Usage

```
import { draftMode } from 'next/headers'

// Before
const { isEnabled } = draftMode()

// After
const { isEnabled } = await draftMode()
```

#### Temporary Synchronous Usage

 app/page.tsxJavaScriptTypeScript

```
import { draftMode, type UnsafeUnwrappedDraftMode } from 'next/headers'

// Before
const { isEnabled } = draftMode()

// After
// will log a warning in dev
const { isEnabled } = draftMode() as unknown as UnsafeUnwrappedDraftMode
```

### params&searchParams

#### Asynchronous Layout

 app/layout.tsxJavaScriptTypeScript

```
// Before
type Params = { slug: string }

export function generateMetadata({ params }: { params: Params }) {
  const { slug } = params
}

export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Params
}) {
  const { slug } = params
}

// After
type Params = Promise<{ slug: string }>

export async function generateMetadata({ params }: { params: Params }) {
  const { slug } = await params
}

export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Params
}) {
  const { slug } = await params
}
```

#### Synchronous Layout

 app/layout.tsxJavaScriptTypeScript

```
// Before
type Params = { slug: string }

export default function Layout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Params
}) {
  const { slug } = params
}

// After
import { use } from 'react'

type Params = Promise<{ slug: string }>

export default function Layout(props: {
  children: React.ReactNode
  params: Params
}) {
  const params = use(props.params)
  const slug = params.slug
}
```

#### Asynchronous Page

 app/page.tsxJavaScriptTypeScript

```
// Before
type Params = { slug: string }
type SearchParams = { [key: string]: string | string[] | undefined }

export function generateMetadata({
  params,
  searchParams,
}: {
  params: Params
  searchParams: SearchParams
}) {
  const { slug } = params
  const { query } = searchParams
}

export default async function Page({
  params,
  searchParams,
}: {
  params: Params
  searchParams: SearchParams
}) {
  const { slug } = params
  const { query } = searchParams
}

// After
type Params = Promise<{ slug: string }>
type SearchParams = Promise<{ [key: string]: string | string[] | undefined }>

export async function generateMetadata(props: {
  params: Params
  searchParams: SearchParams
}) {
  const params = await props.params
  const searchParams = await props.searchParams
  const slug = params.slug
  const query = searchParams.query
}

export default async function Page(props: {
  params: Params
  searchParams: SearchParams
}) {
  const params = await props.params
  const searchParams = await props.searchParams
  const slug = params.slug
  const query = searchParams.query
}
```

#### Synchronous Page

```
'use client'

// Before
type Params = { slug: string }
type SearchParams = { [key: string]: string | string[] | undefined }

export default function Page({
  params,
  searchParams,
}: {
  params: Params
  searchParams: SearchParams
}) {
  const { slug } = params
  const { query } = searchParams
}

// After
import { use } from 'react'

type Params = Promise<{ slug: string }>
type SearchParams = Promise<{ [key: string]: string | string[] | undefined }>

export default function Page(props: {
  params: Params
  searchParams: SearchParams
}) {
  const params = use(props.params)
  const searchParams = use(props.searchParams)
  const slug = params.slug
  const query = searchParams.query
}
```

```
// Before
export default function Page({ params, searchParams }) {
  const { slug } = params
  const { query } = searchParams
}

// After
import { use } from "react"

export default function Page(props) {
  const params = use(props.params)
  const searchParams = use(props.searchParams)
  const slug = params.slug
  const query = searchParams.query
}
```

#### Route Handlers

 app/api/route.tsJavaScriptTypeScript

```
// Before
type Params = { slug: string }

export async function GET(request: Request, segmentData: { params: Params }) {
  const params = segmentData.params
  const slug = params.slug
}

// After
type Params = Promise<{ slug: string }>

export async function GET(request: Request, segmentData: { params: Params }) {
  const params = await segmentData.params
  const slug = params.slug
}
```

## runtimeconfiguration (Breaking change)

The `runtime` [segment configuration](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#runtime) previously supported a value of `experimental-edge` in addition to `edge`. Both configurations refer to the same thing, and to simplify the options, we will now error if `experimental-edge` is used. To fix this, update your `runtime` configuration to `edge`. A [codemod](https://nextjs.org/docs/app/guides/upgrading/codemods#app-dir-runtime-config-experimental-edge) is available to automatically do this.

## fetchrequests

[fetchrequests](https://nextjs.org/docs/app/api-reference/functions/fetch) are no longer cached by default.

To opt specific `fetch` requests into caching, you can pass the `cache: 'force-cache'` option.

 app/layout.js

```
export default async function RootLayout() {
  const a = await fetch('https://...') // Not Cached
  const b = await fetch('https://...', { cache: 'force-cache' }) // Cached

  // ...
}
```

To opt all `fetch` requests in a layout or page into caching, you can use the `export const fetchCache = 'default-cache'` [segment config option](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config). If individual `fetch` requests specify a `cache` option, that will be used instead.

 app/layout.js

```
// Since this is the root layout, all fetch requests in the app
// that don't set their own cache option will be cached.
export const fetchCache = 'default-cache'

export default async function RootLayout() {
  const a = await fetch('https://...') // Cached
  const b = await fetch('https://...', { cache: 'no-store' }) // Not cached

  // ...
}
```

## Route Handlers

`GET` functions in [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) are no longer cached by default. To opt `GET` methods into caching, you can use a [route config option](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config) such as `export const dynamic = 'force-static'` in your Route Handler file.

 app/api/route.js

```
export const dynamic = 'force-static'

export async function GET() {}
```

## Client-side Router Cache

When navigating between pages via `<Link>` or `useRouter`, [page](https://nextjs.org/docs/app/api-reference/file-conventions/page) segments are no longer reused from the client-side router cache. However, they are still reused during browser backward and forward navigation and for shared layouts.

To opt page segments into caching, you can use the [staleTimes](https://nextjs.org/docs/app/api-reference/config/next-config-js/staleTimes) config option:

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    staleTimes: {
      dynamic: 30,
      static: 180,
    },
  },
}

module.exports = nextConfig
```

[Layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout) and [loading states](https://nextjs.org/docs/app/api-reference/file-conventions/loading) are still cached and reused on navigation.

## next/font

The `@next/font` package has been removed in favor of the built-in [next/font](https://nextjs.org/docs/app/api-reference/components/font). A [codemod is available](https://nextjs.org/docs/app/guides/upgrading/codemods#built-in-next-font) to safely and automatically rename your imports.

 app/layout.js

```
// Before
import { Inter } from '@next/font/google'

// After
import { Inter } from 'next/font/google'
```

## bundlePagesRouterDependencies

`experimental.bundlePagesExternals` is now stable and renamed to `bundlePagesRouterDependencies`.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Before
  experimental: {
    bundlePagesExternals: true,
  },

  // After
  bundlePagesRouterDependencies: true,
}

module.exports = nextConfig
```

## serverExternalPackages

`experimental.serverComponentsExternalPackages` is now stable and renamed to `serverExternalPackages`.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Before
  experimental: {
    serverComponentsExternalPackages: ['package-name'],
  },

  // After
  serverExternalPackages: ['package-name'],
}

module.exports = nextConfig
```

## Speed Insights

Auto instrumentation for Speed Insights was removed in Next.js 15.

To continue using Speed Insights, follow the [Vercel Speed Insights Quickstart](https://vercel.com/docs/speed-insights/quickstart) guide.

## NextRequestGeolocation

The `geo` and `ip` properties on `NextRequest` have been removed as these values are provided by your hosting provider. A [codemod](https://nextjs.org/docs/app/guides/upgrading/codemods#150) is available to automate this migration.

If you are using Vercel, you can alternatively use the `geolocation` and `ipAddress` functions from [@vercel/functions](https://vercel.com/docs/functions/vercel-functions-package) instead:

 middleware.ts

```
import { geolocation } from '@vercel/functions'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { city } = geolocation(request)

  // ...
}
```

 middleware.ts

```
import { ipAddress } from '@vercel/functions'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const ip = ipAddress(request)

  // ...
}
```

Was this helpful?

supported.

---

# How to upgrade to version 16

> Upgrade your Next.js Application from Version 15 to 16.

[Guides](https://nextjs.org/docs/app/guides)[Upgrading](https://nextjs.org/docs/app/guides/upgrading)Version 16

# How to upgrade to version 16

Last updated  January 16, 2026

## Upgrading from 15 to 16

### Using AI Agents with Next.js DevTools MCP

If you're using an AI coding assistant that supports the [Model Context Protocol (MCP)](https://modelcontextprotocol.io), you can use the **Next.js DevTools MCP** to automate the upgrade process and migration tasks.

#### Setup

Add the following configuration to your MCP client, for each coding agent you can read [this section](https://github.com/vercel/next-devtools-mcp#mcp-client-configuration) for configuration details.

**example:**

 .mcp.json

```
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

For more information, visit the [next-devtools-mcp](https://github.com/vercel/next-devtools-mcp) documentation to configure with your MCP client.

> **Note:** Using `next-devtools-mcp@latest` ensures that your MCP client will always use the latest version of the Next.js DevTools MCP server.

#### Example Prompts

Once configured, you can use natural language prompts to upgrade your Next.js app:

**To upgrade to Next.js 16:**

Connect to your coding agent and then prompt:

```
Next Devtools, help me upgrade my Next.js app to version 16
```

**To migrate to Cache Components (after upgrading to v16):**

Connect to your coding agent and then prompt:

```
Next Devtools, migrate my Next.js app to cache components
```

Learn more in the documentation [here](https://nextjs.org/docs/app/guides/mcp).

### Using the Codemod

To update to Next.js version 16, you can use the `upgrade` [codemod](https://nextjs.org/docs/app/guides/upgrading/codemods#160):

 Terminal

```
npx @next/codemod@canary upgrade latest
```

The [codemod](https://nextjs.org/docs/app/guides/upgrading/codemods#160) is able to:

- Update `next.config.js` to use the new `turbopack` configuration
- Migrate from `next lint` to the ESLint CLI
- Migrate from deprecated `middleware` convention to `proxy`
- Remove `unstable_` prefix from stabilized APIs
- Remove `experimental_ppr` Route Segment Config from pages and layouts

If you prefer to do it manually, install the latest Next.js and React versions:

 Terminal

```
npm install next@latest react@latest react-dom@latest
```

If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their latest versions.

## Node.js runtime and browser support

| Requirement | Change / Details |
| --- | --- |
| Node.js 20.9+ | Minimum version now20.9.0(LTS); Node.js 18 no longer supported |
| TypeScript 5+ | Minimum version now5.1.0 |
| Browsers | Chrome 111+, Edge 111+, Firefox 111+, Safari 16.4+ |

## Turbopack by default

Starting with **Next.js 16**, Turbopack is stable and used by default with `next dev` and `next build`

Previously you had to enable Turbopack using `--turbopack`, or `--turbo`.

 package.json

```
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build --turbopack",
    "start": "next start"
  }
}
```

This is no longer necessary. You can update your `package.json` scripts:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

If your project has a [customwebpack](https://nextjs.org/docs/app/api-reference/config/next-config-js/webpack) configuration and you run `next build` (which now uses Turbopack by default), the build will **fail** to prevent misconfiguration issues.

You have a few different ways to address this:

- **Use Turbopack anyway:** Run with `next build --turbopack` to build using Turbopack and ignore your `webpack` config.
- **Switch to Turbopack fully:** Migrate your `webpack` config to Turbopack-compatible options.
- **Keep using Webpack:** Use the `--webpack` flag to opt out of Turbopack and build with Webpack.

> **Good to know**: If you see failing builds because a `webpack` configuration was found, but you don't define one yourself, it is likely that a plugin is adding a `webpack` option

### Opting out of Turbopack

If you need to continue using Webpack, you can opt out with the `--webpack` flag. For example, to use Turbopack in development but Webpack for production builds:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build --webpack",
    "start": "next start"
  }
}
```

We recommend using Turbopack for development and production. Submit a comment to this [thread](https://github.com/vercel/next.js/discussions/77721), if you are unable to switch to Turbopack.

### Turbopack configuration location

The `experimental.turbopack` configuration is out of experimental.

 next.config.ts

```
import type { NextConfig } from 'next'

// Next.js 15 - experimental.turbopack
const nextConfig: NextConfig = {
  experimental: {
    turbopack: {
      // options
    },
  },
}

export default nextConfig
```

You can use it as a top-level `turbopack` option:

 next.config.ts

```
import type { NextConfig } from 'next'

// Next.js 16 - turbopack at the top level of nextConfig
const nextConfig: NextConfig = {
  turbopack: {
    // options
  },
}

export default nextConfig
```

Make sure to review the `Turbopack` configuration [options](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack). **Next.js 16** introduces various improvements and new options, for example:

- [Advanced Webpack loader conditions](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#advanced-webpack-loader-conditions)
- [debugIds](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#debug-ids)

### Resolve alias fallback

In some projects, client-side code may import files containing Node.js native modules. This will cause `Module not found: Can't resolve 'fs'` type of errors.

When this happens, you should refactor your code so that your client-side bundles do not reference these Node.js native modules.

However, in some cases, this might not be possible. In Webpack the `resolve.fallback` option was typically used to **silence** the error. Turbopack offers a similar option, using `turbopack.resolveAlias`. In this case, tell Turbopack to load an empty module when `fs` is requested for the browser.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  turbopack: {
    resolveAlias: {
      fs: {
        browser: './empty.ts', // We recommend to fix code imports before using this method
      },
    },
  },
}

export default nextConfig
```

It is preferable to refactor your modules so that client code doesn't ever import from modules using Node.js native modules.

### Sass node_modules imports

Turbopack fully supports importing Sass files from `node_modules`. Note that while Webpack allowed the legacy tilde (`~`) prefix, Turbopack does not support this syntax.

In Webpack:

 styles/globals.scss

```
@import '~bootstrap/dist/css/bootstrap.min.css';
```

In Turbopack:

 styles/globals.scss

```
@import 'bootstrap/dist/css/bootstrap.min.css';
```

If changing the imports is not possible, you can use `turbopack.resolveAlias`. For example:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  turbopack: {
    resolveAlias: {
      '~*': '*',
    },
  },
}

export default nextConfig
```

### Turbopack File System Caching (beta)

Turbopack now supports filesystem caching in development, storing compiler artifacts on disk between runs for significantly faster compile times across restarts.

Enable filesystem caching in your configuration:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    turbopackFileSystemCacheForDev: true,
  },
}

export default nextConfig
```

## Async Request APIs (Breaking change)

Version 15 introduced [Async Request APIs](https://nextjs.org/docs/app/guides/upgrading/version-15#async-request-apis-breaking-change) as a breaking change, with **temporary** synchronous compatibility.

Starting with **Next.js 16**, synchronous access is fully removed. These APIs can only be accessed asynchronously.

- [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies)
- [headers](https://nextjs.org/docs/app/api-reference/functions/headers)
- [draftMode](https://nextjs.org/docs/app/api-reference/functions/draft-mode)
- `params` in [layout.js](https://nextjs.org/docs/app/api-reference/file-conventions/layout), [page.js](https://nextjs.org/docs/app/api-reference/file-conventions/page), [route.js](https://nextjs.org/docs/app/api-reference/file-conventions/route), [default.js](https://nextjs.org/docs/app/api-reference/file-conventions/default), [opengraph-image](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image#opengraph-image), [twitter-image](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image#twitter-image), [icon](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons#icon), and [apple-icon](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons#apple-icon).
- `searchParams` in [page.js](https://nextjs.org/docs/app/api-reference/file-conventions/page)

Use the [codemod](https://nextjs.org/docs/app/guides/upgrading/codemods#migrate-to-async-dynamic-apis) to migrate to async Dynamic APIs.

### Migrating types for async Dynamic APIs

To help migrate to async `params` and `searchParams`, you can run [npx next typegen](https://nextjs.org/docs/app/api-reference/cli/next#next-typegen-options) to automatically generate these globally available types helpers:

- [PageProps](https://nextjs.org/docs/app/api-reference/file-conventions/page#page-props-helper)
- [LayoutProps](https://nextjs.org/docs/app/api-reference/file-conventions/layout#layout-props-helper)
- [RouteContext](https://nextjs.org/docs/app/api-reference/file-conventions/route#route-context-helper)

> **Good to know**: `typegen` was introduced in Next.js 15.5

This simplifies type-safe migration to the new async API pattern, and enables you to update your components with full type safety, for example:

 /app/blog/[slug]/page.tsx

```
export default async function Page(props: PageProps<'/blog/[slug]'>) {
  const { slug } = await props.params
  const query = await props.searchParams
  return <h1>Blog Post: {slug}</h1>
}
```

This approach gives you fully type-safe access to `props.params`, including the `slug`, and to `searchParams`, directly within your page.

## Async parameters for icon, and open-graph Image (Breaking change)

> The props passed to the image generating functions in `opengraph-image`, `twitter-image`, `icon`, and `apple-icon`, are now Promises.

In previous versions, both the `Image` (image generation function), and the `generateImageMetadata` received a `params` object. The `id` returned by `generateImageMetadata` was passed as a string to the image generation function.

 app/shop/[slug]/opengraph-image.js

```
// Next.js 15 - synchronous params access
export function generateImageMetadata({ params }) {
  const { slug } = params
  return [{ id: '1' }, { id: '2' }]
}

// Next.js 15 - synchronous params and id access
export default function Image({ params, id }) {
  const slug = params.slug
  const imageId = id // string
  // ...
}
```

Starting with **Next.js 16**, to align with the [Async Request APIs](#async-request-apis-breaking-change) change, the image generating function now receives `params` and `id` as promises. The `generateImageMetadata` function continues to receive synchronous `params`.

 app/shop/[slug]/opengraph-image.js

```
export async function generateImageMetadata({ params }) {
  const { slug } = params
  return [{ id: '1' }, { id: '2' }]
}

// Next.js 16 - asynchronous params and id access
export default async function Image({ params, id }) {
  const { slug } = await params // params now async
  const imageId = await id // id is now Promise<string> when using generateImageMetadata
  // ...
}
```

## Asyncidparameter forsitemap(Breaking change)

Previously, the `id` values returned from [generateSitemaps](https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps) were passed directly to the `sitemap` generating function.

 app/product/sitemap.js

```
export async function generateSitemaps() {
  return [{ id: 0 }, { id: 1 }, { id: 2 }, { id: 3 }]
}

// Next.js 15 - synchronous id access
export default async function sitemap({ id }) {
  const start = id * 50000 // id is a number
  // ...
}
```

Starting with **Next.js 16**, the `sitemap` generating function now receives `id` as a promise.

 app/product/sitemap.js

```
export async function generateSitemaps() {
  return [{ id: 0 }, { id: 1 }, { id: 2 }, { id: 3 }]
}

// Next.js 16 - asynchronous id access
export default async function sitemap({ id }) {
  const resolvedId = await id // id is now Promise<string>
  const start = Number(resolvedId) * 50000
  // ...
}
```

## React 19.2

The App Router in **Next.js 16** uses the latest React [Canary release](https://react.dev/blog/2023/05/03/react-canaries), which includes the newly released React 19.2 features and other features being incrementally stabilized. Highlights include:

- **View Transitions**: Animate elements that update inside a Transition or navigation
- **useEffectEvent**: Extract non-reactive logic from Effects into reusable Effect Event functions
- **Activity**: Render "background activity" by hiding UI with `display: none` while maintaining state and cleaning up Effects

Learn more in the [React 19.2 announcement](https://react.dev/blog/2025/10/01/react-19-2).

## React Compiler Support

Built-in support for the React Compiler is now stable in **Next.js 16** following the React Compiler's 1.0 release. The React Compiler automatically memoizes components, reducing unnecessary re-renders with zero manual code changes.

The `reactCompiler` configuration option has been promoted from `experimental` to stable. It is not enabled by default as we continue gathering build performance data across different application types.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactCompiler: true,
}

export default nextConfig
```

Install the latest version of the React Compiler plugin:

 Terminal

```
npm install -D babel-plugin-react-compiler
```

> **Good to know:** Expect compile times in development and during builds to be higher when enabling this option as the React Compiler relies on Babel.

## Caching APIs

### revalidateTag

[revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) has a new function signature. You can pass a [cacheLife](https://nextjs.org/docs/app/api-reference/functions/cacheLife#reference) profile as the second argument.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { revalidateTag } from 'next/cache'

export async function updateArticle(articleId: string) {
  // Mark article data as stale - article readers see stale data while it revalidates
  revalidateTag(`article-${articleId}`, 'max')
}
```

Use `revalidateTag` for content where a slight delay in updates is acceptable, such as blog posts, product catalogs, or documentation. Users receive stale content while fresh data loads in the background.

### updateTag

[updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag) is a new [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data#what-are-server-functions)-only API that provides **read-your-writes** semantics, where a user makes a change and the UI immediately shows the change, rather than stale data.

It does this by expiring and immediately refreshing data within the same request.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { updateTag } from 'next/cache'

export async function updateUserProfile(userId: string, profile: Profile) {
  await db.users.update(userId, profile)

  // Expire cache and refresh immediately - user sees their changes right away
  updateTag(`user-${userId}`)
}
```

This ensures interactive features reflect changes immediately. Perfect for forms, user settings, and any workflow where users expect to see their updates instantly.

Learn more about when to use `updateTag` or `revalidateTag` [here](https://nextjs.org/docs/app/api-reference/functions/updateTag#when-to-use-updatetag).

### refresh

[refresh](https://nextjs.org/docs/app/api-reference/functions/refresh) allows you to refresh the client router from within a Server Action.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { refresh } from 'next/cache'

export async function markNotificationAsRead(notificationId: string) {
  // Update the notification in the database
  await db.notifications.markAsRead(notificationId)

  // Refresh the notification count displayed in the header
  refresh()
}
```

Use it when you need to refresh the client router after performing an action.

### cacheLife and cacheTag

[cacheLife](https://nextjs.org/docs/app/api-reference/functions/cacheLife) and [cacheTag](https://nextjs.org/docs/app/api-reference/functions/cacheTag) are now stable. The `unstable_` prefix is no longer needed.

Wherever you had aliased imports like:

```
import {
  unstable_cacheLife as cacheLife,
  unstable_cacheTag as cacheTag,
} from 'next/cache'
```

You can update your imports to:

```
import { cacheLife, cacheTag } from 'next/cache'
```

## Enhanced Routing and Navigation

**Next.js 16** includes a complete overhaul of the routing and navigation system, making page transitions leaner and faster. This optimizes how Next.js prefetches and caches navigation data:

- **Layout deduplication**: When prefetching multiple URLs with a shared layout, the layout is downloaded once.
- **Incremental prefetching**: Next.js only prefetches parts not already in cache, rather than entire pages.

These changes require **no code modifications** and are designed to improve performance across all apps.

However, you may see more individual prefetch requests with much lower total transfer sizes. We believe this is the right trade-off for nearly all applications.

If the increased request count causes issues, please let us know by creating an [issue](https://github.com/vercel/next.js/issues) or [discussion](https://github.com/vercel/next.js/discussions) item.

## Partial Pre-Rendering (PPR)

**Next.js 16** removes the experimental **Partial Pre-Rendering (PPR)** flag and configuration options, including the route level segment `experimental_ppr`.

Starting with **Next.js 16**, you can opt into PPR using the [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) configuration.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  cacheComponents: true,
}

module.exports = nextConfig
```

PPR in **Next.js 16** works differently than in **Next.js 15** canaries. If you are using PPR today, stay in the current Next.js 15 canary you are using. We will follow up with a guide to migrate to Cache Components.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  // If you are using PPR today
  // stay in the current Next.js 15 canary
  experimental: {
    ppr: true,
  },
}

module.exports = nextConfig
```

## middlewaretoproxy

The `middleware` filename is deprecated, and has been renamed to `proxy` to clarify network boundary and routing focus.

The `edge` runtime is **NOT** supported in `proxy`. The `proxy` runtime is `nodejs`, and it cannot be configured. If you want to continue using the `edge` runtime, keep using `middleware`. We will follow up on a minor release with further `edge` runtime instructions.

 Terminal

```
# Rename your middleware file
mv middleware.ts proxy.ts
# or
mv middleware.js proxy.js
```

The named export `middleware` is also deprecated. Rename your function to `proxy`.

 proxy.tsJavaScriptTypeScript

```
export function proxy(request: Request) {}
```

We recommend changing the function name to `proxy`, even if you are using a default export.

Configuration flags that contained the `middleware` name are also renamed. For example, `skipMiddlewareUrlNormalize` is now `skipProxyUrlNormalize`

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  skipProxyUrlNormalize: true,
}

export default nextConfig
```

The version 16 [codemod](https://nextjs.org/docs/app/guides/upgrading/codemods#160) is able to update these flags too.

## next/imagechanges

### Local Images with Query Strings (Breaking change)

Local image sources with query strings now require `images.localPatterns.search` configuration to prevent enumeration attacks.

 app/page.tsx

```
import Image from 'next/image'

export default function Page() {
  return <Image src="/assets/photo?v=1" alt="Photo" width="100" height="100" />
}
```

If you need to use query strings with local images, add the pattern to your configuration:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    localPatterns: [
      {
        pathname: '/assets/**',
        search: '?v=1',
      },
    ],
  },
}

export default nextConfig
```

### minimumCacheTTLDefault (Breaking change)

The default value for `images.minimumCacheTTL` has changed from `60 seconds` to `4 hours` (14400 seconds). This reduces revalidation cost for images without cache-control headers.

For some Next.js users, image revalidation was happening frequently, often because the upstream source images missed a `cache-control` header. This caused revalidation to happen every `60` seconds, which increased CPU usage and cost.

Since most images do not change often, this short interval is not ideal. Setting the default to 4 hours offers a more durable cache by default, while still allowing images to update a few times per day if needed.

If you need the previous behavior, change `minimumCacheTTL` to a lower value, for example back to `60` seconds:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    minimumCacheTTL: 60,
  },
}

export default nextConfig
```

### imageSizesDefault (Breaking change)

The value `16` has been removed from the default `images.imageSizes` array.

We have looked at request analytics and found out that very few projects ever serve 16 pixels width images. Removing this setting reduces the size of the `srcset` attribute shipped to the browser by `next/image`.

If you need to support 16px images:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
}

export default nextConfig
```

Rather than lack of developer usage, we believe 16 pixels width images have become less common, because `devicePixelRatio: 2` actually fetches a 32px image to prevent blurriness in retina displays.

### qualitiesDefault (Breaking change)

The default value for `images.qualities` has changed from allowing all qualities to only `[75]`.

If you need to support multiple quality levels:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    qualities: [50, 75, 100],
  },
}

export default nextConfig
```

If you specify a `quality` prop not included in the `image.qualities` array, the quality will be coerced to the closest value in `images.qualities`. For example, given the configuration above, a `quality` prop of 80, is coerced to 75.

### Local IP Restriction (Breaking change)

A new security restriction blocks local IP optimization by default. Set `images.dangerouslyAllowLocalIP` to `true` only for private networks.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    dangerouslyAllowLocalIP: true, // Only for private networks
  },
}

export default nextConfig
```

### Maximum Redirects (Breaking change)

The default for `images.maximumRedirects` has changed from unlimited to 3 redirects maximum.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    maximumRedirects: 0, // Disable redirects
    // or
    maximumRedirects: 5, // Increase for edge cases
  },
}

export default nextConfig
```

### next/legacy/imageComponent (deprecated)

The `next/legacy/image` component is deprecated. Use `next/image` instead:

```
// Before
import Image from 'next/legacy/image'

// After
import Image from 'next/image'
```

### images.domainsConfiguration (deprecated)

The `images.domains` config is deprecated.

 next.config.js

```
// image.domains is deprecated
module.exports = {
  images: {
    domains: ['example.com'],
  },
}
```

Use `images.remotePatterns` instead for improved security:

 next.config.js

```
// Use image.remotePatterns instead
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
      },
    ],
  },
}
```

## Concurrentdevandbuild

`next dev` and `next build` now use separate output directories, enabling concurrent execution. The `next dev` command outputs to `.next/dev`. This is the new default behavior, controlled by [isolatedDevBuild](https://nextjs.org/docs/app/api-reference/config/next-config-js/isolatedDevBuild).

Additionally, a lockfile mechanism prevents multiple `next dev` or `next build` instances on the same project.

Since the development server outputs to `.next/dev`, the [Turbopack tracing command](https://nextjs.org/docs/app/guides/local-development#turbopack-tracing) should be:

```
npx next internal trace .next/dev/trace-turbopack
```

## Parallel Routesdefault.jsrequirement

All [parallel route](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes) slots now require explicit `default.js` files. Builds will fail without them.

To maintain previous behavior, create a [default.js](https://nextjs.org/docs/app/api-reference/file-conventions/default) file that calls `notFound()` or returns `null`.

 app/@modal/default.tsx

```
import { notFound } from 'next/navigation'

export default function Default() {
  notFound()
}
```

Or return `null`:

 app/@modal/default.tsx

```
export default function Default() {
  return null
}
```

## ESLint Flat Config

`@next/eslint-plugin-next` now defaults to ESLint Flat Config format, aligning with ESLint v10 which will drop legacy config support.

Make sure to review our API reference for the [@next/eslint-plugin-next](https://nextjs.org/docs/app/api-reference/config/eslint#setup-eslint) plugin.

If you're using the legacy `.eslintrc` format, consider migrating to the flat config format. See the [ESLint migration guide](https://eslint.org/docs/latest/use/configure/migration-guide) for details.

## Scroll Behavior Override

In **previous versions of Next.js**, if you had set `scroll-behavior: smooth` globally on your `<html>` element via CSS, Next.js would override this during SPA route transitions, as follows:

1. Temporarily set `scroll-behavior` to `auto`
2. Perform the navigation (causing instant scroll to top)
3. Restore your original `scroll-behavior` value

This ensured that page navigation always felt snappy and instant, even when you had smooth scrolling enabled for in-page navigation. However, this manipulation could be expensive, especially at the start of every navigation.

In **Next.js 16**, this behavior has changed. By default, Next.js will **no longer override** your `scroll-behavior` setting during navigation.

**If you want Next.js to perform this override** (the previous default behavior), add the `data-scroll-behavior="smooth"` attribute to your `<html>` element:

 app/layout.tsx

```
export default function RootLayout({ children }) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body>{children}</body>
    </html>
  )
}
```

## Performance Improvements

Significant performance optimizations for `next dev` and `next start` commands, along with improved terminal output with clearer formatting, better error messages, and improved performance metrics.

**Next.js 16** removes the `size` and `First Load JS` metrics from the `next build` output. We found these to be inaccurate in server-driven architectures using React Server Components. Both our Turbopack and Webpack implementations had issues, and disagreed on how to account for Client Components payload.

The most effective way to measure actual route performance is through tools such as [Chrome Lighthouse](https://developer.chrome.com/docs/lighthouse/overview) or Vercel Analytics, which focus on Core Web Vitals and downloaded resource sizes.

### next devconfig load

In previous versions the Next config file was loaded twice during development:

- When running the `next dev` command
- When the `next dev` command started the Next.js server

This was inefficient because the `next dev` command doesn't need the config file to start the Next.js server.

A consequence of this change is that, when running `next dev` checking if `process.argv` includes `'dev'`, in your Next.js config file, will return `false`.

> **Good to know**: The `typegen`, and `build` commands, are still visible in `process.argv`.

This is specially important for plugins that trigger side-effects on `next dev`. If that's the case, it might be enough to check if `NODE_ENV` is set to `development`.

 next.config.js

```
import { startServer } from 'docs-lib/dev-server'

const isDev = process.env.NODE_ENV === 'development'

if (isDev) {
  startServer()
}

const nextConfig = {
  /* Your config options */
}

module.exports = nextConfig
```

Alternatively, use the [phase](https://nextjs.org/docs/app/api-reference/config/next-config-js#phase) in which the configuration is loaded.

## Build Adapters API (alpha)

Following the [Build Adapters RFC](https://github.com/vercel/next.js/discussions/77740), the first alpha version of the Build Adapters API is now available.

Build Adapters allow you to create custom adapters that hook into the build process, enabling deployment platforms and custom build integrations to modify Next.js configuration or process build output.

 next.config.js

```
const nextConfig = {
  experimental: {
    adapterPath: require.resolve('./my-adapter.js'),
  },
}

module.exports = nextConfig
```

Share your feedback in the [RFC discussion](https://github.com/vercel/next.js/discussions/77740).

## Modern Sass API

`sass-loader` has been bumped to v16, which supports [modern Sass syntax](https://sass-lang.com/documentation/js-api/#md:usage) and new features.

## Removals

These features were previously deprecated and are now removed:

### AMP Support

AMP adoption has declined significantly, and maintaining this feature adds complexity to the framework. All AMP APIs and configurations have been removed:

- `amp` configuration from your Next config file
- `next/amp` hook imports and usage (`useAmp`)

```
// Removed
import { useAmp } from 'next/amp'

// Removed
export const config = { amp: true }
```

- `export const config = { amp: true }` from pages

 next.config.js

```
const nextConfig = {
  // Removed
  amp: {
    canonicalBase: 'https://example.com',
  },
}

export default nextConfig
```

Evaluate if AMP is still necessary for your use case. Most performance benefits can now be achieved through Next.js's built-in optimizations and modern web standards.

### next lintCommand

The `next lint` command has been removed. Use Biome or ESLint directly. `next build` no longer runs linting.

A codemod is available to automate migration:

 Terminal

```
npx @next/codemod@canary next-lint-to-eslint-cli .
```

The `eslint` option in the Next.js config file is also removed.

 next.config.mjs

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  // No longer supported
  // eslint: {},
}

export default nextConfig
```

### Runtime Configuration

`serverRuntimeConfig` and `publicRuntimeConfig` have been removed. Use environment variables instead.

**Before (Next.js 15):**

 next.config.js

```
module.exports = {
  serverRuntimeConfig: {
    dbUrl: process.env.DATABASE_URL,
  },
  publicRuntimeConfig: {
    apiUrl: '/api',
  },
}
```

 pages/index.tsx

```
import getConfig from 'next/config'

export default function Page() {
  const { publicRuntimeConfig } = getConfig()
  return <p>API URL: {publicRuntimeConfig.apiUrl}</p>
}
```

**After (Next.js 16):**

For server-only values, access environment variables directly in Server Components:

 app/page.tsx

```
async function fetchData() {
  const dbUrl = process.env.DATABASE_URL
  // Use for server-side operations only
  return await db.query(dbUrl, 'SELECT * FROM users')
}

export default async function Page() {
  const data = await fetchData()
  return <div>{/* render data */}</div>
}
```

> **Good to know**: Use the [taint API](https://nextjs.org/docs/app/api-reference/config/next-config-js/taint) to prevent accidentally passing sensitive server values to Client Components.

For client-accessible values, use the `NEXT_PUBLIC_` prefix:

 .env.local

```
NEXT_PUBLIC_API_URL="/api"
```

 app/components/client-component.tsx

```
'use client'

export default function ClientComponent() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL
  return <p>API URL: {apiUrl}</p>
}
```

To ensure environment variables are read at runtime (not bundled at build time), use the [connection()](https://nextjs.org/docs/app/api-reference/functions/connection) function before reading from `process.env`:

 app/page.tsx

```
import { connection } from 'next/server'

export default async function Page() {
  await connection()
  const config = process.env.RUNTIME_CONFIG
  return <p>{config}</p>
}
```

Learn more about [environment variables](https://nextjs.org/docs/app/guides/environment-variables).

### devIndicatorsOptions

The following options have been removed from [devIndicators](https://nextjs.org/docs/app/api-reference/config/next-config-js/devIndicators):

- `appIsrStatus`
- `buildActivity`
- `buildActivityPosition`

The indicator itself remains available.

### experimental.dynamicIO

The `experimental.dynamicIO` flag has been renamed to `cacheComponents`:

Update your Next config file, by removing the `dynamicIO` flag.

 next.config.js

```
// Next.js 15 - experimental.dynamicIO is now removed
module.exports = {
  experimental: {
    dynamicIO: true,
  },
}
```

Add the [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) flag set to true.

 next.config.js

```
// Next.js 16 - use cacheComponents instead
module.exports = {
  cacheComponents: true,
}
```

### unstable_rootParams

The `unstable_rootParams` function has been removed. We are working on an alternative API that we will ship in an upcoming minor release.

Was this helpful?

supported.

---

# Upgrade Guides

> Learn how to upgrade to the latest versions of Next.js.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Upgrading

# Upgrade Guides

Last updated  April 15, 2025

Learn how to upgrade to the latest versions of Next.js following the versions-specific guides:

[CodemodsUse codemods to upgrade your Next.js codebase when new features are released.](https://nextjs.org/docs/app/guides/upgrading/codemods)[Version 14Upgrade your Next.js Application from Version 13 to 14.](https://nextjs.org/docs/app/guides/upgrading/version-14)[Version 15Upgrade your Next.js Application from Version 14 to 15.](https://nextjs.org/docs/app/guides/upgrading/version-15)[Version 16Upgrade your Next.js Application from Version 15 to 16.](https://nextjs.org/docs/app/guides/upgrading/version-16)

Was this helpful?

supported.
