# How to deploy with ASGI¶ and more

# How to deploy with ASGI¶

# How to deploy with ASGI¶

As well as WSGI, Django also supports deploying on [ASGI](https://asgi.readthedocs.io/en/latest/), the emerging Python
standard for asynchronous web servers and applications.

Django’s [startproject](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-startproject) management command sets up a default ASGI
configuration for you, which you can tweak as needed for your project, and
direct any ASGI-compliant application server to use.

Django includes getting-started documentation for the following ASGI servers:

## Theapplicationobject¶

Like WSGI, ASGI has you supply an `application` callable which
the application server uses to communicate with your code. It’s commonly
provided as an object named `application` in a Python module accessible to
the server.

The [startproject](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-startproject) command creates a file
`<project_name>/asgi.py` that contains such an `application` callable.

It’s not used by the development server (`runserver`), but can be used by
any ASGI server either in development or in production.

ASGI servers usually take the path to the application callable as a string;
for most Django projects, this will look like `myproject.asgi:application`.

Warning

While Django’s default ASGI handler will run all your code in a synchronous
thread, if you choose to run your own async handler you must be aware of
async-safety.

Do not call blocking synchronous functions or libraries in any async code.
Django prevents you from doing this with the parts of Django that are not
async-safe, but the same may not be true of third-party apps or Python
libraries.

## Configuring the settings module¶

When the ASGI server loads your application, Django needs to import the
settings module — that’s where your entire application is defined.

Django uses the [DJANGO_SETTINGS_MODULE](https://docs.djangoproject.com/en/topics/settings/#envvar-DJANGO_SETTINGS_MODULE) environment variable to locate
the appropriate settings module. It must contain the dotted path to the
settings module. You can use a different value for development and production;
it all depends on how you organize your settings.

If this variable isn’t set, the default `asgi.py` sets it to
`mysite.settings`, where `mysite` is the name of your project.

## Applying ASGI middleware¶

To apply ASGI middleware, or to embed Django in another ASGI application, you
can wrap Django’s `application` object in the `asgi.py` file. For example:

```
from some_asgi_library import AmazingMiddleware

application = AmazingMiddleware(application)
```

---

# Deployment checklist¶

# Deployment checklist¶

The internet is a hostile environment. Before deploying your Django project,
you should take some time to review your settings, with security, performance,
and operations in mind.

Django includes many [security features](https://docs.djangoproject.com/en/topics/security/). Some are
built-in and always enabled. Others are optional because they aren’t always
appropriate, or because they’re inconvenient for development. For example,
forcing HTTPS may not be suitable for all websites, and it’s impractical for
local development.

Performance optimizations are another category of trade-offs with convenience.
For instance, caching is useful in production, less so for local development.
Error reporting needs are also widely different.

The following checklist includes settings that:

- must be set properly for Django to provide the expected level of security;
- are expected to be different in each environment;
- enable optional security features;
- enable performance optimizations;
- provide error reporting.

Many of these settings are sensitive and should be treated as confidential. If
you’re releasing the source code for your project, a common practice is to
publish suitable settings for development, and to use a private settings
module for production.

## Runmanage.pycheck--deploy¶

Some of the checks described below can be automated using the [check--deploy](https://docs.djangoproject.com/en/ref/django-admin/#cmdoption-check-deploy) option. Be sure to run it against your production settings file as
described in the option’s documentation.

## Critical settings¶

### SECRET_KEY¶

**The secret key must be a large random value and it must be kept secret.**

Make sure that the key used in production isn’t used anywhere else and avoid
committing it to source control. This reduces the number of vectors from which
an attacker may acquire the key.

Instead of hardcoding the secret key in your settings module, consider loading
it from an environment variable:

```
import os

SECRET_KEY = os.environ["SECRET_KEY"]
```

or from a file:

```
with open("/etc/secret_key.txt") as f:
    SECRET_KEY = f.read().strip()
```

If rotating secret keys, you may use [SECRET_KEY_FALLBACKS](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECRET_KEY_FALLBACKS):

```
import os

SECRET_KEY = os.environ["CURRENT_SECRET_KEY"]
SECRET_KEY_FALLBACKS = [
    os.environ["OLD_SECRET_KEY"],
]
```

Ensure that old secret keys are removed from `SECRET_KEY_FALLBACKS` in a
timely manner.

### DEBUG¶

**You must never enable debug in production.**

You’re certainly developing your project with [DEBUG=True](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG),
since this enables handy features like full tracebacks in your browser.

For a production environment, though, this is a really bad idea, because it
leaks lots of information about your project: excerpts of your source code,
local variables, settings, libraries used, etc.

## Environment-specific settings¶

### ALLOWED_HOSTS¶

When [DEBUG=False](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG), Django doesn’t work at all without a
suitable value for [ALLOWED_HOSTS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ALLOWED_HOSTS).

This setting is required to protect your site against some CSRF attacks. If
you use a wildcard, you must perform your own validation of the `Host` HTTP
header, or otherwise ensure that you aren’t vulnerable to this category of
attacks.

You should also configure the web server that sits in front of Django to
validate the host. It should respond with a static error page or ignore
requests for incorrect hosts instead of forwarding the request to Django. This
way you’ll avoid spurious errors in your Django logs (or emails if you have
error reporting configured that way). For example, on nginx you might set up a
default server to return “444 No Response” on an unrecognized host:

```
server {
    listen 80 default_server;
    return 444;
}
```

### CACHES¶

If you’re using a cache, connection parameters may be different in development
and in production. Django defaults to per-process [local-memory caching](https://docs.djangoproject.com/en/topics/cache/#local-memory-caching) which may not be desirable.

Cache servers often have weak authentication. Make sure they only accept
connections from your application servers.

### DATABASES¶

Database connection parameters are probably different in development and in
production.

Database passwords are very sensitive. You should protect them exactly like
[SECRET_KEY](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECRET_KEY).

For maximum security, make sure database servers only accept connections from
your application servers.

If you haven’t set up backups for your database, do it right now!

### EMAIL_BACKENDand related settings¶

If your site sends emails, these values need to be set correctly.

By default, Django sends email from [webmaster@localhost](mailto:webmaster%40localhost) and [root@localhost](mailto:root%40localhost).
However, some mail providers reject email from these addresses. To use
different sender addresses, modify the [DEFAULT_FROM_EMAIL](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEFAULT_FROM_EMAIL) and
[SERVER_EMAIL](https://docs.djangoproject.com/en/ref/settings/#std-setting-SERVER_EMAIL) settings.

### STATIC_ROOTandSTATIC_URL¶

Static files are automatically served by the development server. In
production, you must define a [STATIC_ROOT](https://docs.djangoproject.com/en/ref/settings/#std-setting-STATIC_ROOT) directory where
[collectstatic](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#django-admin-collectstatic) will copy them.

See [How to manage static files (e.g. images, JavaScript, CSS)](https://docs.djangoproject.com/en/5.0/static-files/) for more information.

### MEDIA_ROOTandMEDIA_URL¶

Media files are uploaded by your users. They’re untrusted! Make sure your web
server never attempts to interpret them. For instance, if a user uploads a
`.php` file, the web server shouldn’t execute it.

Now is a good time to check your backup strategy for these files.

## HTTPS¶

Any website which allows users to log in should enforce site-wide HTTPS to
avoid transmitting access tokens in clear. In Django, access tokens include
the login/password, the session cookie, and password reset tokens. (You can’t
do much to protect password reset tokens if you’re sending them by email.)

Protecting sensitive areas such as the user account or the admin isn’t
sufficient, because the same session cookie is used for HTTP and HTTPS. Your
web server must redirect all HTTP traffic to HTTPS, and only transmit HTTPS
requests to Django.

Once you’ve set up HTTPS, enable the following settings.

### CSRF_COOKIE_SECURE¶

Set this to `True` to avoid transmitting the CSRF cookie over HTTP
accidentally.

### SESSION_COOKIE_SECURE¶

Set this to `True` to avoid transmitting the session cookie over HTTP
accidentally.

## Performance optimizations¶

Setting [DEBUG=False](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) disables several features that are
only useful in development. In addition, you can tune the following settings.

### Sessions¶

Consider using [cached sessions](https://docs.djangoproject.com/en/topics/http/sessions/#cached-sessions-backend) to improve
performance.

If using database-backed sessions, regularly [clear old sessions](https://docs.djangoproject.com/en/topics/http/sessions/#clearing-the-session-store) to avoid storing unnecessary data.

### CONN_MAX_AGE¶

Enabling [persistent database connections](https://docs.djangoproject.com/en/ref/databases/#persistent-database-connections) can result in a nice speed-up when
connecting to the database accounts for a significant part of the request
processing time.

This helps a lot on virtualized hosts with limited network performance.

### TEMPLATES¶

Enabling the cached template loader often improves performance drastically, as
it avoids compiling each template every time it needs to be rendered. When
[DEBUG=False](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG), the cached template loader is enabled
automatically. See [django.template.loaders.cached.Loader](https://docs.djangoproject.com/en/ref/templates/api/#django.template.loaders.cached.Loader) for more
information.

## Error reporting¶

By the time you push your code to production, it’s hopefully robust, but you
can’t rule out unexpected errors. Thankfully, Django can capture errors and
notify you accordingly.

### LOGGING¶

Review your logging configuration before putting your website in production,
and check that it works as expected as soon as you have received some traffic.

See [Logging](https://docs.djangoproject.com/en/topics/logging/) for details on logging.

### ADMINSandMANAGERS¶

[ADMINS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ADMINS) will be notified of 500 errors by email.

[MANAGERS](https://docs.djangoproject.com/en/ref/settings/#std-setting-MANAGERS) will be notified of 404 errors.
[IGNORABLE_404_URLS](https://docs.djangoproject.com/en/ref/settings/#std-setting-IGNORABLE_404_URLS) can help filter out spurious reports.

See [How to manage error reporting](https://docs.djangoproject.com/en/5.0/error-reporting/) for details on error reporting by email.

Error reporting by email doesn’t scale very well

Consider using an error monitoring system such as [Sentry](https://docs.sentry.io/) before your
inbox is flooded by reports. Sentry can also aggregate logs.

### Customize the default error views¶

Django includes default views and templates for several HTTP error codes. You
may want to override the default templates by creating the following templates
in your root template directory: `404.html`, `500.html`, `403.html`, and
`400.html`. The [default error views](https://docs.djangoproject.com/en/ref/views/#error-views) that use these
templates should suffice for 99% of web applications, but you can
[customize them](https://docs.djangoproject.com/en/topics/http/views/#customizing-error-views) as well.

---

# How to deploy with WSGI¶

# How to deploy with WSGI¶

Django’s primary deployment platform is [WSGI](https://wsgi.readthedocs.io/en/latest/), the Python standard for web
servers and applications.

Django’s [startproject](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-startproject) management command sets up a minimal default
WSGI configuration for you, which you can tweak as needed for your project,
and direct any WSGI-compliant application server to use.

Django includes getting-started documentation for the following WSGI servers:

## Theapplicationobject¶

The key concept of deploying with WSGI is the `application` callable which
the application server uses to communicate with your code. It’s commonly
provided as an object named `application` in a Python module accessible to
the server.

The [startproject](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-startproject) command creates a file
`<project_name>/wsgi.py` that contains such an `application` callable.

It’s used both by Django’s development server and in production WSGI
deployments.

WSGI servers obtain the path to the `application` callable from their
configuration. Django’s built-in server, namely the [runserver](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-runserver)
command, reads it from the [WSGI_APPLICATION](https://docs.djangoproject.com/en/ref/settings/#std-setting-WSGI_APPLICATION) setting. By default, it’s
set to `<project_name>.wsgi.application`, which points to the `application`
callable in `<project_name>/wsgi.py`.

## Configuring the settings module¶

When the WSGI server loads your application, Django needs to import the
settings module — that’s where your entire application is defined.

Django uses the [DJANGO_SETTINGS_MODULE](https://docs.djangoproject.com/en/topics/settings/#envvar-DJANGO_SETTINGS_MODULE) environment variable to
locate the appropriate settings module. It must contain the dotted path to the
settings module. You can use a different value for development and production;
it all depends on how you organize your settings.

If this variable isn’t set, the default `wsgi.py` sets it to
`mysite.settings`, where `mysite` is the name of your project. That’s how
[runserver](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-runserver) discovers the default settings file by default.

Note

Since environment variables are process-wide, this doesn’t work when you
run multiple Django sites in the same process. This happens with mod_wsgi.

To avoid this problem, use mod_wsgi’s daemon mode with each site in its
own daemon process, or override the value from the environment by
enforcing `os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"` in
your `wsgi.py`.

## Applying WSGI middleware¶

To apply [WSGI middleware](https://peps.python.org/pep-3333/#middleware-components-that-play-both-sides) you can wrap the application
object. For instance you could add these lines at the bottom of
`wsgi.py`:

```
from helloworld.wsgi import HelloWorldApplication

application = HelloWorldApplication(application)
```

You could also replace the Django WSGI application with a custom WSGI
application that later delegates to the Django WSGI application, if you want
to combine a Django application with a WSGI application of another framework.

---

# How to deploy Django¶

# How to deploy Django¶

Django is full of shortcuts to make web developers’ lives easier, but all
those tools are of no use if you can’t easily deploy your sites. Since Django’s
inception, ease of deployment has been a major goal.

There are many options for deploying your Django application, based on your
architecture or your particular business needs, but that discussion is outside
the scope of what Django can give you as guidance.

Django, being a web framework, needs a web server in order to operate. And
since most web servers don’t natively speak Python, we need an interface to
make that communication happen.

Django currently supports two interfaces: WSGI and ASGI.

- [WSGI](https://wsgi.readthedocs.io/en/latest/) is the main Python standard for communicating between web servers and
  applications, but it only supports synchronous code.
- [ASGI](https://asgi.readthedocs.io/en/latest/) is the new, asynchronous-friendly standard that will allow your
  Django site to use asynchronous Python features, and asynchronous Django
  features as they are developed.

You should also consider how you will handle [static files](https://docs.djangoproject.com/en/5.0/static-files/deployment/) for your application, and how to handle
[error reporting](https://docs.djangoproject.com/en/5.0/error-reporting/).

Finally, before you deploy your application to production, you should run
through our [deployment checklist](https://docs.djangoproject.com/en/5.0/howto/checklist/) to ensure that your
configurations are suitable.

---

# How to manage error reporting¶

# How to manage error reporting¶

When you’re running a public site you should always turn off the
[DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) setting. That will make your server run much faster, and will
also prevent malicious users from seeing details of your application that can be
revealed by the error pages.

However, running with [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) set to `False` means you’ll never see
errors generated by your site – everyone will instead see your public error
pages. You need to keep track of errors that occur in deployed sites, so Django
can be configured to create reports with details about those errors.

## Email reports¶

### Server errors¶

When [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) is `False`, Django will email the users listed in the
[ADMINS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ADMINS) setting whenever your code raises an unhandled exception and
results in an internal server error (strictly speaking, for any response with
an HTTP status code of 500 or greater). This gives the administrators immediate
notification of any errors. The [ADMINS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ADMINS) will get a description of the
error, a complete Python traceback, and details about the HTTP request that
caused the error.

Note

In order to send email, Django requires a few settings telling it
how to connect to your mail server. At the very least, you’ll need
to specify [EMAIL_HOST](https://docs.djangoproject.com/en/ref/settings/#std-setting-EMAIL_HOST) and possibly
[EMAIL_HOST_USER](https://docs.djangoproject.com/en/ref/settings/#std-setting-EMAIL_HOST_USER) and [EMAIL_HOST_PASSWORD](https://docs.djangoproject.com/en/ref/settings/#std-setting-EMAIL_HOST_PASSWORD),
though other settings may be also required depending on your mail
server’s configuration. Consult [the Django settings
documentation](https://docs.djangoproject.com/en/ref/settings/) for a full list of email-related
settings.

By default, Django will send email from [root@localhost](mailto:root%40localhost). However, some mail
providers reject all email from this address. To use a different sender
address, modify the [SERVER_EMAIL](https://docs.djangoproject.com/en/ref/settings/#std-setting-SERVER_EMAIL) setting.

To activate this behavior, put the email addresses of the recipients in the
[ADMINS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ADMINS) setting.

See also

Server error emails are sent using the logging framework, so you can
customize this behavior by [customizing your logging configuration](https://docs.djangoproject.com/en/topics/logging/).

### 404 errors¶

Django can also be configured to email errors about broken links (404 “page
not found” errors). Django sends emails about 404 errors when:

- [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) is `False`;
- Your [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE) setting includes
  [django.middleware.common.BrokenLinkEmailsMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.common.BrokenLinkEmailsMiddleware).

If those conditions are met, Django will email the users listed in the
[MANAGERS](https://docs.djangoproject.com/en/ref/settings/#std-setting-MANAGERS) setting whenever your code raises a 404 and the request has
a referer. It doesn’t bother to email for 404s that don’t have a referer –
those are usually people typing in broken URLs or broken web bots. It also
ignores 404s when the referer is equal to the requested URL, since this
behavior is from broken web bots too.

Note

[BrokenLinkEmailsMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.common.BrokenLinkEmailsMiddleware) must appear
before other middleware that intercepts 404 errors, such as
[LocaleMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.locale.LocaleMiddleware) or
[FlatpageFallbackMiddleware](https://docs.djangoproject.com/en/ref/contrib/flatpages/#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware).
Put it toward the top of your [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE) setting.

You can tell Django to stop reporting particular 404s by tweaking the
[IGNORABLE_404_URLS](https://docs.djangoproject.com/en/ref/settings/#std-setting-IGNORABLE_404_URLS) setting. It should be a list of compiled
regular expression objects. For example:

```
import re

IGNORABLE_404_URLS = [
    re.compile(r"\.(php|cgi)$"),
    re.compile(r"^/phpmyadmin/"),
]
```

In this example, a 404 to any URL ending with `.php` or `.cgi` will *not* be
reported. Neither will any URL starting with `/phpmyadmin/`.

The following example shows how to exclude some conventional URLs that browsers and
crawlers often request:

```
import re

IGNORABLE_404_URLS = [
    re.compile(r"^/apple-touch-icon.*\.png$"),
    re.compile(r"^/favicon\.ico$"),
    re.compile(r"^/robots\.txt$"),
]
```

(Note that these are regular expressions, so we put a backslash in front of
periods to escape them.)

If you’d like to customize the behavior of
[django.middleware.common.BrokenLinkEmailsMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.common.BrokenLinkEmailsMiddleware) further (for
example to ignore requests coming from web crawlers), you should subclass it
and override its methods.

See also

404 errors are logged using the logging framework. By default, these log
records are ignored, but you can use them for error reporting by writing a
handler and [configuring logging](https://docs.djangoproject.com/en/topics/logging/) appropriately.

## Filtering error reports¶

Warning

Filtering sensitive data is a hard problem, and it’s nearly impossible to
guarantee that sensitive data won’t leak into an error report. Therefore,
error reports should only be available to trusted team members and you
should avoid transmitting error reports unencrypted over the internet
(such as through email).

### Filtering sensitive information¶

Error reports are really helpful for debugging errors, so it is generally
useful to record as much relevant information about those errors as possible.
For example, by default Django records the [full traceback](https://en.wikipedia.org/wiki/Stack_trace) for the
exception raised, each [traceback frame](https://en.wikipedia.org/wiki/Stack_frame)’s local variables, and the
[HttpRequest](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest)’s [attributes](https://docs.djangoproject.com/en/ref/request-response/#httprequest-attributes).

However, sometimes certain types of information may be too sensitive and thus
may not be appropriate to be kept track of, for example a user’s password or
credit card number. So in addition to filtering out settings that appear to be
sensitive as described in the [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) documentation, Django offers a
set of function decorators to help you control which information should be
filtered out of error reports in a production environment (that is, where
[DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) is set to `False`): [sensitive_variables()](#django.views.decorators.debug.sensitive_variables) and
[sensitive_post_parameters()](#django.views.decorators.debug.sensitive_post_parameters).

   sensitive_variables(**variables*)[[source]](https://docs.djangoproject.com/en/_modules/django/views/decorators/debug/#sensitive_variables)[¶](#django.views.decorators.debug.sensitive_variables)

If a function (either a view or any regular callback) in your code uses
local variables susceptible to contain sensitive information, you may
prevent the values of those variables from being included in error reports
using the `sensitive_variables` decorator:

```
from django.views.decorators.debug import sensitive_variables

@sensitive_variables("user", "pw", "cc")
def process_info(user):
    pw = user.pass_word
    cc = user.credit_card_number
    name = user.name
    ...
```

In the above example, the values for the `user`, `pw` and `cc`
variables will be hidden and replaced with stars (`**********`)
in the error reports, whereas the value of the `name` variable will be
disclosed.

To systematically hide all local variables of a function from error logs,
do not provide any argument to the `sensitive_variables` decorator:

```
@sensitive_variables()
def my_function(): ...
```

When using multiple decorators

If the variable you want to hide is also a function argument (e.g.
‘`user`’ in the following example), and if the decorated function has
multiple decorators, then make sure to place `@sensitive_variables`
at the top of the decorator chain. This way it will also hide the
function argument as it gets passed through the other decorators:

```
@sensitive_variables("user", "pw", "cc")
@some_decorator
@another_decorator
def process_info(user): ...
```

    Changed in Django 5.0:

Support for wrapping `async` functions was added.

     sensitive_post_parameters(**parameters*)[[source]](https://docs.djangoproject.com/en/_modules/django/views/decorators/debug/#sensitive_post_parameters)[¶](#django.views.decorators.debug.sensitive_post_parameters)

If one of your views receives an [HttpRequest](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest) object
with [POSTparameters](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.POST) susceptible to
contain sensitive information, you may prevent the values of those
parameters from being included in the error reports using the
`sensitive_post_parameters` decorator:

```
from django.views.decorators.debug import sensitive_post_parameters

@sensitive_post_parameters("pass_word", "credit_card_number")
def record_user_profile(request):
    UserProfile.create(
        user=request.user,
        password=request.POST["pass_word"],
        credit_card=request.POST["credit_card_number"],
        name=request.POST["name"],
    )
    ...
```

In the above example, the values for the `pass_word` and
`credit_card_number` POST parameters will be hidden and replaced with
stars (`**********`) in the request’s representation inside the
error reports, whereas the value of the `name` parameter will be
disclosed.

To systematically hide all POST parameters of a request in error reports,
do not provide any argument to the `sensitive_post_parameters` decorator:

```
@sensitive_post_parameters()
def my_view(request): ...
```

All POST parameters are systematically filtered out of error reports for
certain [django.contrib.auth.views](https://docs.djangoproject.com/en/topics/auth/default/#module-django.contrib.auth.views) views (`login`,
`password_reset_confirm`, `password_change`, and `add_view` and
`user_change_password` in the `auth` admin) to prevent the leaking of
sensitive information such as user passwords.

  Changed in Django 5.0:

Support for wrapping `async` functions was added.

### Custom error reports¶

All [sensitive_variables()](#django.views.decorators.debug.sensitive_variables) and [sensitive_post_parameters()](#django.views.decorators.debug.sensitive_post_parameters) do is,
respectively, annotate the decorated function with the names of sensitive
variables and annotate the `HttpRequest` object with the names of sensitive
POST parameters, so that this sensitive information can later be filtered out
of reports when an error occurs. The actual filtering is done by Django’s
default error reporter filter:
[django.views.debug.SafeExceptionReporterFilter](#django.views.debug.SafeExceptionReporterFilter). This filter uses the
decorators’ annotations to replace the corresponding values with stars
(`**********`) when the error reports are produced. If you wish to
override or customize this default behavior for your entire site, you need to
define your own filter class and tell Django to use it via the
[DEFAULT_EXCEPTION_REPORTER_FILTER](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEFAULT_EXCEPTION_REPORTER_FILTER) setting:

```
DEFAULT_EXCEPTION_REPORTER_FILTER = "path.to.your.CustomExceptionReporterFilter"
```

You may also control in a more granular way which filter to use within any
given view by setting the `HttpRequest`’s `exception_reporter_filter`
attribute:

```
def my_view(request):
    if request.user.is_authenticated:
        request.exception_reporter_filter = CustomExceptionReporterFilter()
    ...
```

Your custom filter class needs to inherit from
[django.views.debug.SafeExceptionReporterFilter](#django.views.debug.SafeExceptionReporterFilter) and may override the
following attributes and methods:

   *class*SafeExceptionReporterFilter[[source]](https://docs.djangoproject.com/en/_modules/django/views/debug/#SafeExceptionReporterFilter)[¶](#django.views.debug.SafeExceptionReporterFilter)   cleansed_substitute[¶](#django.views.debug.SafeExceptionReporterFilter.cleansed_substitute)

The string value to replace sensitive value with. By default it
replaces the values of sensitive variables with stars
(`**********`).

    hidden_settings[¶](#django.views.debug.SafeExceptionReporterFilter.hidden_settings)

A compiled regular expression object used to match settings and
`request.META` values considered as sensitive. By default equivalent
to:

```
import re

re.compile(r"API|TOKEN|KEY|SECRET|PASS|SIGNATURE|HTTP_COOKIE", flags=re.IGNORECASE)
```

   Changed in Django 4.2:

`HTTP_COOKIE` was added.

     is_active(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/views/debug/#SafeExceptionReporterFilter.is_active)[¶](#django.views.debug.SafeExceptionReporterFilter.is_active)

Returns `True` to activate the filtering in
[get_post_parameters()](#django.views.debug.SafeExceptionReporterFilter.get_post_parameters) and [get_traceback_frame_variables()](#django.views.debug.SafeExceptionReporterFilter.get_traceback_frame_variables).
By default the filter is active if [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) is `False`. Note
that sensitive `request.META` values are always filtered along with
sensitive setting values, as described in the [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG)
documentation.

    get_post_parameters(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/views/debug/#SafeExceptionReporterFilter.get_post_parameters)[¶](#django.views.debug.SafeExceptionReporterFilter.get_post_parameters)

Returns the filtered dictionary of POST parameters. Sensitive values
are replaced with [cleansed_substitute](#django.views.debug.SafeExceptionReporterFilter.cleansed_substitute).

    get_traceback_frame_variables(*request*, *tb_frame*)[[source]](https://docs.djangoproject.com/en/_modules/django/views/debug/#SafeExceptionReporterFilter.get_traceback_frame_variables)[¶](#django.views.debug.SafeExceptionReporterFilter.get_traceback_frame_variables)

Returns the filtered dictionary of local variables for the given
traceback frame. Sensitive values are replaced with
[cleansed_substitute](#django.views.debug.SafeExceptionReporterFilter.cleansed_substitute).

If you need to customize error reports beyond filtering you may specify a
custom error reporter class by defining the
[DEFAULT_EXCEPTION_REPORTER](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEFAULT_EXCEPTION_REPORTER) setting:

```
DEFAULT_EXCEPTION_REPORTER = "path.to.your.CustomExceptionReporter"
```

The exception reporter is responsible for compiling the exception report data,
and formatting it as text or HTML appropriately. (The exception reporter uses
[DEFAULT_EXCEPTION_REPORTER_FILTER](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEFAULT_EXCEPTION_REPORTER_FILTER) when preparing the exception
report data.)

Your custom reporter class needs to inherit from
[django.views.debug.ExceptionReporter](#django.views.debug.ExceptionReporter).

   *class*ExceptionReporter[[source]](https://docs.djangoproject.com/en/_modules/django/views/debug/#ExceptionReporter)[¶](#django.views.debug.ExceptionReporter)   html_template_path[¶](#django.views.debug.ExceptionReporter.html_template_path)

Property that returns a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) representing the absolute
filesystem path to a template for rendering the HTML representation of
the exception. Defaults to the Django provided template.

    text_template_path[¶](#django.views.debug.ExceptionReporter.text_template_path)

Property that returns a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) representing the absolute
filesystem path to a template for rendering the plain-text
representation of the exception. Defaults to the Django provided
template.

    get_traceback_data()[[source]](https://docs.djangoproject.com/en/_modules/django/views/debug/#ExceptionReporter.get_traceback_data)[¶](#django.views.debug.ExceptionReporter.get_traceback_data)

Return a dictionary containing traceback information.

This is the main extension point for customizing exception reports, for
example:

```
from django.views.debug import ExceptionReporter

class CustomExceptionReporter(ExceptionReporter):
    def get_traceback_data(self):
        data = super().get_traceback_data()
        # ... remove/add something here ...
        return data
```

     get_traceback_html()[[source]](https://docs.djangoproject.com/en/_modules/django/views/debug/#ExceptionReporter.get_traceback_html)[¶](#django.views.debug.ExceptionReporter.get_traceback_html)

Return HTML version of exception report.

Used for HTML version of debug 500 HTTP error page.

    get_traceback_text()[[source]](https://docs.djangoproject.com/en/_modules/django/views/debug/#ExceptionReporter.get_traceback_text)[¶](#django.views.debug.ExceptionReporter.get_traceback_text)

Return plain text version of exception report.

Used for plain text version of debug 500 HTTP error page and email
reports.

As with the filter class, you may control which exception reporter class to use
within any given view by setting the `HttpRequest`’s
`exception_reporter_class` attribute:

```
def my_view(request):
    if request.user.is_authenticated:
        request.exception_reporter_class = CustomExceptionReporter()
    ...
```

See also

You can also set up custom error reporting by writing a custom piece of
[exception middleware](https://docs.djangoproject.com/en/topics/http/middleware/#exception-middleware). If you do write custom
error handling, it’s a good idea to emulate Django’s built-in error handling
and only report/log errors if [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) is `False`.

---

# How to provide initial data for models¶

# How to provide initial data for models¶

It’s sometimes useful to prepopulate your database with hard-coded data when
you’re first setting up an app. You can provide initial data with migrations or
fixtures.

## Provide initial data with migrations¶

To automatically load initial data for an app, create a
[data migration](https://docs.djangoproject.com/en/topics/migrations/#data-migrations). Migrations are run when setting up the
test database, so the data will be available there, subject to [some
limitations](https://docs.djangoproject.com/en/topics/testing/overview/#test-case-serialized-rollback).

## Provide data with fixtures¶

You can also provide data using [fixtures](https://docs.djangoproject.com/en/topics/db/fixtures/#fixtures-explanation),
however, this data isn’t loaded automatically, except if you use
[TransactionTestCase.fixtures](https://docs.djangoproject.com/en/topics/testing/tools/#django.test.TransactionTestCase.fixtures).

A fixture is a collection of data that Django knows how to import into a
database. The most straightforward way of creating a fixture if you’ve already
got some data is to use the [manage.pydumpdata](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-dumpdata) command.
Or, you can write fixtures by hand; fixtures can be written as JSON, XML or YAML
(with [PyYAML](https://pyyaml.org/) installed) documents. The [serialization documentation](https://docs.djangoproject.com/en/topics/serialization/) has more details about each of these supported
[serialization formats](https://docs.djangoproject.com/en/topics/serialization/#serialization-formats).

As an example, though, here’s what a fixture for a `Person` model might look
like in JSON:

```
[
  {
    "model": "myapp.person",
    "pk": 1,
    "fields": {
      "first_name": "John",
      "last_name": "Lennon"
    }
  },
  {
    "model": "myapp.person",
    "pk": 2,
    "fields": {
      "first_name": "Paul",
      "last_name": "McCartney"
    }
  }
]
```

And here’s that same fixture as YAML:

```
- model: myapp.person
  pk: 1
  fields:
    first_name: John
    last_name: Lennon
- model: myapp.person
  pk: 2
  fields:
    first_name: Paul
    last_name: McCartney
```

You’ll store this data in a `fixtures` directory inside your app.

You can load data by calling [manage.pyloaddata](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-loaddata) `<fixturename>`, where `<fixturename>` is the name of the fixture file
you’ve created. Each time you run [loaddata](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-loaddata), the data will be read
from the fixture and reloaded into the database. Note this means that if you
change one of the rows created by a fixture and then run [loaddata](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-loaddata)
again, you’ll wipe out any changes you’ve made.

### Tell Django where to look for fixture files¶

By default, Django looks for fixtures in the `fixtures` directory inside each
app for, so the command `loaddata sample` will find the file
`my_app/fixtures/sample.json`. This works with relative paths as well, so
`loaddata my_app/sample` will find the file
`my_app/fixtures/my_app/sample.json`.

Django also looks for fixtures in the list of directories provided in the
[FIXTURE_DIRS](https://docs.djangoproject.com/en/ref/settings/#std-setting-FIXTURE_DIRS) setting.

To completely prevent default search form happening, use an absolute path to
specify the location of your fixture file, e.g. `loaddata /path/to/sample`.

Namespace your fixture files

Django will use the first fixture file it finds whose name matches, so if
you have fixture files with the same name in different applications, you
will be unable to distinguish between them in your `loaddata` commands.
The easiest way to avoid this problem is by *namespacing* your fixture
files. That is, by putting them inside a directory named for their
application, as in the relative path example above.

See also

Fixtures are also used by the [testing framework](https://docs.djangoproject.com/en/topics/testing/tools/#topics-testing-fixtures) to help set up a consistent test environment.

---

# How to integrate Django with a legacy database¶

# How to integrate Django with a legacy database¶

While Django is best suited for developing new applications, it’s quite
possible to integrate it into legacy databases. Django includes a couple of
utilities to automate as much of this process as possible.

This document assumes you know the Django basics, as covered in the
[tutorial](https://docs.djangoproject.com/en/intro/tutorial01/).

Once you’ve got Django set up, you’ll follow this general process to integrate
with an existing database.

## Give Django your database parameters¶

You’ll need to tell Django what your database connection parameters are, and
what the name of the database is. Do that by editing the [DATABASES](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASES)
setting and assigning values to the following keys for the `'default'`
connection:

- [NAME](https://docs.djangoproject.com/en/ref/settings/#std-setting-NAME)
- [ENGINE](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASE-ENGINE)
- [USER](https://docs.djangoproject.com/en/ref/settings/#std-setting-USER)
- [PASSWORD](https://docs.djangoproject.com/en/ref/settings/#std-setting-PASSWORD)
- [HOST](https://docs.djangoproject.com/en/ref/settings/#std-setting-HOST)
- [PORT](https://docs.djangoproject.com/en/ref/settings/#std-setting-PORT)

## Auto-generate the models¶

Django comes with a utility called [inspectdb](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-inspectdb) that can create models
by introspecting an existing database. You can view the output by running this
command:

```
$ python manage.py inspectdb
```

Save this as a file by using standard Unix output redirection:

```
$ python manage.py inspectdb > models.py
```

This feature is meant as a shortcut, not as definitive model generation. See the
[documentationofinspectdb](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-inspectdb) for more information.

Once you’ve cleaned up your models, name the file `models.py` and put it in
the Python package that holds your app. Then add the app to your
[INSTALLED_APPS](https://docs.djangoproject.com/en/ref/settings/#std-setting-INSTALLED_APPS) setting.

By default, [inspectdb](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-inspectdb) creates unmanaged models. That is,
`managed = False` in the model’s `Meta` class tells Django not to manage
each table’s creation, modification, and deletion:

```
class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=70)

    class Meta:
        managed = False
        db_table = "CENSUS_PERSONS"
```

If you do want to allow Django to manage the table’s lifecycle, you’ll need to
change the [managed](https://docs.djangoproject.com/en/ref/models/options/#django.db.models.Options.managed) option above to `True`
(or remove it because `True` is its default value).

## Install the core Django tables¶

Next, run the [migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate) command to install any extra needed database
records such as admin permissions and content types:

```
$ python manage.py migrate
```

## Test and tweak¶

Those are the basic steps – from here you’ll want to tweak the models Django
generated until they work the way you’d like. Try accessing your data via the
Django database API, and try editing objects via Django’s admin site, and edit
the models file accordingly.

---

# How to create CSV output¶

# How to create CSV output¶

This document explains how to output CSV (Comma Separated Values) dynamically
using Django views. To do this, you can either use the Python CSV library or the
Django template system.

## Using the Python CSV library¶

Python comes with a CSV library, [csv](https://docs.python.org/3/library/csv.html#module-csv). The key to using it with Django is
that the [csv](https://docs.python.org/3/library/csv.html#module-csv) module’s CSV-creation capability acts on file-like objects,
and Django’s [HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse) objects are file-like objects.

Here’s an example:

```
import csv
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["First row", "Foo", "Bar", "Baz"])
    writer.writerow(["Second row", "A", "B", "C", '"Testing"', "Here's a quote"])

    return response
```

The code and comments should be self-explanatory, but a few things deserve a
mention:

- The response gets a special MIME type, *text/csv*. This tells
  browsers that the document is a CSV file, rather than an HTML file. If
  you leave this off, browsers will probably interpret the output as HTML,
  which will result in ugly, scary gobbledygook in the browser window.
- The response gets an additional `Content-Disposition` header, which
  contains the name of the CSV file. This filename is arbitrary; call it
  whatever you want. It’ll be used by browsers in the “Save as…” dialog, etc.
- You can hook into the CSV-generation API by passing `response` as the first
  argument to `csv.writer`. The `csv.writer` function expects a file-like
  object, and [HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse) objects fit the bill.
- For each row in your CSV file, call `writer.writerow`, passing it an
  [iterable](https://docs.python.org/3/glossary.html#term-iterable).
- The CSV module takes care of quoting for you, so you don’t have to worry
  about escaping strings with quotes or commas in them. Pass `writerow()`
  your raw strings, and it’ll do the right thing.

### Streaming large CSV files¶

When dealing with views that generate very large responses, you might want to
consider using Django’s [StreamingHttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.StreamingHttpResponse) instead.
For example, by streaming a file that takes a long time to generate you can
avoid a load balancer dropping a connection that might have otherwise timed out
while the server was generating the response.

In this example, we make full use of Python generators to efficiently handle
the assembly and transmission of a large CSV file:

```
import csv

from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )
```

## Using the template system¶

Alternatively, you can use the [Django template system](https://docs.djangoproject.com/en/topics/templates/)
to generate CSV. This is lower-level than using the convenient Python [csv](https://docs.python.org/3/library/csv.html#module-csv)
module, but the solution is presented here for completeness.

The idea here is to pass a list of items to your template, and have the
template output the commas in a [for](https://docs.djangoproject.com/en/ref/templates/builtins/#std-templatetag-for) loop.

Here’s an example, which generates the same CSV file as above:

```
from django.http import HttpResponse
from django.template import loader

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ("First row", "Foo", "Bar", "Baz"),
        ("Second row", "A", "B", "C", '"Testing"', "Here's a quote"),
    )

    t = loader.get_template("my_template_name.txt")
    c = {"data": csv_data}
    response.write(t.render(c))
    return response
```

The only difference between this example and the previous example is that this
one uses template loading instead of the CSV module. The rest of the code –
such as the `content_type='text/csv'` – is the same.

Then, create the template `my_template_name.txt`, with this template code:

```
{% for row in data %}"{{ row.0|addslashes }}", "{{ row.1|addslashes }}", "{{ row.2|addslashes }}", "{{ row.3|addslashes }}", "{{ row.4|addslashes }}"
{% endfor %}
```

This short template iterates over the given data and displays a line of CSV for
each row. It uses the [addslashes](https://docs.djangoproject.com/en/ref/templates/builtins/#std-templatefilter-addslashes) template filter to ensure there
aren’t any problems with quotes.

## Other text-based formats¶

Notice that there isn’t very much specific to CSV here – just the specific
output format. You can use either of these techniques to output any text-based
format you can dream of. You can also use a similar technique to generate
arbitrary binary data; see [How to create PDF files](https://docs.djangoproject.com/en/5.0/outputting-pdf/) for an example.
