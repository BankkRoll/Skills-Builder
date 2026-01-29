# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [Working with Data](https://docs.sqlalchemy.org/en/20/tutorial/data.html)   |   Next: [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html)

# Data Manipulation with the ORM

The previous section [Working with Data](https://docs.sqlalchemy.org/en/20/tutorial/data.html#tutorial-working-with-data) remained focused on
the SQL Expression Language from a Core perspective, in order to provide
continuity across the major SQL statement constructs.  This section will
then build out the lifecycle of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and how it interacts
with these constructs.

**Prerequisite Sections** - the ORM focused part of the tutorial builds upon
two previous ORM-centric sections in this document:

- [Executing with an ORM Session](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-executing-orm-session) - introduces how to make an ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object
- [Using ORM Declarative Forms to Define Table Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-orm-table-metadata) - where we set up our ORM mappings of the `User` and `Address` entities
- [Selecting ORM Entities and Columns](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-orm-entities) - a few examples on how to run SELECT statements for entities like `User`

## Inserting Rows using the ORM Unit of Work pattern

When using the ORM, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object is responsible for
constructing [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) constructs and emitting them as INSERT
statements within the ongoing transaction. The way we instruct the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to do so is by **adding** object entries to it; the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) then makes sure these new entries will be emitted to the
database when they are needed, using a process known as a **flush**. The
overall process used by the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to persist objects is known
as the [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) pattern.

### Instances of Classes represent Rows

Whereas in the previous example we emitted an INSERT using Python dictionaries
to indicate the data we wanted to add, with the ORM we make direct use of the
custom Python classes we defined, back at
[Using ORM Declarative Forms to Define Table Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-orm-table-metadata).    At the class level, the `User` and
`Address` classes served as a place to define what the corresponding
database tables should look like.   These classes also serve as extensible
data objects that we use to create and manipulate rows within a transaction
as well.  Below we will create two `User` objects each representing a
potential database row to be INSERTed:

```
>>> squidward = User(name="squidward", fullname="Squidward Tentacles")
>>> krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
```

We are able to construct these objects using the names of the mapped columns as
keyword arguments in the constructor.  This is possible as the `User` class
includes an automatically generated `__init__()` constructor that was
provided by the ORM mapping so that we could create each object using column
names as keys in the constructor.

In a similar manner as in our Core examples of [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), we did not
include a primary key (i.e. an entry for the `id` column), since we would
like to make use of the auto-incrementing primary key feature of the database,
SQLite in this case, which the ORM also integrates with.
The value of the `id` attribute on the above
objects, if we were to view it, displays itself as `None`:

```
>>> squidward
User(id=None, name='squidward', fullname='Squidward Tentacles')
```

The `None` value is provided by SQLAlchemy to indicate that the attribute
has no value as of yet.  SQLAlchemy-mapped attributes always return a value
in Python and don’t raise `AttributeError` if they’re missing, when
dealing with a new object that has not had a value assigned.

At the moment, our two objects above are said to be in a state called
[transient](https://docs.sqlalchemy.org/en/20/glossary.html#term-transient) - they are not associated with any database state and are yet
to be associated with a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object that can generate
INSERT statements for them.

### Adding objects to a Session

To illustrate the addition process step by step, we will create a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) without using a context manager (and hence we must
make sure we close it later!):

```
>>> session = Session(engine)
```

The objects are then added to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) using the
[Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) method.   When this is called, the objects are in a
state known as [pending](https://docs.sqlalchemy.org/en/20/glossary.html#term-pending) and have not been inserted yet:

```
>>> session.add(squidward)
>>> session.add(krabs)
```

When we have pending objects, we can see this state by looking at a
collection on the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) called [Session.new](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.new):

```
>>> session.new
IdentitySet([User(id=None, name='squidward', fullname='Squidward Tentacles'), User(id=None, name='ehkrabs', fullname='Eugene H. Krabs')])
```

The above view is using a collection called `IdentitySet` that is
essentially a Python set that hashes on object identity in all cases (i.e.,
using Python built-in `id()` function, rather than the Python `hash()` function).

### Flushing

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) makes use of a pattern known as [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work).
This generally means it accumulates changes one at a time, but does not actually
communicate them to the database until needed.   This allows it to make
better decisions about how SQL DML should be emitted in the transaction based
on a given set of pending changes.   When it does emit SQL to the database
to push out the current set of changes, the process is known as a **flush**.

We can illustrate the flush process manually by calling the [Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush)
method:

```
>>> session.flush()
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[... (insertmanyvalues) 1/2 (ordered; batch not supported)] ('squidward', 'Squidward Tentacles')
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[insertmanyvalues 2/2 (ordered; batch not supported)] ('ehkrabs', 'Eugene H. Krabs')
```

Above we observe the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) was first called upon to emit SQL,
so it created a new transaction and emitted the appropriate INSERT statements
for the two objects.   The transaction now **remains open** until we call any
of the [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit), [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback), or
[Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) methods of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

While [Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush) may be used to manually push out pending
changes to the current transaction, it is usually unnecessary as the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) features a behavior known as **autoflush**, which
we will illustrate later.   It also flushes out changes whenever
[Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) is called.

### Autogenerated primary key attributes

Once the rows are inserted, the two Python objects we’ve created are in a
state known as [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent), where they are associated with the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object in which they were added or loaded, and feature lots of
other behaviors that will be covered later.

Another effect of the INSERT that occurred was that the ORM has retrieved the
new primary key identifiers for each new object; internally it normally uses
the same [CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) accessor we
introduced previously.   The `squidward` and `krabs` objects now have these new
primary key identifiers associated with them and we can view them by accessing
the `id` attribute:

```
>>> squidward.id
4
>>> krabs.id
5
```

Tip

Why did the ORM emit two separate INSERT statements when it could have
used [executemany](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-multiple-parameters)?  As we’ll see in the
next section, the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) when flushing objects always needs to know the
primary key of newly inserted objects.  If a feature such as SQLite’s autoincrement is used
(other examples include PostgreSQL IDENTITY or SERIAL, using sequences,
etc.), the [CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) feature
usually requires that each INSERT is emitted one row at a time.  If we had provided values for the primary keys ahead of
time, the ORM would have been able to optimize the operation better.  Some
database backends such as [psycopg2](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-psycopg2) can also
INSERT many rows at once while still being able to retrieve the primary key
values.

### Getting Objects by Primary Key from the Identity Map

The primary key identity of the objects are significant to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
as the objects are now linked to this identity in memory using a feature
known as the [identity map](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-map).   The identity map is an in-memory store
that links all objects currently loaded in memory to their primary key
identity.   We can observe this by retrieving one of the above objects
using the [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) method, which will return an entry
from the identity map if locally present, otherwise emitting a SELECT:

```
>>> some_squidward = session.get(User, 4)
>>> some_squidward
User(id=4, name='squidward', fullname='Squidward Tentacles')
```

The important thing to note about the identity map is that it maintains a
**unique instance** of a particular Python object per a particular database
identity, within the scope of a particular [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object.  We
may observe that the `some_squidward` refers to the **same object** as that
of `squidward` previously:

```
>>> some_squidward is squidward
True
```

The identity map is a critical feature that allows complex sets of objects
to be manipulated within a transaction without things getting out of sync.

### Committing

There’s much more to say about how the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) works which will
be discussed further.   For now we will commit the transaction so that
we can build up knowledge on how to SELECT rows before examining more ORM
behaviors and features:

```
>>> session.commit()
COMMIT
```

The above operation will commit the transaction that was in progress.  The
objects which we’ve dealt with are still [attached](https://docs.sqlalchemy.org/en/20/glossary.html#term-attached) to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
which is a state they stay in until the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is closed
(which is introduced at [Closing a Session](#tutorial-orm-closing)).

Tip

An important thing to note is that attributes on the objects that we just
worked with have been [expired](https://docs.sqlalchemy.org/en/20/glossary.html#term-expired), meaning, when we next access any
attributes on them, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will start a new transaction and
re-load their state. This option is sometimes problematic for both
performance reasons, or if one wishes to use the objects after closing the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) (which is known as the [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached) state), as they
will not have any state and will have no [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with which to load
that state, leading to “detached instance” errors. The behavior is
controllable using a parameter called [Session.expire_on_commit](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.expire_on_commit).
More on this is at [Closing a Session](#tutorial-orm-closing).

## Updating ORM Objects using the Unit of Work pattern

In the preceding section [Using UPDATE and DELETE Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-core-update-delete), we introduced the
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct that represents a SQL UPDATE statement. When
using the ORM, there are two ways in which this construct is used. The primary
way is that it is emitted automatically as part of the [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work)
process used by the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), where an UPDATE statement is emitted
on a per-primary key basis corresponding to individual objects that have
changes on them.

Supposing we loaded the `User` object for the username `sandy` into
a transaction (also showing off the [Select.filter_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.filter_by) method
as well as the [Result.scalar_one()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalar_one) method):

```
>>> sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('sandy',)
```

The Python object `sandy` as mentioned before acts as a **proxy** for the
row in the database, more specifically the database row **in terms of the
current transaction**, that has the primary key identity of `2`:

```
>>> sandy
User(id=2, name='sandy', fullname='Sandy Cheeks')
```

If we alter the attributes of this object, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) tracks
this change:

```
>>> sandy.fullname = "Sandy Squirrel"
```

The object appears in a collection called [Session.dirty](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.dirty), indicating
the object is “dirty”:

```
>>> sandy in session.dirty
True
```

When the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) next emits a flush, an UPDATE will be emitted
that updates this value in the database.  As mentioned previously, a flush
occurs automatically before we emit any SELECT, using a behavior known as
**autoflush**.  We can query directly for the `User.fullname` column
from this row and we will get our updated value back:

```
>>> sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
UPDATE user_account SET fullname=? WHERE user_account.id = ?
[...] ('Sandy Squirrel', 2)
SELECT user_account.fullname
FROM user_account
WHERE user_account.id = ?
[...] (2,)
>>> print(sandy_fullname)
Sandy Squirrel
```

We can see above that we requested that the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) execute
a single [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) statement.  However the SQL emitted shows
that an UPDATE were emitted as well, which was the flush process pushing
out pending changes.  The `sandy` Python object is now no longer considered
dirty:

```
>>> sandy in session.dirty
False
```

However note we are **still in a transaction** and our changes have not
been pushed to the database’s permanent storage.   Since Sandy’s last name
is in fact “Cheeks” not “Squirrel”, we will repair this mistake later when
we roll back the transaction.  But first we’ll make some more data changes.

See also

[Flushing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)- details the flush process as well as information
about the [Session.autoflush](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.autoflush) setting.

## Deleting ORM Objects using the Unit of Work pattern

To round out the basic persistence operations, an individual ORM object
may be marked for deletion within the [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) process
by using the [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) method.
Let’s load up `patrick` from the database:

```
>>> patrick = session.get(User, 3)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (3,)
```

If we mark `patrick` for deletion, as is the case with other operations,
nothing actually happens yet until a flush proceeds:

```
>>> session.delete(patrick)
```

Current ORM behavior is that `patrick` stays in the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
until the flush proceeds, which as mentioned before occurs if we emit a query:

```
>>> session.execute(select(User).where(User.name == "patrick")).first()
SELECT address.id AS address_id, address.email_address AS address_email_address,
address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id
[...] (3,)
DELETE FROM user_account WHERE user_account.id = ?
[...] (3,)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('patrick',)
```

Above, the SELECT we asked to emit was preceded by a DELETE, which indicated
the pending deletion for `patrick` proceeded.  There was also a `SELECT`
against the `address` table, which was prompted by the ORM looking for rows
in this table which may be related to the target row; this behavior is part of
a behavior known as [cascade](https://docs.sqlalchemy.org/en/20/glossary.html#term-cascade), and can be tailored to work more
efficiently by allowing the database to handle related rows in `address`
automatically; the section [delete](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete) has all the detail on this.

See also

[delete](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete) - describes how to tune the behavior of
[Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) in terms of how related rows in other tables
should be handled.

Beyond that, the `patrick` object instance now being deleted is no longer
considered to be persistent within the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), as is shown
by the containment check:

```
>>> patrick in session
False
```

However just like the UPDATEs we made to the `sandy` object, every change
we’ve made here is local to an ongoing transaction, which won’t become
permanent if we don’t commit it.  As rolling the transaction back is actually
more interesting at the moment, we will do that in the next section.

## Bulk / Multi Row INSERT, upsert, UPDATE and DELETE

The [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) techniques discussed in this section
are intended to integrate [dml](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML), or INSERT/UPDATE/DELETE statements,
with Python object mechanics, often involving complex graphs of
inter-related objects.  Once objects are added to a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) using
[Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add), the unit of work process transparently emits
INSERT/UPDATE/DELETE on our behalf as attributes on our objects are created
and modified.

However, the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) also has the ability to process commands
that allow it to emit INSERT, UPDATE and DELETE statements directly without
being passed any ORM-persisted objects, instead being passed lists of values to
be INSERTed, UPDATEd, or upserted, or WHERE criteria so that an UPDATE or
DELETE statement that matches many rows at once can be invoked. This mode of
use is of particular importance when large numbers of rows must be affected
without the need to construct and manipulate mapped objects, which may be
cumbersome and unnecessary for simplistic, performance-intensive tasks such as
large bulk inserts.

The Bulk / Multi row features of the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) make use of the
[insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert), [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) and [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) constructs
directly, and their usage resembles how they are used with SQLAlchemy Core
(first introduced in this tutorial at [Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert) and
[Using UPDATE and DELETE Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-core-update-delete)).  When using these constructs
with the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) instead of a plain [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection),
their construction, execution and result handling is fully integrated with the ORM.

For background and examples on using these features, see the section
[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete) in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).

See also

[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

## Rolling Back

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has a [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) method that as
expected emits a ROLLBACK on the SQL connection in progress.  However, it also
has an effect on the objects that are currently associated with the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), in our previous example the Python object `sandy`.
While we changed the `.fullname` of the `sandy` object to read `"Sandy
Squirrel"`, we want to roll back this change.   Calling
[Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) will not only roll back the transaction but also
**expire** all objects currently associated with this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
which will have the effect that they will refresh themselves when next accessed
using a process known as [lazy loading](https://docs.sqlalchemy.org/en/20/glossary.html#term-lazy-loading):

```
>>> session.rollback()
ROLLBACK
```

To view the “expiration” process more closely, we may observe that the
Python object `sandy` has no state left within its Python `__dict__`,
with the exception of a special SQLAlchemy internal state object:

```
>>> sandy.__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x...>}
```

This is the “[expired](https://docs.sqlalchemy.org/en/20/glossary.html#term-expired)” state; accessing the attribute again will autobegin
a new transaction and refresh `sandy` with the current database row:

```
>>> sandy.fullname
BEGIN (implicit)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (2,)
'Sandy Cheeks'
```

We may now observe that the full database row was also populated into the
`__dict__` of the `sandy` object:

```
>>> sandy.__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x...>,
 'id': 2, 'name': 'sandy', 'fullname': 'Sandy Cheeks'}
```

For deleted objects, when we earlier noted that `patrick` was no longer
in the session, that object’s identity is also restored:

```
>>> patrick in session
True
```

and of course the database data is present again as well:

```
>>> session.execute(select(User).where(User.name == "patrick")).scalar_one() is patrick
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('patrick',)
True
```

## Closing a Session

Within the above sections we used a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object outside
of a Python context manager, that is, we didn’t use the `with` statement.
That’s fine, however if we are doing things this way, it’s best that we explicitly
close out the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) when we are done with it:

```
>>> session.close()
ROLLBACK
```

Closing the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), which is what happens when we use it in
a context manager as well, accomplishes the following things:

- It [releases](https://docs.sqlalchemy.org/en/20/glossary.html#term-releases) all connection resources to the connection pool, cancelling
  out (e.g. rolling back) any transactions that were in progress.
  This means that when we make use of a session to perform some read-only
  tasks and then close it, we don’t need to explicitly call upon
  [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) to make sure the transaction is rolled back;
  the connection pool handles this.
- It **expunges** all objects from the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
  This means that all the Python objects we had loaded for this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
  like `sandy`, `patrick` and `squidward`, are now in a state known
  as [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached).  In particular, we will note that objects that were still
  in an [expired](https://docs.sqlalchemy.org/en/20/glossary.html#term-expired) state, for example due to the call to [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit),
  are now non-functional, as they don’t contain the state of a current row and
  are no longer associated with any database transaction in which to be
  refreshed:
  ```
  # note that 'squidward.name' was just expired previously, so its value is unloaded
  >>> squidward.name
  Traceback (most recent call last):
    ...
  sqlalchemy.orm.exc.DetachedInstanceError: Instance <User at 0x...> is not bound to a Session; attribute refresh operation cannot proceed
  ```
  The detached objects can be re-associated with the same, or a new
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) using the [Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) method, which
  will re-establish their relationship with their particular database row:
  ```
  >>> session.add(squidward)
  >>> squidward.name
  BEGIN (implicit)
  SELECT user_account.id AS user_account_id, user_account.name AS user_account_name, user_account.fullname AS user_account_fullname
  FROM user_account
  WHERE user_account.id = ?
  [...] (4,)
  'squidward'
  ```
  Tip
  Try to avoid using objects in their detached state, if possible. When the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is closed, clean up references to all the
  previously attached objects as well.   For cases where detached objects
  are necessary, typically the immediate display of just-committed objects
  for a web application where the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is closed before
  the view is rendered, set the [Session.expire_on_commit](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.expire_on_commit)
  flag to `False`.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html)
