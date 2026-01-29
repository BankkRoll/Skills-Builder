# System check framework¶ and more

# System check framework¶

# System check framework¶

The system check framework is a set of static checks for validating Django
projects. It detects common problems and provides hints for how to fix them.
The framework is extensible so you can easily add your own checks.

Checks can be triggered explicitly via the [check](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-check) command. Checks are
triggered implicitly before most commands, including [runserver](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-runserver) and
[migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate). For performance reasons, checks are not run as part of the
WSGI stack that is used in deployment. If you need to run system checks on your
deployment server, trigger them explicitly using [check](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-check).

Serious errors will prevent Django commands (such as [runserver](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-runserver)) from
running at all. Minor problems are reported to the console. If you have inspected
the cause of a warning and are happy to ignore it, you can hide specific warnings
using the [SILENCED_SYSTEM_CHECKS](https://docs.djangoproject.com/en/ref/settings/#std-setting-SILENCED_SYSTEM_CHECKS) setting in your project settings file.

A full list of all checks that can be raised by Django can be found in the
[System check reference](https://docs.djangoproject.com/en/ref/checks/).

## Writing your own checks¶

The framework is flexible and allows you to write functions that perform
any other kind of check you may require. The following is an example stub
check function:

```
from django.core.checks import Error, register

@register()
def example_check(app_configs, **kwargs):
    errors = []
    # ... your check logic here
    if check_failed:
        errors.append(
            Error(
                "an error",
                hint="A hint.",
                obj=checked_object,
                id="myapp.E001",
            )
        )
    return errors
```

The check function *must* accept an `app_configs` argument; this argument is
the list of applications that should be inspected. If `None`, the check must
be run on *all* installed apps in the project.

The check will receive a `databases` keyword argument. This is a list of
database aliases whose connections may be used to inspect database level
configuration. If `databases` is `None`, the check must not use any
database connections.

The `**kwargs` argument is required for future expansion.

### Messages¶

The function must return a list of messages. If no problems are found as a result
of the check, the check function must return an empty list.

The warnings and errors raised by the check method must be instances of
[CheckMessage](https://docs.djangoproject.com/en/ref/checks/#django.core.checks.CheckMessage). An instance of
[CheckMessage](https://docs.djangoproject.com/en/ref/checks/#django.core.checks.CheckMessage) encapsulates a single reportable
error or warning. It also provides context and hints applicable to the
message, and a unique identifier that is used for filtering purposes.

The concept is very similar to messages from the [message framework](https://docs.djangoproject.com/en/ref/contrib/messages/) or the [logging framework](https://docs.djangoproject.com/en/5.0/logging/).
Messages are tagged with a `level` indicating the severity of the message.

There are also shortcuts to make creating messages with common levels easier.
When using these classes you can omit the `level` argument because it is
implied by the class name.

- [Debug](https://docs.djangoproject.com/en/ref/checks/#django.core.checks.Debug)
- [Info](https://docs.djangoproject.com/en/ref/checks/#django.core.checks.Info)
- [Warning](https://docs.djangoproject.com/en/ref/checks/#django.core.checks.Warning)
- [Error](https://docs.djangoproject.com/en/ref/checks/#django.core.checks.Error)
- [Critical](https://docs.djangoproject.com/en/ref/checks/#django.core.checks.Critical)

### Registering and labeling checks¶

Lastly, your check function must be registered explicitly with system check
registry. Checks should be registered in a file that’s loaded when your
application is loaded; for example, in the [AppConfig.ready()](https://docs.djangoproject.com/en/ref/applications/#django.apps.AppConfig.ready) method.

   register(**tags)(function*)[¶](#django.core.checks.register)

You can pass as many tags to `register` as you want in order to label your
check. Tagging checks is useful since it allows you to run only a certain
group of checks. For example, to register a compatibility check, you would
make the following call:

```
from django.core.checks import register, Tags

@register(Tags.compatibility)
def my_check(app_configs, **kwargs):
    # ... perform compatibility checks and collect errors
    return errors
```

You can register “deployment checks” that are only relevant to a production
settings file like this:

```
@register(Tags.security, deploy=True)
def my_check(app_configs, **kwargs): ...
```

These checks will only be run if the [check--deploy](https://docs.djangoproject.com/en/ref/django-admin/#cmdoption-check-deploy) option is used.

You can also use `register` as a function rather than a decorator by
passing a callable object (usually a function) as the first argument
to `register`.

The code below is equivalent to the code above:

```
def my_check(app_configs, **kwargs): ...

register(my_check, Tags.security, deploy=True)
```

### Field, model, manager, and database checks¶

In some cases, you won’t need to register your check function – you can
piggyback on an existing registration.

Fields, models, model managers, and database backends all implement a
`check()` method that is already registered with the check framework. If you
want to add extra checks, you can extend the implementation on the base class,
perform any extra checks you need, and append any messages to those generated
by the base class. It’s recommended that you delegate each check to separate
methods.

Consider an example where you are implementing a custom field named
`RangedIntegerField`. This field adds `min` and `max` arguments to the
constructor of `IntegerField`. You may want to add a check to ensure that users
provide a min value that is less than or equal to the max value. The following
code snippet shows how you can implement this check:

```
from django.core import checks
from django.db import models

class RangedIntegerField(models.IntegerField):
    def __init__(self, min=None, max=None, **kwargs):
        super().__init__(**kwargs)
        self.min = min
        self.max = max

    def check(self, **kwargs):
        # Call the superclass
        errors = super().check(**kwargs)

        # Do some custom checks and add messages to `errors`:
        errors.extend(self._check_min_max_values(**kwargs))

        # Return all errors and warnings
        return errors

    def _check_min_max_values(self, **kwargs):
        if self.min is not None and self.max is not None and self.min > self.max:
            return [
                checks.Error(
                    "min greater than max.",
                    hint="Decrease min or increase max.",
                    obj=self,
                    id="myapp.E001",
                )
            ]
        # When no error, return an empty list
        return []
```

If you wanted to add checks to a model manager, you would take the same
approach on your subclass of [Manager](https://docs.djangoproject.com/en/5.0/db/managers/#django.db.models.Manager).

If you want to add a check to a model class, the approach is *almost* the same:
the only difference is that the check is a classmethod, not an instance method:

```
class MyModel(models.Model):
    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        # ... your own checks ...
        return errors
```

### Writing tests¶

Messages are comparable. That allows you to easily write tests:

```
from django.core.checks import Error

errors = checked_object.check()
expected_errors = [
    Error(
        "an error",
        hint="A hint.",
        obj=checked_object,
        id="myapp.E001",
    )
]
self.assertEqual(errors, expected_errors)
```

#### Writing integration tests¶

Given the need to register certain checks when the application loads, it can be
useful to test their integration within the system checks framework. This can
be accomplished by using the [call_command()](https://docs.djangoproject.com/en/ref/django-admin/#django.core.management.call_command)
function.

For example, this test demonstrates that the [SITE_ID](https://docs.djangoproject.com/en/ref/settings/#std-setting-SITE_ID) setting must be
an integer, a built-in [check from the sites framework](https://docs.djangoproject.com/en/ref/checks/#sites-system-checks):

```
from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django.test import SimpleTestCase, modify_settings, override_settings

class SystemCheckIntegrationTest(SimpleTestCase):
    @override_settings(SITE_ID="non_integer")
    @modify_settings(INSTALLED_APPS={"prepend": "django.contrib.sites"})
    def test_non_integer_site_id(self):
        message = "(sites.E101) The SITE_ID setting must be an integer."
        with self.assertRaisesMessage(SystemCheckError, message):
            call_command("check")
```

Consider the following check which issues a warning on deployment if a custom
setting named `ENABLE_ANALYTICS` is not set to `True`:

```
from django.conf import settings
from django.core.checks import Warning, register

@register("myapp", deploy=True)
def check_enable_analytics_is_true_on_deploy(app_configs, **kwargs):
    errors = []
    if getattr(settings, "ENABLE_ANALYTICS", None) is not True:
        errors.append(
            Warning(
                "The ENABLE_ANALYTICS setting should be set to True in deployment.",
                id="myapp.W001",
            )
        )
    return errors
```

Given that this check will not raise a `SystemCheckError`, the presence of
the warning message in the `stderr` output can be asserted like so:

```
from io import StringIO

from django.core.management import call_command
from django.test import SimpleTestCase, override_settings

class EnableAnalyticsDeploymentCheckTest(SimpleTestCase):
    @override_settings(ENABLE_ANALYTICS=None)
    def test_when_set_to_none(self):
        stderr = StringIO()
        call_command("check", "-t", "myapp", "--deploy", stderr=stderr)
        message = (
            "(myapp.W001) The ENABLE_ANALYTICS setting should be set "
            "to True in deployment."
        )
        self.assertIn(message, stderr.getvalue())
```

---

# Built

# Built-in class-based generic views¶

Writing web applications can be monotonous, because we repeat certain patterns
again and again. Django tries to take away some of that monotony at the model
and template layers, but web developers also experience this boredom at the view
level.

Django’s *generic views* were developed to ease that pain. They take certain
common idioms and patterns found in view development and abstract them so that
you can quickly write common views of data without having to write too much
code.

We can recognize certain common tasks, like displaying a list of objects, and
write code that displays a list of *any* object. Then the model in question can
be passed as an extra argument to the URLconf.

Django ships with generic views to do the following:

- Display list and detail pages for a single object. If we were creating an
  application to manage conferences then a `TalkListView` and a
  `RegisteredUserListView` would be examples of list views. A single
  talk page is an example of what we call a “detail” view.
- Present date-based objects in year/month/day archive pages,
  associated detail, and “latest” pages.
- Allow users to create, update, and delete objects – with or
  without authorization.

Taken together, these views provide interfaces to perform the most common tasks
developers encounter.

## Extending generic views¶

There’s no question that using generic views can speed up development
substantially. In most projects, however, there comes a moment when the
generic views no longer suffice. Indeed, the most common question asked by new
Django developers is how to make generic views handle a wider array of
situations.

This is one of the reasons generic views were redesigned for the 1.3 release -
previously, they were view functions with a bewildering array of options; now,
rather than passing in a large amount of configuration in the URLconf, the
recommended way to extend generic views is to subclass them, and override their
attributes or methods.

That said, generic views will have a limit. If you find you’re struggling to
implement your view as a subclass of a generic view, then you may find it more
effective to write just the code you need, using your own class-based or
functional views.

More examples of generic views are available in some third party applications,
or you could write your own as needed.

## Generic views of objects¶

[TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.TemplateView) certainly is useful, but
Django’s generic views really shine when it comes to presenting views of your
database content. Because it’s such a common task, Django comes with a handful
of built-in generic views to help generate list and detail views of objects.

Let’s start by looking at some examples of showing a list of objects or an
individual object.

We’ll be using these models:

```
# models.py
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to="author_headshots")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField("Author")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
```

Now we need to define a view:

```
# views.py
from django.views.generic import ListView
from books.models import Publisher

class PublisherListView(ListView):
    model = Publisher
```

Finally hook that view into your urls:

```
# urls.py
from django.urls import path
from books.views import PublisherListView

urlpatterns = [
    path("publishers/", PublisherListView.as_view()),
]
```

That’s all the Python code we need to write. We still need to write a template,
however. We could explicitly tell the view which template to use by adding a
`template_name` attribute to the view, but in the absence of an explicit
template Django will infer one from the object’s name. In this case, the
inferred template will be `"books/publisher_list.html"` – the “books” part
comes from the name of the app that defines the model, while the “publisher”
bit is the lowercased version of the model’s name.

Note

Thus, when (for example) the `APP_DIRS` option of a `DjangoTemplates`
backend is set to True in [TEMPLATES](https://docs.djangoproject.com/en/ref/settings/#std-setting-TEMPLATES), a template location could
be: /path/to/project/books/templates/books/publisher_list.html

This template will be rendered against a context containing a variable called
`object_list` that contains all the publisher objects. A template might look
like this:

```
{% extends "base.html" %}

{% block content %}
    <h2>Publishers</h2>
    <ul>
        {% for publisher in object_list %}
            <li>{{ publisher.name }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```

That’s really all there is to it. All the cool features of generic views come
from changing the attributes set on the generic view. The
[generic views reference](https://docs.djangoproject.com/en/ref/class-based-views/) documents all the
generic views and their options in detail; the rest of this document will
consider some of the common ways you might customize and extend generic views.

### Making “friendly” template contexts¶

You might have noticed that our sample publisher list template stores all the
publishers in a variable named `object_list`. While this works just fine, it
isn’t all that “friendly” to template authors: they have to “just know” that
they’re dealing with publishers here.

Well, if you’re dealing with a model object, this is already done for you. When
you are dealing with an object or queryset, Django is able to populate the
context using the lowercased version of the model class’ name. This is provided
in addition to the default `object_list` entry, but contains exactly the same
data, i.e. `publisher_list`.

If this still isn’t a good match, you can manually set the name of the
context variable. The `context_object_name` attribute on a generic view
specifies the context variable to use:

```
# views.py
from django.views.generic import ListView
from books.models import Publisher

class PublisherListView(ListView):
    model = Publisher
    context_object_name = "my_favorite_publishers"
```

Providing a useful `context_object_name` is always a good idea. Your
coworkers who design templates will thank you.

### Adding extra context¶

Often you need to present some extra information beyond that provided by the
generic view. For example, think of showing a list of all the books on each
publisher detail page. The [DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView)
generic view provides the publisher to the context, but how do we get
additional information in that template?

The answer is to subclass [DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView)
and provide your own implementation of the `get_context_data` method.
The default implementation adds the object being displayed to the template, but
you can override it to send more:

```
from django.views.generic import DetailView
from books.models import Book, Publisher

class PublisherDetailView(DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["book_list"] = Book.objects.all()
        return context
```

Note

Generally, `get_context_data` will merge the context data of all parent
classes with those of the current class. To preserve this behavior in your
own classes where you want to alter the context, you should be sure to call
`get_context_data` on the super class. When no two classes try to define the
same key, this will give the expected results. However if any class
attempts to override a key after parent classes have set it (after the call
to super), any children of that class will also need to explicitly set it
after super if they want to be sure to override all parents. If you’re
having trouble, review the method resolution order of your view.

Another consideration is that the context data from class-based generic
views will override data provided by context processors; see
[get_context_data()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data) for
an example.

### Viewing subsets of objects¶

Now let’s take a closer look at the `model` argument we’ve been
using all along. The `model` argument, which specifies the database
model that the view will operate upon, is available on all the
generic views that operate on a single object or a collection of
objects. However, the `model` argument is not the only way to
specify the objects that the view will operate upon – you can also
specify the list of objects using the `queryset` argument:

```
from django.views.generic import DetailView
from books.models import Publisher

class PublisherDetailView(DetailView):
    context_object_name = "publisher"
    queryset = Publisher.objects.all()
```

Specifying `model = Publisher` is shorthand for saying `queryset =
Publisher.objects.all()`. However, by using `queryset` to define a filtered
list of objects you can be more specific about the objects that will be visible
in the view (see [Making queries](https://docs.djangoproject.com/en/5.0/db/queries/) for more information about
[QuerySet](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet) objects, and see the
[class-based views reference](https://docs.djangoproject.com/en/ref/class-based-views/) for the
complete details).

To pick an example, we might want to order a list of books by publication date,
with the most recent first:

```
from django.views.generic import ListView
from books.models import Book

class BookListView(ListView):
    queryset = Book.objects.order_by("-publication_date")
    context_object_name = "book_list"
```

That’s a pretty minimal example, but it illustrates the idea nicely. You’ll
usually want to do more than just reorder objects. If you want to present a
list of books by a particular publisher, you can use the same technique:

```
from django.views.generic import ListView
from books.models import Book

class AcmeBookListView(ListView):
    context_object_name = "book_list"
    queryset = Book.objects.filter(publisher__name="ACME Publishing")
    template_name = "books/acme_list.html"
```

Notice that along with a filtered `queryset`, we’re also using a custom
template name. If we didn’t, the generic view would use the same template as the
“vanilla” object list, which might not be what we want.

Also notice that this isn’t a very elegant way of doing publisher-specific
books. If we want to add another publisher page, we’d need another handful of
lines in the URLconf, and more than a few publishers would get unreasonable.
We’ll deal with this problem in the next section.

Note

If you get a 404 when requesting `/books/acme/`, check to ensure you
actually have a Publisher with the name ‘ACME Publishing’.  Generic
views have an `allow_empty` parameter for this case.  See the
[class-based-views reference](https://docs.djangoproject.com/en/ref/class-based-views/) for more
details.

### Dynamic filtering¶

Another common need is to filter down the objects given in a list page by some
key in the URL. Earlier we hard-coded the publisher’s name in the URLconf, but
what if we wanted to write a view that displayed all the books by some arbitrary
publisher?

Handily, the `ListView` has a
[get_queryset()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset) method we
can override. By default, it returns the value of the `queryset` attribute,
but we can use it to add more logic.

The key part to making this work is that when class-based views are called,
various useful things are stored on `self`; as well as the request
(`self.request`) this includes the positional (`self.args`) and name-based
(`self.kwargs`) arguments captured according to the URLconf.

Here, we have a URLconf with a single captured group:

```
# urls.py
from django.urls import path
from books.views import PublisherBookListView

urlpatterns = [
    path("books/<publisher>/", PublisherBookListView.as_view()),
]
```

Next, we’ll write the `PublisherBookListView` view itself:

```
# views.py
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from books.models import Book, Publisher

class PublisherBookListView(ListView):
    template_name = "books/books_by_publisher.html"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs["publisher"])
        return Book.objects.filter(publisher=self.publisher)
```

Using `get_queryset` to add logic to the queryset selection is as convenient
as it is powerful. For instance, if we wanted, we could use
`self.request.user` to filter using the current user, or other more complex
logic.

We can also add the publisher into the context at the same time, so we can
use it in the template:

```
# ...

def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in the publisher
    context["publisher"] = self.publisher
    return context
```

### Performing extra work¶

The last common pattern we’ll look at involves doing some extra work before
or after calling the generic view.

Imagine we had a `last_accessed` field on our `Author` model that we were
using to keep track of the last time anybody looked at that author:

```
# models.py
from django.db import models

class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to="author_headshots")
    last_accessed = models.DateTimeField()
```

The generic `DetailView` class wouldn’t know anything about this field, but
once again we could write a custom view to keep that field updated.

First, we’d need to add an author detail bit in the URLconf to point to a
custom view:

```
from django.urls import path
from books.views import AuthorDetailView

urlpatterns = [
    # ...
    path("authors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
]
```

Then we’d write our new view – `get_object` is the method that retrieves the
object – so we override it and wrap the call:

```
from django.utils import timezone
from django.views.generic import DetailView
from books.models import Author

class AuthorDetailView(DetailView):
    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj
```

Note

The URLconf here uses the named group `pk` - this name is the default
name that `DetailView` uses to find the value of the primary key used to
filter the queryset.

If you want to call the group something else, you can set
[pk_url_kwarg](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.pk_url_kwarg)
on the view.

---

# Form handling with class

# Form handling with class-based views¶

Form processing generally has 3 paths:

- Initial GET (blank or prepopulated form)
- POST with invalid data (typically redisplay form with errors)
- POST with valid data (process the data and typically redirect)

Implementing this yourself often results in a lot of repeated boilerplate code
(see [Using a form in a view](https://docs.djangoproject.com/en/5.0/forms/#using-a-form-in-a-view)). To help avoid
this, Django provides a collection of generic class-based views for form
processing.

## Basic forms¶

Given a contact form:

  `forms.py`[¶](#id2)

```
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
```

The view can be constructed using a `FormView`:

  `views.py`[¶](#id3)

```
from myapp.forms import ContactForm
from django.views.generic.edit import FormView

class ContactFormView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
```

Notes:

- FormView inherits
  [TemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin) so
  [template_name](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name)
  can be used here.
- The default implementation for
  [form_valid()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_valid) simply
  redirects to the [success_url](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.success_url).

## Model forms¶

Generic views really shine when working with models.  These generic
views will automatically create a [ModelForm](https://docs.djangoproject.com/en/5.0/forms/modelforms/#django.forms.ModelForm), so long as
they can work out which model class to use:

- If the [model](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.model) attribute is
  given, that model class will be used.
- If [get_object()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object)
  returns an object, the class of that object will be used.
- If a [queryset](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.queryset) is
  given, the model for that queryset will be used.

Model form views provide a
[form_valid()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid) implementation
that saves the model automatically.  You can override this if you have any
special requirements; see below for examples.

You don’t even need to provide a `success_url` for
[CreateView](https://docs.djangoproject.com/en/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView) or
[UpdateView](https://docs.djangoproject.com/en/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView) - they will use
[get_absolute_url()](https://docs.djangoproject.com/en/ref/models/instances/#django.db.models.Model.get_absolute_url) on the model object if available.

If you want to use a custom [ModelForm](https://docs.djangoproject.com/en/5.0/forms/modelforms/#django.forms.ModelForm) (for instance to
add extra validation), set
[form_class](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_class) on your view.

Note

When specifying a custom form class, you must still specify the model,
even though the [form_class](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_class) may
be a [ModelForm](https://docs.djangoproject.com/en/5.0/forms/modelforms/#django.forms.ModelForm).

First we need to add [get_absolute_url()](https://docs.djangoproject.com/en/ref/models/instances/#django.db.models.Model.get_absolute_url) to our
`Author` class:

  `models.py`[¶](#id4)

```
from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})
```

Then we can use [CreateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#CreateView) and friends to do the actual
work. Notice how we’re just configuring the generic class-based views
here; we don’t have to write any logic ourselves:

  `views.py`[¶](#id5)

```
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from myapp.models import Author

class AuthorCreateView(CreateView):
    model = Author
    fields = ["name"]

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ["name"]

class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy("author-list")
```

Note

We have to use [reverse_lazy()](https://docs.djangoproject.com/en/ref/urlresolvers/#django.urls.reverse_lazy) instead of
`reverse()`, as the urls are not loaded when the file is imported.

The `fields` attribute works the same way as the `fields` attribute on the
inner `Meta` class on [ModelForm](https://docs.djangoproject.com/en/5.0/forms/modelforms/#django.forms.ModelForm). Unless you define the
form class in another way, the attribute is required and the view will raise
an [ImproperlyConfigured](https://docs.djangoproject.com/en/ref/exceptions/#django.core.exceptions.ImproperlyConfigured) exception if it’s not.

If you specify both the [fields](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.fields)
and [form_class](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_class) attributes, an
[ImproperlyConfigured](https://docs.djangoproject.com/en/ref/exceptions/#django.core.exceptions.ImproperlyConfigured) exception will be raised.

Finally, we hook these new views into the URLconf:

  `urls.py`[¶](#id6)

```
from django.urls import path
from myapp.views import AuthorCreateView, AuthorDeleteView, AuthorUpdateView

urlpatterns = [
    # ...
    path("author/add/", AuthorCreateView.as_view(), name="author-add"),
    path("author/<int:pk>/", AuthorUpdateView.as_view(), name="author-update"),
    path("author/<int:pk>/delete/", AuthorDeleteView.as_view(), name="author-delete"),
]
```

Note

These views inherit
[SingleObjectTemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin)
which uses
[template_name_suffix](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_suffix)
to construct the
[template_name](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name)
based on the model.

In this example:

- [CreateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#CreateView) and [UpdateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#UpdateView) use `myapp/author_form.html`
- [DeleteView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DeleteView) uses `myapp/author_confirm_delete.html`

If you wish to have separate templates for [CreateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#CreateView) and
[UpdateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#UpdateView), you can set either
[template_name](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) or
[template_name_suffix](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_suffix)
on your view class.

## Models andrequest.user¶

To track the user that created an object using a [CreateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#CreateView),
you can use a custom [ModelForm](https://docs.djangoproject.com/en/5.0/forms/modelforms/#django.forms.ModelForm) to do this. First, add
the foreign key relation to the model:

  `models.py`[¶](#id7)

```
from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # ...
```

In the view, ensure that you don’t include `created_by` in the list of fields
to edit, and override
[form_valid()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid) to add the user:

  `views.py`[¶](#id8)

```
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from myapp.models import Author

class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = ["name"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
```

[LoginRequiredMixin](https://docs.djangoproject.com/en/5.0/auth/default/#django.contrib.auth.mixins.LoginRequiredMixin) prevents users who
aren’t logged in from accessing the form. If you omit that, you’ll need to
handle unauthorized users in [form_valid()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid).

## Content negotiation example¶

Here is an example showing how you might go about implementing a form that
works with an API-based workflow as well as ‘normal’ form POSTs:

```
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from myapp.models import Author

class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts("text/html"):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts("text/html"):
            return response
        else:
            data = {
                "pk": self.object.pk,
            }
            return JsonResponse(data)

class AuthorCreateView(JsonableResponseMixin, CreateView):
    model = Author
    fields = ["name"]
```
