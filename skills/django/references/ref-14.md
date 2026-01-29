---

# Middleware¶

# Middleware¶

This document explains all middleware components that come with Django. For
information on how to use them and how to write your own middleware, see
the [middleware usage guide](https://docs.djangoproject.com/en/topics/http/middleware/).

## Available middleware¶

### Cache middleware¶

   *class*UpdateCacheMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/cache/#UpdateCacheMiddleware)[¶](#django.middleware.cache.UpdateCacheMiddleware)    *class*FetchFromCacheMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/cache/#FetchFromCacheMiddleware)[¶](#django.middleware.cache.FetchFromCacheMiddleware)

Enable the site-wide cache. If these are enabled, each Django-powered page will
be cached for as long as the [CACHE_MIDDLEWARE_SECONDS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CACHE_MIDDLEWARE_SECONDS) setting
defines. See the [cache documentation](https://docs.djangoproject.com/en/topics/cache/).

### “Common” middleware¶

   *class*CommonMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/common/#CommonMiddleware)[¶](#django.middleware.common.CommonMiddleware)

Adds a few conveniences for perfectionists:

- Forbids access to user agents in the [DISALLOWED_USER_AGENTS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DISALLOWED_USER_AGENTS)
  setting, which should be a list of compiled regular expression objects.
- Performs URL rewriting based on the [APPEND_SLASH](https://docs.djangoproject.com/en/5.0/settings/#std-setting-APPEND_SLASH) and
  [PREPEND_WWW](https://docs.djangoproject.com/en/5.0/settings/#std-setting-PREPEND_WWW) settings.
  If [APPEND_SLASH](https://docs.djangoproject.com/en/5.0/settings/#std-setting-APPEND_SLASH) is `True` and the initial URL doesn’t end
  with a slash, and it is not found in the URLconf, then a new URL is
  formed by appending a slash at the end. If this new URL is found in the
  URLconf, then Django redirects the request to this new URL. Otherwise,
  the initial URL is processed as usual.
  For example, `foo.com/bar` will be redirected to `foo.com/bar/` if
  you don’t have a valid URL pattern for `foo.com/bar` but *do* have a
  valid pattern for `foo.com/bar/`.
  If [PREPEND_WWW](https://docs.djangoproject.com/en/5.0/settings/#std-setting-PREPEND_WWW) is `True`, URLs that lack a leading “www.”
  will be redirected to the same URL with a leading “www.”
  Both of these options are meant to normalize URLs. The philosophy is that
  each URL should exist in one, and only one, place. Technically a URL
  `foo.com/bar` is distinct from `foo.com/bar/` – a search-engine
  indexer would treat them as separate URLs – so it’s best practice to
  normalize URLs.
  If necessary, individual views may be excluded from the `APPEND_SLASH`
  behavior using the [no_append_slash()](https://docs.djangoproject.com/en/topics/http/decorators/#django.views.decorators.common.no_append_slash)
  decorator:
  ```
  from django.views.decorators.common import no_append_slash
  @no_append_slash
  def sensitive_fbv(request, *args, **kwargs):
      """View to be excluded from APPEND_SLASH."""
      return HttpResponse()
  ```
- Sets the `Content-Length` header for non-streaming responses.

   CommonMiddleware.response_redirect_class[¶](#django.middleware.common.CommonMiddleware.response_redirect_class)

Defaults to [HttpResponsePermanentRedirect](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponsePermanentRedirect). Subclass
`CommonMiddleware` and override the attribute to customize the redirects
issued by the middleware.

   *class*BrokenLinkEmailsMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/common/#BrokenLinkEmailsMiddleware)[¶](#django.middleware.common.BrokenLinkEmailsMiddleware)

- Sends broken link notification emails to [MANAGERS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MANAGERS) (see
  [How to manage error reporting](https://docs.djangoproject.com/en/howto/error-reporting/)).

### GZip middleware¶

   *class*GZipMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/gzip/#GZipMiddleware)[¶](#django.middleware.gzip.GZipMiddleware)   max_random_bytes[¶](#django.middleware.gzip.GZipMiddleware.max_random_bytes)

Defaults to 100. Subclass `GZipMiddleware` and override the attribute
to change the maximum number of random bytes that is included with
compressed responses.

Note

Security researchers revealed that when compression techniques (including
`GZipMiddleware`) are used on a website, the site may become exposed to a
number of possible attacks.

To mitigate attacks, Django implements a technique called *Heal The Breach
(HTB)*. It adds up to 100 bytes (see
[max_random_bytes](#django.middleware.gzip.GZipMiddleware.max_random_bytes)) of random bytes to each response
to make the attacks less effective.

For more details, see the [BREACH paper (PDF)](https://www.breachattack.com/resources/BREACH%20-%20SSL,%20gone%20in%2030%20seconds.pdf), [breachattack.com](https://www.breachattack.com/), and
the [Heal The Breach (HTB) paper](https://ieeexplore.ieee.org/document/9754554).

   Changed in Django 4.2:

Mitigation for the BREACH attack was added.

The `django.middleware.gzip.GZipMiddleware` compresses content for browsers
that understand GZip compression (all modern browsers).

This middleware should be placed before any other middleware that need to
read or write the response body so that compression happens afterward.

It will NOT compress content if any of the following are true:

- The content body is less than 200 bytes long.
- The response has already set the `Content-Encoding` header.
- The request (the browser) hasn’t sent an `Accept-Encoding` header
  containing `gzip`.

If the response has an `ETag` header, the ETag is made weak to comply with
[RFC 9110 Section 8.8.1](https://datatracker.ietf.org/doc/html/rfc9110.html#section-8.8.1).

You can apply GZip compression to individual views using the
[gzip_page()](https://docs.djangoproject.com/en/topics/http/decorators/#django.views.decorators.gzip.gzip_page) decorator.

### Conditional GET middleware¶

   *class*ConditionalGetMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/http/#ConditionalGetMiddleware)[¶](#django.middleware.http.ConditionalGetMiddleware)

Handles conditional GET operations. If the response doesn’t have an `ETag`
header, the middleware adds one if needed. If the response has an `ETag` or
`Last-Modified` header, and the request has `If-None-Match` or
`If-Modified-Since`, the response is replaced by an
[HttpResponseNotModified](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponseNotModified).

### Locale middleware¶

   *class*LocaleMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/locale/#LocaleMiddleware)[¶](#django.middleware.locale.LocaleMiddleware)

Enables language selection based on data from the request. It customizes
content for each user. See the [internationalization documentation](https://docs.djangoproject.com/en/topics/i18n/translation/).

   LocaleMiddleware.response_redirect_class[¶](#django.middleware.locale.LocaleMiddleware.response_redirect_class)

Defaults to [HttpResponseRedirect](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponseRedirect). Subclass
`LocaleMiddleware` and override the attribute to customize the redirects
issued by the middleware.

### Message middleware¶

   *class*MessageMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/messages/middleware/#MessageMiddleware)[¶](#django.contrib.messages.middleware.MessageMiddleware)

Enables cookie- and session-based message support. See the
[messages documentation](https://docs.djangoproject.com/en/5.0/contrib/messages/).

### Security middleware¶

Warning

If your deployment situation allows, it’s usually a good idea to have your
front-end web server perform the functionality provided by the
`SecurityMiddleware`. That way, if there are requests that aren’t served
by Django (such as static media or user-uploaded files), they will have
the same protections as requests to your Django application.

    *class*SecurityMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/security/#SecurityMiddleware)[¶](#django.middleware.security.SecurityMiddleware)

The `django.middleware.security.SecurityMiddleware` provides several security
enhancements to the request/response cycle. Each one can be independently
enabled or disabled with a setting.

- [SECURE_CONTENT_TYPE_NOSNIFF](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_CONTENT_TYPE_NOSNIFF)
- [SECURE_CROSS_ORIGIN_OPENER_POLICY](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_CROSS_ORIGIN_OPENER_POLICY)
- [SECURE_HSTS_INCLUDE_SUBDOMAINS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_HSTS_INCLUDE_SUBDOMAINS)
- [SECURE_HSTS_PRELOAD](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_HSTS_PRELOAD)
- [SECURE_HSTS_SECONDS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_HSTS_SECONDS)
- [SECURE_REDIRECT_EXEMPT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_REDIRECT_EXEMPT)
- [SECURE_REFERRER_POLICY](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_REFERRER_POLICY)
- [SECURE_SSL_HOST](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_SSL_HOST)
- [SECURE_SSL_REDIRECT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_SSL_REDIRECT)

#### HTTP Strict Transport Security¶

For sites that should only be accessed over HTTPS, you can instruct modern
browsers to refuse to connect to your domain name via an insecure connection
(for a given period of time) by setting the [“Strict-Transport-Security”
header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security). This reduces your exposure to some SSL-stripping man-in-the-middle
(MITM) attacks.

`SecurityMiddleware` will set this header for you on all HTTPS responses if
you set the [SECURE_HSTS_SECONDS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_HSTS_SECONDS) setting to a non-zero integer value.

When enabling HSTS, it’s a good idea to first use a small value for testing,
for example, [SECURE_HSTS_SECONDS=3600](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_HSTS_SECONDS) for one
hour. Each time a web browser sees the HSTS header from your site, it will
refuse to communicate non-securely (using HTTP) with your domain for the given
period of time. Once you confirm that all assets are served securely on your
site (i.e. HSTS didn’t break anything), it’s a good idea to increase this value
so that infrequent visitors will be protected (31536000 seconds, i.e. 1 year,
is common).

Additionally, if you set the [SECURE_HSTS_INCLUDE_SUBDOMAINS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_HSTS_INCLUDE_SUBDOMAINS) setting
to `True`, `SecurityMiddleware` will add the `includeSubDomains` directive
to the `Strict-Transport-Security` header. This is recommended (assuming all
subdomains are served exclusively using HTTPS), otherwise your site may still
be vulnerable via an insecure connection to a subdomain.

If you wish to submit your site to the [browser preload list](https://hstspreload.org/), set the
[SECURE_HSTS_PRELOAD](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_HSTS_PRELOAD) setting to `True`. That appends the
`preload` directive to the `Strict-Transport-Security` header.

Warning

The HSTS policy applies to your entire domain, not just the URL of the
response that you set the header on. Therefore, you should only use it if
your entire domain is served via HTTPS only.

Browsers properly respecting the HSTS header will refuse to allow users to
bypass warnings and connect to a site with an expired, self-signed, or
otherwise invalid SSL certificate. If you use HSTS, make sure your
certificates are in good shape and stay that way!

Note

If you are deployed behind a load-balancer or reverse-proxy server, and the
`Strict-Transport-Security` header is not being added to your responses,
it may be because Django doesn’t realize that it’s on a secure connection;
you may need to set the [SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_PROXY_SSL_HEADER) setting.

#### Referrer Policy¶

Browsers use [the Referer header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer) as a way to send information to a site
about how users got there. When a user clicks a link, the browser will send the
full URL of the linking page as the referrer. While this can be useful for some
purposes – like figuring out who’s linking to your site – it also can cause
privacy concerns by informing one site that a user was visiting another site.

Some browsers have the ability to accept hints about whether they should send
the HTTP `Referer` header when a user clicks a link; this hint is provided
via [the Referrer-Policy header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy). This header can suggest any of three
behaviors to browsers:

- Full URL: send the entire URL in the `Referer` header. For example, if the
  user is visiting `https://example.com/page.html`, the `Referer` header
  would contain `"https://example.com/page.html"`.
- Origin only: send only the “origin” in the referrer. The origin consists of
  the scheme, host and (optionally) port number. For example, if the user is
  visiting `https://example.com/page.html`, the origin would be
  `https://example.com/`.
- No referrer: do not send a `Referer` header at all.

There are two types of conditions this header can tell a browser to watch out
for:

- Same-origin versus cross-origin: a link from `https://example.com/1.html`
  to `https://example.com/2.html` is same-origin. A link from
  `https://example.com/page.html` to `https://not.example.com/page.html` is
  cross-origin.
- Protocol downgrade: a downgrade occurs if the page containing the link is
  served via HTTPS, but the page being linked to is not served via HTTPS.

Warning

When your site is served via HTTPS, [Django’s CSRF protection system](https://docs.djangoproject.com/en/5.0/csrf/#how-csrf-works) requires the `Referer` header to be present, so
completely disabling the `Referer` header will interfere with CSRF
protection. To gain most of the benefits of disabling `Referer` headers
while also keeping CSRF protection, consider enabling only same-origin
referrers.

`SecurityMiddleware` can set the `Referrer-Policy` header for you, based on
the [SECURE_REFERRER_POLICY](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_REFERRER_POLICY) setting (note spelling: browsers send a
`Referer` header when a user clicks a link, but the header instructing a
browser whether to do so is spelled `Referrer-Policy`). The valid values for
this setting are:

  `no-referrer`

Instructs the browser to send no referrer for links clicked on this site.

  `no-referrer-when-downgrade`

Instructs the browser to send a full URL as the referrer, but only when no
protocol downgrade occurs.

  `origin`

Instructs the browser to send only the origin, not the full URL, as the
referrer.

  `origin-when-cross-origin`

Instructs the browser to send the full URL as the referrer for same-origin
links, and only the origin for cross-origin links.

  `same-origin`

Instructs the browser to send a full URL, but only for same-origin links. No
referrer will be sent for cross-origin links.

  `strict-origin`

Instructs the browser to send only the origin, not the full URL, and to send
no referrer when a protocol downgrade occurs.

  `strict-origin-when-cross-origin`

Instructs the browser to send the full URL when the link is same-origin and
no protocol downgrade occurs; send only the origin when the link is
cross-origin and no protocol downgrade occurs; and no referrer when a
protocol downgrade occurs.

  `unsafe-url`

Instructs the browser to always send the full URL as the referrer.

Unknown Policy Values

Where a policy value is [unknown](https://w3c.github.io/webappsec-referrer-policy/#unknown-policy-values) by a user agent, it is possible to
specify multiple policy values to provide a fallback. The last specified
value that is understood takes precedence. To support this, an iterable or
comma-separated string can be used with [SECURE_REFERRER_POLICY](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_REFERRER_POLICY).

#### Cross-Origin Opener Policy¶

Some browsers have the ability to isolate top-level windows from other
documents by putting them in a separate browsing context group based on the
value of the [Cross-Origin Opener Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy) (COOP) header. If a document that
is isolated in this way opens a cross-origin popup window, the popup’s
`window.opener` property will be `null`. Isolating windows using COOP is a
defense-in-depth protection against cross-origin attacks, especially those like
Spectre which allowed exfiltration of data loaded into a shared browsing
context.

`SecurityMiddleware` can set the `Cross-Origin-Opener-Policy` header for
you, based on the [SECURE_CROSS_ORIGIN_OPENER_POLICY](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_CROSS_ORIGIN_OPENER_POLICY) setting. The
valid values for this setting are:

  `same-origin`

Isolates the browsing context exclusively to same-origin documents.
Cross-origin documents are not loaded in the same browsing context. This
is the default and most secure option.

  `same-origin-allow-popups`

Isolates the browsing context to same-origin documents or those which
either don’t set COOP or which opt out of isolation by setting a COOP of
`unsafe-none`.

  `unsafe-none`

Allows the document to be added to its opener’s browsing context group
unless the opener itself has a COOP of `same-origin` or
`same-origin-allow-popups`.

#### X-Content-Type-Options:nosniff¶

Some browsers will try to guess the content types of the assets that they
fetch, overriding the `Content-Type` header. While this can help display
sites with improperly configured servers, it can also pose a security
risk.

If your site serves user-uploaded files, a malicious user could upload a
specially-crafted file that would be interpreted as HTML or JavaScript by
the browser when you expected it to be something harmless.

To prevent the browser from guessing the content type and force it to
always use the type provided in the `Content-Type` header, you can pass
the [X-Content-Type-Options: nosniff](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options) header.  `SecurityMiddleware` will
do this for all responses if the [SECURE_CONTENT_TYPE_NOSNIFF](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_CONTENT_TYPE_NOSNIFF) setting
is `True`.

Note that in most deployment situations where Django isn’t involved in serving
user-uploaded files, this setting won’t help you. For example, if your
[MEDIA_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_URL) is served directly by your front-end web server (nginx,
Apache, etc.) then you’d want to set this header there. On the other hand, if
you are using Django to do something like require authorization in order to
download files and you cannot set the header using your web server, this
setting will be useful.

#### SSL Redirect¶

If your site offers both HTTP and HTTPS connections, most users will end up
with an unsecured connection by default. For best security, you should redirect
all HTTP connections to HTTPS.

If you set the [SECURE_SSL_REDIRECT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_SSL_REDIRECT) setting to True,
`SecurityMiddleware` will permanently (HTTP 301) redirect all HTTP
connections to HTTPS.

Note

For performance reasons, it’s preferable to do these redirects outside of
Django, in a front-end load balancer or reverse-proxy server such as
[nginx](https://nginx.org/). [SECURE_SSL_REDIRECT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_SSL_REDIRECT) is intended for the deployment
situations where this isn’t an option.

If the [SECURE_SSL_HOST](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_SSL_HOST) setting has a value, all redirects will be
sent to that host instead of the originally-requested host.

If there are a few pages on your site that should be available over HTTP, and
not redirected to HTTPS, you can list regular expressions to match those URLs
in the [SECURE_REDIRECT_EXEMPT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_REDIRECT_EXEMPT) setting.

Note

If you are deployed behind a load-balancer or reverse-proxy server and
Django can’t seem to tell when a request actually is already secure, you
may need to set the [SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECURE_PROXY_SSL_HEADER) setting.

### Session middleware¶

   *class*SessionMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sessions/middleware/#SessionMiddleware)[¶](#django.contrib.sessions.middleware.SessionMiddleware)

Enables session support. See the [session documentation](https://docs.djangoproject.com/en/topics/http/sessions/).

### Site middleware¶

   *class*CurrentSiteMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sites/middleware/#CurrentSiteMiddleware)[¶](#django.contrib.sites.middleware.CurrentSiteMiddleware)

Adds the `site` attribute representing the current site to every incoming
`HttpRequest` object. See the [sites documentation](https://docs.djangoproject.com/en/5.0/contrib/sites/#site-middleware).

### Authentication middleware¶

   *class*AuthenticationMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/middleware/#AuthenticationMiddleware)[¶](#django.contrib.auth.middleware.AuthenticationMiddleware)

Adds the `user` attribute, representing the currently-logged-in user, to
every incoming `HttpRequest` object. See [Authentication in web requests](https://docs.djangoproject.com/en/topics/auth/default/#auth-web-requests).

   *class*RemoteUserMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/middleware/#RemoteUserMiddleware)[¶](#django.contrib.auth.middleware.RemoteUserMiddleware)

Middleware for utilizing web server provided authentication. See
[How to authenticate using REMOTE_USER](https://docs.djangoproject.com/en/howto/auth-remote-user/) for usage details.

   *class*PersistentRemoteUserMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/middleware/#PersistentRemoteUserMiddleware)[¶](#django.contrib.auth.middleware.PersistentRemoteUserMiddleware)

Middleware for utilizing web server provided authentication when enabled only
on the login page. See [Using REMOTE_USER on login pages only](https://docs.djangoproject.com/en/howto/auth-remote-user/#persistent-remote-user-middleware-howto) for usage
details.

### CSRF protection middleware¶

   *class*CsrfViewMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/csrf/#CsrfViewMiddleware)[¶](#django.middleware.csrf.CsrfViewMiddleware)

Adds protection against Cross Site Request Forgeries by adding hidden form
fields to POST forms and checking requests for the correct value. See the
[Cross Site Request Forgery protection documentation](https://docs.djangoproject.com/en/5.0/csrf/).

### X-Frame-Optionsmiddleware¶

   *class*XFrameOptionsMiddleware[[source]](https://docs.djangoproject.com/en/_modules/django/middleware/clickjacking/#XFrameOptionsMiddleware)[¶](#django.middleware.clickjacking.XFrameOptionsMiddleware)

Simple [clickjacking protection via the X-Frame-Options header](https://docs.djangoproject.com/en/5.0/clickjacking/).

## Middleware ordering¶

Here are some hints about the ordering of various Django middleware classes:

1. [SecurityMiddleware](#django.middleware.security.SecurityMiddleware)
  It should go near the top of the list if you’re going to turn on the SSL
  redirect as that avoids running through a bunch of other unnecessary
  middleware.
2. [UpdateCacheMiddleware](#django.middleware.cache.UpdateCacheMiddleware)
  Before those that modify the `Vary` header (`SessionMiddleware`,
  `GZipMiddleware`, `LocaleMiddleware`).
3. [GZipMiddleware](#django.middleware.gzip.GZipMiddleware)
  Before any middleware that may change or use the response body.
  After `UpdateCacheMiddleware`: Modifies `Vary` header.
4. [SessionMiddleware](#django.contrib.sessions.middleware.SessionMiddleware)
  Before any middleware that may raise an exception to trigger an error
  view (such as [PermissionDenied](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.PermissionDenied)) if you’re
  using [CSRF_USE_SESSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_USE_SESSIONS).
  After `UpdateCacheMiddleware`: Modifies `Vary` header.
5. [ConditionalGetMiddleware](#django.middleware.http.ConditionalGetMiddleware)
  Before any middleware that may change the response (it sets the `ETag`
  header).
  After `GZipMiddleware` so it won’t calculate an `ETag` header on gzipped
  contents.
6. [LocaleMiddleware](#django.middleware.locale.LocaleMiddleware)
  One of the topmost, after `SessionMiddleware` (uses session data) and
  `UpdateCacheMiddleware` (modifies `Vary` header).
7. [CommonMiddleware](#django.middleware.common.CommonMiddleware)
  Before any middleware that may change the response (it sets the
  `Content-Length` header). A middleware that appears before
  `CommonMiddleware` and changes the response must reset `Content-Length`.
  Close to the top: it redirects when [APPEND_SLASH](https://docs.djangoproject.com/en/5.0/settings/#std-setting-APPEND_SLASH) or
  [PREPEND_WWW](https://docs.djangoproject.com/en/5.0/settings/#std-setting-PREPEND_WWW) are set to `True`.
  After `SessionMiddleware` if you’re using [CSRF_USE_SESSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_USE_SESSIONS).
8. [CsrfViewMiddleware](#django.middleware.csrf.CsrfViewMiddleware)
  Before any view middleware that assumes that CSRF attacks have been dealt
  with.
  Before [RemoteUserMiddleware](#django.contrib.auth.middleware.RemoteUserMiddleware), or any
  other authentication middleware that may perform a login, and hence rotate
  the CSRF token, before calling down the middleware chain.
  After `SessionMiddleware` if you’re using [CSRF_USE_SESSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_USE_SESSIONS).
9. [AuthenticationMiddleware](#django.contrib.auth.middleware.AuthenticationMiddleware)
  After `SessionMiddleware`: uses session storage.
10. [MessageMiddleware](#django.contrib.messages.middleware.MessageMiddleware)
  After `SessionMiddleware`: can use session-based storage.
11. [FetchFromCacheMiddleware](#django.middleware.cache.FetchFromCacheMiddleware)
  After any middleware that modifies the `Vary` header: that header is used
  to pick a value for the cache hash-key.
12. [FlatpageFallbackMiddleware](https://docs.djangoproject.com/en/5.0/contrib/flatpages/#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware)
  Should be near the bottom as it’s a last-resort type of middleware.
13. [RedirectFallbackMiddleware](https://docs.djangoproject.com/en/5.0/contrib/redirects/#django.contrib.redirects.middleware.RedirectFallbackMiddleware)
  Should be near the bottom as it’s a last-resort type of middleware.

---

# Migration Operations¶

# Migration Operations¶

Migration files are composed of one or more `Operation`s, objects that
declaratively record what the migration should do to your database.

Django also uses these `Operation` objects to work out what your models
looked like historically, and to calculate what changes you’ve made to
your models since the last migration so it can automatically write
your migrations; that’s why they’re declarative, as it means Django can
easily load them all into memory and run through them without touching
the database to work out what your project should look like.

There are also more specialized `Operation` objects which are for things like
[data migrations](https://docs.djangoproject.com/en/topics/migrations/#data-migrations) and for advanced manual database
manipulation. You can also write your own `Operation` classes if you want
to encapsulate a custom change you commonly make.

If you need an empty migration file to write your own `Operation` objects
into, use `python manage.py makemigrations --empty yourappname`, but be aware
that manually adding schema-altering operations can confuse the migration
autodetector and make resulting runs of [makemigrations](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-makemigrations) output
incorrect code.

All of the core Django operations are available from the
`django.db.migrations.operations` module.

For introductory material, see the [migrations topic guide](https://docs.djangoproject.com/en/topics/migrations/).

## Schema Operations¶

### CreateModel¶

   *class*CreateModel(*name*, *fields*, *options=None*, *bases=None*, *managers=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#CreateModel)[¶](#django.db.migrations.operations.CreateModel)

Creates a new model in the project history and a corresponding table in the
database to match it.

`name` is the model name, as would be written in the `models.py` file.

`fields` is a list of 2-tuples of `(field_name, field_instance)`.
The field instance should be an unbound field (so just
`models.CharField(...)`, rather than a field taken from another model).

`options` is an optional dictionary of values from the model’s `Meta` class.

`bases` is an optional list of other classes to have this model inherit from;
it can contain both class objects as well as strings in the format
`"appname.ModelName"` if you want to depend on another model (so you inherit
from the historical version). If it’s not supplied, it defaults to inheriting
from the standard `models.Model`.

`managers` takes a list of 2-tuples of `(manager_name, manager_instance)`.
The first manager in the list will be the default manager for this model during
migrations.

### DeleteModel¶

   *class*DeleteModel(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#DeleteModel)[¶](#django.db.migrations.operations.DeleteModel)

Deletes the model from the project history and its table from the database.

### RenameModel¶

   *class*RenameModel(*old_name*, *new_name*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#RenameModel)[¶](#django.db.migrations.operations.RenameModel)

Renames the model from an old name to a new one.

You may have to manually add
this if you change the model’s name and quite a few of its fields at once; to
the autodetector, this will look like you deleted a model with the old name
and added a new one with a different name, and the migration it creates will
lose any data in the old table.

### AlterModelTable¶

   *class*AlterModelTable(*name*, *table*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AlterModelTable)[¶](#django.db.migrations.operations.AlterModelTable)

Changes the model’s table name (the [db_table](https://docs.djangoproject.com/en/5.0/models/options/#django.db.models.Options.db_table)
option on the `Meta` subclass).

### AlterModelTableComment¶

  New in Django 4.2.    *class*AlterModelTableComment(*name*, *table_comment*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AlterModelTableComment)[¶](#django.db.migrations.operations.AlterModelTableComment)

Changes the model’s table comment (the
[db_table_comment](https://docs.djangoproject.com/en/5.0/models/options/#django.db.models.Options.db_table_comment) option on the `Meta`
subclass).

### AlterUniqueTogether¶

   *class*AlterUniqueTogether(*name*, *unique_together*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AlterUniqueTogether)[¶](#django.db.migrations.operations.AlterUniqueTogether)

Changes the model’s set of unique constraints (the
[unique_together](https://docs.djangoproject.com/en/5.0/models/options/#django.db.models.Options.unique_together) option on the `Meta`
subclass).

### AlterIndexTogether¶

   *class*AlterIndexTogether(*name*, *index_together*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AlterIndexTogether)[¶](#django.db.migrations.operations.AlterIndexTogether)

Changes the model’s set of custom indexes (the `index_together` option on the
`Meta` subclass).

Warning

`AlterIndexTogether` is officially supported only for pre-Django 4.2
migration files. For backward compatibility reasons, it’s still part of the
public API, and there’s no plan to deprecate or remove it, but it should
not be used for new migrations. Use
[AddIndex](#django.db.migrations.operations.AddIndex) and
[RemoveIndex](#django.db.migrations.operations.RemoveIndex) operations instead.

### AlterOrderWithRespectTo¶

   *class*AlterOrderWithRespectTo(*name*, *order_with_respect_to*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AlterOrderWithRespectTo)[¶](#django.db.migrations.operations.AlterOrderWithRespectTo)

Makes or deletes the `_order` column needed for the
[order_with_respect_to](https://docs.djangoproject.com/en/5.0/models/options/#django.db.models.Options.order_with_respect_to) option on the `Meta`
subclass.

### AlterModelOptions¶

   *class*AlterModelOptions(*name*, *options*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AlterModelOptions)[¶](#django.db.migrations.operations.AlterModelOptions)

Stores changes to miscellaneous model options (settings on a model’s `Meta`)
like `permissions` and `verbose_name`. Does not affect the database, but
persists these changes for [RunPython](#django.db.migrations.operations.RunPython) instances to use. `options`
should be a dictionary mapping option names to values.

### AlterModelManagers¶

   *class*AlterModelManagers(*name*, *managers*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AlterModelManagers)[¶](#django.db.migrations.operations.AlterModelManagers)

Alters the managers that are available during migrations.

### AddField¶

   *class*AddField(*model_name*, *name*, *field*, *preserve_default=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/fields/#AddField)[¶](#django.db.migrations.operations.AddField)

Adds a field to a model. `model_name` is the model’s name, `name` is
the field’s name, and `field` is an unbound Field instance (the thing
you would put in the field declaration in `models.py` - for example,
`models.IntegerField(null=True)`.

The `preserve_default` argument indicates whether the field’s default
value is permanent and should be baked into the project state (`True`),
or if it is temporary and just for this migration (`False`) - usually
because the migration is adding a non-nullable field to a table and needs
a default value to put into existing rows. It does not affect the behavior
of setting defaults in the database directly - Django never sets database
defaults and always applies them in the Django ORM code.

Warning

On older databases, adding a field with a default value may cause a full
rewrite of the table. This happens even for nullable fields and may have a
negative performance impact. To avoid that, the following steps should be
taken.

- Add the nullable field without the default value and run the
  [makemigrations](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-makemigrations) command. This should generate a migration with
  an `AddField` operation.
- Add the default value to your field and run the [makemigrations](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-makemigrations)
  command. This should generate a migration with an `AlterField`
  operation.

### RemoveField¶

   *class*RemoveField(*model_name*, *name*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/fields/#RemoveField)[¶](#django.db.migrations.operations.RemoveField)

Removes a field from a model.

Bear in mind that when reversed, this is actually adding a field to a model.
The operation is reversible (apart from any data loss, which is irreversible)
if the field is nullable or if it has a default value that can be used to
populate the recreated column. If the field is not nullable and does not have a
default value, the operation is irreversible.

PostgreSQL

`RemoveField` will also delete any additional database objects that are
related to the removed field (like views, for example). This is because the
resulting `DROP COLUMN` statement will include the `CASCADE` clause to
ensure [dependent objects outside the table are also dropped](https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-PARMS-CASCADE).

### AlterField¶

   *class*AlterField(*model_name*, *name*, *field*, *preserve_default=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/fields/#AlterField)[¶](#django.db.migrations.operations.AlterField)

Alters a field’s definition, including changes to its type,
[null](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.null), [unique](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.unique),
[db_column](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.db_column) and other field attributes.

The `preserve_default` argument indicates whether the field’s default
value is permanent and should be baked into the project state (`True`),
or if it is temporary and just for this migration (`False`) - usually
because the migration is altering a nullable field to a non-nullable one and
needs a default value to put into existing rows. It does not affect the
behavior of setting defaults in the database directly - Django never sets
database defaults and always applies them in the Django ORM code.

Note that not all changes are possible on all databases - for example, you
cannot change a text-type field like `models.TextField()` into a number-type
field like `models.IntegerField()` on most databases.

### RenameField¶

   *class*RenameField(*model_name*, *old_name*, *new_name*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/fields/#RenameField)[¶](#django.db.migrations.operations.RenameField)

Changes a field’s name (and, unless [db_column](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.db_column)
is set, its column name).

### AddIndex¶

   *class*AddIndex(*model_name*, *index*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AddIndex)[¶](#django.db.migrations.operations.AddIndex)

Creates an index in the database table for the model with `model_name`.
`index` is an instance of the [Index](https://docs.djangoproject.com/en/5.0/models/indexes/#django.db.models.Index) class.

### RemoveIndex¶

   *class*RemoveIndex(*model_name*, *name*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#RemoveIndex)[¶](#django.db.migrations.operations.RemoveIndex)

Removes the index named `name` from the model with `model_name`.

### RenameIndex¶

   *class*RenameIndex(*model_name*, *new_name*, *old_name=None*, *old_fields=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#RenameIndex)[¶](#django.db.migrations.operations.RenameIndex)

Renames an index in the database table for the model with `model_name`.
Exactly one of `old_name` and `old_fields` can be provided. `old_fields`
is an iterable of the strings, often corresponding to fields of
[index_together](https://docs.djangoproject.com/en/5.0/models/options/#django.db.models.Options.index_together).

On databases that don’t support an index renaming statement (SQLite and MariaDB
< 10.5.2), the operation will drop and recreate the index, which can be
expensive.

### AddConstraint¶

   *class*AddConstraint(*model_name*, *constraint*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#AddConstraint)[¶](#django.db.migrations.operations.AddConstraint)

Creates a [constraint](https://docs.djangoproject.com/en/5.0/models/constraints/) in the database table for
the model with `model_name`.

### RemoveConstraint¶

   *class*RemoveConstraint(*model_name*, *name*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/models/#RemoveConstraint)[¶](#django.db.migrations.operations.RemoveConstraint)

Removes the constraint named `name` from the model with `model_name`.

## Special Operations¶

### RunSQL¶

   *class*RunSQL(*sql*, *reverse_sql=None*, *state_operations=None*, *hints=None*, *elidable=False*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/special/#RunSQL)[¶](#django.db.migrations.operations.RunSQL)

Allows running of arbitrary SQL on the database - useful for more advanced
features of database backends that Django doesn’t support directly.

`sql`, and `reverse_sql` if provided, should be strings of SQL to run on
the database. On most database backends (all but PostgreSQL), Django will
split the SQL into individual statements prior to executing them.

Warning

On PostgreSQL and SQLite, only use `BEGIN` or `COMMIT` in your SQL in
[non-atomic migrations](https://docs.djangoproject.com/en/howto/writing-migrations/#non-atomic-migrations), to avoid breaking
Django’s transaction state.

You can also pass a list of strings or 2-tuples. The latter is used for passing
queries and parameters in the same way as [cursor.execute()](https://docs.djangoproject.com/en/topics/db/sql/#executing-custom-sql). These three operations are equivalent:

```
migrations.RunSQL("INSERT INTO musician (name) VALUES ('Reinhardt');")
migrations.RunSQL([("INSERT INTO musician (name) VALUES ('Reinhardt');", None)])
migrations.RunSQL([("INSERT INTO musician (name) VALUES (%s);", ["Reinhardt"])])
```

If you want to include literal percent signs in the query, you have to double
them if you are passing parameters.

The `reverse_sql` queries are executed when the migration is unapplied. They
should undo what is done by the `sql` queries. For example, to undo the above
insertion with a deletion:

```
migrations.RunSQL(
    sql=[("INSERT INTO musician (name) VALUES (%s);", ["Reinhardt"])],
    reverse_sql=[("DELETE FROM musician where name=%s;", ["Reinhardt"])],
)
```

If `reverse_sql` is `None` (the default), the `RunSQL` operation is
irreversible.

The `state_operations` argument allows you to supply operations that are
equivalent to the SQL in terms of project state. For example, if you are
manually creating a column, you should pass in a list containing an `AddField`
operation here so that the autodetector still has an up-to-date state of the
model. If you don’t, when you next run `makemigrations`, it won’t see any
operation that adds that field and so will try to run it again. For example:

```
migrations.RunSQL(
    "ALTER TABLE musician ADD COLUMN name varchar(255) NOT NULL;",
    state_operations=[
        migrations.AddField(
            "musician",
            "name",
            models.CharField(max_length=255),
        ),
    ],
)
```

The optional `hints` argument will be passed as `**hints` to the
[allow_migrate()](https://docs.djangoproject.com/en/topics/db/multi-db/#allow_migrate) method of database routers to assist them in making
routing decisions. See [Hints](https://docs.djangoproject.com/en/topics/db/multi-db/#topics-db-multi-db-hints) for more details on
database hints.

The optional `elidable` argument determines whether or not the operation will
be removed (elided) when [squashing migrations](https://docs.djangoproject.com/en/topics/migrations/#migration-squashing).

   RunSQL.noop[¶](#django.db.migrations.operations.RunSQL.noop)

Pass the `RunSQL.noop` attribute to `sql` or `reverse_sql` when you
want the operation not to do anything in the given direction. This is
especially useful in making the operation reversible.

### RunPython¶

   *class*RunPython(*code*, *reverse_code=None*, *atomic=None*, *hints=None*, *elidable=False*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/special/#RunPython)[¶](#django.db.migrations.operations.RunPython)

Runs custom Python code in a historical context. `code` (and `reverse_code`
if supplied) should be callable objects that accept two arguments; the first is
an instance of `django.apps.registry.Apps` containing historical models that
match the operation’s place in the project history, and the second is an
instance of [SchemaEditor](https://docs.djangoproject.com/en/5.0/schema-editor/#django.db.backends.base.schema.BaseDatabaseSchemaEditor).

The `reverse_code` argument is called when unapplying migrations. This
callable should undo what is done in the `code` callable so that the
migration is reversible. If `reverse_code` is `None` (the default), the
`RunPython` operation is irreversible.

The optional `hints` argument will be passed as `**hints` to the
[allow_migrate()](https://docs.djangoproject.com/en/topics/db/multi-db/#allow_migrate) method of database routers to assist them in making a
routing decision. See [Hints](https://docs.djangoproject.com/en/topics/db/multi-db/#topics-db-multi-db-hints) for more details on
database hints.

The optional `elidable` argument determines whether or not the operation will
be removed (elided) when [squashing migrations](https://docs.djangoproject.com/en/topics/migrations/#migration-squashing).

You are advised to write the code as a separate function above the `Migration`
class in the migration file, and pass it to `RunPython`. Here’s an example of
using `RunPython` to create some initial objects on a `Country` model:

```
from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Country = apps.get_model("myapp", "Country")
    db_alias = schema_editor.connection.alias
    Country.objects.using(db_alias).bulk_create(
        [
            Country(name="USA", code="us"),
            Country(name="France", code="fr"),
        ]
    )

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Country = apps.get_model("myapp", "Country")
    db_alias = schema_editor.connection.alias
    Country.objects.using(db_alias).filter(name="USA", code="us").delete()
    Country.objects.using(db_alias).filter(name="France", code="fr").delete()

class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
```

This is generally the operation you would use to create
[data migrations](https://docs.djangoproject.com/en/topics/migrations/#data-migrations), run
custom data updates and alterations, and anything else you need access to an
ORM and/or Python code for.

Much like [RunSQL](#django.db.migrations.operations.RunSQL), ensure that if you change schema inside here you’re
either doing it outside the scope of the Django model system (e.g. triggers)
or that you use [SeparateDatabaseAndState](#django.db.migrations.operations.SeparateDatabaseAndState) to add in operations that will
reflect your changes to the model state - otherwise, the versioned ORM and
the autodetector will stop working correctly.

By default, `RunPython` will run its contents inside a transaction on
databases that do not support DDL transactions (for example, MySQL and
Oracle). This should be safe, but may cause a crash if you attempt to use
the `schema_editor` provided on these backends; in this case, pass
`atomic=False` to the `RunPython` operation.

On databases that do support DDL transactions (SQLite and PostgreSQL),
`RunPython` operations do not have any transactions automatically added
besides the transactions created for each migration. Thus, on PostgreSQL, for
example, you should avoid combining schema changes and `RunPython` operations
in the same migration or you may hit errors like `OperationalError: cannot
ALTER TABLE "mytable" because it has pending trigger events`.

If you have a different database and aren’t sure if it supports DDL
transactions, check the `django.db.connection.features.can_rollback_ddl`
attribute.

If the `RunPython` operation is part of a [non-atomic migration](https://docs.djangoproject.com/en/howto/writing-migrations/#non-atomic-migrations), the operation will only be executed in a transaction
if `atomic=True` is passed to the `RunPython` operation.

Warning

`RunPython` does not magically alter the connection of the models for you;
any model methods you call will go to the default database unless you
give them the current database alias (available from
`schema_editor.connection.alias`, where `schema_editor` is the second
argument to your function).

    *static*RunPython.noop()[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/special/#RunPython.noop)[¶](#django.db.migrations.operations.RunPython.noop)

Pass the `RunPython.noop` method to `code` or `reverse_code` when
you want the operation not to do anything in the given direction. This is
especially useful in making the operation reversible.

### SeparateDatabaseAndState¶

   *class*SeparateDatabaseAndState(*database_operations=None*, *state_operations=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/migrations/operations/special/#SeparateDatabaseAndState)[¶](#django.db.migrations.operations.SeparateDatabaseAndState)

A highly specialized operation that lets you mix and match the database
(schema-changing) and state (autodetector-powering) aspects of operations.

It accepts two lists of operations. When asked to apply state, it will use the
`state_operations` list (this is a generalized version of [RunSQL](#django.db.migrations.operations.RunSQL)’s
`state_operations` argument). When asked to apply changes to the database, it
will use the `database_operations` list.

If the actual state of the database and Django’s view of the state get out of
sync, this can break the migration framework, even leading to data loss. It’s
worth exercising caution and checking your database and state operations
carefully. You can use [sqlmigrate](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-sqlmigrate) and [dbshell](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-dbshell) to check
your database operations. You can use [makemigrations](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-makemigrations), especially
with [--dry-run](https://docs.djangoproject.com/en/5.0/django-admin/#cmdoption-makemigrations-dry-run), to check your state
operations.

For an example using `SeparateDatabaseAndState`, see
[Changing a ManyToManyField to use a through model](https://docs.djangoproject.com/en/howto/writing-migrations/#changing-a-manytomanyfield-to-use-a-through-model).

## Writing your own¶

Operations have a relatively simple API, and they’re designed so that you can
easily write your own to supplement the built-in Django ones. The basic
structure of an `Operation` looks like this:

```
from django.db.migrations.operations.base import Operation

class MyCustomOperation(Operation):
    # If this is False, it means that this operation will be ignored by
    # sqlmigrate; if true, it will be run and the SQL collected for its output.
    reduces_to_sql = False

    # If this is False, Django will refuse to reverse past this operation.
    reversible = False

    def __init__(self, arg1, arg2):
        # Operations are usually instantiated with arguments in migration
        # files. Store the values of them on self for later use.
        pass

    def state_forwards(self, app_label, state):
        # The Operation should take the 'state' parameter (an instance of
        # django.db.migrations.state.ProjectState) and mutate it to match
        # any schema changes that have occurred.
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        # The Operation should use schema_editor to apply any changes it
        # wants to make to the database.
        pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        # If reversible is True, this is called when the operation is reversed.
        pass

    def describe(self):
        # This is used to describe what the operation does in console output.
        return "Custom Operation"

    @property
    def migration_name_fragment(self):
        # Optional. A filename part suitable for automatically naming a
        # migration containing this operation, or None if not applicable.
        return "custom_operation_%s_%s" % (self.arg1, self.arg2)
```

You can take this template and work from it, though we suggest looking at the
built-in Django operations in `django.db.migrations.operations` - they cover
a lot of the example usage of semi-internal aspects of the migration framework
like `ProjectState` and the patterns used to get historical models, as well
as `ModelState` and the patterns used to mutate historical models in
`state_forwards()`.

Some things to note:

- You don’t need to learn too much about `ProjectState` to write migrations;
  just know that it has an `apps` property that gives access to an app
  registry (which you can then call `get_model` on).
- `database_forwards` and `database_backwards` both get two states passed
  to them; these represent the difference the `state_forwards` method would
  have applied, but are given to you for convenience and speed reasons.
- If you want to work with model classes or model instances from the
  `from_state` argument in `database_forwards()` or
  `database_backwards()`, you must render model states using the
  `clear_delayed_apps_cache()` method to make related models available:
  ```
  def database_forwards(self, app_label, schema_editor, from_state, to_state):
      # This operation should have access to all models. Ensure that all models are
      # reloaded in case any are delayed.
      from_state.clear_delayed_apps_cache()
      ...
  ```
- `to_state` in the database_backwards method is the *older* state; that is,
  the one that will be the current state once the migration has finished reversing.
- You might see implementations of `references_model` on the built-in
  operations; this is part of the autodetection code and does not matter for
  custom operations.

Warning

For performance reasons, the [Field](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field) instances in
`ModelState.fields` are reused across migrations. You must never change
the attributes on these instances. If you need to mutate a field in
`state_forwards()`, you must remove the old instance from
`ModelState.fields` and add a new instance in its place. The same is true
for the [Manager](https://docs.djangoproject.com/en/topics/db/managers/#django.db.models.Manager) instances in
`ModelState.managers`.

As an example, let’s make an operation that loads PostgreSQL extensions (which
contain some of PostgreSQL’s more exciting features). Since there’s no model
state changes, all it does is run one command:

```
from django.db.migrations.operations.base import Operation

class LoadExtension(Operation):
    reversible = True

    def __init__(self, name):
        self.name = name

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("CREATE EXTENSION IF NOT EXISTS %s" % self.name)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("DROP EXTENSION %s" % self.name)

    def describe(self):
        return "Creates extension %s" % self.name

    @property
    def migration_name_fragment(self):
        return "create_extension_%s" % self.name
```
