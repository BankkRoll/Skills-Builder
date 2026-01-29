# Application Dispatching¶ and more

# Application Dispatching¶

# Application Dispatching

Application dispatching is the process of combining multiple Flask
applications on the WSGI level.  You can combine not only Flask
applications but any WSGI application.  This would allow you to run a
Django and a Flask application in the same interpreter side by side if
you want.  The usefulness of this depends on how the applications work
internally.

The fundamental difference from [Large Applications as Packages](https://flask.palletsprojects.com/en/stable/packages/) is that in this case you
are running the same or different Flask applications that are entirely
isolated from each other. They run different configurations and are
dispatched on the WSGI level.

## Working with this Document

Each of the techniques and examples below results in an `application`
object that can be run with any WSGI server. For development, use the
`flask run` command to start a development server. For production, see
[Deploying to Production](https://flask.palletsprojects.com/en/deploying/).

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
```

## Combining Applications

If you have entirely separated applications and you want them to work next
to each other in the same Python interpreter process you can take
advantage of the `werkzeug.wsgi.DispatcherMiddleware`.  The idea
here is that each Flask application is a valid WSGI application and they
are combined by the dispatcher middleware into a larger one that is
dispatched based on prefix.

For example you could have your main application run on `/` and your
backend interface on `/backend`.

```
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from frontend_app import application as frontend
from backend_app import application as backend

application = DispatcherMiddleware(frontend, {
    '/backend': backend
})
```

## Dispatch by Subdomain

Sometimes you might want to use multiple instances of the same application
with different configurations.  Assuming the application is created inside
a function and you can call that function to instantiate it, that is
really easy to implement.  In order to develop your application to support
creating new instances in functions have a look at the
[Application Factories](https://flask.palletsprojects.com/en/stable/appfactories/) pattern.

A very common example would be creating applications per subdomain.  For
instance you configure your webserver to dispatch all requests for all
subdomains to your application and you then use the subdomain information
to create user-specific instances.  Once you have your server set up to
listen on all subdomains you can use a very simple WSGI application to do
the dynamic application creation.

The perfect level for abstraction in that regard is the WSGI layer.  You
write your own WSGI application that looks at the request that comes and
delegates it to your Flask application.  If that application does not
exist yet, it is dynamically created and remembered.

```
from threading import Lock

class SubdomainDispatcher:

    def __init__(self, domain, create_app):
        self.domain = domain
        self.create_app = create_app
        self.lock = Lock()
        self.instances = {}

    def get_application(self, host):
        host = host.split(':')[0]
        assert host.endswith(self.domain), 'Configuration error'
        subdomain = host[:-len(self.domain)].rstrip('.')
        with self.lock:
            app = self.instances.get(subdomain)
            if app is None:
                app = self.create_app(subdomain)
                self.instances[subdomain] = app
            return app

    def __call__(self, environ, start_response):
        app = self.get_application(environ['HTTP_HOST'])
        return app(environ, start_response)
```

This dispatcher can then be used like this:

```
from myapplication import create_app, get_user_for_subdomain
from werkzeug.exceptions import NotFound

def make_app(subdomain):
    user = get_user_for_subdomain(subdomain)
    if user is None:
        # if there is no user for that subdomain we still have
        # to return a WSGI application that handles that request.
        # We can then just return the NotFound() exception as
        # application which will render a default 404 page.
        # You might also redirect the user to the main page then
        return NotFound()

    # otherwise create the application for the specific user
    return create_app(user)

application = SubdomainDispatcher('example.com', make_app)
```

## Dispatch by Path

Dispatching by a path on the URL is very similar.  Instead of looking at
the `Host` header to figure out the subdomain one simply looks at the
request path up to the first slash.

```
from threading import Lock
from wsgiref.util import shift_path_info

class PathDispatcher:

    def __init__(self, default_app, create_app):
        self.default_app = default_app
        self.create_app = create_app
        self.lock = Lock()
        self.instances = {}

    def get_application(self, prefix):
        with self.lock:
            app = self.instances.get(prefix)
            if app is None:
                app = self.create_app(prefix)
                if app is not None:
                    self.instances[prefix] = app
            return app

    def __call__(self, environ, start_response):
        app = self.get_application(_peek_path_info(environ))
        if app is not None:
            shift_path_info(environ)
        else:
            app = self.default_app
        return app(environ, start_response)

def _peek_path_info(environ):
    segments = environ.get("PATH_INFO", "").lstrip("/").split("/", 1)
    if segments:
        return segments[0]

    return None
```

The big difference between this and the subdomain one is that this one
falls back to another application if the creator function returns `None`.

```
from myapplication import create_app, default_app, get_user_for_prefix

def make_app(prefix):
    user = get_user_for_prefix(prefix)
    if user is not None:
        return create_app(user)

application = PathDispatcher(default_app, make_app)
```

---

# Application Factories¶

# Application Factories

If you are already using packages and blueprints for your application
([Modular Applications with Blueprints](https://flask.palletsprojects.com/en/blueprints/)) there are a couple of really nice ways to further improve
the experience.  A common pattern is creating the application object when
the blueprint is imported.  But if you move the creation of this object
into a function, you can then create multiple instances of this app later.

So why would you want to do this?

1. Testing.  You can have instances of the application with different
  settings to test every case.
2. Multiple instances.  Imagine you want to run different versions of the
  same application.  Of course you could have multiple instances with
  different configs set up in your webserver, but if you use factories,
  you can have multiple instances of the same application running in the
  same application process which can be handy.

So how would you then actually implement that?

## Basic Factories

The idea is to set up the application in a function.  Like this:

```
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from yourapplication.model import db
    db.init_app(app)

    from yourapplication.views.admin import admin
    from yourapplication.views.frontend import frontend
    app.register_blueprint(admin)
    app.register_blueprint(frontend)

    return app
```

The downside is that you cannot use the application object in the blueprints
at import time.  You can however use it from within a request.  How do you
get access to the application with the config?  Use
[current_app](https://flask.palletsprojects.com/en/api/#flask.current_app):

```
from flask import current_app, Blueprint, render_template
admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
def index():
    return render_template(current_app.config['INDEX_TEMPLATE'])
```

Here we look up the name of a template in the config.

## Factories & Extensions

It’s preferable to create your extensions and app factories so that the
extension object does not initially get bound to the application.

Using [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/),
as an example, you should not do something along those lines:

```
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db = SQLAlchemy(app)
```

But, rather, in model.py (or equivalent):

```
db = SQLAlchemy()
```

and in your application.py (or equivalent):

```
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from yourapplication.model import db
    db.init_app(app)
```

Using this design pattern, no application-specific state is stored on the
extension object, so one extension object can be used for multiple apps.
For more information about the design of extensions refer to [Flask Extension Development](https://flask.palletsprojects.com/en/extensiondev/).

## Using Applications

To run such an application, you can use the **flask** command:

```
$ flask --app hello run
```

Flask will automatically detect the factory if it is named
`create_app` or `make_app` in `hello`. You can also pass arguments
to the factory like this:

```
$ flask --app 'hello:create_app(local_auth=True)' run
```

Then the `create_app` factory in `hello` is called with the keyword
argument `local_auth=True`. See [Command Line Interface](https://flask.palletsprojects.com/en/cli/) for more detail.

## Factory Improvements

The factory function above is not very clever, but you can improve it.
The following changes are straightforward to implement:

1. Make it possible to pass in configuration values for unit tests so that
  you don’t have to create config files on the filesystem.
2. Call a function from a blueprint when the application is setting up so
  that you have a place to modify attributes of the application (like
  hooking in before/after request handlers etc.)
3. Add in WSGI middlewares when the application is being created if necessary.

---

# Caching¶

# Caching

When your application runs slow, throw some caches in.  Well, at least
it’s the easiest way to speed up things.  What does a cache do?  Say you
have a function that takes some time to complete but the results would
still be good enough if they were 5 minutes old.  So then the idea is that
you actually put the result of that calculation into a cache for some
time.

Flask itself does not provide caching for you, but [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/), an
extension for Flask does. Flask-Caching supports various backends, and it is
even possible to develop your own caching backend.

---

# Background Tasks with Celery¶

# Background Tasks with Celery

If your application has a long running task, such as processing some uploaded data or
sending email, you don’t want to wait for it to finish during a request. Instead, use a
task queue to send the necessary data to another process that will run the task in the
background while the request returns immediately.

[Celery](https://celery.readthedocs.io) is a powerful task queue that can be used for simple background tasks as well
as complex multi-stage programs and schedules. This guide will show you how to configure
Celery using Flask. Read Celery’s [First Steps with Celery](https://celery.readthedocs.io/en/latest/getting-started/first-steps-with-celery.html) guide to learn how to use
Celery itself.

The Flask repository contains [an example](https://github.com/pallets/flask/tree/main/examples/celery)
based on the information on this page, which also shows how to use JavaScript to submit
tasks and poll for progress and results.

## Install

Install Celery from PyPI, for example using pip:

```
$ pip install celery
```

## Integrate Celery with Flask

You can use Celery without any integration with Flask, but it’s convenient to configure
it through Flask’s config, and to let tasks access the Flask application.

Celery uses similar ideas to Flask, with a `Celery` app object that has configuration
and registers tasks. While creating a Flask app, use the following code to create and
configure a Celery app as well.

```
from celery import Celery, Task

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
```

This creates and returns a `Celery` app object. Celery [configuration](https://celery.readthedocs.io/en/stable/userguide/configuration.html) is taken from
the `CELERY` key in the Flask configuration. The Celery app is set as the default, so
that it is seen during each request. The `Task` subclass automatically runs task
functions with a Flask app context active, so that services like your database
connections are available.

Here’s a basic `example.py` that configures Celery to use Redis for communication. We
enable a result backend, but ignore results by default. This allows us to store results
only for tasks where we care about the result.

```
from flask import Flask

app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)
```

Point the `celery worker` command at this and it will find the `celery_app` object.

```
$ celery -A example worker --loglevel INFO
```

You can also run the `celery beat` command to run tasks on a schedule. See Celery’s
docs for more information about defining schedules.

```
$ celery -A example beat --loglevel INFO
```

## Application Factory

When using the Flask application factory pattern, call the `celery_init_app` function
inside the factory. It sets `app.extensions["celery"]` to the Celery app object, which
can be used to get the Celery app from the Flask app returned by the factory.

```
def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app
```

To use `celery` commands, Celery needs an app object, but that’s no longer directly
available. Create a `make_celery.py` file that calls the Flask app factory and gets
the Celery app from the returned Flask app.

```
from example import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
```

Point the `celery` command to this file.

```
$ celery -A make_celery worker --loglevel INFO
$ celery -A make_celery beat --loglevel INFO
```

## Defining Tasks

Using `@celery_app.task` to decorate task functions requires access to the
`celery_app` object, which won’t be available when using the factory pattern. It also
means that the decorated tasks are tied to the specific Flask and Celery app instances,
which could be an issue during testing if you change configuration for a test.

Instead, use Celery’s `@shared_task` decorator. This creates task objects that will
access whatever the “current app” is, which is a similar concept to Flask’s blueprints
and app context. This is why we called `celery_app.set_default()` above.

Here’s an example task that adds two numbers together and returns the result.

```
from celery import shared_task

@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b
```

Earlier, we configured Celery to ignore task results by default. Since we want to know
the return value of this task, we set `ignore_result=False`. On the other hand, a task
that didn’t need a result, such as sending an email, wouldn’t set this.

## Calling Tasks

The decorated function becomes a task object with methods to call it in the background.
The simplest way is to use the `delay(*args, **kwargs)` method. See Celery’s docs for
more methods.

A Celery worker must be running to run the task. Starting a worker is shown in the
previous sections.

```
from flask import request

@app.post("/add")
def start_add() -> dict[str, object]:
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = add_together.delay(a, b)
    return {"result_id": result.id}
```

The route doesn’t get the task’s result immediately. That would defeat the purpose by
blocking the response. Instead, we return the running task’s result id, which we can use
later to get the result.

## Getting Results

To fetch the result of the task we started above, we’ll add another route that takes the
result id we returned before. We return whether the task is finished (ready), whether it
finished successfully, and what the return value (or error) was if it is finished.

```
from celery.result import AsyncResult

@app.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
```

Now you can start the task using the first route, then poll for the result using the
second route. This keeps the Flask request workers from being blocked waiting for tasks
to finish.

The Flask repository contains [an example](https://github.com/pallets/flask/tree/main/examples/celery)
using JavaScript to submit tasks and poll for progress and results.

## Passing Data to Tasks

The “add” task above took two integers as arguments. To pass arguments to tasks, Celery
has to serialize them to a format that it can pass to other processes. Therefore,
passing complex objects is not recommended. For example, it would be impossible to pass
a SQLAlchemy model object, since that object is probably not serializable and is tied to
the session that queried it.

Pass the minimal amount of data necessary to fetch or recreate any complex data within
the task. Consider a task that will run when the logged in user asks for an archive of
their data. The Flask request knows the logged in user, and has the user object queried
from the database. It got that by querying the database for a given id, so the task can
do the same thing. Pass the user’s id rather than the user object.

```
@shared_task
def generate_user_archive(user_id: str) -> None:
    user = db.session.get(User, user_id)
    ...

generate_user_archive.delay(current_user.id)
```

---

# Deferred Request Callbacks¶

# Deferred Request Callbacks

One of the design principles of Flask is that response objects are created and
passed down a chain of potential callbacks that can modify them or replace
them. When the request handling starts, there is no response object yet. It is
created as necessary either by a view function or by some other component in
the system.

What happens if you want to modify the response at a point where the response
does not exist yet?  A common example for that would be a
[before_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.before_request) callback that wants to set a cookie on the
response object.

One way is to avoid the situation. Very often that is possible. For instance
you can try to move that logic into a [after_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.after_request)
callback instead. However, sometimes moving code there makes it
more complicated or awkward to reason about.

As an alternative, you can use [after_this_request()](https://flask.palletsprojects.com/en/api/#flask.after_this_request) to register
callbacks that will execute after only the current request. This way you can
defer code execution from anywhere in the application, based on the current
request.

At any time during a request, we can register a function to be called at the
end of the request. For example you can remember the current language of the
user in a cookie in a [before_request()](https://flask.palletsprojects.com/en/api/#flask.Flask.before_request) callback:

```
from flask import request, after_this_request

@app.before_request
def detect_user_language():
    language = request.cookies.get('user_lang')

    if language is None:
        language = guess_language_from_request()

        # when the response exists, set a cookie with the language
        @after_this_request
        def remember_language(response):
            response.set_cookie('user_lang', language)
            return response

    g.language = language
```

---

# Adding a favicon¶

# Adding a favicon

A “favicon” is an icon used by browsers for tabs and bookmarks. This helps
to distinguish your website and to give it a unique brand.

A common question is how to add a favicon to a Flask application. First, of
course, you need an icon. It should be 16 × 16 pixels and in the ICO file
format. This is not a requirement but a de-facto standard supported by all
relevant browsers. Put the icon in your static directory as
`favicon.ico`.

Now, to get browsers to find your icon, the correct way is to add a link
tag in your HTML. So, for example:

```
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
```

That’s all you need for most browsers, however some really old ones do not
support this standard. The old de-facto standard is to serve this file,
with this name, at the website root. If your application is not mounted at
the root path of the domain you either need to configure the web server to
serve the icon at the root or if you can’t do that you’re out of luck. If
however your application is the root you can simply route a redirect:

```
app.add_url_rule(
    "/favicon.ico",
    endpoint="favicon",
    redirect_to=url_for("static", filename="favicon.ico"),
)
```

If you want to save the extra redirect request you can also write a view
using [send_from_directory()](https://flask.palletsprojects.com/en/api/#flask.send_from_directory):

```
import os
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
```

We can leave out the explicit mimetype and it will be guessed, but we may
as well specify it to avoid the extra guessing, as it will always be the
same.

The above will serve the icon via your application and if possible it’s
better to configure your dedicated web server to serve it; refer to the
web server’s documentation.

## See also

- The [Favicon](https://en.wikipedia.org/wiki/Favicon) article on
  Wikipedia

---

# Uploading Files¶

# Uploading Files

Ah yes, the good old problem of file uploads.  The basic idea of file
uploads is actually quite simple.  It basically works like this:

1. A `<form>` tag is marked with `enctype=multipart/form-data`
  and an `<input type=file>` is placed in that form.
2. The application accesses the file from the `files`
  dictionary on the request object.
3. use the [save()](https://werkzeug.palletsprojects.com/en/stable/datastructures/#werkzeug.datastructures.FileStorage.save) method of the file to save
  the file permanently somewhere on the filesystem.

## A Gentle Introduction

Let’s start with a very basic application that uploads a file to a
specific upload folder and displays a file to the user.  Let’s look at the
bootstrapping code for our application:

```
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
```

So first we need a couple of imports.  Most should be straightforward, the
`werkzeug.secure_filename()` is explained a little bit later.  The
`UPLOAD_FOLDER` is where we will store the uploaded files and the
`ALLOWED_EXTENSIONS` is the set of allowed file extensions.

Why do we limit the extensions that are allowed?  You probably don’t want
your users to be able to upload everything there if the server is directly
sending out the data to the client.  That way you can make sure that users
are not able to upload HTML files that would cause XSS problems (see
[Cross-Site Scripting (XSS)](https://flask.palletsprojects.com/en/web-security/#security-xss)).  Also make sure to disallow `.php` files if the server
executes them, but who has PHP installed on their server, right?  :)

Next the functions that check if an extension is valid and that uploads
the file and redirects the user to the URL for the uploaded file:

```
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
```

So what does that [secure_filename()](https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.utils.secure_filename) function actually do?
Now the problem is that there is that principle called “never trust user
input”.  This is also true for the filename of an uploaded file.  All
submitted form data can be forged, and filenames can be dangerous.  For
the moment just remember: always use that function to secure a filename
before storing it directly on the filesystem.

Information for the Pros

So you’re interested in what that [secure_filename()](https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.utils.secure_filename)
function does and what the problem is if you’re not using it?  So just
imagine someone would send the following information as `filename` to
your application:

```
filename = "../../../../home/username/.bashrc"
```

Assuming the number of `../` is correct and you would join this with
the `UPLOAD_FOLDER` the user might have the ability to modify a file on
the server’s filesystem he or she should not modify.  This does require some
knowledge about how the application looks like, but trust me, hackers
are patient :)

Now let’s look how that function works:

```
>>> secure_filename('../../../../home/username/.bashrc')
'home_username_.bashrc'
```

We want to be able to serve the uploaded files so they can be downloaded
by users. We’ll define a `download_file` view to serve files in the
upload folder by name. `url_for("download_file", name=name)` generates
download URLs.

```
from flask import send_from_directory

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
```

If you’re using middleware or the HTTP server to serve files, you can
register the `download_file` endpoint as `build_only` so `url_for`
will work without a view function.

```
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)
```

## Improving Uploads

  Changelog

Added in version 0.6.

So how exactly does Flask handle uploads?  Well it will store them in the
webserver’s memory if the files are reasonably small, otherwise in a
temporary location (as returned by [tempfile.gettempdir()](https://docs.python.org/3/library/tempfile.html#tempfile.gettempdir)).  But how
do you specify the maximum file size after which an upload is aborted?  By
default Flask will happily accept file uploads with an unlimited amount of
memory, but you can limit that by setting the `MAX_CONTENT_LENGTH`
config key:

```
from flask import Flask, Request

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
```

The code above will limit the maximum allowed payload to 16 megabytes.
If a larger file is transmitted, Flask will raise a
[RequestEntityTooLarge](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.RequestEntityTooLarge) exception.

Connection Reset Issue

When using the local development server, you may get a connection
reset error instead of a 413 response. You will get the correct
status response when running the app with a production WSGI server.

This feature was added in Flask 0.6 but can be achieved in older versions
as well by subclassing the request object.  For more information on that
consult the Werkzeug documentation on file handling.

## Upload Progress Bars

A while ago many developers had the idea to read the incoming file in
small chunks and store the upload progress in the database to be able to
poll the progress with JavaScript from the client. The client asks the
server every 5 seconds how much it has transmitted, but this is
something it should already know.

## An Easier Solution

Now there are better solutions that work faster and are more reliable. There
are JavaScript libraries like [jQuery](https://jquery.com/) that have form plugins to ease the
construction of progress bar.

Because the common pattern for file uploads exists almost unchanged in all
applications dealing with uploads, there are also some Flask extensions that
implement a full fledged upload mechanism that allows controlling which
file extensions are allowed to be uploaded.

---

# Message Flashing¶

# Message Flashing

Good applications and user interfaces are all about feedback.  If the user
does not get enough feedback they will probably end up hating the
application.  Flask provides a really simple way to give feedback to a
user with the flashing system.  The flashing system basically makes it
possible to record a message at the end of a request and access it next
request and only next request.  This is usually combined with a layout
template that does this. Note that browsers and sometimes web servers enforce
a limit on cookie sizes. This means that flashing messages that are too
large for session cookies causes message flashing to fail silently.

## Simple Flashing

So here is a full example:

```
from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)
```

And here is the `layout.html` template which does the magic:

```
<!doctype html>
<title>My Application</title>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul class=flashes>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
{% block body %}{% endblock %}
```

Here is the `index.html` template which inherits from `layout.html`:

```
{% extends "layout.html" %}
{% block body %}
  <h1>Overview</h1>
  <p>Do you want to <a href="{{ url_for('login') }}">log in?</a>
{% endblock %}
```

And here is the `login.html` template which also inherits from
`layout.html`:

```
{% extends "layout.html" %}
{% block body %}
  <h1>Login</h1>
  {% if error %}
    <p class=error><strong>Error:</strong> {{ error }}
  {% endif %}
  <form method=post>
    <dl>
      <dt>Username:
      <dd><input type=text name=username value="{{
          request.form.username }}">
      <dt>Password:
      <dd><input type=password name=password>
    </dl>
    <p><input type=submit value=Login>
  </form>
{% endblock %}
```

## Flashing With Categories

  Changelog

Added in version 0.3.

It is also possible to provide categories when flashing a message.  The
default category if nothing is provided is `'message'`.  Alternative
categories can be used to give the user better feedback.  For example
error messages could be displayed with a red background.

To flash a message with a different category, just use the second argument
to the [flash()](https://flask.palletsprojects.com/en/api/#flask.flash) function:

```
flash('Invalid password provided', 'error')
```

Inside the template you then have to tell the
[get_flashed_messages()](https://flask.palletsprojects.com/en/api/#flask.get_flashed_messages) function to also return the
categories.  The loop looks slightly different in that situation then:

```
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul class=flashes>
    {% for category, message in messages %}
      <li class="{{ category }}">{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
```

This is just one example of how to render these flashed messages.  One
might also use the category to add a prefix such as
`<strong>Error:</strong>` to the message.

## Filtering Flash Messages

  Changelog

Added in version 0.9.

Optionally you can pass a list of categories which filters the results of
[get_flashed_messages()](https://flask.palletsprojects.com/en/api/#flask.get_flashed_messages).  This is useful if you wish to
render each category in a separate block.

```
{% with errors = get_flashed_messages(category_filter=["error"]) %}
{% if errors %}
<div class="alert-message block-message error">
  <a class="close" href="#">×</a>
  <ul>
    {%- for msg in errors %}
    <li>{{ msg }}</li>
    {% endfor -%}
  </ul>
</div>
{% endif %}
{% endwith %}
```

---

# JavaScript,fetch, and JSON¶

# JavaScript,fetch, and JSON

You may want to make your HTML page dynamic, by changing data without
reloading the entire page. Instead of submitting an HTML `<form>` and
performing a redirect to re-render the template, you can add
[JavaScript](https://developer.mozilla.org/Web/JavaScript) that calls [fetch()](https://developer.mozilla.org/Web/API/Fetch_API) and replaces content on the page.

[fetch()](https://developer.mozilla.org/Web/API/Fetch_API) is the modern, built-in JavaScript solution to making
requests from a page. You may have heard of other “AJAX” methods and
libraries, such as [XMLHttpRequest()](https://developer.mozilla.org/Web/API/XMLHttpRequest) or [jQuery](https://jquery.com/). These are no longer needed in
modern browsers, although you may choose to use them or another library
depending on your application’s requirements. These docs will only focus
on built-in JavaScript features.

## Rendering Templates

It is important to understand the difference between templates and
JavaScript. Templates are rendered on the server, before the response is
sent to the user’s browser. JavaScript runs in the user’s browser, after
the template is rendered and sent. Therefore, it is impossible to use
JavaScript to affect how the Jinja template is rendered, but it is
possible to render data into the JavaScript that will run.

To provide data to JavaScript when rendering the template, use the
[tojson()](https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.tojson) filter in a `<script>` block. This will
convert the data to a valid JavaScript object, and ensure that any
unsafe HTML characters are rendered safely. If you do not use the
`tojson` filter, you will get a `SyntaxError` in the browser
console.

```
data = generate_report()
return render_template("report.html", chart_data=data)
```

```
<script>
    const chart_data = {{ chart_data|tojson }}
    chartLib.makeChart(chart_data)
</script>
```

A less common pattern is to add the data to a `data-` attribute on an
HTML tag. In this case, you must use single quotes around the value, not
double quotes, otherwise you will produce invalid or unsafe HTML.

```
<div data-chart='{{ chart_data|tojson }}'></div>
```

## Generating URLs

The other way to get data from the server to JavaScript is to make a
request for it. First, you need to know the URL to request.

The simplest way to generate URLs is to continue to use
[url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for) when rendering the template. For example:

```
const user_url = {{ url_for("user", id=current_user.id)|tojson }}
fetch(user_url).then(...)
```

However, you might need to generate a URL based on information you only
know in JavaScript. As discussed above, JavaScript runs in the user’s
browser, not as part of the template rendering, so you can’t use
`url_for` at that point.

In this case, you need to know the “root URL” under which your
application is served. In simple setups, this is `/`, but it might
also be something else, like `https://example.com/myapp/`.

A simple way to tell your JavaScript code about this root is to set it
as a global variable when rendering the template. Then you can use it
when generating URLs from JavaScript.

```
const SCRIPT_ROOT = {{ request.script_root|tojson }}
let user_id = ...  // do something to get a user id from the page
let user_url = `${SCRIPT_ROOT}/user/${user_id}`
fetch(user_url).then(...)
```

## Making a Request withfetch

[fetch()](https://developer.mozilla.org/Web/API/Fetch_API) takes two arguments, a URL and an object with other options,
and returns a [Promise](https://developer.mozilla.org/Web/JavaScript/Reference/Global_Objects/Promise). We won’t cover all the available options, and
will only use `then()` on the promise, not other callbacks or
`await` syntax. Read the linked MDN docs for more information about
those features.

By default, the GET method is used. If the response contains JSON, it
can be used with a `then()` callback chain.

```
const room_url = {{ url_for("room_detail", id=room.id)|tojson }}
fetch(room_url)
    .then(response => response.json())
    .then(data => {
        // data is a parsed JSON object
    })
```

To send data, use a data method such as POST, and pass the `body`
option. The most common types for data are form data or JSON data.

To send form data, pass a populated [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) object. This uses the
same format as an HTML form, and would be accessed with `request.form`
in a Flask view.

```
let data = new FormData()
data.append("name", "Flask Room")
data.append("description", "Talk about Flask here.")
fetch(room_url, {
    "method": "POST",
    "body": data,
}).then(...)
```

In general, prefer sending request data as form data, as would be used
when submitting an HTML form. JSON can represent more complex data, but
unless you need that it’s better to stick with the simpler format. When
sending JSON data, the `Content-Type: application/json` header must be
sent as well, otherwise Flask will return a 415 Unsupported Media Type
error.

```
let data = {
    "name": "Flask Room",
    "description": "Talk about Flask here.",
}
fetch(room_url, {
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": JSON.stringify(data),
}).then(...)
```

## Following Redirects

A response might be a redirect, for example if you logged in with
JavaScript instead of a traditional HTML form, and your view returned
a redirect instead of JSON. JavaScript requests do follow redirects, but
they don’t change the page. If you want to make the page change you can
inspect the response and apply the redirect manually.

```
fetch("/login", {"body": ...}).then(
    response => {
        if (response.redirected) {
            window.location = response.url
        } else {
            showLoginError()
        }
    }
)
```

## Replacing Content

A response might be new HTML, either a new section of the page to add or
replace, or an entirely new page. In general, if you’re returning the
entire page, it would be better to handle that with a redirect as shown
in the previous section. The following example shows how to replace a
`<div>` with the HTML returned by a request.

```
<div id="geology-fact">
    {{ include "geology_fact.html" }}
</div>
<script>
    const geology_url = {{ url_for("geology_fact")|tojson }}
    const geology_div = getElementById("geology-fact")
    fetch(geology_url)
        .then(response => response.text)
        .then(text => geology_div.innerHTML = text)
</script>
```

## Return JSON from Views

To return a JSON object from your API view, you can directly return a
dict from the view. It will be serialized to JSON automatically.

```
@app.route("/user/<int:id>")
def user_detail(id):
    user = User.query.get_or_404(id)
    return {
        "username": User.username,
        "email": User.email,
        "picture": url_for("static", filename=f"users/{id}/profile.png"),
    }
```

If you want to return another JSON type, use the
[jsonify()](https://flask.palletsprojects.com/en/api/#flask.json.jsonify) function, which creates a response object
with the given data serialized to JSON.

```
from flask import jsonify

@app.route("/users")
def user_list():
    users = User.query.order_by(User.name).all()
    return jsonify([u.to_json() for u in users])
```

It is usually not a good idea to return file data in a JSON response.
JSON cannot represent binary data directly, so it must be base64
encoded, which can be slow, takes more bandwidth to send, and is not as
easy to cache. Instead, serve files using one view, and generate a URL
to the desired file to include in the JSON. Then the client can make a
separate request to get the linked resource after getting the JSON.

## Receiving JSON in Views

Use the [json](https://flask.palletsprojects.com/en/api/#flask.Request.json) property of the
[request](https://flask.palletsprojects.com/en/api/#flask.request) object to decode the request’s body as JSON. If
the body is not valid JSON, a 400 Bad Request error will be raised. If
the `Content-Type` header is not set to `application/json`, a 415
Unsupported Media Type error will be raised.

```
from flask import request

@app.post("/user/<int:id>")
def user_update(id):
    user = User.query.get_or_404(id)
    user.update_from_json(request.json)
    db.session.commit()
    return user.to_json()
```
