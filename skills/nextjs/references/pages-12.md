# API Routes and more

# API Routes

> Next.js supports API Routes, which allow you to build your API without leaving your Next.js app. Learn how it works here.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Routing](https://nextjs.org/docs/pages/building-your-application/routing)API RoutesYou are currently viewing the documentation for Pages Router.

# API Routes

Last updated  October 17, 2025Examples

- [API Routes Request Helpers](https://github.com/vercel/next.js/tree/canary/examples/api-routes-proxy)
- [API Routes with GraphQL](https://github.com/vercel/next.js/tree/canary/examples/api-routes-graphql)
- [API Routes with REST](https://github.com/vercel/next.js/tree/canary/examples/api-routes-rest)
- [API Routes with CORS](https://github.com/vercel/next.js/tree/canary/examples/api-routes-cors)

> **Good to know**: If you are using the App Router, you can use [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) or [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) instead of API Routes.

API routes provide a solution to build a **public API** with Next.js.

Any file inside the folder `pages/api` is mapped to `/api/*` and will be treated as an API endpoint instead of a `page`. They are server-side only bundles and won't increase your client-side bundle size.

For example, the following API route returns a JSON response with a status code of `200`:

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
  res.status(200).json({ message: 'Hello from Next.js!' })
}
```

> **Good to know**:
>
>
>
> - API Routes [do not specify CORS headers](https://developer.mozilla.org/docs/Web/HTTP/CORS), meaning they are **same-origin only** by default. You can customize such behavior by wrapping the request handler with the [CORS request helpers](https://github.com/vercel/next.js/tree/canary/examples/api-routes-cors).

- API Routes can't be used with [static exports](https://nextjs.org/docs/pages/guides/static-exports). However, [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) in the App Router can.
  > - API Routes will be affected by [pageExtensionsconfiguration](https://nextjs.org/docs/pages/api-reference/config/next-config-js/pageExtensions) in `next.config.js`.

## Parameters

```
export default function handler(req: NextApiRequest, res: NextApiResponse) {
  // ...
}
```

- `req`: An instance of [http.IncomingMessage](https://nodejs.org/api/http.html#class-httpincomingmessage)
- `res`: An instance of [http.ServerResponse](https://nodejs.org/api/http.html#class-httpserverresponse)

## HTTP Methods

To handle different HTTP methods in an API route, you can use `req.method` in your request handler, like so:

 pages/api/hello.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    // Process a POST request
  } else {
    // Handle any other HTTP method
  }
}
```

## Request Helpers

API Routes provide built-in request helpers which parse the incoming request (`req`):

- `req.cookies` - An object containing the cookies sent by the request. Defaults to `{}`
- `req.query` - An object containing the [query string](https://en.wikipedia.org/wiki/Query_string). Defaults to `{}`
- `req.body` - An object containing the body parsed by `content-type`, or `null` if no body was sent

### Custom config

Every API Route can export a `config` object to change the default configuration, which is the following:

```
export const config = {
  api: {
    bodyParser: {
      sizeLimit: '1mb',
    },
  },
  // Specifies the maximum allowed duration for this function to execute (in seconds)
  maxDuration: 5,
}
```

`bodyParser` is automatically enabled. If you want to consume the body as a `Stream` or with [raw-body](https://www.npmjs.com/package/raw-body), you can set this to `false`.

One use case for disabling the automatic `bodyParsing` is to allow you to verify the raw body of a **webhook** request, for example [from GitHub](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks#validating-payloads-from-github).

```
export const config = {
  api: {
    bodyParser: false,
  },
}
```

`bodyParser.sizeLimit` is the maximum size allowed for the parsed body, in any format supported by [bytes](https://github.com/visionmedia/bytes.js), like so:

```
export const config = {
  api: {
    bodyParser: {
      sizeLimit: '500kb',
    },
  },
}
```

`externalResolver` is an explicit flag that tells the server that this route is being handled by an external resolver like *express* or *connect*. Enabling this option disables warnings for unresolved requests.

```
export const config = {
  api: {
    externalResolver: true,
  },
}
```

`responseLimit` is automatically enabled, warning when an API Routes' response body is over 4MB.

If you are not using Next.js in a serverless environment, and understand the performance implications of not using a CDN or dedicated media host, you can set this limit to `false`.

```
export const config = {
  api: {
    responseLimit: false,
  },
}
```

`responseLimit` can also take the number of bytes or any string format supported by `bytes`, for example `1000`, `'500kb'` or `'3mb'`.
This value will be the maximum response size before a warning is displayed. Default is 4MB. (see above)

```
export const config = {
  api: {
    responseLimit: '8mb',
  },
}
```

## Response Helpers

The [Server Response object](https://nodejs.org/api/http.html#http_class_http_serverresponse), (often abbreviated as `res`) includes a set of Express.js-like helper methods to improve the developer experience and increase the speed of creating new API endpoints.

The included helpers are:

- `res.status(code)` - A function to set the status code. `code` must be a valid [HTTP status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)
- `res.json(body)` - Sends a JSON response. `body` must be a [serializable object](https://developer.mozilla.org/docs/Glossary/Serialization)
- `res.send(body)` - Sends the HTTP response. `body` can be a `string`, an `object` or a `Buffer`
- `res.redirect([status,] path)` - Redirects to a specified path or URL. `status` must be a valid [HTTP status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). If not specified, `status` defaults to "307" "Temporary redirect".
- `res.revalidate(urlPath)` - [Revalidate a page on demand](https://nextjs.org/docs/pages/guides/incremental-static-regeneration#on-demand-revalidation-with-revalidatepath) using `getStaticProps`. `urlPath` must be a `string`.

### Setting the status code of a response

When sending a response back to the client, you can set the status code of the response.

The following example sets the status code of the response to `200` (`OK`) and returns a `message` property with the value of `Hello from Next.js!` as a JSON response:

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
  res.status(200).json({ message: 'Hello from Next.js!' })
}
```

### Sending a JSON response

When sending a response back to the client you can send a JSON response, this must be a [serializable object](https://developer.mozilla.org/docs/Glossary/Serialization).
In a real world application you might want to let the client know the status of the request depending on the result of the requested endpoint.

The following example sends a JSON response with the status code `200` (`OK`) and the result of the async operation. It's contained in a try catch block to handle any errors that may occur, with the appropriate status code and error message caught and sent back to the client:

 pages/api/hello.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const result = await someAsyncOperation()
    res.status(200).json({ result })
  } catch (err) {
    res.status(500).json({ error: 'failed to load data' })
  }
}
```

### Sending a HTTP response

Sending an HTTP response works the same way as when sending a JSON response. The only difference is that the response body can be a `string`, an `object` or a `Buffer`.

The following example sends a HTTP response with the status code `200` (`OK`) and the result of the async operation.

 pages/api/hello.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const result = await someAsyncOperation()
    res.status(200).send({ result })
  } catch (err) {
    res.status(500).send({ error: 'failed to fetch data' })
  }
}
```

### Redirects to a specified path or URL

Taking a form as an example, you may want to redirect your client to a specified path or URL once they have submitted the form.

The following example redirects the client to the `/` path if the form is successfully submitted:

 pages/api/hello.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { name, message } = req.body

  try {
    await handleFormInputAsync({ name, message })
    res.redirect(307, '/')
  } catch (err) {
    res.status(500).send({ error: 'Failed to fetch data' })
  }
}
```

### Adding TypeScript types

You can make your API Routes more type-safe by importing the `NextApiRequest` and `NextApiResponse` types from `next`, in addition to those, you can also type your response data:

```
import type { NextApiRequest, NextApiResponse } from 'next'

type ResponseData = {
  message: string
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  res.status(200).json({ message: 'Hello from Next.js!' })
}
```

> **Good to know**: The body of `NextApiRequest` is `any` because the client may include any payload. You should validate the type/shape of the body at runtime before using it.

## Dynamic API Routes

API Routes support [dynamic routes](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes), and follow the same file naming rules used for `pages/`.

 pages/api/post/[pid].tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { pid } = req.query
  res.end(`Post: ${pid}`)
}
```

Now, a request to `/api/post/abc` will respond with the text: `Post: abc`.

### Catch all API routes

API Routes can be extended to catch all paths by adding three dots (`...`) inside the brackets. For example:

- `pages/api/post/[...slug].js` matches `/api/post/a`, but also `/api/post/a/b`, `/api/post/a/b/c` and so on.

> **Good to know**: You can use names other than `slug`, such as: `[...param]`

Matched parameters will be sent as a query parameter (`slug` in the example) to the page, and it will always be an array, so, the path `/api/post/a` will have the following `query` object:

```
{ "slug": ["a"] }
```

And in the case of `/api/post/a/b`, and any other matching path, new parameters will be added to the array, like so:

```
{ "slug": ["a", "b"] }
```

For example:

 pages/api/post/[...slug].tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { slug } = req.query
  res.end(`Post: ${slug.join(', ')}`)
}
```

Now, a request to `/api/post/a/b/c` will respond with the text: `Post: a, b, c`.

### Optional catch all API routes

Catch all routes can be made optional by including the parameter in double brackets (`[[...slug]]`).

For example, `pages/api/post/[[...slug]].js` will match `/api/post`, `/api/post/a`, `/api/post/a/b`, and so on.

The main difference between catch all and optional catch all routes is that with optional, the route without the parameter is also matched (`/api/post` in the example above).

The `query` objects are as follows:

```
{ } // GET `/api/post` (empty object)
{ "slug": ["a"] } // `GET /api/post/a` (single-element array)
{ "slug": ["a", "b"] } // `GET /api/post/a/b` (multi-element array)
```

### Caveats

- Predefined API routes take precedence over dynamic API routes, and dynamic API routes over catch all API routes. Take a look at the following examples:
  - `pages/api/post/create.js` - Will match `/api/post/create`
  - `pages/api/post/[pid].js` - Will match `/api/post/1`, `/api/post/abc`, etc. But not `/api/post/create`
  - `pages/api/post/[...slug].js` - Will match `/api/post/1/2`, `/api/post/a/b/c`, etc. But not `/api/post/create`, `/api/post/abc`

## Streaming responses

While the Pages Router does support streaming responses with API Routes, we recommend incrementally adopting the App Router and using [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) if you are on Next.js 14+.

Here's how you can stream a response from an API Route with `writeHead`:

 pages/api/hello.tsJavaScriptTypeScript

```
import { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-store',
  })
  let i = 0
  while (i < 10) {
    res.write(`data: ${i}\n\n`)
    i++
    await new Promise((resolve) => setTimeout(resolve, 1000))
  }
  res.end()
}
```

Was this helpful?

supported.

---

# Custom App

> Control page initialization and add a layout that persists for all pages by overriding the default App component used by Next.js.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Routing](https://nextjs.org/docs/pages/building-your-application/routing)Custom AppYou are currently viewing the documentation for Pages Router.

# Custom App

Last updated  May 27, 2025

Next.js uses the `App` component to initialize pages. You can override it and control the page initialization and:

- Create a shared layout between page changes
- Inject additional data into pages
- [Add global CSS](https://nextjs.org/docs/app/getting-started/css)

## Usage

To override the default `App`, create the file `pages/_app` as shown below:

 pages/_app.tsxJavaScriptTypeScript

```
import type { AppProps } from 'next/app'

export default function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
```

The `Component` prop is the active `page`, so whenever you navigate between routes, `Component` will change to the new `page`. Therefore, any props you send to `Component` will be received by the `page`.

`pageProps` is an object with the initial props that were preloaded for your page by one of our [data fetching methods](https://nextjs.org/docs/pages/building-your-application/data-fetching), otherwise it's an empty object.

> **Good to know**:
>
>
>
> - If your app is running and you added a custom `App`, you'll need to restart the development server. Only required if `pages/_app.js` didn't exist before.
> - `App` does not support Next.js [Data Fetching methods](https://nextjs.org/docs/pages/building-your-application/data-fetching) like [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) or [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props).

## getInitialPropswithApp

Using [getInitialProps](https://nextjs.org/docs/pages/api-reference/functions/get-initial-props) in `App` will disable [Automatic Static Optimization](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization) for pages without [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props).

**We do not recommend using this pattern.** Instead, consider [incrementally adopting](https://nextjs.org/docs/app/guides/migrating/app-router-migration) the App Router, which allows you to more easily fetch data for pages and layouts.

 pages/_app.tsxJavaScriptTypeScript

```
import App, { AppContext, AppInitialProps, AppProps } from 'next/app'

type AppOwnProps = { example: string }

export default function MyApp({
  Component,
  pageProps,
  example,
}: AppProps & AppOwnProps) {
  return (
    <>
      <p>Data: {example}</p>
      <Component {...pageProps} />
    </>
  )
}

MyApp.getInitialProps = async (
  context: AppContext
): Promise<AppOwnProps & AppInitialProps> => {
  const ctx = await App.getInitialProps(context)

  return { ...ctx, example: 'data' }
}
```

Was this helpful?

supported.

---

# Custom Document

> Extend the default document markup added by Next.js.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Routing](https://nextjs.org/docs/pages/building-your-application/routing)Custom DocumentYou are currently viewing the documentation for Pages Router.

# Custom Document

Last updated  May 27, 2025

A custom `Document` can update the `<html>` and `<body>` tags used to render a [Page](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts).

To override the default `Document`, create the file `pages/_document` as shown below:

 pages/_document.tsxJavaScriptTypeScript

```
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

> **Good to know**:
>
>
>
> - `_document` is only rendered on the server, so event handlers like `onClick` cannot be used in this file.
> - `<Html>`, `<Head />`, `<Main />` and `<NextScript />` are required for the page to be properly rendered.

## Caveats

- The `<Head />` component used in `_document` is not the same as [next/head](https://nextjs.org/docs/pages/api-reference/components/head). The `<Head />` component used here should only be used for any `<head>` code that is common for all pages. For all other cases, such as `<title>` tags, we recommend using [next/head](https://nextjs.org/docs/pages/api-reference/components/head) in your pages or components.
- React components outside of `<Main />` will not be initialized by the browser. Do *not* add application logic here or custom CSS (like `styled-jsx`). If you need shared components in all your pages (like a menu or a toolbar), read [Layouts](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts#layout-pattern) instead.
- `Document` currently does not support Next.js [Data Fetching methods](https://nextjs.org/docs/pages/building-your-application/data-fetching) like [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) or [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props).

## CustomizingrenderPage

Customizing `renderPage` is advanced and only needed for libraries like CSS-in-JS to support server-side rendering. This is not needed for built-in `styled-jsx` support.

**We do not recommend using this pattern.** Instead, consider [incrementally adopting](https://nextjs.org/docs/app/guides/migrating/app-router-migration) the App Router, which allows you to more easily fetch data for pages and layouts.

 pages/_document.tsxJavaScriptTypeScript

```
import Document, {
  Html,
  Head,
  Main,
  NextScript,
  DocumentContext,
  DocumentInitialProps,
} from 'next/document'

class MyDocument extends Document {
  static async getInitialProps(
    ctx: DocumentContext
  ): Promise<DocumentInitialProps> {
    const originalRenderPage = ctx.renderPage

    // Run the React rendering logic synchronously
    ctx.renderPage = () =>
      originalRenderPage({
        // Useful for wrapping the whole react tree
        enhanceApp: (App) => App,
        // Useful for wrapping in a per-page basis
        enhanceComponent: (Component) => Component,
      })

    // Run the parent `getInitialProps`, it now includes the custom `renderPage`
    const initialProps = await Document.getInitialProps(ctx)

    return initialProps
  }

  render() {
    return (
      <Html lang="en">
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

> **Good to know**:
>
>
>
> - `getInitialProps` in `_document` is not called during client-side transitions.
> - The `ctx` object for `_document` is equivalent to the one received in [getInitialProps](https://nextjs.org/docs/pages/api-reference/functions/get-initial-props#context-object), with the addition of `renderPage`.

Was this helpful?

supported.

---

# Custom Errors

> Override and extend the built-in Error page to handle custom errors.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Routing](https://nextjs.org/docs/pages/building-your-application/routing)Custom ErrorsYou are currently viewing the documentation for Pages Router.

# Custom Errors

Last updated  April 24, 2025

## 404 Page

A 404 page may be accessed very often. Server-rendering an error page for every visit increases the load of the Next.js server. This can result in increased costs and slow experiences.

To avoid the above pitfalls, Next.js provides a static 404 page by default without having to add any additional files.

### Customizing The 404 Page

To create a custom 404 page you can create a `pages/404.js` file. This file is statically generated at build time.

 pages/404.js

```
export default function Custom404() {
  return <h1>404 - Page Not Found</h1>
}
```

> **Good to know**: You can use [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) inside this page if you need to fetch data at build time.

## 500 Page

Server-rendering an error page for every visit adds complexity to responding to errors. To help users get responses to errors as fast as possible, Next.js provides a static 500 page by default without having to add any additional files.

### Customizing The 500 Page

To customize the 500 page you can create a `pages/500.js` file. This file is statically generated at build time.

 pages/500.js

```
export default function Custom500() {
  return <h1>500 - Server-side error occurred</h1>
}
```

> **Good to know**: You can use [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) inside this page if you need to fetch data at build time.

### More Advanced Error Page Customizing

500 errors are handled both client-side and server-side by the `Error` component. If you wish to override it, define the file `pages/_error.js` and add the following code:

```
function Error({ statusCode }) {
  return (
    <p>
      {statusCode
        ? `An error ${statusCode} occurred on server`
        : 'An error occurred on client'}
    </p>
  )
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404
  return { statusCode }
}

export default Error
```

> `pages/_error.js` is only used in production. In development you’ll get an error with the call stack to know where the error originated from.

### Reusing the built-in error page

If you want to render the built-in error page you can by importing the `Error` component:

```
import Error from 'next/error'

export async function getServerSideProps() {
  const res = await fetch('https://api.github.com/repos/vercel/next.js')
  const errorCode = res.ok ? false : res.status
  const json = await res.json()

  return {
    props: { errorCode, stars: json.stargazers_count },
  }
}

export default function Page({ errorCode, stars }) {
  if (errorCode) {
    return <Error statusCode={errorCode} />
  }

  return <div>Next stars: {stars}</div>
}
```

The `Error` component also takes `title` as a property if you want to pass in a text message along with a `statusCode`.

If you have a custom `Error` component be sure to import that one instead. `next/error` exports the default component used by Next.js.

### Caveats

- `Error` does not currently support Next.js [Data Fetching methods](https://nextjs.org/docs/pages/building-your-application/data-fetching) like [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props) or [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props).
- `_error`, like `_app`, is a reserved pathname. `_error` is used to define the customized layouts and behaviors of the error pages. `/_error` will render 404 when accessed directly via [routing](https://nextjs.org/docs/pages/building-your-application/routing) or rendering in a [custom server](https://nextjs.org/docs/pages/guides/custom-server).

Was this helpful?

supported.

---

# Dynamic Routes

> Dynamic Routes are pages that allow you to add custom params to your URLs. Start creating Dynamic Routes and learn more here.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Routing](https://nextjs.org/docs/pages/building-your-application/routing)Dynamic RoutesYou are currently viewing the documentation for Pages Router.

# Dynamic Routes

Last updated  April 15, 2025

When you don't know the exact segment names ahead of time and want to create routes from dynamic data, you can use Dynamic Segments that are filled in at request time or [prerendered](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-paths) at build time.

## Convention

A Dynamic Segment can be created by wrapping a file or folder name in square brackets: `[segmentName]`. For example, `[id]` or `[slug]`.

Dynamic Segments can be accessed from [useRouter](https://nextjs.org/docs/pages/api-reference/functions/use-router).

## Example

For example, a blog could include the following route `pages/blog/[slug].js` where `[slug]` is the Dynamic Segment for blog posts.

```
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()
  return <p>Post: {router.query.slug}</p>
}
```

| Route | Example URL | params |
| --- | --- | --- |
| pages/blog/[slug].js | /blog/a | { slug: 'a' } |
| pages/blog/[slug].js | /blog/b | { slug: 'b' } |
| pages/blog/[slug].js | /blog/c | { slug: 'c' } |

## Catch-all Segments

Dynamic Segments can be extended to **catch-all** subsequent segments by adding an ellipsis inside the brackets `[...segmentName]`.

For example, `pages/shop/[...slug].js` will match `/shop/clothes`, but also `/shop/clothes/tops`, `/shop/clothes/tops/t-shirts`, and so on.

| Route | Example URL | params |
| --- | --- | --- |
| pages/shop/[...slug].js | /shop/a | { slug: ['a'] } |
| pages/shop/[...slug].js | /shop/a/b | { slug: ['a', 'b'] } |
| pages/shop/[...slug].js | /shop/a/b/c | { slug: ['a', 'b', 'c'] } |

## Optional Catch-all Segments

Catch-all Segments can be made **optional** by including the parameter in double square brackets: `[[...segmentName]]`.

For example, `pages/shop/[[...slug]].js` will **also** match `/shop`, in addition to `/shop/clothes`, `/shop/clothes/tops`, `/shop/clothes/tops/t-shirts`.

The difference between **catch-all** and **optional catch-all** segments is that with optional, the route without the parameter is also matched (`/shop` in the example above).

| Route | Example URL | params |
| --- | --- | --- |
| pages/shop/[[...slug]].js | /shop | { slug: undefined } |
| pages/shop/[[...slug]].js | /shop/a | { slug: ['a'] } |
| pages/shop/[[...slug]].js | /shop/a/b | { slug: ['a', 'b'] } |
| pages/shop/[[...slug]].js | /shop/a/b/c | { slug: ['a', 'b', 'c'] } |

## Next Steps

For more information on what to do next, we recommend the following sections[Linking and NavigatingLearn how navigation works in Next.js, and how to use the Link Component and `useRouter` hook.](https://nextjs.org/docs/pages/building-your-application/routing/linking-and-navigating)[useRouterLearn more about the API of the Next.js Router, and access the router instance in your page with the useRouter hook.](https://nextjs.org/docs/pages/api-reference/functions/use-router)

Was this helpful?

supported.

---

# Linking and Navigating

> Learn how navigation works in Next.js, and how to use the Link Component and `useRouter` hook.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Routing](https://nextjs.org/docs/pages/building-your-application/routing)Linking and NavigatingYou are currently viewing the documentation for Pages Router.

# Linking and Navigating

Last updated  October 17, 2025

The Next.js router allows you to do client-side route transitions between pages, similar to a single-page application.

A React component called `Link` is provided to do this client-side route transition.

```
import Link from 'next/link'

function Home() {
  return (
    <ul>
      <li>
        <Link href="/">Home</Link>
      </li>
      <li>
        <Link href="/about">About Us</Link>
      </li>
      <li>
        <Link href="/blog/hello-world">Blog Post</Link>
      </li>
    </ul>
  )
}

export default Home
```

The example above uses multiple links. Each one maps a path (`href`) to a known page:

- `/` → `pages/index.js`
- `/about` → `pages/about.js`
- `/blog/hello-world` → `pages/blog/[slug].js`

Any `<Link />` in the viewport (initially or through scroll) will be prefetched by default (including the corresponding data) for pages using [Static Generation](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props). The corresponding data for [server-rendered](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props) routes is fetched *only when* the `<Link />` is clicked.

## Linking to dynamic paths

You can also use interpolation to create the path, which comes in handy for [dynamic route segments](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes). For example, to show a list of posts which have been passed to the component as a prop:

```
import Link from 'next/link'

function Posts({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <Link href={`/blog/${encodeURIComponent(post.slug)}`}>
            {post.title}
          </Link>
        </li>
      ))}
    </ul>
  )
}

export default Posts
```

> [encodeURIComponent](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent) is used in the example to keep the path utf-8 compatible.

Alternatively, using a URL Object:

```
import Link from 'next/link'

function Posts({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <Link
            href={{
              pathname: '/blog/[slug]',
              query: { slug: post.slug },
            }}
          >
            {post.title}
          </Link>
        </li>
      ))}
    </ul>
  )
}

export default Posts
```

Now, instead of using interpolation to create the path, we use a URL object in `href` where:

- `pathname` is the name of the page in the `pages` directory. `/blog/[slug]` in this case.
- `query` is an object with the dynamic segment. `slug` in this case.

## Injecting the router

To access the [routerobject](https://nextjs.org/docs/pages/api-reference/functions/use-router#router-object) in a React component you can use [useRouter](https://nextjs.org/docs/pages/api-reference/functions/use-router) or [withRouter](https://nextjs.org/docs/pages/api-reference/functions/use-router#withrouter).

In general we recommend using [useRouter](https://nextjs.org/docs/pages/api-reference/functions/use-router).

## Imperative Routing

[next/link](https://nextjs.org/docs/pages/api-reference/components/link) should be able to cover most of your routing needs, but you can also do client-side navigations without it, take a look at the [documentation fornext/router](https://nextjs.org/docs/pages/api-reference/functions/use-router).

The following example shows how to do basic page navigations with [useRouter](https://nextjs.org/docs/pages/api-reference/functions/use-router):

```
import { useRouter } from 'next/router'

export default function ReadMore() {
  const router = useRouter()

  return (
    <button onClick={() => router.push('/about')}>
      Click here to read more
    </button>
  )
}
```

## Shallow Routing

 Examples

- [Shallow Routing](https://github.com/vercel/next.js/tree/canary/examples/with-shallow-routing)

Shallow routing allows you to change the URL without running data fetching methods again, that includes [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props), [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props), and [getInitialProps](https://nextjs.org/docs/pages/api-reference/functions/get-initial-props).

You'll receive the updated `pathname` and the `query` via the [routerobject](https://nextjs.org/docs/pages/api-reference/functions/use-router#router-object) (added by [useRouter](https://nextjs.org/docs/pages/api-reference/functions/use-router) or [withRouter](https://nextjs.org/docs/pages/api-reference/functions/use-router#withrouter)), without losing state.

To enable shallow routing, set the `shallow` option to `true`. Consider the following example:

```
import { useEffect } from 'react'
import { useRouter } from 'next/router'

// Current URL is '/'
function Page() {
  const router = useRouter()

  useEffect(() => {
    // Always do navigations after the first render
    router.push('/?counter=10', undefined, { shallow: true })
  }, [])

  useEffect(() => {
    // The counter changed!
  }, [router.query.counter])
}

export default Page
```

The URL will get updated to `/?counter=10` and the page won't get replaced, only the state of the route is changed.

You can also watch for URL changes via [componentDidUpdate](https://react.dev/reference/react/Component#componentdidupdate) as shown below:

```
componentDidUpdate(prevProps) {
  const { pathname, query } = this.props.router
  // verify props have changed to avoid an infinite loop
  if (query.counter !== prevProps.router.query.counter) {
    // fetch data based on the new query
  }
}
```

### Caveats

Shallow routing **only** works for URL changes in the current page. For example, let's assume we have another page called `pages/about.js`, and you run this:

```
router.push('/?counter=10', '/about?counter=10', { shallow: true })
```

Since that's a new page, it'll unload the current page, load the new one and wait for data fetching even though we asked to do shallow routing.

When shallow routing is used with proxy it will not ensure the new page matches the current page like previously done without proxy. This is due to proxy being able to rewrite dynamically and can't be verified client-side without a data fetch which is skipped with shallow, so a shallow route change must always be treated as shallow.

Was this helpful?

supported.

---

# Pages and Layouts

> Create your first page and shared layout with the Pages Router.

[Building Your Application](https://nextjs.org/docs/pages/building-your-application)[Routing](https://nextjs.org/docs/pages/building-your-application/routing)Pages and LayoutsYou are currently viewing the documentation for Pages Router.

# Pages and Layouts

Last updated  April 15, 2025

The Pages Router has a file-system based router built on the concept of pages.

When a file is added to the `pages` directory, it's automatically available as a route.

In Next.js, a **page** is a [React Component](https://react.dev/learn/your-first-component) exported from a `.js`, `.jsx`, `.ts`, or `.tsx` file in the `pages` directory. Each page is associated with a route based on its file name.

**Example**: If you create `pages/about.js` that exports a React component like below, it will be accessible at `/about`.

```
export default function About() {
  return <div>About</div>
}
```

## Index routes

The router will automatically route files named `index` to the root of the directory.

- `pages/index.js` → `/`
- `pages/blog/index.js` → `/blog`

## Nested routes

The router supports nested files. If you create a nested folder structure, files will automatically be routed in the same way still.

- `pages/blog/first-post.js` → `/blog/first-post`
- `pages/dashboard/settings/username.js` → `/dashboard/settings/username`

## Pages with Dynamic Routes

Next.js supports pages with dynamic routes. For example, if you create a file called `pages/posts/[id].js`, then it will be accessible at `posts/1`, `posts/2`, etc.

> To learn more about dynamic routing, check the [Dynamic Routing documentation](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes).

## Layout Pattern

The React model allows us to deconstruct a [page](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts) into a series of components. Many of these components are often reused between pages. For example, you might have the same navigation bar and footer on every page.

 components/layout.js

```
import Navbar from './navbar'
import Footer from './footer'

export default function Layout({ children }) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
      <Footer />
    </>
  )
}
```

## Examples

### Single Shared Layout with Custom App

If you only have one layout for your entire application, you can create a [Custom App](https://nextjs.org/docs/pages/building-your-application/routing/custom-app) and wrap your application with the layout. Since the `<Layout />` component is re-used when changing pages, its component state will be preserved (e.g. input values).

 pages/_app.js

```
import Layout from '../components/layout'

export default function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  )
}
```

### Per-Page Layouts

If you need multiple layouts, you can add a property `getLayout` to your page, allowing you to return a React component for the layout. This allows you to define the layout on a *per-page basis*. Since we're returning a function, we can have complex nested layouts if desired.

 pages/index.js

```
import Layout from '../components/layout'
import NestedLayout from '../components/nested-layout'

export default function Page() {
  return (
    /** Your content */
  )
}

Page.getLayout = function getLayout(page) {
  return (
    <Layout>
      <NestedLayout>{page}</NestedLayout>
    </Layout>
  )
}
```

 pages/_app.js

```
export default function MyApp({ Component, pageProps }) {
  // Use the layout defined at the page level, if available
  const getLayout = Component.getLayout ?? ((page) => page)

  return getLayout(<Component {...pageProps} />)
}
```

When navigating between pages, we want to *persist* page state (input values, scroll position, etc.) for a Single-Page Application (SPA) experience.

This layout pattern enables state persistence because the React component tree is maintained between page transitions. With the component tree, React can understand which elements have changed to preserve state.

> **Good to know**: This process is called [reconciliation](https://react.dev/learn/preserving-and-resetting-state), which is how React understands which elements have changed.

### With TypeScript

When using TypeScript, you must first create a new type for your pages which includes a `getLayout` function. Then, you must create a new type for your `AppProps` which overrides the `Component` property to use the previously created type.

 pages/index.tsxJavaScriptTypeScript

```
import type { ReactElement } from 'react'
import Layout from '../components/layout'
import NestedLayout from '../components/nested-layout'
import type { NextPageWithLayout } from './_app'

const Page: NextPageWithLayout = () => {
  return <p>hello world</p>
}

Page.getLayout = function getLayout(page: ReactElement) {
  return (
    <Layout>
      <NestedLayout>{page}</NestedLayout>
    </Layout>
  )
}

export default Page
```

   pages/_app.tsxJavaScriptTypeScript

```
import type { ReactElement, ReactNode } from 'react'
import type { NextPage } from 'next'
import type { AppProps } from 'next/app'

export type NextPageWithLayout<P = {}, IP = P> = NextPage<P, IP> & {
  getLayout?: (page: ReactElement) => ReactNode
}

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout
}

export default function MyApp({ Component, pageProps }: AppPropsWithLayout) {
  // Use the layout defined at the page level, if available
  const getLayout = Component.getLayout ?? ((page) => page)

  return getLayout(<Component {...pageProps} />)
}
```

### Data Fetching

Inside your layout, you can fetch data on the client-side using `useEffect` or a library like [SWR](https://swr.vercel.app/). Because this file is not a [Page](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts), you cannot use `getStaticProps` or `getServerSideProps` currently.

 components/layout.js

```
import useSWR from 'swr'
import Navbar from './navbar'
import Footer from './footer'

export default function Layout({ children }) {
  const { data, error } = useSWR('/api/navigation', fetcher)

  if (error) return <div>Failed to load</div>
  if (!data) return <div>Loading...</div>

  return (
    <>
      <Navbar links={data.links} />
      <main>{children}</main>
      <Footer />
    </>
  )
}
```

Was this helpful?

supported.

---

# Routing

> Learn the fundamentals of routing for front-end applications with the Pages Router.

[Pages Router](https://nextjs.org/docs/pages)[Building Your Application](https://nextjs.org/docs/pages/building-your-application)RoutingYou are currently viewing the documentation for Pages Router.

# Routing

Last updated  April 15, 2025

The Pages Router has a file-system based router built on concepts of pages. When a file is added to the `pages` directory it's automatically available as a route. Learn more about routing in the Pages Router:

[Pages and LayoutsCreate your first page and shared layout with the Pages Router.](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts)[Dynamic RoutesDynamic Routes are pages that allow you to add custom params to your URLs. Start creating Dynamic Routes and learn more here.](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes)[Linking and NavigatingLearn how navigation works in Next.js, and how to use the Link Component and `useRouter` hook.](https://nextjs.org/docs/pages/building-your-application/routing/linking-and-navigating)[Custom AppControl page initialization and add a layout that persists for all pages by overriding the default App component used by Next.js.](https://nextjs.org/docs/pages/building-your-application/routing/custom-app)[Custom DocumentExtend the default document markup added by Next.js.](https://nextjs.org/docs/pages/building-your-application/routing/custom-document)[API RoutesNext.js supports API Routes, which allow you to build your API without leaving your Next.js app. Learn how it works here.](https://nextjs.org/docs/pages/building-your-application/routing/api-routes)[Custom ErrorsOverride and extend the built-in Error page to handle custom errors.](https://nextjs.org/docs/pages/building-your-application/routing/custom-error)

Was this helpful?

supported.

---

# Building Your Application

> Learn how to use Next.js features to build your application.

[Next.js Docs](https://nextjs.org/docs)[Pages Router](https://nextjs.org/docs/pages)Building Your ApplicationYou are currently viewing the documentation for Pages Router.

# Building Your Application

Last updated  June 16, 2025[RoutingLearn the fundamentals of routing for front-end applications with the Pages Router.](https://nextjs.org/docs/pages/building-your-application/routing)[RenderingLearn the fundamentals of rendering in React and Next.js.](https://nextjs.org/docs/pages/building-your-application/rendering)[Data FetchingNext.js allows you to fetch data in multiple ways, with pre-rendering, server-side rendering or static-site generation, and incremental static regeneration. Learn how to manage your application data in Next.js.](https://nextjs.org/docs/pages/building-your-application/data-fetching)[ConfiguringLearn how to configure your Next.js application.](https://nextjs.org/docs/pages/building-your-application/configuring)

Was this helpful?

supported.
