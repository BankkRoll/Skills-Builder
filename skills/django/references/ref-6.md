# The sitemap framework¶ and more

# The sitemap framework¶

# The sitemap framework¶

Django comes with a high-level sitemap-generating framework to create [sitemap](https://www.sitemaps.org/)
XML files.

## Overview¶

A sitemap is an XML file on your website that tells search-engine indexers how
frequently your pages change and how “important” certain pages are in relation
to other pages on your site. This information helps search engines index your
site.

The Django sitemap framework automates the creation of this XML file by letting
you express this information in Python code.

It works much like Django’s [syndication framework](https://docs.djangoproject.com/en/5.0/ref/syndication/). To create a sitemap, write a
[Sitemap](#django.contrib.sitemaps.Sitemap) class and point to it in your
[URLconf](https://docs.djangoproject.com/en/topics/http/urls/).

## Installation¶

To install the sitemap app, follow these steps:

1. Add `'django.contrib.sitemaps'` to your [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting.
2. Make sure your [TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES) setting contains a `DjangoTemplates`
  backend whose `APP_DIRS` options is set to `True`. It’s in there by
  default, so you’ll only need to change this if you’ve changed that setting.
3. Make sure you’ve installed the [sitesframework](https://docs.djangoproject.com/en/5.0/ref/sites/#module-django.contrib.sites).

(Note: The sitemap application doesn’t install any database tables. The only
reason it needs to go into [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) is so that the
[Loader()](https://docs.djangoproject.com/en/5.0/templates/api/#django.template.loaders.app_directories.Loader) template
loader can find the default templates.)

## Initialization¶

   views.sitemap(*request*, *sitemaps*, *section=None*, *template_name='sitemap.xml'*, *content_type='application/xml'*)[¶](#django.contrib.sitemaps.views.sitemap)

To activate sitemap generation on your Django site, add this line to your
[URLconf](https://docs.djangoproject.com/en/topics/http/urls/):

```
from django.contrib.sitemaps.views import sitemap

path(
    "sitemap.xml",
    sitemap,
    {"sitemaps": sitemaps},
    name="django.contrib.sitemaps.views.sitemap",
)
```

This tells Django to build a sitemap when a client accesses `/sitemap.xml`.

The name of the sitemap file is not important, but the location is. Search
engines will only index links in your sitemap for the current URL level and
below. For instance, if `sitemap.xml` lives in your root directory, it may
reference any URL in your site. However, if your sitemap lives at
`/content/sitemap.xml`, it may only reference URLs that begin with
`/content/`.

The sitemap view takes an extra, required argument: `{'sitemaps': sitemaps}`.
`sitemaps` should be a dictionary that maps a short section label (e.g.,
`blog` or `news`) to its [Sitemap](#django.contrib.sitemaps.Sitemap) class
(e.g., `BlogSitemap` or `NewsSitemap`). It may also map to an *instance* of
a [Sitemap](#django.contrib.sitemaps.Sitemap) class (e.g.,
`BlogSitemap(some_var)`).

## Sitemapclasses¶

A [Sitemap](#django.contrib.sitemaps.Sitemap) class is a Python class that
represents a “section” of entries in your sitemap. For example, one
[Sitemap](#django.contrib.sitemaps.Sitemap) class could represent all the entries
of your blog, while another could represent all of the events in your events
calendar.

In the simplest case, all these sections get lumped together into one
`sitemap.xml`, but it’s also possible to use the framework to generate a
sitemap index that references individual sitemap files, one per section. (See
[Creating a sitemap index](#creating-a-sitemap-index) below.)

[Sitemap](#django.contrib.sitemaps.Sitemap) classes must subclass
`django.contrib.sitemaps.Sitemap`. They can live anywhere in your codebase.

## An example¶

Let’s assume you have a blog system, with an `Entry` model, and you want your
sitemap to include all the links to your individual blog entries. Here’s how
your sitemap class might look:

```
from django.contrib.sitemaps import Sitemap
from blog.models import Entry

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.objects.filter(is_draft=False)

    def lastmod(self, obj):
        return obj.pub_date
```

Note:

- [changefreq](#django.contrib.sitemaps.Sitemap.changefreq) and [priority](#django.contrib.sitemaps.Sitemap.priority) are class
  attributes corresponding to `<changefreq>` and `<priority>` elements,
  respectively. They can be made callable as functions, as
  [lastmod](#django.contrib.sitemaps.Sitemap.lastmod) was in the example.
- [items()](#django.contrib.sitemaps.Sitemap.items) is a method that returns a [sequence](https://docs.python.org/3/glossary.html#term-sequence) or
  `QuerySet` of objects. The objects returned will get passed to any callable
  methods corresponding to a sitemap property ([location](#django.contrib.sitemaps.Sitemap.location),
  [lastmod](#django.contrib.sitemaps.Sitemap.lastmod), [changefreq](#django.contrib.sitemaps.Sitemap.changefreq), and
  [priority](#django.contrib.sitemaps.Sitemap.priority)).
- [lastmod](#django.contrib.sitemaps.Sitemap.lastmod) should return a [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime).
- There is no [location](#django.contrib.sitemaps.Sitemap.location) method in this example, but you
  can provide it in order to specify the URL for your object. By default,
  [location()](#django.contrib.sitemaps.Sitemap.location) calls `get_absolute_url()` on each object
  and returns the result.

## Sitemapclass reference¶

   *class*Sitemap[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sitemaps/#Sitemap)[¶](#django.contrib.sitemaps.Sitemap)

A `Sitemap` class can define the following methods/attributes:

   items[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sitemaps/#Sitemap.items)[¶](#django.contrib.sitemaps.Sitemap.items)

**Required.** A method that returns a [sequence](https://docs.python.org/3/glossary.html#term-sequence) or `QuerySet`
of objects. The framework doesn’t care what *type* of objects they are;
all that matters is that these objects get passed to the
[location()](#django.contrib.sitemaps.Sitemap.location), [lastmod()](#django.contrib.sitemaps.Sitemap.lastmod),
[changefreq()](#django.contrib.sitemaps.Sitemap.changefreq) and [priority()](#django.contrib.sitemaps.Sitemap.priority) methods.

    location[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sitemaps/#Sitemap.location)[¶](#django.contrib.sitemaps.Sitemap.location)

**Optional.** Either a method or attribute.

If it’s a method, it should return the absolute path for a given object
as returned by [items()](#django.contrib.sitemaps.Sitemap.items).

If it’s an attribute, its value should be a string representing an
absolute path to use for *every* object returned by
[items()](#django.contrib.sitemaps.Sitemap.items).

In both cases, “absolute path” means a URL that doesn’t include the
protocol or domain. Examples:

- Good: `'/foo/bar/'`
- Bad: `'example.com/foo/bar/'`
- Bad: `'https://example.com/foo/bar/'`

If [location](#django.contrib.sitemaps.Sitemap.location) isn’t provided, the framework will call
the `get_absolute_url()` method on each object as returned by
[items()](#django.contrib.sitemaps.Sitemap.items).

To specify a protocol other than `'http'`, use
[protocol](#django.contrib.sitemaps.Sitemap.protocol).

    lastmod[¶](#django.contrib.sitemaps.Sitemap.lastmod)

**Optional.** Either a method or attribute.

If it’s a method, it should take one argument – an object as returned
by [items()](#django.contrib.sitemaps.Sitemap.items) – and return that object’s last-modified
date/time as a [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime).

If it’s an attribute, its value should be a [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime)
representing the last-modified date/time for *every* object returned by
[items()](#django.contrib.sitemaps.Sitemap.items).

If all items in a sitemap have a [lastmod](#django.contrib.sitemaps.Sitemap.lastmod), the sitemap
generated by [views.sitemap()](#django.contrib.sitemaps.views.sitemap) will have a `Last-Modified`
header equal to the latest `lastmod`. You can activate the
[ConditionalGetMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.middleware.http.ConditionalGetMiddleware) to make
Django respond appropriately to requests with an `If-Modified-Since`
header which will prevent sending the sitemap if it hasn’t changed.

    paginator[¶](#django.contrib.sitemaps.Sitemap.paginator)

**Optional.**

This property returns a [Paginator](https://docs.djangoproject.com/en/5.0/paginator/#django.core.paginator.Paginator) for
[items()](#django.contrib.sitemaps.Sitemap.items). If you generate sitemaps in a batch you may
want to override this as a cached property in order to avoid multiple
`items()` calls.

    changefreq[¶](#django.contrib.sitemaps.Sitemap.changefreq)

**Optional.** Either a method or attribute.

If it’s a method, it should take one argument – an object as returned
by [items()](#django.contrib.sitemaps.Sitemap.items) – and return that object’s change
frequency as a string.

If it’s an attribute, its value should be a string representing the
change frequency of *every* object returned by [items()](#django.contrib.sitemaps.Sitemap.items).

Possible values for [changefreq](#django.contrib.sitemaps.Sitemap.changefreq), whether you use a
method or attribute, are:

- `'always'`
- `'hourly'`
- `'daily'`
- `'weekly'`
- `'monthly'`
- `'yearly'`
- `'never'`

    priority[¶](#django.contrib.sitemaps.Sitemap.priority)

**Optional.** Either a method or attribute.

If it’s a method, it should take one argument – an object as returned
by [items()](#django.contrib.sitemaps.Sitemap.items) – and return that object’s priority as
either a string or float.

If it’s an attribute, its value should be either a string or float
representing the priority of *every* object returned by
[items()](#django.contrib.sitemaps.Sitemap.items).

Example values for [priority](#django.contrib.sitemaps.Sitemap.priority): `0.4`, `1.0`. The
default priority of a page is `0.5`. See the [sitemaps.org
documentation](https://www.sitemaps.org/protocol.html#prioritydef) for more.

    protocol[¶](#django.contrib.sitemaps.Sitemap.protocol)

**Optional.**

This attribute defines the protocol (`'http'` or `'https'`) of the
URLs in the sitemap. If it isn’t set, the protocol with which the
sitemap was requested is used. If the sitemap is built outside the
context of a request, the default is `'https'`.

  Changed in Django 5.0:

In older versions, the default protocol for sitemaps built outside
the context of a request was `'http'`.

     limit[¶](#django.contrib.sitemaps.Sitemap.limit)

**Optional.**

This attribute defines the maximum number of URLs included on each page
of the sitemap. Its value should not exceed the default value of
`50000`, which is the upper limit allowed in the [Sitemaps protocol](https://www.sitemaps.org/protocol.html#index).

    i18n[¶](#django.contrib.sitemaps.Sitemap.i18n)

**Optional.**

A boolean attribute that defines if the URLs of this sitemap should
be generated using all of your [LANGUAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-LANGUAGES). The default is
`False`.

    languages[¶](#django.contrib.sitemaps.Sitemap.languages)

**Optional.**

A [sequence](https://docs.python.org/3/glossary.html#term-sequence) of [language codes](https://docs.djangoproject.com/en/topics/i18n/#term-language-code) to use for
generating alternate links when [i18n](#django.contrib.sitemaps.Sitemap.i18n) is enabled.
Defaults to [LANGUAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-LANGUAGES).

    alternates[¶](#django.contrib.sitemaps.Sitemap.alternates)

**Optional.**

A boolean attribute. When used in conjunction with
[i18n](#django.contrib.sitemaps.Sitemap.i18n) generated URLs will each have a list of alternate
links pointing to other language versions using the [hreflang
attribute](https://developers.google.com/search/docs/advanced/crawling/localized-versions). The default is `False`.

    x_default[¶](#django.contrib.sitemaps.Sitemap.x_default)

**Optional.**

A boolean attribute. When `True` the alternate links generated by
[alternates](#django.contrib.sitemaps.Sitemap.alternates) will contain a `hreflang="x-default"`
fallback entry with a value of [LANGUAGE_CODE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-LANGUAGE_CODE). The default is
`False`.

    get_latest_lastmod()[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sitemaps/#Sitemap.get_latest_lastmod)[¶](#django.contrib.sitemaps.Sitemap.get_latest_lastmod)

**Optional.** A method that returns the latest value returned by
[lastmod](#django.contrib.sitemaps.Sitemap.lastmod). This function is used to add the `lastmod`
attribute to [Sitemap index context
variables](#sitemap-index-context-variables).

By default [get_latest_lastmod()](#django.contrib.sitemaps.Sitemap.get_latest_lastmod) returns:

- If [lastmod](#django.contrib.sitemaps.Sitemap.lastmod) is an attribute:
  [lastmod](#django.contrib.sitemaps.Sitemap.lastmod).
- If [lastmod](#django.contrib.sitemaps.Sitemap.lastmod) is a method:
  The latest `lastmod` returned by calling the method with all
  items returned by [Sitemap.items()](#django.contrib.sitemaps.Sitemap.items).

    get_languages_for_item(*item*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sitemaps/#Sitemap.get_languages_for_item)[¶](#django.contrib.sitemaps.Sitemap.get_languages_for_item)  New in Django 4.2.

**Optional.** A method that returns the sequence of language codes for
which the item is displayed. By default
[get_languages_for_item()](#django.contrib.sitemaps.Sitemap.get_languages_for_item) returns
[languages](#django.contrib.sitemaps.Sitemap.languages).

## Shortcuts¶

The sitemap framework provides a convenience class for a common case:

   *class*GenericSitemap(*info_dict*, *priority=None*, *changefreq=None*, *protocol=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sitemaps/#GenericSitemap)[¶](#django.contrib.sitemaps.GenericSitemap)

The [django.contrib.sitemaps.GenericSitemap](#django.contrib.sitemaps.GenericSitemap) class allows you to
create a sitemap by passing it a dictionary which has to contain at least
a `queryset` entry. This queryset will be used to generate the items
of the sitemap. It may also have a `date_field` entry that
specifies a date field for objects retrieved from the `queryset`.
This will be used for the [lastmod](#django.contrib.sitemaps.Sitemap.lastmod) attribute and
[get_latest_lastmod()](#django.contrib.sitemaps.Sitemap.get_latest_lastmod) methods in the in the
generated sitemap.

The [priority](#django.contrib.sitemaps.Sitemap.priority), [changefreq](#django.contrib.sitemaps.Sitemap.changefreq),
and [protocol](#django.contrib.sitemaps.Sitemap.protocol) keyword arguments allow specifying these
attributes for all URLs.

### Example¶

Here’s an example of a [URLconf](https://docs.djangoproject.com/en/topics/http/urls/) using
[GenericSitemap](#django.contrib.sitemaps.GenericSitemap):

```
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from blog.models import Entry

info_dict = {
    "queryset": Entry.objects.all(),
    "date_field": "pub_date",
}

urlpatterns = [
    # some generic view using info_dict
    # ...
    # the sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"blog": GenericSitemap(info_dict, priority=0.6)}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
```

## Sitemap for static views¶

Often you want the search engine crawlers to index views which are neither
object detail pages nor flatpages. The solution is to explicitly list URL
names for these views in `items` and call [reverse()](https://docs.djangoproject.com/en/5.0/urlresolvers/#django.urls.reverse) in
the `location` method of the sitemap. For example:

```
# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["main", "about", "license"]

    def location(self, item):
        return reverse(item)

# urls.py
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .sitemaps import StaticViewSitemap
from . import views

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", views.main, name="main"),
    path("about/", views.about, name="about"),
    path("license/", views.license, name="license"),
    # ...
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
```

## Creating a sitemap index¶

   views.index(*request*, *sitemaps*, *template_name='sitemap_index.xml'*, *content_type='application/xml'*, *sitemap_url_name='django.contrib.sitemaps.views.sitemap'*)[¶](#django.contrib.sitemaps.views.index)

The sitemap framework also has the ability to create a sitemap index that
references individual sitemap files, one per each section defined in your
`sitemaps` dictionary. The only differences in usage are:

- You use two views in your URLconf: [django.contrib.sitemaps.views.index()](#django.contrib.sitemaps.views.index)
  and [django.contrib.sitemaps.views.sitemap()](#django.contrib.sitemaps.views.sitemap).
- The [django.contrib.sitemaps.views.sitemap()](#django.contrib.sitemaps.views.sitemap) view should take a
  `section` keyword argument.

Here’s what the relevant URLconf lines would look like for the example above:

```
from django.contrib.sitemaps import views

urlpatterns = [
    path(
        "sitemap.xml",
        views.index,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        "sitemap-<section>.xml",
        views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
```

This will automatically generate a `sitemap.xml` file that references
both `sitemap-flatpages.xml` and `sitemap-blog.xml`. The
[Sitemap](#django.contrib.sitemaps.Sitemap) classes and the `sitemaps`
dict don’t change at all.

If all sitemaps have a `lastmod` returned by
[Sitemap.get_latest_lastmod()](#django.contrib.sitemaps.Sitemap.get_latest_lastmod) the sitemap index will have a
`Last-Modified` header equal to the latest `lastmod`.

You should create an index file if one of your sitemaps has more than 50,000
URLs. In this case, Django will automatically paginate the sitemap, and the
index will reflect that.

If you’re not using the vanilla sitemap view – for example, if it’s wrapped
with a caching decorator – you must name your sitemap view and pass
`sitemap_url_name` to the index view:

```
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path(
        "sitemap.xml",
        cache_page(86400)(sitemaps_views.index),
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemaps"},
    ),
    path(
        "sitemap-<section>.xml",
        cache_page(86400)(sitemaps_views.sitemap),
        {"sitemaps": sitemaps},
        name="sitemaps",
    ),
]
```

## Template customization¶

If you wish to use a different template for each sitemap or sitemap index
available on your site, you may specify it by passing a `template_name`
parameter to the `sitemap` and `index` views via the URLconf:

```
from django.contrib.sitemaps import views

urlpatterns = [
    path(
        "custom-sitemap.xml",
        views.index,
        {"sitemaps": sitemaps, "template_name": "custom_sitemap.html"},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        "custom-sitemap-<section>.xml",
        views.sitemap,
        {"sitemaps": sitemaps, "template_name": "custom_sitemap.html"},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
```

These views return [TemplateResponse](https://docs.djangoproject.com/en/5.0/template-response/#django.template.response.TemplateResponse)
instances which allow you to easily customize the response data before
rendering. For more details, see the [TemplateResponse documentation](https://docs.djangoproject.com/en/5.0/template-response/).

### Context variables¶

When customizing the templates for the
[index()](#django.contrib.sitemaps.views.index) and
[sitemap()](#django.contrib.sitemaps.views.sitemap) views, you can rely on the
following context variables.

### Index¶

The variable `sitemaps` is a list of objects containing the `location` and
`lastmod` attribute for each of the sitemaps. Each URL exposes the following
attributes:

- `location`: The location (url & page) of the sitemap.
- `lastmod`: Populated by the [get_latest_lastmod()](#django.contrib.sitemaps.Sitemap.get_latest_lastmod)
  method for each sitemap.

### Sitemap¶

The variable `urlset` is a list of URLs that should appear in the
sitemap. Each URL exposes attributes as defined in the
[Sitemap](#django.contrib.sitemaps.Sitemap) class:

- `alternates`
- `changefreq`
- `item`
- `lastmod`
- `location`
- `priority`

The `alternates` attribute is available when [i18n](#django.contrib.sitemaps.Sitemap.i18n) and
[alternates](#django.contrib.sitemaps.Sitemap.alternates) are enabled. It is a list of other language
versions, including the optional [x_default](#django.contrib.sitemaps.Sitemap.x_default) fallback, for each
URL. Each alternate is a dictionary with `location` and `lang_code` keys.

The `item` attribute has been added for each URL to allow more flexible
customization of the templates, such as [Google news sitemaps](https://support.google.com/news/publisher-center/answer/9606710). Assuming
Sitemap’s [items()](#django.contrib.sitemaps.Sitemap.items) would return a list of items with
`publication_data` and a `tags` field something like this would
generate a Google News compatible sitemap:

```
<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="https://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
{% spaceless %}
{% for url in urlset %}
  <url>
    <loc>{{ url.location }}</loc>
    {% if url.lastmod %}<lastmod>{{ url.lastmod|date:"Y-m-d" }}</lastmod>{% endif %}
    {% if url.changefreq %}<changefreq>{{ url.changefreq }}</changefreq>{% endif %}
    {% if url.priority %}<priority>{{ url.priority }}</priority>{% endif %}
    <news:news>
      {% if url.item.publication_date %}<news:publication_date>{{ url.item.publication_date|date:"Y-m-d" }}</news:publication_date>{% endif %}
      {% if url.item.tags %}<news:keywords>{{ url.item.tags }}</news:keywords>{% endif %}
    </news:news>
   </url>
{% endfor %}
{% endspaceless %}
</urlset>
```

---

# The “sites” framework¶

# The “sites” framework¶

Django comes with an optional “sites” framework. It’s a hook for associating
objects and functionality to particular websites, and it’s a holding place for
the domain names and “verbose” names of your Django-powered sites.

Use it if your single Django installation powers more than one site and you
need to differentiate between those sites in some way.

The sites framework is mainly based on this model:

   *class*models.Site[¶](#django.contrib.sites.models.Site)

A model for storing the `domain` and `name` attributes of a website.

   domain[¶](#django.contrib.sites.models.Site.domain)

The fully qualified domain name associated with the website.
For example, `www.example.com`.

    name[¶](#django.contrib.sites.models.Site.name)

A human-readable “verbose” name for the website.

The [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) setting specifies the database ID of the
[Site](#django.contrib.sites.models.Site) object associated with that
particular settings file. If the setting is omitted, the
[get_current_site()](#django.contrib.sites.shortcuts.get_current_site) function will
try to get the current site by comparing the
[domain](#django.contrib.sites.models.Site.domain) with the host name from
the [request.get_host()](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest.get_host) method.

How you use this is up to you, but Django uses it in a couple of ways
automatically via a couple of conventions.

## Example usage¶

Why would you use sites? It’s best explained through examples.

### Associating content with multiple sites¶

The [LJWorld.com](https://www2.ljworld.com/) and Lawrence.com sites were operated by the same news
organization – the Lawrence Journal-World newspaper in Lawrence, Kansas.
LJWorld.com focused on news, while Lawrence.com focused on local entertainment.
But sometimes editors wanted to publish an article on *both* sites.

The naive way of solving the problem would be to require site producers to
publish the same story twice: once for LJWorld.com and again for Lawrence.com.
But that’s inefficient for site producers, and it’s redundant to store
multiple copies of the same story in the database.

A better solution removes the content duplication: Both sites use the same
article database, and an article is associated with one or more sites. In
Django model terminology, that’s represented by a
[ManyToManyField](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ManyToManyField) in the `Article` model:

```
from django.contrib.sites.models import Site
from django.db import models

class Article(models.Model):
    headline = models.CharField(max_length=200)
    # ...
    sites = models.ManyToManyField(Site)
```

This accomplishes several things quite nicely:

- It lets the site producers edit all content – on both sites – in a
  single interface (the Django admin).
- It means the same story doesn’t have to be published twice in the
  database; it only has a single record in the database.
- It lets the site developers use the same Django view code for both sites.
  The view code that displays a given story checks to make sure the requested
  story is on the current site. It looks something like this:
  ```
  from django.contrib.sites.shortcuts import get_current_site
  def article_detail(request, article_id):
      try:
          a = Article.objects.get(id=article_id, sites__id=get_current_site(request).id)
      except Article.DoesNotExist:
          raise Http404("Article does not exist on this site")
      # ...
  ```

### Associating content with a single site¶

Similarly, you can associate a model to the
[Site](#django.contrib.sites.models.Site)
model in a many-to-one relationship, using
[ForeignKey](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey).

For example, if an article is only allowed on a single site, you’d use a model
like this:

```
from django.contrib.sites.models import Site
from django.db import models

class Article(models.Model):
    headline = models.CharField(max_length=200)
    # ...
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
```

This has the same benefits as described in the last section.

### Hooking into the current site from views¶

You can use the sites framework in your Django views to do
particular things based on the site in which the view is being called.
For example:

```
from django.conf import settings

def my_view(request):
    if settings.SITE_ID == 3:
        # Do something.
        pass
    else:
        # Do something else.
        pass
```

It’s fragile to hard-code the site IDs like that, in case they change. The
cleaner way of accomplishing the same thing is to check the current site’s
domain:

```
from django.contrib.sites.shortcuts import get_current_site

def my_view(request):
    current_site = get_current_site(request)
    if current_site.domain == "foo.com":
        # Do something
        pass
    else:
        # Do something else.
        pass
```

This has also the advantage of checking if the sites framework is installed,
and return a [RequestSite](#django.contrib.sites.requests.RequestSite) instance if
it is not.

If you don’t have access to the request object, you can use the
`get_current()` method of the [Site](#django.contrib.sites.models.Site)
model’s manager. You should then ensure that your settings file does contain
the [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) setting. This example is equivalent to the previous one:

```
from django.contrib.sites.models import Site

def my_function_without_request():
    current_site = Site.objects.get_current()
    if current_site.domain == "foo.com":
        # Do something
        pass
    else:
        # Do something else.
        pass
```

### Getting the current domain for display¶

LJWorld.com and Lawrence.com both have email alert functionality, which lets
readers sign up to get notifications when news happens. It’s pretty basic: A
reader signs up on a web form and immediately gets an email saying,
“Thanks for your subscription.”

It’d be inefficient and redundant to implement this sign up processing code
twice, so the sites use the same code behind the scenes. But the “thank you for
signing up” notice needs to be different for each site. By using
[Site](#django.contrib.sites.models.Site)
objects, we can abstract the “thank you” notice to use the values of the
current site’s [name](#django.contrib.sites.models.Site.name) and
[domain](#django.contrib.sites.models.Site.domain).

Here’s an example of what the form-handling view looks like:

```
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

def register_for_newsletter(request):
    # Check form values, etc., and subscribe the user.
    # ...

    current_site = get_current_site(request)
    send_mail(
        "Thanks for subscribing to %s alerts" % current_site.name,
        "Thanks for your subscription. We appreciate it.\n\n-The %s team."
        % (current_site.name,),
        "editor@%s" % current_site.domain,
        [user.email],
    )

    # ...
```

On Lawrence.com, this email has the subject line “Thanks for subscribing to
lawrence.com alerts.” On LJWorld.com, the email has the subject “Thanks for
subscribing to LJWorld.com alerts.” Same goes for the email’s message body.

Note that an even more flexible (but more heavyweight) way of doing this would
be to use Django’s template system. Assuming Lawrence.com and LJWorld.com have
different template directories ([DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES-DIRS)), you could
farm out to the template system like so:

```
from django.core.mail import send_mail
from django.template import loader

def register_for_newsletter(request):
    # Check form values, etc., and subscribe the user.
    # ...

    subject = loader.get_template("alerts/subject.txt").render({})
    message = loader.get_template("alerts/message.txt").render({})
    send_mail(subject, message, "editor@ljworld.com", [user.email])

    # ...
```

In this case, you’d have to create `subject.txt` and `message.txt`
template files for both the LJWorld.com and Lawrence.com template directories.
That gives you more flexibility, but it’s also more complex.

It’s a good idea to exploit the [Site](#django.contrib.sites.models.Site)
objects as much as possible, to remove unneeded complexity and redundancy.

### Getting the current domain for full URLs¶

Django’s `get_absolute_url()` convention is nice for getting your objects’
URL without the domain name, but in some cases you might want to display the
full URL – with `http://` and the domain and everything – for an object.
To do this, you can use the sites framework. An example:

```
>>> from django.contrib.sites.models import Site
>>> obj = MyModel.objects.get(id=3)
>>> obj.get_absolute_url()
'/mymodel/objects/3/'
>>> Site.objects.get_current().domain
'example.com'
>>> "https://%s%s" % (Site.objects.get_current().domain, obj.get_absolute_url())
'https://example.com/mymodel/objects/3/'
```

## Enabling the sites framework¶

To enable the sites framework, follow these steps:

1. Add `'django.contrib.sites'` to your [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting.
2. Define a [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) setting:
  ```
  SITE_ID = 1
  ```
3. Run [migrate](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-migrate).

`django.contrib.sites` registers a
[post_migrate](https://docs.djangoproject.com/en/5.0/signals/#django.db.models.signals.post_migrate) signal handler which creates a
default site named `example.com` with the domain `example.com`. This site
will also be created after Django creates the test database. To set the
correct name and domain for your project, you can use a [data migration](https://docs.djangoproject.com/en/topics/migrations/#data-migrations).

In order to serve different sites in production, you’d create a separate
settings file with each `SITE_ID` (perhaps importing from a common settings
file to avoid duplicating shared settings) and then specify the appropriate
[DJANGO_SETTINGS_MODULE](https://docs.djangoproject.com/en/topics/settings/#envvar-DJANGO_SETTINGS_MODULE) for each site.

## Caching the currentSiteobject¶

As the current site is stored in the database, each call to
`Site.objects.get_current()` could result in a database query. But Django is a
little cleverer than that: on the first request, the current site is cached, and
any subsequent call returns the cached data instead of hitting the database.

If for any reason you want to force a database query, you can tell Django to
clear the cache using `Site.objects.clear_cache()`:

```
# First call; current site fetched from database.
current_site = Site.objects.get_current()
# ...

# Second call; current site fetched from cache.
current_site = Site.objects.get_current()
# ...

# Force a database query for the third call.
Site.objects.clear_cache()
current_site = Site.objects.get_current()
```

## TheCurrentSiteManager¶

   *class*managers.CurrentSiteManager[¶](#django.contrib.sites.managers.CurrentSiteManager)

If [Site](#django.contrib.sites.models.Site) plays a key role in your
application, consider using the helpful
[CurrentSiteManager](#django.contrib.sites.managers.CurrentSiteManager) in your
model(s). It’s a model [manager](https://docs.djangoproject.com/en/topics/db/managers/) that
automatically filters its queries to include only objects associated
with the current [Site](#django.contrib.sites.models.Site).

Mandatory [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID)

The `CurrentSiteManager` is only usable when the [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID)
setting is defined in your settings.

Use [CurrentSiteManager](#django.contrib.sites.managers.CurrentSiteManager) by adding it to
your model explicitly. For example:

```
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models

class Photo(models.Model):
    photo = models.FileField(upload_to="photos")
    photographer_name = models.CharField(max_length=100)
    pub_date = models.DateField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    objects = models.Manager()
    on_site = CurrentSiteManager()
```

With this model, `Photo.objects.all()` will return all `Photo` objects in
the database, but `Photo.on_site.all()` will return only the `Photo` objects
associated with the current site, according to the [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) setting.

Put another way, these two statements are equivalent:

```
Photo.objects.filter(site=settings.SITE_ID)
Photo.on_site.all()
```

How did [CurrentSiteManager](#django.contrib.sites.managers.CurrentSiteManager)
know which field of `Photo` was the
[Site](#django.contrib.sites.models.Site)? By default,
[CurrentSiteManager](#django.contrib.sites.managers.CurrentSiteManager) looks for a
either a [ForeignKey](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey) called
`site` or a
[ManyToManyField](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ManyToManyField) called
`sites` to filter on. If you use a field named something other than
`site` or `sites` to identify which
[Site](#django.contrib.sites.models.Site) objects your object is
related to, then you need to explicitly pass the custom field name as
a parameter to
[CurrentSiteManager](#django.contrib.sites.managers.CurrentSiteManager) on your
model. The following model, which has a field called `publish_on`,
demonstrates this:

```
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models

class Photo(models.Model):
    photo = models.FileField(upload_to="photos")
    photographer_name = models.CharField(max_length=100)
    pub_date = models.DateField()
    publish_on = models.ForeignKey(Site, on_delete=models.CASCADE)
    objects = models.Manager()
    on_site = CurrentSiteManager("publish_on")
```

If you attempt to use [CurrentSiteManager](#django.contrib.sites.managers.CurrentSiteManager)
and pass a field name that doesn’t exist, Django will raise a `ValueError`.

Finally, note that you’ll probably want to keep a normal
(non-site-specific) `Manager` on your model, even if you use
[CurrentSiteManager](#django.contrib.sites.managers.CurrentSiteManager). As
explained in the [manager documentation](https://docs.djangoproject.com/en/topics/db/managers/), if
you define a manager manually, then Django won’t create the automatic
`objects = models.Manager()` manager for you. Also note that certain
parts of Django – namely, the Django admin site and generic views –
use whichever manager is defined *first* in the model, so if you want
your admin site to have access to all objects (not just site-specific
ones), put `objects = models.Manager()` in your model, before you
define [CurrentSiteManager](#django.contrib.sites.managers.CurrentSiteManager).

## Site middleware¶

If you often use this pattern:

```
from django.contrib.sites.models import Site

def my_view(request):
    site = Site.objects.get_current()
    ...
```

To avoid repetitions, add
[django.contrib.sites.middleware.CurrentSiteMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.contrib.sites.middleware.CurrentSiteMiddleware) to
[MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE). The middleware sets the `site` attribute on every
request object, so you can use `request.site` to get the current site.

## How Django uses the sites framework¶

Although it’s not required that you use the sites framework, it’s strongly
encouraged, because Django takes advantage of it in a few places. Even if your
Django installation is powering only a single site, you should take the two
seconds to create the site object with your `domain` and `name`, and point
to its ID in your [SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) setting.

Here’s how Django uses the sites framework:

- In the [redirectsframework](https://docs.djangoproject.com/en/5.0/ref/redirects/#module-django.contrib.redirects), each
  redirect object is associated with a particular site. When Django searches
  for a redirect, it takes into account the current site.
- In the [flatpagesframework](https://docs.djangoproject.com/en/5.0/ref/flatpages/#module-django.contrib.flatpages), each
  flatpage is associated with a particular site. When a flatpage is created,
  you specify its [Site](#django.contrib.sites.models.Site), and the
  [FlatpageFallbackMiddleware](https://docs.djangoproject.com/en/5.0/ref/flatpages/#django.contrib.flatpages.middleware.FlatpageFallbackMiddleware)
  checks the current site in retrieving flatpages to display.
- In the [syndicationframework](https://docs.djangoproject.com/en/5.0/ref/syndication/#module-django.contrib.syndication), the
  templates for `title` and `description` automatically have access to a
  variable `{{ site }}`, which is the
  [Site](#django.contrib.sites.models.Site) object representing the current
  site. Also, the hook for providing item URLs will use the `domain` from
  the current [Site](#django.contrib.sites.models.Site) object if you don’t
  specify a fully-qualified domain.
- In the [authenticationframework](https://docs.djangoproject.com/en/topics/auth/#module-django.contrib.auth),
  [django.contrib.auth.views.LoginView](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.views.LoginView) passes the current
  [Site](#django.contrib.sites.models.Site) name to the template as
  `{{ site_name }}`.
- The shortcut view (`django.contrib.contenttypes.views.shortcut`)
  uses the domain of the current
  [Site](#django.contrib.sites.models.Site) object when calculating
  an object’s URL.
- In the admin framework, the “view on site” link uses the current
  [Site](#django.contrib.sites.models.Site) to work out the domain for the
  site that it will redirect to.

## RequestSiteobjects¶

Some [django.contrib](https://docs.djangoproject.com/en/5.0/ref/) applications take advantage of
the sites framework but are architected in a way that doesn’t *require* the
sites framework to be installed in your database. (Some people don’t want to,
or just aren’t *able* to install the extra database table that the sites
framework requires.) For those cases, the framework provides a
[django.contrib.sites.requests.RequestSite](#django.contrib.sites.requests.RequestSite) class, which can be used as
a fallback when the database-backed sites framework is not available.

   *class*requests.RequestSite[¶](#django.contrib.sites.requests.RequestSite)

A class that shares the primary interface of
[Site](#django.contrib.sites.models.Site) (i.e., it has
`domain` and `name` attributes) but gets its data from a Django
[HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) object rather than from a database.

   __init__(*request*)[¶](#django.contrib.sites.requests.RequestSite.__init__)

Sets the `name` and `domain` attributes to the value of
[get_host()](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest.get_host).

A [RequestSite](#django.contrib.sites.requests.RequestSite) object has a similar
interface to a normal [Site](#django.contrib.sites.models.Site) object,
except its [__init__()](#django.contrib.sites.requests.RequestSite.__init__)
method takes an [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) object. It’s able to deduce
the `domain` and `name` by looking at the request’s domain. It has
`save()` and `delete()` methods to match the interface of
[Site](#django.contrib.sites.models.Site), but the methods raise
[NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError).

## get_current_siteshortcut¶

Finally, to avoid repetitive fallback code, the framework provides a
[django.contrib.sites.shortcuts.get_current_site()](#django.contrib.sites.shortcuts.get_current_site) function.

   shortcuts.get_current_site(*request*)[¶](#django.contrib.sites.shortcuts.get_current_site)

A function that checks if `django.contrib.sites` is installed and
returns either the current [Site](#django.contrib.sites.models.Site)
object or a [RequestSite](#django.contrib.sites.requests.RequestSite) object
based on the request. It looks up the current site based on
[request.get_host()](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest.get_host) if the
[SITE_ID](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SITE_ID) setting is not defined.

Both a domain and a port may be returned by [request.get_host()](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest.get_host) when the Host header has a port
explicitly specified, e.g. `example.com:80`. In such cases, if the
lookup fails because the host does not match a record in the database,
the port is stripped and the lookup is retried with the domain part
only. This does not apply to
[RequestSite](#django.contrib.sites.requests.RequestSite) which will always
use the unmodified host.
