# Blog Blueprint¶ and more

# Blog Blueprint¶

# Blog Blueprint

You’ll use the same techniques you learned about when writing the
authentication blueprint to write the blog blueprint. The blog should
list all posts, allow logged in users to create posts, and allow the
author of a post to edit or delete it.

As you implement each view, keep the development server running. As you
save your changes, try going to the URL in your browser and testing them
out.

## The Blueprint

Define the blueprint and register it in the application factory.

  `flaskr/blog.py`

```
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)
```

Import and register the blueprint from the factory using
[app.register_blueprint()](https://flask.palletsprojects.com/en/api/#flask.Flask.register_blueprint). Place the
new code at the end of the factory function before returning the app.

  `flaskr/__init__.py`

```
def create_app():
    app = ...
    # existing code omitted

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
```

Unlike the auth blueprint, the blog blueprint does not have a
`url_prefix`. So the `index` view will be at `/`, the `create`
view at `/create`, and so on. The blog is the main feature of Flaskr,
so it makes sense that the blog index will be the main index.

However, the endpoint for the `index` view defined below will be
`blog.index`. Some of the authentication views referred to a plain
`index` endpoint. [app.add_url_rule()](https://flask.palletsprojects.com/en/api/#flask.Flask.add_url_rule)
associates the endpoint name `'index'` with the `/` url so that
`url_for('index')` or `url_for('blog.index')` will both work,
generating the same `/` URL either way.

In another application you might give the blog blueprint a
`url_prefix` and define a separate `index` view in the application
factory, similar to the `hello` view. Then the `index` and
`blog.index` endpoints and URLs would be different.

## Index

The index will show all of the posts, most recent first. A `JOIN` is
used so that the author information from the `user` table is
available in the result.

  `flaskr/blog.py`

```
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)
```

    `flaskr/templates/blog/index.html`

```
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Posts{% endblock %}</h1>
  {% if g.user %}
    <a class="action" href="{{ url_for('blog.create') }}">New</a>
  {% endif %}
{% endblock %}

{% block content %}
  {% for post in posts %}
    <article class="post">
      <header>
        <div>
          <h1>{{ post['title'] }}</h1>
          <div class="about">by {{ post['username'] }} on {{ post['created'].strftime('%Y-%m-%d') }}</div>
        </div>
        {% if g.user['id'] == post['author_id'] %}
          <a class="action" href="{{ url_for('blog.update', id=post['id']) }}">Edit</a>
        {% endif %}
      </header>
      <p class="body">{{ post['body'] }}</p>
    </article>
    {% if not loop.last %}
      <hr>
    {% endif %}
  {% endfor %}
{% endblock %}
```

When a user is logged in, the `header` block adds a link to the
`create` view. When the user is the author of a post, they’ll see an
“Edit” link to the `update` view for that post. `loop.last` is a
special variable available inside [Jinja for loops](https://jinja.palletsprojects.com/templates/#for). It’s used to
display a line after each post except the last one, to visually separate
them.

## Create

The `create` view works the same as the auth `register` view. Either
the form is displayed, or the posted data is validated and the post is
added to the database or an error is shown.

The `login_required` decorator you wrote earlier is used on the blog
views. A user must be logged in to visit these views, otherwise they
will be redirected to the login page.

  `flaskr/blog.py`

```
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
```

    `flaskr/templates/blog/create.html`

```
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}New Post{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="title">Title</label>
    <input name="title" id="title" value="{{ request.form['title'] }}" required>
    <label for="body">Body</label>
    <textarea name="body" id="body">{{ request.form['body'] }}</textarea>
    <input type="submit" value="Save">
  </form>
{% endblock %}
```

## Update

Both the `update` and `delete` views will need to fetch a `post`
by `id` and check if the author matches the logged in user. To avoid
duplicating code, you can write a function to get the `post` and call
it from each view.

  `flaskr/blog.py`

```
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
```

[abort()](https://flask.palletsprojects.com/en/api/#flask.abort) will raise a special exception that returns an HTTP status
code. It takes an optional message to show with the error, otherwise a
default message is used. `404` means “Not Found”, and `403` means
“Forbidden”. (`401` means “Unauthorized”, but you redirect to the
login page instead of returning that status.)

The `check_author` argument is defined so that the function can be
used to get a `post` without checking the author. This would be useful
if you wrote a view to show an individual post on a page, where the user
doesn’t matter because they’re not modifying the post.

  `flaskr/blog.py`

```
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)
```

Unlike the views you’ve written so far, the `update` function takes
an argument, `id`. That corresponds to the `<int:id>` in the route.
A real URL will look like `/1/update`. Flask will capture the `1`,
ensure it’s an [int](https://docs.python.org/3/library/functions.html#int), and pass it as the `id` argument. If you
don’t specify `int:` and instead do `<id>`, it will be a string.
To generate a URL to the update page, [url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for) needs to be passed
the `id` so it knows what to fill in:
`url_for('blog.update', id=post['id'])`. This is also in the
`index.html` file above.

The `create` and `update` views look very similar. The main
difference is that the `update` view uses a `post` object and an
`UPDATE` query instead of an `INSERT`. With some clever refactoring,
you could use one view and template for both actions, but for the
tutorial it’s clearer to keep them separate.

  `flaskr/templates/blog/update.html`

```
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Edit "{{ post['title'] }}"{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="title">Title</label>
    <input name="title" id="title"
      value="{{ request.form['title'] or post['title'] }}" required>
    <label for="body">Body</label>
    <textarea name="body" id="body">{{ request.form['body'] or post['body'] }}</textarea>
    <input type="submit" value="Save">
  </form>
  <hr>
  <form action="{{ url_for('blog.delete', id=post['id']) }}" method="post">
    <input class="danger" type="submit" value="Delete" onclick="return confirm('Are you sure?');">
  </form>
{% endblock %}
```

This template has two forms. The first posts the edited data to the
current page (`/<id>/update`). The other form contains only a button
and specifies an `action` attribute that posts to the delete view
instead. The button uses some JavaScript to show a confirmation dialog
before submitting.

The pattern `{{ request.form['title'] or post['title'] }}` is used to
choose what data appears in the form. When the form hasn’t been
submitted, the original `post` data appears, but if invalid form data
was posted you want to display that so the user can fix the error, so
`request.form` is used instead. [request](https://flask.palletsprojects.com/en/api/#flask.request) is another variable
that’s automatically available in templates.

## Delete

The delete view doesn’t have its own template, the delete button is part
of `update.html` and posts to the `/<id>/delete` URL. Since there
is no template, it will only handle the `POST` method and then redirect
to the `index` view.

  `flaskr/blog.py`

```
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
```

Congratulations, you’ve now finished writing your application! Take some
time to try out everything in the browser. However, there’s still more
to do before the project is complete.

Continue to [Make the Project Installable](https://flask.palletsprojects.com/en/stable/install/).

---

# Define and Access the Database¶

# Define and Access the Database

The application will use a [SQLite](https://sqlite.org/about.html) database to store users and posts.
Python comes with built-in support for SQLite in the [sqlite3](https://docs.python.org/3/library/sqlite3.html#module-sqlite3)
module.

SQLite is convenient because it doesn’t require setting up a separate
database server and is built-in to Python. However, if concurrent
requests try to write to the database at the same time, they will slow
down as each write happens sequentially. Small applications won’t notice
this. Once you become big, you may want to switch to a different
database.

The tutorial doesn’t go into detail about SQL. If you are not familiar
with it, the SQLite docs describe the [language](https://sqlite.org/lang.html).

## Connect to the Database

The first thing to do when working with a SQLite database (and most
other Python database libraries) is to create a connection to it. Any
queries and operations are performed using the connection, which is
closed after the work is finished.

In web applications this connection is typically tied to the request. It
is created at some point when handling a request, and closed before the
response is sent.

  `flaskr/db.py`

```
import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
```

[g](https://flask.palletsprojects.com/en/api/#flask.g) is a special object that is unique for each request. It is
used to store data that might be accessed by multiple functions during
the request. The connection is stored and reused instead of creating a
new connection if `get_db` is called a second time in the same
request.

[current_app](https://flask.palletsprojects.com/en/api/#flask.current_app) is another special object that points to the Flask
application handling the request. Since you used an application factory,
there is no application object when writing the rest of your code.
`get_db` will be called when the application has been created and is
handling a request, so [current_app](https://flask.palletsprojects.com/en/api/#flask.current_app) can be used.

[sqlite3.connect()](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect) establishes a connection to the file pointed at
by the `DATABASE` configuration key. This file doesn’t have to exist
yet, and won’t until you initialize the database later.

[sqlite3.Row](https://docs.python.org/3/library/sqlite3.html#sqlite3.Row) tells the connection to return rows that behave
like dicts. This allows accessing the columns by name.

`close_db` checks if a connection was created by checking if `g.db`
was set. If the connection exists, it is closed. Further down you will
tell your application about the `close_db` function in the application
factory so that it is called after each request.

## Create the Tables

In SQLite, data is stored in *tables* and *columns*. These need to be
created before you can store and retrieve data. Flaskr will store users
in the `user` table, and posts in the `post` table. Create a file
with the SQL commands needed to create empty tables:

  `flaskr/schema.sql`

```
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
```

Add the Python functions that will run these SQL commands to the
`db.py` file:

  `flaskr/db.py`

```
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
```

[open_resource()](https://flask.palletsprojects.com/en/api/#flask.Flask.open_resource) opens a file relative to
the `flaskr` package, which is useful since you won’t necessarily know
where that location is when deploying the application later. `get_db`
returns a database connection, which is used to execute the commands
read from the file.

[click.command()](https://click.palletsprojects.com/en/stable/api/#click.command) defines a command line command called `init-db`
that calls the `init_db` function and shows a success message to the
user. You can read [Command Line Interface](https://flask.palletsprojects.com/en/cli/) to learn more about writing commands.

The call to [sqlite3.register_converter()](https://docs.python.org/3/library/sqlite3.html#sqlite3.register_converter) tells Python how to
interpret timestamp values in the database. We convert the value to a
[datetime.datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime).

## Register with the Application

The `close_db` and `init_db_command` functions need to be registered
with the application instance; otherwise, they won’t be used by the
application. However, since you’re using a factory function, that
instance isn’t available when writing the functions. Instead, write a
function that takes an application and does the registration.

  `flaskr/db.py`

```
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
```

[app.teardown_appcontext()](https://flask.palletsprojects.com/en/api/#flask.Flask.teardown_appcontext) tells
Flask to call that function when cleaning up after returning the
response.

[app.cli.add_command()](https://click.palletsprojects.com/en/stable/api/#click.Group.add_command) adds a new
command that can be called with the `flask` command.

Import and call this function from the factory. Place the new code at
the end of the factory function before returning the app.

  `flaskr/__init__.py`

```
def create_app():
    app = ...
    # existing code omitted

    from . import db
    db.init_app(app)

    return app
```

## Initialize the Database File

Now that `init-db` has been registered with the app, it can be called
using the `flask` command, similar to the `run` command from the
previous page.

Note

If you’re still running the server from the previous page, you can
either stop the server, or run this command in a new terminal. If
you use a new terminal, remember to change to your project directory
and activate the env as described in [Installation](https://flask.palletsprojects.com/en/installation/).

Run the `init-db` command:

```
$ flask --app flaskr init-db
Initialized the database.
```

There will now be a `flaskr.sqlite` file in the `instance` folder in
your project.

Continue to [Blueprints and Views](https://flask.palletsprojects.com/en/stable/views/).

---

# Deploy to Production¶

# Deploy to Production

This part of the tutorial assumes you have a server that you want to
deploy your application to. It gives an overview of how to create the
distribution file and install it, but won’t go into specifics about
what server or software to use. You can set up a new environment on your
development computer to try out the instructions below, but probably
shouldn’t use it for hosting a real public application. See
[Deploying to Production](https://flask.palletsprojects.com/en/deploying/) for a list of many different ways to host your
application.

## Build and Install

When you want to deploy your application elsewhere, you build a *wheel*
(`.whl`) file. Install and use the `build` tool to do this.

```
$ pip install build
$ python -m build --wheel
```

You can find the file in `dist/flaskr-1.0.0-py3-none-any.whl`. The
file name is in the format of {project name}-{version}-{python tag}
-{abi tag}-{platform tag}.

Copy this file to another machine,
[set up a new virtualenv](https://flask.palletsprojects.com/en/installation/#install-create-env), then install the
file with `pip`.

```
$ pip install flaskr-1.0.0-py3-none-any.whl
```

Pip will install your project along with its dependencies.

Since this is a different machine, you need to run `init-db` again to
create the database in the instance folder.

> ```
> $ flask --app flaskr init-db
> ```

When Flask detects that it’s installed (not in editable mode), it uses
a different directory for the instance folder. You can find it at
`.venv/var/flaskr-instance` instead.

## Configure the Secret Key

In the beginning of the tutorial that you gave a default value for
[SECRET_KEY](https://flask.palletsprojects.com/en/config/#SECRET_KEY). This should be changed to some random bytes in
production. Otherwise, attackers could use the public `'dev'` key to
modify the session cookie, or anything else that uses the secret key.

You can use the following command to output a random secret key:

```
$ python -c 'import secrets; print(secrets.token_hex())'

'192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```

Create the `config.py` file in the instance folder, which the factory
will read from if it exists. Copy the generated value into it.

  `.venv/var/flaskr-instance/config.py`

```
SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```

You can also set any other necessary configuration here, although
`SECRET_KEY` is the only one needed for Flaskr.

## Run with a Production Server

When running publicly rather than in development, you should not use the
built-in development server (`flask run`). The development server is
provided by Werkzeug for convenience, but is not designed to be
particularly efficient, stable, or secure.

Instead, use a production WSGI server. For example, to use [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/),
first install it in the virtual environment:

```
$ pip install waitress
```

You need to tell Waitress about your application, but it doesn’t use
`--app` like `flask run` does. You need to tell it to import and
call the application factory to get an application object.

```
$ waitress-serve --call 'flaskr:create_app'

Serving on http://0.0.0.0:8080
```

See [Deploying to Production](https://flask.palletsprojects.com/en/deploying/) for a list of many different ways to host
your application. Waitress is just an example, chosen for the tutorial
because it supports both Windows and Linux. There are many more WSGI
servers and deployment options that you may choose for your project.

Continue to [Keep Developing!](https://flask.palletsprojects.com/en/stable/next/).

---

# Application Setup¶

# Application Setup

A Flask application is an instance of the [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) class.
Everything about the application, such as configuration and URLs, will
be registered with this class.

The most straightforward way to create a Flask application is to create
a global [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) instance directly at the top of your code, like
how the “Hello, World!” example did on the previous page. While this is
simple and useful in some cases, it can cause some tricky issues as the
project grows.

Instead of creating a [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) instance globally, you will create
it inside a function. This function is known as the *application
factory*. Any configuration, registration, and other setup the
application needs will happen inside the function, then the application
will be returned.

## The Application Factory

It’s time to start coding! Create the `flaskr` directory and add the
`__init__.py` file. The `__init__.py` serves double duty: it will
contain the application factory, and it tells Python that the `flaskr`
directory should be treated as a package.

```
$ mkdir flaskr
```

   `flaskr/__init__.py`

```
import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
```

`create_app` is the application factory function. You’ll add to it
later in the tutorial, but it already does a lot.

1. `app = Flask(__name__, instance_relative_config=True)` creates the
  [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) instance.
  - `__name__` is the name of the current Python module. The app
    needs to know where it’s located to set up some paths, and
    `__name__` is a convenient way to tell it that.
  - `instance_relative_config=True` tells the app that
    configuration files are relative to the
    [instance folder](https://flask.palletsprojects.com/en/config/#instance-folders). The instance folder
    is located outside the `flaskr` package and can hold local
    data that shouldn’t be committed to version control, such as
    configuration secrets and the database file.
2. [app.config.from_mapping()](https://flask.palletsprojects.com/en/api/#flask.Config.from_mapping) sets
  some default configuration that the app will use:
  - [SECRET_KEY](https://flask.palletsprojects.com/en/config/#SECRET_KEY) is used by Flask and extensions to keep data
    safe. It’s set to `'dev'` to provide a convenient value
    during development, but it should be overridden with a random
    value when deploying.
  - `DATABASE` is the path where the SQLite database file will be
    saved. It’s under
    [app.instance_path](https://flask.palletsprojects.com/en/api/#flask.Flask.instance_path), which is the
    path that Flask has chosen for the instance folder. You’ll learn
    more about the database in the next section.
3. [app.config.from_pyfile()](https://flask.palletsprojects.com/en/api/#flask.Config.from_pyfile) overrides
  the default configuration with values taken from the `config.py`
  file in the instance folder if it exists. For example, when
  deploying, this can be used to set a real `SECRET_KEY`.
  - `test_config` can also be passed to the factory, and will be
    used instead of the instance configuration. This is so the tests
    you’ll write later in the tutorial can be configured
    independently of any development values you have configured.
4. [os.makedirs()](https://docs.python.org/3/library/os.html#os.makedirs) ensures that
  [app.instance_path](https://flask.palletsprojects.com/en/api/#flask.Flask.instance_path) exists. Flask
  doesn’t create the instance folder automatically, but it needs to be
  created because your project will create the SQLite database file
  there.
5. [@app.route()](https://flask.palletsprojects.com/en/api/#flask.Flask.route) creates a simple route so you can
  see the application working before getting into the rest of the
  tutorial. It creates a connection between the URL `/hello` and a
  function that returns a response, the string `'Hello, World!'` in
  this case.

## Run The Application

Now you can run your application using the `flask` command. From the
terminal, tell Flask where to find your application, then run it in
debug mode. Remember, you should still be in the top-level
`flask-tutorial` directory, not the `flaskr` package.

Debug mode shows an interactive debugger whenever a page raises an
exception, and restarts the server whenever you make changes to the
code. You can leave it running and just reload the browser page as you
follow the tutorial.

```
$ flask --app flaskr run --debug
```

You’ll see output similar to this:

```
* Serving Flask app "flaskr"
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: nnn-nnn-nnn
```

Visit [http://127.0.0.1:5000/hello](http://127.0.0.1:5000/hello) in a browser and you should see the
“Hello, World!” message. Congratulations, you’re now running your Flask
web application!

If another program is already using port 5000, you’ll see
`OSError: [Errno 98]` or `OSError: [WinError 10013]` when the
server tries to start. See [Address already in use](https://flask.palletsprojects.com/en/server/#address-already-in-use) for how to
handle that.

Continue to [Define and Access the Database](https://flask.palletsprojects.com/en/stable/database/).

---

# Make the Project Installable¶

# Make the Project Installable

Making your project installable means that you can build a *wheel* file and install that
in another environment, just like you installed Flask in your project’s environment.
This makes deploying your project the same as installing any other library, so you’re
using all the standard Python tools to manage everything.

Installing also comes with other benefits that might not be obvious from
the tutorial or as a new Python user, including:

- Currently, Python and Flask understand how to use the `flaskr`
  package only because you’re running from your project’s directory.
  Installing means you can import it no matter where you run from.
- You can manage your project’s dependencies just like other packages
  do, so `pip install yourproject.whl` installs them.
- Test tools can isolate your test environment from your development
  environment.

Note

This is being introduced late in the tutorial, but in your future
projects you should always start with this.

## Describe the Project

The `pyproject.toml` file describes your project and how to build it.

  `pyproject.toml`

```
[project]
name = "flaskr"
version = "1.0.0"
description = "The basic blog app built in the Flask tutorial."
dependencies = [
    "flask",
]

[build-system]
requires = ["flit_core<4"]
build-backend = "flit_core.buildapi"
```

See the official [Packaging tutorial](https://packaging.python.org/tutorials/packaging-projects/) for more
explanation of the files and options used.

## Install the Project

Use `pip` to install your project in the virtual environment.

```
$ pip install -e .
```

This tells pip to find `pyproject.toml` in the current directory and install the
project in *editable* or *development* mode. Editable mode means that as you make
changes to your local code, you’ll only need to re-install if you change the metadata
about the project, such as its dependencies.

You can observe that the project is now installed with `pip list`.

```
$ pip list

Package        Version   Location
-------------- --------- ----------------------------------
click          6.7
Flask          1.0
flaskr         1.0.0     /home/user/Projects/flask-tutorial
itsdangerous   0.24
Jinja2         2.10
MarkupSafe     1.0
pip            9.0.3
Werkzeug       0.14.1
```

Nothing changes from how you’ve been running your project so far.
`--app` is still set to `flaskr` and `flask run` still runs
the application, but you can call it from anywhere, not just the
`flask-tutorial` directory.

Continue to [Test Coverage](https://flask.palletsprojects.com/en/stable/tests/).

---

# Project Layout¶

# Project Layout

Create a project directory and enter it:

```
$ mkdir flask-tutorial
$ cd flask-tutorial
```

Then follow the [installation instructions](https://flask.palletsprojects.com/en/installation/) to set
up a Python virtual environment and install Flask for your project.

The tutorial will assume you’re working from the `flask-tutorial`
directory from now on. The file names at the top of each code block are
relative to this directory.

---

A Flask application can be as simple as a single file.

  `hello.py`

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
```

However, as a project gets bigger, it becomes overwhelming to keep all
the code in one file. Python projects use *packages* to organize code
into multiple modules that can be imported where needed, and the
tutorial will do this as well.

The project directory will contain:

- `flaskr/`, a Python package containing your application code and
  files.
- `tests/`, a directory containing test modules.
- `.venv/`, a Python virtual environment where Flask and other
  dependencies are installed.
- Installation files telling Python how to install your project.
- Version control config, such as [git](https://git-scm.com/). You should make a habit of
  using some type of version control for all your projects, no matter
  the size.
- Any other project files you might add in the future.

By the end, your project layout will look like this:

```
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── .venv/
├── pyproject.toml
└── MANIFEST.in
```

If you’re using version control, the following files that are generated
while running your project should be ignored. There may be other files
based on the editor you use. In general, ignore files that you didn’t
write. For example, with git:

  `.gitignore`

```
.venv/

*.pyc
__pycache__/

instance/

.pytest_cache/
.coverage
htmlcov/

dist/
build/
*.egg-info/
```

Continue to [Application Setup](https://flask.palletsprojects.com/en/stable/factory/).

---

# Keep Developing!¶

# Keep Developing!

You’ve learned about quite a few Flask and Python concepts throughout
the tutorial. Go back and review the tutorial and compare your code with
the steps you took to get there. Compare your project to the
[example project](https://github.com/pallets/flask/tree/3.1.2/examples/tutorial), which might look a bit
different due to the step-by-step nature of the tutorial.

There’s a lot more to Flask than what you’ve seen so far. Even so,
you’re now equipped to start developing your own web applications. Check
out the [Quickstart](https://flask.palletsprojects.com/en/quickstart/) for an overview of what Flask can do, then
dive into the docs to keep learning. Flask uses [Jinja](https://palletsprojects.com/p/jinja/), [Click](https://palletsprojects.com/p/click/),
[Werkzeug](https://palletsprojects.com/p/werkzeug/), and [ItsDangerous](https://palletsprojects.com/p/itsdangerous/) behind the scenes, and they all have
their own documentation too. You’ll also be interested in
[Extensions](https://flask.palletsprojects.com/en/extensions/) which make tasks like working with the database or
validating form data easier and more powerful.

If you want to keep developing your Flaskr project, here are some ideas
for what to try next:

- A detail view to show a single post. Click a post’s title to go to
  its page.
- Like / unlike a post.
- Comments.
- Tags. Clicking a tag shows all the posts with that tag.
- A search box that filters the index page by name.
- Paged display. Only show 5 posts per page.
- Upload an image to go along with a post.
- Format posts using Markdown.
- An RSS feed of new posts.

Have fun and make awesome applications!

---

# Static Files¶

# Static Files

The authentication views and templates work, but they look very plain
right now. Some [CSS](https://developer.mozilla.org/docs/Web/CSS) can be added to add style to the HTML layout you
constructed. The style won’t change, so it’s a *static* file rather than
a template.

Flask automatically adds a `static` view that takes a path relative
to the `flaskr/static` directory and serves it. The `base.html`
template already has a link to the `style.css` file:

```
{{ url_for('static', filename='style.css') }}
```

Besides CSS, other types of static files might be files with JavaScript
functions, or a logo image. They are all placed under the
`flaskr/static` directory and referenced with
`url_for('static', filename='...')`.

This tutorial isn’t focused on how to write CSS, so you can just copy
the following into the `flaskr/static/style.css` file:

  `flaskr/static/style.css`

```
html { font-family: sans-serif; background: #eee; padding: 1rem; }
body { max-width: 960px; margin: 0 auto; background: white; }
h1 { font-family: serif; color: #377ba8; margin: 1rem 0; }
a { color: #377ba8; }
hr { border: none; border-top: 1px solid lightgray; }
nav { background: lightgray; display: flex; align-items: center; padding: 0 0.5rem; }
nav h1 { flex: auto; margin: 0; }
nav h1 a { text-decoration: none; padding: 0.25rem 0.5rem; }
nav ul  { display: flex; list-style: none; margin: 0; padding: 0; }
nav ul li a, nav ul li span, header .action { display: block; padding: 0.5rem; }
.content { padding: 0 1rem 1rem; }
.content > header { border-bottom: 1px solid lightgray; display: flex; align-items: flex-end; }
.content > header h1 { flex: auto; margin: 1rem 0 0.25rem 0; }
.flash { margin: 1em 0; padding: 1em; background: #cae6f6; border: 1px solid #377ba8; }
.post > header { display: flex; align-items: flex-end; font-size: 0.85em; }
.post > header > div:first-of-type { flex: auto; }
.post > header h1 { font-size: 1.5em; margin-bottom: 0; }
.post .about { color: slategray; font-style: italic; }
.post .body { white-space: pre-line; }
.content:last-child { margin-bottom: 0; }
.content form { margin: 1em 0; display: flex; flex-direction: column; }
.content label { font-weight: bold; margin-bottom: 0.5em; }
.content input, .content textarea { margin-bottom: 1em; }
.content textarea { min-height: 12em; resize: vertical; }
input.danger { color: #cc2f2e; }
input[type=submit] { align-self: start; min-width: 10em; }
```

You can find a less compact version of `style.css` in the
[example code](https://github.com/pallets/flask/tree/3.1.2/examples/tutorial/flaskr/static/style.css).

Go to [http://127.0.0.1:5000/auth/login](http://127.0.0.1:5000/auth/login) and the page should look like the
screenshot below.

 ![screenshot of login page](https://flask.palletsprojects.com/en/_images/flaskr_login.png)

You can read more about CSS from [Mozilla’s documentation](https://developer.mozilla.org/docs/Web/CSS). If
you change a static file, refresh the browser page. If the change
doesn’t show up, try clearing your browser’s cache.

Continue to [Blog Blueprint](https://flask.palletsprojects.com/en/stable/blog/).

---

# Templates¶

# Templates

You’ve written the authentication views for your application, but if
you’re running the server and try to go to any of the URLs, you’ll see a
`TemplateNotFound` error. That’s because the views are calling
[render_template()](https://flask.palletsprojects.com/en/api/#flask.render_template), but you haven’t written the templates yet.
The template files will be stored in the `templates` directory inside
the `flaskr` package.

Templates are files that contain static data as well as placeholders
for dynamic data. A template is rendered with specific data to produce a
final document. Flask uses the [Jinja](https://jinja.palletsprojects.com/templates/) template library to render
templates.

In your application, you will use templates to render [HTML](https://developer.mozilla.org/docs/Web/HTML) which
will display in the user’s browser. In Flask, Jinja is configured to
*autoescape* any data that is rendered in HTML templates. This means
that it’s safe to render user input; any characters they’ve entered that
could mess with the HTML, such as `<` and `>` will be *escaped* with
*safe* values that look the same in the browser but don’t cause unwanted
effects.

Jinja looks and behaves mostly like Python. Special delimiters are used
to distinguish Jinja syntax from the static data in the template.
Anything between `{{` and `}}` is an expression that will be output
to the final document. `{%` and `%}` denotes a control flow
statement like `if` and `for`. Unlike Python, blocks are denoted
by start and end tags rather than indentation since static text within
a block could change indentation.

## The Base Layout

Each page in the application will have the same basic layout around a
different body. Instead of writing the entire HTML structure in each
template, each template will *extend* a base template and override
specific sections.

  `flaskr/templates/base.html`

```
<!doctype html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<nav>
  <h1>Flaskr</h1>
  <ul>
    {% if g.user %}
      <li><span>{{ g.user['username'] }}</span>
      <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
    {% else %}
      <li><a href="{{ url_for('auth.register') }}">Register</a>
      <li><a href="{{ url_for('auth.login') }}">Log In</a>
    {% endif %}
  </ul>
</nav>
<section class="content">
  <header>
    {% block header %}{% endblock %}
  </header>
  {% for message in get_flashed_messages() %}
    <div class="flash">{{ message }}</div>
  {% endfor %}
  {% block content %}{% endblock %}
</section>
```

[g](https://flask.palletsprojects.com/en/api/#flask.g) is automatically available in templates. Based on if
`g.user` is set (from `load_logged_in_user`), either the username
and a log out link are displayed, or links to register and log in
are displayed. [url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for) is also automatically available, and is
used to generate URLs to views instead of writing them out manually.

After the page title, and before the content, the template loops over
each message returned by [get_flashed_messages()](https://flask.palletsprojects.com/en/api/#flask.get_flashed_messages). You used
[flash()](https://flask.palletsprojects.com/en/api/#flask.flash) in the views to show error messages, and this is the code
that will display them.

There are three blocks defined here that will be overridden in the other
templates:

1. `{% block title %}` will change the title displayed in the
  browser’s tab and window title.
2. `{% block header %}` is similar to `title` but will change the
  title displayed on the page.
3. `{% block content %}` is where the content of each page goes, such
  as the login form or a blog post.

The base template is directly in the `templates` directory. To keep
the others organized, the templates for a blueprint will be placed in a
directory with the same name as the blueprint.

## Register

  `flaskr/templates/auth/register.html`

```
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Register{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Register">
  </form>
{% endblock %}
```

`{% extends 'base.html' %}` tells Jinja that this template should
replace the blocks from the base template. All the rendered content must
appear inside `{% block %}` tags that override blocks from the base
template.

A useful pattern used here is to place `{% block title %}` inside
`{% block header %}`. This will set the title block and then output
the value of it into the header block, so that both the window and page
share the same title without writing it twice.

The `input` tags are using the `required` attribute here. This tells
the browser not to submit the form until those fields are filled in. If
the user is using an older browser that doesn’t support that attribute,
or if they are using something besides a browser to make requests, you
still want to validate the data in the Flask view. It’s important to
always fully validate the data on the server, even if the client does
some validation as well.

## Log In

This is identical to the register template except for the title and
submit button.

  `flaskr/templates/auth/login.html`

```
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Log In{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Log In">
  </form>
{% endblock %}
```

## Register A User

Now that the authentication templates are written, you can register a
user. Make sure the server is still running (`flask run` if it’s not),
then go to [http://127.0.0.1:5000/auth/register](http://127.0.0.1:5000/auth/register).

Try clicking the “Register” button without filling out the form and see
that the browser shows an error message. Try removing the `required`
attributes from the `register.html` template and click “Register”
again. Instead of the browser showing an error, the page will reload and
the error from [flash()](https://flask.palletsprojects.com/en/api/#flask.flash) in the view will be shown.

Fill out a username and password and you’ll be redirected to the login
page. Try entering an incorrect username, or the correct username and
incorrect password. If you log in you’ll get an error because there’s
no `index` view to redirect to yet.

Continue to [Static Files](https://flask.palletsprojects.com/en/stable/static/).
