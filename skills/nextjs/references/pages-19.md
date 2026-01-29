# How to instrument your Next.js app with OpenTelemetry and more

# How to instrument your Next.js app with OpenTelemetry

> Learn how to instrument your Next.js app with OpenTelemetry.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)OpenTelemetryYou are currently viewing the documentation for Pages Router.

# How to instrument your Next.js app with OpenTelemetry

Last updated  April 24, 2025

Observability is crucial for understanding and optimizing the behavior and performance of your Next.js app.

As applications become more complex, it becomes increasingly difficult to identify and diagnose issues that may arise. By leveraging observability tools, such as logging and metrics, developers can gain insights into their application's behavior and identify areas for optimization. With observability, developers can proactively address issues before they become major problems and provide a better user experience. Therefore, it is highly recommended to use observability in your Next.js applications to improve performance, optimize resources, and enhance user experience.

We recommend using OpenTelemetry for instrumenting your apps.
It's a platform-agnostic way to instrument apps that allows you to change your observability provider without changing your code.
Read [Official OpenTelemetry docs](https://opentelemetry.io/docs/) for more information about OpenTelemetry and how it works.

This documentation uses terms like *Span*, *Trace* or *Exporter* throughout this doc, all of which can be found in [the OpenTelemetry Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/).

Next.js supports OpenTelemetry instrumentation out of the box, which means that we already instrumented Next.js itself.

When you enable OpenTelemetry we will automatically wrap all your code like
`getStaticProps` in *spans* with helpful attributes.

## Getting Started

OpenTelemetry is extensible but setting it up properly can be quite verbose.
That's why we prepared a package `@vercel/otel` that helps you get started quickly.

### Using@vercel/otel

To get started, install the following packages:

 Terminal

```
npm install @vercel/otel @opentelemetry/sdk-logs @opentelemetry/api-logs @opentelemetry/instrumentation
```

Next, create a custom [instrumentation.ts](https://nextjs.org/docs/pages/guides/instrumentation) (or `.js`) file in the **root directory** of the project (or inside `src` folder if using one):

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
> - If you use the [pageExtensionsconfig option](https://nextjs.org/docs/pages/api-reference/config/next-config-js/pageExtensions) to add a suffix, you will also need to update the `instrumentation` filename to match.
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

# How to optimize package bundling

> Learn how to optimize your application's server and client bundles.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Package BundlingYou are currently viewing the documentation for Pages Router.

# How to optimize package bundling

Last updated  April 24, 2025

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

### External packages that aren't pre-bundled

By default, packages imported into your application are not bundled. This can impact performance if external packages are not pre-bundled, for example, if imported from a monorepo or `node_modules`.

To bundle specific packages, you can use the [transpilePackages](https://nextjs.org/docs/app/api-reference/config/next-config-js/transpilePackages) option in your `next.config.js`.

next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['package-name'],
}

module.exports = nextConfig
```

To automatically bundle all packages, you can use the [bundlePagesRouterDependencies](https://nextjs.org/docs/pages/api-reference/config/next-config-js/bundlePagesRouterDependencies) option in your `next.config.js`.

next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  bundlePagesRouterDependencies: true,
}

module.exports = nextConfig
```

### Opting specific packages out of bundling

If you identify packages that shouldn't be in the bundle, you can opt specific packages out of automatic bundling using the [serverExternalPackages](https://nextjs.org/docs/pages/api-reference/config/next-config-js/serverExternalPackages) option in your `next.config.js`:

next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Automatically bundle external packages:
  bundlePagesRouterDependencies: true,
  // Opt specific packages out of bundling:
  serverExternalPackages: ['package-name'],
}

module.exports = nextConfig
```

Learn more about optimizing your application for production.[ProductionRecommendations to ensure the best performance and user experience before taking your Next.js application to production.](https://nextjs.org/docs/pages/guides/production-checklist)

Was this helpful?

supported.

---

# How to configure PostCSS in Next.js

> Extend the PostCSS config and plugins added by Next.js with your own.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)PostCSSYou are currently viewing the documentation for Pages Router.

# How to configure PostCSS in Next.js

Last updated  May 12, 2025

## Default Behavior

Next.js compiles CSS for its [built-in CSS support](https://nextjs.org/docs/app/getting-started/css) using PostCSS.

Out of the box, with no configuration, Next.js compiles CSS with the following transformations:

- [Autoprefixer](https://github.com/postcss/autoprefixer) automatically adds vendor prefixes to CSS rules (back to IE11).
- [Cross-browser Flexbox bugs](https://github.com/philipwalton/flexbugs) are corrected to behave like [the spec](https://www.w3.org/TR/css-flexbox-1/).
- New CSS features are automatically compiled for Internet Explorer 11 compatibility:
  - [allProperty](https://developer.mozilla.org/docs/Web/CSS/all)
  - [Break Properties](https://developer.mozilla.org/docs/Web/CSS/break-after)
  - [font-variantProperty](https://developer.mozilla.org/docs/Web/CSS/font-variant)
  - [Gap Properties](https://developer.mozilla.org/docs/Web/CSS/gap)
  - [Media Query Ranges](https://developer.mozilla.org/docs/Web/CSS/Media_Queries/Using_media_queries#Syntax_improvements_in_Level_4)

By default, [CSS Grid](https://www.w3.org/TR/css-grid-1/) and [Custom Properties](https://developer.mozilla.org/docs/Web/CSS/var) (CSS variables) are **not compiled** for IE11 support.

To compile [CSS Grid Layout](https://developer.mozilla.org/docs/Web/CSS/grid) for IE11, you can place the following comment at the top of your CSS file:

```
/* autoprefixer grid: autoplace */
```

You can also enable IE11 support for [CSS Grid Layout](https://developer.mozilla.org/docs/Web/CSS/grid)
in your entire project by configuring autoprefixer with the configuration shown below (collapsed).
See ["Customizing Plugins"](#customizing-plugins) below for more information.

 Click to view the configuration to enable CSS Grid Layoutpostcss.config.json

```
{
  "plugins": [
    "postcss-flexbugs-fixes",
    [
      "postcss-preset-env",
      {
        "autoprefixer": {
          "flexbox": "no-2009",
          "grid": "autoplace"
        },
        "stage": 3,
        "features": {
          "custom-properties": false
        }
      }
    ]
  ]
}
```

CSS variables are not compiled because it is [not possible to safely do so](https://github.com/MadLittleMods/postcss-css-variables#caveats).
If you must use variables, consider using something like [Sass variables](https://sass-lang.com/documentation/variables) which are compiled away by [Sass](https://sass-lang.com/).

## Customizing Target Browsers

Next.js allows you to configure the target browsers (for [Autoprefixer](https://github.com/postcss/autoprefixer) and compiled css features) through [Browserslist](https://github.com/browserslist/browserslist).

To customize browserslist, create a `browserslist` key in your `package.json` like so:

 package.json

```
{
  "browserslist": [">0.3%", "not dead", "not op_mini all"]
}
```

You can use the [browsersl.ist](https://browsersl.ist/?q=%3E0.3%25%2C+not+ie+11%2C+not+dead%2C+not+op_mini+all) tool to visualize what browsers you are targeting.

## CSS Modules

No configuration is needed to support CSS Modules. To enable CSS Modules for a file, rename the file to have the extension `.module.css`.

You can learn more about [Next.js' CSS Module support here](https://nextjs.org/docs/app/getting-started/css).

## Customizing Plugins

> **Warning**: When you define a custom PostCSS configuration file, Next.js **completely disables** the [default behavior](#default-behavior).
> Be sure to manually configure all the features you need compiled, including [Autoprefixer](https://github.com/postcss/autoprefixer).
> You also need to install any plugins included in your custom configuration manually, i.e. `npm install postcss-flexbugs-fixes postcss-preset-env`.

To customize the PostCSS configuration, create a `postcss.config.json` file in the root of your project.

This is the default configuration used by Next.js:

 postcss.config.json

```
{
  "plugins": [
    "postcss-flexbugs-fixes",
    [
      "postcss-preset-env",
      {
        "autoprefixer": {
          "flexbox": "no-2009"
        },
        "stage": 3,
        "features": {
          "custom-properties": false
        }
      }
    ]
  ]
}
```

> **Good to know**: Next.js also allows the file to be named `.postcssrc.json`, or, to be read from the `postcss` key in `package.json`.

It is also possible to configure PostCSS with a `postcss.config.js` file, which is useful when you want to conditionally include plugins based on environment:

 postcss.config.js

```
module.exports = {
  plugins:
    process.env.NODE_ENV === 'production'
      ? [
          'postcss-flexbugs-fixes',
          [
            'postcss-preset-env',
            {
              autoprefixer: {
                flexbox: 'no-2009',
              },
              stage: 3,
              features: {
                'custom-properties': false,
              },
            },
          ],
        ]
      : [
          // No transformations in development
        ],
}
```

> **Good to know**: Next.js also allows the file to be named `.postcssrc.js`.

Do **not userequire()** to import the PostCSS Plugins. Plugins must be provided as strings.

> **Good to know**: If your `postcss.config.js` needs to support other non-Next.js tools in the same project, you must use the interoperable object-based format instead:
>
>
>
> ```
> module.exports = {
>   plugins: {
>     'postcss-flexbugs-fixes': {},
>     'postcss-preset-env': {
>       autoprefixer: {
>         flexbox: 'no-2009',
>       },
>       stage: 3,
>       features: {
>         'custom-properties': false,
>       },
>     },
>   },
> }
> ```

Was this helpful?

supported.

---

# How to preview content with Preview Mode in Next.js

> Next.js has the preview mode for statically generated pages. You can learn how it works here.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Preview ModeYou are currently viewing the documentation for Pages Router.

# How to preview content with Preview Mode in Next.js

This is a legacy API and no longer recommended. It's still supported for backward compatibility.Last updated  May 21, 2025

> **Note**: This feature is superseded by [Draft Mode](https://nextjs.org/docs/pages/guides/draft-mode).

 Examples

- [Agility CMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-agilitycms) ([Demo](https://next-blog-agilitycms.vercel.app/))
- [Builder.io Example](https://github.com/vercel/next.js/tree/canary/examples/cms-builder-io) ([Demo](https://cms-builder-io.vercel.app/))
- [ButterCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-buttercms) ([Demo](https://next-blog-buttercms.vercel.app/))
- [Contentful Example](https://github.com/vercel/next.js/tree/canary/examples/cms-contentful) ([Demo](https://app-router-contentful.vercel.app/))
- [Cosmic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-cosmic) ([Demo](https://next-blog-cosmic.vercel.app/))
- [DatoCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-datocms) ([Demo](https://next-blog-datocms.vercel.app/))
- [DotCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-dotcms) ([Demo](https://nextjs-dotcms-blog.vercel.app/))
- [Drupal Example](https://github.com/vercel/next.js/tree/canary/examples/cms-drupal) ([Demo](https://cms-drupal.vercel.app/))
- [Enterspeed Example](https://github.com/vercel/next.js/tree/canary/examples/cms-enterspeed) ([Demo](https://next-blog-demo.enterspeed.com/))
- [GraphCMS Example](https://github.com/vercel/next.js/tree/canary/examples/cms-graphcms) ([Demo](https://next-blog-graphcms.vercel.app/))
- [Keystone Example](https://github.com/vercel/next.js/tree/canary/examples/cms-keystonejs-embedded) ([Demo](https://nextjs-keystone-demo.vercel.app/))
- [Kontent.ai Example](https://github.com/vercel/next.js/tree/canary/examples/cms-kontent-ai) ([Demo](https://next-blog-kontent-ai.vercel.app/))
- [Makeswift Example](https://github.com/vercel/next.js/tree/canary/examples/cms-makeswift) ([Demo](https://nextjs-makeswift-example.vercel.app/))
- [Plasmic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-plasmic) ([Demo](https://nextjs-plasmic-example.vercel.app/))
- [Prepr Example](https://github.com/vercel/next.js/tree/canary/examples/cms-prepr) ([Demo](https://next-blog-prepr.vercel.app/))
- [Prismic Example](https://github.com/vercel/next.js/tree/canary/examples/cms-prismic) ([Demo](https://next-blog-prismic.vercel.app/))
- [Sanity Example](https://github.com/vercel/next.js/tree/canary/examples/cms-sanity) ([Demo](https://next-blog.sanity.build/))
- [Sitecore XM Cloud Example](https://github.com/vercel/next.js/tree/canary/examples/cms-sitecore-xmcloud) ([Demo](https://vercel-sitecore-xmcloud-demo.vercel.app/))
- [Storyblok Example](https://github.com/vercel/next.js/tree/canary/examples/cms-storyblok) ([Demo](https://next-blog-storyblok.vercel.app/))
- [Strapi Example](https://github.com/vercel/next.js/tree/canary/examples/cms-strapi) ([Demo](https://next-blog-strapi.vercel.app/))
- [TakeShape Example](https://github.com/vercel/next.js/tree/canary/examples/cms-takeshape) ([Demo](https://next-blog-takeshape.vercel.app/))
- [Tina Example](https://github.com/vercel/next.js/tree/canary/examples/cms-tina) ([Demo](https://cms-tina-example.vercel.app/))
- [Umbraco Example](https://github.com/vercel/next.js/tree/canary/examples/cms-umbraco) ([Demo](https://nextjs-umbraco-sample-blog.vercel.app/))
- [Umbraco Heartcore Example](https://github.com/vercel/next.js/tree/canary/examples/cms-umbraco-heartcore) ([Demo](https://next-blog-umbraco-heartcore.vercel.app/))
- [Webiny Example](https://github.com/vercel/next.js/tree/canary/examples/cms-webiny) ([Demo](https://webiny-headlesscms-nextjs-example.vercel.app/))
- [WordPress Example](https://github.com/vercel/next.js/tree/canary/examples/cms-wordpress) ([Demo](https://next-blog-wordpress.vercel.app/))
- [Blog Starter Example](https://github.com/vercel/next.js/tree/canary/examples/blog-starter) ([Demo](https://next-blog-starter.vercel.app/))

In the [Pages documentation](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts) and the [Data Fetching documentation](https://nextjs.org/docs/pages/building-your-application/data-fetching), we talked about how to pre-render a page at build time (**Static Generation**) using `getStaticProps` and `getStaticPaths`.

Static Generation is useful when your pages fetch data from a headless CMS. However, it’s not ideal when you’re writing a draft on your headless CMS and want to **preview** the draft immediately on your page. You’d want Next.js to render these pages at **request time** instead of build time and fetch the draft content instead of the published content. You’d want Next.js to bypass Static Generation only for this specific case.

Next.js has a feature called **Preview Mode** which solves this problem. Here are instructions on how to use it.

## Step 1: Create and access a preview API route

> Take a look at the [API Routes documentation](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) first if you’re not familiar with Next.js API Routes.

First, create a **preview API route**. It can have any name - e.g. `pages/api/preview.js` (or `.ts` if using TypeScript).

In this API route, you need to call `setPreviewData` on the response object. The argument for `setPreviewData` should be an object, and this can be used by `getStaticProps` (more on this later). For now, we’ll use `{}`.

```
export default function handler(req, res) {
  // ...
  res.setPreviewData({})
  // ...
}
```

`res.setPreviewData` sets some **cookies** on the browser which turns on the preview mode. Any requests to Next.js containing these cookies will be considered as the **preview mode**, and the behavior for statically generated pages will change (more on this later).

You can test this manually by creating an API route like below and accessing it from your browser manually:

 pages/api/preview.js

```
// simple example for testing it manually from your browser.
export default function handler(req, res) {
  res.setPreviewData({})
  res.end('Preview mode enabled')
}
```

If you open your browser’s developer tools and visit `/api/preview`, you’ll notice that the `__prerender_bypass` and `__next_preview_data` cookies will be set on this request.

### Securely accessing it from your Headless CMS

In practice, you’d want to call this API route *securely* from your headless CMS. The specific steps will vary depending on which headless CMS you’re using, but here are some common steps you could take.

These steps assume that the headless CMS you’re using supports setting **custom preview URLs**. If it doesn’t, you can still use this method to secure your preview URLs, but you’ll need to construct and access the preview URL manually.

**First**, you should create a **secret token string** using a token generator of your choice. This secret will only be known by your Next.js app and your headless CMS. This secret prevents people who don’t have access to your CMS from accessing preview URLs.

**Second**, if your headless CMS supports setting custom preview URLs, specify the following as the preview URL. This assumes that your preview API route is located at `pages/api/preview.js`.

 Terminal

```
https://<your-site>/api/preview?secret=<token>&slug=<path>
```

- `<your-site>` should be your deployment domain.
- `<token>` should be replaced with the secret token you generated.
- `<path>` should be the path for the page that you want to preview. If you want to preview `/posts/foo`, then you should use `&slug=/posts/foo`.

Your headless CMS might allow you to include a variable in the preview URL so that `<path>` can be set dynamically based on the CMS’s data like so: `&slug=/posts/{entry.fields.slug}`

**Finally**, in the preview API route:

- Check that the secret matches and that the `slug` parameter exists (if not, the request should fail).
-
- Call `res.setPreviewData`.
- Then redirect the browser to the path specified by `slug`. (The following example uses a [307 redirect](https://developer.mozilla.org/docs/Web/HTTP/Status/307)).

```
export default async (req, res) => {
  // Check the secret and next parameters
  // This secret should only be known to this API route and the CMS
  if (req.query.secret !== 'MY_SECRET_TOKEN' || !req.query.slug) {
    return res.status(401).json({ message: 'Invalid token' })
  }

  // Fetch the headless CMS to check if the provided `slug` exists
  // getPostBySlug would implement the required fetching logic to the headless CMS
  const post = await getPostBySlug(req.query.slug)

  // If the slug doesn't exist prevent preview mode from being enabled
  if (!post) {
    return res.status(401).json({ message: 'Invalid slug' })
  }

  // Enable Preview Mode by setting the cookies
  res.setPreviewData({})

  // Redirect to the path from the fetched post
  // We don't redirect to req.query.slug as that might lead to open redirect vulnerabilities
  res.redirect(post.slug)
}
```

If it succeeds, then the browser will be redirected to the path you want to preview with the preview mode cookies being set.

## Step 2: UpdategetStaticProps

The next step is to update `getStaticProps` to support the preview mode.

If you request a page which has `getStaticProps` with the preview mode cookies set (via `res.setPreviewData`), then `getStaticProps` will be called at **request time** (instead of at build time).

Furthermore, it will be called with a `context` object where:

- `context.preview` will be `true`.
- `context.previewData` will be the same as the argument used for `setPreviewData`.

```
export async function getStaticProps(context) {
  // If you request this page with the preview mode cookies set:
  //
  // - context.preview will be true
  // - context.previewData will be the same as
  //   the argument used for `setPreviewData`.
}
```

We used `res.setPreviewData({})` in the preview API route, so `context.previewData` will be `{}`. You can use this to pass session information from the preview API route to `getStaticProps` if necessary.

If you’re also using `getStaticPaths`, then `context.params` will also be available.

### Fetch preview data

You can update `getStaticProps` to fetch different data based on `context.preview` and/or `context.previewData`.

For example, your headless CMS might have a different API endpoint for draft posts. If so, you can use `context.preview` to modify the API endpoint URL like below:

```
export async function getStaticProps(context) {
  // If context.preview is true, append "/preview" to the API endpoint
  // to request draft data instead of published data. This will vary
  // based on which headless CMS you're using.
  const res = await fetch(`https://.../${context.preview ? 'preview' : ''}`)
  // ...
}
```

That’s it! If you access the preview API route (with `secret` and `slug`) from your headless CMS or manually, you should now be able to see the preview content. And if you update your draft without publishing, you should be able to preview the draft.

Set this as the preview URL on your headless CMS or access manually, and you should be able to see the preview.

 Terminal

```
https://<your-site>/api/preview?secret=<token>&slug=<path>
```

## More Details

> **Good to know**: during rendering `next/router` exposes an `isPreview` flag, see the [router object docs](https://nextjs.org/docs/pages/api-reference/functions/use-router#router-object) for more info.

### Specify the Preview Mode duration

`setPreviewData` takes an optional second parameter which should be an options object. It accepts the following keys:

- `maxAge`: Specifies the number (in seconds) for the preview session to last for.
- `path`: Specifies the path the cookie should be applied under. Defaults to `/` enabling preview mode for all paths.

```
setPreviewData(data, {
  maxAge: 60 * 60, // The preview mode cookies expire in 1 hour
  path: '/about', // The preview mode cookies apply to paths with /about
})
```

### Clear the Preview Mode cookies

By default, no expiration date is set for Preview Mode cookies, so the preview session ends when the browser is closed.

To clear the Preview Mode cookies manually, create an API route that calls `clearPreviewData()`:

 pages/api/clear-preview-mode-cookies.js

```
export default function handler(req, res) {
  res.clearPreviewData({})
}
```

Then, send a request to `/api/clear-preview-mode-cookies` to invoke the API Route. If calling this route using [next/link](https://nextjs.org/docs/pages/api-reference/components/link), you must pass `prefetch={false}` to prevent calling `clearPreviewData` during link prefetching.

If a path was specified in the `setPreviewData` call, you must pass the same path to `clearPreviewData`:

 pages/api/clear-preview-mode-cookies.js

```
export default function handler(req, res) {
  const { path } = req.query

  res.clearPreviewData({ path })
}
```

### previewDatasize limits

You can pass an object to `setPreviewData` and have it be available in `getStaticProps`. However, because the data will be stored in a cookie, there’s a size limitation. Currently, preview data is limited to 2KB.

### Works withgetServerSideProps

The preview mode works on `getServerSideProps` as well. It will also be available on the `context` object containing `preview` and `previewData`.

> **Good to know**: You shouldn't set the `Cache-Control` header when using Preview Mode because it cannot be bypassed. Instead, we recommend using [ISR](https://nextjs.org/docs/pages/guides/incremental-static-regeneration).

### Works with API Routes

API Routes will have access to `preview` and `previewData` under the request object. For example:

```
export default function myApiRoute(req, res) {
  const isPreview = req.preview
  const previewData = req.previewData
  // ...
}
```

### Unique pernext build

Both the bypass cookie value and the private key for encrypting the `previewData` change when `next build` is completed.
This ensures that the bypass cookie can’t be guessed.

> **Good to know**: To test Preview Mode locally over HTTP your browser will need to allow third-party cookies and local storage access.

Was this helpful?

supported.

---

# How to optimize your Next.js application for production

> Recommendations to ensure the best performance and user experience before taking your Next.js application to production.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)ProductionYou are currently viewing the documentation for Pages Router.

# How to optimize your Next.js application for production

Last updated  April 17, 2025

Before taking your Next.js application to production, there are some optimizations and patterns you should consider implementing for the best user experience, performance, and security.

This page provides best practices that you can use as a reference when [building your application](#during-development) and [before going to production](#before-going-to-production), as well as the [automatic Next.js optimizations](#automatic-optimizations) you should be aware of.

## Automatic optimizations

These Next.js optimizations are enabled by default and require no configuration:

- **Code-splitting:** Next.js automatically code-splits your application code by pages. This means only the code needed for the current page is loaded on navigation. You may also consider [lazy loading](https://nextjs.org/docs/pages/guides/lazy-loading) third-party libraries, where appropriate.
- **Prefetching:** When a link to a new route enters the user's viewport, Next.js prefetches the route in background. This makes navigation to new routes almost instant. You can opt out of prefetching, where appropriate.
- **Automatic Static Optimization:** Next.js automatically determines that a page is static (can be pre-rendered) if it has no blocking data requirements. Optimized pages can be cached, and served to the end-user from multiple CDN locations. You may opt into [Server-side Rendering](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props), where appropriate.

These defaults aim to improve your application's performance, and reduce the cost and amount of data transferred on each network request.

## During development

While building your application, we recommend using the following features to ensure the best performance and user experience:

### Routing and rendering

- **<Link>component:** Use the `<Link>` component for client-side navigation and prefetching.
- **Custom Errors:** Gracefully handle [500](https://nextjs.org/docs/pages/building-your-application/routing/custom-error#500-page) and [404 errors](https://nextjs.org/docs/pages/building-your-application/routing/custom-error#404-page)

### Data fetching and caching

- **API Routes:** Use Route Handlers to access your backend resources, and prevent sensitive secrets from being exposed to the client.
- **Data Caching:** Verify whether your data requests are being cached or not, and opt into caching, where appropriate. Ensure requests that don't use `getStaticProps` are cached where appropriate.
- **Incremental Static Regeneration:** Use Incremental Static Regeneration to update static pages after they've been built, without rebuilding your entire site.
- **Static Images:** Use the `public` directory to automatically cache your application's static assets, e.g. images.

### UI and accessibility

- **Font Module:** Optimize fonts by using the Font Module, which automatically hosts your font files with other static assets, removes external network requests, and reduces [layout shift](https://web.dev/articles/cls).
- **<Image>Component:** Optimize images by using the Image Component, which automatically optimizes images, prevents layout shift, and serves them in modern formats like WebP.
- **<Script>Component:** Optimize third-party scripts by using the Script Component, which automatically defers scripts and prevents them from blocking the main thread.
- **ESLint:** Use the built-in `eslint-plugin-jsx-a11y` plugin to catch accessibility issues early.

### Security

- **Environment Variables:** Ensure your `.env.*` files are added to `.gitignore` and only public variables are prefixed with `NEXT_PUBLIC_`.
- **Content Security Policy:** Consider adding a Content Security Policy to protect your application against various security threats such as cross-site scripting, clickjacking, and other code injection attacks.

### Metadata and SEO

- **<Head>Component:** Use the `next/head` component to add page titles, descriptions, and more.

### Type safety

- **TypeScript andTS Plugin:** Use TypeScript and the TypeScript plugin for better type-safety, and to help you catch errors early.

## Before going to production

Before going to production, you can run `next build` to build your application locally and catch any build errors, then run `next start` to measure the performance of your application in a production-like environment.

### Core Web Vitals

- **Lighthouse:** Run lighthouse in incognito to gain a better understanding of how your users will experience your site, and to identify areas for improvement. This is a simulated test and should be paired with looking at field data (such as Core Web Vitals).

### Analyzing bundles

Use the [@next/bundle-analyzerplugin](https://nextjs.org/docs/app/guides/package-bundling#nextbundle-analyzer-for-webpack) to analyze the size of your JavaScript bundles and identify large modules and dependencies that might be impacting your application's performance.

Additionally, the following tools can help you understand the impact of adding new dependencies to your application:

- [Import Cost](https://marketplace.visualstudio.com/items?itemName=wix.vscode-import-cost)
- [Package Phobia](https://packagephobia.com/)
- [Bundle Phobia](https://bundlephobia.com/)
- [bundlejs](https://bundlejs.com/)

Was this helpful?

supported.
