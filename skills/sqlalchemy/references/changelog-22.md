# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# What’s New in SQLAlchemy 1.1?

About this Document

This document describes changes between SQLAlchemy version 1.0
and SQLAlchemy version 1.1.

## Introduction

This guide introduces what’s new in SQLAlchemy version 1.1,
and also documents changes which affect users migrating
their applications from the 1.0 series of SQLAlchemy to 1.1.

Please carefully review the sections on behavioral changes for
potentially backwards-incompatible changes in behavior.

## Platform / Installer Changes

### Setuptools is now required for install

SQLAlchemy’s `setup.py` file has for many years supported operation
both with Setuptools installed and without; supporting a “fallback” mode
that uses straight Distutils.  As a Setuptools-less Python environment is
now unheard of, and in order to support the featureset of Setuptools
more fully, in particular to support py.test’s integration with it as well
as things like “extras”, `setup.py` now depends on Setuptools fully.

See also

[Installation Guide](https://docs.sqlalchemy.org/en/20/intro.html#installation)

[#3489](https://www.sqlalchemy.org/trac/ticket/3489)

### Enabling / Disabling C Extension builds is only via environment variable

The C Extensions build by default during install as long as it is possible.
To disable C extension builds, the `DISABLE_SQLALCHEMY_CEXT` environment
variable was made available as of SQLAlchemy 0.8.6 / 0.9.4.  The previous
approach of using the `--without-cextensions` argument has been removed,
as it relies on deprecated features of setuptools.

See also

[Building the Cython Extensions](https://docs.sqlalchemy.org/en/20/intro.html#c-extensions)

[#3500](https://www.sqlalchemy.org/trac/ticket/3500)

## New Features and Improvements - ORM

### New Session lifecycle events

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has long supported events that allow some degree
of tracking of state changes to objects, including
[SessionEvents.before_attach()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.before_attach), [SessionEvents.after_attach()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.after_attach),
and [SessionEvents.before_flush()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.before_flush).  The Session documentation also
documents major object states at [Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states).  However,
there has never been system of tracking objects specifically as they
pass through these transitions.  Additionally, the status of “deleted” objects
has historically been murky as the objects act somewhere between
the “persistent” and “detached” states.

To clean up this area and allow the realm of session state transition
to be fully transparent, a new series of events have been added that
are intended to cover every possible way that an object might transition
between states, and additionally the “deleted” status has been given
its own official state name within the realm of session object states.

#### New State Transition Events

Transitions between all states of an object such as [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent),
[pending](https://docs.sqlalchemy.org/en/20/glossary.html#term-pending) and others can now be intercepted in terms of a
session-level event intended to cover a specific transition.
Transitions as objects move into a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), move out of a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), and even all the transitions which occur when the
transaction is rolled back using [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback)
are explicitly present in the interface of [SessionEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents).

In total, there are **ten new events**.  A summary of these events is in a
newly written documentation section [Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#session-lifecycle-events).

#### New Object State “deleted” is added, deleted objects no longer “persistent”

The [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent) state of an object in the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has
always been documented as an object that has a valid database identity;
however in the case of objects that were deleted within a flush, they
have always been in a grey area where they are not really “detached”
from the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) yet, because they can still be restored
within a rollback, but are not really “persistent” because their database
identity has been deleted and they aren’t present in the identity map.

To resolve this grey area given the new events, a new object state
[deleted](https://docs.sqlalchemy.org/en/20/glossary.html#term-deleted) is introduced.  This state exists between the “persistent” and
“detached” states.  An object that is marked for deletion via
[Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) remains in the “persistent” state until a flush
proceeds; at that point, it is removed from the identity map, moves
to the “deleted” state, and the [SessionEvents.persistent_to_deleted()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.persistent_to_deleted)
hook is invoked.  If the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s transaction is rolled
back, the object is restored as persistent; the
[SessionEvents.deleted_to_persistent()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.deleted_to_persistent) transition is called.  Otherwise
if the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s transaction is committed,
the [SessionEvents.deleted_to_detached()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.deleted_to_detached) transition is invoked.

Additionally, the [InstanceState.persistent](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.persistent) accessor **no longer returns
True** for an object that is in the new “deleted” state; instead, the
[InstanceState.deleted](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.deleted) accessor has been enhanced to reliably
report on this new state.   When the object is detached, the [InstanceState.deleted](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.deleted)
returns False and the [InstanceState.detached](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.detached) accessor is True
instead.  To determine if an object was deleted either in the current
transaction or in a previous transaction, use the
[InstanceState.was_deleted](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.was_deleted) accessor.

#### Strong Identity Map is Deprecated

One of the inspirations for the new series of transition events was to enable
leak-proof tracking of objects as they move in and out of the identity map,
so that a “strong reference” may be maintained mirroring the object
moving in and out of this map.  With this new capability, there is no longer
any need for the [Session.weak_identity_map](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.weak_identity_map) parameter and the
corresponding `StrongIdentityMap` object.  This option has remained
in SQLAlchemy for many years as the “strong-referencing” behavior used to be
the only behavior available, and many applications were written to assume
this behavior.   It has long been recommended that strong-reference tracking
of objects not be an intrinsic job of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and instead
be an application-level construct built as needed by the application; the
new event model allows even the exact behavior of the strong identity map
to be replicated.   See [Session Referencing Behavior](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-referencing-behavior) for a new
recipe illustrating how to replace the strong identity map.

[#2677](https://www.sqlalchemy.org/trac/ticket/2677)

### New init_scalar() event intercepts default values at ORM level

The ORM produces a value of `None` when an attribute that has not been
set is first accessed, for a non-persistent object:

```
>>> obj = MyObj()
>>> obj.some_value
None
```

There’s a use case for this in-Python value to correspond to that of a
Core-generated default value, even before the object is persisted.
To suit this use case a new event [AttributeEvents.init_scalar()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.init_scalar)
is added.   The new example `active_column_defaults.py` at
[Attribute Instrumentation](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-instrumentation) illustrates a sample use, so the effect
can instead be:

```
>>> obj = MyObj()
>>> obj.some_value
"my default"
```

[#1311](https://www.sqlalchemy.org/trac/ticket/1311)

### Changes regarding “unhashable” types, impacts deduping of ORM rows

The [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object has a well-known behavior of “deduping”
returned rows that contain at least one ORM-mapped entity (e.g., a
full mapped object, as opposed to individual column values). The
primary purpose of this is so that the handling of entities works
smoothly in conjunction with the identity map, including to
accommodate for the duplicate entities normally represented within
joined eager loading, as well as when joins are used for the purposes
of filtering on additional columns.

This deduplication relies upon the hashability of the elements within
the row.  With the introduction of PostgreSQL’s special types like
[ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY), [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE) and
[JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON), the experience of types within rows being
unhashable and encountering problems here is more prevalent than
it was previously.

In fact, SQLAlchemy has since version 0.8 included a flag on datatypes that
are noted as “unhashable”, however this flag was not used consistently
on built in types.  As described in [ARRAY and JSON types now correctly specify “unhashable”](#change-3499-postgresql), this
flag is now set consistently for all of PostgreSQL’s “structural” types.

The “unhashable” flag is also set on the [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType) type,
as [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType) is used to refer to any expression of unknown
type.

Since [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType) is applied to most
usages of `func`, as `func` doesn’t actually know anything
about the function names given in most cases, **using func() will
often disable row deduping unless explicit typing is applied**.
The following examples illustrate `func.substr()` applied to a string
expression, and `func.date()` applied to a datetime expression; both
examples will return duplicate rows due to the joined eager load unless
explicit typing is applied:

```
result = (
    session.query(func.substr(A.some_thing, 0, 4), A).options(joinedload(A.bs)).all()
)

users = (
    session.query(
        func.date(User.date_created, "start of month").label("month"),
        User,
    )
    .options(joinedload(User.orders))
    .all()
)
```

The above examples, in order to retain deduping, should be specified as:

```
result = (
    session.query(func.substr(A.some_thing, 0, 4, type_=String), A)
    .options(joinedload(A.bs))
    .all()
)

users = (
    session.query(
        func.date(User.date_created, "start of month", type_=DateTime).label("month"),
        User,
    )
    .options(joinedload(User.orders))
    .all()
)
```

Additionally, the treatment of a so-called “unhashable” type is slightly
different than its been in previous releases; internally we are using
the `id()` function to get a “hash value” from these structures, just
as we would any ordinary mapped object.   This replaces the previous
approach which applied a counter to the object.

[#3499](https://www.sqlalchemy.org/trac/ticket/3499)

### Specific checks added for passing mapped classes, instances as SQL literals

The typing system now has specific checks for passing of SQLAlchemy
“inspectable” objects in contexts where they would otherwise be handled as
literal values.   Any SQLAlchemy built-in object that is legal to pass as a
SQL value (which is not already a [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) instance)
includes a method `__clause_element__()` which provides a
valid SQL expression for that object.  For SQLAlchemy objects that
don’t provide this, such as mapped classes, mappers, and mapped
instances, a more informative error message is emitted rather than
allowing the DBAPI to receive the object and fail later.  An example
is illustrated below, where a string-based attribute `User.name` is
compared to a full instance of `User()`, rather than against a
string value:

```
>>> some_user = User()
>>> q = s.query(User).filter(User.name == some_user)
sqlalchemy.exc.ArgumentError: Object <__main__.User object at 0x103167e90> is not legal as a SQL literal value
```

The exception is now immediate when the comparison is made between
`User.name == some_user`.  Previously, a comparison like the above
would produce a SQL expression that would only fail once resolved
into a DBAPI execution call; the mapped `User` object would
ultimately become a bound parameter that would be rejected by the
DBAPI.

Note that in the above example, the expression fails because
`User.name` is a string-based (e.g. column oriented) attribute.
The change does *not* impact the usual case of comparing a many-to-one
relationship attribute to an object, which is handled distinctly:

```
>>> # Address.user refers to the User mapper, so
>>> # this is of course still OK!
>>> q = s.query(Address).filter(Address.user == some_user)
```

[#3321](https://www.sqlalchemy.org/trac/ticket/3321)

### New Indexable ORM extension

The [Indexable](https://docs.sqlalchemy.org/en/20/orm/extensions/indexable.html) extension is an extension to the hybrid
attribute feature which allows the construction of attributes which
refer to specific elements of an “indexable” data type, such as an array
or JSON field:

```
class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    data = Column(JSON)

    name = index_property("data", "name")
```

Above, the `name` attribute will read/write the field `"name"`
from the JSON column `data`, after initializing it to an
empty dictionary:

```
>>> person = Person(name="foobar")
>>> person.name
foobar
```

The extension also triggers a change event when the attribute is modified,
so that there’s no need to use [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict) in order
to track this change.

See also

[Indexable](https://docs.sqlalchemy.org/en/20/orm/extensions/indexable.html)

### New options allowing explicit persistence of NULL over a default

Related to the new JSON-NULL support added to PostgreSQL as part of
[JSON “null” is inserted as expected with ORM operations, omitted when not present](#change-3514), the base [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class now supports
a method [TypeEngine.evaluates_none()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.evaluates_none) which allows a positive set
of the `None` value on an attribute to be persisted as NULL, rather than
omitting the column from the INSERT statement, which has the effect of using
the column-level default.  This allows a mapper-level
configuration of the existing object-level technique of assigning
[null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) to the attribute.

See also

[Forcing NULL on a column with a default](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#session-forcing-null)

[#3250](https://www.sqlalchemy.org/trac/ticket/3250)

### Further Fixes to single-table inheritance querying

Continuing from 1.0’s [Change to single-table-inheritance criteria when using from_self(), count()](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#migration-3177), the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) should
no longer inappropriately add the “single inheritance” criteria when the
query is against a subquery expression such as an exists:

```
class Widget(Base):
    __tablename__ = "widget"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    data = Column(String)
    __mapper_args__ = {"polymorphic_on": type}

class FooWidget(Widget):
    __mapper_args__ = {"polymorphic_identity": "foo"}

q = session.query(FooWidget).filter(FooWidget.data == "bar").exists()

session.query(q).all()
```

Produces:

```
SELECT EXISTS (SELECT 1
FROM widget
WHERE widget.data = :data_1 AND widget.type IN (:type_1)) AS anon_1
```

The IN clause on the inside is appropriate, in order to limit to FooWidget
objects, however previously the IN clause would also be generated a second
time on the outside of the subquery.

[#3582](https://www.sqlalchemy.org/trac/ticket/3582)

### Improved Session state when a SAVEPOINT is cancelled by the database

A common case with MySQL is that a SAVEPOINT is cancelled when a deadlock
occurs within the transaction.  The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has been modified
to deal with this failure mode slightly more gracefully, such that the
outer, non-savepoint transaction still remains usable:

```
s = Session()
s.begin_nested()

s.add(SomeObject())

try:
    # assume the flush fails, flush goes to rollback to the
    # savepoint and that also fails
    s.flush()
except Exception as err:
    print("Something broke, and our SAVEPOINT vanished too")

# this is the SAVEPOINT transaction, marked as
# DEACTIVE so the rollback() call succeeds
s.rollback()

# this is the outermost transaction, remains ACTIVE
# so rollback() or commit() can succeed
s.rollback()
```

This issue is a continuation of [#2696](https://www.sqlalchemy.org/trac/ticket/2696) where we emit a warning
so that the original error can be seen when running on Python 2, even though
the SAVEPOINT exception takes precedence.  On Python 3, exceptions are chained
so both failures are reported individually.

[#3680](https://www.sqlalchemy.org/trac/ticket/3680)

### Erroneous “new instance X conflicts with persistent instance Y” flush errors fixed

The [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) method is responsible for removing objects
that were INSERTed into the database, e.g. moved from pending to persistent,
within that now rolled-back transaction.   Objects that make this state
change are tracked in a weak-referencing collection, and if an object is
garbage collected from that collection, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) no longer worries
about it (it would otherwise not scale for operations that insert many new
objects within a transaction).  However, an issue arises if the application
re-loads that same garbage-collected row within the transaction, before the
rollback occurs; if a strong reference to this object remains into the next
transaction, the fact that this object was not inserted and should be
removed would be lost, and the flush would incorrectly raise an error:

```
from sqlalchemy import Column, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)

e = create_engine("sqlite://", echo=True)
Base.metadata.create_all(e)

s = Session(e)

# persist an object
s.add(A(id=1))
s.flush()

# rollback buffer loses reference to A

# load it again, rollback buffer knows nothing
# about it
a1 = s.query(A).first()

# roll back the transaction; all state is expired but the
# "a1" reference remains
s.rollback()

# previous "a1" conflicts with the new one because we aren't
# checking that it never got committed
s.add(A(id=1))
s.commit()
```

The above program would raise:

```
FlushError: New instance <User at 0x7f0287eca4d0> with identity key
(<class 'test.orm.test_transaction.User'>, ('u1',)) conflicts
with persistent instance <User at 0x7f02889c70d0>
```

The bug is that when the above exception is raised, the unit of work
is operating upon the original object assuming it’s a live row, when in
fact the object is expired and upon testing reveals that it’s gone.  The
fix tests this condition now, so in the SQL log we see:

```
BEGIN (implicit)

INSERT INTO a (id) VALUES (?)
(1,)

SELECT a.id AS a_id FROM a LIMIT ? OFFSET ?
(1, 0)

ROLLBACK

BEGIN (implicit)

SELECT a.id AS a_id FROM a WHERE a.id = ?
(1,)

INSERT INTO a (id) VALUES (?)
(1,)

COMMIT
```

Above, the unit of work now does a SELECT for the row we’re about to report
as a conflict for, sees that it doesn’t exist, and proceeds normally.
The expense of this SELECT is only incurred in the case when we would have
erroneously raised an exception in any case.

[#3677](https://www.sqlalchemy.org/trac/ticket/3677)

### passive_deletes feature for joined-inheritance mappings

A joined-table inheritance mapping may now allow a DELETE to proceed
as a result of [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete), which only emits DELETE for the
base table, and not the subclass table, allowing configured ON DELETE CASCADE
to take place for the configured foreign keys.  This is configured using
the `mapper.passive_deletes` option:

```
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class A(Base):
    __tablename__ = "a"
    id = Column("id", Integer, primary_key=True)
    type = Column(String)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "a",
        "passive_deletes": True,
    }

class B(A):
    __tablename__ = "b"
    b_table_id = Column("b_table_id", Integer, primary_key=True)
    bid = Column("bid", Integer, ForeignKey("a.id", ondelete="CASCADE"))
    data = Column("data", String)

    __mapper_args__ = {"polymorphic_identity": "b"}
```

With the above mapping, the `mapper.passive_deletes` option
is configured on the base mapper; it takes effect for all non-base mappers
that are descendants of the mapper with the option set.  A DELETE for
an object of type `B` no longer needs to retrieve the primary key value
of `b_table_id` if unloaded, nor does it need to emit a DELETE statement
for the table itself:

```
session.delete(some_b)
session.commit()
```

Will emit SQL as:

```
DELETE FROM a WHERE a.id = %(id)s
-- {'id': 1}
COMMIT
```

As always, the target database must have foreign key support with
ON DELETE CASCADE enabled.

[#2349](https://www.sqlalchemy.org/trac/ticket/2349)

### Same-named backrefs will not raise an error when applied to concrete inheritance subclasses

The following mapping has always been possible without issue:

```
class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)
    b = relationship("B", foreign_keys="B.a_id", backref="a")

class A1(A):
    __tablename__ = "a1"
    id = Column(Integer, primary_key=True)
    b = relationship("B", foreign_keys="B.a1_id", backref="a1")
    __mapper_args__ = {"concrete": True}

class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)

    a_id = Column(ForeignKey("a.id"))
    a1_id = Column(ForeignKey("a1.id"))
```

Above, even though class `A` and class `A1` have a relationship
named `b`, no conflict warning or error occurs because class `A1` is
marked as “concrete”.

However, if the relationships were configured the other way, an error
would occur:

```
class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)

class A1(A):
    __tablename__ = "a1"
    id = Column(Integer, primary_key=True)
    __mapper_args__ = {"concrete": True}

class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)

    a_id = Column(ForeignKey("a.id"))
    a1_id = Column(ForeignKey("a1.id"))

    a = relationship("A", backref="b")
    a1 = relationship("A1", backref="b")
```

The fix enhances the backref feature so that an error is not emitted,
as well as an additional check within the mapper logic to bypass warning
for an attribute being replaced.

[#3630](https://www.sqlalchemy.org/trac/ticket/3630)

### Same-named relationships on inheriting mappers no longer warn

When creating two mappers in an inheritance scenario, placing a relationship
on both with the same name would emit the warning
“relationship ‘<name>’ on mapper <name> supersedes the same relationship
on inherited mapper ‘<name>’; this can cause dependency issues during flush”.
An example is as follows:

```
class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)
    bs = relationship("B")

class ASub(A):
    __tablename__ = "a_sub"
    id = Column(Integer, ForeignKey("a.id"), primary_key=True)
    bs = relationship("B")

class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id = Column(ForeignKey("a.id"))
```

This warning dates back to the 0.4 series in 2007 and is based on a version of
the unit of work code that has since been entirely rewritten. Currently, there
is no known issue with the same-named relationships being placed on a base
class and a descendant class, so the warning is lifted.   However, note that
this use case is likely not prevalent in real world use due to the warning.
While rudimentary test support is added for this use case, it is possible that
some new issue with this pattern may be identified.

Added in version 1.1.0b3.

[#3749](https://www.sqlalchemy.org/trac/ticket/3749)

### Hybrid properties and methods now propagate the docstring as well as .info

A hybrid method or property will now reflect the `__doc__` value
present in the original docstring:

```
class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)

    name = Column(String)

    @hybrid_property
    def some_name(self):
        """The name field"""
        return self.name
```

The above value of `A.some_name.__doc__` is now honored:

```
>>> A.some_name.__doc__
The name field
```

However, to accomplish this, the mechanics of hybrid properties necessarily
becomes more complex.  Previously, the class-level accessor for a hybrid
would be a simple pass-through, that is, this test would succeed:

```
>>> assert A.name is A.some_name
```

With the change, the expression returned by `A.some_name` is wrapped inside
of its own `QueryableAttribute` wrapper:

```
>>> A.some_name
<sqlalchemy.orm.attributes.hybrid_propertyProxy object at 0x7fde03888230>
```

A lot of testing went into making sure this wrapper works correctly, including
for elaborate schemes like that of the
[Custom Value Object](https://techspot.zzzeek.org/2011/10/21/hybrids-and-value-agnostic-types/)
recipe, however we’ll be looking to see that no other regressions occur for
users.

As part of this change, the `hybrid_property.info` collection is now
also propagated from the hybrid descriptor itself, rather than from the underlying
expression.  That is, accessing `A.some_name.info` now returns the same
dictionary that you’d get from `inspect(A).all_orm_descriptors['some_name'].info`:

```
>>> A.some_name.info["foo"] = "bar"
>>> from sqlalchemy import inspect
>>> inspect(A).all_orm_descriptors["some_name"].info
{'foo': 'bar'}
```

Note that this `.info` dictionary is **separate** from that of a mapped attribute
which the hybrid descriptor may be proxying directly; this is a behavioral
change from 1.0.   The wrapper will still proxy other useful attributes
of a mirrored attribute such as `QueryableAttribute.property` and
`QueryableAttribute.class_`.

[#3653](https://www.sqlalchemy.org/trac/ticket/3653)

### Session.merge resolves pending conflicts the same as persistent

The [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) method will now track the identities of objects given
within a graph to maintain primary key uniqueness before emitting an INSERT.
When duplicate objects of the same identity are encountered, non-primary-key
attributes are **overwritten** as the objects are encountered, which is
essentially non-deterministic.   This behavior matches that of how persistent
objects, that is objects that are already located in the database via
primary key, are already treated, so this behavior is more internally
consistent.

Given:

```
u1 = User(id=7, name="x")
u1.orders = [
    Order(description="o1", address=Address(id=1, email_address="a")),
    Order(description="o2", address=Address(id=1, email_address="b")),
    Order(description="o3", address=Address(id=1, email_address="c")),
]

sess = Session()
sess.merge(u1)
```

Above, we merge a `User` object with three new `Order` objects, each referring to
a distinct `Address` object, however each is given the same primary key.
The current behavior of [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) is to look in the identity
map for this `Address` object, and use that as the target.   If the object
is present, meaning that the database already has a row for `Address` with
primary key “1”, we can see that the `email_address` field of the `Address`
will be overwritten three times, in this case with the values a, b and finally
c.

However, if the `Address` row for primary key “1” were not present, [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge)
would instead create three separate `Address` instances, and we’d then get
a primary key conflict upon INSERT.  The new behavior is that the proposed
primary key for these `Address` objects are tracked in a separate dictionary
so that we merge the state of the three proposed `Address` objects onto
one `Address` object to be inserted.

It may have been preferable if the original case emitted some kind of warning
that conflicting data were present in a single merge-tree, however the
non-deterministic merging of values has been the behavior for many
years for the persistent case; it now matches for the pending case.   A
feature that warns for conflicting values could still be feasible for both
cases but would add considerable performance overhead as each column value
would have to be compared during the merge.

[#3601](https://www.sqlalchemy.org/trac/ticket/3601)

### Fix involving many-to-one object moves with user-initiated foreign key manipulations

A bug has been fixed involving the mechanics of replacing a many-to-one
reference to an object with another object.   During the attribute operation,
the location of the object that was previously referred to now makes use of the
database-committed foreign key value, rather than the current foreign key
value.  The main effect of the fix is that a backref event towards a collection
will fire off more accurately when a many-to-one change is made, even if the
foreign key attribute was manually moved to the new value beforehand.  Assume a
mapping of the classes `Parent` and `SomeClass`, where `SomeClass.parent`
refers to `Parent` and `Parent.items` refers to the collection of
`SomeClass` objects:

```
some_object = SomeClass()
session.add(some_object)
some_object.parent_id = some_parent.id
some_object.parent = some_parent
```

Above, we’ve made a pending object `some_object`, manipulated its foreign key
towards `Parent` to refer to it, *then* we actually set up the relationship.
Before the bug fix, the backref would not have fired off:

```
# before the fix
assert some_object not in some_parent.items
```

The fix now is that when we seek to locate the previous value of
`some_object.parent`, we disregard the parent id that’s been manually set,
and we look for the database-committed value.  In this case, it’s None because
the object is pending, so the event system logs `some_object.parent`
as a net change:

```
# after the fix, backref fired off for some_object.parent = some_parent
assert some_object in some_parent.items
```

While it is discouraged to manipulate foreign key attributes that are managed
by relationships, there is limited support for this use case.  Applications
that manipulate foreign keys in order to allow loads to proceed will often make
use of the [Session.enable_relationship_loading()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.enable_relationship_loading) and
`RelationshipProperty.load_on_pending` features, which cause
relationships to emit lazy loads based on in-memory foreign key values that
aren’t persisted.   Whether or not these features are in use, this behavioral
improvement will now be apparent.

[#3708](https://www.sqlalchemy.org/trac/ticket/3708)

### Improvements to the Query.correlate method with polymorphic entities

In recent SQLAlchemy versions, the SQL generated by many forms of
“polymorphic” queries has a more “flat” form than it used to, where
a JOIN of several tables is no longer bundled into a subquery unconditionally.
To accommodate this, the [Query.correlate()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.correlate) method now extracts the
individual tables from such a polymorphic selectable and ensures that all
are part of the “correlate” for the subquery.  Assuming the
`Person/Manager/Engineer->Company` setup from the mapping documentation,
using with_polymorphic:

```
sess.query(Person.name).filter(
    sess.query(Company.name)
    .filter(Company.company_id == Person.company_id)
    .correlate(Person)
    .as_scalar()
    == "Elbonia, Inc."
)
```

The above query now produces:

```
SELECT people.name AS people_name
FROM people
LEFT OUTER JOIN engineers ON people.person_id = engineers.person_id
LEFT OUTER JOIN managers ON people.person_id = managers.person_id
WHERE (SELECT companies.name
FROM companies
WHERE companies.company_id = people.company_id) = ?
```

Before the fix, the call to `correlate(Person)` would inadvertently
attempt to correlate to the join of `Person`, `Engineer` and `Manager`
as a single unit, so `Person` wouldn’t be correlated:

```
-- old, incorrect query
SELECT people.name AS people_name
FROM people
LEFT OUTER JOIN engineers ON people.person_id = engineers.person_id
LEFT OUTER JOIN managers ON people.person_id = managers.person_id
WHERE (SELECT companies.name
FROM companies, people
WHERE companies.company_id = people.company_id) = ?
```

Using correlated subqueries against polymorphic mappings still has some
unpolished edges.  If for example `Person` is polymorphically linked
to a so-called “concrete polymorphic union” query, the above subquery
may not correctly refer to this subquery.  In all cases, a way to refer
to the “polymorphic” entity fully is to create an [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) object
from it first:

```
# works with all SQLAlchemy versions and all types of polymorphic
# aliasing.

paliased = aliased(Person)
sess.query(paliased.name).filter(
    sess.query(Company.name)
    .filter(Company.company_id == paliased.company_id)
    .correlate(paliased)
    .as_scalar()
    == "Elbonia, Inc."
)
```

The [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct guarantees that the “polymorphic selectable”
is wrapped in a subquery.  By referring to it explicitly in the correlated
subquery, the polymorphic form is correctly used.

[#3662](https://www.sqlalchemy.org/trac/ticket/3662)

### Stringify of Query will consult the Session for the correct dialect

Calling `str()` on a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object will consult the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
for the correct “bind” to use, in order to render the SQL that would be
passed to the database.  In particular this allows a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) that
refers to dialect-specific SQL constructs to be renderable, assuming the
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) is associated with an appropriate [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
Previously, this behavior would only take effect if the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
to which the mappings were associated were itself bound to the target
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).

If neither the underlying [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) nor the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) are
associated with any bound [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), then the fallback to the
“default” dialect is used to generate the SQL string.

See also

[“Friendly” stringification of Core SQL constructs without a dialect](#change-3631)

[#3081](https://www.sqlalchemy.org/trac/ticket/3081)

### Joined eager loading where the same entity is present multiple times in one row

A fix has been made to the case has been made whereby an attribute will be
loaded via joined eager loading, even if the entity was already loaded from the
row on a different “path” that doesn’t include the attribute.  This is a
deep use case that’s hard to reproduce, but the general idea is as follows:

```
class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)
    b_id = Column(ForeignKey("b.id"))
    c_id = Column(ForeignKey("c.id"))

    b = relationship("B")
    c = relationship("C")

class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    c_id = Column(ForeignKey("c.id"))

    c = relationship("C")

class C(Base):
    __tablename__ = "c"
    id = Column(Integer, primary_key=True)
    d_id = Column(ForeignKey("d.id"))
    d = relationship("D")

class D(Base):
    __tablename__ = "d"
    id = Column(Integer, primary_key=True)

c_alias_1 = aliased(C)
c_alias_2 = aliased(C)

q = s.query(A)
q = q.join(A.b).join(c_alias_1, B.c).join(c_alias_1.d)
q = q.options(
    contains_eager(A.b).contains_eager(B.c, alias=c_alias_1).contains_eager(C.d)
)
q = q.join(c_alias_2, A.c)
q = q.options(contains_eager(A.c, alias=c_alias_2))
```

The above query emits SQL like this:

```
SELECT
    d.id AS d_id,
    c_1.id AS c_1_id, c_1.d_id AS c_1_d_id,
    b.id AS b_id, b.c_id AS b_c_id,
    c_2.id AS c_2_id, c_2.d_id AS c_2_d_id,
    a.id AS a_id, a.b_id AS a_b_id, a.c_id AS a_c_id
FROM
    a
    JOIN b ON b.id = a.b_id
    JOIN c AS c_1 ON c_1.id = b.c_id
    JOIN d ON d.id = c_1.d_id
    JOIN c AS c_2 ON c_2.id = a.c_id
```

We can see that the `c` table is selected from twice; once in the context
of `A.b.c -> c_alias_1` and another in the context of `A.c -> c_alias_2`.
Also, we can see that it is quite possible that the `C` identity for a
single row is the **same** for both `c_alias_1` and `c_alias_2`, meaning
two sets of columns in one row result in only one new object being added
to the identity map.

The query options above only call for the attribute `C.d` to be loaded
in the context of `c_alias_1`, and not `c_alias_2`.  So whether or not
the final `C` object we get in the identity map has the `C.d` attribute
loaded depends on how the mappings are traversed, which while not completely
random, is essentially non-deterministic.   The fix is that even if the
loader for `c_alias_1` is processed after that of `c_alias_2` for a
single row where they both refer to the same identity, the `C.d`
element will still be loaded.  Previously, the loader did not seek to
modify the load of an entity that was already loaded via a different path.
The loader that reaches the entity first has always been non-deterministic,
so this fix may be detectable as a behavioral change in some situations and
not others.

The fix includes tests for two variants of the “multiple paths to one entity”
case, and the fix should hopefully cover all other scenarios of this nature.

[#3431](https://www.sqlalchemy.org/trac/ticket/3431)

### New MutableList and MutableSet helpers added to the mutation tracking extension

New helper classes [MutableList](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList) and [MutableSet](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableSet) have been
added to the [Mutation Tracking](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html) extension, to complement the existing
[MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict) helper.

[#3297](https://www.sqlalchemy.org/trac/ticket/3297)

### New “raise” / “raise_on_sql” loader strategies

To assist with the use case of preventing unwanted lazy loads from occurring
after a series of objects are loaded, the new “lazy=’raise’” and
“lazy=’raise_on_sql’” strategies and
corresponding loader option [raiseload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.raiseload) may be applied to a
relationship attribute which will cause it to raise `InvalidRequestError`
when a non-eagerly-loaded attribute is accessed for read.  The two variants
test for either a lazy load of any variety, including those that would
only return None or retrieve from the identity map:

```
>>> from sqlalchemy.orm import raiseload
>>> a1 = s.query(A).options(raiseload(A.some_b)).first()
>>> a1.some_b
Traceback (most recent call last):
...
sqlalchemy.exc.InvalidRequestError: 'A.some_b' is not available due to lazy='raise'
```

Or a lazy load only where SQL would be emitted:

```
>>> from sqlalchemy.orm import raiseload
>>> a1 = s.query(A).options(raiseload(A.some_b, sql_only=True)).first()
>>> a1.some_b
Traceback (most recent call last):
...
sqlalchemy.exc.InvalidRequestError: 'A.bs' is not available due to lazy='raise_on_sql'
```

[#3512](https://www.sqlalchemy.org/trac/ticket/3512)

### Mapper.order_by is deprecated

This old parameter from the very first versions of SQLAlchemy was part of
the original design of the ORM which featured the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object
as a public-facing query structure.   This role has long since been replaced
by the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object, where we use [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) to
indicate the ordering of results in a way that works consistently for any
combination of SELECT statements, entities and SQL expressions.   There are
many areas in which [Mapper.order_by](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.order_by) doesn’t work as expected
(or what would be expected is not clear), such as when queries are combined
into unions; these cases are not supported.

[#3394](https://www.sqlalchemy.org/trac/ticket/3394)

## New Features and Improvements - Core

### Engines now invalidate connections, run error handlers for BaseException

Added in version 1.1: this change is a late add to the 1.1 series just
prior to 1.1 final, and is not present in the 1.1 beta releases.

The Python `BaseException` class is below that of `Exception` but is the
identifiable base for system-level exceptions such as `KeyboardInterrupt`,
`SystemExit`, and notably the `GreenletExit` exception that’s used by
eventlet and gevent. This exception class is now intercepted by the exception-
handling routines of [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), and includes handling by the
`ConnectionEvents.handle_error()` event.  The [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is now
**invalidated** by default in the case of a system level exception that is not
a subclass of `Exception`, as it is assumed an operation was interrupted and
the connection may be in an unusable state.  The MySQL drivers are most
targeted by this change however the change is across all DBAPIs.

Note that upon invalidation, the immediate DBAPI connection used by
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is disposed, and the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), if still
being used subsequent to the exception raise, will use a new
DBAPI connection for subsequent operations upon next use; however, the state of
any transaction in progress is lost and the appropriate `.rollback()` method
must be called if applicable before this reuse can proceed.

In order to identify this change, it was straightforward to demonstrate a pymysql or
mysqlclient / MySQL-Python connection moving into a corrupted state when
these exceptions occur in the middle of the connection doing its work;
the connection would then be returned to the connection pool where subsequent
uses would fail, or even before returning to the pool would cause secondary
failures in context managers that call `.rollback()` upon the exception
catch.   The behavior here is expected to reduce
the incidence of the MySQL error “commands out of sync”, as well as the
`ResourceClosedError` which can occur when the MySQL driver fails to
report `cursor.description` correctly, when running under greenlet
conditions where greenlets are killed, or where `KeyboardInterrupt` exceptions
are handled without exiting the program entirely.

The behavior is distinct from the usual auto-invalidation feature, in that it
does not assume that the backend database itself has been shut down or
restarted; it does not recycle the entire connection pool as is the case
for usual DBAPI disconnect exceptions.

This change should be a net improvement for all users with the exception
of **any application that currently intercepts ``KeyboardInterrupt`` or
``GreenletExit`` and wishes to continue working within the same transaction**.
Such an operation is theoretically possible with other DBAPIs that do not appear to be
impacted by `KeyboardInterrupt` such as psycopg2.  For these DBAPIs,
the following workaround will disable the connection from being recycled
for specific exceptions:

```
engine = create_engine("postgresql+psycopg2://")

@event.listens_for(engine, "handle_error")
def cancel_disconnect(ctx):
    if isinstance(ctx.original_exception, KeyboardInterrupt):
        ctx.is_disconnect = False
```

[#3803](https://www.sqlalchemy.org/trac/ticket/3803)

### CTE Support for INSERT, UPDATE, DELETE

One of the most widely requested features is support for common table
expressions (CTE) that work with INSERT, UPDATE, DELETE, and is now implemented.
An INSERT/UPDATE/DELETE can both draw from a WITH clause that’s stated at the
top of the SQL, as well as can be used as a CTE itself in the context of
a larger statement.

As part of this change, an INSERT from SELECT that includes a CTE will now
render the CTE at the top of the entire statement, rather than nested
in the SELECT statement as was the case in 1.0.

Below is an example that renders UPDATE, INSERT and SELECT all in one
statement:

```
>>> from sqlalchemy import table, column, select, literal, exists
>>> orders = table(
...     "orders",
...     column("region"),
...     column("amount"),
...     column("product"),
...     column("quantity"),
... )
>>>
>>> upsert = (
...     orders.update()
...     .where(orders.c.region == "Region1")
...     .values(amount=1.0, product="Product1", quantity=1)
...     .returning(*(orders.c._all_columns))
...     .cte("upsert")
... )
>>>
>>> insert = orders.insert().from_select(
...     orders.c.keys(),
...     select([literal("Region1"), literal(1.0), literal("Product1"), literal(1)]).where(
...         ~exists(upsert.select())
...     ),
... )
>>>
>>> print(insert)  # Note: formatting added for clarity
WITH upsert AS
(UPDATE orders SET amount=:amount, product=:product, quantity=:quantity
 WHERE orders.region = :region_1
 RETURNING orders.region, orders.amount, orders.product, orders.quantity
)
INSERT INTO orders (region, amount, product, quantity)
SELECT
    :param_1 AS anon_1, :param_2 AS anon_2,
    :param_3 AS anon_3, :param_4 AS anon_4
WHERE NOT (
    EXISTS (
        SELECT upsert.region, upsert.amount,
               upsert.product, upsert.quantity
        FROM upsert))
```

[#2551](https://www.sqlalchemy.org/trac/ticket/2551)

### Support for RANGE and ROWS specification within window functions

New [over.range_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over.params.range_) and [over.rows](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over.params.rows) parameters allow
RANGE and ROWS expressions for window functions:

```
>>> from sqlalchemy import func

>>> print(func.row_number().over(order_by="x", range_=(-5, 10)))
row_number() OVER (ORDER BY x RANGE BETWEEN :param_1 PRECEDING AND :param_2 FOLLOWING)
>>> print(func.row_number().over(order_by="x", rows=(None, 0)))
row_number() OVER (ORDER BY x ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
>>> print(func.row_number().over(order_by="x", range_=(-2, None)))
row_number() OVER (ORDER BY x RANGE BETWEEN :param_1 PRECEDING AND UNBOUNDED FOLLOWING)
```

[over.range_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over.params.range_) and [over.rows](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over.params.rows) are specified as
2-tuples and indicate negative and positive values for specific ranges,
0 for “CURRENT ROW”, and None for UNBOUNDED.

See also

[Using Window Functions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-window-functions)

[#3049](https://www.sqlalchemy.org/trac/ticket/3049)

### Support for the SQL LATERAL keyword

The LATERAL keyword is currently known to only be supported by PostgreSQL 9.3
and greater, however as it is part of the SQL standard support for this keyword
is added to Core.   The implementation of [Select.lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.lateral) employs
special logic beyond just rendering the LATERAL keyword to allow for
correlation of tables that are derived from the same FROM clause as the
selectable, e.g. lateral correlation:

```
>>> from sqlalchemy import table, column, select, true
>>> people = table("people", column("people_id"), column("age"), column("name"))
>>> books = table("books", column("book_id"), column("owner_id"))
>>> subq = (
...     select([books.c.book_id])
...     .where(books.c.owner_id == people.c.people_id)
...     .lateral("book_subq")
... )
>>> print(select([people]).select_from(people.join(subq, true())))
SELECT people.people_id, people.age, people.name
FROM people JOIN LATERAL (SELECT books.book_id AS book_id
FROM books WHERE books.owner_id = people.people_id)
AS book_subq ON true
```

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation)

[Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral)

[Select.lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.lateral)

[#2857](https://www.sqlalchemy.org/trac/ticket/2857)

### Support for TABLESAMPLE

The SQL standard TABLESAMPLE can be rendered using the
[FromClause.tablesample()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.tablesample) method, which returns a [TableSample](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableSample)
construct similar to an alias:

```
from sqlalchemy import func

selectable = people.tablesample(func.bernoulli(1), name="alias", seed=func.random())
stmt = select([selectable.c.people_id])
```

Assuming `people` with a column `people_id`, the above
statement would render as:

```
SELECT alias.people_id FROM
people AS alias TABLESAMPLE bernoulli(:bernoulli_1)
REPEATABLE (random())
```

[#3718](https://www.sqlalchemy.org/trac/ticket/3718)

### The.autoincrementdirective is no longer implicitly enabled for a composite primary key column

SQLAlchemy has always had the convenience feature of enabling the backend database’s
“autoincrement” feature for a single-column integer primary key; by “autoincrement”
we mean that the database column will include whatever DDL directives the
database provides in order to indicate an auto-incrementing integer identifier,
such as the SERIAL keyword on PostgreSQL or AUTO_INCREMENT on MySQL, and additionally
that the dialect will receive these generated values from the execution
of a [Table.insert()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.insert) construct using techniques appropriate to that
backend.

What’s changed is that this feature no longer turns on automatically for a
*composite* primary key; previously, a table definition such as:

```
Table(
    "some_table",
    metadata,
    Column("x", Integer, primary_key=True),
    Column("y", Integer, primary_key=True),
)
```

Would have “autoincrement” semantics applied to the `'x'` column, only
because it’s first in the list of primary key columns.  In order to
disable this, one would have to turn off `autoincrement` on all columns:

```
# old way
Table(
    "some_table",
    metadata,
    Column("x", Integer, primary_key=True, autoincrement=False),
    Column("y", Integer, primary_key=True, autoincrement=False),
)
```

With the new behavior, the composite primary key will not have autoincrement
semantics unless a column is marked explicitly with `autoincrement=True`:

```
# column 'y' will be SERIAL/AUTO_INCREMENT/ auto-generating
Table(
    "some_table",
    metadata,
    Column("x", Integer, primary_key=True),
    Column("y", Integer, primary_key=True, autoincrement=True),
)
```

In order to anticipate some potential backwards-incompatible scenarios,
the [Table.insert()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.insert) construct will perform more thorough checks
for missing primary key values on composite primary key columns that don’t
have autoincrement set up; given a table such as:

```
Table(
    "b",
    metadata,
    Column("x", Integer, primary_key=True),
    Column("y", Integer, primary_key=True),
)
```

An INSERT emitted with no values for this table will produce this warning:

```
SAWarning: Column 'b.x' is marked as a member of the primary
key for table 'b', but has no Python-side or server-side default
generator indicated, nor does it indicate 'autoincrement=True',
and no explicit value is passed.  Primary key columns may not
store NULL. Note that as of SQLAlchemy 1.1, 'autoincrement=True'
must be indicated explicitly for composite (e.g. multicolumn)
primary keys if AUTO_INCREMENT/SERIAL/IDENTITY behavior is
expected for one of the columns in the primary key. CREATE TABLE
statements are impacted by this change as well on most backends.
```

For a column that is receiving primary key values from a server-side
default or something less common such as a trigger, the presence of a
value generator can be indicated using [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue):

```
Table(
    "b",
    metadata,
    Column("x", Integer, primary_key=True, server_default=FetchedValue()),
    Column("y", Integer, primary_key=True, server_default=FetchedValue()),
)
```

For the very unlikely case where a composite primary key is actually intended
to store NULL in one or more of its columns (only supported on SQLite and MySQL),
specify the column with `nullable=True`:

```
Table(
    "b",
    metadata,
    Column("x", Integer, primary_key=True),
    Column("y", Integer, primary_key=True, nullable=True),
)
```

In a related change, the `autoincrement` flag may be set to True
on a column that has a client-side or server-side default.  This typically
will not have much impact on the behavior of the column during an INSERT.

See also

[No more generation of an implicit KEY for composite primary key w/ AUTO_INCREMENT](#change-mysql-3216)

[#3216](https://www.sqlalchemy.org/trac/ticket/3216)

### Support for IS DISTINCT FROM and IS NOT DISTINCT FROM

New operators [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) and
[ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) allow the IS DISTINCT
FROM and IS NOT DISTINCT FROM sql operation:

```
>>> print(column("x").is_distinct_from(None))
x IS DISTINCT FROM NULL
```

Handling is provided for NULL, True and False:

```
>>> print(column("x").isnot_distinct_from(False))
x IS NOT DISTINCT FROM false
```

For SQLite, which doesn’t have this operator, “IS” / “IS NOT” is rendered,
which on SQLite works for NULL unlike other backends:

```
>>> from sqlalchemy.dialects import sqlite
>>> print(column("x").is_distinct_from(None).compile(dialect=sqlite.dialect()))
x IS NOT NULL
```

### Core and ORM support for FULL OUTER JOIN

The new flag [FromClause.outerjoin.full](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.outerjoin.params.full), available at the Core
and ORM level, instructs the compiler to render `FULL OUTER JOIN`
where it would normally render `LEFT OUTER JOIN`:

```
stmt = select([t1]).select_from(t1.outerjoin(t2, full=True))
```

The flag also works at the ORM level:

```
q = session.query(MyClass).outerjoin(MyOtherClass, full=True)
```

[#1957](https://www.sqlalchemy.org/trac/ticket/1957)

### ResultSet column matching enhancements; positional column setup for textual SQL

A series of improvements were made to the `ResultProxy` system
in the 1.0 series as part of [#918](https://www.sqlalchemy.org/trac/ticket/918), which reorganizes the internals
to match cursor-bound result columns with table/ORM metadata positionally,
rather than by matching names, for compiled SQL constructs that contain full
information about the result rows to be returned.   This allows a dramatic savings
on Python overhead as well as much greater accuracy in linking ORM and Core
SQL expressions to result rows.  In 1.1, this reorganization has been taken
further internally, and also has been made available to pure-text SQL
constructs via the use of the recently added [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method.

#### TextAsFrom.columns() now works positionally

The [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method, added in 0.9, accepts column-based arguments
positionally; in 1.1, when all columns are passed positionally, the correlation
of these columns to the ultimate result set is also performed positionally.
The key advantage here is that textual SQL can now be linked to an ORM-
level result set without the need to deal with ambiguous or duplicate column
names, or with having to match labeling schemes to ORM-level labeling schemes.  All
that’s needed now is the same ordering of columns within the textual SQL
and the column arguments passed to [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns):

```
from sqlalchemy import text

stmt = text(
    "SELECT users.id, addresses.id, users.id, "
    "users.name, addresses.email_address AS email "
    "FROM users JOIN addresses ON users.id=addresses.user_id "
    "WHERE users.id = 1"
).columns(User.id, Address.id, Address.user_id, User.name, Address.email_address)

query = session.query(User).from_statement(stmt).options(contains_eager(User.addresses))
result = query.all()
```

Above, the textual SQL contains the column “id” three times, which would
normally be ambiguous.  Using the new feature, we can apply the mapped
columns from the `User` and `Address` class directly, even linking
the `Address.user_id` column to the `users.id` column in textual SQL
for fun, and the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object will receive rows that are correctly
targetable as needed, including for an eager load.

This change is **backwards incompatible** with code that passes the columns
to the method with a different ordering than is present in the textual statement.
It is hoped that this impact will be low due to the fact that this
method has always been documented illustrating the columns being passed in the same order as that of the
textual SQL statement, as would seem intuitive, even though the internals
weren’t checking for this.  The method itself was only added as of 0.9 in
any case and may not yet have widespread use.  Notes on exactly how to handle
this behavioral change for applications using it are at [TextClause.columns() will match columns positionally, not by name, when passed positionally](#behavior-change-3501).

See also

[Selecting with Textual Column Expressions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-select-arbitrary-text)

> [TextClause.columns() will match columns positionally, not by name, when passed positionally](#behavior-change-3501) - backwards compatibility remarks

#### Positional matching is trusted over name-based matching for Core/ORM SQL constructs

Another aspect of this change is that the rules for matching columns have also been modified
to rely upon “positional” matching more fully for compiled SQL constructs
as well.   Given a statement like the following:

```
ua = users.alias("ua")
stmt = select([users.c.user_id, ua.c.user_id])
```

The above statement will compile to:

```
SELECT users.user_id, ua.user_id FROM users, users AS ua
```

In 1.0, the above statement when executed would be matched to its original
compiled construct using positional matching, however because the statement
contains the `'user_id'` label duplicated, the “ambiguous column” rule
would still get involved and prevent the columns from being fetched from a row.
As of 1.1, the “ambiguous column” rule does not affect an exact match from
a column construct to the SQL column, which is what the ORM uses to
fetch columns:

```
result = conn.execute(stmt)
row = result.first()

# these both match positionally, so no error
user_id = row[users.c.user_id]
ua_id = row[ua.c.user_id]

# this still raises, however
user_id = row["user_id"]
```

#### Much less likely to get an “ambiguous column” error message

As part of this change, the wording of the error message `Ambiguous column
name '<name>' in result set! try 'use_labels' option on select statement.`
has been dialed back; as this message should now be extremely rare when using
the ORM or Core compiled SQL constructs, it merely states
`Ambiguous column name '<name>' in result set column descriptions`, and
only when a result column is retrieved using the string name that is actually
ambiguous, e.g. `row['user_id']` in the above example.  It also now refers
to the actual ambiguous name from the rendered SQL statement itself,
rather than indicating the key or name that was local to the construct being
used for the fetch.

[#3501](https://www.sqlalchemy.org/trac/ticket/3501)

### Support for Python’s nativeenumtype and compatible forms

The [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) type can now be constructed using any
PEP-435 compliant enumerated type.   When using this mode, input values
and return values are the actual enumerated objects, not the
string/integer/etc values:

```
import enum
from sqlalchemy import Table, MetaData, Column, Enum, create_engine

class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3

t = Table("data", MetaData(), Column("value", Enum(MyEnum)))

e = create_engine("sqlite://")
t.create(e)

e.execute(t.insert(), {"value": MyEnum.two})
assert e.scalar(t.select()) is MyEnum.two
```

#### TheEnum.enumscollection is now a list instead of a tuple

As part of the changes to [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum), the `Enum.enums` collection
of elements is now a list instead of a tuple.  This because lists
are appropriate for variable length sequences of homogeneous items where
the position of the element is not semantically significant.

[#3292](https://www.sqlalchemy.org/trac/ticket/3292)

### Negative integer indexes accommodated by Core result rows

The `RowProxy` object now accommodates single negative integer indexes
like a regular Python sequence, both in the pure Python and C-extension
version.  Previously, negative values would only work in slices:

```
>>> from sqlalchemy import create_engine
>>> e = create_engine("sqlite://")
>>> row = e.execute("select 1, 2, 3").first()
>>> row[-1], row[-2], row[1], row[-2:2]
3 2 2 (2,)
```

### TheEnumtype now does in-Python validation of values

To accommodate for Python native enumerated objects, as well as for edge
cases such as that of where a non-native ENUM type is used within an ARRAY
and a CHECK constraint is infeasible, the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatype now adds
in-Python validation of input values when the [Enum.validate_strings](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.validate_strings)
flag is used (1.1.0b2):

```
>>> from sqlalchemy import Table, MetaData, Column, Enum, create_engine
>>> t = Table(
...     "data",
...     MetaData(),
...     Column("value", Enum("one", "two", "three", validate_strings=True)),
... )
>>> e = create_engine("sqlite://")
>>> t.create(e)
>>> e.execute(t.insert(), {"value": "four"})
Traceback (most recent call last):
  ...
sqlalchemy.exc.StatementError: (exceptions.LookupError)
"four" is not among the defined enum values
[SQL: u'INSERT INTO data (value) VALUES (?)']
[parameters: [{'value': 'four'}]]
```

This validation is turned off by default as there are already use cases
identified where users don’t want such validation (such as string comparisons).
For non-string types, it necessarily takes place in all cases.  The
check also occurs unconditionally on the result-handling side as well, when
values coming from the database are returned.

This validation is in addition to the existing behavior of creating a
CHECK constraint when a non-native enumerated type is used.  The creation of
this CHECK constraint can now be disabled using the new
[Enum.create_constraint](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.create_constraint) flag.

[#3095](https://www.sqlalchemy.org/trac/ticket/3095)

### Non-native boolean integer values coerced to zero/one/None in all cases

The [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) datatype coerces Python booleans to integer values
for backends that don’t have a native boolean type, such as SQLite and
MySQL.  On these backends, a CHECK constraint is normally set up which
ensures the values in the database are in fact one of these two values.
However, MySQL ignores CHECK constraints, the constraint is optional, and
an existing database might not have this constraint.  The [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)
datatype has been repaired such that an incoming Python-side value that is
already an integer value is coerced to zero or one, not just passed as-is;
additionally, the C-extension version of the int-to-boolean processor for
results now uses the same Python boolean interpretation of the value,
rather than asserting an exact one or zero value.  This is now consistent
with the pure-Python int-to-boolean processor and is more forgiving of
existing data already within the database.   Values of None/NULL are as before
retained as None/NULL.

Note

this change had an unintended side effect that the interpretation of non-
integer values, such as strings, also changed in behavior such that the
string value `"0"` would be interpreted as “true”, but only on backends
that don’t have a native boolean datatype - on “native boolean” backends
like PostgreSQL, the string value `"0"` is passed directly to the driver
and is interpreted as “false”.  This is an inconsistency that did not occur
with the previous implementation. It should be noted that passing strings or
any other value outside of `None`, `True`, `False`, `1`, `0` to
the [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) datatype is **not supported** and version 1.2 will
raise an error for this scenario (or possibly just emit a warning, TBD).
See also [#4102](https://www.sqlalchemy.org/trac/ticket/4102).

[#3730](https://www.sqlalchemy.org/trac/ticket/3730)

### Large parameter and row values are now truncated in logging and exception displays

A large value present as a bound parameter for a SQL statement, as well as a
large value present in a result row, will now be truncated during display
within logging, exception reporting, as well as `repr()` of the row itself:

```
>>> from sqlalchemy import create_engine
>>> import random
>>> e = create_engine("sqlite://", echo="debug")
>>> some_value = "".join(chr(random.randint(52, 85)) for i in range(5000))
>>> row = e.execute("select ?", [some_value]).first()
... # (lines are wrapped for clarity) ...
2016-02-17 13:23:03,027 INFO sqlalchemy.engine.base.Engine select ?
2016-02-17 13:23:03,027 INFO sqlalchemy.engine.base.Engine
('E6@?>9HPOJB<<BHR:@=TS:5ILU=;JLM<4?B9<S48PTNG9>:=TSTLA;9K;9FPM4M8M@;NM6GU
LUAEBT9QGHNHTHR5EP75@OER4?SKC;D:TFUMD:M>;C6U:JLM6R67GEK<A6@S@C@J7>4=4:P
GJ7HQ6 ... (4702 characters truncated) ... J6IK546AJMB4N6S9L;;9AKI;=RJP
HDSSOTNBUEEC9@Q:RCL:I@5?FO<9K>KJAGAO@E6@A7JI8O:J7B69T6<8;F:S;4BEIJS9HM
K:;5OLPM@JR;R:J6<SOTTT=>Q>7T@I::OTDC:CC<=NGP6C>BC8N',)
2016-02-17 13:23:03,027 DEBUG sqlalchemy.engine.base.Engine Col ('?',)
2016-02-17 13:23:03,027 DEBUG sqlalchemy.engine.base.Engine
Row (u'E6@?>9HPOJB<<BHR:@=TS:5ILU=;JLM<4?B9<S48PTNG9>:=TSTLA;9K;9FPM4M8M@;
NM6GULUAEBT9QGHNHTHR5EP75@OER4?SKC;D:TFUMD:M>;C6U:JLM6R67GEK<A6@S@C@J7
>4=4:PGJ7HQ ... (4703 characters truncated) ... J6IK546AJMB4N6S9L;;9AKI;=
RJPHDSSOTNBUEEC9@Q:RCL:I@5?FO<9K>KJAGAO@E6@A7JI8O:J7B69T6<8;F:S;4BEIJS9HM
K:;5OLPM@JR;R:J6<SOTTT=>Q>7T@I::OTDC:CC<=NGP6C>BC8N',)
>>> print(row)
(u'E6@?>9HPOJB<<BHR:@=TS:5ILU=;JLM<4?B9<S48PTNG9>:=TSTLA;9K;9FPM4M8M@;NM6
GULUAEBT9QGHNHTHR5EP75@OER4?SKC;D:TFUMD:M>;C6U:JLM6R67GEK<A6@S@C@J7>4
=4:PGJ7HQ ... (4703 characters truncated) ... J6IK546AJMB4N6S9L;;9AKI;
=RJPHDSSOTNBUEEC9@Q:RCL:I@5?FO<9K>KJAGAO@E6@A7JI8O:J7B69T6<8;F:S;4BEIJS9H
MK:;5OLPM@JR;R:J6<SOTTT=>Q>7T@I::OTDC:CC<=NGP6C>BC8N',)
```

[#2837](https://www.sqlalchemy.org/trac/ticket/2837)

### JSON support added to Core

As MySQL now has a JSON datatype in addition to the PostgreSQL JSON datatype,
the core now gains a [sqlalchemy.types.JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) datatype that is the basis
for both of these.  Using this type allows access to the “getitem” operator
as well as the “getpath” operator in a way that is agnostic across PostgreSQL
and MySQL.

The new datatype also has a series of improvements to the handling of
NULL values as well as expression handling.

See also

[MySQL JSON Support](#change-3547)

[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)

[JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON)

[JSON](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.JSON)

[#3619](https://www.sqlalchemy.org/trac/ticket/3619)

#### JSON “null” is inserted as expected with ORM operations, omitted when not present

The [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type and its descendant types [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON)
and [JSON](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.JSON) have a flag [JSON.none_as_null](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.params.none_as_null) which
when set to True indicates that the Python value `None` should translate
into a SQL NULL rather than a JSON NULL value.  This flag defaults to False,
which means that the Python value `None` should result in a JSON NULL value.

This logic would fail, and is now corrected, in the following circumstances:

1. When the column also contained a default or server_default value,
a positive value of `None` on the mapped attribute that expects to persist
JSON “null” would still result in the column-level default being triggered,
replacing the `None` value:

```
class MyObject(Base):
    # ...

    json_value = Column(JSON(none_as_null=False), default="some default")

# would insert "some default" instead of "'null'",
# now will insert "'null'"
obj = MyObject(json_value=None)
session.add(obj)
session.commit()
```

2. When the column *did not* contain a default or server_default value, a missing
value on a JSON column configured with none_as_null=False would still render
JSON NULL rather than falling back to not inserting any value, behaving
inconsistently vs. all other datatypes:

```
class MyObject(Base):
    # ...

    some_other_value = Column(String(50))
    json_value = Column(JSON(none_as_null=False))

# would result in NULL for some_other_value,
# but json "'null'" for json_value.  Now results in NULL for both
# (the json_value is omitted from the INSERT)
obj = MyObject()
session.add(obj)
session.commit()
```

This is a behavioral change that is backwards incompatible for an application
that was relying upon this to default a missing value as JSON null.  This
essentially establishes that a **missing value is distinguished from a present
value of None**.  See [JSON Columns will not insert JSON NULL if no value is supplied and no default is established](#behavior-change-3514) for further detail.

3. When the [Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings) method were used, `None`
would be ignored in all cases:

```
# would insert SQL NULL and/or trigger defaults,
# now inserts "'null'"
session.bulk_insert_mappings(MyObject, [{"json_value": None}])
```

The [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type now implements the
[TypeEngine.should_evaluate_none](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.should_evaluate_none) flag,
indicating that `None` should not be ignored here; it is configured
automatically based on the value of [JSON.none_as_null](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.params.none_as_null).
Thanks to [#3061](https://www.sqlalchemy.org/trac/ticket/3061), we can differentiate when the value `None` is actively
set by the user versus when it was never set at all.

The feature applies as well to the new base [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type
and its descendant types.

[#3514](https://www.sqlalchemy.org/trac/ticket/3514)

#### New JSON.NULL Constant Added

To ensure that an application can always have full control at the value level
of whether a [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON), [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON), [JSON](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.JSON),
or [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) column
should receive a SQL NULL or JSON `"null"` value, the constant
[JSON.NULL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.NULL) has been added, which in conjunction with
[null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) can be used to determine fully between SQL NULL and
JSON `"null"`, regardless of what [JSON.none_as_null](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.params.none_as_null) is set
to:

```
from sqlalchemy import null
from sqlalchemy.dialects.postgresql import JSON

obj1 = MyObject(json_value=null())  # will *always* insert SQL NULL
obj2 = MyObject(json_value=JSON.NULL)  # will *always* insert JSON string "null"

session.add_all([obj1, obj2])
session.commit()
```

The feature applies as well to the new base [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type
and its descendant types.

[#3514](https://www.sqlalchemy.org/trac/ticket/3514)

### Array support added to Core; new ANY and ALL operators

Along with the enhancements made to the PostgreSQL [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY)
type described in [Correct SQL Types are Established from Indexed Access of ARRAY, JSON, HSTORE](#change-3503), the base class of [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY)
itself has been moved to Core in a new class [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY).

Arrays are part of the SQL standard, as are several array-oriented functions
such as `array_agg()` and `unnest()`.  In support of these constructs
for not just PostgreSQL but also potentially for other array-capable backends
in the future such as DB2, the majority of array logic for SQL expressions
is now in Core.   The [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) type still **only works on
PostgreSQL**, however it can be used directly, supporting special array
use cases such as indexed access, as well as support for the ANY and ALL:

```
mytable = Table("mytable", metadata, Column("data", ARRAY(Integer, dimensions=2)))

expr = mytable.c.data[5][6]

expr = mytable.c.data[5].any(12)
```

In support of ANY and ALL, the [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) type retains the same
[Comparator.any()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.any) and [Comparator.all()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.all) methods
from the PostgreSQL type, but also exports these operations to new
standalone operator functions [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) and
[all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_).  These two functions work in more
of the traditional SQL way, allowing a right-side expression form such
as:

```
from sqlalchemy import any_, all_

select([mytable]).where(12 == any_(mytable.c.data[5]))
```

For the PostgreSQL-specific operators “contains”, “contained_by”, and
“overlaps”, one should continue to use the [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY)
type directly, which provides all functionality of the [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY)
type as well.

The [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) and [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_) operators
are open-ended at the Core level, however their interpretation by backend
databases is limited.  On the PostgreSQL backend, the two operators
**only accept array values**.  Whereas on the MySQL backend, they
**only accept subquery values**.  On MySQL, one can use an expression
such as:

```
from sqlalchemy import any_, all_

subq = select([mytable.c.value])
select([mytable]).where(12 > any_(subq))
```

[#3516](https://www.sqlalchemy.org/trac/ticket/3516)

### New Function features, “WITHIN GROUP”, array_agg and set aggregate functions

With the new [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) type we can also implement a pre-typed
function for the `array_agg()` SQL function that returns an array,
which is now available using [array_agg](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg):

```
from sqlalchemy import func

stmt = select([func.array_agg(table.c.value)])
```

A PostgreSQL element for an aggregate ORDER BY is also added via
[aggregate_order_by](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.aggregate_order_by):

```
from sqlalchemy.dialects.postgresql import aggregate_order_by

expr = func.array_agg(aggregate_order_by(table.c.a, table.c.b.desc()))
stmt = select([expr])
```

Producing:

```
SELECT array_agg(table1.a ORDER BY table1.b DESC) AS array_agg_1 FROM table1
```

The PG dialect itself also provides an [array_agg()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array_agg) wrapper to
ensure the [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) type:

```
from sqlalchemy.dialects.postgresql import array_agg

stmt = select([array_agg(table.c.value).contains("foo")])
```

Additionally, functions like `percentile_cont()`, `percentile_disc()`,
`rank()`, `dense_rank()` and others that require an ordering via
`WITHIN GROUP (ORDER BY <expr>)` are now available via the
[FunctionElement.within_group()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.within_group) modifier:

```
from sqlalchemy import func

stmt = select(
    [
        department.c.id,
        func.percentile_cont(0.5).within_group(department.c.salary.desc()),
    ]
)
```

The above statement would produce SQL similar to:

```
SELECT department.id, percentile_cont(0.5)
WITHIN GROUP (ORDER BY department.salary DESC)
```

Placeholders with correct return types are now provided for these functions,
and include [percentile_cont](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percentile_cont), [percentile_disc](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percentile_disc),
[rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.rank), [dense_rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.dense_rank), [mode](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.mode), [percent_rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percent_rank),
and [cume_dist](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.cume_dist).

[#3132](https://www.sqlalchemy.org/trac/ticket/3132) [#1370](https://www.sqlalchemy.org/trac/ticket/1370)

### TypeDecorator now works with Enum, Boolean, “schema” types automatically

The [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType) types include types such as [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum)
and [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) which, in addition to corresponding to a database
type, also generate either a CHECK constraint or in the case of PostgreSQL
ENUM a new CREATE TYPE statement, will now work automatically with
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) recipes.  Previously, a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) for
an [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) had to look like this:

```
# old way
class MyEnum(TypeDecorator, SchemaType):
    impl = postgresql.ENUM("one", "two", "three", name="myenum")

    def _set_table(self, table):
        self.impl._set_table(table)
```

The [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) now propagates those additional events so it
can be done like any other type:

```
# new way
class MyEnum(TypeDecorator):
    impl = postgresql.ENUM("one", "two", "three", name="myenum")
```

[#2919](https://www.sqlalchemy.org/trac/ticket/2919)

### Multi-Tenancy Schema Translation for Table objects

To support the use case of an application that uses the same set of
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects in many schemas, such as schema-per-user, a new
execution option [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map)
is added.  Using this mapping, a set of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects can be made on a per-connection basis to refer to any set of schemas
instead of the [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) to which they were assigned.  The
translation works for DDL and SQL generation, as well as with the ORM.

For example, if the `User` class were assigned the schema “per_user”:

```
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)

    __table_args__ = {"schema": "per_user"}
```

On each request, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) can be set up to refer to a
different schema each time:

```
session = Session()
session.connection(
    execution_options={"schema_translate_map": {"per_user": "account_one"}}
)

# will query from the ``account_one.user`` table
session.query(User).get(5)
```

See also

[Translation of Schema Names](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating)

[#2685](https://www.sqlalchemy.org/trac/ticket/2685)

### “Friendly” stringification of Core SQL constructs without a dialect

Calling `str()` on a Core SQL construct will now produce a string
in more cases than before, supporting various SQL constructs not normally
present in default SQL such as RETURNING, array indexes, and non-standard
datatypes:

```
>>> from sqlalchemy import table, column
t>>> t = table('x', column('a'), column('b'))
>>> print(t.insert().returning(t.c.a, t.c.b))
INSERT INTO x (a, b) VALUES (:a, :b) RETURNING x.a, x.b
```

The `str()` function now calls upon an entirely separate dialect / compiler
intended just for plain string printing without a specific dialect set up,
so as more “just show me a string!” cases come up, these can be added
to this dialect/compiler without impacting behaviors on real dialects.

See also

[Stringify of Query will consult the Session for the correct dialect](#change-3081)

[#3631](https://www.sqlalchemy.org/trac/ticket/3631)

### The type_coerce function is now a persistent SQL element

The [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) function previously would return
an object either of type [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) or [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label), depending
on the input.  An effect this would have was that in the case where expression
transformations were used, such as the conversion of an element from a
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) to a [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) that’s critical to ORM-level
lazy loading, the type coercion information would not be used since it would
have been lost already.

To improve this behavior, the function now returns a persistent
[TypeCoerce](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TypeCoerce) container around the given expression, which itself
remains unaffected; this construct is evaluated explicitly by the
SQL compiler.  This allows for the coercion of the inner expression
to be maintained no matter how the statement is modified, including if
the contained element is replaced with a different one, as is common
within the ORM’s lazy loading feature.

The test case illustrating the effect makes use of a heterogeneous
primaryjoin condition in conjunction with custom types and lazy loading.
Given a custom type that applies a CAST as a “bind expression”:

```
class StringAsInt(TypeDecorator):
    impl = String

    def column_expression(self, col):
        return cast(col, Integer)

    def bind_expression(self, value):
        return cast(value, String)
```

Then, a mapping where we are equating a string “id” column on one
table to an integer “id” column on the other:

```
class Person(Base):
    __tablename__ = "person"
    id = Column(StringAsInt, primary_key=True)

    pets = relationship(
        "Pets",
        primaryjoin=(
            "foreign(Pets.person_id)==cast(type_coerce(Person.id, Integer), Integer)"
        ),
    )

class Pets(Base):
    __tablename__ = "pets"
    id = Column("id", Integer, primary_key=True)
    person_id = Column("person_id", Integer)
```

Above, in the [relationship.primaryjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin) expression, we are
using [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) to handle bound parameters passed via
lazyloading as integers, since we already know these will come from
our `StringAsInt` type which maintains the value as an integer in
Python. We are then using [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) so that as a SQL expression,
the VARCHAR “id”  column will be CAST to an integer for a regular non-
converted join as with [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) or [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload).
That is, a joinedload of `.pets` looks like:

```
SELECT person.id AS person_id, pets_1.id AS pets_1_id,
       pets_1.person_id AS pets_1_person_id
FROM person
LEFT OUTER JOIN pets AS pets_1
ON pets_1.person_id = CAST(person.id AS INTEGER)
```

Without the CAST in the ON clause of the join, strongly-typed databases
such as PostgreSQL will refuse to implicitly compare the integer and fail.

The lazyload case of `.pets` relies upon replacing
the `Person.id` column at load time with a bound parameter, which receives
a Python-loaded value.  This replacement is specifically where the intent
of our [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) function would be lost.  Prior to the change,
this lazy load comes out as:

```
SELECT pets.id AS pets_id, pets.person_id AS pets_person_id
FROM pets
WHERE pets.person_id = CAST(CAST(%(param_1)s AS VARCHAR) AS INTEGER)
-- {'param_1': 5}
```

Where above, we see that our in-Python value of `5` is CAST first
to a VARCHAR, then back to an INTEGER in SQL; a double CAST which works,
but is nevertheless not what we asked for.

With the change, the [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) function maintains a wrapper
even after the column is swapped out for a bound parameter, and the query now
looks like:

```
SELECT pets.id AS pets_id, pets.person_id AS pets_person_id
FROM pets
WHERE pets.person_id = CAST(%(param_1)s AS INTEGER)
-- {'param_1': 5}
```

Where our outer CAST that’s in our primaryjoin still takes effect, but the
needless CAST that’s in part of the `StringAsInt` custom type is removed
as intended by the [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) function.

[#3531](https://www.sqlalchemy.org/trac/ticket/3531)

## Key Behavioral Changes - ORM

### JSON Columns will not insert JSON NULL if no value is supplied and no default is established

As detailed in [JSON “null” is inserted as expected with ORM operations, omitted when not present](#change-3514), [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) will not render
a JSON “null” value if the value is missing entirely.  To prevent SQL NULL,
a default should be set up.  Given the following mapping:

```
class MyObject(Base):
    # ...

    json_value = Column(JSON(none_as_null=False), nullable=False)
```

The following flush operation will fail with an integrity error:

```
obj = MyObject()  # note no json_value
session.add(obj)
session.commit()  # will fail with integrity error
```

If the default for the column should be JSON NULL, set this on the
Column:

```
class MyObject(Base):
    # ...

    json_value = Column(JSON(none_as_null=False), nullable=False, default=JSON.NULL)
```

Or, ensure the value is present on the object:

```
obj = MyObject(json_value=None)
session.add(obj)
session.commit()  # will insert JSON NULL
```

Note that setting `None` for the default is the same as omitting it entirely;
the [JSON.none_as_null](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.params.none_as_null) flag does not impact the value of `None`
passed to [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) or [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default):

```
# default=None is the same as omitting it entirely, does not apply JSON NULL
json_value = Column(JSON(none_as_null=False), nullable=False, default=None)
```

See also

[JSON “null” is inserted as expected with ORM operations, omitted when not present](#change-3514)

### Columns no longer added redundantly with DISTINCT + ORDER BY

A query such as the following will now augment only those columns
that are missing from the SELECT list, without duplicates:

```
q = (
    session.query(User.id, User.name.label("name"))
    .distinct()
    .order_by(User.id, User.name, User.fullname)
)
```

Produces:

```
SELECT DISTINCT user.id AS a_id, user.name AS name,
 user.fullname AS a_fullname
FROM a ORDER BY user.id, user.name, user.fullname
```

Previously, it would produce:

```
SELECT DISTINCT user.id AS a_id, user.name AS name, user.name AS a_name,
  user.fullname AS a_fullname
FROM a ORDER BY user.id, user.name, user.fullname
```

Where above, the `user.name` column is added unnecessarily.  The results
would not be affected, as the additional columns are not included in the
result in any case, but the columns are unnecessary.

Additionally, when the PostgreSQL DISTINCT ON format is used by passing
expressions to [Query.distinct()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.distinct), the above “column adding” logic
is disabled entirely.

When the query is being bundled into a subquery for the purposes of
joined eager loading, the “augment column list” rules are necessarily
more aggressive so that the ORDER BY can still be satisfied, so this case
remains unchanged.

[#3641](https://www.sqlalchemy.org/trac/ticket/3641)

### Same-named @validates decorators will now raise an exception

The [validates()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.validates) decorator is only intended to be created once
per class for a particular attribute name.   Creating more than one
now raises an error, whereas previously it would silently pick only the
last defined validator:

```
class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)

    data = Column(String)

    @validates("data")
    def _validate_data_one(self):
        assert "x" in data

    @validates("data")
    def _validate_data_two(self):
        assert "y" in data

configure_mappers()
```

Will raise:

```
sqlalchemy.exc.InvalidRequestError: A validation function for mapped attribute 'data'
on mapper Mapper|A|a already exists.
```

[#3776](https://www.sqlalchemy.org/trac/ticket/3776)

## Key Behavioral Changes - Core

### TextClause.columns() will match columns positionally, not by name, when passed positionally

The new behavior of the [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method, which itself
was recently added as of the 0.9 series, is that when
columns are passed positionally without any additional keyword arguments,
they are linked to the ultimate result set
columns positionally, and no longer on name.   It is hoped that the impact
of this change will be low due to the fact that the method has always been documented
illustrating the columns being passed in the same order as that of the
textual SQL statement, as would seem intuitive, even though the internals
weren’t checking for this.

An application that is using this method by passing [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
to it positionally must ensure that the position of those [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
objects matches the position in which these columns are stated in the
textual SQL.

E.g., code like the following:

```
stmt = text("SELECT id, name, description FROM table")

# no longer matches by name
stmt = stmt.columns(my_table.c.name, my_table.c.description, my_table.c.id)
```

Would no longer work as expected; the order of the columns given is now
significant:

```
# correct version
stmt = stmt.columns(my_table.c.id, my_table.c.name, my_table.c.description)
```

Possibly more likely, a statement that worked like this:

```
stmt = text("SELECT * FROM table")
stmt = stmt.columns(my_table.c.id, my_table.c.name, my_table.c.description)
```

is now slightly risky, as the “*” specification will generally deliver columns
in the order in which they are present in the table itself.  If the structure
of the table changes due to schema changes, this ordering may no longer be the same.
Therefore when using [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns), it’s advised to list out
the desired columns explicitly in the textual SQL, though it’s no longer
necessary to worry about the names themselves in the textual SQL.

See also

[ResultSet column matching enhancements; positional column setup for textual SQL](#change-3501)

### String server_default now literal quoted

A server default passed to [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) as a plain
Python string that has quotes embedded is now
passed through the literal quoting system:

```
>>> from sqlalchemy.schema import MetaData, Table, Column, CreateTable
>>> from sqlalchemy.types import String
>>> t = Table("t", MetaData(), Column("x", String(), server_default="hi ' there"))
>>> print(CreateTable(t))
CREATE TABLE t (
    x VARCHAR DEFAULT 'hi '' there'
)
```

Previously the quote would render directly.     This change may be backwards
incompatible for applications with such a use case who were working around
the issue.

[#3809](https://www.sqlalchemy.org/trac/ticket/3809)

### A UNION or similar of SELECTs with LIMIT/OFFSET/ORDER BY now parenthesizes the embedded selects

An issue that, like others, was long driven by SQLite’s lack of capabilities
has now been enhanced to work on all supporting backends.   We refer to a query that
is a UNION of SELECT statements that themselves contain row-limiting or ordering
features which include LIMIT, OFFSET, and/or ORDER BY:

```
(SELECT x FROM table1 ORDER BY y LIMIT 1) UNION
(SELECT x FROM table2 ORDER BY y LIMIT 2)
```

The above query requires parenthesis within each sub-select in order to
group the sub-results correctly.  Production of the above statement in
SQLAlchemy Core looks like:

```
stmt1 = select([table1.c.x]).order_by(table1.c.y).limit(1)
stmt2 = select([table1.c.x]).order_by(table2.c.y).limit(2)

stmt = union(stmt1, stmt2)
```

Previously, the above construct would not produce parenthesization for the
inner SELECT statements, producing a query that fails on all backends.

The above formats will **continue to fail on SQLite**; additionally, the format
that includes ORDER BY but no LIMIT/SELECT will **continue to fail on Oracle**.
This is not a backwards-incompatible change, because the queries fail without
the parentheses as well; with the fix, the queries at least work on all other
databases.

In all cases, in order to produce a UNION of limited SELECT statements that
also works on SQLite and in all cases on Oracle, the
subqueries must be a SELECT of an ALIAS:

```
stmt1 = select([table1.c.x]).order_by(table1.c.y).limit(1).alias().select()
stmt2 = select([table2.c.x]).order_by(table2.c.y).limit(2).alias().select()

stmt = union(stmt1, stmt2)
```

This workaround works on all SQLAlchemy versions.  In the ORM, it looks like:

```
stmt1 = session.query(Model1).order_by(Model1.y).limit(1).subquery().select()
stmt2 = session.query(Model2).order_by(Model2.y).limit(1).subquery().select()

stmt = session.query(Model1).from_statement(stmt1.union(stmt2))
```

The behavior here has many parallels to the “join rewriting” behavior
introduced in SQLAlchemy 0.9 in [Many JOIN and LEFT OUTER JOIN expressions will no longer be wrapped in (SELECT * FROM ..) AS ANON_1](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-joins-09); however in this case
we have opted not to add new rewriting behavior to accommodate this
case for SQLite.
The existing rewriting behavior is very complicated already, and the case of
UNIONs with parenthesized SELECT statements is much less common than the
“right-nested-join” use case of that feature.

[#2528](https://www.sqlalchemy.org/trac/ticket/2528)

## Dialect Improvements and Changes - PostgreSQL

### Support for INSERT..ON CONFLICT (DO UPDATE | DO NOTHING)

The `ON CONFLICT` clause of `INSERT` added to PostgreSQL as of
version 9.5 is now supported using a PostgreSQL-specific version of the
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) object, via `sqlalchemy.dialects.postgresql.dml.insert()`.
This [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) subclass adds two new methods `Insert.on_conflict_do_update()`
and `Insert.on_conflict_do_nothing()` which implement the full syntax
supported by PostgreSQL 9.5 in this area:

```
from sqlalchemy.dialects.postgresql import insert

insert_stmt = insert(my_table).values(id="some_id", data="some data to insert")

do_update_stmt = insert_stmt.on_conflict_do_update(
    index_elements=[my_table.c.id], set_=dict(data="some data to update")
)

conn.execute(do_update_stmt)
```

The above will render:

```
INSERT INTO my_table (id, data)
VALUES (:id, :data)
ON CONFLICT id DO UPDATE SET data=:data_2
```

See also

[INSERT…ON CONFLICT (Upsert)](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-insert-on-conflict)

[#3529](https://www.sqlalchemy.org/trac/ticket/3529)

### ARRAY and JSON types now correctly specify “unhashable”

As described in [Changes regarding “unhashable” types, impacts deduping of ORM rows](#change-3499), the ORM relies upon being able to
produce a hash function for column values when a query’s selected entities
mixes full ORM entities with column expressions.   The `hashable=False`
flag is now correctly set on all of PG’s “data structure” types, including
[ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) and [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON).
The [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) and [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE)
types already included this flag.  For [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY),
this is conditional based on the [ARRAY.as_tuple](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.params.as_tuple)
flag, however it should no longer be necessary to set this flag
in order to have an array value present in a composed ORM row.

See also

[Changes regarding “unhashable” types, impacts deduping of ORM rows](#change-3499)

[Correct SQL Types are Established from Indexed Access of ARRAY, JSON, HSTORE](#change-3503)

[#3499](https://www.sqlalchemy.org/trac/ticket/3499)

### Correct SQL Types are Established from Indexed Access of ARRAY, JSON, HSTORE

For all three of [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY), [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE),
the SQL type assigned to the expression returned by indexed access, e.g.
`col[someindex]`, should be correct in all cases.

This includes:

- The SQL type assigned to indexed access of an [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) takes into
  account the number of dimensions configured.   An [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) with three
  dimensions will return a SQL expression with a type of [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) of
  one less dimension.  Given a column with type `ARRAY(Integer, dimensions=3)`,
  we can now perform this expression:
  ```
  int_expr = col[5][6][7]  # returns an Integer expression object
  ```
  Previously, the indexed access to `col[5]` would return an expression of
  type [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) where we could no longer perform indexed access
  for the remaining dimensions, unless we used [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) or [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce).
- The [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) types now mirror what PostgreSQL
  itself does for indexed access.  This means that all indexed access for
  a [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) or [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) type returns an expression that itself
  is *always* [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) or [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) itself, unless the
  [Comparator.astext](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext) modifier is used.   This means that whether
  the indexed access of the JSON structure ultimately refers to a string,
  list, number, or other JSON structure, PostgreSQL always considers it
  to be JSON itself unless it is explicitly cast differently.   Like
  the [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) type, this means that it is now straightforward
  to produce JSON expressions with multiple levels of indexed access:
  ```
  json_expr = json_col["key1"]["attr1"][5]
  ```
- The “textual” type that is returned by indexed access of [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE)
  as well as the “textual” type that is returned by indexed access of
  [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) in conjunction with the
  [Comparator.astext](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext) modifier is now configurable; it defaults
  to [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) in both cases but can be set to a user-defined
  type using the [JSON.astext_type](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.params.astext_type) or
  [HSTORE.text_type](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE.params.text_type) parameters.

See also

[The JSON cast() operation now requires .astext is called explicitly](#change-3503-cast)

[#3499](https://www.sqlalchemy.org/trac/ticket/3499) [#3487](https://www.sqlalchemy.org/trac/ticket/3487)

### The JSON cast() operation now requires.astextis called explicitly

As part of the changes in [Correct SQL Types are Established from Indexed Access of ARRAY, JSON, HSTORE](#change-3503), the workings of the
[ColumnElement.cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast) operator on [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and
[JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) no longer implicitly invoke the
[Comparator.astext](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext) modifier; PostgreSQL’s JSON/JSONB types
support CAST operations to each other without the “astext” aspect.

This means that in most cases, an application that was doing this:

```
expr = json_col["somekey"].cast(Integer)
```

Will now need to change to this:

```
expr = json_col["somekey"].astext.cast(Integer)
```

### ARRAY with ENUM will now emit CREATE TYPE for the ENUM

A table definition like the following will now emit CREATE TYPE
as expected:

```
enum = Enum(
    "manager",
    "place_admin",
    "carwash_admin",
    "parking_admin",
    "service_admin",
    "tire_admin",
    "mechanic",
    "carwasher",
    "tire_mechanic",
    name="work_place_roles",
)

class WorkPlacement(Base):
    __tablename__ = "work_placement"
    id = Column(Integer, primary_key=True)
    roles = Column(ARRAY(enum))

e = create_engine("postgresql://scott:tiger@localhost/test", echo=True)
Base.metadata.create_all(e)
```

emits:

```
CREATE TYPE work_place_roles AS ENUM (
    'manager', 'place_admin', 'carwash_admin', 'parking_admin',
    'service_admin', 'tire_admin', 'mechanic', 'carwasher',
    'tire_mechanic')

CREATE TABLE work_placement (
    id SERIAL NOT NULL,
    roles work_place_roles[],
    PRIMARY KEY (id)
)
```

[#2729](https://www.sqlalchemy.org/trac/ticket/2729)

### Check constraints now reflect

The PostgreSQL dialect now supports reflection of CHECK constraints
both within the method [Inspector.get_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints) as well
as within [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) reflection within the [Table.constraints](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.constraints)
collection.

### “Plain” and “Materialized” views can be inspected separately

The new argument `PGInspector.get_view_names.include`
allows specification of which sub-types of views should be returned:

```
from sqlalchemy import inspect

insp = inspect(engine)

plain_views = insp.get_view_names(include="plain")
all_views = insp.get_view_names(include=("plain", "materialized"))
```

[#3588](https://www.sqlalchemy.org/trac/ticket/3588)

### Added tablespace option to Index

The [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) object now accepts the argument `postgresql_tablespace`
in order to specify TABLESPACE, the same way as accepted by the
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.

See also

[Index Storage Parameters](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-index-storage)

[#3720](https://www.sqlalchemy.org/trac/ticket/3720)

### Support for PyGreSQL

The [PyGreSQL](https://pypi.org/project/PyGreSQL) DBAPI is now supported.

### The “postgres” module is removed

The `sqlalchemy.dialects.postgres` module, long deprecated, is
removed; this has emitted a warning for many years and projects
should be calling upon `sqlalchemy.dialects.postgresql`.
Engine URLs of the form `postgres://` will still continue to function,
however.

### Support for FOR UPDATE SKIP LOCKED  / FOR NO KEY UPDATE / FOR KEY SHARE

The new parameters [GenerativeSelect.with_for_update.skip_locked](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.skip_locked)
and [GenerativeSelect.with_for_update.key_share](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.key_share)
in both Core and ORM apply a modification to a “SELECT…FOR UPDATE”
or “SELECT…FOR SHARE” query on the PostgreSQL backend:

- SELECT FOR NO KEY UPDATE:
  ```
  stmt = select([table]).with_for_update(key_share=True)
  ```
- SELECT FOR UPDATE SKIP LOCKED:
  ```
  stmt = select([table]).with_for_update(skip_locked=True)
  ```
- SELECT FOR KEY SHARE:
  ```
  stmt = select([table]).with_for_update(read=True, key_share=True)
  ```

## Dialect Improvements and Changes - MySQL

### MySQL JSON Support

A new type [JSON](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.JSON) is added to the MySQL dialect supporting
the JSON type newly added to MySQL 5.7.   This type provides both persistence
of JSON as well as rudimentary indexed-access using the `JSON_EXTRACT`
function internally.  An indexable JSON column that works across MySQL
and PostgreSQL can be achieved by using the [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) datatype
common to both MySQL and PostgreSQL.

See also

[JSON support added to Core](#change-3619)

[#3547](https://www.sqlalchemy.org/trac/ticket/3547)

### Added support for AUTOCOMMIT “isolation level”

The MySQL dialect now accepts the value “AUTOCOMMIT” for the
[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) and
[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
parameters:

```
connection = engine.connect()
connection = connection.execution_options(isolation_level="AUTOCOMMIT")
```

The isolation level makes use of the various “autocommit” attributes
provided by most MySQL DBAPIs.

[#3332](https://www.sqlalchemy.org/trac/ticket/3332)

### No more generation of an implicit KEY for composite primary key w/ AUTO_INCREMENT

The MySQL dialect had the behavior such that if a composite primary key
on an InnoDB table featured AUTO_INCREMENT on one of its columns which was
not the first column, e.g.:

```
t = Table(
    "some_table",
    metadata,
    Column("x", Integer, primary_key=True, autoincrement=False),
    Column("y", Integer, primary_key=True, autoincrement=True),
    mysql_engine="InnoDB",
)
```

DDL such as the following would be generated:

```
CREATE TABLE some_table (
    x INTEGER NOT NULL,
    y INTEGER NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (x, y),
    KEY idx_autoinc_y (y)
)ENGINE=InnoDB
```

Note the above “KEY” with an auto-generated name; this is a change that
found its way into the dialect many years ago in response to the issue that
the AUTO_INCREMENT would otherwise fail on InnoDB without this additional KEY.

This workaround has been removed and replaced with the much better system
of just stating the AUTO_INCREMENT column *first* within the primary key:

```
CREATE TABLE some_table (
    x INTEGER NOT NULL,
    y INTEGER NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (y, x)
)ENGINE=InnoDB
```

To maintain explicit control of the ordering of primary key columns,
use the [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) construct explicitly (1.1.0b2)
(along with a KEY for the autoincrement column as required by MySQL), e.g.:

```
t = Table(
    "some_table",
    metadata,
    Column("x", Integer, primary_key=True),
    Column("y", Integer, primary_key=True, autoincrement=True),
    PrimaryKeyConstraint("x", "y"),
    UniqueConstraint("y"),
    mysql_engine="InnoDB",
)
```

Along with the change [The .autoincrement directive is no longer implicitly enabled for a composite primary key column](#change-3216), composite primary keys with
or without auto increment are now easier to specify;
[Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement)
now defaults to the value `"auto"` and the `autoincrement=False`
directives are no longer needed:

```
t = Table(
    "some_table",
    metadata,
    Column("x", Integer, primary_key=True),
    Column("y", Integer, primary_key=True, autoincrement=True),
    mysql_engine="InnoDB",
)
```

## Dialect Improvements and Changes - SQLite

### Right-nested join workaround lifted for SQLite version 3.7.16

In version 0.9, the feature introduced by [Many JOIN and LEFT OUTER JOIN expressions will no longer be wrapped in (SELECT * FROM ..) AS ANON_1](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-joins-09) went
through lots of effort to support rewriting of joins on SQLite to always
use subqueries in order to achieve a “right-nested-join” effect, as
SQLite has not supported this syntax for many years.  Ironically,
the version of SQLite noted in that migration note, 3.7.15.2, was the *last*
version of SQLite to actually have this limitation!   The next release was
3.7.16 and support for right nested joins was quietly added.   In 1.1, the work
to identify the specific SQLite version and source commit where this change
was made was done (SQLite’s changelog refers to it with the cryptic phrase “Enhance
the query optimizer to exploit transitive join constraints” without linking
to any issue number, change number, or further explanation), and the workarounds
present in this change are now lifted for SQLite when the DBAPI reports
that version 3.7.16 or greater is in effect.

[#3634](https://www.sqlalchemy.org/trac/ticket/3634)

### Dotted column names workaround lifted for SQLite version 3.10.0

The SQLite dialect has long had a workaround for an issue where the database
driver does not report the correct column names for some SQL result sets, in
particular when UNION is used.  The workaround is detailed at
[Dotted Column Names](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-dotted-column-names), and requires that SQLAlchemy assume that any
column name with a dot in it is actually a `tablename.columnname` combination
delivered via this buggy behavior, with an option to turn it off via the
`sqlite_raw_colnames` execution option.

As of SQLite version 3.10.0, the bug in UNION and other queries has been fixed;
like the change described in [Right-nested join workaround lifted for SQLite version 3.7.16](#change-3634), SQLite’s changelog only
identifies it cryptically as “Added the colUsed field to sqlite3_index_info for
use by the sqlite3_module.xBestIndex method”, however SQLAlchemy’s translation
of these dotted column names is no longer required with this version, so is
turned off when version 3.10.0 or greater is detected.

Overall, the SQLAlchemy `ResultProxy` as of the 1.0 series relies much
less on column names in result sets when delivering results for Core and ORM
SQL constructs, so the importance of this issue was already lessened in any
case.

[#3633](https://www.sqlalchemy.org/trac/ticket/3633)

### Improved Support for Remote Schemas

The SQLite dialect now implements [Inspector.get_schema_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_schema_names)
and additionally has improved support for tables and indexes that are
created and reflected from a remote schema, which in SQLite is a
database that is assigned a name via the `ATTACH` statement; previously,
the``CREATE INDEX`` DDL didn’t work correctly for a schema-bound table
and the [Inspector.get_foreign_keys()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_foreign_keys) method will now indicate the
given schema in the results.  Cross-schema foreign keys aren’t supported.

### Reflection of the name of PRIMARY KEY constraints

The SQLite backend now takes advantage of the “sqlite_master” view
of SQLite in order to extract the name of the primary key constraint
of a table from the original DDL, in the same way that is achieved for
foreign key constraints in recent SQLAlchemy versions.

[#3629](https://www.sqlalchemy.org/trac/ticket/3629)

### Check constraints now reflect

The SQLite dialect now supports reflection of CHECK constraints
both within the method [Inspector.get_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints) as well
as within [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) reflection within the [Table.constraints](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.constraints)
collection.

### ON DELETE and ON UPDATE foreign key phrases now reflect

The [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) will now include ON DELETE and ON UPDATE
phrases from foreign key constraints on the SQLite dialect, and the
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object as reflected as part of a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) will also indicate these phrases.

## Dialect Improvements and Changes - SQL Server

### Added transaction isolation level support for SQL Server

All SQL Server dialects support transaction isolation level settings
via the [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) and
[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
parameters.  The four standard levels are supported as well as
`SNAPSHOT`:

```
engine = create_engine(
    "mssql+pyodbc://scott:tiger@ms_2008", isolation_level="REPEATABLE READ"
)
```

See also

[Transaction Isolation Level](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-isolation-level)

[#3534](https://www.sqlalchemy.org/trac/ticket/3534)

### String / varlength types no longer represent “max” explicitly on reflection

When reflecting a type such as [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String), [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause), etc.
which includes a length, an “un-lengthed” type under SQL Server would
copy the “length” parameter as the value `"max"`:

```
>>> from sqlalchemy import create_engine, inspect
>>> engine = create_engine("mssql+pyodbc://scott:tiger@ms_2008", echo=True)
>>> engine.execute("create table s (x varchar(max), y varbinary(max))")
>>> insp = inspect(engine)
>>> for col in insp.get_columns("s"):
...     print(col["type"].__class__, col["type"].length)
<class 'sqlalchemy.sql.sqltypes.VARCHAR'> max
<class 'sqlalchemy.dialects.mssql.base.VARBINARY'> max
```

The “length” parameter in the base types is expected to be an integer value
or None only; None indicates unbounded length which the SQL Server dialect
interprets as “max”.   The fix then is so that these lengths come
out as None, so that the type objects work in non-SQL Server contexts:

```
>>> for col in insp.get_columns("s"):
...     print(col["type"].__class__, col["type"].length)
<class 'sqlalchemy.sql.sqltypes.VARCHAR'> None
<class 'sqlalchemy.dialects.mssql.base.VARBINARY'> None
```

Applications which may have been relying on a direct comparison of the “length”
value to the string “max” should consider the value of `None` to mean
the same thing.

[#3504](https://www.sqlalchemy.org/trac/ticket/3504)

### Support for “non clustered” on primary key to allow clustered elsewhere

The `mssql_clustered` flag available on [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint),
[PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint), [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) now defaults to `None`, and
can be set to False which will render the NONCLUSTERED keyword in particular
for a primary key, allowing a different index to be used as “clustered”.

See also

[Clustered Index Support](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-indexes)

### The legacy_schema_aliasing flag is now set to False

SQLAlchemy 1.0.5 introduced the `legacy_schema_aliasing` flag to the
MSSQL dialect, allowing so-called “legacy mode” aliasing to be turned off.
This aliasing attempts to turn schema-qualified tables into aliases;
given a table such as:

```
account_table = Table(
    "account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("info", String(100)),
    schema="customer_schema",
)
```

The legacy mode of behavior will attempt to turn a schema-qualified table
name into an alias:

```
>>> eng = create_engine("mssql+pymssql://mydsn", legacy_schema_aliasing=True)
>>> print(account_table.select().compile(eng))
SELECT account_1.id, account_1.info
FROM customer_schema.account AS account_1
```

However, this aliasing has been shown to be unnecessary and in many cases
produces incorrect SQL.

In SQLAlchemy 1.1, the `legacy_schema_aliasing` flag now defaults to
False, disabling this mode of behavior and allowing the MSSQL dialect to behave
normally with schema-qualified tables.  For applications which may rely
on this behavior, set the flag back to True.

[#3434](https://www.sqlalchemy.org/trac/ticket/3434)

## Dialect Improvements and Changes - Oracle

### Support for SKIP LOCKED

The new parameter [GenerativeSelect.with_for_update.skip_locked](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.skip_locked)
in both Core and ORM will generate the “SKIP LOCKED” suffix for a
“SELECT…FOR UPDATE” or “SELECT.. FOR SHARE” query.
