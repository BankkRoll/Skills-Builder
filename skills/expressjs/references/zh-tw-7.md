# 移至 Express 5 and more

# 移至 Express 5

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# 移至 Express 5

## 概觀

Express 5 與 Express 4 之間差異不大：API 的變更不會像從 3.0 至 4.0 那樣顯著。雖然基本 API 維持相同，仍有一些突破性變更；換句話說，如果您更新成使用 Express 5，現有 Express 4 程式可能無法運作。 Therefore, an application built with Express 4 might not work if you update it to use Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

然後您可以執行自動化測試，查看失敗之處，並根據下方列出的更新項目來修正問題。解決測試失敗之後，請執行您的應用程式，查看發生哪些錯誤。只要應用程式使用任何不支援的方法或內容，您會馬上發現。 After addressing test failures, run your app to see what errors occur. You’ll find out right away if the app uses any methods or properties that are not supported.

## Express 5 Codemods

To help you migrate your express server, we have created a set of codemods that will help you automatically update your code to the latest version of Express.

Run the following command for run all the codemods available:

```
npx codemod@latest @expressjs/v5-migration-recipe
```

If you want to run a specific codemod, you can run the following command:

```
npx codemod@latest @expressjs/name-of-the-codemod
```

You can find the list of available codemods [here](https://codemod.link/express).

## Express 5 中的變更

**已移除的方法和內容**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [複數化的方法名稱](#plural)
- [Leading colon in name argument to app.param(name, fn)](#leading)
- [req.param(name)](#req.param)
- [res.json(obj, status)](#res.json)
- [res.jsonp(obj, status)](#res.jsonp)
- [res.redirect('back') and res.location('back')](#magic-redirect)
- [res.redirect(url, status)](#res.redirect)
- [res.send(body, status)](#res.send.body)
- [res.send(status)](#res.send.status)
- [res.sendfile()](#res.sendfile)
- [router.param(fn)](#router.param)
- [express.static.mime](#express.static.mime)
- [express:router debug logs](#express:router-debug-logs)

**改良**

- [Path route matching syntax](#path-syntax)
- [Rejected promises handled from middleware and handlers](#rejected-promises)
- [express.urlencoded](#express.urlencoded)
- [express.static dotfiles](#express.static.dotfiles)
- [app.param(name, fn) 名稱引數中的前導冒號](#leading)
- [app.router](#app.router)
- [req.body](#req.body)
- [req.host](#req.host)
- [req.params](#req.params)
- [req.query](#req.query)
- [res.clearCookie](#res.clearCookie)
- [res.status](#res.status)
- [res.vary](#res.vary)

**已變更**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## 已移除的方法和內容

If you use any of these methods or properties in your app, it will crash. So, you’ll need to change your app after you update to version 5.

### app.del()

Express 5 no longer supports the `app.del()` function. If you use this function, an error is thrown. For registering HTTP DELETE routes, use the `app.delete()` function instead.

最初是使用 `del` 而非 `delete`，因為 `delete` 是 JavaScript 中的保留關鍵字。不過，從 ECMAScript 6 起，`delete` 和其他保留關鍵字可以合法作為內容名稱。您可以在這裡閱讀導致淘汰 `app.del` 函數的相關討論。 However, as of ECMAScript 6, `delete` and other reserved keywords can legally be used as property names.

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/route-del-to-delete
```

```
// v4
app.del('/user/:id', (req, res) => {
  res.send(`DELETE /user/${req.params.id}`)
})

// v5
app.delete('/user/:id', (req, res) => {
  res.send(`DELETE /user/${req.params.id}`)
})
```

### app.param(fn)

The `app.param(fn)` signature was used for modifying the behavior of the `app.param(name, fn)` function. It has been deprecated since v4.11.0, and Express 5 no longer supports it at all.

### Pluralized method names

The following method names have been pluralized. In Express 4, using the old methods resulted in a deprecation warning. Express 5 no longer supports them at all:

`req.acceptsLanguage()` 以 `req.acceptsLanguages()` 取代。

`req.acceptsCharset()` 以 `req.acceptsCharsets()` 取代。

`req.acceptsEncoding()` 以 `req.acceptsEncodings()` 取代。

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/pluralize-method-names
```

```
// v4
app.all('/', (req, res) => {
  req.acceptsCharset('utf-8')
  req.acceptsEncoding('br')
  req.acceptsLanguage('en')

  // ...
})

// v5
app.all('/', (req, res) => {
  req.acceptsCharsets('utf-8')
  req.acceptsEncodings('br')
  req.acceptsLanguages('en')

  // ...
})
```

### app.param(name, fn) 名稱中的前導冒號 (:)

`app.param(name, fn)` 函數名稱中的前導冒號字元 (:) 遺留自 Express 3，基於舊版相容性，Express 4 仍支援它，只是會發出淘汰警示。Express 5 會無聲自動忽略它，並使用少了冒號字首的名稱參數。 Express 5 will silently ignore it and use the name parameter without prefixing it with a colon.

如果您遵循 Express 4 [app.param](https://expressjs.com/zh-tw/4x/api.html#app.param) 說明文件，應該不會影響您的程式碼，因為該說明文件不會提及前導冒號。

### req.param(name)

This potentially confusing and dangerous method of retrieving form data has been removed. You will now need to specifically look for the submitted parameter name in the `req.params`, `req.body`, or `req.query` object.

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/explicit-request-params
```

```
// v4
app.post('/user', (req, res) => {
  const id = req.param('id')
  const body = req.param('body')
  const query = req.param('query')

  // ...
})

// v5
app.post('/user', (req, res) => {
  const id = req.params.id
  const body = req.body
  const query = req.query

  // ...
})
```

### res.json(obj, status)

Express 5 不再支援 `res.json(obj, status)` 簽章。請改以設定狀態，然後與 `res.json()` 方法鏈接，如下所示：`res.status(status).json(obj)`。 Instead, set the status and then chain it to the `res.json()` method like this: `res.status(status).json(obj)`.

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```

```
// v4
app.post('/user', (req, res) => {
  res.json({ name: 'Ruben' }, 201)
})

// v5
app.post('/user', (req, res) => {
  res.status(201).json({ name: 'Ruben' })
})
```

### res.jsonp(obj, status)

Express 5 不再支援 `res.jsonp(obj, status)` 簽章。請改以設定狀態，然後與 `res.jsonp()` 方法鏈接，如下所示：`res.status(status).jsonp(obj)`。 Instead, set the status and then chain it to the `res.jsonp()` method like this: `res.status(status).jsonp(obj)`.

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```

```
// v4
app.post('/user', (req, res) => {
  res.jsonp({ name: 'Ruben' }, 201)
})

// v5
app.post('/user', (req, res) => {
  res.status(201).jsonp({ name: 'Ruben' })
})
```

### res.redirect(url, status)

Express 5 no longer supports the signature `res.redirect(url, status)`. Instead, use the following signature: `res.redirect(status, url)`.

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/redirect-arg-order
```

```
// v4
app.get('/user', (req, res) => {
  res.redirect('/users', 301)
})

// v5
app.get('/user', (req, res) => {
  res.redirect(301, '/users')
})
```

### res.redirect('back') and res.location('back')

Express 5 no longer supports the magic string `back` in the `res.redirect()` and `res.location()` methods. Instead, use the `req.get('Referrer') || '/'` value to redirect back to the previous page. In Express 4, the `res.redirect('back')` and `res.location('back')` methods were deprecated.

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/back-redirect-deprecated
```

```
// v4
app.get('/user', (req, res) => {
  res.redirect('back')
})

// v5
app.get('/user', (req, res) => {
  res.redirect(req.get('Referrer') || '/')
})
```

### res.send(body, status)

Express 5 不再支援 `res.send(obj, status)` 簽章。請改以設定狀態，然後與 `res.send()` 方法鏈接，如下所示：`res.status(status).send(obj)`。 Instead, set the status and then chain it to the `res.send()` method like this: `res.status(status).send(obj)`.

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```

```
// v4
app.get('/user', (req, res) => {
  res.send({ name: 'Ruben' }, 200)
})

// v5
app.get('/user', (req, res) => {
  res.status(200).send({ name: 'Ruben' })
})
```

### res.send(status)

Express 5 不再支援 `res.send(status)` 簽章，其中 *status* 是數字。請改用 `res.sendStatus(statusCode)` 函數，此函數是設定 HTTP 回應標頭狀態碼，並傳送文字版的程式碼：「找不到」、「內部伺服器錯誤」等。
如果您需要使用 `res.send()` 函數來傳送數字，請將數字括上引號來轉換成字串，這樣 Express 就不會解譯它以試圖使用不支援的舊簽章。 Instead, use the `res.sendStatus(statusCode)` function, which sets the HTTP response header status code and sends the text version of the code: “Not Found”, “Internal Server Error”, and so on.
If you need to send a number by using the `res.send()` function, quote the number to convert it to a string, so that Express does not interpret it as an attempt to use the unsupported old signature.

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```

```
// v4
app.get('/user', (req, res) => {
  res.send(200)
})

// v5
app.get('/user', (req, res) => {
  res.sendStatus(200)
})
```

### res.sendfile()

`res.sendfile()` 函數已被 Express 5 中的駝峰式大小寫版本 `res.sendFile()` 取代。

**Note:** In Express 5, `res.sendFile()` uses the `mime-types` package for MIME type detection, which returns different Content-Type values than Express 4 for several common file types:

- JavaScript files (.js): now “text/javascript” instead of “application/javascript”
- JSON files (.json): now “application/json” instead of “text/json”
- CSS files (.css): now “text/css” instead of “text/plain”
- XML files (.xml): now “application/xml” instead of “text/xml”
- Font files (.woff): now “font/woff” instead of “application/font-woff”
- SVG files (.svg): now “image/svg+xml” instead of “application/svg+xml”

Note

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/camelcase-sendfile
```

```
// v4
app.get('/user', (req, res) => {
  res.sendfile('/path/to/file')
})

// v5
app.get('/user', (req, res) => {
  res.sendFile('/path/to/file')
})
```

### router.param(fn)

The `router.param(fn)` signature was used for modifying the behavior of the `router.param(name, fn)` function. It has been deprecated since v4.11.0, and Express 5 no longer supports it at all.

### express.static.mime

In Express 5, `mime` is no longer an exported property of the `static` field.
Use the [mime-typespackage](https://github.com/jshttp/mime-types) to work with MIME type values.

**Important:** This change affects not only direct usage of `express.static.mime` but also other Express methods that rely on MIME type detection, such as `res.sendFile()`. The following MIME types have changed from Express 4:

- JavaScript files (.js): now served as “text/javascript” instead of “application/javascript”
- JSON files (.json): now served as “application/json” instead of “text/json”
- CSS files (.css): now served as “text/css” instead of “text/plain”
- HTML files (.html): now served as “text/html; charset=utf-8” instead of just “text/html”
- XML files (.xml): now served as “application/xml” instead of “text/xml”
- Font files (.woff): now served as “font/woff” instead of “application/font-woff”

```
// v4
express.static.mime.lookup('json')

// v5
const mime = require('mime-types')
mime.lookup('json')
```

### express:router debug logs

In Express 5, router handling logic is performed by a dependency. Therefore, the
debug logs for the router are no longer available under the `express:` namespace.
In v4, the logs were available under the namespaces `express:router`, `express:router:layer`,
and `express:router:route`. All of these were included under the namespace `express:*`.
In v5.1+, the logs are available under the namespaces `router`, `router:layer`, and `router:route`.
The logs from `router:layer` and `router:route` are included in the namespace `router:*`.
To achieve the same detail of debug logging when using `express:*` in v4, use a conjunction of
`express:*`, `router`, and `router:*`.

```
# v4
DEBUG=express:* node index.js

# v5
DEBUG=express:*,router,router:* node index.js
```

## 已變更

### Path route matching syntax

Path route matching syntax is when a string is supplied as the first parameter to the `app.all()`, `app.use()`, `app.METHOD()`, `router.all()`, `router.METHOD()`, and `router.use()` APIs. The following changes have been made to how the path string is matched to an incoming request:

- The wildcard `*` must have a name, matching the behavior of parameters `:`, use `/*splat` instead of `/*`

```
// v4
app.get('/*', async (req, res) => {
  res.send('ok')
})

// v5
app.get('/*splat', async (req, res) => {
  res.send('ok')
})
```

Note

`*splat` matches any path without the root path. If you need to match the root path as well `/`, you can use `/{*splat}`, wrapping the wildcard in braces.

```
// v5
app.get('/{*splat}', async (req, res) => {
  res.send('ok')
})
```

- The optional character `?` is no longer supported, use braces instead.

```
// v4
app.get('/:file.:ext?', async (req, res) => {
  res.send('ok')
})

// v5
app.get('/:file{.:ext}', async (req, res) => {
  res.send('ok')
})
```

- Regexp characters are not supported. For example:

```
app.get('/[discussion|page]/:slug', async (req, res) => {
  res.status(200).send('ok')
})
```

should be changed to:

```
app.get(['/discussion/:slug', '/page/:slug'], async (req, res) => {
  res.status(200).send('ok')
})
```

- Some characters have been reserved to avoid confusion during upgrade (`()[]?+!`), use `\` to escape them.
- Parameter names now support valid JavaScript identifiers, or quoted like `:"this"`.

### Rejected promises handled from middleware and handlers

Request middleware and handlers that return rejected promises are now handled by forwarding the rejected value as an `Error` to the error handling middleware. This means that using `async` functions as middleware and handlers are easier than ever. When an error is thrown in an `async` function or a rejected promise is `await`ed inside an async function, those errors will be passed to the error handler as if calling `next(err)`.

Details of how Express handles errors is covered in the [error handling documentation](https://expressjs.com/en/guide/error-handling.html).

### express.urlencoded

The `express.urlencoded` method makes the `extended` option `false` by default.

### express.static dotfiles

In Express 5, the `express.static` middleware’s `dotfiles` option now defaults to `"ignore"`. This is a change from Express 4, where dotfiles were served by default. As a result, files inside a directory that starts with a dot (`.`), such as `.well-known`, will no longer be accessible and will return a **404 Not Found** error. This can break functionality that depends on serving dot-directories, such as Android App Links, and Apple Universal Links.

Example of breaking code:

```
// v4
app.use(express.static('public'))
```

After migrating to Express 5, a request to `/.well-known/assetlinks.json` will result in a **404 Not Found**.

To fix this, serve specific dot-directories explicitly using the `dotfiles: "allow"` option:

```
// v5
app.use('/.well-known', express.static('public/.well-known', { dotfiles: 'allow' }))
app.use(express.static('public'))
```

This approach allows you to safely serve only the intended dot-directories while keeping the default secure behavior for other dotfiles, which remain inaccessible.

### app.listen

In Express 5, the `app.listen` method will invoke the user-provided callback function (if provided) when the server receives an error event. In Express 4, such errors would be thrown. This change shifts error-handling responsibility to the callback function in Express 5. If there is an error, it will be passed to the callback as an argument.
For example:

```
const server = app.listen(8080, '0.0.0.0', (error) => {
  if (error) {
    throw error // e.g. EADDRINUSE
  }
  console.log(`Listening on ${JSON.stringify(server.address())}`)
})
```

### app.router

`app.router` 物件已在 Express 4 中移除，在 Express 5 中又重新納入。
在新版本中，這個物件只用來參照至基本 Express 路由器，不像在 Express 3 中，應用程式還得明確載入它。 In the new version, this object is a just a reference to the base Express router, unlike in Express 3, where an app had to explicitly load it.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

In Express 4, the `req.host` function incorrectly stripped off the port number if it was present. In Express 5, the port number is maintained.

### req.params

The `req.params` object now has a **null prototype** when using string paths. However, if the path is defined with a regular expression, `req.params` remains a standard object with a normal prototype. Additionally, there are two important behavioral changes:

**Wildcard parameters are now arrays:**

Wildcards (e.g., `/*splat`) capture path segments as an array instead of a single string.

```
app.get('/*splat', (req, res) => {
  // GET /foo/bar
  console.dir(req.params)
  // => [Object: null prototype] { splat: [ 'foo', 'bar' ] }
})
```

**Unmatched parameters are omitted:**

In Express 4, unmatched wildcards were empty strings (`''`) and optional `:` parameters (using `?`) had a key with value `undefined`. In Express 5, unmatched parameters are completely omitted from `req.params`.

```
// v4: unmatched wildcard is empty string
app.get('/*', (req, res) => {
  // GET /
  console.dir(req.params)
  // => { '0': '' }
})

// v4: unmatched optional param is undefined
app.get('/:file.:ext?', (req, res) => {
  // GET /image
  console.dir(req.params)
  // => { file: 'image', ext: undefined }
})

// v5: unmatched optional param is omitted
app.get('/:file{.:ext}', (req, res) => {
  // GET /image
  console.dir(req.params)
  // => [Object: null prototype] { file: 'image' }
})
```

### req.query

The `req.query` property is no longer a writable property and is instead a getter. The default query parser has been changed from “extended” to “simple”.

### res.clearCookie

The `res.clearCookie` method ignores the `maxAge` and `expires` options provided by the user.

### res.status

The `res.status` method only accepts integers in the range of `100` to `999`, following the behavior defined by Node.js, and it returns an error when the status code is not an integer.

### res.vary

The `res.vary` throws an error when the `field` argument is missing. In Express 4, if the argument was omitted, it gave a warning in the console

## 改良

### res.render()

此方法現在會針對所有視圖引擎施行非同步行為，可避免採行同步實作及違反建議介面的視圖引擎所造成的錯誤。

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/migrating-5.md          )

---

# Overriding the Express API

> Discover how to customize and extend the Express.js API by overriding methods and properties on the request and response objects using prototypes.

# Overriding the Express API

The Express API consists of various methods and properties on the request and response objects. These are inherited by prototype. There are two extension points for the Express API:

1. The global prototypes at `express.request` and `express.response`.
2. App-specific prototypes at `app.request` and `app.response`.

Altering the global prototypes will affect all loaded Express apps in the same process. If desired, alterations can be made app-specific by only altering the app-specific prototypes after creating a new app.

## Methods

You can override the signature and behavior of existing methods with your own, by assigning a custom function.

Following is an example of overriding the behavior of [res.sendStatus](https://expressjs.com/4x/api.html#res.sendStatus).

```
app.response.sendStatus = function (statusCode, type, message) {
  // code is intentionally kept simple for demonstration purpose
  return this.contentType(type)
    .status(statusCode)
    .send(message)
}
```

The above implementation completely changes the original signature of `res.sendStatus`. It now accepts a status code, encoding type, and the message to be sent to the client.

The overridden method may now be used this way:

```
res.sendStatus(404, 'application/json', '{"error":"resource not found"}')
```

## Properties

Properties in the Express API are either:

1. Assigned properties (ex: `req.baseUrl`, `req.originalUrl`)
2. Defined as getters (ex: `req.secure`, `req.ip`)

Since properties under category 1 are dynamically assigned on the `request` and `response` objects in the context of the current request-response cycle, their behavior cannot be overridden.

Properties under category 2 can be overwritten using the Express API extensions API.

The following code rewrites how the value of `req.ip` is to be derived. Now, it simply returns the value of the `Client-IP` request header.

```
Object.defineProperty(app.request, 'ip', {
  configurable: true,
  enumerable: true,
  get () { return this.get('Client-IP') }
})
```

## Prototype

In order to provide the Express API, the request/response objects passed to Express (via `app(req, res)`, for example) need to inherit from the same prototype chain. By default, this is `http.IncomingRequest.prototype` for the request and `http.ServerResponse.prototype` for the response.

Unless necessary, it is recommended that this be done only at the application level, rather than globally. Also, take care that the prototype that is being used matches the functionality as closely as possible to the default prototypes.

```
// Use FakeRequest and FakeResponse in place of http.IncomingRequest and http.ServerResponse
// for the given app reference
Object.setPrototypeOf(Object.getPrototypeOf(app.request), FakeRequest.prototype)
Object.setPrototypeOf(Object.getPrototypeOf(app.response), FakeResponse.prototype)
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/overriding-express-api.md          )

---

# 路由

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# 路由

*Routing* refers to how an application’s endpoints (URIs) respond to client requests.
For an introduction to routing, see [Basic routing](https://expressjs.com/zh-tw/starter/basic-routing.html).

You define routing using methods of the Express `app` object that correspond to HTTP methods;
for example, `app.get()` to handle GET requests and `app.post` to handle POST requests. For a full list,
see [app.METHOD](https://expressjs.com/zh-tw/5x/api.html#app.METHOD). You can also use [app.all()](https://expressjs.com/zh-tw/5x/api.html#app.all) to handle all HTTP methods and [app.use()](https://expressjs.com/zh-tw/5x/api.html#app.use) to
specify middleware as the callback function (See [Using middleware](https://expressjs.com/zh-tw/guide/using-middleware.html) for details).

These routing methods specify a callback function (sometimes called “handler functions”) called when the application receives a request to the specified route (endpoint) and HTTP method. In other words, the application “listens” for requests that match the specified route(s) and method(s), and when it detects a match, it calls the specified callback function.

In fact, the routing methods can have more than one callback function as arguments.
With multiple callback functions, it is important to provide `next` as an argument to the callback function and then call `next()` within the body of the function to hand off control
to the next callback.

以下是以字串為基礎的部分路由路徑範例。

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## 路由方法

路由方法衍生自其中一個 HTTP 方法，並且會附加到 `express` 類別的實例中。

下列程式碼範例說明對應用程式根目錄提出 GET 和 POST 方法時所定義的路由。

```
// GET method route
app.get('/', (req, res) => {
  res.send('GET request to the homepage')
})

// POST method route
app.post('/', (req, res) => {
  res.send('POST request to the homepage')
})
```

Express supports methods that correspond to all HTTP request methods: `get`, `post`, and so on.
For a full list, see [app.METHOD](https://expressjs.com/zh-tw/5x/api.html#app.METHOD).

`app.all()` 是一個特殊的路由方法，它不是衍生自任何 HTTP 方法。此方法用來在所有要求方法的路徑中載入中介軟體函數。 在下列範例中，不論您使用的是 GET、POST、PUT、DELETE 或 [http 模組](https://nodejs.org/api/http.html#http_http_methods)中支援的其他任何 HTTP 要求方法，都會針對傳給 “/secret” 的要求執行處理程式。

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## 路由路徑

Route paths, in combination with a request method, define the endpoints at which requests can be made. Route paths can be strings, string patterns, or regular expressions.

Caution

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/zh-tw/guide/migrating-5.html#path-syntax) for more information.

Caution

In express 4, regular expression characters such as `$` need to be escaped with a `\`.

Note

Express uses [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) for matching the route paths; see the path-to-regexp documentation for all the possibilities in defining route paths. [Express Playground Router](https://bjohansebas.github.io/playground-router/) is a handy tool for testing basic Express routes, although it does not support pattern matching.

Warning

Query strings are not part of the route path.

### Route paths based on strings

This route path will match requests to the root route, `/`.

```
app.get('/', (req, res) => {
  res.send('root')
})
```

This route path will match requests to `/about`.

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

此路由路徑將符合傳送給 `/random.text` 的要求。

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### Route paths based on string patterns

Caution

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/zh-tw/guide/migrating-5.html#path-syntax) for more information.

此路由路徑將符合 `acd` 和 `abcd`。

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

此路由路徑將符合 `abcd`、`abbcd`、`abbbcd` 等。

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

此路由路徑將符合 `abcd`、`abxcd`、`abRABDOMcd`、`ab123cd` 等。

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

此路由路徑將符合 `/abe` 和 `/abcde`。

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### 以正規表示式為基礎的路由路徑範例：

This route path will match anything with an “a” in it.

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

此路由路徑將符合 `butterfly` 和 `dragonfly`，但不符合 `butterflyman`、`dragonfly man` 等。

```
app.get(/.*fly$/, (req, res) => {
  res.send('/.*fly$/')
})
```

## 當路由路徑配上要求方法時，即定義了發出要求時的目標端點。路由路徑可以是字串、字串型樣或正規表示式。

Route parameters are named URL segments that are used to capture the values specified at their position in the URL. The captured values are populated in the `req.params` object, with the name of the route parameter specified in the path as their respective keys.

```
Route path: /users/:userId/books/:bookId
Request URL: http://localhost:3000/users/34/books/8989
req.params: { "userId": "34", "bookId": "8989" }
```

To define routes with route parameters, simply specify the route parameters in the path of the route as shown below.

```
app.get('/users/:userId/books/:bookId', (req, res) => {
  res.send(req.params)
})
```

The name of route parameters must be made up of “word characters” ([A-Za-z0-9_]).

Since the hyphen (`-`) and the dot (`.`) are interpreted literally, they can be used along with route parameters for useful purposes.

```
Route path: /flights/:from-:to
Request URL: http://localhost:3000/flights/LAX-SFO
req.params: { "from": "LAX", "to": "SFO" }
```

```
Route path: /plantae/:genus.:species
Request URL: http://localhost:3000/plantae/Prunus.persica
req.params: { "genus": "Prunus", "species": "persica" }
```

Caution

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/zh-tw/guide/migrating-5.html#path-syntax).

To have more control over the exact string that can be matched by a route parameter, you can append a regular expression in parentheses (`()`):

```
Route path: /user/:userId(\d+)
Request URL: http://localhost:3000/user/42
req.params: {"userId": "42"}
```

Warning

Because the regular expression is usually part of a literal string, be sure to escape any `\` characters with an additional backslash, for example `\\d+`.

Warning

In Express 4.x, [the*character in regular expressions is not interpreted in the usual way](https://github.com/expressjs/express/issues/2495). As a workaround, use `{0,}` instead of `*`. This will likely be fixed in Express 5.

## Route handlers

You can provide multiple callback functions that behave like [middleware](https://expressjs.com/zh-tw/guide/using-middleware.html) to handle a request. The only exception is that these callbacks might invoke `next('route')` to bypass the remaining route callbacks. You can use this mechanism to impose pre-conditions on a route, then pass control to subsequent routes if there’s no reason to proceed with the current route.

```
app.get('/user/:id', (req, res, next) => {
  if (req.params.id === '0') {
    return next('route')
  }
  res.send(`User ${req.params.id}`)
})

app.get('/user/:id', (req, res) => {
  res.send('Special handler for user ID 0')
})
```

In this example:

- `GET /user/5` → handled by first route → sends “User 5”
- `GET /user/0` → first route calls `next('route')`, skipping to the next matching `/user/:id` route

Route handlers can be in the form of a function, an array of functions, or combinations of both, as shown in the following examples.

A single callback function can handle a route. For example:

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

More than one callback function can handle a route (make sure you specify the `next` object). For example:

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

An array of callback functions can handle a route. For example:

```
const cb0 = function (req, res, next) {
  console.log('CB0')
  next()
}

const cb1 = function (req, res, next) {
  console.log('CB1')
  next()
}

const cb2 = function (req, res) {
  res.send('Hello from C!')
}

app.get('/example/c', [cb0, cb1, cb2])
```

A combination of independent functions and arrays of functions can handle a route. For example:

```
const cb0 = function (req, res, next) {
  console.log('CB0')
  next()
}

const cb1 = function (req, res, next) {
  console.log('CB1')
  next()
}

app.get('/example/d', [cb0, cb1], (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from D!')
})
```

## 回應方法

The methods on the response object (`res`) in the following table can send a response to the client, and terminate the request-response cycle. If none of these methods are called from a route handler, the client request will be left hanging.

| 方法 | Description |
| --- | --- |
| res.download() | 提示您提供要下載的檔案。 |
| res.end() | End the response process. |
| res.json() | 傳送 JSON 回應。 |
| res.jsonp() | 傳送 JSON 回應，並支援 JSONP。 |
| res.redirect() | 將要求重新導向。 |
| res.render() | Render a view template. |
| res.send() | 傳送各種類型的回應。 |
| res.sendFile() | 以八位元組串流形式傳送檔案。 |
| res.sendStatus() | Set the response status code and send its string representation as the response body. |

## app.route()

您可以使用 `app.route()`，來為路由路徑建立可鏈接的路由處理程式。
由於是在單一位置指定路徑，建立模組路由很有用，因為它可減少冗餘和打錯字的情況。如需路由的相關資訊，請參閱 [Router() 說明文件](https://expressjs.com/zh-tw/4x/api.html#router)。
Because the path is specified at a single location, creating modular routes is helpful, as is reducing redundancy and typos. For more information about routes, see: [Router() documentation](https://expressjs.com/zh-tw/5x/api.html#router).

下列範例顯示利用 `app.route()` 所定義的路由處理程式鏈。

```
app.route('/book')
  .get((req, res) => {
    res.send('Get a random book')
  })
  .post((req, res) => {
    res.send('Add a book')
  })
  .put((req, res) => {
    res.send('Update the book')
  })
```

## express.Router

Use the `express.Router` class to create modular, mountable route handlers. A `Router` instance is a complete middleware and routing system; for this reason, it is often referred to as a “mini-app”.

The following example creates a router as a module, loads a middleware function in it, defines some routes, and mounts the router module on a path in the main app.

在應用程式目錄中建立一個名為 `birds.js` 的路由器檔案，內含下列內容：

```
const express = require('express')
const router = express.Router()

// middleware that is specific to this router
const timeLog = (req, res, next) => {
  console.log('Time: ', Date.now())
  next()
}
router.use(timeLog)

// define the home page route
router.get('/', (req, res) => {
  res.send('Birds home page')
})
// define the about route
router.get('/about', (req, res) => {
  res.send('About birds')
})

module.exports = router
```

然後將路由器模組載入應用程式中：

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

現在，應用程式就能夠處理發給 `/birds` 和 `/birds/about` 的要求，並且呼叫該路由特定的 `timeLog` 中介軟體函數。

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/zh-tw/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/routing.md          )

---

# 使用中介軟體

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# 使用中介軟體

Express 是一個本身功能極簡的路由與中介軟體 Web 架構：本質上，Express 應用程式是一系列的中介軟體函數呼叫。

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/zh-tw/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/zh-tw/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. The next middleware function is commonly denoted by a variable named `next`.

Middleware functions can perform the following tasks:

- 執行任何程式碼。
- Make changes to the request and the response objects.
- End the request-response cycle.
- Call the next middleware function in the stack.

If the current middleware function does not end the request-response cycle, it must call `next()` to pass control to the next middleware function. Otherwise, the request will be left hanging.

Express 應用程式可以使用下列類型的中介軟體：

- [應用程式層次的中介軟體](#middleware.application)
- [路由器層次的中介軟體](#middleware.router)
- [錯誤處理中介軟體](#middleware.error-handling)
- [內建中介軟體](#middleware.built-in)
- [協力廠商中介軟體](#middleware.third-party)

You can load application-level and router-level middleware with an optional mount path.
You can also load a series of middleware functions together, which creates a sub-stack of the middleware system at a mount point.

## 應用程式層次的中介軟體

Bind application-level middleware to an instance of the [app object](https://expressjs.com/zh-tw/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

This example shows a middleware function with no mount path. The function is executed every time the app receives a request.

```
const express = require('express')
const app = express()

app.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})
```

This example shows a middleware function mounted on the `/user/:id` path. The function is executed for any type of
HTTP request on the `/user/:id` path.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

This example shows a route and its handler function (middleware system). The function handles GET requests to the `/user/:id` path.

```
app.get('/user/:id', (req, res, next) => {
  res.send('USER')
})
```

Here is an example of loading a series of middleware functions at a mount point, with a mount path.
It illustrates a middleware sub-stack that prints request info for any type of HTTP request to the `/user/:id` path.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Route handlers enable you to define multiple routes for a path. The example below defines two routes for GET requests to the `/user/:id` path. The second route will not cause any problems, but it will never get called because the first route ends the request-response cycle.

本例顯示中介軟體子堆疊，它處理了指向 `/user/:id` 路徑的 GET 要求。

```
app.get('/user/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
}, (req, res, next) => {
  res.send('User Info')
})

// handler for the /user/:id path, which prints the user ID
app.get('/user/:id', (req, res, next) => {
  res.send(req.params.id)
})
```

To skip the rest of the middleware functions from a router middleware stack, call `next('route')` to pass control to the next route.

Note

`next('route')` will work only in middleware functions that were loaded by using the `app.METHOD()` or `router.METHOD()` functions.

本例顯示中介軟體子堆疊，它處理了指向 `/user/:id` 路徑的 GET 要求。

```
app.get('/user/:id', (req, res, next) => {
  // if the user ID is 0, skip to the next route
  if (req.params.id === '0') next('route')
  // otherwise pass the control to the next middleware function in this stack
  else next()
}, (req, res, next) => {
  // send a regular response
  res.send('regular')
})

// handler for the /user/:id path, which sends a special response
app.get('/user/:id', (req, res, next) => {
  res.send('special')
})
```

Middleware can also be declared in an array for reusability.

本例顯示裝載在 `/user/:id` 路徑的中介軟體函數。會對 `/user/:id` 路徑上任何類型的 HTTP 要求，執行此函數。

```
function logOriginalUrl (req, res, next) {
  console.log('Request URL:', req.originalUrl)
  next()
}

function logMethod (req, res, next) {
  console.log('Request Type:', req.method)
  next()
}

const logStuff = [logOriginalUrl, logMethod]
app.get('/user/:id', logStuff, (req, res, next) => {
  res.send('User Info')
})
```

## 路由器層次的中介軟體

路由器層次的中介軟體的運作方式如同應用程式層次的中介軟體，不同之處在於它會連結至 `express.Router()` 實例。

```
const router = express.Router()
```

請利用 `router.use()` 和 `router.METHOD()` 函數來載入路由器層次的中介軟體。

下列的程式碼範例是使用路由器層次的中介軟體，抄寫上述針對應用程式層次的中介軟體顯示的中介軟體系統：

```
const express = require('express')
const app = express()
const router = express.Router()

// a middleware function with no mount path. This code is executed for every request to the router
router.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})

// a middleware sub-stack shows request info for any type of HTTP request to the /user/:id path
router.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})

// a middleware sub-stack that handles GET requests to the /user/:id path
router.get('/user/:id', (req, res, next) => {
  // if the user ID is 0, skip to the next router
  if (req.params.id === '0') next('route')
  // otherwise pass control to the next middleware function in this stack
  else next()
}, (req, res, next) => {
  // render a regular page
  res.render('regular')
})

// handler for the /user/:id path, which renders a special page
router.get('/user/:id', (req, res, next) => {
  console.log(req.params.id)
  res.render('special')
})

// mount the router on the app
app.use('/', router)
```

To skip the rest of the router’s middleware functions, call `next('router')`
to pass control back out of the router instance.

本例顯示中介軟體子堆疊，它處理了指向 `/user/:id` 路徑的 GET 要求。

```
const express = require('express')
const app = express()
const router = express.Router()

// predicate the router with a check and bail out when needed
router.use((req, res, next) => {
  if (!req.headers['x-auth']) return next('router')
  next()
})

router.get('/user/:id', (req, res) => {
  res.send('hello, user!')
})

// use the router and 401 anything falling through
app.use('/admin', router, (req, res) => {
  res.sendStatus(401)
})
```

## Error-handling middleware

Error-handling middleware always takes *four* arguments. You must provide four arguments to identify it as an error-handling middleware function. Even if you don’t need to use the `next` object, you must specify it to maintain the signature. Otherwise, the `next` object will be interpreted as regular middleware and will fail to handle errors.

Define error-handling middleware functions in the same way as other middleware functions, except with four arguments instead of three, specifically with the signature `(err, req, res, next)`:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

For details about error-handling middleware, see: [Error handling](https://expressjs.com/zh-tw/guide/error-handling.html).

## Built-in middleware

從 4.x 版起，Express 不再相依於 [Connect](https://github.com/senchalabs/connect)。除了 `express.static`，Express 先前隨附的所有中介軟體函數現在位於個別的模組中。請檢視[中介軟體函數清單](https://github.com/senchalabs/connect#middleware)。 The middleware
functions that were previously included with Express are now in separate modules; see [the list of middleware functions](https://github.com/senchalabs/connect#middleware).

Express has the following built-in middleware functions:

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## Third-party middleware

Use third-party middleware to add functionality to Express apps.

針對必要的功能安裝 Node.js 模組，然後在應用程式層次或路由器層次將它載入到您的應用程式中。

下列範例說明如何安裝和載入用來剖析 Cookie 的中介軟體函數 `cookie-parser`。

```
$ npm install cookie-parser
```

```
const express = require('express')
const app = express()
const cookieParser = require('cookie-parser')

// load the cookie-parsing middleware
app.use(cookieParser())
```

For a partial list of third-party middleware functions that are commonly used with Express, see: [Third-party middleware](https://expressjs.com/zh-tw/resources/middleware.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/using-middleware.md          )

---

# 在 Express 中使用模板引擎

> Discover how to integrate and use template engines like Pug, Handlebars, and EJS with Express.js to render dynamic HTML pages efficiently.

# 在 Express 中使用模板引擎

A *template engine* enables you to use static template files in your application. 模板引擎讓您能在應用程式中使用靜態模板檔案。在執行時，模板引擎會將靜態模板檔案中的變數取代為真實的值，並將模板轉換為 HTML 檔案發送至客戶端，這種方法使得設計一個 HTML 頁面變得更加容易。
This approach makes it easier to design an HTML page.

部分主流的模板引擎 [Pug](https://pugjs.org/api/getting-started.html)、[Mustache](https://www.npmjs.com/package/mustache) 和 [EJS](https://www.npmjs.com/package/ejs) 均可被使用於 Express 中。[Express 應用程式產生器](http://expressjs.com/en/starter/generator.html)預設採用 [Jade](https://www.npmjs.com/package/jade)，但也支援包含上述的多種模板引擎。

若要渲染模板檔案，您必須在應用程式產生器產生的 `app.js` 設定以下[應用程式屬性](http://expressjs.com/en/4x/api.html#app.set)：

- `views`, the directory where the template files are located. `views`：範本檔所在的目錄。例如：`app.set('views', './views')`，其預設為應用程式根目錄的 `views` 資料夾。
  This defaults to the `views` directory in the application root directory.
- `view engine`, the template engine to use. `view engine`：要使用的範本引擎，例如若要使用 Pug 模板引擎：`app.set('view engine', 'pug')`

並安裝對應的模板引擎 npm 套件，例如安裝 Pug：

```
$ npm install pug --save
```

與 Express 相容的範本引擎（例如 Pug）會匯出一個名稱是 `__express(filePath, options, callback)` 的函數，以供 `res.render()` 函數呼叫，來呈現範本程式碼。

Some template engines do not follow this convention. 有些範本引擎不遵循這項慣例。[Consolidate.js](https://www.npmjs.org/package/consolidate) 程式庫遵循這項慣例，它會對映所有常見的 Node.js 範本引擎，因此能在 Express 內平順無礙地運作。

在設定模板引擎之後，您不必指定引擎或將範本引擎模組載入到應用程式中；Express 會在內部載入模組，如以下所示（針對上述範例）。

```
app.set('view engine', 'pug')
```

在 `views` 目錄中，建立一個名稱是 `index.pug` 並內含下列內容的 Pug 範本檔：

```pug
html
  head
    title= title
  body
    h1= message
```

Create a route to render the `index.pug` file. If the `view engine` property is not set,
you must specify the extension of the `view` file. Otherwise, you can omit it.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

當您向首頁發出請求時，`index.pug` 檔會以 HTML 被渲染出來。

The view engine cache does not cache the contents of the template’s output, only the underlying template itself. The view is still re-rendered with every request even when the cache is on.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/using-template-engines.md          )
