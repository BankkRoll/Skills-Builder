# reactCompiler and more

# reactCompiler

> Enable the React Compiler to automatically optimize component rendering.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)reactCompiler

# reactCompiler

Last updated  October 23, 2025

Next.js includes support for the [React Compiler](https://react.dev/learn/react-compiler/introduction), a tool designed to improve performance by automatically optimizing component rendering. This reduces the need for manual memoization using `useMemo` and `useCallback`.

Next.js includes a custom performance optimization written in SWC that makes the React Compiler more efficient. Instead of running the compiler on every file, Next.js analyzes your project and only applies the React Compiler to relevant files. This avoids unnecessary work and leads to faster builds compared to using the Babel plugin on its own.

## How It Works

The React Compiler runs through a Babel plugin. To keep builds fast, Next.js uses a custom SWC optimization that only applies the React Compiler to relevant files—like those with JSX or React Hooks.

This avoids compiling everything and keeps the performance cost minimal. You may still see slightly slower builds compared to the default Rust-based compiler, but the impact is small and localized.

To use it, install the `babel-plugin-react-compiler`:

 Terminal

```
npm install -D babel-plugin-react-compiler
```

Then, add `reactCompiler` option in `next.config.js`:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactCompiler: true,
}

export default nextConfig
```

## Annotations

You can configure the compiler to run in "opt-in" mode as follows:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactCompiler: {
    compilationMode: 'annotation',
  },
}

export default nextConfig
```

Then, you can annotate specific components or hooks with the `"use memo"` directive from React to opt-in:

 app/page.tsxJavaScriptTypeScript

```
export default function Page() {
  'use memo'
  // ...
}
```

> **Note:** You can also use the `"use no memo"` directive from React for the opposite effect, to opt-out a component or hook.

Was this helpful?

supported.

---

# reactMaxHeadersLength

> The maximum length of the headers that are emitted by React and added to the response.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)reactMaxHeadersLength

# reactMaxHeadersLength

Last updated  June 16, 2025

During static rendering, React can emit headers that can be added to the response. These can be used to improve performance by allowing the browser to preload resources like fonts, scripts, and stylesheets. The default value is `6000`, but you can override this value by configuring the `reactMaxHeadersLength` option in `next.config.js`:

 next.config.js

```
module.exports = {
  reactMaxHeadersLength: 1000,
}
```

> **Good to know**: This option is only available in App Router.

Depending on the type of proxy between the browser and the server, the headers can be truncated. For example, if you are using a reverse proxy that doesn't support long headers, you should set a lower value to ensure that the headers are not truncated.

Was this helpful?

supported.

---

# reactStrictMode

> The complete Next.js runtime is now Strict Mode-compliant, learn how to opt-in

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)reactStrictMode

# reactStrictMode

Last updated  June 16, 2025

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

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)redirects

# redirects

Last updated  November 12, 2025

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

When implementing redirects with internationalization in the App Router, you can include locales in `next.config.js` redirects, but only as hardcoded paths.

For dynamic or per-request locale handling, use [dynamic route segments and proxy](https://nextjs.org/docs/app/guides/internationalization), which can redirect based on the user's preferred language.

next.config.js

```
module.exports = {
  async redirects() {
    return [
      {
        // Manually handle locale prefixes for App Router
        source: '/en/old-path',
        destination: '/en/new-path',
        permanent: false,
      },
      {
        // Redirect for all locales using a parameter
        source: '/:locale/old-path',
        destination: '/:locale/new-path',
        permanent: false,
      },
      {
        // Redirect from one locale to another
        source: '/de/old-path',
        destination: '/en/new-path',
        permanent: false,
      },
      {
        // Catch-all redirect for multiple locales
        source: '/:locale(en|fr|de)/:path*',
        destination: '/:locale/new-section/:path*',
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

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)rewrites

# rewrites

Last updated  November 4, 2025

Rewrites allow you to map an incoming request path to a different destination path.

Rewrites act as a URL proxy and mask the destination path, making it appear the user hasn't changed their location on the site. In contrast, [redirects](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects) will reroute to a new page and show the URL changes.

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

1. [headers](https://nextjs.org/docs/app/api-reference/config/next-config-js/headers) are checked/applied
2. [redirects](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects) are checked/applied
3. [proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)
4. `beforeFiles` rewrites are checked/applied
5. static files from the [public directory](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder), `_next/static` files, and non-dynamic pages are checked/served
6. `afterFiles` rewrites are checked/applied, if one of these rewrites is matched we check dynamic routes/static files after each match
7. `fallback` rewrites are checked/applied, these are applied before rendering the 404 page and after dynamic routes/all static assets have been checked. If you use [fallback: true/'blocking'](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-true) in `getStaticPaths`, the fallback `rewrites` defined in your `next.config.js` will *not* be run.

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

## Version History

| Version | Changes |
| --- | --- |
| v13.3.0 | missingadded. |
| v10.2.0 | hasadded. |
| v9.5.0 | Headers added. |

Was this helpful?

supported.

---

# sassOptions

> Configure Sass options.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)sassOptions

# sassOptions

Last updated  October 19, 2025

`sassOptions` allow you to configure the Sass compiler.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const sassOptions = {
  additionalData: `
    $var: red;
  `,
}

const nextConfig: NextConfig = {
  sassOptions: {
    ...sassOptions,
    implementation: 'sass-embedded',
  },
}

export default nextConfig
```

> **Good to know:**
>
>
>
> - `sassOptions` are not typed outside of `implementation` because Next.js does not maintain the other possible properties.
> - The `functions` property for defining custom Sass functions is only supported with webpack. When using Turbopack, custom Sass functions are not available because Turbopack's Rust-based architecture cannot directly execute JavaScript functions passed through this option.

Was this helpful?

supported.

---

# serverActions

> Configure Server Actions behavior in your Next.js application.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)serverActions

# serverActions

Last updated  June 16, 2025

Options for configuring Server Actions behavior in your Next.js application.

## allowedOrigins

A list of extra safe origin domains from which Server Actions can be invoked. Next.js compares the origin of a Server Action request with the host domain, ensuring they match to prevent CSRF attacks. If not provided, only the same origin is allowed.

 next.config.js

```
/** @type {import('next').NextConfig} */

module.exports = {
  experimental: {
    serverActions: {
      allowedOrigins: ['my-proxy.com', '*.my-proxy.com'],
    },
  },
}
```

## bodySizeLimit

By default, the maximum size of the request body sent to a Server Action is 1MB, to prevent the consumption of excessive server resources in parsing large amounts of data, as well as potential DDoS attacks.

However, you can configure this limit using the `serverActions.bodySizeLimit` option. It can take the number of bytes or any string format supported by bytes, for example `1000`, `'500kb'` or `'3mb'`.

 next.config.js

```
/** @type {import('next').NextConfig} */

module.exports = {
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
}
```

## Enabling Server Actions (v13)

Server Actions became a stable feature in Next.js 14, and are enabled by default. However, if you are using an earlier version of Next.js, you can enable them by setting `experimental.serverActions` to `true`.

 next.config.js

```
/** @type {import('next').NextConfig} */
const config = {
  experimental: {
    serverActions: true,
  },
}

module.exports = config
```

Was this helpful?

supported.

---

# serverComponentsHmrCache

> Configure whether fetch responses in Server Components are cached across HMR refresh requests.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)serverComponentsHmrCache

# serverComponentsHmrCache

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

The experimental `serverComponentsHmrCache` option allows you to cache `fetch` responses in Server Components across Hot Module Replacement (HMR) refreshes in local development. This results in faster responses and reduced costs for billed API calls.

By default, the HMR cache applies to all `fetch` requests, including those with the `cache: 'no-store'` option. This means uncached requests will not show fresh data between HMR refreshes. However, the cache will be cleared on navigation or full-page reloads.

You can disable the HMR cache by setting `serverComponentsHmrCache` to `false` in your `next.config.js` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    serverComponentsHmrCache: false, // defaults to true
  },
}

export default nextConfig
```

> **Good to know:** For better observability, we recommend using the [logging.fetches](https://nextjs.org/docs/app/api-reference/config/next-config-js/logging) option which logs fetch cache hits and misses in the console during development.

Was this helpful?

supported.

---

# serverExternalPackages

> Opt-out specific dependencies from the Server Components bundling and use native Node.js `require`.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)serverExternalPackages

# serverExternalPackages

Last updated  December 5, 2025

Dependencies used inside [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) and [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) will automatically be bundled by Next.js.

If a dependency is using Node.js specific features, you can choose to opt-out specific dependencies from the Server Components bundling and use native Node.js `require`.

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

| Version | Changes |
| --- | --- |
| v15.0.0 | Moved from experimental to stable. Renamed fromserverComponentsExternalPackagestoserverExternalPackages |

Was this helpful?

supported.

---

# staleTimes

> Learn how to override the invalidation time of the Client Router Cache.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)staleTimes

# staleTimes

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

`staleTimes` is an experimental feature that enables caching of page segments in the [client-side router cache](https://nextjs.org/docs/app/guides/caching#client-side-router-cache).

You can enable this experimental feature and provide custom revalidation times by setting the experimental `staleTimes` flag:

 next.config.js

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    staleTimes: {
      dynamic: 30,
      static: 180,
    },
  },
}

module.exports = nextConfig
```

The `static` and `dynamic` properties correspond with the time period (in seconds) based on different types of [link prefetching](https://nextjs.org/docs/app/api-reference/components/link#prefetch).

- The `dynamic` property is used when the page is neither statically generated nor fully prefetched (e.g. with `prefetch={true}`).
  - Default: 0 seconds (not cached)
- The `static` property is used for statically generated pages, or when the `prefetch` prop on `Link` is set to `true`, or when calling [router.prefetch](https://nextjs.org/docs/app/guides/caching#routerprefetch).
  - Default: 5 minutes

> **Good to know:**
>
>
>
> - [Loading boundaries](https://nextjs.org/docs/app/api-reference/file-conventions/loading) are considered reusable for the `static` period defined in this configuration.
> - This doesn't affect [partial rendering](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions), **meaning shared layouts won't automatically be refetched on every navigation, only the page segment that changes.**
> - This doesn't change [back/forward caching](https://nextjs.org/docs/app/guides/caching#client-side-router-cache) behavior to prevent layout shift and to prevent losing the browser scroll position.

You can learn more about the Client Router Cache [here](https://nextjs.org/docs/app/guides/caching#client-side-router-cache).

### Version History

| Version | Changes |
| --- | --- |
| v15.0.0 | ThedynamicstaleTimesdefault changed from 30s to 0s. |
| v14.2.0 | ExperimentalstaleTimesintroduced. |

Was this helpful?

supported.

---

# staticGeneration*

> Learn how to configure static generation in your Next.js application.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)staticGeneration*

# staticGeneration*

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

The `staticGeneration*` options allow you to configure the Static Generation process for advanced use cases.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    staticGenerationRetryCount: 1,
    staticGenerationMaxConcurrency: 8,
    staticGenerationMinPagesPerWorker: 25,
  },
}

export default nextConfig
```

## Config Options

The following options are available:

- `staticGenerationRetryCount`: The number of times to retry a failed page generation before failing the build.
- `staticGenerationMaxConcurrency`: The maximum number of pages to be processed per worker.
- `staticGenerationMinPagesPerWorker`: The minimum number of pages to be processed before starting a new worker.

Was this helpful?

supported.

---

# taint

> Enable tainting Objects and Values.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)taint

# taint

This feature is currently experimental and subject to change, it's not recommended for production. Try it out and share your feedback on  [GitHub](https://github.com/vercel/next.js/issues).Last updated  June 16, 2025

## Usage

The `taint` option enables support for experimental React APIs for tainting objects and values. This feature helps prevent sensitive data from being accidentally passed to the client. When enabled, you can use:

- [experimental_taintObjectReference](https://react.dev/reference/react/experimental_taintObjectReference) taint objects references.
- [experimental_taintUniqueValue](https://react.dev/reference/react/experimental_taintUniqueValue) to taint unique values.

> **Good to know**: Activating this flag also enables the React `experimental` channel for `app` directory.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    taint: true,
  },
}

export default nextConfig
```

> **Warning:** Do not rely on the taint API as your only mechanism to prevent exposing sensitive data to the client. See our [security recommendations](https://nextjs.org/blog/security-nextjs-server-components-actions).

The taint APIs allows you to be defensive, by declaratively and explicitly marking data that is not allowed to pass through the Server-Client boundary. When an object or value, is passed through the Server-Client boundary, React throws an error.

This is helpful for cases where:

- The methods to read data are out of your control
- You have to work with sensitive data shapes not defined by you
- Sensitive data is accessed during Server Component rendering

It is recommended to model your data and APIs so that sensitive data is not returned to contexts where it is not needed.

## Caveats

- Tainting can only keep track of objects by reference. Copying an object creates an untainted version, which loses all guarantees given by the API. You'll need to taint the copy.
- Tainting cannot keep track of data derived from a tainted value. You also need to taint the derived value.
- Values are tainted for as long as their lifetime reference is within scope. See the [experimental_taintUniqueValueparameters reference](https://react.dev/reference/react/experimental_taintUniqueValue#parameters), for more information.

## Examples

### Tainting an object reference

In this case, the `getUserDetails` function returns data about a given user. We taint the user object reference, so that it cannot cross a Server-Client boundary. For example, assuming `UserCard` is a Client Component.

```
import { experimental_taintObjectReference } from 'react'

function getUserDetails(id: string): UserDetails {
  const user = await db.queryUserById(id)

  experimental_taintObjectReference(
    'Do not use the entire user info object. Instead, select only the fields you need.',
    user
  )

  return user
}
```

We can still access individual fields from the tainted `userDetails` object.

```
export async function ContactPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const userDetails = await getUserDetails(id)

  return (
    <UserCard
      firstName={userDetails.firstName}
      lastName={userDetails.lastName}
    />
  )
}
```

Now, passing the entire object to the Client Component will throw an error.

```
export async function ContactPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const userDetails = await getUserDetails(id)

  // Throws an error
  return <UserCard user={userDetails} />
}
```

### Tainting a unique value

In this case, we can access the server configuration by awaiting calls to `config.getConfigDetails`. However, the system configuration contains the `SERVICE_API_KEY` that we don't want to expose to clients.

We can taint the `config.SERVICE_API_KEY` value.

```
import { experimental_taintUniqueValue } from 'react'

function getSystemConfig(): SystemConfig {
  const config = await config.getConfigDetails()

  experimental_taintUniqueValue(
    'Do not pass configuration tokens to the client',
    config,
    config.SERVICE_API_KEY
  )

  return config
}
```

We can still access other properties of the `systemConfig` object.

```
export async function Dashboard() {
  const systemConfig = await getSystemConfig()

  return <ClientDashboard version={systemConfig.SERVICE_API_VERSION} />
}
```

However, passing `SERVICE_API_KEY` to `ClientDashboard` throws an error.

```
export async function Dashboard() {
  const systemConfig = await getSystemConfig()
  // Someone makes a mistake in a PR
  const version = systemConfig.SERVICE_API_KEY

  return <ClientDashboard version={version} />
}
```

Note that, even though, `systemConfig.SERVICE_API_KEY` is reassigned to a new variable. Passing it to a Client Component still throws an error.

Whereas, a value derived from a tainted unique value, will be exposed to the client.

```
export async function Dashboard() {
  const systemConfig = await getSystemConfig()
  // Someone makes a mistake in a PR
  const version = `version::${systemConfig.SERVICE_API_KEY}`

  return <ClientDashboard version={version} />
}
```

A better approach is to remove `SERVICE_API_KEY` from the data returned by `getSystemConfig`.

Was this helpful?

supported.

---

# trailingSlash

> Configure Next.js pages to resolve with or without a trailing slash.

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)trailingSlash

# trailingSlash

Last updated  June 16, 2025

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

[Configuration](https://nextjs.org/docs/app/api-reference/config)[next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js)transpilePackages

# transpilePackages

Last updated  June 16, 2025

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
