# Performance and optimization¶ and more

# Performance and optimization¶

# Performance and optimization¶

This document provides an overview of techniques and tools that can help get
your Django code running more efficiently - faster, and using fewer system
resources.

## Introduction¶

Generally one’s first concern is to write code that *works*, whose logic
functions as required to produce the expected output. Sometimes, however, this
will not be enough to make the code work as *efficiently* as one would like.

In this case, what’s needed is something - and in practice, often a collection
of things - to improve the code’s performance without, or only minimally,
affecting its behavior.

## General approaches¶

### What are you optimizingfor?¶

It’s important to have a clear idea what you mean by ‘performance’. There is
not just one metric of it.

Improved speed might be the most obvious aim for a program, but sometimes other
performance improvements might be sought, such as lower memory consumption or
fewer demands on the database or network.

Improvements in one area will often bring about improved performance in
another, but not always; sometimes one can even be at the expense of another.
For example, an improvement in a program’s speed might cause it to use more
memory. Even worse, it can be self-defeating - if the speed improvement is so
memory-hungry that the system starts to run out of memory, you’ll have done
more harm than good.

There are other trade-offs to bear in mind. Your own time is a valuable
resource, more precious than CPU time. Some improvements might be too difficult
to be worth implementing, or might affect the portability or maintainability of
the code. Not all performance improvements are worth the effort.

So, you need to know what performance improvements you are aiming for, and you
also need to know that you have a good reason for aiming in that direction -
and for that you need:

### Performance benchmarking¶

It’s no good just guessing or assuming where the inefficiencies lie in your
code.

#### Django tools¶

[django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar/) is a very handy tool that
provides insights into what your code is doing and how much time it spends
doing it. In particular it can show you all the SQL queries your page is
generating, and how long each one has taken.

Third-party panels are also available for the toolbar, that can (for example)
report on cache performance and template rendering times.

#### Third-party services¶

There are a number of free services that will analyze and report on the
performance of your site’s pages from the perspective of a remote HTTP client,
in effect simulating the experience of an actual user.

These can’t report on the internals of your code, but can provide a useful
insight into your site’s overall performance, including aspects that can’t be
adequately measured from within Django environment. Examples include:

- [Yahoo’s Yslow](http://yslow.org/)
- [Google PageSpeed](https://developers.google.com/speed/)

There are also several paid-for services that perform a similar analysis,
including some that are Django-aware and can integrate with your codebase to
profile its performance far more comprehensively.

### Get things right from the start¶

Some work in optimization involves tackling performance shortcomings, but some
of the work can be built-in to what you’d do anyway, as part of the good
practices you should adopt even before you start thinking about improving
performance.

In this respect Python is an excellent language to work with, because solutions
that look elegant and feel right usually are the best performing ones. As with
most skills, learning what “looks right” takes practice, but one of the most
useful guidelines is:

#### Work at the appropriate level¶

Django offers many different ways of approaching things, but just because it’s
possible to do something in a certain way doesn’t mean that it’s the most
appropriate way to do it. For example, you might find that you could calculate
the same thing - the number of items in a collection, perhaps - in a
`QuerySet`, in Python, or in a template.

However, it will almost always be faster to do this work at lower rather than
higher levels. At higher levels the system has to deal with objects through
multiple levels of abstraction and layers of machinery.

That is, the database can typically do things faster than Python can, which can
do them faster than the template language can:

```
# QuerySet operation on the database
# fast, because that's what databases are good at
my_bicycles.count()

# counting Python objects
# slower, because it requires a database query anyway, and processing
# of the Python objects
len(my_bicycles)
```

```

{{ my_bicycles|length }}
```

Generally speaking, the most appropriate level for the job is the lowest-level
one that it is comfortable to code for.

Note

The example above is merely illustrative.

Firstly, in a real-life case you need to consider what is happening before
and after your count to work out what’s an optimal way of doing it *in that
particular context*. The database optimization documents describes [a
case where counting in the template would be better](https://docs.djangoproject.com/en/5.0/db/optimization/#overuse-of-count-and-exists).

Secondly, there are other options to consider: in a real-life case, `{{
my_bicycles.count }}`, which invokes the `QuerySet` `count()` method
directly from the template, might be the most appropriate choice.

## Caching¶

Often it is expensive (that is, resource-hungry and slow) to compute a value,
so there can be huge benefit in saving the value to a quickly accessible cache,
ready for the next time it’s required.

It’s a sufficiently significant and powerful technique that Django includes a
comprehensive caching framework, as well as other smaller pieces of caching
functionality.

### The caching framework¶

Django’s [caching framework](https://docs.djangoproject.com/en/5.0/cache/) offers very significant
opportunities for performance gains, by saving dynamic content so that it
doesn’t need to be calculated for each request.

For convenience, Django offers different levels of cache granularity: you can
cache the output of specific views, or only the pieces that are difficult to
produce, or even an entire site.

Implementing caching should not be regarded as an alternative to improving code
that’s performing poorly because it has been written badly. It’s one of the
final steps toward producing well-performing code, not a shortcut.

### cached_property¶

It’s common to have to call a class instance’s method more than once. If
that function is expensive, then doing so can be wasteful.

Using the [cached_property](https://docs.djangoproject.com/en/ref/utils/#django.utils.functional.cached_property) decorator saves the
value returned by a property; the next time the function is called on that
instance, it will return the saved value rather than re-computing it. Note that
this only works on methods that take `self` as their only argument and that
it changes the method to a property.

Certain Django components also have their own caching functionality; these are
discussed below in the sections related to those components.

## Understanding laziness¶

*Laziness* is a strategy complementary to caching. Caching avoids
recomputation by saving results; laziness delays computation until it’s
actually required.

Laziness allows us to refer to things before they are instantiated, or even
before it’s possible to instantiate them. This has numerous uses.

For example, [lazy translation](https://docs.djangoproject.com/en/5.0/i18n/translation/#lazy-translations) can be used before the
target language is even known, because it doesn’t take place until the
translated string is actually required, such as in a rendered template.

Laziness is also a way to save effort by trying to avoid work in the first
place. That is, one aspect of laziness is not doing anything until it has to be
done, because it may not turn out to be necessary after all. Laziness can
therefore have performance implications, and the more expensive the work
concerned, the more there is to gain through laziness.

Python provides a number of tools for lazy evaluation, particularly through the
[generator](https://docs.python.org/3/glossary.html#term-generator) and [generator expression](https://docs.python.org/3/glossary.html#term-generator-expression) constructs. It’s worth
reading up on laziness in Python to discover opportunities for making use of
lazy patterns in your code.

### Laziness in Django¶

Django is itself quite lazy. A good example of this can be found in the
evaluation of `QuerySets`. [QuerySets are lazy](https://docs.djangoproject.com/en/5.0/db/queries/#querysets-are-lazy).
Thus a `QuerySet` can be created, passed around and combined with other
`QuerySets`, without actually incurring any trips to the database to fetch
the items it describes. What gets passed around is the `QuerySet` object, not
the collection of items that - eventually - will be required from the database.

On the other hand, [certain operations will force the evaluation of a
QuerySet](https://docs.djangoproject.com/en/ref/models/querysets/#when-querysets-are-evaluated). Avoiding the premature evaluation of
a `QuerySet` can save making an expensive and unnecessary trip to the
database.

Django also offers a [keep_lazy()](https://docs.djangoproject.com/en/ref/utils/#django.utils.functional.keep_lazy) decorator.
This allows a function that has been called with a lazy argument to behave
lazily itself, only being evaluated when it needs to be. Thus the lazy argument
- which could be an expensive one - will not be called upon for evaluation
until it’s strictly required.

## Databases¶

### Database optimization¶

Django’s database layer provides various ways to help developers get the best
performance from their databases. The [database optimization documentation](https://docs.djangoproject.com/en/5.0/db/optimization/) gathers together links to the relevant
documentation and adds various tips that outline the steps to take when
attempting to optimize your database usage.

### Other database-related tips¶

Enabling [Persistent connections](https://docs.djangoproject.com/en/ref/databases/#persistent-database-connections) can speed up connections to the
database accounts for a significant part of the request processing time.

This helps a lot on virtualized hosts with limited network performance, for example.

## HTTP performance¶

### Middleware¶

Django comes with a few helpful pieces of [middleware](https://docs.djangoproject.com/en/ref/middleware/)
that can help optimize your site’s performance. They include:

#### ConditionalGetMiddleware¶

Adds support for modern browsers to conditionally GET responses based on the
`ETag` and `Last-Modified` headers. It also calculates and sets an ETag if
needed.

#### GZipMiddleware¶

Compresses responses for all modern browsers, saving bandwidth and transfer
time. Note that GZipMiddleware is currently considered a security risk, and is
vulnerable to attacks that nullify the protection provided by TLS/SSL. See the
warning in [GZipMiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.gzip.GZipMiddleware) for more information.

### Sessions¶

#### Using cached sessions¶

[Using cached sessions](https://docs.djangoproject.com/en/5.0/http/sessions/#cached-sessions-backend) may be a way to increase
performance by eliminating the need to load session data from a slower storage
source like the database and instead storing frequently used session data in
memory.

### Static files¶

Static files, which by definition are not dynamic, make an excellent target for
optimization gains.

#### ManifestStaticFilesStorage¶

By taking advantage of web browsers’ caching abilities, you can
eliminate network hits entirely for a given file after the initial download.

[ManifestStaticFilesStorage](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#django.contrib.staticfiles.storage.ManifestStaticFilesStorage) appends a
content-dependent tag to the filenames of [static files](https://docs.djangoproject.com/en/ref/contrib/staticfiles/) to make it safe for browsers to cache them
long-term without missing future changes - when a file changes, so will the
tag, so browsers will reload the asset automatically.

#### “Minification”¶

Several third-party Django tools and packages provide the ability to “minify”
HTML, CSS, and JavaScript. They remove unnecessary whitespace, newlines, and
comments, and shorten variable names, and thus reduce the size of the documents
that your site publishes.

## Template performance¶

Note that:

- using `{% block %}` is faster than using `{% include %}`
- heavily-fragmented templates, assembled from many small pieces, can affect
  performance

### The cached template loader¶

Enabling the [cachedtemplateloader](https://docs.djangoproject.com/en/ref/templates/api/#django.template.loaders.cached.Loader) often improves performance
drastically, as it avoids compiling each template every time it needs to be
rendered.

## Using different versions of available software¶

It can sometimes be worth checking whether different and better-performing
versions of the software that you’re using are available.

These techniques are targeted at more advanced users who want to push the
boundaries of performance of an already well-optimized Django site.

However, they are not magic solutions to performance problems, and they’re
unlikely to bring better than marginal gains to sites that don’t already do the
more basic things the right way.

Note

It’s worth repeating: **reaching for alternatives to software you’re
already using is never the first answer to performance problems**. When
you reach this level of optimization, you need a formal benchmarking
solution.

### Newer is often - but not always - better¶

It’s fairly rare for a new release of well-maintained software to be less
efficient, but the maintainers can’t anticipate every possible use-case - so
while being aware that newer versions are likely to perform better, don’t
assume that they always will.

This is true of Django itself. Successive releases have offered a number of
improvements across the system, but you should still check the real-world
performance of your application, because in some cases you may find that
changes mean it performs worse rather than better.

Newer versions of Python, and also of Python packages, will often perform
better too - but measure, rather than assume.

Note

Unless you’ve encountered an unusual performance problem in a particular
version, you’ll generally find better features, reliability, and security
in a new release and that these benefits are far more significant than any
performance you might win or lose.

### Alternatives to Django’s template language¶

For nearly all cases, Django’s built-in template language is perfectly
adequate. However, if the bottlenecks in your Django project seem to lie in the
template system and you have exhausted other opportunities to remedy this, a
third-party alternative may be the answer.

[Jinja2](https://jinja.palletsprojects.com/) can offer performance improvements, particularly when it comes to
speed.

Alternative template systems vary in the extent to which they share Django’s
templating language.

Note

*If* you experience performance issues in templates, the first thing to do
is to understand exactly why. Using an alternative template system may
prove faster, but the same gains may also be available without going to
that trouble - for example, expensive processing and logic in your
templates could be done more efficiently in your views.

### Alternative software implementations¶

It may be worth checking whether Python software you’re using has been
provided in a different implementation that can execute the same code faster.

However: most performance problems in well-written Django sites aren’t at the
Python execution level, but rather in inefficient database querying, caching,
and templates. If you’re relying on poorly-written Python code, your
performance problems are unlikely to be solved by having it execute faster.

Using an alternative implementation may introduce compatibility, deployment,
portability, or maintenance issues. It goes without saying that before adopting
a non-standard implementation you should ensure it provides sufficient
performance gains for your application to outweigh the potential risks.

With these caveats in mind, you should be aware of:

#### PyPy¶

[PyPy](https://www.pypy.org/) is an implementation of Python in Python itself
(the ‘standard’ Python implementation is in C). PyPy can offer substantial
performance gains, typically for heavyweight applications.

A key aim of the PyPy project is [compatibility](https://www.pypy.org/compat.html) with existing Python APIs and libraries.
Django is compatible, but you will need to check the compatibility of other
libraries you rely on.

#### C implementations of Python libraries¶

Some Python libraries are also implemented in C, and can be much faster. They
aim to offer the same APIs. Note that compatibility issues and behavior
differences are not unknown (and not always immediately evident).

---

# Security in Django¶

# Security in Django¶

This document is an overview of Django’s security features. It includes advice
on securing a Django-powered site.

## Cross site scripting (XSS) protection¶

XSS attacks allow a user to inject client side scripts into the browsers of
other users. This is usually achieved by storing the malicious scripts in the
database where it will be retrieved and displayed to other users, or by getting
users to click a link which will cause the attacker’s JavaScript to be executed
by the user’s browser. However, XSS attacks can originate from any untrusted
source of data, such as cookies or web services, whenever the data is not
sufficiently sanitized before including in a page.

Using Django templates protects you against the majority of XSS attacks.
However, it is important to understand what protections it provides
and its limitations.

Django templates [escape specific characters](https://docs.djangoproject.com/en/ref/templates/language/#automatic-html-escaping)
which are particularly dangerous to HTML. While this protects users from most
malicious input, it is not entirely foolproof. For example, it will not
protect the following:

```
<style class={{ var }}>...</style>
```

If `var` is set to `'class1 onmouseover=javascript:func()'`, this can result
in unauthorized JavaScript execution, depending on how the browser renders
imperfect HTML. (Quoting the attribute value would fix this case.)

It is also important to be particularly careful when using `is_safe` with
custom template tags, the [safe](https://docs.djangoproject.com/en/ref/templates/builtins/#std-templatefilter-safe) template tag, [mark_safe](https://docs.djangoproject.com/en/ref/utils/#module-django.utils.safestring), and when autoescape is turned off.

In addition, if you are using the template system to output something other
than HTML, there may be entirely separate characters and words which require
escaping.

You should also be very careful when storing HTML in the database, especially
when that HTML is retrieved and displayed.

## Cross site request forgery (CSRF) protection¶

CSRF attacks allow a malicious user to execute actions using the credentials
of another user without that user’s knowledge or consent.

Django has built-in protection against most types of CSRF attacks, providing you
have [enabled and used it](https://docs.djangoproject.com/en/howto/csrf/#using-csrf) where appropriate. However, as with
any mitigation technique, there are limitations. For example, it is possible to
disable the CSRF module globally or for particular views. You should only do
this if you know what you are doing. There are other [limitations](https://docs.djangoproject.com/en/ref/csrf/#csrf-limitations) if your site has subdomains that are outside of your
control.

[CSRF protection works](https://docs.djangoproject.com/en/ref/csrf/#how-csrf-works) by checking for a secret in each
POST request. This ensures that a malicious user cannot “replay” a form POST to
your website and have another logged in user unwittingly submit that form. The
malicious user would have to know the secret, which is user specific (using a
cookie).

When deployed with [HTTPS](#security-recommendation-ssl),
`CsrfViewMiddleware` will check that the HTTP referer header is set to a
URL on the same origin (including subdomain and port). Because HTTPS
provides additional security, it is imperative to ensure connections use HTTPS
where it is available by forwarding insecure connection requests and using
HSTS for supported browsers.

Be very careful with marking views with the `csrf_exempt` decorator unless
it is absolutely necessary.

## SQL injection protection¶

SQL injection is a type of attack where a malicious user is able to execute
arbitrary SQL code on a database. This can result in records
being deleted or data leakage.

Django’s querysets are protected from SQL injection since their queries are
constructed using query parameterization. A query’s SQL code is defined
separately from the query’s parameters. Since parameters may be user-provided
and therefore unsafe, they are escaped by the underlying database driver.

Django also gives developers power to write [raw queries](https://docs.djangoproject.com/en/5.0/db/sql/#executing-raw-queries) or execute [custom sql](https://docs.djangoproject.com/en/5.0/db/sql/#executing-custom-sql).
These capabilities should be used sparingly and you should always be careful to
properly escape any parameters that the user can control. In addition, you
should exercise caution when using [extra()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.extra)
and [RawSQL](https://docs.djangoproject.com/en/ref/models/expressions/#django.db.models.expressions.RawSQL).

## Clickjacking protection¶

Clickjacking is a type of attack where a malicious site wraps another site
in a frame. This attack can result in an unsuspecting user being tricked
into performing unintended actions on the target site.

Django contains [clickjacking protection](https://docs.djangoproject.com/en/ref/clickjacking/#clickjacking-prevention) in
the form of the
[X-Frame-Optionsmiddleware](https://docs.djangoproject.com/en/ref/middleware/#django.middleware.clickjacking.XFrameOptionsMiddleware)
which in a supporting browser can prevent a site from being rendered inside
a frame. It is possible to disable the protection on a per view basis
or to configure the exact header value sent.

The middleware is strongly recommended for any site that does not need to have
its pages wrapped in a frame by third party sites, or only needs to allow that
for a small section of the site.

## SSL/HTTPS¶

It is always better for security to deploy your site behind HTTPS. Without
this, it is possible for malicious network users to sniff authentication
credentials or any other information transferred between client and server, and
in some cases – **active** network attackers – to alter data that is sent in
either direction.

If you want the protection that HTTPS provides, and have enabled it on your
server, there are some additional steps you may need:

- If necessary, set [SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECURE_PROXY_SSL_HEADER), ensuring that you have
  understood the warnings there thoroughly. Failure to do this can result
  in CSRF vulnerabilities, and failure to do it correctly can also be
  dangerous!
- Set [SECURE_SSL_REDIRECT](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECURE_SSL_REDIRECT) to `True`, so that requests over HTTP
  are redirected to HTTPS.
  Please note the caveats under [SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECURE_PROXY_SSL_HEADER). For the
  case of a reverse proxy, it may be easier or more secure to configure the
  main web server to do the redirect to HTTPS.
- Use ‘secure’ cookies.
  If a browser connects initially via HTTP, which is the default for most
  browsers, it is possible for existing cookies to be leaked. For this reason,
  you should set your [SESSION_COOKIE_SECURE](https://docs.djangoproject.com/en/ref/settings/#std-setting-SESSION_COOKIE_SECURE) and
  [CSRF_COOKIE_SECURE](https://docs.djangoproject.com/en/ref/settings/#std-setting-CSRF_COOKIE_SECURE) settings to `True`. This instructs the browser
  to only send these cookies over HTTPS connections. Note that this will mean
  that sessions will not work over HTTP, and the CSRF protection will prevent
  any POST data being accepted over HTTP (which will be fine if you are
  redirecting all HTTP traffic to HTTPS).
- Use [HTTP Strict Transport Security](https://docs.djangoproject.com/en/ref/middleware/#http-strict-transport-security) (HSTS)
  HSTS is an HTTP header that informs a browser that all future connections
  to a particular site should always use HTTPS. Combined with redirecting
  requests over HTTP to HTTPS, this will ensure that connections always enjoy
  the added security of SSL provided one successful connection has occurred.
  HSTS may either be configured with [SECURE_HSTS_SECONDS](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECURE_HSTS_SECONDS),
  [SECURE_HSTS_INCLUDE_SUBDOMAINS](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECURE_HSTS_INCLUDE_SUBDOMAINS), and [SECURE_HSTS_PRELOAD](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECURE_HSTS_PRELOAD),
  or on the web server.

## Host header validation¶

Django uses the `Host` header provided by the client to construct URLs in
certain cases. While these values are sanitized to prevent Cross Site Scripting
attacks, a fake `Host` value can be used for Cross-Site Request Forgery,
cache poisoning attacks, and poisoning links in emails.

Because even seemingly-secure web server configurations are susceptible to fake
`Host` headers, Django validates `Host` headers against the
[ALLOWED_HOSTS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ALLOWED_HOSTS) setting in the
[django.http.HttpRequest.get_host()](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.get_host) method.

This validation only applies via [get_host()](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpRequest.get_host);
if your code accesses the `Host` header directly from `request.META` you
are bypassing this security protection.

For more details see the full [ALLOWED_HOSTS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ALLOWED_HOSTS) documentation.

Warning

Previous versions of this document recommended configuring your web server to
ensure it validates incoming HTTP `Host` headers. While this is still
recommended, in many common web servers a configuration that seems to
validate the `Host` header may not in fact do so. For instance, even if
Apache is configured such that your Django site is served from a non-default
virtual host with the `ServerName` set, it is still possible for an HTTP
request to match this virtual host and supply a fake `Host` header. Thus,
Django now requires that you set [ALLOWED_HOSTS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ALLOWED_HOSTS) explicitly rather
than relying on web server configuration.

Additionally, Django requires you to explicitly enable support for the
`X-Forwarded-Host` header (via the [USE_X_FORWARDED_HOST](https://docs.djangoproject.com/en/ref/settings/#std-setting-USE_X_FORWARDED_HOST) setting)
if your configuration requires it.

## Referrer policy¶

Browsers use the `Referer` header as a way to send information to a site
about how users got there. By setting a *Referrer Policy* you can help to
protect the privacy of your users, restricting under which circumstances the
`Referer` header is set. See [the referrer policy section of the
security middleware reference](https://docs.djangoproject.com/en/ref/middleware/#referrer-policy) for details.

## Cross-origin opener policy¶

The cross-origin opener policy (COOP) header allows browsers to isolate a
top-level window from other documents by putting them in a different context
group so that they cannot directly interact with the top-level window. If a
document protected by COOP opens a cross-origin popup window, the popup’s
`window.opener` property will be `null`. COOP protects against cross-origin
attacks. See [the cross-origin opener policy section of the security
middleware reference](https://docs.djangoproject.com/en/ref/middleware/#cross-origin-opener-policy) for details.

## Session security¶

Similar to the [CSRF limitations](https://docs.djangoproject.com/en/ref/csrf/#csrf-limitations) requiring a site to
be deployed such that untrusted users don’t have access to any subdomains,
[django.contrib.sessions](https://docs.djangoproject.com/en/5.0/http/sessions/#module-django.contrib.sessions) also has limitations. See [the session
topic guide section on security](https://docs.djangoproject.com/en/5.0/http/sessions/#topics-session-security) for details.

## User-uploaded content¶

Note

Consider [serving static files from a cloud service or CDN](https://docs.djangoproject.com/en/howto/static-files/deployment/#staticfiles-from-cdn) to avoid some of these issues.

- If your site accepts file uploads, it is strongly advised that you limit
  these uploads in your web server configuration to a reasonable
  size in order to prevent denial of service (DOS) attacks. In Apache, this
  can be easily set using the [LimitRequestBody](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestbody) directive.
- If you are serving your own static files, be sure that handlers like Apache’s
  `mod_php`, which would execute static files as code, are disabled. You don’t
  want users to be able to execute arbitrary code by uploading and requesting a
  specially crafted file.
- Django’s media upload handling poses some vulnerabilities when that media is
  served in ways that do not follow security best practices. Specifically, an
  HTML file can be uploaded as an image if that file contains a valid PNG
  header followed by malicious HTML. This file will pass verification of the
  library that Django uses for [ImageField](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.ImageField) image
  processing (Pillow). When this file is subsequently displayed to a
  user, it may be displayed as HTML depending on the type and configuration of
  your web server.
  No bulletproof technical solution exists at the framework level to safely
  validate all user uploaded file content, however, there are some other steps
  you can take to mitigate these attacks:
  1. One class of attacks can be prevented by always serving user uploaded
    content from a distinct top-level or second-level domain. This prevents
    any exploit blocked by [same-origin policy](https://en.wikipedia.org/wiki/Same-origin_policy) protections such as cross
    site scripting. For example, if your site runs on `example.com`, you
    would want to serve uploaded content (the [MEDIA_URL](https://docs.djangoproject.com/en/ref/settings/#std-setting-MEDIA_URL) setting)
    from something like `usercontent-example.com`. It’s *not* sufficient to
    serve content from a subdomain like `usercontent.example.com`.
  2. Beyond this, applications may choose to define a list of allowable
    file extensions for user uploaded files and configure the web server
    to only serve such files.

## Additional security topics¶

While Django provides good security protection out of the box, it is still
important to properly deploy your application and take advantage of the
security protection of the web server, operating system and other components.

- Make sure that your Python code is outside of the web server’s root. This
  will ensure that your Python code is not accidentally served as plain text
  (or accidentally executed).
- Take care with any [user uploaded files](https://docs.djangoproject.com/en/ref/models/fields/#file-upload-security).
- Django does not throttle requests to authenticate users. To protect against
  brute-force attacks against the authentication system, you may consider
  deploying a Django plugin or web server module to throttle these requests.
- Keep your [SECRET_KEY](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECRET_KEY), and [SECRET_KEY_FALLBACKS](https://docs.djangoproject.com/en/ref/settings/#std-setting-SECRET_KEY_FALLBACKS) if in
  use, secret.
- It is a good idea to limit the accessibility of your caching system and
  database using a firewall.
- Take a look at the Open Web Application Security Project (OWASP) [Top 10
  list](https://owasp.org/Top10/) which identifies some common vulnerabilities in web applications. While
  Django has tools to address some of the issues, other issues must be
  accounted for in the design of your project.
- Mozilla discusses various topics regarding [web security](https://infosec.mozilla.org/guidelines/web_security.html). Their
  pages also include security principles that apply to any system.
