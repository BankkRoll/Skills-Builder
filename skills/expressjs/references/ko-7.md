# Express 5로의 이전 and more

# Express 5로의 이전

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# Express 5로의 이전

## 개요

Express 5는 Express 4와 크게 다르지 않으며, API에 대한 변경은 3.0에서 4.0으로의 변경만큼 크지 않습니다. 기본적인 API는 동일하게 유지되지만, 근본적인 변경사항이 존재합니다. 즉, Express 5를 사용하기 위해 기존 Express 4 프로그램을 업데이트하면 기존 Express 4 프로그램은 작동하지 않을 수 있습니다.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

이후 자동화된 테스트를 실행하여 실패하는 항목을 확인하고, 아래에 나열된 업데이트에 따라 문제를 수정할 수 있습니다. 테스트 실패 항목을 처리한 후에는 앱을 실행하여 어떠한 오류가 발생하는지 확인하십시오. 지원되지 않는 메소드나 특성을 앱이 사용하는 경우에는 이를 곧바로 확인할 수 있습니다.

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

## Express 5에서의 변경사항

**제거된 메소드 및 특성**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [복수형의 메소드 이름](#plural)
- [app.param(name, fn)에 대한 이름(name) 인수의 첫머리 콜론](#leading)
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

**개선된 항목**

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

**변경된 항목**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## 제거된 메소드 및 특성

앱에서 이러한 메소드 또는 특성 중 어느 하나라도 사용한다면 앱에서 충돌이 발생합니다. 따라서 버전 5로 업데이트한 후에는 앱을 변경해야 합니다.

### app.del()

Express 5는 `app.del()` 함수를 더 이상 지원하지 않습니다. 이 함수를 사용하면 오류에 대한 예외 처리(throw)가 발생합니다. HTTP DELETE 라우트를 등록하려면 `app.delete()` 함수를 대신 사용하십시오.

`delete`는 JavaScript의 예약된 키워드이므로, 처음에는 `delete` 대신 `del`이 사용되었습니다. 그러나, ECMAScript 6을 기준으로, `delete` 및 다른 예약된 키워드를 정식 특성 이름으로 사용할 수 있게 되었습니다.

참고

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

`app.param(fn)` 시그니처는 `app.param(name, fn)` 함수의 작동을 수정하는 데 사용되었습니다. 이 시그니처는 v4.11.0 이후 더 이상 사용되지 않았으며 Express 5에서는 전혀 지원되지 않습니다.

### 복수형의 메소드 이름

다음과 같은 메소드 이름은 이제 복수형이 되었습니다. Express 4에서는 구버전의 메소드를 사용하면 사용 중단 경고가 표시되었습니다. Express 5는 구버전의 메소드를 전혀 지원하지 않습니다.

`req.acceptsLanguage()`는 `req.acceptsLanguages()`로 대체되었습니다.

`req.acceptsCharset()`는 `req.acceptsCharsets()`로 대체되었습니다.

`req.acceptsEncoding()`은 `req.acceptsEncodings()`로 대체되었습니다.

참고

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

### app.param(name, fn)에 대한 이름(name)의 첫머리 콜론(:)

`app.param(name, fn)` 함수의 이름(name)의 첫머리 콜론 문자(:)는 Express 3의 잔존물이며, 하위 호환성을 위해 Express 4에서는 첫머리 콜론을 지원하면서 사용 중단 알림을 표시했습니다. Express 5는 아무런 메시지 표시 없이 첫머리 콜론을 무시하며, 콜론을 이용한 접두부가 없는 이름 매개변수를 사용합니다.

[app.param](https://expressjs.com/ko/4x/api.html#app.param)에 대한 Express 4 문서에는 첫머리 콜론이 언급되어 있지 않으므로, 이 문서를 따라 앱을 작성한 경우에는 이 변경사항이 코드에 영향을 미치지 않을 것입니다.

### req.param(name)

양식 데이터 검색을 위한 이 메소드는 혼란과 위험을 발생시킬 수 있으므로 제거되었습니다. 이제는 `req.params`, `req.body` 또는 `req.query` 오브젝트에서 제출된 매개변수 이름을 구체적으로 확인해야 합니다.

참고

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

Express 5는 `res.json(obj, status)` 시그니처를 더 이상 지원하지 않습니다. 대신, 상태를 설정한 후 이를 `res.status(status).json(obj)`과 같은 `res.json()` 메소드에 체인해야 합니다.

참고

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

Express 5는 `res.jsonp(obj, status)` 시그니처를 더 이상 지원하지 않습니다. 대신, 상태를 설정한 후 이를 `res.status(status).jsonp(obj)`와 같은 `res.jsonp()` 메소드에 체인해야 합니다.

참고

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

Express 5는 `res.send(obj, status)` 시그니처를 더 이상 지원하지 않습니다. 대신, 상태를 설정한 후 이를 `res.status(status).send(obj)`와 같은 `res.send()` 메소드에 체인해야 합니다.

참고

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

참고

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

Express 5 no longer supports the signature `res.send(obj, status)`. Instead, set the status and then chain it to the `res.send()` method like this: `res.status(status).send(obj)`.

참고

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

Express 5는 *`status`*가 숫자인 `res.send(status)` 시그니처를 더 이상 지원하지 않습니다. 대신, HTTP 응답 헤더 상태 코드를 설정하고 해당 코드의 텍스트 버전(“Not Found”, “Internal Server Error” 등)을 전송하는 `res.sendStatus(statusCode)` 함수를 사용해야 합니다.
`res.send()` 함수를 이용해 숫자를 전송해야 하는 경우, Express가 그 숫자를 지원되지 않는 구버전 시그니처 사용 시도로 해석하지 않도록 숫자의 앞뒤에 따옴표를 추가하여 숫자를 문자열로 변환하십시오.

참고

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

Express 5에서 `res.sendfile()` 함수는 낙타 대문자(camel-cased) 버전인 `res.sendFile()`로 대체되었습니다.

**Note:** In Express 5, `res.sendFile()` uses the `mime-types` package for MIME type detection, which returns different Content-Type values than Express 4 for several common file types:

- JavaScript files (.js): now “text/javascript” instead of “application/javascript”
- JSON files (.json): now “application/json” instead of “text/json”
- CSS files (.css): now “text/css” instead of “text/plain”
- XML files (.xml): now “application/xml” instead of “text/xml”
- Font files (.woff): now “font/woff” instead of “application/font-woff”
- SVG files (.svg): now “image/svg+xml” instead of “application/svg+xml”

참고

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

The `router.param(fn)` signature was used for modifying the behavior of the `router.param(name, fn)` function. 이 시그니처는 v4.11.0 이후 더 이상 사용되지 않았으며 Express 5에서는 전혀 지원되지 않습니다.

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

## 변경된 항목

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

참고

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

- Regexp characters are not supported. 예를 들면 다음과 같습니다.

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
예를 들면 다음과 같습니다.

```
const server = app.listen(8080, '0.0.0.0', (error) => {
  if (error) {
    throw error // e.g. EADDRINUSE
  }
  console.log(`Listening on ${JSON.stringify(server.address())}`)
})
```

### app.router

Express 4에서 제거되었던 `app.router` 오브젝트가 Express 5에 되돌아왔습니다. Express 3에서는 앱이 이 오브젝트를 명시적으로 로드해야 했던 것과 달리, 새 버전에서 이 오브젝트는 단순히 기본 Express 라우터에 대한 참조의 역할을 합니다.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

Express 4에서, 포트 번호가 존재하는 경우 `req.host` 함수는 포트 번호를 올바르지 않게 제거했습니다. Express 5에서는 포트 번호가 유지됩니다.

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

## 개선된 항목

### res.render()

이 메소드는 이제 모든 보기 엔진에 대해 비동기식 작동을 적용하며, 동기식 구현을 갖는 보기 엔진 및 권장되는 인터페이스를 위반하는 보기 엔진에 의한 버그의 발생을 방지합니다.

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/migrating-5.md          )

---

# Overriding the Express API

> 프로토타입을 사용해 request와 response 객체의 메서드와 속성을 오버라이드하여 Express.js API를 커스터마이즈하고 확장하는 방법을 알아보세요.

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/overriding-express-api.md          )

---

# 라우팅

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# 라우팅

_라우팅_은 애플리케이션 엔드 포인트(URI)의 정의, 그리고 URI가 클라이언트 요청에 응답하는 방식을 말합니다.
라우팅에 대한 소개는 [기본 라우팅](https://expressjs.com/ko/starter/basic-routing.html)을 참조하십시오.

You define routing using methods of the Express `app` object that correspond to HTTP methods;
for example, `app.get()` to handle GET requests and `app.post` to handle POST requests. For a full list,
see [app.METHOD](https://expressjs.com/ko/5x/api.html#app.METHOD). You can also use [app.all()](https://expressjs.com/ko/5x/api.html#app.all) to handle all HTTP methods and [app.use()](https://expressjs.com/ko/5x/api.html#app.use) to
specify middleware as the callback function (See [Using middleware](https://expressjs.com/ko/guide/using-middleware.html) for details).

특수한 라우팅 메소드인 `app.all()`은 어떠한 HTTP 메소드로부터도 파생되지 않습니다. 이 메소드는 모든 요청 메소드에 대해 한 경로에서 미들웨어 함수를 로드하는 데 사용됩니다.

In fact, the routing methods can have more than one callback function as arguments.
With multiple callback functions, it is important to provide `next` as an argument to the callback function and then call `next()` within the body of the function to hand off control
to the next callback.

다음 코드는 매우 기본적인 라우트의 예입니다.

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## 라우트 메소드

라우트 메소드는 HTTP 메소드 중 하나로부터 파생되며, `express` 클래스의 인스턴스에 연결됩니다.

다음 코드는 앱의 루트에 대한 GET 및 POST 메소드에 대해 정의된 라우트의 예입니다.

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

Express는 HTTP 메소드에 해당하는 다음과 같은 라우팅 메소드를 지원합니다.
For a full list, see [app.METHOD](https://expressjs.com/ko/5x/api.html#app.METHOD).

There is a special routing method, `app.all()`, used to load middleware functions at a path for *all* HTTP request methods. For example, the following handler is executed for requests to the route `"/secret"` whether using `GET`, `POST`, `PUT`, `DELETE`, or any other HTTP request method supported in the [http module](https://nodejs.org/api/http.html#http_http_methods).

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## 라우트 경로

라우트 경로는, 요청 메소드와의 조합을 통해, 요청이 이루어질 수 있는 엔드포인트를 정의합니다. 라우트 경로는 문자열, 문자열 패턴 또는 정규식일 수 있습니다.

주의

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/ko/guide/migrating-5.html#path-syntax) for more information.

주의

In express 4, regular expression characters such as `$` need to be escaped with a `\`.

참고

Express uses [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) for matching the route paths; see the path-to-regexp documentation for all the possibilities in defining route paths. [Express Route Tester](http://forbeslindesay.github.io/express-route-tester/)는 기본적인 Express 라우트의 테스트를 위한 편리한 도구이지만, 패턴 일치는 지원하지 않습니다.

경고

Query strings are not part of the route path.

### 문자열을 기반으로 하는 라우트 경로의 몇 가지 예는 다음과 같습니다.

다음의 라우트 경로는 요청을 루트 라우트 `/`에 일치시킵니다.

```
app.get('/', (req, res) => {
  res.send('root')
})
```

다음의 라우트 경로는 요청을 `/about`에 일치시킵니다.

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

다음의 라우트 경로는 요청을 `/random.text`에 일치시킵니다.

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### 문자열 패턴을 기반으로 하는 라우트 경로의 몇 가지 예는 다음과 같습니다.

주의

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/ko/guide/migrating-5.html#path-syntax) for more information.

다음의 라우트 경로는 `acd` 및 `abcd`와 일치합니다.

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

다음의 라우트 경로는 `abcd`, `abbcd` 및 `abbbcd` 등과 일치합니다.

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

다음의 라우트 경로는 `abcd`, `abxcd`, `abRABDOMcd` 및 `ab123cd` 등과 일치합니다.

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

다음의 라우트 경로는 `/abe` 및 `/abcde`와 일치합니다.

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### 정규식을 기반으로 하는 라우트 경로의 예:

다음의 라우트 경로는 라우트 이름에 “a”가 포함된 모든 항목과 일치합니다.

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

다음의 라우트 경로는 `butterfly` 및 `dragonfly`와 일치하지만, `butterflyman` 및 `dragonfly man` 등과 일치하지 않습니다.

```
app.get(/.*fly$/, (req, res) => {
  res.send('/.*fly$/')
})
```

## 조회 문자열은 라우트 경로의 일부가 아닙니다.

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

주의

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/ko/guide/migrating-5.html#path-syntax).

To have more control over the exact string that can be matched by a route parameter, you can append a regular expression in parentheses (`()`):

```
Route path: /user/:userId(\d+)
Request URL: http://localhost:3000/user/42
req.params: {"userId": "42"}
```

경고

Because the regular expression is usually part of a literal string, be sure to escape any `\` characters with an additional backslash, for example `\\d+`.

경고

In Express 4.x, [the*character in regular expressions is not interpreted in the usual way](https://github.com/expressjs/express/issues/2495). As a workaround, use `{0,}` instead of `*`. This will likely be fixed in Express 5.

## 라우트 핸들러

[미들웨어](https://expressjs.com/ko/guide/using-middleware.html)와 비슷하게 작동하는 여러 콜백 함수를 제공하여 요청을 처리할 수 있습니다. 유일한 차이점은 이러한 콜백은 `next('route')`를 호출하여 나머지 라우트 콜백을 우회할 수도 있다는 점입니다. 이러한 메커니즘을 이용하면 라우트에 대한 사전 조건을 지정한 후, 현재의 라우트를 계속할 이유가 없는 경우에는 제어를 후속 라우트에 전달할 수 있습니다.

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

다음 예에 나타난 것과 같이, 라우트 핸들러는 함수나 함수 배열의 형태 또는 둘을 조합한 형태일 수 있습니다.

하나의 콜백 함수는 하나의 라우트를 처리할 수 있습니다. 예를 들면 다음과 같습니다.

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

2개 이상의 콜백 함수는 하나의 라우트를 처리할 수 있습니다(`next` 오브젝트를 반드시 지정해야 함). 예를 들면 다음과 같습니다.

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

하나의 콜백 함수 배열은 하나의 라우트를 처리할 수 있습니다. 예를 들면 다음과 같습니다.

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

독립적인 함수와 함수 배열의 조합은 하나의 라우트를 처리할 수 있습니다. 예를 들면 다음과 같습니다.

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

## 응답 메소드

다음 표에 표시된 응답 오브젝트에 대한 메소드(`res`)는 응답을 클라이언트로 전송하고 요청-응답 주기를 종료할 수 있습니다. 라우트 핸들러로부터 다음 메소드 중 어느 하나도 호출되지 않는 경우, 클라이언트 요청은 정지된 채로 방치됩니다.

| 메소드 | 설명 |
| --- | --- |
| res.download() | 파일이 다운로드되도록 프롬프트합니다. |
| res.end() | 응답 프로세스를 종료합니다. |
| res.json() | JSON 응답을 전송합니다. |
| res.jsonp() | JSONP 지원을 통해 JSON 응답을 전송합니다. |
| res.redirect() | 요청의 경로를 재지정합니다. |
| res.render() | 보기 템플리트를 렌더링합니다. |
| res.send() | 다양한 유형의 응답을 전송합니다. |
| res.sendFile() | 파일을 옥텟 스트림의 형태로 전송합니다. |
| res.sendStatus() | 응답 상태 코드를 설정한 후 해당 코드를 문자열로 표현한 내용을 응답 본문으로서 전송합니다. |

## app.route()

`app.route()`를 이용하면 라우트 경로에 대하여 체인 가능한 라우트 핸들러를 작성할 수 있습니다.
경로는 한 곳에 지정되어 있으므로, 모듈식 라우트를 작성하면 중복성과 오타가 감소하여 도움이 됩니다. 라우트에 대한 자세한 정보는 [Router() 문서](https://expressjs.com/ko/4x/api.html#router)를 참조하십시오.

`app.route()`를 사용하여 정의된 체인 라우트 핸들러의 예는 다음과 같습니다.

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

`express.Router` 클래스를 사용하면 모듈식 마운팅 가능한 핸들러를 작성할 수 있습니다. `Router` 인스턴스는 완전한 미들웨어이자 라우팅 시스템이며, 따라서 “미니 앱(mini-app)”이라고 불리는 경우가 많습니다.

다음 예에서는 라우터를 모듈로서 작성하고, 라우터 모듈에서 미들웨어 함수를 로드하고, 몇몇 라우트를 정의하고, 기본 앱의 한 경로에 라우터 모듈을 마운트합니다.

다음의 내용이 입력된 `birds.js`라는 이름의 라우터 파일을 앱 디렉토리에 작성하십시오.

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

이후 앱 내에서 다음과 같이 라우터 모듈을 로드하십시오.

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

앱은 이제 `/birds` 및 `/birds/about`에 대한 요청을 처리할 수 있게 되었으며, 해당 라우트에 대한 특정한 미들웨어 함수인 `timeLog`를 호출할 것입니다.

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/ko/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/routing.md          )

---

# 미들웨어 사용

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# 미들웨어 사용

Express는 자체적인 최소한의 기능을 갖춘 라우팅 및 미들웨어 웹 프레임워크이며, Express 애플리케이션은 기본적으로 일련의 미들웨어 함수 호출입니다.

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/ko/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/ko/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. 그 다음의 미들웨어 함수는 일반적으로 `next`라는 이름의 변수로 표시됩니다.

미들웨어 함수는 다음과 같은 태스크를 수행할 수 있습니다.

- 모든 코드를 실행.
- 요청 및 응답 오브젝트에 대한 변경을 실행.
- 요청-응답 주기를 종료.
- 스택 내의 그 다음 미들웨어 함수를 호출.

현재의 미들웨어 함수가 요청-응답 주기를 종료하지 않는 경우에는 `next()`를 호출하여 그 다음 미들웨어 함수에 제어를 전달해야 합니다. 그렇지 않으면 해당 요청은 정지된 채로 방치됩니다.

Express 애플리케이션은 다음과 같은 유형의 미들웨어를 사용할 수 있습니다.

- [애플리케이션 레벨 미들웨어](#middleware.application)
- [라우터 레벨 미들웨어](#middleware.router)
- [오류 처리 미들웨어](#middleware.error-handling)
- [기본 제공 미들웨어](#middleware.built-in)
- [써드파티 미들웨어](#middleware.third-party)

애플리케이션 레벨 및 라우터 레벨 미들웨어는 선택적인 마운트 경로를 통해 로드할 수 있습니다.
일련의 미들웨어 함수를 함께 로드할 수도 있으며, 이를 통해 하나의 마운트 위치에 미들웨어 시스템의 하위 스택을 작성할 수 있습니다.

## 애플리케이션 레벨 미들웨어

Bind application-level middleware to an instance of the [app object](https://expressjs.com/ko/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

다음 예에는 마운트 경로가 없는 미들웨어 함수가 표시되어 있습니다. 이 함수는 앱이 요청을 수신할 때마다 실행됩니다.

```
const express = require('express')
const app = express()

app.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})
```

다음 예에는 `/user/:id` 경로에 마운트되는 미들웨어 함수가 표시되어 있습니다. 이 함수는 `/user/:id` 경로에
대한 모든 유형의 HTTP 요청에 대해 실행됩니다.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

다음 예에는 라우트 및 해당 라우트의 핸들러 함수(미들웨어 시스템)이 표시되어 있습니다. 이 함수는 `/user/:id` 경로에 대한 GET 요청을 처리합니다.

```
app.get('/user/:id', (req, res, next) => {
  res.send('USER')
})
```

아래에는 하나의 마운트 경로를 통해 일련의 미들웨어 함수를 하나의 마운트 위치에 로드하는 예가 표시되어 있습니다.
이 예는 `/user/:id` 경로에 대한 모든 유형의 HTTP 요청에 대한 요청 정보를 인쇄하는 미들웨어 하위 스택을 나타냅니다.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

라우트 핸들러를 이용하면 하나의 경로에 대해 여러 라우트를 정의할 수 있습니다. 아래의 예에서는 `/user/:id` 경로에 대한 GET 요청에 대해 2개의 라우트를 정의합니다. 두 번째 라우트는 어떠한 문제도 발생키지 않지만, 첫 번째 라우트가 요청-응답 주기를 종료시키므로 두 번째 라우트는 절대로 호출되지 않습니다.

다음 예에는 `/user/:id` 경로에 대한 GET 요청을 처리하는 미들웨어 하위 스택이 표시되어 있습니다.

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

라우터 미들웨어 스택의 나머지 미들웨어 함수들을 건너뛰려면 `next('route')`를 호출하여 제어를 그 다음 라우트로 전달하십시오.

참고

`next('route')` will work only in middleware functions that were loaded by using the `app.METHOD()` or `router.METHOD()` functions.

다음 예에는 `/user/:id` 경로에 대한 GET 요청을 처리하는 미들웨어 하위 스택이 표시되어 있습니다.

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

아래에는 상세한 옵션 오브젝트와 함께 `express.static` 미들웨어 함수를 사용하는 예가 표시되어 있습니다.

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

## 라우터 레벨 미들웨어

라우터 레벨 미들웨어는 `express.Router()` 인스턴스에 바인드된다는 점을 제외하면 애플리케이션 레벨 미들웨어와 동일한 방식으로 작동합니다.

```
const router = express.Router()
```

`router.use()` 및 `router.METHOD()` 함수를 사용하여 라우터 레벨 미들웨어를 로드하십시오.

다음 예의 코드는 위에서 애플리케이션 레벨 미들웨어에 대해 표시된 미들웨어 시스템을 라우터 레벨 미들웨어를 사용하여 복제합니다.

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

다음 예에는 `/user/:id` 경로에 대한 GET 요청을 처리하는 미들웨어 하위 스택이 표시되어 있습니다.

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

## 오류 처리 미들웨어

오류 처리 미들웨어에는 항상 *4개*의 인수가 필요합니다. 어떠한 함수를 오류 처리 미들웨어 함수로 식별하려면 4개의 인수를 제공해야 합니다. `next` 오브젝트를 사용할 필요는 없지만, 시그니처를 유지하기 위해 해당 오브젝트를 지정해야 합니다. 그렇지 않으면 `next` 오브젝트는 일반적인 미들웨어로 해석되어 오류 처리에 실패하게 됩니다.

다른 미들웨어 함수와 동일반 방법으로 다음과 같이 오류 처리 미들웨어 함수를 정의할 수 있지만, 오류 처리 함수는 3개가 아닌 4개의 인수, 구체적으로 말하면 `(err, req, res, next)` 시그니처를 갖는다는 점이 다릅니다.

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

오류 처리 미들웨어에 대한 상세 정보는 [오류 처리](https://expressjs.com/ko/guide/error-handling.html)를 참조하십시오.

## Built-in middleware

4.x 버전 이후의 Express는 더 이상 [Connect](https://github.com/senchalabs/connect)에 종속되지 않습니다. `express.static`의 실행을 제외하면, 이전에 Express와 함께
포함되었던 모든 미들웨어 함수는 이제 별도의 모듈에 포함되어 있습니다. [미들웨어 함수 목록](https://github.com/senchalabs/connect#middleware)을 확인하십시오.

Express has the following built-in middleware functions:

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## Third-party middleware

Express 앱에 기능을 추가하려면 써드파티 미들웨어를 사용하십시오.

필요한 기능을 위한 Node.js 모듈을 설치한 후, 애플리케이션 레벨 또는 라우터 레벨에서 해당 모듈을 앱에 로드하십시오.

다음 예는 쿠키 구문 분석 미들웨어 함수인 `cookie-parser`의 설치 및 로드를 나타냅니다.

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

Express와 함께 일반적으로 사용되고 있는 써드파티 미들웨어 함수의 일부 목록을 확인하려면 [써드파티 미들웨어](https://expressjs.com/ko/resources/middleware.html)를 참조하십시오.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/using-middleware.md          )
