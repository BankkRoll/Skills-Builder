# Advanced tutorial: How to write reusable apps¶ and more

# Advanced tutorial: How to write reusable apps¶

# Advanced tutorial: How to write reusable apps¶

This advanced tutorial begins where [Tutorial 8](https://docs.djangoproject.com/en/5.0/tutorial08/)
left off. We’ll be turning our web-poll into a standalone Python package
you can reuse in new projects and share with other people.

If you haven’t recently completed Tutorials 1–7, we encourage you to review
these so that your example project matches the one described below.

## Reusability matters¶

It’s a lot of work to design, build, test and maintain a web application. Many
Python and Django projects share common problems. Wouldn’t it be great if we
could save some of this repeated work?

Reusability is the way of life in Python. [The Python Package Index (PyPI)](https://pypi.org/) has a vast range of packages you can use in your own
Python programs. Check out [Django Packages](https://djangopackages.org) for
existing reusable apps you could incorporate in your project. Django itself is
also a normal Python package. This means that you can take existing Python
packages or Django apps and compose them into your own web project. You only
need to write the parts that make your project unique.

Let’s say you were starting a new project that needed a polls app like the one
we’ve been working on. How do you make this app reusable? Luckily, you’re well
on the way already. In [Tutorial 1](https://docs.djangoproject.com/en/5.0/tutorial01/), we saw how we
could decouple polls from the project-level URLconf using an `include`.
In this tutorial, we’ll take further steps to make the app easy to use in new
projects and ready to publish for others to install and use.

Package? App?

A Python [package](https://docs.python.org/3/glossary.html#term-package) provides a way of grouping related Python code for
easy reuse. A package contains one or more files of Python code (also known
as “modules”).

A package can be imported with `import foo.bar` or `from foo import
bar`. For a directory (like `polls`) to form a package, it must contain
a special file `__init__.py`, even if this file is empty.

A Django *application* is a Python package that is specifically intended
for use in a Django project. An application may use common Django
conventions, such as having `models`, `tests`, `urls`, and `views`
submodules.

Later on we use the term *packaging* to describe the process of making a
Python package easy for others to install. It can be a little confusing, we
know.

## Your project and your reusable app¶

After the previous tutorials, our project should look like this:

```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    polls/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
            0001_initial.py
        models.py
        static/
            polls/
                images/
                    background.png
                style.css
        templates/
            polls/
                detail.html
                index.html
                results.html
        tests.py
        urls.py
        views.py
    templates/
        admin/
            base_site.html
```

You created `mysite/templates` in [Tutorial 7](https://docs.djangoproject.com/en/5.0/tutorial07/),
and `polls/templates` in [Tutorial 3](https://docs.djangoproject.com/en/5.0/tutorial03/). Now perhaps
it is clearer why we chose to have separate template directories for the
project and application: everything that is part of the polls application is in
`polls`. It makes the application self-contained and easier to drop into a
new project.

The `polls` directory could now be copied into a new Django project and
immediately reused. It’s not quite ready to be published though. For that, we
need to package the app to make it easy for others to install.

## Installing some prerequisites¶

The current state of Python packaging is a bit muddled with various tools. For
this tutorial, we’re going to use [setuptools](https://pypi.org/project/setuptools/) to build our package. It’s
the recommended packaging tool (merged with the `distribute` fork). We’ll
also be using [pip](https://pypi.org/project/pip/) to install and uninstall it. You should install these
two packages now. If you need help, you can refer to [how to install
Django with pip](https://docs.djangoproject.com/en/topics/install/#installing-official-release). You can install `setuptools`
the same way.

## Packaging your app¶

Python *packaging* refers to preparing your app in a specific format that can
be easily installed and used. Django itself is packaged very much like
this. For a small app like polls, this process isn’t too difficult.

1. First, create a parent directory for the package, outside of your Django
  project. Call this directory `django-polls`.
  Choosing a name for your app
  When choosing a name for your package, check PyPI to avoid naming
  conflicts with existing packages. We recommend using a `django-`
  prefix for package names, to identify your package as specific to
  Django, and a corresponding `django_` prefix for your module name. For
  example, the `django-ratelimit` package contains the
  `django_ratelimit` module.
  Application labels (that is, the final part of the dotted path to
  application packages) *must* be unique in [INSTALLED_APPS](https://docs.djangoproject.com/en/ref/settings/#std-setting-INSTALLED_APPS).
  Avoid using the same label as any of the Django [contrib packages](https://docs.djangoproject.com/en/ref/contrib/), for example `auth`, `admin`, or
  `messages`.
2. Move the `polls` directory into `django-polls` directory, and rename it
  to `django_polls`.
3. Edit `django_polls/apps.py` so that [name](https://docs.djangoproject.com/en/ref/applications/#django.apps.AppConfig.name) refers to the
  new module name and add [label](https://docs.djangoproject.com/en/ref/applications/#django.apps.AppConfig.label) to give a short name for
  the app:
    `django-polls/django_polls/apps.py`[¶](#id1)
  ```
  from django.apps import AppConfig
  class PollsConfig(AppConfig):
      default_auto_field = "django.db.models.BigAutoField"
      name = "django_polls"
      label = "polls"
  ```
4. Create a file `django-polls/README.rst` with the following contents:
    `django-polls/README.rst`[¶](#id2)
  ```
  ============
  django-polls
  ============
  django-polls is a Django app to conduct web-based polls. For each
  question, visitors can choose between a fixed number of answers.
  Detailed documentation is in the "docs" directory.
  Quick start
  -----------
  1. Add "polls" to your INSTALLED_APPS setting like this::
      INSTALLED_APPS = [
          ...,
          "django_polls",
      ]
  2. Include the polls URLconf in your project urls.py like this::
      path("polls/", include("django_polls.urls")),
  3. Run ``python manage.py migrate`` to create the models.
  4. Start the development server and visit the admin to create a poll.
  5. Visit the ``/polls/`` URL to participate in the poll.
  ```
5. Create a `django-polls/LICENSE` file. Choosing a license is beyond the
  scope of this tutorial, but suffice it to say that code released publicly
  without a license is *useless*. Django and many Django-compatible apps are
  distributed under the BSD license; however, you’re free to pick your own
  license. Just be aware that your licensing choice will affect who is able
  to use your code.
6. Next we’ll create `pyproject.toml`, `setup.cfg`, and `setup.py` files
  which detail how to build and install the app. A full explanation of these
  files is beyond the scope of this tutorial, but the [setuptools
  documentation](https://setuptools.pypa.io/en/latest/) has a good
  explanation. Create the `django-polls/pyproject.toml`,
  `django-polls/setup.cfg`, and `django-polls/setup.py` files with the
  following contents:
    `django-polls/pyproject.toml`[¶](#id3)
  ```
  [build-system]
  requires = ['setuptools>=40.8.0']
  build-backend = 'setuptools.build_meta'
  ```
      `django-polls/setup.cfg`[¶](#id4)
  ```
  [metadata]
  name = django-polls
  version = 0.1
  description = A Django app to conduct web-based polls.
  long_description = file: README.rst
  url = https://www.example.com/
  author = Your Name
  author_email = yourname@example.com
  license = BSD-3-Clause  # Example license
  classifiers =
      Environment :: Web Environment
      Framework :: Django
      Framework :: Django :: X.Y  # Replace "X.Y" as appropriate
      Intended Audience :: Developers
      License :: OSI Approved :: BSD License
      Operating System :: OS Independent
      Programming Language :: Python
      Programming Language :: Python :: 3
      Programming Language :: Python :: 3 :: Only
      Programming Language :: Python :: 3.10
      Programming Language :: Python :: 3.11
      Programming Language :: Python :: 3.12
      Topic :: Internet :: WWW/HTTP
      Topic :: Internet :: WWW/HTTP :: Dynamic Content
  [options]
  include_package_data = true
  packages = find:
  python_requires = >=3.10
  install_requires =
      Django >= X.Y  # Replace "X.Y" as appropriate
  ```
      `django-polls/setup.py`[¶](#id5)
  ```
  from setuptools import setup
  setup()
  ```
7. Only Python modules and packages are included in the package by default. To
  include additional files, we’ll need to create a `MANIFEST.in` file. The
  `setuptools` docs referred to in the previous step discuss this file in
  more detail. To include the templates, the `README.rst` and our
  `LICENSE` file, create a file `django-polls/MANIFEST.in` with the
  following contents:
    `django-polls/MANIFEST.in`[¶](#id6)
  ```
  include LICENSE
  include README.rst
  recursive-include django_polls/static *
  recursive-include django_polls/templates *
  ```
8. It’s optional, but recommended, to include detailed documentation with your
  app. Create an empty directory `django-polls/docs` for future
  documentation. Add an additional line to `django-polls/MANIFEST.in`:
  ```
  recursive-include docs *
  ```
  Note that the `docs` directory won’t be included in your package unless
  you add some files to it. Many Django apps also provide their documentation
  online through sites like [readthedocs.org](https://readthedocs.org).
9. Try building your package by running `python setup.py sdist` inside
  `django-polls`. This creates a directory called `dist` and builds your
  new package, `django-polls-0.1.tar.gz`.

For more information on packaging, see Python’s [Tutorial on Packaging and
Distributing Projects](https://packaging.python.org/tutorials/packaging-projects/).

## Using your own package¶

Since we moved the `polls` directory out of the project, it’s no longer
working. We’ll now fix this by installing our new `django-polls` package.

Installing as a user library

The following steps install `django-polls` as a user library. Per-user
installs have a lot of advantages over installing the package system-wide,
such as being usable on systems where you don’t have administrator access
as well as preventing the package from affecting system services and other
users of the machine.

Note that per-user installations can still affect the behavior of system
tools that run as that user, so using a virtual environment is a more robust
solution (see below).

1. To install the package, use pip (you already [installed it](#installing-reusable-apps-prerequisites), right?):
  ```
  python -m pip install --user django-polls/dist/django-polls-0.1.tar.gz
  ```
2. Update `mysite/settings.py` to point to the new module name:
  ```
  INSTALLED_APPS = [
      "django_polls.apps.PollsConfig",
      ...,
  ]
  ```
3. Update `mysite/urls.py` to point to the new module name:
  ```
  urlpatterns = [
      path("polls/", include("django_polls.urls")),
      ...,
  ]
  ```
4. Run the development server to confirm the project continues to work.

## Publishing your app¶

Now that we’ve packaged and tested `django-polls`, it’s ready to share with
the world! If this wasn’t just an example, you could now:

- Email the package to a friend.
- Upload the package on your website.
- Post the package on a public repository, such as [the Python Package Index
  (PyPI)](https://pypi.org/). [packaging.python.org](https://packaging.python.org) has [a good
  tutorial](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives)
  for doing this.

## Installing Python packages with a virtual environment¶

Earlier, we installed `django-polls` as a user library. This has some
disadvantages:

- Modifying the user libraries can affect other Python software on your system.
- You won’t be able to run multiple versions of this package (or others with
  the same name).

Typically, these situations only arise once you’re maintaining several Django
projects. When they do, the best solution is to use [venv](https://docs.python.org/3/tutorial/venv.html). This tool allows you to maintain multiple isolated
Python environments, each with its own copy of the libraries and package
namespace.

---

# Writing your first Django app, part 1¶

# Writing your first Django app, part 1¶

Let’s learn by example.

Throughout this tutorial, we’ll walk you through the creation of a basic
poll application.

It’ll consist of two parts:

- A public site that lets people view polls and vote in them.
- An admin site that lets you add, change, and delete polls.

We’ll assume you have [Django installed](https://docs.djangoproject.com/en/5.0/install/) already. You can
tell Django is installed and which version by running the following command
in a shell prompt (indicated by the $ prefix):

   /  

```
$ python -m django --version
```

```
...\> py -m django --version
```

If Django is installed, you should see the version of your installation. If it
isn’t, you’ll get an error telling “No module named django”.

This tutorial is written for Django 5.0, which supports Python 3.10 and
later. If the Django version doesn’t match, you can refer to the tutorial for
your version of Django by using the version switcher at the bottom right corner
of this page, or update Django to the newest version. If you’re using an older
version of Python, check [What Python version can I use with Django?](https://docs.djangoproject.com/en/faq/install/#faq-python-version-support) to find a compatible
version of Django.

See [How to install Django](https://docs.djangoproject.com/en/topics/install/) for advice on how to remove
older versions of Django and install a newer one.

Where to get help:

If you’re having trouble going through this tutorial, please head over to
the [Getting Help](https://docs.djangoproject.com/en/faq/help/) section of the FAQ.

## Creating a project¶

If this is your first time using Django, you’ll have to take care of some
initial setup. Namely, you’ll need to auto-generate some code that establishes a
Django [project](https://docs.djangoproject.com/en/glossary/#term-project) – a collection of settings for an instance of Django,
including database configuration, Django-specific options and
application-specific settings.

From the command line, `cd` into a directory where you’d like to store your
code, then run the following command:

   /  

```
$ django-admin startproject mysite
```

```
...\> django-admin startproject mysite
```

This will create a `mysite` directory in your current directory. If it didn’t
work, see [Problems running django-admin](https://docs.djangoproject.com/en/faq/troubleshooting/#troubleshooting-django-admin).

Note

You’ll need to avoid naming projects after built-in Python or Django
components. In particular, this means you should avoid using names like
`django` (which will conflict with Django itself) or `test` (which
conflicts with a built-in Python package).

Let’s look at what [startproject](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-startproject) created:

```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

These files are:

- The outer `mysite/` root directory is a container for your project. Its
  name doesn’t matter to Django; you can rename it to anything you like.
- `manage.py`: A command-line utility that lets you interact with this
  Django project in various ways. You can read all the details about
  `manage.py` in [django-admin and manage.py](https://docs.djangoproject.com/en/ref/django-admin/).
- The inner `mysite/` directory is the actual Python package for your
  project. Its name is the Python package name you’ll need to use to import
  anything inside it (e.g. `mysite.urls`).
- `mysite/__init__.py`: An empty file that tells Python that this
  directory should be considered a Python package. If you’re a Python beginner,
  read [more about packages](https://docs.python.org/3/tutorial/modules.html#tut-packages) in the official Python docs.
- `mysite/settings.py`: Settings/configuration for this Django
  project.  [Django settings](https://docs.djangoproject.com/en/topics/settings/) will tell you all about how settings
  work.
- `mysite/urls.py`: The URL declarations for this Django project; a
  “table of contents” of your Django-powered site. You can read more about
  URLs in [URL dispatcher](https://docs.djangoproject.com/en/topics/http/urls/).
- `mysite/asgi.py`: An entry-point for ASGI-compatible web servers to
  serve your project. See [How to deploy with ASGI](https://docs.djangoproject.com/en/howto/deployment/asgi/) for more details.
- `mysite/wsgi.py`: An entry-point for WSGI-compatible web servers to
  serve your project. See [How to deploy with WSGI](https://docs.djangoproject.com/en/howto/deployment/wsgi/) for more details.

## The development server¶

Let’s verify your Django project works. Change into the outer `mysite` directory, if
you haven’t already, and run the following commands:

   /  

```
$ python manage.py runserver
```

```
...\> py manage.py runserver
```

You’ll see the following output on the command line:

```
Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

April 02, 2025 - 15:50:53
Django version 5.0, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Note

Ignore the warning about unapplied database migrations for now; we’ll deal
with the database shortly.

Now that the server’s running, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) with your web
browser. You’ll see a “Congratulations!” page, with a rocket taking off.
It worked!

You’ve started the Django development server, a lightweight web server written
purely in Python. We’ve included this with Django so you can develop things
rapidly, without having to deal with configuring a production server – such as
Apache – until you’re ready for production.

Now’s a good time to note: **don’t** use this server in anything resembling a
production environment. It’s intended only for use while developing. (We’re in
the business of making web frameworks, not web servers.)

(To serve the site on a different port, see the [runserver](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-runserver) reference.)

Automatic reloading of [runserver](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-runserver)

The development server automatically reloads Python code for each request
as needed. You don’t need to restart the server for code changes to take
effect. However, some actions like adding files don’t trigger a restart,
so you’ll have to restart the server in these cases.

## Creating the Polls app¶

Now that your environment – a “project” – is set up, you’re set to start
doing work.

Each application you write in Django consists of a Python package that follows
a certain convention. Django comes with a utility that automatically generates
the basic directory structure of an app, so you can focus on writing code
rather than creating directories.

Projects vs. apps

What’s the difference between a project and an app? An app is a web
application that does something – e.g., a blog system, a database of
public records or a small poll app. A project is a collection of
configuration and apps for a particular website. A project can contain
multiple apps. An app can be in multiple projects.

Your apps can live anywhere on your [Python path](https://docs.python.org/3/tutorial/modules.html#tut-searchpath). In
this tutorial, we’ll create our poll app in the same directory as your
`manage.py` file so that it can be imported as its own top-level module,
rather than a submodule of `mysite`.

To create your app, make sure you’re in the same directory as `manage.py`
and type this command:

   /  

```
$ python manage.py startapp polls
```

```
...\> py manage.py startapp polls
```

That’ll create a directory `polls`, which is laid out like this:

```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

This directory structure will house the poll application.

## Write your first view¶

Let’s write the first view. Open the file `polls/views.py`
and put the following Python code in it:

  `polls/views.py`[¶](#id1)

```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

This is the most basic view possible in Django. To access it in a browser, we
need to map it to a URL - and for this we need to define a URL configuration,
or “URLconf” for short. These URL configurations are defined inside each
Django app, and they are Python files named `urls.py`.

To define a URLconf for the `polls` app, create a file `polls/urls.py`
with the following content:

  `polls/urls.py`[¶](#id2)

```
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

Your app directory should now look like:

```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py
```

The next step is to configure the global URLconf in the `mysite` project to
include the URLconf defined in `polls.urls`. To do this, add an import for
`django.urls.include` in `mysite/urls.py` and insert an
[include()](https://docs.djangoproject.com/en/ref/urls/#django.urls.include) in the `urlpatterns` list, so you have:

  `mysite/urls.py`[¶](#id3)

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

The [include()](https://docs.djangoproject.com/en/ref/urls/#django.urls.include) function allows referencing other URLconfs.
Whenever Django encounters [include()](https://docs.djangoproject.com/en/ref/urls/#django.urls.include), it chops off whatever
part of the URL matched up to that point and sends the remaining string to the
included URLconf for further processing.

The idea behind [include()](https://docs.djangoproject.com/en/ref/urls/#django.urls.include) is to make it easy to
plug-and-play URLs. Since polls are in their own URLconf
(`polls/urls.py`), they can be placed under “/polls/”, or under
“/fun_polls/”, or under “/content/polls/”, or any other path root, and the
app will still work.

When to use [include()](https://docs.djangoproject.com/en/ref/urls/#django.urls.include)

You should always use `include()` when you include other URL patterns.
`admin.site.urls` is the only exception to this.

You have now wired an `index` view into the URLconf. Verify it’s working with
the following command:

   /  

```
$ python manage.py runserver
```

```
...\> py manage.py runserver
```

Go to [http://localhost:8000/polls/](http://localhost:8000/polls/) in your browser, and you should see the
text “*Hello, world. You’re at the polls index.*”, which you defined in the
`index` view.

Page not found?

If you get an error page here, check that you’re going to
[http://localhost:8000/polls/](http://localhost:8000/polls/) and not [http://localhost:8000/](http://localhost:8000/).

The [path()](https://docs.djangoproject.com/en/ref/urls/#django.urls.path) function is passed four arguments, two required:
`route` and `view`, and two optional: `kwargs`, and `name`.
At this point, it’s worth reviewing what these arguments are for.

### path()argument:route¶

`route` is a string that contains a URL pattern. When processing a request,
Django starts at the first pattern in `urlpatterns` and makes its way down
the list, comparing the requested URL against each pattern until it finds one
that matches.

Patterns don’t search GET and POST parameters, or the domain name. For example,
in a request to `https://www.example.com/myapp/`, the URLconf will look for
`myapp/`. In a request to `https://www.example.com/myapp/?page=3`, the
URLconf will also look for `myapp/`.

### path()argument:view¶

When Django finds a matching pattern, it calls the specified view function with
an [HttpRequest](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest) object as the first argument and any
“captured” values from the route as keyword arguments. We’ll give an example
of this in a bit.

### path()argument:kwargs¶

Arbitrary keyword arguments can be passed in a dictionary to the target view. We
aren’t going to use this feature of Django in the tutorial.

### path()argument:name¶

Naming your URL lets you refer to it unambiguously from elsewhere in Django,
especially from within templates. This powerful feature allows you to make
global changes to the URL patterns of your project while only touching a single
file.

When you’re comfortable with the basic request and response flow, read
[part 2 of this tutorial](https://docs.djangoproject.com/en/5.0/tutorial02/) to start working with the
database.
