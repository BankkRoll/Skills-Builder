# How to migrate from Create React App to Next.js and more

# How to migrate from Create React App to Next.js

> Learn how to migrate your existing React application from Create React App to Next.js.

[Guides](https://nextjs.org/docs/app/guides)[Migrating](https://nextjs.org/docs/app/guides/migrating)Create React App

# How to migrate from Create React App to Next.js

Last updated  October 17, 2025

This guide will help you migrate an existing Create React App (CRA) site to Next.js.

## Why Switch?

There are several reasons why you might want to switch from Create React App to Next.js:

### Slow initial page loading time

Create React App uses purely client-side rendering. Client-side only applications, also known as [single-page applications (SPAs)](https://nextjs.org/docs/app/guides/single-page-applications), often experience slow initial page loading time. This happens due to a couple of reasons:

1. The browser needs to wait for the React code and your entire application bundle to download and run before your code is able to send requests to load data.
2. Your application code grows with every new feature and dependency you add.

### No automatic code splitting

The previous issue of slow loading times can be somewhat mitigated with code splitting. However, if you try to do code splitting manually, you can inadvertently introduce network waterfalls. Next.js provides automatic code splitting and tree-shaking built into its router and build pipeline.

### Network waterfalls

A common cause of poor performance occurs when applications make sequential client-server requests to fetch data. One pattern for data fetching in a [SPA](https://nextjs.org/docs/app/guides/single-page-applications) is to render a placeholder, and then fetch data after the component has mounted. Unfortunately, a child component can only begin fetching data after its parent has finished loading its own data, resulting in a “waterfall” of requests.

While client-side data fetching is supported in Next.js, Next.js also lets you move data fetching to the server. This often eliminates client-server waterfalls altogether.

### Fast and intentional loading states

With built-in support for [streaming through React Suspense](https://nextjs.org/docs/app/getting-started/linking-and-navigating#streaming), you can define which parts of your UI load first and in what order, without creating network waterfalls.

This enables you to build pages that are faster to load and eliminate [layout shifts](https://vercel.com/blog/how-core-web-vitals-affect-seo).

### Choose the data fetching strategy

Depending on your needs, Next.js allows you to choose your data fetching strategy on a page or component-level basis. For example, you could fetch data from your CMS and render blog posts at build time (SSG) for quick load speeds, or fetch data at request time (SSR) when necessary.

### Proxy

[Next.js Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) allows you to run code on the server before a request is completed. For instance, you can avoid a flash of unauthenticated content by redirecting a user to a login page in the proxy for authenticated-only pages. You can also use it for features like A/B testing, experimentation, and [internationalization](https://nextjs.org/docs/app/guides/internationalization).

### Built-in Optimizations

[Images](https://nextjs.org/docs/app/api-reference/components/image), [fonts](https://nextjs.org/docs/app/api-reference/components/font), and [third-party scripts](https://nextjs.org/docs/app/guides/scripts) often have a large impact on an application’s performance. Next.js includes specialized components and APIs that automatically optimize them for you.

## Migration Steps

Our goal is to get a working Next.js application as quickly as possible so that you can then adopt Next.js features incrementally. To begin with, we’ll treat your application as a purely client-side application ([SPA](https://nextjs.org/docs/app/guides/single-page-applications)) without immediately replacing your existing router. This reduces complexity and merge conflicts.

> **Note**: If you are using advanced CRA configurations such as a custom `homepage` field in your `package.json`, a custom service worker, or specific Babel/webpack tweaks, please see the **Additional Considerations** section at the end of this guide for tips on replicating or adapting these features in Next.js.

### Step 1: Install the Next.js Dependency

Install Next.js in your existing project:

 Terminal

```
npm install next@latest
```

### Step 2: Create the Next.js Configuration File

Create a `next.config.ts` at the root of your project (same level as your `package.json`). This file holds your [Next.js configuration options](https://nextjs.org/docs/app/api-reference/config/next-config-js).

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'export', // Outputs a Single-Page Application (SPA)
  distDir: 'build', // Changes the build output directory to `build`
}

export default nextConfig
```

> **Note**: Using `output: 'export'` means you’re doing a static export. You will **not** have access to server-side features like SSR or APIs. You can remove this line to leverage Next.js server features.

### Step 3: Create the Root Layout

A Next.js [App Router](https://nextjs.org/docs/app) application must include a [root layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout) file, which is a [React Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) that will wrap all your pages.

The closest equivalent of the root layout file in a CRA application is `public/index.html`, which includes your `<html>`, `<head>`, and `<body>` tags.

1. Create a new `app` directory inside your `src` folder (or at your project root if you prefer `app` at the root).
2. Inside the `app` directory, create a `layout.tsx` (or `layout.js`) file:

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return '...'
}
```

Now copy the content of your old `index.html` into this `<RootLayout>` component. Replace `body div#root` (and `body noscript`) with `<div id="root">{children}</div>`.

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="UTF-8" />
        <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>React App</title>
        <meta name="description" content="Web site created..." />
      </head>
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

> **Good to know**: Next.js ignores CRA’s `public/manifest.json`, additional iconography, and [testing configuration](https://nextjs.org/docs/app/guides/testing) by default. If you need these, Next.js has support with its [Metadata API](https://nextjs.org/docs/app/getting-started/metadata-and-og-images) and [Testing](https://nextjs.org/docs/app/guides/testing) setup.

### Step 4: Metadata

Next.js automatically includes the `<meta charset="UTF-8" />` and `<meta name="viewport" content="width=device-width, initial-scale=1" />` tags, so you can remove them from `<head>`:

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
        <title>React App</title>
        <meta name="description" content="Web site created..." />
      </head>
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

Any [metadata files](https://nextjs.org/docs/app/getting-started/metadata-and-og-images#file-based-metadata) such as `favicon.ico`, `icon.png`, `robots.txt` are automatically added to the application `<head>` tag as long as you have them placed into the top level of the `app` directory. After moving [all supported files](https://nextjs.org/docs/app/getting-started/metadata-and-og-images#file-based-metadata) into the `app` directory you can safely delete their `<link>` tags:

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <title>React App</title>
        <meta name="description" content="Web site created..." />
      </head>
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

Finally, Next.js can manage your last `<head>` tags with the [Metadata API](https://nextjs.org/docs/app/getting-started/metadata-and-og-images). Move your final metadata info into an exported [metadataobject](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#metadata-object):

 app/layout.tsxJavaScriptTypeScript

```
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'React App',
  description: 'Web site created with Next.js.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

With the above changes, you shifted from declaring everything in your `index.html` to using Next.js' convention-based approach built into the framework ([Metadata API](https://nextjs.org/docs/app/getting-started/metadata-and-og-images)). This approach enables you to more easily improve your SEO and web shareability of your pages.

### Step 5: Styles

Like CRA, Next.js supports [CSS Modules](https://nextjs.org/docs/app/getting-started/css#css-modules) out of the box. It also supports [global CSS imports](https://nextjs.org/docs/app/getting-started/css#global-css).

If you have a global CSS file, import it into your `app/layout.tsx`:

 app/layout.tsxJavaScriptTypeScript

```
import '../index.css'

export const metadata = {
  title: 'React App',
  description: 'Web site created with Next.js.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

If you're using Tailwind CSS, see our [installation docs](https://nextjs.org/docs/app/getting-started/css#tailwind-css).

### Step 6: Create the Entrypoint Page

Create React App uses `src/index.tsx` (or `index.js`) as the entry point. In Next.js (App Router), each folder inside the `app` directory corresponds to a route, and each folder should have a `page.tsx`.

Since we want to keep the app as an SPA for now and intercept **all** routes, we’ll use an [optional catch-all route](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#optional-catch-all-segments).

1. **Create a[[...slug]]directory insideapp.**

```
app
 ┣ [[...slug]]
 ┃ ┗ page.tsx
 ┣ layout.tsx
```

1. **Add the following topage.tsx**:

 app/[[...slug]]/page.tsxJavaScriptTypeScript

```
export function generateStaticParams() {
  return [{ slug: [''] }]
}

export default function Page() {
  return '...' // We'll update this
}
```

This tells Next.js to generate a single route for the empty slug (`/`), effectively mapping **all** routes to the same page. This page is a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components), prerendered into static HTML.

### Step 7: Add a Client-Only Entrypoint

Next, we’ll embed your CRA’s root App component inside a [Client Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) so that all logic remains client-side. If this is your first time using Next.js, it's worth knowing that clients components (by default) are still prerendered on the server. You can think about them as having the additional capability of running client-side JavaScript.

Create a `client.tsx` (or `client.js`) in `app/[[...slug]]/`:

 app/[[...slug]]/client.tsxJavaScriptTypeScript

```
'use client'

import dynamic from 'next/dynamic'

const App = dynamic(() => import('../../App'), { ssr: false })

export function ClientOnly() {
  return <App />
}
```

- The `'use client'` directive makes this file a **Client Component**.
- The `dynamic` import with `ssr: false` disables server-side rendering for the `<App />` component, making it truly client-only (SPA).

Now update your `page.tsx` (or `page.js`) to use your new component:

 app/[[...slug]]/page.tsxJavaScriptTypeScript

```
import { ClientOnly } from './client'

export function generateStaticParams() {
  return [{ slug: [''] }]
}

export default function Page() {
  return <ClientOnly />
}
```

### Step 8: Update Static Image Imports

In CRA, importing an image file returns its public URL as a string:

```
import image from './img.png'

export default function App() {
  return <img src={image} />
}
```

With Next.js, static image imports return an object. The object can then be used directly with the Next.js [<Image>component](https://nextjs.org/docs/app/api-reference/components/image), or you can use the object's `src` property with your existing `<img>` tag.

The `<Image>` component has the added benefits of [automatic image optimization](https://nextjs.org/docs/app/api-reference/components/image). The `<Image>` component automatically sets the `width` and `height` attributes of the resulting `<img>` based on the image's dimensions. This prevents layout shifts when the image loads. However, this can cause issues if your app contains images with only one of their dimensions being styled without the other styled to `auto`. When not styled to `auto`, the dimension will default to the `<img>` dimension attribute's value, which can cause the image to appear distorted.

Keeping the `<img>` tag will reduce the amount of changes in your application and prevent the above issues. You can then optionally later migrate to the `<Image>` component to take advantage of optimizing images by [configuring a loader](https://nextjs.org/docs/app/api-reference/components/image#loader), or moving to the default Next.js server which has automatic image optimization.

**Convert absolute import paths for images imported from/publicinto relative imports:**

```
// Before
import logo from '/logo.png'

// After
import logo from '../public/logo.png'
```

**Pass the imagesrcproperty instead of the whole image object to your<img>tag:**

```
// Before
<img src={logo} />

// After
<img src={logo.src} />
```

Alternatively, you can reference the public URL for the image asset based on the filename. For example, `public/logo.png` will serve the image at `/logo.png` for your application, which would be the `src` value.

> **Warning:** If you're using TypeScript, you might encounter type errors when accessing the `src` property. To fix them, you need to add `next-env.d.ts` to the [includearray](https://www.typescriptlang.org/tsconfig#include) of your `tsconfig.json` file. Next.js will automatically generate this file when you run your application on step 9.

### Step 9: Migrate Environment Variables

Next.js supports [environment variables](https://nextjs.org/docs/app/guides/environment-variables) similarly to CRA but **requires** a `NEXT_PUBLIC_` prefix for any variable you want to expose in the browser.

The main difference is the prefix used to expose environment variables on the client-side. Change all environment variables with the `REACT_APP_` prefix to `NEXT_PUBLIC_`.

### Step 10: Update Scripts inpackage.json

Update your `package.json` scripts to use Next.js commands. Also, add `.next` and `next-env.d.ts` to your `.gitignore`:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "npx serve@latest ./build"
  }
}
```

 .gitignore

```
# ...
.next
next-env.d.ts
```

Now you can run:

```
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). You should see your application now running on Next.js (in SPA mode).

### Step 11: Clean Up

You can now remove artifacts that are specific to Create React App:

- `public/index.html`
- `src/index.tsx`
- `src/react-app-env.d.ts`
- The `reportWebVitals` setup
- The `react-scripts` dependency (uninstall it from `package.json`)

## Additional Considerations

### Using a Customhomepagein CRA

If you used the `homepage` field in your CRA `package.json` to serve the app under a specific subpath, you can replicate that in Next.js using the [basePathconfiguration](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath) in `next.config.ts`:

 next.config.ts

```
import { NextConfig } from 'next'

const nextConfig: NextConfig = {
  basePath: '/my-subpath',
  // ...
}

export default nextConfig
```

### Handling a CustomService Worker

If you used CRA’s service worker (e.g., `serviceWorker.js` from `create-react-app`), you can learn how to create [Progressive Web Applications (PWAs)](https://nextjs.org/docs/app/guides/progressive-web-apps) with Next.js.

### Proxying API Requests

If your CRA app used the `proxy` field in `package.json` to forward requests to a backend server, you can replicate this with [Next.js rewrites](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites) in `next.config.ts`:

 next.config.ts

```
import { NextConfig } from 'next'

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://your-backend.com/:path*',
      },
    ]
  },
}
```

### Custom Webpack

If you had a custom webpack or Babel configuration in CRA, you can extend Next.js’s config in `next.config.ts`:

 next.config.ts

```
import { NextConfig } from 'next'

const nextConfig: NextConfig = {
  webpack: (config, { isServer }) => {
    // Modify the webpack config here
    return config
  },
}

export default nextConfig
```

> **Note**: This will require using Webpack by adding `--webpack` to your `dev` script.

### TypeScript Setup

Next.js automatically sets up TypeScript if you have a `tsconfig.json`. Make sure `next-env.d.ts` is listed in your `tsconfig.json` `include` array:

```
{
  "include": ["next-env.d.ts", "app/**/*", "src/**/*"]
}
```

## Bundler Compatibility

Create React App uses webpack for bundling. Next.js now defaults to [Turbopack](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack) for faster local development:

```
next dev  # Uses Turbopack by default
```

To use Webpack instead (similar to CRA):

```
next dev --webpack
```

You can still provide a [custom webpack configuration](https://nextjs.org/docs/app/api-reference/config/next-config-js/webpack) if you need to migrate advanced webpack settings from CRA.

## Next Steps

If everything worked, you now have a functioning Next.js application running as a single-page application. You aren’t yet leveraging Next.js features like server-side rendering or file-based routing, but you can now do so incrementally:

- **Migrate from React Router** to the [Next.js App Router](https://nextjs.org/docs/app) for:
  - Automatic code splitting
  - [Streaming server rendering](https://nextjs.org/docs/app/api-reference/file-conventions/loading)
  - [React Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- **Optimize images** with the [<Image>component](https://nextjs.org/docs/app/api-reference/components/image)
- **Optimize fonts** with [next/font](https://nextjs.org/docs/app/api-reference/components/font)
- **Optimize third-party scripts** with the [<Script>component](https://nextjs.org/docs/app/guides/scripts)
- **Enable ESLint** with Next.js [recommended rules](https://nextjs.org/docs/app/api-reference/config/eslint#setup-eslint)

> **Note**: Using a static export (`output: 'export'`) [does not currently support](https://github.com/vercel/next.js/issues/54393) the `useParams` hook or other server features. To use all Next.js features, remove `output: 'export'` from your `next.config.ts`.

Was this helpful?

supported.

---

# How to migrate from Vite to Next.js

> Learn how to migrate your existing React application from Vite to Next.js.

[Guides](https://nextjs.org/docs/app/guides)[Migrating](https://nextjs.org/docs/app/guides/migrating)Vite

# How to migrate from Vite to Next.js

Last updated  October 17, 2025

This guide will help you migrate an existing Vite application to Next.js.

## Why Switch?

There are several reasons why you might want to switch from Vite to Next.js:

### Slow initial page loading time

If you have built your application with the [default Vite plugin for React](https://github.com/vitejs/vite-plugin-react/tree/main/packages/plugin-react), your application is a purely client-side application. Client-side only applications, also known as single-page applications (SPAs), often experience slow initial page loading time. This happens due to a couple of reasons:

1. The browser needs to wait for the React code and your entire application bundle to download and run before your code is able to send requests to load some data.
2. Your application code grows with every new feature and extra dependency you add.

### No automatic code splitting

The previous issue of slow loading times can be somewhat managed with code splitting. However, if you try to do code splitting manually, you'll often make performance worse. It's easy to inadvertently introduce network waterfalls when code-splitting manually. Next.js provides automatic code splitting built into its router.

### Network waterfalls

A common cause of poor performance occurs when applications make sequential client-server requests to fetch data. One common pattern for data fetching in an SPA is to initially render a placeholder, and then fetch data after the component has mounted. Unfortunately, this means that a child component that fetches data can't start fetching until the parent component has finished loading its own data.

While fetching data on the client is supported with Next.js, it also gives you the option to shift data fetching to the server, which can eliminate client-server waterfalls.

### Fast and intentional loading states

With built-in support for [streaming through React Suspense](https://nextjs.org/docs/app/getting-started/linking-and-navigating#streaming), you can be more intentional about which parts of your UI you want to load first and in what order without introducing network waterfalls.

This enables you to build pages that are faster to load and eliminate [layout shifts](https://vercel.com/blog/how-core-web-vitals-affect-seo).

### Choose the data fetching strategy

Depending on your needs, Next.js allows you to choose your data fetching strategy on a page and component basis. You can decide to fetch at build time, at request time on the server, or on the client. For example, you can fetch data from your CMS and render your blog posts at build time, which can then be efficiently cached on a CDN.

### Proxy

[Next.js Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) allows you to run code on the server before a request is completed. This is especially useful to avoid having a flash of unauthenticated content when the user visits an authenticated-only page by redirecting the user to a login page. The proxy is also useful for experimentation and [internationalization](https://nextjs.org/docs/app/guides/internationalization).

### Built-in Optimizations

[Images](https://nextjs.org/docs/app/api-reference/components/image), [fonts](https://nextjs.org/docs/app/api-reference/components/font), and [third-party scripts](https://nextjs.org/docs/app/guides/scripts) often have significant impact on an application's performance. Next.js comes with built-in components that automatically optimize those for you.

## Migration Steps

Our goal with this migration is to get a working Next.js application as quickly as possible, so that
you can then adopt Next.js features incrementally. To begin with, we'll keep it as a purely
client-side application (SPA) without migrating your existing router. This helps minimize the
chances of encountering issues during the migration process and reduces merge conflicts.

### Step 1: Install the Next.js Dependency

The first thing you need to do is to install `next` as a dependency:

 Terminal

```
npm install next@latest
```

### Step 2: Create the Next.js Configuration File

Create a `next.config.mjs` at the root of your project. This file will hold your
[Next.js configuration options](https://nextjs.org/docs/app/api-reference/config/next-config-js).

 next.config.mjs

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Outputs a Single-Page Application (SPA).
  distDir: './dist', // Changes the build output directory to `./dist/`.
}

export default nextConfig
```

> **Good to know:** You can use either `.js` or `.mjs` for your Next.js configuration file.

### Step 3: Update TypeScript Configuration

If you're using TypeScript, you need to update your `tsconfig.json` file with the following changes
to make it compatible with Next.js. If you're not using TypeScript, you can skip this step.

1. Remove the [project reference](https://www.typescriptlang.org/tsconfig#references) to `tsconfig.node.json`
2. Add `./dist/types/**/*.ts` and `./next-env.d.ts` to the [includearray](https://www.typescriptlang.org/tsconfig#include)
3. Add `./node_modules` to the [excludearray](https://www.typescriptlang.org/tsconfig#exclude)
4. Add `{ "name": "next" }` to the [pluginsarray incompilerOptions](https://www.typescriptlang.org/tsconfig#plugins): `"plugins": [{ "name": "next" }]`
5. Set [esModuleInterop](https://www.typescriptlang.org/tsconfig#esModuleInterop) to `true`: `"esModuleInterop": true`
6. Set [jsx](https://www.typescriptlang.org/tsconfig#jsx) to `react-jsx`: `"jsx": "react-jsx"`
7. Set [allowJs](https://www.typescriptlang.org/tsconfig#allowJs) to `true`: `"allowJs": true`
8. Set [forceConsistentCasingInFileNames](https://www.typescriptlang.org/tsconfig#forceConsistentCasingInFileNames) to `true`: `"forceConsistentCasingInFileNames": true`
9. Set [incremental](https://www.typescriptlang.org/tsconfig#incremental) to `true`: `"incremental": true`

Here's an example of a working `tsconfig.json` with those changes:

 tsconfig.json

```
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "allowJs": true,
    "forceConsistentCasingInFileNames": true,
    "incremental": true,
    "plugins": [{ "name": "next" }]
  },
  "include": ["./src", "./dist/types/**/*.ts", "./next-env.d.ts"],
  "exclude": ["./node_modules"]
}
```

You can find more information about configuring TypeScript on the
[Next.js docs](https://nextjs.org/docs/app/api-reference/config/typescript#ide-plugin).

### Step 4: Create the Root Layout

A Next.js [App Router](https://nextjs.org/docs/app) application must include a
[root layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout)
file, which is a [React Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components)
that will wrap all pages in your application. This file is defined at the top level of the `app`
directory.

The closest equivalent to the root layout file in a Vite application is the
[index.htmlfile](https://vitejs.dev/guide/#index-html-and-project-root), which contains your
`<html>`, `<head>`, and `<body>` tags.

In this step, you'll convert your `index.html` file into a root layout file:

1. Create a new `app` directory in your `src` folder.
2. Create a new `layout.tsx` file inside that `app` directory:

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return '...'
}
```

> **Good to know**: `.js`, `.jsx`, or `.tsx` extensions can be used for Layout files.

1. Copy the content of your `index.html` file into the previously created `<RootLayout>` component while
  replacing the `body.div#root` and `body.script` tags with `<div id="root">{children}</div>`:

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <link rel="icon" type="image/svg+xml" href="/icon.svg" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>My App</title>
        <meta name="description" content="My App is a..." />
      </head>
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

1. Next.js already includes by default the
  [meta charset](https://developer.mozilla.org/docs/Web/HTML/Element/meta#charset) and
  [meta viewport](https://developer.mozilla.org/docs/Web/HTML/Viewport_meta_tag) tags, so you
  can safely remove those from your `<head>`:

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" type="image/svg+xml" href="/icon.svg" />
        <title>My App</title>
        <meta name="description" content="My App is a..." />
      </head>
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

1. Any [metadata files](https://nextjs.org/docs/app/getting-started/metadata-and-og-images#file-based-metadata)
  such as `favicon.ico`, `icon.png`, `robots.txt` are automatically added to the application
  `<head>` tag as long as you have them placed into the top level of the `app` directory. After
  moving
  [all supported files](https://nextjs.org/docs/app/getting-started/metadata-and-og-images#file-based-metadata)
  into the `app` directory you can safely delete their `<link>` tags:

 app/layout.tsxJavaScriptTypeScript

```
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <title>My App</title>
        <meta name="description" content="My App is a..." />
      </head>
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

1. Finally, Next.js can manage your last `<head>` tags with the
  [Metadata API](https://nextjs.org/docs/app/getting-started/metadata-and-og-images). Move your final metadata
  info into an exported
  [metadataobject](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#metadata-object):

 app/layout.tsxJavaScriptTypeScript

```
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My App',
  description: 'My App is a...',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

With the above changes, you shifted from declaring everything in your `index.html` to using Next.js'
convention-based approach built into the framework
([Metadata API](https://nextjs.org/docs/app/getting-started/metadata-and-og-images)). This approach enables you
to more easily improve your SEO and web shareability of your pages.

### Step 5: Create the Entrypoint Page

On Next.js you declare an entrypoint for your application by creating a `page.tsx` file. The
closest equivalent of this file on Vite is your `main.tsx` file. In this step, you’ll set up the
entrypoint of your application.

1. **Create a[[...slug]]directory in yourappdirectory.**

Since in this guide we're aiming first to set up our Next.js as an SPA (Single Page Application), you need your page entrypoint to catch all possible routes of your application. For that, create a new `[[...slug]]` directory in your `app` directory.

This directory is what is called an [optional catch-all route segment](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes#optional-catch-all-segments). Next.js uses a file-system based router where folders are used to define routes. This special directory will make sure that all routes of your application will be directed to its containing `page.tsx` file.

1. **Create a newpage.tsxfile inside theapp/[[...slug]]directory with the following content:**

 app/[[...slug]]/page.tsxJavaScriptTypeScript

```
import '../../index.css'

export function generateStaticParams() {
  return [{ slug: [''] }]
}

export default function Page() {
  return '...' // We'll update this
}
```

> **Good to know**: `.js`, `.jsx`, or `.tsx` extensions can be used for Page files.

This file is a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components). When you run `next build`, the file is prerendered into a static asset. It does *not* require any dynamic code.

This file imports our global CSS and tells [generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params) we are only going to generate one route, the index route at `/`.

Now, let's move the rest of our Vite application which will run client-only.

 app/[[...slug]]/client.tsxJavaScriptTypeScript

```
'use client'

import React from 'react'
import dynamic from 'next/dynamic'

const App = dynamic(() => import('../../App'), { ssr: false })

export function ClientOnly() {
  return <App />
}
```

This file is a [Client Component](https://nextjs.org/docs/app/getting-started/server-and-client-components), defined by the `'use client'`
directive. Client Components are still [prerendered to HTML](https://nextjs.org/docs/app/getting-started/server-and-client-components#how-do-server-and-client-components-work-in-nextjs) on the server before being sent to the client.

Since we want a client-only application to start, we can configure Next.js to disable prerendering from the `App` component down.

```
const App = dynamic(() => import('../../App'), { ssr: false })
```

Now, update your entrypoint page to use the new component:

 app/[[...slug]]/page.tsxJavaScriptTypeScript

```
import '../../index.css'
import { ClientOnly } from './client'

export function generateStaticParams() {
  return [{ slug: [''] }]
}

export default function Page() {
  return <ClientOnly />
}
```

### Step 6: Update Static Image Imports

Next.js handles static image imports slightly different from Vite. With Vite, importing an image
file will return its public URL as a string:

 App.tsx

```
import image from './img.png' // `image` will be '/assets/img.2d8efhg.png' in production

export default function App() {
  return <img src={image} />
}
```

With Next.js, static image imports return an object. The object can then be used directly with the
Next.js [<Image>component](https://nextjs.org/docs/app/api-reference/components/image), or you can use the object's
`src` property with your existing `<img>` tag.

The `<Image>` component has the added benefits of
[automatic image optimization](https://nextjs.org/docs/app/api-reference/components/image). The `<Image>`
component automatically sets the `width` and `height` attributes of the resulting `<img>` based on
the image's dimensions. This prevents layout shifts when the image loads. However, this can cause
issues if your app contains images with only one of their dimensions being styled without the other
styled to `auto`. When not styled to `auto`, the dimension will default to the `<img>` dimension
attribute's value, which can cause the image to appear distorted.

Keeping the `<img>` tag will reduce the amount of changes in your application and prevent the above
issues. You can then optionally later migrate to the `<Image>` component to take advantage of optimizing images by [configuring a loader](https://nextjs.org/docs/app/api-reference/components/image#loader), or moving to the default Next.js server which has automatic image optimization.

1. **Convert absolute import paths for images imported from/publicinto relative imports:**

```
// Before
import logo from '/logo.png'

// After
import logo from '../public/logo.png'
```

1. **Pass the imagesrcproperty instead of the whole image object to your<img>tag:**

```
// Before
<img src={logo} />

// After
<img src={logo.src} />
```

Alternatively, you can reference the public URL for the image asset based on the filename. For example, `public/logo.png` will serve the image at `/logo.png` for your application, which would be the `src` value.

> **Warning:** If you're using TypeScript, you might encounter type errors when accessing the `src`
> property. You can safely ignore those for now. They will be fixed by the end of this guide.

### Step 7: Migrate the Environment Variables

Next.js has support for `.env` [environment variables](https://nextjs.org/docs/app/guides/environment-variables)
similar to Vite. The main difference is the prefix used to expose environment variables on the
client-side.

- Change all environment variables with the `VITE_` prefix to `NEXT_PUBLIC_`.

Vite exposes a few built-in environment variables on the special `import.meta.env` object which
aren’t supported by Next.js. You need to update their usage as follows:

- `import.meta.env.MODE` ⇒ `process.env.NODE_ENV`
- `import.meta.env.PROD` ⇒ `process.env.NODE_ENV === 'production'`
- `import.meta.env.DEV` ⇒ `process.env.NODE_ENV !== 'production'`
- `import.meta.env.SSR` ⇒ `typeof window !== 'undefined'`

Next.js also doesn't provide a built-in `BASE_URL` environment variable. However, you can still
configure one, if you need it:

1. **Add the following to your.envfile:**

 .env

```
# ...
NEXT_PUBLIC_BASE_PATH="/some-base-path"
```

1. **SetbasePathtoprocess.env.NEXT_PUBLIC_BASE_PATHin yournext.config.mjsfile:**

 next.config.mjs

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Outputs a Single-Page Application (SPA).
  distDir: './dist', // Changes the build output directory to `./dist/`.
  basePath: process.env.NEXT_PUBLIC_BASE_PATH, // Sets the base path to `/some-base-path`.
}

export default nextConfig
```

1. **Updateimport.meta.env.BASE_URLusages toprocess.env.NEXT_PUBLIC_BASE_PATH**

### Step 8: Update Scripts inpackage.json

You should now be able to run your application to test if you successfully migrated to Next.js. But
before that, you need to update your `scripts` in your `package.json` with Next.js related commands,
and add `.next` and `next-env.d.ts` to your `.gitignore`:

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

 .gitignore

```
# ...
.next
next-env.d.ts
dist
```

Now run `npm run dev`, and open [http://localhost:3000](http://localhost:3000). You should see your application now running on Next.js.

> **Example:** Check out [this pull request](https://github.com/inngest/vite-to-nextjs/pull/1) for a
> working example of a Vite application migrated to Next.js.

### Step 9: Clean Up

You can now clean up your codebase from Vite related artifacts:

- Delete `main.tsx`
- Delete `index.html`
- Delete `vite-env.d.ts`
- Delete `tsconfig.node.json`
- Delete `vite.config.ts`
- Uninstall Vite dependencies

## Next Steps

If everything went according to plan, you now have a functioning Next.js application running as a
single-page application. However, you aren't yet taking advantage of most of Next.js' benefits, but
you can now start making incremental changes to reap all the benefits. Here's what you might want to
do next:

- Migrate from React Router to the [Next.js App Router](https://nextjs.org/docs/app) to get:
  - Automatic code splitting
  - [Streaming Server-Rendering](https://nextjs.org/docs/app/api-reference/file-conventions/loading)
  - [React Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- [Optimize images with the<Image>component](https://nextjs.org/docs/app/api-reference/components/image)
- [Optimize fonts withnext/font](https://nextjs.org/docs/app/api-reference/components/font)
- [Optimize third-party scripts with the<Script>component](https://nextjs.org/docs/app/guides/scripts)
- [Update your ESLint configuration to support Next.js rules](https://nextjs.org/docs/app/api-reference/config/eslint)

Was this helpful?

supported.

---

# Migrating

> Learn how to migrate from popular frameworks to Next.js

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Migrating

# Migrating

Last updated  April 15, 2025[App RouterLearn how to upgrade your existing Next.js application from the Pages Router to the App Router.](https://nextjs.org/docs/app/guides/migrating/app-router-migration)[Create React AppLearn how to migrate your existing React application from Create React App to Next.js.](https://nextjs.org/docs/app/guides/migrating/from-create-react-app)[ViteLearn how to migrate your existing React application from Vite to Next.js.](https://nextjs.org/docs/app/guides/migrating/from-vite)

Was this helpful?

supported.

---

# How to build multi

> Learn how to build multi-tenant apps with the App Router.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Multi-tenant

# How to build multi-tenant apps in Next.js

Last updated  April 15, 2025

If you are looking to build a single Next.js application that serves multiple tenants, we have [built an example](https://vercel.com/templates/next.js/platforms-starter-kit) showing our recommended architecture.

Was this helpful?

supported.

---

# How to build micro

> Learn how to build micro-frontends using Next.js Multi-Zones to deploy multiple Next.js apps under a single domain.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Multi-zones

# How to build micro-frontends using multi-zones and Next.js

Last updated  October 17, 2025 Examples

- [With Zones](https://github.com/vercel/next.js/tree/canary/examples/with-zones)

Multi-Zones are an approach to micro-frontends that separate a large application on a domain into smaller Next.js applications that each serve a set of paths. This is useful when there are collections of pages unrelated to the other pages in the application. By moving those pages to a separate zone (i.e., a separate application), you can reduce the size of each application which improves build times and removes code that is only necessary for one of the zones. Since applications are decoupled, Multi-Zones also allows other applications on the domain to use their own choice of framework.

For example, let's say you have the following set of pages that you would like to split up:

- `/blog/*` for all blog posts
- `/dashboard/*` for all pages when the user is logged-in to the dashboard
- `/*` for the rest of your website not covered by other zones

With Multi-Zones support, you can create three applications that all are served on the same domain and look the same to the user, but you can develop and deploy each of the applications independently.

 ![Three zones: A, B, C. Showing a hard navigation between routes from different zones, and soft navigations between routes within the same zone.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fmulti-zones.png&w=3840&q=75)![Three zones: A, B, C. Showing a hard navigation between routes from different zones, and soft navigations between routes within the same zone.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fmulti-zones.png&w=3840&q=75)

Navigating between pages in the same zone will perform soft navigations, a navigation that does not require reloading the page. For example, in this diagram, navigating from `/` to `/products` will be a soft navigation.

Navigating from a page in one zone to a page in another zone, such as from `/` to `/dashboard`, will perform a hard navigation, unloading the resources of the current page and loading the resources of the new page. Pages that are frequently visited together should live in the same zone to avoid hard navigations.

## How to define a zone

A zone is a normal Next.js application where you also configure an [assetPrefix](https://nextjs.org/docs/app/api-reference/config/next-config-js/assetPrefix) to avoid conflicts with pages and static files in other zones.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  assetPrefix: '/blog-static',
}
```

Next.js assets, such as JavaScript and CSS, will be prefixed with `assetPrefix` to make sure that they don't conflict with assets from other zones. These assets will be served under `/assetPrefix/_next/...` for each of the zones.

The default application handling all paths not routed to another more specific zone does not need an `assetPrefix`.

In versions older than Next.js 15, you may also need an additional rewrite to handle the static assets. This is no longer necessary in Next.js 15.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  assetPrefix: '/blog-static',
  async rewrites() {
    return {
      beforeFiles: [
        {
          source: '/blog-static/_next/:path+',
          destination: '/_next/:path+',
        },
      ],
    }
  },
}
```

## How to route requests to the right zone

With the Multi Zones set-up, you need to route the paths to the correct zone since they are served by different applications. You can use any HTTP proxy to do this, but one of the Next.js applications can also be used to route requests for the entire domain.

To route to the correct zone using a Next.js application, you can use [rewrites](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites). For each path served by a different zone, you would add a rewrite rule to send that path to the domain of the other zone, and you also need to rewrite the requests for the static assets. For example:

 next.config.js

```
async rewrites() {
    return [
        {
            source: '/blog',
            destination: `${process.env.BLOG_DOMAIN}/blog`,
        },
        {
            source: '/blog/:path+',
            destination: `${process.env.BLOG_DOMAIN}/blog/:path+`,
        },
        {
            source: '/blog-static/:path+',
            destination: `${process.env.BLOG_DOMAIN}/blog-static/:path+`,
        }
    ];
}
```

`destination` should be a URL that is served by the zone, including scheme and domain. This should point to the zone's production domain, but it can also be used to route requests to `localhost` in local development.

> **Good to know**: URL paths should be unique to a zone. For example, two zones trying to serve `/blog` would create a routing conflict.

### Routing requests using proxy

Routing requests through [rewrites](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites) is recommended to minimize latency overhead for the requests, but proxy can also be used when there is a need for a dynamic decision when routing. For example, if you are using a feature flag to decide where a path should be routed such as during a migration, you can use proxy.

 proxy.js

```
export async function proxy(request) {
  const { pathname, search } = req.nextUrl;
  if (pathname === '/your-path' && myFeatureFlag.isEnabled()) {
    return NextResponse.rewrite(`${rewriteDomain}${pathname}${search});
  }
}
```

## Linking between zones

Links to paths in a different zone should use an `a` tag instead of the Next.js [<Link>](https://nextjs.org/docs/pages/api-reference/components/link) component. This is because Next.js will try to prefetch and soft navigate to any relative path in `<Link>` component, which will not work across zones.

## Sharing code

The Next.js applications that make up the different zones can live in any repository. However, it is often convenient to put these zones in a [monorepo](https://en.wikipedia.org/wiki/Monorepo) to more easily share code. For zones that live in different repositories, code can also be shared using public or private NPM packages.

Since the pages in different zones may be released at different times, feature flags can be useful for enabling or disabling features in unison across the different zones.

## Server Actions

When using [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data) with Multi-Zones, you must explicitly allow the user-facing origin since your user facing domain may serve multiple applications. In your `next.config.js` file, add the following lines:

next.config.js

```
const nextConfig = {
  experimental: {
    serverActions: {
      allowedOrigins: ['your-production-domain.com'],
    },
  },
}
```

See [serverActions.allowedOrigins](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverActions#allowedorigins) for more information.

Was this helpful?

supported.
