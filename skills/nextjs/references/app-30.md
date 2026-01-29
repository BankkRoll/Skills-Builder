# Internationalization and more

# Internationalization

> Add support for multiple languages with internationalized routing and localized content.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Internationalization

# Internationalization

Last updated  December 9, 2025

Next.js enables you to configure the routing and rendering of content to support multiple languages. Making your site adaptive to different locales includes translated content (localization) and internationalized routes.

## Terminology

- **Locale:** An identifier for a set of language and formatting preferences. This usually includes the preferred language of the user and possibly their geographic region.
  - `en-US`: English as spoken in the United States
  - `nl-NL`: Dutch as spoken in the Netherlands
  - `nl`: Dutch, no specific region

## Routing Overview

It’s recommended to use the user’s language preferences in the browser to select which locale to use. Changing your preferred language will modify the incoming `Accept-Language` header to your application.

For example, using the following libraries, you can look at an incoming `Request` to determine which locale to select, based on the `Headers`, locales you plan to support, and the default locale.

 proxy.js

```
import { match } from '@formatjs/intl-localematcher'
import Negotiator from 'negotiator'

let headers = { 'accept-language': 'en-US,en;q=0.5' }
let languages = new Negotiator({ headers }).languages()
let locales = ['en-US', 'nl-NL', 'nl']
let defaultLocale = 'en-US'

match(languages, locales, defaultLocale) // -> 'en-US'
```

Routing can be internationalized by either the sub-path (`/fr/products`) or domain (`my-site.fr/products`). With this information, you can now redirect the user based on the locale inside [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy).

 proxy.js

```
import { NextResponse } from "next/server";

let locales = ['en-US', 'nl-NL', 'nl']

// Get the preferred locale, similar to the above or using a library
function getLocale(request) { ... }

export function proxy(request) {
  // Check if there is any supported locale in the pathname
  const { pathname } = request.nextUrl
  const pathnameHasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  )

  if (pathnameHasLocale) return

  // Redirect if there is no locale
  const locale = getLocale(request)
  request.nextUrl.pathname = `/${locale}${pathname}`
  // e.g. incoming request is /products
  // The new URL is now /en-US/products
  return NextResponse.redirect(request.nextUrl)
}

export const config = {
  matcher: [
    // Skip all internal paths (_next)
    '/((?!_next).*)',
    // Optional: only run on root (/) URL
    // '/'
  ],
}
```

Finally, ensure all special files inside `app/` are nested under `app/[lang]`. This enables the Next.js router to dynamically handle different locales in the route, and forward the `lang` parameter to every layout and page. For example:

 app/[lang]/page.tsxJavaScriptTypeScript

```
// You now have access to the current locale
// e.g. /en-US/products -> `lang` is "en-US"
export default async function Page({ params }: PageProps<'/[lang]'>) {
  const { lang } = await params
  return ...
}
```

> **Good to know:** `PageProps` and `LayoutProps` are globally available TypeScript helpers that provide strong typing for route parameters. See [PageProps](https://nextjs.org/docs/app/api-reference/file-conventions/page#page-props-helper) and [LayoutProps](https://nextjs.org/docs/app/api-reference/file-conventions/layout#layout-props-helper) for more details.

The root layout can also be nested in the new folder (e.g. `app/[lang]/layout.js`).

## Localization

Changing displayed content based on the user’s preferred locale, or localization, is not something specific to Next.js. The patterns described below would work the same with any web application.

Let’s assume we want to support both English and Dutch content inside our application. We might maintain two different “dictionaries”, which are objects that give us a mapping from some key to a localized string. For example:

 dictionaries/en.json

```
{
  "products": {
    "cart": "Add to Cart"
  }
}
```

 dictionaries/nl.json

```
{
  "products": {
    "cart": "Toevoegen aan Winkelwagen"
  }
}
```

We can then create a `getDictionary` function to load the translations for the requested locale:

 app/[lang]/dictionaries.tsJavaScriptTypeScript

```
import 'server-only'

const dictionaries = {
  en: () => import('./dictionaries/en.json').then((module) => module.default),
  nl: () => import('./dictionaries/nl.json').then((module) => module.default),
}

export type Locale = keyof typeof dictionaries

export const hasLocale = (locale: string): locale is Locale =>
  locale in dictionaries

export const getDictionary = async (locale: Locale) => dictionaries[locale]()
```

Given the currently selected language, we can fetch the dictionary inside of a layout or page.

Since `lang` is typed as `string`, using `hasLocale` narrows the type to your supported locales. It also ensures a 404 is returned if a translation is missing, rather than a runtime error.

 app/[lang]/page.tsxJavaScriptTypeScript

```
import { notFound } from 'next/navigation'
import { getDictionary, hasLocale } from './dictionaries'

export default async function Page({ params }: PageProps<'/[lang]'>) {
  const { lang } = await params

  if (!hasLocale(lang)) notFound()

  const dict = await getDictionary(lang)
  return <button>{dict.products.cart}</button> // Add to Cart
}
```

Because all layouts and pages in the `app/` directory default to [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), we do not need to worry about the size of the translation files affecting our client-side JavaScript bundle size. This code will **only run on the server**, and only the resulting HTML will be sent to the browser.

## Static Rendering

To generate static routes for a given set of locales, we can use `generateStaticParams` with any page or layout. This can be global, for example, in the root layout:

 app/[lang]/layout.tsxJavaScriptTypeScript

```
export async function generateStaticParams() {
  return [{ lang: 'en-US' }, { lang: 'de' }]
}

export default async function RootLayout({
  children,
  params,
}: LayoutProps<'/[lang]'>) {
  return (
    <html lang={(await params).lang}>
      <body>{children}</body>
    </html>
  )
}
```

## Resources

- [Minimal i18n routing and translations](https://github.com/vercel/next.js/tree/canary/examples/i18n-routing)
- [next-intl](https://next-intl.dev)
- [next-international](https://github.com/QuiiBz/next-international)
- [next-i18n-router](https://github.com/i18nexus/next-i18n-router)
- [paraglide-next](https://inlang.com/m/osslbuzt/paraglide-next-i18n)
- [lingui](https://lingui.dev)
- [tolgee](https://tolgee.io/apps-integrations/next)
- [next-intlayer](https://intlayer.org/doc/environment/nextjs)
- [gt-next](https://generaltranslation.com/en/docs/next)

Was this helpful?

supported.

---

# How to implement JSON

> Learn how to add JSON-LD to your Next.js application to describe your content to search engines and AI.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)JSON-LD

# How to implement JSON-LD in your Next.js application

Last updated  September 30, 2025

[JSON-LD](https://json-ld.org/) is a format for structured data that can be used by search engines and AI to help them understand the structure of the page beyond pure content. For example, you can use it to describe a person, an event, an organization, a movie, a book, a recipe, and many other types of entities.

Our current recommendation for JSON-LD is to render structured data as a `<script>` tag in your `layout.js` or `page.js` components.

The following snippet uses `JSON.stringify`, which does not sanitize malicious strings used in XSS injection. To prevent this type of vulnerability, you can scrub `HTML` tags from the `JSON-LD` payload, for example, by replacing the character, `<`, with its unicode equivalent, `\u003c`.

Review your organization's recommended approach to sanitize potentially dangerous strings, or use community maintained alternatives for `JSON.stringify` such as, [serialize-javascript](https://www.npmjs.com/package/serialize-javascript).

 app/products/[id]/page.tsxJavaScriptTypeScript

```
export default async function Page({ params }) {
  const { id } = await params
  const product = await getProduct(id)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: product.image,
    description: product.description,
  }

  return (
    <section>
      {/* Add JSON-LD to your page */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c'),
        }}
      />
      {/* ... */}
    </section>
  )
}
```

You can validate and test your structured data with the [Rich Results Test](https://search.google.com/test/rich-results) for Google or the generic [Schema Markup Validator](https://validator.schema.org/).

You can type your JSON-LD with TypeScript using community packages like [schema-dts](https://www.npmjs.com/package/schema-dts):

```
import { Product, WithContext } from 'schema-dts'

const jsonLd: WithContext<Product> = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: 'Next.js Sticker',
  image: 'https://nextjs.org/imgs/sticker.png',
  description: 'Dynamic at the speed of static.',
}
```

Was this helpful?

supported.

---

# How to lazy load Client Components and libraries

> Lazy load imported libraries and React Components to improve your application's loading performance.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Lazy Loading

# How to lazy load Client Components and libraries

Last updated  October 15, 2025

[Lazy loading](https://developer.mozilla.org/docs/Web/Performance/Lazy_loading) in Next.js helps improve the initial loading performance of an application by decreasing the amount of JavaScript needed to render a route.

It allows you to defer loading of **Client Components** and imported libraries, and only include them in the client bundle when they're needed. For example, you might want to defer loading a modal until a user clicks to open it.

There are two ways you can implement lazy loading in Next.js:

1. Using [Dynamic Imports](#nextdynamic) with `next/dynamic`
2. Using [React.lazy()](https://react.dev/reference/react/lazy) with [Suspense](https://react.dev/reference/react/Suspense)

By default, Server Components are automatically [code split](https://developer.mozilla.org/docs/Glossary/Code_splitting), and you can use [streaming](https://nextjs.org/docs/app/api-reference/file-conventions/loading) to progressively send pieces of UI from the server to the client. Lazy loading applies to Client Components.

## next/dynamic

`next/dynamic` is a composite of [React.lazy()](https://react.dev/reference/react/lazy) and [Suspense](https://react.dev/reference/react/Suspense). It behaves the same way in the `app` and `pages` directories to allow for incremental migration.

## Examples

### Importing Client Components

app/page.js

```
'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'

// Client Components:
const ComponentA = dynamic(() => import('../components/A'))
const ComponentB = dynamic(() => import('../components/B'))
const ComponentC = dynamic(() => import('../components/C'), { ssr: false })

export default function ClientComponentExample() {
  const [showMore, setShowMore] = useState(false)

  return (
    <div>
      {/* Load immediately, but in a separate client bundle */}
      <ComponentA />

      {/* Load on demand, only when/if the condition is met */}
      {showMore && <ComponentB />}
      <button onClick={() => setShowMore(!showMore)}>Toggle</button>

      {/* Load only on the client side */}
      <ComponentC />
    </div>
  )
}
```

> **Note:** When a Server Component dynamically imports a Client Component, automatic [code splitting](https://developer.mozilla.org/docs/Glossary/Code_splitting) is currently **not** supported.

### Skipping SSR

When using `React.lazy()` and Suspense, Client Components will be [prerendered](https://github.com/reactwg/server-components/discussions/4) (SSR) by default.

> **Note:** `ssr: false` option will only work for Client Components, move it into Client Components ensure the client code-splitting working properly.

If you want to disable pre-rendering for a Client Component, you can use the `ssr` option set to `false`:

```
const ComponentC = dynamic(() => import('../components/C'), { ssr: false })
```

### Importing Server Components

If you dynamically import a Server Component, only the Client Components that are children of the Server Component will be lazy-loaded - not the Server Component itself.
It will also help preload the static assets such as CSS when you're using it in Server Components.

app/page.js

```
import dynamic from 'next/dynamic'

// Server Component:
const ServerComponent = dynamic(() => import('../components/ServerComponent'))

export default function ServerComponentExample() {
  return (
    <div>
      <ServerComponent />
    </div>
  )
}
```

> **Note:** `ssr: false` option is not supported in Server Components. You will see an error if you try to use it in Server Components.
> `ssr: false` is not allowed with `next/dynamic` in Server Components. Please move it into a Client Component.

### Loading External Libraries

External libraries can be loaded on demand using the [import()](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/import) function. This example uses the external library `fuse.js` for fuzzy search. The module is only loaded on the client after the user types in the search input.

app/page.js

```
'use client'

import { useState } from 'react'

const names = ['Tim', 'Joe', 'Bel', 'Lee']

export default function Page() {
  const [results, setResults] = useState()

  return (
    <div>
      <input
        type="text"
        placeholder="Search"
        onChange={async (e) => {
          const { value } = e.currentTarget
          // Dynamically load fuse.js
          const Fuse = (await import('fuse.js')).default
          const fuse = new Fuse(names)

          setResults(fuse.search(value))
        }}
      />
      <pre>Results: {JSON.stringify(results, null, 2)}</pre>
    </div>
  )
}
```

### Adding a custom loading component

app/page.js

```
'use client'

import dynamic from 'next/dynamic'

const WithCustomLoading = dynamic(
  () => import('../components/WithCustomLoading'),
  {
    loading: () => <p>Loading...</p>,
  }
)

export default function Page() {
  return (
    <div>
      {/* The loading component will be rendered while  <WithCustomLoading/> is loading */}
      <WithCustomLoading />
    </div>
  )
}
```

### Importing Named Exports

To dynamically import a named export, you can return it from the Promise returned by [import()](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/import) function:

components/hello.js

```
'use client'

export function Hello() {
  return <p>Hello!</p>
}
```

app/page.js

```
import dynamic from 'next/dynamic'

const ClientComponent = dynamic(() =>
  import('../components/hello').then((mod) => mod.Hello)
)
```

Was this helpful?

supported.

---

# How to optimize your local development environment

> Learn how to optimize your local development environment with Next.js.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Development Environment

# How to optimize your local development environment

Last updated  October 16, 2025

Next.js is designed to provide a great developer experience. As your application grows, you might notice slower compilation times during local development. This guide will help you identify and fix common compile-time performance issues.

## Local dev vs. production

The development process with `next dev` is different than `next build` and `next start`.

`next dev` compiles routes in your application as you open or navigate to them. This enables you to start the dev server without waiting for every route in your application to compile, which is both faster and uses less memory. Running a production build applies other optimizations, like minifying files and creating content hashes, which are not needed for local development.

## Improving local dev performance

### 1. Check your computer's antivirus

Antivirus software can slow down file access. While this is more common on Windows machines, this can be an issue for any system with an antivirus tool installed.

On Windows, you can add your project to the [Microsoft Defender Antivirus exclusion list](https://support.microsoft.com/en-us/windows/virus-and-threat-protection-in-the-windows-security-app-1362f4cd-d71a-b52a-0b66-c2820032b65e#bkmk_threat-protection-settings).

1. Open the **"Windows Security"** application and then select **"Virus & threat protection"** → **"Manage settings"** → **"Add or remove exclusions"**.
2. Add a **"Folder"** exclusion. Select your project folder.

On macOS, you can disable [Gatekeeper](https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web) inside of your terminal.

1. Run `sudo spctl developer-mode enable-terminal` in your terminal.
2. Open the **"System Settings"** app and then select **"Privacy & Security"** → **"Developer Tools"**.
3. Ensure your terminal is listed and enabled. If you're using a third-party terminal like iTerm or Ghostty, add that to the list.
4. Restart your terminal.

 ![Screenshot of macOS System Settings showing the Privacy & Security pane](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fmacos-gatekeeper-privacy-and-security.png&w=1920&q=75)![Screenshot of macOS System Settings showing the Privacy & Security pane](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fmacos-gatekeeper-privacy-and-security.png&w=1920&q=75) ![Screenshot of macOS System Settings showing the Developer Tools options](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fmacos-gatekeeper-developer-tools.png&w=1920&q=75)![Screenshot of macOS System Settings showing the Developer Tools options](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fmacos-gatekeeper-developer-tools.png&w=1920&q=75)

If you or your employer have configured any other Antivirus solutions on your system, you should inspect the relevant settings for those products.

### 2. Update Next.js and use Turbopack

Make sure you're using the latest version of Next.js. Each new version often includes performance improvements.

Turbopack is now the default bundler for Next.js development and provides significant performance improvements over webpack.

```
npm install next@latest
npm run dev  # Turbopack is used by default
```

If you need to use Webpack instead of Turbopack, you can opt-in:

```
npm run dev --webpack
```

[Learn more about Turbopack](https://nextjs.org/blog/turbopack-for-development-stable). See our [upgrade guides](https://nextjs.org/docs/app/guides/upgrading) and codemods for more information.

### 3. Check your imports

The way you import code can greatly affect compilation and bundling time. Learn more about [optimizing package bundling](https://nextjs.org/docs/app/guides/package-bundling) and explore tools like [Dependency Cruiser](https://github.com/sverweij/dependency-cruiser) or [Madge](https://github.com/pahen/madge).

#### Icon libraries

Libraries like `@material-ui/icons`, `@phosphor-icons/react`, or `react-icons` can import thousands of icons, even if you only use a few. Try to import only the icons you need:

```
// Instead of this:
import { TriangleIcon } from '@phosphor-icons/react'

// Do this:
import { TriangleIcon } from '@phosphor-icons/react/dist/csr/Triangle'
```

You can often find what import pattern to use in the documentation for the icon library you're using. This example follows [@phosphor-icons/react](https://www.npmjs.com/package/@phosphor-icons/react#import-performance-optimization) recommendation.

Libraries like `react-icons` includes many different icon sets. Choose one set and stick with that set.

For example, if your application uses `react-icons` and imports all of these:

- `pi` (Phosphor Icons)
- `md` (Material Design Icons)
- `tb` (tabler-icons)
- `cg` (cssgg)

Combined they will be tens of thousands of modules that the compiler has to handle, even if you only use a single import from each.

#### Barrel files

"Barrel files" are files that export many items from other files. They can slow down builds because the compiler has to parse them to find if there are side-effects in the module scope by using the import.

Try to import directly from specific files when possible. [Learn more about barrel files](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js) and the built-in optimizations in Next.js.

#### Optimize package imports

Next.js can automatically optimize imports for certain packages. If you are using packages that utilize barrel files, add them to your `next.config.js`:

```
module.exports = {
  experimental: {
    optimizePackageImports: ['package-name'],
  },
}
```

Turbopack automatically analyzes imports and optimizes them. It does not require this configuration.

### 4. Check your Tailwind CSS setup

If you're using Tailwind CSS, make sure it's set up correctly.

A common mistake is configuring your `content` array in a way which includes `node_modules` or other large directories of files that should not be scanned.

Tailwind CSS version 3.4.8 or newer will warn you about settings that might slow down your build.

1. In your `tailwind.config.js`, be specific about which files to scan:
  ```
  module.exports = {
    content: [
      './src/**/*.{js,ts,jsx,tsx}', // Good
      // This might be too broad
      // It will match `packages/**/node_modules` too
      // '../../packages/**/*.{js,ts,jsx,tsx}',
    ],
  }
  ```
2. Avoid scanning unnecessary files:
  ```
  module.exports = {
    content: [
      // Better - only scans the 'src' folder
      '../../packages/ui/src/**/*.{js,ts,jsx,tsx}',
    ],
  }
  ```

### 5. Check custom webpack settings

If you've added custom webpack settings, they might be slowing down compilation.

Consider if you really need them for local development. You can optionally only include certain tools for production builds, or explore using the default Turbopack bundler and configuring [loaders](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#configuring-webpack-loaders) instead.

### 6. Optimize memory usage

If your app is very large, it might need more memory.

[Learn more about optimizing memory usage](https://nextjs.org/docs/app/guides/memory-usage).

### 7. Server Components and data fetching

Changes to Server Components cause the entire page to re-render locally in order to show the new changes, which includes fetching new data for the component.

The experimental `serverComponentsHmrCache` option allows you to cache `fetch` responses in Server Components across Hot Module Replacement (HMR) refreshes in local development. This results in faster responses and reduced costs for billed API calls.

[Learn more about the experimental option](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverComponentsHmrCache).

### 8. Consider local development over Docker

If you're using Docker for development on Mac or Windows, you may experience significantly slower performance compared to running Next.js locally.

Docker's filesystem access on Mac and Windows can cause Hot Module Replacement (HMR) to take seconds or even minutes, while the same application runs with fast HMR when developed locally.

This performance difference is due to how Docker handles filesystem operations outside of Linux environments. For the best development experience:

- Use local development (`npm run dev` or `pnpm dev`) instead of Docker during development
- Reserve Docker for production deployments and testing production builds
- If you must use Docker for development, consider using Docker on a Linux machine or VM

[Learn more about Docker deployment](https://nextjs.org/docs/app/getting-started/deploying#docker) for production use.

## Tools for finding problems

### Detailed fetch logging

Use the `logging.fetches` option in your `next.config.js` file, to see more detailed information about what's happening during development:

```
module.exports = {
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
}
```

[Learn more about fetch logging](https://nextjs.org/docs/app/api-reference/config/next-config-js/logging).

### Turbopack tracing

Turbopack tracing is a tool that helps you understand the performance of your application during local development.
It provides detailed information about the time taken for each module to compile and how they are related.

1. Make sure you have the latest version of Next.js installed.
2. Generate a Turbopack trace file:
  ```
  NEXT_TURBOPACK_TRACING=1 npm run dev
  ```
3. Navigate around your application or make edits to files to reproduce the problem.
4. Stop the Next.js development server.
5. A file called `trace-turbopack` will be available in the `.next/dev` folder.
6. You can interpret the file using `npx next internal trace [path-to-file]`:
  ```
  npx next internal trace .next/dev/trace-turbopack
  ```
  On versions where `trace` is not available, the command was named `turbo-trace-server`:
  ```
  npx next internal turbo-trace-server .next/dev/trace-turbopack
  ```
7. Once the trace server is running you can view the trace at [https://trace.nextjs.org/](https://trace.nextjs.org/).
8. By default the trace viewer will aggregate timings, in order to see each individual time you can switch from "Aggregated in order" to "Spans in order" at the top right of the viewer.

> **Good to know**: The trace file is place under the development server directory, which defaults to `.next/dev`. This is controllable using the [isolatedDevBuild](https://nextjs.org/docs/app/api-reference/config/next-config-js/isolatedDevBuild) flag in your Next config file.

### Still having problems?

Share the trace file generated in the [Turbopack Tracing](#turbopack-tracing) section and share it on [GitHub Discussions](https://github.com/vercel/next.js/discussions) or [Discord](https://nextjs.org/discord).

Was this helpful?

supported.

---

# Enabling Next.js MCP Server for Coding Agents

> Learn how to use Next.js MCP support to allow coding agents access to your application state

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Next.js MCP Server

# Enabling Next.js MCP Server for Coding Agents

Last updated  January 6, 2026

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open standard that allows AI agents and coding assistants to interact with your applications through a standardized interface.

Next.js 16+ includes MCP support that enables coding agents to access your application's internals in real-time. To use this functionality, install the [next-devtools-mcp](https://www.npmjs.com/package/next-devtools-mcp) package.

## Getting started

**Requirements:** Next.js 16 or above

Add `next-devtools-mcp` to the `.mcp.json` file at the root of your project:

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

That's it! When you start your development server, `next-devtools-mcp` will automatically discover and connect to your running Next.js instance.

For more configuration options, see the [next-devtools-mcp repository](https://github.com/vercel/next-devtools-mcp).

## Capabilities

`next-devtools-mcp` provides coding agents with a growing set of capabilities:

### Application Runtime Access

- **Error Detection**: Retrieve current build errors, runtime errors, and type errors from your dev server
- **Live State Queries**: Access real-time application state and runtime information
- **Page Metadata**: Query page routes, components, and rendering details
- **Server Actions**: Inspect Server Actions and component hierarchies
- **Development Logs**: Access development server logs and console output

### Development Tools

- **Next.js Knowledge Base**: Query comprehensive Next.js documentation and best practices
- **Migration and Upgrade Tools**: Automated helpers for upgrading to Next.js 16 with codemods
- **Cache Components Guide**: Setup and configuration assistance for Cache Components
- **Browser Testing**: [Playwright MCP](https://github.com/microsoft/playwright-mcp) integration for verifying pages in the browser

> **Note:** The Next.js team is actively expanding these capabilities. New tools and features are added regularly to improve the agent development experience.

## Development workflow

1. Start your Next.js development server:

 Terminal

```
npm run dev
```

1. Your Coding Agent will automatically connect to the running Next.js instance via `next-devtools-mcp`
2. Open your application in the browser to view pages
3. Query your agent for insights and diagnostics (see examples below)

### Available tools

Through `next-devtools-mcp`, agents can use the following tools:

- **get_errors**: Retrieve current build errors, runtime errors, and type errors from your dev server
- **get_logs**: Get the path to the development log file containing browser console logs and server output
- **get_page_metadata**: Get metadata about specific pages including routes, components, and rendering information
- **get_project_metadata**: Retrieve project structure, configuration, and dev server URL
- **get_server_action_by_id**: Look up Server Actions by their ID to find the source file and function name

## Using with agents

MCP-compatible Coding Agents can automatically discover and connect to your Next.js development server, providing them with rich context about your project.

### Benefits for agent-assisted development

Agents can:

- **Make context-aware suggestions**: Recommend the right place to add new features based on your existing structure
- **Query live application state**: Check current configuration, routes, and middleware during development
- **Understand your app router pages layout**: Know exactly which page and layout are rendered
- **Provide accurate implementations**: Generate code that follows your project's patterns and conventions

## Examples

### Error detection and diagnosis

Ask your agent about errors in real-time:

```
User: "What errors are currently in my application?"
```

The agent will:

- Query your running Next.js application via `next-devtools-mcp`
- Retrieve current build errors, runtime errors, and type errors
- Analyze the errors and provide actionable fixes

 Agent response (click to expand)

```
> fix errors on the page

⏺ I'll help you fix the errors on the page. Let me first check what errors exist by looking at the
  current state of the project.

⏺ next-devtools - nextjs_runtime (MCP)(action: "discover_servers")
⏺ next-devtools - nextjs_runtime (MCP)(action: "call_tool", toolName: "get_errors")

⏺ I found a hydration error on the /about page. The error shows that the server is rendering
  "server" but the client is rendering "client", causing a mismatch. Let me create a todo list and fix
   this issue.

⏺ Perfect! Now let me check for errors on the page.           01:14 PM  claude-sonnet-4-5-20250929

⏺ next-devtools - nextjs_runtime (MCP)(action: "call_tool", toolName: "get_errors")
  ⎿ {
      "success": true,
      "port": 3000,
      "toolName": "get_errors",
      "result": {
        "content": [
          {
            "type": "text",
            "text": "# Found errors in 1 browser session(s)\n\n## Session: /about\n\n**1 error(s)
     found**\n\n### Runtime Errors\n\n#### Error 1 (Type: recoverable)\n\n**Error**: Hydration failed
```

### Upgrading and best practices

Get help with Next.js concepts and migrations:

```
User: "Help me upgrade my Next.js app to version 16"
```

The agent will analyze your current version, guide you through automated migrations with codemods, and provide step-by-step instructions for handling breaking changes.

Ask conceptual questions:

```
User: "When should I use 'use client' in App Router?"
```

The agent will query the Next.js knowledge base and provide documentation-backed explanations with examples from your codebase.

## How it works

Next.js 16+ includes a built-in MCP endpoint at `/_next/mcp` that runs within your development server. The `next-devtools-mcp` package automatically discovers and communicates with these endpoints, allowing it to:

- Connect to multiple Next.js instances running on different ports
- Forward tool calls to the appropriate Next.js dev server
- Provide a unified interface for coding agents

This architecture decouples the agent interface from the internal implementation, enabling `next-devtools-mcp` to work seamlessly across different Next.js projects.

## Troubleshooting

### MCP server not connecting

- Ensure you're using Next.js v16 or above
- Verify `next-devtools-mcp` is configured in your `.mcp.json`
- Start your development server: `npm run dev`
- Restart your development server if it was already running
- Check that your coding agent has loaded the MCP server configuration

Was this helpful?

supported.
