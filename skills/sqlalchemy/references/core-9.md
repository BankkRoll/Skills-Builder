# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Engine and Connection Use

- [Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html)
  - [Supported Databases](https://docs.sqlalchemy.org/en/20/core/engines.html#supported-databases)
  - [Database URLs](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
    - [Escaping Special Characters such as @ signs in Passwords](https://docs.sqlalchemy.org/en/20/core/engines.html#escaping-special-characters-such-as-signs-in-passwords)
    - [Creating URLs Programmatically](https://docs.sqlalchemy.org/en/20/core/engines.html#creating-urls-programmatically)
    - [Backend-Specific URLs](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls)
  - [Engine Creation API](https://docs.sqlalchemy.org/en/20/core/engines.html#engine-creation-api)
    - [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
    - [engine_from_config()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine_from_config)
    - [create_mock_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_mock_engine)
    - [make_url()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.make_url)
    - [create_pool_from_url()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_pool_from_url)
    - [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL)
  - [Pooling](https://docs.sqlalchemy.org/en/20/core/engines.html#pooling)
  - [Custom DBAPI connect() arguments / on-connect routines](https://docs.sqlalchemy.org/en/20/core/engines.html#custom-dbapi-connect-arguments-on-connect-routines)
    - [Special Keyword Arguments Passed to dbapi.connect()](https://docs.sqlalchemy.org/en/20/core/engines.html#special-keyword-arguments-passed-to-dbapi-connect)
    - [Controlling how parameters are passed to the DBAPI connect() function](https://docs.sqlalchemy.org/en/20/core/engines.html#controlling-how-parameters-are-passed-to-the-dbapi-connect-function)
    - [Modifying the DBAPI connection after connect, or running commands after connect](https://docs.sqlalchemy.org/en/20/core/engines.html#modifying-the-dbapi-connection-after-connect-or-running-commands-after-connect)
    - [Fully Replacing the DBAPIconnect()function](https://docs.sqlalchemy.org/en/20/core/engines.html#fully-replacing-the-dbapi-connect-function)
  - [Configuring Logging](https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging)
    - [More on the Echo Flag](https://docs.sqlalchemy.org/en/20/core/engines.html#more-on-the-echo-flag)
    - [Setting the Logging Name](https://docs.sqlalchemy.org/en/20/core/engines.html#setting-the-logging-name)
    - [Setting Per-Connection / Sub-Engine Tokens](https://docs.sqlalchemy.org/en/20/core/engines.html#setting-per-connection-sub-engine-tokens)
    - [Hiding Parameters](https://docs.sqlalchemy.org/en/20/core/engines.html#hiding-parameters)
- [Working with Engines and Connections](https://docs.sqlalchemy.org/en/20/core/connections.html)
  - [Basic Usage](https://docs.sqlalchemy.org/en/20/core/connections.html#basic-usage)
  - [Using Transactions](https://docs.sqlalchemy.org/en/20/core/connections.html#using-transactions)
    - [Commit As You Go](https://docs.sqlalchemy.org/en/20/core/connections.html#commit-as-you-go)
    - [Begin Once](https://docs.sqlalchemy.org/en/20/core/connections.html#begin-once)
    - [Connect and Begin Once from the Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#connect-and-begin-once-from-the-engine)
    - [Mixing Styles](https://docs.sqlalchemy.org/en/20/core/connections.html#mixing-styles)
  - [Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#setting-transaction-isolation-levels-including-dbapi-autocommit)
    - [Setting Isolation Level or DBAPI Autocommit for a Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#setting-isolation-level-or-dbapi-autocommit-for-a-connection)
    - [Setting Isolation Level or DBAPI Autocommit for an Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#setting-isolation-level-or-dbapi-autocommit-for-an-engine)
    - [Maintaining Multiple Isolation Levels for a Single Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#maintaining-multiple-isolation-levels-for-a-single-engine)
    - [Understanding the DBAPI-Level Autocommit Isolation Level](https://docs.sqlalchemy.org/en/20/core/connections.html#understanding-the-dbapi-level-autocommit-isolation-level)
  - [Using Server Side Cursors (a.k.a. stream results)](https://docs.sqlalchemy.org/en/20/core/connections.html#using-server-side-cursors-a-k-a-stream-results)
    - [Streaming with a fixed buffer via yield_per](https://docs.sqlalchemy.org/en/20/core/connections.html#streaming-with-a-fixed-buffer-via-yield-per)
    - [Streaming with a dynamically growing buffer using stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#streaming-with-a-dynamically-growing-buffer-using-stream-results)
  - [Translation of Schema Names](https://docs.sqlalchemy.org/en/20/core/connections.html#translation-of-schema-names)
  - [SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-compilation-caching)
    - [Configuration](https://docs.sqlalchemy.org/en/20/core/connections.html#configuration)
    - [Estimating Cache Performance Using Logging](https://docs.sqlalchemy.org/en/20/core/connections.html#estimating-cache-performance-using-logging)
    - [How much memory does the cache use?](https://docs.sqlalchemy.org/en/20/core/connections.html#how-much-memory-does-the-cache-use)
    - [Disabling or using an alternate dictionary to cache some (or all) statements](https://docs.sqlalchemy.org/en/20/core/connections.html#disabling-or-using-an-alternate-dictionary-to-cache-some-or-all-statements)
    - [Caching for Third Party Dialects](https://docs.sqlalchemy.org/en/20/core/connections.html#caching-for-third-party-dialects)
    - [Using Lambdas to add significant speed gains to statement production](https://docs.sqlalchemy.org/en/20/core/connections.html#using-lambdas-to-add-significant-speed-gains-to-statement-production)
  - [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#insert-many-values-behavior-for-insert-statements)
    - [Current Support](https://docs.sqlalchemy.org/en/20/core/connections.html#current-support)
    - [Disabling the feature](https://docs.sqlalchemy.org/en/20/core/connections.html#disabling-the-feature)
    - [Batched Mode Operation](https://docs.sqlalchemy.org/en/20/core/connections.html#batched-mode-operation)
    - [Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#correlating-returning-rows-to-parameter-sets)
    - [Non-Batched Mode Operation](https://docs.sqlalchemy.org/en/20/core/connections.html#non-batched-mode-operation)
    - [Statement Execution Model](https://docs.sqlalchemy.org/en/20/core/connections.html#statement-execution-model)
    - [Controlling the Batch Size](https://docs.sqlalchemy.org/en/20/core/connections.html#controlling-the-batch-size)
    - [Logging and Events](https://docs.sqlalchemy.org/en/20/core/connections.html#logging-and-events)
    - [Upsert Support](https://docs.sqlalchemy.org/en/20/core/connections.html#upsert-support)
  - [Engine Disposal](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-disposal)
  - [Working with Driver SQL and Raw DBAPI Connections](https://docs.sqlalchemy.org/en/20/core/connections.html#working-with-driver-sql-and-raw-dbapi-connections)
    - [Invoking SQL strings directly to the driver](https://docs.sqlalchemy.org/en/20/core/connections.html#invoking-sql-strings-directly-to-the-driver)
    - [Working with the DBAPI cursor directly](https://docs.sqlalchemy.org/en/20/core/connections.html#working-with-the-dbapi-cursor-directly)
    - [Calling Stored Procedures and User Defined Functions](https://docs.sqlalchemy.org/en/20/core/connections.html#calling-stored-procedures-and-user-defined-functions)
    - [Multiple Result Sets](https://docs.sqlalchemy.org/en/20/core/connections.html#multiple-result-sets)
  - [Registering New Dialects](https://docs.sqlalchemy.org/en/20/core/connections.html#registering-new-dialects)
    - [Registering Dialects In-Process](https://docs.sqlalchemy.org/en/20/core/connections.html#registering-dialects-in-process)
  - [Connection / Engine API](https://docs.sqlalchemy.org/en/20/core/connections.html#connection-engine-api)
    - [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
    - [CreateEnginePlugin](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CreateEnginePlugin)
    - [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
    - [ExceptionContext](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext)
    - [NestedTransaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.NestedTransaction)
    - [RootTransaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.RootTransaction)
    - [Transaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Transaction)
    - [TwoPhaseTransaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TwoPhaseTransaction)
  - [Result Set API](https://docs.sqlalchemy.org/en/20/core/connections.html#result-set-api)
    - [ChunkedIteratorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ChunkedIteratorResult)
    - [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult)
    - [FilterResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.FilterResult)
    - [FrozenResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.FrozenResult)
    - [IteratorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.IteratorResult)
    - [MergedResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.MergedResult)
    - [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)
    - [ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult)
    - [MappingResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.MappingResult)
    - [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
    - [RowMapping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.RowMapping)
    - [TupleResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TupleResult)
- [Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
  - [Connection Pool Configuration](https://docs.sqlalchemy.org/en/20/core/pooling.html#connection-pool-configuration)
  - [Switching Pool Implementations](https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations)
  - [Using a Custom Connection Function](https://docs.sqlalchemy.org/en/20/core/pooling.html#using-a-custom-connection-function)
  - [Constructing a Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#constructing-a-pool)
  - [Reset On Return](https://docs.sqlalchemy.org/en/20/core/pooling.html#reset-on-return)
    - [Disabling Reset on Return for non-transactional connections](https://docs.sqlalchemy.org/en/20/core/pooling.html#disabling-reset-on-return-for-non-transactional-connections)
    - [Custom Reset-on-Return Schemes](https://docs.sqlalchemy.org/en/20/core/pooling.html#custom-reset-on-return-schemes)
    - [Logging reset-on-return events](https://docs.sqlalchemy.org/en/20/core/pooling.html#logging-reset-on-return-events)
  - [Pool Events](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-events)
  - [Dealing with Disconnects](https://docs.sqlalchemy.org/en/20/core/pooling.html#dealing-with-disconnects)
    - [Disconnect Handling - Pessimistic](https://docs.sqlalchemy.org/en/20/core/pooling.html#disconnect-handling-pessimistic)
    - [Disconnect Handling - Optimistic](https://docs.sqlalchemy.org/en/20/core/pooling.html#disconnect-handling-optimistic)
    - [More on Invalidation](https://docs.sqlalchemy.org/en/20/core/pooling.html#more-on-invalidation)
    - [Supporting new database error codes for disconnect scenarios](https://docs.sqlalchemy.org/en/20/core/pooling.html#supporting-new-database-error-codes-for-disconnect-scenarios)
  - [Using FIFO vs. LIFO](https://docs.sqlalchemy.org/en/20/core/pooling.html#using-fifo-vs-lifo)
  - [Using Connection Pools with Multiprocessing or os.fork()](https://docs.sqlalchemy.org/en/20/core/pooling.html#using-connection-pools-with-multiprocessing-or-os-fork)
  - [Using a pool instance directly](https://docs.sqlalchemy.org/en/20/core/pooling.html#using-a-pool-instance-directly)
  - [API Documentation - Available Pool Implementations](https://docs.sqlalchemy.org/en/20/core/pooling.html#api-documentation-available-pool-implementations)
    - [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
    - [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool)
    - [AsyncAdaptedQueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AsyncAdaptedQueuePool)
    - [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool)
    - [AssertionPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AssertionPool)
    - [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool)
    - [StaticPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.StaticPool)
    - [ManagesConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ManagesConnection)
    - [ConnectionPoolEntry](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.ConnectionPoolEntry)
    - [PoolProxiedConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection)
    - [_ConnectionFairy](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool._ConnectionFairy)
    - [_ConnectionRecord](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool._ConnectionRecord)
- [Core Events](https://docs.sqlalchemy.org/en/20/core/events.html)
  - [Events](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.event.base.Events)
    - [Events.dispatch](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.event.base.Events.dispatch)
  - [Connection Pool Events](https://docs.sqlalchemy.org/en/20/core/events.html#connection-pool-events)
    - [PoolEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents)
    - [PoolResetState](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolResetState)
  - [SQL Execution and Connection Events](https://docs.sqlalchemy.org/en/20/core/events.html#sql-execution-and-connection-events)
    - [ConnectionEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents)
    - [DialectEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents)
  - [Schema Events](https://docs.sqlalchemy.org/en/20/core/events.html#schema-events)
    - [DDLEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents)
    - [SchemaEventTarget](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.SchemaEventTarget)

---

# SQLAlchemy 2.0 Documentation

# Events

SQLAlchemy includes an event API which publishes a wide variety of hooks into
the internals of both SQLAlchemy Core and ORM.

## Event Registration

Subscribing to an event occurs through a single API point, the [listen()](#sqlalchemy.event.listen) function,
or alternatively the [listens_for()](#sqlalchemy.event.listens_for) decorator.   These functions accept a
target, a string identifier which identifies the event to be intercepted, and
a user-defined listening function.  Additional positional and keyword arguments to these
two functions may be supported by
specific types of events, which may specify alternate interfaces for the given event function, or provide
instructions regarding secondary event targets based on the given target.

The name of an event and the argument signature of a corresponding listener function is derived from
a class bound specification method, which exists bound to a marker class that’s described in the documentation.
For example, the documentation for [PoolEvents.connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.connect) indicates that the event name is `"connect"`
and that a user-defined listener function should receive two positional arguments:

```
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool

def my_on_connect(dbapi_con, connection_record):
    print("New DBAPI connection:", dbapi_con)

listen(Pool, "connect", my_on_connect)
```

To listen with the [listens_for()](#sqlalchemy.event.listens_for) decorator looks like:

```
from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool

@listens_for(Pool, "connect")
def my_on_connect(dbapi_con, connection_record):
    print("New DBAPI connection:", dbapi_con)
```

## Named Argument Styles

There are some varieties of argument styles which can be accepted by listener
functions.  Taking the example of [PoolEvents.connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.connect), this function
is documented as receiving `dbapi_connection` and `connection_record` arguments.
We can opt to receive these arguments by name, by establishing a listener function
that accepts `**keyword` arguments, by passing `named=True` to either
[listen()](#sqlalchemy.event.listen) or [listens_for()](#sqlalchemy.event.listens_for):

```
from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool

@listens_for(Pool, "connect", named=True)
def my_on_connect(**kw):
    print("New DBAPI connection:", kw["dbapi_connection"])
```

When using named argument passing, the names listed in the function argument
specification will be used as keys in the dictionary.

Named style passes all arguments by name regardless of the function
signature, so specific arguments may be listed as well, in any order,
as long as the names match up:

```
from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool

@listens_for(Pool, "connect", named=True)
def my_on_connect(dbapi_connection, **kw):
    print("New DBAPI connection:", dbapi_connection)
    print("Connection record:", kw["connection_record"])
```

Above, the presence of `**kw` tells [listens_for()](#sqlalchemy.event.listens_for) that
arguments should be passed to the function by name, rather than positionally.

## Targets

The [listen()](#sqlalchemy.event.listen) function is very flexible regarding targets.  It
generally accepts classes, instances of those classes, and related
classes or objects from which the appropriate target can be derived.
For example, the above mentioned `"connect"` event accepts
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) classes and objects as well as [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) classes
and objects:

```
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool, QueuePool
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import psycopg2

def connect():
    return psycopg2.connect(user="ed", host="127.0.0.1", dbname="test")

my_pool = QueuePool(connect)
my_engine = create_engine("postgresql+psycopg2://ed@localhost/test")

# associate listener with all instances of Pool
listen(Pool, "connect", my_on_connect)

# associate listener with all instances of Pool
# via the Engine class
listen(Engine, "connect", my_on_connect)

# associate listener with my_pool
listen(my_pool, "connect", my_on_connect)

# associate listener with my_engine.pool
listen(my_engine, "connect", my_on_connect)
```

## Modifiers

Some listeners allow modifiers to be passed to [listen()](#sqlalchemy.event.listen).  These
modifiers sometimes provide alternate calling signatures for
listeners.  Such as with ORM events, some event listeners can have a
return value which modifies the subsequent handling.   By default, no
listener ever requires a return value, but by passing `retval=True`
this value can be supported:

```
def validate_phone(target, value, oldvalue, initiator):
    """Strip non-numeric characters from a phone number"""

    return re.sub(r"\D", "", value)

# setup listener on UserContact.phone attribute, instructing
# it to use the return value
listen(UserContact.phone, "set", validate_phone, retval=True)
```

## Events and Multiprocessing

SQLAlchemy’s event hooks are implemented with Python functions and objects,
so events propagate via Python function calls.
Python multiprocessing follows the
same way we think about OS multiprocessing,
such as a parent process forking a child process,
thus we can describe the SQLAlchemy event system’s behavior using the same model.

Event hooks registered in a parent process
will be present in new child processes
that are forked from that parent after the hooks have been registered,
since the child process starts with
a copy of all existing Python structures from the parent when spawned.
Child processes that already exist before the hooks are registered
will not receive those new event hooks,
as changes made to Python structures in a parent process
do not propagate to child processes.

For the events themselves, these are Python function calls,
which do not have any ability to propagate between processes.
SQLAlchemy’s event system does not implement any inter-process communication.
It is possible to implement event hooks
that use Python inter-process messaging within them,
however this would need to be implemented by the user.

## Event Reference

Both SQLAlchemy Core and SQLAlchemy ORM feature a wide variety of event hooks:

- **Core Events** - these are described in
  [Core Events](https://docs.sqlalchemy.org/en/20/core/events.html) and include event hooks specific to
  connection pool lifecycle, SQL statement execution,
  transaction lifecycle, and schema creation and teardown.
- **ORM Events** - these are described in
  [ORM Events](https://docs.sqlalchemy.org/en/20/orm/events.html), and include event hooks specific to
  class and attribute instrumentation, object initialization
  hooks, attribute on-change hooks, session state, flush, and
  commit hooks, mapper initialization, object/result population,
  and per-instance persistence hooks.

## API Reference

| Object Name | Description |
| --- | --- |
| contains(target, identifier, fn) | Return True if the given target/ident/fn is set up to listen. |
| listen(target, identifier, fn, *args, **kw) | Register a listener function for the given target. |
| listens_for(target, identifier, *args, **kw) | Decorate a function as a listener for the given target + identifier. |
| remove(target, identifier, fn) | Remove an event listener. |

   function sqlalchemy.event.listen(*target:Any*, *identifier:str*, *fn:Callable[[...],Any]*, **args:Any*, ***kw:Any*) → None

Register a listener function for the given target.

The [listen()](#sqlalchemy.event.listen) function is part of the primary interface for the
SQLAlchemy event system, documented at [Events](#).

e.g.:

```
from sqlalchemy import event
from sqlalchemy.schema import UniqueConstraint

def unique_constraint_name(const, table):
    const.name = "uq_%s_%s" % (table.name, list(const.columns)[0].name)

event.listen(
    UniqueConstraint, "after_parent_attach", unique_constraint_name
)
```

   Parameters:

- **insert** (*bool*) – The default behavior for event handlers is to append
  the decorated user defined function to an internal list of registered
  event listeners upon discovery. If a user registers a function with
  `insert=True`, SQLAlchemy will insert (prepend) the function to the
  internal list upon discovery. This feature is not typically used or
  recommended by the SQLAlchemy maintainers, but is provided to ensure
  certain user defined functions can run before others, such as when
  [Changing the sql_mode in MySQL](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-sql-mode).
- **named** (*bool*) – When using named argument passing, the names listed in
  the function argument specification will be used as keys in the
  dictionary.
  See [Named Argument Styles](#event-named-argument-styles).
- **once** (*bool*) – Private/Internal API usage. Deprecated.  This parameter
  would provide that an event function would run only once per given
  target. It does not however imply automatic de-registration of the
  listener function; associating an arbitrarily high number of listeners
  without explicitly removing them will cause memory to grow unbounded even
  if `once=True` is specified.
- **propagate** (*bool*) – The `propagate` kwarg is available when working
  with ORM instrumentation and mapping events.
  See [MapperEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents) and
  [MapperEvents.before_mapper_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_mapper_configured) for examples.
- **retval** (*bool*) –
  This flag applies only to specific event listeners,
  each of which includes documentation explaining when it should be used.
  By default, no listener ever requires a return value.
  However, some listeners do support special behaviors for return values,
  and include in their documentation that the `retval=True` flag is
  necessary for a return value to be processed.
  Event listener suites that make use of [listen.retval](#sqlalchemy.event.listen.params.retval)
  include [ConnectionEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents) and
  [AttributeEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents).

Note

The [listen()](#sqlalchemy.event.listen) function cannot be called at the same time
that the target event is being run.   This has implications
for thread safety, and also means an event cannot be added
from inside the listener function for itself.  The list of
events to be run are present inside of a mutable collection
that can’t be changed during iteration.

Event registration and removal is not intended to be a “high
velocity” operation; it is a configurational operation.  For
systems that need to quickly associate and deassociate with
events at high scale, use a mutable structure that is handled
from inside of a single listener.

See also

[listens_for()](#sqlalchemy.event.listens_for)

[remove()](#sqlalchemy.event.remove)

     function sqlalchemy.event.listens_for(*target:Any*, *identifier:str*, **args:Any*, ***kw:Any*) → Callable[[Callable[[...], Any]], Callable[[...], Any]]

Decorate a function as a listener for the given target + identifier.

The [listens_for()](#sqlalchemy.event.listens_for) decorator is part of the primary interface for the
SQLAlchemy event system, documented at [Events](#).

This function generally shares the same kwargs as [listen()](#sqlalchemy.event.listen).

e.g.:

```
from sqlalchemy import event
from sqlalchemy.schema import UniqueConstraint

@event.listens_for(UniqueConstraint, "after_parent_attach")
def unique_constraint_name(const, table):
    const.name = "uq_%s_%s" % (table.name, list(const.columns)[0].name)
```

A given function can also be invoked for only the first invocation
of the event using the `once` argument:

```
@event.listens_for(Mapper, "before_configure", once=True)
def on_config():
    do_config()
```

Warning

The `once` argument does not imply automatic de-registration
of the listener function after it has been invoked a first time; a
listener entry will remain associated with the target object.
Associating an arbitrarily high number of listeners without explicitly
removing them will cause memory to grow unbounded even if `once=True`
is specified.

See also

[listen()](#sqlalchemy.event.listen) - general description of event listening

     function sqlalchemy.event.remove(*target:Any*, *identifier:str*, *fn:Callable[[...],Any]*) → None

Remove an event listener.

The arguments here should match exactly those which were sent to
[listen()](#sqlalchemy.event.listen); all the event registration which proceeded as a result
of this call will be reverted by calling [remove()](#sqlalchemy.event.remove) with the same
arguments.

e.g.:

```
# if a function was registered like this...
@event.listens_for(SomeMappedClass, "before_insert", propagate=True)
def my_listener_function(*arg):
    pass

# ... it's removed like this
event.remove(SomeMappedClass, "before_insert", my_listener_function)
```

Above, the listener function associated with `SomeMappedClass` was also
propagated to subclasses of `SomeMappedClass`; the [remove()](#sqlalchemy.event.remove)
function will revert all of these operations.

Note

The [remove()](#sqlalchemy.event.remove) function cannot be called at the same time
that the target event is being run.   This has implications
for thread safety, and also means an event cannot be removed
from inside the listener function for itself.  The list of
events to be run are present inside of a mutable collection
that can’t be changed during iteration.

Event registration and removal is not intended to be a “high
velocity” operation; it is a configurational operation.  For
systems that need to quickly associate and deassociate with
events at high scale, use a mutable structure that is handled
from inside of a single listener.

See also

[listen()](#sqlalchemy.event.listen)

     function sqlalchemy.event.contains(*target:Any*, *identifier:str*, *fn:Callable[[...],Any]*) → bool

Return True if the given target/ident/fn is set up to listen.
