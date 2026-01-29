# Using mixins with class and more

# Using mixins with class

# Using mixins with class-based views¶

Caution

This is an advanced topic. A working knowledge of [Django’s
class-based views](https://docs.djangoproject.com/en/5.0/topics/) is advised before exploring these
techniques.

Django’s built-in class-based views provide a lot of functionality,
but some of it you may want to use separately. For instance, you may
want to write a view that renders a template to make the HTTP
response, but you can’t use
[TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.TemplateView); perhaps you need to
render a template only on `POST`, with `GET` doing something else
entirely. While you could use
[TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse) directly, this
will likely result in duplicate code.

For this reason, Django also provides a number of mixins that provide
more discrete functionality. Template rendering, for instance, is
encapsulated in the
[TemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin). The Django
reference documentation contains [full documentation of all the
mixins](https://docs.djangoproject.com/en/ref/class-based-views/mixins/).

## Context and template responses¶

Two central mixins are provided that help in providing a consistent
interface to working with templates in class-based views.

  [TemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin)

Every built in view which returns a
[TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse) will call the
[render_to_response()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
method that `TemplateResponseMixin` provides. Most of the time this
will be called for you (for instance, it is called by the `get()` method
implemented by both [TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.TemplateView) and
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView)); similarly, it’s unlikely
that you’ll need to override it, although if you want your response to
return something not rendered via a Django template then you’ll want to do
it. For an example of this, see the [JSONResponseMixin example](#jsonresponsemixin-example).

`render_to_response()` itself calls
[get_template_names()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names),
which by default will look up
[template_name](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.template_name) on
the class-based view; two other mixins
([SingleObjectTemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin)
and
[MultipleObjectTemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin))
override this to provide more flexible defaults when dealing with actual
objects.

  [ContextMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin)

Every built in view which needs context data, such as for rendering a
template (including `TemplateResponseMixin` above), should call
[get_context_data()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin.get_context_data) passing
any data they want to ensure is in there as keyword arguments.
`get_context_data()` returns a dictionary; in `ContextMixin` it
returns its keyword arguments, but it is common to override this to add
more members to the dictionary. You can also use the
[extra_context](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin.extra_context) attribute.

## Building up Django’s generic class-based views¶

Let’s look at how two of Django’s generic class-based views are built
out of mixins providing discrete functionality. We’ll consider
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView), which renders a
“detail” view of an object, and
[ListView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.list.ListView), which will render a list
of objects, typically from a queryset, and optionally paginate
them. This will introduce us to four mixins which between them provide
useful functionality when working with either a single Django object,
or multiple objects.

There are also mixins involved in the generic edit views
([FormView](https://docs.djangoproject.com/en/ref/class-based-views/generic-editing/#django.views.generic.edit.FormView), and the model-specific
views [CreateView](https://docs.djangoproject.com/en/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView),
[UpdateView](https://docs.djangoproject.com/en/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView) and
[DeleteView](https://docs.djangoproject.com/en/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView)), and in the
date-based generic views. These are
covered in the [mixin reference
documentation](https://docs.djangoproject.com/en/ref/class-based-views/mixins/).

### DetailView: working with a single Django object¶

To show the detail of an object, we basically need to do two things:
we need to look up the object and then we need to make a
[TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse) with a suitable template,
and that object as context.

To get the object, [DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView)
relies on [SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin),
which provides a
[get_object()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object)
method that figures out the object based on the URL of the request (it
looks for `pk` and `slug` keyword arguments as declared in the
URLConf, and looks the object up either from the
[model](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.model) attribute
on the view, or the
[queryset](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.queryset)
attribute if that’s provided). `SingleObjectMixin` also overrides
[get_context_data()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin.get_context_data),
which is used across all Django’s built in class-based views to supply
context data for template renders.

To then make a [TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse),
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DetailView) uses
[SingleObjectTemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin),
which extends [TemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin),
overriding
[get_template_names()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.get_template_names)
as discussed above. It actually provides a fairly sophisticated set of options,
but the main one that most people are going to use is
`<app_label>/<model_name>_detail.html`. The `_detail` part can be changed
by setting
[template_name_suffix](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin.template_name_suffix)
on a subclass to something else. (For instance, the [generic edit
views](https://docs.djangoproject.com/en/5.0/topics/generic-editing/) use `_form` for create and update views, and
`_confirm_delete` for delete views.)

### ListView: working with many Django objects¶

Lists of objects follow roughly the same pattern: we need a (possibly
paginated) list of objects, typically a
[QuerySet](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet), and then we need to make a
[TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse) with a suitable template
using that list of objects.

To get the objects, [ListView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.list.ListView) uses
[MultipleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin), which
provides both
[get_queryset()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)
and
[paginate_queryset()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_queryset). Unlike
with [SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin), there’s no need
to key off parts of the URL to figure out the queryset to work with, so the
default uses the
[queryset](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.queryset) or
[model](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model) attribute
on the view class. A common reason to override
[get_queryset()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.get_queryset)
here would be to dynamically vary the objects, such as depending on
the current user or to exclude posts in the future for a blog.

[MultipleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin) also overrides
[get_context_data()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin.get_context_data) to
include appropriate context variables for pagination (providing
dummies if pagination is disabled). It relies on `object_list` being
passed in as a keyword argument, which [ListView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#ListView) arranges for
it.

To make a [TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse),
[ListView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#ListView) then uses
[MultipleObjectTemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin);
as with [SingleObjectTemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin)
above, this overrides `get_template_names()` to provide [arangeofoptions](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin),
with the most commonly-used being
`<app_label>/<model_name>_list.html`, with the `_list` part again
being taken from the
[template_name_suffix](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin.template_name_suffix)
attribute. (The date based generic views use suffixes such as `_archive`,
`_archive_year` and so on to use different templates for the various
specialized date-based list views.)

## Using Django’s class-based view mixins¶

Now we’ve seen how Django’s generic class-based views use the provided mixins,
let’s look at other ways we can combine them. We’re still going to be combining
them with either built-in class-based views, or other generic class-based
views, but there are a range of rarer problems you can solve than are provided
for by Django out of the box.

Warning

Not all mixins can be used together, and not all generic class
based views can be used with all other mixins. Here we present a
few examples that do work; if you want to bring together other
functionality then you’ll have to consider interactions between
attributes and methods that overlap between the different classes
you’re using, and how [method resolution order](https://www.python.org/download/releases/2.3/mro/) will affect which
versions of the methods will be called in what order.

The reference documentation for Django’s [class-based
views](https://docs.djangoproject.com/en/ref/class-based-views/) and [class-based view
mixins](https://docs.djangoproject.com/en/ref/class-based-views/mixins/) will help you in
understanding which attributes and methods are likely to cause
conflict between different classes and mixins.

If in doubt, it’s often better to back off and base your work on
[View](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#View) or [TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#TemplateView), perhaps with
[SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin) and
[MultipleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin). Although you
will probably end up writing more code, it is more likely to be clearly
understandable to someone else coming to it later, and with fewer
interactions to worry about you will save yourself some thinking. (Of
course, you can always dip into Django’s implementation of the generic
class-based views for inspiration on how to tackle problems.)

### UsingSingleObjectMixinwith View¶

If we want to write a class-based view that responds only to `POST`, we’ll
subclass [View](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.View) and write a `post()` method
in the subclass. However if we want our processing to work on a particular
object, identified from the URL, we’ll want the functionality provided by
[SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin).

We’ll demonstrate this with the `Author` model we used in the
[generic class-based views introduction](https://docs.djangoproject.com/en/5.0/topics/generic-display/).

  `views.py`[¶](#id1)

```
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from books.models import Author

class RecordInterestView(SingleObjectMixin, View):
    """Records the current user's interest in an author."""

    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # Look up the author we're interested in.
        self.object = self.get_object()
        # Actually record interest somehow here!

        return HttpResponseRedirect(
            reverse("author-detail", kwargs={"pk": self.object.pk})
        )
```

In practice you’d probably want to record the interest in a key-value
store rather than in a relational database, so we’ve left that bit
out. The only bit of the view that needs to worry about using
[SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin) is where we want to
look up the author we’re interested in, which it does with a call to
`self.get_object()`. Everything else is taken care of for us by the mixin.

We can hook this into our URLs easily enough:

  `urls.py`[¶](#id2)

```
from django.urls import path
from books.views import RecordInterestView

urlpatterns = [
    # ...
    path(
        "author/<int:pk>/interest/",
        RecordInterestView.as_view(),
        name="author-interest",
    ),
]
```

Note the `pk` named group, which
[get_object()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object) uses
to look up the `Author` instance. You could also use a slug, or
any of the other features of
[SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin).

### UsingSingleObjectMixinwithListView¶

[ListView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.list.ListView) provides built-in
pagination, but you might want to paginate a list of objects that are
all linked (by a foreign key) to another object. In our publishing
example, you might want to paginate through all the books by a
particular publisher.

One way to do this is to combine [ListView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#ListView) with
[SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin), so that the queryset
for the paginated list of books can hang off the publisher found as the single
object. In order to do this, we need to have two different querysets:

  `Book` queryset for use by [ListView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.list.ListView)

Since we have access to the `Publisher` whose books we want to list, we
override `get_queryset()` and use the `Publisher`’s [reverse
foreign key manager](https://docs.djangoproject.com/en/5.0/db/queries/#backwards-related-objects).

  `Publisher` queryset for use in [get_object()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object)

We’ll rely on the default implementation of `get_object()` to fetch the
correct `Publisher` object.
However, we need to explicitly pass a `queryset` argument because
otherwise the default implementation of `get_object()` would call
`get_queryset()` which we have overridden to return `Book` objects
instead of `Publisher` ones.

Note

We have to think carefully about `get_context_data()`.
Since both [SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin) and
[ListView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#ListView) will
put things in the context data under the value of
`context_object_name` if it’s set, we’ll instead explicitly
ensure the `Publisher` is in the context data. [ListView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#ListView)
will add in the suitable `page_obj` and `paginator` for us
providing we remember to call `super()`.

Now we can write a new `PublisherDetailView`:

```
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from books.models import Publisher

class PublisherDetailView(SingleObjectMixin, ListView):
    paginate_by = 2
    template_name = "books/publisher_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publisher"] = self.object
        return context

    def get_queryset(self):
        return self.object.book_set.all()
```

Notice how we set `self.object` within `get()` so we
can use it again later in `get_context_data()` and `get_queryset()`.
If you don’t set `template_name`, the template will default to the normal
[ListView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#ListView) choice, which in this case would be
`"books/book_list.html"` because it’s a list of books;
[ListView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#ListView) knows nothing about
[SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin), so it doesn’t have
any clue this view is anything to do with a `Publisher`.

The `paginate_by` is deliberately small in the example so you don’t
have to create lots of books to see the pagination working! Here’s the
template you’d want to use:

```
{% extends "base.html" %}

{% block content %}
    <h2>Publisher {{ publisher.name }}</h2>

    <ol>
      {% for book in page_obj %}
        <li>{{ book.title }}</li>
      {% endfor %}
    </ol>

    <div class="pagination">
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}

            <span class="current">
                Page {{ page_obj.number }} of {{ paginator.num_pages }}.
            </span>

            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
            {% endif %}
        </span>
    </div>
{% endblock %}
```

## Avoid anything more complex¶

Generally you can use
[TemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin) and
[SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin) when you need
their functionality. As shown above, with a bit of care you can even
combine `SingleObjectMixin` with
[ListView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.list.ListView). However things get
increasingly complex as you try to do so, and a good rule of thumb is:

Hint

Each of your views should use only mixins or views from one of the
groups of generic class-based views: [detail,
list](https://docs.djangoproject.com/en/5.0/topics/generic-display/), [editing](https://docs.djangoproject.com/en/5.0/topics/generic-editing/) and
date. For example it’s fine to combine
[TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#TemplateView) (built in view) with
[MultipleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin) (generic list), but
you’re likely to have problems combining `SingleObjectMixin` (generic
detail) with `MultipleObjectMixin` (generic list).

To show what happens when you try to get more sophisticated, we show
an example that sacrifices readability and maintainability when there
is a simpler solution. First, let’s look at a naive attempt to combine
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView) with
[FormMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin) to enable us to
`POST` a Django [Form](https://docs.djangoproject.com/en/ref/forms/api/#django.forms.Form) to the same URL as we’re
displaying an object using [DetailView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DetailView).

### UsingFormMixinwithDetailView¶

Think back to our earlier example of using [View](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#View) and
[SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin) together. We were
recording a user’s interest in a particular author; say now that we want to
let them leave a message saying why they like them. Again, let’s assume we’re
not going to store this in a relational database but instead in
something more esoteric that we won’t worry about here.

At this point it’s natural to reach for a [Form](https://docs.djangoproject.com/en/ref/forms/api/#django.forms.Form) to
encapsulate the information sent from the user’s browser to Django. Say also
that we’re heavily invested in [REST](https://en.wikipedia.org/wiki/Representational_state_transfer), so we want to use the same URL for
displaying the author as for capturing the message from the
user. Let’s rewrite our `AuthorDetailView` to do that.

We’ll keep the `GET` handling from [DetailView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DetailView), although
we’ll have to add a [Form](https://docs.djangoproject.com/en/ref/forms/api/#django.forms.Form) into the context data so we can
render it in the template. We’ll also want to pull in form processing
from [FormMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin), and write a bit of
code so that on `POST` the form gets called appropriately.

Note

We use [FormMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin) and implement
`post()` ourselves rather than try to mix [DetailView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DetailView) with
[FormView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#FormView) (which provides a suitable `post()` already) because
both of the views implement `get()`, and things would get much more
confusing.

Our new `AuthorDetailView` looks like this:

```
# CAUTION: you almost certainly do not want to do this.
# It is provided as part of a discussion of problems you can
# run into when combining different generic class-based view
# functionality that is not designed to be used together.

from django import forms
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from books.models import Author

class AuthorInterestForm(forms.Form):
    message = forms.CharField()

class AuthorDetailView(FormMixin, DetailView):
    model = Author
    form_class = AuthorInterestForm

    def get_success_url(self):
        return reverse("author-detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)
```

`get_success_url()` provides somewhere to redirect to, which gets used
in the default implementation of `form_valid()`. We have to provide our
own `post()` as noted earlier.

### A better solution¶

The number of subtle interactions between
[FormMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin) and [DetailView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DetailView) is
already testing our ability to manage things. It’s unlikely you’d want to
write this kind of class yourself.

In this case, you could write the `post()` method yourself, keeping
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DetailView) as the only generic functionality, although writing
[Form](https://docs.djangoproject.com/en/ref/forms/api/#django.forms.Form) handling code involves a lot of duplication.

Alternatively, it would still be less work than the above approach to
have a separate view for processing the form, which could use
[FormView](https://docs.djangoproject.com/en/ref/class-based-views/generic-editing/#django.views.generic.edit.FormView) distinct from
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DetailView) without concerns.

### An alternative better solution¶

What we’re really trying to do here is to use two different class
based views from the same URL. So why not do just that? We have a very
clear division here: `GET` requests should get the
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#DetailView) (with the [Form](https://docs.djangoproject.com/en/ref/forms/api/#django.forms.Form) added to the context
data), and `POST` requests should get the [FormView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#FormView). Let’s
set up those views first.

The `AuthorDetailView` view is almost the same as [when we
first introduced AuthorDetailView](https://docs.djangoproject.com/en/5.0/topics/generic-display/#generic-views-extra-work); we have to
write our own `get_context_data()` to make the
`AuthorInterestForm` available to the template. We’ll skip the
`get_object()` override from before for clarity:

```
from django import forms
from django.views.generic import DetailView
from books.models import Author

class AuthorInterestForm(forms.Form):
    message = forms.CharField()

class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AuthorInterestForm()
        return context
```

Then the `AuthorInterestFormView` is a [FormView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#FormView), but we have to
bring in [SingleObjectMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin) so we can find
the author we’re talking about, and we have to remember to set
`template_name` to ensure that form errors will render the same template as
`AuthorDetailView` is using on `GET`:

```
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

class AuthorInterestFormView(SingleObjectMixin, FormView):
    template_name = "books/author_detail.html"
    form_class = AuthorInterestForm
    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("author-detail", kwargs={"pk": self.object.pk})
```

Finally we bring this together in a new `AuthorView` view. We
already know that calling [as_view()](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.View.as_view) on
a class-based view gives us something that behaves exactly like a function
based view, so we can do that at the point we choose between the two subviews.

You can pass through keyword arguments to
[as_view()](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.View.as_view) in the same way you
would in your URLconf, such as if you wanted the `AuthorInterestFormView`
behavior to also appear at another URL but using a different template:

```
from django.views import View

class AuthorView(View):
    def get(self, request, *args, **kwargs):
        view = AuthorDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AuthorInterestFormView.as_view()
        return view(request, *args, **kwargs)
```

This approach can also be used with any other generic class-based
views or your own class-based views inheriting directly from
[View](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#View) or [TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/flattened-index/#TemplateView), as it keeps the different
views as separate as possible.

## More than just HTML¶

Where class-based views shine is when you want to do the same thing many times.
Suppose you’re writing an API, and every view should return JSON instead of
rendered HTML.

We can create a mixin class to use in all of our views, handling the
conversion to JSON once.

For example, a JSON mixin might look something like this:

```
from django.http import JsonResponse

class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context
```

Note

Check out the [Serializing Django objects](https://docs.djangoproject.com/en/5.0/serialization/) documentation for more
information on how to correctly transform Django models and querysets into
JSON.

This mixin provides a `render_to_json_response()` method with the same signature
as [render_to_response()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response).
To use it, we need to mix it into a `TemplateView` for example, and override
`render_to_response()` to call `render_to_json_response()` instead:

```
from django.views.generic import TemplateView

class JSONView(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
```

Equally we could use our mixin with one of the generic views. We can make our
own version of [DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView) by mixing
`JSONResponseMixin` with the
[BaseDetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.BaseDetailView) – (the
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView) before template
rendering behavior has been mixed in):

```
from django.views.generic.detail import BaseDetailView

class JSONDetailView(JSONResponseMixin, BaseDetailView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
```

This view can then be deployed in the same way as any other
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView), with exactly the
same behavior – except for the format of the response.

If you want to be really adventurous, you could even mix a
[DetailView](https://docs.djangoproject.com/en/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView) subclass that is able
to return *both* HTML and JSON content, depending on some property of
the HTTP request, such as a query argument or an HTTP header. Mix in both the
`JSONResponseMixin` and a
[SingleObjectTemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin),
and override the implementation of
[render_to_response()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
to defer to the appropriate rendering method depending on the type of response
that the user requested:

```
from django.views.generic.detail import SingleObjectTemplateResponseMixin

class HybridDetailView(
    JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView
):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get("format") == "json":
            return self.render_to_json_response(context)
        else:
            return super().render_to_response(context)
```

Because of the way that Python resolves method overloading, the call to
`super().render_to_response(context)` ends up calling the
[render_to_response()](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.render_to_response)
implementation of [TemplateResponseMixin](https://docs.djangoproject.com/en/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin).

---

# Class

# Class-based views¶

A view is a callable which takes a request and returns a
response. This can be more than just a function, and Django provides
an example of some classes which can be used as views. These allow you
to structure your views and reuse code by harnessing inheritance and
mixins. There are also some generic views for tasks which we’ll get to later,
but you may want to design your own structure of reusable views which suits
your use case. For full details, see the [class-based views reference
documentation](https://docs.djangoproject.com/en/ref/class-based-views/).

## Basic examples¶

Django provides base view classes which will suit a wide range of applications.
All views inherit from the [View](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.View) class, which
handles linking the view into the URLs, HTTP method dispatching and other
common features. [RedirectView](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.RedirectView) provides a
HTTP redirect, and [TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.TemplateView) extends the
base class to make it also render a template.

## Usage in your URLconf¶

The most direct way to use generic views is to create them directly in your
URLconf. If you’re only changing a few attributes on a class-based view, you
can pass them into the [as_view()](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.View.as_view) method
call itself:

```
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("about/", TemplateView.as_view(template_name="about.html")),
]
```

Any arguments passed to [as_view()](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.View.as_view) will
override attributes set on the class. In this example, we set `template_name`
on the `TemplateView`. A similar overriding pattern can be used for the
`url` attribute on [RedirectView](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.RedirectView).

## Subclassing generic views¶

The second, more powerful way to use generic views is to inherit from an
existing view and override attributes (such as the `template_name`) or
methods (such as `get_context_data`) in your subclass to provide new values
or methods. Consider, for example, a view that just displays one template,
`about.html`. Django has a generic view to do this -
[TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.TemplateView) - so we can subclass it, and
override the template name:

```
# some_app/views.py
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"
```

Then we need to add this new view into our URLconf.
[TemplateView](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.TemplateView) is a class, not a function, so
we point the URL to the [as_view()](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.View.as_view) class
method instead, which provides a function-like entry to class-based views:

```
# urls.py
from django.urls import path
from some_app.views import AboutView

urlpatterns = [
    path("about/", AboutView.as_view()),
]
```

For more information on how to use the built in generic views, consult the next
topic on [generic class-based views](https://docs.djangoproject.com/en/5.0/topics/generic-display/).

### Supporting other HTTP methods¶

Suppose somebody wants to access our book library over HTTP using the views
as an API. The API client would connect every now and then and download book
data for the books published since last visit. But if no new books appeared
since then, it is a waste of CPU time and bandwidth to fetch the books from the
database, render a full response and send it to the client. It might be
preferable to ask the API when the most recent book was published.

We map the URL to book list view in the URLconf:

```
from django.urls import path
from books.views import BookListView

urlpatterns = [
    path("books/", BookListView.as_view()),
]
```

And the view:

```
from django.http import HttpResponse
from django.views.generic import ListView
from books.models import Book

class BookListView(ListView):
    model = Book

    def head(self, *args, **kwargs):
        last_book = self.get_queryset().latest("publication_date")
        response = HttpResponse(
            # RFC 1123 date format.
            headers={
                "Last-Modified": last_book.publication_date.strftime(
                    "%a, %d %b %Y %H:%M:%S GMT"
                )
            },
        )
        return response
```

If the view is accessed from a `GET` request, an object list is returned in
the response (using the `book_list.html` template). But if the client issues
a `HEAD` request, the response has an empty body and the `Last-Modified`
header indicates when the most recent book was published.  Based on this
information, the client may or may not download the full object list.

## Asynchronous class-based views¶

As well as the synchronous (`def`) method handlers already shown, `View`
subclasses may define asynchronous (`async def`) method handlers to leverage
asynchronous code using `await`:

```
import asyncio
from django.http import HttpResponse
from django.views import View

class AsyncView(View):
    async def get(self, request, *args, **kwargs):
        # Perform io-blocking view logic using await, sleep for example.
        await asyncio.sleep(1)
        return HttpResponse("Hello async world!")
```

Within a single view-class, all user-defined method handlers must be either
synchronous, using `def`, or all asynchronous, using `async def`. An
`ImproperlyConfigured` exception will be raised in `as_view()` if `def`
and `async def` declarations are mixed.

Django will automatically detect asynchronous views and run them in an
asynchronous context. You can read more about Django’s asynchronous support,
and how to best use async views, in [Asynchronous support](https://docs.djangoproject.com/en/5.0/async/).

---

# Conditional View Processing¶

# Conditional View Processing¶

HTTP clients can send a number of headers to tell the server about copies of a
resource that they have already seen. This is commonly used when retrieving a
web page (using an HTTP `GET` request) to avoid sending all the data for
something the client has already retrieved. However, the same headers can be
used for all HTTP methods (`POST`, `PUT`, `DELETE`, etc.).

For each page (response) that Django sends back from a view, it might provide
two HTTP headers: the `ETag` header and the `Last-Modified` header. These
headers are optional on HTTP responses. They can be set by your view function,
or you can rely on the [ConditionalGetMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.http.ConditionalGetMiddleware)
middleware to set the `ETag` header.

When the client next requests the same resource, it might send along a header
such as either [If-Modified-Since](https://datatracker.ietf.org/doc/html/rfc9110.html#section-13.1.3) or
[If-Unmodified-Since](https://datatracker.ietf.org/doc/html/rfc9110.html#section-13.1.4), containing the date of the
last modification time it was sent, or either [If-Match](https://datatracker.ietf.org/doc/html/rfc9110.html#section-13.1.1) or [If-None-Match](https://datatracker.ietf.org/doc/html/rfc9110.html#section-13.1.2),
containing the last `ETag` it was sent. If the current version of the page
matches the `ETag` sent by the client, or if the resource has not been
modified, a 304 status code can be sent back, instead of a full response,
telling the client that nothing has changed.  Depending on the header, if the
page has been modified or does not match the `ETag` sent by the client, a 412
status code (Precondition Failed) may be returned.

When you need more fine-grained control you may use per-view conditional
processing functions.

## Theconditiondecorator¶

Sometimes (in fact, quite often) you can create functions to rapidly compute
the [ETag](https://datatracker.ietf.org/doc/html/rfc9110.html#section-8.8.3) value or the last-modified time for a
resource, **without** needing to do all the computations needed to construct
the full view. Django can then use these functions to provide an
“early bailout” option for the view processing. Telling the client that the
content has not been modified since the last request, perhaps.

These two functions are passed as parameters to the
`django.views.decorators.http.condition` decorator. This decorator uses
the two functions (you only need to supply one, if you can’t compute both
quantities easily and quickly) to work out if the headers in the HTTP request
match those on the resource. If they don’t match, a new copy of the resource
must be computed and your normal view is called.

The `condition` decorator’s signature looks like this:

```
condition(etag_func=None, last_modified_func=None)
```

The two functions, to compute the ETag and the last modified time, will be
passed the incoming `request` object and the same parameters, in the same
order, as the view function they are helping to wrap. The function passed
`last_modified_func` should return a standard datetime value specifying the
last time the resource was modified, or `None` if the resource doesn’t
exist. The function passed to the `etag` decorator should return a string
representing the [ETag](https://datatracker.ietf.org/doc/html/rfc9110.html#section-8.8.3) for the resource, or `None`
if it doesn’t exist.

The decorator sets the `ETag` and `Last-Modified` headers on the response
if they are not already set by the view and if the request’s method is safe
(`GET` or `HEAD`).

Using this feature usefully is probably best explained with an example.
Suppose you have this pair of models, representing a small blog system:

```
import datetime
from django.db import models

class Blog(models.Model): ...

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    published = models.DateTimeField(default=datetime.datetime.now)
    ...
```

If the front page, displaying the latest blog entries, only changes when you
add a new blog entry, you can compute the last modified time very quickly. You
need the latest `published` date for every entry associated with that blog.
One way to do this would be:

```
def latest_entry(request, blog_id):
    return Entry.objects.filter(blog=blog_id).latest("published").published
```

You can then use this function to provide early detection of an unchanged page
for your front page view:

```
from django.views.decorators.http import condition

@condition(last_modified_func=latest_entry)
def front_page(request, blog_id): ...
```

Be careful with the order of decorators

When `condition()` returns a conditional response, any decorators below
it will be skipped and won’t apply to the response. Therefore, any
decorators that need to apply to both the regular view response and a
conditional response must be above `condition()`. In particular,
[vary_on_cookie()](https://docs.djangoproject.com/en/5.0/http/decorators/#django.views.decorators.vary.vary_on_cookie),
[vary_on_headers()](https://docs.djangoproject.com/en/5.0/http/decorators/#django.views.decorators.vary.vary_on_headers), and
[cache_control()](https://docs.djangoproject.com/en/5.0/http/decorators/#django.views.decorators.cache.cache_control) should come first
because [RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110.html#section-15.4.5) requires that the headers
they set be present on 304 responses.

## Shortcuts for only computing one value¶

As a general rule, if you can provide functions to compute *both* the ETag and
the last modified time, you should do so. You don’t know which headers any
given HTTP client will send you, so be prepared to handle both. However,
sometimes only one value is easy to compute and Django provides decorators
that handle only ETag or only last-modified computations.

The `django.views.decorators.http.etag` and
`django.views.decorators.http.last_modified` decorators are passed the same
type of functions as the `condition` decorator. Their signatures are:

```
etag(etag_func)
last_modified(last_modified_func)
```

We could write the earlier example, which only uses a last-modified function,
using one of these decorators:

```
@last_modified(latest_entry)
def front_page(request, blog_id): ...
```

…or:

```
def front_page(request, blog_id): ...

front_page = last_modified(latest_entry)(front_page)
```

### Useconditionwhen testing both conditions¶

It might look nicer to some people to try and chain the `etag` and
`last_modified` decorators if you want to test both preconditions. However,
this would lead to incorrect behavior.

```
# Bad code. Don't do this!
@etag(etag_func)
@last_modified(last_modified_func)
def my_view(request): ...

# End of bad code.
```

The first decorator doesn’t know anything about the second and might
answer that the response is not modified even if the second decorators would
determine otherwise. The `condition` decorator uses both callback functions
simultaneously to work out the right action to take.

## Using the decorators with other HTTP methods¶

The `condition` decorator is useful for more than only `GET` and
`HEAD` requests (`HEAD` requests are the same as `GET` in this
situation). It can also be used to provide checking for `POST`,
`PUT` and `DELETE` requests. In these situations, the idea isn’t to return
a “not modified” response, but to tell the client that the resource they are
trying to change has been altered in the meantime.

For example, consider the following exchange between the client and server:

1. Client requests `/foo/`.
2. Server responds with some content with an ETag of `"abcd1234"`.
3. Client sends an HTTP `PUT` request to `/foo/` to update the
  resource. It also sends an `If-Match: "abcd1234"` header to specify
  the version it is trying to update.
4. Server checks to see if the resource has changed, by computing the ETag
  the same way it does for a `GET` request (using the same function).
  If the resource *has* changed, it will return a 412 status code,
  meaning “precondition failed”.
5. Client sends a `GET` request to `/foo/`, after receiving a 412
  response, to retrieve an updated version of the content before updating
  it.

The important thing this example shows is that the same functions can be used
to compute the ETag and last modification values in all situations. In fact,
you **should** use the same functions, so that the same values are returned
every time.

Validator headers with non-safe request methods

The `condition` decorator only sets validator headers (`ETag` and
`Last-Modified`) for safe HTTP methods, i.e. `GET` and `HEAD`. If you
wish to return them in other cases, set them in your view. See
[RFC 9110 Section 9.3.4](https://datatracker.ietf.org/doc/html/rfc9110.html#section-9.3.4) to learn about the distinction between setting a
validator header in response to requests made with `PUT` versus `POST`.

## Comparison with middleware conditional processing¶

Django provides conditional `GET` handling via
[django.middleware.http.ConditionalGetMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.http.ConditionalGetMiddleware). While being suitable
for many situations, the middleware has limitations for advanced usage:

- It’s applied globally to all views in your project.
- It doesn’t save you from generating the response, which may be expensive.
- It’s only appropriate for HTTP `GET` requests.

You should choose the most appropriate tool for your particular problem here.
If you have a way to compute ETags and modification times quickly and if some
view takes a while to generate the content, you should consider using the
`condition` decorator described in this document. If everything already runs
fairly quickly, stick to using the middleware and the amount of network
traffic sent back to the clients will still be reduced if the view hasn’t
changed.
