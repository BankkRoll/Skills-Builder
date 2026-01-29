# Model index reference¶ and more

# Model index reference¶

# Model index reference¶

Index classes ease creating database indexes. They can be added using the
[Meta.indexes](https://docs.djangoproject.com/en/5.0/ref/options/#django.db.models.Options.indexes) option. This document
explains the API references of [Index](#django.db.models.Index) which includes the [index
options](#index-options).

Referencing built-in indexes

Indexes are defined in `django.db.models.indexes`, but for convenience
they’re imported into [django.db.models](https://docs.djangoproject.com/en/topics/db/models/#module-django.db.models). The standard convention is
to use `from django.db import models` and refer to the indexes as
`models.<IndexClass>`.

## Indexoptions¶

   *class*Index(**expressions*, *fields=()*, *name=None*, *db_tablespace=None*, *opclasses=()*, *condition=None*, *include=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/indexes/#Index)[¶](#django.db.models.Index)

Creates an index (B-Tree) in the database.

### expressions¶

   Index.expressions[¶](#django.db.models.Index.expressions)

Positional argument `*expressions` allows creating functional indexes on
expressions and database functions.

For example:

```
Index(Lower("title").desc(), "pub_date", name="lower_title_date_idx")
```

creates an index on the lowercased value of the `title` field in descending
order and the `pub_date` field in the default ascending order.

Another example:

```
Index(F("height") * F("weight"), Round("weight"), name="calc_idx")
```

creates an index on the result of multiplying fields `height` and `weight`
and the `weight` rounded to the nearest integer.

[Index.name](#django.db.models.Index.name) is required when using `*expressions`.

Restrictions on Oracle

Oracle requires functions referenced in an index to be marked as
`DETERMINISTIC`. Django doesn’t validate this but Oracle will error. This
means that functions such as
[Random()](https://docs.djangoproject.com/en/5.0/ref/database-functions/#django.db.models.functions.Random) aren’t accepted.

Restrictions on PostgreSQL

PostgreSQL requires functions and operators referenced in an index to be
marked as `IMMUTABLE`. Django doesn’t validate this but PostgreSQL will
error. This means that functions such as
[Concat()](https://docs.djangoproject.com/en/5.0/ref/database-functions/#django.db.models.functions.Concat) aren’t accepted.

MySQL and MariaDB

Functional indexes are ignored with MySQL < 8.0.13 and MariaDB as neither
supports them.

### fields¶

   Index.fields[¶](#django.db.models.Index.fields)

A list or tuple of the name of the fields on which the index is desired.

By default, indexes are created with an ascending order for each column. To
define an index with a descending order for a column, add a hyphen before the
field’s name.

For example `Index(fields=['headline', '-pub_date'])` would create SQL with
`(headline, pub_date DESC)`.

MariaDB

Index ordering isn’t supported on MariaDB < 10.8. In that case, a
descending index is created as a normal index.

### name¶

   Index.name[¶](#django.db.models.Index.name)

The name of the index. If `name` isn’t provided Django will auto-generate a
name. For compatibility with different databases, index names cannot be longer
than 30 characters and shouldn’t start with a number (0-9) or underscore (_).

Partial indexes in abstract base classes

You must always specify a unique name for an index. As such, you
cannot normally specify a partial index on an abstract base class, since
the [Meta.indexes](https://docs.djangoproject.com/en/5.0/ref/options/#django.db.models.Options.indexes) option is
inherited by subclasses, with exactly the same values for the attributes
(including `name`) each time. To work around name collisions, part of the
name may contain `'%(app_label)s'` and `'%(class)s'`, which are
replaced, respectively, by the lowercased app label and class name of the
concrete model. For example `Index(fields=['title'],
name='%(app_label)s_%(class)s_title_index')`.

### db_tablespace¶

   Index.db_tablespace[¶](#django.db.models.Index.db_tablespace)

The name of the [database tablespace](https://docs.djangoproject.com/en/topics/db/tablespaces/) to use for
this index. For single field indexes, if `db_tablespace` isn’t provided, the
index is created in the `db_tablespace` of the field.

If [Field.db_tablespace](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.db_tablespace) isn’t specified (or if the index uses multiple
fields), the index is created in tablespace specified in the
[db_tablespace](https://docs.djangoproject.com/en/5.0/ref/options/#django.db.models.Options.db_tablespace) option inside the model’s
`class Meta`. If neither of those tablespaces are set, the index is created
in the same tablespace as the table.

See also

For a list of PostgreSQL-specific indexes, see
[django.contrib.postgres.indexes](https://docs.djangoproject.com/en/5.0/contrib/postgres/indexes/#module-django.contrib.postgres.indexes).

### opclasses¶

   Index.opclasses[¶](#django.db.models.Index.opclasses)

The names of the [PostgreSQL operator classes](https://www.postgresql.org/docs/current/indexes-opclass.html) to use for
this index. If you require a custom operator class, you must provide one for
each field in the index.

For example, `GinIndex(name='json_index', fields=['jsonfield'],
opclasses=['jsonb_path_ops'])` creates a gin index on `jsonfield` using
`jsonb_path_ops`.

`opclasses` are ignored for databases besides PostgreSQL.

[Index.name](#django.db.models.Index.name) is required when using `opclasses`.

### condition¶

   Index.condition[¶](#django.db.models.Index.condition)

If the table is very large and your queries mostly target a subset of rows,
it may be useful to restrict an index to that subset. Specify a condition as a
[Q](https://docs.djangoproject.com/en/5.0/ref/querysets/#django.db.models.Q). For example, `condition=Q(pages__gt=400)`
indexes records with more than 400 pages.

[Index.name](#django.db.models.Index.name) is required when using `condition`.

Restrictions on PostgreSQL

PostgreSQL requires functions referenced in the condition to be marked as
IMMUTABLE. Django doesn’t validate this but PostgreSQL will error. This
means that functions such as [Date functions](https://docs.djangoproject.com/en/5.0/ref/database-functions/#date-functions) and
[Concat](https://docs.djangoproject.com/en/5.0/ref/database-functions/#django.db.models.functions.Concat) aren’t accepted. If you store
dates in [DateTimeField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.DateTimeField), comparison to
[datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) objects may require the `tzinfo` argument
to be provided because otherwise the comparison could result in a mutable
function due to the casting Django does for [lookups](https://docs.djangoproject.com/en/5.0/ref/querysets/#field-lookups).

Restrictions on SQLite

SQLite [imposes restrictions](https://www.sqlite.org/partialindex.html)
on how a partial index can be constructed.

Oracle

Oracle does not support partial indexes. Instead, partial indexes can be
emulated by using functional indexes together with
[Case](https://docs.djangoproject.com/en/5.0/ref/conditional-expressions/#django.db.models.expressions.Case) expressions.

MySQL and MariaDB

The `condition` argument is ignored with MySQL and MariaDB as neither
supports conditional indexes.

### include¶

   Index.include[¶](#django.db.models.Index.include)

A list or tuple of the names of the fields to be included in the covering index
as non-key columns. This allows index-only scans to be used for queries that
select only included fields ([include](#django.db.models.Index.include)) and filter only by indexed
fields ([fields](#django.db.models.Index.fields)).

For example:

```
Index(name="covering_index", fields=["headline"], include=["pub_date"])
```

will allow filtering on `headline`, also selecting `pub_date`, while
fetching data only from the index.

Using `include` will produce a smaller index than using a multiple column
index but with the drawback that non-key columns can not be used for sorting or
filtering.

`include` is ignored for databases besides PostgreSQL.

[Index.name](#django.db.models.Index.name) is required when using `include`.

See the PostgreSQL documentation for more details about [covering indexes](https://www.postgresql.org/docs/current/indexes-index-only-scans.html).

Restrictions on PostgreSQL

PostgreSQL supports covering B-Tree and [GiSTindexes](https://docs.djangoproject.com/en/5.0/contrib/postgres/indexes/#django.contrib.postgres.indexes.GistIndex). PostgreSQL 14+ also supports
covering [SP-GiSTindexes](https://docs.djangoproject.com/en/5.0/contrib/postgres/indexes/#django.contrib.postgres.indexes.SpGistIndex).

---

# Model instance reference¶

# Model instance reference¶

This document describes the details of the `Model` API. It builds on the
material presented in the [model](https://docs.djangoproject.com/en/topics/db/models/) and [database
query](https://docs.djangoproject.com/en/topics/db/queries/) guides, so you’ll probably want to read and
understand those documents before reading this one.

Throughout this reference we’ll use the [example blog models](https://docs.djangoproject.com/en/topics/db/queries/#queryset-model-example) presented in the [database query guide](https://docs.djangoproject.com/en/topics/db/queries/).

## Creating objects¶

To create a new instance of a model, instantiate it like any other Python
class:

   *class*Model(***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model)[¶](#django.db.models.Model)

The keyword arguments are the names of the fields you’ve defined on your model.
Note that instantiating a model in no way touches your database; for that, you
need to [save()](#django.db.models.Model.save).

Note

You may be tempted to customize the model by overriding the `__init__`
method. If you do so, however, take care not to change the calling
signature as any change may prevent the model instance from being saved.
Additionally, referring to model fields within `__init__` may potentially
result in infinite recursion errors in some circumstances.  Rather than
overriding `__init__`, try using one of these approaches:

1. Add a classmethod on the model class:
  ```
  from django.db import models
  class Book(models.Model):
      title = models.CharField(max_length=100)
      @classmethod
      def create(cls, title):
          book = cls(title=title)
          # do something with the book
          return book
  book = Book.create("Pride and Prejudice")
  ```
2. Add a method on a custom manager (usually preferred):
  ```
  class BookManager(models.Manager):
      def create_book(self, title):
          book = self.create(title=title)
          # do something with the book
          return book
  class Book(models.Model):
      title = models.CharField(max_length=100)
      objects = BookManager()
  book = Book.objects.create_book("Pride and Prejudice")
  ```

### Customizing model loading¶

   *classmethod*Model.from_db(*db*, *field_names*, *values*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.from_db)[¶](#django.db.models.Model.from_db)

The `from_db()` method can be used to customize model instance creation
when loading from the database.

The `db` argument contains the database alias for the database the model
is loaded from, `field_names` contains the names of all loaded fields, and
`values` contains the loaded values for each field in `field_names`. The
`field_names` are in the same order as the `values`. If all of the model’s
fields are present, then `values` are guaranteed to be in the order
`__init__()` expects them. That is, the instance can be created by
`cls(*values)`. If any fields are deferred, they won’t appear in
`field_names`. In that case, assign a value of `django.db.models.DEFERRED`
to each of the missing fields.

In addition to creating the new model, the `from_db()` method must set the
`adding` and `db` flags in the new instance’s [_state](#django.db.models.Model._state) attribute.

Below is an example showing how to record the initial values of fields that
are loaded from the database:

```
from django.db.models import DEFERRED

@classmethod
def from_db(cls, db, field_names, values):
    # Default implementation of from_db() (subject to change and could
    # be replaced with super()).
    if len(values) != len(cls._meta.concrete_fields):
        values = list(values)
        values.reverse()
        values = [
            values.pop() if f.attname in field_names else DEFERRED
            for f in cls._meta.concrete_fields
        ]
    instance = cls(*values)
    instance._state.adding = False
    instance._state.db = db
    # customization to store the original field values on the instance
    instance._loaded_values = dict(
        zip(field_names, (value for value in values if value is not DEFERRED))
    )
    return instance

def save(self, *args, **kwargs):
    # Check how the current values differ from ._loaded_values. For example,
    # prevent changing the creator_id of the model. (This example doesn't
    # support cases where 'creator_id' is deferred).
    if not self._state.adding and (
        self.creator_id != self._loaded_values["creator_id"]
    ):
        raise ValueError("Updating the value of creator isn't allowed")
    super().save(*args, **kwargs)
```

The example above shows a full `from_db()` implementation to clarify how that
is done. In this case it would be possible to use a `super()` call in the
`from_db()` method.

## Refreshing objects from database¶

If you delete a field from a model instance, accessing it again reloads the
value from the database:

```
>>> obj = MyModel.objects.first()
>>> del obj.field
>>> obj.field  # Loads the field from the database
```

    Model.refresh_from_db(*using=None*, *fields=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.refresh_from_db)[¶](#django.db.models.Model.refresh_from_db)    Model.arefresh_from_db(*using=None*, *fields=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.arefresh_from_db)[¶](#django.db.models.Model.arefresh_from_db)

*Asynchronous version*: `arefresh_from_db()`

If you need to reload a model’s values from the database, you can use the
`refresh_from_db()` method. When this method is called without arguments the
following is done:

1. All non-deferred fields of the model are updated to the values currently
  present in the database.
2. Any cached relations are cleared from the reloaded instance.

Only fields of the model are reloaded from the database. Other
database-dependent values such as annotations aren’t reloaded. Any
[@cached_property](https://docs.djangoproject.com/en/5.0/utils/#django.utils.functional.cached_property) attributes
aren’t cleared either.

The reloading happens from the database the instance was loaded from, or from
the default database if the instance wasn’t loaded from the database. The
`using` argument can be used to force the database used for reloading.

It is possible to force the set of fields to be loaded by using the `fields`
argument.

For example, to test that an `update()` call resulted in the expected
update, you could write a test similar to this:

```
def test_update_result(self):
    obj = MyModel.objects.create(val=1)
    MyModel.objects.filter(pk=obj.pk).update(val=F("val") + 1)
    # At this point obj.val is still 1, but the value in the database
    # was updated to 2. The object's updated value needs to be reloaded
    # from the database.
    obj.refresh_from_db()
    self.assertEqual(obj.val, 2)
```

Note that when deferred fields are accessed, the loading of the deferred
field’s value happens through this method. Thus it is possible to customize
the way deferred loading happens. The example below shows how one can reload
all of the instance’s fields when a deferred field is reloaded:

```
class ExampleModel(models.Model):
    def refresh_from_db(self, using=None, fields=None, **kwargs):
        # fields contains the name of the deferred field to be
        # loaded.
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            # If any deferred field is going to be loaded
            if fields.intersection(deferred_fields):
                # then load all of them
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)
```

    Model.get_deferred_fields()[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.get_deferred_fields)[¶](#django.db.models.Model.get_deferred_fields)

A helper method that returns a set containing the attribute names of all those
fields that are currently deferred for this model.

  Changed in Django 4.2:

`arefresh_from_db()` method was added.

## Validating objects¶

There are four steps involved in validating a model:

1. Validate the model fields - [Model.clean_fields()](#django.db.models.Model.clean_fields)
2. Validate the model as a whole - [Model.clean()](#django.db.models.Model.clean)
3. Validate the field uniqueness - [Model.validate_unique()](#django.db.models.Model.validate_unique)
4. Validate the constraints - [Model.validate_constraints()](#django.db.models.Model.validate_constraints)

All four steps are performed when you call a model’s [full_clean()](#django.db.models.Model.full_clean)
method.

When you use a [ModelForm](https://docs.djangoproject.com/en/topics/forms/modelforms/#django.forms.ModelForm), the call to
[is_valid()](https://docs.djangoproject.com/en/5.0/forms/api/#django.forms.Form.is_valid) will perform these validation steps for
all the fields that are included on the form. See the [ModelForm
documentation](https://docs.djangoproject.com/en/topics/forms/modelforms/) for more information. You should only
need to call a model’s [full_clean()](#django.db.models.Model.full_clean) method if you plan to handle
validation errors yourself, or if you have excluded fields from the
[ModelForm](https://docs.djangoproject.com/en/topics/forms/modelforms/#django.forms.ModelForm) that require validation.

Warning

Constraints containing [JSONField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.JSONField) may not raise
validation errors as key, index, and path transforms have many
database-specific caveats. This [may be fully supported later](https://code.djangoproject.com/ticket/34059).

You should always check that there are no log messages, in the
`django.db.models` logger, like *“Got a database error calling check() on
…”* to confirm it’s validated properly.

    Model.full_clean(*exclude=None*, *validate_unique=True*, *validate_constraints=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.full_clean)[¶](#django.db.models.Model.full_clean)

This method calls [Model.clean_fields()](#django.db.models.Model.clean_fields), [Model.clean()](#django.db.models.Model.clean),
[Model.validate_unique()](#django.db.models.Model.validate_unique) (if `validate_unique` is `True`),  and
[Model.validate_constraints()](#django.db.models.Model.validate_constraints) (if `validate_constraints` is `True`)
in that order and raises a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) that
has a `message_dict` attribute containing errors from all four stages.

The optional `exclude` argument can be used to provide a `set` of field
names that can be excluded from validation and cleaning.
[ModelForm](https://docs.djangoproject.com/en/topics/forms/modelforms/#django.forms.ModelForm) uses this argument to exclude fields that
aren’t present on your form from being validated since any errors raised could
not be corrected by the user.

Note that `full_clean()` will *not* be called automatically when you call
your model’s [save()](#django.db.models.Model.save) method. You’ll need to call it manually
when you want to run one-step model validation for your own manually created
models. For example:

```
from django.core.exceptions import ValidationError

try:
    article.full_clean()
except ValidationError as e:
    # Do something based on the errors contained in e.message_dict.
    # Display them to a user, or handle them programmatically.
    pass
```

The first step `full_clean()` performs is to clean each individual field.

   Model.clean_fields(*exclude=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.clean_fields)[¶](#django.db.models.Model.clean_fields)

This method will validate all fields on your model. The optional `exclude`
argument lets you provide a `set` of field names to exclude from validation.
It will raise a [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if any fields
fail validation.

The second step `full_clean()` performs is to call [Model.clean()](#django.db.models.Model.clean).
This method should be overridden to perform custom validation on your model.

   Model.clean()[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.clean)[¶](#django.db.models.Model.clean)

This method should be used to provide custom model validation, and to modify
attributes on your model if desired. For instance, you could use it to
automatically provide a value for a field, or to do validation that requires
access to more than a single field:

```
import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class Article(models.Model):
    ...

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.status == "draft" and self.pub_date is not None:
            raise ValidationError(_("Draft entries may not have a publication date."))
        # Set the pub_date for published items if it hasn't been set already.
        if self.status == "published" and self.pub_date is None:
            self.pub_date = datetime.date.today()
```

Note, however, that like [Model.full_clean()](#django.db.models.Model.full_clean), a model’s `clean()`
method is not invoked when you call your model’s [save()](#django.db.models.Model.save) method.

In the above example, the [ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError)
exception raised by `Model.clean()` was instantiated with a string, so it
will be stored in a special error dictionary key,
[NON_FIELD_ERRORS](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.NON_FIELD_ERRORS). This key is used for errors
that are tied to the entire model instead of to a specific field:

```
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

try:
    article.full_clean()
except ValidationError as e:
    non_field_errors = e.message_dict[NON_FIELD_ERRORS]
```

To assign exceptions to a specific field, instantiate the
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) with a dictionary, where the
keys are the field names. We could update the previous example to assign the
error to the `pub_date` field:

```
class Article(models.Model):
    ...

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.status == "draft" and self.pub_date is not None:
            raise ValidationError(
                {"pub_date": _("Draft entries may not have a publication date.")}
            )
        ...
```

If you detect errors in multiple fields during `Model.clean()`, you can also
pass a dictionary mapping field names to errors:

```
raise ValidationError(
    {
        "title": ValidationError(_("Missing title."), code="required"),
        "pub_date": ValidationError(_("Invalid date."), code="invalid"),
    }
)
```

Then, `full_clean()` will check unique constraints on your model.

How to raise field-specific validation errors if those fields don’t appear in a `ModelForm`

You can’t raise validation errors in `Model.clean()` for fields that
don’t appear in a model form (a form may limit its fields using
`Meta.fields` or `Meta.exclude`). Doing so will raise a `ValueError`
because the validation error won’t be able to be associated with the
excluded field.

To work around this dilemma, instead override [Model.clean_fields()](#django.db.models.Model.clean_fields) as it receives the list of fields
that are excluded from validation. For example:

```
class Article(models.Model):
    ...

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.status == "draft" and self.pub_date is not None:
            if exclude and "status" in exclude:
                raise ValidationError(
                    _("Draft entries may not have a publication date.")
                )
            else:
                raise ValidationError(
                    {
                        "status": _(
                            "Set status to draft if there is not a publication date."
                        ),
                    }
                )
```

     Model.validate_unique(*exclude=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.validate_unique)[¶](#django.db.models.Model.validate_unique)

This method is similar to [clean_fields()](#django.db.models.Model.clean_fields), but validates
uniqueness constraints defined via [Field.unique](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.unique),
[Field.unique_for_date](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.unique_for_date), [Field.unique_for_month](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.unique_for_month),
[Field.unique_for_year](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.unique_for_year), or [Meta.unique_together](https://docs.djangoproject.com/en/5.0/ref/options/#django.db.models.Options.unique_together) on your model instead of individual
field values. The optional `exclude` argument allows you to provide a `set`
of field names to exclude from validation. It will raise a
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if any fields fail validation.

[UniqueConstraint](https://docs.djangoproject.com/en/5.0/ref/constraints/#django.db.models.UniqueConstraint)s defined in the
[Meta.constraints](https://docs.djangoproject.com/en/5.0/ref/options/#django.db.models.Options.constraints) are validated
by [Model.validate_constraints()](#django.db.models.Model.validate_constraints).

Note that if you provide an `exclude` argument to `validate_unique()`, any
[unique_together](https://docs.djangoproject.com/en/5.0/ref/options/#django.db.models.Options.unique_together) constraint involving one of
the fields you provided will not be checked.

Finally, `full_clean()` will check any other constraints on your model.

   Model.validate_constraints(*exclude=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.validate_constraints)[¶](#django.db.models.Model.validate_constraints)

This method validates all constraints defined in
[Meta.constraints](https://docs.djangoproject.com/en/5.0/ref/options/#django.db.models.Options.constraints). The
optional `exclude` argument allows you to provide a `set` of field names to
exclude from validation. It will raise a
[ValidationError](https://docs.djangoproject.com/en/5.0/exceptions/#django.core.exceptions.ValidationError) if any constraints fail
validation.

## Saving objects¶

To save an object back to the database, call `save()`:

   Model.save(*force_insert=False*, *force_update=False*, *using=DEFAULT_DB_ALIAS*, *update_fields=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.save)[¶](#django.db.models.Model.save)    Model.asave(*force_insert=False*, *force_update=False*, *using=DEFAULT_DB_ALIAS*, *update_fields=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.asave)[¶](#django.db.models.Model.asave)

*Asynchronous version*: `asave()`

For details on using the `force_insert` and `force_update` arguments, see
[Forcing an INSERT or UPDATE](#ref-models-force-insert). Details about the `update_fields` argument
can be found in the [Specifying which fields to save](#ref-models-update-fields) section.

If you want customized saving behavior, you can override this `save()`
method. See [Overriding predefined model methods](https://docs.djangoproject.com/en/topics/db/models/#overriding-model-methods) for more details.

The model save process also has some subtleties; see the sections below.

  Changed in Django 4.2:

`asave()` method was added.

### Auto-incrementing primary keys¶

If a model has an [AutoField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.AutoField) — an auto-incrementing
primary key — then that auto-incremented value will be calculated and saved as
an attribute on your object the first time you call `save()`:

```
>>> b2 = Blog(name="Cheddar Talk", tagline="Thoughts on cheese.")
>>> b2.id  # Returns None, because b2 doesn't have an ID yet.
>>> b2.save()
>>> b2.id  # Returns the ID of your new object.
```

There’s no way to tell what the value of an ID will be before you call
`save()`, because that value is calculated by your database, not by Django.

For convenience, each model has an [AutoField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.AutoField) named
`id` by default unless you explicitly specify `primary_key=True` on a field
in your model. See the documentation for [AutoField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.AutoField)
for more details.

#### Thepkproperty¶

   Model.pk[¶](#django.db.models.Model.pk)

Regardless of whether you define a primary key field yourself, or let Django
supply one for you, each model will have a property called `pk`. It behaves
like a normal attribute on the model, but is actually an alias for whichever
attribute is the primary key field for the model. You can read and set this
value, just as you would for any other attribute, and it will update the
correct field in the model.

#### Explicitly specifying auto-primary-key values¶

If a model has an [AutoField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.AutoField) but you want to define a
new object’s ID explicitly when saving, define it explicitly before saving,
rather than relying on the auto-assignment of the ID:

```
>>> b3 = Blog(id=3, name="Cheddar Talk", tagline="Thoughts on cheese.")
>>> b3.id  # Returns 3.
>>> b3.save()
>>> b3.id  # Returns 3.
```

If you assign auto-primary-key values manually, make sure not to use an
already-existing primary-key value! If you create a new object with an explicit
primary-key value that already exists in the database, Django will assume you’re
changing the existing record rather than creating a new one.

Given the above `'Cheddar Talk'` blog example, this example would override the
previous record in the database:

```
b4 = Blog(id=3, name="Not Cheddar", tagline="Anything but cheese.")
b4.save()  # Overrides the previous blog with ID=3!
```

See [How Django knows to UPDATE vs. INSERT](#how-django-knows-to-update-vs-insert), below, for the reason this
happens.

Explicitly specifying auto-primary-key values is mostly useful for bulk-saving
objects, when you’re confident you won’t have primary-key collision.

If you’re using PostgreSQL, the sequence associated with the primary key might
need to be updated; see [Manually-specifying values of auto-incrementing primary keys](https://docs.djangoproject.com/en/5.0/databases/#manually-specified-autoincrement-pk).

### What happens when you save?¶

When you save an object, Django performs the following steps:

1. **Emit a pre-save signal.** The [pre_save](https://docs.djangoproject.com/en/5.0/signals/#django.db.models.signals.pre_save)
  signal is sent, allowing any functions listening for that signal to do
  something.
2. **Preprocess the data.** Each field’s
  [pre_save()](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.pre_save) method is called to perform any
  automated data modification that’s needed. For example, the date/time fields
  override `pre_save()` to implement
  [auto_now_add](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.DateField.auto_now_add) and
  [auto_now](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.DateField.auto_now).
3. **Prepare the data for the database.** Each field’s
  [get_db_prep_save()](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.get_db_prep_save) method is asked to provide
  its current value in a data type that can be written to the database.
  Most fields don’t require data preparation. Simple data types, such as
  integers and strings, are ‘ready to write’ as a Python object. However, more
  complex data types often require some modification.
  For example, [DateField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.DateField) fields use a Python
  `datetime` object to store data. Databases don’t store `datetime`
  objects, so the field value must be converted into an ISO-compliant date
  string for insertion into the database.
4. **Insert the data into the database.** The preprocessed, prepared data is
  composed into an SQL statement for insertion into the database.
5. **Emit a post-save signal.** The [post_save](https://docs.djangoproject.com/en/5.0/signals/#django.db.models.signals.post_save)
  signal is sent, allowing any functions listening for that signal to do
  something.

### How Django knows to UPDATE vs. INSERT¶

You may have noticed Django database objects use the same `save()` method
for creating and changing objects. Django abstracts the need to use `INSERT`
or `UPDATE` SQL statements. Specifically, when you call `save()` and the
object’s primary key attribute does **not** define a
[default](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.default) or
[db_default](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.db_default), Django follows this algorithm:

- If the object’s primary key attribute is set to a value that evaluates to
  `True` (i.e., a value other than `None` or the empty string), Django
  executes an `UPDATE`.
- If the object’s primary key attribute is *not* set or if the `UPDATE`
  didn’t update anything (e.g. if primary key is set to a value that doesn’t
  exist in the database), Django executes an `INSERT`.

If the object’s primary key attribute defines a
[default](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.default) or
[db_default](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.db_default) then Django executes an `UPDATE`
if it is an existing model instance and primary key is set to a value that
exists in the database. Otherwise, Django executes an `INSERT`.

The one gotcha here is that you should be careful not to specify a primary-key
value explicitly when saving new objects, if you cannot guarantee the
primary-key value is unused. For more on this nuance, see [Explicitly specifying
auto-primary-key values](#explicitly-specifying-auto-primary-key-values) above and [Forcing an INSERT or UPDATE](#forcing-an-insert-or-update) below.

In Django 1.5 and earlier, Django did a `SELECT` when the primary key
attribute was set. If the `SELECT` found a row, then Django did an `UPDATE`,
otherwise it did an `INSERT`. The old algorithm results in one more query in
the `UPDATE` case. There are some rare cases where the database doesn’t
report that a row was updated even if the database contains a row for the
object’s primary key value. An example is the PostgreSQL `ON UPDATE` trigger
which returns `NULL`. In such cases it is possible to revert to the old
algorithm by setting the [select_on_save](https://docs.djangoproject.com/en/5.0/ref/options/#django.db.models.Options.select_on_save)
option to `True`.

  Changed in Django 5.0:

The `Field.db_default` parameter was added.

#### Forcing an INSERT or UPDATE¶

In some rare circumstances, it’s necessary to be able to force the
[save()](#django.db.models.Model.save) method to perform an SQL `INSERT` and not fall back to
doing an `UPDATE`. Or vice-versa: update, if possible, but not insert a new
row. In these cases you can pass the `force_insert=True` or
`force_update=True` parameters to the [save()](#django.db.models.Model.save) method.
Passing both parameters is an error: you cannot both insert *and* update at the
same time!

When using [multi-table inheritance](https://docs.djangoproject.com/en/topics/db/models/#multi-table-inheritance), it’s also
possible to provide a tuple of parent classes to `force_insert` in order to
force `INSERT` statements for each base. For example:

```
Restaurant(pk=1, name="Bob's Cafe").save(force_insert=(Place,))

Restaurant(pk=1, name="Bob's Cafe", rating=4).save(force_insert=(Place, Rating))
```

You can pass `force_insert=(models.Model,)` to force an `INSERT` statement
for all parents. By default, `force_insert=True` only forces the insertion of
a new row for the current model.

It should be very rare that you’ll need to use these parameters. Django will
almost always do the right thing and trying to override that will lead to
errors that are difficult to track down. This feature is for advanced use
only.

Using `update_fields` will force an update similarly to `force_update`.

  Changed in Django 5.0:

Support for passing a tuple of parent classes to `force_insert` was
added.

### Updating attributes based on existing fields¶

Sometimes you’ll need to perform a simple arithmetic task on a field, such
as incrementing or decrementing the current value. One way of achieving this is
doing the arithmetic in Python like:

```
>>> product = Product.objects.get(name="Venezuelan Beaver Cheese")
>>> product.number_sold += 1
>>> product.save()
```

If the old `number_sold` value retrieved from the database was 10, then
the value of 11 will be written back to the database.

The process can be made robust, [avoiding a race condition](https://docs.djangoproject.com/en/5.0/ref/expressions/#avoiding-race-conditions-using-f), as well as slightly faster by expressing
the update relative to the original field value, rather than as an explicit
assignment of a new value. Django provides [Fexpressions](https://docs.djangoproject.com/en/5.0/ref/expressions/#django.db.models.F) for performing this kind of relative update. Using
[Fexpressions](https://docs.djangoproject.com/en/5.0/ref/expressions/#django.db.models.F), the previous example is expressed
as:

```
>>> from django.db.models import F
>>> product = Product.objects.get(name="Venezuelan Beaver Cheese")
>>> product.number_sold = F("number_sold") + 1
>>> product.save()
```

For more details, see the documentation on [Fexpressions](https://docs.djangoproject.com/en/5.0/ref/expressions/#django.db.models.F) and their [use in update queries](https://docs.djangoproject.com/en/topics/db/queries/#topics-db-queries-update).

### Specifying which fields to save¶

If `save()` is passed a list of field names in keyword argument
`update_fields`, only the fields named in that list will be updated.
This may be desirable if you want to update just one or a few fields on
an object. There will be a slight performance benefit from preventing
all of the model fields from being updated in the database. For example:

```
product.name = "Name changed again"
product.save(update_fields=["name"])
```

The `update_fields` argument can be any iterable containing strings. An
empty `update_fields` iterable will skip the save. A value of `None` will
perform an update on all fields.

Specifying `update_fields` will force an update.

When saving a model fetched through deferred model loading
([only()](https://docs.djangoproject.com/en/5.0/ref/querysets/#django.db.models.query.QuerySet.only) or
[defer()](https://docs.djangoproject.com/en/5.0/ref/querysets/#django.db.models.query.QuerySet.defer)) only the fields loaded
from the DB will get updated. In effect there is an automatic
`update_fields` in this case. If you assign or change any deferred field
value, the field will be added to the updated fields.

`Field.pre_save()` and `update_fields`

If `update_fields` is passed in, only the
[pre_save()](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.pre_save) methods of the `update_fields`
are called. For example, this means that date/time fields with
`auto_now=True` will not be updated unless they are included in the
`update_fields`.

## Deleting objects¶

   Model.delete(*using=DEFAULT_DB_ALIAS*, *keep_parents=False*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.delete)[¶](#django.db.models.Model.delete)    Model.adelete(*using=DEFAULT_DB_ALIAS*, *keep_parents=False*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.adelete)[¶](#django.db.models.Model.adelete)

*Asynchronous version*: `adelete()`

Issues an SQL `DELETE` for the object. This only deletes the object in the
database; the Python instance will still exist and will still have data in
its fields, except for the primary key set to `None`. This method returns the
number of objects deleted and a dictionary with the number of deletions per
object type.

For more details, including how to delete objects in bulk, see
[Deleting objects](https://docs.djangoproject.com/en/topics/db/queries/#topics-db-queries-delete).

If you want customized deletion behavior, you can override the `delete()`
method. See [Overriding predefined model methods](https://docs.djangoproject.com/en/topics/db/models/#overriding-model-methods) for more details.

Sometimes with [multi-table inheritance](https://docs.djangoproject.com/en/topics/db/models/#multi-table-inheritance) you may
want to delete only a child model’s data. Specifying `keep_parents=True` will
keep the parent model’s data.

  Changed in Django 4.2:

`adelete()` method was added.

## Pickling objects¶

When you [pickle](https://docs.python.org/3/library/pickle.html#module-pickle) a model, its current state is pickled. When you unpickle
it, it’ll contain the model instance at the moment it was pickled, rather than
the data that’s currently in the database.

You can’t share pickles between versions

Pickles of models are only valid for the version of Django that
was used to generate them. If you generate a pickle using Django
version N, there is no guarantee that pickle will be readable with
Django version N+1. Pickles should not be used as part of a long-term
archival strategy.

Since pickle compatibility errors can be difficult to diagnose, such as
silently corrupted objects, a `RuntimeWarning` is raised when you try to
unpickle a model in a Django version that is different than the one in
which it was pickled.

## Other model instance methods¶

A few object methods have special purposes.

### __str__()¶

   Model.__str__()[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.__str__)[¶](#django.db.models.Model.__str__)

The `__str__()` method is called whenever you call `str()` on an object.
Django uses `str(obj)` in a number of places. Most notably, to display an
object in the Django admin site and as the value inserted into a template when
it displays an object. Thus, you should always return a nice, human-readable
representation of the model from the `__str__()` method.

For example:

```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

### __eq__()¶

   Model.__eq__()[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.__eq__)[¶](#django.db.models.Model.__eq__)

The equality method is defined such that instances with the same primary
key value and the same concrete class are considered equal, except that
instances with a primary key value of `None` aren’t equal to anything except
themselves. For proxy models, concrete class is defined as the model’s first
non-proxy parent; for all other models it’s simply the model’s class.

For example:

```
from django.db import models

class MyModel(models.Model):
    id = models.AutoField(primary_key=True)

class MyProxyModel(MyModel):
    class Meta:
        proxy = True

class MultitableInherited(MyModel):
    pass

# Primary keys compared
MyModel(id=1) == MyModel(id=1)
MyModel(id=1) != MyModel(id=2)
# Primary keys are None
MyModel(id=None) != MyModel(id=None)
# Same instance
instance = MyModel(id=None)
instance == instance
# Proxy model
MyModel(id=1) == MyProxyModel(id=1)
# Multi-table inheritance
MyModel(id=1) != MultitableInherited(id=1)
```

### __hash__()¶

   Model.__hash__()[[source]](https://docs.djangoproject.com/en/_modules/django/db/models/base/#Model.__hash__)[¶](#django.db.models.Model.__hash__)

The `__hash__()` method is based on the instance’s primary key value. It
is effectively `hash(obj.pk)`. If the instance doesn’t have a primary key
value then a `TypeError` will be raised (otherwise the `__hash__()`
method would return different values before and after the instance is
saved, but changing the [__hash__()](https://docs.python.org/3/reference/datamodel.html#object.__hash__) value of an instance is
forbidden in Python.

### get_absolute_url()¶

   Model.get_absolute_url()[¶](#django.db.models.Model.get_absolute_url)

Define a `get_absolute_url()` method to tell Django how to calculate the
canonical URL for an object. To callers, this method should appear to return a
string that can be used to refer to the object over HTTP.

For example:

```
def get_absolute_url(self):
    return "/people/%i/" % self.id
```

While this code is correct and simple, it may not be the most portable way to
to write this kind of method. The [reverse()](https://docs.djangoproject.com/en/5.0/urlresolvers/#django.urls.reverse) function is
usually the best approach.

For example:

```
def get_absolute_url(self):
    from django.urls import reverse

    return reverse("people-detail", kwargs={"pk": self.pk})
```

One place Django uses `get_absolute_url()` is in the admin app. If an object
defines this method, the object-editing page will have a “View on site” link
that will jump you directly to the object’s public view, as given by
`get_absolute_url()`.

Similarly, a couple of other bits of Django, such as the [syndication feed
framework](https://docs.djangoproject.com/en/5.0/contrib/syndication/), use `get_absolute_url()` when it is
defined. If it makes sense for your model’s instances to each have a unique
URL, you should define `get_absolute_url()`.

Warning

You should avoid building the URL from unvalidated user input, in order to
reduce possibilities of link or redirect poisoning:

```
def get_absolute_url(self):
    return "/%s/" % self.name
```

If `self.name` is `'/example.com'` this returns `'//example.com/'`
which, in turn, is a valid schema relative URL but not the expected
`'/%2Fexample.com/'`.

It’s good practice to use `get_absolute_url()` in templates, instead of
hard-coding your objects’ URLs. For example, this template code is bad:

```

<a href="/people/{{ object.id }}/">{{ object.name }}</a>
```

This template code is much better:

```
<a href="{{ object.get_absolute_url }}">{{ object.name }}</a>
```

The logic here is that if you change the URL structure of your objects, even
for something small like correcting a spelling error, you don’t want to have to
track down every place that the URL might be created. Specify it once, in
`get_absolute_url()` and have all your other code call that one place.

Note

The string you return from `get_absolute_url()` **must** contain only
ASCII characters (required by the URI specification, [RFC 3986 Section 2](https://datatracker.ietf.org/doc/html/rfc3986.html#section-2))
and be URL-encoded, if necessary.

Code and templates calling `get_absolute_url()` should be able to use the
result directly without any further processing. You may wish to use the
`django.utils.encoding.iri_to_uri()` function to help with this if you
are using strings containing characters outside the ASCII range.

## Extra instance methods¶

In addition to [save()](#django.db.models.Model.save), [delete()](#django.db.models.Model.delete), a model object
might have some of the following methods:

   Model.get_FOO_display()[¶](#django.db.models.Model.get_FOO_display)

For every field that has [choices](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.choices) set, the
object will have a `get_FOO_display()` method, where `FOO` is the name of
the field. This method returns the “human-readable” value of the field.

For example:

```
from django.db import models

class Person(models.Model):
    SHIRT_SIZES = {
        "S": "Small",
        "M": "Medium",
        "L": "Large",
    }
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=2, choices=SHIRT_SIZES)
```

```
>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
'L'
>>> p.get_shirt_size_display()
'Large'
```

    Model.get_next_by_FOO(***kwargs*)[¶](#django.db.models.Model.get_next_by_FOO)    Model.get_previous_by_FOO(***kwargs*)[¶](#django.db.models.Model.get_previous_by_FOO)

For every [DateField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.DateField) and
[DateTimeField](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.DateTimeField) that does not have [null=True](https://docs.djangoproject.com/en/5.0/ref/fields/#django.db.models.Field.null), the object will have `get_next_by_FOO()` and
`get_previous_by_FOO()` methods, where `FOO` is the name of the field. This
returns the next and previous object with respect to the date field, raising
a [DoesNotExist](https://docs.djangoproject.com/en/5.0/ref/class/#django.db.models.Model.DoesNotExist) exception when appropriate.

Both of these methods will perform their queries using the default
manager for the model. If you need to emulate filtering used by a
custom manager, or want to perform one-off custom filtering, both
methods also accept optional keyword arguments, which should be in the
format described in [Field lookups](https://docs.djangoproject.com/en/5.0/ref/querysets/#field-lookups).

Note that in the case of identical date values, these methods will use the
primary key as a tie-breaker. This guarantees that no records are skipped or
duplicated. That also means you cannot use those methods on unsaved objects.

Overriding extra instance methods

In most cases overriding or inheriting `get_FOO_display()`,
`get_next_by_FOO()`, and `get_previous_by_FOO()` should work as
expected. Since they are added by the metaclass however, it is not
practical to account for all possible inheritance structures. In more
complex cases you should override `Field.contribute_to_class()` to set
the methods you need.

## Other attributes¶

### _state¶

   Model._state[¶](#django.db.models.Model._state)

The `_state` attribute refers to a `ModelState` object that tracks
the lifecycle of the model instance.

The `ModelState` object has two attributes: `adding`, a flag which is
`True` if the model has not been saved to the database yet, and `db`,
a string referring to the database alias the instance was loaded from or
saved to.

Newly instantiated instances have `adding=True` and `db=None`,
since they are yet to be saved. Instances fetched from a `QuerySet`
will have `adding=False` and `db` set to the alias of the associated
database.
