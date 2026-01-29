# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Core Events

This section describes the event interfaces provided in
SQLAlchemy Core.
For an introduction to the event listening API, see [Events](https://docs.sqlalchemy.org/en/20/core/event.html).
ORM events are described in [ORM Events](https://docs.sqlalchemy.org/en/20/orm/events.html).

| Object Name | Description |
| --- | --- |
| Events | Define event listening functions for a particular target type. |

   class sqlalchemy.event.base.Events

*inherits from* `sqlalchemy.event._HasEventsDispatch`

Define event listening functions for a particular target type.

| Member Name | Description |
| --- | --- |
| dispatch | reference back to the _Dispatch class. |

   attribute [sqlalchemy.event.base.Events.](#sqlalchemy.event.base.Events)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.EventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

## Connection Pool Events

| Object Name | Description |
| --- | --- |
| PoolEvents | Available events forPool. |
| PoolResetState | describes the state of a DBAPI connection as it is being passed to
thePoolEvents.reset()connection pool event. |

   class sqlalchemy.events.PoolEvents

*inherits from* `sqlalchemy.event.Events`

Available events for [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool).

The methods here define the name of an event as well
as the names of members that are passed to listener
functions.

When using an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object created via [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
(or indirectly via [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine)), [PoolEvents](#sqlalchemy.events.PoolEvents)
listeners are expected to be registered in terms of the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
which will direct the listeners to the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) contained within:

```
from sqlalchemy import create_engine
from sqlalchemy import event

engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")

@event.listens_for(engine, "checkout")
def my_on_checkout(dbapi_conn, connection_rec, connection_proxy):
    "handle an on checkout event"
```

[PoolEvents](#sqlalchemy.events.PoolEvents) may also be registered with the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
class, with the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) class, as well as with instances of
[Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool).

Tip

Registering [PoolEvents](#sqlalchemy.events.PoolEvents) with the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), if present,
is recommended since the [Engine.dispose()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose) method will carry
along event listeners from the old pool to the new pool.

| Member Name | Description |
| --- | --- |
| checkin() | Called when a connection returns to the pool. |
| checkout() | Called when a connection is retrieved from the Pool. |
| close() | Called when a DBAPI connection is closed. |
| close_detached() | Called when a detached DBAPI connection is closed. |
| connect() | Called at the moment a particular DBAPI connection is first
created for a givenPool. |
| detach() | Called when a DBAPI connection is “detached” from a pool. |
| dispatch | reference back to the _Dispatch class. |
| first_connect() | Called exactly once for the first time a DBAPI connection is
checked out from a particularPool. |
| invalidate() | Called when a DBAPI connection is to be “invalidated”. |
| reset() | Called before the “reset” action occurs for a pooled connection. |
| soft_invalidate() | Called when a DBAPI connection is to be “soft invalidated”. |

   method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)checkin(*dbapi_connection:DBAPIConnection|None*, *connection_record:ConnectionPoolEntry*) → None

Called when a connection returns to the pool.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'checkin')
def receive_checkin(dbapi_connection, connection_record):
    "listen for the 'checkin' event"

    # ... (event handling logic) ...
```

Note that the connection may be closed, and may be None if the
connection has been invalidated.  `checkin` will not be called
for detached connections.  (They do not return to the pool.)

  Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.

      method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)checkout(*dbapi_connection:DBAPIConnection*, *connection_record:ConnectionPoolEntry*, *connection_proxy:PoolProxiedConnection*) → None

Called when a connection is retrieved from the Pool.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'checkout')
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    "listen for the 'checkout' event"

    # ... (event handling logic) ...
```

    Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.
- **connection_proxy** – the [PoolProxiedConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection) object
  which will proxy the public interface of the DBAPI connection for the
  lifespan of the checkout.

If you raise a [DisconnectionError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DisconnectionError), the current
connection will be disposed and a fresh connection retrieved.
Processing of all checkout listeners will abort and restart
using the new connection.

See also

[ConnectionEvents.engine_connect()](#sqlalchemy.events.ConnectionEvents.engine_connect)
- a similar event
which occurs upon creation of a new [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).

     method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)close(*dbapi_connection:DBAPIConnection*, *connection_record:ConnectionPoolEntry*) → None

Called when a DBAPI connection is closed.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'close')
def receive_close(dbapi_connection, connection_record):
    "listen for the 'close' event"

    # ... (event handling logic) ...
```

The event is emitted before the close occurs.

The close of a connection can fail; typically this is because
the connection is already closed.  If the close operation fails,
the connection is discarded.

The [close()](#sqlalchemy.events.PoolEvents.close) event corresponds to a connection that’s still
associated with the pool. To intercept close events for detached
connections use [close_detached()](#sqlalchemy.events.PoolEvents.close_detached).

  Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.

      method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)close_detached(*dbapi_connection:DBAPIConnection*) → None

Called when a detached DBAPI connection is closed.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'close_detached')
def receive_close_detached(dbapi_connection):
    "listen for the 'close_detached' event"

    # ... (event handling logic) ...
```

The event is emitted before the close occurs.

The close of a connection can fail; typically this is because
the connection is already closed.  If the close operation fails,
the connection is discarded.

  Parameters:

**dbapi_connection** – a DBAPI connection.
The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.

      method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)connect(*dbapi_connection:DBAPIConnection*, *connection_record:ConnectionPoolEntry*) → None

Called at the moment a particular DBAPI connection is first
created for a given [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'connect')
def receive_connect(dbapi_connection, connection_record):
    "listen for the 'connect' event"

    # ... (event handling logic) ...
```

This event allows one to capture the point directly after which
the DBAPI module-level `.connect()` method has been used in order
to produce a new DBAPI connection.

  Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.

      method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)detach(*dbapi_connection:DBAPIConnection*, *connection_record:ConnectionPoolEntry*) → None

Called when a DBAPI connection is “detached” from a pool.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'detach')
def receive_detach(dbapi_connection, connection_record):
    "listen for the 'detach' event"

    # ... (event handling logic) ...
```

This event is emitted after the detach occurs.  The connection
is no longer associated with the given connection record.

  Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.

      attribute [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.PoolEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

    method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)first_connect(*dbapi_connection:DBAPIConnection*, *connection_record:ConnectionPoolEntry*) → None

Called exactly once for the first time a DBAPI connection is
checked out from a particular [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'first_connect')
def receive_first_connect(dbapi_connection, connection_record):
    "listen for the 'first_connect' event"

    # ... (event handling logic) ...
```

The rationale for [PoolEvents.first_connect()](#sqlalchemy.events.PoolEvents.first_connect)
is to determine
information about a particular series of database connections based
on the settings used for all connections.  Since a particular
[Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
refers to a single “creator” function (which in terms
of a [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
refers to the URL and connection options used),
it is typically valid to make observations about a single connection
that can be safely assumed to be valid about all subsequent
connections, such as the database version, the server and client
encoding settings, collation settings, and many others.

  Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.

      method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)invalidate(*dbapi_connection:DBAPIConnection*, *connection_record:ConnectionPoolEntry*, *exception:BaseException|None*) → None

Called when a DBAPI connection is to be “invalidated”.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'invalidate')
def receive_invalidate(dbapi_connection, connection_record, exception):
    "listen for the 'invalidate' event"

    # ... (event handling logic) ...
```

This event is called any time the
[ConnectionPoolEntry.invalidate()](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.invalidate) method is invoked, either from
API usage or via “auto-invalidation”, without the `soft` flag.

The event occurs before a final attempt to call `.close()` on the
connection occurs.

  Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.
- **exception** – the exception object corresponding to the reason
  for this invalidation, if any.  May be `None`.

See also

[More on Invalidation](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-connection-invalidation)

     method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)reset(*dbapi_connection:DBAPIConnection*, *connection_record:ConnectionPoolEntry*, *reset_state:PoolResetState*) → None

Called before the “reset” action occurs for a pooled connection.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'reset')
def receive_reset(dbapi_connection, connection_record, reset_state):
    "listen for the 'reset' event"

    # ... (event handling logic) ...

# DEPRECATED calling style (pre-2.0, will be removed in a future release)
@event.listens_for(SomeEngineOrPool, 'reset')
def receive_reset(dbapi_connection, connection_record):
    "listen for the 'reset' event"

    # ... (event handling logic) ...
```

Changed in version 2.0: The [PoolEvents.reset()](#sqlalchemy.events.PoolEvents.reset) event now accepts the
arguments [PoolEvents.reset.dbapi_connection](#sqlalchemy.events.PoolEvents.reset.params.dbapi_connection), [PoolEvents.reset.connection_record](#sqlalchemy.events.PoolEvents.reset.params.connection_record), [PoolEvents.reset.reset_state](#sqlalchemy.events.PoolEvents.reset.params.reset_state).
Support for listener functions which accept the previous
argument signature(s) listed above as “deprecated” will be
removed in a future release.

This event represents
when the `rollback()` method is called on the DBAPI connection
before it is returned to the pool or discarded.
A custom “reset” strategy may be implemented using this event hook,
which may also be combined with disabling the default “reset”
behavior using the [Pool.reset_on_return](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool.params.reset_on_return) parameter.

The primary difference between the [PoolEvents.reset()](#sqlalchemy.events.PoolEvents.reset) and
[PoolEvents.checkin()](#sqlalchemy.events.PoolEvents.checkin) events are that
[PoolEvents.reset()](#sqlalchemy.events.PoolEvents.reset) is called not just for pooled
connections that are being returned to the pool, but also for
connections that were detached using the
[Connection.detach()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.detach) method as well as asyncio connections
that are being discarded due to garbage collection taking place on
connections before the connection was checked in.

Note that the event **is not** invoked for connections that were
invalidated using [Connection.invalidate()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.invalidate).    These
events may be intercepted using the [PoolEvents.soft_invalidate()](#sqlalchemy.events.PoolEvents.soft_invalidate)
and [PoolEvents.invalidate()](#sqlalchemy.events.PoolEvents.invalidate) event hooks, and all “connection
close” events may be intercepted using [PoolEvents.close()](#sqlalchemy.events.PoolEvents.close).

The [PoolEvents.reset()](#sqlalchemy.events.PoolEvents.reset) event is usually followed by the
[PoolEvents.checkin()](#sqlalchemy.events.PoolEvents.checkin) event, except in those
cases where the connection is discarded immediately after reset.

  Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.
- **reset_state** –
  [PoolResetState](#sqlalchemy.events.PoolResetState) instance which provides
  information about the circumstances under which the connection
  is being reset.
  Added in version 2.0.

See also

[Reset On Return](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-reset-on-return)

[ConnectionEvents.rollback()](#sqlalchemy.events.ConnectionEvents.rollback)

[ConnectionEvents.commit()](#sqlalchemy.events.ConnectionEvents.commit)

     method [sqlalchemy.events.PoolEvents.](#sqlalchemy.events.PoolEvents)soft_invalidate(*dbapi_connection:DBAPIConnection*, *connection_record:ConnectionPoolEntry*, *exception:BaseException|None*) → None

Called when a DBAPI connection is to be “soft invalidated”.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngineOrPool, 'soft_invalidate')
def receive_soft_invalidate(dbapi_connection, connection_record, exception):
    "listen for the 'soft_invalidate' event"

    # ... (event handling logic) ...
```

This event is called any time the
[ConnectionPoolEntry.invalidate()](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.invalidate)
method is invoked with the `soft` flag.

Soft invalidation refers to when the connection record that tracks
this connection will force a reconnect after the current connection
is checked in.   It does not actively close the dbapi_connection
at the point at which it is called.

  Parameters:

- **dbapi_connection** – a DBAPI connection.
  The [ConnectionPoolEntry.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry.dbapi_connection) attribute.
- **connection_record** – the [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry) managing
  the DBAPI connection.
- **exception** – the exception object corresponding to the reason
  for this invalidation, if any.  May be `None`.

       class sqlalchemy.events.PoolResetState

describes the state of a DBAPI connection as it is being passed to
the [PoolEvents.reset()](#sqlalchemy.events.PoolEvents.reset) connection pool event.

Added in version 2.0.0b3.

| Member Name | Description |
| --- | --- |
| asyncio_safe | Indicates if the reset operation is occurring within a scope where
an enclosing event loop is expected to be present for asyncio applications. |
| terminate_only | indicates if the connection is to be immediately terminated and
not checked in to the pool. |
| transaction_was_reset | Indicates if the transaction on the DBAPI connection was already
essentially “reset” back by theConnectionobject. |

   attribute [sqlalchemy.events.PoolResetState.](#sqlalchemy.events.PoolResetState)asyncio_safe: bool

Indicates if the reset operation is occurring within a scope where
an enclosing event loop is expected to be present for asyncio applications.

Will be False in the case that the connection is being garbage collected.

    attribute [sqlalchemy.events.PoolResetState.](#sqlalchemy.events.PoolResetState)terminate_only: bool

indicates if the connection is to be immediately terminated and
not checked in to the pool.

This occurs for connections that were invalidated, as well as asyncio
connections that were not cleanly handled by the calling code that
are instead being garbage collected.   In the latter case,
operations can’t be safely run on asyncio connections within garbage
collection as there is not necessarily an event loop present.

    attribute [sqlalchemy.events.PoolResetState.](#sqlalchemy.events.PoolResetState)transaction_was_reset: bool

Indicates if the transaction on the DBAPI connection was already
essentially “reset” back by the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object.

This boolean is True if the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) had transactional
state present upon it, which was then not closed using the
[Connection.rollback()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.rollback) or [Connection.commit()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.commit) method;
instead, the transaction was closed inline within the
[Connection.close()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.close) method so is guaranteed to remain non-present
when this event is reached.

## SQL Execution and Connection Events

| Object Name | Description |
| --- | --- |
| ConnectionEvents | Available events forConnectionandEngine. |
| DialectEvents | event interface for execution-replacement functions. |

   class sqlalchemy.events.ConnectionEvents

*inherits from* `sqlalchemy.event.Events`

Available events for
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).

The methods here define the name of an event as well as the names of
members that are passed to listener functions.

An event listener can be associated with any
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
class or instance, such as an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), e.g.:

```
from sqlalchemy import event, create_engine

def before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    log.info("Received statement: %s", statement)

engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")
event.listen(engine, "before_cursor_execute", before_cursor_execute)
```

or with a specific [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection):

```
with engine.begin() as conn:

    @event.listens_for(conn, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        log.info("Received statement: %s", statement)
```

When the methods are called with a statement parameter, such as in
[after_cursor_execute()](#sqlalchemy.events.ConnectionEvents.after_cursor_execute) or [before_cursor_execute()](#sqlalchemy.events.ConnectionEvents.before_cursor_execute),
the statement is the exact SQL string that was prepared for transmission
to the DBAPI `cursor` in the connection’s [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect).

The [before_execute()](#sqlalchemy.events.ConnectionEvents.before_execute) and [before_cursor_execute()](#sqlalchemy.events.ConnectionEvents.before_cursor_execute)
events can also be established with the `retval=True` flag, which
allows modification of the statement and parameters to be sent
to the database.  The [before_cursor_execute()](#sqlalchemy.events.ConnectionEvents.before_cursor_execute) event is
particularly useful here to add ad-hoc string transformations, such
as comments, to all executions:

```
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "before_cursor_execute", retval=True)
def comment_sql_calls(
    conn, cursor, statement, parameters, context, executemany
):
    statement = statement + " -- some comment"
    return statement, parameters
```

Note

[ConnectionEvents](#sqlalchemy.events.ConnectionEvents) can be established on any
combination of [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection),
as well
as instances of each of those classes.  Events across all
four scopes will fire off for a given instance of
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  However, for performance reasons, the
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object determines at instantiation time
whether or not its parent [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) has event listeners
established.   Event listeners added to the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
class or to an instance of [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) *after* the instantiation
of a dependent [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) instance will usually
*not* be available on that [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) instance.
The newly
added listeners will instead take effect for
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
instances created subsequent to those event listeners being
established on the parent [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) class or instance.

   Parameters:

**retval=False** – Applies to the [before_execute()](#sqlalchemy.events.ConnectionEvents.before_execute) and
[before_cursor_execute()](#sqlalchemy.events.ConnectionEvents.before_cursor_execute) events only.  When True, the
user-defined event function must have a return value, which
is a tuple of parameters that replace the given statement
and parameters.  See those methods for a description of
specific return arguments.

| Member Name | Description |
| --- | --- |
| after_cursor_execute() | Intercept low-level cursor execute() events after execution. |
| after_execute() | Intercept high level execute() events after execute. |
| before_cursor_execute() | Intercept low-level cursor execute() events before execution,
receiving the string SQL statement and DBAPI-specific parameter list to
be invoked against a cursor. |
| before_execute() | Intercept high level execute() events, receiving uncompiled
SQL constructs and other objects prior to rendering into SQL. |
| begin() | Intercept begin() events. |
| begin_twophase() | Intercept begin_twophase() events. |
| commit() | Intercept commit() events, as initiated by aTransaction. |
| commit_twophase() | Intercept commit_twophase() events. |
| dispatch | reference back to the _Dispatch class. |
| engine_connect() | Intercept the creation of a newConnection. |
| engine_disposed() | Intercept when theEngine.dispose()method is called. |
| prepare_twophase() | Intercept prepare_twophase() events. |
| release_savepoint() | Intercept release_savepoint() events. |
| rollback() | Intercept rollback() events, as initiated by aTransaction. |
| rollback_savepoint() | Intercept rollback_savepoint() events. |
| rollback_twophase() | Intercept rollback_twophase() events. |
| savepoint() | Intercept savepoint() events. |
| set_connection_execution_options() | Intercept when theConnection.execution_options()method is called. |
| set_engine_execution_options() | Intercept when theEngine.execution_options()method is called. |

   method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)after_cursor_execute(*conn:Connection*, *cursor:DBAPICursor*, *statement:str*, *parameters:_DBAPIAnyExecuteParams*, *context:ExecutionContext|None*, *executemany:bool*) → None

Intercept low-level cursor execute() events after execution.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'after_cursor_execute')
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    "listen for the 'after_cursor_execute' event"

    # ... (event handling logic) ...
```

    Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **cursor** – DBAPI cursor object.  Will have results pending
  if the statement was a SELECT, but these should not be consumed
  as they will be needed by the [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult).
- **statement** – string SQL statement, as passed to the DBAPI
- **parameters** – Dictionary, tuple, or list of parameters being
  passed to the `execute()` or `executemany()` method of the
  DBAPI `cursor`.  In some cases may be `None`.
- **context** – [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext) object in use.  May
  be `None`.
- **executemany** – boolean, if `True`, this is an `executemany()`
  call, if `False`, this is an `execute()` call.

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)after_execute(*conn:Connection*, *clauseelement:Executable*, *multiparams:_CoreMultiExecuteParams*, *params:_CoreSingleExecuteParams*, *execution_options:_ExecuteOptions*, *result:Result[Any]*) → None

Intercept high level execute() events after execute.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'after_execute')
def receive_after_execute(conn, clauseelement, multiparams, params, execution_options, result):
    "listen for the 'after_execute' event"

    # ... (event handling logic) ...

# DEPRECATED calling style (pre-1.4, will be removed in a future release)
@event.listens_for(SomeEngine, 'after_execute')
def receive_after_execute(conn, clauseelement, multiparams, params, result):
    "listen for the 'after_execute' event"

    # ... (event handling logic) ...
```

Changed in version 1.4: The [ConnectionEvents.after_execute()](#sqlalchemy.events.ConnectionEvents.after_execute) event now accepts the
arguments [ConnectionEvents.after_execute.conn](#sqlalchemy.events.ConnectionEvents.after_execute.params.conn), [ConnectionEvents.after_execute.clauseelement](#sqlalchemy.events.ConnectionEvents.after_execute.params.clauseelement), [ConnectionEvents.after_execute.multiparams](#sqlalchemy.events.ConnectionEvents.after_execute.params.multiparams), [ConnectionEvents.after_execute.params](#sqlalchemy.events.ConnectionEvents.after_execute.params.params), [ConnectionEvents.after_execute.execution_options](#sqlalchemy.events.ConnectionEvents.after_execute.params.execution_options), [ConnectionEvents.after_execute.result](#sqlalchemy.events.ConnectionEvents.after_execute.params.result).
Support for listener functions which accept the previous
argument signature(s) listed above as “deprecated” will be
removed in a future release.

   Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **clauseelement** – SQL expression construct, [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)
  instance, or string statement passed to
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute).
- **multiparams** – Multiple parameter sets, a list of dictionaries.
- **params** – Single parameter set, a single dictionary.
- **execution_options** –
  dictionary of execution
  options passed along with the statement, if any.  This is a merge
  of all options that will be used, including those of the statement,
  the connection, and those passed in to the method itself for
  the 2.0 style of execution.
- **result** – [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) generated by the
  execution.

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)before_cursor_execute(*conn:Connection*, *cursor:DBAPICursor*, *statement:str*, *parameters:_DBAPIAnyExecuteParams*, *context:ExecutionContext|None*, *executemany:bool*) → [Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[str, _DBAPIAnyExecuteParams] | None

Intercept low-level cursor execute() events before execution,
receiving the string SQL statement and DBAPI-specific parameter list to
be invoked against a cursor.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'before_cursor_execute')
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    "listen for the 'before_cursor_execute' event"

    # ... (event handling logic) ...
```

This event is a good choice for logging as well as late modifications
to the SQL string.  It’s less ideal for parameter modifications except
for those which are specific to a target backend.

This event can be optionally established with the `retval=True`
flag.  The `statement` and `parameters` arguments should be
returned as a two-tuple in this case:

```
@event.listens_for(Engine, "before_cursor_execute", retval=True)
def before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    # do something with statement, parameters
    return statement, parameters
```

See the example at [ConnectionEvents](#sqlalchemy.events.ConnectionEvents).

  Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **cursor** – DBAPI cursor object
- **statement** – string SQL statement, as to be passed to the DBAPI
- **parameters** – Dictionary, tuple, or list of parameters being
  passed to the `execute()` or `executemany()` method of the
  DBAPI `cursor`.  In some cases may be `None`.
- **context** – [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext) object in use.  May
  be `None`.
- **executemany** – boolean, if `True`, this is an `executemany()`
  call, if `False`, this is an `execute()` call.

See also

[before_execute()](#sqlalchemy.events.ConnectionEvents.before_execute)

[after_cursor_execute()](#sqlalchemy.events.ConnectionEvents.after_cursor_execute)

     method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)before_execute(*conn:Connection*, *clauseelement:Executable*, *multiparams:_CoreMultiExecuteParams*, *params:_CoreSingleExecuteParams*, *execution_options:_ExecuteOptions*) → [Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[[Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable), _CoreMultiExecuteParams, _CoreSingleExecuteParams] | None

Intercept high level execute() events, receiving uncompiled
SQL constructs and other objects prior to rendering into SQL.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'before_execute')
def receive_before_execute(conn, clauseelement, multiparams, params, execution_options):
    "listen for the 'before_execute' event"

    # ... (event handling logic) ...

# DEPRECATED calling style (pre-1.4, will be removed in a future release)
@event.listens_for(SomeEngine, 'before_execute')
def receive_before_execute(conn, clauseelement, multiparams, params):
    "listen for the 'before_execute' event"

    # ... (event handling logic) ...
```

Changed in version 1.4: The [ConnectionEvents.before_execute()](#sqlalchemy.events.ConnectionEvents.before_execute) event now accepts the
arguments [ConnectionEvents.before_execute.conn](#sqlalchemy.events.ConnectionEvents.before_execute.params.conn), [ConnectionEvents.before_execute.clauseelement](#sqlalchemy.events.ConnectionEvents.before_execute.params.clauseelement), [ConnectionEvents.before_execute.multiparams](#sqlalchemy.events.ConnectionEvents.before_execute.params.multiparams), [ConnectionEvents.before_execute.params](#sqlalchemy.events.ConnectionEvents.before_execute.params.params), [ConnectionEvents.before_execute.execution_options](#sqlalchemy.events.ConnectionEvents.before_execute.params.execution_options).
Support for listener functions which accept the previous
argument signature(s) listed above as “deprecated” will be
removed in a future release.

This event is good for debugging SQL compilation issues as well
as early manipulation of the parameters being sent to the database,
as the parameter lists will be in a consistent format here.

This event can be optionally established with the `retval=True`
flag.  The `clauseelement`, `multiparams`, and `params`
arguments should be returned as a three-tuple in this case:

```
@event.listens_for(Engine, "before_execute", retval=True)
def before_execute(conn, clauseelement, multiparams, params):
    # do something with clauseelement, multiparams, params
    return clauseelement, multiparams, params
```

   Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **clauseelement** – SQL expression construct, [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)
  instance, or string statement passed to
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute).
- **multiparams** – Multiple parameter sets, a list of dictionaries.
- **params** – Single parameter set, a single dictionary.
- **execution_options** –
  dictionary of execution
  options passed along with the statement, if any.  This is a merge
  of all options that will be used, including those of the statement,
  the connection, and those passed in to the method itself for
  the 2.0 style of execution.

See also

[before_cursor_execute()](#sqlalchemy.events.ConnectionEvents.before_cursor_execute)

     method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)begin(*conn:Connection*) → None

Intercept begin() events.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'begin')
def receive_begin(conn):
    "listen for the 'begin' event"

    # ... (event handling logic) ...
```

    Parameters:

**conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)begin_twophase(*conn:Connection*, *xid:Any*) → None

Intercept begin_twophase() events.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'begin_twophase')
def receive_begin_twophase(conn, xid):
    "listen for the 'begin_twophase' event"

    # ... (event handling logic) ...
```

    Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **xid** – two-phase XID identifier

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)commit(*conn:Connection*) → None

Intercept commit() events, as initiated by a
[Transaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Transaction).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'commit')
def receive_commit(conn):
    "listen for the 'commit' event"

    # ... (event handling logic) ...
```

Note that the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) may also “auto-commit”
a DBAPI connection upon checkin, if the `reset_on_return`
flag is set to the value `'commit'`.  To intercept this
commit, use the [PoolEvents.reset()](#sqlalchemy.events.PoolEvents.reset) hook.

  Parameters:

**conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)commit_twophase(*conn:Connection*, *xid:Any*, *is_prepared:bool*) → None

Intercept commit_twophase() events.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'commit_twophase')
def receive_commit_twophase(conn, xid, is_prepared):
    "listen for the 'commit_twophase' event"

    # ... (event handling logic) ...
```

    Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **xid** – two-phase XID identifier
- **is_prepared** – boolean, indicates if
  [TwoPhaseTransaction.prepare()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TwoPhaseTransaction.prepare) was called.

      attribute [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.ConnectionEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

    method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)engine_connect(*conn:Connection*) → None

Intercept the creation of a new [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'engine_connect')
def receive_engine_connect(conn):
    "listen for the 'engine_connect' event"

    # ... (event handling logic) ...

# DEPRECATED calling style (pre-2.0, will be removed in a future release)
@event.listens_for(SomeEngine, 'engine_connect')
def receive_engine_connect(conn, branch):
    "listen for the 'engine_connect' event"

    # ... (event handling logic) ...
```

Changed in version 2.0: The [ConnectionEvents.engine_connect()](#sqlalchemy.events.ConnectionEvents.engine_connect) event now accepts the
arguments [ConnectionEvents.engine_connect.conn](#sqlalchemy.events.ConnectionEvents.engine_connect.params.conn).
Support for listener functions which accept the previous
argument signature(s) listed above as “deprecated” will be
removed in a future release.

This event is called typically as the direct result of calling
the [Engine.connect()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.connect) method.

It differs from the [PoolEvents.connect()](#sqlalchemy.events.PoolEvents.connect) method, which
refers to the actual connection to a database at the DBAPI level;
a DBAPI connection may be pooled and reused for many operations.
In contrast, this event refers only to the production of a higher level
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) wrapper around such a DBAPI connection.

It also differs from the [PoolEvents.checkout()](#sqlalchemy.events.PoolEvents.checkout) event
in that it is specific to the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object,
not the
DBAPI connection that [PoolEvents.checkout()](#sqlalchemy.events.PoolEvents.checkout) deals with,
although
this DBAPI connection is available here via the
[Connection.connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.connection) attribute.
But note there can in fact
be multiple [PoolEvents.checkout()](#sqlalchemy.events.PoolEvents.checkout)
events within the lifespan
of a single [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object, if that
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
is invalidated and re-established.

  Parameters:

**conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object.

See also

[PoolEvents.checkout()](#sqlalchemy.events.PoolEvents.checkout)
the lower-level pool checkout event
for an individual DBAPI connection

     method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)engine_disposed(*engine:Engine*) → None

Intercept when the [Engine.dispose()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose) method is called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'engine_disposed')
def receive_engine_disposed(engine):
    "listen for the 'engine_disposed' event"

    # ... (event handling logic) ...
```

The [Engine.dispose()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose) method instructs the engine to
“dispose” of it’s connection pool (e.g. [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)), and
replaces it with a new one.  Disposing of the old pool has the
effect that existing checked-in connections are closed.  The new
pool does not establish any new connections until it is first used.

This event can be used to indicate that resources related to the
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) should also be cleaned up,
keeping in mind that the
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
can still be used for new requests in which case
it re-acquires connection resources.

    method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)prepare_twophase(*conn:Connection*, *xid:Any*) → None

Intercept prepare_twophase() events.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'prepare_twophase')
def receive_prepare_twophase(conn, xid):
    "listen for the 'prepare_twophase' event"

    # ... (event handling logic) ...
```

    Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **xid** – two-phase XID identifier

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)release_savepoint(*conn:Connection*, *name:str*, *context:None*) → None

Intercept release_savepoint() events.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'release_savepoint')
def receive_release_savepoint(conn, name, context):
    "listen for the 'release_savepoint' event"

    # ... (event handling logic) ...
```

    Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **name** – specified name used for the savepoint.
- **context** – not used

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)rollback(*conn:Connection*) → None

Intercept rollback() events, as initiated by a
[Transaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Transaction).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'rollback')
def receive_rollback(conn):
    "listen for the 'rollback' event"

    # ... (event handling logic) ...
```

Note that the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) also “auto-rolls back”
a DBAPI connection upon checkin, if the `reset_on_return`
flag is set to its default value of `'rollback'`.
To intercept this
rollback, use the [PoolEvents.reset()](#sqlalchemy.events.PoolEvents.reset) hook.

  Parameters:

**conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object

See also

[PoolEvents.reset()](#sqlalchemy.events.PoolEvents.reset)

     method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)rollback_savepoint(*conn:Connection*, *name:str*, *context:None*) → None

Intercept rollback_savepoint() events.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'rollback_savepoint')
def receive_rollback_savepoint(conn, name, context):
    "listen for the 'rollback_savepoint' event"

    # ... (event handling logic) ...
```

    Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **name** – specified name used for the savepoint.
- **context** – not used

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)rollback_twophase(*conn:Connection*, *xid:Any*, *is_prepared:bool*) → None

Intercept rollback_twophase() events.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'rollback_twophase')
def receive_rollback_twophase(conn, xid, is_prepared):
    "listen for the 'rollback_twophase' event"

    # ... (event handling logic) ...
```

    Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **xid** – two-phase XID identifier
- **is_prepared** – boolean, indicates if
  [TwoPhaseTransaction.prepare()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TwoPhaseTransaction.prepare) was called.

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)savepoint(*conn:Connection*, *name:str*) → None

Intercept savepoint() events.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'savepoint')
def receive_savepoint(conn, name):
    "listen for the 'savepoint' event"

    # ... (event handling logic) ...
```

    Parameters:

- **conn** – [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **name** – specified name used for the savepoint.

      method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)set_connection_execution_options(*conn:Connection*, *opts:Dict[str,Any]*) → None

Intercept when the [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options)
method is called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'set_connection_execution_options')
def receive_set_connection_execution_options(conn, opts):
    "listen for the 'set_connection_execution_options' event"

    # ... (event handling logic) ...
```

This method is called after the new [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
has been
produced, with the newly updated execution options collection, but
before the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) has acted upon any of those new options.

Note that this method is not called when a new
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
is produced which is inheriting execution options from its parent
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine); to intercept this condition, use the
[ConnectionEvents.engine_connect()](#sqlalchemy.events.ConnectionEvents.engine_connect) event.

  Parameters:

- **conn** – The newly copied [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
- **opts** –
  dictionary of options that were passed to the
  [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) method.
  This dictionary may be modified in place to affect the ultimate
  options which take effect.
  Added in version 2.0: the `opts` dictionary may be modified
  in place.

See also

[ConnectionEvents.set_engine_execution_options()](#sqlalchemy.events.ConnectionEvents.set_engine_execution_options)
- event
which is called when [Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options)
is called.

     method [sqlalchemy.events.ConnectionEvents.](#sqlalchemy.events.ConnectionEvents)set_engine_execution_options(*engine:Engine*, *opts:Dict[str,Any]*) → None

Intercept when the [Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options)
method is called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'set_engine_execution_options')
def receive_set_engine_execution_options(engine, opts):
    "listen for the 'set_engine_execution_options' event"

    # ... (event handling logic) ...
```

The [Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options) method produces a shallow
copy of the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which stores the new options.
That new
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) is passed here.
A particular application of this
method is to add a [ConnectionEvents.engine_connect()](#sqlalchemy.events.ConnectionEvents.engine_connect)
event
handler to the given [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
which will perform some per-
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) task specific to these execution options.

  Parameters:

- **conn** – The newly copied [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object
- **opts** –
  dictionary of options that were passed to the
  [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) method.
  This dictionary may be modified in place to affect the ultimate
  options which take effect.
  Added in version 2.0: the `opts` dictionary may be modified
  in place.

See also

[ConnectionEvents.set_connection_execution_options()](#sqlalchemy.events.ConnectionEvents.set_connection_execution_options)
- event
which is called when [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options)
is
called.

      class sqlalchemy.events.DialectEvents

*inherits from* `sqlalchemy.event.Events`

event interface for execution-replacement functions.

These events allow direct instrumentation and replacement
of key dialect functions which interact with the DBAPI.

Note

[DialectEvents](#sqlalchemy.events.DialectEvents) hooks should be considered **semi-public**
and experimental.
These hooks are not for general use and are only for those situations
where intricate re-statement of DBAPI mechanics must be injected onto
an existing dialect.  For general-use statement-interception events,
please use the [ConnectionEvents](#sqlalchemy.events.ConnectionEvents) interface.

See also

[ConnectionEvents.before_cursor_execute()](#sqlalchemy.events.ConnectionEvents.before_cursor_execute)

[ConnectionEvents.before_execute()](#sqlalchemy.events.ConnectionEvents.before_execute)

[ConnectionEvents.after_cursor_execute()](#sqlalchemy.events.ConnectionEvents.after_cursor_execute)

[ConnectionEvents.after_execute()](#sqlalchemy.events.ConnectionEvents.after_execute)

| Member Name | Description |
| --- | --- |
| dispatch | reference back to the _Dispatch class. |
| do_connect() | Receive connection arguments before a connection is made. |
| do_execute() | Receive a cursor to have execute() called. |
| do_execute_no_params() | Receive a cursor to have execute() with no parameters called. |
| do_executemany() | Receive a cursor to have executemany() called. |
| do_setinputsizes() | Receive the setinputsizes dictionary for possible modification. |
| handle_error() | Intercept all exceptions processed by theDialect, typically but not limited to those
emitted within the scope of aConnection. |

   attribute [sqlalchemy.events.DialectEvents.](#sqlalchemy.events.DialectEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.DialectEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

    method [sqlalchemy.events.DialectEvents.](#sqlalchemy.events.DialectEvents)do_connect(*dialect:Dialect*, *conn_rec:ConnectionPoolEntry*, *cargs:Tuple[Any,...]*, *cparams:Dict[str,Any]*) → [DBAPIConnection](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPIConnection) | None

Receive connection arguments before a connection is made.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'do_connect')
def receive_do_connect(dialect, conn_rec, cargs, cparams):
    "listen for the 'do_connect' event"

    # ... (event handling logic) ...
```

This event is useful in that it allows the handler to manipulate the
cargs and/or cparams collections that control how the DBAPI
`connect()` function will be called. `cargs` will always be a
Python list that can be mutated in-place, and `cparams` a Python
dictionary that may also be mutated:

```
e = create_engine("postgresql+psycopg2://user@host/dbname")

@event.listens_for(e, "do_connect")
def receive_do_connect(dialect, conn_rec, cargs, cparams):
    cparams["password"] = "some_password"
```

The event hook may also be used to override the call to `connect()`
entirely, by returning a non-`None` DBAPI connection object:

```
e = create_engine("postgresql+psycopg2://user@host/dbname")

@event.listens_for(e, "do_connect")
def receive_do_connect(dialect, conn_rec, cargs, cparams):
    return psycopg2.connect(*cargs, **cparams)
```

See also

[Custom DBAPI connect() arguments / on-connect routines](https://docs.sqlalchemy.org/en/20/core/engines.html#custom-dbapi-args)

     method [sqlalchemy.events.DialectEvents.](#sqlalchemy.events.DialectEvents)do_execute(*cursor:DBAPICursor*, *statement:str*, *parameters:_DBAPISingleExecuteParams*, *context:ExecutionContext*) → Literal[True] | None

Receive a cursor to have execute() called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'do_execute')
def receive_do_execute(cursor, statement, parameters, context):
    "listen for the 'do_execute' event"

    # ... (event handling logic) ...
```

Return the value True to halt further events from invoking,
and to indicate that the cursor execution has already taken
place within the event handler.

    method [sqlalchemy.events.DialectEvents.](#sqlalchemy.events.DialectEvents)do_execute_no_params(*cursor:DBAPICursor*, *statement:str*, *context:ExecutionContext*) → Literal[True] | None

Receive a cursor to have execute() with no parameters called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'do_execute_no_params')
def receive_do_execute_no_params(cursor, statement, context):
    "listen for the 'do_execute_no_params' event"

    # ... (event handling logic) ...
```

Return the value True to halt further events from invoking,
and to indicate that the cursor execution has already taken
place within the event handler.

    method [sqlalchemy.events.DialectEvents.](#sqlalchemy.events.DialectEvents)do_executemany(*cursor:DBAPICursor*, *statement:str*, *parameters:_DBAPIMultiExecuteParams*, *context:ExecutionContext*) → Literal[True] | None

Receive a cursor to have executemany() called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'do_executemany')
def receive_do_executemany(cursor, statement, parameters, context):
    "listen for the 'do_executemany' event"

    # ... (event handling logic) ...
```

Return the value True to halt further events from invoking,
and to indicate that the cursor execution has already taken
place within the event handler.

    method [sqlalchemy.events.DialectEvents.](#sqlalchemy.events.DialectEvents)do_setinputsizes(*inputsizes:Dict[BindParameter[Any],Any]*, *cursor:DBAPICursor*, *statement:str*, *parameters:_DBAPIAnyExecuteParams*, *context:ExecutionContext*) → None

Receive the setinputsizes dictionary for possible modification.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'do_setinputsizes')
def receive_do_setinputsizes(inputsizes, cursor, statement, parameters, context):
    "listen for the 'do_setinputsizes' event"

    # ... (event handling logic) ...
```

This event is emitted in the case where the dialect makes use of the
DBAPI `cursor.setinputsizes()` method which passes information about
parameter binding for a particular statement.   The given
`inputsizes` dictionary will contain [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects
as keys, linked to DBAPI-specific type objects as values; for
parameters that are not bound, they are added to the dictionary with
`None` as the value, which means the parameter will not be included
in the ultimate setinputsizes call.   The event may be used to inspect
and/or log the datatypes that are being bound, as well as to modify the
dictionary in place.  Parameters can be added, modified, or removed
from this dictionary.   Callers will typically want to inspect the
`BindParameter.type` attribute of the given bind objects in
order to make decisions about the DBAPI object.

After the event, the `inputsizes` dictionary is converted into
an appropriate datastructure to be passed to `cursor.setinputsizes`;
either a list for a positional bound parameter execution style,
or a dictionary of string parameter keys to DBAPI type objects for
a named bound parameter execution style.

The setinputsizes hook overall is only used for dialects which include
the flag `use_setinputsizes=True`.  Dialects which use this
include python-oracledb, cx_Oracle, pg8000, asyncpg, and pyodbc
dialects.

Note

For use with pyodbc, the `use_setinputsizes` flag
must be passed to the dialect, e.g.:

```
create_engine("mssql+pyodbc://...", use_setinputsizes=True)
```

See also

[Setinputsizes Support](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-pyodbc-setinputsizes)

Added in version 1.2.9.

See also

[Fine grained control over cx_Oracle data binding performance with setinputsizes](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#cx-oracle-setinputsizes)

     method [sqlalchemy.events.DialectEvents.](#sqlalchemy.events.DialectEvents)handle_error(*exception_context:ExceptionContext*) → BaseException | None

Intercept all exceptions processed by the
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect), typically but not limited to those
emitted within the scope of a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeEngine, 'handle_error')
def receive_handle_error(exception_context):
    "listen for the 'handle_error' event"

    # ... (event handling logic) ...
```

Changed in version 2.0: the [DialectEvents.handle_error()](#sqlalchemy.events.DialectEvents.handle_error) event
is moved to the [DialectEvents](#sqlalchemy.events.DialectEvents) class, moved from the
[ConnectionEvents](#sqlalchemy.events.ConnectionEvents) class, so that it may also participate in
the “pre ping” operation configured with the
[create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) parameter. The event
remains registered by using the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) as the event
target, however note that using the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) as
an event target for [DialectEvents.handle_error()](#sqlalchemy.events.DialectEvents.handle_error) is no longer
supported.

This includes all exceptions emitted by the DBAPI as well as
within SQLAlchemy’s statement invocation process, including
encoding errors and other statement validation errors.  Other areas
in which the event is invoked include transaction begin and end,
result row fetching, cursor creation.

Note that [handle_error()](#sqlalchemy.events.DialectEvents.handle_error) may support new kinds of exceptions
and new calling scenarios at *any time*.  Code which uses this
event must expect new calling patterns to be present in minor
releases.

To support the wide variety of members that correspond to an exception,
as well as to allow extensibility of the event without backwards
incompatibility, the sole argument received is an instance of
[ExceptionContext](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext).   This object contains data members
representing detail about the exception.

Use cases supported by this hook include:

- read-only, low-level exception handling for logging and
  debugging purposes
- Establishing whether a DBAPI connection error message indicates
  that the database connection needs to be reconnected, including
  for the “pre_ping” handler used by **some** dialects
- Establishing or disabling whether a connection or the owning
  connection pool is invalidated or expired in response to a
  specific exception
- exception re-writing

The hook is called while the cursor from the failed operation
(if any) is still open and accessible.   Special cleanup operations
can be called on this cursor; SQLAlchemy will attempt to close
this cursor subsequent to this hook being invoked.

As of SQLAlchemy 2.0, the “pre_ping” handler enabled using the
[create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) parameter will also
participate in the [handle_error()](#sqlalchemy.events.DialectEvents.handle_error) process, **for those dialects
that rely upon disconnect codes to detect database liveness**. Note
that some dialects such as psycopg, psycopg2, and most MySQL dialects
make use of a native `ping()` method supplied by the DBAPI which does
not make use of disconnect codes.

Changed in version 2.0.0: The [DialectEvents.handle_error()](#sqlalchemy.events.DialectEvents.handle_error)
event hook participates in connection pool “pre-ping” operations.
Within this usage, the [ExceptionContext.engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext.engine) attribute
will be `None`, however the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in use is always
available via the [ExceptionContext.dialect](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext.dialect) attribute.

Changed in version 2.0.5: Added [ExceptionContext.is_pre_ping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext.is_pre_ping)
attribute which will be set to `True` when the
[DialectEvents.handle_error()](#sqlalchemy.events.DialectEvents.handle_error) event hook is triggered within
a connection pool pre-ping operation.

Changed in version 2.0.5: An issue was repaired that allows for the
PostgreSQL `psycopg` and `psycopg2` drivers, as well as all
MySQL drivers, to properly participate in the
[DialectEvents.handle_error()](#sqlalchemy.events.DialectEvents.handle_error) event hook during
connection pool “pre-ping” operations; previously, the
implementation was non-working for these drivers.

A handler function has two options for replacing
the SQLAlchemy-constructed exception into one that is user
defined.   It can either raise this new exception directly, in
which case all further event listeners are bypassed and the
exception will be raised, after appropriate cleanup as taken
place:

```
@event.listens_for(Engine, "handle_error")
def handle_exception(context):
    if isinstance(
        context.original_exception, psycopg2.OperationalError
    ) and "failed" in str(context.original_exception):
        raise MySpecialException("failed operation")
```

Warning

Because the
[DialectEvents.handle_error()](#sqlalchemy.events.DialectEvents.handle_error)
event specifically provides for exceptions to be re-thrown as
the ultimate exception raised by the failed statement,
**stack traces will be misleading** if the user-defined event
handler itself fails and throws an unexpected exception;
the stack trace may not illustrate the actual code line that
failed!  It is advised to code carefully here and use
logging and/or inline debugging if unexpected exceptions are
occurring.

Alternatively, a “chained” style of event handling can be
used, by configuring the handler with the `retval=True`
modifier and returning the new exception instance from the
function.  In this case, event handling will continue onto the
next handler.   The “chained” exception is available using
[ExceptionContext.chained_exception](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext.chained_exception):

```
@event.listens_for(Engine, "handle_error", retval=True)
def handle_exception(context):
    if (
        context.chained_exception is not None
        and "special" in context.chained_exception.message
    ):
        return MySpecialException(
            "failed", cause=context.chained_exception
        )
```

Handlers that return `None` may be used within the chain; when
a handler returns `None`, the previous exception instance,
if any, is maintained as the current exception that is passed onto the
next handler.

When a custom exception is raised or returned, SQLAlchemy raises
this new exception as-is, it is not wrapped by any SQLAlchemy
object.  If the exception is not a subclass of
[sqlalchemy.exc.StatementError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.StatementError),
certain features may not be available; currently this includes
the ORM’s feature of adding a detail hint about “autoflush” to
exceptions raised within the autoflush process.

  Parameters:

**context** – an [ExceptionContext](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext) object.  See this
class for details on all available members.

See also

[Supporting new database error codes for disconnect scenarios](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-new-disconnect-codes)

## Schema Events

| Object Name | Description |
| --- | --- |
| DDLEvents | Define event listeners for schema objects,
that is,SchemaItemand otherSchemaEventTargetsubclasses, includingMetaData,Table,Column, etc. |
| SchemaEventTarget | Base class for elements that are the targets ofDDLEventsevents. |

   class sqlalchemy.events.DDLEvents

*inherits from* `sqlalchemy.event.Events`

Define event listeners for schema objects,
that is, [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) and other [SchemaEventTarget](#sqlalchemy.events.SchemaEventTarget)
subclasses, including [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData), [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table),
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), etc.

**Create / Drop Events**

Events emitted when CREATE and DROP commands are emitted to the database.
The event hooks in this category include [DDLEvents.before_create()](#sqlalchemy.events.DDLEvents.before_create),
[DDLEvents.after_create()](#sqlalchemy.events.DDLEvents.after_create), [DDLEvents.before_drop()](#sqlalchemy.events.DDLEvents.before_drop), and
[DDLEvents.after_drop()](#sqlalchemy.events.DDLEvents.after_drop).

These events are emitted when using schema-level methods such as
[MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) and [MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all). Per-object
create/drop methods such as [Table.create()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.create), [Table.drop()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.drop),
[Index.create()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index.create) are also included, as well as dialect-specific
methods such as [ENUM.create()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM.create).

Added in version 2.0: [DDLEvents](#sqlalchemy.events.DDLEvents) event hooks now take place
for non-table objects including constraints, indexes, and
dialect-specific schema types.

Event hooks may be attached directly to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object or
to a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection, as well as to any
[SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) class or object that can be individually created and
dropped using a distinct SQL command. Such classes include [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index),
[Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), and dialect-specific classes such as
[ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM).

Example using the [DDLEvents.after_create()](#sqlalchemy.events.DDLEvents.after_create) event, where a custom
event hook will emit an `ALTER TABLE` command on the current connection,
after `CREATE TABLE` is emitted:

```
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import Table, Column, Metadata, Integer

m = MetaData()
some_table = Table("some_table", m, Column("data", Integer))

@event.listens_for(some_table, "after_create")
def after_create(target, connection, **kw):
    connection.execute(
        text("ALTER TABLE %s SET name=foo_%s" % (target.name, target.name))
    )

some_engine = create_engine("postgresql://scott:tiger@host/test")

# will emit "CREATE TABLE some_table" as well as the above
# "ALTER TABLE" statement afterwards
m.create_all(some_engine)
```

Constraint objects such as [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint),
[UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint), [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) may also be
subscribed to these events, however they will **not** normally produce
events as these objects are usually rendered inline within an
enclosing `CREATE TABLE` statement and implicitly dropped from a
`DROP TABLE` statement.

For the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct, the event hook will be emitted
for `CREATE INDEX`, however SQLAlchemy does not normally emit
`DROP INDEX` when dropping tables as this is again implicit within the
`DROP TABLE` statement.

Added in version 2.0: Support for [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) objects
for create/drop events was expanded from its previous support for
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) and [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) to also include
[Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) and all subclasses, [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index),
[Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) and some type-related constructs such as
[ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM).

Note

These event hooks are only emitted within the scope of
SQLAlchemy’s create/drop methods; they are not necessarily supported
by tools such as [alembic](https://alembic.sqlalchemy.org).

**Attachment Events**

Attachment events are provided to customize
behavior whenever a child schema element is associated
with a parent, such as when a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is associated
with its [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), when a
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
is associated with a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), etc.  These events include
[DDLEvents.before_parent_attach()](#sqlalchemy.events.DDLEvents.before_parent_attach) and
[DDLEvents.after_parent_attach()](#sqlalchemy.events.DDLEvents.after_parent_attach).

**Reflection Events**

The [DDLEvents.column_reflect()](#sqlalchemy.events.DDLEvents.column_reflect) event is used to intercept
and modify the in-Python definition of database columns when
[reflection](https://docs.sqlalchemy.org/en/20/glossary.html#term-reflection) of database tables proceeds.

**Use with Generic DDL**

DDL events integrate closely with the
[DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DDL) class and the [ExecutableDDLElement](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement) hierarchy
of DDL clause constructs, which are themselves appropriate
as listener callables:

```
from sqlalchemy import DDL

event.listen(
    some_table,
    "after_create",
    DDL("ALTER TABLE %(table)s SET name=foo_%(table)s"),
)
```

**Event Propagation to MetaData Copies**

For all `DDLEvent` events, the `propagate=True` keyword argument
will ensure that a given event handler is propagated to copies of the
object, which are made when using the [Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata)
method:

```
from sqlalchemy import DDL

metadata = MetaData()
some_table = Table("some_table", metadata, Column("data", Integer))

event.listen(
    some_table,
    "after_create",
    DDL("ALTER TABLE %(table)s SET name=foo_%(table)s"),
    propagate=True,
)

new_metadata = MetaData()
new_table = some_table.to_metadata(new_metadata)
```

The above [DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DDL) object will be associated with the
[DDLEvents.after_create()](#sqlalchemy.events.DDLEvents.after_create) event for both the `some_table` and
the `new_table` [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects.

See also

[Events](https://docs.sqlalchemy.org/en/20/core/event.html)

[ExecutableDDLElement](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement)

[DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DDL)

[Controlling DDL Sequences](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-sequences)

| Member Name | Description |
| --- | --- |
| after_create() | Called after CREATE statements are emitted. |
| after_drop() | Called after DROP statements are emitted. |
| after_parent_attach() | Called after aSchemaItemis associated with
a parentSchemaItem. |
| before_create() | Called before CREATE statements are emitted. |
| before_drop() | Called before DROP statements are emitted. |
| before_parent_attach() | Called before aSchemaItemis associated with
a parentSchemaItem. |
| column_reflect() | Called for each unit of ‘column info’ retrieved when
aTableis being reflected. |
| dispatch | reference back to the _Dispatch class. |

   method [sqlalchemy.events.DDLEvents.](#sqlalchemy.events.DDLEvents)after_create(*target:SchemaEventTarget*, *connection:Connection*, ***kw:Any*) → None

Called after CREATE statements are emitted.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSchemaClassOrObject, 'after_create')
def receive_after_create(target, connection, **kw):
    "listen for the 'after_create' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** –
  the `SchemaObject`, such as a
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) or [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  but also including all create/drop objects such as
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), etc.,
  object which is the target of the event.
  Added in version 2.0: Support for all [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) objects
  was added.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) where the
  CREATE statement or statements have been emitted.
- ****kw** – additional keyword arguments relevant
  to the event.  The contents of this dictionary
  may vary across releases, and include the
  list of tables being generated for a metadata-level
  event, the checkfirst flag, and other
  elements used by internal events.

[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) also accepts the `propagate=True`
modifier for this event; when True, the listener function will
be established for any copies made of the target object,
i.e. those copies that are generated when
[Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) is used.

    method [sqlalchemy.events.DDLEvents.](#sqlalchemy.events.DDLEvents)after_drop(*target:SchemaEventTarget*, *connection:Connection*, ***kw:Any*) → None

Called after DROP statements are emitted.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSchemaClassOrObject, 'after_drop')
def receive_after_drop(target, connection, **kw):
    "listen for the 'after_drop' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** –
  the `SchemaObject`, such as a
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) or [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  but also including all create/drop objects such as
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), etc.,
  object which is the target of the event.
  Added in version 2.0: Support for all [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) objects
  was added.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) where the
  DROP statement or statements have been emitted.
- ****kw** – additional keyword arguments relevant
  to the event.  The contents of this dictionary
  may vary across releases, and include the
  list of tables being generated for a metadata-level
  event, the checkfirst flag, and other
  elements used by internal events.

[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) also accepts the `propagate=True`
modifier for this event; when True, the listener function will
be established for any copies made of the target object,
i.e. those copies that are generated when
[Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) is used.

    method [sqlalchemy.events.DDLEvents.](#sqlalchemy.events.DDLEvents)after_parent_attach(*target:SchemaEventTarget*, *parent:SchemaItem*) → None

Called after a [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) is associated with
a parent [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSchemaClassOrObject, 'after_parent_attach')
def receive_after_parent_attach(target, parent):
    "listen for the 'after_parent_attach' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** – the target object
- **parent** – the parent to which the target is being attached.

[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) also accepts the `propagate=True`
modifier for this event; when True, the listener function will
be established for any copies made of the target object,
i.e. those copies that are generated when
[Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) is used.

    method [sqlalchemy.events.DDLEvents.](#sqlalchemy.events.DDLEvents)before_create(*target:SchemaEventTarget*, *connection:Connection*, ***kw:Any*) → None

Called before CREATE statements are emitted.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSchemaClassOrObject, 'before_create')
def receive_before_create(target, connection, **kw):
    "listen for the 'before_create' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** –
  the `SchemaObject`, such as a
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) or [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  but also including all create/drop objects such as
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), etc.,
  object which is the target of the event.
  Added in version 2.0: Support for all [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) objects
  was added.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) where the
  CREATE statement or statements will be emitted.
- ****kw** – additional keyword arguments relevant
  to the event.  The contents of this dictionary
  may vary across releases, and include the
  list of tables being generated for a metadata-level
  event, the checkfirst flag, and other
  elements used by internal events.

[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) accepts the `propagate=True`
modifier for this event; when True, the listener function will
be established for any copies made of the target object,
i.e. those copies that are generated when
[Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) is used.

[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) accepts the `insert=True`
modifier for this event; when True, the listener function will
be prepended to the internal list of events upon discovery, and execute
before registered listener functions that do not pass this argument.

    method [sqlalchemy.events.DDLEvents.](#sqlalchemy.events.DDLEvents)before_drop(*target:SchemaEventTarget*, *connection:Connection*, ***kw:Any*) → None

Called before DROP statements are emitted.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSchemaClassOrObject, 'before_drop')
def receive_before_drop(target, connection, **kw):
    "listen for the 'before_drop' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** –
  the `SchemaObject`, such as a
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) or [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  but also including all create/drop objects such as
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), etc.,
  object which is the target of the event.
  Added in version 2.0: Support for all [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) objects
  was added.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) where the
  DROP statement or statements will be emitted.
- ****kw** – additional keyword arguments relevant
  to the event.  The contents of this dictionary
  may vary across releases, and include the
  list of tables being generated for a metadata-level
  event, the checkfirst flag, and other
  elements used by internal events.

[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) also accepts the `propagate=True`
modifier for this event; when True, the listener function will
be established for any copies made of the target object,
i.e. those copies that are generated when
[Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) is used.

    method [sqlalchemy.events.DDLEvents.](#sqlalchemy.events.DDLEvents)before_parent_attach(*target:SchemaEventTarget*, *parent:SchemaItem*) → None

Called before a [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) is associated with
a parent [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSchemaClassOrObject, 'before_parent_attach')
def receive_before_parent_attach(target, parent):
    "listen for the 'before_parent_attach' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** – the target object
- **parent** – the parent to which the target is being attached.

[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) also accepts the `propagate=True`
modifier for this event; when True, the listener function will
be established for any copies made of the target object,
i.e. those copies that are generated when
[Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) is used.

    method [sqlalchemy.events.DDLEvents.](#sqlalchemy.events.DDLEvents)column_reflect(*inspector:Inspector*, *table:Table*, *column_info:ReflectedColumn*) → None

Called for each unit of ‘column info’ retrieved when
a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is being reflected.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSchemaClassOrObject, 'column_reflect')
def receive_column_reflect(inspector, table, column_info):
    "listen for the 'column_reflect' event"

    # ... (event handling logic) ...
```

This event is most easily used by applying it to a specific
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) instance, where it will take effect for
all [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects within that
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) that undergo reflection:

```
metadata = MetaData()

@event.listens_for(metadata, "column_reflect")
def receive_column_reflect(inspector, table, column_info):
    # receives for all Table objects that are reflected
    # under this MetaData
    ...

# will use the above event hook
my_table = Table("my_table", metadata, autoload_with=some_engine)
```

Added in version 1.4.0b2: The [DDLEvents.column_reflect()](#sqlalchemy.events.DDLEvents.column_reflect)
hook may now be applied to a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object as
well as the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) class itself where it will
take place for all [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects associated with
the targeted [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData).

It may also be applied to the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) class across
the board:

```
from sqlalchemy import Table

@event.listens_for(Table, "column_reflect")
def receive_column_reflect(inspector, table, column_info):
    # receives for all Table objects that are reflected
    ...
```

It can also be applied to a specific [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) at the
point that one is being reflected using the
[Table.listeners](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.listeners) parameter:

```
t1 = Table(
    "my_table",
    autoload_with=some_engine,
    listeners=[("column_reflect", receive_column_reflect)],
)
```

The dictionary of column information as returned by the
dialect is passed, and can be modified.  The dictionary
is that returned in each element of the list returned
by [Inspector.get_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns):

> - `name` - the column’s name, is applied to the
>   [Column.name](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.name) parameter
> - `type` - the type of this column, which should be an instance
>   of [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine), is applied to the
>   [Column.type](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.type) parameter
> - `nullable` - boolean flag if the column is NULL or NOT NULL,
>   is applied to the [Column.nullable](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.nullable) parameter
> - `default` - the column’s server default value.  This is
>   normally specified as a plain string SQL expression, however the
>   event can pass a [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue), [DefaultClause](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.DefaultClause),
>   or [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) object as well.  Is applied to the
>   [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) parameter

The event is called before any action is taken against
this dictionary, and the contents can be modified; the following
additional keys may be added to the dictionary to further modify
how the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is constructed:

> - `key` - the string key that will be used to access this
>   [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) in the `.c` collection; will be applied
>   to the [Column.key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.key) parameter. Is also used
>   for ORM mapping.  See the section
>   [Automating Column Naming Schemes from Reflected Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapper-automated-reflection-schemes) for an example.
> - `quote` - force or un-force quoting on the column name;
>   is applied to the [Column.quote](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.quote) parameter.
> - `info` - a dictionary of arbitrary data to follow along with
>   the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), is applied to the
>   [Column.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.info) parameter.

[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) also accepts the `propagate=True`
modifier for this event; when True, the listener function will
be established for any copies made of the target object,
i.e. those copies that are generated when
[Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) is used.

See also

[Automating Column Naming Schemes from Reflected Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapper-automated-reflection-schemes) -
in the ORM mapping documentation

[Intercepting Column Definitions](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#automap-intercepting-columns) -
in the [Automap](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html) documentation

[Reflecting with Database-Agnostic Types](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection-dbagnostic-types) - in
the [Reflecting Database Objects](https://docs.sqlalchemy.org/en/20/core/reflection.html) documentation

     attribute [sqlalchemy.events.DDLEvents.](#sqlalchemy.events.DDLEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.DDLEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

     class sqlalchemy.events.SchemaEventTarget

*inherits from* `sqlalchemy.event.registry.EventTarget`

Base class for elements that are the targets of [DDLEvents](#sqlalchemy.events.DDLEvents)
events.

This includes [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) as well as [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType).
