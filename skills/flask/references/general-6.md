# Flask Extension Development¶ and more

# Flask Extension Development¶

# Flask Extension Development

Extensions are extra packages that add functionality to a Flask
application. While [PyPI](https://pypi.org/search/?c=Framework+%3A%3A+Flask) contains many Flask extensions, you may not
find one that fits your need. If this is the case, you can create your
own, and publish it for others to use as well.

This guide will show how to create a Flask extension, and some of the
common patterns and requirements involved. Since extensions can do
anything, this guide won’t be able to cover every possibility.

The best ways to learn about extensions are to look at how other
extensions you use are written, and discuss with others. Discuss your
design ideas with others on our [Discord Chat](https://discord.gg/pallets) or
[GitHub Discussions](https://github.com/pallets/flask/discussions).

The best extensions share common patterns, so that anyone familiar with
using one extension won’t feel completely lost with another. This can
only work if collaboration happens early.

## Naming

A Flask extension typically has `flask` in its name as a prefix or
suffix. If it wraps another library, it should include the library name
as well. This makes it easy to search for extensions, and makes their
purpose clearer.

A general Python packaging recommendation is that the install name from
the package index and the name used in `import` statements should be
related. The import name is lowercase, with words separated by
underscores (`_`). The install name is either lower case or title
case, with words separated by dashes (`-`). If it wraps another
library, prefer using the same case as that library’s name.

Here are some example install and import names:

- `Flask-Name` imported as `flask_name`
- `flask-name-lower` imported as `flask_name_lower`
- `Flask-ComboName` imported as `flask_comboname`
- `Name-Flask` imported as `name_flask`

## The Extension Class and Initialization

All extensions will need some entry point that initializes the
extension with the application. The most common pattern is to create a
class that represents the extension’s configuration and behavior, with
an `init_app` method to apply the extension instance to the given
application instance.

```
class HelloExtension:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(...)
```

It is important that the app is not stored on the extension, don’t do
`self.app = app`. The only time the extension should have direct
access to an app is during `init_app`, otherwise it should use
[current_app](https://flask.palletsprojects.com/en/api/#flask.current_app).

This allows the extension to support the application factory pattern,
avoids circular import issues when importing the extension instance
elsewhere in a user’s code, and makes testing with different
configurations easier.

```
hello = HelloExtension()

def create_app():
    app = Flask(__name__)
    hello.init_app(app)
    return app
```

Above, the `hello` extension instance exists independently of the
application. This means that other modules in a user’s project can do
`from project import hello` and use the extension in blueprints before
the app exists.

The [Flask.extensions](https://flask.palletsprojects.com/en/api/#flask.Flask.extensions) dict can be used to store a reference to
the extension on the application, or some other state specific to the
application. Be aware that this is a single namespace, so use a name
unique to your extension, such as the extension’s name without the
“flask” prefix.

## Adding Behavior

There are many ways that an extension can add behavior. Any setup
methods that are available on the [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) object can be used
during an extension’s `init_app` method.

A common pattern is to use [before_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.before_request) to initialize
some data or a connection at the beginning of each request, then
[teardown_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_request) to clean it up at the end. This can be
stored on [g](https://flask.palletsprojects.com/en/api/#flask.g), discussed more below.

A more lazy approach is to provide a method that initializes and caches
the data or connection. For example, a `ext.get_db` method could
create a database connection the first time it’s called, so that a view
that doesn’t use the database doesn’t create a connection.

Besides doing something before and after every view, your extension
might want to add some specific views as well. In this case, you could
define a [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint), then call [register_blueprint()](https://flask.palletsprojects.com/en/api/#flask.Flask.register_blueprint)
during `init_app` to add the blueprint to the app.

## Configuration Techniques

There can be multiple levels and sources of configuration for an
extension. You should consider what parts of your extension fall into
each one.

- Configuration per application instance, through `app.config`
  values. This is configuration that could reasonably change for each
  deployment of an application. A common example is a URL to an
  external resource, such as a database. Configuration keys should
  start with the extension’s name so that they don’t interfere with
  other extensions.
- Configuration per extension instance, through `__init__`
  arguments. This configuration usually affects how the extension
  is used, such that it wouldn’t make sense to change it per
  deployment.
- Configuration per extension instance, through instance attributes
  and decorator methods. It might be more ergonomic to assign to
  `ext.value`, or use a `@ext.register` decorator to register a
  function, after the extension instance has been created.
- Global configuration through class attributes. Changing a class
  attribute like `Ext.connection_class` can customize default
  behavior without making a subclass. This could be combined
  per-extension configuration to override defaults.
- Subclassing and overriding methods and attributes. Making the API of
  the extension itself something that can be overridden provides a
  very powerful tool for advanced customization.

The [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) object itself uses all of these techniques.

It’s up to you to decide what configuration is appropriate for your
extension, based on what you need and what you want to support.

Configuration should not be changed after the application setup phase is
complete and the server begins handling requests. Configuration is
global, any changes to it are not guaranteed to be visible to other
workers.

## Data During a Request

When writing a Flask application, the [g](https://flask.palletsprojects.com/en/api/#flask.g) object is used to
store information during a request. For example the
[tutorial](https://flask.palletsprojects.com/en/tutorial/database/) stores a connection to a SQLite
database as `g.db`. Extensions can also use this, with some care.
Since `g` is a single global namespace, extensions must use unique
names that won’t collide with user data. For example, use the extension
name as a prefix, or as a namespace.

```
# an internal prefix with the extension name
g._hello_user_id = 2

# or an internal prefix as a namespace
from types import SimpleNamespace
g._hello = SimpleNamespace()
g._hello.user_id = 2
```

The data in `g` lasts for an application context. An application
context is active when a request context is, or when a CLI command is
run. If you’re storing something that should be closed, use
[teardown_appcontext()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_appcontext) to ensure that it gets closed
when the application context ends. If it should only be valid during a
request, or would not be used in the CLI outside a request, use
[teardown_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_request).

## Views and Models

Your extension views might want to interact with specific models in your
database, or some other extension or data connected to your application.
For example, let’s consider a `Flask-SimpleBlog` extension that works
with Flask-SQLAlchemy to provide a `Post` model and views to write
and read posts.

The `Post` model needs to subclass the Flask-SQLAlchemy `db.Model`
object, but that’s only available once you’ve created an instance of
that extension, not when your extension is defining its views. So how
can the view code, defined before the model exists, access the model?

One method could be to use [Class-based Views](https://flask.palletsprojects.com/en/views/). During `__init__`, create
the model, then create the views by passing the model to the view
class’s [as_view()](https://flask.palletsprojects.com/en/api/#flask.views.View.as_view) method.

```
class PostAPI(MethodView):
    def __init__(self, model):
        self.model = model

    def get(self, id):
        post = self.model.query.get(id)
        return jsonify(post.to_json())

class BlogExtension:
    def __init__(self, db):
        class Post(db.Model):
            id = db.Column(primary_key=True)
            title = db.Column(db.String, nullable=False)

        self.post_model = Post

    def init_app(self, app):
        api_view = PostAPI.as_view(model=self.post_model)

db = SQLAlchemy()
blog = BlogExtension(db)
db.init_app(app)
blog.init_app(app)
```

Another technique could be to use an attribute on the extension, such as
`self.post_model` from above. Add the extension to `app.extensions`
in `init_app`, then access
`current_app.extensions["simple_blog"].post_model` from views.

You may also want to provide base classes so that users can provide
their own `Post` model that conforms to the API your extension
expects. So they could implement `class Post(blog.BasePost)`, then
set it as `blog.post_model`.

As you can see, this can get a bit complex. Unfortunately, there’s no
perfect solution here, only different strategies and tradeoffs depending
on your needs and how much customization you want to offer. Luckily,
this sort of resource dependency is not a common need for most
extensions. Remember, if you need help with design, ask on our
[Discord Chat](https://discord.gg/pallets) or [GitHub Discussions](https://github.com/pallets/flask/discussions).

## Recommended Extension Guidelines

Flask previously had the concept of “approved extensions”, where the
Flask maintainers evaluated the quality, support, and compatibility of
the extensions before listing them. While the list became too difficult
to maintain over time, the guidelines are still relevant to all
extensions maintained and developed today, as they help the Flask
ecosystem remain consistent and compatible.

1. An extension requires a maintainer. In the event an extension author
  would like to move beyond the project, the project should find a new
  maintainer and transfer access to the repository, documentation,
  PyPI, and any other services. The [Pallets-Eco](https://github.com/pallets-eco) organization on
  GitHub allows for community maintenance with oversight from the
  Pallets maintainers.
2. The naming scheme is *Flask-ExtensionName* or *ExtensionName-Flask*.
  It must provide exactly one package or module named
  `flask_extension_name`.
3. The extension must use an open source license. The Python web
  ecosystem tends to prefer BSD or MIT. It must be open source and
  publicly available.
4. The extension’s API must have the following characteristics:
  - It must support multiple applications running in the same Python
    process. Use `current_app` instead of `self.app`, store
    configuration and state per application instance.
  - It must be possible to use the factory pattern for creating
    applications. Use the `ext.init_app()` pattern.
5. From a clone of the repository, an extension with its dependencies
  must be installable in editable mode with `pip install -e .`.
6. It must ship tests that can be invoked with a common tool like
  `tox -e py`, `nox -s test` or `pytest`. If not using `tox`,
  the test dependencies should be specified in a requirements file.
  The tests must be part of the sdist distribution.
7. A link to the documentation or project website must be in the PyPI
  metadata or the readme. The documentation should use the Flask theme
  from the [Official Pallets Themes](https://pypi.org/project/Pallets-Sphinx-Themes/).
8. The extension’s dependencies should not use upper bounds or assume
  any particular version scheme, but should use lower bounds to
  indicate minimum compatibility support. For example,
  `sqlalchemy>=1.4`.
9. Indicate the versions of Python supported using `python_requires=">=version"`.
  Flask itself supports Python >=3.9 as of October 2024, and this will update
  over time.

---

# Extensions¶

# Extensions

Extensions are extra packages that add functionality to a Flask
application. For example, an extension might add support for sending
email or connecting to a database. Some extensions add entire new
frameworks to help build certain types of applications, like a REST API.

## Finding Extensions

Flask extensions are usually named “Flask-Foo” or “Foo-Flask”. You can
search PyPI for packages tagged with [Framework :: Flask](https://pypi.org/search/?c=Framework+%3A%3A+Flask).

## Using Extensions

Consult each extension’s documentation for installation, configuration,
and usage instructions. Generally, extensions pull their own
configuration from [app.config](https://flask.palletsprojects.com/en/api/#flask.Flask.config) and are
passed an application instance during initialization. For example,
an extension called “Flask-Foo” might be used like this:

```
from flask_foo import Foo

foo = Foo()

app = Flask(__name__)
app.config.update(
    FOO_BAR='baz',
    FOO_SPAM='eggs',
)

foo.init_app(app)
```

## Building Extensions

While [PyPI](https://pypi.org/search/?c=Framework+%3A%3A+Flask) contains many Flask extensions, you may not find
an extension that fits your need. If this is the case, you can create
your own, and publish it for others to use as well. Read
[Flask Extension Development](https://flask.palletsprojects.com/en/extensiondev/) to develop your own Flask extension.

---

# Async with Gevent¶

# Async with Gevent

[Gevent](https://www.gevent.org) patches Python’s standard library to run within special async workers
called [greenlets](https://greenlet.readthedocs.io). Gevent has existed since long before Python’s native
asyncio was available, and Flask has always worked with it.

Gevent is a reliable way to handle numerous, long lived, concurrent connections,
and to achieve similar capabilities to ASGI and asyncio. This works without
needing to write `async def` or `await` anywhere, but relies on gevent and
greenlet’s low level manipulation of the Python interpreter.

Deciding whether you should use gevent with Flask, or [Quart](https://quart.palletsprojects.com), or something
else, is ultimately up to understanding the specific needs of your project.

## Enabling gevent

You need to apply gevent’s patching as early as possible in your code. This
enables gevent’s underlying event loop and converts many Python internals to run
inside it. Add the following at the top of your project’s module or top
`__init__.py`:

```
import gevent.monkey
gevent.monkey.patch_all()
```

When deploying in production, use [Gunicorn](https://flask.palletsprojects.com/en/deploying/gunicorn/) or
[uWSGI](https://flask.palletsprojects.com/en/deploying/uwsgi/) with a gevent worker, as described on those pages.

To run concurrent tasks within your own code, such as views, use
[gevent.spawn()](https://www.gevent.org/api/gevent.html#gevent.spawn):

```
@app.post("/send")
def send_email():
    gevent.spawn(email.send, to="example@example.example", text="example")
    return "Email is being sent."
```

If you need to access `request` or other Flask context globals within the
spawned function, decorate the function with [stream_with_context()](https://flask.palletsprojects.com/en/api/#flask.stream_with_context) or
[copy_current_request_context()](https://flask.palletsprojects.com/en/api/#flask.copy_current_request_context). Prefer passing the exact data you need
when spawning the function, rather than using the decorators.

Note

When using gevent, greenlet>=1.0 is required. When using PyPy, PyPy>=7.3.7
is required.

## Combining withasync/await

Gevent’s patching does not interact well with Flask’s built-in asyncio support.
If you want to use Gevent and asyncio in the same app, you’ll need to override
[flask.Flask.async_to_sync()](https://flask.palletsprojects.com/en/api/#flask.Flask.async_to_sync) to run async functions inside gevent.

```
import gevent.monkey
gevent.monkey.patch_all()

import asyncio
from flask import Flask, request

loop = asyncio.EventLoop()
gevent.spawn(loop.run_forever)

class GeventFlask(Flask):
    def async_to_sync(self, func):
        def run(*args, **kwargs):
            coro = func(*args, **kwargs)
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            return future.result()

        return run

app = GeventFlask(__name__)

@app.get("/")
async def greet():
    await asyncio.sleep(1)
    return f"Hello, {request.args.get("name", "World")}!"
```

This starts an asyncio event loop in a gevent worker. Async functions are
scheduled on that event loop. This may still have limitations, and may need to
be modified further when using other asyncio implementations.

### libuv

[libuv](https://libuv.org/) is another event loop implementation that [gevent supports](https://www.gevent.org/loop_impls.html). There’s
also a project called [uvloop](https://uvloop.readthedocs.io/) that enables libuv in asyncio. If you want to
use libuv, use gevent’s support, not uvloop. It may be possible to further
modify the `async_to_sync` code from the previous section to work with uvloop,
but that’s not currently known.

To enable gevent’s libuv support, add the following at the *very* top of your
code, before `gevent.monkey.patch_all()`:

```
import gevent
gevent.config.loop = "libuv"

import gevent.monkey
gevent.monkey.patch_all()
```

---

# Welcome to Flask¶

# Welcome to Flask

Welcome to Flask’s documentation. Flask is a lightweight WSGI web application framework.
It is designed to make getting started quick and easy, with the ability to scale up to
complex applications.

Get started with [Installation](https://flask.palletsprojects.com/en/stable/installation/)
and then get an overview with the [Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/). There is also a
more detailed [Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/) that shows how to create a small but
complete application with Flask. Common patterns are described in the
[Patterns for Flask](https://flask.palletsprojects.com/en/stable/patterns/) section. The rest of the docs describe each
component of Flask in detail, with a full reference in the [API](https://flask.palletsprojects.com/en/stable/api/)
section.

Flask depends on the [Werkzeug](https://werkzeug.palletsprojects.com) WSGI toolkit, the [Jinja](https://jinja.palletsprojects.com) template engine, and the
[Click](https://click.palletsprojects.com) CLI toolkit. Be sure to check their documentation as well as Flask’s when
looking for information.

## User’s Guide

Flask provides configuration and conventions, with sensible defaults, to get started.
This section of the documentation explains the different parts of the Flask framework
and how they can be used, customized, and extended. Beyond Flask itself, look for
community-maintained extensions to add even more functionality.

- [Installation](https://flask.palletsprojects.com/en/stable/installation/)
  - [Python Version](https://flask.palletsprojects.com/en/stable/installation/#python-version)
  - [Dependencies](https://flask.palletsprojects.com/en/stable/installation/#dependencies)
  - [Virtual environments](https://flask.palletsprojects.com/en/stable/installation/#virtual-environments)
  - [Install Flask](https://flask.palletsprojects.com/en/stable/installation/#install-flask)
- [Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
  - [A Minimal Application](https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application)
  - [Debug Mode](https://flask.palletsprojects.com/en/stable/quickstart/#debug-mode)
  - [HTML Escaping](https://flask.palletsprojects.com/en/stable/quickstart/#html-escaping)
  - [Routing](https://flask.palletsprojects.com/en/stable/quickstart/#routing)
  - [Static Files](https://flask.palletsprojects.com/en/stable/quickstart/#static-files)
  - [Rendering Templates](https://flask.palletsprojects.com/en/stable/quickstart/#rendering-templates)
  - [Accessing Request Data](https://flask.palletsprojects.com/en/stable/quickstart/#accessing-request-data)
  - [Redirects and Errors](https://flask.palletsprojects.com/en/stable/quickstart/#redirects-and-errors)
  - [About Responses](https://flask.palletsprojects.com/en/stable/quickstart/#about-responses)
  - [Sessions](https://flask.palletsprojects.com/en/stable/quickstart/#sessions)
  - [Message Flashing](https://flask.palletsprojects.com/en/stable/quickstart/#message-flashing)
  - [Logging](https://flask.palletsprojects.com/en/stable/quickstart/#logging)
  - [Hooking in WSGI Middleware](https://flask.palletsprojects.com/en/stable/quickstart/#hooking-in-wsgi-middleware)
  - [Using Flask Extensions](https://flask.palletsprojects.com/en/stable/quickstart/#using-flask-extensions)
  - [Deploying to a Web Server](https://flask.palletsprojects.com/en/stable/quickstart/#deploying-to-a-web-server)
- [Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
  - [Project Layout](https://flask.palletsprojects.com/en/stable/tutorial/layout/)
  - [Application Setup](https://flask.palletsprojects.com/en/stable/tutorial/factory/)
  - [Define and Access the Database](https://flask.palletsprojects.com/en/stable/tutorial/database/)
  - [Blueprints and Views](https://flask.palletsprojects.com/en/stable/tutorial/views/)
  - [Templates](https://flask.palletsprojects.com/en/stable/tutorial/templates/)
  - [Static Files](https://flask.palletsprojects.com/en/stable/tutorial/static/)
  - [Blog Blueprint](https://flask.palletsprojects.com/en/stable/tutorial/blog/)
  - [Make the Project Installable](https://flask.palletsprojects.com/en/stable/tutorial/install/)
  - [Test Coverage](https://flask.palletsprojects.com/en/stable/tutorial/tests/)
  - [Deploy to Production](https://flask.palletsprojects.com/en/stable/tutorial/deploy/)
  - [Keep Developing!](https://flask.palletsprojects.com/en/stable/tutorial/next/)
- [Templates](https://flask.palletsprojects.com/en/stable/templating/)
  - [Jinja Setup](https://flask.palletsprojects.com/en/stable/templating/#jinja-setup)
  - [Standard Context](https://flask.palletsprojects.com/en/stable/templating/#standard-context)
  - [Controlling Autoescaping](https://flask.palletsprojects.com/en/stable/templating/#controlling-autoescaping)
  - [Registering Filters](https://flask.palletsprojects.com/en/stable/templating/#registering-filters)
  - [Context Processors](https://flask.palletsprojects.com/en/stable/templating/#context-processors)
  - [Streaming](https://flask.palletsprojects.com/en/stable/templating/#streaming)
- [Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/)
  - [Identifying Tests](https://flask.palletsprojects.com/en/stable/testing/#identifying-tests)
  - [Fixtures](https://flask.palletsprojects.com/en/stable/testing/#fixtures)
  - [Sending Requests with the Test Client](https://flask.palletsprojects.com/en/stable/testing/#sending-requests-with-the-test-client)
  - [Following Redirects](https://flask.palletsprojects.com/en/stable/testing/#following-redirects)
  - [Accessing and Modifying the Session](https://flask.palletsprojects.com/en/stable/testing/#accessing-and-modifying-the-session)
  - [Running Commands with the CLI Runner](https://flask.palletsprojects.com/en/stable/testing/#running-commands-with-the-cli-runner)
  - [Tests that depend on an Active Context](https://flask.palletsprojects.com/en/stable/testing/#tests-that-depend-on-an-active-context)
- [Handling Application Errors](https://flask.palletsprojects.com/en/stable/errorhandling/)
  - [Error Logging Tools](https://flask.palletsprojects.com/en/stable/errorhandling/#error-logging-tools)
  - [Error Handlers](https://flask.palletsprojects.com/en/stable/errorhandling/#error-handlers)
  - [Custom Error Pages](https://flask.palletsprojects.com/en/stable/errorhandling/#custom-error-pages)
  - [Blueprint Error Handlers](https://flask.palletsprojects.com/en/stable/errorhandling/#blueprint-error-handlers)
  - [Returning API Errors as JSON](https://flask.palletsprojects.com/en/stable/errorhandling/#returning-api-errors-as-json)
  - [Logging](https://flask.palletsprojects.com/en/stable/errorhandling/#logging)
  - [Debugging](https://flask.palletsprojects.com/en/stable/errorhandling/#debugging)
- [Debugging Application Errors](https://flask.palletsprojects.com/en/stable/debugging/)
  - [In Production](https://flask.palletsprojects.com/en/stable/debugging/#in-production)
  - [The Built-In Debugger](https://flask.palletsprojects.com/en/stable/debugging/#the-built-in-debugger)
  - [External Debuggers](https://flask.palletsprojects.com/en/stable/debugging/#external-debuggers)
- [Logging](https://flask.palletsprojects.com/en/stable/logging/)
  - [Basic Configuration](https://flask.palletsprojects.com/en/stable/logging/#basic-configuration)
  - [Email Errors to Admins](https://flask.palletsprojects.com/en/stable/logging/#email-errors-to-admins)
  - [Injecting Request Information](https://flask.palletsprojects.com/en/stable/logging/#injecting-request-information)
  - [Other Libraries](https://flask.palletsprojects.com/en/stable/logging/#other-libraries)
- [Configuration Handling](https://flask.palletsprojects.com/en/stable/config/)
  - [Configuration Basics](https://flask.palletsprojects.com/en/stable/config/#configuration-basics)
  - [Debug Mode](https://flask.palletsprojects.com/en/stable/config/#debug-mode)
  - [Builtin Configuration Values](https://flask.palletsprojects.com/en/stable/config/#builtin-configuration-values)
  - [Configuring from Python Files](https://flask.palletsprojects.com/en/stable/config/#configuring-from-python-files)
  - [Configuring from Data Files](https://flask.palletsprojects.com/en/stable/config/#configuring-from-data-files)
  - [Configuring from Environment Variables](https://flask.palletsprojects.com/en/stable/config/#configuring-from-environment-variables)
  - [Configuration Best Practices](https://flask.palletsprojects.com/en/stable/config/#configuration-best-practices)
  - [Development / Production](https://flask.palletsprojects.com/en/stable/config/#development-production)
  - [Instance Folders](https://flask.palletsprojects.com/en/stable/config/#instance-folders)
- [Signals](https://flask.palletsprojects.com/en/stable/signals/)
  - [Core Signals](https://flask.palletsprojects.com/en/stable/signals/#core-signals)
  - [Subscribing to Signals](https://flask.palletsprojects.com/en/stable/signals/#subscribing-to-signals)
  - [Creating Signals](https://flask.palletsprojects.com/en/stable/signals/#creating-signals)
  - [Sending Signals](https://flask.palletsprojects.com/en/stable/signals/#sending-signals)
  - [Signals and Flask’s Request Context](https://flask.palletsprojects.com/en/stable/signals/#signals-and-flask-s-request-context)
  - [Decorator Based Signal Subscriptions](https://flask.palletsprojects.com/en/stable/signals/#decorator-based-signal-subscriptions)
- [Class-based Views](https://flask.palletsprojects.com/en/stable/views/)
  - [Basic Reusable View](https://flask.palletsprojects.com/en/stable/views/#basic-reusable-view)
  - [URL Variables](https://flask.palletsprojects.com/en/stable/views/#url-variables)
  - [View Lifetime andself](https://flask.palletsprojects.com/en/stable/views/#view-lifetime-and-self)
  - [View Decorators](https://flask.palletsprojects.com/en/stable/views/#view-decorators)
  - [Method Hints](https://flask.palletsprojects.com/en/stable/views/#method-hints)
  - [Method Dispatching and APIs](https://flask.palletsprojects.com/en/stable/views/#method-dispatching-and-apis)
- [Application Structure and Lifecycle](https://flask.palletsprojects.com/en/stable/lifecycle/)
  - [Application Setup](https://flask.palletsprojects.com/en/stable/lifecycle/#application-setup)
  - [Serving the Application](https://flask.palletsprojects.com/en/stable/lifecycle/#serving-the-application)
  - [How a Request is Handled](https://flask.palletsprojects.com/en/stable/lifecycle/#how-a-request-is-handled)
- [The Application Context](https://flask.palletsprojects.com/en/stable/appcontext/)
  - [Purpose of the Context](https://flask.palletsprojects.com/en/stable/appcontext/#purpose-of-the-context)
  - [Lifetime of the Context](https://flask.palletsprojects.com/en/stable/appcontext/#lifetime-of-the-context)
  - [Manually Push a Context](https://flask.palletsprojects.com/en/stable/appcontext/#manually-push-a-context)
  - [Storing Data](https://flask.palletsprojects.com/en/stable/appcontext/#storing-data)
  - [Events and Signals](https://flask.palletsprojects.com/en/stable/appcontext/#events-and-signals)
- [The Request Context](https://flask.palletsprojects.com/en/stable/reqcontext/)
  - [Purpose of the Context](https://flask.palletsprojects.com/en/stable/reqcontext/#purpose-of-the-context)
  - [Lifetime of the Context](https://flask.palletsprojects.com/en/stable/reqcontext/#lifetime-of-the-context)
  - [Manually Push a Context](https://flask.palletsprojects.com/en/stable/reqcontext/#manually-push-a-context)
  - [How the Context Works](https://flask.palletsprojects.com/en/stable/reqcontext/#how-the-context-works)
  - [Callbacks and Errors](https://flask.palletsprojects.com/en/stable/reqcontext/#callbacks-and-errors)
  - [Notes On Proxies](https://flask.palletsprojects.com/en/stable/reqcontext/#notes-on-proxies)
- [Modular Applications with Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/)
  - [Why Blueprints?](https://flask.palletsprojects.com/en/stable/blueprints/#why-blueprints)
  - [The Concept of Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/#the-concept-of-blueprints)
  - [My First Blueprint](https://flask.palletsprojects.com/en/stable/blueprints/#my-first-blueprint)
  - [Registering Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/#registering-blueprints)
  - [Nesting Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/#nesting-blueprints)
  - [Blueprint Resources](https://flask.palletsprojects.com/en/stable/blueprints/#blueprint-resources)
  - [Building URLs](https://flask.palletsprojects.com/en/stable/blueprints/#building-urls)
  - [Blueprint Error Handlers](https://flask.palletsprojects.com/en/stable/blueprints/#blueprint-error-handlers)
- [Extensions](https://flask.palletsprojects.com/en/stable/extensions/)
  - [Finding Extensions](https://flask.palletsprojects.com/en/stable/extensions/#finding-extensions)
  - [Using Extensions](https://flask.palletsprojects.com/en/stable/extensions/#using-extensions)
  - [Building Extensions](https://flask.palletsprojects.com/en/stable/extensions/#building-extensions)
- [Command Line Interface](https://flask.palletsprojects.com/en/stable/cli/)
  - [Application Discovery](https://flask.palletsprojects.com/en/stable/cli/#application-discovery)
  - [Run the Development Server](https://flask.palletsprojects.com/en/stable/cli/#run-the-development-server)
  - [Open a Shell](https://flask.palletsprojects.com/en/stable/cli/#open-a-shell)
  - [Environment Variables From dotenv](https://flask.palletsprojects.com/en/stable/cli/#environment-variables-from-dotenv)
  - [Environment Variables From virtualenv](https://flask.palletsprojects.com/en/stable/cli/#environment-variables-from-virtualenv)
  - [Custom Commands](https://flask.palletsprojects.com/en/stable/cli/#custom-commands)
  - [Plugins](https://flask.palletsprojects.com/en/stable/cli/#plugins)
  - [Custom Scripts](https://flask.palletsprojects.com/en/stable/cli/#custom-scripts)
  - [PyCharm Integration](https://flask.palletsprojects.com/en/stable/cli/#pycharm-integration)
- [Development Server](https://flask.palletsprojects.com/en/stable/server/)
  - [Command Line](https://flask.palletsprojects.com/en/stable/server/#command-line)
  - [In Code](https://flask.palletsprojects.com/en/stable/server/#in-code)
- [Working with the Shell](https://flask.palletsprojects.com/en/stable/shell/)
  - [Command Line Interface](https://flask.palletsprojects.com/en/stable/shell/#command-line-interface)
  - [Creating a Request Context](https://flask.palletsprojects.com/en/stable/shell/#creating-a-request-context)
  - [Firing Before/After Request](https://flask.palletsprojects.com/en/stable/shell/#firing-before-after-request)
  - [Further Improving the Shell Experience](https://flask.palletsprojects.com/en/stable/shell/#further-improving-the-shell-experience)
- [Patterns for Flask](https://flask.palletsprojects.com/en/stable/patterns/)
  - [Large Applications as Packages](https://flask.palletsprojects.com/en/stable/patterns/packages/)
  - [Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)
  - [Application Dispatching](https://flask.palletsprojects.com/en/stable/patterns/appdispatch/)
  - [Using URL Processors](https://flask.palletsprojects.com/en/stable/patterns/urlprocessors/)
  - [Using SQLite 3 with Flask](https://flask.palletsprojects.com/en/stable/patterns/sqlite3/)
  - [SQLAlchemy in Flask](https://flask.palletsprojects.com/en/stable/patterns/sqlalchemy/)
  - [Uploading Files](https://flask.palletsprojects.com/en/stable/patterns/fileuploads/)
  - [Caching](https://flask.palletsprojects.com/en/stable/patterns/caching/)
  - [View Decorators](https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/)
  - [Form Validation with WTForms](https://flask.palletsprojects.com/en/stable/patterns/wtforms/)
  - [Template Inheritance](https://flask.palletsprojects.com/en/stable/patterns/templateinheritance/)
  - [Message Flashing](https://flask.palletsprojects.com/en/stable/patterns/flashing/)
  - [JavaScript,fetch, and JSON](https://flask.palletsprojects.com/en/stable/patterns/javascript/)
  - [Lazily Loading Views](https://flask.palletsprojects.com/en/stable/patterns/lazyloading/)
  - [MongoDB with MongoEngine](https://flask.palletsprojects.com/en/stable/patterns/mongoengine/)
  - [Adding a favicon](https://flask.palletsprojects.com/en/stable/patterns/favicon/)
  - [Streaming Contents](https://flask.palletsprojects.com/en/stable/patterns/streaming/)
  - [Deferred Request Callbacks](https://flask.palletsprojects.com/en/stable/patterns/deferredcallbacks/)
  - [Adding HTTP Method Overrides](https://flask.palletsprojects.com/en/stable/patterns/methodoverrides/)
  - [Request Content Checksums](https://flask.palletsprojects.com/en/stable/patterns/requestchecksum/)
  - [Background Tasks with Celery](https://flask.palletsprojects.com/en/stable/patterns/celery/)
  - [Subclassing Flask](https://flask.palletsprojects.com/en/stable/patterns/subclassing/)
  - [Single-Page Applications](https://flask.palletsprojects.com/en/stable/patterns/singlepageapplications/)
- [Security Considerations](https://flask.palletsprojects.com/en/stable/web-security/)
  - [Resource Use](https://flask.palletsprojects.com/en/stable/web-security/#resource-use)
  - [Cross-Site Scripting (XSS)](https://flask.palletsprojects.com/en/stable/web-security/#cross-site-scripting-xss)
  - [Cross-Site Request Forgery (CSRF)](https://flask.palletsprojects.com/en/stable/web-security/#cross-site-request-forgery-csrf)
  - [JSON Security](https://flask.palletsprojects.com/en/stable/web-security/#json-security)
  - [Security Headers](https://flask.palletsprojects.com/en/stable/web-security/#security-headers)
  - [Host Header Validation](https://flask.palletsprojects.com/en/stable/web-security/#host-header-validation)
  - [Copy/Paste to Terminal](https://flask.palletsprojects.com/en/stable/web-security/#copy-paste-to-terminal)
- [Deploying to Production](https://flask.palletsprojects.com/en/stable/deploying/)
  - [Self-Hosted Options](https://flask.palletsprojects.com/en/stable/deploying/#self-hosted-options)
  - [Hosting Platforms](https://flask.palletsprojects.com/en/stable/deploying/#hosting-platforms)
- [Async with Gevent](https://flask.palletsprojects.com/en/stable/gevent/)
  - [Enabling gevent](https://flask.palletsprojects.com/en/stable/gevent/#enabling-gevent)
  - [Combining withasync/await](https://flask.palletsprojects.com/en/stable/gevent/#combining-with-async-await)
- [Usingasyncandawait](https://flask.palletsprojects.com/en/stable/async-await/)
  - [Performance](https://flask.palletsprojects.com/en/stable/async-await/#performance)
  - [Background tasks](https://flask.palletsprojects.com/en/stable/async-await/#background-tasks)
  - [When to use Quart instead](https://flask.palletsprojects.com/en/stable/async-await/#when-to-use-quart-instead)
  - [Extensions](https://flask.palletsprojects.com/en/stable/async-await/#extensions)
  - [Other event loops](https://flask.palletsprojects.com/en/stable/async-await/#other-event-loops)

## API Reference

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

- [API](https://flask.palletsprojects.com/en/stable/api/)
  - [Application Object](https://flask.palletsprojects.com/en/stable/api/#application-object)
  - [Blueprint Objects](https://flask.palletsprojects.com/en/stable/api/#blueprint-objects)
  - [Incoming Request Data](https://flask.palletsprojects.com/en/stable/api/#incoming-request-data)
  - [Response Objects](https://flask.palletsprojects.com/en/stable/api/#response-objects)
  - [Sessions](https://flask.palletsprojects.com/en/stable/api/#sessions)
  - [Session Interface](https://flask.palletsprojects.com/en/stable/api/#session-interface)
  - [Test Client](https://flask.palletsprojects.com/en/stable/api/#test-client)
  - [Test CLI Runner](https://flask.palletsprojects.com/en/stable/api/#test-cli-runner)
  - [Application Globals](https://flask.palletsprojects.com/en/stable/api/#application-globals)
  - [Useful Functions and Classes](https://flask.palletsprojects.com/en/stable/api/#useful-functions-and-classes)
  - [Message Flashing](https://flask.palletsprojects.com/en/stable/api/#message-flashing)
  - [JSON Support](https://flask.palletsprojects.com/en/stable/api/#module-flask.json)
  - [Template Rendering](https://flask.palletsprojects.com/en/stable/api/#template-rendering)
  - [Configuration](https://flask.palletsprojects.com/en/stable/api/#configuration)
  - [Stream Helpers](https://flask.palletsprojects.com/en/stable/api/#stream-helpers)
  - [Useful Internals](https://flask.palletsprojects.com/en/stable/api/#useful-internals)
  - [Signals](https://flask.palletsprojects.com/en/stable/api/#signals)
  - [Class-Based Views](https://flask.palletsprojects.com/en/stable/api/#class-based-views)
  - [URL Route Registrations](https://flask.palletsprojects.com/en/stable/api/#url-route-registrations)
  - [View Function Options](https://flask.palletsprojects.com/en/stable/api/#view-function-options)
  - [Command Line Interface](https://flask.palletsprojects.com/en/stable/api/#command-line-interface)

## Additional Notes

- [Design Decisions in Flask](https://flask.palletsprojects.com/en/stable/design/)
  - [The Explicit Application Object](https://flask.palletsprojects.com/en/stable/design/#the-explicit-application-object)
  - [The Routing System](https://flask.palletsprojects.com/en/stable/design/#the-routing-system)
  - [One Template Engine](https://flask.palletsprojects.com/en/stable/design/#one-template-engine)
  - [What does “micro” mean?](https://flask.palletsprojects.com/en/stable/design/#what-does-micro-mean)
  - [Thread Locals](https://flask.palletsprojects.com/en/stable/design/#thread-locals)
  - [Async/await and ASGI support](https://flask.palletsprojects.com/en/stable/design/#async-await-and-asgi-support)
  - [What Flask is, What Flask is Not](https://flask.palletsprojects.com/en/stable/design/#what-flask-is-what-flask-is-not)
- [Flask Extension Development](https://flask.palletsprojects.com/en/stable/extensiondev/)
  - [Naming](https://flask.palletsprojects.com/en/stable/extensiondev/#naming)
  - [The Extension Class and Initialization](https://flask.palletsprojects.com/en/stable/extensiondev/#the-extension-class-and-initialization)
  - [Adding Behavior](https://flask.palletsprojects.com/en/stable/extensiondev/#adding-behavior)
  - [Configuration Techniques](https://flask.palletsprojects.com/en/stable/extensiondev/#configuration-techniques)
  - [Data During a Request](https://flask.palletsprojects.com/en/stable/extensiondev/#data-during-a-request)
  - [Views and Models](https://flask.palletsprojects.com/en/stable/extensiondev/#views-and-models)
  - [Recommended Extension Guidelines](https://flask.palletsprojects.com/en/stable/extensiondev/#recommended-extension-guidelines)
- [Contributing](https://flask.palletsprojects.com/en/stable/contributing/)
- [BSD-3-Clause License](https://flask.palletsprojects.com/en/stable/license/)
- [Changes](https://flask.palletsprojects.com/en/stable/changes/)
  - [Version 3.1.2](https://flask.palletsprojects.com/en/stable/changes/#version-3-1-2)
  - [Version 3.1.1](https://flask.palletsprojects.com/en/stable/changes/#version-3-1-1)
  - [Version 3.1.0](https://flask.palletsprojects.com/en/stable/changes/#version-3-1-0)
  - [Version 3.0.3](https://flask.palletsprojects.com/en/stable/changes/#version-3-0-3)
  - [Version 3.0.2](https://flask.palletsprojects.com/en/stable/changes/#version-3-0-2)
  - [Version 3.0.1](https://flask.palletsprojects.com/en/stable/changes/#version-3-0-1)
  - [Version 3.0.0](https://flask.palletsprojects.com/en/stable/changes/#version-3-0-0)
  - [Version 2.3.3](https://flask.palletsprojects.com/en/stable/changes/#version-2-3-3)
  - [Version 2.3.2](https://flask.palletsprojects.com/en/stable/changes/#version-2-3-2)
  - [Version 2.3.1](https://flask.palletsprojects.com/en/stable/changes/#version-2-3-1)
  - [Version 2.3.0](https://flask.palletsprojects.com/en/stable/changes/#version-2-3-0)
  - [Version 2.2.5](https://flask.palletsprojects.com/en/stable/changes/#version-2-2-5)
  - [Version 2.2.4](https://flask.palletsprojects.com/en/stable/changes/#version-2-2-4)
  - [Version 2.2.3](https://flask.palletsprojects.com/en/stable/changes/#version-2-2-3)
  - [Version 2.2.2](https://flask.palletsprojects.com/en/stable/changes/#version-2-2-2)
  - [Version 2.2.1](https://flask.palletsprojects.com/en/stable/changes/#version-2-2-1)
  - [Version 2.2.0](https://flask.palletsprojects.com/en/stable/changes/#version-2-2-0)
  - [Version 2.1.3](https://flask.palletsprojects.com/en/stable/changes/#version-2-1-3)
  - [Version 2.1.2](https://flask.palletsprojects.com/en/stable/changes/#version-2-1-2)
  - [Version 2.1.1](https://flask.palletsprojects.com/en/stable/changes/#version-2-1-1)
  - [Version 2.1.0](https://flask.palletsprojects.com/en/stable/changes/#version-2-1-0)
  - [Version 2.0.3](https://flask.palletsprojects.com/en/stable/changes/#version-2-0-3)
  - [Version 2.0.2](https://flask.palletsprojects.com/en/stable/changes/#version-2-0-2)
  - [Version 2.0.1](https://flask.palletsprojects.com/en/stable/changes/#version-2-0-1)
  - [Version 2.0.0](https://flask.palletsprojects.com/en/stable/changes/#version-2-0-0)
  - [Version 1.1.4](https://flask.palletsprojects.com/en/stable/changes/#version-1-1-4)
  - [Version 1.1.3](https://flask.palletsprojects.com/en/stable/changes/#version-1-1-3)
  - [Version 1.1.2](https://flask.palletsprojects.com/en/stable/changes/#version-1-1-2)
  - [Version 1.1.1](https://flask.palletsprojects.com/en/stable/changes/#version-1-1-1)
  - [Version 1.1.0](https://flask.palletsprojects.com/en/stable/changes/#version-1-1-0)
  - [Version 1.0.4](https://flask.palletsprojects.com/en/stable/changes/#version-1-0-4)
  - [Version 1.0.3](https://flask.palletsprojects.com/en/stable/changes/#version-1-0-3)
  - [Version 1.0.2](https://flask.palletsprojects.com/en/stable/changes/#version-1-0-2)
  - [Version 1.0.1](https://flask.palletsprojects.com/en/stable/changes/#version-1-0-1)
  - [Version 1.0](https://flask.palletsprojects.com/en/stable/changes/#version-1-0)
  - [Version 0.12.5](https://flask.palletsprojects.com/en/stable/changes/#version-0-12-5)
  - [Version 0.12.4](https://flask.palletsprojects.com/en/stable/changes/#version-0-12-4)
  - [Version 0.12.3](https://flask.palletsprojects.com/en/stable/changes/#version-0-12-3)
  - [Version 0.12.2](https://flask.palletsprojects.com/en/stable/changes/#version-0-12-2)
  - [Version 0.12.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-12-1)
  - [Version 0.12](https://flask.palletsprojects.com/en/stable/changes/#version-0-12)
  - [Version 0.11.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-11-1)
  - [Version 0.11](https://flask.palletsprojects.com/en/stable/changes/#version-0-11)
  - [Version 0.10.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-10-1)
  - [Version 0.10](https://flask.palletsprojects.com/en/stable/changes/#version-0-10)
  - [Version 0.9](https://flask.palletsprojects.com/en/stable/changes/#version-0-9)
  - [Version 0.8.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-8-1)
  - [Version 0.8](https://flask.palletsprojects.com/en/stable/changes/#version-0-8)
  - [Version 0.7.2](https://flask.palletsprojects.com/en/stable/changes/#version-0-7-2)
  - [Version 0.7.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-7-1)
  - [Version 0.7](https://flask.palletsprojects.com/en/stable/changes/#version-0-7)
  - [Version 0.6.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-6-1)
  - [Version 0.6](https://flask.palletsprojects.com/en/stable/changes/#version-0-6)
  - [Version 0.5.2](https://flask.palletsprojects.com/en/stable/changes/#version-0-5-2)
  - [Version 0.5.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-5-1)
  - [Version 0.5](https://flask.palletsprojects.com/en/stable/changes/#version-0-5)
  - [Version 0.4](https://flask.palletsprojects.com/en/stable/changes/#version-0-4)
  - [Version 0.3.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-3-1)
  - [Version 0.3](https://flask.palletsprojects.com/en/stable/changes/#version-0-3)
  - [Version 0.2](https://flask.palletsprojects.com/en/stable/changes/#version-0-2)
  - [Version 0.1](https://flask.palletsprojects.com/en/stable/changes/#version-0-1)

---

# Installation¶

# Installation

## Python Version

We recommend using the latest version of Python. Flask supports Python 3.9 and newer.

## Dependencies

These distributions will be installed automatically when installing Flask.

- [Werkzeug](https://palletsprojects.com/p/werkzeug/) implements WSGI, the standard Python interface between
  applications and servers.
- [Jinja](https://palletsprojects.com/p/jinja/) is a template language that renders the pages your application
  serves.
- [MarkupSafe](https://palletsprojects.com/p/markupsafe/) comes with Jinja. It escapes untrusted input when rendering
  templates to avoid injection attacks.
- [ItsDangerous](https://palletsprojects.com/p/itsdangerous/) securely signs data to ensure its integrity. This is used
  to protect Flask’s session cookie.
- [Click](https://palletsprojects.com/p/click/) is a framework for writing command line applications. It provides
  the `flask` command and allows adding custom management commands.
- [Blinker](https://blinker.readthedocs.io/) provides support for [Signals](https://flask.palletsprojects.com/en/signals/).

### Optional dependencies

These distributions will not be installed automatically. Flask will detect and
use them if you install them.

- [python-dotenv](https://github.com/theskumar/python-dotenv#readme) enables support for [Environment Variables From dotenv](https://flask.palletsprojects.com/en/cli/#dotenv) when running `flask`
  commands.
- [Watchdog](https://pythonhosted.org/watchdog/) provides a faster, more efficient reloader for the development
  server.

### greenlet

You may choose to use [Async with Gevent](https://flask.palletsprojects.com/en/gevent/) with your application. In this case,
greenlet>=1.0 is required. When using PyPy, PyPy>=7.3.7 is required.

These are not minimum supported versions, they only indicate the first
versions that added necessary features. You should use the latest
versions of each.

## Virtual environments

Use a virtual environment to manage the dependencies for your project, both in
development and in production.

What problem does a virtual environment solve? The more Python projects you
have, the more likely it is that you need to work with different versions of
Python libraries, or even Python itself. Newer versions of libraries for one
project can break compatibility in another project.

Virtual environments are independent groups of Python libraries, one for each
project. Packages installed for one project will not affect other projects or
the operating system’s packages.

Python comes bundled with the [venv](https://docs.python.org/3/library/venv.html#module-venv) module to create virtual
environments.

### Create an environment

Create a project folder and a `.venv` folder within:

```
$ mkdir myproject
$ cd myproject
$ python3 -m venv .venv
```

```
> mkdir myproject
> cd myproject
> py -3 -m venv .venv
```

### Activate the environment

Before you work on your project, activate the corresponding environment:

```
$ . .venv/bin/activate
```

```
> .venv\Scripts\activate
```

Your shell prompt will change to show the name of the activated
environment.

## Install Flask

Within the activated environment, use the following command to install
Flask:

```
$ pip install Flask
```

Flask is now installed. Check out the [Quickstart](https://flask.palletsprojects.com/en/quickstart/) or go to the
[Documentation Overview](https://flask.palletsprojects.com/en/).

---

# BSD

# BSD-3-Clause License

```
Copyright 2010 Pallets

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1.  Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

2.  Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

3.  Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

---

# Application Structure and Lifecycle¶

# Application Structure and Lifecycle

Flask makes it pretty easy to write a web application. But there are quite a few
different parts to an application and to each request it handles. Knowing what happens
during application setup, serving, and handling requests will help you know what’s
possible in Flask and how to structure your application.

## Application Setup

The first step in creating a Flask application is creating the application object. Each
Flask application is an instance of the [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) class, which collects all
configuration, extensions, and views.

```
from flask import Flask

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY="dev",
)
app.config.from_prefixed_env()

@app.route("/")
def index():
    return "Hello, World!"
```

This is known as the “application setup phase”, it’s the code you write that’s outside
any view functions or other handlers. It can be split up between different modules and
sub-packages, but all code that you want to be part of your application must be imported
in order for it to be registered.

All application setup must be completed before you start serving your application and
handling requests. This is because WSGI servers divide work between multiple workers, or
can be distributed across multiple machines. If the configuration changed in one worker,
there’s no way for Flask to ensure consistency between other workers.

Flask tries to help developers catch some of these setup ordering issues by showing an
error if setup-related methods are called after requests are handled. In that case
you’ll see this error:

> The setup method ‘route’ can no longer be called on the application. It has already
> handled its first request, any changes will not be applied consistently.
> Make sure all imports, decorators, functions, etc. needed to set up the application
> are done before running it.

However, it is not possible for Flask to detect all cases of out-of-order setup. In
general, don’t do anything to modify the `Flask` app object and `Blueprint` objects
from within view functions that run during requests. This includes:

- Adding routes, view functions, and other request handlers with `@app.route`,
  `@app.errorhandler`, `@app.before_request`, etc.
- Registering blueprints.
- Loading configuration with `app.config`.
- Setting up the Jinja template environment with `app.jinja_env`.
- Setting a session interface, instead of the default itsdangerous cookie.
- Setting a JSON provider with `app.json`, instead of the default provider.
- Creating and initializing Flask extensions.

## Serving the Application

Flask is a WSGI application framework. The other half of WSGI is the WSGI server. During
development, Flask, through Werkzeug, provides a development WSGI server with the
`flask run` CLI command. When you are done with development, use a production server
to serve your application, see [Deploying to Production](https://flask.palletsprojects.com/en/deploying/).

Regardless of what server you’re using, it will follow the [PEP 3333](https://peps.python.org/pep-3333/) WSGI spec. The
WSGI server will be told how to access your Flask application object, which is the WSGI
application. Then it will start listening for HTTP requests, translate the request data
into a WSGI environ, and call the WSGI application with that data. The WSGI application
will return data that is translated into an HTTP response.

1. Browser or other client makes HTTP request.
2. WSGI server receives request.
3. WSGI server converts HTTP data to WSGI `environ` dict.
4. WSGI server calls WSGI application with the `environ`.
5. Flask, the WSGI application, does all its internal processing to route the request
  to a view function, handle errors, etc.
6. Flask translates View function return into WSGI response data, passes it to WSGI
  server.
7. WSGI server creates and send an HTTP response.
8. Client receives the HTTP response.

### Middleware

The WSGI application above is a callable that behaves in a certain way. Middleware
is a WSGI application that wraps another WSGI application. It’s a similar concept to
Python decorators. The outermost middleware will be called by the server. It can modify
the data passed to it, then call the WSGI application (or further middleware) that it
wraps, and so on. And it can take the return value of that call and modify it further.

From the WSGI server’s perspective, there is one WSGI application, the one it calls
directly. Typically, Flask is the “real” application at the end of the chain of
middleware. But even Flask can call further WSGI applications, although that’s an
advanced, uncommon use case.

A common middleware you’ll see used with Flask is Werkzeug’s
[ProxyFix](https://werkzeug.palletsprojects.com/en/stable/middleware/proxy_fix/#werkzeug.middleware.proxy_fix.ProxyFix), which modifies the request to look
like it came directly from a client even if it passed through HTTP proxies on the way.
There are other middleware that can handle serving static files, authentication, etc.

## How a Request is Handled

For us, the interesting part of the steps above is when Flask gets called by the WSGI
server (or middleware). At that point, it will do quite a lot to handle the request and
generate the response. At the most basic, it will match the URL to a view function, call
the view function, and pass the return value back to the server. But there are many more
parts that you can use to customize its behavior.

1. WSGI server calls the Flask object, which calls [Flask.wsgi_app()](https://flask.palletsprojects.com/en/api/#flask.Flask.wsgi_app).
2. A [RequestContext](https://flask.palletsprojects.com/en/api/#flask.ctx.RequestContext) object is created. This converts the WSGI `environ`
  dict into a [Request](https://flask.palletsprojects.com/en/api/#flask.Request) object. It also creates an `AppContext` object.
3. The [app context](https://flask.palletsprojects.com/en/appcontext/) is pushed, which makes [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app) and
  [g](https://flask.palletsprojects.com/en/api/#flask.g) available.
4. The [appcontext_pushed](https://flask.palletsprojects.com/en/api/#flask.appcontext_pushed) signal is sent.
5. The [request context](https://flask.palletsprojects.com/en/reqcontext/) is pushed, which makes [request](https://flask.palletsprojects.com/en/api/#flask.request) and
  [session](https://flask.palletsprojects.com/en/api/#flask.session) available.
6. The session is opened, loading any existing session data using the app’s
  [session_interface](https://flask.palletsprojects.com/en/api/#flask.Flask.session_interface), an instance of [SessionInterface](https://flask.palletsprojects.com/en/api/#flask.sessions.SessionInterface).
7. The URL is matched against the URL rules registered with the [route()](https://flask.palletsprojects.com/en/api/#flask.Flask.route)
  decorator during application setup. If there is no match, the error - usually a 404,
  405, or redirect - is stored to be handled later.
8. The [request_started](https://flask.palletsprojects.com/en/api/#flask.request_started) signal is sent.
9. Any [url_value_preprocessor()](https://flask.palletsprojects.com/en/api/#flask.Flask.url_value_preprocessor) decorated functions are called.
10. Any [before_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.before_request) decorated functions are called. If any of
  these function returns a value it is treated as the response immediately.
11. If the URL didn’t match a route a few steps ago, that error is raised now.
12. The [route()](https://flask.palletsprojects.com/en/api/#flask.Flask.route) decorated view function associated with the matched URL
  is called and returns a value to be used as the response.
13. If any step so far raised an exception, and there is an [errorhandler()](https://flask.palletsprojects.com/en/api/#flask.Flask.errorhandler)
  decorated function that matches the exception class or HTTP error code, it is
  called to handle the error and return a response.
14. Whatever returned a response value - a before request function, the view, or an
  error handler, that value is converted to a [Response](https://flask.palletsprojects.com/en/api/#flask.Response) object.
15. Any [after_this_request()](https://flask.palletsprojects.com/en/api/#flask.after_this_request) decorated functions are called, then cleared.
16. Any [after_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.after_request) decorated functions are called, which can modify
  the response object.
17. The session is saved, persisting any modified session data using the app’s
  [session_interface](https://flask.palletsprojects.com/en/api/#flask.Flask.session_interface).
18. The [request_finished](https://flask.palletsprojects.com/en/api/#flask.request_finished) signal is sent.
19. If any step so far raised an exception, and it was not handled by an error handler
  function, it is handled now. HTTP exceptions are treated as responses with their
  corresponding status code, other exceptions are converted to a generic 500 response.
  The [got_request_exception](https://flask.palletsprojects.com/en/api/#flask.got_request_exception) signal is sent.
20. The response object’s status, headers, and body are returned to the WSGI server.
21. Any [teardown_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_request) decorated functions are called.
22. The [request_tearing_down](https://flask.palletsprojects.com/en/api/#flask.request_tearing_down) signal is sent.
23. The request context is popped, [request](https://flask.palletsprojects.com/en/api/#flask.request) and [session](https://flask.palletsprojects.com/en/api/#flask.session) are no longer
  available.
24. Any [teardown_appcontext()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_appcontext) decorated functions are called.
25. The [appcontext_tearing_down](https://flask.palletsprojects.com/en/api/#flask.appcontext_tearing_down) signal is sent.
26. The app context is popped, [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app) and [g](https://flask.palletsprojects.com/en/api/#flask.g) are no longer
  available.
27. The [appcontext_popped](https://flask.palletsprojects.com/en/api/#flask.appcontext_popped) signal is sent.

There are even more decorators and customization points than this, but that aren’t part
of every request lifecycle. They’re more specific to certain things you might use during
a request, such as templates, building URLs, or handling JSON data. See the rest of this
documentation, as well as the [API](https://flask.palletsprojects.com/en/api/) to explore further.
