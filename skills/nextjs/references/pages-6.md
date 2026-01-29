# output and more

# output

> Next.js automatically traces which files are needed by each page to allow for easy deployment of your application. Learn how it works here.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)outputYou are currently viewing the documentation for Pages Router.

# output

Last updated  April 15, 2025

During a build, Next.js will automatically trace each page and its dependencies to determine all of the files that are needed for deploying a production version of your application.

This feature helps reduce the size of deployments drastically. Previously, when deploying with Docker you would need to have all files from your package's `dependencies` installed to run `next start`. Starting with Next.js 12, you can leverage Output File Tracing in the `.next/` directory to only include the necessary files.

Furthermore, this removes the need for the deprecated `serverless` target which can cause various issues and also creates unnecessary duplication.

## How it Works

During `next build`, Next.js will use [@vercel/nft](https://github.com/vercel/nft) to statically analyze `import`, `require`, and `fs` usage to determine all files that a page might load.

Next.js' production server is also traced for its needed files and output at `.next/next-server.js.nft.json` which can be leveraged in production.

To leverage the `.nft.json` files emitted to the `.next` output directory, you can read the list of files in each trace that are relative to the `.nft.json` file and then copy them to your deployment location.

## Automatically Copying Traced Files

Next.js can automatically create a `standalone` folder that copies only the necessary files for a production deployment including select files in `node_modules`.

To leverage this automatic copying you can enable it in your `next.config.js`:

 next.config.js

```
module.exports = {
  output: 'standalone',
}
```

This will create a folder at `.next/standalone` which can then be deployed on its own without installing `node_modules`.

Additionally, a minimal `server.js` file is also output which can be used instead of `next start`. This minimal server does not copy the `public` or `.next/static` folders by default as these should ideally be handled by a CDN instead, although these folders can be copied to the `standalone/public` and `standalone/.next/static` folders manually, after which `server.js` file will serve these automatically.

To copy these manually, you can use the `cp` command-line tool after you `next build`:

 Terminal

```
cp -r public .next/standalone/ && cp -r .next/static .next/standalone/.next/
```

To start your minimal `server.js` file locally, run the following command:

 Terminal

```
node .next/standalone/server.js
```

> **Good to know**:
>
>
>
> - `next.config.js` is read during `next build` and serialized into the `server.js` output file.
> - If your project needs to listen to a specific port or hostname, you can define `PORT` or `HOSTNAME` environment variables before running `server.js`. For example, run `PORT=8080 HOSTNAME=0.0.0.0 node server.js` to start the server on `http://0.0.0.0:8080`.

## Caveats

- While tracing in monorepo setups, the project directory is used for tracing by default. For `next build packages/web-app`, `packages/web-app` would be the tracing root and any files outside of that folder will not be included. To include files outside of this folder you can set `outputFileTracingRoot` in your `next.config.js`.

 packages/web-app/next.config.js

```
const path = require('path')

module.exports = {
  // this includes files from the monorepo base two directories up
  outputFileTracingRoot: path.join(__dirname, '../../'),
}
```

- There are some cases in which Next.js might fail to include required files, or might incorrectly include unused files. In those cases, you can leverage `outputFileTracingExcludes` and `outputFileTracingIncludes` respectively in `next.config.js`. Each option accepts an object whose keys are **route globs** (matched with [picomatch](https://www.npmjs.com/package/picomatch#basic-globbing) against the route path, e.g. `/api/hello`) and whose values are **glob patterns resolved from the project root** that specify files to include or exclude in the trace.

> **Good to know**:
> In a monorepo, `project root` refers to the Next.js project root (the folder containing next.config.js, e.g., packages/web-app), not necessarily the monorepo root.

 next.config.js

```
module.exports = {
  outputFileTracingExcludes: {
    '/api/hello': ['./un-necessary-folder/**/*'],
  },
  outputFileTracingIncludes: {
    '/api/another': ['./necessary-folder/**/*'],
    '/api/login/\\[\\[\\.\\.\\.slug\\]\\]': [
      './node_modules/aws-crt/dist/bin/**/*',
    ],
  },
}
```

Using a `src/` directory does not change how you write these options:

- **Keys** still match the route path (`'/api/hello'`, `'/products/[id]'`, etc.).
- **Values** can reference paths under `src/` since they are resolved relative to the project root.

 next.config.js

```
module.exports = {
  outputFileTracingIncludes: {
    '/products/*': ['src/lib/payments/**/*'],
    '/*': ['src/config/runtime/**/*.json'],
  },
  outputFileTracingExcludes: {
    '/api/*': ['src/temp/**/*', 'public/large-logs/**/*'],
  },
}
```

You can also target all routes using a global key like `'/*'`:

 next.config.js

```
module.exports = {
  outputFileTracingIncludes: {
    '/*': ['src/i18n/locales/**/*.json'],
  },
}
```

These options are applied to server traces and do not affect routes that do not produce a server trace file:

- Edge Runtime routes are not affected.
- Fully static pages are not affected.

In monorepos or when you need to include files outside the app folder, combine `outputFileTracingRoot` with includes:

 next.config.js

```
const path = require('path')

module.exports = {
  // Trace from the monorepo root
  outputFileTracingRoot: path.join(__dirname, '../../'),
  outputFileTracingIncludes: {
    '/route1': ['../shared/assets/**/*'],
  },
}
```

> **Good to know**:
>
>
>
> - Prefer forward slashes (`/`) in patterns for cross-platform compatibility.
> - Keep patterns as narrow as possible to avoid oversized traces (avoid `**/*` at the repo root).

Common include patterns for native/runtime assets:

 next.config.js

```
module.exports = {
  outputFileTracingIncludes: {
    '/*': ['node_modules/sharp/**/*', 'node_modules/aws-crt/dist/bin/**/*'],
  },
}
```

Was this helpful?

supported.

---

# pageExtensions

> Extend the default page extensions used by Next.js when resolving pages in the Pages Router.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)pageExtensionsYou are currently viewing the documentation for Pages Router.

# pageExtensions

Last updated  April 15, 2025

You can extend the default Page extensions (`.tsx`, `.ts`, `.jsx`, `.js`) used by Next.js. Inside `next.config.js`, add the `pageExtensions` config:

next.config.js

```
module.exports = {
  pageExtensions: ['mdx', 'md', 'jsx', 'js', 'tsx', 'ts'],
}
```

Changing these values affects *all* Next.js pages, including the following:

- [proxy.js](https://nextjs.org/docs/pages/api-reference/file-conventions/proxy)
- [instrumentation.js](https://nextjs.org/docs/pages/guides/instrumentation)
- `pages/_document.js`
- `pages/_app.js`
- `pages/api/`

For example, if you reconfigure `.ts` page extensions to `.page.ts`, you would need to rename pages like `proxy.page.ts`, `instrumentation.page.ts`, `_app.page.ts`.

## Including non-page files in thepagesdirectory

You can colocate test files or other files used by components in the `pages` directory. Inside `next.config.js`, add the `pageExtensions` config:

next.config.js

```
module.exports = {
  pageExtensions: ['page.tsx', 'page.ts', 'page.jsx', 'page.js'],
}
```

Then, rename your pages to have a file extension that includes `.page` (e.g. rename `MyPage.tsx` to `MyPage.page.tsx`). Ensure you rename *all* Next.js pages, including the files mentioned above.

Was this helpful?

supported.

---

# poweredByHeader

> Next.js will add the `x-powered-by` header by default. Learn to opt-out of it here.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)poweredByHeaderYou are currently viewing the documentation for Pages Router.

# poweredByHeader

Last updated  April 15, 2025

By default Next.js will add the `x-powered-by` header. To opt-out of it, open `next.config.js` and disable the `poweredByHeader` config:

 next.config.js

```
module.exports = {
  poweredByHeader: false,
}
```

Was this helpful?

supported.

---

# productionBrowserSourceMaps

> Enables browser source map generation during the production build.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)productionBrowserSourceMapsYou are currently viewing the documentation for Pages Router.

# productionBrowserSourceMaps

Last updated  April 15, 2025

Source Maps are enabled by default during development. During production builds, they are disabled to prevent you leaking your source on the client, unless you specifically opt-in with the configuration flag.

Next.js provides a configuration flag you can use to enable browser source map generation during the production build:

 next.config.js

```
module.exports = {
  productionBrowserSourceMaps: true,
}
```

When the `productionBrowserSourceMaps` option is enabled, the source maps will be output in the same directory as the JavaScript files. Next.js will automatically serve these files when requested.

- Adding source maps can increase `next build` time
- Increases memory usage during `next build`

Was this helpful?

supported.

---

# experimental.proxyClientMaxBodySize

> Configure the maximum request body size when using proxy.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)experimental.proxyClientMaxBodySizeYou are currently viewing the documentation for Pages Router.

# experimental.proxyClientMaxBodySize

Last updated  October 17, 2025

When proxy is used, Next.js automatically clones the request body and buffers it in memory to enable multiple reads - both in proxy and the underlying route handler. To prevent excessive memory usage, this configuration option sets a size limit on the buffered body.

By default, the maximum body size is **10MB**. If a request body exceeds this limit, the body will only be buffered up to the limit, and a warning will be logged indicating which route exceeded the limit.

## Options

### String format (recommended)

Specify the size using a human-readable string format:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    proxyClientMaxBodySize: '1mb',
  },
}

export default nextConfig
```

Supported units: `b`, `kb`, `mb`, `gb`

### Number format

Alternatively, specify the size in bytes as a number:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    proxyClientMaxBodySize: 1048576, // 1MB in bytes
  },
}

export default nextConfig
```

## Behavior

When a request body exceeds the configured limit:

1. Next.js will buffer only the first N bytes (up to the limit)
2. A warning will be logged to the console indicating the route that exceeded the limit
3. The request will continue processing normally, but only the partial body will be available
4. The request will **not** fail or return an error to the client

If your application needs to process the full request body, you should either:

- Increase the `proxyClientMaxBodySize` limit
- Handle the partial body gracefully in your application logic

## Example

 proxy.ts

```
import { NextRequest, NextResponse } from 'next/server'

export async function proxy(request: NextRequest) {
  // Next.js automatically buffers the body with the configured size limit
  // You can read the body in proxy...
  const body = await request.text()

  // If the body exceeded the limit, only partial data will be available
  console.log('Body size:', body.length)

  return NextResponse.next()
}
```

 app/api/upload/route.ts

```
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  // ...and the body is still available in your route handler
  const body = await request.text()

  console.log('Body in route handler:', body.length)

  return NextResponse.json({ received: body.length })
}
```

## Good to know

- This setting only applies when proxy is used in your application
- The default limit of 10MB is designed to balance memory usage and typical use cases
- The limit applies per-request, not globally across all concurrent requests
- For applications handling large file uploads, consider increasing the limit accordingly

Was this helpful?

supported.

---

# reactStrictMode

> The complete Next.js runtime is now Strict Mode-compliant, learn how to opt-in

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)reactStrictModeYou are currently viewing the documentation for Pages Router.

# reactStrictMode

Last updated  April 15, 2025

> **Good to know**: Since Next.js 13.5.1, Strict Mode is `true` by default with `app` router, so the above configuration is only necessary for `pages`. You can still disable Strict Mode by setting `reactStrictMode: false`.

> **Suggested**: We strongly suggest you enable Strict Mode in your Next.js application to better prepare your application for the future of React.

React's [Strict Mode](https://react.dev/reference/react/StrictMode) is a development mode only feature for highlighting potential problems in an application. It helps to identify unsafe lifecycles, legacy API usage, and a number of other features.

The Next.js runtime is Strict Mode-compliant. To opt-in to Strict Mode, configure the following option in your `next.config.js`:

 next.config.js

```
module.exports = {
  reactStrictMode: true,
}
```

If you or your team are not ready to use Strict Mode in your entire application, that's OK! You can incrementally migrate on a page-by-page basis using `<React.StrictMode>`.

Was this helpful?

supported.

---

# redirects

> Add redirects to your Next.js app.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)redirectsYou are currently viewing the documentation for Pages Router.

# redirects

Last updated  April 15, 2025

Redirects allow you to redirect an incoming request path to a different destination path.

To use redirects you can use the `redirects` key in `next.config.js`:

 next.config.js

```
module.exports = {
  async redirects() {
    return [
      {
        source: '/about',
        destination: '/',
        permanent: true,
      },
    ]
  },
}
```

`redirects` is an async function that expects an array to be returned holding objects with `source`, `destination`, and `permanent` properties:

- `source` is the incoming request path pattern.
- `destination` is the path you want to route to.
- `permanent` `true` or `false` - if `true` will use the 308 status code which instructs clients/search engines to cache the redirect forever, if `false` will use the 307 status code which is temporary and is not cached.

> **Why does Next.js use 307 and 308?** Traditionally a 302 was used for a temporary redirect, and a 301 for a permanent redirect, but many browsers changed the request method of the redirect to `GET`, regardless of the original method. For example, if the browser made a request to `POST /v1/users` which returned status code `302` with location `/v2/users`, the subsequent request might be `GET /v2/users` instead of the expected `POST /v2/users`. Next.js uses the 307 temporary redirect, and 308 permanent redirect status codes to explicitly preserve the request method used.

- `basePath`: `false` or `undefined` - if false the `basePath` won't be included when matching, can be used for external redirects only.
- `locale`: `false` or `undefined` - whether the locale should not be included when matching.
- `has` is an array of [has objects](#header-cookie-and-query-matching) with the `type`, `key` and `value` properties.
- `missing` is an array of [missing objects](#header-cookie-and-query-matching) with the `type`, `key` and `value` properties.

Redirects are checked before the filesystem which includes pages and `/public` files.

When using the Pages Router, redirects are not applied to client-side routing (`Link`, `router.push`) unless [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) is present and matches the path.

When a redirect is applied, any query values provided in the request will be passed through to the redirect destination. For example, see the following redirect configuration:

```
{
  source: '/old-blog/:path*',
  destination: '/blog/:path*',
  permanent: false
}
```

> **Good to know**: Remember to include the forward slash `/` before the colon `:` in path parameters of the `source` and `destination` paths, otherwise the path will be treated as a literal string and you run the risk of causing infinite redirects.

When `/old-blog/post-1?hello=world` is requested, the client will be redirected to `/blog/post-1?hello=world`.

## Path Matching

Path matches are allowed, for example `/old-blog/:slug` will match `/old-blog/first-post` (no nested paths):

 next.config.js

```
module.exports = {
  async redirects() {
    return [
      {
        source: '/old-blog/:slug',
        destination: '/news/:slug', // Matched parameters can be used in the destination
        permanent: true,
      },
    ]
  },
}
```

The pattern `/old-blog/:slug` matches `/old-blog/first-post` and `/old-blog/post-1` but not `/old-blog/a/b` (no nested paths). Patterns are anchored to the start: `/old-blog/:slug` will not match `/archive/old-blog/first-post`.

You can use modifiers on parameters: `*` (zero or more), `+` (one or more), `?` (zero or one). For example, `/blog/:slug*` matches `/blog`, `/blog/a`, and `/blog/a/b/c`.

Read more details on [path-to-regexp](https://github.com/pillarjs/path-to-regexp) documentation.

### Wildcard Path Matching

To match a wildcard path you can use `*` after a parameter, for example `/blog/:slug*` will match `/blog/a/b/c/d/hello-world`:

 next.config.js

```
module.exports = {
  async redirects() {
    return [
      {
        source: '/blog/:slug*',
        destination: '/news/:slug*', // Matched parameters can be used in the destination
        permanent: true,
      },
    ]
  },
}
```

### Regex Path Matching

To match a regex path you can wrap the regex in parentheses after a parameter, for example `/post/:slug(\\d{1,})` will match `/post/123` but not `/post/abc`:

 next.config.js

```
module.exports = {
  async redirects() {
    return [
      {
        source: '/post/:slug(\\d{1,})',
        destination: '/news/:slug', // Matched parameters can be used in the destination
        permanent: false,
      },
    ]
  },
}
```

The following characters `(`, `)`, `{`, `}`, `:`, `*`, `+`, `?` are used for regex path matching, so when used in the `source` as non-special values they must be escaped by adding `\\` before them:

 next.config.js

```
module.exports = {
  async redirects() {
    return [
      {
        // this will match `/english(default)/something` being requested
        source: '/english\\(default\\)/:slug',
        destination: '/en-us/:slug',
        permanent: false,
      },
    ]
  },
}
```

## Header, Cookie, and Query Matching

To only match a redirect when header, cookie, or query values also match the `has` field or don't match the `missing` field can be used. Both the `source` and all `has` items must match and all `missing` items must not match for the redirect to be applied.

`has` and `missing` items can have the following fields:

- `type`: `String` - must be either `header`, `cookie`, `host`, or `query`.
- `key`: `String` - the key from the selected type to match against.
- `value`: `String` or `undefined` - the value to check for, if undefined any value will match. A regex like string can be used to capture a specific part of the value, e.g. if the value `first-(?<paramName>.*)` is used for `first-second` then `second` will be usable in the destination with `:paramName`.

 next.config.js

```
module.exports = {
  async redirects() {
    return [
      // if the header `x-redirect-me` is present,
      // this redirect will be applied
      {
        source: '/:path((?!another-page$).*)',
        has: [
          {
            type: 'header',
            key: 'x-redirect-me',
          },
        ],
        permanent: false,
        destination: '/another-page',
      },
      // if the header `x-do-not-redirect` is present,
      // this redirect will NOT be applied
      {
        source: '/:path((?!another-page$).*)',
        missing: [
          {
            type: 'header',
            key: 'x-do-not-redirect',
          },
        ],
        permanent: false,
        destination: '/another-page',
      },
      // if the source, query, and cookie are matched,
      // this redirect will be applied
      {
        source: '/specific/:path*',
        has: [
          {
            type: 'query',
            key: 'page',
            // the page value will not be available in the
            // destination since value is provided and doesn't
            // use a named capture group e.g. (?<page>home)
            value: 'home',
          },
          {
            type: 'cookie',
            key: 'authorized',
            value: 'true',
          },
        ],
        permanent: false,
        destination: '/another/:path*',
      },
      // if the header `x-authorized` is present and
      // contains a matching value, this redirect will be applied
      {
        source: '/',
        has: [
          {
            type: 'header',
            key: 'x-authorized',
            value: '(?<authorized>yes|true)',
          },
        ],
        permanent: false,
        destination: '/home?authorized=:authorized',
      },
      // if the host is `example.com`,
      // this redirect will be applied
      {
        source: '/:path((?!another-page$).*)',
        has: [
          {
            type: 'host',
            value: 'example.com',
          },
        ],
        permanent: false,
        destination: '/another-page',
      },
    ]
  },
}
```

### Redirects with basePath support

When leveraging [basePathsupport](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath) with redirects each `source` and `destination` is automatically prefixed with the `basePath` unless you add `basePath: false` to the redirect:

 next.config.js

```
module.exports = {
  basePath: '/docs',

  async redirects() {
    return [
      {
        source: '/with-basePath', // automatically becomes /docs/with-basePath
        destination: '/another', // automatically becomes /docs/another
        permanent: false,
      },
      {
        // does not add /docs since basePath: false is set
        source: '/without-basePath',
        destination: 'https://example.com',
        basePath: false,
        permanent: false,
      },
    ]
  },
}
```

### Redirects with i18n support

When leveraging [i18nsupport](https://nextjs.org/docs/pages/guides/internationalization) with redirects each `source` and `destination` is automatically prefixed to handle the configured `locales` unless you add `locale: false` to the redirect. If `locale: false` is used you must prefix the `source` and `destination` with a locale for it to be matched correctly.

next.config.js

```
module.exports = {
  i18n: {
    locales: ['en', 'fr', 'de'],
    defaultLocale: 'en',
  },

  async redirects() {
    return [
      {
        source: '/with-locale', // automatically handles all locales
        destination: '/another', // automatically passes the locale on
        permanent: false,
      },
      {
        // does not handle locales automatically since locale: false is set
        source: '/nl/with-locale-manual',
        destination: '/nl/another',
        locale: false,
        permanent: false,
      },
      {
        // this matches '/' since `en` is the defaultLocale
        source: '/en',
        destination: '/en/another',
        locale: false,
        permanent: false,
      },
      // it's possible to match all locales even when locale: false is set
      {
        source: '/:locale/page',
        destination: '/en/newpage',
        permanent: false,
        locale: false,
      },
      {
        // this gets converted to /(en|fr|de)/(.*) so will not match the top-level
        // `/` or `/fr` routes like /:path* would
        source: '/(.*)',
        destination: '/another',
        permanent: false,
      },
    ]
  },
}
```

In some rare cases, you might need to assign a custom status code for older HTTP Clients to properly redirect. In these cases, you can use the `statusCode` property instead of the `permanent` property, but not both. To ensure IE11 compatibility, a `Refresh` header is automatically added for the 308 status code.

## Other Redirects

- Inside [API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) and [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route), you can redirect based on the incoming request.
- Inside [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) and [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props), you can redirect specific pages at request-time.

## Version History

| Version | Changes |
| --- | --- |
| v13.3.0 | missingadded. |
| v10.2.0 | hasadded. |
| v9.5.0 | redirectsadded. |

Was this helpful?

supported.

---

# rewrites

> Add rewrites to your Next.js app.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)rewritesYou are currently viewing the documentation for Pages Router.

# rewrites

Last updated  April 15, 2025

Rewrites allow you to map an incoming request path to a different destination path.

Rewrites act as a URL proxy and mask the destination path, making it appear the user hasn't changed their location on the site. In contrast, [redirects](https://nextjs.org/docs/pages/api-reference/config/next-config-js/redirects) will reroute to a new page and show the URL changes.

To use rewrites you can use the `rewrites` key in `next.config.js`:

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/about',
        destination: '/',
      },
    ]
  },
}
```

Rewrites are applied to client-side routing. In the example above, navigating to `<Link href="/about">` will serve content from `/` while keeping the URL as `/about`.

`rewrites` is an async function that expects to return either an array or an object of arrays (see below) holding objects with `source` and `destination` properties:

- `source`: `String` - is the incoming request path pattern.
- `destination`: `String` is the path you want to route to.
- `basePath`: `false` or `undefined` - if false the basePath won't be included when matching, can be used for external rewrites only.
- `locale`: `false` or `undefined` - whether the locale should not be included when matching.
- `has` is an array of [has objects](#header-cookie-and-query-matching) with the `type`, `key` and `value` properties.
- `missing` is an array of [missing objects](#header-cookie-and-query-matching) with the `type`, `key` and `value` properties.

When the `rewrites` function returns an array, rewrites are applied after checking the filesystem (pages and `/public` files) and before dynamic routes. When the `rewrites` function returns an object of arrays with a specific shape, this behavior can be changed and more finely controlled, as of `v10.1` of Next.js:

 next.config.js

```
module.exports = {
  async rewrites() {
    return {
      beforeFiles: [
        // These rewrites are checked after headers/redirects
        // and before all files including _next/public files which
        // allows overriding page files
        {
          source: '/some-page',
          destination: '/somewhere-else',
          has: [{ type: 'query', key: 'overrideMe' }],
        },
      ],
      afterFiles: [
        // These rewrites are checked after pages/public files
        // are checked but before dynamic routes
        {
          source: '/non-existent',
          destination: '/somewhere-else',
        },
      ],
      fallback: [
        // These rewrites are checked after both pages/public files
        // and dynamic routes are checked
        {
          source: '/:path*',
          destination: `https://my-old-site.com/:path*`,
        },
      ],
    }
  },
}
```

> **Good to know**: rewrites in `beforeFiles` do not check the filesystem/dynamic routes immediately after matching a source, they continue until all `beforeFiles` have been checked.

The order Next.js routes are checked is:

1. [headers](https://nextjs.org/docs/pages/api-reference/config/next-config-js/headers) are checked/applied
2. [redirects](https://nextjs.org/docs/pages/api-reference/config/next-config-js/redirects) are checked/applied
3. `beforeFiles` rewrites are checked/applied
4. static files from the [public directory](https://nextjs.org/docs/pages/api-reference/file-conventions/public-folder), `_next/static` files, and non-dynamic pages are checked/served
5. `afterFiles` rewrites are checked/applied, if one of these rewrites is matched we check dynamic routes/static files after each match
6. `fallback` rewrites are checked/applied, these are applied before rendering the 404 page and after dynamic routes/all static assets have been checked. If you use [fallback: true/'blocking'](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-true) in `getStaticPaths`, the fallback `rewrites` defined in your `next.config.js` will *not* be run.

## Rewrite parameters

When using parameters in a rewrite the parameters will be passed in the query by default when none of the parameters are used in the `destination`.

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/old-about/:path*',
        destination: '/about', // The :path parameter isn't used here so will be automatically passed in the query
      },
    ]
  },
}
```

If a parameter is used in the destination none of the parameters will be automatically passed in the query.

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/docs/:path*',
        destination: '/:path*', // The :path parameter is used here so will not be automatically passed in the query
      },
    ]
  },
}
```

You can still pass the parameters manually in the query if one is already used in the destination by specifying the query in the `destination`.

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/:first/:second',
        destination: '/:first?second=:second',
        // Since the :first parameter is used in the destination the :second parameter
        // will not automatically be added in the query although we can manually add it
        // as shown above
      },
    ]
  },
}
```

> **Good to know**: Static pages from [Automatic Static Optimization](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization) or [prerendering](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) params from rewrites will be parsed on the client after hydration and provided in the query.

## Path Matching

Path matches are allowed, for example `/blog/:slug` will match `/blog/first-post` (no nested paths):

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/blog/:slug',
        destination: '/news/:slug', // Matched parameters can be used in the destination
      },
    ]
  },
}
```

The pattern `/blog/:slug` matches `/blog/first-post` and `/blog/post-1` but not `/blog/a/b` (no nested paths). Patterns are anchored to the start: `/blog/:slug` will not match `/archive/blog/first-post`.

You can use modifiers on parameters: `*` (zero or more), `+` (one or more), `?` (zero or one). For example, `/blog/:slug*` matches `/blog`, `/blog/a`, and `/blog/a/b/c`.

Read more details on [path-to-regexp](https://github.com/pillarjs/path-to-regexp) documentation.

### Wildcard Path Matching

To match a wildcard path you can use `*` after a parameter, for example `/blog/:slug*` will match `/blog/a/b/c/d/hello-world`:

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/blog/:slug*',
        destination: '/news/:slug*', // Matched parameters can be used in the destination
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
  async rewrites() {
    return [
      {
        source: '/old-blog/:post(\\d{1,})',
        destination: '/blog/:post', // Matched parameters can be used in the destination
      },
    ]
  },
}
```

The following characters `(`, `)`, `{`, `}`, `[`, `]`, `|`, `\`, `^`, `.`, `:`, `*`, `+`, `-`, `?`, `$` are used for regex path matching, so when used in the `source` as non-special values they must be escaped by adding `\\` before them:

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        // this will match `/english(default)/something` being requested
        source: '/english\\(default\\)/:slug',
        destination: '/en-us/:slug',
      },
    ]
  },
}
```

## Header, Cookie, and Query Matching

To only match a rewrite when header, cookie, or query values also match the `has` field or don't match the `missing` field can be used. Both the `source` and all `has` items must match and all `missing` items must not match for the rewrite to be applied.

`has` and `missing` items can have the following fields:

- `type`: `String` - must be either `header`, `cookie`, `host`, or `query`.
- `key`: `String` - the key from the selected type to match against.
- `value`: `String` or `undefined` - the value to check for, if undefined any value will match. A regex like string can be used to capture a specific part of the value, e.g. if the value `first-(?<paramName>.*)` is used for `first-second` then `second` will be usable in the destination with `:paramName`.

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      // if the header `x-rewrite-me` is present,
      // this rewrite will be applied
      {
        source: '/:path*',
        has: [
          {
            type: 'header',
            key: 'x-rewrite-me',
          },
        ],
        destination: '/another-page',
      },
      // if the header `x-rewrite-me` is not present,
      // this rewrite will be applied
      {
        source: '/:path*',
        missing: [
          {
            type: 'header',
            key: 'x-rewrite-me',
          },
        ],
        destination: '/another-page',
      },
      // if the source, query, and cookie are matched,
      // this rewrite will be applied
      {
        source: '/specific/:path*',
        has: [
          {
            type: 'query',
            key: 'page',
            // the page value will not be available in the
            // destination since value is provided and doesn't
            // use a named capture group e.g. (?<page>home)
            value: 'home',
          },
          {
            type: 'cookie',
            key: 'authorized',
            value: 'true',
          },
        ],
        destination: '/:path*/home',
      },
      // if the header `x-authorized` is present and
      // contains a matching value, this rewrite will be applied
      {
        source: '/:path*',
        has: [
          {
            type: 'header',
            key: 'x-authorized',
            value: '(?<authorized>yes|true)',
          },
        ],
        destination: '/home?authorized=:authorized',
      },
      // if the host is `example.com`,
      // this rewrite will be applied
      {
        source: '/:path*',
        has: [
          {
            type: 'host',
            value: 'example.com',
          },
        ],
        destination: '/another-page',
      },
    ]
  },
}
```

## Rewriting to an external URL

 Examples

- [Using Multiple Zones](https://github.com/vercel/next.js/tree/canary/examples/with-zones)

Rewrites allow you to rewrite to an external URL. This is especially useful for incrementally adopting Next.js. The following is an example rewrite for redirecting the `/blog` route of your main app to an external site.

 next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/blog',
        destination: 'https://example.com/blog',
      },
      {
        source: '/blog/:slug',
        destination: 'https://example.com/blog/:slug', // Matched parameters can be used in the destination
      },
    ]
  },
}
```

If you're using `trailingSlash: true`, you also need to insert a trailing slash in the `source` parameter. If the destination server is also expecting a trailing slash it should be included in the `destination` parameter as well.

 next.config.js

```
module.exports = {
  trailingSlash: true,
  async rewrites() {
    return [
      {
        source: '/blog/',
        destination: 'https://example.com/blog/',
      },
      {
        source: '/blog/:path*/',
        destination: 'https://example.com/blog/:path*/',
      },
    ]
  },
}
```

### Incremental adoption of Next.js

You can also have Next.js fall back to proxying to an existing website after checking all Next.js routes.

This way you don't have to change the rewrites configuration when migrating more pages to Next.js

 next.config.js

```
module.exports = {
  async rewrites() {
    return {
      fallback: [
        {
          source: '/:path*',
          destination: `https://custom-routes-proxying-endpoint.vercel.app/:path*`,
        },
      ],
    }
  },
}
```

### Rewrites with basePath support

When leveraging [basePathsupport](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath) with rewrites each `source` and `destination` is automatically prefixed with the `basePath` unless you add `basePath: false` to the rewrite:

 next.config.js

```
module.exports = {
  basePath: '/docs',

  async rewrites() {
    return [
      {
        source: '/with-basePath', // automatically becomes /docs/with-basePath
        destination: '/another', // automatically becomes /docs/another
      },
      {
        // does not add /docs to /without-basePath since basePath: false is set
        // Note: this can not be used for internal rewrites e.g. `destination: '/another'`
        source: '/without-basePath',
        destination: 'https://example.com',
        basePath: false,
      },
    ]
  },
}
```

### Rewrites with i18n support

When leveraging [i18nsupport](https://nextjs.org/docs/pages/guides/internationalization) with rewrites each `source` and `destination` is automatically prefixed to handle the configured `locales` unless you add `locale: false` to the rewrite. If `locale: false` is used you must prefix the `source` and `destination` with a locale for it to be matched correctly.

next.config.js

```
module.exports = {
  i18n: {
    locales: ['en', 'fr', 'de'],
    defaultLocale: 'en',
  },

  async rewrites() {
    return [
      {
        source: '/with-locale', // automatically handles all locales
        destination: '/another', // automatically passes the locale on
      },
      {
        // does not handle locales automatically since locale: false is set
        source: '/nl/with-locale-manual',
        destination: '/nl/another',
        locale: false,
      },
      {
        // this matches '/' since `en` is the defaultLocale
        source: '/en',
        destination: '/en/another',
        locale: false,
      },
      {
        // it's possible to match all locales even when locale: false is set
        source: '/:locale/api-alias/:path*',
        destination: '/api/:path*',
        locale: false,
      },
      {
        // this gets converted to /(en|fr|de)/(.*) so will not match the top-level
        // `/` or `/fr` routes like /:path* would
        source: '/(.*)',
        destination: '/another',
      },
    ]
  },
}
```

## Version History

| Version | Changes |
| --- | --- |
| v13.3.0 | missingadded. |
| v10.2.0 | hasadded. |
| v9.5.0 | Headers added. |

Was this helpful?

supported.

---

# serverExternalPackages

> Opt-out specific dependencies from the dependency bundling enabled by `bundlePagesRouterDependencies`.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)serverExternalPackagesYou are currently viewing the documentation for Pages Router.

# serverExternalPackages

Last updated  December 5, 2025

Opt-out specific dependencies from being included in the automatic bundling of the [bundlePagesRouterDependencies](https://nextjs.org/docs/pages/api-reference/config/next-config-js/bundlePagesRouterDependencies) option.

These pages will then use native Node.js `require` to resolve the dependency.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  serverExternalPackages: ['@acme/ui'],
}

module.exports = nextConfig
```

Next.js includes a [short list of popular packages](https://github.com/vercel/next.js/blob/canary/packages/next/src/lib/server-external-packages.jsonc) that currently are working on compatibility and automatically opt-ed out:

- `@alinea/generated`
- `@appsignal/nodejs`
- `@aws-sdk/client-s3`
- `@aws-sdk/s3-presigned-post`
- `@blockfrost/blockfrost-js`
- `@highlight-run/node`
- `@huggingface/transformers`
- `@jpg-store/lucid-cardano`
- `@libsql/client`
- `@mikro-orm/core`
- `@mikro-orm/knex`
- `@node-rs/argon2`
- `@node-rs/bcrypt`
- `@prisma/client`
- `@react-pdf/renderer`
- `@sentry/profiling-node`
- `@sparticuz/chromium`
- `@sparticuz/chromium-min`
- `@statsig/statsig-node-core`
- `@swc/core`
- `@xenova/transformers`
- `@zenstackhq/runtime`
- `argon2`
- `autoprefixer`
- `aws-crt`
- `bcrypt`
- `better-sqlite3`
- `canvas`
- `chromadb-default-embed`
- `config`
- `cpu-features`
- `cypress`
- `dd-trace`
- `eslint`
- `express`
- `firebase-admin`
- `htmlrewriter`
- `import-in-the-middle`
- `isolated-vm`
- `jest`
- `jsdom`
- `keyv`
- `libsql`
- `mdx-bundler`
- `mongodb`
- `mongoose`
- `newrelic`
- `next-mdx-remote`
- `next-seo`
- `node-cron`
- `node-pty`
- `node-web-audio-api`
- `onnxruntime-node`
- `oslo`
- `pg`
- `pino`
- `pino-pretty`
- `pino-roll`
- `playwright`
- `playwright-core`
- `postcss`
- `prettier`
- `prisma`
- `puppeteer-core`
- `puppeteer`
- `ravendb`
- `require-in-the-middle`
- `rimraf`
- `sharp`
- `shiki`
- `sqlite3`
- `thread-stream`
- `ts-morph`
- `ts-node`
- `typescript`
- `vscode-oniguruma`
- `webpack`
- `websocket`
- `zeromq`

Was this helpful?

supported.

---

# trailingSlash

> Configure Next.js pages to resolve with or without a trailing slash.

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)trailingSlashYou are currently viewing the documentation for Pages Router.

# trailingSlash

Last updated  April 15, 2025

By default Next.js will redirect URLs with trailing slashes to their counterpart without a trailing slash. For example `/about/` will redirect to `/about`. You can configure this behavior to act the opposite way, where URLs without trailing slashes are redirected to their counterparts with trailing slashes.

Open `next.config.js` and add the `trailingSlash` config:

 next.config.js

```
module.exports = {
  trailingSlash: true,
}
```

With this option set, URLs like `/about` will redirect to `/about/`.

When using `trailingSlash: true`, certain URLs are exceptions and will not have a trailing slash appended:

- Static file URLs, such as files with extensions.
- Any paths under `.well-known/`.

For example, the following URLs will remain unchanged: `/file.txt`, `images/photos/picture.png`, and `.well-known/subfolder/config.json`.

When used with [output: "export"](https://nextjs.org/docs/app/guides/static-exports) configuration, the `/about` page will output `/about/index.html` (instead of the default `/about.html`).

## Version History

| Version | Changes |
| --- | --- |
| v9.5.0 | trailingSlashadded. |

Was this helpful?

supported.

---

# transpilePackages

> Automatically transpile and bundle dependencies from local packages (like monorepos) or from external dependencies (`node_modules`).

[Configuration](https://nextjs.org/docs/pages/api-reference/config)[next.config.js Options](https://nextjs.org/docs/pages/api-reference/config/next-config-js)transpilePackagesYou are currently viewing the documentation for Pages Router.

# transpilePackages

Last updated  April 15, 2025

Next.js can automatically transpile and bundle dependencies from local packages (like monorepos) or from external dependencies (`node_modules`). This replaces the `next-transpile-modules` package.

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['package-name'],
}

module.exports = nextConfig
```

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | transpilePackagesadded. |

Was this helpful?

supported.
