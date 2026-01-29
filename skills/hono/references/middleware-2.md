# Language Middleware​ and more

# Language Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Language Middleware​

The Language Detector middleware automatically determines a user's preferred language (locale) from various sources and makes it available via `c.get('language')`. Detection strategies include query parameters, cookies, headers, and URL path segments. Perfect for internationalization (i18n) and locale-specific content.

## Import​

ts

```
import { Hono } from 'hono'
import { languageDetector } from 'hono/language'
```

## Basic Usage​

Detect language from query string, cookie, and header (default order), with fallback to English:

ts

```
const app = new Hono()

app.use(
  languageDetector({
    supportedLanguages: ['en', 'ar', 'ja'], // Must include fallback
    fallbackLanguage: 'en', // Required
  })
)

app.get('/', (c) => {
  const lang = c.get('language')
  return c.text(`Hello! Your language is ${lang}`)
})
```

### Client Examples​

sh

```
# Via path
curl http://localhost:8787/ar/home

# Via query parameter
curl http://localhost:8787/?lang=ar

# Via cookie
curl -H 'Cookie: language=ja' http://localhost:8787/

# Via header
curl -H 'Accept-Language: ar,en;q=0.9' http://localhost:8787/
```

## Default Configuration​

ts

```
export const DEFAULT_OPTIONS: DetectorOptions = {
  order: ['querystring', 'cookie', 'header'],
  lookupQueryString: 'lang',
  lookupCookie: 'language',
  lookupFromHeaderKey: 'accept-language',
  lookupFromPathIndex: 0,
  caches: ['cookie'],
  ignoreCase: true,
  fallbackLanguage: 'en',
  supportedLanguages: ['en'],
  cookieOptions: {
    sameSite: 'Strict',
    secure: true,
    maxAge: 365 * 24 * 60 * 60,
    httpOnly: true,
  },
  debug: false,
}
```

## Key Behaviors​

### Detection Workflow​

1. **Order**: Checks sources in this sequence by default:
  - Query parameter (?lang=ar)
  - Cookie (language=ar)
  - Accept-Language header
2. **Caching**: Stores detected language in a cookie (1 year by default)
3. **Fallback**: Uses `fallbackLanguage` if no valid detection (must be in `supportedLanguages`)

## Advanced Configuration​

### Custom Detection Order​

Prioritize URL path detection (e.g., /en/about):

ts

```
app.use(
  languageDetector({
    order: ['path', 'cookie', 'querystring', 'header'],
    lookupFromPathIndex: 0, // /en/profile → index 0 = 'en'
    supportedLanguages: ['en', 'ar'],
    fallbackLanguage: 'en',
  })
)
```

### Language Code Transformation​

Normalize complex codes (e.g., en-US → en):

ts

```
app.use(
  languageDetector({
    convertDetectedLanguage: (lang) => lang.split('-')[0],
    supportedLanguages: ['en', 'ja'],
    fallbackLanguage: 'en',
  })
)
```

### Cookie Configuration​

ts

```
app.use(
  languageDetector({
    lookupCookie: 'app_lang',
    caches: ['cookie'],
    cookieOptions: {
      path: '/', // Cookie path
      sameSite: 'Lax', // Cookie same-site policy
      secure: true, // Only send over HTTPS
      maxAge: 86400 * 365, // 1 year expiration
      httpOnly: true, // Not accessible via JavaScript
      domain: '.example.com', // Optional: specific domain
    },
  })
)
```

To disable cookie caching:

ts

```
languageDetector({
  caches: false,
})
```

### Debugging​

Log detection steps:

ts

```
languageDetector({
  debug: true, // Shows: "Detected from querystring: ar"
})
```

## Options Reference​

### Basic Options​

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| supportedLanguages | string[] | ['en'] | Yes | Allowed language codes |
| fallbackLanguage | string | 'en' | Yes | Default language |
| order | DetectorType[] | ['querystring', 'cookie', 'header'] | No | Detection sequence |
| debug | boolean | false | No | Enable logging |

### Detection Options​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| lookupQueryString | string | 'lang' | Query parameter name |
| lookupCookie | string | 'language' | Cookie name |
| lookupFromHeaderKey | string | 'accept-language' | Header name |
| lookupFromPathIndex | number | 0 | Path segment index |

### Cookie Options​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| caches | CacheType[] | false | ['cookie'] | Cache settings |
| cookieOptions.path | string | '/' | Cookie path |
| cookieOptions.sameSite | 'Strict' | 'Lax' | 'None' | 'Strict' | SameSite policy |
| cookieOptions.secure | boolean | true | HTTPS only |
| cookieOptions.maxAge | number | 31536000 | Expiration (seconds) |
| cookieOptions.httpOnly | boolean | true | JS accessibility |
| cookieOptions.domain | string | undefined | Cookie domain |

### Advanced Options​

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| ignoreCase | boolean | true | Case-insensitive matching |
| convertDetectedLanguage | (lang: string) => string | undefined | Language code transformer |

## Validation & Error Handling​

- `fallbackLanguage` must be in `supportedLanguages` (throws error during setup)
- `lookupFromPathIndex` must be ≥ 0
- Invalid configurations throw errors during middleware initialization
- Failed detections silently use `fallbackLanguage`

## Common Recipes​

### Path-Based Routing​

ts

```
app.get('/:lang/home', (c) => {
  const lang = c.get('language') // 'en', 'ar', etc.
  return c.json({ message: getLocalizedContent(lang) })
})
```

### Multiple Supported Languages​

ts

```
languageDetector({
  supportedLanguages: ['en', 'en-GB', 'ar', 'ar-EG'],
  convertDetectedLanguage: (lang) => lang.replace('_', '-'), // Normalize
})
```

---

# Logger Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Logger Middleware​

It's a simple logger.

## Import​

ts

```
import { Hono } from 'hono'
import { logger } from 'hono/logger'
```

## Usage​

ts

```
const app = new Hono()

app.use(logger())
app.get('/', (c) => c.text('Hello Hono!'))
```

## Logging Details​

The Logger Middleware logs the following details for each request:

- **Incoming Request**: Logs the HTTP method, request path, and incoming request.
- **Outgoing Response**: Logs the HTTP method, request path, response status code, and request/response times.
- **Status Code Coloring**: Response status codes are color-coded for better visibility and quick identification of status categories. Different status code categories are represented by different colors.
- **Elapsed Time**: The time taken for the request/response cycle is logged in a human-readable format, either in milliseconds (ms) or seconds (s).

By using the Logger Middleware, you can easily monitor the flow of requests and responses in your Hono application and quickly identify any issues or performance bottlenecks.

You can also extend the middleware further by providing your own `PrintFunc` function for tailored logging behavior.

## PrintFunc​

The Logger Middleware accepts an optional `PrintFunc` function as a parameter. This function allows you to customize the logger and add additional logs.

## Options​

### optionalfn:PrintFunc(str: string, ...rest: string[])​

- `str`: Passed by the logger.
- `...rest`: Additional string props to be printed to console.

### Example​

Setting up a custom `PrintFunc` function to the Logger Middleware:

ts

```
export const customLogger = (message: string, ...rest: string[]) => {
  console.log(message, ...rest)
}

app.use(logger(customLogger))
```

Setting up the custom logger in a route:

ts

```
app.post('/blog', (c) => {
  // Routing logic

  customLogger('Blog saved:', `Path: ${blog.url},`, `ID: ${blog.id}`)
  // Output
  // <-- POST /blog
  // Blog saved: Path: /blog/example, ID: 1
  // --> POST /blog 201 93ms

  // Return Context
})
```

---

# Method Override Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Method Override Middleware​

This middleware executes the handler of the specified method, which is different from the actual method of the request, depending on the value of the form, header, or query, and returns its response.

## Import​

ts

```
import { Hono } from 'hono'
import { methodOverride } from 'hono/method-override'
```

## Usage​

ts

```
const app = new Hono()

// If no options are specified, the value of `_method` in the form,
// e.g. DELETE, is used as the method.
app.use('/posts', methodOverride({ app }))

app.delete('/posts', (c) => {
  // ....
})
```

## For example​

Since HTML forms cannot send a DELETE method, you can put the value `DELETE` in the property named `_method` and send it. And the handler for `app.delete()` will be executed.

The HTML form:

html

```
<form action="/posts" method="POST">
  <input type="hidden" name="_method" value="DELETE" />
  <input type="text" name="id" />
</form>
```

The application:

ts

```
import { methodOverride } from 'hono/method-override'

const app = new Hono()
app.use('/posts', methodOverride({ app }))

app.delete('/posts', () => {
  // ...
})
```

You can change the default values or use the header value and query value:

ts

```
app.use('/posts', methodOverride({ app, form: '_custom_name' }))
app.use(
  '/posts',
  methodOverride({ app, header: 'X-METHOD-OVERRIDE' })
)
app.use('/posts', methodOverride({ app, query: '_method' }))
```

## Options​

### requiredapp:Hono​

The instance of `Hono` is used in your application.

### optionalform:string​

Form key with a value containing the method name. The default is `_method`.

### optionalheader:boolean​

Header name with a value containing the method name.

### optionalquery:boolean​

Query parameter key with a value containing the method name.

---

# Pretty JSON Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Pretty JSON Middleware​

Pretty JSON middleware enables "*JSON pretty print*" for JSON response body. Adding `?pretty` to url query param, the JSON strings are prettified.

js

```
// GET /
{"project":{"name":"Hono","repository":"https://github.com/honojs/hono"}}
```

will be:

js

```
// GET /?pretty
{
  "project": {
    "name": "Hono",
    "repository": "https://github.com/honojs/hono"
  }
}
```

## Import​

ts

```
import { Hono } from 'hono'
import { prettyJSON } from 'hono/pretty-json'
```

## Usage​

ts

```
const app = new Hono()

app.use(prettyJSON()) // With options: prettyJSON({ space: 4 })
app.get('/', (c) => {
  return c.json({ message: 'Hono!' })
})
```

## Options​

### optionalspace:number​

Number of spaces for indentation. The default is `2`.

### optionalquery:string​

The name of the query string for applying. The default is `pretty`.

### optionalforce:boolean​

When set to `true`, JSON responses are always prettified regardless of the query parameter. The default is `false`.

---

# Request ID Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Request ID Middleware​

Request ID Middleware generates a unique ID for each request, which you can use in your handlers.

INFO

**Node.js**: This middleware uses `crypto.randomUUID()` to generate IDs. The global `crypto` was introduced in Node.js version 20 or later. Therefore, errors may occur in versions earlier than that. In that case, please specify `generator`. However, if you are using [the Node.js adapter](https://github.com/honojs/node-server), it automatically sets `crypto` globally, so this is not necessary.

## Import​

ts

```
import { Hono } from 'hono'
import { requestId } from 'hono/request-id'
```

## Usage​

You can access the Request ID through the `requestId` variable in the handlers and middleware to which the Request ID Middleware is applied.

ts

```
const app = new Hono()

app.use('*', requestId())

app.get('/', (c) => {
  return c.text(`Your request id is ${c.get('requestId')}`)
})
```

If you want to explicitly specify the type, import `RequestIdVariables` and pass it in the generics of `new Hono()`.

ts

```
import type { RequestIdVariables } from 'hono/request-id'

const app = new Hono<{
  Variables: RequestIdVariables
}>()
```

### Set Request ID​

You set a custom request ID in the header (default: `X-Request-Id`), the middleware will use that value instead of generating a new one:

ts

```
const app = new Hono()

app.use('*', requestId())

app.get('/', (c) => {
  return c.text(`${c.get('requestId')}`)
})

const res = await app.request('/', {
  headers: {
    'X-Request-Id': 'your-custom-id',
  },
})
console.log(await res.text()) // your-custom-id
```

If you want to disable this feature, set [headerNameoption](#headername-string) to an empty string.

## Options​

### optionallimitLength:number​

The maximum length of the request ID. The default is `255`.

### optionalheaderName:string​

The header name used for the request ID. The default is `X-Request-Id`.

### optionalgenerator:(c: Context) => string​

The request ID generation function. By default, it uses `crypto.randomUUID()`.

## Platform specific Request IDs​

Some platform (such as AWS Lambda) already generate their own Request IDs per request. Without any additional configuration, this middleware is unaware of these specific Request IDs and generates a new Request ID. This can lead to confusion when looking at your application logs.

To unify these IDs, use the `generator` function to capture the platform specific Request ID and to use it in this middleware.

### Platform specific links​

- AWS Lambda
  - [AWS documentation: Context object](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-context.html)
  - [Hono: Access AWS Lambda Object](https://hono.dev/docs/getting-started/aws-lambda#access-aws-lambda-object)
- Cloudflare
  - [Cloudflare Ray ID](https://developers.cloudflare.com/fundamentals/reference/cloudflare-ray-id/)
- Deno
  - [Request ID on the Deno Blog](https://deno.com/blog/zero-config-debugging-deno-opentelemetry#:~:text=s%20automatically%20have-,unique%20request%20IDs,-associated%20with%20them)
- Fastly
  - [Fastly documentation: req.xid](https://www.fastly.com/documentation/reference/vcl/variables/client-request/req-xid/)

---

# Secure Headers Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Secure Headers Middleware​

Secure Headers Middleware simplifies the setup of security headers. Inspired in part by the capabilities of Helmet, it allows you to control the activation and deactivation of specific security headers.

## Import​

ts

```
import { Hono } from 'hono'
import { secureHeaders } from 'hono/secure-headers'
```

## Usage​

You can use the optimal settings by default.

ts

```
const app = new Hono()
app.use(secureHeaders())
```

You can suppress unnecessary headers by setting them to false.

ts

```
const app = new Hono()
app.use(
  '*',
  secureHeaders({
    xFrameOptions: false,
    xXssProtection: false,
  })
)
```

You can override default header values using a string.

ts

```
const app = new Hono()
app.use(
  '*',
  secureHeaders({
    strictTransportSecurity:
      'max-age=63072000; includeSubDomains; preload',
    xFrameOptions: 'DENY',
    xXssProtection: '1',
  })
)
```

## Supported Options​

Each option corresponds to the following Header Key-Value pairs.

| Option | Header | Value | Default |
| --- | --- | --- | --- |
| - | X-Powered-By | (Delete Header) | True |
| contentSecurityPolicy | Content-Security-Policy | Usage:Setting Content-Security-Policy | No Setting |
| contentSecurityPolicyReportOnly | Content-Security-Policy-Report-Only | Usage:Setting Content-Security-Policy | No Setting |
| trustedTypes | Trusted Types | Usage:Setting Content-Security-Policy | No Setting |
| requireTrustedTypesFor | Require Trusted Types For | Usage:Setting Content-Security-Policy | No Setting |
| crossOriginEmbedderPolicy | Cross-Origin-Embedder-Policy | require-corp | False |
| crossOriginResourcePolicy | Cross-Origin-Resource-Policy | same-origin | True |
| crossOriginOpenerPolicy | Cross-Origin-Opener-Policy | same-origin | True |
| originAgentCluster | Origin-Agent-Cluster | ?1 | True |
| referrerPolicy | Referrer-Policy | no-referrer | True |
| reportingEndpoints | Reporting-Endpoints | Usage:Setting Content-Security-Policy | No Setting |
| reportTo | Report-To | Usage:Setting Content-Security-Policy | No Setting |
| strictTransportSecurity | Strict-Transport-Security | max-age=15552000; includeSubDomains | True |
| xContentTypeOptions | X-Content-Type-Options | nosniff | True |
| xDnsPrefetchControl | X-DNS-Prefetch-Control | off | True |
| xDownloadOptions | X-Download-Options | noopen | True |
| xFrameOptions | X-Frame-Options | SAMEORIGIN | True |
| xPermittedCrossDomainPolicies | X-Permitted-Cross-Domain-Policies | none | True |
| xXssProtection | X-XSS-Protection | 0 | True |
| permissionPolicy | Permissions-Policy | Usage:Setting Permission-Policy | No Setting |

## Middleware Conflict​

Please be cautious about the order of specification when dealing with middleware that manipulates the same header.

In this case, Secure-headers operates and the `x-powered-by` is removed:

ts

```
const app = new Hono()
app.use(secureHeaders())
app.use(poweredBy())
```

In this case, Powered-By operates and the `x-powered-by` is added:

ts

```
const app = new Hono()
app.use(poweredBy())
app.use(secureHeaders())
```

## Setting Content-Security-Policy​

ts

```
const app = new Hono()
app.use(
  '/test',
  secureHeaders({
    reportingEndpoints: [
      {
        name: 'endpoint-1',
        url: 'https://example.com/reports',
      },
    ],
    // -- or alternatively
    // reportTo: [
    //   {
    //     group: 'endpoint-1',
    //     max_age: 10886400,
    //     endpoints: [{ url: 'https://example.com/reports' }],
    //   },
    // ],
    contentSecurityPolicy: {
      defaultSrc: ["'self'"],
      baseUri: ["'self'"],
      childSrc: ["'self'"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'", 'https:', 'data:'],
      formAction: ["'self'"],
      frameAncestors: ["'self'"],
      frameSrc: ["'self'"],
      imgSrc: ["'self'", 'data:'],
      manifestSrc: ["'self'"],
      mediaSrc: ["'self'"],
      objectSrc: ["'none'"],
      reportTo: 'endpoint-1',
      reportUri: '/csp-report',
      sandbox: ['allow-same-origin', 'allow-scripts'],
      scriptSrc: ["'self'"],
      scriptSrcAttr: ["'none'"],
      scriptSrcElem: ["'self'"],
      styleSrc: ["'self'", 'https:', "'unsafe-inline'"],
      styleSrcAttr: ['none'],
      styleSrcElem: ["'self'", 'https:', "'unsafe-inline'"],
      upgradeInsecureRequests: [],
      workerSrc: ["'self'"],
    },
  })
)
```

### nonceattribute​

You can add a [nonceattribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) to a `script` or `style` element by adding the `NONCE` imported from `hono/secure-headers` to a `scriptSrc` or `styleSrc`:

tsx

```
import { secureHeaders, NONCE } from 'hono/secure-headers'
import type { SecureHeadersVariables } from 'hono/secure-headers'

// Specify the variable types to infer the `c.get('secureHeadersNonce')`:
type Variables = SecureHeadersVariables

const app = new Hono<{ Variables: Variables }>()

// Set the pre-defined nonce value to `scriptSrc`:
app.get(
  '*',
  secureHeaders({
    contentSecurityPolicy: {
      scriptSrc: [NONCE, 'https://allowed1.example.com'],
    },
  })
)

// Get the value from `c.get('secureHeadersNonce')`:
app.get('/', (c) => {
  return c.html(
    <html>
      <body>
        {/** contents */}
        <script
          src='/js/client.js'
          nonce={c.get('secureHeadersNonce')}
        />
      </body>
    </html>
  )
})
```

If you want to generate the nonce value yourself, you can also specify a function as the following:

tsx

```
const app = new Hono<{
  Variables: { myNonce: string }
}>()

const myNonceGenerator: ContentSecurityPolicyOptionHandler = (c) => {
  // This function is called on every request.
  const nonce = Math.random().toString(36).slice(2)
  c.set('myNonce', nonce)
  return `'nonce-${nonce}'`
}

app.get(
  '*',
  secureHeaders({
    contentSecurityPolicy: {
      scriptSrc: [myNonceGenerator, 'https://allowed1.example.com'],
    },
  })
)

app.get('/', (c) => {
  return c.html(
    <html>
      <body>
        {/** contents */}
        <script src='/js/client.js' nonce={c.get('myNonce')} />
      </body>
    </html>
  )
})
```

## Setting Permission-Policy​

The Permission-Policy header allows you to control which features and APIs can be used in the browser. Here's an example of how to set it:

ts

```
const app = new Hono()
app.use(
  '*',
  secureHeaders({
    permissionsPolicy: {
      fullscreen: ['self'], // fullscreen=(self)
      bluetooth: ['none'], // bluetooth=(none)
      payment: ['self', 'https://example.com'], // payment=(self "https://example.com")
      syncXhr: [], // sync-xhr=()
      camera: false, // camera=none
      microphone: true, // microphone=*
      geolocation: ['*'], // geolocation=*
      usb: ['self', 'https://a.example.com', 'https://b.example.com'], // usb=(self "https://a.example.com" "https://b.example.com")
      accelerometer: ['https://*.example.com'], // accelerometer=("https://*.example.com")
      gyroscope: ['src'], // gyroscope=(src)
      magnetometer: [
        'https://a.example.com',
        'https://b.example.com',
      ], // magnetometer=("https://a.example.com" "https://b.example.com")
    },
  })
)
```

---

# Timeout Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Timeout Middleware​

The Timeout Middleware enables you to easily manage request timeouts in your application. It allows you to set a maximum duration for requests and optionally define custom error responses if the specified timeout is exceeded.

## Import​

ts

```
import { Hono } from 'hono'
import { timeout } from 'hono/timeout'
```

## Usage​

Here's how to use the Timeout Middleware with both default and custom settings:

Default Settings:

ts

```
const app = new Hono()

// Applying a 5-second timeout
app.use('/api', timeout(5000))

// Handling a route
app.get('/api/data', async (c) => {
  // Your route handler logic
  return c.json({ data: 'Your data here' })
})
```

Custom settings:

ts

```
import { HTTPException } from 'hono/http-exception'

// Custom exception factory function
const customTimeoutException = (context) =>
  new HTTPException(408, {
    message: `Request timeout after waiting ${context.req.headers.get(
      'Duration'
    )} seconds. Please try again later.`,
  })

// for Static Exception Message
// const customTimeoutException = new HTTPException(408, {
//   message: 'Operation timed out. Please try again later.'
// });

// Applying a 1-minute timeout with a custom exception
app.use('/api/long-process', timeout(60000, customTimeoutException))

app.get('/api/long-process', async (c) => {
  // Simulate a long process
  await new Promise((resolve) => setTimeout(resolve, 61000))
  return c.json({ data: 'This usually takes longer' })
})
```

## Notes​

- The duration for the timeout can be specified in milliseconds. The middleware will automatically reject the promise and potentially throw an error if the specified duration is exceeded.
- The timeout middleware cannot be used with stream Thus, use `stream.close` and `setTimeout` together.

ts

```
app.get('/sse', async (c) => {
  let id = 0
  let running = true
  let timer: number | undefined

  return streamSSE(c, async (stream) => {
    timer = setTimeout(() => {
      console.log('Stream timeout reached, closing stream')
      stream.close()
    }, 3000) as unknown as number

    stream.onAbort(async () => {
      console.log('Client closed connection')
      running = false
      clearTimeout(timer)
    })

    while (running) {
      const message = `It is ${new Date().toISOString()}`
      await stream.writeSSE({
        data: message,
        event: 'time-update',
        id: String(id++),
      })
      await stream.sleep(1000)
    }
  })
})
```

## Middleware Conflicts​

Be cautious about the order of middleware, especially when using error-handling or other timing-related middleware, as it might affect the behavior of this timeout middleware.

---

# Server

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Server-Timing Middleware​

The [Server-Timing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing) Middleware provides performance metrics in the response headers.

INFO

Note: On Cloudflare Workers, the timer metrics may not be accurate, since [timers only show the time of last I/O](https://developers.cloudflare.com/workers/learning/security-model/#step-1-disallow-timers-and-multi-threading).

## Import​

npmts

```
import { Hono } from 'hono'
import {
  timing,
  setMetric,
  startTime,
  endTime,
  wrapTime,
} from 'hono/timing'
import type { TimingVariables } from 'hono/timing'
```

## Usage​

js

```
// Specify the variable types to infer the `c.get('metric')`:
type Variables = TimingVariables

const app = new Hono<{ Variables: Variables }>()

// add the middleware to your router
app.use(timing());

app.get('/', async (c) => {

  // add custom metrics
  setMetric(c, 'region', 'europe-west3')

  // add custom metrics with timing, must be in milliseconds
  setMetric(c, 'custom', 23.8, 'My custom Metric')

  // start a new timer
  startTime(c, 'db');
  const data = await db.findMany(...);

  // end the timer
  endTime(c, 'db');

  // ...or you can also just wrap a Promise using this function:
  const data = await wrapTime(c, 'db', db.findMany(...));

  return c.json({ response: data });
});
```

### Conditionally enabled​

ts

```
const app = new Hono()

app.use(
  '*',
  timing({
    // c: Context of the request
    enabled: (c) => c.req.method === 'POST',
  })
)
```

## Result​

![](https://hono.dev/images/timing-example.png)

## Options​

### optionaltotal:boolean​

Show the total response time. The default is `true`.

### optionalenabled:boolean|(c: Context) => boolean​

Whether timings should be added to the headers or not. The default is `true`.

### optionaltotalDescription:boolean​

Description for the total response time. The default is `Total Response Time`.

### optionalautoEnd:boolean​

If `startTime()` should end automatically at the end of the request. If disabled, not manually ended timers will not be shown.

### optionalcrossOrigin:boolean|string|(c: Context) => boolean | string​

The origin this timings header should be readable.

- If false, only from current origin.
- If true, from all origin.
- If string, from this domain(s). Multiple domains must be separated with a comma.

The default is `false`. See more [docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Timing-Allow-Origin).

---

# Trailing Slash Middleware​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Trailing Slash Middleware​

This middleware handles Trailing Slash in the URL on a GET request.

`appendTrailingSlash` redirects the URL to which it added the Trailing Slash if the content was not found. Also, `trimTrailingSlash` will remove the Trailing Slash.

## Import​

ts

```
import { Hono } from 'hono'
import {
  appendTrailingSlash,
  trimTrailingSlash,
} from 'hono/trailing-slash'
```

## Usage​

Example of redirecting a GET request of `/about/me` to `/about/me/`.

ts

```
import { Hono } from 'hono'
import { appendTrailingSlash } from 'hono/trailing-slash'

const app = new Hono({ strict: true })

app.use(appendTrailingSlash())
app.get('/about/me/', (c) => c.text('With Trailing Slash'))
```

Example of redirecting a GET request of `/about/me/` to `/about/me`.

ts

```
import { Hono } from 'hono'
import { trimTrailingSlash } from 'hono/trailing-slash'

const app = new Hono({ strict: true })

app.use(trimTrailingSlash())
app.get('/about/me', (c) => c.text('Without Trailing Slash'))
```

## Note​

It will be enabled when the request method is `GET` and the response status is `404`.

---

# Third

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Third-party Middleware​

Third-party middleware refers to middleware not bundled within the Hono package. Most of this middleware leverages external libraries.

### Authentication​

- [Auth.js(Next Auth)](https://github.com/honojs/middleware/tree/main/packages/auth-js)
- [Casbin](https://github.com/honojs/middleware/tree/main/packages/casbin)
- [Clerk Auth](https://github.com/honojs/middleware/tree/main/packages/clerk-auth)
- [Cloudflare Access](https://github.com/honojs/middleware/tree/main/packages/cloudflare-access)
- [OAuth Providers](https://github.com/honojs/middleware/tree/main/packages/oauth-providers)
- [OIDC Auth](https://github.com/honojs/middleware/tree/main/packages/oidc-auth)
- [Firebase Auth](https://github.com/honojs/middleware/tree/main/packages/firebase-auth)
- [Verify RSA JWT (JWKS)](https://github.com/wataruoguchi/verify-rsa-jwt-cloudflare-worker)
- [Stytch Auth](https://github.com/honojs/middleware/tree/main/packages/stytch-auth)

### Validators​

- [Ajv Validator](https://github.com/honojs/middleware/tree/main/packages/ajv-validator)
- [ArkType Validator](https://github.com/honojs/middleware/tree/main/packages/arktype-validator)
- [Class Validator](https://github.com/honojs/middleware/tree/main/packages/class-validator)
- [Conform Validator](https://github.com/honojs/middleware/tree/main/packages/conform-validator)
- [Effect Schema Validator](https://github.com/honojs/middleware/tree/main/packages/effect-validator)
- [Standard Schema Validator](https://github.com/honojs/middleware/tree/main/packages/standard-validator)
- [TypeBox Validator](https://github.com/honojs/middleware/tree/main/packages/typebox-validator)
- [Typia Validator](https://github.com/honojs/middleware/tree/main/packages/typia-validator)
- [unknownutil Validator](https://github.com/ryoppippi/hono-unknownutil-validator)
- [Valibot Validator](https://github.com/honojs/middleware/tree/main/packages/valibot-validator)
- [Zod Validator](https://github.com/honojs/middleware/tree/main/packages/zod-validator)

### OpenAPI​

- [Zod OpenAPI](https://github.com/honojs/middleware/tree/main/packages/zod-openapi)
- [Scalar](https://github.com/scalar/scalar/tree/main/integrations/hono)
- [Swagger UI](https://github.com/honojs/middleware/tree/main/packages/swagger-ui)
- [Swagger Editor](https://github.com/honojs/middleware/tree/main/packages/swagger-editor)
- [Hono OpenAPI](https://github.com/rhinobase/hono-openapi)
- [hono-zod-openapi](https://github.com/paolostyle/hono-zod-openapi)

### Development​

- [ESLint Config](https://github.com/honojs/middleware/tree/main/packages/eslint-config)
- [SSG Plugin Essential](https://github.com/honojs/middleware/tree/main/packages/ssg-plugins-essential)

### Monitoring / Tracing​

- [Apitally (API monitoring & analytics)](https://docs.apitally.io/frameworks/hono)
- [Highlight.io](https://www.highlight.io/docs/getting-started/backend-sdk/js/hono)
- [LogTape (Logging)](https://logtape.org/manual/integrations#hono)
- [OpenTelemetry](https://github.com/honojs/middleware/tree/main/packages/otel)
- [Prometheus Metrics](https://github.com/honojs/middleware/tree/main/packages/prometheus)
- [Sentry](https://github.com/honojs/middleware/tree/main/packages/sentry)

### Server / Adapter​

- [GraphQL Server](https://github.com/honojs/middleware/tree/main/packages/graphql-server)
- [Node WebSocket Helper](https://github.com/honojs/middleware/tree/main/packages/node-ws)
- [tRPC Server](https://github.com/honojs/middleware/tree/main/packages/trpc-server)

### Transpiler​

- [Bun Transpiler](https://github.com/honojs/middleware/tree/main/packages/bun-transpiler)
- [esbuild Transpiler](https://github.com/honojs/middleware/tree/main/packages/esbuild-transpiler)

### UI / Renderer​

- [Qwik City](https://github.com/honojs/middleware/tree/main/packages/qwik-city)
- [React Compatibility](https://github.com/honojs/middleware/tree/main/packages/react-compat)
- [React Renderer](https://github.com/honojs/middleware/tree/main/packages/react-renderer)

### Utilities​

- [Bun Compress](https://github.com/honojs/middleware/tree/main/packages/bun-compress)
- [Cap Checkpoint](https://capjs.js.org/guide/middleware/hono.html)
- [Event Emitter](https://github.com/honojs/middleware/tree/main/packages/event-emitter)
- [Geo](https://github.com/ktkongtong/hono-geo-middleware/tree/main/packages/middleware)
- [Hono Rate Limiter](https://github.com/rhinobase/hono-rate-limiter)
- [Hono Simple DI](https://github.com/maou-shonen/hono-simple-DI)
- [jsonv-ts (Validator, OpenAPI, MCP)](https://github.com/dswbx/jsonv-ts)
- [MCP](https://github.com/honojs/middleware/tree/main/packages/mcp)
- [RONIN (Database)](https://github.com/ronin-co/hono-client)
- [Session](https://github.com/honojs/middleware/tree/main/packages/session)
- [tsyringe](https://github.com/honojs/middleware/tree/main/packages/tsyringe)
- [User Agent based Blocker](https://github.com/honojs/middleware/tree/main/packages/ua-blocker)
