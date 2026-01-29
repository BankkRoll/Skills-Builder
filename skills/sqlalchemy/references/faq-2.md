# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# ORM Configuration

## How do I map a table that has no primary key?

The SQLAlchemy ORM, in order to map to a particular table, needs there to be
at least one column denoted as a primary key column; multiple-column,
i.e. composite, primary keys are of course entirely feasible as well.  These
columns do **not** need to be actually known to the database as primary key
columns, though it’s a good idea that they are.  It’s only necessary that the columns
*behave* as a primary key does, e.g. as a unique and not nullable identifier
for a row.

Most ORMs require that objects have some kind of primary key defined
because the object in memory must correspond to a uniquely identifiable
row in the database table; at the very least, this allows the
object can be targeted for UPDATE and DELETE statements which will affect only
that object’s row and no other.   However, the importance of the primary key
goes far beyond that.  In SQLAlchemy, all ORM-mapped objects are at all times
linked uniquely within a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
to their specific database row using a pattern called the [identity map](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-map),
a pattern that’s central to the unit of work system employed by SQLAlchemy,
and is also key to the most common (and not-so-common) patterns of ORM usage.

Note

It’s important to note that we’re only talking about the SQLAlchemy ORM; an
application which builds on Core and deals only with [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects,
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) constructs and the like, **does not** need any primary key
to be present on or associated with a table in any way (though again, in SQL, all tables
should really have some kind of primary key, lest you need to actually
update or delete specific rows).

In almost all cases, a table does have a so-called [candidate key](https://docs.sqlalchemy.org/en/20/glossary.html#term-candidate-key), which is a column or series
of columns that uniquely identify a row.  If a table truly doesn’t have this, and has actual
fully duplicate rows, the table is not corresponding to [first normal form](https://en.wikipedia.org/wiki/First_normal_form) and cannot be mapped.   Otherwise, whatever columns comprise the best candidate key can be
applied directly to the mapper:

```
class SomeClass(Base):
    __table__ = some_table_with_no_pk
    __mapper_args__ = {
        "primary_key": [some_table_with_no_pk.c.uid, some_table_with_no_pk.c.bar]
    }
```

Better yet is when using fully declared table metadata, use the `primary_key=True`
flag on those columns:

```
class SomeClass(Base):
    __tablename__ = "some_table_with_no_pk"

    uid = Column(Integer, primary_key=True)
    bar = Column(String, primary_key=True)
```

All tables in a relational database should have primary keys.   Even a many-to-many
association table - the primary key would be the composite of the two association
columns:

```
CREATE TABLE my_association (
  user_id INTEGER REFERENCES user(id),
  account_id INTEGER REFERENCES account(id),
  PRIMARY KEY (user_id, account_id)
)
```

## How do I configure a Column that is a Python reserved word or similar?

Column-based attributes can be given any name desired in the mapping. See
[Naming Declarative Mapped Columns Explicitly](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapper-column-distinct-names).

## How do I get a list of all columns, relationships, mapped attributes, etc. given a mapped class?

This information is all available from the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object.

To get at the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) for a particular mapped class, call the
[inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function on it:

```
from sqlalchemy import inspect

mapper = inspect(MyClass)
```

From there, all information about the class can be accessed through properties
such as:

- [Mapper.attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.attrs) - a namespace of all mapped attributes.  The attributes
  themselves are instances of [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty), which contain additional
  attributes that can lead to the mapped SQL expression or column, if applicable.
- [Mapper.column_attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.column_attrs) - the mapped attribute namespace
  limited to column and SQL expression attributes.   You might want to use
  [Mapper.columns](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.columns) to get at the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects directly.
- [Mapper.relationships](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.relationships) - namespace of all [RelationshipProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.RelationshipProperty) attributes.
- [Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors) - namespace of all mapped attributes, plus user-defined
  attributes defined using systems such as [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property), [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) and others.
- [Mapper.columns](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.columns) - A namespace of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects and other named
  SQL expressions associated with the mapping.
- [Mapper.mapped_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.mapped_table) - The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or other selectable to which
  this mapper is mapped.
- [Mapper.local_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.local_table) - The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that is “local” to this mapper;
  this differs from [Mapper.mapped_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.mapped_table) in the case of a mapper mapped
  using inheritance to a composed selectable.

## I’m getting a warning or error about “Implicitly combining column X under attribute Y”

This condition refers to when a mapping contains two columns that are being
mapped under the same attribute name due to their name, but there’s no indication
that this is intentional.  A mapped class needs to have explicit names for
every attribute that is to store an independent value; when two columns have the
same name and aren’t disambiguated, they fall under the same attribute and
the effect is that the value from one column is **copied** into the other, based
on which column was assigned to the attribute first.

This behavior is often desirable and is allowed without warning in the case
where the two columns are linked together via a foreign key relationship
within an inheritance mapping.   When the warning or exception occurs, the
issue can be resolved by either assigning the columns to differently-named
attributes, or if combining them together is desired, by using
[column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) to make this explicit.

Given the example as follows:

```
from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)

class B(A):
    __tablename__ = "b"

    id = Column(Integer, primary_key=True)
    a_id = Column(Integer, ForeignKey("a.id"))
```

As of SQLAlchemy version 0.9.5, the above condition is detected, and will
warn that the `id` column of `A` and `B` is being combined under
the same-named attribute `id`, which above is a serious issue since it means
that a `B` object’s primary key will always mirror that of its `A`.

A mapping which resolves this is as follows:

```
class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)

class B(A):
    __tablename__ = "b"

    b_id = Column("id", Integer, primary_key=True)
    a_id = Column(Integer, ForeignKey("a.id"))
```

Suppose we did want `A.id` and `B.id` to be mirrors of each other, despite
the fact that `B.a_id` is where `A.id` is related.  We could combine
them together using [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property):

```
class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)

class B(A):
    __tablename__ = "b"

    # probably not what you want, but this is a demonstration
    id = column_property(Column(Integer, primary_key=True), A.id)
    a_id = Column(Integer, ForeignKey("a.id"))
```

## I’m using Declarative and setting primaryjoin/secondaryjoin using anand_()oror_(), and I am getting an error message about foreign keys.

Are you doing this?:

```
class MyClass(Base):
    # ....

    foo = relationship(
        "Dest", primaryjoin=and_("MyClass.id==Dest.foo_id", "MyClass.foo==Dest.bar")
    )
```

That’s an `and_()` of two string expressions, which SQLAlchemy cannot apply any mapping towards.  Declarative allows [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) arguments to be specified as strings, which are converted into expression objects using `eval()`.   But this doesn’t occur inside of an `and_()` expression - it’s a special operation declarative applies only to the *entirety* of what’s passed to primaryjoin or other arguments as a string:

```
class MyClass(Base):
    # ....

    foo = relationship(
        "Dest", primaryjoin="and_(MyClass.id==Dest.foo_id, MyClass.foo==Dest.bar)"
    )
```

Or if the objects you need are already available, skip the strings:

```
class MyClass(Base):
    # ....

    foo = relationship(
        Dest, primaryjoin=and_(MyClass.id == Dest.foo_id, MyClass.foo == Dest.bar)
    )
```

The same idea applies to all the other arguments, such as `foreign_keys`:

```
# wrong !
foo = relationship(Dest, foreign_keys=["Dest.foo_id", "Dest.bar_id"])

# correct !
foo = relationship(Dest, foreign_keys="[Dest.foo_id, Dest.bar_id]")

# also correct !
foo = relationship(Dest, foreign_keys=[Dest.foo_id, Dest.bar_id])

# if you're using columns from the class that you're inside of, just use the column objects !
class MyClass(Base):
    foo_id = Column(...)
    bar_id = Column(...)
    # ...

    foo = relationship(Dest, foreign_keys=[foo_id, bar_id])
```

## Why isORDERBYrecommended withLIMIT(especially withsubqueryload())?

When ORDER BY is not used for a SELECT statement that returns rows, the
relational database is free to returned matched rows in any arbitrary
order.  While this ordering very often corresponds to the natural
order of rows within a table, this is not the case for all databases and all
queries. The consequence of this is that any query that limits rows using
`LIMIT` or `OFFSET`, or which merely selects the first row of the result,
discarding the rest, will not be deterministic in terms of what result row is
returned, assuming there’s more than one row that matches the query’s criteria.

While we may not notice this for simple queries on databases that usually
returns rows in their natural order, it becomes more of an issue if we
also use [subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload) to load related collections, and we may not
be loading the collections as intended.

SQLAlchemy implements [subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload) by issuing a separate query,
the results of which are matched up to the results from the first query.
We see two queries emitted like this:

```
>>> session.scalars(select(User).options(subqueryload(User.addresses))).all()
-- the "main" query
SELECT users.id AS users_id
FROM users
-- the "load" query issued by subqueryload
SELECT addresses.id AS addresses_id,
       addresses.user_id AS addresses_user_id,
       anon_1.users_id AS anon_1_users_id
FROM (SELECT users.id AS users_id FROM users) AS anon_1
JOIN addresses ON anon_1.users_id = addresses.user_id
ORDER BY anon_1.users_id
```

The second query embeds the first query as a source of rows.
When the inner query uses `OFFSET` and/or `LIMIT` without ordering,
the two queries may not see the same results:

```
>>> user = session.scalars(
...     select(User).options(subqueryload(User.addresses)).limit(1)
... ).first()
-- the "main" query
SELECT users.id AS users_id
FROM users
 LIMIT 1
-- the "load" query issued by subqueryload
SELECT addresses.id AS addresses_id,
       addresses.user_id AS addresses_user_id,
       anon_1.users_id AS anon_1_users_id
FROM (SELECT users.id AS users_id FROM users LIMIT 1) AS anon_1
JOIN addresses ON anon_1.users_id = addresses.user_id
ORDER BY anon_1.users_id
```

Depending on database specifics, there is
a chance we may get a result like the following for the two queries:

```
-- query #1
+--------+
|users_id|
+--------+
|       1|
+--------+

-- query #2
+------------+-----------------+---------------+
|addresses_id|addresses_user_id|anon_1_users_id|
+------------+-----------------+---------------+
|           3|                2|              2|
+------------+-----------------+---------------+
|           4|                2|              2|
+------------+-----------------+---------------+
```

Above, we receive two `addresses` rows for `user.id` of 2, and none for
1.  We’ve wasted two rows and failed to actually load the collection.  This
is an insidious error because without looking at the SQL and the results, the
ORM will not show that there’s any issue; if we access the `addresses`
for the `User` we have, it will emit a lazy load for the collection and we
won’t see that anything actually went wrong.

The solution to this problem is to always specify a deterministic sort order,
so that the main query always returns the same set of rows. This generally
means that you should [Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by) on a unique column on the table.
The primary key is a good choice for this:

```
session.scalars(
    select(User).options(subqueryload(User.addresses)).order_by(User.id).limit(1)
).first()
```

Note that the [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload) eager loader strategy does not suffer from
the same problem because only one query is ever issued, so the load query
cannot be different from the main query.  Similarly, the [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload)
eager loader strategy also does not have this issue as it links its collection
loads directly to primary key values just loaded.

See also

[Subquery Eager Loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#subquery-eager-loading)

## What aredefault,default_factoryandinsert_defaultand what should I use?

There’s a bit of a clash in SQLAlchemy’s API here due to the addition of PEP-681
dataclass transforms, which is strict about its naming conventions. PEP-681 comes
into play if you are using [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) as shown in [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses).
If you are not using MappedAsDataclass, then it does not apply.

### Part One - Classic SQLAlchemy that is not using dataclasses

When **not** using [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass), as has been the case for many years
in SQLAlchemy, the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) (and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column))
construct supports a parameter [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default).
This indicates a Python-side default (as opposed to a server side default that
would be part of your database’s schema definition) that will take place when
an `INSERT` statement is emitted. This default can be **any** of a static Python value
like a string, **or** a Python callable function, **or** a SQLAlchemy SQL construct.
Full documentation for [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) is at
[Client-Invoked SQL Expressions](https://docs.sqlalchemy.org/en/20/core/defaults.html#defaults-client-invoked-sql).

When using [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) with an ORM mapping that is **not**
using [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass), this default value /callable **does not show
up on your object when you first construct it**. It only takes place when SQLAlchemy
works up an `INSERT` statement for your object.

A very important thing to note is that when using [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column)
(and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)), the classic [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default)
parameter is also available under a new name, called
[mapped_column.insert_default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.insert_default). If you build a
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) and you are **not** using [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass), the
[mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) and [mapped_column.insert_default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.insert_default)
parameters are **synonymous**.

### Part Two - Using Dataclasses support with MappedAsDataclass

When you **are** using [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass), that is, the specific form
of mapping used at [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), the meaning of the
[mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) keyword changes. We recognize that it’s not
ideal that this name changes its behavior, however there was no alternative as
PEP-681 requires [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) to take on this meaning.

When dataclasses are used, the [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) parameter must
be used the way it’s described at
[Python Dataclasses](https://docs.python.org/3/library/dataclasses.html) - it refers
to a constant value like a string or a number, and **is applied to your object
immediately when constructed**. It is also at the moment also applied to the
[mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) parameter of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) where
it would be used in an `INSERT` statement automatically even if not present
on the object. If you instead want to use a callable for your dataclass,
which will be applied to the object when constructed, you would use
[mapped_column.default_factory](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default_factory).

The value used for [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) is also applied to the
[Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) parameter of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).
This is so that the value used as the dataclass default is also applied in
an ORM INSERT statement for a mapped object where the value was not
explicitly passed.  Using this parameter is **mutually exclusive** against the
[Column.insert_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.insert_default) parameter, meaning that both cannot
be used at the same time.

For the specific case of using a callable to generate defaults, the situation
changes a bit; the [mapped_column.default_factory](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default_factory) parameter is
a **dataclass only** parameter that may be used to generate new default values
for instances of the class, but **only takes place when the object is
constructed**.   That is, it is **not** equivalent to
[mapped_column.insert_default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.insert_default) with a callable as it **will not
take effect** for a plain `insert()` statement that does not actually
construct the object; it only is useful for objects that are inserted using
[unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) patterns, i.e. using [Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) with
[Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush) / [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit). For defaults that
should apply to INSERT statements regardless of how they are invoked, use
[mapped_column.insert_default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.insert_default) instead.

| Construct | Works with dataclasses? | Works without dataclasses? | Accepts scalar? | Accepts callable? | Available on object immediately? | Used in INSERT statements? |
| --- | --- | --- | --- | --- | --- | --- |
| mapped_column.default | ✔ | ✔ | ✔ | Only if no dataclasses | Only if dataclasses | ✔ |
| mapped_column.insert_default | ✔ | ✔ | ✔ | ✔ | ✖ | ✔ |
| mapped_column.default_factory | ✔ | ✖ | ✖ | ✔ | Only if dataclasses | ✖ (unit of work only) |

---

# SQLAlchemy 2.0 Documentation

# Performance

## Why is my application slow after upgrading to 1.4 and/or 2.x?

SQLAlchemy as of version 1.4 includes a
[SQL compilation caching facility](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching) which will allow
Core and ORM SQL constructs to cache their stringified form, along with other
structural information used to fetch results from the statement, allowing the
relatively expensive string compilation process to be skipped when another
structurally equivalent construct is next used. This system
relies upon functionality that is implemented for all SQL constructs, including
objects such as  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column),
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select), and [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) objects, to produce a
**cache key** which fully represents their state to the degree that it affects
the SQL compilation process.

The caching system allows SQLAlchemy 1.4 and above to be more performant than
SQLAlchemy 1.3 with regards to the time spent converting SQL constructs into
strings repeatedly.  However, this only works if caching is enabled for the
dialect and SQL constructs in use; if not, string compilation is usually
similar to that of SQLAlchemy 1.3, with a slight decrease in speed in some
cases.

There is one case however where if SQLAlchemy’s new caching system has been
disabled (for reasons below), performance for the ORM may be in fact
significantly poorer than that of 1.3 or other prior releases which is due to
the lack of caching within ORM lazy loaders and object refresh queries, which
in the 1.3 and earlier releases used the now-legacy `BakedQuery` system. If
an application is seeing significant (30% or higher) degradations in
performance (measured in time for operations to complete) when switching to
1.4, this is the likely cause of the issue, with steps to mitigate below.

See also

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching) - overview of the caching system

[Object will not produce a cache key, Performance Implications](https://docs.sqlalchemy.org/en/20/errors.html#caching-caveats) - additional information regarding the warnings
generated for elements that don’t enable caching.

### Step one - turn on SQL logging and confirm whether or not caching is working

Here, we want to use the technique described at
[engine logging](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching-logging), looking for statements with the
`[no key]` indicator or even `[dialect does not support caching]`.
The indicators we would see for SQL statements that are successfully participating
in the caching system would be indicating `[generated in Xs]` when
statements are invoked for the first time and then
`[cached since Xs ago]` for the vast majority of statements subsequent.
If `[no key]` is prevalent in particular for SELECT statements, or
if caching is disabled entirely due to `[dialect does not support caching]`,
this can be the cause of significant performance degradation.

See also

[Estimating Cache Performance Using Logging](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching-logging)

### Step two - identify what constructs are blocking caching from being enabled

Assuming statements are not being cached, there should be warnings emitted
early in the application’s log (SQLAlchemy 1.4.28 and above only) indicating
dialects, [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) objects, and SQL constructs that are not
participating in caching.

For user defined datatypes such as those which extend [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
and [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType), the warnings will look like:

```
sqlalchemy.ext.SAWarning: MyType will not produce a cache key because the
``cache_ok`` attribute is not set to True. This can have significant
performance implications including some performance degradations in
comparison to prior SQLAlchemy versions. Set this attribute to True if this
type object's state is safe to use in a cache key, or False to disable this
warning.
```

For custom and third party SQL elements, such as those constructed using
the techniques described at [Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html), these
warnings will look like:

```
sqlalchemy.exc.SAWarning: Class MyClass will not make use of SQL
compilation caching as it does not set the 'inherit_cache' attribute to
``True``. This can have significant performance implications including some
performance degradations in comparison to prior SQLAlchemy versions. Set
this attribute to True if this object can make use of the cache key
generated by the superclass. Alternatively, this attribute may be set to
False which will disable this warning.
```

For custom and third party dialects which make use of the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect)
class hierarchy, the warnings will look like:

```
sqlalchemy.exc.SAWarning: Dialect database:driver will not make use of SQL
compilation caching as it does not set the 'supports_statement_cache'
attribute to ``True``. This can have significant performance implications
including some performance degradations in comparison to prior SQLAlchemy
versions. Dialect maintainers should seek to set this attribute to True
after appropriate development and testing for SQLAlchemy 1.4 caching
support. Alternatively, this attribute may be set to False which will
disable this warning.
```

### Step three - enable caching for the given objects and/or seek alternatives

Steps to mitigate the lack of caching include:

- Review and set [ExternalType.cache_ok](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType.cache_ok) to `True` for all custom types
  which extend from [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator),
  [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType), as well as subclasses of these such as
  [PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType).  Set this **only** if the custom type does not
  include any additional state attributes which affect how it renders SQL:
  ```
  class MyCustomType(TypeDecorator):
      cache_ok = True
      impl = String
  ```
  If the types in use are from a third-party library, consult with the
  maintainers of that library so that it may be adjusted and released.
  See also
  [ExternalType.cache_ok](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType.cache_ok) - background on requirements to enable
  caching for custom datatypes.
- Make sure third party dialects set [Dialect.supports_statement_cache](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.supports_statement_cache)
  to `True`. What this indicates is that the maintainers of a third party
  dialect have made sure their dialect works with SQLAlchemy 1.4 or greater,
  and that their dialect doesn’t include any compilation features which may get
  in the way of caching. As there are some common compilation patterns which
  can in fact interfere with caching, it’s important that dialect maintainers
  check and test this carefully, adjusting for any of the legacy patterns
  which won’t work with caching.
  See also
  [Caching for Third Party Dialects](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-thirdparty-caching) - background and examples for third-party
  dialects to participate in SQL statement caching.
- Custom SQL classes, including all DQL / DML constructs one might create
  using the [Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html), as well as ad-hoc
  subclasses of objects such as [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).   The [HasCacheKey.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache) attribute
  may be set to `True` for trivial subclasses, which do not contain any
  subclass-specific state information which affects the SQL compilation.
  See also
  [Enabling Caching Support for Custom Constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#compilerext-caching) - guidelines for applying the
  [HasCacheKey.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache) attribute.

See also

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching) - caching system overview

[Object will not produce a cache key, Performance Implications](https://docs.sqlalchemy.org/en/20/errors.html#caching-caveats) - background on warnings emitted when caching
is not enabled for specific constructs and/or dialects.

## How can I profile a SQLAlchemy powered application?

Looking for performance issues typically involves two strategies.  One
is query profiling, and the other is code profiling.

### Query Profiling

Sometimes just plain SQL logging (enabled via python’s logging module
or via the `echo=True` argument on [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)) can give an
idea how long things are taking.  For example, if you log something
right after a SQL operation, you’d see something like this in your
log:

```
17:37:48,325 INFO  [sqlalchemy.engine.base.Engine.0x...048c] SELECT ...
17:37:48,326 INFO  [sqlalchemy.engine.base.Engine.0x...048c] {<params>}
17:37:48,660 DEBUG [myapp.somemessage]
```

if you logged `myapp.somemessage` right after the operation, you know
it took 334ms to complete the SQL part of things.

Logging SQL will also illustrate if dozens/hundreds of queries are
being issued which could be better organized into much fewer queries.
When using the SQLAlchemy ORM, the “eager loading”
feature is provided to partially ([contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager)) or fully
([joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload), [subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload))
automate this activity, but without
the ORM “eager loading” typically means to use joins so that results across multiple
tables can be loaded in one result set instead of multiplying numbers
of queries as more depth is added (i.e. `r + r*r2 + r*r2*r3` …)

For more long-term profiling of queries, or to implement an application-side
“slow query” monitor, events can be used to intercept cursor executions,
using a recipe like the following:

```
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

logging.basicConfig()
logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.DEBUG)

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())
    logger.debug("Start Query: %s", statement)

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    logger.debug("Query Complete!")
    logger.debug("Total Time: %f", total)
```

Above, we use the [ConnectionEvents.before_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute) and
[ConnectionEvents.after_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.after_cursor_execute) events to establish an interception
point around when a statement is executed.  We attach a timer onto the
connection using the `info` dictionary; we use a
stack here for the occasional case where the cursor execute events may be nested.

### Code Profiling

If logging reveals that individual queries are taking too long, you’d
need a breakdown of how much time was spent within the database
processing the query, sending results over the network, being handled
by the [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI), and finally being received by SQLAlchemy’s result set
and/or ORM layer.   Each of these stages can present their own
individual bottlenecks, depending on specifics.

For that you need to use the
[Python Profiling Module](https://docs.python.org/2/library/profile.html).
Below is a simple recipe which works profiling into a context manager:

```
import cProfile
import io
import pstats
import contextlib

@contextlib.contextmanager
def profiled():
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats()
    # uncomment this to see who's calling what
    # ps.print_callers()
    print(s.getvalue())
```

To profile a section of code:

```
with profiled():
    session.scalars(select(FooClass).where(FooClass.somevalue == 8)).all()
```

The output of profiling can be used to give an idea where time is
being spent.   A section of profiling output looks like this:

```
13726 function calls (13042 primitive calls) in 0.014 seconds

Ordered by: cumulative time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
222/21    0.001    0.000    0.011    0.001 lib/sqlalchemy/orm/loading.py:26(instances)
220/20    0.002    0.000    0.010    0.001 lib/sqlalchemy/orm/loading.py:327(_instance)
220/20    0.000    0.000    0.010    0.000 lib/sqlalchemy/orm/loading.py:284(populate_state)
   20    0.000    0.000    0.010    0.000 lib/sqlalchemy/orm/strategies.py:987(load_collection_from_subq)
   20    0.000    0.000    0.009    0.000 lib/sqlalchemy/orm/strategies.py:935(get)
    1    0.000    0.000    0.009    0.009 lib/sqlalchemy/orm/strategies.py:940(_load)
   21    0.000    0.000    0.008    0.000 lib/sqlalchemy/orm/strategies.py:942(<genexpr>)
    2    0.000    0.000    0.004    0.002 lib/sqlalchemy/orm/query.py:2400(__iter__)
    2    0.000    0.000    0.002    0.001 lib/sqlalchemy/orm/query.py:2414(_execute_and_instances)
    2    0.000    0.000    0.002    0.001 lib/sqlalchemy/engine/base.py:659(execute)
    2    0.000    0.000    0.002    0.001 lib/sqlalchemy/sql/elements.py:321(_execute_on_connection)
    2    0.000    0.000    0.002    0.001 lib/sqlalchemy/engine/base.py:788(_execute_clauseelement)

...
```

Above, we can see that the `instances()` SQLAlchemy function was called 222
times (recursively, and 21 times from the outside), taking a total of .011
seconds for all calls combined.

### Execution Slowness

The specifics of these calls can tell us where the time is being spent.
If for example, you see time being spent within `cursor.execute()`,
e.g. against the DBAPI:

```
2    0.102    0.102    0.204    0.102 {method 'execute' of 'sqlite3.Cursor' objects}
```

this would indicate that the database is taking a long time to start returning
results, and it means your query should be optimized, either by adding indexes
or restructuring the query and/or underlying schema.  For that task,
analysis of the query plan is warranted, using a system such as EXPLAIN,
SHOW PLAN, etc. as is provided by the database backend.

### Result Fetching Slowness - Core

If on the other hand you see many thousands of calls related to fetching rows,
or very long calls to `fetchall()`, it may
mean your query is returning more rows than expected, or that the fetching
of rows itself is slow.   The ORM itself typically uses `fetchall()` to fetch
rows (or `fetchmany()` if the [Query.yield_per()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.yield_per) option is used).

An inordinately large number of rows would be indicated
by a very slow call to `fetchall()` at the DBAPI level:

```
2    0.300    0.600    0.300    0.600 {method 'fetchall' of 'sqlite3.Cursor' objects}
```

An unexpectedly large number of rows, even if the ultimate result doesn’t seem
to have many rows, can be the result of a cartesian product - when multiple
sets of rows are combined together without appropriately joining the tables
together.   It’s often easy to produce this behavior with SQLAlchemy Core or
ORM query if the wrong [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects are used in a complex query,
pulling in additional FROM clauses that are unexpected.

On the other hand, a fast call to `fetchall()` at the DBAPI level, but then
slowness when SQLAlchemy’s [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) is asked to do a `fetchall()`,
may indicate slowness in processing of datatypes, such as unicode conversions
and similar:

```
# the DBAPI cursor is fast...
2    0.020    0.040    0.020    0.040 {method 'fetchall' of 'sqlite3.Cursor' objects}

...

# but SQLAlchemy's result proxy is slow, this is type-level processing
2    0.100    0.200    0.100    0.200 lib/sqlalchemy/engine/result.py:778(fetchall)
```

In some cases, a backend might be doing type-level processing that isn’t
needed.   More specifically, seeing calls within the type API that are slow
are better indicators - below is what it looks like when we use a type like
this:

```
from sqlalchemy import TypeDecorator
import time

class Foo(TypeDecorator):
    impl = String

    def process_result_value(self, value, thing):
        # intentionally add slowness for illustration purposes
        time.sleep(0.001)
        return value
```

the profiling output of this intentionally slow operation can be seen like this:

```
200    0.001    0.000    0.237    0.001 lib/sqlalchemy/sql/type_api.py:911(process)
200    0.001    0.000    0.236    0.001 test.py:28(process_result_value)
200    0.235    0.001    0.235    0.001 {time.sleep}
```

that is, we see many expensive calls within the `type_api` system, and the actual
time consuming thing is the `time.sleep()` call.

Make sure to check the [Dialect documentation](https://docs.sqlalchemy.org/en/20/dialects/index.html)
for notes on known performance tuning suggestions at this level, especially for
databases like Oracle.  There may be systems related to ensuring numeric accuracy
or string processing that may not be needed in all cases.

There also may be even more low-level points at which row-fetching performance is suffering;
for example, if time spent seems to focus on a call like `socket.receive()`,
that could indicate that everything is fast except for the actual network connection,
and too much time is spent with data moving over the network.

### Result Fetching Slowness - ORM

To detect slowness in ORM fetching of rows (which is the most common area
of performance concern), calls like `populate_state()` and `_instance()` will
illustrate individual ORM object populations:

```
# the ORM calls _instance for each ORM-loaded row it sees, and
# populate_state for each ORM-loaded row that results in the population
# of an object's attributes
220/20    0.001    0.000    0.010    0.000 lib/sqlalchemy/orm/loading.py:327(_instance)
220/20    0.000    0.000    0.009    0.000 lib/sqlalchemy/orm/loading.py:284(populate_state)
```

The ORM’s slowness in turning rows into ORM-mapped objects is a product
of the complexity of this operation combined with the overhead of cPython.
Common strategies to mitigate this include:

- fetch individual columns instead of full entities, that is:
  ```
  select(User.id, User.name)
  ```
  instead of:
  ```
  select(User)
  ```
- Use [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) objects to organize column-based results:
  ```
  u_b = Bundle("user", User.id, User.name)
  a_b = Bundle("address", Address.id, Address.email)
  for user, address in session.execute(select(u_b, a_b).join(User.addresses)):
      ...
  ```
- Use result caching - see [Dogpile Caching](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-caching) for an in-depth example
  of this.
- Consider a faster interpreter like that of PyPy.

The output of a profile can be a little daunting but after some
practice they are very easy to read.

See also

[Performance](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-performance) - a suite of performance demonstrations
with bundled profiling capabilities.

## I’m inserting 400,000 rows with the ORM and it’s really slow!

The nature of ORM inserts has changed, as most included drivers use RETURNING
with [insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) support as of SQLAlchemy
2.0. See the section [Optimized ORM bulk insert now implemented for all backends other than MySQL](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-6047) for details.

Overall, SQLAlchemy built-in drivers other than that of MySQL should now
offer very fast ORM bulk insert performance.

Third party drivers can opt in to the new bulk infrastructure as well with some
small code changes assuming their backends support the necessary syntaxes.
SQLAlchemy developers would encourage users of third party dialects to post
issues with these drivers, so that they may contact SQLAlchemy developers for
assistance.
