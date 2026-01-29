# Accepts Helper​ and more

# Accepts Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Accepts Helper​

Accepts Helper helps to handle Accept headers in the Requests.

## Import​

ts

```
import { Hono } from 'hono'
import { accepts } from 'hono/accepts'
```

## accepts()​

The `accepts()` function looks at the Accept header, such as Accept-Encoding and Accept-Language, and returns the proper value.

ts

```
import { accepts } from 'hono/accepts'

app.get('/', (c) => {
  const accept = accepts(c, {
    header: 'Accept-Language',
    supports: ['en', 'ja', 'zh'],
    default: 'en',
  })
  return c.json({ lang: accept })
})
```

### AcceptHeadertype​

The definition of the `AcceptHeader` type is as follows.

ts

```
export type AcceptHeader =
  | 'Accept'
  | 'Accept-Charset'
  | 'Accept-Encoding'
  | 'Accept-Language'
  | 'Accept-Patch'
  | 'Accept-Post'
  | 'Accept-Ranges'
```

## Options​

### requiredheader:AcceptHeader​

The target accept header.

### requiredsupports:string[]​

The header values which your application supports.

### requireddefault:string​

The default values.

### optionalmatch:(accepts: Accept[], config: acceptsConfig) => string​

The custom match function.

---

# Adapter Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Adapter Helper​

The Adapter Helper provides a seamless way to interact with various platforms through a unified interface.

## Import​

ts

```
import { Hono } from 'hono'
import { env, getRuntimeKey } from 'hono/adapter'
```

## env()​

The `env()` function facilitates retrieving environment variables across different runtimes, extending beyond just Cloudflare Workers' Bindings. The value that can be retrieved with `env(c)` may be different for each runtimes.

ts

```
import { env } from 'hono/adapter'

app.get('/env', (c) => {
  // NAME is process.env.NAME on Node.js or Bun
  // NAME is the value written in `wrangler.toml` on Cloudflare
  const { NAME } = env<{ NAME: string }>(c)
  return c.text(NAME)
})
```

Supported Runtimes, Serverless Platforms and Cloud Services:

- Cloudflare Workers
  - `wrangler.toml`
  - `wrangler.jsonc`
- Deno
  - [Deno.env](https://docs.deno.com/runtime/manual/basics/env_variables)
  - `.env` file
- Bun
  - [Bun.env](https://bun.com/guides/runtime/set-env)
  - `process.env`
- Node.js
  - `process.env`
- Vercel
  - [Environment Variables on Vercel](https://vercel.com/docs/projects/environment-variables)
- AWS Lambda
  - [Environment Variables on AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/samples-blank.html#samples-blank-architecture)
- Lambda@Edge
   Environment Variables on Lambda are [not supported](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/add-origin-custom-headers.html) by Lambda@Edge, you need to use [Lamdba@Edge event](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-event-structure.html) as an alternative.
- Fastly Compute
   On Fastly Compute, you can use the ConfigStore to manage user-defined data.
- Netlify
   On Netlify, you can use the [Netlify Contexts](https://docs.netlify.com/site-deploys/overview/#deploy-contexts) to manage user-defined data.

### Specify the runtime​

You can specify the runtime to get environment variables by passing the runtime key as the second argument.

ts

```
app.get('/env', (c) => {
  const { NAME } = env<{ NAME: string }>(c, 'workerd')
  return c.text(NAME)
})
```

## getRuntimeKey()​

The `getRuntimeKey()` function returns the identifier of the current runtime.

ts

```
app.get('/', (c) => {
  if (getRuntimeKey() === 'workerd') {
    return c.text('You are on Cloudflare')
  } else if (getRuntimeKey() === 'bun') {
    return c.text('You are on Bun')
  }
  ...
})
```

### Available Runtimes Keys​

Here are the available runtimes keys, unavailable runtime key runtimes may be supported and labeled as `other`, with some being inspired by [WinterCG's Runtime Keys](https://runtime-keys.proposal.wintercg.org/):

- `workerd` - Cloudflare Workers
- `deno`
- `bun`
- `node`
- `edge-light` - Vercel Edge Functions
- `fastly` - Fastly Compute
- `other` - Other unknown runtimes keys

---

# ConnInfo Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# ConnInfo Helper​

The ConnInfo Helper helps you to get the connection information. For example, you can get the client's remote address easily.

## Import​

Cloudflare WorkersDenoBunVercelLambda@EdgeNode.jsts

```
import { Hono } from 'hono'
import { getConnInfo } from 'hono/cloudflare-workers'
```

ts

```
import { Hono } from 'hono'
import { getConnInfo } from 'hono/deno'
```

ts

```
import { Hono } from 'hono'
import { getConnInfo } from 'hono/bun'
```

ts

```
import { Hono } from 'hono'
import { getConnInfo } from 'hono/vercel'
```

ts

```
import { Hono } from 'hono'
import { getConnInfo } from 'hono/lambda-edge'
```

ts

```
import { Hono } from 'hono'
import { getConnInfo } from '@hono/node-server/conninfo'
```

## Usage​

ts

```
const app = new Hono()

app.get('/', (c) => {
  const info = getConnInfo(c) // info is `ConnInfo`
  return c.text(`Your remote address is ${info.remote.address}`)
})
```

## Type Definitions​

The type definitions of the values that you can get from `getConnInfo()` are the following:

ts

```
type AddressType = 'IPv6' | 'IPv4' | undefined

type NetAddrInfo = {
  /**
   * Transport protocol type
   */
  transport?: 'tcp' | 'udp'
  /**
   * Transport port number
   */
  port?: number

  address?: string
  addressType?: AddressType
} & (
  | {
      /**
       * Host name such as IP Addr
       */
      address: string

      /**
       * Host name type
       */
      addressType: AddressType
    }
  | {}
)

/**
 * HTTP Connection information
 */
interface ConnInfo {
  /**
   * Remote information
   */
  remote: NetAddrInfo
}
```

---

# Cookie Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Cookie Helper​

The Cookie Helper provides an easy interface to manage cookies, enabling developers to set, parse, and delete cookies seamlessly.

## Import​

ts

```
import { Hono } from 'hono'
import {
  deleteCookie,
  getCookie,
  getSignedCookie,
  setCookie,
  setSignedCookie,
  generateCookie,
  generateSignedCookie,
} from 'hono/cookie'
```

## Usage​

### Regular cookies​

ts

```
app.get('/cookie', (c) => {
  setCookie(c, 'cookie_name', 'cookie_value')
  const yummyCookie = getCookie(c, 'cookie_name')
  deleteCookie(c, 'cookie_name')
  const allCookies = getCookie(c)
  // ...
})
```

### Signed cookies​

**NOTE**: Setting and retrieving signed cookies returns a Promise due to the async nature of the WebCrypto API, which is used to create HMAC SHA-256 signatures.

ts

```
app.get('/signed-cookie', (c) => {
  const secret = 'secret' // make sure it's a large enough string to be secure

  await setSignedCookie(c, 'cookie_name0', 'cookie_value', secret)
  const fortuneCookie = await getSignedCookie(
    c,
    secret,
    'cookie_name0'
  )
  deleteCookie(c, 'cookie_name0')
  // `getSignedCookie` will return `false` for a specified cookie if the signature was tampered with or is invalid
  const allSignedCookies = await getSignedCookie(c, secret)
  // ...
})
```

### Cookie Generation​

`generateCookie` and `generateSignedCookie` functions allow you to create cookie strings directly without setting them in the response headers.

#### generateCookie​

ts

```
// Basic cookie generation
const cookie = generateCookie('delicious_cookie', 'macha')
// Returns: 'delicious_cookie=macha; Path=/'

// Cookie with options
const cookie = generateCookie('delicious_cookie', 'macha', {
  path: '/',
  secure: true,
  httpOnly: true,
  domain: 'example.com',
})
```

#### generateSignedCookie​

ts

```
// Basic signed cookie generation
const signedCookie = await generateSignedCookie(
  'delicious_cookie',
  'macha',
  'secret chocolate chips'
)

// Signed cookie with options
const signedCookie = await generateSignedCookie(
  'delicious_cookie',
  'macha',
  'secret chocolate chips',
  {
    path: '/',
    secure: true,
    httpOnly: true,
  }
)
```

**Note**: Unlike `setCookie` and `setSignedCookie`, these functions only generate the cookie strings. You need to manually set them in headers if needed.

## Options​

### setCookie&setSignedCookie​

- domain: `string`
- expires: `Date`
- httpOnly: `boolean`
- maxAge: `number`
- path: `string`
- secure: `boolean`
- sameSite: `'Strict'` | `'Lax'` | `'None'`
- priority: `'Low' | 'Medium' | 'High'`
- prefix: `secure` | `'host'`
- partitioned: `boolean`

Example:

ts

```
// Regular cookies
setCookie(c, 'great_cookie', 'banana', {
  path: '/',
  secure: true,
  domain: 'example.com',
  httpOnly: true,
  maxAge: 1000,
  expires: new Date(Date.UTC(2000, 11, 24, 10, 30, 59, 900)),
  sameSite: 'Strict',
})

// Signed cookies
await setSignedCookie(
  c,
  'fortune_cookie',
  'lots-of-money',
  'secret ingredient',
  {
    path: '/',
    secure: true,
    domain: 'example.com',
    httpOnly: true,
    maxAge: 1000,
    expires: new Date(Date.UTC(2000, 11, 24, 10, 30, 59, 900)),
    sameSite: 'Strict',
  }
)
```

### deleteCookie​

- path: `string`
- secure: `boolean`
- domain: `string`

Example:

ts

```
deleteCookie(c, 'banana', {
  path: '/',
  secure: true,
  domain: 'example.com',
})
```

`deleteCookie` returns the deleted value:

ts

```
const deletedCookie = deleteCookie(c, 'delicious_cookie')
```

## __Secure-and__Host-prefix​

The Cookie helper supports `__Secure-` and `__Host-` prefix for cookies names.

If you want to verify if the cookie name has a prefix, specify the prefix option.

ts

```
const securePrefixCookie = getCookie(c, 'yummy_cookie', 'secure')
const hostPrefixCookie = getCookie(c, 'yummy_cookie', 'host')

const securePrefixSignedCookie = await getSignedCookie(
  c,
  secret,
  'fortune_cookie',
  'secure'
)
const hostPrefixSignedCookie = await getSignedCookie(
  c,
  secret,
  'fortune_cookie',
  'host'
)
```

Also, if you wish to specify a prefix when setting the cookie, specify a value for the prefix option.

ts

```
setCookie(c, 'delicious_cookie', 'macha', {
  prefix: 'secure', // or `host`
})

await setSignedCookie(
  c,
  'delicious_cookie',
  'macha',
  'secret choco chips',
  {
    prefix: 'secure', // or `host`
  }
)
```

## Following the best practices​

A New Cookie RFC (a.k.a cookie-bis) and CHIPS include some best practices for Cookie settings that developers should follow.

- [RFC6265bis-13](https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis-13)
  - `Max-Age`/`Expires` limitation
  - `__Host-`/`__Secure-` prefix limitation
- [CHIPS-01](https://www.ietf.org/archive/id/draft-cutler-httpbis-partitioned-cookies-01.html)
  - `Partitioned` limitation

Hono is following the best practices. The cookie helper will throw an `Error` when parsing cookies under the following conditions:

- The cookie name starts with `__Secure-`, but `secure` option is not set.
- The cookie name starts with `__Host-`, but `secure` option is not set.
- The cookie name starts with `__Host-`, but `path` is not `/`.
- The cookie name starts with `__Host-`, but `domain` is set.
- The `maxAge` option value is greater than 400 days.
- The `expires` option value is 400 days later than the current time.

---

# css Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# css Helper​

The css helper - `hono/css` - is Hono's built-in CSS in JS(X).

You can write CSS in JSX in a JavaScript template literal named `css`. The return value of `css` will be the class name, which is set to the value of the class attribute. The `<Style />` component will then contain the value of the CSS.

## Import​

ts

```
import { Hono } from 'hono'
import { css, cx, keyframes, Style } from 'hono/css'
```

## cssExperimental​

You can write CSS in the `css` template literal. In this case, it uses `headerClass` as a value of the `class` attribute. Don't forget to add `<Style />` as it contains the CSS content.

ts

```
app.get('/', (c) => {
  const headerClass = css`
    background-color: orange;
    color: white;
    padding: 1rem;
  `
  return c.html(
    <html>
      <head>
        <Style />
      </head>
      <body>
        <h1 class={headerClass}>Hello!</h1>
      </body>
    </html>
  )
})
```

You can style pseudo-classes like `:hover` by using the [nesting selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Nesting_selector), `&`:

ts

```
const buttonClass = css`
  background-color: #fff;
  &:hover {
    background-color: red;
  }
`
```

### Extending​

You can extend the CSS definition by embedding the class name.

tsx

```
const baseClass = css`
  color: white;
  background-color: blue;
`

const header1Class = css`
  ${baseClass}
  font-size: 3rem;
`

const header2Class = css`
  ${baseClass}
  font-size: 2rem;
`
```

In addition, the syntax of `${baseClass} {}` enables nesting classes.

tsx

```
const headerClass = css`
  color: white;
  background-color: blue;
`
const containerClass = css`
  ${headerClass} {
    h1 {
      font-size: 3rem;
    }
  }
`
return c.render(
  <div class={containerClass}>
    <header class={headerClass}>
      <h1>Hello!</h1>
    </header>
  </div>
)
```

### Global styles​

A pseudo-selector called `:-hono-global` allows you to define global styles.

tsx

```
const globalClass = css`
  :-hono-global {
    html {
      font-family: Arial, Helvetica, sans-serif;
    }
  }
`

return c.render(
  <div class={globalClass}>
    <h1>Hello!</h1>
    <p>Today is a good day.</p>
  </div>
)
```

Or you can write CSS in the `<Style />` component with the `css` literal.

tsx

```
export const renderer = jsxRenderer(({ children, title }) => {
  return (
    <html>
      <head>
        <Style>{css`
          html {
            font-family: Arial, Helvetica, sans-serif;
          }
        `}</Style>
        <title>{title}</title>
      </head>
      <body>
        <div>{children}</div>
      </body>
    </html>
  )
})
```

## keyframesExperimental​

You can use `keyframes` to write the contents of `@keyframes`. In this case, `fadeInAnimation` will be the name of the animation

tsx

```
const fadeInAnimation = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`
const headerClass = css`
  animation-name: ${fadeInAnimation};
  animation-duration: 2s;
`
const Header = () => <a class={headerClass}>Hello!</a>
```

## cxExperimental​

The `cx` composites the two class names.

tsx

```
const buttonClass = css`
  border-radius: 10px;
`
const primaryClass = css`
  background: orange;
`
const Button = () => (
  <a class={cx(buttonClass, primaryClass)}>Click!</a>
)
```

It can also compose simple strings.

tsx

```
const Header = () => <a class={cx('h1', primaryClass)}>Hi</a>
```

## Usage in combination withSecure Headersmiddleware​

If you want to use the css helpers in combination with the [Secure Headers](https://hono.dev/docs/middleware/builtin/secure-headers) middleware, you can add the [nonceattribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) to the `<Style nonce={c.get('secureHeadersNonce')} />` to avoid Content-Security-Policy caused by the css helpers.

tsx

```
import { secureHeaders, NONCE } from 'hono/secure-headers'

app.get(
  '*',
  secureHeaders({
    contentSecurityPolicy: {
      // Set the pre-defined nonce value to `styleSrc`:
      styleSrc: [NONCE],
    },
  })
)

app.get('/', (c) => {
  const headerClass = css`
    background-color: orange;
    color: white;
    padding: 1rem;
  `
  return c.html(
    <html>
      <head>
        {/* Set the `nonce` attribute on the css helpers `style` and `script` elements */}
        <Style nonce={c.get('secureHeadersNonce')} />
      </head>
      <body>
        <h1 class={headerClass}>Hello!</h1>
      </body>
    </html>
  )
})
```

## Tips​

If you use VS Code, you can use [vscode-styled-components](https://marketplace.visualstudio.com/items?itemName=styled-components.vscode-styled-components) for Syntax highlighting and IntelliSense for css tagged literals.

![](https://hono.dev/images/css-ss.png)

---

# Dev Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Dev Helper​

Dev Helper provides useful methods you can use in development.

ts

```
import { Hono } from 'hono'
import { getRouterName, showRoutes } from 'hono/dev'
```

## getRouterName()​

You can get the name of the currently used router with `getRouterName()`.

ts

```
const app = new Hono()

// ...

console.log(getRouterName(app))
```

## showRoutes()​

`showRoutes()` function displays the registered routes in your console.

Consider an application like the following:

ts

```
const app = new Hono().basePath('/v1')

app.get('/posts', (c) => {
  // ...
})

app.get('/posts/:id', (c) => {
  // ...
})

app.post('/posts', (c) => {
  // ...
})

showRoutes(app, {
  verbose: true,
})
```

When this application starts running, the routes will be shown in your console as follows:

txt

```
GET   /v1/posts
GET   /v1/posts/:id
POST  /v1/posts
```

## Options​

### optionalverbose:boolean​

When set to `true`, it displays verbose information.

### optionalcolorize:boolean​

When set to `false`, the output will not be colored.

---

# Factory Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Factory Helper​

The Factory Helper provides useful functions for creating Hono's components such as Middleware. Sometimes it's difficult to set the proper TypeScript types, but this helper facilitates that.

## Import​

ts

```
import { Hono } from 'hono'
import { createFactory, createMiddleware } from 'hono/factory'
```

## createFactory()​

`createFactory()` will create an instance of the Factory class.

ts

```
import { createFactory } from 'hono/factory'

const factory = createFactory()
```

You can pass your Env types as Generics:

ts

```
type Env = {
  Variables: {
    foo: string
  }
}

const factory = createFactory<Env>()
```

### Options​

### optionaldefaultAppOptions:HonoOptions​

The default options to pass to the Hono application created by `createApp()`.

ts

```
const factory = createFactory({
  defaultAppOptions: { strict: false },
})

const app = factory.createApp() // `strict: false` is applied
```

## createMiddleware()​

`createMiddleware()` is shortcut of `factory.createMiddleware()`. This function will create your custom middleware.

ts

```
const messageMiddleware = createMiddleware(async (c, next) => {
  await next()
  c.res.headers.set('X-Message', 'Good morning!')
})
```

Tip: If you want to get an argument like `message`, you can create it as a function like the following.

ts

```
const messageMiddleware = (message: string) => {
  return createMiddleware(async (c, next) => {
    await next()
    c.res.headers.set('X-Message', message)
  })
}

app.use(messageMiddleware('Good evening!'))
```

## factory.createHandlers()​

`createHandlers()` helps to define handlers in a different place than `app.get('/')`.

ts

```
import { createFactory } from 'hono/factory'
import { logger } from 'hono/logger'

// ...

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

## factory.createApp()​

`createApp()` helps to create an instance of Hono with the proper types. If you use this method with `createFactory()`, you can avoid redundancy in the definition of the `Env` type.

If your application is like this, you have to set the `Env` in two places:

ts

```
import { createMiddleware } from 'hono/factory'

type Env = {
  Variables: {
    myVar: string
  }
}

// 1. Set the `Env` to `new Hono()`
const app = new Hono<Env>()

// 2. Set the `Env` to `createMiddleware()`
const mw = createMiddleware<Env>(async (c, next) => {
  await next()
})

app.use(mw)
```

By using `createFactory()` and `createApp()`, you can set the `Env` only in one place.

ts

```
import { createFactory } from 'hono/factory'

// ...

// Set the `Env` to `createFactory()`
const factory = createFactory<Env>()

const app = factory.createApp()

// factory also has `createMiddleware()`
const mw = factory.createMiddleware(async (c, next) => {
  await next()
})
```

`createFactory()` can receive the `initApp` option to initialize an `app` created by `createApp()`. The following is an example that uses the option.

ts

```
// factory-with-db.ts
type Env = {
  Bindings: {
    MY_DB: D1Database
  }
  Variables: {
    db: DrizzleD1Database
  }
}

export default createFactory<Env>({
  initApp: (app) => {
    app.use(async (c, next) => {
      const db = drizzle(c.env.MY_DB)
      c.set('db', db)
      await next()
    })
  },
})
```

ts

```
// crud.ts
import factoryWithDB from './factory-with-db'

const app = factoryWithDB.createApp()

app.post('/posts', (c) => {
  c.var.db.insert()
  // ...
})
```

---

# html Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# html Helper​

The html Helper lets you write HTML in JavaScript template literal with a tag named `html`. Using `raw()`, the content will be rendered as is. You have to escape these strings by yourself.

## Import​

ts

```
import { Hono } from 'hono'
import { html, raw } from 'hono/html'
```

## html​

ts

```
const app = new Hono()

app.get('/:username', (c) => {
  const { username } = c.req.param()
  return c.html(
    html`<!doctype html>
      <h1>Hello! ${username}!</h1>`
  )
})
```

### Insert snippets into JSX​

Insert the inline script into JSX:

tsx

```
app.get('/', (c) => {
  return c.html(
    <html>
      <head>
        <title>Test Site</title>
        {html`
          <script>
            // No need to use dangerouslySetInnerHTML.
            // If you write it here, it will not be escaped.
          </script>
        `}
      </head>
      <body>Hello!</body>
    </html>
  )
})
```

### Act as functional component​

Since `html` returns an HtmlEscapedString, it can act as a fully functional component without using JSX.

#### Usehtmlto speed up the process instead ofmemo​

typescript

```
const Footer = () => html`
  <footer>
    <address>My Address...</address>
  </footer>
`
```

### Receives props and embeds values​

typescript

```
interface SiteData {
  title: string
  description: string
  image: string
  children?: any
}
const Layout = (props: SiteData) => html`
<html>
<head>
  <meta charset="UTF-8">
  <title>${props.title}</title>
  <meta name="description" content="${props.description}">
  <head prefix="og: http://ogp.me/ns#">
  <meta property="og:type" content="article">
  
  <meta property="og:title" content="${props.title}">
  <meta property="og:image" content="${props.image}">
</head>
<body>
  ${props.children}
</body>
</html>
`

const Content = (props: { siteData: SiteData; name: string }) => (
  <Layout {...props.siteData}>
    <h1>Hello {props.name}</h1>
  </Layout>
)

app.get('/', (c) => {
  const props = {
    name: 'World',
    siteData: {
      title: 'Hello <> World',
      description: 'This is a description',
      image: 'https://example.com/image.png',
    },
  }
  return c.html(<Content {...props} />)
})
```

## raw()​

ts

```
app.get('/', (c) => {
  const name = 'John &quot;Johnny&quot; Smith'
  return c.html(html`<p>I'm ${raw(name)}.</p>`)
})
```

## Tips​

Thanks to these libraries, Visual Studio Code and vim also interprets template literals as HTML, allowing syntax highlighting and formatting to be applied.

- [https://marketplace.visualstudio.com/items?itemName=bierner.lit-html](https://marketplace.visualstudio.com/items?itemName=bierner.lit-html)
- [https://github.com/MaxMEllon/vim-jsx-pretty](https://github.com/MaxMEllon/vim-jsx-pretty)

---

# JWT Authentication Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# JWT Authentication Helper​

This helper provides functions for encoding, decoding, signing, and verifying JSON Web Tokens (JWTs). JWTs are commonly used for authentication and authorization purposes in web applications. This helper offers robust JWT functionality with support for various cryptographic algorithms.

## Import​

To use this helper, you can import it as follows:

ts

```
import { decode, sign, verify } from 'hono/jwt'
```

INFO

[JWT Middleware](https://hono.dev/docs/middleware/builtin/jwt) also import the `jwt` function from the `hono/jwt`.

## sign()​

This function generates a JWT token by encoding a payload and signing it using the specified algorithm and secret.

ts

```
sign(
  payload: unknown,
  secret: string,
  alg?: 'HS256';

): Promise<string>;
```

### Example​

ts

```
import { sign } from 'hono/jwt'

const payload = {
  sub: 'user123',
  role: 'admin',
  exp: Math.floor(Date.now() / 1000) + 60 * 5, // Token expires in 5 minutes
}
const secret = 'mySecretKey'
const token = await sign(payload, secret)
```

### Options​

#### requiredpayload:unknown​

The JWT payload to be signed. You can include other claims like in [Payload Validation](#payload-validation).

#### requiredsecret:string​

The secret key used for JWT verification or signing.

#### optionalalg:AlgorithmTypes​

The algorithm used for JWT signing or verification. The default is HS256.

## verify()​

This function checks if a JWT token is genuine and still valid. It ensures the token hasn't been altered and checks validity only if you added [Payload Validation](#payload-validation).

ts

```
verify(
  token: string,
  secret: string,
  alg?: 'HS256';
  issuer?: string | RegExp;
): Promise<any>;
```

### Example​

ts

```
import { verify } from 'hono/jwt'

const tokenToVerify = 'token'
const secretKey = 'mySecretKey'

const decodedPayload = await verify(tokenToVerify, secretKey)
console.log(decodedPayload)
```

### Options​

#### requiredtoken:string​

The JWT token to be verified.

#### requiredsecret:string​

The secret key used for JWT verification or signing.

#### optionalalg:AlgorithmTypes​

The algorithm used for JWT signing or verification. The default is HS256.

#### optionalissuer:string | RegExp​

The expected issuer used for JWT verification.

## decode()​

This function decodes a JWT token without performing signature verification. It extracts and returns the header and payload from the token.

ts

```
decode(token: string): { header: any; payload: any };
```

### Example​

ts

```
import { decode } from 'hono/jwt'

// Decode the JWT token
const tokenToDecode =
  'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAidXNlcjEyMyIsICJyb2xlIjogImFkbWluIn0.JxUwx6Ua1B0D1B0FtCrj72ok5cm1Pkmr_hL82sd7ELA'

const { header, payload } = decode(tokenToDecode)

console.log('Decoded Header:', header)
console.log('Decoded Payload:', payload)
```

### Options​

#### requiredtoken:string​

The JWT token to be decoded.

> The `decode` function allows you to inspect the header and payload of a JWT token *without* performing verification. This can be useful for debugging or extracting information from JWT tokens.

## Payload Validation​

When verifying a JWT token, the following payload validations are performed:

- `exp`: The token is checked to ensure it has not expired.
- `nbf`: The token is checked to ensure it is not being used before a specified time.
- `iat`: The token is checked to ensure it is not issued in the future.
- `iss`: The token is checked to ensure it has been issued by a trusted issuer.

Please ensure that your JWT payload includes these fields, as an object, if you intend to perform these checks during verification.

## Custom Error Types​

The module also defines custom error types to handle JWT-related errors.

- `JwtAlgorithmNotImplemented`: Indicates that the requested JWT algorithm is not implemented.
- `JwtTokenInvalid`: Indicates that the JWT token is invalid.
- `JwtTokenNotBefore`: Indicates that the token is being used before its valid date.
- `JwtTokenExpired`: Indicates that the token has expired.
- `JwtTokenIssuedAt`: Indicates that the "iat" claim in the token is incorrect.
- `JwtTokenIssuer`: Indicates that the "iss" claim in the token is incorrect.
- `JwtTokenSignatureMismatched`: Indicates a signature mismatch in the token.

## Supported AlgorithmTypes​

The module supports the following JWT cryptographic algorithms:

- `HS256`: HMAC using SHA-256
- `HS384`: HMAC using SHA-384
- `HS512`: HMAC using SHA-512
- `RS256`: RSASSA-PKCS1-v1_5 using SHA-256
- `RS384`: RSASSA-PKCS1-v1_5 using SHA-384
- `RS512`: RSASSA-PKCS1-v1_5 using SHA-512
- `PS256`: RSASSA-PSS using SHA-256 and MGF1 with SHA-256
- `PS384`: RSASSA-PSS using SHA-386 and MGF1 with SHA-386
- `PS512`: RSASSA-PSS using SHA-512 and MGF1 with SHA-512
- `ES256`: ECDSA using P-256 and SHA-256
- `ES384`: ECDSA using P-384 and SHA-384
- `ES512`: ECDSA using P-521 and SHA-512
- `EdDSA`: EdDSA using Ed25519

---

# Proxy Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Proxy Helper​

Proxy Helper provides useful functions when using Hono application as a (reverse) proxy.

## Import​

ts

```
import { Hono } from 'hono'
import { proxy } from 'hono/proxy'
```

## proxy()​

`proxy()` is a `fetch()` API wrapper for proxy. The parameters and return value are the same as for `fetch()` (except for the proxy-specific options).

The `Accept-Encoding` header is replaced with an encoding that the current runtime can handle. Unnecessary response headers are deleted, and a `Response` object is returned that you can return as a response from the handler.

### Examples​

Simple usage:

ts

```
app.get('/proxy/:path', (c) => {
  return proxy(`http://${originServer}/${c.req.param('path')}`)
})
```

Complicated usage:

ts

```
app.get('/proxy/:path', async (c) => {
  const res = await proxy(
    `http://${originServer}/${c.req.param('path')}`,
    {
      headers: {
        ...c.req.header(), // optional, specify only when forwarding all the request data (including credentials) is necessary.
        'X-Forwarded-For': '127.0.0.1',
        'X-Forwarded-Host': c.req.header('host'),
        Authorization: undefined, // do not propagate request headers contained in c.req.header('Authorization')
      },
    }
  )
  res.headers.delete('Set-Cookie')
  return res
})
```

Or you can pass the `c.req` as a parameter.

ts

```
app.all('/proxy/:path', (c) => {
  return proxy(`http://${originServer}/${c.req.param('path')}`, {
    ...c.req, // optional, specify only when forwarding all the request data (including credentials) is necessary.
    headers: {
      ...c.req.header(),
      'X-Forwarded-For': '127.0.0.1',
      'X-Forwarded-Host': c.req.header('host'),
      Authorization: undefined, // do not propagate request headers contained in c.req.header('Authorization')
    },
  })
})
```

You can override the default global `fetch` function with the `customFetch` option:

ts

```
app.get('/proxy', (c) => {
  return proxy('https://example.com/', {
    customFetch,
  })
})
```

### Connection Header Processing​

By default, `proxy()` ignores the `Connection` header to prevent Hop-by-Hop Header Injection attacks. You can enable strict RFC 9110 compliance with the `strictConnectionProcessing` option:

ts

```
// Default behavior (recommended for untrusted clients)
app.get('/proxy/:path', (c) => {
  return proxy(`http://${originServer}/${c.req.param('path')}`, c.req)
})

// Strict RFC 9110 compliance (use only in trusted environments)
app.get('/internal-proxy/:path', (c) => {
  return proxy(`http://${internalServer}/${c.req.param('path')}`, {
    ...c.req,
    strictConnectionProcessing: true,
  })
})
```

### ProxyFetch​

The type of `proxy()` is defined as `ProxyFetch` and is as follows

ts

```
interface ProxyRequestInit extends Omit<RequestInit, 'headers'> {
  raw?: Request
  customFetch?: (request: Request) => Promise<Response>
  strictConnectionProcessing?: boolean
  headers?:
    | HeadersInit
    | [string, string][]
    | Record<RequestHeader, string | undefined>
    | Record<string, string | undefined>
}

interface ProxyFetch {
  (
    input: string | URL | Request,
    init?: ProxyRequestInit
  ): Promise<Response>
}
```

---

# Route Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Route Helper​

The Route Helper provides enhanced routing information for debugging and middleware development. It allows you to access detailed information about matched routes and the current route being processed.

## Import​

ts

```
import { Hono } from 'hono'
import {
  matchedRoutes,
  routePath,
  baseRoutePath,
  basePath,
} from 'hono/route'
```

## Usage​

### Basic route information​

ts

```
const app = new Hono()

app.get('/posts/:id', (c) => {
  const currentPath = routePath(c) // '/posts/:id'
  const routes = matchedRoutes(c) // Array of matched routes

  return c.json({
    path: currentPath,
    totalRoutes: routes.length,
  })
})
```

### Working with sub-applications​

ts

```
const app = new Hono()
const apiApp = new Hono()

apiApp.get('/posts/:id', (c) => {
  return c.json({
    routePath: routePath(c), // '/posts/:id'
    baseRoutePath: baseRoutePath(c), // '/api'
    basePath: basePath(c), // '/api' (with actual params)
  })
})

app.route('/api', apiApp)
```

## matchedRoutes()​

Returns an array of all routes that matched the current request, including middleware.

ts

```
app.all('/api/*', (c, next) => {
  console.log('API middleware')
  return next()
})

app.get('/api/users/:id', (c) => {
  const routes = matchedRoutes(c)
  // Returns: [
  //   { method: 'ALL', path: '/api/*', handler: [Function] },
  //   { method: 'GET', path: '/api/users/:id', handler: [Function] }
  // ]
  return c.json({ routes: routes.length })
})
```

## routePath()​

Returns the route path pattern registered for the current handler.

ts

```
app.get('/posts/:id', (c) => {
  console.log(routePath(c)) // '/posts/:id'
  return c.text('Post details')
})
```

### Using with index parameter​

You can optionally pass an index parameter to get the route path at a specific position, similar to `Array.prototype.at()`.

ts

```
app.all('/api/*', (c, next) => {
  return next()
})

app.get('/api/users/:id', (c) => {
  console.log(routePath(c, 0)) // '/api/*' (first matched route)
  console.log(routePath(c, -1)) // '/api/users/:id' (last matched route)
  return c.text('User details')
})
```

## baseRoutePath()​

Returns the base path pattern of the current route as specified in routing.

ts

```
const subApp = new Hono()
subApp.get('/posts/:id', (c) => {
  return c.text(baseRoutePath(c)) // '/:sub'
})

app.route('/:sub', subApp)
```

### Using with index parameter​

You can optionally pass an index parameter to get the base route path at a specific position, similar to `Array.prototype.at()`.

ts

```
app.all('/api/*', (c, next) => {
  return next()
})

const subApp = new Hono()
subApp.get('/users/:id', (c) => {
  console.log(baseRoutePath(c, 0)) // '/' (first matched route)
  console.log(baseRoutePath(c, -1)) // '/api' (last matched route)
  return c.text('User details')
})

app.route('/api', subApp)
```

## basePath()​

Returns the base path with embedded parameters from the actual request.

ts

```
const subApp = new Hono()
subApp.get('/posts/:id', (c) => {
  return c.text(basePath(c)) // '/api' (for request to '/api/posts/123')
})

app.route('/:sub', subApp)
```

---

# SSG Helper​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# SSG Helper​

SSG Helper generates a static site from your Hono application. It will retrieve the contents of registered routes and save them as static files.

## Usage​

### Manual​

If you have a simple Hono application like the following:

tsx

```
// index.tsx
const app = new Hono()

app.get('/', (c) => c.html('Hello, World!'))

app.use('/about', async (c, next) => {
  c.setRenderer((content) => {
    return c.html(
      <html>
        <head />
        <body>
          <p>{content}</p>
        </body>
      </html>
    )
  })
  await next()
})

app.get('/about', (c) => {
  return c.render(
    <>
      <title>Hono SSG Page</title>Hello!
    </>
  )
})

export default app
```

For Node.js, create a build script like this:

ts

```
// build.ts
import app from './index'
import { toSSG } from 'hono/ssg'
import fs from 'fs/promises'

toSSG(app, fs)
```

By executing the script, the files will be output as follows:

bash

```
ls ./static
about.html  index.html
```

### Vite Plugin​

Using the `@hono/vite-ssg` Vite Plugin, you can easily handle the process.

For more details, see here:

[https://github.com/honojs/vite-plugins/tree/main/packages/ssg](https://github.com/honojs/vite-plugins/tree/main/packages/ssg)

## toSSG​

`toSSG` is the main function for generating static sites, taking an application and a filesystem module as arguments. It is based on the following:

### Input​

The arguments for toSSG are specified in ToSSGInterface.

ts

```
export interface ToSSGInterface {
  (
    app: Hono,
    fsModule: FileSystemModule,
    options?: ToSSGOptions
  ): Promise<ToSSGResult>
}
```

- `app` specifies `new Hono()` with registered routes.
- `fs` specifies the following object, assuming `node:fs/promise`.

ts

```
export interface FileSystemModule {
  writeFile(path: string, data: string | Uint8Array): Promise<void>
  mkdir(
    path: string,
    options: { recursive: boolean }
  ): Promise<void | string>
}
```

### Using adapters for Deno and Bun​

If you want to use SSG on Deno or Bun, a `toSSG` function is provided for each file system.

For Deno:

ts

```
import { toSSG } from 'hono/deno'

toSSG(app) // The second argument is an option typed `ToSSGOptions`.
```

For Bun:

ts

```
import { toSSG } from 'hono/bun'

toSSG(app) // The second argument is an option typed `ToSSGOptions`.
```

### Options​

Options are specified in the ToSSGOptions interface.

ts

```
export interface ToSSGOptions {
  dir?: string
  concurrency?: number
  extensionMap?: Record<string, string>
  plugins?: SSGPlugin[]
}
```

- `dir` is the output destination for Static files. The default value is `./static`.
- `concurrency` is the concurrent number of files to be generated at the same time. The default value is `2`.
- `extensionMap` is a map containing the `Content-Type` as a key and the string of the extension as a value. This is used to determine the file extension of the output file.
- `plugins` is an array of SSG plugins that extend the functionality of the static site generation process.

### Output​

`toSSG` returns the result in the following Result type.

ts

```
export interface ToSSGResult {
  success: boolean
  files: string[]
  error?: Error
}
```

## Generate File​

### Route and Filename​

The following rules apply to the registered route information and the generated file name. The default `./static` behaves as follows:

- `/` -> `./static/index.html`
- `/path` -> `./static/path.html`
- `/path/` -> `./static/path/index.html`

### File Extension​

The file extension depends on the `Content-Type` returned by each route. For example, responses from `c.html` are saved as `.html`.

If you want to customize the file extensions, set the `extensionMap` option.

ts

```
import { toSSG, defaultExtensionMap } from 'hono/ssg'

// Save `application/x-html` content with `.html`
toSSG(app, fs, {
  extensionMap: {
    'application/x-html': 'html',
    ...defaultExtensionMap,
  },
})
```

Note that paths ending with a slash are saved as index.ext regardless of the extension.

ts

```
// save to ./static/html/index.html
app.get('/html/', (c) => c.html('html'))

// save to ./static/text/index.txt
app.get('/text/', (c) => c.text('text'))
```

## Middleware​

Introducing built-in middleware that supports SSG.

### ssgParams​

You can use an API like `generateStaticParams` of Next.js.

Example:

ts

```
app.get(
  '/shops/:id',
  ssgParams(async () => {
    const shops = await getShops()
    return shops.map((shop) => ({ id: shop.id }))
  }),
  async (c) => {
    const shop = await getShop(c.req.param('id'))
    if (!shop) {
      return c.notFound()
    }
    return c.render(
      <div>
        <h1>{shop.name}</h1>
      </div>
    )
  }
)
```

### disableSSG​

Routes with the `disableSSG` middleware set are excluded from static file generation by `toSSG`.

ts

```
app.get('/api', disableSSG(), (c) => c.text('an-api'))
```

### onlySSG​

Routes with the `onlySSG` middleware set will be overridden by `c.notFound()` after `toSSG` execution.

ts

```
app.get('/static-page', onlySSG(), (c) => c.html(<h1>Welcome to my site</h1>))
```

## Plugins​

Plugins allow you to extend the functionality of the static site generation process. They use hooks to customize the generation process at different stages.

### Default Plugin​

By default, `toSSG` uses `defaultPlugin` which skips non-200 status responses (like redirects, errors, or 404s). This prevents generating files for unsuccessful responses.

ts

```
import { toSSG, defaultPlugin } from 'hono/ssg'

// defaultPlugin is automatically applied when no plugins specified
toSSG(app, fs)

// Equivalent to:
toSSG(app, fs, { plugins: [defaultPlugin] })
```

If you specify custom plugins, `defaultPlugin` is **not** automatically included. To keep the default behavior while adding custom plugins, explicitly include it:

ts

```
toSSG(app, fs, {
  plugins: [defaultPlugin, myCustomPlugin],
})
```

### Hook Types​

Plugins can use the following hooks to customize the `toSSG` process:

ts

```
export type BeforeRequestHook = (req: Request) => Request | false
export type AfterResponseHook = (res: Response) => Response | false
export type AfterGenerateHook = (
  result: ToSSGResult
) => void | Promise<void>
```

- **BeforeRequestHook**: Called before processing each request. Return `false` to skip the route.
- **AfterResponseHook**: Called after receiving each response. Return `false` to skip file generation.
- **AfterGenerateHook**: Called after the entire generation process completes.

### Plugin Interface​

ts

```
export interface SSGPlugin {
  beforeRequestHook?: BeforeRequestHook | BeforeRequestHook[]
  afterResponseHook?: AfterResponseHook | AfterResponseHook[]
  afterGenerateHook?: AfterGenerateHook | AfterGenerateHook[]
}
```

### Basic Plugin Examples​

Filter only GET requests:

ts

```
const getOnlyPlugin: SSGPlugin = {
  beforeRequestHook: (req) => {
    if (req.method === 'GET') {
      return req
    }
    return false
  },
}
```

Filter by status code:

ts

```
const statusFilterPlugin: SSGPlugin = {
  afterResponseHook: (res) => {
    if (res.status === 200 || res.status === 500) {
      return res
    }
    return false
  },
}
```

Log generated files:

ts

```
const logFilesPlugin: SSGPlugin = {
  afterGenerateHook: (result) => {
    if (result.files) {
      result.files.forEach((file) => console.log(file))
    }
  },
}
```

### Advanced Plugin Example​

Here's an example of creating a sitemap plugin that generates a `sitemap.xml` file:

ts

```
// plugins.ts
import fs from 'node:fs/promises'
import path from 'node:path'
import type { SSGPlugin } from 'hono/ssg'
import { DEFAULT_OUTPUT_DIR } from 'hono/ssg'

export const sitemapPlugin = (baseURL: string): SSGPlugin => {
  return {
    afterGenerateHook: (result, fsModule, options) => {
      const outputDir = options?.dir ?? DEFAULT_OUTPUT_DIR
      const filePath = path.join(outputDir, 'sitemap.xml')
      const urls = result.files.map((file) =>
        new URL(file, baseURL).toString()
      )
      const siteMapText = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((url) => `<url><loc>${url}</loc></url>`).join('\n')}
</urlset>`
      fsModule.writeFile(filePath, siteMapText)
    },
  }
}
```

Applying plugins:

ts

```
import app from './index'
import { toSSG } from 'hono/ssg'
import { sitemapPlugin } from './plugins'

toSSG(app, fs, {
  plugins: [
    getOnlyPlugin,
    statusFilterPlugin,
    logFilesPlugin,
    sitemapPlugin('https://example.com'),
  ],
})
```
