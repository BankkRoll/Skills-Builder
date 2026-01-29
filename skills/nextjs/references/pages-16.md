# How to implement internationalization in Next.js and more

# How to implement internationalization in Next.js

> Next.js has built-in support for internationalized routing and language detection. Learn more here.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)InternationalizationYou are currently viewing the documentation for Pages Router.

# How to implement internationalization in Next.js

Last updated  October 17, 2025Examples

- [i18n routing](https://github.com/vercel/next.js/tree/canary/examples/i18n-routing-pages)

Next.js has built-in support for internationalized ([i18n](https://en.wikipedia.org/wiki/Internationalization_and_localization#Naming)) routing since `v10.0.0`. You can provide a list of locales, the default locale, and domain-specific locales and Next.js will automatically handle the routing.

The i18n routing support is currently meant to complement existing i18n library solutions like [react-intl](https://formatjs.io/docs/getting-started/installation), [react-i18next](https://react.i18next.com/), [lingui](https://lingui.dev/), [rosetta](https://github.com/lukeed/rosetta), [next-intl](https://github.com/amannn/next-intl), [next-translate](https://github.com/aralroca/next-translate), [next-multilingual](https://github.com/Avansai/next-multilingual), [tolgee](https://tolgee.io/integrations/next), [paraglide-next](https://inlang.com/m/osslbuzt/paraglide-next-i18n), [next-intlayer](https://intlayer.org/doc/environment/nextjs/next-with-page-router), [gt-react](https://generaltranslation.com/en/docs/react) and others by streamlining the routes and locale parsing.

## Getting started

To get started, add the `i18n` config to your `next.config.js` file.

Locales are [UTS Locale Identifiers](https://www.unicode.org/reports/tr35/tr35-59/tr35.html#Identifiers), a standardized format for defining locales.

Generally a Locale Identifier is made up of a language, region, and script separated by a dash: `language-region-script`. The region and script are optional. An example:

- `en-US` - English as spoken in the United States
- `nl-NL` - Dutch as spoken in the Netherlands
- `nl` - Dutch, no specific region

If user locale is `nl-BE` and it is not listed in your configuration, they will be redirected to `nl` if available, or to the default locale otherwise.
If you don't plan to support all regions of a country, it is therefore a good practice to include country locales that will act as fallbacks.

 next.config.js

```
module.exports = {
  i18n: {
    // These are all the locales you want to support in
    // your application
    locales: ['en-US', 'fr', 'nl-NL'],
    // This is the default locale you want to be used when visiting
    // a non-locale prefixed path e.g. `/hello`
    defaultLocale: 'en-US',
    // This is a list of locale domains and the default locale they
    // should handle (these are only required when setting up domain routing)
    // Note: subdomains must be included in the domain value to be matched e.g. "fr.example.com".
    domains: [
      {
        domain: 'example.com',
        defaultLocale: 'en-US',
      },
      {
        domain: 'example.nl',
        defaultLocale: 'nl-NL',
      },
      {
        domain: 'example.fr',
        defaultLocale: 'fr',
        // an optional http field can also be used to test
        // locale domains locally with http instead of https
        http: true,
      },
    ],
  },
}
```

## Locale Strategies

There are two locale handling strategies: Sub-path Routing and Domain Routing.

### Sub-path Routing

Sub-path Routing puts the locale in the url path.

 next.config.js

```
module.exports = {
  i18n: {
    locales: ['en-US', 'fr', 'nl-NL'],
    defaultLocale: 'en-US',
  },
}
```

With the above configuration `en-US`, `fr`, and `nl-NL` will be available to be routed to, and `en-US` is the default locale. If you have a `pages/blog.js` the following urls would be available:

- `/blog`
- `/fr/blog`
- `/nl-nl/blog`

The default locale does not have a prefix.

### Domain Routing

By using domain routing you can configure locales to be served from different domains:

 next.config.js

```
module.exports = {
  i18n: {
    locales: ['en-US', 'fr', 'nl-NL', 'nl-BE'],
    defaultLocale: 'en-US',

    domains: [
      {
        // Note: subdomains must be included in the domain value to be matched
        // e.g. www.example.com should be used if that is the expected hostname
        domain: 'example.com',
        defaultLocale: 'en-US',
      },
      {
        domain: 'example.fr',
        defaultLocale: 'fr',
      },
      {
        domain: 'example.nl',
        defaultLocale: 'nl-NL',
        // specify other locales that should be redirected
        // to this domain
        locales: ['nl-BE'],
      },
    ],
  },
}
```

For example if you have `pages/blog.js` the following urls will be available:

- `example.com/blog`
- `www.example.com/blog`
- `example.fr/blog`
- `example.nl/blog`
- `example.nl/nl-BE/blog`

## Automatic Locale Detection

When a user visits the application root (generally `/`), Next.js will try to automatically detect which locale the user prefers based on the [Accept-Language](https://developer.mozilla.org/docs/Web/HTTP/Headers/Accept-Language) header and the current domain.

If a locale other than the default locale is detected, the user will be redirected to either:

- **When using Sub-path Routing:** The locale prefixed path
- **When using Domain Routing:** The domain with that locale specified as the default

When using Domain Routing, if a user with the `Accept-Language` header `fr;q=0.9` visits `example.com`, they will be redirected to `example.fr` since that domain handles the `fr` locale by default.

When using Sub-path Routing, the user would be redirected to `/fr`.

### Prefixing the Default Locale

With Next.js 12 and [Proxy](https://nextjs.org/docs/pages/api-reference/file-conventions/proxy), we can add a prefix to the default locale with a [workaround](https://github.com/vercel/next.js/discussions/18419).

For example, here's a `next.config.js` file with support for a few languages. Note the `"default"` locale has been added intentionally.

 next.config.js

```
module.exports = {
  i18n: {
    locales: ['default', 'en', 'de', 'fr'],
    defaultLocale: 'default',
    localeDetection: false,
  },
  trailingSlash: true,
}
```

Next, we can use [Proxy](https://nextjs.org/docs/pages/api-reference/file-conventions/proxy) to add custom routing rules:

 proxy.ts

```
import { NextRequest, NextResponse } from 'next/server'

const PUBLIC_FILE = /\.(.*)$/

export async function proxy(req: NextRequest) {
  if (
    req.nextUrl.pathname.startsWith('/_next') ||
    req.nextUrl.pathname.includes('/api/') ||
    PUBLIC_FILE.test(req.nextUrl.pathname)
  ) {
    return
  }

  if (req.nextUrl.locale === 'default') {
    const locale = req.cookies.get('NEXT_LOCALE')?.value || 'en'

    return NextResponse.redirect(
      new URL(`/${locale}${req.nextUrl.pathname}${req.nextUrl.search}`, req.url)
    )
  }
}
```

This [Proxy](https://nextjs.org/docs/pages/api-reference/file-conventions/proxy) skips adding the default prefix to [API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) and [public](https://nextjs.org/docs/pages/api-reference/file-conventions/public-folder) files like fonts or images. If a request is made to the default locale, we redirect to our prefix `/en`.

### Disabling Automatic Locale Detection

The automatic locale detection can be disabled with:

 next.config.js

```
module.exports = {
  i18n: {
    localeDetection: false,
  },
}
```

When `localeDetection` is set to `false` Next.js will no longer automatically redirect based on the user's preferred locale and will only provide locale information detected from either the locale based domain or locale path as described above.

## Accessing the locale information

You can access the locale information via the Next.js router. For example, using the [useRouter()](https://nextjs.org/docs/pages/api-reference/functions/use-router) hook the following properties are available:

- `locale` contains the currently active locale.
- `locales` contains all configured locales.
- `defaultLocale` contains the configured default locale.

When [pre-rendering](https://nextjs.org/docs/pages/building-your-application/rendering/static-site-generation) pages with `getStaticProps` or `getServerSideProps`, the locale information is provided in [the context](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) provided to the function.

When leveraging `getStaticPaths`, the configured locales are provided in the context parameter of the function under `locales` and the configured defaultLocale under `defaultLocale`.

## Transition between locales

You can use `next/link` or `next/router` to transition between locales.

For `next/link`, a `locale` prop can be provided to transition to a different locale from the currently active one. If no `locale` prop is provided, the currently active `locale` is used during client-transitions. For example:

```
import Link from 'next/link'

export default function IndexPage(props) {
  return (
    <Link href="/another" locale="fr">
      To /fr/another
    </Link>
  )
}
```

When using the `next/router` methods directly, you can specify the `locale` that should be used via the transition options. For example:

```
import { useRouter } from 'next/router'

export default function IndexPage(props) {
  const router = useRouter()

  return (
    <div
      onClick={() => {
        router.push('/another', '/another', { locale: 'fr' })
      }}
    >
      to /fr/another
    </div>
  )
}
```

Note that to handle switching only the `locale` while preserving all routing information such as [dynamic route](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes) query values or hidden href query values, you can provide the `href` parameter as an object:

```
import { useRouter } from 'next/router'
const router = useRouter()
const { pathname, asPath, query } = router
// change just the locale and maintain all other route information including href's query
router.push({ pathname, query }, asPath, { locale: nextLocale })
```

See [here](https://nextjs.org/docs/pages/api-reference/functions/use-router#with-url-object) for more information on the object structure for `router.push`.

If you have a `href` that already includes the locale you can opt-out of automatically handling the locale prefixing:

```
import Link from 'next/link'

export default function IndexPage(props) {
  return (
    <Link href="/fr/another" locale={false}>
      To /fr/another
    </Link>
  )
}
```

## Leveraging theNEXT_LOCALEcookie

Next.js allows setting a `NEXT_LOCALE=the-locale` cookie, which takes priority over the accept-language header. This cookie can be set using a language switcher and then when a user comes back to the site it will leverage the locale specified in the cookie when redirecting from `/` to the correct locale location.

For example, if a user prefers the locale `fr` in their accept-language header but a `NEXT_LOCALE=en` cookie is set the `en` locale when visiting `/` the user will be redirected to the `en` locale location until the cookie is removed or expired.

## Search Engine Optimization

Since Next.js knows what language the user is visiting it will automatically add the `lang` attribute to the `<html>` tag.

Next.js doesn't know about variants of a page so it's up to you to add the `hreflang` meta tags using [next/head](https://nextjs.org/docs/pages/api-reference/components/head). You can learn more about `hreflang` in the [Google Webmasters documentation](https://support.google.com/webmasters/answer/189077).

## How does this work with Static Generation?

> Note that Internationalized Routing does not integrate with [output: 'export'](https://nextjs.org/docs/pages/guides/static-exports) as it does not leverage the Next.js routing layer. Hybrid Next.js applications that do not use `output: 'export'` are fully supported.

### Dynamic Routes andgetStaticPropsPages

For pages using `getStaticProps` with [Dynamic Routes](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes), all locale variants of the page desired to be prerendered need to be returned from [getStaticPaths](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-paths). Along with the `params` object returned for `paths`, you can also return a `locale` field specifying which locale you want to render. For example:

 pages/blog/[slug].js

```
export const getStaticPaths = ({ locales }) => {
  return {
    paths: [
      // if no `locale` is provided only the defaultLocale will be generated
      { params: { slug: 'post-1' }, locale: 'en-US' },
      { params: { slug: 'post-1' }, locale: 'fr' },
    ],
    fallback: true,
  }
}
```

For [Automatically Statically Optimized](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization) and non-dynamic `getStaticProps` pages, **a version of the page will be generated for each locale**. This is important to consider because it can increase build times depending on how many locales are configured inside `getStaticProps`.

For example, if you have 50 locales configured with 10 non-dynamic pages using `getStaticProps`, this means `getStaticProps` will be called 500 times. 50 versions of the 10 pages will be generated during each build.

To decrease the build time of dynamic pages with `getStaticProps`, use a [fallbackmode](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-true). This allows you to return only the most popular paths and locales from `getStaticPaths` for prerendering during the build. Then, Next.js will build the remaining pages at runtime as they are requested.

### Automatically Statically Optimized Pages

For pages that are [automatically statically optimized](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization), a version of the page will be generated for each locale.

### Non-dynamic getStaticProps Pages

For non-dynamic `getStaticProps` pages, a version is generated for each locale like above. `getStaticProps` is called with each `locale` that is being rendered. If you would like to opt-out of a certain locale from being pre-rendered, you can return `notFound: true` from `getStaticProps` and this variant of the page will not be generated.

```
export async function getStaticProps({ locale }) {
  // Call an external API endpoint to get posts.
  // You can use any data fetching library
  const res = await fetch(`https://.../posts?locale=${locale}`)
  const posts = await res.json()

  if (posts.length === 0) {
    return {
      notFound: true,
    }
  }

  // By returning { props: posts }, the Blog component
  // will receive `posts` as a prop at build time
  return {
    props: {
      posts,
    },
  }
}
```

## Limits for the i18n config

- `locales`: 100 total locales
- `domains`: 100 total locale domain items

> **Good to know**: These limits have been added initially to prevent potential [performance issues at build time](#dynamic-routes-and-getstaticprops-pages). You can workaround these limits with custom routing using [Proxy](https://nextjs.org/docs/pages/api-reference/file-conventions/proxy) in Next.js 12.

Was this helpful?

supported.

---

# How to lazy load Client Components and libraries

> Lazy load imported libraries and React Components to improve your application's overall loading performance.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Lazy LoadingYou are currently viewing the documentation for Pages Router.

# How to lazy load Client Components and libraries

Last updated  April 24, 2025

[Lazy loading](https://developer.mozilla.org/docs/Web/Performance/Lazy_loading) in Next.js helps improve the initial loading performance of an application by decreasing the amount of JavaScript needed to render a route.

## next/dynamic

`next/dynamic` is a composite of [React.lazy()](https://react.dev/reference/react/lazy) and [Suspense](https://react.dev/reference/react/Suspense). It behaves the same way in the `app` and `pages` directories to allow for incremental migration.

In the example below, by using `next/dynamic`, the header component will not be included in the page's initial JavaScript bundle. The page will render the Suspense `fallback` first, followed by the `Header` component when the `Suspense` boundary is resolved.

```
import dynamic from 'next/dynamic'

const DynamicHeader = dynamic(() => import('../components/header'), {
  loading: () => <p>Loading...</p>,
})

export default function Home() {
  return <DynamicHeader />
}
```

> **Good to know**: In `import('path/to/component')`, the path must be explicitly written. It can't be a template string nor a variable. Furthermore the `import()` has to be inside the `dynamic()` call for Next.js to be able to match webpack bundles / module ids to the specific `dynamic()` call and preload them before rendering. `dynamic()` can't be used inside of React rendering as it needs to be marked in the top level of the module for preloading to work, similar to `React.lazy`.

## Examples

### With named exports

To dynamically import a named export, you can return it from the [Promise](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise) returned by [import()](https://github.com/tc39/proposal-dynamic-import#example):

components/hello.js

```
export function Hello() {
  return <p>Hello!</p>
}

// pages/index.js
import dynamic from 'next/dynamic'

const DynamicComponent = dynamic(() =>
  import('../components/hello').then((mod) => mod.Hello)
)
```

### With no SSR

To dynamically load a component on the client side, you can use the `ssr` option to disable server-rendering. This is useful if an external dependency or component relies on browser APIs like `window`.

```
'use client'

import dynamic from 'next/dynamic'

const DynamicHeader = dynamic(() => import('../components/header'), {
  ssr: false,
})
```

### With external libraries

This example uses the external library `fuse.js` for fuzzy search. The module is only loaded in the browser after the user types in the search input.

```
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

Was this helpful?

supported.

---

# How to use markdown and MDX in Next.js

> Learn how to configure MDX to write JSX in your markdown files.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)MDXYou are currently viewing the documentation for Pages Router.

# How to use markdown and MDX in Next.js

Last updated  April 24, 2025

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

Create a new MDX page within the `/pages` directory:

```
my-project
  |── mdx-components.(tsx/js)
  ├── pages
  │   └── mdx-page.(mdx/md)
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

Create a new page within the `/pages` directory and an MDX file wherever you'd like:

```
.
  ├── markdown/
  │   └── welcome.(mdx/md)
  ├── pages/
  │   └── mdx-page.(tsx/js)
  ├── mdx-components.(tsx/js)
  └── package.json
```

You can use MDX in these files, and even import React components, directly inside your MDX page:

Import the MDX file inside the page to display the content:

   pages/mdx-page.tsxJavaScriptTypeScript

```
import Welcome from '@/markdown/welcome.mdx'

export default function Page() {
  return <Welcome />
}
```

Navigating to the `/mdx-page` route should display your rendered MDX page.

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

   pages/mdx-page.tsxJavaScriptTypeScript

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

To share a layout around MDX pages, create a layout component:

components/mdx-layout.tsxJavaScriptTypeScript

```
export default function MdxLayout({ children }: { children: React.ReactNode }) {
  // Create any shared layout or styles here
  return <div style={{ color: 'blue' }}>{children}</div>
}
```

Then, import the layout component into the MDX page, wrap the MDX content in the layout, and export it:

```
import MdxLayout from '../components/mdx-layout'

# Welcome to my MDX page!

export default function MDXPage({ children }) {
  return <MdxLayout>{children}</MdxLayout>

}
```

### Using Tailwind typography plugin

If you are using [Tailwind](https://tailwindcss.com) to style your application, using the [@tailwindcss/typographyplugin](https://tailwindcss.com/docs/plugins#typography) will allow you to reuse your Tailwind configuration and styles in your markdown files.

The plugin adds a set of `prose` classes that can be used to add typographic styles to content blocks that come from sources, like markdown.

[Install Tailwind typography](https://github.com/tailwindlabs/tailwindcss-typography?tab=readme-ov-file#installation) and use with [shared layouts](#shared-layouts) to add the `prose` you want.

To share a layout around MDX pages, create a layout component:

components/mdx-layout.tsxJavaScriptTypeScript

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

Then, import the layout component into the MDX page, wrap the MDX content in the layout, and export it:

```
import MdxLayout from '../components/mdx-layout'

# Welcome to my MDX page!

export default function MDXPage({ children }) {
  return <MdxLayout>{children}</MdxLayout>

}
```

## Frontmatter

Frontmatter is a YAML like key/value pairing that can be used to store data about a page. `@next/mdx` does **not** support frontmatter by default, though there are many solutions for adding frontmatter to your MDX content, such as:

- [remark-frontmatter](https://github.com/remarkjs/remark-frontmatter)
- [remark-mdx-frontmatter](https://github.com/remcohaszing/remark-mdx-frontmatter)
- [gray-matter](https://github.com/jonschlinkert/gray-matter)

`@next/mdx` **does** allow you to use exports like any other JavaScript component:

Metadata can now be referenced outside of the MDX file:

   pages/blog.tsxJavaScriptTypeScript

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

   pages/mdx-page-remote.tsxJavaScriptTypeScript

```
import {
  serialize,
  type SerializeResult,
} from 'next-mdx-remote-client/serialize'
import { MDXClient } from 'next-mdx-remote-client'

type Props = {
  mdxSource: SerializeResult
}

export default function RemoteMdxPage({ mdxSource }: Props) {
  if ('error' in mdxSource) {
    // either render error UI or throw `mdxSource.error`
  }
  return <MDXClient {...mdxSource} />
}

export async function getStaticProps() {
  // MDX text - can be from a database, CMS, fetch, anywhere...
  const res = await fetch('https:...')
  const mdxText = await res.text()
  const mdxSource = await serialize({ source: mdxText })
  return { props: { mdxSource } }
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
