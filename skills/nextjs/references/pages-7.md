# turbopack and more

# turbopack

> Configure Next.js with Turbopack-specific options

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)turbopackYou are currently viewing the documentation for Pages Router.

# turbopack

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  September 22, 2025

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

# typescript

> Next.js reports TypeScript errors by default. Learn to opt-out of this behavior here.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)typescriptYou are currently viewing the documentation for Pages Router.

# typescript

Last updated  April 15, 2025

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

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)urlImportsYou are currently viewing the documentation for Pages Router.

# urlImports

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  April 15, 2025

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

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)useLightningcssYou are currently viewing the documentation for Pages Router.

# useLightningcss

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  April 15, 2025

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

# Custom Webpack Config

> Learn how to customize the webpack config used by Next.js

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)webpackYou are currently viewing the documentation for Pages Router.

# Custom Webpack Config

Last updated  April 15, 2025

> **Good to know**: changes to webpack config are not covered by semver so proceed at your own risk

Before continuing to add custom webpack configuration to your application make sure Next.js doesn't already support your use-case:

- [CSS imports](https://nextjs.org/docs/app/getting-started/css)
- [CSS modules](https://nextjs.org/docs/app/getting-started/css)
- [Sass/SCSS imports](https://nextjs.org/docs/pages/guides/sass)
- [Sass/SCSS modules](https://nextjs.org/docs/pages/guides/sass)
- [Customizing babel configuration](https://nextjs.org/docs/pages/guides/babel)

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

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)webVitalsAttributionYou are currently viewing the documentation for Pages Router.

# webVitalsAttribution

Last updated  April 15, 2025

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

# next.config.js Options

> Learn about the options available in next.config.js for the Pages Router.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Configuration](https://nextjs.org/docs/pages/api-reference/config)next.config.js OptionsYou are currently viewing the documentation for Pages Router.

# next.config.js Options

Last updated  April 15, 2025

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

[experimental.adapterPathConfigure a custom adapter for Next.js to hook into the build process with modifyConfig and buildComplete callbacks.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/adapterPath)[allowedDevOriginsUse `allowedDevOrigins` to configure additional origins that can request the dev server.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/allowedDevOrigins)[assetPrefixLearn how to use the assetPrefix config option to configure your CDN.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/assetPrefix)[basePathUse `basePath` to deploy a Next.js application under a sub-path of a domain.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/basePath)[bundlePagesRouterDependenciesEnable automatic dependency bundling for Pages Router](https://nextjs.org/docs/pages/api-reference/config/next-config-js/bundlePagesRouterDependencies)[compressNext.js provides gzip compression to compress rendered content and static files, it only works with the server target. Learn more about it here.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/compress)[crossOriginUse the `crossOrigin` option to add a crossOrigin tag on the `script` tags generated by `next/script` and `next/head`.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/crossOrigin)[devIndicatorsOptimized pages include an indicator to let you know if it's being statically optimized. You can opt-out of it here.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/devIndicators)[distDirSet a custom build directory to use instead of the default .next directory.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/distDir)[envLearn to add and access environment variables in your Next.js application at build time.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/env)[exportPathMapCustomize the pages that will be exported as HTML files when using `next export`.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/exportPathMap)[generateBuildIdConfigure the build id, which is used to identify the current build in which your application is being served.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/generateBuildId)[generateEtagsNext.js will generate etags for every page by default. Learn more about how to disable etag generation here.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/generateEtags)[headersAdd custom HTTP headers to your Next.js app.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/headers)[httpAgentOptionsNext.js will automatically use HTTP Keep-Alive by default. Learn more about how to disable HTTP Keep-Alive here.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/httpAgentOptions)[imagesCustom configuration for the next/image loader](https://nextjs.org/docs/pages/api-reference/config/next-config-js/images)[isolatedDevBuildUse isolated directories for development builds to prevent conflicts with production builds.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/isolatedDevBuild)[onDemandEntriesConfigure how Next.js will dispose and keep in memory pages created in development.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/onDemandEntries)[optimizePackageImportsAPI Reference for optimizePackageImports Next.js Config Option](https://nextjs.org/docs/pages/api-reference/config/next-config-js/optimizePackageImports)[outputNext.js automatically traces which files are needed by each page to allow for easy deployment of your application. Learn how it works here.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/output)[pageExtensionsExtend the default page extensions used by Next.js when resolving pages in the Pages Router.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/pageExtensions)[poweredByHeaderNext.js will add the `x-powered-by` header by default. Learn to opt-out of it here.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/poweredByHeader)[productionBrowserSourceMapsEnables browser source map generation during the production build.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/productionBrowserSourceMaps)[experimental.proxyClientMaxBodySizeConfigure the maximum request body size when using proxy.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/proxyClientMaxBodySize)[reactStrictModeThe complete Next.js runtime is now Strict Mode-compliant, learn how to opt-in](https://nextjs.org/docs/pages/api-reference/config/next-config-js/reactStrictMode)[redirectsAdd redirects to your Next.js app.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/redirects)[rewritesAdd rewrites to your Next.js app.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/rewrites)[serverExternalPackagesOpt-out specific dependencies from the dependency bundling enabled by `bundlePagesRouterDependencies`.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/serverExternalPackages)[trailingSlashConfigure Next.js pages to resolve with or without a trailing slash.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/trailingSlash)[transpilePackagesAutomatically transpile and bundle dependencies from local packages (like monorepos) or from external dependencies (`node_modules`).](https://nextjs.org/docs/pages/api-reference/config/next-config-js/transpilePackages)[turbopackConfigure Next.js with Turbopack-specific options](https://nextjs.org/docs/pages/api-reference/config/next-config-js/turbopack)[typescriptNext.js reports TypeScript errors by default. Learn to opt-out of this behavior here.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/typescript)[urlImportsConfigure Next.js to allow importing modules from external URLs.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/urlImports)[useLightningcssEnable experimental support for Lightning CSS.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/useLightningcss)[webpackLearn how to customize the webpack config used by Next.js](https://nextjs.org/docs/pages/api-reference/config/next-config-js/webpack)[webVitalsAttributionLearn how to use the webVitalsAttribution option to pinpoint the source of Web Vitals issues.](https://nextjs.org/docs/pages/api-reference/config/next-config-js/webVitalsAttribution)

Was this helpful?

supported.

---

# TypeScript

> Next.js provides a TypeScript-first development experience for building your React application.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Configuration](https://nextjs.org/docs/pages/api-reference/config)TypeScriptYou are currently viewing the documentation for Pages Router.

# TypeScript

Last updated  April 15, 2025

Next.js comes with built-in TypeScript, automatically installing the necessary packages and configuring the proper settings when you create a new project with `create-next-app`.

To add TypeScript to an existing project, rename a file to `.ts` / `.tsx`. Run `next dev` and `next build` to automatically install the necessary dependencies and add a `tsconfig.json` file with the recommended config options.

> **Good to know**: If you already have a `jsconfig.json` file, copy the `paths` compiler option from the old `jsconfig.json` into the new `tsconfig.json` file, and delete the old `jsconfig.json` file.

## next-env.d.ts

Next.js generates a `next-env.d.ts` file in your project root. This file references Next.js type definitions, allowing TypeScript to recognize non-code imports (images, stylesheets, etc.) and Next.js-specific types.

Running `next dev`, `next build`, or [next typegen](https://nextjs.org/docs/app/api-reference/cli/next#next-typegen-options) regenerates this file.

> **Good to know**:
>
>
>
> - We recommend adding `next-env.d.ts` to your `.gitignore` file.
> - The file must be in your `tsconfig.json` `include` array (`create-next-app` does this automatically).

## Examples

### Type Checking Next.js Configuration Files

You can use TypeScript and import types in your Next.js configuration by using `next.config.ts`.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  /* config options here */
}

export default nextConfig
```

Module resolution in `next.config.ts` is currently limited to CommonJS. However, ECMAScript Modules (ESM) syntax is available when [using Node.js native TypeScript resolver](#using-nodejs-native-typescript-resolver-for-nextconfigts) for Node.js v22.10.0 and higher.

When using the `next.config.js` file, you can add some type checking in your IDE using JSDoc as below:

 next.config.js

```
// @ts-check

/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
}

module.exports = nextConfig
```

### Using Node.js Native TypeScript Resolver fornext.config.ts

> **Note**: Available on Node.js v22.10.0+ and only when the feature is enabled. Next.js does not enable it.

Next.js detects the [Node.js native TypeScript resolver](https://nodejs.org/api/typescript.html) via [process.features.typescript](https://nodejs.org/api/process.html#processfeaturestypescript), added in **v22.10.0**. When present, `next.config.ts` can use native ESM, including top‑level `await` and dynamic `import()`. This mechanism inherits the capabilities and limitations of Node's resolver.

In Node.js versions **v22.18.0+**, `process.features.typescript` is enabled by default. For versions between **v22.10.0** and **22.17.x**, opt in with `NODE_OPTIONS=--experimental-transform-types`:

 Terminal

```
NODE_OPTIONS=--experimental-transform-types next <command>
```

#### For CommonJS Projects (Default)

Although `next.config.ts` supports native ESM syntax in CommonJS projects, Node.js will still assume `next.config.ts` is a CommonJS file by default, resulting in Node.js reparsing the file as ESM when module syntax is detected. Therefore, we recommend using the `next.config.mts` file for CommonJS projects to explicitly indicate it's an ESM module:

 next.config.mts

```
import type { NextConfig } from 'next'

// Top-level await and dynamic import are supported
const flags = await import('./flags.js').then((m) => m.default ?? m)

const nextConfig: NextConfig = {
  /* config options here */
  typedRoutes: Boolean(flags?.typedRoutes),
}

export default nextConfig
```

#### For ESM Projects

When `"type"` is set to `"module"` in `package.json`, your project uses ESM. Learn more about this setting [in the Node.js docs](https://nodejs.org/api/packages.html#type). In this case, you can write `next.config.ts` directly with ESM syntax.

> **Good to know**: When using `"type": "module"` in your `package.json`, all `.js` and `.ts` files in your project are treated as ESM modules by default. You may need to rename files with CommonJS syntax to `.cjs` or `.cts` extensions if needed.

### Statically Typed Links

Next.js can statically type links to prevent typos and other errors when using `next/link`, improving type safety when navigating between pages.

Works in both the Pages and App Router for the `href` prop in `next/link`. In the App Router, it also types `next/navigation` methods like `push`, `replace`, and `prefetch`. It does not type `next/router` methods in Pages Router.

Literal `href` strings are validated, while non-literal `href`s may require a cast with `as Route`.

To opt-into this feature, `typedRoutes` needs to be enabled and the project needs to be using TypeScript.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  typedRoutes: true,
}

export default nextConfig
```

Next.js will generate a link definition in `.next/types` that contains information about all existing routes in your application, which TypeScript can then use to provide feedback in your editor about invalid links.

> **Good to know**: If you set up your project without `create-next-app`, ensure the generated Next.js types are included by adding `.next/types/**/*.ts` to the `include` array in your `tsconfig.json`:

   tsconfig.json

```
{
  "include": [
    "next-env.d.ts",
    ".next/types/**/*.ts",
    "**/*.ts",
    "**/*.tsx"
  ],
  "exclude": ["node_modules"]
}
```

Currently, support includes any string literal, including dynamic segments. For non-literal strings, you need to manually cast with `as Route`. The example below shows both `next/link` and `next/navigation` usage:

 app/example-client.tsx

```
'use client'

import type { Route } from 'next'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export default function Example() {
  const router = useRouter()
  const slug = 'nextjs'

  return (
    <>
      {/* Link: literal and dynamic */}
      <Link href="/about" />
      <Link href={`/blog/${slug}`} />
      <Link href={('/blog/' + slug) as Route} />
      {/* TypeScript error if href is not a valid route */}
      <Link href="/aboot" />

      {/* Router: literal and dynamic strings are validated */}
      <button onClick={() => router.push('/about')}>Push About</button>
      <button onClick={() => router.replace(`/blog/${slug}`)}>
        Replace Blog
      </button>
      <button onClick={() => router.prefetch('/contact')}>
        Prefetch Contact
      </button>

      {/* For non-literal strings, cast to Route */}
      <button onClick={() => router.push(('/blog/' + slug) as Route)}>
        Push Non-literal Blog
      </button>
    </>
  )
}
```

The same applies for redirecting routes defined by proxy:

 proxy.ts

```
import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  if (request.nextUrl.pathname === '/proxy-redirect') {
    return NextResponse.redirect(new URL('/', request.url))
  }

  return NextResponse.next()
}
```

 app/some/page.tsx

```
import type { Route } from 'next'

export default function Page() {
  return <Link href={'/proxy-redirect' as Route}>Link Text</Link>
}
```

To accept `href` in a custom component wrapping `next/link`, use a generic:

```
import type { Route } from 'next'
import Link from 'next/link'

function Card<T extends string>({ href }: { href: Route<T> | URL }) {
  return (
    <Link href={href}>
      <div>My Card</div>
    </Link>
  )
}
```

You can also type a simple data structure and iterate to render links:

 components/nav-items.ts

```
import type { Route } from 'next'

type NavItem<T extends string = string> = {
  href: T
  label: string
}

export const navItems: NavItem<Route>[] = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About' },
  { href: '/blog', label: 'Blog' },
]
```

Then, map over the items to render `Link`s:

 components/nav.tsx

```
import Link from 'next/link'
import { navItems } from './nav-items'

export function Nav() {
  return (
    <nav>
      {navItems.map((item) => (
        <Link key={item.href} href={item.href}>
          {item.label}
        </Link>
      ))}
    </nav>
  )
}
```

> **How does it work?**
>
>
>
> When running `next dev` or `next build`, Next.js generates a hidden `.d.ts` file inside `.next` that contains information about all existing routes in your application (all valid routes as the `href` type of `Link`). This `.d.ts` file is included in `tsconfig.json` and the TypeScript compiler will check that `.d.ts` and provide feedback in your editor about invalid links.

### Type IntelliSense for Environment Variables

During development, Next.js generates a `.d.ts` file in `.next/types` that contains information about the loaded environment variables for your editor's IntelliSense. If the same environment variable key is defined in multiple files, it is deduplicated according to the [Environment Variable Load Order](https://nextjs.org/docs/app/guides/environment-variables#environment-variable-load-order).

To opt-into this feature, `experimental.typedEnv` needs to be enabled and the project needs to be using TypeScript.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    typedEnv: true,
  },
}

export default nextConfig
```

> **Good to know**: Types are generated based on the environment variables loaded at development runtime, which excludes variables from `.env.production*` files by default. To include production-specific variables, run `next dev` with `NODE_ENV=production`.

### Static Generation and Server-side Rendering

For [getStaticProps](https://nextjs.org/docs/pages/api-reference/functions/get-static-props), [getStaticPaths](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths), and [getServerSideProps](https://nextjs.org/docs/pages/api-reference/functions/get-server-side-props), you can use the `GetStaticProps`, `GetStaticPaths`, and `GetServerSideProps` types respectively:

pages/blog/[slug].tsx

```
import type { GetStaticProps, GetStaticPaths, GetServerSideProps } from 'next'

export const getStaticProps = (async (context) => {
  // ...
}) satisfies GetStaticProps

export const getStaticPaths = (async () => {
  // ...
}) satisfies GetStaticPaths

export const getServerSideProps = (async (context) => {
  // ...
}) satisfies GetServerSideProps
```

> **Good to know:** `satisfies` was added to TypeScript in [4.9](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html). We recommend upgrading to the latest version of TypeScript.

### With API Routes

The following is an example of how to use the built-in types for API routes:

pages/api/hello.ts

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ name: 'John Doe' })
}
```

You can also type the response data:

pages/api/hello.ts

```
import type { NextApiRequest, NextApiResponse } from 'next'

type Data = {
  name: string
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  res.status(200).json({ name: 'John Doe' })
}
```

### With customApp

If you have a [customApp](https://nextjs.org/docs/pages/building-your-application/routing/custom-app), you can use the built-in type `AppProps` and change file name to `./pages/_app.tsx` like so:

```
import type { AppProps } from 'next/app'

export default function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
```

### Incremental type checking

Since `v10.2.1` Next.js supports [incremental type checking](https://www.typescriptlang.org/tsconfig#incremental) when enabled in your `tsconfig.json`, this can help speed up type checking in larger applications.

### Customtsconfigpath

In some cases, you might want to use a different TypeScript configuration for builds or tooling. To do that, set `typescript.tsconfigPath` in `next.config.ts` to point Next.js to another `tsconfig` file.

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  typescript: {
    tsconfigPath: 'tsconfig.build.json',
  },
}

export default nextConfig
```

For example, switch to a different config for production builds:

 next.config.ts

```
import type { NextConfig } from 'next'

const isProd = process.env.NODE_ENV === 'production'

const nextConfig: NextConfig = {
  typescript: {
    tsconfigPath: isProd ? 'tsconfig.build.json' : 'tsconfig.json',
  },
}

export default nextConfig
```

 Why you might use a separate `tsconfig` for builds

You might need to relax checks in scenarios like monorepos, where the build also validates shared dependencies that don't match your project's standards, or when loosening checks in CI to continue delivering while migrating locally to stricter TypeScript settings (and still wanting your IDE to highlight misuse).

For example, if your project uses `useUnknownInCatchVariables` but some monorepo dependencies still assume `any`:

tsconfig.build.json

```
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "useUnknownInCatchVariables": false
  }
}
```

This keeps your editor strict via `tsconfig.json` while allowing the production build to use relaxed settings.

> **Good to know**:
>
>
>
> - IDEs typically read `tsconfig.json` for diagnostics and IntelliSense, so you can still see IDE warnings while production builds use the alternate config. Mirror critical options if you want parity in the editor.
> - In development, only `tsconfig.json` is watched for changes. If you edit a different file name via `typescript.tsconfigPath`, restart the dev server to apply changes.
> - The configured file is used in `next dev`, `next build`, and `next typegen`.

### Disabling TypeScript errors in production

Next.js fails your **production build** (`next build`) when TypeScript errors are present in your project.

If you'd like Next.js to dangerously produce production code even when your application has errors, you can disable the built-in type checking step.

If disabled, be sure you are running type checks as part of your build or deploy process, otherwise this can be very dangerous.

Open `next.config.ts` and enable the `ignoreBuildErrors` option in the [typescript](https://nextjs.org/docs/app/api-reference/config/next-config-js/typescript) config:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
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

> **Good to know**: You can run `tsc --noEmit` to check for TypeScript errors yourself before building. This is useful for CI/CD pipelines where you'd like to check for TypeScript errors before deploying.

### Custom type declarations

When you need to declare custom types, you might be tempted to modify `next-env.d.ts`. However, this file is automatically generated, so any changes you make will be overwritten. Instead, you should create a new file, let's call it `new-types.d.ts`, and reference it in your `tsconfig.json`:

 tsconfig.json

```
{
  "compilerOptions": {
    "skipLibCheck": true
    //...truncated...
  },
  "include": [
    "new-types.d.ts",
    "next-env.d.ts",
    ".next/types/**/*.ts",
    "**/*.ts",
    "**/*.tsx"
  ],
  "exclude": ["node_modules"]
}
```

## Version Changes

| Version | Changes |
| --- | --- |
| v15.0.0 | next.config.tssupport added for TypeScript projects. |
| v13.2.0 | Statically typed links are available in beta. |
| v12.0.0 | SWCis now used by default to compile TypeScript and TSX for faster builds. |
| v10.2.1 | Incremental type checkingsupport added when enabled in yourtsconfig.json. |

Was this helpful?

supported.

---

# Configuration

> Learn how to configure your Next.js application.

[Pages Router](https://nextjs.org/docs/pages)[API Reference](https://nextjs.org/docs/pages/api-reference)ConfigurationYou are currently viewing the documentation for Pages Router.

# Configuration

Last updated  April 15, 2025[next.config.js OptionsLearn about the options available in next.config.js for the Pages Router.](https://nextjs.org/docs/pages/api-reference/config/next-config-js)[TypeScriptNext.js provides a TypeScript-first development experience for building your React application.](https://nextjs.org/docs/pages/api-reference/config/typescript)[ESLintNext.js reports ESLint errors and warnings during builds by default. Learn how to opt-out of this behavior here.](https://nextjs.org/docs/pages/api-reference/config/eslint)

Was this helpful?

supported.
