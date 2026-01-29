# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Column INSERT/UPDATE Defaults

Column INSERT and UPDATE defaults refer to functions that create a **default
value** for a particular column in a row as an INSERT or UPDATE statement is
proceeding against that row, in the case where **no value was provided to the
INSERT or UPDATE statement for that column**.  That is, if a table has a column
called “timestamp”, and an INSERT statement proceeds which does not include a
value for this column, an INSERT default would create a new value, such as
the current time, that is used as the value to be INSERTed into the “timestamp”
column.  If the statement *does* include a value  for this column, then the
default does *not* take place.

Column defaults can be server-side functions or constant values which are
defined in the database along with the schema in [DDL](https://docs.sqlalchemy.org/en/20/glossary.html#term-DDL), or as SQL
expressions which are rendered directly within an INSERT or UPDATE statement
emitted by SQLAlchemy; they may also be client-side Python functions or
constant values which are invoked by SQLAlchemy before data is passed to the
database.

Note

A column default handler should not be confused with a construct that
intercepts and modifies incoming values for INSERT and UPDATE statements
which *are* provided to the statement as it is invoked.  This is known
as [data marshalling](https://docs.sqlalchemy.org/en/20/glossary.html#term-data-marshalling), where a column value is modified in some way
by the application before being sent to the database.  SQLAlchemy provides
a few means of achieving this which include using [custom datatypes](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator), [SQL execution events](https://docs.sqlalchemy.org/en/20/core/events.html#core-sql-events) and
in the ORM [custom  validators](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#simple-validators) as well as
[attribute events](https://docs.sqlalchemy.org/en/20/orm/events.html#orm-attribute-events).    Column defaults are only
invoked when there is **no value present** for a column in a SQL
[DML](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML) statement.

SQLAlchemy provides an array of features regarding default generation
functions which take place for non-present values during INSERT and UPDATE
statements. Options include:

- Scalar values used as defaults during INSERT and UPDATE operations
- Python functions which execute upon INSERT and UPDATE operations
- SQL expressions which are embedded in INSERT statements (or in some cases execute beforehand)
- SQL expressions which are embedded in UPDATE statements
- Server side default values used during INSERT
- Markers for server-side triggers used during UPDATE

The general rule for all insert/update defaults is that they only take effect
if no value for a particular column is passed as an `execute()` parameter;
otherwise, the given value is used.

## Scalar Defaults

The simplest kind of default is a scalar value used as the default value of a column:

```
Table("mytable", metadata_obj, Column("somecolumn", Integer, default=12))
```

Above, the value “12” will be bound as the column value during an INSERT if no
other value is supplied.

A scalar value may also be associated with an UPDATE statement, though this is
not very common (as UPDATE statements are usually looking for dynamic
defaults):

```
Table("mytable", metadata_obj, Column("somecolumn", Integer, onupdate=25))
```

## Python-Executed Functions

The [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate) keyword arguments also accept Python
functions. These functions are invoked at the time of insert or update if no
other value for that column is supplied, and the value returned is used for
the column’s value. Below illustrates a crude “sequence” that assigns an
incrementing counter to a primary key column:

```
# a function which counts upwards
i = 0

def mydefault():
    global i
    i += 1
    return i

t = Table(
    "mytable",
    metadata_obj,
    Column("id", Integer, primary_key=True, default=mydefault),
)
```

It should be noted that for real “incrementing sequence” behavior, the
built-in capabilities of the database should normally be used, which may
include sequence objects or other autoincrementing capabilities. For primary
key columns, SQLAlchemy will in most cases use these capabilities
automatically. See the API documentation for
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) including the [Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement) flag, as
well as the section on [Sequence](#sqlalchemy.schema.Sequence) later in this
chapter for background on standard primary key generation techniques.

To illustrate onupdate, we assign the Python `datetime` function `now` to
the [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate) attribute:

```
import datetime

t = Table(
    "mytable",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    # define 'last_updated' to be populated with datetime.now()
    Column("last_updated", DateTime, onupdate=datetime.datetime.now),
)
```

When an update statement executes and no value is passed for `last_updated`,
the `datetime.datetime.now()` Python function is executed and its return
value used as the value for `last_updated`. Notice that we provide `now`
as the function itself without calling it (i.e. there are no parenthesis
following) - SQLAlchemy will execute the function at the time the statement
executes.

### Context-Sensitive Default Functions

The Python functions used by [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and
[Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate) may also make use of the current statement’s
context in order to determine a value. The context of a statement is an
internal SQLAlchemy object which contains all information about the statement
being executed, including its source expression, the parameters associated with
it and the cursor. The typical use case for this context with regards to
default generation is to have access to the other values being inserted or
updated on the row. To access the context, provide a function that accepts a
single `context` argument:

```
def mydefault(context):
    return context.get_current_parameters()["counter"] + 12

t = Table(
    "mytable",
    metadata_obj,
    Column("counter", Integer),
    Column("counter_plus_twelve", Integer, default=mydefault, onupdate=mydefault),
)
```

The above default generation function is applied so that it will execute for
all INSERT and UPDATE statements where a value for `counter_plus_twelve` was
otherwise not provided, and the value will be that of whatever value is present
in the execution for the `counter` column, plus the number 12.

For a single statement that is being executed using “executemany” style, e.g.
with multiple parameter sets passed to [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), the
user-defined function is called once for each set of parameters. For the use case of
a multi-valued [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct (e.g. with more than one VALUES
clause set up via the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method), the user-defined function
is also called once for each set of parameters.

When the function is invoked, the special method
[DefaultExecutionContext.get_current_parameters()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultExecutionContext.get_current_parameters) is available from
the context object (an subclass of [DefaultExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultExecutionContext)).  This
method returns a dictionary of column-key to values that represents the
full set of values for the INSERT or UPDATE statement.   In the case of a
multi-valued INSERT construct, the subset of parameters that corresponds to
the individual VALUES clause is isolated from the full parameter dictionary
and returned alone.

Added in version 1.2: Added [DefaultExecutionContext.get_current_parameters()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultExecutionContext.get_current_parameters) method,
which improves upon the still-present
[DefaultExecutionContext.current_parameters](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultExecutionContext.current_parameters) attribute
by offering the service of organizing multiple VALUES clauses
into individual parameter dictionaries.

## Client-Invoked SQL Expressions

The [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate) keywords may
also be passed SQL expressions, which are in most cases rendered inline within the
INSERT or UPDATE statement:

```
t = Table(
    "mytable",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    # define 'create_date' to default to now()
    Column("create_date", DateTime, default=func.now()),
    # define 'key' to pull its default from the 'keyvalues' table
    Column(
        "key",
        String(20),
        default=select(keyvalues.c.key).where(keyvalues.c.type="type1"),
    ),
    # define 'last_modified' to use the current_timestamp SQL function on update
    Column("last_modified", DateTime, onupdate=func.utc_timestamp()),
)
```

Above, the `create_date` column will be populated with the result of the
`now()` SQL function (which, depending on backend, compiles into `NOW()`
or `CURRENT_TIMESTAMP` in most cases) during an INSERT statement, and the
`key` column with the result of a SELECT subquery from another table. The
`last_modified` column will be populated with the value of
the SQL `UTC_TIMESTAMP()` MySQL function when an UPDATE statement is
emitted for this table.

Note

When using SQL functions with the `func` construct, we “call” the
named function, e.g. with parenthesis as in `func.now()`.   This differs
from when we specify a Python callable as a default such as
`datetime.datetime`, where we pass the function itself, but we don’t
invoke it ourselves.   In the case of a SQL function, invoking
`func.now()` returns the SQL expression object that will render the
“NOW” function into the SQL being emitted.

Default and update SQL expressions specified by [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and
[Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate) are invoked explicitly by SQLAlchemy when an
INSERT or UPDATE statement occurs, typically rendered inline within the DML
statement except in certain cases listed below.   This is different than a
“server side” default, which is part of the table’s DDL definition, e.g. as
part of the “CREATE TABLE” statement, which are likely more common.   For
server side defaults, see the next section [Server-invoked DDL-Explicit Default Expressions](#server-defaults).

When a SQL expression indicated by [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) is used with
primary key columns, there are some cases where SQLAlchemy must “pre-execute”
the default generation SQL function, meaning it is invoked in a separate SELECT
statement, and the resulting value is passed as a parameter to the INSERT.
This only occurs for primary key columns for an INSERT statement that is being
asked to return this primary key value, where RETURNING or `cursor.lastrowid`
may not be used.   An [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct that specifies the
[insert.inline](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert.params.inline) flag will always render default expressions
inline.

When the statement is executed with a single set of parameters (that is, it is
not an “executemany” style execution), the returned
[CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) will contain a collection accessible
via [CursorResult.postfetch_cols()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.postfetch_cols) which contains a list of all
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects which had an inline-executed
default. Similarly, all parameters which were bound to the statement, including
all Python and SQL expressions which were pre-executed, are present in the
[CursorResult.last_inserted_params()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.last_inserted_params) or
[CursorResult.last_updated_params()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.last_updated_params) collections on
[CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult). The
[CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) collection contains a list of primary
key values for the row inserted (a list so that single-column and
composite-column primary keys are represented in the same format).

## Server-invoked DDL-Explicit Default Expressions

A variant on the SQL expression default is the [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default), which gets
placed in the CREATE TABLE statement during a [Table.create()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.create) operation:

```
t = Table(
    "test",
    metadata_obj,
    Column("abc", String(20), server_default="abc"),
    Column("created_at", DateTime, server_default=func.sysdate()),
    Column("index_value", Integer, server_default=text("0")),
)
```

A create call for the above table will produce:

```
CREATE TABLE test (
    abc varchar(20) default 'abc',
    created_at datetime default sysdate,
    index_value integer default 0
)
```

The above example illustrates the two typical use cases for [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default),
that of the SQL function (SYSDATE in the above example) as well as a server-side constant
value (the integer “0” in the above example).  It is advisable to use the
[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct for any literal SQL values as opposed to passing the
raw value, as SQLAlchemy does not typically perform any quoting or escaping on
these values.

Like client-generated expressions, [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) can accommodate
SQL expressions in general, however it is expected that these will usually be simple
functions and expressions, and not the more complex cases like an embedded SELECT.

## Marking Implicitly Generated Values, timestamps, and Triggered Columns

Columns which generate a new value on INSERT or UPDATE based on other
server-side database mechanisms, such as database-specific auto-generating
behaviors such as seen with TIMESTAMP columns on some platforms, as well as
custom triggers that invoke upon INSERT or UPDATE to generate a new value,
may be called out using [FetchedValue](#sqlalchemy.schema.FetchedValue) as a marker:

```
from sqlalchemy.schema import FetchedValue

t = Table(
    "test",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("abc", TIMESTAMP, server_default=FetchedValue()),
    Column("def", String(20), server_onupdate=FetchedValue()),
)
```

The [FetchedValue](#sqlalchemy.schema.FetchedValue) indicator does not affect the rendered DDL for the
CREATE TABLE.  Instead, it marks the column as one that will have a new value
populated by the database during the process of an INSERT or UPDATE statement,
and for supporting  databases may be used to indicate that the column should be
part of a RETURNING or OUTPUT clause for the statement.    Tools such as the
SQLAlchemy ORM then make use of this marker in order to know how to get at the
value of the column after such an operation.   In particular, the
`ValuesBase.return_defaults()` method can be used with an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
or [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct to indicate that these values should be
returned.

For details on using [FetchedValue](#sqlalchemy.schema.FetchedValue) with the ORM, see
[Fetching Server-Generated Defaults](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#orm-server-defaults).

Warning

The [Column.server_onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_onupdate) directive
**does not** currently produce MySQL’s
“ON UPDATE CURRENT_TIMESTAMP()” clause.  See
[Rendering ON UPDATE CURRENT TIMESTAMP for MySQL / MariaDB’s explicit_defaults_for_timestamp](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-timestamp-onupdate) for background on how to produce
this clause.

See also

[Fetching Server-Generated Defaults](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#orm-server-defaults)

## Defining Sequences

SQLAlchemy represents database sequences using the
[Sequence](#sqlalchemy.schema.Sequence) object, which is considered to be a
special case of “column default”. It only has an effect on databases which have
explicit support for sequences, which among SQLAlchemy’s included dialects
includes PostgreSQL, Oracle Database, MS SQL Server, and MariaDB.  The
[Sequence](#sqlalchemy.schema.Sequence) object is otherwise ignored.

Tip

In newer database engines, the [Identity](#sqlalchemy.schema.Identity) construct should likely
be preferred vs. [Sequence](#sqlalchemy.schema.Sequence) for generation of integer primary key
values. See the section [Identity Columns (GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY)](#identity-ddl) for background on this
construct.

The [Sequence](#sqlalchemy.schema.Sequence) may be placed on any column as a
“default” generator to be used during INSERT operations, and can also be
configured to fire off during UPDATE operations if desired. It is most
commonly used in conjunction with a single integer primary key column:

```
table = Table(
    "cartitems",
    metadata_obj,
    Column(
        "cart_id",
        Integer,
        Sequence("cart_id_seq", start=1),
        primary_key=True,
    ),
    Column("description", String(40)),
    Column("createdate", DateTime()),
)
```

Where above, the table `cartitems` is associated with a sequence named
`cart_id_seq`.   Emitting [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) for the above
table will include:

```
CREATE SEQUENCE cart_id_seq START WITH 1

CREATE TABLE cartitems (
  cart_id INTEGER NOT NULL,
  description VARCHAR(40),
  createdate TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (cart_id)
)
```

Tip

When using tables with explicit schema names (detailed at
[Specifying the Schema Name](https://docs.sqlalchemy.org/en/20/core/metadata.html#schema-table-schema-name)), the configured schema of the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
is **not** automatically shared by an embedded [Sequence](#sqlalchemy.schema.Sequence), instead,
specify [Sequence.schema](#sqlalchemy.schema.Sequence.params.schema):

```
Sequence("cart_id_seq", start=1, schema="some_schema")
```

The [Sequence](#sqlalchemy.schema.Sequence) may also be made to automatically make use of the
[MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) setting on the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) in use;
see [Associating a Sequence with the MetaData](#sequence-metadata) for background.

When [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) DML constructs are invoked against the `cartitems`
table, without an explicit value passed for the `cart_id` column, the
`cart_id_seq` sequence will be used to generate a value on participating
backends. Typically, the sequence function is embedded in the INSERT statement,
which is combined with RETURNING so that the newly generated value can be
returned to the Python process:

```
INSERT INTO cartitems (cart_id, description, createdate)
VALUES (next_val(cart_id_seq), 'some description', '2015-10-15 12:00:15')
RETURNING cart_id
```

When using [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) to invoke an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct,
newly generated primary key identifiers, including but not limited to those
generated using [Sequence](#sqlalchemy.schema.Sequence), are available from the [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult)
construct using the [CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) attribute.

When the [Sequence](#sqlalchemy.schema.Sequence) is associated with a
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) as its **Python-side** default generator, the
[Sequence](#sqlalchemy.schema.Sequence) will also be subject to “CREATE SEQUENCE” and “DROP
SEQUENCE” DDL when similar DDL is emitted for the owning [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table),
such as when using [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) to generate DDL for a series
of tables.

The [Sequence](#sqlalchemy.schema.Sequence) may also be associated with a
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) construct directly.  This allows the [Sequence](#sqlalchemy.schema.Sequence)
to be used in more than one [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) at a time and also allows the
[MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) parameter to be inherited.  See the section
[Associating a Sequence with the MetaData](#sequence-metadata) for background.

### Associating a Sequence on a SERIAL column

PostgreSQL’s SERIAL datatype is an auto-incrementing type that implies
the implicit creation of a PostgreSQL sequence when CREATE TABLE is emitted.
The [Sequence](#sqlalchemy.schema.Sequence) construct, when indicated for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column),
may indicate that it should not be used in this specific case by specifying
a value of `True` for the [Sequence.optional](#sqlalchemy.schema.Sequence.params.optional) parameter.
This allows the given [Sequence](#sqlalchemy.schema.Sequence) to be used for backends that have no
alternative primary key generation system but to ignore it for backends
such as PostgreSQL which will automatically generate a sequence for a particular
column:

```
table = Table(
    "cartitems",
    metadata_obj,
    Column(
        "cart_id",
        Integer,
        # use an explicit Sequence where available, but not on
        # PostgreSQL where SERIAL will be used
        Sequence("cart_id_seq", start=1, optional=True),
        primary_key=True,
    ),
    Column("description", String(40)),
    Column("createdate", DateTime()),
)
```

In the above example, `CREATE TABLE` for PostgreSQL will make use of the
`SERIAL` datatype for the `cart_id` column, and the `cart_id_seq`
sequence will be ignored.  However on Oracle Database, the `cart_id_seq`
sequence will be created explicitly.

Tip

This particular interaction of SERIAL and SEQUENCE is fairly legacy, and
as in other cases, using [Identity](#sqlalchemy.schema.Identity) instead will simplify the
operation to simply use `IDENTITY` on all supported backends.

### Executing a Sequence Standalone

A SEQUENCE is a first class schema object in SQL and can be used to generate
values independently in the database.   If you have a [Sequence](#sqlalchemy.schema.Sequence)
object, it can be invoked with its “next value” instruction by
passing it directly to a SQL execution method:

```
with my_engine.connect() as conn:
    seq = Sequence("some_sequence", start=1)
    nextid = conn.execute(seq)
```

In order to embed the “next value” function of a [Sequence](#sqlalchemy.schema.Sequence)
inside of a SQL statement like a SELECT or INSERT, use the [Sequence.next_value()](#sqlalchemy.schema.Sequence.next_value)
method, which will render at statement compilation time a SQL function that is
appropriate for the target backend:

```
>>> my_seq = Sequence("some_sequence", start=1)
>>> stmt = select(my_seq.next_value())
>>> print(stmt.compile(dialect=postgresql.dialect()))
SELECT nextval('some_sequence') AS next_value_1
```

### Associating a Sequence with the MetaData

For a [Sequence](#sqlalchemy.schema.Sequence) that is to be associated with arbitrary
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, the [Sequence](#sqlalchemy.schema.Sequence) may be associated with
a particular [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData), using the
[Sequence.metadata](#sqlalchemy.schema.Sequence.params.metadata) parameter:

```
seq = Sequence("my_general_seq", metadata=metadata_obj, start=1)
```

Such a sequence can then be associated with columns in the usual way:

```
table = Table(
    "cartitems",
    metadata_obj,
    seq,
    Column("description", String(40)),
    Column("createdate", DateTime()),
)
```

In the above example, the [Sequence](#sqlalchemy.schema.Sequence) object is treated as an
independent schema construct that can exist on its own or be shared among
tables.

Explicitly associating the [Sequence](#sqlalchemy.schema.Sequence) with [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
allows for the following behaviors:

- The [Sequence](#sqlalchemy.schema.Sequence) will inherit the [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema)
  parameter specified to the target [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData), which
  affects the production of CREATE / DROP DDL as well as how the
  [Sequence.next_value()](#sqlalchemy.schema.Sequence.next_value) function is rendered in SQL statements.
- The [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) and [MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all)
  methods will emit CREATE / DROP for this [Sequence](#sqlalchemy.schema.Sequence),
  even if the [Sequence](#sqlalchemy.schema.Sequence) is not associated with any
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) / [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that’s a member of this
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData).

### Associating a Sequence as the Server Side Default

Note

The following technique is known to work only with the PostgreSQL
database.  It does not work with Oracle Database.

The preceding sections illustrate how to associate a [Sequence](#sqlalchemy.schema.Sequence) with a
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) as the **Python side default generator**:

```
Column(
    "cart_id",
    Integer,
    Sequence("cart_id_seq", metadata=metadata_obj, start=1),
    primary_key=True,
)
```

In the above case, the [Sequence](#sqlalchemy.schema.Sequence) will automatically be subject
to CREATE SEQUENCE / DROP SEQUENCE DDL when the related [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
is subject to CREATE / DROP.  However, the sequence will **not** be present
as the server-side default for the column when CREATE TABLE is emitted.

If we want the sequence to be used as a server-side default,
meaning it takes place even if we emit INSERT commands to the table from
the SQL command line, we can use the [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default)
parameter in conjunction with the value-generation function of the
sequence, available from the [Sequence.next_value()](#sqlalchemy.schema.Sequence.next_value) method.  Below
we illustrate the same [Sequence](#sqlalchemy.schema.Sequence) being associated with the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) both as the Python-side default generator as well as
the server-side default generator:

```
cart_id_seq = Sequence("cart_id_seq", metadata=metadata_obj, start=1)
table = Table(
    "cartitems",
    metadata_obj,
    Column(
        "cart_id",
        Integer,
        cart_id_seq,
        server_default=cart_id_seq.next_value(),
        primary_key=True,
    ),
    Column("description", String(40)),
    Column("createdate", DateTime()),
)
```

or with the ORM:

```
class CartItem(Base):
    __tablename__ = "cartitems"

    cart_id_seq = Sequence("cart_id_seq", metadata=Base.metadata, start=1)
    cart_id = Column(
        Integer, cart_id_seq, server_default=cart_id_seq.next_value(), primary_key=True
    )
    description = Column(String(40))
    createdate = Column(DateTime)
```

When the “CREATE TABLE” statement is emitted, on PostgreSQL it would be
emitted as:

```
CREATE TABLE cartitems (
    cart_id INTEGER DEFAULT nextval('cart_id_seq') NOT NULL,
    description VARCHAR(40),
    createdate TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (cart_id)
)
```

Placement of the [Sequence](#sqlalchemy.schema.Sequence) in both the Python-side and server-side
default generation contexts ensures that the “primary key fetch” logic
works in all cases.  Typically, sequence-enabled databases also support
RETURNING for INSERT statements, which is used automatically by SQLAlchemy
when emitting this statement.  However if RETURNING is not used for a particular
insert, then SQLAlchemy would prefer to “pre-execute” the sequence outside
of the INSERT statement itself, which only works if the sequence is
included as the Python-side default generator function.

The example also associates the [Sequence](#sqlalchemy.schema.Sequence) with the enclosing
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) directly, which again ensures that the [Sequence](#sqlalchemy.schema.Sequence)
is fully associated with the parameters of the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection
including the default schema, if any.

See also

[Sequences/SERIAL/IDENTITY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-sequences) - in the PostgreSQL dialect documentation

[RETURNING Support](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracle-returning) - in the Oracle Database dialect documentation

## Computed Columns (GENERATED ALWAYS AS)

Added in version 1.3.11.

The [Computed](#sqlalchemy.schema.Computed) construct allows a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) to be declared in
DDL as a “GENERATED ALWAYS AS” column, that is, one which has a value that is
computed by the database server.    The construct accepts a SQL expression
typically declared textually using a string or the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct, in
a similar manner as that of [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint).   The SQL expression is
then interpreted by the database server in order to determine the value for the
column within a row.

Example:

```
from sqlalchemy import Table, Column, MetaData, Integer, Computed

metadata_obj = MetaData()

square = Table(
    "square",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("side", Integer),
    Column("area", Integer, Computed("side * side")),
    Column("perimeter", Integer, Computed("4 * side")),
)
```

The DDL for the `square` table when run on a PostgreSQL 12 backend will look
like:

```
CREATE TABLE square (
    id SERIAL NOT NULL,
    side INTEGER,
    area INTEGER GENERATED ALWAYS AS (side * side) STORED,
    perimeter INTEGER GENERATED ALWAYS AS (4 * side) STORED,
    PRIMARY KEY (id)
)
```

Whether the value is persisted upon INSERT and UPDATE, or if it is calculated
on fetch, is an implementation detail of the database; the former is known as
“stored” and the latter is known as “virtual”.  Some database implementations
support both, but some only support one or the other.  The optional
[Computed.persisted](#sqlalchemy.schema.Computed.params.persisted) flag may be specified as `True` or `False`
to indicate if the “STORED” or “VIRTUAL” keyword should be rendered in DDL,
however this will raise an error if the keyword is not supported by the target
backend; leaving it unset will use  a working default for the target backend.

The [Computed](#sqlalchemy.schema.Computed) construct is a subclass of the [FetchedValue](#sqlalchemy.schema.FetchedValue)
object, and will set itself up as both the “server default” and “server
onupdate” generator for the target [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), meaning it will be treated
as a default generating column when INSERT and UPDATE statements are generated,
as well as that it will be fetched as a generating column when using the ORM.
This includes that it will be part of the RETURNING clause of the database
for databases which support RETURNING and the generated values are to be
eagerly fetched.

Note

A [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that is defined with the [Computed](#sqlalchemy.schema.Computed)
construct may not store any value outside of that which the server applies
to it;  SQLAlchemy’s behavior when a value is passed for such a column
to be written in INSERT or UPDATE is currently that the value will be
ignored.

“GENERATED ALWAYS AS” is currently known to be supported by:

- MySQL version 5.7 and onwards
- MariaDB 10.x series and onwards
- PostgreSQL as of version 12
- Oracle Database - with the caveat that RETURNING does not work correctly with
  UPDATE (a warning will be emitted to this effect when the UPDATE..RETURNING
  that includes a computed column is rendered)
- Microsoft SQL Server
- SQLite as of version 3.31

When [Computed](#sqlalchemy.schema.Computed) is used with an unsupported backend, if the target
dialect does not support it, a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) is raised when attempting
to render the construct.  Otherwise, if the dialect supports it but the
particular database server version in use does not, then a subclass of
[DBAPIError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DBAPIError), usually [OperationalError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.OperationalError), is raised when the
DDL is emitted to the database.

See also

[Computed](#sqlalchemy.schema.Computed)

## Identity Columns (GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY)

Added in version 1.4.

The [Identity](#sqlalchemy.schema.Identity) construct allows a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) to be declared
as an identity column and rendered in DDL as “GENERATED { ALWAYS | BY DEFAULT }
AS IDENTITY”.  An identity column has its value automatically generated by the
database server using an incrementing (or decrementing) sequence. The construct
shares most of its option to control the database behaviour with
[Sequence](#sqlalchemy.schema.Sequence).

Example:

```
from sqlalchemy import Table, Column, MetaData, Integer, Identity, String

metadata_obj = MetaData()

data = Table(
    "data",
    metadata_obj,
    Column("id", Integer, Identity(start=42, cycle=True), primary_key=True),
    Column("data", String),
)
```

The DDL for the `data` table when run on a PostgreSQL 12 backend will look
like:

```
CREATE TABLE data (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 42 CYCLE) NOT NULL,
    data VARCHAR,
    PRIMARY KEY (id)
)
```

The database will generate a value for the `id` column upon insert,
starting from `42`, if the statement did not already contain a value for
the `id` column.
An identity column can also require that the database generates the value
of the column, ignoring the value passed with the statement or raising an
error, depending on the backend. To activate this mode, set the parameter
[Identity.always](#sqlalchemy.schema.Identity.params.always) to `True` in the
[Identity](#sqlalchemy.schema.Identity) construct. Updating the previous
example to include this parameter will generate the following DDL:

```
CREATE TABLE data (
    id INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 42 CYCLE) NOT NULL,
    data VARCHAR,
    PRIMARY KEY (id)
)
```

The [Identity](#sqlalchemy.schema.Identity) construct is a subclass of the [FetchedValue](#sqlalchemy.schema.FetchedValue)
object, and will set itself up as the “server default” generator for the
target [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), meaning it will be treated
as a default generating column when INSERT statements are generated,
as well as that it will be fetched as a generating column when using the ORM.
This includes that it will be part of the RETURNING clause of the database
for databases which support RETURNING and the generated values are to be
eagerly fetched.

The [Identity](#sqlalchemy.schema.Identity) construct is currently known to be supported by:

- PostgreSQL as of version 10.
- Oracle Database as of version 12. It also supports passing `always=None` to
  enable the default generated mode and the parameter `on_null=True` to
  specify “ON NULL” in conjunction with a “BY DEFAULT” identity column.
- Microsoft SQL Server. MSSQL uses a custom syntax that only supports the
  `start` and `increment` parameters, and ignores all other.

When [Identity](#sqlalchemy.schema.Identity) is used with an unsupported backend, it is ignored,
and the default SQLAlchemy logic for autoincrementing columns is used.

An error is raised when a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) specifies both an
[Identity](#sqlalchemy.schema.Identity) and also sets [Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement)
to `False`.

See also

[Identity](#sqlalchemy.schema.Identity)

## Default Objects API

| Object Name | Description |
| --- | --- |
| ColumnDefault | A plain default value on a column. |
| Computed | Defines a generated column, i.e. “GENERATED ALWAYS AS” syntax. |
| DefaultClause | A DDL-specified DEFAULT column value. |
| DefaultGenerator | Base class for columndefaultvalues. |
| FetchedValue | A marker for a transparent database-side default. |
| Identity | Defines an identity column, i.e. “GENERATED { ALWAYS | BY DEFAULT }
AS IDENTITY” syntax. |
| Sequence | Represents a named database sequence. |

   class sqlalchemy.schema.Computed

*inherits from* [sqlalchemy.schema.FetchedValue](#sqlalchemy.schema.FetchedValue), [sqlalchemy.schema.SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Defines a generated column, i.e. “GENERATED ALWAYS AS” syntax.

The [Computed](#sqlalchemy.schema.Computed) construct is an inline construct added to the
argument list of a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object:

```
from sqlalchemy import Computed

Table(
    "square",
    metadata_obj,
    Column("side", Float, nullable=False),
    Column("area", Float, Computed("side * side")),
)
```

See the linked documentation below for complete details.

Added in version 1.3.11.

See also

[Computed Columns (GENERATED ALWAYS AS)](#computed-ddl)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a GENERATED ALWAYS AS DDL construct to accompany aColumn. |
| copy() |  |

   method [sqlalchemy.schema.Computed.](#sqlalchemy.schema.Computed)__init__(*sqltext:_DDLColumnArgument*, *persisted:bool|None=None*) → None

Construct a GENERATED ALWAYS AS DDL construct to accompany a
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

  Parameters:

- **sqltext** – A string containing the column generation expression, which will be
  used verbatim, or a SQL expression construct, such as a
  [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
  object.   If given as a string, the object is converted to a
  [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) object.
- **persisted** –
  Optional, controls how this column should be persisted by the
  database.   Possible values are:
  - `None`, the default, it will use the default persistence
    defined by the database.
  - `True`, will render `GENERATED ALWAYS AS ... STORED`, or the
    equivalent for the target database if supported.
  - `False`, will render `GENERATED ALWAYS AS ... VIRTUAL`, or
    the equivalent for the target database if supported.
  Specifying `True` or `False` may raise an error when the DDL
  is emitted to the target database if the database does not support
  that persistence option.   Leaving this parameter at its default
  of `None` is guaranteed to succeed for all databases that support
  `GENERATED ALWAYS AS`.

      method [sqlalchemy.schema.Computed.](#sqlalchemy.schema.Computed)copy(***, *target_table:Table|None=None*, ***kw:Any*) → [Computed](#sqlalchemy.schema.Computed)

Deprecated since version 1.4: The [Computed.copy()](#sqlalchemy.schema.Computed.copy) method is deprecated and will be removed in a future release.

      class sqlalchemy.schema.ColumnDefault

*inherits from* [sqlalchemy.schema.DefaultGenerator](#sqlalchemy.schema.DefaultGenerator), `abc.ABC`

A plain default value on a column.

This could correspond to a constant, a callable function,
or a SQL clause.

[ColumnDefault](#sqlalchemy.schema.ColumnDefault) is generated automatically
whenever the `default`, `onupdate` arguments of
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) are used.  A [ColumnDefault](#sqlalchemy.schema.ColumnDefault)
can be passed positionally as well.

For example, the following:

```
Column("foo", Integer, default=50)
```

Is equivalent to:

```
Column("foo", Integer, ColumnDefault(50))
```

     class sqlalchemy.schema.DefaultClause

*inherits from* [sqlalchemy.schema.FetchedValue](#sqlalchemy.schema.FetchedValue)

A DDL-specified DEFAULT column value.

[DefaultClause](#sqlalchemy.schema.DefaultClause) is a [FetchedValue](#sqlalchemy.schema.FetchedValue)
that also generates a “DEFAULT” clause when
“CREATE TABLE” is emitted.

[DefaultClause](#sqlalchemy.schema.DefaultClause) is generated automatically
whenever the `server_default`, `server_onupdate` arguments of
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) are used.  A [DefaultClause](#sqlalchemy.schema.DefaultClause)
can be passed positionally as well.

For example, the following:

```
Column("foo", Integer, server_default="50")
```

Is equivalent to:

```
Column("foo", Integer, DefaultClause("50"))
```

     class sqlalchemy.schema.DefaultGenerator

*inherits from* [sqlalchemy.sql.expression.Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable), [sqlalchemy.schema.SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Base class for column *default* values.

This object is only present on column.default or column.onupdate.
It’s not valid as a server default.

    class sqlalchemy.schema.FetchedValue

*inherits from* `sqlalchemy.sql.expression.SchemaEventTarget`

A marker for a transparent database-side default.

Use [FetchedValue](#sqlalchemy.schema.FetchedValue) when the database is configured
to provide some automatic default for a column.

E.g.:

```
Column("foo", Integer, FetchedValue())
```

Would indicate that some trigger or default generator
will create a new value for the `foo` column during an
INSERT.

See also

[Marking Implicitly Generated Values, timestamps, and Triggered Columns](#triggered-columns)

     class sqlalchemy.schema.Sequence

*inherits from* `sqlalchemy.schema.HasSchemaAttr`, `sqlalchemy.schema.IdentityOptions`, [sqlalchemy.schema.DefaultGenerator](#sqlalchemy.schema.DefaultGenerator)

Represents a named database sequence.

The [Sequence](#sqlalchemy.schema.Sequence) object represents the name and configurational
parameters of a database sequence.   It also represents
a construct that can be “executed” by a SQLAlchemy [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
or [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection),
rendering the appropriate “next value” function
for the target database and returning a result.

The [Sequence](#sqlalchemy.schema.Sequence) is typically associated with a primary key column:

```
some_table = Table(
    "some_table",
    metadata,
    Column(
        "id",
        Integer,
        Sequence("some_table_seq", start=1),
        primary_key=True,
    ),
)
```

When CREATE TABLE is emitted for the above [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), if the
target platform supports sequences, a CREATE SEQUENCE statement will
be emitted as well.   For platforms that don’t support sequences,
the [Sequence](#sqlalchemy.schema.Sequence) construct is ignored.

See also

[Defining Sequences](#defaults-sequences)

[CreateSequence](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateSequence)

[DropSequence](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropSequence)

| Member Name | Description |
| --- | --- |
| __init__() | Construct aSequenceobject. |
| create() | Creates this sequence in the database. |
| drop() | Drops this sequence from the database. |
| next_value() | Return anext_valuefunction element
which will render the appropriate increment function
for thisSequencewithin any SQL expression. |

   method [sqlalchemy.schema.Sequence.](#sqlalchemy.schema.Sequence)__init__(*name:str*, *start:int|None=None*, *increment:int|None=None*, *minvalue:int|None=None*, *maxvalue:int|None=None*, *nominvalue:bool|None=None*, *nomaxvalue:bool|None=None*, *cycle:bool|None=None*, *schema:str|Literal[SchemaConst.BLANK_SCHEMA]|None=None*, *cache:int|None=None*, *order:bool|None=None*, *data_type:_TypeEngineArgument[int]|None=None*, *optional:bool=False*, *quote:bool|None=None*, *metadata:MetaData|None=None*, *quote_schema:bool|None=None*, *for_update:bool=False*) → None

Construct a [Sequence](#sqlalchemy.schema.Sequence) object.

  Parameters:

- **name** – the name of the sequence.
- **start** –
  the starting index of the sequence.  This value is
  used when the CREATE SEQUENCE command is emitted to the database
  as the value of the “START WITH” clause. If `None`, the
  clause is omitted, which on most platforms indicates a starting
  value of 1.
  Changed in version 2.0: The [Sequence.start](#sqlalchemy.schema.Sequence.params.start) parameter
  is required in order to have DDL emit “START WITH”.  This is a
  reversal of a change made in version 1.4 which would implicitly
  render “START WITH 1” if the [Sequence.start](#sqlalchemy.schema.Sequence.params.start) were
  not included.  See [The Sequence construct reverts to not having any explicit default “start” value; impacts MS SQL Server](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7211) for more detail.
- **increment** – the increment value of the sequence.  This
  value is used when the CREATE SEQUENCE command is emitted to
  the database as the value of the “INCREMENT BY” clause.  If `None`,
  the clause is omitted, which on most platforms indicates an
  increment of 1.
- **minvalue** – the minimum value of the sequence.  This
  value is used when the CREATE SEQUENCE command is emitted to
  the database as the value of the “MINVALUE” clause.  If `None`,
  the clause is omitted, which on most platforms indicates a
  minvalue of 1 and -2^63-1 for ascending and descending sequences,
  respectively.
- **maxvalue** – the maximum value of the sequence.  This
  value is used when the CREATE SEQUENCE command is emitted to
  the database as the value of the “MAXVALUE” clause.  If `None`,
  the clause is omitted, which on most platforms indicates a
  maxvalue of 2^63-1 and -1 for ascending and descending sequences,
  respectively.
- **nominvalue** – no minimum value of the sequence.  This
  value is used when the CREATE SEQUENCE command is emitted to
  the database as the value of the “NO MINVALUE” clause.  If `None`,
  the clause is omitted, which on most platforms indicates a
  minvalue of 1 and -2^63-1 for ascending and descending sequences,
  respectively.
- **nomaxvalue** – no maximum value of the sequence.  This
  value is used when the CREATE SEQUENCE command is emitted to
  the database as the value of the “NO MAXVALUE” clause.  If `None`,
  the clause is omitted, which on most platforms indicates a
  maxvalue of 2^63-1 and -1 for ascending and descending sequences,
  respectively.
- **cycle** – allows the sequence to wrap around when the maxvalue
  or minvalue has been reached by an ascending or descending sequence
  respectively.  This value is used when the CREATE SEQUENCE command
  is emitted to the database as the “CYCLE” clause.  If the limit is
  reached, the next number generated will be the minvalue or maxvalue,
  respectively.  If cycle=False (the default) any calls to nextval
  after the sequence has reached its maximum value will return an
  error.
- **schema** – optional schema name for the sequence, if located
  in a schema other than the default.  The rules for selecting the
  schema name when a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
  is also present are the same
  as that of [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema).
- **cache** – optional integer value; number of future values in the
  sequence which are calculated in advance.  Renders the CACHE keyword
  understood by Oracle Database and PostgreSQL.
- **order** – optional boolean value; if `True`, renders the
  ORDER keyword, understood by Oracle Database, indicating the sequence
  is definitively ordered.   May be necessary to provide deterministic
  ordering using Oracle RAC.
- **data_type** –
  The type to be returned by the sequence, for
  dialects that allow us to choose between INTEGER, BIGINT, etc.
  (e.g., mssql).
  Added in version 1.4.0.
- **optional** – boolean value, when `True`, indicates that this
  [Sequence](#sqlalchemy.schema.Sequence) object only needs to be explicitly generated
  on backends that don’t provide another way to generate primary
  key identifiers.  Currently, it essentially means, “don’t create
  this sequence on the PostgreSQL backend, where the SERIAL keyword
  creates a sequence for us automatically”.
- **quote** – boolean value, when `True` or `False`, explicitly
  forces quoting of the [Sequence.name](#sqlalchemy.schema.Sequence.params.name) on or off.
  When left at its default of `None`, normal quoting rules based
  on casing and reserved words take place.
- **quote_schema** – Set the quoting preferences for the `schema`
  name.
- **metadata** –
  optional [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object which this
  [Sequence](#sqlalchemy.schema.Sequence) will be associated with.  A [Sequence](#sqlalchemy.schema.Sequence)
  that is associated with a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
  gains the following
  capabilities:
  - The [Sequence](#sqlalchemy.schema.Sequence) will inherit the
    [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema)
    parameter specified to the target [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData), which
    affects the production of CREATE / DROP DDL, if any.
  - The [Sequence.create()](#sqlalchemy.schema.Sequence.create) and [Sequence.drop()](#sqlalchemy.schema.Sequence.drop) methods
    automatically use the engine bound to the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
    object, if any.
  - The [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) and
    [MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all)
    methods will emit CREATE / DROP for this [Sequence](#sqlalchemy.schema.Sequence),
    even if the [Sequence](#sqlalchemy.schema.Sequence) is not associated with any
    [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) / [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
    that’s a member of this
    [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData).
  The above behaviors can only occur if the [Sequence](#sqlalchemy.schema.Sequence) is
  explicitly associated with the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
  via this parameter.
  See also
  [Associating a Sequence with the MetaData](#sequence-metadata) - full discussion of the
  [Sequence.metadata](#sqlalchemy.schema.Sequence.params.metadata) parameter.
- **for_update** – Indicates this [Sequence](#sqlalchemy.schema.Sequence), when associated
  with a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column),
  should be invoked for UPDATE statements
  on that column’s table, rather than for INSERT statements, when
  no value is otherwise present for that column in the statement.

      method [sqlalchemy.schema.Sequence.](#sqlalchemy.schema.Sequence)create(*bind:_CreateDropBind*, *checkfirst:bool=True*) → None

Creates this sequence in the database.

    method [sqlalchemy.schema.Sequence.](#sqlalchemy.schema.Sequence)drop(*bind:_CreateDropBind*, *checkfirst:bool=True*) → None

Drops this sequence from the database.

    method [sqlalchemy.schema.Sequence.](#sqlalchemy.schema.Sequence)next_value() → [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function)[int]

Return a [next_value](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.next_value) function element
which will render the appropriate increment function
for this [Sequence](#sqlalchemy.schema.Sequence) within any SQL expression.

     class sqlalchemy.schema.Identity

*inherits from* `sqlalchemy.schema.IdentityOptions`, [sqlalchemy.schema.FetchedValue](#sqlalchemy.schema.FetchedValue), [sqlalchemy.schema.SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Defines an identity column, i.e. “GENERATED { ALWAYS | BY DEFAULT }
AS IDENTITY” syntax.

The [Identity](#sqlalchemy.schema.Identity) construct is an inline construct added to the
argument list of a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object:

```
from sqlalchemy import Identity

Table(
    "foo",
    metadata_obj,
    Column("id", Integer, Identity()),
    Column("description", Text),
)
```

See the linked documentation below for complete details.

Added in version 1.4.

See also

[Identity Columns (GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY)](#identity-ddl)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY DDL
construct to accompany aColumn. |
| copy() |  |

   method [sqlalchemy.schema.Identity.](#sqlalchemy.schema.Identity)__init__(*always:bool=False*, *on_null:bool|None=None*, *start:int|None=None*, *increment:int|None=None*, *minvalue:int|None=None*, *maxvalue:int|None=None*, *nominvalue:bool|None=None*, *nomaxvalue:bool|None=None*, *cycle:bool|None=None*, *cache:int|None=None*, *order:bool|None=None*) → None

Construct a GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY DDL
construct to accompany a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

See the [Sequence](#sqlalchemy.schema.Sequence) documentation for a complete description
of most parameters.

Note

MSSQL supports this construct as the preferred alternative to
generate an IDENTITY on a column, but it uses non standard
syntax that only support [Identity.start](#sqlalchemy.schema.Identity.params.start)
and [Identity.increment](#sqlalchemy.schema.Identity.params.increment).
All other parameters are ignored.

   Parameters:

- **always** – A boolean, that indicates the type of identity column.
  If `False` is specified, the default, then the user-specified
  value takes precedence.
  If `True` is specified, a user-specified value is not accepted (
  on some backends, like PostgreSQL, OVERRIDING SYSTEM VALUE, or
  similar, may be specified in an INSERT to override the sequence
  value).
  Some backends also have a default value for this parameter,
  `None` can be used to omit rendering this part in the DDL. It
  will be treated as `False` if a backend does not have a default
  value.
- **on_null** – Set to `True` to specify ON NULL in conjunction with a
  `always=False` identity column. This option is only supported on
  some backends, like Oracle Database.
- **start** – the starting index of the sequence.
- **increment** – the increment value of the sequence.
- **minvalue** – the minimum value of the sequence.
- **maxvalue** – the maximum value of the sequence.
- **nominvalue** – no minimum value of the sequence.
- **nomaxvalue** – no maximum value of the sequence.
- **cycle** – allows the sequence to wrap around when the maxvalue
  or minvalue has been reached.
- **cache** – optional integer value; number of future values in the
  sequence which are calculated in advance.
- **order** – optional boolean value; if true, renders the
  ORDER keyword.

      method [sqlalchemy.schema.Identity.](#sqlalchemy.schema.Identity)copy(***kw:Any*) → [Identity](#sqlalchemy.schema.Identity)

Deprecated since version 1.4: The [Identity.copy()](#sqlalchemy.schema.Identity.copy) method is deprecated and will be removed in a future release.
