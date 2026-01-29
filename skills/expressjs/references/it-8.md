# Passaggio a Express 5 and more

# Passaggio a Express 5

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# Passaggio a Express 5

## Panoramica

Express 5 non è molto differente da Express 4: le modifiche all’API non sono così importanti come quelle che sono state effettuate nel passaggio dalla 3.0 alla 4.0. Anche se le API di base sono le stesse, ci sono comunque delle modifiche importanti; in altre parole, un programma Express 4 esistente potrebbe non funzionare se lo si aggiorna per utilizzare Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

È quindi possibile eseguire i test automatizzati per trovare errori e correggere i problemi in base agli aggiornamenti elencati di seguito. Dopo aver gestito gli errori del test, avviare l’applicazione per verificare gli errori. Si noterà subito se l’applicazione utilizza qualsiasi metodo o proprietà non supportati.

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

## Modifiche in Express 5

**Proprietà e metodi rimossi**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [Nomi di metodi al plurale](#plural)
- [Due punti nell'argomento del nome in app.param(name, fn)](#leading)
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

**Miglioramenti**

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

**Modificato**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## Proprietà e metodi rimossi

Se si utilizza uno dei seguenti metodi o proprietà nell’applicazione, quest’ultima si chiuderà in modo anomalo. Quindi, sarà necessario modificare l’applicazione dopo aver effettuato l’aggiornamento alla versione 5.

### app.del()

Express 5 non supporta più la funzione `app.del()`. Se si utilizza questa funzione verrà generato un errore. Per registrare le route HTTP DELETE, utilizzare al contrario la funzione `app.delete()`.

Inizialmente era stato utilizzato il comando `del` al posto di `delete`, perché `delete` è una parola chiave riservata in JavaScript. Tuttavia, a partire da ECMAScript 6, `delete` e altre parole chiave riservate possono essere utilizzate liberamente come nomi di proprietà.

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

La firma `app.param(fn)` è stata utilizzata per modificare la funzionalità della funzione `app.param(name, fn)`. È stata considerata obsoleta a partire dalla v4.11.0 e non è più supportata in Express 5.

### Nomi di metodi al plurale

I seguenti nomi di metodi sono stati messi al plurale. In Express 4, l’utilizzo di vecchi metodi ha dato origine ad avvisi di deprecazione. Express 5 non li supporta più in alcun modo:

`req.acceptsLanguage()` è stato sostituito con `req.acceptsLanguages()`.

`req.acceptsCharset()` è stato sostituito con `req.acceptsCharsets()`.

`req.acceptsEncoding()` è stato sostituito con `req.acceptsEncodings()`.

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

### Due punti (:) nel nome per app.param(name, fn)

I due punti (:) nel nome della funzione `app.param(name, fn)` è una eredità di Express 3 e per il bene della compatibilità con le versioni precedenti, Express 4 supporta questa condizione ma comunque fornendo un messaggio di avviso di deprecazione. Express 5 lo ignorerà senza avvisi e utilizzerà il parametro nome senza inserire i due punti.

Questa procedura non dovrebbe influenzare il codice se si segue correttamente la documentazione di Express 4 di [app.param](https://expressjs.com/it/4x/api.html#app.param), poiché non si parla dei due punti.

### req.param(name)

Questo metodo poco chiaro e molto pericoloso che si utilizzava per richiamare i dati del modulo è stato rimosso. Ora sarà necessario ricercare il nome del parametro inviato nell’oggetto `req.params`, `req.body` o `req.query`.

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

Express 5 non supporta più la firma `res.json(obj, status)`. Al contrario, impostare lo stato e successivamente associarlo al metodo `res.json()` come segue: `res.status(status).json(obj)`.

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

Express 5 non supporta più la firma `res.jsonp(obj, status)`. Al contrario, impostare lo stato e successivamente associarlo al metodo `res.jsonp()` come segue: `res.status(status).jsonp(obj)`.

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

Express 5 non supporta più la firma `res.send(obj, status)`. Al contrario, impostare lo stato e successivamente associarlo al metodo `res.send()` come segue: `res.status(status).send(obj)`.

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

Express 5 no longer supports the signature `res.send(obj, status)`. Instead, set the status and then chain it to the `res.send()` method like this: `res.status(status).send(obj)`.

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

Express 5 non supporta più la firma `res.send(status)`, dove *status* è un numero. Al contrario, utilizzare la funzione `res.sendStatus(statusCode)`, la quale imposta il codice di stato dell’intestazione della risposta HTTP e invia la versione di testo del codice: “Non trovato”, “Errore interno del server” e così via.
Se è necessario inviare un numero utilizzando la funzione `res.send()`, citare il numero per convertirlo in una stringa, in modo tale che Express non lo interpreti come un tentativo di utilizzo di una firma vecchia non supportata.

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

La funzione `res.sendfile()` è stata sostituita da una versione in cui ogni frase composta inizia con una lettera maiuscola che utilizza ad esempio `res.sendFile()` in Express 5.

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

The `router.param(fn)` signature was used for modifying the behavior of the `router.param(name, fn)` function. È stata considerata obsoleta a partire dalla v4.11.0 e non è più supportata in Express 5.

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

## Modificato

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

- Regexp characters are not supported. Ad esempio:

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
Ad esempio:

```
const server = app.listen(8080, '0.0.0.0', (error) => {
  if (error) {
    throw error // e.g. EADDRINUSE
  }
  console.log(`Listening on ${JSON.stringify(server.address())}`)
})
```

### app.router

L’oggetto `app.router`, che era stato rimosso in Express 4, è ritornato in Express 5. Nella nuova versione, questo oggetto è solo un riferimento al router Express di base, diversamente da Express 3, in cui un’applicazione aveva il compito esplicito di caricarlo.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

In Express 4, la funzione `req.host` andava a rimuovere in modo non corretto il numero porta nel caso fosse stato presente. In Express 5 il numero porta viene conservato.

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

## Miglioramenti

### res.render()

Questo metodo ora potenzia i funzionamenti asincroni per tutti i motori di visualizzazione, evitando i bug causati dai motori di visualizzazione con un’implementazione sincrona e che violavano l’interfaccia consigliata.

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/guide/migrating-5.md          )

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/guide/overriding-express-api.md          )

---

# Routing

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# Routing

*Routing* fa riferimento alla definizione di endpoint dell’applicazione (URI) e alla loro modalità di risposta alle richieste del client.
Per un’introduzione al concetto di routing, consultare la sezione [Routing di base](https://expressjs.com/it/starter/basic-routing.html).

You define routing using methods of the Express `app` object that correspond to HTTP methods;
for example, `app.get()` to handle GET requests and `app.post` to handle POST requests. For a full list,
see [app.METHOD](https://expressjs.com/it/5x/api.html#app.METHOD). You can also use [app.all()](https://expressjs.com/it/5x/api.html#app.all) to handle all HTTP methods and [app.use()](https://expressjs.com/it/5x/api.html#app.use) to
specify middleware as the callback function (See [Using middleware](https://expressjs.com/it/guide/using-middleware.html) for details).

These routing methods specify a callback function (sometimes called “handler functions”) called when the application receives a request to the specified route (endpoint) and HTTP method. In other words, the application “listens” for requests that match the specified route(s) and method(s), and when it detects a match, it calls the specified callback function.

In fact, the routing methods can have more than one callback function as arguments.
With multiple callback functions, it is important to provide `next` as an argument to the callback function and then call `next()` within the body of the function to hand off control
to the next callback.

Il codice seguente è un esempio di una route veramente di base.

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## Metodi di route

Un metodo di route deriva da uno dei metodi HTTP ed è collegato ad un’istanza delle classe `express`.

Il codice seguente è un esempio di route definite per i metodi GET e POST nella root dell’app.

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
For a full list, see [app.METHOD](https://expressjs.com/it/5x/api.html#app.METHOD).

Esiste un metodo di routing speciale, `app.all()`, che non deriva da alcun metodo HTTP. Questo metodo viene utilizzato per caricare funzioni middleware in un percorso per tutti i metodi di richiesta.

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## Percorsi di route

I percorsi di route, in combinazione con un metodo di richiesta, definiscono gli endpoint a cui possono essere rivolte richieste. I percorsi di route possono essere stringhe, modelli di stringa o espressioni regolari.

Caution

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/it/guide/migrating-5.html#path-syntax) for more information.

Caution

In express 4, regular expression characters such as `$` need to be escaped with a `\`.

Note

Express uses [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) for matching the route paths; see the path-to-regexp documentation for all the possibilities in defining route paths. [Express Route Tester](http://forbeslindesay.github.io/express-route-tester/) è uno strumento utile per il test delle route Express di base, anche se non supporta la corrispondenza di modelli.

Warning

Query strings are not part of the route path.

### Ecco alcuni esempi di percorsi di route basati su stringhe.

Questo percorso di route corrisponderà a richieste nella route root, `/`.

```
app.get('/', (req, res) => {
  res.send('root')
})
```

Questo percorso di route corrisponderà a richieste in `/about`.

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

Questo percorso di route corrisponderà a richieste in `/random.text`.

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### Ecco alcuni esempi di percorsi di route basati su modelli di stringa.

Caution

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/it/guide/migrating-5.html#path-syntax) for more information.

Questo percorso di route corrisponderà a `acd` e `abcd`.

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

Questo percorso di route corrisponderà a `abcd`, `abbcd`, `abbbcd` e così via.

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

Questo percorso di route corrisponderà a `abcd`, `abxcd`, `abRABDOMcd`, `ab123cd` e così via.

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

Questo percorso di route corrisponderà a `/abe` e `/abcde`.

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### Esempi di percorsi di route basati su espressioni regolari:

Questo percorso di route corrisponderà a qualsiasi elemento con “a” nel nome route.

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

Questo percorso di route corrisponderà a `butterfly` e `dragonfly`, ma non a `butterflyman`, `dragonfly man` e così via.

```
app.get(/.*fly$/, (req, res) => {
  res.send('/.*fly$/')
})
```

## Le stringhe di query non fanno parte del percorso di route.

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

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/it/guide/migrating-5.html#path-syntax).

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

## Handler di route

È possibile fornire molteplici funzioni di callback che si comportino come [middleware](https://expressjs.com/it/guide/using-middleware.html) per gestire una richiesta. La sola eccezione è rappresentata dal fatto che queste callback potrebbero richiamare `next('route')` per ignorare le callback di route restanti. È possibile utilizzare questo meccanismo per imporre pre-condizioni su una route, quindi, passare il controllo a route successive, nel caso non ci siano motivi per proseguire con la route corrente.

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

Gli handler di route possono avere il formato di una funzione, di un array di funzioni o di combinazioni di entrambi, come illustrato nei seguenti esempi.

Una singola funzione di callback può gestire una route. Ad esempio:

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

Più funzioni di callback possono gestire una route (assicurarsi di specificare l’oggetto `next`). Ad esempio:

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

Un array di funzioni callback possono gestire una route. Ad esempio:

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

Una combinazione di funzioni indipendenti e array di funzioni può gestire una route. Ad esempio:

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

## Metodi di risposta

I metodi sull’oggetto risposta (`res`) nella seguente tabella possono inviare una risposta al client e terminare il ciclo richiesta-risposta. Se nessuno di questi metodi viene richiamato da un handler di route, la richiesta del client verrà lasciata in sospeso.

| Metodo | Descrizione |
| --- | --- |
| res.download() | Richiedere un file da scaricare. |
| res.end() | Terminare il processo di risposta. |
| res.json() | Inviare una risposta JSON. |
| res.jsonp() | Inviare una risposta JSON con supporto JSONP. |
| res.redirect() | Reindirizzare una richiesta. |
| res.render() | Eseguire il rendering di un template di vista. |
| res.send() | Inviare una risposta di vari tipi. |
| res.sendFile | Inviare un file come un flusso di ottetti. |
| res.sendStatus() | Impostare il codice di stato della risposta e inviare la relativa rappresentazione di stringa come corpo della risposta. |

## app.route()

È possibile creare handler di route concatenabili per un percorso di route, utilizzando `app.route()`.
Poiché il percorso è specificato in una singola ubicazione, la creazione di route modulari è utile, come lo è la riduzione della ridondanza e degli errori tipografici. Per ulteriori informazioni sulle route, consultare: [Documentazione su Router()](https://expressjs.com/it/4x/api.html#router).

Ecco un esempio di handler di route concatenati, definiti utilizzando `app.route()`.

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

Utilizzare la classe `express.Router` per creare handler di route modulari, montabili. Un’istanza `Router` è un middleware e un sistema di routing completo; per questa ragione, spesso si definisce “mini-app”.

Nel seguente esempio si crea un router come modulo, si carica al suo interno una funzione middleware, si definiscono alcune route e si monta un modulo router su un percorso nell’app principale.

Creare un file router denominato `birds.js` nella directory app, con il seguente contenuto:

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

Successivamente, caricare il modulo router nell’applicazione:

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

L’app ora sarà in grado di gestire richieste a `/birds` e `/birds/about`, oltre a richiamare la funzione middleware `timeLog`, specifica per la route.

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/it/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/guide/routing.md          )
