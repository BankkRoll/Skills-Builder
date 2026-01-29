# Migración a Express 5 and more

# Migración a Express 5

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# Migración a Express 5

## Overview

Express 5 no es muy diferente de Express 4: los cambios en la API no son tan significativos como los de la migración de 3.0 a 4.0. Aunque la API básica permanece igual, continúa habiendo cambios que rompen el código existente; es decir, un programa de Express 4 existente no funcionará si lo actualiza para que utilice Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

A continuación, puede ejecutar las pruebas automatizadas para ver qué falla y solucionar los problemas según las actualizaciones siguientes. Después de solucionar los errores de las pruebas, ejecute la aplicación para ver qué errores se producen. Verá rápidamente si la aplicación utiliza métodos o propiedades que no están soportados.

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

## Changes in Express 5

**Métodos y propiedades eliminados**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [Nombres de métodos pluralizados](#plural)
- [Dos puntos delanteros en el argumento de nombre en app.param(name, fn)](#leading)
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

**Mejoras**

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

**Modificados**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## Removed methods and properties

Si utiliza cualquiera de estos métodos o propiedades en la aplicación, se bloqueará. Por lo tanto, deberá cambiar la aplicación después de actualizar a la versión 5.

### app.del()

Express 5 ya no da soporte a la función `app.del()`. Si utiliza esta función, se genera un error. Para registrar las rutas HTTP DELETE, utilice la función `app.delete()` en su lugar.

Inicialmente, se utilizaba `del` en lugar de `delete`, porque `delete` es una palabra clave reservada en JavaScript. No obstante, a partir de ECMAScript 6, `delete` y otras palabras clave reservadas pueden utilizarse correctamente como nombres de propiedad.

Nota

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

La firma `app.param(fn)` se utilizaba para modificar el comportamiento de la función `app.param(name, fn)`. Está en desuso desde v4.11.0 y Express 5 ya no le da soporte.

### Pluralized method names

Los siguientes nombres de métodos se han pluralizado. En Express 4, el uso de los métodos antiguos daba como resultado un aviso de obsolescencia. Express 5 ya no les da soporte:

`req.acceptsLanguage()` se ha sustituido por `req.acceptsLanguages()`.

`req.acceptsCharset()` se ha sustituido por `req.acceptsCharsets()`.

`req.acceptsEncoding()` se ha sustituido por `req.acceptsEncodings()`.

Nota

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

### Dos puntos (:) delanteros en el nombre de app.param(name, fn)

El carácter de dos puntos (:) delanteros en el nombre de la función `app.param(name, fn)` es un remanente de Express 3 y, a efectos de retrocompatibilidad, Express 4 le daba soporte con un aviso de obsolescencia. Express 5 lo ignorará de forma silenciosa y utilizará el parámetro de nombre sin añadir el prefijo de dos puntos.

Esto no afectará al código si sigue la documentación de Express 4 de [app.param](https://expressjs.com/es/4x/api.html#app.param), ya que no hace ninguna referencia a los dos puntos delanteros.

### req.param(name)

Este método potencialmente confuso y peligroso de recuperar datos de formulario se ha eliminado. No necesitará buscar específicamente el nombre de parámetro enviado en el objeto `req.params`, `req.body` o `req.query`.

Nota

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

Express 5 ya no da soporte a la firma `res.json(obj, status)`. En su lugar, establezca el estado y encadénelo al método `res.json()` de la siguiente manera: `res.status(status).json(obj)`.

Nota

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

Express 5 ya no da soporte a la firma `res.jsonp(obj, status)`. En su lugar, establezca el estado y encadénelo al método `res.jsonp()` de la siguiente manera: `res.status(status).jsonp(obj)`.

Nota

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

Express 5 ya no da soporte a la firma `res.send(obj, status)`. En su lugar, establezca el estado y encadénelo al método `res.send()` de la siguiente manera: `res.status(status).send(obj)`.

Nota

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

Nota

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

Nota

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

Express 5 ya no da soporte a la firma `res.send(status)`, donde *status* es un número. En su lugar, utilice la función `res.sendStatus(statusCode)`, que establece el código de estado de la cabecera de respuesta HTTP y envía la versión de texto del código: “Not Found”, “Internal Server Error”, etc.
Si necesita enviar un número utilizando la función `res.send()`, escríbalo entre comillas para convertirlo en una serie, para que Express no lo interprete como un intento de utilizar la firma antigua no soportada.

Nota

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

La función `res.sendfile()` se ha sustituido por una versión de la función `res.sendFile()` con cada palabra en mayúscula en Express 5.

**Note:** In Express 5, `res.sendFile()` uses the `mime-types` package for MIME type detection, which returns different Content-Type values than Express 4 for several common file types:

- JavaScript files (.js): now “text/javascript” instead of “application/javascript”
- JSON files (.json): now “application/json” instead of “text/json”
- CSS files (.css): now “text/css” instead of “text/plain”
- XML files (.xml): now “application/xml” instead of “text/xml”
- Font files (.woff): now “font/woff” instead of “application/font-woff”
- SVG files (.svg): now “image/svg+xml” instead of “application/svg+xml”

Nota

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

The `router.param(fn)` signature was used for modifying the behavior of the `router.param(name, fn)` function. Está en desuso desde v4.11.0 y Express 5 ya no le da soporte.

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

## Modificados

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

Nota

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

El objeto `app.router`, que se ha eliminado en Express 4, ha vuelto en Express 5. En la nueva versión, este objeto es sólo una referencia al direccionador de Express base, a diferencia de en Express 3, donde una aplicación debía cargarlo explícitamente.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

En Express 4, la función `req.host` fragmentaba incorrectamente el número de puerto si estaba presente. In Express 5, the port number is maintained.

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

## Improvements

### res.render()

Este método ahora impone un comportamiento asíncrono para todos los motores de vistas, lo que evita los errores provocados por los motores de vistas que tenían una implementación síncrona e incumplían la interfaz recomendada.

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/migrating-5.md          )

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/overriding-express-api.md          )

---

# Direccionamiento

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# Direccionamiento

*Direccionamiento* hace referencia a la definición de puntos finales de aplicación (URI) y cómo responden a las solicitudes de cliente.
Para ver una introducción al direccionamiento, consulte [Direccionamiento básico](https://expressjs.com/es/starter/basic-routing.html).

You define routing using methods of the Express `app` object that correspond to HTTP methods;
for example, `app.get()` to handle GET requests and `app.post` to handle POST requests. For a full list,
see [app.METHOD](https://expressjs.com/es/5x/api.html#app.METHOD). You can also use [app.all()](https://expressjs.com/es/5x/api.html#app.all) to handle all HTTP methods and [app.use()](https://expressjs.com/es/5x/api.html#app.use) to
specify middleware as the callback function (See [Using middleware](https://expressjs.com/es/guide/using-middleware.html) for details).

These routing methods specify a callback function (sometimes called “handler functions”) called when the application receives a request to the specified route (endpoint) and HTTP method. In other words, the application “listens” for requests that match the specified route(s) and method(s), and when it detects a match, it calls the specified callback function.

In fact, the routing methods can have more than one callback function as arguments.
With multiple callback functions, it is important to provide `next` as an argument to the callback function and then call `next()` within the body of the function to hand off control
to the next callback.

The following code is an example of a very basic route.

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## Route methods

A route method is derived from one of the HTTP methods, and is attached to an instance of the `express` class.

El siguiente código es un ejemplo de las rutas que se definen para los métodos GET y POST a la raíz de la aplicación.

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
For a full list, see [app.METHOD](https://expressjs.com/es/5x/api.html#app.METHOD).

Hay un método de direccionamiento especial, `app.all()`, que no se deriva de ningún método HTTP. Este método se utiliza para cargar funciones de middleware en una vía de acceso para todos los métodos de solicitud. En el siguiente ejemplo, el manejador se ejecutará para las solicitudes a “/secret”, tanto si utiliza GET, POST, PUT, DELETE, como cualquier otro método de solicitud HTTP soportado en el [módulo http](https://nodejs.org/api/http.html#http_http_methods).

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## Vías de acceso de ruta

Las vías de acceso de ruta, en combinación con un método de solicitud, definen los puntos finales en los que pueden realizarse las solicitudes. Las vías de acceso de ruta pueden ser series, patrones de serie o expresiones regulares.

Precaución

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/es/guide/migrating-5.html#path-syntax) for more information.

Precaución

In express 4, regular expression characters such as `$` need to be escaped with a `\`.

Nota

Express uses [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) for matching the route paths; see the path-to-regexp documentation for all the possibilities in defining route paths. [Express Route Tester](http://forbeslindesay.github.io/express-route-tester/) es una herramienta muy útil para probar rutas básicas de Express, aunque no da soporte a la coincidencia de patrones.

Advertencia

Query strings are not part of the route path.

### Route paths based on strings

Esta vía de acceso de ruta coincidirá con las solicitudes a la ruta raíz, `/`.

```
app.get('/', (req, res) => {
  res.send('root')
})
```

Esta vía de acceso de ruta coincidirá con las solicitudes a `/about`.

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

Esta vía de acceso de ruta coincidirá con las solicitudes a `/random.text`.

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### Route paths based on string patterns

Precaución

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/es/guide/migrating-5.html#path-syntax) for more information.

Esta vía de acceso de ruta coincidirá con `acd` y `abcd`.

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

Esta vía de acceso de ruta coincidirá con `abcd`, `abbcd`, `abbbcd`, etc.

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

Esta vía de acceso de ruta coincidirá con `abcd`, `abxcd`, `abRABDOMcd`, `ab123cd`, etc.

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

Esta vía de acceso de ruta coincidirá con `/abe` y `/abcde`.

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### Ejemplos de vías de acceso de ruta basadas en expresiones regulares:

Esta vía de acceso de ruta coincidirá con cualquier valor con una “a” en el nombre de la ruta.

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

Esta vía de acceso de ruta coincidirá con `butterfly` y `dragonfly`, pero no con `butterflyman`, `dragonfly man`, etc.

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

Precaución

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/es/guide/migrating-5.html#path-syntax).

To have more control over the exact string that can be matched by a route parameter, you can append a regular expression in parentheses (`()`):

```
Route path: /user/:userId(\d+)
Request URL: http://localhost:3000/user/42
req.params: {"userId": "42"}
```

Advertencia

Because the regular expression is usually part of a literal string, be sure to escape any `\` characters with an additional backslash, for example `\\d+`.

Advertencia

In Express 4.x, [the*character in regular expressions is not interpreted in the usual way](https://github.com/expressjs/express/issues/2495). As a workaround, use `{0,}` instead of `*`. This will likely be fixed in Express 5.

## Route handlers

Puede proporcionar varias funciones de devolución de llamada que se comportan como [middleware](https://expressjs.com/es/guide/using-middleware.html) para manejar una solicitud. La única excepción es que estas devoluciones de llamada pueden invocar `next('route')` para omitir el resto de las devoluciones de llamada de ruta. Puede utilizar este mecanismo para imponer condiciones previas en una ruta y, a continuación, pasar el control a las rutas posteriores si no hay motivo para continuar con la ruta actual.

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

Los manejadores de rutas pueden tener la forma de una función, una matriz de funciones o combinaciones de ambas, como se muestra en los siguientes ejemplos.

Una función de devolución de llamada individual puede manejar una ruta. For example:

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

Más de una función de devolución de llamada puede manejar una ruta (asegúrese de especificar el objeto `next`). For example:

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

Una matriz de funciones de devolución de llamada puede manejar una ruta. For example:

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

Una combinación de funciones independientes y matrices de funciones puede manejar una ruta. For example:

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

## Response methods

Los métodos en el objeto de respuesta (`res`) de la tabla siguiente pueden enviar una respuesta al cliente y terminar el ciclo de solicitud/respuestas. Si ninguno de estos métodos se invoca desde un manejador de rutas, la solicitud de cliente se dejará colgada.

| Method | Description |
| --- | --- |
| res.download() | Solicita un archivo para descargarlo. |
| res.end() | Finaliza el proceso de respuesta. |
| res.json() | Envía una respuesta JSON. |
| res.jsonp() | Send a JSON response with JSONP support. |
| res.redirect() | Redirecciona una solicitud. |
| res.render() | Representa una plantilla de vista. |
| res.send() | Envía una respuesta de varios tipos. |
| res.sendFile() | Envía un archivo como una secuencia de octetos. |
| res.sendStatus() | Establece el código de estado de la respuesta y envía su representación de serie como el cuerpo de respuesta. |

## app.route()

Puede crear manejadores de rutas encadenables para una vía de acceso de ruta utilizando `app.route()`.
Como la vía de acceso se especifica en una única ubicación, la creación de rutas modulares es muy útil, al igual que la reducción de redundancia y errores tipográficos. Para obtener más información sobre las rutas, consulte: [Documentación de Router()](https://expressjs.com/es/4x/api.html#router).

A continuación, se muestra un ejemplo de manejadores de rutas encadenados que se definen utilizando `app.route()`.

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

Utilice la clase `express.Router` para crear manejadores de rutas montables y modulares. Una instancia `Router` es un sistema de middleware y direccionamiento completo; por este motivo, a menudo se conoce como una “miniaplicación”.

El siguiente ejemplo crea un direccionador como un módulo, carga una función de middleware en él, define algunas rutas y monta el módulo de direccionador en una vía de acceso en la aplicación principal.

Cree un archivo de direccionador denominado `birds.js` en el directorio de la aplicación, con el siguiente contenido:

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

A continuación, cargue el módulo de direccionador en la aplicación:

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

La aplicación ahora podrá manejar solicitudes a `/birds` y `/birds/about`, así como invocar la función de middleware `timeLog` que es específica de la ruta.

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/es/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/routing.md          )
