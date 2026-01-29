# Wechsel zu Express 5 and more

# Wechsel zu Express 5

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# Wechsel zu Express 5

## Überblick

Express 5.0 befindet sich noch in der Beta-Release-Phase. Hier finden Sie jedoch bereits eine Vorschau zu den Änderungen in diesem Release und zur Migration Ihrer Express 4-Anwendung auf Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

Sie können Ihre automatisierten Tests ausführen, um zu sehen, was fehlschlägt, und Probleme gemäß den folgenden Updates beheben. Nachdem Sie alle Testfehler behoben haben, führen Sie Ihre Anwendung aus, um zu sehen, welche Fehler noch auftreten. Sie werden sofort feststellen, ob die Anwendung Methoden oder Eigenschaften verwendet, die nicht unterstützt werden.

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

## Änderungen in Express 5

**Entfernte Methoden und Eigenschaften**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [Pluralisierte Methodennamen](#plural)
- [Führender Doppelpunkt im Namensargument für app.param(name, fn)](#leading)
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

**Verbesserungen**

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

**Geändert**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## Entfernte Methoden und Eigenschaften

Wenn Sie eine dieser Methoden oder Eigenschaften in Ihrer Anwendung verwenden, stürzt die Anwendung ab. Sie müssen also Ihre Anwendung ändern, wenn Sie auf Version 5 umgestellt haben.

### app.del()

Express 5 unterstützt die Funktion `app.del()` nicht mehr. Wenn Sie diese Funktion verwenden, wird ein Fehler ausgelöst. Für die Registrierung von HTTP DELETE-Weiterleitungen verwenden Sie stattdessen die Funktion `app.delete()`.

Anfänglich wurde `del` statt `delete` verwendet, weil `delete` in JavaScript ein reserviertes Schlüsselwort ist. Ab ECMAScript 6 jedoch können `delete` und andere reservierte Schlüsselwörter legal als Eigenschaftsnamen verwendet werden.

Hinweis

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

Die Signatur `app.param(fn)` wurde für die Änderung der Verhaltensweise der Funktion `app.param(name, fn)` verwendet. Seit v4.11.0 wurde sie nicht mehr verwendet. In Express 5 wird sie überhaupt nicht mehr unterstützt.

### Pluralisierte Methodennamen

Die folgenden Methodennamen wurden pluralisiert. In Express 4 wurde bei Verwendung der alten Methoden eine Warnung zur Einstellung der Unterstützung ausgegeben. Express 5 unterstützt diese Methoden nicht mehr.

`req.acceptsLanguage()` wird durch `req.acceptsLanguages()` ersetzt.

`req.acceptsCharset()` wird durch `req.acceptsCharsets()` ersetzt.

`req.acceptsEncoding()` wird durch `req.acceptsEncodings()` ersetzt.

Hinweis

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

### Führender Doppelpunkt (:) im Namen für app.param(name, fn)

Ein führendes Doppelpunktzeichen (:) im Namen für die Funktion `app.param(name, fn)` ist ein Überbleibsel aus Express 3. Aus Gründen der Abwärtskompatibilität wurde dieser Name in Express 4 mit einem Hinweis zu veralteten Versionen weiter unterstützt. In Express 5 wird dieser Name stillschwiegend ignoriert und der Namensparameter ohne einen vorangestellten Doppelpunkt verwendet.

Dies dürfte keine Auswirkungen auf Ihren Code haben, wenn Sie die Express 4-Dokumentation zu [app.param](https://expressjs.com/de/4x/api.html#app.param) befolgen, da dort der führende Doppelpunkt nicht erwähnt wird.

### req.param(name)

Dieses potenziell verwirrende und durchaus riskante Verfahren des Abrufens von Formulardaten wurde entfernt. Sie müssen nun ganz speziell nach dem übergebenen Parameternamen im Objekt `req.params`, `req.body` oder `req.query` suchen.

Hinweis

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

Express 5 unterstützt die Signatur `res.json(obj, status)` nicht mehr. Stattdessen müssen Sie den Status festlegen und diesen dann mit `res.json()`-Methoden wie  dieser verketten: `res.status(status).json(obj)`.

Hinweis

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

Express 5 unterstützt die Signatur `res.jsonp(obj, status)` nicht mehr. Stattdessen müssen Sie den Status festlegen und diesen dann mit `res.jsonp()`-Methoden wie  dieser verketten: `res.status(status).jsonp(obj)`.

Hinweis

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

Express 5 unterstützt die Signatur `res.send(obj, status)` nicht mehr. Stattdessen müssen Sie den Status festlegen und diesen dann mit `res.send()`-Methoden wie  dieser verketten: `res.status(status).send(obj)`.

Hinweis

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

Hinweis

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

Hinweis

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

Express 5 unterstützt die Signatur `res.send(status)`, nicht mehr, wobei *status* für eine Zahl steht. Verwenden Sie stattdessen die Funktion `res.sendStatus(statusCode)`, mit der der Statuscode für den HTTP-Antwort-Header festgelegt und die Textversion des Codes gesendet wird: “Not Found” (Nicht gefunden), “Internal Server Error” (Interner Serverfehler) usw.
Wenn Sie eine Zahl senden und hierfür die Funktion `res.send()` verwenden müssen, müssen Sie die Zahl in Anführungszeichen setzen, um diese in eine Zeichenfolge zu konvertieren. Dadurch interpretiert Express diese Zahl nicht als Versuch, die nicht mehr unterstützte alte Signatur zu verwenden.

Hinweis

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

Die Funktion `res.sendfile()` wurde durch eine Version in Camel-Schreibweise von `res.sendFile()` in Express 5 ersetzt.

**Note:** In Express 5, `res.sendFile()` uses the `mime-types` package for MIME type detection, which returns different Content-Type values than Express 4 for several common file types:

- JavaScript files (.js): now “text/javascript” instead of “application/javascript”
- JSON files (.json): now “application/json” instead of “text/json”
- CSS files (.css): now “text/css” instead of “text/plain”
- XML files (.xml): now “application/xml” instead of “text/xml”
- Font files (.woff): now “font/woff” instead of “application/font-woff”
- SVG files (.svg): now “image/svg+xml” instead of “application/svg+xml”

Hinweis

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

The `router.param(fn)` signature was used for modifying the behavior of the `router.param(name, fn)` function. Seit v4.11.0 wurde sie nicht mehr verwendet. In Express 5 wird sie überhaupt nicht mehr unterstützt.

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

## Geändert

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

Hinweis

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

- Regexp characters are not supported. Beispiel:

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
Beispiel:

```
const server = app.listen(8080, '0.0.0.0', (error) => {
  if (error) {
    throw error // e.g. EADDRINUSE
  }
  console.log(`Listening on ${JSON.stringify(server.address())}`)
})
```

### app.router

Das Objekt `app.router`, das in Express 4 entfernt wurde, ist in Express 5 wieder verfügbar. In der neuen Version fungiert dieses Objekt nur als Referenz zum Express-Basisrouter – im Gegensatz zu Express 3, wo die Anwendung dieses Objekt explizit laden musste.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

In Express 4 übergab die Funktion `req.host` nicht ordnungsgemäß eine eventuell vorhandene Portnummer. In Express 5 wird die Portnummer beibehalten.

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

## Verbesserungen

### res.render()

Diese Methode erzwingt nun asynchrones Verhalten für alle View-Engines, sodass durch View-Engines mit synchroner Implementierung verursachte Fehler vermieden werden, durch die die empfohlene Schnittstelle nicht verwendet werden konnte.

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/migrating-5.md          )

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/overriding-express-api.md          )

---

# Weiterleitung (Routing)

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# Weiterleitung (Routing)

Der Begriff *Weiterleitung* (Routing) bezieht sich auf die Definition von Anwendungsendpunkten (URIs) und deren Antworten auf Clientanforderungen.
Eine Einführung in dieses Routing siehe [Basisrouting](https://expressjs.com/de/starter/basic-routing.html).

You define routing using methods of the Express `app` object that correspond to HTTP methods;
for example, `app.get()` to handle GET requests and `app.post` to handle POST requests. For a full list,
see [app.METHOD](https://expressjs.com/de/5x/api.html#app.METHOD). You can also use [app.all()](https://expressjs.com/de/5x/api.html#app.all) to handle all HTTP methods and [app.use()](https://expressjs.com/de/5x/api.html#app.use) to
specify middleware as the callback function (See [Using middleware](https://expressjs.com/de/guide/using-middleware.html) for details).

These routing methods specify a callback function (sometimes called “handler functions”) called when the application receives a request to the specified route (endpoint) and HTTP method. In other words, the application “listens” for requests that match the specified route(s) and method(s), and when it detects a match, it calls the specified callback function.

In fact, the routing methods can have more than one callback function as arguments.
With multiple callback functions, it is important to provide `next` as an argument to the callback function and then call `next()` within the body of the function to hand off control
to the next callback.

Der folgende Code ist ein Beispiel für ein sehr einfaches Basisrouting.

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## Weiterleitungsmethoden

Eine Weiterleitungsmethode wird von einer HTTP-Methode abgeleitet und an eine Instanz der Klasse `express` angehängt.

Der folgende Code ist ein Beispiel für Weiterleitungen, die für die Methoden GET und POST zum Stamm (Root) der Anwendung definiert werden.

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
For a full list, see [app.METHOD](https://expressjs.com/de/5x/api.html#app.METHOD).

Es gibt eine spezielle Weiterleitungsmethode, `app.all()`, die nicht von einer HTTP-Methode abgeleitet wird. Diese Methode wird zum Laden von Middlewarefunktionen bei einem Pfad für alle Anforderungsmethoden verwendet. Im folgenden Beispiel wird der Handler für Anforderungen zur Weiterleitung “/secret” ausgeführt, um herauszufinden, ob Sie GET-, POST-, PUT-, DELETE- oder andere HTTP-Anforderungsmethoden verwenden, die im [HTTP-Modul](https://nodejs.org/api/http.html#http_http_methods) unterstützt werden.

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## Weiterleitungspfade

Über Weiterleitungspfade werden in Kombination mit einer Anforderungsmethode die Endpunkte definiert, bei denen Anforderungen erfolgen können. Weiterleitungspfade können Zeichenfolgen, Zeichenfolgemuster oder reguläre Ausdrücke sein.

Vorsicht

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/de/guide/migrating-5.html#path-syntax) for more information.

Vorsicht

In express 4, regular expression characters such as `$` need to be escaped with a `\`.

Hinweis

Express uses [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) for matching the route paths; see the path-to-regexp documentation for all the possibilities in defining route paths. [Express Route Tester](http://forbeslindesay.github.io/express-route-tester/) ist ein handliches Tool zum Testen von Express-Basisweiterleitungen, auch wenn dieses Tool keine Musterabgleiche unterstützt.

Warnung

Query strings are not part of the route path.

### Route paths based on strings

Dieser Weiterleitungspfad gleicht Weiterleitungsanforderungen zum Stammverzeichnis (`/`) ab.

```
app.get('/', (req, res) => {
  res.send('root')
})
```

Dieser Weiterleitungspfad gleicht Anforderungen mit `/about` ab.

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

Dieser Weiterleitungspfad gleicht Anforderungen mit `/random.text` ab.

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### Route paths based on string patterns

Vorsicht

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/de/guide/migrating-5.html#path-syntax) for more information.

Dieser Weiterleitungspfad gleicht `acd` und `abcd` ab.

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

Dies sind einige Beispiele für Weiterleitungspfade auf Basis von Zeichenfolgemustern.

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

Dies sind einige Beispiele für Weiterleitungspfade auf Basis von Zeichenfolgen.

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

Dieser Weiterleitungspfad gleicht `/abe` und `/abcde` ab.

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### Route paths based on regular expressions

Dieser Weiterleitungspfad gleicht alle Weiterleitungsnamen ab, die den Buchstaben “a” enthalten.

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

Dieser Weiterleitungspfad gleicht `butterfly` und `dragonfly`, jedoch nicht `butterflyman`, `dragonfly man` usw.

```
app.get(/.*fly$/, (req, res) => {
  res.send('/.*fly$/')
})
```

## Route parameters

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

Vorsicht

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/de/guide/migrating-5.html#path-syntax).

To have more control over the exact string that can be matched by a route parameter, you can append a regular expression in parentheses (`()`):

```
Route path: /user/:userId(\d+)
Request URL: http://localhost:3000/user/42
req.params: {"userId": "42"}
```

Warnung

Because the regular expression is usually part of a literal string, be sure to escape any `\` characters with an additional backslash, for example `\\d+`.

Warnung

In Express 4.x, [the*character in regular expressions is not interpreted in the usual way](https://github.com/expressjs/express/issues/2495). As a workaround, use `{0,}` instead of `*`. This will likely be fixed in Express 5.

## Routenhandler (Weiterleitungsroutinen)

Sie können mehrere Callback-Funktionen angeben, die sich wie [Middleware](https://expressjs.com/de/guide/using-middleware.html) verhalten, um eine Anforderung zu verarbeiten. Die einzige Ausnahme hierbei ist, dass diese Callbacks möglicherweise `next('route')` aufrufen, um die verbleibenden Weiterleitungs-Callbacks zu umgehen. Mit diesem Verfahren können Sie Vorabbedingungen für eine Weiterleitung festlegen und dann die Steuerung an nachfolgende Weiterleitungen übergeben, wenn kein Grund vorliegt, mit der aktuellen Weiterleitung fortzufahren.

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

Routenhandler können eine Funktion und/oder ein Funktionsarray sein, wie in den folgenden Beispielen zu sehen ist.

Eine einzelne Callback-Funktion kann eine Weiterleitung verarbeiten. Beispiel:

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

Mehrere Callback-Funktionen können eine Weiterleitung verarbeiten (achten Sie darauf, dass Sie das Objekt `next` angeben). Beispiel:

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

Ein Array von Callback-Funktionen kann eine Weiterleitung verarbeiten. Beispiel:

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

Eine Kombination aus unabhängigen Funktionen und Funktionsarrays kann eine Weiterleitung verarbeiten. Beispiel:

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

## Antwortmethoden

Über die Methoden für das Antwortobjekt (`res`) in der folgenden Tabelle kann eine Antwort an den Client gesendet und der Anforderung/Antwort-Zyklus beendet werden. Wenn keine dieser Methoden über einen Routenhandler aufgerufen wird, bleibt die Clientanforderung im Status “blockiert”.

| Methode | Beschreibung |
| --- | --- |
| res.download() | Gibt eine Eingabeaufforderung zum Herunterladen einer Datei aus. |
| res.end() | End the response process. |
| res.json() | Sendet eine JSON-Antwort. |
| res.jsonp() | Sendet eine JSON-Antwort mit JSONP-Unterstützung. |
| res.redirect() | Leitet eine Anforderung um. |
| res.render() | Render a view template. |
| res.send() | Sendet eine Antwort mit unterschiedlichen Typen. |
| res.sendFile | Sendet eine Datei als Oktett-Stream. |
| res.sendStatus() | Legt den Antwortstatuscode fest und sendet dessen Zeichenfolgedarstellung als Antworthauptteil. |

## app.route()

Sie können mithilfe von `app.route()` verkettbare Routenhandler für einen Weiterleitungspfad erstellen.
Da der Pfad an einer einzelnen Position angegeben wird, ist das Erstellen modularer Weiterleitungen hilfreich, da Redundanzen und Schreibfehler reduziert werden. Weitere Informationen zu Weiterleitungen finden Sie in der Dokumentation zu [Router()](https://expressjs.com/de/4x/api.html#router).

Dies ist ein Beispiel für verkettete Routenhandler, die mit der Funktion `app.route()` definiert werden.

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

Mit der Klasse `express.Router` lassen sich modular einbindbare Routenhandler erstellen. Eine `Router`-Instanz ist ein vollständiges Middleware- und Routingsystem. Aus diesem Grund wird diese Instanz oft auch als “Mini-App” bezeichnet.

Im folgenden Beispiel wird ein Router als Modul erstellt, eine Middlewarefunktion in das Modul geladen, es werden Weiterleitungen definiert und das Modul letztendlich in einen Pfad in der Hauptanwendung eingebunden.

Erstellen Sie eine Routerdatei namens `birds.js` mit dem folgenden Inhalt im Anwendungsverzeichnis:

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

Laden Sie dann das Routermodul in die Anwendung:

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

Die Anwendung kann nun Anforderungen an die Pfade `/birds` und `/birds/about` bearbeiten und ruft die Middlewarefunktion `timeLog` auf, die speziell für diese Weiterleitung bestimmt ist.

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/de/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/routing.md          )

---

# Middleware verwenden

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# Middleware verwenden

Express ist ein Weiterleitungs- und Middleware-Web-Framework, das selbst nur minimale Funktionalität aufweist: Eine Express-Anwendung besteht im Wesentlichen aus einer Reihe von Middlewarefunktionsaufrufen.

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/de/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/de/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. Die nächste Middlewarefunktion wird im Allgemeinen durch die Variable `next` bezeichnet.

Über Middlewarefunktionen lassen sich die folgenden Tasks ausführen:

- Ausführen von Code
- Vornehmen von Änderungen an der Anforderung und an Antwortobjekten
- End the request-response cycle.
- Aufrufen der nächsten Middlewarefunktion im Stack

Wenn über die aktuelle Middlewarefunktion der Anforderung/Antwort-Zyklus nicht beendet werden kann, muss `next()` aufgerufen werden, um die Steuerung an die nächste Middlewarefunktion zu übergeben. Andernfalls geht die Anforderung in den Status “Blockiert” über.

Eine Express-Anwendung kann die folgenden Middlewaretypen verwenden:

- [Middleware auf Anwendungsebene](#middleware.application)
- [Middleware auf Routerebene](#middleware.router)
- [Middleware für die Fehlerbehandlung](#middleware.error-handling)
- [Integrierte Middleware](#middleware.built-in)
- [Middleware anderer Anbieter](#middleware.third-party)

Sie können Middleware auf Anwendungsebene und Routerebene mit einem optionalen Mountpfad laden.
Sie können auch eine Reihe von Middlewarefunktionen zusammen laden. Dadurch wird ein Sub-Stack des Middlewaresystems am Mountpunkt erstellt.

## Middleware auf Anwendungsebene

Bind application-level middleware to an instance of the [app object](https://expressjs.com/de/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

Dieses Beispiel zeigt eine Middlewarefunktion ohne Mountpfad. Die Funktion wird immer dann ausgeführt, wenn die Anwendung eine Anforderung erhält.

```
const express = require('express')
const app = express()

app.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})
```

Dieses Beispiel zeigt eine Middlewarefunktion mit dem Mountpfad `/user/:id`. Die Funktion wird für jede Art von HTTP-Anforderung auf dem Pfad `/user/:id` ausgeführt.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Dieses Beispiel zeigt eine Weiterleitung und deren Handlerfunktion (Middlewaresystem). Die Funktion verarbeitet GET-Anforderungen zum Pfad `/user/:id`.

```
app.get('/user/:id', (req, res, next) => {
  res.send('USER')
})
```

Dies ist ein Beispiel zum Laden einer Reihe von Middlewarefunktionen an einem Mountpunkt mit einem Mountpfad.
Das Beispiel veranschaulicht einen Middleware-Stack, über den Anforderungsinformationen  zu einer HTTP-Anforderung zum Pfad `/user/:id` ausgegeben werden.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Mit einem Routenhandler können Sie mehrere Weiterleitungen für einen Pfad definieren. Im folgenden Beispiel werden zwei Weiterleitungen für GET-Anforderungen zum Pfad `/user/:id` definiert. Die zweite Weiterleitung verursacht zwar keine Probleme, wird jedoch nie aufgerufen, da durch die erste Weiterleitung der Anforderung/Antwort-Zyklus beendet wird.

Dieses Beispiel zeigt einen Middleware-Sub-Stack, über den GET-Anforderungen zum Pfad `/user/:id` verarbeitet werden.

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

Wenn Sie den Rest der Middlewarefunktionen eines Weiterleitungs-Middleware-Stack überspringen wollen, rufen Sie `next('route')` auf, um die Steuerung an die nächste Weiterleitung zu übergeben.

Hinweis

`next('route')` will work only in middleware functions that were loaded by using the `app.METHOD()` or `router.METHOD()` functions.

Dieses Beispiel zeigt einen Middleware-Sub-Stack, über den GET-Anforderungen zum Pfad `/user/:id` verarbeitet werden.

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

Dies ist ein Beispiel zur Verwendung der Middlewarefunktion `express.static` mit einem ausführlich dargestellten Optionsobjekt:

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

## Middleware auf Routerebene

Middleware auf Routerebene funktioniert in der gleichen Weise wie Middleware auf Anwendungsebene, mit dem einzigen Unterschied, dass sie an eine Instanz von `express.Router()` gebunden ist.

```
const router = express.Router()
```

Laden Sie Middleware auf Routerebene über die Funktionen `router.use()` und `router.METHOD()`.

Der folgende Beispielcode repliziert das Middlewaresystem, das oben für die Middleware auf Anwendungsebene gezeigt wird, durch Verwendung von Middleware auf Routerebene.

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

Dieses Beispiel zeigt einen Middleware-Sub-Stack, über den GET-Anforderungen zum Pfad `/user/:id` verarbeitet werden.

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

## Middleware für die Fehlerbehandlung

Middleware für die Fehlerbehandlung benötigt immer *vier* Argumente. Sie müssen vier Argumente angeben, um die Erkennung als Middlewarefunktion für die Fehlerbehandlung zu ermöglichen. Selbst wenn das Objekt `next` nicht verwenden müssen, müssen Sie dies angeben, um die Signatur beizubehalten. Andernfalls wird das Objekt `next` als reguläre Middleware interpretiert, sodass keine Fehlerbehandlung möglich ist.

Middlewarefunktionen für die Fehlerbehandlung werden in derselben Weise definiert wie andere Middlewarefunktionen, außer dass Fehlerbehandlungsfunktionen speziell bei Signaturen vier anstatt drei Argumente aufweisen `(err, req, res, next)`:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

Details zu Middleware für die Fehlerbehandlung siehe [Fehlerbehandlung](https://expressjs.com/de/guide/error-handling.html).

## Integrierte Middleware

Seit Version 4.x bestehen bei Express keine Abhängigkeiten zu [Connect](https://github.com/senchalabs/connect) mehr. Mit Ausnahme von `express.static` befinden sich nun alle Middlewarefunktionen, die bisher in Express enthalten waren, in separaten Modulen. Sehen Sie sich hierzu auch die [Liste der Middlewarefunktionen](https://github.com/senchalabs/connect#middleware) an.

Die einzige integrierte Middlewarefunktion in Express ist `express.static`.

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## Middleware anderer Anbieter

Mit Middleware anderer Anbieter können Sie Express-Anwendungen um neue Funktionalität erweitern.

Installieren Sie das Modul Node.js für die erforderliche Funktionalität. Laden Sie das Modul dann in Ihre Anwendung auf Anwendungsebene oder auf Routerebene.

Das folgende Beispiel veranschaulicht das Installieren und Laden der Middlewarefunktion `cookie-parser` für das Cookie-Parsing.

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

Eine nicht vollständige Liste zu den Middlewarefunktionen anderer Anbieter, die im Allgemeinen mit Express verwendet werden, finden Sie unter [Middleware anderer Anbieter](https://expressjs.com/de/resources/middleware.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/using-middleware.md          )
