# page.js and more

# page.js

> API reference for the page.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)page.js

# page.js

Last updated  October 22, 2025

The `page` file allows you to define UI that is **unique** to a route. You can create a page by default exporting a component from the file:

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export default function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  return <h1>My Page</h1>
}
```

## Good to know

- The `.js`, `.jsx`, or `.tsx` file extensions can be used for `page`.
- A `page` is always the **leaf** of the route subtree.
- A `page` file is required to make a route segment **publicly accessible**.
- Pages are [Server Components](https://react.dev/reference/rsc/server-components) by default, but can be set to a [Client Component](https://react.dev/reference/rsc/use-client).

## Reference

### Props

#### params(optional)

A promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) from the root segment down to that page.

 app/shop/[slug]/page.tsxJavaScriptTypeScript

```
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
}
```

| Example Route | URL | params |
| --- | --- | --- |
| app/shop/[slug]/page.js | /shop/1 | Promise<{ slug: '1' }> |
| app/shop/[category]/[item]/page.js | /shop/1/2 | Promise<{ category: '1', item: '2' }> |
| app/shop/[...slug]/page.js | /shop/1/2 | Promise<{ slug: ['1', '2'] }> |

- Since the `params` prop is a promise, you must use `async/await` or React's [use](https://react.dev/reference/react/use) function to access the values.
  - In version 14 and earlier, `params` was a synchronous prop. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future.

#### searchParams(optional)

A promise that resolves to an object containing the [search parameters](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_URL#parameters) of the current URL. For example:

 app/shop/page.tsxJavaScriptTypeScript

```
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const filters = (await searchParams).filters
}
```

Client Component **pages** can also access `searchParams` using React’s [use](https://react.dev/reference/react/use) hook:

 app/shop/page.tsxJavaScriptTypeScript

```
'use client'
import { use } from 'react'

export default function Page({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const filters = use(searchParams).filters
}
```

| Example URL | searchParams |
| --- | --- |
| /shop?a=1 | Promise<{ a: '1' }> |
| /shop?a=1&b=2 | Promise<{ a: '1', b: '2' }> |
| /shop?a=1&a=2 | Promise<{ a: ['1', '2'] }> |

- Since the `searchParams` prop is a promise. You must use `async/await` or React's [use](https://react.dev/reference/react/use) function to access the values.
  - In version 14 and earlier, `searchParams` was a synchronous prop. To help with backwards compatibility, you can still access it synchronously in Next.js 15, but this behavior will be deprecated in the future.
- `searchParams` is a **Dynamic API** whose values cannot be known ahead of time. Using it will opt the page into **dynamic rendering** at request time.
- `searchParams` is a plain JavaScript object, not a `URLSearchParams` instance.

### Page Props Helper

You can type pages with `PageProps` to get strongly typed `params` and `searchParams` from the route literal. `PageProps` is a globally available helper.

 app/blog/[slug]/page.tsx

```
export default async function Page(props: PageProps<'/blog/[slug]'>) {
  const { slug } = await props.params
  const query = await props.searchParams
  return <h1>Blog Post: {slug}</h1>
}
```

> **Good to know**
>
>
>
> - Using a literal route (e.g. `'/blog/[slug]'`) enables autocomplete and strict keys for `params`.
> - Static routes resolve `params` to `{}`.
> - Types are generated during `next dev`, `next build`, or with `next typegen`.
> - After type generation, the `PageProps` helper is globally available. It doesn't need to be imported.

## Examples

### Displaying content based onparams

Using [dynamic route segments](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes), you can display or fetch specific content for the page based on the `params` prop.

 app/blog/[slug]/page.tsxJavaScriptTypeScript

```
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <h1>Blog Post: {slug}</h1>
}
```

### Handling filtering withsearchParams

You can use the `searchParams` prop to handle filtering, pagination, or sorting based on the query string of the URL.

 app/shop/page.tsxJavaScriptTypeScript

```
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const { page = '1', sort = 'asc', query = '' } = await searchParams

  return (
    <div>
      <h1>Product Listing</h1>
      <p>Search query: {query}</p>
      <p>Current page: {page}</p>
      <p>Sort order: {sort}</p>
    </div>
  )
}
```

### ReadingsearchParamsandparamsin Client Components

To use `searchParams` and `params` in a Client Component (which cannot be `async`), you can use React's [use](https://react.dev/reference/react/use) function to read the promise:

 app/page.tsxJavaScriptTypeScript

```
'use client'

import { use } from 'react'

export default function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const { slug } = use(params)
  const { query } = use(searchParams)
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.0.0-RC | paramsandsearchParamsare now promises. Acodemodis available. |
| v13.0.0 | pageintroduced. |

Was this helpful?

supported.

---

# Parallel Routes

> Simultaneously render one or more pages in the same view that can be navigated independently. A pattern for highly dynamic applications.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)Parallel Routes

# Parallel Routes

Last updated  October 22, 2025

Parallel Routes allows you to simultaneously or conditionally render one or more pages within the same layout. They are useful for highly dynamic sections of an app, such as dashboards and feeds on social sites.

For example, considering a dashboard, you can use parallel routes to simultaneously render the `team` and `analytics` pages:

 ![Parallel Routes Diagram](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fparallel-routes.png&w=3840&q=75)![Parallel Routes Diagram](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fparallel-routes.png&w=3840&q=75)

## Convention

### Slots

Parallel routes are created using named **slots**. Slots are defined with the `@folder` convention. For example, the following file structure defines two slots: `@analytics` and `@team`:

 ![Parallel Routes File-system Structure](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fparallel-routes-file-system.png&w=3840&q=75)![Parallel Routes File-system Structure](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fparallel-routes-file-system.png&w=3840&q=75)

Slots are passed as props to the shared parent layout. For the example above, the component in `app/layout.js` now accepts the `@analytics` and `@team` slots props, and can render them in parallel alongside the `children` prop:

 app/layout.tsxJavaScriptTypeScript

```
export default function Layout({
  children,
  team,
  analytics,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <>
      {children}
      {team}
      {analytics}
    </>
  )
}
```

However, slots are **not** route segments and do not affect the URL structure. For example, for `/@analytics/views`, the URL will be `/views` since `@analytics` is a slot. Slots are combined with the regular [Page](https://nextjs.org/docs/app/api-reference/file-conventions/page) component to form the final page associated with the route segment. Because of this, you cannot have separate [static](https://nextjs.org/docs/app/guides/caching#static-rendering) and [dynamic](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) slots at the same route segment level. If one slot is dynamic, all slots at that level must be dynamic.

> **Good to know**:
>
>
>
> - The `children` prop is an implicit slot that does not need to be mapped to a folder. This means `app/page.js` is equivalent to `app/@children/page.js`.

### default.js

You can define a `default.js` file to render as a fallback for unmatched slots during the initial load or full-page reload.

Consider the following folder structure. The `@team` slot has a `/settings` page, but `@analytics` does not.

 ![Parallel Routes unmatched routes](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fparallel-routes-unmatched-routes.png&w=3840&q=75)![Parallel Routes unmatched routes](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fparallel-routes-unmatched-routes.png&w=3840&q=75)

When navigating to `/settings`, the `@team` slot will render the `/settings` page while maintaining the currently active page for the `@analytics` slot.

On refresh, Next.js will render a `default.js` for `@analytics`. If `default.js` doesn't exist, a `404` is rendered instead.

Additionally, since `children` is an implicit slot, you also need to create a `default.js` file to render a fallback for `children` when Next.js cannot recover the active state of the parent page.

## Behavior

By default, Next.js keeps track of the active *state* (or subpage) for each slot. However, the content rendered within a slot will depend on the type of navigation:

- [Soft Navigation](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions): During client-side navigation, Next.js will perform a [partial render](https://nextjs.org/docs/app/getting-started/linking-and-navigating#client-side-transitions), changing the subpage within the slot, while maintaining the other slot's active subpages, even if they don't match the current URL.
- **Hard Navigation**: After a full-page load (browser refresh), Next.js cannot determine the active state for the slots that don't match the current URL. Instead, it will render a [default.js](#defaultjs) file for the unmatched slots, or `404` if `default.js` doesn't exist.

> **Good to know**:
>
>
>
> - The `404` for unmatched routes helps ensure that you don't accidentally render a parallel route on a page that it was not intended for.

## Examples

### WithuseSelectedLayoutSegment(s)

Both [useSelectedLayoutSegment](https://nextjs.org/docs/app/api-reference/functions/use-selected-layout-segment) and [useSelectedLayoutSegments](https://nextjs.org/docs/app/api-reference/functions/use-selected-layout-segments) accept a `parallelRoutesKey` parameter, which allows you to read the active route segment within a slot.

 app/layout.tsxJavaScriptTypeScript

```
'use client'

import { useSelectedLayoutSegment } from 'next/navigation'

export default function Layout({ auth }: { auth: React.ReactNode }) {
  const loginSegment = useSelectedLayoutSegment('auth')
  // ...
}
```

When a user navigates to `app/@auth/login` (or `/login` in the URL bar), `loginSegment` will be equal to the string `"login"`.

### Conditional Routes

You can use Parallel Routes to conditionally render routes based on certain conditions, such as user role. For example, to render a different dashboard page for the `/admin` or `/user` roles:

 ![Conditional routes diagram](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fconditional-routes-ui.png&w=3840&q=75)![Conditional routes diagram](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fconditional-routes-ui.png&w=3840&q=75) app/dashboard/layout.tsxJavaScriptTypeScript

```
import { checkUserRole } from '@/lib/auth'

export default function Layout({
  user,
  admin,
}: {
  user: React.ReactNode
  admin: React.ReactNode
}) {
  const role = checkUserRole()
  return role === 'admin' ? admin : user
}
```

### Tab Groups

You can add a `layout` inside a slot to allow users to navigate the slot independently. This is useful for creating tabs.

For example, the `@analytics` slot has two subpages: `/page-views` and `/visitors`.

 ![Analytics slot with two subpages and a layout](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fparallel-routes-tab-groups.png&w=3840&q=75)![Analytics slot with two subpages and a layout](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fparallel-routes-tab-groups.png&w=3840&q=75)

Within `@analytics`, create a [layout](https://nextjs.org/docs/app/api-reference/file-conventions/layout) file to share the tabs between the two pages:

 app/@analytics/layout.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <nav>
        <Link href="/page-views">Page Views</Link>
        <Link href="/visitors">Visitors</Link>
      </nav>
      <div>{children}</div>
    </>
  )
}
```

### Modals

Parallel Routes can be used together with [Intercepting Routes](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes) to create modals that support deep linking. This allows you to solve common challenges when building modals, such as:

- Making the modal content **shareable through a URL**.
- **Preserving context** when the page is refreshed, instead of closing the modal.
- **Closing the modal on backwards navigation** rather than going to the previous route.
- **Reopening the modal on forwards navigation**.

Consider the following UI pattern, where a user can open a login modal from a layout using client-side navigation, or access a separate `/login` page:

 ![Parallel Routes Diagram](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fparallel-routes-auth-modal.png&w=3840&q=75)![Parallel Routes Diagram](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fparallel-routes-auth-modal.png&w=3840&q=75)

To implement this pattern, start by creating a `/login` route that renders your **main** login page.

 ![Parallel Routes Diagram](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fparallel-routes-modal-login-page.png&w=3840&q=75)![Parallel Routes Diagram](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fparallel-routes-modal-login-page.png&w=3840&q=75) app/login/page.tsxJavaScriptTypeScript

```
import { Login } from '@/app/ui/login'

export default function Page() {
  return <Login />
}
```

Then, inside the `@auth` slot, add [default.js](https://nextjs.org/docs/app/api-reference/file-conventions/default) file that returns `null`. This ensures that the modal is not rendered when it's not active.

 app/@auth/default.tsxJavaScriptTypeScript

```
export default function Default() {
  return null
}
```

Inside your `@auth` slot, intercept the `/login` route by importing the `<Modal>` component and its children into the `@auth/(.)login/page.tsx` file, and updating the folder name to `/@auth/(.)login/page.tsx`.

 app/@auth/(.)login/page.tsxJavaScriptTypeScript

```
import { Modal } from '@/app/ui/modal'
import { Login } from '@/app/ui/login'

export default function Page() {
  return (
    <Modal>
      <Login />
    </Modal>
  )
}
```

> **Good to know:**
>
>
>
> - The convention `(.)` is used for intercepting routes. See [Intercepting Routes](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes#convention) docs for more information.
> - By separating the `<Modal>` functionality from the modal content (`<Login>`), you can ensure any content inside the modal, e.g. [forms](https://nextjs.org/docs/app/guides/forms), are Server Components. See [Interleaving Client and Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components#examples#supported-pattern-passing-server-components-to-client-components-as-props) for more information.

#### Opening the modal

Now, you can leverage the Next.js router to open and close the modal. This ensures the URL is correctly updated when the modal is open, and when navigating backwards and forwards.

To open the modal, pass the `@auth` slot as a prop to the parent layout and render it alongside the `children` prop.

 app/layout.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Layout({
  auth,
  children,
}: {
  auth: React.ReactNode
  children: React.ReactNode
}) {
  return (
    <>
      <nav>
        <Link href="/login">Open modal</Link>
      </nav>
      <div>{auth}</div>
      <div>{children}</div>
    </>
  )
}
```

When the user clicks the `<Link>`, the modal will open instead of navigating to the `/login` page. However, on refresh or initial load, navigating to `/login` will take the user to the main login page.

#### Closing the modal

You can close the modal by calling `router.back()` or by using the `Link` component.

 app/ui/modal.tsxJavaScriptTypeScript

```
'use client'

import { useRouter } from 'next/navigation'

export function Modal({ children }: { children: React.ReactNode }) {
  const router = useRouter()

  return (
    <>
      <button
        onClick={() => {
          router.back()
        }}
      >
        Close modal
      </button>
      <div>{children}</div>
    </>
  )
}
```

When using the `Link` component to navigate away from a page that shouldn't render the `@auth` slot anymore, we need to make sure the parallel route matches to a component that returns `null`. For example, when navigating back to the root page, we create a `@auth/page.tsx` component:

 app/ui/modal.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export function Modal({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Link href="/">Close modal</Link>
      <div>{children}</div>
    </>
  )
}
```

   app/@auth/page.tsxJavaScriptTypeScript

```
export default function Page() {
  return null
}
```

Or if navigating to any other page (such as `/foo`, `/foo/bar`, etc), you can use a catch-all slot:

 app/@auth/[...catchAll]/page.tsxJavaScriptTypeScript

```
export default function CatchAll() {
  return null
}
```

> **Good to know:**
>
>
>
> - We use a catch-all route in our `@auth` slot to close the modal because of how parallel routes behave. Since client-side navigations to a route that no longer match the slot will remain visible, we need to match the slot to a route that returns `null` to close the modal.
> - Other examples could include opening a photo modal in a gallery while also having a dedicated `/photo/[id]` page, or opening a shopping cart in a side modal.
> - [View an example](https://github.com/vercel-labs/nextgram) of modals with Intercepted and Parallel Routes.

### Loading and Error UI

Parallel Routes can be streamed independently, allowing you to define independent error and loading states for each route:

 ![Parallel routes enable custom error and loading states](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fparallel-routes-cinematic-universe.png&w=3840&q=75)![Parallel routes enable custom error and loading states](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fparallel-routes-cinematic-universe.png&w=3840&q=75)

See the [Loading UI](https://nextjs.org/docs/app/api-reference/file-conventions/loading) and [Error Handling](https://nextjs.org/docs/app/getting-started/error-handling) documentation for more information.

[default.jsAPI Reference for the default.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/default)

Was this helpful?

supported.

---

# proxy.js

> API reference for the proxy.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)proxy.js

# proxy.js

Last updated  November 4, 2025

> **Note**: The `middleware` file convention is deprecated and has been renamed to `proxy`. See [Migration to Proxy](#migration-to-proxy) for more details.

The `proxy.js|ts` file is used to write [Proxy](https://nextjs.org/docs/app/getting-started/proxy) and run code on the server before a request is completed. Then, based on the incoming request, you can modify the response by rewriting, redirecting, modifying the request or response headers, or responding directly.

Proxy executes before routes are rendered. It's particularly useful for implementing custom server-side logic like authentication, logging, or handling redirects.

> **Good to know**:
>
>
>
> Proxy is meant to be invoked separately of your render code and in optimized cases deployed to your CDN for fast redirect/rewrite handling, you should not attempt relying on shared modules or globals.
>
>
>
> To pass information from Proxy to your application, use [headers](#setting-headers), [cookies](#using-cookies), [rewrites](https://nextjs.org/docs/app/api-reference/functions/next-response#rewrite), [redirects](https://nextjs.org/docs/app/api-reference/functions/next-response#redirect), or the URL.

Create a `proxy.ts` (or `.js`) file in the project root, or inside `src` if applicable, so that it is located at the same level as `pages` or `app`.

If you’ve customized [pageExtensions](https://nextjs.org/docs/app/api-reference/config/next-config-js/pageExtensions), for example to `.page.ts` or `.page.js`, name your file `proxy.page.ts` or `proxy.page.js` accordingly.

 proxy.tsJavaScriptTypeScript

```
import { NextResponse, NextRequest } from 'next/server'

// This function can be marked `async` if using `await` inside
export function proxy(request: NextRequest) {
  return NextResponse.redirect(new URL('/home', request.url))
}

export const config = {
  matcher: '/about/:path*',
}
```

## Exports

### Proxy function

The file must export a single function, either as a default export or named `proxy`. Note that multiple proxy from the same file are not supported.

 proxy.js

```
// Example of default export
export default function proxy(request) {
  // Proxy logic
}
```

### Config object (optional)

Optionally, a config object can be exported alongside the Proxy function. This object includes the [matcher](#matcher) to specify paths where the Proxy applies.

### Matcher

The `matcher` option allows you to target specific paths for the Proxy to run on. You can specify these paths in several ways:

- For a single path: Directly use a string to define the path, like `'/about'`.
- For multiple paths: Use an array to list multiple paths, such as `matcher: ['/about', '/contact']`, which applies the Proxy to both `/about` and `/contact`.

 proxy.js

```
export const config = {
  matcher: ['/about/:path*', '/dashboard/:path*'],
}
```

Additionally, the `matcher` option supports complex path specifications using regular expressions. For example, you can exclude certain paths with a regular expression matcher:

 proxy.js

```
export const config = {
  matcher: [
    // Exclude API routes, static files, image optimizations, and .png files
    '/((?!api|_next/static|_next/image|.*\\.png$).*)',
  ],
}
```

This enables precise control over which paths to include or exclude.

The `matcher` option accepts an array of objects with the following keys:

- `source`: The path or pattern used to match the request paths. It can be a string for direct path matching or a pattern for more complex matching.
- `locale` (optional): A boolean that, when set to `false`, ignores locale-based routing in path matching.
- `has` (optional): Specifies conditions based on the presence of specific request elements such as headers, query parameters, or cookies.
- `missing` (optional): Focuses on conditions where certain request elements are absent, like missing headers or cookies.

 proxy.js

```
export const config = {
  matcher: [
    {
      source: '/api/:path*',
      locale: false,
      has: [
        { type: 'header', key: 'Authorization', value: 'Bearer Token' },
        { type: 'query', key: 'userId', value: '123' },
      ],
      missing: [{ type: 'cookie', key: 'session', value: 'active' }],
    },
  ],
}
```

Configured matchers:

1. MUST start with `/`
2. Can include named parameters: `/about/:path` matches `/about/a` and `/about/b` but not `/about/a/c`
3. Can have modifiers on named parameters (starting with `:`): `/about/:path*` matches `/about/a/b/c` because `*` is *zero or more*. `?` is *zero or one* and `+` *one or more*
4. Can use regular expression enclosed in parenthesis: `/about/(.*)` is the same as `/about/:path*`
5. Are anchored to the start of the path: `/about` matches `/about` and `/about/team` but not `/blog/about`

Read more details on [path-to-regexp](https://github.com/pillarjs/path-to-regexp#path-to-regexp-1) documentation.

> **Good to know**:
>
>
>
> - The `matcher` values need to be constants so they can be statically analyzed at build-time. Dynamic values such as variables will be ignored.
> - For backward compatibility, Next.js always considers `/public` as `/public/index`. Therefore, a matcher of `/public/:path` will match.

## Params

### request

When defining Proxy, the default export function accepts a single parameter, `request`. This parameter is an instance of `NextRequest`, which represents the incoming HTTP request.

 proxy.tsJavaScriptTypeScript

```
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Proxy logic goes here
}
```

> **Good to know**:
>
>
>
> - `NextRequest` is a type that represents incoming HTTP requests in Next.js Proxy, whereas [NextResponse](#nextresponse) is a class used to manipulate and send back HTTP responses.

## NextResponse

The `NextResponse` API allows you to:

- `redirect` the incoming request to a different URL
- `rewrite` the response by displaying a given URL
- Set request headers for API Routes, `getServerSideProps`, and `rewrite` destinations
- Set response cookies
- Set response headers

To produce a response from Proxy, you can:

1. `rewrite` to a route ([Page](https://nextjs.org/docs/app/api-reference/file-conventions/page) or [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route)) that produces a response
2. return a `NextResponse` directly. See [Producing a Response](#producing-a-response)

> **Good to know**: For redirects, you can also use `Response.redirect` instead of `NextResponse.redirect`.

## Execution order

Proxy will be invoked for **every route in your project**. Given this, it's crucial to use [matchers](#matcher) to precisely target or exclude specific routes. The following is the execution order:

1. `headers` from `next.config.js`
2. `redirects` from `next.config.js`
3. Proxy (`rewrites`, `redirects`, etc.)
4. `beforeFiles` (`rewrites`) from `next.config.js`
5. Filesystem routes (`public/`, `_next/static/`, `pages/`, `app/`, etc.)
6. `afterFiles` (`rewrites`) from `next.config.js`
7. Dynamic Routes (`/blog/[slug]`)
8. `fallback` (`rewrites`) from `next.config.js`

## Runtime

Proxy defaults to using the Node.js runtime. The [runtime](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#runtime) config option is not available in Proxy files. Setting the `runtime` config option in Proxy will throw an error.

## Advanced Proxy flags

In `v13.1` of Next.js two additional flags were introduced for proxy, `skipMiddlewareUrlNormalize` and `skipTrailingSlashRedirect` to handle advanced use cases.

`skipTrailingSlashRedirect` disables Next.js redirects for adding or removing trailing slashes. This allows custom handling inside proxy to maintain the trailing slash for some paths but not others, which can make incremental migrations easier.

 next.config.js

```
module.exports = {
  skipTrailingSlashRedirect: true,
}
```

 proxy.js

```
const legacyPrefixes = ['/docs', '/blog']

export default async function proxy(req) {
  const { pathname } = req.nextUrl

  if (legacyPrefixes.some((prefix) => pathname.startsWith(prefix))) {
    return NextResponse.next()
  }

  // apply trailing slash handling
  if (
    !pathname.endsWith('/') &&
    !pathname.match(/((?!\.well-known(?:\/.*)?)(?:[^/]+\/)*[^/]+\.\w+)/)
  ) {
    return NextResponse.redirect(
      new URL(`${req.nextUrl.pathname}/`, req.nextUrl)
    )
  }
}
```

`skipMiddlewareUrlNormalize` allows for disabling the URL normalization in Next.js to make handling direct visits and client-transitions the same. In some advanced cases, this option provides full control by using the original URL.

 next.config.js

```
module.exports = {
  skipMiddlewareUrlNormalize: true,
}
```

 proxy.js

```
export default async function proxy(req) {
  const { pathname } = req.nextUrl

  // GET /_next/data/build-id/hello.json

  console.log(pathname)
  // with the flag this now /_next/data/build-id/hello.json
  // without the flag this would be normalized to /hello
}
```

## Examples

### Conditional Statements

 proxy.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/about')) {
    return NextResponse.rewrite(new URL('/about-2', request.url))
  }

  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.rewrite(new URL('/dashboard/user', request.url))
  }
}
```

### Using Cookies

Cookies are regular headers. On a `Request`, they are stored in the `Cookie` header. On a `Response` they are in the `Set-Cookie` header. Next.js provides a convenient way to access and manipulate these cookies through the `cookies` extension on `NextRequest` and `NextResponse`.

1. For incoming requests, `cookies` comes with the following methods: `get`, `getAll`, `set`, and `delete` cookies. You can check for the existence of a cookie with `has` or remove all cookies with `clear`.
2. For outgoing responses, `cookies` have the following methods `get`, `getAll`, `set`, and `delete`.

 proxy.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Assume a "Cookie:nextjs=fast" header to be present on the incoming request
  // Getting cookies from the request using the `RequestCookies` API
  let cookie = request.cookies.get('nextjs')
  console.log(cookie) // => { name: 'nextjs', value: 'fast', Path: '/' }
  const allCookies = request.cookies.getAll()
  console.log(allCookies) // => [{ name: 'nextjs', value: 'fast' }]

  request.cookies.has('nextjs') // => true
  request.cookies.delete('nextjs')
  request.cookies.has('nextjs') // => false

  // Setting cookies on the response using the `ResponseCookies` API
  const response = NextResponse.next()
  response.cookies.set('vercel', 'fast')
  response.cookies.set({
    name: 'vercel',
    value: 'fast',
    path: '/',
  })
  cookie = response.cookies.get('vercel')
  console.log(cookie) // => { name: 'vercel', value: 'fast', Path: '/' }
  // The outgoing response will have a `Set-Cookie:vercel=fast;path=/` header.

  return response
}
```

### Setting Headers

You can set request and response headers using the `NextResponse` API (setting *request* headers is available since Next.js v13.0.0).

 proxy.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Clone the request headers and set a new header `x-hello-from-proxy1`
  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-hello-from-proxy1', 'hello')

  // You can also set request headers in NextResponse.next
  const response = NextResponse.next({
    request: {
      // New request headers
      headers: requestHeaders,
    },
  })

  // Set a new response header `x-hello-from-proxy2`
  response.headers.set('x-hello-from-proxy2', 'hello')
  return response
}
```

Note that the snippet uses:

- `NextResponse.next({ request: { headers: requestHeaders } })` to make `requestHeaders` available upstream
- **NOT** `NextResponse.next({ headers: requestHeaders })` which makes `requestHeaders` available to clients

Learn more in [NextResponse headers in Proxy](https://nextjs.org/docs/app/api-reference/functions/next-response#next).

> **Good to know**: Avoid setting large headers as it might cause [431 Request Header Fields Too Large](https://developer.mozilla.org/docs/Web/HTTP/Status/431) error depending on your backend web server configuration.

### CORS

You can set CORS headers in Proxy to allow cross-origin requests, including [simple](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests) and [preflighted](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#preflighted_requests) requests.

 proxy.tsJavaScriptTypeScript

```
import { NextRequest, NextResponse } from 'next/server'

const allowedOrigins = ['https://acme.com', 'https://my-app.org']

const corsOptions = {
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}

export function proxy(request: NextRequest) {
  // Check the origin from the request
  const origin = request.headers.get('origin') ?? ''
  const isAllowedOrigin = allowedOrigins.includes(origin)

  // Handle preflighted requests
  const isPreflight = request.method === 'OPTIONS'

  if (isPreflight) {
    const preflightHeaders = {
      ...(isAllowedOrigin && { 'Access-Control-Allow-Origin': origin }),
      ...corsOptions,
    }
    return NextResponse.json({}, { headers: preflightHeaders })
  }

  // Handle simple requests
  const response = NextResponse.next()

  if (isAllowedOrigin) {
    response.headers.set('Access-Control-Allow-Origin', origin)
  }

  Object.entries(corsOptions).forEach(([key, value]) => {
    response.headers.set(key, value)
  })

  return response
}

export const config = {
  matcher: '/api/:path*',
}
```

> **Good to know:** You can configure CORS headers for individual routes in [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route#cors).

### Producing a response

You can respond from Proxy directly by returning a `Response` or `NextResponse` instance. (This is available since [Next.js v13.1.0](https://nextjs.org/blog/next-13-1#nextjs-advanced-proxy))

 proxy.tsJavaScriptTypeScript

```
import type { NextRequest } from 'next/server'
import { isAuthenticated } from '@lib/auth'

// Limit the proxy to paths starting with `/api/`
export const config = {
  matcher: '/api/:function*',
}

export function proxy(request: NextRequest) {
  // Call our authentication function to check the request
  if (!isAuthenticated(request)) {
    // Respond with JSON indicating an error message
    return Response.json(
      { success: false, message: 'authentication failed' },
      { status: 401 }
    )
  }
}
```

### Negative matching

The `matcher` config allows full regex so matching like negative lookaheads or character matching is supported. An example of a negative lookahead to match all except specific paths can be seen here:

 proxy.js

```
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, sitemap.xml, robots.txt (metadata files)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
  ],
}
```

You can also bypass Proxy for certain requests by using the `missing` or `has` arrays, or a combination of both:

 proxy.js

```
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, sitemap.xml, robots.txt (metadata files)
     */
    {
      source:
        '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },

    {
      source:
        '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
      has: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },

    {
      source:
        '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
      has: [{ type: 'header', key: 'x-present' }],
      missing: [{ type: 'header', key: 'x-missing', value: 'prefetch' }],
    },
  ],
}
```

> **Good to know**:
>
>
>
> Even when `_next/data` is excluded in a negative matcher pattern, proxy will still be invoked for `_next/data` routes. This is intentional behavior to prevent accidental security issues where you might protect a page but forget to protect the corresponding data route.

 proxy.js

```
export const config = {
  matcher:
    '/((?!api|_next/data|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
}

// Proxy will still run for /_next/data/* routes despite being excluded
```

### waitUntilandNextFetchEvent

The `NextFetchEvent` object extends the native [FetchEvent](https://developer.mozilla.org/docs/Web/API/FetchEvent) object, and includes the [waitUntil()](https://developer.mozilla.org/docs/Web/API/ExtendableEvent/waitUntil) method.

The `waitUntil()` method takes a promise as an argument, and extends the lifetime of the Proxy until the promise settles. This is useful for performing work in the background.

 proxy.ts

```
import { NextResponse } from 'next/server'
import type { NextFetchEvent, NextRequest } from 'next/server'

export function proxy(req: NextRequest, event: NextFetchEvent) {
  event.waitUntil(
    fetch('https://my-analytics-platform.com', {
      method: 'POST',
      body: JSON.stringify({ pathname: req.nextUrl.pathname }),
    })
  )

  return NextResponse.next()
}
```

### Unit testing (experimental)

Starting in Next.js 15.1, the `next/experimental/testing/server` package contains utilities to help unit test proxy files. Unit testing proxy can help ensure that it's only run on desired paths and that custom routing logic works as intended before code reaches production.

The `unstable_doesProxyMatch` function can be used to assert whether proxy will run for the provided URL, headers, and cookies.

```
import { unstable_doesProxyMatch } from 'next/experimental/testing/server'

expect(
  unstable_doesProxyMatch({
    config,
    nextConfig,
    url: '/test',
  })
).toEqual(false)
```

The entire proxy function can also be tested.

```
import { isRewrite, getRewrittenUrl } from 'next/experimental/testing/server'

const request = new NextRequest('https://nextjs.org/docs')
const response = await proxy(request)
expect(isRewrite(response)).toEqual(true)
expect(getRewrittenUrl(response)).toEqual('https://other-domain.com/docs')
// getRedirectUrl could also be used if the response were a redirect
```

## Platform support

| Deployment Option | Supported |
| --- | --- |
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

Learn how to [configure Proxy](https://nextjs.org/docs/app/guides/self-hosting#proxy) when self-hosting Next.js.

## Migration to Proxy

### Why the Change

The reason behind the renaming of `middleware` is that the term "middleware" can often be confused with Express.js middleware, leading to a misinterpretation of its purpose. Also, Middleware is highly capable, so it may encourage the usage; however, this feature is recommended to be used as a last resort.

Next.js is moving forward to provide better APIs with better ergonomics so that developers can achieve their goals without Middleware. This is the reason behind the renaming of `middleware`.

### Why "Proxy"

The name Proxy clarifies what Middleware is capable of. The term "proxy" implies that it has a network boundary in front of the app, which is the behavior of Middleware. Also, Middleware defaults to run at the [Edge Runtime](https://nextjs.org/docs/app/api-reference/edge), which can run closer to the client, separated from the app's region. These behaviors align better with the term "proxy" and provide a clearer purpose of the feature.

### How to Migrate

We recommend users avoid relying on Middleware unless no other options exist. Our goal is to give them APIs with better ergonomics so they can achieve their goals without Middleware.

The term “middleware” often confuses users with Express.js middleware, which can encourage misuse. To clarify our direction, we are renaming the file convention to “proxy.” This highlights that we are moving away from Middleware, breaking down its overloaded features, and making the Proxy clear in its purpose.

Next.js provides a codemod to migrate from `middleware.ts` to `proxy.ts`. You can run the following command to migrate:

```
npx @next/codemod@canary middleware-to-proxy .
```

The codemod will rename the file and the function name from `middleware` to `proxy`.

```
// middleware.ts -> proxy.ts

- export function middleware() {
+ export function proxy() {
```

## Version history

| Version | Changes |
| --- | --- |
| v16.0.0 | Middleware is deprecated and renamed to Proxy |
| v15.5.0 | Middleware can now use the Node.js runtime (stable) |
| v15.2.0 | Middleware can now use the Node.js runtime (experimental) |
| v13.1.0 | Advanced Middleware flags added |
| v13.0.0 | Middleware can modify request headers, response headers, and send responses |
| v12.2.0 | Middleware is stable, please see theupgrade guide |
| v12.0.9 | Enforce absolute URLs in Edge Runtime (PR) |
| v12.0.0 | Middleware (Beta) added |

## Learn more about Proxy

[NextRequestAPI Reference for NextRequest.](https://nextjs.org/docs/app/api-reference/functions/next-request)[NextResponseAPI Reference for NextResponse.](https://nextjs.org/docs/app/api-reference/functions/next-response)

Was this helpful?

supported.

---

# public Folder

> Next.js allows you to serve static files, like images, in the public directory. You can learn how it works here.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)public

# public Folder

Last updated  June 16, 2025

Next.js can serve static files, like images, under a folder called `public` in the root directory. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

For example, the file `public/avatars/me.png` can be viewed by visiting the `/avatars/me.png` path. The code to display that image might look like:

 avatar.js

```
import Image from 'next/image'

export function Avatar({ id, alt }) {
  return <Image src={`/avatars/${id}.png`} alt={alt} width="64" height="64" />
}

export function AvatarOfMe() {
  return <Avatar id="me" alt="A portrait of me" />
}
```

## Caching

Next.js cannot safely cache assets in the `public` folder because they may change. The default caching headers applied are:

```
Cache-Control: public, max-age=0
```

## Robots, Favicons, and others

For static metadata files, such as `robots.txt`, `favicon.ico`, etc, you should use [special metadata files](https://nextjs.org/docs/app/api-reference/file-conventions/metadata) inside the `app` folder.

Was this helpful?

supported.

---

# Route Groups

> Route Groups can be used to partition your Next.js application into different sections.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)Route Groups

# Route Groups

Last updated  June 16, 2025

Route Groups are a folder convention that let you organize routes by category or team.

## Convention

A route group can be created by wrapping a folder's name in parenthesis: `(folderName)`.

This convention indicates the folder is for organizational purposes and should **not be included** in the route's URL path.

 ![An example folder structure using route groups](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-route-groups.png&w=3840&q=75)![An example folder structure using route groups](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-route-groups.png&w=3840&q=75)

## Use cases

- Organizing routes by team, concern, or feature.
- Defining multiple [root layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout).
- Opting specific route segments into sharing a layout, while keeping others out.

## Caveats

- **Full page load**: If you navigate between routes that use different root layouts, it'll trigger a full page reload. For example, navigating from `/cart` that uses `app/(shop)/layout.js` to `/blog` that uses `app/(marketing)/layout.js`. This **only** applies to multiple root layouts.
- **Conflicting paths**: Routes in different groups should not resolve to the same URL path. For example, `(marketing)/about/page.js` and `(shop)/about/page.js` would both resolve to `/about` and cause an error.
- **Top-level root layout**: If you use multiple root layouts without a top-level `layout.js` file, make sure your home route (/) is defined within one of the route groups, e.g. app/(marketing)/page.js.

Was this helpful?

supported.
