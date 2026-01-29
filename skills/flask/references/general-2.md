# The Application Context¶ and more

# The Application Context¶

# The Application Context

The application context keeps track of the application-level data during
a request, CLI command, or other activity. Rather than passing the
application around to each function, the [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app) and
[g](https://flask.palletsprojects.com/en/api/#flask.g) proxies are accessed instead.

This is similar to [The Request Context](https://flask.palletsprojects.com/en/reqcontext/), which keeps track of
request-level data during a request. A corresponding application context
is pushed when a request context is pushed.

## Purpose of the Context

The [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) application object has attributes, such as
[config](https://flask.palletsprojects.com/en/api/#flask.Flask.config), that are useful to access within views and
[CLI commands](https://flask.palletsprojects.com/en/cli/). However, importing the `app` instance
within the modules in your project is prone to circular import issues.
When using the [app factory pattern](https://flask.palletsprojects.com/en/patterns/appfactories/) or
writing reusable [blueprints](https://flask.palletsprojects.com/en/blueprints/) or
[extensions](https://flask.palletsprojects.com/en/extensions/) there won’t be an `app` instance to
import at all.

Flask solves this issue with the *application context*. Rather than
referring to an `app` directly, you use the [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app)
proxy, which points to the application handling the current activity.

Flask automatically *pushes* an application context when handling a
request. View functions, error handlers, and other functions that run
during a request will have access to [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app).

Flask will also automatically push an app context when running CLI
commands registered with [Flask.cli](https://flask.palletsprojects.com/en/api/#flask.Flask.cli) using `@app.cli.command()`.

## Lifetime of the Context

The application context is created and destroyed as necessary. When a
Flask application begins handling a request, it pushes an application
context and a [request context](https://flask.palletsprojects.com/en/reqcontext/). When the request
ends it pops the request context then the application context.
Typically, an application context will have the same lifetime as a
request.

See [The Request Context](https://flask.palletsprojects.com/en/reqcontext/) for more information about how the contexts work
and the full life cycle of a request.

## Manually Push a Context

If you try to access [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app), or anything that uses it,
outside an application context, you’ll get this error message:

```
RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that
needed to interface with the current application object in some way.
To solve this, set up an application context with app.app_context().
```

If you see that error while configuring your application, such as when
initializing an extension, you can push a context manually since you
have direct access to the `app`. Use [app_context()](https://flask.palletsprojects.com/en/api/#flask.Flask.app_context) in a
`with` block, and everything that runs in the block will have access
to [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app).

```
def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app
```

If you see that error somewhere else in your code not related to
configuring the application, it most likely indicates that you should
move that code into a view function or CLI command.

## Storing Data

The application context is a good place to store common data during a
request or CLI command. Flask provides the [gobject](https://flask.palletsprojects.com/en/api/#flask.g) for this
purpose. It is a simple namespace object that has the same lifetime as
an application context.

Note

The `g` name stands for “global”, but that is referring to the
data being global *within a context*. The data on `g` is lost
after the context ends, and it is not an appropriate place to store
data between requests. Use the [session](https://flask.palletsprojects.com/en/api/#flask.session) or a database to
store data across requests.

A common use for [g](https://flask.palletsprojects.com/en/api/#flask.g) is to manage resources during a request.

1. `get_X()` creates resource `X` if it does not exist, caching it
  as `g.X`.
2. `teardown_X()` closes or otherwise deallocates the resource if it
  exists. It is registered as a [teardown_appcontext()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_appcontext)
  handler.

For example, you can manage a database connection using this pattern:

```
from flask import g

def get_db():
    if 'db' not in g:
        g.db = connect_to_database()

    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()
```

During a request, every call to `get_db()` will return the same
connection, and it will be closed automatically at the end of the
request.

You can use [LocalProxy](https://werkzeug.palletsprojects.com/en/stable/local/#werkzeug.local.LocalProxy) to make a new context
local from `get_db()`:

```
from werkzeug.local import LocalProxy
db = LocalProxy(get_db)
```

Accessing `db` will call `get_db` internally, in the same way that
[current_app](https://flask.palletsprojects.com/en/api/#flask.current_app) works.

## Events and Signals

The application will call functions registered with [teardown_appcontext()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_appcontext)
when the application context is popped.

The following signals are sent: [appcontext_pushed](https://flask.palletsprojects.com/en/api/#flask.appcontext_pushed),
[appcontext_tearing_down](https://flask.palletsprojects.com/en/api/#flask.appcontext_tearing_down), and [appcontext_popped](https://flask.palletsprojects.com/en/api/#flask.appcontext_popped).

---

# Usingasyncandawait¶

# Usingasyncandawait

  Changelog

Added in version 2.0.

Routes, error handlers, before request, after request, and teardown
functions can all be coroutine functions if Flask is installed with the
`async` extra (`pip install flask[async]`). This allows views to be
defined with `async def` and use `await`.

```
@app.route("/get-data")
async def get_data():
    data = await async_db_query(...)
    return jsonify(data)
```

Pluggable class-based views also support handlers that are implemented as
coroutines. This applies to the [dispatch_request()](https://flask.palletsprojects.com/en/api/#flask.views.View.dispatch_request)
method in views that inherit from the [flask.views.View](https://flask.palletsprojects.com/en/api/#flask.views.View) class, as
well as all the HTTP method handlers in views that inherit from the
[flask.views.MethodView](https://flask.palletsprojects.com/en/api/#flask.views.MethodView) class.

## Performance

Async functions require an event loop to run. Flask, as a WSGI
application, uses one worker to handle one request/response cycle.
When a request comes in to an async view, Flask will start an event loop
in a thread, run the view function there, then return the result.

Each request still ties up one worker, even for async views. The upside
is that you can run async code within a view, for example to make
multiple concurrent database queries, HTTP requests to an external API,
etc. However, the number of requests your application can handle at one
time will remain the same.

**Async is not inherently faster than sync code.** Async is beneficial
when performing concurrent IO-bound tasks, but will probably not improve
CPU-bound tasks. Traditional Flask views will still be appropriate for
most use cases, but Flask’s async support enables writing and using
code that wasn’t possible natively before.

## Background tasks

Async functions will run in an event loop until they complete, at
which stage the event loop will stop. This means any additional
spawned tasks that haven’t completed when the async function completes
will be cancelled. Therefore you cannot spawn background tasks, for
example via `asyncio.create_task`.

If you wish to use background tasks it is best to use a task queue to
trigger background work, rather than spawn tasks in a view
function. With that in mind you can spawn asyncio tasks by serving
Flask with an ASGI server and utilising the asgiref WsgiToAsgi adapter
as described in [ASGI](https://flask.palletsprojects.com/en/deploying/asgi/). This works as the adapter creates
an event loop that runs continually.

## When to use Quart instead

Flask’s async support is less performant than async-first frameworks due
to the way it is implemented. If you have a mainly async codebase it
would make sense to consider [Quart](https://quart.palletsprojects.com). Quart is a reimplementation of
Flask based on the [ASGI](https://asgi.readthedocs.io) standard instead of WSGI. This allows it to
handle many concurrent requests, long running requests, and websockets
without requiring multiple worker processes or threads.

It has also already been possible to [run Flask with Gevent](https://flask.palletsprojects.com/en/gevent/) to
get many of the benefits of async request handling. Gevent patches low-level
Python functions to accomplish this, whereas `async`/`await` and ASGI use
standard, modern Python capabilities. Deciding whether you should use gevent
with Flask, or Quart, or something else is ultimately up to understanding the
specific needs of your project.

## Extensions

Flask extensions predating Flask’s async support do not expect async views.
If they provide decorators to add functionality to views, those will probably
not work with async views because they will not await the function or be
awaitable. Other functions they provide will not be awaitable either and
will probably be blocking if called within an async view.

Extension authors can support async functions by utilising the
[flask.Flask.ensure_sync()](https://flask.palletsprojects.com/en/api/#flask.Flask.ensure_sync) method. For example, if the extension
provides a view function decorator add `ensure_sync` before calling
the decorated function,

```
def extension(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...  # Extension logic
        return current_app.ensure_sync(func)(*args, **kwargs)

    return wrapper
```

Check the changelog of the extension you want to use to see if they’ve
implemented async support, or make a feature request or PR to them.

## Other event loops

At the moment Flask only supports [asyncio](https://docs.python.org/3/library/asyncio.html#module-asyncio). It’s possible to override
[flask.Flask.ensure_sync()](https://flask.palletsprojects.com/en/api/#flask.Flask.ensure_sync) to change how async functions are wrapped to use
a different library. See [Combining with async/await](https://flask.palletsprojects.com/en/gevent/#gevent-asyncio) for an example.

---

# Modular Applications with Blueprints¶

# Modular Applications with Blueprints

  Changelog

Added in version 0.7.

Flask uses a concept of *blueprints* for making application components and
supporting common patterns within an application or across applications.
Blueprints can greatly simplify how large applications work and provide a
central means for Flask extensions to register operations on applications.
A [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint) object works similarly to a [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask)
application object, but it is not actually an application.  Rather it is a
*blueprint* of how to construct or extend an application.

## Why Blueprints?

Blueprints in Flask are intended for these cases:

- Factor an application into a set of blueprints.  This is ideal for
  larger applications; a project could instantiate an application object,
  initialize several extensions, and register a collection of blueprints.
- Register a blueprint on an application at a URL prefix and/or subdomain.
  Parameters in the URL prefix/subdomain become common view arguments
  (with defaults) across all view functions in the blueprint.
- Register a blueprint multiple times on an application with different URL
  rules.
- Provide template filters, static files, templates, and other utilities
  through blueprints.  A blueprint does not have to implement applications
  or view functions.
- Register a blueprint on an application for any of these cases when
  initializing a Flask extension.

A blueprint in Flask is not a pluggable app because it is not actually an
application – it’s a set of operations which can be registered on an
application, even multiple times.  Why not have multiple application
objects?  You can do that (see [Application Dispatching](https://flask.palletsprojects.com/en/patterns/appdispatch/)), but your
applications will have separate configs and will be managed at the WSGI
layer.

Blueprints instead provide separation at the Flask level, share
application config, and can change an application object as necessary with
being registered. The downside is that you cannot unregister a blueprint
once an application was created without having to destroy the whole
application object.

## The Concept of Blueprints

The basic concept of blueprints is that they record operations to execute
when registered on an application.  Flask associates view functions with
blueprints when dispatching requests and generating URLs from one endpoint
to another.

## My First Blueprint

This is what a very basic blueprint looks like.  In this case we want to
implement a blueprint that does simple rendering of static templates:

```
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)
```

When you bind a function with the help of the `@simple_page.route`
decorator, the blueprint will record the intention of registering the
function `show` on the application when it’s later registered.
Additionally it will prefix the endpoint of the function with the
name of the blueprint which was given to the [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint)
constructor (in this case also `simple_page`). The blueprint’s name
does not modify the URL, only the endpoint.

## Registering Blueprints

So how do you register that blueprint?  Like this:

```
from flask import Flask
from yourapplication.simple_page import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)
```

If you check the rules registered on the application, you will find
these:

```
>>> app.url_map
Map([<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
 <Rule '/<page>' (HEAD, OPTIONS, GET) -> simple_page.show>,
 <Rule '/' (HEAD, OPTIONS, GET) -> simple_page.show>])
```

The first one is obviously from the application itself for the static
files.  The other two are for the `show` function of the `simple_page`
blueprint.  As you can see, they are also prefixed with the name of the
blueprint and separated by a dot (`.`).

Blueprints however can also be mounted at different locations:

```
app.register_blueprint(simple_page, url_prefix='/pages')
```

And sure enough, these are the generated rules:

```
>>> app.url_map
Map([<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
 <Rule '/pages/<page>' (HEAD, OPTIONS, GET) -> simple_page.show>,
 <Rule '/pages/' (HEAD, OPTIONS, GET) -> simple_page.show>])
```

On top of that you can register blueprints multiple times though not every
blueprint might respond properly to that.  In fact it depends on how the
blueprint is implemented if it can be mounted more than once.

## Nesting Blueprints

It is possible to register a blueprint on another blueprint.

```
parent = Blueprint('parent', __name__, url_prefix='/parent')
child = Blueprint('child', __name__, url_prefix='/child')
parent.register_blueprint(child)
app.register_blueprint(parent)
```

The child blueprint will gain the parent’s name as a prefix to its
name, and child URLs will be prefixed with the parent’s URL prefix.

```
url_for('parent.child.create')
/parent/child/create
```

In addition a child blueprint’s will gain their parent’s subdomain,
with their subdomain as prefix if present i.e.

```
parent = Blueprint('parent', __name__, subdomain='parent')
child = Blueprint('child', __name__, subdomain='child')
parent.register_blueprint(child)
app.register_blueprint(parent)

url_for('parent.child.create', _external=True)
"child.parent.domain.tld"
```

Blueprint-specific before request functions, etc. registered with the
parent will trigger for the child. If a child does not have an error
handler that can handle a given exception, the parent’s will be tried.

## Blueprint Resources

Blueprints can provide resources as well.  Sometimes you might want to
introduce a blueprint only for the resources it provides.

### Blueprint Resource Folder

Like for regular applications, blueprints are considered to be contained
in a folder.  While multiple blueprints can originate from the same folder,
it does not have to be the case and it’s usually not recommended.

The folder is inferred from the second argument to [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint) which
is usually `__name__`.  This argument specifies what logical Python
module or package corresponds to the blueprint.  If it points to an actual
Python package that package (which is a folder on the filesystem) is the
resource folder.  If it’s a module, the package the module is contained in
will be the resource folder.  You can access the
[Blueprint.root_path](https://flask.palletsprojects.com/en/api/#flask.Blueprint.root_path) property to see what the resource folder is:

```
>>> simple_page.root_path
'/Users/username/TestProject/yourapplication'
```

To quickly open sources from this folder you can use the
[open_resource()](https://flask.palletsprojects.com/en/api/#flask.Blueprint.open_resource) function:

```
with simple_page.open_resource('static/style.css') as f:
    code = f.read()
```

### Static Files

A blueprint can expose a folder with static files by providing the path
to the folder on the filesystem with the `static_folder` argument.
It is either an absolute path or relative to the blueprint’s location:

```
admin = Blueprint('admin', __name__, static_folder='static')
```

By default the rightmost part of the path is where it is exposed on the
web. This can be changed with the `static_url_path` argument. Because the
folder is called `static` here it will be available at the
`url_prefix` of the blueprint + `/static`. If the blueprint
has the prefix `/admin`, the static URL will be `/admin/static`.

The endpoint is named `blueprint_name.static`. You can generate URLs
to it with [url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for) like you would with the static folder of the
application:

```
url_for('admin.static', filename='style.css')
```

However, if the blueprint does not have a `url_prefix`, it is not
possible to access the blueprint’s static folder. This is because the
URL would be `/static` in this case, and the application’s `/static`
route takes precedence. Unlike template folders, blueprint static
folders are not searched if the file does not exist in the application
static folder.

### Templates

If you want the blueprint to expose templates you can do that by providing
the `template_folder` parameter to the [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint) constructor:

```
admin = Blueprint('admin', __name__, template_folder='templates')
```

For static files, the path can be absolute or relative to the blueprint
resource folder.

The template folder is added to the search path of templates but with a lower
priority than the actual application’s template folder. That way you can
easily override templates that a blueprint provides in the actual application.
This also means that if you don’t want a blueprint template to be accidentally
overridden, make sure that no other blueprint or actual application template
has the same relative path. When multiple blueprints provide the same relative
template path the first blueprint registered takes precedence over the others.

So if you have a blueprint in the folder `yourapplication/admin` and you
want to render the template `'admin/index.html'` and you have provided
`templates` as a `template_folder` you will have to create a file like
this: `yourapplication/admin/templates/admin/index.html`. The reason
for the extra `admin` folder is to avoid getting our template overridden
by a template named `index.html` in the actual application template
folder.

To further reiterate this: if you have a blueprint named `admin` and you
want to render a template called `index.html` which is specific to this
blueprint, the best idea is to lay out your templates like this:

```
yourpackage/
    blueprints/
        admin/
            templates/
                admin/
                    index.html
            __init__.py
```

And then when you want to render the template, use `admin/index.html` as
the name to look up the template by.  If you encounter problems loading
the correct templates enable the `EXPLAIN_TEMPLATE_LOADING` config
variable which will instruct Flask to print out the steps it goes through
to locate templates on every `render_template` call.

## Building URLs

If you want to link from one page to another you can use the
[url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for) function just like you normally would do just that you
prefix the URL endpoint with the name of the blueprint and a dot (`.`):

```
url_for('admin.index')
```

Additionally if you are in a view function of a blueprint or a rendered
template and you want to link to another endpoint of the same blueprint,
you can use relative redirects by prefixing the endpoint with a dot only:

```
url_for('.index')
```

This will link to `admin.index` for instance in case the current request
was dispatched to any other admin blueprint endpoint.

## Blueprint Error Handlers

Blueprints support the `errorhandler` decorator just like the [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask)
application object, so it is easy to make Blueprint-specific custom error
pages.

Here is an example for a “404 Page Not Found” exception:

```
@simple_page.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html')
```

Most errorhandlers will simply work as expected; however, there is a caveat
concerning handlers for 404 and 405 exceptions.  These errorhandlers are only
invoked from an appropriate `raise` statement or a call to `abort` in another
of the blueprint’s view functions; they are not invoked by, e.g., an invalid URL
access.  This is because the blueprint does not “own” a certain URL space, so
the application instance has no way of knowing which blueprint error handler it
should run if given an invalid URL.  If you would like to execute different
handling strategies for these errors based on URL prefixes, they may be defined
at the application level using the `request` proxy object:

```
@app.errorhandler(404)
@app.errorhandler(405)
def _handle_api_error(ex):
    if request.path.startswith('/api/'):
        return jsonify(error=str(ex)), ex.code
    else:
        return ex
```

See [Handling Application Errors](https://flask.palletsprojects.com/en/errorhandling/).
