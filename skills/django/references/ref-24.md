# SchemaEditor¶

# SchemaEditor¶

# SchemaEditor¶

   *class*BaseDatabaseSchemaEditor[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor)

Django’s migration system is split into two parts; the logic for calculating
and storing what operations should be run (`django.db.migrations`), and the
database abstraction layer that turns things like “create a model” or
“delete a field” into SQL - which is the job of the `SchemaEditor`.

It’s unlikely that you will want to interact directly with `SchemaEditor` as
a normal developer using Django, but if you want to write your own migration
system, or have more advanced needs, it’s a lot nicer than writing SQL.

Each database backend in Django supplies its own version of `SchemaEditor`,
and it’s always accessible via the `connection.schema_editor()` context
manager:

```
with connection.schema_editor() as schema_editor:
    schema_editor.delete_model(MyModel)
```

It must be used via the context manager as this allows it to manage things
like transactions and deferred SQL (like creating `ForeignKey` constraints).

It exposes all possible operations as methods, that should be called in
the order you wish changes to be applied. Some possible operations or types
of change are not possible on all databases - for example, MyISAM does not
support foreign key constraints.

If you are writing or maintaining a third-party database backend for Django,
you will need to provide a `SchemaEditor` implementation in order to work with
Django’s migration functionality - however, as long as your database is
relatively standard in its use of SQL and relational design, you should be able
to subclass one of the built-in Django `SchemaEditor` classes and tweak the
syntax a little.

## Methods¶

### execute()¶

   BaseDatabaseSchemaEditor.execute(*sql*, *params=()*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.execute)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.execute)

Executes the SQL statement passed in, with parameters if supplied. This
is a wrapper around the normal database cursors that allows capture of the SQL
to a `.sql` file if the user wishes.

### create_model()¶

   BaseDatabaseSchemaEditor.create_model(*model*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.create_model)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.create_model)

Creates a new table in the database for the provided model, along with any
unique constraints or indexes it requires.

### delete_model()¶

   BaseDatabaseSchemaEditor.delete_model(*model*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.delete_model)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.delete_model)

Drops the model’s table in the database along with any unique constraints
or indexes it has.

### add_index()¶

   BaseDatabaseSchemaEditor.add_index(*model*, *index*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.add_index)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.add_index)

Adds `index` to `model`’s table.

### remove_index()¶

   BaseDatabaseSchemaEditor.remove_index(*model*, *index*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.remove_index)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.remove_index)

Removes `index` from `model`’s table.

### rename_index()¶

   BaseDatabaseSchemaEditor.rename_index(*model*, *old_index*, *new_index*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.rename_index)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.rename_index)

Renames `old_index` from `model`’s table to `new_index`.

### add_constraint()¶

   BaseDatabaseSchemaEditor.add_constraint(*model*, *constraint*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.add_constraint)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.add_constraint)

Adds `constraint` to `model`’s table.

### remove_constraint()¶

   BaseDatabaseSchemaEditor.remove_constraint(*model*, *constraint*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.remove_constraint)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.remove_constraint)

Removes `constraint` from `model`’s table.

### alter_unique_together()¶

   BaseDatabaseSchemaEditor.alter_unique_together(*model*, *old_unique_together*, *new_unique_together*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.alter_unique_together)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.alter_unique_together)

Changes a model’s [unique_together](https://docs.djangoproject.com/en/5.0/models/options/#django.db.models.Options.unique_together) value; this
will add or remove unique constraints from the model’s table until they match
the new value.

### alter_index_together()¶

   BaseDatabaseSchemaEditor.alter_index_together(*model*, *old_index_together*, *new_index_together*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.alter_index_together)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.alter_index_together)

Changes a model’s [index_together](https://docs.djangoproject.com/en/5.0/models/options/#django.db.models.Options.index_together) value; this
will add or remove indexes from the model’s table until they match the new
value.

### alter_db_table()¶

   BaseDatabaseSchemaEditor.alter_db_table(*model*, *old_db_table*, *new_db_table*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.alter_db_table)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.alter_db_table)

Renames the model’s table from `old_db_table` to `new_db_table`.

### alter_db_table_comment()¶

  New in Django 4.2.    BaseDatabaseSchemaEditor.alter_db_table_comment(*model*, *old_db_table_comment*, *new_db_table_comment*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.alter_db_table_comment)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.alter_db_table_comment)

Change the `model`’s table comment to `new_db_table_comment`.

### alter_db_tablespace()¶

   BaseDatabaseSchemaEditor.alter_db_tablespace(*model*, *old_db_tablespace*, *new_db_tablespace*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.alter_db_tablespace)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.alter_db_tablespace)

Moves the model’s table from one tablespace to another.

### add_field()¶

   BaseDatabaseSchemaEditor.add_field(*model*, *field*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.add_field)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.add_field)

Adds a column (or sometimes multiple) to the model’s table to represent the
field. This will also add indexes or a unique constraint
if the field has `db_index=True` or `unique=True`.

If the field is a `ManyToManyField` without a value for `through`, instead
of creating a column, it will make a table to represent the relationship. If
`through` is provided, it is a no-op.

If the field is a `ForeignKey`, this will also add the foreign key
constraint to the column.

### remove_field()¶

   BaseDatabaseSchemaEditor.remove_field(*model*, *field*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.remove_field)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.remove_field)

Removes the column(s) representing the field from the model’s table, along
with any unique constraints, foreign key constraints, or indexes caused by
that field.

If the field is a ManyToManyField without a value for `through`, it will
remove the table created to track the relationship. If
`through` is provided, it is a no-op.

### alter_field()¶

   BaseDatabaseSchemaEditor.alter_field(*model*, *old_field*, *new_field*, *strict=False*)[[source]](https://docs.djangoproject.com/en/_modules/django/db/backends/base/schema/#BaseDatabaseSchemaEditor.alter_field)[¶](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.alter_field)

This transforms the field on the model from the old field to the new one. This
includes changing the name of the column (the
[db_column](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.db_column) attribute), changing the type of the
field (if the field class changes), changing the `NULL` status of the field,
adding or removing field-only unique constraints and indexes, changing primary
key, and changing the destination of `ForeignKey` constraints.

The most common transformation this cannot do is transforming a
`ManyToManyField` into a normal Field or vice-versa; Django cannot do this
without losing data, and so it will refuse to do it. Instead,
[remove_field()](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.remove_field) and [add_field()](#django.db.backends.base.schema.BaseDatabaseSchemaEditor.add_field) should be called separately.

If the database has the `supports_combined_alters`, Django will try and
do as many of these in a single database call as possible; otherwise, it will
issue a separate ALTER statement for each change, but will not issue ALTERs
where no change is required.

## Attributes¶

All attributes should be considered read-only unless stated otherwise.

### connection¶

   SchemaEditor.connection[¶](#django.db.backends.base.schema.SchemaEditor.connection)

A connection object to the database. A useful attribute of the connection is
`alias` which can be used to determine the name of the database being
accessed.

This is useful when doing data migrations for [migrations with multiple
databases](https://docs.djangoproject.com/en/howto/writing-migrations/#data-migrations-and-multiple-databases).
