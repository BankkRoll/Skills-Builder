# How to build a Progressive Web Application (PWA) with Next.js and more

# How to build a Progressive Web Application (PWA) with Next.js

> Learn how to build a Progressive Web Application (PWA) with Next.js.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)PWAs

# How to build a Progressive Web Application (PWA) with Next.js

Last updated  August 21, 2025

Progressive Web Applications (PWAs) offer the reach and accessibility of web applications combined with the features and user experience of native mobile apps. With Next.js, you can create PWAs that provide a seamless, app-like experience across all platforms without the need for multiple codebases or app store approvals.

PWAs allow you to:

- Deploy updates instantly without waiting for app store approval
- Create cross-platform applications with a single codebase
- Provide native-like features such as home screen installation and push notifications

## Creating a PWA with Next.js

### 1. Creating the Web App Manifest

Next.js provides built-in support for creating a [web app manifest](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/manifest) using the App Router. You can create either a static or dynamic manifest file:

For example, create a `app/manifest.ts` or `app/manifest.json` file:

 app/manifest.tsJavaScriptTypeScript

```
import type { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Next.js PWA',
    short_name: 'NextPWA',
    description: 'A Progressive Web App built with Next.js',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#000000',
    icons: [
      {
        src: '/icon-192x192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512x512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  }
}
```

This file should contain information about the name, icons, and how it should be displayed as an icon on the user's device. This will allow users to install your PWA on their home screen, providing a native app-like experience.

You can use tools like [favicon generators](https://realfavicongenerator.net/) to create the different icon sets and place the generated files in your `public/` folder.

### 2. Implementing Web Push Notifications

Web Push Notifications are supported with all modern browsers, including:

- iOS 16.4+ for applications installed to the home screen
- Safari 16 for macOS 13 or later
- Chromium based browsers
- Firefox

This makes PWAs a viable alternative to native apps. Notably, you can trigger install prompts without needing offline support.

Web Push Notifications allow you to re-engage users even when they're not actively using your app. Here's how to implement them in a Next.js application:

First, let's create the main page component in `app/page.tsx`. We'll break it down into smaller parts for better understanding. First, we’ll add some of the imports and utilities we’ll need. It’s okay that the referenced Server Actions do not yet exist:

```
'use client'

import { useState, useEffect } from 'react'
import { subscribeUser, unsubscribeUser, sendNotification } from './actions'

function urlBase64ToUint8Array(base64String: string) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4)
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/')

  const rawData = window.atob(base64)
  const outputArray = new Uint8Array(rawData.length)

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i)
  }
  return outputArray
}
```

Let’s now add a component to manage subscribing, unsubscribing, and sending push notifications.

```
function PushNotificationManager() {
  const [isSupported, setIsSupported] = useState(false)
  const [subscription, setSubscription] = useState<PushSubscription | null>(
    null
  )
  const [message, setMessage] = useState('')

  useEffect(() => {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      setIsSupported(true)
      registerServiceWorker()
    }
  }, [])

  async function registerServiceWorker() {
    const registration = await navigator.serviceWorker.register('/sw.js', {
      scope: '/',
      updateViaCache: 'none',
    })
    const sub = await registration.pushManager.getSubscription()
    setSubscription(sub)
  }

  async function subscribeToPush() {
    const registration = await navigator.serviceWorker.ready
    const sub = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(
        process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!
      ),
    })
    setSubscription(sub)
    const serializedSub = JSON.parse(JSON.stringify(sub))
    await subscribeUser(serializedSub)
  }

  async function unsubscribeFromPush() {
    await subscription?.unsubscribe()
    setSubscription(null)
    await unsubscribeUser()
  }

  async function sendTestNotification() {
    if (subscription) {
      await sendNotification(message)
      setMessage('')
    }
  }

  if (!isSupported) {
    return <p>Push notifications are not supported in this browser.</p>
  }

  return (
    <div>
      <h3>Push Notifications</h3>
      {subscription ? (
        <>
          <p>You are subscribed to push notifications.</p>
          <button onClick={unsubscribeFromPush}>Unsubscribe</button>
          <input
            type="text"
            placeholder="Enter notification message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <button onClick={sendTestNotification}>Send Test</button>
        </>
      ) : (
        <>
          <p>You are not subscribed to push notifications.</p>
          <button onClick={subscribeToPush}>Subscribe</button>
        </>
      )}
    </div>
  )
}
```

Finally, let’s create a component to show a message for iOS devices to instruct them to install to their home screen, and only show this if the app is not already installed.

```
function InstallPrompt() {
  const [isIOS, setIsIOS] = useState(false)
  const [isStandalone, setIsStandalone] = useState(false)

  useEffect(() => {
    setIsIOS(
      /iPad|iPhone|iPod/.test(navigator.userAgent) && !(window as any).MSStream
    )

    setIsStandalone(window.matchMedia('(display-mode: standalone)').matches)
  }, [])

  if (isStandalone) {
    return null // Don't show install button if already installed
  }

  return (
    <div>
      <h3>Install App</h3>
      <button>Add to Home Screen</button>
      {isIOS && (
        <p>
          To install this app on your iOS device, tap the share button
          <span role="img" aria-label="share icon">
            {' '}
            ⎋{' '}
          </span>
          and then "Add to Home Screen"
          <span role="img" aria-label="plus icon">
            {' '}
            ➕{' '}
          </span>
          .
        </p>
      )}
    </div>
  )
}

export default function Page() {
  return (
    <div>
      <PushNotificationManager />
      <InstallPrompt />
    </div>
  )
}
```

Now, let’s create the Server Actions which this file calls.

### 3. Implementing Server Actions

Create a new file to contain your actions at `app/actions.ts`. This file will handle creating subscriptions, deleting subscriptions, and sending notifications.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import webpush from 'web-push'

webpush.setVapidDetails(
  '<mailto:your-email@example.com>',
  process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!,
  process.env.VAPID_PRIVATE_KEY!
)

let subscription: PushSubscription | null = null

export async function subscribeUser(sub: PushSubscription) {
  subscription = sub
  // In a production environment, you would want to store the subscription in a database
  // For example: await db.subscriptions.create({ data: sub })
  return { success: true }
}

export async function unsubscribeUser() {
  subscription = null
  // In a production environment, you would want to remove the subscription from the database
  // For example: await db.subscriptions.delete({ where: { ... } })
  return { success: true }
}

export async function sendNotification(message: string) {
  if (!subscription) {
    throw new Error('No subscription available')
  }

  try {
    await webpush.sendNotification(
      subscription,
      JSON.stringify({
        title: 'Test Notification',
        body: message,
        icon: '/icon.png',
      })
    )
    return { success: true }
  } catch (error) {
    console.error('Error sending push notification:', error)
    return { success: false, error: 'Failed to send notification' }
  }
}
```

Sending a notification will be handled by our service worker, created in step 5.

In a production environment, you would want to store the subscription in a database for persistence across server restarts and to manage multiple users' subscriptions.

### 4. Generating VAPID Keys

To use the Web Push API, you need to generate [VAPID](https://vapidkeys.com/) keys. The simplest way is to use the web-push CLI directly:

First, install web-push globally:

 Terminal

```
npm install -g web-push
```

Generate the VAPID keys by running:

 Terminal

```
web-push generate-vapid-keys
```

Copy the output and paste the keys into your `.env` file:

```
NEXT_PUBLIC_VAPID_PUBLIC_KEY=your_public_key_here
VAPID_PRIVATE_KEY=your_private_key_here
```

### 5. Creating a Service Worker

Create a `public/sw.js` file for your service worker:

 public/sw.js

```
self.addEventListener('push', function (event) {
  if (event.data) {
    const data = event.data.json()
    const options = {
      body: data.body,
      icon: data.icon || '/icon.png',
      badge: '/badge.png',
      vibrate: [100, 50, 100],
      data: {
        dateOfArrival: Date.now(),
        primaryKey: '2',
      },
    }
    event.waitUntil(self.registration.showNotification(data.title, options))
  }
})

self.addEventListener('notificationclick', function (event) {
  console.log('Notification click received.')
  event.notification.close()
  event.waitUntil(clients.openWindow('<https://your-website.com>'))
})
```

This service worker supports custom images and notifications. It handles incoming push events and notification clicks.

- You can set custom icons for notifications using the `icon` and `badge` properties.
- The `vibrate` pattern can be adjusted to create custom vibration alerts on supported devices.
- Additional data can be attached to the notification using the `data` property.

Remember to test your service worker thoroughly to ensure it behaves as expected across different devices and browsers. Also, make sure to update the `'https://your-website.com'` link in the `notificationclick` event listener to the appropriate URL for your application.

### 6. Adding to Home Screen

The `InstallPrompt` component defined in step 2 shows a message for iOS devices to instruct them to install to their home screen.

To ensure your application can be installed to a mobile home screen, you must have:

1. A valid web app manifest (created in step 1)
2. The website served over HTTPS

Modern browsers will automatically show an installation prompt to users when these criteria are met. You can provide a custom installation button with [beforeinstallprompt](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeinstallprompt_event), however, we do not recommend this as it is not cross browser and platform (does not work on Safari iOS).

### 7. Testing Locally

To ensure you can view notifications locally, ensure that:

- You are [running locally with HTTPS](https://nextjs.org/docs/app/api-reference/cli/next#using-https-during-development)
  - Use `next dev --experimental-https` for testing
- Your browser (Chrome, Safari, Firefox) has notifications enabled
  - When prompted locally, accept permissions to use notifications
  - Ensure notifications are not disabled globally for the entire browser
  - If you are still not seeing notifications, try using another browser to debug

### 8. Securing your application

Security is a crucial aspect of any web application, especially for PWAs. Next.js allows you to configure security headers using the `next.config.js` file. For example:

 next.config.js

```
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
      {
        source: '/sw.js',
        headers: [
          {
            key: 'Content-Type',
            value: 'application/javascript; charset=utf-8',
          },
          {
            key: 'Cache-Control',
            value: 'no-cache, no-store, must-revalidate',
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self'",
          },
        ],
      },
    ]
  },
}
```

Let’s go over each of these options:

1. Global Headers (applied to all routes):
  1. `X-Content-Type-Options: nosniff`: Prevents MIME type sniffing, reducing the risk of malicious file uploads.
  2. `X-Frame-Options: DENY`: Protects against clickjacking attacks by preventing your site from being embedded in iframes.
  3. `Referrer-Policy: strict-origin-when-cross-origin`: Controls how much referrer information is included with requests, balancing security and functionality.
2. Service Worker Specific Headers:
  1. `Content-Type: application/javascript; charset=utf-8`: Ensures the service worker is interpreted correctly as JavaScript.
  2. `Cache-Control: no-cache, no-store, must-revalidate`: Prevents caching of the service worker, ensuring users always get the latest version.
  3. `Content-Security-Policy: default-src 'self'; script-src 'self'`: Implements a strict Content Security Policy for the service worker, only allowing scripts from the same origin.

Learn more about defining [Content Security Policies](https://nextjs.org/docs/app/guides/content-security-policy) with Next.js.

## Extending your PWA

1. **Exploring PWA Capabilities**: PWAs can leverage various web APIs to provide advanced functionality. Consider exploring features like background sync, periodic background sync, or the File System Access API to enhance your application. For inspiration and up-to-date information on PWA capabilities, you can refer to resources like [What PWA Can Do Today](https://whatpwacando.today/).
2. **Static Exports:** If your application requires not running a server, and instead using a static export of files, you can update the Next.js configuration to enable this change. Learn more in the [Next.js Static Export documentation](https://nextjs.org/docs/app/guides/static-exports). However, you will need to move from Server Actions to calling an external API, as well as moving your defined headers to your proxy.
3. **Offline Support**: To provide offline functionality, one option is [Serwist](https://github.com/serwist/serwist) with Next.js. You can find an example of how to integrate Serwist with Next.js in their [documentation](https://github.com/serwist/serwist/tree/main/examples/next-basic). **Note:** this plugin currently requires webpack configuration.
4. **Security Considerations**: Ensure that your service worker is properly secured. This includes using HTTPS, validating the source of push messages, and implementing proper error handling.
5. **User Experience**: Consider implementing progressive enhancement techniques to ensure your app works well even when certain PWA features are not supported by the user's browser.

[manifest.jsonAPI Reference for manifest.json file.](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/manifest)

Was this helpful?

supported.

---

# Building public pages

> Learn how to build public, "static" pages that share data across users, such as landing pages, list pages (products, blogs, etc.), marketing and news sites.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Public pages

# Building public pages

Last updated  January 27, 2026

Public pages show the same content to every user. Common examples include landing pages, marketing pages, and product pages.

Since data is shared, these kind of pages can be [prerendered](https://nextjs.org/docs/app/glossary#prerendering) ahead of time and reused. This leads to faster page loads and lower server costs.

This guide will show you how to build public pages that share data across users.

## Example

As an example, we'll build a product list page.

We'll start with a static header, add a product list with async external data, and learn how to render it without blocking the response. Finally, we'll add a user-specific promotion banner without switching the entire page to [request-time rendering](https://nextjs.org/docs/app/glossary#request-time-rendering).

You can find the resources used in this example here:

- [Video](https://youtu.be/F6romq71KtI)
- [Demo](https://cache-components-public-pages.labs.vercel.dev/)
- [Code](https://github.com/vercel-labs/cache-components-public-pages)

### Step 1: Add a simple header

Let's start with a simple header.

 app/products/page.tsx

```
// Static component
function Header() {
  return <h1>Shop</h1>
}

export default async function Page() {
  return (
    <>
      <Header />
    </>
  )
}
```

#### Static components

The `<Header />` component doesn't depend on any inputs that change between requests, such as: external data, request headers, route params, the current time, or random values.

Since its output never changes and can be determined ahead of time, this kind of component is called a **static** component. With no reason to wait for a request, Next.js can safely **prerender** the page at [build time](https://nextjs.org/docs/app/glossary#build-time).

We can confirm this by running [next build](https://nextjs.org/docs/app/api-reference/cli/next#next-build-options).

 Terminal

```
Route (app)      Revalidate  Expire
┌ ○ /products           15m      1y
└ ○ /_not-found

○  (Static)  prerendered as static content
```

Notice that the product route is marked as static, even though we didn't add any explicit configuration.

### Step 2: Add the product list

Now, let's fetch and render our product list.

 app/products/page.tsx

```
import db from '@/db'
import { List } from '@/app/products/ui'

function Header() {}

// Dynamic component
async function ProductList() {
  const products = await db.product.findMany()
  return <List items={products} />
}

export default async function Page() {
  return (
    <>
      <Header />
      <ProductList />
    </>
  )
}
```

Unlike the header, the product list depends on external data.

#### Dynamic components

Since this data **can** change over time, the rendered output is no longer guaranteed to be stable. This makes the product list a **dynamic** component.

Without guidance, the framework assumes you want to fetch **fresh** data on every user request. This design choice reflects standard web behavior where a new server request renders the page.

However, if this component is rendered at request time, fetching its data will delay the **entire** route from responding. If we refresh the page, we can see this happen.

Even though the header is rendered instantly, it can't be sent to the browser until the product list has finished fetching.

To protect us from this performance cliff, Next.js will show us a [warning](https://nextjs.org/docs/messages/blocking-route) the first time we **await** data: `Blocking data was accessed outside of Suspense`

At this point, we have to decide how to **unblock** the response. Either:

- [Cache](https://nextjs.org/docs/app/glossary#cache-components) the component, so it becomes **stable** and can be prerendered with the rest of the page.
- [Stream](https://nextjs.org/docs/app/glossary#streaming) the component, so it becomes **non-blocking** and the rest of the page doesn't have to wait for it.

In our case, the product catalog is shared across all users, so caching is the right choice.

### Cache components

We can mark a function as cacheable using the ['use cache'](https://nextjs.org/docs/app/api-reference/directives/use-cache) directive.

 app/products/page.tsx

```
import db from '@/db'
import { List } from '@/app/products/ui'

function Header() {}

// Cache component
async function ProductList() {
  'use cache'
  const products = await db.product.findMany()
  return <List items={products} />
}

export default async function Page() {
  return (
    <>
      <Header />
      <ProductList />
    </>
  )
}
```

This turns it into a [cache component](https://nextjs.org/docs/app/glossary#cache-components). The first time it runs, whatever we return will be cached and reused.

If a cache component's inputs are available **before** the request arrives, it can be prerendered just like a static component.

If we refresh again, we can see the page loads instantly because the cache component doesn't block the response. And, if we run `next build` again, we can confirm the page is still static:

 Terminal

```
Route (app)      Revalidate  Expire
┌ ○ /products           15m      1y
└ ○ /_not-found

○  (Static)  prerendered as static content
```

But, pages rarely stay static forever.

### Step 3: Add a dynamic promotion banner

Sooner or later, even simple pages need some dynamic content. To demonstrate this, let's add a promotional banner:

 app/products/page.tsx

```
import db from '@/db'
import { List, Promotion } from '@/app/products/ui'
import { getPromotion } from '@/app/products/data'

function Header() {}

async function ProductList() {}

// Dynamic component
async function PromotionContent() {
  const promotion = await getPromotion()
  return <Promotion data={promotion} />
}

export default async function Page() {
  return (
    <>
      <PromotionContent />
      <Header />
      <ProductList />
    </>
  )
}
```

Once again, this starts off as dynamic. And as before, introducing blocking behavior triggers a Next.js warning.

Last time, the data was shared, so it could be cached. This time, the promotion depends on request specific inputs like the user's location and A/B tests, so we can't cache our way out of the blocking behavior.

### Partial prerendering

Adding dynamic content doesn't mean we have to go back to a fully blocking render. We can unblock the response with streaming.

Next.js supports streaming by default. We can use a [Suspense boundary](https://nextjs.org/docs/app/glossary#suspense-boundary) to tell the framework where to slice the streamed response into *chunks*, and what fallback UI to show while content loads.

 app/products/page.tsx

```
import { Suspense } from 'react'
import db from '@/db'
import { List, Promotion, PromotionSkeleton } from '@/app/products/ui'
import { getPromotion } from '@/app/products/data'

function Header() {}

async function ProductList() {}

// Dynamic component (streamed)
async function PromotionContent() {
  const promotion = await getPromotion()
  return <Promotion data={promotion} />
}

export default async function Page() {
  return (
    <>
      <Suspense fallback={<PromotionSkeleton />}>
        <PromotionContent />
      </Suspense>
      <Header />
      <ProductList />
    </>
  )
}
```

The fallback is prerendered alongside the rest of our static and cached content. The inner component streams in later, once its async work completes.

With this change, Next.js can separate prerenderable work from request-time work and the route becomes [partially prerendered](https://nextjs.org/docs/app/glossary#partial-prerendering-ppr).

Again, we can confirm this by running `next build`:

 Terminal

```
Route (app)      Revalidate  Expire
┌ ◐ /products    15m      1y
└ ◐ /_not-found

◐  (Partial Prerender)  Prerendered as static HTML with dynamic server-streamed content
```

At [build time](https://nextjs.org/docs/app/glossary#build-time), most of the page, including the header, product list and promotion fallback, is rendered, cached and pushed to a content delivery network.

At [request time](https://nextjs.org/docs/app/glossary#request-time), the prerendered part is served instantly from a CDN node close to the user.

In parallel, the user specific promotion is rendered on the server, streamed to the client, and swapped into the fallback slot.

If we refresh the page one last time, we can see most of the page loads instantly, while the dynamic parts stream in as they become available.

### Next steps

We've learned how to build mostly static pages that include pockets of dynamic content.

We started with a static page, added async work, and resolved the blocking behavior by caching what could be prerendered, and streaming what couldn't.

In future guides, we'll learn how to:

- Revalidate prerendered pages or cached data.
- Create variants of the same page with route params.
- Create private pages with personalized user data.

Was this helpful?

supported.

---

# How to handle redirects in Next.js

> Learn the different ways to handle redirects in Next.js.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Redirecting

# How to handle redirects in Next.js

Last updated  January 23, 2026

There are a few ways you can handle redirects in Next.js. This page will go through each available option, use cases, and how to manage large numbers of redirects.

| API | Purpose | Where | Status Code |
| --- | --- | --- | --- |
| redirect | Redirect user after a mutation or event | Server Components, Server Functions, Route Handlers | 307 (Temporary) or 303 (Server Action) |
| permanentRedirect | Redirect user after a mutation or event | Server Components, Server Functions, Route Handlers | 308 (Permanent) |
| useRouter | Perform a client-side navigation | Event Handlers in Client Components | N/A |
| redirectsinnext.config.js | Redirect an incoming request based on a path | next.config.jsfile | 307 (Temporary) or 308 (Permanent) |
| NextResponse.redirect | Redirect an incoming request based on a condition | Proxy | Any |

## redirectfunction

The `redirect` function allows you to redirect the user to another URL. You can call `redirect` in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data).

`redirect` is often used after a mutation or event. For example, creating a post:

app/actions.tsJavaScriptTypeScript

```
'use server'

import { redirect } from 'next/navigation'
import { revalidatePath } from 'next/cache'

export async function createPost(id: string) {
  try {
    // Call database
  } catch (error) {
    // Handle errors
  }

  revalidatePath('/posts') // Update cached posts
  redirect(`/post/${id}`) // Navigate to the new post page
}
```

> **Good to know**:
>
>
>
> - `redirect` returns a 307 (Temporary Redirect) status code by default. When used in a Server Action, it returns a 303 (See Other), which is commonly used for redirecting to a success page as a result of a POST request.
> - `redirect` throws an error so it should be called **outside** the `try` block when using `try/catch` statements.
> - `redirect` can be called in Client Components during the rendering process but not in event handlers. You can use the [useRouterhook](#userouter-hook) instead.
> - `redirect` also accepts absolute URLs and can be used to redirect to external links.
> - If you'd like to redirect before the render process, use [next.config.js](#redirects-in-nextconfigjs) or [Proxy](#nextresponseredirect-in-proxy).

See the [redirectAPI reference](https://nextjs.org/docs/app/api-reference/functions/redirect) for more information.

## permanentRedirectfunction

The `permanentRedirect` function allows you to **permanently** redirect the user to another URL. You can call `permanentRedirect` in [Server Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route), and [Server Functions](https://nextjs.org/docs/app/getting-started/updating-data).

`permanentRedirect` is often used after a mutation or event that changes an entity's canonical URL, such as updating a user's profile URL after they change their username:

app/actions.tsJavaScriptTypeScript

```
'use server'

import { permanentRedirect } from 'next/navigation'
import { revalidateTag } from 'next/cache'

export async function updateUsername(username: string, formData: FormData) {
  try {
    // Call database
  } catch (error) {
    // Handle errors
  }

  revalidateTag('username') // Update all references to the username
  permanentRedirect(`/profile/${username}`) // Navigate to the new user profile
}
```

> **Good to know**:
>
>
>
> - `permanentRedirect` returns a 308 (permanent redirect) status code by default.
> - `permanentRedirect` also accepts absolute URLs and can be used to redirect to external links.
> - If you'd like to redirect before the render process, use [next.config.js](#redirects-in-nextconfigjs) or [Proxy](#nextresponseredirect-in-proxy).

See the [permanentRedirectAPI reference](https://nextjs.org/docs/app/api-reference/functions/permanentRedirect) for more information.

## useRouter()hook

If you need to redirect inside an event handler in a Client Component, you can use the `push` method from the `useRouter` hook. For example:

app/page.tsxJavaScriptTypeScript

```
'use client'

import { useRouter } from 'next/navigation'

export default function Page() {
  const router = useRouter()

  return (
    <button type="button" onClick={() => router.push('/dashboard')}>
      Dashboard
    </button>
  )
}
```

> **Good to know**:
>
>
>
> - If you don't need to programmatically navigate a user, you should use a [<Link>](https://nextjs.org/docs/app/api-reference/components/link) component.

See the [useRouterAPI reference](https://nextjs.org/docs/app/api-reference/functions/use-router) for more information.

## redirectsinnext.config.js

The `redirects` option in the `next.config.js` file allows you to redirect an incoming request path to a different destination path. This is useful when you change the URL structure of pages or have a list of redirects that are known ahead of time.

`redirects` supports [path](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects#path-matching), [header, cookie, and query matching](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects#header-cookie-and-query-matching), giving you the flexibility to redirect users based on an incoming request.

To use `redirects`, add the option to your `next.config.js` file:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  async redirects() {
    return [
      // Basic redirect
      {
        source: '/about',
        destination: '/',
        permanent: true,
      },
      // Wildcard path matching
      {
        source: '/blog/:slug',
        destination: '/news/:slug',
        permanent: true,
      },
    ]
  },
}

export default nextConfig
```

See the [redirectsAPI reference](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects) for more information.

> **Good to know**:
>
>
>
> - `redirects` can return a 307 (Temporary Redirect) or 308 (Permanent Redirect) status code with the `permanent` option.
> - `redirects` may have a limit on platforms. For example, on Vercel, there's a limit of 1,024 redirects. To manage a large number of redirects (1000+), consider creating a custom solution using [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy). See [managing redirects at scale](#managing-redirects-at-scale-advanced) for more.
> - `redirects` runs **before** Proxy.

## NextResponse.redirectin Proxy

Proxy allows you to run code before a request is completed. Then, based on the incoming request, redirect to a different URL using `NextResponse.redirect`. This is useful if you want to redirect users based on a condition (e.g. authentication, session management, etc) or have [a large number of redirects](#managing-redirects-at-scale-advanced).

For example, to redirect the user to a `/login` page if they are not authenticated:

 proxy.tsJavaScriptTypeScript

```
import { NextResponse, NextRequest } from 'next/server'
import { authenticate } from 'auth-provider'

export function proxy(request: NextRequest) {
  const isAuthenticated = authenticate(request)

  // If the user is authenticated, continue as normal
  if (isAuthenticated) {
    return NextResponse.next()
  }

  // Redirect to login page if not authenticated
  return NextResponse.redirect(new URL('/login', request.url))
}

export const config = {
  matcher: '/dashboard/:path*',
}
```

> **Good to know**:
>
>
>
> - Proxy runs **after** `redirects` in `next.config.js` and **before** rendering.

See the [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) documentation for more information.

## Managing redirects at scale (advanced)

To manage a large number of redirects (1000+), you may consider creating a custom solution using Proxy. This allows you to handle redirects programmatically without having to redeploy your application.

To do this, you'll need to consider:

1. Creating and storing a redirect map.
2. Optimizing data lookup performance.

> **Next.js Example**: See our [Proxy with Bloom filter](https://redirects-bloom-filter.vercel.app/) example for an implementation of the recommendations below.

### 1. Creating and storing a redirect map

A redirect map is a list of redirects that you can store in a database (usually a key-value store) or JSON file.

Consider the following data structure:

```
{
  "/old": {
    "destination": "/new",
    "permanent": true
  },
  "/blog/post-old": {
    "destination": "/blog/post-new",
    "permanent": true
  }
}
```

In [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy), you can read from a database such as Vercel's [Edge Config](https://vercel.com/docs/edge-config/get-started) or [Redis](https://vercel.com/docs/redis), and redirect the user based on the incoming request:

 proxy.tsJavaScriptTypeScript

```
import { NextResponse, NextRequest } from 'next/server'
import { get } from '@vercel/edge-config'

type RedirectEntry = {
  destination: string
  permanent: boolean
}

export async function proxy(request: NextRequest) {
  const pathname = request.nextUrl.pathname
  const redirectData = await get(pathname)

  if (redirectData && typeof redirectData === 'string') {
    const redirectEntry: RedirectEntry = JSON.parse(redirectData)
    const statusCode = redirectEntry.permanent ? 308 : 307
    return NextResponse.redirect(redirectEntry.destination, statusCode)
  }

  // No redirect found, continue without redirecting
  return NextResponse.next()
}
```

### 2. Optimizing data lookup performance

Reading a large dataset for every incoming request can be slow and expensive. There are two ways you can optimize data lookup performance:

- Use a database that is optimized for fast reads
- Use a data lookup strategy such as a [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) to efficiently check if a redirect exists **before** reading the larger redirects file or database.

Considering the previous example, you can import a generated bloom filter file into Proxy, then, check if the incoming request pathname exists in the bloom filter.

If it does, forward the request to a [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route)   which will check the actual file and redirect the user to the appropriate URL. This avoids importing a large redirects file into Proxy, which can slow down every incoming request.

 proxy.tsJavaScriptTypeScript

```
import { NextResponse, NextRequest } from 'next/server'
import { ScalableBloomFilter } from 'bloom-filters'
import GeneratedBloomFilter from './redirects/bloom-filter.json'

type RedirectEntry = {
  destination: string
  permanent: boolean
}

// Initialize bloom filter from a generated JSON file
const bloomFilter = ScalableBloomFilter.fromJSON(GeneratedBloomFilter as any)

export async function proxy(request: NextRequest) {
  // Get the path for the incoming request
  const pathname = request.nextUrl.pathname

  // Check if the path is in the bloom filter
  if (bloomFilter.has(pathname)) {
    // Forward the pathname to the Route Handler
    const api = new URL(
      `/api/redirects?pathname=${encodeURIComponent(request.nextUrl.pathname)}`,
      request.nextUrl.origin
    )

    try {
      // Fetch redirect data from the Route Handler
      const redirectData = await fetch(api)

      if (redirectData.ok) {
        const redirectEntry: RedirectEntry | undefined =
          await redirectData.json()

        if (redirectEntry) {
          // Determine the status code
          const statusCode = redirectEntry.permanent ? 308 : 307

          // Redirect to the destination
          return NextResponse.redirect(redirectEntry.destination, statusCode)
        }
      }
    } catch (error) {
      console.error(error)
    }
  }

  // No redirect found, continue the request without redirecting
  return NextResponse.next()
}
```

Then, in the Route Handler:

app/api/redirects/route.tsJavaScriptTypeScript

```
import { NextRequest, NextResponse } from 'next/server'
import redirects from '@/app/redirects/redirects.json'

type RedirectEntry = {
  destination: string
  permanent: boolean
}

export function GET(request: NextRequest) {
  const pathname = request.nextUrl.searchParams.get('pathname')
  if (!pathname) {
    return new Response('Bad Request', { status: 400 })
  }

  // Get the redirect entry from the redirects.json file
  const redirect = (redirects as Record<string, RedirectEntry>)[pathname]

  // Account for bloom filter false positives
  if (!redirect) {
    return new Response('No redirect', { status: 400 })
  }

  // Return the redirect entry
  return NextResponse.json(redirect)
}
```

> **Good to know:**
>
>
>
> - To generate a bloom filter, you can use a library like [bloom-filters](https://www.npmjs.com/package/bloom-filters).
> - You should validate requests made to your Route Handler to prevent malicious requests.

[redirectAPI Reference for the redirect function.](https://nextjs.org/docs/app/api-reference/functions/redirect)[permanentRedirectAPI Reference for the permanentRedirect function.](https://nextjs.org/docs/app/api-reference/functions/permanentRedirect)[proxy.jsAPI reference for the proxy.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)[redirectsAdd redirects to your Next.js app.](https://nextjs.org/docs/app/api-reference/config/next-config-js/redirects)

Was this helpful?

supported.

---

# How to use Sass

> Style your Next.js application using Sass.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Sass

# How to use Sass

Last updated  April 25, 2025

Next.js has built-in support for integrating with Sass after the package is installed using both the `.scss` and `.sass` extensions. You can use component-level Sass via CSS Modules and the `.module.scss`or `.module.sass` extension.

First, install [sass](https://github.com/sass/sass):

 Terminal

```
npm install --save-dev sass
```

> **Good to know**:
>
>
>
> Sass supports [two different syntaxes](https://sass-lang.com/documentation/syntax), each with their own extension.
> The `.scss` extension requires you use the [SCSS syntax](https://sass-lang.com/documentation/syntax#scss),
> while the `.sass` extension requires you use the [Indented Syntax ("Sass")](https://sass-lang.com/documentation/syntax#the-indented-syntax).
>
>
>
> If you're not sure which to choose, start with the `.scss` extension which is a superset of CSS, and doesn't require you learn the
> Indented Syntax ("Sass").

### Customizing Sass Options

If you want to configure your Sass options, use `sassOptions` in `next.config`.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  sassOptions: {
    additionalData: `$var: red;`,
  },
}

export default nextConfig
```

#### Implementation

You can use the `implementation` property to specify the Sass implementation to use. By default, Next.js uses the [sass](https://www.npmjs.com/package/sass) package.

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  sassOptions: {
    implementation: 'sass-embedded',
  },
}

export default nextConfig
```

### Sass Variables

Next.js supports Sass variables exported from CSS Module files.

For example, using the exported `primaryColor` Sass variable:

 app/variables.module.scss

```
$primary-color: #64ff00;

:export {
  primaryColor: $primary-color;
}
```

 app/page.js

```
// maps to root `/` URL

import variables from './variables.module.scss'

export default function Page() {
  return <h1 style={{ color: variables.primaryColor }}>Hello, Next.js!</h1>
}
```

Was this helpful?

supported.

---

# How to load and optimize scripts

> Optimize 3rd party scripts with the built-in Script component.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Scripts

# How to load and optimize scripts

Last updated  January 24, 2026

### Layout Scripts

To load a third-party script for multiple routes, import `next/script` and include the script directly in your layout component:

app/dashboard/layout.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <section>{children}</section>
      <Script src="https://example.com/script.js" />
    </>
  )
}
```

The third-party script is fetched when the folder route (e.g. `dashboard/page.js`) or any nested route (e.g. `dashboard/settings/page.js`) is accessed by the user. Next.js will ensure the script will **only load once**, even if a user navigates between multiple routes in the same layout.

### Application Scripts

To load a third-party script for all routes, import `next/script` and include the script directly in your root layout:

app/layout.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
      <Script src="https://example.com/script.js" />
    </html>
  )
}
```

This script will load and execute when *any* route in your application is accessed. Next.js will ensure the script will **only load once**, even if a user navigates between multiple pages.

> **Recommendation**: We recommend only including third-party scripts in specific pages or layouts in order to minimize any unnecessary impact to performance.

### Strategy

Although the default behavior of `next/script` allows you to load third-party scripts in any page or layout, you can fine-tune its loading behavior by using the `strategy` property:

- `beforeInteractive`: Load the script before any Next.js code and before any page hydration occurs.
- `afterInteractive`: (**default**) Load the script early but after some hydration on the page occurs.
- `lazyOnload`: Load the script later during browser idle time.
- `worker`: (experimental) Load the script in a web worker.

Refer to the [next/script](https://nextjs.org/docs/app/api-reference/components/script#strategy) API reference documentation to learn more about each strategy and their use cases.

### Offloading Scripts To A Web Worker (experimental)

> **Warning:** The `worker` strategy is not yet stable and does not yet work with the App Router. Use with caution.

Scripts that use the `worker` strategy are offloaded and executed in a web worker with [Partytown](https://partytown.qwik.dev/). This can improve the performance of your site by dedicating the main thread to the rest of your application code.

This strategy is still experimental and can only be used if the `nextScriptWorkers` flag is enabled in `next.config.js`:

 next.config.js

```
module.exports = {
  experimental: {
    nextScriptWorkers: true,
  },
}
```

Then, run `next` (normally `npm run dev` or `yarn dev`) and Next.js will guide you through the installation of the required packages to finish the setup:

 Terminal

```
npm run dev
```

You'll see instructions like these: Please install Partytown by running `npm install @qwik.dev/partytown`

Once setup is complete, defining `strategy="worker"` will automatically instantiate Partytown in your application and offload the script to a web worker.

 pages/home.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function Home() {
  return (
    <>
      <Script src="https://example.com/script.js" strategy="worker" />
    </>
  )
}
```

There are a number of trade-offs that need to be considered when loading a third-party script in a web worker. Please see Partytown's [tradeoffs](https://partytown.qwik.dev/trade-offs) documentation for more information.

### Inline Scripts

Inline scripts, or scripts not loaded from an external file, are also supported by the Script component. They can be written by placing the JavaScript within curly braces:

```
<Script id="show-banner">
  {`document.getElementById('banner').classList.remove('hidden')`}
</Script>
```

Or by using the `dangerouslySetInnerHTML` property:

```
<Script
  id="show-banner"
  dangerouslySetInnerHTML={{
    __html: `document.getElementById('banner').classList.remove('hidden')`,
  }}
/>
```

> **Warning**: An `id` property must be assigned for inline scripts in order for Next.js to track and optimize the script.

### Executing Additional Code

Event handlers can be used with the Script component to execute additional code after a certain event occurs:

- `onLoad`: Execute code after the script has finished loading.
- `onReady`: Execute code after the script has finished loading and every time the component is mounted.
- `onError`: Execute code if the script fails to load.

These handlers will only work when `next/script` is imported and used inside of a [Client Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) where `"use client"` is defined as the first line of code:

app/page.tsxJavaScriptTypeScript

```
'use client'

import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script
        src="https://example.com/script.js"
        onLoad={() => {
          console.log('Script has loaded')
        }}
      />
    </>
  )
}
```

Refer to the [next/script](https://nextjs.org/docs/app/api-reference/components/script#onload) API reference to learn more about each event handler and view examples.

### Additional Attributes

There are many DOM attributes that can be assigned to a `<script>` element that are not used by the Script component, like [nonce](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/nonce) or [custom data attributes](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/data-*). Including any additional attributes will automatically forward it to the final, optimized `<script>` element that is included in the HTML.

 app/page.tsxJavaScriptTypeScript

```
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script
        src="https://example.com/script.js"
        id="example-script"
        nonce="XUENAJFW"
        data-test="script"
      />
    </>
  )
}
```

## API Reference

Learn more about the next/script API.[Script ComponentOptimize third-party scripts in your Next.js application using the built-in `next/script` Component.](https://nextjs.org/docs/app/api-reference/components/script)

Was this helpful?

supported.
