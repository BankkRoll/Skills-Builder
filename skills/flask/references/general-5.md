# Debugging Application Errors¶ and more

# Debugging Application Errors¶

# Debugging Application Errors

## In Production

**Do not run the development server, or enable the built-in debugger, in
a production environment.** The debugger allows executing arbitrary
Python code from the browser. It’s protected by a pin, but that should
not be relied on for security.

Use an error logging tool, such as Sentry, as described in
[Error Logging Tools](https://flask.palletsprojects.com/en/errorhandling/#error-logging-tools), or enable logging and notifications as
described in [Logging](https://flask.palletsprojects.com/en/logging/).

If you have access to the server, you could add some code to start an
external debugger if `request.remote_addr` matches your IP. Some IDE
debuggers also have a remote mode so breakpoints on the server can be
interacted with locally. Only enable a debugger temporarily.

## The Built-In Debugger

The built-in Werkzeug development server provides a debugger which shows
an interactive traceback in the browser when an unhandled error occurs
during a request. This debugger should only be used during development.

 ![screenshot of debugger in action](https://flask.palletsprojects.com/en/_images/debugger.png)

Warning

The debugger allows executing arbitrary Python code from the
browser. It is protected by a pin, but still represents a major
security risk. Do not run the development server or debugger in a
production environment.

The debugger is enabled by default when the development server is run in debug mode.

```
$ flask --app hello run --debug
```

When running from Python code, passing `debug=True` enables debug mode, which is
mostly equivalent.

```
app.run(debug=True)
```

[Development Server](https://flask.palletsprojects.com/en/server/) and [Command Line Interface](https://flask.palletsprojects.com/en/cli/) have more information about running the debugger and
debug mode. More information about the debugger can be found in the [Werkzeug
documentation](https://werkzeug.palletsprojects.com/debug/).

## External Debuggers

External debuggers, such as those provided by IDEs, can offer a more
powerful debugging experience than the built-in debugger. They can also
be used to step through code during a request before an error is raised,
or if no error is raised. Some even have a remote mode so you can debug
code running on another machine.

When using an external debugger, the app should still be in debug mode, otherwise Flask
turns unhandled errors into generic 500 error pages. However, the built-in debugger and
reloader should be disabled so they don’t interfere with the external debugger.

```
$ flask --app hello run --debug --no-debugger --no-reload
```

When running from Python:

```
app.run(debug=True, use_debugger=False, use_reloader=False)
```

Disabling these isn’t required, an external debugger will continue to work with the
following caveats.

- If the built-in debugger is not disabled, it will catch unhandled exceptions before
  the external debugger can.
- If the reloader is not disabled, it could cause an unexpected reload if code changes
  during a breakpoint.
- The development server will still catch unhandled exceptions if the built-in
  debugger is disabled, otherwise it would crash on any error. If you want that (and
  usually you don’t) pass `passthrough_errors=True` to `app.run`.
  ```
  app.run(
      debug=True, passthrough_errors=True,
      use_debugger=False, use_reloader=False
  )
  ```

---

# Deploying to Production¶

# Deploying to Production

After developing your application, you’ll want to make it available
publicly to other users. When you’re developing locally, you’re probably
using the built-in development server, debugger, and reloader. These
should not be used in production. Instead, you should use a dedicated
WSGI server or hosting platform, some of which will be described here.

“Production” means “not development”, which applies whether you’re
serving your application publicly to millions of users or privately /
locally to a single user. **Do not use the development server when
deploying to production. It is intended for use only during local
development. It is not designed to be particularly secure, stable, or
efficient.**

## Self-Hosted Options

Flask is a WSGI *application*. A WSGI *server* is used to run the
application, converting incoming HTTP requests to the standard WSGI
environ, and converting outgoing WSGI responses to HTTP responses.

The primary goal of these docs is to familiarize you with the concepts
involved in running a WSGI application using a production WSGI server
and HTTP server. There are many WSGI servers and HTTP servers, with many
configuration possibilities. The pages below discuss the most common
servers, and show the basics of running each one. The next section
discusses platforms that can manage this for you.

- [Gunicorn](https://flask.palletsprojects.com/en/stable/gunicorn/)
- [Waitress](https://flask.palletsprojects.com/en/stable/waitress/)
- [mod_wsgi](https://flask.palletsprojects.com/en/stable/mod_wsgi/)
- [uWSGI](https://flask.palletsprojects.com/en/stable/uwsgi/)
- [gevent](https://flask.palletsprojects.com/en/stable/gevent/)
- [ASGI](https://flask.palletsprojects.com/en/stable/asgi/)

WSGI servers have HTTP servers built-in. However, a dedicated HTTP
server may be safer, more efficient, or more capable. Putting an HTTP
server in front of the WSGI server is called a “reverse proxy.”

- [Tell Flask it is Behind a Proxy](https://flask.palletsprojects.com/en/stable/proxy_fix/)
- [nginx](https://flask.palletsprojects.com/en/stable/nginx/)
- [Apache httpd](https://flask.palletsprojects.com/en/stable/apache-httpd/)

This list is not exhaustive, and you should evaluate these and other
servers based on your application’s needs. Different servers will have
different capabilities, configuration, and support.

## Hosting Platforms

There are many services available for hosting web applications without
needing to maintain your own server, networking, domain, etc. Some
services may have a free tier up to a certain time or bandwidth. Many of
these services use one of the WSGI servers described above, or a similar
interface. The links below are for some of the most common platforms,
which have instructions for Flask, WSGI, or Python.

- [PythonAnywhere](https://help.pythonanywhere.com/pages/Flask/)
- [Google App Engine](https://cloud.google.com/appengine/docs/standard/python3/building-app)
- [Google Cloud Run](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
- [Microsoft Azure](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)

This list is not exhaustive, and you should evaluate these and other
services based on your application’s needs. Different services will have
different capabilities, configuration, pricing, and support.

You’ll probably need to [Tell Flask it is Behind a Proxy](https://flask.palletsprojects.com/en/stable/proxy_fix/) when using most hosting
platforms.

---

# Design Decisions in Flask¶

# Design Decisions in Flask

If you are curious why Flask does certain things the way it does and not
differently, this section is for you.  This should give you an idea about
some of the design decisions that may appear arbitrary and surprising at
first, especially in direct comparison with other frameworks.

## The Explicit Application Object

A Python web application based on WSGI has to have one central callable
object that implements the actual application.  In Flask this is an
instance of the [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) class.  Each Flask application has
to create an instance of this class itself and pass it the name of the
module, but why can’t Flask do that itself?

Without such an explicit application object the following code:

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'
```

Would look like this instead:

```
from hypothetical_flask import route

@route('/')
def index():
    return 'Hello World!'
```

There are three major reasons for this.  The most important one is that
implicit application objects require that there may only be one instance at
the time.  There are ways to fake multiple applications with a single
application object, like maintaining a stack of applications, but this
causes some problems I won’t outline here in detail.  Now the question is:
when does a microframework need more than one application at the same
time?  A good example for this is unit testing.  When you want to test
something it can be very helpful to create a minimal application to test
specific behavior.  When the application object is deleted everything it
allocated will be freed again.

Another thing that becomes possible when you have an explicit object lying
around in your code is that you can subclass the base class
([Flask](https://flask.palletsprojects.com/en/api/#flask.Flask)) to alter specific behavior.  This would not be
possible without hacks if the object were created ahead of time for you
based on a class that is not exposed to you.

But there is another very important reason why Flask depends on an
explicit instantiation of that class: the package name.  Whenever you
create a Flask instance you usually pass it `__name__` as package name.
Flask depends on that information to properly load resources relative
to your module.  With Python’s outstanding support for reflection it can
then access the package to figure out where the templates and static files
are stored (see [open_resource()](https://flask.palletsprojects.com/en/api/#flask.Flask.open_resource)).  Now obviously there
are frameworks around that do not need any configuration and will still be
able to load templates relative to your application module.  But they have
to use the current working directory for that, which is a very unreliable
way to determine where the application is.  The current working directory
is process-wide and if you are running multiple applications in one
process (which could happen in a webserver without you knowing) the paths
will be off.  Worse: many webservers do not set the working directory to
the directory of your application but to the document root which does not
have to be the same folder.

The third reason is “explicit is better than implicit”.  That object is
your WSGI application, you don’t have to remember anything else.  If you
want to apply a WSGI middleware, just wrap it and you’re done (though
there are better ways to do that so that you do not lose the reference
to the application object [wsgi_app()](https://flask.palletsprojects.com/en/api/#flask.Flask.wsgi_app)).

Furthermore this design makes it possible to use a factory function to
create the application which is very helpful for unit testing and similar
things ([Application Factories](https://flask.palletsprojects.com/en/patterns/appfactories/)).

## The Routing System

Flask uses the Werkzeug routing system which was designed to
automatically order routes by complexity.  This means that you can declare
routes in arbitrary order and they will still work as expected.  This is a
requirement if you want to properly implement decorator based routing
since decorators could be fired in undefined order when the application is
split into multiple modules.

Another design decision with the Werkzeug routing system is that routes
in Werkzeug try to ensure that URLs are unique.  Werkzeug will go quite far
with that in that it will automatically redirect to a canonical URL if a route
is ambiguous.

## One Template Engine

Flask decides on one template engine: Jinja.  Why doesn’t Flask have a
pluggable template engine interface?  You can obviously use a different
template engine, but Flask will still configure Jinja for you.  While
that limitation that Jinja is *always* configured will probably go away,
the decision to bundle one template engine and use that will not.

Template engines are like programming languages and each of those engines
has a certain understanding about how things work.  On the surface they
all work the same: you tell the engine to evaluate a template with a set
of variables and take the return value as string.

But that’s about where similarities end. Jinja for example has an
extensive filter system, a certain way to do template inheritance,
support for reusable blocks (macros) that can be used from inside
templates and also from Python code, supports iterative template
rendering, configurable syntax and more. On the other hand an engine
like Genshi is based on XML stream evaluation, template inheritance by
taking the availability of XPath into account and more. Mako on the
other hand treats templates similar to Python modules.

When it comes to connecting a template engine with an application or
framework there is more than just rendering templates.  For instance,
Flask uses Jinja’s extensive autoescaping support.  Also it provides
ways to access macros from Jinja templates.

A template abstraction layer that would not take the unique features of
the template engines away is a science on its own and a too large
undertaking for a microframework like Flask.

Furthermore extensions can then easily depend on one template language
being present.  You can easily use your own templating language, but an
extension could still depend on Jinja itself.

## What does “micro” mean?

“Micro” does not mean that your whole web application has to fit into a single
Python file (although it certainly can), nor does it mean that Flask is lacking
in functionality. The “micro” in microframework means Flask aims to keep the
core simple but extensible. Flask won’t make many decisions for you, such as
what database to use. Those decisions that it does make, such as what
templating engine to use, are easy to change.  Everything else is up to you, so
that Flask can be everything you need and nothing you don’t.

By default, Flask does not include a database abstraction layer, form
validation or anything else where different libraries already exist that can
handle that. Instead, Flask supports extensions to add such functionality to
your application as if it was implemented in Flask itself. Numerous extensions
provide database integration, form validation, upload handling, various open
authentication technologies, and more. Flask may be “micro”, but it’s ready for
production use on a variety of needs.

Why does Flask call itself a microframework and yet it depends on two
libraries (namely Werkzeug and Jinja).  Why shouldn’t it?  If we look
over to the Ruby side of web development there we have a protocol very
similar to WSGI.  Just that it’s called Rack there, but besides that it
looks very much like a WSGI rendition for Ruby.  But nearly all
applications in Ruby land do not work with Rack directly, but on top of a
library with the same name.  This Rack library has two equivalents in
Python: WebOb (formerly Paste) and Werkzeug.  Paste is still around but
from my understanding it’s sort of deprecated in favour of WebOb.  The
development of WebOb and Werkzeug started side by side with similar ideas
in mind: be a good implementation of WSGI for other applications to take
advantage.

Flask is a framework that takes advantage of the work already done by
Werkzeug to properly interface WSGI (which can be a complex task at
times).  Thanks to recent developments in the Python package
infrastructure, packages with dependencies are no longer an issue and
there are very few reasons against having libraries that depend on others.

## Thread Locals

Flask uses thread local objects (context local objects in fact, they
support greenlet contexts as well) for request, session and an extra
object you can put your own things on ([g](https://flask.palletsprojects.com/en/api/#flask.g)).  Why is that and
isn’t that a bad idea?

Yes it is usually not such a bright idea to use thread locals.  They cause
troubles for servers that are not based on the concept of threads and make
large applications harder to maintain.  However Flask is just not designed
for large applications or asynchronous servers.  Flask wants to make it
quick and easy to write a traditional web application.

## Async/await and ASGI support

Flask supports `async` coroutines for view functions by executing the
coroutine on a separate thread instead of using an event loop on the
main thread as an async-first (ASGI) framework would. This is necessary
for Flask to remain backwards compatible with extensions and code built
before `async` was introduced into Python. This compromise introduces
a performance cost compared with the ASGI frameworks, due to the
overhead of the threads.

Due to how tied to WSGI Flask’s code is, it’s not clear if it’s possible
to make the `Flask` class support ASGI and WSGI at the same time. Work
is currently being done in Werkzeug to work with ASGI, which may
eventually enable support in Flask as well.

See [Using async and await](https://flask.palletsprojects.com/en/async-await/) for more discussion.

## What Flask is, What Flask is Not

Flask will never have a database layer.  It will not have a form library
or anything else in that direction.  Flask itself just bridges to Werkzeug
to implement a proper WSGI application and to Jinja to handle templating.
It also binds to a few common standard library packages such as logging.
Everything else is up for extensions.

Why is this the case?  Because people have different preferences and
requirements and Flask could not meet those if it would force any of this
into the core.  The majority of web applications will need a template
engine in some sort.  However not every application needs a SQL database.

As your codebase grows, you are free to make the design decisions appropriate
for your project.  Flask will continue to provide a very simple glue layer to
the best that Python has to offer.  You can implement advanced patterns in
SQLAlchemy or another database tool, introduce non-relational data persistence
as appropriate, and take advantage of framework-agnostic tools built for WSGI,
the Python web interface.

The idea of Flask is to build a good foundation for all applications.
Everything else is up to you or extensions.

---

# Handling Application Errors¶

# Handling Application Errors

Applications fail, servers fail. Sooner or later you will see an exception
in production. Even if your code is 100% correct, you will still see
exceptions from time to time. Why? Because everything else involved will
fail. Here are some situations where perfectly fine code can lead to server
errors:

- the client terminated the request early and the application was still
  reading from the incoming data
- the database server was overloaded and could not handle the query
- a filesystem is full
- a harddrive crashed
- a backend server overloaded
- a programming error in a library you are using
- network connection of the server to another system failed

And that’s just a small sample of issues you could be facing. So how do we
deal with that sort of problem? By default if your application runs in
production mode, and an exception is raised Flask will display a very simple
page for you and log the exception to the [logger](https://flask.palletsprojects.com/en/api/#flask.Flask.logger).

But there is more you can do, and we will cover some better setups to deal
with errors including custom exceptions and 3rd party tools.

## Error Logging Tools

Sending error mails, even if just for critical ones, can become
overwhelming if enough users are hitting the error and log files are
typically never looked at. This is why we recommend using [Sentry](https://sentry.io/) for dealing with application errors. It’s
available as a source-available project [on GitHub](https://github.com/getsentry/sentry) and is also available as a [hosted version](https://sentry.io/signup/) which you can try for free. Sentry
aggregates duplicate errors, captures the full stack trace and local
variables for debugging, and sends you mails based on new errors or
frequency thresholds.

To use Sentry you need to install the `sentry-sdk` client with extra
`flask` dependencies.

```
$ pip install sentry-sdk[flask]
```

And then add this to your Flask app:

```
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init('YOUR_DSN_HERE', integrations=[FlaskIntegration()])
```

The `YOUR_DSN_HERE` value needs to be replaced with the DSN value you
get from your Sentry installation.

After installation, failures leading to an Internal Server Error
are automatically reported to Sentry and from there you can
receive error notifications.

See also:

- Sentry also supports catching errors from a worker queue
  (RQ, Celery, etc.) in a similar fashion. See the [Python SDK docs](https://docs.sentry.io/platforms/python/) for more information.
- [Flask-specific documentation](https://docs.sentry.io/platforms/python/guides/flask/)

## Error Handlers

When an error occurs in Flask, an appropriate [HTTP status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) will be
returned. 400-499 indicate errors with the client’s request data, or
about the data requested. 500-599 indicate errors with the server or
application itself.

You might want to show custom error pages to the user when an error occurs.
This can be done by registering error handlers.

An error handler is a function that returns a response when a type of error is
raised, similar to how a view is a function that returns a response when a
request URL is matched. It is passed the instance of the error being handled,
which is most likely a [HTTPException](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.HTTPException).

The status code of the response will not be set to the handler’s code. Make
sure to provide the appropriate HTTP status code when returning a response from
a handler.

### Registering

Register handlers by decorating a function with
[errorhandler()](https://flask.palletsprojects.com/en/api/#flask.Flask.errorhandler). Or use
[register_error_handler()](https://flask.palletsprojects.com/en/api/#flask.Flask.register_error_handler) to register the function later.
Remember to set the error code when returning the response.

```
@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400

# or, without the decorator
app.register_error_handler(400, handle_bad_request)
```

[werkzeug.exceptions.HTTPException](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.HTTPException) subclasses like
[BadRequest](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.BadRequest) and their HTTP codes are interchangeable
when registering handlers. (`BadRequest.code == 400`)

Non-standard HTTP codes cannot be registered by code because they are not known
by Werkzeug. Instead, define a subclass of
[HTTPException](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.HTTPException) with the appropriate code and
register and raise that exception class.

```
class InsufficientStorage(werkzeug.exceptions.HTTPException):
    code = 507
    description = 'Not enough storage space.'

app.register_error_handler(InsufficientStorage, handle_507)

raise InsufficientStorage()
```

Handlers can be registered for any exception class, not just
[HTTPException](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.HTTPException) subclasses or HTTP status
codes. Handlers can be registered for a specific class, or for all subclasses
of a parent class.

### Handling

When building a Flask application you *will* run into exceptions. If some part
of your code breaks while handling a request (and you have no error handlers
registered), a “500 Internal Server Error”
([InternalServerError](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.InternalServerError)) will be returned by default.
Similarly, “404 Not Found”
([NotFound](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.NotFound)) error will occur if a request is sent to an unregistered route.
If a route receives an unallowed request method, a “405 Method Not Allowed”
([MethodNotAllowed](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.MethodNotAllowed)) will be raised. These are all
subclasses of [HTTPException](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.HTTPException) and are provided by
default in Flask.

Flask gives you the ability to raise any HTTP exception registered by
Werkzeug. However, the default HTTP exceptions return simple exception
pages. You might want to show custom error pages to the user when an error occurs.
This can be done by registering error handlers.

When Flask catches an exception while handling a request, it is first looked up by code.
If no handler is registered for the code, Flask looks up the error by its class hierarchy; the most specific handler is chosen.
If no handler is registered, [HTTPException](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.HTTPException) subclasses show a
generic message about their code, while other exceptions are converted to a
generic “500 Internal Server Error”.

For example, if an instance of [ConnectionRefusedError](https://docs.python.org/3/library/exceptions.html#ConnectionRefusedError) is raised,
and a handler is registered for [ConnectionError](https://docs.python.org/3/library/exceptions.html#ConnectionError) and
[ConnectionRefusedError](https://docs.python.org/3/library/exceptions.html#ConnectionRefusedError), the more specific [ConnectionRefusedError](https://docs.python.org/3/library/exceptions.html#ConnectionRefusedError)
handler is called with the exception instance to generate the response.

Handlers registered on the blueprint take precedence over those registered
globally on the application, assuming a blueprint is handling the request that
raises the exception. However, the blueprint cannot handle 404 routing errors
because the 404 occurs at the routing level before the blueprint can be
determined.

### Generic Exception Handlers

It is possible to register error handlers for very generic base classes
such as `HTTPException` or even `Exception`. However, be aware that
these will catch more than you might expect.

For example, an error handler for `HTTPException` might be useful for turning
the default HTML errors pages into JSON. However, this
handler will trigger for things you don’t cause directly, such as 404
and 405 errors during routing. Be sure to craft your handler carefully
so you don’t lose information about the HTTP error.

```
from flask import json
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
```

An error handler for `Exception` might seem useful for changing how
all errors, even unhandled ones, are presented to the user. However,
this is similar to doing `except Exception:` in Python, it will
capture *all* otherwise unhandled errors, including all HTTP status
codes.

In most cases it will be safer to register handlers for more
specific exceptions. Since `HTTPException` instances are valid WSGI
responses, you could also pass them through directly.

```
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", e=e), 500
```

Error handlers still respect the exception class hierarchy. If you
register handlers for both `HTTPException` and `Exception`, the
`Exception` handler will not handle `HTTPException` subclasses
because the `HTTPException` handler is more specific.

### Unhandled Exceptions

When there is no error handler registered for an exception, a 500
Internal Server Error will be returned instead. See
[flask.Flask.handle_exception()](https://flask.palletsprojects.com/en/api/#flask.Flask.handle_exception) for information about this
behavior.

If there is an error handler registered for `InternalServerError`,
this will be invoked. As of Flask 1.1.0, this error handler will always
be passed an instance of `InternalServerError`, not the original
unhandled error.

The original error is available as `e.original_exception`.

An error handler for “500 Internal Server Error” will be passed uncaught
exceptions in addition to explicit 500 errors. In debug mode, a handler
for “500 Internal Server Error” will not be used. Instead, the
interactive debugger will be shown.

## Custom Error Pages

Sometimes when building a Flask application, you might want to raise a
[HTTPException](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.HTTPException) to signal to the user that
something is wrong with the request. Fortunately, Flask comes with a handy
[abort()](https://flask.palletsprojects.com/en/api/#flask.abort) function that aborts a request with a HTTP error from
werkzeug as desired. It will also provide a plain black and white error page
for you with a basic description, but nothing fancy.

Depending on the error code it is less or more likely for the user to
actually see such an error.

Consider the code below, we might have a user profile route, and if the user
fails to pass a username we can raise a “400 Bad Request”. If the user passes a
username and we can’t find it, we raise a “404 Not Found”.

```
from flask import abort, render_template, request

# a username needs to be supplied in the query args
# a successful request would be like /profile?username=jack
@app.route("/profile")
def user_profile():
    username = request.arg.get("username")
    # if a username isn't supplied in the request, return a 400 bad request
    if username is None:
        abort(400)

    user = get_user(username=username)
    # if a user can't be found by their username, return 404 not found
    if user is None:
        abort(404)

    return render_template("profile.html", user=user)
```

Here is another example implementation for a “404 Page Not Found” exception:

```
from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
```

When using [Application Factories](https://flask.palletsprojects.com/en/patterns/appfactories/):

```
from flask import Flask, render_template

def page_not_found(e):
  return render_template('404.html'), 404

def create_app(config_filename):
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    return app
```

An example template might be this:

```
{% extends "layout.html" %}
{% block title %}Page Not Found{% endblock %}
{% block body %}
  <h1>Page Not Found</h1>
  <p>What you were looking for is just not there.
  <p><a href="{{ url_for('index') }}">go somewhere nice</a>
{% endblock %}
```

### Further Examples

The above examples wouldn’t actually be an improvement on the default
exception pages. We can create a custom 500.html template like this:

```
{% extends "layout.html" %}
{% block title %}Internal Server Error{% endblock %}
{% block body %}
  <h1>Internal Server Error</h1>
  <p>Oops... we seem to have made a mistake, sorry!</p>
  <p><a href="{{ url_for('index') }}">Go somewhere nice instead</a>
{% endblock %}
```

It can be implemented by rendering the template on “500 Internal Server Error”:

```
from flask import render_template

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500
```

When using [Application Factories](https://flask.palletsprojects.com/en/patterns/appfactories/):

```
from flask import Flask, render_template

def internal_server_error(e):
  return render_template('500.html'), 500

def create_app():
    app = Flask(__name__)
    app.register_error_handler(500, internal_server_error)
    return app
```

When using [Modular Applications with Blueprints](https://flask.palletsprojects.com/en/blueprints/):

```
from flask import Blueprint

blog = Blueprint('blog', __name__)

# as a decorator
@blog.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# or with register_error_handler
blog.register_error_handler(500, internal_server_error)
```

## Blueprint Error Handlers

In [Modular Applications with Blueprints](https://flask.palletsprojects.com/en/blueprints/), most error handlers will work as expected.
However, there is a caveat concerning handlers for 404 and 405
exceptions. These error handlers are only invoked from an appropriate
`raise` statement or a call to `abort` in another of the blueprint’s
view functions; they are not invoked by, e.g., an invalid URL access.

This is because the blueprint does not “own” a certain URL space, so
the application instance has no way of knowing which blueprint error
handler it should run if given an invalid URL. If you would like to
execute different handling strategies for these errors based on URL
prefixes, they may be defined at the application level using the
`request` proxy object.

```
from flask import jsonify, render_template

# at the application level
# not the blueprint level
@app.errorhandler(404)
def page_not_found(e):
    # if a request is in our blog URL space
    if request.path.startswith('/blog/'):
        # we return a custom blog 404 page
        return render_template("blog/404.html"), 404
    else:
        # otherwise we return our generic site-wide 404 page
        return render_template("404.html"), 404

@app.errorhandler(405)
def method_not_allowed(e):
    # if a request has the wrong method to our API
    if request.path.startswith('/api/'):
        # we return a json saying so
        return jsonify(message="Method Not Allowed"), 405
    else:
        # otherwise we return a generic site-wide 405 page
        return render_template("405.html"), 405
```

## Returning API Errors as JSON

When building APIs in Flask, some developers realise that the built-in
exceptions are not expressive enough for APIs and that the content type of
*text/html* they are emitting is not very useful for API consumers.

Using the same techniques as above and [jsonify()](https://flask.palletsprojects.com/en/api/#flask.json.jsonify) we can return JSON
responses to API errors.  [abort()](https://flask.palletsprojects.com/en/api/#flask.abort) is called
with a `description` parameter. The error handler will
use that as the JSON error message, and set the status code to 404.

```
from flask import abort, jsonify

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route("/cheese")
def get_one_cheese():
    resource = get_resource()

    if resource is None:
        abort(404, description="Resource not found")

    return jsonify(resource)
```

We can also create custom exception classes. For instance, we can
introduce a new custom exception for an API that can take a proper human readable message,
a status code for the error and some optional payload to give more context
for the error.

This is a simple example:

```
from flask import jsonify, request

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

# an API app route for getting user information
# a correct request might be /api/user?user_id=420
@app.route("/api/user")
def user_api(user_id):
    user_id = request.arg.get("user_id")
    if not user_id:
        raise InvalidAPIUsage("No user id provided!")

    user = get_user(user_id=user_id)
    if not user:
        raise InvalidAPIUsage("No such user!", status_code=404)

    return jsonify(user.to_dict())
```

A view can now raise that exception with an error message. Additionally
some extra payload can be provided as a dictionary through the `payload`
parameter.

## Logging

See [Logging](https://flask.palletsprojects.com/en/logging/) for information about how to log exceptions, such as
by emailing them to admins.

## Debugging

See [Debugging Application Errors](https://flask.palletsprojects.com/en/debugging/) for information about how to debug errors in
development and production.
