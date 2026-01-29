# Command Line Interface¶ and more

# Command Line Interface¶

# Command Line Interface

Installing Flask installs the `flask` script, a [Click](https://click.palletsprojects.com/) command line
interface, in your virtualenv. Executed from the terminal, this script gives
access to built-in, extension, and application-defined commands. The `--help`
option will give more information about any commands and options.

## Application Discovery

The `flask` command is installed by Flask, not your application; it must be
told where to find your application in order to use it. The `--app`
option is used to specify how to load the application.

While `--app` supports a variety of options for specifying your
application, most use cases should be simple. Here are the typical values:

  (nothing)

The name “app” or “wsgi” is imported (as a “.py” file, or package),
automatically detecting an app (`app` or `application`) or
factory (`create_app` or `make_app`).

  `--app hello`

The given name is imported, automatically detecting an app (`app`
or `application`) or factory (`create_app` or `make_app`).

---

`--app` has three parts: an optional path that sets the current working
directory, a Python file or dotted import path, and an optional variable
name of the instance or factory. If the name is a factory, it can optionally
be followed by arguments in parentheses. The following values demonstrate these
parts:

  `--app src/hello`

Sets the current working directory to `src` then imports `hello`.

  `--app hello.web`

Imports the path `hello.web`.

  `--app hello:app2`

Uses the `app2` Flask instance in `hello`.

  `--app 'hello:create_app("dev")'`

The `create_app` factory in `hello` is called with the string `'dev'`
as the argument.

If `--app` is not set, the command will try to import “app” or
“wsgi” (as a “.py” file, or package) and try to detect an application
instance or factory.

Within the given import, the command looks for an application instance named
`app` or `application`, then any application instance. If no instance is
found, the command looks for a factory function named `create_app` or
`make_app` that returns an instance.

If parentheses follow the factory name, their contents are parsed as
Python literals and passed as arguments and keyword arguments to the
function. This means that strings must still be in quotes.

## Run the Development Server

The [run](https://flask.palletsprojects.com/en/api/#flask.cli.run_command) command will start the development server. It
replaces the [Flask.run()](https://flask.palletsprojects.com/en/api/#flask.Flask.run) method in most cases.

```
$ flask --app hello run
 * Serving Flask app "hello"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Warning

Do not use this command to run your application in production.
Only use the development server during development. The development server
is provided for convenience, but is not designed to be particularly secure,
stable, or efficient. See [Deploying to Production](https://flask.palletsprojects.com/en/deploying/) for how to run in production.

If another program is already using port 5000, you’ll see
`OSError: [Errno 98]` or `OSError: [WinError 10013]` when the
server tries to start. See [Address already in use](https://flask.palletsprojects.com/en/server/#address-already-in-use) for how to
handle that.

### Debug Mode

In debug mode, the `flask run` command will enable the interactive debugger and the
reloader by default, and make errors easier to see and debug. To enable debug mode, use
the `--debug` option.

```
$ flask --app hello run --debug
 * Serving Flask app "hello"
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with inotify reloader
 * Debugger is active!
 * Debugger PIN: 223-456-919
```

The `--debug` option can also be passed to the top level `flask` command to enable
debug mode for any command. The following two `run` calls are equivalent.

```
$ flask --app hello --debug run
$ flask --app hello run --debug
```

### Watch and Ignore Files with the Reloader

When using debug mode, the reloader will trigger whenever your Python code or imported
modules change. The reloader can watch additional files with the `--extra-files`
option. Multiple paths are separated with `:`, or `;` on Windows.

```
$ flask run --extra-files file1:dirA/file2:dirB/
 * Running on http://127.0.0.1:8000/
 * Detected change in '/path/to/file1', reloading
```

The reloader can also ignore files using [fnmatch](https://docs.python.org/3/library/fnmatch.html#module-fnmatch) patterns with the
`--exclude-patterns` option. Multiple patterns are separated with `:`, or `;` on
Windows.

## Open a Shell

To explore the data in your application, you can start an interactive Python
shell with the [shell](https://flask.palletsprojects.com/en/api/#flask.cli.shell_command) command. An application
context will be active, and the app instance will be imported.

```
$ flask shell
Python 3.10.0 (default, Oct 27 2021, 06:59:51) [GCC 11.1.0] on linux
App: example [production]
Instance: /home/david/Projects/pallets/flask/instance
>>>
```

Use [shell_context_processor()](https://flask.palletsprojects.com/en/api/#flask.Flask.shell_context_processor) to add other automatic imports.

## Environment Variables From dotenv

The `flask` command supports setting any option for any command with
environment variables. The variables are named like `FLASK_OPTION` or
`FLASK_COMMAND_OPTION`, for example `FLASK_APP` or
`FLASK_RUN_PORT`.

Rather than passing options every time you run a command, or environment
variables every time you open a new terminal, you can use Flask’s dotenv
support to set environment variables automatically.

If [python-dotenv](https://github.com/theskumar/python-dotenv#readme) is installed, running the `flask` command will set
environment variables defined in the files `.env` and `.flaskenv`.
You can also specify an extra file to load with the `--env-file`
option. Dotenv files can be used to avoid having to set `--app` or
`FLASK_APP` manually, and to set configuration using environment
variables similar to how some deployment services work.

Variables set on the command line are used over those set in `.env`,
which are used over those set in `.flaskenv`. `.flaskenv` should be
used for public variables, such as `FLASK_APP`, while `.env` should not
be committed to your repository so that it can set private variables.

Directories are scanned upwards from the directory you call `flask`
from to locate the files.

The files are only loaded by the `flask` command or calling
[run()](https://flask.palletsprojects.com/en/api/#flask.Flask.run). If you would like to load these files when running in
production, you should call [load_dotenv()](https://flask.palletsprojects.com/en/api/#flask.cli.load_dotenv) manually.

### Setting Command Options

Click is configured to load default values for command options from
environment variables. The variables use the pattern
`FLASK_COMMAND_OPTION`. For example, to set the port for the run
command, instead of `flask run --port 8000`:

```
$ export FLASK_RUN_PORT=8000
$ flask run
 * Running on http://127.0.0.1:8000/
```

```
$ set -x FLASK_RUN_PORT 8000
$ flask run
 * Running on http://127.0.0.1:8000/
```

```
> set FLASK_RUN_PORT=8000
> flask run
 * Running on http://127.0.0.1:8000/
```

```
> $env:FLASK_RUN_PORT = 8000
> flask run
 * Running on http://127.0.0.1:8000/
```

These can be added to the `.flaskenv` file just like `FLASK_APP` to
control default command options.

### Disable dotenv

The `flask` command will show a message if it detects dotenv files but
python-dotenv is not installed.

```
$ flask run
 * Tip: There are .env files present. Do "pip install python-dotenv" to use them.
```

You can tell Flask not to load dotenv files even when python-dotenv is
installed by setting the `FLASK_SKIP_DOTENV` environment variable.
This can be useful if you want to load them manually, or if you’re using
a project runner that loads them already. Keep in mind that the
environment variables must be set before the app loads or it won’t
configure as expected.

```
$ export FLASK_SKIP_DOTENV=1
$ flask run
```

```
$ set -x FLASK_SKIP_DOTENV 1
$ flask run
```

```
> set FLASK_SKIP_DOTENV=1
> flask run
```

```
> $env:FLASK_SKIP_DOTENV = 1
> flask run
```

## Environment Variables From virtualenv

If you do not want to install dotenv support, you can still set environment
variables by adding them to the end of the virtualenv’s `activate`
script. Activating the virtualenv will set the variables.

Unix Bash, `.venv/bin/activate`:

```
$ export FLASK_APP=hello
```

Fish, `.venv/bin/activate.fish`:

```
$ set -x FLASK_APP hello
```

Windows CMD, `.venv\Scripts\activate.bat`:

```
> set FLASK_APP=hello
```

Windows Powershell, `.venv\Scripts\activate.ps1`:

```
> $env:FLASK_APP = "hello"
```

It is preferred to use dotenv support over this, since `.flaskenv` can be
committed to the repository so that it works automatically wherever the project
is checked out.

## Custom Commands

The `flask` command is implemented using [Click](https://click.palletsprojects.com/). See that project’s
documentation for full information about writing commands.

This example adds the command `create-user` that takes the argument
`name`.

```
import click
from flask import Flask

app = Flask(__name__)

@app.cli.command("create-user")
@click.argument("name")
def create_user(name):
    ...
```

```
$ flask create-user admin
```

This example adds the same command, but as `user create`, a command in a
group. This is useful if you want to organize multiple related commands.

```
import click
from flask import Flask
from flask.cli import AppGroup

app = Flask(__name__)
user_cli = AppGroup('user')

@user_cli.command('create')
@click.argument('name')
def create_user(name):
    ...

app.cli.add_command(user_cli)
```

```
$ flask user create demo
```

See [Running Commands with the CLI Runner](https://flask.palletsprojects.com/en/testing/#testing-cli) for an overview of how to test your custom
commands.

### Registering Commands with Blueprints

If your application uses blueprints, you can optionally register CLI
commands directly onto them. When your blueprint is registered onto your
application, the associated commands will be available to the `flask`
command. By default, those commands will be nested in a group matching
the name of the blueprint.

```
from flask import Blueprint

bp = Blueprint('students', __name__)

@bp.cli.command('create')
@click.argument('name')
def create(name):
    ...

app.register_blueprint(bp)
```

```
$ flask students create alice
```

You can alter the group name by specifying the `cli_group` parameter
when creating the [Blueprint](https://flask.palletsprojects.com/en/api/#flask.Blueprint) object, or later with
[app.register_blueprint(bp,cli_group='...')](https://flask.palletsprojects.com/en/api/#flask.Flask.register_blueprint).
The following are equivalent:

```
bp = Blueprint('students', __name__, cli_group='other')
# or
app.register_blueprint(bp, cli_group='other')
```

```
$ flask other create alice
```

Specifying `cli_group=None` will remove the nesting and merge the
commands directly to the application’s level:

```
bp = Blueprint('students', __name__, cli_group=None)
# or
app.register_blueprint(bp, cli_group=None)
```

```
$ flask create alice
```

### Application Context

Commands added using the Flask app’s [cli](https://flask.palletsprojects.com/en/api/#flask.Flask.cli) or
[FlaskGroup](https://flask.palletsprojects.com/en/api/#flask.cli.FlaskGroup) [command()](https://flask.palletsprojects.com/en/api/#flask.cli.AppGroup.command) decorator
will be executed with an application context pushed, so your custom
commands and parameters have access to the app and its configuration. The
[with_appcontext()](https://flask.palletsprojects.com/en/api/#flask.cli.with_appcontext) decorator can be used to get the same
behavior, but is not needed in most cases.

```
import click
from flask.cli import with_appcontext

@click.command()
@with_appcontext
def do_work():
    ...

app.cli.add_command(do_work)
```

## Plugins

Flask will automatically load commands specified in the `flask.commands` [entry point](https://packaging.python.org/tutorials/packaging-projects/#entry-points). This is useful for extensions that want to add commands when
they are installed. Entry points are specified in `pyproject.toml`:

```
[project.entry-points."flask.commands"]
my-command = "my_extension.commands:cli"
```

Inside `my_extension/commands.py` you can then export a Click
object:

```
import click

@click.command()
def cli():
    ...
```

Once that package is installed in the same virtualenv as your Flask project,
you can run `flask my-command` to invoke the command.

## Custom Scripts

When you are using the app factory pattern, it may be more convenient to define
your own Click script. Instead of using `--app` and letting Flask load
your application, you can create your own Click object and export it as a
[console script](https://packaging.python.org/tutorials/packaging-projects/#console-scripts) entry point.

Create an instance of [FlaskGroup](https://flask.palletsprojects.com/en/api/#flask.cli.FlaskGroup) and pass it the factory:

```
import click
from flask import Flask
from flask.cli import FlaskGroup

def create_app():
    app = Flask('wiki')
    # other setup
    return app

@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""
```

Define the entry point in `pyproject.toml`:

```
[project.scripts]
wiki = "wiki:cli"
```

Install the application in the virtualenv in editable mode and the custom
script is available. Note that you don’t need to set `--app`.

```
$ pip install -e .
$ wiki run
```

Errors in Custom Scripts

When using a custom script, if you introduce an error in your
module-level code, the reloader will fail because it can no longer
load the entry point.

The `flask` command, being separate from your code, does not have
this issue and is recommended in most cases.

## PyCharm Integration

PyCharm Professional provides a special Flask run configuration to run the development
server. For the Community Edition, and for other commands besides `run`, you need to
create a custom run configuration. These instructions should be similar for any other
IDE you use.

In PyCharm, with your project open, click on *Run* from the menu bar and go to *Edit
Configurations*. You’ll see a screen similar to this:

 ![Screenshot of PyCharm run configuration.](https://flask.palletsprojects.com/en/_images/pycharm-run-config.png)

Once you create a configuration for the `flask run`, you can copy and change it to
call any other command.

Click the *+ (Add New Configuration)* button and select *Python*. Give the configuration
a name such as “flask run”.

Click the *Script path* dropdown and change it to *Module name*, then input `flask`.

The *Parameters* field is set to the CLI command to execute along with any arguments.
This example uses `--app hello run --debug`, which will run the development server in
debug mode. `--app hello` should be the import or file with your Flask app.

If you installed your project as a package in your virtualenv, you may uncheck the
*PYTHONPATH* options. This will more accurately match how you deploy later.

Click *OK* to save and close the configuration. Select the configuration in the main
PyCharm window and click the play button next to it to run the server.

Now that you have a configuration for `flask run`, you can copy that configuration and
change the *Parameters* argument to run a different CLI command.

---

# Configuration Handling¶

# Configuration Handling

Applications need some kind of configuration.  There are different settings
you might want to change depending on the application environment like
toggling the debug mode, setting the secret key, and other such
environment-specific things.

The way Flask is designed usually requires the configuration to be
available when the application starts up.  You can hard code the
configuration in the code, which for many small applications is not
actually that bad, but there are better ways.

Independent of how you load your config, there is a config object
available which holds the loaded configuration values:
The [config](https://flask.palletsprojects.com/en/api/#flask.Flask.config) attribute of the [Flask](https://flask.palletsprojects.com/en/api/#flask.Flask)
object.  This is the place where Flask itself puts certain configuration
values and also where extensions can put their configuration values.  But
this is also where you can have your own configuration.

## Configuration Basics

The [config](https://flask.palletsprojects.com/en/api/#flask.Flask.config) is actually a subclass of a dictionary and
can be modified just like any dictionary:

```
app = Flask(__name__)
app.config['TESTING'] = True
```

Certain configuration values are also forwarded to the
[Flask](https://flask.palletsprojects.com/en/api/#flask.Flask) object so you can read and write them from there:

```
app.testing = True
```

To update multiple keys at once you can use the [dict.update()](https://docs.python.org/3/library/stdtypes.html#dict.update)
method:

```
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)
```

## Debug Mode

The [DEBUG](#DEBUG) config value is special because it may behave inconsistently if
changed after the app has begun setting up. In order to set debug mode reliably, use the
`--debug` option on the `flask` or `flask run` command. `flask run` will use the
interactive debugger and reloader by default in debug mode.

```
$ flask --app hello run --debug
```

Using the option is recommended. While it is possible to set [DEBUG](#DEBUG) in your
config or code, this is strongly discouraged. It can’t be read early by the
`flask run` command, and some systems or extensions may have already configured
themselves based on a previous value.

## Builtin Configuration Values

The following configuration values are used internally by Flask:

   DEBUG

Whether debug mode is enabled. When using `flask run` to start the development
server, an interactive debugger will be shown for unhandled exceptions, and the
server will be reloaded when code changes. The [debug](https://flask.palletsprojects.com/en/api/#flask.Flask.debug) attribute
maps to this config key. This is set with the `FLASK_DEBUG` environment variable.
It may not behave as expected if set in code.

**Do not enable debug mode when deploying in production.**

Default: `False`

    TESTING

Enable testing mode. Exceptions are propagated rather than handled by the
the app’s error handlers. Extensions may also change their behavior to
facilitate easier testing. You should enable this in your own tests.

Default: `False`

    PROPAGATE_EXCEPTIONS

Exceptions are re-raised rather than being handled by the app’s error
handlers. If not set, this is implicitly true if `TESTING` or `DEBUG`
is enabled.

Default: `None`

    TRAP_HTTP_EXCEPTIONS

If there is no handler for an `HTTPException`-type exception, re-raise it
to be handled by the interactive debugger instead of returning it as a
simple error response.

Default: `False`

    TRAP_BAD_REQUEST_ERRORS

Trying to access a key that doesn’t exist from request dicts like `args`
and `form` will return a 400 Bad Request error page. Enable this to treat
the error as an unhandled exception instead so that you get the interactive
debugger. This is a more specific version of `TRAP_HTTP_EXCEPTIONS`. If
unset, it is enabled in debug mode.

Default: `None`

    SECRET_KEY

A secret key that will be used for securely signing the session cookie
and can be used for any other security related needs by extensions or your
application. It should be a long random `bytes` or `str`. For
example, copy the output of this to your config:

```
$ python -c 'import secrets; print(secrets.token_hex())'
'192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```

**Do not reveal the secret key when posting questions or committing code.**

Default: `None`

    SECRET_KEY_FALLBACKS

A list of old secret keys that can still be used for unsigning. This allows
a project to implement key rotation without invalidating active sessions or
other recently-signed secrets.

Keys should be removed after an appropriate period of time, as checking each
additional key adds some overhead.

Order should not matter, but the default implementation will test the last
key in the list first, so it might make sense to order oldest to newest.

Flask’s built-in secure cookie session supports this. Extensions that use
[SECRET_KEY](#SECRET_KEY) may not support this yet.

Default: `None`

Added in version 3.1.

     SESSION_COOKIE_NAME

The name of the session cookie. Can be changed in case you already have a
cookie with the same name.

Default: `'session'`

    SESSION_COOKIE_DOMAIN

The value of the `Domain` parameter on the session cookie. If not set, browsers
will only send the cookie to the exact domain it was set from. Otherwise, they
will send it to any subdomain of the given value as well.

Not setting this value is more restricted and secure than setting it.

Default: `None`

Warning

If this is changed after the browser created a cookie is created with
one setting, it may result in another being created. Browsers may send
send both in an undefined order. In that case, you may want to change
[SESSION_COOKIE_NAME](#SESSION_COOKIE_NAME) as well or otherwise invalidate old sessions.

   Changelog

Changed in version 2.3: Not set by default, does not fall back to `SERVER_NAME`.

     SESSION_COOKIE_PATH

The path that the session cookie will be valid for. If not set, the cookie
will be valid underneath `APPLICATION_ROOT` or `/` if that is not set.

Default: `None`

    SESSION_COOKIE_HTTPONLY

Browsers will not allow JavaScript access to cookies marked as “HTTP only”
for security.

Default: `True`

    SESSION_COOKIE_SECURE

Browsers will only send cookies with requests over HTTPS if the cookie is
marked “secure”. The application must be served over HTTPS for this to make
sense.

Default: `False`

    SESSION_COOKIE_PARTITIONED

Browsers will send cookies based on the top-level document’s domain, rather
than only the domain of the document setting the cookie. This prevents third
party cookies set in iframes from “leaking” between separate sites.

Browsers are beginning to disallow non-partitioned third party cookies, so
you need to mark your cookies partitioned if you expect them to work in such
embedded situations.

Enabling this implicitly enables [SESSION_COOKIE_SECURE](#SESSION_COOKIE_SECURE) as well, as
it is only valid when served over HTTPS.

Default: `False`

Added in version 3.1.

     SESSION_COOKIE_SAMESITE

Restrict how cookies are sent with requests from external sites. Can
be set to `'Lax'` (recommended) or `'Strict'`.
See [Set-Cookie options](https://flask.palletsprojects.com/en/web-security/#security-cookie).

Default: `None`

  Changelog

Added in version 1.0.

     PERMANENT_SESSION_LIFETIME

If `session.permanent` is true, the cookie’s expiration will be set this
number of seconds in the future. Can either be a
[datetime.timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta) or an `int`.

Flask’s default cookie implementation validates that the cryptographic
signature is not older than this value.

Default: `timedelta(days=31)` (`2678400` seconds)

    SESSION_REFRESH_EACH_REQUEST

Control whether the cookie is sent with every response when
`session.permanent` is true. Sending the cookie every time (the default)
can more reliably keep the session from expiring, but uses more bandwidth.
Non-permanent sessions are not affected.

Default: `True`

    USE_X_SENDFILE

When serving files, set the `X-Sendfile` header instead of serving the
data with Flask. Some web servers, such as Apache, recognize this and serve
the data more efficiently. This only makes sense when using such a server.

Default: `False`

    SEND_FILE_MAX_AGE_DEFAULT

When serving files, set the cache control max age to this number of
seconds. Can be a [datetime.timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta) or an `int`.
Override this value on a per-file basis using
[get_send_file_max_age()](https://flask.palletsprojects.com/en/api/#flask.Flask.get_send_file_max_age) on the application or
blueprint.

If `None`, `send_file` tells the browser to use conditional
requests will be used instead of a timed cache, which is usually
preferable.

Default: `None`

    TRUSTED_HOSTS

Validate [Request.host](https://flask.palletsprojects.com/en/api/#flask.Request.host) and other attributes that use it against
these trusted values. Raise a [SecurityError](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.SecurityError) if
the host is invalid, which results in a 400 error. If it is `None`, all
hosts are valid. Each value is either an exact match, or can start with
a dot `.` to match any subdomain.

Validation is done during routing against this value. `before_request` and
`after_request` callbacks will still be called.

Default: `None`

Added in version 3.1.

     SERVER_NAME

Inform the application what host and port it is bound to.

Must be set if `subdomain_matching` is enabled, to be able to extract the
subdomain from the request.

Must be set for `url_for` to generate external URLs outside of a
request context.

Default: `None`

Changed in version 3.1: Does not restrict requests to only this domain, for both
`subdomain_matching` and `host_matching`.

   Changelog

Changed in version 2.3: Does not affect `SESSION_COOKIE_DOMAIN`.

Changed in version 1.0: Does not implicitly enable `subdomain_matching`.

     APPLICATION_ROOT

Inform the application what path it is mounted under by the application /
web server.  This is used for generating URLs outside the context of a
request (inside a request, the dispatcher is responsible for setting
`SCRIPT_NAME` instead; see [Application Dispatching](https://flask.palletsprojects.com/en/patterns/appdispatch/)
for examples of dispatch configuration).

Will be used for the session cookie path if `SESSION_COOKIE_PATH` is not
set.

Default: `'/'`

    PREFERRED_URL_SCHEME

Use this scheme for generating external URLs when not in a request context.

Default: `'http'`

    MAX_CONTENT_LENGTH

The maximum number of bytes that will be read during this request. If
this limit is exceeded, a 413 [RequestEntityTooLarge](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.RequestEntityTooLarge)
error is raised. If it is set to `None`, no limit is enforced at the
Flask application level. However, if it is `None` and the request has no
`Content-Length` header and the WSGI server does not indicate that it
terminates the stream, then no data is read to avoid an infinite stream.

Each request defaults to this config. It can be set on a specific
[Request.max_content_length](https://flask.palletsprojects.com/en/api/#flask.Request.max_content_length) to apply the limit to that specific
view. This should be set appropriately based on an application’s or view’s
specific needs.

Default: `None`

  Changelog

Added in version 0.6.

     MAX_FORM_MEMORY_SIZE

The maximum size in bytes any non-file form field may be in a
`multipart/form-data` body. If this limit is exceeded, a 413
[RequestEntityTooLarge](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.RequestEntityTooLarge) error is raised. If it is
set to `None`, no limit is enforced at the Flask application level.

Each request defaults to this config. It can be set on a specific
`Request.max_form_memory_parts` to apply the limit to that specific
view. This should be set appropriately based on an application’s or view’s
specific needs.

Default: `500_000`

Added in version 3.1.

     MAX_FORM_PARTS

The maximum number of fields that may be present in a
`multipart/form-data` body. If this limit is exceeded, a 413
[RequestEntityTooLarge](https://werkzeug.palletsprojects.com/en/stable/exceptions/#werkzeug.exceptions.RequestEntityTooLarge) error is raised. If it
is set to `None`, no limit is enforced at the Flask application level.

Each request defaults to this config. It can be set on a specific
[Request.max_form_parts](https://flask.palletsprojects.com/en/api/#flask.Request.max_form_parts) to apply the limit to that specific view.
This should be set appropriately based on an application’s or view’s
specific needs.

Default: `1_000`

Added in version 3.1.

     TEMPLATES_AUTO_RELOAD

Reload templates when they are changed. If not set, it will be enabled in
debug mode.

Default: `None`

    EXPLAIN_TEMPLATE_LOADING

Log debugging information tracing how a template file was loaded. This can
be useful to figure out why a template was not loaded or the wrong file
appears to be loaded.

Default: `False`

    MAX_COOKIE_SIZE

Warn if cookie headers are larger than this many bytes. Defaults to
`4093`. Larger cookies may be silently ignored by browsers. Set to
`0` to disable the warning.

    PROVIDE_AUTOMATIC_OPTIONS

Set to `False` to disable the automatic addition of OPTIONS
responses. This can be overridden per route by altering the
`provide_automatic_options` attribute.

Added in version 3.10: Added [PROVIDE_AUTOMATIC_OPTIONS](#PROVIDE_AUTOMATIC_OPTIONS) to control the default
addition of autogenerated OPTIONS responses.

   Changelog

Changed in version 2.3: `JSON_AS_ASCII`, `JSON_SORT_KEYS`, `JSONIFY_MIMETYPE`, and
`JSONIFY_PRETTYPRINT_REGULAR` were removed. The default `app.json` provider has
equivalent attributes instead.

Changed in version 2.3: `ENV` was removed.

Changed in version 2.2: Removed `PRESERVE_CONTEXT_ON_EXCEPTION`.

Changed in version 1.0: `LOGGER_NAME` and `LOGGER_HANDLER_POLICY` were removed. See
[Logging](https://flask.palletsprojects.com/en/logging/) for information about configuration.

Added `ENV` to reflect the `FLASK_ENV` environment
variable.

Added [SESSION_COOKIE_SAMESITE](#SESSION_COOKIE_SAMESITE) to control the session
cookie’s `SameSite` option.

Added [MAX_COOKIE_SIZE](#MAX_COOKIE_SIZE) to control a warning from Werkzeug.

Added in version 0.11: `SESSION_REFRESH_EACH_REQUEST`, `TEMPLATES_AUTO_RELOAD`,
`LOGGER_HANDLER_POLICY`, `EXPLAIN_TEMPLATE_LOADING`

Added in version 0.10: `JSON_AS_ASCII`, `JSON_SORT_KEYS`, `JSONIFY_PRETTYPRINT_REGULAR`

Added in version 0.9: `PREFERRED_URL_SCHEME`

Added in version 0.8: `TRAP_BAD_REQUEST_ERRORS`, `TRAP_HTTP_EXCEPTIONS`,
`APPLICATION_ROOT`, `SESSION_COOKIE_DOMAIN`,
`SESSION_COOKIE_PATH`, `SESSION_COOKIE_HTTPONLY`,
`SESSION_COOKIE_SECURE`

Added in version 0.7: `PROPAGATE_EXCEPTIONS`, `PRESERVE_CONTEXT_ON_EXCEPTION`

Added in version 0.6: `MAX_CONTENT_LENGTH`

Added in version 0.5: `SERVER_NAME`

Added in version 0.4: `LOGGER_NAME`

## Configuring from Python Files

Configuration becomes more useful if you can store it in a separate file, ideally
located outside the actual application package. You can deploy your application, then
separately configure it for the specific deployment.

A common pattern is this:

```
app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
```

This first loads the configuration from the
`yourapplication.default_settings` module and then overrides the values
with the contents of the file the `YOURAPPLICATION_SETTINGS`
environment variable points to.  This environment variable can be set
in the shell before starting the server:

```
$ export YOURAPPLICATION_SETTINGS=/path/to/settings.cfg
$ flask run
 * Running on http://127.0.0.1:5000/
```

```
$ set -x YOURAPPLICATION_SETTINGS /path/to/settings.cfg
$ flask run
 * Running on http://127.0.0.1:5000/
```

```
> set YOURAPPLICATION_SETTINGS=\path\to\settings.cfg
> flask run
 * Running on http://127.0.0.1:5000/
```

```
> $env:YOURAPPLICATION_SETTINGS = "\path\to\settings.cfg"
> flask run
 * Running on http://127.0.0.1:5000/
```

The configuration files themselves are actual Python files.  Only values
in uppercase are actually stored in the config object later on.  So make
sure to use uppercase letters for your config keys.

Here is an example of a configuration file:

```
# Example configuration
SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```

Make sure to load the configuration very early on, so that extensions have
the ability to access the configuration when starting up.  There are other
methods on the config object as well to load from individual files.  For a
complete reference, read the [Config](https://flask.palletsprojects.com/en/api/#flask.Config) object’s
documentation.

## Configuring from Data Files

It is also possible to load configuration from a file in a format of
your choice using [from_file()](https://flask.palletsprojects.com/en/api/#flask.Config.from_file). For example to load
from a TOML file:

```
import tomllib
app.config.from_file("config.toml", load=tomllib.load, text=False)
```

Or from a JSON file:

```
import json
app.config.from_file("config.json", load=json.load)
```

## Configuring from Environment Variables

In addition to pointing to configuration files using environment
variables, you may find it useful (or necessary) to control your
configuration values directly from the environment. Flask can be
instructed to load all environment variables starting with a specific
prefix into the config using [from_prefixed_env()](https://flask.palletsprojects.com/en/api/#flask.Config.from_prefixed_env).

Environment variables can be set in the shell before starting the
server:

```
$ export FLASK_SECRET_KEY="5f352379324c22463451387a0aec5d2f"
$ export FLASK_MAIL_ENABLED=false
$ flask run
 * Running on http://127.0.0.1:5000/
```

```
$ set -x FLASK_SECRET_KEY "5f352379324c22463451387a0aec5d2f"
$ set -x FLASK_MAIL_ENABLED false
$ flask run
 * Running on http://127.0.0.1:5000/
```

```
> set FLASK_SECRET_KEY="5f352379324c22463451387a0aec5d2f"
> set FLASK_MAIL_ENABLED=false
> flask run
 * Running on http://127.0.0.1:5000/
```

```
> $env:FLASK_SECRET_KEY = "5f352379324c22463451387a0aec5d2f"
> $env:FLASK_MAIL_ENABLED = "false"
> flask run
 * Running on http://127.0.0.1:5000/
```

The variables can then be loaded and accessed via the config with a key
equal to the environment variable name without the prefix i.e.

```
app.config.from_prefixed_env()
app.config["SECRET_KEY"]  # Is "5f352379324c22463451387a0aec5d2f"
```

The prefix is `FLASK_` by default. This is configurable via the
`prefix` argument of [from_prefixed_env()](https://flask.palletsprojects.com/en/api/#flask.Config.from_prefixed_env).

Values will be parsed to attempt to convert them to a more specific type
than strings. By default [json.loads()](https://docs.python.org/3/library/json.html#json.loads) is used, so any valid JSON
value is possible, including lists and dicts. This is configurable via
the `loads` argument of [from_prefixed_env()](https://flask.palletsprojects.com/en/api/#flask.Config.from_prefixed_env).

When adding a boolean value with the default JSON parsing, only “true”
and “false”, lowercase, are valid values. Keep in mind that any
non-empty string is considered `True` by Python.

It is possible to set keys in nested dictionaries by separating the
keys with double underscore (`__`). Any intermediate keys that don’t
exist on the parent dict will be initialized to an empty dict.

```
$ export FLASK_MYAPI__credentials__username=user123
```

```
app.config["MYAPI"]["credentials"]["username"]  # Is "user123"
```

On Windows, environment variable keys are always uppercase, therefore
the above example would end up as `MYAPI__CREDENTIALS__USERNAME`.

For even more config loading features, including merging and
case-insensitive Windows support, try a dedicated library such as
[Dynaconf](https://www.dynaconf.com/), which includes integration with Flask.

## Configuration Best Practices

The downside with the approach mentioned earlier is that it makes testing
a little harder.  There is no single 100% solution for this problem in
general, but there are a couple of things you can keep in mind to improve
that experience:

1. Create your application in a function and register blueprints on it.
  That way you can create multiple instances of your application with
  different configurations attached which makes unit testing a lot
  easier.  You can use this to pass in configuration as needed.
2. Do not write code that needs the configuration at import time.  If you
  limit yourself to request-only accesses to the configuration you can
  reconfigure the object later on as needed.
3. Make sure to load the configuration very early on, so that
  extensions can access the configuration when calling `init_app`.

## Development / Production

Most applications need more than one configuration.  There should be at
least separate configurations for the production server and the one used
during development.  The easiest way to handle this is to use a default
configuration that is always loaded and part of the version control, and a
separate configuration that overrides the values as necessary as mentioned
in the example above:

```
app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
```

Then you just have to add a separate `config.py` file and export
`YOURAPPLICATION_SETTINGS=/path/to/config.py` and you are done.  However
there are alternative ways as well.  For example you could use imports or
subclassing.

What is very popular in the Django world is to make the import explicit in
the config file by adding `from yourapplication.default_settings
import *` to the top of the file and then overriding the changes by hand.
You could also inspect an environment variable like
`YOURAPPLICATION_MODE` and set that to `production`, `development` etc
and import different hard-coded files based on that.

An interesting pattern is also to use classes and inheritance for
configuration:

```
class Config(object):
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DATABASE_URI = "sqlite:////tmp/foo.db"

class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
```

To enable such a config you just have to call into
[from_object()](https://flask.palletsprojects.com/en/api/#flask.Config.from_object):

```
app.config.from_object('configmodule.ProductionConfig')
```

Note that [from_object()](https://flask.palletsprojects.com/en/api/#flask.Config.from_object) does not instantiate the class
object. If you need to instantiate the class, such as to access a property,
then you must do so before calling [from_object()](https://flask.palletsprojects.com/en/api/#flask.Config.from_object):

```
from configmodule import ProductionConfig
app.config.from_object(ProductionConfig())

# Alternatively, import via string:
from werkzeug.utils import import_string
cfg = import_string('configmodule.ProductionConfig')()
app.config.from_object(cfg)
```

Instantiating the configuration object allows you to use `@property` in
your configuration classes:

```
class Config(object):
    """Base config, uses staging database server."""
    TESTING = False
    DB_SERVER = '192.168.1.56'

    @property
    def DATABASE_URI(self):  # Note: all caps
        return f"mysql://user@{self.DB_SERVER}/foo"

class ProductionConfig(Config):
    """Uses production database server."""
    DB_SERVER = '192.168.19.32'

class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'

class TestingConfig(Config):
    DB_SERVER = 'localhost'
    DATABASE_URI = 'sqlite:///:memory:'
```

There are many different ways and it’s up to you how you want to manage
your configuration files.  However here a list of good recommendations:

- Keep a default configuration in version control.  Either populate the
  config with this default configuration or import it in your own
  configuration files before overriding values.
- Use an environment variable to switch between the configurations.
  This can be done from outside the Python interpreter and makes
  development and deployment much easier because you can quickly and
  easily switch between different configs without having to touch the
  code at all.  If you are working often on different projects you can
  even create your own script for sourcing that activates a virtualenv
  and exports the development configuration for you.
- Use a tool like [fabric](https://www.fabfile.org/) to push code and configuration separately
  to the production server(s).

## Instance Folders

  Changelog

Added in version 0.8.

Flask 0.8 introduces instance folders.  Flask for a long time made it
possible to refer to paths relative to the application’s folder directly
(via `Flask.root_path`).  This was also how many developers loaded
configurations stored next to the application.  Unfortunately however this
only works well if applications are not packages in which case the root
path refers to the contents of the package.

With Flask 0.8 a new attribute was introduced:
`Flask.instance_path`.  It refers to a new concept called the
“instance folder”.  The instance folder is designed to not be under
version control and be deployment specific.  It’s the perfect place to
drop things that either change at runtime or configuration files.

You can either explicitly provide the path of the instance folder when
creating the Flask application or you can let Flask autodetect the
instance folder.  For explicit configuration use the `instance_path`
parameter:

```
app = Flask(__name__, instance_path='/path/to/instance/folder')
```

Please keep in mind that this path *must* be absolute when provided.

If the `instance_path` parameter is not provided the following default
locations are used:

- Uninstalled module:
  ```
  /myapp.py
  /instance
  ```
- Uninstalled package:
  ```
  /myapp
      /__init__.py
  /instance
  ```
- Installed module or package:
  ```
  $PREFIX/lib/pythonX.Y/site-packages/myapp
  $PREFIX/var/myapp-instance
  ```
  `$PREFIX` is the prefix of your Python installation.  This can be
  `/usr` or the path to your virtualenv.  You can print the value of
  `sys.prefix` to see what the prefix is set to.

Since the config object provided loading of configuration files from
relative filenames we made it possible to change the loading via filenames
to be relative to the instance path if wanted.  The behavior of relative
paths in config files can be flipped between “relative to the application
root” (the default) to “relative to instance folder” via the
`instance_relative_config` switch to the application constructor:

```
app = Flask(__name__, instance_relative_config=True)
```

Here is a full example of how to configure Flask to preload the config
from a module and then override the config from a file in the instance
folder if it exists:

```
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('yourapplication.default_settings')
app.config.from_pyfile('application.cfg', silent=True)
```

The path to the instance folder can be found via the
`Flask.instance_path`.  Flask also provides a shortcut to open a
file from the instance folder with `Flask.open_instance_resource()`.

Example usage for both:

```
filename = os.path.join(app.instance_path, 'application.cfg')
with open(filename) as f:
    config = f.read()

# or via open_instance_resource:
with app.open_instance_resource('application.cfg') as f:
    config = f.read()
```

---

# Contributing¶

# Contributing

See the Pallets [detailed contributing documentation](https://palletsprojects.com/contributing/) for many ways
to contribute, including reporting issues, requesting features, asking or
answering questions, and making PRs.
