# How to use markdown and MDX in Next.js and more

# How to use markdown and MDX in Next.js

> Learn how to configure MDX and use it in your Next.js apps.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)MDX

# How to use markdown and MDX in Next.js

Last updated  July 29, 2025

[Markdown](https://daringfireball.net/projects/markdown/syntax) is a lightweight markup language used to format text. It allows you to write using plain text syntax and convert it to structurally valid HTML. It's commonly used for writing content on websites and blogs.

You write...

```
I **love** using [Next.js](https://nextjs.org/)
```

Output:

```
<p>I <strong>love</strong> using <a href="https://nextjs.org/">Next.js</a></p>
```

[MDX](https://mdxjs.com/) is a superset of markdown that lets you write [JSX](https://react.dev/learn/writing-markup-with-jsx) directly in your markdown files. It is a powerful way to add dynamic interactivity and embed React components within your content.

Next.js can support both local MDX content inside your application, as well as remote MDX files fetched dynamically on the server. The Next.js plugin handles transforming markdown and React components into HTML, including support for usage in Server Components (the default in App Router).

> **Good to know**: View the [Portfolio Starter Kit](https://vercel.com/templates/next.js/portfolio-starter-kit) template for a complete working example.

## Install dependencies

The `@next/mdx` package, and related packages, are used to configure Next.js so it can process markdown and MDX. **It sources data from local files**, allowing you to create pages with a `.md` or `.mdx` extension, directly in your `/pages` or `/app` directory.

Install these packages to render MDX with Next.js:

 Terminal

```
npm install @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

## Configurenext.config.mjs

Update the `next.config.mjs` file at your project's root to configure it to use MDX:

 next.config.mjs

```
import createMDX from '@next/mdx'

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configure `pageExtensions` to include markdown and MDX files
  pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'],
  // Optionally, add any other Next.js config below
}

const withMDX = createMDX({
  // Add markdown plugins here, as desired
})

// Merge MDX config with Next.js config
export default withMDX(nextConfig)
```

This allows `.mdx` files to act as pages, routes, or imports in your application.

### Handling.mdfiles

By default, `next/mdx` only compiles files with the `.mdx` extension. To handle `.md` files with webpack, update the `extension` option:

 next.config.mjs

```
const withMDX = createMDX({
  extension: /\.(md|mdx)$/,
})
```

## Add anmdx-components.tsxfile

Create an `mdx-components.tsx` (or `.js`) file in the root of your project to define global MDX Components. For example, at the same level as `pages` or `app`, or inside `src` if applicable.

 mdx-components.tsxJavaScriptTypeScript

```
import type { MDXComponents } from 'mdx/types'

const components: MDXComponents = {}

export function useMDXComponents(): MDXComponents {
  return components
}
```

> **Good to know**:
>
>
>
> - `mdx-components.tsx` is **required** to use `@next/mdx` with App Router and will not work without it.
> - Learn more about the [mdx-components.tsxfile convention](https://nextjs.org/docs/app/api-reference/file-conventions/mdx-components).
> - Learn how to [use custom styles and components](#using-custom-styles-and-components).

## Rendering MDX

You can render MDX using Next.js's file based routing or by importing MDX files into other pages.

### Using file based routing

When using file based routing, you can use MDX pages like any other page.

In App Router apps, that includes being able to use [metadata](https://nextjs.org/docs/app/getting-started/metadata-and-og-images).

Create a new MDX page within the `/app` directory:

```
my-project
  ├── app
  │   └── mdx-page
  │       └── page.(mdx/md)
  |── mdx-components.(tsx/js)
  └── package.json
```

You can use MDX in these files, and even import React components, directly inside your MDX page:

```
import { MyComponent } from 'my-component'

# Welcome to my MDX page!

This is some **bold** and _italics_ text.

This is a list in markdown:

- One
- Two
- Three

Checkout my React component:

<MyComponent />
```

Navigating to the `/mdx-page` route should display your rendered MDX page.

### Using imports

Create a new page within the `/app` directory and an MDX file wherever you'd like:

```
.
  ├── app/
  │   └── mdx-page/
  │       └── page.(tsx/js)
  ├── markdown/
  │   └── welcome.(mdx/md)
  ├── mdx-components.(tsx/js)
  └── package.json
```

You can use MDX in these files, and even import React components, directly inside your MDX page:

Import the MDX file inside the page to display the content:

 app/mdx-page/page.tsxJavaScriptTypeScript

```
import Welcome from '@/markdown/welcome.mdx'

export default function Page() {
  return <Welcome />
}
```

Navigating to the `/mdx-page` route should display your rendered MDX page.

### Using dynamic imports

You can import dynamic MDX components instead of using filesystem routing for MDX files.

For example, you can have a dynamic route segment which loads MDX components from a separate directory:

![Route segments for dynamic MDX components](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fmdx-files.png&w=3840&q=75)![Route segments for dynamic MDX components](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fmdx-files.png&w=3840&q=75)

[generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params) can be used to prerender the provided routes. By marking `dynamicParams` as `false`, accessing a route not defined in `generateStaticParams` will 404.

app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const { default: Post } = await import(`@/content/${slug}.mdx`)

  return <Post />
}

export function generateStaticParams() {
  return [{ slug: 'welcome' }, { slug: 'about' }]
}

export const dynamicParams = false
```

> **Good to know**: Ensure you specify the `.mdx` file extension in your import. While it is not required to use [module path aliases](https://nextjs.org/docs/app/getting-started/installation#set-up-absolute-imports-and-module-path-aliases) (e.g., `@/content`), it does simplify your import path.

## Using custom styles and components

Markdown, when rendered, maps to native HTML elements. For example, writing the following markdown:

```
## This is a heading

This is a list in markdown:

- One
- Two
- Three
```

Generates the following HTML:

```
<h2>This is a heading</h2>

<p>This is a list in markdown:</p>

<ul>
  <li>One</li>
  <li>Two</li>
  <li>Three</li>
</ul>
```

To style your markdown, you can provide custom components that map to the generated HTML elements. Styles and components can be implemented globally, locally, and with shared layouts.

### Global styles and components

Adding styles and components in `mdx-components.tsx` will affect *all* MDX files in your application.

 mdx-components.tsxJavaScriptTypeScript

```
import type { MDXComponents } from 'mdx/types'
import Image, { ImageProps } from 'next/image'

// This file allows you to provide custom React components
// to be used in MDX files. You can import and use any
// React component you want, including inline styles,
// components from other libraries, and more.

const components = {
  // Allows customizing built-in components, e.g. to add styling.
  h1: ({ children }) => (
    <h1 style={{ color: 'red', fontSize: '48px' }}>{children}</h1>
  ),
  img: (props) => (
    <Image
      sizes="100vw"
      style={{ width: '100%', height: 'auto' }}
      {...(props as ImageProps)}
    />
  ),
} satisfies MDXComponents

export function useMDXComponents(): MDXComponents {
  return components
}
```

### Local styles and components

You can apply local styles and components to specific pages by passing them into imported MDX components. These will merge with and override [global styles and components](#global-styles-and-components).

 app/mdx-page/page.tsxJavaScriptTypeScript

```
import Welcome from '@/markdown/welcome.mdx'

function CustomH1({ children }) {
  return <h1 style={{ color: 'blue', fontSize: '100px' }}>{children}</h1>
}

const overrideComponents = {
  h1: CustomH1,
}

export default function Page() {
  return <Welcome components={overrideComponents} />
}
```

### Shared layouts

To share a layout across MDX pages, you can use the [built-in layouts support](https://nextjs.org/docs/app/api-reference/file-conventions/layout) with the App Router.

app/mdx-page/layout.tsxJavaScriptTypeScript

```
export default function MdxLayout({ children }: { children: React.ReactNode }) {
  // Create any shared layout or styles here
  return <div style={{ color: 'blue' }}>{children}</div>
}
```

### Using Tailwind typography plugin

If you are using [Tailwind](https://tailwindcss.com) to style your application, using the [@tailwindcss/typographyplugin](https://tailwindcss.com/docs/plugins#typography) will allow you to reuse your Tailwind configuration and styles in your markdown files.

The plugin adds a set of `prose` classes that can be used to add typographic styles to content blocks that come from sources, like markdown.

[Install Tailwind typography](https://github.com/tailwindlabs/tailwindcss-typography?tab=readme-ov-file#installation) and use with [shared layouts](#shared-layouts) to add the `prose` you want.

 app/mdx-page/layout.tsxJavaScriptTypeScript

```
export default function MdxLayout({ children }: { children: React.ReactNode }) {
  // Create any shared layout or styles here
  return (
    <div className="prose prose-headings:mt-8 prose-headings:font-semibold prose-headings:text-black prose-h1:text-5xl prose-h2:text-4xl prose-h3:text-3xl prose-h4:text-2xl prose-h5:text-xl prose-h6:text-lg dark:prose-headings:text-white">
      {children}
    </div>
  )
}
```

## Frontmatter

Frontmatter is a YAML like key/value pairing that can be used to store data about a page. `@next/mdx` does **not** support frontmatter by default, though there are many solutions for adding frontmatter to your MDX content, such as:

- [remark-frontmatter](https://github.com/remarkjs/remark-frontmatter)
- [remark-mdx-frontmatter](https://github.com/remcohaszing/remark-mdx-frontmatter)
- [gray-matter](https://github.com/jonschlinkert/gray-matter)

`@next/mdx` **does** allow you to use exports like any other JavaScript component:

Metadata can now be referenced outside of the MDX file:

 app/blog/page.tsxJavaScriptTypeScript

```
import BlogPost, { metadata } from '@/content/blog-post.mdx'

export default function Page() {
  console.log('metadata: ', metadata)
  //=> { author: 'John Doe' }
  return <BlogPost />
}
```

A common use case for this is when you want to iterate over a collection of MDX and extract data. For example, creating a blog index page from all blog posts. You can use packages like [Node'sfsmodule](https://nodejs.org/api/fs.html) or [globby](https://www.npmjs.com/package/globby) to read a directory of posts and extract the metadata.

> **Good to know**:
>
>
>
> - Using `fs`, `globby`, etc. can only be used server-side.
> - View the [Portfolio Starter Kit](https://vercel.com/templates/next.js/portfolio-starter-kit) template for a complete working example.

## remark and rehype Plugins

You can optionally provide remark and rehype plugins to transform the MDX content.

For example, you can use [remark-gfm](https://github.com/remarkjs/remark-gfm) to support GitHub Flavored Markdown.

Since the remark and rehype ecosystem is ESM only, you'll need to use `next.config.mjs` or `next.config.ts` as the configuration file.

 next.config.mjs

```
import remarkGfm from 'remark-gfm'
import createMDX from '@next/mdx'

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow .mdx extensions for files
  pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'],
  // Optionally, add any other Next.js config below
}

const withMDX = createMDX({
  // Add markdown plugins here, as desired
  options: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [],
  },
})

// Combine MDX and Next.js config
export default withMDX(nextConfig)
```

### Using Plugins with Turbopack

To use plugins with [Turbopack](https://nextjs.org/docs/app/api-reference/turbopack), upgrade to the latest `@next/mdx` and specify plugin names using a string:

 next.config.mjs

```
import createMDX from '@next/mdx'

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'],
}

const withMDX = createMDX({
  options: {
    remarkPlugins: [
      // Without options
      'remark-gfm',
      // With options
      ['remark-toc', { heading: 'The Table' }],
    ],
    rehypePlugins: [
      // Without options
      'rehype-slug',
      // With options
      ['rehype-katex', { strict: true, throwOnError: true }],
    ],
  },
})

export default withMDX(nextConfig)
```

> **Good to know**:
>
>
>
> remark and rehype plugins without serializable options cannot be used yet with [Turbopack](https://nextjs.org/docs/app/api-reference/turbopack), because JavaScript functions can't be passed to Rust.

## Remote MDX

If your MDX files or content lives *somewhere else*, you can fetch it dynamically on the server. This is useful for content stored in a CMS, database, or anywhere else. A community package for this use is [next-mdx-remote-client](https://github.com/ipikuka/next-mdx-remote-client?tab=readme-ov-file#the-part-associated-with-nextjs-app-router).

> **Good to know**: Please proceed with caution. MDX compiles to JavaScript and is executed on the server. You should only fetch MDX content from a trusted source, otherwise this can lead to remote code execution (RCE).

The following example uses `next-mdx-remote-client`:

 app/mdx-page-remote/page.tsxJavaScriptTypeScript

```
import { MDXRemote } from 'next-mdx-remote-client/rsc'

export default async function RemoteMdxPage() {
  // MDX text - can be from a database, CMS, fetch, anywhere...
  const res = await fetch('https://...')
  const markdown = await res.text()
  return <MDXRemote source={markdown} />
}
```

Navigating to the `/mdx-page-remote` route should display your rendered MDX.

## Deep Dive: How do you transform markdown into HTML?

React does not natively understand markdown. The markdown plaintext needs to first be transformed into HTML. This can be accomplished with `remark` and `rehype`.

`remark` is an ecosystem of tools around markdown. `rehype` is the same, but for HTML. For example, the following code snippet transforms markdown into HTML:

```
import { unified } from 'unified'
import remarkParse from 'remark-parse'
import remarkRehype from 'remark-rehype'
import rehypeSanitize from 'rehype-sanitize'
import rehypeStringify from 'rehype-stringify'

main()

async function main() {
  const file = await unified()
    .use(remarkParse) // Convert into markdown AST
    .use(remarkRehype) // Transform to HTML AST
    .use(rehypeSanitize) // Sanitize HTML input
    .use(rehypeStringify) // Convert AST into serialized HTML
    .process('Hello, Next.js!')

  console.log(String(file)) // <p>Hello, Next.js!</p>
}
```

The `remark` and `rehype` ecosystem contains plugins for [syntax highlighting](https://github.com/atomiks/rehype-pretty-code), [linking headings](https://github.com/rehypejs/rehype-autolink-headings), [generating a table of contents](https://github.com/remarkjs/remark-toc), and more.

When using `@next/mdx` as shown above, you **do not** need to use `remark` or `rehype` directly, as it is handled for you. We're describing it here for a deeper understanding of what the `@next/mdx` package is doing underneath.

## Using the Rust-based MDX compiler (experimental)

Next.js supports a new MDX compiler written in Rust. This compiler is still experimental and is not recommended for production use. To use the new compiler, you need to configure `next.config.js` when you pass it to `withMDX`:

 next.config.js

```
module.exports = withMDX({
  experimental: {
    mdxRs: true,
  },
})
```

`mdxRs` also accepts an object to configure how to transform mdx files.

 next.config.js

```
module.exports = withMDX({
  experimental: {
    mdxRs: {
      jsxRuntime?: string            // Custom jsx runtime
      jsxImportSource?: string       // Custom jsx import source,
      mdxType?: 'gfm' | 'commonmark' // Configure what kind of mdx syntax will be used to parse & transform
    },
  },
})
```

## Helpful Links

- [MDX](https://mdxjs.com)
- [@next/mdx](https://www.npmjs.com/package/@next/mdx)
- [remark](https://github.com/remarkjs/remark)
- [rehype](https://github.com/rehypejs/rehype)
- [Markdoc](https://markdoc.dev/docs/nextjs)

Was this helpful?

supported.

---

# How to optimize memory usage

> Optimize memory used by your application in development and production.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Memory Usage

# How to optimize memory usage

Last updated  October 18, 2025

As applications grow and become more feature rich, they can demand more resources when developing locally or creating production builds.

Let's explore some strategies and techniques to optimize memory and address common memory issues in Next.js.

## Reduce number of dependencies

Applications with a large amount of dependencies will use more memory.

The [Bundle Analyzer](https://nextjs.org/docs/app/guides/package-bundling) can help you investigate large dependencies in your application that may be able to be removed to improve performance and memory usage.

## Tryexperimental.webpackMemoryOptimizations

Starting in `v15.0.0`, you can add `experimental.webpackMemoryOptimizations: true` to your `next.config.js` file to change behavior in Webpack that reduces max memory usage but may increase compilation times by a slight amount.

> **Good to know**: This feature is currently experimental to test on more projects first, but it is considered to be low-risk.

## Runnext buildwith--experimental-debug-memory-usage

Starting in `14.2.0`, you can run `next build --experimental-debug-memory-usage` to run the build in a mode where Next.js will print out information about memory usage continuously throughout the build, such as heap usage and garbage collection statistics. Heap snapshots will also be taken automatically when memory usage gets close to the configured limit.

> **Good to know**: This feature is not compatible with the Webpack build worker option which is auto-enabled unless you have custom webpack config.

## Record a heap profile

To look for memory issues, you can record a heap profile from Node.js and load it in Chrome DevTools to identify potential sources of memory leaks.

In your terminal, pass the `--heap-prof` flag to Node.js when starting your Next.js build:

```
node --heap-prof node_modules/next/dist/bin/next build
```

At the end of the build, a `.heapprofile` file will be created by Node.js.

In Chrome DevTools, you can open the Memory tab and click on the "Load Profile" button to visualize the file.

## Analyze a snapshot of the heap

You can use an inspector tool to analyze the memory usage of the application.

When running the `next build` or `next dev` command, add `NODE_OPTIONS=--inspect` to the beginning of the command. This will expose the inspector agent on the default port.
If you wish to break before any user code starts, you can pass `--inspect-brk` instead. While the process is running, you can use a tool such as Chrome DevTools to connect to the debugging port to record and analyze a snapshot of the heap to see what memory is being retained.

Starting in `14.2.0`, you can also run `next build` with the `--experimental-debug-memory-usage` flag to make it easier to take heap snapshots.

While running in this mode, you can send a `SIGUSR2` signal to the process at any point, and the process will take a heap snapshot.

The heap snapshot will be saved to the project root of the Next.js application and can be loaded in any heap analyzer, such as Chrome DevTools, to see what memory is retained. This mode is not yet compatible with Webpack build workers.

See [how to record and analyze heap snapshots](https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots) for more information.

## Webpack build worker

The Webpack build worker allows you to run Webpack compilations inside a separate Node.js worker which will decrease memory usage of your application during builds.

This option is enabled by default if your application does not have a custom Webpack configuration starting in `v14.1.0`.

If you are using an older version of Next.js or you have a custom Webpack configuration, you can enable this option by setting `experimental.webpackBuildWorker: true` inside your `next.config.js`.

> **Good to know**: This feature may not be compatible with all custom Webpack plugins.

## Disable Webpack cache

The [Webpack cache](https://webpack.js.org/configuration/cache/) saves generated Webpack modules in memory and/or to disk to improve the speed of builds. This can
help with performance, but it will also increase the memory usage of your application to store the cached data.

You can disable this behavior by adding a [custom Webpack configuration](https://nextjs.org/docs/app/api-reference/config/next-config-js/webpack) to your application:

 next.config.mjs

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (
    config,
    { buildId, dev, isServer, defaultLoaders, nextRuntime, webpack }
  ) => {
    if (config.cache && !dev) {
      config.cache = Object.freeze({
        type: 'memory',
      })
    }
    // Important: return the modified config
    return config
  },
}

export default nextConfig
```

## Disable static analysis

Typechecking may require a lot of memory, especially in large projects.
However, most projects have a dedicated CI runner that already handles these tasks.
When the build produces out-of-memory issues during the "Running TypeScript" step, you can disable this task during builds:

 next.config.mjs

```
/** @type {import('next').NextConfig} */
const nextConfig = {
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

- [Ignoring TypeScript Errors](https://nextjs.org/docs/app/api-reference/config/typescript#disabling-typescript-errors-in-production)

Keep in mind that this may produce faulty deploys due to type errors.
We strongly recommend only promoting builds to production after static analysis has completed.
If you deploy to Vercel, you can check out the [guide for staging deployments](https://vercel.com/docs/deployments/managing-deployments#staging-and-promoting-a-production-deployment) to learn how to promote builds to production after custom tasks have succeeded.

## Disable source maps

Generating source maps consumes extra memory during the build process.

You can disable source map generation by adding `productionBrowserSourceMaps: false` and `experimental.serverSourceMaps: false` to your Next.js configuration.

When using the `cacheComponents` feature, Next.js will use source maps by default during the prerender phase of `next build`.
If you consistently encounter memory issues during that phase (after "Generating static pages"),
you can try disabling source maps in that phase by adding `enablePrerenderSourceMaps: false` to your Next.js configuration.

> **Good to know**: Some plugins may turn on source maps and may require custom configuration to disable.

## Edge memory issues

Next.js `v14.1.3` fixed a memory issue when using the Edge runtime. Please update to this version (or later) to see if it addresses your issue.

## Preloading Entries

When the Next.js server starts, it preloads each page's JavaScript modules into memory, rather than at request time.

This optimization allows for faster response times, in exchange for a larger initial memory footprint.

To disable this optimization, set the `experimental.preloadEntriesOnStart` flag to `false`.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const config: NextConfig = {
  experimental: {
    preloadEntriesOnStart: false,
  },
}

export default config
```

Next.js doesn't unload these JavaScript modules, meaning that even with this optimization disabled, the memory footprint of your Next.js server will eventually be the same if all pages are eventually requested.

Was this helpful?

supported.
