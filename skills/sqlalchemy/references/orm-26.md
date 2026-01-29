# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

ORM Querying Guide

This page is part of the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).

Previous: [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)   |   Next: [Legacy Query API](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html)

# ORM API Features for Querying

## ORM Loader Options

Loader options are objects which, when passed to the
[Select.options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.options) method of a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object or similar SQL
construct, affect the loading of both column and relationship-oriented
attributes. The majority of loader options descend from the [Load](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load)
hierarchy. For a complete overview of using loader options, see the linked
sections below.

See also

- [Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#loading-columns) - details mapper and loading options that affect
  how column and SQL-expression mapped attributes are loaded
- [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html) - details relationship and loading options that
  affect how [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) mapped attributes are loaded

## ORM Execution Options

ORM-level execution options are keyword options that may be associated with a
statement execution using either the
[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options) parameter, which is a
dictionary argument accepted by [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) methods such as
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) and [Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars), or by
associating them directly with the statement to be invoked itself using the
[Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options) method, which accepts them as
arbitrary keyword arguments.

ORM-level options are distinct from the Core level execution options
documented at [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options).
It’s important to note that the ORM options
discussed below are **not** compatible with Core level methods
[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) or
[Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options); the options are ignored at this
level, even if the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is associated
with the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) in use.

Within this section, the [Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options) method
style will be illustrated for examples.

### Populate Existing

The `populate_existing` execution option ensures that, for all rows
loaded, the corresponding instances in the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will
be fully refreshed – erasing any existing data within the objects
(including pending changes) and replacing with the data loaded from the
result.

Example use looks like:

```
>>> stmt = select(User).execution_options(populate_existing=True)
>>> result = session.execute(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
...
```

Normally, ORM objects are only loaded once, and if they are matched up
to the primary key in a subsequent result row, the row is not applied to the
object.  This is both to preserve pending, unflushed changes on the object
as well as to avoid the overhead and complexity of refreshing data which
is already there.   The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) assumes a default working
model of a highly isolated transaction, and to the degree that data is
expected to change within the transaction outside of the local changes being
made, those use cases would be handled using explicit steps such as this method.

Using `populate_existing`, any set of objects that matches a query
can be refreshed, and it also allows control over relationship loader options.
E.g. to refresh an instance while also refreshing a related set of objects:

```
stmt = (
    select(User)
    .where(User.name.in_(names))
    .execution_options(populate_existing=True)
    .options(selectinload(User.addresses))
)
# will refresh all matching User objects as well as the related
# Address objects
users = session.execute(stmt).scalars().all()
```

Another use case for `populate_existing` is in support of various
attribute loading features that can change how an attribute is loaded on
a per-query basis.   Options for which this apply include:

- The [with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) option
- The [PropComparator.and_()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.and_) method that can modify what a loader
  strategy loads
- The [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) option
- The [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) option
- The [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) option to select what attributes to refresh

The `populate_existing` execution option is equvialent to the
[Query.populate_existing()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.populate_existing) method in [1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style) ORM queries.

See also

[I’m re-loading data with my Session but it isn’t seeing changes that I committed elsewhere](https://docs.sqlalchemy.org/en/20/faq/sessions.html#faq-session-identity) - in [Frequently Asked Questions](https://docs.sqlalchemy.org/en/20/faq/index.html)

[Refreshing / Expiring](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-expire) - in the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
documentation

### Autoflush

This option, when passed as `False`, will cause the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
to not invoke the “autoflush” step.  It is equivalent to using the
[Session.no_autoflush](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.no_autoflush) context manager to disable autoflush:

```
>>> stmt = select(User).execution_options(autoflush=False)
>>> session.execute(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
...
```

This option will also work on ORM-enabled [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and
[Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) queries.

The `autoflush` execution option is equvialent to the
[Query.autoflush()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.autoflush) method in [1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style) ORM queries.

See also

[Flushing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)

### Fetching Large Result Sets with Yield Per

The `yield_per` execution option is an integer value which will cause the
[Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) to buffer only a limited number of rows and/or ORM
objects at a time, before making data available to the client.

Normally, the ORM will fetch **all** rows immediately, constructing ORM objects
for each and assembling those objects into a single buffer, before passing this
buffer to the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object as a source of rows to be
returned. The rationale for this behavior is to allow correct behavior for
features such as joined eager loading, uniquifying of results, and the general
case of result handling logic that relies upon the identity map maintaining a
consistent state for every object in a result set as it is fetched.

The purpose of the `yield_per` option is to change this behavior so that the
ORM result set is optimized for iteration through very large result sets (e.g.
> 10K rows), where the user has determined that the above patterns don’t apply.
When `yield_per` is used, the ORM will instead batch ORM results into
sub-collections and yield rows from each sub-collection individually as the
[Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object is iterated, so that the Python interpreter
doesn’t need to declare very large areas of memory which is both time consuming
and leads to excessive memory use. The option affects both the way the database
cursor is used as well as how the ORM constructs rows and objects to be passed
to the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result).

Tip

From the above, it follows that the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) must be
consumed in an iterable fashion, that is, using iteration such as
`for row in result` or using partial row methods such as
[Result.fetchmany()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.fetchmany) or [Result.partitions()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.partitions).
Calling [Result.all()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.all) will defeat the purpose of using
`yield_per`.

Using `yield_per` is equivalent to making use
of both the [Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results)
execution option, which selects for server side cursors to be used
by the backend if supported, and the [Result.yield_per()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.yield_per) method
on the returned [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object,
which establishes a fixed size of rows to be fetched as well as a
corresponding limit to how many ORM objects will be constructed at once.

Tip

`yield_per` is now available as a Core execution option as well,
described in detail at [Using Server Side Cursors (a.k.a. stream results)](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results).  This section details
the use of `yield_per` as an execution option with an ORM
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  The option behaves as similarly as possible
in both contexts.

When used with the ORM, `yield_per` must be established either
via the [Executable.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.execution_options) method on the given statement
or by passing it to the [Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options)
parameter of [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) or other similar [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
method such as [Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars).  Typical use for fetching
ORM objects is illustrated below:

```
>>> stmt = select(User).execution_options(yield_per=10)
>>> for user_obj in session.scalars(stmt):
...     print(user_obj)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
[...] ()
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
...
>>> # ... rows continue ...
```

The above code is equivalent to the example below, which uses
[Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results)
and [Connection.execution_options.max_row_buffer](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.max_row_buffer) Core-level
execution options in conjunction with the [Result.yield_per()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.yield_per)
method of [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result):

```
# equivalent code
>>> stmt = select(User).execution_options(stream_results=True, max_row_buffer=10)
>>> for user_obj in session.scalars(stmt).yield_per(10):
...     print(user_obj)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
[...] ()
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
...
>>> # ... rows continue ...
```

`yield_per` is also commonly used in combination with the
[Result.partitions()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.partitions) method, which will iterate rows in grouped
partitions. The size of each partition defaults to the integer value passed to
`yield_per`, as in the below example:

```
>>> stmt = select(User).execution_options(yield_per=10)
>>> for partition in session.scalars(stmt).partitions():
...     for user_obj in partition:
...         print(user_obj)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
[...] ()
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
...
>>> # ... rows continue ...
```

The `yield_per` execution option **is not compatible** with
[“subquery” eager loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#subquery-eager-loading) loading or
[“joined” eager loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#joined-eager-loading) when using collections. It
is potentially compatible with [“select in” eager loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#selectin-eager-loading) , provided the database driver supports multiple,
independent cursors.

Additionally, the `yield_per` execution option is not compatible
with the [Result.unique()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.unique) method; as this method relies upon
storing a complete set of identities for all rows, it would necessarily
defeat the purpose of using `yield_per` which is to handle an arbitrarily
large number of rows.

Changed in version 1.4.6: An exception is raised when ORM rows are fetched
from a [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object that makes use of the
[Result.unique()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.unique) filter, at the same time as the `yield_per`
execution option is used.

When using the legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object with
[1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style) ORM use, the [Query.yield_per()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.yield_per) method
will have the same result as that of the `yield_per` execution option.

See also

[Using Server Side Cursors (a.k.a. stream results)](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results)

### Identity Token

Deep Alchemy

This option is an advanced-use feature mostly intended
to be used with the [Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html) extension. For
typical cases of loading objects with identical primary keys from different
“shards” or partitions, consider using individual [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
objects per shard first.

The “identity token” is an arbitrary value that can be associated within
the [identity key](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-key) of newly loaded objects.   This element exists
first and foremost to support extensions which perform per-row “sharding”,
where objects may be loaded from any number of replicas of a particular
database table that nonetheless have overlapping primary key values.
The primary consumer of “identity token” is the
[Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html) extension, which supplies a general
framework for persisting objects among multiple “shards” of a particular
database table.

The `identity_token` execution option may be used on a per-query basis
to directly affect this token.   Using it directly, one can populate a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with multiple instances of an object that have the
same primary key and source table, but different “identities”.

One such example is to populate a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with objects that
come from same-named tables in different schemas, using the
[Translation of Schema Names](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating) feature which can affect the choice of schema
within the scope of queries.  Given a mapping as:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class MyTable(Base):
    __tablename__ = "my_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
```

The default “schema” name for the class above is `None`, meaning, no
schema qualification will be written into SQL statements.  However,
if we make use of [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map),
mapping `None` to an alternate schema, we can place instances of
`MyTable` into two different schemas:

```
engine = create_engine(
    "postgresql+psycopg://scott:tiger@localhost/test",
)

with Session(
    engine.execution_options(schema_translate_map={None: "test_schema"})
) as sess:
    sess.add(MyTable(name="this is schema one"))
    sess.commit()

with Session(
    engine.execution_options(schema_translate_map={None: "test_schema_2"})
) as sess:
    sess.add(MyTable(name="this is schema two"))
    sess.commit()
```

The above two blocks create a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object linked to a different
schema translate map each time, and an instance of `MyTable` is persisted
into both `test_schema.my_table` as well as `test_schema_2.my_table`.

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects above are independent.  If we wanted to
persist both objects in one transaction, we would need to use the
[Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html) extension to do this.

However, we can illustrate querying for these objects in one session as follows:

```
with Session(engine) as sess:
    obj1 = sess.scalar(
        select(MyTable)
        .where(MyTable.id == 1)
        .execution_options(
            schema_translate_map={None: "test_schema"},
            identity_token="test_schema",
        )
    )
    obj2 = sess.scalar(
        select(MyTable)
        .where(MyTable.id == 1)
        .execution_options(
            schema_translate_map={None: "test_schema_2"},
            identity_token="test_schema_2",
        )
    )
```

Both `obj1` and `obj2` are distinct from each other.  However, they both
refer to primary key id 1 for the `MyTable` class, yet are distinct.
This is how the `identity_token` comes into play, which we can see in the
inspection of each object, where we look at `InstanceState.key`
to view the two distinct identity tokens:

```
>>> from sqlalchemy import inspect
>>> inspect(obj1).key
(<class '__main__.MyTable'>, (1,), 'test_schema')
>>> inspect(obj2).key
(<class '__main__.MyTable'>, (1,), 'test_schema_2')
```

The above logic takes place automatically when using the
[Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html) extension.

Added in version 2.0.0rc1: - added the `identity_token` ORM level execution
option.

See also

[Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-sharding) - in the [ORM Examples](https://docs.sqlalchemy.org/en/20/orm/examples.html) section.
See the script `separate_schema_translates.py` for a demonstration of
the above use case using the full sharding API.

#### Inspecting entities and columns from ORM-enabled SELECT and DML statements

The [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct, as well as the [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert), [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update)
and [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) constructs (for the latter DML constructs, as of SQLAlchemy
1.4.33), all support the ability to inspect the entities in which these
statements are created against, as well as the columns and datatypes that would
be returned in a result set.

For a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object, this information is available from the
[Select.column_descriptions](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.column_descriptions) attribute. This attribute operates in the
same way as the legacy [Query.column_descriptions](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.column_descriptions) attribute. The format
returned is a list of dictionaries:

```
>>> from pprint import pprint
>>> user_alias = aliased(User, name="user2")
>>> stmt = select(User, User.id, user_alias)
>>> pprint(stmt.column_descriptions)
[{'aliased': False,
  'entity': <class 'User'>,
  'expr': <class 'User'>,
  'name': 'User',
  'type': <class 'User'>},
 {'aliased': False,
  'entity': <class 'User'>,
  'expr': <....InstrumentedAttribute object at ...>,
  'name': 'id',
  'type': Integer()},
 {'aliased': True,
  'entity': <AliasedClass ...; User>,
  'expr': <AliasedClass ...; User>,
  'name': 'user2',
  'type': <class 'User'>}]
```

When [Select.column_descriptions](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.column_descriptions) is used with non-ORM objects
such as plain [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects, the entries
will contain basic information about individual columns returned in all
cases:

```
>>> stmt = select(user_table, address_table.c.id)
>>> pprint(stmt.column_descriptions)
[{'expr': Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False),
  'name': 'id',
  'type': Integer()},
 {'expr': Column('name', String(), table=<user_account>, nullable=False),
  'name': 'name',
  'type': String()},
 {'expr': Column('fullname', String(), table=<user_account>),
  'name': 'fullname',
  'type': String()},
 {'expr': Column('id', Integer(), table=<address>, primary_key=True, nullable=False),
  'name': 'id_1',
  'type': Integer()}]
```

Changed in version 1.4.33: The [Select.column_descriptions](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.column_descriptions) attribute now returns
a value when used against a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) that is not ORM-enabled.  Previously,
this would raise `NotImplementedError`.

For [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert), [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) and [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) constructs, there are
two separate attributes. One is [UpdateBase.entity_description](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.entity_description) which
returns information about the primary ORM entity and database table which the
DML construct would be affecting:

```
>>> from sqlalchemy import update
>>> stmt = update(User).values(name="somename").returning(User.id)
>>> pprint(stmt.entity_description)
{'entity': <class 'User'>,
 'expr': <class 'User'>,
 'name': 'User',
 'table': Table('user_account', ...),
 'type': <class 'User'>}
```

Tip

The [UpdateBase.entity_description](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.entity_description) includes an entry
`"table"` which is actually the **table to be inserted, updated or
deleted** by the statement, which is **not** always the same as the SQL
“selectable” to which the class may be mapped. For example, in a
joined-table inheritance scenario, `"table"` will refer to the local table
for the given entity.

The other is [UpdateBase.returning_column_descriptions](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning_column_descriptions) which
delivers information about the columns present in the RETURNING collection
in a manner roughly similar to that of [Select.column_descriptions](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.column_descriptions):

```
>>> pprint(stmt.returning_column_descriptions)
[{'aliased': False,
  'entity': <class 'User'>,
  'expr': <sqlalchemy.orm.attributes.InstrumentedAttribute ...>,
  'name': 'id',
  'type': Integer()}]
```

Added in version 1.4.33: Added the [UpdateBase.entity_description](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.entity_description)
and [UpdateBase.returning_column_descriptions](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning_column_descriptions) attributes.

#### Additional ORM API Constructs

| Object Name | Description |
| --- | --- |
| aliased(element[, alias, name, flat, ...]) | Produce an alias of the given element, usually anAliasedClassinstance. |
| AliasedClass | Represents an “aliased” form of a mapped class for usage with Query. |
| AliasedInsp | Provide an inspection interface for anAliasedClassobject. |
| Bundle | A grouping of SQL expressions that are returned by aQueryunder one namespace. |
| join(left, right[, onclause, isouter, ...]) | Produce an inner join between left and right clauses. |
| outerjoin(left, right[, onclause, full]) | Produce a left outer join between left and right clauses. |
| with_loader_criteria(entity_or_base, where_criteria[, loader_only, include_aliases, ...]) | Add additional WHERE criteria to the load for all occurrences of
a particular entity. |
| with_parent(instance, prop[, from_entity]) | Create filtering criterion that relates this query’s primary entity
to the given related instance, using establishedrelationship()configuration. |

   function sqlalchemy.orm.aliased(*element:_EntityType[_O]|FromClause*, *alias:FromClause|None=None*, *name:str|None=None*, *flat:bool=False*, *adapt_on_names:bool=False*) → [AliasedClass](#sqlalchemy.orm.util.AliasedClass)[_O] | [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) | AliasedType[_O]

Produce an alias of the given element, usually an [AliasedClass](#sqlalchemy.orm.util.AliasedClass)
instance.

E.g.:

```
my_alias = aliased(MyClass)

stmt = select(MyClass, my_alias).filter(MyClass.id > my_alias.id)
result = session.execute(stmt)
```

The [aliased()](#sqlalchemy.orm.aliased) function is used to create an ad-hoc mapping of a
mapped class to a new selectable.  By default, a selectable is generated
from the normally mapped selectable (typically a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
) using the
[FromClause.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.alias) method. However, [aliased()](#sqlalchemy.orm.aliased)
can also be
used to link the class to a new [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) statement.
Also, the [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) function is a variant of
[aliased()](#sqlalchemy.orm.aliased) that is intended to specify a so-called “polymorphic
selectable”, that corresponds to the union of several joined-inheritance
subclasses at once.

For convenience, the [aliased()](#sqlalchemy.orm.aliased) function also accepts plain
[FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) constructs, such as a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct.   In those cases, the
[FromClause.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.alias)
method is called on the object and the new
[Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) object returned.  The returned
[Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) is not
ORM-mapped in this case.

See also

[ORM Entity Aliases](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-orm-entity-aliases) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Selecting ORM Aliases](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-orm-aliases) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

   Parameters:

- **element** – element to be aliased.  Is normally a mapped class,
  but for convenience can also be a [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
  element.
- **alias** – Optional selectable unit to map the element to.  This is
  usually used to link the object to a subquery, and should be an aliased
  select construct as one would produce from the
  [Query.subquery()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.subquery) method or
  the [Select.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.subquery) or
  [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) methods of the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
  construct.
- **name** – optional string name to use for the alias, if not specified
  by the `alias` parameter.  The name, among other things, forms the
  attribute name that will be accessible via tuples returned by a
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object.  Not supported when creating aliases
  of [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) objects.
- **flat** –
  Boolean, will be passed through to the
  [FromClause.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.alias) call so that aliases of
  [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) objects will alias the individual tables
  inside the join, rather than creating a subquery.  This is generally
  supported by all modern databases with regards to right-nested joins
  and generally produces more efficient queries.
  When [aliased.flat](#sqlalchemy.orm.aliased.params.flat) is combined with
  [aliased.name](#sqlalchemy.orm.aliased.params.name), the resulting joins will alias individual
  tables using a naming scheme similar to `<prefix>_<tablename>`.  This
  naming scheme is for visibility / debugging purposes only and the
  specific scheme is subject to change without notice.
  Added in version 2.0.32: added support for combining
  [aliased.name](#sqlalchemy.orm.aliased.params.name) with [aliased.flat](#sqlalchemy.orm.aliased.params.flat).
  Previously, this would raise `NotImplementedError`.
- **adapt_on_names** –
  if True, more liberal “matching” will be used when
  mapping the mapped columns of the ORM entity to those of the
  given selectable - a name-based match will be performed if the
  given selectable doesn’t otherwise have a column that corresponds
  to one on the entity.  The use case for this is when associating
  an entity with some derived selectable such as one that uses
  aggregate functions:
  ```
  class UnitPrice(Base):
      __tablename__ = "unit_price"
      ...
      unit_id = Column(Integer)
      price = Column(Numeric)
  aggregated_unit_price = (
      Session.query(func.sum(UnitPrice.price).label("price"))
      .group_by(UnitPrice.unit_id)
      .subquery()
  )
  aggregated_unit_price = aliased(
      UnitPrice, alias=aggregated_unit_price, adapt_on_names=True
  )
  ```
  Above, functions on `aggregated_unit_price` which refer to
  `.price` will return the
  `func.sum(UnitPrice.price).label('price')` column, as it is
  matched on the name “price”.  Ordinarily, the “price” function
  wouldn’t have any “column correspondence” to the actual
  `UnitPrice.price` column as it is not a proxy of the original.

      class sqlalchemy.orm.util.AliasedClass

*inherits from* `sqlalchemy.inspection.Inspectable`, `sqlalchemy.orm.ORMColumnsClauseRole`

Represents an “aliased” form of a mapped class for usage with Query.

The ORM equivalent of a [alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.alias)
construct, this object mimics the mapped class using a
`__getattr__` scheme and maintains a reference to a
real [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) object.

A primary purpose of [AliasedClass](#sqlalchemy.orm.util.AliasedClass) is to serve as an alternate
within a SQL statement generated by the ORM, such that an existing
mapped entity can be used in multiple contexts.   A simple example:

```
# find all pairs of users with the same name
user_alias = aliased(User)
session.query(User, user_alias).join(
    (user_alias, User.id > user_alias.id)
).filter(User.name == user_alias.name)
```

[AliasedClass](#sqlalchemy.orm.util.AliasedClass) is also capable of mapping an existing mapped
class to an entirely new selectable, provided this selectable is column-
compatible with the existing mapped selectable, and it can also be
configured in a mapping as the target of a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).
See the links below for examples.

The [AliasedClass](#sqlalchemy.orm.util.AliasedClass) object is constructed typically using the
[aliased()](#sqlalchemy.orm.aliased) function.   It also is produced with additional
configuration when using the [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) function.

The resulting object is an instance of [AliasedClass](#sqlalchemy.orm.util.AliasedClass).
This object implements an attribute scheme which produces the
same attribute and method interface as the original mapped
class, allowing [AliasedClass](#sqlalchemy.orm.util.AliasedClass) to be compatible
with any attribute technique which works on the original class,
including hybrid attributes (see [Hybrid Attributes](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html)).

The [AliasedClass](#sqlalchemy.orm.util.AliasedClass) can be inspected for its underlying
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper), aliased selectable, and other information
using [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect):

```
from sqlalchemy import inspect

my_alias = aliased(MyClass)
insp = inspect(my_alias)
```

The resulting inspection object is an instance of [AliasedInsp](#sqlalchemy.orm.util.AliasedInsp).

See also

[aliased()](#sqlalchemy.orm.aliased)

[with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic)

[Relationship to Aliased Class](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-aliased-class)

[Row-Limited Relationships with Window Functions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-to-window-function)

     class sqlalchemy.orm.util.AliasedInsp

*inherits from* `sqlalchemy.orm.ORMEntityColumnsClauseRole`, `sqlalchemy.orm.ORMFromClauseRole`, [sqlalchemy.sql.cache_key.HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey), [sqlalchemy.orm.base.InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr), `sqlalchemy.util.langhelpers.MemoizedSlots`, `sqlalchemy.inspection.Inspectable`, `typing.Generic`

Provide an inspection interface for an
[AliasedClass](#sqlalchemy.orm.util.AliasedClass) object.

The [AliasedInsp](#sqlalchemy.orm.util.AliasedInsp) object is returned
given an [AliasedClass](#sqlalchemy.orm.util.AliasedClass) using the
[inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function:

```
from sqlalchemy import inspect
from sqlalchemy.orm import aliased

my_alias = aliased(MyMappedClass)
insp = inspect(my_alias)
```

Attributes on [AliasedInsp](#sqlalchemy.orm.util.AliasedInsp)
include:

- `entity` - the [AliasedClass](#sqlalchemy.orm.util.AliasedClass) represented.
- `mapper` - the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) mapping the underlying class.
- `selectable` - the [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias)
  construct which ultimately
  represents an aliased [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or
  [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
  construct.
- `name` - the name of the alias.  Also is used as the attribute
  name when returned in a result tuple from [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query).
- `with_polymorphic_mappers` - collection of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
  objects
  indicating all those mappers expressed in the select construct
  for the [AliasedClass](#sqlalchemy.orm.util.AliasedClass).
- `polymorphic_on` - an alternate column or SQL expression which
  will be used as the “discriminator” for a polymorphic load.

See also

[Runtime Inspection API](https://docs.sqlalchemy.org/en/20/core/inspection.html)

     class sqlalchemy.orm.Bundle

*inherits from* `sqlalchemy.orm.ORMColumnsClauseRole`, `sqlalchemy.sql.annotation.SupportsCloneAnnotations`, `sqlalchemy.sql.cache_key.MemoizedHasCacheKey`, `sqlalchemy.inspection.Inspectable`, [sqlalchemy.orm.base.InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)

A grouping of SQL expressions that are returned by a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
under one namespace.

The [Bundle](#sqlalchemy.orm.Bundle) essentially allows nesting of the tuple-based
results returned by a column-oriented [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object.
It also
is extensible via simple subclassing, where the primary capability
to override is that of how the set of expressions should be returned,
allowing post-processing as well as custom return types, without
involving ORM identity-mapped classes.

See also

[Grouping Selected Attributes with Bundles](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#bundles)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newBundle. |
| c | An alias forBundle.columns. |
| columns | A namespace of SQL expressions referred to by thisBundle. |
| create_row_processor() | Produce the “row processing” function for thisBundle. |
| is_aliased_class | True if this object is an instance ofAliasedClass. |
| is_bundle | True if this object is an instance ofBundle. |
| is_clause_element | True if this object is an instance ofClauseElement. |
| is_mapper | True if this object is an instance ofMapper. |
| label() | Provide a copy of thisBundlepassing a new label. |
| single_entity | If True, queries for a single Bundle will be returned as a single
entity, rather than an element within a keyed tuple. |

   method [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)__init__(*name:str*, **exprs:_ColumnExpressionArgument[Any]*, ***kw:Any*)

Construct a new [Bundle](#sqlalchemy.orm.Bundle).

e.g.:

```
bn = Bundle("mybundle", MyClass.x, MyClass.y)

for row in session.query(bn).filter(bn.c.x == 5).filter(bn.c.y == 4):
    print(row.mybundle.x, row.mybundle.y)
```

   Parameters:

- **name** – name of the bundle.
- ***exprs** – columns or SQL expressions comprising the bundle.
- **single_entity=False** – if True, rows for this [Bundle](#sqlalchemy.orm.Bundle)
  can be returned as a “single entity” outside of any enclosing tuple
  in the same manner as a mapped entity.

      attribute [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)c: ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]

An alias for [Bundle.columns](#sqlalchemy.orm.Bundle.columns).

    attribute [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)columns: ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]

A namespace of SQL expressions referred to by this [Bundle](#sqlalchemy.orm.Bundle).

> e.g.:
>
>
>
> ```
> bn = Bundle("mybundle", MyClass.x, MyClass.y)
>
> q = sess.query(bn).filter(bn.c.x == 5)
> ```
>
>
>
> Nesting of bundles is also supported:
>
>
>
> ```
> b1 = Bundle(
>     "b1",
>     Bundle("b2", MyClass.a, MyClass.b),
>     Bundle("b3", MyClass.x, MyClass.y),
> )
>
> q = sess.query(b1).filter(b1.c.b2.c.a == 5).filter(b1.c.b3.c.y == 9)
> ```

See also

[Bundle.c](#sqlalchemy.orm.Bundle.c)

     method [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)create_row_processor(*query:Select[Any]*, *procs:Sequence[Callable[[Row[Any]],Any]]*, *labels:Sequence[str]*) → Callable[[[Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)[Any]], Any]

Produce the “row processing” function for this [Bundle](#sqlalchemy.orm.Bundle).

May be overridden by subclasses to provide custom behaviors when
results are fetched. The method is passed the statement object and a
set of “row processor” functions at query execution time; these
processor functions when given a result row will return the individual
attribute value, which can then be adapted into any kind of return data
structure.

The example below illustrates replacing the usual [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
return structure with a straight Python dictionary:

```
from sqlalchemy.orm import Bundle

class DictBundle(Bundle):
    def create_row_processor(self, query, procs, labels):
        "Override create_row_processor to return values as dictionaries"

        def proc(row):
            return dict(zip(labels, (proc(row) for proc in procs)))

        return proc
```

A result from the above [Bundle](#sqlalchemy.orm.Bundle) will return dictionary
values:

```
bn = DictBundle("mybundle", MyClass.data1, MyClass.data2)
for row in session.execute(select(bn)).where(bn.c.data1 == "d1"):
    print(row.mybundle["data1"], row.mybundle["data2"])
```

     attribute [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)is_aliased_class = False

True if this object is an instance of [AliasedClass](#sqlalchemy.orm.util.AliasedClass).

    attribute [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)is_bundle = True

True if this object is an instance of [Bundle](#sqlalchemy.orm.Bundle).

    attribute [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)is_clause_element = False

True if this object is an instance of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

    attribute [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)is_mapper = False

True if this object is an instance of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper).

    method [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)label(*name*)

Provide a copy of this [Bundle](#sqlalchemy.orm.Bundle) passing a new label.

    attribute [sqlalchemy.orm.Bundle.](#sqlalchemy.orm.Bundle)single_entity = False

If True, queries for a single Bundle will be returned as a single
entity, rather than an element within a keyed tuple.

     function sqlalchemy.orm.with_loader_criteria(*entity_or_base:_EntityType[Any]*, *where_criteria:_ColumnExpressionArgument[bool]|Callable[[Any],_ColumnExpressionArgument[bool]]*, *loader_only:bool=False*, *include_aliases:bool=False*, *propagate_to_loaders:bool=True*, *track_closure_variables:bool=True*) → LoaderCriteriaOption

Add additional WHERE criteria to the load for all occurrences of
a particular entity.

Added in version 1.4.

The [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) option is intended to add
limiting criteria to a particular kind of entity in a query,
**globally**, meaning it will apply to the entity as it appears
in the SELECT query as well as within any subqueries, join
conditions, and relationship loads, including both eager and lazy
loaders, without the need for it to be specified in any particular
part of the query.    The rendering logic uses the same system used by
single table inheritance to ensure a certain discriminator is applied
to a table.

E.g., using [2.0-style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1) queries, we can limit the way the
`User.addresses` collection is loaded, regardless of the kind
of loading used:

```
from sqlalchemy.orm import with_loader_criteria

stmt = select(User).options(
    selectinload(User.addresses),
    with_loader_criteria(Address, Address.email_address != "foo"),
)
```

Above, the “selectinload” for `User.addresses` will apply the
given filtering criteria to the WHERE clause.

Another example, where the filtering will be applied to the
ON clause of the join, in this example using [1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style)
queries:

```
q = (
    session.query(User)
    .outerjoin(User.addresses)
    .options(with_loader_criteria(Address, Address.email_address != "foo"))
)
```

The primary purpose of [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) is to use
it in the [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute) event handler
to ensure that all occurrences of a particular entity are filtered
in a certain way, such as filtering for access control roles.    It
also can be used to apply criteria to relationship loads.  In the
example below, we can apply a certain set of rules to all queries
emitted by a particular [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session):

```
session = Session(bind=engine)

@event.listens_for("do_orm_execute", session)
def _add_filtering_criteria(execute_state):

    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.is_relationship_load
    ):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                SecurityRole,
                lambda cls: cls.role.in_(["some_role"]),
                include_aliases=True,
            )
        )
```

In the above example, the [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute)
event will intercept all queries emitted using the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session). For those queries which are SELECT statements
and are not attribute or relationship loads a custom
[with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) option is added to the query.    The
[with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) option will be used in the given
statement and will also be automatically propagated to all relationship
loads that descend from this query.

The criteria argument given is a `lambda` that accepts a `cls`
argument.  The given class will expand to include all mapped subclass
and need not itself be a mapped class.

Tip

When using [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) option in
conjunction with the [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) loader option,
it’s important to note that [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) only
affects the part of the query that determines what SQL is rendered
in terms of the WHERE and FROM clauses. The
[contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) option does not affect the rendering of
the SELECT statement outside of the columns clause, so does not have
any interaction with the [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) option.
However, the way things “work” is that [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager)
is meant to be used with a query that is already selecting from the
additional entities in some way, where
[with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) can apply it’s additional
criteria.

In the example below, assuming a mapping relationship as
`A -> A.bs -> B`, the given [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria)
option will affect the way in which the JOIN is rendered:

```
stmt = (
    select(A)
    .join(A.bs)
    .options(contains_eager(A.bs), with_loader_criteria(B, B.flag == 1))
)
```

Above, the given [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) option will
affect the ON clause of the JOIN that is specified by
`.join(A.bs)`, so is applied as expected. The
[contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) option has the effect that columns from
`B` are added to the columns clause:

```
SELECT
    b.id, b.a_id, b.data, b.flag,
    a.id AS id_1,
    a.data AS data_1
FROM a JOIN b ON a.id = b.a_id AND b.flag = :flag_1
```

The use of the [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) option within the above
statement has no effect on the behavior of the
[with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) option. If the
[contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) option were omitted, the SQL would be
the same as regards the FROM and WHERE clauses, where
[with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) continues to add its criteria to
the ON clause of the JOIN. The addition of
[contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) only affects the columns clause, in that
additional columns against `b` are added which are then consumed
by the ORM to produce `B` instances.

Warning

The use of a lambda inside of the call to
[with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) is only invoked **once per unique
class**. Custom functions should not be invoked within this lambda.
See [Using Lambdas to add significant speed gains to statement production](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-lambda-caching) for an overview of the “lambda SQL”
feature, which is for advanced use only.

   Parameters:

- **entity_or_base** – a mapped class, or a class that is a super
  class of a particular set of mapped classes, to which the rule
  will apply.
- **where_criteria** –
  a Core SQL expression that applies limiting
  criteria.   This may also be a “lambda:” or Python function that
  accepts a target class as an argument, when the given class is
  a base with many different mapped subclasses.
  Note
  To support pickling, use a module-level Python function to
  produce the SQL expression instead of a lambda or a fixed SQL
  expression, which tend to not be picklable.
- **include_aliases** – if True, apply the rule to [aliased()](#sqlalchemy.orm.aliased)
  constructs as well.
- **propagate_to_loaders** –
  defaults to True, apply to relationship
  loaders such as lazy loaders.   This indicates that the
  option object itself including SQL expression is carried along with
  each loaded instance.  Set to `False` to prevent the object from
  being assigned to individual instances.
  See also
  [ORM Query Events](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-session-orm-events) - includes examples of using
  [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria).
  [Adding global WHERE / ON criteria](https://docs.sqlalchemy.org/en/20/orm/session_events.html#do-orm-execute-global-criteria) - basic example on how to
  combine [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria) with the
  [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute) event.
- **track_closure_variables** –
  when False, closure variables inside
  of a lambda expression will not be used as part of
  any cache key.    This allows more complex expressions to be used
  inside of a lambda expression but requires that the lambda ensures
  it returns the identical SQL every time given a particular class.
  Added in version 1.4.0b2.

      function sqlalchemy.orm.join(*left:_FromClauseArgument*, *right:_FromClauseArgument*, *onclause:_OnClauseArgument|None=None*, *isouter:bool=False*, *full:bool=False*) → _ORMJoin

Produce an inner join between left and right clauses.

[join()](#sqlalchemy.orm.join) is an extension to the core join interface
provided by [join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.join), where the
left and right selectable may be not only core selectable
objects such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), but also mapped classes or
[AliasedClass](#sqlalchemy.orm.util.AliasedClass) instances.   The “on” clause can
be a SQL expression or an ORM mapped attribute
referencing a configured [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

[join()](#sqlalchemy.orm.join) is not commonly needed in modern usage,
as its functionality is encapsulated within that of the
[Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) and [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join)
methods. which feature a
significant amount of automation beyond [join()](#sqlalchemy.orm.join)
by itself.  Explicit use of [join()](#sqlalchemy.orm.join)
with ORM-enabled SELECT statements involves use of the
[Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) method, as in:

```
from sqlalchemy.orm import join

stmt = (
    select(User)
    .select_from(join(User, Address, User.addresses))
    .filter(Address.email_address == "[email protected]")
)
```

In modern SQLAlchemy the above join can be written more
succinctly as:

```
stmt = (
    select(User)
    .join(User.addresses)
    .filter(Address.email_address == "[email protected]")
)
```

Warning

using [join()](#sqlalchemy.orm.join) directly may not work properly
with modern ORM options such as [with_loader_criteria()](#sqlalchemy.orm.with_loader_criteria).
It is strongly recommended to use the idiomatic join patterns
provided by methods such as [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) and
[Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from) when creating ORM joins.

See also

[Joins](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-joins) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html) for
background on idiomatic ORM join patterns

     function sqlalchemy.orm.outerjoin(*left:_FromClauseArgument*, *right:_FromClauseArgument*, *onclause:_OnClauseArgument|None=None*, *full:bool=False*) → _ORMJoin

Produce a left outer join between left and right clauses.

This is the “outer join” version of the [join()](#sqlalchemy.orm.join) function,
featuring the same behavior except that an OUTER JOIN is generated.
See that function’s documentation for other usage details.

    function sqlalchemy.orm.with_parent(*instance:object*, *prop:attributes.QueryableAttribute[Any]*, *from_entity:_EntityType[Any]|None=None*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Create filtering criterion that relates this query’s primary entity
to the given related instance, using established
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
configuration.

E.g.:

```
stmt = select(Address).where(with_parent(some_user, User.addresses))
```

The SQL rendered is the same as that rendered when a lazy loader
would fire off from the given parent on that attribute, meaning
that the appropriate state is taken from the parent object in
Python without the need to render joins to the parent table
in the rendered statement.

The given property may also make use of [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type)
to indicate the left side of the criteria:

```
a1 = aliased(Address)
a2 = aliased(Address)
stmt = select(a1, a2).where(with_parent(u1, User.addresses.of_type(a2)))
```

The above use is equivalent to using the
`from_entity()` argument:

```
a1 = aliased(Address)
a2 = aliased(Address)
stmt = select(a1, a2).where(
    with_parent(u1, User.addresses, from_entity=a2)
)
```

   Parameters:

- **instance** – An instance which has some [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).
- **property** – Class-bound attribute, which indicates
  what relationship from the instance should be used to reconcile the
  parent/child relationship.
- **from_entity** –
  Entity in which to consider as the left side.  This defaults to the
  “zero” entity of the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) itself.
  Added in version 1.2.

ORM Querying Guide

Next Query Guide Section: [Legacy Query API](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html)
