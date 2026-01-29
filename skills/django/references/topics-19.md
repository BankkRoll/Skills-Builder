# File Uploads¶ and more

# File Uploads¶

# File Uploads¶

When Django handles a file upload, the file data ends up placed in
[request.FILES](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.FILES) (for more on the
`request` object see the documentation for [request and response objects](https://docs.djangoproject.com/en/ref/request-response/)). This document explains how files are stored on disk
and in memory, and how to customize the default behavior.

Warning

There are security risks if you are accepting uploaded content from
untrusted users! See the security guide’s topic on
[User-uploaded content](https://docs.djangoproject.com/en/5.0/security/#user-uploaded-content-security) for mitigation details.

## Basic file uploads¶

Consider a form containing a [FileField](https://docs.djangoproject.com/en/ref/forms/fields/#django.forms.FileField):

  `forms.py`[¶](#id3)

```
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
```

A view handling this form will receive the file data in
[request.FILES](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.FILES), which is a dictionary
containing a key for each [FileField](https://docs.djangoproject.com/en/ref/forms/fields/#django.forms.FileField) (or
[ImageField](https://docs.djangoproject.com/en/ref/forms/fields/#django.forms.ImageField), or other [FileField](https://docs.djangoproject.com/en/ref/forms/fields/#django.forms.FileField)
subclass) in the form. So the data from the above form would
be accessible as `request.FILES['file']`.

Note that [request.FILES](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.FILES) will only
contain data if the request method was `POST`, at least one file field was
actually posted, and the `<form>` that posted the request has the attribute
`enctype="multipart/form-data"`. Otherwise, `request.FILES` will be empty.

Most of the time, you’ll pass the file data from `request` into the form as
described in [Binding uploaded files to a form](https://docs.djangoproject.com/en/ref/forms/api/#binding-uploaded-files). This would look something like:

  `views.py`[¶](#id4)

```
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
```

Notice that we have to pass [request.FILES](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.FILES)
into the form’s constructor; this is how file data gets bound into a form.

Here’s a common way you might handle an uploaded file:

```
def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
```

Looping over `UploadedFile.chunks()` instead of using `read()` ensures that
large files don’t overwhelm your system’s memory.

There are a few other methods and attributes available on `UploadedFile`
objects; see [UploadedFile](https://docs.djangoproject.com/en/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile) for a complete reference.

### Handling uploaded files with a model¶

If you’re saving a file on a [Model](https://docs.djangoproject.com/en/ref/models/instances/#django.db.models.Model) with a
[FileField](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.FileField), using a [ModelForm](https://docs.djangoproject.com/en/5.0/forms/modelforms/#django.forms.ModelForm)
makes this process much easier. The file object will be saved to the location
specified by the [upload_to](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.FileField.upload_to) argument of the
corresponding [FileField](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.FileField) when calling
`form.save()`:

```
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ModelFormWithFileField

def upload_file(request):
    if request.method == "POST":
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect("/success/url/")
    else:
        form = ModelFormWithFileField()
    return render(request, "upload.html", {"form": form})
```

If you are constructing an object manually, you can assign the file object from
[request.FILES](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.FILES) to the file field in the
model:

```
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import ModelWithFileField

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ModelWithFileField(file_field=request.FILES["file"])
            instance.save()
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
```

If you are constructing an object manually outside of a request, you can assign
a [File](https://docs.djangoproject.com/en/ref/files/file/#django.core.files.File) like object to the
[FileField](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.FileField):

```
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

class MyCommand(BaseCommand):
    def handle(self, *args, **options):
        content_file = ContentFile(b"Hello world!", name="hello-world.txt")
        instance = ModelWithFileField(file_field=content_file)
        instance.save()
```

### Uploading multiple files¶

If you want to upload multiple files using one form field, create a subclass
of the field’s widget and set its `allow_multiple_selected` class attribute
to `True`.

In order for such files to be all validated by your form (and have the value of
the field include them all), you will also have to subclass `FileField`. See
below for an example.

Multiple file field

Django is likely to have a proper multiple file field support at some point
in the future.

   `forms.py`[¶](#id5)

```
from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class FileFieldForm(forms.Form):
    file_field = MultipleFileField()
```

Then override the `form_valid()` method of your
[FormView](https://docs.djangoproject.com/en/ref/class-based-views/generic-editing/#django.views.generic.edit.FormView) subclass to handle multiple file
uploads:

  `views.py`[¶](#id6)

```
from django.views.generic.edit import FormView
from .forms import FileFieldForm

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "upload.html"  # Replace with your template.
    success_url = "..."  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            ...  # Do something with each file.
        return super().form_valid(form)
```

Warning

This will allow you to handle multiple files at the form level only. Be
aware that you cannot use it to put multiple files on a single model
instance (in a single field), for example, even if the custom widget is used
with a form field related to a model `FileField`.

   Changed in Django 3.2.19:

In previous versions, there was no support for the `allow_multiple_selected`
class attribute, and users were advised to create the widget with the HTML
attribute `multiple` set through the `attrs` argument. However, this
caused validation of the form field to be applied only to the last file
submitted, which could have adverse security implications.

## Upload Handlers¶

When a user uploads a file, Django passes off the file data to an *upload
handler* – a small class that handles file data as it gets uploaded. Upload
handlers are initially defined in the [FILE_UPLOAD_HANDLERS](https://docs.djangoproject.com/en/ref/settings/#std-setting-FILE_UPLOAD_HANDLERS) setting,
which defaults to:

```
[
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]
```

Together [MemoryFileUploadHandler](https://docs.djangoproject.com/en/ref/files/uploads/#django.core.files.uploadhandler.MemoryFileUploadHandler) and
[TemporaryFileUploadHandler](https://docs.djangoproject.com/en/ref/files/uploads/#django.core.files.uploadhandler.TemporaryFileUploadHandler) provide Django’s default file upload
behavior of reading small files into memory and large ones onto disk.

You can write custom handlers that customize how Django handles files. You
could, for example, use custom handlers to enforce user-level quotas, compress
data on the fly, render progress bars, and even send data to another storage
location directly without storing it locally. See [Writing custom upload handlers](https://docs.djangoproject.com/en/ref/files/uploads/#custom-upload-handlers)
for details on how you can customize or completely replace upload behavior.

### Where uploaded data is stored¶

Before you save uploaded files, the data needs to be stored somewhere.

By default, if an uploaded file is smaller than 2.5 megabytes, Django will hold
the entire contents of the upload in memory. This means that saving the file
involves only a read from memory and a write to disk and thus is very fast.

However, if an uploaded file is too large, Django will write the uploaded file
to a temporary file stored in your system’s temporary directory. On a Unix-like
platform this means you can expect Django to generate a file called something
like `/tmp/tmpzfp6I6.upload`. If an upload is large enough, you can watch this
file grow in size as Django streams the data onto disk.

These specifics – 2.5 megabytes; `/tmp`; etc. – are “reasonable defaults”
which can be customized as described in the next section.

### Changing upload handler behavior¶

There are a few settings which control Django’s file upload behavior. See
[File Upload Settings](https://docs.djangoproject.com/en/ref/settings/#file-upload-settings) for details.

### Modifying upload handlers on the fly¶

Sometimes particular views require different upload behavior. In these cases,
you can override upload handlers on a per-request basis by modifying
`request.upload_handlers`. By default, this list will contain the upload
handlers given by [FILE_UPLOAD_HANDLERS](https://docs.djangoproject.com/en/ref/settings/#std-setting-FILE_UPLOAD_HANDLERS), but you can modify the list
as you would any other list.

For instance, suppose you’ve written a `ProgressBarUploadHandler` that
provides feedback on upload progress to some sort of AJAX widget. You’d add this
handler to your upload handlers like this:

```
request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
```

You’d probably want to use `list.insert()` in this case (instead of
`append()`) because a progress bar handler would need to run *before* any
other handlers. Remember, the upload handlers are processed in order.

If you want to replace the upload handlers completely, you can assign a new
list:

```
request.upload_handlers = [ProgressBarUploadHandler(request)]
```

Note

You can only modify upload handlers *before* accessing
`request.POST` or `request.FILES` – it doesn’t make sense to
change upload handlers after upload handling has already
started. If you try to modify `request.upload_handlers` after
reading from `request.POST` or `request.FILES` Django will
throw an error.

Thus, you should always modify uploading handlers as early in your view as
possible.

Also, `request.POST` is accessed by
[CsrfViewMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.csrf.CsrfViewMiddleware) which is enabled by
default. This means you will need to use
[csrf_exempt()](https://docs.djangoproject.com/en/ref/csrf/#django.views.decorators.csrf.csrf_exempt) on your view to allow you
to change the upload handlers.  You will then need to use
[csrf_protect()](https://docs.djangoproject.com/en/ref/csrf/#django.views.decorators.csrf.csrf_protect) on the function that
actually processes the request.  Note that this means that the handlers may
start receiving the file upload before the CSRF checks have been done.
Example code:

```
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def upload_file_view(request):
    request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
    return _upload_file_view(request)

@csrf_protect
def _upload_file_view(request):
    # Process request
    ...
```

If you are using a class-based view, you will need to use
[csrf_exempt()](https://docs.djangoproject.com/en/ref/csrf/#django.views.decorators.csrf.csrf_exempt) on its
[dispatch()](https://docs.djangoproject.com/en/ref/class-based-views/base/#django.views.generic.base.View.dispatch) method and
[csrf_protect()](https://docs.djangoproject.com/en/ref/csrf/#django.views.decorators.csrf.csrf_protect) on the method that
actually processes the request. Example code:

```
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@method_decorator(csrf_exempt, name="dispatch")
class UploadFileView(View):
    def setup(self, request, *args, **kwargs):
        request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
        super().setup(request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        # Process request
        ...
```

---

# Middleware¶

# Middleware¶

Middleware is a framework of hooks into Django’s request/response processing.
It’s a light, low-level “plugin” system for globally altering Django’s input
or output.

Each middleware component is responsible for doing some specific function. For
example, Django includes a middleware component,
[AuthenticationMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware), that
associates users with requests using sessions.

This document explains how middleware works, how you activate middleware, and
how to write your own middleware. Django ships with some built-in middleware
you can use right out of the box. They’re documented in the [built-in
middleware reference](https://docs.djangoproject.com/en/ref/middleware/).

## Writing your own middleware¶

A middleware factory is a callable that takes a `get_response` callable and
returns a middleware. A middleware is a callable that takes a request and
returns a response, just like a view.

A middleware can be written as a function that looks like this:

```
def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
```

Or it can be written as a class whose instances are callable, like this:

```
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
```

The `get_response` callable provided by Django might be the actual view (if
this is the last listed middleware) or it might be the next middleware in the
chain. The current middleware doesn’t need to know or care what exactly it is,
just that it represents whatever comes next.

The above is a slight simplification – the `get_response` callable for the
last middleware in the chain won’t be the actual view but rather a wrapper
method from the handler which takes care of applying [view middleware](#view-middleware), calling the view with appropriate URL arguments, and
applying [template-response](#template-response-middleware) and
[exception](#exception-middleware) middleware.

Middleware can either support only synchronous Python (the default), only
asynchronous Python, or both. See [Asynchronous support](#async-middleware) for details of how to
advertise what you support, and know what kind of request you are getting.

Middleware can live anywhere on your Python path.

### __init__(get_response)¶

Middleware factories must accept a `get_response` argument. You can also
initialize some global state for the middleware. Keep in mind a couple of
caveats:

- Django initializes your middleware with only the `get_response` argument,
  so you can’t define `__init__()` as requiring any other arguments.
- Unlike the `__call__()` method which is called once per request,
  `__init__()` is called only *once*, when the web server starts.

### Marking middleware as unused¶

It’s sometimes useful to determine at startup time whether a piece of
middleware should be used. In these cases, your middleware’s `__init__()`
method may raise [MiddlewareNotUsed](https://docs.djangoproject.com/en/ref/exceptions/#django.core.exceptions.MiddlewareNotUsed). Django will
then remove that middleware from the middleware process and log a debug message
to the [django.request](https://docs.djangoproject.com/en/ref/logging/#django-request-logger) logger when [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) is `True`.

## Activating middleware¶

To activate a middleware component, add it to the [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE) list in
your Django settings.

In [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE), each middleware component is represented by a string:
the full Python path to the middleware factory’s class or function name. For
example, here’s the default value created by [django-adminstartproject](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-startproject):

```
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

A Django installation doesn’t require any middleware — [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE)
can be empty, if you’d like — but it’s strongly suggested that you at least use
[CommonMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.common.CommonMiddleware).

The order in [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE) matters because a middleware can depend on
other middleware. For instance,
[AuthenticationMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware) stores the
authenticated user in the session; therefore, it must run after
[SessionMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.contrib.sessions.middleware.SessionMiddleware). See
[Middleware ordering](https://docs.djangoproject.com/en/ref/middleware/#middleware-ordering) for some common hints about ordering of Django
middleware classes.

## Middleware order and layering¶

During the request phase, before calling the view, Django applies middleware in
the order it’s defined in [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE), top-down.

You can think of it like an onion: each middleware class is a “layer” that
wraps the view, which is in the core of the onion. If the request passes
through all the layers of the onion (each one calls `get_response` to pass
the request in to the next layer), all the way to the view at the core, the
response will then pass through every layer (in reverse order) on the way back
out.

If one of the layers decides to short-circuit and return a response without
ever calling its `get_response`, none of the layers of the onion inside that
layer (including the view) will see the request or the response. The response
will only return through the same layers that the request passed in through.

## Other middleware hooks¶

Besides the basic request/response middleware pattern described earlier, you
can add three other special methods to class-based middleware:

### process_view()¶

   process_view(*request*, *view_func*, *view_args*, *view_kwargs*)[¶](#process_view)

`request` is an [HttpRequest](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest) object. `view_func` is
the Python function that Django is about to use. (It’s the actual function
object, not the name of the function as a string.) `view_args` is a list of
positional arguments that will be passed to the view, and `view_kwargs` is a
dictionary of keyword arguments that will be passed to the view. Neither
`view_args` nor `view_kwargs` include the first view argument
(`request`).

`process_view()` is called just before Django calls the view.

It should return either `None` or an [HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse)
object. If it returns `None`, Django will continue processing this request,
executing any other `process_view()` middleware and, then, the appropriate
view. If it returns an [HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse) object, Django won’t
bother calling the appropriate view; it’ll apply response middleware to that
[HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse) and return the result.

Note

Accessing [request.POST](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.POST) inside
middleware before the view runs or in `process_view()` will prevent any
view running after the middleware from being able to [modify the
upload handlers for the request](https://docs.djangoproject.com/en/5.0/topics/file-uploads/#modifying-upload-handlers-on-the-fly),
and should normally be avoided.

The [CsrfViewMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.csrf.CsrfViewMiddleware) class can be
considered an exception, as it provides the
[csrf_exempt()](https://docs.djangoproject.com/en/ref/csrf/#django.views.decorators.csrf.csrf_exempt) and
[csrf_protect()](https://docs.djangoproject.com/en/ref/csrf/#django.views.decorators.csrf.csrf_protect) decorators which allow
views to explicitly control at what point the CSRF validation should occur.

### process_exception()¶

   process_exception(*request*, *exception*)[¶](#process_exception)

`request` is an [HttpRequest](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest) object. `exception` is an
`Exception` object raised by the view function.

Django calls `process_exception()` when a view raises an exception.
`process_exception()` should return either `None` or an
[HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse) object. If it returns an
[HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse) object, the template response and response
middleware will be applied and the resulting response returned to the
browser. Otherwise, [default exception handling](https://docs.djangoproject.com/en/ref/views/#error-views) kicks in.

Again, middleware are run in reverse order during the response phase, which
includes `process_exception`. If an exception middleware returns a response,
the `process_exception` methods of the middleware classes above that
middleware won’t be called at all.

### process_template_response()¶

   process_template_response(*request*, *response*)[¶](#process_template_response)

`request` is an [HttpRequest](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest) object. `response` is
the [TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse) object (or equivalent)
returned by a Django view or by a middleware.

`process_template_response()` is called just after the view has finished
executing, if the response instance has a `render()` method, indicating that
it is a [TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse) or equivalent.

It must return a response object that implements a `render` method. It could
alter the given `response` by changing `response.template_name` and
`response.context_data`, or it could create and return a brand-new
[TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse) or equivalent.

You don’t need to explicitly render responses – responses will be
automatically rendered once all template response middleware has been
called.

Middleware are run in reverse order during the response phase, which
includes `process_template_response()`.

## Dealing with streaming responses¶

Unlike [HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse),
[StreamingHttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.StreamingHttpResponse) does not have a `content`
attribute. As a result, middleware can no longer assume that all responses
will have a `content` attribute. If they need access to the content, they
must test for streaming responses and adjust their behavior accordingly:

```
if response.streaming:
    response.streaming_content = wrap_streaming_content(response.streaming_content)
else:
    response.content = alter_content(response.content)
```

Note

`streaming_content` should be assumed to be too large to hold in memory.
Response middleware may wrap it in a new generator, but must not consume
it. Wrapping is typically implemented as follows:

```
def wrap_streaming_content(content):
    for chunk in content:
        yield alter_content(chunk)
```

[StreamingHttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.StreamingHttpResponse) allows both synchronous and
asynchronous iterators. The wrapping function must match. Check
[StreamingHttpResponse.is_async](https://docs.djangoproject.com/en/ref/request-response/#django.http.StreamingHttpResponse.is_async) if your middleware needs to
support both types of iterator.

  Changed in Django 4.2:

Support for streaming responses with asynchronous iterators was added.

## Exception handling¶

Django automatically converts exceptions raised by the view or by middleware
into an appropriate HTTP response with an error status code. [Certain
exceptions](https://docs.djangoproject.com/en/ref/views/#error-views) are converted to 4xx status codes, while an unknown
exception is converted to a 500 status code.

This conversion takes place before and after each middleware (you can think of
it as the thin film in between each layer of the onion), so that every
middleware can always rely on getting some kind of HTTP response back from
calling its `get_response` callable. Middleware don’t need to worry about
wrapping their call to `get_response` in a `try/except` and handling an
exception that might have been raised by a later middleware or the view. Even
if the very next middleware in the chain raises an
[Http404](https://docs.djangoproject.com/en/5.0/topics/views/#django.http.Http404) exception, for example, your middleware won’t see
that exception; instead it will get an [HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse)
object with a [status_code](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse.status_code) of 404.

You can set [DEBUG_PROPAGATE_EXCEPTIONS](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG_PROPAGATE_EXCEPTIONS) to `True` to skip this
conversion and propagate exceptions upward.

## Asynchronous support¶

Middleware can support any combination of synchronous and asynchronous
requests. Django will adapt requests to fit the middleware’s requirements if it
cannot support both, but at a performance penalty.

By default, Django assumes that your middleware is capable of handling only
synchronous requests. To change these assumptions, set the following attributes
on your middleware factory function or class:

- `sync_capable` is a boolean indicating if the middleware can handle
  synchronous requests. Defaults to `True`.
- `async_capable` is a boolean indicating if the middleware can handle
  asynchronous requests. Defaults to `False`.

If your middleware has both `sync_capable = True` and
`async_capable = True`, then Django will pass it the request without
converting it. In this case, you can work out if your middleware will receive
async requests by checking if the `get_response` object you are passed is a
coroutine function, using `asgiref.sync.iscoroutinefunction`.

The `django.utils.decorators` module contains
[sync_only_middleware()](https://docs.djangoproject.com/en/ref/utils/#django.utils.decorators.sync_only_middleware),
[async_only_middleware()](https://docs.djangoproject.com/en/ref/utils/#django.utils.decorators.async_only_middleware), and
[sync_and_async_middleware()](https://docs.djangoproject.com/en/ref/utils/#django.utils.decorators.sync_and_async_middleware) decorators that
allow you to apply these flags to middleware factory functions.

The returned callable must match the sync or async nature of the
`get_response` method. If you have an asynchronous `get_response`, you must
return a coroutine function (`async def`).

`process_view`, `process_template_response` and `process_exception`
methods, if they are provided, should also be adapted to match the sync/async
mode. However, Django will individually adapt them as required if you do not,
at an additional performance penalty.

Here’s an example of how to create a middleware function that supports both:

```
from asgiref.sync import iscoroutinefunction
from django.utils.decorators import sync_and_async_middleware

@sync_and_async_middleware
def simple_middleware(get_response):
    # One-time configuration and initialization goes here.
    if iscoroutinefunction(get_response):

        async def middleware(request):
            # Do something here!
            response = await get_response(request)
            return response

    else:

        def middleware(request):
            # Do something here!
            response = get_response(request)
            return response

    return middleware
```

Note

If you declare a hybrid middleware that supports both synchronous and
asynchronous calls, the kind of call you get may not match the underlying
view. Django will optimize the middleware call stack to have as few
sync/async transitions as possible.

Thus, even if you are wrapping an async view, you may be called in sync
mode if there is other, synchronous middleware between you and the view.

When using an asynchronous class-based middleware, you must ensure that
instances are correctly marked as coroutine functions:

```
from asgiref.sync import iscoroutinefunction, markcoroutinefunction

class AsyncMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        response = await self.get_response(request)
        # Some logic ...
        return response
```

## Upgrading pre-Django 1.10-style middleware¶

   *class*django.utils.deprecation.MiddlewareMixin[¶](#django.utils.deprecation.MiddlewareMixin)

Django provides `django.utils.deprecation.MiddlewareMixin` to ease creating
middleware classes that are compatible with both [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE) and the
old `MIDDLEWARE_CLASSES`, and support synchronous and asynchronous requests.
All middleware classes included with Django are compatible with both settings.

The mixin provides an `__init__()` method that requires a `get_response`
argument and stores it in `self.get_response`.

The `__call__()` method:

1. Calls `self.process_request(request)` (if defined).
2. Calls `self.get_response(request)` to get the response from later
  middleware and the view.
3. Calls `self.process_response(request, response)` (if defined).
4. Returns the response.

If used with `MIDDLEWARE_CLASSES`, the `__call__()` method will
never be used; Django calls `process_request()` and `process_response()`
directly.

In most cases, inheriting from this mixin will be sufficient to make an
old-style middleware compatible with the new system with sufficient
backwards-compatibility. The new short-circuiting semantics will be harmless or
even beneficial to the existing middleware. In a few cases, a middleware class
may need some changes to adjust to the new semantics.

These are the behavioral differences between using [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE) and
`MIDDLEWARE_CLASSES`:

1. Under `MIDDLEWARE_CLASSES`, every middleware will always have its
  `process_response` method called, even if an earlier middleware
  short-circuited by returning a response from its `process_request`
  method. Under [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE), middleware behaves more like an onion:
  the layers that a response goes through on the way out are the same layers
  that saw the request on the way in. If a middleware short-circuits, only
  that middleware and the ones before it in [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE) will see the
  response.
2. Under `MIDDLEWARE_CLASSES`, `process_exception` is applied to
  exceptions raised from a middleware `process_request` method. Under
  [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE), `process_exception` applies only to exceptions
  raised from the view (or from the `render` method of a
  [TemplateResponse](https://docs.djangoproject.com/en/ref/template-response/#django.template.response.TemplateResponse)). Exceptions raised from
  a middleware are converted to the appropriate HTTP response and then passed
  to the next middleware.
3. Under `MIDDLEWARE_CLASSES`, if a `process_response` method raises
  an exception, the `process_response` methods of all earlier middleware are
  skipped and a `500 Internal Server Error` HTTP response is always
  returned (even if the exception raised was e.g. an
  [Http404](https://docs.djangoproject.com/en/5.0/topics/views/#django.http.Http404)). Under [MIDDLEWARE](https://docs.djangoproject.com/en/ref/settings/#std-setting-MIDDLEWARE), an exception
  raised from a middleware will immediately be converted to the appropriate
  HTTP response, and then the next middleware in line will see that
  response. Middleware are never skipped due to a middleware raising an
  exception.
