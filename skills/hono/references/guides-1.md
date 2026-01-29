# Best Practices​ and more

# Best Practices​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Best Practices​

Hono is very flexible. You can write your app as you like. However, there are best practices that are better to follow.

## Don't make "Controllers" when possible​

When possible, you should not create "Ruby on Rails-like Controllers".

ts

```
// 🙁
// A RoR-like Controller
const booksList = (c: Context) => {
  return c.json('list books')
}

app.get('/books', booksList)
```

The issue is related to types. For example, the path parameter cannot be inferred in the Controller without writing complex generics.

ts

```
// 🙁
// A RoR-like Controller
const bookPermalink = (c: Context) => {
  const id = c.req.param('id') // Can't infer the path param
  return c.json(`get ${id}`)
}
```

Therefore, you don't need to create RoR-like controllers and should write handlers directly after path definitions.

ts

```
// 😃
app.get('/books/:id', (c) => {
  const id = c.req.param('id') // Can infer the path param
  return c.json(`get ${id}`)
})
```

## factory.createHandlers()inhono/factory​

If you still want to create a RoR-like Controller, use `factory.createHandlers()` in [hono/factory](https://hono.dev/docs/helpers/factory). If you use this, type inference will work correctly.

ts

```
import { createFactory } from 'hono/factory'
import { logger } from 'hono/logger'

// ...

// 😃
const factory = createFactory()

const middleware = factory.createMiddleware(async (c, next) => {
  c.set('foo', 'bar')
  await next()
})

const handlers = factory.createHandlers(logger(), middleware, (c) => {
  return c.json(c.var.foo)
})

app.get('/api', ...handlers)
```

## Building a larger application​

Use `app.route()` to build a larger application without creating "Ruby on Rails-like Controllers".

If your application has `/authors` and `/books` endpoints and you wish to separate files from `index.ts`, create `authors.ts` and `books.ts`.

ts

```
// authors.ts
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.json('list authors'))
app.post('/', (c) => c.json('create an author', 201))
app.get('/:id', (c) => c.json(`get ${c.req.param('id')}`))

export default app
```

ts

```
// books.ts
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.json('list books'))
app.post('/', (c) => c.json('create a book', 201))
app.get('/:id', (c) => c.json(`get ${c.req.param('id')}`))

export default app
```

Then, import them and mount on the paths `/authors` and `/books` with `app.route()`.

ts

```
// index.ts
import { Hono } from 'hono'
import authors from './authors'
import books from './books'

const app = new Hono()

// 😃
app.route('/authors', authors)
app.route('/books', books)

export default app
```

### If you want to use RPC features​

The code above works well for normal use cases. However, if you want to use the `RPC` feature, you can get the correct type by chaining as follows.

ts

```
// authors.ts
import { Hono } from 'hono'

const app = new Hono()
  .get('/', (c) => c.json('list authors'))
  .post('/', (c) => c.json('create an author', 201))
  .get('/:id', (c) => c.json(`get ${c.req.param('id')}`))

export default app
export type AppType = typeof app
```

If you pass the type of the `app` to `hc`, it will get the correct type.

ts

```
import type { AppType } from './authors'
import { hc } from 'hono/client'

// 😃
const client = hc<AppType>('http://localhost') // Typed correctly
```

For more detailed information, please see [the RPC page](https://hono.dev/docs/guides/rpc#using-rpc-with-larger-applications).

---

# Create

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Create-hono​

Command-line options supported by `create-hono` - the project initializer that runs when you run `npm create hono@latest`, `npx create-hono@latest`, or `pnpm create hono@latest`.

NOTE

**Why this page?** The installation / quick-start examples often show a minimal `npm create hono@latest my-app` command. `create-hono` supports several useful flags you can pass to automate and customize project creation (select templates, skip prompts, pick a package manager, use local cache, and more).

## Passing arguments:​

When you use `npm create` (or `npx`) arguments intended for the initializer script must be placed **after** `--`. Anything after `--` is forwarded to the initializer.

npmyarnpnpmbundenosh

```
# Forwarding arguments to create-hono (npm requires `--`)
npm create hono@latest my-app -- --template cloudflare-workers
```

sh

```
# "--template cloudflare-workers" selects the Cloudflare Workers template
yarn create hono my-app --template cloudflare-workers
```

sh

```
# "--template cloudflare-workers" selects the Cloudflare Workers template
pnpm create hono@latest my-app --template cloudflare-workers
```

sh

```
# "--template cloudflare-workers" selects the Cloudflare Workers template
bun create hono@latest my-app --template cloudflare-workers
```

sh

```
# "--template cloudflare-workers" selects the Cloudflare Workers template
deno init --npm hono@latest my-app --template cloudflare-workers
```

## Commonly used arguments​

| Argument | Description | Example |
| --- | --- | --- |
| --template <template> | Select a starter template and skip the interactive template prompt. Templates may include names likebun,cloudflare-workers,vercel, etc. | --template cloudflare-workers |
| --install | Automatically install dependencies after the template is created. | --install |
| --pm <packageManager> | Specify which package manager to run when installing dependencies. Common values:npm,pnpm,yarn. | --pm pnpm |
| --offline | Use the local cache/templates instead of fetching the latest remote templates. Useful for offline environments or deterministic local runs. | --offline |

NOTE

The exact set of templates and available options is maintained by the `create-hono` project. This docs page summarizes the most-used flags — see the linked repository below for the full, authoritative reference.

## Example flows​

### Minimal, interactive​

bash

```
npm create hono@latest my-app
```

This prompts you for template and options.

### Non-interactive, pick template and package manager​

bash

```
npm create hono@latest my-app -- --template vercel --pm npm --install
```

This creates `my-app` using the `vercel` template, installs dependencies using `npm`, and skips the interactive prompts.

### Use offline cache (no network)​

bash

```
pnpm create hono@latest my-app --template deno --offline
```

## Troubleshooting & tips​

- If an option appears not to be recognized, make sure you're forwarding it with `--` when using `npm create` / `npx` .
- To see the most current list of templates and flags, consult the `create-hono` repository or run the initializer locally and follow its help output.

## Links & references​

- `create-hono` repository : [create-hono](https://github.com/honojs/create-hono)

---

# Frequently Asked Questions​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Frequently Asked Questions​

This guide is a collection of frequently asked questions (FAQ) about Hono and how to resolve them.

## Is there an official Renovate config for Hono?​

The Hono teams does not currently maintain [Renovate](https://github.com/renovatebot/renovate) Configuration. Therefore, please use third-party renovate-config as follows.

In your `renovate.json` :

json

```
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "github>shinGangan/renovate-config-hono"
  ]
}
```

see [renovate-config-hono](https://github.com/shinGangan/renovate-config-hono) repository for more details.

---

# Helpers​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Helpers​

Helpers are available to assist in developing your application. Unlike middleware, they don't act as handlers, but rather provide useful functions.

For instance, here's how to use the [Cookie helper](https://hono.dev/docs/helpers/cookie):

ts

```
import { getCookie, setCookie } from 'hono/cookie'

const app = new Hono()

app.get('/cookie', (c) => {
  const yummyCookie = getCookie(c, 'yummy_cookie')
  // ...
  setCookie(c, 'delicious_cookie', 'macha')
  //
})
```

## Available Helpers​

- [Accepts](https://hono.dev/docs/helpers/accepts)
- [Adapter](https://hono.dev/docs/helpers/adapter)
- [Cookie](https://hono.dev/docs/helpers/cookie)
- [css](https://hono.dev/docs/helpers/css)
- [Dev](https://hono.dev/docs/helpers/dev)
- [Factory](https://hono.dev/docs/helpers/factory)
- [html](https://hono.dev/docs/helpers/html)
- [JWT](https://hono.dev/docs/helpers/jwt)
- [SSG](https://hono.dev/docs/helpers/ssg)
- [Streaming](https://hono.dev/docs/helpers/streaming)
- [Testing](https://hono.dev/docs/helpers/testing)
- [WebSocket](https://hono.dev/docs/helpers/websocket)

---

# Client Components​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Client Components​

`hono/jsx` supports not only server side but also client side. This means that it is possible to create an interactive UI that runs in the browser. We call it Client Components or `hono/jsx/dom`.

It is fast and very small. The counter program in `hono/jsx/dom` is only 2.8KB with Brotli compression. But, 47.8KB for React.

This section introduces Client Components-specific features.

## Counter example​

Here is an example of a simple counter, the same code works as in React.

tsx

```
import { useState } from 'hono/jsx'
import { render } from 'hono/jsx/dom'

function Counter() {
  const [count, setCount] = useState(0)
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}

function App() {
  return (
    <html>
      <body>
        <Counter />
      </body>
    </html>
  )
}

const root = document.getElementById('root')
render(<App />, root)
```

## render()​

You can use `render()` to insert JSX components within a specified HTML element.

tsx

```
render(<Component />, container)
```

You can see full example code here: [Counter example](https://github.com/honojs/examples/tree/main/hono-vite-jsx).

## Hooks compatible with React​

hono/jsx/dom has Hooks that are compatible or partially compatible with React. You can learn about these APIs by looking at [the React documentation](https://react.dev/reference/react/hooks).

- `useState()`
- `useEffect()`
- `useRef()`
- `useCallback()`
- `use()`
- `startTransition()`
- `useTransition()`
- `useDeferredValue()`
- `useMemo()`
- `useLayoutEffect()`
- `useReducer()`
- `useDebugValue()`
- `createElement()`
- `memo()`
- `isValidElement()`
- `useId()`
- `createRef()`
- `forwardRef()`
- `useImperativeHandle()`
- `useSyncExternalStore()`
- `useInsertionEffect()`
- `useFormStatus()`
- `useActionState()`
- `useOptimistic()`

## startViewTransition()family​

The `startViewTransition()` family contains original hooks and functions to handle [View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API) easily. The followings are examples of how to use them.

### 1. An easiest example​

You can write a transition using the `document.startViewTransition` shortly with the `startViewTransition()`.

tsx

```
import { useState, startViewTransition } from 'hono/jsx'
import { css, Style } from 'hono/css'

export default function App() {
  const [showLargeImage, setShowLargeImage] = useState(false)
  return (
    <>
      <Style />
      <button
        onClick={() =>
          startViewTransition(() =>
            setShowLargeImage((state) => !state)
          )
        }
      >
        Click!
      </button>
      <div>
        {!showLargeImage ? (
          <img src='https://hono.dev/images/logo.png' />
        ) : (
          <div
            class={css`
              background: url('https://hono.dev/images/logo-large.png');
              background-size: contain;
              background-repeat: no-repeat;
              background-position: center;
              width: 600px;
              height: 600px;
            `}
          ></div>
        )}
      </div>
    </>
  )
}
```

### 2. UsingviewTransition()withkeyframes()​

The `viewTransition()` function allows you to get the unique `view-transition-name`.

You can use it with the `keyframes()`, The `::view-transition-old()` is converted to `::view-transition-old(${uniqueName))`.

tsx

```
import { useState, startViewTransition } from 'hono/jsx'
import { viewTransition } from 'hono/jsx/dom/css'
import { css, keyframes, Style } from 'hono/css'

const rotate = keyframes`
  from {
    rotate: 0deg;
  }
  to {
    rotate: 360deg;
  }
`

export default function App() {
  const [showLargeImage, setShowLargeImage] = useState(false)
  const [transitionNameClass] = useState(() =>
    viewTransition(css`
      ::view-transition-old() {
        animation-name: ${rotate};
      }
      ::view-transition-new() {
        animation-name: ${rotate};
      }
    `)
  )
  return (
    <>
      <Style />
      <button
        onClick={() =>
          startViewTransition(() =>
            setShowLargeImage((state) => !state)
          )
        }
      >
        Click!
      </button>
      <div>
        {!showLargeImage ? (
          <img src='https://hono.dev/images/logo.png' />
        ) : (
          <div
            class={css`
              ${transitionNameClass}
              background: url('https://hono.dev/images/logo-large.png');
              background-size: contain;
              background-repeat: no-repeat;
              background-position: center;
              width: 600px;
              height: 600px;
            `}
          ></div>
        )}
      </div>
    </>
  )
}
```

### 3. UsinguseViewTransition​

If you want to change the style only during the animation. You can use `useViewTransition()`. This hook returns the `[boolean, (callback: () => void) => void]`, and they are the `isUpdating` flag and the `startViewTransition()` function.

When this hook is used, the Component is evaluated at the following two times.

- Inside the callback of a call to `startViewTransition()`.
- When [thefinishpromise becomes fulfilled](https://developer.mozilla.org/en-US/docs/Web/API/ViewTransition/finished)

tsx

```
import { useState, useViewTransition } from 'hono/jsx'
import { viewTransition } from 'hono/jsx/dom/css'
import { css, keyframes, Style } from 'hono/css'

const rotate = keyframes`
  from {
    rotate: 0deg;
  }
  to {
    rotate: 360deg;
  }
`

export default function App() {
  const [isUpdating, startViewTransition] = useViewTransition()
  const [showLargeImage, setShowLargeImage] = useState(false)
  const [transitionNameClass] = useState(() =>
    viewTransition(css`
      ::view-transition-old() {
        animation-name: ${rotate};
      }
      ::view-transition-new() {
        animation-name: ${rotate};
      }
    `)
  )
  return (
    <>
      <Style />
      <button
        onClick={() =>
          startViewTransition(() =>
            setShowLargeImage((state) => !state)
          )
        }
      >
        Click!
      </button>
      <div>
        {!showLargeImage ? (
          <img src='https://hono.dev/images/logo.png' />
        ) : (
          <div
            class={css`
              ${transitionNameClass}
              background: url('https://hono.dev/images/logo-large.png');
              background-size: contain;
              background-repeat: no-repeat;
              background-position: center;
              width: 600px;
              height: 600px;
              position: relative;
              ${isUpdating &&
              css`
                &:before {
                  content: 'Loading...';
                  position: absolute;
                  top: 50%;
                  left: 50%;
                }
              `}
            `}
          ></div>
        )}
      </div>
    </>
  )
}
```

## Thehono/jsx/domruntime​

There is a small JSX Runtime for Client Components. Using this will result in smaller bundled results than using `hono/jsx`. Specify `hono/jsx/dom` in `tsconfig.json`. For Deno, modify the deno.json.

json

```
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "hono/jsx/dom"
  }
}
```

Alternatively, you can specify `hono/jsx/dom` in the esbuild transform options in `vite.config.ts`.

ts

```
import { defineConfig } from 'vite'

export default defineConfig({
  esbuild: {
    jsxImportSource: 'hono/jsx/dom',
  },
})
```

---

# JSX​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# JSX​

You can write HTML with JSX syntax with `hono/jsx`.

Although `hono/jsx` works on the client, you will probably use it most often when rendering content on the server side. Here are some things related to JSX that are common to both server and client.

## Settings​

To use JSX, modify the `tsconfig.json`:

`tsconfig.json`:

json

```
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "hono/jsx"
  }
}
```

Alternatively, use the pragma directives:

ts

```
/** @jsx jsx */
/** @jsxImportSource hono/jsx */
```

For Deno, you have to modify the `deno.json` instead of the `tsconfig.json`:

json

```
{
  "compilerOptions": {
    "jsx": "precompile",
    "jsxImportSource": "@hono/hono/jsx"
  }
}
```

## Usage​

INFO

If you are coming straight from the [Quick Start](https://hono.dev/docs/#quick-start), the main file has a `.ts` extension - you need to change it to `.tsx` - otherwise you will not be able to run the application at all. You should additionally modify the `package.json` (or `deno.json` if you are using Deno) to reflect that change (e.g. instead of having `bun run --hot src/index.ts` in dev script, you should have `bun run --hot src/index.tsx`).

`index.tsx`:

tsx

```
import { Hono } from 'hono'
import type { FC } from 'hono/jsx'

const app = new Hono()

const Layout: FC = (props) => {
  return (
    <html>
      <body>{props.children}</body>
    </html>
  )
}

const Top: FC<{ messages: string[] }> = (props: {
  messages: string[]
}) => {
  return (
    <Layout>
      <h1>Hello Hono!</h1>
      <ul>
        {props.messages.map((message) => {
          return <li>{message}!!</li>
        })}
      </ul>
    </Layout>
  )
}

app.get('/', (c) => {
  const messages = ['Good Morning', 'Good Evening', 'Good Night']
  return c.html(<Top messages={messages} />)
})

export default app
```

## Metadata hoisting​

You can write document metadata tags such as `<title>`, `<link>`, and `<meta>` directly inside your components. These tags will be automatically hoisted to the `<head>` section of the document. This is especially useful when the `<head>` element is rendered far from the component that determines the appropriate metadata.

tsx

```
import { Hono } from 'hono'

const app = new Hono()

app.use('*', async (c, next) => {
  c.setRenderer((content) => {
    return c.html(
      <html>
        <head></head>
        <body>{content}</body>
      </html>
    )
  })
  await next()
})

app.get('/about', (c) => {
  return c.render(
    <>
      <title>About Page</title>
      <meta name='description' content='This is the about page.' />
      about page content
    </>
  )
})

export default app
```

INFO

When hoisting occurs, existing elements are not removed. Elements appearing later are added to the end. For example, if you have `<title>Default</title>` in your `<head>` and a component renders `<title>Page Title</title>`, both titles will appear in the head.

## Fragment​

Use Fragment to group multiple elements without adding extra nodes:

tsx

```
import { Fragment } from 'hono/jsx'

const List = () => (
  <Fragment>
    <p>first child</p>
    <p>second child</p>
    <p>third child</p>
  </Fragment>
)
```

Or you can write it with `<></>` if it set up properly.

tsx

```
const List = () => (
  <>
    <p>first child</p>
    <p>second child</p>
    <p>third child</p>
  </>
)
```

## PropsWithChildren​

You can use `PropsWithChildren` to correctly infer a child element in a function component.

tsx

```
import { PropsWithChildren } from 'hono/jsx'

type Post = {
  id: number
  title: string
}

function Component({ title, children }: PropsWithChildren<Post>) {
  return (
    <div>
      <h1>{title}</h1>
      {children}
    </div>
  )
}
```

## Inserting Raw HTML​

To directly insert HTML, use `dangerouslySetInnerHTML`:

tsx

```
app.get('/foo', (c) => {
  const inner = { __html: 'JSX &middot; SSR' }
  const Div = <div dangerouslySetInnerHTML={inner} />
})
```

## Memoization​

Optimize your components by memoizing computed strings using `memo`:

tsx

```
import { memo } from 'hono/jsx'

const Header = memo(() => <header>Welcome to Hono</header>)
const Footer = memo(() => <footer>Powered by Hono</footer>)
const Layout = (
  <div>
    <Header />
    <p>Hono is cool!</p>
    <Footer />
  </div>
)
```

## Context​

By using `useContext`, you can share data globally across any level of the Component tree without passing values through props.

tsx

```
import type { FC } from 'hono/jsx'
import { createContext, useContext } from 'hono/jsx'

const themes = {
  light: {
    color: '#000000',
    background: '#eeeeee',
  },
  dark: {
    color: '#ffffff',
    background: '#222222',
  },
}

const ThemeContext = createContext(themes.light)

const Button: FC = () => {
  const theme = useContext(ThemeContext)
  return <button style={theme}>Push!</button>
}

const Toolbar: FC = () => {
  return (
    <div>
      <Button />
    </div>
  )
}

// ...

app.get('/', (c) => {
  return c.html(
    <div>
      <ThemeContext.Provider value={themes.dark}>
        <Toolbar />
      </ThemeContext.Provider>
    </div>
  )
})
```

## Async Component​

`hono/jsx` supports an Async Component, so you can use `async`/`await` in your component. If you render it with `c.html()`, it will await automatically.

tsx

```
const AsyncComponent = async () => {
  await new Promise((r) => setTimeout(r, 1000)) // sleep 1s
  return <div>Done!</div>
}

app.get('/', (c) => {
  return c.html(
    <html>
      <body>
        <AsyncComponent />
      </body>
    </html>
  )
})
```

## SuspenseExperimental​

The React-like `Suspense` feature is available. If you wrap the async component with `Suspense`, the content in the fallback will be rendered first, and once the Promise is resolved, the awaited content will be displayed. You can use it with `renderToReadableStream()`.

tsx

```
import { renderToReadableStream, Suspense } from 'hono/jsx/streaming'

//...

app.get('/', (c) => {
  const stream = renderToReadableStream(
    <html>
      <body>
        <Suspense fallback={<div>loading...</div>}>
          <Component />
        </Suspense>
      </body>
    </html>
  )
  return c.body(stream, {
    headers: {
      'Content-Type': 'text/html; charset=UTF-8',
      'Transfer-Encoding': 'chunked',
    },
  })
})
```

## ErrorBoundaryExperimental​

You can catch errors in child components using `ErrorBoundary`.

In the example below, it will show the content specified in `fallback` if an error occurs.

tsx

```
function SyncComponent() {
  throw new Error('Error')
  return <div>Hello</div>
}

app.get('/sync', async (c) => {
  return c.html(
    <html>
      <body>
        <ErrorBoundary fallback={<div>Out of Service</div>}>
          <SyncComponent />
        </ErrorBoundary>
      </body>
    </html>
  )
})
```

`ErrorBoundary` can also be used with async components and `Suspense`.

tsx

```
async function AsyncComponent() {
  await new Promise((resolve) => setTimeout(resolve, 2000))
  throw new Error('Error')
  return <div>Hello</div>
}

app.get('/with-suspense', async (c) => {
  return c.html(
    <html>
      <body>
        <ErrorBoundary fallback={<div>Out of Service</div>}>
          <Suspense fallback={<div>Loading...</div>}>
            <AsyncComponent />
          </Suspense>
        </ErrorBoundary>
      </body>
    </html>
  )
})
```

## StreamingContextExperimental​

You can use `StreamingContext` to provide configuration for streaming components like `Suspense` and `ErrorBoundary`. This is useful for adding nonce values to script tags generated by these components for Content Security Policy (CSP).

tsx

```
import { Suspense, StreamingContext } from 'hono/jsx/streaming'

// ...

app.get('/', (c) => {
  const stream = renderToReadableStream(
    <html>
      <body>
        <StreamingContext
          value={{ scriptNonce: 'random-nonce-value' }}
        >
          <Suspense fallback={<div>Loading...</div>}>
            <AsyncComponent />
          </Suspense>
        </StreamingContext>
      </body>
    </html>
  )

  return c.body(stream, {
    headers: {
      'Content-Type': 'text/html; charset=UTF-8',
      'Transfer-Encoding': 'chunked',
      'Content-Security-Policy':
        "script-src 'nonce-random-nonce-value'",
    },
  })
})
```

The `scriptNonce` value will be automatically added to any `<script>` tags generated by `Suspense` and `ErrorBoundary` components.

## Integration with html Middleware​

Combine the JSX and html middlewares for powerful templating. For in-depth details, consult the [html middleware documentation](https://hono.dev/docs/helpers/html).

tsx

```
import { Hono } from 'hono'
import { html } from 'hono/html'

const app = new Hono()

interface SiteData {
  title: string
  children?: any
}

const Layout = (props: SiteData) =>
  html`<!doctype html>
    <html>
      <head>
        <title>${props.title}</title>
      </head>
      <body>
        ${props.children}
      </body>
    </html>`

const Content = (props: { siteData: SiteData; name: string }) => (
  <Layout {...props.siteData}>
    <h1>Hello {props.name}</h1>
  </Layout>
)

app.get('/:name', (c) => {
  const { name } = c.req.param()
  const props = {
    name: name,
    siteData: {
      title: 'JSX with html sample',
    },
  }
  return c.html(<Content {...props} />)
})

export default app
```

## With JSX Renderer Middleware​

The [JSX Renderer Middleware](https://hono.dev/docs/middleware/builtin/jsx-renderer) allows you to create HTML pages more easily with the JSX.

## Override type definitions​

You can override the type definition to add your custom elements and attributes.

ts

```
declare module 'hono/jsx' {
  namespace JSX {
    interface IntrinsicElements {
      'my-custom-element': HTMLAttributes & {
        'x-event'?: 'click' | 'scroll'
      }
    }
  }
}
```

---

# Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Middleware​

Middleware works before/after the endpoint `Handler`. We can get the `Request` before dispatching or manipulate the `Response` after dispatching.

## Definition of Middleware​

- Handler - should return `Response` object. Only one handler will be called.
- Middleware - should `await next()` and return nothing to call the next Middleware, **or** return a `Response` to early-exit.

The user can register middleware using `app.use` or using `app.HTTP_METHOD` as well as the handlers. For this feature, it's easy to specify the path and the method.

ts

```
// match any method, all routes
app.use(logger())

// specify path
app.use('/posts/*', cors())

// specify method and path
app.post('/posts/*', basicAuth())
```

If the handler returns `Response`, it will be used for the end-user, and stopping the processing.

ts

```
app.post('/posts', (c) => c.text('Created!', 201))
```

In this case, four middleware are processed before dispatching like this:

ts

```
logger() -> cors() -> basicAuth() -> *handler*
```

## Execution order​

The order in which Middleware is executed is determined by the order in which it is registered. The process before the `next` of the first registered Middleware is executed first, and the process after the `next` is executed last. See below.

ts

```
app.use(async (_, next) => {
  console.log('middleware 1 start')
  await next()
  console.log('middleware 1 end')
})
app.use(async (_, next) => {
  console.log('middleware 2 start')
  await next()
  console.log('middleware 2 end')
})
app.use(async (_, next) => {
  console.log('middleware 3 start')
  await next()
  console.log('middleware 3 end')
})

app.get('/', (c) => {
  console.log('handler')
  return c.text('Hello!')
})
```

Result is the following.

```
middleware 1 start
  middleware 2 start
    middleware 3 start
      handler
    middleware 3 end
  middleware 2 end
middleware 1 end
```

Note that if the handler or any middleware throws, hono will catch it and either pass it to [your app.onError() callback](https://hono.dev/docs/api/hono#error-handling) or automatically convert it to a 500 response before returning it up the chain of middleware. This means that next() will never throw, so there is no need to wrap it in a try/catch/finally.

## Built-in Middleware​

Hono has built-in middleware.

ts

```
import { Hono } from 'hono'
import { poweredBy } from 'hono/powered-by'
import { logger } from 'hono/logger'
import { basicAuth } from 'hono/basic-auth'

const app = new Hono()

app.use(poweredBy())
app.use(logger())

app.use(
  '/auth/*',
  basicAuth({
    username: 'hono',
    password: 'acoolproject',
  })
)
```

WARNING

In Deno, it is possible to use a different version of middleware than the Hono version, but this can lead to bugs. For example, this code is not working because the version is different.

ts

```
import { Hono } from 'jsr:@hono/hono@4.4.0'
import { upgradeWebSocket } from 'jsr:@hono/hono@4.4.5/deno'

const app = new Hono()

app.get(
  '/ws',
  upgradeWebSocket(() => ({
    // ...
  }))
)
```

## Custom Middleware​

You can write your own middleware directly inside `app.use()`:

ts

```
// Custom logger
app.use(async (c, next) => {
  console.log(`[${c.req.method}] ${c.req.url}`)
  await next()
})

// Add a custom header
app.use('/message/*', async (c, next) => {
  await next()
  c.header('x-message', 'This is middleware!')
})

app.get('/message/hello', (c) => c.text('Hello Middleware!'))
```

However, embedding middleware directly within `app.use()` can limit its reusability. Therefore, we can separate our middleware into different files.

To ensure we don't lose type definitions for `context` and `next`, when separating middleware, we can use [createMiddleware()](https://hono.dev/docs/helpers/factory#createmiddleware) from Hono's factory. This also allows us to type-safely [access data we'vesetinContext](https://hono.dev/docs/api/context#set-get) from downstream handlers.

ts

```
import { createMiddleware } from 'hono/factory'

const logger = createMiddleware(async (c, next) => {
  console.log(`[${c.req.method}] ${c.req.url}`)
  await next()
})
```

INFO

Type generics can be used with `createMiddleware`:

ts

```
createMiddleware<{Bindings: Bindings}>(async (c, next) =>
```

### Modify the Response After Next​

Additionally, middleware can be designed to modify responses if necessary:

ts

```
const stripRes = createMiddleware(async (c, next) => {
  await next()
  c.res = undefined
  c.res = new Response('New Response')
})
```

## Context access inside Middleware arguments​

To access the context inside middleware arguments, directly use the context parameter provided by `app.use`. See the example below for clarification.

ts

```
import { cors } from 'hono/cors'

app.use('*', async (c, next) => {
  const middleware = cors({
    origin: c.env.CORS_ORIGIN,
  })
  return middleware(c, next)
})
```

### Extending the Context in Middleware​

To extend the context inside middleware, use `c.set`. You can make this type-safe by passing a `{ Variables: { yourVariable: YourVariableType } }` generic argument to the `createMiddleware` function.

ts

```
import { createMiddleware } from 'hono/factory'

const echoMiddleware = createMiddleware<{
  Variables: {
    echo: (str: string) => string
  }
}>(async (c, next) => {
  c.set('echo', (str) => str)
  await next()
})

app.get('/echo', echoMiddleware, (c) => {
  return c.text(c.var.echo('Hello!'))
})
```

## Third-party Middleware​

Built-in middleware does not depend on external modules, but third-party middleware can depend on third-party libraries. So with them, we may make a more complex application.

We can explore a variety of [third-party middleware](https://hono.dev/docs/middleware/third-party). For example, we have GraphQL Server Middleware, Sentry Middleware, Firebase Auth Middleware, and others.

---

# Miscellaneous​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Miscellaneous​

## Contributing​

Contributions Welcome! You can contribute in the following ways.

- Create an Issue - Propose a new feature. Report a bug.
- Pull Request - Fix a bug and typo. Refactor the code.
- Create third-party middleware - Instruct below.
- Share - Share your thoughts on the Blog, X(Twitter), and others.
- Make your application - Please try to use Hono.

For more details, see [Contribution Guide](https://github.com/honojs/hono/blob/main/docs/CONTRIBUTING.md).

## Sponsoring​

You can sponsor Hono authors via the GitHub sponsor program.

- [Sponsor @yusukebe on GitHub Sponsors](https://github.com/sponsors/yusukebe)
- [Sponsor @usualoma on GitHub Sponsors](https://github.com/sponsors/usualoma)

## Other Resources​

- GitHub repository: [https://github.com/honojs](https://github.com/honojs)
- npm registry: [https://www.npmjs.com/package/hono](https://www.npmjs.com/package/hono)
- JSR: [https://jsr.io/@hono/hono](https://jsr.io/@hono/hono)
