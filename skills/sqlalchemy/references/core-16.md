# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Connection Pooling

A connection pool is a standard technique used to maintain
long running connections in memory for efficient reuse,
as well as to provide
management for the total number of connections an application
might use simultaneously.

Particularly for
server-side web applications, a connection pool is the standard way to
maintain a “pool” of active database connections in memory which are
reused across requests.

SQLAlchemy includes several connection pool implementations
which integrate with the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).  They can also be used
directly for applications that want to add pooling to an otherwise
plain DBAPI approach.

## Connection Pool Configuration

The [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) returned by the
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) function in most cases has a [QueuePool](#sqlalchemy.pool.QueuePool)
integrated, pre-configured with reasonable pooling defaults.  If
you’re reading this section only to learn how to enable pooling - congratulations!
You’re already done.

The most common [QueuePool](#sqlalchemy.pool.QueuePool) tuning parameters can be passed
directly to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) as keyword arguments:
`pool_size`, `max_overflow`, `pool_recycle` and
`pool_timeout`.  For example:

```
engine = create_engine(
    "postgresql+psycopg2://me@localhost/mydb", pool_size=20, max_overflow=0
)
```

All SQLAlchemy pool implementations have in common
that none of them “pre create” connections - all implementations wait
until first use before creating a connection.   At that point, if
no additional concurrent checkout requests for more connections
are made, no additional connections are created.   This is why it’s perfectly
fine for [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) to default to using a [QueuePool](#sqlalchemy.pool.QueuePool)
of size five without regard to whether or not the application really needs five connections
queued up - the pool would only grow to that size if the application
actually used five connections concurrently, in which case the usage of a
small pool is an entirely appropriate default behavior.

Note

The [QueuePool](#sqlalchemy.pool.QueuePool) class is **not compatible with asyncio**.
When using [create_async_engine](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) to create an instance of
[AsyncEngine](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncEngine), the [AsyncAdaptedQueuePool](#sqlalchemy.pool.AsyncAdaptedQueuePool) class,
which makes use of an asyncio-compatible queue implementation, is used
instead.

## Switching Pool Implementations

The usual way to use a different kind of pool with [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
is to use the `poolclass` argument.   This argument accepts a class
imported from the `sqlalchemy.pool` module, and handles the details
of building the pool for you.   A common use case here is when
connection pooling is to be disabled, which can be achieved by using
the [NullPool](#sqlalchemy.pool.NullPool) implementation:

```
from sqlalchemy.pool import NullPool

engine = create_engine(
    "postgresql+psycopg2://scott:tiger@localhost/test", poolclass=NullPool
)
```

## Using a Custom Connection Function

See the section [Custom DBAPI connect() arguments / on-connect routines](https://docs.sqlalchemy.org/en/20/core/engines.html#custom-dbapi-args) for a rundown of the various
connection customization routines.

## Constructing a Pool

To use a [Pool](#sqlalchemy.pool.Pool) by itself, the `creator` function is
the only argument that’s required and is passed first, followed
by any additional options:

```
import sqlalchemy.pool as pool
import psycopg2

def getconn():
    c = psycopg2.connect(user="ed", host="127.0.0.1", dbname="test")
    return c

mypool = pool.QueuePool(getconn, max_overflow=10, pool_size=5)
```

DBAPI connections can then be procured from the pool using the
[Pool.connect()](#sqlalchemy.pool.Pool.connect) function. The return value of this method is a DBAPI
connection that’s contained within a transparent proxy:

```
# get a connection
conn = mypool.connect()

# use it
cursor_obj = conn.cursor()
cursor_obj.execute("select foo")
```

The purpose of the transparent proxy is to intercept the `close()` call,
such that instead of the DBAPI connection being closed, it is returned to the
pool:

```
# "close" the connection.  Returns
# it to the pool.
conn.close()
```

The proxy also returns its contained DBAPI connection to the pool when it is
garbage collected, though it’s not deterministic in Python that this occurs
immediately (though it is typical with cPython). This usage is not recommended
however and in particular is not supported with asyncio DBAPI drivers.

## Reset On Return

The pool includes “reset on return” behavior which will call the `rollback()`
method of the DBAPI connection when the connection is returned to the pool.
This is so that any existing transactional state is removed from the
connection, which includes not just uncommitted data but table and row locks as
well. For most DBAPIs, the call to `rollback()` is relatively inexpensive.

The “reset on return” feature takes place when a connection is [released](https://docs.sqlalchemy.org/en/20/glossary.html#term-released)
back to the connection pool.  In modern SQLAlchemy, this reset on return
behavior is shared between the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and the [Pool](#sqlalchemy.pool.Pool),
where the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) itself, if it releases its transaction upon close,
considers `.rollback()` to have been called, and instructs the pool to skip
this step.

### Disabling Reset on Return for non-transactional connections

For very specific cases where this `rollback()` is not useful, such as when
using a connection that is configured for
[autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit-understanding) or when using a database
that has no ACID capabilities such as the MyISAM engine of MySQL, the
reset-on-return behavior can be disabled, which is typically done for
performance reasons.

As of SQLAlchemy 2.0.43, the [create_engine.skip_autocommit_rollback](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.skip_autocommit_rollback)
parameter of [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) provides the most complete means of
preventing ROLLBACK from being emitted while under autocommit mode, as it
blocks the DBAPI `.rollback()` method from being called by the dialect
completely:

```
autocommit_engine = create_engine(
    "mysql+mysqldb://scott:tiger@mysql80/test",
    skip_autocommit_rollback=True,
    isolation_level="AUTOCOMMIT",
)
```

Detail on this pattern is at [Fully preventing ROLLBACK calls under autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit-skip-rollback).

The [Pool](#sqlalchemy.pool.Pool) itself also has a parameter that can control its
“reset on return” behavior, noting that in modern SQLAlchemy this is not
the only path by which the DBAPI transaction is released, which is the
[Pool.reset_on_return](#sqlalchemy.pool.Pool.params.reset_on_return) parameter of [Pool](#sqlalchemy.pool.Pool), which
is also available from [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) as
[create_engine.pool_reset_on_return](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_reset_on_return), passing a value of `None`.
This pattern looks as below:

```
autocommit_engine = create_engine(
    "mysql+mysqldb://scott:tiger@mysql80/test",
    pool_reset_on_return=None,
    isolation_level="AUTOCOMMIT",
)
```

The above pattern will still see ROLLBACKs occur however as the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
object implicitly starts transaction blocks in the SQLAlchemy 2.0 series,
which still emit ROLLBACK independently of the pool’s reset sequence.

### Custom Reset-on-Return Schemes

“reset on return” consisting of a single `rollback()` may not be sufficient
for some use cases; in particular, applications which make use of temporary
tables may wish for these tables to be automatically removed on connection
checkin. Some (but notably not all) backends include features that can “reset”
such tables within the scope of a database connection, which may be a desirable
behavior for connection pool reset. Other server resources such as prepared
statement handles and server-side statement caches may persist beyond the
checkin process, which may or may not be desirable, depending on specifics.
Again, some (but again not all) backends may provide for a means of resetting
this state.  The two SQLAlchemy included dialects which are known to have
such reset schemes include Microsoft SQL Server, where an undocumented but
widely known stored procedure called `sp_reset_connection` is often used,
and PostgreSQL, which has a well-documented series of commands including
`DISCARD` `RESET`, `DEALLOCATE`, and `UNLISTEN`.

The following example illustrates how to replace reset on return with the
Microsoft SQL Server `sp_reset_connection` stored procedure, using the
[PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event hook. The
[create_engine.pool_reset_on_return](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_reset_on_return) parameter is set to `None`
so that the custom scheme can replace the default behavior completely. The
custom hook implementation calls `.rollback()` in any case, as it’s usually
important that the DBAPI’s own tracking of commit/rollback will remain
consistent with the state of the transaction:

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

- [Temporary Table / Resource Reset for Connection Pooling](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-reset-on-return) - in the [Microsoft SQL Server](https://docs.sqlalchemy.org/en/20/dialects/mssql.html) documentation
- [Temporary Table / Resource Reset for Connection Pooling](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-reset-on-return) in the [PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) documentation

### Logging reset-on-return events

Logging for pool events including reset on return can be set
`logging.DEBUG`
log level along with the `sqlalchemy.pool` logger, or by setting
[create_engine.echo_pool](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo_pool) to `"debug"` when using
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine):

```
>>> from sqlalchemy import create_engine
>>> engine = create_engine("postgresql://scott:tiger@localhost/test", echo_pool="debug")
```

The above pool will show verbose logging including reset on return:

```
>>> c1 = engine.connect()
DEBUG sqlalchemy.pool.impl.QueuePool Created new connection <connection object ...>
DEBUG sqlalchemy.pool.impl.QueuePool Connection <connection object ...> checked out from pool
>>> c1.close()
DEBUG sqlalchemy.pool.impl.QueuePool Connection <connection object ...> being returned to pool
DEBUG sqlalchemy.pool.impl.QueuePool Connection <connection object ...> rollback-on-return
```

## Pool Events

Connection pools support an event interface that allows hooks to execute
upon first connect, upon each new connection, and upon checkout and
checkin of connections.   See [PoolEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents) for details.

## Dealing with Disconnects

The connection pool has the ability to refresh individual connections as well as
its entire set of connections, setting the previously pooled connections as
“invalid”.   A common use case is allow the connection pool to gracefully recover
when the database server has been restarted, and all previously established connections
are no longer functional.   There are two approaches to this.

### Disconnect Handling - Pessimistic

The pessimistic approach refers to emitting a test statement on the SQL
connection at the start of each connection pool checkout, to test
that the database connection is still viable.   The implementation is
dialect-specific, and makes use of either a DBAPI-specific ping method,
or by using a simple SQL statement like “SELECT 1”, in order to test the
connection for liveness.

The approach adds a small bit of overhead to the connection checkout process,
however is otherwise the most simple and reliable approach to completely
eliminating database errors due to stale pooled connections.   The calling
application does not need to be concerned about organizing operations
to be able to recover from stale connections checked out from the pool.

Pessimistic testing of connections upon checkout is achievable by
using the [Pool.pre_ping](#sqlalchemy.pool.Pool.params.pre_ping) argument, available from [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
via the [create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) argument:

```
engine = create_engine("mysql+pymysql://user:pw@host/db", pool_pre_ping=True)
```

The “pre ping” feature operates on a per-dialect basis either by invoking a
DBAPI-specific “ping” method, or if not available will emit SQL equivalent to
“SELECT 1”, catching any errors and detecting the error as a “disconnect”
situation. If the ping / error check determines that the connection is not
usable, the connection will be immediately recycled, and all other pooled
connections older than the current time are invalidated, so that the next time
they are checked out, they will also be recycled before use.

If the database is still not available when “pre ping” runs, then the initial
connect will fail and the error for failure to connect will be propagated
normally.  In the uncommon situation that the database is available for
connections, but is not able to respond to a “ping”, the “pre_ping” will try up
to three times before giving up, propagating the database error last received.

It is critical to note that the pre-ping approach **does not accommodate for
connections dropped in the middle of transactions or other SQL operations**. If
the database becomes unavailable while a transaction is in progress, the
transaction will be lost and the database error will be raised.   While the
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object will detect a “disconnect” situation and
recycle the connection as well as invalidate the rest of the connection pool
when this condition occurs, the individual operation where the exception was
raised will be lost, and it’s up to the application to either abandon the
operation, or retry the whole transaction again.  If the engine is
configured using DBAPI-level autocommit connections, as described at
[Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit), a connection **may** be reconnected transparently
mid-operation using events.  See the section [How Do I “Retry” a Statement Execution Automatically?](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-execute-retry) for
an example.

For dialects that make use of “SELECT 1” and catch errors in order to detect
disconnects, the disconnection test may be augmented for new backend-specific
error messages using the [DialectEvents.handle_error()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.handle_error) hook.

#### Custom / Legacy Pessimistic Ping

Before [create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) was added, the “pre-ping”
approach historically has been performed manually using
the [ConnectionEvents.engine_connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.engine_connect) engine event.
The most common recipe for this is below, for reference
purposes in case an application is already using such a recipe, or special
behaviors are needed:

```
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select

some_engine = create_engine(...)

@event.listens_for(some_engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # this parameter is always False as of SQLAlchemy 2.0,
        # but is still accepted by the event hook.  In 1.x versions
        # of SQLAlchemy, "branched" connections should be skipped.
        return

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select(1))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select(1))
        else:
            raise
```

The above recipe has the advantage that we are making use of SQLAlchemy’s
facilities for detecting those DBAPI exceptions that are known to indicate
a “disconnect” situation, as well as the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object’s ability
to correctly invalidate the current connection pool when this condition
occurs and allowing the current [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) to re-validate onto
a new DBAPI connection.

### Disconnect Handling - Optimistic

When pessimistic handling is not employed, as well as when the database is
shutdown and/or restarted in the middle of a connection’s period of use within
a transaction, the other approach to dealing with stale / closed connections is
to let SQLAlchemy handle disconnects as  they occur, at which point all
connections in the pool are invalidated, meaning they are assumed to be
stale and will be refreshed upon next checkout.  This behavior assumes the
[Pool](#sqlalchemy.pool.Pool) is used in conjunction with a [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).
The [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) has logic which can detect
disconnection events and refresh the pool automatically.

When the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) attempts to use a DBAPI connection, and an
exception is raised that corresponds to a “disconnect” event, the connection
is invalidated. The [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) then calls the [Pool.recreate()](#sqlalchemy.pool.Pool.recreate)
method, effectively invalidating all connections not currently checked out so
that they are replaced with new ones upon next checkout.  This flow is
illustrated by the code example below:

```
from sqlalchemy import create_engine, exc

e = create_engine(...)
c = e.connect()

try:
    # suppose the database has been restarted.
    c.execute(text("SELECT * FROM table"))
    c.close()
except exc.DBAPIError as e:
    # an exception is raised, Connection is invalidated.
    if e.connection_invalidated:
        print("Connection was invalidated!")

# after the invalidate event, a new connection
# starts with a new Pool
c = e.connect()
c.execute(text("SELECT * FROM table"))
```

The above example illustrates that no special intervention is needed to
refresh the pool, which continues normally after a disconnection event is
detected.   However, one database exception is raised, per each connection
that is in use while the database unavailability event occurred.
In a typical web application using an ORM Session, the above condition would
correspond to a single request failing with a 500 error, then the web application
continuing normally beyond that.   Hence the approach is “optimistic” in that frequent
database restarts are not anticipated.

#### Setting Pool Recycle

An additional setting that can augment the “optimistic” approach is to set the
pool recycle parameter.   This parameter prevents the pool from using a particular
connection that has passed a certain age, and is appropriate for database backends
such as MySQL that automatically close connections that have been stale after a particular
period of time:

```
from sqlalchemy import create_engine

e = create_engine("mysql+mysqldb://scott:tiger@localhost/test", pool_recycle=3600)
```

Above, any DBAPI connection that has been open for more than one hour will be invalidated and replaced,
upon next checkout.   Note that the invalidation **only** occurs during checkout - not on
any connections that are held in a checked out state.     `pool_recycle` is a function
of the [Pool](#sqlalchemy.pool.Pool) itself, independent of whether or not an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) is in use.

### More on Invalidation

The [Pool](#sqlalchemy.pool.Pool) provides “connection invalidation” services which allow
both explicit invalidation of a connection as well as automatic invalidation
in response to conditions that are determined to render a connection unusable.

“Invalidation” means that a particular DBAPI connection is removed from the
pool and discarded.  The `.close()` method is called on this connection
if it is not clear that the connection itself might not be closed, however
if this method fails, the exception is logged but the operation still proceeds.

When using a [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), the [Connection.invalidate()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.invalidate) method is
the usual entrypoint to explicit invalidation.   Other conditions by which
a DBAPI connection might be invalidated include:

- a DBAPI exception such as [OperationalError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.OperationalError), raised when a
  method like `connection.execute()` is called, is detected as indicating
  a so-called “disconnect” condition.   As the Python DBAPI provides no
  standard system for determining the nature of an exception, all SQLAlchemy
  dialects include a system called `is_disconnect()` which will examine
  the contents of an exception object, including the string message and
  any potential error codes included with it, in order to determine if this
  exception indicates that the connection is no longer usable.  If this is the
  case, the `_ConnectionFairy.invalidate()` method is called and the
  DBAPI connection is then discarded.
- When the connection is returned to the pool, and
  calling the `connection.rollback()` or `connection.commit()` methods,
  as dictated by the pool’s “reset on return” behavior, throws an exception.
  A final attempt at calling `.close()` on the connection will be made,
  and it is then discarded.
- When a listener implementing [PoolEvents.checkout()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.checkout) raises the
  [DisconnectionError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DisconnectionError) exception, indicating that the connection
  won’t be usable and a new connection attempt needs to be made.

All invalidations which occur will invoke the [PoolEvents.invalidate()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.invalidate)
event.

### Supporting new database error codes for disconnect scenarios

SQLAlchemy dialects each include a routine called `is_disconnect()` that is
invoked whenever a DBAPI exception is encountered. The DBAPI exception object
is passed to this method, where dialect-specific heuristics will then determine
if the error code received indicates that the database connection has been
“disconnected”, or is in an otherwise unusable state which indicates it should
be recycled. The heuristics applied here may be customized using the
[DialectEvents.handle_error()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.handle_error) event hook, which is typically
established via the owning [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object. Using this hook, all
errors which occur are delivered passing along a contextual object known as
[ExceptionContext](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext). Custom event hooks may control whether or not a
particular error should be considered a “disconnect” situation or not, as well
as if this disconnect should cause the entire connection pool to be invalidated
or not.

For example, to add support to consider the Oracle Database driver error codes
`DPY-1001` and `DPY-4011` to be handled as disconnect codes, apply an event
handler to the engine after creation:

```
import re

from sqlalchemy import create_engine

engine = create_engine(
    "oracle+oracledb://scott:tiger@localhost:1521?service_name=freepdb1"
)

@event.listens_for(engine, "handle_error")
def handle_exception(context: ExceptionContext) -> None:
    if not context.is_disconnect and re.match(
        r"^(?:DPY-1001|DPY-4011)", str(context.original_exception)
    ):
        context.is_disconnect = True

    return None
```

The above error processing function will be invoked for all Oracle Database
errors raised, including those caught when using the [pool pre ping](#pool-disconnects-pessimistic) feature for those backends that rely upon
disconnect error handling (new in 2.0).

See also

[DialectEvents.handle_error()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.handle_error)

## Using FIFO vs. LIFO

The [QueuePool](#sqlalchemy.pool.QueuePool) class features a flag called
[QueuePool.use_lifo](#sqlalchemy.pool.QueuePool.params.use_lifo), which can also be accessed from
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) via the flag [create_engine.pool_use_lifo](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_use_lifo).
Setting this flag to `True` causes the pool’s “queue” behavior to instead be
that of a “stack”, e.g. the last connection to be returned to the pool is the
first one to be used on the next request. In contrast to the pool’s long-
standing behavior of first-in-first-out, which produces a round-robin effect of
using each connection in the pool in series, lifo mode allows excess
connections to remain idle in the pool, allowing server-side timeout schemes to
close these connections out.   The difference between FIFO and LIFO is
basically whether or not its desirable for the pool to keep a full set of
connections ready to go even during idle periods:

```
engine = create_engine("postgresql://", pool_use_lifo=True, pool_pre_ping=True)
```

Above, we also make use of the [create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) flag
so that connections which are closed from the server side are gracefully
handled by the connection pool and replaced with a new connection.

Note that the flag only applies to [QueuePool](#sqlalchemy.pool.QueuePool) use.

Added in version 1.3.

See also

[Dealing with Disconnects](#pool-disconnects)

## Using Connection Pools with Multiprocessing or os.fork()

It’s critical that when using a connection pool, and by extension when
using an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) created via [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine), that
the pooled connections **are not shared to a forked process**.  TCP connections
are represented as file descriptors, which usually work across process
boundaries, meaning this will cause concurrent access to the file descriptor
on behalf of two or more entirely independent Python interpreter states.

Depending on specifics of the driver and OS, the issues that arise here range
from non-working connections to socket connections that are used by multiple
processes concurrently, leading to broken messaging (the latter case is
typically the most common).

The SQLAlchemy [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object refers to a connection pool of existing
database connections.  So when this object is replicated to a child process,
the goal is to ensure that no database connections are carried over.  There
are four general approaches to this:

1. Disable pooling using [NullPool](#sqlalchemy.pool.NullPool).  This is the most simplistic,
  one shot system that prevents the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) from using any connection
  more than once:
  ```
  from sqlalchemy.pool import NullPool
  engine = create_engine("mysql+mysqldb://user:pass@host/dbname", poolclass=NullPool)
  ```
2. Call [Engine.dispose()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose) on any given [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
  passing the [Engine.dispose.close](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose.params.close) parameter with a value of
  `False`, within the initialize phase of the child process.  This is
  so that the new process will not touch any of the parent process’ connections
  and will instead start with new connections.
  **This is the recommended approach**:
  ```
  from multiprocessing import Pool
  engine = create_engine("mysql+mysqldb://user:pass@host/dbname")
  def run_in_process(some_data_record):
      with engine.connect() as conn:
          conn.execute(text("..."))
  def initializer():
      """ensure the parent proc's database connections are not touched
      in the new connection pool"""
      engine.dispose(close=False)
  with Pool(10, initializer=initializer) as p:
      p.map(run_in_process, data)
  ```
  Added in version 1.4.33: Added the [Engine.dispose.close](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose.params.close)
  parameter to allow the replacement of a connection pool in a child
  process without interfering with the connections used by the parent
  process.
3. Call [Engine.dispose()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose) **directly before** the child process is
  created.  This will also cause the child process to start with a new
  connection pool, while ensuring the parent connections are not transferred
  to the child process:
  ```
  engine = create_engine("mysql://user:pass@host/dbname")
  def run_in_process():
      with engine.connect() as conn:
          conn.execute(text("..."))
  # before process starts, ensure engine.dispose() is called
  engine.dispose()
  p = Process(target=run_in_process)
  p.start()
  ```
4. An event handler can be applied to the connection pool that tests for
  connections being shared across process boundaries, and invalidates them:
  ```
  from sqlalchemy import event
  from sqlalchemy import exc
  import os
  engine = create_engine("...")
  @event.listens_for(engine, "connect")
  def connect(dbapi_connection, connection_record):
      connection_record.info["pid"] = os.getpid()
  @event.listens_for(engine, "checkout")
  def checkout(dbapi_connection, connection_record, connection_proxy):
      pid = os.getpid()
      if connection_record.info["pid"] != pid:
          connection_record.dbapi_connection = connection_proxy.dbapi_connection = None
          raise exc.DisconnectionError(
              "Connection record belongs to pid %s, "
              "attempting to check out in pid %s" % (connection_record.info["pid"], pid)
          )
  ```
  Above, we use an approach similar to that described in
  [Disconnect Handling - Pessimistic](#pool-disconnects-pessimistic) to treat a DBAPI connection that
  originated in a different parent process as an “invalid” connection,
  coercing the pool to recycle the connection record to make a new connection.

The above strategies will accommodate the case of an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
being shared among processes. The above steps alone are not sufficient for the
case of sharing a specific [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) over a process boundary;
prefer to keep the scope of a particular [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) local to a
single process (and thread). It’s additionally not supported to share any kind
of ongoing transactional state directly across a process boundary, such as an
ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object that’s begun a transaction and references
active `Connection` instances; again prefer to create new
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects in new processes.

## Using a pool instance directly

A pool implementation can be used directly without an engine. This could be used
in applications that just wish to use the pool behavior without all other
SQLAlchemy features.
In the example below the default pool for the `MySQLdb` dialect is obtained using
[create_pool_from_url()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_pool_from_url):

```
from sqlalchemy import create_pool_from_url

my_pool = create_pool_from_url(
    "mysql+mysqldb://", max_overflow=5, pool_size=5, pre_ping=True
)

con = my_pool.connect()
# use the connection
...
# then close it
con.close()
```

If the type of pool to create is not specified, the default one for the dialect
will be used. To specify it directly the `poolclass` argument can be used,
like in the following example:

```
from sqlalchemy import create_pool_from_url
from sqlalchemy import NullPool

my_pool = create_pool_from_url("mysql+mysqldb://", poolclass=NullPool)
```

## API Documentation - Available Pool Implementations

| Object Name | Description |
| --- | --- |
| _ConnectionFairy | Proxies a DBAPI connection and provides return-on-dereference
support. |
| _ConnectionRecord | Maintains a position in a connection pool which references a pooled
connection. |
| AssertionPool | APoolthat allows at most one checked out connection at
any given time. |
| AsyncAdaptedQueuePool | An asyncio-compatible version ofQueuePool. |
| ConnectionPoolEntry | Interface for the object that maintains an individual database
connection on behalf of aPoolinstance. |
| ManagesConnection | Common base for the two connection-management interfacesPoolProxiedConnectionandConnectionPoolEntry. |
| NullPool | A Pool which does not pool connections. |
| Pool | Abstract base class for connection pools. |
| PoolProxiedConnection | A connection-like adapter for aPEP 249DBAPI connection, which
includes additional methods specific to thePoolimplementation. |
| QueuePool | APoolthat imposes a limit on the number of open connections. |
| SingletonThreadPool | A Pool that maintains one connection per thread. |
| StaticPool | A Pool of exactly one connection, used for all requests. |

   class sqlalchemy.pool.Pool

*inherits from* [sqlalchemy.log.Identified](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.log.Identified), `sqlalchemy.event.registry.EventTarget`

Abstract base class for connection pools.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Pool. |
| connect() | Return a DBAPI connection from the pool. |
| dispose() | Dispose of this pool. |
| recreate() | Return a newPool, of the same class as this one
and configured with identical creation arguments. |
| status() | Returns a brief description of the state of this pool. |

   method [sqlalchemy.pool.Pool.](#sqlalchemy.pool.Pool)__init__(*creator:_CreatorFnType|_CreatorWRecFnType*, *recycle:int=-1*, *echo:log._EchoFlagType=None*, *logging_name:str|None=None*, *reset_on_return:_ResetStyleArgType=True*, *events:List[Tuple[_ListenerFnType,str]]|None=None*, *dialect:_ConnDialect|Dialect|None=None*, *pre_ping:bool=False*, *_dispatch:_DispatchCommon[Pool]|None=None*)

Construct a Pool.

  Parameters:

- **creator** – a callable function that returns a DB-API
  connection object.  The function will be called with
  parameters.
- **recycle** – If set to a value other than -1, number of
  seconds between connection recycling, which means upon
  checkout, if this timeout is surpassed the connection will be
  closed and replaced with a newly opened connection. Defaults to -1.
- **logging_name** – String identifier which will be used within
  the “name” field of logging records generated within the
  “sqlalchemy.pool” logger. Defaults to a hexstring of the object’s
  id.
- **echo** –
  if True, the connection pool will log
  informational output such as when connections are invalidated
  as well as when connections are recycled to the default log handler,
  which defaults to `sys.stdout` for output..   If set to the string
  `"debug"`, the logging will include pool checkouts and checkins.
  The [Pool.echo](#sqlalchemy.pool.Pool.params.echo) parameter can also be set from the
  [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) call by using the
  [create_engine.echo_pool](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo_pool) parameter.
  See also
  [Configuring Logging](https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging) - further detail on how to configure
  logging.
- **reset_on_return** –
  Determine steps to take on
  connections as they are returned to the pool, which were
  not otherwise handled by a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
  Available from [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) via the
  [create_engine.pool_reset_on_return](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_reset_on_return) parameter.
  [Pool.reset_on_return](#sqlalchemy.pool.Pool.params.reset_on_return) can have any of these values:
  - `"rollback"` - call rollback() on the connection,
    to release locks and transaction resources.
    This is the default value.  The vast majority
    of use cases should leave this value set.
  - `"commit"` - call commit() on the connection,
    to release locks and transaction resources.
    A commit here may be desirable for databases that
    cache query plans if a commit is emitted,
    such as Microsoft SQL Server.  However, this
    value is more dangerous than ‘rollback’ because
    any data changes present on the transaction
    are committed unconditionally.
  - `None` - don’t do anything on the connection.
    This setting may be appropriate if the database / DBAPI
    works in pure “autocommit” mode at all times, or if
    a custom reset handler is established using the
    [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event handler.
  - `True` - same as ‘rollback’, this is here for
    backwards compatibility.
  - `False` - same as None, this is here for
    backwards compatibility.
  For further customization of reset on return, the
  [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event hook may be used which can perform
  any connection activity desired on reset.
  See also
  [Reset On Return](#pool-reset-on-return)
  [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset)
- **events** – a list of 2-tuples, each of the form
  `(callable, target)` which will be passed to [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen)
  upon construction.   Provided here so that event listeners
  can be assigned via [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) before dialect-level
  listeners are applied.
- **dialect** – a [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) that will handle the job
  of calling rollback(), close(), or commit() on DBAPI connections.
  If omitted, a built-in “stub” dialect is used.   Applications that
  make use of [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) should not use this parameter
  as it is handled by the engine creation strategy.
- **pre_ping** –
  if True, the pool will emit a “ping” (typically
  “SELECT 1”, but is dialect-specific) on the connection
  upon checkout, to test if the connection is alive or not.   If not,
  the connection is transparently re-connected and upon success, all
  other pooled connections established prior to that timestamp are
  invalidated.     Requires that a dialect is passed as well to
  interpret the disconnection error.
  Added in version 1.2.

      method [sqlalchemy.pool.Pool.](#sqlalchemy.pool.Pool)connect() → [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection)

Return a DBAPI connection from the pool.

The connection is instrumented such that when its
`close()` method is called, the connection will be returned to
the pool.

    method [sqlalchemy.pool.Pool.](#sqlalchemy.pool.Pool)dispose() → None

Dispose of this pool.

This method leaves the possibility of checked-out connections
remaining open, as it only affects connections that are
idle in the pool.

See also

[Pool.recreate()](#sqlalchemy.pool.Pool.recreate)

     method [sqlalchemy.pool.Pool.](#sqlalchemy.pool.Pool)recreate() → [Pool](#sqlalchemy.pool.Pool)

Return a new [Pool](#sqlalchemy.pool.Pool), of the same class as this one
and configured with identical creation arguments.

This method is used in conjunction with [dispose()](#sqlalchemy.pool.Pool.dispose)
to close out an entire [Pool](#sqlalchemy.pool.Pool) and create a new one in
its place.

    method [sqlalchemy.pool.Pool.](#sqlalchemy.pool.Pool)status() → str

Returns a brief description of the state of this pool.

     class sqlalchemy.pool.QueuePool

*inherits from* [sqlalchemy.pool.base.Pool](#sqlalchemy.pool.Pool)

A [Pool](#sqlalchemy.pool.Pool)
that imposes a limit on the number of open connections.

[QueuePool](#sqlalchemy.pool.QueuePool) is the default pooling implementation used for
all [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) objects other than SQLite with a `:memory:`
database.

The [QueuePool](#sqlalchemy.pool.QueuePool) class **is not compatible** with asyncio and
[create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine).  The
[AsyncAdaptedQueuePool](#sqlalchemy.pool.AsyncAdaptedQueuePool) class is used automatically when
using [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine), if no other kind of pool
is specified.

See also

[AsyncAdaptedQueuePool](#sqlalchemy.pool.AsyncAdaptedQueuePool)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a QueuePool. |
| dispose() | Dispose of this pool. |
| recreate() | Return a newPool, of the same class as this one
and configured with identical creation arguments. |
| status() | Returns a brief description of the state of this pool. |

   method [sqlalchemy.pool.QueuePool.](#sqlalchemy.pool.QueuePool)__init__(*creator:_CreatorFnType|_CreatorWRecFnType*, *pool_size:int=5*, *max_overflow:int=10*, *timeout:float=30.0*, *use_lifo:bool=False*, ***kw:Any*)

Construct a QueuePool.

  Parameters:

- **creator** – a callable function that returns a DB-API
  connection object, same as that of [Pool.creator](#sqlalchemy.pool.Pool.params.creator).
- **pool_size** – The size of the pool to be maintained,
  defaults to 5. This is the largest number of connections that
  will be kept persistently in the pool. Note that the pool
  begins with no connections; once this number of connections
  is requested, that number of connections will remain.
  `pool_size` can be set to 0 to indicate no size limit; to
  disable pooling, use a [NullPool](#sqlalchemy.pool.NullPool)
  instead.
- **max_overflow** – The maximum overflow size of the
  pool. When the number of checked-out connections reaches the
  size set in pool_size, additional connections will be
  returned up to this limit. When those additional connections
  are returned to the pool, they are disconnected and
  discarded. It follows then that the total number of
  simultaneous connections the pool will allow is pool_size +
  max_overflow, and the total number of “sleeping”
  connections the pool will allow is pool_size. max_overflow
  can be set to -1 to indicate no overflow limit; no limit
  will be placed on the total number of concurrent
  connections. Defaults to 10.
- **timeout** – The number of seconds to wait before giving up
  on returning a connection. Defaults to 30.0. This can be a float
  but is subject to the limitations of Python time functions which
  may not be reliable in the tens of milliseconds.
- **use_lifo** –
  use LIFO (last-in-first-out) when retrieving
  connections instead of FIFO (first-in-first-out). Using LIFO, a
  server-side timeout scheme can reduce the number of connections used
  during non-peak periods of use.   When planning for server-side
  timeouts, ensure that a recycle or pre-ping strategy is in use to
  gracefully handle stale connections.
  Added in version 1.3.
  See also
  [Using FIFO vs. LIFO](#pool-use-lifo)
  [Dealing with Disconnects](#pool-disconnects)
- ****kw** – Other keyword arguments including
  [Pool.recycle](#sqlalchemy.pool.Pool.params.recycle), [Pool.echo](#sqlalchemy.pool.Pool.params.echo),
  [Pool.reset_on_return](#sqlalchemy.pool.Pool.params.reset_on_return) and others are passed to the
  [Pool](#sqlalchemy.pool.Pool) constructor.

      method [sqlalchemy.pool.QueuePool.](#sqlalchemy.pool.QueuePool)dispose() → None

Dispose of this pool.

This method leaves the possibility of checked-out connections
remaining open, as it only affects connections that are
idle in the pool.

See also

[Pool.recreate()](#sqlalchemy.pool.Pool.recreate)

     method [sqlalchemy.pool.QueuePool.](#sqlalchemy.pool.QueuePool)recreate() → [QueuePool](#sqlalchemy.pool.QueuePool)

Return a new [Pool](#sqlalchemy.pool.Pool), of the same class as this one
and configured with identical creation arguments.

This method is used in conjunction with [dispose()](#sqlalchemy.pool.QueuePool.dispose)
to close out an entire [Pool](#sqlalchemy.pool.Pool) and create a new one in
its place.

    method [sqlalchemy.pool.QueuePool.](#sqlalchemy.pool.QueuePool)status() → str

Returns a brief description of the state of this pool.

     class sqlalchemy.pool.AsyncAdaptedQueuePool

*inherits from* [sqlalchemy.pool.impl.QueuePool](#sqlalchemy.pool.QueuePool)

An asyncio-compatible version of [QueuePool](#sqlalchemy.pool.QueuePool).

This pool is used by default when using [AsyncEngine](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncEngine) engines that
were generated from [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine).   It uses an
asyncio-compatible queue implementation that does not use
`threading.Lock`.

The arguments and operation of [AsyncAdaptedQueuePool](#sqlalchemy.pool.AsyncAdaptedQueuePool) are
otherwise identical to that of [QueuePool](#sqlalchemy.pool.QueuePool).

    class sqlalchemy.pool.SingletonThreadPool

*inherits from* [sqlalchemy.pool.base.Pool](#sqlalchemy.pool.Pool)

A Pool that maintains one connection per thread.

Maintains one connection per each thread, never moving a connection to a
thread other than the one which it was created in.

Warning

the [SingletonThreadPool](#sqlalchemy.pool.SingletonThreadPool) will call `.close()`
on arbitrary connections that exist beyond the size setting of
`pool_size`, e.g. if more unique **thread identities**
than what `pool_size` states are used.   This cleanup is
non-deterministic and not sensitive to whether or not the connections
linked to those thread identities are currently in use.

[SingletonThreadPool](#sqlalchemy.pool.SingletonThreadPool) may be improved in a future release,
however in its current status it is generally used only for test
scenarios using a SQLite `:memory:` database and is not recommended
for production use.

The [SingletonThreadPool](#sqlalchemy.pool.SingletonThreadPool) class **is not compatible** with asyncio
and [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine).

Options are the same as those of [Pool](#sqlalchemy.pool.Pool), as well as:

  Parameters:

**pool_size** – The number of threads in which to maintain connections
at once.  Defaults to five.

[SingletonThreadPool](#sqlalchemy.pool.SingletonThreadPool) is used by the SQLite dialect
automatically when a memory-based database is used.
See [SQLite](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html).

| Member Name | Description |
| --- | --- |
| connect() | Return a DBAPI connection from the pool. |
| dispose() | Dispose of this pool. |
| recreate() | Return a newPool, of the same class as this one
and configured with identical creation arguments. |
| status() | Returns a brief description of the state of this pool. |

   method [sqlalchemy.pool.SingletonThreadPool.](#sqlalchemy.pool.SingletonThreadPool)connect() → [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection)

Return a DBAPI connection from the pool.

The connection is instrumented such that when its
`close()` method is called, the connection will be returned to
the pool.

    method [sqlalchemy.pool.SingletonThreadPool.](#sqlalchemy.pool.SingletonThreadPool)dispose() → None

Dispose of this pool.

    method [sqlalchemy.pool.SingletonThreadPool.](#sqlalchemy.pool.SingletonThreadPool)recreate() → [SingletonThreadPool](#sqlalchemy.pool.SingletonThreadPool)

Return a new [Pool](#sqlalchemy.pool.Pool), of the same class as this one
and configured with identical creation arguments.

This method is used in conjunction with [dispose()](#sqlalchemy.pool.SingletonThreadPool.dispose)
to close out an entire [Pool](#sqlalchemy.pool.Pool) and create a new one in
its place.

    method [sqlalchemy.pool.SingletonThreadPool.](#sqlalchemy.pool.SingletonThreadPool)status() → str

Returns a brief description of the state of this pool.

     class sqlalchemy.pool.AssertionPool

*inherits from* [sqlalchemy.pool.base.Pool](#sqlalchemy.pool.Pool)

A [Pool](#sqlalchemy.pool.Pool) that allows at most one checked out connection at
any given time.

This will raise an exception if more than one connection is checked out
at a time.  Useful for debugging code that is using more connections
than desired.

The [AssertionPool](#sqlalchemy.pool.AssertionPool) class **is compatible** with asyncio and
[create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine).

| Member Name | Description |
| --- | --- |
| dispose() | Dispose of this pool. |
| recreate() | Return a newPool, of the same class as this one
and configured with identical creation arguments. |
| status() | Returns a brief description of the state of this pool. |

   method [sqlalchemy.pool.AssertionPool.](#sqlalchemy.pool.AssertionPool)dispose() → None

Dispose of this pool.

This method leaves the possibility of checked-out connections
remaining open, as it only affects connections that are
idle in the pool.

See also

[Pool.recreate()](#sqlalchemy.pool.Pool.recreate)

     method [sqlalchemy.pool.AssertionPool.](#sqlalchemy.pool.AssertionPool)recreate() → [AssertionPool](#sqlalchemy.pool.AssertionPool)

Return a new [Pool](#sqlalchemy.pool.Pool), of the same class as this one
and configured with identical creation arguments.

This method is used in conjunction with [dispose()](#sqlalchemy.pool.AssertionPool.dispose)
to close out an entire [Pool](#sqlalchemy.pool.Pool) and create a new one in
its place.

    method [sqlalchemy.pool.AssertionPool.](#sqlalchemy.pool.AssertionPool)status() → str

Returns a brief description of the state of this pool.

     class sqlalchemy.pool.NullPool

*inherits from* [sqlalchemy.pool.base.Pool](#sqlalchemy.pool.Pool)

A Pool which does not pool connections.

Instead it literally opens and closes the underlying DB-API connection
per each connection open/close.

Reconnect-related functions such as `recycle` and connection
invalidation are not supported by this Pool implementation, since
no connections are held persistently.

The [NullPool](#sqlalchemy.pool.NullPool) class **is compatible** with asyncio and
[create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine).

| Member Name | Description |
| --- | --- |
| dispose() | Dispose of this pool. |
| recreate() | Return a newPool, of the same class as this one
and configured with identical creation arguments. |
| status() | Returns a brief description of the state of this pool. |

   method [sqlalchemy.pool.NullPool.](#sqlalchemy.pool.NullPool)dispose() → None

Dispose of this pool.

This method leaves the possibility of checked-out connections
remaining open, as it only affects connections that are
idle in the pool.

See also

[Pool.recreate()](#sqlalchemy.pool.Pool.recreate)

     method [sqlalchemy.pool.NullPool.](#sqlalchemy.pool.NullPool)recreate() → [NullPool](#sqlalchemy.pool.NullPool)

Return a new [Pool](#sqlalchemy.pool.Pool), of the same class as this one
and configured with identical creation arguments.

This method is used in conjunction with [dispose()](#sqlalchemy.pool.NullPool.dispose)
to close out an entire [Pool](#sqlalchemy.pool.Pool) and create a new one in
its place.

    method [sqlalchemy.pool.NullPool.](#sqlalchemy.pool.NullPool)status() → str

Returns a brief description of the state of this pool.

     class sqlalchemy.pool.StaticPool

*inherits from* [sqlalchemy.pool.base.Pool](#sqlalchemy.pool.Pool)

A Pool of exactly one connection, used for all requests.

Reconnect-related functions such as `recycle` and connection
invalidation (which is also used to support auto-reconnect) are only
partially supported right now and may not yield good results.

The [StaticPool](#sqlalchemy.pool.StaticPool) class **is compatible** with asyncio and
[create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine).

| Member Name | Description |
| --- | --- |
| dispose() | Dispose of this pool. |
| recreate() | Return a newPool, of the same class as this one
and configured with identical creation arguments. |
| status() | Returns a brief description of the state of this pool. |

   method [sqlalchemy.pool.StaticPool.](#sqlalchemy.pool.StaticPool)dispose() → None

Dispose of this pool.

This method leaves the possibility of checked-out connections
remaining open, as it only affects connections that are
idle in the pool.

See also

[Pool.recreate()](#sqlalchemy.pool.Pool.recreate)

     method [sqlalchemy.pool.StaticPool.](#sqlalchemy.pool.StaticPool)recreate() → [StaticPool](#sqlalchemy.pool.StaticPool)

Return a new [Pool](#sqlalchemy.pool.Pool), of the same class as this one
and configured with identical creation arguments.

This method is used in conjunction with [dispose()](#sqlalchemy.pool.StaticPool.dispose)
to close out an entire [Pool](#sqlalchemy.pool.Pool) and create a new one in
its place.

    method [sqlalchemy.pool.StaticPool.](#sqlalchemy.pool.StaticPool)status() → str

Returns a brief description of the state of this pool.

     class sqlalchemy.pool.ManagesConnection

Common base for the two connection-management interfaces
[PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) and [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry).

These two objects are typically exposed in the public facing API
via the connection pool event hooks, documented at [PoolEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents).

Added in version 2.0.

| Member Name | Description |
| --- | --- |
| dbapi_connection | A reference to the actual DBAPI connection being tracked. |
| driver_connection | The “driver level” connection object as used by the Python
DBAPI or database driver. |
| info | Info dictionary associated with the underlying DBAPI connection
referred to by thisManagesConnectioninstance, allowing
user-defined data to be associated with the connection. |
| invalidate() | Mark the managed connection as invalidated. |
| record_info | Persistent info dictionary associated with thisManagesConnection. |

   attribute [sqlalchemy.pool.ManagesConnection.](#sqlalchemy.pool.ManagesConnection)dbapi_connection: [DBAPIConnection](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPIConnection) | None

A reference to the actual DBAPI connection being tracked.

This is a [PEP 249](https://peps.python.org/pep-0249/)-compliant object that for traditional sync-style
dialects is provided by the third-party
DBAPI implementation in use.  For asyncio dialects, the implementation
is typically an adapter object provided by the SQLAlchemy dialect
itself; the underlying asyncio object is available via the
[ManagesConnection.driver_connection](#sqlalchemy.pool.ManagesConnection.driver_connection) attribute.

SQLAlchemy’s interface for the DBAPI connection is based on the
[DBAPIConnection](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPIConnection) protocol object

See also

[ManagesConnection.driver_connection](#sqlalchemy.pool.ManagesConnection.driver_connection)

[How do I get at the raw DBAPI connection when using an Engine?](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-dbapi-connection)

     attribute [sqlalchemy.pool.ManagesConnection.](#sqlalchemy.pool.ManagesConnection)driver_connection: Any | None

The “driver level” connection object as used by the Python
DBAPI or database driver.

For traditional [PEP 249](https://peps.python.org/pep-0249/) DBAPI implementations, this object will
be the same object as that of
[ManagesConnection.dbapi_connection](#sqlalchemy.pool.ManagesConnection.dbapi_connection).   For an asyncio database
driver, this will be the ultimate “connection” object used by that
driver, such as the `asyncpg.Connection` object which will not have
standard pep-249 methods.

Added in version 1.4.24.

See also

[ManagesConnection.dbapi_connection](#sqlalchemy.pool.ManagesConnection.dbapi_connection)

[How do I get at the raw DBAPI connection when using an Engine?](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-dbapi-connection)

     attribute [sqlalchemy.pool.ManagesConnection.](#sqlalchemy.pool.ManagesConnection)info

Info dictionary associated with the underlying DBAPI connection
referred to by this [ManagesConnection](#sqlalchemy.pool.ManagesConnection) instance, allowing
user-defined data to be associated with the connection.

The data in this dictionary is persistent for the lifespan
of the DBAPI connection itself, including across pool checkins
and checkouts.  When the connection is invalidated
and replaced with a new one, this dictionary is cleared.

For a [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) instance that’s not associated
with a [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry), such as if it were detached, the
attribute returns a dictionary that is local to that
[ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry). Therefore the
[ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info) attribute will always provide a Python
dictionary.

See also

[ManagesConnection.record_info](#sqlalchemy.pool.ManagesConnection.record_info)

     method [sqlalchemy.pool.ManagesConnection.](#sqlalchemy.pool.ManagesConnection)invalidate(*e:BaseException|None=None*, *soft:bool=False*) → None

Mark the managed connection as invalidated.

  Parameters:

- **e** – an exception object indicating a reason for the invalidation.
- **soft** – if True, the connection isn’t closed; instead, this
  connection will be recycled on next checkout.

See also

[More on Invalidation](#pool-connection-invalidation)

     attribute [sqlalchemy.pool.ManagesConnection.](#sqlalchemy.pool.ManagesConnection)record_info

Persistent info dictionary associated with this
[ManagesConnection](#sqlalchemy.pool.ManagesConnection).

Unlike the [ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info) dictionary, the lifespan
of this dictionary is that of the [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry)
which owns it; therefore this dictionary will persist across
reconnects and connection invalidation for a particular entry
in the connection pool.

For a [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) instance that’s not associated
with a [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry), such as if it were detached, the
attribute returns None. Contrast to the [ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info)
dictionary which is never None.

See also

[ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info)

      class sqlalchemy.pool.ConnectionPoolEntry

*inherits from* [sqlalchemy.pool.base.ManagesConnection](#sqlalchemy.pool.ManagesConnection)

Interface for the object that maintains an individual database
connection on behalf of a [Pool](#sqlalchemy.pool.Pool) instance.

The [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry) object represents the long term
maintenance of a particular connection for a pool, including expiring or
invalidating that connection to have it replaced with a new one, which will
continue to be maintained by that same [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry)
instance. Compared to [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection), which is the
short-term, per-checkout connection manager, this object lasts for the
lifespan of a particular “slot” within a connection pool.

The [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry) object is mostly visible to public-facing
API code when it is delivered to connection pool event hooks, such as
[PoolEvents.connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.connect) and [PoolEvents.checkout()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.checkout).

Added in version 2.0: [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry) provides the public
facing interface for the [_ConnectionRecord](#sqlalchemy.pool._ConnectionRecord) internal class.

| Member Name | Description |
| --- | --- |
| close() | Close the DBAPI connection managed by this connection pool entry. |
| dbapi_connection | A reference to the actual DBAPI connection being tracked. |
| driver_connection | The “driver level” connection object as used by the Python
DBAPI or database driver. |
| info | Info dictionary associated with the underlying DBAPI connection
referred to by thisManagesConnectioninstance, allowing
user-defined data to be associated with the connection. |
| invalidate() | Mark the managed connection as invalidated. |
| record_info | Persistent info dictionary associated with thisManagesConnection. |

   method [sqlalchemy.pool.ConnectionPoolEntry.](#sqlalchemy.pool.ConnectionPoolEntry)close() → None

Close the DBAPI connection managed by this connection pool entry.

    attribute [sqlalchemy.pool.ConnectionPoolEntry.](#sqlalchemy.pool.ConnectionPoolEntry)dbapi_connection

A reference to the actual DBAPI connection being tracked.

This is a [PEP 249](https://peps.python.org/pep-0249/)-compliant object that for traditional sync-style
dialects is provided by the third-party
DBAPI implementation in use.  For asyncio dialects, the implementation
is typically an adapter object provided by the SQLAlchemy dialect
itself; the underlying asyncio object is available via the
[ManagesConnection.driver_connection](#sqlalchemy.pool.ManagesConnection.driver_connection) attribute.

SQLAlchemy’s interface for the DBAPI connection is based on the
[DBAPIConnection](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPIConnection) protocol object

See also

[ManagesConnection.driver_connection](#sqlalchemy.pool.ManagesConnection.driver_connection)

[How do I get at the raw DBAPI connection when using an Engine?](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-dbapi-connection)

     attribute [sqlalchemy.pool.ConnectionPoolEntry.](#sqlalchemy.pool.ConnectionPoolEntry)driver_connection

The “driver level” connection object as used by the Python
DBAPI or database driver.

For traditional [PEP 249](https://peps.python.org/pep-0249/) DBAPI implementations, this object will
be the same object as that of
[ManagesConnection.dbapi_connection](#sqlalchemy.pool.ManagesConnection.dbapi_connection).   For an asyncio database
driver, this will be the ultimate “connection” object used by that
driver, such as the `asyncpg.Connection` object which will not have
standard pep-249 methods.

Added in version 1.4.24.

See also

[ManagesConnection.dbapi_connection](#sqlalchemy.pool.ManagesConnection.dbapi_connection)

[How do I get at the raw DBAPI connection when using an Engine?](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-dbapi-connection)

     property in_use: bool

Return True the connection is currently checked out

    attribute [sqlalchemy.pool.ConnectionPoolEntry.](#sqlalchemy.pool.ConnectionPoolEntry)info

*inherited from the* `ManagesConnection.info` *attribute of* [ManagesConnection](#sqlalchemy.pool.ManagesConnection)

Info dictionary associated with the underlying DBAPI connection
referred to by this [ManagesConnection](#sqlalchemy.pool.ManagesConnection) instance, allowing
user-defined data to be associated with the connection.

The data in this dictionary is persistent for the lifespan
of the DBAPI connection itself, including across pool checkins
and checkouts.  When the connection is invalidated
and replaced with a new one, this dictionary is cleared.

For a [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) instance that’s not associated
with a [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry), such as if it were detached, the
attribute returns a dictionary that is local to that
[ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry). Therefore the
[ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info) attribute will always provide a Python
dictionary.

See also

[ManagesConnection.record_info](#sqlalchemy.pool.ManagesConnection.record_info)

     method [sqlalchemy.pool.ConnectionPoolEntry.](#sqlalchemy.pool.ConnectionPoolEntry)invalidate(*e:BaseException|None=None*, *soft:bool=False*) → None

*inherited from the* `ManagesConnection.invalidate()` *method of* [ManagesConnection](#sqlalchemy.pool.ManagesConnection)

Mark the managed connection as invalidated.

  Parameters:

- **e** – an exception object indicating a reason for the invalidation.
- **soft** – if True, the connection isn’t closed; instead, this
  connection will be recycled on next checkout.

See also

[More on Invalidation](#pool-connection-invalidation)

     attribute [sqlalchemy.pool.ConnectionPoolEntry.](#sqlalchemy.pool.ConnectionPoolEntry)record_info

*inherited from the* `ManagesConnection.record_info` *attribute of* [ManagesConnection](#sqlalchemy.pool.ManagesConnection)

Persistent info dictionary associated with this
[ManagesConnection](#sqlalchemy.pool.ManagesConnection).

Unlike the [ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info) dictionary, the lifespan
of this dictionary is that of the [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry)
which owns it; therefore this dictionary will persist across
reconnects and connection invalidation for a particular entry
in the connection pool.

For a [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) instance that’s not associated
with a [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry), such as if it were detached, the
attribute returns None. Contrast to the [ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info)
dictionary which is never None.

See also

[ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info)

      class sqlalchemy.pool.PoolProxiedConnection

*inherits from* [sqlalchemy.pool.base.ManagesConnection](#sqlalchemy.pool.ManagesConnection)

A connection-like adapter for a [PEP 249](https://peps.python.org/pep-0249/) DBAPI connection, which
includes additional methods specific to the [Pool](#sqlalchemy.pool.Pool) implementation.

[PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) is the public-facing interface for the
internal [_ConnectionFairy](#sqlalchemy.pool._ConnectionFairy) implementation object; users familiar
with [_ConnectionFairy](#sqlalchemy.pool._ConnectionFairy) can consider this object to be equivalent.

Added in version 2.0: [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) provides the public-
facing interface for the [_ConnectionFairy](#sqlalchemy.pool._ConnectionFairy) internal class.

| Member Name | Description |
| --- | --- |
| close() | Release this connection back to the pool. |
| dbapi_connection | A reference to the actual DBAPI connection being tracked. |
| detach() | Separate this connection from its Pool. |
| driver_connection | The “driver level” connection object as used by the Python
DBAPI or database driver. |
| info | Info dictionary associated with the underlying DBAPI connection
referred to by thisManagesConnectioninstance, allowing
user-defined data to be associated with the connection. |
| invalidate() | Mark the managed connection as invalidated. |
| record_info | Persistent info dictionary associated with thisManagesConnection. |

   method [sqlalchemy.pool.PoolProxiedConnection.](#sqlalchemy.pool.PoolProxiedConnection)close() → None

Release this connection back to the pool.

The [PoolProxiedConnection.close()](#sqlalchemy.pool.PoolProxiedConnection.close) method shadows the
[PEP 249](https://peps.python.org/pep-0249/) `.close()` method, altering its behavior to instead
[release](https://docs.sqlalchemy.org/en/20/glossary.html#term-release) the proxied connection back to the connection pool.

Upon release to the pool, whether the connection stays “opened” and
pooled in the Python process, versus actually closed out and removed
from the Python process, is based on the pool implementation in use and
its configuration and current state.

    attribute [sqlalchemy.pool.PoolProxiedConnection.](#sqlalchemy.pool.PoolProxiedConnection)dbapi_connection

A reference to the actual DBAPI connection being tracked.

This is a [PEP 249](https://peps.python.org/pep-0249/)-compliant object that for traditional sync-style
dialects is provided by the third-party
DBAPI implementation in use.  For asyncio dialects, the implementation
is typically an adapter object provided by the SQLAlchemy dialect
itself; the underlying asyncio object is available via the
[ManagesConnection.driver_connection](#sqlalchemy.pool.ManagesConnection.driver_connection) attribute.

SQLAlchemy’s interface for the DBAPI connection is based on the
[DBAPIConnection](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPIConnection) protocol object

See also

[ManagesConnection.driver_connection](#sqlalchemy.pool.ManagesConnection.driver_connection)

[How do I get at the raw DBAPI connection when using an Engine?](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-dbapi-connection)

     method [sqlalchemy.pool.PoolProxiedConnection.](#sqlalchemy.pool.PoolProxiedConnection)detach() → None

Separate this connection from its Pool.

This means that the connection will no longer be returned to the
pool when closed, and will instead be literally closed.  The
associated [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry) is de-associated from this
DBAPI connection.

Note that any overall connection limiting constraints imposed by a
Pool implementation may be violated after a detach, as the detached
connection is removed from the pool’s knowledge and control.

    attribute [sqlalchemy.pool.PoolProxiedConnection.](#sqlalchemy.pool.PoolProxiedConnection)driver_connection

The “driver level” connection object as used by the Python
DBAPI or database driver.

For traditional [PEP 249](https://peps.python.org/pep-0249/) DBAPI implementations, this object will
be the same object as that of
[ManagesConnection.dbapi_connection](#sqlalchemy.pool.ManagesConnection.dbapi_connection).   For an asyncio database
driver, this will be the ultimate “connection” object used by that
driver, such as the `asyncpg.Connection` object which will not have
standard pep-249 methods.

Added in version 1.4.24.

See also

[ManagesConnection.dbapi_connection](#sqlalchemy.pool.ManagesConnection.dbapi_connection)

[How do I get at the raw DBAPI connection when using an Engine?](https://docs.sqlalchemy.org/en/20/faq/connections.html#faq-dbapi-connection)

     attribute [sqlalchemy.pool.PoolProxiedConnection.](#sqlalchemy.pool.PoolProxiedConnection)info

*inherited from the* `ManagesConnection.info` *attribute of* [ManagesConnection](#sqlalchemy.pool.ManagesConnection)

Info dictionary associated with the underlying DBAPI connection
referred to by this [ManagesConnection](#sqlalchemy.pool.ManagesConnection) instance, allowing
user-defined data to be associated with the connection.

The data in this dictionary is persistent for the lifespan
of the DBAPI connection itself, including across pool checkins
and checkouts.  When the connection is invalidated
and replaced with a new one, this dictionary is cleared.

For a [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) instance that’s not associated
with a [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry), such as if it were detached, the
attribute returns a dictionary that is local to that
[ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry). Therefore the
[ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info) attribute will always provide a Python
dictionary.

See also

[ManagesConnection.record_info](#sqlalchemy.pool.ManagesConnection.record_info)

     method [sqlalchemy.pool.PoolProxiedConnection.](#sqlalchemy.pool.PoolProxiedConnection)invalidate(*e:BaseException|None=None*, *soft:bool=False*) → None

*inherited from the* `ManagesConnection.invalidate()` *method of* [ManagesConnection](#sqlalchemy.pool.ManagesConnection)

Mark the managed connection as invalidated.

  Parameters:

- **e** – an exception object indicating a reason for the invalidation.
- **soft** – if True, the connection isn’t closed; instead, this
  connection will be recycled on next checkout.

See also

[More on Invalidation](#pool-connection-invalidation)

     property is_detached: bool

Return True if this [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) is detached
from its pool.

    property is_valid: bool

Return True if this [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) still refers
to an active DBAPI connection.

    attribute [sqlalchemy.pool.PoolProxiedConnection.](#sqlalchemy.pool.PoolProxiedConnection)record_info

*inherited from the* `ManagesConnection.record_info` *attribute of* [ManagesConnection](#sqlalchemy.pool.ManagesConnection)

Persistent info dictionary associated with this
[ManagesConnection](#sqlalchemy.pool.ManagesConnection).

Unlike the [ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info) dictionary, the lifespan
of this dictionary is that of the [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry)
which owns it; therefore this dictionary will persist across
reconnects and connection invalidation for a particular entry
in the connection pool.

For a [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) instance that’s not associated
with a [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry), such as if it were detached, the
attribute returns None. Contrast to the [ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info)
dictionary which is never None.

See also

[ManagesConnection.info](#sqlalchemy.pool.ManagesConnection.info)

      class sqlalchemy.pool._ConnectionFairy

*inherits from* [sqlalchemy.pool.base.PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection)

Proxies a DBAPI connection and provides return-on-dereference
support.

This is an internal object used by the [Pool](#sqlalchemy.pool.Pool) implementation
to provide context management to a DBAPI connection delivered by
that [Pool](#sqlalchemy.pool.Pool).   The public facing interface for this class
is described by the [PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection) class.  See that
class for public API details.

The name “fairy” is inspired by the fact that the
[_ConnectionFairy](#sqlalchemy.pool._ConnectionFairy) object’s lifespan is transitory, as it lasts
only for the length of a specific DBAPI connection being checked out from
the pool, and additionally that as a transparent proxy, it is mostly
invisible.

See also

[PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection)

[ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry)

     class sqlalchemy.pool._ConnectionRecord

*inherits from* [sqlalchemy.pool.base.ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry)

Maintains a position in a connection pool which references a pooled
connection.

This is an internal object used by the [Pool](#sqlalchemy.pool.Pool) implementation
to provide context management to a DBAPI connection maintained by
that [Pool](#sqlalchemy.pool.Pool).   The public facing interface for this class
is described by the [ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry) class.  See that
class for public API details.

See also

[ConnectionPoolEntry](#sqlalchemy.pool.ConnectionPoolEntry)

[PoolProxiedConnection](#sqlalchemy.pool.PoolProxiedConnection)
