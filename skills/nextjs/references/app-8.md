# turbopack and more

# turbopack

> Configure Next.js with Turbopack-specific options

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)turbopack

# turbopack

Last updated  January 22, 2026

The `turbopack` option lets you customize [Turbopack](https://nextjs.org/docs/app/api-reference/turbopack) to transform different files and change how modules are resolved.

> **Good to know**: The `turbopack` option was previously named `experimental.turbo` in Next.js versions 13.0.0 to 15.2.x. The `experimental.turbo` option will be removed in Next.js 16.
>
>
>
> If you are using an older version of Next.js, run `npx @next/codemod@latest next-experimental-turbo-to-turbopack .` to automatically migrate your configuration.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  turbopack: {
    // ...
  },
}

export default nextConfig
```

> **Good to know**:
>
>
>
> - Turbopack for Next.js does not require loaders or loader configuration for built-in functionality. Turbopack has built-in support for CSS and compiling modern JavaScript, so there's no need for `css-loader`, `postcss-loader`, or `babel-loader` if you're using `@babel/preset-env`.

## Reference

### Options

The following options are available for the `turbopack` configuration:

| Option | Description |
| --- | --- |
| root | Sets the application root directory. Should be an absolute path. |
| rules | List of supported webpack loaders to apply when running with Turbopack. |
| resolveAlias | Map aliased imports to modules to load in their place. |
| resolveExtensions | List of extensions to resolve when importing files. |
| debugIds | Enable generation ofdebug IDsin JavaScript bundles and source maps. |

### Supported loaders

The following loaders have been tested to work with Turbopack's webpack loader implementation, but many other webpack loaders should work as well even if not listed here:

- [babel-loader](https://www.npmjs.com/package/babel-loader) [(Configured automatically if a Babel configuration file is found)](https://nextjs.org/docs/app/api-reference/turbopack#language-features)
- [@svgr/webpack](https://www.npmjs.com/package/@svgr/webpack)
- [svg-inline-loader](https://www.npmjs.com/package/svg-inline-loader)
- [yaml-loader](https://www.npmjs.com/package/yaml-loader)
- [string-replace-loader](https://www.npmjs.com/package/string-replace-loader)
- [raw-loader](https://www.npmjs.com/package/raw-loader)
- [sass-loader](https://www.npmjs.com/package/sass-loader) [(Configured automatically)](https://nextjs.org/docs/app/api-reference/turbopack#css-and-styling)
- [graphql-tag/loader](https://www.npmjs.com/package/graphql-tag)

#### Missing Webpack loader features

Turbopack uses the [loader-runner](https://github.com/webpack/loader-runner) library to execute webpack loaders, which provides most of the standard loader API. However, some features are not supported:

**Module loading:**

- [importModule](https://webpack.js.org/api/loaders/#thisimportmodule) - No support
- [loadModule](https://webpack.js.org/api/loaders/#thisloadmodule) - No support

**File system and output:**

- [fs](https://webpack.js.org/api/loaders/#thisfs) - Partial support: only `fs.readFile` is currently implemented.
- [emitFile](https://webpack.js.org/api/loaders/#thisemitfile) - No support

**Context properties:**

- [version](https://webpack.js.org/api/loaders/#thisversion) - No support
- [mode](https://webpack.js.org/api/loaders/#thismode) - No support
- [target](https://webpack.js.org/api/loaders/#thistarget) - No support

**Utilities:**

- [utils](https://webpack.js.org/api/loaders/#thisutils) - No support
- [resolve](https://webpack.js.org/api/loaders/#thisresolve) - No support (use [getResolve](https://webpack.js.org/api/loaders/#thisgetresolve) instead)

If you have a loader that is critically dependent upon one of these features please file an issue.

## Examples

### Root directory

Turbopack uses the root directory to resolve modules. Files outside of the project root are not resolved.

The reason files are not resolved outside of the project root is to improve cache validation, reduce filesystem watching overhead, and reduce the number of resolving steps needed.

Next.js automatically detects the root directory of your project. It does so by looking for one of these files:

- `pnpm-lock.yaml`
- `package-lock.json`
- `yarn.lock`
- `bun.lock`
- `bun.lockb`

If you have a different project structure, for example if you don't use workspaces, you can manually set the `root` option:

 next.config.js

```
const path = require('path')
module.exports = {
  turbopack: {
    root: path.join(__dirname, '..'),
  },
}
```

To resolve files from linked dependencies outside the project root (via `npm link`, `yarn link`, `pnpm link`, etc.), you must configure the `turbopack.root` to the parent directory of both the project and the linked dependencies.

While this expands the scope of filesystem watching, it's typically only necessary during development when actively working on linked packages.

### Configuring webpack loaders

If you need loader support beyond what's built in, many webpack loaders already work with Turbopack. There are currently some limitations:

- Only a core subset of the webpack loader API is implemented. Currently, there is enough coverage for some popular loaders, and we'll expand our API support in the future.
- Only loaders that return JavaScript code are supported. Loaders that transform files like stylesheets or images are not currently supported.
- Options passed to webpack loaders must be plain JavaScript primitives, objects, and arrays. For example, it's not possible to pass `require()` plugin modules as option values.

To configure loaders, add the names of the loaders you've installed and any options in `next.config.js`, mapping file extensions to a list of loaders. Rules are evaluated in order.

Here is an example below using the [@svgr/webpack](https://www.npmjs.com/package/@svgr/webpack) loader, which enables importing `.svg` files and rendering them as React components.

 next.config.js

```
module.exports = {
  turbopack: {
    rules: {
      '*.svg': {
        loaders: ['@svgr/webpack'],
        as: '*.js',
      },
    },
  },
}
```

> **Good to know**: Globs used in the `rules` object match based on file name, unless the glob contains a `/` character, which will cause it to match based on the full project-relative file path. Windows file paths are normalized to use unix-style `/` path separators.
>
>
>
> Turbopack uses a modified version of the [Rustglobsetlibrary](https://docs.rs/globset/latest/globset/).

For loaders that require configuration options, you can use an object format instead of a string:

 next.config.js

```
module.exports = {
  turbopack: {
    rules: {
      '*.svg': {
        loaders: [
          {
            loader: '@svgr/webpack',
            options: {
              icon: true,
            },
          },
        ],
        as: '*.js',
      },
    },
  },
}
```

> **Good to know**: Prior to Next.js version 13.4.4, `turbopack.rules` was named `turbo.loaders` and only accepted file extensions like `.mdx` instead of `*.mdx`.

### Advanced webpack loader conditions

You can further restrict where a loader runs using the advanced `condition` syntax:

 next.config.js

```
module.exports = {
  turbopack: {
    rules: {
      // '*' will match all file paths, but we restrict where our
      // rule runs with a condition.
      '*': {
        condition: {
          all: [
            // 'foreign' is a built-in condition.
            { not: 'foreign' },
            // 'path' can be a RegExp or a glob string. A RegExp matches
            // anywhere in the full project-relative file path.
            { path: /^img\/[0-9]{3}\// },
            {
              any: [
                { path: '*.svg' },
                // 'content' is always a RegExp, and can match
                // anywhere in the file.
                { content: /\<svg\W/ },
              ],
            },
          ],
        },
        loaders: ['@svgr/webpack'],
        as: '*.js',
      },
    },
  },
}
```

- Supported boolean operators are `{all: [...]}`, `{any: [...]}` and `{not: ...}`.
- Supported customizable operators are `{path: string | RegExp}` and `{content: RegExp}`. If `path` and `content` are specified in the same object, it acts as an implicit `and`.

In addition, a number of built-in conditions are supported:

- `browser`: Matches code that will execute on the client. Server code can be matched using `{not: 'browser'}`.
- `foreign`: Matches code in `node_modules`, as well as some Next.js internals. Usually you'll want to restrict loaders to `{not: 'foreign'}`. This can improve performance by reducing the number of files the loader is invoked on.
- `development`: Matches when using `next dev`.
- `production`: Matches when using `next build`.
- `node`: Matches code that will run on the default Node.js runtime.
- `edge-light`: Matches code that will run on the [Edge runtime](https://nextjs.org/docs/app/api-reference/edge).

Rules can be an object or an array of objects. An array is often useful for modeling disjoint conditions:

 next.config.js

```
module.exports = {
  turbopack: {
    rules: {
      '*.svg': [
        {
          condition: 'browser',
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
        {
          condition: { not: 'browser' },
          loaders: [require.resolve('./custom-svg-loader.js')],
          as: '*.js',
        },
      ],
    },
  },
}
```

> **Good to know**: All matching rules are executed in order.

### Resolving aliases

Turbopack can be configured to modify module resolution through aliases, similar to webpack's [resolve.alias](https://webpack.js.org/configuration/resolve/#resolvealias) configuration.

To configure resolve aliases, map imported patterns to their new destination in `next.config.js`:

 next.config.js

```
module.exports = {
  turbopack: {
    resolveAlias: {
      underscore: 'lodash',
      mocha: { browser: 'mocha/browser-entry.js' },
    },
  },
}
```

This aliases imports of the `underscore` package to the `lodash` package. In other words, `import underscore from 'underscore'` will load the `lodash` module instead of `underscore`.

Turbopack also supports conditional aliasing through this field, similar to Node.js' [conditional exports](https://nodejs.org/docs/latest-v18.x/api/packages.html#conditional-exports). At the moment only the `browser` condition is supported. In the case above, imports of the `mocha` module will be aliased to `mocha/browser-entry.js` when Turbopack targets browser environments.

### Resolving custom extensions

Turbopack can be configured to resolve modules with custom extensions, similar to webpack's [resolve.extensions](https://webpack.js.org/configuration/resolve/#resolveextensions) configuration.

To configure resolve extensions, use the `resolveExtensions` field in `next.config.js`:

 next.config.js

```
module.exports = {
  turbopack: {
    resolveExtensions: ['.mdx', '.tsx', '.ts', '.jsx', '.js', '.mjs', '.json'],
  },
}
```

This overwrites the original resolve extensions with the provided list. Make sure to include the default extensions.

For more information and guidance for how to migrate your app to Turbopack from webpack, see [Turbopack's documentation on webpack compatibility](https://turbo.build/pack/docs/migrating-from-webpack).

### Debug IDs

Turbopack can be configured to generate [debug IDs](https://github.com/tc39/ecma426/blob/main/proposals/debug-id.md) in JavaScript bundles and source maps.

To configure debug IDs, use the `debugIds` field in `next.config.js`:

 next.config.js

```
module.exports = {
  turbopack: {
    debugIds: true,
  },
}
```

The option automatically adds a polyfill for debug IDs to the JavaScript bundle to ensure compatibility. The debug IDs are available in the `globalThis._debugIds` global variable.

## Version History

| Version | Changes |
| --- | --- |
| 16.0.0 | turbopack.debugIdswas added. |
| 16.0.0 | turbopack.rules.*.conditionwas added. |
| 15.3.0 | experimental.turbois changed toturbopack. |
| 13.0.0 | experimental.turbointroduced. |

Was this helpful?

supported.

---

# Turbopack FileSystem Caching

> Learn how to enable FileSystem Caching for Turbopack builds

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)turbopackFileSystemCache

# Turbopack FileSystem Caching

Last updated  December 1, 2025

## Usage

Turbopack FileSystem Cache enables Turbopack to reduce work across `next dev` or `next build` commands. When enabled, Turbopack will save and restore data to the `.next` folder between builds, which can greatly speed up subsequent builds and dev sessions.

> **Good to know:** The FileSystem Cache feature is considered stable for development and experimental for production builds

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    // Enable filesystem caching for `next dev`
    turbopackFileSystemCacheForDev: true,
    // Enable filesystem caching for `next build`
    turbopackFileSystemCacheForBuild: true,
  },
}

export default nextConfig
```

## Version Changes

| Version | Changes |
| --- | --- |
| v16.1.0 | FileSystem caching is enabled by default for development |
| v16.0.0 | Beta release with separate flags for build and dev |
| v15.5.0 | Persistent caching released as experimental on canary releases |

Was this helpful?

supported.

---

# typedRoutes

> Enable support for statically typed links.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)typedRoutes

# typedRoutes

Last updated  August 19, 2025

> **Note**: This option has been marked as stable, so you should use `typedRoutes` instead of `experimental.typedRoutes`.

Support for [statically typed links](https://nextjs.org/docs/app/api-reference/config/typescript#statically-typed-links). This feature requires using TypeScript in your project.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  typedRoutes: true,
}

module.exports = nextConfig
```

Was this helpful?

supported.

---

# typescript

> Configure how Next.js handles TypeScript errors during production builds and specify a custom tsconfig file.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)typescript

# typescript

Last updated  December 9, 2025

Configure TypeScript behavior with the `typescript` option in `next.config.js`:

 next.config.js

```
module.exports = {
  typescript: {
    ignoreBuildErrors: false,
    tsconfigPath: 'tsconfig.json',
  },
}
```

## Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| ignoreBuildErrors | boolean | false | Allow production builds to complete even with TypeScript errors. |
| tsconfigPath | string | 'tsconfig.json' | Path to a customtsconfig.jsonfile. |

## ignoreBuildErrors

Next.js fails your **production build** (`next build`) when TypeScript errors are present in your project.

If you'd like Next.js to dangerously produce production code even when your application has errors, you can disable the built-in type checking step.

If disabled, be sure you are running type checks as part of your build or deploy process, otherwise this can be very dangerous.

 next.config.js

```
module.exports = {
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: true,
  },
}
```

## tsconfigPath

Use a different TypeScript configuration file for builds or tooling:

 next.config.js

```
module.exports = {
  typescript: {
    tsconfigPath: 'tsconfig.build.json',
  },
}
```

See the [TypeScript configuration](https://nextjs.org/docs/app/api-reference/config/typescript#custom-tsconfig-path) page for more details.

Was this helpful?

supported.

---

# urlImports

> Configure Next.js to allow importing modules from external URLs.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)urlImports

# urlImports

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

URL imports are an experimental feature that allows you to import modules directly from external servers (instead of from the local disk).

> **Warning**: Only use domains that you trust to download and execute on your machine. Please exercise discretion, and caution until the feature is flagged as stable.

To opt-in, add the allowed URL prefixes inside `next.config.js`:

 next.config.js

```
module.exports = {
  experimental: {
    urlImports: ['https://example.com/assets/', 'https://cdn.skypack.dev'],
  },
}
```

Then, you can import modules directly from URLs:

```
import { a, b, c } from 'https://example.com/assets/some/module.js'
```

URL Imports can be used everywhere normal package imports can be used.

## Security Model

This feature is being designed with **security as the top priority**. To start, we added an experimental flag forcing you to explicitly allow the domains you accept URL imports from. We're working to take this further by limiting URL imports to execute in the browser sandbox using the [Edge Runtime](https://nextjs.org/docs/app/api-reference/edge).

## Lockfile

When using URL imports, Next.js will create a `next.lock` directory containing a lockfile and fetched assets.
This directory **must be committed to Git**, not ignored by `.gitignore`.

- When running `next dev`, Next.js will download and add all newly discovered URL Imports to your lockfile.
- When running `next build`, Next.js will use only the lockfile to build the application for production.

Typically, no network requests are needed and any outdated lockfile will cause the build to fail.
One exception is resources that respond with `Cache-Control: no-cache`.
These resources will have a `no-cache` entry in the lockfile and will always be fetched from the network on each build.

## Examples

### Skypack

```
import confetti from 'https://cdn.skypack.dev/canvas-confetti'
import { useEffect } from 'react'

export default () => {
  useEffect(() => {
    confetti()
  })
  return <p>Hello</p>
}
```

### Static Image Imports

```
import Image from 'next/image'
import logo from 'https://example.com/assets/logo.png'

export default () => (
  <div>
    <Image src={logo} placeholder="blur" />
  </div>
)
```

### URLs in CSS

```
.className {
  background: url('https://example.com/assets/hero.jpg');
}
```

### Asset Imports

```
const logo = new URL('https://example.com/assets/file.txt', import.meta.url)

console.log(logo.pathname)

// prints "/_next/static/media/file.a9727b5d.txt"
```

Was this helpful?

supported.

---

# useLightningcss

> Enable experimental support for Lightning CSS.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)useLightningcss

# useLightningcss

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  October 9, 2025

Experimental support for using [Lightning CSS](https://lightningcss.dev) with webpack. Lightning CSS is a fast CSS transformer and minifier, written in Rust.

If this option is not set, Next.js on webpack uses [PostCSS](https://postcss.org/) with [postcss-preset-env](https://www.npmjs.com/package/postcss-preset-env) by default.

Turbopack uses Lightning CSS by default since Next 14.2. This configuration option has no effect on Turbopack. Turbopack always uses Lightning CSS.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    useLightningcss: false, // default, ignored on Turbopack
  },
}

export default nextConfig
```

## Version History

| Version | Changes |
| --- | --- |
| 15.1.0 | Support foruseSwcCsswas removed from Turbopack. |
| 14.2.0 | Turbopack's default CSS processor was changed from@swc/cssto Lightning CSS.useLightningcssbecame ignored on Turbopack, and a legacyexperimental.turbo.useSwcCssoption was added. |

Was this helpful?

supported.

---

# viewTransition

> Enable ViewTransition API from React in App Router

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)viewTransition

# viewTransition

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  October 7, 2025

`viewTransition` is an experimental flag that enables the new [View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) in React. This API allows you to leverage the native View Transitions browser API to create seamless transitions between UI states.

To enable this feature, you need to set the `viewTransition` property to `true` in your `next.config.js` file.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    viewTransition: true,
  },
}

module.exports = nextConfig
```

> Important Notice: The `<ViewTransition>` Component is already available in React's Canary release channel.
> `experimental.viewTransition` is only required to enable deeper integration with Next.js features e.g. automatically
> [adding Transition types](https://react.dev/reference/react/addTransitionType) for navigations. Next.js specific transition types are not implemented yet.

## Usage

You can import the [<ViewTransition>Component](https://react.dev/reference/react/ViewTransition) from React in your application:

```
import { ViewTransition } from 'react'
```

### Live Demo

Check out our [Next.js View Transition Demo](https://view-transition-example.vercel.app) to see this feature in action.

As this API evolves, we will update our documentation and share more examples. However, for now, we strongly advise against using this feature in production.

Was this helpful?

supported.

---

# Custom Webpack Config

> Learn how to customize the webpack config used by Next.js

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)webpack

# Custom Webpack Config

Last updated  October 17, 2025

> **Good to know**: changes to webpack config are not covered by semver so proceed at your own risk

Before continuing to add custom webpack configuration to your application make sure Next.js doesn't already support your use-case:

- [CSS imports](https://nextjs.org/docs/app/getting-started/css)
- [CSS modules](https://nextjs.org/docs/app/getting-started/css#css-modules)
- [Sass/SCSS imports](https://nextjs.org/docs/app/guides/sass)
- [Sass/SCSS modules](https://nextjs.org/docs/app/guides/sass)

Some commonly asked for features are available as plugins:

- [@next/mdx](https://github.com/vercel/next.js/tree/canary/packages/next-mdx)
- [@next/bundle-analyzer](https://github.com/vercel/next.js/tree/canary/packages/next-bundle-analyzer)

In order to extend our usage of `webpack`, you can define a function that extends its config inside `next.config.js`, like so:

 next.config.js

```
module.exports = {
  webpack: (
    config,
    { buildId, dev, isServer, defaultLoaders, nextRuntime, webpack }
  ) => {
    // Important: return the modified config
    return config
  },
}
```

> The `webpack` function is executed three times, twice for the server (nodejs / edge runtime) and once for the client. This allows you to distinguish between client and server configuration using the `isServer` property.

The second argument to the `webpack` function is an object with the following properties:

- `buildId`: `String` - The build id, used as a unique identifier between builds.
- `dev`: `Boolean` - Indicates if the compilation will be done in development.
- `isServer`: `Boolean` - It's `true` for server-side compilation, and `false` for client-side compilation.
- `nextRuntime`: `String | undefined` - The target runtime for server-side compilation; either `"edge"` or `"nodejs"`, it's `undefined` for client-side compilation.
- `defaultLoaders`: `Object` - Default loaders used internally by Next.js:
  - `babel`: `Object` - Default `babel-loader` configuration.

Example usage of `defaultLoaders.babel`:

```
// Example config for adding a loader that depends on babel-loader
// This source was taken from the @next/mdx plugin source:
// https://github.com/vercel/next.js/tree/canary/packages/next-mdx
module.exports = {
  webpack: (config, options) => {
    config.module.rules.push({
      test: /\.mdx/,
      use: [
        options.defaultLoaders.babel,
        {
          loader: '@mdx-js/loader',
          options: pluginOptions.options,
        },
      ],
    })

    return config
  },
}
```

#### nextRuntime

Notice that `isServer` is `true` when `nextRuntime` is `"edge"` or `"nodejs"`, `nextRuntime` `"edge"` is currently for proxy and Server Components in edge runtime only.

Was this helpful?

supported.

---

# webVitalsAttribution

> Learn how to use the webVitalsAttribution option to pinpoint the source of Web Vitals issues.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)webVitalsAttribution

# webVitalsAttribution

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

When debugging issues related to Web Vitals, it is often helpful if we can pinpoint the source of the problem.
For example, in the case of Cumulative Layout Shift (CLS), we might want to know the first element that shifted when the single largest layout shift occurred.
Or, in the case of Largest Contentful Paint (LCP), we might want to identify the element corresponding to the LCP for the page.
If the LCP element is an image, knowing the URL of the image resource can help us locate the asset we need to optimize.

Pinpointing the biggest contributor to the Web Vitals score, aka [attribution](https://github.com/GoogleChrome/web-vitals/blob/4ca38ae64b8d1e899028c692f94d4c56acfc996c/README.md#attribution),
allows us to obtain more in-depth information like entries for [PerformanceEventTiming](https://developer.mozilla.org/docs/Web/API/PerformanceEventTiming), [PerformanceNavigationTiming](https://developer.mozilla.org/docs/Web/API/PerformanceNavigationTiming) and [PerformanceResourceTiming](https://developer.mozilla.org/docs/Web/API/PerformanceResourceTiming).

Attribution is disabled by default in Next.js but can be enabled **per metric** by specifying the following in `next.config.js`.

 next.config.js

```
module.exports = {
  experimental: {
    webVitalsAttribution: ['CLS', 'LCP'],
  },
}
```

Valid attribution values are all `web-vitals` metrics specified in the [NextWebVitalsMetric](https://github.com/vercel/next.js/blob/442378d21dd56d6e769863eb8c2cb521a463a2e0/packages/next/shared/lib/utils.ts#L43) type.

Was this helpful?

supported.

---

# next.config.js

> Learn how to configure your application with next.config.js.

[API Reference](https://nextjs.org/docs/app/api-reference)[Configuration](https://nextjs.org/docs/app/api-reference/config)next.config.js

# next.config.js

Last updated  November 4, 2025

Next.js can be configured through a `next.config.js` file in the root of your project directory (for example, by `package.json`) with a default export.

 next.config.js

```
// @ts-check

/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
}

module.exports = nextConfig
```

## ECMAScript Modules

`next.config.js` is a regular Node.js module, not a JSON file. It gets used by the Next.js server and build phases, and it's not included in the browser build.

If you need [ECMAScript modules](https://nodejs.org/api/esm.html), you can use `next.config.mjs`:

 next.config.mjs

```
// @ts-check

/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  /* config options here */
}

export default nextConfig
```

> **Good to know**: `next.config` with the `.cjs` or `.cts` extensions are currently **not** supported.

## Configuration as a Function

You can also use a function:

 next.config.mjs

```
// @ts-check

export default (phase, { defaultConfig }) => {
  /**
   * @type {import('next').NextConfig}
   */
  const nextConfig = {
    /* config options here */
  }
  return nextConfig
}
```

### Async Configuration

Since Next.js 12.1.0, you can use an async function:

 next.config.js

```
// @ts-check

module.exports = async (phase, { defaultConfig }) => {
  /**
   * @type {import('next').NextConfig}
   */
  const nextConfig = {
    /* config options here */
  }
  return nextConfig
}
```

### Phase

`phase` is the current context in which the configuration is loaded. You can see the [available phases](https://github.com/vercel/next.js/blob/5e6b008b561caf2710ab7be63320a3d549474a5b/packages/next/shared/lib/constants.ts#L19-L23). Phases can be imported from `next/constants`:

 next.config.js

```
// @ts-check

const { PHASE_DEVELOPMENT_SERVER } = require('next/constants')

module.exports = (phase, { defaultConfig }) => {
  if (phase === PHASE_DEVELOPMENT_SERVER) {
    return {
      /* development only config options here */
    }
  }

  return {
    /* config options for all phases except development here */
  }
}
```

## TypeScript

If you are using TypeScript in your project, you can use `next.config.ts` to use TypeScript in your configuration:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  /* config options here */
}

export default nextConfig
```

The commented lines are the place where you can put the configs allowed by `next.config.js`, which are [defined in this file](https://github.com/vercel/next.js/blob/canary/packages/next/src/server/config-shared.ts).

However, none of the configs are required, and it's not necessary to understand what each config does. Instead, search for the features you need to enable or modify in this section and they will show you what to do.

> Avoid using new JavaScript features not available in your target Node.js version. `next.config.js` will not be parsed by Webpack or Babel.

This page documents all the available configuration options:

## Unit Testing (experimental)

Starting in Next.js 15.1, the `next/experimental/testing/server` package contains utilities to help unit test `next.config.js` files.

The `unstable_getResponseFromNextConfig` function runs the [headers](https://nextjs.org/docs/app/api-reference/config/next-config-js/headers), [redirects](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects), and [rewrites](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites) functions from `next.config.js` with the provided request information and returns `NextResponse` with the results of the routing.

> The response from `unstable_getResponseFromNextConfig` only considers `next.config.js` fields and does not consider proxy or filesystem routes, so the result in production may be different than the unit test.

```
import {
  getRedirectUrl,
  unstable_getResponseFromNextConfig,
} from 'next/experimental/testing/server'

const response = await unstable_getResponseFromNextConfig({
  url: 'https://nextjs.org/test',
  nextConfig: {
    async redirects() {
      return [{ source: '/test', destination: '/test2', permanent: false }]
    },
  },
})
expect(response.status).toEqual(307)
expect(getRedirectUrl(response)).toEqual('https://nextjs.org/test2')
```

[experimental.adapterPathConfigure a custom adapter for Next.js to hook into the build process with modifyConfig and onBuildComplete callbacks.](https://nextjs.org/docs/app/api-reference/config/next-config-js/adapterPath)[allowedDevOriginsUse `allowedDevOrigins` to configure additional origins that can request the dev server.](https://nextjs.org/docs/app/api-reference/config/next-config-js/allowedDevOrigins)[appDirEnable the App Router to use layouts, streaming, and more.](https://nextjs.org/docs/app/api-reference/config/next-config-js/appDir)[assetPrefixLearn how to use the assetPrefix config option to configure your CDN.](https://nextjs.org/docs/app/api-reference/config/next-config-js/assetPrefix)[authInterruptsLearn how to enable the experimental `authInterrupts` configuration option to use `forbidden` and `unauthorized`.](https://nextjs.org/docs/app/api-reference/config/next-config-js/authInterrupts)[basePathUse `basePath` to deploy a Next.js application under a sub-path of a domain.](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath)[browserDebugInfoInTerminalForward browser console logs and errors to your terminal during development.](https://nextjs.org/docs/app/api-reference/config/next-config-js/browserDebugInfoInTerminal)[cacheComponentsLearn how to enable the cacheComponents flag in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)[cacheHandlersConfigure custom cache handlers for use cache directives in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheHandlers)[cacheLifeLearn how to set up cacheLife configurations in Next.js.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheLife)[compressNext.js provides gzip compression to compress rendered content and static files, it only works with the server target. Learn more about it here.](https://nextjs.org/docs/app/api-reference/config/next-config-js/compress)[crossOriginUse the `crossOrigin` option to add a crossOrigin tag on the `script` tags generated by `next/script`.](https://nextjs.org/docs/app/api-reference/config/next-config-js/crossOrigin)[cssChunkingUse the `cssChunking` option to control how CSS files are chunked in your Next.js application.](https://nextjs.org/docs/app/api-reference/config/next-config-js/cssChunking)[devIndicatorsConfiguration options for the on-screen indicator that gives context about the current route you're viewing during development.](https://nextjs.org/docs/app/api-reference/config/next-config-js/devIndicators)[distDirSet a custom build directory to use instead of the default .next directory.](https://nextjs.org/docs/app/api-reference/config/next-config-js/distDir)[envLearn to add and access environment variables in your Next.js application at build time.](https://nextjs.org/docs/app/api-reference/config/next-config-js/env)[expireTimeCustomize stale-while-revalidate expire time for ISR enabled pages.](https://nextjs.org/docs/app/api-reference/config/next-config-js/expireTime)[exportPathMapCustomize the pages that will be exported as HTML files when using `next export`.](https://nextjs.org/docs/app/api-reference/config/next-config-js/exportPathMap)[generateBuildIdConfigure the build id, which is used to identify the current build in which your application is being served.](https://nextjs.org/docs/app/api-reference/config/next-config-js/generateBuildId)[generateEtagsNext.js will generate etags for every page by default. Learn more about how to disable etag generation here.](https://nextjs.org/docs/app/api-reference/config/next-config-js/generateEtags)[headersAdd custom HTTP headers to your Next.js app.](https://nextjs.org/docs/app/api-reference/config/next-config-js/headers)[htmlLimitedBotsSpecify a list of user agents that should receive blocking metadata.](https://nextjs.org/docs/app/api-reference/config/next-config-js/htmlLimitedBots)[httpAgentOptionsNext.js will automatically use HTTP Keep-Alive by default. Learn more about how to disable HTTP Keep-Alive here.](https://nextjs.org/docs/app/api-reference/config/next-config-js/httpAgentOptions)[imagesCustom configuration for the next/image loader](https://nextjs.org/docs/app/api-reference/config/next-config-js/images)[cacheHandlerConfigure the Next.js cache used for storing and revalidating data to use any external service like Redis, Memcached, or others.](https://nextjs.org/docs/app/api-reference/config/next-config-js/incrementalCacheHandlerPath)[inlineCssEnable inline CSS support.](https://nextjs.org/docs/app/api-reference/config/next-config-js/inlineCss)[isolatedDevBuildUse isolated build outputs for development server to prevent conflicts with production builds.](https://nextjs.org/docs/app/api-reference/config/next-config-js/isolatedDevBuild)[loggingConfigure how data fetches are logged to the console when running Next.js in development mode.](https://nextjs.org/docs/app/api-reference/config/next-config-js/logging)[mdxRsUse the new Rust compiler to compile MDX files in the App Router.](https://nextjs.org/docs/app/api-reference/config/next-config-js/mdxRs)[onDemandEntriesConfigure how Next.js will dispose and keep in memory pages created in development.](https://nextjs.org/docs/app/api-reference/config/next-config-js/onDemandEntries)[optimizePackageImportsAPI Reference for optimizePackageImports Next.js Config Option](https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports)[outputNext.js automatically traces which files are needed by each page to allow for easy deployment of your application. Learn how it works here.](https://nextjs.org/docs/app/api-reference/config/next-config-js/output)[pageExtensionsExtend the default page extensions used by Next.js when resolving pages in the Pages Router.](https://nextjs.org/docs/app/api-reference/config/next-config-js/pageExtensions)[poweredByHeaderNext.js will add the `x-powered-by` header by default. Learn to opt-out of it here.](https://nextjs.org/docs/app/api-reference/config/next-config-js/poweredByHeader)[productionBrowserSourceMapsEnables browser source map generation during the production build.](https://nextjs.org/docs/app/api-reference/config/next-config-js/productionBrowserSourceMaps)[proxyClientMaxBodySizeConfigure the maximum request body size when using proxy.](https://nextjs.org/docs/app/api-reference/config/next-config-js/proxyClientMaxBodySize)[reactCompilerEnable the React Compiler to automatically optimize component rendering.](https://nextjs.org/docs/app/api-reference/config/next-config-js/reactCompiler)[reactMaxHeadersLengthThe maximum length of the headers that are emitted by React and added to the response.](https://nextjs.org/docs/app/api-reference/config/next-config-js/reactMaxHeadersLength)[reactStrictModeThe complete Next.js runtime is now Strict Mode-compliant, learn how to opt-in](https://nextjs.org/docs/app/api-reference/config/next-config-js/reactStrictMode)[redirectsAdd redirects to your Next.js app.](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects)[rewritesAdd rewrites to your Next.js app.](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites)[sassOptionsConfigure Sass options.](https://nextjs.org/docs/app/api-reference/config/next-config-js/sassOptions)[serverActionsConfigure Server Actions behavior in your Next.js application.](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverActions)[serverComponentsHmrCacheConfigure whether fetch responses in Server Components are cached across HMR refresh requests.](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverComponentsHmrCache)[serverExternalPackagesOpt-out specific dependencies from the Server Components bundling and use native Node.js `require`.](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverExternalPackages)[staleTimesLearn how to override the invalidation time of the Client Router Cache.](https://nextjs.org/docs/app/api-reference/config/next-config-js/staleTimes)[staticGeneration*Learn how to configure static generation in your Next.js application.](https://nextjs.org/docs/app/api-reference/config/next-config-js/staticGeneration)[taintEnable tainting Objects and Values.](https://nextjs.org/docs/app/api-reference/config/next-config-js/taint)[trailingSlashConfigure Next.js pages to resolve with or without a trailing slash.](https://nextjs.org/docs/app/api-reference/config/next-config-js/trailingSlash)[transpilePackagesAutomatically transpile and bundle dependencies from local packages (like monorepos) or from external dependencies (`node_modules`).](https://nextjs.org/docs/app/api-reference/config/next-config-js/transpilePackages)[turbopackConfigure Next.js with Turbopack-specific options](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack)[turbopackFileSystemCacheLearn how to enable FileSystem Caching for Turbopack builds](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache)[typedRoutesEnable support for statically typed links.](https://nextjs.org/docs/app/api-reference/config/next-config-js/typedRoutes)[typescriptConfigure how Next.js handles TypeScript errors during production builds and specify a custom tsconfig file.](https://nextjs.org/docs/app/api-reference/config/next-config-js/typescript)[urlImportsConfigure Next.js to allow importing modules from external URLs.](https://nextjs.org/docs/app/api-reference/config/next-config-js/urlImports)[useLightningcssEnable experimental support for Lightning CSS.](https://nextjs.org/docs/app/api-reference/config/next-config-js/useLightningcss)[viewTransitionEnable ViewTransition API from React in App Router](https://nextjs.org/docs/app/api-reference/config/next-config-js/viewTransition)[webpackLearn how to customize the webpack config used by Next.js](https://nextjs.org/docs/app/api-reference/config/next-config-js/webpack)[webVitalsAttributionLearn how to use the webVitalsAttribution option to pinpoint the source of Web Vitals issues.](https://nextjs.org/docs/app/api-reference/config/next-config-js/webVitalsAttribution)

Was this helpful?

supported.
