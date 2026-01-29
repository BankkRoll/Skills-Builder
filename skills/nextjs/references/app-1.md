# create and more

# create

> Create Next.js apps using one command with the create-next-app CLI.

[API Reference](https://nextjs.org/docs/app/api-reference)[CLI](https://nextjs.org/docs/app/api-reference/cli)create-next-app

# create-next-app

Last updated  October 28, 2025

The `create-next-app` CLI allow you to create a new Next.js application using the default template or an [example](https://github.com/vercel/next.js/tree/canary/examples) from a public GitHub repository. It is the easiest way to get started with Next.js.

Basic usage:

 Terminal

```
npx create-next-app@latest [project-name] [options]
```

## Reference

The following options are available:

| Options | Description |
| --- | --- |
| -hor--help | Show all available options |
| -vor--version | Output the version number |
| --no-* | Negate default options. E.g.--no-ts |
| --tsor--typescript | Initialize as a TypeScript project (default) |
| --jsor--javascript | Initialize as a JavaScript project |
| --tailwind | Initialize with Tailwind CSS config (default) |
| --react-compiler | Initialize with React Compiler enabled |
| --eslint | Initialize with ESLint config |
| --biome | Initialize with Biome config |
| --no-linter | Skip linter configuration |
| --app | Initialize as an App Router project |
| --api | Initialize a project with only route handlers |
| --src-dir | Initialize inside asrc/directory |
| --turbopack | Force enable Turbopack in generated package.json (enabled by default) |
| --webpack | Force enable Webpack in generated package.json |
| --import-alias <alias-to-configure> | Specify import alias to use (default "@/*") |
| --empty | Initialize an empty project |
| --use-npm | Explicitly tell the CLI to bootstrap the application using npm |
| --use-pnpm | Explicitly tell the CLI to bootstrap the application using pnpm |
| --use-yarn | Explicitly tell the CLI to bootstrap the application using Yarn |
| --use-bun | Explicitly tell the CLI to bootstrap the application using Bun |
| -eor--example [name] [github-url] | An example to bootstrap the app with |
| --example-path <path-to-example> | Specify the path to the example separately |
| --reset-preferences | Explicitly tell the CLI to reset any stored preferences |
| --skip-install | Explicitly tell the CLI to skip installing packages |
| --disable-git | Explicitly tell the CLI to disable git initialization |
| --yes | Use previous preferences or defaults for all options |

## Examples

### With the default template

To create a new app using the default template, run the following command in your terminal:

 Terminal

```
npx create-next-app@latest
```

On installation, you'll see the following prompts:

 Terminal

```
What is your project named? my-app
Would you like to use the recommended Next.js defaults?
    Yes, use recommended defaults - TypeScript, ESLint, Tailwind CSS, App Router, Turbopack
    No, reuse previous settings
    No, customize settings - Choose your own preferences
```

If you choose to `customize settings`, you'll see the following prompts:

 Terminal

```
Would you like to use TypeScript? No / Yes
Which linter would you like to use? ESLint / Biome / None
Would you like to use React Compiler? No / Yes
Would you like to use Tailwind CSS? No / Yes
Would you like your code inside a `src/` directory? No / Yes
Would you like to use App Router? (recommended) No / Yes
Would you like to customize the import alias (`@/*` by default)? No / Yes
What import alias would you like configured? @/*
```

After the prompts, `create-next-app` will create a folder with your project name and install the required dependencies.

### Linter Options

**ESLint**: The traditional and most popular JavaScript linter. Includes Next.js-specific rules from `@next/eslint-plugin-next`.

**Biome**: A fast, modern linter and formatter that combines the functionality of ESLint and Prettier. Includes built-in Next.js and React domain support for optimal performance.

**None**: Skip linter configuration entirely. You can always add a linter later.

Once you've answered the prompts, a new project will be created with your chosen configuration.

### With an official Next.js example

To create a new app using an official Next.js example, use the `--example` flag. For example:

 Terminal

```
npx create-next-app@latest --example [example-name] [your-project-name]
```

You can view a list of all available examples along with setup instructions in the [Next.js repository](https://github.com/vercel/next.js/tree/canary/examples).

### With any public GitHub example

To create a new app using any public GitHub example, use the `--example` option with the GitHub repo's URL. For example:

 Terminal

```
npx create-next-app@latest --example "https://github.com/.../" [your-project-name]
```

Was this helpful?

supported.

---

# next CLI

> Learn how to run and build your application with the Next.js CLI.

[API Reference](https://nextjs.org/docs/app/api-reference)[CLI](https://nextjs.org/docs/app/api-reference/cli)next CLI

# next CLI

Last updated  January 7, 2026

The Next.js CLI allows you to develop, build, start your application, and more.

Basic usage:

 Terminal

```
npx next [command] [options]
```

## Reference

The following options are available:

| Options | Description |
| --- | --- |
| -hor--help | Shows all available options |
| -vor--version | Outputs the Next.js version number |

### Commands

The following commands are available:

| Command | Description |
| --- | --- |
| dev | Starts Next.js in development mode with Hot Module Reloading, error reporting, and more. |
| build | Creates an optimized production build of your application. Displaying information about each route. |
| start | Starts Next.js in production mode. The application should be compiled withnext buildfirst. |
| info | Prints relevant details about the current system which can be used to report Next.js bugs. |
| telemetry | Allows you to enable or disable Next.js' completely anonymous telemetry collection. |
| typegen | Generates TypeScript definitions for routes, pages, layouts, and route handlers without running a full build. |
| upgrade | Upgrades your Next.js application to the latest version. |
| experimental-analyze | Analyzes bundle output using Turbopack. Does not produce build artifacts. |

> **Good to know**: Running `next` without a command is an alias for `next dev`.

### next devoptions

`next dev` starts the application in development mode with Hot Module Reloading (HMR), error reporting, and more. The following options are available when running `next dev`:

| Option | Description |
| --- | --- |
| -h, --help | Show all available options. |
| [directory] | A directory in which to build the application. If not provided, current directory is used. |
| --turbopack | Force enableTurbopack(enabled by default). Also available as--turbo. |
| --webpack | Use Webpack instead of the defaultTurbopackbundler for development. |
| -por--port <port> | Specify a port number on which to start the application. Default: 3000, env: PORT |
| -Hor--hostname <hostname> | Specify a hostname on which to start the application. Useful for making the application available for other devices on the network. Default: 0.0.0.0 |
| --experimental-https | Starts the server with HTTPS and generates a self-signed certificate. |
| --experimental-https-key <path> | Path to a HTTPS key file. |
| --experimental-https-cert <path> | Path to a HTTPS certificate file. |
| --experimental-https-ca <path> | Path to a HTTPS certificate authority file. |
| --experimental-upload-trace <traceUrl> | Reports a subset of the debugging trace to a remote HTTP URL. |

### next buildoptions

`next build` creates an optimized production build of your application. The output displays information about each route. For example:

 Terminal

```
Route (app)
┌ ○ /_not-found
└ ƒ /products/[id]

○  (Static)   prerendered as static content
ƒ  (Dynamic)  server-rendered on demand
```

The following options are available for the `next build` command:

| Option | Description |
| --- | --- |
| -h, --help | Show all available options. |
| [directory] | A directory on which to build the application. If not provided, the current directory will be used. |
| --turbopack | Force enableTurbopack(enabled by default). Also available as--turbo. |
| --webpack | Build using Webpack. |
| -dor--debug | Enables a more verbose build output. With this flag enabled additional build output like rewrites, redirects, and headers will be shown. |
|  |  |
| --profile | Enables productionprofiling for React. |
| --no-lint | Disables linting.Note: linting will be removed fromnext buildin Next 16. If you're using Next 15.5+ with a linter other thaneslint, linting during build will not occur. |
| --no-mangling | Disablesmangling. This may affect performance and should only be used for debugging purposes. |
| --experimental-app-only | Builds only App Router routes. |
| --experimental-build-mode [mode] | Uses an experimental build mode. (choices: "compile", "generate", default: "default") |
| --debug-prerender | Debug prerender errors in development. |
| --debug-build-paths=<patterns> | Build only specific routes for debugging. |

### next startoptions

`next start` starts the application in production mode. The application should be compiled with [next build](#next-build-options) first.

The following options are available for the `next start` command:

| Option | Description |
| --- | --- |
| -hor--help | Show all available options. |
| [directory] | A directory on which to start the application. If no directory is provided, the current directory will be used. |
| -por--port <port> | Specify a port number on which to start the application. (default: 3000, env: PORT) |
| -Hor--hostname <hostname> | Specify a hostname on which to start the application (default: 0.0.0.0). |
| --keepAliveTimeout <keepAliveTimeout> | Specify the maximum amount of milliseconds to wait before closing the inactive connections. |

### next infooptions

`next info` prints relevant details about the current system which can be used to report Next.js bugs when opening a [GitHub issue](https://github.com/vercel/next.js/issues). This information includes Operating System platform/arch/version, Binaries (Node.js, npm, Yarn, pnpm), package versions (`next`, `react`, `react-dom`), and more.

The output should look like this:

 Terminal

```
Operating System:
  Platform: darwin
  Arch: arm64
  Version: Darwin Kernel Version 23.6.0
  Available memory (MB): 65536
  Available CPU cores: 10
Binaries:
  Node: 20.12.0
  npm: 10.5.0
  Yarn: 1.22.19
  pnpm: 9.6.0
Relevant Packages:
  next: 15.0.0-canary.115 // Latest available version is detected (15.0.0-canary.115).
  eslint-config-next: 14.2.5
  react: 19.0.0-rc
  react-dom: 19.0.0
  typescript: 5.5.4
Next.js Config:
  output: N/A
```

The following options are available for the `next info` command:

| Option | Description |
| --- | --- |
| -hor--help | Show all available options |
| --verbose | Collects additional information for debugging. |

### next telemetryoptions

Next.js collects **completely anonymous** telemetry data about general usage. Participation in this anonymous program is optional, and you can opt-out if you prefer not to share information.

The following options are available for the `next telemetry` command:

| Option | Description |
| --- | --- |
| -h, --help | Show all available options. |
| --enable | Enables Next.js' telemetry collection. |
| --disable | Disables Next.js' telemetry collection. |

Learn more about [Telemetry](https://nextjs.org/telemetry).

### next typegenoptions

`next typegen` generates TypeScript definitions for your application's routes without performing a full build. This is useful for IDE autocomplete and CI type-checking of route usage.

Previously, route types were only generated during `next dev` or `next build`, which meant running `tsc --noEmit` directly wouldn't validate your route types. Now you can generate types independently and validate them externally:

 Terminal

```
# Generate route types first, then validate with TypeScript
next typegen && tsc --noEmit

# Or in CI workflows for type checking without building
next typegen && npm run type-check
```

The following options are available for the `next typegen` command:

| Option | Description |
| --- | --- |
| -h, --help | Show all available options. |
| [directory] | A directory on which to generate types. If not provided, the current directory will be used. |

Output files are written to `<distDir>/types` (typically: `.next/dev/types` or `.next/types`, see [isolatedDevBuild](https://nextjs.org/docs/app/api-reference/config/next-config-js/isolatedDevBuild)):

 Terminal

```
next typegen
# or for a specific app
next typegen ./apps/web
```

Additionally, `next typegen` generates a `next-env.d.ts` file. We recommend adding `next-env.d.ts` to your `.gitignore` file.

The `next-env.d.ts` file is included into your `tsconfig.json` file, to make Next.js types available to your project.

To ensure `next-env.d.ts` is present before type-checking run `next typegen`. The commands `next dev` and `next build` also generate the `next-env.d.ts` file, but it is often undesirable to run these just to type-check, for example in CI/CD environments.

> **Good to know**: `next typegen` loads your Next.js config (`next.config.js`, `next.config.mjs`, or `next.config.ts`) using the production build phase. Ensure any required environment variables and dependencies are available so the config can load correctly.

### next upgradeoptions

`next upgrade` upgrades your Next.js application to the latest version.

The following options are available for the `next upgrade` command:

| Option | Description |
| --- | --- |
| -h, --help | Show all available options. |
| [directory] | A directory with the Next.js application to upgrade. If not provided, the current directory will be used. |
| --revision <revision> | Specify a Next.js version or tag to upgrade to (e.g.,latest,canary,15.0.0). Defaults to the release channel you have currently installed. |
| --verbose | Show verbose output during the upgrade process. |

### next experimental-analyzeoptions

`next experimental-analyze` analyzes your application's bundle output using [Turbopack](https://nextjs.org/docs/app/api-reference/turbopack). This command helps you understand the size and composition of your bundles, including JavaScript, CSS, and other assets. This command doesn't produce an application build.

 Terminal

```
npx next experimental-analyze
```

By default, the command starts a local server after analysis completes, allowing you to explore your bundle composition in the browser. The analyzer lets you:

- Filter bundles by route and switch between client and server views
- View the full import chain showing why a module is included
- Trace imports across server-to-client component boundaries and dynamic imports

See [Package Bundling](https://nextjs.org/docs/app/guides/package-bundling#optimizing-large-bundles) for optimization strategies.

To write the analysis output to disk without starting the server, use the `--output` flag. The output is written to `.next/diagnostics/analyze` and contains static files that can be copied elsewhere or shared with others:

 Terminal

```
# Write output to .next/diagnostics/analyze
npx next experimental-analyze --output

# Copy the output for comparison with a future analysis
cp -r .next/diagnostics/analyze ./analyze-before-refactor
```

The following options are available for the `next experimental-analyze` command:

| Option | Description |
| --- | --- |
| -h, --help | Show all available options. |
| [directory] | A directory on which to analyze the application. If not provided, the current directory will be used. |
| --no-mangling | Disablesmangling. This may affect performance and should only be used for debugging purposes. |
| --profile | Enables productionprofiling for React. This may affect performance. |
| -o, --output | Write analysis files to disk without starting the server. Output is written to.next/diagnostics/analyze. |
| --port <port> | Specify a port number to serve the analyzer on. (default: 4000, env: PORT) |

## Examples

### Debugging prerender errors

If you encounter prerendering errors during `next build`, you can pass the `--debug-prerender` flag to get more detailed output:

 Terminal

```
next build --debug-prerender
```

This enables several experimental options to make debugging easier:

- Disables server code minification:
  - `experimental.serverMinification = false`
  - `experimental.turbopackMinify = false`
- Generates source maps for server bundles:
  - `experimental.serverSourceMaps = true`
- Enables source map consumption in child processes used for prerendering:
  - `enablePrerenderSourceMaps = true`
- Continues building even after the first prerender error, so you can see all issues at once:
  - `experimental.prerenderEarlyExit = false`

This helps surface more readable stack traces and code frames in the build output.

> **Warning**: `--debug-prerender` is for debugging in development only. Do not deploy builds generated with `--debug-prerender` to production, as it may impact performance.

### Building specific routes

You can build only specific routes in the App and Pages Routers using the `--debug-build-paths` option. This is useful for faster debugging when working with large applications. The `--debug-build-paths` option accepts comma-separated file paths and supports glob patterns:

 Terminal

```
# Build a specific route
next build --debug-build-paths="app/page.tsx"

# Build more than one route
next build --debug-build-paths="app/page.tsx,pages/index.tsx"

# Use glob patterns
next build --debug-build-paths="app/**/page.tsx"
next build --debug-build-paths="pages/*.tsx"
```

### Changing the default port

By default, Next.js uses `http://localhost:3000` during development and with `next start`. The default port can be changed with the `-p` option, like so:

 Terminal

```
next dev -p 4000
```

Or using the `PORT` environment variable:

 Terminal

```
PORT=4000 next dev
```

> **Good to know**: `PORT` cannot be set in `.env` as booting up the HTTP server happens before any other code is initialized.

### Using HTTPS during development

For certain use cases like webhooks or authentication, you can use [HTTPS](https://developer.mozilla.org/en-US/docs/Glossary/HTTPS) to have a secure environment on `localhost`. Next.js can generate a self-signed certificate with `next dev` using the `--experimental-https` flag:

 Terminal

```
next dev --experimental-https
```

With the generated certificate, the Next.js development server will exist at `https://localhost:3000`. The default port `3000` is used unless a port is specified with `-p`, `--port`, or `PORT`.

You can also provide a custom certificate and key with `--experimental-https-key` and `--experimental-https-cert`. Optionally, you can provide a custom CA certificate with `--experimental-https-ca` as well.

 Terminal

```
next dev --experimental-https --experimental-https-key ./certificates/localhost-key.pem --experimental-https-cert ./certificates/localhost.pem
```

`next dev --experimental-https` is only intended for development and creates a locally trusted certificate with [mkcert](https://github.com/FiloSottile/mkcert). In production, use properly issued certificates from trusted authorities.

### Configuring a timeout for downstream proxies

When deploying Next.js behind a downstream proxy (e.g. a load-balancer like AWS ELB/ALB), it's important to configure Next's underlying HTTP server with [keep-alive timeouts](https://nodejs.org/api/http.html#http_server_keepalivetimeout) that are *larger* than the downstream proxy's timeouts. Otherwise, once a keep-alive timeout is reached for a given TCP connection, Node.js will immediately terminate that connection without notifying the downstream proxy. This results in a proxy error whenever it attempts to reuse a connection that Node.js has already terminated.

To configure the timeout values for the production Next.js server, pass `--keepAliveTimeout` (in milliseconds) to `next start`, like so:

 Terminal

```
next start --keepAliveTimeout 70000
```

### Passing Node.js arguments

You can pass any [node arguments](https://nodejs.org/api/cli.html#cli_node_options_options) to `next` commands. For example:

 Terminal

```
NODE_OPTIONS='--throw-deprecation' next
NODE_OPTIONS='-r esm' next
NODE_OPTIONS='--inspect' next
```

| Version | Changes |
| --- | --- |
| v16.1.0 | Add thenext experimental-analyzecommand |
| v16.0.0 | The JS bundle size metrics have been removed fromnext build |
| v15.5.0 | Add thenext typegencommand |
| v15.4.0 | Add--debug-prerenderoption fornext buildto help debug prerender errors. |

Was this helpful?

supported.

---

# CLI

> API Reference for the Next.js Command Line Interface (CLI) tools.

[App Router](https://nextjs.org/docs/app)[API Reference](https://nextjs.org/docs/app/api-reference)CLI

# CLI

Last updated  June 16, 2025

Next.js comes with **two** Command Line Interface (CLI) tools:

- **create-next-app**: Quickly create a new Next.js application using the default template or an [example](https://github.com/vercel/next.js/tree/canary/examples) from a public GitHub repository.
- **next**: Run the Next.js development server, build your application, and more.

[create-next-appCreate Next.js apps using one command with the create-next-app CLI.](https://nextjs.org/docs/app/api-reference/cli/create-next-app)[next CLILearn how to run and build your application with the Next.js CLI.](https://nextjs.org/docs/app/api-reference/cli/next)

Was this helpful?

supported.

---

# Font Module

> Optimizing loading web fonts with the built-in `next/font` loaders.

[API Reference](https://nextjs.org/docs/app/api-reference)[Components](https://nextjs.org/docs/app/api-reference/components)Font

# Font Module

Last updated  August 6, 2025

[next/font](https://nextjs.org/docs/app/api-reference/components/font) automatically optimizes your fonts (including custom fonts) and removes external network requests for improved privacy and performance.

It includes **built-in automatic self-hosting** for any font file. This means you can optimally load web fonts with no [layout shift](https://web.dev/articles/cls).

You can also conveniently use all [Google Fonts](https://fonts.google.com/). CSS and font files are downloaded at build time and self-hosted with the rest of your static assets. **No requests are sent to Google by the browser.**

 app/layout.tsxJavaScriptTypeScript

```
import { Inter } from 'next/font/google'

// If loading a variable font, you don't need to specify the font weight
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

> **🎥 Watch:** Learn more about using `next/font` → [YouTube (6 minutes)](https://www.youtube.com/watch?v=L8_98i_bMMA).

## Reference

| Key | font/google | font/local | Type | Required |
| --- | --- | --- | --- | --- |
| src |  |  | String or Array of Objects | Yes |
| weight |  |  | String or Array | Required/Optional |
| style |  |  | String or Array | - |
| subsets |  |  | Array of Strings | - |
| axes |  |  | Array of Strings | - |
| display |  |  | String | - |
| preload |  |  | Boolean | - |
| fallback |  |  | Array of Strings | - |
| adjustFontFallback |  |  | Boolean or String | - |
| variable |  |  | String | - |
| declarations |  |  | Array of Objects | - |

### src

The path of the font file as a string or an array of objects (with type `Array<{path: string, weight?: string, style?: string}>`) relative to the directory where the font loader function is called.

Used in `next/font/local`

- Required

Examples:

- `src:'./fonts/my-font.woff2'` where `my-font.woff2` is placed in a directory named `fonts` inside the `app` directory
- `src:[{path: './inter/Inter-Thin.ttf', weight: '100',},{path: './inter/Inter-Regular.ttf',weight: '400',},{path: './inter/Inter-Bold-Italic.ttf', weight: '700',style: 'italic',},]`
- if the font loader function is called in `app/page.tsx` using `src:'../styles/fonts/my-font.ttf'`, then `my-font.ttf` is placed in `styles/fonts` at the root of the project

### weight

The font [weight](https://fonts.google.com/knowledge/glossary/weight) with the following possibilities:

- A string with possible values of the weights available for the specific font or a range of values if it's a [variable](https://fonts.google.com/variablefonts) font
- An array of weight values if the font is not a [variable google font](https://fonts.google.com/variablefonts). It applies to `next/font/google` only.

Used in `next/font/google` and `next/font/local`

- Required if the font being used is **not** [variable](https://fonts.google.com/variablefonts)

Examples:

- `weight: '400'`: A string for a single weight value - for the font [Inter](https://fonts.google.com/specimen/Inter?query=inter), the possible values are `'100'`, `'200'`, `'300'`, `'400'`, `'500'`, `'600'`, `'700'`, `'800'`, `'900'` or `'variable'` where `'variable'` is the default)
- `weight: '100 900'`: A string for the range between `100` and `900` for a variable font
- `weight: ['100','400','900']`: An array of 3 possible values for a non variable font

### style

The font [style](https://developer.mozilla.org/docs/Web/CSS/font-style) with the following possibilities:

- A string [value](https://developer.mozilla.org/docs/Web/CSS/font-style#values) with default value of `'normal'`
- An array of style values if the font is not a [variable google font](https://fonts.google.com/variablefonts). It applies to `next/font/google` only.

Used in `next/font/google` and `next/font/local`

- Optional

Examples:

- `style: 'italic'`: A string - it can be `normal` or `italic` for `next/font/google`
- `style: 'oblique'`: A string - it can take any value for `next/font/local` but is expected to come from [standard font styles](https://developer.mozilla.org/docs/Web/CSS/font-style)
- `style: ['italic','normal']`: An array of 2 values for `next/font/google` - the values are from `normal` and `italic`

### subsets

The font [subsets](https://fonts.google.com/knowledge/glossary/subsetting) defined by an array of string values with the names of each subset you would like to be [preloaded](https://nextjs.org/docs/app/api-reference/components/font#specifying-a-subset). Fonts specified via `subsets` will have a link preload tag injected into the head when the [preload](#preload) option is true, which is the default.

Used in `next/font/google`

- Optional

Examples:

- `subsets: ['latin']`: An array with the subset `latin`

You can find a list of all subsets on the Google Fonts page for your font.

### axes

Some variable fonts have extra `axes` that can be included. By default, only the font weight is included to keep the file size down. The possible values of `axes` depend on the specific font.

Used in `next/font/google`

- Optional

Examples:

- `axes: ['slnt']`: An array with value `slnt` for the `Inter` variable font which has `slnt` as additional `axes` as shown [here](https://fonts.google.com/variablefonts?vfquery=inter#font-families). You can find the possible `axes` values for your font by using the filter on the [Google variable fonts page](https://fonts.google.com/variablefonts#font-families) and looking for axes other than `wght`

### display

The font [display](https://developer.mozilla.org/docs/Web/CSS/@font-face/font-display) with possible string [values](https://developer.mozilla.org/docs/Web/CSS/@font-face/font-display#values) of `'auto'`, `'block'`, `'swap'`, `'fallback'` or `'optional'` with default value of `'swap'`.

Used in `next/font/google` and `next/font/local`

- Optional

Examples:

- `display: 'optional'`: A string assigned to the `optional` value

### preload

A boolean value that specifies whether the font should be [preloaded](https://nextjs.org/docs/app/api-reference/components/font#preloading) or not. The default is `true`.

Used in `next/font/google` and `next/font/local`

- Optional

Examples:

- `preload: false`

### fallback

The fallback font to use if the font cannot be loaded. An array of strings of fallback fonts with no default.

- Optional

Used in `next/font/google` and `next/font/local`

Examples:

- `fallback: ['system-ui', 'arial']`: An array setting the fallback fonts to `system-ui` or `arial`

### adjustFontFallback

- For `next/font/google`: A boolean value that sets whether an automatic fallback font should be used to reduce [Cumulative Layout Shift](https://web.dev/cls/). The default is `true`.
- For `next/font/local`: A string or boolean `false` value that sets whether an automatic fallback font should be used to reduce [Cumulative Layout Shift](https://web.dev/cls/). The possible values are `'Arial'`, `'Times New Roman'` or `false`. The default is `'Arial'`.

Used in `next/font/google` and `next/font/local`

- Optional

Examples:

- `adjustFontFallback: false`: for `next/font/google`
- `adjustFontFallback: 'Times New Roman'`: for `next/font/local`

### variable

A string value to define the CSS variable name to be used if the style is applied with the [CSS variable method](#css-variables).

Used in `next/font/google` and `next/font/local`

- Optional

Examples:

- `variable: '--my-font'`: The CSS variable `--my-font` is declared

### declarations

An array of font face [descriptor](https://developer.mozilla.org/docs/Web/CSS/@font-face#descriptors) key-value pairs that define the generated `@font-face` further.

Used in `next/font/local`

- Optional

Examples:

- `declarations: [{ prop: 'ascent-override', value: '90%' }]`

## Examples

## Google Fonts

To use a Google font, import it from `next/font/google` as a function. We recommend using [variable fonts](https://fonts.google.com/variablefonts) for the best performance and flexibility.

 app/layout.tsxJavaScriptTypeScript

```
import { Inter } from 'next/font/google'

// If loading a variable font, you don't need to specify the font weight
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

If you can't use a variable font, you will **need to specify a weight**:

app/layout.tsxJavaScriptTypeScript

```
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  weight: '400',
  subsets: ['latin'],
  display: 'swap',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={roboto.className}>
      <body>{children}</body>
    </html>
  )
}
```

You can specify multiple weights and/or styles by using an array:

 app/layout.js

```
const roboto = Roboto({
  weight: ['400', '700'],
  style: ['normal', 'italic'],
  subsets: ['latin'],
  display: 'swap',
})
```

> **Good to know**: Use an underscore (_) for font names with multiple words. E.g. `Roboto Mono` should be imported as `Roboto_Mono`.

### Specifying a subset

Google Fonts are automatically [subset](https://fonts.google.com/knowledge/glossary/subsetting). This reduces the size of the font file and improves performance. You'll need to define which of these subsets you want to preload. Failing to specify any subsets while [preload](https://nextjs.org/docs/app/api-reference/components/font#preload) is `true` will result in a warning.

This can be done by adding it to the function call:

 app/layout.tsxJavaScriptTypeScript

```
const inter = Inter({ subsets: ['latin'] })
```

View the [Font API Reference](https://nextjs.org/docs/app/api-reference/components/font) for more information.

## Using Multiple Fonts

You can import and use multiple fonts in your application. There are two approaches you can take.

The first approach is to create a utility function that exports a font, imports it, and applies its `className` where needed. This ensures the font is preloaded only when it's rendered:

 app/fonts.tsJavaScriptTypeScript

```
import { Inter, Roboto_Mono } from 'next/font/google'

export const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

export const roboto_mono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
})
```

   app/layout.tsxJavaScriptTypeScript

```
import { inter } from './fonts'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>
        <div>{children}</div>
      </body>
    </html>
  )
}
```

app/page.tsxJavaScriptTypeScript

```
import { roboto_mono } from './fonts'

export default function Page() {
  return (
    <>
      <h1 className={roboto_mono.className}>My page</h1>
    </>
  )
}
```

In the example above, `Inter` will be applied globally, and `Roboto Mono` can be imported and applied as needed.

Alternatively, you can create a [CSS variable](https://nextjs.org/docs/app/api-reference/components/font#variable) and use it with your preferred CSS solution:

 app/layout.tsxJavaScriptTypeScript

```
import { Inter, Roboto_Mono } from 'next/font/google'
import styles from './global.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const roboto_mono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
  display: 'swap',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${roboto_mono.variable}`}>
      <body>
        <h1>My App</h1>
        <div>{children}</div>
      </body>
    </html>
  )
}
```

 app/global.css

```
html {
  font-family: var(--font-inter);
}

h1 {
  font-family: var(--font-roboto-mono);
}
```

In the example above, `Inter` will be applied globally, and any `<h1>` tags will be styled with `Roboto Mono`.

> **Recommendation**: Use multiple fonts conservatively since each new font is an additional resource the client has to download.

### Local Fonts

Import `next/font/local` and specify the `src` of your local font file. We recommend using [variable fonts](https://fonts.google.com/variablefonts) for the best performance and flexibility.

 app/layout.tsxJavaScriptTypeScript

```
import localFont from 'next/font/local'

// Font files can be colocated inside of `app`
const myFont = localFont({
  src: './my-font.woff2',
  display: 'swap',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={myFont.className}>
      <body>{children}</body>
    </html>
  )
}
```

If you want to use multiple files for a single font family, `src` can be an array:

```
const roboto = localFont({
  src: [
    {
      path: './Roboto-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: './Roboto-Italic.woff2',
      weight: '400',
      style: 'italic',
    },
    {
      path: './Roboto-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
    {
      path: './Roboto-BoldItalic.woff2',
      weight: '700',
      style: 'italic',
    },
  ],
})
```

View the [Font API Reference](https://nextjs.org/docs/app/api-reference/components/font) for more information.

### With Tailwind CSS

`next/font` integrates seamlessly with [Tailwind CSS](https://tailwindcss.com/) using [CSS variables](https://nextjs.org/docs/app/api-reference/components/font#css-variables).

In the example below, we use the `Inter` and `Roboto_Mono` fonts from `next/font/google` (you can use any Google Font or Local Font). Use the `variable` option to define a CSS variable name, such as `inter` and `roboto_mono` for these fonts, respectively. Then, apply `inter.variable` and `roboto_mono.variable` to include the CSS variables in your HTML document.

> **Good to know**: You can add these variables to the `<html>` or `<body>` tag, depending on your preference, styling needs or project requirements.

 app/layout.tsxJavaScriptTypeScript

```
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const roboto_mono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${roboto_mono.variable} antialiased`}
    >
      <body>{children}</body>
    </html>
  )
}
```

Finally, add the CSS variable to your [Tailwind CSS config](https://nextjs.org/docs/app/getting-started/css#tailwind-css):

 global.css

```
@import 'tailwindcss';

@theme inline {
  --font-sans: var(--font-inter);
  --font-mono: var(--font-roboto-mono);
}
```

### Tailwind CSS v3

 tailwind.config.js

```
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)'],
        mono: ['var(--font-roboto-mono)'],
      },
    },
  },
  plugins: [],
}
```

You can now use the `font-sans` and `font-mono` utility classes to apply the font to your elements.

```
<p class="font-sans ...">The quick brown fox ...</p>
<p class="font-mono ...">The quick brown fox ...</p>
```

### Applying Styles

You can apply the font styles in three ways:

- [className](#classname)
- [style](#style-1)
- [CSS Variables](#css-variables)

#### className

Returns a read-only CSS `className` for the loaded font to be passed to an HTML element.

```
<p className={inter.className}>Hello, Next.js!</p>
```

#### style

Returns a read-only CSS `style` object for the loaded font to be passed to an HTML element, including `style.fontFamily` to access the font family name and fallback fonts.

```
<p style={inter.style}>Hello World</p>
```

#### CSS Variables

If you would like to set your styles in an external style sheet and specify additional options there, use the CSS variable method.

In addition to importing the font, also import the CSS file where the CSS variable is defined and set the variable option of the font loader object as follows:

 app/page.tsxJavaScriptTypeScript

```
import { Inter } from 'next/font/google'
import styles from '../styles/component.module.css'

const inter = Inter({
  variable: '--font-inter',
})
```

To use the font, set the `className` of the parent container of the text you would like to style to the font loader's `variable` value and the `className` of the text to the `styles` property from the external CSS file.

 app/page.tsxJavaScriptTypeScript

```
<main className={inter.variable}>
  <p className={styles.text}>Hello World</p>
</main>
```

Define the `text` selector class in the `component.module.css` CSS file as follows:

 styles/component.module.css

```
.text {
  font-family: var(--font-inter);
  font-weight: 200;
  font-style: italic;
}
```

In the example above, the text `Hello World` is styled using the `Inter` font and the generated font fallback with `font-weight: 200` and `font-style: italic`.

### Using a font definitions file

Every time you call the `localFont` or Google font function, that font will be hosted as one instance in your application. Therefore, if you need to use the same font in multiple places, you should load it in one place and import the related font object where you need it. This is done using a font definitions file.

For example, create a `fonts.ts` file in a `styles` folder at the root of your app directory.

Then, specify your font definitions as follows:

 styles/fonts.tsJavaScriptTypeScript

```
import { Inter, Lora, Source_Sans_3 } from 'next/font/google'
import localFont from 'next/font/local'

// define your variable fonts
const inter = Inter()
const lora = Lora()
// define 2 weights of a non-variable font
const sourceCodePro400 = Source_Sans_3({ weight: '400' })
const sourceCodePro700 = Source_Sans_3({ weight: '700' })
// define a custom local font where GreatVibes-Regular.ttf is stored in the styles folder
const greatVibes = localFont({ src: './GreatVibes-Regular.ttf' })

export { inter, lora, sourceCodePro400, sourceCodePro700, greatVibes }
```

You can now use these definitions in your code as follows:

 app/page.tsxJavaScriptTypeScript

```
import { inter, lora, sourceCodePro700, greatVibes } from '../styles/fonts'

export default function Page() {
  return (
    <div>
      <p className={inter.className}>Hello world using Inter font</p>
      <p style={lora.style}>Hello world using Lora font</p>
      <p className={sourceCodePro700.className}>
        Hello world using Source_Sans_3 font with weight 700
      </p>
      <p className={greatVibes.className}>My title in Great Vibes font</p>
    </div>
  )
}
```

To make it easier to access the font definitions in your code, you can define a path alias in your `tsconfig.json` or `jsconfig.json` files as follows:

 tsconfig.json

```
{
  "compilerOptions": {
    "paths": {
      "@/fonts": ["./styles/fonts"]
    }
  }
}
```

You can now import any font definition as follows:

 app/about/page.tsxJavaScriptTypeScript

```
import { greatVibes, sourceCodePro400 } from '@/fonts'
```

### Preloading

When a font function is called on a page of your site, it is not globally available and preloaded on all routes. Rather, the font is only preloaded on the related routes based on the type of file where it is used:

- If it's a [unique page](https://nextjs.org/docs/app/api-reference/file-conventions/page), it is preloaded on the unique route for that page.
- If it's a [layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout), it is preloaded on all the routes wrapped by the layout.
- If it's the [root layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout), it is preloaded on all routes.

## Version Changes

| Version | Changes |
| --- | --- |
| v13.2.0 | @next/fontrenamed tonext/font. Installation no longer required. |
| v13.0.0 | @next/fontwas added. |

Was this helpful?

supported.
