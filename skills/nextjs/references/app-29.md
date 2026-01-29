# How to use debugging tools with Next.js and more

# How to use debugging tools with Next.js

> Learn how to debug your Next.js application with VS Code, Chrome DevTools, or Firefox DevTools.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Debugging

# How to use debugging tools with Next.js

Last updated  January 19, 2026

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

---

# How to preview content with Draft Mode in Next.js

> Next.js has draft mode to toggle between static and dynamic pages. You can learn how it works with App Router here.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Draft Mode

# How to preview content with Draft Mode in Next.js

Last updated  October 22, 2025

**Draft Mode** allows you to preview draft content from your headless CMS in your Next.js application. This is useful for static pages that are generated at build time as it allows you to switch to [dynamic rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering) and see the draft changes without having to rebuild your entire site.

This page walks through how to enable and use Draft Mode.

## Step 1: Create a Route Handler

Create a [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route). It can have any name, for example, `app/api/draft/route.ts`.

 app/api/draft/route.tsJavaScriptTypeScript

```
export async function GET(request: Request) {
  return new Response('')
}
```

Then, import the [draftMode](https://nextjs.org/docs/app/api-reference/functions/draft-mode) function and call the `enable()` method.

 app/api/draft/route.tsJavaScriptTypeScript

```
import { draftMode } from 'next/headers'

export async function GET(request: Request) {
  const draft = await draftMode()
  draft.enable()
  return new Response('Draft mode is enabled')
}
```

This will set a **cookie** to enable draft mode. Subsequent requests containing this cookie will trigger draft mode and change the behavior of statically generated pages.

You can test this manually by visiting `/api/draft` and looking at your browser’s developer tools. Notice the `Set-Cookie` response header with a cookie named `__prerender_bypass`.

## Step 2: Access the Route Handler from your Headless CMS

> These steps assume that the headless CMS you’re using supports setting **custom draft URLs**. If it doesn’t, you can still use this method to secure your draft URLs, but you’ll need to construct and access the draft URL manually. The specific steps will vary depending on which headless CMS you’re using.

To securely access the Route Handler from your headless CMS:

1. Create a **secret token string** using a token generator of your choice. This secret will only be known by your Next.js app and your headless CMS.
2. If your headless CMS supports setting custom draft URLs, specify a draft URL (this assumes that your Route Handler is located at `app/api/draft/route.ts`). For example:

 Terminal

```
https://<your-site>/api/draft?secret=<token>&slug=<path>
```

> - `<your-site>` should be your deployment domain.
> - `<token>` should be replaced with the secret token you generated.
> - `<path>` should be the path for the page that you want to view. If you want to view `/posts/one`, then you should use `&slug=/posts/one`.
>
>
>
> Your headless CMS might allow you to include a variable in the draft URL so that `<path>` can be set dynamically based on the CMS’s data like so: `&slug=/posts/{entry.fields.slug}`

1. In your Route Handler, check that the secret matches and that the `slug` parameter exists (if not, the request should fail), call `draftMode.enable()` to set the cookie. Then, redirect the browser to the path specified by `slug`:

 app/api/draft/route.tsJavaScriptTypeScript

```
import { draftMode } from 'next/headers'
import { redirect } from 'next/navigation'

export async function GET(request: Request) {
  // Parse query string parameters
  const { searchParams } = new URL(request.url)
  const secret = searchParams.get('secret')
  const slug = searchParams.get('slug')

  // Check the secret and next parameters
  // This secret should only be known to this Route Handler and the CMS
  if (secret !== 'MY_SECRET_TOKEN' || !slug) {
    return new Response('Invalid token', { status: 401 })
  }

  // Fetch the headless CMS to check if the provided `slug` exists
  // getPostBySlug would implement the required fetching logic to the headless CMS
  const post = await getPostBySlug(slug)

  // If the slug doesn't exist prevent draft mode from being enabled
  if (!post) {
    return new Response('Invalid slug', { status: 401 })
  }

  // Enable Draft Mode by setting the cookie
  const draft = await draftMode()
  draft.enable()

  // Redirect to the path from the fetched post
  // We don't redirect to searchParams.slug as that might lead to open redirect vulnerabilities
  redirect(post.slug)
}
```

If it succeeds, then the browser will be redirected to the path you want to view with the draft mode cookie.

## Step 3: Preview the Draft Content

The next step is to update your page to check the value of `draftMode().isEnabled`.

If you request a page which has the cookie set, then data will be fetched at **request time** (instead of at build time).

Furthermore, the value of `isEnabled` will be `true`.

 app/page.tsxJavaScriptTypeScript

```
// page that fetches data
import { draftMode } from 'next/headers'

async function getData() {
  const { isEnabled } = await draftMode()

  const url = isEnabled
    ? 'https://draft.example.com'
    : 'https://production.example.com'

  const res = await fetch(url)

  return res.json()
}

export default async function Page() {
  const { title, desc } = await getData()

  return (
    <main>
      <h1>{title}</h1>
      <p>{desc}</p>
    </main>
  )
}
```

If you access the draft Route Handler (with `secret` and `slug`) from your headless CMS or manually using the URL, you should now be able to see the draft content. And, if you update your draft without publishing, you should be able to view the draft.

## Next Steps

See the API reference for more information on how to use Draft Mode.[draftModeAPI Reference for the draftMode function.](https://nextjs.org/docs/app/api-reference/functions/draft-mode)

Was this helpful?

supported.

---

# How to use environment variables in Next.js

> Learn to add and access environment variables in your Next.js application.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Environment Variables

# How to use environment variables in Next.js

Last updated  October 8, 2025

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

> **Note**: Next.js also supports multiline variables inside of your `.env*` files:
>
>
>
> ```
> # .env
>
> # you can write with line breaks
> PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
> ...
> Kh9NV...
> ...
> -----END DSA PRIVATE KEY-----"
>
> # or with `\n` inside double quotes
> PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nKh9NV...\n-----END DSA PRIVATE KEY-----\n"
> ```

> **Note**: If you are using a `/src` folder, please note that Next.js will load the .env files **only** from the parent folder and **not** from the `/src` folder.
> This loads `process.env.DB_HOST`, `process.env.DB_USER`, and `process.env.DB_PASS` into the Node.js environment automatically allowing you to use them in [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route).

For example:

app/api/route.js

```
export async function GET() {
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

You can safely read environment variables on the server during dynamic rendering:

app/page.tsJavaScriptTypeScript

```
import { connection } from 'next/server'

export default async function Component() {
  await connection()
  // cookies, headers, and other Dynamic APIs
  // will also opt into dynamic rendering, meaning
  // this env variable is evaluated at runtime
  const value = process.env.MY_VALUE
  // ...
}
```

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

# How to create forms with Server Actions

> Learn how to create forms in Next.js with React Server Actions.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Forms

# How to create forms with Server Actions

Last updated  October 9, 2025

React Server Actions are [Server Functions](https://react.dev/reference/rsc/server-functions) that execute on the server. They can be called in Server and Client Components to handle form submissions. This guide will walk you through how to create forms in Next.js with Server Actions.

## How it works

React extends the HTML [<form>](https://developer.mozilla.org/docs/Web/HTML/Element/form) element to allow Server Actions to be invoked with the [action](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form#action) attribute.

When used in a form, the function automatically receives the [FormData](https://developer.mozilla.org/docs/Web/API/FormData/FormData) object. You can then extract the data using the native [FormDatamethods](https://developer.mozilla.org/en-US/docs/Web/API/FormData#instance_methods):

 app/invoices/page.tsxJavaScriptTypeScript

```
export default function Page() {
  async function createInvoice(formData: FormData) {
    'use server'

    const rawFormData = {
      customerId: formData.get('customerId'),
      amount: formData.get('amount'),
      status: formData.get('status'),
    }

    // mutate data
    // revalidate the cache
  }

  return <form action={createInvoice}>...</form>
}
```

> **Good to know:** When working with forms that have multiple fields, use JavaScript's [Object.fromEntries()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/fromEntries). For example: `const rawFormData = Object.fromEntries(formData)`. Note that this object will contain extra properties prefixed with `$ACTION_`.

## Passing additional arguments

Outside of form fields, you can pass additional arguments to a Server Function using the JavaScript [bind](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind) method. For example, to pass the `userId` argument to the `updateUser` Server Function:

 app/client-component.tsxJavaScriptTypeScript

```
'use client'

import { updateUser } from './actions'

export function UserProfile({ userId }: { userId: string }) {
  const updateUserWithId = updateUser.bind(null, userId)

  return (
    <form action={updateUserWithId}>
      <input type="text" name="name" />
      <button type="submit">Update User Name</button>
    </form>
  )
}
```

The Server Function will receive the `userId` as an additional argument:

 app/actions.tsJavaScriptTypeScript

```
'use server'

export async function updateUser(userId: string, formData: FormData) {}
```

> **Good to know**:
>
>
>
> - An alternative is to pass arguments as hidden input fields in the form (e.g. `<input type="hidden" name="userId" value={userId} />`). However, the value will be part of the rendered HTML and will not be encoded.
> - `bind` works in both Server and Client Components and supports progressive enhancement.

## Form validation

Forms can be validated on the client or server.

- For **client-side validation**, you can use the HTML attributes like `required` and `type="email"` for basic validation.
- For **server-side validation**, you can use a library like [zod](https://zod.dev/) to validate the form fields. For example:

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { z } from 'zod'

const schema = z.object({
  email: z.string({
    invalid_type_error: 'Invalid Email',
  }),
})

export default async function createUser(formData: FormData) {
  const validatedFields = schema.safeParse({
    email: formData.get('email'),
  })

  // Return early if the form data is invalid
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }

  // Mutate data
}
```

## Validation errors

To display validation errors or messages, turn the component that defines the `<form>` into a Client Component and use React [useActionState](https://react.dev/reference/react/useActionState).

When using `useActionState`, the Server function signature will change to receive a new `prevState` or `initialState` parameter as its first argument.

 app/actions.tsJavaScriptTypeScript

```
'use server'

import { z } from 'zod'

export async function createUser(initialState: any, formData: FormData) {
  const validatedFields = schema.safeParse({
    email: formData.get('email'),
  })
  // ...
}
```

You can then conditionally render the error message based on the `state` object.

 app/ui/signup.tsxJavaScriptTypeScript

```
'use client'

import { useActionState } from 'react'
import { createUser } from '@/app/actions'

const initialState = {
  message: '',
}

export function Signup() {
  const [state, formAction, pending] = useActionState(createUser, initialState)

  return (
    <form action={formAction}>
      <label htmlFor="email">Email</label>
      <input type="text" id="email" name="email" required />
      {/* ... */}
      <p aria-live="polite">{state?.message}</p>
      <button disabled={pending}>Sign up</button>
    </form>
  )
}
```

## Pending states

The [useActionState](https://react.dev/reference/react/useActionState) hook exposes a `pending` boolean that can be used to show a loading indicator or disable the submit button while the action is being executed.

 app/ui/signup.tsxJavaScriptTypeScript

```
'use client'

import { useActionState } from 'react'
import { createUser } from '@/app/actions'

export function Signup() {
  const [state, formAction, pending] = useActionState(createUser, initialState)

  return (
    <form action={formAction}>
      {/* Other form elements */}
      <button disabled={pending}>Sign up</button>
    </form>
  )
}
```

Alternatively, you can use the [useFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus) hook to show a loading indicator while the action is being executed. When using this hook, you'll need to create a separate component to render the loading indicator. For example, to disable the button when the action is pending:

 app/ui/button.tsxJavaScriptTypeScript

```
'use client'

import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button disabled={pending} type="submit">
      Sign Up
    </button>
  )
}
```

You can then nest the `SubmitButton` component inside the form:

 app/ui/signup.tsxJavaScriptTypeScript

```
import { SubmitButton } from './button'
import { createUser } from '@/app/actions'

export function Signup() {
  return (
    <form action={createUser}>
      {/* Other form elements */}
      <SubmitButton />
    </form>
  )
}
```

> **Good to know:** In React 19, `useFormStatus` includes additional keys on the returned object, like data, method, and action. If you are not using React 19, only the `pending` key is available.

## Optimistic updates

You can use the React [useOptimistic](https://react.dev/reference/react/useOptimistic) hook to optimistically update the UI before the Server Function finishes executing, rather than waiting for the response:

 app/page.tsxJavaScriptTypeScript

```
'use client'

import { useOptimistic } from 'react'
import { send } from './actions'

type Message = {
  message: string
}

export function Thread({ messages }: { messages: Message[] }) {
  const [optimisticMessages, addOptimisticMessage] = useOptimistic<
    Message[],
    string
  >(messages, (state, newMessage) => [...state, { message: newMessage }])

  const formAction = async (formData: FormData) => {
    const message = formData.get('message') as string
    addOptimisticMessage(message)
    await send(message)
  }

  return (
    <div>
      {optimisticMessages.map((m, i) => (
        <div key={i}>{m.message}</div>
      ))}
      <form action={formAction}>
        <input type="text" name="message" />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}
```

## Nested form elements

You can call Server Actions in elements nested inside `<form>` such as `<button>`, `<input type="submit">`, and `<input type="image">`. These elements accept the `formAction` prop or event handlers.

This is useful in cases where you want to call multiple Server Actions within a form. For example, you can create a specific `<button>` element for saving a post draft in addition to publishing it. See the [React<form>docs](https://react.dev/reference/react-dom/components/form#handling-multiple-submission-types) for more information.

## Programmatic form submission

You can trigger a form submission programmatically using the [requestSubmit()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/requestSubmit) method. For example, when the user submits a form using the `⌘` + `Enter` keyboard shortcut, you can listen for the `onKeyDown` event:

 app/entry.tsxJavaScriptTypeScript

```
'use client'

export function Entry() {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (
      (e.ctrlKey || e.metaKey) &&
      (e.key === 'Enter' || e.key === 'NumpadEnter')
    ) {
      e.preventDefault()
      e.currentTarget.form?.requestSubmit()
    }
  }

  return (
    <div>
      <textarea name="entry" rows={20} required onKeyDown={handleKeyDown} />
    </div>
  )
}
```

This will trigger the submission of the nearest `<form>` ancestor, which will invoke the Server Function.

Was this helpful?

supported.

---

# How to implement Incremental Static Regeneration (ISR)

> Learn how to create or update static pages at runtime with Incremental Static Regeneration.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)ISR

# How to implement Incremental Static Regeneration (ISR)

Last updated  October 22, 2025Examples

- [Next.js Commerce](https://vercel.com/templates/next.js/nextjs-commerce)
- [On-Demand ISR](https://on-demand-isr.vercel.app)
- [Next.js Forms](https://github.com/vercel/next.js/tree/canary/examples/next-forms)

Incremental Static Regeneration (ISR) enables you to:

- Update static content without rebuilding the entire site
- Reduce server load by serving prerendered, static pages for most requests
- Ensure proper `cache-control` headers are automatically added to pages
- Handle large amounts of content pages without long `next build` times

Here's a minimal example:

 app/blog/[id]/page.tsxJavaScriptTypeScript

```
interface Post {
  id: string
  title: string
  content: string
}

// Next.js will invalidate the cache when a
// request comes in, at most once every 60 seconds.
export const revalidate = 60

export async function generateStaticParams() {
  const posts: Post[] = await fetch('https://api.vercel.app/blog').then((res) =>
    res.json()
  )
  return posts.map((post) => ({
    id: String(post.id),
  }))
}

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const post: Post = await fetch(`https://api.vercel.app/blog/${id}`).then(
    (res) => res.json()
  )
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
6. If `/blog/26` is requested, and it exists, the page will be generated on-demand. This behavior can be changed by using a different [dynamicParams](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamicparams) value. However, if the post does not exist, then 404 is returned.

## Reference

### Route segment config

- [revalidate](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#revalidate)
- [dynamicParams](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamicparams)

### Functions

- [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)
- [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)

## Examples

### Time-based revalidation

This fetches and displays a list of blog posts on /blog. After an hour has passed, the next visitor will still receive the cached (stale) version of the page immediately for a fast response. Simultaneously, Next.js triggers regeneration of a fresh version in the background. Once the new version is successfully generated, it replaces the cached version, and subsequent visitors will receive the updated content.

app/blog/page.tsxJavaScriptTypeScript

```
interface Post {
  id: string
  title: string
  content: string
}

export const revalidate = 3600 // invalidate every hour

export default async function Page() {
  const data = await fetch('https://api.vercel.app/blog')
  const posts: Post[] = await data.json()
  return (
    <main>
      <h1>Blog Posts</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </main>
  )
}
```

We recommend setting a high revalidation time. For instance, 1 hour instead of 1 second. If you need more precision, consider using on-demand revalidation. If you need real-time data, consider switching to [dynamic rendering](https://nextjs.org/docs/app/guides/caching#dynamic-rendering).

### On-demand revalidation withrevalidatePath

For a more precise method of revalidation, invalidate cached pages on-demand with the `revalidatePath` function.

For example, this Server Action would get called after adding a new post. Regardless of how you retrieve your data in your Server Component, either using `fetch` or connecting to a database, this will invalidate the cache for the entire route. The next request to that route will trigger regeneration and serve fresh data, which will then be cached for subsequent requests.

> **Note:** `revalidatePath` invalidates the cache entries but regeneration happens on the next request. If you want to eagerly regenerate the cache entry immediately instead of waiting for the next request, you can use the Pages router [res.revalidate](https://nextjs.org/docs/app/guides/docs/pages/guides/incremental-static-regeneration#on-demand-validation-with-resrevalidate) method. We're working on adding new methods to provide eager regeneration capabilities for the App Router.

app/actions.tsJavaScriptTypeScript

```
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost() {
  // Invalidate the cache for the /posts route
  revalidatePath('/posts')
}
```

[View a demo](https://on-demand-isr.vercel.app) and [explore the source code](https://github.com/vercel/on-demand-isr).

### On-demand revalidation withrevalidateTag

For most use cases, prefer revalidating entire paths. If you need more granular control, you can use the `revalidateTag` function. For example, you can tag individual `fetch` calls:

app/blog/page.tsxJavaScriptTypeScript

```
export default async function Page() {
  const data = await fetch('https://api.vercel.app/blog', {
    next: { tags: ['posts'] },
  })
  const posts = await data.json()
  // ...
}
```

If you are using an ORM or connecting to a database, you can use `unstable_cache`:

app/blog/page.tsxJavaScriptTypeScript

```
import { unstable_cache } from 'next/cache'
import { db, posts } from '@/lib/db'

const getCachedPosts = unstable_cache(
  async () => {
    return await db.select().from(posts)
  },
  ['posts'],
  { revalidate: 3600, tags: ['posts'] }
)

export default async function Page() {
  const posts = getCachedPosts()
  // ...
}
```

You can then use `revalidateTag` in a [Server Actions](https://nextjs.org/docs/app/getting-started/updating-data) or [Route Handler](https://nextjs.org/docs/app/api-reference/file-conventions/route):

app/actions.tsJavaScriptTypeScript

```
'use server'

import { revalidateTag } from 'next/cache'

export async function createPost() {
  // Invalidate all data tagged with 'posts'
  revalidateTag('posts')
}
```

### Handling uncaught exceptions

If an error is thrown while attempting to revalidate data, the last successfully generated data will continue to be served from the cache. On the next subsequent request, Next.js will retry revalidating the data. [Learn more about error handling](https://nextjs.org/docs/app/getting-started/error-handling).

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
- If you have multiple `fetch` requests in a statically rendered route, and each has a different `revalidate` frequency, the lowest time will be used for ISR. However, those revalidate frequencies will still be respected by the [Data Cache](https://nextjs.org/docs/app/guides/caching#data-cache).
- If any of the `fetch` requests used on a route have a `revalidate` time of `0`, or an explicit `no-store`, the route will be [dynamically rendered](https://nextjs.org/docs/app/guides/caching#dynamic-rendering).
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

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Instrumentation

# How to set up instrumentation

Last updated  May 14, 2025

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

## Learn more about Instrumentation

[instrumentation.jsAPI reference for the instrumentation.js file.](https://nextjs.org/docs/app/api-reference/file-conventions/instrumentation)

Was this helpful?

supported.
