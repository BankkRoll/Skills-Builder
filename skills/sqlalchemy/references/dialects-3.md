# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# MySQL and MariaDB

Support for the MySQL / MariaDB database.

The following table summarizes current support levels for database release versions.

| Support type | Versions |
| --- | --- |
| Supported version | 5.6+ / 10+ |
| Best effort | 5.0.2+ / 5.0.2+ |

## DBAPI Support

The following dialect/DBAPI options are available.  Please refer to individual DBAPI sections for connect information.

- [mysqlclient (maintained fork of MySQL-Python)](#module-sqlalchemy.dialects.mysql.mysqldb)
- [PyMySQL](#module-sqlalchemy.dialects.mysql.pymysql)
- [MariaDB Connector/Python](#module-sqlalchemy.dialects.mysql.mariadbconnector)
- [MySQL Connector/Python](#module-sqlalchemy.dialects.mysql.mysqlconnector)
- [asyncmy](#module-sqlalchemy.dialects.mysql.asyncmy)
- [aiomysql](#module-sqlalchemy.dialects.mysql.aiomysql)
- [CyMySQL](#module-sqlalchemy.dialects.mysql.cymysql)
- [PyODBC](#module-sqlalchemy.dialects.mysql.pyodbc)

## Supported Versions and Features

SQLAlchemy supports MySQL starting with version 5.0.2 through modern releases,
as well as all modern versions of MariaDB.   See the official MySQL
documentation for detailed information about features supported in any given
server release.

Changed in version 1.4: minimum MySQL version supported is now 5.0.2.

### MariaDB Support

The MariaDB variant of MySQL retains fundamental compatibility with MySQL’s
protocols however the development of these two products continues to diverge.
Within the realm of SQLAlchemy, the two databases have a small number of
syntactical and behavioral differences that SQLAlchemy accommodates automatically.
To connect to a MariaDB database, no changes to the database URL are required:

```
engine = create_engine(
    "mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4"
)
```

Upon first connect, the SQLAlchemy dialect employs a
server version detection scheme that determines if the
backing database reports as MariaDB.  Based on this flag, the dialect
can make different choices in those of areas where its behavior
must be different.

### MariaDB-Only Mode

The dialect also supports an **optional** “MariaDB-only” mode of connection, which may be
useful for the case where an application makes use of MariaDB-specific features
and is not compatible with a MySQL database.    To use this mode of operation,
replace the “mysql” token in the above URL with “mariadb”:

```
engine = create_engine(
    "mariadb+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4"
)
```

The above engine, upon first connect, will raise an error if the server version
detection detects that the backing database is not MariaDB.

When using an engine with `"mariadb"` as the dialect name, **all mysql-specific options
that include the name “mysql” in them are now named with “mariadb”**.  This means
options like `mysql_engine` should be named `mariadb_engine`, etc.  Both
“mysql” and “mariadb” options can be used simultaneously for applications that
use URLs with both “mysql” and “mariadb” dialects:

```
my_table = Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("textdata", String(50)),
    mariadb_engine="InnoDB",
    mysql_engine="InnoDB",
)

Index(
    "textdata_ix",
    my_table.c.textdata,
    mysql_prefix="FULLTEXT",
    mariadb_prefix="FULLTEXT",
)
```

Similar behavior will occur when the above structures are reflected, i.e. the
“mariadb” prefix will be present in the option names when the database URL
is based on the “mariadb” name.

Added in version 1.4: Added “mariadb” dialect name supporting “MariaDB-only mode”
for the MySQL dialect.

## Connection Timeouts and Disconnects

MySQL / MariaDB feature an automatic connection close behavior, for connections that
have been idle for a fixed period of time, defaulting to eight hours.
To circumvent having this issue, use
the [create_engine.pool_recycle](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_recycle) option which ensures that
a connection will be discarded and replaced with a new one if it has been
present in the pool for a fixed number of seconds:

```
engine = create_engine("mysql+mysqldb://...", pool_recycle=3600)
```

For more comprehensive disconnect detection of pooled connections, including
accommodation of  server restarts and network issues, a pre-ping approach may
be employed.  See [Dealing with Disconnects](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects) for current approaches.

See also

[Dealing with Disconnects](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects) - Background on several techniques for dealing
with timed out connections as well as database restarts.

## CREATE TABLE arguments including Storage Engines

Both MySQL’s and MariaDB’s CREATE TABLE syntax includes a wide array of special options,
including `ENGINE`, `CHARSET`, `MAX_ROWS`, `ROW_FORMAT`,
`INSERT_METHOD`, and many more.
To accommodate the rendering of these arguments, specify the form
`mysql_argument_name="value"`.  For example, to specify a table with
`ENGINE` of `InnoDB`, `CHARSET` of `utf8mb4`, and `KEY_BLOCK_SIZE`
of `1024`:

```
Table(
    "mytable",
    metadata,
    Column("data", String(32)),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
    mysql_key_block_size="1024",
)
```

When supporting [MariaDB-Only Mode](#mysql-mariadb-only-mode) mode, similar keys against
the “mariadb” prefix must be included as well.  The values can of course
vary independently so that different settings on MySQL vs. MariaDB may
be maintained:

```
# support both "mysql" and "mariadb-only" engine URLs

Table(
    "mytable",
    metadata,
    Column("data", String(32)),
    mysql_engine="InnoDB",
    mariadb_engine="InnoDB",
    mysql_charset="utf8mb4",
    mariadb_charset="utf8",
    mysql_key_block_size="1024",
    mariadb_key_block_size="1024",
)
```

The MySQL / MariaDB dialects will normally transfer any keyword specified as
`mysql_keyword_name` to be rendered as `KEYWORD_NAME` in the
`CREATE TABLE` statement.  A handful of these names will render with a space
instead of an underscore; to support this, the MySQL dialect has awareness of
these particular names, which include `DATA DIRECTORY`
(e.g. `mysql_data_directory`), `CHARACTER SET` (e.g.
`mysql_character_set`) and `INDEX DIRECTORY` (e.g.
`mysql_index_directory`).

The most common argument is `mysql_engine`, which refers to the storage
engine for the table.  Historically, MySQL server installations would default
to `MyISAM` for this value, although newer versions may be defaulting
to `InnoDB`.  The `InnoDB` engine is typically preferred for its support
of transactions and foreign keys.

A [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
that is created in a MySQL / MariaDB database with a storage engine
of `MyISAM` will be essentially non-transactional, meaning any
INSERT/UPDATE/DELETE statement referring to this table will be invoked as
autocommit.   It also will have no support for foreign key constraints; while
the `CREATE TABLE` statement accepts foreign key options, when using the
`MyISAM` storage engine these arguments are discarded.  Reflecting such a
table will also produce no foreign key constraint information.

For fully atomic transactions as well as support for foreign key
constraints, all participating `CREATE TABLE` statements must specify a
transactional engine, which in the vast majority of cases is `InnoDB`.

Partitioning can similarly be specified using similar options.
In the example below the create table will specify `PARTITION_BY`,
`PARTITIONS`, `SUBPARTITIONS` and `SUBPARTITION_BY`:

```
# can also use mariadb_* prefix
Table(
    "testtable",
    MetaData(),
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("other_id", Integer(), primary_key=True, autoincrement=False),
    mysql_partitions="2",
    mysql_partition_by="KEY(other_id)",
    mysql_subpartition_by="HASH(some_expr)",
    mysql_subpartitions="2",
)
```

This will render:

```
CREATE TABLE testtable (
        id INTEGER NOT NULL AUTO_INCREMENT,
        other_id INTEGER NOT NULL,
        PRIMARY KEY (id, other_id)
)PARTITION BY KEY(other_id) PARTITIONS 2 SUBPARTITION BY HASH(some_expr) SUBPARTITIONS 2
```

## Case Sensitivity and Table Reflection

Both MySQL and MariaDB have inconsistent support for case-sensitive identifier
names, basing support on specific details of the underlying
operating system. However, it has been observed that no matter
what case sensitivity behavior is present, the names of tables in
foreign key declarations are *always* received from the database
as all-lower case, making it impossible to accurately reflect a
schema where inter-related tables use mixed-case identifier names.

Therefore it is strongly advised that table names be declared as
all lower case both within SQLAlchemy as well as on the MySQL / MariaDB
database itself, especially if database reflection features are
to be used.

## Transaction Isolation Level

All MySQL / MariaDB dialects support setting of transaction isolation level both via a
dialect-specific parameter [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level)
accepted
by [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine), as well as the
[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) argument as passed to
[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options).
This feature works by issuing the
command `SET SESSION TRANSACTION ISOLATION LEVEL <level>` for each new
connection.  For the special AUTOCOMMIT isolation level, DBAPI-specific
techniques are used.

To set isolation level using [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine):

```
engine = create_engine(
    "mysql+mysqldb://scott:tiger@localhost/test",
    isolation_level="READ UNCOMMITTED",
)
```

To set using per-connection execution options:

```
connection = engine.connect()
connection = connection.execution_options(isolation_level="READ COMMITTED")
```

Valid values for `isolation_level` include:

- `READ COMMITTED`
- `READ UNCOMMITTED`
- `REPEATABLE READ`
- `SERIALIZABLE`
- `AUTOCOMMIT`

The special `AUTOCOMMIT` value makes use of the various “autocommit”
attributes provided by specific DBAPIs, and is currently supported by
MySQLdb, MySQL-Client, MySQL-Connector Python, and PyMySQL.   Using it,
the database connection will return true for the value of
`SELECT @@autocommit;`.

There are also more options for isolation level configurations, such as
“sub-engine” objects linked to a main [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which each apply
different isolation level settings.  See the discussion at
[Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit) for background.

See also

[Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit)

## AUTO_INCREMENT Behavior

When creating tables, SQLAlchemy will automatically set `AUTO_INCREMENT` on
the first [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) primary key column which is not marked as a
foreign key:

```
>>> t = Table(
...     "mytable", metadata, Column("mytable_id", Integer, primary_key=True)
... )
>>> t.create()
CREATE TABLE mytable (
        id INTEGER NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (id)
)
```

You can disable this behavior by passing `False` to the
[Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement) argument of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).
This flag
can also be used to enable auto-increment on a secondary column in a
multi-column key for some storage engines:

```
Table(
    "mytable",
    metadata,
    Column("gid", Integer, primary_key=True, autoincrement=False),
    Column("id", Integer, primary_key=True),
)
```

## Server Side Cursors

Server-side cursor support is available for the mysqlclient, PyMySQL,
mariadbconnector dialects and may also be available in others.   This makes use
of either the “buffered=True/False” flag if available or by using a class such
as `MySQLdb.cursors.SSCursor` or `pymysql.cursors.SSCursor` internally.

Server side cursors are enabled on a per-statement basis by using the
[Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results) connection execution
option:

```
with engine.connect() as conn:
    result = conn.execution_options(stream_results=True).execute(
        text("select * from table")
    )
```

Note that some kinds of SQL statements may not be supported with
server side cursors; generally, only SQL statements that return rows should be
used with this option.

Deprecated since version 1.4: The dialect-level server_side_cursors flag is deprecated
and will be removed in a future release.  Please use the
[Connection.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.params.stream_results) execution option for
unbuffered cursor support.

See also

[Using Server Side Cursors (a.k.a. stream results)](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results)

## Unicode

### Charset Selection

Most MySQL / MariaDB DBAPIs offer the option to set the client character set for
a connection.   This is typically delivered using the `charset` parameter
in the URL, such as:

```
e = create_engine(
    "mysql+pymysql://scott:tiger@localhost/test?charset=utf8mb4"
)
```

This charset is the **client character set** for the connection.  Some
MySQL DBAPIs will default this to a value such as `latin1`, and some
will make use of the `default-character-set` setting in the `my.cnf`
file as well.   Documentation for the DBAPI in use should be consulted
for specific behavior.

The encoding used for Unicode has traditionally been `'utf8'`.  However, for
MySQL versions 5.5.3 and MariaDB 5.5 on forward, a new MySQL-specific encoding
`'utf8mb4'` has been introduced, and as of MySQL 8.0 a warning is emitted by
the server if plain `utf8` is specified within any server-side directives,
replaced with `utf8mb3`.  The rationale for this new encoding is due to the
fact that MySQL’s legacy utf-8 encoding only supports codepoints up to three
bytes instead of four.  Therefore, when communicating with a MySQL or MariaDB
database that includes codepoints more than three bytes in size, this new
charset is preferred, if supported by both the database as well as the client
DBAPI, as in:

```
e = create_engine(
    "mysql+pymysql://scott:tiger@localhost/test?charset=utf8mb4"
)
```

All modern DBAPIs should support the `utf8mb4` charset.

In order to use `utf8mb4` encoding for a schema that was created with  legacy
`utf8`, changes to the MySQL/MariaDB schema and/or server configuration may be
required.

See also

[The utf8mb4 Character Set](https://dev.mysql.com/doc/refman/5.5/en/charset-unicode-utf8mb4.html) - in the MySQL documentation

### Dealing with Binary Data Warnings and Unicode

MySQL versions 5.6, 5.7 and later (not MariaDB at the time of this writing) now
emit a warning when attempting to pass binary data to the database, while a
character set encoding is also in place, when the binary data itself is not
valid for that encoding:

```
default.py:509: Warning: (1300, "Invalid utf8mb4 character string:
'F9876A'")
  cursor.execute(statement, parameters)
```

This warning is due to the fact that the MySQL client library is attempting to
interpret the binary string as a unicode object even if a datatype such
as [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) is in use.   To resolve this, the SQL statement requires
a binary “character set introducer” be present before any non-NULL value
that renders like this:

```
INSERT INTO table (data) VALUES (_binary %s)
```

These character set introducers are provided by the DBAPI driver, assuming the
use of mysqlclient or PyMySQL (both of which are recommended).  Add the query
string parameter `binary_prefix=true` to the URL to repair this warning:

```
# mysqlclient
engine = create_engine(
    "mysql+mysqldb://scott:tiger@localhost/test?charset=utf8mb4&binary_prefix=true"
)

# PyMySQL
engine = create_engine(
    "mysql+pymysql://scott:tiger@localhost/test?charset=utf8mb4&binary_prefix=true"
)
```

The `binary_prefix` flag may or may not be supported by other MySQL drivers.

SQLAlchemy itself cannot render this `_binary` prefix reliably, as it does
not work with the NULL value, which is valid to be sent as a bound parameter.
As the MySQL driver renders parameters directly into the SQL string, it’s the
most efficient place for this additional keyword to be passed.

See also

[Character set introducers](https://dev.mysql.com/doc/refman/5.7/en/charset-introducer.html) - on the MySQL website

## ANSI Quoting Style

MySQL / MariaDB feature two varieties of identifier “quoting style”, one using
backticks and the other using quotes, e.g. ``some_identifier``  vs.
`"some_identifier"`.   All MySQL dialects detect which version
is in use by checking the value of [sql_mode](#mysql-sql-mode) when a connection is first
established with a particular [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).
This quoting style comes
into play when rendering table and column names as well as when reflecting
existing database structures.  The detection is entirely automatic and
no special configuration is needed to use either quoting style.

## Changing the sql_mode

MySQL supports operating in multiple
[Server SQL Modes](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html)  for
both Servers and Clients. To change the `sql_mode` for a given application, a
developer can leverage SQLAlchemy’s Events system.

In the following example, the event system is used to set the `sql_mode` on
the `first_connect` and `connect` events:

```
from sqlalchemy import create_engine, event

eng = create_engine(
    "mysql+mysqldb://scott:tiger@localhost/test", echo="debug"
)

# `insert=True` will ensure this is the very first listener to run
@event.listens_for(eng, "connect", insert=True)
def connect(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET sql_mode = 'STRICT_ALL_TABLES'")

conn = eng.connect()
```

In the example illustrated above, the “connect” event will invoke the “SET”
statement on the connection at the moment a particular DBAPI connection is
first created for a given Pool, before the connection is made available to the
connection pool.  Additionally, because the function was registered with
`insert=True`, it will be prepended to the internal list of registered
functions.

## MySQL / MariaDB SQL Extensions

Many of the MySQL / MariaDB SQL extensions are handled through SQLAlchemy’s generic
function and operator support:

```
table.select(table.c.password == func.md5("plaintext"))
table.select(table.c.username.op("regexp")("^[a-d]"))
```

And of course any valid SQL statement can be executed as a string as well.

Some limited direct support for MySQL / MariaDB extensions to SQL is currently
available.

- INSERT..ON DUPLICATE KEY UPDATE:  See
  [INSERT…ON DUPLICATE KEY UPDATE (Upsert)](#mysql-insert-on-duplicate-key-update)
- SELECT pragma, use [Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) and
  [Query.prefix_with()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.prefix_with):
  ```
  select(...).prefix_with(["HIGH_PRIORITY", "SQL_SMALL_RESULT"])
  ```
- UPDATE with LIMIT:
  ```
  update(...).with_dialect_options(mysql_limit=10, mariadb_limit=10)
  ```
- DELETE
  with LIMIT:
  ```
  delete(...).with_dialect_options(mysql_limit=10, mariadb_limit=10)
  ```
  Added in version 2.0.37: Added delete with limit
- optimizer hints, use [Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) and
  [Query.prefix_with()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.prefix_with):
  ```
  select(...).prefix_with("/*+ NO_RANGE_OPTIMIZATION(t4 PRIMARY) */")
  ```
- index hints, use [Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) and
  [Query.with_hint()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_hint):
  ```
  select(...).with_hint(some_table, "USE INDEX xyz")
  ```
- MATCH
  operator support:
  ```
  from sqlalchemy.dialects.mysql import match
  select(...).where(match(col1, col2, against="some expr").in_boolean_mode())
  ```
  See also
  [match](#sqlalchemy.dialects.mysql.match)

## INSERT/DELETE…RETURNING

The MariaDB dialect supports 10.5+’s `INSERT..RETURNING` and
`DELETE..RETURNING` (10.0+) syntaxes.   `INSERT..RETURNING` may be used
automatically in some cases in order to fetch newly generated identifiers in
place of the traditional approach of using `cursor.lastrowid`, however
`cursor.lastrowid` is currently still preferred for simple single-statement
cases for its better performance.

To specify an explicit `RETURNING` clause, use the
`_UpdateBase.returning()` method on a per-statement basis:

```
# INSERT..RETURNING
result = connection.execute(
    table.insert().values(name="foo").returning(table.c.col1, table.c.col2)
)
print(result.all())

# DELETE..RETURNING
result = connection.execute(
    table.delete()
    .where(table.c.name == "foo")
    .returning(table.c.col1, table.c.col2)
)
print(result.all())
```

Added in version 2.0: Added support for MariaDB RETURNING

## INSERT…ON DUPLICATE KEY UPDATE (Upsert)

MySQL / MariaDB allow “upserts” (update or insert)
of rows into a table via the `ON DUPLICATE KEY UPDATE` clause of the
`INSERT` statement.  A candidate row will only be inserted if that row does
not match an existing primary or unique key in the table; otherwise, an UPDATE
will be performed.   The statement allows for separate specification of the
values to INSERT versus the values for UPDATE.

SQLAlchemy provides `ON DUPLICATE KEY UPDATE` support via the MySQL-specific
[insert()](#sqlalchemy.dialects.mysql.insert) function, which provides
the generative method [Insert.on_duplicate_key_update()](#sqlalchemy.dialects.mysql.Insert.on_duplicate_key_update):

```
>>> from sqlalchemy.dialects.mysql import insert

>>> insert_stmt = insert(my_table).values(
...     id="some_existing_id", data="inserted value"
... )

>>> on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
...     data=insert_stmt.inserted.data, status="U"
... )
>>> print(on_duplicate_key_stmt)
INSERT INTO my_table (id, data) VALUES (%s, %s)
ON DUPLICATE KEY UPDATE data = VALUES(data), status = %s
```

Unlike PostgreSQL’s “ON CONFLICT” phrase, the “ON DUPLICATE KEY UPDATE”
phrase will always match on any primary key or unique key, and will always
perform an UPDATE if there’s a match; there are no options for it to raise
an error or to skip performing an UPDATE.

`ON DUPLICATE KEY UPDATE` is used to perform an update of the already
existing row, using any combination of new values as well as values
from the proposed insertion.   These values are normally specified using
keyword arguments passed to the
[Insert.on_duplicate_key_update()](#sqlalchemy.dialects.mysql.Insert.on_duplicate_key_update)
given column key values (usually the name of the column, unless it
specifies [Column.key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.key)
) as keys and literal or SQL expressions
as values:

```
>>> insert_stmt = insert(my_table).values(
...     id="some_existing_id", data="inserted value"
... )

>>> on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
...     data="some data",
...     updated_at=func.current_timestamp(),
... )

>>> print(on_duplicate_key_stmt)
INSERT INTO my_table (id, data) VALUES (%s, %s)
ON DUPLICATE KEY UPDATE data = %s, updated_at = CURRENT_TIMESTAMP
```

In a manner similar to that of `UpdateBase.values()`, other parameter
forms are accepted, including a single dictionary:

```
>>> on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
...     {"data": "some data", "updated_at": func.current_timestamp()},
... )
```

as well as a list of 2-tuples, which will automatically provide
a parameter-ordered UPDATE statement in a manner similar to that described
at [Parameter Ordered Updates](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-parameter-ordered-updates).  Unlike the [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)
object,
no special flag is needed to specify the intent since the argument form is
this context is unambiguous:

```
>>> on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
...     [
...         ("data", "some data"),
...         ("updated_at", func.current_timestamp()),
...     ]
... )

>>> print(on_duplicate_key_stmt)
INSERT INTO my_table (id, data) VALUES (%s, %s)
ON DUPLICATE KEY UPDATE data = %s, updated_at = CURRENT_TIMESTAMP
```

Changed in version 1.3: support for parameter-ordered UPDATE clause within
MySQL ON DUPLICATE KEY UPDATE

Warning

The [Insert.on_duplicate_key_update()](#sqlalchemy.dialects.mysql.Insert.on_duplicate_key_update)
method does **not** take into
account Python-side default UPDATE values or generation functions, e.g.
e.g. those specified using [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate).
These values will not be exercised for an ON DUPLICATE KEY style of UPDATE,
unless they are manually specified explicitly in the parameters.

In order to refer to the proposed insertion row, the special alias
[Insert.inserted](#sqlalchemy.dialects.mysql.Insert.inserted) is available as an attribute on
the [Insert](#sqlalchemy.dialects.mysql.Insert) object; this object is a
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) which contains all columns of the target
table:

```
>>> stmt = insert(my_table).values(
...     id="some_id", data="inserted value", author="jlh"
... )

>>> do_update_stmt = stmt.on_duplicate_key_update(
...     data="updated value", author=stmt.inserted.author
... )

>>> print(do_update_stmt)
INSERT INTO my_table (id, data, author) VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE data = %s, author = VALUES(author)
```

When rendered, the “inserted” namespace will produce the expression
`VALUES(<columnname>)`.

Added in version 1.2: Added support for MySQL ON DUPLICATE KEY UPDATE clause

## rowcount Support

SQLAlchemy standardizes the DBAPI `cursor.rowcount` attribute to be the
usual definition of “number of rows matched by an UPDATE or DELETE” statement.
This is in contradiction to the default setting on most MySQL DBAPI drivers,
which is “number of rows actually modified/deleted”.  For this reason, the
SQLAlchemy MySQL dialects always add the `constants.CLIENT.FOUND_ROWS`
flag, or whatever is equivalent for the target dialect, upon connection.
This setting is currently hardcoded.

See also

[CursorResult.rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount)

## MySQL / MariaDB- Specific Index Options

MySQL and MariaDB-specific extensions to the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct are available.

### Index Length

MySQL and MariaDB both provide an option to create index entries with a certain length, where
“length” refers to the number of characters or bytes in each value which will
become part of the index. SQLAlchemy provides this feature via the
`mysql_length` and/or `mariadb_length` parameters:

```
Index("my_index", my_table.c.data, mysql_length=10, mariadb_length=10)

Index("a_b_idx", my_table.c.a, my_table.c.b, mysql_length={"a": 4, "b": 9})

Index(
    "a_b_idx", my_table.c.a, my_table.c.b, mariadb_length={"a": 4, "b": 9}
)
```

Prefix lengths are given in characters for nonbinary string types and in bytes
for binary string types. The value passed to the keyword argument *must* be
either an integer (and, thus, specify the same prefix length value for all
columns of the index) or a dict in which keys are column names and values are
prefix length values for corresponding columns. MySQL and MariaDB only allow a
length for a column of an index if it is for a CHAR, VARCHAR, TEXT, BINARY,
VARBINARY and BLOB.

### Index Prefixes

MySQL storage engines permit you to specify an index prefix when creating
an index. SQLAlchemy provides this feature via the
`mysql_prefix` parameter on [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index):

```
Index("my_index", my_table.c.data, mysql_prefix="FULLTEXT")
```

The value passed to the keyword argument will be simply passed through to the
underlying CREATE INDEX, so it *must* be a valid index prefix for your MySQL
storage engine.

See also

[CREATE INDEX](https://dev.mysql.com/doc/refman/5.0/en/create-index.html) - MySQL documentation

### Index Types

Some MySQL storage engines permit you to specify an index type when creating
an index or primary key constraint. SQLAlchemy provides this feature via the
`mysql_using` parameter on [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index):

```
Index(
    "my_index", my_table.c.data, mysql_using="hash", mariadb_using="hash"
)
```

As well as the `mysql_using` parameter on [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint):

```
PrimaryKeyConstraint("data", mysql_using="hash", mariadb_using="hash")
```

The value passed to the keyword argument will be simply passed through to the
underlying CREATE INDEX or PRIMARY KEY clause, so it *must* be a valid index
type for your MySQL storage engine.

More information can be found at:

[https://dev.mysql.com/doc/refman/5.0/en/create-index.html](https://dev.mysql.com/doc/refman/5.0/en/create-index.html)

[https://dev.mysql.com/doc/refman/5.0/en/create-table.html](https://dev.mysql.com/doc/refman/5.0/en/create-table.html)

### Index Parsers

CREATE FULLTEXT INDEX in MySQL also supports a “WITH PARSER” option.  This
is available using the keyword argument `mysql_with_parser`:

```
Index(
    "my_index",
    my_table.c.data,
    mysql_prefix="FULLTEXT",
    mysql_with_parser="ngram",
    mariadb_prefix="FULLTEXT",
    mariadb_with_parser="ngram",
)
```

Added in version 1.3.

## MySQL / MariaDB Foreign Keys

MySQL and MariaDB’s behavior regarding foreign keys has some important caveats.

### Foreign Key Arguments to Avoid

Neither MySQL nor MariaDB support the foreign key arguments “DEFERRABLE”, “INITIALLY”,
or “MATCH”.  Using the `deferrable` or `initially` keyword argument with
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) or [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)
will have the effect of
these keywords being rendered in a DDL expression, which will then raise an
error on MySQL or MariaDB.  In order to use these keywords on a foreign key while having
them ignored on a MySQL / MariaDB backend, use a custom compile rule:

```
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import ForeignKeyConstraint

@compiles(ForeignKeyConstraint, "mysql", "mariadb")
def process(element, compiler, **kw):
    element.deferrable = element.initially = None
    return compiler.visit_foreign_key_constraint(element, **kw)
```

The “MATCH” keyword is in fact more insidious, and is explicitly disallowed
by SQLAlchemy in conjunction with the MySQL or MariaDB backends.  This argument is
silently ignored by MySQL / MariaDB, but in addition has the effect of ON UPDATE and ON
DELETE options also being ignored by the backend.   Therefore MATCH should
never be used with the MySQL / MariaDB backends; as is the case with DEFERRABLE and
INITIALLY, custom compilation rules can be used to correct a
ForeignKeyConstraint at DDL definition time.

### Reflection of Foreign Key Constraints

Not all MySQL / MariaDB storage engines support foreign keys.  When using the
very common `MyISAM` MySQL storage engine, the information loaded by table
reflection will not include foreign keys.  For these tables, you may supply a
`ForeignKeyConstraint` at reflection time:

```
Table(
    "mytable",
    metadata,
    ForeignKeyConstraint(["other_id"], ["othertable.other_id"]),
    autoload_with=engine,
)
```

See also

[CREATE TABLE arguments including Storage Engines](#mysql-storage-engines)

## MySQL / MariaDB Unique Constraints and Reflection

SQLAlchemy supports both the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct with the
flag `unique=True`, indicating a UNIQUE index, as well as the
[UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) construct, representing a UNIQUE constraint.
Both objects/syntaxes are supported by MySQL / MariaDB when emitting DDL to create
these constraints.  However, MySQL / MariaDB does not have a unique constraint
construct that is separate from a unique index; that is, the “UNIQUE”
constraint on MySQL / MariaDB is equivalent to creating a “UNIQUE INDEX”.

When reflecting these constructs, the
[Inspector.get_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes)
and the [Inspector.get_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints)
methods will **both**
return an entry for a UNIQUE index in MySQL / MariaDB.  However, when performing
full table reflection using `Table(..., autoload_with=engine)`,
the [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) construct is
**not** part of the fully reflected [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct under any
circumstances; this construct is always represented by a [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index)
with the `unique=True` setting present in the [Table.indexes](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.indexes)
collection.

## TIMESTAMP / DATETIME issues

### Rendering ON UPDATE CURRENT TIMESTAMP for MySQL / MariaDB’s explicit_defaults_for_timestamp

MySQL / MariaDB have historically expanded the DDL for the [TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP)
datatype into the phrase “TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE
CURRENT_TIMESTAMP”, which includes non-standard SQL that automatically updates
the column with the current timestamp when an UPDATE occurs, eliminating the
usual need to use a trigger in such a case where server-side update changes are
desired.

MySQL 5.6 introduced a new flag [explicit_defaults_for_timestamp](https://dev.mysql.com/doc/refman/5.6/en/server-system-variables.html#sysvar_explicit_defaults_for_timestamp) which disables the above behavior,
and in MySQL 8 this flag defaults to true, meaning in order to get a MySQL
“on update timestamp” without changing this flag, the above DDL must be
rendered explicitly.   Additionally, the same DDL is valid for use of the
`DATETIME` datatype as well.

SQLAlchemy’s MySQL dialect does not yet have an option to generate
MySQL’s “ON UPDATE CURRENT_TIMESTAMP” clause, noting that this is not a general
purpose “ON UPDATE” as there is no such syntax in standard SQL.  SQLAlchemy’s
[Column.server_onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_onupdate) parameter is currently not related
to this special MySQL behavior.

To generate this DDL, make use of the [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default)
parameter and pass a textual clause that also includes the ON UPDATE clause:

```
from sqlalchemy import Table, MetaData, Column, Integer, String, TIMESTAMP
from sqlalchemy import text

metadata = MetaData()

mytable = Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", String(50)),
    Column(
        "last_updated",
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        ),
    ),
)
```

The same instructions apply to use of the [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime) and
[DATETIME](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DATETIME) datatypes:

```
from sqlalchemy import DateTime

mytable = Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", String(50)),
    Column(
        "last_updated",
        DateTime,
        server_default=text(
            "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        ),
    ),
)
```

Even though the [Column.server_onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_onupdate) feature does not
generate this DDL, it still may be desirable to signal to the ORM that this
updated value should be fetched.  This syntax looks like the following:

```
from sqlalchemy.schema import FetchedValue

class MyClass(Base):
    __tablename__ = "mytable"

    id = Column(Integer, primary_key=True)
    data = Column(String(50))
    last_updated = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        ),
        server_onupdate=FetchedValue(),
    )
```

### TIMESTAMP Columns and NULL

MySQL historically enforces that a column which specifies the
TIMESTAMP datatype implicitly includes a default value of
CURRENT_TIMESTAMP, even though this is not stated, and additionally
sets the column as NOT NULL, the opposite behavior vs. that of all
other datatypes:

```
mysql> CREATE TABLE ts_test (
    -> a INTEGER,
    -> b INTEGER NOT NULL,
    -> c TIMESTAMP,
    -> d TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -> e TIMESTAMP NULL);
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW CREATE TABLE ts_test;
+---------+-----------------------------------------------------
| Table   | Create Table
+---------+-----------------------------------------------------
| ts_test | CREATE TABLE `ts_test` (
  `a` int(11) DEFAULT NULL,
  `b` int(11) NOT NULL,
  `c` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `d` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `e` timestamp NULL DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1
```

Above, we see that an INTEGER column defaults to NULL, unless it is specified
with NOT NULL.   But when the column is of type TIMESTAMP, an implicit
default of CURRENT_TIMESTAMP is generated which also coerces the column
to be a NOT NULL, even though we did not specify it as such.

This behavior of MySQL can be changed on the MySQL side using the
[explicit_defaults_for_timestamp](https://dev.mysql.com/doc/refman/5.6/en/server-system-variables.html#sysvar_explicit_defaults_for_timestamp) configuration flag introduced in
MySQL 5.6.  With this server setting enabled, TIMESTAMP columns behave like
any other datatype on the MySQL side with regards to defaults and nullability.

However, to accommodate the vast majority of MySQL databases that do not
specify this new flag, SQLAlchemy emits the “NULL” specifier explicitly with
any TIMESTAMP column that does not specify `nullable=False`.   In order to
accommodate newer databases that specify `explicit_defaults_for_timestamp`,
SQLAlchemy also emits NOT NULL for TIMESTAMP columns that do specify
`nullable=False`.   The following example illustrates:

```
from sqlalchemy import MetaData, Integer, Table, Column, text
from sqlalchemy.dialects.mysql import TIMESTAMP

m = MetaData()
t = Table(
    "ts_test",
    m,
    Column("a", Integer),
    Column("b", Integer, nullable=False),
    Column("c", TIMESTAMP),
    Column("d", TIMESTAMP, nullable=False),
)

from sqlalchemy import create_engine

e = create_engine("mysql+mysqldb://scott:tiger@localhost/test", echo=True)
m.create_all(e)
```

output:

```
CREATE TABLE ts_test (
    a INTEGER,
    b INTEGER NOT NULL,
    c TIMESTAMP NULL,
    d TIMESTAMP NOT NULL
)
```

## MySQL SQL Constructs

| Object Name | Description |
| --- | --- |
| match | Produce aMATCH(X,Y)AGAINST('TEXT')clause. |

   class sqlalchemy.dialects.mysql.match

*inherits from* `sqlalchemy.sql.expression.Generative`, [sqlalchemy.sql.expression.BinaryExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BinaryExpression)

Produce a `MATCH (X, Y) AGAINST ('TEXT')` clause.

E.g.:

```
from sqlalchemy import desc
from sqlalchemy.dialects.mysql import match

match_expr = match(
    users_table.c.firstname,
    users_table.c.lastname,
    against="Firstname Lastname",
)

stmt = (
    select(users_table)
    .where(match_expr.in_boolean_mode())
    .order_by(desc(match_expr))
)
```

Would produce SQL resembling:

```
SELECT id, firstname, lastname
FROM user
WHERE MATCH(firstname, lastname) AGAINST (:param_1 IN BOOLEAN MODE)
ORDER BY MATCH(firstname, lastname) AGAINST (:param_2) DESC
```

The [match()](#sqlalchemy.dialects.mysql.match) function is a standalone version of the
[ColumnElement.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.match) method available on all
SQL expressions, as when [ColumnElement.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.match) is
used, but allows to pass multiple columns

  Parameters:

- **cols** – column expressions to match against
- **against** – expression to be compared towards
- **in_boolean_mode** – boolean, set “boolean mode” to true
- **in_natural_language_mode** – boolean , set “natural language” to true
- **with_query_expansion** – boolean, set “query expansion” to true

Added in version 1.4.19.

See also

[ColumnElement.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.match)

| Member Name | Description |
| --- | --- |
| in_boolean_mode() | Apply the “IN BOOLEAN MODE” modifier to the MATCH expression. |
| in_natural_language_mode() | Apply the “IN NATURAL LANGUAGE MODE” modifier to the MATCH
expression. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| with_query_expansion() | Apply the “WITH QUERY EXPANSION” modifier to the MATCH expression. |

   method [sqlalchemy.dialects.mysql.match.](#sqlalchemy.dialects.mysql.match)in_boolean_mode() → Self

Apply the “IN BOOLEAN MODE” modifier to the MATCH expression.

  Returns:

a new [match](#sqlalchemy.dialects.mysql.match) instance with modifications
applied.

      method [sqlalchemy.dialects.mysql.match.](#sqlalchemy.dialects.mysql.match)in_natural_language_mode() → Self

Apply the “IN NATURAL LANGUAGE MODE” modifier to the MATCH
expression.

  Returns:

a new [match](#sqlalchemy.dialects.mysql.match) instance with modifications
applied.

      attribute [sqlalchemy.dialects.mysql.match.](#sqlalchemy.dialects.mysql.match)inherit_cache = True

Indicate if this [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) instance should make use of the
cache key generation scheme used by its immediate superclass.

The attribute defaults to `None`, which indicates that a construct has
not yet taken into account whether or not its appropriate for it to
participate in caching; this is functionally equivalent to setting the
value to `False`, except that a warning is also emitted.

This flag can be set to `True` on a particular class, if the SQL that
corresponds to the object does not change based on attributes which
are local to this class, and not its superclass.

See also

[Enabling Caching Support for Custom Constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#compilerext-caching) - General guideslines for setting the
[HasCacheKey.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache) attribute for third-party or user
defined SQL constructs.

     method [sqlalchemy.dialects.mysql.match.](#sqlalchemy.dialects.mysql.match)with_query_expansion() → Self

Apply the “WITH QUERY EXPANSION” modifier to the MATCH expression.

  Returns:

a new [match](#sqlalchemy.dialects.mysql.match) instance with modifications
applied.

## MySQL Data Types

As with all SQLAlchemy dialects, all UPPERCASE types that are known to be
valid with MySQL are importable from the top level dialect:

```
from sqlalchemy.dialects.mysql import (
    BIGINT,
    BINARY,
    BIT,
    BLOB,
    BOOLEAN,
    CHAR,
    DATE,
    DATETIME,
    DECIMAL,
    DECIMAL,
    DOUBLE,
    ENUM,
    FLOAT,
    INTEGER,
    LONGBLOB,
    LONGTEXT,
    MEDIUMBLOB,
    MEDIUMINT,
    MEDIUMTEXT,
    NCHAR,
    NUMERIC,
    NVARCHAR,
    REAL,
    SET,
    SMALLINT,
    TEXT,
    TIME,
    TIMESTAMP,
    TINYBLOB,
    TINYINT,
    TINYTEXT,
    VARBINARY,
    VARCHAR,
    YEAR,
)
```

In addition to the above types, MariaDB also supports the following:

```
from sqlalchemy.dialects.mysql import (
    INET4,
    INET6,
)
```

Types which are specific to MySQL or MariaDB, or have specific
construction arguments, are as follows:

| Object Name | Description |
| --- | --- |
| BIGINT | MySQL BIGINTEGER type. |
| BIT | MySQL BIT type. |
| CHAR | MySQL CHAR type, for fixed-length character data. |
| DATETIME | MySQL DATETIME type. |
| DECIMAL | MySQL DECIMAL type. |
| ENUM | MySQL ENUM type. |
| FLOAT | MySQL FLOAT type. |
| INET4 | INET4 column type for MariaDB |
| INET6 | INET6 column type for MariaDB |
| INTEGER | MySQL INTEGER type. |
| JSON | MySQL JSON type. |
| LONGBLOB | MySQL LONGBLOB type, for binary data up to 2^32 bytes. |
| LONGTEXT | MySQL LONGTEXT type, for character storage encoded up to 2^32 bytes. |
| MEDIUMBLOB | MySQL MEDIUMBLOB type, for binary data up to 2^24 bytes. |
| MEDIUMINT | MySQL MEDIUMINTEGER type. |
| MEDIUMTEXT | MySQL MEDIUMTEXT type, for character storage encoded up
to 2^24 bytes. |
| NCHAR | MySQL NCHAR type. |
| NUMERIC | MySQL NUMERIC type. |
| NVARCHAR | MySQL NVARCHAR type. |
| REAL | MySQL REAL type. |
| SET | MySQL SET type. |
| SMALLINT | MySQL SMALLINTEGER type. |
| TIME | MySQL TIME type. |
| TIMESTAMP | MySQL TIMESTAMP type. |
| TINYBLOB | MySQL TINYBLOB type, for binary data up to 2^8 bytes. |
| TINYINT | MySQL TINYINT type. |
| TINYTEXT | MySQL TINYTEXT type, for character storage encoded up to 2^8 bytes. |
| VARCHAR | MySQL VARCHAR type, for variable-length character data. |
| YEAR | MySQL YEAR type, for single byte storage of years 1901-2155. |

   class sqlalchemy.dialects.mysql.BIGINT

*inherits from* `sqlalchemy.dialects.mysql.types._IntegerType`, [sqlalchemy.types.BIGINT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BIGINT)

MySQL BIGINTEGER type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a BIGINTEGER. |

   method [sqlalchemy.dialects.mysql.BIGINT.](#sqlalchemy.dialects.mysql.BIGINT)__init__(*display_width:int|None=None*, ***kw:Any*)

Construct a BIGINTEGER.

  Parameters:

- **display_width** – Optional, maximum display width for this number.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.BINARY

*inherits from* `sqlalchemy.types._Binary`

The SQL BINARY type.

    class sqlalchemy.dialects.mysql.BIT

*inherits from* [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

MySQL BIT type.

This type is for MySQL 5.0.3 or greater for MyISAM, and 5.0.5 or greater
for MyISAM, MEMORY, InnoDB and BDB.  For older versions, use a
MSTinyInteger() type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a BIT. |

   method [sqlalchemy.dialects.mysql.BIT.](#sqlalchemy.dialects.mysql.BIT)__init__(*length:int|None=None*)

Construct a BIT.

  Parameters:

**length** – Optional, number of bits.

       class sqlalchemy.dialects.mysql.BLOB

*inherits from* [sqlalchemy.types.LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary)

The SQL BLOB type.

   method [sqlalchemy.dialects.mysql.BLOB.](#sqlalchemy.dialects.mysql.BLOB)__init__(*length:int|None=None*)

*inherited from the* `sqlalchemy.types.LargeBinary.__init__` *method of* [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary)

Construct a LargeBinary type.

  Parameters:

**length** – optional, a length for the column for use in
DDL statements, for those binary types that accept a length,
such as the MySQL BLOB type.

       class sqlalchemy.dialects.mysql.BOOLEAN

*inherits from* [sqlalchemy.types.Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)

The SQL BOOLEAN type.

   method [sqlalchemy.dialects.mysql.BOOLEAN.](#sqlalchemy.dialects.mysql.BOOLEAN)__init__(*create_constraint:bool=False*, *name:str|None=None*, *_create_events:bool=True*, *_adapted_from:SchemaType|None=None*)

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

       class sqlalchemy.dialects.mysql.CHAR

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`, [sqlalchemy.types.CHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.CHAR)

MySQL CHAR type, for fixed-length character data.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a CHAR. |

   method [sqlalchemy.dialects.mysql.CHAR.](#sqlalchemy.dialects.mysql.CHAR)__init__(*length:int|None=None*, ***kwargs:Any*)

Construct a CHAR.

  Parameters:

- **length** – Maximum data length, in characters.
- **binary** – Optional, use the default binary collation for the
  national character set.  This does not affect the type of data
  stored, use a BINARY type for binary data.
- **collation** – Optional, request a particular collation.  Must be
  compatible with the national character set.

       class sqlalchemy.dialects.mysql.DATE

*inherits from* [sqlalchemy.types.Date](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Date)

The SQL DATE type.

    class sqlalchemy.dialects.mysql.DATETIME

*inherits from* [sqlalchemy.types.DATETIME](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DATETIME)

MySQL DATETIME type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a MySQL DATETIME type. |

   method [sqlalchemy.dialects.mysql.DATETIME.](#sqlalchemy.dialects.mysql.DATETIME)__init__(*timezone:bool=False*, *fsp:int|None=None*)

Construct a MySQL DATETIME type.

  Parameters:

- **timezone** – not used by the MySQL dialect.
- **fsp** –
  fractional seconds precision value.
  MySQL 5.6.4 supports storage of fractional seconds;
  this parameter will be used when emitting DDL
  for the DATETIME type.
  Note
  DBAPI driver support for fractional seconds may
  be limited; current support includes
  MySQL Connector/Python.

       class sqlalchemy.dialects.mysql.DECIMAL

*inherits from* `sqlalchemy.dialects.mysql.types._NumericType`, [sqlalchemy.types.DECIMAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DECIMAL)

MySQL DECIMAL type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a DECIMAL. |

   method [sqlalchemy.dialects.mysql.DECIMAL.](#sqlalchemy.dialects.mysql.DECIMAL)__init__(*precision:int|None=None*, *scale:int|None=None*, *asdecimal:bool=True*, ***kw:Any*)

Construct a DECIMAL.

  Parameters:

- **precision** – Total digits in this number.  If scale and precision
  are both None, values are stored to limits allowed by the server.
- **scale** – The number of digits after the decimal point.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.DOUBLE

*inherits from* `sqlalchemy.dialects.mysql.types._FloatType`, [sqlalchemy.types.DOUBLE](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE)

MySQL DOUBLE type.

   method [sqlalchemy.dialects.mysql.DOUBLE.](#sqlalchemy.dialects.mysql.DOUBLE)__init__(*precision:int|None=None*, *scale:int|None=None*, *asdecimal:bool=True*, ***kw:Any*)

Construct a DOUBLE.

Note

The [DOUBLE](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE) type by default converts from float
to Decimal, using a truncation that defaults to 10 digits.
Specify either `scale=n` or `decimal_return_scale=n` in order
to change this scale, or `asdecimal=False` to return values
directly as Python floating points.

   Parameters:

- **precision** – Total digits in this number.  If scale and precision
  are both None, values are stored to limits allowed by the server.
- **scale** – The number of digits after the decimal point.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.ENUM

*inherits from* `sqlalchemy.types.NativeForEmulated`, [sqlalchemy.types.Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum), `sqlalchemy.dialects.mysql.types._StringType`

MySQL ENUM type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct an ENUM. |

   method [sqlalchemy.dialects.mysql.ENUM.](#sqlalchemy.dialects.mysql.ENUM)__init__(**enums:str|Type[Enum]*, ***kw:Any*) → None

Construct an ENUM.

E.g.:

```
Column("myenum", ENUM("foo", "bar", "baz"))
```

   Parameters:

- **enums** –
  The range of valid values for this ENUM.  Values in
  enums are not quoted, they will be escaped and surrounded by single
  quotes when generating the schema.  This object may also be a
  PEP-435-compliant enumerated type.
- **strict** –
  This flag has no effect.
  Changed in version The: MySQL ENUM type as well as the base Enum
  type now validates all Python data values.
- **charset** – Optional, a column-level character set for this string
  value.  Takes precedence to ‘ascii’ or ‘unicode’ short-hand.
- **collation** – Optional, a column-level collation for this string
  value.  Takes precedence to ‘binary’ short-hand.
- **ascii** – Defaults to False: short-hand for the `latin1`
  character set, generates ASCII in schema.
- **unicode** – Defaults to False: short-hand for the `ucs2`
  character set, generates UNICODE in schema.
- **binary** – Defaults to False: short-hand, pick the binary
  collation type that matches the column’s character set.  Generates
  BINARY in schema.  This does not affect the type of data stored,
  only the collation of character data.

       class sqlalchemy.dialects.mysql.FLOAT

*inherits from* `sqlalchemy.dialects.mysql.types._FloatType`, [sqlalchemy.types.FLOAT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.FLOAT)

MySQL FLOAT type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a FLOAT. |

   method [sqlalchemy.dialects.mysql.FLOAT.](#sqlalchemy.dialects.mysql.FLOAT)__init__(*precision:int|None=None*, *scale:int|None=None*, *asdecimal:bool=False*, ***kw:Any*)

Construct a FLOAT.

  Parameters:

- **precision** – Total digits in this number.  If scale and precision
  are both None, values are stored to limits allowed by the server.
- **scale** – The number of digits after the decimal point.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.INET4

*inherits from* [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

INET4 column type for MariaDB

Added in version 2.0.37.

     class sqlalchemy.dialects.mysql.INET6

*inherits from* [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

INET6 column type for MariaDB

Added in version 2.0.37.

     class sqlalchemy.dialects.mysql.INTEGER

*inherits from* `sqlalchemy.dialects.mysql.types._IntegerType`, [sqlalchemy.types.INTEGER](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.INTEGER)

MySQL INTEGER type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct an INTEGER. |

   method [sqlalchemy.dialects.mysql.INTEGER.](#sqlalchemy.dialects.mysql.INTEGER)__init__(*display_width:int|None=None*, ***kw:Any*)

Construct an INTEGER.

  Parameters:

- **display_width** – Optional, maximum display width for this number.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.JSON

*inherits from* [sqlalchemy.types.JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)

MySQL JSON type.

MySQL supports JSON as of version 5.7.
MariaDB supports JSON (as an alias for LONGTEXT) as of version 10.2.

[JSON](#sqlalchemy.dialects.mysql.JSON) is used automatically whenever the base
[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) datatype is used against a MySQL or MariaDB backend.

See also

[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) - main documentation for the generic
cross-platform JSON datatype.

The [JSON](#sqlalchemy.dialects.mysql.JSON) type supports persistence of JSON values
as well as the core index operations provided by [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)
datatype, by adapting the operations to render the `JSON_EXTRACT`
function at the database level.

    class sqlalchemy.dialects.mysql.LONGBLOB

*inherits from* `sqlalchemy.types._Binary`

MySQL LONGBLOB type, for binary data up to 2^32 bytes.

    class sqlalchemy.dialects.mysql.LONGTEXT

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`

MySQL LONGTEXT type, for character storage encoded up to 2^32 bytes.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a LONGTEXT. |

   method [sqlalchemy.dialects.mysql.LONGTEXT.](#sqlalchemy.dialects.mysql.LONGTEXT)__init__(***kwargs:Any*)

Construct a LONGTEXT.

  Parameters:

- **charset** – Optional, a column-level character set for this string
  value.  Takes precedence to ‘ascii’ or ‘unicode’ short-hand.
- **collation** – Optional, a column-level collation for this string
  value.  Takes precedence to ‘binary’ short-hand.
- **ascii** – Defaults to False: short-hand for the `latin1`
  character set, generates ASCII in schema.
- **unicode** – Defaults to False: short-hand for the `ucs2`
  character set, generates UNICODE in schema.
- **national** – Optional. If true, use the server’s configured
  national character set.
- **binary** – Defaults to False: short-hand, pick the binary
  collation type that matches the column’s character set.  Generates
  BINARY in schema.  This does not affect the type of data stored,
  only the collation of character data.

       class sqlalchemy.dialects.mysql.MEDIUMBLOB

*inherits from* `sqlalchemy.types._Binary`

MySQL MEDIUMBLOB type, for binary data up to 2^24 bytes.

    class sqlalchemy.dialects.mysql.MEDIUMINT

*inherits from* `sqlalchemy.dialects.mysql.types._IntegerType`

MySQL MEDIUMINTEGER type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a MEDIUMINTEGER |

   method [sqlalchemy.dialects.mysql.MEDIUMINT.](#sqlalchemy.dialects.mysql.MEDIUMINT)__init__(*display_width:int|None=None*, ***kw:Any*)

Construct a MEDIUMINTEGER

  Parameters:

- **display_width** – Optional, maximum display width for this number.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.MEDIUMTEXT

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`

MySQL MEDIUMTEXT type, for character storage encoded up
to 2^24 bytes.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a MEDIUMTEXT. |

   method [sqlalchemy.dialects.mysql.MEDIUMTEXT.](#sqlalchemy.dialects.mysql.MEDIUMTEXT)__init__(***kwargs:Any*)

Construct a MEDIUMTEXT.

  Parameters:

- **charset** – Optional, a column-level character set for this string
  value.  Takes precedence to ‘ascii’ or ‘unicode’ short-hand.
- **collation** – Optional, a column-level collation for this string
  value.  Takes precedence to ‘binary’ short-hand.
- **ascii** – Defaults to False: short-hand for the `latin1`
  character set, generates ASCII in schema.
- **unicode** – Defaults to False: short-hand for the `ucs2`
  character set, generates UNICODE in schema.
- **national** – Optional. If true, use the server’s configured
  national character set.
- **binary** – Defaults to False: short-hand, pick the binary
  collation type that matches the column’s character set.  Generates
  BINARY in schema.  This does not affect the type of data stored,
  only the collation of character data.

       class sqlalchemy.dialects.mysql.NCHAR

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`, [sqlalchemy.types.NCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NCHAR)

MySQL NCHAR type.

For fixed-length character data in the server’s configured national
character set.

| Member Name | Description |
| --- | --- |
| __init__() | Construct an NCHAR. |

   method [sqlalchemy.dialects.mysql.NCHAR.](#sqlalchemy.dialects.mysql.NCHAR)__init__(*length:int|None=None*, ***kwargs:Any*)

Construct an NCHAR.

  Parameters:

- **length** – Maximum data length, in characters.
- **binary** – Optional, use the default binary collation for the
  national character set.  This does not affect the type of data
  stored, use a BINARY type for binary data.
- **collation** – Optional, request a particular collation.  Must be
  compatible with the national character set.

       class sqlalchemy.dialects.mysql.NUMERIC

*inherits from* `sqlalchemy.dialects.mysql.types._NumericType`, [sqlalchemy.types.NUMERIC](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NUMERIC)

MySQL NUMERIC type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a NUMERIC. |

   method [sqlalchemy.dialects.mysql.NUMERIC.](#sqlalchemy.dialects.mysql.NUMERIC)__init__(*precision:int|None=None*, *scale:int|None=None*, *asdecimal:bool=True*, ***kw:Any*)

Construct a NUMERIC.

  Parameters:

- **precision** – Total digits in this number.  If scale and precision
  are both None, values are stored to limits allowed by the server.
- **scale** – The number of digits after the decimal point.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.NVARCHAR

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`, [sqlalchemy.types.NVARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NVARCHAR)

MySQL NVARCHAR type.

For variable-length character data in the server’s configured national
character set.

| Member Name | Description |
| --- | --- |
| __init__() | Construct an NVARCHAR. |

   method [sqlalchemy.dialects.mysql.NVARCHAR.](#sqlalchemy.dialects.mysql.NVARCHAR)__init__(*length:int|None=None*, ***kwargs:Any*)

Construct an NVARCHAR.

  Parameters:

- **length** – Maximum data length, in characters.
- **binary** – Optional, use the default binary collation for the
  national character set.  This does not affect the type of data
  stored, use a BINARY type for binary data.
- **collation** – Optional, request a particular collation.  Must be
  compatible with the national character set.

       class sqlalchemy.dialects.mysql.REAL

*inherits from* `sqlalchemy.dialects.mysql.types._FloatType`, [sqlalchemy.types.REAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.REAL)

MySQL REAL type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a REAL. |

   method [sqlalchemy.dialects.mysql.REAL.](#sqlalchemy.dialects.mysql.REAL)__init__(*precision:int|None=None*, *scale:int|None=None*, *asdecimal:bool=True*, ***kw:Any*)

Construct a REAL.

Note

The [REAL](#sqlalchemy.dialects.mysql.REAL) type by default converts from float
to Decimal, using a truncation that defaults to 10 digits.
Specify either `scale=n` or `decimal_return_scale=n` in order
to change this scale, or `asdecimal=False` to return values
directly as Python floating points.

   Parameters:

- **precision** – Total digits in this number.  If scale and precision
  are both None, values are stored to limits allowed by the server.
- **scale** – The number of digits after the decimal point.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.SET

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`

MySQL SET type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a SET. |

   method [sqlalchemy.dialects.mysql.SET.](#sqlalchemy.dialects.mysql.SET)__init__(**values:str*, ***kw:Any*)

Construct a SET.

E.g.:

```
Column("myset", SET("foo", "bar", "baz"))
```

The list of potential values is required in the case that this
set will be used to generate DDL for a table, or if the
[SET.retrieve_as_bitwise](#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise) flag is set to True.

  Parameters:

- **values** – The range of valid values for this SET. The values
  are not quoted, they will be escaped and surrounded by single
  quotes when generating the schema.
- **convert_unicode** – Same flag as that of
  [String.convert_unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String.params.convert_unicode).
- **collation** – same as that of [String.collation](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String.params.collation)
- **charset** – same as that of [VARCHAR.charset](#sqlalchemy.dialects.mysql.VARCHAR.params.charset).
- **ascii** – same as that of [VARCHAR.ascii](#sqlalchemy.dialects.mysql.VARCHAR.params.ascii).
- **unicode** – same as that of [VARCHAR.unicode](#sqlalchemy.dialects.mysql.VARCHAR.params.unicode).
- **binary** – same as that of [VARCHAR.binary](#sqlalchemy.dialects.mysql.VARCHAR.params.binary).
- **retrieve_as_bitwise** –
  if True, the data for the set type will be
  persisted and selected using an integer value, where a set is coerced
  into a bitwise mask for persistence.  MySQL allows this mode which
  has the advantage of being able to store values unambiguously,
  such as the blank string `''`.   The datatype will appear
  as the expression `col + 0` in a SELECT statement, so that the
  value is coerced into an integer value in result sets.
  This flag is required if one wishes
  to persist a set that can store the blank string `''` as a value.
  Warning
  When using [SET.retrieve_as_bitwise](#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise), it is
  essential that the list of set values is expressed in the
  **exact same order** as exists on the MySQL database.

       class sqlalchemy.dialects.mysql.SMALLINT

*inherits from* `sqlalchemy.dialects.mysql.types._IntegerType`, [sqlalchemy.types.SMALLINT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SMALLINT)

MySQL SMALLINTEGER type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a SMALLINTEGER. |

   method [sqlalchemy.dialects.mysql.SMALLINT.](#sqlalchemy.dialects.mysql.SMALLINT)__init__(*display_width:int|None=None*, ***kw:Any*)

Construct a SMALLINTEGER.

  Parameters:

- **display_width** – Optional, maximum display width for this number.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.TEXT

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`, [sqlalchemy.types.TEXT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TEXT)

MySQL TEXT type, for character storage encoded up to 2^16 bytes.

   method [sqlalchemy.dialects.mysql.TEXT.](#sqlalchemy.dialects.mysql.TEXT)__init__(*length:int|None=None*, ***kw:Any*)

Construct a TEXT.

  Parameters:

- **length** – Optional, if provided the server may optimize storage
  by substituting the smallest TEXT type sufficient to store
  `length` bytes of characters.
- **charset** – Optional, a column-level character set for this string
  value.  Takes precedence to ‘ascii’ or ‘unicode’ short-hand.
- **collation** – Optional, a column-level collation for this string
  value.  Takes precedence to ‘binary’ short-hand.
- **ascii** – Defaults to False: short-hand for the `latin1`
  character set, generates ASCII in schema.
- **unicode** – Defaults to False: short-hand for the `ucs2`
  character set, generates UNICODE in schema.
- **national** – Optional. If true, use the server’s configured
  national character set.
- **binary** – Defaults to False: short-hand, pick the binary
  collation type that matches the column’s character set.  Generates
  BINARY in schema.  This does not affect the type of data stored,
  only the collation of character data.

       class sqlalchemy.dialects.mysql.TIME

*inherits from* [sqlalchemy.types.TIME](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIME)

MySQL TIME type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a MySQL TIME type. |

   method [sqlalchemy.dialects.mysql.TIME.](#sqlalchemy.dialects.mysql.TIME)__init__(*timezone:bool=False*, *fsp:int|None=None*)

Construct a MySQL TIME type.

  Parameters:

- **timezone** – not used by the MySQL dialect.
- **fsp** –
  fractional seconds precision value.
  MySQL 5.6 supports storage of fractional seconds;
  this parameter will be used when emitting DDL
  for the TIME type.
  Note
  DBAPI driver support for fractional seconds may
  be limited; current support includes
  MySQL Connector/Python.

       class sqlalchemy.dialects.mysql.TIMESTAMP

*inherits from* [sqlalchemy.types.TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP)

MySQL TIMESTAMP type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a MySQL TIMESTAMP type. |

   method [sqlalchemy.dialects.mysql.TIMESTAMP.](#sqlalchemy.dialects.mysql.TIMESTAMP)__init__(*timezone:bool=False*, *fsp:int|None=None*)

Construct a MySQL TIMESTAMP type.

  Parameters:

- **timezone** – not used by the MySQL dialect.
- **fsp** –
  fractional seconds precision value.
  MySQL 5.6.4 supports storage of fractional seconds;
  this parameter will be used when emitting DDL
  for the TIMESTAMP type.
  Note
  DBAPI driver support for fractional seconds may
  be limited; current support includes
  MySQL Connector/Python.

       class sqlalchemy.dialects.mysql.TINYBLOB

*inherits from* `sqlalchemy.types._Binary`

MySQL TINYBLOB type, for binary data up to 2^8 bytes.

    class sqlalchemy.dialects.mysql.TINYINT

*inherits from* `sqlalchemy.dialects.mysql.types._IntegerType`

MySQL TINYINT type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a TINYINT. |

   method [sqlalchemy.dialects.mysql.TINYINT.](#sqlalchemy.dialects.mysql.TINYINT)__init__(*display_width:int|None=None*, ***kw:Any*)

Construct a TINYINT.

  Parameters:

- **display_width** – Optional, maximum display width for this number.
- **unsigned** – a boolean, optional.
- **zerofill** – Optional. If true, values will be stored as strings
  left-padded with zeros. Note that this does not effect the values
  returned by the underlying database API, which continue to be
  numeric.

       class sqlalchemy.dialects.mysql.TINYTEXT

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`

MySQL TINYTEXT type, for character storage encoded up to 2^8 bytes.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a TINYTEXT. |

   method [sqlalchemy.dialects.mysql.TINYTEXT.](#sqlalchemy.dialects.mysql.TINYTEXT)__init__(***kwargs:Any*)

Construct a TINYTEXT.

  Parameters:

- **charset** – Optional, a column-level character set for this string
  value.  Takes precedence to ‘ascii’ or ‘unicode’ short-hand.
- **collation** – Optional, a column-level collation for this string
  value.  Takes precedence to ‘binary’ short-hand.
- **ascii** – Defaults to False: short-hand for the `latin1`
  character set, generates ASCII in schema.
- **unicode** – Defaults to False: short-hand for the `ucs2`
  character set, generates UNICODE in schema.
- **national** – Optional. If true, use the server’s configured
  national character set.
- **binary** – Defaults to False: short-hand, pick the binary
  collation type that matches the column’s character set.  Generates
  BINARY in schema.  This does not affect the type of data stored,
  only the collation of character data.

       class sqlalchemy.dialects.mysql.VARBINARY

*inherits from* `sqlalchemy.types._Binary`

The SQL VARBINARY type.

    class sqlalchemy.dialects.mysql.VARCHAR

*inherits from* `sqlalchemy.dialects.mysql.types._StringType`, [sqlalchemy.types.VARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARCHAR)

MySQL VARCHAR type, for variable-length character data.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a VARCHAR. |

   method [sqlalchemy.dialects.mysql.VARCHAR.](#sqlalchemy.dialects.mysql.VARCHAR)__init__(*length:int|None=None*, ***kwargs:Any*) → None

Construct a VARCHAR.

  Parameters:

- **charset** – Optional, a column-level character set for this string
  value.  Takes precedence to ‘ascii’ or ‘unicode’ short-hand.
- **collation** – Optional, a column-level collation for this string
  value.  Takes precedence to ‘binary’ short-hand.
- **ascii** – Defaults to False: short-hand for the `latin1`
  character set, generates ASCII in schema.
- **unicode** – Defaults to False: short-hand for the `ucs2`
  character set, generates UNICODE in schema.
- **national** – Optional. If true, use the server’s configured
  national character set.
- **binary** – Defaults to False: short-hand, pick the binary
  collation type that matches the column’s character set.  Generates
  BINARY in schema.  This does not affect the type of data stored,
  only the collation of character data.

       class sqlalchemy.dialects.mysql.YEAR

*inherits from* [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

MySQL YEAR type, for single byte storage of years 1901-2155.

## MySQL DML Constructs

| Object Name | Description |
| --- | --- |
| insert(table) | Construct a MySQL/MariaDB-specific variantInsertconstruct. |
| Insert | MySQL-specific implementation of INSERT. |

   function sqlalchemy.dialects.mysql.insert(*table:_DMLTableArgument*) → [Insert](#sqlalchemy.dialects.mysql.Insert)

Construct a MySQL/MariaDB-specific variant [Insert](#sqlalchemy.dialects.mysql.Insert)
construct.

The [sqlalchemy.dialects.mysql.insert()](#sqlalchemy.dialects.mysql.insert) function creates
a [sqlalchemy.dialects.mysql.Insert](#sqlalchemy.dialects.mysql.Insert).  This class is based
on the dialect-agnostic [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct which may
be constructed using the [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) function in
SQLAlchemy Core.

The [Insert](#sqlalchemy.dialects.mysql.Insert) construct includes additional methods
[Insert.on_duplicate_key_update()](#sqlalchemy.dialects.mysql.Insert.on_duplicate_key_update).

    class sqlalchemy.dialects.mysql.Insert

*inherits from* [sqlalchemy.sql.expression.Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)

MySQL-specific implementation of INSERT.

Adds methods for MySQL-specific syntaxes such as ON DUPLICATE KEY UPDATE.

The [Insert](#sqlalchemy.dialects.mysql.Insert) object is created using the
[sqlalchemy.dialects.mysql.insert()](#sqlalchemy.dialects.mysql.insert) function.

Added in version 1.2.

| Member Name | Description |
| --- | --- |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| on_duplicate_key_update() | Specifies the ON DUPLICATE KEY UPDATE clause. |

   attribute [sqlalchemy.dialects.mysql.Insert.](#sqlalchemy.dialects.mysql.Insert)inherit_cache = False

Indicate if this [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) instance should make use of the
cache key generation scheme used by its immediate superclass.

The attribute defaults to `None`, which indicates that a construct has
not yet taken into account whether or not its appropriate for it to
participate in caching; this is functionally equivalent to setting the
value to `False`, except that a warning is also emitted.

This flag can be set to `True` on a particular class, if the SQL that
corresponds to the object does not change based on attributes which
are local to this class, and not its superclass.

See also

[Enabling Caching Support for Custom Constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#compilerext-caching) - General guideslines for setting the
[HasCacheKey.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache) attribute for third-party or user
defined SQL constructs.

     property inserted: ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]

Provide the “inserted” namespace for an ON DUPLICATE KEY UPDATE
statement

MySQL’s ON DUPLICATE KEY UPDATE clause allows reference to the row
that would be inserted, via a special function called `VALUES()`.
This attribute provides all columns in this row to be referenceable
such that they will render within a `VALUES()` function inside the
ON DUPLICATE KEY UPDATE clause.    The attribute is named `.inserted`
so as not to conflict with the existing
[Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method.

Tip

The [Insert.inserted](#sqlalchemy.dialects.mysql.Insert.inserted) attribute is an instance
of [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection), which provides an
interface the same as that of the [Table.c](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.c)
collection described at [Accessing Tables and Columns](https://docs.sqlalchemy.org/en/20/core/metadata.html#metadata-tables-and-columns).
With this collection, ordinary names are accessible like attributes
(e.g. `stmt.inserted.some_column`), but special names and
dictionary method names should be accessed using indexed access,
such as `stmt.inserted["column name"]` or
`stmt.inserted["values"]`.  See the docstring for
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) for further examples.

See also

[INSERT…ON DUPLICATE KEY UPDATE (Upsert)](#mysql-insert-on-duplicate-key-update) - example of how
to use `Insert.inserted`

     method [sqlalchemy.dialects.mysql.Insert.](#sqlalchemy.dialects.mysql.Insert)on_duplicate_key_update(**args:Mapping[Any,Any]|List[Tuple[str,Any]]|ColumnCollection[Any,Any]*, ***kw:Any*) → Self

Specifies the ON DUPLICATE KEY UPDATE clause.

  Parameters:

****kw** – Column keys linked to UPDATE values.  The
values may be any SQL expression or supported literal Python
values.

Warning

This dictionary does **not** take into account
Python-specified default UPDATE values or generation functions,
e.g. those specified using [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate).
These values will not be exercised for an ON DUPLICATE KEY UPDATE
style of UPDATE, unless values are manually specified here.

   Parameters:

***args** –

As an alternative to passing key/value parameters,
a dictionary or list of 2-tuples can be passed as a single positional
argument.

Passing a single dictionary is equivalent to the keyword argument
form:

```
insert().on_duplicate_key_update({"name": "some name"})
```

Passing a list of 2-tuples indicates that the parameter assignments
in the UPDATE clause should be ordered as sent, in a manner similar
to that described for the [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)
construct overall
in [Parameter Ordered Updates](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-parameter-ordered-updates):

```
insert().on_duplicate_key_update(
    [
        ("name", "some name"),
        ("value", "some value"),
    ]
)
```

Changed in version 1.3: parameters can be specified as a dictionary
or list of 2-tuples; the latter form provides for parameter
ordering.

Added in version 1.2.

See also

[INSERT…ON DUPLICATE KEY UPDATE (Upsert)](#mysql-insert-on-duplicate-key-update)

## mysqlclient (fork of MySQL-Python)

Support for the MySQL / MariaDB database via the mysqlclient (maintained fork of MySQL-Python) driver.

### DBAPI

Documentation and download information (if applicable) for mysqlclient (maintained fork of MySQL-Python) is available at:
[https://pypi.org/project/mysqlclient/](https://pypi.org/project/mysqlclient/)

### Connecting

Connect String:

```
mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
```

### Driver Status

The mysqlclient DBAPI is a maintained fork of the
[MySQL-Python](https://sourceforge.net/projects/mysql-python) DBAPI
that is no longer maintained.  [mysqlclient](https://github.com/PyMySQL/mysqlclient-python) supports Python 2 and Python 3
and is very stable.

### Unicode

Please see [Unicode](#mysql-unicode) for current recommendations on unicode
handling.

### SSL Connections

The mysqlclient and PyMySQL DBAPIs accept an additional dictionary under the
key “ssl”, which may be specified using the
[create_engine.connect_args](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.connect_args) dictionary:

```
engine = create_engine(
    "mysql+mysqldb://scott:[email protected]/test",
    connect_args={
        "ssl": {
            "ca": "/home/gord/client-ssl/ca.pem",
            "cert": "/home/gord/client-ssl/client-cert.pem",
            "key": "/home/gord/client-ssl/client-key.pem",
        }
    },
)
```

For convenience, the following keys may also be specified inline within the URL
where they will be interpreted into the “ssl” dictionary automatically:
“ssl_ca”, “ssl_cert”, “ssl_key”, “ssl_capath”, “ssl_cipher”,
“ssl_check_hostname”. An example is as follows:

```
connection_uri = (
    "mysql+mysqldb://scott:[email protected]/test"
    "?ssl_ca=/home/gord/client-ssl/ca.pem"
    "&ssl_cert=/home/gord/client-ssl/client-cert.pem"
    "&ssl_key=/home/gord/client-ssl/client-key.pem"
)
```

See also

[SSL Connections](#pymysql-ssl) in the PyMySQL dialect

### Using MySQLdb with Google Cloud SQL

Google Cloud SQL now recommends use of the MySQLdb dialect.  Connect
using a URL like the following:

```
mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>
```

### Server Side Cursors

The mysqldb dialect supports server-side cursors. See [Server Side Cursors](#mysql-ss-cursors).

## PyMySQL

Support for the MySQL / MariaDB database via the PyMySQL driver.

### DBAPI

Documentation and download information (if applicable) for PyMySQL is available at:
[https://pymysql.readthedocs.io/](https://pymysql.readthedocs.io/)

### Connecting

Connect String:

```
mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
```

### Unicode

Please see [Unicode](#mysql-unicode) for current recommendations on unicode
handling.

### SSL Connections

The PyMySQL DBAPI accepts the same SSL arguments as that of MySQLdb,
described at [SSL Connections](#mysqldb-ssl).   See that section for additional examples.

If the server uses an automatically-generated certificate that is self-signed
or does not match the host name (as seen from the client), it may also be
necessary to indicate `ssl_check_hostname=false` in PyMySQL:

```
connection_uri = (
    "mysql+pymysql://scott:[email protected]/test"
    "?ssl_ca=/home/gord/client-ssl/ca.pem"
    "&ssl_cert=/home/gord/client-ssl/client-cert.pem"
    "&ssl_key=/home/gord/client-ssl/client-key.pem"
    "&ssl_check_hostname=false"
)
```

### MySQL-Python Compatibility

The pymysql DBAPI is a pure Python port of the MySQL-python (MySQLdb) driver,
and targets 100% compatibility.   Most behavioral notes for MySQL-python apply
to the pymysql driver as well.

## MariaDB-Connector

Support for the MySQL / MariaDB database via the MariaDB Connector/Python driver.

### DBAPI

Documentation and download information (if applicable) for MariaDB Connector/Python is available at:
[https://pypi.org/project/mariadb/](https://pypi.org/project/mariadb/)

### Connecting

Connect String:

```
mariadb+mariadbconnector://<user>:<password>@<host>[:<port>]/<dbname>
```

### Driver Status

MariaDB Connector/Python enables Python programs to access MariaDB and MySQL
databases using an API which is compliant with the Python DB API 2.0 (PEP-249).
It is written in C and uses MariaDB Connector/C client library for client server
communication.

Note that the default driver for a `mariadb://` connection URI continues to
be `mysqldb`. `mariadb+mariadbconnector://` is required to use this driver.

## MySQL-Connector

Support for the MySQL / MariaDB database via the MySQL Connector/Python driver.

### DBAPI

Documentation and download information (if applicable) for MySQL Connector/Python is available at:
[https://pypi.org/project/mysql-connector-python/](https://pypi.org/project/mysql-connector-python/)

### Connecting

Connect String:

```
mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
```

### Driver Status

MySQL Connector/Python is supported as of SQLAlchemy 2.0.39 to the
degree which the driver is functional.   There are still ongoing issues
with features such as server side cursors which remain disabled until
upstream issues are repaired.

Warning

The MySQL Connector/Python driver published by Oracle is subject
to frequent, major regressions of essential functionality such as being able
to correctly persist simple binary strings which indicate it is not well
tested.  The SQLAlchemy project is not able to maintain this dialect fully as
regressions in the driver prevent it from being included in continuous
integration.

Changed in version 2.0.39: The MySQL Connector/Python dialect has been updated to support the
latest version of this DBAPI.   Previously, MySQL Connector/Python
was not fully supported.  However, support remains limited due to ongoing
regressions introduced in this driver.

### Connecting to MariaDB with MySQL Connector/Python

MySQL Connector/Python may attempt to pass an incompatible collation to the
database when connecting to MariaDB.  Experimentation has shown that using
`?charset=utf8mb4&collation=utfmb4_general_ci` or similar MariaDB-compatible
charset/collation will allow connectivity.

## asyncmy

Support for the MySQL / MariaDB database via the asyncmy driver.

### DBAPI

Documentation and download information (if applicable) for asyncmy is available at:
[https://github.com/long2ice/asyncmy](https://github.com/long2ice/asyncmy)

### Connecting

Connect String:

```
mysql+asyncmy://user:password@host:port/dbname[?key=value&key=value...]
```

Using a special asyncio mediation layer, the asyncmy dialect is usable
as the backend for the [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
extension package.

This dialect should normally be used only with the
[create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) engine creation function:

```
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "mysql+asyncmy://user:pass@hostname/dbname?charset=utf8mb4"
)
```

## aiomysql

Support for the MySQL / MariaDB database via the aiomysql driver.

### DBAPI

Documentation and download information (if applicable) for aiomysql is available at:
[https://github.com/aio-libs/aiomysql](https://github.com/aio-libs/aiomysql)

### Connecting

Connect String:

```
mysql+aiomysql://user:password@host:port/dbname[?key=value&key=value...]
```

The aiomysql dialect is SQLAlchemy’s second Python asyncio dialect.

Using a special asyncio mediation layer, the aiomysql dialect is usable
as the backend for the [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
extension package.

This dialect should normally be used only with the
[create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) engine creation function:

```
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "mysql+aiomysql://user:pass@hostname/dbname?charset=utf8mb4"
)
```

## cymysql

Support for the MySQL / MariaDB database via the CyMySQL driver.

### DBAPI

Documentation and download information (if applicable) for CyMySQL is available at:
[https://github.com/nakagami/CyMySQL](https://github.com/nakagami/CyMySQL)

### Connecting

Connect String:

```
mysql+cymysql://<username>:<password>@<host>/<dbname>[?<options>]
```

Note

The CyMySQL dialect is **not tested as part of SQLAlchemy’s continuous
integration** and may have unresolved issues.  The recommended MySQL
dialects are mysqlclient and PyMySQL.

## pyodbc

Support for the MySQL / MariaDB database via the PyODBC driver.

### DBAPI

Documentation and download information (if applicable) for PyODBC is available at:
[https://pypi.org/project/pyodbc/](https://pypi.org/project/pyodbc/)

### Connecting

Connect String:

```
mysql+pyodbc://<username>:<password>@<dsnname>
```

Note

The PyODBC for MySQL dialect is **not tested as part of
SQLAlchemy’s continuous integration**.
The recommended MySQL dialects are mysqlclient and PyMySQL.
However, if you want to use the mysql+pyodbc dialect and require
full support for `utf8mb4` characters (including supplementary
characters like emoji) be sure to use a current release of
MySQL Connector/ODBC and specify the “ANSI” (**not** “Unicode”)
version of the driver in your DSN or connection string.

Pass through exact pyodbc connection string:

```
import urllib

connection_string = (
    "DRIVER=MySQL ODBC 8.0 ANSI Driver;"
    "SERVER=localhost;"
    "PORT=3307;"
    "DATABASE=mydb;"
    "UID=root;"
    "PWD=(whatever);"
    "charset=utf8mb4;"
)
params = urllib.parse.quote_plus(connection_string)
connection_uri = "mysql+pyodbc:///?odbc_connect=%s" % params
```
