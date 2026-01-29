# Accessibility and more

# Accessibility

> The built-in accessibility features of Next.js.

[Next.js Docs](https://nextjs.org/docs)[Architecture](https://nextjs.org/docs/architecture)Accessibility

# Accessibility

Last updated  November 6, 2024

The Next.js team is committed to making Next.js accessible to all developers (and their end-users). By adding accessibility features to Next.js by default, we aim to make the Web more inclusive for everyone.

## Route Announcements

When transitioning between pages rendered on the server (e.g. using the `<a href>` tag) screen readers and other assistive technology announce the page title when the page loads so that users understand that the page has changed.

In addition to traditional page navigations, Next.js also supports client-side transitions for improved performance (using `next/link`). To ensure that client-side transitions are also announced to assistive technology, Next.js includes a route announcer by default.

The Next.js route announcer looks for the page name to announce by first inspecting `document.title`, then the `<h1>` element, and finally the URL pathname. For the most accessible user experience, ensure that each page in your application has a unique and descriptive title.

## Linting

Next.js provides an [integrated ESLint experience](https://nextjs.org/docs/pages/api-reference/config/eslint) out of the box, including custom rules for Next.js. By default, Next.js includes `eslint-plugin-jsx-a11y` to help catch accessibility issues early, including warning on:

- [aria-props](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y/blob/HEAD/docs/rules/aria-props.md?rgh-link-date=2021-06-04T02%3A10%3A36Z)
- [aria-proptypes](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y/blob/HEAD/docs/rules/aria-proptypes.md?rgh-link-date=2021-06-04T02%3A10%3A36Z)
- [aria-unsupported-elements](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y/blob/HEAD/docs/rules/aria-unsupported-elements.md?rgh-link-date=2021-06-04T02%3A10%3A36Z)
- [role-has-required-aria-props](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y/blob/HEAD/docs/rules/role-has-required-aria-props.md?rgh-link-date=2021-06-04T02%3A10%3A36Z)
- [role-supports-aria-props](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y/blob/HEAD/docs/rules/role-supports-aria-props.md?rgh-link-date=2021-06-04T02%3A10%3A36Z)

For example, this plugin helps ensure you add alt text to `img` tags, use correct `aria-*` attributes, use correct `role` attributes, and more.

## Accessibility Resources

- [WebAIM WCAG checklist](https://webaim.org/standards/wcag/checklist)
- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [The A11y Project](https://www.a11yproject.com/)
- Check [color contrast ratios](https://developer.mozilla.org/docs/Web/Accessibility/Understanding_WCAG/Perceivable/Color_contrast) between foreground and background elements
- Use [prefers-reduced-motion](https://web.dev/prefers-reduced-motion/) when working with animations

Was this helpful?

supported.

---

# Fast Refresh

> Fast Refresh is a hot module reloading experience that gives you instantaneous feedback on edits made to your React components.

[Next.js Docs](https://nextjs.org/docs)[Architecture](https://nextjs.org/docs/architecture)Fast Refresh

# Fast Refresh

Last updated  October 27, 2025

Fast refresh is a React feature integrated into Next.js that allows you to live reload the browser page while maintaining temporary client-side state when you save changes to a file. It's enabled by default in all Next.js applications on **9.4 or newer**. With Fast Refresh enabled, most edits should be visible within a second.

## How It Works

- If you edit a file that **only exports React component(s)**, Fast Refresh will
  update the code only for that file, and re-render your component. You can edit
  anything in that file, including styles, rendering logic, event handlers, or
  effects.
- If you edit a file with exports that *aren't* React components, Fast Refresh
  will re-run both that file, and the other files importing it. So if both
  `Button.js` and `Modal.js` import `theme.js`, editing `theme.js` will update
  both components.
- Finally, if you **edit a file** that's **imported by files outside of the
  React tree**, Fast Refresh **will fall back to doing a full reload**. You
  might have a file which renders a React component but also exports a value
  that is imported by a **non-React component**. For example, maybe your
  component also exports a constant, and a non-React utility file imports it. In
  that case, consider migrating the constant to a separate file and importing it
  into both files. This will re-enable Fast Refresh to work. Other cases can
  usually be solved in a similar way.

## Error Resilience

### Syntax Errors

If you make a syntax error during development, you can fix it and save the file
again. The error will disappear automatically, so you won't need to reload the
app. **You will not lose component state**.

### Runtime Errors

If you make a mistake that leads to a runtime error inside your component,
you'll be greeted with a contextual overlay. Fixing the error will automatically
dismiss the overlay, without reloading the app.

Component state will be retained if the error did not occur during rendering. If
the error did occur during rendering, React will remount your application using
the updated code.

If you have [error boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
in your app (which is a good idea for graceful failures in production), they
will retry rendering on the next edit after a rendering error. This means having
an error boundary can prevent you from always getting reset to the root app
state. However, keep in mind that error boundaries shouldn't be *too* granular.
They are used by React in production, and should always be designed
intentionally.

## Limitations

Fast Refresh tries to preserve local React state in the component you're
editing, but only if it's safe to do so. Here's a few reasons why you might see
local state being reset on every edit to a file:

- Local state is not preserved for class components (only function components
  and Hooks preserve state).
- The file you're editing might have *other* exports in addition to a React
  component.
- Sometimes, a file would export the result of calling a higher-order component
  like `HOC(WrappedComponent)`. If the returned component is a
  class, its state will be reset.
- Anonymous arrow functions like `export default () => <div />;` cause Fast Refresh to not preserve local component state. For large codebases you can use our [name-default-componentcodemod](https://nextjs.org/docs/pages/guides/upgrading/codemods#name-default-component).

As more of your codebase moves to function components and Hooks, you can expect
state to be preserved in more cases.

## Tips

- Fast Refresh preserves React local state in function components (and Hooks) by
  default.
- Sometimes you might want to *force* the state to be reset, and a component to
  be remounted. For example, this can be handy if you're tweaking an animation
  that only happens on mount. To do this, you can add `// @refresh reset`
  anywhere in the file you're editing. This directive is local to the file, and
  instructs Fast Refresh to remount components defined in that file on every
  edit.
- You can put `console.log` or `debugger;` into the components you edit during
  development.
- Remember that imports are case sensitive. Both fast and full refresh can fail,
  when your import doesn't match the actual filename.
  For example, `'./header'` vs `'./Header'`.

## Fast Refresh and Hooks

When possible, Fast Refresh attempts to preserve the state of your component
between edits. In particular, `useState` and `useRef` preserve their previous
values as long as you don't change their arguments or the order of the Hook
calls.

Hooks with dependencies—such as `useEffect`, `useMemo`, and `useCallback`—will
*always* update during Fast Refresh. Their list of dependencies will be ignored
while Fast Refresh is happening.

For example, when you edit `useMemo(() => x * 2, [x])` to
`useMemo(() => x * 10, [x])`, it will re-run even though `x` (the dependency)
has not changed. If React didn't do that, your edit wouldn't reflect on the
screen!

Sometimes, this can lead to unexpected results. For example, even a `useEffect`
with an empty array of dependencies would still re-run once during Fast Refresh.

However, writing code resilient to occasional re-running of `useEffect` is a good practice even
without Fast Refresh. It will make it easier for you to introduce new dependencies to it later on
and it's enforced by [React Strict Mode](https://nextjs.org/docs/pages/api-reference/config/next-config-js/reactStrictMode),
which we highly recommend enabling.

Was this helpful?

supported.

---

# Next.js Compiler

> Next.js Compiler, written in Rust, which transforms and minifies your Next.js application.

[Next.js Docs](https://nextjs.org/docs)[Architecture](https://nextjs.org/docs/architecture)Next.js Compiler

# Next.js Compiler

Last updated  May 19, 2025

The Next.js Compiler, written in Rust using [SWC](https://swc.rs/), allows Next.js to transform and minify your JavaScript code for production. This replaces Babel for individual files and Terser for minifying output bundles.

Compilation using the Next.js Compiler is 17x faster than Babel and enabled by default since Next.js version 12. If you have an existing Babel configuration or are using [unsupported features](#unsupported-features), your application will opt-out of the Next.js Compiler and continue using Babel.

## Why SWC?

[SWC](https://swc.rs/) is an extensible Rust-based platform for the next generation of fast developer tools.

SWC can be used for compilation, minification, bundling, and more – and is designed to be extended. It's something you can call to perform code transformations (either built-in or custom). Running those transformations happens through higher-level tools like Next.js.

We chose to build on SWC for a few reasons:

- **Extensibility:** SWC can be used as a Crate inside Next.js, without having to fork the library or workaround design constraints.
- **Performance:** We were able to achieve ~3x faster Fast Refresh and ~5x faster builds in Next.js by switching to SWC, with more room for optimization still in progress.
- **WebAssembly:** Rust's support for WASM is essential for supporting all possible platforms and taking Next.js development everywhere.
- **Community:** The Rust community and ecosystem are amazing and still growing.

## Supported Features

### Styled Components

We're working to port `babel-plugin-styled-components` to the Next.js Compiler.

First, update to the latest version of Next.js: `npm install next@latest`. Then, update your `next.config.js` file:

 next.config.js

```
module.exports = {
  compiler: {
    styledComponents: true,
  },
}
```

For advanced use cases, you can configure individual properties for styled-components compilation.

> Note: `ssr` and `displayName` transforms are the main requirement for using `styled-components` in Next.js.

 next.config.js

```
module.exports = {
  compiler: {
    // see https://styled-components.com/docs/tooling#babel-plugin for more info on the options.
    styledComponents: {
      // Enabled by default in development, disabled in production to reduce file size,
      // setting this will override the default for all environments.
      displayName?: boolean,
      // Enabled by default.
      ssr?: boolean,
      // Enabled by default.
      fileName?: boolean,
      // Empty by default.
      topLevelImportPaths?: string[],
      // Defaults to ["index"].
      meaninglessFileNames?: string[],
      // Enabled by default.
      minify?: boolean,
      // Enabled by default.
      transpileTemplateLiterals?: boolean,
      // Empty by default.
      namespace?: string,
      // Disabled by default.
      pure?: boolean,
      // Enabled by default.
      cssProp?: boolean,
    },
  },
}
```

### Jest

The Next.js Compiler transpiles your tests and simplifies configuring Jest together with Next.js including:

- Auto mocking of `.css`, `.module.css` (and their `.scss` variants), and image imports
- Automatically sets up `transform` using SWC
- Loading `.env` (and all variants) into `process.env`
- Ignores `node_modules` from test resolving and transforms
- Ignoring `.next` from test resolving
- Loads `next.config.js` for flags that enable experimental SWC transforms

First, update to the latest version of Next.js: `npm install next@latest`. Then, update your `jest.config.js` file:

 jest.config.js

```
const nextJest = require('next/jest')

// Providing the path to your Next.js app which will enable loading next.config.js and .env files
const createJestConfig = nextJest({ dir: './' })

// Any custom config you want to pass to Jest
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
}

// createJestConfig is exported in this way to ensure that next/jest can load the Next.js configuration, which is async
module.exports = createJestConfig(customJestConfig)
```

### Relay

To enable [Relay](https://relay.dev/) support:

 next.config.js

```
module.exports = {
  compiler: {
    relay: {
      // This should match relay.config.js
      src: './',
      artifactDirectory: './__generated__',
      language: 'typescript',
      eagerEsModules: false,
    },
  },
}
```

> **Good to know**: In Next.js, all JavaScript files in `pages` directory are considered routes. So, for `relay-compiler` you'll need to specify `artifactDirectory` configuration settings outside of the `pages`, otherwise `relay-compiler` will generate files next to the source file in the `__generated__` directory, and this file will be considered a route, which will break production builds.

### Remove React Properties

Allows to remove JSX properties. This is often used for testing. Similar to `babel-plugin-react-remove-properties`.

To remove properties matching the default regex `^data-test`:

 next.config.js

```
module.exports = {
  compiler: {
    reactRemoveProperties: true,
  },
}
```

To remove custom properties:

 next.config.js

```
module.exports = {
  compiler: {
    // The regexes defined here are processed in Rust so the syntax is different from
    // JavaScript `RegExp`s. See https://docs.rs/regex.
    reactRemoveProperties: { properties: ['^data-custom$'] },
  },
}
```

### Remove Console

This transform allows for removing all `console.*` calls in application code (not `node_modules`). Similar to `babel-plugin-transform-remove-console`.

Remove all `console.*` calls:

 next.config.js

```
module.exports = {
  compiler: {
    removeConsole: true,
  },
}
```

Remove `console.*` output except `console.error`:

 next.config.js

```
module.exports = {
  compiler: {
    removeConsole: {
      exclude: ['error'],
    },
  },
}
```

### Legacy Decorators

Next.js will automatically detect `experimentalDecorators` in `jsconfig.json` or `tsconfig.json`. Legacy decorators are commonly used with older versions of libraries like `mobx`.

This flag is only supported for compatibility with existing applications. We do not recommend using legacy decorators in new applications.

First, update to the latest version of Next.js: `npm install next@latest`. Then, update your `jsconfig.json` or `tsconfig.json` file:

```
{
  "compilerOptions": {
    "experimentalDecorators": true
  }
}
```

### importSource

Next.js will automatically detect `jsxImportSource` in `jsconfig.json` or `tsconfig.json` and apply that. This is commonly used with libraries like [Theme UI](https://theme-ui.com).

First, update to the latest version of Next.js: `npm install next@latest`. Then, update your `jsconfig.json` or `tsconfig.json` file:

```
{
  "compilerOptions": {
    "jsxImportSource": "theme-ui"
  }
}
```

### Emotion

We're working to port `@emotion/babel-plugin` to the Next.js Compiler.

First, update to the latest version of Next.js: `npm install next@latest`. Then, update your `next.config.js` file:

 next.config.js

```
module.exports = {
  compiler: {
    emotion: boolean | {
      // default is true. It will be disabled when build type is production.
      sourceMap?: boolean,
      // default is 'dev-only'.
      autoLabel?: 'never' | 'dev-only' | 'always',
      // default is '[local]'.
      // Allowed values: `[local]` `[filename]` and `[dirname]`
      // This option only works when autoLabel is set to 'dev-only' or 'always'.
      // It allows you to define the format of the resulting label.
      // The format is defined via string where variable parts are enclosed in square brackets [].
      // For example labelFormat: "my-classname--[local]", where [local] will be replaced with the name of the variable the result is assigned to.
      labelFormat?: string,
      // default is undefined.
      // This option allows you to tell the compiler what imports it should
      // look at to determine what it should transform so if you re-export
      // Emotion's exports, you can still use transforms.
      importMap?: {
        [packageName: string]: {
          [exportName: string]: {
            canonicalImport?: [string, string],
            styledBaseImport?: [string, string],
          }
        }
      },
    },
  },
}
```

### Minification

Next.js' swc compiler is used for minification by default since v13. This is 7x faster than Terser.

> **Good to know:** Starting with v15, minification cannot be customized using `next.config.js`. Support for the `swcMinify` flag has been removed.

### Module Transpilation

Next.js can automatically transpile and bundle dependencies from local packages (like monorepos) or from external dependencies (`node_modules`). This replaces the `next-transpile-modules` package.

 next.config.js

```
module.exports = {
  transpilePackages: ['@acme/ui', 'lodash-es'],
}
```

### Modularize Imports

This option has been superseded by [optimizePackageImports](https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports) in Next.js 13.5. We recommend upgrading to use the new option that does not require manual configuration of import paths.

### Define (Replacing variables during build)

The `define` option allows you to statically replace variables in your code at build-time.
The option takes an object as key-value pairs, where the keys are the variables that should be replaced with the corresponding values.

Use the `compiler.define` field in `next.config.js` to define variables for all environments (server, edge, and client). Or, use `compiler.defineServer` to define variables only for server-side (server and edge) code:

 next.config.js

```
module.exports = {
  compiler: {
    define: {
      MY_VARIABLE: 'my-string',
      'process.env.MY_ENV_VAR': 'my-env-var',
    },
    defineServer: {
      MY_SERVER_VARIABLE: 'my-server-var',
    },
  },
}
```

### Build Lifecycle Hooks

The Next.js Compiler supports lifecycle hooks that allow you to run custom code at specific points during the build process. Currently, the following hook is supported:

#### runAfterProductionCompile

A hook function that executes after production build compilation finishes, but before running post-compilation tasks such as type checking and static page generation. This hook provides access to project metadata including the project directory and build output directory, making it useful for third-party tools to collect build outputs like sourcemaps.

 next.config.js

```
module.exports = {
  compiler: {
    runAfterProductionCompile: async ({ distDir, projectDir }) => {
      // Your custom code here
    },
  },
}
```

The hook receives an object with the following properties:

- `distDir`: The build output directory (defaults to `.next`)
- `projectDir`: The root directory of the project

## Experimental Features

### SWC Trace profiling

You can generate SWC's internal transform traces as chromium's [trace event format](https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/preview?mode=html#%21=).

 next.config.js

```
module.exports = {
  experimental: {
    swcTraceProfiling: true,
  },
}
```

Once enabled, swc will generate trace named as `swc-trace-profile-${timestamp}.json` under `.next/`. Chromium's trace viewer (chrome://tracing/, [https://ui.perfetto.dev/](https://ui.perfetto.dev/)), or compatible flamegraph viewer ([https://www.speedscope.app/](https://www.speedscope.app/)) can load & visualize generated traces.

### SWC Plugins (experimental)

You can configure swc's transform to use SWC's experimental plugin support written in wasm to customize transformation behavior.

 next.config.js

```
module.exports = {
  experimental: {
    swcPlugins: [
      [
        'plugin',
        {
          ...pluginOptions,
        },
      ],
    ],
  },
}
```

`swcPlugins` accepts an array of tuples for configuring plugins. A tuple for the plugin contains the path to the plugin and an object for plugin configuration. The path to the plugin can be an npm module package name or an absolute path to the `.wasm` binary itself.

## Unsupported Features

When your application has a `.babelrc` file, Next.js will automatically fall back to using Babel for transforming individual files. This ensures backwards compatibility with existing applications that leverage custom Babel plugins.

If you're using a custom Babel setup, [please share your configuration](https://github.com/vercel/next.js/discussions/30174). We're working to port as many commonly used Babel transformations as possible, as well as supporting plugins in the future.

## Version History

| Version | Changes |
| --- | --- |
| v13.1.0 | Module TranspilationandModularize Importsstable. |
| v13.0.0 | SWC Minifier enabled by default. |
| v12.3.0 | SWC Minifierstable. |
| v12.2.0 | SWC Pluginsexperimental support added. |
| v12.1.0 | Added support for Styled Components, Jest, Relay, Remove React Properties, Legacy Decorators, Remove Console, and jsxImportSource. |
| v12.0.0 | Next.js Compilerintroduced. |

Was this helpful?

supported.

---

# Supported Browsers

> Browser support and which JavaScript features are supported by Next.js.

[Next.js Docs](https://nextjs.org/docs)[Architecture](https://nextjs.org/docs/architecture)Supported Browsers

# Supported Browsers

Last updated  October 1, 2025

Next.js supports **modern browsers** with zero configuration.

- Chrome 111+
- Edge 111+
- Firefox 111+
- Safari 16.4+

## Browserslist

If you would like to target specific browsers or features, Next.js supports [Browserslist](https://browsersl.ist) configuration in your `package.json` file. Next.js uses the following Browserslist configuration by default:

 package.json

```
{
  "browserslist": ["chrome 111", "edge 111", "firefox 111", "safari 16.4"]
}
```

## Polyfills

We inject [widely used polyfills](https://github.com/vercel/next.js/blob/canary/packages/next-polyfill-nomodule/src/index.js), including:

- [fetch()](https://developer.mozilla.org/docs/Web/API/Fetch_API) — Replacing: `whatwg-fetch` and `unfetch`.
- [URL](https://developer.mozilla.org/docs/Web/API/URL) — Replacing: the [urlpackage (Node.js API)](https://nodejs.org/api/url.html).
- [Object.assign()](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/assign) — Replacing: `object-assign`, `object.assign`, and `core-js/object/assign`.

If any of your dependencies include these polyfills, they’ll be eliminated automatically from the production build to avoid duplication.

In addition, to reduce bundle size, Next.js will only load these polyfills for browsers that require them. The majority of the web traffic globally will not download these polyfills.

### Custom Polyfills

If your own code or any external npm dependencies require features not supported by your target browsers (such as IE 11), you need to add polyfills yourself.

#### In App Router

To include polyfills, you can import them into the [instrumentation-client.jsfile](https://nextjs.org/docs/app/api-reference/file-conventions/instrumentation-client).

 instrumentation-client.ts

```
import './polyfills'
```

#### In Pages Router

In this case, you should add a top-level import for the **specific polyfill** you need in your [Custom<App>](https://nextjs.org/docs/pages/building-your-application/routing/custom-app) or the individual component.

 pages/_app.tsxJavaScriptTypeScript

```
import './polyfills'

import type { AppProps } from 'next/app'

export default function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
```

#### Conditionally loading polyfills

The best approach is to isolate unsupported features to specific UI sections and conditionally load the polyfill if needed.

 hooks/analytics.tsJavaScriptTypeScript

```
import { useCallback } from 'react'

export const useAnalytics = () => {
  const tracker = useCallback(async (data: unknown) => {
    if (!('structuredClone' in globalThis)) {
      import('polyfills/structured-clone').then((mod) => {
        globalThis.structuredClone = mod.default
      })
    }

    /* Do some work that uses structured clone */
  }, [])

  return tracker
}
```

## JavaScript Language Features

Next.js allows you to use the latest JavaScript features out of the box. In addition to [ES6 features](https://github.com/lukehoban/es6features), Next.js also supports:

- [Async/await](https://github.com/tc39/ecmascript-asyncawait) (ES2017)
- [Object Rest/Spread Properties](https://github.com/tc39/proposal-object-rest-spread) (ES2018)
- [Dynamicimport()](https://github.com/tc39/proposal-dynamic-import) (ES2020)
- [Optional Chaining](https://github.com/tc39/proposal-optional-chaining) (ES2020)
- [Nullish Coalescing](https://github.com/tc39/proposal-nullish-coalescing) (ES2020)
- [Class Fields](https://github.com/tc39/proposal-class-fields) and [Static Properties](https://github.com/tc39/proposal-static-class-features) (ES2022)
- and more!

### TypeScript Features

Next.js has built-in TypeScript support. [Learn more here](https://nextjs.org/docs/pages/api-reference/config/typescript).

### Customizing Babel Config (Advanced)

You can customize babel configuration. [Learn more here](https://nextjs.org/docs/pages/guides/babel).

Was this helpful?

supported.
