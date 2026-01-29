# Express 5 への移行 and more

# Express 5 への移行

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# Express 5 への移行

## 概説

Express 5 は Express 4 とあまり変わりません。API の変更は、3.0 から 4.0 への変更ほど大きいものではありません。基本的な API は同じままですが、それでも互換性のない変更が行われています。つまり、Express 5 を使用するように既存の Express 4 を更新すると、機能しなくなる可能性があります。 Therefore, an application built with Express 4 might not work if you update it to use Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

その後、自動テストを実行して、どの機能が失敗するかを確認し、下記の更新に従って問題を修正することができます。テストの失敗に対応した後、アプリケーションを実行して、どのようなエラーが発生するかを確認します。サポートされていないメソッドまたはプロパティーをアプリケーションが使用している場合は、すぐに判明します。 After addressing test failures, run your app to see what errors occur. You’ll find out right away if the app uses any methods or properties that are not supported.

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

## Express 5 における変更点

**削除されたメソッドとプロパティー**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [メソッド名の複数化](#plural)
- [app.param(name, fn) の name 引数の先頭コロン](#leading)
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

**改善**

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

**変更**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## 削除されたメソッドとプロパティー

If you use any of these methods or properties in your app, it will crash. アプリケーションで以下のいずれかのメソッドまたはプロパティーを使用すると、異常終了します。そのため、バージョン 5 に更新した後で、アプリケーションを変更する必要があります。

### app.del()

Express 5 は、`app.del()` 関数をサポートしなくなりました。この関数を使用すると、エラーがスローされます。HTTP DELETE ルートを登録するには、代わりに `app.delete()` 関数を使用してください。 If you use this function, an error is thrown. For registering HTTP DELETE routes, use the `app.delete()` function instead.

最初は `del` が `delete` の代わりに使用されていました。`delete` は、JavaScript で予約されているキーワードであるためです。しかし、ECMAScript 6 以降では、`delete` およびその他の予約済みキーワードを正式にプロパティー名として使用できます。ここで、`app.del` 関数の非推奨につながった議論を読むことができます。 However, as of ECMAScript 6, `delete` and other reserved keywords can legally be used as property names.

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

`app.param(fn)` シグニチャーは、`app.param(name, fn)` 関数の動作を変更するために使用されていました。v4.11.0 以降では非推奨になったため、Express 5 は完全にサポートしなくなりました。 It has been deprecated since v4.11.0, and Express 5 no longer supports it at all.

### メソッド名の複数化

The following method names have been pluralized. In Express 4, using the old methods resulted in a deprecation warning. Express 5 no longer supports them at all:

`req.acceptsLanguage()` は `req.acceptsLanguages()` に置き換えられます。

`req.acceptsCharset()` は `req.acceptsCharsets()` に置き換えられます。

`req.acceptsEncoding()` は `req.acceptsEncodings()` に置き換えられます。

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

### app.param(name, fn) の name の先頭コロン (:)

`app.param(name, fn)` 関数の name の先頭コロン文字 (:) は、Express 3 の残余物であり、Express 4 では後方互換性のためにサポートされていましたが、非推奨の通知が出されてました。Express 5 では、サイレントに無視して、先頭にコロンを付けない name パラメーターを使用します。 Express 5 will silently ignore it and use the name parameter without prefixing it with a colon.

[app.param](https://expressjs.com/ja/4x/api.html#app.param) に関する Express 4 の資料では、先頭のコロンについて言及していないため、この資料に従う場合には、コードに影響は及ばないはずです。

### req.param(name)

This potentially confusing and dangerous method of retrieving form data has been removed. この混乱を招く可能性がある危険なメソッドは、フォーム・データを取得するためのものでしたが、削除されました。今後は、実行依頼されたパラメーター名を `req.params`、`req.body`、または `req.query` オブジェクトで具体的に見つける必要があります。

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

Express 5 は、シグニチャー `res.json(obj, status)` をサポートしなくなりました。代わりに、状況を設定してから、`res.status(status).json(obj)` のように `res.json()` メソッドにチェーニングします。 Instead, set the status and then chain it to the `res.json()` method like this: `res.status(status).json(obj)`.

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

Express 5 は、シグニチャー `res.jsonp(obj, status)` をサポートしなくなりました。代わりに、状況を設定してから、`res.status(status).jsonp(obj)` のように `res.jsonp()` メソッドにチェーニングします。 Instead, set the status and then chain it to the `res.jsonp()` method like this: `res.status(status).jsonp(obj)`.

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

Express 5 は、シグニチャー `res.send(obj, status)` をサポートしなくなりました。代わりに、状況を設定してから、`res.status(status).send(obj)` のように `res.send()` メソッドにチェーニングします。 Instead, set the status and then chain it to the `res.send()` method like this: `res.status(status).send(obj)`.

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

`res.sendfile()` 関数は、Express 5 ではキャメルケース版の `res.sendFile()` に置き換えられます。

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

## 変更

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

`app.router` オブジェクトは、Express 4 で削除されましたが、Express 5 で復帰しました。アプリケーションが明示的にロードする必要があった Express 3 とは異なり、新しいバージョンでは、このオブジェクトは基本の Express ルーターの単なる参照です。 In the new version, this object is a just a reference to the base Express router, unlike in Express 3, where an app had to explicitly load it.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

Express 4 では、`req.host` 関数は、ポート番号が存在する場合に、ポート番号を誤って削除していました。Express 5 では、ポート番号は維持されます。 In Express 5, the port number is maintained.

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

## 改善

### res.render()

このメソッドは、すべてのビュー・エンジンに非同期動作を適用するようになり、同期実装を使用して推奨インターフェースに違反していたビュー・エンジンに起因するバグを回避します。

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/migrating-5.md          )

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/overriding-express-api.md          )

---

# ルーティング

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# ルーティング

*Routing* refers to how an application’s endpoints (URIs) respond to client requests.
For an introduction to routing, see [Basic routing](https://expressjs.com/ja/starter/basic-routing.html).

ルーティングはHTTPメソッドに対応するExpressの`app`オブジェクトのメソッドを使用して定義します。たとえば、GETリクエストを処理する`app.get()`やPOSTリクエストを処理する`app.post`があります。
完全なリストについては、[app.METHOD](https://expressjs.com/ja/4x/api.html#app.METHOD)を参照してください。
また、すべてのHTTPメソッドを制御するために[app.all()](https://expressjs.com/ja/4x/api.html#app.all)を、ミドルウェアを指定するために[app.use()](https://expressjs.com/ja/4x/api.html#app.use)をコールバック関数として使用することができます(詳細については、[Using middleware](https://expressjs.com/ja/guide/using-middleware.html)を参照してください)。 For a full list,
see [app.METHOD](https://expressjs.com/ja/5x/api.html#app.METHOD). You can also use [app.all()](https://expressjs.com/ja/5x/api.html#app.all) to handle all HTTP methods and [app.use()](https://expressjs.com/ja/5x/api.html#app.use) to
specify middleware as the callback function (See [Using middleware](https://expressjs.com/ja/guide/using-middleware.html) for details).

これらのルーティングメソッドは、アプリケーションが指定されたルート（エンドポイント）とHTTPメソッドへのリクエストを受け取ったときに呼び出されるコールバック関数（ハンドラ関数とも呼ばれます）を指定します。 つまり、アプリケーションは指定されたルートとメソッドに一致するリクエストをリッスンし、一致を検出すると指定されたコールバック関数を呼び出します。 In other words, the application “listens” for requests that match the specified route(s) and method(s), and when it detects a match, it calls the specified callback function.

In fact, the routing methods can have more than one callback function as arguments.
実際、ルーティングメソッドは複数のコールバック関数を引数として持つことができます。
複数のコールバック関数では、コールバック関数に引数として`next`を指定し、次のコールバックに制御を渡す関数の本体内で`next()`を呼び出すことが重要です。

次のコードは、極めて基本的なルートの例です。

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## route メソッド

route メソッドは、いずれかの HTTP メソッドから派生され、`express` クラスのインスタンスに付加されます。

次のコードは、アプリケーションのルートへの GET メソッドと POST メソッドに定義されたルートの例です。

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

Expressは、すべてのHTTPリクエストメソッドに対応するメソッド（`get`、`post`など）をサポートしています。
完全なリストについては、[app.METHOD](https://expressjs.com/ja/4x/api.html#app.METHOD)を参照して下さい。
For a full list, see [app.METHOD](https://expressjs.com/ja/5x/api.html#app.METHOD).

*すべての* HTTPリクエストメソッドのパスにミドルウェア関数をロードするために使用される特別なルーティングメソッド、`app.all()`があります。 たとえば、GET、POST、PUT、DELETE、または[httpモジュール](https://nodejs.org/api/http.html#http_http_methods)でサポートされているその他のHTTPリクエストメソッドを使用するかどうかにかかわらず、”/secret”ルートへのリクエストに対して次のハンドラが実行されます。 For example, the following handler is executed for requests to the route `"/secret"` whether using `GET`, `POST`, `PUT`, `DELETE`, or any other HTTP request method supported in the [http module](https://nodejs.org/api/http.html#http_http_methods).

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## ルート・パス

ルート・パスは、リクエストメソッドとの組み合わせにより、リクエストを実行できるエンドポイントを定義します。ルート・パスは、ストリング、ストリング・パターン、または正規表現にすることができます。 Route paths can be strings, string patterns, or regular expressions.

Caution

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/ja/guide/migrating-5.html#path-syntax) for more information.

Caution

In express 4, regular expression characters such as `$` need to be escaped with a `\`.

Note

Express uses [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) for matching the route paths; see the path-to-regexp documentation for all the possibilities in defining route paths. [Express Playground Router](https://bjohansebas.github.io/playground-router/) is a handy tool for testing basic Express routes, although it does not support pattern matching.

Warning

Query strings are not part of the route path.

### 次に、ストリングに基づくルート・パスの例を示します。

このルート・パスは、リクエストをルートのルート `/` にマッチングします。

```
app.get('/', (req, res) => {
  res.send('root')
})
```

このルート・パスは、リクエストを `/about` にマッチングします。

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

このルート・パスは、リクエストを `/random.text` にマッチングします。

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### 次に、ストリング・パターンに基づくルート・パスの例を示します。

Caution

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/ja/guide/migrating-5.html#path-syntax) for more information.

このルート・パスは、`acd` および `abcd` をマッチングします。

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

このルート・パスは、`abcd`、`abbcd`、`abbbcd` などをマッチングします。

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

このルート・パスは、`abcd`、`abxcd`、`abRABDOMcd`、`ab123cd` などをマッチングします。

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

このルート・パスは、`/abe` および `/abcde` をマッチングします。

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### 次に、正規表現に基づくルート・パスの例を示します。

このルート・パスは、ルート名に「a」が含まれるすべてのものをマッチングします。

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

このルート・パスは、`butterfly` および `dragonfly` をマッチングしますが、`butterflyman`、`dragonfly man` などはマッチングしません。

```
app.get(/.*fly$/, (req, res) => {
  res.send('/.*fly$/')
})
```

## ルート・パラメータ

Route parameters are named URL segments that are used to capture the values specified at their position in the URL. ルート・パラメータは、URL内の指定された値を取得するために使用されるURLセグメントのことを言います。捕捉された値は`req.params`オブジェクトの中で、パスに指定されたルート・パラメータの名前をそれぞれのキーとして設定されます。

```
Route path: /users/:userId/books/:bookId
Request URL: http://localhost:3000/users/34/books/8989
req.params: { "userId": "34", "bookId": "8989" }
```

ルート・パラメータを使用してルートを定義するには、以下に示すようにルートのパスにルート・パラメータを指定するだけです。

```
app.get('/users/:userId/books/:bookId', (req, res) => {
  res.send(req.params)
})
```

ルート・パラメータの名前は、「単語文字」([A-Za-z0-9_])で構成する必要があります。

ハイフン（`-`）とドット（`.`）は文字通りに解釈されるので、有用な目的のためにルート・パラメータとともに使用することができます。

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

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/ja/guide/migrating-5.html#path-syntax).

ルート・パラメータで一致させることができる正確な文字列をより詳細に制御するために、括弧（`()`）内で正規表現を追加できます：

```
Route path: /user/:userId(\d+)
Request URL: http://localhost:3000/user/42
req.params: {"userId": "42"}
```

Warning

Because the regular expression is usually part of a literal string, be sure to escape any `\` characters with an additional backslash, for example `\\d+`.

Warning

In Express 4.x, [the*character in regular expressions is not interpreted in the usual way](https://github.com/expressjs/express/issues/2495). As a workaround, use `{0,}` instead of `*`. This will likely be fixed in Express 5.

## ルート・ハンドラー

リクエストを処理するために、[ミドルウェア](https://expressjs.com/ja/guide/using-middleware.html)のように動作する複数のコールバック関数を指定できます。唯一の例外は、これらのコールバックが `next('route')` を呼び出して、残りのルート・コールバックをバイパスすることです。このメカニズムを使用して、ルートに事前条件を適用し、現在のルートで続行する理由がない場合に後続のルートに制御を渡すことができます。 The only exception is that these callbacks might invoke `next('route')` to bypass the remaining route callbacks. You can use this mechanism to impose pre-conditions on a route, then pass control to subsequent routes if there’s no reason to proceed with the current route.

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

次の例に示すように、ルート・ハンドラーの形式は、関数、関数の配列、または両方の組み合わせにすることができます。

単一のコールバック関数で 1 つのルートを処理できます。次に例を示します。 For example:

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

複数のコールバック関数で1つのルートを処理できます (必ず、`next` オブジェクトを指定してください)。次に例を示します。 For example:

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

コールバック関数の配列で 1 つのルートを処理できます。次に例を示します。 For example:

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

独立した関数と、関数の配列の組み合わせで1つのルートを処理できます。次に例を示します。 For example:

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

## レスポンスメソッド

次の表に示すレスポンスオブジェクト (`res`) のメソッドは、レスポンスをクライアントに送信して、リクエストとレスポンスのサイクルを終了することができます。これらのメソッドのいずれもルート・ハンドラーから呼び出されない場合、クライアントリクエストはハングしたままになります。 If none of these methods are called from a route handler, the client request will be left hanging.

| メソッド | 説明 |
| --- | --- |
| res.download() | ファイルのダウンロードのプロンプトを出します。 |
| res.end() | レスポンスプロセスを終了します。 |
| res.json() | JSON レスポンスを送信します。 |
| res.jsonp() | JSONP をサポートする JSON レスポンスを送信します。 |
| res.redirect() | リクエストをリダイレクトします。 |
| res.render() | ビュー・テンプレートをレンダリングします。 |
| res.send() | さまざまなタイプのレスポンスを送信します。 |
| res.sendFile | ファイルをオクテット・ストリームとして送信します。 |
| res.sendStatus() | レスポンスのステータスコードを設定して、そのストリング表現をレスポンス本文として送信します。 |

## app.route()

You can create chainable route handlers for a route path by using `app.route()`.
Because the path is specified at a single location, creating modular routes is helpful, as is reducing redundancy and typos. For more information about routes, see: [Router() documentation](https://expressjs.com/ja/5x/api.html#router).

次に、`app.route()` を使用して定義された、チェーニングされたルート・ハンドラーの例を示します。

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

モジュール式のマウント可能なルート・ハンドラーを作成するには、`express.Router` クラスを使用します。`Router` インスタンスは、完全なミドルウェアおよびルーティング・システムです。そのため、よく「ミニアプリケーション」と呼ばれます。 A `Router` instance is a complete middleware and routing system; for this reason, it is often referred to as a “mini-app”.

次の例では、ルーターをモジュールとして作成し、その中にミドルウェア関数をロードして、いくつかのルートを定義し、ルート・モジュールをメインアプリケーションのパスにマウントします。

アプリケーション・ディレクトリーに次の内容で `birds.js` というルーター・ファイルを作成します。

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

次に、ルーター・モジュールをアプリケーションにロードします。

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

これで、アプリケーションは、`/birds` および `/birds/about` に対するリクエストを処理するほか、ルートに固有の `timeLog` ミドルウェア関数を呼び出すことができるようになります。

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/ja/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/routing.md          )

---

# ミドルウェアの使用

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# ミドルウェアの使用

Express は、それ自体では最小限の機能を備えたルーティングとミドルウェアの Web フレームワークです。Express アプリケーションは基本的に一連のミドルウェア関数呼び出しです。

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/ja/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/ja/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. The next middleware function is commonly denoted by a variable named `next`.

ミドルウェア関数は以下のタスクを実行できます。

- 任意のコードを実行する。
- リクエストオブジェクトとレスポンスオブジェクトを変更する。
- リクエストレスポンスサイクルを終了する。
- スタック内の次のミドルウェア関数を呼び出す。

現在のミドルウェア関数がリクエストレスポンスサイクルを終了しない場合は、`next()` を呼び出して、次のミドルウェア関数に制御を渡す必要があります。そうしないと、リクエストはハングしたままになります。 Otherwise, the request will be left hanging.

Express アプリケーションは、以下のタイプのミドルウェアを使用できます。

- [アプリケーション・レベルのミドルウェア](#middleware.application)
- [ルーター・レベルのミドルウェア](#middleware.router)
- [エラー処理ミドルウェア](#middleware.error-handling)
- [標準装備のミドルウェア](#middleware.built-in)
- [サード・パーティー・ミドルウェア](#middleware.third-party)

アプリケーション・レベルとルーター・レベルのミドルウェアは、オプションのマウント・パスを指定してロードできます。
また、一連のミドルウェア関数を一緒にロードできます。こうすると、マウント・ポイントにミドルウェア・システムのサブスタックが作成されます。
You can also load a series of middleware functions together, which creates a sub-stack of the middleware system at a mount point.

## アプリケーション・レベルのミドルウェア

Bind application-level middleware to an instance of the [app object](https://expressjs.com/ja/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

This example shows a middleware function with no mount path. The function is executed every time the app receives a request.

```
const express = require('express')
const app = express()

app.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})
```

This example shows a middleware function mounted on the `/user/:id` path. 次の例は、`/user/:id` パスにマウントされたミドルウェア関数を示しています。この関数は、`/user/:id` パスに対するすべてのタイプの HTTP リクエストで実行されます。

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

次の例は、`/user/:id` パスへの GET リクエストを処理するミドルウェア・サブスタックを示しています。

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

ルーター・ミドルウェア・スタックの残りのミドルウェア関数をスキップするには、`next('route')` を呼び出して、次のルートに制御を渡します。
**注**: `next('route')` は、`app.METHOD()` 関数または `router.METHOD()` 関数を使用してロードされたミドルウェア関数でのみ機能します。

Note

`next('route')` will work only in middleware functions that were loaded by using the `app.METHOD()` or `router.METHOD()` functions.

次の例は、`/user/:id` パスへの GET リクエストを処理するミドルウェア・サブスタックを示しています。

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

次の例は、ルートとそのハンドラー関数 (ミドルウェア・システム) を示しています。この関数は、`/user/:id` パスへの GET リクエストを処理します。

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

## ルーター・レベルのミドルウェア

ルーター・レベルのミドルウェアは、`express.Router()` のインスタンスにバインドされる点を除き、アプリケーション・レベルのミドルウェアと同じように動作します。

```
const router = express.Router()
```

`router.use()` 関数と `router.METHOD()` 関数を使用して、ルーター・レベルのミドルウェアをロードします。

次のコードの例では、ルーター・レベルのミドルウェアを使用して、上記のアプリケーション・レベルのミドルウェアで示されているミドルウェア・システムを複製します。

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

ルータのミドルウェア機能の残りの部分をスキップするには、`next('router')`を呼び出してルータインスタンスから制御を戻します。

次の例は、`/user/:id` パスへの GET リクエストを処理するミドルウェア・サブスタックを示しています。

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

## エラー処理ミドルウェア

Error-handling middleware always takes *four* arguments. You must provide four arguments to identify it as an error-handling middleware function. Even if you don’t need to use the `next` object, you must specify it to maintain the signature. Otherwise, the `next` object will be interpreted as regular middleware and will fail to handle errors.

エラー処理ミドルウェア関数は、その他のミドルウェア関数と同じ方法で定義しますが、例外として、シグニチャーで3つではなく4つの引数 `(err、req、res、next)`) を明示的に指定します。

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

エラー処理ミドルウェアについて詳しくは、[エラー処理](https://expressjs.com/ja/guide/error-handling.html)を参照してください。

## Built-in middleware

Starting with version 4.x, Express no longer depends on [Connect](https://github.com/senchalabs/connect). バージョン 4.x 以降、Express は [Connect](https://github.com/senchalabs/connect) に依存しなくなりました。以前に Express に組み込まれていたすべてのミドルウェア関数は個別のモジュールになりました。[ミドルウェア関数のリスト](https://github.com/senchalabs/connect#middleware)を参照してください。

Expressには、次のミドルウェア機能が組み込まれています。

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## Third-party middleware

Express アプリケーションに機能を追加するには、サード・パーティー・ミドルウェアを使用します。

必要な機能を提供する Node.js モジュールをインストールして、アプリケーションにアプリケーション・レベルまたはルーター・レベルでロードします。

次の例は、Cookie 解析ミドルウェア関数 `cookie-parser` のインストールおよびロードを示しています。

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

Express で一般的に使用されているサード・パーティー・ミドルウェア関数の一部のリストについては、[サード・パーティー・ミドルウェア](https://expressjs.com/ja/resources/middleware.html)を参照してください。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/using-middleware.md          )

---

# Express でのテンプレート・エンジンの使用

> Discover how to integrate and use template engines like Pug, Handlebars, and EJS with Express.js to render dynamic HTML pages efficiently.

# Express でのテンプレート・エンジンの使用

A *template engine* enables you to use static template files in your application. *テンプレートエンジン* を使用すると、アプリケーションで静的なテンプレートファイルを使用できます。実行時に、テンプレートエンジンはテンプレートファイルの変数を実際の値に置き換え、テンプレートをクライアントに送信するHTMLファイルに変換します。このアプローチにより、HTMLページの設計が容易になります。
This approach makes it easier to design an HTML page.

Expressで動作する一般的なテンプレートエンジンには、[Pug](https://pugjs.org/api/getting-started.html)、[Mustache](https://www.npmjs.com/package/mustache)、[EJS](https://www.npmjs.com/package/ejs)があります。[Expressアプリケーションジェネレータ](https://expressjs.com/ja/starter/generator.html)は[Jade](https://www.npmjs.com/package/jade)をデフォルトとして使用しますが、いくつかの他のものもサポートしています。

テンプレートファイルをレンダリングするには、次の[アプリケーション設定プロパティ](https://expressjs.com/ja/4x/api.html#app.set)を設定し、ジェネレータで作成されたデフォルトアプリの`app.js`にセットします。

- `views`, the directory where the template files are located. `views`はテンプレートファイルが置かれているディレクトリ。例：`app.set('views', './views')`。これは、デフォルトではアプリケーションのルートディレクトリ内の`views`ディレクトリになります
  This defaults to the `views` directory in the application root directory.
- `view engine`, the template engine to use. `view engine`は使用するテンプレートエンジン。たとえば、Pugテンプレートエンジンを使用するには、`app.set('view engine', 'pug')`を使用します

次に、対応するテンプレートエンジンnpmパッケージをインストールします。たとえばPugをインストールするには：

```
$ npm install pug --save
```

Pug などの Express 対応テンプレート・エンジンは、`__express(filePath, options, callback)` という関数をエクスポートします。この関数は、テンプレート・コードをレンダリングするために `res.render()` 関数によって呼び出されます。
一部のテンプレート・エンジンは、この規則に従いません。[Consolidate.js](https://www.npmjs.org/package/consolidate) ライブラリーは、すべての一般的な Node.js テンプレート・エンジンをマップすることで、この規則に従います。そのため、Express 内でシームレスに動作します。

Some template engines do not follow this convention. The [@ladjs/consolidate](https://www.npmjs.com/package/@ladjs/consolidate)
library follows this convention by mapping all of the popular Node.js template engines, and therefore works seamlessly within Express.

ビュー・エンジンが設定された後は、アプリケーションでエンジンを指定したり、テンプレート・エンジンをロードしたりする必要はありません。(上記の例に対応した) 下記のように、Express がモジュールを内部的にロードします。

```
app.set('view engine', 'pug')
```

以下の内容で `index.pug` という Pug テンプレート・ファイルを `views` ディレクトリーに作成します。

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

ホーム・ページに要求すると、`index.pug` ファイルは HTML としてレンダリングされます。

注：view engine のキャッシュは、テンプレートの出力内容をキャッシュしません。基本となるテンプレート自体だけです。このビューは、キャッシュがオンの場合でも、すべてのリクエストで再レンダリングされます。 The view is still re-rendered with every request even when the cache is on.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/using-template-engines.md          )

---

# Express アプリケーションで使用するミドルウェアの作成

> Learn how to write custom middleware functions for Express.js applications, including examples and best practices for enhancing request and response handling.

# Express アプリケーションで使用するミドルウェアの作成

## 概説

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/ja/5x/api.html#req) (`req`), the [response object](https://expressjs.com/ja/5x/api.html#res) (`res`), and the `next` function in the application’s request-response cycle. The `next` function is a function in the Express router which, when invoked, executes the middleware succeeding the current middleware.

ミドルウェア関数は以下のタスクを実行できます。

- 任意のコードを実行する。
- リクエストオブジェクトとレスポンスオブジェクトを変更する。
- リクエストレスポンスサイクルを終了する。
- スタック内の次のミドルウェアを呼び出す。

現在のミドルウェア関数がリクエストレスポンスサイクルを終了しない場合は、`next()` を呼び出して、次のミドルウェア関数に制御を渡す必要があります。そうしないと、リクエストはハングしたままになります。 Otherwise, the request will be left hanging.

次の例は、ミドルウェア関数呼び出しの要素を示しています。

|  | ミドルウェア関数が適用される HTTP メソッド。</tbody>ミドルウェア関数が適用されるパス (ルート)。ミドルウェア関数。ミドルウェア関数へのコールバック引数 (慣習的に「next」と呼ばれます)。HTTPresponseargument to the middleware function, called "res" by convention.HTTPrequestargument to the middleware function, called "req" by convention. |
| --- | --- |

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/writing-middleware.md          )

---

# コミュニティー

> Connect with the Express.js community, learn about the technical committee, find resources, explore community-contributed modules, and get involved in discussions.

# コミュニティー

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

この活気あるコミュニティーでは、さまざまな拡張機能、[ミドルウェア・モジュール](https://expressjs.com/ja/resources/middleware.html)、高水準のフレームワークが作成されています。[Wiki](https://github.com/expressjs/express/wiki) で確認してください。

Additionally, the Express community maintains modules in these two GitHub orgs:

- [jshttp](https://github.com/jshttp) modules providing useful utility functions; see [Utility modules](https://expressjs.com/ja/resources/utils.html).
- [pillarjs](https://github.com/pillarjs): low-level modules that Express uses internally.

To keep up with what is going on in the whole community, check out the [ExpressJS StatusBoard](https://expressjs.github.io/statusboard/).

## 問題

バグに思われるものが見つかったり、単に機能を要求したりする場合は、[問題のキュー](https://github.com/expressjs/express/issues)でチケットをオープンしてください。

## 例

API の設計や認証からテンプレート・エンジンの統合まで、あらゆるものを扱っている数十の Express アプリケーションの[例](https://github.com/expressjs/express/tree/master/examples)をリポジトリーでご覧ください。

## Github Discussions

The [GitHub Discussions](https://github.com/expressjs/discussions) section is an excellent space to engage in conversations about the development and maintenance of Express, as well as to share ideas and discuss topics related to its usage.

# Branding of Express.js

## Express.js Logo

Express is a project of the OpenJS Foundation. Please review the [trademark policy](https://trademark-policy.openjsf.org/) for information about permissible use of Express.js logos and marks.

### Logotype

### Logomark

       [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/resources/community.md          )
