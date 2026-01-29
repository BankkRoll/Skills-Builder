# Serializing Django objects¶ and more

# Serializing Django objects¶

# Serializing Django objects¶

Django’s serialization framework provides a mechanism for “translating” Django
models into other formats. Usually these other formats will be text-based and
used for sending Django data over a wire, but it’s possible for a
serializer to handle any format (text-based or not).

See also

If you just want to get some data from your tables into a serialized
form, you could use the [dumpdata](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-dumpdata) management command.

## Serializing data¶

At the highest level, you can serialize data like this:

```
from django.core import serializers

data = serializers.serialize("xml", SomeModel.objects.all())
```

The arguments to the `serialize` function are the format to serialize the data
to (see [Serialization formats](#id2)) and a
[QuerySet](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet) to serialize. (Actually, the second
argument can be any iterator that yields Django model instances, but it’ll
almost always be a QuerySet).

   django.core.serializers.get_serializer(*format*)[¶](#django.core.serializers.get_serializer)

You can also use a serializer object directly:

```
XMLSerializer = serializers.get_serializer("xml")
xml_serializer = XMLSerializer()
xml_serializer.serialize(queryset)
data = xml_serializer.getvalue()
```

This is useful if you want to serialize data directly to a file-like object
(which includes an [HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse)):

```
with open("file.xml", "w") as out:
    xml_serializer.serialize(SomeModel.objects.all(), stream=out)
```

Note

Calling [get_serializer()](#django.core.serializers.get_serializer) with an unknown
[format](#serialization-formats) will raise a
`django.core.serializers.SerializerDoesNotExist` exception.

### Subset of fields¶

If you only want a subset of fields to be serialized, you can
specify a `fields` argument to the serializer:

```
from django.core import serializers

data = serializers.serialize("xml", SomeModel.objects.all(), fields=["name", "size"])
```

In this example, only the `name` and `size` attributes of each model will
be serialized. The primary key is always serialized as the `pk` element in the
resulting output; it never appears in the `fields` part.

Note

Depending on your model, you may find that it is not possible to
deserialize a model that only serializes a subset of its fields. If a
serialized object doesn’t specify all the fields that are required by a
model, the deserializer will not be able to save deserialized instances.

### Inherited models¶

If you have a model that is defined using an [abstract base class](https://docs.djangoproject.com/en/5.0/db/models/#abstract-base-classes), you don’t have to do anything special to serialize
that model. Call the serializer on the object (or objects) that you want to
serialize, and the output will be a complete representation of the serialized
object.

However, if you have a model that uses [multi-table inheritance](https://docs.djangoproject.com/en/5.0/db/models/#multi-table-inheritance), you also need to serialize all of the base classes
for the model. This is because only the fields that are locally defined on the
model will be serialized. For example, consider the following models:

```
class Place(models.Model):
    name = models.CharField(max_length=50)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
```

If you only serialize the Restaurant model:

```
data = serializers.serialize("xml", Restaurant.objects.all())
```

the fields on the serialized output will only contain the `serves_hot_dogs`
attribute. The `name` attribute of the base class will be ignored.

In order to fully serialize your `Restaurant` instances, you will need to
serialize the `Place` models as well:

```
all_objects = [*Restaurant.objects.all(), *Place.objects.all()]
data = serializers.serialize("xml", all_objects)
```

## Deserializing data¶

Deserializing data is very similar to serializing it:

```
for obj in serializers.deserialize("xml", data):
    do_something_with(obj)
```

As you can see, the `deserialize` function takes the same format argument as
`serialize`, a string or stream of data, and returns an iterator.

However, here it gets slightly complicated. The objects returned by the
`deserialize` iterator *aren’t* regular Django objects. Instead, they are
special `DeserializedObject` instances that wrap a created – but unsaved –
object and any associated relationship data.

Calling `DeserializedObject.save()` saves the object to the database.

Note

If the `pk` attribute in the serialized data doesn’t exist or is
null, a new instance will be saved to the database.

This ensures that deserializing is a non-destructive operation even if the
data in your serialized representation doesn’t match what’s currently in the
database. Usually, working with these `DeserializedObject` instances looks
something like:

```
for deserialized_object in serializers.deserialize("xml", data):
    if object_should_be_saved(deserialized_object):
        deserialized_object.save()
```

In other words, the usual use is to examine the deserialized objects to make
sure that they are “appropriate” for saving before doing so. If you trust your
data source you can instead save the object directly and move on.

The Django object itself can be inspected as `deserialized_object.object`.
If fields in the serialized data do not exist on a model, a
`DeserializationError` will be raised unless the `ignorenonexistent`
argument is passed in as `True`:

```
serializers.deserialize("xml", data, ignorenonexistent=True)
```

## Serialization formats¶

Django supports a number of serialization formats, some of which require you
to install third-party Python modules:

| Identifier | Information |
| --- | --- |
| xml | Serializes to and from a simple XML dialect. |
| json | Serializes to and fromJSON. |
| jsonl | Serializes to and fromJSONL. |
| yaml | Serializes to YAML (YAML Ain’t a Markup Language). This
serializer is only available ifPyYAMLis installed. |

### XML¶

The basic XML serialization format looks like this:

```
<?xml version="1.0" encoding="utf-8"?>
<django-objects version="1.0">
    <object pk="123" model="sessions.session">
        <field type="DateTimeField" name="expire_date">2013-01-16T08:16:59.844560+00:00</field>
        
    </object>
</django-objects>
```

The whole collection of objects that is either serialized or deserialized is
represented by a `<django-objects>`-tag which contains multiple
`<object>`-elements. Each such object has two attributes: “pk” and “model”,
the latter being represented by the name of the app (“sessions”) and the
lowercase name of the model (“session”) separated by a dot.

Each field of the object is serialized as a `<field>`-element sporting the
fields “type” and “name”. The text content of the element represents the value
that should be stored.

Foreign keys and other relational fields are treated a little bit differently:

```
<object pk="27" model="auth.permission">
    
    <field to="contenttypes.contenttype" name="content_type" rel="ManyToOneRel">9</field>
    
</object>
```

In this example we specify that the `auth.Permission` object with the PK 27
has a foreign key to the `contenttypes.ContentType` instance with the PK 9.

ManyToMany-relations are exported for the model that binds them. For instance,
the `auth.User` model has such a relation to the `auth.Permission` model:

```
<object pk="1" model="auth.user">
    
    <field to="auth.permission" name="user_permissions" rel="ManyToManyRel">
        <object pk="46"></object>
        <object pk="47"></object>
    </field>
</object>
```

This example links the given user with the permission models with PKs 46 and 47.

Control characters

If the content to be serialized contains control characters that are not
accepted in the XML 1.0 standard, the serialization will fail with a
[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError) exception. Read also the W3C’s explanation of [HTML,
XHTML, XML and Control Codes](https://www.w3.org/International/questions/qa-controls).

### JSON¶

When staying with the same example data as before it would be serialized as
JSON in the following way:

```
[
    {
        "pk": "4b678b301dfd8a4e0dad910de3ae245b",
        "model": "sessions.session",
        "fields": {
            "expire_date": "2013-01-16T08:16:59.844Z",
            # ...
        },
    }
]
```

The formatting here is a bit simpler than with XML. The whole collection
is just represented as an array and the objects are represented by JSON objects
with three properties: “pk”, “model” and “fields”. “fields” is again an object
containing each field’s name and value as property and property-value
respectively.

Foreign keys have the PK of the linked object as property value.
ManyToMany-relations are serialized for the model that defines them and are
represented as a list of PKs.

Be aware that not all Django output can be passed unmodified to [json](https://docs.python.org/3/library/json.html#module-json).
For example, if you have some custom type in an object to be serialized, you’ll
have to write a custom [json](https://docs.python.org/3/library/json.html#module-json) encoder for it. Something like this will
work:

```
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)
```

You can then pass `cls=LazyEncoder` to the `serializers.serialize()`
function:

```
from django.core.serializers import serialize

serialize("json", SomeModel.objects.all(), cls=LazyEncoder)
```

Also note that GeoDjango provides a [customized GeoJSON serializer](https://docs.djangoproject.com/en/ref/contrib/gis/serializers/).

#### DjangoJSONEncoder¶

   *class*django.core.serializers.json.DjangoJSONEncoder[¶](#django.core.serializers.json.DjangoJSONEncoder)

The JSON serializer uses `DjangoJSONEncoder` for encoding. A subclass of
[JSONEncoder](https://docs.python.org/3/library/json.html#json.JSONEncoder), it handles these additional types:

  [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime)

A string of the form `YYYY-MM-DDTHH:mm:ss.sssZ` or
`YYYY-MM-DDTHH:mm:ss.sss+HH:MM` as defined in [ECMA-262](https://262.ecma-international.org/5.1/#sec-15.9.1.15).

  [date](https://docs.python.org/3/library/datetime.html#datetime.date)

A string of the form `YYYY-MM-DD` as defined in [ECMA-262](https://262.ecma-international.org/5.1/#sec-15.9.1.15).

  [time](https://docs.python.org/3/library/datetime.html#datetime.time)

A string of the form `HH:MM:ss.sss` as defined in [ECMA-262](https://262.ecma-international.org/5.1/#sec-15.9.1.15).

  [timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta)

A string representing a duration as defined in ISO-8601. For example,
`timedelta(days=1, hours=2, seconds=3.4)` is represented as
`'P1DT02H00M03.400000S'`.

  [Decimal](https://docs.python.org/3/library/decimal.html#decimal.Decimal), `Promise` (`django.utils.functional.lazy()` objects), [UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID)

A string representation of the object.

### JSONL¶

*JSONL* stands for *JSON Lines*. With this format, objects are separated by new
lines, and each line contains a valid JSON object. JSONL serialized data looks
like this:

```
{"pk": "4b678b301dfd8a4e0dad910de3ae245b", "model": "sessions.session", "fields": {...}}
{"pk": "88bea72c02274f3c9bf1cb2bb8cee4fc", "model": "sessions.session", "fields": {...}}
{"pk": "9cf0e26691b64147a67e2a9f06ad7a53", "model": "sessions.session", "fields": {...}}
```

JSONL can be useful for populating large databases, since the data can be
processed line by line, rather than being loaded into memory all at once.

### YAML¶

YAML serialization looks quite similar to JSON. The object list is serialized
as a sequence mappings with the keys “pk”, “model” and “fields”. Each field is
again a mapping with the key being name of the field and the value the value:

```
- model: sessions.session
  pk: 4b678b301dfd8a4e0dad910de3ae245b
  fields:
    expire_date: 2013-01-16 08:16:59.844560+00:00
```

Referential fields are again represented by the PK or sequence of PKs.

## Natural keys¶

The default serialization strategy for foreign keys and many-to-many relations
is to serialize the value of the primary key(s) of the objects in the relation.
This strategy works well for most objects, but it can cause difficulty in some
circumstances.

Consider the case of a list of objects that have a foreign key referencing
[ContentType](https://docs.djangoproject.com/en/ref/contrib/contenttypes/#django.contrib.contenttypes.models.ContentType). If you’re going to
serialize an object that refers to a content type, then you need to have a way
to refer to that content type to begin with. Since `ContentType` objects are
automatically created by Django during the database synchronization process,
the primary key of a given content type isn’t easy to predict; it will
depend on how and when [migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate) was executed. This is true for all
models which automatically generate objects, notably including
[Permission](https://docs.djangoproject.com/en/ref/contrib/auth/#django.contrib.auth.models.Permission),
[Group](https://docs.djangoproject.com/en/ref/contrib/auth/#django.contrib.auth.models.Group), and
[User](https://docs.djangoproject.com/en/ref/contrib/auth/#django.contrib.auth.models.User).

Warning

You should never include automatically generated objects in a fixture or
other serialized data. By chance, the primary keys in the fixture
may match those in the database and loading the fixture will
have no effect. In the more likely case that they don’t match, the fixture
loading will fail with an [IntegrityError](https://docs.djangoproject.com/en/ref/exceptions/#django.db.IntegrityError).

There is also the matter of convenience. An integer id isn’t always
the most convenient way to refer to an object; sometimes, a
more natural reference would be helpful.

It is for these reasons that Django provides *natural keys*. A natural
key is a tuple of values that can be used to uniquely identify an
object instance without using the primary key value.

### Deserialization of natural keys¶

Consider the following two models:

```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    birthdate = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"],
                name="unique_first_last_name",
            ),
        ]

class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
```

Ordinarily, serialized data for `Book` would use an integer to refer to
the author. For example, in JSON, a Book might be serialized as:

```
...
{"pk": 1, "model": "store.book", "fields": {"name": "Mostly Harmless", "author": 42}}
...
```

This isn’t a particularly natural way to refer to an author. It
requires that you know the primary key value for the author; it also
requires that this primary key value is stable and predictable.

However, if we add natural key handling to Person, the fixture becomes
much more humane. To add natural key handling, you define a default
Manager for Person with a `get_by_natural_key()` method. In the case
of a Person, a good natural key might be the pair of first and last
name:

```
from django.db import models

class PersonManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()

    objects = PersonManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"],
                name="unique_first_last_name",
            ),
        ]
```

Now books can use that natural key to refer to `Person` objects:

```
...
{
    "pk": 1,
    "model": "store.book",
    "fields": {"name": "Mostly Harmless", "author": ["Douglas", "Adams"]},
}
...
```

When you try to load this serialized data, Django will use the
`get_by_natural_key()` method to resolve `["Douglas", "Adams"]`
into the primary key of an actual `Person` object.

Note

Whatever fields you use for a natural key must be able to uniquely
identify an object. This will usually mean that your model will
have a uniqueness clause (either `unique=True` on a single field, or a
`UniqueConstraint` or `unique_together` over multiple fields) for the
field or fields in your natural key. However, uniqueness doesn’t need to be
enforced at the database level. If you are certain that a set of fields
will be effectively unique, you can still use those fields as a natural
key.

Deserialization of objects with no primary key will always check whether the
model’s manager has a `get_by_natural_key()` method and if so, use it to
populate the deserialized object’s primary key.

### Serialization of natural keys¶

So how do you get Django to emit a natural key when serializing an object?
Firstly, you need to add another method – this time to the model itself:

```
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()

    objects = PersonManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"],
                name="unique_first_last_name",
            ),
        ]

    def natural_key(self):
        return (self.first_name, self.last_name)
```

That method should always return a natural key tuple – in this
example, `(first name, last name)`. Then, when you call
`serializers.serialize()`, you provide `use_natural_foreign_keys=True`
or `use_natural_primary_keys=True` arguments:

```
>>> serializers.serialize(
...     "json",
...     [book1, book2],
...     indent=2,
...     use_natural_foreign_keys=True,
...     use_natural_primary_keys=True,
... )
```

When `use_natural_foreign_keys=True` is specified, Django will use the
`natural_key()` method to serialize any foreign key reference to objects
of the type that defines the method.

When `use_natural_primary_keys=True` is specified, Django will not provide the
primary key in the serialized data of this object since it can be calculated
during deserialization:

```
...
{
    "model": "store.person",
    "fields": {
        "first_name": "Douglas",
        "last_name": "Adams",
        "birth_date": "1952-03-11",
    },
}
...
```

This can be useful when you need to load serialized data into an existing
database and you cannot guarantee that the serialized primary key value is not
already in use, and do not need to ensure that deserialized objects retain the
same primary keys.

If you are using [dumpdata](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-dumpdata) to generate serialized data, use the
[dumpdata--natural-foreign](https://docs.djangoproject.com/en/ref/django-admin/#cmdoption-dumpdata-natural-foreign) and [dumpdata--natural-primary](https://docs.djangoproject.com/en/ref/django-admin/#cmdoption-dumpdata-natural-primary)
command line flags to generate natural keys.

Note

You don’t need to define both `natural_key()` and
`get_by_natural_key()`. If you don’t want Django to output
natural keys during serialization, but you want to retain the
ability to load natural keys, then you can opt to not implement
the `natural_key()` method.

Conversely, if (for some strange reason) you want Django to output
natural keys during serialization, but *not* be able to load those
key values, just don’t define the `get_by_natural_key()` method.

### Natural keys and forward references¶

Sometimes when you use [natural foreign keys](#topics-serialization-natural-keys) you’ll need to deserialize data where
an object has a foreign key referencing another object that hasn’t yet been
deserialized. This is called a “forward reference”.

For instance, suppose you have the following objects in your fixture:

```
...
{
    "model": "store.book",
    "fields": {"name": "Mostly Harmless", "author": ["Douglas", "Adams"]},
},
...
{"model": "store.person", "fields": {"first_name": "Douglas", "last_name": "Adams"}},
...
```

In order to handle this situation, you need to pass
`handle_forward_references=True` to `serializers.deserialize()`. This will
set the `deferred_fields` attribute on the `DeserializedObject` instances.
You’ll need to keep track of `DeserializedObject` instances where this
attribute isn’t `None` and later call `save_deferred_fields()` on them.

Typical usage looks like this:

```
objs_with_deferred_fields = []

for obj in serializers.deserialize("xml", data, handle_forward_references=True):
    obj.save()
    if obj.deferred_fields is not None:
        objs_with_deferred_fields.append(obj)

for obj in objs_with_deferred_fields:
    obj.save_deferred_fields()
```

For this to work, the `ForeignKey` on the referencing model must have
`null=True`.

### Dependencies during serialization¶

It’s often possible to avoid explicitly having to handle forward references by
taking care with the ordering of objects within a fixture.

To help with this, calls to [dumpdata](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-dumpdata) that use the [dumpdata--natural-foreign](https://docs.djangoproject.com/en/ref/django-admin/#cmdoption-dumpdata-natural-foreign) option will serialize any model with a `natural_key()`
method before serializing standard primary key objects.

However, this may not always be enough. If your natural key refers to
another object (by using a foreign key or natural key to another object
as part of a natural key), then you need to be able to ensure that
the objects on which a natural key depends occur in the serialized data
before the natural key requires them.

To control this ordering, you can define dependencies on your
`natural_key()` methods. You do this by setting a `dependencies`
attribute on the `natural_key()` method itself.

For example, let’s add a natural key to the `Book` model from the
example above:

```
class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)

    def natural_key(self):
        return (self.name,) + self.author.natural_key()
```

The natural key for a `Book` is a combination of its name and its
author. This means that `Person` must be serialized before `Book`.
To define this dependency, we add one extra line:

```
def natural_key(self):
    return (self.name,) + self.author.natural_key()

natural_key.dependencies = ["example_app.person"]
```

This definition ensures that all `Person` objects are serialized before
any `Book` objects. In turn, any object referencing `Book` will be
serialized after both `Person` and `Book` have been serialized.

---

# Django settings¶

# Django settings¶

A Django settings file contains all the configuration of your Django
installation. This document explains how settings work and which settings are
available.

## The basics¶

A settings file is just a Python module with module-level variables.

Here are a couple of example settings:

```
ALLOWED_HOSTS = ["www.example.com"]
DEBUG = False
DEFAULT_FROM_EMAIL = "webmaster@example.com"
```

Note

If you set [DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) to `False`, you also need to properly set
the [ALLOWED_HOSTS](https://docs.djangoproject.com/en/ref/settings/#std-setting-ALLOWED_HOSTS) setting.

Because a settings file is a Python module, the following apply:

- It doesn’t allow for Python syntax errors.
- It can assign settings dynamically using normal Python syntax.
  For example:
  ```
  MY_SETTING = [str(i) for i in range(30)]
  ```
- It can import values from other settings files.

## Designating the settings¶

   DJANGO_SETTINGS_MODULE[¶](#envvar-DJANGO_SETTINGS_MODULE)

When you use Django, you have to tell it which settings you’re using. Do this
by using an environment variable, [DJANGO_SETTINGS_MODULE](#envvar-DJANGO_SETTINGS_MODULE).

The value of [DJANGO_SETTINGS_MODULE](#envvar-DJANGO_SETTINGS_MODULE) should be in Python path syntax,
e.g. `mysite.settings`. Note that the settings module should be on the
Python [sys.path](https://docs.python.org/3/library/sys.html#sys.path).

### Thedjango-adminutility¶

When using [django-admin](https://docs.djangoproject.com/en/ref/django-admin/), you can either set the
environment variable once, or explicitly pass in the settings module each time
you run the utility.

Example (Unix Bash shell):

```
export DJANGO_SETTINGS_MODULE=mysite.settings
django-admin runserver
```

Example (Windows shell):

```
set DJANGO_SETTINGS_MODULE=mysite.settings
django-admin runserver
```

Use the `--settings` command-line argument to specify the settings manually:

```
django-admin runserver --settings=mysite.settings
```

### On the server (mod_wsgi)¶

In your live server environment, you’ll need to tell your WSGI
application what settings file to use. Do that with `os.environ`:

```
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
```

Read the [Django mod_wsgi documentation](https://docs.djangoproject.com/en/howto/deployment/wsgi/modwsgi/) for more information and other common
elements to a Django WSGI application.

## Default settings¶

A Django settings file doesn’t have to define any settings if it doesn’t need
to. Each setting has a sensible default value. These defaults live in the
module [django/conf/global_settings.py](https://github.com/django/django/blob/main/django/conf/global_settings.py).

Here’s the algorithm Django uses in compiling settings:

- Load settings from `global_settings.py`.
- Load settings from the specified settings file, overriding the global
  settings as necessary.

Note that a settings file should *not* import from `global_settings`, because
that’s redundant.

### Seeing which settings you’ve changed¶

The command `python manage.py diffsettings` displays differences between the
current settings file and Django’s default settings.

For more, see the [diffsettings](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-diffsettings) documentation.

## Using settings in Python code¶

In your Django apps, use settings by importing the object
`django.conf.settings`. Example:

```
from django.conf import settings

if settings.DEBUG:
    # Do something
    ...
```

Note that `django.conf.settings` isn’t a module – it’s an object. So
importing individual settings is not possible:

```
from django.conf.settings import DEBUG  # This won't work.
```

Also note that your code should *not* import from either `global_settings` or
your own settings file. `django.conf.settings` abstracts the concepts of
default settings and site-specific settings; it presents a single interface.
It also decouples the code that uses settings from the location of your
settings.

## Altering settings at runtime¶

You shouldn’t alter settings in your applications at runtime. For example,
don’t do this in a view:

```
from django.conf import settings

settings.DEBUG = True  # Don't do this!
```

The only place you should assign to settings is in a settings file.

## Security¶

Because a settings file contains sensitive information, such as the database
password, you should make every attempt to limit access to it. For example,
change its file permissions so that only you and your web server’s user can
read it. This is especially important in a shared-hosting environment.

## Available settings¶

For a full list of available settings, see the [settings reference](https://docs.djangoproject.com/en/ref/settings/).

## Creating your own settings¶

There’s nothing stopping you from creating your own settings, for your own
Django apps, but follow these guidelines:

- Setting names must be all uppercase.
- Don’t reinvent an already-existing setting.

For settings that are sequences, Django itself uses lists, but this is only
a convention.

## Using settings without settingDJANGO_SETTINGS_MODULE¶

In some cases, you might want to bypass the [DJANGO_SETTINGS_MODULE](#envvar-DJANGO_SETTINGS_MODULE)
environment variable. For example, if you’re using the template system by
itself, you likely don’t want to have to set up an environment variable
pointing to a settings module.

In these cases, you can configure Django’s settings manually. Do this by
calling:

   django.conf.settings.configure(*default_settings*, ***settings*)[¶](#django.conf.settings.configure)

Example:

```
from django.conf import settings

settings.configure(DEBUG=True)
```

Pass `configure()` as many keyword arguments as you’d like, with each keyword
argument representing a setting and its value. Each argument name should be all
uppercase, with the same name as the settings described above. If a particular
setting is not passed to `configure()` and is needed at some later point,
Django will use the default setting value.

Configuring Django in this fashion is mostly necessary – and, indeed,
recommended – when you’re using a piece of the framework inside a larger
application.

Consequently, when configured via `settings.configure()`, Django will not
make any modifications to the process environment variables (see the
documentation of [TIME_ZONE](https://docs.djangoproject.com/en/ref/settings/#std-setting-TIME_ZONE) for why this would normally occur). It’s
assumed that you’re already in full control of your environment in these
cases.

### Custom default settings¶

If you’d like default values to come from somewhere other than
`django.conf.global_settings`, you can pass in a module or class that
provides the default settings as the `default_settings` argument (or as the
first positional argument) in the call to `configure()`.

In this example, default settings are taken from `myapp_defaults`, and the
[DEBUG](https://docs.djangoproject.com/en/ref/settings/#std-setting-DEBUG) setting is set to `True`, regardless of its value in
`myapp_defaults`:

```
from django.conf import settings
from myapp import myapp_defaults

settings.configure(default_settings=myapp_defaults, DEBUG=True)
```

The following example, which uses `myapp_defaults` as a positional argument,
is equivalent:

```
settings.configure(myapp_defaults, DEBUG=True)
```

Normally, you will not need to override the defaults in this fashion. The
Django defaults are sufficiently tame that you can safely use them. Be aware
that if you do pass in a new default module, it entirely *replaces* the Django
defaults, so you must specify a value for every possible setting that might be
used in the code you are importing. Check in
`django.conf.settings.global_settings` for the full list.

### Eitherconfigure()orDJANGO_SETTINGS_MODULEis required¶

If you’re not setting the [DJANGO_SETTINGS_MODULE](#envvar-DJANGO_SETTINGS_MODULE) environment
variable, you *must* call `configure()` at some point before using any code
that reads settings.

If you don’t set [DJANGO_SETTINGS_MODULE](#envvar-DJANGO_SETTINGS_MODULE) and don’t call
`configure()`, Django will raise an `ImportError` exception the first time
a setting is accessed.

If you set [DJANGO_SETTINGS_MODULE](#envvar-DJANGO_SETTINGS_MODULE), access settings values somehow,
*then* call `configure()`, Django will raise a `RuntimeError` indicating
that settings have already been configured. There is a property for this
purpose:

   django.conf.settings.configured[¶](#django.conf.settings.configured)

For example:

```
from django.conf import settings

if not settings.configured:
    settings.configure(myapp_defaults, DEBUG=True)
```

Also, it’s an error to call `configure()` more than once, or to call
`configure()` after any setting has been accessed.

It boils down to this: Use exactly one of either `configure()` or
[DJANGO_SETTINGS_MODULE](#envvar-DJANGO_SETTINGS_MODULE). Not both, and not neither.

### Callingdjango.setup()is required for “standalone” Django usage¶

If you’re using components of Django “standalone” – for example, writing a
Python script which loads some Django templates and renders them, or uses the
ORM to fetch some data – there’s one more step you’ll need in addition to
configuring settings.

After you’ve either set [DJANGO_SETTINGS_MODULE](#envvar-DJANGO_SETTINGS_MODULE) or called
`configure()`, you’ll need to call [django.setup()](https://docs.djangoproject.com/en/ref/applications/#django.setup) to load your
settings and populate Django’s application registry. For example:

```
import django
from django.conf import settings
from myapp import myapp_defaults

settings.configure(default_settings=myapp_defaults, DEBUG=True)
django.setup()

# Now this script or any imported module can use any part of Django it needs.
from myapp import models
```

Note that calling `django.setup()` is only necessary if your code is truly
standalone. When invoked by your web server, or through [django-admin](https://docs.djangoproject.com/en/ref/django-admin/), Django will handle this for you.

`django.setup()` may only be called once.

Therefore, avoid putting reusable application logic in standalone scripts
so that you have to import from the script elsewhere in your application.
If you can’t avoid that, put the call to `django.setup()` inside an
`if` block:

```
if __name__ == "__main__":
    import django

    django.setup()
```

See also

  [The Settings Reference](https://docs.djangoproject.com/en/ref/settings/)

Contains the complete list of core and contrib app settings.

---

# Signals¶

# Signals¶

Django includes a “signal dispatcher” which helps decoupled applications get
notified when actions occur elsewhere in the framework. In a nutshell, signals
allow certain *senders* to notify a set of *receivers* that some action has
taken place. They’re especially useful when many pieces of code may be
interested in the same events.

For example, a third-party app can register to be notified of settings
changes:

```
from django.apps import AppConfig
from django.core.signals import setting_changed

def my_callback(sender, **kwargs):
    print("Setting changed!")

class MyAppConfig(AppConfig):
    ...

    def ready(self):
        setting_changed.connect(my_callback)
```

Django’s [built-in signals](https://docs.djangoproject.com/en/ref/signals/) let user code get notified of
certain actions.

You can also define and send your own custom signals. See
[Defining and sending signals](#defining-and-sending-signals) below.

Warning

Signals give the appearance of loose coupling, but they can quickly lead to
code that is hard to understand, adjust and debug.

Where possible you should opt for directly calling the handling code,
rather than dispatching via a signal.

## Listening to signals¶

To receive a signal, register a *receiver* function using the
[Signal.connect()](#django.dispatch.Signal.connect) method. The receiver function is called when the signal
is sent. All of the signal’s receiver functions are called one at a time, in
the order they were registered.

   Signal.connect(*receiver*, *sender=None*, *weak=True*, *dispatch_uid=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/dispatch/dispatcher/#Signal.connect)[¶](#django.dispatch.Signal.connect)  Parameters:

- **receiver** – The callback function which will be connected to this
  signal. See [Receiver functions](#receiver-functions) for more information.
- **sender** – Specifies a particular sender to receive signals from. See
  [Connecting to signals sent by specific senders](#connecting-to-specific-signals) for more information.
- **weak** – Django stores signal handlers as weak references by
  default. Thus, if your receiver is a local function, it may be
  garbage collected. To prevent this, pass `weak=False` when you call
  the signal’s `connect()` method.
- **dispatch_uid** – A unique identifier for a signal receiver in cases
  where duplicate signals may be sent. See
  [Preventing duplicate signals](#preventing-duplicate-signals) for more information.

Let’s see how this works by registering a signal that
gets called after each HTTP request is finished. We’ll be connecting to the
[request_finished](https://docs.djangoproject.com/en/ref/signals/#django.core.signals.request_finished) signal.

### Receiver functions¶

First, we need to define a receiver function. A receiver can be any Python
function or method:

```
def my_callback(sender, **kwargs):
    print("Request finished!")
```

Notice that the function takes a `sender` argument, along with wildcard
keyword arguments (`**kwargs`); all signal handlers must take these arguments.

We’ll look at senders [a bit later](#connecting-to-specific-signals), but
right now look at the `**kwargs` argument. All signals send keyword
arguments, and may change those keyword arguments at any time. In the case of
[request_finished](https://docs.djangoproject.com/en/ref/signals/#django.core.signals.request_finished), it’s documented as sending no
arguments, which means we might be tempted to write our signal handling as
`my_callback(sender)`.

This would be wrong – in fact, Django will throw an error if you do so. That’s
because at any point arguments could get added to the signal and your receiver
must be able to handle those new arguments.

Receivers may also be asynchronous functions, with the same signature but
declared using `async def`:

```
async def my_callback(sender, **kwargs):
    await asyncio.sleep(5)
    print("Request finished!")
```

Signals can be sent either synchronously or asynchronously, and receivers will
automatically be adapted to the correct call-style. See [sending signals](#sending-signals) for more information.

  Changed in Django 5.0:

Support for asynchronous receivers was added.

### Connecting receiver functions¶

There are two ways you can connect a receiver to a signal. You can take the
manual connect route:

```
from django.core.signals import request_finished

request_finished.connect(my_callback)
```

Alternatively, you can use a [receiver()](#django.dispatch.receiver) decorator:

   receiver(*signal*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/dispatch/dispatcher/#receiver)[¶](#django.dispatch.receiver)  Parameters:

- **signal** – A signal or a list of signals to connect a function to.
- **kwargs** – Wildcard keyword arguments to pass to a
  [function](#receiver-functions).

Here’s how you connect with the decorator:

```
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")
```

Now, our `my_callback` function will be called each time a request finishes.

Where should this code live?

Strictly speaking, signal handling and registration code can live anywhere
you like, although it’s recommended to avoid the application’s root module
and its `models` module to minimize side-effects of importing code.

In practice, signal handlers are usually defined in a `signals`
submodule of the application they relate to. Signal receivers are
connected in the [ready()](https://docs.djangoproject.com/en/ref/applications/#django.apps.AppConfig.ready) method of your
application [configuration class](https://docs.djangoproject.com/en/ref/applications/#configuring-applications-ref). If
you’re using the [receiver()](#django.dispatch.receiver) decorator, import the `signals`
submodule inside [ready()](https://docs.djangoproject.com/en/ref/applications/#django.apps.AppConfig.ready), this will implicitly
connect signal handlers:

```
from django.apps import AppConfig
from django.core.signals import request_finished

class MyAppConfig(AppConfig):
    ...

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals

        # Explicitly connect a signal handler.
        request_finished.connect(signals.my_callback)
```

Note

The [ready()](https://docs.djangoproject.com/en/ref/applications/#django.apps.AppConfig.ready) method may be executed more than
once during testing, so you may want to [guard your signals from
duplication](#preventing-duplicate-signals), especially if you’re planning
to send them within tests.

### Connecting to signals sent by specific senders¶

Some signals get sent many times, but you’ll only be interested in receiving a
certain subset of those signals. For example, consider the
[django.db.models.signals.pre_save](https://docs.djangoproject.com/en/ref/signals/#django.db.models.signals.pre_save) signal sent before a model gets saved.
Most of the time, you don’t need to know when *any* model gets saved – just
when one *specific* model is saved.

In these cases, you can register to receive signals sent only by particular
senders. In the case of [django.db.models.signals.pre_save](https://docs.djangoproject.com/en/ref/signals/#django.db.models.signals.pre_save), the sender
will be the model class being saved, so you can indicate that you only want
signals sent by some model:

```
from django.db.models.signals import pre_save
from django.dispatch import receiver
from myapp.models import MyModel

@receiver(pre_save, sender=MyModel)
def my_handler(sender, **kwargs): ...
```

The `my_handler` function will only be called when an instance of `MyModel`
is saved.

Different signals use different objects as their senders; you’ll need to consult
the [built-in signal documentation](https://docs.djangoproject.com/en/ref/signals/) for details of each
particular signal.

### Preventing duplicate signals¶

In some circumstances, the code connecting receivers to signals may run
multiple times. This can cause your receiver function to be registered more
than once, and thus called as many times for a signal event. For example, the
[ready()](https://docs.djangoproject.com/en/ref/applications/#django.apps.AppConfig.ready) method may be executed more than once
during testing. More generally, this occurs everywhere your project imports the
module where you define the signals, because signal registration runs as many
times as it is imported.

If this behavior is problematic (such as when using signals to
send an email whenever a model is saved), pass a unique identifier as
the `dispatch_uid` argument to identify your receiver function. This
identifier will usually be a string, although any hashable object will
suffice. The end result is that your receiver function will only be
bound to the signal once for each unique `dispatch_uid` value:

```
from django.core.signals import request_finished

request_finished.connect(my_callback, dispatch_uid="my_unique_identifier")
```

## Defining and sending signals¶

Your applications can take advantage of the signal infrastructure and provide
its own signals.

When to use custom signals

Signals are implicit function calls which make debugging harder. If the
sender and receiver of your custom signal are both within your project,
you’re better off using an explicit function call.

### Defining signals¶

   *class*Signal[[source]](https://docs.djangoproject.com/en/_modules/django/dispatch/dispatcher/#Signal)[¶](#django.dispatch.Signal)

All signals are [django.dispatch.Signal](#django.dispatch.Signal) instances.

For example:

```
import django.dispatch

pizza_done = django.dispatch.Signal()
```

This declares a `pizza_done` signal.

### Sending signals¶

There are two ways to send signals synchronously in Django.

   Signal.send(*sender*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/dispatch/dispatcher/#Signal.send)[¶](#django.dispatch.Signal.send)    Signal.send_robust(*sender*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/dispatch/dispatcher/#Signal.send_robust)[¶](#django.dispatch.Signal.send_robust)

Signals may also be sent asynchronously.

   Signal.asend(*sender*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/dispatch/dispatcher/#Signal.asend)[¶](#django.dispatch.Signal.asend)    Signal.asend_robust(*sender*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/dispatch/dispatcher/#Signal.asend_robust)[¶](#django.dispatch.Signal.asend_robust)

To send a signal, call either [Signal.send()](#django.dispatch.Signal.send), [Signal.send_robust()](#django.dispatch.Signal.send_robust),
[awaitSignal.asend()](#django.dispatch.Signal.asend), or
[awaitSignal.asend_robust()](#django.dispatch.Signal.asend_robust). You must provide the
`sender` argument (which is a class most of the time) and may provide as many
other keyword arguments as you like.

For example, here’s how sending our `pizza_done` signal might look:

```
class PizzaStore:
    ...

    def send_pizza(self, toppings, size):
        pizza_done.send(sender=self.__class__, toppings=toppings, size=size)
        ...
```

All four methods return a list of tuple pairs `[(receiver, response), ...]`,
representing the list of called receiver functions and their response values.

`send()` differs from `send_robust()` in how exceptions raised by receiver
functions are handled. `send()` does *not* catch any exceptions raised by
receivers; it simply allows errors to propagate. Thus not all receivers may
be notified of a signal in the face of an error.

`send_robust()` catches all errors derived from Python’s `Exception` class,
and ensures all receivers are notified of the signal. If an error occurs, the
error instance is returned in the tuple pair for the receiver that raised the error.

The tracebacks are present on the `__traceback__` attribute of the errors
returned when calling `send_robust()`.

`asend()` is similar to `send()`, but it is a coroutine that must be
awaited:

```
async def asend_pizza(self, toppings, size):
    await pizza_done.asend(sender=self.__class__, toppings=toppings, size=size)
    ...
```

Whether synchronous or asynchronous, receivers will be correctly adapted to
whether `send()` or `asend()` is used. Synchronous receivers will be
called using [sync_to_async()](https://docs.djangoproject.com/en/5.0/async/#asgiref.sync.sync_to_async) when invoked via `asend()`. Asynchronous
receivers will be called using [async_to_sync()](https://docs.djangoproject.com/en/5.0/async/#asgiref.sync.async_to_sync) when invoked via
`sync()`. Similar to the [case for middleware](https://docs.djangoproject.com/en/5.0/async/#async-performance),
there is a small performance cost to adapting receivers in this way. Note that
in order to reduce the number of sync/async calling-style switches within a
`send()` or `asend()` call, the receivers are grouped by whether or not
they are async before being called. This means that an asynchronous receiver
registered before a synchronous receiver may be executed after the synchronous
receiver. In addition, async receivers are executed concurrently using
`asyncio.gather()`.

All built-in signals, except those in the async request-response cycle, are
dispatched using [Signal.send()](#django.dispatch.Signal.send).

  Changed in Django 5.0:

Support for asynchronous signals was added.

## Disconnecting signals¶

   Signal.disconnect(*receiver=None*, *sender=None*, *dispatch_uid=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/dispatch/dispatcher/#Signal.disconnect)[¶](#django.dispatch.Signal.disconnect)

To disconnect a receiver from a signal, call [Signal.disconnect()](#django.dispatch.Signal.disconnect). The
arguments are as described in [Signal.connect()](#django.dispatch.Signal.connect). The method returns
`True` if a receiver was disconnected and `False` if not. When `sender`
is passed as a lazy reference to `<app label>.<model>`, this method always
returns `None`.

The `receiver` argument indicates the registered receiver to disconnect. It
may be `None` if `dispatch_uid` is used to identify the receiver.
