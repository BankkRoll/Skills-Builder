# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Transactions and Connection Management

## Managing Transactions

Changed in version 1.4: Session transaction management has been revised
to be clearer and easier to use.  In particular, it now features
“autobegin” operation, which means the point at which a transaction begins
may be controlled, without using the legacy “autocommit” mode.

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) tracks the state of a single “virtual” transaction
at a time, using an object called
[SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction).   This object then makes use of the underlying
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or engines to which the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
object is bound in order to start real connection-level transactions using
the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object as needed.

This “virtual” transaction is created automatically when needed, or can
alternatively be started using the [Session.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin) method.  To
as great a degree as possible, Python context manager use is supported both
at the level of creating [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects as well as to maintain
the scope of the [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction).

Below, assume we start with a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session):

```
from sqlalchemy.orm import Session

session = Session(engine)
```

We can now run operations within a demarcated transaction using a context
manager:

```
with session.begin():
    session.add(some_object())
    session.add(some_other_object())
# commits transaction at the end, or rolls back if there
# was an exception raised
```

At the end of the above context, assuming no exceptions were raised, any
pending objects will be flushed to the database and the database transaction
will be committed. If an exception was raised within the above block, then the
transaction would be rolled back.  In both cases, the above
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) subsequent to exiting the block is ready to be used in
subsequent transactions.

The [Session.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin) method is optional, and the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) may also be used in a commit-as-you-go approach, where it
will begin transactions automatically as needed; these only need be committed
or rolled back:

```
session = Session(engine)

session.add(some_object())
session.add(some_other_object())

session.commit()  # commits

# will automatically begin again
result = session.execute(text("< some select statement >"))
session.add_all([more_objects, ...])
session.commit()  # commits

session.add(still_another_object)
session.flush()  # flush still_another_object
session.rollback()  # rolls back still_another_object
```

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) itself features a [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close)
method.  If the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is begun within a transaction that
has not yet been committed or rolled back, this method will cancel
(i.e. rollback) that transaction, and also expunge all objects contained
within the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s state.   If the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
is being used in such a way that a call to [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit)
or [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) is not guaranteed (e.g. not within a context
manager or similar), the [close](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) method may be used
to ensure all resources are released:

```
# expunges all objects, releases all transactions unconditionally
# (with rollback), releases all database connections back to their
# engines
session.close()
```

Finally, the session construction / close process can itself be run
via context manager.  This is the best way to ensure that the scope of
a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s use is scoped within a fixed block.
Illustrated via the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) constructor
first:

```
with Session(engine) as session:
    session.add(some_object())
    session.add(some_other_object())

    session.commit()  # commits

    session.add(still_another_object)
    session.flush()  # flush still_another_object

    session.commit()  # commits

    result = session.execute(text("<some SELECT statement>"))

# remaining transactional state from the .execute() call is
# discarded
```

Similarly, the [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) can be used in the same way:

```
Session = sessionmaker(engine)

with Session() as session:
    with session.begin():
        session.add(some_object)
    # commits

# closes the Session
```

[sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) itself includes a [sessionmaker.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker.begin)
method to allow both operations to take place at once:

```
with Session.begin() as session:
    session.add(some_object)
```

### Using SAVEPOINT

SAVEPOINT transactions, if supported by the underlying engine, may be
delineated using the [Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested)
method:

```
Session = sessionmaker()

with Session.begin() as session:
    session.add(u1)
    session.add(u2)

    nested = session.begin_nested()  # establish a savepoint
    session.add(u3)
    nested.rollback()  # rolls back u3, keeps u1 and u2

# commits u1 and u2
```

Each time [Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested) is called, a new “BEGIN SAVEPOINT”
command is emitted to the database within the scope of the current
database transaction (starting one if not already in progress), and
an object of type [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) is returned, which
represents a handle to this SAVEPOINT.  When
the `.commit()` method on this object is called, “RELEASE SAVEPOINT”
is emitted to the database, and if instead the `.rollback()`
method is called, “ROLLBACK TO SAVEPOINT” is emitted.  The enclosing
database transaction remains in progress.

[Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested) is typically used as a context manager
where specific per-instance errors may be caught, in conjunction with
a rollback emitted for that portion of the transaction’s state, without
rolling back the whole transaction, as in the example below:

```
for record in records:
    try:
        with session.begin_nested():
            session.merge(record)
    except:
        print("Skipped record %s" % record)
session.commit()
```

When the context manager yielded by [Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested)
completes, it “commits” the savepoint,
which includes the usual behavior of flushing all pending state.  When
an error is raised, the savepoint is rolled back and the state of the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) local to the objects that were changed is expired.

This pattern is ideal for situations such as using PostgreSQL and
catching [IntegrityError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.IntegrityError) to detect duplicate rows; PostgreSQL normally
aborts the entire transaction when such an error is raised, however when using
SAVEPOINT, the outer transaction is maintained.   In the example below
a list of data is persisted into the database, with the occasional
“duplicate primary key” record skipped, without rolling back the entire
operation:

```
from sqlalchemy import exc

with session.begin():
    for record in records:
        try:
            with session.begin_nested():
                obj = SomeRecord(id=record["identifier"], name=record["name"])
                session.add(obj)
        except exc.IntegrityError:
            print(f"Skipped record {record} - row already exists")
```

When [Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested) is called, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) first
flushes all currently pending state to the database; this occurs unconditionally,
regardless of the value of the [Session.autoflush](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.autoflush) parameter
which normally may be used to disable automatic flush.  The rationale
for this behavior is so that
when a rollback on this nested transaction occurs, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
may expire any in-memory state that was created within the scope of the
SAVEPOINT, while
ensuring that when those expired objects are refreshed, the state of the
object graph prior to the beginning of the SAVEPOINT will be available
to re-load from the database.

In modern versions of SQLAlchemy, when a SAVEPOINT initiated by
[Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested) is rolled back, in-memory object state that
was modified since the SAVEPOINT was created
is expired, however other object state that was not altered since the SAVEPOINT
began is maintained.  This is so that subsequent operations can continue to make use of the
otherwise unaffected data
without the need for refreshing it from the database.

See also

[Connection.begin_nested()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.begin_nested) -  Core SAVEPOINT API

### Session-level vs. Engine level transaction control

The [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) in Core and
`_session.Session` in ORM feature equivalent transactional
semantics, both at the level of the [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) vs.
the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), as well as the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) vs.
the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  The following sections detail
these scenarios based on the following scheme:

```
ORM                                           Core
-----------------------------------------     -----------------------------------
sessionmaker                                  Engine
Session                                       Connection
sessionmaker.begin()                          Engine.begin()
some_session.commit()                         some_connection.commit()
with some_sessionmaker() as session:          with some_engine.connect() as conn:
with some_sessionmaker.begin() as session:    with some_engine.begin() as conn:
with some_session.begin_nested() as sp:       with some_connection.begin_nested() as sp:
```

#### Commit as you go

Both [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) feature
[Connection.commit()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.commit) and [Connection.rollback()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.rollback)
methods.   Using SQLAlchemy 2.0-style operation, these methods affect the
**outermost** transaction in all cases.   For the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), it is
assumed that [Session.autobegin](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.autobegin) is left at its default
value of `True`.

[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine):

```
engine = create_engine("postgresql+psycopg2://user:pass@host/dbname")

with engine.connect() as conn:
    conn.execute(
        some_table.insert(),
        [
            {"data": "some data one"},
            {"data": "some data two"},
            {"data": "some data three"},
        ],
    )
    conn.commit()
```

[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session):

```
Session = sessionmaker(engine)

with Session() as session:
    session.add_all(
        [
            SomeClass(data="some data one"),
            SomeClass(data="some data two"),
            SomeClass(data="some data three"),
        ]
    )
    session.commit()
```

#### Begin Once

Both [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) and [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) feature a
[Engine.begin()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.begin) method that will both procure a new object
with which to execute SQL statements (the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), respectively) and then return a context manager
that will maintain a begin/commit/rollback context for that object.

Engine:

```
engine = create_engine("postgresql+psycopg2://user:pass@host/dbname")

with engine.begin() as conn:
    conn.execute(
        some_table.insert(),
        [
            {"data": "some data one"},
            {"data": "some data two"},
            {"data": "some data three"},
        ],
    )
# commits and closes automatically
```

Session:

```
Session = sessionmaker(engine)

with Session.begin() as session:
    session.add_all(
        [
            SomeClass(data="some data one"),
            SomeClass(data="some data two"),
            SomeClass(data="some data three"),
        ]
    )
# commits and closes automatically
```

#### Nested Transaction

When using a SAVEPOINT via the [Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested) or
[Connection.begin_nested()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.begin_nested) methods, the transaction object
returned must be used to commit or rollback the SAVEPOINT.  Calling
the [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) or [Connection.commit()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.commit) methods
will always commit the **outermost** transaction; this is a SQLAlchemy 2.0
specific behavior that is reversed from the 1.x series.

Engine:

```
engine = create_engine("postgresql+psycopg2://user:pass@host/dbname")

with engine.begin() as conn:
    savepoint = conn.begin_nested()
    conn.execute(
        some_table.insert(),
        [
            {"data": "some data one"},
            {"data": "some data two"},
            {"data": "some data three"},
        ],
    )
    savepoint.commit()  # or rollback

# commits automatically
```

Session:

```
Session = sessionmaker(engine)

with Session.begin() as session:
    savepoint = session.begin_nested()
    session.add_all(
        [
            SomeClass(data="some data one"),
            SomeClass(data="some data two"),
            SomeClass(data="some data three"),
        ]
    )
    savepoint.commit()  # or rollback
# commits automatically
```

### Explicit Begin

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) features “autobegin” behavior, meaning that as soon
as operations begin to take place, it ensures a [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)
is present to track ongoing operations.   This transaction is completed
when [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) is called.

It is often desirable, particularly in framework integrations, to control the
point at which the “begin” operation occurs.  To suit this, the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) uses an “autobegin” strategy, such that the
[Session.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin) method may be called directly for a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) that has not already had a transaction begun:

```
Session = sessionmaker(bind=engine)
session = Session()
session.begin()
try:
    item1 = session.get(Item, 1)
    item2 = session.get(Item, 2)
    item1.foo = "bar"
    item2.bar = "foo"
    session.commit()
except:
    session.rollback()
    raise
```

The above pattern is more idiomatically invoked using a context manager:

```
Session = sessionmaker(bind=engine)
session = Session()
with session.begin():
    item1 = session.get(Item, 1)
    item2 = session.get(Item, 2)
    item1.foo = "bar"
    item2.bar = "foo"
```

The [Session.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin) method and the session’s “autobegin” process
use the same sequence of steps to begin the transaction.   This includes
that the [SessionEvents.after_transaction_create()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.after_transaction_create) event is invoked
when it occurs; this hook is used by frameworks in order to integrate their
own transactional processes with that of the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

### Enabling Two-Phase Commit

For backends which support two-phase operation (currently MySQL and
PostgreSQL), the session can be instructed to use two-phase commit semantics.
This will coordinate the committing of transactions across databases so that
the transaction is either committed or rolled back in all databases. You can
also [Session.prepare()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.prepare) the session for
interacting with transactions not managed by SQLAlchemy. To use two phase
transactions set the flag `twophase=True` on the session:

```
engine1 = create_engine("postgresql+psycopg2://db1")
engine2 = create_engine("postgresql+psycopg2://db2")

Session = sessionmaker(twophase=True)

# bind User operations to engine 1, Account operations to engine 2
Session.configure(binds={User: engine1, Account: engine2})

session = Session()

# .... work with accounts and users

# commit.  session will issue a flush to all DBs, and a prepare step to all DBs,
# before committing both transactions
session.commit()
```

### Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT

Most DBAPIs support the concept of configurable transaction [isolation](https://docs.sqlalchemy.org/en/20/glossary.html#term-isolation) levels.
These are traditionally the four levels “READ UNCOMMITTED”, “READ COMMITTED”,
“REPEATABLE READ” and “SERIALIZABLE”.  These are usually applied to a
DBAPI connection before it begins a new transaction, noting that most
DBAPIs will begin this transaction implicitly when SQL statements are first
emitted.

DBAPIs that support isolation levels also usually support the concept of true
“autocommit”, which means that the DBAPI connection itself will be placed into
a non-transactional autocommit mode.   This usually means that the typical
DBAPI behavior of emitting “BEGIN” to the database automatically no longer
occurs, but it may also include other directives.   When using this mode,
**the DBAPI does not use a transaction under any circumstances**.  SQLAlchemy
methods like `.begin()`, `.commit()` and `.rollback()` pass silently.

SQLAlchemy’s dialects support settable isolation modes on a per-[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
or per-[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) basis, using flags at both the
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) level as well as at the [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options)
level.

When using the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), it acts as a *facade* for engines and
connections, but does not expose transaction isolation directly.  So in
order to affect transaction isolation level, we need to act upon the
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) as appropriate.

See also

[Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit) - be sure to review how isolation levels work at
the level of the SQLAlchemy [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object as well.

#### Setting Isolation For A Sessionmaker / Engine Wide

To set up a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) or [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) with a specific
isolation level globally, the first technique is that an
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) can be constructed against a specific isolation level
in all cases, which is then used as the source of connectivity for a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and/or [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker):

```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

eng = create_engine(
    "postgresql+psycopg2://scott:tiger@localhost/test",
    isolation_level="REPEATABLE READ",
)

Session = sessionmaker(eng)
```

Another option, useful if there are to be two engines with different isolation
levels at once, is to use the [Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options) method,
which will produce a shallow copy of the original [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which
shares the same connection pool as the parent engine.  This is often preferable
when operations will be separated into “transactional” and “autocommit”
operations:

```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

eng = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")

autocommit_engine = eng.execution_options(isolation_level="AUTOCOMMIT")

transactional_session = sessionmaker(eng)
autocommit_session = sessionmaker(autocommit_engine)
```

Above, both “`eng`” and `"autocommit_engine"` share the same dialect and
connection pool.  However the “AUTOCOMMIT” mode will be set upon connections
when they are acquired from the `autocommit_engine`.  The two
[sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) objects “`transactional_session`” and “`autocommit_session"`
then inherit these characteristics when they work with database connections.

The “`autocommit_session`” **continues to have transactional semantics**,
including that
[Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) and [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) still consider
themselves to be “committing” and “rolling back” objects, however the
transaction will be silently absent.  For this reason, **it is typical,
though not strictly required, that a Session with AUTOCOMMIT isolation be
used in a read-only fashion**, that is:

```
with autocommit_session() as session:
    some_objects = session.execute(text("<statement>"))
    some_other_objects = session.execute(text("<statement>"))

# closes connection
```

#### Setting Isolation for Individual Sessions

When we make a new [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), either using the constructor directly
or when we call upon the callable produced by a [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker),
we can pass the `bind` argument directly, overriding the pre-existing bind.
We can for example create our [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) from a default
[sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) and pass an engine set for autocommit:

```
plain_engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")

autocommit_engine = plain_engine.execution_options(isolation_level="AUTOCOMMIT")

# will normally use plain_engine
Session = sessionmaker(plain_engine)

# make a specific Session that will use the "autocommit" engine
with Session(bind=autocommit_engine) as session:
    # work with session
    ...
```

For the case where the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) or [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) is
configured with multiple “binds”, we can either re-specify the `binds`
argument fully, or if we want to only replace specific binds, we
can use the [Session.bind_mapper()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bind_mapper) or [Session.bind_table()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bind_table)
methods:

```
with Session() as session:
    session.bind_mapper(User, autocommit_engine)
```

#### Setting Isolation for Individual Transactions

A key caveat regarding isolation level is that the setting cannot be
safely modified on a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) where a transaction has already
started.  Databases cannot change the isolation level of a transaction
in progress, and some DBAPIs and SQLAlchemy dialects
have inconsistent behaviors in this area.

Therefore it is preferable to use a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) that is up front
bound to an engine with the desired isolation level.  However, the isolation
level on a per-connection basis can be affected by using the
[Session.connection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) method at the start of a transaction:

```
from sqlalchemy.orm import Session

# assume session just constructed
sess = Session(bind=engine)

# call connection() with options before any other operations proceed.
# this will procure a new connection from the bound engine and begin a real
# database transaction.
sess.connection(execution_options={"isolation_level": "SERIALIZABLE"})

# ... work with session in SERIALIZABLE isolation level...

# commit transaction.  the connection is released
# and reverted to its previous isolation level.
sess.commit()

# subsequent to commit() above, a new transaction may be begun if desired,
# which will proceed with the previous default isolation level unless
# it is set again.
```

Above, we first produce a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) using either the constructor or a
[sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker). Then we explicitly set up the start of a database-level
transaction by calling upon [Session.connection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection), which provides for
execution options that will be passed to the connection before the
database-level transaction is begun.  The transaction proceeds with this
selected isolation level.   When the transaction completes, the isolation
level is reset on the connection to its default before the connection is
returned to the connection pool.

The [Session.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin) method may also be used to begin the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) level transaction; calling upon
[Session.connection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) subsequent to that call may be used to set up
the per-connection-transaction isolation level:

```
sess = Session(bind=engine)

with sess.begin():
    # call connection() with options before any other operations proceed.
    # this will procure a new connection from the bound engine and begin a
    # real database transaction.
    sess.connection(execution_options={"isolation_level": "SERIALIZABLE"})

    # ... work with session in SERIALIZABLE isolation level...

# outside the block, the transaction has been committed.  the connection is
# released and reverted to its previous isolation level.
```

### Tracking Transaction State with Events

See the section [Transaction Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-transaction-events) for an overview
of the available event hooks for session transaction state changes.

## Joining a Session into an External Transaction (such as for test suites)

If a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is being used which is already in a transactional
state (i.e. has a [Transaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Transaction) established), a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) can
be made to participate within that transaction by just binding the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to that [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection). The usual rationale for this
is a test suite that allows ORM code to work freely with a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
including the ability to call [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit), where afterwards the
entire database interaction is rolled back.

Changed in version 2.0: The “join into an external transaction” recipe is
newly improved again in 2.0; event handlers to “reset” the nested
transaction are no longer required.

The recipe works by establishing a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) within a
transaction and optionally a SAVEPOINT, then passing it to a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) as the “bind”; the
[Session.join_transaction_mode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.join_transaction_mode) parameter is passed with the
setting `"create_savepoint"`, which indicates that new SAVEPOINTs should be
created in order to implement BEGIN/COMMIT/ROLLBACK for the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), which will leave the external transaction in the same
state in which it was passed.

When the test tears down, the external transaction is rolled back so that any
data changes throughout the test are reverted:

```
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from unittest import TestCase

# global application scope.  create Session class, engine
Session = sessionmaker()

engine = create_engine("postgresql+psycopg2://...")

class SomeTest(TestCase):
    def setUp(self):
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection, selecting
        # "create_savepoint" join_transaction_mode
        self.session = Session(
            bind=self.connection, join_transaction_mode="create_savepoint"
        )

    def test_something(self):
        # use the session in tests.

        self.session.add(Foo())
        self.session.commit()

    def test_something_with_rollbacks(self):
        self.session.add(Bar())
        self.session.flush()
        self.session.rollback()

        self.session.add(Foo())
        self.session.commit()

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()
```

The above recipe is part of SQLAlchemy’s own CI to ensure that it remains
working as expected.

---

# SQLAlchemy 2.0 Documentation

# Object Relational Tutorial

We’ve Moved!

This page is the previous home of the SQLAlchemy 1.x Tutorial.  As of 2.0,
SQLAlchemy presents a revised way of working and an all new tutorial that
presents Core and ORM in an integrated fashion using all the latest usage
patterns.    See [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial).

---

# SQLAlchemy 2.0 Documentation

# Configuring a Version Counter

The [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) supports management of a [version id column](https://docs.sqlalchemy.org/en/20/glossary.html#term-version-id-column), which
is a single table column that increments or otherwise updates its value
each time an `UPDATE` to the mapped table occurs.  This value is checked each
time the ORM emits an `UPDATE` or `DELETE` against the row to ensure that
the value held in memory matches the database value.

Warning

Because the versioning feature relies upon comparison of the **in memory**
record of an object, the feature only applies to the [Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush)
process, where the ORM flushes individual in-memory rows to the database.
It does **not** take effect when performing
a multirow UPDATE or DELETE using [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) or [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete)
methods, as these methods only emit an UPDATE or DELETE statement but otherwise
do not have direct access to the contents of those rows being affected.

The purpose of this feature is to detect when two concurrent transactions
are modifying the same row at roughly the same time, or alternatively to provide
a guard against the usage of a “stale” row in a system that might be reusing
data from a previous transaction without refreshing (e.g. if one sets `expire_on_commit=False`
with a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), it is possible to reuse the data from a previous
transaction).

Concurrent transaction updates

When detecting concurrent updates within transactions, it is typically the
case that the database’s transaction isolation level is below the level of
[repeatable read](https://docs.sqlalchemy.org/en/20/glossary.html#term-repeatable-read); otherwise, the transaction will not be exposed
to a new row value created by a concurrent update which conflicts with
the locally updated value.  In this case, the SQLAlchemy versioning
feature will typically not be useful for in-transaction conflict detection,
though it still can be used for cross-transaction staleness detection.

The database that enforces repeatable reads will typically either have locked the
target row against a concurrent update, or is employing some form
of multi version concurrency control such that it will emit an error
when the transaction is committed.  SQLAlchemy’s version_id_col is an alternative
which allows version tracking to occur for specific tables within a transaction
that otherwise might not have this isolation level set.

See also

[Repeatable Read Isolation Level](https://www.postgresql.org/docs/current/static/transaction-iso.html#XACT-REPEATABLE-READ) - PostgreSQL’s implementation of repeatable read, including a description of the error condition.

## Simple Version Counting

The most straightforward way to track versions is to add an integer column
to the mapped table, then establish it as the `version_id_col` within the
mapper options:

```
class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    version_id = mapped_column(Integer, nullable=False)
    name = mapped_column(String(50), nullable=False)

    __mapper_args__ = {"version_id_col": version_id}
```

Note

It is **strongly recommended** that the `version_id` column
be made NOT NULL.  The versioning feature **does not support** a NULL
value in the versioning column.

Above, the `User` mapping tracks integer versions using the column
`version_id`.   When an object of type `User` is first flushed, the
`version_id` column will be given a value of “1”.   Then, an UPDATE
of the table later on will always be emitted in a manner similar to the
following:

```
UPDATE user SET version_id=:version_id, name=:name
WHERE user.id = :user_id AND user.version_id = :user_version_id
-- {"name": "new name", "version_id": 2, "user_id": 1, "user_version_id": 1}
```

The above UPDATE statement is updating the row that not only matches
`user.id = 1`, it also is requiring that `user.version_id = 1`, where “1”
is the last version identifier we’ve been known to use on this object.
If a transaction elsewhere has modified the row independently, this version id
will no longer match, and the UPDATE statement will report that no rows matched;
this is the condition that SQLAlchemy tests, that exactly one row matched our
UPDATE (or DELETE) statement.  If zero rows match, that indicates our version
of the data is stale, and a [StaleDataError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.StaleDataError) is raised.

## Custom Version Counters / Types

Other kinds of values or counters can be used for versioning.  Common types include
dates and GUIDs.   When using an alternate type or counter scheme, SQLAlchemy
provides a hook for this scheme using the `version_id_generator` argument,
which accepts a version generation callable.  This callable is passed the value of the current
known version, and is expected to return the subsequent version.

For example, if we wanted to track the versioning of our `User` class
using a randomly generated GUID, we could do this (note that some backends
support a native GUID type, but we illustrate here using a simple string):

```
import uuid

class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    version_uuid = mapped_column(String(32), nullable=False)
    name = mapped_column(String(50), nullable=False)

    __mapper_args__ = {
        "version_id_col": version_uuid,
        "version_id_generator": lambda version: uuid.uuid4().hex,
    }
```

The persistence engine will call upon `uuid.uuid4()` each time a
`User` object is subject to an INSERT or an UPDATE.  In this case, our
version generation function can disregard the incoming value of `version`,
as the `uuid4()` function
generates identifiers without any prerequisite value.  If we were using
a sequential versioning scheme such as numeric or a special character system,
we could make use of the given `version` in order to help determine the
subsequent value.

See also

[Backend-agnostic GUID Type](https://docs.sqlalchemy.org/en/20/core/custom_types.html#custom-guid-type)

## Server Side Version Counters

The `version_id_generator` can also be configured to rely upon a value
that is generated by the database.  In this case, the database would need
some means of generating new identifiers when a row is subject to an INSERT
as well as with an UPDATE.   For the UPDATE case, typically an update trigger
is needed, unless the database in question supports some other native
version identifier.  The PostgreSQL database in particular supports a system
column called [xmin](https://www.postgresql.org/docs/current/static/ddl-system-columns.html)
which provides UPDATE versioning.  We can make use
of the PostgreSQL `xmin` column to version our `User`
class as follows:

```
from sqlalchemy import FetchedValue

class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    xmin = mapped_column("xmin", String, system=True, server_default=FetchedValue())

    __mapper_args__ = {"version_id_col": xmin, "version_id_generator": False}
```

With the above mapping, the ORM will rely upon the `xmin` column for
automatically providing the new value of the version id counter.

creating tables that refer to system columns

In the above scenario, as `xmin` is a system column provided by PostgreSQL,
we use the `system=True` argument to mark it as a system-provided
column, omitted from the `CREATE TABLE` statement.   The datatype of this
column is an internal PostgreSQL type called `xid` which acts mostly
like a string, so we use the [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) datatype.

The ORM typically does not actively fetch the values of database-generated
values when it emits an INSERT or UPDATE, instead leaving these columns as
“expired” and to be fetched when they are next accessed, unless the `eager_defaults` [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) flag is set.  However, when a
server side version column is used, the ORM needs to actively fetch the newly
generated value.  This is so that the version counter is set up *before*
any concurrent transaction may update it again.   This fetching is also
best done simultaneously within the INSERT or UPDATE statement using [RETURNING](https://docs.sqlalchemy.org/en/20/glossary.html#term-RETURNING),
otherwise if emitting a SELECT statement afterwards, there is still a potential
race condition where the version counter may change before it can be fetched.

When the target database supports RETURNING, an INSERT statement for our `User` class will look
like this:

```
INSERT INTO "user" (name) VALUES (%(name)s) RETURNING "user".id, "user".xmin
-- {'name': 'ed'}
```

Where above, the ORM can acquire any newly generated primary key values along
with server-generated version identifiers in one statement.   When the backend
does not support RETURNING, an additional SELECT must be emitted for **every**
INSERT and UPDATE, which is much less efficient, and also introduces the possibility of
missed version counters:

```
INSERT INTO "user" (name) VALUES (%(name)s)
-- {'name': 'ed'}

SELECT "user".version_id AS user_version_id FROM "user" where
"user".id = :param_1
-- {"param_1": 1}
```

It is *strongly recommended* that server side version counters only be used
when absolutely necessary and only on backends that support [RETURNING](https://docs.sqlalchemy.org/en/20/glossary.html#term-RETURNING),
currently PostgreSQL, Oracle Database, MariaDB 10.5, SQLite 3.35, and SQL
Server.

## Programmatic or Conditional Version Counters

When `version_id_generator` is set to False, we can also programmatically
(and conditionally) set the version identifier on our object in the same way
we assign any other mapped attribute.  Such as if we used our UUID example, but
set `version_id_generator` to `False`, we can set the version identifier
at our choosing:

```
import uuid

class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    version_uuid = mapped_column(String(32), nullable=False)
    name = mapped_column(String(50), nullable=False)

    __mapper_args__ = {"version_id_col": version_uuid, "version_id_generator": False}

u1 = User(name="u1", version_uuid=uuid.uuid4().hex)

session.add(u1)

session.commit()

u1.name = "u2"
u1.version_uuid = uuid.uuid4().hex

session.commit()
```

We can update our `User` object without incrementing the version counter
as well; the value of the counter will remain unchanged, and the UPDATE
statement will still check against the previous value.  This may be useful
for schemes where only certain classes of UPDATE are sensitive to concurrency
issues:

```
# will leave version_uuid unchanged
u1.name = "u3"
session.commit()
```
