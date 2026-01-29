# How to implement authentication in Next.js and more

# How to implement authentication in Next.js

> Learn how to implement authentication in Next.js, covering best practices, securing routes, authorization techniques, and session management.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)AuthenticationYou are currently viewing the documentation for Pages Router.

# How to implement authentication in Next.js

Last updated  April 22, 2025

Understanding authentication is crucial for protecting your application's data. This page will guide you through what React and Next.js features to use to implement auth.

Before starting, it helps to break down the process into three concepts:

1. **Authentication**: Verifies if the user is who they say they are. It requires the user to prove their identity with something they have, such as a username and password.
2. **Session Management**: Tracks the user's auth state across requests.
3. **Authorization**: Decides what routes and data the user can access.

This diagram shows the authentication flow using React and Next.js features:

 ![Diagram showing the authentication flow with React and Next.js features](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fauthentication-overview.png&w=3840&q=75)![Diagram showing the authentication flow with React and Next.js features](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fauthentication-overview.png&w=3840&q=75)

The examples on this page walk through basic username and password auth for educational purposes. While you can implement a custom auth solution, for increased security and simplicity, we recommend using an authentication library. These offer built-in solutions for authentication, session management, and authorization, as well as additional features such as social logins, multi-factor authentication, and role-based access control. You can find a list in the [Auth Libraries](#auth-libraries) section.

## Authentication

Here are the steps to implement a sign-up and/or login form:

1. The user submits their credentials through a form.
2. The form sends a request that is handled by an API route.
3. Upon successful verification, the process is completed, indicating the user's successful authentication.
4. If verification is unsuccessful, an error message is shown.

Consider a login form where users can input their credentials:

pages/login.tsxJavaScriptTypeScript

```
import { FormEvent } from 'react'
import { useRouter } from 'next/router'

export default function LoginPage() {
  const router = useRouter()

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const formData = new FormData(event.currentTarget)
    const email = formData.get('email')
    const password = formData.get('password')

    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })

    if (response.ok) {
      router.push('/profile')
    } else {
      // Handle errors
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" name="email" placeholder="Email" required />
      <input type="password" name="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  )
}
```

The form above has two input fields for capturing the user's email and password. On submission, it triggers a function that sends a POST request to an API route (`/api/auth/login`).

You can then call your Authentication Provider's API in the API route to handle authentication:

pages/api/auth/login.tsJavaScriptTypeScript

```
import type { NextApiRequest, NextApiResponse } from 'next'
import { signIn } from '@/auth'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const { email, password } = req.body
    await signIn('credentials', { email, password })

    res.status(200).json({ success: true })
  } catch (error) {
    if (error.type === 'CredentialsSignin') {
      res.status(401).json({ error: 'Invalid credentials.' })
    } else {
      res.status(500).json({ error: 'Something went wrong.' })
    }
  }
}
```

## Session Management

Session management ensures that the user's authenticated state is preserved across requests. It involves creating, storing, refreshing, and deleting sessions or tokens.

There are two types of sessions:

1. [Stateless](#stateless-sessions): Session data (or a token) is stored in the browser's cookies. The cookie is sent with each request, allowing the session to be verified on the server. This method is simpler, but can be less secure if not implemented correctly.
2. [Database](#database-sessions): Session data is stored in a database, with the user's browser only receiving the encrypted session ID. This method is more secure, but can be complex and use more server resources.

> **Good to know:** While you can use either method, or both, we recommend using a session management library such as [iron-session](https://github.com/vvo/iron-session) or [Jose](https://github.com/panva/jose).

### Stateless Sessions

#### Setting and deleting cookies

You can use [API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes) to set the session as a cookie on the server:

pages/api/login.tsJavaScriptTypeScript

```
import { serialize } from 'cookie'
import type { NextApiRequest, NextApiResponse } from 'next'
import { encrypt } from '@/app/lib/session'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const sessionData = req.body
  const encryptedSessionData = encrypt(sessionData)

  const cookie = serialize('session', encryptedSessionData, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    maxAge: 60 * 60 * 24 * 7, // One week
    path: '/',
  })
  res.setHeader('Set-Cookie', cookie)
  res.status(200).json({ message: 'Successfully set cookie!' })
}
```

### Database Sessions

To create and manage database sessions, you'll need to follow these steps:

1. Create a table in your database to store session and data (or check if your Auth Library handles this).
2. Implement functionality to insert, update, and delete sessions
3. Encrypt the session ID before storing it in the user's browser, and ensure the database and cookie stay in sync (this is optional, but recommended for optimistic auth checks in [Proxy](#optimistic-checks-with-proxy-optional)).

**Creating a Session on the Server**:

pages/api/create-session.tsJavaScriptTypeScript

```
import db from '../../lib/db'
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const user = req.body
    const sessionId = generateSessionId()
    await db.insertSession({
      sessionId,
      userId: user.id,
      createdAt: new Date(),
    })

    res.status(200).json({ sessionId })
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' })
  }
}
```

## Authorization

Once a user is authenticated and a session is created, you can implement authorization to control what the user can access and do within your application.

There are two main types of authorization checks:

1. **Optimistic**: Checks if the user is authorized to access a route or perform an action using the session data stored in the cookie. These checks are useful for quick operations, such as showing/hiding UI elements or redirecting users based on permissions or roles.
2. **Secure**: Checks if the user is authorized to access a route or perform an action using the session data stored in the database. These checks are more secure and are used for operations that require access to sensitive data or actions.

For both cases, we recommend:

- Creating a [Data Access Layer](#creating-a-data-access-layer-dal) to centralize your authorization logic
- Using [Data Transfer Objects (DTO)](#using-data-transfer-objects-dto) to only return the necessary data
- Optionally use [Proxy](#optimistic-checks-with-proxy-optional) to perform optimistic checks.

### Optimistic checks with Proxy (Optional)

There are some cases where you may want to use [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) and redirect users based on permissions:

- To perform optimistic checks. Since Proxy runs on every route, it's a good way to centralize redirect logic and pre-filter unauthorized users.
- To protect static routes that share data between users (e.g. content behind a paywall).

However, since Proxy runs on every route, including [prefetched](https://nextjs.org/docs/app/getting-started/linking-and-navigating#prefetching) routes, it's important to only read the session from the cookie (optimistic checks), and avoid database checks to prevent performance issues.

For example:

 proxy.tsJavaScriptTypeScript

```
import { NextRequest, NextResponse } from 'next/server'
import { decrypt } from '@/app/lib/session'
import { cookies } from 'next/headers'

// 1. Specify protected and public routes
const protectedRoutes = ['/dashboard']
const publicRoutes = ['/login', '/signup', '/']

export default async function proxy(req: NextRequest) {
  // 2. Check if the current route is protected or public
  const path = req.nextUrl.pathname
  const isProtectedRoute = protectedRoutes.includes(path)
  const isPublicRoute = publicRoutes.includes(path)

  // 3. Decrypt the session from the cookie
  const cookie = (await cookies()).get('session')?.value
  const session = await decrypt(cookie)

  // 4. Redirect to /login if the user is not authenticated
  if (isProtectedRoute && !session?.userId) {
    return NextResponse.redirect(new URL('/login', req.nextUrl))
  }

  // 5. Redirect to /dashboard if the user is authenticated
  if (
    isPublicRoute &&
    session?.userId &&
    !req.nextUrl.pathname.startsWith('/dashboard')
  ) {
    return NextResponse.redirect(new URL('/dashboard', req.nextUrl))
  }

  return NextResponse.next()
}

// Routes Proxy should not run on
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}
```

While Proxy can be useful for initial checks, it should not be your only line of defense in protecting your data. The majority of security checks should be performed as close as possible to your data source, see [Data Access Layer](#creating-a-data-access-layer-dal) for more information.

> **Tips**:
>
>
>
> - In Proxy, you can also read cookies using `req.cookies.get('session').value`.
> - Proxy uses the Node.js runtime, check if your Auth library and session management library are compatible. You may need to use [Middleware](https://github.com/vercel/next.js/blob/v15.5.6/docs/01-app/03-api-reference/03-file-conventions/middleware.mdx) if your Auth library only supports [Edge Runtime](https://nextjs.org/docs/app/api-reference/edge)
> - You can use the `matcher` property in the Proxy to specify which routes Proxy should run on. Although, for auth, it's recommended Proxy runs on all routes.

### Creating a Data Access Layer (DAL)

#### Protecting API Routes

API Routes in Next.js are essential for handling server-side logic and data management. It's crucial to secure these routes to ensure that only authorized users can access specific functionalities. This typically involves verifying the user's authentication status and their role-based permissions.

Here's an example of securing an API Route:

pages/api/route.tsJavaScriptTypeScript

```
import { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const session = await getSession(req)

  // Check if the user is authenticated
  if (!session) {
    res.status(401).json({
      error: 'User is not authenticated',
    })
    return
  }

  // Check if the user has the 'admin' role
  if (session.user.role !== 'admin') {
    res.status(401).json({
      error: 'Unauthorized access: User does not have admin privileges.',
    })
    return
  }

  // Proceed with the route for authorized users
  // ... implementation of the API Route
}
```

This example demonstrates an API Route with a two-tier security check for authentication and authorization. It first checks for an active session, and then verifies if the logged-in user is an 'admin'. This approach ensures secure access, limited to authenticated and authorized users, maintaining robust security for request processing.

## Resources

Now that you've learned about authentication in Next.js, here are Next.js-compatible libraries and resources to help you implement secure authentication and session management:

### Auth Libraries

- [Auth0](https://auth0.com/docs/quickstart/webapp/nextjs)
- [Better Auth](https://www.better-auth.com/docs/integrations/next)
- [Clerk](https://clerk.com/docs/quickstarts/nextjs)
- [Descope](https://docs.descope.com/getting-started/nextjs)
- [Kinde](https://kinde.com/docs/developer-tools/nextjs-sdk)
- [Logto](https://docs.logto.io/quick-starts/next-app-router)
- [NextAuth.js](https://authjs.dev/getting-started/installation?framework=next.js)
- [Ory](https://www.ory.sh/docs/getting-started/integrate-auth/nextjs)
- [Stack Auth](https://docs.stack-auth.com/getting-started/setup)
- [Supabase](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs)
- [Stytch](https://stytch.com/docs/guides/quickstarts/nextjs)
- [WorkOS](https://workos.com/docs/user-management/nextjs)

### Session Management Libraries

- [Iron Session](https://github.com/vvo/iron-session)
- [Jose](https://github.com/panva/jose)

## Further Reading

To continue learning about authentication and security, check out the following resources:

- [How to think about security in Next.js](https://nextjs.org/blog/security-nextjs-server-components-actions)
- [Understanding XSS Attacks](https://vercel.com/guides/understanding-xss-attacks)
- [Understanding CSRF Attacks](https://vercel.com/guides/understanding-csrf-attacks)
- [The Copenhagen Book](https://thecopenhagenbook.com/)

Was this helpful?

supported.

---

# How to configure Babel in Next.js

> Extend the babel preset added by Next.js with your own configs.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)BabelYou are currently viewing the documentation for Pages Router.

# How to configure Babel in Next.js

Last updated  April 24, 2025Examples

- [Customizing babel configuration](https://github.com/vercel/next.js/tree/canary/examples/with-custom-babel-config)

Next.js includes the `next/babel` preset to your app, which includes everything needed to compile React applications and server-side code. But if you want to extend the default Babel configs, it's also possible.

## Adding Presets and Plugins

To start, you only need to define a `.babelrc` file (or `babel.config.js`) in the root directory of your project. If such a file is found, it will be considered as the *source of truth*, and therefore it needs to define what Next.js needs as well, which is the `next/babel` preset.

Here's an example `.babelrc` file:

 .babelrc

```
{
  "presets": ["next/babel"],
  "plugins": []
}
```

You can [take a look at this file](https://github.com/vercel/next.js/blob/canary/packages/next/src/build/babel/preset.ts) to learn about the presets included by `next/babel`.

To add presets/plugins **without configuring them**, you can do it this way:

 .babelrc

```
{
  "presets": ["next/babel"],
  "plugins": ["@babel/plugin-proposal-do-expressions"]
}
```

## Customizing Presets and Plugins

To add presets/plugins **with custom configuration**, do it on the `next/babel` preset like so:

 .babelrc

```
{
  "presets": [
    [
      "next/babel",
      {
        "preset-env": {},
        "transform-runtime": {},
        "styled-jsx": {},
        "class-properties": {}
      }
    ]
  ],
  "plugins": []
}
```

To learn more about the available options for each config, visit babel's [documentation](https://babeljs.io/docs/) site.

> **Good to know**:
>
>
>
> - Next.js uses the [currentNode.js version](https://github.com/nodejs/release#release-schedule) for server-side compilations.
> - The `modules` option on `"preset-env"` should be kept to `false`, otherwise webpack code splitting is turned off.

Was this helpful?

supported.

---

# How to configure Continuous Integration (CI) build caching

> Learn how to configure CI to cache Next.js builds

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)CI Build CachingYou are currently viewing the documentation for Pages Router.

# How to configure Continuous Integration (CI) build caching

Last updated  April 22, 2025

To improve build performance, Next.js saves a cache to `.next/cache` that is shared between builds.

To take advantage of this cache in Continuous Integration (CI) environments, your CI workflow will need to be configured to correctly persist the cache between builds.

> If your CI is not configured to persist `.next/cache` between builds, you may see a [No Cache Detected](https://nextjs.org/docs/messages/no-cache) error.

Here are some example cache configurations for common CI providers:

## Vercel

Next.js caching is automatically configured for you. There's no action required on your part. If you are using Turborepo on Vercel, [learn more here](https://vercel.com/docs/monorepos/turborepo).

## CircleCI

Edit your `save_cache` step in `.circleci/config.yml` to include `.next/cache`:

```
steps:
  - save_cache:
      key: dependency-cache-{{ checksum "yarn.lock" }}
      paths:
        - ./node_modules
        - ./.next/cache
```

If you do not have a `save_cache` key, please follow CircleCI's [documentation on setting up build caching](https://circleci.com/docs/2.0/caching/).

## Travis CI

Add or merge the following into your `.travis.yml`:

```
cache:
  directories:
    - $HOME/.cache/yarn
    - node_modules
    - .next/cache
```

## GitLab CI

Add or merge the following into your `.gitlab-ci.yml`:

```
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .next/cache/
```

## Netlify CI

Use [Netlify Plugins](https://www.netlify.com/products/build/plugins/) with [@netlify/plugin-nextjs](https://www.npmjs.com/package/@netlify/plugin-nextjs).

## AWS CodeBuild

Add (or merge in) the following to your `buildspec.yml`:

```
cache:
  paths:
    - 'node_modules/**/*' # Cache `node_modules` for faster `yarn` or `npm i`
    - '.next/cache/**/*' # Cache Next.js for faster application rebuilds
```

## GitHub Actions

Using GitHub's [actions/cache](https://github.com/actions/cache), add the following step in your workflow file:

```
uses: actions/cache@v4
with:
  # See here for caching with `yarn`, `bun` or other package managers https://github.com/actions/cache/blob/main/examples.md or you can leverage caching with actions/setup-node https://github.com/actions/setup-node
  path: |
    ~/.npm
    ${{ github.workspace }}/.next/cache
  # Generate a new cache whenever packages or source files change.
  key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx') }}
  # If source files changed but packages didn't, rebuild from a prior cache.
  restore-keys: |
    ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-
```

## Bitbucket Pipelines

Add or merge the following into your `bitbucket-pipelines.yml` at the top level (same level as `pipelines`):

```
definitions:
  caches:
    nextcache: .next/cache
```

Then reference it in the `caches` section of your pipeline's `step`:

```
- step:
    name: your_step_name
    caches:
      - node
      - nextcache
```

## Heroku

Using Heroku's [custom cache](https://devcenter.heroku.com/articles/nodejs-support#custom-caching), add a `cacheDirectories` array in your top-level package.json:

```
"cacheDirectories": [".next/cache"]
```

## Azure Pipelines

Using Azure Pipelines' [Cache task](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/utility/cache), add the following task to your pipeline yaml file somewhere prior to the task that executes `next build`:

```
- task: Cache@2
  displayName: 'Cache .next/cache'
  inputs:
    key: next | $(Agent.OS) | yarn.lock
    path: '$(System.DefaultWorkingDirectory)/.next/cache'
```

## Jenkins (Pipeline)

Using Jenkins' [Job Cacher](https://www.jenkins.io/doc/pipeline/steps/jobcacher/) plugin, add the following build step to your `Jenkinsfile` where you would normally run `next build` or `npm install`:

```
stage("Restore npm packages") {
    steps {
        // Writes lock-file to cache based on the GIT_COMMIT hash
        writeFile file: "next-lock.cache", text: "$GIT_COMMIT"

        cache(caches: [
            arbitraryFileCache(
                path: "node_modules",
                includes: "**/*",
                cacheValidityDecidingFile: "package-lock.json"
            )
        ]) {
            sh "npm install"
        }
    }
}
stage("Build") {
    steps {
        // Writes lock-file to cache based on the GIT_COMMIT hash
        writeFile file: "next-lock.cache", text: "$GIT_COMMIT"

        cache(caches: [
            arbitraryFileCache(
                path: ".next/cache",
                includes: "**/*",
                cacheValidityDecidingFile: "next-lock.cache"
            )
        ]) {
            // aka `next build`
            sh "npm run build"
        }
    }
}
```

Was this helpful?

supported.

---

# How to set a Content Security Policy (CSP) for your Next.js application

> Learn how to set a Content Security Policy (CSP) for your Next.js application.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Content Security PolicyYou are currently viewing the documentation for Pages Router.

# How to set a Content Security Policy (CSP) for your Next.js application

Last updated  April 24, 2025

[Content Security Policy (CSP)](https://developer.mozilla.org/docs/Web/HTTP/CSP) is important to guard your Next.js application against various security threats such as cross-site scripting (XSS), clickjacking, and other code injection attacks.

By using CSP, developers can specify which origins are permissible for content sources, scripts, stylesheets, images, fonts, objects, media (audio, video), iframes, and more.

 Examples

- [Strict CSP](https://github.com/vercel/next.js/tree/canary/examples/with-strict-csp)

## Nonces

A [nonce](https://developer.mozilla.org/docs/Web/HTML/Global_attributes/nonce) is a unique, random string of characters created for a one-time use. It is used in conjunction with CSP to selectively allow certain inline scripts or styles to execute, bypassing strict CSP directives.

### Why use a nonce?

CSP can block both inline and external scripts to prevent attacks. A nonce lets you safely allow specific scripts to run—only if they include the matching nonce value.

If an attacker wanted to load a script into your page, they'd need to guess the nonce value. That's why the nonce must be unpredictable and unique for every request.

### Adding a nonce with Proxy

[Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) enables you to add headers and generate nonces before the page renders.

Every time a page is viewed, a fresh nonce should be generated. This means that you **must usedynamic renderingto add nonces**.

For example:

 proxy.tsJavaScriptTypeScript

```
import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64')
  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic';
    style-src 'self' 'nonce-${nonce}';
    img-src 'self' blob: data:;
    font-src 'self';
    object-src 'none';
    base-uri 'self';
    form-action 'self';
    frame-ancestors 'none';
    upgrade-insecure-requests;
`
  // Replace newline characters and spaces
  const contentSecurityPolicyHeaderValue = cspHeader
    .replace(/\s{2,}/g, ' ')
    .trim()

  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-nonce', nonce)

  requestHeaders.set(
    'Content-Security-Policy',
    contentSecurityPolicyHeaderValue
  )

  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  })
  response.headers.set(
    'Content-Security-Policy',
    contentSecurityPolicyHeaderValue
  )

  return response
}
```

By default, Proxy runs on all requests. You can filter Proxy to run on specific paths using a [matcher](https://nextjs.org/docs/app/api-reference/file-conventions/proxy#matcher).

We recommend ignoring matching prefetches (from `next/link`) and static assets that don't need the CSP header.

 proxy.tsJavaScriptTypeScript

```
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    {
      source: '/((?!api|_next/static|_next/image|favicon.ico).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },
  ],
}
```

### How nonces work in Next.js

To use a nonce, your page must be **dynamically rendered**. This is because Next.js applies nonces during **server-side rendering**, based on the CSP header present in the request. Static pages are generated at build time, when no request or response headers exist—so no nonce can be injected.

Here’s how nonce support works in a dynamically rendered page:

1. **Proxy generates a nonce**: Your proxy creates a unique nonce for the request, adds it to your `Content-Security-Policy` header, and also sets it in a custom `x-nonce` header.
2. **Next.js extracts the nonce**: During rendering, Next.js parses the `Content-Security-Policy` header and extracts the nonce using the `'nonce-{value}'` pattern.
3. **Nonce is applied automatically**: Next.js attaches the nonce to:
  - Framework scripts (React, Next.js runtime)
  - Page-specific JavaScript bundles
  - Inline styles and scripts generated by Next.js
  - Any `<Script>` components using the `nonce` prop

Because of this automatic behavior, you don’t need to manually add a nonce to each tag.

### Forcing dynamic rendering

If you're using nonces, you may need to explicitly opt pages into dynamic rendering:

 app/page.tsxJavaScriptTypeScript

```
import { connection } from 'next/server'

export default async function Page() {
  // wait for an incoming request to render this page
  await connection()
  // Your page content
}
```

### Reading the nonce

You can provide the nonce to your page using
[getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props):

pages/index.tsxJavaScriptTypeScript

```
import Script from 'next/script'

import type { GetServerSideProps } from 'next'

export default function Page({ nonce }) {
  return (
    <Script
      src="https://www.googletagmanager.com/gtag/js"
      strategy="afterInteractive"
      nonce={nonce}
    />
  )
}

export const getServerSideProps: GetServerSideProps = async ({ req }) => {
  const nonce = req.headers['x-nonce']
  return { props: { nonce } }
}
```

You can also access the nonce in `_document.tsx` for Pages Router applications:

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

interface ExtendedDocumentProps extends DocumentInitialProps {
  nonce?: string
}

class MyDocument extends Document<ExtendedDocumentProps> {
  static async getInitialProps(
    ctx: DocumentContext
  ): Promise<ExtendedDocumentProps> {
    const initialProps = await Document.getInitialProps(ctx)
    const nonce = ctx.req?.headers?.['x-nonce'] as string | undefined

    return {
      ...initialProps,
      nonce,
    }
  }

  render() {
    const { nonce } = this.props

    return (
      <Html lang="en">
        <Head nonce={nonce} />
        <body>
          <Main />
          <NextScript nonce={nonce} />
        </body>
      </Html>
    )
  }
}

export default MyDocument
```

## Static vs Dynamic Rendering with CSP

Using nonces has important implications for how your Next.js application renders:

### Dynamic Rendering Requirement

When you use nonces in your CSP, **all pages must be dynamically rendered**. This means:

- Pages will build successfully but may encounter runtime errors if not properly configured for dynamic rendering
- Each request generates a fresh page with a new nonce
- Static optimization and Incremental Static Regeneration (ISR) are disabled
- Pages cannot be cached by CDNs without additional configuration
- **Partial Prerendering (PPR) is incompatible** with nonce-based CSP since static shell scripts won't have access to the nonce

### Performance Implications

The shift from static to dynamic rendering affects performance:

- **Slower initial page loads**: Pages must be generated on each request
- **Increased server load**: Every request requires server-side rendering
- **No CDN caching**: Dynamic pages cannot be cached at the edge by default
- **Higher hosting costs**: More server resources needed for dynamic rendering

### When to use nonces

Consider nonces when:

- You have strict security requirements that prohibit `'unsafe-inline'`
- Your application handles sensitive data
- You need to allow specific inline scripts while blocking others
- Compliance requirements mandate strict CSP

## Without Nonces

For applications that do not require nonces, you can set the CSP header directly in your [next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js) file:

 next.config.js

```
const isDev = process.env.NODE_ENV === 'development'

const cspHeader = `
    default-src 'self';
    script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ''};
    style-src 'self' 'unsafe-inline';
    img-src 'self' blob: data:;
    font-src 'self';
    object-src 'none';
    base-uri 'self';
    form-action 'self';
    frame-ancestors 'none';
    upgrade-insecure-requests;
`

module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: cspHeader.replace(/\n/g, ''),
          },
        ],
      },
    ]
  },
}
```

## Development vs Production Considerations

CSP implementation differs between development and production environments:

### Development Environment

In development, you will need to enable `'unsafe-eval'` to support APIs that provide additional debugging information:

 proxy.tsJavaScriptTypeScript

```
export function proxy(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64')
  const isDev = process.env.NODE_ENV === 'development'

  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic' ${isDev ? "'unsafe-eval'" : ''};
    style-src 'self' ${isDev ? "'unsafe-inline'" : `'nonce-${nonce}'`};
    img-src 'self' blob: data:;
    font-src 'self';
    object-src 'none';
    base-uri 'self';
    form-action 'self';
    frame-ancestors 'none';
    upgrade-insecure-requests;
`

  // Rest of proxy implementation
}
```

### Production Deployment

Common issues in production:

- **Nonce not applied**: Ensure your proxy runs on all necessary routes
- **Static assets blocked**: Verify your CSP allows Next.js static assets
- **Third-party scripts**: Add necessary domains to your CSP policy

## Troubleshooting

### Third-party Scripts

When using third-party scripts with CSP, ensure you add the necessary domains and pass the nonce:

pages/_app.tsxJavaScriptTypeScript

```
import type { AppProps } from 'next/app'
import Script from 'next/script'

export default function App({ Component, pageProps }: AppProps) {
  const nonce = pageProps.nonce

  return (
    <>
      <Component {...pageProps} />
      <Script
        src="https://www.googletagmanager.com/gtag/js"
        strategy="afterInteractive"
        nonce={nonce}
      />
    </>
  )
}
```

Update your CSP to allow third-party domains:

 proxy.tsJavaScriptTypeScript

```
const cspHeader = `
  default-src 'self';
  script-src 'self' 'nonce-${nonce}' 'strict-dynamic' https://www.googletagmanager.com;
  connect-src 'self' https://www.google-analytics.com;
  img-src 'self' data: https://www.google-analytics.com;
`
```

### Common CSP Violations

1. **Inline styles**: Use CSS-in-JS libraries that support nonces or move styles to external files
2. **Dynamic imports**: Ensure dynamic imports are allowed in your script-src policy
3. **WebAssembly**: Add `'wasm-unsafe-eval'` if using WebAssembly
4. **Service workers**: Add appropriate policies for service worker scripts

## Version History

| Version | Changes |
| --- | --- |
| v14.0.0 | Experimental SRI support added for hash-based CSP |
| v13.4.20 | Recommended for proper nonce handling and CSP header parsing. |

Was this helpful?

supported.

---

# How to use CSS

> Use CSS-in-JS libraries with Next.js

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)CSS-in-JSYou are currently viewing the documentation for Pages Router.

# How to use CSS-in-JS libraries

Last updated  April 25, 2025   Examples

- [Styled JSX](https://github.com/vercel/next.js/tree/canary/examples/with-styled-jsx)
- [Styled Components](https://github.com/vercel/next.js/tree/canary/examples/with-styled-components)
- [Emotion](https://github.com/vercel/next.js/tree/canary/examples/with-emotion)
- [Linaria](https://github.com/vercel/next.js/tree/canary/examples/with-linaria)
- [Styletron](https://github.com/vercel/next.js/tree/canary/examples/with-styletron)
- [Cxs](https://github.com/vercel/next.js/tree/canary/examples/with-cxs)
- [Fela](https://github.com/vercel/next.js/tree/canary/examples/with-fela)
- [Stitches](https://github.com/vercel/next.js/tree/canary/examples/with-stitches)

It's possible to use any existing CSS-in-JS solution. The simplest one is inline styles:

```
function HiThere() {
  return <p style={{ color: 'red' }}>hi there</p>
}

export default HiThere
```

We bundle [styled-jsx](https://github.com/vercel/styled-jsx) to provide support for isolated scoped CSS.
The aim is to support "shadow CSS" similar to Web Components, which unfortunately [do not support server-rendering and are JS-only](https://github.com/w3c/webcomponents/issues/71).

See the above examples for other popular CSS-in-JS solutions (like Styled Components).

A component using `styled-jsx` looks like this:

```
function HelloWorld() {
  return (
    <div>
      Hello world
      <p>scoped!</p>
      <style jsx>{`
        p {
          color: blue;
        }
        div {
          background: red;
        }
        @media (max-width: 600px) {
          div {
            background: blue;
          }
        }
      `}</style>
      <style global jsx>{`
        body {
          background: black;
        }
      `}</style>
    </div>
  )
}

export default HelloWorld
```

Please see the [styled-jsx documentation](https://github.com/vercel/styled-jsx) for more examples.

### Disabling JavaScript

Yes, if you disable JavaScript the CSS will still be loaded in the production build (`next start`). During development, we require JavaScript to be enabled to provide the best developer experience with [Fast Refresh](https://nextjs.org/blog/next-9-4#fast-refresh).

Was this helpful?

supported.

---

# How to set up a custom server in Next.js

> Start a Next.js app programmatically using a custom server.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)Custom ServerYou are currently viewing the documentation for Pages Router.

# How to set up a custom server in Next.js

Last updated  April 24, 2025

Next.js includes its own server with `next start` by default. If you have an existing backend, you can still use it with Next.js (this is not a custom server). A custom Next.js server allows you to programmatically start a server for custom patterns. The majority of the time, you will not need this approach. However, it's available if you need to eject.

> **Good to know**:
>
>
>
> - Before deciding to use a custom server, keep in mind that it should only be used when the integrated router of Next.js can't meet your app requirements. A custom server will remove important performance optimizations, like **Automatic Static Optimization.**
> - When using standalone output mode, it does not trace custom server files. This mode outputs a separate minimal `server.js` file, instead. These cannot be used together.

Take a look at the [following example](https://github.com/vercel/next.js/tree/canary/examples/custom-server) of a custom server:

 server.tsJavaScriptTypeScript

```
import { createServer } from 'http'
import { parse } from 'url'
import next from 'next'

const port = parseInt(process.env.PORT || '3000', 10)
const dev = process.env.NODE_ENV !== 'production'
const app = next({ dev })
const handle = app.getRequestHandler()

app.prepare().then(() => {
  createServer((req, res) => {
    handle(req, res)
  }).listen(port)
})

  console.log(
    `> Server listening at http://localhost:${port} as ${
      dev ? 'development' : process.env.NODE_ENV
    }`
  )
})
```

> `server.js` does not run through the Next.js Compiler or bundling process. Make sure the syntax and source code this file requires are compatible with the current Node.js version you are using. [View an example](https://github.com/vercel/next.js/tree/canary/examples/custom-server).

To run the custom server, you'll need to update the `scripts` in `package.json` like so:

 package.json

```
{
  "scripts": {
    "dev": "node server.js",
    "build": "next build",
    "start": "NODE_ENV=production node server.js"
  }
}
```

Alternatively, you can set up `nodemon` ([example](https://github.com/vercel/next.js/tree/canary/examples/custom-server)). The custom server uses the following import to connect the server with the Next.js application:

```
import next from 'next'

const app = next({})
```

The above `next` import is a function that receives an object with the following options:

| Option | Type | Description |
| --- | --- | --- |
| conf | Object | The same object you would use innext.config.js. Defaults to{} |
| dev | Boolean | (Optional) Whether or not to launch Next.js in dev mode. Defaults tofalse |
| dir | String | (Optional) Location of the Next.js project. Defaults to'.' |
| quiet | Boolean | (Optional) Hide error messages containing server information. Defaults tofalse |
| hostname | String | (Optional) The hostname the server is running behind |
| port | Number | (Optional) The port the server is running behind |
| httpServer | node:http#Server | (Optional) The HTTP Server that Next.js is running behind |
| turbopack | Boolean | (Optional) Enable Turbopack (enabled by default) |
| webpack | Boolean | (Optional) Enable webpack |

The returned `app` can then be used to let Next.js handle requests as required.

## Disabling file-system routing

By default, `Next` will serve each file in the `pages` folder under a pathname matching the filename. If your project uses a custom server, this behavior may result in the same content being served from multiple paths, which can present problems with SEO and UX.

To disable this behavior and prevent routing based on files in `pages`, open `next.config.js` and disable the `useFileSystemPublicRoutes` config:

next.config.js

```
module.exports = {
  useFileSystemPublicRoutes: false,
}
```

> Note that `useFileSystemPublicRoutes` disables filename routes from SSR; client-side routing may still access those paths. When using this option, you should guard against navigation to routes you do not want programmatically.

> You may also wish to configure the client-side router to disallow client-side redirects to filename routes; for that refer to [router.beforePopState](https://nextjs.org/docs/pages/api-reference/functions/use-router#routerbeforepopstate).

Was this helpful?

supported.

---

# How to use debugging tools with Next.js

> Learn how to debug your Next.js application with VS Code or Chrome DevTools.

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)DebuggingYou are currently viewing the documentation for Pages Router.

# How to use debugging tools with Next.js

Last updated  April 24, 2025

This documentation explains how you can debug your Next.js frontend and backend code with full source maps support using the [VS Code debugger](https://code.visualstudio.com/docs/editor/debugging), [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools), or [Firefox DevTools](https://firefox-source-docs.mozilla.org/devtools-user/).

Any debugger that can attach to Node.js can also be used to debug a Next.js application. You can find more details in the Node.js [Debugging Guide](https://nodejs.org/en/docs/guides/debugging-getting-started/).

## Debugging with VS Code

Create a file named `.vscode/launch.json` at the root of your project with the following content:

 launch.json

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev -- --inspect"
    },
    {
      "name": "Next.js: debug client-side",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    },
    {
      "name": "Next.js: debug client-side (Firefox)",
      "type": "firefox",
      "request": "launch",
      "url": "http://localhost:3000",
      "reAttach": true,
      "pathMappings": [
        {
          "url": "webpack://_N_E",
          "path": "${workspaceFolder}"
        }
      ]
    },
    {
      "name": "Next.js: debug full stack",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/next/dist/bin/next",
      "runtimeArgs": ["--inspect"],
      "skipFiles": ["<node_internals>/**"],
      "serverReadyAction": {
        "action": "debugWithEdge",
        "killOnServerStop": true,
        "pattern": "- Local:.+(https?://.+)",
        "uriFormat": "%s",
        "webRoot": "${workspaceFolder}"
      }
    }
  ]
}
```

> **Note**: To use Firefox debugging in VS Code, you'll need to install the [Firefox Debugger extension](https://marketplace.visualstudio.com/items?itemName=firefox-devtools.vscode-firefox-debug).

`npm run dev` can be replaced with `yarn dev` if you're using Yarn or `pnpm dev` if you're using pnpm.

In the "Next.js: debug full stack" configuration, `serverReadyAction.action` specifies which browser to open when the server is ready. `debugWithEdge` means to launch the Edge browser. If you are using Chrome, change this value to `debugWithChrome`.

If you're [changing the port number](https://nextjs.org/docs/pages/api-reference/cli/next#next-dev-options) your application starts on, replace the `3000` in `http://localhost:3000` with the port you're using instead.

If you're running Next.js from a directory other than root (for example, if you're using Turborepo) then you need to add `cwd` to the server-side and full stack debugging tasks. For example, `"cwd": "${workspaceFolder}/apps/web"`.

Now go to the Debug panel (`Ctrl+Shift+D` on Windows/Linux, `⇧+⌘+D` on macOS), select a launch configuration, then press `F5` or select **Debug: Start Debugging** from the Command Palette to start your debugging session.

## Using the Debugger in Jetbrains WebStorm

Click the drop down menu listing the runtime configuration, and click `Edit Configurations...`. Create a `JavaScript Debug` debug configuration with `http://localhost:3000` as the URL. Customize to your liking (e.g. Browser for debugging, store as project file), and click `OK`. Run this debug configuration, and the selected browser should automatically open. At this point, you should have 2 applications in debug mode: the NextJS node application, and the client/browser application.

## Debugging with Browser DevTools

### Client-side code

Start your development server as usual by running `next dev`, `npm run dev`, or `yarn dev`. Once the server starts, open `http://localhost:3000` (or your alternate URL) in your preferred browser.

For Chrome:

- Open Chrome's Developer Tools (`Ctrl+Shift+J` on Windows/Linux, `⌥+⌘+I` on macOS)
- Go to the **Sources** tab

For Firefox:

- Open Firefox's Developer Tools (`Ctrl+Shift+I` on Windows/Linux, `⌥+⌘+I` on macOS)
- Go to the **Debugger** tab

In either browser, any time your client-side code reaches a [debugger](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/debugger) statement, code execution will pause and that file will appear in the debug area. You can also search for files to set breakpoints manually:

- In Chrome: Press `Ctrl+P` on Windows/Linux or `⌘+P` on macOS
- In Firefox: Press `Ctrl+P` on Windows/Linux or `⌘+P` on macOS, or use the file tree in the left panel

Note that when searching, your source files will have paths starting with `webpack://_N_E/./`.

### React Developer Tools

For React-specific debugging, install the [React Developer Tools](https://react.dev/learn/react-developer-tools) browser extension. This essential tool helps you:

- Inspect React components
- Edit props and state
- Identify performance problems

### Server-side code

To debug server-side Next.js code with browser DevTools, you need to pass the `--inspect` flag:

 Terminal

```
next dev --inspect
```

The value of `--inspect` is passed to the underlying Node.js process. Check out the [--inspectdocs for advanced use cases](https://nodejs.org/api/cli.html#--inspecthostport).

> **Good to know**: Use `--inspect=0.0.0.0` to allow remote debugging access outside localhost, such as when running the app in a Docker container.

Launching the Next.js dev server with the `--inspect` flag will look something like this:

 Terminal

```
Debugger listening on ws://127.0.0.1:9229/0cf90313-350d-4466-a748-cd60f4e47c95
For help, see: https://nodejs.org/en/docs/inspector
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

For Chrome:

1. Open a new tab and visit `chrome://inspect`
2. Look for your Next.js application in the **Remote Target** section
3. Click **inspect** to open a separate DevTools window
4. Go to the **Sources** tab

For Firefox:

1. Open a new tab and visit `about:debugging`
2. Click **This Firefox** in the left sidebar
3. Under **Remote Targets**, find your Next.js application
4. Click **Inspect** to open the debugger
5. Go to the **Debugger** tab

Debugging server-side code works similarly to client-side debugging. When searching for files (`Ctrl+P`/`⌘+P`), your source files will have paths starting with `webpack://{application-name}/./` (where `{application-name}` will be replaced with the name of your application according to your `package.json` file).

To use `--inspect-brk` or `--inspect-wait`, you have to specify `NODE_OPTIONS` instead. e.g. `NODE_OPTIONS=--inspect-brk next dev`.

### Inspect Server Errors with Browser DevTools

When you encounter an error, inspecting the source code can help trace the root cause of errors.

Next.js will display a Node.js icon underneath the Next.js version indicator on the error overlay. By clicking that icon, the DevTools URL is copied to your clipboard. You can open a new browser tab with that URL to inspect the Next.js server process.

### Debugging on Windows

Ensure Windows Defender is disabled on your machine. This external service will check *every file read*, which has been reported to greatly increase Fast Refresh time with `next dev`. This is a known issue, not related to Next.js, but it does affect Next.js development.

## More information

To learn more about how to use a JavaScript debugger, take a look at the following documentation:

- [Node.js debugging in VS Code: Breakpoints](https://code.visualstudio.com/docs/nodejs/nodejs-debugging#_breakpoints)
- [Chrome DevTools: Debug JavaScript](https://developers.google.com/web/tools/chrome-devtools/javascript)
- [Firefox DevTools: Debugger](https://firefox-source-docs.mozilla.org/devtools-user/debugger/)

Was this helpful?

supported.
