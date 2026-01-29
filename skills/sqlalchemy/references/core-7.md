# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Insert, Updates, Deletes

INSERT, UPDATE and DELETE statements build on a hierarchy starting
with [UpdateBase](#sqlalchemy.sql.expression.UpdateBase).   The [Insert](#sqlalchemy.sql.expression.Insert) and [Update](#sqlalchemy.sql.expression.Update)
constructs build on the intermediary [ValuesBase](#sqlalchemy.sql.expression.ValuesBase).

## DML Foundational Constructors

Top level “INSERT”, “UPDATE”, “DELETE” constructors.

| Object Name | Description |
| --- | --- |
| delete(table) | ConstructDeleteobject. |
| insert(table) | Construct anInsertobject. |
| update(table) | Construct anUpdateobject. |

   function sqlalchemy.sql.expression.delete(*table:_DMLTableArgument*) → [Delete](#sqlalchemy.sql.expression.Delete)

Construct [Delete](#sqlalchemy.sql.expression.Delete) object.

E.g.:

```
from sqlalchemy import delete

stmt = delete(user_table).where(user_table.c.id == 5)
```

Similar functionality is available via the
[TableClause.delete()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause.delete) method on
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

  Parameters:

**table** – The table to delete rows from.

See also

[Using UPDATE and DELETE Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-core-update-delete) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     function sqlalchemy.sql.expression.insert(*table:_DMLTableArgument*) → [Insert](#sqlalchemy.sql.expression.Insert)

Construct an [Insert](#sqlalchemy.sql.expression.Insert) object.

E.g.:

```
from sqlalchemy import insert

stmt = insert(user_table).values(name="username", fullname="Full Username")
```

Similar functionality is available via the
[TableClause.insert()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause.insert) method on
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

See also

[Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

   Parameters:

- **table** – [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)
  which is the subject of the
  insert.
- **values** – collection of values to be inserted; see
  [Insert.values()](#sqlalchemy.sql.expression.Insert.values)
  for a description of allowed formats here.
  Can be omitted entirely; a [Insert](#sqlalchemy.sql.expression.Insert) construct
  will also dynamically render the VALUES clause at execution time
  based on the parameters passed to [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute).
- **inline** – if True, no attempt will be made to retrieve the
  SQL-generated default values to be provided within the statement;
  in particular,
  this allows SQL expressions to be rendered ‘inline’ within the
  statement without the need to pre-execute them beforehand; for
  backends that support “returning”, this turns off the “implicit
  returning” feature for the statement.

If both [insert.values](#sqlalchemy.sql.expression.insert.params.values) and compile-time bind
parameters are present, the compile-time bind parameters override the
information specified within [insert.values](#sqlalchemy.sql.expression.insert.params.values) on a
per-key basis.

The keys within [Insert.values](#sqlalchemy.sql.expression.Insert.params.values) can be either
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects or their string
identifiers. Each key may reference one of:

- a literal data value (i.e. string, number, etc.);
- a Column object;
- a SELECT statement.

If a `SELECT` statement is specified which references this
`INSERT` statement’s table, the statement will be correlated
against the `INSERT` statement.

See also

[Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     function sqlalchemy.sql.expression.update(*table:_DMLTableArgument*) → [Update](#sqlalchemy.sql.expression.Update)

Construct an [Update](#sqlalchemy.sql.expression.Update) object.

E.g.:

```
from sqlalchemy import update

stmt = (
    update(user_table).where(user_table.c.id == 5).values(name="user #5")
)
```

Similar functionality is available via the
[TableClause.update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause.update) method on
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

  Parameters:

**table** – A [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object representing the database
table to be updated.

See also

[Using UPDATE and DELETE Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-core-update-delete) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

## DML Class Documentation Constructors

Class documentation for the constructors listed at
[DML Foundational Constructors](#dml-foundational-consructors).

| Object Name | Description |
| --- | --- |
| Delete | Represent a DELETE construct. |
| Insert | Represent an INSERT construct. |
| Update | Represent an Update construct. |
| UpdateBase | Form the base forINSERT,UPDATE, andDELETEstatements. |
| ValuesBase | Supplies support forValuesBase.values()to
INSERT and UPDATE constructs. |

   class sqlalchemy.sql.expression.Delete

*inherits from* `sqlalchemy.sql.expression.DMLWhereBase`, [sqlalchemy.sql.expression.UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Represent a DELETE construct.

The [Delete](#sqlalchemy.sql.expression.Delete) object is created using the
[delete()](#sqlalchemy.sql.expression.delete) function.

| Member Name | Description |
| --- | --- |
| where() | Return a new construct with the given expression(s) added to
its WHERE clause, joined to the existing clause via AND, if any. |
| with_dialect_options() | Add dialect options to this INSERT/UPDATE/DELETE object. |
| returning() | Add aRETURNINGor equivalent clause to this statement. |

   method [sqlalchemy.sql.expression.Delete.](#sqlalchemy.sql.expression.Delete)where(**whereclause:_ColumnExpressionArgument[bool]*) → Self

*inherited from the* `DMLWhereBase.where()` *method of* `DMLWhereBase`

Return a new construct with the given expression(s) added to
its WHERE clause, joined to the existing clause via AND, if any.

Both [Update.where()](#sqlalchemy.sql.expression.Update.where) and [Delete.where()](#sqlalchemy.sql.expression.Delete.where)
support multiple-table forms, including database-specific
`UPDATE...FROM` as well as `DELETE..USING`.  For backends that
don’t have multiple-table support, a backend agnostic approach
to using multiple tables is to make use of correlated subqueries.
See the linked tutorial sections below for examples.

See also

[Correlated Updates](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-correlated-updates)

[UPDATE..FROM](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-update-from)

[Multiple Table Deletes](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-multi-table-deletes)

     method [sqlalchemy.sql.expression.Delete.](#sqlalchemy.sql.expression.Delete)with_dialect_options(***opt:Any*) → Self

*inherited from the* [UpdateBase.with_dialect_options()](#sqlalchemy.sql.expression.UpdateBase.with_dialect_options) *method of* [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Add dialect options to this INSERT/UPDATE/DELETE object.

e.g.:

```
upd = table.update().dialect_options(mysql_limit=10)
```

     method [sqlalchemy.sql.expression.Delete.](#sqlalchemy.sql.expression.Delete)returning(**cols:_ColumnsClauseArgument[Any]*, *sort_by_parameter_order:bool=False*, ***_UpdateBase__kw:Any*) → [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

*inherited from the* [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning) *method of* [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Add a [RETURNING](https://docs.sqlalchemy.org/en/20/glossary.html#term-RETURNING) or equivalent clause to this statement.

e.g.:

```
>>> stmt = (
...     table.update()
...     .where(table.c.data == "value")
...     .values(status="X")
...     .returning(table.c.server_flag, table.c.updated_timestamp)
... )
>>> print(stmt)
UPDATE some_table SET status=:status
WHERE some_table.data = :data_1
RETURNING some_table.server_flag, some_table.updated_timestamp
```

The method may be invoked multiple times to add new entries to the
list of expressions to be returned.

Added in version 1.4.0b2: The method may be invoked multiple times to
add new entries to the list of expressions to be returned.

The given collection of column expressions should be derived from the
table that is the target of the INSERT, UPDATE, or DELETE.  While
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects are typical, the elements can also be
expressions:

```
>>> stmt = table.insert().returning(
...     (table.c.first_name + " " + table.c.last_name).label("fullname")
... )
>>> print(stmt)
INSERT INTO some_table (first_name, last_name)
VALUES (:first_name, :last_name)
RETURNING some_table.first_name || :first_name_1 || some_table.last_name AS fullname
```

Upon compilation, a RETURNING clause, or database equivalent,
will be rendered within the statement.   For INSERT and UPDATE,
the values are the newly inserted/updated values.  For DELETE,
the values are those of the rows which were deleted.

Upon execution, the values of the columns to be returned are made
available via the result set and can be iterated using
[CursorResult.fetchone()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.fetchone) and similar.
For DBAPIs which do not
natively support returning values (i.e. cx_oracle), SQLAlchemy will
approximate this behavior at the result level so that a reasonable
amount of behavioral neutrality is provided.

Note that not all databases/DBAPIs
support RETURNING.   For those backends with no support,
an exception is raised upon compilation and/or execution.
For those who do support it, the functionality across backends
varies greatly, including restrictions on executemany()
and other statements which return multiple rows. Please
read the documentation notes for the database in use in
order to determine the availability of RETURNING.

  Parameters:

- ***cols** – series of columns, SQL expressions, or whole tables
  entities to be returned.
- **sort_by_parameter_order** –
  for a batch INSERT that is being
  executed against multiple parameter sets, organize the results of
  RETURNING so that the returned rows correspond to the order of
  parameter sets passed in.  This applies only to an [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)
  execution for supporting dialects and typically makes use of the
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature.
  Added in version 2.0.10.
  See also
  [Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order) - background on
  sorting of RETURNING rows for bulk INSERT (Core level discussion)
  [Correlating RETURNING records with input data order](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert-returning-ordered) - example of
  use with [ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) (ORM level discussion)

See also

[UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) - an alternative method tailored
towards efficient fetching of server-side defaults and triggers
for single-row INSERTs or UPDATEs.

[INSERT…RETURNING](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-insert-returning) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

      class sqlalchemy.sql.expression.Insert

*inherits from* [sqlalchemy.sql.expression.ValuesBase](#sqlalchemy.sql.expression.ValuesBase)

Represent an INSERT construct.

The [Insert](#sqlalchemy.sql.expression.Insert) object is created using the
[insert()](#sqlalchemy.sql.expression.insert) function.

| Member Name | Description |
| --- | --- |
| with_dialect_options() | Add dialect options to this INSERT/UPDATE/DELETE object. |
| values() | Specify a fixed VALUES clause for an INSERT statement, or the SET
clause for an UPDATE. |
| returning() | Add aRETURNINGor equivalent clause to this statement. |
| from_select() | Return a newInsertconstruct which represents
anINSERT...FROMSELECTstatement. |
| inline() | Make thisInsertconstruct “inline” . |
| select | SELECT statement for INSERT .. FROM SELECT |

   method [sqlalchemy.sql.expression.Insert.](#sqlalchemy.sql.expression.Insert)with_dialect_options(***opt:Any*) → Self

*inherited from the* [UpdateBase.with_dialect_options()](#sqlalchemy.sql.expression.UpdateBase.with_dialect_options) *method of* [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Add dialect options to this INSERT/UPDATE/DELETE object.

e.g.:

```
upd = table.update().dialect_options(mysql_limit=10)
```

     method [sqlalchemy.sql.expression.Insert.](#sqlalchemy.sql.expression.Insert)values(**args:_DMLColumnKeyMapping[Any]|Sequence[Any]*, ***kwargs:Any*) → Self

*inherited from the* [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) *method of* [ValuesBase](#sqlalchemy.sql.expression.ValuesBase)

Specify a fixed VALUES clause for an INSERT statement, or the SET
clause for an UPDATE.

Note that the [Insert](#sqlalchemy.sql.expression.Insert) and
[Update](#sqlalchemy.sql.expression.Update)
constructs support
per-execution time formatting of the VALUES and/or SET clauses,
based on the arguments passed to [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute).
However, the [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) method can be used to “fix” a
particular set of parameters into the statement.

Multiple calls to [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) will produce a new
construct, each one with the parameter list modified to include
the new parameters sent.  In the typical case of a single
dictionary of parameters, the newly passed keys will replace
the same keys in the previous construct.  In the case of a list-based
“multiple values” construct, each new list of values is extended
onto the existing list of values.

  Parameters:

- ****kwargs** –
  key value pairs representing the string key
  of a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  mapped to the value to be rendered into the
  VALUES or SET clause:
  ```
  users.insert().values(name="some name")
  users.update().where(users.c.id == 5).values(name="some name")
  ```
- ***args** –
  As an alternative to passing key/value parameters,
  a dictionary, tuple, or list of dictionaries or tuples can be passed
  as a single positional argument in order to form the VALUES or
  SET clause of the statement.  The forms that are accepted vary
  based on whether this is an [Insert](#sqlalchemy.sql.expression.Insert) or an
  [Update](#sqlalchemy.sql.expression.Update) construct.
  For either an [Insert](#sqlalchemy.sql.expression.Insert) or
  [Update](#sqlalchemy.sql.expression.Update)
  construct, a single dictionary can be passed, which works the same as
  that of the kwargs form:
  ```
  users.insert().values({"name": "some name"})
  users.update().values({"name": "some new name"})
  ```
  Also for either form but more typically for the
  [Insert](#sqlalchemy.sql.expression.Insert) construct, a tuple that contains an
  entry for every column in the table is also accepted:
  ```
  users.insert().values((5, "some name"))
  ```
  The [Insert](#sqlalchemy.sql.expression.Insert) construct also supports being
  passed a list of dictionaries or full-table-tuples, which on the
  server will render the less common SQL syntax of “multiple values” -
  this syntax is supported on backends such as SQLite, PostgreSQL,
  MySQL, but not necessarily others:
  ```
  users.insert().values(
      [
          {"name": "some name"},
          {"name": "some other name"},
          {"name": "yet another name"},
      ]
  )
  ```
  The above form would render a multiple VALUES statement similar to:
  ```
  INSERT INTO users (name) VALUES
                  (:name_1),
                  (:name_2),
                  (:name_3)
  ```
  It is essential to note that **passing multiple values is
  NOT the same as using traditional executemany() form**.  The above
  syntax is a **special** syntax not typically used.  To emit an
  INSERT statement against multiple rows, the normal method is
  to pass a multiple values list to the
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute)
  method, which is supported by all database backends and is generally
  more efficient for a very large number of parameters.
  > > See also
  > >
  > >
  > >
  > > [Sending Multiple Parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-multiple-parameters) - an introduction to
  > > the traditional Core method of multiple parameter set
  > > invocation for INSERTs and other statements.
  >
  >
  >
  > The UPDATE construct also supports rendering the SET parameters
  > in a specific order.  For this feature refer to the
  > [Update.ordered_values()](#sqlalchemy.sql.expression.Update.ordered_values) method.
  >
  >
  >
  > > See also
  > >
  > >
  > >
  > > [Update.ordered_values()](#sqlalchemy.sql.expression.Update.ordered_values)

      method [sqlalchemy.sql.expression.Insert.](#sqlalchemy.sql.expression.Insert)returning(**cols:_ColumnsClauseArgument[Any]*, *sort_by_parameter_order:bool=False*, ***_UpdateBase__kw:Any*) → [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

*inherited from the* [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning) *method of* [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Add a [RETURNING](https://docs.sqlalchemy.org/en/20/glossary.html#term-RETURNING) or equivalent clause to this statement.

e.g.:

```
>>> stmt = (
...     table.update()
...     .where(table.c.data == "value")
...     .values(status="X")
...     .returning(table.c.server_flag, table.c.updated_timestamp)
... )
>>> print(stmt)
UPDATE some_table SET status=:status
WHERE some_table.data = :data_1
RETURNING some_table.server_flag, some_table.updated_timestamp
```

The method may be invoked multiple times to add new entries to the
list of expressions to be returned.

Added in version 1.4.0b2: The method may be invoked multiple times to
add new entries to the list of expressions to be returned.

The given collection of column expressions should be derived from the
table that is the target of the INSERT, UPDATE, or DELETE.  While
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects are typical, the elements can also be
expressions:

```
>>> stmt = table.insert().returning(
...     (table.c.first_name + " " + table.c.last_name).label("fullname")
... )
>>> print(stmt)
INSERT INTO some_table (first_name, last_name)
VALUES (:first_name, :last_name)
RETURNING some_table.first_name || :first_name_1 || some_table.last_name AS fullname
```

Upon compilation, a RETURNING clause, or database equivalent,
will be rendered within the statement.   For INSERT and UPDATE,
the values are the newly inserted/updated values.  For DELETE,
the values are those of the rows which were deleted.

Upon execution, the values of the columns to be returned are made
available via the result set and can be iterated using
[CursorResult.fetchone()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.fetchone) and similar.
For DBAPIs which do not
natively support returning values (i.e. cx_oracle), SQLAlchemy will
approximate this behavior at the result level so that a reasonable
amount of behavioral neutrality is provided.

Note that not all databases/DBAPIs
support RETURNING.   For those backends with no support,
an exception is raised upon compilation and/or execution.
For those who do support it, the functionality across backends
varies greatly, including restrictions on executemany()
and other statements which return multiple rows. Please
read the documentation notes for the database in use in
order to determine the availability of RETURNING.

  Parameters:

- ***cols** – series of columns, SQL expressions, or whole tables
  entities to be returned.
- **sort_by_parameter_order** –
  for a batch INSERT that is being
  executed against multiple parameter sets, organize the results of
  RETURNING so that the returned rows correspond to the order of
  parameter sets passed in.  This applies only to an [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)
  execution for supporting dialects and typically makes use of the
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature.
  Added in version 2.0.10.
  See also
  [Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order) - background on
  sorting of RETURNING rows for bulk INSERT (Core level discussion)
  [Correlating RETURNING records with input data order](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert-returning-ordered) - example of
  use with [ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) (ORM level discussion)

See also

[UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) - an alternative method tailored
towards efficient fetching of server-side defaults and triggers
for single-row INSERTs or UPDATEs.

[INSERT…RETURNING](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-insert-returning) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.sql.expression.Insert.](#sqlalchemy.sql.expression.Insert)from_select(*names:Sequence[_DMLColumnArgument]*, *select:Selectable*, *include_defaults:bool=True*) → Self

Return a new [Insert](#sqlalchemy.sql.expression.Insert) construct which represents
an `INSERT...FROM SELECT` statement.

e.g.:

```
sel = select(table1.c.a, table1.c.b).where(table1.c.c > 5)
ins = table2.insert().from_select(["a", "b"], sel)
```

   Parameters:

- **names** – a sequence of string column names or
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  objects representing the target columns.
- **select** – a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct,
  [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
  or other construct which resolves into a
  [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause),
  such as an ORM [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object, etc.  The order of
  columns returned from this FROM clause should correspond to the
  order of columns sent as the `names` parameter;  while this
  is not checked before passing along to the database, the database
  would normally raise an exception if these column lists don’t
  correspond.
- **include_defaults** –
  if True, non-server default values and
  SQL expressions as specified on [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
  (as documented in [Column INSERT/UPDATE Defaults](https://docs.sqlalchemy.org/en/20/core/defaults.html)) not
  otherwise specified in the list of names will be rendered
  into the INSERT and SELECT statements, so that these values are also
  included in the data to be inserted.
  Note
  A Python-side default that uses a Python callable function
  will only be invoked **once** for the whole statement, and **not
  per row**.

      method [sqlalchemy.sql.expression.Insert.](#sqlalchemy.sql.expression.Insert)inline() → Self

Make this [Insert](#sqlalchemy.sql.expression.Insert) construct “inline” .

When set, no attempt will be made to retrieve the
SQL-generated default values to be provided within the statement;
in particular,
this allows SQL expressions to be rendered ‘inline’ within the
statement without the need to pre-execute them beforehand; for
backends that support “returning”, this turns off the “implicit
returning” feature for the statement.

Changed in version 1.4: the [Insert.inline](#sqlalchemy.sql.expression.Insert.params.inline)
parameter
is now superseded by the [Insert.inline()](#sqlalchemy.sql.expression.Insert.inline) method.

     attribute [sqlalchemy.sql.expression.Insert.](#sqlalchemy.sql.expression.Insert)select = None

SELECT statement for INSERT .. FROM SELECT

     class sqlalchemy.sql.expression.Update

*inherits from* `sqlalchemy.sql.expression.DMLWhereBase`, [sqlalchemy.sql.expression.ValuesBase](#sqlalchemy.sql.expression.ValuesBase)

Represent an Update construct.

The [Update](#sqlalchemy.sql.expression.Update) object is created using the
[update()](#sqlalchemy.sql.expression.update) function.

| Member Name | Description |
| --- | --- |
| returning() | Add aRETURNINGor equivalent clause to this statement. |
| where() | Return a new construct with the given expression(s) added to
its WHERE clause, joined to the existing clause via AND, if any. |
| with_dialect_options() | Add dialect options to this INSERT/UPDATE/DELETE object. |
| values() | Specify a fixed VALUES clause for an INSERT statement, or the SET
clause for an UPDATE. |
| inline() | Make thisUpdateconstruct “inline” . |
| ordered_values() | Specify the VALUES clause of this UPDATE statement with an explicit
parameter ordering that will be maintained in the SET clause of the
resulting UPDATE statement. |

   method [sqlalchemy.sql.expression.Update.](#sqlalchemy.sql.expression.Update)returning(**cols:_ColumnsClauseArgument[Any]*, *sort_by_parameter_order:bool=False*, ***_UpdateBase__kw:Any*) → [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

*inherited from the* [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning) *method of* [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Add a [RETURNING](https://docs.sqlalchemy.org/en/20/glossary.html#term-RETURNING) or equivalent clause to this statement.

e.g.:

```
>>> stmt = (
...     table.update()
...     .where(table.c.data == "value")
...     .values(status="X")
...     .returning(table.c.server_flag, table.c.updated_timestamp)
... )
>>> print(stmt)
UPDATE some_table SET status=:status
WHERE some_table.data = :data_1
RETURNING some_table.server_flag, some_table.updated_timestamp
```

The method may be invoked multiple times to add new entries to the
list of expressions to be returned.

Added in version 1.4.0b2: The method may be invoked multiple times to
add new entries to the list of expressions to be returned.

The given collection of column expressions should be derived from the
table that is the target of the INSERT, UPDATE, or DELETE.  While
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects are typical, the elements can also be
expressions:

```
>>> stmt = table.insert().returning(
...     (table.c.first_name + " " + table.c.last_name).label("fullname")
... )
>>> print(stmt)
INSERT INTO some_table (first_name, last_name)
VALUES (:first_name, :last_name)
RETURNING some_table.first_name || :first_name_1 || some_table.last_name AS fullname
```

Upon compilation, a RETURNING clause, or database equivalent,
will be rendered within the statement.   For INSERT and UPDATE,
the values are the newly inserted/updated values.  For DELETE,
the values are those of the rows which were deleted.

Upon execution, the values of the columns to be returned are made
available via the result set and can be iterated using
[CursorResult.fetchone()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.fetchone) and similar.
For DBAPIs which do not
natively support returning values (i.e. cx_oracle), SQLAlchemy will
approximate this behavior at the result level so that a reasonable
amount of behavioral neutrality is provided.

Note that not all databases/DBAPIs
support RETURNING.   For those backends with no support,
an exception is raised upon compilation and/or execution.
For those who do support it, the functionality across backends
varies greatly, including restrictions on executemany()
and other statements which return multiple rows. Please
read the documentation notes for the database in use in
order to determine the availability of RETURNING.

  Parameters:

- ***cols** – series of columns, SQL expressions, or whole tables
  entities to be returned.
- **sort_by_parameter_order** –
  for a batch INSERT that is being
  executed against multiple parameter sets, organize the results of
  RETURNING so that the returned rows correspond to the order of
  parameter sets passed in.  This applies only to an [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)
  execution for supporting dialects and typically makes use of the
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature.
  Added in version 2.0.10.
  See also
  [Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order) - background on
  sorting of RETURNING rows for bulk INSERT (Core level discussion)
  [Correlating RETURNING records with input data order](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert-returning-ordered) - example of
  use with [ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) (ORM level discussion)

See also

[UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) - an alternative method tailored
towards efficient fetching of server-side defaults and triggers
for single-row INSERTs or UPDATEs.

[INSERT…RETURNING](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-insert-returning) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.sql.expression.Update.](#sqlalchemy.sql.expression.Update)where(**whereclause:_ColumnExpressionArgument[bool]*) → Self

*inherited from the* `DMLWhereBase.where()` *method of* `DMLWhereBase`

Return a new construct with the given expression(s) added to
its WHERE clause, joined to the existing clause via AND, if any.

Both [Update.where()](#sqlalchemy.sql.expression.Update.where) and [Delete.where()](#sqlalchemy.sql.expression.Delete.where)
support multiple-table forms, including database-specific
`UPDATE...FROM` as well as `DELETE..USING`.  For backends that
don’t have multiple-table support, a backend agnostic approach
to using multiple tables is to make use of correlated subqueries.
See the linked tutorial sections below for examples.

See also

[Correlated Updates](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-correlated-updates)

[UPDATE..FROM](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-update-from)

[Multiple Table Deletes](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-multi-table-deletes)

     method [sqlalchemy.sql.expression.Update.](#sqlalchemy.sql.expression.Update)with_dialect_options(***opt:Any*) → Self

*inherited from the* [UpdateBase.with_dialect_options()](#sqlalchemy.sql.expression.UpdateBase.with_dialect_options) *method of* [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Add dialect options to this INSERT/UPDATE/DELETE object.

e.g.:

```
upd = table.update().dialect_options(mysql_limit=10)
```

     method [sqlalchemy.sql.expression.Update.](#sqlalchemy.sql.expression.Update)values(**args:_DMLColumnKeyMapping[Any]|Sequence[Any]*, ***kwargs:Any*) → Self

*inherited from the* [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) *method of* [ValuesBase](#sqlalchemy.sql.expression.ValuesBase)

Specify a fixed VALUES clause for an INSERT statement, or the SET
clause for an UPDATE.

Note that the [Insert](#sqlalchemy.sql.expression.Insert) and
[Update](#sqlalchemy.sql.expression.Update)
constructs support
per-execution time formatting of the VALUES and/or SET clauses,
based on the arguments passed to [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute).
However, the [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) method can be used to “fix” a
particular set of parameters into the statement.

Multiple calls to [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) will produce a new
construct, each one with the parameter list modified to include
the new parameters sent.  In the typical case of a single
dictionary of parameters, the newly passed keys will replace
the same keys in the previous construct.  In the case of a list-based
“multiple values” construct, each new list of values is extended
onto the existing list of values.

  Parameters:

- ****kwargs** –
  key value pairs representing the string key
  of a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  mapped to the value to be rendered into the
  VALUES or SET clause:
  ```
  users.insert().values(name="some name")
  users.update().where(users.c.id == 5).values(name="some name")
  ```
- ***args** –
  As an alternative to passing key/value parameters,
  a dictionary, tuple, or list of dictionaries or tuples can be passed
  as a single positional argument in order to form the VALUES or
  SET clause of the statement.  The forms that are accepted vary
  based on whether this is an [Insert](#sqlalchemy.sql.expression.Insert) or an
  [Update](#sqlalchemy.sql.expression.Update) construct.
  For either an [Insert](#sqlalchemy.sql.expression.Insert) or
  [Update](#sqlalchemy.sql.expression.Update)
  construct, a single dictionary can be passed, which works the same as
  that of the kwargs form:
  ```
  users.insert().values({"name": "some name"})
  users.update().values({"name": "some new name"})
  ```
  Also for either form but more typically for the
  [Insert](#sqlalchemy.sql.expression.Insert) construct, a tuple that contains an
  entry for every column in the table is also accepted:
  ```
  users.insert().values((5, "some name"))
  ```
  The [Insert](#sqlalchemy.sql.expression.Insert) construct also supports being
  passed a list of dictionaries or full-table-tuples, which on the
  server will render the less common SQL syntax of “multiple values” -
  this syntax is supported on backends such as SQLite, PostgreSQL,
  MySQL, but not necessarily others:
  ```
  users.insert().values(
      [
          {"name": "some name"},
          {"name": "some other name"},
          {"name": "yet another name"},
      ]
  )
  ```
  The above form would render a multiple VALUES statement similar to:
  ```
  INSERT INTO users (name) VALUES
                  (:name_1),
                  (:name_2),
                  (:name_3)
  ```
  It is essential to note that **passing multiple values is
  NOT the same as using traditional executemany() form**.  The above
  syntax is a **special** syntax not typically used.  To emit an
  INSERT statement against multiple rows, the normal method is
  to pass a multiple values list to the
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute)
  method, which is supported by all database backends and is generally
  more efficient for a very large number of parameters.
  > > See also
  > >
  > >
  > >
  > > [Sending Multiple Parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-multiple-parameters) - an introduction to
  > > the traditional Core method of multiple parameter set
  > > invocation for INSERTs and other statements.
  >
  >
  >
  > The UPDATE construct also supports rendering the SET parameters
  > in a specific order.  For this feature refer to the
  > [Update.ordered_values()](#sqlalchemy.sql.expression.Update.ordered_values) method.
  >
  >
  >
  > > See also
  > >
  > >
  > >
  > > [Update.ordered_values()](#sqlalchemy.sql.expression.Update.ordered_values)

      method [sqlalchemy.sql.expression.Update.](#sqlalchemy.sql.expression.Update)inline() → Self

Make this [Update](#sqlalchemy.sql.expression.Update) construct “inline” .

When set, SQL defaults present on [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
objects via the
`default` keyword will be compiled ‘inline’ into the statement and
not pre-executed.  This means that their values will not be available
in the dictionary returned from
[CursorResult.last_updated_params()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.last_updated_params).

Changed in version 1.4: the [update.inline](#sqlalchemy.sql.expression.update.params.inline)
parameter
is now superseded by the [Update.inline()](#sqlalchemy.sql.expression.Update.inline) method.

     method [sqlalchemy.sql.expression.Update.](#sqlalchemy.sql.expression.Update)ordered_values(**args:Tuple[_DMLColumnArgument,Any]*) → Self

Specify the VALUES clause of this UPDATE statement with an explicit
parameter ordering that will be maintained in the SET clause of the
resulting UPDATE statement.

E.g.:

```
stmt = table.update().ordered_values(("name", "ed"), ("ident", "foo"))
```

See also

[Parameter Ordered Updates](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-parameter-ordered-updates) - full example of the
[Update.ordered_values()](#sqlalchemy.sql.expression.Update.ordered_values) method.

Changed in version 1.4: The [Update.ordered_values()](#sqlalchemy.sql.expression.Update.ordered_values)
method
supersedes the
[update.preserve_parameter_order](#sqlalchemy.sql.expression.update.params.preserve_parameter_order)
parameter, which will be removed in SQLAlchemy 2.0.

      class sqlalchemy.sql.expression.UpdateBase

*inherits from* `sqlalchemy.sql.roles.DMLRole`, [sqlalchemy.sql.expression.HasCTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasCTE), `sqlalchemy.sql.expression.HasCompileState`, `sqlalchemy.sql.expression.DialectKWArgs`, [sqlalchemy.sql.expression.HasPrefixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes), `sqlalchemy.sql.expression.Generative`, `sqlalchemy.sql.expression.ExecutableReturnsRows`, [sqlalchemy.sql.expression.ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Form the base for `INSERT`, `UPDATE`, and `DELETE` statements.

| Member Name | Description |
| --- | --- |
| exported_columns | Return the RETURNING columns as a column collection for this
statement. |
| is_derived_from() | ReturnTrueif thisReturnsRowsis
‘derived’ from the givenFromClause. |
| params() | Set the parameters for the statement. |
| return_defaults() | Make use of aRETURNINGclause for the purpose
of fetching server-side expressions and defaults, for supporting
backends only. |
| returning() | Add aRETURNINGor equivalent clause to this statement. |
| with_dialect_options() | Add dialect options to this INSERT/UPDATE/DELETE object. |
| with_hint() | Add a table hint for a single table to this
INSERT/UPDATE/DELETE statement. |

   property entity_description: Dict[str, Any]

Return a [plugin-enabled](https://docs.sqlalchemy.org/en/20/glossary.html#term-plugin-enabled) description of the table and/or
entity which this DML construct is operating against.

This attribute is generally useful when using the ORM, as an
extended structure which includes information about mapped
entities is returned.  The section [Inspecting entities and columns from ORM-enabled SELECT and DML statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-inspection)
contains more background.

For a Core statement, the structure returned by this accessor
is derived from the `UpdateBase.table` attribute, and
refers to the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) being inserted, updated, or deleted:

```
>>> stmt = insert(user_table)
>>> stmt.entity_description
{
    "name": "user_table",
    "table": Table("user_table", ...)
}
```

Added in version 1.4.33.

See also

[UpdateBase.returning_column_descriptions](#sqlalchemy.sql.expression.UpdateBase.returning_column_descriptions)

[Select.column_descriptions](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.column_descriptions) - entity information for
a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct

[Inspecting entities and columns from ORM-enabled SELECT and DML statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-inspection) - ORM background

     attribute [sqlalchemy.sql.expression.UpdateBase.](#sqlalchemy.sql.expression.UpdateBase)exported_columns

Return the RETURNING columns as a column collection for this
statement.

Added in version 1.4.

     method [sqlalchemy.sql.expression.UpdateBase.](#sqlalchemy.sql.expression.UpdateBase)is_derived_from(*fromclause:FromClause|None*) → bool

Return `True` if this [ReturnsRows](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ReturnsRows) is
‘derived’ from the given [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).

Since these are DMLs, we dont want such statements ever being adapted
so we return False for derives.

    method [sqlalchemy.sql.expression.UpdateBase.](#sqlalchemy.sql.expression.UpdateBase)params(**arg:Any*, ***kw:Any*) → NoReturn

Set the parameters for the statement.

This method raises `NotImplementedError` on the base class,
and is overridden by [ValuesBase](#sqlalchemy.sql.expression.ValuesBase) to provide the
SET/VALUES clause of UPDATE and INSERT.

    method [sqlalchemy.sql.expression.UpdateBase.](#sqlalchemy.sql.expression.UpdateBase)return_defaults(**cols:_DMLColumnArgument*, *supplemental_cols:Iterable[_DMLColumnArgument]|None=None*, *sort_by_parameter_order:bool=False*) → Self

Make use of a [RETURNING](https://docs.sqlalchemy.org/en/20/glossary.html#term-RETURNING) clause for the purpose
of fetching server-side expressions and defaults, for supporting
backends only.

Deep Alchemy

The [UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) method is used by the ORM
for its internal work in fetching newly generated primary key
and server default values, in particular to provide the underlying
implementation of the [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults)
ORM feature as well as to allow RETURNING support with bulk
ORM inserts.  Its behavior is fairly idiosyncratic
and is not really intended for general use.  End users should
stick with using [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning) in order to
add RETURNING clauses to their INSERT, UPDATE and DELETE
statements.

Normally, a single row INSERT statement will automatically populate the
[CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) attribute when executed,
which stores the primary key of the row that was just inserted in the
form of a [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) object with column names as named tuple keys
(and the [Row._mapping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row._mapping) view fully populated as well). The
dialect in use chooses the strategy to use in order to populate this
data; if it was generated using server-side defaults and / or SQL
expressions, dialect-specific approaches such as `cursor.lastrowid`
or `RETURNING` are typically used to acquire the new primary key
value.

However, when the statement is modified by calling
[UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) before executing the statement,
additional behaviors take place **only** for backends that support
RETURNING and for [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects that maintain the
[Table.implicit_returning](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.implicit_returning) parameter at its default value of
`True`. In these cases, when the [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) is returned
from the statement’s execution, not only will
[CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) be populated as always, the
[CursorResult.returned_defaults](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults) attribute will also be
populated with a [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) named-tuple representing the full range
of server generated
values from that single row, including values for any columns that
specify [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) or which make use of
[Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) using a SQL expression.

When invoking INSERT statements with multiple rows using
[insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues), the
[UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) modifier will have the effect of
the [CursorResult.inserted_primary_key_rows](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key_rows) and
[CursorResult.returned_defaults_rows](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults_rows) attributes being
fully populated with lists of [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects representing newly
inserted primary key values as well as newly inserted server generated
values for each row inserted. The
[CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) and
[CursorResult.returned_defaults](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults) attributes will also continue
to be populated with the first row of these two collections.

If the backend does not support RETURNING or the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) in use
has disabled [Table.implicit_returning](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.implicit_returning), then no RETURNING
clause is added and no additional data is fetched, however the
INSERT, UPDATE or DELETE statement proceeds normally.

E.g.:

```
stmt = table.insert().values(data="newdata").return_defaults()

result = connection.execute(stmt)

server_created_at = result.returned_defaults["created_at"]
```

When used against an UPDATE statement
[UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) instead looks for columns that
include [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate) or
[Column.server_onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_onupdate) parameters assigned, when
constructing the columns that will be included in the RETURNING clause
by default if explicit columns were not specified. When used against a
DELETE statement, no columns are included in RETURNING by default, they
instead must be specified explicitly as there are no columns that
normally change values when a DELETE statement proceeds.

Added in version 2.0: [UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) is supported
for DELETE statements also and has been moved from
[ValuesBase](#sqlalchemy.sql.expression.ValuesBase) to [UpdateBase](#sqlalchemy.sql.expression.UpdateBase).

The [UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) method is mutually exclusive
against the [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning) method and errors will be
raised during the SQL compilation process if both are used at the same
time on one statement. The RETURNING clause of the INSERT, UPDATE or
DELETE statement is therefore controlled by only one of these methods
at a time.

The [UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) method differs from
[UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning) in these ways:

1. [UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) method causes the
  [CursorResult.returned_defaults](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults) collection to be populated
  with the first row from the RETURNING result. This attribute is not
  populated when using [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning).
2. [UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) is compatible with existing
  logic used to fetch auto-generated primary key values that are then
  populated into the [CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key)
  attribute. By contrast, using [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning) will
  have the effect of the [CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key)
  attribute being left unpopulated.
3. [UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) can be called against any
  backend. Backends that don’t support RETURNING will skip the usage
  of the feature, rather than raising an exception, *unless* `supplemental_cols` is passed. The return value
  of [CursorResult.returned_defaults](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults) will be `None`
  for backends that don’t support RETURNING or for which the target
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) sets [Table.implicit_returning](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.implicit_returning) to
  `False`.
4. An INSERT statement invoked with executemany() is supported if the
  backend database driver supports the
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)
  feature which is now supported by most SQLAlchemy-included backends.
  When executemany is used, the
  [CursorResult.returned_defaults_rows](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults_rows) and
  [CursorResult.inserted_primary_key_rows](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key_rows) accessors
  will return the inserted defaults and primary keys.
  Added in version 1.4: Added
  [CursorResult.returned_defaults_rows](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults_rows) and
  [CursorResult.inserted_primary_key_rows](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key_rows) accessors.
  In version 2.0, the underlying implementation which fetches and
  populates the data for these attributes was generalized to be
  supported by most backends, whereas in 1.4 they were only
  supported by the `psycopg2` driver.

  Parameters:

- **cols** – optional list of column key names or
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that acts as a filter for those columns that
  will be fetched.
- **supplemental_cols** –
  optional list of RETURNING expressions,
  in the same form as one would pass to the
  [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning) method. When present, the additional
  columns will be included in the RETURNING clause, and the
  [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) object will be “rewound” when returned, so
  that methods like [CursorResult.all()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.all) will return new rows
  mostly as though the statement used [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning)
  directly. However, unlike when using [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning)
  directly, the **order of the columns is undefined**, so can only be
  targeted using names or [Row._mapping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row._mapping) keys; they cannot
  reliably be targeted positionally.
  Added in version 2.0.
- **sort_by_parameter_order** –
  for a batch INSERT that is being
  executed against multiple parameter sets, organize the results of
  RETURNING so that the returned rows correspond to the order of
  parameter sets passed in.  This applies only to an [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)
  execution for supporting dialects and typically makes use of the
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature.
  Added in version 2.0.10.
  See also
  [Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order) - background on
  sorting of RETURNING rows for bulk INSERT

See also

[UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning)

[CursorResult.returned_defaults](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults)

[CursorResult.returned_defaults_rows](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.returned_defaults_rows)

[CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key)

[CursorResult.inserted_primary_key_rows](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key_rows)

     method [sqlalchemy.sql.expression.UpdateBase.](#sqlalchemy.sql.expression.UpdateBase)returning(**cols:_ColumnsClauseArgument[Any]*, *sort_by_parameter_order:bool=False*, ***_UpdateBase__kw:Any*) → [UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Add a [RETURNING](https://docs.sqlalchemy.org/en/20/glossary.html#term-RETURNING) or equivalent clause to this statement.

e.g.:

```
>>> stmt = (
...     table.update()
...     .where(table.c.data == "value")
...     .values(status="X")
...     .returning(table.c.server_flag, table.c.updated_timestamp)
... )
>>> print(stmt)
UPDATE some_table SET status=:status
WHERE some_table.data = :data_1
RETURNING some_table.server_flag, some_table.updated_timestamp
```

The method may be invoked multiple times to add new entries to the
list of expressions to be returned.

Added in version 1.4.0b2: The method may be invoked multiple times to
add new entries to the list of expressions to be returned.

The given collection of column expressions should be derived from the
table that is the target of the INSERT, UPDATE, or DELETE.  While
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects are typical, the elements can also be
expressions:

```
>>> stmt = table.insert().returning(
...     (table.c.first_name + " " + table.c.last_name).label("fullname")
... )
>>> print(stmt)
INSERT INTO some_table (first_name, last_name)
VALUES (:first_name, :last_name)
RETURNING some_table.first_name || :first_name_1 || some_table.last_name AS fullname
```

Upon compilation, a RETURNING clause, or database equivalent,
will be rendered within the statement.   For INSERT and UPDATE,
the values are the newly inserted/updated values.  For DELETE,
the values are those of the rows which were deleted.

Upon execution, the values of the columns to be returned are made
available via the result set and can be iterated using
[CursorResult.fetchone()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.fetchone) and similar.
For DBAPIs which do not
natively support returning values (i.e. cx_oracle), SQLAlchemy will
approximate this behavior at the result level so that a reasonable
amount of behavioral neutrality is provided.

Note that not all databases/DBAPIs
support RETURNING.   For those backends with no support,
an exception is raised upon compilation and/or execution.
For those who do support it, the functionality across backends
varies greatly, including restrictions on executemany()
and other statements which return multiple rows. Please
read the documentation notes for the database in use in
order to determine the availability of RETURNING.

  Parameters:

- ***cols** – series of columns, SQL expressions, or whole tables
  entities to be returned.
- **sort_by_parameter_order** –
  for a batch INSERT that is being
  executed against multiple parameter sets, organize the results of
  RETURNING so that the returned rows correspond to the order of
  parameter sets passed in.  This applies only to an [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)
  execution for supporting dialects and typically makes use of the
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature.
  Added in version 2.0.10.
  See also
  [Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order) - background on
  sorting of RETURNING rows for bulk INSERT (Core level discussion)
  [Correlating RETURNING records with input data order](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert-returning-ordered) - example of
  use with [ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) (ORM level discussion)

See also

[UpdateBase.return_defaults()](#sqlalchemy.sql.expression.UpdateBase.return_defaults) - an alternative method tailored
towards efficient fetching of server-side defaults and triggers
for single-row INSERTs or UPDATEs.

[INSERT…RETURNING](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-insert-returning) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     property returning_column_descriptions: List[Dict[str, Any]]

Return a [plugin-enabled](https://docs.sqlalchemy.org/en/20/glossary.html#term-plugin-enabled) description of the columns
which this DML construct is RETURNING against, in other words
the expressions established as part of [UpdateBase.returning()](#sqlalchemy.sql.expression.UpdateBase.returning).

This attribute is generally useful when using the ORM, as an
extended structure which includes information about mapped
entities is returned.  The section [Inspecting entities and columns from ORM-enabled SELECT and DML statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-inspection)
contains more background.

For a Core statement, the structure returned by this accessor is
derived from the same objects that are returned by the
[UpdateBase.exported_columns](#sqlalchemy.sql.expression.UpdateBase.exported_columns) accessor:

```
>>> stmt = insert(user_table).returning(user_table.c.id, user_table.c.name)
>>> stmt.entity_description
[
    {
        "name": "id",
        "type": Integer,
        "expr": Column("id", Integer(), table=<user>, ...)
    },
    {
        "name": "name",
        "type": String(),
        "expr": Column("name", String(), table=<user>, ...)
    },
]
```

Added in version 1.4.33.

See also

[UpdateBase.entity_description](#sqlalchemy.sql.expression.UpdateBase.entity_description)

[Select.column_descriptions](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.column_descriptions) - entity information for
a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct

[Inspecting entities and columns from ORM-enabled SELECT and DML statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-inspection) - ORM background

     method [sqlalchemy.sql.expression.UpdateBase.](#sqlalchemy.sql.expression.UpdateBase)with_dialect_options(***opt:Any*) → Self

Add dialect options to this INSERT/UPDATE/DELETE object.

e.g.:

```
upd = table.update().dialect_options(mysql_limit=10)
```

     method [sqlalchemy.sql.expression.UpdateBase.](#sqlalchemy.sql.expression.UpdateBase)with_hint(*text:str*, *selectable:_DMLTableArgument|None=None*, *dialect_name:str='*'*) → Self

Add a table hint for a single table to this
INSERT/UPDATE/DELETE statement.

Note

[UpdateBase.with_hint()](#sqlalchemy.sql.expression.UpdateBase.with_hint) currently applies only to
Microsoft SQL Server.  For MySQL INSERT/UPDATE/DELETE hints, use
`UpdateBase.prefix_with()`.

The text of the hint is rendered in the appropriate
location for the database backend in use, relative
to the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that is the subject of this
statement, or optionally to that of the given
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) passed as the `selectable` argument.

The `dialect_name` option will limit the rendering of a particular
hint to a particular backend. Such as, to add a hint
that only takes effect for SQL Server:

```
mytable.insert().with_hint("WITH (PAGLOCK)", dialect_name="mssql")
```

   Parameters:

- **text** – Text of the hint.
- **selectable** – optional [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that specifies
  an element of the FROM clause within an UPDATE or DELETE
  to be the subject of the hint - applies only to certain backends.
- **dialect_name** – defaults to `*`, if specified as the name
  of a particular dialect, will apply these hints only when
  that dialect is in use.

       class sqlalchemy.sql.expression.ValuesBase

*inherits from* [sqlalchemy.sql.expression.UpdateBase](#sqlalchemy.sql.expression.UpdateBase)

Supplies support for [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) to
INSERT and UPDATE constructs.

| Member Name | Description |
| --- | --- |
| select | SELECT statement for INSERT .. FROM SELECT |
| values() | Specify a fixed VALUES clause for an INSERT statement, or the SET
clause for an UPDATE. |

   attribute [sqlalchemy.sql.expression.ValuesBase.](#sqlalchemy.sql.expression.ValuesBase)select: [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)[Any] | None = None

SELECT statement for INSERT .. FROM SELECT

    method [sqlalchemy.sql.expression.ValuesBase.](#sqlalchemy.sql.expression.ValuesBase)values(**args:_DMLColumnKeyMapping[Any]|Sequence[Any]*, ***kwargs:Any*) → Self

Specify a fixed VALUES clause for an INSERT statement, or the SET
clause for an UPDATE.

Note that the [Insert](#sqlalchemy.sql.expression.Insert) and
[Update](#sqlalchemy.sql.expression.Update)
constructs support
per-execution time formatting of the VALUES and/or SET clauses,
based on the arguments passed to [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute).
However, the [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) method can be used to “fix” a
particular set of parameters into the statement.

Multiple calls to [ValuesBase.values()](#sqlalchemy.sql.expression.ValuesBase.values) will produce a new
construct, each one with the parameter list modified to include
the new parameters sent.  In the typical case of a single
dictionary of parameters, the newly passed keys will replace
the same keys in the previous construct.  In the case of a list-based
“multiple values” construct, each new list of values is extended
onto the existing list of values.

  Parameters:

- ****kwargs** –
  key value pairs representing the string key
  of a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  mapped to the value to be rendered into the
  VALUES or SET clause:
  ```
  users.insert().values(name="some name")
  users.update().where(users.c.id == 5).values(name="some name")
  ```
- ***args** –
  As an alternative to passing key/value parameters,
  a dictionary, tuple, or list of dictionaries or tuples can be passed
  as a single positional argument in order to form the VALUES or
  SET clause of the statement.  The forms that are accepted vary
  based on whether this is an [Insert](#sqlalchemy.sql.expression.Insert) or an
  [Update](#sqlalchemy.sql.expression.Update) construct.
  For either an [Insert](#sqlalchemy.sql.expression.Insert) or
  [Update](#sqlalchemy.sql.expression.Update)
  construct, a single dictionary can be passed, which works the same as
  that of the kwargs form:
  ```
  users.insert().values({"name": "some name"})
  users.update().values({"name": "some new name"})
  ```
  Also for either form but more typically for the
  [Insert](#sqlalchemy.sql.expression.Insert) construct, a tuple that contains an
  entry for every column in the table is also accepted:
  ```
  users.insert().values((5, "some name"))
  ```
  The [Insert](#sqlalchemy.sql.expression.Insert) construct also supports being
  passed a list of dictionaries or full-table-tuples, which on the
  server will render the less common SQL syntax of “multiple values” -
  this syntax is supported on backends such as SQLite, PostgreSQL,
  MySQL, but not necessarily others:
  ```
  users.insert().values(
      [
          {"name": "some name"},
          {"name": "some other name"},
          {"name": "yet another name"},
      ]
  )
  ```
  The above form would render a multiple VALUES statement similar to:
  ```
  INSERT INTO users (name) VALUES
                  (:name_1),
                  (:name_2),
                  (:name_3)
  ```
  It is essential to note that **passing multiple values is
  NOT the same as using traditional executemany() form**.  The above
  syntax is a **special** syntax not typically used.  To emit an
  INSERT statement against multiple rows, the normal method is
  to pass a multiple values list to the
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute)
  method, which is supported by all database backends and is generally
  more efficient for a very large number of parameters.
  > > See also
  > >
  > >
  > >
  > > [Sending Multiple Parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-multiple-parameters) - an introduction to
  > > the traditional Core method of multiple parameter set
  > > invocation for INSERTs and other statements.
  >
  >
  >
  > The UPDATE construct also supports rendering the SET parameters
  > in a specific order.  For this feature refer to the
  > [Update.ordered_values()](#sqlalchemy.sql.expression.Update.ordered_values) method.
  >
  >
  >
  > > See also
  > >
  > >
  > >
  > > [Update.ordered_values()](#sqlalchemy.sql.expression.Update.ordered_values)
