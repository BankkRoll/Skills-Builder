# assetPrefix and more

# assetPrefix

> Learn how to use the assetPrefix config option to configure your CDN.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)assetPrefixYou are currently viewing the documentation for Pages Router.

# assetPrefix

Last updated  April 15, 2025

> **Attention**: [Deploying to Vercel](https://nextjs.org/docs/pages/getting-started/deploying) automatically configures a global CDN for your Next.js project.
> You do not need to manually setup an Asset Prefix.

> **Good to know**: Next.js 9.5+ added support for a customizable [Base Path](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath), which is better
> suited for hosting your application on a sub-path like `/docs`.
> We do not suggest you use a custom Asset Prefix for this use case.

## Set up a CDN

To set up a [CDN](https://en.wikipedia.org/wiki/Content_delivery_network), you can set up an asset prefix and configure your CDN's origin to resolve to the domain that Next.js is hosted on.

Open `next.config.mjs` and add the `assetPrefix` config based on the [phase](https://nextjs.org/docs/app/api-reference/config/next-config-js#async-configuration):

 next.config.mjs

```
// @ts-check
import { PHASE_DEVELOPMENT_SERVER } from 'next/constants'

export default (phase) => {
  const isDev = phase === PHASE_DEVELOPMENT_SERVER
  /**
   * @type {import('next').NextConfig}
   */
  const nextConfig = {
    assetPrefix: isDev ? undefined : 'https://cdn.mydomain.com',
  }
  return nextConfig
}
```

Next.js will automatically use your asset prefix for the JavaScript and CSS files it loads from the `/_next/` path (`.next/static/` folder). For example, with the above configuration, the following request for a JS chunk:

```
/_next/static/chunks/4b9b41aaa062cbbfeff4add70f256968c51ece5d.4d708494b3aed70c04f0.js
```

Would instead become:

```
https://cdn.mydomain.com/_next/static/chunks/4b9b41aaa062cbbfeff4add70f256968c51ece5d.4d708494b3aed70c04f0.js
```

The exact configuration for uploading your files to a given CDN will depend on your CDN of choice. The only folder you need to host on your CDN is the contents of `.next/static/`, which should be uploaded as `_next/static/` as the above URL request indicates. **Do not upload the rest of your.next/folder**, as you should not expose your server code and other configuration to the public.

While `assetPrefix` covers requests to `_next/static`, it does not influence the following paths:

- Files in the [public](https://nextjs.org/docs/pages/api-reference/file-conventions/public-folder) folder; if you want to serve those assets over a CDN, you'll have to introduce the prefix yourself
- `/_next/data/` requests for `getServerSideProps` pages. These requests will always be made against the main domain since they're not static.
- `/_next/data/` requests for `getStaticProps` pages. These requests will always be made against the main domain to support [Incremental Static Generation](https://nextjs.org/docs/pages/guides/incremental-static-regeneration), even if you're not using it (for consistency).

Was this helpful?

supported.

---

# basePath

> Use `basePath` to deploy a Next.js application under a sub-path of a domain.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)basePathYou are currently viewing the documentation for Pages Router.

# basePath

Last updated  April 15, 2025

To deploy a Next.js application under a sub-path of a domain you can use the `basePath` config option.

`basePath` allows you to set a path prefix for the application. For example, to use `/docs` instead of `''` (an empty string, the default), open `next.config.js` and add the `basePath` config:

 next.config.js

```
module.exports = {
  basePath: '/docs',
}
```

> **Good to know**: This value must be set at build time and cannot be changed without re-building as the value is inlined in the client-side bundles.

### Links

When linking to other pages using `next/link` and `next/router` the `basePath` will be automatically applied.

For example, using `/about` will automatically become `/docs/about` when `basePath` is set to `/docs`.

```
export default function HomePage() {
  return (
    <>
      <Link href="/about">About Page</Link>
    </>
  )
}
```

Output html:

```
<a href="/docs/about">About Page</a>
```

This makes sure that you don't have to change all links in your application when changing the `basePath` value.

### Images

When using the [next/image](https://nextjs.org/docs/pages/api-reference/components/image) component, you will need to add the `basePath` in front of `src`.

For example, using `/docs/me.png` will properly serve your image when `basePath` is set to `/docs`.

```
import Image from 'next/image'

function Home() {
  return (
    <>
      <h1>My Homepage</h1>
      <Image
        src="/docs/me.png"
        alt="Picture of the author"
        width={500}
        height={500}
      />
      <p>Welcome to my homepage!</p>
    </>
  )
}

export default Home
```

Was this helpful?

supported.

---

# bundlePagesRouterDependencies

> Enable automatic dependency bundling for Pages Router

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)bundlePagesRouterDependenciesYou are currently viewing the documentation for Pages Router.

# bundlePagesRouterDependencies

Last updated  April 15, 2025

Enable automatic server-side dependency bundling for Pages Router applications. Matches the automatic dependency bundling in App Router.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  bundlePagesRouterDependencies: true,
}

module.exports = nextConfig
```

Explicitly opt-out certain packages from being bundled using the [serverExternalPackages](https://nextjs.org/docs/pages/api-reference/config/next-config-js/serverExternalPackages) option.

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0 | Moved from experimental to stable. Renamed frombundlePagesExternalstobundlePagesRouterDependencies |

Was this helpful?

supported.

---

# compress

> Next.js provides gzip compression to compress rendered content and static files, it only works with the server target. Learn more about it here.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)compressYou are currently viewing the documentation for Pages Router.

# compress

Last updated  April 15, 2025

By default, Next.js uses `gzip` to compress rendered content and static files when using `next start` or a custom server. This is an optimization for applications that do not have compression configured. If compression is *already* configured in your application via a custom server, Next.js will not add compression.

You can check if compression is enabled and which algorithm is used by looking at the [Accept-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Encoding) (browser accepted options) and [Content-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding) (currently used) headers in the response.

## Disabling compression

To disable **compression**, set the `compress` config option to `false`:

 next.config.js

```
module.exports = {
  compress: false,
}
```

We **do not recommend disabling compression** unless you have compression configured on your server, as compression reduces bandwidth usage and improves the performance of your application. For example, you're using [nginx](https://nginx.org/) and want to switch to `brotli`, set the `compress` option to `false` to allow nginx to handle compression.

Was this helpful?

supported.

---

# crossOrigin

> Use the `crossOrigin` option to add a crossOrigin tag on the `script` tags generated by `next/script` and `next/head`.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)crossOriginYou are currently viewing the documentation for Pages Router.

# crossOrigin

Last updated  April 15, 2025

Use the `crossOrigin` option to add a [crossOriginattribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin) in all `<script>` tags generated by the   [next/script](https://nextjs.org/docs/pages/guides/scripts) and [next/head](https://nextjs.org/docs/pages/api-reference/components/head)components , and define how cross-origin requests should be handled.

 next.config.js

```
module.exports = {
  crossOrigin: 'anonymous',
}
```

## Options

- `'anonymous'`: Adds [crossOrigin="anonymous"](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin#anonymous) attribute.
- `'use-credentials'`: Adds [crossOrigin="use-credentials"](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin#use-credentials).

Was this helpful?

supported.

---

# devIndicators

> Optimized pages include an indicator to let you know if it's being statically optimized. You can opt-out of it here.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)devIndicatorsYou are currently viewing the documentation for Pages Router.

# devIndicators

Last updated  April 15, 2025

`devIndicators` allows you to configure the on-screen indicator that gives context about the current route you're viewing during development.

 Types

```
devIndicators: false | {
    position?: 'bottom-right'
    | 'bottom-left'
    | 'top-right'
    | 'top-left', // defaults to 'bottom-left',
  },
```

Setting `devIndicators` to `false` will hide the indicator, however Next.js will continue to surface any build or runtime errors that were encountered.

## Troubleshooting

### Indicator not marking a route as static

If you expect a route to be static and the indicator has marked it as dynamic, it's likely the route has opted out of static rendering.

You can confirm if a route is [static](https://nextjs.org/docs/app/guides/caching#static-rendering) or [dynamic](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) by building your application using `next build --debug`, and checking the output in your terminal. Static (or prerendered) routes will display a `○` symbol, whereas dynamic routes will display a `ƒ` symbol. For example:

 Build Output

```
Route (app)
┌ ○ /_not-found
└ ƒ /products/[id]

○  (Static)   prerendered as static content
ƒ  (Dynamic)  server-rendered on demand
```

When exporting [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props) or [getInitialProps](https://nextjs.org/docs/pages/api-reference/functions/get-initial-props) from a page, it will be marked as dynamic.

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | appIsrStatus,buildActivity, andbuildActivityPositionoptions have been removed. |
| v15.2.0 | Improved on-screen indicator with newpositionoption.appIsrStatus,buildActivity, andbuildActivityPositionoptions have been deprecated. |
| v15.0.0 | Static on-screen indicator added withappIsrStatusoption. |

Was this helpful?

supported.

---

# distDir

> Set a custom build directory to use instead of the default .next directory.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)distDirYou are currently viewing the documentation for Pages Router.

# distDir

Last updated  April 15, 2025

You can specify a name to use for a custom build directory to use instead of `.next`.

Open `next.config.js` and add the `distDir` config:

 next.config.js

```
module.exports = {
  distDir: 'build',
}
```

Now if you run `next build` Next.js will use `build` instead of the default `.next` folder.

> `distDir` **should not** leave your project directory. For example, `../build` is an **invalid** directory.

Was this helpful?

supported.

---

# env

> Learn to add and access environment variables in your Next.js application at build time.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)envYou are currently viewing the documentation for Pages Router.

# env

Last updated  April 15, 2025

> Since the release of [Next.js 9.4](https://nextjs.org/blog/next-9-4) we now have a more intuitive and ergonomic experience for [adding environment variables](https://nextjs.org/docs/pages/guides/environment-variables). Give it a try!

> **Good to know**: environment variables specified in this way will **always** be included in the JavaScript bundle, prefixing the environment variable name with `NEXT_PUBLIC_` only has an effect when specifying them [through the environment or .env files](https://nextjs.org/docs/pages/guides/environment-variables).

To add environment variables to the JavaScript bundle, open `next.config.js` and add the `env` config:

 next.config.js

```
module.exports = {
  env: {
    customKey: 'my-value',
  },
}
```

Now you can access `process.env.customKey` in your code. For example:

```
function Page() {
  return <h1>The value of customKey is: {process.env.customKey}</h1>
}

export default Page
```

Next.js will replace `process.env.customKey` with `'my-value'` at build time. Trying to destructure `process.env` variables won't work due to the nature of webpack [DefinePlugin](https://webpack.js.org/plugins/define-plugin/).

For example, the following line:

```
return <h1>The value of customKey is: {process.env.customKey}</h1>
```

Will end up being:

```
return <h1>The value of customKey is: {'my-value'}</h1>
```

Was this helpful?

supported.

---

# exportPathMap

> Customize the pages that will be exported as HTML files when using `next export`.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)exportPathMapYou are currently viewing the documentation for Pages Router.

# exportPathMap

Last updated  April 15, 2025

> This feature is exclusive to `next export` and currently **deprecated** in favor of `getStaticPaths` with `pages` or `generateStaticParams` with `app`.

`exportPathMap` allows you to specify a mapping of request paths to page destinations, to be used during export. Paths defined in `exportPathMap` will also be available when using [next dev](https://nextjs.org/docs/app/api-reference/cli/next#next-dev-options).

Let's start with an example, to create a custom `exportPathMap` for an app with the following pages:

- `pages/index.js`
- `pages/about.js`
- `pages/post.js`

Open `next.config.js` and add the following `exportPathMap` config:

 next.config.js

```
module.exports = {
  exportPathMap: async function (
    defaultPathMap,
    { dev, dir, outDir, distDir, buildId }
  ) {
    return {
      '/': { page: '/' },
      '/about': { page: '/about' },
      '/p/hello-nextjs': { page: '/post', query: { title: 'hello-nextjs' } },
      '/p/learn-nextjs': { page: '/post', query: { title: 'learn-nextjs' } },
      '/p/deploy-nextjs': { page: '/post', query: { title: 'deploy-nextjs' } },
    }
  },
}
```

> **Good to know**: the `query` field in `exportPathMap` cannot be used with [automatically statically optimized pages](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization) or [getStaticPropspages](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) as they are rendered to HTML files at build-time and additional query information cannot be provided during `next export`.

The pages will then be exported as HTML files, for example, `/about` will become `/about.html`.

`exportPathMap` is an `async` function that receives 2 arguments: the first one is `defaultPathMap`, which is the default map used by Next.js. The second argument is an object with:

- `dev` - `true` when `exportPathMap` is being called in development. `false` when running `next export`. In development `exportPathMap` is used to define routes.
- `dir` - Absolute path to the project directory
- `outDir` - Absolute path to the `out/` directory ([configurable with-o](#customizing-the-output-directory)). When `dev` is `true` the value of `outDir` will be `null`.
- `distDir` - Absolute path to the `.next/` directory (configurable with the [distDir](https://nextjs.org/docs/pages/api-reference/config/next-config-js/distDir) config)
- `buildId` - The generated build id

The returned object is a map of pages where the `key` is the `pathname` and the `value` is an object that accepts the following fields:

- `page`: `String` - the page inside the `pages` directory to render
- `query`: `Object` - the `query` object passed to `getInitialProps` when prerendering. Defaults to `{}`

> The exported `pathname` can also be a filename (for example, `/readme.md`), but you may need to set the `Content-Type` header to `text/html` when serving its content if it is different than `.html`.

## Adding a trailing slash

It is possible to configure Next.js to export pages as `index.html` files and require trailing slashes, `/about` becomes `/about/index.html` and is routable via `/about/`. This was the default behavior prior to Next.js 9.

To switch back and add a trailing slash, open `next.config.js` and enable the `trailingSlash` config:

 next.config.js

```
module.exports = {
  trailingSlash: true,
}
```

## Customizing the output directory

[next export](https://nextjs.org/docs/pages/guides/static-exports) will use `out` as the default output directory, you can customize this using the `-o` argument, like so:

 Terminal

```
next export -o outdir
```

> **Warning**: Using `exportPathMap` is deprecated and is overridden by `getStaticPaths` inside `pages`. We don't recommend using them together.

Was this helpful?

supported.

---

# generateBuildId

> Configure the build id, which is used to identify the current build in which your application is being served.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)generateBuildIdYou are currently viewing the documentation for Pages Router.

# generateBuildId

Last updated  April 15, 2025

Next.js generates an ID during `next build` to identify which version of your application is being served. The same build should be used and boot up multiple containers.

If you are rebuilding for each stage of your environment, you will need to generate a consistent build ID to use between containers. Use the `generateBuildId` command in `next.config.js`:

 next.config.js

```
module.exports = {
  generateBuildId: async () => {
    // This could be anything, using the latest git hash
    return process.env.GIT_HASH
  },
}
```

Was this helpful?

supported.

---

# generateEtags

> Next.js will generate etags for every page by default. Learn more about how to disable etag generation here.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)generateEtagsYou are currently viewing the documentation for Pages Router.

# generateEtags

Last updated  April 15, 2025

Next.js will generate [etags](https://en.wikipedia.org/wiki/HTTP_ETag) for every page by default. You may want to disable etag generation for HTML pages depending on your cache strategy.

Open `next.config.js` and disable the `generateEtags` option:

 next.config.js

```
module.exports = {
  generateEtags: false,
}
```

Was this helpful?

supported.

---

# headers

> Add custom HTTP headers to your Next.js app.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)headersYou are currently viewing the documentation for Pages Router.

# headers

Last updated  April 15, 2025

Headers allow you to set custom HTTP headers on the response to an incoming request on a given path.

To set custom HTTP headers you can use the `headers` key in `next.config.js`:

 next.config.js

```
module.exports = {
  async headers() {
    return [
      {
        source: '/about',
        headers: [
          {
            key: 'x-custom-header',
            value: 'my custom header value',
          },
          {
            key: 'x-another-custom-header',
            value: 'my other custom header value',
          },
        ],
      },
    ]
  },
}
```

`headers` is an async function that expects an array to be returned holding objects with `source` and `headers` properties:

- `source` is the incoming request path pattern.
- `headers` is an array of response header objects, with `key` and `value` properties.
- `basePath`: `false` or `undefined` - if false the basePath won't be included when matching, can be used for external rewrites only.
- `locale`: `false` or `undefined` - whether the locale should not be included when matching.
- `has` is an array of [has objects](#header-cookie-and-query-matching) with the `type`, `key` and `value` properties.
- `missing` is an array of [missing objects](#header-cookie-and-query-matching) with the `type`, `key` and `value` properties.

Headers are checked before the filesystem which includes pages and `/public` files.

## Header Overriding Behavior

If two headers match the same path and set the same header key, the last header key will override the first. Using the below headers, the path `/hello` will result in the header `x-hello` being `world` due to the last header value set being `world`.

 next.config.js

```
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'x-hello',
            value: 'there',
          },
        ],
      },
      {
        source: '/hello',
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
    ]
  },
}
```

## Path Matching

Path matches are allowed, for example `/blog/:slug` will match `/blog/first-post` (no nested paths):

 next.config.js

```
module.exports = {
  async headers() {
    return [
      {
        source: '/blog/:slug',
        headers: [
          {
            key: 'x-slug',
            value: ':slug', // Matched parameters can be used in the value
          },
          {
            key: 'x-slug-:slug', // Matched parameters can be used in the key
            value: 'my other custom header value',
          },
        ],
      },
    ]
  },
}
```

The pattern `/blog/:slug` matches `/blog/first-post` and `/blog/post-1` but not a nested path like `/blog/a/b`. Patterns are anchored to the start, `/blog/:slug` will not match `/archive/blog/first-post`.

You can use modifiers on parameters: `*` (zero or more), `+` (one or more), `?` (zero or one). For example, `/blog/:slug*` matches `/blog`, `/blog/a`, and `/blog/a/b/c`.

Read more details on [path-to-regexp](https://github.com/pillarjs/path-to-regexp) documentation.

### Wildcard Path Matching

To match a wildcard path you can use `*` after a parameter, for example `/blog/:slug*` will match `/blog/a/b/c/d/hello-world`:

 next.config.js

```
module.exports = {
  async headers() {
    return [
      {
        source: '/blog/:slug*',
        headers: [
          {
            key: 'x-slug',
            value: ':slug*', // Matched parameters can be used in the value
          },
          {
            key: 'x-slug-:slug*', // Matched parameters can be used in the key
            value: 'my other custom header value',
          },
        ],
      },
    ]
  },
}
```

### Regex Path Matching

To match a regex path you can wrap the regex in parenthesis after a parameter, for example `/blog/:slug(\\d{1,})` will match `/blog/123` but not `/blog/abc`:

 next.config.js

```
module.exports = {
  async headers() {
    return [
      {
        source: '/blog/:post(\\d{1,})',
        headers: [
          {
            key: 'x-post',
            value: ':post',
          },
        ],
      },
    ]
  },
}
```

The following characters `(`, `)`, `{`, `}`, `:`, `*`, `+`, `?` are used for regex path matching, so when used in the `source` as non-special values they must be escaped by adding `\\` before them:

 next.config.js

```
module.exports = {
  async headers() {
    return [
      {
        // this will match `/english(default)/something` being requested
        source: '/english\\(default\\)/:slug',
        headers: [
          {
            key: 'x-header',
            value: 'value',
          },
        ],
      },
    ]
  },
}
```

## Header, Cookie, and Query Matching

To only apply a header when header, cookie, or query values also match the `has` field or don't match the `missing` field can be used. Both the `source` and all `has` items must match and all `missing` items must not match for the header to be applied.

`has` and `missing` items can have the following fields:

- `type`: `String` - must be either `header`, `cookie`, `host`, or `query`.
- `key`: `String` - the key from the selected type to match against.
- `value`: `String` or `undefined` - the value to check for, if undefined any value will match. A regex like string can be used to capture a specific part of the value, e.g. if the value `first-(?<paramName>.*)` is used for `first-second` then `second` will be usable in the destination with `:paramName`.

 next.config.js

```
module.exports = {
  async headers() {
    return [
      // if the header `x-add-header` is present,
      // the `x-another-header` header will be applied
      {
        source: '/:path*',
        has: [
          {
            type: 'header',
            key: 'x-add-header',
          },
        ],
        headers: [
          {
            key: 'x-another-header',
            value: 'hello',
          },
        ],
      },
      // if the header `x-no-header` is not present,
      // the `x-another-header` header will be applied
      {
        source: '/:path*',
        missing: [
          {
            type: 'header',
            key: 'x-no-header',
          },
        ],
        headers: [
          {
            key: 'x-another-header',
            value: 'hello',
          },
        ],
      },
      // if the source, query, and cookie are matched,
      // the `x-authorized` header will be applied
      {
        source: '/specific/:path*',
        has: [
          {
            type: 'query',
            key: 'page',
            // the page value will not be available in the
            // header key/values since value is provided and
            // doesn't use a named capture group e.g. (?<page>home)
            value: 'home',
          },
          {
            type: 'cookie',
            key: 'authorized',
            value: 'true',
          },
        ],
        headers: [
          {
            key: 'x-authorized',
            value: ':authorized',
          },
        ],
      },
      // if the header `x-authorized` is present and
      // contains a matching value, the `x-another-header` will be applied
      {
        source: '/:path*',
        has: [
          {
            type: 'header',
            key: 'x-authorized',
            value: '(?<authorized>yes|true)',
          },
        ],
        headers: [
          {
            key: 'x-another-header',
            value: ':authorized',
          },
        ],
      },
      // if the host is `example.com`,
      // this header will be applied
      {
        source: '/:path*',
        has: [
          {
            type: 'host',
            value: 'example.com',
          },
        ],
        headers: [
          {
            key: 'x-another-header',
            value: ':authorized',
          },
        ],
      },
    ]
  },
}
```

## Headers with basePath support

When leveraging [basePathsupport](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath) with headers each `source` is automatically prefixed with the `basePath` unless you add `basePath: false` to the header:

 next.config.js

```
module.exports = {
  basePath: '/docs',

  async headers() {
    return [
      {
        source: '/with-basePath', // becomes /docs/with-basePath
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
      {
        source: '/without-basePath', // is not modified since basePath: false is set
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
        basePath: false,
      },
    ]
  },
}
```

## Headers with i18n support

When leveraging [i18nsupport](https://nextjs.org/docs/pages/guides/internationalization) with headers each `source` is automatically prefixed to handle the configured `locales` unless you add `locale: false` to the header. If `locale: false` is used you must prefix the `source` with a locale for it to be matched correctly.

 next.config.js

```
module.exports = {
  i18n: {
    locales: ['en', 'fr', 'de'],
    defaultLocale: 'en',
  },

  async headers() {
    return [
      {
        source: '/with-locale', // automatically handles all locales
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
      {
        // does not handle locales automatically since locale: false is set
        source: '/nl/with-locale-manual',
        locale: false,
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
      {
        // this matches '/' since `en` is the defaultLocale
        source: '/en',
        locale: false,
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
      {
        // this gets converted to /(en|fr|de)/(.*) so will not match the top-level
        // `/` or `/fr` routes like /:path* would
        source: '/(.*)',
        headers: [
          {
            key: 'x-hello',
            value: 'world',
          },
        ],
      },
    ]
  },
}
```

## Cache-Control

Next.js sets the `Cache-Control` header of `public, max-age=31536000, immutable` for truly immutable assets. It cannot be overridden. These immutable files contain a SHA-hash in the file name, so they can be safely cached indefinitely. For example, [Static Image Imports](https://nextjs.org/docs/app/getting-started/images#local-images). You cannot set `Cache-Control` headers in `next.config.js` for these assets.

However, you can set `Cache-Control` headers for other responses or data.

If you need to revalidate the cache of a page that has been [statically generated](https://nextjs.org/docs/pages/building-your-application/rendering/static-site-generation), you can do so by setting the `revalidate` prop in the page's [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) function.

To cache the response from an [API Route](https://nextjs.org/docs/pages/building-your-application/routing/api-routes), you can use `res.setHeader`:

pages/api/hello.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

type ResponseData = {
  message: string
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  res.setHeader('Cache-Control', 's-maxage=86400')
  res.status(200).json({ message: 'Hello from Next.js!' })
}
```

You can also use caching headers (`Cache-Control`) inside `getServerSideProps` to cache dynamic responses. For example, using [stale-while-revalidate](https://web.dev/stale-while-revalidate/).

pages/index.tsxJavaScriptTypeScript

```
import { GetStaticProps, GetStaticPaths, GetServerSideProps } from 'next'

// This value is considered fresh for ten seconds (s-maxage=10).
// If a request is repeated within the next 10 seconds, the previously
// cached value will still be fresh. If the request is repeated before 59 seconds,
// the cached value will be stale but still render (stale-while-revalidate=59).
//
// In the background, a revalidation request will be made to populate the cache
// with a fresh value. If you refresh the page, you will see the new value.
export const getServerSideProps = (async (context) => {
  context.res.setHeader(
    'Cache-Control',
    'public, s-maxage=10, stale-while-revalidate=59'
  )

  return {
    props: {},
  }
}) satisfies GetServerSideProps
```

## Options

### CORS

[Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/docs/Web/HTTP/CORS) is a security feature that allows you to control which sites can access your resources. You can set the `Access-Control-Allow-Origin` header to allow a specific origin to access your  API Endpoints .

```
async headers() {
    return [
      {
        source: "/api/:path*",
        headers: [
          {
            key: "Access-Control-Allow-Origin",
            value: "*", // Set your origin
          },
          {
            key: "Access-Control-Allow-Methods",
            value: "GET, POST, PUT, DELETE, OPTIONS",
          },
          {
            key: "Access-Control-Allow-Headers",
            value: "Content-Type, Authorization",
          },
        ],
      },
    ];
  },
```

### X-DNS-Prefetch-Control

[This header](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-DNS-Prefetch-Control) controls DNS prefetching, allowing browsers to proactively perform domain name resolution on external links, images, CSS, JavaScript, and more. This prefetching is performed in the background, so the [DNS](https://developer.mozilla.org/docs/Glossary/DNS) is more likely to be resolved by the time the referenced items are needed. This reduces latency when the user clicks a link.

```
{
  key: 'X-DNS-Prefetch-Control',
  value: 'on'
}
```

### Strict-Transport-Security

[This header](https://developer.mozilla.org/docs/Web/HTTP/Headers/Strict-Transport-Security) informs browsers it should only be accessed using HTTPS, instead of using HTTP. Using the configuration below, all present and future subdomains will use HTTPS for a `max-age` of 2 years. This blocks access to pages or subdomains that can only be served over HTTP.

```
{
  key: 'Strict-Transport-Security',
  value: 'max-age=63072000; includeSubDomains; preload'
}
```

### X-Frame-Options

[This header](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Frame-Options) indicates whether the site should be allowed to be displayed within an `iframe`. This can prevent against clickjacking attacks.

**This header has been superseded by CSP'sframe-ancestorsoption**, which has better support in modern browsers (see [Content Security Policy](https://nextjs.org/docs/app/guides/content-security-policy) for configuration details).

```
{
  key: 'X-Frame-Options',
  value: 'SAMEORIGIN'
}
```

### Permissions-Policy

[This header](https://developer.mozilla.org/docs/Web/HTTP/Headers/Permissions-Policy) allows you to control which features and APIs can be used in the browser. It was previously named `Feature-Policy`.

```
{
  key: 'Permissions-Policy',
  value: 'camera=(), microphone=(), geolocation=(), browsing-topics=()'
}
```

### X-Content-Type-Options

[This header](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Content-Type-Options) prevents the browser from attempting to guess the type of content if the `Content-Type` header is not explicitly set. This can prevent XSS exploits for websites that allow users to upload and share files.

For example, a user trying to download an image, but having it treated as a different `Content-Type` like an executable, which could be malicious. This header also applies to downloading browser extensions. The only valid value for this header is `nosniff`.

```
{
  key: 'X-Content-Type-Options',
  value: 'nosniff'
}
```

### Referrer-Policy

[This header](https://developer.mozilla.org/docs/Web/HTTP/Headers/Referrer-Policy) controls how much information the browser includes when navigating from the current website (origin) to another.

```
{
  key: 'Referrer-Policy',
  value: 'origin-when-cross-origin'
}
```

### Content-Security-Policy

Learn more about adding a [Content Security Policy](https://nextjs.org/docs/app/guides/content-security-policy) to your application.

## Version History

| Version | Changes |
| --- | --- |
| v13.3.0 | missingadded. |
| v10.2.0 | hasadded. |
| v9.5.0 | Headers added. |

Was this helpful?

supported.

---

# httpAgentOptions

> Next.js will automatically use HTTP Keep-Alive by default. Learn more about how to disable HTTP Keep-Alive here.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)httpAgentOptionsYou are currently viewing the documentation for Pages Router.

# httpAgentOptions

Last updated  April 15, 2025

In Node.js versions prior to 18, Next.js automatically polyfills `fetch()` with [undici](https://nextjs.org/docs/architecture/supported-browsers#polyfills) and enables [HTTP Keep-Alive](https://developer.mozilla.org/docs/Web/HTTP/Headers/Keep-Alive) by default.

To disable HTTP Keep-Alive for all `fetch()` calls on the server-side, open `next.config.js` and add the `httpAgentOptions` config:

 next.config.js

```
module.exports = {
  httpAgentOptions: {
    keepAlive: false,
  },
}
```

Was this helpful?

supported.

---

# images

> Custom configuration for the next/image loader

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)imagesYou are currently viewing the documentation for Pages Router.

# images

Last updated  April 15, 2025

If you want to use a cloud provider to optimize images instead of using the Next.js built-in Image Optimization API, you can configure `next.config.js` with the following:

 next.config.js

```
module.exports = {
  images: {
    loader: 'custom',
    loaderFile: './my/image/loader.js',
  },
}
```

This `loaderFile` must point to a file relative to the root of your Next.js application. The file must export a default function that returns a string, for example:

   my/image/loader.js

```
export default function myImageLoader({ src, width, quality }) {
  return `https://example.com/${src}?w=${width}&q=${quality || 75}`
}
```

Alternatively, you can use the [loaderprop](https://nextjs.org/docs/pages/api-reference/components/image#loader) to pass the function to each instance of `next/image`.

To learn more about configuring the behavior of the built-in [Image Optimization API](https://nextjs.org/docs/pages/api-reference/components/image) and the [Image Component](https://nextjs.org/docs/pages/api-reference/components/image), see [Image Configuration Options](https://nextjs.org/docs/pages/api-reference/components/image#configuration-options) for available options.

## Example Loader Configuration

- [Akamai](#akamai)
- [AWS CloudFront](#aws-cloudfront)
- [Cloudinary](#cloudinary)
- [Cloudflare](#cloudflare)
- [Contentful](#contentful)
- [Fastly](#fastly)
- [Gumlet](#gumlet)
- [ImageEngine](#imageengine)
- [Imgix](#imgix)
- [PixelBin](#pixelbin)
- [Sanity](#sanity)
- [Sirv](#sirv)
- [Supabase](#supabase)
- [Thumbor](#thumbor)
- [Imagekit](#imagekitio)
- [Nitrogen AIO](#nitrogen-aio)

### Akamai

```
// Docs: https://techdocs.akamai.com/ivm/reference/test-images-on-demand
export default function akamaiLoader({ src, width, quality }) {
  return `https://example.com/${src}?imwidth=${width}`
}
```

### AWS CloudFront

```
// Docs: https://aws.amazon.com/developer/application-security-performance/articles/image-optimization
export default function cloudfrontLoader({ src, width, quality }) {
  const url = new URL(`https://example.com${src}`)
  url.searchParams.set('format', 'auto')
  url.searchParams.set('width', width.toString())
  url.searchParams.set('quality', (quality || 75).toString())
  return url.href
}
```

### Cloudinary

```
// Demo: https://res.cloudinary.com/demo/image/upload/w_300,c_limit,q_auto/turtles.jpg
export default function cloudinaryLoader({ src, width, quality }) {
  const params = ['f_auto', 'c_limit', `w_${width}`, `q_${quality || 'auto'}`]
  return `https://example.com/${params.join(',')}${src}`
}
```

### Cloudflare

```
// Docs: https://developers.cloudflare.com/images/transform-images
export default function cloudflareLoader({ src, width, quality }) {
  const params = [`width=${width}`, `quality=${quality || 75}`, 'format=auto']
  return `https://example.com/cdn-cgi/image/${params.join(',')}/${src}`
}
```

### Contentful

```
// Docs: https://www.contentful.com/developers/docs/references/images-api/
export default function contentfulLoader({ src, width, quality }) {
  const url = new URL(`https://example.com${src}`)
  url.searchParams.set('fm', 'webp')
  url.searchParams.set('w', width.toString())
  url.searchParams.set('q', (quality || 75).toString())
  return url.href
}
```

### Fastly

```
// Docs: https://developer.fastly.com/reference/io/
export default function fastlyLoader({ src, width, quality }) {
  const url = new URL(`https://example.com${src}`)
  url.searchParams.set('auto', 'webp')
  url.searchParams.set('width', width.toString())
  url.searchParams.set('quality', (quality || 75).toString())
  return url.href
}
```

### Gumlet

```
// Docs: https://docs.gumlet.com/reference/image-transform-size
export default function gumletLoader({ src, width, quality }) {
  const url = new URL(`https://example.com${src}`)
  url.searchParams.set('format', 'auto')
  url.searchParams.set('w', width.toString())
  url.searchParams.set('q', (quality || 75).toString())
  return url.href
}
```

### ImageEngine

```
// Docs: https://support.imageengine.io/hc/en-us/articles/360058880672-Directives
export default function imageengineLoader({ src, width, quality }) {
  const compression = 100 - (quality || 50)
  const params = [`w_${width}`, `cmpr_${compression}`)]
  return `https://example.com${src}?imgeng=/${params.join('/')`
}
```

### Imgix

```
// Demo: https://static.imgix.net/daisy.png?format=auto&fit=max&w=300
export default function imgixLoader({ src, width, quality }) {
  const url = new URL(`https://example.com${src}`)
  const params = url.searchParams
  params.set('auto', params.getAll('auto').join(',') || 'format')
  params.set('fit', params.get('fit') || 'max')
  params.set('w', params.get('w') || width.toString())
  params.set('q', (quality || 50).toString())
  return url.href
}
```

### PixelBin

```
// Doc (Resize): https://www.pixelbin.io/docs/transformations/basic/resize/#width-w
// Doc (Optimise): https://www.pixelbin.io/docs/optimizations/quality/#image-quality-when-delivering
// Doc (Auto Format Delivery): https://www.pixelbin.io/docs/optimizations/format/#automatic-format-selection-with-f_auto-url-parameter
export default function pixelBinLoader({ src, width, quality }) {
  const name = '<your-cloud-name>'
  const opt = `t.resize(w:${width})~t.compress(q:${quality || 75})`
  return `https://cdn.pixelbin.io/v2/${name}/${opt}/${src}?f_auto=true`
}
```

### Sanity

```
// Docs: https://www.sanity.io/docs/image-urls
export default function sanityLoader({ src, width, quality }) {
  const prj = 'zp7mbokg'
  const dataset = 'production'
  const url = new URL(`https://cdn.sanity.io/images/${prj}/${dataset}${src}`)
  url.searchParams.set('auto', 'format')
  url.searchParams.set('fit', 'max')
  url.searchParams.set('w', width.toString())
  if (quality) {
    url.searchParams.set('q', quality.toString())
  }
  return url.href
}
```

### Sirv

```
// Docs: https://sirv.com/help/articles/dynamic-imaging/
export default function sirvLoader({ src, width, quality }) {
  const url = new URL(`https://example.com${src}`)
  const params = url.searchParams
  params.set('format', params.getAll('format').join(',') || 'optimal')
  params.set('w', params.get('w') || width.toString())
  params.set('q', (quality || 85).toString())
  return url.href
}
```

### Supabase

```
// Docs: https://supabase.com/docs/guides/storage/image-transformations#nextjs-loader
export default function supabaseLoader({ src, width, quality }) {
  const url = new URL(`https://example.com${src}`)
  url.searchParams.set('width', width.toString())
  url.searchParams.set('quality', (quality || 75).toString())
  return url.href
}
```

### Thumbor

```
// Docs: https://thumbor.readthedocs.io/en/latest/
export default function thumborLoader({ src, width, quality }) {
  const params = [`${width}x0`, `filters:quality(${quality || 75})`]
  return `https://example.com${params.join('/')}${src}`
}
```

### ImageKit.io

```
// Docs: https://imagekit.io/docs/image-transformation
export default function imageKitLoader({ src, width, quality }) {
  const params = [`w-${width}`, `q-${quality || 80}`]
  return `https://ik.imagekit.io/your_imagekit_id/${src}?tr=${params.join(',')}`
}
```

### Nitrogen AIO

```
// Docs: https://docs.n7.io/aio/intergrations/
export default function aioLoader({ src, width, quality }) {
  const url = new URL(src, window.location.href)
  const params = url.searchParams
  const aioParams = params.getAll('aio')
  aioParams.push(`w-${width}`)
  if (quality) {
    aioParams.push(`q-${quality.toString()}`)
  }
  params.set('aio', aioParams.join(';'))
  return url.href
}
```

Was this helpful?

supported.

---

# isolatedDevBuild

> Use isolated directories for development builds to prevent conflicts with production builds.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)isolatedDevBuildYou are currently viewing the documentation for Pages Router.

# isolatedDevBuild

Last updated  October 9, 2025

The experimental `isolatedDevBuild` option separates development and production build outputs into different directories. When enabled, the development server (`next dev`) writes its output to `.next/dev` instead of `.next`, preventing conflicts when running `next dev` and `next build` concurrently.

This is especially helpful when automated tools (for example, AI agents) run `next build` to validate changes while your development server is running, ensuring the dev server is not affected by changes made by the build process.

This feature is **enabled by default** to keep development and production outputs separate and prevent conflicts.

## Configuration

To opt out of this feature, set `isolatedDevBuild` to `false` in your configuration:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    isolatedDevBuild: false, // defaults to true
  },
}

export default nextConfig
```

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | experimental.isolatedDevBuildis introduced. |

Was this helpful?

supported.

---

# onDemandEntries

> Configure how Next.js will dispose and keep in memory pages created in development.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)onDemandEntriesYou are currently viewing the documentation for Pages Router.

# onDemandEntries

Last updated  April 15, 2025

Next.js exposes some options that give you some control over how the server will dispose or keep in memory built pages in development.

To change the defaults, open `next.config.js` and add the `onDemandEntries` config:

 next.config.js

```
module.exports = {
  onDemandEntries: {
    // period (in ms) where the server will keep pages in the buffer
    maxInactiveAge: 25 * 1000,
    // number of pages that should be kept simultaneously without being disposed
    pagesBufferLength: 2,
  },
}
```

Was this helpful?

supported.

---

# optimizePackageImports

> API Reference for optimizePackageImports Next.js Config Option

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)optimizePackageImportsYou are currently viewing the documentation for Pages Router.

# optimizePackageImports

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  December 19, 2025

Some packages can export hundreds or thousands of modules, which can cause performance issues in development and production.

Adding a package to `experimental.optimizePackageImports` will only load the modules you are actually using, while still giving you the convenience of writing import statements with many named exports.

 next.config.js

```
module.exports = {
  experimental: {
    optimizePackageImports: ['package-name'],
  },
}
```

The following libraries are optimized by default:

- `lucide-react`
- `date-fns`
- `lodash-es`
- `ramda`
- `antd`
- `react-bootstrap`
- `ahooks`
- `@ant-design/icons`
- `@headlessui/react`
- `@headlessui-float/react`
- `@heroicons/react/20/solid`
- `@heroicons/react/24/solid`
- `@heroicons/react/24/outline`
- `@visx/visx`
- `@tremor/react`
- `rxjs`
- `@mui/material`
- `@mui/icons-material`
- `recharts`
- `react-use`
- `@material-ui/core`
- `@material-ui/icons`
- `@tabler/icons-react`
- `mui-core`
- `react-icons/*`
- `effect`
- `@effect/*`

Was this helpful?

supported.
