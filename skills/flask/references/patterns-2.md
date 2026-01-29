# Lazily Loading Views¶ and more

# Lazily Loading Views¶

# Lazily Loading Views

Flask is usually used with the decorators.  Decorators are simple and you
have the URL right next to the function that is called for that specific
URL.  However there is a downside to this approach: it means all your code
that uses decorators has to be imported upfront or Flask will never
actually find your function.

This can be a problem if your application has to import quick.  It might
have to do that on systems like Google’s App Engine or other systems.  So
if you suddenly notice that your application outgrows this approach you
can fall back to a centralized URL mapping.

The system that enables having a central URL map is the
[add_url_rule()](https://flask.palletsprojects.com/en/api/#flask.Flask.add_url_rule) function.  Instead of using decorators,
you have a file that sets up the application with all URLs.

## Converting to Centralized URL Map

Imagine the current application looks somewhat like this:

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    pass

@app.route('/user/<username>')
def user(username):
    pass
```

Then, with the centralized approach you would have one file with the views
(`views.py`) but without any decorator:

```
def index():
    pass

def user(username):
    pass
```

And then a file that sets up an application which maps the functions to
URLs:

```
from flask import Flask
from yourapplication import views
app = Flask(__name__)
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/user/<username>', view_func=views.user)
```

## Loading Late

So far we only split up the views and the routing, but the module is still
loaded upfront.  The trick is to actually load the view function as needed.
This can be accomplished with a helper class that behaves just like a
function but internally imports the real function on first use:

```
from werkzeug.utils import import_string, cached_property

class LazyView(object):

    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)
```

What’s important here is is that `__module__` and `__name__` are properly
set.  This is used by Flask internally to figure out how to name the
URL rules in case you don’t provide a name for the rule yourself.

Then you can define your central place to combine the views like this:

```
from flask import Flask
from yourapplication.helpers import LazyView
app = Flask(__name__)
app.add_url_rule('/',
                 view_func=LazyView('yourapplication.views.index'))
app.add_url_rule('/user/<username>',
                 view_func=LazyView('yourapplication.views.user'))
```

You can further optimize this in terms of amount of keystrokes needed to
write this by having a function that calls into
[add_url_rule()](https://flask.palletsprojects.com/en/api/#flask.Flask.add_url_rule) by prefixing a string with the project
name and a dot, and by wrapping `view_func` in a `LazyView` as needed.

```
def url(import_name, url_rules=[], **options):
    view = LazyView(f"yourapplication.{import_name}")
    for url_rule in url_rules:
        app.add_url_rule(url_rule, view_func=view, **options)

# add a single route to the index view
url('views.index', ['/'])

# add two routes to a single function endpoint
url_rules = ['/user/','/user/<username>']
url('views.user', url_rules)
```

One thing to keep in mind is that before and after request handlers have
to be in a file that is imported upfront to work properly on the first
request.  The same goes for any kind of remaining decorator.

---

# Adding HTTP Method Overrides¶

# Adding HTTP Method Overrides

Some HTTP proxies do not support arbitrary HTTP methods or newer HTTP
methods (such as PATCH). In that case it’s possible to “proxy” HTTP
methods through another HTTP method in total violation of the protocol.

The way this works is by letting the client do an HTTP POST request and
set the `X-HTTP-Method-Override` header. Then the method is replaced
with the header value before being passed to Flask.

This can be accomplished with an HTTP middleware:

```
class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)
```

To use this with Flask, wrap the app object with the middleware:

```
from flask import Flask

app = Flask(__name__)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
```

---

# MongoDB with MongoEngine¶

# MongoDB with MongoEngine

Using a document database like MongoDB is a common alternative to
relational SQL databases. This pattern shows how to use
[MongoEngine](http://mongoengine.org), a document mapper library, to integrate with MongoDB.

A running MongoDB server and [Flask-MongoEngine](https://flask-mongoengine.readthedocs.io) are required.

```
pip install flask-mongoengine
```

## Configuration

Basic setup can be done by defining `MONGODB_SETTINGS` on
`app.config` and creating a `MongoEngine` instance.

```
from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "myapp",
}
db = MongoEngine(app)
```

## Mapping Documents

To declare a model that represents a Mongo document, create a class that
inherits from `Document` and declare each of the fields.

```
import mongoengine as me

class Movie(me.Document):
    title = me.StringField(required=True)
    year = me.IntField()
    rated = me.StringField()
    director = me.StringField()
    actors = me.ListField()
```

If the document has nested fields, use `EmbeddedDocument` to
defined the fields of the embedded document and
`EmbeddedDocumentField` to declare it on the parent document.

```
class Imdb(me.EmbeddedDocument):
    imdb_id = me.StringField()
    rating = me.DecimalField()
    votes = me.IntField()

class Movie(me.Document):
    ...
    imdb = me.EmbeddedDocumentField(Imdb)
```

## Creating Data

Instantiate your document class with keyword arguments for the fields.
You can also assign values to the field attributes after instantiation.
Then call `doc.save()`.

```
bttf = Movie(title="Back To The Future", year=1985)
bttf.actors = [
    "Michael J. Fox",
    "Christopher Lloyd"
]
bttf.imdb = Imdb(imdb_id="tt0088763", rating=8.5)
bttf.save()
```

## Queries

Use the class `objects` attribute to make queries. A keyword argument
looks for an equal value on the field.

```
bttf = Movie.objects(title="Back To The Future").get_or_404()
```

Query operators may be used by concatenating them with the field name
using a double-underscore. `objects`, and queries returned by
calling it, are iterable.

```
some_theron_movie = Movie.objects(actors__in=["Charlize Theron"]).first()

for recents in Movie.objects(year__gte=2017):
    print(recents.title)
```

## Documentation

There are many more ways to define and query documents with MongoEngine.
For more information, check out the [official documentation](http://mongoengine.org).

Flask-MongoEngine adds helpful utilities on top of MongoEngine. Check
out their [documentation](https://flask-mongoengine.readthedocs.io) as well.

---

# Large Applications as Packages¶

# Large Applications as Packages

Imagine a simple flask application structure that looks like this:

```
/yourapplication
    yourapplication.py
    /static
        style.css
    /templates
        layout.html
        index.html
        login.html
        ...
```

While this is fine for small applications, for larger applications
it’s a good idea to use a package instead of a module.
The [Tutorial](https://flask.palletsprojects.com/en/tutorial/) is structured to use the package pattern,
see the [example code](https://github.com/pallets/flask/tree/3.1.2/examples/tutorial).

## Simple Packages

To convert that into a larger one, just create a new folder
`yourapplication` inside the existing one and move everything below it.
Then rename `yourapplication.py` to `__init__.py`.  (Make sure to delete
all `.pyc` files first, otherwise things would most likely break)

You should then end up with something like that:

```
/yourapplication
    /yourapplication
        __init__.py
        /static
            style.css
        /templates
            layout.html
            index.html
            login.html
            ...
```

But how do you run your application now?  The naive `python
yourapplication/__init__.py` will not work.  Let’s just say that Python
does not want modules in packages to be the startup file.  But that is not
a big problem, just add a new file called `pyproject.toml` next to the inner
`yourapplication` folder with the following contents:

```
[project]
name = "yourapplication"
dependencies = [
    "flask",
]

[build-system]
requires = ["flit_core<4"]
build-backend = "flit_core.buildapi"
```

Install your application so it is importable:

```
$ pip install -e .
```

To use the `flask` command and run your application you need to set
the `--app` option that tells Flask where to find the application
instance:

```
$ flask --app yourapplication run
```

What did we gain from this?  Now we can restructure the application a bit
into multiple modules.  The only thing you have to remember is the
following quick checklist:

1. the `Flask` application object creation has to be in the
  `__init__.py` file.  That way each module can import it safely and the
  `__name__` variable will resolve to the correct package.
2. all the view functions (the ones with a [route()](https://flask.palletsprojects.com/en/api/#flask.Flask.route)
  decorator on top) have to be imported in the `__init__.py` file.
  Not the object itself, but the module it is in. Import the view module
  **after the application object is created**.

Here’s an example `__init__.py`:

```
from flask import Flask
app = Flask(__name__)

import yourapplication.views
```

And this is what `views.py` would look like:

```
from yourapplication import app

@app.route('/')
def index():
    return 'Hello World!'
```

You should then end up with something like that:

```
/yourapplication
    pyproject.toml
    /yourapplication
        __init__.py
        views.py
        /static
            style.css
        /templates
            layout.html
            index.html
            login.html
            ...
```

Circular Imports

Every Python programmer hates them, and yet we just added some:
circular imports (That’s when two modules depend on each other.  In this
case `views.py` depends on `__init__.py`).  Be advised that this is a
bad idea in general but here it is actually fine.  The reason for this is
that we are not actually using the views in `__init__.py` and just
ensuring the module is imported and we are doing that at the bottom of
the file.

## Working with Blueprints

If you have larger applications it’s recommended to divide them into
smaller groups where each group is implemented with the help of a
blueprint.  For a gentle introduction into this topic refer to the
[Modular Applications with Blueprints](https://flask.palletsprojects.com/en/blueprints/) chapter of the documentation.

---

# Request Content Checksums¶

# Request Content Checksums

Various pieces of code can consume the request data and preprocess it.
For instance JSON data ends up on the request object already read and
processed, form data ends up there as well but goes through a different
code path.  This seems inconvenient when you want to calculate the
checksum of the incoming request data.  This is necessary sometimes for
some APIs.

Fortunately this is however very simple to change by wrapping the input
stream.

The following example calculates the SHA1 checksum of the incoming data as
it gets read and stores it in the WSGI environment:

```
import hashlib

class ChecksumCalcStream(object):

    def __init__(self, stream):
        self._stream = stream
        self._hash = hashlib.sha1()

    def read(self, bytes):
        rv = self._stream.read(bytes)
        self._hash.update(rv)
        return rv

    def readline(self, size_hint):
        rv = self._stream.readline(size_hint)
        self._hash.update(rv)
        return rv

def generate_checksum(request):
    env = request.environ
    stream = ChecksumCalcStream(env['wsgi.input'])
    env['wsgi.input'] = stream
    return stream._hash
```

To use this, all you need to do is to hook the calculating stream in
before the request starts consuming data.  (Eg: be careful accessing
`request.form` or anything of that nature.  `before_request_handlers`
for instance should be careful not to access it).

Example usage:

```
@app.route('/special-api', methods=['POST'])
def special_api():
    hash = generate_checksum(request)
    # Accessing this parses the input stream
    files = request.files
    # At this point the hash is fully constructed.
    checksum = hash.hexdigest()
    return f"Hash was: {checksum}"
```

---

# Single

# Single-Page Applications

Flask can be used to serve Single-Page Applications (SPA) by placing static
files produced by your frontend framework in a subfolder inside of your
project. You will also need to create a catch-all endpoint that routes all
requests to your SPA.

The following example demonstrates how to serve an SPA along with an API:

```
from flask import Flask, jsonify

app = Flask(__name__, static_folder='app', static_url_path="/app")

@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")
```

---

# SQLAlchemy in Flask¶

# SQLAlchemy in Flask

Many people prefer [SQLAlchemy](https://www.sqlalchemy.org/) for database access.  In this case it’s
encouraged to use a package instead of a module for your flask application
and drop the models into a separate module ([Large Applications as Packages](https://flask.palletsprojects.com/en/stable/packages/)). While that
is not necessary, it makes a lot of sense.

There are four very common ways to use SQLAlchemy.  I will outline each
of them here:

## Flask-SQLAlchemy Extension

Because SQLAlchemy is a common database abstraction layer and object
relational mapper that requires a little bit of configuration effort,
there is a Flask extension that handles that for you.  This is recommended
if you want to get started quickly.

You can download [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) from [PyPI](https://pypi.org/project/Flask-SQLAlchemy/).

## Declarative

The declarative extension in SQLAlchemy is the most recent method of using
SQLAlchemy.  It allows you to define tables and models in one go, similar
to how Django works.  In addition to the following text I recommend the
official documentation on the [declarative](https://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/) extension.

Here’s the example `database.py` module for your application:

```
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:////tmp/test.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import yourapplication.models
    Base.metadata.create_all(bind=engine)
```

To define your models, just subclass the `Base` class that was created by
the code above.  If you are wondering why we don’t have to care about
threads here (like we did in the SQLite3 example above with the
[g](https://flask.palletsprojects.com/en/api/#flask.g) object): that’s because SQLAlchemy does that for us
already with the [scoped_session](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoped_session).

To use SQLAlchemy in a declarative way with your application, you just
have to put the following code into your application module.  Flask will
automatically remove database sessions at the end of the request or
when the application shuts down:

```
from yourapplication.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
```

Here is an example model (put this into `models.py`, e.g.):

```
from sqlalchemy import Column, Integer, String
from yourapplication.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'
```

To create the database you can use the `init_db` function:

```
>>> from yourapplication.database import init_db
>>> init_db()
```

You can insert entries into the database like this:

```
>>> from yourapplication.database import db_session
>>> from yourapplication.models import User
>>> u = User('admin', 'admin@localhost')
>>> db_session.add(u)
>>> db_session.commit()
```

Querying is simple as well:

```
>>> User.query.all()
[<User 'admin'>]
>>> User.query.filter(User.name == 'admin').first()
<User 'admin'>
```

## Manual Object Relational Mapping

Manual object relational mapping has a few upsides and a few downsides
versus the declarative approach from above.  The main difference is that
you define tables and classes separately and map them together.  It’s more
flexible but a little more to type.  In general it works like the
declarative approach, so make sure to also split up your application into
multiple modules in a package.

Here is an example `database.py` module for your application:

```
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:////tmp/test.db')
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
def init_db():
    metadata.create_all(bind=engine)
```

As in the declarative approach, you need to close the session after
each request or application context shutdown.  Put this into your
application module:

```
from yourapplication.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
```

Here is an example table and model (put this into `models.py`):

```
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from yourapplication.database import metadata, db_session

class User(object):
    query = db_session.query_property()

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'

users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True),
    Column('email', String(120), unique=True)
)
mapper(User, users)
```

Querying and inserting works exactly the same as in the example above.

## SQL Abstraction Layer

If you just want to use the database system (and SQL) abstraction layer
you basically only need the engine:

```
from sqlalchemy import create_engine, MetaData, Table

engine = create_engine('sqlite:////tmp/test.db')
metadata = MetaData(bind=engine)
```

Then you can either declare the tables in your code like in the examples
above, or automatically load them:

```
from sqlalchemy import Table

users = Table('users', metadata, autoload=True)
```

To insert data you can use the `insert` method.  We have to get a
connection first so that we can use a transaction:

```
>>> con = engine.connect()
>>> con.execute(users.insert(), name='admin', email='admin@localhost')
```

SQLAlchemy will automatically commit for us.

To query your database, you use the engine directly or use a connection:

```
>>> users.select(users.c.id == 1).execute().first()
(1, 'admin', 'admin@localhost')
```

These results are also dict-like tuples:

```
>>> r = users.select(users.c.id == 1).execute().first()
>>> r['name']
'admin'
```

You can also pass strings of SQL statements to the
`execute()` method:

```
>>> engine.execute('select * from users where id = :1', [1]).first()
(1, 'admin', 'admin@localhost')
```

For more information about SQLAlchemy, head over to the
[website](https://www.sqlalchemy.org/).

---

# Using SQLite 3 with Flask¶

# Using SQLite 3 with Flask

In Flask you can easily implement the opening of database connections on
demand and closing them when the context dies (usually at the end of the
request).

Here is a simple example of how you can use SQLite 3 with Flask:

```
import sqlite3
from flask import g

DATABASE = '/path/to/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
```

Now, to use the database, the application must either have an active
application context (which is always true if there is a request in flight)
or create an application context itself.  At that point the `get_db`
function can be used to get the current database connection.  Whenever the
context is destroyed the database connection will be terminated.

Example:

```
@app.route('/')
def index():
    cur = get_db().cursor()
    ...
```

Note

Please keep in mind that the teardown request and appcontext functions
are always executed, even if a before-request handler failed or was
never executed.  Because of this we have to make sure here that the
database is there before we close it.

## Connect on Demand

The upside of this approach (connecting on first use) is that this will
only open the connection if truly necessary.  If you want to use this
code outside a request context you can use it in a Python shell by opening
the application context by hand:

```
with app.app_context():
    # now you can use get_db()
```

## Easy Querying

Now in each request handling function you can access `get_db()` to get the
current open database connection.  To simplify working with SQLite, a
row factory function is useful.  It is executed for every result returned
from the database to convert the result.  For instance, in order to get
dictionaries instead of tuples, this could be inserted into the `get_db`
function we created above:

```
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

db.row_factory = make_dicts
```

This will make the sqlite3 module return dicts for this database connection, which are much nicer to deal with. Even more simply, we could place this in `get_db` instead:

```
db.row_factory = sqlite3.Row
```

This would use Row objects rather than dicts to return the results of queries. These are `namedtuple` s, so we can access them either by index or by key. For example, assuming we have a `sqlite3.Row` called `r` for the rows `id`, `FirstName`, `LastName`, and `MiddleInitial`:

```
>>> # You can get values based on the row's name
>>> r['FirstName']
John
>>> # Or, you can get them based on index
>>> r[1]
John
# Row objects are also iterable:
>>> for value in r:
...     print(value)
1
John
Doe
M
```

Additionally, it is a good idea to provide a query function that combines
getting the cursor, executing and fetching the results:

```
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
```

This handy little function, in combination with a row factory, makes
working with the database much more pleasant than it is by just using the
raw cursor and connection objects.

Here is how you can use it:

```
for user in query_db('select * from users'):
    print(user['username'], 'has the id', user['user_id'])
```

Or if you just want a single result:

```
user = query_db('select * from users where username = ?',
                [the_username], one=True)
if user is None:
    print('No such user')
else:
    print(the_username, 'has the id', user['user_id'])
```

To pass variable parts to the SQL statement, use a question mark in the
statement and pass in the arguments as a list.  Never directly add them to
the SQL statement with string formatting because this makes it possible
to attack the application using [SQL Injections](https://en.wikipedia.org/wiki/SQL_injection).

## Initial Schemas

Relational databases need schemas, so applications often ship a
`schema.sql` file that creates the database.  It’s a good idea to provide
a function that creates the database based on that schema.  This function
can do that for you:

```
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
```

You can then create such a database from the Python shell:

```
>>> from yourapplication import init_db
>>> init_db()
```

---

# Streaming Contents¶

# Streaming Contents

Sometimes you want to send an enormous amount of data to the client, much
more than you want to keep in memory.  When you are generating the data on
the fly though, how do you send that back to the client without the
roundtrip to the filesystem?

The answer is by using generators and direct responses.

## Basic Usage

This is a basic view function that generates a lot of CSV data on the fly.
The trick is to have an inner function that uses a generator to generate
data and to then invoke that function and pass it to a response object:

```
@app.route('/large.csv')
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield f"{','.join(row)}\n"
    return generate(), {"Content-Type": "text/csv"}
```

Each `yield` expression is directly sent to the browser.  Note though
that some WSGI middlewares might break streaming, so be careful there in
debug environments with profilers and other things you might have enabled.

## Streaming from Templates

The Jinja template engine supports rendering a template piece by
piece, returning an iterator of strings. Flask provides the
[stream_template()](https://flask.palletsprojects.com/en/api/#flask.stream_template) and [stream_template_string()](https://flask.palletsprojects.com/en/api/#flask.stream_template_string)
functions to make this easier to use.

```
from flask import stream_template

@app.get("/timeline")
def timeline():
    return stream_template("timeline.html")
```

The parts yielded by the render stream tend to match statement blocks in
the template.

## Streaming with Context

The [request](https://flask.palletsprojects.com/en/api/#flask.request) will not be active while the generator is
running, because the view has already returned at that point. If you try
to access `request`, you’ll get a `RuntimeError`.

If your generator function relies on data in `request`, use the
[stream_with_context()](https://flask.palletsprojects.com/en/api/#flask.stream_with_context) wrapper. This will keep the request
context active during the generator.

```
from flask import stream_with_context, request
from markupsafe import escape

@app.route('/stream')
def streamed_response():
    def generate():
        yield '<p>Hello '
        yield escape(request.args['name'])
        yield '!</p>'
    return stream_with_context(generate())
```

It can also be used as a decorator.

```
@stream_with_context
def generate():
    ...

return generate()
```

The [stream_template()](https://flask.palletsprojects.com/en/api/#flask.stream_template) and
[stream_template_string()](https://flask.palletsprojects.com/en/api/#flask.stream_template_string) functions automatically
use [stream_with_context()](https://flask.palletsprojects.com/en/api/#flask.stream_with_context) if a request is active.

---

# Subclassing Flask¶

# Subclassing Flask

The [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) class is designed for subclassing.

For example, you may want to override how request parameters are handled to preserve their order:

```
from flask import Flask, Request
from werkzeug.datastructures import ImmutableOrderedMultiDict
class MyRequest(Request):
    """Request subclass to override request parameter storage"""
    parameter_storage_class = ImmutableOrderedMultiDict
class MyFlask(Flask):
    """Flask subclass using the custom request class"""
    request_class = MyRequest
```

This is the recommended approach for overriding or augmenting Flask’s internal functionality.

---

# Template Inheritance¶

# Template Inheritance

The most powerful part of Jinja is template inheritance. Template inheritance
allows you to build a base “skeleton” template that contains all the common
elements of your site and defines **blocks** that child templates can override.

Sounds complicated but is very basic. It’s easiest to understand it by starting
with an example.

## Base Template

This template, which we’ll call `layout.html`, defines a simple HTML skeleton
document that you might use for a simple two-column page. It’s the job of
“child” templates to fill the empty blocks with content:

```
<!doctype html>
<html>
  <head>
    {% block head %}
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>{% block title %}{% endblock %} - My Webpage</title>
    {% endblock %}
  </head>
  <body>
    <div id="content">{% block content %}{% endblock %}</div>
    <div id="footer">
      {% block footer %}
      &copy; Copyright 2010 by <a href="http://domain.invalid/">you</a>.
      {% endblock %}
    </div>
  </body>
</html>
```

In this example, the `{% block %}` tags define four blocks that child templates
can fill in. All the `block` tag does is tell the template engine that a
child template may override those portions of the template.

## Child Template

A child template might look like this:

```
{% extends "layout.html" %}
{% block title %}Index{% endblock %}
{% block head %}
  {{ super() }}
  <style type="text/css">
    .important { color: #336699; }
  </style>
{% endblock %}
{% block content %}
  <h1>Index</h1>
  <p class="important">
    Welcome on my awesome homepage.
{% endblock %}
```

The `{% extends %}` tag is the key here. It tells the template engine that
this template “extends” another template.  When the template system evaluates
this template, first it locates the parent.  The extends tag must be the
first tag in the template.  To render the contents of a block defined in
the parent template, use `{{ super() }}`.

---

# Using URL Processors¶

# Using URL Processors

  Changelog

Added in version 0.7.

Flask 0.7 introduces the concept of URL processors.  The idea is that you
might have a bunch of resources with common parts in the URL that you
don’t always explicitly want to provide.  For instance you might have a
bunch of URLs that have the language code in it but you don’t want to have
to handle it in every single function yourself.

URL processors are especially helpful when combined with blueprints.  We
will handle both application specific URL processors here as well as
blueprint specifics.

## Internationalized Application URLs

Consider an application like this:

```
from flask import Flask, g

app = Flask(__name__)

@app.route('/<lang_code>/')
def index(lang_code):
    g.lang_code = lang_code
    ...

@app.route('/<lang_code>/about')
def about(lang_code):
    g.lang_code = lang_code
    ...
```

This is an awful lot of repetition as you have to handle the language code
setting on the [g](https://flask.palletsprojects.com/en/api/#flask.g) object yourself in every single function.
Sure, a decorator could be used to simplify this, but if you want to
generate URLs from one function to another you would have to still provide
the language code explicitly which can be annoying.

For the latter, this is where [url_defaults()](https://flask.palletsprojects.com/en/api/#flask.Flask.url_defaults) functions
come in.  They can automatically inject values into a call to
[url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for).  The code below checks if the
language code is not yet in the dictionary of URL values and if the
endpoint wants a value named `'lang_code'`:

```
@app.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or not g.lang_code:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code
```

The method [is_endpoint_expecting()](https://werkzeug.palletsprojects.com/en/stable/routing/#werkzeug.routing.Map.is_endpoint_expecting) of the URL
map can be used to figure out if it would make sense to provide a language
code for the given endpoint.

The reverse of that function are
[url_value_preprocessor()](https://flask.palletsprojects.com/en/api/#flask.Flask.url_value_preprocessor)s.  They are executed right
after the request was matched and can execute code based on the URL
values.  The idea is that they pull information out of the values
dictionary and put it somewhere else:

```
@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code', None)
```

That way you no longer have to do the `lang_code` assignment to
[g](https://flask.palletsprojects.com/en/api/#flask.g) in every function.  You can further improve that by
writing your own decorator that prefixes URLs with the language code, but
the more beautiful solution is using a blueprint.  Once the
`'lang_code'` is popped from the values dictionary and it will no longer
be forwarded to the view function reducing the code to this:

```
from flask import Flask, g

app = Flask(__name__)

@app.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or not g.lang_code:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code

@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code', None)

@app.route('/<lang_code>/')
def index():
    ...

@app.route('/<lang_code>/about')
def about():
    ...
```

## Internationalized Blueprint URLs

Because blueprints can automatically prefix all URLs with a common string
it’s easy to automatically do that for every function.  Furthermore
blueprints can have per-blueprint URL processors which removes a whole lot
of logic from the [url_defaults()](https://flask.palletsprojects.com/en/api/#flask.Flask.url_defaults) function because it no
longer has to check if the URL is really interested in a `'lang_code'`
parameter:

```
from flask import Blueprint, g

bp = Blueprint('frontend', __name__, url_prefix='/<lang_code>')

@bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)

@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')

@bp.route('/')
def index():
    ...

@bp.route('/about')
def about():
    ...
```

---

# View Decorators¶

# View Decorators

Python has a really interesting feature called function decorators.  This
allows some really neat things for web applications.  Because each view in
Flask is a function, decorators can be used to inject additional
functionality to one or more functions.  The [route()](https://flask.palletsprojects.com/en/api/#flask.Flask.route)
decorator is the one you probably used already.  But there are use cases
for implementing your own decorator.  For instance, imagine you have a
view that should only be used by people that are logged in.  If a user
goes to the site and is not logged in, they should be redirected to the
login page.  This is a good example of a use case where a decorator is an
excellent solution.

## Login Required Decorator

So let’s implement such a decorator.  A decorator is a function that
wraps and replaces another function.  Since the original function is
replaced, you need to remember to copy the original function’s information
to the new function.  Use [functools.wraps()](https://docs.python.org/3/library/functools.html#functools.wraps) to handle this for you.

This example assumes that the login page is called `'login'` and that
the current user is stored in `g.user` and is `None` if there is no-one
logged in.

```
from functools import wraps
from flask import g, request, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
```

To use the decorator, apply it as innermost decorator to a view function.
When applying further decorators, always remember
that the [route()](https://flask.palletsprojects.com/en/api/#flask.Flask.route) decorator is the outermost.

```
@app.route('/secret_page')
@login_required
def secret_page():
    pass
```

Note

The `next` value will exist in `request.args` after a `GET` request for
the login page.  You’ll have to pass it along when sending the `POST` request
from the login form.  You can do this with a hidden input tag, then retrieve it
from `request.form` when logging the user in.

```
<input type="hidden" value="{{ request.args.get('next', '') }}"/>
```

## Caching Decorator

Imagine you have a view function that does an expensive calculation and
because of that you would like to cache the generated results for a
certain amount of time.  A decorator would be nice for that.  We’re
assuming you have set up a cache like mentioned in [Caching](https://flask.palletsprojects.com/en/stable/caching/).

Here is an example cache function.  It generates the cache key from a
specific prefix (actually a format string) and the current path of the
request.  Notice that we are using a function that first creates the
decorator that then decorates the function.  Sounds awful? Unfortunately
it is a little bit more complex, but the code should still be
straightforward to read.

The decorated function will then work as follows

1. get the unique cache key for the current request based on the current
  path.
2. get the value for that key from the cache. If the cache returned
  something we will return that value.
3. otherwise the original function is called and the return value is
  stored in the cache for the timeout provided (by default 5 minutes).

Here the code:

```
from functools import wraps
from flask import request

def cached(timeout=5 * 60, key='view/{}'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key.format(request.path)
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator
```

Notice that this assumes an instantiated `cache` object is available, see
[Caching](https://flask.palletsprojects.com/en/stable/caching/).

## Templating Decorator

A common pattern invented by the TurboGears guys a while back is a
templating decorator.  The idea of that decorator is that you return a
dictionary with the values passed to the template from the view function
and the template is automatically rendered.  With that, the following
three examples do exactly the same:

```
@app.route('/')
def index():
    return render_template('index.html', value=42)

@app.route('/')
@templated('index.html')
def index():
    return dict(value=42)

@app.route('/')
@templated()
def index():
    return dict(value=42)
```

As you can see, if no template name is provided it will use the endpoint
of the URL map with dots converted to slashes + `'.html'`.  Otherwise
the provided template name is used.  When the decorated function returns,
the dictionary returned is passed to the template rendering function.  If
`None` is returned, an empty dictionary is assumed, if something else than
a dictionary is returned we return it from the function unchanged.  That
way you can still use the redirect function or return simple strings.

Here is the code for that decorator:

```
from functools import wraps
from flask import request, render_template

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = f"{request.endpoint.replace('.', '/')}.html"
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator
```

## Endpoint Decorator

When you want to use the werkzeug routing system for more flexibility you
need to map the endpoint as defined in the [Rule](https://werkzeug.palletsprojects.com/en/stable/routing/#werkzeug.routing.Rule)
to a view function. This is possible with this decorator. For example:

```
from flask import Flask
from werkzeug.routing import Rule

app = Flask(__name__)
app.url_map.add(Rule('/', endpoint='index'))

@app.endpoint('index')
def my_index():
    return "Hello world"
```

---

# Form Validation with WTForms¶

# Form Validation with WTForms

When you have to work with form data submitted by a browser view, code
quickly becomes very hard to read.  There are libraries out there designed
to make this process easier to manage.  One of them is [WTForms](https://wtforms.readthedocs.io/) which we
will handle here.  If you find yourself in the situation of having many
forms, you might want to give it a try.

When you are working with WTForms you have to define your forms as classes
first.  I recommend breaking up the application into multiple modules
([Large Applications as Packages](https://flask.palletsprojects.com/en/stable/packages/)) for that and adding a separate module for the
forms.

Getting the most out of WTForms with an Extension

The [Flask-WTF](https://flask-wtf.readthedocs.io/) extension expands on this pattern and adds a
few little helpers that make working with forms and Flask more
fun.  You can get it from [PyPI](https://pypi.org/project/Flask-WTF/).

## The Forms

This is an example form for a typical registration page:

```
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
```

## In the View

In the view function, the usage of this form looks like this:

```
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
```

Notice we’re implying that the view is using SQLAlchemy here
([SQLAlchemy in Flask](https://flask.palletsprojects.com/en/stable/sqlalchemy/)), but that’s not a requirement, of course.  Adapt
the code as necessary.

Things to remember:

1. create the form from the request `form` value if
  the data is submitted via the HTTP `POST` method and
  `args` if the data is submitted as `GET`.
2. to validate the data, call the `validate()`
  method, which will return `True` if the data validates, `False`
  otherwise.
3. to access individual values from the form, access `form.<NAME>.data`.

## Forms in Templates

Now to the template side.  When you pass the form to the templates, you can
easily render them there.  Look at the following example template to see
how easy this is.  WTForms does half the form generation for us already.
To make it even nicer, we can write a macro that renders a field with
label and a list of errors if there are any.

Here’s an example `_formhelpers.html` template with such a macro:

```
{% macro render_field(field) %}
  <dt>{{ field.label }}
  <dd>{{ field(**kwargs)|safe }}
  {% if field.errors %}
    <ul class=errors>
    {% for error in field.errors %}
      <li>{{ error }}</li>
    {% endfor %}
    </ul>
  {% endif %}
  </dd>
{% endmacro %}
```

This macro accepts a couple of keyword arguments that are forwarded to
WTForm’s field function, which renders the field for us.  The keyword
arguments will be inserted as HTML attributes.  So, for example, you can
call `render_field(form.username, class='username')` to add a class to
the input element.  Note that WTForms returns standard Python strings,
so we have to tell Jinja that this data is already HTML-escaped with
the `|safe` filter.

Here is the `register.html` template for the function we used above, which
takes advantage of the `_formhelpers.html` template:

```
{% from "_formhelpers.html" import render_field %}
<form method=post>
  <dl>
    {{ render_field(form.username) }}
    {{ render_field(form.email) }}
    {{ render_field(form.password) }}
    {{ render_field(form.confirm) }}
    {{ render_field(form.accept_tos) }}
  </dl>
  <p><input type=submit value=Register>
</form>
```

For more information about WTForms, head over to the [WTForms
website](https://wtforms.readthedocs.io/).
