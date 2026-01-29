# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Working with Engines and Connections

This section details direct usage of the [Engine](#sqlalchemy.engine.Engine),
[Connection](#sqlalchemy.engine.Connection), and related objects. Its important to note that when
using the SQLAlchemy ORM, these objects are not generally accessed; instead,
the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object is used as the interface to the database.
However, for applications that are built around direct usage of textual SQL
statements and/or SQL expression constructs without involvement by the ORM’s
higher level management services, the [Engine](#sqlalchemy.engine.Engine) and
[Connection](#sqlalchemy.engine.Connection) are king (and queen?) - read on.

## Basic Usage

Recall from [Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html) that an [Engine](#sqlalchemy.engine.Engine) is created via
the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) call:

```
engine = create_engine("mysql+mysqldb://scott:tiger@localhost/test")
```

The typical usage of [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) is once per particular database
URL, held globally for the lifetime of a single application process. A single
[Engine](#sqlalchemy.engine.Engine) manages many individual [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) connections on behalf of
the process and is intended to be called upon in a concurrent fashion. The
[Engine](#sqlalchemy.engine.Engine) is **not** synonymous to the DBAPI `connect()` function, which
represents just one connection resource - the [Engine](#sqlalchemy.engine.Engine) is most
efficient when created just once at the module level of an application, not
per-object or per-function call.

tip

When using an [Engine](#sqlalchemy.engine.Engine) with multiple Python processes, such as when
using `os.fork` or Python `multiprocessing`, it’s important that the
engine is initialized per process.  See [Using Connection Pools with Multiprocessing or os.fork()](https://docs.sqlalchemy.org/en/20/core/pooling.html#pooling-multiprocessing) for
details.

The most basic function of the [Engine](#sqlalchemy.engine.Engine) is to provide access to a
[Connection](#sqlalchemy.engine.Connection), which can then invoke SQL statements.   To emit
a textual statement to the database looks like:

```
from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("select username from users"))
    for row in result:
        print("username:", row.username)
```

Above, the [Engine.connect()](#sqlalchemy.engine.Engine.connect) method returns a [Connection](#sqlalchemy.engine.Connection)
object, and by using it in a Python context manager (e.g. the `with:`
statement) the [Connection.close()](#sqlalchemy.engine.Connection.close) method is automatically invoked at the
end of the block.  The [Connection](#sqlalchemy.engine.Connection), is a **proxy** object for an
actual DBAPI connection. The DBAPI connection is retrieved from the connection
pool at the point at which [Connection](#sqlalchemy.engine.Connection) is created.

The object returned is known as [CursorResult](#sqlalchemy.engine.CursorResult), which
references a DBAPI cursor and provides methods for fetching rows
similar to that of the DBAPI cursor.   The DBAPI cursor will be closed
by the [CursorResult](#sqlalchemy.engine.CursorResult) when all of its result rows (if any) are
exhausted.  A [CursorResult](#sqlalchemy.engine.CursorResult) that returns no rows, such as that of
an UPDATE statement (without any returned rows),
releases cursor resources immediately upon construction.

When the [Connection](#sqlalchemy.engine.Connection) is closed at the end of the `with:` block, the
referenced DBAPI connection is [released](https://docs.sqlalchemy.org/en/20/glossary.html#term-released) to the connection pool.   From
the perspective of the database itself, the connection pool will not actually
“close” the connection assuming the pool has room to store this connection  for
the next use.  When the connection is returned to the pool for reuse, the
pooling mechanism issues a `rollback()` call on the DBAPI connection so that
any transactional state or locks are removed (this is known as
[Reset On Return](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-reset-on-return)), and the connection is ready for its next use.

Our example above illustrated the execution of a textual SQL string, which
should be invoked by using the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct to indicate that
we’d like to use textual SQL.  The [Connection.execute()](#sqlalchemy.engine.Connection.execute) method can of
course accommodate more than that; see [Working with Data](https://docs.sqlalchemy.org/en/20/tutorial/data.html#tutorial-working-with-data)
in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial) for a tutorial.

## Using Transactions

Note

This section describes how to use transactions when working directly
with [Engine](#sqlalchemy.engine.Engine) and [Connection](#sqlalchemy.engine.Connection) objects. When using the
SQLAlchemy ORM, the public API for transaction control is via the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object, which makes usage of the [Transaction](#sqlalchemy.engine.Transaction)
object internally. See [Managing Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#unitofwork-transaction) for further
information.

### Commit As You Go

The [Connection](#sqlalchemy.engine.Connection) object always emits SQL statements
within the context of a transaction block.   The first time the
[Connection.execute()](#sqlalchemy.engine.Connection.execute) method is called to execute a SQL
statement, this transaction is begun automatically, using a behavior known
as **autobegin**.  The transaction remains in place for the scope of the
[Connection](#sqlalchemy.engine.Connection) object until the [Connection.commit()](#sqlalchemy.engine.Connection.commit)
or [Connection.rollback()](#sqlalchemy.engine.Connection.rollback) methods are called.  Subsequent
to the transaction ending, the [Connection](#sqlalchemy.engine.Connection) waits for the
[Connection.execute()](#sqlalchemy.engine.Connection.execute) method to be called again, at which point
it autobegins again.

This calling style is known as **commit as you go**, and is
illustrated in the example below:

```
with engine.connect() as connection:
    connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})
    connection.execute(
        some_other_table.insert(), {"q": 8, "p": "this is some more data"}
    )

    connection.commit()  # commit the transaction
```

the Python DBAPI is where autobegin actually happens

The design of “commit as you go” is intended to be complementary to the
design of the [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI), which is the underlying database interface
that SQLAlchemy interacts with. In the DBAPI, the `connection` object does
not assume changes to the database will be automatically committed, instead
requiring in the default case that the `connection.commit()` method is
called in order to commit changes to the database. It should be noted that
the DBAPI itself **does not have a begin() method at all**.  All
Python DBAPIs implement “autobegin” as the primary means of managing
transactions, and handle the job of emitting a statement like BEGIN on the
connection when SQL statements are first emitted.
SQLAlchemy’s API is basically re-stating this behavior in terms of higher
level Python objects.

In “commit as you go” style, we can call upon [Connection.commit()](#sqlalchemy.engine.Connection.commit)
and [Connection.rollback()](#sqlalchemy.engine.Connection.rollback) methods freely within an ongoing
sequence of other statements emitted using [Connection.execute()](#sqlalchemy.engine.Connection.execute);
each time the transaction is ended, and a new statement is
emitted, a new transaction begins implicitly:

```
with engine.connect() as connection:
    connection.execute(text("<some statement>"))
    connection.commit()  # commits "some statement"

    # new transaction starts
    connection.execute(text("<some other statement>"))
    connection.rollback()  # rolls back "some other statement"

    # new transaction starts
    connection.execute(text("<a third statement>"))
    connection.commit()  # commits "a third statement"
```

Added in version 2.0: “commit as you go” style is a new feature of
SQLAlchemy 2.0.  It is also available in SQLAlchemy 1.4’s “transitional”
mode when using a “future” style engine.

### Begin Once

The [Connection](#sqlalchemy.engine.Connection) object provides a more explicit transaction
management style known as **begin once**. In contrast to “commit as
you go”, “begin once” allows the start point of the transaction to be
stated explicitly,
and allows that the transaction itself may be framed out as a context manager
block so that the end of the transaction is instead implicit. To use
“begin once”, the [Connection.begin()](#sqlalchemy.engine.Connection.begin) method is used, which returns a
[Transaction](#sqlalchemy.engine.Transaction) object which represents the DBAPI transaction.
This object also supports explicit management via its own
[Transaction.commit()](#sqlalchemy.engine.Transaction.commit) and [Transaction.rollback()](#sqlalchemy.engine.Transaction.rollback)
methods, but as a preferred practice also supports the context manager interface,
where it will commit itself when
the block ends normally and emit a rollback if an exception is raised, before
propagating the exception outwards. Below illustrates the form of a “begin
once” block:

```
with engine.connect() as connection:
    with connection.begin():
        connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})
        connection.execute(
            some_other_table.insert(), {"q": 8, "p": "this is some more data"}
        )

    # transaction is committed
```

### Connect and Begin Once from the Engine

A convenient shorthand form for the above “begin once” block is to use
the [Engine.begin()](#sqlalchemy.engine.Engine.begin) method at the level of the originating
[Engine](#sqlalchemy.engine.Engine) object, rather than performing the two separate
steps of [Engine.connect()](#sqlalchemy.engine.Engine.connect) and [Connection.begin()](#sqlalchemy.engine.Connection.begin);
the [Engine.begin()](#sqlalchemy.engine.Engine.begin) method returns a special context manager
that internally maintains both the context manager for the [Connection](#sqlalchemy.engine.Connection)
as well as the context manager for the [Transaction](#sqlalchemy.engine.Transaction) normally
returned by the [Connection.begin()](#sqlalchemy.engine.Connection.begin) method:

```
with engine.begin() as connection:
    connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})
    connection.execute(
        some_other_table.insert(), {"q": 8, "p": "this is some more data"}
    )

# transaction is committed, and Connection is released to the connection
# pool
```

Tip

Within the [Engine.begin()](#sqlalchemy.engine.Engine.begin) block, we can call upon the
[Connection.commit()](#sqlalchemy.engine.Connection.commit) or [Connection.rollback()](#sqlalchemy.engine.Connection.rollback)
methods, which will end the transaction normally demarcated by the block
ahead of time.  However, if we do so, no further SQL operations may be
emitted on the [Connection](#sqlalchemy.engine.Connection) until the block ends:

```
>>> from sqlalchemy import create_engine
>>> e = create_engine("sqlite://", echo=True)
>>> with e.begin() as conn:
...     conn.commit()
...     conn.begin()
2021-11-08 09:49:07,517 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2021-11-08 09:49:07,517 INFO sqlalchemy.engine.Engine COMMIT
Traceback (most recent call last):
...
sqlalchemy.exc.InvalidRequestError: Can't operate on closed transaction inside
context manager.  Please complete the context manager before emitting
further commands.
```

### Mixing Styles

The “commit as you go” and “begin once” styles can be freely mixed within
a single [Engine.connect()](#sqlalchemy.engine.Engine.connect) block, provided that the call to
[Connection.begin()](#sqlalchemy.engine.Connection.begin) does not conflict with the “autobegin”
behavior.  To accomplish this, [Connection.begin()](#sqlalchemy.engine.Connection.begin) should only
be called either before any SQL statements have been emitted, or directly
after a previous call to [Connection.commit()](#sqlalchemy.engine.Connection.commit) or [Connection.rollback()](#sqlalchemy.engine.Connection.rollback):

```
with engine.connect() as connection:
    with connection.begin():
        # run statements in a "begin once" block
        connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})

    # transaction is committed

    # run a new statement outside of a block. The connection
    # autobegins
    connection.execute(
        some_other_table.insert(), {"q": 8, "p": "this is some more data"}
    )

    # commit explicitly
    connection.commit()

    # can use a "begin once" block here
    with connection.begin():
        # run more statements
        connection.execute(...)
```

When developing code that uses “begin once”, the library will raise
[InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) if a transaction was already “autobegun”.

## Setting Transaction Isolation Levels including DBAPI Autocommit

Most DBAPIs support the concept of configurable transaction [isolation](https://docs.sqlalchemy.org/en/20/glossary.html#term-isolation) levels.
These are traditionally the four levels “READ UNCOMMITTED”, “READ COMMITTED”,
“REPEATABLE READ” and “SERIALIZABLE”.  These are usually applied to a
DBAPI connection before it begins a new transaction, noting that most
DBAPIs will begin this transaction implicitly when SQL statements are first
emitted.

DBAPIs that support isolation levels also usually support the concept of true
“autocommit”, which means that the DBAPI connection itself will be placed into
a non-transactional autocommit mode. This usually means that the typical DBAPI
behavior of emitting “BEGIN” to the database automatically no longer occurs,
but it may also include other directives. SQLAlchemy treats the concept of
“autocommit” like any other isolation level; in that it is an isolation level
that loses not only “read committed” but also loses atomicity.

Tip

It is important to note, as will be discussed further in the section below at
[Understanding the DBAPI-Level Autocommit Isolation Level](#dbapi-autocommit-understanding), that “autocommit” isolation level like
any other isolation level does **not** affect the “transactional” behavior of
the [Connection](#sqlalchemy.engine.Connection) object, which continues to call upon DBAPI
`.commit()` and `.rollback()` methods (they just have no net effect under
autocommit), and for which the `.begin()` method assumes the DBAPI will
start a transaction implicitly (which means that SQLAlchemy’s “begin” **does
not change autocommit mode**).

SQLAlchemy dialects should support these isolation levels as well as autocommit
to as great a degree as possible.

### Setting Isolation Level or DBAPI Autocommit for a Connection

For an individual [Connection](#sqlalchemy.engine.Connection) object that’s acquired from
[Engine.connect()](#sqlalchemy.engine.Engine.connect), the isolation level can be set for the duration of
that [Connection](#sqlalchemy.engine.Connection) object using the
[Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options) method. The parameter is known as
[Connection.execution_options.isolation_level](#sqlalchemy.engine.Connection.execution_options.params.isolation_level) and the values
are strings which are typically a subset of the following names:

```
# possible values for Connection.execution_options(isolation_level="<value>")

"AUTOCOMMIT"
"READ COMMITTED"
"READ UNCOMMITTED"
"REPEATABLE READ"
"SERIALIZABLE"
```

Not every DBAPI supports every value; if an unsupported value is used for a
certain backend, an error is raised.

For example, to force REPEATABLE READ on a specific connection, then
begin a transaction:

```
with engine.connect().execution_options(
    isolation_level="REPEATABLE READ"
) as connection:
    with connection.begin():
        connection.execute(text("<statement>"))
```

Tip

The return value of
the [Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options) method is the same
[Connection](#sqlalchemy.engine.Connection) object upon which the method was called,
meaning, it modifies the state of the [Connection](#sqlalchemy.engine.Connection)
object in place.  This is a new behavior as of SQLAlchemy 2.0.
This behavior does not apply to the [Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options)
method; that method still returns a copy of the [Engine](#sqlalchemy.engine.Engine) and
as described below may be used to construct multiple [Engine](#sqlalchemy.engine.Engine)
objects with different execution options, which nonetheless share the same
dialect and connection pool.

Note

The [Connection.execution_options.isolation_level](#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
parameter necessarily does not apply to statement level options, such as
that of [Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options), and will be rejected if
set at this level. This because the option must be set on a DBAPI connection
on a per-transaction basis.

### Setting Isolation Level or DBAPI Autocommit for an Engine

The [Connection.execution_options.isolation_level](#sqlalchemy.engine.Connection.execution_options.params.isolation_level) option may
also be set engine wide, as is often preferable.  This may be
achieved by passing the [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level)
parameter to `create_engine()`:

```
from sqlalchemy import create_engine

eng = create_engine(
    "postgresql://scott:tiger@localhost/test", isolation_level="REPEATABLE READ"
)
```

With the above setting, each new DBAPI connection the moment it’s created will
be set to use a `"REPEATABLE READ"` isolation level setting for all
subsequent operations.

Tip

Prefer to set frequently used isolation levels engine wide as illustrated
above compared to using per-engine or per-connection execution options for
maximum performance.

### Maintaining Multiple Isolation Levels for a Single Engine

The isolation level may also be set per engine, with a potentially greater
level of flexibility but with a small per-connection performance overhead,
using either the [create_engine.execution_options](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.execution_options) parameter to
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) or the [Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options)
method, the latter of which will create a copy of the [Engine](#sqlalchemy.engine.Engine) that
shares the dialect and connection pool of the original engine, but has its own
per-connection isolation level setting:

```
from sqlalchemy import create_engine

eng = create_engine(
    "postgresql+psycopg2://scott:tiger@localhost/test",
    execution_options={"isolation_level": "REPEATABLE READ"},
)
```

With the above setting, the DBAPI connection will be set to use a
`"REPEATABLE READ"` isolation level setting for each new transaction
begun; but the connection as pooled will be reset to the original isolation
level that was present when the connection first occurred.   At the level
of [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine), the end effect is not any different
from using the [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) parameter.

However, an application that frequently chooses to run operations within
different isolation levels may wish to create multiple “sub-engines” of a lead
[Engine](#sqlalchemy.engine.Engine), each of which will be configured to a different
isolation level. One such use case is an application that has operations that
break into “transactional” and “read-only” operations, a separate
[Engine](#sqlalchemy.engine.Engine) that makes use of `"AUTOCOMMIT"` may be separated off
from the main engine:

```
from sqlalchemy import create_engine

eng = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")

autocommit_engine = eng.execution_options(isolation_level="AUTOCOMMIT")
```

Above, the [Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options) method creates a shallow
copy of the original [Engine](#sqlalchemy.engine.Engine).  Both `eng` and
`autocommit_engine` share the same dialect and connection pool.  However, the
“AUTOCOMMIT” mode will be set upon connections when they are acquired from the
`autocommit_engine`.

The isolation level setting, regardless of which one it is, is unconditionally
reverted when a connection is returned to the connection pool.

Note

The execution options approach, whether used engine wide or per connection,
incurs a small performance penalty as isolation level instructions
are sent on connection acquire as well as connection release.   Consider
the engine-wide isolation setting at [Setting Isolation Level or DBAPI Autocommit for an Engine](#dbapi-autocommit-engine) so
that connections are configured at the target isolation level permanently
as they are pooled.

See also

[SQLite Transaction Isolation](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-isolation-level)

[PostgreSQL Transaction Isolation](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-isolation-level)

[MySQL Transaction Isolation](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-isolation-level)

[SQL Server Transaction Isolation](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-isolation-level)

[Oracle Database Transaction Isolation](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracle-isolation-level)

[Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-transaction-isolation) - for the ORM

[Using DBAPI Autocommit Allows for a Readonly Version of Transparent Reconnect](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-execute-retry-autocommit) - a recipe that uses DBAPI autocommit
to transparently reconnect to the database for read-only operations

### Understanding the DBAPI-Level Autocommit Isolation Level

In the parent section, we introduced the concept of the
[Connection.execution_options.isolation_level](#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
parameter and how it can be used to set database isolation levels, including
DBAPI-level “autocommit” which is treated by SQLAlchemy as another transaction
isolation level.   In this section we will attempt to clarify the implications
of this approach.

If we wanted to check out a [Connection](#sqlalchemy.engine.Connection) object and use it
“autocommit” mode, we would proceed as follows:

```
with engine.connect() as connection:
    connection.execution_options(isolation_level="AUTOCOMMIT")
    connection.execute(text("<statement>"))
    connection.execute(text("<statement>"))
```

Above illustrates normal usage of “DBAPI autocommit” mode.   There is no
need to make use of methods such as [Connection.begin()](#sqlalchemy.engine.Connection.begin)
or [Connection.commit()](#sqlalchemy.engine.Connection.commit), as all statements are committed
to the database immediately.  When the block ends, the [Connection](#sqlalchemy.engine.Connection)
object will revert the “autocommit” isolation level, and the DBAPI connection
is released to the connection pool where the DBAPI `connection.rollback()`
method will normally be invoked, but as the above statements were already
committed, this rollback has no change on the state of the database.

It is important to note that “autocommit” mode
persists even when the [Connection.begin()](#sqlalchemy.engine.Connection.begin) method is called;
the DBAPI will not emit any BEGIN to the database.   When
[Connection.commit()](#sqlalchemy.engine.Connection.commit) is called, the DBAPI may still emit the
“COMMIT” instruction, but this is a no-op at the database level.  This usage is also
not an error scenario, as it is expected that the “autocommit” isolation level
may be applied to code that otherwise was written assuming a transactional context;
the “isolation level” is, after all, a configurational detail of the transaction
itself just like any other isolation level.

In the example below, statements remain
**autocommitting** regardless of SQLAlchemy-level transaction blocks:

```
with engine.connect() as connection:
    connection = connection.execution_options(isolation_level="AUTOCOMMIT")

    # this begin() does not affect the DBAPI connection, isolation stays at AUTOCOMMIT
    with connection.begin() as trans:
        connection.execute(text("<statement>"))
        connection.execute(text("<statement>"))
```

When we run a block like the above with logging turned on, the logging
will attempt to indicate that while a DBAPI level `.commit()` is called,
it probably will have no effect due to autocommit mode:

```
INFO sqlalchemy.engine.Engine BEGIN (implicit)
...
INFO sqlalchemy.engine.Engine COMMIT using DBAPI connection.commit(), has no effect due to autocommit mode
```

At the same time, even though we are using “DBAPI autocommit”, SQLAlchemy’s
transactional semantics, that is, the in-Python behavior of [Connection.begin()](#sqlalchemy.engine.Connection.begin)
as well as the behavior of “autobegin”, **remain in place, even though these
don’t impact the DBAPI connection itself**.  To illustrate, the code
below will raise an error, as [Connection.begin()](#sqlalchemy.engine.Connection.begin) is being
called after autobegin has already occurred:

```
with engine.connect() as connection:
    connection = connection.execution_options(isolation_level="AUTOCOMMIT")

    # "transaction" is autobegin (but has no effect due to autocommit)
    connection.execute(text("<statement>"))

    # this will raise; "transaction" is already begun
    with connection.begin() as trans:
        connection.execute(text("<statement>"))
```

The above example also demonstrates the same theme that the “autocommit”
isolation level is a configurational detail of the underlying database
transaction, and is independent of the begin/commit behavior of the SQLAlchemy
Connection object. The “autocommit” mode will not interact with
[Connection.begin()](#sqlalchemy.engine.Connection.begin) in any way and the [Connection](#sqlalchemy.engine.Connection)
does not consult this status when performing its own state changes with regards
to the transaction (with the exception of suggesting within engine logging that
these blocks are not actually committing). The rationale for this design is to
maintain a completely consistent usage pattern with the
[Connection](#sqlalchemy.engine.Connection) where DBAPI-autocommit mode can be changed
independently without indicating any code changes elsewhere.

#### Fully preventing ROLLBACK calls under autocommit

Added in version 2.0.43.

A common use case is to use AUTOCOMMIT isolation mode to improve performance,
and this is a particularly common practice on MySQL / MariaDB databases.
When seeking this pattern, it should be preferred to set AUTOCOMMIT engine
wide using the [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) so that pooled
connections are permanently set in autocommit mode.   The SQLAlchemy connection
pool as well as the [Connection](#sqlalchemy.engine.Connection) will still seek to invoke the DBAPI
`.rollback()` method upon connection [release](https://docs.sqlalchemy.org/en/20/glossary.html#term-release), as their behavior
remains agnostic of the isolation level that’s configured on the connection.
As this rollback still incurs a network round trip under most if not all
DBAPI drivers, this additional network trip may be disabled using the
[create_engine.skip_autocommit_rollback](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.skip_autocommit_rollback) parameter, which will
apply a rule at the basemost portion of the dialect that invokes DBAPI
`.rollback()` to first check if the connection is configured in autocommit,
using a method of detection that does not itself incur network overhead:

```
autocommit_engine = create_engine(
    "mysql+mysqldb://scott:tiger@mysql80/test",
    skip_autocommit_rollback=True,
    isolation_level="AUTOCOMMIT",
)
```

When DBAPI connections are returned to the pool by the [Connection](#sqlalchemy.engine.Connection),
whether the [Connection](#sqlalchemy.engine.Connection) or the pool attempts to reset the
“transaction”, the underlying DBAPI `.rollback()` method will be blocked
based on a positive test of “autocommit”.

If the dialect in use does not support a no-network means of detecting
autocommit, the dialect will raise `NotImplementedError` when a connection
release is attempted.

#### Changing Between Isolation Levels

TL;DR;

prefer to use individual [Connection](#sqlalchemy.engine.Connection) objects
each with just one isolation level, rather than switching isolation on a single
[Connection](#sqlalchemy.engine.Connection).  The code will be easier to read and less
error prone.

Isolation level settings, including autocommit mode, are reset automatically
when the connection is released back to the connection pool. Therefore it is
preferable to avoid trying to switch isolation levels on a single
[Connection](#sqlalchemy.engine.Connection) object as this leads to excess verbosity.

To illustrate how to use “autocommit” in an ad-hoc mode within the scope of a
single [Connection](#sqlalchemy.engine.Connection) checkout, the
[Connection.execution_options.isolation_level](#sqlalchemy.engine.Connection.execution_options.params.isolation_level) parameter
must be re-applied with the previous isolation level.
The previous section illustrated an attempt to call [Connection.begin()](#sqlalchemy.engine.Connection.begin)
in order to start a transaction while autocommit was taking place; we can
rewrite that example to actually do so by first reverting the isolation level
before we call upon [Connection.begin()](#sqlalchemy.engine.Connection.begin):

```
# if we wanted to flip autocommit on and off on a single connection/
# which... we usually don't.

with engine.connect() as connection:
    connection.execution_options(isolation_level="AUTOCOMMIT")

    # run statement(s) in autocommit mode
    connection.execute(text("<statement>"))

    # "commit" the autobegun "transaction"
    connection.commit()

    # switch to default isolation level
    connection.execution_options(isolation_level=connection.default_isolation_level)

    # use a begin block
    with connection.begin() as trans:
        connection.execute(text("<statement>"))
```

Above, to manually revert the isolation level we made use of
[Connection.default_isolation_level](#sqlalchemy.engine.Connection.default_isolation_level) to restore the default
isolation level (assuming that’s what we want here). However, it’s
probably a better idea to work with the architecture of of the
[Connection](#sqlalchemy.engine.Connection) which already handles resetting of isolation level
automatically upon checkin. The **preferred** way to write the above is to
use two blocks

```
# use an autocommit block
with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
    # run statement in autocommit mode
    connection.execute(text("<statement>"))

# use a regular block
with engine.begin() as connection:
    connection.execute(text("<statement>"))
```

To sum up:

1. “DBAPI level autocommit” isolation level is entirely independent of the
  [Connection](#sqlalchemy.engine.Connection) object’s notion of “begin” and “commit”
2. use individual [Connection](#sqlalchemy.engine.Connection) checkouts per isolation level.
  Avoid trying to change back and forth between “autocommit” on a single
  connection checkout; let the engine do the work of restoring default
  isolation levels

## Using Server Side Cursors (a.k.a. stream results)

Some backends feature explicit support for the concept of “server side cursors”
versus “client side cursors”.  A client side cursor here means that the
database driver fully fetches all rows from a result set into memory before
returning from a statement execution.  Drivers such as those of PostgreSQL and
MySQL/MariaDB generally use client side cursors by default.  A server side
cursor, by contrast, indicates that result rows remain pending within the
database server’s state as result rows are consumed by the client.  The drivers
for Oracle Database generally use a “server side” model, for example, and the
SQLite dialect, while not using a real “client / server” architecture, still
uses an unbuffered result fetching approach that will leave result rows outside
of process memory before they are consumed.

What we really mean is “buffered” vs. “unbuffered” results

Server side cursors also imply a wider set of features with relational
databases, such as the ability to “scroll” a cursor forwards and backwards.
SQLAlchemy does not include any explicit support for these behaviors; within
SQLAlchemy itself, the general term “server side cursors” should be considered
to mean “unbuffered results” and “client side cursors” means “result rows
are buffered into memory before the first row is returned”.   To work with
a richer “server side cursor” featureset specific to a certain DBAPI driver,
see the section [Working with the DBAPI cursor directly](#dbapi-connections-cursor).

From this basic architecture it follows that a “server side cursor” is more
memory efficient when fetching very large result sets, while at the same time
may introduce more complexity in the client/server communication process
and be less efficient for small result sets (typically less than 10000 rows).

For those dialects that have conditional support for buffered or unbuffered
results, there are usually caveats to the use of the “unbuffered”, or server
side cursor mode.   When using the psycopg2 dialect for example, an error is
raised if a server side cursor is used with any kind of DML or DDL statement.
When using MySQL drivers with a server side cursor, the DBAPI connection is in
a more fragile state and does not recover as gracefully from error conditions
nor will it allow a rollback to proceed until the cursor is fully closed.

For this reason, SQLAlchemy’s dialects will always default to the less error
prone version of a cursor, which means for PostgreSQL and MySQL dialects
it defaults to a buffered, “client side” cursor where the full set of results
is pulled into memory before any fetch methods are called from the cursor.
This mode of operation is appropriate in the **vast majority** of cases;
unbuffered cursors are not generally useful except in the uncommon case
of an application fetching a very large number of rows in chunks, where
the processing of these rows can be complete before more rows are fetched.

For database drivers that provide client and server side cursor options,
the [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
and [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) execution
options provide access to “server side cursors” on a per-[Connection](#sqlalchemy.engine.Connection)
or per-statement basis.    Similar options exist when using an ORM
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) as well.

### Streaming with a fixed buffer via yield_per

As individual row-fetch operations with fully unbuffered server side cursors
are typically more expensive than fetching batches of rows at once, The
[Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) execution option
configures a [Connection](#sqlalchemy.engine.Connection) or statement to make use of
server-side cursors as are available, while at the same time configuring a
fixed-size buffer of rows that will retrieve rows from the server in batches as
they are consumed. This parameter may be to a positive integer value using the
[Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options) method on
[Connection](#sqlalchemy.engine.Connection) or on a statement using the
[Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options) method.

Added in version 1.4.40: [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) as a
Core-only option is new as of SQLAlchemy 1.4.40; for prior 1.4 versions,
use [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
directly in combination with [Result.yield_per()](#sqlalchemy.engine.Result.yield_per).

Using this option is equivalent to manually setting the
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results) option,
described in the next section, and then invoking the
[Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method on the [Result](#sqlalchemy.engine.Result)
object with the given integer value.   In both cases, the effect this
combination has includes:

- server side cursors mode is selected for the given backend, if available
  and not already the default behavior for that backend
- as result rows are fetched, they will be buffered in batches, where the
  size of each batch up until the last batch will be equal to the integer
  argument passed to the
  [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) option or the
  [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method; the last batch is then sized against
  the remaining rows fewer than this size
- The default partition size used by the [Result.partitions()](#sqlalchemy.engine.Result.partitions)
  method, if used, will be made equal to this integer size as well.

These three behaviors are illustrated in the example below:

```
with engine.connect() as conn:
    with conn.execution_options(yield_per=100).execute(
        text("select * from table")
    ) as result:
        for partition in result.partitions():
            # partition is an iterable that will be at most 100 items
            for row in partition:
                print(f"{row}")
```

The above example illustrates the combination of `yield_per=100` along
with using the [Result.partitions()](#sqlalchemy.engine.Result.partitions) method to run processing
on rows in batches that match the size fetched from the server.   The
use of [Result.partitions()](#sqlalchemy.engine.Result.partitions) is optional, and if the
[Result](#sqlalchemy.engine.Result) is iterated directly, a new batch of rows will be
buffered for each 100 rows fetched.    Calling a method such as
[Result.all()](#sqlalchemy.engine.Result.all) should **not** be used, as this will fully
fetch all remaining rows at once and defeat the purpose of using `yield_per`.

Tip

The [Result](#sqlalchemy.engine.Result) object may be used as a context manager as illustrated
above.  When iterating with a server-side cursor, this is the best way to
ensure the [Result](#sqlalchemy.engine.Result) object is closed, even if exceptions are
raised within the iteration process.

The [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) option
is portable to the ORM as well, used by a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to fetch
ORM objects, where it also limits the amount of ORM objects generated at once.
See the section [Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
for further background on using
[Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) with the ORM.

Added in version 1.4.40: Added
[Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
as a Core level execution option to conveniently set streaming results,
buffer size, and partition size all at once in a manner that is transferable
to that of the ORM’s similar use case.

### Streaming with a dynamically growing buffer using stream_results

To enable server side cursors without a specific partition size, the
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results) option may be
used, which like [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) may
be called on the [Connection](#sqlalchemy.engine.Connection) object or the statement object.

When a [Result](#sqlalchemy.engine.Result) object delivered using the
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results) option
is iterated directly, rows are fetched internally
using a default buffering scheme that buffers first a small set of rows,
then a larger and larger buffer on each fetch up to a pre-configured limit
of 1000 rows.   The maximum size of this buffer can be affected using the
[Connection.execution_options.max_row_buffer](#sqlalchemy.engine.Connection.execution_options.params.max_row_buffer) execution option:

```
with engine.connect() as conn:
    with conn.execution_options(stream_results=True, max_row_buffer=100).execute(
        text("select * from table")
    ) as result:
        for row in result:
            print(f"{row}")
```

While the [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
option may be combined with use of the [Result.partitions()](#sqlalchemy.engine.Result.partitions)
method, a specific partition size should be passed to
[Result.partitions()](#sqlalchemy.engine.Result.partitions) so that the entire result is not fetched.
It is usually more straightforward to use the
[Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) option when setting
up to use the [Result.partitions()](#sqlalchemy.engine.Result.partitions) method.

See also

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Result.partitions()](#sqlalchemy.engine.Result.partitions)

[Result.yield_per()](#sqlalchemy.engine.Result.yield_per)

## Translation of Schema Names

To support multi-tenancy applications that distribute common sets of tables
into multiple schemas, the
[Connection.execution_options.schema_translate_map](#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map)
execution option may be used to repurpose a set of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects
to render under different schema names without any changes.

Given a table:

```
user_table = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)
```

The “schema” of this [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) as defined by the
[Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) attribute is `None`.  The
[Connection.execution_options.schema_translate_map](#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map) can specify
that all [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects with a schema of `None` would instead
render the schema as `user_schema_one`:

```
connection = engine.connect().execution_options(
    schema_translate_map={None: "user_schema_one"}
)

result = connection.execute(user_table.select())
```

The above code will invoke SQL on the database of the form:

```
SELECT user_schema_one.user.id, user_schema_one.user.name FROM
user_schema_one.user
```

That is, the schema name is substituted with our translated name.  The
map can specify any number of target->destination schemas:

```
connection = engine.connect().execution_options(
    schema_translate_map={
        None: "user_schema_one",  # no schema name -> "user_schema_one"
        "special": "special_schema",  # schema="special" becomes "special_schema"
        "public": None,  # Table objects with schema="public" will render with no schema
    }
)
```

The [Connection.execution_options.schema_translate_map](#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map) parameter
affects all DDL and SQL constructs generated from the SQL expression language,
as derived from the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) objects.
It does **not** impact literal string SQL used via the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
construct nor via plain strings passed to [Connection.execute()](#sqlalchemy.engine.Connection.execute).

The feature takes effect **only** in those cases where the name of the
schema is derived directly from that of a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence);
it does not impact methods where a string schema name is passed directly.
By this pattern, it takes effect within the “can create” / “can drop” checks
performed by methods such as [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) or
[MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all) are called, and it takes effect when
using table reflection given a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.  However it does
**not** affect the operations present on the [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) object,
as the schema name is passed to these methods explicitly.

Tip

To use the schema translation feature with the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
set this option at the level of the [Engine](#sqlalchemy.engine.Engine), then pass that engine
to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) uses a new
[Connection](#sqlalchemy.engine.Connection) for each transaction:

```
schema_engine = engine.execution_options(schema_translate_map={...})

session = Session(schema_engine)

...
```

Warning

When using the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) without extensions, the schema
translate feature is only supported as
**a single schema translate map per Session**.   It will **not work** if
different schema translate maps are given on a per-statement basis, as
the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) does not take current schema translate
values into account for individual objects.

To use a single [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with multiple `schema_translate_map`
configurations, the [Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html) extension may
be used.  See the example at [Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-sharding).

## SQL Compilation Caching

Added in version 1.4: SQLAlchemy now has a transparent query caching system
that substantially lowers the Python computational overhead involved in
converting SQL statement constructs into SQL strings across both
Core and ORM.   See the introduction at [Transparent SQL Compilation Caching added to All DQL, DML Statements in Core, ORM](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-4639).

SQLAlchemy includes a comprehensive caching system for the SQL compiler as well
as its ORM variants.   This caching system is transparent within the
[Engine](#sqlalchemy.engine.Engine) and provides that the SQL compilation process for a given Core
or ORM SQL statement, as well as related computations which assemble
result-fetching mechanics for that statement, will only occur once for that
statement object and all others with the identical
structure, for the duration that the particular structure remains within the
engine’s “compiled cache”. By “statement objects that have the identical
structure”, this generally corresponds to a SQL statement that is
constructed within a function and is built each time that function runs:

```
def run_my_statement(connection, parameter):
    stmt = select(table)
    stmt = stmt.where(table.c.col == parameter)
    stmt = stmt.order_by(table.c.id)
    return connection.execute(stmt)
```

The above statement will generate SQL resembling
`SELECT id, col FROM table WHERE col = :col ORDER BY id`, noting that
while the value of `parameter` is a plain Python object such as a string
or an integer, the string SQL form of the statement does not include this
value as it uses bound parameters.  Subsequent invocations of the above
`run_my_statement()` function will use a cached compilation construct
within the scope of the `connection.execute()` call for enhanced performance.

Note

it is important to note that the SQL compilation cache is caching
the **SQL string that is passed to the database only**, and **not the data**
returned by a query.   It is in no way a data cache and does not
impact the results returned for a particular SQL statement nor does it
imply any memory use linked to fetching of result rows.

While SQLAlchemy has had a rudimentary statement cache since the early 1.x
series, and additionally has featured the “Baked Query” extension for the ORM,
both of these systems required a high degree of special API use in order for
the cache to be effective.  The new cache as of 1.4 is instead completely
automatic and requires no change in programming style to be effective.

The cache is automatically used without any configurational changes and no
special steps are needed in order to enable it. The following sections
detail the configuration and advanced usage patterns for the cache.

### Configuration

The cache itself is a dictionary-like object called an `LRUCache`, which is
an internal SQLAlchemy dictionary subclass that tracks the usage of particular
keys and features a periodic “pruning” step which removes the least recently
used items when the size of the cache reaches a certain threshold.  The size
of this cache defaults to 500 and may be configured using the
[create_engine.query_cache_size](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.query_cache_size) parameter:

```
engine = create_engine(
    "postgresql+psycopg2://scott:tiger@localhost/test", query_cache_size=1200
)
```

The size of the cache can grow to be a factor of 150% of the size given, before
it’s pruned back down to the target size.  A cache of size 1200 above can therefore
grow to be 1800 elements in size at which point it will be pruned to 1200.

The sizing of the cache is based on a single entry per unique SQL statement rendered,
per engine.   SQL statements generated from both the Core and the ORM are
treated equally.  DDL statements will usually not be cached.  In order to determine
what the cache is doing, engine logging will include details about the
cache’s behavior, described in the next section.

### Estimating Cache Performance Using Logging

The above cache size of 1200 is actually fairly large.   For small applications,
a size of 100 is likely sufficient.  To estimate the optimal size of the cache,
assuming enough memory is present on the target host, the size of the cache
should be based on the number of unique SQL strings that may be rendered for the
target engine in use.    The most expedient way to see this is to use
SQL echoing, which is most directly enabled by using the
[create_engine.echo](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo) flag, or by using Python logging; see the
section [Configuring Logging](https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging) for background on logging configuration.

As an example, we will examine the logging produced by the following program:

```
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

Base = declarative_base()

class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    bs = relationship("B")

class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id = Column(ForeignKey("a.id"))
    data = Column(String)

e = create_engine("sqlite://", echo=True)
Base.metadata.create_all(e)

s = Session(e)

s.add_all([A(bs=[B(), B(), B()]), A(bs=[B(), B(), B()]), A(bs=[B(), B(), B()])])
s.commit()

for a_rec in s.scalars(select(A)):
    print(a_rec.bs)
```

When run, each SQL statement that’s logged will include a bracketed
cache statistics badge to the left of the parameters passed.   The four
types of message we may see are summarized as follows:

- `[raw sql]` - the driver or the end-user emitted raw SQL using
  [Connection.exec_driver_sql()](#sqlalchemy.engine.Connection.exec_driver_sql) - caching does not apply
- `[no key]` - the statement object is a DDL statement that is not cached, or
  the statement object contains uncacheable elements such as user-defined
  constructs or arbitrarily large VALUES clauses.
- `[generated in Xs]` - the statement was a **cache miss** and had to be
  compiled, then stored in the cache.  it took X seconds to produce the
  compiled construct.  The number X will be in the small fractional seconds.
- `[cached since Xs ago]` - the statement was a **cache hit** and did not
  have to be recompiled.  The statement has been stored in the cache since
  X seconds ago.  The number X will be proportional to how long the application
  has been running and how long the statement has been cached, so for example
  would be 86400 for a 24 hour period.

Each badge is described in more detail below.

The first statements we see for the above program will be the SQLite dialect
checking for the existence of the “a” and “b” tables:

```
INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("a")
INFO sqlalchemy.engine.Engine [raw sql] ()
INFO sqlalchemy.engine.Engine PRAGMA main.table_info("b")
INFO sqlalchemy.engine.Engine [raw sql] ()
```

For the above two SQLite PRAGMA statements, the badge reads `[raw sql]`,
which indicates the driver is sending a Python string directly to the
database using [Connection.exec_driver_sql()](#sqlalchemy.engine.Connection.exec_driver_sql).  Caching does not apply
to such statements because they already exist in string form, and there
is nothing known about what kinds of result rows will be returned since
SQLAlchemy does not parse SQL strings ahead of time.

The next statements we see are the CREATE TABLE statements:

```
INFO sqlalchemy.engine.Engine
CREATE TABLE a (
  id INTEGER NOT NULL,
  data VARCHAR,
  PRIMARY KEY (id)
)

INFO sqlalchemy.engine.Engine [no key 0.00007s] ()
INFO sqlalchemy.engine.Engine
CREATE TABLE b (
  id INTEGER NOT NULL,
  a_id INTEGER,
  data VARCHAR,
  PRIMARY KEY (id),
  FOREIGN KEY(a_id) REFERENCES a (id)
)

INFO sqlalchemy.engine.Engine [no key 0.00006s] ()
```

For each of these statements, the badge reads `[no key 0.00006s]`.  This
indicates that these two particular statements, caching did not occur because
the DDL-oriented [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable) construct did not produce a
cache key.  DDL constructs generally do not participate in caching because
they are not typically subject to being repeated a second time and DDL
is also a database configurational step where performance is not as critical.

The `[no key]` badge is important for one other reason, as it can be produced
for SQL statements that are cacheable except for some particular sub-construct
that is not currently cacheable.   Examples of this include custom user-defined
SQL elements that don’t define caching parameters, as well as some constructs
that generate arbitrarily long and non-reproducible SQL strings, the main
examples being the [Values](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values) construct as well as when using “multivalued
inserts” with the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method.

So far our cache is still empty.  The next statements will be cached however,
a segment looks like:

```
INFO sqlalchemy.engine.Engine INSERT INTO a (data) VALUES (?)
INFO sqlalchemy.engine.Engine [generated in 0.00011s] (None,)
INFO sqlalchemy.engine.Engine INSERT INTO a (data) VALUES (?)
INFO sqlalchemy.engine.Engine [cached since 0.0003533s ago] (None,)
INFO sqlalchemy.engine.Engine INSERT INTO a (data) VALUES (?)
INFO sqlalchemy.engine.Engine [cached since 0.0005326s ago] (None,)
INFO sqlalchemy.engine.Engine INSERT INTO b (a_id, data) VALUES (?, ?)
INFO sqlalchemy.engine.Engine [generated in 0.00010s] (1, None)
INFO sqlalchemy.engine.Engine INSERT INTO b (a_id, data) VALUES (?, ?)
INFO sqlalchemy.engine.Engine [cached since 0.0003232s ago] (1, None)
INFO sqlalchemy.engine.Engine INSERT INTO b (a_id, data) VALUES (?, ?)
INFO sqlalchemy.engine.Engine [cached since 0.0004887s ago] (1, None)
```

Above, we see essentially two unique SQL strings; `"INSERT INTO a (data) VALUES (?)"`
and `"INSERT INTO b (a_id, data) VALUES (?, ?)"`.  Since SQLAlchemy uses
bound parameters for all literal values, even though these statements are
repeated many times for different objects, because the parameters are separate,
the actual SQL string stays the same.

Note

the above two statements are generated by the ORM unit of work
process, and in fact will be caching these in a separate cache that is
local to each mapper.  However the mechanics and terminology are the same.
The section [Disabling or using an alternate dictionary to cache some (or all) statements](#engine-compiled-cache) below will describe how user-facing
code can also use an alternate caching container on a per-statement basis.

The caching badge we see for the first occurrence of each of these two
statements is `[generated in 0.00011s]`. This indicates that the statement
was **not in the cache, was compiled into a String in .00011s and was then
cached**.   When we see the `[generated]` badge, we know that this means
there was a **cache miss**.  This is to be expected for the first occurrence of
a particular statement.  However, if lots of new `[generated]` badges are
observed for a long-running application that is generally using the same series
of SQL statements over and over, this may be a sign that the
[create_engine.query_cache_size](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.query_cache_size) parameter is too small.  When a
statement that was cached is then evicted from the cache due to the LRU
cache pruning lesser used items, it will display the `[generated]` badge
when it is next used.

The caching badge that we then see for the subsequent occurrences of each of
these two statements looks like `[cached since 0.0003533s ago]`.  This
indicates that the statement **was found in the cache, and was originally
placed into the cache .0003533 seconds ago**.   It is important to note that
while the `[generated]` and `[cached since]` badges refer to a number of
seconds, they mean different things; in the case of `[generated]`, the number
is a rough timing of how long it took to compile the statement, and will be an
extremely small amount of time.   In the case of `[cached since]`, this is
the total time that a statement has been present in the cache.  For an
application that’s been running for six hours, this number may read `[cached
since 21600 seconds ago]`, and that’s a good thing.    Seeing high numbers for
“cached since” is an indication that these statements have not been subject to
cache misses for a long time.  Statements that frequently have a low number of
“cached since” even if the application has been running a long time may
indicate these statements are too frequently subject to cache misses, and that
the
[create_engine.query_cache_size](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.query_cache_size) may need to be increased.

Our example program then performs some SELECTs where we can see the same
pattern of “generated” then “cached”, for the SELECT of the “a” table as well
as for subsequent lazy loads of the “b” table:

```
INFO sqlalchemy.engine.Engine SELECT a.id AS a_id, a.data AS a_data
FROM a
INFO sqlalchemy.engine.Engine [generated in 0.00009s] ()
INFO sqlalchemy.engine.Engine SELECT b.id AS b_id, b.a_id AS b_a_id, b.data AS b_data
FROM b
WHERE ? = b.a_id
INFO sqlalchemy.engine.Engine [generated in 0.00010s] (1,)
INFO sqlalchemy.engine.Engine SELECT b.id AS b_id, b.a_id AS b_a_id, b.data AS b_data
FROM b
WHERE ? = b.a_id
INFO sqlalchemy.engine.Engine [cached since 0.0005922s ago] (2,)
INFO sqlalchemy.engine.Engine SELECT b.id AS b_id, b.a_id AS b_a_id, b.data AS b_data
FROM b
WHERE ? = b.a_id
```

From our above program, a full run shows a total of four distinct SQL strings
being cached.   Which indicates a cache size of **four** would be sufficient.   This is
obviously an extremely small size, and the default size of 500 is fine to be left
at its default.

### How much memory does the cache use?

The previous section detailed some techniques to check if the
[create_engine.query_cache_size](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.query_cache_size) needs to be bigger.   How do we know
if the cache is not too large?   The reason we may want to set
[create_engine.query_cache_size](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.query_cache_size) to not be higher than a certain
number would be because we have an application that may make use of a very large
number of different statements, such as an application that is building queries
on the fly from a search UX, and we don’t want our host to run out of memory
if for example, a hundred thousand different queries were run in the past 24 hours
and they were all cached.

It is extremely difficult to measure how much memory is occupied by Python
data structures, however using a process to measure growth in memory via `top` as a
successive series of 250 new statements are added to the cache suggest a
moderate Core statement takes up about 12K while a small ORM statement takes about
20K, including result-fetching structures which for the ORM will be much greater.

### Disabling or using an alternate dictionary to cache some (or all) statements

The internal cache used is known as `LRUCache`, but this is mostly just
a dictionary.  Any dictionary may be used as a cache for any series of
statements by using the [Connection.execution_options.compiled_cache](#sqlalchemy.engine.Connection.execution_options.params.compiled_cache)
option as an execution option.  Execution options may be set on a statement,
on an [Engine](#sqlalchemy.engine.Engine) or [Connection](#sqlalchemy.engine.Connection), as well as
when using the ORM [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method for SQLAlchemy-2.0
style invocations.   For example, to run a series of SQL statements and have
them cached in a particular dictionary:

```
my_cache = {}
with engine.connect().execution_options(compiled_cache=my_cache) as conn:
    conn.execute(table.select())
```

The SQLAlchemy ORM uses the above technique to hold onto per-mapper caches
within the unit of work “flush” process that are separate from the default
cache configured on the [Engine](#sqlalchemy.engine.Engine), as well as for some
relationship loader queries.

The cache can also be disabled with this argument by sending a value of
`None`:

```
# disable caching for this connection
with engine.connect().execution_options(compiled_cache=None) as conn:
    conn.execute(table.select())
```

### Caching for Third Party Dialects

The caching feature requires that the dialect’s compiler produces SQL
strings that are safe to reuse for many statement invocations, given
a particular cache key that is keyed to that SQL string.  This means
that any literal values in a statement, such as the LIMIT/OFFSET values for
a SELECT, can not be hardcoded in the dialect’s compilation scheme, as
the compiled string will not be reusable.   SQLAlchemy supports rendered
bound parameters using the [BindParameter.render_literal_execute()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter.render_literal_execute)
method which can be applied to the existing `Select._limit_clause` and
`Select._offset_clause` attributes by a custom compiler, which
are illustrated later in this section.

As there are many third party dialects, many of which may be generating literal
values from SQL statements without the benefit of the newer “literal execute”
feature, SQLAlchemy as of version 1.4.5 has added an attribute to dialects
known as [Dialect.supports_statement_cache](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.supports_statement_cache). This attribute is
checked at runtime for its presence directly on a particular dialect’s class,
even if it’s already present on a superclass, so that even a third party
dialect that subclasses an existing cacheable SQLAlchemy dialect such as
`sqlalchemy.dialects.postgresql.PGDialect` must still explicitly include this
attribute for caching to be enabled. The attribute should **only** be enabled
once the dialect has been altered as needed and tested for reusability of
compiled SQL statements with differing parameters.

For all third party dialects that don’t support this attribute, the logging for
such a dialect will indicate `dialect does not support caching`.

When a dialect has been tested against caching, and in particular the SQL
compiler has been updated to not render any literal LIMIT / OFFSET within
a SQL string directly, dialect authors can apply the attribute as follows:

```
from sqlalchemy.engine.default import DefaultDialect

class MyDialect(DefaultDialect):
    supports_statement_cache = True
```

The flag needs to be applied to all subclasses of the dialect as well:

```
class MyDBAPIForMyDialect(MyDialect):
    supports_statement_cache = True
```

Added in version 1.4.5: Added the [Dialect.supports_statement_cache](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.supports_statement_cache) attribute.

The typical case for dialect modification follows.

#### Example: Rendering LIMIT / OFFSET with post compile parameters

As an example, suppose a dialect overrides the `SQLCompiler.limit_clause()`
method, which produces the “LIMIT / OFFSET” clause for a SQL statement,
like this:

```
# pre 1.4 style code
def limit_clause(self, select, **kw):
    text = ""
    if select._limit is not None:
        text += " \n LIMIT %d" % (select._limit,)
    if select._offset is not None:
        text += " \n OFFSET %d" % (select._offset,)
    return text
```

The above routine renders the `Select._limit` and
`Select._offset` integer values as literal integers embedded in the SQL
statement. This is a common requirement for databases that do not support using
a bound parameter within the LIMIT/OFFSET clauses of a SELECT statement.
However, rendering the integer value within the initial compilation stage is
directly **incompatible** with caching as the limit and offset integer values
of a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object are not part of the cache key, so that many
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) statements with different limit/offset values would not render
with the correct value.

The correction for the above code is to move the literal integer into
SQLAlchemy’s [post-compile](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-4808) facility, which will render the
literal integer outside of the initial compilation stage, but instead at
execution time before the statement is sent to the DBAPI.  This is accessed
within the compilation stage using the [BindParameter.render_literal_execute()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter.render_literal_execute)
method, in conjunction with using the `Select._limit_clause` and
`Select._offset_clause` attributes, which represent the LIMIT/OFFSET
as a complete SQL expression, as follows:

```
# 1.4 cache-compatible code
def limit_clause(self, select, **kw):
    text = ""

    limit_clause = select._limit_clause
    offset_clause = select._offset_clause

    if select._simple_int_clause(limit_clause):
        text += " \n LIMIT %s" % (
            self.process(limit_clause.render_literal_execute(), **kw)
        )
    elif limit_clause is not None:
        # assuming the DB doesn't support SQL expressions for LIMIT.
        # Otherwise render here normally
        raise exc.CompileError(
            "dialect 'mydialect' can only render simple integers for LIMIT"
        )
    if select._simple_int_clause(offset_clause):
        text += " \n OFFSET %s" % (
            self.process(offset_clause.render_literal_execute(), **kw)
        )
    elif offset_clause is not None:
        # assuming the DB doesn't support SQL expressions for OFFSET.
        # Otherwise render here normally
        raise exc.CompileError(
            "dialect 'mydialect' can only render simple integers for OFFSET"
        )

    return text
```

The approach above will generate a compiled SELECT statement that looks like:

```
SELECT x FROM y
LIMIT __[POSTCOMPILE_param_1]
OFFSET __[POSTCOMPILE_param_2]
```

Where above, the `__[POSTCOMPILE_param_1]` and `__[POSTCOMPILE_param_2]`
indicators will be populated with their corresponding integer values at
statement execution time, after the SQL string has been retrieved from the
cache.

After changes like the above have been made as appropriate, the
[Dialect.supports_statement_cache](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.supports_statement_cache) flag should be set to `True`.
It is strongly recommended that third party dialects make use of the
[dialect third party test suite](https://github.com/sqlalchemy/sqlalchemy/blob/main/README.dialects.rst)
which will assert that operations like
SELECTs with LIMIT/OFFSET are correctly rendered and cached.

See also

[Why is my application slow after upgrading to 1.4 and/or 2.x?](https://docs.sqlalchemy.org/en/20/faq/performance.html#faq-new-caching) - in the [Frequently Asked Questions](https://docs.sqlalchemy.org/en/20/faq/index.html) section

### Using Lambdas to add significant speed gains to statement production

Deep Alchemy

This technique is generally non-essential except in very performance
intensive scenarios, and intended for experienced Python programmers.
While fairly straightforward, it involves metaprogramming concepts that are
not appropriate for novice Python developers.  The lambda approach can be
applied to at a later time to existing code with a minimal amount of effort.

Python functions, typically expressed as lambdas, may be used to generate
SQL expressions which are cacheable based on the Python code location of
the lambda function itself as well as the closure variables within the
lambda.   The rationale is to allow caching of not only the SQL string-compiled
form of a SQL expression construct as is SQLAlchemy’s normal behavior when
the lambda system isn’t used, but also the in-Python composition
of the SQL expression construct itself, which also has some degree of
Python overhead.

The lambda SQL expression feature is available as a performance enhancing
feature, and is also optionally used in the [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria)
ORM option in order to provide a generic SQL fragment.

#### Synopsis

Lambda statements are constructed using the [lambda_stmt()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.lambda_stmt) function,
which returns an instance of [StatementLambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement), which is
itself an executable statement construct.    Additional modifiers and criteria
are added to the object using the Python addition operator `+`, or
alternatively the [StatementLambdaElement.add_criteria()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.add_criteria) method which
allows for more options.

It is assumed that the [lambda_stmt()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.lambda_stmt) construct is being invoked
within an enclosing function or method that expects to be used many times
within an application, so that subsequent executions beyond the first one
can take advantage of the compiled SQL being cached.  When the lambda is
constructed inside of an enclosing function in Python it is then subject
to also having closure variables, which are significant to the whole
approach:

```
from sqlalchemy import lambda_stmt

def run_my_statement(connection, parameter):
    stmt = lambda_stmt(lambda: select(table))
    stmt += lambda s: s.where(table.c.col == parameter)
    stmt += lambda s: s.order_by(table.c.id)

    return connection.execute(stmt)

with engine.connect() as conn:
    result = run_my_statement(some_connection, "some parameter")
```

Above, the three `lambda` callables that are used to define the structure
of a SELECT statement are invoked exactly once, and the resulting SQL
string cached in the compilation cache of the engine.   From that point
forward, the `run_my_statement()` function may be invoked any number
of times and the `lambda` callables within it will not be called, only
used as cache keys to retrieve the already-compiled SQL.

Note

It is important to note that there is already SQL caching in place
when the lambda system is not used.   The lambda system only adds an
additional layer of work reduction per SQL statement invoked by caching
the building up of the SQL construct itself and also using a simpler
cache key.

#### Quick Guidelines for Lambdas

Above all, the emphasis within the lambda SQL system is ensuring that there
is never a mismatch between the cache key generated for a lambda and the
SQL string it will produce.   The [LambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.LambdaElement) and related
objects will run and analyze the given lambda in order to calculate how
it should be cached on each run, trying to detect any potential problems.
Basic guidelines include:

- **Any kind of statement is supported** - while it’s expected that
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) constructs are the prime use case for [lambda_stmt()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.lambda_stmt),
  DML statements such as [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) and [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) are
  equally usable:
  ```
  def upd(id_, newname):
      stmt = lambda_stmt(lambda: users.update())
      stmt += lambda s: s.values(name=newname)
      stmt += lambda s: s.where(users.c.id == id_)
      return stmt
  with engine.begin() as conn:
      conn.execute(upd(7, "foo"))
  ```
- **ORM use cases directly supported as well** - the [lambda_stmt()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.lambda_stmt)
  can accommodate ORM functionality completely and used directly with
  [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute):
  ```
  def select_user(session, name):
      stmt = lambda_stmt(lambda: select(User))
      stmt += lambda s: s.where(User.name == name)
      row = session.execute(stmt).first()
      return row
  ```
- **Bound parameters are automatically accommodated** - in contrast to SQLAlchemy’s
  previous “baked query” system, the lambda SQL system accommodates for
  Python literal values which become SQL bound parameters automatically.
  This means that even though a given lambda runs only once, the values that
  become bound parameters are extracted from the **closure** of the lambda
  on every run:
  ```
  >>> def my_stmt(x, y):
  ...     stmt = lambda_stmt(lambda: select(func.max(x, y)))
  ...     return stmt
  >>> engine = create_engine("sqlite://", echo=True)
  >>> with engine.connect() as conn:
  ...     print(conn.scalar(my_stmt(5, 10)))
  ...     print(conn.scalar(my_stmt(12, 8)))
  SELECT max(?, ?) AS max_1
  [generated in 0.00057s] (5, 10)
  10
  SELECT max(?, ?) AS max_1
  [cached since 0.002059s ago] (12, 8)
  12
  ```
  Above, [StatementLambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement) extracted the values of `x`
  and `y` from the **closure** of the lambda that is generated each time
  `my_stmt()` is invoked; these were substituted into the cached SQL
  construct as the values of the parameters.
- **The lambda should ideally produce an identical SQL structure in all cases** -
  Avoid using conditionals or custom callables inside of lambdas that might make
  it produce different SQL based on inputs; if a function might conditionally
  use two different SQL fragments, use two separate lambdas:
  ```
  # **Don't** do this:
  def my_stmt(parameter, thing=False):
      stmt = lambda_stmt(lambda: select(table))
      stmt += lambda s: (
          s.where(table.c.x > parameter) if thing else s.where(table.c.y == parameter)
      )
      return stmt
  # **Do** do this:
  def my_stmt(parameter, thing=False):
      stmt = lambda_stmt(lambda: select(table))
      if thing:
          stmt += lambda s: s.where(table.c.x > parameter)
      else:
          stmt += lambda s: s.where(table.c.y == parameter)
      return stmt
  ```
  There are a variety of failures which can occur if the lambda does not
  produce a consistent SQL construct and some are not trivially detectable
  right now.
- **Don’t use functions inside the lambda to produce bound values** - the
  bound value tracking approach requires that the actual value to be used in
  the SQL statement be locally present in the closure of the lambda.  This is
  not possible if values are generated from other functions, and the
  [LambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.LambdaElement) should normally raise an error if this is
  attempted:
  ```
  >>> def my_stmt(x, y):
  ...     def get_x():
  ...         return x
  ...
  ...     def get_y():
  ...         return y
  ...
  ...     stmt = lambda_stmt(lambda: select(func.max(get_x(), get_y())))
  ...     return stmt
  >>> with engine.connect() as conn:
  ...     print(conn.scalar(my_stmt(5, 10)))
  Traceback (most recent call last):
    # ...
  sqlalchemy.exc.InvalidRequestError: Can't invoke Python callable get_x()
  inside of lambda expression argument at
  <code object <lambda> at 0x7fed15f350e0, file "<stdin>", line 6>;
  lambda SQL constructs should not invoke functions from closure variables
  to produce literal values since the lambda SQL system normally extracts
  bound values without actually invoking the lambda or any functions within it.
  ```
  Above, the use of `get_x()` and `get_y()`, if they are necessary, should
  occur **outside** of the lambda and assigned to a local closure variable:
  ```
  >>> def my_stmt(x, y):
  ...     def get_x():
  ...         return x
  ...
  ...     def get_y():
  ...         return y
  ...
  ...     x_param, y_param = get_x(), get_y()
  ...     stmt = lambda_stmt(lambda: select(func.max(x_param, y_param)))
  ...     return stmt
  ```
- **Avoid referring to non-SQL constructs inside of lambdas as they are not
  cacheable by default** - this issue refers to how the [LambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.LambdaElement)
  creates a cache key from other closure variables within the statement.  In order
  to provide the best guarantee of an accurate cache key, all objects located
  in the closure of the lambda are considered to be significant, and none
  will be assumed to be appropriate for a cache key by default.
  So the following example will also raise a rather detailed error message:
  ```
  >>> class Foo:
  ...     def __init__(self, x, y):
  ...         self.x = x
  ...         self.y = y
  >>> def my_stmt(foo):
  ...     stmt = lambda_stmt(lambda: select(func.max(foo.x, foo.y)))
  ...     return stmt
  >>> with engine.connect() as conn:
  ...     print(conn.scalar(my_stmt(Foo(5, 10))))
  Traceback (most recent call last):
    # ...
  sqlalchemy.exc.InvalidRequestError: Closure variable named 'foo' inside of
  lambda callable <code object <lambda> at 0x7fed15f35450, file
  "<stdin>", line 2> does not refer to a cacheable SQL element, and also
  does not appear to be serving as a SQL literal bound value based on the
  default SQL expression returned by the function.  This variable needs to
  remain outside the scope of a SQL-generating lambda so that a proper cache
  key may be generated from the lambda's state.  Evaluate this variable
  outside of the lambda, set track_on=[<elements>] to explicitly select
  closure elements to track, or set track_closure_variables=False to exclude
  closure variables from being part of the cache key.
  ```
  The above error indicates that [LambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.LambdaElement) will not assume
  that the `Foo` object passed in will continue to behave the same in all
  cases.    It also won’t assume it can use `Foo` as part of the cache key
  by default; if it were to use the `Foo` object as part of the cache key,
  if there were many different `Foo` objects this would fill up the cache
  with duplicate information, and would also hold long-lasting references to
  all of these objects.
  The best way to resolve the above situation is to not refer to `foo`
  inside of the lambda, and refer to it **outside** instead:
  ```
  >>> def my_stmt(foo):
  ...     x_param, y_param = foo.x, foo.y
  ...     stmt = lambda_stmt(lambda: select(func.max(x_param, y_param)))
  ...     return stmt
  ```
  In some situations, if the SQL structure of the lambda is guaranteed to
  never change based on input, to pass `track_closure_variables=False`
  which will disable any tracking of closure variables other than those
  used for bound parameters:
  ```
  >>> def my_stmt(foo):
  ...     stmt = lambda_stmt(
  ...         lambda: select(func.max(foo.x, foo.y)), track_closure_variables=False
  ...     )
  ...     return stmt
  ```
  There is also the option to add objects to the element to explicitly form
  part of the cache key, using the `track_on` parameter; using this parameter
  allows specific values to serve as the cache key and will also prevent other
  closure variables from being considered.  This is useful for cases where part
  of the SQL being constructed originates from a contextual object of some sort
  that may have many different values.  In the example below, the first
  segment of the SELECT statement will disable tracking of the `foo` variable,
  whereas the second segment will explicitly track `self` as part of the
  cache key:
  ```
  >>> def my_stmt(self, foo):
  ...     stmt = lambda_stmt(
  ...         lambda: select(*self.column_expressions), track_closure_variables=False
  ...     )
  ...     stmt = stmt.add_criteria(lambda: self.where_criteria, track_on=[self])
  ...     return stmt
  ```
  Using `track_on` means the given objects will be stored long term in the
  lambda’s internal cache and will have strong references for as long as the
  cache doesn’t clear out those objects (an LRU scheme of 1000 entries is used
  by default).

#### Cache Key Generation

In order to understand some of the options and behaviors which occur
with lambda SQL constructs, an understanding of the caching system
is helpful.

SQLAlchemy’s caching system normally generates a cache key from a given
SQL expression construct by producing a structure that represents all the
state within the construct:

```
>>> from sqlalchemy import select, column
>>> stmt = select(column("q"))
>>> cache_key = stmt._generate_cache_key()
>>> print(cache_key)  # somewhat paraphrased
CacheKey(key=(
  '0',
  <class 'sqlalchemy.sql.selectable.Select'>,
  '_raw_columns',
  (
    (
      '1',
      <class 'sqlalchemy.sql.elements.ColumnClause'>,
      'name',
      'q',
      'type',
      (
        <class 'sqlalchemy.sql.sqltypes.NullType'>,
      ),
    ),
  ),
  # a few more elements are here, and many more for a more
  # complicated SELECT statement
),)
```

The above key is stored in the cache which is essentially a dictionary, and the
value is a construct that among other things stores the string form of the SQL
statement, in this case the phrase “SELECT q”.  We can observe that even for an
extremely short query the cache key is pretty verbose as it has to represent
everything that may vary about what’s being rendered and potentially executed.

The lambda construction system by contrast creates a different kind of cache
key:

```
>>> from sqlalchemy import lambda_stmt
>>> stmt = lambda_stmt(lambda: select(column("q")))
>>> cache_key = stmt._generate_cache_key()
>>> print(cache_key)
CacheKey(key=(
  <code object <lambda> at 0x7fed1617c710, file "<stdin>", line 1>,
  <class 'sqlalchemy.sql.lambdas.StatementLambdaElement'>,
),)
```

Above, we see a cache key that is vastly shorter than that of the non-lambda
statement, and additionally that production of the `select(column("q"))`
construct itself was not even necessary; the Python lambda itself contains
an attribute called `__code__` which refers to a Python code object that
within the runtime of the application is immutable and permanent.

When the lambda also includes closure variables, in the normal case that these
variables refer to SQL constructs such as column objects, they become
part of the cache key, or if they refer to literal values that will be bound
parameters, they are placed in a separate element of the cache key:

```
>>> def my_stmt(parameter):
...     col = column("q")
...     stmt = lambda_stmt(lambda: select(col))
...     stmt += lambda s: s.where(col == parameter)
...     return stmt
```

The above [StatementLambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement) includes two lambdas, both
of which refer to the `col` closure variable, so the cache key will
represent both of these segments as well as the `column()` object:

```
>>> stmt = my_stmt(5)
>>> key = stmt._generate_cache_key()
>>> print(key)
CacheKey(key=(
  <code object <lambda> at 0x7f07323c50e0, file "<stdin>", line 3>,
  (
    '0',
    <class 'sqlalchemy.sql.elements.ColumnClause'>,
    'name',
    'q',
    'type',
    (
      <class 'sqlalchemy.sql.sqltypes.NullType'>,
    ),
  ),
  <code object <lambda> at 0x7f07323c5190, file "<stdin>", line 4>,
  <class 'sqlalchemy.sql.lambdas.LinkedLambdaElement'>,
  (
    '0',
    <class 'sqlalchemy.sql.elements.ColumnClause'>,
    'name',
    'q',
    'type',
    (
      <class 'sqlalchemy.sql.sqltypes.NullType'>,
    ),
  ),
  (
    '0',
    <class 'sqlalchemy.sql.elements.ColumnClause'>,
    'name',
    'q',
    'type',
    (
      <class 'sqlalchemy.sql.sqltypes.NullType'>,
    ),
  ),
),)
```

The second part of the cache key has retrieved the bound parameters that will
be used when the statement is invoked:

```
>>> key.bindparams
[BindParameter('%(139668884281280 parameter)s', 5, type_=Integer())]
```

For a series of examples of “lambda” caching with performance comparisons,
see the “short_selects” test suite within the [Performance](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-performance)
performance example.

## “Insert Many Values” Behavior for INSERT statements

Added in version 2.0: see [Optimized ORM bulk insert now implemented for all backends other than MySQL](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-6047) for background on the change
including sample performance tests

Tip

The [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature is a **transparently available**
performance feature which requires no end-user intervention in order for
it to take place as needed.   This section describes the architecture
of the feature as well as how to measure its performance and tune its
behavior in order to optimize the speed of bulk INSERT statements,
particularly as used by the ORM.

As more databases have added support for INSERT..RETURNING, SQLAlchemy has
undergone a major change in how it approaches the subject of INSERT statements
where there’s a need to acquire server-generated values, most importantly
server-generated primary key values which allow the new row to be referenced in
subsequent operations. In particular, this scenario has long been a significant
performance issue in the ORM, which relies on being able to retrieve
server-generated primary key values in order to correctly populate the
[identity map](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-map).

With recent support for RETURNING added to SQLite and MariaDB, SQLAlchemy no
longer needs to rely upon the single-row-only
[cursor.lastrowid](https://peps.python.org/pep-0249/#lastrowid) attribute
provided by the [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) for most backends; RETURNING may now be used for
all [SQLAlchemy-included](https://docs.sqlalchemy.org/en/20/dialects/index.html#included-dialects) backends with the exception
of MySQL. The remaining performance
limitation, that the
[cursor.executemany()](https://peps.python.org/pep-0249/#executemany) DBAPI
method does not allow for rows to be fetched, is resolved for most backends by
foregoing the use of `executemany()` and instead restructuring individual
INSERT statements to each accommodate a large number of rows in a single
statement that is invoked using `cursor.execute()`. This approach originates
from the
[psycopg2 fast execution helpers](https://www.psycopg.org/docs/extras.html#fast-execution-helpers)
feature of the `psycopg2` DBAPI, which SQLAlchemy incrementally added more
and more support towards in recent release series.

### Current Support

The feature is enabled for all backend included in SQLAlchemy that support
RETURNING, with the exception of Oracle Database for which both the
python-oracledb and cx_Oracle drivers offer their own equivalent feature. The
feature normally takes place when making use of the
[Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) method of an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct in
conjunction with [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany) execution, which occurs when passing a
list of dictionaries to the [Connection.execute.parameters](#sqlalchemy.engine.Connection.execute.params.parameters)
parameter of the [Connection.execute()](#sqlalchemy.engine.Connection.execute) or
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) methods (as well as equivalent methods under
[asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) and shorthand methods like
[Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars)). It also takes place within the ORM [unit
of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) process when using methods such as [Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) and
[Session.add_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add_all) to add rows.

For SQLAlchemy’s included dialects, support or equivalent support is currently
as follows:

- SQLite - supported for SQLite versions 3.35 and above
- PostgreSQL - all supported Postgresql versions (9 and above)
- SQL Server - all supported SQL Server versions [[1]](#id2)
- MariaDB - supported for MariaDB versions 10.5 and above
- MySQL - no support, no RETURNING feature is present
- Oracle Database - supports RETURNING with executemany using native python-oracledb / cx_Oracle
  APIs, for all supported Oracle Database versions 9 and above, using multi-row OUT
  parameters. This is not the same implementation as “executemanyvalues”, however has
  the same usage patterns and equivalent performance benefits.

Changed in version 2.0.10:

   [[1](#id1)]

”insertmanyvalues” support for Microsoft SQL Server
is restored, after being temporarily disabled in version 2.0.9.

### Disabling the feature

To disable the “insertmanyvalues” feature for a given backend for an
[Engine](#sqlalchemy.engine.Engine) overall, pass the
[create_engine.use_insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.use_insertmanyvalues) parameter as `False` to
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine):

```
engine = create_engine(
    "mariadb+mariadbconnector://scott:tiger@host/db", use_insertmanyvalues=False
)
```

The feature can also be disabled from being used implicitly for a particular
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object by passing the
[Table.implicit_returning](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.implicit_returning) parameter as `False`:

```
t = Table(
    "t",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("x", Integer),
    implicit_returning=False,
)
```

The reason one might want to disable RETURNING for a specific table is to
work around backend-specific limitations.

### Batched Mode Operation

The feature has two modes of operation, which are selected transparently on a
per-dialect, per-[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) basis. One is **batched mode**,
which reduces the number of database round trips by rewriting an
INSERT statement of the form:

```
INSERT INTO a (data, x, y) VALUES (%(data)s, %(x)s, %(y)s) RETURNING a.id
```

into a “batched” form such as:

```
INSERT INTO a (data, x, y) VALUES
    (%(data_0)s, %(x_0)s, %(y_0)s),
    (%(data_1)s, %(x_1)s, %(y_1)s),
    (%(data_2)s, %(x_2)s, %(y_2)s),
    ...
    (%(data_78)s, %(x_78)s, %(y_78)s)
RETURNING a.id
```

where above, the statement is organized against a subset (a “batch”) of the
input data, the size of which is determined by the database backend as well as
the number of parameters in each batch to correspond to known limits for
statement size / number of parameters.  The feature then executes the INSERT
statement once for each batch of input data until all records are consumed,
concatenating the RETURNING results for each batch into a single large
rowset that’s available from a single [Result](#sqlalchemy.engine.Result) object.

This “batched” form allows INSERT of many rows using much fewer database round
trips, and has been shown to allow dramatic performance improvements for most
backends where it’s supported.

### Correlating RETURNING rows to parameter sets

Added in version 2.0.10.

The “batch” mode query illustrated in the previous section does not guarantee
the order of records returned would correspond with that of the input data.
When used by the SQLAlchemy ORM [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) process, as well as for
applications which correlate returned server-generated values with input data,
the [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) and [UpdateBase.return_defaults()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.return_defaults)
methods include an option
[Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order) which indicates that
“insertmanyvalues” mode should guarantee this correspondence. This is **not
related** to the order in which records are actually INSERTed by the database
backend, which is **not** assumed under any circumstances; only that the
returned records should be organized when received back to correspond to the
order in which the original input data was passed.

When the [Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order) parameter is
present, for tables that use server-generated integer primary key values such
as `IDENTITY`, PostgreSQL `SERIAL`, MariaDB `AUTO_INCREMENT`, or SQLite’s
`ROWID` scheme, “batch” mode may instead opt to use a more complex
INSERT..RETURNING form, in conjunction with post-execution sorting of rows
based on the returned values, or if
such a form is not available, the “insertmanyvalues” feature may gracefully
degrade to “non-batched” mode which runs individual INSERT statements for each
parameter set.

For example, on SQL Server when an auto incrementing `IDENTITY` column is
used as the primary key, the following SQL form is used [[2]](#id6):

```
INSERT INTO a (data, x, y)
OUTPUT inserted.id, inserted.id AS id__1
SELECT p0, p1, p2 FROM (VALUES
    (?, ?, ?, 0), (?, ?, ?, 1), (?, ?, ?, 2),
    ...
    (?, ?, ?, 77)
) AS imp_sen(p0, p1, p2, sen_counter) ORDER BY sen_counter
```

A similar form is used for PostgreSQL as well, when primary key columns use
SERIAL or IDENTITY. The above form **does not** guarantee the order in which
rows are inserted. However, it does guarantee that the IDENTITY or SERIAL
values will be created in order with each parameter set [[3]](#id7). The
“insertmanyvalues” feature then sorts the returned rows for the above INSERT
statement by incrementing integer identity.

For the SQLite database, there is no appropriate INSERT form that can
correlate the production of new ROWID values with the order in which
the parameter sets are passed.  As a result, when using server-generated
primary key values, the SQLite backend will degrade to “non-batched”
mode when ordered RETURNING is requested.
For MariaDB, the default INSERT form used by insertmanyvalues is sufficient,
as this database backend will line up the
order of AUTO_INCREMENT with the order of input data when using InnoDB [[4]](#id8).

For a client-side generated primary key, such as when using the Python
`uuid.uuid4()` function to generate new values for a [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) column,
the “insertmanyvalues” feature transparently includes this column in the
RETURNING records and correlates its value to that of the given input records,
thus maintaining correspondence between input records and result rows. From
this, it follows that all backends allow for batched, parameter-correlated
RETURNING order when client-side-generated primary key values are used.

The subject of how “insertmanyvalues” “batch” mode determines a column or
columns to use as a point of correspondence between input parameters and
RETURNING rows is known as an [insert sentinel](https://docs.sqlalchemy.org/en/20/glossary.html#term-insert-sentinel), which is a specific
column or columns that are used to track such values. The “insert sentinel” is
normally selected automatically, however can also be user-configuration for
extremely special cases; the section
[Configuring Sentinel Columns](#engine-insertmanyvalues-sentinel-columns) describes this.

For backends that do not offer an appropriate INSERT form that can deliver
server-generated values deterministically aligned with input values, or
for [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) configurations that feature other kinds of
server generated primary key values, “insertmanyvalues” mode will make use
of **non-batched** mode when guaranteed RETURNING ordering is requested.

See also

   [[2](#id3)]

- Microsoft SQL Server rationale
  “INSERT queries that use SELECT with ORDER BY to populate rows guarantees
  how identity values are computed but not the order in which the rows are inserted.”
  [https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver16#limitations-and-restrictions](https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver16#limitations-and-restrictions)

   [[3](#id4)]

- PostgreSQL batched INSERT Discussion
  Original description in 2018 [https://www.postgresql.org/message-id/29386.1528813619@sss.pgh.pa.us](https://www.postgresql.org/message-id/29386.1528813619@sss.pgh.pa.us)
  Follow up in 2023 - [https://www.postgresql.org/message-id/be108555-da2a-4abc-a46b-acbe8b55bd25%40app.fastmail.com](https://www.postgresql.org/message-id/be108555-da2a-4abc-a46b-acbe8b55bd25%40app.fastmail.com)

   [[4](#id5)]

- MariaDB AUTO_INCREMENT behavior (using the same InnoDB engine as MySQL)
  [https://dev.mysql.com/doc/refman/8.0/en/innodb-auto-increment-handling.html](https://dev.mysql.com/doc/refman/8.0/en/innodb-auto-increment-handling.html)
  [https://dba.stackexchange.com/a/72099](https://dba.stackexchange.com/a/72099)

### Non-Batched Mode Operation

For [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) configurations that do not have client side primary
key values, and offer server-generated primary key values (or no primary key)
that the database in question is not able to invoke in a deterministic or
sortable way relative to multiple parameter sets, the “insertmanyvalues”
feature when tasked with satisfying the
[Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order) requirement for an
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) statement may instead opt to use **non-batched mode**.

In this mode, the original SQL form of INSERT is maintained, and the
“insertmanyvalues” feature will instead run the statement as given for each
parameter set individually, organizing the returned rows into a full result
set. Unlike previous SQLAlchemy versions, it does so in a tight loop that
minimizes Python overhead. In some cases, such as on SQLite, “non-batched” mode
performs exactly as well as “batched” mode.

### Statement Execution Model

For both “batched” and “non-batched” modes, the feature will necessarily
invoke **multiple INSERT statements** using the DBAPI `cursor.execute()` method,
within the scope of  **single** call to the Core-level
[Connection.execute()](#sqlalchemy.engine.Connection.execute) method,
with each statement containing up to a fixed limit of parameter sets.
This limit is configurable as described below at [Controlling the Batch Size](#engine-insertmanyvalues-page-size).
The separate calls to `cursor.execute()` are logged individually and
also individually passed along to event listeners such as
[ConnectionEvents.before_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute) (see [Logging and Events](#engine-insertmanyvalues-events)
below).

#### Configuring Sentinel Columns

In typical cases, the “insertmanyvalues” feature in order to provide
INSERT..RETURNING with deterministic row order will automatically determine a
sentinel column from a given table’s primary key, gracefully degrading to “row
at a time” mode if one cannot be identified. As a completely **optional**
feature, to get full “insertmanyvalues” bulk performance for tables that have
server generated primary keys whose default generator functions aren’t
compatible with the “sentinel” use case, other non-primary key columns may be
marked as “sentinel” columns assuming they meet certain requirements. A typical
example is a non-primary key [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) column with a client side
default such as the Python `uuid.uuid4()` function.  There is also a construct to create
simple integer columns with a a client side integer counter oriented towards
the “insertmanyvalues” use case.

Sentinel columns may be indicated by adding [Column.insert_sentinel](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.insert_sentinel)
to qualifying columns.   The most basic “qualifying” column is a not-nullable,
unique column with a client side default, such as a UUID column as follows:

```
import uuid

from sqlalchemy import Column
from sqlalchemy import FetchedValue
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Uuid

my_table = Table(
    "some_table",
    metadata,
    # assume some arbitrary server-side function generates
    # primary key values, so cannot be tracked by a bulk insert
    Column("id", String(50), server_default=FetchedValue(), primary_key=True),
    Column("data", String(50)),
    Column(
        "uniqueid",
        Uuid(),
        default=uuid.uuid4,
        nullable=False,
        unique=True,
        insert_sentinel=True,
    ),
)
```

When using ORM Declarative models, the same forms are available using
the [mapped_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct:

```
import uuid

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class MyClass(Base):
    __tablename__ = "my_table"

    id: Mapped[str] = mapped_column(primary_key=True, server_default=FetchedValue())
    data: Mapped[str] = mapped_column(String(50))
    uniqueid: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, unique=True, insert_sentinel=True
    )
```

While the values generated by the default generator **must** be unique, the
actual UNIQUE constraint on the above “sentinel” column, indicated by the
`unique=True` parameter, itself is optional and may be omitted if not
desired.

There is also a special form of “insert sentinel” that’s a dedicated nullable
integer column which makes use of a special default integer counter that’s only
used during “insertmanyvalues” operations; as an additional behavior, the
column will omit itself from SQL statements and result sets and behave in a
mostly transparent manner.  It does need to be physically present within
the actual database table, however.  This style of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
may be constructed using the function [insert_sentinel()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.insert_sentinel):

```
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Uuid
from sqlalchemy import insert_sentinel

Table(
    "some_table",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", String(50)),
    insert_sentinel("sentinel"),
)
```

When using ORM Declarative, a Declarative-friendly version of
[insert_sentinel()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.insert_sentinel) is available called
[orm_insert_sentinel()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.orm_insert_sentinel), which has the ability to be used on the Base
class or a mixin; if packaged using [declared_attr()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr), the column will
apply itself to all table-bound subclasses including within joined inheritance
hierarchies:

```
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import orm_insert_sentinel

class Base(DeclarativeBase):
    @declared_attr
    def _sentinel(cls) -> Mapped[int]:
        return orm_insert_sentinel()

class MyClass(Base):
    __tablename__ = "my_table"

    id: Mapped[str] = mapped_column(primary_key=True, server_default=FetchedValue())
    data: Mapped[str] = mapped_column(String(50))

class MySubClass(MyClass):
    __tablename__ = "sub_table"

    id: Mapped[str] = mapped_column(ForeignKey("my_table.id"), primary_key=True)

class MySingleInhClass(MyClass):
    pass
```

In the example above, both “my_table” and “sub_table” will have an additional
integer column named “_sentinel” that can be used by the “insertmanyvalues”
feature to help optimize bulk inserts used by the ORM.

### Controlling the Batch Size

A key characteristic of “insertmanyvalues” is that the size of the INSERT
statement is limited on a fixed max number of “values” clauses as well as a
dialect-specific fixed total number of bound parameters that may be represented
in one INSERT statement at a time. When the number of parameter dictionaries
given exceeds a fixed limit, or when the total number of bound parameters to be
rendered in a single INSERT statement exceeds a fixed limit (the two fixed
limits are separate), multiple INSERT statements will be invoked within the
scope of a single [Connection.execute()](#sqlalchemy.engine.Connection.execute) call, each of which
accommodate for a portion of the parameter dictionaries, known as a
“batch”.  The number of parameter dictionaries represented within each
“batch” is then known as the “batch size”.  For example, a batch size of
500 means that each INSERT statement emitted will INSERT at most 500 rows.

It’s potentially important to be able to adjust the batch size,
as a larger batch size may be more performant for an INSERT where the value
sets themselves are relatively small, and a smaller batch size may be more
appropriate for an INSERT that uses very large value sets, where both the size
of the rendered SQL as well as the total data size being passed in one
statement may benefit from being limited to a certain size based on backend
behavior and memory constraints.  For this reason the batch size
can be configured on a per-[Engine](#sqlalchemy.engine.Engine) as well as a per-statement
basis.   The parameter limit on the other hand is fixed based on the known
characteristics of the database in use.

The batch size defaults to 1000 for most backends, with an additional
per-dialect “max number of parameters” limiting factor that may reduce the
batch size further on a per-statement basis. The max number of parameters
varies by dialect and server version; the largest size is 32700 (chosen as a
healthy distance away from PostgreSQL’s limit of 32767 and SQLite’s modern
limit of 32766, while leaving room for additional parameters in the statement
as well as for DBAPI quirkiness). Older versions of SQLite (prior to 3.32.0)
will set this value to 999. MariaDB has no established limit however 32700
remains as a limiting factor for SQL message size.

The value of the “batch size” can be affected [Engine](#sqlalchemy.engine.Engine)
wide via the [create_engine.insertmanyvalues_page_size](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.insertmanyvalues_page_size) parameter.
Such as, to affect INSERT statements to include up to 100 parameter sets
in each statement:

```
e = create_engine("sqlite://", insertmanyvalues_page_size=100)
```

The batch size may also be affected on a per statement basis using the
[Connection.execution_options.insertmanyvalues_page_size](#sqlalchemy.engine.Connection.execution_options.params.insertmanyvalues_page_size)
execution option, such as per execution:

```
with e.begin() as conn:
    result = conn.execute(
        table.insert().returning(table.c.id),
        parameterlist,
        execution_options={"insertmanyvalues_page_size": 100},
    )
```

Or configured on the statement itself:

```
stmt = (
    table.insert()
    .returning(table.c.id)
    .execution_options(insertmanyvalues_page_size=100)
)
with e.begin() as conn:
    result = conn.execute(stmt, parameterlist)
```

### Logging and Events

The “insertmanyvalues” feature integrates fully with SQLAlchemy’s [statement
logging](https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging) as well as cursor events such as [ConnectionEvents.before_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute).
When the list of parameters is broken into separate batches, **each INSERT
statement is logged and passed to event handlers individually**.   This is a major change
compared to how the psycopg2-only feature worked in previous 1.x series of
SQLAlchemy, where the production of multiple INSERT statements was hidden from
logging and events.  Logging display will truncate the long lists of parameters for readability,
and will also indicate the specific batch of each statement. The example below illustrates
an excerpt of this logging:

```
INSERT INTO a (data, x, y) VALUES (?, ?, ?), ... 795 characters truncated ...  (?, ?, ?), (?, ?, ?) RETURNING id
[generated in 0.00177s (insertmanyvalues) 1/10 (unordered)] ('d0', 0, 0, 'd1',  ...
INSERT INTO a (data, x, y) VALUES (?, ?, ?), ... 795 characters truncated ...  (?, ?, ?), (?, ?, ?) RETURNING id
[insertmanyvalues 2/10 (unordered)] ('d100', 100, 1000, 'd101', ...

...

INSERT INTO a (data, x, y) VALUES (?, ?, ?), ... 795 characters truncated ...  (?, ?, ?), (?, ?, ?) RETURNING id
[insertmanyvalues 10/10 (unordered)] ('d900', 900, 9000, 'd901', ...
```

When [non-batch mode](#engine-insertmanyvalues-non-batch) takes place, logging
will indicate this along with the insertmanyvalues message:

```
...

INSERT INTO a (data, x, y) VALUES (?, ?, ?) RETURNING id
[insertmanyvalues 67/78 (ordered; batch not supported)] ('d66', 66, 66)
INSERT INTO a (data, x, y) VALUES (?, ?, ?) RETURNING id
[insertmanyvalues 68/78 (ordered; batch not supported)] ('d67', 67, 67)
INSERT INTO a (data, x, y) VALUES (?, ?, ?) RETURNING id
[insertmanyvalues 69/78 (ordered; batch not supported)] ('d68', 68, 68)
INSERT INTO a (data, x, y) VALUES (?, ?, ?) RETURNING id
[insertmanyvalues 70/78 (ordered; batch not supported)] ('d69', 69, 69)

...
```

See also

[Configuring Logging](https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging)

### Upsert Support

The PostgreSQL, SQLite, and MariaDB dialects offer backend-specific
“upsert” constructs [insert()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.insert), [insert()](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.insert)
and [insert()](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.insert), which are each [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) constructs that
have an additional method such as `on_conflict_do_update()` or
``on_duplicate_key()`.   These constructs also support “insertmanyvalues”
behaviors when they are used with RETURNING, allowing efficient upserts
with RETURNING to take place.

## Engine Disposal

The [Engine](#sqlalchemy.engine.Engine) refers to a connection pool, which means under normal
circumstances, there are open database connections present while the
[Engine](#sqlalchemy.engine.Engine) object is still resident in memory.   When an [Engine](#sqlalchemy.engine.Engine)
is garbage collected, its connection pool is no longer referred to by
that [Engine](#sqlalchemy.engine.Engine), and assuming none of its connections are still checked
out, the pool and its connections will also be garbage collected, which has the
effect of closing out the actual database connections as well.   But otherwise,
the [Engine](#sqlalchemy.engine.Engine) will hold onto open database connections assuming
it uses the normally default pool implementation of [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool).

The [Engine](#sqlalchemy.engine.Engine) is intended to normally be a permanent
fixture established up-front and maintained throughout the lifespan of an
application.  It is **not** intended to be created and disposed on a
per-connection basis; it is instead a registry that maintains both a pool
of connections as well as configurational information about the database
and DBAPI in use, as well as some degree of internal caching of per-database
resources.

However, there are many cases where it is desirable that all connection resources
referred to by the [Engine](#sqlalchemy.engine.Engine) be completely closed out.  It’s
generally not a good idea to rely on Python garbage collection for this
to occur for these cases; instead, the [Engine](#sqlalchemy.engine.Engine) can be explicitly disposed using
the [Engine.dispose()](#sqlalchemy.engine.Engine.dispose) method.   This disposes of the engine’s
underlying connection pool and replaces it with a new one that’s empty.
Provided that the [Engine](#sqlalchemy.engine.Engine)
is discarded at this point and no longer used, all **checked-in** connections
which it refers to will also be fully closed.

Valid use cases for calling [Engine.dispose()](#sqlalchemy.engine.Engine.dispose) include:

- When a program wants to release any remaining checked-in connections
  held by the connection pool and expects to no longer be connected
  to that database at all for any future operations.
- When a program uses multiprocessing or `fork()`, and an
  [Engine](#sqlalchemy.engine.Engine) object is copied to the child process,
  [Engine.dispose()](#sqlalchemy.engine.Engine.dispose) should be called so that the engine creates
  brand new database connections local to that fork.   Database connections
  generally do **not** travel across process boundaries.  Use the
  [Engine.dispose.close](#sqlalchemy.engine.Engine.dispose.params.close) parameter set to False in this case.
  See the section [Using Connection Pools with Multiprocessing or os.fork()](https://docs.sqlalchemy.org/en/20/core/pooling.html#pooling-multiprocessing) for more background on this
  use case.
- Within test suites or multitenancy scenarios where many
  ad-hoc, short-lived [Engine](#sqlalchemy.engine.Engine) objects may be created and disposed.

Connections that are **checked out** are **not** discarded when the
engine is disposed or garbage collected, as these connections are still
strongly referenced elsewhere by the application.
However, after [Engine.dispose()](#sqlalchemy.engine.Engine.dispose) is called, those
connections are no longer associated with that [Engine](#sqlalchemy.engine.Engine); when they
are closed, they will be returned to their now-orphaned connection pool
which will ultimately be garbage collected, once all connections which refer
to it are also no longer referenced anywhere.
Since this process is not easy to control, it is strongly recommended that
[Engine.dispose()](#sqlalchemy.engine.Engine.dispose) is called only after all checked out connections
are checked in or otherwise de-associated from their pool.

An alternative for applications that are negatively impacted by the
[Engine](#sqlalchemy.engine.Engine) object’s use of connection pooling is to disable pooling
entirely.  This typically incurs only a modest performance impact upon the
use of new connections, and means that when a connection is checked in,
it is entirely closed out and is not held in memory.  See [Switching Pool Implementations](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-switching)
for guidelines on how to disable pooling.

See also

[Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)

[Using Connection Pools with Multiprocessing or os.fork()](https://docs.sqlalchemy.org/en/20/core/pooling.html#pooling-multiprocessing)

## Working with Driver SQL and Raw DBAPI Connections

The introduction on using [Connection.execute()](#sqlalchemy.engine.Connection.execute) made use of the
[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct in order to illustrate how textual SQL statements
may be invoked.  When working with SQLAlchemy, textual SQL is actually more
of the exception rather than the norm, as the Core expression language
and the ORM both abstract away the textual representation of SQL.  However, the
[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct itself also provides some abstraction of textual
SQL in that it normalizes how bound parameters are passed, as well as that
it supports datatyping behavior for parameters and result set rows.

### Invoking SQL strings directly to the driver

For the use case where one wants to invoke textual SQL directly passed to the
underlying driver (known as the [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI)) without any intervention
from the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct, the [Connection.exec_driver_sql()](#sqlalchemy.engine.Connection.exec_driver_sql)
method may be used:

```
with engine.connect() as conn:
    conn.exec_driver_sql("SET param='bar'")
```

Added in version 1.4: Added the [Connection.exec_driver_sql()](#sqlalchemy.engine.Connection.exec_driver_sql) method.

### Working with the DBAPI cursor directly

There are some cases where SQLAlchemy does not provide a genericized way
at accessing some [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) functions, such as calling stored procedures as well
as dealing with multiple result sets.  In these cases, it’s just as expedient
to deal with the raw DBAPI connection directly.

The most common way to access the raw DBAPI connection is to get it
from an already present [Connection](#sqlalchemy.engine.Connection) object directly.  It is
present using the [Connection.connection](#sqlalchemy.engine.Connection.connection) attribute:

```
connection = engine.connect()
dbapi_conn = connection.connection
```

The DBAPI connection here is actually a “proxied” in terms of the
originating connection pool, however this is an implementation detail
that in most cases can be ignored.    As this DBAPI connection is still
contained within the scope of an owning [Connection](#sqlalchemy.engine.Connection) object, it is
best to make use of the [Connection](#sqlalchemy.engine.Connection) object for most features such
as transaction control as well as calling the [Connection.close()](#sqlalchemy.engine.Connection.close)
method; if these operations are performed on the DBAPI connection directly,
the owning [Connection](#sqlalchemy.engine.Connection) will not be aware of these changes in state.

To overcome the limitations imposed by the DBAPI connection that is
maintained by an owning [Connection](#sqlalchemy.engine.Connection), a DBAPI connection is also
available without the need to procure a
[Connection](#sqlalchemy.engine.Connection) first, using the [Engine.raw_connection()](#sqlalchemy.engine.Engine.raw_connection) method
of [Engine](#sqlalchemy.engine.Engine):

```
dbapi_conn = engine.raw_connection()
```

This DBAPI connection is again a “proxied” form as was the case before.
The purpose of this proxying is now apparent, as when we call the `.close()`
method of this connection, the DBAPI connection is typically not actually
closed, but instead [released](https://docs.sqlalchemy.org/en/20/glossary.html#term-released) back to the
engine’s connection pool:

```
dbapi_conn.close()
```

While SQLAlchemy may in the future add built-in patterns for more DBAPI
use cases, there are diminishing returns as these cases tend to be rarely
needed and they also vary highly dependent on the type of DBAPI in use,
so in any case the direct DBAPI calling pattern is always there for those
cases where it is needed.

See also

[How do I get at the raw DBAPI connection when using an Engine?](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-dbapi-connection) - includes additional details about how
the DBAPI connection is accessed as well as the “driver” connection
when using asyncio drivers.

Some recipes for DBAPI connection use follow.

### Calling Stored Procedures and User Defined Functions

SQLAlchemy supports calling stored procedures and user defined functions
several ways. Please note that all DBAPIs have different practices, so you must
consult your underlying DBAPI’s documentation for specifics in relation to your
particular usage. The following examples are hypothetical and may not work with
your underlying DBAPI.

For stored procedures or functions with special syntactical or parameter concerns,
DBAPI-level [callproc](https://legacy.python.org/dev/peps/pep-0249/#callproc)
may potentially be used with your DBAPI. An example of this pattern is:

```
connection = engine.raw_connection()
try:
    cursor_obj = connection.cursor()
    cursor_obj.callproc("my_procedure", ["x", "y", "z"])
    results = list(cursor_obj.fetchall())
    cursor_obj.close()
    connection.commit()
finally:
    connection.close()
```

Note

Not all DBAPIs use callproc and overall usage details will vary. The above
example is only an illustration of how it might look to use a particular DBAPI
function.

Your DBAPI may not have a `callproc` requirement *or* may require a stored
procedure or user defined function to be invoked with another pattern, such as
normal SQLAlchemy connection usage. One example of this usage pattern is,
*at the time of this documentation’s writing*, executing a stored procedure in
the PostgreSQL database with the psycopg2 DBAPI, which should be invoked
with normal connection usage:

```
connection.execute("CALL my_procedure();")
```

This above example is hypothetical. The underlying database is not guaranteed to
support “CALL” or “SELECT” in these situations, and the keyword may vary
dependent on the function being a stored procedure or a user defined function.
You should consult your underlying DBAPI and database documentation in these
situations to determine the correct syntax and patterns to use.

### Multiple Result Sets

Multiple result set support is available from a raw DBAPI cursor using the
[nextset](https://legacy.python.org/dev/peps/pep-0249/#nextset) method:

```
connection = engine.raw_connection()
try:
    cursor_obj = connection.cursor()
    cursor_obj.execute("select * from table1; select * from table2")
    results_one = cursor_obj.fetchall()
    cursor_obj.nextset()
    results_two = cursor_obj.fetchall()
    cursor_obj.close()
finally:
    connection.close()
```

## Registering New Dialects

The [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) function call locates the given dialect
using setuptools entrypoints.   These entry points can be established
for third party dialects within the setup.py script.  For example,
to create a new dialect “foodialect://”, the steps are as follows:

1. Create a package called `foodialect`.
2. The package should have a module containing the dialect class,
  which is typically a subclass of [sqlalchemy.engine.default.DefaultDialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect).
  In this example let’s say it’s called `FooDialect` and its module is accessed
  via `foodialect.dialect`.
3. The entry point can be established in `setup.cfg` as follows:
  ```
  [options.entry_points]
  sqlalchemy.dialects =
      foodialect = foodialect.dialect:FooDialect
  ```

If the dialect is providing support for a particular DBAPI on top of
an existing SQLAlchemy-supported database, the name can be given
including a database-qualification.  For example, if `FooDialect`
were in fact a MySQL dialect, the entry point could be established like this:

```
[options.entry_points]
sqlalchemy.dialects
    mysql.foodialect = foodialect.dialect:FooDialect
```

The above entrypoint would then be accessed as `create_engine("mysql+foodialect://")`.

### Registering Dialects In-Process

SQLAlchemy also allows a dialect to be registered within the current process, bypassing
the need for separate installation.   Use the `register()` function as follows:

```
from sqlalchemy.dialects import registry

registry.register("mysql.foodialect", "myapp.dialect", "MyMySQLDialect")
```

The above will respond to `create_engine("mysql+foodialect://")` and load the
`MyMySQLDialect` class from the `myapp.dialect` module.

## Connection / Engine API

| Object Name | Description |
| --- | --- |
| Connection | Provides high-level functionality for a wrapped DB-API connection. |
| CreateEnginePlugin | A set of hooks intended to augment the construction of anEngineobject based on entrypoint names in a URL. |
| Engine | Connects aPoolandDialecttogether to provide a
source of database connectivity and behavior. |
| ExceptionContext | Encapsulate information about an error condition in progress. |
| NestedTransaction | Represent a ‘nested’, or SAVEPOINT transaction. |
| RootTransaction | Represent the “root” transaction on aConnection. |
| Transaction | Represent a database transaction in progress. |
| TwoPhaseTransaction | Represent a two-phase transaction. |

   class sqlalchemy.engine.Connection

*inherits from* `sqlalchemy.engine.interfaces.ConnectionEventsTarget`, `sqlalchemy.inspection.Inspectable`

Provides high-level functionality for a wrapped DB-API connection.

The [Connection](#sqlalchemy.engine.Connection) object is procured by calling the
[Engine.connect()](#sqlalchemy.engine.Engine.connect) method of the [Engine](#sqlalchemy.engine.Engine)
object, and provides services for execution of SQL statements as well
as transaction control.

The Connection object is **not** thread-safe. While a Connection can be
shared among threads using properly synchronized access, it is still
possible that the underlying DBAPI connection may not support shared
access between threads. Check the DBAPI documentation for details.

The Connection object represents a single DBAPI connection checked out
from the connection pool. In this state, the connection pool has no
affect upon the connection, including its expiration or timeout state.
For the connection pool to properly manage connections, connections
should be returned to the connection pool (i.e. `connection.close()`)
whenever the connection is not in use.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a new Connection. |
| begin() | Begin a transaction prior to autobegin occurring. |
| begin_nested() | Begin a nested transaction (i.e. SAVEPOINT) and return a transaction
handle that controls the scope of the SAVEPOINT. |
| begin_twophase() | Begin a two-phase or XA transaction and return a transaction
handle. |
| close() | Close thisConnection. |
| commit() | Commit the transaction that is currently in progress. |
| detach() | Detach the underlying DB-API connection from its connection pool. |
| exec_driver_sql() | Executes a string SQL statement on the DBAPI cursor directly,
without any SQL compilation steps. |
| execute() | Executes a SQL statement construct and returns aCursorResult. |
| execution_options() | Set non-SQL options for the connection which take effect
during execution. |
| get_execution_options() | Get the non-SQL options which will take effect during execution. |
| get_isolation_level() | Return the currentactualisolation level that’s present on
the database within the scope of this connection. |
| get_nested_transaction() | Return the current nested transaction in progress, if any. |
| get_transaction() | Return the current root transaction in progress, if any. |
| in_nested_transaction() | Return True if a transaction is in progress. |
| in_transaction() | Return True if a transaction is in progress. |
| invalidate() | Invalidate the underlying DBAPI connection associated with
thisConnection. |
| rollback() | Roll back the transaction that is currently in progress. |
| scalar() | Executes a SQL statement construct and returns a scalar object. |
| scalars() | Executes and returns a scalar result set, which yields scalar values
from the first column of each row. |
| schema_for_object() | Return the schema name for the given schema item taking into
account current schema translate map. |

   method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)__init__(*engine:Engine*, *connection:PoolProxiedConnection|None=None*, *_has_events:bool|None=None*, *_allow_revalidate:bool=True*, *_allow_autobegin:bool=True*)

Construct a new Connection.

    method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)begin() → [RootTransaction](#sqlalchemy.engine.RootTransaction)

Begin a transaction prior to autobegin occurring.

E.g.:

```
with engine.connect() as conn:
    with conn.begin() as trans:
        conn.execute(table.insert(), {"username": "sandy"})
```

The returned object is an instance of [RootTransaction](#sqlalchemy.engine.RootTransaction).
This object represents the “scope” of the transaction,
which completes when either the [Transaction.rollback()](#sqlalchemy.engine.Transaction.rollback)
or [Transaction.commit()](#sqlalchemy.engine.Transaction.commit) method is called; the object
also works as a context manager as illustrated above.

The [Connection.begin()](#sqlalchemy.engine.Connection.begin) method begins a
transaction that normally will be begun in any case when the connection
is first used to execute a statement.  The reason this method might be
used would be to invoke the [ConnectionEvents.begin()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.begin)
event at a specific time, or to organize code within the scope of a
connection checkout in terms of context managed blocks, such as:

```
with engine.connect() as conn:
    with conn.begin():
        conn.execute(...)
        conn.execute(...)

    with conn.begin():
        conn.execute(...)
        conn.execute(...)
```

The above code is not  fundamentally any different in its behavior than
the following code  which does not use
[Connection.begin()](#sqlalchemy.engine.Connection.begin); the below style is known
as “commit as you go” style:

```
with engine.connect() as conn:
    conn.execute(...)
    conn.execute(...)
    conn.commit()

    conn.execute(...)
    conn.execute(...)
    conn.commit()
```

From a database point of view, the [Connection.begin()](#sqlalchemy.engine.Connection.begin)
method does not emit any SQL or change the state of the underlying
DBAPI connection in any way; the Python DBAPI does not have any
concept of explicit transaction begin.

See also

[Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-working-with-transactions) - in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested) - use a SAVEPOINT

[Connection.begin_twophase()](#sqlalchemy.engine.Connection.begin_twophase) -
use a two phase /XID transaction

[Engine.begin()](#sqlalchemy.engine.Engine.begin) - context manager available from
[Engine](#sqlalchemy.engine.Engine)

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)begin_nested() → [NestedTransaction](#sqlalchemy.engine.NestedTransaction)

Begin a nested transaction (i.e. SAVEPOINT) and return a transaction
handle that controls the scope of the SAVEPOINT.

E.g.:

```
with engine.begin() as connection:
    with connection.begin_nested():
        connection.execute(table.insert(), {"username": "sandy"})
```

The returned object is an instance of
[NestedTransaction](#sqlalchemy.engine.NestedTransaction), which includes transactional
methods [NestedTransaction.commit()](#sqlalchemy.engine.NestedTransaction.commit) and
[NestedTransaction.rollback()](#sqlalchemy.engine.NestedTransaction.rollback); for a nested transaction,
these methods correspond to the operations “RELEASE SAVEPOINT <name>”
and “ROLLBACK TO SAVEPOINT <name>”. The name of the savepoint is local
to the [NestedTransaction](#sqlalchemy.engine.NestedTransaction) object and is generated
automatically. Like any other [Transaction](#sqlalchemy.engine.Transaction), the
[NestedTransaction](#sqlalchemy.engine.NestedTransaction) may be used as a context manager as
illustrated above which will “release” or “rollback” corresponding to
if the operation within the block were successful or raised an
exception.

Nested transactions require SAVEPOINT support in the underlying
database, else the behavior is undefined. SAVEPOINT is commonly used to
run operations within a transaction that may fail, while continuing the
outer transaction. E.g.:

```
from sqlalchemy import exc

with engine.begin() as connection:
    trans = connection.begin_nested()
    try:
        connection.execute(table.insert(), {"username": "sandy"})
        trans.commit()
    except exc.IntegrityError:  # catch for duplicate username
        trans.rollback()  # rollback to savepoint

    # outer transaction continues
    connection.execute(...)
```

If [Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested) is called without first
calling [Connection.begin()](#sqlalchemy.engine.Connection.begin) or
[Engine.begin()](#sqlalchemy.engine.Engine.begin), the [Connection](#sqlalchemy.engine.Connection) object
will “autobegin” the outer transaction first. This outer transaction
may be committed using “commit-as-you-go” style, e.g.:

```
with engine.connect() as connection:  # begin() wasn't called

    with connection.begin_nested():  # will auto-"begin()" first
        connection.execute(...)
    # savepoint is released

    connection.execute(...)

    # explicitly commit outer transaction
    connection.commit()

    # can continue working with connection here
```

Changed in version 2.0: [Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested) will now participate
in the connection “autobegin” behavior that is new as of
2.0 / “future” style connections in 1.4.

See also

[Connection.begin()](#sqlalchemy.engine.Connection.begin)

[Using SAVEPOINT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-begin-nested) - ORM support for SAVEPOINT

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)begin_twophase(*xid:Any|None=None*) → [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction)

Begin a two-phase or XA transaction and return a transaction
handle.

The returned object is an instance of [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction),
which in addition to the methods provided by
[Transaction](#sqlalchemy.engine.Transaction), also provides a
[TwoPhaseTransaction.prepare()](#sqlalchemy.engine.TwoPhaseTransaction.prepare) method.

  Parameters:

**xid** – the two phase transaction id.  If not supplied, a
random id will be generated.

See also

[Connection.begin()](#sqlalchemy.engine.Connection.begin)

[Connection.begin_twophase()](#sqlalchemy.engine.Connection.begin_twophase)

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)close() → None

Close this [Connection](#sqlalchemy.engine.Connection).

This results in a release of the underlying database
resources, that is, the DBAPI connection referenced
internally. The DBAPI connection is typically restored
back to the connection-holding [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) referenced
by the [Engine](#sqlalchemy.engine.Engine) that produced this
[Connection](#sqlalchemy.engine.Connection). Any transactional state present on
the DBAPI connection is also unconditionally released via
the DBAPI connection’s `rollback()` method, regardless
of any [Transaction](#sqlalchemy.engine.Transaction) object that may be
outstanding with regards to this [Connection](#sqlalchemy.engine.Connection).

This has the effect of also calling [Connection.rollback()](#sqlalchemy.engine.Connection.rollback)
if any transaction is in place.

After [Connection.close()](#sqlalchemy.engine.Connection.close) is called, the
[Connection](#sqlalchemy.engine.Connection) is permanently in a closed state,
and will allow no further operations.

    property closed: bool

Return True if this connection is closed.

    method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)commit() → None

Commit the transaction that is currently in progress.

This method commits the current transaction if one has been started.
If no transaction was started, the method has no effect, assuming
the connection is in a non-invalidated state.

A transaction is begun on a [Connection](#sqlalchemy.engine.Connection) automatically
whenever a statement is first executed, or when the
[Connection.begin()](#sqlalchemy.engine.Connection.begin) method is called.

Note

The [Connection.commit()](#sqlalchemy.engine.Connection.commit) method only acts upon
the primary database transaction that is linked to the
[Connection](#sqlalchemy.engine.Connection) object.  It does not operate upon a
SAVEPOINT that would have been invoked from the
[Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested) method; for control of a
SAVEPOINT, call [NestedTransaction.commit()](#sqlalchemy.engine.NestedTransaction.commit) on the
[NestedTransaction](#sqlalchemy.engine.NestedTransaction) that is returned by the
[Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested) method itself.

     property connection: [PoolProxiedConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection)

The underlying DB-API connection managed by this Connection.

This is a SQLAlchemy connection-pool proxied connection
which then has the attribute
`_ConnectionFairy.dbapi_connection` that refers to the
actual driver connection.

See also

[Working with Driver SQL and Raw DBAPI Connections](#dbapi-connections)

     property default_isolation_level: Literal['SERIALIZABLE', 'REPEATABLE READ', 'READ COMMITTED', 'READ UNCOMMITTED', 'AUTOCOMMIT'] | None

The initial-connection time isolation level associated with the
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in use.

This value is independent of the
[Connection.execution_options.isolation_level](#sqlalchemy.engine.Connection.execution_options.params.isolation_level) and
[Engine.execution_options.isolation_level](#sqlalchemy.engine.Engine.execution_options.params.isolation_level) execution
options, and is determined by the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) when the
first connection is created, by performing a SQL query against the
database for the current isolation level before any additional commands
have been emitted.

Calling this accessor does not invoke any new SQL queries.

See also

[Connection.get_isolation_level()](#sqlalchemy.engine.Connection.get_isolation_level)
- view current actual isolation level

[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level)
- set per [Engine](#sqlalchemy.engine.Engine) isolation level

[Connection.execution_options.isolation_level](#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
- set per [Connection](#sqlalchemy.engine.Connection) isolation level

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)detach() → None

Detach the underlying DB-API connection from its connection pool.

E.g.:

```
with engine.connect() as conn:
    conn.detach()
    conn.execute(text("SET search_path TO schema1, schema2"))

    # work with connection

# connection is fully closed (since we used "with:", can
# also call .close())
```

This [Connection](#sqlalchemy.engine.Connection) instance will remain usable.
When closed
(or exited from a context manager context as above),
the DB-API connection will be literally closed and not
returned to its originating pool.

This method can be used to insulate the rest of an application
from a modified state on a connection (such as a transaction
isolation level or similar).

    method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)exec_driver_sql(*statement:str*, *parameters:_DBAPIAnyExecuteParams|None=None*, *execution_options:CoreExecuteOptionsParameter|None=None*) → [CursorResult](#sqlalchemy.engine.CursorResult)[Any]

Executes a string SQL statement on the DBAPI cursor directly,
without any SQL compilation steps.

This can be used to pass any string directly to the
`cursor.execute()` method of the DBAPI in use.

  Parameters:

- **statement** – The statement str to be executed.   Bound parameters
  must use the underlying DBAPI’s paramstyle, such as “qmark”,
  “pyformat”, “format”, etc.
- **parameters** – represent bound parameter values to be used in the
  execution.  The format is one of:   a dictionary of named parameters,
  a tuple of positional parameters, or a list containing either
  dictionaries or tuples for multiple-execute support.

  Returns:

a [CursorResult](#sqlalchemy.engine.CursorResult).

E.g. multiple dictionaries:

```
conn.exec_driver_sql(
    "INSERT INTO table (id, value) VALUES (%(id)s, %(value)s)",
    [{"id": 1, "value": "v1"}, {"id": 2, "value": "v2"}],
)
```

Single dictionary:

```
conn.exec_driver_sql(
    "INSERT INTO table (id, value) VALUES (%(id)s, %(value)s)",
    dict(id=1, value="v1"),
)
```

Single tuple:

```
conn.exec_driver_sql(
    "INSERT INTO table (id, value) VALUES (?, ?)", (1, "v1")
)
```

Note

The [Connection.exec_driver_sql()](#sqlalchemy.engine.Connection.exec_driver_sql) method does
not participate in the
[ConnectionEvents.before_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_execute) and
[ConnectionEvents.after_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.after_execute) events.   To
intercept calls to [Connection.exec_driver_sql()](#sqlalchemy.engine.Connection.exec_driver_sql), use
[ConnectionEvents.before_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute) and
[ConnectionEvents.after_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.after_cursor_execute).

See also

[PEP 249](https://peps.python.org/pep-0249/)

       method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)execute(*statement:Executable*, *parameters:_CoreAnyExecuteParams|None=None*, ***, *execution_options:CoreExecuteOptionsParameter|None=None*) → [CursorResult](#sqlalchemy.engine.CursorResult)[Any]

Executes a SQL statement construct and returns a
[CursorResult](#sqlalchemy.engine.CursorResult).

  Parameters:

- **statement** –
  The statement to be executed.  This is always
  an object that is in both the [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) and
  [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable) hierarchies, including:
  - [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
  - [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update),
    [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete)
  - [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) and
    [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect)
  - [DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DDL) and objects which inherit from
    [ExecutableDDLElement](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement)
- **parameters** – parameters which will be bound into the statement.
  This may be either a dictionary of parameter names to values,
  or a mutable sequence (e.g. a list) of dictionaries.  When a
  list of dictionaries is passed, the underlying statement execution
  will make use of the DBAPI `cursor.executemany()` method.
  When a single dictionary is passed, the DBAPI `cursor.execute()`
  method will be used.
- **execution_options** – optional dictionary of execution options,
  which will be associated with the statement execution.  This
  dictionary can provide a subset of the options that are accepted
  by [Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options).

  Returns:

a [Result](#sqlalchemy.engine.Result) object.

      method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)execution_options(***opt:Any*) → [Connection](#sqlalchemy.engine.Connection)

Set non-SQL options for the connection which take effect
during execution.

This method modifies this [Connection](#sqlalchemy.engine.Connection) **in-place**;
the return value is the same [Connection](#sqlalchemy.engine.Connection) object
upon which the method is called.   Note that this is in contrast
to the behavior of the `execution_options` methods on other
objects such as [Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options) and
[Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options).  The rationale is that many
such execution options necessarily modify the state of the base
DBAPI connection in any case so there is no feasible means of
keeping the effect of such an option localized to a “sub” connection.

Changed in version 2.0: The [Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options)
method, in contrast to other objects with this method, modifies
the connection in-place without creating copy of it.

As discussed elsewhere, the [Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options)
method accepts any arbitrary parameters including user defined names.
All parameters given are consumable in a number of ways including
by using the [Connection.get_execution_options()](#sqlalchemy.engine.Connection.get_execution_options) method.
See the examples at [Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options)
and [Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options).

The keywords that are currently recognized by SQLAlchemy itself
include all those listed under [Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options),
as well as others that are specific to [Connection](#sqlalchemy.engine.Connection).

  Parameters:

- **compiled_cache** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Engine](#sqlalchemy.engine.Engine).
  A dictionary where [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) objects
  will be cached when the [Connection](#sqlalchemy.engine.Connection)
  compiles a clause
  expression into a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  This dictionary will
  supersede the statement cache that may be configured on the
  [Engine](#sqlalchemy.engine.Engine) itself.   If set to None, caching
  is disabled, even if the engine has a configured cache size.
  Note that the ORM makes use of its own “compiled” caches for
  some operations, including flush operations.  The caching
  used by the ORM internally supersedes a cache dictionary
  specified here.
- **logging_token** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Engine](#sqlalchemy.engine.Engine), [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable).
  Adds the specified string token surrounded by brackets in log
  messages logged by the connection, i.e. the logging that’s enabled
  either via the [create_engine.echo](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo) flag or via the
  `logging.getLogger("sqlalchemy.engine")` logger. This allows a
  per-connection or per-sub-engine token to be available which is
  useful for debugging concurrent connection scenarios.
  Added in version 1.4.0b2.
  See also
  [Setting Per-Connection / Sub-Engine Tokens](https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging-tokens) - usage example
  [create_engine.logging_name](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.logging_name) - adds a name to the
  name used by the Python logger object itself.
- **isolation_level** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Engine](#sqlalchemy.engine.Engine).
  Set the transaction isolation level for the lifespan of this
  [Connection](#sqlalchemy.engine.Connection) object.
  Valid values include those string
  values accepted by the [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level)
  parameter passed to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).  These levels are
  semi-database specific; see individual dialect documentation for
  valid levels.
  The isolation level option applies the isolation level by emitting
  statements on the DBAPI connection, and **necessarily affects the
  original Connection object overall**. The isolation level will remain
  at the given setting until explicitly changed, or when the DBAPI
  connection itself is [released](https://docs.sqlalchemy.org/en/20/glossary.html#term-released) to the connection pool, i.e. the
  [Connection.close()](#sqlalchemy.engine.Connection.close) method is called, at which time an
  event handler will emit additional statements on the DBAPI connection
  in order to revert the isolation level change.
  Note
  The `isolation_level` execution option may only be
  established before the [Connection.begin()](#sqlalchemy.engine.Connection.begin) method is
  called, as well as before any SQL statements are emitted which
  would otherwise trigger “autobegin”, or directly after a call to
  [Connection.commit()](#sqlalchemy.engine.Connection.commit) or
  [Connection.rollback()](#sqlalchemy.engine.Connection.rollback). A database cannot change the
  isolation level on a transaction in progress.
  Note
  The `isolation_level` execution option is implicitly
  reset if the [Connection](#sqlalchemy.engine.Connection) is invalidated, e.g. via
  the [Connection.invalidate()](#sqlalchemy.engine.Connection.invalidate) method, or if a
  disconnection error occurs. The new connection produced after the
  invalidation will **not** have the selected isolation level
  re-applied to it automatically.
  See also
  [Setting Transaction Isolation Levels including DBAPI Autocommit](#dbapi-autocommit)
  [Connection.get_isolation_level()](#sqlalchemy.engine.Connection.get_isolation_level)
  - view current actual level
- **no_parameters** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable).
  When `True`, if the final parameter
  list or dictionary is totally empty, will invoke the
  statement on the cursor as `cursor.execute(statement)`,
  not passing the parameter collection at all.
  Some DBAPIs such as psycopg2 and mysql-python consider
  percent signs as significant only when parameters are
  present; this option allows code to generate SQL
  containing percent signs (and possibly other characters)
  that is neutral regarding whether it’s executed by the DBAPI
  or piped into a script that’s later invoked by
  command line tools.
- **stream_results** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable).
  Indicate to the dialect that results should be “streamed” and not
  pre-buffered, if possible.  For backends such as PostgreSQL, MySQL
  and MariaDB, this indicates the use of a “server side cursor” as
  opposed to a client side cursor.  Other backends such as that of
  Oracle Database may already use server side cursors by default.
  The usage of
  [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results) is
  usually combined with setting a fixed number of rows to to be fetched
  in batches, to allow for efficient iteration of database rows while
  at the same time not loading all result rows into memory at once;
  this can be configured on a [Result](#sqlalchemy.engine.Result) object using the
  [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method, after execution has
  returned a new [Result](#sqlalchemy.engine.Result).   If
  [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) is not used,
  the [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
  mode of operation will instead use a dynamically sized buffer
  which buffers sets of rows at a time, growing on each batch
  based on a fixed growth size up until a limit which may
  be configured using the
  [Connection.execution_options.max_row_buffer](#sqlalchemy.engine.Connection.execution_options.params.max_row_buffer)
  parameter.
  When using the ORM to fetch ORM mapped objects from a result,
  [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) should always be used with
  [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results),
  so that the ORM does not fetch all rows into new ORM objects at once.
  For typical use, the
  [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per) execution
  option should be preferred, which sets up both
  [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results) and
  [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) at once. This option is supported
  both at a core level by [Connection](#sqlalchemy.engine.Connection) as well as by the
  ORM `Session`; the latter is described at
  [Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per).
  See also
  [Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - background on
  [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
  [Connection.execution_options.max_row_buffer](#sqlalchemy.engine.Connection.execution_options.params.max_row_buffer)
  [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
  [Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
  describing the ORM version of `yield_per`
- **max_row_buffer** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable).  Sets a maximum
  buffer size to use when the
  [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
  execution option is used on a backend that supports server side
  cursors.  The default value if not specified is 1000.
  See also
  [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
  [Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results)
- **yield_per** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable).  Integer value applied which will
  set the [Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
  execution option and invoke [Result.yield_per()](#sqlalchemy.engine.Result.yield_per)
  automatically at once.  Allows equivalent functionality as
  is present when using this parameter with the ORM.
  Added in version 1.4.40.
  See also
  [Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - background and examples
  on using server side cursors with Core.
  [Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
  describing the ORM version of `yield_per`
- **insertmanyvalues_page_size** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Engine](#sqlalchemy.engine.Engine). Number of rows to format into an
  INSERT statement when the statement uses “insertmanyvalues” mode,
  which is a paged form of bulk insert that is used for many backends
  when using [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany) execution typically in conjunction
  with RETURNING. Defaults to 1000. May also be modified on a
  per-engine basis using the
  [create_engine.insertmanyvalues_page_size](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.insertmanyvalues_page_size) parameter.
  Added in version 2.0.
  See also
  [“Insert Many Values” Behavior for INSERT statements](#engine-insertmanyvalues)
- **schema_translate_map** –
  Available on: [Connection](#sqlalchemy.engine.Connection),
  [Engine](#sqlalchemy.engine.Engine), [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable).
  A dictionary mapping schema names to schema names, that will be
  applied to the [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) element of each
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  encountered when SQL or DDL expression elements
  are compiled into strings; the resulting schema name will be
  converted based on presence in the map of the original name.
  See also
  [Translation of Schema Names](#schema-translating)
- **preserve_rowcount** –
  Boolean; when True, the `cursor.rowcount`
  attribute will be unconditionally memoized within the result and
  made available via the [CursorResult.rowcount](#sqlalchemy.engine.CursorResult.rowcount) attribute.
  Normally, this attribute is only preserved for UPDATE and DELETE
  statements.  Using this option, the DBAPIs rowcount value can
  be accessed for other kinds of statements such as INSERT and SELECT,
  to the degree that the DBAPI supports these statements.  See
  [CursorResult.rowcount](#sqlalchemy.engine.CursorResult.rowcount) for notes regarding the behavior
  of this attribute.
  Added in version 2.0.28.

See also

[Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options)

[Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options)

[Connection.get_execution_options()](#sqlalchemy.engine.Connection.get_execution_options)

[ORM Execution Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-execution-options) - documentation on all
ORM-specific execution options

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)get_execution_options() → _ExecuteOptions

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

See also

[Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options)

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)get_isolation_level() → Literal['SERIALIZABLE', 'REPEATABLE READ', 'READ COMMITTED', 'READ UNCOMMITTED', 'AUTOCOMMIT']

Return the current **actual** isolation level that’s present on
the database within the scope of this connection.

This attribute will perform a live SQL operation against the database
in order to procure the current isolation level, so the value returned
is the actual level on the underlying DBAPI connection regardless of
how this state was set. This will be one of the four actual isolation
modes `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`,
`SERIALIZABLE`. It will **not** include the `AUTOCOMMIT` isolation
level setting. Third party dialects may also feature additional
isolation level settings.

Note

This method **will not report** on the `AUTOCOMMIT`
isolation level, which is a separate [dbapi](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) setting that’s
independent of **actual** isolation level.  When `AUTOCOMMIT` is
in use, the database connection still has a “traditional” isolation
mode in effect, that is typically one of the four values
`READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`,
`SERIALIZABLE`.

Compare to the [Connection.default_isolation_level](#sqlalchemy.engine.Connection.default_isolation_level)
accessor which returns the isolation level that is present on the
database at initial connection time.

See also

[Connection.default_isolation_level](#sqlalchemy.engine.Connection.default_isolation_level)
- view default level

[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level)
- set per [Engine](#sqlalchemy.engine.Engine) isolation level

[Connection.execution_options.isolation_level](#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
- set per [Connection](#sqlalchemy.engine.Connection) isolation level

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)get_nested_transaction() → [NestedTransaction](#sqlalchemy.engine.NestedTransaction) | None

Return the current nested transaction in progress, if any.

Added in version 1.4.

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)get_transaction() → [RootTransaction](#sqlalchemy.engine.RootTransaction) | None

Return the current root transaction in progress, if any.

Added in version 1.4.

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)in_nested_transaction() → bool

Return True if a transaction is in progress.

    method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)in_transaction() → bool

Return True if a transaction is in progress.

    property info: _InfoType

Info dictionary associated with the underlying DBAPI connection
referred to by this [Connection](#sqlalchemy.engine.Connection), allowing user-defined
data to be associated with the connection.

The data here will follow along with the DBAPI connection including
after it is returned to the connection pool and used again
in subsequent instances of [Connection](#sqlalchemy.engine.Connection).

    method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)invalidate(*exception:BaseException|None=None*) → None

Invalidate the underlying DBAPI connection associated with
this [Connection](#sqlalchemy.engine.Connection).

An attempt will be made to close the underlying DBAPI connection
immediately; however if this operation fails, the error is logged
but not raised.  The connection is then discarded whether or not
close() succeeded.

Upon the next use (where “use” typically means using the
[Connection.execute()](#sqlalchemy.engine.Connection.execute) method or similar),
this [Connection](#sqlalchemy.engine.Connection) will attempt to
procure a new DBAPI connection using the services of the
[Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) as a source of connectivity (e.g.
a “reconnection”).

If a transaction was in progress (e.g. the
[Connection.begin()](#sqlalchemy.engine.Connection.begin) method has been called) when
[Connection.invalidate()](#sqlalchemy.engine.Connection.invalidate) method is called, at the DBAPI
level all state associated with this transaction is lost, as
the DBAPI connection is closed.  The [Connection](#sqlalchemy.engine.Connection)
will not allow a reconnection to proceed until the
[Transaction](#sqlalchemy.engine.Transaction) object is ended, by calling the
[Transaction.rollback()](#sqlalchemy.engine.Transaction.rollback) method; until that point, any attempt at
continuing to use the [Connection](#sqlalchemy.engine.Connection) will raise an
[InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError).
This is to prevent applications from accidentally
continuing an ongoing transactional operations despite the
fact that the transaction has been lost due to an
invalidation.

The [Connection.invalidate()](#sqlalchemy.engine.Connection.invalidate) method,
just like auto-invalidation,
will at the connection pool level invoke the
[PoolEvents.invalidate()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.invalidate) event.

  Parameters:

**exception** – an optional `Exception` instance that’s the
reason for the invalidation.  is passed along to event handlers
and logging functions.

See also

[More on Invalidation](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-connection-invalidation)

     property invalidated: bool

Return True if this connection was invalidated.

This does not indicate whether or not the connection was
invalidated at the pool level, however

    method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)rollback() → None

Roll back the transaction that is currently in progress.

This method rolls back the current transaction if one has been started.
If no transaction was started, the method has no effect.  If a
transaction was started and the connection is in an invalidated state,
the transaction is cleared using this method.

A transaction is begun on a [Connection](#sqlalchemy.engine.Connection) automatically
whenever a statement is first executed, or when the
[Connection.begin()](#sqlalchemy.engine.Connection.begin) method is called.

Note

The [Connection.rollback()](#sqlalchemy.engine.Connection.rollback) method only acts
upon the primary database transaction that is linked to the
[Connection](#sqlalchemy.engine.Connection) object.  It does not operate upon a
SAVEPOINT that would have been invoked from the
[Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested) method; for control of a
SAVEPOINT, call [NestedTransaction.rollback()](#sqlalchemy.engine.NestedTransaction.rollback) on the
[NestedTransaction](#sqlalchemy.engine.NestedTransaction) that is returned by the
[Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested) method itself.

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)scalar(*statement:Executable*, *parameters:_CoreSingleExecuteParams|None=None*, ***, *execution_options:CoreExecuteOptionsParameter|None=None*) → Any

Executes a SQL statement construct and returns a scalar object.

This method is shorthand for invoking the
[Result.scalar()](#sqlalchemy.engine.Result.scalar) method after invoking the
[Connection.execute()](#sqlalchemy.engine.Connection.execute) method.  Parameters are equivalent.

  Returns:

a scalar Python value representing the first column of the
first row returned.

      method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)scalars(*statement:Executable*, *parameters:_CoreAnyExecuteParams|None=None*, ***, *execution_options:CoreExecuteOptionsParameter|None=None*) → [ScalarResult](#sqlalchemy.engine.ScalarResult)[Any]

Executes and returns a scalar result set, which yields scalar values
from the first column of each row.

This method is equivalent to calling [Connection.execute()](#sqlalchemy.engine.Connection.execute)
to receive a [Result](#sqlalchemy.engine.Result) object, then invoking the
[Result.scalars()](#sqlalchemy.engine.Result.scalars) method to produce a
[ScalarResult](#sqlalchemy.engine.ScalarResult) instance.

  Returns:

a [ScalarResult](#sqlalchemy.engine.ScalarResult)

Added in version 1.4.24.

     method [sqlalchemy.engine.Connection.](#sqlalchemy.engine.Connection)schema_for_object(*obj:HasSchemaAttr*) → str | None

Return the schema name for the given schema item taking into
account current schema translate map.

     class sqlalchemy.engine.CreateEnginePlugin

A set of hooks intended to augment the construction of an
[Engine](#sqlalchemy.engine.Engine) object based on entrypoint names in a URL.

The purpose of [CreateEnginePlugin](#sqlalchemy.engine.CreateEnginePlugin) is to allow third-party
systems to apply engine, pool and dialect level event listeners without
the need for the target application to be modified; instead, the plugin
names can be added to the database URL.  Target applications for
[CreateEnginePlugin](#sqlalchemy.engine.CreateEnginePlugin) include:

- connection and SQL performance tools, e.g. which use events to track
  number of checkouts and/or time spent with statements
- connectivity plugins such as proxies

A rudimentary [CreateEnginePlugin](#sqlalchemy.engine.CreateEnginePlugin) that attaches a logger
to an [Engine](#sqlalchemy.engine.Engine) object might look like:

```
import logging

from sqlalchemy.engine import CreateEnginePlugin
from sqlalchemy import event

class LogCursorEventsPlugin(CreateEnginePlugin):
    def __init__(self, url, kwargs):
        # consume the parameter "log_cursor_logging_name" from the
        # URL query
        logging_name = url.query.get(
            "log_cursor_logging_name", "log_cursor"
        )

        self.log = logging.getLogger(logging_name)

    def update_url(self, url):
        "update the URL to one that no longer includes our parameters"
        return url.difference_update_query(["log_cursor_logging_name"])

    def engine_created(self, engine):
        "attach an event listener after the new Engine is constructed"
        event.listen(engine, "before_cursor_execute", self._log_event)

    def _log_event(
        self,
        conn,
        cursor,
        statement,
        parameters,
        context,
        executemany,
    ):

        self.log.info("Plugin logged cursor event: %s", statement)
```

Plugins are registered using entry points in a similar way as that
of dialects:

```
entry_points = {
    "sqlalchemy.plugins": [
        "log_cursor_plugin = myapp.plugins:LogCursorEventsPlugin"
    ]
}
```

A plugin that uses the above names would be invoked from a database
URL as in:

```
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://scott:tiger@localhost/test?"
    "plugin=log_cursor_plugin&log_cursor_logging_name=mylogger"
)
```

The `plugin` URL parameter supports multiple instances, so that a URL
may specify multiple plugins; they are loaded in the order stated
in the URL:

```
engine = create_engine(
    "mysql+pymysql://scott:tiger@localhost/test?"
    "plugin=plugin_one&plugin=plugin_twp&plugin=plugin_three"
)
```

The plugin names may also be passed directly to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
using the [create_engine.plugins](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.plugins) argument:

```
engine = create_engine(
    "mysql+pymysql://scott:tiger@localhost/test", plugins=["myplugin"]
)
```

Added in version 1.2.3: plugin names can also be specified
to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) as a list

A plugin may consume plugin-specific arguments from the
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object as well as the `kwargs` dictionary, which is
the dictionary of arguments passed to the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
call.  “Consuming” these arguments includes that they must be removed
when the plugin initializes, so that the arguments are not passed along
to the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) constructor, where they will raise an
[ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) because they are not known by the dialect.

As of version 1.4 of SQLAlchemy, arguments should continue to be consumed
from the `kwargs` dictionary directly, by removing the values with a
method such as `dict.pop`. Arguments from the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object
should be consumed by implementing the
[CreateEnginePlugin.update_url()](#sqlalchemy.engine.CreateEnginePlugin.update_url) method, returning a new copy
of the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) with plugin-specific parameters removed:

```
class MyPlugin(CreateEnginePlugin):
    def __init__(self, url, kwargs):
        self.my_argument_one = url.query["my_argument_one"]
        self.my_argument_two = url.query["my_argument_two"]
        self.my_argument_three = kwargs.pop("my_argument_three", None)

    def update_url(self, url):
        return url.difference_update_query(
            ["my_argument_one", "my_argument_two"]
        )
```

Arguments like those illustrated above would be consumed from a
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) call such as:

```
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://scott:tiger@localhost/test?"
    "plugin=myplugin&my_argument_one=foo&my_argument_two=bar",
    my_argument_three="bat",
)
```

Changed in version 1.4: The [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object is now immutable; a
[CreateEnginePlugin](#sqlalchemy.engine.CreateEnginePlugin) that needs to alter the
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) should implement the newly added
[CreateEnginePlugin.update_url()](#sqlalchemy.engine.CreateEnginePlugin.update_url) method, which
is invoked after the plugin is constructed.

For migration, construct the plugin in the following way, checking
for the existence of the [CreateEnginePlugin.update_url()](#sqlalchemy.engine.CreateEnginePlugin.update_url)
method to detect which version is running:

```
class MyPlugin(CreateEnginePlugin):
    def __init__(self, url, kwargs):
        if hasattr(CreateEnginePlugin, "update_url"):
            # detect the 1.4 API
            self.my_argument_one = url.query["my_argument_one"]
            self.my_argument_two = url.query["my_argument_two"]
        else:
            # detect the 1.3 and earlier API - mutate the
            # URL directly
            self.my_argument_one = url.query.pop("my_argument_one")
            self.my_argument_two = url.query.pop("my_argument_two")

        self.my_argument_three = kwargs.pop("my_argument_three", None)

    def update_url(self, url):
        # this method is only called in the 1.4 version
        return url.difference_update_query(
            ["my_argument_one", "my_argument_two"]
        )
```

See also

[The URL object is now immutable](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-5526) - overview of the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) change which
also includes notes regarding [CreateEnginePlugin](#sqlalchemy.engine.CreateEnginePlugin).

When the engine creation process completes and produces the
[Engine](#sqlalchemy.engine.Engine) object, it is again passed to the plugin via the
[CreateEnginePlugin.engine_created()](#sqlalchemy.engine.CreateEnginePlugin.engine_created) hook.  In this hook, additional
changes can be made to the engine, most typically involving setup of
events (e.g. those defined in [Core Events](https://docs.sqlalchemy.org/en/20/core/events.html)).

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newCreateEnginePlugin. |
| engine_created() | Receive theEngineobject when it is fully constructed. |
| handle_dialect_kwargs() | parse and modify dialect kwargs |
| handle_pool_kwargs() | parse and modify pool kwargs |
| update_url() | Update theURL. |

   method [sqlalchemy.engine.CreateEnginePlugin.](#sqlalchemy.engine.CreateEnginePlugin)__init__(*url:URL*, *kwargs:Dict[str,Any]*)

Construct a new [CreateEnginePlugin](#sqlalchemy.engine.CreateEnginePlugin).

The plugin object is instantiated individually for each call
to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).  A single `
Engine` will be
passed to the [CreateEnginePlugin.engine_created()](#sqlalchemy.engine.CreateEnginePlugin.engine_created) method
corresponding to this URL.

  Parameters:

- **url** –
  the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object.  The plugin may inspect
  the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) for arguments.  Arguments used by the
  plugin should be removed, by returning an updated [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL)
  from the [CreateEnginePlugin.update_url()](#sqlalchemy.engine.CreateEnginePlugin.update_url) method.
  Changed in version 1.4: The [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object is now immutable, so a
  [CreateEnginePlugin](#sqlalchemy.engine.CreateEnginePlugin) that needs to alter the
  [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object should implement the
  [CreateEnginePlugin.update_url()](#sqlalchemy.engine.CreateEnginePlugin.update_url) method.
- **kwargs** – The keyword arguments passed to
  [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).

      method [sqlalchemy.engine.CreateEnginePlugin.](#sqlalchemy.engine.CreateEnginePlugin)engine_created(*engine:Engine*) → None

Receive the [Engine](#sqlalchemy.engine.Engine)
object when it is fully constructed.

The plugin may make additional changes to the engine, such as
registering engine or connection pool events.

    method [sqlalchemy.engine.CreateEnginePlugin.](#sqlalchemy.engine.CreateEnginePlugin)handle_dialect_kwargs(*dialect_cls:Type[Dialect]*, *dialect_args:Dict[str,Any]*) → None

parse and modify dialect kwargs

    method [sqlalchemy.engine.CreateEnginePlugin.](#sqlalchemy.engine.CreateEnginePlugin)handle_pool_kwargs(*pool_cls:Type[Pool]*, *pool_args:Dict[str,Any]*) → None

parse and modify pool kwargs

    method [sqlalchemy.engine.CreateEnginePlugin.](#sqlalchemy.engine.CreateEnginePlugin)update_url(*url:URL*) → [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL)

Update the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL).

A new [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) should be returned.   This method is
typically used to consume configuration arguments from the
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) which must be removed, as they will not be
recognized by the dialect.  The
[URL.difference_update_query()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.difference_update_query) method is available
to remove these arguments.   See the docstring at
[CreateEnginePlugin](#sqlalchemy.engine.CreateEnginePlugin) for an example.

Added in version 1.4.

      class sqlalchemy.engine.Engine

*inherits from* `sqlalchemy.engine.interfaces.ConnectionEventsTarget`, [sqlalchemy.log.Identified](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.log.Identified), `sqlalchemy.inspection.Inspectable`

Connects a [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) and
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) together to provide a
source of database connectivity and behavior.

An [Engine](#sqlalchemy.engine.Engine) object is instantiated publicly using the
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) function.

See also

[Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html)

[Working with Engines and Connections](#)

| Member Name | Description |
| --- | --- |
| begin() | Return a context manager delivering aConnectionwith aTransactionestablished. |
| clear_compiled_cache() | Clear the compiled cache associated with the dialect. |
| connect() | Return a newConnectionobject. |
| dispose() | Dispose of the connection pool used by thisEngine. |
| execution_options() | Return a newEnginethat will provideConnectionobjects with the given execution options. |
| get_execution_options() | Get the non-SQL options which will take effect during execution. |
| raw_connection() | Return a “raw” DBAPI connection from the connection pool. |
| update_execution_options() | Update the default execution_options dictionary
of thisEngine. |

   method [sqlalchemy.engine.Engine.](#sqlalchemy.engine.Engine)begin() → Iterator[[Connection](#sqlalchemy.engine.Connection)]

Return a context manager delivering a [Connection](#sqlalchemy.engine.Connection)
with a [Transaction](#sqlalchemy.engine.Transaction) established.

E.g.:

```
with engine.begin() as conn:
    conn.execute(text("insert into table (x, y, z) values (1, 2, 3)"))
    conn.execute(text("my_special_procedure(5)"))
```

Upon successful operation, the [Transaction](#sqlalchemy.engine.Transaction)
is committed.  If an error is raised, the [Transaction](#sqlalchemy.engine.Transaction)
is rolled back.

See also

[Engine.connect()](#sqlalchemy.engine.Engine.connect) - procure a
[Connection](#sqlalchemy.engine.Connection) from
an [Engine](#sqlalchemy.engine.Engine).

[Connection.begin()](#sqlalchemy.engine.Connection.begin) - start a [Transaction](#sqlalchemy.engine.Transaction)
for a particular [Connection](#sqlalchemy.engine.Connection).

     method [sqlalchemy.engine.Engine.](#sqlalchemy.engine.Engine)clear_compiled_cache() → None

Clear the compiled cache associated with the dialect.

This applies **only** to the built-in cache that is established
via the `create_engine.query_cache_size` parameter.
It will not impact any dictionary caches that were passed via the
[Connection.execution_options.compiled_cache](#sqlalchemy.engine.Connection.execution_options.params.compiled_cache) parameter.

Added in version 1.4.

     method [sqlalchemy.engine.Engine.](#sqlalchemy.engine.Engine)connect() → [Connection](#sqlalchemy.engine.Connection)

Return a new [Connection](#sqlalchemy.engine.Connection) object.

The [Connection](#sqlalchemy.engine.Connection) acts as a Python context manager, so
the typical use of this method looks like:

```
with engine.connect() as connection:
    connection.execute(text("insert into table values ('foo')"))
    connection.commit()
```

Where above, after the block is completed, the connection is “closed”
and its underlying DBAPI resources are returned to the connection pool.
This also has the effect of rolling back any transaction that
was explicitly begun or was begun via autobegin, and will
emit the [ConnectionEvents.rollback()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.rollback) event if one was
started and is still in progress.

See also

[Engine.begin()](#sqlalchemy.engine.Engine.begin)

     method [sqlalchemy.engine.Engine.](#sqlalchemy.engine.Engine)dispose(*close:bool=True*) → None

Dispose of the connection pool used by this
[Engine](#sqlalchemy.engine.Engine).

A new connection pool is created immediately after the old one has been
disposed. The previous connection pool is disposed either actively, by
closing out all currently checked-in connections in that pool, or
passively, by losing references to it but otherwise not closing any
connections. The latter strategy is more appropriate for an initializer
in a forked Python process.

Event listeners associated with the old pool via [PoolEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents)
are **transferred to the new pool**; this is to support the pattern
by which [PoolEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents) are set up in terms of the owning
[Engine](#sqlalchemy.engine.Engine) without the need to refer to the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
directly.

  Parameters:

**close** –

if left at its default of `True`, has the
effect of fully closing all **currently checked in**
database connections.  Connections that are still checked out
will **not** be closed, however they will no longer be associated
with this [Engine](#sqlalchemy.engine.Engine),
so when they are closed individually, eventually the
[Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) which they are associated with will
be garbage collected and they will be closed out fully, if
not already closed on checkin.

If set to `False`, the previous connection pool is de-referenced,
and otherwise not touched in any way.

Added in version 1.4.33: Added the [Engine.dispose.close](#sqlalchemy.engine.Engine.dispose.params.close)
parameter to allow the replacement of a connection pool in a child
process without interfering with the connections used by the parent
process.

See also

[Engine Disposal](#engine-disposal)

[Using Connection Pools with Multiprocessing or os.fork()](https://docs.sqlalchemy.org/en/20/core/pooling.html#pooling-multiprocessing)

[ConnectionEvents.engine_disposed()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.engine_disposed)

     property driver: str

Driver name of the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect)
in use by this [Engine](#sqlalchemy.engine.Engine).

    property engine: [Engine](#sqlalchemy.engine.Engine)

Returns this [Engine](#sqlalchemy.engine.Engine).

Used for legacy schemes that accept [Connection](#sqlalchemy.engine.Connection) /
[Engine](#sqlalchemy.engine.Engine) objects within the same variable.

    method [sqlalchemy.engine.Engine.](#sqlalchemy.engine.Engine)execution_options(***opt:Any*) → OptionEngine

Return a new [Engine](#sqlalchemy.engine.Engine) that will provide
[Connection](#sqlalchemy.engine.Connection) objects with the given execution options.

The returned [Engine](#sqlalchemy.engine.Engine) remains related to the original
[Engine](#sqlalchemy.engine.Engine) in that it shares the same connection pool and
other state:

- The [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) used by the new [Engine](#sqlalchemy.engine.Engine)
  is the
  same instance.  The [Engine.dispose()](#sqlalchemy.engine.Engine.dispose)
  method will replace
  the connection pool instance for the parent engine as well
  as this one.
- Event listeners are “cascaded” - meaning, the new
  [Engine](#sqlalchemy.engine.Engine)
  inherits the events of the parent, and new events can be associated
  with the new [Engine](#sqlalchemy.engine.Engine) individually.
- The logging configuration and logging_name is copied from the parent
  [Engine](#sqlalchemy.engine.Engine).

The intent of the [Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options) method is
to implement schemes where multiple [Engine](#sqlalchemy.engine.Engine)
objects refer to the same connection pool, but are differentiated
by options that affect some execution-level behavior for each
engine.    One such example is breaking into separate “reader” and
“writer” [Engine](#sqlalchemy.engine.Engine) instances, where one
[Engine](#sqlalchemy.engine.Engine)
has a lower [isolation level](https://docs.sqlalchemy.org/en/20/glossary.html#term-isolation-level) setting configured or is even
transaction-disabled using “autocommit”.  An example of this
configuration is at [Maintaining Multiple Isolation Levels for a Single Engine](#dbapi-autocommit-multiple).

Another example is one that
uses a custom option `shard_id` which is consumed by an event
to change the current schema on a database connection:

```
from sqlalchemy import event
from sqlalchemy.engine import Engine

primary_engine = create_engine("mysql+mysqldb://")
shard1 = primary_engine.execution_options(shard_id="shard1")
shard2 = primary_engine.execution_options(shard_id="shard2")

shards = {"default": "base", "shard_1": "db1", "shard_2": "db2"}

@event.listens_for(Engine, "before_cursor_execute")
def _switch_shard(conn, cursor, stmt, params, context, executemany):
    shard_id = conn.get_execution_options().get("shard_id", "default")
    current_shard = conn.info.get("current_shard", None)

    if current_shard != shard_id:
        cursor.execute("use %s" % shards[shard_id])
        conn.info["current_shard"] = shard_id
```

The above recipe illustrates two [Engine](#sqlalchemy.engine.Engine) objects that
will each serve as factories for [Connection](#sqlalchemy.engine.Connection) objects
that have pre-established “shard_id” execution options present. A
[ConnectionEvents.before_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute) event handler
then interprets this execution option to emit a MySQL `use` statement
to switch databases before a statement execution, while at the same
time keeping track of which database we’ve established using the
[Connection.info](#sqlalchemy.engine.Connection.info) dictionary.

See also

[Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options)
- update execution options
on a [Connection](#sqlalchemy.engine.Connection) object.

[Engine.update_execution_options()](#sqlalchemy.engine.Engine.update_execution_options)
- update the execution
options for a given [Engine](#sqlalchemy.engine.Engine) in place.

[Engine.get_execution_options()](#sqlalchemy.engine.Engine.get_execution_options)

     method [sqlalchemy.engine.Engine.](#sqlalchemy.engine.Engine)get_execution_options() → _ExecuteOptions

Get the non-SQL options which will take effect during execution.

See also

[Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options)

     property name: str

String name of the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect)
in use by this [Engine](#sqlalchemy.engine.Engine).

    method [sqlalchemy.engine.Engine.](#sqlalchemy.engine.Engine)raw_connection() → [PoolProxiedConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection)

Return a “raw” DBAPI connection from the connection pool.

The returned object is a proxied version of the DBAPI
connection object used by the underlying driver in use.
The object will have all the same behavior as the real DBAPI
connection, except that its `close()` method will result in the
connection being returned to the pool, rather than being closed
for real.

This method provides direct DBAPI connection access for
special situations when the API provided by
[Connection](#sqlalchemy.engine.Connection)
is not needed.   When a [Connection](#sqlalchemy.engine.Connection) object is already
present, the DBAPI connection is available using
the [Connection.connection](#sqlalchemy.engine.Connection.connection) accessor.

See also

[Working with Driver SQL and Raw DBAPI Connections](#dbapi-connections)

     method [sqlalchemy.engine.Engine.](#sqlalchemy.engine.Engine)update_execution_options(***opt:Any*) → None

Update the default execution_options dictionary
of this [Engine](#sqlalchemy.engine.Engine).

The given keys/values in **opt are added to the
default execution options that will be used for
all connections.  The initial contents of this dictionary
can be sent via the `execution_options` parameter
to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).

See also

[Connection.execution_options()](#sqlalchemy.engine.Connection.execution_options)

[Engine.execution_options()](#sqlalchemy.engine.Engine.execution_options)

      class sqlalchemy.engine.ExceptionContext

Encapsulate information about an error condition in progress.

This object exists solely to be passed to the
[DialectEvents.handle_error()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.handle_error) event,
supporting an interface that
can be extended without backwards-incompatibility.

| Member Name | Description |
| --- | --- |
| chained_exception | The exception that was returned by the previous handler in the
exception chain, if any. |
| connection | TheConnectionin use during the exception. |
| cursor | The DBAPI cursor object. |
| dialect | TheDialectin use. |
| engine | TheEnginein use during the exception. |
| execution_context | TheExecutionContextcorresponding to the execution
operation in progress. |
| invalidate_pool_on_disconnect | Represent whether all connections in the pool should be invalidated
when a “disconnect” condition is in effect. |
| is_disconnect | Represent whether the exception as occurred represents a “disconnect”
condition. |
| is_pre_ping | Indicates if this error is occurring within the “pre-ping” step
performed whencreate_engine.pool_pre_pingis set toTrue.  In this mode, theExceptionContext.engineattribute
will beNone.  The dialect in use is accessible via theExceptionContext.dialectattribute. |
| original_exception | The exception object which was caught. |
| parameters | Parameter collection that was emitted directly to the DBAPI. |
| sqlalchemy_exception | Thesqlalchemy.exc.StatementErrorwhich wraps the original,
and will be raised if exception handling is not circumvented by the event. |
| statement | String SQL statement that was emitted directly to the DBAPI. |

   attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)chained_exception: BaseException | None

The exception that was returned by the previous handler in the
exception chain, if any.

If present, this exception will be the one ultimately raised by
SQLAlchemy unless a subsequent handler replaces it.

May be None.

    attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)connection: [Connection](#sqlalchemy.engine.Connection) | None

The [Connection](#sqlalchemy.engine.Connection) in use during the exception.

This member is present, except in the case of a failure when
first connecting.

See also

[ExceptionContext.engine](#sqlalchemy.engine.ExceptionContext.engine)

     attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)cursor: [DBAPICursor](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPICursor) | None

The DBAPI cursor object.

May be None.

    attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)dialect: [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect)

The [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in use.

This member is present for all invocations of the event hook.

Added in version 2.0.

     attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)engine: [Engine](#sqlalchemy.engine.Engine) | None

The [Engine](#sqlalchemy.engine.Engine) in use during the exception.

This member is present in all cases except for when handling an error
within the connection pool “pre-ping” process.

    attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)execution_context: [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext) | None

The [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext) corresponding to the execution
operation in progress.

This is present for statement execution operations, but not for
operations such as transaction begin/end.  It also is not present when
the exception was raised before the [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext)
could be constructed.

Note that the [ExceptionContext.statement](#sqlalchemy.engine.ExceptionContext.statement) and
[ExceptionContext.parameters](#sqlalchemy.engine.ExceptionContext.parameters) members may represent a
different value than that of the [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext),
potentially in the case where a
[ConnectionEvents.before_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute) event or similar
modified the statement/parameters to be sent.

May be None.

    attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)invalidate_pool_on_disconnect: bool

Represent whether all connections in the pool should be invalidated
when a “disconnect” condition is in effect.

Setting this flag to False within the scope of the
[DialectEvents.handle_error()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.handle_error)
event will have the effect such
that the full collection of connections in the pool will not be
invalidated during a disconnect; only the current connection that is the
subject of the error will actually be invalidated.

The purpose of this flag is for custom disconnect-handling schemes where
the invalidation of other connections in the pool is to be performed
based on other conditions, or even on a per-connection basis.

    attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)is_disconnect: bool

Represent whether the exception as occurred represents a “disconnect”
condition.

This flag will always be True or False within the scope of the
[DialectEvents.handle_error()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.handle_error) handler.

SQLAlchemy will defer to this flag in order to determine whether or not
the connection should be invalidated subsequently.    That is, by
assigning to this flag, a “disconnect” event which then results in
a connection and pool invalidation can be invoked or prevented by
changing this flag.

Note

The pool “pre_ping” handler enabled using the
[create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) parameter does **not**
consult this event before deciding if the “ping” returned false,
as opposed to receiving an unhandled error.   For this use case, the
[legacy recipe based on engine_connect() may be used](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects-pessimistic-custom).  A future API allow more
comprehensive customization of the “disconnect” detection mechanism
across all functions.

     attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)is_pre_ping: bool

Indicates if this error is occurring within the “pre-ping” step
performed when [create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) is set to
`True`.  In this mode, the [ExceptionContext.engine](#sqlalchemy.engine.ExceptionContext.engine) attribute
will be `None`.  The dialect in use is accessible via the
[ExceptionContext.dialect](#sqlalchemy.engine.ExceptionContext.dialect) attribute.

Added in version 2.0.5.

     attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)original_exception: BaseException

The exception object which was caught.

This member is always present.

    attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)parameters: _DBAPIAnyExecuteParams | None

Parameter collection that was emitted directly to the DBAPI.

May be None.

    attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)sqlalchemy_exception: [StatementError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.StatementError) | None

The [sqlalchemy.exc.StatementError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.StatementError) which wraps the original,
and will be raised if exception handling is not circumvented by the event.

May be None, as not all exception types are wrapped by SQLAlchemy.
For DBAPI-level exceptions that subclass the dbapi’s Error class, this
field will always be present.

    attribute [sqlalchemy.engine.ExceptionContext.](#sqlalchemy.engine.ExceptionContext)statement: str | None

String SQL statement that was emitted directly to the DBAPI.

May be None.

     class sqlalchemy.engine.NestedTransaction

*inherits from* [sqlalchemy.engine.Transaction](#sqlalchemy.engine.Transaction)

Represent a ‘nested’, or SAVEPOINT transaction.

The [NestedTransaction](#sqlalchemy.engine.NestedTransaction) object is created by calling the
[Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested) method of
[Connection](#sqlalchemy.engine.Connection).

When using [NestedTransaction](#sqlalchemy.engine.NestedTransaction), the semantics of “begin” /
“commit” / “rollback” are as follows:

- the “begin” operation corresponds to the “BEGIN SAVEPOINT” command, where
  the savepoint is given an explicit name that is part of the state
  of this object.
- The [NestedTransaction.commit()](#sqlalchemy.engine.NestedTransaction.commit) method corresponds to a
  “RELEASE SAVEPOINT” operation, using the savepoint identifier associated
  with this [NestedTransaction](#sqlalchemy.engine.NestedTransaction).
- The [NestedTransaction.rollback()](#sqlalchemy.engine.NestedTransaction.rollback) method corresponds to a
  “ROLLBACK TO SAVEPOINT” operation, using the savepoint identifier
  associated with this [NestedTransaction](#sqlalchemy.engine.NestedTransaction).

The rationale for mimicking the semantics of an outer transaction in
terms of savepoints so that code may deal with a “savepoint” transaction
and an “outer” transaction in an agnostic way.

See also

[Using SAVEPOINT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-begin-nested) - ORM version of the SAVEPOINT API.

| Member Name | Description |
| --- | --- |
| close() | Close thisTransaction. |
| commit() | Commit thisTransaction. |
| rollback() | Roll back thisTransaction. |

   method [sqlalchemy.engine.NestedTransaction.](#sqlalchemy.engine.NestedTransaction)close() → None

*inherited from the* [Transaction.close()](#sqlalchemy.engine.Transaction.close) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Close this [Transaction](#sqlalchemy.engine.Transaction).

If this transaction is the base transaction in a begin/commit
nesting, the transaction will rollback().  Otherwise, the
method returns.

This is used to cancel a Transaction without affecting the scope of
an enclosing transaction.

    method [sqlalchemy.engine.NestedTransaction.](#sqlalchemy.engine.NestedTransaction)commit() → None

*inherited from the* [Transaction.commit()](#sqlalchemy.engine.Transaction.commit) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Commit this [Transaction](#sqlalchemy.engine.Transaction).

The implementation of this may vary based on the type of transaction in
use:

- For a simple database transaction (e.g. [RootTransaction](#sqlalchemy.engine.RootTransaction)),
  it corresponds to a COMMIT.
- For a [NestedTransaction](#sqlalchemy.engine.NestedTransaction), it corresponds to a
  “RELEASE SAVEPOINT” operation.
- For a [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction), DBAPI-specific methods for two
  phase transactions may be used.

    method [sqlalchemy.engine.NestedTransaction.](#sqlalchemy.engine.NestedTransaction)rollback() → None

*inherited from the* [Transaction.rollback()](#sqlalchemy.engine.Transaction.rollback) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Roll back this [Transaction](#sqlalchemy.engine.Transaction).

The implementation of this may vary based on the type of transaction in
use:

- For a simple database transaction (e.g. [RootTransaction](#sqlalchemy.engine.RootTransaction)),
  it corresponds to a ROLLBACK.
- For a [NestedTransaction](#sqlalchemy.engine.NestedTransaction), it corresponds to a
  “ROLLBACK TO SAVEPOINT” operation.
- For a [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction), DBAPI-specific methods for two
  phase transactions may be used.

     class sqlalchemy.engine.RootTransaction

*inherits from* [sqlalchemy.engine.Transaction](#sqlalchemy.engine.Transaction)

Represent the “root” transaction on a [Connection](#sqlalchemy.engine.Connection).

This corresponds to the current “BEGIN/COMMIT/ROLLBACK” that’s occurring
for the [Connection](#sqlalchemy.engine.Connection). The [RootTransaction](#sqlalchemy.engine.RootTransaction)
is created by calling upon the [Connection.begin()](#sqlalchemy.engine.Connection.begin) method, and
remains associated with the [Connection](#sqlalchemy.engine.Connection) throughout its
active span. The current [RootTransaction](#sqlalchemy.engine.RootTransaction) in use is
accessible via the [Connection.get_transaction](#sqlalchemy.engine.Connection.get_transaction) method of
[Connection](#sqlalchemy.engine.Connection).

In [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) use, the [Connection](#sqlalchemy.engine.Connection) also employs
“autobegin” behavior that will create a new
[RootTransaction](#sqlalchemy.engine.RootTransaction) whenever a connection in a
non-transactional state is used to emit commands on the DBAPI connection.
The scope of the [RootTransaction](#sqlalchemy.engine.RootTransaction) in 2.0 style
use can be controlled using the [Connection.commit()](#sqlalchemy.engine.Connection.commit) and
[Connection.rollback()](#sqlalchemy.engine.Connection.rollback) methods.

| Member Name | Description |
| --- | --- |
| close() | Close thisTransaction. |
| commit() | Commit thisTransaction. |
| rollback() | Roll back thisTransaction. |

   method [sqlalchemy.engine.RootTransaction.](#sqlalchemy.engine.RootTransaction)close() → None

*inherited from the* [Transaction.close()](#sqlalchemy.engine.Transaction.close) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Close this [Transaction](#sqlalchemy.engine.Transaction).

If this transaction is the base transaction in a begin/commit
nesting, the transaction will rollback().  Otherwise, the
method returns.

This is used to cancel a Transaction without affecting the scope of
an enclosing transaction.

    method [sqlalchemy.engine.RootTransaction.](#sqlalchemy.engine.RootTransaction)commit() → None

*inherited from the* [Transaction.commit()](#sqlalchemy.engine.Transaction.commit) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Commit this [Transaction](#sqlalchemy.engine.Transaction).

The implementation of this may vary based on the type of transaction in
use:

- For a simple database transaction (e.g. [RootTransaction](#sqlalchemy.engine.RootTransaction)),
  it corresponds to a COMMIT.
- For a [NestedTransaction](#sqlalchemy.engine.NestedTransaction), it corresponds to a
  “RELEASE SAVEPOINT” operation.
- For a [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction), DBAPI-specific methods for two
  phase transactions may be used.

    method [sqlalchemy.engine.RootTransaction.](#sqlalchemy.engine.RootTransaction)rollback() → None

*inherited from the* [Transaction.rollback()](#sqlalchemy.engine.Transaction.rollback) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Roll back this [Transaction](#sqlalchemy.engine.Transaction).

The implementation of this may vary based on the type of transaction in
use:

- For a simple database transaction (e.g. [RootTransaction](#sqlalchemy.engine.RootTransaction)),
  it corresponds to a ROLLBACK.
- For a [NestedTransaction](#sqlalchemy.engine.NestedTransaction), it corresponds to a
  “ROLLBACK TO SAVEPOINT” operation.
- For a [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction), DBAPI-specific methods for two
  phase transactions may be used.

     class sqlalchemy.engine.Transaction

*inherits from* `sqlalchemy.engine.util.TransactionalContext`

Represent a database transaction in progress.

The [Transaction](#sqlalchemy.engine.Transaction) object is procured by
calling the [Connection.begin()](#sqlalchemy.engine.Connection.begin) method of
[Connection](#sqlalchemy.engine.Connection):

```
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")
connection = engine.connect()
trans = connection.begin()
connection.execute(text("insert into x (a, b) values (1, 2)"))
trans.commit()
```

The object provides [rollback()](#sqlalchemy.engine.Transaction.rollback) and [commit()](#sqlalchemy.engine.Transaction.commit)
methods in order to control transaction boundaries.  It
also implements a context manager interface so that
the Python `with` statement can be used with the
[Connection.begin()](#sqlalchemy.engine.Connection.begin) method:

```
with connection.begin():
    connection.execute(text("insert into x (a, b) values (1, 2)"))
```

The Transaction object is **not** threadsafe.

See also

[Connection.begin()](#sqlalchemy.engine.Connection.begin)

[Connection.begin_twophase()](#sqlalchemy.engine.Connection.begin_twophase)

[Connection.begin_nested()](#sqlalchemy.engine.Connection.begin_nested)

| Member Name | Description |
| --- | --- |
| close() | Close thisTransaction. |
| commit() | Commit thisTransaction. |
| rollback() | Roll back thisTransaction. |

   method [sqlalchemy.engine.Transaction.](#sqlalchemy.engine.Transaction)close() → None

Close this [Transaction](#sqlalchemy.engine.Transaction).

If this transaction is the base transaction in a begin/commit
nesting, the transaction will rollback().  Otherwise, the
method returns.

This is used to cancel a Transaction without affecting the scope of
an enclosing transaction.

    method [sqlalchemy.engine.Transaction.](#sqlalchemy.engine.Transaction)commit() → None

Commit this [Transaction](#sqlalchemy.engine.Transaction).

The implementation of this may vary based on the type of transaction in
use:

- For a simple database transaction (e.g. [RootTransaction](#sqlalchemy.engine.RootTransaction)),
  it corresponds to a COMMIT.
- For a [NestedTransaction](#sqlalchemy.engine.NestedTransaction), it corresponds to a
  “RELEASE SAVEPOINT” operation.
- For a [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction), DBAPI-specific methods for two
  phase transactions may be used.

    method [sqlalchemy.engine.Transaction.](#sqlalchemy.engine.Transaction)rollback() → None

Roll back this [Transaction](#sqlalchemy.engine.Transaction).

The implementation of this may vary based on the type of transaction in
use:

- For a simple database transaction (e.g. [RootTransaction](#sqlalchemy.engine.RootTransaction)),
  it corresponds to a ROLLBACK.
- For a [NestedTransaction](#sqlalchemy.engine.NestedTransaction), it corresponds to a
  “ROLLBACK TO SAVEPOINT” operation.
- For a [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction), DBAPI-specific methods for two
  phase transactions may be used.

     class sqlalchemy.engine.TwoPhaseTransaction

*inherits from* [sqlalchemy.engine.RootTransaction](#sqlalchemy.engine.RootTransaction)

Represent a two-phase transaction.

A new [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction) object may be procured
using the [Connection.begin_twophase()](#sqlalchemy.engine.Connection.begin_twophase) method.

The interface is the same as that of [Transaction](#sqlalchemy.engine.Transaction)
with the addition of the [prepare()](#sqlalchemy.engine.TwoPhaseTransaction.prepare) method.

| Member Name | Description |
| --- | --- |
| close() | Close thisTransaction. |
| commit() | Commit thisTransaction. |
| prepare() | Prepare thisTwoPhaseTransaction. |
| rollback() | Roll back thisTransaction. |

   method [sqlalchemy.engine.TwoPhaseTransaction.](#sqlalchemy.engine.TwoPhaseTransaction)close() → None

*inherited from the* [Transaction.close()](#sqlalchemy.engine.Transaction.close) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Close this [Transaction](#sqlalchemy.engine.Transaction).

If this transaction is the base transaction in a begin/commit
nesting, the transaction will rollback().  Otherwise, the
method returns.

This is used to cancel a Transaction without affecting the scope of
an enclosing transaction.

    method [sqlalchemy.engine.TwoPhaseTransaction.](#sqlalchemy.engine.TwoPhaseTransaction)commit() → None

*inherited from the* [Transaction.commit()](#sqlalchemy.engine.Transaction.commit) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Commit this [Transaction](#sqlalchemy.engine.Transaction).

The implementation of this may vary based on the type of transaction in
use:

- For a simple database transaction (e.g. [RootTransaction](#sqlalchemy.engine.RootTransaction)),
  it corresponds to a COMMIT.
- For a [NestedTransaction](#sqlalchemy.engine.NestedTransaction), it corresponds to a
  “RELEASE SAVEPOINT” operation.
- For a [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction), DBAPI-specific methods for two
  phase transactions may be used.

    method [sqlalchemy.engine.TwoPhaseTransaction.](#sqlalchemy.engine.TwoPhaseTransaction)prepare() → None

Prepare this [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction).

After a PREPARE, the transaction can be committed.

    method [sqlalchemy.engine.TwoPhaseTransaction.](#sqlalchemy.engine.TwoPhaseTransaction)rollback() → None

*inherited from the* [Transaction.rollback()](#sqlalchemy.engine.Transaction.rollback) *method of* [Transaction](#sqlalchemy.engine.Transaction)

Roll back this [Transaction](#sqlalchemy.engine.Transaction).

The implementation of this may vary based on the type of transaction in
use:

- For a simple database transaction (e.g. [RootTransaction](#sqlalchemy.engine.RootTransaction)),
  it corresponds to a ROLLBACK.
- For a [NestedTransaction](#sqlalchemy.engine.NestedTransaction), it corresponds to a
  “ROLLBACK TO SAVEPOINT” operation.
- For a [TwoPhaseTransaction](#sqlalchemy.engine.TwoPhaseTransaction), DBAPI-specific methods for two
  phase transactions may be used.

## Result Set API

| Object Name | Description |
| --- | --- |
| ChunkedIteratorResult | AnIteratorResultthat works from an
iterator-producing callable. |
| CursorResult | A Result that is representing state from a DBAPI cursor. |
| FilterResult | A wrapper for aResultthat returns objects other thanRowobjects, such as dictionaries or scalar objects. |
| FrozenResult | Represents aResultobject in a “frozen” state suitable
for caching. |
| IteratorResult | AResultthat gets data from a Python iterator ofRowobjects or similar row-like data. |
| MappingResult | A wrapper for aResultthat returns dictionary values
rather thanRowvalues. |
| MergedResult | AResultthat is merged from any number ofResultobjects. |
| Result | Represent a set of database results. |
| Row | Represent a single result row. |
| RowMapping | AMappingthat maps column names and objects toRowvalues. |
| ScalarResult | A wrapper for aResultthat returns scalar values
rather thanRowvalues. |
| TupleResult | AResultthat’s typed as returning plain
Python tuples instead of rows. |

   class sqlalchemy.engine.ChunkedIteratorResult

*inherits from* [sqlalchemy.engine.IteratorResult](#sqlalchemy.engine.IteratorResult)

An [IteratorResult](#sqlalchemy.engine.IteratorResult) that works from an
iterator-producing callable.

The given `chunks` argument is a function that is given a number of rows
to return in each chunk, or `None` for all rows.  The function should
then return an un-consumed iterator of lists, each list of the requested
size.

The function can be called at any time again, in which case it should
continue from the same result set but adjust the chunk size as given.

Added in version 1.4.

| Member Name | Description |
| --- | --- |
| yield_per() | Configure the row-fetching strategy to fetchnumrows at a time. |

   method [sqlalchemy.engine.ChunkedIteratorResult.](#sqlalchemy.engine.ChunkedIteratorResult)yield_per(*num:int*) → Self

Configure the row-fetching strategy to fetch `num` rows at a time.

This impacts the underlying behavior of the result when iterating over
the result object, or otherwise making use of  methods such as
[Result.fetchone()](#sqlalchemy.engine.Result.fetchone) that return one row at a time.   Data
from the underlying cursor or other data source will be buffered up to
this many rows in memory, and the buffered collection will then be
yielded out one row at a time or as many rows are requested. Each time
the buffer clears, it will be refreshed to this many rows or as many
rows remain if fewer remain.

The [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method is generally used in
conjunction with the
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
execution option, which will allow the database dialect in use to make
use of a server side cursor, if the DBAPI supports a specific “server
side cursor” mode separate from its default mode of operation.

Tip

Consider using the
[Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
execution option, which will simultaneously set
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
to ensure the use of server side cursors, as well as automatically
invoke the [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method to establish
a fixed row buffer size at once.

The [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
execution option is available for ORM operations, with
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)-oriented use described at
[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per). The Core-only version which works
with [Connection](#sqlalchemy.engine.Connection) is new as of SQLAlchemy 1.4.40.

Added in version 1.4.

   Parameters:

**num** – number of rows to fetch each time the buffer is refilled.
If set to a value below 1, fetches all rows for the next buffer.

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - describes Core behavior for
[Result.yield_per()](#sqlalchemy.engine.Result.yield_per)

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

      class sqlalchemy.engine.CursorResult

*inherits from* [sqlalchemy.engine.Result](#sqlalchemy.engine.Result)

A Result that is representing state from a DBAPI cursor.

Changed in version 1.4: The `CursorResult``
class replaces the previous `ResultProxy` interface.
This classes are based on the [Result](#sqlalchemy.engine.Result) calling API
which provides an updated usage model and calling facade for
SQLAlchemy Core and SQLAlchemy ORM.

Returns database rows via the [Row](#sqlalchemy.engine.Row) class, which provides
additional API features and behaviors on top of the raw data returned by
the DBAPI.   Through the use of filters such as the [Result.scalars()](#sqlalchemy.engine.Result.scalars)
method, other kinds of objects may also be returned.

See also

[Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-data) - introductory material for accessing
[CursorResult](#sqlalchemy.engine.CursorResult) and [Row](#sqlalchemy.engine.Row) objects.

| Member Name | Description |
| --- | --- |
| all() | Return all rows in a sequence. |
| close() | Close thisCursorResult. |
| columns() | Establish the columns that should be returned in each row. |
| fetchall() | A synonym for theResult.all()method. |
| fetchmany() | Fetch many rows. |
| fetchone() | Fetch one row. |
| first() | Fetch the first row orNoneif no row is present. |
| freeze() | Return a callable object that will produce copies of thisResultwhen invoked. |
| keys() | Return an iterable view which yields the string keys that would
be represented by eachRow. |
| last_inserted_params() | Return the collection of inserted parameters from this
execution. |
| last_updated_params() | Return the collection of updated parameters from this
execution. |
| lastrow_has_defaults() | Returnlastrow_has_defaults()from the underlyingExecutionContext. |
| mappings() | Apply a mappings filter to returned rows, returning an instance ofMappingResult. |
| merge() | Merge thisResultwith other compatible result
objects. |
| one() | Return exactly one row or raise an exception. |
| one_or_none() | Return at most one result or raise an exception. |
| partitions() | Iterate through sub-lists of rows of the size given. |
| postfetch_cols() | Returnpostfetch_cols()from the underlyingExecutionContext. |
| prefetch_cols() | Returnprefetch_cols()from the underlyingExecutionContext. |
| rowcount | Return the ‘rowcount’ for this result. |
| scalar() | Fetch the first column of the first row, and close the result set. |
| scalar_one() | Return exactly one scalar result or raise an exception. |
| scalar_one_or_none() | Return exactly one scalar result orNone. |
| scalars() | Return aScalarResultfiltering object which
will return single elements rather thanRowobjects. |
| splice_horizontally() | Return a newCursorResultthat “horizontally splices”
together the rows of thisCursorResultwith that of anotherCursorResult. |
| splice_vertically() | Return a newCursorResultthat “vertically splices”,
i.e. “extends”, the rows of thisCursorResultwith that of
anotherCursorResult. |
| supports_sane_multi_rowcount() | Returnsupports_sane_multi_rowcountfrom the dialect. |
| supports_sane_rowcount() | Returnsupports_sane_rowcountfrom the dialect. |
| tuples() | Apply a “typed tuple” typing filter to returned rows. |
| unique() | Apply unique filtering to the objects returned by thisResult. |
| yield_per() | Configure the row-fetching strategy to fetchnumrows at a time. |

   method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)all() → Sequence[[Row](#sqlalchemy.engine.Row)[_TP]]

*inherited from the* [Result.all()](#sqlalchemy.engine.Result.all) *method of* [Result](#sqlalchemy.engine.Result)

Return all rows in a sequence.

Closes the result set after invocation.   Subsequent invocations
will return an empty sequence.

Added in version 1.4.

   Returns:

a sequence of [Row](#sqlalchemy.engine.Row) objects.

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - How to stream a large result set
without loading it completely in python.

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)close() → None

Close this [CursorResult](#sqlalchemy.engine.CursorResult).

This closes out the underlying DBAPI cursor corresponding to the
statement execution, if one is still present.  Note that the DBAPI
cursor is automatically released when the [CursorResult](#sqlalchemy.engine.CursorResult)
exhausts all available rows.  [CursorResult.close()](#sqlalchemy.engine.CursorResult.close) is
generally an optional method except in the case when discarding a
[CursorResult](#sqlalchemy.engine.CursorResult) that still has additional rows pending
for fetch.

After this method is called, it is no longer valid to call upon
the fetch methods, which will raise a [ResourceClosedError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ResourceClosedError)
on subsequent use.

See also

[Working with Engines and Connections](#)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)columns(**col_expressions:_KeyIndexType*) → Self

*inherited from the* [Result.columns()](#sqlalchemy.engine.Result.columns) *method of* [Result](#sqlalchemy.engine.Result)

Establish the columns that should be returned in each row.

This method may be used to limit the columns returned as well
as to reorder them.   The given list of expressions are normally
a series of integers or string key names.   They may also be
appropriate [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects which correspond to
a given statement construct.

Changed in version 2.0: Due to a bug in 1.4, the
[Result.columns()](#sqlalchemy.engine.Result.columns) method had an incorrect behavior
where calling upon the method with just one index would cause the
[Result](#sqlalchemy.engine.Result) object to yield scalar values rather than
[Row](#sqlalchemy.engine.Row) objects.   In version 2.0, this behavior
has been corrected such that calling upon
[Result.columns()](#sqlalchemy.engine.Result.columns) with a single index will
produce a [Result](#sqlalchemy.engine.Result) object that continues
to yield [Row](#sqlalchemy.engine.Row) objects, which include
only a single column.

E.g.:

```
statement = select(table.c.x, table.c.y, table.c.z)
result = connection.execute(statement)

for z, y in result.columns("z", "y"):
    ...
```

Example of using the column objects from the statement itself:

```
for z, y in result.columns(
    statement.selected_columns.c.z, statement.selected_columns.c.y
):
    ...
```

Added in version 1.4.

   Parameters:

***col_expressions** – indicates columns to be returned.  Elements
may be integer row indexes, string column names, or appropriate
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects corresponding to a select construct.

  Returns:

this [Result](#sqlalchemy.engine.Result) object with the modifications
given.

      method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)fetchall() → Sequence[[Row](#sqlalchemy.engine.Row)[_TP]]

*inherited from the* [Result.fetchall()](#sqlalchemy.engine.Result.fetchall) *method of* [Result](#sqlalchemy.engine.Result)

A synonym for the [Result.all()](#sqlalchemy.engine.Result.all) method.

    method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)fetchmany(*size:int|None=None*) → Sequence[[Row](#sqlalchemy.engine.Row)[_TP]]

*inherited from the* [Result.fetchmany()](#sqlalchemy.engine.Result.fetchmany) *method of* [Result](#sqlalchemy.engine.Result)

Fetch many rows.

When all rows are exhausted, returns an empty sequence.

This method is provided for backwards compatibility with
SQLAlchemy 1.x.x.

To fetch rows in groups, use the [Result.partitions()](#sqlalchemy.engine.Result.partitions)
method.

  Returns:

a sequence of [Row](#sqlalchemy.engine.Row) objects.

See also

[Result.partitions()](#sqlalchemy.engine.Result.partitions)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)fetchone() → [Row](#sqlalchemy.engine.Row)[_TP] | None

*inherited from the* [Result.fetchone()](#sqlalchemy.engine.Result.fetchone) *method of* [Result](#sqlalchemy.engine.Result)

Fetch one row.

When all rows are exhausted, returns None.

This method is provided for backwards compatibility with
SQLAlchemy 1.x.x.

To fetch the first row of a result only, use the
[Result.first()](#sqlalchemy.engine.Result.first) method.  To iterate through all
rows, iterate the [Result](#sqlalchemy.engine.Result) object directly.

  Returns:

a [Row](#sqlalchemy.engine.Row) object if no filters are applied,
or `None` if no rows remain.

      method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)first() → [Row](#sqlalchemy.engine.Row)[_TP] | None

*inherited from the* [Result.first()](#sqlalchemy.engine.Result.first) *method of* [Result](#sqlalchemy.engine.Result)

Fetch the first row or `None` if no row is present.

Closes the result set and discards remaining rows.

Note

This method returns one **row**, e.g. tuple, by default.
To return exactly one single scalar value, that is, the first
column of the first row, use the
[Result.scalar()](#sqlalchemy.engine.Result.scalar) method,
or combine [Result.scalars()](#sqlalchemy.engine.Result.scalars) and
[Result.first()](#sqlalchemy.engine.Result.first).

Additionally, in contrast to the behavior of the legacy  ORM
[Query.first()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.first) method, **no limit is applied** to the
SQL query which was invoked to produce this
[Result](#sqlalchemy.engine.Result);
for a DBAPI driver that buffers results in memory before yielding
rows, all rows will be sent to the Python process and all but
the first row will be discarded.

See also

[ORM Query Unified with Core Select](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-unify-select)

    Returns:

a [Row](#sqlalchemy.engine.Row) object, or None
if no rows remain.

See also

[Result.scalar()](#sqlalchemy.engine.Result.scalar)

[Result.one()](#sqlalchemy.engine.Result.one)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)freeze() → [FrozenResult](#sqlalchemy.engine.FrozenResult)[_TP]

*inherited from the* [Result.freeze()](#sqlalchemy.engine.Result.freeze) *method of* [Result](#sqlalchemy.engine.Result)

Return a callable object that will produce copies of this
[Result](#sqlalchemy.engine.Result) when invoked.

The callable object returned is an instance of
[FrozenResult](#sqlalchemy.engine.FrozenResult).

This is used for result set caching.  The method must be called
on the result when it has been unconsumed, and calling the method
will consume the result fully.   When the [FrozenResult](#sqlalchemy.engine.FrozenResult)
is retrieved from a cache, it can be called any number of times where
it will produce a new [Result](#sqlalchemy.engine.Result) object each time
against its stored set of rows.

See also

[Re-Executing Statements](https://docs.sqlalchemy.org/en/20/orm/session_events.html#do-orm-execute-re-executing) - example usage within the
ORM to implement a result-set cache.

     property inserted_primary_key: Any | None

Return the primary key for the row just inserted.

The return value is a [Row](#sqlalchemy.engine.Row) object representing
a named tuple of primary key values in the order in which the
primary key columns are configured in the source
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

Changed in version 1.4.8: - the
[CursorResult.inserted_primary_key](#sqlalchemy.engine.CursorResult.inserted_primary_key)
value is now a named tuple via the [Row](#sqlalchemy.engine.Row) class,
rather than a plain tuple.

This accessor only applies to single row [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert)
constructs which did not explicitly specify
[Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning).    Support for multirow inserts,
while not yet available for most backends, would be accessed using
the [CursorResult.inserted_primary_key_rows](#sqlalchemy.engine.CursorResult.inserted_primary_key_rows) accessor.

Note that primary key columns which specify a server_default clause, or
otherwise do not qualify as “autoincrement” columns (see the notes at
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)), and were generated using the database-side
default, will appear in this list as `None` unless the backend
supports “returning” and the insert statement executed with the
“implicit returning” enabled.

Raises [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) if the executed
statement is not a compiled expression construct
or is not an insert() construct.

    property inserted_primary_key_rows: List[Any | None]

Return the value of
[CursorResult.inserted_primary_key](#sqlalchemy.engine.CursorResult.inserted_primary_key)
as a row contained within a list; some dialects may support a
multiple row form as well.

Note

As indicated below, in current SQLAlchemy versions this
accessor is only useful beyond what’s already supplied by
[CursorResult.inserted_primary_key](#sqlalchemy.engine.CursorResult.inserted_primary_key) when using the
[psycopg2](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-psycopg2) dialect.   Future versions hope to
generalize this feature to more dialects.

This accessor is added to support dialects that offer the feature
that is currently implemented by the [Psycopg2 Fast Execution Helpers](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#psycopg2-executemany-mode)
feature, currently **only the psycopg2 dialect**, which provides
for many rows to be INSERTed at once while still retaining the
behavior of being able to return server-generated primary key values.

- **When using the psycopg2 dialect, or other dialects that may support
  “fast executemany” style inserts in upcoming releases** : When
  invoking an INSERT statement while passing a list of rows as the
  second argument to [Connection.execute()](#sqlalchemy.engine.Connection.execute), this accessor
  will then provide a list of rows, where each row contains the primary
  key value for each row that was INSERTed.
- **When using all other dialects / backends that don’t yet support
  this feature**: This accessor is only useful for **single row INSERT
  statements**, and returns the same information as that of the
  [CursorResult.inserted_primary_key](#sqlalchemy.engine.CursorResult.inserted_primary_key) within a
  single-element list. When an INSERT statement is executed in
  conjunction with a list of rows to be INSERTed, the list will contain
  one row per row inserted in the statement, however it will contain
  `None` for any server-generated values.

Future releases of SQLAlchemy will further generalize the
“fast execution helper” feature of psycopg2 to suit other dialects,
thus allowing this accessor to be of more general use.

Added in version 1.4.

See also

[CursorResult.inserted_primary_key](#sqlalchemy.engine.CursorResult.inserted_primary_key)

     property is_insert: bool

True if this [CursorResult](#sqlalchemy.engine.CursorResult) is the result
of a executing an expression language compiled
[insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct.

When True, this implies that the
[inserted_primary_key](#sqlalchemy.engine.CursorResult.inserted_primary_key) attribute is accessible,
assuming the statement did not include
a user defined “returning” construct.

    method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)keys() → RMKeyView

*inherited from the* `sqlalchemy.engine._WithKeys.keys` *method of* `sqlalchemy.engine._WithKeys`

Return an iterable view which yields the string keys that would
be represented by each [Row](#sqlalchemy.engine.Row).

The keys can represent the labels of the columns returned by a core
statement or the names of the orm classes returned by an orm
execution.

The view also can be tested for key containment using the Python
`in` operator, which will test both for the string keys represented
in the view, as well as for alternate keys such as column objects.

Changed in version 1.4: a key view object is returned rather than a
plain list.

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)last_inserted_params() → List[_MutableCoreSingleExecuteParams] | _MutableCoreSingleExecuteParams

Return the collection of inserted parameters from this
execution.

Raises [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) if the executed
statement is not a compiled expression construct
or is not an insert() construct.

    method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)last_updated_params() → List[_MutableCoreSingleExecuteParams] | _MutableCoreSingleExecuteParams

Return the collection of updated parameters from this
execution.

Raises [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) if the executed
statement is not a compiled expression construct
or is not an update() construct.

    method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)lastrow_has_defaults() → bool

Return `lastrow_has_defaults()` from the underlying
[ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext).

See [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext) for details.

    property lastrowid: int

Return the ‘lastrowid’ accessor on the DBAPI cursor.

This is a DBAPI specific method and is only functional
for those backends which support it, for statements
where it is appropriate.  It’s behavior is not
consistent across backends.

Usage of this method is normally unnecessary when
using insert() expression constructs; the
[CursorResult.inserted_primary_key](#sqlalchemy.engine.CursorResult.inserted_primary_key) attribute provides a
tuple of primary key values for a newly inserted row,
regardless of database backend.

    method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)mappings() → [MappingResult](#sqlalchemy.engine.MappingResult)

*inherited from the* [Result.mappings()](#sqlalchemy.engine.Result.mappings) *method of* [Result](#sqlalchemy.engine.Result)

Apply a mappings filter to returned rows, returning an instance of
[MappingResult](#sqlalchemy.engine.MappingResult).

When this filter is applied, fetching rows will return
[RowMapping](#sqlalchemy.engine.RowMapping) objects instead of [Row](#sqlalchemy.engine.Row)
objects.

Added in version 1.4.

   Returns:

a new [MappingResult](#sqlalchemy.engine.MappingResult) filtering object
referring to this [Result](#sqlalchemy.engine.Result) object.

      method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)merge(**others:Result[Any]*) → [MergedResult](#sqlalchemy.engine.MergedResult)[Any]

Merge this [Result](#sqlalchemy.engine.Result) with other compatible result
objects.

The object returned is an instance of [MergedResult](#sqlalchemy.engine.MergedResult),
which will be composed of iterators from the given result
objects.

The new result will use the metadata from this result object.
The subsequent result objects must be against an identical
set of result / cursor metadata, otherwise the behavior is
undefined.

    method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)one() → [Row](#sqlalchemy.engine.Row)[_TP]

*inherited from the* [Result.one()](#sqlalchemy.engine.Result.one) *method of* [Result](#sqlalchemy.engine.Result)

Return exactly one row or raise an exception.

Raises [NoResultFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoResultFound) if the result returns no
rows, or [MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound) if multiple rows
would be returned.

Note

This method returns one **row**, e.g. tuple, by default.
To return exactly one single scalar value, that is, the first
column of the first row, use the
[Result.scalar_one()](#sqlalchemy.engine.Result.scalar_one) method, or combine
[Result.scalars()](#sqlalchemy.engine.Result.scalars) and
[Result.one()](#sqlalchemy.engine.Result.one).

Added in version 1.4.

   Returns:

The first [Row](#sqlalchemy.engine.Row).

  Raises:

[MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound), [NoResultFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoResultFound)

See also

[Result.first()](#sqlalchemy.engine.Result.first)

[Result.one_or_none()](#sqlalchemy.engine.Result.one_or_none)

[Result.scalar_one()](#sqlalchemy.engine.Result.scalar_one)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)one_or_none() → [Row](#sqlalchemy.engine.Row)[_TP] | None

*inherited from the* [Result.one_or_none()](#sqlalchemy.engine.Result.one_or_none) *method of* [Result](#sqlalchemy.engine.Result)

Return at most one result or raise an exception.

Returns `None` if the result has no rows.
Raises [MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound)
if multiple rows are returned.

Added in version 1.4.

   Returns:

The first [Row](#sqlalchemy.engine.Row) or `None` if no row
is available.

  Raises:

[MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound)

See also

[Result.first()](#sqlalchemy.engine.Result.first)

[Result.one()](#sqlalchemy.engine.Result.one)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)partitions(*size:int|None=None*) → Iterator[Sequence[[Row](#sqlalchemy.engine.Row)[_TP]]]

*inherited from the* [Result.partitions()](#sqlalchemy.engine.Result.partitions) *method of* [Result](#sqlalchemy.engine.Result)

Iterate through sub-lists of rows of the size given.

Each list will be of the size given, excluding the last list to
be yielded, which may have a small number of rows.  No empty
lists will be yielded.

The result object is automatically closed when the iterator
is fully consumed.

Note that the backend driver will usually buffer the entire result
ahead of time unless the
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results) execution
option is used indicating that the driver should not pre-buffer
results, if possible.   Not all drivers support this option and
the option is silently ignored for those who do not.

When using the ORM, the [Result.partitions()](#sqlalchemy.engine.Result.partitions) method
is typically more effective from a memory perspective when it is
combined with use of the
[yield_per execution option](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per),
which instructs both the DBAPI driver to use server side cursors,
if available, as well as instructs the ORM loading internals to only
build a certain amount of ORM objects from a result at a time before
yielding them out.

Added in version 1.4.

   Parameters:

**size** – indicate the maximum number of rows to be present
in each list yielded.  If None, makes use of the value set by
the [Result.yield_per()](#sqlalchemy.engine.Result.yield_per), method, if it were called,
or the [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
execution option, which is equivalent in this regard.  If
yield_per weren’t set, it makes use of the
[Result.fetchmany()](#sqlalchemy.engine.Result.fetchmany) default, which may be backend
specific and not well defined.

  Returns:

iterator of lists

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results)

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)postfetch_cols() → [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]] | None

Return `postfetch_cols()` from the underlying
[ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext).

See [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext) for details.

Raises [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) if the executed
statement is not a compiled expression construct
or is not an insert() or update() construct.

    method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)prefetch_cols() → [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]] | None

Return `prefetch_cols()` from the underlying
[ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext).

See [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext) for details.

Raises [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) if the executed
statement is not a compiled expression construct
or is not an insert() or update() construct.

    property returned_defaults: [Row](#sqlalchemy.engine.Row)[Any] | None

Return the values of default columns that were fetched using
the `ValuesBase.return_defaults()` feature.

The value is an instance of [Row](#sqlalchemy.engine.Row), or `None`
if `ValuesBase.return_defaults()` was not used or if the
backend does not support RETURNING.

See also

`ValuesBase.return_defaults()`

     property returned_defaults_rows: Sequence[[Row](#sqlalchemy.engine.Row)[Any]] | None

Return a list of rows each containing the values of default
columns that were fetched using
the `ValuesBase.return_defaults()` feature.

The return value is a list of [Row](#sqlalchemy.engine.Row) objects.

Added in version 1.4.

     property returns_rows: bool

True if this [CursorResult](#sqlalchemy.engine.CursorResult) returns zero or more
rows.

I.e. if it is legal to call the methods
[CursorResult.fetchone()](#sqlalchemy.engine.CursorResult.fetchone),
[CursorResult.fetchmany()](#sqlalchemy.engine.CursorResult.fetchmany) [CursorResult.fetchall()](#sqlalchemy.engine.CursorResult.fetchall).

Overall, the value of [CursorResult.returns_rows](#sqlalchemy.engine.CursorResult.returns_rows) should
always be synonymous with whether or not the DBAPI cursor had a
`.description` attribute, indicating the presence of result columns,
noting that a cursor that returns zero rows still has a
`.description` if a row-returning statement was emitted.

This attribute should be True for all results that are against
SELECT statements, as well as for DML statements INSERT/UPDATE/DELETE
that use RETURNING.   For INSERT/UPDATE/DELETE statements that were
not using RETURNING, the value will usually be False, however
there are some dialect-specific exceptions to this, such as when
using the MSSQL / pyodbc dialect a SELECT is emitted inline in
order to retrieve an inserted primary key value.

    attribute [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)rowcount

Return the ‘rowcount’ for this result.

The primary purpose of ‘rowcount’ is to report the number of rows
matched by the WHERE criterion of an UPDATE or DELETE statement
executed once (i.e. for a single parameter set), which may then be
compared to the number of rows expected to be updated or deleted as a
means of asserting data integrity.

This attribute is transferred from the `cursor.rowcount` attribute
of the DBAPI before the cursor is closed, to support DBAPIs that
don’t make this value available after cursor close.   Some DBAPIs may
offer meaningful values for other kinds of statements, such as INSERT
and SELECT statements as well.  In order to retrieve `cursor.rowcount`
for these statements, set the
[Connection.execution_options.preserve_rowcount](#sqlalchemy.engine.Connection.execution_options.params.preserve_rowcount)
execution option to True, which will cause the `cursor.rowcount`
value to be unconditionally memoized before any results are returned
or the cursor is closed, regardless of statement type.

For cases where the DBAPI does not support rowcount for a particular
kind of statement and/or execution, the returned value will be `-1`,
which is delivered directly from the DBAPI and is part of [PEP 249](https://peps.python.org/pep-0249/).
All DBAPIs should support rowcount for single-parameter-set
UPDATE and DELETE statements, however.

Note

Notes regarding [CursorResult.rowcount](#sqlalchemy.engine.CursorResult.rowcount):

- This attribute returns the number of rows *matched*,
  which is not necessarily the same as the number of rows
  that were actually *modified*. For example, an UPDATE statement
  may have no net change on a given row if the SET values
  given are the same as those present in the row already.
  Such a row would be matched but not modified.
  On backends that feature both styles, such as MySQL,
  rowcount is configured to return the match
  count in all cases.
- [CursorResult.rowcount](#sqlalchemy.engine.CursorResult.rowcount) in the default case is
  *only* useful in conjunction with an UPDATE or DELETE statement,
  and only with a single set of parameters. For other kinds of
  statements, SQLAlchemy will not attempt to pre-memoize the value
  unless the
  [Connection.execution_options.preserve_rowcount](#sqlalchemy.engine.Connection.execution_options.params.preserve_rowcount)
  execution option is used.  Note that contrary to [PEP 249](https://peps.python.org/pep-0249/), many
  DBAPIs do not support rowcount values for statements that are not
  UPDATE or DELETE, particularly when rows are being returned which
  are not fully pre-buffered.   DBAPIs that dont support rowcount
  for a particular kind of statement should return the value `-1`
  for such statements.
- [CursorResult.rowcount](#sqlalchemy.engine.CursorResult.rowcount) may not be meaningful
  when executing a single statement with multiple parameter sets
  (i.e. an [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)). Most DBAPIs do not sum “rowcount”
  values across multiple parameter sets and will return `-1`
  when accessed.
- SQLAlchemy’s [“Insert Many Values” Behavior for INSERT statements](#engine-insertmanyvalues) feature does support
  a correct population of [CursorResult.rowcount](#sqlalchemy.engine.CursorResult.rowcount)
  when the [Connection.execution_options.preserve_rowcount](#sqlalchemy.engine.Connection.execution_options.params.preserve_rowcount)
  execution option is set to True.
- Statements that use RETURNING may not support rowcount, returning
  a `-1` value instead.

See also

[Getting Affected Row Count from UPDATE, DELETE](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-update-delete-rowcount) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Connection.execution_options.preserve_rowcount](#sqlalchemy.engine.Connection.execution_options.params.preserve_rowcount)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)scalar() → Any

*inherited from the* [Result.scalar()](#sqlalchemy.engine.Result.scalar) *method of* [Result](#sqlalchemy.engine.Result)

Fetch the first column of the first row, and close the result set.

Returns `None` if there are no rows to fetch.

No validation is performed to test if additional rows remain.

After calling this method, the object is fully closed,
e.g. the [CursorResult.close()](#sqlalchemy.engine.CursorResult.close)
method will have been called.

  Returns:

a Python scalar value, or `None` if no rows remain.

      method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)scalar_one() → Any

*inherited from the* [Result.scalar_one()](#sqlalchemy.engine.Result.scalar_one) *method of* [Result](#sqlalchemy.engine.Result)

Return exactly one scalar result or raise an exception.

This is equivalent to calling [Result.scalars()](#sqlalchemy.engine.Result.scalars) and
then [ScalarResult.one()](#sqlalchemy.engine.ScalarResult.one).

See also

[ScalarResult.one()](#sqlalchemy.engine.ScalarResult.one)

[Result.scalars()](#sqlalchemy.engine.Result.scalars)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)scalar_one_or_none() → Any | None

*inherited from the* [Result.scalar_one_or_none()](#sqlalchemy.engine.Result.scalar_one_or_none) *method of* [Result](#sqlalchemy.engine.Result)

Return exactly one scalar result or `None`.

This is equivalent to calling [Result.scalars()](#sqlalchemy.engine.Result.scalars) and
then [ScalarResult.one_or_none()](#sqlalchemy.engine.ScalarResult.one_or_none).

See also

[ScalarResult.one_or_none()](#sqlalchemy.engine.ScalarResult.one_or_none)

[Result.scalars()](#sqlalchemy.engine.Result.scalars)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)scalars(*index:_KeyIndexType=0*) → [ScalarResult](#sqlalchemy.engine.ScalarResult)[Any]

*inherited from the* [Result.scalars()](#sqlalchemy.engine.Result.scalars) *method of* [Result](#sqlalchemy.engine.Result)

Return a [ScalarResult](#sqlalchemy.engine.ScalarResult) filtering object which
will return single elements rather than [Row](#sqlalchemy.engine.Row) objects.

E.g.:

```
>>> result = conn.execute(text("select int_id from table"))
>>> result.scalars().all()
[1, 2, 3]
```

When results are fetched from the [ScalarResult](#sqlalchemy.engine.ScalarResult)
filtering object, the single column-row that would be returned by the
[Result](#sqlalchemy.engine.Result) is instead returned as the column’s value.

Added in version 1.4.

   Parameters:

**index** – integer or row key indicating the column to be fetched
from each row, defaults to `0` indicating the first column.

  Returns:

a new [ScalarResult](#sqlalchemy.engine.ScalarResult) filtering object referring
to this [Result](#sqlalchemy.engine.Result) object.

      method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)splice_horizontally(*other:CursorResult[Any]*) → Self

Return a new [CursorResult](#sqlalchemy.engine.CursorResult) that “horizontally splices”
together the rows of this [CursorResult](#sqlalchemy.engine.CursorResult) with that of another
[CursorResult](#sqlalchemy.engine.CursorResult).

Tip

This method is for the benefit of the SQLAlchemy ORM and is
not intended for general use.

“horizontally splices” means that for each row in the first and second
result sets, a new row that concatenates the two rows together is
produced, which then becomes the new row.  The incoming
[CursorResult](#sqlalchemy.engine.CursorResult) must have the identical number of rows.  It is
typically expected that the two result sets come from the same sort
order as well, as the result rows are spliced together based on their
position in the result.

The expected use case here is so that multiple INSERT..RETURNING
statements (which definitely need to be sorted) against different
tables can produce a single result that looks like a JOIN of those two
tables.

E.g.:

```
r1 = connection.execute(
    users.insert().returning(
        users.c.user_name, users.c.user_id, sort_by_parameter_order=True
    ),
    user_values,
)

r2 = connection.execute(
    addresses.insert().returning(
        addresses.c.address_id,
        addresses.c.address,
        addresses.c.user_id,
        sort_by_parameter_order=True,
    ),
    address_values,
)

rows = r1.splice_horizontally(r2).all()
assert rows == [
    ("john", 1, 1, "[email protected]", 1),
    ("jack", 2, 2, "[email protected]", 2),
]
```

Added in version 2.0.

See also

[CursorResult.splice_vertically()](#sqlalchemy.engine.CursorResult.splice_vertically)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)splice_vertically(*other:CursorResult[Any]*) → Self

Return a new [CursorResult](#sqlalchemy.engine.CursorResult) that “vertically splices”,
i.e. “extends”, the rows of this [CursorResult](#sqlalchemy.engine.CursorResult) with that of
another [CursorResult](#sqlalchemy.engine.CursorResult).

Tip

This method is for the benefit of the SQLAlchemy ORM and is
not intended for general use.

“vertically splices” means the rows of the given result are appended to
the rows of this cursor result. The incoming [CursorResult](#sqlalchemy.engine.CursorResult)
must have rows that represent the identical list of columns in the
identical order as they are in this [CursorResult](#sqlalchemy.engine.CursorResult).

Added in version 2.0.

See also

[CursorResult.splice_horizontally()](#sqlalchemy.engine.CursorResult.splice_horizontally)

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)supports_sane_multi_rowcount() → bool

Return `supports_sane_multi_rowcount` from the dialect.

See [CursorResult.rowcount](#sqlalchemy.engine.CursorResult.rowcount) for background.

    method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)supports_sane_rowcount() → bool

Return `supports_sane_rowcount` from the dialect.

See [CursorResult.rowcount](#sqlalchemy.engine.CursorResult.rowcount) for background.

    property t: [TupleResult](#sqlalchemy.engine.TupleResult)[_TP]

Apply a “typed tuple” typing filter to returned rows.

The [Result.t](#sqlalchemy.engine.Result.t) attribute is a synonym for
calling the [Result.tuples()](#sqlalchemy.engine.Result.tuples) method.

Added in version 2.0.

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)tuples() → [TupleResult](#sqlalchemy.engine.TupleResult)[_TP]

*inherited from the* [Result.tuples()](#sqlalchemy.engine.Result.tuples) *method of* [Result](#sqlalchemy.engine.Result)

Apply a “typed tuple” typing filter to returned rows.

This method returns the same [Result](#sqlalchemy.engine.Result) object
at runtime,
however annotates as returning a [TupleResult](#sqlalchemy.engine.TupleResult) object
that will indicate to [PEP 484](https://peps.python.org/pep-0484/) typing tools that plain typed
`Tuple` instances are returned rather than rows.  This allows
tuple unpacking and `__getitem__` access of [Row](#sqlalchemy.engine.Row)
objects to by typed, for those cases where the statement invoked
itself included typing information.

Added in version 2.0.

   Returns:

the [TupleResult](#sqlalchemy.engine.TupleResult) type at typing time.

See also

[Result.t](#sqlalchemy.engine.Result.t) - shorter synonym

[Row._t](#sqlalchemy.engine.Row._t) - [Row](#sqlalchemy.engine.Row) version

     method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)unique(*strategy:Callable[[Any],Any]|None=None*) → Self

*inherited from the* [Result.unique()](#sqlalchemy.engine.Result.unique) *method of* [Result](#sqlalchemy.engine.Result)

Apply unique filtering to the objects returned by this
[Result](#sqlalchemy.engine.Result).

When this filter is applied with no arguments, the rows or objects
returned will filtered such that each row is returned uniquely. The
algorithm used to determine this uniqueness is by default the Python
hashing identity of the whole tuple.   In some cases a specialized
per-entity hashing scheme may be used, such as when using the ORM, a
scheme is applied which  works against the primary key identity of
returned objects.

The unique filter is applied **after all other filters**, which means
if the columns returned have been refined using a method such as the
[Result.columns()](#sqlalchemy.engine.Result.columns) or [Result.scalars()](#sqlalchemy.engine.Result.scalars)
method, the uniquing is applied to **only the column or columns
returned**.   This occurs regardless of the order in which these
methods have been called upon the [Result](#sqlalchemy.engine.Result) object.

The unique filter also changes the calculus used for methods like
[Result.fetchmany()](#sqlalchemy.engine.Result.fetchmany) and [Result.partitions()](#sqlalchemy.engine.Result.partitions).
When using [Result.unique()](#sqlalchemy.engine.Result.unique), these methods will continue
to yield the number of rows or objects requested, after uniquing
has been applied.  However, this necessarily impacts the buffering
behavior of the underlying cursor or datasource, such that multiple
underlying calls to `cursor.fetchmany()` may be necessary in order
to accumulate enough objects in order to provide a unique collection
of the requested size.

  Parameters:

**strategy** – a callable that will be applied to rows or objects
being iterated, which should return an object that represents the
unique value of the row.   A Python `set()` is used to store
these identities.   If not passed, a default uniqueness strategy
is used which may have been assembled by the source of this
[Result](#sqlalchemy.engine.Result) object.

      method [sqlalchemy.engine.CursorResult.](#sqlalchemy.engine.CursorResult)yield_per(*num:int*) → Self

Configure the row-fetching strategy to fetch `num` rows at a time.

This impacts the underlying behavior of the result when iterating over
the result object, or otherwise making use of  methods such as
[Result.fetchone()](#sqlalchemy.engine.Result.fetchone) that return one row at a time.   Data
from the underlying cursor or other data source will be buffered up to
this many rows in memory, and the buffered collection will then be
yielded out one row at a time or as many rows are requested. Each time
the buffer clears, it will be refreshed to this many rows or as many
rows remain if fewer remain.

The [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method is generally used in
conjunction with the
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
execution option, which will allow the database dialect in use to make
use of a server side cursor, if the DBAPI supports a specific “server
side cursor” mode separate from its default mode of operation.

Tip

Consider using the
[Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
execution option, which will simultaneously set
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
to ensure the use of server side cursors, as well as automatically
invoke the [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method to establish
a fixed row buffer size at once.

The [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
execution option is available for ORM operations, with
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)-oriented use described at
[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per). The Core-only version which works
with [Connection](#sqlalchemy.engine.Connection) is new as of SQLAlchemy 1.4.40.

Added in version 1.4.

   Parameters:

**num** – number of rows to fetch each time the buffer is refilled.
If set to a value below 1, fetches all rows for the next buffer.

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - describes Core behavior for
[Result.yield_per()](#sqlalchemy.engine.Result.yield_per)

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

      class sqlalchemy.engine.FilterResult

*inherits from* `sqlalchemy.engine.ResultInternal`

A wrapper for a [Result](#sqlalchemy.engine.Result) that returns objects other than
[Row](#sqlalchemy.engine.Row) objects, such as dictionaries or scalar objects.

[FilterResult](#sqlalchemy.engine.FilterResult) is the common base for additional result
APIs including [MappingResult](#sqlalchemy.engine.MappingResult),
[ScalarResult](#sqlalchemy.engine.ScalarResult) and `AsyncResult`.

| Member Name | Description |
| --- | --- |
| close() | Close thisFilterResult. |
| yield_per() | Configure the row-fetching strategy to fetchnumrows at a time. |

   method [sqlalchemy.engine.FilterResult.](#sqlalchemy.engine.FilterResult)close() → None

Close this [FilterResult](#sqlalchemy.engine.FilterResult).

Added in version 1.4.43.

     property closed: bool

Return `True` if the underlying [Result](#sqlalchemy.engine.Result) reports
closed

Added in version 1.4.43.

     method [sqlalchemy.engine.FilterResult.](#sqlalchemy.engine.FilterResult)yield_per(*num:int*) → Self

Configure the row-fetching strategy to fetch `num` rows at a time.

The [FilterResult.yield_per()](#sqlalchemy.engine.FilterResult.yield_per) method is a pass through
to the [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method.  See that method’s
documentation for usage notes.

Added in version 1.4.40: - added [FilterResult.yield_per()](#sqlalchemy.engine.FilterResult.yield_per)
so that the method is available on all result set implementations

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - describes Core behavior for
[Result.yield_per()](#sqlalchemy.engine.Result.yield_per)

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

      class sqlalchemy.engine.FrozenResult

*inherits from* `typing.Generic`

Represents a [Result](#sqlalchemy.engine.Result) object in a “frozen” state suitable
for caching.

The [FrozenResult](#sqlalchemy.engine.FrozenResult) object is returned from the
[Result.freeze()](#sqlalchemy.engine.Result.freeze) method of any [Result](#sqlalchemy.engine.Result)
object.

A new iterable [Result](#sqlalchemy.engine.Result) object is generated from a fixed
set of data each time the [FrozenResult](#sqlalchemy.engine.FrozenResult) is invoked as
a callable:

```
result = connection.execute(query)

frozen = result.freeze()

unfrozen_result_one = frozen()

for row in unfrozen_result_one:
    print(row)

unfrozen_result_two = frozen()
rows = unfrozen_result_two.all()

# ... etc
```

Added in version 1.4.

See also

[Re-Executing Statements](https://docs.sqlalchemy.org/en/20/orm/session_events.html#do-orm-execute-re-executing) - example usage within the
ORM to implement a result-set cache.

`merge_frozen_result()` - ORM function to merge
a frozen result back into a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

     class sqlalchemy.engine.IteratorResult

*inherits from* [sqlalchemy.engine.Result](#sqlalchemy.engine.Result)

A [Result](#sqlalchemy.engine.Result) that gets data from a Python iterator of
[Row](#sqlalchemy.engine.Row) objects or similar row-like data.

Added in version 1.4.

    property closed: bool

Return `True` if this [IteratorResult](#sqlalchemy.engine.IteratorResult) has
been closed

Added in version 1.4.43.

      class sqlalchemy.engine.MergedResult

*inherits from* [sqlalchemy.engine.IteratorResult](#sqlalchemy.engine.IteratorResult)

A [Result](#sqlalchemy.engine.Result) that is merged from any number of
[Result](#sqlalchemy.engine.Result) objects.

Returned by the [Result.merge()](#sqlalchemy.engine.Result.merge) method.

Added in version 1.4.

     class sqlalchemy.engine.Result

*inherits from* `sqlalchemy.engine._WithKeys`, `sqlalchemy.engine.ResultInternal`

Represent a set of database results.

Added in version 1.4: The [Result](#sqlalchemy.engine.Result) object provides a
completely updated usage model and calling facade for SQLAlchemy
Core and SQLAlchemy ORM.   In Core, it forms the basis of the
[CursorResult](#sqlalchemy.engine.CursorResult) object which replaces the previous
`ResultProxy` interface.   When using the ORM, a
higher level object called [ChunkedIteratorResult](#sqlalchemy.engine.ChunkedIteratorResult)
is normally used.

Note

In SQLAlchemy 1.4 and above, this object is
used for ORM results returned by [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), which can
yield instances of ORM mapped objects either individually or within
tuple-like rows. Note that the [Result](#sqlalchemy.engine.Result) object does not
deduplicate instances or rows automatically as is the case with the
legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object. For in-Python de-duplication of
instances or rows, use the [Result.unique()](#sqlalchemy.engine.Result.unique) modifier
method.

See also

[Fetching Rows](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-fetching-rows) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

| Member Name | Description |
| --- | --- |
| all() | Return all rows in a sequence. |
| close() | close thisResult. |
| columns() | Establish the columns that should be returned in each row. |
| fetchall() | A synonym for theResult.all()method. |
| fetchmany() | Fetch many rows. |
| fetchone() | Fetch one row. |
| first() | Fetch the first row orNoneif no row is present. |
| freeze() | Return a callable object that will produce copies of thisResultwhen invoked. |
| keys() | Return an iterable view which yields the string keys that would
be represented by eachRow. |
| mappings() | Apply a mappings filter to returned rows, returning an instance ofMappingResult. |
| merge() | Merge thisResultwith other compatible result
objects. |
| one() | Return exactly one row or raise an exception. |
| one_or_none() | Return at most one result or raise an exception. |
| partitions() | Iterate through sub-lists of rows of the size given. |
| scalar() | Fetch the first column of the first row, and close the result set. |
| scalar_one() | Return exactly one scalar result or raise an exception. |
| scalar_one_or_none() | Return exactly one scalar result orNone. |
| scalars() | Return aScalarResultfiltering object which
will return single elements rather thanRowobjects. |
| tuples() | Apply a “typed tuple” typing filter to returned rows. |
| unique() | Apply unique filtering to the objects returned by thisResult. |
| yield_per() | Configure the row-fetching strategy to fetchnumrows at a time. |

   method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)all() → Sequence[[Row](#sqlalchemy.engine.Row)[_TP]]

Return all rows in a sequence.

Closes the result set after invocation.   Subsequent invocations
will return an empty sequence.

Added in version 1.4.

   Returns:

a sequence of [Row](#sqlalchemy.engine.Row) objects.

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - How to stream a large result set
without loading it completely in python.

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)close() → None

close this [Result](#sqlalchemy.engine.Result).

The behavior of this method is implementation specific, and is
not implemented by default.    The method should generally end
the resources in use by the result object and also cause any
subsequent iteration or row fetching to raise
[ResourceClosedError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ResourceClosedError).

Added in version 1.4.27: - `.close()` was previously not generally
available for all [Result](#sqlalchemy.engine.Result) classes, instead only
being available on the [CursorResult](#sqlalchemy.engine.CursorResult) returned for
Core statement executions. As most other result objects, namely the
ones used by the ORM, are proxying a [CursorResult](#sqlalchemy.engine.CursorResult)
in any case, this allows the underlying cursor result to be closed
from the outside facade for the case when the ORM query is using
the `yield_per` execution option where it does not immediately
exhaust and autoclose the database cursor.

     property closed: bool

return `True` if this [Result](#sqlalchemy.engine.Result) reports .closed

Added in version 1.4.43.

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)columns(**col_expressions:_KeyIndexType*) → Self

Establish the columns that should be returned in each row.

This method may be used to limit the columns returned as well
as to reorder them.   The given list of expressions are normally
a series of integers or string key names.   They may also be
appropriate [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects which correspond to
a given statement construct.

Changed in version 2.0: Due to a bug in 1.4, the
[Result.columns()](#sqlalchemy.engine.Result.columns) method had an incorrect behavior
where calling upon the method with just one index would cause the
[Result](#sqlalchemy.engine.Result) object to yield scalar values rather than
[Row](#sqlalchemy.engine.Row) objects.   In version 2.0, this behavior
has been corrected such that calling upon
[Result.columns()](#sqlalchemy.engine.Result.columns) with a single index will
produce a [Result](#sqlalchemy.engine.Result) object that continues
to yield [Row](#sqlalchemy.engine.Row) objects, which include
only a single column.

E.g.:

```
statement = select(table.c.x, table.c.y, table.c.z)
result = connection.execute(statement)

for z, y in result.columns("z", "y"):
    ...
```

Example of using the column objects from the statement itself:

```
for z, y in result.columns(
    statement.selected_columns.c.z, statement.selected_columns.c.y
):
    ...
```

Added in version 1.4.

   Parameters:

***col_expressions** – indicates columns to be returned.  Elements
may be integer row indexes, string column names, or appropriate
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects corresponding to a select construct.

  Returns:

this [Result](#sqlalchemy.engine.Result) object with the modifications
given.

      method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)fetchall() → Sequence[[Row](#sqlalchemy.engine.Row)[_TP]]

A synonym for the [Result.all()](#sqlalchemy.engine.Result.all) method.

    method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)fetchmany(*size:int|None=None*) → Sequence[[Row](#sqlalchemy.engine.Row)[_TP]]

Fetch many rows.

When all rows are exhausted, returns an empty sequence.

This method is provided for backwards compatibility with
SQLAlchemy 1.x.x.

To fetch rows in groups, use the [Result.partitions()](#sqlalchemy.engine.Result.partitions)
method.

  Returns:

a sequence of [Row](#sqlalchemy.engine.Row) objects.

See also

[Result.partitions()](#sqlalchemy.engine.Result.partitions)

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)fetchone() → [Row](#sqlalchemy.engine.Row)[_TP] | None

Fetch one row.

When all rows are exhausted, returns None.

This method is provided for backwards compatibility with
SQLAlchemy 1.x.x.

To fetch the first row of a result only, use the
[Result.first()](#sqlalchemy.engine.Result.first) method.  To iterate through all
rows, iterate the [Result](#sqlalchemy.engine.Result) object directly.

  Returns:

a [Row](#sqlalchemy.engine.Row) object if no filters are applied,
or `None` if no rows remain.

      method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)first() → [Row](#sqlalchemy.engine.Row)[_TP] | None

Fetch the first row or `None` if no row is present.

Closes the result set and discards remaining rows.

Note

This method returns one **row**, e.g. tuple, by default.
To return exactly one single scalar value, that is, the first
column of the first row, use the
[Result.scalar()](#sqlalchemy.engine.Result.scalar) method,
or combine [Result.scalars()](#sqlalchemy.engine.Result.scalars) and
[Result.first()](#sqlalchemy.engine.Result.first).

Additionally, in contrast to the behavior of the legacy  ORM
[Query.first()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.first) method, **no limit is applied** to the
SQL query which was invoked to produce this
[Result](#sqlalchemy.engine.Result);
for a DBAPI driver that buffers results in memory before yielding
rows, all rows will be sent to the Python process and all but
the first row will be discarded.

See also

[ORM Query Unified with Core Select](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-unify-select)

    Returns:

a [Row](#sqlalchemy.engine.Row) object, or None
if no rows remain.

See also

[Result.scalar()](#sqlalchemy.engine.Result.scalar)

[Result.one()](#sqlalchemy.engine.Result.one)

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)freeze() → [FrozenResult](#sqlalchemy.engine.FrozenResult)[_TP]

Return a callable object that will produce copies of this
[Result](#sqlalchemy.engine.Result) when invoked.

The callable object returned is an instance of
[FrozenResult](#sqlalchemy.engine.FrozenResult).

This is used for result set caching.  The method must be called
on the result when it has been unconsumed, and calling the method
will consume the result fully.   When the [FrozenResult](#sqlalchemy.engine.FrozenResult)
is retrieved from a cache, it can be called any number of times where
it will produce a new [Result](#sqlalchemy.engine.Result) object each time
against its stored set of rows.

See also

[Re-Executing Statements](https://docs.sqlalchemy.org/en/20/orm/session_events.html#do-orm-execute-re-executing) - example usage within the
ORM to implement a result-set cache.

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)keys() → RMKeyView

*inherited from the* `sqlalchemy.engine._WithKeys.keys` *method of* `sqlalchemy.engine._WithKeys`

Return an iterable view which yields the string keys that would
be represented by each [Row](#sqlalchemy.engine.Row).

The keys can represent the labels of the columns returned by a core
statement or the names of the orm classes returned by an orm
execution.

The view also can be tested for key containment using the Python
`in` operator, which will test both for the string keys represented
in the view, as well as for alternate keys such as column objects.

Changed in version 1.4: a key view object is returned rather than a
plain list.

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)mappings() → [MappingResult](#sqlalchemy.engine.MappingResult)

Apply a mappings filter to returned rows, returning an instance of
[MappingResult](#sqlalchemy.engine.MappingResult).

When this filter is applied, fetching rows will return
[RowMapping](#sqlalchemy.engine.RowMapping) objects instead of [Row](#sqlalchemy.engine.Row)
objects.

Added in version 1.4.

   Returns:

a new [MappingResult](#sqlalchemy.engine.MappingResult) filtering object
referring to this [Result](#sqlalchemy.engine.Result) object.

      method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)merge(**others:Result[Any]*) → [MergedResult](#sqlalchemy.engine.MergedResult)[_TP]

Merge this [Result](#sqlalchemy.engine.Result) with other compatible result
objects.

The object returned is an instance of [MergedResult](#sqlalchemy.engine.MergedResult),
which will be composed of iterators from the given result
objects.

The new result will use the metadata from this result object.
The subsequent result objects must be against an identical
set of result / cursor metadata, otherwise the behavior is
undefined.

    method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)one() → [Row](#sqlalchemy.engine.Row)[_TP]

Return exactly one row or raise an exception.

Raises [NoResultFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoResultFound) if the result returns no
rows, or [MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound) if multiple rows
would be returned.

Note

This method returns one **row**, e.g. tuple, by default.
To return exactly one single scalar value, that is, the first
column of the first row, use the
[Result.scalar_one()](#sqlalchemy.engine.Result.scalar_one) method, or combine
[Result.scalars()](#sqlalchemy.engine.Result.scalars) and
[Result.one()](#sqlalchemy.engine.Result.one).

Added in version 1.4.

   Returns:

The first [Row](#sqlalchemy.engine.Row).

  Raises:

[MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound), [NoResultFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoResultFound)

See also

[Result.first()](#sqlalchemy.engine.Result.first)

[Result.one_or_none()](#sqlalchemy.engine.Result.one_or_none)

[Result.scalar_one()](#sqlalchemy.engine.Result.scalar_one)

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)one_or_none() → [Row](#sqlalchemy.engine.Row)[_TP] | None

Return at most one result or raise an exception.

Returns `None` if the result has no rows.
Raises [MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound)
if multiple rows are returned.

Added in version 1.4.

   Returns:

The first [Row](#sqlalchemy.engine.Row) or `None` if no row
is available.

  Raises:

[MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound)

See also

[Result.first()](#sqlalchemy.engine.Result.first)

[Result.one()](#sqlalchemy.engine.Result.one)

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)partitions(*size:int|None=None*) → Iterator[Sequence[[Row](#sqlalchemy.engine.Row)[_TP]]]

Iterate through sub-lists of rows of the size given.

Each list will be of the size given, excluding the last list to
be yielded, which may have a small number of rows.  No empty
lists will be yielded.

The result object is automatically closed when the iterator
is fully consumed.

Note that the backend driver will usually buffer the entire result
ahead of time unless the
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results) execution
option is used indicating that the driver should not pre-buffer
results, if possible.   Not all drivers support this option and
the option is silently ignored for those who do not.

When using the ORM, the [Result.partitions()](#sqlalchemy.engine.Result.partitions) method
is typically more effective from a memory perspective when it is
combined with use of the
[yield_per execution option](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per),
which instructs both the DBAPI driver to use server side cursors,
if available, as well as instructs the ORM loading internals to only
build a certain amount of ORM objects from a result at a time before
yielding them out.

Added in version 1.4.

   Parameters:

**size** – indicate the maximum number of rows to be present
in each list yielded.  If None, makes use of the value set by
the [Result.yield_per()](#sqlalchemy.engine.Result.yield_per), method, if it were called,
or the [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
execution option, which is equivalent in this regard.  If
yield_per weren’t set, it makes use of the
[Result.fetchmany()](#sqlalchemy.engine.Result.fetchmany) default, which may be backend
specific and not well defined.

  Returns:

iterator of lists

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results)

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)scalar() → Any

Fetch the first column of the first row, and close the result set.

Returns `None` if there are no rows to fetch.

No validation is performed to test if additional rows remain.

After calling this method, the object is fully closed,
e.g. the [CursorResult.close()](#sqlalchemy.engine.CursorResult.close)
method will have been called.

  Returns:

a Python scalar value, or `None` if no rows remain.

      method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)scalar_one() → Any

Return exactly one scalar result or raise an exception.

This is equivalent to calling [Result.scalars()](#sqlalchemy.engine.Result.scalars) and
then [ScalarResult.one()](#sqlalchemy.engine.ScalarResult.one).

See also

[ScalarResult.one()](#sqlalchemy.engine.ScalarResult.one)

[Result.scalars()](#sqlalchemy.engine.Result.scalars)

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)scalar_one_or_none() → Any | None

Return exactly one scalar result or `None`.

This is equivalent to calling [Result.scalars()](#sqlalchemy.engine.Result.scalars) and
then [ScalarResult.one_or_none()](#sqlalchemy.engine.ScalarResult.one_or_none).

See also

[ScalarResult.one_or_none()](#sqlalchemy.engine.ScalarResult.one_or_none)

[Result.scalars()](#sqlalchemy.engine.Result.scalars)

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)scalars(*index:_KeyIndexType=0*) → [ScalarResult](#sqlalchemy.engine.ScalarResult)[Any]

Return a [ScalarResult](#sqlalchemy.engine.ScalarResult) filtering object which
will return single elements rather than [Row](#sqlalchemy.engine.Row) objects.

E.g.:

```
>>> result = conn.execute(text("select int_id from table"))
>>> result.scalars().all()
[1, 2, 3]
```

When results are fetched from the [ScalarResult](#sqlalchemy.engine.ScalarResult)
filtering object, the single column-row that would be returned by the
[Result](#sqlalchemy.engine.Result) is instead returned as the column’s value.

Added in version 1.4.

   Parameters:

**index** – integer or row key indicating the column to be fetched
from each row, defaults to `0` indicating the first column.

  Returns:

a new [ScalarResult](#sqlalchemy.engine.ScalarResult) filtering object referring
to this [Result](#sqlalchemy.engine.Result) object.

      property t: [TupleResult](#sqlalchemy.engine.TupleResult)[_TP]

Apply a “typed tuple” typing filter to returned rows.

The [Result.t](#sqlalchemy.engine.Result.t) attribute is a synonym for
calling the [Result.tuples()](#sqlalchemy.engine.Result.tuples) method.

Added in version 2.0.

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)tuples() → [TupleResult](#sqlalchemy.engine.TupleResult)[_TP]

Apply a “typed tuple” typing filter to returned rows.

This method returns the same [Result](#sqlalchemy.engine.Result) object
at runtime,
however annotates as returning a [TupleResult](#sqlalchemy.engine.TupleResult) object
that will indicate to [PEP 484](https://peps.python.org/pep-0484/) typing tools that plain typed
`Tuple` instances are returned rather than rows.  This allows
tuple unpacking and `__getitem__` access of [Row](#sqlalchemy.engine.Row)
objects to by typed, for those cases where the statement invoked
itself included typing information.

Added in version 2.0.

   Returns:

the [TupleResult](#sqlalchemy.engine.TupleResult) type at typing time.

See also

[Result.t](#sqlalchemy.engine.Result.t) - shorter synonym

[Row._t](#sqlalchemy.engine.Row._t) - [Row](#sqlalchemy.engine.Row) version

     method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)unique(*strategy:Callable[[Any],Any]|None=None*) → Self

Apply unique filtering to the objects returned by this
[Result](#sqlalchemy.engine.Result).

When this filter is applied with no arguments, the rows or objects
returned will filtered such that each row is returned uniquely. The
algorithm used to determine this uniqueness is by default the Python
hashing identity of the whole tuple.   In some cases a specialized
per-entity hashing scheme may be used, such as when using the ORM, a
scheme is applied which  works against the primary key identity of
returned objects.

The unique filter is applied **after all other filters**, which means
if the columns returned have been refined using a method such as the
[Result.columns()](#sqlalchemy.engine.Result.columns) or [Result.scalars()](#sqlalchemy.engine.Result.scalars)
method, the uniquing is applied to **only the column or columns
returned**.   This occurs regardless of the order in which these
methods have been called upon the [Result](#sqlalchemy.engine.Result) object.

The unique filter also changes the calculus used for methods like
[Result.fetchmany()](#sqlalchemy.engine.Result.fetchmany) and [Result.partitions()](#sqlalchemy.engine.Result.partitions).
When using [Result.unique()](#sqlalchemy.engine.Result.unique), these methods will continue
to yield the number of rows or objects requested, after uniquing
has been applied.  However, this necessarily impacts the buffering
behavior of the underlying cursor or datasource, such that multiple
underlying calls to `cursor.fetchmany()` may be necessary in order
to accumulate enough objects in order to provide a unique collection
of the requested size.

  Parameters:

**strategy** – a callable that will be applied to rows or objects
being iterated, which should return an object that represents the
unique value of the row.   A Python `set()` is used to store
these identities.   If not passed, a default uniqueness strategy
is used which may have been assembled by the source of this
[Result](#sqlalchemy.engine.Result) object.

      method [sqlalchemy.engine.Result.](#sqlalchemy.engine.Result)yield_per(*num:int*) → Self

Configure the row-fetching strategy to fetch `num` rows at a time.

This impacts the underlying behavior of the result when iterating over
the result object, or otherwise making use of  methods such as
[Result.fetchone()](#sqlalchemy.engine.Result.fetchone) that return one row at a time.   Data
from the underlying cursor or other data source will be buffered up to
this many rows in memory, and the buffered collection will then be
yielded out one row at a time or as many rows are requested. Each time
the buffer clears, it will be refreshed to this many rows or as many
rows remain if fewer remain.

The [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method is generally used in
conjunction with the
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
execution option, which will allow the database dialect in use to make
use of a server side cursor, if the DBAPI supports a specific “server
side cursor” mode separate from its default mode of operation.

Tip

Consider using the
[Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
execution option, which will simultaneously set
[Connection.execution_options.stream_results](#sqlalchemy.engine.Connection.execution_options.params.stream_results)
to ensure the use of server side cursors, as well as automatically
invoke the [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method to establish
a fixed row buffer size at once.

The [Connection.execution_options.yield_per](#sqlalchemy.engine.Connection.execution_options.params.yield_per)
execution option is available for ORM operations, with
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)-oriented use described at
[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per). The Core-only version which works
with [Connection](#sqlalchemy.engine.Connection) is new as of SQLAlchemy 1.4.40.

Added in version 1.4.

   Parameters:

**num** – number of rows to fetch each time the buffer is refilled.
If set to a value below 1, fetches all rows for the next buffer.

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - describes Core behavior for
[Result.yield_per()](#sqlalchemy.engine.Result.yield_per)

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

      class sqlalchemy.engine.ScalarResult

*inherits from* [sqlalchemy.engine.FilterResult](#sqlalchemy.engine.FilterResult)

A wrapper for a [Result](#sqlalchemy.engine.Result) that returns scalar values
rather than [Row](#sqlalchemy.engine.Row) values.

The [ScalarResult](#sqlalchemy.engine.ScalarResult) object is acquired by calling the
[Result.scalars()](#sqlalchemy.engine.Result.scalars) method.

A special limitation of [ScalarResult](#sqlalchemy.engine.ScalarResult) is that it has
no `fetchone()` method; since the semantics of `fetchone()` are that
the `None` value indicates no more results, this is not compatible
with [ScalarResult](#sqlalchemy.engine.ScalarResult) since there is no way to distinguish
between `None` as a row value versus `None` as an indicator.  Use
`next(result)` to receive values individually.

| Member Name | Description |
| --- | --- |
| all() | Return all scalar values in a sequence. |
| close() | Close thisFilterResult. |
| fetchall() | A synonym for theScalarResult.all()method. |
| fetchmany() | Fetch many objects. |
| first() | Fetch the first object orNoneif no object is present. |
| one() | Return exactly one object or raise an exception. |
| one_or_none() | Return at most one object or raise an exception. |
| partitions() | Iterate through sub-lists of elements of the size given. |
| unique() | Apply unique filtering to the objects returned by thisScalarResult. |
| yield_per() | Configure the row-fetching strategy to fetchnumrows at a time. |

   method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)all() → Sequence[_R]

Return all scalar values in a sequence.

Equivalent to [Result.all()](#sqlalchemy.engine.Result.all) except that
scalar values, rather than [Row](#sqlalchemy.engine.Row) objects,
are returned.

    method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)close() → None

*inherited from the* [FilterResult.close()](#sqlalchemy.engine.FilterResult.close) *method of* [FilterResult](#sqlalchemy.engine.FilterResult)

Close this [FilterResult](#sqlalchemy.engine.FilterResult).

Added in version 1.4.43.

     property closed: bool

Return `True` if the underlying [Result](#sqlalchemy.engine.Result) reports
closed

Added in version 1.4.43.

     method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)fetchall() → Sequence[_R]

A synonym for the [ScalarResult.all()](#sqlalchemy.engine.ScalarResult.all) method.

    method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)fetchmany(*size:int|None=None*) → Sequence[_R]

Fetch many objects.

Equivalent to [Result.fetchmany()](#sqlalchemy.engine.Result.fetchmany) except that
scalar values, rather than [Row](#sqlalchemy.engine.Row) objects,
are returned.

    method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)first() → _R | None

Fetch the first object or `None` if no object is present.

Equivalent to [Result.first()](#sqlalchemy.engine.Result.first) except that
scalar values, rather than [Row](#sqlalchemy.engine.Row) objects,
are returned.

    method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)one() → _R

Return exactly one object or raise an exception.

Equivalent to [Result.one()](#sqlalchemy.engine.Result.one) except that
scalar values, rather than [Row](#sqlalchemy.engine.Row) objects,
are returned.

    method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)one_or_none() → _R | None

Return at most one object or raise an exception.

Equivalent to [Result.one_or_none()](#sqlalchemy.engine.Result.one_or_none) except that
scalar values, rather than [Row](#sqlalchemy.engine.Row) objects,
are returned.

    method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)partitions(*size:int|None=None*) → Iterator[Sequence[_R]]

Iterate through sub-lists of elements of the size given.

Equivalent to [Result.partitions()](#sqlalchemy.engine.Result.partitions) except that
scalar values, rather than [Row](#sqlalchemy.engine.Row) objects,
are returned.

    method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)unique(*strategy:Callable[[Any],Any]|None=None*) → Self

Apply unique filtering to the objects returned by this
[ScalarResult](#sqlalchemy.engine.ScalarResult).

See [Result.unique()](#sqlalchemy.engine.Result.unique) for usage details.

    method [sqlalchemy.engine.ScalarResult.](#sqlalchemy.engine.ScalarResult)yield_per(*num:int*) → Self

*inherited from the* [FilterResult.yield_per()](#sqlalchemy.engine.FilterResult.yield_per) *method of* [FilterResult](#sqlalchemy.engine.FilterResult)

Configure the row-fetching strategy to fetch `num` rows at a time.

The [FilterResult.yield_per()](#sqlalchemy.engine.FilterResult.yield_per) method is a pass through
to the [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method.  See that method’s
documentation for usage notes.

Added in version 1.4.40: - added [FilterResult.yield_per()](#sqlalchemy.engine.FilterResult.yield_per)
so that the method is available on all result set implementations

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - describes Core behavior for
[Result.yield_per()](#sqlalchemy.engine.Result.yield_per)

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

      class sqlalchemy.engine.MappingResult

*inherits from* `sqlalchemy.engine._WithKeys`, [sqlalchemy.engine.FilterResult](#sqlalchemy.engine.FilterResult)

A wrapper for a [Result](#sqlalchemy.engine.Result) that returns dictionary values
rather than [Row](#sqlalchemy.engine.Row) values.

The [MappingResult](#sqlalchemy.engine.MappingResult) object is acquired by calling the
[Result.mappings()](#sqlalchemy.engine.Result.mappings) method.

| Member Name | Description |
| --- | --- |
| all() | Return all scalar values in a sequence. |
| close() | Close thisFilterResult. |
| columns() | Establish the columns that should be returned in each row. |
| fetchall() | A synonym for theMappingResult.all()method. |
| fetchmany() | Fetch many objects. |
| fetchone() | Fetch one object. |
| first() | Fetch the first object orNoneif no object is present. |
| keys() | Return an iterable view which yields the string keys that would
be represented by eachRow. |
| one() | Return exactly one object or raise an exception. |
| one_or_none() | Return at most one object or raise an exception. |
| partitions() | Iterate through sub-lists of elements of the size given. |
| unique() | Apply unique filtering to the objects returned by thisMappingResult. |
| yield_per() | Configure the row-fetching strategy to fetchnumrows at a time. |

   method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)all() → Sequence[[RowMapping](#sqlalchemy.engine.RowMapping)]

Return all scalar values in a sequence.

Equivalent to [Result.all()](#sqlalchemy.engine.Result.all) except that
[RowMapping](#sqlalchemy.engine.RowMapping) values, rather than [Row](#sqlalchemy.engine.Row)
objects, are returned.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)close() → None

*inherited from the* [FilterResult.close()](#sqlalchemy.engine.FilterResult.close) *method of* [FilterResult](#sqlalchemy.engine.FilterResult)

Close this [FilterResult](#sqlalchemy.engine.FilterResult).

Added in version 1.4.43.

     property closed: bool

Return `True` if the underlying [Result](#sqlalchemy.engine.Result) reports
closed

Added in version 1.4.43.

     method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)columns(**col_expressions:_KeyIndexType*) → Self

Establish the columns that should be returned in each row.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)fetchall() → Sequence[[RowMapping](#sqlalchemy.engine.RowMapping)]

A synonym for the [MappingResult.all()](#sqlalchemy.engine.MappingResult.all) method.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)fetchmany(*size:int|None=None*) → Sequence[[RowMapping](#sqlalchemy.engine.RowMapping)]

Fetch many objects.

Equivalent to [Result.fetchmany()](#sqlalchemy.engine.Result.fetchmany) except that
[RowMapping](#sqlalchemy.engine.RowMapping) values, rather than [Row](#sqlalchemy.engine.Row)
objects, are returned.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)fetchone() → [RowMapping](#sqlalchemy.engine.RowMapping) | None

Fetch one object.

Equivalent to [Result.fetchone()](#sqlalchemy.engine.Result.fetchone) except that
[RowMapping](#sqlalchemy.engine.RowMapping) values, rather than [Row](#sqlalchemy.engine.Row)
objects, are returned.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)first() → [RowMapping](#sqlalchemy.engine.RowMapping) | None

Fetch the first object or `None` if no object is present.

Equivalent to [Result.first()](#sqlalchemy.engine.Result.first) except that
[RowMapping](#sqlalchemy.engine.RowMapping) values, rather than [Row](#sqlalchemy.engine.Row)
objects, are returned.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)keys() → RMKeyView

*inherited from the* `sqlalchemy.engine._WithKeys.keys` *method of* `sqlalchemy.engine._WithKeys`

Return an iterable view which yields the string keys that would
be represented by each [Row](#sqlalchemy.engine.Row).

The keys can represent the labels of the columns returned by a core
statement or the names of the orm classes returned by an orm
execution.

The view also can be tested for key containment using the Python
`in` operator, which will test both for the string keys represented
in the view, as well as for alternate keys such as column objects.

Changed in version 1.4: a key view object is returned rather than a
plain list.

     method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)one() → [RowMapping](#sqlalchemy.engine.RowMapping)

Return exactly one object or raise an exception.

Equivalent to [Result.one()](#sqlalchemy.engine.Result.one) except that
[RowMapping](#sqlalchemy.engine.RowMapping) values, rather than [Row](#sqlalchemy.engine.Row)
objects, are returned.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)one_or_none() → [RowMapping](#sqlalchemy.engine.RowMapping) | None

Return at most one object or raise an exception.

Equivalent to [Result.one_or_none()](#sqlalchemy.engine.Result.one_or_none) except that
[RowMapping](#sqlalchemy.engine.RowMapping) values, rather than [Row](#sqlalchemy.engine.Row)
objects, are returned.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)partitions(*size:int|None=None*) → Iterator[Sequence[[RowMapping](#sqlalchemy.engine.RowMapping)]]

Iterate through sub-lists of elements of the size given.

Equivalent to [Result.partitions()](#sqlalchemy.engine.Result.partitions) except that
[RowMapping](#sqlalchemy.engine.RowMapping) values, rather than [Row](#sqlalchemy.engine.Row)
objects, are returned.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)unique(*strategy:Callable[[Any],Any]|None=None*) → Self

Apply unique filtering to the objects returned by this
[MappingResult](#sqlalchemy.engine.MappingResult).

See [Result.unique()](#sqlalchemy.engine.Result.unique) for usage details.

    method [sqlalchemy.engine.MappingResult.](#sqlalchemy.engine.MappingResult)yield_per(*num:int*) → Self

*inherited from the* [FilterResult.yield_per()](#sqlalchemy.engine.FilterResult.yield_per) *method of* [FilterResult](#sqlalchemy.engine.FilterResult)

Configure the row-fetching strategy to fetch `num` rows at a time.

The [FilterResult.yield_per()](#sqlalchemy.engine.FilterResult.yield_per) method is a pass through
to the [Result.yield_per()](#sqlalchemy.engine.Result.yield_per) method.  See that method’s
documentation for usage notes.

Added in version 1.4.40: - added [FilterResult.yield_per()](#sqlalchemy.engine.FilterResult.yield_per)
so that the method is available on all result set implementations

See also

[Using Server Side Cursors (a.k.a. stream results)](#engine-stream-results) - describes Core behavior for
[Result.yield_per()](#sqlalchemy.engine.Result.yield_per)

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

      class sqlalchemy.engine.Row

*inherits from* `sqlalchemy.engine._py_row.BaseRow`, `collections.abc.Sequence`, `typing.Generic`

Represent a single result row.

The [Row](#sqlalchemy.engine.Row) object represents a row of a database result.  It is
typically associated in the 1.x series of SQLAlchemy with the
[CursorResult](#sqlalchemy.engine.CursorResult) object, however is also used by the ORM for
tuple-like results as of SQLAlchemy 1.4.

The [Row](#sqlalchemy.engine.Row) object seeks to act as much like a Python named
tuple as possible.   For mapping (i.e. dictionary) behavior on a row,
such as testing for containment of keys, refer to the [Row._mapping](#sqlalchemy.engine.Row._mapping)
attribute.

See also

[Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-data) - includes examples of selecting
rows from SELECT statements.

Changed in version 1.4: Renamed `RowProxy` to [Row](#sqlalchemy.engine.Row). [Row](#sqlalchemy.engine.Row) is no longer a
“proxy” object in that it contains the final form of data within it,
and now acts mostly like a named tuple. Mapping-like functionality is
moved to the [Row._mapping](#sqlalchemy.engine.Row._mapping) attribute. See
[RowProxy is no longer a “proxy”; is now called Row and behaves like an enhanced named tuple](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-4710-core) for background on this change.

| Member Name | Description |
| --- | --- |
| _asdict() | Return a new dict which maps field names to their corresponding
values. |
| _tuple() | Return a ‘tuple’ form of thisRow. |
| tuple() | Return a ‘tuple’ form of thisRow. |

   method [sqlalchemy.engine.Row.](#sqlalchemy.engine.Row)_asdict() → Dict[str, Any]

Return a new dict which maps field names to their corresponding
values.

This method is analogous to the Python named tuple `._asdict()`
method, and works by applying the `dict()` constructor to the
[Row._mapping](#sqlalchemy.engine.Row._mapping) attribute.

Added in version 1.4.

See also

[Row._mapping](#sqlalchemy.engine.Row._mapping)

     property _fields: Tuple[str, ...]

Return a tuple of string keys as represented by this
[Row](#sqlalchemy.engine.Row).

The keys can represent the labels of the columns returned by a core
statement or the names of the orm classes returned by an orm
execution.

This attribute is analogous to the Python named tuple `._fields`
attribute.

Added in version 1.4.

See also

[Row._mapping](#sqlalchemy.engine.Row._mapping)

     property _mapping: [RowMapping](#sqlalchemy.engine.RowMapping)

Return a [RowMapping](#sqlalchemy.engine.RowMapping) for this [Row](#sqlalchemy.engine.Row).

This object provides a consistent Python mapping (i.e. dictionary)
interface for the data contained within the row.   The [Row](#sqlalchemy.engine.Row)
by itself behaves like a named tuple.

See also

[Row._fields](#sqlalchemy.engine.Row._fields)

Added in version 1.4.

     property _t: _TP

A synonym for [Row._tuple()](#sqlalchemy.engine.Row._tuple).

Added in version 2.0.19: - The [Row._t](#sqlalchemy.engine.Row._t) attribute supersedes
the previous [Row.t](#sqlalchemy.engine.Row.t) attribute, which is now underscored
to avoid name conflicts with column names in the same way as other
named-tuple methods on [Row](#sqlalchemy.engine.Row).

See also

[Result.t](#sqlalchemy.engine.Result.t)

     method [sqlalchemy.engine.Row.](#sqlalchemy.engine.Row)_tuple() → _TP

Return a ‘tuple’ form of this [Row](#sqlalchemy.engine.Row).

At runtime, this method returns “self”; the [Row](#sqlalchemy.engine.Row) object is
already a named tuple. However, at the typing level, if this
[Row](#sqlalchemy.engine.Row) is typed, the “tuple” return type will be a [PEP 484](https://peps.python.org/pep-0484/) `Tuple` datatype that contains typing information about individual
elements, supporting typed unpacking and attribute access.

Added in version 2.0.19: - The [Row._tuple()](#sqlalchemy.engine.Row._tuple) method supersedes
the previous [Row.tuple()](#sqlalchemy.engine.Row.tuple) method, which is now underscored
to avoid name conflicts with column names in the same way as other
named-tuple methods on [Row](#sqlalchemy.engine.Row).

See also

[Row._t](#sqlalchemy.engine.Row._t) - shorthand attribute notation

[Result.tuples()](#sqlalchemy.engine.Result.tuples)

     Row.count -> integer -- return number of occurrences of value    Row.index -> integer -- return first index of value.

Raises ValueError if the value is not present.

Supporting start and stop arguments is optional, but
recommended.

    property t: _TP

A synonym for [Row._tuple()](#sqlalchemy.engine.Row._tuple).

Deprecated since version 2.0.19: The [Row.t](#sqlalchemy.engine.Row.t) attribute is deprecated in favor of [Row._t](#sqlalchemy.engine.Row._t); all [Row](#sqlalchemy.engine.Row) methods and library-level attributes are intended to be underscored to avoid name conflicts.  Please use [Row._t](#sqlalchemy.engine.Row._t).

Added in version 2.0.

     method [sqlalchemy.engine.Row.](#sqlalchemy.engine.Row)tuple() → _TP

Return a ‘tuple’ form of this [Row](#sqlalchemy.engine.Row).

Deprecated since version 2.0.19: The [Row.tuple()](#sqlalchemy.engine.Row.tuple) method is deprecated in favor of [Row._tuple()](#sqlalchemy.engine.Row._tuple); all [Row](#sqlalchemy.engine.Row) methods and library-level attributes are intended to be underscored to avoid name conflicts.  Please use [Row._tuple()](#sqlalchemy.engine.Row._tuple).

Added in version 2.0.

      class sqlalchemy.engine.RowMapping

*inherits from* `sqlalchemy.engine._py_row.BaseRow`, `collections.abc.Mapping`, `typing.Generic`

A `Mapping` that maps column names and objects to [Row](#sqlalchemy.engine.Row)
values.

The [RowMapping](#sqlalchemy.engine.RowMapping) is available from a [Row](#sqlalchemy.engine.Row) via the
[Row._mapping](#sqlalchemy.engine.Row._mapping) attribute, as well as from the iterable interface
provided by the [MappingResult](#sqlalchemy.engine.MappingResult) object returned by the
[Result.mappings()](#sqlalchemy.engine.Result.mappings) method.

[RowMapping](#sqlalchemy.engine.RowMapping) supplies Python mapping (i.e. dictionary) access to
the  contents of the row.   This includes support for testing of
containment of specific keys (string column names or objects), as well
as iteration of keys, values, and items:

```
for row in result:
    if "a" in row._mapping:
        print("Column 'a': %s" % row._mapping["a"])

    print("Column b: %s" % row._mapping[table.c.b])
```

Added in version 1.4: The [RowMapping](#sqlalchemy.engine.RowMapping) object replaces the
mapping-like access previously provided by a database result row,
which now seeks to behave mostly like a named tuple.

| Member Name | Description |
| --- | --- |
| items() | Return a view of key/value tuples for the elements in the
underlyingRow. |
| keys() | Return a view of ‘keys’ for string column names represented
by the underlyingRow. |
| values() | Return a view of values for the values represented in the
underlyingRow. |

   method [sqlalchemy.engine.RowMapping.](#sqlalchemy.engine.RowMapping)items() → ROMappingItemsView

Return a view of key/value tuples for the elements in the
underlying [Row](#sqlalchemy.engine.Row).

    method [sqlalchemy.engine.RowMapping.](#sqlalchemy.engine.RowMapping)keys() → RMKeyView

Return a view of ‘keys’ for string column names represented
by the underlying [Row](#sqlalchemy.engine.Row).

    method [sqlalchemy.engine.RowMapping.](#sqlalchemy.engine.RowMapping)values() → ROMappingKeysValuesView

Return a view of values for the values represented in the
underlying [Row](#sqlalchemy.engine.Row).

     class sqlalchemy.engine.TupleResult

*inherits from* [sqlalchemy.engine.FilterResult](#sqlalchemy.engine.FilterResult), `sqlalchemy.util.langhelpers.TypingOnly`

A [Result](#sqlalchemy.engine.Result) that’s typed as returning plain
Python tuples instead of rows.

Since [Row](#sqlalchemy.engine.Row) acts like a tuple in every way already,
this class is a typing only class, regular [Result](#sqlalchemy.engine.Result) is
still used at runtime.
