# No async Client Component and more

# No async Client Component

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No async Client Component

# No async Client Component

> Client components cannot be async functions.

## Why This Error Occurred

The error occurs when you try to define a Client Component as an async function. React Client Components [do not support](https://github.com/acdlite/rfcs/blob/first-class-promises/text/0000-first-class-support-for-promises.md#why-cant-client-components-be-async-functions) async functions. For example:

```
'use client'

// This will cause an error
async function ClientComponent() {
  // ...
}
```

## Possible Ways to Fix It

1. **Convert to a Server Component**: If possible, convert your Client Component to a Server Component. This allows you to use `async`/`await` directly in your component.
2. **Remove theasynckeyword**: If you need to keep it as a Client Component, remove the `async` keyword and handle data fetching differently.
3. **Use React Hooks for data fetching**: Utilize hooks like `useEffect` for client-side data fetching, or use third-party libraries.
4. **Leverage theusehook with a Context Provider**: Pass promises to child components using context, then resolve them with the `use` hook.

### Recommended: Server-side data fetching

We recommend fetching data on the server. For example:

 app/page.tsx

```
export default async function Page() {
  const data = await fetch('https://api.vercel.app/blog')
  const posts = await data.json()
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### Usingusewith Context Provider

Another pattern to explore is using the React `use` hook with a Context Provider. This allows you to pass Promises to child components and resolve them using the `use` hook . Here's an example:

First, let's create a separate file for the context provider:

 app/context.tsx

```
'use client'

import { createContext, useContext } from 'react'

export const BlogContext = createContext<Promise<any> | null>(null)

export function BlogProvider({
  children,
  blogPromise,
}: {
  children: React.ReactNode
  blogPromise: Promise<any>
}) {
  return (
    <BlogContext.Provider value={blogPromise}>{children}</BlogContext.Provider>
  )
}

export function useBlogContext() {
  const context = useContext(BlogContext)
  if (!context) {
    throw new Error('useBlogContext must be used within a BlogProvider')
  }
  return context
}
```

Now, let's create the Promise in a Server Component and stream it to the client:

 app/page.tsx

```
import { BlogProvider } from './context'

export default function Page() {
  const blogPromise = fetch('https://api.vercel.app/blog').then((res) =>
    res.json()
  )

  return (
    <BlogProvider blogPromise={blogPromise}>
      <BlogPosts />
    </BlogProvider>
  )
}
```

Here is the blog posts component:

 app/blog-posts.tsx

```
'use client'

import { use } from 'react'
import { useBlogContext } from './context'

export function BlogPosts() {
  const blogPromise = useBlogContext()
  const posts = use(blogPromise)

  return <div>{posts.length} blog posts</div>
}
```

This pattern allows you to start data fetching early and pass the Promise down to child components, which can then use the `use` hook to access the data when it's ready.

### Client-side data fetching

In scenarios where client fetching is needed, you can call `fetch` in `useEffect` (not recommended), or lean on popular React libraries in the community (such as [SWR](https://swr.vercel.app/) or [React Query](https://tanstack.com/query/latest)) for client fetching.

 app/page.tsx

```
'use client'

import { useState, useEffect } from 'react'

export function Posts() {
  const [posts, setPosts] = useState(null)

  useEffect(() => {
    async function fetchPosts() {
      const res = await fetch('https://api.vercel.app/blog')
      const data = await res.json()
      setPosts(data)
    }
    fetchPosts()
  }, [])

  if (!posts) return <div>Loading...</div>

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

Was this helpful?

supported.

---

# No Before Interactive Script Outside Document

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Before Interactive Script Outside Document

# No Before Interactive Script Outside Document

> Prevent usage of `next/script`'s `beforeInteractive` strategy outside of `app/layout.jsx` or `pages/_document.js`.

## Why This Error Occurred

You cannot use the `next/script` component with the `beforeInteractive` strategy outside `app/layout.jsx` or `pages/_document.js`. That's because `beforeInteractive` strategy only works inside **app/layout.jsx** or **pages/_document.js** and is designed to load scripts that are needed by the entire site (i.e. the script will load when any page in the application has been loaded server-side).

## Possible Ways to Fix It

### App Router

If you want a global script, and you are using the App Router, move the script inside `app/layout.jsx`.

 app/layout.jsx

```
import Script from 'next/script'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
      <Script
        src="https://example.com/script.js"
        strategy="beforeInteractive"
      />
    </html>
  )
}
```

### Pages Router

If you want a global script, and you are using the Pages Router, move the script inside `pages/_document.js`.

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
        ></Script>
      </body>
    </Html>
  )
}
```

## Useful Links

- [App Router Script Optimization](https://nextjs.org/docs/app/guides/scripts)
- [Pages Router Script Optimization](https://nextjs.org/docs/pages/guides/scripts)

Was this helpful?

supported.

---

# No Cache Detected

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Cache Detected

# No Cache Detected

## Why This Error Occurred

A Next.js build was triggered in a continuous integration environment, but no cache was detected.

This results in slower builds and can hurt Next.js' filesystem cache of client-side bundles across builds.

## Possible Ways to Fix It

> **Note**: If this is a new project, or being built for the first time in your CI, you can ignore this error.
> However, you'll want to make sure it doesn't continue to happen and fix it if it does!

Follow the instructions in [CI Build Caching](https://nextjs.org/docs/pages/guides/ci-build-caching) to ensure your Next.js cache is persisted between builds.

Was this helpful?

supported.

---

# No CSS Tags

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No CSS Tags

# No CSS Tags

> Prevent manual stylesheet tags.

## Why This Error Occurred

A `link` element was used to link to an external stylesheet. This can negatively affect CSS resource loading on your webpage.

## Possible Ways to Fix It

There are multiple ways to include styles using Next.js' built-in CSS support, including the option to use `@import` within the root stylesheet that is imported in `pages/_app.js`:

 styles.css

```
/* Root stylesheet */
@import 'extra.css';

body {
  /* ... */
}
```

Another option is to use CSS Modules to import the CSS file scoped specifically to the component.

 pages/index.js

```
import styles from './extra.module.css'

export class Home {
  render() {
    return (
      <div>
        <button type="button" className={styles.active}>
          Open
        </button>
      </div>
    )
  }
}
```

Refer to the [Built-In CSS Support](https://nextjs.org/docs/app/getting-started/css) documentation to learn about all the ways to include CSS to your application.

Was this helpful?

supported.

---

# No Document Import in Page

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Document Import in Page

# No Document Import in Page

> Prevent importing `next/document` outside of `pages/_document.js`.

## Why This Error Occurred

`next/document` was imported in a page outside of `pages/_document.js` (or `pages/_document.tsx` if you are using TypeScript). This can cause unexpected issues in your application.

## Possible Ways to Fix It

Only import and use `next/document` within `pages/_document.js` (or `pages/_document.tsx`) to override the default `Document` component:

 pages/_document.js

```
import Document, { Html, Head, Main, NextScript } from 'next/document'

class MyDocument extends Document {
  //...
}

export default MyDocument
```

## Useful Links

- [Custom Document](https://nextjs.org/docs/pages/building-your-application/routing/custom-document)

Was this helpful?

supported.

---

# No Duplicate Head

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Duplicate Head

# No Duplicate Head

> Prevent duplicate usage of `<Head>` in `pages/_document.js`.

## Why This Error Occurred

More than a single instance of the `<Head />` component was used in a single custom document. This can cause unexpected behavior in your application.

## Possible Ways to Fix It

Only use a single `<Head />` component in your custom document in `pages/_document.js`.

 pages/_document.js

```
import Document, { Html, Head, Main, NextScript } from 'next/document'

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    //...
  }

  render() {
    return (
      <Html>
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default MyDocument
```

## Useful Links

- [Custom Document](https://nextjs.org/docs/pages/building-your-application/routing/custom-document)

Was this helpful?

supported.

---

# No Head Element

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Head Element

# No Head Element

> Prevent usage of `<head>` element.

## Why This Error Occurred

A `<head>` element was used to include page-level metadata, but this can cause unexpected behavior in a Next.js application. Use Next.js' built-in `next/head` component instead.

## Possible Ways to Fix It

Import and use the `<Head />` component:

 pages/index.js

```
import Head from 'next/head'

function Index() {
  return (
    <>
      <Head>
        <title>My page title</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
    </>
  )
}

export default Index
```

## Useful Links

- [next/head](https://nextjs.org/docs/pages/api-reference/components/head)

Was this helpful?

supported.

---

# No Head Import in Document

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Head Import in Document

# No Head Import in Document

> Prevent usage of `next/head` in `pages/_document.js`.

## Why This Error Occurred

`next/head` was imported in `pages/_document.js`. This can cause unexpected issues in your application.

## Possible Ways to Fix It

Only import and use `next/document` within `pages/_document.js` to override the default `Document` component. If you are importing `next/head` to use the `Head` component, import it from `next/document` instead in order to modify `<head>` code across all pages:

 pages/_document.js

```
import Document, { Html, Head, Main, NextScript } from 'next/document'

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    //...
  }

  render() {
    return (
      <Html>
        <Head></Head>
      </Html>
    )
  }
}

export default MyDocument
```

## Useful Links

- [Custom Document](https://nextjs.org/docs/pages/building-your-application/routing/custom-document)

Was this helpful?

supported.

---

# No HTML link for pages

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No HTML link for pages

# No HTML link for pages

> Prevent usage of `<a>` elements to navigate to internal Next.js pages.

## Why This Error Occurred

An `<a>` element was used to navigate to a page route without using the `next/link` component, causing unnecessary full-page refreshes.

The `Link` component is required to enable client-side route transitions between pages and provide a single-page app experience.

## Possible Ways to Fix It

Make sure to import the `Link` component and wrap anchor elements that route to different page routes.

**Before:**

 pages/index.js

```
function Home() {
  return (
    <div>
      <a href="/about">About Us</a>
    </div>
  )
}
```

**After:**

 pages/index.js

```
import Link from 'next/link'

function Home() {
  return (
    <div>
      <Link href="/about">About Us</Link>
    </div>
  )
}

export default Home
```

### Options

#### pagesDir

This rule can normally locate your `pages` directory automatically.

If you're working in a monorepo, we recommend configuring the [rootDir](https://nextjs.org/docs/pages/api-reference/config/eslint#specifying-a-root-directory-within-a-monorepo) setting in `eslint-plugin-next`, which `pagesDir` will use to locate your `pages` directory.

In some cases, you may also need to configure this rule directly by providing a `pages` directory. This can be a path or an array of paths.

 eslint.config.json

```
{
  "rules": {
    "@next/next/no-html-link-for-pages": ["error", "packages/my-app/pages/"]
  }
}
```

## Useful Links

- [next/link API Reference](https://nextjs.org/docs/pages/api-reference/components/link)

Was this helpful?

supported.

---

# No img element

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No img element

# No img element

> Prevent usage of `<img>` element due to slower LCP and higher bandwidth.

## Why This Error Occurred

An `<img>` element was used to display an image instead of `<Image />` from `next/image`.

## Possible Ways to Fix It

1. Use [next/image](https://nextjs.org/docs/pages/api-reference/components/image) to improve performance with automatic [Image Optimization](https://nextjs.org/docs/pages/api-reference/components/image).

> **Note**: If deploying to a [managed hosting provider](https://nextjs.org/docs/pages/getting-started/deploying), remember to check provider pricing since optimized images might be charged differently than the original images.
>
>
>
> Common image optimization platform pricing:
>
>
>
> - [Vercel pricing](https://vercel.com/pricing)
> - [Cloudinary pricing](https://cloudinary.com/pricing)
> - [imgix pricing](https://imgix.com/pricing)

> **Note**: If self-hosting, remember to install [sharp](https://www.npmjs.com/package/sharp) and check if your server has enough storage to cache the optimized images.

 pages/index.js

```
import Image from 'next/image'

function Home() {
  return (
    <Image
      src="https://example.com/hero.jpg"
      alt="Landscape picture"
      width={800}
      height={500}
    />
  )
}

export default Home
```

1. If you would like to use `next/image` features such as blur-up placeholders but disable Image Optimization, you can do so using [unoptimized](https://nextjs.org/docs/pages/api-reference/components/image#unoptimized):

 pages/index.js

```
import Image from 'next/image'

const UnoptimizedImage = (props) => {
  return <Image {...props} unoptimized />
}
```

1. You can also use the `<picture>` element with the nested `<img>` element:

 pages/index.js

```
function Home() {
  return (
    <picture>
      <source srcSet="https://example.com/hero.avif" type="image/avif" />
      <source srcSet="https://example.com/hero.webp" type="image/webp" />
      <img
        src="https://example.com/hero.jpg"
        alt="Landscape picture"
        width={800}
        height={500}
      />
    </picture>
  )
}
```

1. You can use a [custom image loader](https://nextjs.org/docs/pages/api-reference/components/image#loader) to optimize images. Set [loaderFile](https://nextjs.org/docs/pages/api-reference/components/image#loaderfile) to the path of your custom loader.

 next.config.js

```
module.exports = {
  images: {
    loader: 'custom',
    loaderFile: './my/image/loader.js',
  },
}
```

## Useful Links

- [Image Component and Image Optimization](https://nextjs.org/docs/pages/api-reference/components/image)
- [next/image API Reference](https://nextjs.org/docs/pages/api-reference/components/image)
- [Largest Contentful Paint (LCP)](https://nextjs.org/learn/seo/web-performance/lcp)
- [Next.js config loaderFile option](https://nextjs.org/docs/pages/api-reference/components/image#loaderfile)

Was this helpful?

supported.

---

# No Page Custom Font

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Page Custom Font

# No Page Custom Font

> Prevent page-only custom fonts.

## Why This Error Occurred

- The custom font you're adding was added to a page - this only adds the font to the specific page and not the entire application.
- The custom font you're adding was added to a separate component within `pages/_document.js` - this disables automatic font optimization.

## Possible Ways to Fix It

Create the file `./pages/_document.js` and add the font to a custom Document:

 pages/_document.js

```
import Document, { Html, Head, Main, NextScript } from 'next/document'

class MyDocument extends Document {
  render() {
    return (
      <Html>
        <Head>
          <link
            href="https://fonts.googleapis.com/css2?family=Inter&display=optional"
            rel="stylesheet"
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default MyDocument
```

Or as a function component:

 pages/_document.js

```
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html>
      <Head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter&display=optional"
          rel="stylesheet"
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

### When Not To Use It

If you have a reason to only load a font for a particular page or don't care about font optimization, then you can disable this rule.

## Useful Links

- [Custom Document](https://nextjs.org/docs/pages/building-your-application/routing/custom-document)
- [Font Optimization](https://nextjs.org/docs/pages/api-reference/components/font)

Was this helpful?

supported.

---

# No Script Component in Head

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Script Component in Head

# No Script Component in Head

> Prevent usage of `next/script` in `next/head` component.

## Why This Error Occurred

The `next/script` component should not be used in a `next/head` component.

## Possible Ways to Fix It

Move the `<Script />` component outside of `<Head>` instead.

**Before**

 pages/index.js

```
import Script from 'next/script'
import Head from 'next/head'

export default function Index() {
  return (
    <Head>
      <title>Next.js</title>
      <Script src="/my-script.js" />
    </Head>
  )
}
```

**After**

 pages/index.js

```
import Script from 'next/script'
import Head from 'next/head'

export default function Index() {
  return (
    <>
      <Head>
        <title>Next.js</title>
      </Head>
      <Script src="/my-script.js" />
    </>
  )
}
```

## Useful Links

- [next/head](https://nextjs.org/docs/pages/api-reference/components/head)
- [next/script](https://nextjs.org/docs/pages/guides/scripts)

Was this helpful?

supported.

---

# No `styled

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No `styled-jsx` in `_document`

# No `styled-jsx` in `_document`

> Prevent usage of `styled-jsx` in `pages/_document.js`.

## Why This Error Occurred

Custom CSS like `styled-jsx` is not allowed in a [Custom Document](https://nextjs.org/docs/pages/building-your-application/routing/custom-document).

## Possible Ways to Fix It

If you need shared CSS for all of your pages, take a look at the [CustomApp](https://nextjs.org/docs/pages/building-your-application/routing/custom-app) file or define a custom layout.

For example, consider the following stylesheet named `styles.css`:

 styles.css

```
body {
  font-family:
    'SF Pro Text', 'SF Pro Icons', 'Helvetica Neue', 'Helvetica', 'Arial',
    sans-serif;
  padding: 20px 20px 60px;
  max-width: 680px;
  margin: 0 auto;
}
```

Create a `pages/_app.{js,tsx}` file if not already present. Then, import the `styles.css` file.

 pages/_app.js

```
import '../styles.css'

// This default export is required in a new `pages/_app.js` file.
export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}
```

These styles (`styles.css`) will apply to all pages and components in your application.

## Useful Links

- [Custom Document Caveats](https://nextjs.org/docs/pages/building-your-application/routing/custom-document#caveats)
- [Layouts](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts#layout-pattern)
- [Built in CSS Support](https://nextjs.org/docs/app/getting-started/css)
- [CustomApp](https://nextjs.org/docs/pages/building-your-application/routing/custom-app)

Was this helpful?

supported.

---

# No Sync Scripts

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Sync Scripts

# No Sync Scripts

> Prevent synchronous scripts.

## Why This Error Occurred

A synchronous script was used which can impact your webpage performance.

## Possible Ways to Fix It

### Script component (recommended)

 pages/index.js

```
import Script from 'next/script'

function Home() {
  return (
    <div class="container">
      <Script src="https://third-party-script.js"></Script>
      <div>Home Page</div>
    </div>
  )
}

export default Home
```

### Useasyncordefer

```
<script src="https://third-party-script.js" async />
<script src="https://third-party-script.js" defer />
```

## Useful Links

- [Efficiently load third-party JavaScript](https://web.dev/efficiently-load-third-party-javascript/)

Was this helpful?

supported.

---

# No Title in Document Head

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Title in Document Head

# No Title in Document Head

> Prevent usage of `<title>` with `Head` component from `next/document`.

## Why This Error Occurred

A `<title>` element was defined within the `Head` component imported from `next/document`, which should only be used for any `<head>` code that is common for all pages. Title tags should be defined at the page-level using `next/head` instead.

## Possible Ways to Fix It

Within a page or component, import and use `next/head` to define a page title:

 pages/index.js

```
import Head from 'next/head'

export function Home() {
  return (
    <div>
      <Head>
        <title>My page title</title>
      </Head>
    </div>
  )
}
```

## Useful Links

- [next/head](https://nextjs.org/docs/pages/api-reference/components/head)
- [Custom Document](https://nextjs.org/docs/pages/building-your-application/routing/custom-document)

Was this helpful?

supported.

---

# No Unwanted Polyfill.io

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)No Unwanted Polyfill.io

# No Unwanted Polyfill.io

> Prevent duplicate polyfills from Polyfill.io.

## Why This Error Occurred

You are using polyfills from Polyfill.io and including polyfills already shipped with Next.js. This unnecessarily increases page weight which can affect loading performance.

## Possible Ways to Fix It

Remove all duplicate polyfills. If you need to add polyfills but are not sure if Next.js already includes it, take a look at the list of [supported browsers and features](https://nextjs.org/docs/architecture/supported-browsers).

## Useful Links

- [Supported Browsers and Features](https://nextjs.org/docs/architecture/supported-browsers)

Was this helpful?

supported.

---

# Dynamic APIs are Asynchronous

> Learn more about why accessing certain APIs synchronously now warns.

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Dynamic APIs are Asynchronous

# Dynamic APIs are Asynchronous

Learn more about why accessing certain APIs synchronously now warns.

## Why This Warning Occurred

Somewhere in your code you used an API that opts into [dynamic rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering).

Dynamic APIs are:

- The `params` and `searchParams` props that get provided to pages, layouts, metadata APIs, and route handlers.
- `cookies()`, `draftMode()`, and `headers()` from `next/headers`

In Next 15, these APIs have been made asynchronous. You can read more about this in the Next.js 15 [Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-15).

For example, the following code will issue a warning:

 app/[id]/page.js

```
function Page({ params }) {
  // direct access of `params.id`.
  return <p>ID: {params.id}</p>
}
```

This also includes enumerating (e.g. `{...params}`, or `Object.keys(params)`) or iterating over the return
value of these APIs (e.g. `[...headers()]` or `for (const cookie of cookies())`, or explicitly with `cookies()[Symbol.iterator]()`).

## Possible Ways to Fix It

The [next-async-request-apicodemod](https://nextjs.org/docs/app/guides/upgrading/codemods#next-async-request-api) can fix many of these cases automatically:

 Terminal

```
npx @next/codemod@canary next-async-request-api .
```

The codemod cannot cover all cases, so you may need to manually adjust some code.

If the warning occurred on the Server (e.g. a route handler, or a Server Component),
you must `await` the dynamic API to access its properties:

 app/[id]/page.js

```
async function Page({ params }) {
  // asynchronous access of `params.id`.
  const { id } = await params
  return <p>ID: {id}</p>
}
```

If the warning occurred in a synchronous component (e.g. a Client component),
you must use `React.use()` to unwrap the Promise first:

 app/[id]/page.js

```
'use client'
import * as React from 'react'

function Page({ params }) {
  // asynchronous access of `params.id`.
  const { id } = React.use(params)
  return <p>ID: {id}</p>
}
```

### Unmigratable Cases

If Next.js codemod found anything that is not able to be migrated by the codemod, it will leave a comment with `@next-codemod-error` prefix and the suggested action, for example:
In this case, you need to manually await the call to `cookies()`, and change the function to async. Then refactor the usages of the function to be properly awaited:

```
export function MyCookiesComponent() {
  const c =
    /* @next-codemod-error Manually await this call and refactor the function to be async */
    cookies()
  return c.get('name')
}
```

### Enforced Migration with Linter

If you didn't address the comments that starting with `@next-codemod-error` left by the codemod, Next.js will error in both dev and build to enforce you to address the issues.
You can review the changes and follow the suggestion in the comments. You can either make the necessary changes and remove the comment, or replace the comment prefix `@next-codemod-error` with `@next-codemod-ignore`
If there's no action to be taken, the comment prefix `@next-codemod-ignore` will bypass the build error.

```
- /* @next-codemod-error <suggested message> */
+ /* @next-codemod-ignore */
```

> **Good to know**:
>
>
>
> You can delay unwrapping the Promise (either with `await` or `React.use`) until you actually need to consume the value.
> This will allow Next.js to statically render more of your page.

Was this helpful?

supported.

---

# `url` is deprecated

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)`url` is deprecated

# `url` is deprecated

## Why This Error Occurred

In versions prior to 6.x the `url` property got magically injected into every `Page` component (every page inside the `pages` directory).

The reason this is going away is that we want to make things very predictable and explicit. Having a magical url property coming out of nowhere doesn't aid that goal.

> **Note**: ⚠️ In some cases using React Dev Tools may trigger this warning even if you do not reference `url` anywhere in your code. Try temporarily disabling the extension and see if the warning persists.

## Possible Ways to Fix It

Since Next 5 we provide a way to explicitly inject the Next.js router object into pages and all their descending components.
The `router` property that is injected will hold the same values as `url`, like `pathname`, `asPath`, and `query`.

Here's an example of using `withRouter`:

 pages/index.js

```
import { withRouter } from 'next/router'

class Page extends React.Component {
  render() {
    const { router } = this.props
    console.log(router)
    return <div>{router.pathname}</div>
  }
}

export default withRouter(Page)
```

We provide a codemod (a code to code transformation) to automatically change the `url` property usages to `withRouter`.

You can find this codemod and instructions on how to run it here: [UsewithRouter](https://nextjs.org/docs/pages/guides/upgrading/codemods#url-to-withrouter)

Was this helpful?

supported.

---

# Webpack 5 Adoption

[Docs](https://nextjs.org/docs)[Errors](https://nextjs.org/docs)Webpack 5 Adoption

# Webpack 5 Adoption

## Why This Message Occurred

Next.js has adopted webpack 5 as the default for compilation. We've spent a lot of effort into ensuring the transition from webpack 4 to 5 will be as smooth as possible.

Your application currently has webpack 5 disabled using the `webpack5: false` flag which has been removed in Next.js 12:

 next.config.js

```
module.exports = {
  // Webpack 5 is enabled by default
  // You can still use webpack 4 while upgrading to the latest version of Next.js by adding the "webpack5: false" flag
  webpack5: false,
}
```

Using webpack 5 in your application has many benefits, notably:

- Improved Disk Caching: `next build` is significantly faster on subsequent builds
- Improved Fast Refresh: Fast Refresh work is prioritized
- Improved Long Term Caching of Assets: Deterministic code output that is less likely to change between builds
- Improved Tree Shaking
- Support for assets using `new URL("file.png", import.meta.url)`
- Support for web workers using `new Worker(new URL("worker.js", import.meta.url))`
- Support for `exports`/`imports` field in `package.json`

In the past releases we have gradually rolled out webpack 5 to Next.js applications:

- In Next.js 10.2 we automatically opted-in applications without custom webpack configuration in `next.config.js`
- In Next.js 10.2 we automatically opted-in applications that do not have a `next.config.js`
- In Next.js 11 webpack 5 was enabled by default for all applications. You could still opt-out and use webpack 4 to help with backwards compatibility using `webpack5: false` in `next.config.js`
- In Next.js 12 webpack 4 support was removed.

## Custom webpack configuration

In case you do have custom webpack configuration, either through custom plugins or your own modifications you'll have to take a few steps to ensure your applications works with webpack 5.

- When using `next-transpile-modules` make sure you use the latest version which includes [this patch](https://github.com/martpie/next-transpile-modules/pull/179)
- When using `@zeit/next-css` / `@zeit/next-sass` make sure you use the [built-in CSS/Sass support](https://nextjs.org/docs/app/getting-started/css) instead
- When using `@zeit/next-preact` use [this example](https://github.com/vercel/next.js/tree/canary/examples/using-preact) instead
- When using `@zeit/next-source-maps` use the [built-in production Source Map support](https://nextjs.org/docs/pages/api-reference/config/next-config-js/productionBrowserSourceMaps)
- When using webpack plugins make sure they're upgraded to the latest version, in most cases the latest version will include webpack 5 support. In some cases these upgraded webpack plugins will only support webpack 5.

## Useful Links

In case you're running into issues you can connect with the community in [this help discussion](https://github.com/vercel/next.js/discussions/23498).

Was this helpful?

supported.
