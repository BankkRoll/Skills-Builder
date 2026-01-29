# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Microsoft SQL Server

Support for the Microsoft SQL Server database.

The following table summarizes current support levels for database release versions.

| Support type | Versions |
| --- | --- |
| Supported version | 2012+ |
| Best effort | 2005+ |

## DBAPI Support

The following dialect/DBAPI options are available.  Please refer to individual DBAPI sections for connect information.

- [PyODBC](#module-sqlalchemy.dialects.mssql.pyodbc)
- [pymssql](#module-sqlalchemy.dialects.mssql.pymssql)
- [aioodbc](#module-sqlalchemy.dialects.mssql.aioodbc)

## External Dialects

In addition to the above DBAPI layers with native SQLAlchemy support, there
are third-party dialects for other DBAPI layers that are compatible
with SQL Server. See the “External Dialects” list on the
[Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) page.

## Auto Increment Behavior / IDENTITY Columns

SQL Server provides so-called “auto incrementing” behavior using the
`IDENTITY` construct, which can be placed on any single integer column in a
table. SQLAlchemy considers `IDENTITY` within its default “autoincrement”
behavior for an integer primary key column, described at
[Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement).  This means that by default,
the first integer primary key column in a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) will be
considered to be the identity column - unless it is associated with a
[Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) - and will generate DDL as such:

```
from sqlalchemy import Table, MetaData, Column, Integer

m = MetaData()
t = Table(
    "t",
    m,
    Column("id", Integer, primary_key=True),
    Column("x", Integer),
)
m.create_all(engine)
```

The above example will generate DDL as:

```
CREATE TABLE t (
    id INTEGER NOT NULL IDENTITY,
    x INTEGER NULL,
    PRIMARY KEY (id)
)
```

For the case where this default generation of `IDENTITY` is not desired,
specify `False` for the [Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement) flag,
on the first integer primary key column:

```
m = MetaData()
t = Table(
    "t",
    m,
    Column("id", Integer, primary_key=True, autoincrement=False),
    Column("x", Integer),
)
m.create_all(engine)
```

To add the `IDENTITY` keyword to a non-primary key column, specify
`True` for the [Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement) flag on the desired
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object, and ensure that
[Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement)
is set to `False` on any integer primary key column:

```
m = MetaData()
t = Table(
    "t",
    m,
    Column("id", Integer, primary_key=True, autoincrement=False),
    Column("x", Integer, autoincrement=True),
)
m.create_all(engine)
```

Changed in version 1.4: Added [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) construct
in a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) to specify the start and increment
parameters of an IDENTITY. These replace
the use of the [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) object in order to specify these values.

Deprecated since version 1.4: The `mssql_identity_start` and `mssql_identity_increment` parameters
to [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) are deprecated and should we replaced by
an [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) object. Specifying both ways of configuring
an IDENTITY will result in a compile error.
These options are also no longer returned as part of the
`dialect_options` key in [Inspector.get_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns).
Use the information in the `identity` key instead.

Deprecated since version 1.3: The use of [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) to specify IDENTITY characteristics is
deprecated and will be removed in a future release.   Please use
the [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) object parameters
[Identity.start](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity.params.start) and
[Identity.increment](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity.params.increment).

Changed in version 1.4: Removed the ability to use a [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)
object to modify IDENTITY characteristics. [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) objects
now only manipulate true T-SQL SEQUENCE types.

Note

There can only be one IDENTITY column on the table.  When using
`autoincrement=True` to enable the IDENTITY keyword, SQLAlchemy does not
guard against multiple columns specifying the option simultaneously.  The
SQL Server database will instead reject the `CREATE TABLE` statement.

Note

An INSERT statement which attempts to provide a value for a column that is
marked with IDENTITY will be rejected by SQL Server.   In order for the
value to be accepted, a session-level option “SET IDENTITY_INSERT” must be
enabled.   The SQLAlchemy SQL Server dialect will perform this operation
automatically when using a core [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
construct; if the
execution specifies a value for the IDENTITY column, the “IDENTITY_INSERT”
option will be enabled for the span of that statement’s invocation.However,
this scenario is not high performing and should not be relied upon for
normal use.   If a table doesn’t actually require IDENTITY behavior in its
integer primary key column, the keyword should be disabled when creating
the table by ensuring that `autoincrement=False` is set.

### Controlling “Start” and “Increment”

Specific control over the “start” and “increment” values for
the `IDENTITY` generator are provided using the
[Identity.start](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity.params.start) and [Identity.increment](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity.params.increment)
parameters passed to the [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) object:

```
from sqlalchemy import Table, Integer, Column, Identity

test = Table(
    "test",
    metadata,
    Column(
        "id", Integer, primary_key=True, Identity(start=100, increment=10)
    ),
    Column("name", String(20)),
)
```

The CREATE TABLE for the above [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object would be:

```
CREATE TABLE test (
  id INTEGER NOT NULL IDENTITY(100,10) PRIMARY KEY,
  name VARCHAR(20) NULL,
)
```

Note

The [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) object supports many other parameter in
addition to `start` and `increment`. These are not supported by
SQL Server and will be ignored when generating the CREATE TABLE ddl.

Changed in version 1.3.19: The [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) object is
now used to affect the
`IDENTITY` generator for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) under  SQL Server.
Previously, the [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) object was used.  As SQL Server now
supports real sequences as a separate construct, [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) will be
functional in the normal way starting from SQLAlchemy version 1.4.

### Using IDENTITY with Non-Integer numeric types

SQL Server also allows `IDENTITY` to be used with `NUMERIC` columns.  To
implement this pattern smoothly in SQLAlchemy, the primary datatype of the
column should remain as `Integer`, however the underlying implementation
type deployed to the SQL Server database can be specified as `Numeric` using
[TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant):

```
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TestTable(Base):
    __tablename__ = "test"
    id = Column(
        Integer().with_variant(Numeric(10, 0), "mssql"),
        primary_key=True,
        autoincrement=True,
    )
    name = Column(String)
```

In the above example, `Integer().with_variant()` provides clear usage
information that accurately describes the intent of the code. The general
restriction that `autoincrement` only applies to `Integer` is established
at the metadata level and not at the per-dialect level.

When using the above pattern, the primary key identifier that comes back from
the insertion of a row, which is also the value that would be assigned to an
ORM object such as `TestTable` above, will be an instance of `Decimal()`
and not `int` when using SQL Server. The numeric return type of the
[Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric) type can be changed to return floats by passing False
to [Numeric.asdecimal](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric.params.asdecimal). To normalize the return type of the
above `Numeric(10, 0)` to return Python ints (which also support “long”
integer values in Python 3), use [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) as follows:

```
from sqlalchemy import TypeDecorator

class NumericAsInteger(TypeDecorator):
    "normalize floating point return values into ints"

    impl = Numeric(10, 0, asdecimal=False)
    cache_ok = True

    def process_result_value(self, value, dialect):
        if value is not None:
            value = int(value)
        return value

class TestTable(Base):
    __tablename__ = "test"
    id = Column(
        Integer().with_variant(NumericAsInteger, "mssql"),
        primary_key=True,
        autoincrement=True,
    )
    name = Column(String)
```

### INSERT behavior

Handling of the `IDENTITY` column at INSERT time involves two key
techniques. The most common is being able to fetch the “last inserted value”
for a given `IDENTITY` column, a process which SQLAlchemy performs
implicitly in many cases, most importantly within the ORM.

The process for fetching this value has several variants:

- In the vast majority of cases, RETURNING is used in conjunction with INSERT
  statements on SQL Server in order to get newly generated primary key values:
  ```
  INSERT INTO t (x) OUTPUT inserted.id VALUES (?)
  ```
  As of SQLAlchemy 2.0, the [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) feature is also
  used by default to optimize many-row INSERT statements; for SQL Server
  the feature takes place for both RETURNING and-non RETURNING
  INSERT statements.
  Changed in version 2.0.10: The [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) feature for
  SQL Server was temporarily disabled for SQLAlchemy version 2.0.9 due to
  issues with row ordering. As of 2.0.10 the feature is re-enabled, with
  special case handling for the unit of work’s requirement for RETURNING to
  be ordered.
- When RETURNING is not available or has been disabled via
  `implicit_returning=False`, either the `scope_identity()` function or
  the `@@identity` variable is used; behavior varies by backend:
  - when using PyODBC, the phrase `; select scope_identity()` will be
    appended to the end of the INSERT statement; a second result set will be
    fetched in order to receive the value.  Given a table as:
    ```
    t = Table(
        "t",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("x", Integer),
        implicit_returning=False,
    )
    ```
    an INSERT will look like:
    ```
    INSERT INTO t (x) VALUES (?); select scope_identity()
    ```
  - Other dialects such as pymssql will call upon
    `SELECT scope_identity() AS lastrowid` subsequent to an INSERT
    statement. If the flag `use_scope_identity=False` is passed to
    [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine),
    the statement `SELECT @@identity AS lastrowid`
    is used instead.

A table that contains an `IDENTITY` column will prohibit an INSERT statement
that refers to the identity column explicitly.  The SQLAlchemy dialect will
detect when an INSERT construct, created using a core
[insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert)
construct (not a plain string SQL), refers to the identity column, and
in this case will emit `SET IDENTITY_INSERT ON` prior to the insert
statement proceeding, and `SET IDENTITY_INSERT OFF` subsequent to the
execution.  Given this example:

```
m = MetaData()
t = Table(
    "t", m, Column("id", Integer, primary_key=True), Column("x", Integer)
)
m.create_all(engine)

with engine.begin() as conn:
    conn.execute(t.insert(), {"id": 1, "x": 1}, {"id": 2, "x": 2})
```

The above column will be created with IDENTITY, however the INSERT statement
we emit is specifying explicit values.  In the echo output we can see
how SQLAlchemy handles this:

```
CREATE TABLE t (
    id INTEGER NOT NULL IDENTITY(1,1),
    x INTEGER NULL,
    PRIMARY KEY (id)
)

COMMIT
SET IDENTITY_INSERT t ON
INSERT INTO t (id, x) VALUES (?, ?)
((1, 1), (2, 2))
SET IDENTITY_INSERT t OFF
COMMIT
```

This is an auxiliary use case suitable for testing and bulk insert scenarios.

## SEQUENCE support

The [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) object creates “real” sequences, i.e.,
`CREATE SEQUENCE`:

```
>>> from sqlalchemy import Sequence
>>> from sqlalchemy.schema import CreateSequence
>>> from sqlalchemy.dialects import mssql
>>> print(
...     CreateSequence(Sequence("my_seq", start=1)).compile(
...         dialect=mssql.dialect()
...     )
... )
CREATE SEQUENCE my_seq START WITH 1
```

For integer primary key generation, SQL Server’s `IDENTITY` construct should
generally be preferred vs. sequence.

Tip

The default start value for T-SQL is `-2**63` instead of 1 as
in most other SQL databases. Users should explicitly set the
[Sequence.start](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.start) to 1 if that’s the expected default:

```
seq = Sequence("my_sequence", start=1)
```

Added in version 1.4: added SQL Server support for [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)

Changed in version 2.0: The SQL Server dialect will no longer implicitly
render “START WITH 1” for `CREATE SEQUENCE`, which was the behavior
first implemented in version 1.4.

## MAX on VARCHAR / NVARCHAR

SQL Server supports the special string “MAX” within the
[VARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARCHAR) and [NVARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NVARCHAR) datatypes,
to indicate “maximum length possible”.   The dialect currently handles this as
a length of “None” in the base type, rather than supplying a
dialect-specific version of these types, so that a base type
specified such as `VARCHAR(None)` can assume “unlengthed” behavior on
more than one backend without using dialect-specific types.

To build a SQL Server VARCHAR or NVARCHAR with MAX length, use None:

```
my_table = Table(
    "my_table",
    metadata,
    Column("my_data", VARCHAR(None)),
    Column("my_n_data", NVARCHAR(None)),
)
```

## Collation Support

Character collations are supported by the base string types,
specified by the string argument “collation”:

```
from sqlalchemy import VARCHAR

Column("login", VARCHAR(32, collation="Latin1_General_CI_AS"))
```

When such a column is associated with a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), the
CREATE TABLE statement for this column will yield:

```
login VARCHAR(32) COLLATE Latin1_General_CI_AS NULL
```

## LIMIT/OFFSET Support

MSSQL has added support for LIMIT / OFFSET as of SQL Server 2012, via the
“OFFSET n ROWS” and “FETCH NEXT n ROWS” clauses.  SQLAlchemy supports these
syntaxes automatically if SQL Server 2012 or greater is detected.

Changed in version 1.4: support added for SQL Server “OFFSET n ROWS” and
“FETCH NEXT n ROWS” syntax.

For statements that specify only LIMIT and no OFFSET, all versions of SQL
Server support the TOP keyword.   This syntax is used for all SQL Server
versions when no OFFSET clause is present.  A statement such as:

```
select(some_table).limit(5)
```

will render similarly to:

```
SELECT TOP 5 col1, col2.. FROM table
```

For versions of SQL Server prior to SQL Server 2012, a statement that uses
LIMIT and OFFSET, or just OFFSET alone, will be rendered using the
`ROW_NUMBER()` window function.   A statement such as:

```
select(some_table).order_by(some_table.c.col3).limit(5).offset(10)
```

will render similarly to:

```
SELECT anon_1.col1, anon_1.col2 FROM (SELECT col1, col2,
ROW_NUMBER() OVER (ORDER BY col3) AS
mssql_rn FROM table WHERE t.x = :x_1) AS
anon_1 WHERE mssql_rn > :param_1 AND mssql_rn <= :param_2 + :param_1
```

Note that when using LIMIT and/or OFFSET, whether using the older
or newer SQL Server syntaxes, the statement must have an ORDER BY as well,
else a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) is raised.

## DDL Comment Support

Comment support, which includes DDL rendering for attributes such as
[Table.comment](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.comment) and [Column.comment](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.comment), as
well as the ability to reflect these comments, is supported assuming a
supported version of SQL Server is in use. If a non-supported version such as
Azure Synapse is detected at first-connect time (based on the presence
of the `fn_listextendedproperty` SQL function), comment support including
rendering and table-comment reflection is disabled, as both features rely upon
SQL Server stored procedures and functions that are not available on all
backend types.

To force comment support to be on or off, bypassing autodetection, set the
parameter `supports_comments` within [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine):

```
e = create_engine("mssql+pyodbc://u:p@dsn", supports_comments=False)
```

Added in version 2.0: Added support for table and column comments for
the SQL Server dialect, including DDL generation and reflection.

## Transaction Isolation Level

All SQL Server dialects support setting of transaction isolation level
both via a dialect-specific parameter
[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level)
accepted by [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine),
as well as the [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
argument as passed to
[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options).
This feature works by issuing the
command `SET TRANSACTION ISOLATION LEVEL <level>` for
each new connection.

To set isolation level using [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine):

```
engine = create_engine(
    "mssql+pyodbc://scott:tiger@ms_2008", isolation_level="REPEATABLE READ"
)
```

To set using per-connection execution options:

```
connection = engine.connect()
connection = connection.execution_options(isolation_level="READ COMMITTED")
```

Valid values for `isolation_level` include:

- `AUTOCOMMIT` - pyodbc / pymssql-specific
- `READ COMMITTED`
- `READ UNCOMMITTED`
- `REPEATABLE READ`
- `SERIALIZABLE`
- `SNAPSHOT` - specific to SQL Server

There are also more options for isolation level configurations, such as
“sub-engine” objects linked to a main [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which each apply
different isolation level settings.  See the discussion at
[Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit) for background.

See also

[Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit)

## Temporary Table / Resource Reset for Connection Pooling

The [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) connection pool implementation used
by the SQLAlchemy [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object includes
[reset on return](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-reset-on-return) behavior that will invoke
the DBAPI `.rollback()` method when connections are returned to the pool.
While this rollback will clear out the immediate state used by the previous
transaction, it does not cover a wider range of session-level state, including
temporary tables as well as other server state such as prepared statement
handles and statement caches.   An undocumented SQL Server procedure known
as `sp_reset_connection` is known to be a workaround for this issue which
will reset most of the session state that builds up on a connection, including
temporary tables.

To install `sp_reset_connection` as the means of performing reset-on-return,
the [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event hook may be used, as demonstrated in the
example below. The [create_engine.pool_reset_on_return](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_reset_on_return) parameter
is set to `None` so that the custom scheme can replace the default behavior
completely.   The custom hook implementation calls `.rollback()` in any case,
as it’s usually important that the DBAPI’s own tracking of commit/rollback
will remain consistent with the state of the transaction:

```
from sqlalchemy import create_engine
from sqlalchemy import event

mssql_engine = create_engine(
    "mssql+pyodbc://scott:tiger^5HHH@mssql2017:1433/test?driver=ODBC+Driver+17+for+SQL+Server",
    # disable default reset-on-return scheme
    pool_reset_on_return=None,
)

@event.listens_for(mssql_engine, "reset")
def _reset_mssql(dbapi_connection, connection_record, reset_state):
    if not reset_state.terminate_only:
        dbapi_connection.execute("{call sys.sp_reset_connection}")

    # so that the DBAPI itself knows that the connection has been
    # reset
    dbapi_connection.rollback()
```

Changed in version 2.0.0b3: Added additional state arguments to
the [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event and additionally ensured the event
is invoked for all “reset” occurrences, so that it’s appropriate
as a place for custom “reset” handlers.   Previous schemes which
use the [PoolEvents.checkin()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.checkin) handler remain usable as well.

See also

[Reset On Return](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-reset-on-return) - in the [Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html) documentation

## Nullability

MSSQL has support for three levels of column nullability. The default
nullability allows nulls and is explicit in the CREATE TABLE
construct:

```
name VARCHAR(20) NULL
```

If `nullable=None` is specified then no specification is made. In
other words the database’s configured default is used. This will
render:

```
name VARCHAR(20)
```

If `nullable` is `True` or `False` then the column will be
`NULL` or `NOT NULL` respectively.

## Date / Time Handling

DATE and TIME are supported.   Bind parameters are converted
to datetime.datetime() objects as required by most MSSQL drivers,
and results are processed from strings if needed.
The DATE and TIME types are not available for MSSQL 2005 and
previous - if a server version below 2008 is detected, DDL
for these types will be issued as DATETIME.

## Large Text/Binary Type Deprecation

Per
[SQL Server 2012/2014 Documentation](https://technet.microsoft.com/en-us/library/ms187993.aspx),
the `NTEXT`, `TEXT` and `IMAGE` datatypes are to be removed from SQL
Server in a future release.   SQLAlchemy normally relates these types to the
[UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText), [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) and
[LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) datatypes.

In order to accommodate this change, a new flag `deprecate_large_types`
is added to the dialect, which will be automatically set based on detection
of the server version in use, if not otherwise set by the user.  The
behavior of this flag is as follows:

- When this flag is `True`, the [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText),
  [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) and
  [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) datatypes, when used to render DDL, will render the
  types `NVARCHAR(max)`, `VARCHAR(max)`, and `VARBINARY(max)`,
  respectively.  This is a new behavior as of the addition of this flag.
- When this flag is `False`, the [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText),
  [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) and
  [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) datatypes, when used to render DDL, will render the
  types `NTEXT`, `TEXT`, and `IMAGE`,
  respectively.  This is the long-standing behavior of these types.
- The flag begins with the value `None`, before a database connection is
  established.   If the dialect is used to render DDL without the flag being
  set, it is interpreted the same as `False`.
- On first connection, the dialect detects if SQL Server version 2012 or
  greater is in use; if the flag is still at `None`, it sets it to `True`
  or `False` based on whether 2012 or greater is detected.
- The flag can be set to either `True` or `False` when the dialect
  is created, typically via [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine):
  ```
  eng = create_engine(
      "mssql+pymssql://user:pass@host/db", deprecate_large_types=True
  )
  ```
- Complete control over whether the “old” or “new” types are rendered is
  available in all SQLAlchemy versions by using the UPPERCASE type objects
  instead: [NVARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NVARCHAR), [VARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARCHAR),
  [VARBINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARBINARY), [TEXT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TEXT), [NTEXT](#sqlalchemy.dialects.mssql.NTEXT),
  [IMAGE](#sqlalchemy.dialects.mssql.IMAGE)
  will always remain fixed and always output exactly that
  type.

## Multipart Schema Names

SQL Server schemas sometimes require multiple parts to their “schema”
qualifier, that is, including the database name and owner name as separate
tokens, such as `mydatabase.dbo.some_table`. These multipart names can be set
at once using the [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) argument of
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table):

```
Table(
    "some_table",
    metadata,
    Column("q", String(50)),
    schema="mydatabase.dbo",
)
```

When performing operations such as table or component reflection, a schema
argument that contains a dot will be split into separate
“database” and “owner”  components in order to correctly query the SQL
Server information schema tables, as these two values are stored separately.
Additionally, when rendering the schema name for DDL or SQL, the two
components will be quoted separately for case sensitive names and other
special characters.   Given an argument as below:

```
Table(
    "some_table",
    metadata,
    Column("q", String(50)),
    schema="MyDataBase.dbo",
)
```

The above schema would be rendered as `[MyDataBase].dbo`, and also in
reflection, would be reflected using “dbo” as the owner and “MyDataBase”
as the database name.

To control how the schema name is broken into database / owner,
specify brackets (which in SQL Server are quoting characters) in the name.
Below, the “owner” will be considered as `MyDataBase.dbo` and the
“database” will be None:

```
Table(
    "some_table",
    metadata,
    Column("q", String(50)),
    schema="[MyDataBase.dbo]",
)
```

To individually specify both database and owner name with special characters
or embedded dots, use two sets of brackets:

```
Table(
    "some_table",
    metadata,
    Column("q", String(50)),
    schema="[MyDataBase.Period].[MyOwner.Dot]",
)
```

Changed in version 1.2: the SQL Server dialect now treats brackets as
identifier delimiters splitting the schema into separate database
and owner tokens, to allow dots within either name itself.

## Legacy Schema Mode

Very old versions of the MSSQL dialect introduced the behavior such that a
schema-qualified table would be auto-aliased when used in a
SELECT statement; given a table:

```
account_table = Table(
    "account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("info", String(100)),
    schema="customer_schema",
)
```

this legacy mode of rendering would assume that “customer_schema.account”
would not be accepted by all parts of the SQL statement, as illustrated
below:

```
>>> eng = create_engine("mssql+pymssql://mydsn", legacy_schema_aliasing=True)
>>> print(account_table.select().compile(eng))
SELECT account_1.id, account_1.info
FROM customer_schema.account AS account_1
```

This mode of behavior is now off by default, as it appears to have served
no purpose; however in the case that legacy applications rely upon it,
it is available using the `legacy_schema_aliasing` argument to
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) as illustrated above.

Deprecated since version 1.4: The `legacy_schema_aliasing` flag is now
deprecated and will be removed in a future release.

## Clustered Index Support

The MSSQL dialect supports clustered indexes (and primary keys) via the
`mssql_clustered` option.  This option is available to [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index),
[UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint). and [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint).
For indexes this option can be combined with the `mssql_columnstore` one
to create a clustered columnstore index.

To generate a clustered index:

```
Index("my_index", table.c.x, mssql_clustered=True)
```

which renders the index as `CREATE CLUSTERED INDEX my_index ON table (x)`.

To generate a clustered primary key use:

```
Table(
    "my_table",
    metadata,
    Column("x", ...),
    Column("y", ...),
    PrimaryKeyConstraint("x", "y", mssql_clustered=True),
)
```

which will render the table, for example, as:

```
CREATE TABLE my_table (
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  PRIMARY KEY CLUSTERED (x, y)
)
```

Similarly, we can generate a clustered unique constraint using:

```
Table(
    "my_table",
    metadata,
    Column("x", ...),
    Column("y", ...),
    PrimaryKeyConstraint("x"),
    UniqueConstraint("y", mssql_clustered=True),
)
```

To explicitly request a non-clustered primary key (for example, when
a separate clustered index is desired), use:

```
Table(
    "my_table",
    metadata,
    Column("x", ...),
    Column("y", ...),
    PrimaryKeyConstraint("x", "y", mssql_clustered=False),
)
```

which will render the table, for example, as:

```
CREATE TABLE my_table (
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  PRIMARY KEY NONCLUSTERED (x, y)
)
```

## Columnstore Index Support

The MSSQL dialect supports columnstore indexes via the `mssql_columnstore`
option.  This option is available to [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index). It be combined with
the `mssql_clustered` option to create a clustered columnstore index.

To generate a columnstore index:

```
Index("my_index", table.c.x, mssql_columnstore=True)
```

which renders the index as `CREATE COLUMNSTORE INDEX my_index ON table (x)`.

To generate a clustered columnstore index provide no columns:

```
idx = Index("my_index", mssql_clustered=True, mssql_columnstore=True)
# required to associate the index with the table
table.append_constraint(idx)
```

the above renders the index as
`CREATE CLUSTERED COLUMNSTORE INDEX my_index ON table`.

Added in version 2.0.18.

## MSSQL-Specific Index Options

In addition to clustering, the MSSQL dialect supports other special options
for [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index).

### INCLUDE

The `mssql_include` option renders INCLUDE(colname) for the given string
names:

```
Index("my_index", table.c.x, mssql_include=["y"])
```

would render the index as `CREATE INDEX my_index ON table (x) INCLUDE (y)`

### Filtered Indexes

The `mssql_where` option renders WHERE(condition) for the given string
names:

```
Index("my_index", table.c.x, mssql_where=table.c.x > 10)
```

would render the index as `CREATE INDEX my_index ON table (x) WHERE x > 10`.

Added in version 1.3.4.

### Index ordering

Index ordering is available via functional expressions, such as:

```
Index("my_index", table.c.x.desc())
```

would render the index as `CREATE INDEX my_index ON table (x DESC)`

See also

[Functional Indexes](https://docs.sqlalchemy.org/en/20/core/constraints.html#schema-indexes-functional)

## Compatibility Levels

MSSQL supports the notion of setting compatibility levels at the
database level. This allows, for instance, to run a database that
is compatible with SQL2000 while running on a SQL2005 database
server. `server_version_info` will always return the database
server version information (in this case SQL2005) and not the
compatibility level information. Because of this, if running under
a backwards compatibility mode SQLAlchemy may attempt to use T-SQL
statements that are unable to be parsed by the database server.

## Triggers

SQLAlchemy by default uses OUTPUT INSERTED to get at newly
generated primary key values via IDENTITY columns or other
server side defaults.   MS-SQL does not
allow the usage of OUTPUT INSERTED on tables that have triggers.
To disable the usage of OUTPUT INSERTED on a per-table basis,
specify `implicit_returning=False` for each [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
which has triggers:

```
Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    # ...,
    implicit_returning=False,
)
```

Declarative form:

```
class MyClass(Base):
    # ...
    __table_args__ = {"implicit_returning": False}
```

## Rowcount Support / ORM Versioning

The SQL Server drivers may have limited ability to return the number
of rows updated from an UPDATE or DELETE statement.

As of this writing, the PyODBC driver is not able to return a rowcount when
OUTPUT INSERTED is used.    Previous versions of SQLAlchemy therefore had
limitations for features such as the “ORM Versioning” feature that relies upon
accurate rowcounts in order to match version numbers with matched rows.

SQLAlchemy 2.0 now retrieves the “rowcount” manually for these particular use
cases based on counting the rows that arrived back within RETURNING; so while
the driver still has this limitation, the ORM Versioning feature is no longer
impacted by it. As of SQLAlchemy 2.0.5, ORM versioning has been fully
re-enabled for the pyodbc driver.

Changed in version 2.0.5: ORM versioning support is restored for the pyodbc
driver.  Previously, a warning would be emitted during ORM flush that
versioning was not supported.

## Enabling Snapshot Isolation

SQL Server has a default transaction
isolation mode that locks entire tables, and causes even mildly concurrent
applications to have long held locks and frequent deadlocks.
Enabling snapshot isolation for the database as a whole is recommended
for modern levels of concurrency support.  This is accomplished via the
following ALTER DATABASE commands executed at the SQL prompt:

```
ALTER DATABASE MyDatabase SET ALLOW_SNAPSHOT_ISOLATION ON

ALTER DATABASE MyDatabase SET READ_COMMITTED_SNAPSHOT ON
```

Background on SQL Server snapshot isolation is available at
[https://msdn.microsoft.com/en-us/library/ms175095.aspx](https://msdn.microsoft.com/en-us/library/ms175095.aspx).

## SQL Server SQL Constructs

| Object Name | Description |
| --- | --- |
| try_cast(expression, type_) | Produce aTRY_CASTexpression for backends which support it;
this is aCASTwhich returns NULL for un-castable conversions. |

   function sqlalchemy.dialects.mssql.try_cast(*expression:_ColumnExpressionOrLiteralArgument[Any]*, *type_:_TypeEngineArgument[_T]*) → [TryCast](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TryCast)[_T]

Produce a `TRY_CAST` expression for backends which support it;
this is a `CAST` which returns NULL for un-castable conversions.

In SQLAlchemy, this construct is supported **only** by the SQL Server
dialect, and will raise a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) if used on other
included backends.  However, third party backends may also support
this construct.

Tip

As [try_cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.try_cast) originates from the SQL Server dialect,
it’s importable both from `sqlalchemy.` as well as from
`sqlalchemy.dialects.mssql`.

[try_cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.try_cast) returns an instance of [TryCast](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TryCast) and
generally behaves similarly to the [Cast](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Cast) construct;
at the SQL level, the difference between `CAST` and `TRY_CAST`
is that `TRY_CAST` returns NULL for an un-castable expression,
such as attempting to cast a string `"hi"` to an integer value.

E.g.:

```
from sqlalchemy import select, try_cast, Numeric

stmt = select(try_cast(product_table.c.unit_price, Numeric(10, 4)))
```

The above would render on Microsoft SQL Server as:

```
SELECT TRY_CAST (product_table.unit_price AS NUMERIC(10, 4))
FROM product_table
```

Added in version 2.0.14: [try_cast()](#sqlalchemy.dialects.mssql.try_cast) has been
generalized from the SQL Server dialect into a general use
construct that may be supported by additional dialects.

## SQL Server Data Types

As with all SQLAlchemy dialects, all UPPERCASE types that are known to be
valid with SQL server are importable from the top level dialect, whether
they originate from [sqlalchemy.types](https://docs.sqlalchemy.org/en/20/core/type_basics.html#module-sqlalchemy.types) or from the local dialect:

```
from sqlalchemy.dialects.mssql import (
    BIGINT,
    BINARY,
    BIT,
    CHAR,
    DATE,
    DATETIME,
    DATETIME2,
    DATETIMEOFFSET,
    DECIMAL,
    DOUBLE_PRECISION,
    FLOAT,
    IMAGE,
    INTEGER,
    JSON,
    MONEY,
    NCHAR,
    NTEXT,
    NUMERIC,
    NVARCHAR,
    REAL,
    SMALLDATETIME,
    SMALLINT,
    SMALLMONEY,
    SQL_VARIANT,
    TEXT,
    TIME,
    TIMESTAMP,
    TINYINT,
    UNIQUEIDENTIFIER,
    VARBINARY,
    VARCHAR,
)
```

Types which are specific to SQL Server, or have SQL Server-specific
construction arguments, are as follows:

| Object Name | Description |
| --- | --- |
| BIT | MSSQL BIT type. |
| DATETIME2 |  |
| DATETIMEOFFSET |  |
| DOUBLE_PRECISION | the SQL Server DOUBLE PRECISION datatype. |
| IMAGE |  |
| JSON | MSSQL JSON type. |
| MONEY |  |
| NTEXT | MSSQL NTEXT type, for variable-length unicode text up to 2^30
characters. |
| REAL | the SQL Server REAL datatype. |
| ROWVERSION | Implement the SQL Server ROWVERSION type. |
| SMALLDATETIME |  |
| SMALLMONEY |  |
| SQL_VARIANT |  |
| TIME |  |
| TIMESTAMP | Implement the SQL Server TIMESTAMP type. |
| TINYINT |  |
| UNIQUEIDENTIFIER |  |
| XML | MSSQL XML type. |

   class sqlalchemy.dialects.mssql.BIT

*inherits from* [sqlalchemy.types.Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)

MSSQL BIT type.

Both pyodbc and pymssql return values from BIT columns as
Python <class ‘bool’> so just subclass Boolean.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Boolean. |

   method [sqlalchemy.dialects.mssql.BIT.](#sqlalchemy.dialects.mssql.BIT)__init__(*create_constraint:bool=False*, *name:str|None=None*, *_create_events:bool=True*, *_adapted_from:SchemaType|None=None*)

*inherited from the* `sqlalchemy.types.Boolean.__init__` *method of* [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)

Construct a Boolean.

  Parameters:

- **create_constraint** –
  defaults to False.  If the boolean
  is generated as an int/smallint, also create a CHECK constraint
  on the table that ensures 1 or 0 as a value.
  Note
  it is strongly recommended that the CHECK constraint
  have an explicit name in order to support schema-management
  concerns.  This can be established either by setting the
  [Boolean.name](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean.params.name) parameter or by setting up an
  appropriate naming convention; see
  [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions) for background.
  Changed in version 1.4: - this flag now defaults to False, meaning
  no CHECK constraint is generated for a non-native enumerated
  type.
- **name** – if a CHECK constraint is generated, specify
  the name of the constraint.

       class sqlalchemy.dialects.mssql.CHAR

*inherits from* [sqlalchemy.types.String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

The SQL CHAR type.

   method [sqlalchemy.dialects.mssql.CHAR.](#sqlalchemy.dialects.mssql.CHAR)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) or [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.dialects.mssql.DATETIME2

*inherits from* `sqlalchemy.dialects.mssql.base._DateTimeBase`, [sqlalchemy.types.DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime)

     class sqlalchemy.dialects.mssql.DATETIMEOFFSET

*inherits from* `sqlalchemy.dialects.mssql.base._DateTimeBase`, [sqlalchemy.types.DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime)

     class sqlalchemy.dialects.mssql.DOUBLE_PRECISION

*inherits from* [sqlalchemy.types.DOUBLE_PRECISION](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE_PRECISION)

the SQL Server DOUBLE PRECISION datatype.

Added in version 2.0.11.

     class sqlalchemy.dialects.mssql.IMAGE

*inherits from* [sqlalchemy.types.LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a LargeBinary type. |

   method [sqlalchemy.dialects.mssql.IMAGE.](#sqlalchemy.dialects.mssql.IMAGE)__init__(*length:int|None=None*)

*inherited from the* `sqlalchemy.types.LargeBinary.__init__` *method of* [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary)

Construct a LargeBinary type.

  Parameters:

**length** – optional, a length for the column for use in
DDL statements, for those binary types that accept a length,
such as the MySQL BLOB type.

       class sqlalchemy.dialects.mssql.JSON

*inherits from* [sqlalchemy.types.JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)

MSSQL JSON type.

MSSQL supports JSON-formatted data as of SQL Server 2016.

The [JSON](#sqlalchemy.dialects.mssql.JSON) datatype at the DDL level will represent the
datatype as `NVARCHAR(max)`, but provides for JSON-level comparison
functions as well as Python coercion behavior.

[JSON](#sqlalchemy.dialects.mssql.JSON) is used automatically whenever the base
[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) datatype is used against a SQL Server backend.

See also

[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) - main documentation for the generic
cross-platform JSON datatype.

The [JSON](#sqlalchemy.dialects.mssql.JSON) type supports persistence of JSON values
as well as the core index operations provided by [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)
datatype, by adapting the operations to render the `JSON_VALUE`
or `JSON_QUERY` functions at the database level.

The SQL Server [JSON](#sqlalchemy.dialects.mssql.JSON) type necessarily makes use of the
`JSON_QUERY` and `JSON_VALUE` functions when querying for elements
of a JSON object.   These two functions have a major restriction in that
they are **mutually exclusive** based on the type of object to be returned.
The `JSON_QUERY` function **only** returns a JSON dictionary or list,
but not an individual string, numeric, or boolean element; the
`JSON_VALUE` function **only** returns an individual string, numeric,
or boolean element.   **both functions either return NULL or raise
an error if they are not used against the correct expected value**.

To handle this awkward requirement, indexed access rules are as follows:

1. When extracting a sub element from a JSON that is itself a JSON
  dictionary or list, the [Comparator.as_json()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_json) accessor
  should be used:
  ```
  stmt = select(data_table.c.data["some key"].as_json()).where(
      data_table.c.data["some key"].as_json() == {"sub": "structure"}
  )
  ```
2. When extracting a sub element from a JSON that is a plain boolean,
  string, integer, or float, use the appropriate method among
  [Comparator.as_boolean()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_boolean),
  [Comparator.as_string()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_string),
  [Comparator.as_integer()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_integer),
  [Comparator.as_float()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_float):
  ```
  stmt = select(data_table.c.data["some key"].as_string()).where(
      data_table.c.data["some key"].as_string() == "some string"
  )
  ```

Added in version 1.4.

| Member Name | Description |
| --- | --- |
| __init__() | Construct aJSONtype. |

   method [sqlalchemy.dialects.mssql.JSON.](#sqlalchemy.dialects.mssql.JSON)__init__(*none_as_null:bool=False*)

*inherited from the* `sqlalchemy.types.JSON.__init__` *method of* [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)

Construct a [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type.

  Parameters:

**none_as_null=False** –

if True, persist the value `None` as a
SQL NULL value, not the JSON encoding of `null`. Note that when this
flag is False, the [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) construct can still be used to
persist a NULL value, which may be passed directly as a parameter
value that is specially interpreted by the [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type
as SQL NULL:

```
from sqlalchemy import null

conn.execute(table.insert(), {"data": null()})
```

Note

[JSON.none_as_null](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.params.none_as_null) does **not** apply to the
values passed to [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and
[Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default); a value of `None`
passed for these parameters means “no default present”.

Additionally, when used in SQL comparison expressions, the
Python value `None` continues to refer to SQL null, and not
JSON NULL.  The [JSON.none_as_null](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.params.none_as_null) flag refers
explicitly to the **persistence** of the value within an
INSERT or UPDATE statement.   The [JSON.NULL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.NULL)
value should be used for SQL expressions that wish to compare to
JSON null.

See also

[JSON.NULL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.NULL)

        class sqlalchemy.dialects.mssql.MONEY

*inherits from* [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

     class sqlalchemy.dialects.mssql.NCHAR

*inherits from* [sqlalchemy.types.Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode)

The SQL NCHAR type.

   method [sqlalchemy.dialects.mssql.NCHAR.](#sqlalchemy.dialects.mssql.NCHAR)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) or [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.dialects.mssql.NTEXT

*inherits from* [sqlalchemy.types.UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)

MSSQL NTEXT type, for variable-length unicode text up to 2^30
characters.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |

   method [sqlalchemy.dialects.mssql.NTEXT.](#sqlalchemy.dialects.mssql.NTEXT)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) or [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.dialects.mssql.NVARCHAR

*inherits from* [sqlalchemy.types.Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode)

The SQL NVARCHAR type.

   method [sqlalchemy.dialects.mssql.NVARCHAR.](#sqlalchemy.dialects.mssql.NVARCHAR)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) or [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.dialects.mssql.REAL

*inherits from* [sqlalchemy.types.REAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.REAL)

the SQL Server REAL datatype.

    class sqlalchemy.dialects.mssql.ROWVERSION

*inherits from* [sqlalchemy.dialects.mssql.base.TIMESTAMP](#sqlalchemy.dialects.mssql.TIMESTAMP)

Implement the SQL Server ROWVERSION type.

The ROWVERSION datatype is a SQL Server synonym for the TIMESTAMP
datatype, however current SQL Server documentation suggests using
ROWVERSION for new datatypes going forward.

The ROWVERSION datatype does **not** reflect (e.g. introspect) from the
database as itself; the returned datatype will be
[TIMESTAMP](#sqlalchemy.dialects.mssql.TIMESTAMP).

This is a read-only datatype that does not support INSERT of values.

Added in version 1.2.

See also

[TIMESTAMP](#sqlalchemy.dialects.mssql.TIMESTAMP)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a TIMESTAMP or ROWVERSION type. |

   method [sqlalchemy.dialects.mssql.ROWVERSION.](#sqlalchemy.dialects.mssql.ROWVERSION)__init__(*convert_int=False*)

*inherited from the* `sqlalchemy.dialects.mssql.base.TIMESTAMP.__init__` *method of* [TIMESTAMP](#sqlalchemy.dialects.mssql.TIMESTAMP)

Construct a TIMESTAMP or ROWVERSION type.

  Parameters:

**convert_int** – if True, binary integer values will
be converted to integers on read.

Added in version 1.2.

      class sqlalchemy.dialects.mssql.SMALLDATETIME

*inherits from* `sqlalchemy.dialects.mssql.base._DateTimeBase`, [sqlalchemy.types.DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newDateTime. |

   method [sqlalchemy.dialects.mssql.SMALLDATETIME.](#sqlalchemy.dialects.mssql.SMALLDATETIME)__init__(*timezone:bool=False*)

*inherited from the* `sqlalchemy.types.DateTime.__init__` *method of* [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime)

Construct a new [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime).

  Parameters:

**timezone** – boolean.  Indicates that the datetime type should
enable timezone support, if available on the
**base date/time-holding type only**.   It is recommended
to make use of the [TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP) datatype directly when
using this flag, as some databases include separate generic
date/time-holding types distinct from the timezone-capable
TIMESTAMP datatype, such as Oracle Database.

       class sqlalchemy.dialects.mssql.SMALLMONEY

*inherits from* [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

     class sqlalchemy.dialects.mssql.SQL_VARIANT

*inherits from* [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

     class sqlalchemy.dialects.mssql.TEXT

*inherits from* [sqlalchemy.types.Text](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Text)

The SQL TEXT type.

   method [sqlalchemy.dialects.mssql.TEXT.](#sqlalchemy.dialects.mssql.TEXT)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) or [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.dialects.mssql.TIME

*inherits from* [sqlalchemy.types.TIME](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIME)

     class sqlalchemy.dialects.mssql.TIMESTAMP

*inherits from* `sqlalchemy.types._Binary`

Implement the SQL Server TIMESTAMP type.

Note this is **completely different** than the SQL Standard
TIMESTAMP type, which is not supported by SQL Server.  It
is a read-only datatype that does not support INSERT of values.

Added in version 1.2.

See also

[ROWVERSION](#sqlalchemy.dialects.mssql.ROWVERSION)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a TIMESTAMP or ROWVERSION type. |

   method [sqlalchemy.dialects.mssql.TIMESTAMP.](#sqlalchemy.dialects.mssql.TIMESTAMP)__init__(*convert_int=False*)

Construct a TIMESTAMP or ROWVERSION type.

  Parameters:

**convert_int** – if True, binary integer values will
be converted to integers on read.

Added in version 1.2.

      class sqlalchemy.dialects.mssql.TINYINT

*inherits from* [sqlalchemy.types.Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer)

     class sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER

*inherits from* [sqlalchemy.types.Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid)

| Member Name | Description |
| --- | --- |
| __init__() | Construct aUNIQUEIDENTIFIERtype. |

   method [sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER.](#sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER)__init__(*as_uuid:bool=True*)

Construct a [UNIQUEIDENTIFIER](#sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER) type.

  Parameters:

**as_uuid=True** –

if True, values will be interpreted
as Python uuid objects, converting to/from string via the
DBAPI.

       class sqlalchemy.dialects.mssql.VARBINARY

*inherits from* [sqlalchemy.types.VARBINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARBINARY), [sqlalchemy.types.LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary)

The MSSQL VARBINARY type.

This type adds additional features to the core [VARBINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARBINARY)
type, including “deprecate_large_types” mode where
either `VARBINARY(max)` or IMAGE is rendered, as well as the SQL
Server `FILESTREAM` option.

See also

[Large Text/Binary Type Deprecation](#mssql-large-type-deprecation)

    method [sqlalchemy.dialects.mssql.VARBINARY.](#sqlalchemy.dialects.mssql.VARBINARY)__init__(*length=None*, *filestream=False*)

Construct a VARBINARY type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL statements, for those binary types that accept a length,
  such as the MySQL BLOB type.
- **filestream=False** –
  if True, renders the `FILESTREAM` keyword
  in the table definition. In this case `length` must be `None`
  or `'max'`.
  Added in version 1.4.31.

       class sqlalchemy.dialects.mssql.VARCHAR

*inherits from* [sqlalchemy.types.String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

The SQL VARCHAR type.

   method [sqlalchemy.dialects.mssql.VARCHAR.](#sqlalchemy.dialects.mssql.VARCHAR)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) or [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.dialects.mssql.XML

*inherits from* [sqlalchemy.types.Text](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Text)

MSSQL XML type.

This is a placeholder type for reflection purposes that does not include
any Python-side datatype support.   It also does not currently support
additional arguments, such as “CONTENT”, “DOCUMENT”,
“xml_schema_collection”.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |

   method [sqlalchemy.dialects.mssql.XML.](#sqlalchemy.dialects.mssql.XML)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) or [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

## PyODBC

Support for the Microsoft SQL Server database via the PyODBC driver.

### DBAPI

Documentation and download information (if applicable) for PyODBC is available at:
[https://pypi.org/project/pyodbc/](https://pypi.org/project/pyodbc/)

### Connecting

Connect String:

```
mssql+pyodbc://<username>:<password>@<dsnname>
```

### Connecting to PyODBC

The URL here is to be translated to PyODBC connection strings, as
detailed in [ConnectionStrings](https://code.google.com/p/pyodbc/wiki/ConnectionStrings).

#### DSN Connections

A DSN connection in ODBC means that a pre-existing ODBC datasource is
configured on the client machine.   The application then specifies the name
of this datasource, which encompasses details such as the specific ODBC driver
in use as well as the network address of the database.   Assuming a datasource
is configured on the client, a basic DSN-based connection looks like:

```
engine = create_engine("mssql+pyodbc://scott:tiger@some_dsn")
```

Which above, will pass the following connection string to PyODBC:

```
DSN=some_dsn;UID=scott;PWD=tiger
```

If the username and password are omitted, the DSN form will also add
the `Trusted_Connection=yes` directive to the ODBC string.

#### Hostname Connections

Hostname-based connections are also supported by pyodbc.  These are often
easier to use than a DSN and have the additional advantage that the specific
database name to connect towards may be specified locally in the URL, rather
than it being fixed as part of a datasource configuration.

When using a hostname connection, the driver name must also be specified in the
query parameters of the URL.  As these names usually have spaces in them, the
name must be URL encoded which means using plus signs for spaces:

```
engine = create_engine(
    "mssql+pyodbc://scott:tiger@myhost:port/databasename?driver=ODBC+Driver+17+for+SQL+Server"
)
```

The `driver` keyword is significant to the pyodbc dialect and must be
specified in lowercase.

Any other names passed in the query string are passed through in the pyodbc
connect string, such as `authentication`, `TrustServerCertificate`, etc.
Multiple keyword arguments must be separated by an ampersand (`&`); these
will be translated to semicolons when the pyodbc connect string is generated
internally:

```
e = create_engine(
    "mssql+pyodbc://scott:tiger@mssql2017:1433/test?"
    "driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    "&authentication=ActiveDirectoryIntegrated"
)
```

The equivalent URL can be constructed using [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL):

```
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mssql+pyodbc",
    username="scott",
    password="tiger",
    host="mssql2017",
    port=1433,
    database="test",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",
        "authentication": "ActiveDirectoryIntegrated",
    },
)
```

#### Pass through exact Pyodbc string

A PyODBC connection string can also be sent in pyodbc’s format directly, as
specified in [the PyODBC documentation](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-databases),
using the parameter `odbc_connect`.  A [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object
can help make this easier:

```
from sqlalchemy.engine import URL

connection_string = "DRIVER={SQL Server Native Client 10.0};SERVER=dagger;DATABASE=test;UID=user;PWD=password"
connection_url = URL.create(
    "mssql+pyodbc", query={"odbc_connect": connection_string}
)

engine = create_engine(connection_url)
```

#### Connecting to databases with access tokens

Some database servers are set up to only accept access tokens for login. For
example, SQL Server allows the use of Azure Active Directory tokens to connect
to databases. This requires creating a credential object using the
`azure-identity` library. More information about the authentication step can be
found in [Microsoft’s documentation](https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=bash).

After getting an engine, the credentials need to be sent to `pyodbc.connect`
each time a connection is requested. One way to do this is to set up an event
listener on the engine that adds the credential token to the dialect’s connect
call. This is discussed more generally in [Generating dynamic authentication tokens](https://docs.sqlalchemy.org/en/20/core/engines.html#engines-dynamic-tokens). For
SQL Server in particular, this is passed as an ODBC connection attribute with
a data structure [described by Microsoft](https://docs.microsoft.com/en-us/sql/connect/odbc/using-azure-active-directory#authenticating-with-an-access-token).

The following code snippet will create an engine that connects to an Azure SQL
database using Azure credentials:

```
import struct
from sqlalchemy import create_engine, event
from sqlalchemy.engine.url import URL
from azure import identity

# Connection option for access tokens, as defined in msodbcsql.h
SQL_COPT_SS_ACCESS_TOKEN = 1256
TOKEN_URL = "https://database.windows.net/"  # The token URL for any Azure SQL database

connection_string = "mssql+pyodbc://@my-server.database.windows.net/myDb?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(connection_string)

azure_credentials = identity.DefaultAzureCredential()

@event.listens_for(engine, "do_connect")
def provide_token(dialect, conn_rec, cargs, cparams):
    # remove the "Trusted_Connection" parameter that SQLAlchemy adds
    cargs[0] = cargs[0].replace(";Trusted_Connection=Yes", "")

    # create token credential
    raw_token = azure_credentials.get_token(TOKEN_URL).token.encode(
        "utf-16-le"
    )
    token_struct = struct.pack(
        f"<I{len(raw_token)}s", len(raw_token), raw_token
    )

    # apply it to keyword arguments
    cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}
```

Tip

The `Trusted_Connection` token is currently added by the SQLAlchemy
pyodbc dialect when no username or password is present.  This needs
to be removed per Microsoft’s
[documentation for Azure access tokens](https://docs.microsoft.com/en-us/sql/connect/odbc/using-azure-active-directory#authenticating-with-an-access-token),
stating that a connection string when using an access token must not contain
`UID`, `PWD`, `Authentication` or `Trusted_Connection` parameters.

#### Avoiding transaction-related exceptions on Azure Synapse Analytics

Azure Synapse Analytics has a significant difference in its transaction
handling compared to plain SQL Server; in some cases an error within a Synapse
transaction can cause it to be arbitrarily terminated on the server side, which
then causes the DBAPI `.rollback()` method (as well as `.commit()`) to
fail. The issue prevents the usual DBAPI contract of allowing `.rollback()`
to pass silently if no transaction is present as the driver does not expect
this condition. The symptom of this failure is an exception with a message
resembling ‘No corresponding transaction found. (111214)’ when attempting to
emit a `.rollback()` after an operation had a failure of some kind.

This specific case can be handled by passing `ignore_no_transaction_on_rollback=True` to
the SQL Server dialect via the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) function as follows:

```
engine = create_engine(
    connection_url, ignore_no_transaction_on_rollback=True
)
```

Using the above parameter, the dialect will catch `ProgrammingError`
exceptions raised during `connection.rollback()` and emit a warning
if the error message contains code `111214`, however will not raise
an exception.

Added in version 1.4.40: Added the
`ignore_no_transaction_on_rollback=True` parameter.

#### Enable autocommit for Azure SQL Data Warehouse (DW) connections

Azure SQL Data Warehouse does not support transactions,
and that can cause problems with SQLAlchemy’s “autobegin” (and implicit
commit/rollback) behavior. We can avoid these problems by enabling autocommit
at both the pyodbc and engine levels:

```
connection_url = sa.engine.URL.create(
    "mssql+pyodbc",
    username="scott",
    password="tiger",
    host="dw.azure.example.com",
    database="mydb",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "autocommit": "True",
    },
)

engine = create_engine(connection_url).execution_options(
    isolation_level="AUTOCOMMIT"
)
```

#### Avoiding sending large string parameters as TEXT/NTEXT

By default, for historical reasons, Microsoft’s ODBC drivers for SQL Server
send long string parameters (greater than 4000 SBCS characters or 2000 Unicode
characters) as TEXT/NTEXT values. TEXT and NTEXT have been deprecated for many
years and are starting to cause compatibility issues with newer versions of
SQL_Server/Azure. For example, see [this
issue](https://github.com/mkleehammer/pyodbc/issues/835).

Starting with ODBC Driver 18 for SQL Server we can override the legacy
behavior and pass long strings as varchar(max)/nvarchar(max) using the
`LongAsMax=Yes` connection string parameter:

```
connection_url = sa.engine.URL.create(
    "mssql+pyodbc",
    username="scott",
    password="tiger",
    host="mssqlserver.example.com",
    database="mydb",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "LongAsMax": "Yes",
    },
)
```

### Pyodbc Pooling / connection close behavior

PyODBC uses internal [pooling](https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#pooling) by
default, which means connections will be longer lived than they are within
SQLAlchemy itself.  As SQLAlchemy has its own pooling behavior, it is often
preferable to disable this behavior.  This behavior can only be disabled
globally at the PyODBC module level, **before** any connections are made:

```
import pyodbc

pyodbc.pooling = False

# don't use the engine before pooling is set to False
engine = create_engine("mssql+pyodbc://user:pass@dsn")
```

If this variable is left at its default value of `True`, **the application
will continue to maintain active database connections**, even when the
SQLAlchemy engine itself fully discards a connection or if the engine is
disposed.

See also

[pooling](https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#pooling) -
in the PyODBC documentation.

### Driver / Unicode Support

PyODBC works best with Microsoft ODBC drivers, particularly in the area
of Unicode support on both Python 2 and Python 3.

Using the FreeTDS ODBC drivers on Linux or OSX with PyODBC is **not**
recommended; there have been historically many Unicode-related issues
in this area, including before Microsoft offered ODBC drivers for Linux
and OSX.   Now that Microsoft offers drivers for all platforms, for
PyODBC support these are recommended.  FreeTDS remains relevant for
non-ODBC drivers such as pymssql where it works very well.

### Rowcount Support

Previous limitations with the SQLAlchemy ORM’s “versioned rows” feature with
Pyodbc have been resolved as of SQLAlchemy 2.0.5. See the notes at
[Rowcount Support / ORM Versioning](#mssql-rowcount-versioning).

### Fast Executemany Mode

The PyODBC driver includes support for a “fast executemany” mode of execution
which greatly reduces round trips for a DBAPI `executemany()` call when using
Microsoft ODBC drivers, for **limited size batches that fit in memory**.  The
feature is enabled by setting the attribute `.fast_executemany` on the DBAPI
cursor when an executemany call is to be used.   The SQLAlchemy PyODBC SQL
Server dialect supports this parameter by passing the
`fast_executemany` parameter to
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) , when using the **Microsoft ODBC driver only**:

```
engine = create_engine(
    "mssql+pyodbc://scott:tiger@mssql2017:1433/test?driver=ODBC+Driver+17+for+SQL+Server",
    fast_executemany=True,
)
```

Changed in version 2.0.9: - the `fast_executemany` parameter now has its
intended effect of this PyODBC feature taking effect for all INSERT
statements that are executed with multiple parameter sets, which don’t
include RETURNING.  Previously, SQLAlchemy 2.0’s [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues)
feature would cause `fast_executemany` to not be used in most cases
even if specified.

Added in version 1.3.

See also

[fast executemany](https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany)
- on github

### Setinputsizes Support

As of version 2.0, the pyodbc `cursor.setinputsizes()` method is used for
all statement executions, except for `cursor.executemany()` calls when
fast_executemany=True where it is not supported (assuming
[insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) is kept enabled,
“fastexecutemany” will not take place for INSERT statements in any case).

The use of `cursor.setinputsizes()` can be disabled by passing
`use_setinputsizes=False` to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).

When `use_setinputsizes` is left at its default of `True`, the
specific per-type symbols passed to `cursor.setinputsizes()` can be
programmatically customized using the [DialectEvents.do_setinputsizes()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.do_setinputsizes)
hook. See that method for usage examples.

Changed in version 2.0: The mssql+pyodbc dialect now defaults to using
`use_setinputsizes=True` for all statement executions with the exception of
cursor.executemany() calls when fast_executemany=True.  The behavior can
be turned off by passing `use_setinputsizes=False` to
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).

## pymssql

Support for the Microsoft SQL Server database via the pymssql driver.

### Connecting

Connect String:

```
mssql+pymssql://<username>:<password>@<freetds_name>/?charset=utf8
```

pymssql is a Python module that provides a Python DBAPI interface around
[FreeTDS](https://www.freetds.org/).

Changed in version 2.0.5: pymssql was restored to SQLAlchemy’s continuous integration testing

## aioodbc

Support for the Microsoft SQL Server database via the aioodbc driver.

### DBAPI

Documentation and download information (if applicable) for aioodbc is available at:
[https://pypi.org/project/aioodbc/](https://pypi.org/project/aioodbc/)

### Connecting

Connect String:

```
mssql+aioodbc://<username>:<password>@<dsnname>
```

Support for the SQL Server database in asyncio style, using the aioodbc
driver which itself is a thread-wrapper around pyodbc.

Added in version 2.0.23: Added the mssql+aioodbc dialect which builds
on top of the pyodbc and general aio* dialect architecture.

Using a special asyncio mediation layer, the aioodbc dialect is usable
as the backend for the [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
extension package.

Most behaviors and caveats for this driver are the same as that of the
pyodbc dialect used on SQL Server; see [PyODBC](#mssql-pyodbc) for general
background.

This dialect should normally be used only with the
[create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) engine creation function; connection
styles are otherwise equivalent to those documented in the pyodbc section:

```
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "mssql+aioodbc://scott:tiger@mssql2017:1433/test?"
    "driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)
```
