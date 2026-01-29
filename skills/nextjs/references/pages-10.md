# useRouter and more

# useRouter

> Learn more about the API of the Next.js Router, and access the router instance in your page with the useRouter hook.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)useRouterYou are currently viewing the documentation for Pages Router.

# useRouter

Last updated  April 24, 2025

If you want to access the [routerobject](#router-object) inside any function component in your app, you can use the `useRouter` hook, take a look at the following example:

```
import { useRouter } from 'next/router'

function ActiveLink({ children, href }) {
  const router = useRouter()
  const style = {
    marginRight: 10,
    color: router.asPath === href ? 'red' : 'black',
  }

  const handleClick = (e) => {
    e.preventDefault()
    router.push(href)
  }

  return (
    <a href={href} onClick={handleClick} style={style}>
      {children}
    </a>
  )
}

export default ActiveLink
```

> `useRouter` is a [React Hook](https://react.dev/learn#using-hooks), meaning it cannot be used with classes. You can either use [withRouter](#withrouter) or wrap your class in a function component.

## routerobject

The following is the definition of the `router` object returned by both [useRouter](#top) and [withRouter](#withrouter):

- `pathname`: `String` - The path for current route file that comes after `/pages`. Therefore, `basePath`, `locale` and trailing slash (`trailingSlash: true`) are not included.
- `query`: `Object` - The query string parsed to an object, including [dynamic route](https://nextjs.org/docs/pages/building-your-application/routing/dynamic-routes) parameters. It will be an empty object during prerendering if the page doesn't use [Server-side Rendering](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props). Defaults to `{}`
- `asPath`: `String` - The path as shown in the browser including the search params and respecting the `trailingSlash` configuration. `basePath` and `locale` are not included.
- `isFallback`: `boolean` - Whether the current page is in [fallback mode](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-true).
- `basePath`: `String` - The active [basePath](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath) (if enabled).
- `locale`: `String` - The active locale (if enabled).
- `locales`: `String[]` - All supported locales (if enabled).
- `defaultLocale`: `String` - The current default locale (if enabled).
- `domainLocales`: `Array<{domain, defaultLocale, locales}>` - Any configured domain locales.
- `isReady`: `boolean` - Whether the router fields are updated client-side and ready for use. Should only be used inside of `useEffect` methods and not for conditionally rendering on the server. See related docs for use case with [automatically statically optimized pages](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization)
- `isPreview`: `boolean` - Whether the application is currently in [preview mode](https://nextjs.org/docs/pages/guides/preview-mode).

> Using the `asPath` field may lead to a mismatch between client and server if the page is rendered using server-side rendering or [automatic static optimization](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization). Avoid using `asPath` until the `isReady` field is `true`.

The following methods are included inside `router`:

### router.push

Handles client-side transitions, this method is useful for cases where [next/link](https://nextjs.org/docs/pages/api-reference/components/link) is not enough.

```
router.push(url, as, options)
```

- `url`: `UrlObject | String` - The URL to navigate to (see [Node.JS URL module documentation](https://nodejs.org/api/url.html#legacy-urlobject) for `UrlObject` properties).
- `as`: `UrlObject | String` - Optional decorator for the path that will be shown in the browser URL bar. Before Next.js 9.5.3 this was used for dynamic routes.
- `options` - Optional object with the following configuration options:
  - `scroll` - Optional boolean, controls scrolling to the top of the page after navigation. Defaults to `true`
  - [shallow](https://nextjs.org/docs/pages/building-your-application/routing/linking-and-navigating#shallow-routing): Update the path of the current page without rerunning [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props), [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props) or [getInitialProps](https://nextjs.org/docs/pages/api-reference/functions/get-initial-props). Defaults to `false`
  - `locale` - Optional string, indicates locale of the new page

> You don't need to use `router.push` for external URLs. [window.location](https://developer.mozilla.org/docs/Web/API/Window/location) is better suited for those cases.

Navigating to `pages/about.js`, which is a predefined route:

```
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()

  return (
    <button type="button" onClick={() => router.push('/about')}>
      Click me
    </button>
  )
}
```

Navigating `pages/post/[pid].js`, which is a dynamic route:

```
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()

  return (
    <button type="button" onClick={() => router.push('/post/abc')}>
      Click me
    </button>
  )
}
```

Redirecting the user to `pages/login.js`, useful for pages behind [authentication](https://nextjs.org/docs/pages/guides/authentication):

```
import { useEffect } from 'react'
import { useRouter } from 'next/router'

// Here you would fetch and return the user
const useUser = () => ({ user: null, loading: false })

export default function Page() {
  const { user, loading } = useUser()
  const router = useRouter()

  useEffect(() => {
    if (!(user || loading)) {
      router.push('/login')
    }
  }, [user, loading])

  return <p>Redirecting...</p>
}
```

#### Resetting state after navigation

When navigating to the same page in Next.js, the page's state **will not** be reset by default as React does not unmount unless the parent component has changed.

 pages/[slug].js

```
import Link from 'next/link'
import { useState } from 'react'
import { useRouter } from 'next/router'

export default function Page(props) {
  const router = useRouter()
  const [count, setCount] = useState(0)
  return (
    <div>
      <h1>Page: {router.query.slug}</h1>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increase count</button>
      <Link href="/one">one</Link> <Link href="/two">two</Link>
    </div>
  )
}
```

In the above example, navigating between `/one` and `/two` **will not** reset the count . The `useState` is maintained between renders because the top-level React component, `Page`, is the same.

If you do not want this behavior, you have a couple of options:

- Manually ensure each state is updated using `useEffect`. In the above example, that could look like:
  ```
  useEffect(() => {
    setCount(0)
  }, [router.query.slug])
  ```
- Use a React `key` to [tell React to remount the component](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key). To do this for all pages, you can use a custom app:
   pages/_app.js
  ```
  import { useRouter } from 'next/router'
  export default function MyApp({ Component, pageProps }) {
    const router = useRouter()
    return <Component key={router.asPath} {...pageProps} />
  }
  ```

#### With URL object

You can use a URL object in the same way you can use it for [next/link](https://nextjs.org/docs/pages/api-reference/components/link#passing-a-url-object). Works for both the `url` and `as` parameters:

```
import { useRouter } from 'next/router'

export default function ReadMore({ post }) {
  const router = useRouter()

  return (
    <button
      type="button"
      onClick={() => {
        router.push({
          pathname: '/post/[pid]',
          query: { pid: post.id },
        })
      }}
    >
      Click here to read more
    </button>
  )
}
```

### router.replace

Similar to the `replace` prop in [next/link](https://nextjs.org/docs/pages/api-reference/components/link), `router.replace` will prevent adding a new URL entry into the `history` stack.

```
router.replace(url, as, options)
```

- The API for `router.replace` is exactly the same as the API for [router.push](#routerpush).

Take a look at the following example:

```
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()

  return (
    <button type="button" onClick={() => router.replace('/home')}>
      Click me
    </button>
  )
}
```

### router.prefetch

Prefetch pages for faster client-side transitions. This method is only useful for navigations without [next/link](https://nextjs.org/docs/pages/api-reference/components/link), as `next/link` takes care of prefetching pages automatically.

> This is a production only feature. Next.js doesn't prefetch pages in development.

```
router.prefetch(url, as, options)
```

- `url` - The URL to prefetch, including explicit routes (e.g. `/dashboard`) and dynamic routes (e.g. `/product/[id]`)
- `as` - Optional decorator for `url`. Before Next.js 9.5.3 this was used to prefetch dynamic routes.
- `options` - Optional object with the following allowed fields:
  - `locale` - allows providing a different locale from the active one. If `false`, `url` has to include the locale as the active locale won't be used.

Let's say you have a login page, and after a login, you redirect the user to the dashboard. For that case, we can prefetch the dashboard to make a faster transition, like in the following example:

```
import { useCallback, useEffect } from 'react'
import { useRouter } from 'next/router'

export default function Login() {
  const router = useRouter()
  const handleSubmit = useCallback((e) => {
    e.preventDefault()

    fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        /* Form data */
      }),
    }).then((res) => {
      // Do a fast client-side transition to the already prefetched dashboard page
      if (res.ok) router.push('/dashboard')
    })
  }, [])

  useEffect(() => {
    // Prefetch the dashboard page
    router.prefetch('/dashboard')
  }, [router])

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit">Login</button>
    </form>
  )
}
```

### router.beforePopState

In some cases (for example, if using a [Custom Server](https://nextjs.org/docs/pages/guides/custom-server)), you may wish to listen to [popstate](https://developer.mozilla.org/docs/Web/API/Window/popstate_event) and do something before the router acts on it.

```
router.beforePopState(cb)
```

- `cb` - The function to run on incoming `popstate` events. The function receives the state of the event as an object with the following props:
  - `url`: `String` - the route for the new state. This is usually the name of a `page`
  - `as`: `String` - the url that will be shown in the browser
  - `options`: `Object` - Additional options sent by [router.push](#routerpush)

If `cb` returns `false`, the Next.js router will not handle `popstate`, and you'll be responsible for handling it in that case. See [Disabling file-system routing](https://nextjs.org/docs/pages/guides/custom-server#disabling-file-system-routing).

You could use `beforePopState` to manipulate the request, or force a SSR refresh, as in the following example:

```
import { useEffect } from 'react'
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()

  useEffect(() => {
    router.beforePopState(({ url, as, options }) => {
      // I only want to allow these two routes!
      if (as !== '/' && as !== '/other') {
        // Have SSR render bad routes as a 404.
        window.location.href = as
        return false
      }

      return true
    })
  }, [router])

  return <p>Welcome to the page</p>
}
```

### router.back

Navigate back in history. Equivalent to clicking the browser’s back button. It executes `window.history.back()`.

```
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()

  return (
    <button type="button" onClick={() => router.back()}>
      Click here to go back
    </button>
  )
}
```

### router.reload

Reload the current URL. Equivalent to clicking the browser’s refresh button. It executes `window.location.reload()`.

```
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()

  return (
    <button type="button" onClick={() => router.reload()}>
      Click here to reload
    </button>
  )
}
```

### router.events

You can listen to different events happening inside the Next.js Router. Here's a list of supported events:

- `routeChangeStart(url, { shallow })` - Fires when a route starts to change
- `routeChangeComplete(url, { shallow })` - Fires when a route changed completely
- `routeChangeError(err, url, { shallow })` - Fires when there's an error when changing routes, or a route load is cancelled
  - `err.cancelled` - Indicates if the navigation was cancelled
- `beforeHistoryChange(url, { shallow })` - Fires before changing the browser's history
- `hashChangeStart(url, { shallow })` - Fires when the hash will change but not the page
- `hashChangeComplete(url, { shallow })` - Fires when the hash has changed but not the page

> **Good to know**: Here `url` is the URL shown in the browser, including the [basePath](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath).

For example, to listen to the router event `routeChangeStart`, open or create `pages/_app.js` and subscribe to the event, like so:

```
import { useEffect } from 'react'
import { useRouter } from 'next/router'

export default function MyApp({ Component, pageProps }) {
  const router = useRouter()

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

  return <Component {...pageProps} />
}
```

> We use a [Custom App](https://nextjs.org/docs/pages/building-your-application/routing/custom-app) (`pages/_app.js`) for this example to subscribe to the event because it's not unmounted on page navigations, but you can subscribe to router events on any component in your application.

Router events should be registered when a component mounts ([useEffect](https://react.dev/reference/react/useEffect) or [componentDidMount](https://react.dev/reference/react/Component#componentdidmount) / [componentWillUnmount](https://react.dev/reference/react/Component#componentwillunmount)) or imperatively when an event happens.

If a route load is cancelled (for example, by clicking two links rapidly in succession), `routeChangeError` will fire. And the passed `err` will contain a `cancelled` property set to `true`, as in the following example:

```
import { useEffect } from 'react'
import { useRouter } from 'next/router'

export default function MyApp({ Component, pageProps }) {
  const router = useRouter()

  useEffect(() => {
    const handleRouteChangeError = (err, url) => {
      if (err.cancelled) {
        console.log(`Route to ${url} was cancelled!`)
      }
    }

    router.events.on('routeChangeError', handleRouteChangeError)

    // If the component is unmounted, unsubscribe
    // from the event with the `off` method:
    return () => {
      router.events.off('routeChangeError', handleRouteChangeError)
    }
  }, [router])

  return <Component {...pageProps} />
}
```

## Thenext/compat/routerexport

This is the same `useRouter` hook, but can be used in both `app` and `pages` directories.

It differs from `next/router` in that it does not throw an error when the pages router is not mounted, and instead has a return type of `NextRouter | null`.
This allows developers to convert components to support running in both `app` and `pages` as they transition to the `app` router.

A component that previously looked like this:

```
import { useRouter } from 'next/router'
const MyComponent = () => {
  const { isReady, query } = useRouter()
  // ...
}
```

Will error when converted over to `next/compat/router`, as `null` can not be destructured. Instead, developers will be able to take advantage of new hooks:

```
import { useEffect } from 'react'
import { useRouter } from 'next/compat/router'
import { useSearchParams } from 'next/navigation'
const MyComponent = () => {
  const router = useRouter() // may be null or a NextRouter instance
  const searchParams = useSearchParams()
  useEffect(() => {
    if (router && !router.isReady) {
      return
    }
    // In `app/`, searchParams will be ready immediately with the values, in
    // `pages/` it will be available after the router is ready.
    const search = searchParams.get('search')
    // ...
  }, [router, searchParams])
  // ...
}
```

This component will now work in both `pages` and `app` directories. When the component is no longer used in `pages`, you can remove the references to the compat router:

```
import { useSearchParams } from 'next/navigation'
const MyComponent = () => {
  const searchParams = useSearchParams()
  // As this component is only used in `app/`, the compat router can be removed.
  const search = searchParams.get('search')
  // ...
}
```

### UsinguseRouteroutside of Next.js context in pages

Another specific use case is when rendering components outside of a Next.js application context, such as inside `getServerSideProps` on the `pages` directory. In this case, the compat router can be used to avoid errors:

```
import { renderToString } from 'react-dom/server'
import { useRouter } from 'next/compat/router'
const MyComponent = () => {
  const router = useRouter() // may be null or a NextRouter instance
  // ...
}
export async function getServerSideProps() {
  const renderedComponent = renderToString(<MyComponent />)
  return {
    props: {
      renderedComponent,
    },
  }
}
```

## Potential ESLint errors

Certain methods accessible on the `router` object return a Promise. If you have the ESLint rule, [no-floating-promises](https://typescript-eslint.io/rules/no-floating-promises) enabled, consider disabling it either globally, or for the affected line.

If your application needs this rule, you should either `void` the promise – or use an `async` function, `await` the Promise, then void the function call. **This is not applicable when the method is called from inside anonClickhandler**.

The affected methods are:

- `router.push`
- `router.replace`
- `router.prefetch`

### Potential solutions

```
import { useEffect } from 'react'
import { useRouter } from 'next/router'

// Here you would fetch and return the user
const useUser = () => ({ user: null, loading: false })

export default function Page() {
  const { user, loading } = useUser()
  const router = useRouter()

  useEffect(() => {
    // disable the linting on the next line - This is the cleanest solution
    // eslint-disable-next-line no-floating-promises
    router.push('/login')

    // void the Promise returned by router.push
    if (!(user || loading)) {
      void router.push('/login')
    }
    // or use an async function, await the Promise, then void the function call
    async function handleRouteChange() {
      if (!(user || loading)) {
        await router.push('/login')
      }
    }
    void handleRouteChange()
  }, [user, loading])

  return <p>Redirecting...</p>
}
```

## withRouter

If [useRouter](#router-object) is not the best fit for you, `withRouter` can also add the same [routerobject](#router-object) to any component.

### Usage

```
import { withRouter } from 'next/router'

function Page({ router }) {
  return <p>{router.pathname}</p>
}

export default withRouter(Page)
```

### TypeScript

To use class components with `withRouter`, the component needs to accept a router prop:

```
import React from 'react'
import { withRouter, NextRouter } from 'next/router'

interface WithRouterProps {
  router: NextRouter
}

interface MyComponentProps extends WithRouterProps {}

class MyComponent extends React.Component<MyComponentProps> {
  render() {
    return <p>{this.props.router.pathname}</p>
  }
}

export default withRouter(MyComponent)
```

Was this helpful?

supported.

---

# useSearchParams

> API Reference for the useSearchParams hook in the Pages Router.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)useSearchParamsYou are currently viewing the documentation for Pages Router.

# useSearchParams

Last updated  January 14, 2026

`useSearchParams` is a hook that lets you read the current URL's **query string**.

`useSearchParams` returns a **read-only** version of the [URLSearchParams](https://developer.mozilla.org/docs/Web/API/URLSearchParams) interface.

 pages/dashboard.tsxJavaScriptTypeScript

```
import { useSearchParams } from 'next/navigation'

export default function Dashboard() {
  const searchParams = useSearchParams()

  if (!searchParams) {
    // Render fallback UI while search params are not yet available
    return null
  }

  const search = searchParams.get('search')

  // URL -> `/dashboard?search=my-project`
  // `search` -> 'my-project'
  return <>Search: {search}</>
}
```

## Parameters

```
const searchParams = useSearchParams()
```

`useSearchParams` does not take any parameters.

## Returns

`useSearchParams` returns a **read-only** version of the [URLSearchParams](https://developer.mozilla.org/docs/Web/API/URLSearchParams) interface, or `null` during [pre-rendering](#behavior-during-pre-rendering).

The interface includes utility methods for reading the URL's query string:

- [URLSearchParams.get()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/get): Returns the first value associated with the search parameter. For example:
  | URL | searchParams.get("a") |
  | --- | --- |
  | /dashboard?a=1 | '1' |
  | /dashboard?a= | '' |
  | /dashboard?b=3 | null |
  | /dashboard?a=1&a=2 | '1'- usegetAll()to get all values |
- [URLSearchParams.has()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/has): Returns a boolean value indicating if the given parameter exists. For example:
  | URL | searchParams.has("a") |
  | --- | --- |
  | /dashboard?a=1 | true |
  | /dashboard?b=3 | false |
- Learn more about other **read-only** methods of [URLSearchParams](https://developer.mozilla.org/docs/Web/API/URLSearchParams), including the [getAll()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/getAll), [keys()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/keys), [values()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/values), [entries()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/entries), [forEach()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/forEach), and [toString()](https://developer.mozilla.org/docs/Web/API/URLSearchParams/toString).

> **Good to know**: `useSearchParams` is a [React Hook](https://react.dev/learn#using-hooks) and cannot be used with classes.

## Behavior

### Behavior during pre-rendering

For pages that are [statically optimized](https://nextjs.org/docs/pages/building-your-application/rendering/automatic-static-optimization) (not using `getServerSideProps`), `useSearchParams` will return `null` during pre-rendering. After hydration, the value will be updated to the actual search params.

This is because search params cannot be known during static generation as they depend on the request.

 pages/dashboard.tsxJavaScriptTypeScript

```
import { useSearchParams } from 'next/navigation'

export default function Dashboard() {
  const searchParams = useSearchParams()

  if (!searchParams) {
    // Return a fallback UI while search params are loading
    // This prevents hydration mismatches
    return <DashboardSkeleton />
  }

  const search = searchParams.get('search')

  return <>Search: {search}</>
}
```

### Using withgetServerSideProps

When using [getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props), the page is server-rendered on each request and `useSearchParams` will return the actual search params immediately:

 pages/dashboard.tsxJavaScriptTypeScript

```
import { useSearchParams } from 'next/navigation'

export default function Dashboard() {
  const searchParams = useSearchParams()

  // With getServerSideProps, this fallback is never rendered because
  // searchParams is always available on the server. However, keeping
  // the fallback allows this component to be reused on other pages
  // that may not use getServerSideProps.
  if (!searchParams) {
    return null
  }

  const search = searchParams.get('search')

  return <>Search: {search}</>
}

export async function getServerSideProps() {
  return { props: {} }
}
```

## Examples

### Updating search params

You can use the [useRouter](https://nextjs.org/docs/pages/api-reference/functions/use-router) hook to update search params:

 pages/dashboard.tsxJavaScriptTypeScript

```
import { useRouter } from 'next/router'
import { useSearchParams } from 'next/navigation'
import { useCallback } from 'react'

export default function Dashboard() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const createQueryString = useCallback(
    (name: string, value: string) => {
      const params = new URLSearchParams(searchParams?.toString())
      params.set(name, value)
      return params.toString()
    },
    [searchParams]
  )

  if (!searchParams) {
    return null
  }

  return (
    <>
      <p>Sort By</p>
      <button
        onClick={() => {
          router.push(router.pathname + '?' + createQueryString('sort', 'asc'))
        }}
      >
        ASC
      </button>
      <button
        onClick={() => {
          router.push(router.pathname + '?' + createQueryString('sort', 'desc'))
        }}
      >
        DESC
      </button>
    </>
  )
}
```

### Sharing components with App Router

`useSearchParams` from `next/navigation` works in both the Pages Router and App Router. This allows you to create shared components that work in either context:

 components/search-bar.tsxJavaScriptTypeScript

```
import { useSearchParams } from 'next/navigation'

// This component works in both pages/ and app/
export function SearchBar() {
  const searchParams = useSearchParams()

  if (!searchParams) {
    // Fallback for Pages Router during pre-rendering
    return <input defaultValue="" placeholder="Search..." />
  }

  const search = searchParams.get('search') ?? ''

  return <input defaultValue={search} placeholder="Search..." />
}
```

> **Good to know**: When using this component in the App Router, wrap it in a `<Suspense>` boundary for [static rendering](https://nextjs.org/docs/app/api-reference/functions/use-search-params#static-rendering) support.

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | useSearchParamsintroduced. |

Was this helpful?

supported.

---

# userAgent

> The userAgent helper extends the Web Request API with additional properties and methods to interact with the user agent object from the request.

[API Reference](https://nextjs.org/docs/pages/api-reference)[Functions](https://nextjs.org/docs/pages/api-reference/functions)userAgentYou are currently viewing the documentation for Pages Router.

# userAgent

Last updated  April 15, 2025

The `userAgent` helper extends the [Web Request API](https://developer.mozilla.org/docs/Web/API/Request) with additional properties and methods to interact with the user agent object from the request.

 proxy.tsJavaScriptTypeScript

```
import { NextRequest, NextResponse, userAgent } from 'next/server'

export function proxy(request: NextRequest) {
  const url = request.nextUrl
  const { device } = userAgent(request)

  // device.type can be: 'mobile', 'tablet', 'console', 'smarttv',
  // 'wearable', 'embedded', or undefined (for desktop browsers)
  const viewport = device.type || 'desktop'

  url.searchParams.set('viewport', viewport)
  return NextResponse.rewrite(url)
}
```

## isBot

A boolean indicating whether the request comes from a known bot.

## browser

An object containing information about the browser used in the request.

- `name`: A string representing the browser's name, or `undefined` if not identifiable.
- `version`: A string representing the browser's version, or `undefined`.

## device

An object containing information about the device used in the request.

- `model`: A string representing the model of the device, or `undefined`.
- `type`: A string representing the type of the device, such as `console`, `mobile`, `tablet`, `smarttv`, `wearable`, `embedded`, or `undefined`.
- `vendor`: A string representing the vendor of the device, or `undefined`.

## engine

An object containing information about the browser's engine.

- `name`: A string representing the engine's name. Possible values include: `Amaya`, `Blink`, `EdgeHTML`, `Flow`, `Gecko`, `Goanna`, `iCab`, `KHTML`, `Links`, `Lynx`, `NetFront`, `NetSurf`, `Presto`, `Tasman`, `Trident`, `w3m`, `WebKit` or `undefined`.
- `version`: A string representing the engine's version, or `undefined`.

## os

An object containing information about the operating system.

- `name`: A string representing the name of the OS, or `undefined`.
- `version`: A string representing the version of the OS, or `undefined`.

## cpu

An object containing information about the CPU architecture.

- `architecture`: A string representing the architecture of the CPU. Possible values include: `68k`, `amd64`, `arm`, `arm64`, `armhf`, `avr`, `ia32`, `ia64`, `irix`, `irix64`, `mips`, `mips64`, `pa-risc`, `ppc`, `sparc`, `sparc64` or `undefined`

Was this helpful?

supported.

---

# Functions

> API Reference for Functions and Hooks in Pages Router.

[Pages Router](https://nextjs.org/docs/pages)[API Reference](https://nextjs.org/docs/pages/api-reference)FunctionsYou are currently viewing the documentation for Pages Router.

# Functions

Last updated  April 15, 2025[getInitialPropsFetch dynamic data on the server for your React component with getInitialProps.](https://nextjs.org/docs/pages/api-reference/functions/get-initial-props)[getServerSidePropsAPI reference for `getServerSideProps`. Learn how to fetch data on each request with Next.js.](https://nextjs.org/docs/pages/api-reference/functions/get-server-side-props)[getStaticPathsAPI reference for `getStaticPaths`. Learn how to fetch data and generate static pages with `getStaticPaths`.](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths)[getStaticPropsAPI reference for `getStaticProps`. Learn how to use `getStaticProps` to generate static pages with Next.js.](https://nextjs.org/docs/pages/api-reference/functions/get-static-props)[NextRequestAPI Reference for NextRequest.](https://nextjs.org/docs/pages/api-reference/functions/next-request)[NextResponseAPI Reference for NextResponse.](https://nextjs.org/docs/pages/api-reference/functions/next-response)[useParamsAPI Reference for the useParams hook in the Pages Router.](https://nextjs.org/docs/pages/api-reference/functions/use-params)[useReportWebVitalsuseReportWebVitals](https://nextjs.org/docs/pages/api-reference/functions/use-report-web-vitals)[useRouterLearn more about the API of the Next.js Router, and access the router instance in your page with the useRouter hook.](https://nextjs.org/docs/pages/api-reference/functions/use-router)[useSearchParamsAPI Reference for the useSearchParams hook in the Pages Router.](https://nextjs.org/docs/pages/api-reference/functions/use-search-params)[userAgentThe userAgent helper extends the Web Request API with additional properties and methods to interact with the user agent object from the request.](https://nextjs.org/docs/pages/api-reference/functions/userAgent)

Was this helpful?

supported.

---

# Turbopack

> Turbopack is an incremental bundler optimized for JavaScript and TypeScript, written in Rust, and built into Next.js.

[Pages Router](https://nextjs.org/docs/pages)[API Reference](https://nextjs.org/docs/pages/api-reference)TurbopackYou are currently viewing the documentation for Pages Router.

# Turbopack

Last updated  April 15, 2025

Turbopack is an **incremental bundler** optimized for JavaScript and TypeScript, written in Rust, and built into **Next.js**. You can use Turbopack with both the Pages and App Router for a **much faster** local development experience.

## Why Turbopack?

We built Turbopack to push the performance of Next.js, including:

- **Unified Graph:** Next.js supports multiple output environments (e.g., client and server). Managing multiple compilers and stitching bundles together can be tedious. Turbopack uses a **single, unified graph** for all environments.
- **Bundling vs Native ESM:** Some tools skip bundling in development and rely on the browser's native ESM. This works well for small apps but can slow down large apps due to excessive network requests. Turbopack **bundles** in dev, but in an optimized way to keep large apps fast.
- **Incremental Computation:** Turbopack parallelizes work across cores and **caches** results down to the function level. Once a piece of work is done, Turbopack won’t repeat it.
- **Lazy Bundling:** Turbopack only bundles what is actually requested by the dev server. This lazy approach can reduce initial compile times and memory usage.

## Getting started

Turbopack is now the **default bundler** in Next.js. No configuration is needed to use Turbopack:

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

### Using Webpack instead

If you need to use Webpack instead of Turbopack, you can opt-in with the `--webpack` flag:

 package.json

```
{
  "scripts": {
    "dev": "next dev --webpack",
    "build": "next build --webpack",
    "start": "next start"
  }
}
```

## Supported features

Turbopack in Next.js has **zero-configuration** for the common use cases. Below is a summary of what is supported out of the box, plus some references to how you can configure Turbopack further when needed.

### Language features

| Feature | Status | Notes |
| --- | --- | --- |
| JavaScript & TypeScript | Supported | Uses SWC under the hood. Type-checking is not done by Turbopack (runtsc --watchor rely on your IDE for type checks). |
| ECMAScript (ESNext) | Supported | Turbopack supports the latest ECMAScript features, matching SWC’s coverage. |
| CommonJS | Supported | require()syntax is handled out of the box. |
| ESM | Supported | Static and dynamicimportare fully supported. |
| Babel | Supported | Starting in Next.js 16, Turbopack uses Babel automatically if it detectsa configuration file. Unlike in webpack, SWC is always used for Next.js's internal transforms and downleveling to older ECMAScript revisions. Next.js with webpack disables SWC if a Babel configuration file is present. Files innode_modulesare excluded, unless youmanually configurebabel-loader. |

### Framework and React features

| Feature | Status | Notes |
| --- | --- | --- |
| JSX / TSX | Supported | SWC handles JSX/TSX compilation. |
| Fast Refresh | Supported | No configuration needed. |
| React Server Components (RSC) | Supported | For the Next.js App Router. Turbopack ensures correct server/client bundling. |
| Root layout creation | Unsupported | Automatic creation of a root layout in App Router is not supported. Turbopack will instruct you to create it manually. |

### CSS and styling

| Feature | Status | Notes |
| --- | --- | --- |
| Global CSS | Supported | Import.cssfiles directly in your application. |
| CSS Modules | Supported | .module.cssfiles work natively (Lightning CSS). |
| CSS Nesting | Supported | Lightning CSS supportsmodern CSS nesting. |
| @import syntax | Supported | Combine multiple CSS files. |
| PostCSS | Supported | Automatically processespostcss.config.jsin a Node.js worker pool. Useful for Tailwind, Autoprefixer, etc. |
| Sass / SCSS | Supported(Next.js) | For Next.js, Sass is supported out of the box. Custom Sass functions (sassOptions.functions) are not supported because Turbopack's Rust-based architecture cannot directly execute JavaScript functions, unlike webpack's Node.js environment. Use webpack if you need this feature. In the future, Turbopack standalone usage will likely require a loader config. |
| Less | Planned via plugins | Not yet supported by default. Will likely require a loader config once custom loaders are stable. |
| Lightning CSS | In Use | Handles CSS transformations. Some low-usage CSS Modules features (like:local/:globalas standalone pseudo-classes) are not yet supported.See below for more details. |

### Assets

| Feature | Status | Notes |
| --- | --- | --- |
| Static Assets(images, fonts) | Supported | Importingimport img from './img.png'works out of the box. In Next.js, returns an object for the<Image />component. |
| JSON Imports | Supported | Named or default imports from.jsonare supported. |

### Module resolution

| Feature | Status | Notes |
| --- | --- | --- |
| Path Aliases | Supported | Readstsconfig.json'spathsandbaseUrl, matching Next.js behavior. |
| Manual Aliases | Supported | ConfigureresolveAliasinnext.config.js(similar towebpack.resolve.alias). |
| Custom Extensions | Supported | ConfigureresolveExtensionsinnext.config.js. |
| AMD | Partially Supported | Basic transforms work; advanced AMD usage is limited. |

### Performance and Fast Refresh

| Feature | Status | Notes |
| --- | --- | --- |
| Fast Refresh | Supported | Updates JavaScript, TypeScript, and CSS without a full refresh. |
| Incremental Bundling | Supported | Turbopack lazily builds only what’s requested by the dev server, speeding up large apps. |

## Known gaps with webpack

There are a number of non-trivial behavior differences between webpack and Turbopack that are important to be aware of when migrating an application. Generally, these are less of a concern for new applications.

### Filesystem Root

Turbopack uses the root directory to resolve modules. Files outside of the project root are not resolved.

For example, when linking dependencies outside the project root (via `npm link`, `yarn link`, `pnpm link`, etc.), those linked files will not be resolved by default. To resolve these files, you must configure the root option to the parent directory of both the project and the linked dependencies.

You can configure the filesystem root using [turbopack.root](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#root-directory) option in `next.config.js`.

### CSS Module Ordering

Turbopack will follow JS import order to order [CSS modules](https://nextjs.org/docs/app/getting-started/css#css-modules) which are not otherwise ordered. For example:

 components/BlogPost.jsx

```
import utilStyles from './utils.module.css'
import buttonStyles from './button.module.css'
export default function BlogPost() {
  return (
    <div className={utilStyles.container}>
      <button className={buttonStyles.primary}>Click me</button>
    </div>
  )
}
```

In this example, Turbopack will ensure that `utils.module.css` will appear before `button.module.css` in the produced CSS chunk, following the import order

Webpack generally does this as well, but there are cases where it will ignore JS inferred ordering, for example if it infers the JS file is side-effect-free.

This can lead to subtle rendering changes when adopting Turbopack, if applications have come to rely on an arbitrary ordering. Generally, the solution is easy, e.g. have `button.module.css` `@import utils.module.css` to force the ordering, or identify the conflicting rules and change them to not target the same properties.

### Sass node_modules imports

Turbopack supports importing `node_modules` Sass files out of the box. Webpack supports a legacy tilde `~` syntax for this, which is not supported by Turbopack.

From:

 styles/globals.scss

```
@import '~bootstrap/dist/css/bootstrap.min.css';
```

To:

 styles/globals.scss

```
@import 'bootstrap/dist/css/bootstrap.min.css';
```

If you can't update the imports, you can add a `turbopack.resolveAlias` configuration to map the `~` syntax to the actual path:

 next.config.js

```
module.exports = {
  turbopack: {
    resolveAlias: {
      '~*': '*',
    },
  },
}
```

### Build Caching

Webpack supports [disk build caching](https://webpack.js.org/configuration/cache/#cache) to improve build performance. Turbopack provides a similar feature, currently in beta. Starting with Next 16, you can enable Turbopack’s filesystem cache by setting the following experimental flags:

- [experimental.turbopackFileSystemCacheForDev](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache) is enabled by default
- [experimental.turbopackFileSystemCacheForBuild](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache) is currently opt-in

> **Good to know:** For this reason, when comparing webpack and Turbopack performance, make sure to delete the `.next` folder between builds to see a fair cold build comparison or enable the turbopack filesystem cache feature to compare warm builds.

### Webpack plugins

Turbopack does not support webpack plugins. This affects third-party tools that rely on webpack's plugin system for integration. We do support [webpack loaders](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#configuring-webpack-loaders). If you depend on webpack plugins, you'll need to find Turbopack-compatible alternatives or continue using webpack until equivalent functionality is available.

## Unsupported and unplanned features

Some features are not yet implemented or not planned:

- **Legacy CSS Modules features**
  - Standalone `:local` and `:global` pseudo-classes (only the function variant `:global(...)` is supported).
  - The `@value` rule (superseded by CSS variables).
  - `:import` and `:export` ICSS rules.
  - `composes` in `.module.css` composing a `.css` file. In webpack this would treat the `.css` file as a CSS Module, with Turbopack the `.css` file will always be global. This means that if you want to use `composes` in a CSS Module, you need to change the `.css` file to a `.module.css` file.
  - `@import` in CSS Modules importing `.css` as a CSS Module. In webpack this would treat the `.css` file as a CSS Module, with Turbopack the `.css` file will always be global. This means that if you want to use `@import` in a CSS Module, you need to change the `.css` file to a `.module.css` file.
- **sassOptions.functions**
  Custom Sass functions defined in `sassOptions.functions` are not supported. This feature allows defining JavaScript functions that can be called from Sass code during compilation. Turbopack's Rust-based architecture cannot directly execute JavaScript functions passed through `sassOptions.functions`, unlike webpack's Node.js-based sass-loader which runs entirely in JavaScript. If you're using custom Sass functions, you'll need to use webpack instead of Turbopack.
- **webpack()configuration** in `next.config.js`
  Turbopack replaces webpack, so `webpack()` configs are not recognized. Use the [turbopackconfig](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack) instead.
- **Yarn PnP**
  Not planned for Turbopack support in Next.js.
- **experimental.urlImports**
  Not planned for Turbopack.
- **experimental.esmExternals**
  Not planned. Turbopack does not support the legacy `esmExternals` configuration in Next.js.
- **Some Next.js Experimental Flags**
  - `experimental.nextScriptWorkers`
  - `experimental.sri.algorithm`
  - `experimental.fallbackNodePolyfills`
    We plan to implement these in the future.

For a full, detailed breakdown of each feature flag and its status, see the [Turbopack API Reference](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack).

## Configuration

Turbopack can be configured via `next.config.js` (or `next.config.ts`) under the `turbopack` key. Configuration options include:

- **rules**
  Define additional [webpack loaders](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#configuring-webpack-loaders) for file transformations.
- **resolveAlias**
  Create manual aliases (like `resolve.alias` in webpack).
- **resolveExtensions**
  Change or extend file extensions for module resolution.

 next.config.js

```
module.exports = {
  turbopack: {
    // Example: adding an alias and custom file extension
    resolveAlias: {
      underscore: 'lodash',
    },
    resolveExtensions: ['.mdx', '.tsx', '.ts', '.jsx', '.js', '.json'],
  },
}
```

For more in-depth configuration examples, see the [Turbopack config documentation](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack).

## Generating trace files for performance debugging

If you encounter performance or memory issues and want to help the Next.js team diagnose them, you can generate a trace file by appending `NEXT_TURBOPACK_TRACING=1` to your dev command:

```
NEXT_TURBOPACK_TRACING=1 next dev
```

This will produce a `.next/dev/trace-turbopack` file. Include that file when creating a GitHub issue on the [Next.js repo](https://github.com/vercel/next.js) to help us investigate.

By default the development server outputs to `.next/dev`. Read more about [isolatedDevBuild](https://nextjs.org/docs/app/api-reference/config/next-config-js/isolatedDevBuild).

## Summary

Turbopack is a **Rust-based**, **incremental** bundler designed to make local development and builds fast—especially for large applications. It is integrated into Next.js, offering zero-config CSS, React, and TypeScript support.

## Version Changes

| Version | Changes |
| --- | --- |
| v16.0.0 | Turbopack becomes the default bundler for Next.js. Automatic support for Babel when a configuration file is found. |
| v15.5.0 | Turbopack support forbuildbeta |
| v15.3.0 | Experimental support forbuild |
| v15.0.0 | Turbopack fordevstable |

Was this helpful?

supported.

---

# API Reference

> Next.js API Reference for the Pages Router.

[Next.js Docs](https://nextjs.org/docs)[Pages Router](https://nextjs.org/docs/pages)API ReferenceYou are currently viewing the documentation for Pages Router.

# API Reference

Last updated  April 15, 2025[ComponentsAPI Reference for Next.js built-in components in the Pages Router.](https://nextjs.org/docs/pages/api-reference/components)[File-system conventionsAPI Reference for Next.js file-system conventions.](https://nextjs.org/docs/pages/api-reference/file-conventions)[FunctionsAPI Reference for Functions and Hooks in Pages Router.](https://nextjs.org/docs/pages/api-reference/functions)[ConfigurationLearn how to configure your Next.js application.](https://nextjs.org/docs/pages/api-reference/config)[CLIAPI Reference for the Next.js Command Line Interface (CLI) tools.](https://nextjs.org/docs/pages/api-reference/cli)[Edge RuntimeAPI Reference for the Edge Runtime.](https://nextjs.org/docs/pages/api-reference/edge)[TurbopackTurbopack is an incremental bundler optimized for JavaScript and TypeScript, written in Rust, and built into Next.js.](https://nextjs.org/docs/pages/api-reference/turbopack)

Was this helpful?

supported.

---

# Configuring

> Learn how to configure your Next.js application.

[Pages Router](https://nextjs.org/docs/pages)[Building Your Application](https://nextjs.org/docs/pages/building-your-application)ConfiguringYou are currently viewing the documentation for Pages Router.

# Configuring

Last updated  April 24, 2025

Next.js allows you to customize your project to meet specific requirements. This includes integrations with TypeScript, ESlint, and more, as well as internal configuration options such as Absolute Imports and Environment Variables.

[Error HandlingHandle errors in your Next.js app.](https://nextjs.org/docs/pages/building-your-application/configuring/error-handling)

Was this helpful?

supported.
