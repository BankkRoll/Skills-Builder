# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Connections / Engines

## How do I configure logging?

See [Configuring Logging](https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging).

## How do I pool database connections?   Are my connections pooled?

SQLAlchemy performs application-level connection pooling automatically
in most cases.  For all included dialects (except SQLite when using a
“memory” database), a [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object refers to a
[QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) as a source of connectivity.

For more detail, see [Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html) and [Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html).

## How do I pass custom connect arguments to my database API?

The [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) call accepts additional arguments either
directly via the `connect_args` keyword argument:

```
e = create_engine(
    "mysql+mysqldb://scott:tiger@localhost/test", connect_args={"encoding": "utf8"}
)
```

Or for basic string and integer arguments, they can usually be specified
in the query string of the URL:

```
e = create_engine("mysql+mysqldb://scott:tiger@localhost/test?encoding=utf8")
```

See also

[Custom DBAPI connect() arguments / on-connect routines](https://docs.sqlalchemy.org/en/20/core/engines.html#custom-dbapi-args)

## “MySQL Server has gone away”

The primary cause of this error is that the MySQL connection has timed out
and has been closed by the server.   The MySQL server closes connections
which have been idle a period of time which defaults to eight hours.
To accommodate this, the immediate setting is to enable the
[create_engine.pool_recycle](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_recycle) setting, which will ensure that a
connection which is older than a set amount of seconds will be discarded
and replaced with a new connection when it is next checked out.

For the more general case of accommodating database restarts and other
temporary loss of connectivity due to network issues, connections that
are in the pool may be recycled in response to more generalized disconnect
detection techniques.  The section [Dealing with Disconnects](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects) provides
background on both “pessimistic” (e.g. pre-ping) and “optimistic”
(e.g. graceful recovery) techniques.   Modern SQLAlchemy tends to favor
the “pessimistic” approach.

See also

[Dealing with Disconnects](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects)

## “Commands out of sync; you can’t run this command now” / “This result object does not return rows. It has been closed automatically”

The MySQL drivers have a fairly wide class of failure modes whereby the state of
the connection to the server is in an invalid state.  Typically, when the connection
is used again, one of these two error messages will occur.    The reason is because
the state of the server has been changed to one in which the client library
does not expect, such that when the client library emits a new statement
on the connection, the server does not respond as expected.

In SQLAlchemy, because database connections are pooled, the issue of the messaging
being out of sync on a connection becomes more important, since when an operation
fails, if the connection itself is in an unusable state, if it goes back into the
connection pool, it will malfunction when checked out again.  The mitigation
for this issue is that the connection is **invalidated** when such a failure
mode occurs so that the underlying database connection to MySQL is discarded.
This invalidation occurs automatically for many known failure modes and can
also be called explicitly via the [Connection.invalidate()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.invalidate) method.

There is also a second class of failure modes within this category where a context manager
such as `with session.begin_nested():` wants to “roll back” the transaction
when an error occurs; however within some failure modes of the connection, the
rollback itself (which can also be a RELEASE SAVEPOINT operation) also
fails, causing misleading stack traces.

Originally, the cause of this error used to be fairly simple, it meant that
a multithreaded program was invoking commands on a single connection from more
than one thread.   This applied to the original “MySQLdb” native-C driver that was
pretty much the only driver in use.   However, with the introduction of pure Python
drivers like PyMySQL and MySQL-connector-Python, as well as increased use of
tools such as gevent/eventlet, multiprocessing (often with Celery), and others,
there is a whole series of factors that has been known to cause this problem, some of
which have been improved across SQLAlchemy versions but others which are unavoidable:

- **Sharing a connection among threads** - This is the original reason these kinds
  of errors occurred.  A program used the same connection in two or more threads at
  the same time, meaning multiple sets of messages got mixed up on the connection,
  putting the server-side session into a state that the client no longer knows how
  to interpret.   However, other causes are usually more likely today.
- **Sharing the filehandle for the connection among processes** - This usually occurs
  when a program uses `os.fork()` to spawn a new process, and a TCP connection
  that is present in th parent process gets shared into one or more child processes.
  As multiple processes are now emitting messages to essentially the same filehandle,
  the server receives interleaved messages and breaks the state of the connection.
  This scenario can occur very easily if a program uses Python’s “multiprocessing”
  module and makes use of an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) that was created in the parent
  process.  It’s common that “multiprocessing” is in use when using tools like
  Celery.  The correct approach should be either that a new [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
  is produced when a child process first starts, discarding any [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
  that came down from the parent process; or, the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) that’s inherited
  from the parent process can have it’s internal pool of connections disposed by
  calling [Engine.dispose()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose).
- **Greenlet Monkeypatching w/ Exits** - When using a library like gevent or eventlet
  that monkeypatches the Python networking API, libraries like PyMySQL are now
  working in an asynchronous mode of operation, even though they are not developed
  explicitly against this model.  A common issue is that a greenthread is interrupted,
  often due to timeout logic in the application.  This results in the `GreenletExit`
  exception being raised, and the pure-Python MySQL driver is interrupted from
  its work, which may have been that it was receiving a response from the server
  or preparing to otherwise reset the state of the connection.   When the exception
  cuts all that work short, the conversation between client and server is now
  out of sync and subsequent usage of the connection may fail.   SQLAlchemy
  as of version 1.1.0 knows how to guard against this, as if a database operation
  is interrupted by a so-called “exit exception”, which includes `GreenletExit`
  and any other subclass of Python `BaseException` that is not also a subclass
  of `Exception`, the connection is invalidated.
- **Rollbacks / SAVEPOINT releases failing** - Some classes of error cause
  the connection to be unusable within the context of a transaction, as well
  as when operating in a “SAVEPOINT” block.  In these cases, the failure
  on the connection has rendered any SAVEPOINT as no longer existing, yet
  when SQLAlchemy, or the application, attempts to “roll back” this savepoint,
  the “RELEASE SAVEPOINT” operation fails, typically with a message like
  “savepoint does not exist”.   In this case, under Python 3 there will be
  a chain of exceptions output, where the ultimate “cause” of the error
  will be displayed as well.  Under Python 2, there are no “chained” exceptions,
  however recent versions of SQLAlchemy will attempt to emit a warning
  illustrating the original failure cause, while still throwing the
  immediate error which is the failure of the ROLLBACK.

## How Do I “Retry” a Statement Execution Automatically?

The documentation section [Dealing with Disconnects](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects) discusses the strategies
available for pooled connections that have been disconnected since the last
time a particular connection was checked out.   The most modern feature
in this regard is the [create_engine.pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pre_ping) parameter, which
allows that a “ping” is emitted on a database connection when it’s retrieved
from the pool, reconnecting if the current connection has been disconnected.

It’s important to note that this “ping” is only emitted **before** the
connection is actually used for an operation.   Once the connection is
delivered to the caller, per the Python [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) specification it is now
subject to an **autobegin** operation, which means it will automatically BEGIN
a new transaction when it is first used that remains in effect for subsequent
statements, until the DBAPI-level `connection.commit()` or
`connection.rollback()` method is invoked.

In modern use of SQLAlchemy, a series of SQL statements are always invoked
within this transactional state, assuming
[DBAPI autocommit mode](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit) is not enabled (more on that in
the next section), meaning that no single statement is automatically committed;
if an operation fails, the effects of all statements within the current
transaction will be lost.

The implication that this has for the notion of “retrying” a statement is that
in the default case, when a connection is lost, **the entire transaction is
lost**. There is no useful way that the database can “reconnect and retry” and
continue where it left off, since data is already lost.   For this reason,
SQLAlchemy does not have a transparent “reconnection” feature that works
mid-transaction, for the case when the database connection has disconnected
while being used. The canonical approach to dealing with mid-operation
disconnects is to **retry the entire operation from the start of the
transaction**, often by using a custom Python decorator that will
“retry” a particular function several times until it succeeds, or to otherwise
architect the application in such a way that it is resilient against
transactions that are dropped that then cause operations to fail.

There is also the notion of extensions that can keep track of all of the
statements that have proceeded within a transaction and then replay them all in
a new transaction in order to approximate a “retry” operation.  SQLAlchemy’s
[event system](https://docs.sqlalchemy.org/en/20/core/events.html) does allow such a system to be
constructed, however this approach is also not generally useful as there is
no way to guarantee that those
[DML](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML) statements will be working against the same state, as once a
transaction has ended the state of the database in a new transaction may be
totally different.   Architecting “retry” explicitly into the application
at the points at which transactional operations begin and commit remains
the better approach since the application-level transactional methods are
the ones that know best how to re-run their steps.

Otherwise, if SQLAlchemy were to provide a feature that transparently and
silently “reconnected” a connection mid-transaction, the effect would be that
data is silently lost.   By trying to hide the problem, SQLAlchemy would make
the situation much worse.

However, if we are **not** using transactions, then there are more options
available, as the next section describes.

### Using DBAPI Autocommit Allows for a Readonly Version of Transparent Reconnect

With the rationale for not having a transparent reconnection mechanism stated,
the preceding section rests upon the assumption that the application is in
fact using DBAPI-level transactions.  As most DBAPIs now offer [native
“autocommit” settings](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit), we can make use of these features to
provide a limited form of transparent reconnect for **read only,
autocommit only operations**.  A transparent statement retry may be applied to
the `cursor.execute()` method of the DBAPI, however it is still not safe to
apply to the `cursor.executemany()` method of the DBAPI, as the statement may
have consumed any portion of the arguments given.

Warning

The following recipe should **not** be used for operations that
write data.   Users should carefully read and understand how the recipe
works and test failure modes very carefully against the specifically
targeted DBAPI driver before making production use of this recipe.
The retry mechanism does not guarantee prevention of disconnection errors
in all cases.

A simple retry mechanism may be applied to the DBAPI level `cursor.execute()`
method by making use of the [DialectEvents.do_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.do_execute) and
[DialectEvents.do_execute_no_params()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.do_execute_no_params) hooks, which will be able to
intercept disconnections during statement executions.   It will **not**
intercept connection failures during result set fetch operations, for those
DBAPIs that don’t fully buffer result sets.  The recipe requires that the
database support DBAPI level autocommit and is **not guaranteed** for
particular backends.  A single function `reconnecting_engine()` is presented
which applies the event hooks to a given [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object,
returning an always-autocommit version that enables DBAPI-level autocommit.
A connection will transparently reconnect for single-parameter and no-parameter
statement executions:

```
import time

from sqlalchemy import event

def reconnecting_engine(engine, num_retries, retry_interval):
    def _run_with_retries(fn, context, cursor_obj, statement, *arg, **kw):
        for retry in range(num_retries + 1):
            try:
                fn(cursor_obj, statement, context=context, *arg)
            except engine.dialect.dbapi.Error as raw_dbapi_err:
                connection = context.root_connection
                if engine.dialect.is_disconnect(
                    raw_dbapi_err, connection.connection.dbapi_connection, cursor_obj
                ):
                    engine.logger.error(
                        "disconnection error, attempt %d/%d",
                        retry + 1,
                        num_retries + 1,
                        exc_info=True,
                    )
                    connection.invalidate()

                    # use SQLAlchemy 2.0 API if available
                    if hasattr(connection, "rollback"):
                        connection.rollback()
                    else:
                        trans = connection.get_transaction()
                        if trans:
                            trans.rollback()

                    if retry == num_retries:
                        raise

                    time.sleep(retry_interval)
                    context.cursor = cursor_obj = connection.connection.cursor()
                else:
                    raise
            else:
                return True

    e = engine.execution_options(isolation_level="AUTOCOMMIT")

    @event.listens_for(e, "do_execute_no_params")
    def do_execute_no_params(cursor_obj, statement, context):
        return _run_with_retries(
            context.dialect.do_execute_no_params, context, cursor_obj, statement
        )

    @event.listens_for(e, "do_execute")
    def do_execute(cursor_obj, statement, parameters, context):
        return _run_with_retries(
            context.dialect.do_execute, context, cursor_obj, statement, parameters
        )

    return e
```

Given the above recipe, a reconnection mid-transaction may be demonstrated
using the following proof of concept script.  Once run, it will emit a
`SELECT 1` statement to the database every five seconds:

```
from sqlalchemy import create_engine
from sqlalchemy import select

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://scott:tiger@localhost/test", echo_pool=True)

    def do_a_thing(engine):
        with engine.begin() as conn:
            while True:
                print("ping: %s" % conn.execute(select([1])).scalar())
                time.sleep(5)

    e = reconnecting_engine(
        create_engine("mysql+mysqldb://scott:tiger@localhost/test", echo_pool=True),
        num_retries=5,
        retry_interval=2,
    )

    do_a_thing(e)
```

Restart the database while the script runs to demonstrate the transparent
reconnect operation:

```
$ python reconnect_test.py
ping: 1
ping: 1
disconnection error, retrying operation
Traceback (most recent call last):
  ...
MySQLdb._exceptions.OperationalError: (2006, 'MySQL server has gone away')
2020-10-19 16:16:22,624 INFO sqlalchemy.pool.impl.QueuePool Invalidate connection <_mysql.connection open to 'localhost' at 0xf59240>
ping: 1
ping: 1
...
```

The above recipe is tested for SQLAlchemy 1.4.

## Why does SQLAlchemy issue so many ROLLBACKs?

SQLAlchemy currently assumes DBAPI connections are in “non-autocommit” mode -
this is the default behavior of the Python database API, meaning it
must be assumed that a transaction is always in progress. The
connection pool issues `connection.rollback()` when a connection is returned.
This is so that any transactional resources remaining on the connection are
released. On a database like PostgreSQL or MSSQL where table resources are
aggressively locked, this is critical so that rows and tables don’t remain
locked within connections that are no longer in use. An application can
otherwise hang. It’s not just for locks, however, and is equally critical on
any database that has any kind of transaction isolation, including MySQL with
InnoDB. Any connection that is still inside an old transaction will return
stale data, if that data was already queried on that connection within
isolation. For background on why you might see stale data even on MySQL, see
[https://dev.mysql.com/doc/refman/5.1/en/innodb-transaction-model.html](https://dev.mysql.com/doc/refman/5.1/en/innodb-transaction-model.html)

### I’m on MyISAM - how do I turn it off?

The behavior of the connection pool’s connection return behavior can be
configured using `reset_on_return`:

```
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "mysql+mysqldb://scott:tiger@localhost/myisam_database",
    pool=QueuePool(reset_on_return=False),
)
```

### I’m on SQL Server - how do I turn those ROLLBACKs into COMMITs?

`reset_on_return` accepts the values `commit`, `rollback` in addition
to `True`, `False`, and `None`.   Setting to `commit` will cause
a COMMIT as any connection is returned to the pool:

```
engine = create_engine(
    "mssql+pyodbc://scott:tiger@mydsn", pool=QueuePool(reset_on_return="commit")
)
```

## I am using multiple connections with a SQLite database (typically to test transaction operation), and my test program is not working!

If using a SQLite `:memory:` database the default connection pool is the
[SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool), which maintains exactly one SQLite connection
per thread.  So two connections in use in the same thread will actually be
the same SQLite connection.  Make sure you’re not using a :memory: database
so that the engine will use [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) (the default for non-memory
databases in current SQLAlchemy versions).

See also

[Threading/Pooling Behavior](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#pysqlite-threading-pooling) - info on PySQLite’s behavior.

## How do I get at the raw DBAPI connection when using an Engine?

With a regular SA engine-level Connection, you can get at a pool-proxied
version of the DBAPI connection via the [Connection.connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.connection) attribute on
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), and for the really-real DBAPI connection you can call the
[PoolProxiedConnection.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.dbapi_connection) attribute on that.  On regular sync drivers
there is usually no need to access the non-pool-proxied DBAPI connection,
as all methods are proxied through:

```
engine = create_engine(...)
conn = engine.connect()

# pep-249 style PoolProxiedConnection (historically called a "connection fairy")
connection_fairy = conn.connection

# typically to run statements one would get a cursor() from this
# object
cursor_obj = connection_fairy.cursor()
# ... work with cursor_obj

# to bypass "connection_fairy", such as to set attributes on the
# unproxied pep-249 DBAPI connection, use .dbapi_connection
raw_dbapi_connection = connection_fairy.dbapi_connection

# the same thing is available as .driver_connection (more on this
# in the next section)
also_raw_dbapi_connection = connection_fairy.driver_connection
```

Changed in version 1.4.24: Added the
[PoolProxiedConnection.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.dbapi_connection) attribute,
which supersedes the previous
`PoolProxiedConnection.connection` attribute which still remains
available; this attribute always provides a pep-249 synchronous style
connection object.  The [PoolProxiedConnection.driver_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.driver_connection)
attribute is also added which will always refer to the real driver-level
connection regardless of what API it presents.

### Accessing the underlying connection for an asyncio driver

When an asyncio driver is in use, there are two changes to the above
scheme.  The first is that when using an [AsyncConnection](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection),
the [PoolProxiedConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection) must be accessed using the awaitable method
[AsyncConnection.get_raw_connection()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection.get_raw_connection).   The
returned [PoolProxiedConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection) in this case retains a sync-style
pep-249 usage pattern, and the [PoolProxiedConnection.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.dbapi_connection)
attribute refers to a
a SQLAlchemy-adapted connection object which adapts the asyncio
connection to a sync style pep-249 API, in other words there are *two* levels
of proxying going on when using an asyncio driver.   The actual asyncio connection
is available from the [driver_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.driver_connection) attribute.
To restate the previous example in terms of asyncio looks like:

```
async def main():
    engine = create_async_engine(...)
    conn = await engine.connect()

    # pep-249 style ConnectionFairy connection pool proxy object
    # presents a sync interface
    connection_fairy = await conn.get_raw_connection()

    # beneath that proxy is a second proxy which adapts the
    # asyncio driver into a pep-249 connection object, accessible
    # via .dbapi_connection as is the same with a sync API
    sqla_sync_conn = connection_fairy.dbapi_connection

    # the really-real innermost driver connection is available
    # from the .driver_connection attribute
    raw_asyncio_connection = connection_fairy.driver_connection

    # work with raw asyncio connection
    result = await raw_asyncio_connection.execute(...)
```

Changed in version 1.4.24: Added the
[PoolProxiedConnection.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.dbapi_connection)
and [PoolProxiedConnection.driver_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.driver_connection) attributes to allow access
to pep-249 connections, pep-249 adaption layers, and underlying driver
connections using a consistent interface.

When using asyncio drivers, the above “DBAPI” connection is actually a
SQLAlchemy-adapted form of connection which presents a synchronous-style
pep-249 style API.  To access the actual
asyncio driver connection, which will present the original asyncio API
of the driver in use, this can be accessed via the
[PoolProxiedConnection.driver_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.driver_connection) attribute of
[PoolProxiedConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection).
For a standard pep-249 driver, [PoolProxiedConnection.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.dbapi_connection)
and [PoolProxiedConnection.driver_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection.driver_connection) are synonymous.

You must ensure that you revert any isolation level settings or other
operation-specific settings on the connection back to normal before returning
it to the pool.

As an alternative to reverting settings, you can call the
[Connection.detach()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.detach) method on either [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
or the proxied connection, which will de-associate the connection from the pool
such that it will be closed and discarded when [Connection.close()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.close)
is called:

```
conn = engine.connect()
conn.detach()  # detaches the DBAPI connection from the connection pool
conn.connection.<go nuts>
conn.close()  # connection is closed for real, the pool replaces it with a new connection
```

## How do I use engines / connections / sessions with Python multiprocessing, or os.fork()?

This is covered in the section [Using Connection Pools with Multiprocessing or os.fork()](https://docs.sqlalchemy.org/en/20/core/pooling.html#pooling-multiprocessing).

---

# SQLAlchemy 2.0 Documentation

# Frequently Asked Questions

The Frequently Asked Questions section is a growing collection of commonly
observed questions to well-known issues.

- [Installation](https://docs.sqlalchemy.org/en/20/faq/installation.html)
  - [I’m getting an error about greenlet not being installed when I try to use asyncio](https://docs.sqlalchemy.org/en/20/faq/installation.html#i-m-getting-an-error-about-greenlet-not-being-installed-when-i-try-to-use-asyncio)
- [Connections / Engines](https://docs.sqlalchemy.org/en/20/faq/connections.html)
  - [How do I configure logging?](https://docs.sqlalchemy.org/en/20/faq/connections.html#how-do-i-configure-logging)
  - [How do I pool database connections?   Are my connections pooled?](https://docs.sqlalchemy.org/en/20/faq/connections.html#how-do-i-pool-database-connections-are-my-connections-pooled)
  - [How do I pass custom connect arguments to my database API?](https://docs.sqlalchemy.org/en/20/faq/connections.html#how-do-i-pass-custom-connect-arguments-to-my-database-api)
  - [“MySQL Server has gone away”](https://docs.sqlalchemy.org/en/20/faq/connections.html#mysql-server-has-gone-away)
  - [“Commands out of sync; you can’t run this command now” / “This result object does not return rows. It has been closed automatically”](https://docs.sqlalchemy.org/en/20/faq/connections.html#commands-out-of-sync-you-can-t-run-this-command-now-this-result-object-does-not-return-rows-it-has-been-closed-automatically)
  - [How Do I “Retry” a Statement Execution Automatically?](https://docs.sqlalchemy.org/en/20/faq/connections.html#how-do-i-retry-a-statement-execution-automatically)
  - [Why does SQLAlchemy issue so many ROLLBACKs?](https://docs.sqlalchemy.org/en/20/faq/connections.html#why-does-sqlalchemy-issue-so-many-rollbacks)
  - [I am using multiple connections with a SQLite database (typically to test transaction operation), and my test program is not working!](https://docs.sqlalchemy.org/en/20/faq/connections.html#i-am-using-multiple-connections-with-a-sqlite-database-typically-to-test-transaction-operation-and-my-test-program-is-not-working)
  - [How do I get at the raw DBAPI connection when using an Engine?](https://docs.sqlalchemy.org/en/20/faq/connections.html#how-do-i-get-at-the-raw-dbapi-connection-when-using-an-engine)
  - [How do I use engines / connections / sessions with Python multiprocessing, or os.fork()?](https://docs.sqlalchemy.org/en/20/faq/connections.html#how-do-i-use-engines-connections-sessions-with-python-multiprocessing-or-os-fork)
- [MetaData / Schema](https://docs.sqlalchemy.org/en/20/faq/metadata_schema.html)
  - [My program is hanging when I saytable.drop()/metadata.drop_all()](https://docs.sqlalchemy.org/en/20/faq/metadata_schema.html#my-program-is-hanging-when-i-say-table-drop-metadata-drop-all)
  - [Does SQLAlchemy support ALTER TABLE, CREATE VIEW, CREATE TRIGGER, Schema Upgrade Functionality?](https://docs.sqlalchemy.org/en/20/faq/metadata_schema.html#does-sqlalchemy-support-alter-table-create-view-create-trigger-schema-upgrade-functionality)
  - [How can I sort Table objects in order of their dependency?](https://docs.sqlalchemy.org/en/20/faq/metadata_schema.html#how-can-i-sort-table-objects-in-order-of-their-dependency)
  - [How can I get the CREATE TABLE/ DROP TABLE output as a string?](https://docs.sqlalchemy.org/en/20/faq/metadata_schema.html#how-can-i-get-the-create-table-drop-table-output-as-a-string)
  - [How can I subclass Table/Column to provide certain behaviors/configurations?](https://docs.sqlalchemy.org/en/20/faq/metadata_schema.html#how-can-i-subclass-table-column-to-provide-certain-behaviors-configurations)
- [SQL Expressions](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html)
  - [How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#how-do-i-render-sql-expressions-as-strings-possibly-with-bound-parameters-inlined)
  - [Why are percent signs being doubled up when stringifying SQL statements?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#why-are-percent-signs-being-doubled-up-when-stringifying-sql-statements)
  - [I’m using op() to generate a custom operator and my parenthesis are not coming out correctly](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#i-m-using-op-to-generate-a-custom-operator-and-my-parenthesis-are-not-coming-out-correctly)
- [ORM Configuration](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html)
  - [How do I map a table that has no primary key?](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#how-do-i-map-a-table-that-has-no-primary-key)
  - [How do I configure a Column that is a Python reserved word or similar?](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#how-do-i-configure-a-column-that-is-a-python-reserved-word-or-similar)
  - [How do I get a list of all columns, relationships, mapped attributes, etc. given a mapped class?](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#how-do-i-get-a-list-of-all-columns-relationships-mapped-attributes-etc-given-a-mapped-class)
  - [I’m getting a warning or error about “Implicitly combining column X under attribute Y”](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#i-m-getting-a-warning-or-error-about-implicitly-combining-column-x-under-attribute-y)
  - [I’m using Declarative and setting primaryjoin/secondaryjoin using anand_()oror_(), and I am getting an error message about foreign keys.](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#i-m-using-declarative-and-setting-primaryjoin-secondaryjoin-using-an-and-or-or-and-i-am-getting-an-error-message-about-foreign-keys)
  - [Why isORDERBYrecommended withLIMIT(especially withsubqueryload())?](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#why-is-order-by-recommended-with-limit-especially-with-subqueryload)
  - [What aredefault,default_factoryandinsert_defaultand what should I use?](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#what-are-default-default-factory-and-insert-default-and-what-should-i-use)
- [Performance](https://docs.sqlalchemy.org/en/20/faq/performance.html)
  - [Why is my application slow after upgrading to 1.4 and/or 2.x?](https://docs.sqlalchemy.org/en/20/faq/performance.html#why-is-my-application-slow-after-upgrading-to-1-4-and-or-2-x)
  - [How can I profile a SQLAlchemy powered application?](https://docs.sqlalchemy.org/en/20/faq/performance.html#how-can-i-profile-a-sqlalchemy-powered-application)
  - [I’m inserting 400,000 rows with the ORM and it’s really slow!](https://docs.sqlalchemy.org/en/20/faq/performance.html#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow)
- [Sessions / Queries](https://docs.sqlalchemy.org/en/20/faq/sessions.html)
  - [I’m re-loading data with my Session but it isn’t seeing changes that I committed elsewhere](https://docs.sqlalchemy.org/en/20/faq/sessions.html#i-m-re-loading-data-with-my-session-but-it-isn-t-seeing-changes-that-i-committed-elsewhere)
  - [“This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar)](https://docs.sqlalchemy.org/en/20/faq/sessions.html#this-session-s-transaction-has-been-rolled-back-due-to-a-previous-exception-during-flush-or-similar)
  - [How do I make a Query that always adds a certain filter to every query?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#how-do-i-make-a-query-that-always-adds-a-certain-filter-to-every-query)
  - [My Query does not return the same number of objects as query.count() tells me - why?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#my-query-does-not-return-the-same-number-of-objects-as-query-count-tells-me-why)
  - [I’ve created a mapping against an Outer Join, and while the query returns rows, no objects are returned.  Why not?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#i-ve-created-a-mapping-against-an-outer-join-and-while-the-query-returns-rows-no-objects-are-returned-why-not)
  - [I’m usingjoinedload()orlazy=Falseto create a JOIN/OUTER JOIN and SQLAlchemy is not constructing the correct query when I try to add a WHERE, ORDER BY, LIMIT, etc. (which relies upon the (OUTER) JOIN)](https://docs.sqlalchemy.org/en/20/faq/sessions.html#i-m-using-joinedload-or-lazy-false-to-create-a-join-outer-join-and-sqlalchemy-is-not-constructing-the-correct-query-when-i-try-to-add-a-where-order-by-limit-etc-which-relies-upon-the-outer-join)
  - [Query has no__len__(), why not?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#query-has-no-len-why-not)
  - [How Do I use Textual SQL with ORM Queries?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#how-do-i-use-textual-sql-with-orm-queries)
  - [I’m callingSession.delete(myobject)and it isn’t removed from the parent collection!](https://docs.sqlalchemy.org/en/20/faq/sessions.html#i-m-calling-session-delete-myobject-and-it-isn-t-removed-from-the-parent-collection)
  - [why isn’t my__init__()called when I load objects?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#why-isn-t-my-init-called-when-i-load-objects)
  - [how do I use ON DELETE CASCADE with SA’s ORM?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#how-do-i-use-on-delete-cascade-with-sa-s-orm)
  - [I set the “foo_id” attribute on my instance to “7”, but the “foo” attribute is stillNone- shouldn’t it have loaded Foo with id #7?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#i-set-the-foo-id-attribute-on-my-instance-to-7-but-the-foo-attribute-is-still-none-shouldn-t-it-have-loaded-foo-with-id-7)
  - [How do I walk all objects that are related to a given object?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#how-do-i-walk-all-objects-that-are-related-to-a-given-object)
  - [Is there a way to automagically have only unique keywords (or other kinds of objects) without doing a query for the keyword and getting a reference to the row containing that keyword?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#is-there-a-way-to-automagically-have-only-unique-keywords-or-other-kinds-of-objects-without-doing-a-query-for-the-keyword-and-getting-a-reference-to-the-row-containing-that-keyword)
  - [Why does post_update emit UPDATE in addition to the first UPDATE?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#why-does-post-update-emit-update-in-addition-to-the-first-update)
- [Third Party Integration Issues](https://docs.sqlalchemy.org/en/20/faq/thirdparty.html)
  - [I’m getting errors related to “numpy.int64”, “numpy.bool_”, etc.](https://docs.sqlalchemy.org/en/20/faq/thirdparty.html#i-m-getting-errors-related-to-numpy-int64-numpy-bool-etc)
  - [SQL expression for WHERE/HAVING role expected, got True](https://docs.sqlalchemy.org/en/20/faq/thirdparty.html#sql-expression-for-where-having-role-expected-got-true)

---

# SQLAlchemy 2.0 Documentation

# Installation

## I’m getting an error about greenlet not being installed when I try to use asyncio

The `greenlet` dependency does not install by default for CPU architectures
for which `greenlet` does not supply a [pre-built binary wheel](https://pypi.org/project/greenlet/#files).
To install including `greenlet`,
add the `asyncio` [setuptools extra](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-setuptools-extras)
to the `pip install` command:

```
pip install sqlalchemy[asyncio]
```

For more background, see [Asyncio Platform Installation Notes (Including Apple M1)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-install).

See also

[Asyncio Platform Installation Notes (Including Apple M1)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-install)

---

# SQLAlchemy 2.0 Documentation

# MetaData / Schema

## My program is hanging when I saytable.drop()/metadata.drop_all()

This usually corresponds to two conditions: 1. using PostgreSQL, which is really
strict about table locks, and 2. you have a connection still open which
contains locks on the table and is distinct from the connection being used for
the DROP statement.  Heres the most minimal version of the pattern:

```
connection = engine.connect()
result = connection.execute(mytable.select())

mytable.drop(engine)
```

Above, a connection pool connection is still checked out; furthermore, the
result object above also maintains a link to this connection.  If
“implicit execution” is used, the result will hold this connection opened until
the result object is closed or all rows are exhausted.

The call to `mytable.drop(engine)` attempts to emit DROP TABLE on a second
connection procured from the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which will lock.

The solution is to close out all connections before emitting DROP TABLE:

```
connection = engine.connect()
result = connection.execute(mytable.select())

# fully read result sets
result.fetchall()

# close connections
connection.close()

# now locks are removed
mytable.drop(engine)
```

## Does SQLAlchemy support ALTER TABLE, CREATE VIEW, CREATE TRIGGER, Schema Upgrade Functionality?

General ALTER support isn’t present in SQLAlchemy directly.  For special DDL
on an ad-hoc basis, the [DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DDL) and related constructs can be used.
See [Customizing DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html) for a discussion on this subject.

A more comprehensive option is to use schema migration tools, such as Alembic
or SQLAlchemy-Migrate; see [Altering Database Objects through Migrations](https://docs.sqlalchemy.org/en/20/core/metadata.html#schema-migrations) for discussion on this.

## How can I sort Table objects in order of their dependency?

This is available via the [MetaData.sorted_tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.sorted_tables) function:

```
metadata_obj = MetaData()
# ... add Table objects to metadata
ti = metadata_obj.sorted_tables
for t in ti:
    print(t)
```

## How can I get the CREATE TABLE/ DROP TABLE output as a string?

Modern SQLAlchemy has clause constructs which represent DDL operations. These
can be rendered to strings like any other SQL expression:

```
from sqlalchemy.schema import CreateTable

print(CreateTable(mytable))
```

To get the string specific to a certain engine:

```
print(CreateTable(mytable).compile(engine))
```

There’s also a special form of [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) available via
[create_mock_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_mock_engine) that allows one to dump an entire
metadata creation sequence as a string, using this recipe:

```
from sqlalchemy import create_mock_engine

def dump(sql, *multiparams, **params):
    print(sql.compile(dialect=engine.dialect))

engine = create_mock_engine("postgresql+psycopg2://", dump)
metadata_obj.create_all(engine, checkfirst=False)
```

The [Alembic](https://alembic.sqlalchemy.org) tool also supports
an “offline” SQL generation mode that renders database migrations as SQL scripts.

## How can I subclass Table/Column to provide certain behaviors/configurations?

[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) are not good targets for direct subclassing.
However, there are simple ways to get on-construction behaviors using creation
functions, and behaviors related to the linkages between schema objects such as
constraint conventions or naming conventions using attachment events.
An example of many of these
techniques can be seen at [Naming Conventions](https://www.sqlalchemy.org/trac/wiki/UsageRecipes/NamingConventions).
