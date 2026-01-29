# Thestaticfilesapp¶ and more

# Thestaticfilesapp¶

# Thestaticfilesapp¶

`django.contrib.staticfiles` collects static files from each of your
applications (and any other places you specify) into a single location that
can easily be served in production.

See also

For an introduction to the static files app and some usage examples, see
[How to manage static files (e.g. images, JavaScript, CSS)](https://docs.djangoproject.com/en/howto/static-files/). For guidelines on deploying static files,
see [How to deploy static files](https://docs.djangoproject.com/en/howto/static-files/deployment/).

## Settings¶

See [staticfiles settings](https://docs.djangoproject.com/en/5.0/settings/#settings-staticfiles) for details on the
following settings:

- [STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES)
- [STATIC_ROOT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_ROOT)
- [STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL)
- [STATICFILES_DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATICFILES_DIRS)
- [STATICFILES_STORAGE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATICFILES_STORAGE)
- [STATICFILES_FINDERS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATICFILES_FINDERS)

## Management Commands¶

`django.contrib.staticfiles` exposes three management commands.

### collectstatic¶

   django-admin collectstatic[¶](#django-admin-collectstatic)

Collects the static files into [STATIC_ROOT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_ROOT).

Duplicate file names are by default resolved in a similar way to how template
resolution works: the file that is first found in one of the specified
locations will be used. If you’re confused, the [findstatic](#django-admin-findstatic) command
can help show you which files are found.

On subsequent `collectstatic` runs (if `STATIC_ROOT` isn’t empty), files
are copied only if they have a modified timestamp greater than the timestamp of
the file in `STATIC_ROOT`. Therefore if you remove an application from
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS), it’s a good idea to use the [collectstatic--clear](#cmdoption-collectstatic-clear) option in order to remove stale static files.

Files are searched by using the [enabledfinders](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATICFILES_FINDERS). The default is to look in all locations defined in
[STATICFILES_DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATICFILES_DIRS) and in the `'static'` directory of apps
specified by the [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting.

The [collectstatic](#django-admin-collectstatic) management command calls the
[post_process()](#django.contrib.staticfiles.storage.StaticFilesStorage.post_process)
method of the `staticfiles` storage backend from [STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES) after
each run and passes a list of paths that have been found by the management
command. It also receives all command line options of [collectstatic](#django-admin-collectstatic).
This is used by the
[ManifestStaticFilesStorage](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage) by
default.

By default, collected files receive permissions from
[FILE_UPLOAD_PERMISSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-FILE_UPLOAD_PERMISSIONS) and collected directories receive permissions
from [FILE_UPLOAD_DIRECTORY_PERMISSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-FILE_UPLOAD_DIRECTORY_PERMISSIONS). If you would like different
permissions for these files and/or directories, you can subclass either of the
[static files storage classes](#staticfiles-storages) and specify the
`file_permissions_mode` and/or `directory_permissions_mode` parameters,
respectively. For example:

```
from django.contrib.staticfiles import storage

class MyStaticFilesStorage(storage.StaticFilesStorage):
    def __init__(self, *args, **kwargs):
        kwargs["file_permissions_mode"] = 0o640
        kwargs["directory_permissions_mode"] = 0o760
        super().__init__(*args, **kwargs)
```

Then set the `staticfiles` storage backend in [STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES) setting to
`'path.to.MyStaticFilesStorage'`.

Some commonly used options are:

   --noinput, --no-input[¶](#cmdoption-collectstatic-noinput)

Do NOT prompt the user for input of any kind.

    --ignore PATTERN, -i PATTERN[¶](#cmdoption-collectstatic-ignore)

Ignore files, directories, or paths matching this glob-style pattern. Use
multiple times to ignore more. When specifying a path, always use forward
slashes, even on Windows.

    --dry-run, -n[¶](#cmdoption-collectstatic-dry-run)

Do everything except modify the filesystem.

    --clear, -c[¶](#cmdoption-collectstatic-clear)

Clear the existing files before trying to copy or link the original file.

    --link, -l[¶](#cmdoption-collectstatic-link)

Create a symbolic link to each file instead of copying.

    --no-post-process[¶](#cmdoption-collectstatic-no-post-process)

Don’t call the
[post_process()](#django.contrib.staticfiles.storage.StaticFilesStorage.post_process)
method of the configured `staticfiles` storage backend from
[STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES).

    --no-default-ignore[¶](#cmdoption-collectstatic-no-default-ignore)

Don’t ignore the common private glob-style patterns `'CVS'`, `'.*'`
and `'*~'`.

For a full list of options, refer to the commands own help by running:

   /  

```
$ python manage.py collectstatic --help
```

```
...\> py manage.py collectstatic --help
```

#### Customizing the ignored pattern list¶

The default ignored pattern list, `['CVS', '.*', '*~']`, can be customized in
a more persistent way than providing the `--ignore` command option at each
`collectstatic` invocation. Provide a custom [AppConfig](https://docs.djangoproject.com/en/5.0/applications/#django.apps.AppConfig)
class, override the `ignore_patterns` attribute of this class and replace
`'django.contrib.staticfiles'` with that class path in your
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting:

```
from django.contrib.staticfiles.apps import StaticFilesConfig

class MyStaticFilesConfig(StaticFilesConfig):
    ignore_patterns = [...]  # your custom ignore list
```

### findstatic¶

   django-admin findstatic staticfile [staticfile ...][¶](#django-admin-findstatic)

Searches for one or more relative paths with the enabled finders.

For example:

   /  

```
$ python manage.py findstatic css/base.css admin/js/core.js
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
  /home/polls.com/core/static/css/base.css
Found 'admin/js/core.js' here:
  /home/polls.com/src/django/contrib/admin/media/js/core.js
```

```
...\> py manage.py findstatic css\base.css admin\js\core.js
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
  /home/polls.com/core/static/css/base.css
Found 'admin/js/core.js' here:
  /home/polls.com/src/django/contrib/admin/media/js/core.js
```

     findstatic --first[¶](#cmdoption-findstatic-arg-findstatic)

By default, all matching locations are found. To only return the first match
for each relative path, use the `--first` option:

   /  

```
$ python manage.py findstatic css/base.css --first
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
```

```
...\> py manage.py findstatic css\base.css --first
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
```

This is a debugging aid; it’ll show you exactly which static file will be
collected for a given path.

By setting the `--verbosity` flag to 0, you can suppress the extra output and
just get the path names:

   /  

```
$ python manage.py findstatic css/base.css --verbosity 0
/home/special.polls.com/core/static/css/base.css
/home/polls.com/core/static/css/base.css
```

```
...\> py manage.py findstatic css\base.css --verbosity 0
/home/special.polls.com/core/static/css/base.css
/home/polls.com/core/static/css/base.css
```

On the other hand, by setting the `--verbosity` flag to 2, you can get all
the directories which were searched:

   /  

```
$ python manage.py findstatic css/base.css --verbosity 2
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
  /home/polls.com/core/static/css/base.css
Looking in the following locations:
  /home/special.polls.com/core/static
  /home/polls.com/core/static
  /some/other/path/static
```

```
...\> py manage.py findstatic css\base.css --verbosity 2
Found 'css/base.css' here:
  /home/special.polls.com/core/static/css/base.css
  /home/polls.com/core/static/css/base.css
Looking in the following locations:
  /home/special.polls.com/core/static
  /home/polls.com/core/static
  /some/other/path/static
```

### runserver¶

   django-admin runserver [addrport]

Overrides the core [runserver](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-runserver) command if the `staticfiles` app
is [installed](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) and adds automatic serving of static
files. File serving doesn’t run through [MIDDLEWARE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MIDDLEWARE).

The command adds these options:

   --nostatic[¶](#cmdoption-runserver-nostatic)

Use the `--nostatic` option to disable serving of static files with the
[staticfiles](#) app entirely. This option is
only available if the [staticfiles](#) app is
in your project’s [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting.

Example usage:

   /  

```
$ django-admin runserver --nostatic
```

```
...\> django-admin runserver --nostatic
```

     --insecure[¶](#cmdoption-runserver-insecure)

Use the `--insecure` option to force serving of static files with the
[staticfiles](#) app even if the [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG)
setting is `False`. By using this you acknowledge the fact that it’s
**grossly inefficient** and probably **insecure**. This is only intended for
local development, should **never be used in production** and is only
available if the [staticfiles](#) app is
in your project’s [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting.

`--insecure` doesn’t work with [ManifestStaticFilesStorage](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage).

Example usage:

   /  

```
$ django-admin runserver --insecure
```

```
...\> django-admin runserver --insecure
```

## Storages¶

### StaticFilesStorage¶

   *class*storage.StaticFilesStorage[¶](#django.contrib.staticfiles.storage.StaticFilesStorage)

A subclass of the [FileSystemStorage](https://docs.djangoproject.com/en/5.0/files/storage/#django.core.files.storage.FileSystemStorage)
storage backend that uses the [STATIC_ROOT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_ROOT) setting as the base
file system location and the [STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL) setting respectively
as the base URL.

   storage.StaticFilesStorage.post_process(*paths*, ***options*)[¶](#django.contrib.staticfiles.storage.StaticFilesStorage.post_process)

If this method is defined on a storage, it’s called by the
[collectstatic](#django-admin-collectstatic) management command after each run and gets passed the
local storages and paths of found files as a dictionary, as well as the command
line options. It yields tuples of three values:
`original_path, processed_path, processed`. The path values are strings and
`processed` is a boolean indicating whether or not the value was
post-processed, or an exception if post-processing failed.

The [ManifestStaticFilesStorage](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage)
uses this behind the scenes to replace the paths with their hashed
counterparts and update the cache appropriately.

### ManifestStaticFilesStorage¶

   *class*storage.ManifestStaticFilesStorage[¶](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage)

A subclass of the [StaticFilesStorage](#django.contrib.staticfiles.storage.StaticFilesStorage)
storage backend which stores the file names it handles by appending the MD5
hash of the file’s content to the filename. For example, the file
`css/styles.css` would also be saved as `css/styles.55e7cbb9ba48.css`.

The purpose of this storage is to keep serving the old files in case some
pages still refer to those files, e.g. because they are cached by you or
a 3rd party proxy server. Additionally, it’s very helpful if you want to
apply [far future Expires headers](https://developer.yahoo.com/performance/rules.html#expires) to the deployed files to speed up the
load time for subsequent page visits.

The storage backend automatically replaces the paths found in the saved
files matching other saved files with the path of the cached copy (using
the [post_process()](#django.contrib.staticfiles.storage.StaticFilesStorage.post_process)
method). The regular expressions used to find those paths
(`django.contrib.staticfiles.storage.HashedFilesMixin.patterns`) cover:

- The [@import](https://www.w3.org/TR/CSS2/cascade.html#at-import) rule and [url()](https://www.w3.org/TR/CSS2/syndata.html#uri) statement of [Cascading Style Sheets](https://www.w3.org/Style/CSS/).
- [Source map](https://firefox-source-docs.mozilla.org/devtools-user/debugger/how_to/use_a_source_map/) comments in CSS and JavaScript files.

Subclass `ManifestStaticFilesStorage` and set the
`support_js_module_import_aggregation` attribute to `True`, if you want to
use the experimental regular expressions to cover:

- The [modules import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#importing_features_into_your_script) in JavaScript.
- The [modules aggregation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#aggregating_modules) in JavaScript.

For example, the `'css/styles.css'` file with this content:

```
@import url("../admin/css/base.css");
```

…would be replaced by calling the
[url()](https://docs.djangoproject.com/en/5.0/files/storage/#django.core.files.storage.Storage.url) method of the
`ManifestStaticFilesStorage` storage backend, ultimately saving a
`'css/styles.55e7cbb9ba48.css'` file with the following content:

```
@import url("../admin/css/base.27e20196a850.css");
```

Usage of the `integrity` HTML attribute with local files

When using the optional `integrity` attribute within tags like
`<script>` or `<link>`, its value should be calculated based on the
files as they are served, not as stored in the filesystem. This is
particularly important because depending on how static files are collected,
their checksum may have changed (for example when using
[collectstatic](#django-admin-collectstatic)). At the moment, there is no out-of-the-box
tooling available for this.

You can change the location of the manifest file by using a custom
`ManifestStaticFilesStorage` subclass that sets the `manifest_storage`
argument. For example:

```
from django.conf import settings
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage,
    StaticFilesStorage,
)

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    def __init__(self, *args, **kwargs):
        manifest_storage = StaticFilesStorage(location=settings.BASE_DIR)
        super().__init__(*args, manifest_storage=manifest_storage, **kwargs)
```

References in comments

`ManifestStaticFilesStorage` doesn’t ignore paths in statements that are
commented out. This [may crash on the nonexistent paths](https://code.djangoproject.com/ticket/21080).
You should check and eventually strip comments.

   Changed in Django 4.2:

Experimental optional support for finding paths to JavaScript modules in
`import` and `export` statements was added.

    storage.ManifestStaticFilesStorage.manifest_hash[¶](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage.manifest_hash)   New in Django 4.2.

This attribute provides a single hash that changes whenever a file in the
manifest changes. This can be useful to communicate to SPAs that the assets on
the server have changed (due to a new deployment).

   storage.ManifestStaticFilesStorage.max_post_process_passes[¶](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage.max_post_process_passes)

Since static files might reference other static files that need to have their
paths replaced, multiple passes of replacing paths may be needed until the file
hashes converge. To prevent an infinite loop due to hashes not converging (for
example, if `'foo.css'` references `'bar.css'` which references
`'foo.css'`) there is a maximum number of passes before post-processing is
abandoned. In cases with a large number of references, a higher number of
passes might be needed. Increase the maximum number of passes by subclassing
`ManifestStaticFilesStorage` and setting the `max_post_process_passes`
attribute. It defaults to 5.

To enable the `ManifestStaticFilesStorage` you have to make sure the
following requirements are met:

- the `staticfiles` storage backend in [STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES) setting is set to
  `'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'`
- the [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) setting is set to `False`
- you’ve collected all your static files by using the
  [collectstatic](#django-admin-collectstatic) management command

Since creating the MD5 hash can be a performance burden to your website
during runtime, `staticfiles` will automatically store the mapping with
hashed names for all processed files in a file called `staticfiles.json`.
This happens once when you run the [collectstatic](#django-admin-collectstatic) management
command.

   storage.ManifestStaticFilesStorage.manifest_strict[¶](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage.manifest_strict)

If a file isn’t found in the `staticfiles.json` manifest at runtime, a
`ValueError` is raised. This behavior can be disabled by subclassing
`ManifestStaticFilesStorage` and setting the `manifest_strict` attribute to
`False` – nonexistent paths will remain unchanged.

Due to the requirement of running [collectstatic](#django-admin-collectstatic), this storage
typically shouldn’t be used when running tests as `collectstatic` isn’t run
as part of the normal test setup. During testing, ensure that `staticfiles`
storage backend in the [STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES) setting is set to something else
like `'django.contrib.staticfiles.storage.StaticFilesStorage'` (the default).

   storage.ManifestStaticFilesStorage.file_hash(*name*, *content=None*)[¶](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage.file_hash)

The method that is used when creating the hashed name of a file.
Needs to return a hash for the given file name and content.
By default it calculates a MD5 hash from the content’s chunks as
mentioned above. Feel free to override this method to use your own
hashing algorithm.

### ManifestFilesMixin¶

   *class*storage.ManifestFilesMixin[¶](#django.contrib.staticfiles.storage.ManifestFilesMixin)

Use this mixin with a custom storage to append the MD5 hash of the file’s
content to the filename as [ManifestStaticFilesStorage](#django.contrib.staticfiles.storage.ManifestStaticFilesStorage) does.

## Finders Module¶

`staticfiles` finders has a `searched_locations` attribute which is a list
of directory paths in which the finders searched. Example usage:

```
from django.contrib.staticfiles import finders

result = finders.find("css/base.css")
searched_locations = finders.searched_locations
```

## Other Helpers¶

There are a few other helpers outside of the
[staticfiles](#module-django.contrib.staticfiles) app to work with static
files:

- The [django.template.context_processors.static()](https://docs.djangoproject.com/en/5.0/templates/api/#django.template.context_processors.static) context processor
  which adds [STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL) to every template context rendered
  with [RequestContext](https://docs.djangoproject.com/en/5.0/templates/api/#django.template.RequestContext) contexts.
- The builtin template tag [static](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatetag-static) which takes a path and urljoins it
  with the static prefix [STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL). If
  `django.contrib.staticfiles` is installed, the tag uses the `url()`
  method of the `staticfiles` storage backend from [STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES)
  instead.
- The builtin template tag [get_static_prefix](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatetag-get_static_prefix) which populates a
  template variable with the static prefix [STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL) to be
  used as a variable or directly.
- The similar template tag [get_media_prefix](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatetag-get_media_prefix) which works like
  [get_static_prefix](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatetag-get_static_prefix) but uses [MEDIA_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_URL).
- The `staticfiles` key in [django.core.files.storage.storages](https://docs.djangoproject.com/en/5.0/files/storage/#django.core.files.storage.storages)
  contains a ready-to-use instance of the staticfiles storage backend.

### Static file development view¶

The static files tools are mostly designed to help with getting static files
successfully deployed into production. This usually means a separate,
dedicated static file server, which is a lot of overhead to mess with when
developing locally. Thus, the `staticfiles` app ships with a
**quick and dirty helper view** that you can use to serve files locally in
development.

   views.serve(*request*, *path*)[¶](#django.contrib.staticfiles.views.serve)

This view function serves static files in development.

Warning

This view will only work if [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) is `True`.

That’s because this view is **grossly inefficient** and probably
**insecure**. This is only intended for local development, and should
**never be used in production**.

Note

To guess the served files’ content types, this view relies on the
[mimetypes](https://docs.python.org/3/library/mimetypes.html#module-mimetypes) module from the Python standard library, which itself
relies on the underlying platform’s map files. If you find that this view
doesn’t return proper content types for certain files, it is most likely
that the platform’s map files are incorrect or need to be updated. This can
be achieved, for example, by installing or updating the `mailcap` package
on a Red Hat distribution, `mime-support` on a Debian distribution, or by
editing the keys under `HKEY_CLASSES_ROOT` in the Windows registry.

This view is automatically enabled by [runserver](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-runserver) (with a
[DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) setting set to `True`). To use the view with a different
local development server, add the following snippet to the end of your
primary URL configuration:

```
from django.conf import settings
from django.contrib.staticfiles import views
from django.urls import re_path

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", views.serve),
    ]
```

Note, the beginning of the pattern (`r'^static/'`) should be your
[STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL) setting.

Since this is a bit finicky, there’s also a helper function that’ll do this for
you:

   urls.staticfiles_urlpatterns()[¶](#django.contrib.staticfiles.urls.staticfiles_urlpatterns)

This will return the proper URL pattern for serving static files to your
already defined pattern list. Use it like this:

```
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# ... the rest of your URLconf here ...

urlpatterns += staticfiles_urlpatterns()
```

This will inspect your [STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL) setting and wire up the view
to serve static files accordingly. Don’t forget to set the
[STATICFILES_DIRS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATICFILES_DIRS) setting appropriately to let
`django.contrib.staticfiles` know where to look for files in addition to
files in app directories.

Warning

This helper function will only work if [DEBUG](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEBUG) is `True`
and your [STATIC_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STATIC_URL) setting is neither empty nor a full
URL such as `http://static.example.com/`.

That’s because this view is **grossly inefficient** and probably
**insecure**. This is only intended for local development, and should
**never be used in production**.

### Specialized test case to support ‘live testing’¶

   *class*testing.StaticLiveServerTestCase[¶](#django.contrib.staticfiles.testing.StaticLiveServerTestCase)

This unittest TestCase subclass extends [django.test.LiveServerTestCase](https://docs.djangoproject.com/en/topics/testing/tools/#django.test.LiveServerTestCase).

Just like its parent, you can use it to write tests that involve running the
code under test and consuming it with testing tools through HTTP (e.g. Selenium,
PhantomJS, etc.), because of which it’s needed that the static assets are also
published.

But given the fact that it makes use of the
[django.contrib.staticfiles.views.serve()](#django.contrib.staticfiles.views.serve) view described above, it can
transparently overlay at test execution-time the assets provided by the
`staticfiles` finders. This means you don’t need to run
[collectstatic](#django-admin-collectstatic) before or as a part of your tests setup.

---

# contribpackages¶

# contribpackages¶

Django aims to follow Python’s [“batteries included” philosophy](https://docs.python.org/3/tutorial/stdlib.html#tut-batteries-included). It ships with a variety of extra, optional tools
that solve common web development problems.

This code lives in [django/contrib](https://github.com/django/django/blob/main/django/contrib) in the Django distribution. This document
gives a rundown of the packages in `contrib`, along with any dependencies
those packages have.

Including `contrib` packages in `INSTALLED_APPS`

For most of these add-ons – specifically, the add-ons that include either
models or template tags – you’ll need to add the package name (e.g.,
`'django.contrib.redirects'`) to your [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting
and rerun `manage.py migrate`.

## admin¶

The automatic Django administrative interface. For more information, see
[Tutorial 2](https://docs.djangoproject.com/en/intro/tutorial02/) and the
[admin documentation](https://docs.djangoproject.com/en/5.0/ref/admin/).

Requires the [auth](#auth) and [contenttypes](#contenttypes) contrib packages to be installed.

## auth¶

Django’s authentication framework.

See [User authentication in Django](https://docs.djangoproject.com/en/topics/auth/).

## contenttypes¶

A light framework for hooking into “types” of content, where each installed
Django model is a separate content type.

See the [contenttypes documentation](https://docs.djangoproject.com/en/5.0/ref/contenttypes/).

## flatpages¶

A framework for managing “flat” HTML content in a database.

See the [flatpages documentation](https://docs.djangoproject.com/en/5.0/ref/flatpages/).

Requires the [sites](#sites) contrib package to be installed as well.

## gis¶

A world-class geospatial framework built on top of Django, that enables
storage, manipulation and display of spatial data.

See the [GeoDjango](https://docs.djangoproject.com/en/5.0/ref/gis/) documentation for more.

## humanize¶

A set of Django template filters useful for adding a “human touch” to data.

See the [humanize documentation](https://docs.djangoproject.com/en/5.0/ref/humanize/).

## messages¶

A framework for storing and retrieving temporary cookie- or session-based
messages

See the [messages documentation](https://docs.djangoproject.com/en/5.0/ref/messages/).

## postgres¶

A collection of PostgreSQL specific features.

See the [contrib.postgres documentation](https://docs.djangoproject.com/en/5.0/ref/postgres/).

## redirects¶

A framework for managing redirects.

See the [redirects documentation](https://docs.djangoproject.com/en/5.0/ref/redirects/).

## sessions¶

A framework for storing data in anonymous sessions.

See the [sessions documentation](https://docs.djangoproject.com/en/topics/http/sessions/).

## sites¶

A light framework that lets you operate multiple websites off of the same
database and Django installation. It gives you hooks for associating objects to
one or more sites.

See the [sites documentation](https://docs.djangoproject.com/en/5.0/ref/sites/).

## sitemaps¶

A framework for generating Google sitemap XML files.

See the [sitemaps documentation](https://docs.djangoproject.com/en/5.0/ref/sitemaps/).

## syndication¶

A framework for generating syndication feeds, in RSS and Atom, quite easily.

See the [syndication documentation](https://docs.djangoproject.com/en/5.0/ref/syndication/).

## Other add-ons¶

If you have an idea for functionality to include in `contrib`, let us know!
Code it up, and post it to the [django-users](https://docs.djangoproject.com/en/internals/mailing-lists/#django-users-mailing-list) mailing list.

---

# Cross Site Request Forgery protection¶

# Cross Site Request Forgery protection¶

The CSRF middleware and template tag provides easy-to-use protection against
[Cross Site Request Forgeries](https://owasp.org/www-community/attacks/csrf#overview). This type of attack occurs when a malicious
website contains a link, a form button or some JavaScript that is intended to
perform some action on your website, using the credentials of a logged-in user
who visits the malicious site in their browser. A related type of attack,
‘login CSRF’, where an attacking site tricks a user’s browser into logging into
a site with someone else’s credentials, is also covered.

The first defense against CSRF attacks is to ensure that GET requests (and other
‘safe’ methods, as defined by [RFC 9110 Section 9.2.1](https://datatracker.ietf.org/doc/html/rfc9110.html#section-9.2.1)) are side effect free.
Requests via ‘unsafe’ methods, such as POST, PUT, and DELETE, can then be
protected by the steps outlined in [How to use Django’s CSRF protection](https://docs.djangoproject.com/en/howto/csrf/#using-csrf).

## How it works¶

The CSRF protection is based on the following things:

1. A CSRF cookie that is a random secret value, which other sites will not have
  access to.
  `CsrfViewMiddleware` sends this cookie with the response whenever
  `django.middleware.csrf.get_token()` is called. It can also send it in
  other cases. For security reasons, the value of the secret is changed each
  time a user logs in.
2. A hidden form field with the name ‘csrfmiddlewaretoken’, present in all
  outgoing POST forms.
  In order to protect against [BREACH](https://www.breachattack.com/) attacks, the value of this field is
  not simply the secret. It is scrambled differently with each response using
  a mask. The mask is generated randomly on every call to `get_token()`, so
  the form field value is different each time.
  This part is done by the template tag.
3. For all incoming requests that are not using HTTP GET, HEAD, OPTIONS or
  TRACE, a CSRF cookie must be present, and the ‘csrfmiddlewaretoken’ field
  must be present and correct. If it isn’t, the user will get a 403 error.
  When validating the ‘csrfmiddlewaretoken’ field value, only the secret,
  not the full token, is compared with the secret in the cookie value.
  This allows the use of ever-changing tokens. While each request may use its
  own token, the secret remains common to all.
  This check is done by `CsrfViewMiddleware`.
4. `CsrfViewMiddleware` verifies the [Origin header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin), if provided by the
  browser, against the current host and the [CSRF_TRUSTED_ORIGINS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_TRUSTED_ORIGINS)
  setting. This provides protection against cross-subdomain attacks.
5. In addition, for HTTPS requests, if the `Origin` header isn’t provided,
  `CsrfViewMiddleware` performs strict referer checking. This means that
  even if a subdomain can set or modify cookies on your domain, it can’t force
  a user to post to your application since that request won’t come from your
  own exact domain.
  This also addresses a man-in-the-middle attack that’s possible under HTTPS
  when using a session independent secret, due to the fact that HTTP
  `Set-Cookie` headers are (unfortunately) accepted by clients even when
  they are talking to a site under HTTPS. (Referer checking is not done for
  HTTP requests because the presence of the `Referer` header isn’t reliable
  enough under HTTP.)
  If the [CSRF_COOKIE_DOMAIN](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_DOMAIN) setting is set, the referer is compared
  against it. You can allow cross-subdomain requests by including a leading
  dot. For example, `CSRF_COOKIE_DOMAIN = '.example.com'` will allow POST
  requests from `www.example.com` and `api.example.com`. If the setting is
  not set, then the referer must match the HTTP `Host` header.
  Expanding the accepted referers beyond the current host or cookie domain can
  be done with the [CSRF_TRUSTED_ORIGINS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_TRUSTED_ORIGINS) setting.

This ensures that only forms that have originated from trusted domains can be
used to POST data back.

It deliberately ignores GET requests (and other requests that are defined as
‘safe’ by [RFC 9110 Section 9.2.1](https://datatracker.ietf.org/doc/html/rfc9110.html#section-9.2.1)). These requests ought never to have any
potentially dangerous side effects, and so a CSRF attack with a GET request
ought to be harmless. [RFC 9110 Section 9.2.1](https://datatracker.ietf.org/doc/html/rfc9110.html#section-9.2.1) defines POST, PUT, and DELETE
as ‘unsafe’, and all other methods are also assumed to be unsafe, for maximum
protection.

The CSRF protection cannot protect against man-in-the-middle attacks, so use
[HTTPS](https://docs.djangoproject.com/en/topics/security/#security-recommendation-ssl) with
[HTTP Strict Transport Security](https://docs.djangoproject.com/en/5.0/middleware/#http-strict-transport-security). It also assumes [validation of
the HOST header](https://docs.djangoproject.com/en/topics/security/#host-headers-virtual-hosting) and that there aren’t any
[cross-site scripting vulnerabilities](https://docs.djangoproject.com/en/topics/security/#cross-site-scripting) on your site
(because XSS vulnerabilities already let an attacker do anything a CSRF
vulnerability allows and much worse).

Removing the `Referer` header

To avoid disclosing the referrer URL to third-party sites, you might want
to [disable the referer](https://www.w3.org/TR/referrer-policy/#referrer-policy-delivery) on your site’s `<a>` tags. For example, you
might use the `<meta name="referrer" content="no-referrer">` tag or
include the `Referrer-Policy: no-referrer` header. Due to the CSRF
protection’s strict referer checking on HTTPS requests, those techniques
cause a CSRF failure on requests with ‘unsafe’ methods. Instead, use
alternatives like `<a rel="noreferrer" ...>"` for links to third-party
sites.

## Limitations¶

Subdomains within a site will be able to set cookies on the client for the whole
domain. By setting the cookie and using a corresponding token, subdomains will
be able to circumvent the CSRF protection. The only way to avoid this is to
ensure that subdomains are controlled by trusted users (or, are at least unable
to set cookies). Note that even without CSRF, there are other vulnerabilities,
such as session fixation, that make giving subdomains to untrusted parties a bad
idea, and these vulnerabilities cannot easily be fixed with current browsers.

## Utilities¶

The examples below assume you are using function-based views. If you
are working with class-based views, you can refer to [Decorating
class-based views](https://docs.djangoproject.com/en/topics/class-based-views/intro/#id1).

   csrf_exempt(*view*)[[source]](https://docs.djangoproject.com/en/_modules/django/views/decorators/csrf/#csrf_exempt)[¶](#django.views.decorators.csrf.csrf_exempt)

This decorator marks a view as being exempt from the protection ensured by
the middleware. Example:

```
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_view(request):
    return HttpResponse("Hello world")
```

   Changed in Django 5.0:

Support for wrapping asynchronous view functions was added.

     csrf_protect(*view*)[¶](#django.views.decorators.csrf.csrf_protect)

Decorator that provides the protection of `CsrfViewMiddleware` to a view.

Usage:

```
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def my_view(request):
    c = {}
    # ...
    return render(request, "a_template.html", c)
```

   Changed in Django 5.0:

Support for wrapping asynchronous view functions was added.

     requires_csrf_token(*view*)[¶](#django.views.decorators.csrf.requires_csrf_token)

Normally the [csrf_token](https://docs.djangoproject.com/en/5.0/templates/builtins/#std-templatetag-csrf_token) template tag will not work if
`CsrfViewMiddleware.process_view` or an equivalent like `csrf_protect`
has not run. The view decorator `requires_csrf_token` can be used to
ensure the template tag does work. This decorator works similarly to
`csrf_protect`, but never rejects an incoming request.

Example:

```
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def my_view(request):
    c = {}
    # ...
    return render(request, "a_template.html", c)
```

   Changed in Django 5.0:

Support for wrapping asynchronous view functions was added.

     ensure_csrf_cookie(*view*)[¶](#django.views.decorators.csrf.ensure_csrf_cookie)

This decorator forces a view to send the CSRF cookie.

  Changed in Django 5.0:

Support for wrapping asynchronous view functions was added.

## Settings¶

A number of settings can be used to control Django’s CSRF behavior:

- [CSRF_COOKIE_AGE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_AGE)
- [CSRF_COOKIE_DOMAIN](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_DOMAIN)
- [CSRF_COOKIE_HTTPONLY](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_HTTPONLY)
- [CSRF_COOKIE_NAME](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_NAME)
- [CSRF_COOKIE_PATH](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_PATH)
- [CSRF_COOKIE_SAMESITE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_SAMESITE)
- [CSRF_COOKIE_SECURE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_COOKIE_SECURE)
- [CSRF_FAILURE_VIEW](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_FAILURE_VIEW)
- [CSRF_HEADER_NAME](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_HEADER_NAME)
- [CSRF_TRUSTED_ORIGINS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_TRUSTED_ORIGINS)
- [CSRF_USE_SESSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_USE_SESSIONS)

## Frequently Asked Questions¶

### Is posting an arbitrary CSRF token pair (cookie and POST data) a vulnerability?¶

No, this is by design. Without a man-in-the-middle attack, there is no way for
an attacker to send a CSRF token cookie to a victim’s browser, so a successful
attack would need to obtain the victim’s browser’s cookie via XSS or similar,
in which case an attacker usually doesn’t need CSRF attacks.

Some security audit tools flag this as a problem but as mentioned before, an
attacker cannot steal a user’s browser’s CSRF cookie. “Stealing” or modifying
*your own* token using Firebug, Chrome dev tools, etc. isn’t a vulnerability.

### Is it a problem that Django’s CSRF protection isn’t linked to a session by default?¶

No, this is by design. Not linking CSRF protection to a session allows using
the protection on sites such as a *pastebin* that allow submissions from
anonymous users which don’t have a session.

If you wish to store the CSRF token in the user’s session, use the
[CSRF_USE_SESSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-CSRF_USE_SESSIONS) setting.

### Why might a user encounter a CSRF validation failure after logging in?¶

For security reasons, CSRF tokens are rotated each time a user logs in. Any
page with a form generated before a login will have an old, invalid CSRF token
and need to be reloaded. This might happen if a user uses the back button after
a login or if they log in a different browser tab.
