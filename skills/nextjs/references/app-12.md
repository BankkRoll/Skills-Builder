# loading.js and more

# loading.js

> API reference for the loading.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)loading.js

# loading.js

Last updated  October 27, 2025

The special file `loading.js` helps you create meaningful Loading UI with [React Suspense](https://react.dev/reference/react/Suspense). With this convention, you can show an [instant loading state](#instant-loading-states) from the server while the content of a route segment streams in. The new content is automatically swapped in once complete.

 ![Loading UI](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Floading-ui.png&w=3840&q=75)![Loading UI](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Floading-ui.png&w=3840&q=75) app/feed/loading.tsxJavaScriptTypeScript

```
export default function Loading() {
  // Or a custom loading skeleton component
  return <p>Loading...</p>
}
```

Inside the `loading.js` file, you can add any light-weight loading UI. You may find it helpful to use the [React Developer Tools](https://react.dev/learn/react-developer-tools) to manually toggle Suspense boundaries.

By default, this file is a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) - but can also be used as a Client Component through the `"use client"` directive.

## Reference

### Parameters

Loading UI components do not accept any parameters.

## Behavior

### Navigation

- The Fallback UI is [prefetched](https://nextjs.org/docs/app/getting-started/linking-and-navigating#prefetching), making navigation immediate unless prefetching hasn't completed.
- Navigation is interruptible, meaning changing routes does not need to wait for the content of the route to fully load before navigating to another route.
- Shared layouts remain interactive while new route segments load.

### Instant Loading States

An instant loading state is fallback UI that is shown immediately upon navigation. You can pre-render loading indicators such as skeletons and spinners, or a small but meaningful part of future screens such as a cover photo, title, etc. This helps users understand the app is responding and provides a better user experience.

Create a loading state by adding a `loading.js` file inside a folder.

 ![loading.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Floading-special-file.png&w=3840&q=75)![loading.js special file](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Floading-special-file.png&w=3840&q=75) app/dashboard/loading.tsxJavaScriptTypeScript

```
export default function Loading() {
  // You can add any UI inside Loading, including a Skeleton.
  return <LoadingSkeleton />
}
```

In the same folder, `loading.js` will be nested inside `layout.js`. It will automatically wrap the `page.js` file and any children below in a `<Suspense>` boundary.

 ![loading.js overview](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Floading-overview.png&w=3840&q=75)![loading.js overview](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Floading-overview.png&w=3840&q=75)

### SEO

- For bots that only scrape static HTML, and cannot execute JavaScript like a full browser, such as Twitterbot, Next.js resolves [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) before streaming UI, and metadata is placed in the `<head>` of the initial HTML.
- Otherwise, [streaming metadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata#streaming-metadata) may be used. Next.js automatically detects user agents to choose between blocking and streaming behavior.
- Since streaming is server-rendered, it does not impact SEO. You can use the [Rich Results Test](https://search.google.com/test/rich-results) tool from Google to see how your page appears to Google's web crawlers and view the serialized HTML ([source](https://web.dev/rendering-on-the-web/#seo-considerations)).

### Status Codes

When streaming, a `200` status code will be returned to signal that the request was successful.

The server can still communicate errors or issues to the client within the streamed content itself, for example, when using [redirect](https://nextjs.org/docs/app/api-reference/functions/redirect) or [notFound](https://nextjs.org/docs/app/api-reference/functions/not-found). Because the response headers have already been sent to the client, the status code of the response cannot be updated.

For example, when a 404 page is streamed to the client, Next.js includes a `<meta name="robots" content="noindex">` tag in the streamed HTML. This prevents search engines from indexing that URL even if the HTTP status is 200. See Google’s guidance on the [robotsmeta tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag).

Some crawlers may label these responses as “soft 404s”. In the streaming case, this does not lead to indexation because the page is explicitly marked `noindex` in the HTML.

If you need a 404 status, for compliance or analytics, ensure the resource exists before the response body is streamed, so that the server can set the HTTP status code.

You can run this check in [proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) to rewrite missing slugs to a not-found route, or [produce a 404 response](https://nextjs.org/docs/app/api-reference/file-conventions/proxy#producing-a-response). Keep proxy checks fast, and avoid fetching full content there.

 When is the response body streamed?

The response body starts streaming when a Suspense fallback renders (for example, a `loading.tsx`) or when a Server Component suspends under a `Suspense` boundary. Place `notFound()` before those boundaries and before any `await` that may suspend.

To start streaming, the response headers must be set. This is why it is not possible to change the status code after streaming started.

### Browser limits

[Some browsers](https://bugs.webkit.org/show_bug.cgi?id=252413) buffer a streaming response. You may not see the streamed response until the response exceeds 1024 bytes. This typically only affects “hello world” applications, but not real applications.

## Platform Support

| Deployment Option | Supported |
| --- | --- |
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

Learn how to [configure streaming](https://nextjs.org/docs/app/guides/self-hosting#streaming-and-suspense) when self-hosting Next.js.

## Examples

### Streaming with Suspense

In addition to `loading.js`, you can also manually create Suspense Boundaries for your own UI components. The App Router supports streaming with [Suspense](https://react.dev/reference/react/Suspense).

`<Suspense>` works by wrapping a component that performs an asynchronous action (e.g. fetch data), showing fallback UI (e.g. skeleton, spinner) while it's happening, and then swapping in your component once the action completes.

 app/dashboard/page.tsxJavaScriptTypeScript

```
import { Suspense } from 'react'
import { PostFeed, Weather } from './Components'

export default function Posts() {
  return (
    <section>
      <Suspense fallback={<p>Loading feed...</p>}>
        <PostFeed />
      </Suspense>
      <Suspense fallback={<p>Loading weather...</p>}>
        <Weather />
      </Suspense>
    </section>
  )
}
```

By using Suspense, you get the benefits of:

1. **Streaming Server Rendering** - Progressively rendering HTML from the server to the client.
2. **Selective Hydration** - React prioritizes what components to make interactive first based on user interaction.

For more Suspense examples and use cases, please see the [React Documentation](https://react.dev/reference/react/Suspense).

## Version History

| Version | Changes |
| --- | --- |
| v13.0.0 | loadingintroduced. |

Was this helpful?

supported.

---

# mdx

> API reference for the mdx-components.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)mdx-components.js

# mdx-components.js

Last updated  July 29, 2025

The `mdx-components.js|tsx` file is **required** to use [@next/mdxwith App Router](https://nextjs.org/docs/app/guides/mdx) and will not work without it. Additionally, you can use it to [customize styles](https://nextjs.org/docs/app/guides/mdx#using-custom-styles-and-components).

Use the file `mdx-components.tsx` (or `.js`) in the root of your project to define MDX Components. For example, at the same level as `pages` or `app`, or inside `src` if applicable.

 mdx-components.tsxJavaScriptTypeScript

```
import type { MDXComponents } from 'mdx/types'

const components: MDXComponents = {}

export function useMDXComponents(): MDXComponents {
  return components
}
```

## Exports

### useMDXComponentsfunction

The file must export a single function named `useMDXComponents`. This function does not accept any arguments.

 mdx-components.tsxJavaScriptTypeScript

```
import type { MDXComponents } from 'mdx/types'

const components: MDXComponents = {}

export function useMDXComponents(): MDXComponents {
  return components
}
```

## Version History

| Version | Changes |
| --- | --- |
| v13.1.2 | MDX Components added |

## Learn more about MDX Components

[MDXLearn how to configure MDX and use it in your Next.js apps.](https://nextjs.org/docs/app/guides/mdx)

Was this helpful?

supported.

---

# favicon, icon, and apple

> API Reference for the Favicon, Icon and Apple Icon file conventions.

[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)[Metadata Files](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)favicon, icon, and apple-icon

# favicon, icon, and apple-icon

Last updated  October 22, 2025

The `favicon`, `icon`, or `apple-icon` file conventions allow you to set icons for your application.

They are useful for adding app icons that appear in places like web browser tabs, phone home screens, and search engine results.

There are two ways to set app icons:

- [Using image files (.ico, .jpg, .png)](#image-files-ico-jpg-png)
- [Using code to generate an icon (.js, .ts, .tsx)](#generate-icons-using-code-js-ts-tsx)

## Image files (.ico, .jpg, .png)

Use an image file to set an app icon by placing a `favicon`, `icon`, or `apple-icon` image file within your `/app` directory.
The `favicon` image can only be located in the top level of `app/`.

Next.js will evaluate the file and automatically add the appropriate tags to your app's `<head>` element.

| File convention | Supported file types | Valid locations |
| --- | --- | --- |
| favicon | .ico | app/ |
| icon | .ico,.jpg,.jpeg,.png,.svg | app/**/* |
| apple-icon | .jpg,.jpeg,.png | app/**/* |

### favicon

Add a `favicon.ico` image file to the root `/app` route segment.

 <head> output

```
<link rel="icon" href="/favicon.ico" sizes="any" />
```

### icon

Add an `icon.(ico|jpg|jpeg|png|svg)` image file.

 <head> output

```
<link
  rel="icon"
  href="/icon?<generated>"
  type="image/<generated>"
  sizes="<generated>"
/>
```

### apple-icon

Add an `apple-icon.(jpg|jpeg|png)` image file.

 <head> output

```
<link
  rel="apple-touch-icon"
  href="/apple-icon?<generated>"
  type="image/<generated>"
  sizes="<generated>"
/>
```

> **Good to know**:
>
>
>
> - You can set multiple icons by adding a number suffix to the file name. For example, `icon1.png`, `icon2.png`, etc. Numbered files will sort lexically.
> - Favicons can only be set in the root `/app` segment. If you need more granularity, you can use [icon](#icon).
> - The appropriate `<link>` tags and attributes such as `rel`, `href`, `type`, and `sizes` are determined by the icon type and metadata of the evaluated file.
> - For example, a 32 by 32px `.png` file will have `type="image/png"` and `sizes="32x32"` attributes.
> - `sizes="any"` is added to icons when the extension is `.svg` or the image size of the file is not determined. More details in this [favicon handbook](https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs).

## Generate icons using code (.js, .ts, .tsx)

In addition to using [literal image files](#image-files-ico-jpg-png), you can programmatically **generate** icons using code.

Generate an app icon by creating an `icon` or `apple-icon` route that default exports a function.

| File convention | Supported file types |
| --- | --- |
| icon | .js,.ts,.tsx |
| apple-icon | .js,.ts,.tsx |

The easiest way to generate an icon is to use the [ImageResponse](https://nextjs.org/docs/app/api-reference/functions/image-response) API from `next/og`.

 app/icon.tsxJavaScriptTypeScript

```
import { ImageResponse } from 'next/og'

// Image metadata
export const size = {
  width: 32,
  height: 32,
}
export const contentType = 'image/png'

// Image generation
export default function Icon() {
  return new ImageResponse(
    (
      // ImageResponse JSX element
      <div
        style={{
          fontSize: 24,
          background: 'black',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
        }}
      >
        A
      </div>
    ),
    // ImageResponse options
    {
      // For convenience, we can re-use the exported icons size metadata
      // config to also set the ImageResponse's width and height.
      ...size,
    }
  )
}
```

   <head> output

```
<link rel="icon" href="/icon?<generated>" type="image/png" sizes="32x32" />
```

> **Good to know**:
>
>
>
> - By default, generated icons are [statically optimized](https://nextjs.org/docs/app/guides/caching#static-rendering) (generated at build time and cached) unless they use [Dynamic APIs](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) or uncached data.
> - You can generate multiple icons in the same file using [generateImageMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-image-metadata).
> - You cannot generate a `favicon` icon. Use [icon](#icon) or a [favicon.ico](#favicon) file instead.
> - App icons are special Route Handlers that are cached by default unless they use a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-apis) or [dynamic config](https://nextjs.org/docs/app/guides/caching#segment-config-options) option.

### Props

The default export function receives the following props:

#### params(optional)

A promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) object from the root segment down to the segment `icon` or `apple-icon` is colocated in.

> **Good to know**: If you use [generateImageMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-image-metadata), the function will also receive an `id` prop that is a promise resolving to the `id` value from one of the items returned by `generateImageMetadata`.

 app/shop/[slug]/icon.tsxJavaScriptTypeScript

```
export default async function Icon({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // ...
}
```

| Route | URL | params |
| --- | --- | --- |
| app/shop/icon.js | /shop | undefined |
| app/shop/[slug]/icon.js | /shop/1 | Promise<{ slug: '1' }> |
| app/shop/[tag]/[item]/icon.js | /shop/1/2 | Promise<{ tag: '1', item: '2' }> |

### Returns

The default export function should return a `Blob` | `ArrayBuffer` | `TypedArray` | `DataView` | `ReadableStream` | `Response`.

> **Good to know**: `ImageResponse` satisfies this return type.

### Config exports

You can optionally configure the icon's metadata by exporting `size` and `contentType` variables from the `icon` or `apple-icon` route.

| Option | Type |
| --- | --- |
| size | { width: number; height: number } |
| contentType | string-image MIME type |

#### size

 icon.tsx | apple-icon.tsxJavaScriptTypeScript

```
export const size = { width: 32, height: 32 }

export default function Icon() {}
```

   <head> output

```
<link rel="icon" sizes="32x32" />
```

#### contentType

 icon.tsx | apple-icon.tsxJavaScriptTypeScript

```
export const contentType = 'image/png'

export default function Icon() {}
```

   <head> output

```
<link rel="icon" type="image/png" />
```

#### Route Segment Config

`icon` and `apple-icon` are specialized [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) that can use the same [route segment configuration](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config) options as Pages and Layouts.

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | paramsis now a promise that resolves to an object |
| v13.3.0 | faviconiconandapple-iconintroduced |

Was this helpful?

supported.

---

# manifest.json

> API Reference for manifest.json file.

[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)[Metadata Files](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)manifest.json

# manifest.json

Last updated  September 3, 2025

Add or generate a `manifest.(json|webmanifest)` file that matches the [Web Manifest Specification](https://developer.mozilla.org/docs/Web/Manifest) in the **root** of `app` directory to provide information about your web application for the browser.

## Static Manifest file

 app/manifest.json | app/manifest.webmanifest

```
{
  "name": "My Next.js Application",
  "short_name": "Next.js App",
  "description": "An application built with Next.js",
  "start_url": "/"
  // ...
}
```

## Generate a Manifest file

Add a `manifest.js` or `manifest.ts` file that returns a [Manifestobject](#manifest-object).

> Good to know: `manifest.js` is special Route Handlers that is cached by default unless it uses a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-apis) or [dynamic config](https://nextjs.org/docs/app/guides/caching#segment-config-options) option.

 app/manifest.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Next.js App',
    short_name: 'Next.js App',
    description: 'Next.js App',
    start_url: '/',
    display: 'standalone',
    background_color: '#fff',
    theme_color: '#fff',
    icons: [
      {
        src: '/favicon.ico',
        sizes: 'any',
        type: 'image/x-icon',
      },
    ],
  }
}
```

### Manifest Object

The manifest object contains an extensive list of options that may be updated due to new web standards. For information on all the current options, refer to the `MetadataRoute.Manifest` type in your code editor if using [TypeScript](https://nextjs.org/docs/app/api-reference/config/typescript#ide-plugin) or see the [MDN](https://developer.mozilla.org/docs/Web/Manifest) docs.

Was this helpful?

supported.

---

# opengraph

> API Reference for the Open Graph Image and Twitter Image file conventions.

[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)[Metadata Files](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)opengraph-image and twitter-image

# opengraph-image and twitter-image

Last updated  October 22, 2025

The `opengraph-image` and `twitter-image` file conventions allow you to set Open Graph and Twitter images for a route segment.

They are useful for setting the images that appear on social networks and messaging apps when a user shares a link to your site.

There are two ways to set Open Graph and Twitter images:

- [Using image files (.jpg, .png, .gif)](#image-files-jpg-png-gif)
- [Using code to generate images (.js, .ts, .tsx)](#generate-images-using-code-js-ts-tsx)

## Image files (.jpg, .png, .gif)

Use an image file to set a route segment's shared image by placing an `opengraph-image` or `twitter-image` image file in the segment.

Next.js will evaluate the file and automatically add the appropriate tags to your app's `<head>` element.

| File convention | Supported file types |
| --- | --- |
| opengraph-image | .jpg,.jpeg,.png,.gif |
| twitter-image | .jpg,.jpeg,.png,.gif |
| opengraph-image.alt | .txt |
| twitter-image.alt | .txt |

> **Good to know**:
>
>
>
> The `twitter-image` file size must not exceed [5MB](https://developer.x.com/en/docs/x-for-websites/cards/overview/summary), and the `opengraph-image` file size must not exceed [8MB](https://developers.facebook.com/docs/sharing/webmasters/images). If the image file size exceeds these limits, the build will fail.

### opengraph-image

Add an `opengraph-image.(jpg|jpeg|png|gif)` image file to any route segment.

 <head> output

```
<meta property="og:image" content="<generated>" />
<meta property="og:image:type" content="<generated>" />
<meta property="og:image:width" content="<generated>" />
<meta property="og:image:height" content="<generated>" />
```

### twitter-image

Add a `twitter-image.(jpg|jpeg|png|gif)` image file to any route segment.

 <head> output

```
<meta name="twitter:image" content="<generated>" />
<meta name="twitter:image:type" content="<generated>" />
<meta name="twitter:image:width" content="<generated>" />
<meta name="twitter:image:height" content="<generated>" />
```

### opengraph-image.alt.txt

Add an accompanying `opengraph-image.alt.txt` file in the same route segment as the `opengraph-image.(jpg|jpeg|png|gif)` image it's alt text.

 opengraph-image.alt.txt

```
About Acme
```

 <head> output

```
<meta property="og:image:alt" content="About Acme" />
```

### twitter-image.alt.txt

Add an accompanying `twitter-image.alt.txt` file in the same route segment as the `twitter-image.(jpg|jpeg|png|gif)` image it's alt text.

 twitter-image.alt.txt

```
About Acme
```

 <head> output

```
<meta property="twitter:image:alt" content="About Acme" />
```

## Generate images using code (.js, .ts, .tsx)

In addition to using [literal image files](#image-files-jpg-png-gif), you can programmatically **generate** images using code.

Generate a route segment's shared image by creating an `opengraph-image` or `twitter-image` route that default exports a function.

| File convention | Supported file types |
| --- | --- |
| opengraph-image | .js,.ts,.tsx |
| twitter-image | .js,.ts,.tsx |

> **Good to know**:
>
>
>
> - By default, generated images are [statically optimized](https://nextjs.org/docs/app/guides/caching#static-rendering) (generated at build time and cached) unless they use [Dynamic APIs](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) or uncached data.
> - You can generate multiple Images in the same file using [generateImageMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-image-metadata).
> - `opengraph-image.js` and `twitter-image.js` are special Route Handlers that is cached by default unless it uses a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-apis) or [dynamic config](https://nextjs.org/docs/app/guides/caching#segment-config-options) option.

The easiest way to generate an image is to use the [ImageResponse](https://nextjs.org/docs/app/api-reference/functions/image-response) API from `next/og`.

 app/about/opengraph-image.tsxJavaScriptTypeScript

```
import { ImageResponse } from 'next/og'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'

// Image metadata
export const alt = 'About Acme'
export const size = {
  width: 1200,
  height: 630,
}

export const contentType = 'image/png'

// Image generation
export default async function Image() {
  // Font loading, process.cwd() is Next.js project directory
  const interSemiBold = await readFile(
    join(process.cwd(), 'assets/Inter-SemiBold.ttf')
  )

  return new ImageResponse(
    (
      // ImageResponse JSX element
      <div
        style={{
          fontSize: 128,
          background: 'white',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        About Acme
      </div>
    ),
    // ImageResponse options
    {
      // For convenience, we can re-use the exported opengraph-image
      // size config to also set the ImageResponse's width and height.
      ...size,
      fonts: [
        {
          name: 'Inter',
          data: interSemiBold,
          style: 'normal',
          weight: 400,
        },
      ],
    }
  )
}
```

   <head> output

```
<meta property="og:image" content="<generated>" />
<meta property="og:image:alt" content="About Acme" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
```

### Props

The default export function receives the following props:

#### params(optional)

A promise that resolves to an object containing the [dynamic route parameters](https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes) object from the root segment down to the segment `opengraph-image` or `twitter-image` is colocated in.

> **Good to know**: If you use [generateImageMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-image-metadata), the function will also receive an `id` prop that is a promise resolving to the `id` value from one of the items returned by `generateImageMetadata`.

 app/shop/[slug]/opengraph-image.tsxJavaScriptTypeScript

```
export default async function Image({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // ...
}
```

| Route | URL | params |
| --- | --- | --- |
| app/shop/opengraph-image.js | /shop | undefined |
| app/shop/[slug]/opengraph-image.js | /shop/1 | Promise<{ slug: '1' }> |
| app/shop/[tag]/[item]/opengraph-image.js | /shop/1/2 | Promise<{ tag: '1', item: '2' }> |

### Returns

The default export function should return a `Blob` | `ArrayBuffer` | `TypedArray` | `DataView` | `ReadableStream` | `Response`.

> **Good to know**: `ImageResponse` satisfies this return type.

### Config exports

You can optionally configure the image's metadata by exporting `alt`, `size`, and `contentType` variables from `opengraph-image` or `twitter-image` route.

| Option | Type |
| --- | --- |
| alt | string |
| size | { width: number; height: number } |
| contentType | string-image MIME type |

#### alt

 opengraph-image.tsx | twitter-image.tsxJavaScriptTypeScript

```
export const alt = 'My images alt text'

export default function Image() {}
```

   <head> output

```
<meta property="og:image:alt" content="My images alt text" />
```

#### size

 opengraph-image.tsx | twitter-image.tsxJavaScriptTypeScript

```
export const size = { width: 1200, height: 630 }

export default function Image() {}
```

   <head> output

```
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
```

#### contentType

 opengraph-image.tsx | twitter-image.tsxJavaScriptTypeScript

```
export const contentType = 'image/png'

export default function Image() {}
```

   <head> output

```
<meta property="og:image:type" content="image/png" />
```

#### Route Segment Config

`opengraph-image` and `twitter-image` are specialized [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route) that can use the same [route segment configuration](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config) options as Pages and Layouts.

### Examples

#### Using external data

This example uses the `params` object and external data to generate the image.

> **Good to know**:
> By default, this generated image will be [statically optimized](https://nextjs.org/docs/app/guides/caching#static-rendering). You can configure the individual `fetch` [options](https://nextjs.org/docs/app/api-reference/functions/fetch) or route segments [options](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#revalidate) to change this behavior.

 app/posts/[slug]/opengraph-image.tsxJavaScriptTypeScript

```
import { ImageResponse } from 'next/og'

export const alt = 'About Acme'
export const size = {
  width: 1200,
  height: 630,
}
export const contentType = 'image/png'

export default async function Image({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await fetch(`https://.../posts/${slug}`).then((res) =>
    res.json()
  )

  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 48,
          background: 'white',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {post.title}
      </div>
    ),
    {
      ...size,
    }
  )
}
```

#### Using Node.js runtime with local assets

These examples use the Node.js runtime to fetch a local image from the file system and pass it to the `<img>` `src` attribute, either as a base64 string or an `ArrayBuffer`. Place the local asset relative to the project root, not the example source file.

 app/opengraph-image.tsxJavaScriptTypeScript

```
import { ImageResponse } from 'next/og'
import { join } from 'node:path'
import { readFile } from 'node:fs/promises'

export default async function Image() {
  const logoData = await readFile(join(process.cwd(), 'logo.png'), 'base64')
  const logoSrc = `data:image/png;base64,${logoData}`

  return new ImageResponse(
    (
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <img src={logoSrc} height="100" />
      </div>
    )
  )
}
```

Passing an `ArrayBuffer` to the `src` attribute of an `<img>` element is not part of the HTML spec. The rendering engine used by `next/og` supports it, but because TypeScript definitions follow the spec, you need a `@ts-expect-error` directive or similar to use this [feature](https://github.com/vercel/satori/issues/606#issuecomment-2144000453).

 app/opengraph-image.tsxJavaScriptTypeScript

```
import { ImageResponse } from 'next/og'
import { join } from 'node:path'
import { readFile } from 'node:fs/promises'

export default async function Image() {
  const logoData = await readFile(join(process.cwd(), 'logo.png'))
  const logoSrc = Uint8Array.from(logoData).buffer

  return new ImageResponse(
    (
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {/* @ts-expect-error Satori accepts ArrayBuffer/typed arrays for <img src> at runtime */}
        <img src={logoSrc} height="100" />
      </div>
    )
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | paramsis now a promise that resolves to an object |
| v13.3.0 | opengraph-imageandtwitter-imageintroduced. |

Was this helpful?

supported.

---

# robots.txt

> API Reference for robots.txt file.

[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)[Metadata Files](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)robots.txt

# robots.txt

Last updated  June 16, 2025

Add or generate a `robots.txt` file that matches the [Robots Exclusion Standard](https://en.wikipedia.org/wiki/Robots.txt#Standard) in the **root** of `app` directory to tell search engine crawlers which URLs they can access on your site.

## Staticrobots.txt

 app/robots.txt

```
User-Agent: *
Allow: /
Disallow: /private/

Sitemap: https://acme.com/sitemap.xml
```

## Generate a Robots file

Add a `robots.js` or `robots.ts` file that returns a [Robotsobject](#robots-object).

> **Good to know**: `robots.js` is a special Route Handlers that is cached by default unless it uses a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-apis) or [dynamic config](https://nextjs.org/docs/app/guides/caching#segment-config-options) option.

 app/robots.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: '/private/',
    },
    sitemap: 'https://acme.com/sitemap.xml',
  }
}
```

Output:

```
User-Agent: *
Allow: /
Disallow: /private/

Sitemap: https://acme.com/sitemap.xml
```

### Customizing specific user agents

You can customise how individual search engine bots crawl your site by passing an array of user agents to the `rules` property. For example:

 app/robots.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: 'Googlebot',
        allow: ['/'],
        disallow: '/private/',
      },
      {
        userAgent: ['Applebot', 'Bingbot'],
        disallow: ['/'],
      },
    ],
    sitemap: 'https://acme.com/sitemap.xml',
  }
}
```

Output:

```
User-Agent: Googlebot
Allow: /
Disallow: /private/

User-Agent: Applebot
Disallow: /

User-Agent: Bingbot
Disallow: /

Sitemap: https://acme.com/sitemap.xml
```

### Robots object

```
type Robots = {
  rules:
    | {
        userAgent?: string | string[]
        allow?: string | string[]
        disallow?: string | string[]
        crawlDelay?: number
      }
    | Array<{
        userAgent: string | string[]
        allow?: string | string[]
        disallow?: string | string[]
        crawlDelay?: number
      }>
  sitemap?: string | string[]
  host?: string
}
```

## Version History

| Version | Changes |
| --- | --- |
| v13.3.0 | robotsintroduced. |

Was this helpful?

supported.

---

# sitemap.xml

> API Reference for the sitemap.xml file.

[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)[Metadata Files](https://nextjs.org/docs/app/api-reference/file-conventions/metadata)sitemap.xml

# sitemap.xml

Last updated  December 9, 2025

`sitemap.(xml|js|ts)` is a special file that matches the [Sitemaps XML format](https://www.sitemaps.org/protocol.html) to help search engine crawlers index your site more efficiently.

### Sitemap files (.xml)

For smaller applications, you can create a `sitemap.xml` file and place it in the root of your `app` directory.

 app/sitemap.xml

```
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://acme.com</loc>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
    <changefreq>yearly</changefreq>
    <priority>1</priority>
  </url>
  <url>
    <loc>https://acme.com/about</loc>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://acme.com/blog</loc>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Generating a sitemap using code (.js, .ts)

You can use the `sitemap.(js|ts)` file convention to programmatically **generate** a sitemap by exporting a default function that returns an array of URLs. If using TypeScript, a [Sitemap](#returns) type is available.

> **Good to know**: `sitemap.js` is a special Route Handler that is cached by default unless it uses a [Dynamic API](https://nextjs.org/docs/app/guides/caching#dynamic-apis) or [dynamic config](https://nextjs.org/docs/app/guides/caching#segment-config-options) option.

 app/sitemap.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://acme.com',
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 1,
    },
    {
      url: 'https://acme.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: 'https://acme.com/blog',
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.5,
    },
  ]
}
```

Output:

 acme.com/sitemap.xml

```
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://acme.com</loc>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
    <changefreq>yearly</changefreq>
    <priority>1</priority>
  </url>
  <url>
    <loc>https://acme.com/about</loc>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://acme.com/blog</loc>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Image Sitemaps

You can use `images` property to create image sitemaps. Learn more details in the [Google Developer Docs](https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps).

 app/sitemap.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://example.com',
      lastModified: '2021-01-01',
      changeFrequency: 'weekly',
      priority: 0.5,
      images: ['https://example.com/image.jpg'],
    },
  ]
}
```

Output:

 acme.com/sitemap.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
>
  <url>
    <loc>https://example.com</loc>
    <image:image>
      <image:loc>https://example.com/image.jpg</image:loc>
    </image:image>
    <lastmod>2021-01-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Video Sitemaps

You can use `videos` property to create video sitemaps. Learn more details in the [Google Developer Docs](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps).

 app/sitemap.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://example.com',
      lastModified: '2021-01-01',
      changeFrequency: 'weekly',
      priority: 0.5,
      videos: [
        {
          title: 'example',
          thumbnail_loc: 'https://example.com/image.jpg',
          description: 'this is the description',
        },
      ],
    },
  ]
}
```

Output:

 acme.com/sitemap.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"
>
  <url>
    <loc>https://example.com</loc>
    <video:video>
      <video:title>example</video:title>
      <video:thumbnail_loc>https://example.com/image.jpg</video:thumbnail_loc>
      <video:description>this is the description</video:description>
    </video:video>
    <lastmod>2021-01-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Generate a localized Sitemap

 app/sitemap.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://acme.com',
      lastModified: new Date(),
      alternates: {
        languages: {
          es: 'https://acme.com/es',
          de: 'https://acme.com/de',
        },
      },
    },
    {
      url: 'https://acme.com/about',
      lastModified: new Date(),
      alternates: {
        languages: {
          es: 'https://acme.com/es/about',
          de: 'https://acme.com/de/about',
        },
      },
    },
    {
      url: 'https://acme.com/blog',
      lastModified: new Date(),
      alternates: {
        languages: {
          es: 'https://acme.com/es/blog',
          de: 'https://acme.com/de/blog',
        },
      },
    },
  ]
}
```

Output:

 acme.com/sitemap.xml

```
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://acme.com</loc>
    <xhtml:link
      rel="alternate"
      hreflang="es"
      href="https://acme.com/es"/>
    <xhtml:link
      rel="alternate"
      hreflang="de"
      href="https://acme.com/de"/>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
  </url>
  <url>
    <loc>https://acme.com/about</loc>
    <xhtml:link
      rel="alternate"
      hreflang="es"
      href="https://acme.com/es/about"/>
    <xhtml:link
      rel="alternate"
      hreflang="de"
      href="https://acme.com/de/about"/>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
  </url>
  <url>
    <loc>https://acme.com/blog</loc>
    <xhtml:link
      rel="alternate"
      hreflang="es"
      href="https://acme.com/es/blog"/>
    <xhtml:link
      rel="alternate"
      hreflang="de"
      href="https://acme.com/de/blog"/>
    <lastmod>2023-04-06T15:02:24.021Z</lastmod>
  </url>
</urlset>
```

### Generating multiple sitemaps

While a single sitemap will work for most applications. For large web applications, you may need to split a sitemap into multiple files.

There are two ways you can create multiple sitemaps:

- By nesting `sitemap.(xml|js|ts)` inside multiple route segments e.g. `app/sitemap.xml` and `app/products/sitemap.xml`.
- By using the [generateSitemaps](https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps) function.

For example, to split a sitemap using `generateSitemaps`, return an array of objects with the sitemap `id`. Then, use the `id` to generate the unique sitemaps.

 app/product/sitemap.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'
import { BASE_URL } from '@/app/lib/constants'

export async function generateSitemaps() {
  // Fetch the total number of products and calculate the number of sitemaps needed
  return [{ id: 0 }, { id: 1 }, { id: 2 }, { id: 3 }]
}

export default async function sitemap(props: {
  id: Promise<string>
}): Promise<MetadataRoute.Sitemap> {
  const id = await props.id
  // Google's limit is 50,000 URLs per sitemap
  const start = id * 50000
  const end = start + 50000
  const products = await getProducts(
    `SELECT id, date FROM products WHERE id BETWEEN ${start} AND ${end}`
  )
  return products.map((product) => ({
    url: `${BASE_URL}/product/${product.id}`,
    lastModified: product.date,
  }))
}
```

Your generated sitemaps will be available at `/.../sitemap/[id]`. For example, `/product/sitemap/1.xml`.

See the [generateSitemapsAPI reference](https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps) for more information.

## Returns

The default function exported from `sitemap.(xml|ts|js)` should return an array of objects with the following properties:

```
type Sitemap = Array<{
  url: string
  lastModified?: string | Date
  changeFrequency?:
    | 'always'
    | 'hourly'
    | 'daily'
    | 'weekly'
    | 'monthly'
    | 'yearly'
    | 'never'
  priority?: number
  alternates?: {
    languages?: Languages<string>
  }
}>
```

## Version History

| Version | Changes |
| --- | --- |
| v16.0.0 | idis now a promise that resolves to astring. |
| v14.2.0 | Add localizations support. |
| v13.4.14 | AddchangeFrequencyandpriorityattributes to sitemaps. |
| v13.3.0 | sitemapintroduced. |

## Next Steps

Learn how to use the generateSitemaps function.[generateSitemapsLearn how to use the generateSiteMaps function to create multiple sitemaps for your application.](https://nextjs.org/docs/app/api-reference/functions/generate-sitemaps)

Was this helpful?

supported.

---

# Metadata Files API Reference

> API documentation for the metadata file conventions.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)Metadata Files

# Metadata Files API Reference

Last updated  October 17, 2025

This section of the docs covers **Metadata file conventions**. File-based metadata can be defined by adding special metadata files to route segments.

Each file convention can be defined using a static file (e.g. `opengraph-image.jpg`), or a dynamic variant that uses code to generate the file (e.g. `opengraph-image.js`).

Once a file is defined, Next.js will automatically serve the file (with hashes in production for caching) and update the relevant head elements with the correct metadata, such as the asset's URL, file type, and image size.

> **Good to know**:
>
>
>
> - Special Route Handlers like [sitemap.ts](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap), [opengraph-image.tsx](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image), and [icon.tsx](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons), and other [metadata files](https://nextjs.org/docs/app/api-reference/file-conventions/metadata) are cached by default.
> - If using along with [proxy.ts](https://nextjs.org/docs/app/api-reference/file-conventions/proxy), [configure the matcher](https://nextjs.org/docs/app/api-reference/file-conventions/proxy#matcher) to exclude the metadata files.

[favicon, icon, and apple-iconAPI Reference for the Favicon, Icon and Apple Icon file conventions.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/app-icons)[manifest.jsonAPI Reference for manifest.json file.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/manifest)[opengraph-image and twitter-imageAPI Reference for the Open Graph Image and Twitter Image file conventions.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image)[robots.txtAPI Reference for robots.txt file.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots)[sitemap.xmlAPI Reference for the sitemap.xml file.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap)

Was this helpful?

supported.

---

# not

> API reference for the not-found.js file.

[API Reference](https://nextjs.org/docs/app/api-reference)[File-system conventions](https://nextjs.org/docs/app/api-reference/file-conventions)not-found.js

# not-found.js

Last updated  August 6, 2025

Next.js provides two conventions to handle not found cases:

- **not-found.js**: Used when you call the [notFound](https://nextjs.org/docs/app/api-reference/functions/not-found) function in a route segment.
- **global-not-found.js**: Used to define a global 404 page for unmatched routes across your entire app. This is handled at the routing level and doesn't depend on rendering a layout or page.

## not-found.js

The **not-found** file is used to render UI when the [notFound](https://nextjs.org/docs/app/api-reference/functions/not-found) function is thrown within a route segment. Along with serving a custom UI, Next.js will return a `200` HTTP status code for streamed responses, and `404` for non-streamed responses.

 app/not-found.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
      <Link href="/">Return Home</Link>
    </div>
  )
}
```

## global-not-found.js(experimental)

The `global-not-found.js` file lets you define a 404 page for your entire application. Unlike `not-found.js`, which works at the route level, this is used when a requested URL doesn't match any route at all. Next.js **skips rendering** and directly returns this global page.

The `global-not-found.js` file bypasses your app's normal rendering, which means you'll need to import any global styles, fonts, or other dependencies that your 404 page requires.

> **Good to know**: A smaller version of your global styles, and a simpler font family could improve performance of this page.

`global-not-found.js` is useful when you can't build a 404 page using a combination of `layout.js` and `not-found.js`. This can happen in two cases:

- Your app has multiple root layouts (e.g. `app/(admin)/layout.tsx` and `app/(shop)/layout.tsx`), so there's no single layout to compose a global 404 from.
- Your root layout is defined using top-level dynamic segments (e.g. `app/[country]/layout.tsx`), which makes composing a consistent 404 page harder.

To enable it, add the `globalNotFound` flag in `next.config.ts`:

 next.config.ts

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    globalNotFound: true,
  },
}

export default nextConfig
```

Then, create a file in the root of the `app` directory: `app/global-not-found.js`:

 app/global-not-found.tsxJavaScriptTypeScript

```
// Import global styles and fonts
import './globals.css'
import { Inter } from 'next/font/google'
import type { Metadata } from 'next'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '404 - Page Not Found',
  description: 'The page you are looking for does not exist.',
}

export default function GlobalNotFound() {
  return (
    <html lang="en" className={inter.className}>
      <body>
        <h1>404 - Page Not Found</h1>
        <p>This page does not exist.</p>
      </body>
    </html>
  )
}
```

Unlike `not-found.js`, this file must return a full HTML document, including `<html>` and `<body>` tags.

## Reference

### Props

`not-found.js` or `global-not-found.js` components do not accept any props.

> **Good to know**: In addition to catching expected `notFound()` errors, the root `app/not-found.js` and `app/global-not-found.js` files handle any unmatched URLs for your whole application. This means users that visit a URL that is not handled by your app will be shown the exported UI.

## Examples

### Data Fetching

By default, `not-found` is a Server Component. You can mark it as `async` to fetch and display data:

 app/not-found.tsxJavaScriptTypeScript

```
import Link from 'next/link'
import { headers } from 'next/headers'

export default async function NotFound() {
  const headersList = await headers()
  const domain = headersList.get('host')
  const data = await getSiteData(domain)
  return (
    <div>
      <h2>Not Found: {data.name}</h2>
      <p>Could not find requested resource</p>
      <p>
        View <Link href="/blog">all posts</Link>
      </p>
    </div>
  )
}
```

If you need to use Client Component hooks like `usePathname` to display content based on the path, you must fetch data on the client-side instead.

### Metadata

For `global-not-found.js`, you can export a `metadata` object or a [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) function to customize the `<title>`, `<meta>`, and other head tags for your 404 page:

> **Good to know**: Next.js automatically injects `<meta name="robots" content="noindex" />` for pages that return a 404 status code, including `global-not-found.js` pages.

 app/global-not-found.tsxJavaScriptTypeScript

```
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Not Found',
  description: 'The page you are looking for does not exist.',
}

export default function GlobalNotFound() {
  return (
    <html lang="en">
      <body>
        <div>
          <h1>Not Found</h1>
          <p>The page you are looking for does not exist.</p>
        </div>
      </body>
    </html>
  )
}
```

## Version History

| Version | Changes |
| --- | --- |
| v15.4.0 | global-not-found.jsintroduced (experimental). |
| v13.3.0 | Rootapp/not-foundhandles global unmatched URLs. |
| v13.0.0 | not-foundintroduced. |

Was this helpful?

supported.
