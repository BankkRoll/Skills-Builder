# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

ORM Querying Guide

This page is part of the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).

Previous: [Writing SELECT statements for Inheritance Mappings](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html)   |   Next: [Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html)

# ORM-Enabled INSERT, UPDATE, and DELETE statements

About this Document

This section makes use of ORM mappings first illustrated in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial), shown in the section
[Declaring Mapped Classes](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-declaring-mapped-classes), as well as inheritance
mappings shown in the section [Mapping Class Inheritance Hierarchies](https://docs.sqlalchemy.org/en/20/orm/inheritance.html).

[View the ORM setup for this page](https://docs.sqlalchemy.org/en/20/orm/queryguide/_dml_setup.html).

The [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method, in addition to handling ORM-enabled
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) objects, can also accommodate ORM-enabled
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) objects,
in various ways which are each used to INSERT, UPDATE, or DELETE
many database rows at once.  There is also dialect-specific support
for ORM-enabled “upserts”, which are INSERT statements that automatically
make use of UPDATE for rows that already exist.

The following table summarizes the calling forms that are discussed in this
document:

| ORM Use Case | DML Construct Used | Data is passed using … | Supports RETURNING? | Supports Multi-Table Mappings? |
| --- | --- | --- | --- | --- |
| ORM Bulk INSERT Statements | insert() | List of dictionaries toSession.execute.params | yes | yes |
| ORM Bulk Insert with SQL Expressions | insert() | Session.execute.paramswithInsert.values() | yes | yes |
| ORM Bulk Insert with Per Row SQL Expressions | insert() | List of dictionaries toInsert.values() | yes | no |
| ORM “upsert” Statements | insert() | List of dictionaries toInsert.values() | yes | no |
| ORM Bulk UPDATE by Primary Key | update() | List of dictionaries toSession.execute.params | no | yes |
| ORM UPDATE and DELETE with Custom WHERE Criteria | update(),delete() | keywords toUpdate.values() | yes | partial, with manual steps |

## ORM Bulk INSERT Statements

A [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct can be constructed in terms of an ORM class
and passed to the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method.   A list of parameter
dictionaries sent to the [Session.execute.params](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.params) parameter, separate
from the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) object itself, will invoke **bulk INSERT mode**
for the statement, which essentially means the operation will optimize
as much as possible for many rows:

```
>>> from sqlalchemy import insert
>>> session.execute(
...     insert(User),
...     [
...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
...         {"name": "sandy", "fullname": "Sandy Cheeks"},
...         {"name": "patrick", "fullname": "Patrick Star"},
...         {"name": "squidward", "fullname": "Squidward Tentacles"},
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
...     ],
... )
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] [('spongebob', 'Spongebob Squarepants'), ('sandy', 'Sandy Cheeks'), ('patrick', 'Patrick Star'),
('squidward', 'Squidward Tentacles'), ('ehkrabs', 'Eugene H. Krabs')]
<...>
```

The parameter dictionaries contain key/value pairs which may correspond to ORM
mapped attributes that line up with mapped [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
or [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) declarations, as well as with
[composite](https://docs.sqlalchemy.org/en/20/orm/composites.html#mapper-composite) declarations.   The keys should match
the **ORM mapped attribute name** and **not** the actual database column name,
if these two names happen to be different.

Tip

ORM bulk INSERT **allows each dictionary to have different keys**.
The operation will emit multiple INSERT statements with different VALUES
clauses for each set of keys. This is distinctly different from a Core
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) operation, which as introduced at
[INSERT usually generates the “values” clause automatically](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert-values-clause) only uses the **first** dictionary
in the list to determine a single VALUES clause for all parameter sets.

Changed in version 2.0: Passing an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct to the
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method now invokes a “bulk insert”, which
makes use of the same functionality as the legacy
[Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings) method.  This is a behavior change
compared to the 1.x series where the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) would be interpreted
in a Core-centric way, using column names for value keys; ORM attribute
keys are now accepted.   Core-style functionality is available by passing
the execution option `{"dml_strategy": "raw"}` to the
[Session.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.execution_options) parameter of
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).

### Getting new objects with RETURNING

The bulk ORM insert feature supports INSERT..RETURNING for selected
backends, which can return a [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object that may yield individual
columns back as well as fully constructed ORM objects corresponding
to the newly generated records.    INSERT..RETURNING requires the use of a backend that
supports SQL RETURNING syntax as well as support for [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)
with RETURNING; this feature is available with all
[SQLAlchemy-included](https://docs.sqlalchemy.org/en/20/dialects/index.html#included-dialects) backends
with the exception of MySQL (MariaDB is included).

As an example, we can run the same statement as before, adding use of the
[UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning) method, passing the full `User` entity
as what we’d like to return.  [Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars) is used to allow
iteration of `User` objects:

```
>>> users = session.scalars(
...     insert(User).returning(User),
...     [
...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
...         {"name": "sandy", "fullname": "Sandy Cheeks"},
...         {"name": "patrick", "fullname": "Patrick Star"},
...         {"name": "squidward", "fullname": "Squidward Tentacles"},
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
...     ],
... )
INSERT INTO user_account (name, fullname)
VALUES (?, ?), (?, ?), (?, ?), (?, ?), (?, ?)
RETURNING id, name, fullname, species
[...] ('spongebob', 'Spongebob Squarepants', 'sandy', 'Sandy Cheeks',
'patrick', 'Patrick Star', 'squidward', 'Squidward Tentacles',
'ehkrabs', 'Eugene H. Krabs')
>>> print(users.all())
[User(name='spongebob', fullname='Spongebob Squarepants'),
 User(name='sandy', fullname='Sandy Cheeks'),
 User(name='patrick', fullname='Patrick Star'),
 User(name='squidward', fullname='Squidward Tentacles'),
 User(name='ehkrabs', fullname='Eugene H. Krabs')]
```

In the above example, the rendered SQL takes on the form used by the
[insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) feature as requested by the
SQLite backend, where individual parameter dictionaries are inlined into a
single INSERT statement so that RETURNING may be used.

Changed in version 2.0: The ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) now interprets RETURNING
clauses from [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update), and
even [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) constructs in an ORM context, meaning a mixture
of column expressions and ORM mapped entities may be passed to the
[Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) method which will then be delivered
in the way that ORM results are delivered from constructs such as
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select), including that mapped entities will be delivered
in the result as ORM mapped objects.  Limited support for ORM loader
options such as [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) and [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload)
is also present.

#### Correlating RETURNING records with input data order

When using bulk INSERT with RETURNING, it’s important to note that most
database backends provide no formal guarantee of the order in which the
records from RETURNING are returned, including that there is no guarantee that
their order will correspond to that of the input records.  For applications
that need to ensure RETURNING records can be correlated with input data,
the additional parameter [Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order)
may be specified, which depending on backend may use special INSERT forms
that maintain a token which is used to reorder the returned rows appropriately,
or in some cases, such as in the example below using the SQLite backend,
the operation will INSERT one row at a time:

```
>>> data = [
...     {"name": "pearl", "fullname": "Pearl Krabs"},
...     {"name": "plankton", "fullname": "Plankton"},
...     {"name": "gary", "fullname": "Gary"},
... ]
>>> user_ids = session.scalars(
...     insert(User).returning(User.id, sort_by_parameter_order=True), data
... )
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[... (insertmanyvalues) 1/3 (ordered; batch not supported)] ('pearl', 'Pearl Krabs')
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[insertmanyvalues 2/3 (ordered; batch not supported)] ('plankton', 'Plankton')
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[insertmanyvalues 3/3 (ordered; batch not supported)] ('gary', 'Gary')
>>> for user_id, input_record in zip(user_ids, data):
...     input_record["id"] = user_id
>>> print(data)
[{'name': 'pearl', 'fullname': 'Pearl Krabs', 'id': 6},
{'name': 'plankton', 'fullname': 'Plankton', 'id': 7},
{'name': 'gary', 'fullname': 'Gary', 'id': 8}]
```

Added in version 2.0.10: Added [Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order)
which is implemented within the [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) architecture.

See also

[Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order) - background on approaches
taken to guarantee correspondence between input data and result rows
without significant loss of performance

### Using Heterogeneous Parameter Dictionaries

The ORM bulk insert feature supports lists of parameter dictionaries that are
“heterogeneous”, which basically means “individual dictionaries can have different
keys”.   When this condition is detected,
the ORM will break up the parameter dictionaries into groups corresponding
to each set of keys and batch accordingly into separate INSERT statements:

```
>>> users = session.scalars(
...     insert(User).returning(User),
...     [
...         {
...             "name": "spongebob",
...             "fullname": "Spongebob Squarepants",
...             "species": "Sea Sponge",
...         },
...         {"name": "sandy", "fullname": "Sandy Cheeks", "species": "Squirrel"},
...         {"name": "patrick", "species": "Starfish"},
...         {
...             "name": "squidward",
...             "fullname": "Squidward Tentacles",
...             "species": "Squid",
...         },
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs", "species": "Crab"},
...     ],
... )
INSERT INTO user_account (name, fullname, species)
VALUES (?, ?, ?), (?, ?, ?) RETURNING id, name, fullname, species
[... (insertmanyvalues) 1/1 (unordered)] ('spongebob', 'Spongebob Squarepants', 'Sea Sponge',
'sandy', 'Sandy Cheeks', 'Squirrel')
INSERT INTO user_account (name, species)
VALUES (?, ?) RETURNING id, name, fullname, species
[...] ('patrick', 'Starfish')
INSERT INTO user_account (name, fullname, species)
VALUES (?, ?, ?), (?, ?, ?) RETURNING id, name, fullname, species
[... (insertmanyvalues) 1/1 (unordered)] ('squidward', 'Squidward Tentacles',
'Squid', 'ehkrabs', 'Eugene H. Krabs', 'Crab')
```

In the above example, the five parameter dictionaries passed translated into
three INSERT statements, grouped along the specific sets of keys
in each dictionary while still maintaining row order, i.e.
`("name", "fullname", "species")`, `("name", "species")`, `("name","fullname", "species")`.

### Sending NULL values in ORM bulk INSERT statements

The bulk ORM insert feature draws upon a behavior that is also present
in the legacy “bulk” insert behavior, as well as in the ORM unit of work
overall, which is that rows which contain NULL values are INSERTed using
a statement that does not refer to those columns; the rationale here is so
that backends and schemas which contain server-side INSERT defaults that may
be sensitive to the presence of a NULL value vs. no value present will
produce a server side value as expected.  This default behavior
has the effect of breaking up the bulk inserted batches into more
batches of fewer rows:

```
>>> session.execute(
...     insert(User),
...     [
...         {
...             "name": "name_a",
...             "fullname": "Employee A",
...             "species": "Squid",
...         },
...         {
...             "name": "name_b",
...             "fullname": "Employee B",
...             "species": "Squirrel",
...         },
...         {
...             "name": "name_c",
...             "fullname": "Employee C",
...             "species": None,
...         },
...         {
...             "name": "name_d",
...             "fullname": "Employee D",
...             "species": "Bluefish",
...         },
...     ],
... )
INSERT INTO user_account (name, fullname, species) VALUES (?, ?, ?)
[...] [('name_a', 'Employee A', 'Squid'), ('name_b', 'Employee B', 'Squirrel')]
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('name_c', 'Employee C')
INSERT INTO user_account (name, fullname, species) VALUES (?, ?, ?)
[...] ('name_d', 'Employee D', 'Bluefish')
...
```

Above, the bulk INSERT of four rows is broken into three separate statements,
the second statement reformatted to not refer to the NULL column for the single
parameter dictionary that contains a `None` value.    This default
behavior may be undesirable when many rows in the dataset contain random NULL
values, as it causes the “executemany” operation to be broken into a larger
number of smaller operations; particularly when relying upon
[insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) to reduce the overall number
of statements, this can have a bigger performance impact.

To disable the handling of `None` values in the parameters into separate
batches, pass the execution option `render_nulls=True`; this will cause
all parameter dictionaries to be treated equivalently, assuming the same
set of keys in each dictionary:

```
>>> session.execute(
...     insert(User).execution_options(render_nulls=True),
...     [
...         {
...             "name": "name_a",
...             "fullname": "Employee A",
...             "species": "Squid",
...         },
...         {
...             "name": "name_b",
...             "fullname": "Employee B",
...             "species": "Squirrel",
...         },
...         {
...             "name": "name_c",
...             "fullname": "Employee C",
...             "species": None,
...         },
...         {
...             "name": "name_d",
...             "fullname": "Employee D",
...             "species": "Bluefish",
...         },
...     ],
... )
INSERT INTO user_account (name, fullname, species) VALUES (?, ?, ?)
[...] [('name_a', 'Employee A', 'Squid'), ('name_b', 'Employee B', 'Squirrel'), ('name_c', 'Employee C', None), ('name_d', 'Employee D', 'Bluefish')]
...
```

Above, all parameter dictionaries are sent in a single INSERT batch, including
the `None` value present in the third parameter dictionary.

Added in version 2.0.23: Added the `render_nulls` execution option which
mirrors the behavior of the legacy
[Session.bulk_insert_mappings.render_nulls](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings.params.render_nulls) parameter.

### Bulk INSERT for Joined Table Inheritance

ORM bulk insert builds upon the internal system that is used by the
traditional [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) system in order to emit INSERT statements.  This means
that for an ORM entity that is mapped to multiple tables, typically one which
is mapped using [joined table inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-inheritance), the
bulk INSERT operation will emit an INSERT statement for each table represented
by the mapping, correctly transferring server-generated primary key values
to the table rows that depend upon them.  The RETURNING feature is also supported
here, where the ORM will receive [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) objects for each INSERT
statement executed, and will then “horizontally splice” them together so that
the returned rows include values for all columns inserted:

```
>>> managers = session.scalars(
...     insert(Manager).returning(Manager),
...     [
...         {"name": "sandy", "manager_name": "Sandy Cheeks"},
...         {"name": "ehkrabs", "manager_name": "Eugene H. Krabs"},
...     ],
... )
INSERT INTO employee (name, type) VALUES (?, ?) RETURNING id, name, type
[... (insertmanyvalues) 1/2 (ordered; batch not supported)] ('sandy', 'manager')
INSERT INTO employee (name, type) VALUES (?, ?) RETURNING id, name, type
[insertmanyvalues 2/2 (ordered; batch not supported)] ('ehkrabs', 'manager')
INSERT INTO manager (id, manager_name) VALUES (?, ?), (?, ?) RETURNING id, manager_name, id AS id__1
[... (insertmanyvalues) 1/1 (ordered)] (1, 'Sandy Cheeks', 2, 'Eugene H. Krabs')
```

Tip

Bulk INSERT of joined inheritance mappings requires that the ORM
make use of the [Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order)
parameter internally, so that it can correlate primary key values from
RETURNING rows from the base table into the parameter sets being used
to INSERT into the “sub” table, which is why the SQLite backend
illustrated above transparently degrades to using non-batched statements.
Background on this feature is at
[Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order).

### ORM Bulk Insert with SQL Expressions

The ORM bulk insert feature supports the addition of a fixed set of
parameters which may include SQL expressions to be applied to every target row.
To achieve this, combine the use of the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method,
passing a dictionary of parameters that will be applied to all rows,
with the usual bulk calling form by including a list of parameter dictionaries
that contain individual row values when invoking [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).

As an example, given an ORM mapping that includes a “timestamp” column:

```
import datetime

class LogRecord(Base):
    __tablename__ = "log_record"
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]
    code: Mapped[str]
    timestamp: Mapped[datetime.datetime]
```

If we wanted to INSERT a series of `LogRecord` elements, each with a unique
`message` field, however we would like to apply the SQL function `now()`
to all rows, we can pass `timestamp` within [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values)
and then pass the additional records using “bulk” mode:

```
>>> from sqlalchemy import func
>>> log_record_result = session.scalars(
...     insert(LogRecord).values(code="SQLA", timestamp=func.now()).returning(LogRecord),
...     [
...         {"message": "log message #1"},
...         {"message": "log message #2"},
...         {"message": "log message #3"},
...         {"message": "log message #4"},
...     ],
... )
INSERT INTO log_record (message, code, timestamp)
VALUES (?, ?, CURRENT_TIMESTAMP), (?, ?, CURRENT_TIMESTAMP),
(?, ?, CURRENT_TIMESTAMP), (?, ?, CURRENT_TIMESTAMP)
RETURNING id, message, code, timestamp
[... (insertmanyvalues) 1/1 (unordered)] ('log message #1', 'SQLA', 'log message #2',
'SQLA', 'log message #3', 'SQLA', 'log message #4', 'SQLA')
>>> print(log_record_result.all())
[LogRecord('log message #1', 'SQLA', datetime.datetime(...)),
 LogRecord('log message #2', 'SQLA', datetime.datetime(...)),
 LogRecord('log message #3', 'SQLA', datetime.datetime(...)),
 LogRecord('log message #4', 'SQLA', datetime.datetime(...))]
```

#### ORM Bulk Insert with Per Row SQL Expressions

The [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method itself accommodates a list of parameter
dictionaries directly. When using the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct in this
way, without passing any list of parameter dictionaries to the
[Session.execute.params](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.params) parameter, bulk ORM insert mode is not
used, and instead the INSERT statement is rendered exactly as given and invoked
exactly once. This mode of operation may be useful both for the case of passing
SQL expressions on a per-row basis, and is also used when using “upsert”
statements with the ORM, documented later in this chapter at
[ORM “upsert” Statements](#orm-queryguide-upsert).

A contrived example of an INSERT that embeds per-row SQL expressions,
and also demonstrates [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) in this form, is below:

```
>>> from sqlalchemy import select
>>> address_result = session.scalars(
...     insert(Address)
...     .values(
...         [
...             {
...                 "user_id": select(User.id).where(User.name == "sandy"),
...                 "email_address": "[email protected]",
...             },
...             {
...                 "user_id": select(User.id).where(User.name == "spongebob"),
...                 "email_address": "[email protected]",
...             },
...             {
...                 "user_id": select(User.id).where(User.name == "patrick"),
...                 "email_address": "[email protected]",
...             },
...         ]
...     )
...     .returning(Address),
... )
INSERT INTO address (user_id, email_address) VALUES
((SELECT user_account.id
FROM user_account
WHERE user_account.name = ?), ?), ((SELECT user_account.id
FROM user_account
WHERE user_account.name = ?), ?), ((SELECT user_account.id
FROM user_account
WHERE user_account.name = ?), ?) RETURNING id, user_id, email_address
[...] ('sandy', '[email protected]', 'spongebob', '[email protected]',
'patrick', '[email protected]')
>>> print(address_result.all())
[Address(email_address='[email protected]'),
 Address(email_address='[email protected]'),
 Address(email_address='[email protected]')]
```

Because bulk ORM insert mode is not used above, the following features
are not present:

- [Joined table inheritance](#orm-queryguide-insert-joined-table-inheritance)
  or other multi-table mappings are not supported, since that would require multiple
  INSERT statements.
- [Heterogeneous parameter sets](#orm-queryguide-insert-heterogeneous-params)
  are not supported - each element in the VALUES set must have the same
  columns.
- Core-level scale optimizations such as the batching provided by
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) are not available; statements
  will need to ensure the total number of parameters does not exceed limits
  imposed by the backing database.

For the above reasons, it is generally not recommended to use multiple
parameter sets with [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) with ORM INSERT statements
unless there is a clear rationale, which is either that “upsert” is being used
or there is a need to embed per-row SQL expressions in each parameter set.

See also

[ORM “upsert” Statements](#orm-queryguide-upsert)

### Legacy Session Bulk INSERT Methods

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) includes legacy methods for performing
“bulk” INSERT and UPDATE statements.  These methods share implementations
with the SQLAlchemy 2.0 versions of these features, described
at [ORM Bulk INSERT Statements](#orm-queryguide-bulk-insert) and [ORM Bulk UPDATE by Primary Key](#orm-queryguide-bulk-update),
however lack many features, namely RETURNING support as well as support
for session-synchronization.

Code which makes use of [Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings) for example
can port code as follows, starting with this mappings example:

```
session.bulk_insert_mappings(User, [{"name": "u1"}, {"name": "u2"}, {"name": "u3"}])
```

The above is expressed using the new API as:

```
from sqlalchemy import insert

session.execute(insert(User), [{"name": "u1"}, {"name": "u2"}, {"name": "u3"}])
```

See also

[Legacy Session Bulk UPDATE Methods](#orm-queryguide-legacy-bulk-update)

### ORM “upsert” Statements

Selected backends with SQLAlchemy may include dialect-specific [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
constructs which additionally have the ability to perform “upserts”, or INSERTs
where an existing row in the parameter set is turned into an approximation of
an UPDATE statement instead. By “existing row” , this may mean rows
which share the same primary key value, or may refer to other indexed
columns within the row that are considered to be unique; this is dependent
on the capabilities of the backend in use.

The dialects included with SQLAlchemy that include dialect-specific “upsert”
API features are:

- SQLite - using [Insert](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.Insert) documented at [INSERT…ON CONFLICT (Upsert)](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-on-conflict-insert)
- PostgreSQL - using [Insert](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert) documented at [INSERT…ON CONFLICT (Upsert)](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-insert-on-conflict)
- MySQL/MariaDB - using [Insert](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.Insert) documented at [INSERT…ON DUPLICATE KEY UPDATE (Upsert)](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-insert-on-duplicate-key-update)

Users should review the above sections for background on proper construction
of these objects; in particular, the “upsert” method typically needs to
refer back to the original statement, so the statement is usually constructed
in two separate steps.

Third party backends such as those mentioned at [External Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) may
also feature similar constructs.

While SQLAlchemy does not yet have a backend-agnostic upsert construct, the above
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) variants are nonetheless ORM compatible in that they may be used
in the same way as the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct itself as documented at
[ORM Bulk Insert with Per Row SQL Expressions](#orm-queryguide-insert-values), that is, by embedding the desired rows
to INSERT within the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method.   In the example
below, the SQLite [insert()](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.insert) function is used to generate
an [Insert](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.Insert) construct that includes “ON CONFLICT DO UPDATE”
support.   The statement is then passed to [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) where
it proceeds normally, with the additional characteristic that the
parameter dictionaries passed to [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) are interpreted
as ORM mapped attribute keys, rather than column names:

```
>>> from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
>>> stmt = sqlite_upsert(User).values(
...     [
...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
...         {"name": "sandy", "fullname": "Sandy Cheeks"},
...         {"name": "patrick", "fullname": "Patrick Star"},
...         {"name": "squidward", "fullname": "Squidward Tentacles"},
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
...     ]
... )
>>> stmt = stmt.on_conflict_do_update(
...     index_elements=[User.name], set_=dict(fullname=stmt.excluded.fullname)
... )
>>> session.execute(stmt)
INSERT INTO user_account (name, fullname)
VALUES (?, ?), (?, ?), (?, ?), (?, ?), (?, ?)
ON CONFLICT (name) DO UPDATE SET fullname = excluded.fullname
[...] ('spongebob', 'Spongebob Squarepants', 'sandy', 'Sandy Cheeks',
'patrick', 'Patrick Star', 'squidward', 'Squidward Tentacles',
'ehkrabs', 'Eugene H. Krabs')
<...>
```

#### Using RETURNING with upsert statements

From the SQLAlchemy ORM’s point of view, upsert statements look like regular
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) constructs, which includes that [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning)
works with upsert statements in the same way as was demonstrated at
[ORM Bulk Insert with Per Row SQL Expressions](#orm-queryguide-insert-values), so that any column expression or
relevant ORM entity class may be passed.  Continuing from the
example in the previous section:

```
>>> result = session.scalars(
...     stmt.returning(User), execution_options={"populate_existing": True}
... )
INSERT INTO user_account (name, fullname)
VALUES (?, ?), (?, ?), (?, ?), (?, ?), (?, ?)
ON CONFLICT (name) DO UPDATE SET fullname = excluded.fullname
RETURNING id, name, fullname, species
[...] ('spongebob', 'Spongebob Squarepants', 'sandy', 'Sandy Cheeks',
'patrick', 'Patrick Star', 'squidward', 'Squidward Tentacles',
'ehkrabs', 'Eugene H. Krabs')
>>> print(result.all())
[User(name='spongebob', fullname='Spongebob Squarepants'),
  User(name='sandy', fullname='Sandy Cheeks'),
  User(name='patrick', fullname='Patrick Star'),
  User(name='squidward', fullname='Squidward Tentacles'),
  User(name='ehkrabs', fullname='Eugene H. Krabs')]
```

The example above uses RETURNING to return ORM objects for each row inserted or
upserted by the statement. The example also adds use of the
[Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing) execution option. This option indicates
that `User` objects which are already present
in the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) for rows that already exist should be
**refreshed** with the data from the new row. For a pure [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
statement, this option is not significant, because every row produced is a
brand new primary key identity. However when the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) also
includes “upsert” options, it may also be yielding results from rows that
already exist and therefore may already have a primary key identity represented
in the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s [identity map](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-map).

See also

[Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing)

## ORM Bulk UPDATE by Primary Key

The [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct may be used with
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) in a similar way as the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
statement is used as described at [ORM Bulk INSERT Statements](#orm-queryguide-bulk-insert), passing a
list of many parameter dictionaries, each dictionary representing an individual
row that corresponds to a single primary key value. This use should not be
confused with a more common way to use [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) statements with the
ORM, using an explicit WHERE clause, which is documented at
[ORM UPDATE and DELETE with Custom WHERE Criteria](#orm-queryguide-update-delete-where).

For the “bulk” version of UPDATE, a [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) construct is made in
terms of an ORM class and passed to the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method;
the resulting [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) object should have **no values and typically
no WHERE criteria**, that is, the [Update.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.values) method is not
used, and the [Update.where()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.where) is **usually** not used, but may be
used in the unusual case that additional filtering criteria would be added.

Passing the [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct along with a list of parameter
dictionaries which each include a full primary key value will invoke **bulk
UPDATE by primary key mode** for the statement, generating the appropriate
WHERE criteria to match each row by primary key, and using [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)
to run each parameter set against the UPDATE statement:

```
>>> from sqlalchemy import update
>>> session.execute(
...     update(User),
...     [
...         {"id": 1, "fullname": "Spongebob Squarepants"},
...         {"id": 3, "fullname": "Patrick Star"},
...         {"id": 5, "fullname": "Eugene H. Krabs"},
...     ],
... )
UPDATE user_account SET fullname=? WHERE user_account.id = ?
[...] [('Spongebob Squarepants', 1), ('Patrick Star', 3), ('Eugene H. Krabs', 5)]
<...>
```

Note that each parameter dictionary **must include a full primary key for
each record**, else an error is raised.

Like the bulk INSERT feature, heterogeneous parameter lists are supported here
as well, where the parameters will be grouped into sub-batches of UPDATE
runs.

Changed in version 2.0.11: Additional WHERE criteria can be combined with
[ORM Bulk UPDATE by Primary Key](#orm-queryguide-bulk-update) by using the [Update.where()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.where)
method to add additional criteria.  However this criteria is always in
addition to the WHERE criteria that’s already made present which includes
primary key values.

The RETURNING feature is not available when using the “bulk UPDATE by primary
key” feature; the list of multiple parameter dictionaries necessarily makes use
of DBAPI [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany), which in its usual form does not typically
support result rows.

Changed in version 2.0: Passing an [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct to the
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method along with a list of parameter
dictionaries now invokes a “bulk update”, which makes use of the same
functionality as the legacy [Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings)
method.  This is a behavior change compared to the 1.x series where the
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) would only be supported with explicit WHERE criteria
and inline VALUES.

### Disabling Bulk ORM Update by Primary Key for an UPDATE statement with multiple parameter sets

The ORM Bulk Update by Primary Key feature, which runs an UPDATE statement
per record which includes WHERE criteria for each primary key value, is
automatically used when:

1. the UPDATE statement given is against an ORM entity
2. the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is used to execute the statement, and not a
  Core [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
3. The parameters passed are a **list of dictionaries**.

In order to invoke an UPDATE statement without using “ORM Bulk Update by Primary Key”,
invoke the statement against the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) directly using
the [Session.connection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) method to acquire the current
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) for the transaction:

```
>>> from sqlalchemy import bindparam
>>> session.connection().execute(
...     update(User).where(User.name == bindparam("u_name")),
...     [
...         {"u_name": "spongebob", "fullname": "Spongebob Squarepants"},
...         {"u_name": "patrick", "fullname": "Patrick Star"},
...     ],
... )
UPDATE user_account SET fullname=? WHERE user_account.name = ?
[...] [('Spongebob Squarepants', 'spongebob'), ('Patrick Star', 'patrick')]
<...>
```

See also

[per-row ORM Bulk Update by Primary Key requires that records contain primary key values](https://docs.sqlalchemy.org/en/20/errors.html#error-bupq)

### Bulk UPDATE by Primary Key for Joined Table Inheritance

ORM bulk update has similar behavior to ORM bulk insert when using mappings
with joined table inheritance; as described at
[Bulk INSERT for Joined Table Inheritance](#orm-queryguide-insert-joined-table-inheritance), the bulk UPDATE
operation will emit an UPDATE statement for each table represented in the
mapping, for which the given parameters include values to be updated
(non-affected tables are skipped).

Example:

```
>>> session.execute(
...     update(Manager),
...     [
...         {
...             "id": 1,
...             "name": "scheeks",
...             "manager_name": "Sandy Cheeks, President",
...         },
...         {
...             "id": 2,
...             "name": "eugene",
...             "manager_name": "Eugene H. Krabs, VP Marketing",
...         },
...     ],
... )
UPDATE employee SET name=? WHERE employee.id = ?
[...] [('scheeks', 1), ('eugene', 2)]
UPDATE manager SET manager_name=? WHERE manager.id = ?
[...] [('Sandy Cheeks, President', 1), ('Eugene H. Krabs, VP Marketing', 2)]
<...>
```

### Legacy Session Bulk UPDATE Methods

As discussed at [Legacy Session Bulk INSERT Methods](#orm-queryguide-legacy-bulk-insert), the
[Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings) method of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is
the legacy form of bulk update, which the ORM makes use of internally when
interpreting a [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) statement with primary key parameters given;
however, when using the legacy version, features such as support for
session-synchronization are not included.

The example below:

```
session.bulk_update_mappings(
    User,
    [
        {"id": 1, "name": "scheeks", "manager_name": "Sandy Cheeks, President"},
        {"id": 2, "name": "eugene", "manager_name": "Eugene H. Krabs, VP Marketing"},
    ],
)
```

Is expressed using the new API as:

```
from sqlalchemy import update

session.execute(
    update(User),
    [
        {"id": 1, "name": "scheeks", "manager_name": "Sandy Cheeks, President"},
        {"id": 2, "name": "eugene", "manager_name": "Eugene H. Krabs, VP Marketing"},
    ],
)
```

See also

[Legacy Session Bulk INSERT Methods](#orm-queryguide-legacy-bulk-insert)

## ORM UPDATE and DELETE with Custom WHERE Criteria

The [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) constructs, when constructed
with custom WHERE criteria (that is, using the [Update.where()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.where) and
[Delete.where()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete.where) methods), may be invoked in an ORM context
by passing them to [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), without using
the [Session.execute.params](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.params) parameter. For [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update),
the values to be updated should be passed using [Update.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.values).

This mode of use differs
from the feature described previously at [ORM Bulk UPDATE by Primary Key](#orm-queryguide-bulk-update)
in that the ORM uses the given WHERE clause as is, rather than fixing the
WHERE clause to be by primary key.   This means that the single UPDATE or
DELETE statement can affect many rows at once.

As an example, below an UPDATE is emitted that affects the “fullname”
field of multiple rows

```
>>> from sqlalchemy import update
>>> stmt = (
...     update(User)
...     .where(User.name.in_(["squidward", "sandy"]))
...     .values(fullname="Name starts with S")
... )
>>> session.execute(stmt)
UPDATE user_account SET fullname=? WHERE user_account.name IN (?, ?)
[...] ('Name starts with S', 'squidward', 'sandy')
<...>
```

For a DELETE, an example of deleting rows based on criteria:

```
>>> from sqlalchemy import delete
>>> stmt = delete(User).where(User.name.in_(["squidward", "sandy"]))
>>> session.execute(stmt)
DELETE FROM user_account WHERE user_account.name IN (?, ?)
[...] ('squidward', 'sandy')
<...>
```

Warning

Please read the following section [Important Notes and Caveats for ORM-Enabled Update and Delete](#orm-queryguide-update-delete-caveats)
for important notes regarding how the functionality of ORM-Enabled UPDATE and DELETE
diverges from that of ORM [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) features, such
as using the [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) method to delete individual objects.

### Important Notes and Caveats for ORM-Enabled Update and Delete

The ORM-enabled UPDATE and DELETE features bypass ORM [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work)
automation in favor of being able to emit a single UPDATE or DELETE statement
that matches multiple rows at once without complexity.

- The operations do not offer in-Python cascading of relationships - it is
  assumed that ON UPDATE CASCADE and/or ON DELETE CASCADE is configured for any
  foreign key references which require it, otherwise the database may emit an
  integrity violation if foreign key references are being enforced. See the
  notes at [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes) for some examples.
- After the UPDATE or DELETE, dependent objects in the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) which
  were impacted by an ON UPDATE CASCADE or ON DELETE CASCADE on related tables,
  particularly objects that refer to rows that have now been deleted, may still
  reference those objects.  This issue is resolved once the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  is expired, which normally occurs upon [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) or can be
  forced by using [Session.expire_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire_all).
- ORM-enabled UPDATEs and DELETEs do not handle joined table inheritance
  automatically.   See the section [UPDATE/DELETE with Custom WHERE Criteria for Joined Table Inheritance](#orm-queryguide-update-delete-joined-inh)
  for notes on how to work with joined-inheritance mappings.
- The WHERE criteria needed in order to limit the polymorphic identity to
  specific subclasses for single-table-inheritance mappings **is included
  automatically** .   This only applies to a subclass mapper that has no table of
  its own.
- The [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) option **is supported** by ORM
  update and delete operations; criteria here will be added to that of the UPDATE
  or DELETE statement being emitted, as well as taken into account during the
  “synchronize” process.
- In order to intercept ORM-enabled UPDATE and DELETE operations with event
  handlers, use the [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute) event.

### Selecting a Synchronization Strategy

When making use of [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) or [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) in conjunction
with ORM-enabled execution using [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), additional
ORM-specific functionality is present which will **synchronize** the state
being changed by the statement with that of the objects that are currently
present within the [identity map](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-map) of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
By “synchronize” we mean that UPDATEd attributes will be refreshed with the
new value, or at the very least [expired](https://docs.sqlalchemy.org/en/20/glossary.html#term-expired) so that they will re-populate
with their new value on next access, and DELETEd objects will be
moved into the [deleted](https://docs.sqlalchemy.org/en/20/glossary.html#term-deleted) state.

This synchronization is controllable as the “synchronization strategy”,
which is passed as an string ORM execution option, typically by using the
[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options) dictionary:

```
>>> from sqlalchemy import update
>>> stmt = (
...     update(User).where(User.name == "squidward").values(fullname="Squidward Tentacles")
... )
>>> session.execute(stmt, execution_options={"synchronize_session": False})
UPDATE user_account SET fullname=? WHERE user_account.name = ?
[...] ('Squidward Tentacles', 'squidward')
<...>
```

The execution option may also be bundled with the statement itself using the
[Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options) method:

```
>>> from sqlalchemy import update
>>> stmt = (
...     update(User)
...     .where(User.name == "squidward")
...     .values(fullname="Squidward Tentacles")
...     .execution_options(synchronize_session=False)
... )
>>> session.execute(stmt)
UPDATE user_account SET fullname=? WHERE user_account.name = ?
[...] ('Squidward Tentacles', 'squidward')
<...>
```

The following values for `synchronize_session` are supported:

- `'auto'` - this is the default.   The `'fetch'` strategy will be used on
  backends that support RETURNING, which includes all SQLAlchemy-native drivers
  except for MySQL.   If RETURNING is not supported, the `'evaluate'`
  strategy will be used instead.
- `'fetch'` - Retrieves the primary key identity of affected rows by either
  performing a SELECT before the UPDATE or DELETE, or by using RETURNING if the
  database supports it, so that in-memory objects which are affected by the
  operation can be refreshed with new values (updates) or expunged from the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) (deletes). This synchronization strategy may be used
  even if the given [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) or [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete)
  construct explicitly specifies entities or columns using
  [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning).
  Changed in version 2.0: Explicit [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning) may be
  combined with the `'fetch'` synchronization strategy when using
  ORM-enabled UPDATE and DELETE with WHERE criteria.  The actual statement
  will contain the union of columns between that which the `'fetch'`
  strategy requires and those which were requested.
- `'evaluate'` - This indicates to evaluate the WHERE
  criteria given in the UPDATE or DELETE statement in Python, to locate
  matching objects within the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session). This approach does not add
  any SQL round trips to the operation, and in the absence of RETURNING
  support, may be more efficient. For UPDATE or DELETE statements with complex
  criteria, the `'evaluate'` strategy may not be able to evaluate the
  expression in Python and will raise an error. If this occurs, use the
  `'fetch'` strategy for the operation instead.
  Tip
  If a SQL expression makes use of custom operators using the
  [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) or [custom_op](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.custom_op) feature, the
  [Operators.op.python_impl](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op.params.python_impl) parameter may be used to indicate
  a Python function that will be used by the `"evaluate"` synchronization
  strategy.
  Added in version 2.0.
  Warning
  The `"evaluate"` strategy should be avoided if an UPDATE operation is
  to run on a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) that has many objects which have
  been expired, because it will necessarily need to refresh objects in order
  to test them against the given WHERE criteria, which will emit a SELECT
  for each one.   In this case, and particularly if the backend supports
  RETURNING, the `"fetch"` strategy should be preferred.
- `False` - don’t synchronize the session. This option may be useful
  for backends that don’t support RETURNING where the `"evaluate"` strategy
  is not able to be used.  In this case, the state of objects in the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is unchanged and will not automatically correspond
  to the UPDATE or DELETE statement that was emitted, if such objects
  that would normally correspond to the rows matched are present.

### Using RETURNING with UPDATE/DELETE and Custom WHERE Criteria

The [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning) method is fully compatible with
ORM-enabled UPDATE and DELETE with WHERE criteria.   Full ORM objects
and/or columns may be indicated for RETURNING:

```
>>> from sqlalchemy import update
>>> stmt = (
...     update(User)
...     .where(User.name == "squidward")
...     .values(fullname="Squidward Tentacles")
...     .returning(User)
... )
>>> result = session.scalars(stmt)
UPDATE user_account SET fullname=? WHERE user_account.name = ?
RETURNING id, name, fullname, species
[...] ('Squidward Tentacles', 'squidward')
>>> print(result.all())
[User(name='squidward', fullname='Squidward Tentacles')]
```

The support for RETURNING is also compatible with the `fetch` synchronization
strategy, which also uses RETURNING.  The ORM will organize the columns in
RETURNING appropriately so that the synchronization proceeds as well as that
the returned [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) will contain the requested entities and SQL
columns in their requested order.

Added in version 2.0: [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning) may be used for
ORM enabled UPDATE and DELETE while still retaining full compatibility
with the `fetch` synchronization strategy.

### UPDATE/DELETE with Custom WHERE Criteria for Joined Table Inheritance

The UPDATE/DELETE with WHERE criteria feature, unlike the
[ORM Bulk UPDATE by Primary Key](#orm-queryguide-bulk-update), only emits a single UPDATE or DELETE
statement per call to [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute). This means that when
running an [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) or [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) statement against a
multi-table mapping, such as a subclass in a joined-table inheritance mapping,
the statement must conform to the backend’s current capabilities, which may
include that the backend does not support an UPDATE or DELETE statement that
refers to multiple tables, or may have only limited support for this. This
means that for mappings such as joined inheritance subclasses, the ORM version
of the UPDATE/DELETE with WHERE criteria feature can only be used to a limited
extent or not at all, depending on specifics.

The most straightforward way to emit a multi-row UPDATE statement
for a joined-table subclass is to refer to the sub-table alone.
This means the [Update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct should only refer to attributes
that are local to the subclass table, as in the example below:

```
>>> stmt = (
...     update(Manager)
...     .where(Manager.id == 1)
...     .values(manager_name="Sandy Cheeks, President")
... )
>>> session.execute(stmt)
UPDATE manager SET manager_name=? WHERE manager.id = ?
[...] ('Sandy Cheeks, President', 1)
<...>
```

With the above form, a rudimentary way to refer to the base table in order
to locate rows which will work on any SQL backend is so use a subquery:

```
>>> stmt = (
...     update(Manager)
...     .where(
...         Manager.id
...         == select(Employee.id).where(Employee.name == "sandy").scalar_subquery()
...     )
...     .values(manager_name="Sandy Cheeks, President")
... )
>>> session.execute(stmt)
UPDATE manager SET manager_name=? WHERE manager.id = (SELECT employee.id
FROM employee
WHERE employee.name = ?) RETURNING id
[...] ('Sandy Cheeks, President', 'sandy')
<...>
```

For backends that support UPDATE…FROM, the subquery may be stated instead
as additional plain WHERE criteria, however the criteria between the two
tables must be stated explicitly in some way:

```
>>> stmt = (
...     update(Manager)
...     .where(Manager.id == Employee.id, Employee.name == "sandy")
...     .values(manager_name="Sandy Cheeks, President")
... )
>>> session.execute(stmt)
UPDATE manager SET manager_name=? FROM employee
WHERE manager.id = employee.id AND employee.name = ?
[...] ('Sandy Cheeks, President', 'sandy')
<...>
```

For a DELETE, it’s expected that rows in both the base table and the sub-table
would be DELETEd at the same time.   To DELETE many rows of joined inheritance
objects **without** using cascading foreign keys, emit DELETE for each
table individually:

```
>>> from sqlalchemy import delete
>>> session.execute(delete(Manager).where(Manager.id == 1))
DELETE FROM manager WHERE manager.id = ?
[...] (1,)
<...>
>>> session.execute(delete(Employee).where(Employee.id == 1))
DELETE FROM employee WHERE employee.id = ?
[...] (1,)
<...>
```

Overall, normal [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) processes should be **preferred** for
updating and deleting rows for joined inheritance and other multi-table
mappings, unless there is a performance rationale for using custom WHERE
criteria.

### Legacy Query Methods

The ORM enabled UPDATE/DELETE with WHERE feature was originally part of the
now-legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object, in the [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update)
and [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete) methods.  These methods remain available
and provide a subset of the same functionality as that described at
[ORM UPDATE and DELETE with Custom WHERE Criteria](#orm-queryguide-update-delete-where).  The primary difference is that
the legacy methods don’t provide for explicit RETURNING support.

See also

[Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update)

[Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete)

ORM Querying Guide

Next Query Guide Section: [Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html)
