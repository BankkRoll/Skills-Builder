# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# SQLite

Support for the SQLite database.

The following table summarizes current support levels for database release versions.

| Support type | Versions |
| --- | --- |
| Supported version | 3.12+ |
| Best effort | 3.7.16+ |

## DBAPI Support

The following dialect/DBAPI options are available.  Please refer to individual DBAPI sections for connect information.

- [pysqlite](#module-sqlalchemy.dialects.sqlite.pysqlite)
- [aiosqlite](#module-sqlalchemy.dialects.sqlite.aiosqlite)
- [pysqlcipher](#module-sqlalchemy.dialects.sqlite.pysqlcipher)

## Date and Time Types

SQLite does not have built-in DATE, TIME, or DATETIME types, and pysqlite does
not provide out of the box functionality for translating values between Python
datetime objects and a SQLite-supported format. SQLAlchemy’s own
[DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime) and related types provide date formatting
and parsing functionality when SQLite is used. The implementation classes are
[DATETIME](#sqlalchemy.dialects.sqlite.DATETIME), [DATE](#sqlalchemy.dialects.sqlite.DATE) and [TIME](#sqlalchemy.dialects.sqlite.TIME).
These types represent dates and times as ISO formatted strings, which also
nicely support ordering. There’s no reliance on typical “libc” internals for
these functions so historical dates are fully supported.

### Ensuring Text affinity

The DDL rendered for these types is the standard `DATE`, `TIME`
and `DATETIME` indicators.    However, custom storage formats can also be
applied to these types.   When the
storage format is detected as containing no alpha characters, the DDL for
these types is rendered as `DATE_CHAR`, `TIME_CHAR`, and `DATETIME_CHAR`,
so that the column continues to have textual affinity.

See also

[Type Affinity](https://www.sqlite.org/datatype3.html#affinity) -
in the SQLite documentation

## SQLite Auto Incrementing Behavior

Background on SQLite’s autoincrement is at: [https://sqlite.org/autoinc.html](https://sqlite.org/autoinc.html)

Key concepts:

- SQLite has an implicit “auto increment” feature that takes place for any
  non-composite primary-key column that is specifically created using
  “INTEGER PRIMARY KEY” for the type + primary key.
- SQLite also has an explicit “AUTOINCREMENT” keyword, that is **not**
  equivalent to the implicit autoincrement feature; this keyword is not
  recommended for general use.  SQLAlchemy does not render this keyword
  unless a special SQLite-specific directive is used (see below).  However,
  it still requires that the column’s type is named “INTEGER”.

### Using the AUTOINCREMENT Keyword

To specifically render the AUTOINCREMENT keyword on the primary key column
when rendering DDL, add the flag `sqlite_autoincrement=True` to the Table
construct:

```
Table(
    "sometable",
    metadata,
    Column("id", Integer, primary_key=True),
    sqlite_autoincrement=True,
)
```

### Allowing autoincrement behavior SQLAlchemy types other than Integer/INTEGER

SQLite’s typing model is based on naming conventions.  Among other things, this
means that any type name which contains the substring `"INT"` will be
determined to be of “integer affinity”.  A type named `"BIGINT"`,
`"SPECIAL_INT"` or even `"XYZINTQPR"`, will be considered by SQLite to be
of “integer” affinity.  However, **the SQLite autoincrement feature, whether
implicitly or explicitly enabled, requires that the name of the column’s type
is exactly the string “INTEGER”**.  Therefore, if an application uses a type
like [BigInteger](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BigInteger) for a primary key, on SQLite this type will need to
be rendered as the name `"INTEGER"` when emitting the initial `CREATE
TABLE` statement in order for the autoincrement behavior to be available.

One approach to achieve this is to use [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) on SQLite
only using [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant):

```
table = Table(
    "my_table",
    metadata,
    Column(
        "id",
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
    ),
)
```

Another is to use a subclass of [BigInteger](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BigInteger) that overrides its DDL
name to be `INTEGER` when compiled against SQLite:

```
from sqlalchemy import BigInteger
from sqlalchemy.ext.compiler import compiles

class SLBigInteger(BigInteger):
    pass

@compiles(SLBigInteger, "sqlite")
def bi_c(element, compiler, **kw):
    return "INTEGER"

@compiles(SLBigInteger)
def bi_c(element, compiler, **kw):
    return compiler.visit_BIGINT(element, **kw)

table = Table(
    "my_table", metadata, Column("id", SLBigInteger(), primary_key=True)
)
```

See also

[TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant)

[Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html)

[Datatypes In SQLite Version 3](https://sqlite.org/datatype3.html)

## Transactions with SQLite and the sqlite3 driver

As a file-based database, SQLite’s approach to transactions differs from
traditional databases in many ways.  Additionally, the `sqlite3` driver
standard with Python (as well as the async version `aiosqlite` which builds
on top of it) has several quirks, workarounds, and API features in the
area of transaction control, all of which generally need to be addressed when
constructing a SQLAlchemy application that uses SQLite.

### Legacy Transaction Mode with the sqlite3 driver

The most important aspect of transaction handling with the sqlite3 driver is
that it defaults (which will continue through Python 3.15 before being
removed in Python 3.16) to legacy transactional behavior which does
not strictly follow [PEP 249](https://peps.python.org/pep-0249/).  The way in which the driver diverges from the
PEP is that it does not “begin” a transaction automatically as dictated by
[PEP 249](https://peps.python.org/pep-0249/) except in the case of DML statements, e.g. INSERT, UPDATE, and
DELETE.   Normally, [PEP 249](https://peps.python.org/pep-0249/) dictates that a BEGIN must be emitted upon
the first SQL statement of any kind, so that all subsequent operations will
be established within a transaction until `connection.commit()` has been
called.   The `sqlite3` driver, in an effort to be easier to use in
highly concurrent environments, skips this step for DQL (e.g. SELECT) statements,
and also skips it for DDL (e.g. CREATE TABLE etc.) statements for more legacy
reasons.  Statements such as SAVEPOINT are also skipped.

In modern versions of the `sqlite3` driver as of Python 3.12, this legacy
mode of operation is referred to as
[“legacy transaction control”](https://docs.python.org/3/library/sqlite3.html#sqlite3-transaction-control-isolation-level), and is in
effect by default due to the `Connection.autocommit` parameter being set to
the constant `sqlite3.LEGACY_TRANSACTION_CONTROL`.  Prior to Python 3.12,
the `Connection.autocommit` attribute did not exist.

The implications of legacy transaction mode include:

- **Incorrect support for transactional DDL** - statements like CREATE TABLE, ALTER TABLE,
  CREATE INDEX etc. will not automatically BEGIN a transaction if one were not
  started already, leading to the changes by each statement being
  “autocommitted” immediately unless BEGIN were otherwise emitted first.   Very
  old (pre Python 3.6) versions of SQLite would also force a COMMIT for these
  operations even if a transaction were present, however this is no longer the
  case.
- **SERIALIZABLE behavior not fully functional** - SQLite’s transaction isolation
  behavior is normally consistent with SERIALIZABLE isolation, as it is a file-
  based system that locks the database file entirely for write operations,
  preventing COMMIT until all reader transactions (and associated file locks)
  have completed.  However, sqlite3’s legacy transaction mode fails to emit BEGIN for SELECT
  statements, which causes these SELECT statements to no longer be “repeatable”,
  failing one of the consistency guarantees of SERIALIZABLE.
- **Incorrect behavior for SAVEPOINT** - as the SAVEPOINT statement does not
  imply a BEGIN, a new SAVEPOINT emitted before a BEGIN will function on its
  own but fails to participate in the enclosing transaction, meaning a ROLLBACK
  of the transaction will not rollback elements that were part of a released
  savepoint.

Legacy transaction mode first existed in order to facilitate working around
SQLite’s file locks.  Because SQLite relies upon whole-file locks, it is easy to
get “database is locked” errors, particularly when newer features like “write
ahead logging” are disabled.   This is a key reason why `sqlite3`’s legacy
transaction mode is still the default mode of operation; disabling it will
produce behavior that is more susceptible to locked database errors.  However
note that **legacy transaction mode will no longer be the default** in a future
Python version (3.16 as of this writing).

### Enabling Non-Legacy SQLite Transactional Modes with the sqlite3 or aiosqlite driver

Current SQLAlchemy support allows either for setting the
`.Connection.autocommit` attribute, most directly by using a
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) parameter, or if on an older version of Python where
the attribute is not available, using event hooks to control the behavior of
BEGIN.

- **Enabling modern sqlite3 transaction control via the autocommit connect parameter** (Python 3.12 and above)
  To use SQLite in the mode described at [Transaction control via the autocommit attribute](https://docs.python.org/3/library/sqlite3.html#transaction-control-via-the-autocommit-attribute),
  the most straightforward approach is to set the attribute to its recommended value
  of `False` at the connect level using [create_engine.connect_args`](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.connect_args`):
  ```
  from sqlalchemy import create_engine
  engine = create_engine(
      "sqlite:///myfile.db", connect_args={"autocommit": False}
  )
  ```
  This parameter is also passed through when using the aiosqlite driver:
  ```
  from sqlalchemy.ext.asyncio import create_async_engine
  engine = create_async_engine(
      "sqlite+aiosqlite:///myfile.db", connect_args={"autocommit": False}
  )
  ```
  The parameter can also be set at the attribute level using the [PoolEvents.connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.connect)
  event hook, however this will only work for sqlite3, as aiosqlite does not yet expose this
  attribute on its `Connection` object:
  ```
  from sqlalchemy import create_engine, event
  engine = create_engine("sqlite:///myfile.db")
  @event.listens_for(engine, "connect")
  def do_connect(dbapi_connection, connection_record):
      # enable autocommit=False mode
      dbapi_connection.autocommit = False
  ```
- **Using SQLAlchemy to emit BEGIN in lieu of SQLite’s transaction control** (all Python versions, sqlite3 and aiosqlite)
  For older versions of `sqlite3` or for cross-compatiblity with older and
  newer versions, SQLAlchemy can also take over the job of transaction control.
  This is achieved by using the [ConnectionEvents.begin()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.begin) hook
  to emit the “BEGIN” command directly, while also disabling SQLite’s control
  of this command using the [PoolEvents.connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.connect) event hook to set the
  `Connection.isolation_level` attribute to `None`:
  ```
  from sqlalchemy import create_engine, event
  engine = create_engine("sqlite:///myfile.db")
  @event.listens_for(engine, "connect")
  def do_connect(dbapi_connection, connection_record):
      # disable sqlite3's emitting of the BEGIN statement entirely.
      dbapi_connection.isolation_level = None
  @event.listens_for(engine, "begin")
  def do_begin(conn):
      # emit our own BEGIN.   sqlite3 still emits COMMIT/ROLLBACK correctly
      conn.exec_driver_sql("BEGIN")
  ```
  When using the asyncio variant `aiosqlite`, refer to `engine.sync_engine`
  as in the example below:
  ```
  from sqlalchemy import create_engine, event
  from sqlalchemy.ext.asyncio import create_async_engine
  engine = create_async_engine("sqlite+aiosqlite:///myfile.db")
  @event.listens_for(engine.sync_engine, "connect")
  def do_connect(dbapi_connection, connection_record):
      # disable aiosqlite's emitting of the BEGIN statement entirely.
      dbapi_connection.isolation_level = None
  @event.listens_for(engine.sync_engine, "begin")
  def do_begin(conn):
      # emit our own BEGIN.  aiosqlite still emits COMMIT/ROLLBACK correctly
      conn.exec_driver_sql("BEGIN")
  ```

### Using SQLAlchemy’s Driver Level AUTOCOMMIT Feature with SQLite

SQLAlchemy has a comprehensive database isolation feature with optional
autocommit support that is introduced in the section [Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit).

For the `sqlite3` and `aiosqlite` drivers, SQLAlchemy only includes
built-in support for “AUTOCOMMIT”.    Note that this mode is currently incompatible
with the non-legacy isolation mode hooks documented in the previous
section at [Enabling Non-Legacy SQLite Transactional Modes with the sqlite3 or aiosqlite driver](#sqlite-enabling-transactions).

To use the `sqlite3` driver with SQLAlchemy driver-level autocommit,
create an engine setting the [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level)
parameter to “AUTOCOMMIT”:

```
eng = create_engine("sqlite:///myfile.db", isolation_level="AUTOCOMMIT")
```

When using the above mode, any event hooks that set the sqlite3 `Connection.autocommit`
parameter away from its default of `sqlite3.LEGACY_TRANSACTION_CONTROL`
as well as hooks that emit `BEGIN` should be disabled.

### Additional Reading for SQLite / sqlite3 transaction control

Links with important information on SQLite, the sqlite3 driver,
as well as long historical conversations on how things got to their current state:

- [Isolation in SQLite](https://www.sqlite.org/isolation.html) - on the SQLite website
- [Transaction control](https://docs.python.org/3/library/sqlite3.html#transaction-control) - describes the sqlite3 autocommit attribute as well
  as the legacy isolation_level attribute.
- [sqlite3 SELECT does not BEGIN a transaction, but should according to spec](https://github.com/python/cpython/issues/54133) - imported Python standard library issue on github
- [sqlite3 module breaks transactions and potentially corrupts data](https://github.com/python/cpython/issues/54949) - imported Python standard library issue on github

## INSERT/UPDATE/DELETE…RETURNING

The SQLite dialect supports SQLite 3.35’s  `INSERT|UPDATE|DELETE..RETURNING`
syntax.   `INSERT..RETURNING` may be used
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

# UPDATE..RETURNING
result = connection.execute(
    table.update()
    .where(table.c.name == "foo")
    .values(name="bar")
    .returning(table.c.col1, table.c.col2)
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

Added in version 2.0: Added support for SQLite RETURNING

## Foreign Key Support

SQLite supports FOREIGN KEY syntax when emitting CREATE statements for tables,
however by default these constraints have no effect on the operation of the
table.

Constraint checking on SQLite has three prerequisites:

- At least version 3.6.19 of SQLite must be in use
- The SQLite library must be compiled *without* the SQLITE_OMIT_FOREIGN_KEY
  or SQLITE_OMIT_TRIGGER symbols enabled.
- The `PRAGMA foreign_keys = ON` statement must be emitted on all
  connections before use – including the initial call to
  [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all).

SQLAlchemy allows for the `PRAGMA` statement to be emitted automatically for
new connections through the usage of events:

```
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # the sqlite3 driver will not set PRAGMA foreign_keys
    # if autocommit=False; set to True temporarily
    ac = dbapi_connection.autocommit
    dbapi_connection.autocommit = True

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

    # restore previous autocommit setting
    dbapi_connection.autocommit = ac
```

Warning

When SQLite foreign keys are enabled, it is **not possible**
to emit CREATE or DROP statements for tables that contain
mutually-dependent foreign key constraints;
to emit the DDL for these tables requires that ALTER TABLE be used to
create or drop these constraints separately, for which SQLite has
no support.

See also

[SQLite Foreign Key Support](https://www.sqlite.org/foreignkeys.html)
- on the SQLite web site.

[Events](https://docs.sqlalchemy.org/en/20/core/event.html) - SQLAlchemy event API.

  [Creating/Dropping Foreign Key Constraints via ALTER](https://docs.sqlalchemy.org/en/20/core/constraints.html#use-alter) - more information on SQLAlchemy’s facilities for handling

mutually-dependent foreign key constraints.

## ON CONFLICT support for constraints

See also

This section describes the [DDL](https://docs.sqlalchemy.org/en/20/glossary.html#term-DDL) version of “ON CONFLICT” for
SQLite, which occurs within a CREATE TABLE statement.  For “ON CONFLICT” as
applied to an INSERT statement, see [INSERT…ON CONFLICT (Upsert)](#sqlite-on-conflict-insert).

SQLite supports a non-standard DDL clause known as ON CONFLICT which can be applied
to primary key, unique, check, and not null constraints.   In DDL, it is
rendered either within the “CONSTRAINT” clause or within the column definition
itself depending on the location of the target constraint.    To render this
clause within DDL, the extension parameter `sqlite_on_conflict` can be
specified with a string conflict resolution algorithm within the
[PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint), [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint),
[CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) objects.  Within the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object,
there
are individual parameters `sqlite_on_conflict_not_null`,
`sqlite_on_conflict_primary_key`, `sqlite_on_conflict_unique` which each
correspond to the three types of relevant constraint types that can be
indicated from a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object.

See also

[ON CONFLICT](https://www.sqlite.org/lang_conflict.html) - in the SQLite
documentation

Added in version 1.3.

The `sqlite_on_conflict` parameters accept a  string argument which is just
the resolution name to be chosen, which on SQLite can be one of ROLLBACK,
ABORT, FAIL, IGNORE, and REPLACE.   For example, to add a UNIQUE constraint
that specifies the IGNORE algorithm:

```
some_table = Table(
    "some_table",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", Integer),
    UniqueConstraint("id", "data", sqlite_on_conflict="IGNORE"),
)
```

The above renders CREATE TABLE DDL as:

```
CREATE TABLE some_table (
    id INTEGER NOT NULL,
    data INTEGER,
    PRIMARY KEY (id),
    UNIQUE (id, data) ON CONFLICT IGNORE
)
```

When using the [Column.unique](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.unique)
flag to add a UNIQUE constraint
to a single column, the `sqlite_on_conflict_unique` parameter can
be added to the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) as well, which will be added to the
UNIQUE constraint in the DDL:

```
some_table = Table(
    "some_table",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "data", Integer, unique=True, sqlite_on_conflict_unique="IGNORE"
    ),
)
```

rendering:

```
CREATE TABLE some_table (
    id INTEGER NOT NULL,
    data INTEGER,
    PRIMARY KEY (id),
    UNIQUE (data) ON CONFLICT IGNORE
)
```

To apply the FAIL algorithm for a NOT NULL constraint,
`sqlite_on_conflict_not_null` is used:

```
some_table = Table(
    "some_table",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "data", Integer, nullable=False, sqlite_on_conflict_not_null="FAIL"
    ),
)
```

this renders the column inline ON CONFLICT phrase:

```
CREATE TABLE some_table (
    id INTEGER NOT NULL,
    data INTEGER NOT NULL ON CONFLICT FAIL,
    PRIMARY KEY (id)
)
```

Similarly, for an inline primary key, use `sqlite_on_conflict_primary_key`:

```
some_table = Table(
    "some_table",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        sqlite_on_conflict_primary_key="FAIL",
    ),
)
```

SQLAlchemy renders the PRIMARY KEY constraint separately, so the conflict
resolution algorithm is applied to the constraint itself:

```
CREATE TABLE some_table (
    id INTEGER NOT NULL,
    PRIMARY KEY (id) ON CONFLICT FAIL
)
```

## INSERT…ON CONFLICT (Upsert)

See also

This section describes the [DML](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML) version of “ON CONFLICT” for
SQLite, which occurs within an INSERT statement.  For “ON CONFLICT” as
applied to a CREATE TABLE statement, see [ON CONFLICT support for constraints](#sqlite-on-conflict-ddl).

From version 3.24.0 onwards, SQLite supports “upserts” (update or insert)
of rows into a table via the `ON CONFLICT` clause of the `INSERT`
statement. A candidate row will only be inserted if that row does not violate
any unique or primary key constraints. In the case of a unique constraint violation, a
secondary action can occur which can be either “DO UPDATE”, indicating that
the data in the target row should be updated, or “DO NOTHING”, which indicates
to silently skip this row.

Conflicts are determined using columns that are part of existing unique
constraints and indexes.  These constraints are identified by stating the
columns and conditions that comprise the indexes.

SQLAlchemy provides `ON CONFLICT` support via the SQLite-specific
[insert()](#sqlalchemy.dialects.sqlite.insert) function, which provides
the generative methods [Insert.on_conflict_do_update()](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update)
and [Insert.on_conflict_do_nothing()](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_nothing):

```
>>> from sqlalchemy.dialects.sqlite import insert

>>> insert_stmt = insert(my_table).values(
...     id="some_existing_id", data="inserted value"
... )

>>> do_update_stmt = insert_stmt.on_conflict_do_update(
...     index_elements=["id"], set_=dict(data="updated value")
... )

>>> print(do_update_stmt)
INSERT INTO my_table (id, data) VALUES (?, ?)
ON CONFLICT (id) DO UPDATE SET data = ?
>>> do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["id"])

>>> print(do_nothing_stmt)
INSERT INTO my_table (id, data) VALUES (?, ?)
ON CONFLICT (id) DO NOTHING
```

Added in version 1.4.

See also

[Upsert](https://sqlite.org/lang_UPSERT.html)
- in the SQLite documentation.

### Specifying the Target

Both methods supply the “target” of the conflict using column inference:

- The [Insert.on_conflict_do_update.index_elements](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update.params.index_elements) argument
  specifies a sequence containing string column names, [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  objects, and/or SQL expression elements, which would identify a unique index
  or unique constraint.
- When using [Insert.on_conflict_do_update.index_elements](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update.params.index_elements)
  to infer an index, a partial index can be inferred by also specifying the
  [Insert.on_conflict_do_update.index_where](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update.params.index_where) parameter:
  ```
  >>> stmt = insert(my_table).values(user_email="[email protected]", data="inserted data")
  >>> do_update_stmt = stmt.on_conflict_do_update(
  ...     index_elements=[my_table.c.user_email],
  ...     index_where=my_table.c.user_email.like("%@gmail.com"),
  ...     set_=dict(data=stmt.excluded.data),
  ... )
  >>> print(do_update_stmt)
  INSERT INTO my_table (data, user_email) VALUES (?, ?)
  ON CONFLICT (user_email)
  WHERE user_email LIKE '%@gmail.com'
  DO UPDATE SET data = excluded.data
  ```

### The SET Clause

`ON CONFLICT...DO UPDATE` is used to perform an update of the already
existing row, using any combination of new values as well as values
from the proposed insertion. These values are specified using the
[Insert.on_conflict_do_update.set_](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update.params.set_) parameter.  This
parameter accepts a dictionary which consists of direct values
for UPDATE:

```
>>> stmt = insert(my_table).values(id="some_id", data="inserted value")

>>> do_update_stmt = stmt.on_conflict_do_update(
...     index_elements=["id"], set_=dict(data="updated value")
... )

>>> print(do_update_stmt)
INSERT INTO my_table (id, data) VALUES (?, ?)
ON CONFLICT (id) DO UPDATE SET data = ?
```

Warning

The [Insert.on_conflict_do_update()](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update) method does **not** take
into account Python-side default UPDATE values or generation functions,
e.g. those specified using [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate). These
values will not be exercised for an ON CONFLICT style of UPDATE, unless
they are manually specified in the
[Insert.on_conflict_do_update.set_](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update.params.set_) dictionary.

### Updating using the Excluded INSERT Values

In order to refer to the proposed insertion row, the special alias
[Insert.excluded](#sqlalchemy.dialects.sqlite.Insert.excluded) is available as an attribute on
the [Insert](#sqlalchemy.dialects.sqlite.Insert) object; this object creates an “excluded.” prefix
on a column, that informs the DO UPDATE to update the row with the value that
would have been inserted had the constraint not failed:

```
>>> stmt = insert(my_table).values(
...     id="some_id", data="inserted value", author="jlh"
... )

>>> do_update_stmt = stmt.on_conflict_do_update(
...     index_elements=["id"],
...     set_=dict(data="updated value", author=stmt.excluded.author),
... )

>>> print(do_update_stmt)
INSERT INTO my_table (id, data, author) VALUES (?, ?, ?)
ON CONFLICT (id) DO UPDATE SET data = ?, author = excluded.author
```

### Additional WHERE Criteria

The [Insert.on_conflict_do_update()](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update) method also accepts
a WHERE clause using the [Insert.on_conflict_do_update.where](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update.params.where)
parameter, which will limit those rows which receive an UPDATE:

```
>>> stmt = insert(my_table).values(
...     id="some_id", data="inserted value", author="jlh"
... )

>>> on_update_stmt = stmt.on_conflict_do_update(
...     index_elements=["id"],
...     set_=dict(data="updated value", author=stmt.excluded.author),
...     where=(my_table.c.status == 2),
... )
>>> print(on_update_stmt)
INSERT INTO my_table (id, data, author) VALUES (?, ?, ?)
ON CONFLICT (id) DO UPDATE SET data = ?, author = excluded.author
WHERE my_table.status = ?
```

### Skipping Rows with DO NOTHING

`ON CONFLICT` may be used to skip inserting a row entirely
if any conflict with a unique constraint occurs; below this is illustrated
using the [Insert.on_conflict_do_nothing()](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_nothing) method:

```
>>> stmt = insert(my_table).values(id="some_id", data="inserted value")
>>> stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
>>> print(stmt)
INSERT INTO my_table (id, data) VALUES (?, ?) ON CONFLICT (id) DO NOTHING
```

If `DO NOTHING` is used without specifying any columns or constraint,
it has the effect of skipping the INSERT for any unique violation which
occurs:

```
>>> stmt = insert(my_table).values(id="some_id", data="inserted value")
>>> stmt = stmt.on_conflict_do_nothing()
>>> print(stmt)
INSERT INTO my_table (id, data) VALUES (?, ?) ON CONFLICT DO NOTHING
```

## Type Reflection

SQLite types are unlike those of most other database backends, in that
the string name of the type usually does not correspond to a “type” in a
one-to-one fashion.  Instead, SQLite links per-column typing behavior
to one of five so-called “type affinities” based on a string matching
pattern for the type.

SQLAlchemy’s reflection process, when inspecting types, uses a simple
lookup table to link the keywords returned to provided SQLAlchemy types.
This lookup table is present within the SQLite dialect as it is for all
other dialects.  However, the SQLite dialect has a different “fallback”
routine for when a particular type name is not located in the lookup map;
it instead implements the SQLite “type affinity” scheme located at
[https://www.sqlite.org/datatype3.html](https://www.sqlite.org/datatype3.html) section 2.1.

The provided typemap will make direct associations from an exact string
name match for the following types:

[BIGINT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BIGINT), [BLOB](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BLOB),
[BOOLEAN](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BOOLEAN), [BOOLEAN](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BOOLEAN),
[CHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.CHAR), [DATE](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DATE),
[DATETIME](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DATETIME), [FLOAT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.FLOAT),
[DECIMAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DECIMAL), [FLOAT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.FLOAT),
[INTEGER](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.INTEGER), [INTEGER](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.INTEGER),
[NUMERIC](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NUMERIC), [REAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.REAL),
[SMALLINT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SMALLINT), [TEXT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TEXT),
[TIME](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIME), [TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP),
[VARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARCHAR), [NVARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NVARCHAR),
[NCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NCHAR)

When a type name does not match one of the above types, the “type affinity”
lookup is used instead:

- [INTEGER](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.INTEGER) is returned if the type name includes the
  string `INT`
- [TEXT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TEXT) is returned if the type name includes the
  string `CHAR`, `CLOB` or `TEXT`
- [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType) is returned if the type name includes the
  string `BLOB`
- [REAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.REAL) is returned if the type name includes the string
  `REAL`, `FLOA` or `DOUB`.
- Otherwise, the [NUMERIC](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NUMERIC) type is used.

## Partial Indexes

A partial index, e.g. one which uses a WHERE clause, can be specified
with the DDL system using the argument `sqlite_where`:

```
tbl = Table("testtbl", m, Column("data", Integer))
idx = Index(
    "test_idx1",
    tbl.c.data,
    sqlite_where=and_(tbl.c.data > 5, tbl.c.data < 10),
)
```

The index will be rendered at create time as:

```
CREATE INDEX test_idx1 ON testtbl (data)
WHERE data > 5 AND data < 10
```

## Dotted Column Names

Using table or column names that explicitly have periods in them is
**not recommended**.   While this is generally a bad idea for relational
databases in general, as the dot is a syntactically significant character,
the SQLite driver up until version **3.10.0** of SQLite has a bug which
requires that SQLAlchemy filter out these dots in result sets.

The bug, entirely outside of SQLAlchemy, can be illustrated thusly:

```
import sqlite3

assert sqlite3.sqlite_version_info < (
    3,
    10,
    0,
), "bug is fixed in this version"

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("create table x (a integer, b integer)")
cursor.execute("insert into x (a, b) values (1, 1)")
cursor.execute("insert into x (a, b) values (2, 2)")

cursor.execute("select x.a, x.b from x")
assert [c[0] for c in cursor.description] == ["a", "b"]

cursor.execute(
    """
    select x.a, x.b from x where a=1
    union
    select x.a, x.b from x where a=2
    """
)
assert [c[0] for c in cursor.description] == ["a", "b"], [
    c[0] for c in cursor.description
]
```

The second assertion fails:

```
Traceback (most recent call last):
  File "test.py", line 19, in <module>
    [c[0] for c in cursor.description]
AssertionError: ['x.a', 'x.b']
```

Where above, the driver incorrectly reports the names of the columns
including the name of the table, which is entirely inconsistent vs.
when the UNION is not present.

SQLAlchemy relies upon column names being predictable in how they match
to the original statement, so the SQLAlchemy dialect has no choice but
to filter these out:

```
from sqlalchemy import create_engine

eng = create_engine("sqlite://")
conn = eng.connect()

conn.exec_driver_sql("create table x (a integer, b integer)")
conn.exec_driver_sql("insert into x (a, b) values (1, 1)")
conn.exec_driver_sql("insert into x (a, b) values (2, 2)")

result = conn.exec_driver_sql("select x.a, x.b from x")
assert result.keys() == ["a", "b"]

result = conn.exec_driver_sql(
    """
    select x.a, x.b from x where a=1
    union
    select x.a, x.b from x where a=2
    """
)
assert result.keys() == ["a", "b"]
```

Note that above, even though SQLAlchemy filters out the dots, *both
names are still addressable*:

```
>>> row = result.first()
>>> row["a"]
1
>>> row["x.a"]
1
>>> row["b"]
1
>>> row["x.b"]
1
```

Therefore, the workaround applied by SQLAlchemy only impacts
[CursorResult.keys()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.keys) and `Row.keys()` in the public API. In
the very specific case where an application is forced to use column names that
contain dots, and the functionality of [CursorResult.keys()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.keys) and
`Row.keys()` is required to return these dotted names unmodified,
the `sqlite_raw_colnames` execution option may be provided, either on a
per-[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) basis:

```
result = conn.execution_options(sqlite_raw_colnames=True).exec_driver_sql(
    """
    select x.a, x.b from x where a=1
    union
    select x.a, x.b from x where a=2
    """
)
assert result.keys() == ["x.a", "x.b"]
```

or on a per-[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) basis:

```
engine = create_engine(
    "sqlite://", execution_options={"sqlite_raw_colnames": True}
)
```

When using the per-[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) execution option, note that
**Core and ORM queries that use UNION may not function properly**.

## SQLite-specific table options

One option for CREATE TABLE is supported directly by the SQLite
dialect in conjunction with the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct:

- `WITHOUT ROWID`:
  ```
  Table("some_table", metadata, ..., sqlite_with_rowid=False)
  ```
- `STRICT`:
  ```
  Table("some_table", metadata, ..., sqlite_strict=True)
  ```
  Added in version 2.0.37.

See also

[SQLite CREATE TABLE options](https://www.sqlite.org/lang_createtable.html)

## Reflecting internal schema tables

Reflection methods that return lists of tables will omit so-called
“SQLite internal schema object” names, which are considered by SQLite
as any object name that is prefixed with `sqlite_`.  An example of
such an object is the `sqlite_sequence` table that’s generated when
the `AUTOINCREMENT` column parameter is used.   In order to return
these objects, the parameter `sqlite_include_internal=True` may be
passed to methods such as [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) or
[Inspector.get_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names).

Added in version 2.0: Added the `sqlite_include_internal=True` parameter.
Previously, these tables were not ignored by SQLAlchemy reflection
methods.

Note

The `sqlite_include_internal` parameter does not refer to the
“system” tables that are present in schemas such as `sqlite_master`.

See also

[SQLite Internal Schema Objects](https://www.sqlite.org/fileformat2.html#intschema) - in the SQLite
documentation.

## SQLite Data Types

As with all SQLAlchemy dialects, all UPPERCASE types that are known to be
valid with SQLite are importable from the top level dialect, whether
they originate from [sqlalchemy.types](https://docs.sqlalchemy.org/en/20/core/type_basics.html#module-sqlalchemy.types) or from the local dialect:

```
from sqlalchemy.dialects.sqlite import (
    BLOB,
    BOOLEAN,
    CHAR,
    DATE,
    DATETIME,
    DECIMAL,
    FLOAT,
    INTEGER,
    NUMERIC,
    JSON,
    SMALLINT,
    TEXT,
    TIME,
    TIMESTAMP,
    VARCHAR,
)
```

| Object Name | Description |
| --- | --- |
| DATE | Represent a Python date object in SQLite using a string. |
| DATETIME | Represent a Python datetime object in SQLite using a string. |
| JSON | SQLite JSON type. |
| TIME | Represent a Python time object in SQLite using a string. |

   class sqlalchemy.dialects.sqlite.DATETIME

*inherits from* `sqlalchemy.dialects.sqlite.base._DateTimeMixin`, [sqlalchemy.types.DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime)

Represent a Python datetime object in SQLite using a string.

The default string storage format is:

```
"%(year)04d-%(month)02d-%(day)02d %(hour)02d:%(minute)02d:%(second)02d.%(microsecond)06d"
```

e.g.:

```
2021-03-15 12:05:57.105542
```

The incoming storage format is by default parsed using the
Python `datetime.fromisoformat()` function.

Changed in version 2.0: `datetime.fromisoformat()` is used for default
datetime string parsing.

The storage format can be customized to some degree using the
`storage_format` and `regexp` parameters, such as:

```
import re
from sqlalchemy.dialects.sqlite import DATETIME

dt = DATETIME(
    storage_format=(
        "%(year)04d/%(month)02d/%(day)02d %(hour)02d:%(minute)02d:%(second)02d"
    ),
    regexp=r"(\d+)/(\d+)/(\d+) (\d+)-(\d+)-(\d+)",
)
```

   Parameters:

- **truncate_microseconds** – when `True` microseconds will be truncated
  from the datetime. Can’t be specified together with `storage_format`
  or `regexp`.
- **storage_format** – format string which will be applied to the dict
  with keys year, month, day, hour, minute, second, and microsecond.
- **regexp** – regular expression which will be applied to incoming result
  rows, replacing the use of `datetime.fromisoformat()` to parse incoming
  strings. If the regexp contains named groups, the resulting match dict is
  applied to the Python datetime() constructor as keyword arguments.
  Otherwise, if positional groups are used, the datetime() constructor
  is called with positional arguments via
  `*map(int, match_obj.groups(0))`.

      class sqlalchemy.dialects.sqlite.DATE

*inherits from* `sqlalchemy.dialects.sqlite.base._DateTimeMixin`, [sqlalchemy.types.Date](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Date)

Represent a Python date object in SQLite using a string.

The default string storage format is:

```
"%(year)04d-%(month)02d-%(day)02d"
```

e.g.:

```
2011-03-15
```

The incoming storage format is by default parsed using the
Python `date.fromisoformat()` function.

Changed in version 2.0: `date.fromisoformat()` is used for default
date string parsing.

The storage format can be customized to some degree using the
`storage_format` and `regexp` parameters, such as:

```
import re
from sqlalchemy.dialects.sqlite import DATE

d = DATE(
    storage_format="%(month)02d/%(day)02d/%(year)04d",
    regexp=re.compile("(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)"),
)
```

   Parameters:

- **storage_format** – format string which will be applied to the
  dict with keys year, month, and day.
- **regexp** – regular expression which will be applied to
  incoming result rows, replacing the use of `date.fromisoformat()` to
  parse incoming strings. If the regexp contains named groups, the resulting
  match dict is applied to the Python date() constructor as keyword
  arguments. Otherwise, if positional groups are used, the date()
  constructor is called with positional arguments via
  `*map(int, match_obj.groups(0))`.

      class sqlalchemy.dialects.sqlite.JSON

*inherits from* [sqlalchemy.types.JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)

SQLite JSON type.

SQLite supports JSON as of version 3.9 through its [JSON1](https://www.sqlite.org/json1.html) extension. Note
that [JSON1](https://www.sqlite.org/json1.html) is a
[loadable extension](https://www.sqlite.org/loadext.html) and as such
may not be available, or may require run-time loading.

[JSON](#sqlalchemy.dialects.sqlite.JSON) is used automatically whenever the base
[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) datatype is used against a SQLite backend.

See also

[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) - main documentation for the generic
cross-platform JSON datatype.

The [JSON](#sqlalchemy.dialects.sqlite.JSON) type supports persistence of JSON values
as well as the core index operations provided by [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)
datatype, by adapting the operations to render the `JSON_EXTRACT`
function wrapped in the `JSON_QUOTE` function at the database level.
Extracted values are quoted in order to ensure that the results are
always JSON string values.

Added in version 1.3.

| Member Name | Description |
| --- | --- |
| __init__() | Construct aJSONtype. |

   method [sqlalchemy.dialects.sqlite.JSON.](#sqlalchemy.dialects.sqlite.JSON)__init__(*none_as_null:bool=False*)

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

        class sqlalchemy.dialects.sqlite.TIME

*inherits from* `sqlalchemy.dialects.sqlite.base._DateTimeMixin`, [sqlalchemy.types.Time](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Time)

Represent a Python time object in SQLite using a string.

The default string storage format is:

```
"%(hour)02d:%(minute)02d:%(second)02d.%(microsecond)06d"
```

e.g.:

```
12:05:57.10558
```

The incoming storage format is by default parsed using the
Python `time.fromisoformat()` function.

Changed in version 2.0: `time.fromisoformat()` is used for default
time string parsing.

The storage format can be customized to some degree using the
`storage_format` and `regexp` parameters, such as:

```
import re
from sqlalchemy.dialects.sqlite import TIME

t = TIME(
    storage_format="%(hour)02d-%(minute)02d-%(second)02d-%(microsecond)06d",
    regexp=re.compile("(\d+)-(\d+)-(\d+)-(?:-(\d+))?"),
)
```

   Parameters:

- **truncate_microseconds** – when `True` microseconds will be truncated
  from the time. Can’t be specified together with `storage_format`
  or `regexp`.
- **storage_format** – format string which will be applied to the dict
  with keys hour, minute, second, and microsecond.
- **regexp** – regular expression which will be applied to incoming result
  rows, replacing the use of `datetime.fromisoformat()` to parse incoming
  strings. If the regexp contains named groups, the resulting match dict is
  applied to the Python time() constructor as keyword arguments. Otherwise,
  if positional groups are used, the time() constructor is called with
  positional arguments via `*map(int, match_obj.groups(0))`.

## SQLite DML Constructs

| Object Name | Description |
| --- | --- |
| insert(table) | Construct a sqlite-specific variantInsertconstruct. |
| Insert | SQLite-specific implementation of INSERT. |

   function sqlalchemy.dialects.sqlite.insert(*table:_DMLTableArgument*) → [Insert](#sqlalchemy.dialects.sqlite.Insert)

Construct a sqlite-specific variant [Insert](#sqlalchemy.dialects.sqlite.Insert)
construct.

The [sqlalchemy.dialects.sqlite.insert()](#sqlalchemy.dialects.sqlite.insert) function creates
a [sqlalchemy.dialects.sqlite.Insert](#sqlalchemy.dialects.sqlite.Insert).  This class is based
on the dialect-agnostic [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct which may
be constructed using the [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) function in
SQLAlchemy Core.

The [Insert](#sqlalchemy.dialects.sqlite.Insert) construct includes additional methods
[Insert.on_conflict_do_update()](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update),
[Insert.on_conflict_do_nothing()](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_nothing).

    class sqlalchemy.dialects.sqlite.Insert

*inherits from* [sqlalchemy.sql.expression.Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)

SQLite-specific implementation of INSERT.

Adds methods for SQLite-specific syntaxes such as ON CONFLICT.

The [Insert](#sqlalchemy.dialects.sqlite.Insert) object is created using the
[sqlalchemy.dialects.sqlite.insert()](#sqlalchemy.dialects.sqlite.insert) function.

Added in version 1.4.

See also

[INSERT…ON CONFLICT (Upsert)](#sqlite-on-conflict-insert)

| Member Name | Description |
| --- | --- |
| excluded | Provide theexcludednamespace for an ON CONFLICT statement |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| on_conflict_do_nothing() | Specifies a DO NOTHING action for ON CONFLICT clause. |
| on_conflict_do_update() | Specifies a DO UPDATE SET action for ON CONFLICT clause. |

   attribute [sqlalchemy.dialects.sqlite.Insert.](#sqlalchemy.dialects.sqlite.Insert)excluded

Provide the `excluded` namespace for an ON CONFLICT statement

SQLite’s ON CONFLICT clause allows reference to the row that would
be inserted, known as `excluded`.  This attribute provides
all columns in this row to be referenceable.

Tip

The [Insert.excluded](#sqlalchemy.dialects.sqlite.Insert.excluded) attribute is an instance
of [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection), which provides an
interface the same as that of the [Table.c](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.c)
collection described at [Accessing Tables and Columns](https://docs.sqlalchemy.org/en/20/core/metadata.html#metadata-tables-and-columns).
With this collection, ordinary names are accessible like attributes
(e.g. `stmt.excluded.some_column`), but special names and
dictionary method names should be accessed using indexed access,
such as `stmt.excluded["column name"]` or
`stmt.excluded["values"]`.  See the docstring for
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) for further examples.

     attribute [sqlalchemy.dialects.sqlite.Insert.](#sqlalchemy.dialects.sqlite.Insert)inherit_cache = False

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

     method [sqlalchemy.dialects.sqlite.Insert.](#sqlalchemy.dialects.sqlite.Insert)on_conflict_do_nothing(*index_elements:Iterable[Column[Any]|str|DDLConstraintColumnRole]|None=None*, *index_where:WhereHavingRole|None=None*) → Self

Specifies a DO NOTHING action for ON CONFLICT clause.

  Parameters:

- **index_elements** – A sequence consisting of string column names, [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  objects, or other column expression objects that will be used
  to infer a target index or unique constraint.
- **index_where** – Additional WHERE criterion that can be used to infer a
  conditional target index.

      method [sqlalchemy.dialects.sqlite.Insert.](#sqlalchemy.dialects.sqlite.Insert)on_conflict_do_update(*index_elements:Iterable[Column[Any]|str|DDLConstraintColumnRole]|None=None*, *index_where:WhereHavingRole|None=None*, *set_:Mapping[Any,Any]|ColumnCollection[Any,Any]|None=None*, *where:WhereHavingRole|None=None*) → Self

Specifies a DO UPDATE SET action for ON CONFLICT clause.

  Parameters:

- **index_elements** – A sequence consisting of string column names, [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  objects, or other column expression objects that will be used
  to infer a target index or unique constraint.
- **index_where** – Additional WHERE criterion that can be used to infer a
  conditional target index.
- **set_** –
  A dictionary or other mapping object
  where the keys are either names of columns in the target table,
  or [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects or other ORM-mapped columns
  matching that of the target table, and expressions or literals
  as values, specifying the `SET` actions to take.
  Added in version 1.4: The
  [Insert.on_conflict_do_update.set_](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update.params.set_)
  parameter supports [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects from the target
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) as keys.
  Warning
  This dictionary does **not** take into account
  Python-specified default UPDATE values or generation functions,
  e.g. those specified using [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate).
  These values will not be exercised for an ON CONFLICT style of
  UPDATE, unless they are manually specified in the
  [Insert.on_conflict_do_update.set_](#sqlalchemy.dialects.sqlite.Insert.on_conflict_do_update.params.set_) dictionary.
- **where** – Optional argument. An expression object representing a `WHERE`
  clause that restricts the rows affected by `DO UPDATE SET`. Rows not
  meeting the `WHERE` condition will not be updated (effectively a
  `DO NOTHING` for those rows).

## Pysqlite

Support for the SQLite database via the pysqlite driver.

Note that `pysqlite` is the same driver as the `sqlite3`
module included with the Python distribution.

### DBAPI

Documentation and download information (if applicable) for pysqlite is available at:
[https://docs.python.org/library/sqlite3.html](https://docs.python.org/library/sqlite3.html)

### Connecting

Connect String:

```
sqlite+pysqlite:///file_path
```

### Driver

The `sqlite3` Python DBAPI is standard on all modern Python versions;
for cPython and Pypy, no additional installation is necessary.

### Connect Strings

The file specification for the SQLite database is taken as the “database”
portion of the URL.  Note that the format of a SQLAlchemy url is:

```
driver://user:pass@host/database
```

This means that the actual filename to be used starts with the characters to
the **right** of the third slash.   So connecting to a relative filepath
looks like:

```
# relative path
e = create_engine("sqlite:///path/to/database.db")
```

An absolute path, which is denoted by starting with a slash, means you
need **four** slashes:

```
# absolute path
e = create_engine("sqlite:////path/to/database.db")
```

To use a Windows path, regular drive specifications and backslashes can be
used. Double backslashes are probably needed:

```
# absolute path on Windows
e = create_engine("sqlite:///C:\\path\\to\\database.db")
```

To use sqlite `:memory:` database specify it as the filename using
`sqlite:///:memory:`. It’s also the default if no filepath is
present, specifying only `sqlite://` and nothing else:

```
# in-memory database (note three slashes)
e = create_engine("sqlite:///:memory:")
# also in-memory database
e2 = create_engine("sqlite://")
```

#### URI Connections

Modern versions of SQLite support an alternative system of connecting using a
[driver level URI](https://www.sqlite.org/uri.html), which has the  advantage
that additional driver-level arguments can be passed including options such as
“read only”.   The Python sqlite3 driver supports this mode under modern Python
3 versions.   The SQLAlchemy pysqlite driver supports this mode of use by
specifying “uri=true” in the URL query string.  The SQLite-level “URI” is kept
as the “database” portion of the SQLAlchemy url (that is, following a slash):

```
e = create_engine("sqlite:///file:path/to/database?mode=ro&uri=true")
```

Note

The “uri=true” parameter must appear in the **query string**
of the URL.  It will not currently work as expected if it is only
present in the [create_engine.connect_args](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.connect_args)
parameter dictionary.

The logic reconciles the simultaneous presence of SQLAlchemy’s query string and
SQLite’s query string by separating out the parameters that belong to the
Python sqlite3 driver vs. those that belong to the SQLite URI.  This is
achieved through the use of a fixed list of parameters known to be accepted by
the Python side of the driver.  For example, to include a URL that indicates
the Python sqlite3 “timeout” and “check_same_thread” parameters, along with the
SQLite “mode” and “nolock” parameters, they can all be passed together on the
query string:

```
e = create_engine(
    "sqlite:///file:path/to/database?"
    "check_same_thread=true&timeout=10&mode=ro&nolock=1&uri=true"
)
```

Above, the pysqlite / sqlite3 DBAPI would be passed arguments as:

```
sqlite3.connect(
    "file:path/to/database?mode=ro&nolock=1",
    check_same_thread=True,
    timeout=10,
    uri=True,
)
```

Regarding future parameters added to either the Python or native drivers. new
parameter names added to the SQLite URI scheme should be automatically
accommodated by this scheme.  New parameter names added to the Python driver
side can be accommodated by specifying them in the
[create_engine.connect_args](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.connect_args) dictionary,
until dialect support is
added by SQLAlchemy.   For the less likely case that the native SQLite driver
adds a new parameter name that overlaps with one of the existing, known Python
driver parameters (such as “timeout” perhaps), SQLAlchemy’s dialect would
require adjustment for the URL scheme to continue to support this.

As is always the case for all SQLAlchemy dialects, the entire “URL” process
can be bypassed in [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) through the use of the
[create_engine.creator](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.creator)
parameter which allows for a custom callable
that creates a Python sqlite3 driver level connection directly.

Added in version 1.3.9.

See also

[Uniform Resource Identifiers](https://www.sqlite.org/uri.html) - in
the SQLite documentation

### Regular Expression Support

Added in version 1.4.

Support for the [ColumnOperators.regexp_match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_match) operator is provided
using Python’s [re.search](https://docs.python.org/3/library/re.html#re.search) function.  SQLite itself does not include a working
regular expression operator; instead, it includes a non-implemented placeholder
operator `REGEXP` that calls a user-defined function that must be provided.

SQLAlchemy’s implementation makes use of the pysqlite [create_function](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.create_function) hook
as follows:

```
def regexp(a, b):
    return re.search(a, b) is not None

sqlite_connection.create_function(
    "regexp",
    2,
    regexp,
)
```

There is currently no support for regular expression flags as a separate
argument, as these are not supported by SQLite’s REGEXP operator, however these
may be included inline within the regular expression string.  See [Python regular expressions](https://docs.python.org/3/library/re.html#re.search) for
details.

See also

[Python regular expressions](https://docs.python.org/3/library/re.html#re.search): Documentation for Python’s regular expression syntax.

### Compatibility with sqlite3 “native” date and datetime types

The pysqlite driver includes the sqlite3.PARSE_DECLTYPES and
sqlite3.PARSE_COLNAMES options, which have the effect of any column
or expression explicitly cast as “date” or “timestamp” will be converted
to a Python date or datetime object.  The date and datetime types provided
with the pysqlite dialect are not currently compatible with these options,
since they render the ISO date/datetime including microseconds, which
pysqlite’s driver does not.   Additionally, SQLAlchemy does not at
this time automatically render the “cast” syntax required for the
freestanding functions “current_timestamp” and “current_date” to return
datetime/date types natively.   Unfortunately, pysqlite
does not provide the standard DBAPI types in `cursor.description`,
leaving SQLAlchemy with no way to detect these types on the fly
without expensive per-row type checks.

Keeping in mind that pysqlite’s parsing option is not recommended,
nor should be necessary, for use with SQLAlchemy, usage of PARSE_DECLTYPES
can be forced if one configures “native_datetime=True” on create_engine():

```
engine = create_engine(
    "sqlite://",
    connect_args={
        "detect_types": sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    },
    native_datetime=True,
)
```

With this flag enabled, the DATE and TIMESTAMP types (but note - not the
DATETIME or TIME types…confused yet ?) will not perform any bind parameter
or result processing. Execution of “func.current_date()” will return a string.
“func.current_timestamp()” is registered as returning a DATETIME type in
SQLAlchemy, so this function still receives SQLAlchemy-level result
processing.

### Threading/Pooling Behavior

The `sqlite3` DBAPI by default prohibits the use of a particular connection
in a thread which is not the one in which it was created.  As SQLite has
matured, it’s behavior under multiple threads has improved, and even includes
options for memory only databases to be used in multiple threads.

The thread prohibition is known as “check same thread” and may be controlled
using the `sqlite3` parameter `check_same_thread`, which will disable or
enable this check. SQLAlchemy’s default behavior here is to set
`check_same_thread` to `False` automatically whenever a file-based database
is in use, to establish compatibility with the default pool class
[QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool).

The SQLAlchemy `pysqlite` DBAPI establishes the connection pool differently
based on the kind of SQLite database that’s requested:

- When a `:memory:` SQLite database is specified, the dialect by default
  will use [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool). This pool maintains a single
  connection per thread, so that all access to the engine within the current
  thread use the same `:memory:` database - other threads would access a
  different `:memory:` database.  The `check_same_thread` parameter
  defaults to `True`.
- When a file-based database is specified, the dialect will use
  [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) as the source of connections.   at the same time,
  the `check_same_thread` flag is set to False by default unless overridden.
  Changed in version 2.0: SQLite file database engines now use [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) by default.
  Previously, [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) were used.  The [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) class
  may be used by specifying it via the
  [create_engine.poolclass](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.poolclass) parameter.

#### Disabling Connection Pooling for File Databases

Pooling may be disabled for a file based database by specifying the
[NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) implementation for the `poolclass()`
parameter:

```
from sqlalchemy import NullPool

engine = create_engine("sqlite:///myfile.db", poolclass=NullPool)
```

It’s been observed that the [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) implementation incurs an
extremely small performance overhead for repeated checkouts due to the lack of
connection reuse implemented by [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool).  However, it still
may be beneficial to use this class if the application is experiencing
issues with files being locked.

#### Using a Memory Database in Multiple Threads

To use a `:memory:` database in a multithreaded scenario, the same
connection object must be shared among threads, since the database exists
only within the scope of that connection.   The
[StaticPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.StaticPool) implementation will maintain a single connection
globally, and the `check_same_thread` flag can be passed to Pysqlite
as `False`:

```
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
```

Note that using a `:memory:` database in multiple threads requires a recent
version of SQLite.

#### Using Temporary Tables with SQLite

Due to the way SQLite deals with temporary tables, if you wish to use a
temporary table in a file-based SQLite database across multiple checkouts
from the connection pool, such as when using an ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) where
the temporary table should continue to remain after [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) or
[Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) is called, a pool which maintains a single
connection must be used.   Use [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool) if the scope is
only needed within the current thread, or [StaticPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.StaticPool) is scope is
needed within multiple threads for this case:

```
# maintain the same connection per thread
from sqlalchemy.pool import SingletonThreadPool

engine = create_engine("sqlite:///mydb.db", poolclass=SingletonThreadPool)

# maintain the same connection across all threads
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite:///mydb.db", poolclass=StaticPool)
```

Note that [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool) should be configured for the number
of threads that are to be used; beyond that number, connections will be
closed out in a non deterministic way.

### Dealing with Mixed String / Binary Columns

The SQLite database is weakly typed, and as such it is possible when using
binary values, which in Python are represented as `b'some string'`, that a
particular SQLite database can have data values within different rows where
some of them will be returned as a `b''` value by the Pysqlite driver, and
others will be returned as Python strings, e.g. `''` values.   This situation
is not known to occur if the SQLAlchemy [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) datatype is used
consistently, however if a particular SQLite database has data that was
inserted using the Pysqlite driver directly, or when using the SQLAlchemy
[String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) type which was later changed to [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary), the
table will not be consistently readable because SQLAlchemy’s
[LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) datatype does not handle strings so it has no way of
“encoding” a value that is in string format.

To deal with a SQLite table that has mixed string / binary data in the
same column, use a custom type that will check each row individually:

```
from sqlalchemy import String
from sqlalchemy import TypeDecorator

class MixedBinary(TypeDecorator):
    impl = String
    cache_ok = True

    def process_result_value(self, value, dialect):
        if isinstance(value, str):
            value = bytes(value, "utf-8")
        elif value is not None:
            value = bytes(value)

        return value
```

Then use the above `MixedBinary` datatype in the place where
[LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) would normally be used.

### Serializable isolation / Savepoints / Transactional DDL

A newly revised version of this important section is now available
at the top level of the SQLAlchemy SQLite documentation, in the section
[Transactions with SQLite and the sqlite3 driver](#sqlite-transactions).

### User-Defined Functions

pysqlite supports a [create_function()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.create_function)
method that allows us to create our own user-defined functions (UDFs) in Python and use them directly in SQLite queries.
These functions are registered with a specific DBAPI Connection.

SQLAlchemy uses connection pooling with file-based SQLite databases, so we need to ensure that the UDF is attached to the
connection when it is created. That is accomplished with an event listener:

```
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import text

def udf():
    return "udf-ok"

engine = create_engine("sqlite:///./db_file")

@event.listens_for(engine, "connect")
def connect(conn, rec):
    conn.create_function("udf", 0, udf)

for i in range(5):
    with engine.connect() as conn:
        print(conn.scalar(text("SELECT UDF()")))
```

## Aiosqlite

Support for the SQLite database via the aiosqlite driver.

### DBAPI

Documentation and download information (if applicable) for aiosqlite is available at:
[https://pypi.org/project/aiosqlite/](https://pypi.org/project/aiosqlite/)

### Connecting

Connect String:

```
sqlite+aiosqlite:///file_path
```

The aiosqlite dialect provides support for the SQLAlchemy asyncio interface
running on top of pysqlite.

aiosqlite is a wrapper around pysqlite that uses a background thread for
each connection.   It does not actually use non-blocking IO, as SQLite
databases are not socket-based.  However it does provide a working asyncio
interface that’s useful for testing and prototyping purposes.

Using a special asyncio mediation layer, the aiosqlite dialect is usable
as the backend for the [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
extension package.

This dialect should normally be used only with the
[create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) engine creation function:

```
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///filename")
```

The URL passes through all arguments to the `pysqlite` driver, so all
connection arguments are the same as they are for that of [Pysqlite](#pysqlite).

### User-Defined Functions

aiosqlite extends pysqlite to support async, so we can create our own user-defined functions (UDFs)
in Python and use them directly in SQLite queries as described here: [User-Defined Functions](#pysqlite-udfs).

### Serializable isolation / Savepoints / Transactional DDL (asyncio version)

A newly revised version of this important section is now available
at the top level of the SQLAlchemy SQLite documentation, in the section
[Transactions with SQLite and the sqlite3 driver](#sqlite-transactions).

### Pooling Behavior

The SQLAlchemy `aiosqlite` DBAPI establishes the connection pool differently
based on the kind of SQLite database that’s requested:

- When a `:memory:` SQLite database is specified, the dialect by default
  will use [StaticPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.StaticPool). This pool maintains a single
  connection, so that all access to the engine
  use the same `:memory:` database.
- When a file-based database is specified, the dialect will use
  [AsyncAdaptedQueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AsyncAdaptedQueuePool) as the source of connections.
  Changed in version 2.0.38: SQLite file database engines now use [AsyncAdaptedQueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AsyncAdaptedQueuePool) by default.
  Previously, [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) were used.  The [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) class
  may be used by specifying it via the
  [create_engine.poolclass](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.poolclass) parameter.

## Pysqlcipher

Support for the SQLite database via the pysqlcipher driver.

Dialect for support of DBAPIs that make use of the
[SQLCipher](https://www.zetetic.net/sqlcipher) backend.

### Connecting

Connect String:

```
sqlite+pysqlcipher://:passphrase@/file_path[?kdf_iter=<iter>]
```

### Driver

Current dialect selection logic is:

- If the [create_engine.module](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.module) parameter supplies a DBAPI module,
  that module is used.
- Otherwise for Python 3, choose [https://pypi.org/project/sqlcipher3/](https://pypi.org/project/sqlcipher3/)
- If not available, fall back to [https://pypi.org/project/pysqlcipher3/](https://pypi.org/project/pysqlcipher3/)
- For Python 2, [https://pypi.org/project/pysqlcipher/](https://pypi.org/project/pysqlcipher/) is used.

Warning

The `pysqlcipher3` and `pysqlcipher` DBAPI drivers are no
longer maintained; the `sqlcipher3` driver as of this writing appears
to be current.  For future compatibility, any pysqlcipher-compatible DBAPI
may be used as follows:

```
import sqlcipher_compatible_driver

from sqlalchemy import create_engine

e = create_engine(
    "sqlite+pysqlcipher://:password@/dbname.db",
    module=sqlcipher_compatible_driver,
)
```

These drivers make use of the SQLCipher engine. This system essentially
introduces new PRAGMA commands to SQLite which allows the setting of a
passphrase and other encryption parameters, allowing the database file to be
encrypted.

### Connect Strings

The format of the connect string is in every way the same as that
of the [pysqlite](#module-sqlalchemy.dialects.sqlite.pysqlite) driver, except that the
“password” field is now accepted, which should contain a passphrase:

```
e = create_engine("sqlite+pysqlcipher://:testing@/foo.db")
```

For an absolute file path, two leading slashes should be used for the
database name:

```
e = create_engine("sqlite+pysqlcipher://:testing@//path/to/foo.db")
```

A selection of additional encryption-related pragmas supported by SQLCipher
as documented at [https://www.zetetic.net/sqlcipher/sqlcipher-api/](https://www.zetetic.net/sqlcipher/sqlcipher-api/) can be passed
in the query string, and will result in that PRAGMA being called for each
new connection.  Currently, `cipher`, `kdf_iter` `cipher_page_size` and `cipher_use_hmac` are supported:

```
e = create_engine(
    "sqlite+pysqlcipher://:testing@/foo.db?cipher=aes-256-cfb&kdf_iter=64000"
)
```

Warning

Previous versions of sqlalchemy did not take into consideration
the encryption-related pragmas passed in the url string, that were silently
ignored. This may cause errors when opening files saved by a
previous sqlalchemy version if the encryption options do not match.

### Pooling Behavior

The driver makes a change to the default pool behavior of pysqlite
as described in [Threading/Pooling Behavior](#pysqlite-threading-pooling).   The pysqlcipher driver
has been observed to be significantly slower on connection than the
pysqlite driver, most likely due to the encryption overhead, so the
dialect here defaults to using the [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool)
implementation,
instead of the [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) pool used by pysqlite.  As always, the pool
implementation is entirely configurable using the
[create_engine.poolclass](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.poolclass) parameter; the `
StaticPool` may
be more feasible for single-threaded use, or [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) may be used
to prevent unencrypted connections from being held open for long periods of
time, at the expense of slower startup time for new connections.
