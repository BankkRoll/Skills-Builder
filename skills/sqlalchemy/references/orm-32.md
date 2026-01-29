# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

ORM Querying Guide

This page is part of the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).

Previous: [Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html)   |   Next: [ORM API Features for Querying](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html)

# Relationship Loading Techniques

About this Document

This section presents an in-depth view of how to load related
objects.   Readers should be familiar with
[Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html) and basic use.

Most examples here assume the “User/Address” mapping setup similar
to the one illustrated at [setup for selects](https://docs.sqlalchemy.org/en/20/orm/queryguide/_plain_setup.html).

A big part of SQLAlchemy is providing a wide range of control over how related
objects get loaded when querying.   By “related objects” we refer to collections
or scalar associations configured on a mapper using [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).
This behavior can be configured at mapper construction time using the
[relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy) parameter to the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
function, as well as by using **ORM loader options** with
the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct.

The loading of relationships falls into three categories; **lazy** loading,
**eager** loading, and **no** loading. Lazy loading refers to objects that are returned
from a query without the related
objects loaded at first.  When the given collection or reference is
first accessed on a particular object, an additional SELECT statement
is emitted such that the requested collection is loaded.

Eager loading refers to objects returned from a query with the related
collection or scalar reference already loaded up front.  The ORM
achieves this either by augmenting the SELECT statement it would normally
emit with a JOIN to load in related rows simultaneously, or by emitting
additional SELECT statements after the primary one to load collections
or scalar references at once.

“No” loading refers to the disabling of loading on a given relationship, either
that the attribute is empty and is just never loaded, or that it raises
an error when it is accessed, in order to guard against unwanted lazy loads.

## Summary of Relationship Loading Styles

The primary forms of relationship loading are:

- **lazy loading** - available via `lazy='select'` or the [lazyload()](#sqlalchemy.orm.lazyload)
  option, this is the form of loading that emits a SELECT statement at
  attribute access time to lazily load a related reference on a single
  object at a time.  Lazy loading is the **default loading style** for all
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs that don’t otherwise indicate the
  [relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy) option.  Lazy loading is detailed at
  [Lazy Loading](#lazy-loading).
- **select IN loading** - available via `lazy='selectin'` or the [selectinload()](#sqlalchemy.orm.selectinload)
  option, this form of loading emits a second (or more) SELECT statement which
  assembles the primary key identifiers of the parent objects into an IN clause,
  so that all members of related collections / scalar references are loaded at once
  by primary key.  Select IN loading is detailed at [Select IN loading](#selectin-eager-loading).
- **joined loading** - available via `lazy='joined'` or the [joinedload()](#sqlalchemy.orm.joinedload)
  option, this form of loading applies a JOIN to the given SELECT statement
  so that related rows are loaded in the same result set.   Joined eager loading
  is detailed at [Joined Eager Loading](#joined-eager-loading).
- **raise loading** - available via `lazy='raise'`, `lazy='raise_on_sql'`,
  or the [raiseload()](#sqlalchemy.orm.raiseload) option, this form of loading is triggered at the
  same time a lazy load would normally occur, except it raises an ORM exception
  in order to guard against the application making unwanted lazy loads.
  An introduction to raise loading is at [Preventing unwanted lazy loads using raiseload](#prevent-lazy-with-raiseload).
- **subquery loading** - available via `lazy='subquery'` or the [subqueryload()](#sqlalchemy.orm.subqueryload)
  option, this form of loading emits a second SELECT statement which re-states the
  original query embedded inside of a subquery, then JOINs that subquery to the
  related table to be loaded to load all members of related collections / scalar
  references at once.  Subquery eager loading is detailed at [Subquery Eager Loading](#subquery-eager-loading).
- **write only loading** - available via `lazy='write_only'`, or by
  annotating the left side of the [Relationship](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Relationship) object using the
  [WriteOnlyMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyMapped) annotation.   This collection-only
  loader style produces an alternative attribute instrumentation that never
  implicitly loads records from the database, instead only allowing
  [WriteOnlyCollection.add()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.add),
  [WriteOnlyCollection.add_all()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.add_all) and [WriteOnlyCollection.remove()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.remove)
  methods.  Querying the collection is performed by invoking a SELECT statement
  which is constructed using the [WriteOnlyCollection.select()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.select)
  method.    Write only loading is discussed at [Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship).
- **dynamic loading** - available via `lazy='dynamic'`, or by
  annotating the left side of the [Relationship](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Relationship) object using the
  [DynamicMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.DynamicMapped) annotation. This is a legacy collection-only
  loader style which produces a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object when the collection
  is accessed, allowing custom SQL to be emitted against the collection’s
  contents. However, dynamic loaders will implicitly iterate the underlying
  collection in various circumstances which makes them less useful for managing
  truly large collections. Dynamic loaders are superseded by
  [“write only”](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship) collections, which will prevent
  the underlying collection from being implicitly loaded under any
  circumstances. Dynamic loaders are discussed at [Dynamic Relationship Loaders](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#dynamic-relationship).

## Configuring Loader Strategies at Mapping Time

The loader strategy for a particular relationship can be configured
at mapping time to take place in all cases where an object of the mapped
type is loaded, in the absence of any query-level options that modify it.
This is configured using the [relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy) parameter to
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship); common values for this parameter
include `select`, `selectin` and `joined`.

The example below illustrates the relationship example at
[One To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns-o2m), configuring the `Parent.children`
relationship to use [Select IN loading](#selectin-eager-loading) when a SELECT
statement for `Parent` objects is emitted:

```
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Parent(Base):
    __tablename__ = "parent"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(lazy="selectin")

class Child(Base):
    __tablename__ = "child"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
```

Above, whenever a collection of `Parent` objects are loaded, each
`Parent` will also have its `children` collection populated, using
the `"selectin"` loader strategy that emits a second query.

The default value of the [relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy) argument is
`"select"`, which indicates [Lazy Loading](#lazy-loading).

## Relationship Loading with Loader Options

The other, and possibly more common way to configure loading strategies
is to set them up on a per-query basis against specific attributes using the
[Select.options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.options) method.  Very detailed
control over relationship loading is available using loader options;
the most common are
[joinedload()](#sqlalchemy.orm.joinedload), [selectinload()](#sqlalchemy.orm.selectinload)
and [lazyload()](#sqlalchemy.orm.lazyload).   The option accepts a class-bound attribute
referring to the specific class/attribute that should be targeted:

```
from sqlalchemy import select
from sqlalchemy.orm import lazyload

# set children to load lazily
stmt = select(Parent).options(lazyload(Parent.children))

from sqlalchemy.orm import joinedload

# set children to load eagerly with a join
stmt = select(Parent).options(joinedload(Parent.children))
```

The loader options can also be “chained” using **method chaining**
to specify how loading should occur further levels deep:

```
from sqlalchemy import select
from sqlalchemy.orm import joinedload

stmt = select(Parent).options(
    joinedload(Parent.children).subqueryload(Child.subelements)
)
```

Chained loader options can be applied against a “lazy” loaded collection.
This means that when a collection or association is lazily loaded upon
access, the specified option will then take effect:

```
from sqlalchemy import select
from sqlalchemy.orm import lazyload

stmt = select(Parent).options(lazyload(Parent.children).subqueryload(Child.subelements))
```

Above, the query will return `Parent` objects without the `children`
collections loaded.  When the `children` collection on a particular
`Parent` object is first accessed, it will lazy load the related
objects, but additionally apply eager loading to the `subelements`
collection on each member of `children`.

### Adding Criteria to loader options

The relationship attributes used to indicate loader options include the
ability to add additional filtering criteria to the ON clause of the join
that’s created, or to the WHERE criteria involved, depending on the loader
strategy.  This can be achieved using the [PropComparator.and_()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.and_)
method which will pass through an option such that loaded results are limited
to the given filter criteria:

```
from sqlalchemy import select
from sqlalchemy.orm import lazyload

stmt = select(A).options(lazyload(A.bs.and_(B.id > 5)))
```

When using limiting criteria, if a particular collection is already loaded
it won’t be refreshed; to ensure the new criteria takes place, apply
the [Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing) execution option:

```
from sqlalchemy import select
from sqlalchemy.orm import lazyload

stmt = (
    select(A)
    .options(lazyload(A.bs.and_(B.id > 5)))
    .execution_options(populate_existing=True)
)
```

In order to add filtering criteria to all occurrences of an entity throughout
a query, regardless of loader strategy or where it occurs in the loading
process, see the [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) function.

Added in version 1.4.

### Specifying Sub-Options with Load.options()

Using method chaining, the loader style of each link in the path is explicitly
stated.  To navigate along a path without changing the existing loader style
of a particular attribute, the [defaultload()](#sqlalchemy.orm.defaultload) method/function may be used:

```
from sqlalchemy import select
from sqlalchemy.orm import defaultload

stmt = select(A).options(defaultload(A.atob).joinedload(B.btoc))
```

A similar approach can be used to specify multiple sub-options at once, using
the [Load.options()](#sqlalchemy.orm.Load.options) method:

```
from sqlalchemy import select
from sqlalchemy.orm import defaultload
from sqlalchemy.orm import joinedload

stmt = select(A).options(
    defaultload(A.atob).options(joinedload(B.btoc), joinedload(B.btod))
)
```

See also

[Using load_only() on related objects and collections](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#orm-queryguide-load-only-related) - illustrates examples of combining
relationship and column-oriented loader options.

Note

The loader options applied to an object’s lazy-loaded collections
are **“sticky”** to specific object instances, meaning they will persist
upon collections loaded by that specific object for as long as it exists in
memory.  For example, given the previous example:

```
stmt = select(Parent).options(lazyload(Parent.children).subqueryload(Child.subelements))
```

if the `children` collection on a particular `Parent` object loaded by
the above query is expired (such as when a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s
transaction is committed or rolled back, or [Session.expire_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire_all) is
used), when the `Parent.children` collection is next accessed in order to
re-load it, the `Child.subelements` collection will again be loaded using
subquery eager loading. This stays the case even if the above `Parent`
object is accessed from a subsequent query that specifies a different set of
options. To change the options on an existing object without expunging it
and re-loading, they must be set explicitly in conjunction using the
[Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing) execution option:

```
# change the options on Parent objects that were already loaded
stmt = (
    select(Parent)
    .execution_options(populate_existing=True)
    .options(lazyload(Parent.children).lazyload(Child.subelements))
    .all()
)
```

If the objects loaded above are fully cleared from the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
such as due to garbage collection or that [Session.expunge_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expunge_all)
were used, the “sticky” options will also be gone and the newly created
objects will make use of new options if loaded again.

A future SQLAlchemy release may add more alternatives to manipulating
the loader options on already-loaded objects.

## Lazy Loading

By default, all inter-object relationships are **lazy loading**. The scalar or
collection attribute associated with a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
contains a trigger which fires the first time the attribute is accessed.  This
trigger typically issues a SQL call at the point of access
in order to load the related object or objects:

```
>>> spongebob.addresses
SELECT
    addresses.id AS addresses_id,
    addresses.email_address AS addresses_email_address,
    addresses.user_id AS addresses_user_id
FROM addresses
WHERE ? = addresses.user_id
[5]
[<Address(u'[email protected]')>, <Address(u'[email protected]')>]
```

The one case where SQL is not emitted is for a simple many-to-one relationship, when
the related object can be identified by its primary key alone and that object is already
present in the current [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  For this reason, while lazy loading
can be expensive for related collections, in the case that one is loading
lots of objects with simple many-to-ones against a relatively small set of
possible target objects, lazy loading may be able to refer to these objects locally
without emitting as many SELECT statements as there are parent objects.

This default behavior of “load upon attribute access” is known as “lazy” or
“select” loading - the name “select” because a “SELECT” statement is typically emitted
when the attribute is first accessed.

Lazy loading can be enabled for a given attribute that is normally
configured in some other way using the [lazyload()](#sqlalchemy.orm.lazyload) loader option:

```
from sqlalchemy import select
from sqlalchemy.orm import lazyload

# force lazy loading for an attribute that is set to
# load some other way normally
stmt = select(User).options(lazyload(User.addresses))
```

### Preventing unwanted lazy loads using raiseload

The [lazyload()](#sqlalchemy.orm.lazyload) strategy produces an effect that is one of the most
common issues referred to in object relational mapping; the
[N plus one problem](https://docs.sqlalchemy.org/en/20/glossary.html#term-N-plus-one-problem), which states that for any N objects loaded,
accessing their lazy-loaded attributes means there will be N+1 SELECT
statements emitted.  In SQLAlchemy, the usual mitigation for the N+1 problem
is to make use of its very capable eager load system.  However, eager loading
requires that the attributes which are to be loaded be specified with the
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) up front.  The problem of code that may access other attributes
that were not eagerly loaded, where lazy loading is not desired, may be
addressed using the [raiseload()](#sqlalchemy.orm.raiseload) strategy; this loader strategy
replaces the behavior of lazy loading with an informative error being
raised:

```
from sqlalchemy import select
from sqlalchemy.orm import raiseload

stmt = select(User).options(raiseload(User.addresses))
```

Above, a `User` object loaded from the above query will not have
the `.addresses` collection loaded; if some code later on attempts to
access this attribute, an ORM exception is raised.

[raiseload()](#sqlalchemy.orm.raiseload) may be used with a so-called “wildcard” specifier to
indicate that all relationships should use this strategy.  For example,
to set up only one attribute as eager loading, and all the rest as raise:

```
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import raiseload

stmt = select(Order).options(joinedload(Order.items), raiseload("*"))
```

The above wildcard will apply to **all** relationships not just on `Order`
besides `items`, but all those on the `Item` objects as well.  To set up
[raiseload()](#sqlalchemy.orm.raiseload) for only the `Order` objects, specify a full
path with [Load](#sqlalchemy.orm.Load):

```
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Load

stmt = select(Order).options(joinedload(Order.items), Load(Order).raiseload("*"))
```

Conversely, to set up the raise for just the `Item` objects:

```
stmt = select(Order).options(joinedload(Order.items).raiseload("*"))
```

The [raiseload()](#sqlalchemy.orm.raiseload) option applies only to relationship attributes.  For
column-oriented attributes, the [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) option supports the
[defer.raiseload](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer.params.raiseload) option which works in the same way.

Tip

The “raiseload” strategies **do not apply**
within the [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) flush process.   That means if the
[Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush) process needs to load a collection in order
to finish its work, it will do so while bypassing any [raiseload()](#sqlalchemy.orm.raiseload)
directives.

See also

[Wildcard Loading Strategies](#wildcard-loader-strategies)

[Using raiseload to prevent deferred column loads](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#orm-queryguide-deferred-raiseload)

## Joined Eager Loading

Joined eager loading is the oldest style of eager loading included with
the SQLAlchemy ORM.  It works by connecting a JOIN (by default
a LEFT OUTER join) to the SELECT statement emitted,
and populates the target scalar/collection from the
same result set as that of the parent.

At the mapping level, this looks like:

```
class Address(Base):
    # ...

    user: Mapped[User] = relationship(lazy="joined")
```

Joined eager loading is usually applied as an option to a query, rather than
as a default loading option on the mapping, in particular when used for
collections rather than many-to-one-references.   This is achieved
using the [joinedload()](#sqlalchemy.orm.joinedload) loader option:

```
>>> from sqlalchemy import select
>>> from sqlalchemy.orm import joinedload
>>> stmt = select(User).options(joinedload(User.addresses)).filter_by(name="spongebob")
>>> spongebob = session.scalars(stmt).unique().all()
SELECT
    addresses_1.id AS addresses_1_id,
    addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id,
    users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users
LEFT OUTER JOIN addresses AS addresses_1
    ON users.id = addresses_1.user_id
WHERE users.name = ?
['spongebob']
```

Tip

When including [joinedload()](#sqlalchemy.orm.joinedload) in reference to a one-to-many or
many-to-many collection, the [Result.unique()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.unique) method must be
applied to the returned result, which will uniquify the incoming rows by
primary key that otherwise are multiplied out by the join. The ORM will
raise an error if this is not present.

This is not automatic in modern SQLAlchemy, as it changes the behavior
of the result set to return fewer ORM objects than the statement would
normally return in terms of number of rows.  Therefore SQLAlchemy keeps
the use of [Result.unique()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.unique) explicit, so there’s no ambiguity
that the returned objects are being uniqified on primary key.

The JOIN emitted by default is a LEFT OUTER JOIN, to allow for a lead object
that does not refer to a related row.  For an attribute that is guaranteed
to have an element, such as a many-to-one
reference to a related object where the referencing foreign key is NOT NULL,
the query can be made more efficient by using an inner join; this is available
at the mapping level via the [relationship.innerjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.innerjoin) flag:

```
class Address(Base):
    # ...

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(lazy="joined", innerjoin=True)
```

At the query option level, via the [joinedload.innerjoin](#sqlalchemy.orm.joinedload.params.innerjoin) flag:

```
from sqlalchemy import select
from sqlalchemy.orm import joinedload

stmt = select(Address).options(joinedload(Address.user, innerjoin=True))
```

The JOIN will right-nest itself when applied in a chain that includes
an OUTER JOIN:

```
>>> from sqlalchemy import select
>>> from sqlalchemy.orm import joinedload
>>> stmt = select(User).options(
...     joinedload(User.addresses).joinedload(Address.widgets, innerjoin=True)
... )
>>> results = session.scalars(stmt).unique().all()
SELECT
    widgets_1.id AS widgets_1_id,
    widgets_1.name AS widgets_1_name,
    addresses_1.id AS addresses_1_id,
    addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id,
    users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users
LEFT OUTER JOIN (
    addresses AS addresses_1 JOIN widgets AS widgets_1 ON
    addresses_1.widget_id = widgets_1.id
) ON users.id = addresses_1.user_id
```

Tip

If using database row locking techniques when emitting the SELECT,
meaning the [Select.with_for_update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update) method is being used
to emit SELECT..FOR UPDATE, the joined table may be locked as well,
depending on the behavior of the backend in use.   It’s not recommended
to use joined eager loading at the same time as SELECT..FOR UPDATE
for this reason.

### The Zen of Joined Eager Loading

Since joined eager loading seems to have many resemblances to the use of
[Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join), it often produces confusion as to when and how it should
be used.   It is critical to understand the distinction that while
[Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) is used to alter the results of a query, [joinedload()](#sqlalchemy.orm.joinedload)
goes through great lengths to **not** alter the results of the query, and
instead hide the effects of the rendered join to only allow for related objects
to be present.

The philosophy behind loader strategies is that any set of loading schemes can
be applied to a particular query, and *the results don’t change* - only the
number of SQL statements required to fully load related objects and collections
changes. A particular query might start out using all lazy loads.   After using
it in context, it might be revealed that particular attributes or collections
are always accessed, and that it would be more efficient to change the loader
strategy for these.   The strategy can be changed with no other modifications
to the query, the results will remain identical, but fewer SQL statements would
be emitted. In theory (and pretty much in practice), nothing you can do to the
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) would make it load a different set of primary or related
objects based on a change in loader strategy.

How [joinedload()](#sqlalchemy.orm.joinedload) in particular achieves this result of not impacting
entity rows returned in any way is that it creates an anonymous alias of the
joins it adds to your query, so that they can’t be referenced by other parts of
the query.   For example, the query below uses [joinedload()](#sqlalchemy.orm.joinedload) to create a
LEFT OUTER JOIN from `users` to `addresses`, however the `ORDER BY` added
against `Address.email_address` is not valid - the `Address` entity is not
named in the query:

```
>>> from sqlalchemy import select
>>> from sqlalchemy.orm import joinedload
>>> stmt = (
...     select(User)
...     .options(joinedload(User.addresses))
...     .filter(User.name == "spongebob")
...     .order_by(Address.email_address)
... )
>>> result = session.scalars(stmt).unique().all()
SELECT
    addresses_1.id AS addresses_1_id,
    addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id,
    users.id AS users_id,
    users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users
LEFT OUTER JOIN addresses AS addresses_1
    ON users.id = addresses_1.user_id
WHERE users.name = ?
ORDER BY addresses.email_address   <-- this part is wrong !
['spongebob']
```

Above, `ORDER BY addresses.email_address` is not valid since `addresses` is not in the
FROM list.   The correct way to load the `User` records and order by email
address is to use [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join):

```
>>> from sqlalchemy import select
>>> stmt = (
...     select(User)
...     .join(User.addresses)
...     .filter(User.name == "spongebob")
...     .order_by(Address.email_address)
... )
>>> result = session.scalars(stmt).unique().all()
SELECT
    users.id AS users_id,
    users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users
JOIN addresses ON users.id = addresses.user_id
WHERE users.name = ?
ORDER BY addresses.email_address
['spongebob']
```

The statement above is of course not the same as the previous one, in that the
columns from `addresses` are not included in the result at all.   We can add
[joinedload()](#sqlalchemy.orm.joinedload) back in, so that there are two joins - one is that which we
are ordering on, the other is used anonymously to load the contents of the
`User.addresses` collection:

```
>>> stmt = (
...     select(User)
...     .join(User.addresses)
...     .options(joinedload(User.addresses))
...     .filter(User.name == "spongebob")
...     .order_by(Address.email_address)
... )
>>> result = session.scalars(stmt).unique().all()
SELECT
    addresses_1.id AS addresses_1_id,
    addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id,
    users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users JOIN addresses
    ON users.id = addresses.user_id
LEFT OUTER JOIN addresses AS addresses_1
    ON users.id = addresses_1.user_id
WHERE users.name = ?
ORDER BY addresses.email_address
['spongebob']
```

What we see above is that our usage of [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) is to supply JOIN
clauses we’d like to use in subsequent query criterion, whereas our usage of
[joinedload()](#sqlalchemy.orm.joinedload) only concerns itself with the loading of the
`User.addresses` collection, for each `User` in the result. In this case,
the two joins most probably appear redundant - which they are.  If we wanted to
use just one JOIN for collection loading as well as ordering, we use the
[contains_eager()](#sqlalchemy.orm.contains_eager) option, described in [Routing Explicit Joins/Statements into Eagerly Loaded Collections](#contains-eager) below.   But
to see why [joinedload()](#sqlalchemy.orm.joinedload) does what it does, consider if we were
**filtering** on a particular `Address`:

```
>>> stmt = (
...     select(User)
...     .join(User.addresses)
...     .options(joinedload(User.addresses))
...     .filter(User.name == "spongebob")
...     .filter(Address.email_address == "[email protected]")
... )
>>> result = session.scalars(stmt).unique().all()
SELECT
    addresses_1.id AS addresses_1_id,
    addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id,
    users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users JOIN addresses
    ON users.id = addresses.user_id
LEFT OUTER JOIN addresses AS addresses_1
    ON users.id = addresses_1.user_id
WHERE users.name = ? AND addresses.email_address = ?
['spongebob', '[email protected]']
```

Above, we can see that the two JOINs have very different roles.  One will match
exactly one row, that of the join of `User` and `Address` where
`Address.email_address=='someaddress@foo.com'`. The other LEFT OUTER JOIN
will match *all* `Address` rows related to `User`, and is only used to
populate the `User.addresses` collection, for those `User` objects that are
returned.

By changing the usage of [joinedload()](#sqlalchemy.orm.joinedload) to another style of loading, we
can change how the collection is loaded completely independently of SQL used to
retrieve the actual `User` rows we want.  Below we change [joinedload()](#sqlalchemy.orm.joinedload)
into [selectinload()](#sqlalchemy.orm.selectinload):

```
>>> stmt = (
...     select(User)
...     .join(User.addresses)
...     .options(selectinload(User.addresses))
...     .filter(User.name == "spongebob")
...     .filter(Address.email_address == "[email protected]")
... )
>>> result = session.scalars(stmt).all()
SELECT
    users.id AS users_id,
    users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users
JOIN addresses ON users.id = addresses.user_id
WHERE
    users.name = ?
    AND addresses.email_address = ?
['spongebob', '[email protected]']
# ... selectinload() emits a SELECT in order
# to load all address records ...
```

When using joined eager loading, if the query contains a modifier that impacts
the rows returned externally to the joins, such as when using DISTINCT, LIMIT,
OFFSET or equivalent, the completed statement is first wrapped inside a
subquery, and the joins used specifically for joined eager loading are applied
to the subquery.   SQLAlchemy’s joined eager loading goes the extra mile, and
then ten miles further, to absolutely ensure that it does not affect the end
result of the query, only the way collections and related objects are loaded,
no matter what the format of the query is.

See also

[Routing Explicit Joins/Statements into Eagerly Loaded Collections](#contains-eager) - using [contains_eager()](#sqlalchemy.orm.contains_eager)

## Select IN loading

In most cases, selectin loading is the most simple and
efficient way to eagerly load collections of objects.  The only scenario in
which selectin eager loading is not feasible is when the model is using
composite primary keys, and the backend database does not support tuples with
IN, which currently includes SQL Server.

“Select IN” eager loading is provided using the `"selectin"` argument to
[relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy) or by using the [selectinload()](#sqlalchemy.orm.selectinload) loader
option.   This style of loading emits a SELECT that refers to the primary key
values of the parent object, or in the case of a many-to-one
relationship to those of the child objects, inside of an IN clause, in
order to load related associations:

```
>>> from sqlalchemy import select
>>> from sqlalchemy.orm import selectinload
>>> stmt = (
...     select(User)
...     .options(selectinload(User.addresses))
...     .filter(or_(User.name == "spongebob", User.name == "ed"))
... )
>>> result = session.scalars(stmt).all()
SELECT
    users.id AS users_id,
    users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users
WHERE users.name = ? OR users.name = ?
('spongebob', 'ed')
SELECT
    addresses.id AS addresses_id,
    addresses.email_address AS addresses_email_address,
    addresses.user_id AS addresses_user_id
FROM addresses
WHERE addresses.user_id IN (?, ?)
(5, 7)
```

Above, the second SELECT refers to `addresses.user_id IN (5, 7)`, where the
“5” and “7” are the primary key values for the previous two `User`
objects loaded; after a batch of objects are completely loaded, their primary
key values are injected into the `IN` clause for the second SELECT.
Because the relationship between `User` and `Address` has a simple
primary join condition and provides that the
primary key values for `User` can be derived from `Address.user_id`, the
statement has no joins or subqueries at all.

For simple many-to-one loads, a JOIN is also not needed as the foreign key
value from the parent object is used:

```
>>> from sqlalchemy import select
>>> from sqlalchemy.orm import selectinload
>>> stmt = select(Address).options(selectinload(Address.user))
>>> result = session.scalars(stmt).all()
SELECT
    addresses.id AS addresses_id,
    addresses.email_address AS addresses_email_address,
    addresses.user_id AS addresses_user_id
    FROM addresses
SELECT
    users.id AS users_id,
    users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users
WHERE users.id IN (?, ?)
(1, 2)
```

Tip

by “simple” we mean that the [relationship.primaryjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin)
condition expresses an equality comparison between the primary key of the
“one” side and a straight foreign key of the “many” side, without any
additional criteria.

Select IN loading also supports many-to-many relationships, where it currently
will JOIN across all three tables to match rows from one side to the other.

Things to know about this kind of loading include:

- The strategy emits a SELECT for up to 500 parent primary key values at a
  time, as the primary keys are rendered into a large IN expression in the SQL
  statement.  Some databases like Oracle Database have a hard limit on how
  large an IN expression can be, and overall the size of the SQL string
  shouldn’t be arbitrarily large.
- As “selectin” loading relies upon IN, for a mapping with composite primary
  keys, it must use the “tuple” form of IN, which looks like `WHERE
  (table.column_a, table.column_b) IN ((?, ?), (?, ?), (?, ?))`. This syntax
  is not currently supported on SQL Server and for SQLite requires at least
  version 3.15.  There is no special logic in SQLAlchemy to check
  ahead of time which platforms support this syntax or not; if run against a
  non-supporting platform, the database will return an error immediately.   An
  advantage to SQLAlchemy just running the SQL out for it to fail is that if a
  particular database does start supporting this syntax, it will work without
  any changes to SQLAlchemy (as was the case with SQLite).

## Subquery Eager Loading

Legacy Feature

The [subqueryload()](#sqlalchemy.orm.subqueryload) eager loader is mostly legacy
at this point, superseded by the [selectinload()](#sqlalchemy.orm.selectinload) strategy
which is of much simpler design, more flexible with features such as
[Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per), and emits more efficient SQL
statements in most cases.   As [subqueryload()](#sqlalchemy.orm.subqueryload) relies upon
re-interpreting the original SELECT statement, it may fail to work
efficiently when given very complex source queries.

[subqueryload()](#sqlalchemy.orm.subqueryload) may continue to be useful for the specific
case of an eager loaded collection for objects that use composite primary
keys, on the Microsoft SQL Server backend that continues to not have
support for the “tuple IN” syntax.

Subquery loading is similar in operation to selectin eager loading, however
the SELECT statement which is emitted is derived from the original statement,
and has a more complex query structure as that of selectin eager loading.

Subquery eager loading is provided using the `"subquery"` argument to
[relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy) or by using the [subqueryload()](#sqlalchemy.orm.subqueryload) loader
option.

The operation of subquery eager loading is to emit a second SELECT statement
for each relationship to be loaded, across all result objects at once.
This SELECT statement refers to the original SELECT statement, wrapped
inside of a subquery, so that we retrieve the same list of primary keys
for the primary object being returned, then link that to the sum of all
the collection members to load them at once:

```
>>> from sqlalchemy import select
>>> from sqlalchemy.orm import subqueryload
>>> stmt = select(User).options(subqueryload(User.addresses)).filter_by(name="spongebob")
>>> results = session.scalars(stmt).all()
SELECT
    users.id AS users_id,
    users.name AS users_name,
    users.fullname AS users_fullname,
    users.nickname AS users_nickname
FROM users
WHERE users.name = ?
('spongebob',)
SELECT
    addresses.id AS addresses_id,
    addresses.email_address AS addresses_email_address,
    addresses.user_id AS addresses_user_id,
    anon_1.users_id AS anon_1_users_id
FROM (
    SELECT users.id AS users_id
    FROM users
    WHERE users.name = ?) AS anon_1
JOIN addresses ON anon_1.users_id = addresses.user_id
ORDER BY anon_1.users_id, addresses.id
('spongebob',)
```

Things to know about this kind of loading include:

- The SELECT statement emitted by the “subquery” loader strategy, unlike
  that of “selectin”, requires a subquery, and will inherit whatever performance
  limitations are present in the original query.  The subquery itself may
  also incur performance penalties based on the specifics of the database in
  use.
- “subquery” loading imposes some special ordering requirements in order to work
  correctly.  A query which makes use of [subqueryload()](#sqlalchemy.orm.subqueryload) in conjunction with a
  limiting modifier such as [Select.limit()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.limit),
  or [Select.offset()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.offset) should **always** include [Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by)
  against unique column(s) such as the primary key, so that the additional queries
  emitted by [subqueryload()](#sqlalchemy.orm.subqueryload) include
  the same ordering as used by the parent query.  Without it, there is a chance
  that the inner query could return the wrong rows:
  ```
  # incorrect, no ORDER BY
  stmt = select(User).options(subqueryload(User.addresses).limit(1))
  # incorrect if User.name is not unique
  stmt = select(User).options(subqueryload(User.addresses)).order_by(User.name).limit(1)
  # correct
  stmt = (
      select(User)
      .options(subqueryload(User.addresses))
      .order_by(User.name, User.id)
      .limit(1)
  )
  ```
  See also
  [Why is ORDER BY recommended with LIMIT (especially with subqueryload())?](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#faq-subqueryload-limit-sort) - detailed example
- “subquery” loading also incurs additional performance / complexity issues
  when used on a many-levels-deep eager load, as subqueries will be nested
  repeatedly.
- “subquery” loading is not compatible with the
  “batched” loading supplied by [Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per), both for collection
  and scalar relationships.

For the above reasons, the “selectin” strategy should be preferred over
“subquery”.

See also

[Select IN loading](#selectin-eager-loading)

## What Kind of Loading to Use ?

Which type of loading to use typically comes down to optimizing the tradeoff
between number of SQL executions, complexity of SQL emitted, and amount of
data fetched.

**One to Many / Many to Many Collection** - The [selectinload()](#sqlalchemy.orm.selectinload) is
generally the best loading strategy to use.  It emits an additional SELECT
that uses as few tables as possible, leaving the original statement unaffected,
and is most flexible for any kind of
originating query.   Its only major limitation is when using a table with
composite primary keys on a backend that does not support “tuple IN”, which
currently includes SQL Server and very old SQLite versions; all other included
backends support it.

**Many to One** - The [joinedload()](#sqlalchemy.orm.joinedload) strategy is the most general
purpose strategy. In special cases, the [immediateload()](#sqlalchemy.orm.immediateload) strategy may
also be useful, if there are a very small number of potential related values,
as this strategy will fetch the object from the local [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
without emitting any SQL if the related object is already present.

## Polymorphic Eager Loading

Specification of polymorphic options on a per-eager-load basis is supported.
See the section [Eager Loading of Polymorphic Subtypes](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#eagerloading-polymorphic-subtypes) for examples
of the [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) method in conjunction with the
[with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) function.

## Wildcard Loading Strategies

Each of [joinedload()](#sqlalchemy.orm.joinedload), [subqueryload()](#sqlalchemy.orm.subqueryload), [lazyload()](#sqlalchemy.orm.lazyload),
[selectinload()](#sqlalchemy.orm.selectinload), and [raiseload()](#sqlalchemy.orm.raiseload) can be used to set the default
style of [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) loading
for a particular query, affecting all [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) -mapped
attributes not otherwise
specified in the statement.   This feature is available by passing
the string `'*'` as the argument to any of these options:

```
from sqlalchemy import select
from sqlalchemy.orm import lazyload

stmt = select(MyClass).options(lazyload("*"))
```

Above, the `lazyload('*')` option will supersede the `lazy` setting
of all [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs in use for that query,
with the exception of those that use `lazy='write_only'`
or `lazy='dynamic'`.

If some relationships specify
`lazy='joined'` or `lazy='selectin'`, for example,
using `lazyload('*')` will unilaterally
cause all those relationships to use `'select'` loading, e.g. emit a
SELECT statement when each attribute is accessed.

The option does not supersede loader options stated in the
query, such as [joinedload()](#sqlalchemy.orm.joinedload),
[selectinload()](#sqlalchemy.orm.selectinload), etc.  The query below will still use joined loading
for the `widget` relationship:

```
from sqlalchemy import select
from sqlalchemy.orm import lazyload
from sqlalchemy.orm import joinedload

stmt = select(MyClass).options(lazyload("*"), joinedload(MyClass.widget))
```

While the instruction for [joinedload()](#sqlalchemy.orm.joinedload) above will take place regardless
of whether it appears before or after the [lazyload()](#sqlalchemy.orm.lazyload) option,
if multiple options that each included `"*"` were passed, the last one
will take effect.

### Per-Entity Wildcard Loading Strategies

A variant of the wildcard loader strategy is the ability to set the strategy
on a per-entity basis.  For example, if querying for `User` and `Address`,
we can instruct all relationships on `Address` to use lazy loading,
while leaving the loader strategies for `User` unaffected,
by first applying the [Load](#sqlalchemy.orm.Load) object, then specifying the `*` as a
chained option:

```
from sqlalchemy import select
from sqlalchemy.orm import Load

stmt = select(User, Address).options(Load(Address).lazyload("*"))
```

Above, all relationships on `Address` will be set to a lazy load.

## Routing Explicit Joins/Statements into Eagerly Loaded Collections

The behavior of [joinedload()](#sqlalchemy.orm.joinedload) is such that joins are
created automatically, using anonymous aliases as targets, the results of which
are routed into collections and
scalar references on loaded objects. It is often the case that a query already
includes the necessary joins which represent a particular collection or scalar
reference, and the joins added by the joinedload feature are redundant - yet
you’d still like the collections/references to be populated.

For this SQLAlchemy supplies the [contains_eager()](#sqlalchemy.orm.contains_eager)
option. This option is used in the same manner as the
[joinedload()](#sqlalchemy.orm.joinedload) option except it is assumed that the
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object will explicitly include the appropriate joins,
typically using methods like [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join).
Below, we specify a join between `User` and `Address`
and additionally establish this as the basis for eager loading of `User.addresses`:

```
from sqlalchemy.orm import contains_eager

stmt = select(User).join(User.addresses).options(contains_eager(User.addresses))
```

If the “eager” portion of the statement is “aliased”, the path
should be specified using [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type), which allows
the specific [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct to be passed:

```
# use an alias of the Address entity
adalias = aliased(Address)

# construct a statement which expects the "addresses" results

stmt = (
    select(User)
    .outerjoin(User.addresses.of_type(adalias))
    .options(contains_eager(User.addresses.of_type(adalias)))
)

# get results normally
r = session.scalars(stmt).unique().all()
SELECT
    users.user_id AS users_user_id,
    users.user_name AS users_user_name,
    adalias.address_id AS adalias_address_id,
    adalias.user_id AS adalias_user_id,
    adalias.email_address AS adalias_email_address,
    (...other columns...)
FROM users
LEFT OUTER JOIN email_addresses AS email_addresses_1
ON users.user_id = email_addresses_1.user_id
```

The path given as the argument to [contains_eager()](#sqlalchemy.orm.contains_eager) needs
to be a full path from the starting entity. For example if we were loading
`Users->orders->Order->items->Item`, the option would be used as:

```
stmt = select(User).options(contains_eager(User.orders).contains_eager(Order.items))
```

### Using contains_eager() to load a custom-filtered collection result

When we use [contains_eager()](#sqlalchemy.orm.contains_eager), *we* are constructing ourselves the
SQL that will be used to populate collections.  From this, it naturally follows
that we can opt to **modify** what values the collection is intended to store,
by writing our SQL to load a subset of elements for collections or
scalar attributes.

Tip

SQLAlchemy now has a **much simpler way to do this**, by allowing
WHERE criteria to be added directly to loader options such as
[joinedload()](#sqlalchemy.orm.joinedload)
and [selectinload()](#sqlalchemy.orm.selectinload) using [PropComparator.and_()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.and_).  See
the section [Adding Criteria to loader options](#loader-option-criteria) for examples.

The techniques described here still apply if the related collection is
to be queried using SQL criteria or modifiers more complex than a simple
WHERE clause.

As an example, we can load a `User` object and eagerly load only particular
addresses into its `.addresses` collection by filtering the joined data,
routing it using [contains_eager()](#sqlalchemy.orm.contains_eager), also using
[Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing) to ensure any already-loaded collections
are overwritten:

```
stmt = (
    select(User)
    .join(User.addresses)
    .filter(Address.email_address.like("%@aol.com"))
    .options(contains_eager(User.addresses))
    .execution_options(populate_existing=True)
)
```

The above query will load only `User` objects which contain at
least `Address` object that contains the substring `'aol.com'` in its
`email` field; the `User.addresses` collection will contain **only**
these `Address` entries, and *not* any other `Address` entries that are
in fact associated with the collection.

Tip

In all cases, the SQLAlchemy ORM does **not overwrite already loaded
attributes and collections** unless told to do so.   As there is an
[identity map](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-map) in use, it is often the case that an ORM query is
returning objects that were in fact already present and loaded in memory.
Therefore, when using [contains_eager()](#sqlalchemy.orm.contains_eager) to populate a collection
in an alternate way, it is usually a good idea to use
[Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing) as illustrated above so that an
already-loaded collection is refreshed with the new data.
The `populate_existing` option will reset **all** attributes that were
already present, including pending changes, so make sure all data is flushed
before using it.   Using the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with its default behavior
of [autoflush](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing) is sufficient.

Note

The customized collection we load using [contains_eager()](#sqlalchemy.orm.contains_eager)
is not “sticky”; that is, the next time this collection is loaded, it will
be loaded with its usual default contents.   The collection is subject
to being reloaded if the object is expired, which occurs whenever the
[Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit), [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) methods are used
assuming default session settings, or the [Session.expire_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire_all)
or [Session.expire()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire) methods are used.

See also

[Adding Criteria to loader options](#loader-option-criteria) - modern API allowing WHERE criteria directly
within any relationship loader option

## Relationship Loader API

| Object Name | Description |
| --- | --- |
| contains_eager(*keys, **kw) | Indicate that the given attribute should be eagerly loaded from
columns stated manually in the query. |
| defaultload(*keys) | Indicate an attribute should load using its predefined loader style. |
| immediateload(*keys, [recursion_depth]) | Indicate that the given attribute should be loaded using
an immediate load with a per-attribute SELECT statement. |
| joinedload(*keys, **kw) | Indicate that the given attribute should be loaded using joined
eager loading. |
| lazyload(*keys) | Indicate that the given attribute should be loaded using “lazy”
loading. |
| Load | Represents loader options which modify the state of a
ORM-enabledSelector a legacyQueryin
order to affect how various mapped attributes are loaded. |
| noload(*keys) | Indicate that the given relationship attribute should remain
unloaded. |
| raiseload(*keys, **kw) | Indicate that the given attribute should raise an error if accessed. |
| selectinload(*keys, [recursion_depth]) | Indicate that the given attribute should be loaded using
SELECT IN eager loading. |
| subqueryload(*keys) | Indicate that the given attribute should be loaded using
subquery eager loading. |

   function sqlalchemy.orm.contains_eager(**keys:Literal['*']|QueryableAttribute[Any]*, ***kw:Any*) → _AbstractLoad

Indicate that the given attribute should be eagerly loaded from
columns stated manually in the query.

This function is part of the [Load](#sqlalchemy.orm.Load) interface and supports
both method-chained and standalone operation.

The option is used in conjunction with an explicit join that loads
the desired rows, i.e.:

```
sess.query(Order).join(Order.user).options(contains_eager(Order.user))
```

The above query would join from the `Order` entity to its related
`User` entity, and the returned `Order` objects would have the
`Order.user` attribute pre-populated.

It may also be used for customizing the entries in an eagerly loaded
collection; queries will normally want to use the
[Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing) execution option assuming the
primary collection of parent objects may already have been loaded:

```
sess.query(User).join(User.addresses).filter(
    Address.email_address.like("%@aol.com")
).options(contains_eager(User.addresses)).populate_existing()
```

See the section [Routing Explicit Joins/Statements into Eagerly Loaded Collections](#contains-eager) for complete usage details.

See also

[Relationship Loading Techniques](#)

[Routing Explicit Joins/Statements into Eagerly Loaded Collections](#contains-eager)

     function sqlalchemy.orm.defaultload(**keys:Literal['*']|QueryableAttribute[Any]*) → _AbstractLoad

Indicate an attribute should load using its predefined loader style.

The behavior of this loading option is to not change the current
loading style of the attribute, meaning that the previously configured
one is used or, if no previous style was selected, the default
loading will be used.

This method is used to link to other loader options further into
a chain of attributes without altering the loader style of the links
along the chain.  For example, to set joined eager loading for an
element of an element:

```
session.query(MyClass).options(
    defaultload(MyClass.someattribute).joinedload(
        MyOtherClass.someotherattribute
    )
)
```

[defaultload()](#sqlalchemy.orm.defaultload) is also useful for setting column-level options on
a related class, namely that of [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) and [undefer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer):

```
session.scalars(
    select(MyClass).options(
        defaultload(MyClass.someattribute)
        .defer("some_column")
        .undefer("some_other_column")
    )
)
```

See also

[Specifying Sub-Options with Load.options()](#orm-queryguide-relationship-sub-options)

[Load.options()](#sqlalchemy.orm.Load.options)

     function sqlalchemy.orm.immediateload(**keys:Literal['*']|QueryableAttribute[Any]*, *recursion_depth:int|None=None*) → _AbstractLoad

Indicate that the given attribute should be loaded using
an immediate load with a per-attribute SELECT statement.

The load is achieved using the “lazyloader” strategy and does not
fire off any additional eager loaders.

The [immediateload()](#sqlalchemy.orm.immediateload) option is superseded in general
by the [selectinload()](#sqlalchemy.orm.selectinload) option, which performs the same task
more efficiently by emitting a SELECT for all loaded objects.

This function is part of the [Load](#sqlalchemy.orm.Load) interface and supports
both method-chained and standalone operation.

  Parameters:

**recursion_depth** –

optional int; when set to a positive integer
in conjunction with a self-referential relationship,
indicates “selectin” loading will continue that many levels deep
automatically until no items are found.

Note

The [immediateload.recursion_depth](#sqlalchemy.orm.immediateload.params.recursion_depth) option
currently supports only self-referential relationships.  There
is not yet an option to automatically traverse recursive structures
with more than one relationship involved.

Warning

This parameter is new and experimental and should be
treated as “alpha” status

Added in version 2.0: added
[immediateload.recursion_depth](#sqlalchemy.orm.immediateload.params.recursion_depth)

See also

[Relationship Loading Techniques](#)

[Select IN loading](#selectin-eager-loading)

     function sqlalchemy.orm.joinedload(**keys:Literal['*']|QueryableAttribute[Any]*, ***kw:Any*) → _AbstractLoad

Indicate that the given attribute should be loaded using joined
eager loading.

This function is part of the [Load](#sqlalchemy.orm.Load) interface and supports
both method-chained and standalone operation.

examples:

```
# joined-load the "orders" collection on "User"
select(User).options(joinedload(User.orders))

# joined-load Order.items and then Item.keywords
select(Order).options(joinedload(Order.items).joinedload(Item.keywords))

# lazily load Order.items, but when Items are loaded,
# joined-load the keywords collection
select(Order).options(lazyload(Order.items).joinedload(Item.keywords))
```

   Parameters:

**innerjoin** –

if `True`, indicates that the joined eager load
should use an inner join instead of the default of left outer join:

```
select(Order).options(joinedload(Order.user, innerjoin=True))
```

In order to chain multiple eager joins together where some may be
OUTER and others INNER, right-nested joins are used to link them:

```
select(A).options(
    joinedload(A.bs, innerjoin=False).joinedload(B.cs, innerjoin=True)
)
```

The above query, linking A.bs via “outer” join and B.cs via “inner”
join would render the joins as “a LEFT OUTER JOIN (b JOIN c)”. When
using older versions of SQLite (< 3.7.16), this form of JOIN is
translated to use full subqueries as this syntax is otherwise not
directly supported.

The `innerjoin` flag can also be stated with the term `"unnested"`.
This indicates that an INNER JOIN should be used, *unless* the join
is linked to a LEFT OUTER JOIN to the left, in which case it
will render as LEFT OUTER JOIN.  For example, supposing `A.bs`
is an outerjoin:

```
select(A).options(joinedload(A.bs).joinedload(B.cs, innerjoin="unnested"))
```

The above join will render as “a LEFT OUTER JOIN b LEFT OUTER JOIN c”,
rather than as “a LEFT OUTER JOIN (b JOIN c)”.

Note

The “unnested” flag does **not** affect the JOIN rendered
from a many-to-many association table, e.g. a table configured as
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary), to the target table; for
correctness of results, these joins are always INNER and are
therefore right-nested if linked to an OUTER join.

Note

The joins produced by [joinedload()](#sqlalchemy.orm.joinedload) are **anonymously
aliased**. The criteria by which the join proceeds cannot be
modified, nor can the ORM-enabled [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) or legacy
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) refer to these joins in any way, including
ordering. See [The Zen of Joined Eager Loading](#zen-of-eager-loading) for further detail.

To produce a specific SQL JOIN which is explicitly available, use
[Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) and [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join). To combine
explicit JOINs with eager loading of collections, use
[contains_eager()](#sqlalchemy.orm.contains_eager); see [Routing Explicit Joins/Statements into Eagerly Loaded Collections](#contains-eager).

See also

[Relationship Loading Techniques](#)

[Joined Eager Loading](#joined-eager-loading)

     function sqlalchemy.orm.lazyload(**keys:Literal['*']|QueryableAttribute[Any]*) → _AbstractLoad

Indicate that the given attribute should be loaded using “lazy”
loading.

This function is part of the [Load](#sqlalchemy.orm.Load) interface and supports
both method-chained and standalone operation.

See also

[Relationship Loading Techniques](#)

[Lazy Loading](#lazy-loading)

     class sqlalchemy.orm.Load

*inherits from* `sqlalchemy.orm.strategy_options._AbstractLoad`

Represents loader options which modify the state of a
ORM-enabled [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) or a legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) in
order to affect how various mapped attributes are loaded.

The [Load](#sqlalchemy.orm.Load) object is in most cases used implicitly behind the
scenes when one makes use of a query option like [joinedload()](#sqlalchemy.orm.joinedload),
[defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer), or similar.   It typically is not instantiated directly
except for in some very specific cases.

See also

[Per-Entity Wildcard Loading Strategies](#orm-queryguide-relationship-per-entity-wildcard) - illustrates an
example where direct use of [Load](#sqlalchemy.orm.Load) may be useful

| Member Name | Description |
| --- | --- |
| contains_eager() | Produce a newLoadobject with thecontains_eager()option applied. |
| defaultload() | Produce a newLoadobject with thedefaultload()option applied. |
| defer() | Produce a newLoadobject with thedefer()option applied. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| immediateload() | Produce a newLoadobject with theimmediateload()option applied. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| joinedload() | Produce a newLoadobject with thejoinedload()option applied. |
| lazyload() | Produce a newLoadobject with thelazyload()option applied. |
| load_only() | Produce a newLoadobject with theload_only()option applied. |
| noload() | Produce a newLoadobject with thenoload()option applied. |
| options() | Apply a series of options as sub-options to thisLoadobject. |
| process_compile_state() | Apply a modification to a givenORMCompileState. |
| process_compile_state_replaced_entities() | Apply a modification to a givenORMCompileState,
given entities that were replaced by with_only_columns() or
with_entities(). |
| propagate_to_loaders | if True, indicate this option should be carried along
to “secondary” SELECT statements that occur for relationship
lazy loaders as well as attribute load / refresh operations. |
| raiseload() | Produce a newLoadobject with theraiseload()option applied. |
| selectin_polymorphic() | Produce a newLoadobject with theselectin_polymorphic()option applied. |
| selectinload() | Produce a newLoadobject with theselectinload()option applied. |
| subqueryload() | Produce a newLoadobject with thesubqueryload()option applied. |
| undefer() | Produce a newLoadobject with theundefer()option applied. |
| undefer_group() | Produce a newLoadobject with theundefer_group()option applied. |
| with_expression() | Produce a newLoadobject with thewith_expression()option applied. |

   method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)contains_eager(*attr:_AttrType*, *alias:_FromClauseArgument|None=None*, *_is_chain:bool=False*, *_propagate_to_loaders:bool=False*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.contains_eager` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[contains_eager()](#sqlalchemy.orm.contains_eager) option applied.

See [contains_eager()](#sqlalchemy.orm.contains_eager) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)defaultload(*attr:Literal['*']|QueryableAttribute[Any]*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.defaultload` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[defaultload()](#sqlalchemy.orm.defaultload) option applied.

See [defaultload()](#sqlalchemy.orm.defaultload) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)defer(*key:Literal['*']|QueryableAttribute[Any]*, *raiseload:bool=False*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.defer` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) option applied.

See [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)immediateload(*attr:Literal['*']|QueryableAttribute[Any]*, *recursion_depth:int|None=None*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.immediateload` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[immediateload()](#sqlalchemy.orm.immediateload) option applied.

See [immediateload()](#sqlalchemy.orm.immediateload) for usage examples.

    attribute [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)inherit_cache = None

*inherited from the* `HasCacheKey.inherit_cache` *attribute of* [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey)

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

     method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)joinedload(*attr:Literal['*']|QueryableAttribute[Any]*, *innerjoin:bool|None=None*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.joinedload` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[joinedload()](#sqlalchemy.orm.joinedload) option applied.

See [joinedload()](#sqlalchemy.orm.joinedload) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)lazyload(*attr:Literal['*']|QueryableAttribute[Any]*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.lazyload` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[lazyload()](#sqlalchemy.orm.lazyload) option applied.

See [lazyload()](#sqlalchemy.orm.lazyload) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)load_only(**attrs:Literal['*']|QueryableAttribute[Any]*, *raiseload:bool=False*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.load_only` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) option applied.

See [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)noload(*attr:Literal['*']|QueryableAttribute[Any]*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.noload` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[noload()](#sqlalchemy.orm.noload) option applied.

See [noload()](#sqlalchemy.orm.noload) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)options(**opts:_AbstractLoad*) → Self

Apply a series of options as sub-options to this
[Load](#sqlalchemy.orm.Load)
object.

E.g.:

```
query = session.query(Author)
query = query.options(
    joinedload(Author.book).options(
        load_only(Book.summary, Book.excerpt),
        joinedload(Book.citations).options(joinedload(Citation.author)),
    )
)
```

   Parameters:

***opts** – A series of loader option objects (ultimately
[Load](#sqlalchemy.orm.Load) objects) which should be applied to the path
specified by this [Load](#sqlalchemy.orm.Load) object.

Added in version 1.3.6.

See also

[defaultload()](#sqlalchemy.orm.defaultload)

[Specifying Sub-Options with Load.options()](#orm-queryguide-relationship-sub-options)

     method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)process_compile_state(*compile_state:ORMCompileState*) → None

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.process_compile_state` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Apply a modification to a given `ORMCompileState`.

This method is part of the implementation of a particular
`CompileStateOption` and is only invoked internally
when an ORM query is compiled.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)process_compile_state_replaced_entities(*compile_state:ORMCompileState*, *mapper_entities:Sequence[_MapperEntity]*) → None

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.process_compile_state_replaced_entities` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Apply a modification to a given `ORMCompileState`,
given entities that were replaced by with_only_columns() or
with_entities().

This method is part of the implementation of a particular
`CompileStateOption` and is only invoked internally
when an ORM query is compiled.

Added in version 1.4.19.

     attribute [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)propagate_to_loaders

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.propagate_to_loaders` *attribute of* `sqlalchemy.orm.strategy_options._AbstractLoad`

if True, indicate this option should be carried along
to “secondary” SELECT statements that occur for relationship
lazy loaders as well as attribute load / refresh operations.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)raiseload(*attr:Literal['*']|QueryableAttribute[Any]*, *sql_only:bool=False*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.raiseload` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[raiseload()](#sqlalchemy.orm.raiseload) option applied.

See [raiseload()](#sqlalchemy.orm.raiseload) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)selectin_polymorphic(*classes:Iterable[Type[Any]]*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.selectin_polymorphic` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[selectin_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.selectin_polymorphic) option applied.

See [selectin_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.selectin_polymorphic) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)selectinload(*attr:Literal['*']|QueryableAttribute[Any]*, *recursion_depth:int|None=None*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.selectinload` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[selectinload()](#sqlalchemy.orm.selectinload) option applied.

See [selectinload()](#sqlalchemy.orm.selectinload) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)subqueryload(*attr:Literal['*']|QueryableAttribute[Any]*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.subqueryload` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[subqueryload()](#sqlalchemy.orm.subqueryload) option applied.

See [subqueryload()](#sqlalchemy.orm.subqueryload) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)undefer(*key:Literal['*']|QueryableAttribute[Any]*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.undefer` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[undefer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer) option applied.

See [undefer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)undefer_group(*name:str*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.undefer_group` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[undefer_group()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer_group) option applied.

See [undefer_group()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer_group) for usage examples.

    method [sqlalchemy.orm.Load.](#sqlalchemy.orm.Load)with_expression(*key:_AttrType*, *expression:_ColumnExpressionArgument[Any]*) → Self

*inherited from the* `sqlalchemy.orm.strategy_options._AbstractLoad.with_expression` *method of* `sqlalchemy.orm.strategy_options._AbstractLoad`

Produce a new [Load](#sqlalchemy.orm.Load) object with the
[with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) option applied.

See [with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) for usage examples.

     function sqlalchemy.orm.noload(**keys:Literal['*']|QueryableAttribute[Any]*) → _AbstractLoad

Indicate that the given relationship attribute should remain
unloaded.

The relationship attribute will return `None` when accessed without
producing any loading effect.

This function is part of the [Load](#sqlalchemy.orm.Load) interface and supports
both method-chained and standalone operation.

[noload()](#sqlalchemy.orm.noload) applies to [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) attributes
only.

Legacy Feature

The [noload()](#sqlalchemy.orm.noload) option is **legacy**.  As it
forces collections to be empty, which invariably leads to
non-intuitive and difficult to predict results.  There are no
legitimate uses for this option in modern SQLAlchemy.

See also

[Relationship Loading Techniques](#)

     function sqlalchemy.orm.raiseload(**keys:Literal['*']|QueryableAttribute[Any]*, ***kw:Any*) → _AbstractLoad

Indicate that the given attribute should raise an error if accessed.

A relationship attribute configured with [raiseload()](#sqlalchemy.orm.raiseload) will
raise an [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) upon access. The
typical way this is useful is when an application is attempting to
ensure that all relationship attributes that are accessed in a
particular context would have been already loaded via eager loading.
Instead of having to read through SQL logs to ensure lazy loads aren’t
occurring, this strategy will cause them to raise immediately.

[raiseload()](#sqlalchemy.orm.raiseload) applies to [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) attributes
only. In order to apply raise-on-SQL behavior to a column-based
attribute, use the [defer.raiseload](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer.params.raiseload) parameter on the
[defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) loader option.

  Parameters:

**sql_only** – if True, raise only if the lazy load would emit SQL,
but not if it is only checking the identity map, or determining that
the related value should just be None due to missing keys. When False,
the strategy will raise for all varieties of relationship loading.

This function is part of the [Load](#sqlalchemy.orm.Load) interface and supports
both method-chained and standalone operation.

See also

[Relationship Loading Techniques](#)

[Preventing unwanted lazy loads using raiseload](#prevent-lazy-with-raiseload)

[Using raiseload to prevent deferred column loads](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#orm-queryguide-deferred-raiseload)

     function sqlalchemy.orm.selectinload(**keys:Literal['*']|QueryableAttribute[Any]*, *recursion_depth:int|None=None*) → _AbstractLoad

Indicate that the given attribute should be loaded using
SELECT IN eager loading.

This function is part of the [Load](#sqlalchemy.orm.Load) interface and supports
both method-chained and standalone operation.

examples:

```
# selectin-load the "orders" collection on "User"
select(User).options(selectinload(User.orders))

# selectin-load Order.items and then Item.keywords
select(Order).options(
    selectinload(Order.items).selectinload(Item.keywords)
)

# lazily load Order.items, but when Items are loaded,
# selectin-load the keywords collection
select(Order).options(lazyload(Order.items).selectinload(Item.keywords))
```

   Parameters:

**recursion_depth** –

optional int; when set to a positive integer
in conjunction with a self-referential relationship,
indicates “selectin” loading will continue that many levels deep
automatically until no items are found.

Note

The [selectinload.recursion_depth](#sqlalchemy.orm.selectinload.params.recursion_depth) option
currently supports only self-referential relationships.  There
is not yet an option to automatically traverse recursive structures
with more than one relationship involved.

Additionally, the [selectinload.recursion_depth](#sqlalchemy.orm.selectinload.params.recursion_depth)
parameter is new and experimental and should be treated as “alpha”
status for the 2.0 series.

Added in version 2.0: added
[selectinload.recursion_depth](#sqlalchemy.orm.selectinload.params.recursion_depth)

See also

[Relationship Loading Techniques](#)

[Select IN loading](#selectin-eager-loading)

     function sqlalchemy.orm.subqueryload(**keys:Literal['*']|QueryableAttribute[Any]*) → _AbstractLoad

Indicate that the given attribute should be loaded using
subquery eager loading.

This function is part of the [Load](#sqlalchemy.orm.Load) interface and supports
both method-chained and standalone operation.

examples:

```
# subquery-load the "orders" collection on "User"
select(User).options(subqueryload(User.orders))

# subquery-load Order.items and then Item.keywords
select(Order).options(
    subqueryload(Order.items).subqueryload(Item.keywords)
)

# lazily load Order.items, but when Items are loaded,
# subquery-load the keywords collection
select(Order).options(lazyload(Order.items).subqueryload(Item.keywords))
```

See also

[Relationship Loading Techniques](#)

[Subquery Eager Loading](#subquery-eager-loading)

ORM Querying Guide

Next Query Guide Section: [ORM API Features for Querying](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html)
