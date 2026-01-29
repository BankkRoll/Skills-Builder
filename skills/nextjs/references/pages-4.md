# Link and more

# Link

> API reference for the `<Link>` component.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Components](https://nextjs.org/docs/pages/api-reference/components)LinkYou are currently viewing the documentation for Pages Router.

# Link

Last updated  April 15, 2025

`<Link>` is a React component that extends the HTML `<a>` element to provide [prefetching](https://nextjs.org/docs/app/getting-started/linking-and-navigating#prefetching) and client-side navigation between routes. It is the primary way to navigate between routes in Next.js.

Basic usage:

   pages/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Home() {
  return <Link href="/dashboard">Dashboard</Link>
}
```

## Reference

The following props can be passed to the `<Link>` component:

| Prop | Example | Type | Required |
| --- | --- | --- | --- |
| href | href="/dashboard" | String or Object | Yes |
| as | as="/post/abc" | String or Object | - |
| replace | replace={false} | Boolean | - |
| scroll | scroll={false} | Boolean | - |
| prefetch | prefetch={false} | Boolean | - |
| shallow | shallow={false} | Boolean | - |
| locale | locale="fr" | String or Boolean | - |
| onNavigate | onNavigate={(e) => {}} | Function | - |

> **Good to know**: `<a>` tag attributes such as `className` or `target="_blank"` can be added to `<Link>` as props and will be passed to the underlying `<a>` element.

### href(required)

The path or URL to navigate to.

   pages/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

// Navigate to /about?name=test
export default function Home() {
  return (
    <Link
      href={{
        pathname: '/about',
        query: { name: 'test' },
      }}
    >
      About
    </Link>
  )
}
```

### replace

**Defaults tofalse.** When `true`, `next/link` will replace the current history state instead of adding a new URL into the [browser's history](https://developer.mozilla.org/docs/Web/API/History_API) stack.

   pages/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Home() {
  return (
    <Link href="/dashboard" replace>
      Dashboard
    </Link>
  )
}
```

### scroll

**Defaults totrue.** The default scrolling behavior of `<Link>` in Next.js **is to maintain scroll position**, similar to how browsers handle back and forwards navigation. When you navigate to a new [Page](https://nextjs.org/docs/app/api-reference/file-conventions/page), scroll position will stay the same as long as the Page is visible in the viewport. However, if the Page is not visible in the viewport, Next.js will scroll to the top of the first Page element.

When `scroll = {false}`, Next.js will not attempt to scroll to the first Page element.

> **Good to know**: Next.js checks if `scroll: false` before managing scroll behavior. If scrolling is enabled, it identifies the relevant DOM node for navigation and inspects each top-level element. All non-scrollable elements and those without rendered HTML are bypassed, this includes sticky or fixed positioned elements, and non-visible elements such as those calculated with `getBoundingClientRect`. Next.js then continues through siblings until it identifies a scrollable element that is visible in the viewport.

   pages/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Home() {
  return (
    <Link href="/dashboard" scroll={false}>
      Dashboard
    </Link>
  )
}
```

### prefetch

Prefetching happens when a `<Link />` component enters the user's viewport (initially or through scroll). Next.js prefetches and loads the linked route (denoted by the `href`) and data in the background to improve the performance of client-side navigation's. **Prefetching is only enabled in production**.

The following values can be passed to the `prefetch` prop:

- **true(default)**: The full route and its data will be prefetched.
- `false`: Prefetching will not happen when entering the viewport, but will happen on hover. If you want to completely remove fetching on hover as well, consider using an `<a>` tag or [incrementally adopting](https://nextjs.org/docs/app/guides/migrating/app-router-migration) the App Router, which enables disabling prefetching on hover too.

pages/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Home() {
  return (
    <Link href="/dashboard" prefetch={false}>
      Dashboard
    </Link>
  )
}
```

### shallow

Update the path of the current page without rerunning [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props), [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props) or [getInitialProps](https://nextjs.org/docs/pages/api-reference/functions/get-initial-props). Defaults to `false`.

pages/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Home() {
  return (
    <Link href="/dashboard" shallow={false}>
      Dashboard
    </Link>
  )
}
```

### locale

The active locale is automatically prepended. `locale` allows for providing a different locale. When `false` `href` has to include the locale as the default behavior is disabled.

pages/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Home() {
  return (
    <>
      {/* Default behavior: locale is prepended */}
      <Link href="/dashboard">Dashboard (with locale)</Link>

      {/* Disable locale prepending */}
      <Link href="/dashboard" locale={false}>
        Dashboard (without locale)
      </Link>

      {/* Specify a different locale */}
      <Link href="/dashboard" locale="fr">
        Dashboard (French)
      </Link>
    </>
  )
}
```

### as

Optional decorator for the path that will be shown in the browser URL bar. Before Next.js 9.5.3 this was used for dynamic routes, check our [previous docs](https://github.com/vercel/next.js/blob/v9.5.2/docs/api-reference/next/link.md#dynamic-routes) to see how it worked.

When this path differs from the one provided in `href` the previous `href`/`as` behavior is used as shown in the [previous docs](https://github.com/vercel/next.js/blob/v9.5.2/docs/api-reference/next/link.md#dynamic-routes).

### onNavigate

An event handler called during client-side navigation. The handler receives an event object that includes a `preventDefault()` method, allowing you to cancel the navigation if needed.

 app/page.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Page() {
  return (
    <Link
      href="/dashboard"
      onNavigate={(e) => {
        // Only executes during SPA navigation
        console.log('Navigating...')

        // Optionally prevent navigation
        // e.preventDefault()
      }}
    >
      Dashboard
    </Link>
  )
}
```

> **Good to know**: While `onClick` and `onNavigate` may seem similar, they serve different purposes. `onClick` executes for all click events, while `onNavigate` only runs during client-side navigation. Some key differences:
>
>
>
> - When using modifier keys (`Ctrl`/`Cmd` + Click), `onClick` executes but `onNavigate` doesn't since Next.js prevents default navigation for new tabs.
> - External URLs won't trigger `onNavigate` since it's only for client-side and same-origin navigations.
> - Links with the `download` attribute will work with `onClick` but not `onNavigate` since the browser will treat the linked URL as a download.

## Examples

The following examples demonstrate how to use the `<Link>` component in different scenarios.

### Linking to dynamic route segments

For [dynamic route segments](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes#convention), it can be handy to use template literals to create the link's path.

For example, you can generate a list of links to the dynamic route `pages/blog/[slug].js`

pages/blog/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

function Posts({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <Link href={`/blog/${post.slug}`}>{post.title}</Link>
        </li>
      ))}
    </ul>
  )
}
```

### Scrolling to anid

If you'd like to scroll to a specific `id` on navigation, you can append your URL with a `#` hash link or just pass a hash link to the `href` prop. This is possible since `<Link>` renders to an `<a>` element.

```
<Link href="/dashboard#settings">Settings</Link>

// Output
<a href="/dashboard#settings">Settings</a>
```

### Passing a URL Object

`Link` can also receive a URL object and it will automatically format it to create the URL string:

pages/index.tsJavaScriptTypeScript

```
import Link from 'next/link'

function Home() {
  return (
    <ul>
      <li>
        <Link
          href={{
            pathname: '/about',
            query: { name: 'test' },
          }}
        >
          About us
        </Link>
      </li>
      <li>
        <Link
          href={{
            pathname: '/blog/[slug]',
            query: { slug: 'my-post' },
          }}
        >
          Blog Post
        </Link>
      </li>
    </ul>
  )
}

export default Home
```

The above example has a link to:

- A predefined route: `/about?name=test`
- A [dynamic route](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes#convention): `/blog/my-post`

You can use every property as defined in the [Node.js URL module documentation](https://nodejs.org/api/url.html#url_url_strings_and_url_objects).

### Replace the URL instead of push

The default behavior of the `Link` component is to `push` a new URL into the `history` stack. You can use the `replace` prop to prevent adding a new entry, as in the following example:

   pages/index.jsJavaScriptTypeScript

```
import Link from 'next/link'

export default function Home() {
  return (
    <Link href="/about" replace>
      About us
    </Link>
  )
}
```

### Disable scrolling to the top of the page

The default behavior of `Link` is to scroll to the top of the page. When there is a hash defined it will scroll to the specific id, like a normal `<a>` tag. To prevent scrolling to the top / hash `scroll={false}` can be added to `Link`:

pages/index.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Home() {
  return (
    <Link href="/#hashid" scroll={false}>
      Disables scrolling to the top
    </Link>
  )
}
```

### Prefetching links in Proxy

It's common to use [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) for authentication or other purposes that involve rewriting the user to a different page. In order for the `<Link />` component to properly prefetch links with rewrites via Proxy, you need to tell Next.js both the URL to display and the URL to prefetch. This is required to avoid un-necessary fetches to proxy to know the correct route to prefetch.

For example, if you want to serve a `/dashboard` route that has authenticated and visitor views, you can add the following in your Proxy to redirect the user to the correct page:

 proxy.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'

export function proxy(request: Request) {
  const nextUrl = request.nextUrl
  if (nextUrl.pathname === '/dashboard') {
    if (request.cookies.authToken) {
      return NextResponse.rewrite(new URL('/auth/dashboard', request.url))
    } else {
      return NextResponse.rewrite(new URL('/public/dashboard', request.url))
    }
  }
}
```

In this case, you would want to use the following code in your `<Link />` component:

   pages/index.tsxJavaScriptTypeScript

```
'use client'

import Link from 'next/link'
import useIsAuthed from './hooks/useIsAuthed' // Your auth hook

export default function Home() {
  const isAuthed = useIsAuthed()
  const path = isAuthed ? '/auth/dashboard' : '/public/dashboard'
  return (
    <Link as="/dashboard" href={path}>
      Dashboard
    </Link>
  )
}
```

> **Good to know**: If you're using [Dynamic Routes](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes#convention), you'll need to adapt your `as` and `href` props. For example, if you have a Dynamic Route like `/dashboard/authed/[user]` that you want to present differently via proxy, you would write: `<Link href={{ pathname: '/dashboard/authed/[user]', query: { user: username } }} as="/dashboard/[user]">Profile</Link>`.

## Version history

| Version | Changes |
| --- | --- |
| v15.4.0 | Addautoas an alias to the defaultprefetchbehavior. |
| v15.3.0 | AddonNavigateAPI |
| v13.0.0 | No longer requires a child<a>tag. Acodemodis provided to automatically update your codebase. |
| v10.0.0 | hrefprops pointing to a dynamic route are automatically resolved and no longer require anasprop. |
| v8.0.0 | Improved prefetching performance. |
| v1.0.0 | next/linkintroduced. |

Was this helpful?

supported.

---

# Script

> Optimize third-party scripts in your Next.js application using the built-in `next/script` Component.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Components](https://nextjs.org/docs/pages/api-reference/components)ScriptYou are currently viewing the documentation for Pages Router.

# Script

Last updated  April 15, 2025

This API reference will help you understand how to use [props](#props) available for the Script Component. For features and usage, please see the [Optimizing Scripts](https://nextjs.org/docs/app/guides/scripts) page.

 app/dashboard/page.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function Dashboard() {
  return (
    <>
      <Script src="https://example.com/script.js" />
    </>
  )
}
```

## Props

Here's a summary of the props available for the Script Component:

| Prop | Example | Type | Required |
| --- | --- | --- | --- |
| src | src="http://example.com/script" | String | Required unless inline script is used |
| strategy | strategy="lazyOnload" | String | - |
| onLoad | onLoad={onLoadFunc} | Function | - |
| onReady | onReady={onReadyFunc} | Function | - |
| onError | onError={onErrorFunc} | Function | - |

## Required Props

The `<Script />` component requires the following properties.

### src

A path string specifying the URL of an external script. This can be either an absolute external URL or an internal path. The `src` property is required unless an inline script is used.

## Optional Props

The `<Script />` component accepts a number of additional properties beyond those which are required.

### strategy

The loading strategy of the script. There are four different strategies that can be used:

- `beforeInteractive`: Load before any Next.js code and before any page hydration occurs.
- `afterInteractive`: (**default**) Load early but after some hydration on the page occurs.
- `lazyOnload`: Load during browser idle time.
- `worker`: (experimental) Load in a web worker.

### beforeInteractive

Scripts that load with the `beforeInteractive` strategy are injected into the initial HTML from the server, downloaded before any Next.js module, and executed in the order they are placed.

Scripts denoted with this strategy are preloaded and fetched before any first-party code, but their execution **does not block page hydration from occurring**.

`beforeInteractive` scripts must be placed inside the `Document` Component (`pages/_document.js`) and are designed to load scripts that are needed by the entire site (i.e. the script will load when any page in the application has been loaded server-side).

**This strategy should only be used for critical scripts that need to be fetched as soon as possible.**

   pages/_document.js

```
import { Html, Head, Main, NextScript } from 'next/document'
import Script from 'next/script'

export default function Document() {
  return (
    <Html>
      <Head />
      <body>
        <Main />
        <NextScript />
        <Script
          src="https://example.com/script.js"
          strategy="beforeInteractive"
        />
      </body>
    </Html>
  )
}
```

> **Good to know**: Scripts with `beforeInteractive` will always be injected inside the `head` of the HTML document regardless of where it's placed in the component.

Some examples of scripts that should be fetched as soon as possible with `beforeInteractive` include:

- Bot detectors
- Cookie consent managers

### afterInteractive

Scripts that use the `afterInteractive` strategy are injected into the HTML client-side and will load after some (or all) hydration occurs on the page. **This is the default strategy** of the Script component and should be used for any script that needs to load as soon as possible but not before any first-party Next.js code.

`afterInteractive` scripts can be placed inside of any page or layout and will only load and execute when that page (or group of pages) is opened in the browser.

 app/page.js

```
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script src="https://example.com/script.js" strategy="afterInteractive" />
    </>
  )
}
```

Some examples of scripts that are good candidates for `afterInteractive` include:

- Tag managers
- Analytics

### lazyOnload

Scripts that use the `lazyOnload` strategy are injected into the HTML client-side during browser idle time and will load after all resources on the page have been fetched. This strategy should be used for any background or low priority scripts that do not need to load early.

`lazyOnload` scripts can be placed inside of any page or layout and will only load and execute when that page (or group of pages) is opened in the browser.

 app/page.js

```
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script src="https://example.com/script.js" strategy="lazyOnload" />
    </>
  )
}
```

Examples of scripts that do not need to load immediately and can be fetched with `lazyOnload` include:

- Chat support plugins
- Social media widgets

### worker

> **Warning:** The `worker` strategy is not yet stable and does not yet work with the App Router. Use with caution.

Scripts that use the `worker` strategy are off-loaded to a web worker in order to free up the main thread and ensure that only critical, first-party resources are processed on it. While this strategy can be used for any script, it is an advanced use case that is not guaranteed to support all third-party scripts.

To use `worker` as a strategy, the `nextScriptWorkers` flag must be enabled in `next.config.js`:

 next.config.js

```
module.exports = {
  experimental: {
    nextScriptWorkers: true,
  },
}
```

`worker` scripts can **only currently be used in thepages/directory**:

 pages/home.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function Home() {
  return (
    <>
      <Script src="https://example.com/script.js" strategy="worker" />
    </>
  )
}
```

### onLoad

> **Warning:** `onLoad` does not yet work with Server Components and can only be used in Client Components. Further, `onLoad` can't be used with `beforeInteractive` – consider using `onReady` instead.

Some third-party scripts require users to run JavaScript code once after the script has finished loading in order to instantiate content or call a function. If you are loading a script with either `afterInteractive` or `lazyOnload` as a loading strategy, you can execute code after it has loaded using the `onLoad` property.

Here's an example of executing a lodash method only after the library has been loaded.

 app/page.tsxJavaScriptTypeScript

```
'use client'

import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script
        src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.20/lodash.min.js"
        onLoad={() => {
          console.log(_.sample([1, 2, 3, 4]))
        }}
      />
    </>
  )
}
```

### onReady

> **Warning:** `onReady` does not yet work with Server Components and can only be used in Client Components.

Some third-party scripts require users to run JavaScript code after the script has finished loading and every time the component is mounted (after a route navigation for example). You can execute code after the script's load event when it first loads and then after every subsequent component re-mount using the `onReady` property.

Here's an example of how to re-instantiate a Google Maps JS embed every time the component is mounted:

```
import { useRef } from 'react'
import Script from 'next/script'

export default function Page() {
  const mapRef = useRef()

  return (
    <>
      <div ref={mapRef}></div>
      <Script
        id="google-maps"
        src="https://maps.googleapis.com/maps/api/js"
        onReady={() => {
          new google.maps.Map(mapRef.current, {
            center: { lat: -34.397, lng: 150.644 },
            zoom: 8,
          })
        }}
      />
    </>
  )
}
```

### onError

> **Warning:** `onError` does not yet work with Server Components and can only be used in Client Components. `onError` cannot be used with the `beforeInteractive` loading strategy.

Sometimes it is helpful to catch when a script fails to load. These errors can be handled with the `onError` property:

```
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script
        src="https://example.com/script.js"
        onError={(e: Error) => {
          console.error('Script failed to load', e)
        }}
      />
    </>
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | beforeInteractiveandafterInteractiveis modified to supportapp. |
| v12.2.4 | onReadyprop added. |
| v12.2.2 | Allownext/scriptwithbeforeInteractiveto be placed in_document. |
| v11.0.0 | next/scriptintroduced. |

Was this helpful?

supported.

---

# Components

> API Reference for Next.js built-in components in the Pages Router.

[Pages Router](https://nextjs.org/docs/pages)[API Reference](https://nextjs.org/docs/pages/api-reference)ComponentsYou are currently viewing the documentation for Pages Router.

# Components

Last updated  April 15, 2025[FontAPI Reference for the Font Module](https://nextjs.org/docs/pages/api-reference/components/font)[FormLearn how to use the `<Form>` component to handle form submissions and search params updates with client-side navigation.](https://nextjs.org/docs/pages/api-reference/components/form)[HeadAdd custom elements to the `head` of your page with the built-in Head component.](https://nextjs.org/docs/pages/api-reference/components/head)[ImageOptimize Images in your Next.js Application using the built-in `next/image` Component.](https://nextjs.org/docs/pages/api-reference/components/image)[Image (Legacy)Backwards compatible Image Optimization with the Legacy Image component.](https://nextjs.org/docs/pages/api-reference/components/image-legacy)[LinkAPI reference for the `<Link>` component.](https://nextjs.org/docs/pages/api-reference/components/link)[ScriptOptimize third-party scripts in your Next.js application using the built-in `next/script` Component.](https://nextjs.org/docs/pages/api-reference/components/script)

Was this helpful?

supported.

---

# ESLint

> Next.js reports ESLint errors and warnings during builds by default. Learn how to opt-out of this behavior here.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Configuration](https://nextjs.org/docs/pages/api-reference/config)ESLintYou are currently viewing the documentation for Pages Router.

# ESLint

Last updated  April 15, 2025

Next.js provides an ESLint configuration package, [eslint-config-next](https://www.npmjs.com/package/eslint-config-next), that makes it easy to catch common issues in your application. It includes the [@next/eslint-plugin-next](https://www.npmjs.com/package/@next/eslint-plugin-next) plugin along with recommended rule-sets from [eslint-plugin-react](https://www.npmjs.com/package/eslint-plugin-react) and [eslint-plugin-react-hooks](https://www.npmjs.com/package/eslint-plugin-react-hooks).

The package provides two main configurations:

- **eslint-config-next**: Base configuration with Next.js, React, and React Hooks rules. Supports both JavaScript and TypeScript files.
- **eslint-config-next/core-web-vitals**: Includes everything from the base config, plus upgrades rules that impact [Core Web Vitals](https://web.dev/vitals/) from warnings to errors. Recommended for most projects.

Additionally, for TypeScript projects:

- **eslint-config-next/typescript**: Adds TypeScript-specific linting rules from [typescript-eslint](https://typescript-eslint.io/). Use this alongside the base or core-web-vitals config.

## Setup ESLint

Get linting working quickly with the ESLint CLI (flat config):

1. Install ESLint and the Next.js config:
   Terminal
  ```
  pnpm add -D eslint eslint-config-next
  ```
2. Create `eslint.config.mjs` with the Next.js config:
   eslint.config.mjs
  ```
  import { defineConfig, globalIgnores } from 'eslint/config'
  import nextVitals from 'eslint-config-next/core-web-vitals'
  const eslintConfig = defineConfig([
    ...nextVitals,
    // Override default ignores of eslint-config-next.
    globalIgnores([
      // Default ignores of eslint-config-next:
      '.next/**',
      'out/**',
      'build/**',
      'next-env.d.ts',
    ]),
  ])
  export default eslintConfig
  ```
3. Run ESLint:
   Terminal
  ```
  pnpm exec eslint .
  ```

## Reference

The `eslint-config-next` package includes the `recommended` rule-sets from the following ESLint plugins:

- [eslint-plugin-react](https://www.npmjs.com/package/eslint-plugin-react)
- [eslint-plugin-react-hooks](https://www.npmjs.com/package/eslint-plugin-react-hooks)
- [@next/eslint-plugin-next](https://www.npmjs.com/package/@next/eslint-plugin-next)

### Rules

The `@next/eslint-plugin-next` rules included are:

| Enabled in recommended config | Rule | Description |
| --- | --- | --- |
|  | @next/next/google-font-display | Enforce font-display behavior with Google Fonts. |
|  | @next/next/google-font-preconnect | Ensurepreconnectis used with Google Fonts. |
|  | @next/next/inline-script-id | Enforceidattribute onnext/scriptcomponents with inline content. |
|  | @next/next/next-script-for-ga | Prefernext/scriptcomponent when using the inline script for Google Analytics. |
|  | @next/next/no-assign-module-variable | Prevent assignment to themodulevariable. |
|  | @next/next/no-async-client-component | Prevent Client Components from being async functions. |
|  | @next/next/no-before-interactive-script-outside-document | Prevent usage ofnext/script'sbeforeInteractivestrategy outside ofpages/_document.js. |
|  | @next/next/no-css-tags | Prevent manual stylesheet tags. |
|  | @next/next/no-document-import-in-page | Prevent importingnext/documentoutside ofpages/_document.js. |
|  | @next/next/no-duplicate-head | Prevent duplicate usage of<Head>inpages/_document.js. |
|  | @next/next/no-head-element | Prevent usage of<head>element. |
|  | @next/next/no-head-import-in-document | Prevent usage ofnext/headinpages/_document.js. |
|  | @next/next/no-html-link-for-pages | Prevent usage of<a>elements to navigate to internal Next.js pages. |
|  | @next/next/no-img-element | Prevent usage of<img>element due to slower LCP and higher bandwidth. |
|  | @next/next/no-page-custom-font | Prevent page-only custom fonts. |
|  | @next/next/no-script-component-in-head | Prevent usage ofnext/scriptinnext/headcomponent. |
|  | @next/next/no-styled-jsx-in-document | Prevent usage ofstyled-jsxinpages/_document.js. |
|  | @next/next/no-sync-scripts | Prevent synchronous scripts. |
|  | @next/next/no-title-in-document-head | Prevent usage of<title>withHeadcomponent fromnext/document. |
|  | @next/next/no-typos | Prevent common typos inNext.js's data fetching functions |
|  | @next/next/no-unwanted-polyfillio | Prevent duplicate polyfills from Polyfill.io. |

We recommend using an appropriate [integration](https://eslint.org/docs/user-guide/integrations#editors) to view warnings and errors directly in your code editor during development.

 `next lint` removal

Starting with Next.js 16, `next lint` is removed.

As part of the removal, the `eslint` option in your Next config file is no longer needed and can be safely removed.

## Examples

### Specifying a root directory within a monorepo

If you're using `@next/eslint-plugin-next` in a project where Next.js isn't installed in your root directory (such as a monorepo), you can tell `@next/eslint-plugin-next` where to find your Next.js application using the `settings` property in your `eslint.config.mjs`:

 eslint.config.mjs

```
import { defineConfig } from 'eslint/config'
import eslintNextPlugin from '@next/eslint-plugin-next'

const eslintConfig = defineConfig([
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    plugins: {
      next: eslintNextPlugin,
    },
    settings: {
      next: {
        rootDir: 'packages/my-app/',
      },
    },
  },
])

export default eslintConfig
```

`rootDir` can be a path (relative or absolute), a glob (i.e. `"packages/*/"`), or an array of paths and/or globs.

### Disabling rules

If you would like to modify or disable any rules provided by the supported plugins (`react`, `react-hooks`, `next`), you can directly change them using the `rules` property in your `eslint.config.mjs`:

 eslint.config.mjs

```
import { defineConfig, globalIgnores } from 'eslint/config'
import nextVitals from 'eslint-config-next/core-web-vitals'

const eslintConfig = defineConfig([
  ...nextVitals,
  {
    rules: {
      'react/no-unescaped-entities': 'off',
      '@next/next/no-page-custom-font': 'off',
    },
  },
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    '.next/**',
    'out/**',
    'build/**',
    'next-env.d.ts',
  ]),
])

export default eslintConfig
```

### With Core Web Vitals

Enable the `eslint-config-next/core-web-vitals` configuration in your ESLint config.

 eslint.config.mjs

```
import { defineConfig, globalIgnores } from 'eslint/config'
import nextVitals from 'eslint-config-next/core-web-vitals'

const eslintConfig = defineConfig([
  ...nextVitals,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    '.next/**',
    'out/**',
    'build/**',
    'next-env.d.ts',
  ]),
])

export default eslintConfig
```

`eslint-config-next/core-web-vitals` upgrades certain lint rules in `@next/eslint-plugin-next` from warnings to errors to help improve your [Core Web Vitals](https://web.dev/vitals/) metrics.

> The `eslint-config-next/core-web-vitals` configuration is automatically included for new applications built with [Create Next App](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

### With TypeScript

In addition to the Next.js ESLint rules, `create-next-app --typescript` will also add TypeScript-specific lint rules with `eslint-config-next/typescript` to your config:

 eslint.config.mjs

```
import { defineConfig, globalIgnores } from 'eslint/config'
import nextVitals from 'eslint-config-next/core-web-vitals'
import nextTs from 'eslint-config-next/typescript'

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    '.next/**',
    'out/**',
    'build/**',
    'next-env.d.ts',
  ]),
])

export default eslintConfig
```

Those rules are based on [plugin:@typescript-eslint/recommended](https://typescript-eslint.io/linting/configs#recommended).
See [typescript-eslint > Configs](https://typescript-eslint.io/linting/configs) for more details.

### With Prettier

ESLint also contains code formatting rules, which can conflict with your existing [Prettier](https://prettier.io/) setup. We recommend including [eslint-config-prettier](https://github.com/prettier/eslint-config-prettier) in your ESLint config to make ESLint and Prettier work together.

First, install the dependency:

 Terminal

```
pnpm add -D eslint-config-prettier
```

Then, add `prettier` to your existing ESLint config:

 eslint.config.mjs

```
import { defineConfig, globalIgnores } from 'eslint/config'
import nextVitals from 'eslint-config-next/core-web-vitals'
import prettier from 'eslint-config-prettier/flat'

const eslintConfig = defineConfig([
  ...nextVitals,
  prettier,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    '.next/**',
    'out/**',
    'build/**',
    'next-env.d.ts',
  ]),
])

export default eslintConfig
```

### Running lint on staged files

If you would like to use ESLint with [lint-staged](https://github.com/okonet/lint-staged) to run the linter on staged git files, add the following to the `.lintstagedrc.js` file in the root of your project:

 .lintstagedrc.js

```
const path = require('path')

const buildEslintCommand = (filenames) =>
  `eslint --fix ${filenames
    .map((f) => `"${path.relative(process.cwd(), f)}"`)
    .join(' ')}`

module.exports = {
  '*.{js,jsx,ts,tsx}': [buildEslintCommand],
}
```

## Migrating existing config

If you already have ESLint configured in your application, there are two approaches to integrate Next.js linting rules, depending on your setup.

#### Using the plugin directly

Use `@next/eslint-plugin-next` directly if you have any of the following already configured:

- Conflicting plugins installed separately or through another config (such as `airbnb` or `react-app`):
  - `react`
  - `react-hooks`
  - `jsx-a11y`
  - `import`
- Custom `parserOptions` different from Next.js defaults (only if you have [customized your Babel configuration](https://nextjs.org/docs/pages/guides/babel))
- `eslint-plugin-import` with custom Node.js and/or TypeScript [resolvers](https://github.com/benmosher/eslint-plugin-import#resolvers)

In these cases, use `@next/eslint-plugin-next` directly to avoid conflicts:

First, install the plugin:

 Terminal

```
pnpm add -D @next/eslint-plugin-next
```

Then add it to your ESLint config:

 eslint.config.mjs

```
import { defineConfig } from 'eslint/config'
import nextPlugin from '@next/eslint-plugin-next'

const eslintConfig = defineConfig([
  // Your other configurations...
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    plugins: {
      '@next/next': nextPlugin,
    },
    rules: {
      ...nextPlugin.configs.recommended.rules,
    },
  },
])

export default eslintConfig
```

This approach eliminates the risk of collisions or errors that can occur when the same plugins or parsers are imported across multiple configurations.

#### Adding to existing config

If you're adding Next.js to an existing ESLint setup, spread the Next.js config into your array:

 eslint.config.mjs

```
import nextConfig from 'eslint-config-next/core-web-vitals'
// Your other config imports...

const eslintConfig = [
  // Your other configurations...
  ...nextConfig,
]

export default eslintConfig
```

When you spread `...nextConfig`, you're adding multiple config objects that include file patterns, plugins, rules, ignores, and parser settings. ESLint applies configs in order, so later rules can override earlier ones for matching files.

> **Good to know:** This approach works well for straightforward setups. If you have a complex existing config with specific file patterns or plugin configurations that conflict, consider using the plugin directly (as shown above) for more granular control.

| Version | Changes |
| --- | --- |
| v16.0.0 | next lintand theeslintnext.config.js option were removed in favor of the ESLint CLI. Acodemodis available to help you migrate. |

Was this helpful?

supported.

---

# experimental.adapterPath

> Configure a custom adapter for Next.js to hook into the build process with modifyConfig and buildComplete callbacks.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)experimental.adapterPathYou are currently viewing the documentation for Pages Router.

# experimental.adapterPath

Last updated  October 6, 2025

Next.js provides an experimental API that allows you to create custom adapters to hook into the build process. This is useful for deployment platforms or custom build integrations that need to modify the Next.js configuration or process the build output.

## Configuration

To use an adapter, specify the path to your adapter module in `experimental.adapterPath`:

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    adapterPath: require.resolve('./my-adapter.js'),
  },
}

module.exports = nextConfig
```

## Creating an Adapter

An adapter is a module that exports an object implementing the `NextAdapter` interface:

```
export interface NextAdapter {
  name: string
  modifyConfig?: (
    config: NextConfigComplete,
    ctx: {
      phase: PHASE_TYPE
    }
  ) => Promise<NextConfigComplete> | NextConfigComplete
  onBuildComplete?: (ctx: {
    routes: {
      headers: Array<ManifestHeaderRoute>
      redirects: Array<ManifestRedirectRoute>
      rewrites: {
        beforeFiles: Array<ManifestRewriteRoute>
        afterFiles: Array<ManifestRewriteRoute>
        fallback: Array<ManifestRewriteRoute>
      }
      dynamicRoutes: ReadonlyArray<ManifestRoute>
    }
    outputs: AdapterOutputs
    projectDir: string
    repoRoot: string
    distDir: string
    config: NextConfigComplete
    nextVersion: string
  }) => Promise<void> | void
}
```

### Basic Adapter Structure

Here's a minimal adapter example:

 my-adapter.js

```
/** @type {import('next').NextAdapter} */
const adapter = {
  name: 'my-custom-adapter',

  async modifyConfig(config, { phase }) {
    // Modify the Next.js config based on the build phase
    if (phase === 'phase-production-build') {
      return {
        ...config,
        // Add your modifications
      }
    }
    return config
  },

  async onBuildComplete({
    routes,
    outputs,
    projectDir,
    repoRoot,
    distDir,
    config,
    nextVersion,
  }) {
    // Process the build output
    console.log('Build completed with', outputs.pages.length, 'pages')

    // Access different output types
    for (const page of outputs.pages) {
      console.log('Page:', page.pathname, 'at', page.filePath)
    }

    for (const apiRoute of outputs.pagesApi) {
      console.log('API Route:', apiRoute.pathname, 'at', apiRoute.filePath)
    }

    for (const appPage of outputs.appPages) {
      console.log('App Page:', appPage.pathname, 'at', appPage.filePath)
    }

    for (const prerender of outputs.prerenders) {
      console.log('Prerendered:', prerender.pathname)
    }
  },
}

module.exports = adapter
```

## API Reference

### modifyConfig(config, context)

Called for any CLI command that loads the next.config to allow modification of the configuration.

**Parameters:**

- `config`: The complete Next.js configuration object
- `context.phase`: The current build phase (see [phases](https://nextjs.org/docs/app/api-reference/config/next-config-js#phase))

**Returns:** The modified configuration object (can be async)

### onBuildComplete(context)

Called after the build process completes with detailed information about routes and outputs.

**Parameters:**

- `routes`: Object containing route manifests for headers, redirects, rewrites, and dynamic routes
  - `routes.headers`: Array of header route objects with `source`, `sourceRegex`, `headers`, `has`, `missing`, and optional `priority` fields
  - `routes.redirects`: Array of redirect route objects with `source`, `sourceRegex`, `destination`, `statusCode`, `has`, `missing`, and optional `priority` fields
  - `routes.rewrites`: Object with `beforeFiles`, `afterFiles`, and `fallback` arrays, each containing rewrite route objects with `source`, `sourceRegex`, `destination`, `has`, and `missing` fields
  - `routes.dynamicRoutes`: Array of dynamic route objects with `source`, `sourceRegex`, `destination`, `has`, and `missing` fields
- `outputs`: Detailed information about all build outputs organized by type
- `projectDir`: Absolute path to the Next.js project directory
- `repoRoot`: Absolute path to the detected repository root
- `distDir`: Absolute path to the build output directory
- `config`: The final Next.js configuration (with `modifyConfig` applied)
- `nextVersion`: Version of Next.js being used
- `buildId`: Unique identifier for the current build

## Output Types

The `outputs` object contains arrays of different output types:

### Pages (outputs.pages)

React pages from the `pages/` directory:

```
{
  type: 'PAGES'
  id: string           // Route identifier
  filePath: string     // Path to the built file
  pathname: string     // URL pathname
  sourcePage: string   // Original source file path in pages/ directory
  runtime: 'nodejs' | 'edge'
  assets: Record<string, string>  // Traced dependencies (key: relative path from repo root, value: absolute path)
  wasmAssets?: Record<string, string>  // Bundled wasm files (key: name, value: absolute path)
  config: {
    maxDuration?: number
    preferredRegion?: string | string[]
    env?: Record<string, string>  // Environment variables (edge runtime only)
  }
}
```

### API Routes (outputs.pagesApi)

API routes from `pages/api/`:

```
{
  type: 'PAGES_API'
  id: string
  filePath: string
  pathname: string
  sourcePage: string   // Original relative source file path
  runtime: 'nodejs' | 'edge'
  assets: Record<string, string>
  wasmAssets?: Record<string, string>
  config: {
    maxDuration?: number
    preferredRegion?: string | string[]
    env?: Record<string, string>
  }
}
```

### App Pages (outputs.appPages)

React pages from the `app/` directory with `page.{js,ts,jsx,tsx}`:

```
{
  type: 'APP_PAGE'
  id: string
  filePath: string
  pathname: string     // Includes .rsc suffix for RSC routes
  sourcePage: string   // Original relative source file path
  runtime: 'nodejs' | 'edge'
  assets: Record<string, string>
  wasmAssets?: Record<string, string>
  config: {
    maxDuration?: number
    preferredRegion?: string | string[]
    env?: Record<string, string>
  }
}
```

### App Routes (outputs.appRoutes)

API and metadata routes from `app/` with `route.{js,ts,jsx,tsx}`:

```
{
  type: 'APP_ROUTE'
  id: string
  filePath: string
  pathname: string
  sourcePage: string
  runtime: 'nodejs' | 'edge'
  assets: Record<string, string>
  wasmAssets?: Record<string, string>
  config: {
    maxDuration?: number
    preferredRegion?: string | string[]
    env?: Record<string, string>
  }
}
```

### Prerenders (outputs.prerenders)

ISR-enabled routes and static prerenders:

```
{
  type: 'PRERENDER'
  id: string
  pathname: string
  parentOutputId: string  // ID of the source page/route
  groupId: number        // Revalidation group identifier (prerenders with same groupId revalidate together)
  pprChain?: {
    headers: Record<string, string>  // PPR chain headers (e.g., 'x-nextjs-resume': '1')
  }
  parentFallbackMode?: 'blocking' | false | null  // Fallback mode from getStaticPaths
  fallback?: {
    filePath: string
    initialStatus?: number
    initialHeaders?: Record<string, string | string[]>
    initialExpiration?: number
    initialRevalidate?: number
    postponedState?: string  // PPR postponed state
  }
  config: {
    allowQuery?: string[]     // Allowed query parameters
    allowHeader?: string[]    // Allowed headers for ISR
    bypassFor?: RouteHas[]    // Cache bypass conditions
    renderingMode?: RenderingMode
    bypassToken?: string
  }
}
```

### Static Files (outputs.staticFiles)

Static assets and auto-statically optimized pages:

```
{
  type: 'STATIC_FILE'
  id: string
  filePath: string
  pathname: string
}
```

### Middleware (outputs.middleware)

Middleware function (if present):

```
{
  type: 'MIDDLEWARE'
  id: string
  filePath: string
  pathname: string      // Always '/_middleware'
  sourcePage: string    // Always 'middleware'
  runtime: 'nodejs' | 'edge'
  assets: Record<string, string>
  wasmAssets?: Record<string, string>
  config: {
    maxDuration?: number
    preferredRegion?: string | string[]
    env?: Record<string, string>
    matchers?: Array<{
      source: string
      sourceRegex: string
      has: RouteHas[] | undefined
      missing: RouteHas[] | undefined
    }>
  }
}
```

## Routes Information

The `routes` object in `onBuildComplete` provides complete routing information with processed patterns ready for deployment:

### Headers

Each header route includes:

- `source`: Original route pattern (e.g., `/about`)
- `sourceRegex`: Compiled regex for matching requests
- `headers`: Key-value pairs of headers to apply
- `has`: Optional conditions that must be met
- `missing`: Optional conditions that must not be met
- `priority`: Optional flag for internal routes

### Redirects

Each redirect route includes:

- `source`: Original route pattern
- `sourceRegex`: Compiled regex for matching
- `destination`: Target URL (can include captured groups)
- `statusCode`: HTTP status code (301, 302, 307, 308)
- `has`: Optional positive conditions
- `missing`: Optional negative conditions
- `priority`: Optional flag for internal routes

### Rewrites

Rewrites are categorized into three phases:

- `beforeFiles`: Checked before filesystem (including pages and public files)
- `afterFiles`: Checked after pages/public files but before dynamic routes
- `fallback`: Checked after all other routes

Each rewrite includes `source`, `sourceRegex`, `destination`, `has`, and `missing`.

### Dynamic Routes

Generated from dynamic route segments (e.g., `[slug]`, `[...path]`). Each includes:

- `source`: Route pattern
- `sourceRegex`: Compiled regex with named capture groups
- `destination`: Internal destination with parameter substitution
- `has`: Optional positive conditions
- `missing`: Optional negative conditions

## Use Cases

Common use cases for adapters include:

- **Deployment Platform Integration**: Automatically configure build outputs for specific hosting platforms
- **Asset Processing**: Transform or optimize build outputs
- **Monitoring Integration**: Collect build metrics and route information
- **Custom Bundling**: Package outputs in platform-specific formats
- **Build Validation**: Ensure outputs meet specific requirements
- **Route Generation**: Use processed route information to generate platform-specific routing configs

Was this helpful?

supported.

---

# allowedDevOrigins

> Use `allowedDevOrigins` to configure additional origins that can request the dev server.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)allowedDevOriginsYou are currently viewing the documentation for Pages Router.

# allowedDevOrigins

Last updated  April 15, 2025

Next.js does not automatically block cross-origin requests during development, but will block by default in a future major version of Next.js to prevent unauthorized requesting of internal assets/endpoints that are available in development mode.

To configure a Next.js application to allow requests from origins other than the hostname the server was initialized with (`localhost` by default) you can use the `allowedDevOrigins` config option.

`allowedDevOrigins` allows you to set additional origins that can be used in development mode. For example, to use `local-origin.dev` instead of only `localhost`, open `next.config.js` and add the `allowedDevOrigins` config:

 next.config.js

```
module.exports = {
  allowedDevOrigins: ['local-origin.dev', '*.local-origin.dev'],
}
```

Was this helpful?

supported.
