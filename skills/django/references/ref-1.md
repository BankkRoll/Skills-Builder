---

# Applications¶

# Applications¶

Django contains a registry of installed applications that stores configuration
and provides introspection. It also maintains a list of available [models](https://docs.djangoproject.com/en/topics/db/models/).

This registry is called [apps](#django.apps.apps) and it’s available in
[django.apps](#module-django.apps):

```
>>> from django.apps import apps
>>> apps.get_app_config("admin").verbose_name
'Administration'
```

## Projects and applications¶

The term **project** describes a Django web application. The project Python
package is defined primarily by a settings module, but it usually contains
other things. For example, when you run  `django-admin startproject mysite`
you’ll get a `mysite` project directory that contains a `mysite` Python
package with `settings.py`, `urls.py`, `asgi.py` and `wsgi.py`. The
project package is often extended to include things like fixtures, CSS, and
templates which aren’t tied to a particular application.

A **project’s root directory** (the one that contains `manage.py`) is usually
the container for all of a project’s applications which aren’t installed
separately.

The term **application** describes a Python package that provides some set of
features. Applications [may be reused](https://docs.djangoproject.com/en/intro/reusable-apps/) in various
projects.

Applications include some combination of models, views, templates, template
tags, static files, URLs, middleware, etc. They’re generally wired into
projects with the [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting and optionally with other
mechanisms such as URLconfs, the [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE) setting, or template
inheritance.

It is important to understand that a Django application is a set of code
that interacts with various parts of the framework. There’s no such thing as
an `Application` object. However, there’s a few places where Django needs to
interact with installed applications, mainly for configuration and also for
introspection. That’s why the application registry maintains metadata in an
[AppConfig](#django.apps.AppConfig) instance for each installed application.

There’s no restriction that a project package can’t also be considered an
application and have models, etc. (which would require adding it to
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS)).

## Configuring applications¶

To configure an application, create an `apps.py` module inside the
application, then define a subclass of [AppConfig](#django.apps.AppConfig) there.

When [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) contains the dotted path to an application
module, by default, if Django finds exactly one [AppConfig](#django.apps.AppConfig) subclass in
the `apps.py` submodule, it uses that configuration for the application. This
behavior may be disabled by setting [AppConfig.default](#django.apps.AppConfig.default) to `False`.

If the `apps.py` module contains more than one [AppConfig](#django.apps.AppConfig) subclass,
Django will look for a single one where [AppConfig.default](#django.apps.AppConfig.default) is `True`.

If no [AppConfig](#django.apps.AppConfig) subclass is found, the base [AppConfig](#django.apps.AppConfig) class
will be used.

Alternatively, [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) may contain the dotted path to a
configuration class to specify it explicitly:

```
INSTALLED_APPS = [
    ...,
    "polls.apps.PollsAppConfig",
    ...,
]
```

### For application authors¶

If you’re creating a pluggable app called “Rock ’n’ roll”, here’s how you
would provide a proper name for the admin:

```
# rock_n_roll/apps.py

from django.apps import AppConfig

class RockNRollConfig(AppConfig):
    name = "rock_n_roll"
    verbose_name = "Rock ’n’ roll"
```

`RockNRollConfig` will be loaded automatically when [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS)
contains `'rock_n_roll'`. If you need to prevent this, set
[default](#django.apps.AppConfig.default) to `False` in the class definition.

You can provide several [AppConfig](#django.apps.AppConfig) subclasses with different behaviors.
To tell Django which one to use by default, set [default](#django.apps.AppConfig.default) to
`True` in its definition. If your users want to pick a non-default
configuration, they must replace `'rock_n_roll'` with the dotted path to that
specific class in their [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting.

The [AppConfig.name](#django.apps.AppConfig.name) attribute tells Django which application this
configuration applies to. You can define any other attribute documented in the
[AppConfig](#django.apps.AppConfig) API reference.

[AppConfig](#django.apps.AppConfig) subclasses may be defined anywhere. The `apps.py`
convention merely allows Django to load them automatically when
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) contains the path to an application module rather
than the path to a configuration class.

Note

If your code imports the application registry in an application’s
`__init__.py`, the name `apps` will clash with the `apps` submodule.
The best practice is to move that code to a submodule and import it. A
workaround is to import the registry under a different name:

```
from django.apps import apps as django_apps
```

### For application users¶

If you’re using “Rock ’n’ roll” in a project called `anthology`, but you
want it to show up as “Jazz Manouche” instead, you can provide your own
configuration:

```
# anthology/apps.py

from rock_n_roll.apps import RockNRollConfig

class JazzManoucheConfig(RockNRollConfig):
    verbose_name = "Jazz Manouche"

# anthology/settings.py

INSTALLED_APPS = [
    "anthology.apps.JazzManoucheConfig",
    # ...
]
```

This example shows project-specific configuration classes located in a
submodule called `apps.py`. This is a convention, not a requirement.
[AppConfig](#django.apps.AppConfig) subclasses may be defined anywhere.

In this situation, [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) must contain the dotted path to
the configuration class because it lives outside of an application and thus
cannot be automatically detected.

## Application configuration¶

   *class*AppConfig[[source]](https://docs.djangoproject.com/en/_modules/django/apps/config/#AppConfig)[¶](#django.apps.AppConfig)

Application configuration objects store metadata for an application. Some
attributes can be configured in [AppConfig](#django.apps.AppConfig)
subclasses. Others are set by Django and read-only.

### Configurable attributes¶

   AppConfig.name[¶](#django.apps.AppConfig.name)

Full Python path to the application, e.g. `'django.contrib.admin'`.

This attribute defines which application the configuration applies to. It
must be set in all [AppConfig](#django.apps.AppConfig) subclasses.

It must be unique across a Django project.

    AppConfig.label[¶](#django.apps.AppConfig.label)

Short name for the application, e.g. `'admin'`

This attribute allows relabeling an application when two applications
have conflicting labels. It defaults to the last component of `name`.
It should be a valid Python identifier.

It must be unique across a Django project.

Warning

Changing this attribute after migrations have been applied for an
application will result in breaking changes to a project or, in the
case of a reusable app, any existing installs of that app. This is
because `AppConfig.label` is used in database tables and migration
files when referencing an app in the dependencies list.

     AppConfig.verbose_name[¶](#django.apps.AppConfig.verbose_name)

Human-readable name for the application, e.g. “Administration”.

This attribute defaults to `label.title()`.

    AppConfig.path[¶](#django.apps.AppConfig.path)

Filesystem path to the application directory, e.g.
`'/usr/lib/pythonX.Y/dist-packages/django/contrib/admin'`.

In most cases, Django can automatically detect and set this, but you can
also provide an explicit override as a class attribute on your
[AppConfig](#django.apps.AppConfig) subclass. In a few situations this is
required; for instance if the app package is a [namespace package](#namespace-package) with
multiple paths.

    AppConfig.default[¶](#django.apps.AppConfig.default)

Set this attribute to `False` to prevent Django from selecting a
configuration class automatically. This is useful when `apps.py` defines
only one [AppConfig](#django.apps.AppConfig) subclass but you don’t want Django to use it by
default.

Set this attribute to `True` to tell Django to select a configuration
class automatically. This is useful when `apps.py` defines more than one
[AppConfig](#django.apps.AppConfig) subclass and you want Django to use one of them by
default.

By default, this attribute isn’t set.

    AppConfig.default_auto_field[¶](#django.apps.AppConfig.default_auto_field)

The implicit primary key type to add to models within this app. You can
use this to keep [AutoField](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.AutoField) as the primary key
type for third party applications.

By default, this is the value of [DEFAULT_AUTO_FIELD](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_AUTO_FIELD).

### Read-only attributes¶

   AppConfig.module[¶](#django.apps.AppConfig.module)

Root module for the application, e.g. `<module 'django.contrib.admin' from
'django/contrib/admin/__init__.py'>`.

    AppConfig.models_module[¶](#django.apps.AppConfig.models_module)

Module containing the models, e.g. `<module 'django.contrib.admin.models'
from 'django/contrib/admin/models.py'>`.

It may be `None` if the application doesn’t contain a `models` module.
Note that the database related signals such as
[pre_migrate](https://docs.djangoproject.com/en/5.0/signals/#django.db.models.signals.pre_migrate) and
[post_migrate](https://docs.djangoproject.com/en/5.0/signals/#django.db.models.signals.post_migrate)
are only emitted for applications that have a `models` module.

### Methods¶

   AppConfig.get_models(*include_auto_created=False*, *include_swapped=False*)[[source]](https://docs.djangoproject.com/en/_modules/django/apps/config/#AppConfig.get_models)[¶](#django.apps.AppConfig.get_models)

Returns an iterable of [Model](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model) classes for this
application.

Requires the app registry to be fully populated.

    AppConfig.get_model(*model_name*, *require_ready=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/apps/config/#AppConfig.get_model)[¶](#django.apps.AppConfig.get_model)

Returns the [Model](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model) with the given
`model_name`. `model_name` is case-insensitive.

Raises [LookupError](https://docs.python.org/3/library/exceptions.html#LookupError) if no such model exists in this application.

Requires the app registry to be fully populated unless the
`require_ready` argument is set to `False`. `require_ready` behaves
exactly as in [apps.get_model()](#django.apps.apps.get_model).

    AppConfig.ready()[[source]](https://docs.djangoproject.com/en/_modules/django/apps/config/#AppConfig.ready)[¶](#django.apps.AppConfig.ready)

Subclasses can override this method to perform initialization tasks such
as registering signals. It is called as soon as the registry is fully
populated.

Although you can’t import models at the module-level where
[AppConfig](#django.apps.AppConfig) classes are defined, you can import them in
`ready()`, using either an `import` statement or
[get_model()](#django.apps.AppConfig.get_model).

If you’re registering [modelsignals](https://docs.djangoproject.com/en/5.0/signals/#module-django.db.models.signals), you
can refer to the sender by its string label instead of using the model
class itself.

Example:

```
from django.apps import AppConfig
from django.db.models.signals import pre_save

class RockNRollConfig(AppConfig):
    # ...

    def ready(self):
        # importing model classes
        from .models import MyModel  # or...

        MyModel = self.get_model("MyModel")

        # registering signals with the model's string label
        pre_save.connect(receiver, sender="app_label.MyModel")
```

Warning

Although you can access model classes as described above, avoid
interacting with the database in your [ready()](#django.apps.AppConfig.ready) implementation.
This includes model methods that execute queries
([save()](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model.save),
[delete()](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model.delete), manager methods etc.), and
also raw SQL queries via `django.db.connection`. Your
[ready()](#django.apps.AppConfig.ready) method will run during startup of every management
command. For example, even though the test database configuration is
separate from the production settings, `manage.py test` would still
execute some queries against your **production** database!

Note

In the usual initialization process, the `ready` method is only called
once by Django. But in some corner cases, particularly in tests which
are fiddling with installed applications, `ready` might be called more
than once. In that case, either write idempotent methods, or put a flag
on your `AppConfig` classes to prevent rerunning code which should
be executed exactly one time.

### Namespace packages as apps¶

Python packages without an `__init__.py` file are known as “namespace
packages” and may be spread across multiple directories at different locations
on `sys.path` (see [PEP 420](https://peps.python.org/pep-0420/)).

Django applications require a single base filesystem path where Django
(depending on configuration) will search for templates, static assets,
etc. Thus, namespace packages may only be Django applications if one of the
following is true:

1. The namespace package actually has only a single location (i.e. is not
  spread across more than one directory.)
2. The [AppConfig](#django.apps.AppConfig) class used to configure the application
  has a [path](#django.apps.AppConfig.path) class attribute, which is the
  absolute directory path Django will use as the single base path for the
  application.

If neither of these conditions is met, Django will raise
[ImproperlyConfigured](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ImproperlyConfigured).

## Application registry¶

   apps[¶](#django.apps.apps)

The application registry provides the following public API. Methods that
aren’t listed below are considered private and may change without notice.

    apps.ready[¶](#django.apps.apps.ready)

Boolean attribute that is set to `True` after the registry is fully
populated and all [AppConfig.ready()](#django.apps.AppConfig.ready) methods are called.

    apps.get_app_configs()[¶](#django.apps.apps.get_app_configs)

Returns an iterable of [AppConfig](#django.apps.AppConfig) instances.

    apps.get_app_config(*app_label*)[¶](#django.apps.apps.get_app_config)

Returns an [AppConfig](#django.apps.AppConfig) for the application with the
given `app_label`. Raises [LookupError](https://docs.python.org/3/library/exceptions.html#LookupError) if no such application
exists.

    apps.is_installed(*app_name*)[¶](#django.apps.apps.is_installed)

Checks whether an application with the given name exists in the registry.
`app_name` is the full name of the app, e.g. `'django.contrib.admin'`.

    apps.get_model(*app_label*, *model_name*, *require_ready=True*)[¶](#django.apps.apps.get_model)

Returns the [Model](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model) with the given `app_label`
and `model_name`. As a shortcut, this method also accepts a single
argument in the form `app_label.model_name`. `model_name` is
case-insensitive.

Raises [LookupError](https://docs.python.org/3/library/exceptions.html#LookupError) if no such application or model exists. Raises
[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError) when called with a single argument that doesn’t contain
exactly one dot.

Requires the app registry to be fully populated unless the
`require_ready` argument is set to `False`.

Setting `require_ready` to `False` allows looking up models
[while the app registry is being populated](#app-loading-process),
specifically during the second phase where it imports models. Then
`get_model()` has the same effect as importing the model. The main use
case is to configure model classes with settings, such as
[AUTH_USER_MODEL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-AUTH_USER_MODEL).

When `require_ready` is `False`, `get_model()` returns a model class
that may not be fully functional (reverse accessors may be missing, for
example) until the app registry is fully populated. For this reason, it’s
best to leave `require_ready` to the default value of `True` whenever
possible.

## Initialization process¶

### How applications are loaded¶

When Django starts, [django.setup()](#django.setup) is responsible for populating the
application registry.

   setup(*set_prefix=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/#setup)[¶](#django.setup)

Configures Django by:

- Loading the settings.
- Setting up logging.
- If `set_prefix` is True, setting the URL resolver script prefix to
  [FORCE_SCRIPT_NAME](https://docs.djangoproject.com/en/5.0/settings/#std-setting-FORCE_SCRIPT_NAME) if defined, or `/` otherwise.
- Initializing the application registry.

This function is called automatically:

- When running an HTTP server via Django’s ASGI or WSGI support.
- When invoking a management command.

It must be called explicitly in other cases, for instance in plain Python
scripts.

  Changed in Django 5.0:

Raises a `RuntimeWarning` when apps interact with the database before
the app registry has been fully populated.

The application registry is initialized in three stages. At each stage, Django
processes all applications in the order of [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS).

1. First Django imports each item in [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS).
  If it’s an application configuration class, Django imports the root package
  of the application, defined by its [name](#django.apps.AppConfig.name) attribute. If
  it’s a Python package, Django looks for an application configuration in an
  `apps.py` submodule, or else creates a default application configuration.
  *At this stage, your code shouldn’t import any models!*
  In other words, your applications’ root packages and the modules that
  define your application configuration classes shouldn’t import any models,
  even indirectly.
  Strictly speaking, Django allows importing models once their application
  configuration is loaded. However, in order to avoid needless constraints on
  the order of [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS), it’s strongly recommended not
  import any models at this stage.
  Once this stage completes, APIs that operate on application configurations
  such as [get_app_config()](#django.apps.apps.get_app_config) become usable.
2. Then Django attempts to import the `models` submodule of each application,
  if there is one.
  You must define or import all models in your application’s `models.py` or
  `models/__init__.py`. Otherwise, the application registry may not be fully
  populated at this point, which could cause the ORM to malfunction.
  Once this stage completes, APIs that operate on models such as
  [get_model()](#django.apps.apps.get_model) become usable.
3. Finally Django runs the [ready()](#django.apps.AppConfig.ready) method of each application
  configuration.

### Troubleshooting¶

Here are some common problems that you may encounter during initialization:

- [AppRegistryNotReady](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.AppRegistryNotReady): This happens when
  importing an application configuration or a models module triggers code that
  depends on the app registry.
  For example, [gettext()](https://docs.djangoproject.com/en/5.0/utils/#django.utils.translation.gettext) uses the app
  registry to look up translation catalogs in applications. To translate at
  import time, you need [gettext_lazy()](https://docs.djangoproject.com/en/5.0/utils/#django.utils.translation.gettext_lazy)
  instead. (Using [gettext()](https://docs.djangoproject.com/en/5.0/utils/#django.utils.translation.gettext) would be a bug,
  because the translation would happen at import time, rather than at each
  request depending on the active language.)
  Executing database queries with the ORM at import time in models modules
  will also trigger this exception. The ORM cannot function properly until all
  models are available.
  This exception also happens if you forget to call [django.setup()](#django.setup) in
  a standalone Python script.
- `ImportError: cannot import name ...` This happens if the import sequence
  ends up in a loop.
  To eliminate such problems, you should minimize dependencies between your
  models modules and do as little work as possible at import time. To avoid
  executing code at import time, you can move it into a function and cache its
  results. The code will be executed when you first need its results. This
  concept is known as “lazy evaluation”.
- `django.contrib.admin` automatically performs autodiscovery of `admin`
  modules in installed applications. To prevent it, change your
  [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) to contain
  `'django.contrib.admin.apps.SimpleAdminConfig'` instead of
  `'django.contrib.admin'`.
- `RuntimeWarning: Accessing the database during app initialization is
  discouraged.` This warning is triggered for database queries executed before
  apps are ready, such as during module imports or in the
  [AppConfig.ready()](#django.apps.AppConfig.ready) method. Such premature database queries are
  discouraged because they will run during the startup of every management
  command, which will slow down your project startup, potentially cache stale
  data, and can even fail if migrations are pending.
  For example, a common mistake is making a database query to populate form
  field choices:
  ```
  class LocationForm(forms.Form):
      country = forms.ChoiceField(choices=[c.name for c in Country.objects.all()])
  ```
  In the example above, the query from `Country.objects.all()` is executed
  during module import, because the `QuerySet` is iterated over. To avoid the
  warning, the form could use a [ModelChoiceField](https://docs.djangoproject.com/en/5.0/forms/fields/#django.forms.ModelChoiceField)
  instead:
  ```
  class LocationForm(forms.Form):
      country = forms.ModelChoiceField(queryset=Country.objects.all())
  ```
  To make it easier to find the code that triggered this warning, you can make
  Python [treat warnings as errors](https://docs.python.org/3/library/warnings.html#warning-filter) to reveal the
  stack trace, for example with `python -Werror manage.py shell`.

---

# Class

# Class-based generic views - flattened index¶

This index provides an alternate organization of the reference documentation
for class-based views. For each view, the effective attributes and methods from
the class tree are represented under that view. For the reference
documentation organized by the class which defines the behavior, see
[Class-based views](https://docs.djangoproject.com/en/5.0/ref/).

See also

[Classy Class-Based Views](https://ccbv.co.uk/) provides a nice interface
to navigate the class hierarchy of the built-in class-based views.

## Simple generic views¶

### View¶

   *class*View[¶](#View)

**Attributes** (with optional accessor):

- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### TemplateView¶

   *class*TemplateView[¶](#TemplateView)

**Attributes** (with optional accessor):

- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.get_context_data)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### RedirectView¶

   *class*RedirectView[¶](#RedirectView)

**Attributes** (with optional accessor):

- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [pattern_name](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.RedirectView.pattern_name)
- [permanent](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.RedirectView.permanent)
- [query_string](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.RedirectView.query_string)
- [url](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.RedirectView.url) [[get_redirect_url()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.RedirectView.get_redirect_url)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- `delete()`
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- `options()`
- `post()`
- `put()`
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

## Detail Views¶

### DetailView¶

   *class*DetailView[¶](#DetailView)

**Attributes** (with optional accessor):

- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_object_name)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.model)
- [pk_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.pk_url_kwarg)
- [query_pk_and_slug](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.query_pk_and_slug)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [slug_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_field) [[get_slug_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_slug_field)]
- [slug_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_url_kwarg)
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_field)
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_suffix)

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- [get()](https://docs.djangoproject.com/en/5.0/ref/generic-display/#django.views.generic.detail.BaseDetailView.get)
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data)
- [get_object()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

## List Views¶

### ListView¶

   *class*ListView[¶](#ListView)

**Attributes** (with optional accessor):

- [allow_empty](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.allow_empty) [[get_allow_empty()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_allow_empty)]
- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_object_name)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model)
- [ordering](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.ordering) [[get_ordering()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_ordering)]
- [paginate_by](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_by) [[get_paginate_by()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_by)]
- [paginate_orphans](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_orphans) [[get_paginate_orphans()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_orphans)]
- [paginator_class](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginator_class)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin.template_name_suffix)

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- [get()](https://docs.djangoproject.com/en/5.0/ref/generic-display/#django.views.generic.list.BaseListView.get)
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_data)
- [get_paginator()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginator)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [paginate_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_queryset)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

## Editing views¶

### FormView¶

   *class*FormView[¶](#FormView)

**Attributes** (with optional accessor):

- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [form_class](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.form_class) [[get_form_class()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_form_class)]
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [initial](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.initial) [[get_initial()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_initial)]
- [prefix](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.prefix) [[get_prefix()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_prefix)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [success_url](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.success_url) [[get_success_url()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_success_url)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- [form_invalid()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.form_invalid)
- [form_valid()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.form_valid)
- [get()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ProcessFormView.get)
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_context_data)
- [get_form()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_form)
- [get_form_kwargs()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_form_kwargs)
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [post()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ProcessFormView.post)
- [put()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ProcessFormView.put)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### CreateView¶

   *class*CreateView[¶](#CreateView)

**Attributes** (with optional accessor):

- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_object_name)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [fields](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.fields)
- [form_class](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.form_class) [[get_form_class()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.get_form_class)]
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [initial](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.initial) [[get_initial()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_initial)]
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.model)
- [pk_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.pk_url_kwarg)
- [prefix](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.prefix) [[get_prefix()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_prefix)]
- [query_pk_and_slug](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.query_pk_and_slug)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [slug_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_field) [[get_slug_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_slug_field)]
- [slug_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_url_kwarg)
- [success_url](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.success_url) [[get_success_url()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.get_success_url)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_field)
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_suffix)

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- [form_invalid()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.form_invalid)
- [form_valid()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid)
- [get()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ProcessFormView.get)
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_context_data)
- [get_form()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_form)
- [get_form_kwargs()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.get_form_kwargs)
- [get_object()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [post()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ProcessFormView.post)
- `put()`
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### UpdateView¶

   *class*UpdateView[¶](#UpdateView)

**Attributes** (with optional accessor):

- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_object_name)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [fields](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.fields)
- [form_class](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.form_class) [[get_form_class()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.get_form_class)]
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [initial](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.initial) [[get_initial()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_initial)]
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.model)
- [pk_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.pk_url_kwarg)
- [prefix](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.prefix) [[get_prefix()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_prefix)]
- [query_pk_and_slug](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.query_pk_and_slug)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [slug_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_field) [[get_slug_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_slug_field)]
- [slug_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_url_kwarg)
- [success_url](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.success_url) [[get_success_url()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.get_success_url)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_field)
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_suffix)

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- [form_invalid()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.form_invalid)
- [form_valid()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid)
- [get()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ProcessFormView.get)
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_context_data)
- [get_form()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.FormMixin.get_form)
- [get_form_kwargs()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ModelFormMixin.get_form_kwargs)
- [get_object()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [post()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.ProcessFormView.post)
- `put()`
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### DeleteView¶

   *class*DeleteView[¶](#DeleteView)

**Attributes** (with optional accessor):

- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_object_name)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.model)
- [pk_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.pk_url_kwarg)
- [query_pk_and_slug](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.query_pk_and_slug)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [slug_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_field) [[get_slug_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_slug_field)]
- [slug_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_url_kwarg)
- [success_url](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.DeletionMixin.success_url) [[get_success_url()](https://docs.djangoproject.com/en/5.0/ref/mixins-editing/#django.views.generic.edit.DeletionMixin.get_success_url)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_field)
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_suffix)

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- `delete()`
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data)
- [get_object()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- `post()`
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

## Date-based views¶

### ArchiveIndexView¶

   *class*ArchiveIndexView[¶](#ArchiveIndexView)

**Attributes** (with optional accessor):

- [allow_empty](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.allow_empty) [[get_allow_empty()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_allow_empty)]
- [allow_future](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.allow_future) [[get_allow_future()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_allow_future)]
- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_object_name)]
- [date_field](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.date_field) [[get_date_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_date_field)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model)
- [ordering](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.ordering) [[get_ordering()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_ordering)]
- [paginate_by](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_by) [[get_paginate_by()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_by)]
- [paginate_orphans](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_orphans) [[get_paginate_orphans()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_orphans)]
- [paginator_class](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginator_class)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin.template_name_suffix)

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_data)
- [get_date_list()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_date_list)
- [get_dated_items()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_items)
- [get_dated_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_queryset)
- [get_paginator()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginator)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [paginate_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_queryset)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### YearArchiveView¶

   *class*YearArchiveView[¶](#YearArchiveView)

**Attributes** (with optional accessor):

- [allow_empty](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.allow_empty) [[get_allow_empty()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_allow_empty)]
- [allow_future](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.allow_future) [[get_allow_future()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_allow_future)]
- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_object_name)]
- [date_field](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.date_field) [[get_date_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_date_field)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [make_object_list](https://docs.djangoproject.com/en/5.0/ref/generic-date-based/#django.views.generic.dates.YearArchiveView.make_object_list) [[get_make_object_list()](https://docs.djangoproject.com/en/5.0/ref/generic-date-based/#django.views.generic.dates.YearArchiveView.get_make_object_list)]
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model)
- [ordering](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.ordering) [[get_ordering()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_ordering)]
- [paginate_by](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_by) [[get_paginate_by()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_by)]
- [paginate_orphans](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_orphans) [[get_paginate_orphans()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_orphans)]
- [paginator_class](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginator_class)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin.template_name_suffix)
- [year](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year) [[get_year()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year)]
- [year_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year_format) [[get_year_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year_format)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_data)
- [get_date_list()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_date_list)
- [get_dated_items()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_items)
- [get_dated_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_queryset)
- [get_paginator()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginator)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [paginate_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_queryset)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### MonthArchiveView¶

   *class*MonthArchiveView[¶](#MonthArchiveView)

**Attributes** (with optional accessor):

- [allow_empty](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.allow_empty) [[get_allow_empty()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_allow_empty)]
- [allow_future](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.allow_future) [[get_allow_future()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_allow_future)]
- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_object_name)]
- [date_field](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.date_field) [[get_date_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_date_field)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model)
- [month](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.month) [[get_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_month)]
- [month_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.month_format) [[get_month_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_month_format)]
- [ordering](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.ordering) [[get_ordering()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_ordering)]
- [paginate_by](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_by) [[get_paginate_by()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_by)]
- [paginate_orphans](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_orphans) [[get_paginate_orphans()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_orphans)]
- [paginator_class](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginator_class)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin.template_name_suffix)
- [year](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year) [[get_year()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year)]
- [year_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year_format) [[get_year_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year_format)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_data)
- [get_date_list()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_date_list)
- [get_dated_items()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_items)
- [get_dated_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_queryset)
- [get_next_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_next_month)
- [get_paginator()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginator)
- [get_previous_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_previous_month)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [paginate_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_queryset)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### WeekArchiveView¶

   *class*WeekArchiveView[¶](#WeekArchiveView)

**Attributes** (with optional accessor):

- [allow_empty](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.allow_empty) [[get_allow_empty()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_allow_empty)]
- [allow_future](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.allow_future) [[get_allow_future()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_allow_future)]
- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_object_name)]
- [date_field](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.date_field) [[get_date_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_date_field)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model)
- [ordering](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.ordering) [[get_ordering()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_ordering)]
- [paginate_by](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_by) [[get_paginate_by()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_by)]
- [paginate_orphans](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_orphans) [[get_paginate_orphans()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_orphans)]
- [paginator_class](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginator_class)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin.template_name_suffix)
- [week](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.WeekMixin.week) [[get_week()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.WeekMixin.get_week)]
- [week_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.WeekMixin.week_format) [[get_week_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.WeekMixin.get_week_format)]
- [year](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year) [[get_year()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year)]
- [year_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year_format) [[get_year_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year_format)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_data)
- [get_date_list()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_date_list)
- [get_dated_items()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_items)
- [get_dated_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_queryset)
- [get_paginator()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginator)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [paginate_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_queryset)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### DayArchiveView¶

   *class*DayArchiveView[¶](#DayArchiveView)

**Attributes** (with optional accessor):

- [allow_empty](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.allow_empty) [[get_allow_empty()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_allow_empty)]
- [allow_future](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.allow_future) [[get_allow_future()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_allow_future)]
- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_object_name)]
- [date_field](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.date_field) [[get_date_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_date_field)]
- [day](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.day) [[get_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_day)]
- [day_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.day_format) [[get_day_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_day_format)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model)
- [month](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.month) [[get_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_month)]
- [month_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.month_format) [[get_month_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_month_format)]
- [ordering](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.ordering) [[get_ordering()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_ordering)]
- [paginate_by](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_by) [[get_paginate_by()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_by)]
- [paginate_orphans](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_orphans) [[get_paginate_orphans()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_orphans)]
- [paginator_class](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginator_class)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin.template_name_suffix)
- [year](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year) [[get_year()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year)]
- [year_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year_format) [[get_year_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year_format)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_data)
- [get_date_list()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_date_list)
- [get_dated_items()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_items)
- [get_dated_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_queryset)
- [get_next_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_next_day)
- [get_next_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_next_month)
- [get_paginator()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginator)
- [get_previous_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_previous_day)
- [get_previous_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_previous_month)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [paginate_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_queryset)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### TodayArchiveView¶

   *class*TodayArchiveView[¶](#TodayArchiveView)

**Attributes** (with optional accessor):

- [allow_empty](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.allow_empty) [[get_allow_empty()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_allow_empty)]
- [allow_future](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.allow_future) [[get_allow_future()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_allow_future)]
- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_object_name)]
- [date_field](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.date_field) [[get_date_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_date_field)]
- [day](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.day) [[get_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_day)]
- [day_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.day_format) [[get_day_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_day_format)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model)
- [month](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.month) [[get_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_month)]
- [month_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.month_format) [[get_month_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_month_format)]
- [ordering](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.ordering) [[get_ordering()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_ordering)]
- [paginate_by](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_by) [[get_paginate_by()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_by)]
- [paginate_orphans](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_orphans) [[get_paginate_orphans()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginate_orphans)]
- [paginator_class](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginator_class)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin.template_name_suffix)
- [year](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year) [[get_year()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year)]
- [year_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year_format) [[get_year_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year_format)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_context_data)
- [get_date_list()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_date_list)
- [get_dated_items()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_items)
- [get_dated_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.BaseDateListView.get_dated_queryset)
- [get_next_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_next_day)
- [get_next_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_next_month)
- [get_paginator()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_paginator)
- [get_previous_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_previous_day)
- [get_previous_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_previous_month)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [paginate_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_queryset)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

### DateDetailView¶

   *class*DateDetailView[¶](#DateDetailView)

**Attributes** (with optional accessor):

- [allow_future](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.allow_future) [[get_allow_future()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_allow_future)]
- [content_type](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.content_type)
- [context_object_name](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.context_object_name) [[get_context_object_name()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_object_name)]
- [date_field](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.date_field) [[get_date_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DateMixin.get_date_field)]
- [day](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.day) [[get_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_day)]
- [day_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.day_format) [[get_day_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_day_format)]
- [extra_context](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.ContextMixin.extra_context)
- [http_method_names](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_names)
- [model](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.model)
- [month](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.month) [[get_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_month)]
- [month_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.month_format) [[get_month_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_month_format)]
- [pk_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.pk_url_kwarg)
- [query_pk_and_slug](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.query_pk_and_slug)
- [queryset](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.queryset) [[get_queryset()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_queryset)]
- [response_class](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class) [[render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)]
- [slug_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_field) [[get_slug_field()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_slug_field)]
- [slug_url_kwarg](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.slug_url_kwarg)
- [template_engine](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_engine)
- [template_name](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) [[get_template_names()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)]
- [template_name_field](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_field)
- [template_name_suffix](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_suffix)
- [year](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year) [[get_year()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year)]
- [year_format](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.year_format) [[get_year_format()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.YearMixin.get_year_format)]

**Methods**

- [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view)
- [dispatch()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.dispatch)
- `get()`
- [get_context_data()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data)
- [get_next_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_next_day)
- [get_next_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_next_month)
- [get_object()](https://docs.djangoproject.com/en/5.0/ref/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object)
- [get_previous_day()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.DayMixin.get_previous_day)
- [get_previous_month()](https://docs.djangoproject.com/en/5.0/ref/mixins-date-based/#django.views.generic.dates.MonthMixin.get_previous_month)
- `head()`
- [http_method_not_allowed()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.http_method_not_allowed)
- [render_to_response()](https://docs.djangoproject.com/en/5.0/ref/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
- [setup()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.setup)

---

# Built

# Built-in class-based views API¶

Class-based views API reference. For introductory material, see the
[Class-based views](https://docs.djangoproject.com/en/topics/class-based-views/) topic guide.

## Specification¶

Each request served by a class-based view has an independent state; therefore,
it is safe to store state variables on the instance (i.e., `self.foo = 3` is
a thread-safe operation).

A class-based view is deployed into a URL pattern using the
[as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view) classmethod:

```
urlpatterns = [
    path("view/", MyView.as_view(size=42)),
]
```

Thread safety with view arguments

Arguments passed to a view are shared between every instance of a view.
This means that you shouldn’t use a list, dictionary, or any other
mutable object as an argument to a view. If you do and the shared object
is modified, the actions of one user visiting your view could have an
effect on subsequent users visiting the same view.

Arguments passed into [as_view()](https://docs.djangoproject.com/en/5.0/ref/base/#django.views.generic.base.View.as_view) will
be assigned onto the instance that is used to service a request. Using the
previous example, this means that every request on `MyView` is able to use
`self.size`. Arguments must correspond to attributes that already exist on
the class (return `True` on a `hasattr` check).

## Base vs Generic views¶

Base class-based views can be thought of as *parent* views, which can be
used by themselves or inherited from. They may not provide all the
capabilities required for projects, in which case there are Mixins which
extend what base views can do.

Django’s generic views are built off of those base views, and were developed
as a shortcut for common usage patterns such as displaying the details of an
object. They take certain common idioms and patterns found in view
development and abstract them so that you can quickly write common views of
data without having to repeat yourself.

Most generic views require the `queryset` key, which is a `QuerySet`
instance; see [Making queries](https://docs.djangoproject.com/en/topics/db/queries/) for more information about `QuerySet`
objects.

---

# Clickjacking Protection¶

# Clickjacking Protection¶

The clickjacking middleware and decorators provide easy-to-use protection
against [clickjacking](https://en.wikipedia.org/wiki/Clickjacking).  This type of attack occurs when a malicious site
tricks a user into clicking on a concealed element of another site which they
have loaded in a hidden frame or iframe.

## An example of clickjacking¶

Suppose an online store has a page where a logged in user can click “Buy Now” to
purchase an item. A user has chosen to stay logged into the store all the time
for convenience. An attacker site might create an “I Like Ponies” button on one
of their own pages, and load the store’s page in a transparent iframe such that
the “Buy Now” button is invisibly overlaid on the “I Like Ponies” button. If the
user visits the attacker’s site, clicking “I Like Ponies” will cause an
inadvertent click on the “Buy Now” button and an unknowing purchase of the item.

## Preventing clickjacking¶

Modern browsers honor the [X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options) HTTP header that indicates whether
or not a resource is allowed to load within a frame or iframe. If the response
contains the header with a value of `SAMEORIGIN` then the browser will only
load the resource in a frame if the request originated from the same site. If
the header is set to `DENY` then the browser will block the resource from
loading in a frame no matter which site made the request.

Django provides a few ways to include this header in responses from your site:

1. A middleware that sets the header in all responses.
2. A set of view decorators that can be used to override the middleware or to
  only set the header for certain views.

The `X-Frame-Options` HTTP header will only be set by the middleware or view
decorators if it is not already present in the response.

## How to use it¶

### SettingX-Frame-Optionsfor all responses¶

To set the same `X-Frame-Options` value for all responses in your site, put
`'django.middleware.clickjacking.XFrameOptionsMiddleware'` to
[MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE):

```
MIDDLEWARE = [
    ...,
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ...,
]
```

This middleware is enabled in the settings file generated by
[startproject](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-startproject).

By default, the middleware will set the `X-Frame-Options` header to
`DENY` for every outgoing `HttpResponse`. If you want any other value for
this header instead, set the [X_FRAME_OPTIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-X_FRAME_OPTIONS) setting:

```
X_FRAME_OPTIONS = "SAMEORIGIN"
```

When using the middleware there may be some views where you do **not** want the
`X-Frame-Options` header set. For those cases, you can use a view decorator
that tells the middleware not to set the header:

```
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def ok_to_load_in_a_frame(request):
    return HttpResponse("This page is safe to load in a frame on any site.")
```

Note

If you want to submit a form or access a session cookie within a frame or
iframe, you may need to modify the [CSRF_COOKIE_SAMESITE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_SAMESITE) or
[SESSION_COOKIE_SAMESITE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SESSION_COOKIE_SAMESITE) settings.

   Changed in Django 5.0:

Support for wrapping asynchronous view functions was added to the
`@xframe_options_exempt` decorator.

### SettingX-Frame-Optionsper view¶

To set the `X-Frame-Options` header on a per view basis, Django provides these
decorators:

```
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin

@xframe_options_deny
def view_one(request):
    return HttpResponse("I won't display in any frame!")

@xframe_options_sameorigin
def view_two(request):
    return HttpResponse("Display in a frame if it's from the same origin as me.")
```

Note that you can use the decorators in conjunction with the middleware. Use of
a decorator overrides the middleware.

  Changed in Django 5.0:

Support for wrapping asynchronous view functions was added to the
`@xframe_options_deny` and `@xframe_options_sameorigin` decorators.

## Limitations¶

The `X-Frame-Options` header will only protect against clickjacking in
[modern browsers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options#browser_compatibility).
