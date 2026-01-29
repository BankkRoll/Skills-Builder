# Lookup API reference¶ and more

# Lookup API reference¶

# Lookup API reference¶

This document has the API references of lookups, the Django API for building
the `WHERE` clause of a database query. To learn how to *use* lookups, see
[Making queries](https://docs.djangoproject.com/en/topics/db/queries/); to learn how to *create* new lookups, see
[How to write custom lookups](https://docs.djangoproject.com/en/howto/custom-lookups/).

The lookup API has two components: a [RegisterLookupMixin](#django.db.models.lookups.RegisterLookupMixin) class
that registers lookups, and the [Query Expression API](#query-expression), a
set of methods that a class has to implement to be registrable as a lookup.

Django has two base classes that follow the query expression API and from where
all Django builtin lookups are derived:

- [Lookup](#django.db.models.Lookup): to lookup a field (e.g. the `exact` of `field_name__exact`)
- [Transform](#django.db.models.Transform): to transform a field

A lookup expression consists of three parts:

- Fields part (e.g. `Book.objects.filter(author__best_friends__first_name...`);
- Transforms part (may be omitted) (e.g. `__lower__first3chars__reversed`);
- A lookup (e.g. `__icontains`) that, if omitted, defaults to `__exact`.

## Registration API¶

Django uses [RegisterLookupMixin](#django.db.models.lookups.RegisterLookupMixin) to give a class the interface to
register lookups on itself or its instances. The two prominent examples are
[Field](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field), the base class of all model fields, and
[Transform](#django.db.models.Transform), the base class of all Django transforms.

   *class*lookups.RegisterLookupMixin[¶](#django.db.models.lookups.RegisterLookupMixin)

A mixin that implements the lookup API on a class.

   *classmethod*register_lookup(*lookup*, *lookup_name=None*)[¶](#django.db.models.lookups.RegisterLookupMixin.register_lookup)

Registers a new lookup in the class or class instance. For example:

```
DateField.register_lookup(YearExact)
User._meta.get_field("date_joined").register_lookup(MonthExact)
```

will register `YearExact` lookup on `DateField` and `MonthExact`
lookup on the `User.date_joined` (you can use [Field Access API](https://docs.djangoproject.com/en/5.0/ref/meta/#model-meta-field-api) to retrieve a single field instance). It
overrides a lookup that already exists with the same name. Lookups
registered on field instances take precedence over the lookups
registered on classes. `lookup_name` will be used for this lookup if
provided, otherwise `lookup.lookup_name` will be used.

    get_lookup(*lookup_name*)[¶](#django.db.models.lookups.RegisterLookupMixin.get_lookup)

Returns the [Lookup](#django.db.models.Lookup) named `lookup_name` registered in the
class or class instance depending on what calls it. The default
implementation looks recursively on all parent classes and checks if
any has a registered lookup named `lookup_name`, returning the first
match. Instance lookups would override any class lookups with the same
`lookup_name`.

    get_lookups()[¶](#django.db.models.lookups.RegisterLookupMixin.get_lookups)

Returns a dictionary of each lookup name registered in the class or
class instance mapped to the [Lookup](#django.db.models.Lookup) class.

    get_transform(*transform_name*)[¶](#django.db.models.lookups.RegisterLookupMixin.get_transform)

Returns a [Transform](#django.db.models.Transform) named `transform_name` registered in the
class or class instance. The default implementation looks recursively
on all parent classes to check if any has the registered transform
named `transform_name`, returning the first match.

For a class to be a lookup, it must follow the [Query Expression API](#query-expression). [Lookup](#django.db.models.Lookup) and [Transform](#django.db.models.Transform) naturally
follow this API.

  Changed in Django 4.2:

Support for registering lookups on [Field](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field)
instances was added.

## The Query Expression API¶

The query expression API is a common set of methods that classes define to be
usable in query expressions to translate themselves into SQL expressions. Direct
field references, aggregates, and `Transform` are examples that follow this
API. A class is said to follow the query expression API when it implements the
following methods:

   as_sql(*compiler*, *connection*)[¶](#django.db.models.as_sql)

Generates the SQL fragment for the expression. Returns a tuple
`(sql, params)`, where `sql` is the SQL string, and `params` is the
list or tuple of query parameters. The `compiler` is an `SQLCompiler`
object, which has a `compile()` method that can be used to compile other
expressions. The `connection` is the connection used to execute the
query.

Calling `expression.as_sql()` is usually incorrect - instead
`compiler.compile(expression)` should be used. The `compiler.compile()`
method will take care of calling vendor-specific methods of the expression.

Custom keyword arguments may be defined on this method if it’s likely that
`as_vendorname()` methods or subclasses will need to supply data to
override the generation of the SQL string. See [Func.as_sql()](https://docs.djangoproject.com/en/5.0/ref/expressions/#django.db.models.Func.as_sql) for
example usage.

    as_vendorname(*compiler*, *connection*)[¶](#django.db.models.as_vendorname)

Works like `as_sql()` method. When an expression is compiled by
`compiler.compile()`, Django will first try to call `as_vendorname()`,
where `vendorname` is the vendor name of the backend used for executing
the query. The `vendorname` is one of `postgresql`, `oracle`,
`sqlite`, or `mysql` for Django’s built-in backends.

    get_lookup(*lookup_name*)[¶](#django.db.models.get_lookup)

Must return the lookup named `lookup_name`. For instance, by returning
`self.output_field.get_lookup(lookup_name)`.

    get_transform(*transform_name*)[¶](#django.db.models.get_transform)

Must return the lookup named `transform_name`. For instance, by returning
`self.output_field.get_transform(transform_name)`.

    output_field[¶](#django.db.models.output_field)

Defines the type of class returned by the `get_lookup()` method. It must
be a [Field](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field) instance.

## Transformreference¶

   *class*Transform[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/lookups/#Transform)[¶](#django.db.models.Transform)

A `Transform` is a generic class to implement field transformations. A
prominent example is `__year` that transforms a `DateField` into a
`IntegerField`.

The notation to use a `Transform` in a lookup expression is
`<expression>__<transformation>` (e.g. `date__year`).

This class follows the [Query Expression API](#query-expression), which
implies that you can use `<expression>__<transform1>__<transform2>`. It’s
a specialized [Func() expression](https://docs.djangoproject.com/en/5.0/ref/expressions/#func-expressions) that only accepts
one argument.  It can also be used on the right hand side of a filter or
directly as an annotation.

   bilateral[¶](#django.db.models.Transform.bilateral)

A boolean indicating whether this transformation should apply to both
`lhs` and `rhs`. Bilateral transformations will be applied to `rhs` in
the same order as they appear in the lookup expression. By default it is set
to `False`. For example usage, see [How to write custom lookups](https://docs.djangoproject.com/en/howto/custom-lookups/).

    lhs[¶](#django.db.models.Transform.lhs)

The left-hand side - what is being transformed. It must follow the
[Query Expression API](#query-expression).

    lookup_name[¶](#django.db.models.Transform.lookup_name)

The name of the lookup, used for identifying it on parsing query
expressions. It cannot contain the string `"__"`.

    output_field[¶](#django.db.models.Transform.output_field)

Defines the class this transformation outputs. It must be a
[Field](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field) instance. By default is the same as
its `lhs.output_field`.

## Lookupreference¶

   *class*Lookup[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/lookups/#Lookup)[¶](#django.db.models.Lookup)

A `Lookup` is a generic class to implement lookups. A lookup is a query
expression with a left-hand side, [lhs](#django.db.models.Lookup.lhs); a right-hand side,
[rhs](#django.db.models.Lookup.rhs); and a `lookup_name` that is used to produce a boolean
comparison between `lhs` and `rhs` such as `lhs in rhs` or
`lhs > rhs`.

The primary notation to use a lookup in an expression is
`<lhs>__<lookup_name>=<rhs>`. Lookups can also be used directly in
`QuerySet` filters:

```
Book.objects.filter(LessThan(F("word_count"), 7500))
```

…or annotations:

```
Book.objects.annotate(is_short_story=LessThan(F("word_count"), 7500))
```

    lhs[¶](#django.db.models.Lookup.lhs)

The left-hand side - what is being looked up. The object typically
follows the [Query Expression API](#query-expression). It may also
be a plain value.

    rhs[¶](#django.db.models.Lookup.rhs)

The right-hand side - what `lhs` is being compared against. It can be
a plain value, or something that compiles into SQL, typically an
`F()` object or a `QuerySet`.

    lookup_name[¶](#django.db.models.Lookup.lookup_name)

The name of this lookup, used to identify it on parsing query
expressions. It cannot contain the string `"__"`.

    prepare_rhs[¶](#django.db.models.Lookup.prepare_rhs)

Defaults to `True`. When [rhs](#django.db.models.Lookup.rhs) is a plain value,
[prepare_rhs](#django.db.models.Lookup.prepare_rhs) determines whether it should be prepared for use as
a parameter in a query. In order to do so,
`lhs.output_field.get_prep_value()` is called if defined, or `rhs`
is wrapped in [Value()](https://docs.djangoproject.com/en/5.0/ref/expressions/#django.db.models.Value) otherwise.

    process_lhs(*compiler*, *connection*, *lhs=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/lookups/#Lookup.process_lhs)[¶](#django.db.models.Lookup.process_lhs)

Returns a tuple `(lhs_string, lhs_params)`, as returned by
`compiler.compile(lhs)`. This method can be overridden to tune how
the `lhs` is processed.

`compiler` is an `SQLCompiler` object, to be used like
`compiler.compile(lhs)` for compiling `lhs`. The `connection`
can be used for compiling vendor specific SQL. If `lhs` is not
`None`, use it as the processed `lhs` instead of `self.lhs`.

    process_rhs(*compiler*, *connection*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/lookups/#Lookup.process_rhs)[¶](#django.db.models.Lookup.process_rhs)

Behaves the same way as [process_lhs()](#django.db.models.Lookup.process_lhs), for the right-hand side.

---

# ModelMetaoptions¶

# ModelMetaoptions¶

This document explains all the possible [metadata options](https://docs.djangoproject.com/en/topics/db/models/#meta-options) that you can give your model in its internal
`class Meta`.

## AvailableMetaoptions¶

### abstract¶

   Options.abstract[¶](#django.db.models.Options.abstract)

If `abstract = True`, this model will be an
[abstract base class](https://docs.djangoproject.com/en/topics/db/models/#abstract-base-classes).

### app_label¶

   Options.app_label[¶](#django.db.models.Options.app_label)

If a model is defined outside of an application in
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS), it must declare which app it belongs to:

```
app_label = "myapp"
```

If you want to represent a model with the format `app_label.object_name`
or `app_label.model_name` you can use `model._meta.label`
or `model._meta.label_lower` respectively.

### base_manager_name¶

   Options.base_manager_name[¶](#django.db.models.Options.base_manager_name)

The attribute name of the manager, for example, `'objects'`, to use for
the model’s [_base_manager](https://docs.djangoproject.com/en/topics/db/managers/#django.db.models.Model._base_manager).

### db_table¶

   Options.db_table[¶](#django.db.models.Options.db_table)

The name of the database table to use for the model:

```
db_table = "music_album"
```

#### Table names¶

To save you time, Django automatically derives the name of the database table
from the name of your model class and the app that contains it. A model’s
database table name is constructed by joining the model’s “app label” – the
name you used in [manage.pystartapp](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-startapp) – to the model’s
class name, with an underscore between them.

For example, if you have an app `bookstore` (as created by
`manage.py startapp bookstore`), a model defined as `class Book` will have
a database table named `bookstore_book`.

To override the database table name, use the `db_table` parameter in
`class Meta`.

If your database table name is an SQL reserved word, or contains characters that
aren’t allowed in Python variable names – notably, the hyphen – that’s OK.
Django quotes column and table names behind the scenes.

Use lowercase table names for MariaDB and MySQL

It is strongly advised that you use lowercase table names when you override
the table name via `db_table`, particularly if you are using the MySQL
backend. See the [MySQL notes](https://docs.djangoproject.com/en/5.0/databases/#mysql-notes) for more details.

Table name quoting for Oracle

In order to meet the 30-char limitation Oracle has on table names,
and match the usual conventions for Oracle databases, Django may shorten
table names and turn them all-uppercase. To prevent such transformations,
use a quoted name as the value for `db_table`:

```
db_table = '"name_left_in_lowercase"'
```

Such quoted names can also be used with Django’s other supported database
backends; except for Oracle, however, the quotes have no effect. See the
[Oracle notes](https://docs.djangoproject.com/en/5.0/databases/#oracle-notes) for more details.

### db_table_comment¶

  New in Django 4.2.    Options.db_table_comment[¶](#django.db.models.Options.db_table_comment)

The comment on the database table to use for this model. It is useful for
documenting database tables for individuals with direct database access who may
not be looking at your Django code. For example:

```
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    class Meta:
        db_table_comment = "Question answers"
```

### db_tablespace¶

   Options.db_tablespace[¶](#django.db.models.Options.db_tablespace)

The name of the [database tablespace](https://docs.djangoproject.com/en/topics/db/tablespaces/) to use
for this model. The default is the project’s [DEFAULT_TABLESPACE](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_TABLESPACE)
setting, if set. If the backend doesn’t support tablespaces, this option is
ignored.

### default_manager_name¶

   Options.default_manager_name[¶](#django.db.models.Options.default_manager_name)

The name of the manager to use for the model’s
[_default_manager](https://docs.djangoproject.com/en/topics/db/managers/#django.db.models.Model._default_manager).

### default_related_name¶

   Options.default_related_name[¶](#django.db.models.Options.default_related_name)

The name that will be used by default for the relation from a related object
back to this one. The default is `<model_name>_set`.

This option also sets [related_query_name](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.ForeignKey.related_query_name).

As the reverse name for a field should be unique, be careful if you intend
to subclass your model. To work around name collisions, part of the name
should contain `'%(app_label)s'` and `'%(model_name)s'`, which are
replaced respectively by the name of the application the model is in,
and the name of the model, both lowercased. See the paragraph on
[related names for abstract models](https://docs.djangoproject.com/en/topics/db/models/#abstract-related-name).

### get_latest_by¶

   Options.get_latest_by[¶](#django.db.models.Options.get_latest_by)

The name of a field or a list of field names in the model, typically
[DateField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.DateField), [DateTimeField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.DateTimeField), or [IntegerField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.IntegerField). This
specifies the default field(s) to use in your model [Manager](https://docs.djangoproject.com/en/topics/db/managers/#django.db.models.Manager)’s
[latest()](https://docs.djangoproject.com/en/5.0/ref/querysets/#django.db.models.query.QuerySet.latest) and
[earliest()](https://docs.djangoproject.com/en/5.0/ref/querysets/#django.db.models.query.QuerySet.earliest) methods.

Example:

```
# Latest by ascending order_date.
get_latest_by = "order_date"

# Latest by priority descending, order_date ascending.
get_latest_by = ["-priority", "order_date"]
```

See the [latest()](https://docs.djangoproject.com/en/5.0/ref/querysets/#django.db.models.query.QuerySet.latest) docs for more.

### managed¶

   Options.managed[¶](#django.db.models.Options.managed)

Defaults to `True`, meaning Django will create the appropriate database
tables in [migrate](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-migrate) or as part of migrations and remove them as
part of a [flush](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-flush) management command. That is, Django
*manages* the database tables’ lifecycles.

If `False`, no database table creation, modification, or deletion
operations will be performed for this model. This is useful if the model
represents an existing table or a database view that has been created by
some other means. This is the *only* difference when `managed=False`. All
other aspects of model handling are exactly the same as normal. This
includes

1. Adding an automatic primary key field to the model if you don’t
  declare it.  To avoid confusion for later code readers, it’s
  recommended to specify all the columns from the database table you
  are modeling when using unmanaged models.
2. If a model with `managed=False` contains a
  [ManyToManyField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.ManyToManyField) that points to another
  unmanaged model, then the intermediate table for the many-to-many
  join will also not be created. However, the intermediary table
  between one managed and one unmanaged model *will* be created.
  If you need to change this default behavior, create the intermediary
  table as an explicit model (with `managed` set as needed) and use
  the [ManyToManyField.through](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.ManyToManyField.through) attribute to make the relation
  use your custom model.

For tests involving models with `managed=False`, it’s up to you to ensure
the correct tables are created as part of the test setup.

If you’re interested in changing the Python-level behavior of a model class,
you *could* use `managed=False` and create a copy of an existing model.
However, there’s a better approach for that situation: [Proxy models](https://docs.djangoproject.com/en/topics/db/models/#proxy-models).

### order_with_respect_to¶

   Options.order_with_respect_to[¶](#django.db.models.Options.order_with_respect_to)

Makes this object orderable with respect to the given field, usually a
`ForeignKey`. This can be used to make related objects orderable with
respect to a parent object. For example, if an `Answer` relates to a
`Question` object, and a question has more than one answer, and the order
of answers matters, you’d do this:

```
from django.db import models

class Question(models.Model):
    text = models.TextField()
    # ...

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ...

    class Meta:
        order_with_respect_to = "question"
```

When `order_with_respect_to` is set, two additional methods are provided to
retrieve and to set the order of the related objects: `get_RELATED_order()`
and `set_RELATED_order()`, where `RELATED` is the lowercased model name. For
example, assuming that a `Question` object has multiple related `Answer`
objects, the list returned contains the primary keys of the related `Answer`
objects:

```
>>> question = Question.objects.get(id=1)
>>> question.get_answer_order()
[1, 2, 3]
```

The order of a `Question` object’s related `Answer` objects can be set by
passing in a list of `Answer` primary keys:

```
>>> question.set_answer_order([3, 1, 2])
```

The related objects also get two methods, `get_next_in_order()` and
`get_previous_in_order()`, which can be used to access those objects in their
proper order. Assuming the `Answer` objects are ordered by `id`:

```
>>> answer = Answer.objects.get(id=2)
>>> answer.get_next_in_order()
<Answer: 3>
>>> answer.get_previous_in_order()
<Answer: 1>
```

`order_with_respect_to` implicitly sets the `ordering` option

Internally, `order_with_respect_to` adds an additional field/database
column named `_order` and sets the model’s [ordering](#django.db.models.Options.ordering)
option to this field. Consequently, `order_with_respect_to` and
`ordering` cannot be used together, and the ordering added by
`order_with_respect_to` will apply whenever you obtain a list of objects
of this model.

Changing `order_with_respect_to`

Because `order_with_respect_to` adds a new database column, be sure to
make and apply the appropriate migrations if you add or change
`order_with_respect_to` after your initial [migrate](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-migrate).

### ordering¶

   Options.ordering[¶](#django.db.models.Options.ordering)

The default ordering for the object, for use when obtaining lists of objects:

```
ordering = ["-order_date"]
```

This is a tuple or list of strings and/or query expressions. Each string is
a field name with an optional “-” prefix, which indicates descending order.
Fields without a leading “-” will be ordered ascending. Use the string “?”
to order randomly.

For example, to order by a `pub_date` field ascending, use this:

```
ordering = ["pub_date"]
```

To order by `pub_date` descending, use this:

```
ordering = ["-pub_date"]
```

To order by `pub_date` descending, then by `author` ascending, use this:

```
ordering = ["-pub_date", "author"]
```

You can also use [query expressions](https://docs.djangoproject.com/en/5.0/ref/expressions/). To
order by `author` ascending and make null values sort last, use this:

```
from django.db.models import F

ordering = [F("author").asc(nulls_last=True)]
```

Warning

Ordering is not a free operation. Each field you add to the ordering
incurs a cost to your database. Each foreign key you add will
implicitly include all of its default orderings as well.

If a query doesn’t have an ordering specified, results are returned from
the database in an unspecified order. A particular ordering is guaranteed
only when ordering by a set of fields that uniquely identify each object in
the results. For example, if a `name` field isn’t unique, ordering by it
won’t guarantee objects with the same name always appear in the same order.

### permissions¶

   Options.permissions[¶](#django.db.models.Options.permissions)

Extra permissions to enter into the permissions table when creating this object.
Add, change, delete, and view permissions are automatically created for each
model. This example specifies an extra permission, `can_deliver_pizzas`:

```
permissions = [("can_deliver_pizzas", "Can deliver pizzas")]
```

This is a list or tuple of 2-tuples in the format `(permission_code,
human_readable_permission_name)`.

### default_permissions¶

   Options.default_permissions[¶](#django.db.models.Options.default_permissions)

Defaults to `('add', 'change', 'delete', 'view')`. You may customize this
list, for example, by setting this to an empty list if your app doesn’t
require any of the default permissions. It must be specified on the model
before the model is created by [migrate](https://docs.djangoproject.com/en/5.0/django-admin/#django-admin-migrate) in order to prevent any
omitted permissions from being created.

### proxy¶

   Options.proxy[¶](#django.db.models.Options.proxy)

If `proxy = True`, a model which subclasses another model will be treated as
a [proxy model](https://docs.djangoproject.com/en/topics/db/models/#proxy-models).

### required_db_features¶

   Options.required_db_features[¶](#django.db.models.Options.required_db_features)

List of database features that the current connection should have so that
the model is considered during the migration phase. For example, if you set
this list to `['gis_enabled']`, the model will only be synchronized on
GIS-enabled databases. It’s also useful to skip some models when testing
with several database backends. Avoid relations between models that may or
may not be created as the ORM doesn’t handle this.

### required_db_vendor¶

   Options.required_db_vendor[¶](#django.db.models.Options.required_db_vendor)

Name of a supported database vendor that this model is specific to. Current
built-in vendor names are: `sqlite`, `postgresql`, `mysql`,
`oracle`. If this attribute is not empty and the current connection vendor
doesn’t match it, the model will not be synchronized.

### select_on_save¶

   Options.select_on_save[¶](#django.db.models.Options.select_on_save)

Determines if Django will use the pre-1.6
[django.db.models.Model.save()](https://docs.djangoproject.com/en/5.0/ref/instances/#django.db.models.Model.save) algorithm. The old algorithm
uses `SELECT` to determine if there is an existing row to be updated.
The new algorithm tries an `UPDATE` directly. In some rare cases the
`UPDATE` of an existing row isn’t visible to Django. An example is the
PostgreSQL `ON UPDATE` trigger which returns `NULL`. In such cases the
new algorithm will end up doing an `INSERT` even when a row exists in
the database.

Usually there is no need to set this attribute. The default is
`False`.

See [django.db.models.Model.save()](https://docs.djangoproject.com/en/5.0/ref/instances/#django.db.models.Model.save) for more about the old and
new saving algorithm.

### indexes¶

   Options.indexes[¶](#django.db.models.Options.indexes)

A list of [indexes](https://docs.djangoproject.com/en/5.0/ref/indexes/) that you want to define on
the model:

```
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["first_name"], name="first_name_idx"),
        ]
```

### unique_together¶

   Options.unique_together[¶](#django.db.models.Options.unique_together)

Use [UniqueConstraint](https://docs.djangoproject.com/en/5.0/ref/constraints/#django.db.models.UniqueConstraint) with the [constraints](#django.db.models.Options.constraints) option instead.

[UniqueConstraint](https://docs.djangoproject.com/en/5.0/ref/constraints/#django.db.models.UniqueConstraint) provides more functionality than
`unique_together`. `unique_together` may be deprecated in the
future.

Sets of field names that, taken together, must be unique:

```
unique_together = [["driver", "restaurant"]]
```

This is a list of lists that must be unique when considered together.
It’s used in the Django admin and is enforced at the database level (i.e., the
appropriate `UNIQUE` statements are included in the `CREATE TABLE`
statement).

For convenience, `unique_together` can be a single list when dealing with
a single set of fields:

```
unique_together = ["driver", "restaurant"]
```

A [ManyToManyField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.ManyToManyField) cannot be included in
`unique_together`. (It’s not clear what that would even mean!) If you
need to validate uniqueness related to a
[ManyToManyField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.ManyToManyField), try using a signal or
an explicit [through](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.ManyToManyField.through) model.

The `ValidationError` raised during model validation when the constraint
is violated has the `unique_together` error code.

### index_together¶

   Options.index_together[¶](#django.db.models.Options.index_together)

Sets of field names that, taken together, are indexed:

```
index_together = [
    ["pub_date", "deadline"],
]
```

This list of fields will be indexed together (i.e. the appropriate
`CREATE INDEX` statement will be issued.)

For convenience, `index_together` can be a single list when dealing with a single
set of fields:

```
index_together = ["pub_date", "deadline"]
```

Deprecated since version 4.2: Use the [indexes](#django.db.models.Options.indexes) option instead.

### constraints¶

   Options.constraints[¶](#django.db.models.Options.constraints)

A list of [constraints](https://docs.djangoproject.com/en/5.0/ref/constraints/) that you want to
define on the model:

```
from django.db import models

class Customer(models.Model):
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name="age_gte_18"),
        ]
```

### verbose_name¶

   Options.verbose_name[¶](#django.db.models.Options.verbose_name)

A human-readable name for the object, singular:

```
verbose_name = "pizza"
```

If this isn’t given, Django will use a munged version of the class name:
`CamelCase` becomes `camel case`.

### verbose_name_plural¶

   Options.verbose_name_plural[¶](#django.db.models.Options.verbose_name_plural)

The plural name for the object:

```
verbose_name_plural = "stories"
```

If this isn’t given, Django will use [verbose_name](#django.db.models.Options.verbose_name) + `"s"`.

## Read-onlyMetaattributes¶

### label¶

   Options.label[¶](#django.db.models.Options.label)

Representation of the object, returns `app_label.object_name`, e.g.
`'polls.Question'`.

### label_lower¶

   Options.label_lower[¶](#django.db.models.Options.label_lower)

Representation of the model, returns `app_label.model_name`, e.g.
`'polls.question'`.
