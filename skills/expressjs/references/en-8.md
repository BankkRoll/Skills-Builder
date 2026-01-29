# Routing and more

# Routing

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# Routing

*Routing* refers to how an application’s endpoints (URIs) respond to client requests.
For an introduction to routing, see [Basic routing](https://expressjs.com/en/starter/basic-routing.html).

You define routing using methods of the Express `app` object that correspond to HTTP methods;
for example, `app.get()` to handle GET requests and `app.post` to handle POST requests. For a full list,
see [app.METHOD](https://expressjs.com/en/5x/api.html#app.METHOD). You can also use [app.all()](https://expressjs.com/en/5x/api.html#app.all) to handle all HTTP methods and [app.use()](https://expressjs.com/en/5x/api.html#app.use) to
specify middleware as the callback function (See [Using middleware](https://expressjs.com/en/guide/using-middleware.html) for details).

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

The following code is an example of routes that are defined for the `GET` and the `POST` methods to the root of the app.

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
For a full list, see [app.METHOD](https://expressjs.com/en/5x/api.html#app.METHOD).

There is a special routing method, `app.all()`, used to load middleware functions at a path for *all* HTTP request methods. For example, the following handler is executed for requests to the route `"/secret"` whether using `GET`, `POST`, `PUT`, `DELETE`, or any other HTTP request method supported in the [http module](https://nodejs.org/api/http.html#http_http_methods).

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## Route paths

Route paths, in combination with a request method, define the endpoints at which requests can be made. Route paths can be strings, string patterns, or regular expressions.

Caution

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/en/guide/migrating-5.html#path-syntax) for more information.

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

This route path will match requests to `/random.text`.

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### Route paths based on string patterns

Caution

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/en/guide/migrating-5.html#path-syntax) for more information.

This route path will match `acd` and `abcd`.

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

This route path will match `abcd`, `abbcd`, `abbbcd`, and so on.

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

This route path will match `abcd`, `abxcd`, `abRANDOMcd`, `ab123cd`, and so on.

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

This route path will match `/abe` and `/abcde`.

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### Route paths based on regular expressions

This route path will match anything with an “a” in it.

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

This route path will match `butterfly` and `dragonfly`, but not `butterflyman`, `dragonflyman`, and so on.

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

Caution

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/en/guide/migrating-5.html#path-syntax).

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

You can provide multiple callback functions that behave like [middleware](https://expressjs.com/en/guide/using-middleware.html) to handle a request. The only exception is that these callbacks might invoke `next('route')` to bypass the remaining route callbacks. You can use this mechanism to impose pre-conditions on a route, then pass control to subsequent routes if there’s no reason to proceed with the current route.

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

## Response methods

The methods on the response object (`res`) in the following table can send a response to the client, and terminate the request-response cycle. If none of these methods are called from a route handler, the client request will be left hanging.

| Method | Description |
| --- | --- |
| res.download() | Prompt a file to be downloaded. |
| res.end() | End the response process. |
| res.json() | Send a JSON response. |
| res.jsonp() | Send a JSON response with JSONP support. |
| res.redirect() | Redirect a request. |
| res.render() | Render a view template. |
| res.send() | Send a response of various types. |
| res.sendFile() | Send a file as an octet stream. |
| res.sendStatus() | Set the response status code and send its string representation as the response body. |

## app.route()

You can create chainable route handlers for a route path by using `app.route()`.
Because the path is specified at a single location, creating modular routes is helpful, as is reducing redundancy and typos. For more information about routes, see: [Router() documentation](https://expressjs.com/en/5x/api.html#router).

Here is an example of chained route handlers that are defined by using `app.route()`.

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

Create a router file named `birds.js` in the app directory, with the following content:

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

Then, load the router module in the app:

```
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

The app will now be able to handle requests to `/birds` and `/birds/about`, as well as call the `timeLog` middleware function that is specific to the route.

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/en/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/guide/routing.md          )

---

# Using middleware

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# Using middleware

Express is a routing and middleware web framework that has minimal functionality of its own: An Express application is essentially a series of middleware function calls.

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/en/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/en/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. The next middleware function is commonly denoted by a variable named `next`.

Middleware functions can perform the following tasks:

- Execute any code.
- Make changes to the request and the response objects.
- End the request-response cycle.
- Call the next middleware function in the stack.

If the current middleware function does not end the request-response cycle, it must call `next()` to pass control to the next middleware function. Otherwise, the request will be left hanging.

An Express application can use the following types of middleware:

- [Application-level middleware](#middleware.application)
- [Router-level middleware](#middleware.router)
- [Error-handling middleware](#middleware.error-handling)
- [Built-in middleware](#middleware.built-in)
- [Third-party middleware](#middleware.third-party)

You can load application-level and router-level middleware with an optional mount path.
You can also load a series of middleware functions together, which creates a sub-stack of the middleware system at a mount point.

## Application-level middleware

Bind application-level middleware to an instance of the [app object](https://expressjs.com/en/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

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

This example shows a middleware sub-stack that handles GET requests to the `/user/:id` path.

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

This example shows a middleware sub-stack that handles GET requests to the `/user/:id` path.

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

This example shows an array with a middleware sub-stack that handles GET requests to the `/user/:id` path

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

## Router-level middleware

Router-level middleware works in the same way as application-level middleware, except it is bound to an instance of `express.Router()`.

```
const router = express.Router()
```

Load router-level middleware by using the `router.use()` and `router.METHOD()` functions.

The following example code replicates the middleware system that is shown above for application-level middleware, by using router-level middleware:

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

This example shows a middleware sub-stack that handles GET requests to the `/user/:id` path.

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

For details about error-handling middleware, see: [Error handling](https://expressjs.com/en/guide/error-handling.html).

## Built-in middleware

Starting with version 4.x, Express no longer depends on [Connect](https://github.com/senchalabs/connect). The middleware
functions that were previously included with Express are now in separate modules; see [the list of middleware functions](https://github.com/senchalabs/connect#middleware).

Express has the following built-in middleware functions:

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## Third-party middleware

Use third-party middleware to add functionality to Express apps.

Install the Node.js module for the required functionality, then load it in your app at the application level or at the router level.

The following example illustrates installing and loading the cookie-parsing middleware function `cookie-parser`.

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

For a partial list of third-party middleware functions that are commonly used with Express, see: [Third-party middleware](https://expressjs.com/en/resources/middleware.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/guide/using-middleware.md          )

---

# Using template engines with Express

> Discover how to integrate and use template engines like Pug, Handlebars, and EJS with Express.js to render dynamic HTML pages efficiently.

# Using template engines with Express

A *template engine* enables you to use static template files in your application. At runtime, the template engine replaces
variables in a template file with actual values, and transforms the template into an HTML file sent to the client.
This approach makes it easier to design an HTML page.

The [Express application generator](https://expressjs.com/en/starter/generator.html) uses [Pug](https://pugjs.org/api/getting-started.html) as its default, but it also supports [Handlebars](https://www.npmjs.com/package/handlebars), and [EJS](https://www.npmjs.com/package/ejs), among others.

To render template files, set the following [application setting properties](https://expressjs.com/en/4x/api.html#app.set), in the default `app.js` created by the generator:

- `views`, the directory where the template files are located. Eg: `app.set('views', './views')`.
  This defaults to the `views` directory in the application root directory.
- `view engine`, the template engine to use. For example, to use the Pug template engine: `app.set('view engine', 'pug')`.

Then install the corresponding template engine npm package; for example to install Pug:

```
$ npm install pug --save
```

Express-compliant template engines such as Pug export a function named `__express(filePath, options, callback)`,
which `res.render()` calls to render the template code.

Some template engines do not follow this convention. The [@ladjs/consolidate](https://www.npmjs.com/package/@ladjs/consolidate)
library follows this convention by mapping all of the popular Node.js template engines, and therefore works seamlessly within Express.

After the view engine is set, you don’t have to specify the engine or load the template engine module in your app;
Express loads the module internally, for example:

```
app.set('view engine', 'pug')
```

Then, create a Pug template file named `index.pug` in the `views` directory, with the following content:

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

When you make a request to the home page, the `index.pug` file will be rendered as HTML.

The view engine cache does not cache the contents of the template’s output, only the underlying template itself. The view is still re-rendered with every request even when the cache is on.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/guide/using-template-engines.md          )

---

# Writing middleware for use in Express apps

> Learn how to write custom middleware functions for Express.js applications, including examples and best practices for enhancing request and response handling.

# Writing middleware for use in Express apps

## Overview

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/en/5x/api.html#req) (`req`), the [response object](https://expressjs.com/en/5x/api.html#res) (`res`), and the `next` function in the application’s request-response cycle. The `next` function is a function in the Express router which, when invoked, executes the middleware succeeding the current middleware.

Middleware functions can perform the following tasks:

- Execute any code.
- Make changes to the request and the response objects.
- End the request-response cycle.
- Call the next middleware in the stack.

If the current middleware function does not end the request-response cycle, it must call `next()` to pass control to the next middleware function. Otherwise, the request will be left hanging.

The following figure shows the elements of a middleware function call:

|  | HTTP method for which the middleware function applies.Path (route) for which the middleware function applies.The middleware function.Callback argument to the middleware function, called "next" by convention.HTTPresponseargument to the middleware function, called "res" by convention.HTTPrequestargument to the middleware function, called "req" by convention. |
| --- | --- |

Starting with Express 5, middleware functions that return a Promise will call `next(value)` when they reject or throw an error. `next` will be called with either the rejected value or the thrown Error.

## Example

Here is an example of a simple “Hello World” Express application.
The remainder of this article will define and add three middleware functions to the application:
one called `myLogger` that prints a simple log message, one called `requestTime` that
displays the timestamp of the HTTP request, and one called `validateCookies` that validates incoming cookies.

```
const express = require('express')
const app = express()

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(3000)
```

### Middleware function myLogger

Here is a simple example of a middleware function called “myLogger”. This function just prints “LOGGED” when a request to the app passes through it. The middleware function is assigned to a variable named `myLogger`.

```
const myLogger = function (req, res, next) {
  console.log('LOGGED')
  next()
}
```

Notice the call above to `next()`. Calling this function invokes the next middleware function in the app.
The `next()` function is not a part of the Node.js or Express API, but is the third argument that is passed to the middleware function. The `next()` function could be named anything, but by convention it is always named “next”.
To avoid confusion, always use this convention.

To load the middleware function, call `app.use()`, specifying the middleware function.
For example, the following code loads the `myLogger` middleware function before the route to the root path (/).

```
const express = require('express')
const app = express()

const myLogger = function (req, res, next) {
  console.log('LOGGED')
  next()
}

app.use(myLogger)

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(3000)
```

Every time the app receives a request, it prints the message “LOGGED” to the terminal.

The order of middleware loading is important: middleware functions that are loaded first are also executed first.

If `myLogger` is loaded after the route to the root path, the request never reaches it and the app doesn’t print “LOGGED”, because the route handler of the root path terminates the request-response cycle.

The middleware function `myLogger` simply prints a message, then passes on the request to the next middleware function in the stack by calling the `next()` function.

### Middleware function requestTime

Next, we’ll create a middleware function called “requestTime” and add a property called `requestTime`
to the request object.

```
const requestTime = function (req, res, next) {
  req.requestTime = Date.now()
  next()
}
```

The app now uses the `requestTime` middleware function. Also, the callback function of the root path route uses the property that the middleware function adds to `req` (the request object).

```
const express = require('express')
const app = express()

const requestTime = function (req, res, next) {
  req.requestTime = Date.now()
  next()
}

app.use(requestTime)

app.get('/', (req, res) => {
  let responseText = 'Hello World!<br>'
  responseText += `<small>Requested at: ${req.requestTime}</small>`
  res.send(responseText)
})

app.listen(3000)
```

When you make a request to the root of the app, the app now displays the timestamp of your request in the browser.

### Middleware function validateCookies

Finally, we’ll create a middleware function that validates incoming cookies and sends a 400 response if cookies are invalid.

Here’s an example function that validates cookies with an external async service.

```
async function cookieValidator (cookies) {
  try {
    await externallyValidateCookie(cookies.testCookie)
  } catch {
    throw new Error('Invalid cookies')
  }
}
```

Here, we use the [cookie-parser](https://expressjs.com/resources/middleware/cookie-parser.html) middleware to parse incoming cookies off the `req` object and pass them to our `cookieValidator` function. The `validateCookies` middleware returns a Promise that upon rejection will automatically trigger our error handler.

```
const express = require('express')
const cookieParser = require('cookie-parser')
const cookieValidator = require('./cookieValidator')

const app = express()

async function validateCookies (req, res, next) {
  await cookieValidator(req.cookies)
  next()
}

app.use(cookieParser())

app.use(validateCookies)

// error handler
app.use((err, req, res, next) => {
  res.status(400).send(err.message)
})

app.listen(3000)
```

Note how `next()` is called after `await cookieValidator(req.cookies)`. This ensures that if `cookieValidator` resolves, the next middleware in the stack will get called. If you pass anything to the `next()` function (except the string `'route'` or `'router'`), Express regards the current request as being an error and will skip any remaining non-error handling routing and middleware functions.

Because you have access to the request object, the response object, the next middleware function in the stack, and the whole Node.js API, the possibilities with middleware functions are endless.

For more information about Express middleware, see: [Using Express middleware](https://expressjs.com/en/guide/using-middleware.html).

## Configurable middleware

If you need your middleware to be configurable, export a function which accepts an options object or other parameters, which, then returns the middleware implementation based on the input parameters.

File: `my-middleware.js`

```
module.exports = function (options) {
  return function (req, res, next) {
    // Implement the middleware function based on the options object
    next()
  }
}
```

The middleware can now be used as shown below.

```
const mw = require('./my-middleware.js')

app.use(mw({ option1: '1', option2: '2' }))
```

Refer to [cookie-session](https://github.com/expressjs/cookie-session) and [compression](https://github.com/expressjs/compression) for examples of configurable middleware.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/guide/writing-middleware.md          )

---

# Community

> Connect with the Express.js community, learn about the technical committee, find resources, explore community-contributed modules, and get involved in discussions.

# Community

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

Our vibrant community has created a large variety of extensions,
[middleware modules](https://expressjs.com/en/resources/middleware.html) and higher-level frameworks.

Additionally, the Express community maintains modules in these two GitHub orgs:

- [jshttp](https://github.com/jshttp) modules providing useful utility functions; see [Utility modules](https://expressjs.com/en/resources/utils.html).
- [pillarjs](https://github.com/pillarjs): low-level modules that Express uses internally.

To keep up with what is going on in the whole community, check out the [ExpressJS StatusBoard](https://expressjs.github.io/statusboard/).

## Issues

If you’ve come across what you think is a bug, or just want to make
a feature request open a ticket in the [issue queue](https://github.com/expressjs/express/issues).

## Examples

View dozens of Express application [examples](https://github.com/expressjs/express/tree/master/examples)
in the repository covering everything from API design and authentication to template engine integration.

## Github Discussions

The [GitHub Discussions](https://github.com/expressjs/discussions) section is an excellent space to engage in conversations about the development and maintenance of Express, as well as to share ideas and discuss topics related to its usage.

# Branding of Express.js

## Express.js Logo

Express is a project of the OpenJS Foundation. Please review the [trademark policy](https://trademark-policy.openjsf.org/) for information about permissible use of Express.js logos and marks.

### Logotype

### Logomark

        [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/resources/community.md          )
