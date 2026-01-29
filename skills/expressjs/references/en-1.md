# 3.x API

# 3.x API

> Access the API reference for Express.js version 3.x, noting that this version is end-of-life and no longer maintained - includes details on modules and methods.

**Express 3.x IS END-OF-LIFE AND NO LONGER MAINTAINED**

Known and unknown security and performance issues in 3.x have not been addressed since the last update (1 August, 2015). It is highly recommended to use the latest version of Express.

If you are unable to upgrade past 3.x, please consider [Commercial Support Options](https://expressjs.com/en/support#commercial-support-options).

# 3.x API

## express()

Creates an Express application. The `express()` function is a top-level function exported by the *express* module.

```
var express = require('express')
var app = express()

app.get('/', function (req, res) {
  res.send('hello world')
})

app.listen(3000)
```

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

## Request

The `req` object is an enhanced version of Node’s own request object
and supports all [built-in fields and methods](https://nodejs.org/api/http.html#http_class_http_incomingmessage).

### req.params

This property is an array containing properties mapped to the named route “parameters”.
For example if you have the route `/user/:name`, then the “name” property
is available to you as `req.params.name`. This object defaults to `{}`.

```
// GET /user/tj
console.dir(req.params.name)
// => 'tj'
```

When a regular expression is used for the route definition, capture groups
are provided in the array using `req.params[N]`, where `N`
is the nth capture group. This rule is applied to unnamed wild-card matches
with string routes such as `/file/*`:

```
// GET /file/javascripts/jquery.js
console.dir(req.params[0])
// => 'javascripts/jquery.js'
```

### req.query

This property is an object containing the parsed query-string,
defaulting to `{}`.

```
// GET /search?q=tobi+ferret
console.dir(req.query.q)
// => 'tobi ferret'

// GET /shoes?order=desc&shoe[color]=blue&shoe[type]=converse
console.dir(req.query.order)
// => 'desc'

console.dir(req.query.shoe.color)
// => 'blue'

console.dir(req.query.shoe.type)
// => 'converse'
```

### req.body

This property is an object containing the parsed request body. This feature
is provided by the `bodyParser()` middleware, though other body
parsing middleware may follow this convention as well. This property
defaults to `{}` when `bodyParser()` is used.

```
// POST user[name]=tobi&user[email][email protected]
console.log(req.body.user.name)
// => "tobi"

console.log(req.body.user.email)
// => "[email protected]"

// POST { "name": "tobi" }
console.log(req.body.name)
// => "tobi"
```

### req.files

This property is an object of the files uploaded. This feature
is provided by the `bodyParser()` middleware, though other body
parsing middleware may follow this convention as well. This property
defaults to `{}` when `bodyParser()` is used.

For example if a **file** field was named “image”,
and a file was uploaded, `req.files.image` would contain
the following `File` object:

```
{ size: 74643,
  path: '/tmp/8ef9c52abe857867fd0a4e9a819d1876',
  name: 'edge.png',
  type: 'image/png',
  hash: false,
  lastModifiedDate: Thu Aug 09 2012 20:07:51 GMT-0700 (PDT),
  _writeStream:
   { path: '/tmp/8ef9c52abe857867fd0a4e9a819d1876',
     fd: 13,
     writable: false,
     flags: 'w',
     encoding: 'binary',
     mode: 438,
     bytesWritten: 74643,
     busy: false,
     _queue: [],
     _open: [Function],
     drainable: true },
  length: [Getter],
  filename: [Getter],
  mime: [Getter] }
```

The `bodyParser()` middleware utilizes the
[node-formidable](https://github.com/felixge/node-formidable)
module internally, and accepts the same options. An example of this
is the `keepExtensions` formidable option, defaulting to **false**
which in this case gives you the filename “/tmp/8ef9c52abe857867fd0a4e9a819d1876” void of
the “.png” extension. To enable this, and others you may pass them to `bodyParser()`:

```
app.use(express.bodyParser({ keepExtensions: true, uploadDir: '/my/files' }))
```

### req.param(name)

Return the value of param `name` when present.

```
// ?name=tobi
req.param('name')
// => "tobi"

// POST name=tobi
req.param('name')
// => "tobi"

// /user/tobi for /user/:name
req.param('name')
// => "tobi"
```

Lookup is performed in the following order:

- `req.params`
- `req.body`
- `req.query`

Direct access to `req.body`, `req.params`,
and `req.query` should be favoured for clarity - unless
you truly accept input from each object.

### req.route

The currently matched `Route` containing
several properties such as the route’s original path
string, the regexp generated, and so on.

```
app.get('/user/:id?', function (req, res) {
  console.dir(req.route)
})
```

Example output from the previous snippet:

```
{ path: '/user/:id?',
  method: 'get',
  callbacks: [ [Function] ],
  keys: [ { name: 'id', optional: true } ],
  regexp: /^\/user(?:\/([^\/]+?))?\/?$/i,
  params: [ id: '12' ] }
```

### req.cookies

This object requires the `cookieParser()` middleware for use.
It contains cookies sent by the user-agent. If no cookies are sent, it
defaults to `{}`.

```
// Cookie: name=tj
console.log(req.cookies.name)
// => "tj"
```

### req.signedCookies

This object requires the `cookieParser(secret)` middleware for use.
It contains signed cookies sent by the user-agent, unsigned and ready for use.
Signed cookies reside in a different object to show developer intent; otherwise,
a malicious attack could be placed on `req.cookie` values (which are easy to spoof).
Note that signing a cookie does not make it “hidden” or encrypted; this simply
prevents tampering (because the secret used to sign is private). If no signed
cookies are sent, it defaults to `{}`.

```
// Cookie: user=tobi.CP7AWaXDfAKIRfH49dQzKJx7sKzzSoPq7/AcBBRVwlI3
console.dir(req.signedCookies.user)
// => 'tobi'
```

### req.get(field)

Get the case-insensitive request header `field`. The “Referrer” and “Referer” fields are interchangeable.

```
req.get('Content-Type')
// => "text/plain"

req.get('content-type')
// => "text/plain"

req.get('Something')
// => undefined
```

p Aliased as `req.header(field)`.

### req.accepts(types)

Check if the given `types` are acceptable, returning
the best match when true, otherwise `undefined` - in which
case you should respond with 406 “Not Acceptable”.

The `type` value may be a single mime type string
such as “application/json”, the extension name
such as “json”, a comma-delimited list or an array. When a list
or array is given the best match, if any is returned.

```
// Accept: text/html
req.accepts('html')
// => "html"

// Accept: text/*, application/json
req.accepts('html')
// => "html"
req.accepts('text/html')
// => "text/html"
req.accepts('json, text')
// => "json"
req.accepts('application/json')
// => "application/json"

// Accept: text/*, application/json
req.accepts('image/png')
req.accepts('png')
// => undefined

// Accept: text/*;q=.5, application/json
req.accepts(['html', 'json'])
req.accepts('html, json')
// => "json"
```

### req.accepted

Return an array of Accepted media types ordered from highest quality to lowest.

```
[ { value: 'application/json',
    quality: 1,
    type: 'application',
    subtype: 'json' },
   { value: 'text/html',
     quality: 0.5,
     type: 'text',
     subtype: 'html' } ]
```

### req.is(type)

Check if the incoming request contains the “Content-Type”
header field, and it matches the give mime `type`.

```
// With Content-Type: text/html; charset=utf-8
req.is('html')
req.is('text/html')
req.is('text/*')
// => true

// When Content-Type is application/json
req.is('json')
req.is('application/json')
req.is('application/*')
// => true

req.is('html')
// => false
```

### req.ip

Return the remote address, or when “trust proxy”
is enabled - the upstream address.

```
console.dir(req.ip)
// => '127.0.0.1'
```

### req.ips

When “trust proxy” is `true`, parse
the “X-Forwarded-For” ip address list
and return an array, otherwise an empty
array is returned.

For example if the value were “client, proxy1, proxy2”
you would receive the array `["client", "proxy1", "proxy2"]`
where “proxy2” is the furthest down-stream.

### req.path

Returns the request URL pathname.

```
// example.com/users?sort=desc
console.dir(req.path)
// => '/users'
```

### req.host

Returns the hostname from the “Host” header field (void of portno).

```
// Host: "example.com:3000"
console.dir(req.host)
// => 'example.com'
```

### req.fresh

Check if the request is fresh - aka Last-Modified and/or the ETag still match,
indicating that the resource is “fresh”.

```
console.dir(req.fresh)
// => true
```

### req.stale

Check if the request is stale - aka Last-Modified and/or the ETag do not match,
indicating that the resource is “stale”.

```
console.dir(req.stale)
// => true
```

### req.xhr

Check if the request was issued with the “X-Requested-With”
header field set to “XMLHttpRequest” (jQuery etc).

```
console.dir(req.xhr)
// => true
```

### req.protocol

Return the protocol string “http” or “https”
when requested with TLS. When the “trust proxy”
setting is enabled the “X-Forwarded-Proto” header
field will be trusted. If you’re running behind
a reverse proxy that supplies https for you this
may be enabled.

```
console.dir(req.protocol)
// => 'http'
```

### req.secure

Check if a TLS connection is established. This is a short-hand for:

```
console.dir(req.protocol === 'https')
// => true
```

### req.subdomains

Return subdomains as an array.

```
// Host: "tobi.ferrets.example.com"
console.dir(req.subdomains)
// => ['ferrets', 'tobi']
```

### req.originalUrl

This property is much like `req.url`, however it retains
the original request url, allowing you to rewrite `req.url`
freely for internal routing purposes. For example the “mounting” feature
of [app.use()](#app.use) will rewrite `req.url` to
strip the mount point.

```
// GET /search?q=something
console.log(req.originalUrl)
// => "/search?q=something"
```

### req.acceptedLanguages

Return an array of Accepted languages ordered from highest quality to lowest.

```
Accept-Language: en;q=.5, en-us
// => ['en-us', 'en']
```

### req.acceptedCharsets

Return an array of Accepted charsets ordered from highest quality to lowest.

```
Accept-Charset: iso-8859-5;q=.2, unicode-1-1;q=0.8
// => ['unicode-1-1', 'iso-8859-5']
```

### req.acceptsCharset(charset)

Check if the given `charset` are acceptable.

### req.acceptsLanguage(lang)

Check if the given `lang` are acceptable.

### req.res

This property holds a reference to the [response object](#response)
that relates to this request object.

## Response

The `res` object is an enhanced version of Node’s own response object
and supports all [built-in fields and methods](https://nodejs.org/api/http.html#http_class_http_serverresponse).

### res.status(code)

Chainable alias of node’s `res.statusCode=`.

```
res.status(404).sendfile('path/to/404.png')
```

### res.set(field, [value])

Set header `field` to `value`, or pass an object to set multiple fields at once.

```
res.set('Content-Type', 'text/plain')

res.set({
  'Content-Type': 'text/plain',
  'Content-Length': '123',
  ETag: '12345'
})
```

Aliased as `res.header(field, [value])`.

### res.get(field)

Get the case-insensitive response header `field`.

```
res.get('Content-Type')
// => "text/plain"
```

### res.cookie(name, value, [options])

Set cookie `name` to `value`, which may be a string or object converted to JSON. The `path`
option defaults to “/”.

```
res.cookie('name', 'tobi', { domain: '.example.com', path: '/admin', secure: true })
res.cookie('rememberme', '1', { expires: new Date(Date.now() + 900000), httpOnly: true })
```

The `maxAge` option is a convenience option for setting “expires”
relative to the current time in milliseconds. The following is equivalent to
the previous example.

```
res.cookie('rememberme', '1', { maxAge: 900000, httpOnly: true })
```

An object may be passed which is then serialized as JSON, which is
automatically parsed by the `bodyParser()` middleware.

```
res.cookie('cart', { items: [1, 2, 3] })
res.cookie('cart', { items: [1, 2, 3] }, { maxAge: 900000 })
```

Signed cookies are also supported through this method. Simply
pass the `signed` option. When given `res.cookie()`
will use the secret passed to `express.cookieParser(secret)`
to sign the value.

```
res.cookie('name', 'tobi', { signed: true })
```

Later you may access this value through the [req.signedCookie](#req.signedCookies)
object.

### res.clearCookie(name, [options])

Clear cookie `name`. The `path` option defaults to “/”.

```
res.cookie('name', 'tobi', { path: '/admin' })
res.clearCookie('name', { path: '/admin' })
```

### res.redirect([status], url)

Redirect to the given `url` with optional `status` code
defaulting to 302 “Found”.

```
res.redirect('/foo/bar')
res.redirect('http://example.com')
res.redirect(301, 'http://example.com')
res.redirect('../login')
```

Express supports a few forms of redirection, first being
a fully qualified URI for redirecting to a different site:

```
res.redirect('http://google.com')
```

The second form is the pathname-relative redirect, for example
if you were on `http://example.com/admin/post/new`, the
following redirect to `/admin` would land you at `http://example.com/admin`:

```
res.redirect('/admin')
```

This next redirect is relative to the `mount` point of the application. For example
if you have a blog application mounted at `/blog`, ideally it has no knowledge of
where it was mounted, so where a redirect of `/admin/post/new` would simply give you
`http://example.com/admin/post/new`, the following mount-relative redirect would give
you `http://example.com/blog/admin/post/new`:

```
res.redirect('admin/post/new')
```

Pathname relative redirects are also possible. If you were
on `http://example.com/admin/post/new`, the following redirect
would land you at `http//example.com/admin/post`:

```
res.redirect('..')
```

The final special-case is a `back` redirect, redirecting back to
the Referer (or Referrer), defaulting to `/` when missing.

```
res.redirect('back')
```

### res.location

Set the location header.

```
res.location('/foo/bar')
res.location('foo/bar')
res.location('http://example.com')
res.location('../login')
res.location('back')
```

You can use the same kind of `urls` as in `res.redirect()`.

For example, if your application is mounted at `/blog`,
the following would set the `location` header to
`/blog/admin`:

```
res.location('admin')
```

### res.charset

Assign the charset. Defaults to “utf-8”.

```
res.charset = 'value'
res.send('<p>some html</p>')
// => Content-Type: text/html; charset=value
```

### res.send([body|status], [body])

Send a response.

```
res.send(Buffer.from('whoop'))
res.send({ some: 'json' })
res.send('<p>some html</p>')
res.send(404, 'Sorry, we cannot find that!')
res.send(500, { error: 'something blew up' })
res.send(200)
```

This method performs a myriad of
useful tasks for simple non-streaming responses such
as automatically assigning the Content-Length unless
previously defined and providing automatic *HEAD* and
HTTP cache freshness support.

When a `Buffer` is given
the Content-Type is set to “application/octet-stream”
unless previously defined as shown below:

```
res.set('Content-Type', 'text/html')
res.send(Buffer.from('<p>some html</p>'))
```

When a `String` is given the
Content-Type is set defaulted to “text/html”:

```
res.send('<p>some html</p>')
```

When an `Array` or `Object` is
given Express will respond with the JSON representation:

```
res.send({ user: 'tobi' })
res.send([1, 2, 3])
```

Finally when a `Number` is given without
any of the previously mentioned bodies, then a response
body string is assigned for you. For example 200 will
respond will the text “OK”, and 404 “Not Found” and so on.

```
res.send(200)
res.send(404)
res.send(500)
```

### res.json([status|body], [body])

Send a JSON response. This method is identical
to `res.send()` when an object or
array is passed, however it may be used for
explicit JSON conversion of non-objects (null, undefined, etc),
though these are technically not valid JSON.

```
res.json(null)
res.json({ user: 'tobi' })
res.json(500, { error: 'message' })
```

### res.jsonp([status|body], [body])

Send a JSON response with JSONP support. This method is identical
to `res.json()` however opts-in to JSONP callback
support.

```
res.jsonp(null)
// => null

res.jsonp({ user: 'tobi' })
// => { "user": "tobi" }

res.jsonp(500, { error: 'message' })
// => { "error": "message" }
```

By default the JSONP callback name is simply `callback`,
however you may alter this with the [jsonp callback name](#app-settings)
setting. The following are some examples of JSONP responses using the same
code:

```
// ?callback=foo
res.jsonp({ user: 'tobi' })
// => foo({ "user": "tobi" })

app.set('jsonp callback name', 'cb')

// ?cb=foo
res.jsonp(500, { error: 'message' })
// => foo({ "error": "message" })
```

### res.type(type)

Sets the Content-Type to the mime lookup of `type`,
or when “/” is present the Content-Type is simply set to this
literal value.

```
res.type('.html')
res.type('html')
res.type('json')
res.type('application/json')
res.type('png')
```

p Aliased as `res.contentType(type)`.

### res.format(object)

Performs content-negotiation on the request Accept header
field when present. This method uses `req.accepted`, an array of
acceptable types ordered by their quality values, otherwise the
first callback is invoked. When no match is performed the server
responds with 406 “Not Acceptable”, or invokes the `default`
callback.

The Content-Type is set for you when a callback is selected,
however you may alter this within the callback using `res.set()`
or `res.type()` etcetera.

The following example would respond with `{ "message": "hey" }`
when the Accept header field is set to “application/json” or “*/json”,
however if “*/*” is given then “hey” will be the response.

```
res.format({
  'text/plain': function () {
    res.send('hey')
  },

  'text/html': function () {
    res.send('<p>hey</p>')
  },

  'application/json': function () {
    res.send({ message: 'hey' })
  }
})
```

In addition to canonicalized MIME types you may also
use extnames mapped to these types, providing a slightly
less verbose implementation:

```
res.format({
  text: function () {
    res.send('hey')
  },

  html: function () {
    res.send('<p>hey</p>')
  },

  json: function () {
    res.send({ message: 'hey' })
  }
})
```

### res.attachment([filename])

Sets the Content-Disposition header field to “attachment”. If
a `filename` is given then the Content-Type will be
automatically set based on the extname via `res.type()`,
and the Content-Disposition’s “filename=” parameter will be set.

```
res.attachment()
// Content-Disposition: attachment

res.attachment('path/to/logo.png')
// Content-Disposition: attachment; filename="logo.png"
// Content-Type: image/png
```

### res.sendfile(path, [options], [fn]])

Transfer the file at the given `path`.

Automatically defaults the Content-Type response header field based
on the filename’s extension. The callback `fn(err)` is
invoked when the transfer is complete or when an error occurs.

Options:

- `maxAge` in milliseconds defaulting to 0
- `root` root directory for relative filenames

This method provides fine-grained support for file serving
as illustrated in the following example:

```
app.get('/user/:uid/photos/:file', function (req, res) {
  var uid = req.params.uid
  var file = req.params.file

  req.user.mayViewFilesFrom(uid, function (yes) {
    if (yes) {
      res.sendfile('/uploads/' + uid + '/' + file)
    } else {
      res.send(403, 'Sorry! you cant see that.')
    }
  })
})
```

### res.download(path, [filename], [fn])

Transfer the file at `path` as an “attachment”,
typically browsers will prompt the user for download. The
Content-Disposition “filename=” parameter, aka the one
that will appear in the brower dialog is set to `path`
by default, however you may provide an override `filename`.

When an error has ocurred or transfer is complete the optional
callback `fn` is invoked. This method uses [res.sendfile()](#res.sendfile)
to transfer the file.

```
res.download('/report-12345.pdf')

res.download('/report-12345.pdf', 'report.pdf')

res.download('/report-12345.pdf', 'report.pdf', function (err) {
  if (err) {
    // handle error, keep in mind the response may be partially-sent
    // so check res.headerSent
  } else {
    // decrement a download credit etc
  }
})
```

### res.links(links)

Join the given `links` to populate the “Link” response header field.

```
res.links({
  next: 'http://api.example.com/users?page=2',
  last: 'http://api.example.com/users?page=5'
})
```

p yields:

```
Link: <http://api.example.com/users?page=2> rel="next",
      <http://api.example.com/users?page=5> rel="last"
```

### res.locals

Response local variables are scoped to the request, thus only
available to the view(s) rendered during that request / response
cycle, if any. Otherwise this API is identical to [app.locals](#app.locals).

This object is useful for exposing request-level information such as the
request pathname, authenticated user, user settings etcetera.

```
app.use(function (req, res, next) {
  res.locals.user = req.user
  res.locals.authenticated = !req.user.anonymous
  next()
})
```

### res.render(view, [locals], callback)

Render a `view` with a callback responding with
the rendered string. When an error occurs `next(err)`
is invoked internally. When a callback is provided both the possible error
and rendered string are passed, and no automated response is performed.

```
res.render('index', function (err, html) {
  // ...
})

res.render('user', { name: 'Tobi' }, function (err, html) {
  // ...
})
```

### res.req

This property holds a reference to the [request object](#request)
that relates to this response object.

## Middleware

### basicAuth()

Basic Authentication middleware, populating `req.user`
with the username.

Simple username and password:

```
app.use(express.basicAuth('username', 'password'))
```

Callback verification:

```
app.use(express.basicAuth(function (user, pass) {
  return user === 'tj' && pass === 'wahoo'
}))
```

Async callback verification, accepting `fn(err, user)`,
in this case `req.user` will be the user object passed.

```
app.use(express.basicAuth(function (user, pass, fn) {
  User.authenticate({ user: user, pass: pass }, fn)
}))
```

### bodyParser()

Request body parsing middleware supporting JSON, urlencoded,
and multipart requests. This middleware is simply a wrapper
for the `json()`, `urlencoded()`, and
`multipart()` middleware.

```
app.use(express.bodyParser())

// is equivalent to:
app.use(express.json())
app.use(express.urlencoded())
app.use(express.multipart())
```

For security sake, it’s better to disable file upload if your application
doesn’t need it. To do this, use only the needed middleware, i.e. don’t use
the `bodyParser` and `multipart()` middleware:

```
app.use(express.json())
app.use(express.urlencoded())
```

If your application needs file upload you should set up
[a strategy for dealing with those files](https://groups.google.com/d/msg/express-js/iP2VyhkypHo/5AXQiYN3RPcJ).

### compress()

Compress response data with gzip / deflate. This middleware
should be placed “high” within the stack to ensure all
responses may be compressed.

```
app.use(express.logger())
app.use(express.compress())
app.use(express.methodOverride())
app.use(express.bodyParser())
```

### cookieParser()

Parses the Cookie header field and populates `req.cookies`
with an object keyed by the cookie names. Optionally you may enabled
signed cookie support by passing a `secret` string.

```
app.use(express.cookieParser())
app.use(express.cookieParser('some secret'))
```

### cookieSession()

Provides cookie-based sessions, and populates `req.session`.
This middleware takes the following options:

- `key` cookie name defaulting to `connect.sess`
- `secret` prevents cookie tampering
- `cookie` session cookie settings, defaulting to `{ path: '/', httpOnly: true, maxAge: null }`
- `proxy` trust the reverse proxy when setting secure cookies (via “x-forwarded-proto”)

```
app.use(express.cookieSession())
```

To clear a cookie simply assign the session to null before responding:

```
req.session = null
```

### csrf()

CSRF protection middleware.

By default this middleware generates a token named “_csrf”
which should be added to requests which mutate
state, within a hidden form field, query-string etc. This
token is validated against `req.csrfToken()`.

The default `value` function checks `req.body` generated
by the `bodyParser()` middleware, `req.query` generated
by `query()`, and the “X-CSRF-Token” header field.

This middleware requires session support, thus should be added
somewhere below `session()`.

### directory()

Directory serving middleware, serves the given `path`.
This middleware may be paired with `static()` to serve
files, providing a full-featured file browser.

```
app.use(express.directory('public'))
app.use(express.static('public'))
```

This middleware accepts the following options:

- `hidden` display hidden (dot) files. Defaults to false.
- `icons`  display icons. Defaults to false.
- `filter` Apply this filter function to files. Defaults to false.

   [Edit this page](https://github.com/expressjs/expressjs.com/tree/gh-pages/_includes/api/en/3x          )
