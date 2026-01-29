# 迁移到 Express 5 and more

# 迁移到 Express 5

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# 迁移到 Express 5

## 概述

Express 5 与 Express 4 的差异不是很大：对 API 的更改不像 3.0 到 4.0 升级那样大刀阔斧。虽然基本 API 保持相同，但仍有一些重大更改；换言之，如果将现有 Express 4 程序更新为使用 Express 5，那么该程序可能无法工作。 Therefore, an application built with Express 4 might not work if you update it to use Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

随后，可以运行自动化测试以查看哪些地方发生故障，然后根据以下列出的更新修复问题。在解决测试故障问题之后，运行应用程序以查看发生哪些错误。如果应用程序使用任何不受支持的方法或属性，您马上就可以发现。 After addressing test failures, run your app to see what errors occur. You’ll find out right away if the app uses any methods or properties that are not supported.

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

## Express 5 中的更改

**已移除的方法和属性**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [复数的方法名称](#plural)
- [app.param(name, fn) 的 name 自变量中的前置冒号](#leading)
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

**改进**

- [Path route matching syntax](#path-syntax)
- [Rejected promises handled from middleware and handlers](#rejected-promises)
- [express.urlencoded](#express.urlencoded)
- [express.static dotfiles](#express.static.dotfiles)
- [app.listen](#app.listen)
- [app.router](#app.router)
- [req.body](#req.body)
- [req.host](#req.host)
- [req.params](#req.params)
- [req.query](#req.query)
- [res.clearCookie](#res.clearCookie)
- [res.status](#res.status)
- [res.vary](#res.vary)

**已更改**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## 已移除的方法和属性

If you use any of these methods or properties in your app, it will crash. So, you’ll need to change your app after you update to version 5.

### app.del()

Express 5 不再支持 `app.del()` 函数。如果使用此函数，将抛出错误。要注册 HTTP DELETE 路由，请使用 `app.delete()` 函数。 If you use this function, an error is thrown. For registering HTTP DELETE routes, use the `app.delete()` function instead.

最初之所以使用 `del` 而不是 `delete`，是因为 `delete` 是 JavaScript 中的保留关键字。但在 ECMAScript 6 时，`delete` 和其他保留关键字可以合法地用作属性名称。您可以在此阅读该讨论，这导致我们在此不推荐使用 `app.del` 函数。 However, as of ECMAScript 6, `delete` and other reserved keywords can legally be used as property names.

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

`app.param(fn)` 特征符用于修改 `app.param(name, fn)` 函数的行为。自 V4.11.0 起不推荐使用该特征符，而 Express 5 完全不再提供支持。 It has been deprecated since v4.11.0, and Express 5 no longer supports it at all.

### 复数的方法名称

The following method names have been pluralized. In Express 4, using the old methods resulted in a deprecation warning. Express 5 no longer supports them at all:

`req.acceptsLanguage()` 由 `req.acceptsLanguages()` 取代。

`req.acceptsCharset()` 由 `req.acceptsCharsets()` 取代。

`req.acceptsEncoding()` 由 `req.acceptsEncodings()` 取代。

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

### app.param(name, fn) 的名称中的前置冒号 (:)

`app.param(name, fn)` 函数名称中的前置冒号字符 (:) 是 Express 3 的遗留问题，为了向后兼容性，Express 4 提供支持但会显示不推荐使用的提醒。而 Express 5 则静默忽略它，使用不带前置冒号的名称参数。 Express 5 will silently ignore it and use the name parameter without prefixing it with a colon.

如果您遵循 [app.param](https://expressjs.com/zh-cn/4x/api.html#app.param) 的 Express 4 文档进行开发，那么不会影响代码，因为文档中没有提及前置冒号。

### req.param(name)

This potentially confusing and dangerous method of retrieving form data has been removed. 已移除用于检索表单数据的方法，因为这可能引起混淆，而且很危险。现在，您需要在 `req.params`、`req.body` 或 `req.query` 对象中专门寻找提交的参数名称。

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

Express 5 不再支持特征符 `res.json(obj, status)`。而是设置状态，然后将其链接到 `res.json()` 方法，如下所示：`res.status(status).json(obj)`。 Instead, set the status and then chain it to the `res.json()` method like this: `res.status(status).json(obj)`.

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

Express 5 不再支持特征符 `res.jsonp(obj, status)`。而是设置状态，然后将其链接到 `res.jsonp()` 方法，如下所示：`res.status(status).jsonp(obj)`。 Instead, set the status and then chain it to the `res.jsonp()` method like this: `res.status(status).jsonp(obj)`.

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

Express 5 不再支持特征符 `res.send(obj, status)`。而是设置状态，然后将其链接到 `res.send()` 方法，如下所示：`res.status(status).send(obj)`。 Instead, set the status and then chain it to the `res.send()` method like this: `res.status(status).send(obj)`.

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

Express 5 no longer supports the signature `res.send(status)`, where `status` is a number. Instead, use the `res.sendStatus(statusCode)` function, which sets the HTTP response header status code and sends the text version of the code: “Not Found”, “Internal Server Error”, and so on.
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

在 Express 5 中，`res.sendfile()` 函数已由驼峰式大小写版本 `res.sendFile()` 替换。

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

## 已更改

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

在 Express 4 中已移除的 `app.router` 对象在 Express 5 中已恢复。在新版本中，此对象只是对 Express 基本路由器的引用，不像在 Express 3 中应用程序必须显式将该路由器装入。 In the new version, this object is a just a reference to the base Express router, unlike in Express 3, where an app had to explicitly load it.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

在 Express 4 中，如果存在端口号，`req.host` 函数会错误地将其剥离。在 Express 5 中，则会保留端口号。 In Express 5, the port number is maintained.

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

## 改进

### res.render()

现在，此方法为所有查看引擎强制执行异步行为，避免具有同步实现以及违反建议接口的查看引擎所导致的错误。

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/migrating-5.md          )

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/overriding-express-api.md          )

---

# 路由

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# 路由

_路由_表示应用程序端点 (URI) 的定义以及端点响应客户机请求的方式。
有关路由的简介，请参阅[基本路由](https://expressjs.com/zh-cn/starter/basic-routing.html)。
For an introduction to routing, see [Basic routing](https://expressjs.com/zh-cn/starter/basic-routing.html).

我们所使用的 app 与 HTTP 方法相对应的 Express 对象方法来定义路由，如 `app.get()` 用于处理 GET 请求，而 `app.post` 则用于处理 POST 请求。 For a full list,
see [app.METHOD](https://expressjs.com/zh-cn/5x/api.html#app.METHOD). You can also use [app.all()](https://expressjs.com/zh-cn/5x/api.html#app.all) to handle all HTTP methods and [app.use()](https://expressjs.com/zh-cn/5x/api.html#app.use) to
specify middleware as the callback function (See [Using middleware](https://expressjs.com/zh-cn/guide/using-middleware.html) for details).

这些路由方法都指定了回调函数（或者：“处理程序函数”），当程序接收到指定的路由（端点）的时候（也就是说 HTTP 方法请求时被调用），来调用回调函数，换句话说就是应用程序监听与指定路由和方法匹配的请求，当检测到匹配时，他会调用对应的回调函数。 In other words, the application “listens” for requests that match the specified route(s) and method(s), and when it detects a match, it calls the specified callback function.

In fact, the routing methods can have more than one callback function as arguments.
With multiple callback functions, it is important to provide `next` as an argument to the callback function and then call `next()` within the body of the function to hand off control
to the next callback.

以下代码是非常基本的路由示例。

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## 路由方法

路由方法派生自 HTTP 方法之一，附加到 `express` 类的实例。

以下代码是为访问应用程序根目录的 GET 和 POST 方法定义的路由示例。

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
For a full list, see [app.METHOD](https://expressjs.com/zh-cn/5x/api.html#app.METHOD).

有一种特殊路由方法：`app.all()`，它并非派生自 HTTP 方法。该方法用于在所有请求方法的路径中装入中间件函数。 在以下示例中，无论您使用 GET、POST、PUT、DELETE 还是在 [http 模块](https://nodejs.org/api/http.html#http_http_methods)中支持的其他任何 HTTP 请求方法，都将为针对“/secret”的请求执行处理程序。

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## 路由路径

路由路径与请求方法相结合，用于定义可以在其中提出请求的端点。路由路径可以是字符串、字符串模式或正则表达式。 Route paths can be strings, string patterns, or regular expressions.

Caution

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/zh-cn/guide/migrating-5.html#path-syntax) for more information.

Caution

In express 4, regular expression characters such as `$` need to be escaped with a `\`.

Note

Express uses [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) for matching the route paths; see the path-to-regexp documentation for all the possibilities in defining route paths. [Express Playground Router](https://bjohansebas.github.io/playground-router/) is a handy tool for testing basic Express routes, although it does not support pattern matching.

Warning

Query strings are not part of the route path.

### 以下是基于字符串的路由路径的一些示例。

此路由路径将请求与 `/random.text` 匹配。

```
app.get('/', (req, res) => {
  res.send('root')
})
```

此路由路径将请求与 `/about` 匹配。

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

此路由路径将请求与根路由 `/` 匹配。

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### 以下是基于字符串模式的路由路径的一些示例。

Caution

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/zh-cn/guide/migrating-5.html#path-syntax) for more information.

此路由路径将匹配 `/abe` 和 `/abcde`。

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

此路由路径将匹配 `abcd`、`abbcd`、`abbbcd` 等。

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

此路由路径将匹配 `abcd`、`abxcd`、`abRABDOMcd`、`ab123cd` 等。

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

此路由路径将匹配 `acd` 和 `abcd`。

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### 基于正则表达式的路由路径的示例：

此路由路径将匹配名称中具有“a”的所有路由。

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

此路由路径将匹配 `butterfly` 和 `dragonfly`，但是不匹配 `butterflyman`、`dragonfly man` 等。

```
app.get(/.*fly$/, (req, res) => {
  res.send('/.*fly$/')
})
```

## 路由处理程序

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

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/zh-cn/guide/migrating-5.html#path-syntax).

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

您可以提供多个回调函数，以类似于[中间件](https://expressjs.com/zh-cn/guide/using-middleware.html)的行为方式来处理请求。唯一例外是这些回调函数可能调用 `next('route')` 来绕过剩余的路由回调。您可以使用此机制对路由施加先决条件，在没有理由继续执行当前路由的情况下，可将控制权传递给后续路由。 The only exception is that these callbacks might invoke `next('route')` to bypass the remaining route callbacks. You can use this mechanism to impose pre-conditions on a route, then pass control to subsequent routes if there’s no reason to proceed with the current route.

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

单个回调函数可以处理一个路由。例如： For example:

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

多个回调函数可以处理一个路由（确保您指定 `next` 对象）。例如： For example:

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

一组回调函数可以处理一个路由。例如： For example:

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

独立函数与一组函数的组合可以处理一个路由。例如： For example:

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

## 响应方法

下表中响应对象 (`res`) 的方法可以向客户机发送响应，并终止请求/响应循环。如果没有从路由处理程序调用其中任何方法，客户机请求将保持挂起状态。 If none of these methods are called from a route handler, the client request will be left hanging.

| 方法 | 描述 |
| --- | --- |
| res.download() | 提示将要下载文件。 |
| res.end() | 结束响应进程。 |
| res.json() | 发送 JSON 响应。 |
| res.jsonp() | 在 JSONP 的支持下发送 JSON 响应。 |
| res.redirect() | 重定向请求。 |
| res.render() | 呈现视图模板。 |
| res.send() | 发送各种类型的响应。 |
| res.sendFile() | 以八位元流形式发送文件。 |
| res.sendStatus() | 设置响应状态码并以响应主体形式发送其字符串表示。 |

## app.route()

您可以使用 `app.route()` 为路由路径创建可链接的路由处理程序。
因为在单一位置指定路径，所以可以减少冗余和输入错误。有关路由的更多信息，请参阅 [Router() 文档](https://expressjs.com/zh-cn/4x/api.html#router)。
Because the path is specified at a single location, creating modular routes is helpful, as is reducing redundancy and typos. For more information about routes, see: [Router() documentation](https://expressjs.com/zh-cn/5x/api.html#router).

以下是使用 `app.route()` 定义的链式路由处理程序的示例。

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

使用 `express.Router` 类来创建可安装的模块化路由处理程序。`Router` 实例是完整的中间件和路由系统；因此，常常将其称为“微型应用程序”。 A `Router` instance is a complete middleware and routing system; for this reason, it is often referred to as a “mini-app”.

以下示例将路由器创建为模块，在其中装入中间件，定义一些路由，然后安装在主应用程序的路径中。

在应用程序目录中创建名为 `birds.js` 的路由器文件，其中包含以下内容：

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

接着，在应用程序中装入路由器模块：

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

此应用程序现在可处理针对 `/birds` 和 `/birds/about` 的请求，调用特定于此路由的 `timeLog` 中间件函数。

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/zh-cn/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/routing.md          )

---

# 使用中间件

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# 使用中间件

Express 是一个路由和中间件 Web 框架，其自身只具有最低程度的功能：Express 应用程序基本上是一系列中间件函数调用。

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/zh-cn/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/zh-cn/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. The next middleware function is commonly denoted by a variable named `next`.

中间件函数可以执行以下任务：

- 执行任何代码。
- 对请求和响应对象进行更改。
- 结束请求/响应循环。
- 调用堆栈中的下一个中间件函数。

如果当前中间件函数没有结束请求/响应循环，那么它必须调用 `next()`，以将控制权传递给下一个中间件函数。否则，请求将保持挂起状态。 Otherwise, the request will be left hanging.

Express 应用程序可以使用以下类型的中间件：

- [应用层中间件](#middleware.application)
- [路由器层中间件](#middleware.router)
- [错误处理中间件](#middleware.error-handling)
- [内置中间件](#middleware.built-in)
- [第三方中间件](#middleware.third-party)

You can load application-level and router-level middleware with an optional mount path.
You can also load a series of middleware functions together, which creates a sub-stack of the middleware system at a mount point.

## 应用层中间件

Bind application-level middleware to an instance of the [app object](https://expressjs.com/zh-cn/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

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

Route handlers enable you to define multiple routes for a path. 路由处理程序使您可以为一个路径定义多个路由。以下示例为针对 `/user/:id` 路径的 GET 请求定义两个路由。第二个路由不会导致任何问题，但是永远都不会被调用，因为第一个路由结束了请求/响应循环。 The second route will not cause any problems, but it will never get called because the first route ends the request-response cycle.

此示例显示一个中间件子堆栈，用于处理针对 `/user/:id` 路径的 GET 请求。

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

要跳过路由器中间件堆栈中剩余的中间件函数，请调用 `next('route')` 将控制权传递给下一个路由。
**注**：`next('route')` 仅在使用 `app.METHOD()` 或 `router.METHOD()` 函数装入的中间件函数中有效。

Note

`next('route')` will work only in middleware functions that were loaded by using the `app.METHOD()` or `router.METHOD()` functions.

此示例显示一个中间件子堆栈，用于处理针对 `/user/:id` 路径的 GET 请求。

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

此示例显示安装在 `/user/:id` 路径中的中间件函数。在 `/user/:id` 路径中为任何类型的 HTTP 请求执行此函数。

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

## 路由器层中间件

路由器层中间件的工作方式与应用层中间件基本相同，差异之处在于它绑定到 `express.Router()` 的实例。

```
const router = express.Router()
```

以下是在安装点使用安装路径装入一系列中间件函数的示例。
它演示一个中间件子堆栈，用于显示针对 `/user/:id` 路径的任何类型 HTTP 请求的信息。

使用 `router.use()` 和 `router.METHOD()` 函数装入路由器层中间件。
以下示例代码使用路由器层中间件复制以上为应用层中间件显示的中间件系统：

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

此示例显示一个中间件子堆栈，用于处理针对 `/user/:id` 路径的 GET 请求。

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

## 错误处理中间件

Error-handling middleware always takes *four* arguments. You must provide four arguments to identify it as an error-handling middleware function. Even if you don’t need to use the `next` object, you must specify it to maintain the signature. Otherwise, the `next` object will be interpreted as regular middleware and will fail to handle errors.

错误处理中间件函数的定义方式与其他中间件函数基本相同，差别在于错误处理函数有四个自变量而不是三个，专门具有特征符 `(err, req, res, next)`：

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

有关错误处理中间件的详细信息，请参阅：[错误处理](https://expressjs.com/zh-cn/guide/error-handling.html)。

## 内置中间件

Starting with version 4.x, Express no longer depends on [Connect](https://github.com/senchalabs/connect). 自 V4.x 起，Express 不再依赖于 [Connect](https://github.com/senchalabs/connect)。除 `express.static` 外，先前 Express 随附的所有中间件函数现在以单独模块的形式提供。请查看[中间件函数的列表](https://github.com/senchalabs/connect#middleware)。

Express has the following built-in middleware functions:

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## 第三方中间件

使用第三方中间件向 Express 应用程序添加功能。

安装具有所需功能的 Node.js 模块，然后在应用层或路由器层的应用程序中将其加装入。

以下示例演示如何安装和装入 cookie 解析中间件函数 `cookie-parser`。

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

有关 Express 常用的第三方中间件函数的部分列表，请参阅：[第三方中间件](https://expressjs.com/zh-cn/resources/middleware.html)。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/using-middleware.md          )

---

# 将模板引擎用于 Express

> Discover how to integrate and use template engines like Pug, Handlebars, and EJS with Express.js to render dynamic HTML pages efficiently.

# 将模板引擎用于 Express

A *template engine* enables you to use static template files in your application. At runtime, the template engine replaces
variables in a template file with actual values, and transforms the template into an HTML file sent to the client.
This approach makes it easier to design an HTML page.

The [Express application generator](https://expressjs.com/zh-cn/starter/generator.html) uses [Pug](https://pugjs.org/api/getting-started.html) as its default, but it also supports [Handlebars](https://www.npmjs.com/package/handlebars), and [EJS](https://www.npmjs.com/package/ejs), among others.

To render template files, set the following [application setting properties](https://expressjs.com/zh-cn/4x/api.html#app.set), in the default `app.js` created by the generator:

- `views`, the directory where the template files are located. `views`：模板文件所在目录。例如：`app.set('views', './views')`
  This defaults to the `views` directory in the application root directory.
- `view engine`, the template engine to use. `view engine`：要使用的模板引擎。例如：`app.set('view engine', 'pug')`

然后安装对应的模板引擎 npm 包：

```
$ npm install pug --save
```

与 Express 兼容的模板引擎（例如 Pug）导出名为 `__express(filePath, options, callback)` 的函数，该函数由 `res.render()` 函数调用以呈现模板代码。
某些模板引擎并不遵循此约定。[Consolidate.js](https://www.npmjs.org/package/consolidate) 库通过映射所有流行的 Node.js 模板引擎来遵循此约定，因此可以在 Express 内无缝工作。

Some template engines do not follow this convention. The [@ladjs/consolidate](https://www.npmjs.com/package/@ladjs/consolidate)
library follows this convention by mapping all of the popular Node.js template engines, and therefore works seamlessly within Express.

在设置视图引擎之后，不必指定该引擎或者在应用程序中装入模板引擎模块；Express 在内部装入此模块，如下所示（针对以上示例）。

```
app.set('view engine', 'pug')
```

在 `views` 目录中创建名为 `index.pug` 的 Pug 模板文件，其中包含以下内容：

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

向主页发出请求时，`index.pug` 文件将呈现为 HTML。

The view engine cache does not cache the contents of the template’s output, only the underlying template itself. The view is still re-rendered with every request even when the cache is on.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/using-template-engines.md          )

---

# 编写中间件以用于 Express 应用程序

> Learn how to write custom middleware functions for Express.js applications, including examples and best practices for enhancing request and response handling.

# 编写中间件以用于 Express 应用程序

## 概述

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/zh-cn/5x/api.html#req) (`req`), the [response object](https://expressjs.com/zh-cn/5x/api.html#res) (`res`), and the `next` function in the application’s request-response cycle. The `next` function is a function in the Express router which, when invoked, executes the middleware succeeding the current middleware.

中间件函数可以执行以下任务：

- 执行任何代码。
- 对请求和响应对象进行更改。
- 结束请求/响应循环。
- 调用堆栈中的下一个中间件。

如果当前中间件函数没有结束请求/响应循环，那么它必须调用 `next()`，以将控制权传递给下一个中间件函数。否则，请求将保持挂起状态。 Otherwise, the request will be left hanging.

以下示例显示中间件函数调用的元素：

|  | 中间件函数适用的 HTTP 方法。</tbody>中间件函数适用的路径（路由）。中间件函数。中间件函数的回调自变量，按约定称为“next”。HTTPresponseargument to the middleware function, called "res" by convention.HTTPrequestargument to the middleware function, called "req" by convention. |
| --- | --- |

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/writing-middleware.md          )

---

# 社区

> Connect with the Express.js community, learn about the technical committee, find resources, explore community-contributed modules, and get involved in discussions.

# 社区

## Technical committee

The Express technical committee meets online every two weeks (as needed) to discuss development and maintenance of Express,
and other issues relevant to the Express project. Each meeting is typically announced in an
[expressjs/discussions issue](https://github.com/expressjs/discussions/issues) with a link to join or view the meeting, which is
open to all observers.

The meetings are recorded; for a list of the recordings, see the [Express.js YouTube channel](https://www.youtube.com/channel/UCYjxjAeH6TRik9Iwy5nXw7g).

Members of the Express technical committee are:

**Active:**

- [@blakeembrey](https://github.com/blakeembrey) - Blake Embrey
- [@crandmck](https://github.com/crandmck) - Rand McKinney
- [@LinusU](https://github.com/LinusU) - Linus Unnebäck
- [@ulisesgascon](https://github.com/ulisesGascon) - Ulises Gascón
- [@sheplu](https://github.com/sheplu) - Jean Burellier
- [@wesleytodd](https://github.com/wesleytodd) - Wes Todd
- [@jonchurch](https://github.com/jonchurch) - Jon Church
- [@ctcpip](https://github.com/ctcpip/) - Chris de Almeida

**Inactive:**

- [@dougwilson](https://github.com/dougwilson) - Douglas Wilson
- [@hacksparrow](https://github.com/hacksparrow) - Hage Yaapa
- [@jonathanong](https://github.com/jonathanong) - jongleberry
- [@niftylettuce](https://github.com/niftylettuce) - niftylettuce
- [@troygoode](https://github.com/troygoode) - Troy Goode

## Express is made of many modules

我们充满活力的社区已创建了大量各种各样的扩展、[中间件模块](https://expressjs.com/zh-cn/resources/middleware.html)和更高层次的框架。请在 [wiki](https://github.com/expressjs/express/wiki) 中了解详细信息。

Additionally, the Express community maintains modules in these two GitHub orgs:

- [jshttp](https://github.com/jshttp) modules providing useful utility functions; see [Utility modules](https://expressjs.com/zh-cn/resources/utils.html).
- [pillarjs](https://github.com/pillarjs): low-level modules that Express uses internally.

To keep up with what is going on in the whole community, check out the [ExpressJS StatusBoard](https://expressjs.github.io/statusboard/).

## 问题

如果您发现程序中存在错误，或者只是希望提出功能请求，请在[问题队列](https://github.com/expressjs/express/issues)中开具凭证。

## 示例

查看存储库中数十个 Express 应用程序[示例](https://github.com/expressjs/express/tree/master/examples)，这些示例涵盖从 API 设计和认证到模板引擎集成的一切内容。

## Github Discussions

The [GitHub Discussions](https://github.com/expressjs/discussions) section is an excellent space to engage in conversations about the development and maintenance of Express, as well as to share ideas and discuss topics related to its usage.

# Branding of Express.js

## Express.js Logo

Express is a project of the OpenJS Foundation. Please review the [trademark policy](https://trademark-policy.openjsf.org/) for information about permissible use of Express.js logos and marks.

### Logotype

### Logomark

       [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/resources/community.md          )
