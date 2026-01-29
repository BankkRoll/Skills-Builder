# Multiple databases¶ and more

# Multiple databases¶

# Multiple databases¶

This topic guide describes Django’s support for interacting with
multiple databases. Most of the rest of Django’s documentation assumes
you are interacting with a single database. If you want to interact
with multiple databases, you’ll need to take some additional steps.

See also

See [Multi-database support](https://docs.djangoproject.com/en/5.0/testing/tools/#testing-multi-db) for information about testing with multiple
databases.

## Defining your databases¶

The first step to using more than one database with Django is to tell
Django about the database servers you’ll be using. This is done using
the [DATABASES](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASES) setting. This setting maps database aliases,
which are a way to refer to a specific database throughout Django, to
a dictionary of settings for that specific connection. The settings in
the inner dictionaries are described fully in the [DATABASES](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASES)
documentation.

Databases can have any alias you choose. However, the alias
`default` has special significance. Django uses the database with
the alias of `default` when no other database has been selected.

The following is an example `settings.py` snippet defining two
databases – a default PostgreSQL database and a MySQL database called
`users`:

```
DATABASES = {
    "default": {
        "NAME": "app_data",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "postgres_user",
        "PASSWORD": "s3krit",
    },
    "users": {
        "NAME": "user_data",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "priv4te",
    },
}
```

If the concept of a `default` database doesn’t make sense in the context
of your project, you need to be careful to always specify the database
that you want to use. Django requires that a `default` database entry
be defined, but the parameters dictionary can be left blank if it will not be
used. To do this, you must set up [DATABASE_ROUTERS](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASE_ROUTERS) for all of your
apps’ models, including those in any contrib and third-party apps you’re using,
so that no queries are routed to the default database. The following is an
example `settings.py` snippet defining two non-default databases, with the
`default` entry intentionally left empty:

```
DATABASES = {
    "default": {},
    "users": {
        "NAME": "user_data",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "superS3cret",
    },
    "customers": {
        "NAME": "customer_data",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_cust",
        "PASSWORD": "veryPriv@ate",
    },
}
```

If you attempt to access a database that you haven’t defined in your
[DATABASES](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASES) setting, Django will raise a
`django.utils.connection.ConnectionDoesNotExist` exception.

## Synchronizing your databases¶

The [migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate) management command operates on one database at a
time. By default, it operates on the `default` database, but by
providing the [--database](https://docs.djangoproject.com/en/ref/django-admin/#cmdoption-migrate-database) option, you can tell it
to synchronize a different database. So, to synchronize all models onto
all databases in the first example above, you would need to call:

```
$ ./manage.py migrate
$ ./manage.py migrate --database=users
```

If you don’t want every application to be synchronized onto a
particular database, you can define a [database
router](#topics-db-multi-db-routing) that implements a policy
constraining the availability of particular models.

If, as in the second example above, you’ve left the `default` database empty,
you must provide a database name each time you run [migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate). Omitting
the database name would raise an error. For the second example:

```
$ ./manage.py migrate --database=users
$ ./manage.py migrate --database=customers
```

### Using other management commands¶

Most other `django-admin` commands that interact with the database operate in
the same way as [migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate) – they only ever operate on one database at
a time, using `--database` to control the database used.

An exception to this rule is the [makemigrations](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-makemigrations) command. It
validates the migration history in the databases to catch problems with the
existing migration files (which could be caused by editing them) before
creating new migrations. By default, it checks only the `default` database,
but it consults the [allow_migrate()](#allow_migrate) method of [routers](#topics-db-multi-db-routing) if any are installed.

## Automatic database routing¶

The easiest way to use multiple databases is to set up a database
routing scheme. The default routing scheme ensures that objects remain
‘sticky’ to their original database (i.e., an object retrieved from
the `foo` database will be saved on the same database). The default
routing scheme ensures that if a database isn’t specified, all queries
fall back to the `default` database.

You don’t have to do anything to activate the default routing scheme
– it is provided ‘out of the box’ on every Django project. However,
if you want to implement more interesting database allocation
behaviors, you can define and install your own database routers.

### Database routers¶

A database Router is a class that provides up to four methods:

   db_for_read(*model*, ***hints*)[¶](#db_for_read)

Suggest the database that should be used for read operations for
objects of type `model`.

If a database operation is able to provide any additional
information that might assist in selecting a database, it will be
provided in the `hints` dictionary. Details on valid hints are
provided [below](#topics-db-multi-db-hints).

Returns `None` if there is no suggestion.

    db_for_write(*model*, ***hints*)[¶](#db_for_write)

Suggest the database that should be used for writes of objects of
type Model.

If a database operation is able to provide any additional
information that might assist in selecting a database, it will be
provided in the `hints` dictionary. Details on valid hints are
provided [below](#topics-db-multi-db-hints).

Returns `None` if there is no suggestion.

    allow_relation(*obj1*, *obj2*, ***hints*)[¶](#allow_relation)

Return `True` if a relation between `obj1` and `obj2` should be
allowed, `False` if the relation should be prevented, or `None` if
the router has no opinion. This is purely a validation operation,
used by foreign key and many to many operations to determine if a
relation should be allowed between two objects.

If no router has an opinion (i.e. all routers return `None`), only
relations within the same database are allowed.

    allow_migrate(*db*, *app_label*, *model_name=None*, ***hints*)[¶](#allow_migrate)

Determine if the migration operation is allowed to run on the database with
alias `db`. Return `True` if the operation should run, `False` if it
shouldn’t run, or `None` if the router has no opinion.

The `app_label` positional argument is the label of the application
being migrated.

`model_name` is set by most migration operations to the value of
`model._meta.model_name` (the lowercased version of the model
`__name__`) of the model being migrated. Its value is `None` for the
[RunPython](https://docs.djangoproject.com/en/ref/migration-operations/#django.db.migrations.operations.RunPython) and
[RunSQL](https://docs.djangoproject.com/en/ref/migration-operations/#django.db.migrations.operations.RunSQL) operations unless they
provide it using hints.

`hints` are used by certain operations to communicate additional
information to the router.

When `model_name` is set, `hints` normally contains the model class
under the key `'model'`. Note that it may be a [historical model](https://docs.djangoproject.com/en/5.0/migrations/#historical-models), and thus not have any custom attributes, methods, or
managers. You should only rely on `_meta`.

This method can also be used to determine the availability of a model on a
given database.

[makemigrations](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-makemigrations) always creates migrations for model changes, but
if `allow_migrate()` returns `False`, any migration operations for the
`model_name` will be silently skipped when running [migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate) on
the `db`. Changing the behavior of `allow_migrate()` for models that
already have migrations may result in broken foreign keys, extra tables,
or missing tables. When [makemigrations](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-makemigrations) verifies the migration
history, it skips databases where no app is allowed to migrate.

A router doesn’t have to provide *all* these methods – it may omit one
or more of them. If one of the methods is omitted, Django will skip
that router when performing the relevant check.

#### Hints¶

The hints received by the database router can be used to decide which
database should receive a given request.

At present, the only hint that will be provided is `instance`, an
object instance that is related to the read or write operation that is
underway. This might be the instance that is being saved, or it might
be an instance that is being added in a many-to-many relation. In some
cases, no instance hint will be provided at all. The router checks for
the existence of an instance hint, and determine if that hint should be
used to alter routing behavior.

### Using routers¶

Database routers are installed using the [DATABASE_ROUTERS](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASE_ROUTERS)
setting. This setting defines a list of class names, each specifying a
router that should be used by the base router
(`django.db.router`).

The base router is used by Django’s database operations to allocate
database usage. Whenever a query needs to know which database to use,
it calls the base router, providing a model and a hint (if
available). The base router tries each router class in turn until one returns
a database suggestion. If no routers return a suggestion, the base router tries
the current [instance._state.db](https://docs.djangoproject.com/en/ref/models/instances/#django.db.models.Model._state) of the hint instance. If no hint instance
was provided, or [instance._state.db](https://docs.djangoproject.com/en/ref/models/instances/#django.db.models.Model._state) is
`None`, the base router will allocate the `default` database.

### An example¶

Example purposes only!

This example is intended as a demonstration of how the router
infrastructure can be used to alter database usage. It
intentionally ignores some complex issues in order to
demonstrate how routers are used.

This example won’t work if any of the models in `myapp` contain
relationships to models outside of the `other` database.
[Cross-database relationships](#no-cross-database-relations)
introduce referential integrity problems that Django can’t
currently handle.

The primary/replica (referred to as master/slave by some databases)
configuration described is also flawed – it
doesn’t provide any solution for handling replication lag (i.e.,
query inconsistencies introduced because of the time taken for a
write to propagate to the replicas). It also doesn’t consider the
interaction of transactions with the database utilization strategy.

So - what does this mean in practice? Let’s consider another sample
configuration. This one will have several databases: one for the
`auth` application, and all other apps using a primary/replica setup
with two read replicas. Here are the settings specifying these
databases:

```
DATABASES = {
    "default": {},
    "auth_db": {
        "NAME": "auth_db_name",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "swordfish",
    },
    "primary": {
        "NAME": "primary_name",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "spam",
    },
    "replica1": {
        "NAME": "replica1_name",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "eggs",
    },
    "replica2": {
        "NAME": "replica2_name",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "bacon",
    },
}
```

Now we’ll need to handle routing. First we want a router that knows to
send queries for the `auth` and `contenttypes` apps to `auth_db`
(`auth` models are linked to `ContentType`, so they must be stored in the
same database):

```
class AuthRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    route_app_labels = {"auth", "contenttypes"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "auth_db"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "auth_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            return db == "auth_db"
        return None
```

And we also want a router that sends all other apps to the
primary/replica configuration, and randomly chooses a replica to read
from:

```
import random

class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return random.choice(["replica1", "replica2"])

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return "primary"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {"primary", "replica1", "replica2"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
```

Finally, in the settings file, we add the following (substituting
`path.to.` with the actual Python path to the module(s) where the
routers are defined):

```
DATABASE_ROUTERS = ["path.to.AuthRouter", "path.to.PrimaryReplicaRouter"]
```

The order in which routers are processed is significant. Routers will
be queried in the order they are listed in the
[DATABASE_ROUTERS](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASE_ROUTERS) setting. In this example, the
`AuthRouter` is processed before the `PrimaryReplicaRouter`, and as a
result, decisions concerning the models in `auth` are processed
before any other decision is made. If the [DATABASE_ROUTERS](https://docs.djangoproject.com/en/ref/settings/#std-setting-DATABASE_ROUTERS)
setting listed the two routers in the other order,
`PrimaryReplicaRouter.allow_migrate()` would be processed first. The
catch-all nature of the PrimaryReplicaRouter implementation would mean
that all models would be available on all databases.

With this setup installed, and all databases migrated as per
[Synchronizing your databases](#synchronizing-multiple-databases), lets run some Django code:

```
>>> # This retrieval will be performed on the 'auth_db' database
>>> fred = User.objects.get(username="fred")
>>> fred.first_name = "Frederick"

>>> # This save will also be directed to 'auth_db'
>>> fred.save()

>>> # These retrieval will be randomly allocated to a replica database
>>> dna = Person.objects.get(name="Douglas Adams")

>>> # A new object has no database allocation when created
>>> mh = Book(title="Mostly Harmless")

>>> # This assignment will consult the router, and set mh onto
>>> # the same database as the author object
>>> mh.author = dna

>>> # This save will force the 'mh' instance onto the primary database...
>>> mh.save()

>>> # ... but if we re-retrieve the object, it will come back on a replica
>>> mh = Book.objects.get(title="Mostly Harmless")
```

This example defined a router to handle interaction with models from the
`auth` app, and other routers to handle interaction with all other apps. If
you left your `default` database empty and don’t want to define a catch-all
database router to handle all apps not otherwise specified, your routers must
handle the names of all apps in [INSTALLED_APPS](https://docs.djangoproject.com/en/ref/settings/#std-setting-INSTALLED_APPS) before you migrate.
See [Behavior of contrib apps](#contrib-app-multiple-databases) for information about contrib apps
that must be together in one database.

## Manually selecting a database¶

Django also provides an API that allows you to maintain complete control
over database usage in your code. A manually specified database allocation
will take priority over a database allocated by a router.

### Manually selecting a database for aQuerySet¶

You can select the database for a `QuerySet` at any point in the
`QuerySet` “chain.” Call `using()` on the `QuerySet` to get another
`QuerySet` that uses the specified database.

`using()` takes a single argument: the alias of the database on
which you want to run the query. For example:

```
>>> # This will run on the 'default' database.
>>> Author.objects.all()

>>> # So will this.
>>> Author.objects.using("default")

>>> # This will run on the 'other' database.
>>> Author.objects.using("other")
```

### Selecting a database forsave()¶

Use the `using` keyword to `Model.save()` to specify to which
database the data should be saved.

For example, to save an object to the `legacy_users` database, you’d
use this:

```
>>> my_object.save(using="legacy_users")
```

If you don’t specify `using`, the `save()` method will save into
the default database allocated by the routers.

#### Moving an object from one database to another¶

If you’ve saved an instance to one database, it might be tempting to
use `save(using=...)` as a way to migrate the instance to a new
database. However, if you don’t take appropriate steps, this could
have some unexpected consequences.

Consider the following example:

```
>>> p = Person(name="Fred")
>>> p.save(using="first")  # (statement 1)
>>> p.save(using="second")  # (statement 2)
```

In statement 1, a new `Person` object is saved to the `first`
database. At this time, `p` doesn’t have a primary key, so Django
issues an SQL `INSERT` statement. This creates a primary key, and
Django assigns that primary key to `p`.

When the save occurs in statement 2, `p` already has a primary key
value, and Django will attempt to use that primary key on the new
database. If the primary key value isn’t in use in the `second`
database, then you won’t have any problems – the object will be
copied to the new database.

However, if the primary key of `p` is already in use on the
`second` database, the existing object in the `second` database
will be overridden when `p` is saved.

You can avoid this in two ways. First, you can clear the primary key
of the instance. If an object has no primary key, Django will treat it
as a new object, avoiding any loss of data on the `second`
database:

```
>>> p = Person(name="Fred")
>>> p.save(using="first")
>>> p.pk = None  # Clear the primary key.
>>> p.save(using="second")  # Write a completely new object.
```

The second option is to use the `force_insert` option to `save()`
to ensure that Django does an SQL `INSERT`:

```
>>> p = Person(name="Fred")
>>> p.save(using="first")
>>> p.save(using="second", force_insert=True)
```

This will ensure that the person named `Fred` will have the same
primary key on both databases. If that primary key is already in use
when you try to save onto the `second` database, an error will be
raised.

### Selecting a database to delete from¶

By default, a call to delete an existing object will be executed on
the same database that was used to retrieve the object in the first
place:

```
>>> u = User.objects.using("legacy_users").get(username="fred")
>>> u.delete()  # will delete from the `legacy_users` database
```

To specify the database from which a model will be deleted, pass a
`using` keyword argument to the `Model.delete()` method. This
argument works just like the `using` keyword argument to `save()`.

For example, if you’re migrating a user from the `legacy_users`
database to the `new_users` database, you might use these commands:

```
>>> user_obj.save(using="new_users")
>>> user_obj.delete(using="legacy_users")
```

### Using managers with multiple databases¶

Use the `db_manager()` method on managers to give managers access to
a non-default database.

For example, say you have a custom manager method that touches the
database – `User.objects.create_user()`. Because `create_user()`
is a manager method, not a `QuerySet` method, you can’t do
`User.objects.using('new_users').create_user()`. (The
`create_user()` method is only available on `User.objects`, the
manager, not on `QuerySet` objects derived from the manager.) The
solution is to use `db_manager()`, like this:

```
User.objects.db_manager("new_users").create_user(...)
```

`db_manager()` returns a copy of the manager bound to the database you specify.

#### Usingget_queryset()with multiple databases¶

If you’re overriding `get_queryset()` on your manager, be sure to
either call the method on the parent (using `super()`) or do the
appropriate handling of the `_db` attribute on the manager (a string
containing the name of the database to use).

For example, if you want to return a custom `QuerySet` class from
the `get_queryset` method, you could do this:

```
class MyManager(models.Manager):
    def get_queryset(self):
        qs = CustomQuerySet(self.model)
        if self._db is not None:
            qs = qs.using(self._db)
        return qs
```

## Exposing multiple databases in Django’s admin interface¶

Django’s admin doesn’t have any explicit support for multiple
databases. If you want to provide an admin interface for a model on a
database other than that specified by your router chain, you’ll
need to write custom [ModelAdmin](https://docs.djangoproject.com/en/ref/contrib/admin/#django.contrib.admin.ModelAdmin) classes
that will direct the admin to use a specific database for content.

`ModelAdmin` objects have the following methods that require customization
for multiple-database support:

```
class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = "other"

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )
```

The implementation provided here implements a multi-database strategy
where all objects of a given type are stored on a specific database
(e.g., all `User` objects are in the `other` database). If your
usage of multiple databases is more complex, your `ModelAdmin` will
need to reflect that strategy.

[InlineModelAdmin](https://docs.djangoproject.com/en/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin) objects can be handled in a
similar fashion. They require three customized methods:

```
class MultiDBTabularInline(admin.TabularInline):
    using = "other"

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )
```

Once you’ve written your model admin definitions, they can be
registered with any `Admin` instance:

```
from django.contrib import admin

# Specialize the multi-db admin objects for use with specific models.
class BookInline(MultiDBTabularInline):
    model = Book

class PublisherAdmin(MultiDBModelAdmin):
    inlines = [BookInline]

admin.site.register(Author, MultiDBModelAdmin)
admin.site.register(Publisher, PublisherAdmin)

othersite = admin.AdminSite("othersite")
othersite.register(Publisher, MultiDBModelAdmin)
```

This example sets up two admin sites. On the first site, the
`Author` and `Publisher` objects are exposed; `Publisher`
objects have a tabular inline showing books published by that
publisher. The second site exposes just publishers, without the
inlines.

## Using raw cursors with multiple databases¶

If you are using more than one database you can use
`django.db.connections` to obtain the connection (and cursor) for a
specific database. `django.db.connections` is a dictionary-like
object that allows you to retrieve a specific connection using its
alias:

```
from django.db import connections

with connections["my_db_alias"].cursor() as cursor:
    ...
```

## Limitations of multiple databases¶

### Cross-database relations¶

Django doesn’t currently provide any support for foreign key or
many-to-many relationships spanning multiple databases. If you
have used a router to partition models to different databases,
any foreign key and many-to-many relationships defined by those
models must be internal to a single database.

This is because of referential integrity. In order to maintain a
relationship between two objects, Django needs to know that the
primary key of the related object is valid. If the primary key is
stored on a separate database, it’s not possible to easily evaluate
the validity of a primary key.

If you’re using Postgres, SQLite, Oracle, or MySQL with InnoDB, this is
enforced at the database integrity level – database level key
constraints prevent the creation of relations that can’t be validated.

However, if you’re using MySQL with MyISAM tables, there is no enforced
referential integrity; as a result, you may be able to ‘fake’ cross database
foreign keys. However, this configuration is not officially supported by
Django.

### Behavior of contrib apps¶

Several contrib apps include models, and some apps depend on others. Since
cross-database relationships are impossible, this creates some restrictions on
how you can split these models across databases:

- each one of `contenttypes.ContentType`, `sessions.Session` and
  `sites.Site` can be stored in any database, given a suitable router.
- `auth` models — `User`, `Group` and `Permission` — are linked
  together and linked to `ContentType`, so they must be stored in the same
  database as `ContentType`.
- `admin` depends on `auth`, so its models must be in the same database
  as `auth`.
- `flatpages` and `redirects` depend on `sites`, so their models must be
  in the same database as `sites`.

In addition, some objects are automatically created just after
[migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate) creates a table to hold them in a database:

- a default `Site`,
- a `ContentType` for each model (including those not stored in that
  database),
- the `Permission`s for each model (including those not stored in that
  database).

For common setups with multiple databases, it isn’t useful to have these
objects in more than one database. Common setups include primary/replica and
connecting to external databases. Therefore, it’s recommended to write a
[database router](#topics-db-multi-db-routing) that allows synchronizing
these three models to only one database. Use the same approach for contrib
and third-party apps that don’t need their tables in multiple databases.

Warning

If you’re synchronizing content types to more than one database, be aware
that their primary keys may not match across databases. This may result in
data corruption or data loss.

---

# Database access optimization¶

# Database access optimization¶

Django’s database layer provides various ways to help developers get the most
out of their databases. This document gathers together links to the relevant
documentation, and adds various tips, organized under a number of headings that
outline the steps to take when attempting to optimize your database usage.

## Profile first¶

As general programming practice, this goes without saying. Find out [what
queries you are doing and what they are costing you](https://docs.djangoproject.com/en/faq/models/#faq-see-raw-sql-queries).
Use [QuerySet.explain()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.explain) to understand how specific `QuerySet`s are
executed by your database. You may also want to use an external project like
[django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar/), or a tool that monitors your database directly.

Remember that you may be optimizing for speed or memory or both, depending on
your requirements. Sometimes optimizing for one will be detrimental to the
other, but sometimes they will help each other. Also, work that is done by the
database process might not have the same cost (to you) as the same amount of
work done in your Python process. It is up to you to decide what your
priorities are, where the balance must lie, and profile all of these as required
since this will depend on your application and server.

With everything that follows, remember to profile after every change to ensure
that the change is a benefit, and a big enough benefit given the decrease in
readability of your code. **All** of the suggestions below come with the caveat
that in your circumstances the general principle might not apply, or might even
be reversed.

## Use standard DB optimization techniques¶

…including:

- [Indexes](https://en.wikipedia.org/wiki/Database_index). This is a number one priority, *after* you have determined from
  profiling what indexes should be added. Use
  [Meta.indexes](https://docs.djangoproject.com/en/ref/models/options/#django.db.models.Options.indexes) or
  [Field.db_index](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.Field.db_index) to add these from
  Django. Consider adding indexes to fields that you frequently query using
  [filter()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.filter),
  [exclude()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.exclude),
  [order_by()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.order_by), etc. as indexes may help
  to speed up lookups. Note that determining the best indexes is a complex
  database-dependent topic that will depend on your particular application.
  The overhead of maintaining an index may outweigh any gains in query speed.

- Appropriate use of field types.

We will assume you have done the things listed above. The rest of this document
focuses on how to use Django in such a way that you are not doing unnecessary
work. This document also does not address other optimization techniques that
apply to all expensive operations, such as [general purpose caching](https://docs.djangoproject.com/en/5.0/cache/).

## UnderstandQuerySets¶

Understanding [QuerySets](https://docs.djangoproject.com/en/ref/models/querysets/) is vital to getting good
performance with simple code. In particular:

### UnderstandQuerySetevaluation¶

To avoid performance problems, it is important to understand:

- that [QuerySets are lazy](https://docs.djangoproject.com/en/5.0/topics/queries/#querysets-are-lazy).
- when [they are evaluated](https://docs.djangoproject.com/en/ref/models/querysets/#when-querysets-are-evaluated).
- how [the data is held in memory](https://docs.djangoproject.com/en/5.0/topics/queries/#caching-and-querysets).

### Understand cached attributes¶

As well as caching of the whole `QuerySet`, there is caching of the result of
attributes on ORM objects. In general, attributes that are not callable will be
cached. For example, assuming the [example blog models](https://docs.djangoproject.com/en/5.0/topics/queries/#queryset-model-example):

```
>>> entry = Entry.objects.get(id=1)
>>> entry.blog  # Blog object is retrieved at this point
>>> entry.blog  # cached version, no DB access
```

But in general, callable attributes cause DB lookups every time:

```
>>> entry = Entry.objects.get(id=1)
>>> entry.authors.all()  # query performed
>>> entry.authors.all()  # query performed again
```

Be careful when reading template code - the template system does not allow use
of parentheses, but will call callables automatically, hiding the above
distinction.

Be careful with your own custom properties - it is up to you to implement
caching when required, for example using the
[cached_property](https://docs.djangoproject.com/en/ref/utils/#django.utils.functional.cached_property) decorator.

### Use thewithtemplate tag¶

To make use of the caching behavior of `QuerySet`, you may need to use the
[with](https://docs.djangoproject.com/en/ref/templates/builtins/#std-templatetag-with) template tag.

### Useiterator()¶

When you have a lot of objects, the caching behavior of the `QuerySet` can
cause a large amount of memory to be used. In this case,
[iterator()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.iterator) may help.

### Useexplain()¶

[QuerySet.explain()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.explain) gives you detailed information about how the database
executes a query, including indexes and joins that are used. These details may
help you find queries that could be rewritten more efficiently, or identify
indexes that could be added to improve performance.

## Do database work in the database rather than in Python¶

For instance:

- At the most basic level, use [filter and exclude](https://docs.djangoproject.com/en/ref/models/querysets/#queryset-api) to do
  filtering in the database.
- Use [Fexpressions](https://docs.djangoproject.com/en/ref/models/expressions/#django.db.models.F) to filter
  based on other fields within the same model.
- Use [annotate to do aggregation in the database](https://docs.djangoproject.com/en/5.0/topics/aggregation/).

If these aren’t enough to generate the SQL you need:

### UseRawSQL¶

A less portable but more powerful method is the
[RawSQL](https://docs.djangoproject.com/en/ref/models/expressions/#django.db.models.expressions.RawSQL) expression, which allows some SQL
to be explicitly added to the query. If that still isn’t powerful enough:

### Use raw SQL¶

Write your own [custom SQL to retrieve data or populate models](https://docs.djangoproject.com/en/5.0/topics/sql/). Use `django.db.connection.queries` to find out what Django
is writing for you and start from there.

## Retrieve individual objects using a unique, indexed column¶

There are two reasons to use a column with
[unique](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.Field.unique) or
[db_index](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.Field.db_index) when using
[get()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.get) to retrieve individual objects.
First, the query will be quicker because of the underlying database index.
Also, the query could run much slower if multiple objects match the lookup;
having a unique constraint on the column guarantees this will never happen.

So using the [example blog models](https://docs.djangoproject.com/en/5.0/topics/queries/#queryset-model-example):

```
>>> entry = Entry.objects.get(id=10)
```

will be quicker than:

```
>>> entry = Entry.objects.get(headline="News Item Title")
```

because `id` is indexed by the database and is guaranteed to be unique.

Doing the following is potentially quite slow:

```
>>> entry = Entry.objects.get(headline__startswith="News")
```

First of all, `headline` is not indexed, which will make the underlying
database fetch slower.

Second, the lookup doesn’t guarantee that only one object will be returned.
If the query matches more than one object, it will retrieve and transfer all of
them from the database. This penalty could be substantial if hundreds or
thousands of records are returned. The penalty will be compounded if the
database lives on a separate server, where network overhead and latency also
play a factor.

## Retrieve everything at once if you know you will need it¶

Hitting the database multiple times for different parts of a single ‘set’ of
data that you will need all parts of is, in general, less efficient than
retrieving it all in one query. This is particularly important if you have a
query that is executed in a loop, and could therefore end up doing many database
queries, when only one was needed. So:

### UseQuerySet.select_related()andprefetch_related()¶

Understand [select_related()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.select_related) and
[prefetch_related()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related) thoroughly, and use
them:

- in [managers and default managers](https://docs.djangoproject.com/en/5.0/topics/managers/) where
  appropriate. Be aware when your manager is and is not used; sometimes this is
  tricky so don’t make assumptions.
- in view code or other layers, possibly making use of
  [prefetch_related_objects()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.prefetch_related_objects) where needed.

## Don’t retrieve things you don’t need¶

### UseQuerySet.values()andvalues_list()¶

When you only want a `dict` or `list` of values, and don’t need ORM model
objects, make appropriate usage of
[values()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.values).
These can be useful for replacing model objects in template code - as long as
the dicts you supply have the same attributes as those used in the template,
you are fine.

### UseQuerySet.defer()andonly()¶

Use [defer()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.defer) and
[only()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.only) if there are database columns
you know that you won’t need (or won’t need in most cases) to avoid loading
them. Note that if you *do* use them, the ORM will have to go and get them in
a separate query, making this a pessimization if you use it inappropriately.

Don’t be too aggressive in deferring fields without profiling as the database
has to read most of the non-text, non-`VARCHAR` data from the disk for a
single row in the results, even if it ends up only using a few columns. The
`defer()` and `only()` methods are most useful when you can avoid loading a
lot of text data or for fields that might take a lot of processing to convert
back to Python. As always, profile first, then optimize.

### UseQuerySet.contains(obj)¶

…if you only want to find out if `obj` is in the queryset, rather than
`if obj in queryset`.

### UseQuerySet.count()¶

…if you only want the count, rather than doing `len(queryset)`.

### UseQuerySet.exists()¶

…if you only want to find out if at least one result exists, rather than `if
queryset`.

But:

### Don’t overusecontains(),count(), andexists()¶

If you are going to need other data from the QuerySet, evaluate it immediately.

For example, assuming a `Group` model that has a many-to-many relation to
`User`, the following code is optimal:

```
members = group.members.all()

if display_group_members:
    if members:
        if current_user in members:
            print("You and", len(members) - 1, "other users are members of this group.")
        else:
            print("There are", len(members), "members in this group.")

        for member in members:
            print(member.username)
    else:
        print("There are no members in this group.")
```

It is optimal because:

1. Since QuerySets are lazy, this does no database queries if
  `display_group_members` is `False`.
2. Storing `group.members.all()` in the `members` variable allows its
  result cache to be reused.
3. The line `if members:` causes `QuerySet.__bool__()` to be called, which
  causes the `group.members.all()` query to be run on the database. If there
  aren’t any results, it will return `False`, otherwise `True`.
4. The line `if current_user in members:` checks if the user is in the result
  cache, so no additional database queries are issued.
5. The use of `len(members)` calls `QuerySet.__len__()`, reusing the result
  cache, so again, no database queries are issued.
6. The `for member` loop iterates over the result cache.

In total, this code does either one or zero database queries. The only
deliberate optimization performed is using the `members` variable. Using
`QuerySet.exists()` for the `if`, `QuerySet.contains()` for the `in`,
or `QuerySet.count()` for the count would each cause additional queries.

### UseQuerySet.update()anddelete()¶

Rather than retrieve a load of objects, set some values, and save them
individual, use a bulk SQL UPDATE statement, via [QuerySet.update()](https://docs.djangoproject.com/en/5.0/topics/queries/#topics-db-queries-update). Similarly, do [bulk deletes](https://docs.djangoproject.com/en/5.0/topics/queries/#topics-db-queries-delete) where possible.

Note, however, that these bulk update methods cannot call the `save()` or
`delete()` methods of individual instances, which means that any custom
behavior you have added for these methods will not be executed, including
anything driven from the normal database object [signals](https://docs.djangoproject.com/en/ref/signals/).

### Use foreign key values directly¶

If you only need a foreign key value, use the foreign key value that is already on
the object you’ve got, rather than getting the whole related object and taking
its primary key. i.e. do:

```
entry.blog_id
```

instead of:

```
entry.blog.id
```

### Don’t order results if you don’t care¶

Ordering is not free; each field to order by is an operation the database must
perform. If a model has a default ordering ([Meta.ordering](https://docs.djangoproject.com/en/ref/models/options/#django.db.models.Options.ordering)) and you don’t need it, remove
it on a `QuerySet` by calling
[order_by()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.order_by) with no parameters.

Adding an index to your database may help to improve ordering performance.

## Use bulk methods¶

Use bulk methods to reduce the number of SQL statements.

### Create in bulk¶

When creating objects, where possible, use the
[bulk_create()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create) method to reduce the
number of SQL queries. For example:

```
Entry.objects.bulk_create(
    [
        Entry(headline="This is a test"),
        Entry(headline="This is only a test"),
    ]
)
```

…is preferable to:

```
Entry.objects.create(headline="This is a test")
Entry.objects.create(headline="This is only a test")
```

Note that there are a number of [caveatstothismethod](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create), so make sure it’s appropriate
for your use case.

### Update in bulk¶

When updating objects, where possible, use the
[bulk_update()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.bulk_update) method to reduce the
number of SQL queries. Given a list or queryset of objects:

```
entries = Entry.objects.bulk_create(
    [
        Entry(headline="This is a test"),
        Entry(headline="This is only a test"),
    ]
)
```

The following example:

```
entries[0].headline = "This is not a test"
entries[1].headline = "This is no longer a test"
Entry.objects.bulk_update(entries, ["headline"])
```

…is preferable to:

```
entries[0].headline = "This is not a test"
entries[0].save()
entries[1].headline = "This is no longer a test"
entries[1].save()
```

Note that there are a number of [caveatstothismethod](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.bulk_update), so make sure it’s appropriate
for your use case.

### Insert in bulk¶

When inserting objects into [ManyToManyFields](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.ManyToManyField), use
[add()](https://docs.djangoproject.com/en/ref/models/relations/#django.db.models.fields.related.RelatedManager.add) with multiple
objects to reduce the number of SQL queries. For example:

```
my_band.members.add(me, my_friend)
```

…is preferable to:

```
my_band.members.add(me)
my_band.members.add(my_friend)
```

…where `Bands` and `Artists` have a many-to-many relationship.

When inserting different pairs of objects into
[ManyToManyField](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.ManyToManyField) or when the custom
[through](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.ManyToManyField.through) table is defined, use
[bulk_create()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create) method to reduce the
number of SQL queries. For example:

```
PizzaToppingRelationship = Pizza.toppings.through
PizzaToppingRelationship.objects.bulk_create(
    [
        PizzaToppingRelationship(pizza=my_pizza, topping=pepperoni),
        PizzaToppingRelationship(pizza=your_pizza, topping=pepperoni),
        PizzaToppingRelationship(pizza=your_pizza, topping=mushroom),
    ],
    ignore_conflicts=True,
)
```

…is preferable to:

```
my_pizza.toppings.add(pepperoni)
your_pizza.toppings.add(pepperoni, mushroom)
```

…where `Pizza` and `Topping` have a many-to-many relationship. Note that
there are a number of [caveatstothismethod](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create), so make sure it’s appropriate
for your use case.

### Remove in bulk¶

When removing objects from [ManyToManyFields](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.ManyToManyField), use
[remove()](https://docs.djangoproject.com/en/ref/models/relations/#django.db.models.fields.related.RelatedManager.remove) with multiple
objects to reduce the number of SQL queries. For example:

```
my_band.members.remove(me, my_friend)
```

…is preferable to:

```
my_band.members.remove(me)
my_band.members.remove(my_friend)
```

…where `Bands` and `Artists` have a many-to-many relationship.

When removing different pairs of objects from [ManyToManyFields](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.ManyToManyField), use
[delete()](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.query.QuerySet.delete) on a
[Q](https://docs.djangoproject.com/en/ref/models/querysets/#django.db.models.Q) expression with multiple
[through](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.ManyToManyField.through)  model instances to reduce
the number of SQL queries. For example:

```
from django.db.models import Q

PizzaToppingRelationship = Pizza.toppings.through
PizzaToppingRelationship.objects.filter(
    Q(pizza=my_pizza, topping=pepperoni)
    | Q(pizza=your_pizza, topping=pepperoni)
    | Q(pizza=your_pizza, topping=mushroom)
).delete()
```

…is preferable to:

```
my_pizza.toppings.remove(pepperoni)
your_pizza.toppings.remove(pepperoni, mushroom)
```

…where `Pizza` and `Topping` have a many-to-many relationship.
