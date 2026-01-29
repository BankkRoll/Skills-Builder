# Moving to Express 4 and more

# Moving to Express 4

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# Moving to Express 4

## Overview

Express 4 is a breaking change from Express 3. That means an existing Express 3 app will *not* work if you update the Express version in its dependencies.

This article covers:

- [Changes in Express 4](#changes).
- [An example](#example-migration) of migrating an Express 3 app to Express 4.
- [Upgrading to the Express 4 app generator](#app-gen).

## Changes in Express 4

There are several significant changes in Express 4:

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [Changes to the routing system.](#routing)
- [Various other changes.](#other-changes)

See also:

- [New features in 4.x.](https://github.com/expressjs/express/wiki/New-features-in-4.x)
- [Migrating from 3.x to 4.x.](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)

### Changes to Express core and middleware system

Express 4 no longer depends on Connect, and removes all built-in
middleware from its core, except for the `express.static` function. This means that
Express is now an independent routing and middleware web framework, and
Express versioning and releases are not affected by middleware updates.

Without built-in middleware, you must explicitly add all the
middleware that is required to run your app. Simply follow these steps:

1. Install the module: `npm install --save <module-name>`
2. In your app, require the module: `require('module-name')`
3. Use the module according to its documentation: `app.use( ... )`

The following table lists Express 3 middleware and their counterparts in Express 4.

| Express 3 | Express 4 |
| --- | --- |
| express.bodyParser | body-parser+multer |
| express.compress | compression |
| express.cookieSession | cookie-session |
| express.cookieParser | cookie-parser |
| express.logger | morgan |
| express.session | express-session |
| express.favicon | serve-favicon |
| express.responseTime | response-time |
| express.errorHandler | errorhandler |
| express.methodOverride | method-override |
| express.timeout | connect-timeout |
| express.vhost | vhost |
| express.csrf | csurf |
| express.directory | serve-index |
| express.static | serve-static |

Here is the [complete list](https://github.com/senchalabs/connect#middleware) of Express 4 middleware.

In most cases, you can simply replace the old version 3 middleware with
its Express 4 counterpart. For details, see the module documentation in
GitHub.

#### app.useaccepts parameters

In version 4 you can use a variable parameter to define the path where middleware functions are loaded, then read the value of the parameter from the route handler.
For example:

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### The routing system

Apps now implicitly load routing middleware, so you no longer have to
worry about the order in which middleware is loaded with respect to
the `router` middleware.

The way you define routes is unchanged, but the routing system has two
new features to help organize your routes:

- A new method, `app.route()`, to create chainable route handlers for a route path.
- A new class, `express.Router`, to create modular mountable route handlers.

#### app.route()method

The new `app.route()` method enables you to create chainable route handlers
for a route path. Because the path is specified in a single location, creating modular routes is helpful, as is reducing redundancy and typos. For more
information about routes, see [Router()documentation](https://expressjs.com/en/4x/api.html#router).

Here is an example of chained route handlers that are defined by using the `app.route()` function.

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

#### express.Routerclass

The other feature that helps to organize routes is a new class,
`express.Router`, that you can use to create modular mountable
route handlers. A `Router` instance is a complete middleware and
routing system; for this reason it is often referred to as a “mini-app”.

The following example creates a router as a module, loads middleware in
it, defines some routes, and mounts it on a path on the main app.

For example, create a router file named `birds.js` in the app directory,
with the following content:

```
var express = require('express')
var router = express.Router()

// middleware specific to this router
router.use((req, res, next) => {
  console.log('Time: ', Date.now())
  next()
})
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

Then, load the router module in the app:

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

The app will now be able to handle requests to the `/birds` and
`/birds/about` paths, and will call the `timeLog`
middleware that is specific to the route.

### Other changes

The following table lists other small but important changes in Express 4:

| Object | Description |
| --- | --- |
| Node.js | Express 4 requires Node.js 0.10.x or later and has dropped support for
Node.js 0.8.x. |
| http.createServer() | Thehttpmodule is no longer needed, unless you need to directly work with it (socket.io/SPDY/HTTPS). The app can be started by using theapp.listen()function. |
| app.configure() | Theapp.configure()function has been removed.  Use theprocess.env.NODE_ENVorapp.get('env')function to detect the environment and configure the app accordingly. |
| json spaces | Thejson spacesapplication property is disabled by default in Express 4. |
| req.accepted() | Usereq.accepts(),req.acceptsEncodings(),req.acceptsCharsets(), andreq.acceptsLanguages(). |
| res.location() | No longer resolves relative URLs. |
| req.params | Was an array; now an object. |
| res.locals | Was a function; now an object. |
| res.headerSent | Changed tores.headersSent. |
| app.route | Now available asapp.mountpath. |
| res.on('header') | Removed. |
| res.charset | Removed. |
| res.setHeader('Set-Cookie', val) | Functionality is now limited to setting the basic cookie value. Useres.cookie()for added functionality. |

## Example app migration

Here is an example of migrating an Express 3 application to Express 4.
The files of interest are `app.js` and `package.json`.

### Version 3 app

#### app.js

Consider an Express v.3 application with the following `app.js` file:

```
var express = require('express')
var routes = require('./routes')
var user = require('./routes/user')
var http = require('http')
var path = require('path')

var app = express()

// all environments
app.set('port', process.env.PORT || 3000)
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')
app.use(express.favicon())
app.use(express.logger('dev'))
app.use(express.methodOverride())
app.use(express.session({ secret: 'your secret here' }))
app.use(express.bodyParser())
app.use(app.router)
app.use(express.static(path.join(__dirname, 'public')))

// development only
if (app.get('env') === 'development') {
  app.use(express.errorHandler())
}

app.get('/', routes.index)
app.get('/users', user.list)

http.createServer(app).listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

#### package.json

The accompanying version 3 `package.json` file might look
  something like this:

```
{
  "name": "application-name",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "3.12.0",
    "pug": "*"
  }
}
```

### Process

Begin the migration process by installing the required middleware for the
Express 4 app and updating Express and Pug to their respective latest
version with the following command:

```
$ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
```

Make the following changes to `app.js`:

1. The built-in Express middleware functions `express.favicon`,
   `express.logger`, `express.methodOverride`,
   `express.session`, `express.bodyParser` and
   `express.errorHandler` are no longer available on the
   `express` object. You must install their alternatives
   manually and load them in the app.
2. You no longer need to load the `app.router` function.
   It is not a valid Express 4 app object, so remove the
   `app.use(app.router);` code.
3. Make sure that the middleware functions are loaded in the correct order - load `errorHandler` after loading the app routes.

### Version 4 app

#### package.json

Running the above `npm` command will update `package.json` as follows:

```
{
  "name": "application-name",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "body-parser": "^1.5.2",
    "errorhandler": "^1.1.1",
    "express": "^4.8.0",
    "express-session": "^1.7.2",
    "pug": "^2.0.0",
    "method-override": "^2.1.2",
    "morgan": "^1.2.2",
    "multer": "^0.1.3",
    "serve-favicon": "^2.0.1"
  }
}
```

#### app.js

Then, remove invalid code, load the required middleware, and make other
changes as necessary. The `app.js` file will look like this:

```
var http = require('http')
var express = require('express')
var routes = require('./routes')
var user = require('./routes/user')
var path = require('path')

var favicon = require('serve-favicon')
var logger = require('morgan')
var methodOverride = require('method-override')
var session = require('express-session')
var bodyParser = require('body-parser')
var multer = require('multer')
var errorHandler = require('errorhandler')

var app = express()

// all environments
app.set('port', process.env.PORT || 3000)
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')
app.use(favicon(path.join(__dirname, '/public/favicon.ico')))
app.use(logger('dev'))
app.use(methodOverride())
app.use(session({
  resave: true,
  saveUninitialized: true,
  secret: 'uwotm8'
}))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(multer())
app.use(express.static(path.join(__dirname, 'public')))

app.get('/', routes.index)
app.get('/users', user.list)

// error handling middleware should be loaded after the loading the routes
if (app.get('env') === 'development') {
  app.use(errorHandler())
}

var server = http.createServer(app)
server.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

Unless you need to work directly with the `http` module (socket.io/SPDY/HTTPS), loading it is not required, and the app can be simply started this way:

```
app.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

### Run the app

The migration process is complete, and the app is now an
Express 4 app. To confirm, start the app by using the following command:

```
$ node .
```

Load [http://localhost:3000](http://localhost:3000)
  and see the home page being rendered by Express 4.

## Upgrading to the Express 4 app generator

The command-line tool to generate an Express app is still
  `express`, but to upgrade to the new version, you must uninstall
  the Express 3 app generator and then install the new
  `express-generator`.

### Installing

If you already have the Express 3 app generator installed on your system,
you must uninstall it:

```
$ npm uninstall -g express
```

Depending on how your file and directory privileges are configured,
you might need to run this command with `sudo`.

Now install the new generator:

```
$ npm install -g express-generator
```

Depending on how your file and directory privileges are configured,
you might need to run this command with `sudo`.

Now the `express` command on your system is updated to the
Express 4 generator.

### Changes to the app generator

Command options and use largely remain the same, with the following exceptions:

- Removed the `--sessions` option.
- Removed the `--jshtml` option.
- Added the `--hogan` option to support [Hogan.js](http://twitter.github.io/hogan.js/).

### Example

Execute the following command to create an Express 4 app:

```
$ express app4
```

If you look at the contents of the `app4/app.js` file, you will notice
that all the middleware functions (except `express.static`) that are required for
the app are loaded as independent modules, and the `router` middleware
is no longer explicitly loaded in the app.

You will also notice that the `app.js` file is now a Node.js module, in contrast to the standalone app that was generated by the old generator.

After installing the dependencies, start the app by using the following command:

```
$ npm start
```

If you look at the `npm start` script in the `package.json` file,
you will notice that the actual command that starts the app is
`node ./bin/www`, which used to be `node app.js`
in Express 3.

Because the `app.js` file that was generated by the Express 4 generator
is now a Node.js module, it can no longer be started independently as an app
(unless you modify the code). The module must be loaded in a Node.js file
and started via the Node.js file. The Node.js file is `./bin/www`
in this case.

Neither the `bin` directory nor the extensionless `www`
file is mandatory for creating an Express app or starting the app. They are
just suggestions made by the generator, so feel free to modify them to suit your
needs.

To get rid of the `www` directory and keep things the “Express 3 way”,
delete the line that says `module.exports = app;` at the end of the
`app.js` file, then paste the following code in its place:

```
app.set('port', process.env.PORT || 3000)

var server = app.listen(app.get('port'), () => {
  debug('Express server listening on port ' + server.address().port)
})
```

Ensure that you load the `debug` module at the top of the `app.js` file by using the following code:

```
var debug = require('debug')('app4')
```

Next, change `"start": "node ./bin/www"` in the `package.json` file to `"start": "node app.js"`.

You have now moved the functionality of `./bin/www` back to
`app.js`. This change is not recommended, but the exercise helps you
to understand how the `./bin/www` file works, and why the `app.js` file
no longer starts on its own.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/guide/migrating-4.md          )

---

# Moving to Express 5

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# Moving to Express 5

## Overview

Express 5 is not very different from Express 4; although it maintains the same basic API, there are still changes that break compatibility with the previous version. Therefore, an application built with Express 4 might not work if you update it to use Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

You can then run your automated tests to see what fails, and fix problems according to the updates listed below. After addressing test failures, run your app to see what errors occur. You’ll find out right away if the app uses any methods or properties that are not supported.

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

**Removed methods and properties**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [Pluralized method names](#plural)
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

**Changed**

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

**Improvements**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## Removed methods and properties

If you use any of these methods or properties in your app, it will crash. So, you’ll need to change your app after you update to version 5.

### app.del()

Express 5 no longer supports the `app.del()` function. If you use this function, an error is thrown. For registering HTTP DELETE routes, use the `app.delete()` function instead.

Initially, `del` was used instead of `delete`, because `delete` is a reserved keyword in JavaScript. However, as of ECMAScript 6, `delete` and other reserved keywords can legally be used as property names.

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

`req.acceptsCharset()` is replaced by `req.acceptsCharsets()`.

`req.acceptsEncoding()` is replaced by `req.acceptsEncodings()`.

`req.acceptsLanguage()` is replaced by `req.acceptsLanguages()`.

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

### Leading colon (:) in the name for app.param(name, fn)

A leading colon character (:) in the name for the `app.param(name, fn)` function is a remnant of Express 3, and for the sake of backwards compatibility, Express 4 supported it with a deprecation notice. Express 5 will silently ignore it and use the name parameter without prefixing it with a colon.

This should not affect your code if you follow the Express 4 documentation of [app.param](https://expressjs.com/en/4x/api.html#app.param), as it makes no mention of the leading colon.

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

Express 5 no longer supports the signature `res.json(obj, status)`. Instead, set the status and then chain it to the `res.json()` method like this: `res.status(status).json(obj)`.

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

Express 5 no longer supports the signature `res.jsonp(obj, status)`. Instead, set the status and then chain it to the `res.jsonp()` method like this: `res.status(status).jsonp(obj)`.

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

The `res.sendfile()` function has been replaced by a camel-cased version `res.sendFile()` in Express 5.

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

## Changed

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

The `app.router` object, which was removed in Express 4, has made a comeback in Express 5. In the new version, this object is a just a reference to the base Express router, unlike in Express 3, where an app had to explicitly load it.

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

## Improvements

### res.render()

This method now enforces asynchronous behavior for all view engines, avoiding bugs caused by view engines that had a synchronous implementation and that violated the recommended interface.

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/guide/migrating-5.md          )

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/guide/overriding-express-api.md          )
