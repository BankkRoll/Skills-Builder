# Request and response objects¶

# Request and response objects¶

# Request and response objects¶

## Quick overview¶

Django uses request and response objects to pass state through the system.

When a page is requested, Django creates an [HttpRequest](#django.http.HttpRequest) object that
contains metadata about the request. Then Django loads the appropriate view,
passing the [HttpRequest](#django.http.HttpRequest) as the first argument to the view function.
Each view is responsible for returning an [HttpResponse](#django.http.HttpResponse) object.

This document explains the APIs for [HttpRequest](#django.http.HttpRequest) and
[HttpResponse](#django.http.HttpResponse) objects, which are defined in the [django.http](#module-django.http)
module.

## HttpRequestobjects¶

   *class*HttpRequest[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest)[¶](#django.http.HttpRequest)

### Attributes¶

All attributes should be considered read-only, unless stated otherwise.

   HttpRequest.scheme[¶](#django.http.HttpRequest.scheme)

A string representing the scheme of the request (`http` or `https`
usually).

    HttpRequest.body[¶](#django.http.HttpRequest.body)

The raw HTTP request body as a bytestring. This is useful for processing
data in different ways than conventional HTML forms: binary images,
XML payload etc. For processing conventional form data, use
[HttpRequest.POST](#django.http.HttpRequest.POST).

You can also read from an `HttpRequest` using a file-like interface with
[HttpRequest.read()](#django.http.HttpRequest.read) or [HttpRequest.readline()](#django.http.HttpRequest.readline). Accessing
the `body` attribute *after* reading the request with either of these I/O
stream methods will produce a `RawPostDataException`.

    HttpRequest.path[¶](#django.http.HttpRequest.path)

A string representing the full path to the requested page, not including
the scheme, domain, or query string.

Example: `"/music/bands/the_beatles/"`

    HttpRequest.path_info[¶](#django.http.HttpRequest.path_info)

Under some web server configurations, the portion of the URL after the
host name is split up into a script prefix portion and a path info
portion. The `path_info` attribute always contains the path info portion
of the path, no matter what web server is being used. Using this instead
of [path](#django.http.HttpRequest.path) can make your code easier to move between
test and deployment servers.

For example, if the `WSGIScriptAlias` for your application is set to
`"/minfo"`, then `path` might be `"/minfo/music/bands/the_beatles/"`
and `path_info` would be `"/music/bands/the_beatles/"`.

    HttpRequest.method[¶](#django.http.HttpRequest.method)

A string representing the HTTP method used in the request. This is
guaranteed to be uppercase. For example:

```
if request.method == "GET":
    do_something()
elif request.method == "POST":
    do_something_else()
```

     HttpRequest.encoding[¶](#django.http.HttpRequest.encoding)

A string representing the current encoding used to decode form submission
data (or `None`, which means the [DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting is
used). You can write to this attribute to change the encoding used when
accessing the form data. Any subsequent attribute accesses (such as reading
from [GET](#django.http.HttpRequest.GET) or [POST](#django.http.HttpRequest.POST)) will use the new `encoding` value.
Useful if you know the form data is not in the [DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET)
encoding.

    HttpRequest.content_type[¶](#django.http.HttpRequest.content_type)

A string representing the MIME type of the request, parsed from the
`CONTENT_TYPE` header.

    HttpRequest.content_params[¶](#django.http.HttpRequest.content_params)

A dictionary of key/value parameters included in the `CONTENT_TYPE`
header.

    HttpRequest.GET[¶](#django.http.HttpRequest.GET)

A dictionary-like object containing all given HTTP GET parameters. See the
[QueryDict](#django.http.QueryDict) documentation below.

    HttpRequest.POST[¶](#django.http.HttpRequest.POST)

A dictionary-like object containing all given HTTP POST parameters,
providing that the request contains form data. See the
[QueryDict](#django.http.QueryDict) documentation below. If you need to access raw or
non-form data posted in the request, access this through the
[HttpRequest.body](#django.http.HttpRequest.body) attribute instead.

It’s possible that a request can come in via POST with an empty `POST`
dictionary – if, say, a form is requested via the POST HTTP method but
does not include form data. Therefore, you shouldn’t use `if request.POST`
to check for use of the POST method; instead, use `if request.method ==
"POST"` (see [HttpRequest.method](#django.http.HttpRequest.method)).

`POST` does *not* include file-upload information. See [FILES](#django.http.HttpRequest.FILES).

    HttpRequest.COOKIES[¶](#django.http.HttpRequest.COOKIES)

A dictionary containing all cookies. Keys and values are strings.

    HttpRequest.FILES[¶](#django.http.HttpRequest.FILES)

A dictionary-like object containing all uploaded files. Each key in
`FILES` is the `name` from the `<input type="file" name="">`. Each
value in `FILES` is an [UploadedFile](https://docs.djangoproject.com/en/5.0/files/uploads/#django.core.files.uploadedfile.UploadedFile).

See [Managing files](https://docs.djangoproject.com/en/topics/files/) for more information.

`FILES` will only contain data if the request method was POST and the
`<form>` that posted to the request had `enctype="multipart/form-data"`.
Otherwise, `FILES` will be a blank dictionary-like object.

    HttpRequest.META[¶](#django.http.HttpRequest.META)

A dictionary containing all available HTTP headers. Available headers
depend on the client and server, but here are some examples:

- `CONTENT_LENGTH` – The length of the request body (as a string).
- `CONTENT_TYPE` – The MIME type of the request body.
- `HTTP_ACCEPT` – Acceptable content types for the response.
- `HTTP_ACCEPT_ENCODING` – Acceptable encodings for the response.
- `HTTP_ACCEPT_LANGUAGE` – Acceptable languages for the response.
- `HTTP_HOST` – The HTTP Host header sent by the client.
- `HTTP_REFERER` – The referring page, if any.
- `HTTP_USER_AGENT` – The client’s user-agent string.
- `QUERY_STRING` – The query string, as a single (unparsed) string.
- `REMOTE_ADDR` – The IP address of the client.
- `REMOTE_HOST` – The hostname of the client.
- `REMOTE_USER` – The user authenticated by the web server, if any.
- `REQUEST_METHOD` – A string such as `"GET"` or `"POST"`.
- `SERVER_NAME` – The hostname of the server.
- `SERVER_PORT` – The port of the server (as a string).

With the exception of `CONTENT_LENGTH` and `CONTENT_TYPE`, as given
above, any HTTP headers in the request are converted to `META` keys by
converting all characters to uppercase, replacing any hyphens with
underscores and adding an `HTTP_` prefix to the name. So, for example, a
header called `X-Bender` would be mapped to the `META` key
`HTTP_X_BENDER`.

Note that [runserver](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-runserver) strips all headers with underscores in the
name, so you won’t see them in `META`. This prevents header-spoofing
based on ambiguity between underscores and dashes both being normalizing to
underscores in WSGI environment variables. It matches the behavior of
web servers like Nginx and Apache 2.4+.

[HttpRequest.headers](#django.http.HttpRequest.headers) is a simpler way to access all HTTP-prefixed
headers, plus `CONTENT_LENGTH` and `CONTENT_TYPE`.

    HttpRequest.headers[¶](#django.http.HttpRequest.headers)

A case insensitive, dict-like object that provides access to all
HTTP-prefixed headers (plus `Content-Length` and `Content-Type`) from
the request.

The name of each header is stylized with title-casing (e.g. `User-Agent`)
when it’s displayed. You can access headers case-insensitively:

```
>>> request.headers
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6', ...}

>>> "User-Agent" in request.headers
True
>>> "user-agent" in request.headers
True

>>> request.headers["User-Agent"]
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
>>> request.headers["user-agent"]
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)

>>> request.headers.get("User-Agent")
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
>>> request.headers.get("user-agent")
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
```

For use in, for example, Django templates, headers can also be looked up
using underscores in place of hyphens:

```
{{ request.headers.user_agent }}
```

     HttpRequest.resolver_match[¶](#django.http.HttpRequest.resolver_match)

An instance of [ResolverMatch](https://docs.djangoproject.com/en/5.0/urlresolvers/#django.urls.ResolverMatch) representing the
resolved URL. This attribute is only set after URL resolving took place,
which means it’s available in all views but not in middleware which are
executed before URL resolving takes place (you can use it in
[process_view()](https://docs.djangoproject.com/en/topics/http/middleware/#process_view) though).

### Attributes set by application code¶

Django doesn’t set these attributes itself but makes use of them if set by your
application.

   HttpRequest.current_app[¶](#django.http.HttpRequest.current_app)

The [url](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatetag-url) template tag will use its value as the `current_app`
argument to [reverse()](https://docs.djangoproject.com/en/5.0/urlresolvers/#django.urls.reverse).

    HttpRequest.urlconf[¶](#django.http.HttpRequest.urlconf)

This will be used as the root URLconf for the current request, overriding
the [ROOT_URLCONF](https://docs.djangoproject.com/en/5.0/settings/#std-setting-ROOT_URLCONF) setting. See
[How Django processes a request](https://docs.djangoproject.com/en/topics/http/urls/#how-django-processes-a-request) for details.

`urlconf` can be set to `None` to revert any changes made by previous
middleware and return to using the [ROOT_URLCONF](https://docs.djangoproject.com/en/5.0/settings/#std-setting-ROOT_URLCONF).

    HttpRequest.exception_reporter_filter[¶](#django.http.HttpRequest.exception_reporter_filter)

This will be used instead of [DEFAULT_EXCEPTION_REPORTER_FILTER](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_EXCEPTION_REPORTER_FILTER)
for the current request. See [Custom error reports](https://docs.djangoproject.com/en/howto/error-reporting/#custom-error-reports) for details.

    HttpRequest.exception_reporter_class[¶](#django.http.HttpRequest.exception_reporter_class)

This will be used instead of [DEFAULT_EXCEPTION_REPORTER](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_EXCEPTION_REPORTER) for the
current request. See [Custom error reports](https://docs.djangoproject.com/en/howto/error-reporting/#custom-error-reports) for details.

### Attributes set by middleware¶

Some of the middleware included in Django’s contrib apps set attributes on the
request. If you don’t see the attribute on a request, be sure the appropriate
middleware class is listed in [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE).

   HttpRequest.session[¶](#django.http.HttpRequest.session)

From the [SessionMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.contrib.sessions.middleware.SessionMiddleware): A
readable and writable, dictionary-like object that represents the current
session.

    HttpRequest.site[¶](#django.http.HttpRequest.site)

From the [CurrentSiteMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.contrib.sites.middleware.CurrentSiteMiddleware):
An instance of [Site](https://docs.djangoproject.com/en/5.0/contrib/sites/#django.contrib.sites.models.Site) or
[RequestSite](https://docs.djangoproject.com/en/5.0/contrib/sites/#django.contrib.sites.requests.RequestSite) as returned by
[get_current_site()](https://docs.djangoproject.com/en/5.0/contrib/sites/#django.contrib.sites.shortcuts.get_current_site)
representing the current site.

    HttpRequest.user[¶](#django.http.HttpRequest.user)

From the [AuthenticationMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware):
An instance of [AUTH_USER_MODEL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-AUTH_USER_MODEL) representing the currently
logged-in user. If the user isn’t currently logged in, `user` will be set
to an instance of [AnonymousUser](https://docs.djangoproject.com/en/5.0/contrib/auth/#django.contrib.auth.models.AnonymousUser). You
can tell them apart with
[is_authenticated](https://docs.djangoproject.com/en/5.0/contrib/auth/#django.contrib.auth.models.User.is_authenticated), like so:

```
if request.user.is_authenticated:
    ...  # Do something for logged-in users.
else:
    ...  # Do something for anonymous users.
```

The [auser()](#django.http.HttpRequest.auser) method does the same thing but can be used from async
contexts.

### Methods¶

   HttpRequest.auser()[¶](#django.http.HttpRequest.auser)  New in Django 5.0.

From the [AuthenticationMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware):
Coroutine. Returns an instance of [AUTH_USER_MODEL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-AUTH_USER_MODEL) representing
the currently logged-in user. If the user isn’t currently logged in,
`auser` will return an instance of
[AnonymousUser](https://docs.djangoproject.com/en/5.0/contrib/auth/#django.contrib.auth.models.AnonymousUser). This is similar to the
[user](#django.http.HttpRequest.user) attribute but it works in async contexts.

    HttpRequest.get_host()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.get_host)[¶](#django.http.HttpRequest.get_host)

Returns the originating host of the request using information from the
`HTTP_X_FORWARDED_HOST` (if [USE_X_FORWARDED_HOST](https://docs.djangoproject.com/en/5.0/settings/#std-setting-USE_X_FORWARDED_HOST) is enabled)
and `HTTP_HOST` headers, in that order. If they don’t provide a value,
the method uses a combination of `SERVER_NAME` and `SERVER_PORT` as
detailed in [PEP 3333](https://peps.python.org/pep-3333/).

Example: `"127.0.0.1:8000"`

Raises `django.core.exceptions.DisallowedHost` if the host is not in
[ALLOWED_HOSTS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-ALLOWED_HOSTS) or the domain name is invalid according to
[RFC 1034](https://datatracker.ietf.org/doc/html/rfc1034.html)/[1035](https://datatracker.ietf.org/doc/html/rfc1035.html).

Note

The [get_host()](#django.http.HttpRequest.get_host) method fails when the host is
behind multiple proxies. One solution is to use middleware to rewrite
the proxy headers, as in the following example:

```
class MultipleProxyMiddleware:
    FORWARDED_FOR_FIELDS = [
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_FORWARDED_HOST",
        "HTTP_X_FORWARDED_SERVER",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if "," in request.META[field]:
                    parts = request.META[field].split(",")
                    request.META[field] = parts[-1].strip()
        return self.get_response(request)
```

This middleware should be positioned before any other middleware that
relies on the value of [get_host()](#django.http.HttpRequest.get_host) – for instance,
[CommonMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.middleware.common.CommonMiddleware) or
[CsrfViewMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.middleware.csrf.CsrfViewMiddleware).

     HttpRequest.get_port()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.get_port)[¶](#django.http.HttpRequest.get_port)

Returns the originating port of the request using information from the
`HTTP_X_FORWARDED_PORT` (if [USE_X_FORWARDED_PORT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-USE_X_FORWARDED_PORT) is enabled)
and `SERVER_PORT` `META` variables, in that order.

    HttpRequest.get_full_path()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.get_full_path)[¶](#django.http.HttpRequest.get_full_path)

Returns the `path`, plus an appended query string, if applicable.

Example: `"/music/bands/the_beatles/?print=true"`

    HttpRequest.get_full_path_info()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.get_full_path_info)[¶](#django.http.HttpRequest.get_full_path_info)

Like [get_full_path()](#django.http.HttpRequest.get_full_path), but uses [path_info](#django.http.HttpRequest.path_info) instead of
[path](#django.http.HttpRequest.path).

Example: `"/minfo/music/bands/the_beatles/?print=true"`

    HttpRequest.build_absolute_uri(*location=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.build_absolute_uri)[¶](#django.http.HttpRequest.build_absolute_uri)

Returns the absolute URI form of `location`. If no location is provided,
the location will be set to `request.get_full_path()`.

If the location is already an absolute URI, it will not be altered.
Otherwise the absolute URI is built using the server variables available in
this request. For example:

```
>>> request.build_absolute_uri()
'https://example.com/music/bands/the_beatles/?print=true'
>>> request.build_absolute_uri("/bands/")
'https://example.com/bands/'
>>> request.build_absolute_uri("https://example2.com/bands/")
'https://example2.com/bands/'
```

Note

Mixing HTTP and HTTPS on the same site is discouraged, therefore
[build_absolute_uri()](#django.http.HttpRequest.build_absolute_uri) will always generate an
absolute URI with the same scheme the current request has. If you need
to redirect users to HTTPS, it’s best to let your web server redirect
all HTTP traffic to HTTPS.

     HttpRequest.get_signed_cookie(*key*, *default=RAISE_ERROR*, *salt=''*, *max_age=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.get_signed_cookie)[¶](#django.http.HttpRequest.get_signed_cookie)

Returns a cookie value for a signed cookie, or raises a
`django.core.signing.BadSignature` exception if the signature is
no longer valid. If you provide the `default` argument the exception
will be suppressed and that default value will be returned instead.

The optional `salt` argument can be used to provide extra protection
against brute force attacks on your secret key. If supplied, the
`max_age` argument will be checked against the signed timestamp
attached to the cookie value to ensure the cookie is not older than
`max_age` seconds.

For example:

```
>>> request.get_signed_cookie("name")
'Tony'
>>> request.get_signed_cookie("name", salt="name-salt")
'Tony' # assuming cookie was set using the same salt
>>> request.get_signed_cookie("nonexistent-cookie")
KeyError: 'nonexistent-cookie'
>>> request.get_signed_cookie("nonexistent-cookie", False)
False
>>> request.get_signed_cookie("cookie-that-was-tampered-with")
BadSignature: ...
>>> request.get_signed_cookie("name", max_age=60)
SignatureExpired: Signature age 1677.3839159 > 60 seconds
>>> request.get_signed_cookie("name", False, max_age=60)
False
```

See [cryptographic signing](https://docs.djangoproject.com/en/topics/signing/) for more information.

    HttpRequest.is_secure()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.is_secure)[¶](#django.http.HttpRequest.is_secure)

Returns `True` if the request is secure; that is, if it was made with
HTTPS.

    HttpRequest.accepts(*mime_type*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.accepts)[¶](#django.http.HttpRequest.accepts)

Returns `True` if the request `Accept` header matches the `mime_type`
argument:

```
>>> request.accepts("text/html")
True
```

Most browsers send `Accept: */*` by default, so this would return
`True` for all content types. Setting an explicit `Accept` header in
API requests can be useful for returning a different content type for those
consumers only. See [Content negotiation example](https://docs.djangoproject.com/en/topics/class-based-views/generic-editing/#content-negotiation-example) of using
`accepts()` to return different content to API consumers.

If a response varies depending on the content of the `Accept` header and
you are using some form of caching like Django’s [cachemiddleware](https://docs.djangoproject.com/en/5.0/middleware/#module-django.middleware.cache), you should decorate the view with
[vary_on_headers('Accept')](https://docs.djangoproject.com/en/topics/http/decorators/#django.views.decorators.vary.vary_on_headers) so that the responses are
properly cached.

    HttpRequest.read(*size=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.read)[¶](#django.http.HttpRequest.read)    HttpRequest.readline()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.readline)[¶](#django.http.HttpRequest.readline)    HttpRequest.readlines()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.readlines)[¶](#django.http.HttpRequest.readlines)    HttpRequest.__iter__()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#HttpRequest.__iter__)[¶](#django.http.HttpRequest.__iter__)

Methods implementing a file-like interface for reading from an
`HttpRequest` instance. This makes it possible to consume an incoming
request in a streaming fashion. A common use-case would be to process a
big XML payload with an iterative parser without constructing a whole
XML tree in memory.

Given this standard interface, an `HttpRequest` instance can be
passed directly to an XML parser such as
[ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree):

```
import xml.etree.ElementTree as ET

for element in ET.iterparse(request):
    process(element)
```

## QueryDictobjects¶

   *class*QueryDict[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict)[¶](#django.http.QueryDict)

In an [HttpRequest](#django.http.HttpRequest) object, the [GET](#django.http.HttpRequest.GET) and
[POST](#django.http.HttpRequest.POST) attributes are instances of `django.http.QueryDict`,
a dictionary-like class customized to deal with multiple values for the same
key. This is necessary because some HTML form elements, notably
`<select multiple>`, pass multiple values for the same key.

The `QueryDict`s at `request.POST` and `request.GET` will be immutable
when accessed in a normal request/response cycle. To get a mutable version you
need to use [QueryDict.copy()](#django.http.QueryDict.copy).

### Methods¶

[QueryDict](#django.http.QueryDict) implements all the standard dictionary methods because it’s
a subclass of dictionary. Exceptions are outlined here:

   QueryDict.__init__(*query_string=None*, *mutable=False*, *encoding=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.__init__)[¶](#django.http.QueryDict.__init__)

Instantiates a `QueryDict` object based on `query_string`.

```
>>> QueryDict("a=1&a=2&c=3")
<QueryDict: {'a': ['1', '2'], 'c': ['3']}>
```

If `query_string` is not passed in, the resulting `QueryDict` will be
empty (it will have no keys or values).

Most `QueryDict`s you encounter, and in particular those at
`request.POST` and `request.GET`, will be immutable. If you are
instantiating one yourself, you can make it mutable by passing
`mutable=True` to its `__init__()`.

Strings for setting both keys and values will be converted from `encoding`
to `str`. If `encoding` is not set, it defaults to
[DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET).

    *classmethod*QueryDict.fromkeys(*iterable*, *value=''*, *mutable=False*, *encoding=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.fromkeys)[¶](#django.http.QueryDict.fromkeys)

Creates a new `QueryDict` with keys from `iterable` and each value
equal to `value`. For example:

```
>>> QueryDict.fromkeys(["a", "a", "b"], value="val")
<QueryDict: {'a': ['val', 'val'], 'b': ['val']}>
```

     QueryDict.__getitem__(*key*)[¶](#django.http.QueryDict.__getitem__)

Returns the value for the given key. If the key has more than one value,
it returns the last value. Raises
`django.utils.datastructures.MultiValueDictKeyError` if the key does not
exist. (This is a subclass of Python’s standard [KeyError](https://docs.python.org/3/library/exceptions.html#KeyError), so you can
stick to catching `KeyError`.)

    QueryDict.__setitem__(*key*, *value*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.__setitem__)[¶](#django.http.QueryDict.__setitem__)

Sets the given key to `[value]` (a list whose single element is
`value`). Note that this, as other dictionary functions that have side
effects, can only be called on a mutable `QueryDict` (such as one that
was created via [QueryDict.copy()](#django.http.QueryDict.copy)).

    QueryDict.__contains__(*key*)[¶](#django.http.QueryDict.__contains__)

Returns `True` if the given key is set. This lets you do, e.g., `if "foo"
in request.GET`.

    QueryDict.get(*key*, *default=None*)[¶](#django.http.QueryDict.get)

Uses the same logic as [__getitem__()](#django.http.QueryDict.__getitem__), with a hook for returning a
default value if the key doesn’t exist.

    QueryDict.setdefault(*key*, *default=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.setdefault)[¶](#django.http.QueryDict.setdefault)

Like [dict.setdefault()](https://docs.python.org/3/library/stdtypes.html#dict.setdefault), except it uses [__setitem__()](#django.http.QueryDict.__setitem__) internally.

    QueryDict.update(*other_dict*)[¶](#django.http.QueryDict.update)

Takes either a `QueryDict` or a dictionary. Like [dict.update()](https://docs.python.org/3/library/stdtypes.html#dict.update),
except it *appends* to the current dictionary items rather than replacing
them. For example:

```
>>> q = QueryDict("a=1", mutable=True)
>>> q.update({"a": "2"})
>>> q.getlist("a")
['1', '2']
>>> q["a"]  # returns the last
'2'
```

     QueryDict.items()[¶](#django.http.QueryDict.items)

Like [dict.items()](https://docs.python.org/3/library/stdtypes.html#dict.items), except this uses the same last-value logic as
[__getitem__()](#django.http.QueryDict.__getitem__) and returns an iterator object instead of a view object.
For example:

```
>>> q = QueryDict("a=1&a=2&a=3")
>>> list(q.items())
[('a', '3')]
```

     QueryDict.values()[¶](#django.http.QueryDict.values)

Like [dict.values()](https://docs.python.org/3/library/stdtypes.html#dict.values), except this uses the same last-value logic as
[__getitem__()](#django.http.QueryDict.__getitem__) and returns an iterator instead of a view object. For
example:

```
>>> q = QueryDict("a=1&a=2&a=3")
>>> list(q.values())
['3']
```

In addition, `QueryDict` has the following methods:

   QueryDict.copy()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.copy)[¶](#django.http.QueryDict.copy)

Returns a copy of the object using [copy.deepcopy()](https://docs.python.org/3/library/copy.html#copy.deepcopy). This copy will
be mutable even if the original was not.

    QueryDict.getlist(*key*, *default=None*)[¶](#django.http.QueryDict.getlist)

Returns a list of the data with the requested key. Returns an empty list if
the key doesn’t exist and `default` is `None`. It’s guaranteed to
return a list unless the default value provided isn’t a list.

    QueryDict.setlist(*key*, *list_*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.setlist)[¶](#django.http.QueryDict.setlist)

Sets the given key to `list_` (unlike [__setitem__()](#django.http.QueryDict.__setitem__)).

    QueryDict.appendlist(*key*, *item*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.appendlist)[¶](#django.http.QueryDict.appendlist)

Appends an item to the internal list associated with key.

    QueryDict.setlistdefault(*key*, *default_list=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.setlistdefault)[¶](#django.http.QueryDict.setlistdefault)

Like [setdefault()](#django.http.QueryDict.setdefault), except it takes a list of values instead of a
single value.

    QueryDict.lists()[¶](#django.http.QueryDict.lists)

Like [items()](#django.http.QueryDict.items), except it includes all values, as a list, for each
member of the dictionary. For example:

```
>>> q = QueryDict("a=1&a=2&a=3")
>>> q.lists()
[('a', ['1', '2', '3'])]
```

     QueryDict.pop(*key*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.pop)[¶](#django.http.QueryDict.pop)

Returns a list of values for the given key and removes them from the
dictionary. Raises `KeyError` if the key does not exist. For example:

```
>>> q = QueryDict("a=1&a=2&a=3", mutable=True)
>>> q.pop("a")
['1', '2', '3']
```

     QueryDict.popitem()[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.popitem)[¶](#django.http.QueryDict.popitem)

Removes an arbitrary member of the dictionary (since there’s no concept
of ordering), and returns a two value tuple containing the key and a list
of all values for the key. Raises `KeyError` when called on an empty
dictionary. For example:

```
>>> q = QueryDict("a=1&a=2&a=3", mutable=True)
>>> q.popitem()
('a', ['1', '2', '3'])
```

     QueryDict.dict()[¶](#django.http.QueryDict.dict)

Returns a `dict` representation of `QueryDict`. For every (key, list)
pair in `QueryDict`, `dict` will have (key, item), where item is one
element of the list, using the same logic as [QueryDict.__getitem__()](#django.http.QueryDict.__getitem__):

```
>>> q = QueryDict("a=1&a=3&a=5")
>>> q.dict()
{'a': '5'}
```

     QueryDict.urlencode(*safe=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#QueryDict.urlencode)[¶](#django.http.QueryDict.urlencode)

Returns a string of the data in query string format. For example:

```
>>> q = QueryDict("a=2&b=3&b=5")
>>> q.urlencode()
'a=2&b=3&b=5'
```

Use the `safe` parameter to pass characters which don’t require encoding.
For example:

```
>>> q = QueryDict(mutable=True)
>>> q["next"] = "/a&b/"
>>> q.urlencode(safe="/")
'next=/a%26b/'
```

## HttpResponseobjects¶

   *class*HttpResponse[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponse)[¶](#django.http.HttpResponse)

In contrast to [HttpRequest](#django.http.HttpRequest) objects, which are created automatically by
Django, [HttpResponse](#django.http.HttpResponse) objects are your responsibility. Each view you
write is responsible for instantiating, populating, and returning an
[HttpResponse](#django.http.HttpResponse).

The [HttpResponse](#django.http.HttpResponse) class lives in the [django.http](#module-django.http) module.

### Usage¶

#### Passing strings¶

Typical usage is to pass the contents of the page, as a string, bytestring,
or [memoryview](https://docs.python.org/3/library/stdtypes.html#memoryview), to the [HttpResponse](#django.http.HttpResponse) constructor:

```
>>> from django.http import HttpResponse
>>> response = HttpResponse("Here's the text of the web page.")
>>> response = HttpResponse("Text only, please.", content_type="text/plain")
>>> response = HttpResponse(b"Bytestrings are also accepted.")
>>> response = HttpResponse(memoryview(b"Memoryview as well."))
```

But if you want to add content incrementally, you can use `response` as a
file-like object:

```
>>> response = HttpResponse()
>>> response.write("<p>Here's the text of the web page.</p>")
>>> response.write("<p>Here's another paragraph.</p>")
```

#### Passing iterators¶

Finally, you can pass `HttpResponse` an iterator rather than strings.
`HttpResponse` will consume the iterator immediately, store its content as a
string, and discard it. Objects with a `close()` method such as files and
generators are immediately closed.

If you need the response to be streamed from the iterator to the client, you
must use the [StreamingHttpResponse](#django.http.StreamingHttpResponse) class instead.

#### Setting header fields¶

To set or remove a header field in your response, use
[HttpResponse.headers](#django.http.HttpResponse.headers):

```
>>> response = HttpResponse()
>>> response.headers["Age"] = 120
>>> del response.headers["Age"]
```

You can also manipulate headers by treating your response like a dictionary:

```
>>> response = HttpResponse()
>>> response["Age"] = 120
>>> del response["Age"]
```

This proxies to `HttpResponse.headers`, and is the original interface offered
by `HttpResponse`.

When using this interface, unlike a dictionary, `del` doesn’t raise
`KeyError` if the header field doesn’t exist.

You can also set headers on instantiation:

```
>>> response = HttpResponse(headers={"Age": 120})
```

For setting the `Cache-Control` and `Vary` header fields, it is recommended
to use the [patch_cache_control()](https://docs.djangoproject.com/en/5.0/utils/#django.utils.cache.patch_cache_control) and
[patch_vary_headers()](https://docs.djangoproject.com/en/5.0/utils/#django.utils.cache.patch_vary_headers) methods from
[django.utils.cache](https://docs.djangoproject.com/en/5.0/utils/#module-django.utils.cache), since these fields can have multiple, comma-separated
values. The “patch” methods ensure that other values, e.g. added by a
middleware, are not removed.

HTTP header fields cannot contain newlines. An attempt to set a header field
containing a newline character (CR or LF) will raise `BadHeaderError`

#### Telling the browser to treat the response as a file attachment¶

To tell the browser to treat the response as a file attachment, set the
`Content-Type` and `Content-Disposition` headers. For example, this is how
you might return a Microsoft Excel spreadsheet:

```
>>> response = HttpResponse(
...     my_data,
...     headers={
...         "Content-Type": "application/vnd.ms-excel",
...         "Content-Disposition": 'attachment; filename="foo.xls"',
...     },
... )
```

There’s nothing Django-specific about the `Content-Disposition` header, but
it’s easy to forget the syntax, so we’ve included it here.

### Attributes¶

   HttpResponse.content[¶](#django.http.HttpResponse.content)

A bytestring representing the content, encoded from a string if necessary.

    HttpResponse.cookies[¶](#django.http.HttpResponse.cookies)

A [http.cookies.SimpleCookie](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie) object holding the cookies included
in the response.

    HttpResponse.headers[¶](#django.http.HttpResponse.headers)

A case insensitive, dict-like object that provides an interface to all
HTTP headers on the response, except a `Set-Cookie` header. See
[Setting header fields](#setting-header-fields) and [HttpResponse.cookies](#django.http.HttpResponse.cookies).

    HttpResponse.charset[¶](#django.http.HttpResponse.charset)

A string denoting the charset in which the response will be encoded. If not
given at `HttpResponse` instantiation time, it will be extracted from
`content_type` and if that is unsuccessful, the
[DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting will be used.

    HttpResponse.status_code[¶](#django.http.HttpResponse.status_code)

The [HTTP status code](https://datatracker.ietf.org/doc/html/rfc9110.html#section-15) for the response.

Unless [reason_phrase](#django.http.HttpResponse.reason_phrase) is explicitly set, modifying the value of
`status_code` outside the constructor will also modify the value of
`reason_phrase`.

    HttpResponse.reason_phrase[¶](#django.http.HttpResponse.reason_phrase)

The HTTP reason phrase for the response. It uses the [HTTP standard’s](https://datatracker.ietf.org/doc/html/rfc9110.html#section-15.1) default reason phrases.

Unless explicitly set, `reason_phrase` is determined by the value of
[status_code](#django.http.HttpResponse.status_code).

    HttpResponse.streaming[¶](#django.http.HttpResponse.streaming)

This is always `False`.

This attribute exists so middleware can treat streaming responses
differently from regular responses.

    HttpResponse.closed[¶](#django.http.HttpResponse.closed)

`True` if the response has been closed.

### Methods¶

   HttpResponse.__init__(*content=b''*, *content_type=None*, *status=200*, *reason=None*, *charset=None*, *headers=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponse.__init__)[¶](#django.http.HttpResponse.__init__)

Instantiates an `HttpResponse` object with the given page content,
content type, and headers.

`content` is most commonly an iterator, bytestring, [memoryview](https://docs.python.org/3/library/stdtypes.html#memoryview),
or string. Other types will be converted to a bytestring by encoding their
string representation. Iterators should return strings or bytestrings and
those will be joined together to form the content of the response.

`content_type` is the MIME type optionally completed by a character set
encoding and is used to fill the HTTP `Content-Type` header. If not
specified, it is formed by `'text/html'` and the
[DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) settings, by default:
`"text/html; charset=utf-8"`.

`status` is the [HTTP status code](https://datatracker.ietf.org/doc/html/rfc9110.html#section-15) for the
response. You can use Python’s [http.HTTPStatus](https://docs.python.org/3/library/http.html#http.HTTPStatus) for meaningful
aliases, such as `HTTPStatus.NO_CONTENT`.

`reason` is the HTTP response phrase. If not provided, a default phrase
will be used.

`charset` is the charset in which the response will be encoded. If not
given it will be extracted from `content_type`, and if that
is unsuccessful, the [DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting will be used.

`headers` is a [dict](https://docs.python.org/3/library/stdtypes.html#dict) of HTTP headers for the response.

    HttpResponse.__setitem__(*header*, *value*)[¶](#django.http.HttpResponse.__setitem__)

Sets the given header name to the given value. Both `header` and
`value` should be strings.

    HttpResponse.__delitem__(*header*)[¶](#django.http.HttpResponse.__delitem__)

Deletes the header with the given name. Fails silently if the header
doesn’t exist. Case-insensitive.

    HttpResponse.__getitem__(*header*)[¶](#django.http.HttpResponse.__getitem__)

Returns the value for the given header name. Case-insensitive.

    HttpResponse.get(*header*, *alternate=None*)[¶](#django.http.HttpResponse.get)

Returns the value for the given header, or an `alternate` if the header
doesn’t exist.

    HttpResponse.has_header(*header*)[¶](#django.http.HttpResponse.has_header)

Returns `True` or `False` based on a case-insensitive check for a
header with the given name.

    HttpResponse.items()[¶](#django.http.HttpResponse.items)

Acts like [dict.items()](https://docs.python.org/3/library/stdtypes.html#dict.items) for HTTP headers on the response.

    HttpResponse.setdefault(*header*, *value*)[¶](#django.http.HttpResponse.setdefault)

Sets a header unless it has already been set.

    HttpResponse.set_cookie(*key*, *value=''*, *max_age=None*, *expires=None*, *path='/'*, *domain=None*, *secure=False*, *httponly=False*, *samesite=None*)[¶](#django.http.HttpResponse.set_cookie)

Sets a cookie. The parameters are the same as in the
[Morsel](https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel) cookie object in the Python standard library.

- `max_age` should be a [timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta) object, an integer
  number of seconds, or `None` (default) if the cookie should last only
  as long as the client’s browser session. If `expires` is not specified,
  it will be calculated.
- `expires` should either be a string in the format
  `"Wdy, DD-Mon-YY HH:MM:SS GMT"` or a `datetime.datetime` object
  in UTC. If `expires` is a `datetime` object, the `max_age`
  will be calculated.
- Use `domain` if you want to set a cross-domain cookie. For example,
  `domain="example.com"` will set a cookie that is readable by the
  domains www.example.com, blog.example.com, etc. Otherwise, a cookie will
  only be readable by the domain that set it.
- Use `secure=True` if you want the cookie to be only sent to the server
  when a request is made with the `https` scheme.
- Use `httponly=True` if you want to prevent client-side
  JavaScript from having access to the cookie.
  [HttpOnly](https://owasp.org/www-community/HttpOnly) is a flag included in a Set-Cookie HTTP response header. It’s
  part of the [RFC 6265](https://datatracker.ietf.org/doc/html/rfc6265.html#section-4.1.2.6) standard for cookies
  and can be a useful way to mitigate the risk of a client-side script
  accessing the protected cookie data.
- Use `samesite='Strict'` or `samesite='Lax'` to tell the browser not
  to send this cookie when performing a cross-origin request. [SameSite](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value)
  isn’t supported by all browsers, so it’s not a replacement for Django’s
  CSRF protection, but rather a defense in depth measure.
  Use `samesite='None'` (string) to explicitly state that this cookie is
  sent with all same-site and cross-site requests.

Warning

[RFC 6265](https://datatracker.ietf.org/doc/html/rfc6265.html#section-6.1) states that user agents should
support cookies of at least 4096 bytes. For many browsers this is also
the maximum size. Django will not raise an exception if there’s an
attempt to store a cookie of more than 4096 bytes, but many browsers
will not set the cookie correctly.

     HttpResponse.set_signed_cookie(*key*, *value*, *salt=''*, *max_age=None*, *expires=None*, *path='/'*, *domain=None*, *secure=False*, *httponly=False*, *samesite=None*)[¶](#django.http.HttpResponse.set_signed_cookie)

Like [set_cookie()](#django.http.HttpResponse.set_cookie), but
[cryptographic signing](https://docs.djangoproject.com/en/topics/signing/) the cookie before setting
it. Use in conjunction with [HttpRequest.get_signed_cookie()](#django.http.HttpRequest.get_signed_cookie).
You can use the optional `salt` argument for added key strength, but
you will need to remember to pass it to the corresponding
[HttpRequest.get_signed_cookie()](#django.http.HttpRequest.get_signed_cookie) call.

    HttpResponse.delete_cookie(*key*, *path='/'*, *domain=None*, *samesite=None*)[¶](#django.http.HttpResponse.delete_cookie)

Deletes the cookie with the given key. Fails silently if the key doesn’t
exist.

Due to the way cookies work, `path` and `domain` should be the same
values you used in `set_cookie()` – otherwise the cookie may not be
deleted.

    HttpResponse.close()[¶](#django.http.HttpResponse.close)

This method is called at the end of the request directly by the WSGI
server.

    HttpResponse.write(*content*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponse.write)[¶](#django.http.HttpResponse.write)

This method makes an [HttpResponse](#django.http.HttpResponse) instance a file-like object.

    HttpResponse.flush()[¶](#django.http.HttpResponse.flush)

This method makes an [HttpResponse](#django.http.HttpResponse) instance a file-like object.

    HttpResponse.tell()[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponse.tell)[¶](#django.http.HttpResponse.tell)

This method makes an [HttpResponse](#django.http.HttpResponse) instance a file-like object.

    HttpResponse.getvalue()[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponse.getvalue)[¶](#django.http.HttpResponse.getvalue)

Returns the value of [HttpResponse.content](#django.http.HttpResponse.content). This method makes
an [HttpResponse](#django.http.HttpResponse) instance a stream-like object.

    HttpResponse.readable()[¶](#django.http.HttpResponse.readable)

Always `False`. This method makes an [HttpResponse](#django.http.HttpResponse) instance a
stream-like object.

    HttpResponse.seekable()[¶](#django.http.HttpResponse.seekable)

Always `False`. This method makes an [HttpResponse](#django.http.HttpResponse) instance a
stream-like object.

    HttpResponse.writable()[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponse.writable)[¶](#django.http.HttpResponse.writable)

Always `True`. This method makes an [HttpResponse](#django.http.HttpResponse) instance a
stream-like object.

    HttpResponse.writelines(*lines*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponse.writelines)[¶](#django.http.HttpResponse.writelines)

Writes a list of lines to the response. Line separators are not added. This
method makes an [HttpResponse](#django.http.HttpResponse) instance a stream-like object.

### HttpResponsesubclasses¶

Django includes a number of `HttpResponse` subclasses that handle different
types of HTTP responses. Like `HttpResponse`, these subclasses live in
[django.http](#module-django.http).

   *class*HttpResponseRedirect[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseRedirect)[¶](#django.http.HttpResponseRedirect)

The first argument to the constructor is required – the path to redirect
to. This can be a fully qualified URL
(e.g. `'https://www.yahoo.com/search/'`), an absolute path with no domain
(e.g. `'/search/'`), or even a relative path (e.g. `'search/'`). In that
last case, the client browser will reconstruct the full URL itself
according to the current path. See [HttpResponse](#django.http.HttpResponse) for other optional
constructor arguments. Note that this returns an HTTP status code 302.

   url[¶](#django.http.HttpResponseRedirect.url)

This read-only attribute represents the URL the response will redirect
to (equivalent to the `Location` response header).

     *class*HttpResponsePermanentRedirect[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponsePermanentRedirect)[¶](#django.http.HttpResponsePermanentRedirect)

Like [HttpResponseRedirect](#django.http.HttpResponseRedirect), but it returns a permanent redirect
(HTTP status code 301) instead of a “found” redirect (status code 302).

    *class*HttpResponseNotModified[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseNotModified)[¶](#django.http.HttpResponseNotModified)

The constructor doesn’t take any arguments and no content should be added
to this response. Use this to designate that a page hasn’t been modified
since the user’s last request (status code 304).

    *class*HttpResponseBadRequest[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseBadRequest)[¶](#django.http.HttpResponseBadRequest)

Acts just like [HttpResponse](#django.http.HttpResponse) but uses a 400 status code.

    *class*HttpResponseNotFound[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseNotFound)[¶](#django.http.HttpResponseNotFound)

Acts just like [HttpResponse](#django.http.HttpResponse) but uses a 404 status code.

    *class*HttpResponseForbidden[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseForbidden)[¶](#django.http.HttpResponseForbidden)

Acts just like [HttpResponse](#django.http.HttpResponse) but uses a 403 status code.

    *class*HttpResponseNotAllowed[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseNotAllowed)[¶](#django.http.HttpResponseNotAllowed)

Like [HttpResponse](#django.http.HttpResponse), but uses a 405 status code. The first argument
to the constructor is required: a list of permitted methods (e.g.
`['GET', 'POST']`).

    *class*HttpResponseGone[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseGone)[¶](#django.http.HttpResponseGone)

Acts just like [HttpResponse](#django.http.HttpResponse) but uses a 410 status code.

    *class*HttpResponseServerError[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseServerError)[¶](#django.http.HttpResponseServerError)

Acts just like [HttpResponse](#django.http.HttpResponse) but uses a 500 status code.

Note

If a custom subclass of [HttpResponse](#django.http.HttpResponse) implements a `render`
method, Django will treat it as emulating a
[SimpleTemplateResponse](https://docs.djangoproject.com/en/5.0/template-response/#django.template.response.SimpleTemplateResponse), and the
`render` method must itself return a valid response object.

#### Custom response classes¶

If you find yourself needing a response class that Django doesn’t provide, you
can create it with the help of [http.HTTPStatus](https://docs.python.org/3/library/http.html#http.HTTPStatus). For example:

```
from http import HTTPStatus
from django.http import HttpResponse

class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT
```

## JsonResponseobjects¶

   *class*JsonResponse(*data*, *encoder=DjangoJSONEncoder*, *safe=True*, *json_dumps_params=None*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#JsonResponse)[¶](#django.http.JsonResponse)

An [HttpResponse](#django.http.HttpResponse) subclass that helps to create a JSON-encoded
response. It inherits most behavior from its superclass with a couple
differences:

Its default `Content-Type` header is set to *application/json*.

The first parameter, `data`, should be a `dict` instance. If the
`safe` parameter is set to `False` (see below) it can be any
JSON-serializable object.

The `encoder`, which defaults to
[django.core.serializers.json.DjangoJSONEncoder](https://docs.djangoproject.com/en/topics/serialization/#django.core.serializers.json.DjangoJSONEncoder), will be used to
serialize the data. See [JSON serialization](https://docs.djangoproject.com/en/topics/serialization/#serialization-formats-json) for more details about this serializer.

The `safe` boolean parameter defaults to `True`. If it’s set to
`False`, any object can be passed for serialization (otherwise only
`dict` instances are allowed). If `safe` is `True` and a non-`dict`
object is passed as the first argument, a [TypeError](https://docs.python.org/3/library/exceptions.html#TypeError) will be raised.

The `json_dumps_params` parameter is a dictionary of keyword arguments
to pass to the `json.dumps()` call used to generate the response.

### Usage¶

Typical usage could look like:

```
>>> from django.http import JsonResponse
>>> response = JsonResponse({"foo": "bar"})
>>> response.content
b'{"foo": "bar"}'
```

#### Serializing non-dictionary objects¶

In order to serialize objects other than `dict` you must set the `safe`
parameter to `False`:

```
>>> response = JsonResponse([1, 2, 3], safe=False)
```

Without passing `safe=False`, a [TypeError](https://docs.python.org/3/library/exceptions.html#TypeError) will be raised.

Note that an API based on `dict` objects is more extensible, flexible, and
makes it easier to maintain forwards compatibility. Therefore, you should avoid
using non-dict objects in JSON-encoded response.

Warning

Before the [5th edition of ECMAScript](https://262.ecma-international.org/5.1/#sec-11.1.4) it was possible to
poison the JavaScript `Array` constructor. For this reason, Django does
not allow passing non-dict objects to the
[JsonResponse](#django.http.JsonResponse) constructor by default.  However, most
modern browsers implement ECMAScript 5 which removes this attack vector.
Therefore it is possible to disable this security precaution.

#### Changing the default JSON encoder¶

If you need to use a different JSON encoder class you can pass the `encoder`
parameter to the constructor method:

```
>>> response = JsonResponse(data, encoder=MyJSONEncoder)
```

## StreamingHttpResponseobjects¶

   *class*StreamingHttpResponse[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#StreamingHttpResponse)[¶](#django.http.StreamingHttpResponse)

The [StreamingHttpResponse](#django.http.StreamingHttpResponse) class is used to stream a response from
Django to the browser.

Advanced usage

[StreamingHttpResponse](#django.http.StreamingHttpResponse) is somewhat advanced, in that it is
important to know whether you’ll be serving your application synchronously
under WSGI or asynchronously under ASGI, and adjust your usage
appropriately.

Please read these notes with care.

An example usage of [StreamingHttpResponse](#django.http.StreamingHttpResponse) under WSGI is streaming
content when generating the response would take too long or uses too much
memory. For instance, it’s useful for [generating large CSV files](https://docs.djangoproject.com/en/howto/outputting-csv/#streaming-csv-files).

There are performance considerations when doing this, though. Django, under
WSGI, is designed for short-lived requests. Streaming responses will tie a
worker process for the entire duration of the response. This may result in poor
performance.

Generally speaking, you would perform expensive tasks outside of the
request-response cycle, rather than resorting to a streamed response.

When serving under ASGI, however, a [StreamingHttpResponse](#django.http.StreamingHttpResponse) need not
stop other requests from being served whilst waiting for I/O. This opens up
the possibility of long-lived requests for streaming content and implementing
patterns such as long-polling, and server-sent events.

Even under ASGI note, [StreamingHttpResponse](#django.http.StreamingHttpResponse) should only be used in
situations where it is absolutely required that the whole content isn’t
iterated before transferring the data to the client. Because the content can’t
be accessed, many middleware can’t function normally. For example the `ETag`
and `Content-Length` headers can’t be generated for streaming responses.

The [StreamingHttpResponse](#django.http.StreamingHttpResponse) is not a subclass of [HttpResponse](#django.http.HttpResponse),
because it features a slightly different API. However, it is almost identical,
with the following notable differences:

- It should be given an iterator that yields bytestrings, [memoryview](https://docs.python.org/3/library/stdtypes.html#memoryview),
  or strings as content. When serving under WSGI, this should be a sync
  iterator. When serving under ASGI, then it should be an async iterator.
- You cannot access its content, except by iterating the response object
  itself. This should only occur when the response is returned to the client:
  you should not iterate the response yourself.
  Under WSGI the response will be iterated synchronously. Under ASGI the
  response will be iterated asynchronously. (This is why the iterator type must
  match the protocol you’re using.)
  To avoid a crash, an incorrect iterator type will be mapped to the correct
  type during iteration, and a warning will be raised, but in order to do this
  the iterator must be fully-consumed, which defeats the purpose of using a
  [StreamingHttpResponse](#django.http.StreamingHttpResponse) at all.
- It has no `content` attribute. Instead, it has a
  [streaming_content](#django.http.StreamingHttpResponse.streaming_content) attribute. This can be used
  in middleware to wrap the response iterable, but should not be consumed.
- You cannot use the file-like object `tell()` or `write()` methods.
  Doing so will raise an exception.

The [HttpResponseBase](#django.http.HttpResponseBase) base class is common between
[HttpResponse](#django.http.HttpResponse) and [StreamingHttpResponse](#django.http.StreamingHttpResponse).

  Changed in Django 4.2:

Support for asynchronous iteration was added.

### Attributes¶

   StreamingHttpResponse.streaming_content[¶](#django.http.StreamingHttpResponse.streaming_content)

An iterator of the response content, bytestring encoded according to
[HttpResponse.charset](#django.http.HttpResponse.charset).

    StreamingHttpResponse.status_code[¶](#django.http.StreamingHttpResponse.status_code)

The [HTTP status code](https://datatracker.ietf.org/doc/html/rfc9110.html#section-15) for the response.

Unless [reason_phrase](#django.http.StreamingHttpResponse.reason_phrase) is explicitly set, modifying the value of
`status_code` outside the constructor will also modify the value of
`reason_phrase`.

    StreamingHttpResponse.reason_phrase[¶](#django.http.StreamingHttpResponse.reason_phrase)

The HTTP reason phrase for the response. It uses the [HTTP standard’s](https://datatracker.ietf.org/doc/html/rfc9110.html#section-15.1) default reason phrases.

Unless explicitly set, `reason_phrase` is determined by the value of
[status_code](#django.http.StreamingHttpResponse.status_code).

    StreamingHttpResponse.streaming[¶](#django.http.StreamingHttpResponse.streaming)

This is always `True`.

    StreamingHttpResponse.is_async[¶](#django.http.StreamingHttpResponse.is_async)  New in Django 4.2.

Boolean indicating whether [StreamingHttpResponse.streaming_content](#django.http.StreamingHttpResponse.streaming_content)
is an asynchronous iterator or not.

This is useful for middleware needing to wrap
[StreamingHttpResponse.streaming_content](#django.http.StreamingHttpResponse.streaming_content).

### Handling disconnects¶

  New in Django 5.0.

If the client disconnects during a streaming response, Django will cancel the
coroutine that is handling the response. If you want to clean up resources
manually, you can do so by catching the `asyncio.CancelledError`:

```
async def streaming_response():
    try:
        # Do some work here
        async for chunk in my_streaming_iterator():
            yield chunk
    except asyncio.CancelledError:
        # Handle disconnect
        ...
        raise

async def my_streaming_view(request):
    return StreamingHttpResponse(streaming_response())
```

This example only shows how to handle client disconnection while the response
is streaming. If you perform long-running operations in your view before
returning the `StreamingHttpResponse` object, then you may also want to
[handle disconnections in the view](https://docs.djangoproject.com/en/topics/async/#async-handling-disconnect) itself.

## FileResponseobjects¶

   *class*FileResponse(*open_file*, *as_attachment=False*, *filename=''*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#FileResponse)[¶](#django.http.FileResponse)

[FileResponse](#django.http.FileResponse) is a subclass of [StreamingHttpResponse](#django.http.StreamingHttpResponse)
optimized for binary files. It uses [wsgi.file_wrapper](https://peps.python.org/pep-3333/#optional-platform-specific-file-handling) if provided by the wsgi
server, otherwise it streams the file out in small chunks.

If `as_attachment=True`, the `Content-Disposition` header is set to
`attachment`, which asks the browser to offer the file to the user as a
download. Otherwise, a `Content-Disposition` header with a value of
`inline` (the browser default) will be set only if a filename is
available.

If `open_file` doesn’t have a name or if the name of `open_file` isn’t
appropriate, provide a custom file name using the `filename`  parameter.
Note that if you pass a file-like object like `io.BytesIO`, it’s your
task to `seek()` it before passing it to `FileResponse`.

The `Content-Length` header is automatically set when it can be guessed
from the content of `open_file`.

The `Content-Type` header is automatically set when it can be guessed
from the `filename`, or the name of `open_file`.

`FileResponse` accepts any file-like object with binary content, for example
a file open in binary mode like so:

```
>>> from django.http import FileResponse
>>> response = FileResponse(open("myfile.png", "rb"))
```

The file will be closed automatically, so don’t open it with a context manager.

Use under ASGI

Python’s file API is synchronous. This means that the file must be fully
consumed in order to be served under ASGI.

In order to stream a file asynchronously you need to use a third-party
package that provides an asynchronous file API, such as [aiofiles](https://github.com/Tinche/aiofiles).

### Methods¶

   FileResponse.set_headers(*open_file*)[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#FileResponse.set_headers)[¶](#django.http.FileResponse.set_headers)

This method is automatically called during the response initialization and
set various headers (`Content-Length`, `Content-Type`, and
`Content-Disposition`) depending on `open_file`.

## HttpResponseBaseclass¶

   *class*HttpResponseBase[[source]](https://docs.djangoproject.com/en/_modules/django/http/response/#HttpResponseBase)[¶](#django.http.HttpResponseBase)

The [HttpResponseBase](#django.http.HttpResponseBase) class is common to all Django responses.
It should not be used to create responses directly, but it can be
useful for type-checking.
