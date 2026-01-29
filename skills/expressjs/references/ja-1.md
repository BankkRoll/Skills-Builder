# 3.x API

# 3.x API

> Access the API reference for Express.js version 3.x, noting that this version is end-of-life and no longer maintained - includes details on modules and methods.

**Express 3.x は保守されなくなりました**

3.xの既知および未知のセキュリティ問題は、最終更新（2015年8月1日）以降は対処されていません。3.x系を使用することは安全であると見なされるべきではありません。 It is highly recommended to use the latest version of Express.

If you are unable to upgrade past 3.x, please consider [Commercial Support Options](https://expressjs.com/ja/support#commercial-support-options).

# 3.x API

## Application

### app.set(name, value)

Assigns setting `name` to `value`.

```
app.set('title', 'My Site')
app.get('title')
// => "My Site"
```

### app.get(name)

Get setting `name` value.

```
app.get('title')
// => undefined

app.set('title', 'My Site')
app.get('title')
// => "My Site"
```

### app.enable(name)

Set setting `name` to `true`.

```
app.enable('trust proxy')
app.get('trust proxy')
// => true
```

### app.disable(name)

Set setting `name` to `false`.

```
app.disable('trust proxy')
app.get('trust proxy')
// => false
```

### app.enabled(name)

Check if setting `name` is enabled.

```
app.enabled('trust proxy')
// => false

app.enable('trust proxy')
app.enabled('trust proxy')
// => true
```

### app.disabled(name)

Check if setting `name` is disabled.

```
app.disabled('trust proxy')
// => true

app.enable('trust proxy')
app.disabled('trust proxy')
// => false
```

### app.configure([env], callback)

Conditionally invoke `callback` when `env` matches `app.get('env')`,
aka `process.env.NODE_ENV`. This method remains for legacy reasons, and is effectively
an `if` statement as illustrated in the following snippets. These functions are *not*
required in order to use `app.set()` and other configuration methods.

```
// all environments
app.configure(function () {
  app.set('title', 'My Application')
})

// development only
app.configure('development', function () {
  app.set('db uri', 'localhost/dev')
})

// production only
app.configure('production', function () {
  app.set('db uri', 'n.n.n.n/prod')
})
```

Is effectively sugar for:

```
// all environments
app.set('title', 'My Application')

// development only
if (app.get('env') === 'development') {
  app.set('db uri', 'localhost/dev')
}

// production only
if (app.get('env') === 'production') {
  app.set('db uri', 'n.n.n.n/prod')
}
```

### app.use([path], function)

Use the given middleware `function`, with optional mount `path`,
defaulting to “/”.

```
var express = require('express')
var app = express()

// simple logger
app.use(function (req, res, next) {
  console.log('%s %s', req.method, req.url)
  next()
})

// respond
app.use(function (req, res, next) {
  res.send('Hello World')
})

app.listen(3000)
```

The “mount” path is stripped and is **not** visible
to the middleware `function`. The main effect of this feature is that
mounted middleware may operate without code changes regardless of its “prefix”
pathname.

A route will match any path that follows its path immediately with either a “`/`” or a “`.`”. For example: `app.use('/apple', ...)` will match */apple*, */apple/images*, */apple/images/news*, */apple.html*, */apple.html.txt*, and so on.

Here’s a concrete example, take the typical use-case of serving files in ./public
using the `express.static()` middleware:

```
// GET /javascripts/jquery.js
// GET /style.css
// GET /favicon.ico
app.use(express.static(path.join(__dirname, 'public')))
```

Say for example you wanted to prefix all static files with “/static”, you could
use the “mounting” feature to support this. Mounted middleware functions are *not*
invoked unless the `req.url` contains this prefix, at which point
it is stripped when the function is invoked. This affects this function only,
subsequent middleware will see `req.url` with “/static” included
unless they are mounted as well.

```
// GET /static/javascripts/jquery.js
// GET /static/style.css
// GET /static/favicon.ico
app.use('/static', express.static(path.join(__dirname, 'public')))
```

The order of which middleware are “defined” using `app.use()` is
very important, they are invoked sequentially, thus this defines middleware
precedence. For example usually `express.logger()` is the very
first middleware you would use, logging every request:

```
app.use(express.logger())
app.use(express.static(path.join(__dirname, 'public')))
app.use(function (req, res) {
  res.send('Hello')
})
```

Now suppose you wanted to ignore logging requests for static files, but to
continue logging routes and middleware defined after `logger()`,
you would simply move `static()` above:

```
app.use(express.static(path.join(__dirname, 'public')))
app.use(express.logger())
app.use(function (req, res) {
  res.send('Hello')
})
```

Another concrete example would be serving files from multiple directories,
giving precedence to “./public” over the others:

```
app.use(express.static(path.join(__dirname, 'public')))
app.use(express.static(path.join(__dirname, 'files')))
app.use(express.static(path.join(__dirname, 'uploads')))
```

### settings

The following settings are provided to alter how Express will behave:

- `env` Environment mode, defaults to process.env.NODE_ENV or “development”
- `trust proxy` Enables reverse proxy support, disabled by default
- `jsonp callback name` Changes the default callback name of ?callback=
- `json replacer` JSON replacer callback, null by default
- `json spaces` JSON response spaces for formatting, defaults to 2 in development, 0 in production
- `case sensitive routing` Enable case sensitivity, disabled by default, treating “/Foo” and “/foo” as the same
- `strict routing` Enable strict routing, by default “/foo” and “/foo/” are treated the same by the router
- `view cache` Enables view template compilation caching, enabled in production by default
- `view engine` The default engine extension to use when omitted
- `views` The view directory path, defaulting to “process.cwd() + ‘/views’”

### app.engine(ext, callback)

Register the given template engine `callback` as `ext`

By default will `require()` the engine based on the
file extension. For example if you try to render
a “foo.jade” file Express will invoke the following internally,
and cache the `require()` on subsequent calls to increase
performance.

```
app.engine('jade', require('jade').__express)
```

For engines that do not provide `.__express` out of the box -
or if you wish to “map” a different extension to the template engine
you may use this method. For example mapping the EJS template engine to
“.html” files:

```
app.engine('html', require('ejs').renderFile)
```

In this case EJS provides a `.renderFile()` method with
the same signature that Express expects: `(path, options, callback)`,
though note that it aliases this method as `ejs.__express` internally
so if you’re using “.ejs” extensions you dont need to do anything.

Some template engines do not follow this convention, the
[consolidate.js](https://github.com/visionmedia/consolidate.js)
library was created to map all of node’s popular template
engines to follow this convention, thus allowing them to
work seemlessly within Express.

```
var engines = require('consolidate')
app.engine('haml', engines.haml)
app.engine('html', engines.hogan)
```

### app.param([name], callback)

Map logic to route parameters. For example when `:user`
is present in a route path you may map user loading logic to automatically
provide `req.user` to the route, or perform validations
on the parameter input.

The following snippet illustrates how the `callback`
is much like middleware, thus supporting async operations, however
providing the additional value of the parameter, here named as `id`.
An attempt to load the user is then performed, assigning `req.user`,
otherwise passing an error to `next(err)`.

```
app.param('user', function (req, res, next, id) {
  User.find(id, function (err, user) {
    if (err) {
      next(err)
    } else if (user) {
      req.user = user
      next()
    } else {
      next(new Error('failed to load user'))
    }
  })
})
```

Alternatively you may pass only a `callback`, in which
case you have the opportunity to alter the `app.param()` API.
For example the [express-params](http://github.com/expressjs/express-params)
defines the following callback which allows you to restrict parameters to a given
regular expression.

This example is a bit more advanced, checking if the second argument is a regular
expression, returning the callback which acts much like the “user” param example.

```
app.param(function (name, fn) {
  if (fn instanceof RegExp) {
    return function (req, res, next, val) {
      var captures
      if ((captures = fn.exec(String(val)))) {
        req.params[name] = captures
        next()
      } else {
        next('route')
      }
    }
  }
})
```

The method could now be used to effectively validate parameters, or also
parse them to provide capture groups:

```
app.param('id', /^\d+$/)

app.get('/user/:id', function (req, res) {
  res.send('user ' + req.params.id)
})

app.param('range', /^(\w+)\.\.(\w+)?$/)

app.get('/range/:range', function (req, res) {
  var range = req.params.range
  res.send('from ' + range[1] + ' to ' + range[2])
})
```

### app.VERB(path, [callback...], callback)

The `app.VERB()` methods provide the routing functionality
in Express, where **VERB** is one of the HTTP verbs, such
as `app.post()`. Multiple callbacks may be given, all are treated
equally, and behave just like middleware, with the one exception that
these callbacks may invoke `next('route')` to bypass the
remaining route callback(s). This mechanism can be used to perform pre-conditions
on a route then pass control to subsequent routes when there is no reason to proceed
with the route matched.

The following snippet illustrates the most simple route definition possible. Express
translates the path strings to regular expressions, used internally to match incoming requests.
Query strings are *not* considered when peforming these matches, for example “GET /”
would match the following route, as would “GET /?name=tobi”.

```
app.get('/', function (req, res) {
  res.send('hello world')
})
```

Regular expressions may also be used, and can be useful
if you have very specific restraints, for example the following
would match “GET /commits/71dbb9c” as well as “GET /commits/71dbb9c..4c084f9”.

```
app.get(/^\/commits\/(\w+)(?:\.\.(\w+))?$/, function (req, res) {
  var from = req.params[0]
  var to = req.params[1] || 'HEAD'
  res.send('commit range ' + from + '..' + to)
})
```

Several callbacks may also be passed, useful for re-using middleware
that load resources, perform validations, etc.

```
app.get('/user/:id', user.load, function () {
  // ...
})
```

These callbacks may be passed within arrays as well, these arrays are
simply flattened when passed:

```
var middleware = [loadForum, loadThread]

app.get('/forum/:fid/thread/:tid', middleware, function () {
  // ...
})

app.post('/forum/:fid/thread/:tid', middleware, function () {
  // ...
})
```

### app.all(path, [callback...], callback)

This method functions just like the `app.VERB()` methods,
however it matches all HTTP verbs.

This method is extremely useful for
mapping “global” logic for specific path prefixes or arbitrary matches.
For example if you placed the following route at the top of all other
route definitions, it would require that all routes from that point on
would require authentication, and automatically load a user. Keep in mind
that these callbacks do not have to act as end points, `loadUser`
can perform a task, then `next()` to continue matching subsequent
routes.

```
app.all('*', requireAuthentication, loadUser)
```

Or the equivalent:

```
app.all('*', requireAuthentication)
app.all('*', loadUser)
```

Another great example of this is white-listed “global” functionality. Here
the example is much like before, however only restricting paths prefixed with
“/api”:

```
app.all('/api/*', requireAuthentication)
```

### app.locals

Application local variables are provided to all templates
rendered within the application. This is useful for providing
helper functions to templates, as well as app-level data.

```
app.locals.title = 'My App'
app.locals.strftime = require('strftime')
```

The `app.locals` object is a JavaScript `Function`,
which when invoked with an object will merge properties into itself, providing
a simple way to expose existing objects as local variables.

```
app.locals({
  title: 'My App',
  phone: '1-250-858-9990',
  email: '[email protected]'
})

console.log(app.locals.title)
// => 'My App'

console.log(app.locals.email)
// => '[email protected]'
```

A consequence of the `app.locals` Object being ultimately a Javascript Function Object is that you must not reuse existing (native) named properties for your own variable names, such as `name, apply, bind, call, arguments, length, constructor`.

```
app.locals({ name: 'My App' })

console.log(app.locals.name)
// => return 'app.locals' in place of 'My App' (app.locals is a Function !)
// => if name's variable is used in a template, a ReferenceError will be returned.
```

The full list of native named properties can be found in many specifications. The [JavaScript specification](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference) introduced original properties, some of which still recognized by modern engines, and the [EcmaScript specification](http://www.ecma-international.org/ecma-262/5.1/) then built on it and normalized the set of properties, adding new ones and removing deprecated ones. Check out properties for Functions and Objects if interested.

By default Express exposes only a single app-level local variable, `settings`.

```
app.set('title', 'My App')
// use settings.title in a view
```

### app.render(view, [options], callback)

Render a `view` with a callback responding with
the rendered string. This is the app-level variant of `res.render()`,
and otherwise behaves the same way.

```
app.render('email', function (err, html) {
  // ...
})

app.render('email', { name: 'Tobi' }, function (err, html) {
  // ...
})
```

### app.routes

The `app.routes` object houses all of the routes defined mapped
by the associated HTTP verb. This object may be used for introspection capabilities,
for example Express uses this internally not only for routing but to provide default

 OPTIONS

behaviour unless `app.options()` is used. Your application
or framework may also remove routes by simply by removing them from this object.

The output of `console.log(app.routes)`:

```
{ get:
   [ { path: '/',
       method: 'get',
       callbacks: [Object],
       keys: [],
       regexp: /^\/\/?$/i },
     { path: '/user/:id',
       method: 'get',
       callbacks: [Object],
       keys: [{ name: 'id', optional: false }],
       regexp: /^\/user\/(?:([^\/]+?))\/?$/i } ],
  delete:
   [ { path: '/user/:id',
       method: 'delete',
       callbacks: [Object],
       keys: [Object],
       regexp: /^\/user\/(?:([^\/]+?))\/?$/i } ] }
```

### app.listen()

Bind and listen for connections on the given host and port,
this method is identical to node’s [http.Server#listen()](http://nodejs.org/api/http.html#http_server_listen_port_hostname_backlog_callback).

```
var express = require('express')
var app = express()
app.listen(3000)
```

The `app` returned by `express()` is in fact a JavaScript
`Function`, designed to be passed to node’s http servers as a callback
to handle requests. This allows you to provide both HTTP and HTTPS versions of
your app with the same codebase easily, as the app does not inherit from these,
it is simply a callback:

```
var express = require('express')
var https = require('https')
var http = require('http')
var app = express()

http.createServer(app).listen(80)
https.createServer(options, app).listen(443)
```

The `app.listen()` method is simply a convenience method defined as,
if you wish to use HTTPS or provide both, use the technique above.

```
app.listen = function () {
  var server = http.createServer(this)
  return server.listen.apply(server, arguments)
}
```

    [Edit this page](https://github.com/expressjs/expressjs.com/tree/gh-pages/_includes/api/en/3x          )
