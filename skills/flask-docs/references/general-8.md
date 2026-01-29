# The Request Context¶ and more

# The Request Context¶

# The Request Context

The request context keeps track of the request-level data during a
request. Rather than passing the request object to each function that
runs during a request, the [request](https://flask.palletsprojects.com/en/api/#flask.request) and [session](https://flask.palletsprojects.com/en/api/#flask.session) proxies
are accessed instead.

This is similar to [The Application Context](https://flask.palletsprojects.com/en/appcontext/), which keeps track of the
application-level data independent of a request. A corresponding
application context is pushed when a request context is pushed.

## Purpose of the Context

When the [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) application handles a request, it creates a
[Request](https://flask.palletsprojects.com/en/api/#flask.Request) object based on the environment it received from the
WSGI server. Because a *worker* (thread, process, or coroutine depending
on the server) handles only one request at a time, the request data can
be considered global to that worker during that request. Flask uses the
term *context local* for this.

Flask automatically *pushes* a request context when handling a request.
View functions, error handlers, and other functions that run during a
request will have access to the [request](https://flask.palletsprojects.com/en/api/#flask.request) proxy, which points to
the request object for the current request.

## Lifetime of the Context

When a Flask application begins handling a request, it pushes a request
context, which also pushes an [app context](https://flask.palletsprojects.com/en/appcontext/). When the
request ends it pops the request context then the application context.

The context is unique to each thread (or other worker type).
[request](https://flask.palletsprojects.com/en/api/#flask.request) cannot be passed to another thread, the other thread has
a different context space and will not know about the request the parent
thread was pointing to.

Context locals are implemented using Python’s [contextvars](https://docs.python.org/3/library/contextvars.html#module-contextvars) and
Werkzeug’s [LocalProxy](https://werkzeug.palletsprojects.com/en/stable/local/#werkzeug.local.LocalProxy). Python manages the
lifetime of context vars automatically, and local proxy wraps that
low-level interface to make the data easier to work with.

## Manually Push a Context

If you try to access [request](https://flask.palletsprojects.com/en/api/#flask.request), or anything that uses it, outside
a request context, you’ll get this error message:

```
RuntimeError: Working outside of request context.

This typically means that you attempted to use functionality that
needed an active HTTP request. Consult the documentation on testing
for information about how to avoid this problem.
```

This should typically only happen when testing code that expects an
active request. One option is to use the
[testclient](https://flask.palletsprojects.com/en/api/#flask.Flask.test_client) to simulate a full request. Or
you can use [test_request_context()](https://flask.palletsprojects.com/en/api/#flask.Flask.test_request_context) in a `with` block, and
everything that runs in the block will have access to [request](https://flask.palletsprojects.com/en/api/#flask.request),
populated with your test data.

```
def generate_report(year):
    format = request.args.get("format")
    ...

with app.test_request_context(
    "/make_report/2017", query_string={"format": "short"}
):
    generate_report()
```

If you see that error somewhere else in your code not related to
testing, it most likely indicates that you should move that code into a
view function.

For information on how to use the request context from the interactive
Python shell, see [Working with the Shell](https://flask.palletsprojects.com/en/shell/).

## How the Context Works

The [Flask.wsgi_app()](https://flask.palletsprojects.com/en/api/#flask.Flask.wsgi_app) method is called to handle each request. It
manages the contexts during the request. Internally, the request and
application contexts work like stacks. When contexts are pushed, the
proxies that depend on them are available and point at information from
the top item.

When the request starts, a [RequestContext](https://flask.palletsprojects.com/en/api/#flask.ctx.RequestContext) is created and
pushed, which creates and pushes an [AppContext](https://flask.palletsprojects.com/en/api/#flask.ctx.AppContext) first if
a context for that application is not already the top context. While
these contexts are pushed, the [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app), [g](https://flask.palletsprojects.com/en/api/#flask.g),
[request](https://flask.palletsprojects.com/en/api/#flask.request), and [session](https://flask.palletsprojects.com/en/api/#flask.session) proxies are available to the
original thread handling the request.

Other contexts may be pushed to change the proxies during a request.
While this is not a common pattern, it can be used in advanced
applications to, for example, do internal redirects or chain different
applications together.

After the request is dispatched and a response is generated and sent,
the request context is popped, which then pops the application context.
Immediately before they are popped, the [teardown_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_request)
and [teardown_appcontext()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_appcontext) functions are executed. These
execute even if an unhandled exception occurred during dispatch.

## Callbacks and Errors

Flask dispatches a request in multiple stages which can affect the
request, response, and how errors are handled. The contexts are active
during all of these stages.

A [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint) can add handlers for these events that are specific
to the blueprint. The handlers for a blueprint will run if the blueprint
owns the route that matches the request.

1. Before each request, [before_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.before_request) functions are
  called. If one of these functions return a value, the other
  functions are skipped. The return value is treated as the response
  and the view function is not called.
2. If the [before_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.before_request) functions did not return a
  response, the view function for the matched route is called and
  returns a response.
3. The return value of the view is converted into an actual response
  object and passed to the [after_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.after_request)
  functions. Each function returns a modified or new response object.
4. After the response is returned, the contexts are popped, which calls
  the [teardown_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_request) and
  [teardown_appcontext()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_appcontext) functions. These functions are
  called even if an unhandled exception was raised at any point above.

If an exception is raised before the teardown functions, Flask tries to
match it with an [errorhandler()](https://flask.palletsprojects.com/en/api/#flask.Flask.errorhandler) function to handle the
exception and return a response. If no error handler is found, or the
handler itself raises an exception, Flask returns a generic
`500 Internal Server Error` response. The teardown functions are still
called, and are passed the exception object.

If debug mode is enabled, unhandled exceptions are not converted to a
`500` response and instead are propagated to the WSGI server. This
allows the development server to present the interactive debugger with
the traceback.

### Teardown Callbacks

The teardown callbacks are independent of the request dispatch, and are
instead called by the contexts when they are popped. The functions are
called even if there is an unhandled exception during dispatch, and for
manually pushed contexts. This means there is no guarantee that any
other parts of the request dispatch have run first. Be sure to write
these functions in a way that does not depend on other callbacks and
will not fail.

During testing, it can be useful to defer popping the contexts after the
request ends, so that their data can be accessed in the test function.
Use the [test_client()](https://flask.palletsprojects.com/en/api/#flask.Flask.test_client) as a `with` block to preserve the
contexts until the `with` block exits.

```
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    print('during view')
    return 'Hello, World!'

@app.teardown_request
def show_teardown(exception):
    print('after with block')

with app.test_request_context():
    print('during with block')

# teardown functions are called after the context with block exits

with app.test_client() as client:
    client.get('/')
    # the contexts are not popped even though the request ended
    print(request.path)

# the contexts are popped and teardown functions are called after
# the client with block exits
```

### Signals

The following signals are sent:

1. [request_started](https://flask.palletsprojects.com/en/api/#flask.request_started) is sent before the [before_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.before_request) functions
  are called.
2. [request_finished](https://flask.palletsprojects.com/en/api/#flask.request_finished) is sent after the [after_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.after_request) functions
  are called.
3. [got_request_exception](https://flask.palletsprojects.com/en/api/#flask.got_request_exception) is sent when an exception begins to be handled, but
  before an [errorhandler()](https://flask.palletsprojects.com/en/api/#flask.Flask.errorhandler) is looked up or called.
4. [request_tearing_down](https://flask.palletsprojects.com/en/api/#flask.request_tearing_down) is sent after the [teardown_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_request)
  functions are called.

## Notes On Proxies

Some of the objects provided by Flask are proxies to other objects. The
proxies are accessed in the same way for each worker thread, but
point to the unique object bound to each worker behind the scenes as
described on this page.

Most of the time you don’t have to care about that, but there are some
exceptions where it is good to know that this object is actually a proxy:

- The proxy objects cannot fake their type as the actual object types.
  If you want to perform instance checks, you have to do that on the
  object being proxied.
- The reference to the proxied object is needed in some situations,
  such as sending [Signals](https://flask.palletsprojects.com/en/signals/) or passing data to a background
  thread.

If you need to access the underlying object that is proxied, use the
`_get_current_object()` method:

```
app = current_app._get_current_object()
my_signal.send(app)
```

---

# Development Server¶

# Development Server

Flask provides a `run` command to run the application with a development server. In
debug mode, this server provides an interactive debugger and will reload when code is
changed.

Warning

Do not use the development server when deploying to production. It
is intended for use only during local development. It is not
designed to be particularly efficient, stable, or secure.

See [Deploying to Production](https://flask.palletsprojects.com/en/deploying/) for deployment options.

## Command Line

The `flask run` CLI command is the recommended way to run the development server. Use
the `--app` option to point to your application, and the `--debug` option to enable
debug mode.

```
$ flask --app hello run --debug
```

This enables debug mode, including the interactive debugger and reloader, and then
starts the server on [http://localhost:5000/](http://localhost:5000/). Use `flask run --help` to see the
available options, and [Command Line Interface](https://flask.palletsprojects.com/en/cli/) for detailed instructions about configuring and using
the CLI.

### Address already in use

If another program is already using port 5000, you’ll see an `OSError`
when the server tries to start. It may have one of the following
messages:

- `OSError: [Errno 98] Address already in use`
- `OSError: [WinError 10013] An attempt was made to access a socket
  in a way forbidden by its access permissions`

Either identify and stop the other program, or use
`flask run --port 5001` to pick a different port.

You can use `netstat` or `lsof` to identify what process id is using
a port, then use other operating system tools stop that process. The
following example shows that process id 6847 is using port 5000.

```
$ netstat -nlp | grep 5000
tcp 0 0 127.0.0.1:5000 0.0.0.0:* LISTEN 6847/python
```

```
$ lsof -P -i :5000
Python 6847 IPv4 TCP localhost:5000 (LISTEN)
```

```
> netstat -ano | findstr 5000
TCP 127.0.0.1:5000 0.0.0.0:0 LISTENING 6847
```

macOS Monterey and later automatically starts a service that uses port
5000. You can choose to disable this service instead of using a different port by
searching for “AirPlay Receiver” in System Settings and toggling it off.

### Deferred Errors on Reload

When using the `flask run` command with the reloader, the server will
continue to run even if you introduce syntax errors or other
initialization errors into the code. Accessing the site will show the
interactive debugger for the error, rather than crashing the server.

If a syntax error is already present when calling `flask run`, it will
fail immediately and show the traceback rather than waiting until the
site is accessed. This is intended to make errors more visible initially
while still allowing the server to handle errors on reload.

## In Code

The development server can also be started from Python with the [Flask.run()](https://flask.palletsprojects.com/en/api/#flask.Flask.run)
method. This method takes arguments similar to the CLI options to control the server.
The main difference from the CLI command is that the server will crash if there are
errors when reloading. `debug=True` can be passed to enable debug mode.

Place the call in a main block, otherwise it will interfere when trying to import and
run the application with a production server later.

```
if __name__ == "__main__":
    app.run(debug=True)
```

```
$ python hello.py
```

---

# Working with the Shell¶

# Working with the Shell

  Changelog

Added in version 0.3.

One of the reasons everybody loves Python is the interactive shell.  It
basically allows you to execute Python commands in real time and
immediately get results back.  Flask itself does not come with an
interactive shell, because it does not require any specific setup upfront,
just import your application and start playing around.

There are however some handy helpers to make playing around in the shell a
more pleasant experience.  The main issue with interactive console
sessions is that you’re not triggering a request like a browser does which
means that [g](https://flask.palletsprojects.com/en/api/#flask.g), [request](https://flask.palletsprojects.com/en/api/#flask.request) and others are not
available.  But the code you want to test might depend on them, so what
can you do?

This is where some helper functions come in handy.  Keep in mind however
that these functions are not only there for interactive shell usage, but
also for unit testing and other situations that require a faked request
context.

Generally it’s recommended that you read [The Request Context](https://flask.palletsprojects.com/en/reqcontext/) first.

## Command Line Interface

Starting with Flask 0.11 the recommended way to work with the shell is the
`flask shell` command which does a lot of this automatically for you.
For instance the shell is automatically initialized with a loaded
application context.

For more information see [Command Line Interface](https://flask.palletsprojects.com/en/cli/).

## Creating a Request Context

The easiest way to create a proper request context from the shell is by
using the [test_request_context](https://flask.palletsprojects.com/en/api/#flask.Flask.test_request_context) method which creates
us a [RequestContext](https://flask.palletsprojects.com/en/api/#flask.ctx.RequestContext):

```
>>> ctx = app.test_request_context()
```

Normally you would use the `with` statement to make this request object
active, but in the shell it’s easier to use the
`push()` and
[pop()](https://flask.palletsprojects.com/en/api/#flask.ctx.RequestContext.pop) methods by hand:

```
>>> ctx.push()
```

From that point onwards you can work with the request object until you
call `pop`:

```
>>> ctx.pop()
```

## Firing Before/After Request

By just creating a request context, you still don’t have run the code that
is normally run before a request.  This might result in your database
being unavailable if you are connecting to the database in a
before-request callback or the current user not being stored on the
[g](https://flask.palletsprojects.com/en/api/#flask.g) object etc.

This however can easily be done yourself.  Just call
[preprocess_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.preprocess_request):

```
>>> ctx = app.test_request_context()
>>> ctx.push()
>>> app.preprocess_request()
```

Keep in mind that the [preprocess_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.preprocess_request) function
might return a response object, in that case just ignore it.

To shutdown a request, you need to trick a bit before the after request
functions (triggered by [process_response()](https://flask.palletsprojects.com/en/api/#flask.Flask.process_response)) operate on
a response object:

```
>>> app.process_response(app.response_class())
<Response 0 bytes [200 OK]>
>>> ctx.pop()
```

The functions registered as [teardown_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_request) are
automatically called when the context is popped.  So this is the perfect
place to automatically tear down resources that were needed by the request
context (such as database connections).

## Further Improving the Shell Experience

If you like the idea of experimenting in a shell, create yourself a module
with stuff you want to star import into your interactive session.  There
you could also define some more helper methods for common things such as
initializing the database, dropping tables etc.

Just put them into a module (like `shelltools`) and import from there:

```
>>> from shelltools import *
```

---

# Signals¶

# Signals

Signals are a lightweight way to notify subscribers of certain events during the
lifecycle of the application and each request. When an event occurs, it emits the
signal, which calls each subscriber.

Signals are implemented by the [Blinker](https://pypi.org/project/blinker/) library. See its documentation for detailed
information. Flask provides some built-in signals. Extensions may provide their own.

Many signals mirror Flask’s decorator-based callbacks with similar names. For example,
the [request_started](https://flask.palletsprojects.com/en/api/#flask.request_started) signal is similar to the [before_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.before_request)
decorator. The advantage of signals over handlers is that they can be subscribed to
temporarily, and can’t directly affect the application. This is useful for testing,
metrics, auditing, and more. For example, if you want to know what templates were
rendered at what parts of what requests, there is a signal that will notify you of that
information.

## Core Signals

See [Signals](https://flask.palletsprojects.com/en/api/#core-signals-list) for a list of all built-in signals. The [Application Structure and Lifecycle](https://flask.palletsprojects.com/en/lifecycle/)
page also describes the order that signals and decorators execute.

## Subscribing to Signals

To subscribe to a signal, you can use the
`connect()` method of a signal.  The first
argument is the function that should be called when the signal is emitted,
the optional second argument specifies a sender.  To unsubscribe from a
signal, you can use the `disconnect()` method.

For all core Flask signals, the sender is the application that issued the
signal.  When you subscribe to a signal, be sure to also provide a sender
unless you really want to listen for signals from all applications.  This is
especially true if you are developing an extension.

For example, here is a helper context manager that can be used in a unit test
to determine which templates were rendered and what variables were passed
to the template:

```
from flask import template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
```

This can now easily be paired with a test client:

```
with captured_templates(app) as templates:
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == 'index.html'
    assert len(context['items']) == 10
```

Make sure to subscribe with an extra `**extra` argument so that your
calls don’t fail if Flask introduces new arguments to the signals.

All the template rendering in the code issued by the application `app`
in the body of the `with` block will now be recorded in the `templates`
variable.  Whenever a template is rendered, the template object as well as
context are appended to it.

Additionally there is a convenient helper method
(`connected_to()`)  that allows you to
temporarily subscribe a function to a signal with a context manager on
its own.  Because the return value of the context manager cannot be
specified that way, you have to pass the list in as an argument:

```
from flask import template_rendered

def captured_templates(app, recorded, **extra):
    def record(sender, template, context):
        recorded.append((template, context))
    return template_rendered.connected_to(record, app)
```

The example above would then look like this:

```
templates = []
with captured_templates(app, templates, **extra):
    ...
    template, context = templates[0]
```

## Creating Signals

If you want to use signals in your own application, you can use the
blinker library directly.  The most common use case are named signals in a
custom [Namespace](https://blinker.readthedocs.io/en/stable/#blinker.Namespace).  This is what is recommended
most of the time:

```
from blinker import Namespace
my_signals = Namespace()
```

Now you can create new signals like this:

```
model_saved = my_signals.signal('model-saved')
```

The name for the signal here makes it unique and also simplifies
debugging.  You can access the name of the signal with the
`name` attribute.

## Sending Signals

If you want to emit a signal, you can do so by calling the
`send()` method.  It accepts a sender as first
argument and optionally some keyword arguments that are forwarded to the
signal subscribers:

```
class Model(object):
    ...

    def save(self):
        model_saved.send(self)
```

Try to always pick a good sender.  If you have a class that is emitting a
signal, pass `self` as sender.  If you are emitting a signal from a random
function, you can pass `current_app._get_current_object()` as sender.

Passing Proxies as Senders

Never pass [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app) as sender to a signal.  Use
`current_app._get_current_object()` instead.  The reason for this is
that [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app) is a proxy and not the real application
object.

## Signals and Flask’s Request Context

Signals fully support [The Request Context](https://flask.palletsprojects.com/en/reqcontext/) when receiving signals.
Context-local variables are consistently available between
[request_started](https://flask.palletsprojects.com/en/api/#flask.request_started) and [request_finished](https://flask.palletsprojects.com/en/api/#flask.request_finished), so you can
rely on [flask.g](https://flask.palletsprojects.com/en/api/#flask.g) and others as needed.  Note the limitations described
in [Sending Signals](#signals-sending) and the [request_tearing_down](https://flask.palletsprojects.com/en/api/#flask.request_tearing_down) signal.

## Decorator Based Signal Subscriptions

You can also easily subscribe to signals by using the
`connect_via()` decorator:

```
from flask import template_rendered

@template_rendered.connect_via(app)
def when_template_rendered(sender, template, context, **extra):
    print(f'Template {template.name} is rendered with {context}')
```

---

# Templates¶

# Templates

Flask leverages Jinja as its template engine.  You are obviously free to use
a different template engine, but you still have to install Jinja to run
Flask itself.  This requirement is necessary to enable rich extensions.
An extension can depend on Jinja being present.

This section only gives a very quick introduction into how Jinja
is integrated into Flask.  If you want information on the template
engine’s syntax itself, head over to the official [Jinja Template
Documentation](https://jinja.palletsprojects.com/templates/) for
more information.

## Jinja Setup

Unless customized, Jinja is configured by Flask as follows:

- autoescaping is enabled for all templates ending in `.html`,
  `.htm`, `.xml`, `.xhtml`, as well as `.svg` when using
  `render_template()`.
- autoescaping is enabled for all strings when using
  `render_template_string()`.
- a template has the ability to opt in/out autoescaping with the
  `{% autoescape %}` tag.
- Flask inserts a couple of global functions and helpers into the
  Jinja context, additionally to the values that are present by
  default.

## Standard Context

The following global variables are available within Jinja templates
by default:

   config

The current configuration object ([flask.Flask.config](https://flask.palletsprojects.com/en/api/#flask.Flask.config))

  Changelog

Changed in version 0.10: This is now always available, even in imported templates.

Added in version 0.6.

     request

The current request object ([flask.request](https://flask.palletsprojects.com/en/api/#flask.request)).  This variable is
unavailable if the template was rendered without an active request
context.

    session

The current session object ([flask.session](https://flask.palletsprojects.com/en/api/#flask.session)).  This variable
is unavailable if the template was rendered without an active request
context.

    g

The request-bound object for global variables ([flask.g](https://flask.palletsprojects.com/en/api/#flask.g)).  This
variable is unavailable if the template was rendered without an active
request context.

    url_for()

The [flask.url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for) function.

    get_flashed_messages()

The [flask.get_flashed_messages()](https://flask.palletsprojects.com/en/api/#flask.get_flashed_messages) function.

The Jinja Context Behavior

These variables are added to the context of variables, they are not
global variables.  The difference is that by default these will not
show up in the context of imported templates.  This is partially caused
by performance considerations, partially to keep things explicit.

What does this mean for you?  If you have a macro you want to import,
that needs to access the request object you have two possibilities:

1. you explicitly pass the request to the macro as parameter, or
  the attribute of the request object you are interested in.
2. you import the macro “with context”.

Importing with context looks like this:

```
{% from '_helpers.html' import my_macro with context %}
```

## Controlling Autoescaping

Autoescaping is the concept of automatically escaping special characters
for you.  Special characters in the sense of HTML (or XML, and thus XHTML)
are `&`, `>`, `<`, `"` as well as `'`.  Because these characters
carry specific meanings in documents on their own you have to replace them
by so called “entities” if you want to use them for text.  Not doing so
would not only cause user frustration by the inability to use these
characters in text, but can also lead to security problems.  (see
[Cross-Site Scripting (XSS)](https://flask.palletsprojects.com/en/web-security/#security-xss))

Sometimes however you will need to disable autoescaping in templates.
This can be the case if you want to explicitly inject HTML into pages, for
example if they come from a system that generates secure HTML like a
markdown to HTML converter.

There are three ways to accomplish that:

- In the Python code, wrap the HTML string in a `Markup`
  object before passing it to the template.  This is in general the
  recommended way.
- Inside the template, use the `|safe` filter to explicitly mark a
  string as safe HTML (`{{ myvariable|safe }}`)
- Temporarily disable the autoescape system altogether.

To disable the autoescape system in templates, you can use the `{%
autoescape %}` block:

```
{% autoescape false %}
    <p>autoescaping is disabled here
    <p>{{ will_not_be_escaped }}
{% endautoescape %}
```

Whenever you do this, please be very cautious about the variables you are
using in this block.

## Registering Filters

If you want to register your own filters in Jinja you have two ways to do
that.  You can either put them by hand into the
[jinja_env](https://flask.palletsprojects.com/en/api/#flask.Flask.jinja_env) of the application or use the
[template_filter()](https://flask.palletsprojects.com/en/api/#flask.Flask.template_filter) decorator.

The two following examples work the same and both reverse an object:

```
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

def reverse_filter(s):
    return s[::-1]
app.jinja_env.filters['reverse'] = reverse_filter
```

In case of the decorator the argument is optional if you want to use the
function name as name of the filter.  Once registered, you can use the filter
in your templates in the same way as Jinja’s builtin filters, for example if
you have a Python list in context called `mylist`:

```
{% for x in mylist | reverse %}
{% endfor %}
```

## Context Processors

To inject new variables automatically into the context of a template,
context processors exist in Flask.  Context processors run before the
template is rendered and have the ability to inject new values into the
template context.  A context processor is a function that returns a
dictionary.  The keys and values of this dictionary are then merged with
the template context, for all templates in the app:

```
@app.context_processor
def inject_user():
    return dict(user=g.user)
```

The context processor above makes a variable called `user` available in
the template with the value of `g.user`.  This example is not very
interesting because `g` is available in templates anyways, but it gives an
idea how this works.

Variables are not limited to values; a context processor can also make
functions available to templates (since Python allows passing around
functions):

```
@app.context_processor
def utility_processor():
    def format_price(amount, currency="€"):
        return f"{amount:.2f}{currency}"
    return dict(format_price=format_price)
```

The context processor above makes the `format_price` function available to all
templates:

```
{{ format_price(0.33) }}
```

You could also build `format_price` as a template filter (see
[Registering Filters](#registering-filters)), but this demonstrates how to pass functions in a
context processor.

## Streaming

It can be useful to not render the whole template as one complete
string, instead render it as a stream, yielding smaller incremental
strings. This can be used for streaming HTML in chunks to speed up
initial page load, or to save memory when rendering a very large
template.

The Jinja template engine supports rendering a template piece
by piece, returning an iterator of strings. Flask provides the
[stream_template()](https://flask.palletsprojects.com/en/api/#flask.stream_template) and [stream_template_string()](https://flask.palletsprojects.com/en/api/#flask.stream_template_string)
functions to make this easier to use.

```
from flask import stream_template

@app.get("/timeline")
def timeline():
    return stream_template("timeline.html")
```

These functions automatically apply the
[stream_with_context()](https://flask.palletsprojects.com/en/api/#flask.stream_with_context) wrapper if a request is active, so
that it remains available in the template.

---

# Testing Flask Applications¶

# Testing Flask Applications

Flask provides utilities for testing an application. This documentation
goes over techniques for working with different parts of the application
in tests.

We will use the [pytest](https://docs.pytest.org/) framework to set up and run our tests.

```
$ pip install pytest
```

The [tutorial](https://flask.palletsprojects.com/en/tutorial/) goes over how to write tests for
100% coverage of the sample Flaskr blog application. See
[the tutorial on tests](https://flask.palletsprojects.com/en/tutorial/tests/) for a detailed
explanation of specific tests for an application.

## Identifying Tests

Tests are typically located in the `tests` folder. Tests are functions
that start with `test_`, in Python modules that start with `test_`.
Tests can also be further grouped in classes that start with `Test`.

It can be difficult to know what to test. Generally, try to test the
code that you write, not the code of libraries that you use, since they
are already tested. Try to extract complex behaviors as separate
functions to test individually.

## Fixtures

Pytest *fixtures* allow writing pieces of code that are reusable across
tests. A simple fixture returns a value, but a fixture can also do
setup, yield a value, then do teardown. Fixtures for the application,
test client, and CLI runner are shown below, they can be placed in
`tests/conftest.py`.

If you’re using an
[application factory](https://flask.palletsprojects.com/en/patterns/appfactories/), define an `app`
fixture to create and configure an app instance. You can add code before
and after the `yield` to set up and tear down other resources, such as
creating and clearing a database.

If you’re not using a factory, you already have an app object you can
import and configure directly. You can still use an `app` fixture to
set up and tear down resources.

```
import pytest
from my_project import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
```

## Sending Requests with the Test Client

The test client makes requests to the application without running a live
server. Flask’s client extends
[Werkzeug’s client](https://werkzeug.palletsprojects.com/en/stable/test/), see those docs for additional
information.

The `client` has methods that match the common HTTP request methods,
such as `client.get()` and `client.post()`. They take many arguments
for building the request; you can find the full documentation in
[EnvironBuilder](https://werkzeug.palletsprojects.com/en/stable/test/#werkzeug.test.EnvironBuilder). Typically you’ll use `path`,
`query_string`, `headers`, and `data` or `json`.

To make a request, call the method the request should use with the path
to the route to test. A [TestResponse](https://werkzeug.palletsprojects.com/en/stable/test/#werkzeug.test.TestResponse) is returned
to examine the response data. It has all the usual properties of a
response object. You’ll usually look at `response.data`, which is the
bytes returned by the view. If you want to use text, Werkzeug 2.1
provides `response.text`, or use `response.get_data(as_text=True)`.

```
def test_request_example(client):
    response = client.get("/posts")
    assert b"<h2>Hello, World!</h2>" in response.data
```

Pass a dict `query_string={"key": "value", ...}` to set arguments in
the query string (after the `?` in the URL). Pass a dict
`headers={}` to set request headers.

To send a request body in a POST or PUT request, pass a value to
`data`. If raw bytes are passed, that exact body is used. Usually,
you’ll pass a dict to set form data.

### Form Data

To send form data, pass a dict to `data`. The `Content-Type` header
will be set to `multipart/form-data` or
`application/x-www-form-urlencoded` automatically.

If a value is a file object opened for reading bytes (`"rb"` mode), it
will be treated as an uploaded file. To change the detected filename and
content type, pass a `(file, filename, content_type)` tuple. File
objects will be closed after making the request, so they do not need to
use the usual `with open() as f:` pattern.

It can be useful to store files in a `tests/resources` folder, then
use `pathlib.Path` to get files relative to the current test file.

```
from pathlib import Path

# get the resources folder in the tests folder
resources = Path(__file__).parent / "resources"

def test_edit_user(client):
    response = client.post("/user/2/edit", data={
        "name": "Flask",
        "theme": "dark",
        "picture": (resources / "picture.png").open("rb"),
    })
    assert response.status_code == 200
```

### JSON Data

To send JSON data, pass an object to `json`. The `Content-Type`
header will be set to `application/json` automatically.

Similarly, if the response contains JSON data, the `response.json`
attribute will contain the deserialized object.

```
def test_json_data(client):
    response = client.post("/graphql", json={
        "query": """
            query User($id: String!) {
                user(id: $id) {
                    name
                    theme
                    picture_url
                }
            }
        """,
        variables={"id": 2},
    })
    assert response.json["data"]["user"]["name"] == "Flask"
```

## Following Redirects

By default, the client does not make additional requests if the response
is a redirect. By passing `follow_redirects=True` to a request method,
the client will continue to make requests until a non-redirect response
is returned.

[TestResponse.history](https://werkzeug.palletsprojects.com/en/stable/test/#werkzeug.test.TestResponse.history) is
a tuple of the responses that led up to the final response. Each
response has a [request](https://werkzeug.palletsprojects.com/en/stable/test/#werkzeug.test.TestResponse.request) attribute
which records the request that produced that response.

```
def test_logout_redirect(client):
    response = client.get("/logout", follow_redirects=True)
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # Check that the second request was to the index page.
    assert response.request.path == "/index"
```

## Accessing and Modifying the Session

To access Flask’s context variables, mainly
[session](https://flask.palletsprojects.com/en/api/#flask.session), use the client in a `with` statement.
The app and request context will remain active *after* making a request,
until the `with` block ends.

```
from flask import session

def test_access_session(client):
    with client:
        client.post("/auth/login", data={"username": "flask"})
        # session is still accessible
        assert session["user_id"] == 1

    # session is no longer accessible
```

If you want to access or set a value in the session *before* making a
request, use the client’s
[session_transaction()](https://flask.palletsprojects.com/en/api/#flask.testing.FlaskClient.session_transaction) method in a
`with` statement. It returns a session object, and will save the
session once the block ends.

```
from flask import session

def test_modify_session(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session["user_id"] = 1

    # session is saved now

    response = client.get("/users/me")
    assert response.json["username"] == "flask"
```

## Running Commands with the CLI Runner

Flask provides [test_cli_runner()](https://flask.palletsprojects.com/en/api/#flask.Flask.test_cli_runner) to create a
[FlaskCliRunner](https://flask.palletsprojects.com/en/api/#flask.testing.FlaskCliRunner), which runs CLI commands in
isolation and captures the output in a [Result](https://click.palletsprojects.com/en/stable/api/#click.testing.Result)
object. Flask’s runner extends [Click’s runner](https://click.palletsprojects.com/en/stable/testing/),
see those docs for additional information.

Use the runner’s [invoke()](https://flask.palletsprojects.com/en/api/#flask.testing.FlaskCliRunner.invoke) method to
call commands in the same way they would be called with the `flask`
command from the command line.

```
import click

@app.cli.command("hello")
@click.option("--name", default="World")
def hello_command(name):
    click.echo(f"Hello, {name}!")

def test_hello_command(runner):
    result = runner.invoke(args="hello")
    assert "World" in result.output

    result = runner.invoke(args=["hello", "--name", "Flask"])
    assert "Flask" in result.output
```

## Tests that depend on an Active Context

You may have functions that are called from views or commands, that
expect an active [application context](https://flask.palletsprojects.com/en/appcontext/) or
[request context](https://flask.palletsprojects.com/en/reqcontext/) because they access `request`,
`session`, or `current_app`. Rather than testing them by making a
request or invoking the command, you can create and activate a context
directly.

Use `with app.app_context()` to push an application context. For
example, database extensions usually require an active app context to
make queries.

```
def test_db_post_model(app):
    with app.app_context():
        post = db.session.query(Post).get(1)
```

Use `with app.test_request_context()` to push a request context. It
takes the same arguments as the test client’s request methods.

```
def test_validate_user_edit(app):
    with app.test_request_context(
        "/user/2/edit", method="POST", data={"name": ""}
    ):
        # call a function that accesses `request`
        messages = validate_edit_user()

    assert messages["name"][0] == "Name cannot be empty."
```

Creating a test request context doesn’t run any of the Flask dispatching
code, so `before_request` functions are not called. If you need to
call these, usually it’s better to make a full request instead. However,
it’s possible to call them manually.

```
def test_auth_token(app):
    with app.test_request_context("/user/2/edit", headers={"X-Auth-Token": "1"}):
        app.preprocess_request()
        assert g.user.name == "Flask"
```

---

# Tutorial¶

# Tutorial

- [Project Layout](https://flask.palletsprojects.com/en/stable/layout/)
- [Application Setup](https://flask.palletsprojects.com/en/stable/factory/)
- [Define and Access the Database](https://flask.palletsprojects.com/en/stable/database/)
- [Blueprints and Views](https://flask.palletsprojects.com/en/stable/views/)
- [Templates](https://flask.palletsprojects.com/en/stable/templates/)
- [Static Files](https://flask.palletsprojects.com/en/stable/static/)
- [Blog Blueprint](https://flask.palletsprojects.com/en/stable/blog/)
- [Make the Project Installable](https://flask.palletsprojects.com/en/stable/install/)
- [Test Coverage](https://flask.palletsprojects.com/en/stable/tests/)
- [Deploy to Production](https://flask.palletsprojects.com/en/stable/deploy/)
- [Keep Developing!](https://flask.palletsprojects.com/en/stable/next/)

This tutorial will walk you through creating a basic blog application
called Flaskr. Users will be able to register, log in, create posts,
and edit or delete their own posts. You will be able to package and
install the application on other computers.

 ![screenshot of index page](https://flask.palletsprojects.com/en/_images/flaskr_index.png)

It’s assumed that you’re already familiar with Python. The [official
tutorial](https://docs.python.org/3/tutorial/) in the Python docs is a great way to learn or review first.

While it’s designed to give a good starting point, the tutorial doesn’t
cover all of Flask’s features. Check out the [Quickstart](https://flask.palletsprojects.com/en/quickstart/) for an
overview of what Flask can do, then dive into the docs to find out more.
The tutorial only uses what’s provided by Flask and Python. In another
project, you might decide to use [Extensions](https://flask.palletsprojects.com/en/extensions/) or other libraries
to make some tasks simpler.

 ![screenshot of login page](https://flask.palletsprojects.com/en/_images/flaskr_login.png)

Flask is flexible. It doesn’t require you to use any particular project
or code layout. However, when first starting, it’s helpful to use a more
structured approach. This means that the tutorial will require a bit of
boilerplate up front, but it’s done to avoid many common pitfalls that
new developers encounter, and it creates a project that’s easy to expand
on. Once you become more comfortable with Flask, you can step out of
this structure and take full advantage of Flask’s flexibility.

 ![screenshot of edit page](https://flask.palletsprojects.com/en/_images/flaskr_edit.png)

[The tutorial project is available as an example in the Flask
repository](https://github.com/pallets/flask/tree/3.1.2/examples/tutorial), if you want to compare your project
with the final product as you follow the tutorial.

Continue to [Project Layout](https://flask.palletsprojects.com/en/stable/layout/).
