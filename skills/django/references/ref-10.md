# Django Exceptions¶ and more

# Django Exceptions¶

# Django Exceptions¶

Django raises some of its own exceptions as well as standard Python exceptions.

## Django Core Exceptions¶

Django core exception classes are defined in `django.core.exceptions`.

### AppRegistryNotReady¶

   *exception*AppRegistryNotReady[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#AppRegistryNotReady)[¶](#django.core.exceptions.AppRegistryNotReady)

This exception is raised when attempting to use models before the [app
loading process](https://docs.djangoproject.com/en/5.0/applications/#app-loading-process), which initializes the ORM, is
complete.

### ObjectDoesNotExist¶

   *exception*ObjectDoesNotExist[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#ObjectDoesNotExist)[¶](#django.core.exceptions.ObjectDoesNotExist)

The base class for [Model.DoesNotExist](https://docs.djangoproject.com/en/5.0/models/class/#django.db.models.Model.DoesNotExist) exceptions. A `try/except` for
`ObjectDoesNotExist` will catch
[DoesNotExist](https://docs.djangoproject.com/en/5.0/models/class/#django.db.models.Model.DoesNotExist) exceptions for all models.

See [get()](https://docs.djangoproject.com/en/5.0/models/querysets/#django.db.models.query.QuerySet.get).

### EmptyResultSet¶

   *exception*EmptyResultSet[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#EmptyResultSet)[¶](#django.core.exceptions.EmptyResultSet)

`EmptyResultSet` may be raised during query generation if a query won’t
return any results. Most Django projects won’t encounter this exception,
but it might be useful for implementing custom lookups and expressions.

### FullResultSet¶

   *exception*FullResultSet[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#FullResultSet)[¶](#django.core.exceptions.FullResultSet)   New in Django 4.2:

`FullResultSet` may be raised during query generation if a query will
match everything. Most Django projects won’t encounter this exception, but
it might be useful for implementing custom lookups and expressions.

### FieldDoesNotExist¶

   *exception*FieldDoesNotExist[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#FieldDoesNotExist)[¶](#django.core.exceptions.FieldDoesNotExist)

The `FieldDoesNotExist` exception is raised by a model’s
`_meta.get_field()` method when the requested field does not exist on the
model or on the model’s parents.

### MultipleObjectsReturned¶

   *exception*MultipleObjectsReturned[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#MultipleObjectsReturned)[¶](#django.core.exceptions.MultipleObjectsReturned)

The base class for [Model.MultipleObjectsReturned](https://docs.djangoproject.com/en/5.0/models/class/#django.db.models.Model.MultipleObjectsReturned) exceptions. A
`try/except` for `MultipleObjectsReturned` will catch
[MultipleObjectsReturned](https://docs.djangoproject.com/en/5.0/models/class/#django.db.models.Model.MultipleObjectsReturned) exceptions for all
models.

See [get()](https://docs.djangoproject.com/en/5.0/models/querysets/#django.db.models.query.QuerySet.get).

### SuspiciousOperation¶

   *exception*SuspiciousOperation[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#SuspiciousOperation)[¶](#django.core.exceptions.SuspiciousOperation)

The [SuspiciousOperation](#django.core.exceptions.SuspiciousOperation) exception is raised when a user has
performed an operation that should be considered suspicious from a security
perspective, such as tampering with a session cookie. Subclasses of
`SuspiciousOperation` include:

- `DisallowedHost`
- `DisallowedModelAdminLookup`
- `DisallowedModelAdminToField`
- `DisallowedRedirect`
- `InvalidSessionKey`
- `RequestDataTooBig`
- `SuspiciousFileOperation`
- `SuspiciousMultipartForm`
- `SuspiciousSession`
- `TooManyFieldsSent`
- `TooManyFilesSent`

If a `SuspiciousOperation` exception reaches the ASGI/WSGI handler level
it is logged at the `Error` level and results in
a [HttpResponseBadRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponseBadRequest). See the [logging
documentation](https://docs.djangoproject.com/en/topics/logging/) for more information.

   Changed in Django 3.2.18:

`SuspiciousOperation` is raised when too many files are submitted.

### PermissionDenied¶

   *exception*PermissionDenied[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#PermissionDenied)[¶](#django.core.exceptions.PermissionDenied)

The [PermissionDenied](#django.core.exceptions.PermissionDenied) exception is raised when a user does not have
permission to perform the action requested.

### ViewDoesNotExist¶

   *exception*ViewDoesNotExist[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#ViewDoesNotExist)[¶](#django.core.exceptions.ViewDoesNotExist)

The [ViewDoesNotExist](#django.core.exceptions.ViewDoesNotExist) exception is raised by
[django.urls](https://docs.djangoproject.com/en/5.0/urlresolvers/#module-django.urls) when a requested view does not exist.

### MiddlewareNotUsed¶

   *exception*MiddlewareNotUsed[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#MiddlewareNotUsed)[¶](#django.core.exceptions.MiddlewareNotUsed)

The [MiddlewareNotUsed](#django.core.exceptions.MiddlewareNotUsed) exception is raised when a middleware is not
used in the server configuration.

### ImproperlyConfigured¶

   *exception*ImproperlyConfigured[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#ImproperlyConfigured)[¶](#django.core.exceptions.ImproperlyConfigured)

The [ImproperlyConfigured](#django.core.exceptions.ImproperlyConfigured) exception is raised when Django is
somehow improperly configured – for example, if a value in `settings.py`
is incorrect or unparseable.

### FieldError¶

   *exception*FieldError[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#FieldError)[¶](#django.core.exceptions.FieldError)

The [FieldError](#django.core.exceptions.FieldError) exception is raised when there is a problem with a
model field. This can happen for several reasons:

- A field in a model clashes with a field of the same name from an
  abstract base class
- An infinite loop is caused by ordering
- A keyword cannot be parsed from the filter parameters
- A field cannot be determined from a keyword in the query
  parameters
- A join is not permitted on the specified field
- A field name is invalid
- A query contains invalid order_by arguments

### ValidationError¶

   *exception*ValidationError[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#ValidationError)[¶](#django.core.exceptions.ValidationError)

The [ValidationError](#django.core.exceptions.ValidationError) exception is raised when data fails form or
model field validation. For more information about validation, see
[Form and Field Validation](https://docs.djangoproject.com/en/5.0/forms/validation/),
[Model Field Validation](https://docs.djangoproject.com/en/5.0/models/instances/#validating-objects) and the
[Validator Reference](https://docs.djangoproject.com/en/5.0/validators/).

#### NON_FIELD_ERRORS¶

   NON_FIELD_ERRORS[¶](#django.core.exceptions.NON_FIELD_ERRORS)

`ValidationError`s that don’t belong to a particular field in a form
or model are classified as `NON_FIELD_ERRORS`. This constant is used
as a key in dictionaries that otherwise map fields to their respective
list of errors.

### BadRequest¶

   *exception*BadRequest[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#BadRequest)[¶](#django.core.exceptions.BadRequest)

The [BadRequest](#django.core.exceptions.BadRequest) exception is raised when the request cannot be
processed due to a client error. If a `BadRequest` exception reaches the
ASGI/WSGI handler level it results in a
[HttpResponseBadRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpResponseBadRequest).

### RequestAborted¶

   *exception*RequestAborted[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#RequestAborted)[¶](#django.core.exceptions.RequestAborted)

The [RequestAborted](#django.core.exceptions.RequestAborted) exception is raised when an HTTP body being read
in by the handler is cut off midstream and the client connection closes,
or when the client does not send data and hits a timeout where the server
closes the connection.

It is internal to the HTTP handler modules and you are unlikely to see
it elsewhere. If you are modifying HTTP handling code, you should raise
this when you encounter an aborted request to make sure the socket is
closed cleanly.

### SynchronousOnlyOperation¶

   *exception*SynchronousOnlyOperation[[source]](https://docs.djangoproject.com/en/_modules/django/core/exceptions/#SynchronousOnlyOperation)[¶](#django.core.exceptions.SynchronousOnlyOperation)

The [SynchronousOnlyOperation](#django.core.exceptions.SynchronousOnlyOperation) exception is raised when code that
is only allowed in synchronous Python code is called from an asynchronous
context (a thread with a running asynchronous event loop). These parts of
Django are generally heavily reliant on thread-safety to function and don’t
work correctly under coroutines sharing the same thread.

If you are trying to call code that is synchronous-only from an
asynchronous thread, then create a synchronous thread and call it in that.
You can accomplish this is with [asgiref.sync.sync_to_async()](https://docs.djangoproject.com/en/topics/async/#asgiref.sync.sync_to_async).

## URL Resolver exceptions¶

URL Resolver exceptions are defined in `django.urls`.

### Resolver404¶

   *exception*Resolver404[[source]](https://docs.djangoproject.com/en/_modules/django/urls/exceptions/#Resolver404)[¶](#django.urls.Resolver404)

The [Resolver404](#django.urls.Resolver404) exception is raised by
[resolve()](https://docs.djangoproject.com/en/5.0/urlresolvers/#django.urls.resolve) if the path passed to `resolve()` doesn’t
map to a view. It’s a subclass of [django.http.Http404](https://docs.djangoproject.com/en/topics/http/views/#django.http.Http404).

### NoReverseMatch¶

   *exception*NoReverseMatch[[source]](https://docs.djangoproject.com/en/_modules/django/urls/exceptions/#NoReverseMatch)[¶](#django.urls.NoReverseMatch)

The [NoReverseMatch](#django.urls.NoReverseMatch) exception is raised by [django.urls](https://docs.djangoproject.com/en/5.0/urlresolvers/#module-django.urls) when a
matching URL in your URLconf cannot be identified based on the parameters
supplied.

## Database Exceptions¶

Database exceptions may be imported from `django.db`.

Django wraps the standard database exceptions so that your Django code has a
guaranteed common implementation of these classes.

   *exception*Error[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#Error)[¶](#django.db.Error)    *exception*InterfaceError[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#InterfaceError)[¶](#django.db.InterfaceError)    *exception*DatabaseError[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#DatabaseError)[¶](#django.db.DatabaseError)    *exception*DataError[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#DataError)[¶](#django.db.DataError)    *exception*OperationalError[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#OperationalError)[¶](#django.db.OperationalError)    *exception*IntegrityError[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#IntegrityError)[¶](#django.db.IntegrityError)    *exception*InternalError[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#InternalError)[¶](#django.db.InternalError)    *exception*ProgrammingError[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#ProgrammingError)[¶](#django.db.ProgrammingError)    *exception*NotSupportedError[[source]](https://docs.djangoproject.com/en/_modules/django/db/utils/#NotSupportedError)[¶](#django.db.NotSupportedError)

The Django wrappers for database exceptions behave exactly the same as
the underlying database exceptions. See [PEP 249](https://peps.python.org/pep-0249/), the Python Database API
Specification v2.0, for further information.

As per [PEP 3134](https://peps.python.org/pep-3134/), a `__cause__` attribute is set with the original
(underlying) database exception, allowing access to any additional
information provided.

   *exception*models.ProtectedError[¶](#django.db.models.ProtectedError)

Raised to prevent deletion of referenced objects when using
[django.db.models.PROTECT](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.PROTECT). [models.ProtectedError](#django.db.models.ProtectedError) is a subclass
of [IntegrityError](#django.db.IntegrityError).

   *exception*models.RestrictedError[¶](#django.db.models.RestrictedError)

Raised to prevent deletion of referenced objects when using
[django.db.models.RESTRICT](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.RESTRICT). [models.RestrictedError](#django.db.models.RestrictedError) is a subclass
of [IntegrityError](#django.db.IntegrityError).

## HTTP Exceptions¶

HTTP exceptions may be imported from `django.http`.

### UnreadablePostError¶

   *exception*UnreadablePostError[[source]](https://docs.djangoproject.com/en/_modules/django/http/request/#UnreadablePostError)[¶](#django.http.UnreadablePostError)

[UnreadablePostError](#django.http.UnreadablePostError) is raised when a user cancels an upload.

## Sessions Exceptions¶

Sessions exceptions are defined in `django.contrib.sessions.exceptions`.

### SessionInterrupted¶

   *exception*SessionInterrupted[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/sessions/exceptions/#SessionInterrupted)[¶](#django.contrib.sessions.exceptions.SessionInterrupted)

[SessionInterrupted](#django.contrib.sessions.exceptions.SessionInterrupted) is raised when a session is destroyed in a
concurrent request. It’s a subclass of
[BadRequest](#django.core.exceptions.BadRequest).

## Transaction Exceptions¶

Transaction exceptions are defined in `django.db.transaction`.

### TransactionManagementError¶

   *exception*TransactionManagementError[[source]](https://docs.djangoproject.com/en/_modules/django/db/transaction/#TransactionManagementError)[¶](#django.db.transaction.TransactionManagementError)

[TransactionManagementError](#django.db.transaction.TransactionManagementError) is raised for any and all problems
related to database transactions.

## Testing Framework Exceptions¶

Exceptions provided by the `django.test` package.

### RedirectCycleError¶

   *exception*client.RedirectCycleError[¶](#django.test.client.RedirectCycleError)

[RedirectCycleError](#django.test.client.RedirectCycleError) is raised when the test client detects a
loop or an overly long chain of redirects.

## Python Exceptions¶

Django raises built-in Python exceptions when appropriate as well. See the
Python documentation for further information on the [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html#bltin-exceptions).

---

# TheFileobject¶

# TheFileobject¶

The [django.core.files](https://docs.djangoproject.com/en/5.0/ref/#module-django.core.files) module and its submodules contain built-in classes
for basic file handling in Django.

## TheFileclass¶

   *class*File(*file_object*, *name=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/base/#File)[¶](#django.core.files.File)

The [File](#django.core.files.File) class is a thin wrapper around a Python
[file object](https://docs.python.org/3/glossary.html#term-file-object) with some Django-specific additions.
Internally, Django uses this class when it needs to represent a file.

[File](#django.core.files.File) objects have the following attributes and methods:

   name[¶](#django.core.files.File.name)

The name of the file including the relative path from
[MEDIA_ROOT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_ROOT).

    size[¶](#django.core.files.File.size)

The size of the file in bytes.

    file[¶](#django.core.files.File.file)

The underlying [file object](https://docs.python.org/3/glossary.html#term-file-object) that this class wraps.

Be careful with this attribute in subclasses.

Some subclasses of [File](#django.core.files.File), including
[ContentFile](#django.core.files.base.ContentFile) and
[FieldFile](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.fields.files.FieldFile), may replace this
attribute with an object other than a Python [file object](https://docs.python.org/3/glossary.html#term-file-object).
In these cases, this attribute may itself be a [File](#django.core.files.File)
subclass (and not necessarily the same subclass). Whenever
possible, use the attributes and methods of the subclass itself
rather than the those of the subclass’s `file` attribute.

     mode[¶](#django.core.files.File.mode)

The read/write mode for the file.

    open(*mode=None*, **args*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/base/#File.open)[¶](#django.core.files.File.open)

Open or reopen the file (which also does `File.seek(0)`).
The `mode` argument allows the same values
as Python’s built-in [open()](https://docs.python.org/3/library/functions.html#open). `*args` and `**kwargs`
are passed after `mode` to Python’s built-in [open()](https://docs.python.org/3/library/functions.html#open).

When reopening a file, `mode` will override whatever mode the file
was originally opened with; `None` means to reopen with the original
mode.

It can be used as a context manager, e.g. `with file.open() as f:`.

  Changed in Django 5.0:

Support for passing `*args` and `**kwargs` was added.

     __iter__()[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/base/#File.__iter__)[¶](#django.core.files.File.__iter__)

Iterate over the file yielding one line at a time.

    chunks(*chunk_size=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/base/#File.chunks)[¶](#django.core.files.File.chunks)

Iterate over the file yielding “chunks” of a given size. `chunk_size`
defaults to 64 KB.

This is especially useful with very large files since it allows them to
be streamed off disk and avoids storing the whole file in memory.

    multiple_chunks(*chunk_size=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/base/#File.multiple_chunks)[¶](#django.core.files.File.multiple_chunks)

Returns `True` if the file is large enough to require multiple chunks
to access all of its content give some `chunk_size`.

    close()[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/base/#File.close)[¶](#django.core.files.File.close)

Close the file.

In addition to the listed methods, [File](#django.core.files.File) exposes
the following attributes and methods of its `file` object:
`encoding`, `fileno`, `flush`, `isatty`, `newlines`, `read`,
`readinto`, `readline`, `readlines`, `seek`, `tell`,
`truncate`, `write`, `writelines`, `readable()`, `writable()`,
and `seekable()`.

## TheContentFileclass¶

   *class*ContentFile(*content*, *name=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/base/#ContentFile)[¶](#django.core.files.base.ContentFile)

The `ContentFile` class inherits from [File](#django.core.files.File),
but unlike [File](#django.core.files.File) it operates on string content
(bytes also supported), rather than an actual file. For example:

```
from django.core.files.base import ContentFile

f1 = ContentFile("esta frase está en español")
f2 = ContentFile(b"these are bytes")
```

## TheImageFileclass¶

   *class*ImageFile(*file_object*, *name=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/images/#ImageFile)[¶](#django.core.files.images.ImageFile)

Django provides a built-in class specifically for images.
[django.core.files.images.ImageFile](#django.core.files.images.ImageFile) inherits all the attributes
and methods of [File](#django.core.files.File), and additionally
provides the following:

   width[¶](#django.core.files.images.ImageFile.width)

Width of the image in pixels.

    height[¶](#django.core.files.images.ImageFile.height)

Height of the image in pixels.

## Additional methods on files attached to objects¶

Any [File](#django.core.files.File) that is associated with an object (as with `Car.photo`,
below) will also have a couple of extra methods:

   File.save(*name*, *content*, *save=True*)[¶](#django.core.files.File.save)

Saves a new file with the file name and contents provided. This will not
replace the existing file, but will create a new file and update the object
to point to it. If `save` is `True`, the model’s `save()` method will
be called once the file is saved. That is, these two lines:

```
>>> car.photo.save("myphoto.jpg", content, save=False)
>>> car.save()
```

are equivalent to:

```
>>> car.photo.save("myphoto.jpg", content, save=True)
```

Note that the `content` argument must be an instance of either
[File](#django.core.files.File) or of a subclass of [File](#django.core.files.File), such as
[ContentFile](#django.core.files.base.ContentFile).

    File.delete(*save=True*)[¶](#django.core.files.File.delete)

Removes the file from the model instance and deletes the underlying file.
If `save` is `True`, the model’s `save()` method will be called once
the file is deleted.

---

# File storage API¶

# File storage API¶

## Getting the default storage class¶

Django provides convenient ways to access the default storage class:

   storages[¶](#django.core.files.storage.storages)  New in Django 4.2.

Storage instances as defined by [STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES).

    *class*DefaultStorage[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/#DefaultStorage)[¶](#django.core.files.storage.DefaultStorage)

[DefaultStorage](#django.core.files.storage.DefaultStorage) provides
lazy access to the default storage system as defined by `default` key in
[STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES). [DefaultStorage](#django.core.files.storage.DefaultStorage) uses
[storages](#django.core.files.storage.storages) internally.

    default_storage[¶](#django.core.files.storage.default_storage)

[default_storage](#django.core.files.storage.default_storage) is an instance of the
[DefaultStorage](#django.core.files.storage.DefaultStorage).

    get_storage_class(*import_path=None*)[¶](#django.core.files.storage.get_storage_class)

Returns a class or module which implements the storage API.

When called without the `import_path` parameter `get_storage_class`
will return the default storage system as defined by `default` key in
[STORAGES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-STORAGES). If `import_path` is provided, `get_storage_class`
will attempt to import the class or module from the given path and will
return it if successful. An exception will be raised if the import is
unsuccessful.

Deprecated since version 4.2: The `get_storage_class()` function is deprecated. Use
[storages](#django.core.files.storage.storages) instead

## TheFileSystemStorageclass¶

   *class*FileSystemStorage(*location=None*, *base_url=None*, *file_permissions_mode=None*, *directory_permissions_mode=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/filesystem/#FileSystemStorage)[¶](#django.core.files.storage.FileSystemStorage)

The [FileSystemStorage](#django.core.files.storage.FileSystemStorage) class implements
basic file storage on a local filesystem. It inherits from
[Storage](#django.core.files.storage.Storage) and provides implementations
for all the public methods thereof.

   location[¶](#django.core.files.storage.FileSystemStorage.location)

Absolute path to the directory that will hold the files.
Defaults to the value of your [MEDIA_ROOT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_ROOT) setting.

    base_url[¶](#django.core.files.storage.FileSystemStorage.base_url)

URL that serves the files stored at this location.
Defaults to the value of your [MEDIA_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_URL) setting.

    file_permissions_mode[¶](#django.core.files.storage.FileSystemStorage.file_permissions_mode)

The file system permissions that the file will receive when it is
saved. Defaults to [FILE_UPLOAD_PERMISSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-FILE_UPLOAD_PERMISSIONS).

    directory_permissions_mode[¶](#django.core.files.storage.FileSystemStorage.directory_permissions_mode)

The file system permissions that the directory will receive when it is
saved. Defaults to [FILE_UPLOAD_DIRECTORY_PERMISSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-FILE_UPLOAD_DIRECTORY_PERMISSIONS).

Note

The `FileSystemStorage.delete()` method will not raise
an exception if the given file name does not exist.

    get_created_time(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/filesystem/#FileSystemStorage.get_created_time)[¶](#django.core.files.storage.FileSystemStorage.get_created_time)

Returns a [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) of the system’s ctime, i.e.
[os.path.getctime()](https://docs.python.org/3/library/os.path.html#os.path.getctime). On some systems (like Unix), this is the
time of the last metadata change, and on others (like Windows), it’s
the creation time of the file.

## TheInMemoryStorageclass¶

  New in Django 4.2.    *class*InMemoryStorage(*location=None*, *base_url=None*, *file_permissions_mode=None*, *directory_permissions_mode=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/memory/#InMemoryStorage)[¶](#django.core.files.storage.InMemoryStorage)

The [InMemoryStorage](#django.core.files.storage.InMemoryStorage) class implements
a memory-based file storage. It has no persistence, but can be useful for
speeding up tests by avoiding disk access.

   location[¶](#django.core.files.storage.InMemoryStorage.location)

Absolute path to the directory name assigned to files. Defaults to the
value of your [MEDIA_ROOT](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_ROOT) setting.

    base_url[¶](#django.core.files.storage.InMemoryStorage.base_url)

URL that serves the files stored at this location.
Defaults to the value of your [MEDIA_URL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-MEDIA_URL) setting.

    file_permissions_mode[¶](#django.core.files.storage.InMemoryStorage.file_permissions_mode)

The file system permissions assigned to files, provided for
compatibility with `FileSystemStorage`. Defaults to
[FILE_UPLOAD_PERMISSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-FILE_UPLOAD_PERMISSIONS).

    directory_permissions_mode[¶](#django.core.files.storage.InMemoryStorage.directory_permissions_mode)

The file system permissions assigned to directories, provided for
compatibility with `FileSystemStorage`. Defaults to
[FILE_UPLOAD_DIRECTORY_PERMISSIONS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-FILE_UPLOAD_DIRECTORY_PERMISSIONS).

## TheStorageclass¶

   *class*Storage[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage)[¶](#django.core.files.storage.Storage)

The [Storage](#django.core.files.storage.Storage) class provides a
standardized API for storing files, along with a set of default
behaviors that all other storage systems can inherit or override
as necessary.

Note

When methods return naive `datetime` objects, the effective timezone
used will be the current value of `os.environ['TZ']`; note that this
is usually set from Django’s [TIME_ZONE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TIME_ZONE).

    delete(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.delete)[¶](#django.core.files.storage.Storage.delete)

Deletes the file referenced by `name`. If deletion is not supported
on the target storage system this will raise `NotImplementedError`
instead.

    exists(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.exists)[¶](#django.core.files.storage.Storage.exists)

Returns `True` if a file referenced by the given name already exists
in the storage system, or `False` if the name is available for a new
file.

    get_accessed_time(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.get_accessed_time)[¶](#django.core.files.storage.Storage.get_accessed_time)

Returns a [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) of the last accessed time of the
file. For storage systems unable to return the last accessed time this
will raise [NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError).

If [USE_TZ](https://docs.djangoproject.com/en/5.0/settings/#std-setting-USE_TZ) is `True`, returns an aware `datetime`,
otherwise returns a naive `datetime` in the local timezone.

    get_alternative_name(*file_root*, *file_ext*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.get_alternative_name)[¶](#django.core.files.storage.Storage.get_alternative_name)

Returns an alternative filename based on the `file_root` and
`file_ext` parameters, an underscore plus a random 7 character
alphanumeric string is appended to the filename before the extension.

    get_available_name(*name*, *max_length=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.get_available_name)[¶](#django.core.files.storage.Storage.get_available_name)

Returns a filename based on the `name` parameter that’s free and
available for new content to be written to on the target storage
system.

The length of the filename will not exceed `max_length`, if provided.
If a free unique filename cannot be found, a
[SuspiciousFileOperation](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.SuspiciousOperation) exception will be raised.

If a file with `name` already exists, [get_alternative_name()](https://docs.djangoproject.com/en/howto/custom-file-storage/#django.core.files.storage.get_alternative_name) is
called to obtain an alternative name.

    get_created_time(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.get_created_time)[¶](#django.core.files.storage.Storage.get_created_time)

Returns a [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) of the creation time of the file.
For storage systems unable to return the creation time this will raise
[NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError).

If [USE_TZ](https://docs.djangoproject.com/en/5.0/settings/#std-setting-USE_TZ) is `True`, returns an aware `datetime`,
otherwise returns a naive `datetime` in the local timezone.

    get_modified_time(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.get_modified_time)[¶](#django.core.files.storage.Storage.get_modified_time)

Returns a [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) of the last modified time of the
file. For storage systems unable to return the last modified time this
will raise [NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError).

If [USE_TZ](https://docs.djangoproject.com/en/5.0/settings/#std-setting-USE_TZ) is `True`, returns an aware `datetime`,
otherwise returns a naive `datetime` in the local timezone.

    get_valid_name(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.get_valid_name)[¶](#django.core.files.storage.Storage.get_valid_name)

Returns a filename based on the `name` parameter that’s suitable
for use on the target storage system.

    generate_filename(*filename*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.generate_filename)[¶](#django.core.files.storage.Storage.generate_filename)

Validates the `filename` by calling [get_valid_name()](https://docs.djangoproject.com/en/howto/custom-file-storage/#django.core.files.storage.get_valid_name) and
returns a filename to be passed to the [save()](#django.core.files.storage.Storage.save) method.

The `filename` argument may include a path as returned by
[FileField.upload_to](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.FileField.upload_to).
In that case, the path won’t be passed to [get_valid_name()](https://docs.djangoproject.com/en/howto/custom-file-storage/#django.core.files.storage.get_valid_name) but
will be prepended back to the resulting name.

The default implementation uses [os.path](https://docs.python.org/3/library/os.path.html#module-os.path) operations. Override
this method if that’s not appropriate for your storage.

    listdir(*path*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.listdir)[¶](#django.core.files.storage.Storage.listdir)

Lists the contents of the specified path, returning a 2-tuple of lists;
the first item being directories, the second item being files. For
storage systems that aren’t able to provide such a listing, this will
raise a `NotImplementedError` instead.

    open(*name*, *mode='rb'*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.open)[¶](#django.core.files.storage.Storage.open)

Opens the file given by `name`. Note that although the returned file
is guaranteed to be a `File` object, it might actually be some
subclass. In the case of remote file storage this means that
reading/writing could be quite slow, so be warned.

    path(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.path)[¶](#django.core.files.storage.Storage.path)

The local filesystem path where the file can be opened using Python’s
standard `open()`. For storage systems that aren’t accessible from
the local filesystem, this will raise `NotImplementedError` instead.

    save(*name*, *content*, *max_length=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.save)[¶](#django.core.files.storage.Storage.save)

Saves a new file using the storage system, preferably with the name
specified. If there already exists a file with this name `name`, the
storage system may modify the filename as necessary to get a unique
name. The actual name of the stored file will be returned.

The `max_length` argument is passed along to
[get_available_name()](https://docs.djangoproject.com/en/howto/custom-file-storage/#django.core.files.storage.get_available_name).

The `content` argument must be an instance of
[django.core.files.File](https://docs.djangoproject.com/en/5.0/ref/file/#django.core.files.File) or a file-like object that can be
wrapped in `File`.

    size(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.size)[¶](#django.core.files.storage.Storage.size)

Returns the total size, in bytes, of the file referenced by `name`.
For storage systems that aren’t able to return the file size this will
raise `NotImplementedError` instead.

    url(*name*)[[source]](https://docs.djangoproject.com/en/_modules/django/core/files/storage/base/#Storage.url)[¶](#django.core.files.storage.Storage.url)

Returns the URL where the contents of the file referenced by `name`
can be accessed. For storage systems that don’t support access by URL
this will raise `NotImplementedError` instead.
