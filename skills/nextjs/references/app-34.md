# How to set up instrumentation with OpenTelemetry and more

# How to set up instrumentation with OpenTelemetry

> Learn how to instrument your Next.js app with OpenTelemetry.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)OpenTelemetry

# How to set up instrumentation with OpenTelemetry

Last updated  September 3, 2025

Observability is crucial for understanding and optimizing the behavior and performance of your Next.js app.

As applications become more complex, it becomes increasingly difficult to identify and diagnose issues that may arise. By leveraging observability tools, such as logging and metrics, developers can gain insights into their application's behavior and identify areas for optimization. With observability, developers can proactively address issues before they become major problems and provide a better user experience. Therefore, it is highly recommended to use observability in your Next.js applications to improve performance, optimize resources, and enhance user experience.

We recommend using OpenTelemetry for instrumenting your apps.
It's a platform-agnostic way to instrument apps that allows you to change your observability provider without changing your code.
Read [Official OpenTelemetry docs](https://opentelemetry.io/docs/) for more information about OpenTelemetry and how it works.

This documentation uses terms like *Span*, *Trace* or *Exporter* throughout this doc, all of which can be found in [the OpenTelemetry Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/).

Next.js supports OpenTelemetry instrumentation out of the box, which means that we already instrumented Next.js itself.

## Getting Started

OpenTelemetry is extensible but setting it up properly can be quite verbose.
That's why we prepared a package `@vercel/otel` that helps you get started quickly.

### Using@vercel/otel

To get started, install the following packages:

 Terminal

```
npm install @vercel/otel @opentelemetry/sdk-logs @opentelemetry/api-logs @opentelemetry/instrumentation
```

Next, create a custom [instrumentation.ts](https://nextjs.org/docs/app/guides/instrumentation) (or `.js`) file in the **root directory** of the project (or inside `src` folder if using one):

   your-project/instrumentation.tsJavaScriptTypeScript

```
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel({ serviceName: 'next-app' })
}
```

See the [@vercel/oteldocumentation](https://www.npmjs.com/package/@vercel/otel) for additional configuration options.

> **Good to know**:
>
>
>
> - The `instrumentation` file should be in the root of your project and not inside the `app` or `pages` directory. If you're using the `src` folder, then place the file inside `src` alongside `pages` and `app`.
> - If you use the [pageExtensionsconfig option](https://nextjs.org/docs/app/api-reference/config/next-config-js/pageExtensions) to add a suffix, you will also need to update the `instrumentation` filename to match.
> - We have created a basic [with-opentelemetry](https://github.com/vercel/next.js/tree/canary/examples/with-opentelemetry) example that you can use.

### Manual OpenTelemetry configuration

The `@vercel/otel` package provides many configuration options and should serve most of common use cases. But if it doesn't suit your needs, you can configure OpenTelemetry manually.

Firstly you need to install OpenTelemetry packages:

 Terminal

```
npm install @opentelemetry/sdk-node @opentelemetry/resources @opentelemetry/semantic-conventions @opentelemetry/sdk-trace-node @opentelemetry/exporter-trace-otlp-http
```

Now you can initialize `NodeSDK` in your `instrumentation.ts`.
Unlike `@vercel/otel`, `NodeSDK` is not compatible with edge runtime, so you need to make sure that you are importing them only when `process.env.NEXT_RUNTIME === 'nodejs'`. We recommend creating a new file `instrumentation.node.ts` which you conditionally import only when using node:

 instrumentation.tsJavaScriptTypeScript

```
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation.node.ts')
  }
}
```

   instrumentation.node.tsJavaScriptTypeScript

```
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { resourceFromAttributes } from '@opentelemetry/resources'
import { NodeSDK } from '@opentelemetry/sdk-node'
import { SimpleSpanProcessor } from '@opentelemetry/sdk-trace-node'
import { ATTR_SERVICE_NAME } from '@opentelemetry/semantic-conventions'

const sdk = new NodeSDK({
  resource: resourceFromAttributes({
    [ATTR_SERVICE_NAME]: 'next-app',
  }),
  spanProcessor: new SimpleSpanProcessor(new OTLPTraceExporter()),
})
sdk.start()
```

Doing this is equivalent to using `@vercel/otel`, but it's possible to modify and extend some features that are not exposed by the `@vercel/otel`. If edge runtime support is necessary, you will have to use `@vercel/otel`.

## Testing your instrumentation

You need an OpenTelemetry collector with a compatible backend to test OpenTelemetry traces locally.
We recommend using our [OpenTelemetry dev environment](https://github.com/vercel/opentelemetry-collector-dev-setup).

If everything works well you should be able to see the root server span labeled as `GET /requested/pathname`.
All other spans from that particular trace will be nested under it.

Next.js traces more spans than are emitted by default.
To see more spans, you must set `NEXT_OTEL_VERBOSE=1`.

## Deployment

### Using OpenTelemetry Collector

When you are deploying with OpenTelemetry Collector, you can use `@vercel/otel`.
It will work both on Vercel and when self-hosted.

#### Deploying on Vercel

We made sure that OpenTelemetry works out of the box on Vercel.

Follow [Vercel documentation](https://vercel.com/docs/concepts/observability/otel-overview/quickstart) to connect your project to an observability provider.

#### Self-hosting

Deploying to other platforms is also straightforward. You will need to spin up your own OpenTelemetry Collector to receive and process the telemetry data from your Next.js app.

To do this, follow the [OpenTelemetry Collector Getting Started guide](https://opentelemetry.io/docs/collector/getting-started/), which will walk you through setting up the collector and configuring it to receive data from your Next.js app.

Once you have your collector up and running, you can deploy your Next.js app to your chosen platform following their respective deployment guides.

### Custom Exporters

OpenTelemetry Collector is not necessary. You can use a custom OpenTelemetry exporter with [@vercel/otel](#using-vercelotel) or [manual OpenTelemetry configuration](#manual-opentelemetry-configuration).

## Custom Spans

You can add a custom span with [OpenTelemetry APIs](https://opentelemetry.io/docs/instrumentation/js/instrumentation).

 Terminal

```
npm install @opentelemetry/api
```

The following example demonstrates a function that fetches GitHub stars and adds a custom `fetchGithubStars` span to track the fetch request's result:

```
import { trace } from '@opentelemetry/api'

export async function fetchGithubStars() {
  return await trace
    .getTracer('nextjs-example')
    .startActiveSpan('fetchGithubStars', async (span) => {
      try {
        return await getValue()
      } finally {
        span.end()
      }
    })
}
```

The `register` function will execute before your code runs in a new environment.
You can start creating new spans, and they should be correctly added to the exported trace.

## Default Spans in Next.js

Next.js automatically instruments several spans for you to provide useful insights into your application's performance.

Attributes on spans follow [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/). We also add some custom attributes under the `next` namespace:

- `next.span_name` - duplicates span name
- `next.span_type` - each span type has a unique identifier
- `next.route` - The route pattern of the request (e.g., `/[param]/user`).
- `next.rsc` (true/false) - Whether the request is an RSC request, such as prefetch.
- `next.page`
  - This is an internal value used by an app router.
  - You can think about it as a route to a special file (like `page.ts`, `layout.ts`, `loading.ts` and others)
  - It can be used as a unique identifier only when paired with `next.route` because `/layout` can be used to identify both `/(groupA)/layout.ts` and `/(groupB)/layout.ts`

### [http.method] [next.route]

- `next.span_type`: `BaseServer.handleRequest`

This span represents the root span for each incoming request to your Next.js application. It tracks the HTTP method, route, target, and status code of the request.

Attributes:

- [Common HTTP attributes](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/http/#common-attributes)
  - `http.method`
  - `http.status_code`
- [Server HTTP attributes](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/http/#http-server-semantic-conventions)
  - `http.route`
  - `http.target`
- `next.span_name`
- `next.span_type`
- `next.route`

### render route (app) [next.route]

- `next.span_type`: `AppRender.getBodyResult`.

This span represents the process of rendering a route in the app router.

Attributes:

- `next.span_name`
- `next.span_type`
- `next.route`

### fetch [http.method] [http.url]

- `next.span_type`: `AppRender.fetch`

This span represents the fetch request executed in your code.

Attributes:

- [Common HTTP attributes](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/http/#common-attributes)
  - `http.method`
- [Client HTTP attributes](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/http/#http-client)
  - `http.url`
  - `net.peer.name`
  - `net.peer.port` (only if specified)
- `next.span_name`
- `next.span_type`

This span can be turned off by setting `NEXT_OTEL_FETCH_DISABLED=1` in your environment. This is useful when you want to use a custom fetch instrumentation library.

### executing api route (app) [next.route]

- `next.span_type`: `AppRouteRouteHandlers.runHandler`.

This span represents the execution of an API Route Handler in the app router.

Attributes:

- `next.span_name`
- `next.span_type`
- `next.route`

### getServerSideProps [next.route]

- `next.span_type`: `Render.getServerSideProps`.

This span represents the execution of `getServerSideProps` for a specific route.

Attributes:

- `next.span_name`
- `next.span_type`
- `next.route`

### getStaticProps [next.route]

- `next.span_type`: `Render.getStaticProps`.

This span represents the execution of `getStaticProps` for a specific route.

Attributes:

- `next.span_name`
- `next.span_type`
- `next.route`

### render route (pages) [next.route]

- `next.span_type`: `Render.renderDocument`.

This span represents the process of rendering the document for a specific route.

Attributes:

- `next.span_name`
- `next.span_type`
- `next.route`

### generateMetadata [next.page]

- `next.span_type`: `ResolveMetadata.generateMetadata`.

This span represents the process of generating metadata for a specific page (a single route can have multiple of these spans).

Attributes:

- `next.span_name`
- `next.span_type`
- `next.page`

### resolve page components

- `next.span_type`: `NextNodeServer.findPageComponents`.

This span represents the process of resolving page components for a specific page.

Attributes:

- `next.span_name`
- `next.span_type`
- `next.route`

### resolve segment modules

- `next.span_type`: `NextNodeServer.getLayoutOrPageModule`.

This span represents loading of code modules for a layout or a page.

Attributes:

- `next.span_name`
- `next.span_type`
- `next.segment`

### start response

- `next.span_type`: `NextNodeServer.startResponse`.

This zero-length span represents the time when the first byte has been sent in the response.

Was this helpful?

supported.

---

# Optimizing package bundling

> Learn how to analyze and optimize your application's server and client bundles with the Next.js Bundle Analyzer for Turbopack, and the `@next/bundle-analyzer` plugin for Webpack.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Package Bundling

# Optimizing package bundling

Last updated  December 19, 2025

Bundling is the process of combining your application code and its dependencies into optimized output files for the client and server. Smaller bundles load faster, reduce JavaScript execution time, improve [Core Web Vitals](https://web.dev/articles/vitals), and lower server cold start times.

Next.js automatically optimizes bundles by code splitting, tree-shaking, and other techniques. However, there are some cases where you may need to optimize your bundles manually.

There are two tools for analyzing your application's bundles:

- [Next.js Bundle Analyzer for Turbopack (experimental)](#nextjs-bundle-analyzer-experimental)
- [@next/bundle-analyzerplugin for Webpack](#nextbundle-analyzer-for-webpack)

This guide will walk you through how to use each tool and how to [optimize large bundles](#optimizing-large-bundles).

## Next.js Bundle Analyzer (Experimental)

> Available in v16.1 and later. You can share feedback in the [dedicated GitHub discussion](https://github.com/vercel/next.js/discussions/86731) and view the demo at [turbopack-bundle-analyzer-demo.vercel.sh](https://turbopack-bundle-analyzer-demo.vercel.sh/).

The Next.js Bundle Analyzer is integrated with Turbopack's module graph. You can inspect server and client modules with precise import tracing, making it easier to find large dependencies. Open the interactive Bundle Analyzer demo to explore the module graph.

### Step 1: Run the Turbopack Bundle Analyzer

To get started, run the following command and open up the interactive view in your browser.

 Terminal

```
npx next experimental-analyze
```

### Step 2: Filter and inspect modules

Within the UI, you can filter by route, environment (client or server), and type (JavaScript, CSS, JSON), or search by file:

 Next.js bundle analyzer UI walkthrough

### Step 3: Trace modules with import chains

The treemap shows each module as a rectangle. Where the size of the module is represented by the area of the rectangle.

Click a module to see its size, inspect its full import chain and see exactly where it’s used in your application:

 ![Next.js Bundle Analyzer import chain view](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fbundle-analyzer.png&w=3840&q=75)![Next.js Bundle Analyzer import chain view](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fbundle-analyzer.png&w=3840&q=75)Next.js Bundle Analyzer import chain view

### Step 4: Write output to disk for sharing or diffing

If you want to share the analysis with teammates or compare bundle sizes before/after optimizations, you can skip the interactive view and save the analysis as a static file with the `--output` flag:

 Terminal

```
npx next experimental-analyze --output
```

This command writes the output to `.next/diagnostics/analyze`. You can copy this directory elsewhere to compare results:

 Terminal

```
cp -r .next/diagnostics/analyze ./analyze-before-refactor
```

> More options are available for the Bundle Analyzer, see Next.js CLI reference docs for the full list.

## @next/bundle-analyzerfor Webpack

The [@next/bundle-analyzer](https://www.npmjs.com/package/@next/bundle-analyzer) is a plugin that helps you manage the size of your application bundles. It generates a visual report of the size of each package and their dependencies. You can use the information to remove large dependencies, split, or [lazy-load](https://nextjs.org/docs/app/guides/lazy-loading) your code.

### Step 1: Installation

Install the plugin by running the following command:

```
npm i @next/bundle-analyzer
# or
yarn add @next/bundle-analyzer
# or
pnpm add @next/bundle-analyzer
```

Then, add the bundle analyzer's settings to your `next.config.js`.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {}

const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer(nextConfig)
```

### Step 2: Generating a report

Run the following command to analyze your bundles:

```
ANALYZE=true npm run build
# or
ANALYZE=true yarn build
# or
ANALYZE=true pnpm build
```

The report will open three new tabs in your browser, which you can inspect.

## Optimizing large bundles

Once you've identified a large module, the solution will depend on your use case. Below are common causes and how to fix them:

### Packages with many exports

If you're using a package that exports hundreds of modules (such as icon and utility libraries), you can optimize how those imports are resolved using the [optimizePackageImports](https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports) option in your `next.config.js` file. This option will only load the modules you *actually* use, while still giving you the convenience of writing import statements with many named exports.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    optimizePackageImports: ['icon-library'],
  },
}

module.exports = nextConfig
```

> **Good to know:** Next.js also optimizes some libraries automatically, thus they do not need to be included in the `optimizePackageImports` list. See the [full list](https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports) of supported packages.

### Heavy client workloads

A common cause of large client bundles is doing expensive rendering work in Client Components. This often happens with libraries that exist only to transform data into UI, such as syntax highlighting, chart rendering, or markdown parsing.

If that work does not require browser APIs or user interaction, it can be run in a Server Component.

In this example, a prism based highlighter runs in a Client Component. Even though the final output is just a `<code>` block, the entire highlighting library is bundled into the client JavaScript bundle:

 app/blog/[slug]/page.tsx

```
'use client'

import Highlight from 'prism-react-renderer'
import theme from 'prism-react-renderer/themes/github'

export default function Page() {
  const code = `export function hello() {
    console.log("hi")
  }`

  return (
    <article>
      <h1>Blog Post Title</h1>

      {/* The prism package and its tokenization logic are shipped to the client */}
      <Highlight code={code} language="tsx" theme={theme}>
        {({ className, style, tokens, getLineProps, getTokenProps }) => (
          <pre className={className} style={style}>
            <code>
              {tokens.map((line, i) => (
                <div key={i} {...getLineProps({ line })}>
                  {line.map((token, key) => (
                    <span key={key} {...getTokenProps({ token })} />
                  ))}
                </div>
              ))}
            </code>
          </pre>
        )}
      </Highlight>
    </article>
  )
}
```

This increases bundle size because the client must download and execute the highlighting library, even though the result is static HTML.

Instead, move the highlighting logic to a Server Component and render the final HTML on the server. The client will only receive the rendered markup.

 app/blog/[slug]/page.tsx

```
import { codeToHtml } from 'shiki'

export default async function Page() {
  const code = `export function hello() {
    console.log("hi")
  }`

  // The Shiki package runs on the server and is never bundled for the client.
  const highlightedHtml = await codeToHtml(code, {
    lang: 'tsx',
    theme: 'github-dark',
  })

  return (
    <article>
      <h1>Blog Post Title</h1>

      {/* Client receives plain markup */}
      <pre>
        <code dangerouslySetInnerHTML={{ __html: highlightedHtml }} />
      </pre>
    </article>
  )
}
```

### Opting specific packages out of bundling

Packages imported inside Server Components and Route Handlers are automatically bundled by Next.js.

You can opt specific packages out of bundling using the [serverExternalPackages](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverExternalPackages) option in your `next.config.js`.

next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  serverExternalPackages: ['package-name'],
}

module.exports = nextConfig
```

 Learn more about optimizing your application for production.[ProductionRecommendations to ensure the best performance and user experience before taking your Next.js application to production.](https://nextjs.org/docs/app/guides/production-checklist)

Was this helpful?

supported.

---

# Prefetching

> Learn how to configure prefetching in Next.js

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Prefetching

# Prefetching

Last updated  October 30, 2025

Prefetching makes navigating between different routes in your application feel instant. Next.js tries to intelligently prefetch by default, based on the links used in your application code.

This guide will explain how prefetching works and show common implementation patterns:

- [Automatic prefetch](#automatic-prefetch)
- [Manual prefetch](#manual-prefetch)
- [Hover-triggered prefetch](#hover-triggered-prefetch)
- [Extending or ejecting link](#extending-or-ejecting-link)
- [Disabled prefetch](#disabled-prefetch)

## How does prefetching work?

When navigating between routes, the browser requests assets for the page like HTML and JavaScript files. Prefetching is the process of fetching these resources *ahead* of time, before you navigate to a new route.

Next.js automatically splits your application into smaller JavaScript chunks based on routes. Instead of loading all the code upfront like traditional SPAs, only the code needed for the current route is loaded. This reduces the initial load time while other parts of the app are loaded in the background. By the time you click the link, the resources for the new route have already been loaded into the browser cache.

When navigating to the new page, there's no full page reload or browser loading spinner. Instead, Next.js performs a [client-side transition](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions), making the page navigation feel instant.

## Prefetching static vs. dynamic routes

|  | Static page | Dynamic page |
| --- | --- | --- |
| Prefetched | Yes, full route | No, unlessloading.js |
| Client Cache TTL | 5 min (default) | Off, unlessenabled |
| Server roundtrip on click | No | Yes, streamed aftershell |

> **Good to know:** During the initial navigation, the browser fetches the HTML, JavaScript, and React Server Components (RSC) Payload. For subsequent navigations, the browser will fetch the RSC Payload for Server Components and JS bundle for Client Components.

## Automatic prefetch

 app/ui/nav-link.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function NavLink() {
  return <Link href="/about">About</Link>
}
```

| Context | Prefetched payload | Client Cache TTL |
| --- | --- | --- |
| Noloading.js | Entire page | Until app reload |
| Withloading.js | Layout to first loading boundary | 30s (configurable) |

Automatic prefetching runs only in production. Disable with `prefetch={false}` or use the wrapper in [Disabled Prefetch](#disabled-prefetch).

## Manual prefetch

To do manual prefetching, import the `useRouter` hook from `next/navigation`, and call `router.prefetch()` to warm routes outside the viewport or in response to analytics, hover, scroll, etc.

```
'use client'

import { useRouter } from 'next/navigation'
import { CustomLink } from '@components/link'

export function PricingCard() {
  const router = useRouter()

  return (
    <div onMouseEnter={() => router.prefetch('/pricing')}>
      {/* other UI elements */}
      <CustomLink href="/pricing">View Pricing</CustomLink>
    </div>
  )
}
```

If the intent is to prefetch a URL when a component loads, see the extending or rejecting a link [example].

## Hover-triggered prefetch

> **Proceed with caution:** Extending `Link` opts you into maintaining prefetching, cache invalidation, and accessibility concerns. Proceed only if defaults are insufficient.

Next.js tries to do the right prefetching by default, but power users can eject and modify based on their needs. You have the control between performance and resource consumption.

For example, you might have to only trigger prefetches on hover, instead of when entering the viewport (the default behavior):

```
'use client'

import Link from 'next/link'
import { useState } from 'react'

export function HoverPrefetchLink({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  const [active, setActive] = useState(false)

  return (
    <Link
      href={href}
      prefetch={active ? null : false}
      onMouseEnter={() => setActive(true)}
    >
      {children}
    </Link>
  )
}
```

`prefetch={null}` restores default (static) prefetching once the user shows intent.

## Extending or ejecting link

You can extend the `<Link>` component to create your own custom prefetching strategy. For example, using the [ForesightJS](https://foresightjs.com/docs/integrations/nextjs) library which prefetches links by predicting the direction of the user's cursor.

Alternatively, you can use [useRouter](https://nextjs.org/docs/app/api-reference/functions/use-router) to recreate some of the native `<Link>` behavior. However, be aware this opts you into maintaining prefetching and cache invalidation.

```
'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

function ManualPrefetchLink({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  const router = useRouter()

  useEffect(() => {
    let cancelled = false
    const poll = () => {
      if (!cancelled) router.prefetch(href, { onInvalidate: poll })
    }
    poll()
    return () => {
      cancelled = true
    }
  }, [href, router])

  return (
    <a
      href={href}
      onClick={(event) => {
        event.preventDefault()
        router.push(href)
      }}
    >
      {children}
    </a>
  )
}
```

[onInvalidate](https://nextjs.org/docs/app/api-reference/functions/use-router#userouter) is invoked when Next.js suspects cached data is stale, allowing you to refresh the prefetch.

> **Good to know:** Using an `a` tag will cause a full page navigation to the destination route, you can use `onClick` to prevent the full page navigation, and then invoke `router.push` to navigate to the destination.

## Disabled prefetch

You can fully disable prefetching for certain routes for more fine-grained control over resource consumption.

```
'use client'

import Link, { LinkProps } from 'next/link'

function NoPrefetchLink({
  prefetch,
  ...rest
}: LinkProps & { children: React.ReactNode }) {
  return <Link {...rest} prefetch={false} />
}
```

For example, you may still want to have consistent usage of `<Link>` in your application, but links in your footer might not need to be prefetched when entering the viewport.

## Prefetching optimizations

### Client cache

Next.js stores prefetched React Server Component payloads in memory, keyed by route segments. When navigating between sibling routes (e.g. `/dashboard/settings` → `/dashboard/analytics`), it reuses the parent layout and only fetches the updated leaf page. This reduces network traffic and improves navigation speed.

### Prefetch scheduling

Next.js maintains a small task queue, which prefetches in the following order:

1. Links in the viewport
2. Links showing user intent (hover or touch)
3. Newer links replace older ones
4. Links scrolled off-screen are discarded

The scheduler prioritizes likely navigations while minimizing unused downloads.

### Partial Prerendering (PPR)

When PPR is enabled, a page is divided into a static shell and a streamed dynamic section:

- The shell, which can be prefetched, streams immediately
- Dynamic data streams when ready
- Data invalidations (`revalidateTag`, `revalidatePath`) silently refresh associated prefetches

## Troubleshooting

### Triggering unwanted side-effects during prefetching

If your layouts or pages are not [pure](https://react.dev/learn/keeping-components-pure#purity-components-as-formulas) and have side-effects (e.g. tracking analytics), these might be triggered when the route is prefetched, not when the user visits the page.

To avoid this, you should move side-effects to a `useEffect` hook or a Server Action triggered from a Client Component.

**Before**:

 app/dashboard/layout.tsxJavaScriptTypeScript

```
import { trackPageView } from '@/lib/analytics'

export default function Layout({ children }: { children: React.ReactNode }) {
  // This runs during prefetch
  trackPageView()

  return <div>{children}</div>
}
```

**After**:

 app/ui/analytics-tracker.tsxJavaScriptTypeScript

```
'use client'

import { useEffect } from 'react'
import { trackPageView } from '@/lib/analytics'

export function AnalyticsTracker() {
  useEffect(() => {
    trackPageView()
  }, [])

  return null
}
```

   app/dashboard/layout.tsxJavaScriptTypeScript

```
import { AnalyticsTracker } from '@/app/ui/analytics-tracker'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <AnalyticsTracker />
      {children}
    </div>
  )
}
```

### Preventing too many prefetches

Next.js automatically prefetches links in the viewport when using the `<Link>` component.

There may be cases where you want to prevent this to avoid unnecessary usage of resources, such as when rendering a large list of links (e.g. an infinite scroll table).

You can disable prefetching by setting the `prefetch` prop of the `<Link>` component to `false`.

 app/ui/no-prefetch-link.tsxJavaScriptTypeScript

```
<Link prefetch={false} href={`/blog/${post.id}`}>
  {post.title}
</Link>
```

However, this means static routes will only be fetched on click, and dynamic routes will wait for the server to render before navigating.

To reduce resource usage without disabling prefetch entirely, you can defer prefetching until the user hovers over a link. This targets only links the user is likely to visit.

 app/ui/hover-prefetch-link.tsxJavaScriptTypeScript

```
'use client'

import Link from 'next/link'
import { useState } from 'react'

export function HoverPrefetchLink({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  const [active, setActive] = useState(false)

  return (
    <Link
      href={href}
      prefetch={active ? null : false}
      onMouseEnter={() => setActive(true)}
    >
      {children}
    </Link>
  )
}
```

Was this helpful?

supported.

---

# How to optimize your Next.js application for production

> Recommendations to ensure the best performance and user experience before taking your Next.js application to production.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Production

# How to optimize your Next.js application for production

Last updated  December 19, 2025

Before taking your Next.js application to production, there are some optimizations and patterns you should consider implementing for the best user experience, performance, and security.

This page provides best practices that you can use as a reference when [building your application](#during-development) and [before going to production](#before-going-to-production), as well as the [automatic Next.js optimizations](#automatic-optimizations) you should be aware of.

## Automatic optimizations

These Next.js optimizations are enabled by default and require no configuration:

- **Server Components:** Next.js uses Server Components by default. Server Components run on the server, and don't require JavaScript to render on the client. As such, they have no impact on the size of your client-side JavaScript bundles. You can then use [Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) as needed for interactivity.
- **Code-splitting:** Server Components enable automatic code-splitting by route segments. You may also consider [lazy loading](https://nextjs.org/docs/app/guides/lazy-loading) Client Components and third-party libraries, where appropriate.
- **Prefetching:** When a link to a new route enters the user's viewport, Next.js prefetches the route in background. This makes navigation to new routes almost instant. You can opt out of prefetching, where appropriate.
- **Static Rendering:** Next.js statically renders Server and Client Components on the server at build time and caches the rendered result to improve your application's performance. You can opt into [Dynamic Rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) for specific routes, where appropriate.
- **Caching:** Next.js caches data requests, the rendered result of Server and Client Components, static assets, and more, to reduce the number of network requests to your server, database, and backend services. You may opt out of caching, where appropriate.

These defaults aim to improve your application's performance, and reduce the cost and amount of data transferred on each network request.

## During development

While building your application, we recommend using the following features to ensure the best performance and user experience:

### Routing and rendering

- **Layouts:** Use layouts to share UI across pages and enable [partial rendering](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions) on navigation.
- **<Link>component:** Use the `<Link>` component for [client-side navigation and prefetching](https://nextjs.org/docs/app/getting-started/linking-and-navigating#how-navigation-works).
- **Error Handling:** Gracefully handle [catch-all errors](https://nextjs.org/docs/app/getting-started/error-handling) and [404 errors](https://nextjs.org/docs/app/api-reference/file-conventions/not-found) in production by creating custom error pages.
- **Client and Server Components:** Follow the recommended composition patterns for Server and Client Components, and check the placement of your ["use client"boundaries](https://nextjs.org/docs/app/getting-started/server-and-client-components#examples#moving-client-components-down-the-tree) to avoid unnecessarily increasing your client-side JavaScript bundle.
- **Dynamic APIs:** Be aware that Dynamic APIs like [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies) and the [searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page#searchparams-optional) prop will opt the entire route into [Dynamic Rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) (or your whole application if used in the [Root Layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout)). Ensure Dynamic API usage is intentional and wrap them in `<Suspense>` boundaries where appropriate.

> **Good to know**: [Partial Prerendering (experimental)](https://nextjs.org/blog/next-14#partial-prerendering-preview) will allow parts of a route to be dynamic without opting the whole route into dynamic rendering.

### Data fetching and caching

- **Server Components:** Leverage the benefits of fetching data on the server using Server Components.
- **Route Handlers:** Use Route Handlers to access your backend resources from Client Components. But do not call Route Handlers from Server Components to avoid an additional server request.
- **Streaming:** Use Loading UI and React Suspense to progressively send UI from the server to the client, and prevent the whole route from blocking while data is being fetched.
- **Parallel Data Fetching:** Reduce network waterfalls by fetching data in parallel, where appropriate. Also, consider [preloading data](https://nextjs.org/docs/app/getting-started/fetching-data#preloading-data) where appropriate.
- **Data Caching:** Verify whether your data requests are being cached or not, and opt into caching, where appropriate. Ensure requests that don't use `fetch` are [cached](https://nextjs.org/docs/app/api-reference/functions/unstable_cache).
- **Static Images:** Use the `public` directory to automatically cache your application's static assets, e.g. images.

### UI and accessibility

- **Forms and Validation:** Use Server Actions to handle form submissions, server-side validation, and handle errors.
- **Global Error UI:** Add `app/global-error.tsx` to provide consistent, accessible fallback UI and recovery for uncaught errors across your app.
- **Global 404:** Add `app/global-not-found.tsx` to serve an accessible 404 for unmatched routes across your app.

- **Font Module:** Optimize fonts by using the Font Module, which automatically hosts your font files with other static assets, removes external network requests, and reduces [layout shift](https://web.dev/articles/cls).
- **<Image>Component:** Optimize images by using the Image Component, which automatically optimizes images, prevents layout shift, and serves them in modern formats like WebP.
- **<Script>Component:** Optimize third-party scripts by using the Script Component, which automatically defers scripts and prevents them from blocking the main thread.
- **ESLint:** Use the built-in `eslint-plugin-jsx-a11y` plugin to catch accessibility issues early.

### Security

- **Tainting:** Prevent sensitive data from being exposed to the client by tainting data objects and/or specific values.
- **Server Actions:** Ensure users are authorized to call Server Actions. Review the recommended [security practices](https://nextjs.org/blog/security-nextjs-server-components-actions).

- **Environment Variables:** Ensure your `.env.*` files are added to `.gitignore` and only public variables are prefixed with `NEXT_PUBLIC_`.
- **Content Security Policy:** Consider adding a Content Security Policy to protect your application against various security threats such as cross-site scripting, clickjacking, and other code injection attacks.

### Metadata and SEO

- **Metadata API:** Use the Metadata API to improve your application's Search Engine Optimization (SEO) by adding page titles, descriptions, and more.
- **Open Graph (OG) images:** Create OG images to prepare your application for social sharing.
- **SitemapsandRobots:** Help Search Engines crawl and index your pages by generating sitemaps and robots files.

### Type safety

- **TypeScript andTS Plugin:** Use TypeScript and the TypeScript plugin for better type-safety, and to help you catch errors early.

## Before going to production

Before going to production, you can run `next build` to build your application locally and catch any build errors, then run `next start` to measure the performance of your application in a production-like environment.

### Core Web Vitals

- **Lighthouse:** Run lighthouse in incognito to gain a better understanding of how your users will experience your site, and to identify areas for improvement. This is a simulated test and should be paired with looking at field data (such as Core Web Vitals).

- **useReportWebVitalshook:** Use this hook to send [Core Web Vitals](https://web.dev/articles/vitals) data to analytics tools.

### Analyzing bundles

Use the [@next/bundle-analyzerplugin](https://nextjs.org/docs/app/guides/package-bundling#nextbundle-analyzer-for-webpack) to analyze the size of your JavaScript bundles and identify large modules and dependencies that might be impacting your application's performance.

Additionally, the following tools can help you understand the impact of adding new dependencies to your application:

- [Import Cost](https://marketplace.visualstudio.com/items?itemName=wix.vscode-import-cost)
- [Package Phobia](https://packagephobia.com/)
- [Bundle Phobia](https://bundlephobia.com/)
- [bundlejs](https://bundlejs.com/)

Was this helpful?

supported.
