# TypeScript and more

# TypeScript

> Next.js provides a TypeScript-first development experience for building your React application.

[API Reference](https://nextjs.org/docs/app/api-reference)[Configuration](https://nextjs.org/docs/app/api-reference/config)TypeScript

# TypeScript

Last updated  December 9, 2025

Next.js comes with built-in TypeScript, automatically installing the necessary packages and configuring the proper settings when you create a new project with `create-next-app`.

To add TypeScript to an existing project, rename a file to `.ts` / `.tsx`. Run `next dev` and `next build` to automatically install the necessary dependencies and add a `tsconfig.json` file with the recommended config options.

> **Good to know**: If you already have a `jsconfig.json` file, copy the `paths` compiler option from the old `jsconfig.json` into the new `tsconfig.json` file, and delete the old `jsconfig.json` file.

## IDE Plugin

Next.js includes a custom TypeScript plugin and type checker, which VSCode and other code editors can use for advanced type-checking and auto-completion.

You can enable the plugin in VS Code by:

1. Opening the command palette (`Ctrl/⌘` + `Shift` + `P`)
2. Searching for "TypeScript: Select TypeScript Version"
3. Selecting "Use Workspace Version"

![TypeScript Command Palette](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ftypescript-command-palette.png&w=3840&q=75)![TypeScript Command Palette](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ftypescript-command-palette.png&w=3840&q=75)

Now, when editing files, the custom plugin will be enabled. When running `next build`, the custom type checker will be used.

The TypeScript plugin can help with:

- Warning if invalid values for [segment config options](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config) are passed.
- Showing available options and in-context documentation.
- Ensuring the `'use client'` directive is used correctly.
- Ensuring client hooks (like `useState`) are only used in Client Components.

> **🎥 Watch:** Learn about the built-in TypeScript plugin → [YouTube (3 minutes)](https://www.youtube.com/watch?v=pqMqn9fKEf8)

## End-to-End Type Safety

The Next.js App Router has **enhanced type safety**. This includes:

1. **No serialization of data between fetching function and page**: You can `fetch` directly in components, layouts, and pages on the server. This data *does not* need to be serialized (converted to a string) to be passed to the client side for consumption in React. Instead, since `app` uses Server Components by default, we can use values like `Date`, `Map`, `Set`, and more without any extra steps. Previously, you needed to manually type the boundary between server and client with Next.js-specific types.
2. **Streamlined data flow between components**: With the removal of `_app` in favor of root layouts, it is now easier to visualize the data flow between components and pages. Previously, data flowing between individual `pages` and `_app` were difficult to type and could introduce confusing bugs. With [colocated data fetching](https://nextjs.org/docs/app/getting-started/fetching-data) in the App Router, this is no longer an issue.

[Data Fetching in Next.js](https://nextjs.org/docs/app/getting-started/fetching-data) now provides as close to end-to-end type safety as possible without being prescriptive about your database or content provider selection.

We're able to type the response data as you would expect with normal TypeScript. For example:

app/page.tsxJavaScriptTypeScript

```
async function getData() {
  const res = await fetch('https://api.example.com/...')
  // The return value is *not* serialized
  // You can return Date, Map, Set, etc.
  return res.json()
}

export default async function Page() {
  const name = await getData()

  return '...'
}
```

For *complete* end-to-end type safety, this also requires your database or content provider to support TypeScript. This could be through using an [ORM](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) or type-safe query builder.

## Route-Aware Type Helpers

Next.js generates global helpers for App Router route types. These are available without imports and are generated during `next dev`, `next build`, or via [next typegen](https://nextjs.org/docs/app/api-reference/cli/next#next-typegen-options):

- [PageProps](https://nextjs.org/docs/app/api-reference/file-conventions/page#page-props-helper)
- [LayoutProps](https://nextjs.org/docs/app/api-reference/file-conventions/layout#layout-props-helper)
- [RouteContext](https://nextjs.org/docs/app/api-reference/file-conventions/route#route-context-helper)

## next-env.d.ts

Next.js generates a `next-env.d.ts` file in your project root. This file references Next.js type definitions, allowing TypeScript to recognize non-code imports (images, stylesheets, etc.) and Next.js-specific types.

Running `next dev`, `next build`, or [next typegen](https://nextjs.org/docs/app/api-reference/cli/next#next-typegen-options) regenerates this file.

> **Good to know**:
>
>
>
> - We recommend adding `next-env.d.ts` to your `.gitignore` file.
> - The file must be in your `tsconfig.json` `include` array (`create-next-app` does this automatically).

## Examples

### Type Checking Next.js Configuration Files

You can use TypeScript and import types in your Next.js configuration by using `next.config.ts`.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  /* config options here */
}

export default nextConfig
```

Module resolution in `next.config.ts` is currently limited to CommonJS. However, ECMAScript Modules (ESM) syntax is available when [using Node.js native TypeScript resolver](#using-nodejs-native-typescript-resolver-for-nextconfigts) for Node.js v22.10.0 and higher.

When using the `next.config.js` file, you can add some type checking in your IDE using JSDoc as below:

 next.config.js

```
// @ts-check

/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
}

module.exports = nextConfig
```

### Using Node.js Native TypeScript Resolver fornext.config.ts

> **Note**: Available on Node.js v22.10.0+ and only when the feature is enabled. Next.js does not enable it.

Next.js detects the [Node.js native TypeScript resolver](https://nodejs.org/api/typescript.html) via [process.features.typescript](https://nodejs.org/api/process.html#processfeaturestypescript), added in **v22.10.0**. When present, `next.config.ts` can use native ESM, including top‑level `await` and dynamic `import()`. This mechanism inherits the capabilities and limitations of Node's resolver.

In Node.js versions **v22.18.0+**, `process.features.typescript` is enabled by default. For versions between **v22.10.0** and **22.17.x**, opt in with `NODE_OPTIONS=--experimental-transform-types`:

 Terminal

```
NODE_OPTIONS=--experimental-transform-types next <command>
```

#### For CommonJS Projects (Default)

Although `next.config.ts` supports native ESM syntax in CommonJS projects, Node.js will still assume `next.config.ts` is a CommonJS file by default, resulting in Node.js reparsing the file as ESM when module syntax is detected. Therefore, we recommend using the `next.config.mts` file for CommonJS projects to explicitly indicate it's an ESM module:

 next.config.mts

```
import type { NextConfig } from 'next'

// Top-level await and dynamic import are supported
const flags = await import('./flags.js').then((m) => m.default ?? m)

const nextConfig: NextConfig = {
  /* config options here */
  typedRoutes: Boolean(flags?.typedRoutes),
}

export default nextConfig
```

#### For ESM Projects

When `"type"` is set to `"module"` in `package.json`, your project uses ESM. Learn more about this setting [in the Node.js docs](https://nodejs.org/api/packages.html#type). In this case, you can write `next.config.ts` directly with ESM syntax.

> **Good to know**: When using `"type": "module"` in your `package.json`, all `.js` and `.ts` files in your project are treated as ESM modules by default. You may need to rename files with CommonJS syntax to `.cjs` or `.cts` extensions if needed.

### Statically Typed Links

Next.js can statically type links to prevent typos and other errors when using `next/link`, improving type safety when navigating between pages.

Works in both the Pages and App Router for the `href` prop in `next/link`. In the App Router, it also types `next/navigation` methods like `push`, `replace`, and `prefetch`. It does not type `next/router` methods in Pages Router.

Literal `href` strings are validated, while non-literal `href`s may require a cast with `as Route`.

To opt-into this feature, `typedRoutes` needs to be enabled and the project needs to be using TypeScript.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  typedRoutes: true,
}

export default nextConfig
```

Next.js will generate a link definition in `.next/types` that contains information about all existing routes in your application, which TypeScript can then use to provide feedback in your editor about invalid links.

> **Good to know**: If you set up your project without `create-next-app`, ensure the generated Next.js types are included by adding `.next/types/**/*.ts` to the `include` array in your `tsconfig.json`:

   tsconfig.json

```
{
  "include": [
    "next-env.d.ts",
    ".next/types/**/*.ts",
    "**/*.ts",
    "**/*.tsx"
  ],
  "exclude": ["node_modules"]
}
```

Currently, support includes any string literal, including dynamic segments. For non-literal strings, you need to manually cast with `as Route`. The example below shows both `next/link` and `next/navigation` usage:

 app/example-client.tsx

```
'use client'

import type { Route } from 'next'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export default function Example() {
  const router = useRouter()
  const slug = 'nextjs'

  return (
    <>
      {/* Link: literal and dynamic */}
      <Link href="/about" />
      <Link href={`/blog/${slug}`} />
      <Link href={('/blog/' + slug) as Route} />
      {/* TypeScript error if href is not a valid route */}
      <Link href="/aboot" />

      {/* Router: literal and dynamic strings are validated */}
      <button onClick={() => router.push('/about')}>Push About</button>
      <button onClick={() => router.replace(`/blog/${slug}`)}>
        Replace Blog
      </button>
      <button onClick={() => router.prefetch('/contact')}>
        Prefetch Contact
      </button>

      {/* For non-literal strings, cast to Route */}
      <button onClick={() => router.push(('/blog/' + slug) as Route)}>
        Push Non-literal Blog
      </button>
    </>
  )
}
```

The same applies for redirecting routes defined by proxy:

 proxy.ts

```
import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  if (request.nextUrl.pathname === '/proxy-redirect') {
    return NextResponse.redirect(new URL('/', request.url))
  }

  return NextResponse.next()
}
```

 app/some/page.tsx

```
import type { Route } from 'next'

export default function Page() {
  return <Link href={'/proxy-redirect' as Route}>Link Text</Link>
}
```

To accept `href` in a custom component wrapping `next/link`, use a generic:

```
import type { Route } from 'next'
import Link from 'next/link'

function Card<T extends string>({ href }: { href: Route<T> | URL }) {
  return (
    <Link href={href}>
      <div>My Card</div>
    </Link>
  )
}
```

You can also type a simple data structure and iterate to render links:

 components/nav-items.ts

```
import type { Route } from 'next'

type NavItem<T extends string = string> = {
  href: T
  label: string
}

export const navItems: NavItem<Route>[] = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About' },
  { href: '/blog', label: 'Blog' },
]
```

Then, map over the items to render `Link`s:

 components/nav.tsx

```
import Link from 'next/link'
import { navItems } from './nav-items'

export function Nav() {
  return (
    <nav>
      {navItems.map((item) => (
        <Link key={item.href} href={item.href}>
          {item.label}
        </Link>
      ))}
    </nav>
  )
}
```

> **How does it work?**
>
>
>
> When running `next dev` or `next build`, Next.js generates a hidden `.d.ts` file inside `.next` that contains information about all existing routes in your application (all valid routes as the `href` type of `Link`). This `.d.ts` file is included in `tsconfig.json` and the TypeScript compiler will check that `.d.ts` and provide feedback in your editor about invalid links.

### Type IntelliSense for Environment Variables

During development, Next.js generates a `.d.ts` file in `.next/types` that contains information about the loaded environment variables for your editor's IntelliSense. If the same environment variable key is defined in multiple files, it is deduplicated according to the [Environment Variable Load Order](https://nextjs.org/docs/app/guides/environment-variables#environment-variable-load-order).

To opt-into this feature, `experimental.typedEnv` needs to be enabled and the project needs to be using TypeScript.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    typedEnv: true,
  },
}

export default nextConfig
```

> **Good to know**: Types are generated based on the environment variables loaded at development runtime, which excludes variables from `.env.production*` files by default. To include production-specific variables, run `next dev` with `NODE_ENV=production`.

### With Async Server Components

To use an `async` Server Component with TypeScript, ensure you are using TypeScript `5.1.3` or higher and `@types/react` `18.2.8` or higher.

If you are using an older version of TypeScript, you may see a `'Promise<Element>' is not a valid JSX element` type error. Updating to the latest version of TypeScript and `@types/react` should resolve this issue.

### Incremental type checking

Since `v10.2.1` Next.js supports [incremental type checking](https://www.typescriptlang.org/tsconfig#incremental) when enabled in your `tsconfig.json`, this can help speed up type checking in larger applications.

### Customtsconfigpath

In some cases, you might want to use a different TypeScript configuration for builds or tooling. To do that, set `typescript.tsconfigPath` in `next.config.ts` to point Next.js to another `tsconfig` file.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  typescript: {
    tsconfigPath: 'tsconfig.build.json',
  },
}

export default nextConfig
```

For example, switch to a different config for production builds:

 next.config.ts

```
import type { NextConfig } from 'next'

const isProd = process.env.NODE_ENV === 'production'

const nextConfig: NextConfig = {
  typescript: {
    tsconfigPath: isProd ? 'tsconfig.build.json' : 'tsconfig.json',
  },
}

export default nextConfig
```

 Why you might use a separate `tsconfig` for builds

You might need to relax checks in scenarios like monorepos, where the build also validates shared dependencies that don't match your project's standards, or when loosening checks in CI to continue delivering while migrating locally to stricter TypeScript settings (and still wanting your IDE to highlight misuse).

For example, if your project uses `useUnknownInCatchVariables` but some monorepo dependencies still assume `any`:

tsconfig.build.json

```
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "useUnknownInCatchVariables": false
  }
}
```

This keeps your editor strict via `tsconfig.json` while allowing the production build to use relaxed settings.

> **Good to know**:
>
>
>
> - IDEs typically read `tsconfig.json` for diagnostics and IntelliSense, so you can still see IDE warnings while production builds use the alternate config. Mirror critical options if you want parity in the editor.
> - In development, only `tsconfig.json` is watched for changes. If you edit a different file name via `typescript.tsconfigPath`, restart the dev server to apply changes.
> - The configured file is used in `next dev`, `next build`, and `next typegen`.

### Disabling TypeScript errors in production

Next.js fails your **production build** (`next build`) when TypeScript errors are present in your project.

If you'd like Next.js to dangerously produce production code even when your application has errors, you can disable the built-in type checking step.

If disabled, be sure you are running type checks as part of your build or deploy process, otherwise this can be very dangerous.

Open `next.config.ts` and enable the `ignoreBuildErrors` option in the [typescript](https://nextjs.org/docs/app/api-reference/config/next-config-js/typescript) config:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: true,
  },
}

export default nextConfig
```

> **Good to know**: You can run `tsc --noEmit` to check for TypeScript errors yourself before building. This is useful for CI/CD pipelines where you'd like to check for TypeScript errors before deploying.

### Custom type declarations

When you need to declare custom types, you might be tempted to modify `next-env.d.ts`. However, this file is automatically generated, so any changes you make will be overwritten. Instead, you should create a new file, let's call it `new-types.d.ts`, and reference it in your `tsconfig.json`:

 tsconfig.json

```
{
  "compilerOptions": {
    "skipLibCheck": true
    //...truncated...
  },
  "include": [
    "new-types.d.ts",
    "next-env.d.ts",
    ".next/types/**/*.ts",
    "**/*.ts",
    "**/*.tsx"
  ],
  "exclude": ["node_modules"]
}
```

## Version Changes

| Version | Changes |
| --- | --- |
| v15.0.0 | next.config.tssupport added for TypeScript projects. |
| v13.2.0 | Statically typed links are available in beta. |
| v12.0.0 | SWCis now used by default to compile TypeScript and TSX for faster builds. |
| v10.2.1 | Incremental type checkingsupport added when enabled in yourtsconfig.json. |

Was this helpful?

supported.

---

# Configuration

> Learn how to configure Next.js applications.

[App Router](https://nextjs.org/docs/app)[API Reference](https://nextjs.org/docs/app/api-reference)Configuration

# Configuration

Last updated  June 16, 2025[next.config.jsLearn how to configure your application with next.config.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js)[TypeScriptNext.js provides a TypeScript-first development experience for building your React application.](https://nextjs.org/docs/app/api-reference/config/typescript)[ESLintLearn how to use and configure the ESLint plugin to catch common issues and problems in a Next.js application.](https://nextjs.org/docs/app/api-reference/config/eslint)

Was this helpful?

supported.

---

# use cache: private

> Learn how to use the "use cache: private" directive to cache functions that access runtime request APIs.

[API Reference](https://nextjs.org/docs/app/api-reference)[Directives](https://nextjs.org/docs/app/api-reference/directives)use cache: private

# use cache: private

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  December 18, 2025

The `'use cache: private'` directive allows functions to access runtime request APIs like `cookies()`, `headers()`, and `searchParams` within a cached scope. However, results are **never stored on the server**, they're cached only in the browser's memory and do not persist across page reloads.

Reach for `'use cache: private'` when:

- You want to cache a function that already accesses runtime data, and refactoring to [move the runtime access outside and pass values as arguments](https://nextjs.org/docs/app/getting-started/cache-components#with-runtime-data) is not practical.
- Compliance requirements prevent storing certain data on the server, even temporarily

Because this directive accesses runtime data, the function executes on every server render and is excluded from running during [static shell](https://nextjs.org/docs/app/getting-started/cache-components#how-rendering-works-with-cache-components) generation.

It is **not** possible to configure custom cache handlers for `'use cache: private'`.

For a comparison of the different cache directives, see [Howuse cache: remotediffers fromuse cacheanduse cache: private](https://nextjs.org/docs/app/api-reference/directives/use-cache-remote#how-use-cache-remote-differs-from-use-cache-and-use-cache-private).

> **Good to know**: This directive is marked as `experimental` because it depends on runtime prefetching, which is not yet stable. Runtime prefetching is an upcoming feature that will let the router prefetch past the [static shell](https://nextjs.org/docs/app/getting-started/cache-components#how-rendering-works-with-cache-components) into **any** cached scope, not just private caches.

## Usage

To use `'use cache: private'`, enable the [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) flag in your `next.config.ts` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

Then add `'use cache: private'` to your function along with a `cacheLife` configuration.

> **Good to know**: This directive is not available in Route Handlers.

### Basic example

In this example, we demonstrate that you can access cookies within a `'use cache: private'` scope:

 app/product/[id]/page.tsxJavaScriptTypeScript

```
import { Suspense } from 'react'
import { cookies } from 'next/headers'
import { cacheLife, cacheTag } from 'next/cache'

export async function generateStaticParams() {
  return [{ id: '1' }]
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return (
    <div>
      <ProductDetails id={id} />
      <Suspense fallback={<div>Loading recommendations...</div>}>
        <Recommendations productId={id} />
      </Suspense>
    </div>
  )
}

async function Recommendations({ productId }: { productId: string }) {
  const recommendations = await getRecommendations(productId)

  return (
    <div>
      {recommendations.map((rec) => (
        <ProductCard key={rec.id} product={rec} />
      ))}
    </div>
  )
}

async function getRecommendations(productId: string) {
  'use cache: private'
  cacheTag(`recommendations-${productId}`)
  cacheLife({ stale: 60 })

  // Access cookies within private cache functions
  const sessionId = (await cookies()).get('session-id')?.value || 'guest'

  return getPersonalizedRecommendations(productId, sessionId)
}
```

> **Good to know**: The `stale` time must be at least 30 seconds for runtime prefetching to work. See [cacheLifeclient router cache behavior](https://nextjs.org/docs/app/api-reference/functions/cacheLife#client-router-cache-behavior) for details.

## Request APIs allowed in private caches

The following request-specific APIs can be used inside `'use cache: private'` functions:

| API | Allowed inuse cache | Allowed in'use cache: private' |
| --- | --- | --- |
| cookies() | No | Yes |
| headers() | No | Yes |
| searchParams | No | Yes |
| connection() | No | No |

> **Note:** The [connection()](https://nextjs.org/docs/app/api-reference/functions/connection) API is prohibited in both `use cache` and `'use cache: private'` as it provides connection-specific information that cannot be safely cached.

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | "use cache: private"is enabled with the Cache Components feature. |

## Related

View related API references.[use cacheLearn how to use the "use cache" directive to cache data in your Next.js application.](https://nextjs.org/docs/app/api-reference/directives/use-cache)[cacheComponentsLearn how to enable the cacheComponents flag in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)[cacheLifeLearn how to use the cacheLife function to set the cache expiration time for a cached function or component.](https://nextjs.org/docs/app/api-reference/functions/cacheLife)[cacheTagLearn how to use the cacheTag function to manage cache invalidation in your Next.js application.](https://nextjs.org/docs/app/api-reference/functions/cacheTag)

Was this helpful?

supported.

---

# use cache: remote

> Learn how to use the "use cache: remote" directive for persistent, shared caching using remote cache handlers.

[API Reference](https://nextjs.org/docs/app/api-reference)[Directives](https://nextjs.org/docs/app/api-reference/directives)use cache: remote

# use cache: remote

Last updated  December 11, 2025

While the `use cache` directive is sufficient for most application needs, you might occasionally notice that cached operations are re-running more often than expected, or that your upstream services (CMS, databases, external APIs) are getting more hits than you'd expect. This can happen because in-memory caching has inherent limitations:

- Cache entries being evicted to make room for new ones
- Memory constraints in your deployment environment
- Cache not persisting across requests or server restarts

Note that `use cache` still provides value beyond server-side caching: it informs Next.js what can be prefetched and defines stale times for client-side navigation.

The `'use cache: remote'` directive lets you declaratively specify that a cached output should be stored in a **remote cache** instead of in-memory. While this gives you more durable caching for specific operations, it comes with tradeoffs: infrastructure cost and network latency during cache lookups.

## Usage

To use `'use cache: remote'`, enable the [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents) flag in your `next.config.ts` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

Then add `'use cache: remote'` to the functions or components where you've determined remote caching is justified. The handler implementation is configured via [cacheHandlers](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheHandlers), though hosting providers should typically provide this automatically. If you're self-hosting, see the `cacheHandlers` configuration reference to set up your cache storage.

### When to avoid remote caching

- If you already have a server-side cache key-value store wrapping your data layer, `use cache` may be sufficient to include data in the static shell without adding another caching layer
- If operations are already fast (< 50ms) due to proximity or local access, the remote cache lookup might not improve performance
- If cache keys have mostly unique values per request (search filters, price ranges, user-specific parameters), cache utilization will be near-zero
- If data changes frequently (seconds to minutes), cache hits will quickly go stale, leading to frequent misses and waiting for upstream revalidation

### When remote caching makes sense

Remote caching provides the most value when content is deferred to request time (outside the static shell). This typically happens when a component accesses request values like [cookies()](https://nextjs.org/docs/app/api-reference/functions/cookies), [headers()](https://nextjs.org/docs/app/api-reference/functions/headers), or [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional), placing it inside a Suspense boundary. In this context:

- Each request executes the component and looks up the cache
- In serverless environments, each instance has its own ephemeral memory with low cache hit rates
- Remote caching provides a shared cache across all instances, improving hit rates and reducing backend load

Compelling scenarios for `'use cache: remote'`:

- **Rate-limited APIs**: Your upstream service has rate limits or request quotas that you risk hitting
- **Protecting slow backends**: Your database or API becomes a bottleneck under high traffic
- **Expensive operations**: Database queries or computations that are costly to run repeatedly
- **Flaky or unreliable services**: External services that occasionally fail or have availability issues

In these cases, the cost and latency of remote caching is justified by avoiding worse outcomes (rate limit errors, backend overload, high compute bills, or degraded user experience).

For static shell content, `use cache` is usually sufficient. However, if your static pages share data from an upstream that can't handle concurrent revalidation requests (like a rate-limited CMS), `use cache: remote` acts as a shared cache layer in front of that upstream. This is the same pattern as putting a key-value store in front of a database, but declared in your code rather than configured in infrastructure.

### Howuse cache: remotediffers fromuse cacheanduse cache: private

Next.js provides three caching directives, each designed for different use cases:

| Feature | use cache | 'use cache: remote' | 'use cache: private' |
| --- | --- | --- | --- |
| Server-side caching | In-memory or cache handler | Remote cache handler | None |
| Cache scope | Shared across all users | Shared across all users | Per-client (browser) |
| Can access cookies/headers directly | No (must pass as arguments) | No (must pass as arguments) | Yes |
| Server cache utilization | May be low outside static shell | High (shared across instances) | N/A |
| Additional costs | None | Infrastructure (storage, network) | None |
| Latency impact | None | Cache handler lookup | None |

### Caching with runtime data

Both `use cache` and `'use cache: remote'` directives can't access runtime data like cookies or search params directly, since this data isn't available when computing the cache. However, you can extract values from these APIs and pass them as arguments to cached functions. See [with runtime data](https://nextjs.org/docs/app/getting-started/cache-components#with-runtime-data) for this pattern.

In general, but most importantly for `'use cache: remote'`, be thoughtful about which values you include in cache keys. Each unique value creates a separate cache entry, reducing cache utilization. Consider this example with search filters:

 app/products/[category]/page.tsx

```
import { Suspense } from 'react'

export default async function ProductsPage({
  params,
  searchParams,
}: {
  params: Promise<{ category: string }>
  searchParams: Promise<{ minPrice?: string }>
}) {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ProductList params={params} searchParams={searchParams} />
    </Suspense>
  )
}

async function ProductList({
  params,
  searchParams,
}: {
  params: Promise<{ category: string }>
  searchParams: Promise<{ minPrice?: string }>
}) {
  const { category } = await params

  const { minPrice } = await searchParams

  // Cache only on category (few unique values)
  // Don't include price filter (many unique values)
  const products = await getProductsByCategory(category)

  // Filter price in memory instead of creating cache entries
  // for every price value
  const filtered = minPrice
    ? products.filter((p) => p.price >= parseFloat(minPrice))
    : products

  return <div>{/* render filtered products */}</div>
}

async function getProductsByCategory(category: string) {
  'use cache: remote'
  // Only category is part of the cache key
  // Much better utilization than caching every price filter value
  return db.products.findByCategory(category)
}
```

In this example, the remote handler stores more data per cache entry (all products in a category) to achieve better cache hit rates. This is worth it when the cost of cache misses (hitting your backend) outweighs the storage cost of larger entries.

The same principle applies to user-specific data. Rather than caching per-user data directly, use user preferences to determine what shared data to cache.

For example, if users have a language preference in their session, extract that preference and use it to cache shared content:

- Instead of remote caching `getUserProfile(sessionID)`, which creates one entry per user
- Remote cache `getCMSContent(language)` to create one entry per language

 app/components/welcome-message.tsx

```
import { cookies } from 'next/headers'
import { cacheLife } from 'next/cache'

export async function WelcomeMessage() {
  // Extract the language preference (not unique per user)
  const language = (await cookies()).get('language')?.value || 'en'

  // Cache based on language (few unique values: en, es, fr, de, etc.)
  // All users who prefer 'en' share the same cache entry
  const content = await getCMSContent(language)

  return <div>{content.welcomeMessage}</div>
}

async function getCMSContent(language: string) {
  'use cache: remote'
  cacheLife({ expire: 3600 })
  // Creates ~10-50 cache entries (one per language)
  // instead of thousands (one per user)
  return cms.getHomeContent(language)
}
```

This way all users who prefer the same language share a cache entry, improving cache utilization and reducing load on your CMS.

The pattern is the same in both examples: find the dimension with fewer unique values (category vs. price, language vs. user ID), cache on that dimension, and filter or select the rest in memory.

If the service used by `getUserProfile` cannot scale with your frontend load, you may still be able to use the `use cache` directive with a short `cacheLife` for in-memory caching. However, for most user data, you likely want to fetch directly from the source (which might already be wrapped in a key/value store as mentioned in the guidelines above).

Only use ['use cache: private'](https://nextjs.org/docs/app/api-reference/directives/use-cache-private) if you have compliance requirements or can't refactor to pass runtime data as arguments.

### Nesting rules

Remote caches have specific nesting rules:

- Remote caches **can** be nested inside other remote caches (`'use cache: remote'`)
- Remote caches **can** be nested inside regular caches (`'use cache'`)
- Remote caches **cannot** be nested inside private caches (`'use cache: private'`)
- Private caches **cannot** be nested inside remote caches

```
// VALID: Remote inside remote
async function outerRemote() {
  'use cache: remote'
  const result = await innerRemote()
  return result
}

async function innerRemote() {
  'use cache: remote'
  return getData()
}

// VALID: Remote inside regular cache
async function outerCache() {
  'use cache'
  // The inner remote cache will work when deferred to request time
  const result = await innerRemote()
  return result
}

async function innerRemote() {
  'use cache: remote'
  return getData()
}

// INVALID: Remote inside private
async function outerPrivate() {
  'use cache: private'
  const result = await innerRemote() // Error!
  return result
}

async function innerRemote() {
  'use cache: remote'
  return getData()
}

// INVALID: Private inside remote
async function outerRemote() {
  'use cache: remote'
  const result = await innerPrivate() // Error!
  return result
}

async function innerPrivate() {
  'use cache: private'
  return getData()
}
```

## Examples

The following examples demonstrate common patterns for using `'use cache: remote'`. For details about `cacheLife` parameters (`stale`, `revalidate`, `expire`), see the [cacheLifeAPI reference](https://nextjs.org/docs/app/api-reference/functions/cacheLife).

### With user preferences

Cache product pricing based on the user's currency preference. Since the currency is stored in a cookie, this component renders at request time. Remote caching is valuable here because all users with the same currency share the cached price, and in serverless environments, all instances share the same remote cache.

 app/product/[id]/page.tsxJavaScriptTypeScript

```
import { Suspense } from 'react'
import { cookies } from 'next/headers'
import { cacheTag, cacheLife } from 'next/cache'

export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }, { id: '3' }]
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return (
    <div>
      <ProductDetails id={id} />
      <Suspense fallback={<div>Loading price...</div>}>
        <ProductPrice productId={id} />
      </Suspense>
    </div>
  )
}

function ProductDetails({ id }: { id: string }) {
  return <div>Product: {id}</div>
}

async function ProductPrice({ productId }: { productId: string }) {
  // Reading cookies defers this component to request time
  const currency = (await cookies()).get('currency')?.value ?? 'USD'

  // Cache the price per product and currency combination
  // All users with the same currency share this cache entry
  const price = await getProductPrice(productId, currency)

  return (
    <div>
      Price: {price} {currency}
    </div>
  )
}

async function getProductPrice(productId: string, currency: string) {
  'use cache: remote'
  cacheTag(`product-price-${productId}`)
  cacheLife({ expire: 3600 }) // 1 hour

  // Cached per (productId, currency) - few currencies means high cache utilization
  return db.products.getPrice(productId, currency)
}
```

### Reducing database load

Cache expensive database queries, reducing load on your database. In this example, we don't access `cookies()`, `headers()`, or `searchParams`. If we had a requirement to not include these stats in the static shell, we could use [connection()](https://nextjs.org/docs/app/api-reference/functions/connection) to explicitly defer to request time:

 app/dashboard/page.tsx

```
import { Suspense } from 'react'
import { connection } from 'next/server'
import { cacheLife, cacheTag } from 'next/cache'

export default function DashboardPage() {
  return (
    <Suspense fallback={<div>Loading stats...</div>}>
      <DashboardStats />
    </Suspense>
  )
}

async function DashboardStats() {
  // Defer to request time
  await connection()

  const stats = await getGlobalStats()

  return <StatsDisplay stats={stats} />
}

async function getGlobalStats() {
  'use cache: remote'
  cacheTag('global-stats')
  cacheLife({ expire: 60 }) // 1 minute

  // This expensive database query is cached and shared across all users,
  // reducing load on your database
  const stats = await db.analytics.aggregate({
    total_users: 'count',
    active_sessions: 'count',
    revenue: 'sum',
  })

  return stats
}
```

With this setup, your upstream database sees at most one request per minute, regardless of how many users visit the dashboard.

### API responses in streaming contexts

Cache API responses that are fetched during streaming or after dynamic operations:

 app/feed/page.tsx

```
import { Suspense } from 'react'
import { connection } from 'next/server'
import { cacheLife, cacheTag } from 'next/cache'

export default async function FeedPage() {
  return (
    <div>
      <Suspense fallback={<Skeleton />}>
        <FeedItems />
      </Suspense>
    </div>
  )
}

async function FeedItems() {
  // Defer to request time
  await connection()

  const items = await getFeedItems()

  return items.map((item) => <FeedItem key={item.id} item={item} />)
}

async function getFeedItems() {
  'use cache: remote'
  cacheTag('feed-items')
  cacheLife({ expire: 120 }) // 2 minutes

  // This API call is cached, reducing requests to your external service
  const response = await fetch('https://api.example.com/feed')
  return response.json()
}
```

### Computed data after dynamic checks

Cache expensive computations that occur after dynamic security or feature checks:

 app/reports/page.tsx

```
import { connection } from 'next/server'
import { cacheLife } from 'next/cache'

export default async function ReportsPage() {
  // Defer to request time (for security check)
  await connection()

  const report = await generateReport()

  return <ReportViewer report={report} />
}

async function generateReport() {
  'use cache: remote'
  cacheLife({ expire: 3600 }) // 1 hour

  // This expensive computation is cached and shared across all authorized users,
  // avoiding repeated calculations
  const data = await db.transactions.findMany()

  return {
    totalRevenue: calculateRevenue(data),
    topProducts: analyzeProducts(data),
    trends: calculateTrends(data),
  }
}
```

### Mixed caching strategies

Combine static, remote, and private caching for optimal performance:

 app/product/[id]/page.tsx

```
import { Suspense } from 'react'
import { connection } from 'next/server'
import { cookies } from 'next/headers'
import { cacheLife, cacheTag } from 'next/cache'

// Static product data - prerendered at build time
async function getProduct(id: string) {
  'use cache'
  cacheTag(`product-${id}`)

  // This is cached at build time and shared across all users
  return db.products.find({ where: { id } })
}

// Shared pricing data - cached at runtime in remote handler
async function getProductPrice(id: string) {
  'use cache: remote'
  cacheTag(`product-price-${id}`)
  cacheLife({ expire: 300 }) // 5 minutes

  // This is cached at runtime and shared across all users
  return db.products.getPrice({ where: { id } })
}

// User-specific recommendations - private cache per user
async function getRecommendations(productId: string) {
  'use cache: private'
  cacheLife({ expire: 60 }) // 1 minute

  const sessionId = (await cookies()).get('session-id')?.value

  // This is cached per-user and never shared
  return db.recommendations.findMany({
    where: { productId, sessionId },
  })
}

export default async function ProductPage({ params }) {
  const { id } = await params

  // Static product data
  const product = await getProduct(id)

  return (
    <div>
      <ProductDetails product={product} />

      {/* Dynamic shared price */}
      <Suspense fallback={<PriceSkeleton />}>
        <ProductPriceComponent productId={id} />
      </Suspense>

      {/* Dynamic personalized recommendations */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <ProductRecommendations productId={id} />
      </Suspense>
    </div>
  )
}

function ProductDetails({ product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  )
}

async function ProductPriceComponent({ productId }) {
  // Defer to request time
  await connection()

  const price = await getProductPrice(productId)
  return <div>Price: ${price}</div>
}

async function ProductRecommendations({ productId }) {
  const recommendations = await getRecommendations(productId)
  return <RecommendationsList items={recommendations} />
}

function PriceSkeleton() {
  return <div>Loading price...</div>
}

function RecommendationsSkeleton() {
  return <div>Loading recommendations...</div>
}

function RecommendationsList({ items }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}
```

> **Good to know**:
>
>
>
> - Remote caches are stored in server-side cache handlers and shared across all users
> - `'use cache: remote'` works outside the static shell where [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache) may not provide server-side cache hits
> - Use [cacheTag()](https://nextjs.org/docs/app/api-reference/functions/cacheTag) and [revalidateTag()](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) to invalidate remote caches on-demand
> - Use [cacheLife()](https://nextjs.org/docs/app/api-reference/functions/cacheLife) to configure cache expiration
> - For user-specific data, use ['use cache: private'](https://nextjs.org/docs/app/api-reference/directives/use-cache-private) instead of `'use cache: remote'`
> - Remote caches reduce origin load by storing computed or fetched data server-side

## Platform Support

| Deployment Option | Supported |
| --- | --- |
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Yes |

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | "use cache: remote"is enabled with the Cache Components feature. |

## Related

View related API references.[use cacheLearn how to use the "use cache" directive to cache data in your Next.js application.](https://nextjs.org/docs/app/api-reference/directives/use-cache)[use cache: privateLearn how to use the "use cache: private" directive to cache functions that access runtime request APIs.](https://nextjs.org/docs/app/api-reference/directives/use-cache-private)[cacheComponentsLearn how to enable the cacheComponents flag in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)[cacheHandlersConfigure custom cache handlers for use cache directives in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheHandlers)[cacheLifeLearn how to use the cacheLife function to set the cache expiration time for a cached function or component.](https://nextjs.org/docs/app/api-reference/functions/cacheLife)[cacheTagLearn how to use the cacheTag function to manage cache invalidation in your Next.js application.](https://nextjs.org/docs/app/api-reference/functions/cacheTag)[connectionAPI Reference for the connection function.](https://nextjs.org/docs/app/api-reference/functions/connection)

Was this helpful?

supported.
