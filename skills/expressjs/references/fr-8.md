# Migration vers Express 5 and more

# Migration vers Express 5

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# Migration vers Express 5

## Présentation

Express 5 n’est pas très différent d’Express 4 : les
modifications apportées à l’API ne sont pas aussi importantes qu’entre
les versions 3.0 et 4.0. Bien que l’API de base reste identique, des modifications radicales ont été apportées ; en d’autres termes, un programme Express 4 risque de ne pas fonctionner si
vous le mettez à jour pour utiliser Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

Vous pouvez alors exécuter les tests automatisés pour voir les
échecs et corriger les problèmes en fonction des mises à jour
répertoriées ci-dessous. Après avoir traité les échecs de test,
exécutez votre application pour détecter les erreurs qui se
produisent. Vous saurez tout de suite si l’application utilise des
méthodes ou des propriétés.

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

## Modifications dans Express 5

**Méthodes et propriétés supprimées**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [Noms de méthodes au pluriel](#plural)
- [Signe deux-points de tête dans l'argument du
  nom pour app.param(name, fn)](#leading)
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

**Améliorations**

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

**Modifié**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## Méthodes et propriétés supprimées

Si vous utilisez une de ces méthodes ou propriétés dans votre
application, elle tombera en panne. Vous devrez donc modifier votre
application après la mise à jour vers la version 5.

### app.del()

Express 5 ne prend plus en charge la fonction
`app.del()`. Si vous utilisez cette fonction, une
erreur est émise. Pour enregistrer des routes HTTP DELETE, utilisez la fonction
`app.delete()` à la place.

Initialement, `del` était utilisé au lieu de
`delete` car `delete` est un mot
clé réservé dans JavaScript. Cependant, à partir d’ECMAScript 6,
`delete` et les autres mots clés réservés peuvent
être utilisés en toute légalité comme noms de propriété.

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

La signature `app.param(fn)` servait à
modifier le comportement de la fonction
`app.param(name, fn)`. Elle est obsolète depuis la
version 4.11.0 et Express 5 ne la prend plus en charge.

### Noms de méthodes au pluriel

Les noms de méthode suivants ont été mis au pluriel. Dans Express 4, l’utilisation des anciennes méthodes ont généré un avertissement
d’obsolescence. Express 5 ne les prend plus du tout en charge :

`req.acceptsLanguage()` est remplacé par
`req.acceptsLanguages()`.

`req.acceptsCharset()` est remplacé par
`req.acceptsCharsets()`.

`req.acceptsEncoding()` est remplacé par
`req.acceptsEncodings()`.

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

### Signe deux-points (:) de tête dans le nom de la
fonction app.param(name, fn)

Le signe deux-points (:) de tête dans le nom de la fonction
`app.param(name, fn)` est une subsistance d’Express 3 et, pour des raisons de
compatibilité avec les versions antérieures, Express 4 la prenait en
charge avec un avis sur l’obsolescence. Express 5 l’ignore
automatiquement et utilise le paramètre de nom sans le préfixer d’un
signe deux-points.

Cela n’affectera normalement pas votre code si vous lisez la documentation Express 4
d’[app.param](https://expressjs.com/fr/4x/api.html#app.param) car cela ne mentionne pas le signe deux-points de tête.

### req.param(name)

Cette méthode potentiellement déroutante et dangereuse
d’extraction des données de formulaire a été supprimée. Vous devrez
désormais rechercher spécifiquement le nom du paramètre soumis dans
l’objet `req.params`, `req.body` ou `req.query`.

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

Express 5 ne prend plus en charge la signature
`res.json(obj, status)`. A la place, définissez le
statut et enchaînez-le à la méthode
`res.json()` comme suit :
`res.status(status).json(obj)`.

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

Express 5 ne prend plus en charge la signature
`res.jsonp(obj, status)`. A la place, définissez le
statut et enchaînez-le à la méthode `res.jsonp()`
comme suit : `res.status(status).jsonp(obj)`.

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

Express 5 ne prend plus en charge la signature
`res.send(obj, status)`. A la place, définissez le
statut et enchaînez-le à la méthode `res.send()`
comme suit : `res.status(status).send(obj)`.

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

Express 5 ne prend plus en charge la signature `res.send(statut)`, où *statut*
est un nombre. A la place, utilisez la fonction
`res.sendStatus(statusCode)`
qui définit le code de statut de l’en-tête de réponse HTTP et envoie
la version texte du code: “Not Found”, “Internal Server Error”, etc.
Si vous devez envoyer un nombre à l’aide de la fonction `res.send()`,
mettez ce nombre entre guillemets pour qu’Express ne l’interprète pas
comme une tentative d’utilisation de l’ancienne signature non prise en charge.

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

La fonction `res.sendfile()` a été remplacée
par une
version CamelCase `res.sendFile()` dans Express 5.

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

The `router.param(fn)` signature was used for modifying the behavior of the `router.param(name, fn)` function. Elle est obsolète depuis la
version 4.11.0 et Express 5 ne la prend plus en charge.

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

## Modifié

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

- Regexp characters are not supported. Par exemple :

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
Par exemple :

```
const server = app.listen(8080, '0.0.0.0', (error) => {
  if (error) {
    throw error // e.g. EADDRINUSE
  }
  console.log(`Listening on ${JSON.stringify(server.address())}`)
})
```

### app.router

L’objet `app.router`, qui a été supprimé dans Express 4, est revenu dans Express 5. Dans la version, cet objet
n’est qu’une référence dans le routeur Express de base, contrairement à Express 3, où une application devait le charger explicitement.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

Dans Express 4, la `req.host` retirait de
manière incorrecte le numéro de port s’il était présent. Dans Express 5, ce numéro de port est conservé.

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

## Améliorations

### res.render()

Cette méthode impose désormais un comportement asynchrone pour
tous les moteurs de vue. Cela évite les bogues générés par les
moteurs de vue qui avaient une implémentation synchrone et qui
ne prenaient pas en compte l’interface recommandée.

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/migrating-5.md          )

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/overriding-express-api.md          )

---

# Routage

> Apprenez à définir et à utiliser des routes dans les applications Express.js, y compris les méthodes de routes, les chemins de routes, les paramètres et l’utilisation de Router pour un routage modulaire.

# Routage

*Routage* fait référence à la définition de points finaux d’application (URI) et à la façon dont ils répondent aux demandes client.
Pour une introduction au routage, voir [Basic routing](https://expressjs.com/fr/starter/basic-routing.html).

Vous définissez le routage à l’aide des méthodes de l’objet app d’Express correspondant aux méthodes HTTP :
par exemple, `app.get()` pour les requêtes GET et `app.post` pour les requêtes POST. Pour la liste complète,
voir [app.METHOD](https://expressjs.com/fr/5x/api.html#app.METHOD). Vous pouvez également utiliser [app.all()](https://expressjs.com/fr/5x/api.html#app.all) pour gérer toutes les méthodes HTTP et [app.use()](https://expressjs.com/fr/5x/api.html#app.use) spécifier le middleware comme fonction de rappel (Voir [Utilisation du middleware](https://expressjs.com/fr/guide/using-middleware.html) pour plus de détails).

Ces méthodes de routage spécifient une fonction de rappel (parfois “appelée fonction de gestion”) qui est appelée lorsque l’application reçoit une requête correspondant à la route (point de terminaison) et à la méthode HTTP spécifiées. Autrement dit, l’application “écoute” les requêtes qui correspondent à la ou aux routes et à la ou aux méthodes spécifiées, et lorsqu’une correspondance est détectée, elle appelle la fonction de rappel définie.

En réalité, les méthodes de routage peuvent accepter plusieurs fonctions de rappel comme arguments.
Lorsqu’il y a plusieurs fonctions de rappel, il est important de fournier `next` comme argument à la fonction de rappel, puis d’appeler `next()` dans le corps de la fonction afin de passer le contrôle à la fonction de rappel suivante.

Le code suivant est un exemple de routage très basique.

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## Méthodes de routage

Une méthode de routage est dérivée de l’une des méthodes HTTP, et est liée à une instance de la classe `express`.

Le code suivant est un exemple de routes qui sont définies pour les méthodes GET et POST jusqu’à la route de l’application.

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

Express prend en charge des méthodes correspondant à toutes les méthodes de requête HTTP : `get`, `post`, etc. Pour la liste complète, voir [app.METHOD](https://expressjs.com/fr/5x/api.html#app.METHOD).
Pour la liste complète, voir [app.METHOD](https://expressjs.com/fr/5x/api.html#app.METHOD).

Il existe une méthode de routage spéciale, `app.all()`, qui n’est pas dérivée d’une méthode HTTP. Cette méthode est utilisée pour charger des fonctions middleware à un chemin d’accès pour toutes les méthodes de demande.

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## Chemins de routage

Les chemins de routage, combinés à une méthode de demande, définissent les noeuds finaux sur lesquels peuvent être effectuées les demandes. Les chemins de routage peuvent être des chaînes, des masques de chaîne ou des expressions régulières.

Caution

Dans Express 5, les caractères `?`, `+`, `*`, `[]`, et `()` sont traités différemment par rapport à la version 4. Veuillez consulter le [migration guide](https://expressjs.com/fr/guide/migrating-5.html#path-syntax) pour plus d’informations.

Caution

Dans Express 4, les caractères d’expression régulière tels que `$` doivent être échappés avec un `\`.

Note

Express utilise [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) pour faire correspondre les chemins de routes ; consultez la documentation de path-to-regexp pour connaître toutes les possibilités de définition des chemins de routes. [Express Route Tester](http://forbeslindesay.github.io/express-route-tester/) est un outil pratique permettant de tester des routes Express de base, bien qu’il ne prenne pas en charge le filtrage par motif.

Warning

Les chaînes de requête (query strings) ne font pas partie du chemin de la route.

### Il s’agit d’exemples de chemins de routage basés sur des chaînes.

Ce chemin de routage fera correspondre des demandes à la route racine, `/`.

```
app.get('/', (req, res) => {
  res.send('root')
})
```

Ce chemin de routage fera correspondre des demandes à `/about`.

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

Ce chemin de routage fera correspondre des demandes à `/random.text`.

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### Il s’agit d’exemples de chemins de routage basés sur des masques de chaîne.

Caution

Les motifs de chaînes (string patterns) ne fonctionnent plus dans Express 5. Veuillez consulter [migration guide](https://expressjs.com/fr/guide/migrating-5.html#path-syntax) pour plus d’informations.

Ce chemin de routage fait correspondre `acd` et `abcd`.

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

Ce chemin de routage fait correspondre `abcd`, `abbcd`, `abbbcd`, etc.

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

Ce chemin de routage fait correspondre `abcd`, `abxcd`, `abRABDOMcd`, `ab123cd`, etc.

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

Ce chemin de routage fait correspondre `/abe` et `/abcde`.

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### Exemples de chemins de routage basés sur des expressions régulières :

Ce chemin de routage fera correspondre tout élément dont le nom de chemin comprend la lettre “a”.

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

Ce chemin de routage fera correspondre `butterfly` et `dragonfly`, mais pas `butterflyman`, `dragonfly man`, etc.

```
app.get(/.*fly$/, (req, res) => {
  res.send('/.*fly$/')
})
```

## Les chaînes de requête ne font pas partie du chemin de routage.

Les paramètres de route sont des segments nommés de l’URL utilisés pour capturer les valeurs spécifiées à leur position dans l’URL. Les valeurs capturées sont placées dans l’objet `req.params`, avec le nom du paramètre de route spécifié dans le chemin comme clé correspondante.

```
Route path: /users/:userId/books/:bookId
Request URL: http://localhost:3000/users/34/books/8989
req.params: { "userId": "34", "bookId": "8989" }
```

Pour définir des routes avec des paramètres de route, il suffit de spécifier les paramètres dans le chemin de la route comme indiqué ci-dessous.

```
app.get('/users/:userId/books/:bookId', (req, res) => {
  res.send(req.params)
})
```

Le nom des paramètres de route doit être composé de “caractères alphanumériques” ([A-Za-z0-9_]).</div>

Comme le tiret (`-`) et le point (`.`) sont interprétés littéralement, ils peuvent être utilisés avec les paramètres de route à des fins pratiques.

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

Dans Express 5, les caractères Regexp ne sont pas pris en chage dans les chemins de route. Pour plus d’informations, veuillez consulter le [guide de migration](https://expressjs.com/fr/guide/migrating-5.html#path-syntax).

Pour mieux contrôler la chaîne exacte pouvant être capturée par un paramètre de route, vous pouvez ajouter une expression régulière entre parenthèses (`()`):

```
Route path: /user/:userId(\d+)
Request URL: http://localhost:3000/user/42
req.params: {"userId": "42"}
```

Warning

Comme l’expression régulière fait généralement partie d’une chaîne littérale, veillez à échapper tout caractère `\` avec un antislash supplémentaire, par exemple `\\d+`.

Warning

Dans Express 4.x, [le caractère*dans une expression régulière n’est pas interprété de manière habituelle](https://github.com/expressjs/express/issues/2495). Comme solution de contournement, utilisez `{0,}` au lieu de `*`. Cela sera probablement corrigé dans Express 5.

## Gestionnaires de routage

Vous pouvez fournir plusieurs fonctions de rappel qui se comportent comme des [middleware](https://expressjs.com/fr/guide/using-middleware.html) pour gérer une demande. La seule exception est que ces fonctions de rappel peuvent faire appel à `next('route')` pour ignorer les rappels de route restants. Vous pouvez utiliser ce mécanisme pour imposer des conditions préalables sur une route, puis passer aux routes suivantes si aucune raison n’est fournie pour traiter la route actuelle.

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

Dans cet exemple :

- `GET /user/5` → géré par la première route → envoie “User 5”
- `GET /user/0` → la première route appelle `next('route')`, en passant à la prochaine route correspondant à `/user/:id`

Les gestionnaires de route se trouvent sous la forme d’une fonction, d’un tableau de fonctions ou d’une combinaison des deux, tel qu’indiqué dans les exemples suivants.

Une fonction de rappel unique peut traiter une route. Par exemple :

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

Plusieurs fonctions de rappel peuvent traiter une route (n’oubliez pas de spécifier l’objet `next`). Par exemple :

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

Un tableau de fonctions de rappel peut traiter une route. Par exemple :

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

Une combinaison de fonctions indépendantes et des tableaux de fonctions peuvent gérer une route. Par exemple :

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

## Méthodes de réponse

Les méthodes de l’objet de réponse (`res`) décrites dans le tableau suivant peuvent envoyer une réponse au client, et mettre fin au cycle de demande-réponse. Si aucune de ces méthodes n’est appelée par un gestionnaire de routage, la demande du client restera bloquée.

| Méthode | Description |
| --- | --- |
| res.download() | Vous invite à télécharger un fichier. |
| res.end() | Met fin au processus de réponse. |
| res.json() | Envoie une réponse JSON. |
| res.jsonp() | Envoie une réponse JSON avec une prise en charge JSONP. |
| res.redirect() | Redirige une demande. |
| res.render() | Génère un modèle de vue. |
| res.send() | Envoie une réponse de divers types. |
| res.sendFile() | Envoyer un fichier sous forme de flux octet. |
| res.sendStatus() | Définit le code de statut de réponse et envoie sa représentation sous forme de chaîne comme corps de réponse. |

## app.route()

Vous pouvez créer des gestionnaires de routage sous forme de chaîne pour un chemin de routage en utilisant `app.route()`.
Etant donné que le chemin est spécifié à une seul emplacement, la création de routes modulaires est utile car elle réduit la redondance et les erreurs. Pour plus d’informations sur les routes, voir la [documentation Router()](https://expressjs.com/fr/4x/api.html#router).

Voici quelques exemples de gestionnaires de chemin de chaînage définis à l’aide de `app.route()`.

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

Utilisez la classe `express.Router` pour créer des gestionnaires de route modulaires et pouvant être montés. Une instance `Router` est un middleware et un système de routage complet ; pour cette raison, elle est souvent appelée “mini-app”.

L’exemple suivant créé une routeur en tant que module, charge une fonction middleware, définit des routes et monte le module de routeur sur un chemin dans l’application principale.

Créez un fichier de routage nommé `birds.js` dans le répertoire app, avec le contenu suivant :

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

Puis, chargez le module de routage dans l’application :

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

L’application pourra dorénavant gérer des demandes dans `/birds` et `/birds/about`, et appeler la fonction middleware `timeLog` spécifique à la route.

Mais si la route parente `/birds` possède des paramètres de chemin, ils ne seront pas accessibles par défaut depuis les sous-routes. Pour qu’ils soient accessibles, vous devez passer l’option `mergeParams` au constructeur de Router [reference](https://expressjs.com/fr/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

    [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/routing.md          )
