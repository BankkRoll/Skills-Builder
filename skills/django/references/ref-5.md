# The flatpages app¶ and more

# The flatpages app¶

# The flatpages app¶

Django comes with an optional “flatpages” application. It lets you store “flat”
HTML content in a database and handles the management for you via Django’s
admin interface and a Python API.

A flatpage is an object with a URL, title and content. Use it for one-off,
special-case pages, such as “About” or “Privacy Policy” pages, that you want to
store in a database but for which you don’t want to develop a custom Django
application.

A flatpage can use a custom template or a default, systemwide flatpage
template. It can be associated with one, or multiple, sites.

The content field may optionally be left blank if you prefer to put your
content in a custom template.

## Installation¶

To install the flatpages app, follow these steps:

1. Install the [sitesframework](https://docs.djangoproject.com/en/5.0/ref/sites/#module-django.contrib.sites) by adding
  `'django.contrib.sites'` to your [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting,
  if it’s not already in there.
  Also make sure you’ve correctly set [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) to the ID of the
  site the settings file represents. This will usually be `1` (i.e.
  `SITE_ID = 1`, but if you’re using the sites framework to manage
  multiple sites, it could be the ID of a different site.
2. Add `'django.contrib.flatpages'` to your [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS)
  setting.

Then either:

1. Add an entry in your URLconf. For example:
  ```
  urlpatterns = [
      path("pages/", include("django.contrib.flatpages.urls")),
  ]
  ```

or:

1. Add `'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'`
  to your [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE) setting.
2. Run the command [manage.pymigrate](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-migrate).

## How it works¶

`manage.py migrate` creates two tables in your database: `django_flatpage`
and `django_flatpage_sites`. `django_flatpage` is a lookup table that maps
a URL to a title and bunch of text content. `django_flatpage_sites`
associates a flatpage with a site.

### Using the URLconf¶

There are several ways to include the flat pages in your URLconf. You can
dedicate a particular path to flat pages:

```
urlpatterns = [
    path("pages/", include("django.contrib.flatpages.urls")),
]
```

You can also set it up as a “catchall” pattern. In this case, it is important
to place the pattern at the end of the other urlpatterns:

```
from django.contrib.flatpages import views

# Your other patterns here
urlpatterns += [
    re_path(r"^(?P<url>.*/)$", views.flatpage),
]
```

Warning

If you set [APPEND_SLASH](https://docs.djangoproject.com/en/5.0/settings/#std-setting-APPEND_SLASH) to `False`, you must remove the slash
in the catchall pattern or flatpages without a trailing slash will not be
matched.

Another common setup is to use flat pages for a limited set of known pages and
to hard code the urls, so you can reference them with the [url](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatetag-url) template
tag:

```
from django.contrib.flatpages import views

urlpatterns += [
    path("about-us/", views.flatpage, {"url": "/about-us/"}, name="about"),
    path("license/", views.flatpage, {"url": "/license/"}, name="license"),
]
```

### Using the middleware¶

The [FlatpageFallbackMiddleware](#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware)
can do all of the work.

   *class*FlatpageFallbackMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/flatpages/middleware/#FlatpageFallbackMiddleware)[¶](#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware)

Each time any Django application raises a 404 error, this middleware
checks the flatpages database for the requested URL as a last resort.
Specifically, it checks for a flatpage with the given URL with a site ID
that corresponds to the [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) setting.

If it finds a match, it follows this algorithm:

- If the flatpage has a custom template, it loads that template.
  Otherwise, it loads the template `flatpages/default.html`.
- It passes that template a single context variable, `flatpage`,
  which is the flatpage object. It uses
  [RequestContext](https://docs.djangoproject.com/en/5.0/templates/api/#django.template.RequestContext) in rendering the
  template.

The middleware will only add a trailing slash and redirect (by looking
at the [APPEND_SLASH](https://docs.djangoproject.com/en/5.0/settings/#std-setting-APPEND_SLASH) setting) if the resulting URL refers to
a valid flatpage. Redirects are permanent (301 status code).

If it doesn’t find a match, the request continues to be processed as usual.

The middleware only gets activated for 404s – not for 500s or responses
of any other status code.

Flatpages will not apply view middleware

Because the `FlatpageFallbackMiddleware` is applied only after
URL resolution has failed and produced a 404, the response it
returns will not apply any [view middleware](https://docs.djangoproject.com/en/topics/http/middleware/#view-middleware)
methods. Only requests which are successfully routed to a view via
normal URL resolution apply view middleware.

Note that the order of [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE) matters. Generally, you can put
[FlatpageFallbackMiddleware](#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware) at the
end of the list. This means it will run first when processing the response, and
ensures that any other response-processing middleware see the real flatpage
response rather than the 404.

For more on middleware, read the [middleware docs](https://docs.djangoproject.com/en/topics/http/middleware/).

Ensure that your 404 template works

Note that the
[FlatpageFallbackMiddleware](#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware)
only steps in once another view has successfully produced a 404 response.
If another view or middleware class attempts to produce a 404 but ends up
raising an exception instead, the response will become an HTTP 500
(“Internal Server Error”) and the
[FlatpageFallbackMiddleware](#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware)
will not attempt to serve a flat page.

## How to add, change and delete flatpages¶

Warning

Permissions to add or edit flatpages should be restricted to trusted users.
Flatpages are defined by raw HTML and are **not sanitized** by Django. As a
consequence, a malicious flatpage can lead to various security
vulnerabilities, including permission escalation.

### Via the admin interface¶

If you’ve activated the automatic Django admin interface, you should see a
“Flatpages” section on the admin index page. Edit flatpages as you edit any
other object in the system.

The `FlatPage` model has an `enable_comments` field that isn’t used by
`contrib.flatpages`, but that could be useful for your project or third-party
apps. It doesn’t appear in the admin interface, but you can add it by
registering a custom `ModelAdmin` for `FlatPage`:

```
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = [
        (None, {"fields": ["url", "title", "content", "sites"]}),
        (
            _("Advanced options"),
            {
                "classes": ["collapse"],
                "fields": [
                    "enable_comments",
                    "registration_required",
                    "template_name",
                ],
            },
        ),
    ]

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
```

### Via the Python API¶

   *class*FlatPage[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/flatpages/models/#FlatPage)[¶](#django.contrib.flatpages.models.FlatPage)

Flatpages are represented by a standard
[Django model](https://docs.djangoproject.com/en/topics/db/models/),
which lives in [django/contrib/flatpages/models.py](https://github.com/django/django/blob/main/django/contrib/flatpages/models.py). You can access
flatpage objects via the [Django database API](https://docs.djangoproject.com/en/topics/db/queries/).

Check for duplicate flatpage URLs.

If you add or modify flatpages via your own code, you will likely want to
check for duplicate flatpage URLs within the same site. The flatpage form
used in the admin performs this validation check, and can be imported from
`django.contrib.flatpages.forms.FlatpageForm` and used in your own
views.

## Flatpage templates¶

By default, flatpages are rendered via the template
`flatpages/default.html`, but you can override that for a
particular flatpage: in the admin, a collapsed fieldset titled
“Advanced options” (clicking will expand it) contains a field for
specifying a template name. If you’re creating a flat page via the
Python API you can set the template name as the field `template_name` on the
`FlatPage` object.

Creating the `flatpages/default.html` template is your responsibility;
in your template directory, create a `flatpages` directory containing a
file `default.html`.

Flatpage templates are passed a single context variable, `flatpage`,
which is the flatpage object.

Here’s a sample `flatpages/default.html` template:

```
<!DOCTYPE html>
<html>
<head>
<title>{{ flatpage.title }}</title>
</head>
<body>
{{ flatpage.content }}
</body>
</html>
```

Since you’re already entering raw HTML into the admin page for a flatpage,
both `flatpage.title` and `flatpage.content` are marked as **not**
requiring [automatic HTML escaping](https://docs.djangoproject.com/en/5.0/templates/language/#automatic-html-escaping) in the
template.

## Getting a list ofFlatPageobjects in your templates¶

The flatpages app provides a template tag that allows you to iterate
over all of the available flatpages on the [current site](https://docs.djangoproject.com/en/5.0/ref/sites/#hooking-into-current-site-from-views).

Like all custom template tags, you’ll need to [load its custom
tag library](https://docs.djangoproject.com/en/5.0/templates/language/#loading-custom-template-libraries) before you can use
it. After loading the library, you can retrieve all current flatpages
via the [get_flatpages](#std-templatetag-get_flatpages) tag:

```
{% load flatpages %}
{% get_flatpages as flatpages %}
<ul>
    {% for page in flatpages %}
        <li><a href="{{ page.url }}">{{ page.title }}</a></li>
    {% endfor %}
</ul>
```

### Displayingregistration_requiredflatpages¶

By default, the [get_flatpages](#std-templatetag-get_flatpages) template tag will only show
flatpages that are marked `registration_required = False`. If you
want to display registration-protected flatpages, you need to specify
an authenticated user using a `for` clause.

For example:

```
{% get_flatpages for someuser as about_pages %}
```

If you provide an anonymous user, [get_flatpages](#std-templatetag-get_flatpages) will behave
the same as if you hadn’t provided a user – i.e., it will only show you
public flatpages.

### Limiting flatpages by base URL¶

An optional argument, `starts_with`, can be applied to limit the
returned pages to those beginning with a particular base URL. This
argument may be passed as a string, or as a variable to be resolved
from the context.

For example:

```
{% get_flatpages '/about/' as about_pages %}
{% get_flatpages about_prefix as about_pages %}
{% get_flatpages '/about/' for someuser as about_pages %}
```

## Integrating withdjango.contrib.sitemaps¶

   *class*FlatPageSitemap[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/flatpages/sitemaps/#FlatPageSitemap)[¶](#django.contrib.flatpages.sitemaps.FlatPageSitemap)

The [sitemaps.FlatPageSitemap](#django.contrib.flatpages.sitemaps.FlatPageSitemap) class looks at all
publicly visible [flatpages](#module-django.contrib.flatpages) defined for the current
[SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) (see the [sitesdocumentation](https://docs.djangoproject.com/en/5.0/ref/sites/#module-django.contrib.sites)) and creates an entry in the sitemap. These entries
include only the [location](https://docs.djangoproject.com/en/5.0/ref/sitemaps/#django.contrib.sitemaps.Sitemap.location)
attribute – not [lastmod](https://docs.djangoproject.com/en/5.0/ref/sitemaps/#django.contrib.sitemaps.Sitemap.lastmod),
[changefreq](https://docs.djangoproject.com/en/5.0/ref/sitemaps/#django.contrib.sitemaps.Sitemap.changefreq) or
[priority](https://docs.djangoproject.com/en/5.0/ref/sitemaps/#django.contrib.sitemaps.Sitemap.priority).

### Example¶

Here’s an example of a URLconf using [FlatPageSitemap](#django.contrib.flatpages.sitemaps.FlatPageSitemap):

```
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

urlpatterns = [
    # ...
    # the sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"flatpages": FlatPageSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
```

---

# GeoDjango¶

# GeoDjango¶

GeoDjango intends to be a world-class geographic web framework. Its goal is to
make it as easy as possible to build GIS web applications and harness the power
of spatially enabled data.

---

# django.contrib.humanize¶

# django.contrib.humanize¶

A set of Django template filters useful for adding a “human touch” to data.

To activate these filters, add `'django.contrib.humanize'` to your
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting. Once you’ve done that, use
`{% load humanize %}` in a template, and you’ll have access to the following
filters.

## apnumber¶

For numbers 1-9, returns the number spelled out. Otherwise, returns the
number. This follows Associated Press style.

Examples:

- `1` becomes `one`.
- `2` becomes `two`.
- `10` becomes `10`.

You can pass in either an integer or a string representation of an integer.

## intcomma¶

Converts an integer or float (or a string representation of either) to a string
containing commas every three digits.

Examples:

- `4500` becomes `4,500`.
- `4500.2` becomes `4,500.2`.
- `45000` becomes `45,000`.
- `450000` becomes `450,000`.
- `4500000` becomes `4,500,000`.

[Format localization](https://docs.djangoproject.com/en/topics/i18n/formatting/) will be respected if enabled,
e.g. with the `'de'` language:

- `45000` becomes `'45.000'`.
- `450000` becomes `'450.000'`.

## intword¶

Converts a large integer (or a string representation of an integer) to a
friendly text representation. Translates `1.0` as a singular phrase and all
other numeric values as plural, this may be incorrect for some languages. Works
best for numbers over 1 million.

Examples:

- `1000000` becomes `1.0 million`.
- `1200000` becomes `1.2 million`.
- `1200000000` becomes `1.2 billion`.
- `-1200000000` becomes `-1.2 billion`.

Values up to 10^100 (Googol) are supported.

[Format localization](https://docs.djangoproject.com/en/topics/i18n/formatting/) will be respected if enabled,
e.g. with the `'de'` language:

- `1000000` becomes `'1,0 Million'`.
- `1200000` becomes `'1,2 Millionen'`.
- `1200000000` becomes `'1,2 Milliarden'`.
- `-1200000000` becomes `'-1,2 Milliarden'`.

## naturalday¶

For dates that are the current day or within one day, return “today”,
“tomorrow” or “yesterday”, as appropriate. Otherwise, format the date using
the passed in format string.

**Argument:** Date formatting string as described in the [date](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatefilter-date) tag.

Examples (when ‘today’ is 17 Feb 2007):

- `16 Feb 2007` becomes `yesterday`.
- `17 Feb 2007` becomes `today`.
- `18 Feb 2007` becomes `tomorrow`.
- Any other day is formatted according to given argument or the
  [DATE_FORMAT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DATE_FORMAT) setting if no argument is given.

## naturaltime¶

For datetime values, returns a string representing how many seconds,
minutes or hours ago it was – falling back to the [timesince](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatefilter-timesince)
format if the value is more than a day old. In case the datetime value is in
the future the return value will automatically use an appropriate phrase.

Examples (when ‘now’ is 17 Feb 2007 16:30:00):

- `17 Feb 2007 16:30:00` becomes `now`.
- `17 Feb 2007 16:29:31` becomes `29 seconds ago`.
- `17 Feb 2007 16:29:00` becomes `a minute ago`.
- `17 Feb 2007 16:25:35` becomes `4 minutes ago`.
- `17 Feb 2007 15:30:29` becomes `59 minutes ago`.
- `17 Feb 2007 15:30:01` becomes `59 minutes ago`.
- `17 Feb 2007 15:30:00` becomes `an hour ago`.
- `17 Feb 2007 13:31:29` becomes `2 hours ago`.
- `16 Feb 2007 13:31:29` becomes `1 day, 2 hours ago`.
- `16 Feb 2007 13:30:01` becomes `1 day, 2 hours ago`.
- `16 Feb 2007 13:30:00` becomes `1 day, 3 hours ago`.
- `17 Feb 2007 16:30:30` becomes `30 seconds from now`.
- `17 Feb 2007 16:30:29` becomes `29 seconds from now`.
- `17 Feb 2007 16:31:00` becomes `a minute from now`.
- `17 Feb 2007 16:34:35` becomes `4 minutes from now`.
- `17 Feb 2007 17:30:29` becomes `an hour from now`.
- `17 Feb 2007 18:31:29` becomes `2 hours from now`.
- `18 Feb 2007 16:31:29` becomes `1 day from now`.
- `26 Feb 2007 18:31:29` becomes `1 week, 2 days from now`.

## ordinal¶

Converts an integer to its ordinal as a string.

Examples:

- `1` becomes `1st`.
- `2` becomes `2nd`.
- `3` becomes `3rd`.

You can pass in either an integer or a string representation of an integer.

---

# The messages framework¶

# The messages framework¶

Quite commonly in web applications, you need to display a one-time
notification message (also known as “flash message”) to the user after
processing a form or some other types of user input.

For this, Django provides full support for cookie- and session-based
messaging, for both anonymous and authenticated users. The messages framework
allows you to temporarily store messages in one request and retrieve them for
display in a subsequent request (usually the next one). Every message is
tagged with a specific `level` that determines its priority (e.g., `info`,
`warning`, or `error`).

## Enabling messages¶

Messages are implemented through a [middleware](https://docs.djangoproject.com/en/5.0/middleware/)
class and corresponding [context processor](https://docs.djangoproject.com/en/5.0/templates/api/).

The default `settings.py` created by `django-admin startproject`
already contains all the settings required to enable message functionality:

- `'django.contrib.messages'` is in [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS).
- [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE) contains
  `'django.contrib.sessions.middleware.SessionMiddleware'` and
  `'django.contrib.messages.middleware.MessageMiddleware'`.
  The default [storage backend](#message-storage-backends) relies on
  [sessions](https://docs.djangoproject.com/en/topics/http/sessions/). That’s why `SessionMiddleware`
  must be enabled and appear before `MessageMiddleware` in
  [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE).
- The `'context_processors'` option of the `DjangoTemplates` backend
  defined in your [TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES) setting contains
  `'django.contrib.messages.context_processors.messages'`.

If you don’t want to use messages, you can remove
`'django.contrib.messages'` from your [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS), the
`MessageMiddleware` line from [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE), and the `messages`
context processor from [TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES).

## Configuring the message engine¶

### Storage backends¶

The messages framework can use different backends to store temporary messages.

Django provides three built-in storage classes in
[django.contrib.messages](#module-django.contrib.messages):

   *class*storage.session.SessionStorage[¶](#django.contrib.messages.storage.session.SessionStorage)

This class stores all messages inside of the request’s session. Therefore
it requires Django’s `contrib.sessions` application.

    *class*storage.cookie.CookieStorage[¶](#django.contrib.messages.storage.cookie.CookieStorage)

This class stores the message data in a cookie (signed with a secret hash
to prevent manipulation) to persist notifications across requests. Old
messages are dropped if the cookie data size would exceed 2048 bytes.

    *class*storage.fallback.FallbackStorage[¶](#django.contrib.messages.storage.fallback.FallbackStorage)

This class first uses `CookieStorage`, and falls back to using
`SessionStorage` for the messages that could not fit in a single cookie.
It also requires Django’s `contrib.sessions` application.

This behavior avoids writing to the session whenever possible. It should
provide the best performance in the general case.

[FallbackStorage](#django.contrib.messages.storage.fallback.FallbackStorage) is the
default storage class. If it isn’t suitable to your needs, you can select
another storage class by setting [MESSAGE_STORAGE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MESSAGE_STORAGE) to its full import
path, for example:

```
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
```

    *class*storage.base.BaseStorage[¶](#django.contrib.messages.storage.base.BaseStorage)

To write your own storage class, subclass the `BaseStorage` class in
`django.contrib.messages.storage.base` and implement the `_get` and
`_store` methods.

### Message levels¶

The messages framework is based on a configurable level architecture similar
to that of the Python logging module. Message levels allow you to group
messages by type so they can be filtered or displayed differently in views and
templates.

The built-in levels, which can be imported from `django.contrib.messages`
directly, are:

| Constant | Purpose |
| --- | --- |
| DEBUG | Development-related messages that will be ignored (or removed) in a production deployment |
| INFO | Informational messages for the user |
| SUCCESS | An action was successful, e.g. “Your profile was updated successfully” |
| WARNING | A failure did not occur but may be imminent |
| ERROR | An action wasnotsuccessful or some other failure occurred |

The [MESSAGE_LEVEL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MESSAGE_LEVEL) setting can be used to change the minimum recorded level
(or it can be [changed per request](#changing-the-minimum-recorded-level-per-request)). Attempts to add messages of a level less
than this will be ignored.

### Message tags¶

Message tags are a string representation of the message level plus any
extra tags that were added directly in the view (see
[Adding extra message tags](#adding-extra-message-tags) below for more details). Tags are stored in a
string and are separated by spaces. Typically, message tags
are used as CSS classes to customize message style based on message type. By
default, each level has a single tag that’s a lowercase version of its own
constant:

| Level Constant | Tag |
| --- | --- |
| DEBUG | debug |
| INFO | info |
| SUCCESS | success |
| WARNING | warning |
| ERROR | error |

To change the default tags for a message level (either built-in or custom),
set the [MESSAGE_TAGS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MESSAGE_TAGS) setting to a dictionary containing the levels
you wish to change. As this extends the default tags, you only need to provide
tags for the levels you wish to override:

```
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.INFO: "",
    50: "critical",
}
```

## Using messages in views and templates¶

   add_message(*request*, *level*, *message*, *extra_tags=''*, *fail_silently=False*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/messages/api/#add_message)[¶](#django.contrib.messages.add_message)

### Adding a message¶

To add a message, call:

```
from django.contrib import messages

messages.add_message(request, messages.INFO, "Hello world.")
```

Some shortcut methods provide a standard way to add messages with commonly
used tags (which are usually represented as HTML classes for the message):

```
messages.debug(request, "%s SQL statements were executed." % count)
messages.info(request, "Three credits remain in your account.")
messages.success(request, "Profile details updated.")
messages.warning(request, "Your account expires in three days.")
messages.error(request, "Document deleted.")
```

### Displaying messages¶

   get_messages(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/messages/api/#get_messages)[¶](#django.contrib.messages.get_messages)

**In your template**, use something like:

```
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```

If you’re using the context processor, your template should be rendered with a
`RequestContext`. Otherwise, ensure `messages` is available to
the template context.

Even if you know there is only one message, you should still iterate over the
`messages` sequence, because otherwise the message storage will not be
cleared for the next request.

The context processor also provides a `DEFAULT_MESSAGE_LEVELS` variable which
is a mapping of the message level names to their numeric value:

```
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>
        {% if message.level == DEFAULT_MESSAGE_LEVELS.ERROR %}Important: {% endif %}
        {{ message }}
    </li>
    {% endfor %}
</ul>
{% endif %}
```

**Outside of templates**, you can use
[get_messages()](#django.contrib.messages.get_messages):

```
from django.contrib.messages import get_messages

storage = get_messages(request)
for message in storage:
    do_something_with_the_message(message)
```

For instance, you can fetch all the messages to return them in a
[JSONResponseMixin](https://docs.djangoproject.com/en/topics/class-based-views/mixins/#jsonresponsemixin-example) instead of a
[TemplateResponseMixin](https://docs.djangoproject.com/en/5.0/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin).

[get_messages()](#django.contrib.messages.get_messages) will return an
instance of the configured storage backend.

### TheMessageclass¶

   *class*Message[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/messages/storage/base/#Message)[¶](#django.contrib.messages.Message)

When you loop over the list of messages in a template, what you get are
instances of the `Message` class. They have only a few attributes:

- `message`: The actual text of the message.
- `level`: An integer describing the type of the message (see the
  [message levels](#message-levels) section above).
- `tags`: A string combining all the message’s tags (`extra_tags` and
  `level_tag`) separated by spaces.
- `extra_tags`: A string containing custom tags for this message,
  separated by spaces. It’s empty by default.
- `level_tag`: The string representation of the level. By default, it’s
  the lowercase version of the name of the associated constant, but this
  can be changed if you need by using the [MESSAGE_TAGS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MESSAGE_TAGS) setting.

### Creating custom message levels¶

Messages levels are nothing more than integers, so you can define your own
level constants and use them to create more customized user feedback, e.g.:

```
CRITICAL = 50

def my_view(request):
    messages.add_message(request, CRITICAL, "A serious error occurred.")
```

When creating custom message levels you should be careful to avoid overloading
existing levels. The values for the built-in levels are:

| Level Constant | Value |
| --- | --- |
| DEBUG | 10 |
| INFO | 20 |
| SUCCESS | 25 |
| WARNING | 30 |
| ERROR | 40 |

If you need to identify the custom levels in your HTML or CSS, you need to
provide a mapping via the [MESSAGE_TAGS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MESSAGE_TAGS) setting.

Note

If you are creating a reusable application, it is recommended to use
only the built-in [message levels](#message-levels) and not rely on any custom levels.

### Changing the minimum recorded level per-request¶

The minimum recorded level can be set per request via the `set_level`
method:

```
from django.contrib import messages

# Change the messages level to ensure the debug message is added.
messages.set_level(request, messages.DEBUG)
messages.debug(request, "Test message...")

# In another request, record only messages with a level of WARNING and higher
messages.set_level(request, messages.WARNING)
messages.success(request, "Your profile was updated.")  # ignored
messages.warning(request, "Your account is about to expire.")  # recorded

# Set the messages level back to default.
messages.set_level(request, None)
```

Similarly, the current effective level can be retrieved with `get_level`:

```
from django.contrib import messages

current_level = messages.get_level(request)
```

For more information on how the minimum recorded level functions, see
[Message levels](#message-levels) above.

### Adding extra message tags¶

For more direct control over message tags, you can optionally provide a string
containing extra tags to any of the add methods:

```
messages.add_message(request, messages.INFO, "Over 9000!", extra_tags="dragonball")
messages.error(request, "Email box full", extra_tags="email")
```

Extra tags are added before the default tag for that level and are space
separated.

### Failing silently when the message framework is disabled¶

If you’re writing a reusable app (or other piece of code) and want to include
messaging functionality, but don’t want to require your users to enable it
if they don’t want to, you may pass an additional keyword argument
`fail_silently=True` to any of the `add_message` family of methods. For
example:

```
messages.add_message(
    request,
    messages.SUCCESS,
    "Profile details updated.",
    fail_silently=True,
)
messages.info(request, "Hello world.", fail_silently=True)
```

Note

Setting `fail_silently=True` only hides the `MessageFailure` that would
otherwise occur when the messages framework disabled and one attempts to
use one of the `add_message` family of methods. It does not hide failures
that may occur for other reasons.

### Adding messages in class-based views¶

   *class*views.SuccessMessageMixin[¶](#django.contrib.messages.views.SuccessMessageMixin)

Adds a success message attribute to
[FormView](https://docs.djangoproject.com/en/5.0/class-based-views/generic-editing/#django.views.generic.edit.FormView) based classes

   get_success_message(*cleaned_data*)[¶](#django.contrib.messages.views.SuccessMessageMixin.get_success_message)

`cleaned_data` is the cleaned data from the form which is used for
string formatting

**Example views.py**:

```
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from myapp.models import Author

class AuthorCreateView(SuccessMessageMixin, CreateView):
    model = Author
    success_url = "/success/"
    success_message = "%(name)s was created successfully"
```

The cleaned data from the `form` is available for string interpolation using
the `%(field_name)s` syntax. For ModelForms, if you need access to fields
from the saved `object` override the
[get_success_message()](#django.contrib.messages.views.SuccessMessageMixin.get_success_message)
method.

**Example views.py for ModelForms**:

```
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from myapp.models import ComplicatedModel

class ComplicatedCreateView(SuccessMessageMixin, CreateView):
    model = ComplicatedModel
    success_url = "/success/"
    success_message = "%(calculated_field)s was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.calculated_field,
        )
```

## Expiration of messages¶

The messages are marked to be cleared when the storage instance is iterated
(and cleared when the response is processed).

To avoid the messages being cleared, you can set the messages storage to
`False` after iterating:

```
storage = messages.get_messages(request)
for message in storage:
    do_something_with(message)
storage.used = False
```

## Behavior of parallel requests¶

Due to the way cookies (and hence sessions) work, **the behavior of any
backends that make use of cookies or sessions is undefined when the same
client makes multiple requests that set or get messages in parallel**. For
example, if a client initiates a request that creates a message in one window
(or tab) and then another that fetches any uniterated messages in another
window, before the first window redirects, the message may appear in the
second window instead of the first window where it may be expected.

In short, when multiple simultaneous requests from the same client are
involved, messages are not guaranteed to be delivered to the same window that
created them nor, in some cases, at all. Note that this is typically not a
problem in most applications and will become a non-issue in HTML5, where each
window/tab will have its own browsing context.

## Settings¶

A few [settings](https://docs.djangoproject.com/en/5.0/settings/#settings-messages) give you control over message
behavior:

- [MESSAGE_LEVEL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MESSAGE_LEVEL)
- [MESSAGE_STORAGE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MESSAGE_STORAGE)
- [MESSAGE_TAGS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MESSAGE_TAGS)

For backends that use cookies, the settings for the cookie are taken from
the session cookie settings:

- [SESSION_COOKIE_DOMAIN](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SESSION_COOKIE_DOMAIN)
- [SESSION_COOKIE_SECURE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SESSION_COOKIE_SECURE)
- [SESSION_COOKIE_HTTPONLY](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SESSION_COOKIE_HTTPONLY)

## Testing¶

  New in Django 5.0.

This module offers a tailored test assertion method, for testing messages
attached to an [HttpResponse](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponse).

To benefit from this assertion, add `MessagesTestMixin` to the class
hierarchy:

```
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase

class MsgTestCase(MessagesTestMixin, TestCase):
    pass
```

Then, inherit from the `MsgTestCase` in your tests.

   MessagesTestMixin.assertMessages(*response*, *expected_messages*, *ordered=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/messages/test/#MessagesTestMixin.assertMessages)[¶](#django.contrib.messages.test.MessagesTestMixin.assertMessages)

Asserts that [messages](#module-django.contrib.messages) added to the [response](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponse) matches `expected_messages`.

`expected_messages` is a list of
[Message](#django.contrib.messages.Message) objects.

By default, the comparison is ordering dependent. You can disable this by
setting the `ordered` argument to `False`.

---

# django.contrib.postgres¶

# django.contrib.postgres¶

PostgreSQL has a number of features which are not shared by the other databases
Django supports. This optional module contains model fields and form fields for
a number of PostgreSQL specific data types.

Note

Django is, and will continue to be, a database-agnostic web framework. We
would encourage those writing reusable applications for the Django
community to write database-agnostic code where practical. However, we
recognize that real world projects written using Django need not be
database-agnostic. In fact, once a project reaches a given size changing
the underlying data store is already a significant challenge and is likely
to require changing the code base in some ways to handle differences
between the data stores.

Django provides support for a number of data types which will
only work with PostgreSQL. There is no fundamental reason why (for example)
a `contrib.mysql` module does not exist, except that PostgreSQL has the
richest feature set of the supported databases so its users have the most
to gain.

---

# The redirects app¶

# The redirects app¶

Django comes with an optional redirects application. It lets you store
redirects in a database and handles the redirecting for you. It uses the HTTP
response status code `301 Moved Permanently` by default.

## Installation¶

To install the redirects app, follow these steps:

1. Ensure that the `django.contrib.sites` framework
  [is installed](https://docs.djangoproject.com/en/5.0/ref/sites/#enabling-the-sites-framework).
2. Add `'django.contrib.redirects'` to your [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting.
3. Add `'django.contrib.redirects.middleware.RedirectFallbackMiddleware'`
  to your [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE) setting.
4. Run the command [manage.pymigrate](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-migrate).

## How it works¶

`manage.py migrate` creates a `django_redirect` table in your database. This
is a lookup table with `site_id`, `old_path` and `new_path` fields.

The [RedirectFallbackMiddleware](#django.contrib.redirects.middleware.RedirectFallbackMiddleware)
does all of the work. Each time any Django application raises a 404
error, this middleware checks the redirects database for the requested
URL as a last resort. Specifically, it checks for a redirect with the
given `old_path` with a site ID that corresponds to the
[SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) setting.

- If it finds a match, and `new_path` is not empty, it redirects to
  `new_path` using a 301 (“Moved Permanently”) redirect. You can subclass
  [RedirectFallbackMiddleware](#django.contrib.redirects.middleware.RedirectFallbackMiddleware)
  and set
  [response_redirect_class](#django.contrib.redirects.middleware.RedirectFallbackMiddleware.response_redirect_class)
  to [django.http.HttpResponseRedirect](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponseRedirect) to use a
  `302 Moved Temporarily` redirect instead.
- If it finds a match, and `new_path` is empty, it sends a 410 (“Gone”)
  HTTP header and empty (content-less) response.
- If it doesn’t find a match, the request continues to be processed as
  usual.

The middleware only gets activated for 404s – not for 500s or responses of any
other status code.

Note that the order of [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE) matters. Generally, you can put
[RedirectFallbackMiddleware](#django.contrib.redirects.middleware.RedirectFallbackMiddleware) at the
end of the list, because it’s a last resort.

For more on middleware, read the [middleware docs](https://docs.djangoproject.com/en/topics/http/middleware/).

## How to add, change and delete redirects¶

### Via the admin interface¶

If you’ve activated the automatic Django admin interface, you should see a
“Redirects” section on the admin index page. Edit redirects as you edit any
other object in the system.

### Via the Python API¶

   *class*models.Redirect[¶](#django.contrib.redirects.models.Redirect)

Redirects are represented by a standard [Django model](https://docs.djangoproject.com/en/topics/db/models/),
which lives in [django/contrib/redirects/models.py](https://github.com/django/django/blob/main/django/contrib/redirects/models.py). You can access
redirect objects via the [Django database API](https://docs.djangoproject.com/en/topics/db/queries/).
For example:

```
>>> from django.conf import settings
>>> from django.contrib.redirects.models import Redirect
>>> # Add a new redirect.
>>> redirect = Redirect.objects.create(
...     site_id=1,
...     old_path="/contact-us/",
...     new_path="/contact/",
... )
>>> # Change a redirect.
>>> redirect.new_path = "/contact-details/"
>>> redirect.save()
>>> redirect
<Redirect: /contact-us/ ---> /contact-details/>
>>> # Delete a redirect.
>>> Redirect.objects.filter(site_id=1, old_path="/contact-us/").delete()
(1, {'redirects.Redirect': 1})
```

## Middleware¶

   *class*middleware.RedirectFallbackMiddleware[¶](#django.contrib.redirects.middleware.RedirectFallbackMiddleware)

You can change the [HttpResponse](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponse) classes used
by the middleware by creating a subclass of
[RedirectFallbackMiddleware](#django.contrib.redirects.middleware.RedirectFallbackMiddleware)
and overriding `response_gone_class` and/or `response_redirect_class`.

   response_gone_class[¶](#django.contrib.redirects.middleware.RedirectFallbackMiddleware.response_gone_class)

The [HttpResponse](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponse) class used when a
[Redirect](#django.contrib.redirects.models.Redirect) is not found for the
requested path or has a blank `new_path` value.

Defaults to [HttpResponseGone](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponseGone).

    response_redirect_class[¶](#django.contrib.redirects.middleware.RedirectFallbackMiddleware.response_redirect_class)

The [HttpResponse](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponse) class that handles the redirect.

Defaults to [HttpResponsePermanentRedirect](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponsePermanentRedirect).
