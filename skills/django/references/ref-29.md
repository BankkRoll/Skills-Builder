# Validators¶ and more

# Validators¶

# Validators¶

## Writing validators¶

A validator is a callable that takes a value and raises a
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if it doesn’t meet some
criteria. Validators can be useful for reusing validation logic between
different types of fields.

For example, here’s a validator that only allows even numbers:

```
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _("%(value)s is not an even number"),
            params={"value": value},
        )
```

You can add this to a model field via the field’s [validators](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.validators)
argument:

```
from django.db import models

class MyModel(models.Model):
    even_field = models.IntegerField(validators=[validate_even])
```

Because values are converted to Python before validators are run, you can even
use the same validator with forms:

```
from django import forms

class MyForm(forms.Form):
    even_field = forms.IntegerField(validators=[validate_even])
```

You can also use a class with a `__call__()` method for more complex or
configurable validators. [RegexValidator](#django.core.validators.RegexValidator), for example, uses this
technique. If a class-based validator is used in the
[validators](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.validators) model field option, you should make
sure it is [serializable by the migration framework](https://docs.djangoproject.com/en/topics/migrations/#migration-serializing) by adding [deconstruct()](https://docs.djangoproject.com/en/topics/migrations/#custom-deconstruct-method) and `__eq__()` methods.

## How validators are run¶

See the [form validation](https://docs.djangoproject.com/en/5.0/forms/validation/) for more information on
how validators are run in forms, and [Validating objects](https://docs.djangoproject.com/en/5.0/models/instances/#validating-objects) for how they’re run in models. Note that validators will
not be run automatically when you save a model, but if you are using a
[ModelForm](https://docs.djangoproject.com/en/topics/forms/modelforms/#django.forms.ModelForm), it will run your validators on any fields
that are included in your form. See the
[ModelForm documentation](https://docs.djangoproject.com/en/topics/forms/modelforms/) for information on
how model validation interacts with forms.

## Built-in validators¶

The [django.core.validators](#module-django.core.validators) module contains a collection of callable
validators for use with model and form fields. They’re used internally but
are available for use with your own fields, too. They can be used in addition
to, or in lieu of custom `field.clean()` methods.

### RegexValidator¶

   *class*RegexValidator(*regex=None*, *message=None*, *code=None*, *inverse_match=None*, *flags=0*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#RegexValidator)[¶](#django.core.validators.RegexValidator)  Parameters:

- **regex** – If not `None`, overrides [regex](#django.core.validators.RegexValidator.regex). Can be a regular
  expression string or a pre-compiled regular expression.
- **message** – If not `None`, overrides [message](#django.core.validators.RegexValidator.message).
- **code** – If not `None`, overrides [code](#django.core.validators.RegexValidator.code).
- **inverse_match** – If not `None`, overrides [inverse_match](#django.core.validators.RegexValidator.inverse_match).
- **flags** – If not `None`, overrides [flags](#django.core.validators.RegexValidator.flags). In that case,
  [regex](#django.core.validators.RegexValidator.regex) must be a regular expression string, or
  [TypeError](https://docs.python.org/3/library/exceptions.html#TypeError) is raised.

A [RegexValidator](#django.core.validators.RegexValidator) searches the provided `value` for a given
regular expression with [re.search()](https://docs.python.org/3/library/re.html#re.search). By default, raises a
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with [message](#django.core.validators.RegexValidator.message) and
[code](#django.core.validators.RegexValidator.code) if a match **is not** found. Its behavior can be inverted by
setting [inverse_match](#django.core.validators.RegexValidator.inverse_match) to `True`, in which case the
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) is raised when a match
**is** found.

   regex[¶](#django.core.validators.RegexValidator.regex)

The regular expression pattern to search for within the provided
`value`, using [re.search()](https://docs.python.org/3/library/re.html#re.search). This may be a string or a
pre-compiled regular expression created with [re.compile()](https://docs.python.org/3/library/re.html#re.compile).
Defaults to the empty string, which will be found in every possible
`value`.

    message[¶](#django.core.validators.RegexValidator.message)

The error message used by
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if validation fails.
Defaults to `"Enter a valid value"`.

    code[¶](#django.core.validators.RegexValidator.code)

The error code used by [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError)
if validation fails. Defaults to `"invalid"`.

    inverse_match[¶](#django.core.validators.RegexValidator.inverse_match)

The match mode for [regex](#django.core.validators.RegexValidator.regex). Defaults to `False`.

    flags[¶](#django.core.validators.RegexValidator.flags)

The [regex flags](https://docs.python.org/3/library/re.html#contents-of-module-re) used when
compiling the regular expression string [regex](#django.core.validators.RegexValidator.regex). If [regex](#django.core.validators.RegexValidator.regex)
is a pre-compiled regular expression, and [flags](#django.core.validators.RegexValidator.flags) is overridden,
[TypeError](https://docs.python.org/3/library/exceptions.html#TypeError) is raised. Defaults to `0`.

### EmailValidator¶

   *class*EmailValidator(*message=None*, *code=None*, *allowlist=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#EmailValidator)[¶](#django.core.validators.EmailValidator)  Parameters:

- **message** – If not `None`, overrides [message](#django.core.validators.EmailValidator.message).
- **code** – If not `None`, overrides [code](#django.core.validators.EmailValidator.code).
- **allowlist** – If not `None`, overrides [allowlist](#django.core.validators.EmailValidator.allowlist).

An [EmailValidator](#django.core.validators.EmailValidator) ensures that a value looks like an email, and
raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with
[message](#django.core.validators.EmailValidator.message) and [code](#django.core.validators.EmailValidator.code) if it doesn’t. Values longer than 320
characters are always considered invalid.

   message[¶](#django.core.validators.EmailValidator.message)

The error message used by
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if validation fails.
Defaults to `"Enter a valid email address"`.

    code[¶](#django.core.validators.EmailValidator.code)

The error code used by [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError)
if validation fails. Defaults to `"invalid"`.

    allowlist[¶](#django.core.validators.EmailValidator.allowlist)

Allowlist of email domains. By default, a regular expression (the
`domain_regex` attribute) is used to validate whatever appears after
the `@` sign. However, if that string appears in the `allowlist`,
this validation is bypassed. If not provided, the default `allowlist`
is `['localhost']`. Other domains that don’t contain a dot won’t pass
validation, so you’d need to add them to the `allowlist` as
necessary.

   Changed in Django 3.2.20:

In older versions, values longer than 320 characters could be
considered valid.

### URLValidator¶

   *class*URLValidator(*schemes=None*, *regex=None*, *message=None*, *code=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#URLValidator)[¶](#django.core.validators.URLValidator)

A [RegexValidator](#django.core.validators.RegexValidator) subclass that ensures a value looks like a URL,
and raises an error code of `'invalid'` if it doesn’t. Values longer than
[max_length](#django.core.validators.URLValidator.max_length) characters are always considered invalid.

Loopback addresses and reserved IP spaces are considered valid. Literal
IPv6 addresses ([RFC 3986 Section 3.2.2](https://datatracker.ietf.org/doc/html/rfc3986.html#section-3.2.2)) and Unicode domains are both
supported.

In addition to the optional arguments of its parent [RegexValidator](#django.core.validators.RegexValidator)
class, `URLValidator` accepts an extra optional attribute:

   schemes[¶](#django.core.validators.URLValidator.schemes)

URL/URI scheme list to validate against. If not provided, the default
list is `['http', 'https', 'ftp', 'ftps']`. As a reference, the IANA
website provides a full list of [valid URI schemes](https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml).

Warning

Values starting with `file:///` will not pass validation even
when the `file` scheme is provided. Valid values must contain a
host.

     max_length[¶](#django.core.validators.URLValidator.max_length)  New in Django 3.2.20.

The maximum length of values that could be considered valid. Defaults
to 2048 characters.

   Changed in Django 3.2.20:

In older versions, values longer than 2048 characters could be
considered valid.

### validate_email¶

   validate_email[¶](#django.core.validators.validate_email)

An [EmailValidator](#django.core.validators.EmailValidator) instance without any customizations.

### validate_slug¶

   validate_slug[¶](#django.core.validators.validate_slug)

A [RegexValidator](#django.core.validators.RegexValidator) instance that ensures a value consists of only
letters, numbers, underscores or hyphens.

### validate_unicode_slug¶

   validate_unicode_slug[¶](#django.core.validators.validate_unicode_slug)

A [RegexValidator](#django.core.validators.RegexValidator) instance that ensures a value consists of only
Unicode letters, numbers, underscores, or hyphens.

### validate_ipv4_address¶

   validate_ipv4_address[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#validate_ipv4_address)[¶](#django.core.validators.validate_ipv4_address)

A [RegexValidator](#django.core.validators.RegexValidator) instance that ensures a value looks like an IPv4
address.

### validate_ipv6_address¶

   validate_ipv6_address[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#validate_ipv6_address)[¶](#django.core.validators.validate_ipv6_address)

Uses `django.utils.ipv6` to check the validity of an IPv6 address.

### validate_ipv46_address¶

   validate_ipv46_address[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#validate_ipv46_address)[¶](#django.core.validators.validate_ipv46_address)

Uses both `validate_ipv4_address` and `validate_ipv6_address` to
ensure a value is either a valid IPv4 or IPv6 address.

### validate_comma_separated_integer_list¶

   validate_comma_separated_integer_list[¶](#django.core.validators.validate_comma_separated_integer_list)

A [RegexValidator](#django.core.validators.RegexValidator) instance that ensures a value is a
comma-separated list of integers.

### int_list_validator¶

   int_list_validator(*sep=','*, *message=None*, *code='invalid'*, *allow_negative=False*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#int_list_validator)[¶](#django.core.validators.int_list_validator)

Returns a [RegexValidator](#django.core.validators.RegexValidator) instance that ensures a string consists
of integers separated by `sep`. It allows negative integers when
`allow_negative` is `True`.

### MaxValueValidator¶

   *class*MaxValueValidator(*limit_value*, *message=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#MaxValueValidator)[¶](#django.core.validators.MaxValueValidator)

Raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with a code of
`'max_value'` if `value` is greater than `limit_value`, which may be
a callable.

### MinValueValidator¶

   *class*MinValueValidator(*limit_value*, *message=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#MinValueValidator)[¶](#django.core.validators.MinValueValidator)

Raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with a code of
`'min_value'` if `value` is less than `limit_value`, which may be a
callable.

### MaxLengthValidator¶

   *class*MaxLengthValidator(*limit_value*, *message=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#MaxLengthValidator)[¶](#django.core.validators.MaxLengthValidator)

Raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with a code of
`'max_length'` if the length of `value` is greater than
`limit_value`, which may be a callable.

### MinLengthValidator¶

   *class*MinLengthValidator(*limit_value*, *message=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#MinLengthValidator)[¶](#django.core.validators.MinLengthValidator)

Raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with a code of
`'min_length'` if the length of `value` is less than `limit_value`,
which may be a callable.

### DecimalValidator¶

   *class*DecimalValidator(*max_digits*, *decimal_places*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#DecimalValidator)[¶](#django.core.validators.DecimalValidator)

Raises [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with the following
codes:

- `'max_digits'` if the number of digits is larger than `max_digits`.
- `'max_decimal_places'` if the number of decimals is larger than
  `decimal_places`.
- `'max_whole_digits'` if the number of whole digits is larger than
  the difference between `max_digits` and `decimal_places`.

### FileExtensionValidator¶

   *class*FileExtensionValidator(*allowed_extensions*, *message*, *code*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#FileExtensionValidator)[¶](#django.core.validators.FileExtensionValidator)

Raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with a code of
`'invalid_extension'` if the extension of `value.name` (`value` is
a [File](https://docs.djangoproject.com/en/5.0/files/file/#django.core.files.File)) isn’t found in `allowed_extensions`.
The extension is compared case-insensitively with `allowed_extensions`.

Warning

Don’t rely on validation of the file extension to determine a file’s
type. Files can be renamed to have any extension no matter what data
they contain.

### validate_image_file_extension¶

   validate_image_file_extension[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#validate_image_file_extension)[¶](#django.core.validators.validate_image_file_extension)

Uses Pillow to ensure that `value.name` (`value` is a
[File](https://docs.djangoproject.com/en/5.0/files/file/#django.core.files.File)) has [a valid image extension](https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html).

### ProhibitNullCharactersValidator¶

   *class*ProhibitNullCharactersValidator(*message=None*, *code=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#ProhibitNullCharactersValidator)[¶](#django.core.validators.ProhibitNullCharactersValidator)

Raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if `str(value)`
contains one or more null characters (`'\x00'`).

  Parameters:

- **message** – If not `None`, overrides [message](#django.core.validators.ProhibitNullCharactersValidator.message).
- **code** – If not `None`, overrides [code](#django.core.validators.ProhibitNullCharactersValidator.code).

     message[¶](#django.core.validators.ProhibitNullCharactersValidator.message)

The error message used by
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if validation fails.
Defaults to `"Null characters are not allowed."`.

    code[¶](#django.core.validators.ProhibitNullCharactersValidator.code)

The error code used by [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError)
if validation fails. Defaults to `"null_characters_not_allowed"`.

### StepValueValidator¶

   *class*StepValueValidator(*limit_value*, *message=None*, *offset=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/validators/#StepValueValidator)[¶](#django.core.validators.StepValueValidator)

Raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with a code of
`'step_size'` if `value` is not an integral multiple of
`limit_value`, which can be a float, integer or decimal value or a
callable. When `offset` is set, the validation occurs against
`limit_value` plus `offset`. For example, for
`StepValueValidator(3, offset=1.4)` valid values include `1.4`,
`4.4`, `7.4`, `10.4`, and so on.

  Changed in Django 5.0:

The `offset` argument was added.

---

# Built

# Built-in Views¶

Several of Django’s built-in views are documented in
[Writing views](https://docs.djangoproject.com/en/topics/http/views/) as well as elsewhere in the documentation.

## Serving files in development¶

   static.serve(*request*, *path*, *document_root*, *show_indexes=False*)[¶](#django.views.static.serve)

There may be files other than your project’s static assets that, for
convenience, you’d like to have Django serve for you in local development.
The [serve()](#django.views.static.serve) view can be used to serve any directory
you give it. (This view is **not** hardened for production use and should be
used only as a development aid; you should serve these files in production
using a real front-end web server).

The most likely example is user-uploaded content in [MEDIA_ROOT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_ROOT).
`django.contrib.staticfiles` is intended for static assets and has no
built-in handling for user-uploaded files, but you can have Django serve your
[MEDIA_ROOT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_ROOT) by appending something like this to your URLconf:

```
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

# ... the rest of your URLconf goes here ...

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
```

Note, the snippet assumes your [MEDIA_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_URL) has a value of
`'media/'`. This will call the [serve()](#django.views.static.serve) view,
passing in the path from the URLconf and the (required) `document_root`
parameter.

Since it can become a bit cumbersome to define this URL pattern, Django
ships with a small URL helper function [static()](https://docs.djangoproject.com/en/5.0/urls/#django.conf.urls.static.static)
that takes as parameters the prefix such as [MEDIA_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_URL) and a dotted
path to a view, such as `'django.views.static.serve'`. Any other function
parameter will be transparently passed to the view.

## Error views¶

Django comes with a few views by default for handling HTTP errors. To override
these with your own custom views, see [Customizing error views](https://docs.djangoproject.com/en/topics/http/views/#customizing-error-views).

### The 404 (page not found) view¶

   defaults.page_not_found(*request*, *exception*, *template_name='404.html'*)[¶](#django.views.defaults.page_not_found)

When you raise [Http404](https://docs.djangoproject.com/en/topics/http/views/#django.http.Http404) from within a view, Django loads a
special view devoted to handling 404 errors. By default, it’s the view
[django.views.defaults.page_not_found()](#django.views.defaults.page_not_found), which either produces a “Not
Found” message or loads and renders the template `404.html` if you created it
in your root template directory.

The default 404 view will pass two variables to the template: `request_path`,
which is the URL that resulted in the error, and `exception`, which is a
useful representation of the exception that triggered the view (e.g. containing
any message passed to a specific `Http404` instance).

Three things to note about 404 views:

- The 404 view is also called if Django doesn’t find a match after
  checking every regular expression in the URLconf.
- The 404 view is passed a [RequestContext](https://docs.djangoproject.com/en/5.0/templates/api/#django.template.RequestContext) and
  will have access to variables supplied by your template context
  processors (e.g. `MEDIA_URL`).
- If [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) is set to `True` (in your settings module), then
  your 404 view will never be used, and your URLconf will be displayed
  instead, with some debug information.

### The 500 (server error) view¶

   defaults.server_error(*request*, *template_name='500.html'*)[¶](#django.views.defaults.server_error)

Similarly, Django executes special-case behavior in the case of runtime errors
in view code. If a view results in an exception, Django will, by default, call
the view `django.views.defaults.server_error`, which either produces a
“Server Error” message or loads and renders the template `500.html` if you
created it in your root template directory.

The default 500 view passes no variables to the `500.html` template and is
rendered with an empty `Context` to lessen the chance of additional errors.

If [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) is set to `True` (in your settings module), then
your 500 view will never be used, and the traceback will be displayed
instead, with some debug information.

### The 403 (HTTP Forbidden) view¶

   defaults.permission_denied(*request*, *exception*, *template_name='403.html'*)[¶](#django.views.defaults.permission_denied)

In the same vein as the 404 and 500 views, Django has a view to handle 403
Forbidden errors. If a view results in a 403 exception then Django will, by
default, call the view `django.views.defaults.permission_denied`.

This view loads and renders the template `403.html` in your root template
directory, or if this file does not exist, instead serves the text
“403 Forbidden”, as per [RFC 9110 Section 15.5.4](https://datatracker.ietf.org/doc/html/rfc9110.html#section-15.5.4) (the HTTP 1.1
Specification). The template context contains `exception`, which is the
string representation of the exception that triggered the view.

`django.views.defaults.permission_denied` is triggered by a
[PermissionDenied](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.PermissionDenied) exception. To deny access in a
view you can use code like this:

```
from django.core.exceptions import PermissionDenied

def edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    # ...
```

### The 400 (bad request) view¶

   defaults.bad_request(*request*, *exception*, *template_name='400.html'*)[¶](#django.views.defaults.bad_request)

When a [SuspiciousOperation](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.SuspiciousOperation) is raised in Django,
it may be handled by a component of Django (for example resetting the session
data). If not specifically handled, Django will consider the current request a
‘bad request’ instead of a server error.

`django.views.defaults.bad_request`, is otherwise very similar to the
`server_error` view, but returns with the status code 400 indicating that
the error condition was the result of a client operation. By default, nothing
related to the exception that triggered the view is passed to the template
context, as the exception message might contain sensitive information like
filesystem paths.

`bad_request` views are also only used when [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) is `False`.
