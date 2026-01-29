# How to upgrade to version 11 and more

# How to upgrade to version 11

> Upgrade your Next.js Application from Version 10 to Version 11.

[Guides](https://nextjs.org/docs/pages/guides)[Upgrading](https://nextjs.org/docs/pages/guides/upgrading)Version 11You are currently viewing the documentation for Pages Router.

# How to upgrade to version 11

Last updated  April 15, 2025

To upgrade to version 11, run the following command:

 Terminal

```
npm i next@11 react@17 react-dom@17
```

 Terminal

```
yarn add next@11 react@17 react-dom@17
```

 Terminal

```
pnpm up next@11 react@17 react-dom@17
```

 Terminal

```
bun add next@11 react@17 react-dom@17
```

> **Good to know:** If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their corresponding versions.

### Webpack 5

Webpack 5 is now the default for all Next.js applications. If you did not have a custom webpack configuration, your application is already using webpack 5. If you do have a custom webpack configuration, you can refer to the [Next.js webpack 5 documentation](https://nextjs.org/docs/messages/webpack5) for upgrade guidance.

### Cleaning thedistDiris now a default

The build output directory (defaults to `.next`) is now cleared by default except for the Next.js caches. You can refer to [the cleaningdistDirRFC](https://github.com/vercel/next.js/discussions/6009) for more information.

If your application was relying on this behavior previously you can disable the new default behavior by adding the `cleanDistDir: false` flag in `next.config.js`.

### PORTis now supported fornext devandnext start

Next.js 11 supports the `PORT` environment variable to set the port the application runs on. Using `-p`/`--port` is still recommended but if you were prohibited from using `-p` in any way you can now use `PORT` as an alternative:

Example:

```
PORT=4000 next start
```

### next.config.jscustomization to import images

Next.js 11 supports static image imports with `next/image`. This new feature relies on being able to process image imports. If you previously added the `next-images` or `next-optimized-images` packages you can either move to the new built-in support using `next/image` or disable the feature:

 next.config.js

```
module.exports = {
  images: {
    disableStaticImages: true,
  },
}
```

### Removesuper.componentDidCatch()frompages/_app.js

The `next/app` component's `componentDidCatch` was deprecated in Next.js 9 as it's no longer needed and has since been a no-op. In Next.js 11, it was removed.

If your `pages/_app.js` has a custom `componentDidCatch` method you can remove `super.componentDidCatch` as it is no longer needed.

### RemoveContainerfrompages/_app.js

This export was deprecated in Next.js 9 as it's no longer needed and has since been a no-op with a warning during development. In Next.js 11 it was removed.

If your `pages/_app.js` imports `Container` from `next/app` you can remove `Container` as it was removed. Learn more in [the documentation](https://nextjs.org/docs/messages/app-container-deprecated).

### Removeprops.urlusage from page components

This property was deprecated in Next.js 4 and has since shown a warning during development. With the introduction of `getStaticProps` / `getServerSideProps` these methods already disallowed the usage of `props.url`. In Next.js 11, it was removed completely.

You can learn more in [the documentation](https://nextjs.org/docs/messages/url-deprecated).

### Removeunsizedproperty onnext/image

The `unsized` property on `next/image` was deprecated in Next.js 10.0.1. You can use `layout="fill"` instead. In Next.js 11 `unsized` was removed.

### Removemodulesproperty onnext/dynamic

The `modules` and `render` option for `next/dynamic` were deprecated in Next.js 9.5. This was done in order to make the `next/dynamic` API closer to `React.lazy`. In Next.js 11, the `modules` and `render` options were removed.

This option hasn't been mentioned in the documentation since Next.js 8 so it's less likely that your application is using it.

If your application does use `modules` and `render` you can refer to [the documentation](https://nextjs.org/docs/messages/next-dynamic-modules).

### RemoveHead.rewind

`Head.rewind` has been a no-op since Next.js 9.5, in Next.js 11 it was removed. You can safely remove your usage of `Head.rewind`.

### Moment.js locales excluded by default

Moment.js includes translations for a lot of locales by default. Next.js now automatically excludes these locales by default to optimize bundle size for applications using Moment.js.

To load a specific locale use this snippet:

```
import moment from 'moment'
import 'moment/locale/ja'

moment.locale('ja')
```

You can opt-out of this new default by adding `excludeDefaultMomentLocales: false` to `next.config.js` if you do not want the new behavior, do note it's highly recommended to not disable this new optimization as it significantly reduces the size of Moment.js.

### Update usage ofrouter.events

In case you're accessing `router.events` during rendering, in Next.js 11 `router.events` is no longer provided during pre-rendering. Ensure you're accessing `router.events` in `useEffect`:

```
useEffect(() => {
  const handleRouteChange = (url, { shallow }) => {
    console.log(
      `App is changing to ${url} ${
        shallow ? 'with' : 'without'
      } shallow routing`
    )
  }

  router.events.on('routeChangeStart', handleRouteChange)

  // If the component is unmounted, unsubscribe
  // from the event with the `off` method:
  return () => {
    router.events.off('routeChangeStart', handleRouteChange)
  }
}, [router])
```

If your application uses `router.router.events` which was an internal property that was not public please make sure to use `router.events` as well.

## React 16 to 17

React 17 introduced a new [JSX Transform](https://reactjs.org/blog/2020/09/22/introducing-the-new-jsx-transform.html) that brings a long-time Next.js feature to the wider React ecosystem: Not having to `import React from 'react'` when using JSX. When using React 17 Next.js will automatically use the new transform. This transform does not make the `React` variable global, which was an unintended side-effect of the previous Next.js implementation. A [codemod is available](https://nextjs.org/docs/pages/guides/upgrading/codemods#add-missing-react-import) to automatically fix cases where you accidentally used `React` without importing it.

Most applications already use the latest version of React, with Next.js 11 the minimum React version has been updated to 17.0.2.

To upgrade you can run the following command:

```
npm install react@latest react-dom@latest
```

Or using `yarn`:

```
yarn add react@latest react-dom@latest
```

Was this helpful?

supported.

---

# How to upgrade to version 12

> Upgrade your Next.js Application from Version 11 to Version 12.

[Guides](https://nextjs.org/docs/pages/guides)[Upgrading](https://nextjs.org/docs/pages/guides/upgrading)Version 12You are currently viewing the documentation for Pages Router.

# How to upgrade to version 12

Last updated  May 8, 2025

To upgrade to version 12, run the following command:

 Terminal

```
npm i next@12 react@17 react-dom@17 eslint-config-next@12
```

 Terminal

```
yarn add next@12 react@17 react-dom@17 eslint-config-next@12
```

 Terminal

```
pnpm up next@12 react@17 react-dom@17 eslint-config-next@12
```

 Terminal

```
bun add next@12 react@17 react-dom@17 eslint-config-next@12
```

> **Good to know:** If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their corresponding versions.

### Upgrading to 12.2

[Middleware](https://nextjs.org/docs/messages/middleware-upgrade-guide) - If you were using Middleware prior to `12.2`, please see the [upgrade guide](https://nextjs.org/docs/messages/middleware-upgrade-guide) for more information.

### Upgrading to 12.0

[Minimum Node.js Version](https://nodejs.org/en/) - The minimum Node.js version has been bumped from `12.0.0` to `12.22.0` which is the first version of Node.js with native ES Modules support.

[Minimum React Version](https://react.dev/learn/add-react-to-an-existing-project) - The minimum required React version is `17.0.2`. To upgrade you can run the following command in the terminal:

 Terminal

```
npm install react@latest react-dom@latest

yarn add react@latest react-dom@latest

pnpm update react@latest react-dom@latest

bun add react@latest react-dom@latest
```

#### SWC replacing Babel

Next.js now uses the Rust-based compiler [SWC](https://swc.rs/) to compile JavaScript/TypeScript. This new compiler is up to 17x faster than Babel when compiling individual files and up to 5x faster Fast Refresh.

Next.js provides full backward compatibility with applications that have [custom Babel configuration](https://nextjs.org/docs/pages/guides/babel). All transformations that Next.js handles by default like styled-jsx and tree-shaking of `getStaticProps` / `getStaticPaths` / `getServerSideProps` have been ported to Rust.

When an application has a custom Babel configuration, Next.js will automatically opt-out of using SWC for compiling JavaScript/Typescript and will fall back to using Babel in the same way that it was used in Next.js 11.

Many of the integrations with external libraries that currently require custom Babel transformations will be ported to Rust-based SWC transforms in the near future. These include but are not limited to:

- Styled Components
- Emotion
- Relay

In order to prioritize transforms that will help you adopt SWC, please provide your `.babelrc` on [this feedback thread](https://github.com/vercel/next.js/discussions/30174).

#### SWC replacing Terser for minification

You can opt-in to replacing Terser with SWC for minifying JavaScript up to 7x faster using a flag in `next.config.js`:

 next.config.js

```
module.exports = {
  swcMinify: true,
}
```

Minification using SWC is an opt-in flag to ensure it can be tested against more real-world Next.js applications before it becomes the default in Next.js 12.1. If you have feedback about minification, please leave it on [this feedback thread](https://github.com/vercel/next.js/discussions/30237).

#### Improvements to styled-jsx CSS parsing

On top of the Rust-based compiler we've implemented a new CSS parser based on the one used for the styled-jsx Babel transform. This new parser has improved handling of CSS and now errors when invalid CSS is used that would previously slip through and cause unexpected behavior.

Because of this change invalid CSS will throw an error during development and `next build`. This change only affects styled-jsx usage.

#### next/imagechanged wrapping element

`next/image` now renders the `<img>` inside a `<span>` instead of `<div>`.

If your application has specific CSS targeting span such as `.container span`, upgrading to Next.js 12 might incorrectly match the wrapping element inside the `<Image>` component. You can avoid this by restricting the selector to a specific class such as `.container span.item` and updating the relevant component with that className, such as `<span className="item" />`.

If your application has specific CSS targeting the `next/image` `<div>` tag, for example `.container div`, it may not match anymore. You can update the selector `.container span`, or preferably, add a new `<div className="wrapper">` wrapping the `<Image>` component and target that instead such as `.container .wrapper`.

The `className` prop is unchanged and will still be passed to the underlying `<img>` element.

See the [documentation](https://nextjs.org/docs/pages/api-reference/components/image#styling-images) for more info.

#### HMR connection now uses a WebSocket

Previously, Next.js used a [server-sent events](https://developer.mozilla.org/docs/Web/API/Server-sent_events) connection to receive HMR events. Next.js 12 now uses a WebSocket connection.

In some cases when proxying requests to the Next.js dev server, you will need to ensure the upgrade request is handled correctly. For example, in `nginx` you would need to add the following configuration:

```
location /_next/webpack-hmr {
    proxy_pass http://localhost:3000/_next/webpack-hmr;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

If you are using Apache (2.x), you can add the following configuration to enable web sockets to the server. Review the port, host name and server names.

```
<VirtualHost *:443>
 # ServerName yourwebsite.local
 ServerName "${WEBSITE_SERVER_NAME}"
 ProxyPass / http://localhost:3000/
 ProxyPassReverse / http://localhost:3000/
 # Next.js 12 uses websocket
 <Location /_next/webpack-hmr>
    RewriteEngine On
    RewriteCond %{QUERY_STRING} transport=websocket [NC]
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule /(.*) ws://localhost:3000/_next/webpack-hmr/$1 [P,L]
    ProxyPass ws://localhost:3000/_next/webpack-hmr retry=0 timeout=30
    ProxyPassReverse ws://localhost:3000/_next/webpack-hmr
 </Location>
</VirtualHost>
```

For custom servers, such as `express`, you may need to use `app.all` to ensure the request is passed correctly, for example:

```
app.all('/_next/webpack-hmr', (req, res) => {
  nextjsRequestHandler(req, res)
})
```

#### Webpack 4 support has been removed

If you are already using webpack 5 you can skip this section.

Next.js has adopted webpack 5 as the default for compilation in Next.js 11. As communicated in the [webpack 5 upgrading documentation](https://nextjs.org/docs/messages/webpack5) Next.js 12 removes support for webpack 4.

If your application is still using webpack 4 using the opt-out flag, you will now see an error linking to the [webpack 5 upgrading documentation](https://nextjs.org/docs/messages/webpack5).

#### targetoption deprecated

If you do not have `target` in `next.config.js` you can skip this section.

The target option has been deprecated in favor of built-in support for tracing what dependencies are needed to run a page.

During `next build`, Next.js will automatically trace each page and its dependencies to determine all of the files that are needed for deploying a production version of your application.

If you are currently using the `target` option set to `serverless`, please read the [documentation on how to leverage the new output](https://nextjs.org/docs/pages/api-reference/config/next-config-js/output).

Was this helpful?

supported.

---

# How to upgrade to version 13

> Upgrade your Next.js Application from Version 12 to 13.

[Guides](https://nextjs.org/docs/pages/guides)[Upgrading](https://nextjs.org/docs/pages/guides/upgrading)Version 13You are currently viewing the documentation for Pages Router.

# How to upgrade to version 13

Last updated  June 16, 2025

## Upgrading from 12 to 13

To update to Next.js version 13, run the following command using your preferred package manager:

 Terminal

```
npm i next@13 react@latest react-dom@latest eslint-config-next@13
```

 Terminal

```
yarn add next@13 react@latest react-dom@latest eslint-config-next@13
```

 Terminal

```
pnpm i next@13 react@latest react-dom@latest eslint-config-next@13
```

 Terminal

```
bun add next@13 react@latest react-dom@latest eslint-config-next@13
```

> **Good to know:** If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their latest versions.

### v13 Summary

- The [Supported Browsers](https://nextjs.org/docs/architecture/supported-browsers) have been changed to drop Internet Explorer and target modern browsers.
- The minimum Node.js version has been bumped from 12.22.0 to 16.14.0, since 12.x and 14.x have reached end-of-life.
- The minimum React version has been bumped from 17.0.2 to 18.2.0.
- The `swcMinify` configuration property was changed from `false` to `true`. See [Next.js Compiler](https://nextjs.org/docs/architecture/nextjs-compiler) for more info.
- The `next/image` import was renamed to `next/legacy/image`. The `next/future/image` import was renamed to `next/image`. A [codemod is available](https://nextjs.org/docs/pages/guides/upgrading/codemods#next-image-to-legacy-image) to safely and automatically rename your imports.
- The `next/link` child can no longer be `<a>`. Add the `legacyBehavior` prop to use the legacy behavior or remove the `<a>` to upgrade. A [codemod is available](https://nextjs.org/docs/pages/guides/upgrading/codemods#new-link) to automatically upgrade your code.
- The `target` configuration property has been removed and superseded by [Output File Tracing](https://nextjs.org/docs/pages/api-reference/config/next-config-js/output).

## Migrating shared features

Next.js 13 introduces a new [appdirectory](https://nextjs.org/docs/app) with new features and conventions. However, upgrading to Next.js 13 does **not** require using the new `app` Router.

You can continue using `pages` with new features that work in both directories, such as the updated [Image component](#image-component), [Link component](#link-component), [Script component](#script-component), and [Font optimization](#font-optimization).

### <Image/>Component

Next.js 12 introduced many improvements to the Image Component with a temporary import: `next/future/image`. These improvements included less client-side JavaScript, easier ways to extend and style images, better accessibility, and native browser lazy loading.

Starting in Next.js 13, this new behavior is now the default for `next/image`.

There are two codemods to help you migrate to the new Image Component:

- [next-image-to-legacy-image](https://nextjs.org/docs/pages/guides/upgrading/codemods#next-image-to-legacy-image): This codemod will safely and automatically rename `next/image` imports to `next/legacy/image` to maintain the same behavior as Next.js 12. We recommend running this codemod to quickly update to Next.js 13 automatically.
- [next-image-experimental](https://nextjs.org/docs/pages/guides/upgrading/codemods#next-image-experimental): After running the previous codemod, you can optionally run this experimental codemod to upgrade `next/legacy/image` to the new `next/image`, which will remove unused props and add inline styles. Please note this codemod is experimental and only covers static usage (such as `<Image src={img} layout="responsive" />`) but not dynamic usage (such as `<Image {...props} />`).

Alternatively, you can manually update by following the [migration guide](https://nextjs.org/docs/pages/guides/upgrading/codemods#next-image-experimental) and also see the [legacy comparison](https://nextjs.org/docs/pages/api-reference/components/image-legacy#comparison).

### <Link>Component

The [<Link>Component](https://nextjs.org/docs/pages/api-reference/components/link) no longer requires manually adding an `<a>` tag as a child. This behavior was added as an experimental option in [version 12.2](https://nextjs.org/blog/next-12-2) and is now the default. In Next.js 13, `<Link>` always renders `<a>` and allows you to forward props to the underlying tag.

For example:

```
import Link from 'next/link'

// Next.js 12: `<a>` has to be nested otherwise it's excluded
<Link href="/about">
  <a>About</a>
</Link>

// Next.js 13: `<Link>` always renders `<a>` under the hood
<Link href="/about">
  About
</Link>
```

To upgrade your links to Next.js 13, you can use the [new-linkcodemod](https://nextjs.org/docs/pages/guides/upgrading/codemods#new-link).

### <Script>Component

The behavior of [next/script](https://nextjs.org/docs/pages/api-reference/components/script) has been updated to support both `pages` and `app`. If incrementally adopting `app`, read the [upgrade guide](https://nextjs.org/docs/pages/guides/upgrading).

### Font Optimization

Previously, Next.js helped you optimize fonts by inlining font CSS. Version 13 introduces the new [next/font](https://nextjs.org/docs/pages/api-reference/components/font) module which gives you the ability to customize your font loading experience while still ensuring great performance and privacy.

See [Optimizing Fonts](https://nextjs.org/docs/pages/api-reference/components/font) to learn how to use `next/font`.

Was this helpful?

supported.

---

# How to upgrade to version 14

> Upgrade your Next.js Application from Version 13 to 14.

[Guides](https://nextjs.org/docs/pages/guides)[Upgrading](https://nextjs.org/docs/pages/guides/upgrading)Version 14You are currently viewing the documentation for Pages Router.

# How to upgrade to version 14

Last updated  April 15, 2025

## Upgrading from 13 to 14

To update to Next.js version 14, run the following command using your preferred package manager:

 Terminal

```
npm i next@next-14 react@18 react-dom@18 && npm i eslint-config-next@next-14 -D
```

 Terminal

```
yarn add next@next-14 react@18 react-dom@18 && yarn add eslint-config-next@next-14 -D
```

 Terminal

```
pnpm i next@next-14 react@18 react-dom@18 && pnpm i eslint-config-next@next-14 -D
```

 Terminal

```
bun add next@next-14 react@18 react-dom@18 && bun add eslint-config-next@next-14 -D
```

> **Good to know:** If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their latest versions.

### v14 Summary

- The minimum Node.js version has been bumped from 16.14 to 18.17, since 16.x has reached end-of-life.
- The `next export` command has been removed in favor of `output: 'export'` config. Please see the [docs](https://nextjs.org/docs/app/guides/static-exports) for more information.
- The `next/server` import for `ImageResponse` was renamed to `next/og`. A [codemod is available](https://nextjs.org/docs/app/guides/upgrading/codemods#next-og-import) to safely and automatically rename your imports.
- The `@next/font` package has been fully removed in favor of the built-in `next/font`. A [codemod is available](https://nextjs.org/docs/app/guides/upgrading/codemods#built-in-next-font) to safely and automatically rename your imports.
- The WASM target for `next-swc` has been removed.

Was this helpful?

supported.

---

# How to upgrade to version 9

> Upgrade your Next.js Application from Version 8 to Version 9.

[Guides](https://nextjs.org/docs/pages/guides)[Upgrading](https://nextjs.org/docs/pages/guides/upgrading)Version 9You are currently viewing the documentation for Pages Router.

# How to upgrade to version 9

Last updated  April 25, 2025

To upgrade to version 9, run the following command:

 Terminal

```
npm i next@9
```

 Terminal

```
yarn add next@9
```

 Terminal

```
pnpm up next@9
```

 Terminal

```
bun add next@9
```

> **Good to know:** If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their corresponding versions.

## Check your Custom App File (pages/_app.js)

If you previously copied the [Custom<App>](https://nextjs.org/docs/pages/building-your-application/routing/custom-app) example, you may be able to remove your `getInitialProps`.

Removing `getInitialProps` from `pages/_app.js` (when possible) is important to leverage new Next.js features!

The following `getInitialProps` does nothing and may be removed:

```
class MyApp extends App {
  // Remove me, I do nothing!
  static async getInitialProps({ Component, ctx }) {
    let pageProps = {}

    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx)
    }

    return { pageProps }
  }

  render() {
    // ... etc
  }
}
```

## Breaking Changes

### @zeit/next-typescriptis no longer necessary

Next.js will now ignore usage `@zeit/next-typescript` and warn you to remove it. Please remove this plugin from your `next.config.js`.

Remove references to `@zeit/next-typescript/babel` from your custom `.babelrc` (if present).

The usage of [fork-ts-checker-webpack-plugin](https://github.com/Realytics/fork-ts-checker-webpack-plugin/issues) should also be removed from your `next.config.js`.

TypeScript Definitions are published with the `next` package, so you need to uninstall `@types/next` as they would conflict.

The following types are different:

> This list was created by the community to help you upgrade, if you find other differences please send a pull-request to this list to help other users.

From:

```
import { NextContext } from 'next'
import { NextAppContext, DefaultAppIProps } from 'next/app'
import { NextDocumentContext, DefaultDocumentIProps } from 'next/document'
```

to

```
import { NextPageContext } from 'next'
import { AppContext, AppInitialProps } from 'next/app'
import { DocumentContext, DocumentInitialProps } from 'next/document'
```

### Theconfigkey is now an export on a page

You may no longer export a custom variable named `config` from a page (i.e. `export { config }` / `export const config ...`).
This exported variable is now used to specify page-level Next.js configuration like Opt-in AMP and API Route features.

You must rename a non-Next.js-purposed `config` export to something different.

### next/dynamicno longer renders "loading..." by default while loading

Dynamic components will not render anything by default while loading. You can still customize this behavior by setting the `loading` property:

```
import dynamic from 'next/dynamic'

const DynamicComponentWithCustomLoading = dynamic(
  () => import('../components/hello2'),
  {
    loading: () => <p>Loading</p>,
  }
)
```

### withAmphas been removed in favor of an exported configuration object

Next.js now has the concept of page-level configuration, so the `withAmp` higher-order component has been removed for consistency.

This change can be **automatically migrated by running the following commands in the root of your Next.js project:**

 Terminal

```
curl -L https://github.com/vercel/next-codemod/archive/master.tar.gz | tar -xz --strip=2 next-codemod-master/transforms/withamp-to-config.js npx jscodeshift -t ./withamp-to-config.js pages/**/*.js
```

To perform this migration by hand, or view what the codemod will produce, see below:

**Before**

```
import { withAmp } from 'next/amp'

function Home() {
  return <h1>My AMP Page</h1>
}

export default withAmp(Home)
// or
export default withAmp(Home, { hybrid: true })
```

**After**

```
export default function Home() {
  return <h1>My AMP Page</h1>
}

export const config = {
  amp: true,
  // or
  amp: 'hybrid',
}
```

### next exportno longer exports pages asindex.html

Previously, exporting `pages/about.js` would result in `out/about/index.html`. This behavior has been changed to result in `out/about.html`.

You can revert to the previous behavior by creating a `next.config.js` with the following content:

 next.config.js

```
module.exports = {
  trailingSlash: true,
}
```

### pages/api/is treated differently

Pages in `pages/api/` are now considered [API Routes](https://nextjs.org/blog/next-9#api-routes).
Pages in this directory will no longer contain a client-side bundle.

## Deprecated Features

### next/dynamichas deprecated loading multiple modules at once

The ability to load multiple modules at once has been deprecated in `next/dynamic` to be closer to React's implementation (`React.lazy` and `Suspense`).

Updating code that relies on this behavior is relatively straightforward! We've provided an example of a before/after to help you migrate your application:

**Before**

```
import dynamic from 'next/dynamic'

const HelloBundle = dynamic({
  modules: () => {
    const components = {
      Hello1: () => import('../components/hello1').then((m) => m.default),
      Hello2: () => import('../components/hello2').then((m) => m.default),
    }

    return components
  },
  render: (props, { Hello1, Hello2 }) => (
    <div>
      <h1>{props.title}</h1>
      <Hello1 />
      <Hello2 />
    </div>
  ),
})

function DynamicBundle() {
  return <HelloBundle title="Dynamic Bundle" />
}

export default DynamicBundle
```

**After**

```
import dynamic from 'next/dynamic'

const Hello1 = dynamic(() => import('../components/hello1'))
const Hello2 = dynamic(() => import('../components/hello2'))

function HelloBundle({ title }) {
  return (
    <div>
      <h1>{title}</h1>
      <Hello1 />
      <Hello2 />
    </div>
  )
}

function DynamicBundle() {
  return <HelloBundle title="Dynamic Bundle" />
}

export default DynamicBundle
```

Was this helpful?

supported.

---

# Upgrading

> Learn how to upgrade to the latest versions of Next.js.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)UpgradingYou are currently viewing the documentation for Pages Router.

# Upgrading

Last updated  April 15, 2025

Learn how to upgrade to the latest versions of Next.js following the versions-specific guides:

[CodemodsUse codemods to upgrade your Next.js codebase when new features are released.](https://nextjs.org/docs/pages/guides/upgrading/codemods)[Version 10Upgrade your Next.js Application from Version 9 to Version 10.](https://nextjs.org/docs/pages/guides/upgrading/version-10)[Version 11Upgrade your Next.js Application from Version 10 to Version 11.](https://nextjs.org/docs/pages/guides/upgrading/version-11)[Version 12Upgrade your Next.js Application from Version 11 to Version 12.](https://nextjs.org/docs/pages/guides/upgrading/version-12)[Version 13Upgrade your Next.js Application from Version 12 to 13.](https://nextjs.org/docs/pages/guides/upgrading/version-13)[Version 14Upgrade your Next.js Application from Version 13 to 14.](https://nextjs.org/docs/pages/guides/upgrading/version-14)[Version 9Upgrade your Next.js Application from Version 8 to Version 9.](https://nextjs.org/docs/pages/guides/upgrading/version-9)

Was this helpful?

supported.

---

# Guides

> Learn how to implement common UI patterns and use cases using Next.js

[Next.js Docs](https://nextjs.org/docs)[Pages Router](https://nextjs.org/docs/pages)GuidesYou are currently viewing the documentation for Pages Router.

# Guides

Last updated  April 15, 2025[AnalyticsMeasure and track page performance using Next.js](https://nextjs.org/docs/pages/guides/analytics)[AuthenticationLearn how to implement authentication in Next.js, covering best practices, securing routes, authorization techniques, and session management.](https://nextjs.org/docs/pages/guides/authentication)[BabelExtend the babel preset added by Next.js with your own configs.](https://nextjs.org/docs/pages/guides/babel)[CI Build CachingLearn how to configure CI to cache Next.js builds](https://nextjs.org/docs/pages/guides/ci-build-caching)[Content Security PolicyLearn how to set a Content Security Policy (CSP) for your Next.js application.](https://nextjs.org/docs/pages/guides/content-security-policy)[CSS-in-JSUse CSS-in-JS libraries with Next.js](https://nextjs.org/docs/pages/guides/css-in-js)[Custom ServerStart a Next.js app programmatically using a custom server.](https://nextjs.org/docs/pages/guides/custom-server)[DebuggingLearn how to debug your Next.js application with VS Code or Chrome DevTools.](https://nextjs.org/docs/pages/guides/debugging)[Draft ModeNext.js has draft mode to toggle between static and dynamic pages. You can learn how it works with Pages Router.](https://nextjs.org/docs/pages/guides/draft-mode)[Environment VariablesLearn to add and access environment variables in your Next.js application.](https://nextjs.org/docs/pages/guides/environment-variables)[FormsLearn how to handle form submissions and data mutations with Next.js.](https://nextjs.org/docs/pages/guides/forms)[ISRLearn how to create or update static pages at runtime with Incremental Static Regeneration.](https://nextjs.org/docs/pages/guides/incremental-static-regeneration)[InstrumentationLearn how to use instrumentation to run code at server startup in your Next.js app](https://nextjs.org/docs/pages/guides/instrumentation)[InternationalizationNext.js has built-in support for internationalized routing and language detection. Learn more here.](https://nextjs.org/docs/pages/guides/internationalization)[Lazy LoadingLazy load imported libraries and React Components to improve your application's overall loading performance.](https://nextjs.org/docs/pages/guides/lazy-loading)[MDXLearn how to configure MDX to write JSX in your markdown files.](https://nextjs.org/docs/pages/guides/mdx)[MigratingLearn how to migrate from popular frameworks to Next.js](https://nextjs.org/docs/pages/guides/migrating)[Multi-ZonesLearn how to build micro-frontends using Next.js Multi-Zones to deploy multiple Next.js apps under a single domain.](https://nextjs.org/docs/pages/guides/multi-zones)[OpenTelemetryLearn how to instrument your Next.js app with OpenTelemetry.](https://nextjs.org/docs/pages/guides/open-telemetry)[Package BundlingLearn how to optimize your application's server and client bundles.](https://nextjs.org/docs/pages/guides/package-bundling)[PostCSSExtend the PostCSS config and plugins added by Next.js with your own.](https://nextjs.org/docs/pages/guides/post-css)[Preview ModeNext.js has the preview mode for statically generated pages. You can learn how it works here.](https://nextjs.org/docs/pages/guides/preview-mode)[ProductionRecommendations to ensure the best performance and user experience before taking your Next.js application to production.](https://nextjs.org/docs/pages/guides/production-checklist)[RedirectingLearn the different ways to handle redirects in Next.js.](https://nextjs.org/docs/pages/guides/redirecting)[SassLearn how to use Sass in your Next.js application.](https://nextjs.org/docs/pages/guides/sass)[ScriptsOptimize 3rd party scripts with the built-in Script component.](https://nextjs.org/docs/pages/guides/scripts)[Self-HostingLearn how to self-host your Next.js application on a Node.js server, Docker image, or static HTML files (static exports).](https://nextjs.org/docs/pages/guides/self-hosting)[Static ExportsNext.js enables starting as a static site or Single-Page Application (SPA), then later optionally upgrading to use features that require a server.](https://nextjs.org/docs/pages/guides/static-exports)[Tailwind CSSStyle your Next.js Application using Tailwind CSS.](https://nextjs.org/docs/pages/guides/tailwind-v3-css)[TestingLearn how to set up Next.js with three commonly used testing tools — Cypress, Playwright, Vitest, and Jest.](https://nextjs.org/docs/pages/guides/testing)[Third Party LibrariesOptimize the performance of third-party libraries in your application with the `@next/third-parties` package.](https://nextjs.org/docs/pages/guides/third-party-libraries)[UpgradingLearn how to upgrade to the latest versions of Next.js.](https://nextjs.org/docs/pages/guides/upgrading)

Was this helpful?

supported.
