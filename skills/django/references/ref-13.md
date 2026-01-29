# Form and field validation¶ and more

# Form and field validation¶

# Form and field validation¶

Form validation happens when the data is cleaned. If you want to customize
this process, there are various places to make changes, each one serving a
different purpose. Three types of cleaning methods are run during form
processing. These are normally executed when you call the `is_valid()`
method on a form. There are other things that can also trigger cleaning and
validation (accessing the `errors` attribute or calling `full_clean()`
directly), but normally they won’t be needed.

In general, any cleaning method can raise `ValidationError` if there is a
problem with the data it is processing, passing the relevant information to
the `ValidationError` constructor. [See below](#raising-validation-error)
for the best practice in raising `ValidationError`. If no `ValidationError`
is raised, the method should return the cleaned (normalized) data as a Python
object.

Most validation can be done using [validators](#validators) - helpers that can be reused.
Validators are functions (or callables) that take a single argument and raise
`ValidationError` on invalid input. Validators are run after the field’s
`to_python` and `validate` methods have been called.

Validation of a form is split into several steps, which can be customized or
overridden:

- The `to_python()` method on a `Field` is the first step in every
  validation. It coerces the value to a correct datatype and raises
  `ValidationError` if that is not possible. This method accepts the raw
  value from the widget and returns the converted value. For example, a
  `FloatField` will turn the data into a Python `float` or raise a
  `ValidationError`.
- The `validate()` method on a `Field` handles field-specific validation
  that is not suitable for a validator. It takes a value that has been
  coerced to a correct datatype and raises `ValidationError` on any error.
  This method does not return anything and shouldn’t alter the value. You
  should override it to handle validation logic that you can’t or don’t
  want to put in a validator.
- The `run_validators()` method on a `Field` runs all of the field’s
  validators and aggregates all the errors into a single
  `ValidationError`. You shouldn’t need to override this method.
- The `clean()` method on a `Field` subclass is responsible for running
  `to_python()`, `validate()`, and `run_validators()` in the correct
  order and propagating their errors. If, at any time, any of the methods
  raise `ValidationError`, the validation stops and that error is raised.
  This method returns the clean data, which is then inserted into the
  `cleaned_data` dictionary of the form.
- The `clean_<fieldname>()` method is called on a form subclass – where
  `<fieldname>` is replaced with the name of the form field attribute.
  This method does any cleaning that is specific to that particular
  attribute, unrelated to the type of field that it is. This method is not
  passed any parameters. You will need to look up the value of the field
  in `self.cleaned_data` and remember that it will be a Python object
  at this point, not the original string submitted in the form (it will be
  in `cleaned_data` because the general field `clean()` method, above,
  has already cleaned the data once).
  For example, if you wanted to validate that the contents of a
  `CharField` called `serialnumber` was unique,
  `clean_serialnumber()` would be the right place to do this. You don’t
  need a specific field (it’s a `CharField`), but you want a
  formfield-specific piece of validation and, possibly, cleaning/normalizing
  the data.
  The return value of this method replaces the existing value in
  `cleaned_data`, so it must be the field’s value from `cleaned_data` (even
  if this method didn’t change it) or a new cleaned value.
- The form subclass’s `clean()` method can perform validation that requires
  access to multiple form fields. This is where you might put in checks such as
  “if field `A` is supplied, field `B` must contain a valid email address”.
  This method can return a completely different dictionary if it wishes, which
  will be used as the `cleaned_data`.
  Since the field validation methods have been run by the time `clean()` is
  called, you also have access to the form’s `errors` attribute which
  contains all the errors raised by cleaning of individual fields.
  Note that any errors raised by your [Form.clean()](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.clean) override will not
  be associated with any field in particular. They go into a special
  “field” (called `__all__`), which you can access via the
  [non_field_errors()](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.non_field_errors) method if you need to. If you
  want to attach errors to a specific field in the form, you need to call
  [add_error()](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.add_error).
  Also note that there are special considerations when overriding
  the `clean()` method of a `ModelForm` subclass. (see the
  [ModelForm documentation](https://docs.djangoproject.com/en/topics/forms/modelforms/#overriding-modelform-clean-method) for more information)

These methods are run in the order given above, one field at a time.  That is,
for each field in the form (in the order they are declared in the form
definition), the `Field.clean()` method (or its override) is run, then
`clean_<fieldname>()`. Finally, once those two methods are run for every
field, the [Form.clean()](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.clean) method, or its override, is executed whether
or not the previous methods have raised errors.

Examples of each of these methods are provided below.

As mentioned, any of these methods can raise a `ValidationError`. For any
field, if the `Field.clean()` method raises a `ValidationError`, any
field-specific cleaning method is not called. However, the cleaning methods
for all remaining fields are still executed.

## RaisingValidationError¶

In order to make error messages flexible and easy to override, consider the
following guidelines:

- Provide a descriptive error `code` to the constructor:
  ```
  # Good
  ValidationError(_("Invalid value"), code="invalid")
  # Bad
  ValidationError(_("Invalid value"))
  ```
- Don’t coerce variables into the message; use placeholders and the `params`
  argument of the constructor:
  ```
  # Good
  ValidationError(
      _("Invalid value: %(value)s"),
      params={"value": "42"},
  )
  # Bad
  ValidationError(_("Invalid value: %s") % value)
  ```
- Use mapping keys instead of positional formatting. This enables putting
  the variables in any order or omitting them altogether when rewriting the
  message:
  ```
  # Good
  ValidationError(
      _("Invalid value: %(value)s"),
      params={"value": "42"},
  )
  # Bad
  ValidationError(
      _("Invalid value: %s"),
      params=("42",),
  )
  ```
- Wrap the message with `gettext` to enable translation:
  ```
  # Good
  ValidationError(_("Invalid value"))
  # Bad
  ValidationError("Invalid value")
  ```

Putting it all together:

```
raise ValidationError(
    _("Invalid value: %(value)s"),
    code="invalid",
    params={"value": "42"},
)
```

Following these guidelines is particularly necessary if you write reusable
forms, form fields, and model fields.

While not recommended, if you are at the end of the validation chain
(i.e. your form `clean()` method) and you know you will *never* need
to override your error message you can still opt for the less verbose:

```
ValidationError(_("Invalid value: %s") % value)
```

The [Form.errors.as_data()](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.errors.as_data) and
[Form.errors.as_json()](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.errors.as_json) methods
greatly benefit from fully featured `ValidationError`s (with a `code` name
and a `params` dictionary).

### Raising multiple errors¶

If you detect multiple errors during a cleaning method and wish to signal all
of them to the form submitter, it is possible to pass a list of errors to the
`ValidationError` constructor.

As above, it is recommended to pass a list of `ValidationError` instances
with `code`s and `params` but a list of strings will also work:

```
# Good
raise ValidationError(
    [
        ValidationError(_("Error 1"), code="error1"),
        ValidationError(_("Error 2"), code="error2"),
    ]
)

# Bad
raise ValidationError(
    [
        _("Error 1"),
        _("Error 2"),
    ]
)
```

## Using validation in practice¶

The previous sections explained how validation works in general for forms.
Since it can sometimes be easier to put things into place by seeing each
feature in use, here are a series of small examples that use each of the
previous features.

### Using validators¶

Django’s form (and model) fields support use of utility functions and classes
known as validators. A validator is a callable object or function that takes a
value and returns nothing if the value is valid or raises a
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if not. These can be passed to a
field’s constructor, via the field’s `validators` argument, or defined on the
[Field](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.Field) class itself with the `default_validators`
attribute.

Validators can be used to validate values inside the field, let’s have a look
at Django’s `SlugField`:

```
from django.core import validators
from django.forms import CharField

class SlugField(CharField):
    default_validators = [validators.validate_slug]
```

As you can see, `SlugField` is a `CharField` with a customized validator
that validates that submitted text obeys to some character rules. This can also
be done on field definition so:

```
slug = forms.SlugField()
```

is equivalent to:

```
slug = forms.CharField(validators=[validators.validate_slug])
```

Common cases such as validating against an email or a regular expression can be
handled using existing validator classes available in Django. For example,
`validators.validate_slug` is an instance of
a [RegexValidator](https://docs.djangoproject.com/en/5.0/validators/#django.core.validators.RegexValidator) constructed with the first
argument being the pattern: `^[-a-zA-Z0-9_]+$`. See the section on
[writing validators](https://docs.djangoproject.com/en/5.0/validators/) to see a list of what is already
available and for an example of how to write a validator.

### Form field default cleaning¶

Let’s first create a custom form field that validates its input is a string
containing comma-separated email addresses. The full class looks like this:

```
from django import forms
from django.core.validators import validate_email

class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(",")

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            validate_email(email)
```

Every form that uses this field will have these methods run before anything
else can be done with the field’s data. This is cleaning that is specific to
this type of field, regardless of how it is subsequently used.

Let’s create a `ContactForm` to demonstrate how you’d use this field:

```
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    recipients = MultiEmailField()
    cc_myself = forms.BooleanField(required=False)
```

Use `MultiEmailField` like any other form field. When the `is_valid()`
method is called on the form, the `MultiEmailField.clean()` method will be
run as part of the cleaning process and it will, in turn, call the custom
`to_python()` and `validate()` methods.

### Cleaning a specific field attribute¶

Continuing on from the previous example, suppose that in our `ContactForm`,
we want to make sure that the `recipients` field always contains the address
`"fred@example.com"`. This is validation that is specific to our form, so we
don’t want to put it into the general `MultiEmailField` class. Instead, we
write a cleaning method that operates on the `recipients` field, like so:

```
from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    # Everything as before.
    ...

    def clean_recipients(self):
        data = self.cleaned_data["recipients"]
        if "fred@example.com" not in data:
            raise ValidationError("You have forgotten about Fred!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
```

### Cleaning and validating fields that depend on each other¶

Suppose we add another requirement to our contact form: if the `cc_myself`
field is `True`, the `subject` must contain the word `"help"`. We are
performing validation on more than one field at a time, so the form’s
[clean()](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.clean) method is a good spot to do this. Notice that we are
talking about the `clean()` method on the form here, whereas earlier we were
writing a `clean()` method on a field. It’s important to keep the field and
form difference clear when working out where to validate things. Fields are
single data points, forms are a collection of fields.

By the time the form’s `clean()` method is called, all the individual field
clean methods will have been run (the previous two sections), so
`self.cleaned_data` will be populated with any data that has survived so
far. So you also need to remember to allow for the fact that the fields you
are wanting to validate might not have survived the initial individual field
checks.

There are two ways to report any errors from this step. Probably the most
common method is to display the error at the top of the form. To create such
an error, you can raise a `ValidationError` from the `clean()` method. For
example:

```
from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    # Everything as before.
    ...

    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise ValidationError(
                    "Did not send for 'help' in the subject despite CC'ing yourself."
                )
```

In this code, if the validation error is raised, the form will display an
error message at the top of the form (normally) describing the problem. Such
errors are non-field errors, which are displayed in the template with
`{{ form.non_field_errors }}`.

The call to `super().clean()` in the example code ensures that any validation
logic in parent classes is maintained. If your form inherits another that
doesn’t return a `cleaned_data` dictionary in its `clean()` method (doing
so is optional), then don’t assign `cleaned_data` to the result of the
`super()` call and use `self.cleaned_data` instead:

```
def clean(self):
    super().clean()
    cc_myself = self.cleaned_data.get("cc_myself")
    ...
```

The second approach for reporting validation errors might involve assigning the
error message to one of the fields. In this case, let’s assign an error message
to both the “subject” and “cc_myself” rows in the form display. Be careful when
doing this in practice, since it can lead to confusing form output. We’re
showing what is possible here and leaving it up to you and your designers to
work out what works effectively in your particular situation. Our new code
(replacing the previous sample) looks like this:

```
from django import forms

class ContactForm(forms.Form):
    # Everything as before.
    ...

    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject and "help" not in subject:
            msg = "Must put 'help' in subject when cc'ing yourself."
            self.add_error("cc_myself", msg)
            self.add_error("subject", msg)
```

The second argument of `add_error()` can be a string, or preferably an
instance of `ValidationError`. See [Raising ValidationError](#raising-validation-error) for more
details. Note that `add_error()` automatically removes the field from
`cleaned_data`.

---

# Widgets¶

# Widgets¶

A widget is Django’s representation of an HTML input element. The widget
handles the rendering of the HTML, and the extraction of data from a GET/POST
dictionary that corresponds to the widget.

The HTML generated by the built-in widgets uses HTML5 syntax, targeting
`<!DOCTYPE html>`. For example, it uses boolean attributes such as `checked`
rather than the XHTML style of `checked='checked'`.

Tip

Widgets should not be confused with the [form fields](https://docs.djangoproject.com/en/5.0/ref/fields/).
Form fields deal with the logic of input validation and are used directly
in templates. Widgets deal with rendering of HTML form input elements on
the web page and extraction of raw submitted data. However, widgets do
need to be [assigned](#widget-to-field) to form fields.

## Specifying widgets¶

Whenever you specify a field on a form, Django will use a default widget
that is appropriate to the type of data that is to be displayed. To find
which widget is used on which field, see the documentation about
[Built-in Field classes](https://docs.djangoproject.com/en/5.0/ref/fields/#built-in-fields).

However, if you want to use a different widget for a field, you can
use the [widget](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.Field.widget) argument on the field definition. For example:

```
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField(widget=forms.Textarea)
```

This would specify a form with a comment that uses a larger [Textarea](#django.forms.Textarea)
widget, rather than the default [TextInput](#django.forms.TextInput) widget.

## Setting arguments for widgets¶

Many widgets have optional extra arguments; they can be set when defining the
widget on the field. In the following example, the
[years](#django.forms.SelectDateWidget.years) attribute is set for a
[SelectDateWidget](#django.forms.SelectDateWidget):

```
from django import forms

BIRTH_YEAR_CHOICES = ["1980", "1981", "1982"]
FAVORITE_COLORS_CHOICES = {
    "blue": "Blue",
    "green": "Green",
    "black": "Black",
}

class SimpleForm(forms.Form):
    birth_year = forms.DateField(
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES)
    )
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )
```

See the [Built-in widgets](#built-in-widgets) for more information about which widgets
are available and which arguments they accept.

## Widgets inheriting from theSelectwidget¶

Widgets inheriting from the [Select](#django.forms.Select) widget deal with choices. They
present the user with a list of options to choose from. The different widgets
present this choice differently; the [Select](#django.forms.Select) widget itself uses a
`<select>` HTML list representation, while [RadioSelect](#django.forms.RadioSelect) uses radio
buttons.

[Select](#django.forms.Select) widgets are used by default on [ChoiceField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.ChoiceField) fields. The
choices displayed on the widget are inherited from the [ChoiceField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.ChoiceField) and
changing [ChoiceField.choices](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.ChoiceField.choices) will update [Select.choices](#django.forms.Select.choices). For
example:

```
>>> from django import forms
>>> CHOICES = {"1": "First", "2": "Second"}
>>> choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
>>> choice_field.choices
[('1', 'First'), ('2', 'Second')]
>>> choice_field.widget.choices
[('1', 'First'), ('2', 'Second')]
>>> choice_field.widget.choices = []
>>> choice_field.choices = [("1", "First and only")]
>>> choice_field.widget.choices
[('1', 'First and only')]
```

Widgets which offer a [choices](#django.forms.Select.choices) attribute can however be used
with fields which are not based on choice – such as a [CharField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.CharField) –
but it is recommended to use a [ChoiceField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.ChoiceField)-based field when the
choices are inherent to the model and not just the representational widget.

## Customizing widget instances¶

When Django renders a widget as HTML, it only renders very minimal markup -
Django doesn’t add class names, or any other widget-specific attributes. This
means, for example, that all [TextInput](#django.forms.TextInput) widgets will appear the same
on your web pages.

There are two ways to customize widgets: [per widget instance](#styling-widget-instances) and [per widget class](#styling-widget-classes).

### Styling widget instances¶

If you want to make one widget instance look different from another, you will
need to specify additional attributes at the time when the widget object is
instantiated and assigned to a form field (and perhaps add some rules to your
CSS files).

For example, take the following form:

```
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField()
```

This form will include three default [TextInput](#django.forms.TextInput) widgets, with default
rendering – no CSS class, no extra attributes. This means that the input boxes
provided for each widget will be rendered exactly the same:

```
>>> f = CommentForm(auto_id=False)
>>> print(f)
<div>Name:<input type="text" name="name" required></div>
<div>Url:<input type="url" name="url" required></div>
<div>Comment:<input type="text" name="comment" required></div>
```

On a real web page, you probably don’t want every widget to look the same. You
might want a larger input element for the comment, and you might want the
‘name’ widget to have some special CSS class. It is also possible to specify
the ‘type’ attribute to take advantage of the new HTML5 input types.  To do
this, you use the [Widget.attrs](#django.forms.Widget.attrs) argument when creating the widget:

```
class CommentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "special"}))
    url = forms.URLField()
    comment = forms.CharField(widget=forms.TextInput(attrs={"size": "40"}))
```

You can also modify a widget in the form definition:

```
class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField()

    name.widget.attrs.update({"class": "special"})
    comment.widget.attrs.update(size="40")
```

Or if the field isn’t declared directly on the form (such as model form fields),
you can use the [Form.fields](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.fields) attribute:

```
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "special"})
        self.fields["comment"].widget.attrs.update(size="40")
```

Django will then include the extra attributes in the rendered output:

```
>>> f = CommentForm(auto_id=False)
>>> print(f)
<div>Name:<input type="text" name="name" class="special" required></div>
<div>Url:<input type="url" name="url" required></div>
<div>Comment:<input type="text" name="comment" size="40" required></div>
```

You can also set the HTML `id` using [attrs](#django.forms.Widget.attrs). See
[BoundField.id_for_label](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.BoundField.id_for_label) for an example.

### Styling widget classes¶

With widgets, it is possible to add assets (`css` and `javascript`)
and more deeply customize their appearance and behavior.

In a nutshell, you will need to subclass the widget and either
[define a “Media” inner class](https://docs.djangoproject.com/en/topics/forms/media/#assets-as-a-static-definition) or
[create a “media” property](https://docs.djangoproject.com/en/topics/forms/media/#dynamic-property).

These methods involve somewhat advanced Python programming and are described in
detail in the [Form Assets](https://docs.djangoproject.com/en/topics/forms/media/) topic guide.

## Base widget classes¶

Base widget classes [Widget](#django.forms.Widget) and [MultiWidget](#django.forms.MultiWidget) are subclassed by
all the [built-in widgets](#built-in-widgets) and may serve as a
foundation for custom widgets.

### Widget¶

   *class*Widget(*attrs=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Widget)[¶](#django.forms.Widget)

This abstract class cannot be rendered, but provides the basic attribute
[attrs](#django.forms.Widget.attrs).  You may also implement or override the
[render()](#django.forms.Widget.render) method on custom widgets.

   attrs[¶](#django.forms.Widget.attrs)

A dictionary containing HTML attributes to be set on the rendered
widget.

```
>>> from django import forms
>>> name = forms.TextInput(attrs={"size": 10, "title": "Your name"})
>>> name.render("name", "A name")
'<input title="Your name" type="text" name="name" value="A name" size="10">'
```

If you assign a value of `True` or `False` to an attribute,
it will be rendered as an HTML5 boolean attribute:

```
>>> name = forms.TextInput(attrs={"required": True})
>>> name.render("name", "A name")
'<input name="name" type="text" value="A name" required>'
>>>
>>> name = forms.TextInput(attrs={"required": False})
>>> name.render("name", "A name")
'<input name="name" type="text" value="A name">'
```

     supports_microseconds[¶](#django.forms.Widget.supports_microseconds)

An attribute that defaults to `True`. If set to `False`, the
microseconds part of [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) and
[time](https://docs.python.org/3/library/datetime.html#datetime.time) values will be set to `0`.

    format_value(*value*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Widget.format_value)[¶](#django.forms.Widget.format_value)

Cleans and returns a value for use in the widget template. `value`
isn’t guaranteed to be valid input, therefore subclass implementations
should program defensively.

    get_context(*name*, *value*, *attrs*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Widget.get_context)[¶](#django.forms.Widget.get_context)

Returns a dictionary of values to use when rendering the widget
template. By default, the dictionary contains a single key,
`'widget'`, which is a dictionary representation of the widget
containing the following keys:

- `'name'`: The name of the field from the `name` argument.
- `'is_hidden'`: A boolean indicating whether or not this widget is
  hidden.
- `'required'`: A boolean indicating whether or not the field for
  this widget is required.
- `'value'`: The value as returned by [format_value()](#django.forms.Widget.format_value).
- `'attrs'`: HTML attributes to be set on the rendered widget. The
  combination of the [attrs](#django.forms.Widget.attrs) attribute and the `attrs` argument.
- `'template_name'`: The value of `self.template_name`.

`Widget` subclasses can provide custom context values by overriding
this method.

    id_for_label(*id_*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Widget.id_for_label)[¶](#django.forms.Widget.id_for_label)

Returns the HTML ID attribute of this widget for use by a `<label>`,
given the ID of the field. Returns an empty string if an ID isn’t
available.

This hook is necessary because some widgets have multiple HTML
elements and, thus, multiple IDs. In that case, this method should
return an ID value that corresponds to the first ID in the widget’s
tags.

    render(*name*, *value*, *attrs=None*, *renderer=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Widget.render)[¶](#django.forms.Widget.render)

Renders a widget to HTML using the given renderer. If `renderer` is
`None`, the renderer from the [FORM_RENDERER](https://docs.djangoproject.com/en/5.0/settings/#std-setting-FORM_RENDERER) setting is
used.

    value_from_datadict(*data*, *files*, *name*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Widget.value_from_datadict)[¶](#django.forms.Widget.value_from_datadict)

Given a dictionary of data and this widget’s name, returns the value
of this widget. `files` may contain data coming from
[request.FILES](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest.FILES). Returns `None`
if a value wasn’t provided. Note also that `value_from_datadict` may
be called more than once during handling of form data, so if you
customize it and add expensive processing, you should implement some
caching mechanism yourself.

    value_omitted_from_data(*data*, *files*, *name*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Widget.value_omitted_from_data)[¶](#django.forms.Widget.value_omitted_from_data)

Given `data` and `files` dictionaries and this widget’s name,
returns whether or not there’s data or files for the widget.

The method’s result affects whether or not a field in a model form
[falls back to its default](https://docs.djangoproject.com/en/topics/forms/modelforms/#topics-modelform-save).

Special cases are [CheckboxInput](#django.forms.CheckboxInput),
[CheckboxSelectMultiple](#django.forms.CheckboxSelectMultiple), and
[SelectMultiple](#django.forms.SelectMultiple), which always return
`False` because an unchecked checkbox and unselected
`<select multiple>` don’t appear in the data of an HTML form
submission, so it’s unknown whether or not the user submitted a value.

    use_fieldset[¶](#django.forms.Widget.use_fieldset)

An attribute to identify if the widget should be grouped in a
`<fieldset>` with a `<legend>` when rendered. Defaults to `False`
but is `True` when the widget contains multiple `<input>` tags such as
[CheckboxSelectMultiple](#django.forms.CheckboxSelectMultiple),
[RadioSelect](#django.forms.RadioSelect),
[MultiWidget](#django.forms.MultiWidget),
[SplitDateTimeWidget](#django.forms.SplitDateTimeWidget), and
[SelectDateWidget](#django.forms.SelectDateWidget).

    use_required_attribute(*initial*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Widget.use_required_attribute)[¶](#django.forms.Widget.use_required_attribute)

Given a form field’s `initial` value, returns whether or not the
widget can be rendered with the `required` HTML attribute. Forms use
this method along with [Field.required](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.Field.required) and [Form.use_required_attribute](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.Form.use_required_attribute) to determine whether or not
to display the `required` attribute for each field.

By default, returns `False` for hidden widgets and `True`
otherwise. Special cases are [FileInput](#django.forms.FileInput) and
[ClearableFileInput](#django.forms.ClearableFileInput), which return `False` when
`initial` is set, and [CheckboxSelectMultiple](#django.forms.CheckboxSelectMultiple),
which always returns `False` because browser validation would require
all checkboxes to be checked instead of at least one.

Override this method in custom widgets that aren’t compatible with
browser validation. For example, a WSYSIWG text editor widget backed by
a hidden `textarea` element may want to always return `False` to
avoid browser validation on the hidden field.

### MultiWidget¶

   *class*MultiWidget(*widgets*, *attrs=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#MultiWidget)[¶](#django.forms.MultiWidget)

A widget that is composed of multiple widgets.
[MultiWidget](#django.forms.MultiWidget) works hand in hand with the
[MultiValueField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.MultiValueField).

[MultiWidget](#django.forms.MultiWidget) has one required argument:

   widgets[¶](#django.forms.MultiWidget.widgets)

An iterable containing the widgets needed. For example:

```
>>> from django.forms import MultiWidget, TextInput
>>> widget = MultiWidget(widgets=[TextInput, TextInput])
>>> widget.render("name", ["john", "paul"])
'<input type="text" name="name_0" value="john"><input type="text" name="name_1" value="paul">'
```

You may provide a dictionary in order to specify custom suffixes for
the `name` attribute on each subwidget. In this case, for each
`(key, widget)` pair, the key will be appended to the `name` of the
widget in order to generate the attribute value. You may provide the
empty string (`''`) for a single key, in order to suppress the suffix
for one widget. For example:

```
>>> widget = MultiWidget(widgets={"": TextInput, "last": TextInput})
>>> widget.render("name", ["john", "paul"])
'<input type="text" name="name" value="john"><input type="text" name="name_last" value="paul">'
```

And one required method:

   decompress(*value*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#MultiWidget.decompress)[¶](#django.forms.MultiWidget.decompress)

This method takes a single “compressed” value from the field and
returns a list of “decompressed” values. The input value can be
assumed valid, but not necessarily non-empty.

This method **must be implemented** by the subclass, and since the
value may be empty, the implementation must be defensive.

The rationale behind “decompression” is that it is necessary to “split”
the combined value of the form field into the values for each widget.

An example of this is how [SplitDateTimeWidget](#django.forms.SplitDateTimeWidget) turns a
[datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) value into a list with date and time split
into two separate values:

```
from django.forms import MultiWidget

class SplitDateTimeWidget(MultiWidget):
    # ...

    def decompress(self, value):
        if value:
            return [value.date(), value.time()]
        return [None, None]
```

Tip

Note that [MultiValueField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.MultiValueField) has a
complementary method [compress()](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.MultiValueField.compress)
with the opposite responsibility - to combine cleaned values of
all member fields into one.

It provides some custom context:

   get_context(*name*, *value*, *attrs*)[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#MultiWidget.get_context)[¶](#django.forms.MultiWidget.get_context)

In addition to the `'widget'` key described in
[Widget.get_context()](#django.forms.Widget.get_context), `MultiWidget` adds a
`widget['subwidgets']` key.

These can be looped over in the widget template:

```
{% for subwidget in widget.subwidgets %}
    {% include subwidget.template_name with widget=subwidget %}
{% endfor %}
```

Here’s an example widget which subclasses [MultiWidget](#django.forms.MultiWidget) to display
a date with the day, month, and year in different select boxes. This widget
is intended to be used with a [DateField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.DateField) rather than
a [MultiValueField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.MultiValueField), thus we have implemented
[value_from_datadict()](#django.forms.Widget.value_from_datadict):

```
from datetime import date
from django import forms

class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = {day: day for day in range(1, 32)}
        months = {month: month for month in range(1, 13)}
        years = {year: year for year in [2018, 2019, 2020]}
        widgets = [
            forms.Select(attrs=attrs, choices=days),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split("-")
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return "{}-{}-{}".format(year, month, day)
```

The constructor creates several [Select](#django.forms.Select) widgets in a list. The
`super()` method uses this list to set up the widget.

The required method [decompress()](#django.forms.MultiWidget.decompress) breaks up a
`datetime.date` value into the day, month, and year values corresponding
to each widget. If an invalid date was selected, such as the non-existent
30th February, the [DateField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.DateField) passes this method a
string instead, so that needs parsing. The final `return` handles when
`value` is `None`, meaning we don’t have any defaults for our
subwidgets.

The default implementation of [value_from_datadict()](#django.forms.Widget.value_from_datadict) returns a
list of values corresponding to each `Widget`. This is appropriate when
using a `MultiWidget` with a [MultiValueField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.MultiValueField). But
since we want to use this widget with a [DateField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.DateField),
which takes a single value, we have overridden this method. The
implementation here combines the data from the subwidgets into a string in
the format that [DateField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.DateField) expects.

## Built-in widgets¶

Django provides a representation of all the basic HTML widgets, plus some
commonly used groups of widgets in the `django.forms.widgets` module,
including [the input of text](#text-widgets), [various checkboxes
and selectors](#selector-widgets), [uploading files](#file-upload-widgets),
and [handling of multi-valued input](#composite-widgets).

### Widgets handling input of text¶

These widgets make use of the HTML elements `input` and `textarea`.

#### TextInput¶

   *class*TextInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#TextInput)[¶](#django.forms.TextInput)

- `input_type`: `'text'`
- `template_name`: `'django/forms/widgets/text.html'`
- Renders as: `<input type="text" ...>`

#### NumberInput¶

   *class*NumberInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#NumberInput)[¶](#django.forms.NumberInput)

- `input_type`: `'number'`
- `template_name`: `'django/forms/widgets/number.html'`
- Renders as: `<input type="number" ...>`

Beware that not all browsers support entering localized numbers in
`number` input types. Django itself avoids using them for fields having
their [localize](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.Field.localize) property set to `True`.

#### EmailInput¶

   *class*EmailInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#EmailInput)[¶](#django.forms.EmailInput)

- `input_type`: `'email'`
- `template_name`: `'django/forms/widgets/email.html'`
- Renders as: `<input type="email" ...>`

#### URLInput¶

   *class*URLInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#URLInput)[¶](#django.forms.URLInput)

- `input_type`: `'url'`
- `template_name`: `'django/forms/widgets/url.html'`
- Renders as: `<input type="url" ...>`

#### PasswordInput¶

   *class*PasswordInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#PasswordInput)[¶](#django.forms.PasswordInput)

- `input_type`: `'password'`
- `template_name`: `'django/forms/widgets/password.html'`
- Renders as: `<input type="password" ...>`

Takes one optional argument:

   render_value[¶](#django.forms.PasswordInput.render_value)

Determines whether the widget will have a value filled in when the
form is re-displayed after a validation error (default is `False`).

#### HiddenInput¶

   *class*HiddenInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#HiddenInput)[¶](#django.forms.HiddenInput)

- `input_type`: `'hidden'`
- `template_name`: `'django/forms/widgets/hidden.html'`
- Renders as: `<input type="hidden" ...>`

Note that there also is a [MultipleHiddenInput](#django.forms.MultipleHiddenInput) widget that
encapsulates a set of hidden input elements.

#### DateInput¶

   *class*DateInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#DateInput)[¶](#django.forms.DateInput)

- `input_type`: `'text'`
- `template_name`: `'django/forms/widgets/date.html'`
- Renders as: `<input type="text" ...>`

Takes same arguments as [TextInput](#django.forms.TextInput), with one more optional argument:

   format[¶](#django.forms.DateInput.format)

The format in which this field’s initial value will be displayed.

If no `format` argument is provided, the default format is the first
format found in [DATE_INPUT_FORMATS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DATE_INPUT_FORMATS) and respects
[Format localization](https://docs.djangoproject.com/en/topics/i18n/formatting/). `%U`, `%W`, and `%j` formats are not
supported by this widget.

#### DateTimeInput¶

   *class*DateTimeInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#DateTimeInput)[¶](#django.forms.DateTimeInput)

- `input_type`: `'text'`
- `template_name`: `'django/forms/widgets/datetime.html'`
- Renders as: `<input type="text" ...>`

Takes same arguments as [TextInput](#django.forms.TextInput), with one more optional argument:

   format[¶](#django.forms.DateTimeInput.format)

The format in which this field’s initial value will be displayed.

If no `format` argument is provided, the default format is the first
format found in [DATETIME_INPUT_FORMATS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DATETIME_INPUT_FORMATS) and respects
[Format localization](https://docs.djangoproject.com/en/topics/i18n/formatting/). `%U`, `%W`, and `%j` formats are not
supported by this widget.

By default, the microseconds part of the time value is always set to `0`.
If microseconds are required, use a subclass with the
[supports_microseconds](#django.forms.Widget.supports_microseconds) attribute set to `True`.

#### TimeInput¶

   *class*TimeInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#TimeInput)[¶](#django.forms.TimeInput)

- `input_type`: `'text'`
- `template_name`: `'django/forms/widgets/time.html'`
- Renders as: `<input type="text" ...>`

Takes same arguments as [TextInput](#django.forms.TextInput), with one more optional argument:

   format[¶](#django.forms.TimeInput.format)

The format in which this field’s initial value will be displayed.

If no `format` argument is provided, the default format is the first
format found in [TIME_INPUT_FORMATS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TIME_INPUT_FORMATS) and respects
[Format localization](https://docs.djangoproject.com/en/topics/i18n/formatting/).

For the treatment of microseconds, see [DateTimeInput](#django.forms.DateTimeInput).

#### Textarea¶

   *class*Textarea[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Textarea)[¶](#django.forms.Textarea)

- `template_name`: `'django/forms/widgets/textarea.html'`
- Renders as: `<textarea>...</textarea>`

### Selector and checkbox widgets¶

These widgets make use of the HTML elements `<select>`,
`<input type="checkbox">`, and `<input type="radio">`.

Widgets that render multiple choices have an `option_template_name` attribute
that specifies the template used to render each choice. For example, for the
[Select](#django.forms.Select) widget, `select_option.html` renders the `<option>` for a
`<select>`.

#### CheckboxInput¶

   *class*CheckboxInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#CheckboxInput)[¶](#django.forms.CheckboxInput)

- `input_type`: `'checkbox'`
- `template_name`: `'django/forms/widgets/checkbox.html'`
- Renders as: `<input type="checkbox" ...>`

Takes one optional argument:

   check_test[¶](#django.forms.CheckboxInput.check_test)

A callable that takes the value of the `CheckboxInput` and returns
`True` if the checkbox should be checked for that value.

#### Select¶

   *class*Select[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#Select)[¶](#django.forms.Select)

- `template_name`: `'django/forms/widgets/select.html'`
- `option_template_name`: `'django/forms/widgets/select_option.html'`
- Renders as: `<select><option ...>...</select>`

   choices[¶](#django.forms.Select.choices)

This attribute is optional when the form field does not have a
`choices` attribute. If it does, it will override anything you set
here when the attribute is updated on the [Field](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.Field).

#### NullBooleanSelect¶

   *class*NullBooleanSelect[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#NullBooleanSelect)[¶](#django.forms.NullBooleanSelect)

- `template_name`: `'django/forms/widgets/select.html'`
- `option_template_name`: `'django/forms/widgets/select_option.html'`

Select widget with options ‘Unknown’, ‘Yes’ and ‘No’

#### SelectMultiple¶

   *class*SelectMultiple[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#SelectMultiple)[¶](#django.forms.SelectMultiple)

- `template_name`: `'django/forms/widgets/select.html'`
- `option_template_name`: `'django/forms/widgets/select_option.html'`

Similar to [Select](#django.forms.Select), but allows multiple selection:
`<select multiple>...</select>`

#### RadioSelect¶

   *class*RadioSelect[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#RadioSelect)[¶](#django.forms.RadioSelect)

- `template_name`: `'django/forms/widgets/radio.html'`
- `option_template_name`: `'django/forms/widgets/radio_option.html'`

Similar to [Select](#django.forms.Select), but rendered as a list of radio buttons within
`<div>` tags:

```
<div>
  <div><input type="radio" name="..."></div>
  ...
</div>
```

For more granular control over the generated markup, you can loop over the
radio buttons in the template. Assuming a form `myform` with a field
`beatles` that uses a `RadioSelect` as its widget:

```
<fieldset>
    <legend>{{ myform.beatles.label }}</legend>
    {% for radio in myform.beatles %}
    <div class="myradio">
        {{ radio }}
    </div>
    {% endfor %}
</fieldset>
```

This would generate the following HTML:

```
<fieldset>
    <legend>Radio buttons</legend>
    <div class="myradio">
        <label for="id_beatles_0"><input id="id_beatles_0" name="beatles" type="radio" value="john" required> John</label>
    </div>
    <div class="myradio">
        <label for="id_beatles_1"><input id="id_beatles_1" name="beatles" type="radio" value="paul" required> Paul</label>
    </div>
    <div class="myradio">
        <label for="id_beatles_2"><input id="id_beatles_2" name="beatles" type="radio" value="george" required> George</label>
    </div>
    <div class="myradio">
        <label for="id_beatles_3"><input id="id_beatles_3" name="beatles" type="radio" value="ringo" required> Ringo</label>
    </div>
</fieldset>
```

That included the `<label>` tags. To get more granular, you can use each
radio button’s `tag`, `choice_label` and `id_for_label` attributes.
For example, this template…

```
<fieldset>
    <legend>{{ myform.beatles.label }}</legend>
    {% for radio in myform.beatles %}
    <label for="{{ radio.id_for_label }}">
        {{ radio.choice_label }}
        <span class="radio">{{ radio.tag }}</span>
    </label>
    {% endfor %}
</fieldset>
```

…will result in the following HTML:

```
<fieldset>
    <legend>Radio buttons</legend>
    <label for="id_beatles_0">
        John
        <span class="radio"><input id="id_beatles_0" name="beatles" type="radio" value="john" required></span>
    </label>
    <label for="id_beatles_1">
        Paul
        <span class="radio"><input id="id_beatles_1" name="beatles" type="radio" value="paul" required></span>
    </label>
    <label for="id_beatles_2">
        George
        <span class="radio"><input id="id_beatles_2" name="beatles" type="radio" value="george" required></span>
    </label>
    <label for="id_beatles_3">
        Ringo
        <span class="radio"><input id="id_beatles_3" name="beatles" type="radio" value="ringo" required></span>
    </label>
</fieldset>
```

If you decide not to loop over the radio buttons – e.g., if your template
includes `{{ myform.beatles }}` – they’ll be output in a `<div>` with
`<div>` tags, as above.

The outer `<div>` container receives the `id` attribute of the widget,
if defined, or [BoundField.auto_id](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.BoundField.auto_id) otherwise.

When looping over the radio buttons, the `label` and `input` tags include
`for` and `id` attributes, respectively. Each radio button has an
`id_for_label` attribute to output the element’s ID.

#### CheckboxSelectMultiple¶

   *class*CheckboxSelectMultiple[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#CheckboxSelectMultiple)[¶](#django.forms.CheckboxSelectMultiple)

- `template_name`: `'django/forms/widgets/checkbox_select.html'`
- `option_template_name`: `'django/forms/widgets/checkbox_option.html'`

Similar to [SelectMultiple](#django.forms.SelectMultiple), but rendered as a list of checkboxes:

```
<div>
  <div><input type="checkbox" name="..." ></div>
  ...
</div>
```

The outer `<div>` container receives the `id` attribute of the widget,
if defined, or [BoundField.auto_id](https://docs.djangoproject.com/en/5.0/ref/api/#django.forms.BoundField.auto_id) otherwise.

Like [RadioSelect](#django.forms.RadioSelect), you can loop over the individual checkboxes for the
widget’s choices. Unlike [RadioSelect](#django.forms.RadioSelect), the checkboxes won’t include the
`required` HTML attribute if the field is required because browser validation
would require all checkboxes to be checked instead of at least one.

When looping over the checkboxes, the `label` and `input` tags include
`for` and `id` attributes, respectively. Each checkbox has an
`id_for_label` attribute to output the element’s ID.

### File upload widgets¶

#### FileInput¶

   *class*FileInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#FileInput)[¶](#django.forms.FileInput)

- `template_name`: `'django/forms/widgets/file.html'`
- Renders as: `<input type="file" ...>`

#### ClearableFileInput¶

   *class*ClearableFileInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#ClearableFileInput)[¶](#django.forms.ClearableFileInput)

- `template_name`: `'django/forms/widgets/clearable_file_input.html'`
- Renders as: `<input type="file" ...>` with an additional checkbox
  input to clear the field’s value, if the field is not required and has
  initial data.

### Composite widgets¶

#### MultipleHiddenInput¶

   *class*MultipleHiddenInput[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#MultipleHiddenInput)[¶](#django.forms.MultipleHiddenInput)

- `template_name`: `'django/forms/widgets/multiple_hidden.html'`
- Renders as: multiple `<input type="hidden" ...>` tags

A widget that handles multiple hidden widgets for fields that have a list
of values.

#### SplitDateTimeWidget¶

   *class*SplitDateTimeWidget[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#SplitDateTimeWidget)[¶](#django.forms.SplitDateTimeWidget)

- `template_name`: `'django/forms/widgets/splitdatetime.html'`

Wrapper (using [MultiWidget](#django.forms.MultiWidget)) around two widgets: [DateInput](#django.forms.DateInput)
for the date, and [TimeInput](#django.forms.TimeInput) for the time. Must be used with
[SplitDateTimeField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.SplitDateTimeField) rather than [DateTimeField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.DateTimeField).

`SplitDateTimeWidget` has several optional arguments:

   date_format[¶](#django.forms.SplitDateTimeWidget.date_format)

Similar to [DateInput.format](#django.forms.DateInput.format)

    time_format[¶](#django.forms.SplitDateTimeWidget.time_format)

Similar to [TimeInput.format](#django.forms.TimeInput.format)

    date_attrs[¶](#django.forms.SplitDateTimeWidget.date_attrs)    time_attrs[¶](#django.forms.SplitDateTimeWidget.time_attrs)

Similar to [Widget.attrs](#django.forms.Widget.attrs). A dictionary containing HTML
attributes to be set on the rendered [DateInput](#django.forms.DateInput) and
[TimeInput](#django.forms.TimeInput) widgets, respectively. If these attributes aren’t
set, [Widget.attrs](#django.forms.Widget.attrs) is used instead.

#### SplitHiddenDateTimeWidget¶

   *class*SplitHiddenDateTimeWidget[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#SplitHiddenDateTimeWidget)[¶](#django.forms.SplitHiddenDateTimeWidget)

- `template_name`: `'django/forms/widgets/splithiddendatetime.html'`

Similar to [SplitDateTimeWidget](#django.forms.SplitDateTimeWidget), but uses [HiddenInput](#django.forms.HiddenInput) for
both date and time.

#### SelectDateWidget¶

   *class*SelectDateWidget[[source]](https://docs.djangoproject.com/en/_modules/django/forms/widgets/#SelectDateWidget)[¶](#django.forms.SelectDateWidget)

- `template_name`: `'django/forms/widgets/select_date.html'`

Wrapper around three [Select](#django.forms.Select) widgets: one each for
month, day, and year.

Takes several optional arguments:

   years[¶](#django.forms.SelectDateWidget.years)

An optional list/tuple of years to use in the “year” select box.
The default is a list containing the current year and the next 9 years.

    months[¶](#django.forms.SelectDateWidget.months)

An optional dict of months to use in the “months” select box.

The keys of the dict correspond to the month number (1-indexed) and
the values are the displayed months:

```
MONTHS = {
    1: _("jan"),
    2: _("feb"),
    3: _("mar"),
    4: _("apr"),
    5: _("may"),
    6: _("jun"),
    7: _("jul"),
    8: _("aug"),
    9: _("sep"),
    10: _("oct"),
    11: _("nov"),
    12: _("dec"),
}
```

     empty_label[¶](#django.forms.SelectDateWidget.empty_label)

If the [DateField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.forms.DateField) is not required,
[SelectDateWidget](#django.forms.SelectDateWidget) will have an empty choice at the top of the
list (which is `---` by default). You can change the text of this
label with the `empty_label` attribute. `empty_label` can be a
`string`, `list`, or `tuple`. When a string is used, all select
boxes will each have an empty choice with this label. If `empty_label`
is a `list` or `tuple` of 3 string elements, the select boxes will
have their own custom label. The labels should be in this order
`('year_label', 'month_label', 'day_label')`.

```
# A custom empty label with string
field1 = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))

# A custom empty label with tuple
field1 = forms.DateField(
    widget=SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ),
)
```
