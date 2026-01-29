# Project structure and organization and more

# Project structure and organization

> Learn the folder and file conventions in Next.js, and how to organize your project.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Project Structure

# Project structure and organization

Last updated  December 9, 2025

This page provides an overview of **all** the folder and file conventions in Next.js, and recommendations for organizing your project.

## Folder and file conventions

### Top-level folders

Top-level folders are used to organize your application's code and static assets.

 ![Route segments to path segments](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ftop-level-folders.png&w=3840&q=75)![Route segments to path segments](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ftop-level-folders.png&w=3840&q=75)

|  |  |
| --- | --- |
| app | App Router |
| pages | Pages Router |
| public | Static assets to be served |
| src | Optional application source folder |

### Top-level files

Top-level files are used to configure your application, manage dependencies, run proxy, integrate monitoring tools, and define environment variables.

|  |  |
| --- | --- |
| Next.js |  |
| next.config.js | Configuration file for Next.js |
| package.json | Project dependencies and scripts |
| instrumentation.ts | OpenTelemetry and Instrumentation file |
| proxy.ts | Next.js request proxy |
| .env | Environment variables (should not be tracked by version control) |
| .env.local | Local environment variables (should not be tracked by version control) |
| .env.production | Production environment variables (should not be tracked by version control) |
| .env.development | Development environment variables (should not be tracked by version control) |
| eslint.config.mjs | Configuration file for ESLint |
| .gitignore | Git files and folders to ignore |
| next-env.d.ts | TypeScript declaration file for Next.js (should not be tracked by version control) |
| tsconfig.json | Configuration file for TypeScript |
| jsconfig.json | Configuration file for JavaScript |

### Routing Files

Add `page` to expose a route, `layout` for shared UI such as header, nav, or footer, `loading` for skeletons, `error` for error boundaries, and `route` for APIs.

|  |  |  |
| --- | --- | --- |
| layout | .js.jsx.tsx | Layout |
| page | .js.jsx.tsx | Page |
| loading | .js.jsx.tsx | Loading UI |
| not-found | .js.jsx.tsx | Not found UI |
| error | .js.jsx.tsx | Error UI |
| global-error | .js.jsx.tsx | Global error UI |
| route | .js.ts | API endpoint |
| template | .js.jsx.tsx | Re-rendered layout |
| default | .js.jsx.tsx | Parallel route fallback page |

### Nested routes

Folders define URL segments. Nesting folders nests segments. Layouts at any level wrap their child segments. A route becomes public when a `page` or `route` file exists.

| Path | URL pattern | Notes |
| --- | --- | --- |
| app/layout.tsx | — | Root layout wraps all routes |
| app/blog/layout.tsx | — | Wraps/blogand descendants |
| app/page.tsx | / | Public route |
| app/blog/page.tsx | /blog | Public route |
| app/blog/authors/page.tsx | /blog/authors | Public route |

### Dynamic routes

Parameterize segments with square brackets. Use `[segment]` for a single param, `[...segment]` for catch‑all, and `[[...segment]]` for optional catch‑all. Access values via the [params](https://nextjs.org/docs/app/api-reference/file-conventions/page#params-optional) prop.

| Path | URL pattern |
| --- | --- |
| app/blog/[slug]/page.tsx | /blog/my-first-post |
| app/shop/[...slug]/page.tsx | /shop/clothing,/shop/clothing/shirts |
| app/docs/[[...slug]]/page.tsx | /docs,/docs/layouts-and-pages,/docs/api-reference/use-router |

### Route groups and private folders

Organize code without changing URLs with route groups [(group)](https://nextjs.org/docs/app/api-reference/file-conventions/route-groups#convention), and colocate non-routable files with private folders [_folder](#private-folders).

| Path | URL pattern | Notes |
| --- | --- | --- |
| app/(marketing)/page.tsx | / | Group omitted from URL |
| app/(shop)/cart/page.tsx | /cart | Share layouts within(shop) |
| app/blog/_components/Post.tsx | — | Not routable; safe place for UI utilities |
| app/blog/_lib/data.ts | — | Not routable; safe place for utils |

### Parallel and Intercepted Routes

These features fit specific UI patterns, such as slot-based layouts or modal routing.

Use `@slot` for named slots rendered by a parent layout. Use intercept patterns to render another route inside the current layout without changing the URL, for example, to show a details view as a modal over a list.

| Pattern (docs) | Meaning | Typical use case |
| --- | --- | --- |
| @folder | Named slot | Sidebar + main content |
| (.)folder | Intercept same level | Preview sibling route in a modal |
| (..)folder | Intercept parent | Open a child of the parent as an overlay |
| (..)(..)folder | Intercept two levels | Deeply nested overlay |
| (...)folder | Intercept from root | Show arbitrary route in current view |

### Metadata file conventions

#### App icons

|  |  |  |
| --- | --- | --- |
| favicon | .ico | Favicon file |
| icon | .ico.jpg.jpeg.png.svg | App Icon file |
| icon | .js.ts.tsx | Generated App Icon |
| apple-icon | .jpg.jpeg,.png | Apple App Icon file |
| apple-icon | .js.ts.tsx | Generated Apple App Icon |

#### Open Graph and Twitter images

|  |  |  |
| --- | --- | --- |
| opengraph-image | .jpg.jpeg.png.gif | Open Graph image file |
| opengraph-image | .js.ts.tsx | Generated Open Graph image |
| twitter-image | .jpg.jpeg.png.gif | Twitter image file |
| twitter-image | .js.ts.tsx | Generated Twitter image |

#### SEO

|  |  |  |
| --- | --- | --- |
| sitemap | .xml | Sitemap file |
| sitemap | .js.ts | Generated Sitemap |
| robots | .txt | Robots file |
| robots | .js.ts | Generated Robots file |

## Organizing your project

Next.js is **unopinionated** about how you organize and colocate your project files. But it does provide several features to help you organize your project.

### Component hierarchy

The components defined in special files are rendered in a specific hierarchy:

- `layout.js`
- `template.js`
- `error.js` (React error boundary)
- `loading.js` (React suspense boundary)
- `not-found.js` (React error boundary for "not found" UI)
- `page.js` or nested `layout.js`

![Component Hierarchy for File Conventions](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ffile-conventions-component-hierarchy.png&w=3840&q=75)![Component Hierarchy for File Conventions](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ffile-conventions-component-hierarchy.png&w=3840&q=75)

The components are rendered recursively in nested routes, meaning the components of a route segment will be nested **inside** the components of its parent segment.

![Nested File Conventions Component Hierarchy](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fnested-file-conventions-component-hierarchy.png&w=3840&q=75)![Nested File Conventions Component Hierarchy](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fnested-file-conventions-component-hierarchy.png&w=3840&q=75)

### Colocation

In the `app` directory, nested folders define route structure. Each folder represents a route segment that is mapped to a corresponding segment in a URL path.

However, even though route structure is defined through folders, a route is **not publicly accessible** until a `page.js` or `route.js` file is added to a route segment.

![A diagram showing how a route is not publicly accessible until a page.js or route.js file is added to a route segment.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-not-routable.png&w=3840&q=75)![A diagram showing how a route is not publicly accessible until a page.js or route.js file is added to a route segment.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-not-routable.png&w=3840&q=75)

And, even when a route is made publicly accessible, only the **content returned** by `page.js` or `route.js` is sent to the client.

![A diagram showing how page.js and route.js files make routes publicly accessible.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-routable.png&w=3840&q=75)![A diagram showing how page.js and route.js files make routes publicly accessible.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-routable.png&w=3840&q=75)

This means that **project files** can be **safely colocated** inside route segments in the `app` directory without accidentally being routable.

![A diagram showing colocated project files are not routable even when a segment contains a page.js or route.js file.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-colocation.png&w=3840&q=75)![A diagram showing colocated project files are not routable even when a segment contains a page.js or route.js file.](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-colocation.png&w=3840&q=75)

> **Good to know**: While you **can** colocate your project files in `app` you don't **have** to. If you prefer, you can [keep them outside theappdirectory](#store-project-files-outside-of-app).

### Private folders

Private folders can be created by prefixing a folder with an underscore: `_folderName`

This indicates the folder is a private implementation detail and should not be considered by the routing system, thereby **opting the folder and all its subfolders** out of routing.

![An example folder structure using private folders](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-private-folders.png&w=3840&q=75)![An example folder structure using private folders](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-private-folders.png&w=3840&q=75)

Since files in the `app` directory can be [safely colocated by default](#colocation), private folders are not required for colocation. However, they can be useful for:

- Separating UI logic from routing logic.
- Consistently organizing internal files across a project and the Next.js ecosystem.
- Sorting and grouping files in code editors.
- Avoiding potential naming conflicts with future Next.js file conventions.

> **Good to know**:
>
>
>
> - While not a framework convention, you might also consider marking files outside private folders as "private" using the same underscore pattern.
> - You can create URL segments that start with an underscore by prefixing the folder name with `%5F` (the URL-encoded form of an underscore): `%5FfolderName`.
> - If you don't use private folders, it would be helpful to know Next.js [special file conventions](https://nextjs.org/docs/app/getting-started/project-structure#routing-files) to prevent unexpected naming conflicts.

### Route groups

Route groups can be created by wrapping a folder in parenthesis: `(folderName)`

This indicates the folder is for organizational purposes and should **not be included** in the route's URL path.

![An example folder structure using route groups](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-route-groups.png&w=3840&q=75)![An example folder structure using route groups](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-route-groups.png&w=3840&q=75)

Route groups are useful for:

- Organizing routes by site section, intent, or team. e.g. marketing pages, admin pages, etc.
- Enabling nested layouts in the same route segment level:
  - [Creating multiple nested layouts in the same segment, including multiple root layouts](#creating-multiple-root-layouts)
  - [Adding a layout to a subset of routes in a common segment](#opting-specific-segments-into-a-layout)

### srcfolder

Next.js supports storing application code (including `app`) inside an optional [srcfolder](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder). This separates application code from project configuration files which mostly live in the root of a project.

![An example folder structure with the `src` folder](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-src-directory.png&w=3840&q=75)![An example folder structure with the `src` folder](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-src-directory.png&w=3840&q=75)

## Examples

The following section lists a very high-level overview of common strategies. The simplest takeaway is to choose a strategy that works for you and your team and be consistent across the project.

> **Good to know**: In our examples below, we're using `components` and `lib` folders as generalized placeholders, their naming has no special framework significance and your projects might use other folders like `ui`, `utils`, `hooks`, `styles`, etc.

### Store project files outside ofapp

This strategy stores all application code in shared folders in the **root of your project** and keeps the `app` directory purely for routing purposes.

![An example folder structure with project files outside of app](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-project-root.png&w=3840&q=75)![An example folder structure with project files outside of app](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-project-root.png&w=3840&q=75)

### Store project files in top-level folders inside ofapp

This strategy stores all application code in shared folders in the **root of theappdirectory**.

![An example folder structure with project files inside app](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-app-root.png&w=3840&q=75)![An example folder structure with project files inside app](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-app-root.png&w=3840&q=75)

### Split project files by feature or route

This strategy stores globally shared application code in the root `app` directory and **splits** more specific application code into the route segments that use them.

![An example folder structure with project files split by feature or route](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fproject-organization-app-root-split.png&w=3840&q=75)![An example folder structure with project files split by feature or route](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fproject-organization-app-root-split.png&w=3840&q=75)

### Organize routes without affecting the URL path

To organize routes without affecting the URL, create a group to keep related routes together. The folders in parenthesis will be omitted from the URL (e.g. `(marketing)` or `(shop)`).

![Organizing Routes with Route Groups](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-organisation.png&w=3840&q=75)![Organizing Routes with Route Groups](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Froute-group-organisation.png&w=3840&q=75)

Even though routes inside `(marketing)` and `(shop)` share the same URL hierarchy, you can create a different layout for each group by adding a `layout.js` file inside their folders.

![Route Groups with Multiple Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-multiple-layouts.png&w=3840&q=75)![Route Groups with Multiple Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Froute-group-multiple-layouts.png&w=3840&q=75)

### Opting specific segments into a layout

To opt specific routes into a layout, create a new route group (e.g. `(shop)`) and move the routes that share the same layout into the group (e.g. `account` and `cart`). The routes outside of the group will not share the layout (e.g. `checkout`).

![Route Groups with Opt-in Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-opt-in-layouts.png&w=3840&q=75)![Route Groups with Opt-in Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Froute-group-opt-in-layouts.png&w=3840&q=75)

### Opting for loading skeletons on a specific route

To apply a [loading skeleton](https://nextjs.org/docs/app/api-reference/file-conventions/loading) via a `loading.js` file to a specific route, create a new route group (e.g., `/(overview)`) and then move your `loading.tsx` inside that route group.

![Folder structure showing a loading.tsx and a page.tsx inside the route group](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-loading.png&w=3840&q=75)![Folder structure showing a loading.tsx and a page.tsx inside the route group](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Froute-group-loading.png&w=3840&q=75)

Now, the `loading.tsx` file will only apply to your dashboard → overview page instead of all your dashboard pages without affecting the URL path structure.

### Creating multiple root layouts

To create multiple [root layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout#root-layout), remove the top-level `layout.js` file, and add a `layout.js` file inside each route group. This is useful for partitioning an application into sections that have a completely different UI or experience. The `<html>` and `<body>` tags need to be added to each root layout.

![Route Groups with Multiple Root Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-group-multiple-root-layouts.png&w=3840&q=75)![Route Groups with Multiple Root Layouts](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Froute-group-multiple-root-layouts.png&w=3840&q=75)

In the example above, both `(marketing)` and `(shop)` have their own root layout.

Was this helpful?

supported.

---

# Proxy

> Learn how to use Proxy

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Proxy

# Proxy

Last updated  December 20, 2025

## Proxy

> **Good to know**: Starting with Next.js 16, Middleware is now called Proxy to better reflect its purpose. The functionality remains the same.

Proxy allows you to run code before a request is completed. Then, based on the incoming request, you can modify the response by rewriting, redirecting, modifying the request or response headers, or responding directly.

### Use cases

Some common scenarios where Proxy is effective include:

- Modifying headers for all pages or a subset of pages
- Rewriting to different pages based on A/B tests or experiments
- Programmatic redirects based on incoming request properties

For simple redirects, consider using the [redirects](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects) configuration in `next.config.ts` first. Proxy should be used when you need access to request data or more complex logic.

Proxy is *not* intended for slow data fetching. While Proxy can be helpful for [optimistic checks](https://nextjs.org/docs/app/guides/authentication#optimistic-checks-with-proxy-optional) such as permission-based redirects, it should not be used as a full session management or authorization solution.

Using fetch with `options.cache`, `options.next.revalidate`, or `options.next.tags`, has no effect in Proxy.

### Convention

Create a `proxy.ts` (or `.js`) file in the project root, or inside `src` if applicable, so that it is located at the same level as `pages` or `app`.

> **Note**: While only one `proxy.ts` file is supported per project, you can still organize your proxy logic into modules. Break out proxy functionalities into separate `.ts` or `.js` files and import them into your main `proxy.ts` file. This allows for cleaner management of route-specific proxy, aggregated in the `proxy.ts` for centralized control. By enforcing a single proxy file, it simplifies configuration, prevents potential conflicts, and optimizes performance by avoiding multiple proxy layers.

### Example

You can export your proxy function as either a default export or a named `proxy` export:

 proxy.tsJavaScriptTypeScript

```
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// This function can be marked `async` if using `await` inside
export function proxy(request: NextRequest) {
  return NextResponse.redirect(new URL('/home', request.url))
}

// Alternatively, you can use a default export:
// export default function proxy(request: NextRequest) { ... }

export const config = {
  matcher: '/about/:path*',
}
```

The `matcher` config allows you to filter Proxy to run on specific paths. See the [Matcher](https://nextjs.org/docs/app/api-reference/file-conventions/proxy#matcher) documentation for more details on path matching.

Read more about [usingproxy](https://nextjs.org/docs/app/guides/backend-for-frontend#proxy), or refer to the `proxy` [API reference](https://nextjs.org/docs/app/api-reference/file-conventions/proxy).

## API Reference

Learn more about Proxy[proxy.jsAPI reference for the proxy.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)[Backend for FrontendLearn how to use Next.js as a backend framework](https://nextjs.org/docs/app/guides/backend-for-frontend)

Was this helpful?

supported.

---

# Route Handlers

> Learn how to use Route Handlers

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Route Handlers

# Route Handlers

Last updated  November 18, 2025

## Route Handlers

Route Handlers allow you to create custom request handlers for a given route using the Web [Request](https://developer.mozilla.org/docs/Web/API/Request) and [Response](https://developer.mozilla.org/docs/Web/API/Response) APIs.

 ![Route.js Special File](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Froute-special-file.png&w=3840&q=75)![Route.js Special File](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Froute-special-file.png&w=3840&q=75)

> **Good to know**: Route Handlers are only available inside the `app` directory. They are the equivalent of [API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) inside the `pages` directory meaning you **do not** need to use API Routes and Route Handlers together.

### Convention

Route Handlers are defined in a [route.js|tsfile](https://nextjs.org/docs/app/api-reference/file-conventions/route) inside the `app` directory:

 app/api/route.tsJavaScriptTypeScript

```
export async function GET(request: Request) {}
```

Route Handlers can be nested anywhere inside the `app` directory, similar to `page.js` and `layout.js`. But there **cannot** be a `route.js` file at the same route segment level as `page.js`.

### Supported HTTP Methods

The following [HTTP methods](https://developer.mozilla.org/docs/Web/HTTP/Methods) are supported: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, and `OPTIONS`. If an unsupported method is called, Next.js will return a `405 Method Not Allowed` response.

### ExtendedNextRequestandNextResponseAPIs

In addition to supporting the native [Request](https://developer.mozilla.org/docs/Web/API/Request) and [Response](https://developer.mozilla.org/docs/Web/API/Response) APIs, Next.js extends them with [NextRequest](https://nextjs.org/docs/app/api-reference/functions/next-request) and [NextResponse](https://nextjs.org/docs/app/api-reference/functions/next-response) to provide convenient helpers for advanced use cases.

### Caching

Route Handlers are not cached by default. You can, however, opt into caching for `GET` methods. Other supported HTTP methods are **not** cached. To cache a `GET` method, use a [route config option](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamic) such as `export const dynamic = 'force-static'` in your Route Handler file.

 app/items/route.tsJavaScriptTypeScript

```
export const dynamic = 'force-static'

export async function GET() {
  const res = await fetch('https://data.mongodb-api.com/...', {
    headers: {
      'Content-Type': 'application/json',
      'API-Key': process.env.DATA_API_KEY,
    },
  })
  const data = await res.json()

  return Response.json({ data })
}
```

> **Good to know**: Other supported HTTP methods are **not** cached, even if they are placed alongside a `GET` method that is cached, in the same file.

#### With Cache Components

When [Cache Components](https://nextjs.org/docs/app/getting-started/cache-components) is enabled, `GET` Route Handlers follow the same model as normal UI routes in your application. They run at request time by default, can be prerendered when they don't access dynamic or runtime data, and you can use `use cache` to include dynamic data in the static response.

**Static example** - doesn't access dynamic or runtime data, so it will be prerendered at build time:

 app/api/project-info/route.ts

```
export async function GET() {
  return Response.json({
    projectName: 'Next.js',
  })
}
```

**Dynamic example** - accesses non-deterministic operations. During the build, prerendering stops when `Math.random()` is called, deferring to request-time rendering:

 app/api/random-number/route.ts

```
export async function GET() {
  return Response.json({
    randomNumber: Math.random(),
  })
}
```

**Runtime data example** - accesses request-specific data. Prerendering terminates when runtime APIs like `headers()` are called:

 app/api/user-agent/route.ts

```
import { headers } from 'next/headers'

export async function GET() {
  const headersList = await headers()
  const userAgent = headersList.get('user-agent')

  return Response.json({ userAgent })
}
```

> **Good to know**: Prerendering stops if the `GET` handler accesses network requests, database queries, async file system operations, request object properties (like `req.url`, `request.headers`, `request.cookies`, `request.body`), runtime APIs like [cookies()](https://nextjs.org/docs/app/api-reference/functions/cookies), [headers()](https://nextjs.org/docs/app/api-reference/functions/headers), [connection()](https://nextjs.org/docs/app/api-reference/functions/connection), or non-deterministic operations.

**Cached example** - accesses dynamic data (database query) but caches it with `use cache`, allowing it to be included in the prerendered response:

 app/api/products/route.ts

```
import { cacheLife } from 'next/cache'

export async function GET() {
  const products = await getProducts()
  return Response.json(products)
}

async function getProducts() {
  'use cache'
  cacheLife('hours')

  return await db.query('SELECT * FROM products')
}
```

> **Good to know**: `use cache` cannot be used directly inside a Route Handler body; extract it to a helper function. Cached responses revalidate according to `cacheLife` when a new request arrives.

### Special Route Handlers

Special Route Handlers like [sitemap.ts](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap), [opengraph-image.tsx](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image), and [icon.tsx](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons), and other [metadata files](https://nextjs.org/docs/app/api-reference/file-conventions/metadata) remain static by default unless they use Dynamic APIs or dynamic config options.

### Route Resolution

You can consider a `route` the lowest level routing primitive.

- They **do not** participate in layouts or client-side navigations like `page`.
- There **cannot** be a `route.js` file at the same route as `page.js`.

| Page | Route | Result |
| --- | --- | --- |
| app/page.js | app/route.js | Conflict |
| app/page.js | app/api/route.js | Valid |
| app/[user]/page.js | app/api/route.js | Valid |

Each `route.js` or `page.js` file takes over all HTTP verbs for that route.

 app/page.tsJavaScriptTypeScript

```
export default function Page() {
  return <h1>Hello, Next.js!</h1>
}

// Conflict
// `app/route.ts`
export async function POST(request: Request) {}
```

Read more about how Route Handlers [complement your frontend application](https://nextjs.org/docs/app/guides/backend-for-frontend), or explore the Route Handlers [API Reference](https://nextjs.org/docs/app/api-reference/file-conventions/route).

### Route Context Helper

In TypeScript, you can type the `context` parameter for Route Handlers with the globally available [RouteContext](https://nextjs.org/docs/app/api-reference/file-conventions/route#route-context-helper) helper:

 app/users/[id]/route.tsJavaScriptTypeScript

```
import type { NextRequest } from 'next/server'

export async function GET(_req: NextRequest, ctx: RouteContext<'/users/[id]'>) {
  const { id } = await ctx.params
  return Response.json({ id })
}
```

> **Good to know**
>
>
>
> - Types are generated during `next dev`, `next build` or `next typegen`.

## API Reference

Learn more about Route Handlers[route.jsAPI reference for the route.js special file.](https://nextjs.org/docs/app/api-reference/file-conventions/route)[Backend for FrontendLearn how to use Next.js as a backend framework](https://nextjs.org/docs/app/guides/backend-for-frontend)

Was this helpful?

supported.

---

# Server and Client Components

> Learn how you can use React Server and Client Components to render parts of your application on the server or the client.

[App Router](https://nextjs.org/docs/app)[Getting Started](https://nextjs.org/docs/app/getting-started)Server and Client Components

# Server and Client Components

Last updated  January 26, 2026

By default, layouts and pages are [Server Components](https://react.dev/reference/rsc/server-components), which lets you fetch data and render parts of your UI on the server, optionally cache the result, and stream it to the client. When you need interactivity or browser APIs, you can use [Client Components](https://react.dev/reference/rsc/use-client) to layer in functionality.

This page explains how Server and Client Components work in Next.js and when to use them, with examples of how to compose them together in your application.

## When to use Server and Client Components?

The client and server environments have different capabilities. Server and Client components allow you to run logic in each environment depending on your use case.

Use **Client Components** when you need:

- [State](https://react.dev/learn/managing-state) and [event handlers](https://react.dev/learn/responding-to-events). E.g. `onClick`, `onChange`.
- [Lifecycle logic](https://react.dev/learn/lifecycle-of-reactive-effects). E.g. `useEffect`.
- Browser-only APIs. E.g. `localStorage`, `window`, `Navigator.geolocation`, etc.
- [Custom hooks](https://react.dev/learn/reusing-logic-with-custom-hooks).

Use **Server Components** when you need:

- Fetch data from databases or APIs close to the source.
- Use API keys, tokens, and other secrets without exposing them to the client.
- Reduce the amount of JavaScript sent to the browser.
- Improve the [First Contentful Paint (FCP)](https://web.dev/fcp/), and stream content progressively to the client.

For example, the `<Page>` component is a Server Component that fetches data about a post, and passes it as props to the `<LikeButton>` which handles client-side interactivity.

 app/[id]/page.tsxJavaScriptTypeScript

```
import LikeButton from '@/app/ui/like-button'
import { getPost } from '@/lib/data'

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const post = await getPost(id)

  return (
    <div>
      <main>
        <h1>{post.title}</h1>
        {/* ... */}
        <LikeButton likes={post.likes} />
      </main>
    </div>
  )
}
```

   app/ui/like-button.tsxJavaScriptTypeScript

```
'use client'

import { useState } from 'react'

export default function LikeButton({ likes }: { likes: number }) {
  // ...
}
```

## How do Server and Client Components work in Next.js?

### On the server

On the server, Next.js uses React's APIs to orchestrate rendering. The rendering work is split into chunks, by individual route segments ([layouts and pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages)):

- **Server Components** are rendered into a special data format called the React Server Component Payload (RSC Payload).
- **Client Components** and the RSC Payload are used to [pre-render](https://nextjs.org/docs/app/guides/caching#rendering-strategies) HTML.

> **What is the React Server Component Payload (RSC)?**
>
>
>
> The RSC Payload is a compact binary representation of the rendered React Server Components tree. It's used by React on the client to update the browser's DOM. The RSC Payload contains:
>
>
>
> - The rendered result of Server Components
> - Placeholders for where Client Components should be rendered and references to their JavaScript files
> - Any props passed from a Server Component to a Client Component

### On the client (first load)

Then, on the client:

1. **HTML** is used to immediately show a fast non-interactive preview of the route to the user.
2. **RSC Payload** is used to reconcile the Client and Server Component trees.
3. **JavaScript** is used to hydrate Client Components and make the application interactive.

> **What is hydration?**
>
>
>
> Hydration is React's process for attaching [event handlers](https://react.dev/learn/responding-to-events) to the DOM, to make the static HTML interactive.

### Subsequent Navigations

On subsequent navigations:

- The **RSC Payload** is prefetched and cached for instant navigation.
- **Client Components** are rendered entirely on the client, without the server-rendered HTML.

## Examples

### Using Client Components

You can create a Client Component by adding the ["use client"](https://react.dev/reference/react/use-client) directive at the top of the file, above your imports.

 app/ui/counter.tsxJavaScriptTypeScript

```
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>{count} likes</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  )
}
```

`"use client"` is used to declare a **boundary** between the Server and Client module graphs (trees).

Once a file is marked with `"use client"`, **all its imports and child components are considered part of the client bundle**. This means you don't need to add the directive to every component that is intended for the client.

### Reducing JS bundle size

To reduce the size of your client JavaScript bundles, add `'use client'` to specific interactive components instead of marking large parts of your UI as Client Components.

For example, the `<Layout>` component contains mostly static elements like a logo and navigation links, but includes an interactive search bar. `<Search />` is interactive and needs to be a Client Component, however, the rest of the layout can remain a Server Component.

 app/layout.tsxJavaScriptTypeScript

```
// Client Component
import Search from './search'
// Server Component
import Logo from './logo'

// Layout is a Server Component by default
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <nav>
        <Logo />
        <Search />
      </nav>
      <main>{children}</main>
    </>
  )
}
```

   app/ui/search.tsxJavaScriptTypeScript

```
'use client'

export default function Search() {
  // ...
}
```

### Passing data from Server to Client Components

You can pass data from Server Components to Client Components using props.

 app/[id]/page.tsxJavaScriptTypeScript

```
import LikeButton from '@/app/ui/like-button'
import { getPost } from '@/lib/data'

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const post = await getPost(id)

  return <LikeButton likes={post.likes} />
}
```

   app/ui/like-button.tsxJavaScriptTypeScript

```
'use client'

export default function LikeButton({ likes }: { likes: number }) {
  // ...
}
```

Alternatively, you can stream data from a Server Component to a Client Component with the [useHook](https://react.dev/reference/react/use). See an [example](https://nextjs.org/docs/app/getting-started/fetching-data#streaming-data-with-the-use-hook).

> **Good to know**: Props passed to Client Components need to be [serializable](https://react.dev/reference/react/use-server#serializable-parameters-and-return-values) by React.

### Interleaving Server and Client Components

You can pass Server Components as a prop to a Client Component. This allows you to visually nest server-rendered UI within Client components.

A common pattern is to use `children` to create a *slot* in a `<ClientComponent>`. For example, a `<Cart>` component that fetches data on the server, inside a `<Modal>` component that uses client state to toggle visibility.

 app/ui/modal.tsxJavaScriptTypeScript

```
'use client'

export default function Modal({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

Then, in a parent Server Component (e.g.`<Page>`), you can pass a `<Cart>` as the child of the `<Modal>`:

 app/page.tsxJavaScriptTypeScript

```
import Modal from './ui/modal'
import Cart from './ui/cart'

export default function Page() {
  return (
    <Modal>
      <Cart />
    </Modal>
  )
}
```

In this pattern, all Server Components will be rendered on the server ahead of time, including those as props. The resulting RSC payload will contain references of where Client Components should be rendered within the component tree.

### Context providers

[React context](https://react.dev/learn/passing-data-deeply-with-context) is commonly used to share global state like the current theme. However, React context is not supported in Server Components.

To use context, create a Client Component that accepts `children`:

 app/theme-provider.tsxJavaScriptTypeScript

```
'use client'

import { createContext } from 'react'

export const ThemeContext = createContext({})

export default function ThemeProvider({
  children,
}: {
  children: React.ReactNode
}) {
  return <ThemeContext.Provider value="dark">{children}</ThemeContext.Provider>
}
```

Then, import it into a Server Component (e.g. `layout`):

 app/layout.tsxJavaScriptTypeScript

```
import ThemeProvider from './theme-provider'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
```

Your Server Component will now be able to directly render your provider, and all other Client Components throughout your app will be able to consume this context.

> **Good to know**: You should render providers as deep as possible in the tree – notice how `ThemeProvider` only wraps `{children}` instead of the entire `<html>` document. This makes it easier for Next.js to optimize the static parts of your Server Components.

### Sharing data with context and React.cache

You can share fetched data across both Server and Client Components by combining [React.cache](https://react.dev/reference/react/cache) with context providers.

Create a cached function that fetches data:

 app/lib/user.tsJavaScriptTypeScript

```
import { cache } from 'react'

export const getUser = cache(async () => {
  const res = await fetch('https://api.example.com/user')
  return res.json()
})
```

Create a context provider that stores the promise:

 app/user-provider.tsxJavaScriptTypeScript

```
'use client'

import { createContext } from 'react'

type User = {
  id: string
  name: string
}

export const UserContext = createContext<Promise<User> | null>(null)

export default function UserProvider({
  children,
  userPromise,
}: {
  children: React.ReactNode
  userPromise: Promise<User>
}) {
  return <UserContext value={userPromise}>{children}</UserContext>
}
```

In a layout, pass the promise to the provider without awaiting:

 app/layout.tsxJavaScriptTypeScript

```
import UserProvider from './user-provider'
import { getUser } from './lib/user'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const userPromise = getUser() // Don't await

  return (
    <html>
      <body>
        <UserProvider userPromise={userPromise}>{children}</UserProvider>
      </body>
    </html>
  )
}
```

Client Components use [use()](https://react.dev/reference/react/use) to resolve the promise from context, wrapped in `<Suspense>` for fallback UI:

 app/ui/profile.tsxJavaScriptTypeScript

```
'use client'

import { use, useContext } from 'react'
import { UserContext } from '../user-provider'

export function Profile() {
  const userPromise = useContext(UserContext)
  if (!userPromise) {
    throw new Error('useContext must be used within a UserProvider')
  }
  const user = use(userPromise)
  return <p>Welcome, {user.name}</p>
}
```

   app/page.tsxJavaScriptTypeScript

```
import { Suspense } from 'react'
import { Profile } from './ui/profile'

export default function Page() {
  return (
    <Suspense fallback={<div>Loading profile...</div>}>
      <Profile />
    </Suspense>
  )
}
```

Server Components can also call `getUser()` directly:

 app/dashboard/page.tsxJavaScriptTypeScript

```
import { getUser } from '../lib/user'

export default async function DashboardPage() {
  const user = await getUser() // Cached - same request, no duplicate fetch
  return <h1>Dashboard for {user.name}</h1>
}
```

Since `getUser` is wrapped with `React.cache`, multiple calls within the same request return the same memoized result, whether called directly in Server Components or resolved via context in Client Components.

> **Good to know**: `React.cache` is scoped to the current request only. Each request gets its own memoization scope with no sharing between requests.

### Third-party components

When using a third-party component that relies on client-only features, you can wrap it in a Client Component to ensure it works as expected.

For example, the `<Carousel />` can be imported from the `acme-carousel` package. This component uses `useState`, but it doesn't yet have the `"use client"` directive.

If you use `<Carousel />` within a Client Component, it will work as expected:

 app/gallery.tsxJavaScriptTypeScript

```
'use client'

import { useState } from 'react'
import { Carousel } from 'acme-carousel'

export default function Gallery() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setIsOpen(true)}>View pictures</button>
      {/* Works, since Carousel is used within a Client Component */}
      {isOpen && <Carousel />}
    </div>
  )
}
```

However, if you try to use it directly within a Server Component, you'll see an error. This is because Next.js doesn't know `<Carousel />` is using client-only features.

To fix this, you can wrap third-party components that rely on client-only features in your own Client Components:

 app/carousel.tsxJavaScriptTypeScript

```
'use client'

import { Carousel } from 'acme-carousel'

export default Carousel
```

Now, you can use `<Carousel />` directly within a Server Component:

 app/page.tsxJavaScriptTypeScript

```
import Carousel from './carousel'

export default function Page() {
  return (
    <div>
      <p>View pictures</p>
      {/*  Works, since Carousel is a Client Component */}
      <Carousel />
    </div>
  )
}
```

> **Advice for Library Authors**
>
>
>
> If you’re building a component library, add the `"use client"` directive to entry points that rely on client-only features. This lets your users import components into Server Components without needing to create wrappers.
>
>
>
> It's worth noting some bundlers might strip out `"use client"` directives. You can find an example of how to configure esbuild to include the `"use client"` directive in the [React Wrap Balancer](https://github.com/shuding/react-wrap-balancer/blob/main/tsup.config.ts#L10-L13) and [Vercel Analytics](https://github.com/vercel/analytics/blob/main/packages/web/tsup.config.js#L26-L30) repositories.

### Preventing environment poisoning

JavaScript modules can be shared between both Server and Client Components modules. This means it's possible to accidentally import server-only code into the client. For example, consider the following function:

 lib/data.tsJavaScriptTypeScript

```
export async function getData() {
  const res = await fetch('https://external-service.com/data', {
    headers: {
      authorization: process.env.API_KEY,
    },
  })

  return res.json()
}
```

This function contains an `API_KEY` that should never be exposed to the client.

In Next.js, only environment variables prefixed with `NEXT_PUBLIC_` are included in the client bundle. If variables are not prefixed, Next.js replaces them with an empty string.

As a result, even though `getData()` can be imported and executed on the client, it won't work as expected.

To prevent accidental usage in Client Components, you can use the [server-onlypackage](https://www.npmjs.com/package/server-only).

Then, import the package into a file that contains server-only code:

 lib/data.js

```
import 'server-only'

export async function getData() {
  const res = await fetch('https://external-service.com/data', {
    headers: {
      authorization: process.env.API_KEY,
    },
  })

  return res.json()
}
```

Now, if you try to import the module into a Client Component, there will be a build-time error.

The corresponding [client-onlypackage](https://www.npmjs.com/package/client-only) can be used to mark modules that contain client-only logic like code that accesses the `window` object.

In Next.js, installing `server-only` or `client-only` is **optional**. However, if your linting rules flag extraneous dependencies, you may install them to avoid issues.

     Terminal

```
pnpm add server-only
```

Next.js handles `server-only` and `client-only` imports internally to provide clearer error messages when a module is used in the wrong environment. The contents of these packages from NPM are not used by Next.js.

Next.js also provides its own type declarations for `server-only` and `client-only`, for TypeScript configurations where [noUncheckedSideEffectImports](https://www.typescriptlang.org/tsconfig/#noUncheckedSideEffectImports) is active.

## Next Steps

Learn more about the APIs mentioned in this page.[use clientLearn how to use the use client directive to render a component on the client.](https://nextjs.org/docs/app/api-reference/directives/use-client)

Was this helpful?

supported.
