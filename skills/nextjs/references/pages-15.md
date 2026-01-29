# How to preview content with Draft Mode in Next.js and more

# How to preview content with Draft Mode in Next.js

> Next.js has draft mode to toggle between static and dynamic pages. You can learn how it works with Pages Router.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Draft ModeYou are currently viewing the documentation for Pages Router.

# How to preview content with Draft Mode in Next.js

Last updated  May 21, 2025

In the [Pages documentation](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts) and the [Data Fetching documentation](https://nextjs.org/docs/pages/building-your-application/data-fetching), we talked about how to pre-render a page at build time (**Static Generation**) using `getStaticProps` and `getStaticPaths`.

Static Generation is useful when your pages fetch data from a headless CMS. However, it’s not ideal when you’re writing a draft on your headless CMS and want to view the draft immediately on your page. You’d want Next.js to render these pages at **request time** instead of build time and fetch the draft content instead of the published content. You’d want Next.js to bypass Static Generation only for this specific case.

Next.js has a feature called **Draft Mode** which solves this problem. Here are instructions on how to use it.

## Step 1: Create and access the API route

> Take a look at the [API Routes documentation](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) first if you’re not familiar with Next.js API Routes.

First, create the **API route**. It can have any name - e.g. `pages/api/draft.ts`

In this API route, you need to call `setDraftMode` on the response object.

```
export default function handler(req, res) {
  // ...
  res.setDraftMode({ enable: true })
  // ...
}
```

This will set a **cookie** to enable draft mode. Subsequent requests containing this cookie will trigger **Draft Mode** changing the behavior for statically generated pages (more on this later).

You can test this manually by creating an API route like below and accessing it from your browser manually:

 pages/api/draft.ts

```
// simple example for testing it manually from your browser.
export default function handler(req, res) {
  res.setDraftMode({ enable: true })
  res.end('Draft mode is enabled')
}
```

If you open your browser’s developer tools and visit `/api/draft`, you’ll notice a `Set-Cookie` response header with a cookie named `__prerender_bypass`.

### Securely accessing it from your Headless CMS

In practice, you’d want to call this API route *securely* from your headless CMS. The specific steps will vary depending on which headless CMS you’re using, but here are some common steps you could take.

These steps assume that the headless CMS you’re using supports setting **custom draft URLs**. If it doesn’t, you can still use this method to secure your draft URLs, but you’ll need to construct and access the draft URL manually.

**First**, you should create a **secret token string** using a token generator of your choice. This secret will only be known by your Next.js app and your headless CMS. This secret prevents people who don’t have access to your CMS from accessing draft URLs.

**Second**, if your headless CMS supports setting custom draft URLs, specify the following as the draft URL. This assumes that your draft API route is located at `pages/api/draft.ts`.

 Terminal

```
https://<your-site>/api/draft?secret=<token>&slug=<path>
```

- `<your-site>` should be your deployment domain.
- `<token>` should be replaced with the secret token you generated.
- `<path>` should be the path for the page that you want to view. If you want to view `/posts/foo`, then you should use `&slug=/posts/foo`.

Your headless CMS might allow you to include a variable in the draft URL so that `<path>` can be set dynamically based on the CMS’s data like so: `&slug=/posts/{entry.fields.slug}`

**Finally**, in the draft API route:

- Check that the secret matches and that the `slug` parameter exists (if not, the request should fail).
-
- Call `res.setDraftMode`.
- Then redirect the browser to the path specified by `slug`. (The following example uses a [307 redirect](https://developer.mozilla.org/docs/Web/HTTP/Status/307)).

```
export default async (req, res) => {
  // Check the secret and next parameters
  // This secret should only be known to this API route and the CMS
  if (req.query.secret !== 'MY_SECRET_TOKEN' || !req.query.slug) {
    return res.status(401).json({ message: 'Invalid token' })
  }

  // Fetch the headless CMS to check if the provided `slug` exists
  // getPostBySlug would implement the required fetching logic to the headless CMS
  const post = await getPostBySlug(req.query.slug)

  // If the slug doesn't exist prevent draft mode from being enabled
  if (!post) {
    return res.status(401).json({ message: 'Invalid slug' })
  }

  // Enable Draft Mode by setting the cookie
  res.setDraftMode({ enable: true })

  // Redirect to the path from the fetched post
  // We don't redirect to req.query.slug as that might lead to open redirect vulnerabilities
  res.redirect(post.slug)
}
```

If it succeeds, then the browser will be redirected to the path you want to view with the draft mode cookie.

## Step 2: UpdategetStaticProps

The next step is to update `getStaticProps` to support draft mode.

If you request a page which has `getStaticProps` with the cookie set (via `res.setDraftMode`), then `getStaticProps` will be called at **request time** (instead of at build time).

Furthermore, it will be called with a `context` object where `context.draftMode` will be `true`.

```
export async function getStaticProps(context) {
  if (context.draftMode) {
    // dynamic data
  }
}
```

We used `res.setDraftMode` in the draft API route, so `context.draftMode` will be `true`.

If you’re also using `getStaticPaths`, then `context.params` will also be available.

### Fetch draft data

You can update `getStaticProps` to fetch different data based on `context.draftMode`.

For example, your headless CMS might have a different API endpoint for draft posts. If so, you can modify the API endpoint URL like below:

```
export async function getStaticProps(context) {
  const url = context.draftMode
    ? 'https://draft.example.com'
    : 'https://production.example.com'
  const res = await fetch(url)
  // ...
}
```

That’s it! If you access the draft API route (with `secret` and `slug`) from your headless CMS or manually, you should now be able to see the draft content. And if you update your draft without publishing, you should be able to view the draft.

Set this as the draft URL on your headless CMS or access manually, and you should be able to see the draft.

 Terminal

```
https://<your-site>/api/draft?secret=<token>&slug=<path>
```

## More Details

### Clear the Draft Mode cookie

By default, the Draft Mode session ends when the browser is closed.

To clear the Draft Mode cookie manually, create an API route that calls `setDraftMode({ enable: false })`:

 pages/api/disable-draft.ts

```
export default function handler(req, res) {
  res.setDraftMode({ enable: false })
}
```

Then, send a request to `/api/disable-draft` to invoke the API Route. If calling this route using [next/link](https://nextjs.org/docs/pages/api-reference/components/link), you must pass `prefetch={false}` to prevent accidentally deleting the cookie on prefetch.

### Works withgetServerSideProps

Draft Mode works with `getServerSideProps`, and is available as a `draftMode` key in the [context](https://nextjs.org/docs/pages/api-reference/functions/get-server-side-props#context-parameter) object.

> **Good to know**: You shouldn't set the `Cache-Control` header when using Draft Mode because it cannot be bypassed. Instead, we recommend using [ISR](https://nextjs.org/docs/pages/guides/incremental-static-regeneration).

### Works with API Routes

API Routes will have access to `draftMode` on the request object. For example:

```
export default function myApiRoute(req, res) {
  if (req.draftMode) {
    // get draft data
  }
}
```

### Unique pernext build

A new bypass cookie value will be generated each time you run `next build`.

This ensures that the bypass cookie can’t be guessed.

> **Good to know**: To test Draft Mode locally over HTTP, your browser will need to allow third-party cookies and local storage access.

Was this helpful?

supported.

---

# How to use environment variables in Next.js

> Learn to add and access environment variables in your Next.js application.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Environment VariablesYou are currently viewing the documentation for Pages Router.

# How to use environment variables in Next.js

Last updated  April 24, 2025

Next.js comes with built-in support for environment variables, which allows you to do the following:

- [Use.envto load environment variables](#loading-environment-variables)
- [Bundle environment variables for the browser by prefixing withNEXT_PUBLIC_](#bundling-environment-variables-for-the-browser)

> **Warning:** The default `create-next-app` template ensures all `.env` files are added to your `.gitignore`. You almost never want to commit these files to your repository.

## Loading Environment Variables

Next.js has built-in support for loading environment variables from `.env*` files into `process.env`.

 .env

```
DB_HOST=localhost
DB_USER=myuser
DB_PASS=mypassword
```

This loads `process.env.DB_HOST`, `process.env.DB_USER`, and `process.env.DB_PASS` into the Node.js environment automatically allowing you to use them in [Next.js data fetching methods](https://nextjs.org/docs/pages/building-your-application/data-fetching) and [API routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes).

For example, using [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props):

pages/index.js

```
export async function getStaticProps() {
  const db = await myDB.connect({
    host: process.env.DB_HOST,
    username: process.env.DB_USER,
    password: process.env.DB_PASS,
  })
  // ...
}
```

### Loading Environment Variables with@next/env

If you need to load environment variables outside of the Next.js runtime, such as in a root config file for an ORM or test runner, you can use the `@next/env` package.

This package is used internally by Next.js to load environment variables from `.env*` files.

To use it, install the package and use the `loadEnvConfig` function to load the environment variables:

```
npm install @next/env
```

 envConfig.tsJavaScriptTypeScript

```
import { loadEnvConfig } from '@next/env'

const projectDir = process.cwd()
loadEnvConfig(projectDir)
```

Then, you can import the configuration where needed. For example:

 orm.config.tsJavaScriptTypeScript

```
import './envConfig.ts'

export default defineConfig({
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
})
```

### Referencing Other Variables

Next.js will automatically expand variables that use `$` to reference other variables e.g. `$VARIABLE` inside of your `.env*` files. This allows you to reference other secrets. For example:

 .env

```
TWITTER_USER=nextjs
TWITTER_URL=https://x.com/$TWITTER_USER
```

In the above example, `process.env.TWITTER_URL` would be set to `https://x.com/nextjs`.

> **Good to know**: If you need to use variable with a `$` in the actual value, it needs to be escaped e.g. `\$`.

## Bundling Environment Variables for the Browser

Non-`NEXT_PUBLIC_` environment variables are only available in the Node.js environment, meaning they aren't accessible to the browser (the client runs in a different *environment*).

In order to make the value of an environment variable accessible in the browser, Next.js can "inline" a value, at build time, into the js bundle that is delivered to the client, replacing all references to `process.env.[variable]` with a hard-coded value. To tell it to do this, you just have to prefix the variable with `NEXT_PUBLIC_`. For example:

 Terminal

```
NEXT_PUBLIC_ANALYTICS_ID=abcdefghijk
```

This will tell Next.js to replace all references to `process.env.NEXT_PUBLIC_ANALYTICS_ID` in the Node.js environment with the value from the environment in which you run `next build`, allowing you to use it anywhere in your code. It will be inlined into any JavaScript sent to the browser.

> **Note**: After being built, your app will no longer respond to changes to these environment variables. For instance, if you use a Heroku pipeline to promote slugs built in one environment to another environment, or if you build and deploy a single Docker image to multiple environments, all `NEXT_PUBLIC_` variables will be frozen with the value evaluated at build time, so these values need to be set appropriately when the project is built. If you need access to runtime environment values, you'll have to setup your own API to provide them to the client (either on demand or during initialization).

 pages/index.js

```
import setupAnalyticsService from '../lib/my-analytics-service'

// 'NEXT_PUBLIC_ANALYTICS_ID' can be used here as it's prefixed by 'NEXT_PUBLIC_'.
// It will be transformed at build time to `setupAnalyticsService('abcdefghijk')`.
setupAnalyticsService(process.env.NEXT_PUBLIC_ANALYTICS_ID)

function HomePage() {
  return <h1>Hello World</h1>
}

export default HomePage
```

Note that dynamic lookups will *not* be inlined, such as:

```
// This will NOT be inlined, because it uses a variable
const varName = 'NEXT_PUBLIC_ANALYTICS_ID'
setupAnalyticsService(process.env[varName])

// This will NOT be inlined, because it uses a variable
const env = process.env
setupAnalyticsService(env.NEXT_PUBLIC_ANALYTICS_ID)
```

### Runtime Environment Variables

Next.js can support both build time and runtime environment variables.

**By default, environment variables are only available on the server**. To expose an environment variable to the browser, it must be prefixed with `NEXT_PUBLIC_`. However, these public environment variables will be inlined into the JavaScript bundle during `next build`.

To read runtime environment variables, we recommend using `getServerSideProps` or [incrementally adopting the App Router](https://nextjs.org/docs/app/guides/migrating/app-router-migration).

This allows you to use a singular Docker image that can be promoted through multiple environments with different values.

**Good to know:**

- You can run code on server startup using the [registerfunction](https://nextjs.org/docs/app/guides/instrumentation).

## Test Environment Variables

Apart from `development` and `production` environments, there is a 3rd option available: `test`. In the same way you can set defaults for development or production environments, you can do the same with a `.env.test` file for the `testing` environment (though this one is not as common as the previous two). Next.js will not load environment variables from `.env.development` or `.env.production` in the `testing` environment.

This one is useful when running tests with tools like `jest` or `cypress` where you need to set specific environment vars only for testing purposes. Test default values will be loaded if `NODE_ENV` is set to `test`, though you usually don't need to do this manually as testing tools will address it for you.

There is a small difference between `test` environment, and both `development` and `production` that you need to bear in mind: `.env.local` won't be loaded, as you expect tests to produce the same results for everyone. This way every test execution will use the same env defaults across different executions by ignoring your `.env.local` (which is intended to override the default set).

> **Good to know**: similar to Default Environment Variables, `.env.test` file should be included in your repository, but `.env.test.local` shouldn't, as `.env*.local` are intended to be ignored through `.gitignore`.

While running unit tests you can make sure to load your environment variables the same way Next.js does by leveraging the `loadEnvConfig` function from the `@next/env` package.

```
// The below can be used in a Jest global setup file or similar for your testing set-up
import { loadEnvConfig } from '@next/env'

export default async () => {
  const projectDir = process.cwd()
  loadEnvConfig(projectDir)
}
```

## Environment Variable Load Order

Environment variables are looked up in the following places, in order, stopping once the variable is found.

1. `process.env`
2. `.env.$(NODE_ENV).local`
3. `.env.local` (Not checked when `NODE_ENV` is `test`.)
4. `.env.$(NODE_ENV)`
5. `.env`

For example, if `NODE_ENV` is `development` and you define a variable in both `.env.development.local` and `.env`, the value in `.env.development.local` will be used.

> **Good to know**: The allowed values for `NODE_ENV` are `production`, `development` and `test`.

## Good to know

- If you are using a [/srcdirectory](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder), `.env.*` files should remain in the root of your project.
- If the environment variable `NODE_ENV` is unassigned, Next.js automatically assigns `development` when running the `next dev` command, or `production` for all other commands.

## Version History

| Version | Changes |
| --- | --- |
| v9.4.0 | Support.envandNEXT_PUBLIC_introduced. |

Was this helpful?

supported.

---

# How to create forms with API Routes

> Learn how to handle form submissions and data mutations with Next.js.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)FormsYou are currently viewing the documentation for Pages Router.

# How to create forms with API Routes

Last updated  July 30, 2025

Forms enable you to create and update data in web applications. Next.js provides a powerful way to handle data mutations using **API Routes**. This guide will walk you through how to handle form submission on the server.

## Server Forms

To handle form submissions on the server, create an API endpoint that securely mutates data.

 pages/api/submit.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const data = req.body
  const id = await createItem(data)
  res.status(200).json({ id })
}
```

Then, call the API Route from the client with an event handler:

 pages/index.tsxJavaScriptTypeScript

```
import { FormEvent } from 'react'

export default function Page() {
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const formData = new FormData(event.currentTarget)
    const response = await fetch('/api/submit', {
      method: 'POST',
      body: formData,
    })

    // Handle response if necessary
    const data = await response.json()
    // ...
  }

  return (
    <form onSubmit={onSubmit}>
      <input type="text" name="name" />
      <button type="submit">Submit</button>
    </form>
  )
}
```

> **Good to know:**
>
>
>
> - API Routes [do not specify CORS headers](https://developer.mozilla.org/docs/Web/HTTP/CORS), meaning they are same-origin only by default.
> - Since API Routes run on the server, we're able to use sensitive values (like API keys) through [Environment Variables](https://nextjs.org/docs/pages/guides/environment-variables) without exposing them to the client. This is critical for the security of your application.

## Form validation

We recommend using HTML validation like `required` and `type="email"` for basic client-side form validation.

For more advanced server-side validation, you can use a schema validation library like [zod](https://zod.dev/) to validate the form fields before mutating the data:

 pages/api/submit.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'
import { z } from 'zod'

const schema = z.object({
  // ...
})

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const parsed = schema.parse(req.body)
  // ...
}
```

### Error handling

You can use React state to show an error message when a form submission fails:

 pages/index.tsxJavaScriptTypeScript

```
import React, { useState, FormEvent } from 'react'

export default function Page() {
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError(null) // Clear previous errors when a new request starts

    try {
      const formData = new FormData(event.currentTarget)
      const response = await fetch('/api/submit', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to submit the data. Please try again.')
      }

      // Handle response if necessary
      const data = await response.json()
      // ...
    } catch (error) {
      // Capture the error message to display to the user
      setError(error.message)
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <form onSubmit={onSubmit}>
        <input type="text" name="name" />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Loading...' : 'Submit'}
        </button>
      </form>
    </div>
  )
}
```

## Displaying loading state

You can use React state to show a loading state when a form is submitting on the server:

 pages/index.tsxJavaScriptTypeScript

```
import React, { useState, FormEvent } from 'react'

export default function Page() {
  const [isLoading, setIsLoading] = useState<boolean>(false)

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true) // Set loading to true when the request starts

    try {
      const formData = new FormData(event.currentTarget)
      const response = await fetch('/api/submit', {
        method: 'POST',
        body: formData,
      })

      // Handle response if necessary
      const data = await response.json()
      // ...
    } catch (error) {
      // Handle error if necessary
      console.error(error)
    } finally {
      setIsLoading(false) // Set loading to false when the request completes
    }
  }

  return (
    <form onSubmit={onSubmit}>
      <input type="text" name="name" />
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Submit'}
      </button>
    </form>
  )
}
```

### Redirecting

If you would like to redirect the user to a different route after a mutation, you can [redirect](https://nextjs.org/docs/pages/building-your-application/routing/api-routes#response-helpers) to any absolute or relative URL:

 pages/api/submit.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const id = await addPost()
  res.redirect(307, `/post/${id}`)
}
```

Was this helpful?

supported.

---

# How to implement Incremental Static Regeneration (ISR)

> Learn how to create or update static pages at runtime with Incremental Static Regeneration.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)ISRYou are currently viewing the documentation for Pages Router.

# How to implement Incremental Static Regeneration (ISR)

Last updated  May 21, 2025Examples

- [Next.js Commerce](https://vercel.com/templates/next.js/nextjs-commerce)
- [On-Demand ISR](https://on-demand-isr.vercel.app)
- [Next.js Forms](https://github.com/vercel/next.js/tree/canary/examples/next-forms)

Incremental Static Regeneration (ISR) enables you to:

- Update static content without rebuilding the entire site
- Reduce server load by serving prerendered, static pages for most requests
- Ensure proper `cache-control` headers are automatically added to pages
- Handle large amounts of content pages without long `next build` times

Here's a minimal example:

   pages/blog/[id].tsxJavaScriptTypeScript

```
import type { GetStaticPaths, GetStaticProps } from 'next'

interface Post {
  id: string
  title: string
  content: string
}

interface Props {
  post: Post
}

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await fetch('https://api.vercel.app/blog').then((res) =>
    res.json()
  )
  const paths = posts.map((post: Post) => ({
    params: { id: String(post.id) },
  }))

  return { paths, fallback: 'blocking' }
}

export const getStaticProps: GetStaticProps<Props> = async ({
  params,
}: {
  params: { id: string }
}) => {
  const post = await fetch(`https://api.vercel.app/blog/${params.id}`).then(
    (res) => res.json()
  )

  return {
    props: { post },
    // Next.js will invalidate the cache when a
    // request comes in, at most once every 60 seconds.
    revalidate: 60,
  }
}

export default function Page({ post }: Props) {
  return (
    <main>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </main>
  )
}
```

Here's how this example works:

1. During `next build`, all known blog posts are generated
2. All requests made to these pages (e.g. `/blog/1`) are cached and instantaneous
3. After 60 seconds has passed, the next request will still return the cached (now stale) page
4. The cache is invalidated and a new version of the page begins generating in the background
5. Once generated successfully, the next request will return the updated page and cache it for subsequent requests
6. If `/blog/26` is requested, and it exists, the page will be generated on-demand. This behavior can be changed by using a different [fallback](https://nextjs.org/docs/pages/api-reference/functions/get-static-paths#fallback-false) value. However, if the post does not exist, then 404 is returned.

## Reference

### Functions

- [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props)
- [res.revalidate](https://nextjs.org/docs/pages/building-your-application/routing/api-routes#response-helpers)

## Examples

### On-demand validation withres.revalidate()

For a more precise method of revalidation, use `res.revalidate` to generate a new page on-demand from an API Router.

For example, this API Route can be called at `/api/revalidate?secret=<token>` to revalidate a given blog post. Create a secret token only known by your Next.js app. This secret will be used to prevent unauthorized access to the revalidation API Route.

pages/api/revalidate.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Check for secret to confirm this is a valid request
  if (req.query.secret !== process.env.MY_SECRET_TOKEN) {
    return res.status(401).json({ message: 'Invalid token' })
  }

  try {
    // This should be the actual path not a rewritten path
    // e.g. for "/posts/[id]" this should be "/posts/1"
    await res.revalidate('/posts/1')
    return res.json({ revalidated: true })
  } catch (err) {
    // If there was an error, Next.js will continue
    // to show the last successfully generated page
    return res.status(500).send('Error revalidating')
  }
}
```

If you are using on-demand revalidation, you do not need to specify a `revalidate` time inside of `getStaticProps`. Next.js will use the default value of `false` (no revalidation) and only revalidate the page on-demand when `res.revalidate()` is called.

### Handling uncaught exceptions

If there is an error inside `getStaticProps` when handling background regeneration, or you manually throw an error, the last successfully generated page will continue to show. On the next subsequent request, Next.js will retry calling `getStaticProps`.

pages/blog/[id].tsxJavaScriptTypeScript

```
import type { GetStaticProps } from 'next'

interface Post {
  id: string
  title: string
  content: string
}

interface Props {
  post: Post
}

export const getStaticProps: GetStaticProps<Props> = async ({
  params,
}: {
  params: { id: string }
}) => {
  // If this request throws an uncaught error, Next.js will
  // not invalidate the currently shown page and
  // retry getStaticProps on the next request.
  const res = await fetch(`https://api.vercel.app/blog/${params.id}`)
  const post: Post = await res.json()

  if (!res.ok) {
    // If there is a server error, you might want to
    // throw an error instead of returning so that the cache is not updated
    // until the next successful request.
    throw new Error(`Failed to fetch posts, received status ${res.status}`)
  }

  return {
    props: { post },
    // Next.js will invalidate the cache when a
    // request comes in, at most once every 60 seconds.
    revalidate: 60,
  }
}
```

### Customizing the cache location

You can configure the Next.js cache location if you want to persist cached pages and data to durable storage, or share the cache across multiple containers or instances of your Next.js application. [Learn more](https://nextjs.org/docs/app/guides/self-hosting#caching-and-isr).

## Troubleshooting

### Debugging cached data in local development

If you are using the `fetch` API, you can add additional logging to understand which requests are cached or uncached. [Learn more about theloggingoption](https://nextjs.org/docs/app/api-reference/config/next-config-js/logging).

 next.config.js

```
module.exports = {
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
}
```

### Verifying correct production behavior

To verify your pages are cached and revalidated correctly in production, you can test locally by running `next build` and then `next start` to run the production Next.js server.

This will allow you to test ISR behavior as it would work in a production environment. For further debugging, add the following environment variable to your `.env` file:

 .env

```
NEXT_PRIVATE_DEBUG_CACHE=1
```

This will make the Next.js server console log ISR cache hits and misses. You can inspect the output to see which pages are generated during `next build`, as well as how pages are updated as paths are accessed on-demand.

## Caveats

- ISR is only supported when using the Node.js runtime (default).
- ISR is not supported when creating a [Static Export](https://nextjs.org/docs/app/guides/static-exports).
- Proxy won't be executed for on-demand ISR requests, meaning any path rewrites or logic in Proxy will not be applied. Ensure you are revalidating the exact path. For example, `/post/1` instead of a rewritten `/post-1`.

## Platform Support

| Deployment Option | Supported |
| --- | --- |
| Node.js server | Yes |
| Docker container | Yes |
| Static export | No |
| Adapters | Platform-specific |

Learn how to [configure ISR](https://nextjs.org/docs/app/guides/self-hosting#caching-and-isr) when self-hosting Next.js.

## Version history

| Version | Changes |
| --- | --- |
| v14.1.0 | CustomcacheHandleris stable. |
| v13.0.0 | App Router is introduced. |
| v12.2.0 | Pages Router: On-Demand ISR is stable |
| v12.0.0 | Pages Router:Bot-aware ISR fallbackadded. |
| v9.5.0 | Pages Router:Stable ISR introduced. |

Was this helpful?

supported.

---

# How to set up instrumentation

> Learn how to use instrumentation to run code at server startup in your Next.js app

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)InstrumentationYou are currently viewing the documentation for Pages Router.

# How to set up instrumentation

Last updated  April 24, 2025

Instrumentation is the process of using code to integrate monitoring and logging tools into your application. This allows you to track the performance and behavior of your application, and to debug issues in production.

## Convention

To set up instrumentation, create `instrumentation.ts|js` file in the **root directory** of your project (or inside the [src](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder) folder if using one).

Then, export a `register` function in the file. This function will be called **once** when a new Next.js server instance is initiated.

For example, to use Next.js with [OpenTelemetry](https://opentelemetry.io/) and [@vercel/otel](https://vercel.com/docs/observability/otel-overview):

 instrumentation.tsJavaScriptTypeScript

```
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel('next-app')
}
```

See the [Next.js with OpenTelemetry example](https://github.com/vercel/next.js/tree/canary/examples/with-opentelemetry) for a complete implementation.

> **Good to know**:
>
>
>
> - The `instrumentation` file should be in the root of your project and not inside the `app` or `pages` directory. If you're using the `src` folder, then place the file inside `src` alongside `pages` and `app`.
> - If you use the [pageExtensionsconfig option](https://nextjs.org/docs/app/api-reference/config/next-config-js/pageExtensions) to add a suffix, you will also need to update the `instrumentation` filename to match.

## Examples

### Importing files with side effects

Sometimes, it may be useful to import a file in your code because of the side effects it will cause. For example, you might import a file that defines a set of global variables, but never explicitly use the imported file in your code. You would still have access to the global variables the package has declared.

We recommend importing files using JavaScript `import` syntax within your `register` function. The following example demonstrates a basic usage of `import` in a `register` function:

 instrumentation.tsJavaScriptTypeScript

```
export async function register() {
  await import('package-with-side-effect')
}
```

> **Good to know:**
>
>
>
> We recommend importing the file from within the `register` function, rather than at the top of the file. By doing this, you can colocate all of your side effects in one place in your code, and avoid any unintended consequences from importing globally at the top of the file.

### Importing runtime-specific code

Next.js calls `register` in all environments, so it's important to conditionally import any code that doesn't support specific runtimes (e.g. [Edge or Node.js](https://nextjs.org/docs/app/api-reference/edge)). You can use the `NEXT_RUNTIME` environment variable to get the current environment:

 instrumentation.tsJavaScriptTypeScript

```
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation-node')
  }

  if (process.env.NEXT_RUNTIME === 'edge') {
    await import('./instrumentation-edge')
  }
}
```

Was this helpful?

supported.
