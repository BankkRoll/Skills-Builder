# Test Coverage¶ and more

# Test Coverage¶

# Test Coverage

Writing unit tests for your application lets you check that the code
you wrote works the way you expect. Flask provides a test client that
simulates requests to the application and returns the response data.

You should test as much of your code as possible. Code in functions only
runs when the function is called, and code in branches, such as `if`
blocks, only runs when the condition is met. You want to make sure that
each function is tested with data that covers each branch.

The closer you get to 100% coverage, the more comfortable you can be
that making a change won’t unexpectedly change other behavior. However,
100% coverage doesn’t guarantee that your application doesn’t have bugs.
In particular, it doesn’t test how the user interacts with the
application in the browser. Despite this, test coverage is an important
tool to use during development.

Note

This is being introduced late in the tutorial, but in your future
projects you should test as you develop.

You’ll use [pytest](https://pytest.readthedocs.io/) and [coverage](https://coverage.readthedocs.io/) to test and measure your code.
Install them both:

```
$ pip install pytest coverage
```

## Setup and Fixtures

The test code is located in the `tests` directory. This directory is
*next to* the `flaskr` package, not inside it. The
`tests/conftest.py` file contains setup functions called *fixtures*
that each test will use. Tests are in Python modules that start with
`test_`, and each test function in those modules also starts with
`test_`.

Each test will create a new temporary database file and populate some
data that will be used in the tests. Write a SQL file to insert that
data.

  `tests/data.sql`

```
INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
```

The `app` fixture will call the factory and pass `test_config` to
configure the application and database for testing instead of using your
local development configuration.

  `tests/conftest.py`

```
import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```

[tempfile.mkstemp()](https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp) creates and opens a temporary file, returning
the file descriptor and the path to it. The `DATABASE` path is
overridden so it points to this temporary path instead of the instance
folder. After setting the path, the database tables are created and the
test data is inserted. After the test is over, the temporary file is
closed and removed.

[TESTING](https://flask.palletsprojects.com/en/config/#TESTING) tells Flask that the app is in test mode. Flask changes
some internal behavior so it’s easier to test, and other extensions can
also use the flag to make testing them easier.

The `client` fixture calls
[app.test_client()](https://flask.palletsprojects.com/en/api/#flask.Flask.test_client) with the application
object created by the `app` fixture. Tests will use the client to make
requests to the application without running the server.

The `runner` fixture is similar to `client`.
[app.test_cli_runner()](https://flask.palletsprojects.com/en/api/#flask.Flask.test_cli_runner) creates a runner
that can call the Click commands registered with the application.

Pytest uses fixtures by matching their function names with the names
of arguments in the test functions. For example, the `test_hello`
function you’ll write next takes a `client` argument. Pytest matches
that with the `client` fixture function, calls it, and passes the
returned value to the test function.

## Factory

There’s not much to test about the factory itself. Most of the code will
be executed for each test already, so if something fails the other tests
will notice.

The only behavior that can change is passing test config. If config is
not passed, there should be some default configuration, otherwise the
configuration should be overridden.

  `tests/test_factory.py`

```
from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
```

You added the `hello` route as an example when writing the factory at
the beginning of the tutorial. It returns “Hello, World!”, so the test
checks that the response data matches.

## Database

Within an application context, `get_db` should return the same
connection each time it’s called. After the context, the connection
should be closed.

  `tests/test_db.py`

```
import sqlite3

import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)
```

The `init-db` command should call the `init_db` function and output
a message.

  `tests/test_db.py`

```
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
```

This test uses Pytest’s `monkeypatch` fixture to replace the
`init_db` function with one that records that it’s been called. The
`runner` fixture you wrote above is used to call the `init-db`
command by name.

## Authentication

For most of the views, a user needs to be logged in. The easiest way to
do this in tests is to make a `POST` request to the `login` view
with the client. Rather than writing that out every time, you can write
a class with methods to do that, and use a fixture to pass it the client
for each test.

  `tests/conftest.py`

```
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
```

With the `auth` fixture, you can call `auth.login()` in a test to
log in as the `test` user, which was inserted as part of the test
data in the `app` fixture.

The `register` view should render successfully on `GET`. On `POST`
with valid form data, it should redirect to the login URL and the user’s
data should be in the database. Invalid data should display error
messages.

  `tests/test_auth.py`

```
import pytest
from flask import g, session
from flaskr.db import get_db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
```

[client.get()](https://werkzeug.palletsprojects.com/en/stable/test/#werkzeug.test.Client.get) makes a `GET` request
and returns the [Response](https://flask.palletsprojects.com/en/api/#flask.Response) object returned by Flask. Similarly,
[client.post()](https://werkzeug.palletsprojects.com/en/stable/test/#werkzeug.test.Client.post) makes a `POST`
request, converting the `data` dict into form data.

To test that the page renders successfully, a simple request is made and
checked for a `200 OK` [status_code](https://flask.palletsprojects.com/en/api/#flask.Response.status_code). If
rendering failed, Flask would return a `500 Internal Server Error`
code.

`headers` will have a `Location` header with the login
URL when the register view redirects to the login view.

[data](https://flask.palletsprojects.com/en/api/#flask.Response.data) contains the body of the response as bytes. If
you expect a certain value to render on the page, check that it’s in
`data`. Bytes must be compared to bytes. If you want to compare text,
use [get_data(as_text=True)](https://werkzeug.palletsprojects.com/en/stable/wrappers/#werkzeug.wrappers.Response.get_data)
instead.

`pytest.mark.parametrize` tells Pytest to run the same test function
with different arguments. You use it here to test different invalid
input and error messages without writing the same code three times.

The tests for the `login` view are very similar to those for
`register`. Rather than testing the data in the database,
[session](https://flask.palletsprojects.com/en/api/#flask.session) should have `user_id` set after logging in.

  `tests/test_auth.py`

```
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
```

Using `client` in a `with` block allows accessing context variables
such as [session](https://flask.palletsprojects.com/en/api/#flask.session) after the response is returned. Normally,
accessing `session` outside of a request would raise an error.

Testing `logout` is the opposite of `login`. [session](https://flask.palletsprojects.com/en/api/#flask.session) should
not contain `user_id` after logging out.

  `tests/test_auth.py`

```
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
```

## Blog

All the blog views use the `auth` fixture you wrote earlier. Call
`auth.login()` and subsequent requests from the client will be logged
in as the `test` user.

The `index` view should display information about the post that was
added with the test data. When logged in as the author, there should be
a link to edit the post.

You can also test some more authentication behavior while testing the
`index` view. When not logged in, each page shows links to log in or
register. When logged in, there’s a link to log out.

  `tests/test_blog.py`

```
import pytest
from flaskr.db import get_db

def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data
```

A user must be logged in to access the `create`, `update`, and
`delete` views. The logged in user must be the author of the post to
access `update` and `delete`, otherwise a `403 Forbidden` status
is returned. If a `post` with the given `id` doesn’t exist,
`update` and `delete` should return `404 Not Found`.

  `tests/test_blog.py`

```
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"

def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404
```

The `create` and `update` views should render and return a
`200 OK` status for a `GET` request. When valid data is sent in a
`POST` request, `create` should insert the new post data into the
database, and `update` should modify the existing data. Both pages
should show an error message on invalid data.

  `tests/test_blog.py`

```
def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2

def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data
```

The `delete` view should redirect to the index URL and the post should
no longer exist in the database.

  `tests/test_blog.py`

```
def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None
```

## Running the Tests

Some extra configuration, which is not required but makes running tests with coverage
less verbose, can be added to the project’s `pyproject.toml` file.

  `pyproject.toml`

```
[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.run]
branch = true
source = ["flaskr"]
```

To run the tests, use the `pytest` command. It will find and run all
the test functions you’ve written.

```
$ pytest

========================= test session starts ==========================
platform linux -- Python 3.6.4, pytest-3.5.0, py-1.5.3, pluggy-0.6.0
rootdir: /home/user/Projects/flask-tutorial
collected 23 items

tests/test_auth.py ........                                      [ 34%]
tests/test_blog.py ............                                  [ 86%]
tests/test_db.py ..                                              [ 95%]
tests/test_factory.py ..                                         [100%]

====================== 24 passed in 0.64 seconds =======================
```

If any tests fail, pytest will show the error that was raised. You can
run `pytest -v` to get a list of each test function rather than dots.

To measure the code coverage of your tests, use the `coverage` command
to run pytest instead of running it directly.

```
$ coverage run -m pytest
```

You can either view a simple coverage report in the terminal:

```
$ coverage report

Name                 Stmts   Miss Branch BrPart  Cover
------------------------------------------------------
flaskr/__init__.py      21      0      2      0   100%
flaskr/auth.py          54      0     22      0   100%
flaskr/blog.py          54      0     16      0   100%
flaskr/db.py            24      0      4      0   100%
------------------------------------------------------
TOTAL                  153      0     44      0   100%
```

An HTML report allows you to see which lines were covered in each file:

```
$ coverage html
```

This generates files in the `htmlcov` directory. Open
`htmlcov/index.html` in your browser to see the report.

Continue to [Deploy to Production](https://flask.palletsprojects.com/en/stable/deploy/).

---

# Blueprints and Views¶

# Blueprints and Views

A view function is the code you write to respond to requests to your
application. Flask uses patterns to match the incoming request URL to
the view that should handle it. The view returns data that Flask turns
into an outgoing response. Flask can also go the other direction and
generate a URL to a view based on its name and arguments.

## Create a Blueprint

A [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint) is a way to organize a group of related views and
other code. Rather than registering views and other code directly with
an application, they are registered with a blueprint. Then the blueprint
is registered with the application when it is available in the factory
function.

Flaskr will have two blueprints, one for authentication functions and
one for the blog posts functions. The code for each blueprint will go
in a separate module. Since the blog needs to know about authentication,
you’ll write the authentication one first.

  `flaskr/auth.py`

```
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
```

This creates a [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint) named `'auth'`. Like the application
object, the blueprint needs to know where it’s defined, so `__name__`
is passed as the second argument. The `url_prefix` will be prepended
to all the URLs associated with the blueprint.

Import and register the blueprint from the factory using
[app.register_blueprint()](https://flask.palletsprojects.com/en/api/#flask.Flask.register_blueprint). Place the
new code at the end of the factory function before returning the app.

  `flaskr/__init__.py`

```
def create_app():
    app = ...
    # existing code omitted

    from . import auth
    app.register_blueprint(auth.bp)

    return app
```

The authentication blueprint will have views to register new users and
to log in and log out.

## The First View: Register

When the user visits the `/auth/register` URL, the `register` view
will return [HTML](https://developer.mozilla.org/docs/Web/HTML) with a form for them to fill out. When they submit
the form, it will validate their input and either show the form again
with an error message or create the new user and go to the login page.

For now you will just write the view code. On the next page, you’ll
write templates to generate the HTML form.

  `flaskr/auth.py`

```
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
```

Here’s what the `register` view function is doing:

1. [@bp.route](https://flask.palletsprojects.com/en/api/#flask.Blueprint.route) associates the URL `/register`
  with the `register` view function. When Flask receives a request
  to `/auth/register`, it will call the `register` view and use
  the return value as the response.
2. If the user submitted the form,
  [request.method](https://flask.palletsprojects.com/en/api/#flask.Request.method) will be `'POST'`. In this
  case, start validating the input.
3. [request.form](https://flask.palletsprojects.com/en/api/#flask.Request.form) is a special type of
  [dict](https://docs.python.org/3/library/stdtypes.html#dict) mapping submitted form keys and values. The user will
  input their `username` and `password`.
4. Validate that `username` and `password` are not empty.
5. If validation succeeds, insert the new user data into the database.
  - [db.execute](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.execute) takes a SQL
    query with `?` placeholders for any user input, and a tuple of
    values to replace the placeholders with. The database library
    will take care of escaping the values so you are not vulnerable
    to a *SQL injection attack*.
  - For security, passwords should never be stored in the database
    directly. Instead,
    [generate_password_hash()](https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security.generate_password_hash) is used to
    securely hash the password, and that hash is stored. Since this
    query modifies data,
    [db.commit()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.commit) needs to be
    called afterwards to save the changes.
  - An [sqlite3.IntegrityError](https://docs.python.org/3/library/sqlite3.html#sqlite3.IntegrityError) will occur if the username
    already exists, which should be shown to the user as another
    validation error.
6. After storing the user, they are redirected to the login page.
  [url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for) generates the URL for the login view based on its
  name. This is preferable to writing the URL directly as it allows
  you to change the URL later without changing all code that links to
  it. [redirect()](https://flask.palletsprojects.com/en/api/#flask.redirect) generates a redirect response to the generated
  URL.
7. If validation fails, the error is shown to the user. [flash()](https://flask.palletsprojects.com/en/api/#flask.flash)
  stores messages that can be retrieved when rendering the template.
8. When the user initially navigates to `auth/register`, or
  there was a validation error, an HTML page with the registration
  form should be shown. [render_template()](https://flask.palletsprojects.com/en/api/#flask.render_template) will render a template
  containing the HTML, which you’ll write in the next step of the
  tutorial.

## Login

This view follows the same pattern as the `register` view above.

  `flaskr/auth.py`

```
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
```

There are a few differences from the `register` view:

1. The user is queried first and stored in a variable for later use.
  [fetchone()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchone) returns one row from the query.
  If the query returned no results, it returns `None`. Later,
  [fetchall()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchall) will be used, which returns a list
  of all results.
2. [check_password_hash()](https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security.check_password_hash) hashes the submitted
  password in the same way as the stored hash and securely compares
  them. If they match, the password is valid.
3. [session](https://flask.palletsprojects.com/en/api/#flask.session) is a [dict](https://docs.python.org/3/library/stdtypes.html#dict) that stores data across requests.
  When validation succeeds, the user’s `id` is stored in a new
  session. The data is stored in a *cookie* that is sent to the
  browser, and the browser then sends it back with subsequent requests.
  Flask securely *signs* the data so that it can’t be tampered with.

Now that the user’s `id` is stored in the [session](https://flask.palletsprojects.com/en/api/#flask.session), it will be
available on subsequent requests. At the beginning of each request, if
a user is logged in their information should be loaded and made
available to other views.

  `flaskr/auth.py`

```
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
```

[bp.before_app_request()](https://flask.palletsprojects.com/en/api/#flask.Blueprint.before_app_request) registers
a function that runs before the view function, no matter what URL is
requested. `load_logged_in_user` checks if a user id is stored in the
[session](https://flask.palletsprojects.com/en/api/#flask.session) and gets that user’s data from the database, storing it
on [g.user](https://flask.palletsprojects.com/en/api/#flask.g), which lasts for the length of the request. If
there is no user id, or if the id doesn’t exist, `g.user` will be
`None`.

## Logout

To log out, you need to remove the user id from the [session](https://flask.palletsprojects.com/en/api/#flask.session).
Then `load_logged_in_user` won’t load a user on subsequent requests.

  `flaskr/auth.py`

```
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
```

## Require Authentication in Other Views

Creating, editing, and deleting blog posts will require a user to be
logged in. A *decorator* can be used to check this for each view it’s
applied to.

  `flaskr/auth.py`

```
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
```

This decorator returns a new view function that wraps the original view
it’s applied to. The new function checks if a user is loaded and
redirects to the login page otherwise. If a user is loaded the original
view is called and continues normally. You’ll use this decorator when
writing the blog views.

## Endpoints and URLs

The [url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for) function generates the URL to a view based on a name
and arguments. The name associated with a view is also called the
*endpoint*, and by default it’s the same as the name of the view
function.

For example, the `hello()` view that was added to the app
factory earlier in the tutorial has the name `'hello'` and can be
linked to with `url_for('hello')`. If it took an argument, which
you’ll see later, it would be linked to using
`url_for('hello', who='World')`.

When using a blueprint, the name of the blueprint is prepended to the
name of the function, so the endpoint for the `login` function you
wrote above is `'auth.login'` because you added it to the `'auth'`
blueprint.

Continue to [Templates](https://flask.palletsprojects.com/en/stable/templates/).
