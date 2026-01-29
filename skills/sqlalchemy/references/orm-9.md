# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# ORM Events

The ORM includes a wide variety of hooks available for subscription.

For an introduction to the most commonly used ORM events, see the section
[Tracking queries, object and Session Changes with Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html).   The event system in general is discussed
at [Events](https://docs.sqlalchemy.org/en/20/core/event.html).  Non-ORM events such as those regarding connections
and low-level statement execution are described in [Core Events](https://docs.sqlalchemy.org/en/20/core/events.html).

## Session Events

The most basic event hooks are available at the level of the ORM
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object.   The types of things that are intercepted
here include:

- **Persistence Operations** - the ORM flush process that sends changes to the
  database can be extended using events that fire off at different parts of the
  flush, to augment or modify the data being sent to the database or to allow
  other things to happen when persistence occurs.   Read more about persistence
  events at [Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events).
- **Object lifecycle events** - hooks when objects are added, persisted,
  deleted from sessions.   Read more about these at
  [Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events).
- **Execution Events** - Part of the [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) execution model, all
  SELECT statements against ORM entities emitted, as well as bulk UPDATE
  and DELETE statements outside of the flush process, are intercepted
  from the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method using the
  [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) method.  Read more about this
  event at [Execute Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-execute-events).

Be sure to read the [Tracking queries, object and Session Changes with Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html) chapter for context
on these events.

| Object Name | Description |
| --- | --- |
| SessionEvents | Define events specific toSessionlifecycle. |

   class sqlalchemy.orm.SessionEvents

*inherits from* `sqlalchemy.event.Events`

Define events specific to [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) lifecycle.

e.g.:

```
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

def my_before_commit(session):
    print("before commit!")

Session = sessionmaker()

event.listen(Session, "before_commit", my_before_commit)
```

The [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) function will accept
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects as well as the return result
of [sessionmaker()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) and [scoped_session()](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoped_session).

Additionally, it accepts the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class which
will apply listeners to all [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) instances
globally.

  Parameters:

- **raw=False** –
  When True, the “target” argument passed
  to applicable event listener functions that work on individual
  objects will be the instance’s [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) management
  object, rather than the mapped instance itself.
  Added in version 1.3.14.
- **restore_load_context=False** –
  Applies to the
  [SessionEvents.loaded_as_persistent()](#sqlalchemy.orm.SessionEvents.loaded_as_persistent) event.  Restores the loader
  context of the object when the event hook is complete, so that ongoing
  eager load operations continue to target the object appropriately.  A
  warning is emitted if the object is moved to a new loader context from
  within this event if this flag is not set.
  Added in version 1.3.14.

| Member Name | Description |
| --- | --- |
| after_attach() | Execute after an instance is attached to a session. |
| after_begin() | Execute after a transaction is begun on a connection. |
| after_bulk_delete() | Event for after the legacyQuery.delete()method
has been called. |
| after_bulk_update() | Event for after the legacyQuery.update()method
has been called. |
| after_commit() | Execute after a commit has occurred. |
| after_flush() | Execute after flush has completed, but before commit has been
called. |
| after_flush_postexec() | Execute after flush has completed, and after the post-exec
state occurs. |
| after_rollback() | Execute after a real DBAPI rollback has occurred. |
| after_soft_rollback() | Execute after any rollback has occurred, including “soft”
rollbacks that don’t actually emit at the DBAPI level. |
| after_transaction_create() | Execute when a newSessionTransactionis created. |
| after_transaction_end() | Execute when the span of aSessionTransactionends. |
| before_attach() | Execute before an instance is attached to a session. |
| before_commit() | Execute before commit is called. |
| before_flush() | Execute before flush process has started. |
| deleted_to_detached() | Intercept the “deleted to detached” transition for a specific
object. |
| deleted_to_persistent() | Intercept the “deleted to persistent” transition for a specific
object. |
| detached_to_persistent() | Intercept the “detached to persistent” transition for a specific
object. |
| dispatch | reference back to the _Dispatch class. |
| do_orm_execute() | Intercept statement executions that occur on behalf of an
ORMSessionobject. |
| loaded_as_persistent() | Intercept the “loaded as persistent” transition for a specific
object. |
| pending_to_persistent() | Intercept the “pending to persistent”” transition for a specific
object. |
| pending_to_transient() | Intercept the “pending to transient” transition for a specific
object. |
| persistent_to_deleted() | Intercept the “persistent to deleted” transition for a specific
object. |
| persistent_to_detached() | Intercept the “persistent to detached” transition for a specific
object. |
| persistent_to_transient() | Intercept the “persistent to transient” transition for a specific
object. |
| transient_to_pending() | Intercept the “transient to pending” transition for a specific
object. |

   method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_attach(*session:Session*, *instance:_O*) → None

Execute after an instance is attached to a session.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_attach')
def receive_after_attach(session, instance):
    "listen for the 'after_attach' event"

    # ... (event handling logic) ...
```

This is called after an add, delete or merge.

Note

As of 0.8, this event fires off *after* the item
has been fully associated with the session, which is
different than previous releases.  For event
handlers that require the object not yet
be part of session state (such as handlers which
may autoflush while the target object is not
yet complete) consider the
new [before_attach()](#sqlalchemy.orm.SessionEvents.before_attach) event.

See also

[SessionEvents.before_attach()](#sqlalchemy.orm.SessionEvents.before_attach)

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_begin(*session:Session*, *transaction:SessionTransaction*, *connection:Connection*) → None

Execute after a transaction is begun on a connection.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_begin')
def receive_after_begin(session, transaction, connection):
    "listen for the 'after_begin' event"

    # ... (event handling logic) ...
```

Note

This event is called within the process of the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) modifying its own internal state.
To invoke SQL operations within this hook, use the
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) provided to the event;
do not run SQL operations using the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
directly.

   Parameters:

- **session** – The target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
- **transaction** – The [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction).
- **connection** – The [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object
  which will be used for SQL statements.

See also

[SessionEvents.before_commit()](#sqlalchemy.orm.SessionEvents.before_commit)

[SessionEvents.after_commit()](#sqlalchemy.orm.SessionEvents.after_commit)

[SessionEvents.after_transaction_create()](#sqlalchemy.orm.SessionEvents.after_transaction_create)

[SessionEvents.after_transaction_end()](#sqlalchemy.orm.SessionEvents.after_transaction_end)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_bulk_delete(*delete_context:_O*) → None

Event for after the legacy [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete) method
has been called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_bulk_delete')
def receive_after_bulk_delete(delete_context):
    "listen for the 'after_bulk_delete' event"

    # ... (event handling logic) ...

# DEPRECATED calling style (pre-0.9, will be removed in a future release)
@event.listens_for(SomeSessionClassOrObject, 'after_bulk_delete')
def receive_after_bulk_delete(session, query, query_context, result):
    "listen for the 'after_bulk_delete' event"

    # ... (event handling logic) ...
```

Changed in version 0.9: The [SessionEvents.after_bulk_delete()](#sqlalchemy.orm.SessionEvents.after_bulk_delete) event now accepts the
arguments [SessionEvents.after_bulk_delete.delete_context](#sqlalchemy.orm.SessionEvents.after_bulk_delete.params.delete_context).
Support for listener functions which accept the previous
argument signature(s) listed above as “deprecated” will be
removed in a future release.

Legacy Feature

The [SessionEvents.after_bulk_delete()](#sqlalchemy.orm.SessionEvents.after_bulk_delete) method
is a legacy event hook as of SQLAlchemy 2.0.   The event
**does not participate** in [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) invocations
using [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) documented at
[ORM UPDATE and DELETE with Custom WHERE Criteria](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-update-delete-where).  For 2.0 style use,
the [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) hook will intercept
these calls.

   Parameters:

**delete_context** –

a “delete context” object which contains
details about the update, including these attributes:

> - `session` - the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) involved
> - `query` -the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
>   object that this update operation
>   was called upon.
> - `result` the [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult)
>   returned as a result of the
>   bulk DELETE operation.

Changed in version 1.4: the update_context no longer has a
`QueryContext` object associated with it.

See also

[QueryEvents.before_compile_delete()](#sqlalchemy.orm.QueryEvents.before_compile_delete)

[SessionEvents.after_bulk_update()](#sqlalchemy.orm.SessionEvents.after_bulk_update)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_bulk_update(*update_context:_O*) → None

Event for after the legacy [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) method
has been called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_bulk_update')
def receive_after_bulk_update(update_context):
    "listen for the 'after_bulk_update' event"

    # ... (event handling logic) ...

# DEPRECATED calling style (pre-0.9, will be removed in a future release)
@event.listens_for(SomeSessionClassOrObject, 'after_bulk_update')
def receive_after_bulk_update(session, query, query_context, result):
    "listen for the 'after_bulk_update' event"

    # ... (event handling logic) ...
```

Changed in version 0.9: The [SessionEvents.after_bulk_update()](#sqlalchemy.orm.SessionEvents.after_bulk_update) event now accepts the
arguments [SessionEvents.after_bulk_update.update_context](#sqlalchemy.orm.SessionEvents.after_bulk_update.params.update_context).
Support for listener functions which accept the previous
argument signature(s) listed above as “deprecated” will be
removed in a future release.

Legacy Feature

The [SessionEvents.after_bulk_update()](#sqlalchemy.orm.SessionEvents.after_bulk_update) method
is a legacy event hook as of SQLAlchemy 2.0.   The event
**does not participate** in [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) invocations
using [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) documented at
[ORM UPDATE and DELETE with Custom WHERE Criteria](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-update-delete-where).  For 2.0 style use,
the [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) hook will intercept
these calls.

   Parameters:

**update_context** –

an “update context” object which contains
details about the update, including these attributes:

> - `session` - the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) involved
> - `query` -the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
>   object that this update operation
>   was called upon.
> - `values` The “values” dictionary that was passed to
>   [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update).
> - `result` the [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult)
>   returned as a result of the
>   bulk UPDATE operation.

Changed in version 1.4: the update_context no longer has a
`QueryContext` object associated with it.

See also

[QueryEvents.before_compile_update()](#sqlalchemy.orm.QueryEvents.before_compile_update)

[SessionEvents.after_bulk_delete()](#sqlalchemy.orm.SessionEvents.after_bulk_delete)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_commit(*session:Session*) → None

Execute after a commit has occurred.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_commit')
def receive_after_commit(session):
    "listen for the 'after_commit' event"

    # ... (event handling logic) ...
```

Note

The [SessionEvents.after_commit()](#sqlalchemy.orm.SessionEvents.after_commit) hook is *not* per-flush,
that is, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) can emit SQL to the database
many times within the scope of a transaction.
For interception of these events, use the
[SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush),
[SessionEvents.after_flush()](#sqlalchemy.orm.SessionEvents.after_flush), or
[SessionEvents.after_flush_postexec()](#sqlalchemy.orm.SessionEvents.after_flush_postexec)
events.

Note

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is not in an active transaction
when the [SessionEvents.after_commit()](#sqlalchemy.orm.SessionEvents.after_commit) event is invoked,
and therefore can not emit SQL.  To emit SQL corresponding to
every transaction, use the [SessionEvents.before_commit()](#sqlalchemy.orm.SessionEvents.before_commit)
event.

   Parameters:

**session** – The target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

See also

[SessionEvents.before_commit()](#sqlalchemy.orm.SessionEvents.before_commit)

[SessionEvents.after_begin()](#sqlalchemy.orm.SessionEvents.after_begin)

[SessionEvents.after_transaction_create()](#sqlalchemy.orm.SessionEvents.after_transaction_create)

[SessionEvents.after_transaction_end()](#sqlalchemy.orm.SessionEvents.after_transaction_end)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_flush(*session:Session*, *flush_context:UOWTransaction*) → None

Execute after flush has completed, but before commit has been
called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_flush')
def receive_after_flush(session, flush_context):
    "listen for the 'after_flush' event"

    # ... (event handling logic) ...
```

Note that the session’s state is still in pre-flush, i.e. ‘new’,
‘dirty’, and ‘deleted’ lists still show pre-flush state as well
as the history settings on instance attributes.

Warning

This event runs after the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has emitted
SQL to modify the database, but **before** it has altered its
internal state to reflect those changes, including that newly
inserted objects are placed into the identity map.  ORM operations
emitted within this event such as loads of related items
may produce new identity map entries that will immediately
be replaced, sometimes causing confusing results.  SQLAlchemy will
emit a warning for this condition as of version 1.3.9.

   Parameters:

- **session** – The target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
- **flush_context** – Internal [UOWTransaction](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.UOWTransaction) object
  which handles the details of the flush.

See also

[SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush)

[SessionEvents.after_flush_postexec()](#sqlalchemy.orm.SessionEvents.after_flush_postexec)

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_flush_postexec(*session:Session*, *flush_context:UOWTransaction*) → None

Execute after flush has completed, and after the post-exec
state occurs.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_flush_postexec')
def receive_after_flush_postexec(session, flush_context):
    "listen for the 'after_flush_postexec' event"

    # ... (event handling logic) ...
```

This will be when the ‘new’, ‘dirty’, and ‘deleted’ lists are in
their final state.  An actual commit() may or may not have
occurred, depending on whether or not the flush started its own
transaction or participated in a larger transaction.

  Parameters:

- **session** – The target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
- **flush_context** – Internal [UOWTransaction](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.UOWTransaction) object
  which handles the details of the flush.

See also

[SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush)

[SessionEvents.after_flush()](#sqlalchemy.orm.SessionEvents.after_flush)

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_rollback(*session:Session*) → None

Execute after a real DBAPI rollback has occurred.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_rollback')
def receive_after_rollback(session):
    "listen for the 'after_rollback' event"

    # ... (event handling logic) ...
```

Note that this event only fires when the *actual* rollback against
the database occurs - it does *not* fire each time the
[Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) method is called, if the underlying
DBAPI transaction has already been rolled back.  In many
cases, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will not be in
an “active” state during this event, as the current
transaction is not valid.   To acquire a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
which is active after the outermost rollback has proceeded,
use the [SessionEvents.after_soft_rollback()](#sqlalchemy.orm.SessionEvents.after_soft_rollback) event, checking the
[Session.is_active](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.is_active) flag.

  Parameters:

**session** – The target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

      method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_soft_rollback(*session:Session*, *previous_transaction:SessionTransaction*) → None

Execute after any rollback has occurred, including “soft”
rollbacks that don’t actually emit at the DBAPI level.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_soft_rollback')
def receive_after_soft_rollback(session, previous_transaction):
    "listen for the 'after_soft_rollback' event"

    # ... (event handling logic) ...
```

This corresponds to both nested and outer rollbacks, i.e.
the innermost rollback that calls the DBAPI’s
rollback() method, as well as the enclosing rollback
calls that only pop themselves from the transaction stack.

The given [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) can be used to invoke SQL and
[Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query) operations after an outermost rollback
by first checking the [Session.is_active](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.is_active) flag:

```
@event.listens_for(Session, "after_soft_rollback")
def do_something(session, previous_transaction):
    if session.is_active:
        session.execute(text("select * from some_table"))
```

   Parameters:

- **session** – The target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
- **previous_transaction** – The [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)
  transactional marker object which was just closed.   The current
  [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) for the given [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is
  available via the `Session.transaction` attribute.

      method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_transaction_create(*session:Session*, *transaction:SessionTransaction*) → None

Execute when a new [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) is created.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_transaction_create')
def receive_after_transaction_create(session, transaction):
    "listen for the 'after_transaction_create' event"

    # ... (event handling logic) ...
```

This event differs from [SessionEvents.after_begin()](#sqlalchemy.orm.SessionEvents.after_begin)
in that it occurs for each [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)
overall, as opposed to when transactions are begun
on individual database connections.  It is also invoked
for nested transactions and subtransactions, and is always
matched by a corresponding
[SessionEvents.after_transaction_end()](#sqlalchemy.orm.SessionEvents.after_transaction_end) event
(assuming normal operation of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)).

  Parameters:

- **session** – the target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
- **transaction** –
  the target [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction).
  To detect if this is the outermost
  [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction), as opposed to a “subtransaction” or a
  SAVEPOINT, test that the [SessionTransaction.parent](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction.parent) attribute
  is `None`:
  ```
  @event.listens_for(session, "after_transaction_create")
  def after_transaction_create(session, transaction):
      if transaction.parent is None:
          ...  # work with top-level transaction
  ```
  To detect if the [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) is a SAVEPOINT, use the
  [SessionTransaction.nested](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction.nested) attribute:
  ```
  @event.listens_for(session, "after_transaction_create")
  def after_transaction_create(session, transaction):
      if transaction.nested:
          ...  # work with SAVEPOINT transaction
  ```

See also

[SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)

[SessionEvents.after_transaction_end()](#sqlalchemy.orm.SessionEvents.after_transaction_end)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)after_transaction_end(*session:Session*, *transaction:SessionTransaction*) → None

Execute when the span of a [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) ends.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'after_transaction_end')
def receive_after_transaction_end(session, transaction):
    "listen for the 'after_transaction_end' event"

    # ... (event handling logic) ...
```

This event differs from [SessionEvents.after_commit()](#sqlalchemy.orm.SessionEvents.after_commit)
in that it corresponds to all [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)
objects in use, including those for nested transactions
and subtransactions, and is always matched by a corresponding
[SessionEvents.after_transaction_create()](#sqlalchemy.orm.SessionEvents.after_transaction_create) event.

  Parameters:

- **session** – the target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
- **transaction** –
  the target [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction).
  To detect if this is the outermost
  [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction), as opposed to a “subtransaction” or a
  SAVEPOINT, test that the [SessionTransaction.parent](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction.parent) attribute
  is `None`:
  ```
  @event.listens_for(session, "after_transaction_create")
  def after_transaction_end(session, transaction):
      if transaction.parent is None:
          ...  # work with top-level transaction
  ```
  To detect if the [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) is a SAVEPOINT, use the
  [SessionTransaction.nested](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction.nested) attribute:
  ```
  @event.listens_for(session, "after_transaction_create")
  def after_transaction_end(session, transaction):
      if transaction.nested:
          ...  # work with SAVEPOINT transaction
  ```

See also

[SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)

[SessionEvents.after_transaction_create()](#sqlalchemy.orm.SessionEvents.after_transaction_create)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)before_attach(*session:Session*, *instance:_O*) → None

Execute before an instance is attached to a session.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'before_attach')
def receive_before_attach(session, instance):
    "listen for the 'before_attach' event"

    # ... (event handling logic) ...
```

This is called before an add, delete or merge causes
the object to be part of the session.

See also

[SessionEvents.after_attach()](#sqlalchemy.orm.SessionEvents.after_attach)

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)before_commit(*session:Session*) → None

Execute before commit is called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'before_commit')
def receive_before_commit(session):
    "listen for the 'before_commit' event"

    # ... (event handling logic) ...
```

Note

The [SessionEvents.before_commit()](#sqlalchemy.orm.SessionEvents.before_commit) hook is *not* per-flush,
that is, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) can emit SQL to the database
many times within the scope of a transaction.
For interception of these events, use the
[SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush),
[SessionEvents.after_flush()](#sqlalchemy.orm.SessionEvents.after_flush), or
[SessionEvents.after_flush_postexec()](#sqlalchemy.orm.SessionEvents.after_flush_postexec)
events.

   Parameters:

**session** – The target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

See also

[SessionEvents.after_commit()](#sqlalchemy.orm.SessionEvents.after_commit)

[SessionEvents.after_begin()](#sqlalchemy.orm.SessionEvents.after_begin)

[SessionEvents.after_transaction_create()](#sqlalchemy.orm.SessionEvents.after_transaction_create)

[SessionEvents.after_transaction_end()](#sqlalchemy.orm.SessionEvents.after_transaction_end)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)before_flush(*session:Session*, *flush_context:UOWTransaction*, *instances:Sequence[_O]|None*) → None

Execute before flush process has started.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'before_flush')
def receive_before_flush(session, flush_context, instances):
    "listen for the 'before_flush' event"

    # ... (event handling logic) ...
```

    Parameters:

- **session** – The target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
- **flush_context** – Internal [UOWTransaction](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.UOWTransaction) object
  which handles the details of the flush.
- **instances** – Usually `None`, this is the collection of
  objects which can be passed to the [Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush) method
  (note this usage is deprecated).

See also

[SessionEvents.after_flush()](#sqlalchemy.orm.SessionEvents.after_flush)

[SessionEvents.after_flush_postexec()](#sqlalchemy.orm.SessionEvents.after_flush_postexec)

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)deleted_to_detached(*session:Session*, *instance:_O*) → None

Intercept the “deleted to detached” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'deleted_to_detached')
def receive_deleted_to_detached(session, instance):
    "listen for the 'deleted_to_detached' event"

    # ... (event handling logic) ...
```

This event is invoked when a deleted object is evicted
from the session.   The typical case when this occurs is when
the transaction for a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) in which the object
was deleted is committed; the object moves from the deleted
state to the detached state.

It is also invoked for objects that were deleted in a flush
when the [Session.expunge_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expunge_all) or [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close)
events are called, as well as if the object is individually
expunged from its deleted state via [Session.expunge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expunge).

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)deleted_to_persistent(*session:Session*, *instance:_O*) → None

Intercept the “deleted to persistent” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'deleted_to_persistent')
def receive_deleted_to_persistent(session, instance):
    "listen for the 'deleted_to_persistent' event"

    # ... (event handling logic) ...
```

This transition occurs only when an object that’s been deleted
successfully in a flush is restored due to a call to
[Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback).   The event is not called under
any other circumstances.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)detached_to_persistent(*session:Session*, *instance:_O*) → None

Intercept the “detached to persistent” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'detached_to_persistent')
def receive_detached_to_persistent(session, instance):
    "listen for the 'detached_to_persistent' event"

    # ... (event handling logic) ...
```

This event is a specialization of the
[SessionEvents.after_attach()](#sqlalchemy.orm.SessionEvents.after_attach) event which is only invoked
for this specific transition.  It is invoked typically during the
[Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) call, as well as during the
[Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) call if the object was not previously
associated with the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) (note that an object marked as “deleted” remains
in the “persistent” state until the flush proceeds).

Note

If the object becomes persistent as part of a call to
[Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete), the object is **not** yet marked as
deleted when this event is called.  To detect deleted objects,
check the `deleted` flag sent to the
[SessionEvents.persistent_to_detached()](#sqlalchemy.orm.SessionEvents.persistent_to_detached) to event after the
flush proceeds, or check the [Session.deleted](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.deleted) collection
within the [SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush) event if deleted
objects need to be intercepted before the flush.

   Parameters:

- **session** – target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
- **instance** – the ORM-mapped instance being operated upon.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     attribute [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.SessionEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

    method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)do_orm_execute(*orm_execute_state:ORMExecuteState*) → None

Intercept statement executions that occur on behalf of an
ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'do_orm_execute')
def receive_do_orm_execute(orm_execute_state):
    "listen for the 'do_orm_execute' event"

    # ... (event handling logic) ...
```

This event is invoked for all top-level SQL statements invoked from the
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method, as well as related methods such as
[Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars) and [Session.scalar()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalar). As of
SQLAlchemy 1.4, all ORM queries that run through the
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method as well as related methods
[Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars), [Session.scalar()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalar) etc.
will participate in this event.
This event hook does **not** apply to the queries that are
emitted internally within the ORM flush process, i.e. the
process described at [Flushing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing).

Note

The [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) event hook
is triggered **for ORM statement executions only**, meaning those
invoked via the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) and similar methods on
the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object. It does **not** trigger for
statements that are invoked by SQLAlchemy Core only, i.e. statements
invoked directly using [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) or
otherwise originating from an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object without
any [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) involved. To intercept **all** SQL
executions regardless of whether the Core or ORM APIs are in use,
see the event hooks at [ConnectionEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents), such as
[ConnectionEvents.before_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_execute) and
[ConnectionEvents.before_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute).

Also, this event hook does **not** apply to queries that are
emitted internally within the ORM flush process,
i.e. the process described at [Flushing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing); to
intercept steps within the flush process, see the event
hooks described at [Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events) as
well as [Mapper-level Flush Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-mapper).

This event is a `do_` event, meaning it has the capability to replace
the operation that the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method normally
performs.  The intended use for this includes sharding and
result-caching schemes which may seek to invoke the same statement
across  multiple database connections, returning a result that is
merged from each of them, or which don’t invoke the statement at all,
instead returning data from a cache.

The hook intends to replace the use of the
`Query._execute_and_instances` method that could be subclassed prior
to SQLAlchemy 1.4.

  Parameters:

**orm_execute_state** – an instance of [ORMExecuteState](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState)
which contains all information about the current execution, as well
as helper functions used to derive other commonly required
information.   See that object for details.

See also

[Execute Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-execute-events) - top level documentation on how
to use [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute)

[ORMExecuteState](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState) - the object passed to the
[SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) event which contains
all information about the statement to be invoked.  It also
provides an interface to extend the current statement, options,
and parameters as well as an option that allows programmatic
invocation of the statement at any point.

[ORM Query Events](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-session-orm-events) - includes examples of using
[SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute)

[Dogpile Caching](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-caching) - an example of how to integrate
Dogpile caching with the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) making use
of the [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) event hook.

[Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-sharding) - the Horizontal Sharding example /
extension relies upon the
[SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) event hook to invoke a
SQL statement on multiple backends and return a merged result.

Added in version 1.4.

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)loaded_as_persistent(*session:Session*, *instance:_O*) → None

Intercept the “loaded as persistent” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'loaded_as_persistent')
def receive_loaded_as_persistent(session, instance):
    "listen for the 'loaded_as_persistent' event"

    # ... (event handling logic) ...
```

This event is invoked within the ORM loading process, and is invoked
very similarly to the [InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load) event.  However,
the event here is linkable to a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class or instance,
rather than to a mapper or class hierarchy, and integrates
with the other session lifecycle events smoothly.  The object
is guaranteed to be present in the session’s identity map when
this event is called.

Note

This event is invoked within the loader process before
eager loaders may have been completed, and the object’s state may
not be complete.  Additionally, invoking row-level refresh
operations on the object will place the object into a new loader
context, interfering with the existing load context.   See the note
on [InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load) for background on making use of the
[SessionEvents.restore_load_context](#sqlalchemy.orm.SessionEvents.params.restore_load_context) parameter, which
works in the same manner as that of
[InstanceEvents.restore_load_context](#sqlalchemy.orm.InstanceEvents.params.restore_load_context), in  order to
resolve this scenario.

   Parameters:

- **session** – target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
- **instance** – the ORM-mapped instance being operated upon.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)pending_to_persistent(*session:Session*, *instance:_O*) → None

Intercept the “pending to persistent”” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'pending_to_persistent')
def receive_pending_to_persistent(session, instance):
    "listen for the 'pending_to_persistent' event"

    # ... (event handling logic) ...
```

This event is invoked within the flush process, and is
similar to scanning the [Session.new](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.new) collection within
the [SessionEvents.after_flush()](#sqlalchemy.orm.SessionEvents.after_flush) event.  However, in this
case the object has already been moved to the persistent state
when the event is called.

  Parameters:

- **session** – target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
- **instance** – the ORM-mapped instance being operated upon.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)pending_to_transient(*session:Session*, *instance:_O*) → None

Intercept the “pending to transient” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'pending_to_transient')
def receive_pending_to_transient(session, instance):
    "listen for the 'pending_to_transient' event"

    # ... (event handling logic) ...
```

This less common transition occurs when an pending object that has
not been flushed is evicted from the session; this can occur
when the [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) method rolls back the transaction,
or when the [Session.expunge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expunge) method is used.

  Parameters:

- **session** – target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
- **instance** – the ORM-mapped instance being operated upon.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)persistent_to_deleted(*session:Session*, *instance:_O*) → None

Intercept the “persistent to deleted” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'persistent_to_deleted')
def receive_persistent_to_deleted(session, instance):
    "listen for the 'persistent_to_deleted' event"

    # ... (event handling logic) ...
```

This event is invoked when a persistent object’s identity
is deleted from the database within a flush, however the object
still remains associated with the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) until the
transaction completes.

If the transaction is rolled back, the object moves again
to the persistent state, and the
[SessionEvents.deleted_to_persistent()](#sqlalchemy.orm.SessionEvents.deleted_to_persistent) event is called.
If the transaction is committed, the object becomes detached,
which will emit the [SessionEvents.deleted_to_detached()](#sqlalchemy.orm.SessionEvents.deleted_to_detached)
event.

Note that while the [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) method is the primary
public interface to mark an object as deleted, many objects
get deleted due to cascade rules, which are not always determined
until flush time.  Therefore, there’s no way to catch
every object that will be deleted until the flush has proceeded.
the [SessionEvents.persistent_to_deleted()](#sqlalchemy.orm.SessionEvents.persistent_to_deleted) event is therefore
invoked at the end of a flush.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)persistent_to_detached(*session:Session*, *instance:_O*) → None

Intercept the “persistent to detached” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'persistent_to_detached')
def receive_persistent_to_detached(session, instance):
    "listen for the 'persistent_to_detached' event"

    # ... (event handling logic) ...
```

This event is invoked when a persistent object is evicted
from the session.  There are many conditions that cause this
to happen, including:

- using a method such as [Session.expunge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expunge)
  or [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close)
- Calling the [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) method, when the object
  was part of an INSERT statement for that session’s transaction

  Parameters:

- **session** – target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
- **instance** – the ORM-mapped instance being operated upon.
- **deleted** – boolean.  If True, indicates this object moved
  to the detached state because it was marked as deleted and flushed.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)persistent_to_transient(*session:Session*, *instance:_O*) → None

Intercept the “persistent to transient” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'persistent_to_transient')
def receive_persistent_to_transient(session, instance):
    "listen for the 'persistent_to_transient' event"

    # ... (event handling logic) ...
```

This less common transition occurs when an pending object that has
has been flushed is evicted from the session; this can occur
when the [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) method rolls back the transaction.

  Parameters:

- **session** – target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
- **instance** – the ORM-mapped instance being operated upon.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

     method [sqlalchemy.orm.SessionEvents.](#sqlalchemy.orm.SessionEvents)transient_to_pending(*session:Session*, *instance:_O*) → None

Intercept the “transient to pending” transition for a specific
object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeSessionClassOrObject, 'transient_to_pending')
def receive_transient_to_pending(session, instance):
    "listen for the 'transient_to_pending' event"

    # ... (event handling logic) ...
```

This event is a specialization of the
[SessionEvents.after_attach()](#sqlalchemy.orm.SessionEvents.after_attach) event which is only invoked
for this specific transition.  It is invoked typically during the
[Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) call.

  Parameters:

- **session** – target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
- **instance** – the ORM-mapped instance being operated upon.

See also

[Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events)

## Mapper Events

Mapper event hooks encompass things that happen as related to individual
or multiple [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects, which are the central configurational
object that maps a user-defined class to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.
Types of things which occur at the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) level include:

- **Per-object persistence operations** - the most popular mapper hooks are the
  unit-of-work hooks such as [MapperEvents.before_insert()](#sqlalchemy.orm.MapperEvents.before_insert),
  [MapperEvents.after_update()](#sqlalchemy.orm.MapperEvents.after_update), etc.  These events are contrasted to
  the more coarse grained session-level events such as
  [SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush) in that they occur within the flush
  process on a per-object basis; while finer grained activity on an object is
  more straightforward, availability of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) features is
  limited.
- **Mapper configuration events** - the other major class of mapper hooks are
  those which occur as a class is mapped, as a mapper is finalized, and when
  sets of mappers are configured to refer to each other.  These events include
  [MapperEvents.instrument_class()](#sqlalchemy.orm.MapperEvents.instrument_class),
  [MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured) and
  [MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured) at the individual
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) level, and  [MapperEvents.before_configured()](#sqlalchemy.orm.MapperEvents.before_configured)
  and [MapperEvents.after_configured()](#sqlalchemy.orm.MapperEvents.after_configured) at the level of collections of
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects.

| Object Name | Description |
| --- | --- |
| MapperEvents | Define events specific to mappings. |

   class sqlalchemy.orm.MapperEvents

*inherits from* `sqlalchemy.event.Events`

Define events specific to mappings.

e.g.:

```
from sqlalchemy import event

def my_before_insert_listener(mapper, connection, target):
    # execute a stored procedure upon INSERT,
    # apply the value to the row to be inserted
    target.calculated_value = connection.execute(
        text("select my_special_function(%d)" % target.special_number)
    ).scalar()

# associate the listener function with SomeClass,
# to execute during the "before_insert" hook
event.listen(SomeClass, "before_insert", my_before_insert_listener)
```

Available targets include:

- mapped classes
- unmapped superclasses of mapped or to-be-mapped classes
  (using the `propagate=True` flag)
- [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects
- the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class itself indicates listening for all
  mappers.

Mapper events provide hooks into critical sections of the
mapper, including those related to object instrumentation,
object loading, and object persistence. In particular, the
persistence methods [MapperEvents.before_insert()](#sqlalchemy.orm.MapperEvents.before_insert),
and [MapperEvents.before_update()](#sqlalchemy.orm.MapperEvents.before_update) are popular
places to augment the state being persisted - however, these
methods operate with several significant restrictions. The
user is encouraged to evaluate the
[SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush) and
[SessionEvents.after_flush()](#sqlalchemy.orm.SessionEvents.after_flush) methods as more
flexible and user-friendly hooks in which to apply
additional database state during a flush.

When using [MapperEvents](#sqlalchemy.orm.MapperEvents), several modifiers are
available to the [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) function.

  Parameters:

- **propagate=False** – When True, the event listener should
  be applied to all inheriting mappers and/or the mappers of
  inheriting classes, as well as any
  mapper which is the target of this listener.
- **raw=False** – When True, the “target” argument passed
  to applicable event listener functions will be the
  instance’s [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) management
  object, rather than the mapped instance itself.
- **retval=False** –
  when True, the user-defined event function
  must have a return value, the purpose of which is either to
  control subsequent event propagation, or to otherwise alter
  the operation in progress by the mapper.   Possible return
  values are:
  - `sqlalchemy.orm.interfaces.EXT_CONTINUE` - continue event
    processing normally.
  - `sqlalchemy.orm.interfaces.EXT_STOP` - cancel all subsequent
    event handlers in the chain.
  - other values - the return value specified by specific listeners.

| Member Name | Description |
| --- | --- |
| after_configured() | Called after a series of mappers have been configured. |
| after_delete() | Receive an object instance after a DELETE statement
has been emitted corresponding to that instance. |
| after_insert() | Receive an object instance after an INSERT statement
is emitted corresponding to that instance. |
| after_mapper_constructed() | Receive a class and mapper when theMapperhas been
fully constructed. |
| after_update() | Receive an object instance after an UPDATE statement
is emitted corresponding to that instance. |
| before_configured() | Called before a series of mappers have been configured. |
| before_delete() | Receive an object instance before a DELETE statement
is emitted corresponding to that instance. |
| before_insert() | Receive an object instance before an INSERT statement
is emitted corresponding to that instance. |
| before_mapper_configured() | Called right before a specific mapper is to be configured. |
| before_update() | Receive an object instance before an UPDATE statement
is emitted corresponding to that instance. |
| dispatch | reference back to the _Dispatch class. |
| instrument_class() | Receive a class when the mapper is first constructed,
before instrumentation is applied to the mapped class. |
| mapper_configured() | Called when a specific mapper has completed its own configuration
within the scope of theconfigure_mappers()call. |

   method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)after_configured() → None

Called after a series of mappers have been configured.

The [MapperEvents.after_configured()](#sqlalchemy.orm.MapperEvents.after_configured) event is invoked
each time the [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) function is
invoked, after the function has completed its work.
[configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) is typically invoked
automatically as mappings are first used, as well as each time
new mappers have been made available and new mapper use is
detected.

Similar events to this one include
[MapperEvents.before_configured()](#sqlalchemy.orm.MapperEvents.before_configured), which is invoked before a
series of mappers are configured, as well as
[MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured) and
[MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured), which are both invoked on a
per-mapper basis.

This event can **only** be applied to the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class,
and not to individual mappings or mapped classes:

```
from sqlalchemy.orm import Mapper

@event.listens_for(Mapper, "after_configured")
def go(): ...
```

Typically, this event is called once per application, but in practice
may be called more than once, any time new mappers are to be affected
by a [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) call.   If new mappings are
constructed after existing ones have already been used, this event will
likely be called again.

See also

[MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured)

[MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured)

[MapperEvents.before_configured()](#sqlalchemy.orm.MapperEvents.before_configured)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)after_delete(*mapper:Mapper[_O]*, *connection:Connection*, *target:_O*) → None

Receive an object instance after a DELETE statement
has been emitted corresponding to that instance.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'after_delete')
def receive_after_delete(mapper, connection, target):
    "listen for the 'after_delete' event"

    # ... (event handling logic) ...
```

Note

this event **only** applies to the
[session flush operation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)
and does **not** apply to the ORM DML operations described at
[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete).  To intercept ORM
DML events, use [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute).

This event is used to emit additional SQL statements on
the given connection as well as to perform application
specific bookkeeping related to a deletion event.

The event is often called for a batch of objects of the
same class after their DELETE statements have been emitted at
once in a previous step.

Warning

Mapper-level flush events only allow **very limited operations**,
on attributes local to the row being operated upon only,
as well as allowing any SQL to be emitted on the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  **Please read fully** the notes
at [Mapper-level Flush Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-mapper) for guidelines on using
these methods; generally, the [SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush)
method should be preferred for general on-flush changes.

   Parameters:

- **mapper** – the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) which is the target
  of this event.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) being used to
  emit DELETE statements for this instance.  This
  provides a handle into the current transaction on the
  target database specific to this instance.
- **target** – the mapped instance being deleted.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.

  Returns:

No return value is supported by this event.

See also

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)after_insert(*mapper:Mapper[_O]*, *connection:Connection*, *target:_O*) → None

Receive an object instance after an INSERT statement
is emitted corresponding to that instance.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'after_insert')
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"

    # ... (event handling logic) ...
```

Note

this event **only** applies to the
[session flush operation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)
and does **not** apply to the ORM DML operations described at
[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete).  To intercept ORM
DML events, use [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute).

This event is used to modify in-Python-only
state on the instance after an INSERT occurs, as well
as to emit additional SQL statements on the given
connection.

The event is often called for a batch of objects of the
same class after their INSERT statements have been
emitted at once in a previous step. In the extremely
rare case that this is not desirable, the
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object can be configured with `batch=False`,
which will cause batches of instances to be broken up
into individual (and more poorly performing)
event->persist->event steps.

Warning

Mapper-level flush events only allow **very limited operations**,
on attributes local to the row being operated upon only,
as well as allowing any SQL to be emitted on the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  **Please read fully** the notes
at [Mapper-level Flush Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-mapper) for guidelines on using
these methods; generally, the [SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush)
method should be preferred for general on-flush changes.

   Parameters:

- **mapper** – the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) which is the target
  of this event.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) being used to
  emit INSERT statements for this instance.  This
  provides a handle into the current transaction on the
  target database specific to this instance.
- **target** – the mapped instance being persisted.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.

  Returns:

No return value is supported by this event.

See also

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)after_mapper_constructed(*mapper:Mapper[_O]*, *class_:Type[_O]*) → None

Receive a class and mapper when the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) has been
fully constructed.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'after_mapper_constructed')
def receive_after_mapper_constructed(mapper, class_):
    "listen for the 'after_mapper_constructed' event"

    # ... (event handling logic) ...
```

This event is called after the initial constructor for
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) completes.  This occurs after the
[MapperEvents.instrument_class()](#sqlalchemy.orm.MapperEvents.instrument_class) event and after the
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) has done an initial pass of its arguments
to generate its collection of [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty) objects,
which are accessible via the [Mapper.get_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.get_property)
method and the [Mapper.iterate_properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.iterate_properties) attribute.

This event differs from the
[MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured) event in that it
is invoked within the constructor for [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper), rather
than within the [registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure) process.   Currently,
this event is the only one which is appropriate for handlers that
wish to create additional mapped classes in response to the
construction of this [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper), which will be part of the
same configure step when [registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure) next runs.

Added in version 2.0.2.

See also

[Versioning Objects](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-versioning) - an example which illustrates the use
of the [MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured)
event to create new mappers to record change-audit histories on
objects.

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)after_update(*mapper:Mapper[_O]*, *connection:Connection*, *target:_O*) → None

Receive an object instance after an UPDATE statement
is emitted corresponding to that instance.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'after_update')
def receive_after_update(mapper, connection, target):
    "listen for the 'after_update' event"

    # ... (event handling logic) ...
```

Note

this event **only** applies to the
[session flush operation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)
and does **not** apply to the ORM DML operations described at
[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete).  To intercept ORM
DML events, use [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute).

This event is used to modify in-Python-only
state on the instance after an UPDATE occurs, as well
as to emit additional SQL statements on the given
connection.

This method is called for all instances that are
marked as “dirty”, *even those which have no net changes
to their column-based attributes*, and for which
no UPDATE statement has proceeded. An object is marked
as dirty when any of its column-based attributes have a
“set attribute” operation called or when any of its
collections are modified. If, at update time, no
column-based attributes have any net changes, no UPDATE
statement will be issued. This means that an instance
being sent to [MapperEvents.after_update()](#sqlalchemy.orm.MapperEvents.after_update) is
*not* a guarantee that an UPDATE statement has been
issued.

To detect if the column-based attributes on the object have net
changes, and therefore resulted in an UPDATE statement, use
`object_session(instance).is_modified(instance,
include_collections=False)`.

The event is often called for a batch of objects of the
same class after their UPDATE statements have been emitted at
once in a previous step. In the extremely rare case that
this is not desirable, the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) can be
configured with `batch=False`, which will cause
batches of instances to be broken up into individual
(and more poorly performing) event->persist->event
steps.

Warning

Mapper-level flush events only allow **very limited operations**,
on attributes local to the row being operated upon only,
as well as allowing any SQL to be emitted on the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  **Please read fully** the notes
at [Mapper-level Flush Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-mapper) for guidelines on using
these methods; generally, the [SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush)
method should be preferred for general on-flush changes.

   Parameters:

- **mapper** – the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) which is the target
  of this event.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) being used to
  emit UPDATE statements for this instance.  This
  provides a handle into the current transaction on the
  target database specific to this instance.
- **target** – the mapped instance being persisted.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.

  Returns:

No return value is supported by this event.

See also

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)before_configured() → None

Called before a series of mappers have been configured.

The [MapperEvents.before_configured()](#sqlalchemy.orm.MapperEvents.before_configured) event is invoked
each time the [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) function is
invoked, before the function has done any of its work.
[configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) is typically invoked
automatically as mappings are first used, as well as each time
new mappers have been made available and new mapper use is
detected.

Similar events to this one include
[MapperEvents.after_configured()](#sqlalchemy.orm.MapperEvents.after_configured), which is invoked after a series
of mappers has been configured, as well as
[MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured) and
[MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured), which are both invoked on a
per-mapper basis.

This event can **only** be applied to the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class,
and not to individual mappings or mapped classes:

```
from sqlalchemy.orm import Mapper

@event.listens_for(Mapper, "before_configured")
def go(): ...
```

Typically, this event is called once per application, but in practice
may be called more than once, any time new mappers are to be affected
by a [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) call.   If new mappings are
constructed after existing ones have already been used, this event will
likely be called again.

See also

[MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured)

[MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured)

[MapperEvents.after_configured()](#sqlalchemy.orm.MapperEvents.after_configured)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)before_delete(*mapper:Mapper[_O]*, *connection:Connection*, *target:_O*) → None

Receive an object instance before a DELETE statement
is emitted corresponding to that instance.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'before_delete')
def receive_before_delete(mapper, connection, target):
    "listen for the 'before_delete' event"

    # ... (event handling logic) ...
```

Note

this event **only** applies to the
[session flush operation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)
and does **not** apply to the ORM DML operations described at
[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete).  To intercept ORM
DML events, use [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute).

This event is used to emit additional SQL statements on
the given connection as well as to perform application
specific bookkeeping related to a deletion event.

The event is often called for a batch of objects of the
same class before their DELETE statements are emitted at
once in a later step.

Warning

Mapper-level flush events only allow **very limited operations**,
on attributes local to the row being operated upon only,
as well as allowing any SQL to be emitted on the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  **Please read fully** the notes
at [Mapper-level Flush Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-mapper) for guidelines on using
these methods; generally, the [SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush)
method should be preferred for general on-flush changes.

   Parameters:

- **mapper** – the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) which is the target
  of this event.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) being used to
  emit DELETE statements for this instance.  This
  provides a handle into the current transaction on the
  target database specific to this instance.
- **target** – the mapped instance being deleted.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.

  Returns:

No return value is supported by this event.

See also

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)before_insert(*mapper:Mapper[_O]*, *connection:Connection*, *target:_O*) → None

Receive an object instance before an INSERT statement
is emitted corresponding to that instance.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'before_insert')
def receive_before_insert(mapper, connection, target):
    "listen for the 'before_insert' event"

    # ... (event handling logic) ...
```

Note

this event **only** applies to the
[session flush operation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)
and does **not** apply to the ORM DML operations described at
[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete).  To intercept ORM
DML events, use [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute).

This event is used to modify local, non-object related
attributes on the instance before an INSERT occurs, as well
as to emit additional SQL statements on the given
connection.

The event is often called for a batch of objects of the
same class before their INSERT statements are emitted at
once in a later step. In the extremely rare case that
this is not desirable, the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object can be
configured with `batch=False`, which will cause
batches of instances to be broken up into individual
(and more poorly performing) event->persist->event
steps.

Warning

Mapper-level flush events only allow **very limited operations**,
on attributes local to the row being operated upon only,
as well as allowing any SQL to be emitted on the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  **Please read fully** the notes
at [Mapper-level Flush Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-mapper) for guidelines on using
these methods; generally, the [SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush)
method should be preferred for general on-flush changes.

   Parameters:

- **mapper** – the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) which is the target
  of this event.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) being used to
  emit INSERT statements for this instance.  This
  provides a handle into the current transaction on the
  target database specific to this instance.
- **target** – the mapped instance being persisted.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.

  Returns:

No return value is supported by this event.

See also

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)before_mapper_configured(*mapper:Mapper[_O]*, *class_:Type[_O]*) → None

Called right before a specific mapper is to be configured.

The [MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured) event is invoked
for each mapper that is encountered when the
[configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) function proceeds through the current
list of not-yet-configured mappers.   It is similar to the
[MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured) event, except that it’s invoked
right before the configuration occurs, rather than afterwards.

The [MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured) event includes
the special capability where it can force the configure step for a
specific mapper to be skipped; to use this feature, establish
the event using the `retval=True` parameter and return
the `interfaces.EXT_SKIP` symbol to indicate the mapper
should be left unconfigured:

```
from sqlalchemy import event
from sqlalchemy.orm import EXT_SKIP
from sqlalchemy.orm import DeclarativeBase

class DontConfigureBase(DeclarativeBase):
    pass

@event.listens_for(
    DontConfigureBase,
    "before_mapper_configured",
    # support return values for the event
    retval=True,
    # propagate the listener to all subclasses of
    # DontConfigureBase
    propagate=True,
)
def dont_configure(mapper, cls):
    return EXT_SKIP
```

See also

[MapperEvents.before_configured()](#sqlalchemy.orm.MapperEvents.before_configured)

[MapperEvents.after_configured()](#sqlalchemy.orm.MapperEvents.after_configured)

[MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)before_update(*mapper:Mapper[_O]*, *connection:Connection*, *target:_O*) → None

Receive an object instance before an UPDATE statement
is emitted corresponding to that instance.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'before_update')
def receive_before_update(mapper, connection, target):
    "listen for the 'before_update' event"

    # ... (event handling logic) ...
```

Note

this event **only** applies to the
[session flush operation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)
and does **not** apply to the ORM DML operations described at
[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete).  To intercept ORM
DML events, use [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute).

This event is used to modify local, non-object related
attributes on the instance before an UPDATE occurs, as well
as to emit additional SQL statements on the given
connection.

This method is called for all instances that are
marked as “dirty”, *even those which have no net changes
to their column-based attributes*. An object is marked
as dirty when any of its column-based attributes have a
“set attribute” operation called or when any of its
collections are modified. If, at update time, no
column-based attributes have any net changes, no UPDATE
statement will be issued. This means that an instance
being sent to [MapperEvents.before_update()](#sqlalchemy.orm.MapperEvents.before_update) is
*not* a guarantee that an UPDATE statement will be
issued, although you can affect the outcome here by
modifying attributes so that a net change in value does
exist.

To detect if the column-based attributes on the object have net
changes, and will therefore generate an UPDATE statement, use
`object_session(instance).is_modified(instance,
include_collections=False)`.

The event is often called for a batch of objects of the
same class before their UPDATE statements are emitted at
once in a later step. In the extremely rare case that
this is not desirable, the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) can be
configured with `batch=False`, which will cause
batches of instances to be broken up into individual
(and more poorly performing) event->persist->event
steps.

Warning

Mapper-level flush events only allow **very limited operations**,
on attributes local to the row being operated upon only,
as well as allowing any SQL to be emitted on the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  **Please read fully** the notes
at [Mapper-level Flush Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-mapper) for guidelines on using
these methods; generally, the [SessionEvents.before_flush()](#sqlalchemy.orm.SessionEvents.before_flush)
method should be preferred for general on-flush changes.

   Parameters:

- **mapper** – the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) which is the target
  of this event.
- **connection** – the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) being used to
  emit UPDATE statements for this instance.  This
  provides a handle into the current transaction on the
  target database specific to this instance.
- **target** – the mapped instance being persisted.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.

  Returns:

No return value is supported by this event.

See also

[Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-persistence-events)

     attribute [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.MapperEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

    method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)instrument_class(*mapper:Mapper[_O]*, *class_:Type[_O]*) → None

Receive a class when the mapper is first constructed,
before instrumentation is applied to the mapped class.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'instrument_class')
def receive_instrument_class(mapper, class_):
    "listen for the 'instrument_class' event"

    # ... (event handling logic) ...
```

This event is the earliest phase of mapper construction.
Most attributes of the mapper are not yet initialized.   To
receive an event within initial mapper construction where basic
state is available such as the [Mapper.attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.attrs) collection,
the [MapperEvents.after_mapper_constructed()](#sqlalchemy.orm.MapperEvents.after_mapper_constructed) event may
be a better choice.

This listener can either be applied to the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
class overall, or to any un-mapped class which serves as a base
for classes that will be mapped (using the `propagate=True` flag):

```
Base = declarative_base()

@event.listens_for(Base, "instrument_class", propagate=True)
def on_new_class(mapper, cls_):
    "..."
```

   Parameters:

- **mapper** – the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) which is the target
  of this event.
- **class_** – the mapped class.

See also

[MapperEvents.after_mapper_constructed()](#sqlalchemy.orm.MapperEvents.after_mapper_constructed)

     method [sqlalchemy.orm.MapperEvents.](#sqlalchemy.orm.MapperEvents)mapper_configured(*mapper:Mapper[_O]*, *class_:Type[_O]*) → None

Called when a specific mapper has completed its own configuration
within the scope of the [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) call.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'mapper_configured')
def receive_mapper_configured(mapper, class_):
    "listen for the 'mapper_configured' event"

    # ... (event handling logic) ...
```

The [MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured) event is invoked
for each mapper that is encountered when the
[configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) function proceeds through the current
list of not-yet-configured mappers.
[configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) is typically invoked
automatically as mappings are first used, as well as each time
new mappers have been made available and new mapper use is
detected.

When the event is called, the mapper should be in its final
state, but **not including backrefs** that may be invoked from
other mappers; they might still be pending within the
configuration operation.    Bidirectional relationships that
are instead configured via the
[relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) argument
*will* be fully available, since this style of relationship does not
rely upon other possibly-not-configured mappers to know that they
exist.

For an event that is guaranteed to have **all** mappers ready
to go including backrefs that are defined only on other
mappings, use the [MapperEvents.after_configured()](#sqlalchemy.orm.MapperEvents.after_configured)
event; this event invokes only after all known mappings have been
fully configured.

The [MapperEvents.mapper_configured()](#sqlalchemy.orm.MapperEvents.mapper_configured) event, unlike the
[MapperEvents.before_configured()](#sqlalchemy.orm.MapperEvents.before_configured) or
[MapperEvents.after_configured()](#sqlalchemy.orm.MapperEvents.after_configured) events, is called for each
mapper/class individually, and the mapper is passed to the event
itself.  It also is called exactly once for a particular mapper.  The
event is therefore useful for configurational steps that benefit from
being invoked just once on a specific mapper basis, which don’t require
that “backref” configurations are necessarily ready yet.

  Parameters:

- **mapper** – the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) which is the target
  of this event.
- **class_** – the mapped class.

See also

[MapperEvents.before_configured()](#sqlalchemy.orm.MapperEvents.before_configured)

[MapperEvents.after_configured()](#sqlalchemy.orm.MapperEvents.after_configured)

[MapperEvents.before_mapper_configured()](#sqlalchemy.orm.MapperEvents.before_mapper_configured)

## Instance Events

Instance events are focused on the construction of ORM mapped instances,
including when they are instantiated as [transient](https://docs.sqlalchemy.org/en/20/glossary.html#term-transient) objects,
when they are loaded from the database and become [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent) objects,
as well as when database refresh or expiration operations occur on the object.

| Object Name | Description |
| --- | --- |
| InstanceEvents | Define events specific to object lifecycle. |

   class sqlalchemy.orm.InstanceEvents

*inherits from* `sqlalchemy.event.Events`

Define events specific to object lifecycle.

e.g.:

```
from sqlalchemy import event

def my_load_listener(target, context):
    print("on load!")

event.listen(SomeClass, "load", my_load_listener)
```

Available targets include:

- mapped classes
- unmapped superclasses of mapped or to-be-mapped classes
  (using the `propagate=True` flag)
- [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects
- the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class itself indicates listening for all
  mappers.

Instance events are closely related to mapper events, but
are more specific to the instance and its instrumentation,
rather than its system of persistence.

When using [InstanceEvents](#sqlalchemy.orm.InstanceEvents), several modifiers are
available to the [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) function.

  Parameters:

- **propagate=False** – When True, the event listener should
  be applied to all inheriting classes as well as the
  class which is the target of this listener.
- **raw=False** – When True, the “target” argument passed
  to applicable event listener functions will be the
  instance’s [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) management
  object, rather than the mapped instance itself.
- **restore_load_context=False** –
  Applies to the
  [InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load) and [InstanceEvents.refresh()](#sqlalchemy.orm.InstanceEvents.refresh)
  events.  Restores the loader context of the object when the event
  hook is complete, so that ongoing eager load operations continue
  to target the object appropriately.  A warning is emitted if the
  object is moved to a new loader context from within one of these
  events if this flag is not set.
  Added in version 1.3.14.

| Member Name | Description |
| --- | --- |
| dispatch | reference back to the _Dispatch class. |
| expire() | Receive an object instance after its attributes or some subset
have been expired. |
| first_init() | Called when the first instance of a particular mapping is called. |
| init() | Receive an instance when its constructor is called. |
| init_failure() | Receive an instance when its constructor has been called,
and raised an exception. |
| load() | Receive an object instance after it has been created via__new__, and after initial attribute population has
occurred. |
| pickle() | Receive an object instance when its associated state is
being pickled. |
| refresh() | Receive an object instance after one or more attributes have
been refreshed from a query. |
| refresh_flush() | Receive an object instance after one or more attributes that
contain a column-level default or onupdate handler have been refreshed
during persistence of the object’s state. |
| unpickle() | Receive an object instance after its associated state has
been unpickled. |

   attribute [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.InstanceEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

    method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)expire(*target:_O*, *attrs:Iterable[str]|None*) → None

Receive an object instance after its attributes or some subset
have been expired.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'expire')
def receive_expire(target, attrs):
    "listen for the 'expire' event"

    # ... (event handling logic) ...
```

‘keys’ is a list of attribute names.  If None, the entire
state was expired.

  Parameters:

- **target** – the mapped instance.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.
- **attrs** – sequence of attribute
  names which were expired, or None if all attributes were
  expired.

      method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)first_init(*manager:ClassManager[_O]*, *cls:Type[_O]*) → None

Called when the first instance of a particular mapping is called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'first_init')
def receive_first_init(manager, cls):
    "listen for the 'first_init' event"

    # ... (event handling logic) ...
```

This event is called when the `__init__` method of a class
is called the first time for that particular class.    The event
invokes before `__init__` actually proceeds as well as before
the [InstanceEvents.init()](#sqlalchemy.orm.InstanceEvents.init) event is invoked.

    method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)init(*target:_O*, *args:Any*, *kwargs:Any*) → None

Receive an instance when its constructor is called.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'init')
def receive_init(target, args, kwargs):
    "listen for the 'init' event"

    # ... (event handling logic) ...
```

This method is only called during a userland construction of
an object, in conjunction with the object’s constructor, e.g.
its `__init__` method.  It is not called when an object is
loaded from the database; see the [InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load)
event in order to intercept a database load.

The event is called before the actual `__init__` constructor
of the object is called.  The `kwargs` dictionary may be
modified in-place in order to affect what is passed to
`__init__`.

  Parameters:

- **target** – the mapped instance.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.
- **args** – positional arguments passed to the `__init__` method.
  This is passed as a tuple and is currently immutable.
- **kwargs** – keyword arguments passed to the `__init__` method.
  This structure *can* be altered in place.

See also

[InstanceEvents.init_failure()](#sqlalchemy.orm.InstanceEvents.init_failure)

[InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load)

     method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)init_failure(*target:_O*, *args:Any*, *kwargs:Any*) → None

Receive an instance when its constructor has been called,
and raised an exception.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'init_failure')
def receive_init_failure(target, args, kwargs):
    "listen for the 'init_failure' event"

    # ... (event handling logic) ...
```

This method is only called during a userland construction of
an object, in conjunction with the object’s constructor, e.g.
its `__init__` method. It is not called when an object is loaded
from the database.

The event is invoked after an exception raised by the `__init__`
method is caught.  After the event
is invoked, the original exception is re-raised outwards, so that
the construction of the object still raises an exception.   The
actual exception and stack trace raised should be present in
`sys.exc_info()`.

  Parameters:

- **target** – the mapped instance.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.
- **args** – positional arguments that were passed to the `__init__`
  method.
- **kwargs** – keyword arguments that were passed to the `__init__`
  method.

See also

[InstanceEvents.init()](#sqlalchemy.orm.InstanceEvents.init)

[InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load)

     method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)load(*target:_O*, *context:QueryContext*) → None

Receive an object instance after it has been created via
`__new__`, and after initial attribute population has
occurred.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'load')
def receive_load(target, context):
    "listen for the 'load' event"

    # ... (event handling logic) ...
```

This typically occurs when the instance is created based on
incoming result rows, and is only called once for that
instance’s lifetime.

Warning

During a result-row load, this event is invoked when the
first row received for this instance is processed.  When using
eager loading with collection-oriented attributes, the additional
rows that are to be loaded / processed in order to load subsequent
collection items have not occurred yet.   This has the effect
both that collections will not be fully loaded, as well as that
if an operation occurs within this event handler that emits
another database load operation for the object, the “loading
context” for the object can change and interfere with the
existing eager loaders still in progress.

Examples of what can cause the “loading context” to change within
the event handler include, but are not necessarily limited to:

- accessing deferred attributes that weren’t part of the row,
  will trigger an “undefer” operation and refresh the object
- accessing attributes on a joined-inheritance subclass that
  weren’t part of the row, will trigger a refresh operation.

As of SQLAlchemy 1.3.14, a warning is emitted when this occurs. The
[InstanceEvents.restore_load_context](#sqlalchemy.orm.InstanceEvents.params.restore_load_context) option may  be
used on the event to prevent this warning; this will ensure that
the existing loading context is maintained for the object after the
event is called:

```
@event.listens_for(SomeClass, "load", restore_load_context=True)
def on_load(instance, context):
    instance.some_unloaded_attribute
```

Changed in version 1.3.14: Added
[InstanceEvents.restore_load_context](#sqlalchemy.orm.InstanceEvents.params.restore_load_context)
and [SessionEvents.restore_load_context](#sqlalchemy.orm.SessionEvents.params.restore_load_context) flags which
apply to “on load” events, which will ensure that the loading
context for an object is restored when the event hook is
complete; a warning is emitted if the load context of the object
changes without this flag being set.

The [InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load) event is also available in a
class-method decorator format called [reconstructor()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.reconstructor).

  Parameters:

- **target** – the mapped instance.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.
- **context** – the [QueryContext](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryContext) corresponding to the
  current [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) in progress.  This argument may be
  `None` if the load does not correspond to a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query),
  such as during [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge).

See also

[Maintaining Non-Mapped State Across Loads](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#mapped-class-load-events)

[InstanceEvents.init()](#sqlalchemy.orm.InstanceEvents.init)

[InstanceEvents.refresh()](#sqlalchemy.orm.InstanceEvents.refresh)

[SessionEvents.loaded_as_persistent()](#sqlalchemy.orm.SessionEvents.loaded_as_persistent)

     method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)pickle(*target:_O*, *state_dict:_InstanceDict*) → None

Receive an object instance when its associated state is
being pickled.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'pickle')
def receive_pickle(target, state_dict):
    "listen for the 'pickle' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** – the mapped instance.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.
- **state_dict** – the dictionary returned by
  `__getstate__`, containing the state
  to be pickled.

      method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)refresh(*target:_O*, *context:QueryContext*, *attrs:Iterable[str]|None*) → None

Receive an object instance after one or more attributes have
been refreshed from a query.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'refresh')
def receive_refresh(target, context, attrs):
    "listen for the 'refresh' event"

    # ... (event handling logic) ...
```

Contrast this to the [InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load) method, which
is invoked when the object is first loaded from a query.

Note

This event is invoked within the loader process before
eager loaders may have been completed, and the object’s state may
not be complete.  Additionally, invoking row-level refresh
operations on the object will place the object into a new loader
context, interfering with the existing load context.   See the note
on [InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load) for background on making use of the
[InstanceEvents.restore_load_context](#sqlalchemy.orm.InstanceEvents.params.restore_load_context) parameter, in
order to resolve this scenario.

   Parameters:

- **target** – the mapped instance.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.
- **context** – the [QueryContext](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryContext) corresponding to the
  current [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) in progress.
- **attrs** – sequence of attribute names which
  were populated, or None if all column-mapped, non-deferred
  attributes were populated.

See also

[Maintaining Non-Mapped State Across Loads](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#mapped-class-load-events)

[InstanceEvents.load()](#sqlalchemy.orm.InstanceEvents.load)

     method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)refresh_flush(*target:_O*, *flush_context:UOWTransaction*, *attrs:Iterable[str]|None*) → None

Receive an object instance after one or more attributes that
contain a column-level default or onupdate handler have been refreshed
during persistence of the object’s state.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'refresh_flush')
def receive_refresh_flush(target, flush_context, attrs):
    "listen for the 'refresh_flush' event"

    # ... (event handling logic) ...
```

This event is the same as [InstanceEvents.refresh()](#sqlalchemy.orm.InstanceEvents.refresh) except
it is invoked within the unit of work flush process, and includes
only non-primary-key columns that have column level default or
onupdate handlers, including Python callables as well as server side
defaults and triggers which may be fetched via the RETURNING clause.

Note

While the [InstanceEvents.refresh_flush()](#sqlalchemy.orm.InstanceEvents.refresh_flush) event is triggered
for an object that was INSERTed as well as for an object that was
UPDATEd, the event is geared primarily  towards the UPDATE process;
it is mostly an internal artifact that INSERT actions can also
trigger this event, and note that **primary key columns for an
INSERTed row are explicitly omitted** from this event.  In order to
intercept the newly INSERTed state of an object, the
[SessionEvents.pending_to_persistent()](#sqlalchemy.orm.SessionEvents.pending_to_persistent) and
[MapperEvents.after_insert()](#sqlalchemy.orm.MapperEvents.after_insert) are better choices.

   Parameters:

- **target** – the mapped instance.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.
- **flush_context** – Internal [UOWTransaction](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.UOWTransaction) object
  which handles the details of the flush.
- **attrs** – sequence of attribute names which
  were populated.

See also

[Maintaining Non-Mapped State Across Loads](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#mapped-class-load-events)

[Fetching Server-Generated Defaults](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#orm-server-defaults)

[Column INSERT/UPDATE Defaults](https://docs.sqlalchemy.org/en/20/core/defaults.html)

     method [sqlalchemy.orm.InstanceEvents.](#sqlalchemy.orm.InstanceEvents)unpickle(*target:_O*, *state_dict:_InstanceDict*) → None

Receive an object instance after its associated state has
been unpickled.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass, 'unpickle')
def receive_unpickle(target, state_dict):
    "listen for the 'unpickle' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** – the mapped instance.  If
  the event is configured with `raw=True`, this will
  instead be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) state-management
  object associated with the instance.
- **state_dict** – the dictionary sent to
  `__setstate__`, containing the state
  dictionary which was pickled.

## Attribute Events

Attribute events are triggered as things occur on individual attributes of
ORM mapped objects.  These events form the basis for things like
[custom validation functions](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#simple-validators) as well as
[backref handlers](https://docs.sqlalchemy.org/en/20/orm/backref.html#relationships-backref).

See also

[Changing Attribute Behavior](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html)

| Object Name | Description |
| --- | --- |
| AttributeEvents | Define events for object attributes. |

   class sqlalchemy.orm.AttributeEvents

*inherits from* `sqlalchemy.event.Events`

Define events for object attributes.

These are typically defined on the class-bound descriptor for the
target class.

For example, to register a listener that will receive the
[AttributeEvents.append()](#sqlalchemy.orm.AttributeEvents.append) event:

```
from sqlalchemy import event

@event.listens_for(MyClass.collection, "append", propagate=True)
def my_append_listener(target, value, initiator):
    print("received append event for target: %s" % target)
```

Listeners have the option to return a possibly modified version of the
value, when the [AttributeEvents.retval](#sqlalchemy.orm.AttributeEvents.params.retval) flag is passed to
[listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) or [listens_for()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listens_for), such as below,
illustrated using the [AttributeEvents.set()](#sqlalchemy.orm.AttributeEvents.set) event:

```
def validate_phone(target, value, oldvalue, initiator):
    "Strip non-numeric characters from a phone number"

    return re.sub(r"\D", "", value)

# setup listener on UserContact.phone attribute, instructing
# it to use the return value
listen(UserContact.phone, "set", validate_phone, retval=True)
```

A validation function like the above can also raise an exception
such as `ValueError` to halt the operation.

The [AttributeEvents.propagate](#sqlalchemy.orm.AttributeEvents.params.propagate) flag is also important when
applying listeners to mapped classes that also have mapped subclasses,
as when using mapper inheritance patterns:

```
@event.listens_for(MySuperClass.attr, "set", propagate=True)
def receive_set(target, value, initiator):
    print("value set: %s" % target)
```

The full list of modifiers available to the [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen)
and [listens_for()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listens_for) functions are below.

  Parameters:

- **active_history=False** – When True, indicates that the
  “set” event would like to receive the “old” value being
  replaced unconditionally, even if this requires firing off
  database loads. Note that `active_history` can also be
  set directly via [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) and
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).
- **propagate=False** – When True, the listener function will
  be established not just for the class attribute given, but
  for attributes of the same name on all current subclasses
  of that class, as well as all future subclasses of that
  class, using an additional listener that listens for
  instrumentation events.
- **raw=False** – When True, the “target” argument to the
  event will be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) management
  object, rather than the mapped instance itself.
- **retval=False** – when True, the user-defined event
  listening must return the “value” argument from the
  function.  This gives the listening function the opportunity
  to change the value that is ultimately used for a “set”
  or “append” event.

| Member Name | Description |
| --- | --- |
| append() | Receive a collection append event. |
| append_wo_mutation() | Receive a collection append event where the collection was not
actually mutated. |
| bulk_replace() | Receive a collection ‘bulk replace’ event. |
| dispatch | reference back to the _Dispatch class. |
| dispose_collection() | Receive a ‘collection dispose’ event. |
| init_collection() | Receive a ‘collection init’ event. |
| init_scalar() | Receive a scalar “init” event. |
| modified() | Receive a ‘modified’ event. |
| remove() | Receive a collection remove event. |
| set() | Receive a scalar set event. |

   method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)append(*target:_O*, *value:_T*, *initiator:Event*, ***, *key:EventConstants=EventConstants.NO_KEY*) → _T | None

Receive a collection append event.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'append')
def receive_append(target, value, initiator):
    "listen for the 'append' event"

    # ... (event handling logic) ...
```

The append event is invoked for each element as it is appended
to the collection.  This occurs for single-item appends as well
as for a “bulk replace” operation.

  Parameters:

- **target** – the object instance receiving the event.
  If the listener is registered with `raw=True`, this will
  be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) object.
- **value** – the value being appended.  If this listener
  is registered with `retval=True`, the listener
  function must return this value, or a new value which
  replaces it.
- **initiator** – An instance of `Event`
  representing the initiation of the event.  May be modified
  from its original value by backref handlers in order to control
  chained event propagation, as well as be inspected for information
  about the source of the event.
- **key** –
  When the event is established using the
  [AttributeEvents.include_key](#sqlalchemy.orm.AttributeEvents.params.include_key) parameter set to
  True, this will be the key used in the operation, such as
  `collection[some_key_or_index] = value`.
  The parameter is not passed
  to the event at all if the the
  [AttributeEvents.include_key](#sqlalchemy.orm.AttributeEvents.params.include_key)
  was not used to set up the event; this is to allow backwards
  compatibility with existing event handlers that don’t include the
  `key` parameter.
  Added in version 2.0.

  Returns:

if the event was registered with `retval=True`,
the given value, or a new effective value, should be returned.

See also

[AttributeEvents](#sqlalchemy.orm.AttributeEvents) - background on listener options such
as propagation to subclasses.

[AttributeEvents.bulk_replace()](#sqlalchemy.orm.AttributeEvents.bulk_replace)

     method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)append_wo_mutation(*target:_O*, *value:_T*, *initiator:Event*, ***, *key:EventConstants=EventConstants.NO_KEY*) → None

Receive a collection append event where the collection was not
actually mutated.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'append_wo_mutation')
def receive_append_wo_mutation(target, value, initiator):
    "listen for the 'append_wo_mutation' event"

    # ... (event handling logic) ...
```

This event differs from [AttributeEvents.append()](#sqlalchemy.orm.AttributeEvents.append) in that
it is fired off for de-duplicating collections such as sets and
dictionaries, when the object already exists in the target collection.
The event does not have a return value and the identity of the
given object cannot be changed.

The event is used for cascading objects into a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
when the collection has already been mutated via a backref event.

  Parameters:

- **target** – the object instance receiving the event.
  If the listener is registered with `raw=True`, this will
  be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) object.
- **value** – the value that would be appended if the object did not
  already exist in the collection.
- **initiator** – An instance of `Event`
  representing the initiation of the event.  May be modified
  from its original value by backref handlers in order to control
  chained event propagation, as well as be inspected for information
  about the source of the event.
- **key** –
  When the event is established using the
  [AttributeEvents.include_key](#sqlalchemy.orm.AttributeEvents.params.include_key) parameter set to
  True, this will be the key used in the operation, such as
  `collection[some_key_or_index] = value`.
  The parameter is not passed
  to the event at all if the the
  [AttributeEvents.include_key](#sqlalchemy.orm.AttributeEvents.params.include_key)
  was not used to set up the event; this is to allow backwards
  compatibility with existing event handlers that don’t include the
  `key` parameter.
  Added in version 2.0.

  Returns:

No return value is defined for this event.

Added in version 1.4.15.

     method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)bulk_replace(*target:_O*, *values:Iterable[_T]*, *initiator:Event*, ***, *keys:Iterable[EventConstants]|None=None*) → None

Receive a collection ‘bulk replace’ event.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'bulk_replace')
def receive_bulk_replace(target, values, initiator):
    "listen for the 'bulk_replace' event"

    # ... (event handling logic) ...
```

This event is invoked for a sequence of values as they are incoming
to a bulk collection set operation, which can be
modified in place before the values are treated as ORM objects.
This is an “early hook” that runs before the bulk replace routine
attempts to reconcile which objects are already present in the
collection and which are being removed by the net replace operation.

It is typical that this method be combined with use of the
[AttributeEvents.append()](#sqlalchemy.orm.AttributeEvents.append) event.    When using both of these
events, note that a bulk replace operation will invoke
the [AttributeEvents.append()](#sqlalchemy.orm.AttributeEvents.append) event for all new items,
even after [AttributeEvents.bulk_replace()](#sqlalchemy.orm.AttributeEvents.bulk_replace) has been invoked
for the collection as a whole.  In order to determine if an
[AttributeEvents.append()](#sqlalchemy.orm.AttributeEvents.append) event is part of a bulk replace,
use the symbol `attributes.OP_BULK_REPLACE` to test the
incoming initiator:

```
from sqlalchemy.orm.attributes import OP_BULK_REPLACE

@event.listens_for(SomeObject.collection, "bulk_replace")
def process_collection(target, values, initiator):
    values[:] = [_make_value(value) for value in values]

@event.listens_for(SomeObject.collection, "append", retval=True)
def process_collection(target, value, initiator):
    # make sure bulk_replace didn't already do it
    if initiator is None or initiator.op is not OP_BULK_REPLACE:
        return _make_value(value)
    else:
        return value
```

Added in version 1.2.

   Parameters:

- **target** – the object instance receiving the event.
  If the listener is registered with `raw=True`, this will
  be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) object.
- **value** – a sequence (e.g. a list) of the values being set.  The
  handler can modify this list in place.
- **initiator** – An instance of `Event`
  representing the initiation of the event.
- **keys** –
  When the event is established using the
  [AttributeEvents.include_key](#sqlalchemy.orm.AttributeEvents.params.include_key) parameter set to
  True, this will be the sequence of keys used in the operation,
  typically only for a dictionary update.  The parameter is not passed
  to the event at all if the the
  [AttributeEvents.include_key](#sqlalchemy.orm.AttributeEvents.params.include_key)
  was not used to set up the event; this is to allow backwards
  compatibility with existing event handlers that don’t include the
  `key` parameter.
  Added in version 2.0.

See also

[AttributeEvents](#sqlalchemy.orm.AttributeEvents) - background on listener options such
as propagation to subclasses.

     attribute [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.AttributeEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

    method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)dispose_collection(*target:_O*, *collection:Collection[Any]*, *collection_adapter:CollectionAdapter*) → None

Receive a ‘collection dispose’ event.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'dispose_collection')
def receive_dispose_collection(target, collection, collection_adapter):
    "listen for the 'dispose_collection' event"

    # ... (event handling logic) ...
```

This event is triggered for a collection-based attribute when
a collection is replaced, that is:

```
u1.addresses.append(a1)

u1.addresses = [a2, a3]  # <- old collection is disposed
```

The old collection received will contain its previous contents.

Changed in version 1.2: The collection passed to
[AttributeEvents.dispose_collection()](#sqlalchemy.orm.AttributeEvents.dispose_collection) will now have its
contents before the dispose intact; previously, the collection
would be empty.

See also

[AttributeEvents](#sqlalchemy.orm.AttributeEvents) - background on listener options such
as propagation to subclasses.

     method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)init_collection(*target:_O*, *collection:Type[Collection[Any]]*, *collection_adapter:CollectionAdapter*) → None

Receive a ‘collection init’ event.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'init_collection')
def receive_init_collection(target, collection, collection_adapter):
    "listen for the 'init_collection' event"

    # ... (event handling logic) ...
```

This event is triggered for a collection-based attribute, when
the initial “empty collection” is first generated for a blank
attribute, as well as for when the collection is replaced with
a new one, such as via a set event.

E.g., given that `User.addresses` is a relationship-based
collection, the event is triggered here:

```
u1 = User()
u1.addresses.append(a1)  #  <- new collection
```

and also during replace operations:

```
u1.addresses = [a2, a3]  #  <- new collection
```

   Parameters:

- **target** – the object instance receiving the event.
  If the listener is registered with `raw=True`, this will
  be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) object.
- **collection** – the new collection.  This will always be generated
  from what was specified as
  [relationship.collection_class](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.collection_class), and will always
  be empty.
- **collection_adapter** – the [CollectionAdapter](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.CollectionAdapter) that will
  mediate internal access to the collection.

See also

[AttributeEvents](#sqlalchemy.orm.AttributeEvents) - background on listener options such
as propagation to subclasses.

[AttributeEvents.init_scalar()](#sqlalchemy.orm.AttributeEvents.init_scalar) - “scalar” version of this
event.

     method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)init_scalar(*target:_O*, *value:_T*, *dict_:Dict[Any,Any]*) → None

Receive a scalar “init” event.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'init_scalar')
def receive_init_scalar(target, value, dict_):
    "listen for the 'init_scalar' event"

    # ... (event handling logic) ...
```

This event is invoked when an uninitialized, unpersisted scalar
attribute is accessed, e.g. read:

```
x = my_object.some_attribute
```

The ORM’s default behavior when this occurs for an un-initialized
attribute is to return the value `None`; note this differs from
Python’s usual behavior of raising `AttributeError`.    The
event here can be used to customize what value is actually returned,
with the assumption that the event listener would be mirroring
a default generator that is configured on the Core
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
object as well.

Since a default generator on a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
might also produce
a changing value such as a timestamp, the
[AttributeEvents.init_scalar()](#sqlalchemy.orm.AttributeEvents.init_scalar)
event handler can also be used to **set** the newly returned value, so
that a Core-level default generation function effectively fires off
only once, but at the moment the attribute is accessed on the
non-persisted object.   Normally, no change to the object’s state
is made when an uninitialized attribute is accessed (much older
SQLAlchemy versions did in fact change the object’s state).

If a default generator on a column returned a particular constant,
a handler might be used as follows:

```
SOME_CONSTANT = 3.1415926

class MyClass(Base):
    # ...

    some_attribute = Column(Numeric, default=SOME_CONSTANT)

@event.listens_for(
    MyClass.some_attribute, "init_scalar", retval=True, propagate=True
)
def _init_some_attribute(target, dict_, value):
    dict_["some_attribute"] = SOME_CONSTANT
    return SOME_CONSTANT
```

Above, we initialize the attribute `MyClass.some_attribute` to the
value of `SOME_CONSTANT`.   The above code includes the following
features:

- By setting the value `SOME_CONSTANT` in the given `dict_`,
  we indicate that this value is to be persisted to the database.
  This supersedes the use of `SOME_CONSTANT` in the default generator
  for the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).  The `active_column_defaults.py`
  example given at [Attribute Instrumentation](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-instrumentation) illustrates using
  the same approach for a changing default, e.g. a timestamp
  generator.    In this particular example, it is not strictly
  necessary to do this since `SOME_CONSTANT` would be part of the
  INSERT statement in either case.
- By establishing the `retval=True` flag, the value we return
  from the function will be returned by the attribute getter.
  Without this flag, the event is assumed to be a passive observer
  and the return value of our function is ignored.
- The `propagate=True` flag is significant if the mapped class
  includes inheriting subclasses, which would also make use of this
  event listener.  Without this flag, an inheriting subclass will
  not use our event handler.

In the above example, the attribute set event
[AttributeEvents.set()](#sqlalchemy.orm.AttributeEvents.set) as well as the related validation feature
provided by [validates](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.validates) is **not** invoked when we apply our
value to the given `dict_`.  To have these events to invoke in
response to our newly generated value, apply the value to the given
object as a normal attribute set operation:

```
SOME_CONSTANT = 3.1415926

@event.listens_for(
    MyClass.some_attribute, "init_scalar", retval=True, propagate=True
)
def _init_some_attribute(target, dict_, value):
    # will also fire off attribute set events
    target.some_attribute = SOME_CONSTANT
    return SOME_CONSTANT
```

When multiple listeners are set up, the generation of the value
is “chained” from one listener to the next by passing the value
returned by the previous listener that specifies `retval=True`
as the `value` argument of the next listener.

  Parameters:

- **target** – the object instance receiving the event.
  If the listener is registered with `raw=True`, this will
  be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) object.
- **value** – the value that is to be returned before this event
  listener were invoked.  This value begins as the value `None`,
  however will be the return value of the previous event handler
  function if multiple listeners are present.
- **dict_** – the attribute dictionary of this mapped object.
  This is normally the `__dict__` of the object, but in all cases
  represents the destination that the attribute system uses to get
  at the actual value of this attribute.  Placing the value in this
  dictionary has the effect that the value will be used in the
  INSERT statement generated by the unit of work.

See also

[AttributeEvents.init_collection()](#sqlalchemy.orm.AttributeEvents.init_collection) - collection version
of this event

[AttributeEvents](#sqlalchemy.orm.AttributeEvents) - background on listener options such
as propagation to subclasses.

[Attribute Instrumentation](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-instrumentation) - see the
`active_column_defaults.py` example.

     method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)modified(*target:_O*, *initiator:Event*) → None

Receive a ‘modified’ event.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'modified')
def receive_modified(target, initiator):
    "listen for the 'modified' event"

    # ... (event handling logic) ...
```

This event is triggered when the [flag_modified()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.flag_modified)
function is used to trigger a modify event on an attribute without
any specific value being set.

Added in version 1.2.

   Parameters:

- **target** – the object instance receiving the event.
  If the listener is registered with `raw=True`, this will
  be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) object.
- **initiator** – An instance of `Event`
  representing the initiation of the event.

See also

[AttributeEvents](#sqlalchemy.orm.AttributeEvents) - background on listener options such
as propagation to subclasses.

     method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)remove(*target:_O*, *value:_T*, *initiator:Event*, ***, *key:EventConstants=EventConstants.NO_KEY*) → None

Receive a collection remove event.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'remove')
def receive_remove(target, value, initiator):
    "listen for the 'remove' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** – the object instance receiving the event.
  If the listener is registered with `raw=True`, this will
  be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) object.
- **value** – the value being removed.
- **initiator** – An instance of `Event`
  representing the initiation of the event.  May be modified
  from its original value by backref handlers in order to control
  chained event propagation.
- **key** –
  When the event is established using the
  [AttributeEvents.include_key](#sqlalchemy.orm.AttributeEvents.params.include_key) parameter set to
  True, this will be the key used in the operation, such as
  `del collection[some_key_or_index]`.  The parameter is not passed
  to the event at all if the the
  [AttributeEvents.include_key](#sqlalchemy.orm.AttributeEvents.params.include_key)
  was not used to set up the event; this is to allow backwards
  compatibility with existing event handlers that don’t include the
  `key` parameter.
  Added in version 2.0.

  Returns:

No return value is defined for this event.

See also

[AttributeEvents](#sqlalchemy.orm.AttributeEvents) - background on listener options such
as propagation to subclasses.

     method [sqlalchemy.orm.AttributeEvents.](#sqlalchemy.orm.AttributeEvents)set(*target:_O*, *value:_T*, *oldvalue:_T*, *initiator:Event*) → None

Receive a scalar set event.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeClass.some_attribute, 'set')
def receive_set(target, value, oldvalue, initiator):
    "listen for the 'set' event"

    # ... (event handling logic) ...
```

    Parameters:

- **target** – the object instance receiving the event.
  If the listener is registered with `raw=True`, this will
  be the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) object.
- **value** – the value being set.  If this listener
  is registered with `retval=True`, the listener
  function must return this value, or a new value which
  replaces it.
- **oldvalue** – the previous value being replaced.  This
  may also be the symbol `NEVER_SET` or `NO_VALUE`.
  If the listener is registered with `active_history=True`,
  the previous value of the attribute will be loaded from
  the database if the existing value is currently unloaded
  or expired.
- **initiator** – An instance of `Event`
  representing the initiation of the event.  May be modified
  from its original value by backref handlers in order to control
  chained event propagation.

  Returns:

if the event was registered with `retval=True`,
the given value, or a new effective value, should be returned.

See also

[AttributeEvents](#sqlalchemy.orm.AttributeEvents) - background on listener options such
as propagation to subclasses.

## Query Events

| Object Name | Description |
| --- | --- |
| QueryEvents | Represent events within the construction of aQueryobject. |

   class sqlalchemy.orm.QueryEvents

*inherits from* `sqlalchemy.event.Events`

Represent events within the construction of a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
object.

Legacy Feature

The [QueryEvents](#sqlalchemy.orm.QueryEvents) event methods are legacy
as of SQLAlchemy 2.0, and only apply to direct use of the
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object. They are not used for [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style)
statements. For events to intercept and modify 2.0 style ORM use,
use the [SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) hook.

The [QueryEvents](#sqlalchemy.orm.QueryEvents) hooks are now superseded by the
[SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) event hook.

| Member Name | Description |
| --- | --- |
| before_compile() | Receive theQueryobject before it is composed into a
coreSelectobject. |
| before_compile_delete() | Allow modifications to theQueryobject withinQuery.delete(). |
| before_compile_update() | Allow modifications to theQueryobject withinQuery.update(). |
| dispatch | reference back to the _Dispatch class. |

   method [sqlalchemy.orm.QueryEvents.](#sqlalchemy.orm.QueryEvents)before_compile(*query:Query*) → None

Receive the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
object before it is composed into a
core [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeQuery, 'before_compile')
def receive_before_compile(query):
    "listen for the 'before_compile' event"

    # ... (event handling logic) ...
```

Deprecated since version 1.4: The [QueryEvents.before_compile()](#sqlalchemy.orm.QueryEvents.before_compile) event
is superseded by the much more capable
[SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) hook.   In version 1.4,
the [QueryEvents.before_compile()](#sqlalchemy.orm.QueryEvents.before_compile) event is **no longer
used** for ORM-level attribute loads, such as loads of deferred
or expired attributes as well as relationship loaders.   See the
new examples in [ORM Query Events](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-session-orm-events) which
illustrate new ways of intercepting and modifying ORM queries
for the most common purpose of adding arbitrary filter criteria.

This event is intended to allow changes to the query given:

```
@event.listens_for(Query, "before_compile", retval=True)
def no_deleted(query):
    for desc in query.column_descriptions:
        if desc["type"] is User:
            entity = desc["entity"]
            query = query.filter(entity.deleted == False)
    return query
```

The event should normally be listened with the `retval=True`
parameter set, so that the modified query may be returned.

The [QueryEvents.before_compile()](#sqlalchemy.orm.QueryEvents.before_compile) event by default
will disallow “baked” queries from caching a query, if the event
hook returns a new [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object.
This affects both direct
use of the baked query extension as well as its operation within
lazy loaders and eager loaders for relationships.  In order to
re-establish the query being cached, apply the event adding the
`bake_ok` flag:

```
@event.listens_for(Query, "before_compile", retval=True, bake_ok=True)
def my_event(query):
    for desc in query.column_descriptions:
        if desc["type"] is User:
            entity = desc["entity"]
            query = query.filter(entity.deleted == False)
    return query
```

When `bake_ok` is set to True, the event hook will only be invoked
once, and not called for subsequent invocations of a particular query
that is being cached.

Added in version 1.3.11: - added the “bake_ok” flag to the
[QueryEvents.before_compile()](#sqlalchemy.orm.QueryEvents.before_compile) event and disallowed caching via
the “baked” extension from occurring for event handlers that
return  a new [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object if this flag is not set.

See also

[QueryEvents.before_compile_update()](#sqlalchemy.orm.QueryEvents.before_compile_update)

[QueryEvents.before_compile_delete()](#sqlalchemy.orm.QueryEvents.before_compile_delete)

[Using the before_compile event](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#baked-with-before-compile)

     method [sqlalchemy.orm.QueryEvents.](#sqlalchemy.orm.QueryEvents)before_compile_delete(*query:Query*, *delete_context:BulkDelete*) → None

Allow modifications to the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object within
[Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeQuery, 'before_compile_delete')
def receive_before_compile_delete(query, delete_context):
    "listen for the 'before_compile_delete' event"

    # ... (event handling logic) ...
```

Deprecated since version 1.4: The [QueryEvents.before_compile_delete()](#sqlalchemy.orm.QueryEvents.before_compile_delete)
event is superseded by the much more capable
[SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) hook.

Like the [QueryEvents.before_compile()](#sqlalchemy.orm.QueryEvents.before_compile) event, this event
should be configured with `retval=True`, and the modified
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object returned, as in

```
@event.listens_for(Query, "before_compile_delete", retval=True)
def no_deleted(query, delete_context):
    for desc in query.column_descriptions:
        if desc["type"] is User:
            entity = desc["entity"]
            query = query.filter(entity.deleted == False)
    return query
```

   Parameters:

- **query** – a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) instance; this is also
  the `.query` attribute of the given “delete context”
  object.
- **delete_context** – a “delete context” object which is
  the same kind of object as described in
  `QueryEvents.after_bulk_delete.delete_context`.

Added in version 1.2.17.

See also

[QueryEvents.before_compile()](#sqlalchemy.orm.QueryEvents.before_compile)

[QueryEvents.before_compile_update()](#sqlalchemy.orm.QueryEvents.before_compile_update)

     method [sqlalchemy.orm.QueryEvents.](#sqlalchemy.orm.QueryEvents)before_compile_update(*query:Query*, *update_context:BulkUpdate*) → None

Allow modifications to the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object within
[Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update).

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeQuery, 'before_compile_update')
def receive_before_compile_update(query, update_context):
    "listen for the 'before_compile_update' event"

    # ... (event handling logic) ...
```

Deprecated since version 1.4: The [QueryEvents.before_compile_update()](#sqlalchemy.orm.QueryEvents.before_compile_update)
event is superseded by the much more capable
[SessionEvents.do_orm_execute()](#sqlalchemy.orm.SessionEvents.do_orm_execute) hook.

Like the [QueryEvents.before_compile()](#sqlalchemy.orm.QueryEvents.before_compile) event, if the event
is to be used to alter the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object, it should
be configured with `retval=True`, and the modified
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object returned, as in

```
@event.listens_for(Query, "before_compile_update", retval=True)
def no_deleted(query, update_context):
    for desc in query.column_descriptions:
        if desc["type"] is User:
            entity = desc["entity"]
            query = query.filter(entity.deleted == False)

            update_context.values["timestamp"] = datetime.datetime.now(
                datetime.UTC
            )
    return query
```

The `.values` dictionary of the “update context” object can also
be modified in place as illustrated above.

  Parameters:

- **query** – a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) instance; this is also
  the `.query` attribute of the given “update context”
  object.
- **update_context** – an “update context” object which is
  the same kind of object as described in
  `QueryEvents.after_bulk_update.update_context`.
  The object has a `.values` attribute in an UPDATE context which is
  the dictionary of parameters passed to [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update).
  This
  dictionary can be modified to alter the VALUES clause of the
  resulting UPDATE statement.

Added in version 1.2.17.

See also

[QueryEvents.before_compile()](#sqlalchemy.orm.QueryEvents.before_compile)

[QueryEvents.before_compile_delete()](#sqlalchemy.orm.QueryEvents.before_compile_delete)

     attribute [sqlalchemy.orm.QueryEvents.](#sqlalchemy.orm.QueryEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.QueryEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

## Instrumentation Events

Defines SQLAlchemy’s system of class instrumentation.

This module is usually not directly visible to user applications, but
defines a large part of the ORM’s interactivity.

instrumentation.py deals with registration of end-user classes
for state tracking.   It interacts closely with state.py
and attributes.py which establish per-instance and per-class-attribute
instrumentation, respectively.

The class instrumentation system can be customized on a per-class
or global basis using the [sqlalchemy.ext.instrumentation](https://docs.sqlalchemy.org/en/20/orm/extensions/instrumentation.html#module-sqlalchemy.ext.instrumentation)
module, which provides the means to build and specify
alternate instrumentation forms.

| Object Name | Description |
| --- | --- |
| InstrumentationEvents | Events related to class instrumentation events. |

   class sqlalchemy.orm.InstrumentationEvents

*inherits from* `sqlalchemy.event.Events`

Events related to class instrumentation events.

The listeners here support being established against
any new style class, that is any object that is a subclass
of ‘type’.  Events will then be fired off for events
against that class.  If the “propagate=True” flag is passed
to event.listen(), the event will fire off for subclasses
of that class as well.

The Python `type` builtin is also accepted as a target,
which when used has the effect of events being emitted
for all classes.

Note the “propagate” flag here is defaulted to `True`,
unlike the other class level events where it defaults
to `False`.  This means that new subclasses will also
be the subject of these events, when a listener
is established on a superclass.

| Member Name | Description |
| --- | --- |
| attribute_instrument() | Called when an attribute is instrumented. |
| class_instrument() | Called after the given class is instrumented. |
| class_uninstrument() | Called before the given class is uninstrumented. |
| dispatch | reference back to the _Dispatch class. |

   method [sqlalchemy.orm.InstrumentationEvents.](#sqlalchemy.orm.InstrumentationEvents)attribute_instrument(*cls:ClassManager[_O]*, *key:_KT*, *inst:_O*) → None

Called when an attribute is instrumented.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeBaseClass, 'attribute_instrument')
def receive_attribute_instrument(cls, key, inst):
    "listen for the 'attribute_instrument' event"

    # ... (event handling logic) ...
```

      method [sqlalchemy.orm.InstrumentationEvents.](#sqlalchemy.orm.InstrumentationEvents)class_instrument(*cls:ClassManager[_O]*) → None

Called after the given class is instrumented.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeBaseClass, 'class_instrument')
def receive_class_instrument(cls):
    "listen for the 'class_instrument' event"

    # ... (event handling logic) ...
```

To get at the [ClassManager](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ClassManager), use
`manager_of_class()`.

    method [sqlalchemy.orm.InstrumentationEvents.](#sqlalchemy.orm.InstrumentationEvents)class_uninstrument(*cls:ClassManager[_O]*) → None

Called before the given class is uninstrumented.

Example argument forms:

```
from sqlalchemy import event

@event.listens_for(SomeBaseClass, 'class_uninstrument')
def receive_class_uninstrument(cls):
    "listen for the 'class_uninstrument' event"

    # ... (event handling logic) ...
```

To get at the [ClassManager](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ClassManager), use
`manager_of_class()`.

    attribute [sqlalchemy.orm.InstrumentationEvents.](#sqlalchemy.orm.InstrumentationEvents)dispatch: _Dispatch[_ET] = <sqlalchemy.event.base.InstrumentationEventsDispatch object>

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events
