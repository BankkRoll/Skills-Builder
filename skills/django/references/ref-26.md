---

# TemplateResponseandSimpleTemplateResponse¶

# TemplateResponseandSimpleTemplateResponse¶

Standard [HttpResponse](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponse) objects are static structures.
They are provided with a block of pre-rendered content at time of
construction, and while that content can be modified, it isn’t in a form that
makes it easy to perform modifications.

However, it can sometimes be beneficial to allow decorators or
middleware to modify a response *after* it has been constructed by the
view. For example, you may want to change the template that is used,
or put additional data into the context.

TemplateResponse provides a way to do just that. Unlike basic
[HttpResponse](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponse) objects, TemplateResponse objects retain
the details of the template and context that was provided by the view to
compute the response. The final output of the response is not computed until
it is needed, later in the response process.

## SimpleTemplateResponseobjects¶

   *class*SimpleTemplateResponse[[source]](https://docs.djangoproject.com/en/_modules/django/template/response/#SimpleTemplateResponse)[¶](#django.template.response.SimpleTemplateResponse)

### Attributes¶

   SimpleTemplateResponse.template_name[¶](#django.template.response.SimpleTemplateResponse.template_name)

The name of the template to be rendered. Accepts a backend-dependent
template object (such as those returned by
[get_template()](https://docs.djangoproject.com/en/topics/templates/#django.template.loader.get_template)), the name of a template,
or a list of template names.

Example: `['foo.html', 'path/to/bar.html']`

    SimpleTemplateResponse.context_data[¶](#django.template.response.SimpleTemplateResponse.context_data)

The context data to be used when rendering the template. It must be a
[dict](https://docs.python.org/3/library/stdtypes.html#dict).

Example: `{'foo': 123}`

    SimpleTemplateResponse.rendered_content[¶](#django.template.response.SimpleTemplateResponse.rendered_content)

The current rendered value of the response content, using the current
template and context data.

    SimpleTemplateResponse.is_rendered[¶](#django.template.response.SimpleTemplateResponse.is_rendered)

A boolean indicating whether the response content has been rendered.

### Methods¶

   SimpleTemplateResponse.__init__(*template*, *context=None*, *content_type=None*, *status=None*, *charset=None*, *using=None*, *headers=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/response/#SimpleTemplateResponse.__init__)[¶](#django.template.response.SimpleTemplateResponse.__init__)

Instantiates a [SimpleTemplateResponse](#django.template.response.SimpleTemplateResponse)
object with the given template, context, content type, HTTP status, and
charset.

  `template`

A backend-dependent template object (such as those returned by
[get_template()](https://docs.djangoproject.com/en/topics/templates/#django.template.loader.get_template)), the name of a template,
or a list of template names.

  `context`

A [dict](https://docs.python.org/3/library/stdtypes.html#dict) of values to add to the template context. By default,
this is an empty dictionary.

  `content_type`

The value included in the HTTP `Content-Type` header, including the
MIME type specification and the character set encoding. If
`content_type` is specified, then its value is used. Otherwise,
`'text/html'` is used.

  `status`

The HTTP status code for the response.

  `charset`

The charset in which the response will be encoded. If not given it will
be extracted from `content_type`, and if that is unsuccessful, the
[DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting will be used.

  `using`

The [NAME](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-NAME) of a template engine to use for
loading the template.

  `headers`

A [dict](https://docs.python.org/3/library/stdtypes.html#dict) of HTTP headers to add to the response.

      SimpleTemplateResponse.resolve_context(*context*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/response/#SimpleTemplateResponse.resolve_context)[¶](#django.template.response.SimpleTemplateResponse.resolve_context)

Preprocesses context data that will be used for rendering a template.
Accepts a [dict](https://docs.python.org/3/library/stdtypes.html#dict) of context data. By default, returns the same
[dict](https://docs.python.org/3/library/stdtypes.html#dict).

Override this method in order to customize the context.

    SimpleTemplateResponse.resolve_template(*template*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/response/#SimpleTemplateResponse.resolve_template)[¶](#django.template.response.SimpleTemplateResponse.resolve_template)

Resolves the template instance to use for rendering. Accepts a
backend-dependent template object (such as those returned by
[get_template()](https://docs.djangoproject.com/en/topics/templates/#django.template.loader.get_template)), the name of a template,
or a list of template names.

Returns the backend-dependent template object instance to be rendered.

Override this method in order to customize template loading.

    SimpleTemplateResponse.add_post_render_callback()[[source]](https://docs.djangoproject.com/en/_modules/django/template/response/#SimpleTemplateResponse.add_post_render_callback)[¶](#django.template.response.SimpleTemplateResponse.add_post_render_callback)

Add a callback that will be invoked after rendering has taken
place. This hook can be used to defer certain processing
operations (such as caching) until after rendering has occurred.

If the [SimpleTemplateResponse](#django.template.response.SimpleTemplateResponse)
has already been rendered, the callback will be invoked
immediately.

When called, callbacks will be passed a single argument – the
rendered [SimpleTemplateResponse](#django.template.response.SimpleTemplateResponse)
instance.

If the callback returns a value that is not `None`, this will be
used as the response instead of the original response object (and
will be passed to the next post rendering callback etc.)

    SimpleTemplateResponse.render()[¶](#django.template.response.SimpleTemplateResponse.render)

Sets `response.content` to the result obtained by
[SimpleTemplateResponse.rendered_content](#django.template.response.SimpleTemplateResponse.rendered_content), runs all post-rendering
callbacks, and returns the resulting response object.

`render()` will only have an effect the first time it is called. On
subsequent calls, it will return the result obtained from the first call.

## TemplateResponseobjects¶

   *class*TemplateResponse[[source]](https://docs.djangoproject.com/en/_modules/django/template/response/#TemplateResponse)[¶](#django.template.response.TemplateResponse)

`TemplateResponse` is a subclass of
[SimpleTemplateResponse](#django.template.response.SimpleTemplateResponse) that knows about
the current [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest).

### Methods¶

   TemplateResponse.__init__(*request*, *template*, *context=None*, *content_type=None*, *status=None*, *charset=None*, *using=None*, *headers=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/response/#TemplateResponse.__init__)[¶](#django.template.response.TemplateResponse.__init__)

Instantiates a [TemplateResponse](#django.template.response.TemplateResponse) object
with the given request, template, context, content type, HTTP status, and
charset.

  `request`

An [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) instance.

  `template`

A backend-dependent template object (such as those returned by
[get_template()](https://docs.djangoproject.com/en/topics/templates/#django.template.loader.get_template)), the name of a template,
or a list of template names.

  `context`

A [dict](https://docs.python.org/3/library/stdtypes.html#dict) of values to add to the template context. By default,
this is an empty dictionary.

  `content_type`

The value included in the HTTP `Content-Type` header, including the
MIME type specification and the character set encoding. If
`content_type` is specified, then its value is used. Otherwise,
`'text/html'` is used.

  `status`

The HTTP status code for the response.

  `charset`

The charset in which the response will be encoded. If not given it will
be extracted from `content_type`, and if that is unsuccessful, the
[DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting will be used.

  `using`

The [NAME](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-NAME) of a template engine to use for
loading the template.

  `headers`

A [dict](https://docs.python.org/3/library/stdtypes.html#dict) of HTTP headers to add to the response.

## The rendering process¶

Before a [TemplateResponse](#django.template.response.TemplateResponse) instance can be
returned to the client, it must be rendered. The rendering process takes the
intermediate representation of template and context, and turns it into the
final byte stream that can be served to the client.

There are three circumstances under which a `TemplateResponse` will be
rendered:

- When the `TemplateResponse` instance is explicitly rendered, using
  the [SimpleTemplateResponse.render()](#django.template.response.SimpleTemplateResponse.render) method.
- When the content of the response is explicitly set by assigning
  `response.content`.
- After passing through template response middleware, but before
  passing through response middleware.

A `TemplateResponse` can only be rendered once. The first call to
[SimpleTemplateResponse.render()](#django.template.response.SimpleTemplateResponse.render) sets the content of the response;
subsequent rendering calls do not change the response content.

However, when `response.content` is explicitly assigned, the
change is always applied. If you want to force the content to be
re-rendered, you can reevaluate the rendered content, and assign
the content of the response manually:

```
# Set up a rendered TemplateResponse
>>> from django.template.response import TemplateResponse
>>> t = TemplateResponse(request, "original.html", {})
>>> t.render()
>>> print(t.content)
Original content

# Re-rendering doesn't change content
>>> t.template_name = "new.html"
>>> t.render()
>>> print(t.content)
Original content

# Assigning content does change, no render() call required
>>> t.content = t.rendered_content
>>> print(t.content)
New content
```

### Post-render callbacks¶

Some operations – such as caching – cannot be performed on an
unrendered template. They must be performed on a fully complete and
rendered response.

If you’re using middleware, you can do that. Middleware provides
multiple opportunities to process a response on exit from a view. If
you put behavior in the response middleware, it’s guaranteed to execute
after template rendering has taken place.

However, if you’re using a decorator, the same opportunities do not
exist. Any behavior defined in a decorator is handled immediately.

To compensate for this (and any other analogous use cases),
[TemplateResponse](#django.template.response.TemplateResponse) allows you to register callbacks that will
be invoked when rendering has completed. Using this callback, you can
defer critical processing until a point where you can guarantee that
rendered content will be available.

To define a post-render callback, define a function that takes
a single argument – response – and register that function with
the template response:

```
from django.template.response import TemplateResponse

def my_render_callback(response):
    # Do content-sensitive processing
    do_post_processing()

def my_view(request):
    # Create a response
    response = TemplateResponse(request, "mytemplate.html", {})
    # Register the callback
    response.add_post_render_callback(my_render_callback)
    # Return the response
    return response
```

`my_render_callback()` will be invoked after the `mytemplate.html`
has been rendered, and will be provided the fully rendered
[TemplateResponse](#django.template.response.TemplateResponse) instance as an argument.

If the template has already been rendered, the callback will be
invoked immediately.

## UsingTemplateResponseandSimpleTemplateResponse¶

A [TemplateResponse](#django.template.response.TemplateResponse) object can be used anywhere that a normal
[django.http.HttpResponse](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponse) can be used. It can also be used as an
alternative to calling [render()](https://docs.djangoproject.com/en/topics/http/shortcuts/#django.shortcuts.render).

For example, the following view returns a [TemplateResponse](#django.template.response.TemplateResponse) with a
template and a context containing a queryset:

```
from django.template.response import TemplateResponse

def blog_index(request):
    return TemplateResponse(
        request, "entry_list.html", {"entries": Entry.objects.all()}
    )
```

---

# The Django template language: for Python programmers¶

# The Django template language: for Python programmers¶

This document explains the Django template system from a technical
perspective – how it works and how to extend it. If you’re looking for
reference on the language syntax, see [The Django template language](https://docs.djangoproject.com/en/5.0/ref/language/).

It assumes an understanding of templates, contexts, variables, tags, and
rendering. Start with the [introduction to the Django template language](https://docs.djangoproject.com/en/topics/templates/#template-language-intro) if you aren’t familiar with these concepts.

## Overview¶

Using the template system in Python is a three-step process:

1. You configure an [Engine](#django.template.Engine).
2. You compile template code into a [Template](#django.template.Template).
3. You render the template with a [Context](#django.template.Context).

Django projects generally rely on the [high level, backend agnostic APIs](https://docs.djangoproject.com/en/topics/templates/#template-engines) for each of these steps instead of the template system’s
lower level APIs:

1. For each [DjangoTemplates](https://docs.djangoproject.com/en/topics/templates/#django.template.backends.django.DjangoTemplates) backend
  in the [TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES) setting, Django instantiates an
  [Engine](#django.template.Engine). [DjangoTemplates](https://docs.djangoproject.com/en/topics/templates/#django.template.backends.django.DjangoTemplates)
  wraps [Engine](#django.template.Engine) and adapts it to the common template backend API.
2. The [django.template.loader](https://docs.djangoproject.com/en/topics/templates/#module-django.template.loader) module provides functions such as
  [get_template()](https://docs.djangoproject.com/en/topics/templates/#django.template.loader.get_template) for loading templates. They
  return a `django.template.backends.django.Template` which wraps the
  actual [django.template.Template](#django.template.Template).
3. The `Template` obtained in the previous step has a
  [render()](https://docs.djangoproject.com/en/topics/templates/#django.template.backends.base.Template.render) method which
  marshals a context and possibly a request into a [Context](#django.template.Context) and
  delegates the rendering to the underlying [Template](#django.template.Template).

## Configuring an engine¶

If you are using the [DjangoTemplates](https://docs.djangoproject.com/en/topics/templates/#django.template.backends.django.DjangoTemplates)
backend, this probably isn’t the documentation you’re looking for. An instance
of the `Engine` class described below is accessible using the `engine`
attribute of that backend and any attribute defaults mentioned below are
overridden by what’s passed by
[DjangoTemplates](https://docs.djangoproject.com/en/topics/templates/#django.template.backends.django.DjangoTemplates).

   *class*Engine(*dirs=None*, *app_dirs=False*, *context_processors=None*, *debug=False*, *loaders=None*, *string_if_invalid=''*, *file_charset='utf-8'*, *libraries=None*, *builtins=None*, *autoescape=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/engine/#Engine)[¶](#django.template.Engine)

When instantiating an `Engine` all arguments must be passed as keyword
arguments:

- `dirs` is a list of directories where the engine should look for
  template source files. It is used to configure
  [filesystem.Loader](#django.template.loaders.filesystem.Loader).
  It defaults to an empty list.
- `app_dirs` only affects the default value of `loaders`. See below.
  It defaults to `False`.
- `autoescape` controls whether HTML autoescaping is enabled.
  It defaults to `True`.
  Warning
  Only set it to `False` if you’re rendering non-HTML templates!
- `context_processors` is a list of dotted Python paths to callables
  that are used to populate the context when a template is rendered with a
  request. These callables take a request object as their argument and
  return a [dict](https://docs.python.org/3/library/stdtypes.html#dict) of items to be merged into the context.
  It defaults to an empty list.
  See [RequestContext](#django.template.RequestContext) for more information.
- `debug` is a boolean that turns on/off template debug mode. If it is
  `True`, the template engine will store additional debug information
  which can be used to display a detailed report for any exception raised
  during template rendering.
  It defaults to `False`.
- `loaders` is a list of template loader classes, specified as strings.
  Each `Loader` class knows how to import templates from a particular
  source. Optionally, a tuple can be used instead of a string. The first
  item in the tuple should be the `Loader` class name, subsequent items
  are passed to the `Loader` during initialization.
  It defaults to a list containing:
  - `'django.template.loaders.filesystem.Loader'`
  - `'django.template.loaders.app_directories.Loader'` if and only if
    `app_dirs` is `True`.
  These loaders are then wrapped in
  [django.template.loaders.cached.Loader](#django.template.loaders.cached.Loader).
  See [Loader types](#template-loaders) for details.
- `string_if_invalid` is the output, as a string, that the template
  system should use for invalid (e.g. misspelled) variables.
  It defaults to the empty string.
  See [How invalid variables are handled](#invalid-template-variables) for details.
- `file_charset` is the charset used to read template files on disk.
  It defaults to `'utf-8'`.
- `'libraries'`: A dictionary of labels and dotted Python paths of template
  tag modules to register with the template engine. This is used to add new
  libraries or provide alternate labels for existing ones. For example:
  ```
  Engine(
      libraries={
          "myapp_tags": "path.to.myapp.tags",
          "admin.urls": "django.contrib.admin.templatetags.admin_urls",
      },
  )
  ```
  Libraries can be loaded by passing the corresponding dictionary key to
  the [{%load%}](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-load) tag.
- `'builtins'`: A list of dotted Python paths of template tag modules to
  add to [built-ins](https://docs.djangoproject.com/en/5.0/ref/builtins/). For example:
  ```
  Engine(
      builtins=["myapp.builtins"],
  )
  ```
  Tags and filters from built-in libraries can be used without first calling
  the [{%load%}](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-load) tag.

    *static*Engine.get_default()[[source]](https://docs.djangoproject.com/en/_modules/django/template/engine/#Engine.get_default)[¶](#django.template.Engine.get_default)

Returns the underlying [Engine](#django.template.Engine) from the first configured
[DjangoTemplates](https://docs.djangoproject.com/en/topics/templates/#django.template.backends.django.DjangoTemplates) engine. Raises
[ImproperlyConfigured](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ImproperlyConfigured) if no engines are
configured.

It’s required for preserving APIs that rely on a globally available,
implicitly configured engine. Any other use is strongly discouraged.

    Engine.from_string(*template_code*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/engine/#Engine.from_string)[¶](#django.template.Engine.from_string)

Compiles the given template code and returns a [Template](#django.template.Template) object.

    Engine.get_template(*template_name*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/engine/#Engine.get_template)[¶](#django.template.Engine.get_template)

Loads a template with the given name, compiles it and returns a
[Template](#django.template.Template) object.

    Engine.select_template(*template_name_list*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/engine/#Engine.select_template)[¶](#django.template.Engine.select_template)

Like [get_template()](#django.template.Engine.get_template), except it takes a list of names
and returns the first template that was found.

## Loading a template¶

The recommended way to create a [Template](#django.template.Template) is by calling the factory
methods of the [Engine](#django.template.Engine): [get_template()](#django.template.Engine.get_template),
[select_template()](#django.template.Engine.select_template) and [from_string()](#django.template.Engine.from_string).

In a Django project where the [TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES) setting defines a
[DjangoTemplates](https://docs.djangoproject.com/en/topics/templates/#django.template.backends.django.DjangoTemplates) engine, it’s
possible to instantiate a [Template](#django.template.Template) directly. If more than one
[DjangoTemplates](https://docs.djangoproject.com/en/topics/templates/#django.template.backends.django.DjangoTemplates) engine is defined,
the first one will be used.

   *class*Template[[source]](https://docs.djangoproject.com/en/_modules/django/template/base/#Template)[¶](#django.template.Template)

This class lives at `django.template.Template`. The constructor takes
one argument — the raw template code:

```
from django.template import Template

template = Template("My name is {{ my_name }}.")
```

Behind the scenes

The system only parses your raw template code once – when you create the
`Template` object. From then on, it’s stored internally as a tree
structure for performance.

Even the parsing itself is quite fast. Most of the parsing happens via a
single call to a single, short, regular expression.

## Rendering a context¶

Once you have a compiled [Template](#django.template.Template) object, you can render a context
with it. You can reuse the same template to render it several times with
different contexts.

   *class*Context(*dict_=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/context/#Context)[¶](#django.template.Context)

The constructor of `django.template.Context` takes an optional argument —
a dictionary mapping variable names to variable values.

For details, see [Playing with Context objects](#playing-with-context) below.

    Template.render(*context*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/base/#Template.render)[¶](#django.template.Template.render)

Call the [Template](#django.template.Template) object’s `render()` method with a
[Context](#django.template.Context) to “fill” the template:

```
>>> from django.template import Context, Template
>>> template = Template("My name is {{ my_name }}.")

>>> context = Context({"my_name": "Adrian"})
>>> template.render(context)
"My name is Adrian."

>>> context = Context({"my_name": "Dolores"})
>>> template.render(context)
"My name is Dolores."
```

### Variables and lookups¶

Variable names must consist of any letter (A-Z), any digit (0-9), an underscore
(but they must not start with an underscore) or a dot.

Dots have a special meaning in template rendering. A dot in a variable name
signifies a **lookup**. Specifically, when the template system encounters a
dot in a variable name, it tries the following lookups, in this order:

- Dictionary lookup. Example: `foo["bar"]`
- Attribute lookup. Example: `foo.bar`
- List-index lookup. Example: `foo[bar]`

Note that “bar” in a template expression like `{{ foo.bar }}` will be
interpreted as a literal string and not using the value of the variable “bar”,
if one exists in the template context.

The template system uses the first lookup type that works. It’s short-circuit
logic. Here are a few examples:

```
>>> from django.template import Context, Template
>>> t = Template("My name is {{ person.first_name }}.")
>>> d = {"person": {"first_name": "Joe", "last_name": "Johnson"}}
>>> t.render(Context(d))
"My name is Joe."

>>> class PersonClass:
...     pass
...
>>> p = PersonClass()
>>> p.first_name = "Ron"
>>> p.last_name = "Nasty"
>>> t.render(Context({"person": p}))
"My name is Ron."

>>> t = Template("The first stooge in the list is {{ stooges.0 }}.")
>>> c = Context({"stooges": ["Larry", "Curly", "Moe"]})
>>> t.render(c)
"The first stooge in the list is Larry."
```

If any part of the variable is callable, the template system will try calling
it. Example:

```
>>> class PersonClass2:
...     def name(self):
...         return "Samantha"
...
>>> t = Template("My name is {{ person.name }}.")
>>> t.render(Context({"person": PersonClass2}))
"My name is Samantha."
```

Callable variables are slightly more complex than variables which only require
straight lookups. Here are some things to keep in mind:

- If the variable raises an exception when called, the exception will be
  propagated, unless the exception has an attribute
  `silent_variable_failure` whose value is `True`. If the exception
  *does* have a `silent_variable_failure` attribute whose value is
  `True`, the variable will render as the value of the engine’s
  `string_if_invalid` configuration option (an empty string, by default).
  Example:
  ```
  >>> t = Template("My name is {{ person.first_name }}.")
  >>> class PersonClass3:
  ...     def first_name(self):
  ...         raise AssertionError("foo")
  ...
  >>> p = PersonClass3()
  >>> t.render(Context({"person": p}))
  Traceback (most recent call last):
  ...
  AssertionError: foo
  >>> class SilentAssertionError(Exception):
  ...     silent_variable_failure = True
  ...
  >>> class PersonClass4:
  ...     def first_name(self):
  ...         raise SilentAssertionError
  ...
  >>> p = PersonClass4()
  >>> t.render(Context({"person": p}))
  "My name is ."
  ```
  Note that [django.core.exceptions.ObjectDoesNotExist](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ObjectDoesNotExist), which is the
  base class for all Django database API `DoesNotExist` exceptions, has
  `silent_variable_failure = True`. So if you’re using Django templates
  with Django model objects, any `DoesNotExist` exception will fail
  silently.
- A variable can only be called if it has no required arguments. Otherwise,
  the system will return the value of the engine’s `string_if_invalid`
  option.

- There can be side effects when calling some variables, and it’d be either
  foolish or a security hole to allow the template system to access them.
  A good example is the [delete()](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model.delete) method on
  each Django model object. The template system shouldn’t be allowed to do
  something like this:
  ```
  I will now delete this valuable data. {{ data.delete }}
  ```
  To prevent this, set an `alters_data` attribute on the callable
  variable. The template system won’t call a variable if it has
  `alters_data=True` set, and will instead replace the variable with
  `string_if_invalid`, unconditionally.  The
  dynamically-generated [delete()](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model.delete) and
  [save()](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model.save) methods on Django model objects get
  `alters_data=True` automatically. Example:
  ```
  def sensitive_function(self):
      self.database_record.delete()
  sensitive_function.alters_data = True
  ```
- Occasionally you may want to turn off this feature for other reasons,
  and tell the template system to leave a variable uncalled no matter
  what.  To do so, set a `do_not_call_in_templates` attribute on the
  callable with the value `True`.  The template system then will act as
  if your variable is not callable (allowing you to access attributes of
  the callable, for example).

### How invalid variables are handled¶

Generally, if a variable doesn’t exist, the template system inserts the value
of the engine’s `string_if_invalid` configuration option, which is set to
`''` (the empty string) by default.

Filters that are applied to an invalid variable will only be applied if
`string_if_invalid` is set to `''` (the empty string). If
`string_if_invalid` is set to any other value, variable filters will be
ignored.

This behavior is slightly different for the `if`, `for` and `regroup`
template tags. If an invalid variable is provided to one of these template
tags, the variable will be interpreted as `None`. Filters are always
applied to invalid variables within these template tags.

If `string_if_invalid` contains a `'%s'`, the format marker will be
replaced with the name of the invalid variable.

For debug purposes only!

While `string_if_invalid` can be a useful debugging tool, it is a bad
idea to turn it on as a ‘development default’.

Many templates, including some of Django’s, rely upon the silence of the
template system when a nonexistent variable is encountered. If you assign a
value other than `''` to `string_if_invalid`, you will experience
rendering problems with these templates and sites.

Generally, `string_if_invalid` should only be enabled in order to debug
a specific template problem, then cleared once debugging is complete.

### Built-in variables¶

Every context contains `True`, `False` and `None`. As you would expect,
these variables resolve to the corresponding Python objects.

### Limitations with string literals¶

Django’s template language has no way to escape the characters used for its own
syntax. For example, the [templatetag](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-templatetag) tag is required if you need to
output character sequences like `{%` and `%}`.

A similar issue exists if you want to include these sequences in template filter
or tag arguments. For example, when parsing a block tag, Django’s template
parser looks for the first occurrence of `%}` after a `{%`. This prevents
the use of `"%}"` as a string literal. For example, a `TemplateSyntaxError`
will be raised for the following expressions:

```
{% include "template.html" tvar="Some string literal with %} in it." %}

{% with tvar="Some string literal with %} in it." %}{% endwith %}
```

The same issue can be triggered by using a reserved sequence in filter
arguments:

```
{{ some.variable|default:"}}" }}
```

If you need to use strings with these sequences, store them in template
variables or use a custom template tag or filter to workaround the limitation.

## Playing withContextobjects¶

Most of the time, you’ll instantiate [Context](#django.template.Context) objects by passing in a
fully-populated dictionary to `Context()`. But you can add and delete items
from a `Context` object once it’s been instantiated, too, using standard
dictionary syntax:

```
>>> from django.template import Context
>>> c = Context({"foo": "bar"})
>>> c["foo"]
'bar'
>>> del c["foo"]
>>> c["foo"]
Traceback (most recent call last):
...
KeyError: 'foo'
>>> c["newvariable"] = "hello"
>>> c["newvariable"]
'hello'
```

    Context.get(*key*, *otherwise=None*)[¶](#django.template.Context.get)

Returns the value for `key` if `key` is in the context, else returns
`otherwise`.

    Context.setdefault(*key*, *default=None*)[¶](#django.template.Context.setdefault)

If `key` is in the context, returns its value. Otherwise inserts `key`
with a value of `default` and returns `default`.

    Context.pop()[¶](#django.template.Context.pop)    Context.push()[¶](#django.template.Context.push)    *exception*ContextPopException[[source]](https://docs.djangoproject.com/en/_modules/django/template/context/#ContextPopException)[¶](#django.template.ContextPopException)

A `Context` object is a stack. That is, you can `push()` and `pop()` it.
If you `pop()` too much, it’ll raise
`django.template.ContextPopException`:

```
>>> c = Context()
>>> c["foo"] = "first level"
>>> c.push()
{}
>>> c["foo"] = "second level"
>>> c["foo"]
'second level'
>>> c.pop()
{'foo': 'second level'}
>>> c["foo"]
'first level'
>>> c["foo"] = "overwritten"
>>> c["foo"]
'overwritten'
>>> c.pop()
Traceback (most recent call last):
...
ContextPopException
```

You can also use `push()` as a context manager to ensure a matching `pop()`
is called.

```
>>> c = Context()
>>> c["foo"] = "first level"
>>> with c.push():
...     c["foo"] = "second level"
...     c["foo"]
...
'second level'
>>> c["foo"]
'first level'
```

All arguments passed to `push()` will be passed to the `dict` constructor
used to build the new context level.

```
>>> c = Context()
>>> c["foo"] = "first level"
>>> with c.push(foo="second level"):
...     c["foo"]
...
'second level'
>>> c["foo"]
'first level'
```

    Context.update(*other_dict*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/context/#Context.update)[¶](#django.template.Context.update)

In addition to `push()` and `pop()`, the `Context`
object also defines an `update()` method. This works like `push()`
but takes a dictionary as an argument and pushes that dictionary onto
the stack instead of an empty one.

```
>>> c = Context()
>>> c["foo"] = "first level"
>>> c.update({"foo": "updated"})
{'foo': 'updated'}
>>> c["foo"]
'updated'
>>> c.pop()
{'foo': 'updated'}
>>> c["foo"]
'first level'
```

Like `push()`, you can use `update()` as a context manager to ensure a
matching `pop()` is called.

```
>>> c = Context()
>>> c["foo"] = "first level"
>>> with c.update({"foo": "second level"}):
...     c["foo"]
...
'second level'
>>> c["foo"]
'first level'
```

Using a `Context` as a stack comes in handy in [some custom template
tags](https://docs.djangoproject.com/en/howto/custom-template-tags/#howto-writing-custom-template-tags).

   Context.flatten()[¶](#django.template.Context.flatten)

Using `flatten()` method you can get whole `Context` stack as one dictionary
including builtin variables.

```
>>> c = Context()
>>> c["foo"] = "first level"
>>> c.update({"bar": "second level"})
{'bar': 'second level'}
>>> c.flatten()
{'True': True, 'None': None, 'foo': 'first level', 'False': False, 'bar': 'second level'}
```

A `flatten()` method is also internally used to make `Context` objects comparable.

```
>>> c1 = Context()
>>> c1["foo"] = "first level"
>>> c1["bar"] = "second level"
>>> c2 = Context()
>>> c2.update({"bar": "second level", "foo": "first level"})
{'foo': 'first level', 'bar': 'second level'}
>>> c1 == c2
True
```

Result from `flatten()` can be useful in unit tests to compare `Context`
against `dict`:

```
class ContextTest(unittest.TestCase):
    def test_against_dictionary(self):
        c1 = Context()
        c1["update"] = "value"
        self.assertEqual(
            c1.flatten(),
            {
                "True": True,
                "None": None,
                "False": False,
                "update": "value",
            },
        )
```

### UsingRequestContext¶

   *class*RequestContext(*request*, *dict_=None*, *processors=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/context/#RequestContext)[¶](#django.template.RequestContext)

Django comes with a special `Context` class,
`django.template.RequestContext`, that acts slightly differently from the
normal `django.template.Context`. The first difference is that it takes an
[HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) as its first argument. For example:

```
c = RequestContext(
    request,
    {
        "foo": "bar",
    },
)
```

The second difference is that it automatically populates the context with a
few variables, according to the engine’s `context_processors` configuration
option.

The `context_processors` option is a list of callables – called **context
processors** – that take a request object as their argument and return a
dictionary of items to be merged into the context. In the default generated
settings file, the default template engine contains the following context
processors:

```
[
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
]
```

In addition to these, [RequestContext](#django.template.RequestContext) always enables
`'django.template.context_processors.csrf'`.  This is a security related
context processor required by the admin and other contrib apps, and, in case
of accidental misconfiguration, it is deliberately hardcoded in and cannot be
turned off in the `context_processors` option.

Each processor is applied in order. That means, if one processor adds a
variable to the context and a second processor adds a variable with the same
name, the second will override the first. The default processors are explained
below.

When context processors are applied

Context processors are applied on top of context data. This means that a
context processor may overwrite variables you’ve supplied to your
[Context](#django.template.Context) or [RequestContext](#django.template.RequestContext), so take care to avoid
variable names that overlap with those supplied by your context
processors.

If you want context data to take priority over context processors, use the
following pattern:

```
from django.template import RequestContext

request_context = RequestContext(request)
request_context.push({"my_name": "Adrian"})
```

Django does this to allow context data to override context processors in
APIs such as [render()](https://docs.djangoproject.com/en/topics/http/shortcuts/#django.shortcuts.render) and
[TemplateResponse](https://docs.djangoproject.com/en/5.0/template-response/#django.template.response.TemplateResponse).

Also, you can give [RequestContext](#django.template.RequestContext) a list of additional processors,
using the optional, third positional argument, `processors`. In this
example, the [RequestContext](#django.template.RequestContext) instance gets an `ip_address` variable:

```
from django.http import HttpResponse
from django.template import RequestContext, Template

def ip_address_processor(request):
    return {"ip_address": request.META["REMOTE_ADDR"]}

def client_ip_view(request):
    template = Template("{{ title }}: {{ ip_address }}")
    context = RequestContext(
        request,
        {
            "title": "Your IP Address",
        },
        [ip_address_processor],
    )
    return HttpResponse(template.render(context))
```

### Built-in template context processors¶

Here’s what each of the built-in processors does:

#### django.contrib.auth.context_processors.auth¶

   auth(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/context_processors/#auth)[¶](#django.contrib.auth.context_processors.auth)

If this processor is enabled, every `RequestContext` will contain these
variables:

- `user` – An `auth.User` instance representing the currently
  logged-in user (or an `AnonymousUser` instance, if the client isn’t
  logged in).
- `perms` – An instance of
  `django.contrib.auth.context_processors.PermWrapper`, representing the
  permissions that the currently logged-in user has.

#### django.template.context_processors.debug¶

   debug(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/context_processors/#debug)[¶](#django.template.context_processors.debug)

If this processor is enabled, every `RequestContext` will contain these two
variables – but only if your [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) setting is set to `True` and
the request’s IP address (`request.META['REMOTE_ADDR']`) is in the
[INTERNAL_IPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INTERNAL_IPS) setting:

- `debug` – `True`. You can use this in templates to test whether
  you’re in [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) mode.
- `sql_queries` – A list of `{'sql': ..., 'time': ...}` dictionaries,
  representing every SQL query that has happened so far during the request
  and how long it took. The list is in order by database alias and then by
  query. It’s lazily generated on access.

#### django.template.context_processors.i18n¶

   i18n(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/context_processors/#i18n)[¶](#django.template.context_processors.i18n)

If this processor is enabled, every `RequestContext` will contain these
variables:

- `LANGUAGES` – The value of the [LANGUAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-LANGUAGES) setting.
- `LANGUAGE_BIDI` – `True` if the current language is a right-to-left
  language, e.g. Hebrew, Arabic. `False` if it’s a left-to-right language,
  e.g. English, French, German.
- `LANGUAGE_CODE` – `request.LANGUAGE_CODE`, if it exists. Otherwise,
  the value of the [LANGUAGE_CODE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-LANGUAGE_CODE) setting.

See [i18n template tags](https://docs.djangoproject.com/en/topics/i18n/translation/#i18n-template-tags) for template tags that
generate the same values.

#### django.template.context_processors.media¶

If this processor is enabled, every `RequestContext` will contain a variable
`MEDIA_URL`, providing the value of the [MEDIA_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_URL) setting.

#### django.template.context_processors.static¶

   static(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/context_processors/#static)[¶](#django.template.context_processors.static)

If this processor is enabled, every `RequestContext` will contain a variable
`STATIC_URL`, providing the value of the [STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL) setting.

#### django.template.context_processors.csrf¶

This processor adds a token that is needed by the [csrf_token](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-csrf_token) template
tag for protection against [Cross Site Request Forgeries](https://docs.djangoproject.com/en/5.0/csrf/).

#### django.template.context_processors.request¶

If this processor is enabled, every `RequestContext` will contain a variable
`request`, which is the current [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest).

#### django.template.context_processors.tz¶

   tz(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/context_processors/#tz)[¶](#django.template.context_processors.tz)

If this processor is enabled, every `RequestContext` will contain a variable
`TIME_ZONE`, providing the name of the currently active time zone.

#### django.contrib.messages.context_processors.messages¶

If this processor is enabled, every `RequestContext` will contain these two
variables:

- `messages` – A list of messages (as strings) that have been set
  via the [messages framework](https://docs.djangoproject.com/en/5.0/contrib/messages/).
- `DEFAULT_MESSAGE_LEVELS` – A mapping of the message level names to
  [their numeric value](https://docs.djangoproject.com/en/5.0/contrib/messages/#message-level-constants).

### Writing your own context processors¶

A context processor has a simple interface: It’s a Python function that takes
one argument, an [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) object, and returns a
dictionary that gets added to the template context.

For example, to add the [DEFAULT_FROM_EMAIL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_FROM_EMAIL) setting to every
context:

```
from django.conf import settings

def from_email(request):
    return {
        "DEFAULT_FROM_EMAIL": settings.DEFAULT_FROM_EMAIL,
    }
```

Custom context processors can live anywhere in your code base. All Django
cares about is that your custom context processors are pointed to by the
`'context_processors'` option in your [TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES) setting — or the
`context_processors` argument of [Engine](#django.template.Engine) if you’re
using it directly.

## Loading templates¶

Generally, you’ll store templates in files on your filesystem rather than
using the low-level [Template](#django.template.Template) API yourself. Save
templates in a directory specified as a **template directory**.

Django searches for template directories in a number of places, depending on
your template loading settings (see “Loader types” below), but the most basic
way of specifying template directories is by using the [DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-DIRS) option.

### TheDIRSoption¶

Tell Django what your template directories are by using the [DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-DIRS) option in the [TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES) setting in your settings
file — or the `dirs` argument of [Engine](#django.template.Engine). This
should be set to a list of strings that contain full paths to your template
directories:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "/home/html/templates/lawrence.com",
            "/home/html/templates/default",
        ],
    },
]
```

Your templates can go anywhere you want, as long as the directories and
templates are readable by the web server. They can have any extension you want,
such as `.html` or `.txt`, or they can have no extension at all.

Note that these paths should use Unix-style forward slashes, even on Windows.

### Loader types¶

By default, Django uses a filesystem-based template loader, but Django comes
with a few other template loaders, which know how to load templates from other
sources.

Some of these other loaders are disabled by default, but you can activate them
by adding a `'loaders'` option to your `DjangoTemplates` backend in the
[TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES) setting or passing a `loaders` argument to
[Engine](#django.template.Engine). `loaders` should be a list of strings or
tuples, where each represents a template loader class. Here are the template
loaders that come with Django:

`django.template.loaders.filesystem.Loader`

   *class*filesystem.Loader[¶](#django.template.loaders.filesystem.Loader)

Loads templates from the filesystem, according to
[DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-DIRS).

This loader is enabled by default. However it won’t find any templates
until you set [DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-DIRS) to a non-empty list:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
    }
]
```

You can also override `'DIRS'` and specify specific directories for a
particular filesystem loader:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.filesystem.Loader",
                    [BASE_DIR / "templates"],
                ),
            ],
        },
    }
]
```

`django.template.loaders.app_directories.Loader`

   *class*app_directories.Loader[¶](#django.template.loaders.app_directories.Loader)

Loads templates from Django apps on the filesystem. For each app in
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS), the loader looks for a `templates`
subdirectory. If the directory exists, Django looks for templates in there.

This means you can store templates with your individual apps. This also
helps to distribute Django apps with default templates.

For example, for this setting:

```
INSTALLED_APPS = ["myproject.polls", "myproject.music"]
```

…then `get_template('foo.html')` will look for `foo.html` in these
directories, in this order:

- `/path/to/myproject/polls/templates/`
- `/path/to/myproject/music/templates/`

… and will use the one it finds first.

The order of [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) is significant! For example, if you
want to customize the Django admin, you might choose to override the
standard `admin/base_site.html` template, from `django.contrib.admin`,
with your own `admin/base_site.html` in `myproject.polls`. You must
then make sure that your `myproject.polls` comes *before* `django.contrib.admin` in [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS), otherwise
`django.contrib.admin`’s will be loaded first and yours will be ignored.

Note that the loader performs an optimization when it first runs:
it caches a list of which [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) packages have a
`templates` subdirectory.

You can enable this loader by setting [APP_DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-APP_DIRS) to `True`:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]
```

`django.template.loaders.cached.Loader`

   *class*cached.Loader[¶](#django.template.loaders.cached.Loader)

While the Django template system is quite fast, if it needs to read and
compile your templates every time they’re rendered, the overhead from that
can add up.

You configure the cached template loader with a list of other loaders that
it should wrap. The wrapped loaders are used to locate unknown templates
when they’re first encountered. The cached loader then stores the compiled
`Template` in memory. The cached `Template` instance is returned for
subsequent requests to load the same template.

This loader is automatically enabled if [OPTIONS['loaders']](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-OPTIONS) isn’t specified.

You can manually specify template caching with some custom template loaders
using settings like this:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                        "path.to.custom.Loader",
                    ],
                ),
            ],
        },
    }
]
```

Note

All of the built-in Django template tags are safe to use with the
cached loader, but if you’re using custom template tags that come from
third party packages, or that you wrote yourself, you should ensure
that the `Node` implementation for each tag is thread-safe. For more
information, see [template tag thread safety considerations](https://docs.djangoproject.com/en/howto/custom-template-tags/#template-tag-thread-safety).

`django.template.loaders.locmem.Loader`

   *class*locmem.Loader[¶](#django.template.loaders.locmem.Loader)

Loads templates from a Python dictionary. This is useful for testing.

This loader takes a dictionary of templates as its first argument:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        "index.html": "content here",
                    },
                ),
            ],
        },
    }
]
```

This loader is disabled by default.

Django uses the template loaders in order according to the `'loaders'`
option. It uses each loader until a loader finds a match.

## Custom loaders¶

It’s possible to load templates from additional sources using custom template
loaders. Custom `Loader` classes should inherit from
`django.template.loaders.base.Loader` and define the `get_contents()` and
`get_template_sources()` methods.

### Loader methods¶

   *class*Loader[[source]](https://docs.djangoproject.com/en/_modules/django/template/loaders/base/#Loader)[¶](#django.template.loaders.base.Loader)

Loads templates from a given source, such as the filesystem or a database.

   get_template_sources(*template_name*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/loaders/base/#Loader.get_template_sources)[¶](#django.template.loaders.base.Loader.get_template_sources)

A method that takes a `template_name` and yields
[Origin](#django.template.base.Origin) instances for each possible
source.

For example, the filesystem loader may receive `'index.html'` as a
`template_name` argument.  This method would yield origins for the
full path of `index.html` as it appears in each template directory
the loader looks at.

The method doesn’t need to verify that the template exists at a given
path, but it should ensure the path is valid. For instance, the
filesystem loader makes sure the path lies under a valid template
directory.

    get_contents(*origin*)[¶](#django.template.loaders.base.Loader.get_contents)

Returns the contents for a template given a
[Origin](#django.template.base.Origin) instance.

This is where a filesystem loader would read contents from the
filesystem, or a database loader would read from the database. If a
matching template doesn’t exist, this should raise a
[TemplateDoesNotExist](https://docs.djangoproject.com/en/topics/templates/#django.template.TemplateDoesNotExist) error.

    get_template(*template_name*, *skip=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/loaders/base/#Loader.get_template)[¶](#django.template.loaders.base.Loader.get_template)

Returns a `Template` object for a given `template_name` by looping
through results from [get_template_sources()](#django.template.loaders.base.Loader.get_template_sources) and calling
[get_contents()](#django.template.loaders.base.Loader.get_contents). This returns the first matching template. If no
template is found, [TemplateDoesNotExist](https://docs.djangoproject.com/en/topics/templates/#django.template.TemplateDoesNotExist) is
raised.

The optional `skip` argument is a list of origins to ignore when
extending templates. This allow templates to extend other templates of
the same name. It also used to avoid recursion errors.

In general, it is enough to define [get_template_sources()](#django.template.loaders.base.Loader.get_template_sources) and
[get_contents()](#django.template.loaders.base.Loader.get_contents) for custom template loaders. `get_template()`
will usually not need to be overridden.

Building your own

For examples, read the [source code for Django’s built-in loaders](https://github.com/django/django/blob/main/django/template/loaders).

## Template origin¶

Templates have an `origin` containing attributes depending on the source
they are loaded from.

   *class*Origin(*name*, *template_name=None*, *loader=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/template/base/#Origin)[¶](#django.template.base.Origin)   name[¶](#django.template.base.Origin.name)

The path to the template as returned by the template loader.
For loaders that read from the file system, this is the full
path to the template.

If the template is instantiated directly rather than through a
template loader, this is a string value of `<unknown_source>`.

    template_name[¶](#django.template.base.Origin.template_name)

The relative path to the template as passed into the
template loader.

If the template is instantiated directly rather than through a
template loader, this is `None`.

    loader[¶](#django.template.base.Origin.loader)

The template loader instance that constructed this `Origin`.

If the template is instantiated directly rather than through a
template loader, this is `None`.

[django.template.loaders.cached.Loader](#django.template.loaders.cached.Loader) requires all of its
wrapped loaders to set this attribute, typically by instantiating
the `Origin` with `loader=self`.
