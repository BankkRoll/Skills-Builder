# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

ORM Querying Guide

This page is part of the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).

Previous: [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)   |   Next: [Writing SELECT statements for Inheritance Mappings](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html)

# Writing SELECT statements for ORM Mapped Classes

About this Document

This section makes use of ORM mappings first illustrated in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial), shown in the section
[Declaring Mapped Classes](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-declaring-mapped-classes).

[View the ORM setup for this page](https://docs.sqlalchemy.org/en/20/orm/queryguide/_plain_setup.html).

SELECT statements are produced by the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) function which
returns a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object.  The entities and/or SQL expressions
to return (i.e. the “columns” clause) are passed positionally to the
function.  From there, additional methods are used to generate the complete
statement, such as the [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where) method illustrated below:

```
>>> from sqlalchemy import select
>>> stmt = select(User).where(User.name == "spongebob")
```

Given a completed [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object, in order to execute it within
the ORM to get rows back, the object is passed to
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), where a [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object is then
returned:

```
>>> result = session.execute(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
>>> for user_obj in result.scalars():
...     print(f"{user_obj.name} {user_obj.fullname}")
spongebob Spongebob Squarepants
```

## Selecting ORM Entities and Attributes

The [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct accepts ORM entities, including mapped
classes as well as class-level attributes representing mapped columns, which
are converted into [ORM-annotated](https://docs.sqlalchemy.org/en/20/glossary.html#term-ORM-annotated) [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) and
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) elements at construction time.

A [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object that contains ORM-annotated entities is normally
executed using a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object, and not a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
object, so that ORM-related features may take effect, including that
instances of ORM-mapped objects may be returned.  When using the
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) directly, result rows will only contain
column-level data.

### Selecting ORM Entities

Below we select from the `User` entity, producing a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
that selects from the mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) to which `User` is mapped:

```
>>> result = session.execute(select(User).order_by(User.id))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.id
[...] ()
```

When selecting from ORM entities, the entity itself is returned in the result
as a row with a single element, as opposed to a series of individual columns;
for example above, the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) returns [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
objects that have just a single element per row, that element holding onto a
`User` object:

```
>>> result.all()
[(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),),
 (User(id=2, name='sandy', fullname='Sandy Cheeks'),),
 (User(id=3, name='patrick', fullname='Patrick Star'),),
 (User(id=4, name='squidward', fullname='Squidward Tentacles'),),
 (User(id=5, name='ehkrabs', fullname='Eugene H. Krabs'),)]
```

When selecting a list of single-element rows containing ORM entities, it is
typical to skip the generation of [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects and instead
receive ORM entities directly.   This is most easily achieved by using the
[Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars) method to execute, rather than the
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method, so that a [ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult) object
which yields single elements rather than rows is returned:

```
>>> session.scalars(select(User).order_by(User.id)).all()
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.id
[...] ()
[User(id=1, name='spongebob', fullname='Spongebob Squarepants'),
 User(id=2, name='sandy', fullname='Sandy Cheeks'),
 User(id=3, name='patrick', fullname='Patrick Star'),
 User(id=4, name='squidward', fullname='Squidward Tentacles'),
 User(id=5, name='ehkrabs', fullname='Eugene H. Krabs')]
```

Calling the [Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars) method is the equivalent to calling
upon [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) to receive a [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object,
then calling upon [Result.scalars()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalars) to receive a
[ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult) object.

### Selecting Multiple ORM Entities Simultaneously

The [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) function accepts any number of ORM classes and/or
column expressions at once, including that multiple ORM classes may be
requested.   When SELECTing from multiple ORM classes, they are named
in each result row based on their class name.   In the example below,
the result rows for a SELECT against `User` and `Address` will
refer to them under the names `User` and `Address`:

```
>>> stmt = select(User, Address).join(User.addresses).order_by(User.id, Address.id)
>>> for row in session.execute(stmt):
...     print(f"{row.User.name} {row.Address.email_address}")
SELECT user_account.id, user_account.name, user_account.fullname,
address.id AS id_1, address.user_id, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
ORDER BY user_account.id, address.id
[...] ()
spongebob [email protected]
sandy [email protected]
sandy [email protected]
patrick [email protected]
squidward [email protected]
```

If we wanted to assign different names to these entities in the rows, we would
use the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct using the [aliased.name](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased.params.name)
parameter to alias them with an explicit name:

```
>>> from sqlalchemy.orm import aliased
>>> user_cls = aliased(User, name="user_cls")
>>> email_cls = aliased(Address, name="email")
>>> stmt = (
...     select(user_cls, email_cls)
...     .join(user_cls.addresses.of_type(email_cls))
...     .order_by(user_cls.id, email_cls.id)
... )
>>> row = session.execute(stmt).first()
SELECT user_cls.id, user_cls.name, user_cls.fullname,
email.id AS id_1, email.user_id, email.email_address
FROM user_account AS user_cls JOIN address AS email
ON user_cls.id = email.user_id ORDER BY user_cls.id, email.id
[...] ()
>>> print(f"{row.user_cls.name} {row.email.email_address}")
spongebob [email protected]
```

The aliased form above is discussed further at
[Using Relationship to join between aliased targets](#orm-queryguide-joining-relationships-aliased).

An existing [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct may also have ORM classes and/or
column expressions added to its columns clause using the
[Select.add_columns()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.add_columns) method. We can produce the same statement as
above using this form as well:

```
>>> stmt = (
...     select(User).join(User.addresses).add_columns(Address).order_by(User.id, Address.id)
... )
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname,
address.id AS id_1, address.user_id, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
ORDER BY user_account.id, address.id
```

### Selecting Individual Attributes

The attributes on a mapped class, such as `User.name` and
`Address.email_address`, can be used just like [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or
other SQL expression objects when passed to [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select). Creating a
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) that is against specific columns will return [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
objects, and **not** entities like `User` or `Address` objects.
Each [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) will have each column represented individually:

```
>>> result = session.execute(
...     select(User.name, Address.email_address)
...     .join(User.addresses)
...     .order_by(User.id, Address.id)
... )
SELECT user_account.name, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
ORDER BY user_account.id, address.id
[...] ()
```

The above statement returns [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects with `name` and
`email_address` columns, as illustrated in the runtime demonstration below:

```
>>> for row in result:
...     print(f"{row.name}  {row.email_address}")
spongebob  [email protected]
sandy  [email protected]
sandy  [email protected]
patrick  [email protected]
squidward  [email protected]
```

### Grouping Selected Attributes with Bundles

The [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) construct is an extensible ORM-only construct that
allows sets of column expressions to be grouped in result rows:

```
>>> from sqlalchemy.orm import Bundle
>>> stmt = select(
...     Bundle("user", User.name, User.fullname),
...     Bundle("email", Address.email_address),
... ).join_from(User, Address)
>>> for row in session.execute(stmt):
...     print(f"{row.user.name} {row.user.fullname} {row.email.email_address}")
SELECT user_account.name, user_account.fullname, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
[...] ()
spongebob Spongebob Squarepants [email protected]
sandy Sandy Cheeks [email protected]
sandy Sandy Cheeks [email protected]
patrick Patrick Star [email protected]
squidward Squidward Tentacles [email protected]
```

The [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) is potentially useful for creating lightweight views
and custom column groupings. [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) may also be subclassed in
order to return alternate data structures; see
[Bundle.create_row_processor()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle.create_row_processor) for an example.

See also

[Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle)

[Bundle.create_row_processor()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle.create_row_processor)

### Selecting ORM Aliases

As discussed in the tutorial at [Using Aliases](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-using-aliases), to create a
SQL alias of an ORM entity is achieved using the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
construct against a mapped class:

```
>>> from sqlalchemy.orm import aliased
>>> u1 = aliased(User)
>>> print(select(u1).order_by(u1.id))
SELECT user_account_1.id, user_account_1.name, user_account_1.fullname
FROM user_account AS user_account_1 ORDER BY user_account_1.id
```

As is the case when using [Table.alias()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.alias), the SQL alias
is anonymously named.   For the case of selecting the entity from a row
with an explicit name, the [aliased.name](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased.params.name) parameter may be
passed as well:

```
>>> from sqlalchemy.orm import aliased
>>> u1 = aliased(User, name="u1")
>>> stmt = select(u1).order_by(u1.id)
>>> row = session.execute(stmt).first()
SELECT u1.id, u1.name, u1.fullname
FROM user_account AS u1 ORDER BY u1.id
[...] ()
>>> print(f"{row.u1.name}")
spongebob
```

See also

The [aliased](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct is central for several use cases,
including:

- making use of subqueries with the ORM; the sections
  [Selecting Entities from Subqueries](#orm-queryguide-subqueries) and
  [Joining to Subqueries](#orm-queryguide-join-subqueries) discuss this further.
- Controlling the name of an entity in a result set; see
  [Selecting Multiple ORM Entities Simultaneously](#orm-queryguide-select-multiple-entities) for an example
- Joining to the same ORM entity multiple times; see
  [Using Relationship to join between aliased targets](#orm-queryguide-joining-relationships-aliased) for an example.

### Getting ORM Results from Textual Statements

The ORM supports loading of entities from SELECT statements that come from
other sources. The typical use case is that of a textual SELECT statement,
which in SQLAlchemy is represented using the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct. A
[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct can be augmented with information about the
ORM-mapped columns that the statement would load; this can then be associated
with the ORM entity itself so that ORM objects can be loaded based on this
statement.

Given a textual SQL statement we’d like to load from:

```
>>> from sqlalchemy import text
>>> textual_sql = text("SELECT id, name, fullname FROM user_account ORDER BY id")
```

We can add column information to the statement by using the
[TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method; when this method is invoked, the
[TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) object is converted into a [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect)
object, which takes on a role that is comparable to the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
construct.  The [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method
is typically passed [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects or equivalent, and in this
case we can make use of the ORM-mapped attributes on the `User` class
directly:

```
>>> textual_sql = textual_sql.columns(User.id, User.name, User.fullname)
```

We now have an ORM-configured SQL construct that as given, can load the “id”,
“name” and “fullname” columns separately.   To use this SELECT statement as a
source of complete `User` entities instead, we can link these columns to a
regular ORM-enabled
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct using the [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement)
method:

```
>>> orm_sql = select(User).from_statement(textual_sql)
>>> for user_obj in session.execute(orm_sql).scalars():
...     print(user_obj)
SELECT id, name, fullname FROM user_account ORDER BY id
[...] ()
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
User(id=3, name='patrick', fullname='Patrick Star')
User(id=4, name='squidward', fullname='Squidward Tentacles')
User(id=5, name='ehkrabs', fullname='Eugene H. Krabs')
```

The same [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect) object can also be converted into
a subquery using the [TextualSelect.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect.subquery) method,
and linked to the `User` entity to it using the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
construct, in a similar manner as discussed below in [Selecting Entities from Subqueries](#orm-queryguide-subqueries):

```
>>> orm_subquery = aliased(User, textual_sql.subquery())
>>> stmt = select(orm_subquery)
>>> for user_obj in session.execute(stmt).scalars():
...     print(user_obj)
SELECT anon_1.id, anon_1.name, anon_1.fullname
FROM (SELECT id, name, fullname FROM user_account ORDER BY id) AS anon_1
[...] ()
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
User(id=3, name='patrick', fullname='Patrick Star')
User(id=4, name='squidward', fullname='Squidward Tentacles')
User(id=5, name='ehkrabs', fullname='Eugene H. Krabs')
```

The difference between using the [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect) directly with
[Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) versus making use of `aliased()`
is that in the former case, no subquery is produced in the resulting SQL.
This can in some scenarios be advantageous from a performance or complexity
perspective.

### Selecting Entities from Subqueries

The [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct discussed in the previous section
can be used with any [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) construct that comes from a
method such as [Select.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.subquery) to link ORM entities to the
columns returned by that subquery; by default, there must be a **column correspondence**
relationship between the columns delivered by the subquery and the columns
to which the entity is mapped, meaning, the subquery needs to be ultimately
derived from those entities, such as in the example below:

```
>>> inner_stmt = select(User).where(User.id < 7).order_by(User.id)
>>> subq = inner_stmt.subquery()
>>> aliased_user = aliased(User, subq)
>>> stmt = select(aliased_user)
>>> for user_obj in session.execute(stmt).scalars():
...     print(user_obj)
 SELECT anon_1.id, anon_1.name, anon_1.fullname
FROM (SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
FROM user_account
WHERE user_account.id < ? ORDER BY user_account.id) AS anon_1
[generated in ...] (7,)
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
User(id=3, name='patrick', fullname='Patrick Star')
User(id=4, name='squidward', fullname='Squidward Tentacles')
User(id=5, name='ehkrabs', fullname='Eugene H. Krabs')
```

Alternatively, an aliased subquery can be matched to the entity based on name
by applying the [aliased.adapt_on_names](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased.params.adapt_on_names) parameter:

```
>>> from sqlalchemy import literal
>>> inner_stmt = select(
...     literal(14).label("id"),
...     literal("made up name").label("name"),
...     literal("made up fullname").label("fullname"),
... )
>>> subq = inner_stmt.subquery()
>>> aliased_user = aliased(User, subq, adapt_on_names=True)
>>> stmt = select(aliased_user)
>>> for user_obj in session.execute(stmt).scalars():
...     print(user_obj)
SELECT anon_1.id, anon_1.name, anon_1.fullname
FROM (SELECT ? AS id, ? AS name, ? AS fullname) AS anon_1
[generated in ...] (14, 'made up name', 'made up fullname')
User(id=14, name='made up name', fullname='made up fullname')
```

See also

[ORM Entity Subqueries/CTEs](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-subqueries-orm-aliased) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Joining to Subqueries](#orm-queryguide-join-subqueries)

### Selecting Entities from UNIONs and other set operations

The [union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union) and [union_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union_all) functions are the most
common set operations, which along with other set operations such as
[except_()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.except_), [intersect()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.intersect) and others deliver an object known as
a [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect), which is composed of multiple
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) constructs joined by a set-operation keyword.   ORM entities may
be selected from simple compound selects using the [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement)
method illustrated previously at [Getting ORM Results from Textual Statements](#orm-queryguide-selecting-text).  In
this method, the UNION statement is the complete statement that will be
rendered, no additional criteria can be added after [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement)
is used:

```
>>> from sqlalchemy import union_all
>>> u = union_all(
...     select(User).where(User.id < 2), select(User).where(User.id == 3)
... ).order_by(User.id)
>>> stmt = select(User).from_statement(u)
>>> for user_obj in session.execute(stmt).scalars():
...     print(user_obj)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.id < ? UNION ALL SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.id = ? ORDER BY id
[generated in ...] (2, 3)
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=3, name='patrick', fullname='Patrick Star')
```

A [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect) construct can be more flexibly used within
a query that can be further modified by organizing it into a subquery
and linking it to an ORM entity using [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased),
as illustrated previously at [Selecting Entities from Subqueries](#orm-queryguide-subqueries).  In the
example below, we first use [CompoundSelect.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect.subquery) to create
a subquery of the UNION ALL statement, we then package that into the
[aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct where it can be used like any other mapped
entity in a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct, including that we can add filtering
and order by criteria based on its exported columns:

```
>>> subq = union_all(
...     select(User).where(User.id < 2), select(User).where(User.id == 3)
... ).subquery()
>>> user_alias = aliased(User, subq)
>>> stmt = select(user_alias).order_by(user_alias.id)
>>> for user_obj in session.execute(stmt).scalars():
...     print(user_obj)
SELECT anon_1.id, anon_1.name, anon_1.fullname
FROM (SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
FROM user_account
WHERE user_account.id < ? UNION ALL SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
FROM user_account
WHERE user_account.id = ?) AS anon_1 ORDER BY anon_1.id
[generated in ...] (2, 3)
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=3, name='patrick', fullname='Patrick Star')
```

See also

[Selecting ORM Entities from Unions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-orm-union) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

## Joins

The [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) and [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from) methods
are used to construct SQL JOINs against a SELECT statement.

This section will detail ORM use cases for these methods.  For a general
overview of their use from a Core perspective, see [Explicit FROM clauses and JOINs](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-select-join)
in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial).

The usage of [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) in an ORM context for [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style)
queries is mostly equivalent, minus legacy use cases, to the usage of the
[Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) method in [1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style) queries.

### Simple Relationship Joins

Consider a mapping between two classes `User` and `Address`,
with a relationship `User.addresses` representing a collection
of `Address` objects associated with each `User`.   The most
common usage of [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join)
is to create a JOIN along this
relationship, using the `User.addresses` attribute as an indicator
for how this should occur:

```
>>> stmt = select(User).join(User.addresses)
```

Where above, the call to [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) along
`User.addresses` will result in SQL approximately equivalent to:

```
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id
```

In the above example we refer to `User.addresses` as passed to
[Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) as the “on clause”, that is, it indicates
how the “ON” portion of the JOIN should be constructed.

Tip

Note that using [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) to JOIN from one entity to another
affects the FROM clause of the SELECT statement, but not the columns clause;
the SELECT statement in this example will continue to return rows from only
the `User` entity.  To SELECT
columns / entities from both `User` and `Address` at the same time,
the `Address` entity must also be named in the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) function,
or added to the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct afterwards using the
[Select.add_columns()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.add_columns) method.  See the section
[Selecting Multiple ORM Entities Simultaneously](#orm-queryguide-select-multiple-entities) for examples of both
of these forms.

### Chaining Multiple Joins

To construct a chain of joins, multiple [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) calls may be
used.  The relationship-bound attribute implies both the left and right side of
the join at once.   Consider additional entities `Order` and `Item`, where
the `User.orders` relationship refers to the `Order` entity, and the
`Order.items` relationship refers to the `Item` entity, via an association
table `order_items`.   Two [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) calls will result in
a JOIN first from `User` to `Order`, and a second from `Order` to
`Item`.  However, since `Order.items` is a [many to many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationships-many-to-many)
relationship, it results in two separate JOIN elements, for a total of three
JOIN elements in the resulting SQL:

```
>>> stmt = select(User).join(User.orders).join(Order.items)
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN user_order ON user_account.id = user_order.user_id
JOIN order_items AS order_items_1 ON user_order.id = order_items_1.order_id
JOIN item ON item.id = order_items_1.item_id
```

The order in which each call to the [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) method
is significant only to the degree that the “left” side of what we would like
to join from needs to be present in the list of FROMs before we indicate a
new target.   [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) would not, for example, know how to
join correctly if we were to specify
`select(User).join(Order.items).join(User.orders)`, and would raise an
error.  In correct practice, the [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) method is invoked
in such a way that lines up with how we would want the JOIN clauses in SQL
to be rendered, and each call should represent a clear link from what
precedes it.

All of the elements that we target in the FROM clause remain available
as potential points to continue joining FROM.    We can continue to add
other elements to join FROM the `User` entity above, for example adding
on the `User.addresses` relationship to our chain of joins:

```
>>> stmt = select(User).join(User.orders).join(Order.items).join(User.addresses)
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN user_order ON user_account.id = user_order.user_id
JOIN order_items AS order_items_1 ON user_order.id = order_items_1.order_id
JOIN item ON item.id = order_items_1.item_id
JOIN address ON user_account.id = address.user_id
```

### Joins to a Target Entity

A second form of [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) allows any mapped entity or core
selectable construct as a target.   In this usage, [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join)
will attempt to **infer** the ON clause for the JOIN, using the natural foreign
key relationship between two entities:

```
>>> stmt = select(User).join(Address)
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id
```

In the above calling form, [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) is called upon to infer
the “on clause” automatically.  This calling form will ultimately raise
an error if either there are no [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) setup
between the two mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) constructs, or if there are multiple
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) linkages between them such that the
appropriate constraint to use is ambiguous.

Note

When making use of [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) or [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from)
without indicating an ON clause, ORM
configured [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs are **not taken into account**.
Only the configured [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) relationships between
the entities at the level of the mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects are consulted
when an attempt is made to infer an ON clause for the JOIN.

### Joins to a Target with an ON Clause

The third calling form allows both the target entity as well
as the ON clause to be passed explicitly.    A example that includes
a SQL expression as the ON clause is as follows:

```
>>> stmt = select(User).join(Address, User.id == Address.user_id)
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id
```

The expression-based ON clause may also be a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-bound
attribute, in the same way it’s used in
[Simple Relationship Joins](#orm-queryguide-simple-relationship-join):

```
>>> stmt = select(User).join(Address, User.addresses)
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id
```

The above example seems redundant in that it indicates the target of `Address`
in two different ways; however, the utility of this form becomes apparent
when joining to aliased entities; see the section
[Using Relationship to join between aliased targets](#orm-queryguide-joining-relationships-aliased) for an example.

### Combining Relationship with Custom ON Criteria

The ON clause generated by the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct may
be augmented with additional criteria.  This is useful both for
quick ways to limit the scope of a particular join over a relationship path,
as well as for cases like configuring loader strategies such as
[joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload) and [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload).
The [PropComparator.and_()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.and_)
method accepts a series of SQL expressions positionally that will be joined
to the ON clause of the JOIN via AND.  For example if we wanted to
JOIN from `User` to `Address` but also limit the ON criteria to only certain
email addresses:

```
>>> stmt = select(User.fullname).join(
...     User.addresses.and_(Address.email_address == "[email protected]")
... )
>>> session.execute(stmt).all()
SELECT user_account.fullname
FROM user_account
JOIN address ON user_account.id = address.user_id AND address.email_address = ?
[...] ('[email protected]',)
[('Sandy Cheeks',)]
```

See also

The [PropComparator.and_()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.and_) method also works with loader
strategies such as [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload) and [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload).
See the section [Adding Criteria to loader options](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#loader-option-criteria).

### Using Relationship to join between aliased targets

When constructing joins using [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-bound attributes to indicate
the ON clause, the two-argument syntax illustrated in
[Joins to a Target with an ON Clause](#queryguide-join-onclause) can be expanded to work with the
[aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct, to indicate a SQL alias as the target of a join
while still making use of the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-bound attribute
to  indicate the ON clause, as in the example below, where the `User`
entity is joined twice to two different [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) constructs
against the `Address` entity:

```
>>> address_alias_1 = aliased(Address)
>>> address_alias_2 = aliased(Address)
>>> stmt = (
...     select(User)
...     .join(address_alias_1, User.addresses)
...     .where(address_alias_1.email_address == "[email protected]")
...     .join(address_alias_2, User.addresses)
...     .where(address_alias_2.email_address == "[email protected]")
... )
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN address AS address_1 ON user_account.id = address_1.user_id
JOIN address AS address_2 ON user_account.id = address_2.user_id
WHERE address_1.email_address = :email_address_1
AND address_2.email_address = :email_address_2
```

The same pattern may be expressed more succinctly using the
modifier [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type), which may be applied to the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-bound attribute, passing along the target entity
in order to indicate the target
in one step.   The example below uses [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type)
to produce the same SQL statement as the one just illustrated:

```
>>> print(
...     select(User)
...     .join(User.addresses.of_type(address_alias_1))
...     .where(address_alias_1.email_address == "[email protected]")
...     .join(User.addresses.of_type(address_alias_2))
...     .where(address_alias_2.email_address == "[email protected]")
... )
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN address AS address_1 ON user_account.id = address_1.user_id
JOIN address AS address_2 ON user_account.id = address_2.user_id
WHERE address_1.email_address = :email_address_1
AND address_2.email_address = :email_address_2
```

To make use of a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) to construct a join **from** an
aliased entity, the attribute is available from the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
construct directly:

```
>>> user_alias_1 = aliased(User)
>>> print(select(user_alias_1.name).join(user_alias_1.addresses))
SELECT user_account_1.name
FROM user_account AS user_account_1
JOIN address ON user_account_1.id = address.user_id
```

### Joining to Subqueries

The target of a join may be any “selectable” entity which includes
subqueries.   When using the ORM, it is typical
that these targets are stated in terms of an
[aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct, but this is not strictly required, particularly
if the joined entity is not being returned in the results.  For example, to join from the
`User` entity to the `Address` entity, where the `Address` entity
is represented as a row limited subquery, we first construct a [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery)
object using [Select.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.subquery), which may then be used as the
target of the [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) method:

```
>>> subq = select(Address).where(Address.email_address == "[email protected]").subquery()
>>> stmt = select(User).join(subq, User.id == subq.c.user_id)
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN (SELECT address.id AS id,
address.user_id AS user_id, address.email_address AS email_address
FROM address
WHERE address.email_address = :email_address_1) AS anon_1
ON user_account.id = anon_1.user_id
```

The above SELECT statement when invoked via [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) will
return rows that contain `User` entities, but not `Address` entities. In
order to include `Address` entities to the set of entities that would be
returned in result sets, we construct an [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) object against
the `Address` entity and [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) object. We also may wish to apply
a name to the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct, such as `"address"` used below,
so that we can refer to it by name in the result row:

```
>>> address_subq = aliased(Address, subq, name="address")
>>> stmt = select(User, address_subq).join(address_subq)
>>> for row in session.execute(stmt):
...     print(f"{row.User} {row.address}")
SELECT user_account.id, user_account.name, user_account.fullname,
anon_1.id AS id_1, anon_1.user_id, anon_1.email_address
FROM user_account
JOIN (SELECT address.id AS id,
address.user_id AS user_id, address.email_address AS email_address
FROM address
WHERE address.email_address = ?) AS anon_1 ON user_account.id = anon_1.user_id
[...] ('[email protected]',)
User(id=3, name='patrick', fullname='Patrick Star') Address(id=4, email_address='[email protected]')
```

### Joining to Subqueries along Relationship paths

The subquery form illustrated in the previous section
may be expressed with more specificity using a
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-bound attribute using one of the forms indicated at
[Using Relationship to join between aliased targets](#orm-queryguide-joining-relationships-aliased). For example, to create the
same join while ensuring the join is along that of a particular
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), we may use the
[PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) method, passing the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
construct containing the [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) object that’s the target
of the join:

```
>>> address_subq = aliased(Address, subq, name="address")
>>> stmt = select(User, address_subq).join(User.addresses.of_type(address_subq))
>>> for row in session.execute(stmt):
...     print(f"{row.User} {row.address}")
SELECT user_account.id, user_account.name, user_account.fullname,
anon_1.id AS id_1, anon_1.user_id, anon_1.email_address
FROM user_account
JOIN (SELECT address.id AS id,
address.user_id AS user_id, address.email_address AS email_address
FROM address
WHERE address.email_address = ?) AS anon_1 ON user_account.id = anon_1.user_id
[...] ('[email protected]',)
User(id=3, name='patrick', fullname='Patrick Star') Address(id=4, email_address='[email protected]')
```

### Subqueries that Refer to Multiple Entities

A subquery that contains columns spanning more than one ORM entity may be
applied to more than one [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct at once, and
used in the same [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct in terms of each entity separately.
The rendered SQL will continue to treat all such [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
constructs as the same subquery, however from the ORM / Python perspective
the different return values and object attributes can be referenced
by using the appropriate [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct.

Given for example a subquery that refers to both `User` and `Address`:

```
>>> user_address_subq = (
...     select(User.id, User.name, User.fullname, Address.id, Address.email_address)
...     .join_from(User, Address)
...     .where(Address.email_address.in_(["[email protected]", "[email protected]"]))
...     .subquery()
... )
```

We can create [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) constructs against both `User` and
`Address` that each refer to the same object:

```
>>> user_alias = aliased(User, user_address_subq, name="user")
>>> address_alias = aliased(Address, user_address_subq, name="address")
```

A [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct selecting from both entities will render the
subquery once, but in a result-row context can return objects of both
`User` and `Address` classes at the same time:

```
>>> stmt = select(user_alias, address_alias).where(user_alias.name == "sandy")
>>> for row in session.execute(stmt):
...     print(f"{row.user} {row.address}")
SELECT anon_1.id, anon_1.name, anon_1.fullname, anon_1.id_1, anon_1.email_address
FROM (SELECT user_account.id AS id, user_account.name AS name,
user_account.fullname AS fullname, address.id AS id_1,
address.email_address AS email_address
FROM user_account JOIN address ON user_account.id = address.user_id
WHERE address.email_address IN (?, ?)) AS anon_1
WHERE anon_1.name = ?
[...] ('[email protected]', '[email protected]', 'sandy')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=3, email_address='[email protected]')
```

### Setting the leftmost FROM clause in a join

In cases where the left side of the current state of
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) is not in line with what we want to join from,
the [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from) method may be used:

```
>>> stmt = select(Address).join_from(User, User.addresses).where(User.name == "sandy")
>>> print(stmt)
SELECT address.id, address.user_id, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
WHERE user_account.name = :name_1
```

The [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from) method accepts two or three arguments, either
in the form `(<join from>, <onclause>)`, or `(<join from>, <join to>,
[<onclause>])`:

```
>>> stmt = select(Address).join_from(User, Address).where(User.name == "sandy")
>>> print(stmt)
SELECT address.id, address.user_id, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
WHERE user_account.name = :name_1
```

To set up the initial FROM clause for a SELECT such that [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join)
can be used subsequent, the [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) method may also
be used:

```
>>> stmt = select(Address).select_from(User).join(Address).where(User.name == "sandy")
>>> print(stmt)
SELECT address.id, address.user_id, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
WHERE user_account.name = :name_1
```

Tip

The [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) method does not actually have the
final say on the order of tables in the FROM clause.    If the statement
also refers to a [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) construct that refers to existing
tables in a different order, the [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) construct takes
precedence.    When we use methods like [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join)
and [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from), these methods are ultimately creating
such a [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) object.   Therefore we can see the contents
of [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) being overridden in a case like this:

```
>>> stmt = select(Address).select_from(User).join(Address.user).where(User.name == "sandy")
>>> print(stmt)
SELECT address.id, address.user_id, address.email_address
FROM address JOIN user_account ON user_account.id = address.user_id
WHERE user_account.name = :name_1
```

Where above, we see that the FROM clause is `address JOIN user_account`,
even though we stated `select_from(User)` first. Because of the
`.join(Address.user)` method call, the statement is ultimately equivalent
to the following:

```
>>> from sqlalchemy.sql import join
>>>
>>> user_table = User.__table__
>>> address_table = Address.__table__
>>>
>>> j = address_table.join(user_table, user_table.c.id == address_table.c.user_id)
>>> stmt = (
...     select(address_table)
...     .select_from(user_table)
...     .select_from(j)
...     .where(user_table.c.name == "sandy")
... )
>>> print(stmt)
SELECT address.id, address.user_id, address.email_address
FROM address JOIN user_account ON user_account.id = address.user_id
WHERE user_account.name = :name_1
```

The [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) construct above is added as another entry in the
[Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) list which supersedes the previous entry.

## Relationship WHERE Operators

Besides the use of [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs within the
[Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) and [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from) methods,
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) also plays a role in helping to construct
SQL expressions that are typically for use in the WHERE clause, using
the [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where) method.

### EXISTS forms: has() / any()

The [Exists](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Exists) construct was first introduced in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial) in the section [EXISTS subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-exists).  This object
is used to render the SQL EXISTS keyword in conjunction with a
scalar subquery.   The [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct provides for some
helper methods that may be used to generate some common EXISTS styles
of queries in terms of the relationship.

For a one-to-many relationship such as `User.addresses`, an EXISTS against
the `address` table that correlates back to the `user_account` table
can be produced using [PropComparator.any()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.any).  This method accepts
an optional WHERE criteria to limit the rows matched by the subquery:

```
>>> stmt = select(User.fullname).where(
...     User.addresses.any(Address.email_address == "[email protected]")
... )
>>> session.execute(stmt).all()
SELECT user_account.fullname
FROM user_account
WHERE EXISTS (SELECT 1
FROM address
WHERE user_account.id = address.user_id AND address.email_address = ?)
[...] ('[email protected]',)
[('Sandy Cheeks',)]
```

As EXISTS tends to be more efficient for negative lookups, a common query
is to locate entities where there are no related entities present.  This
is succinct using a phrase such as `~User.addresses.any()`, to select
for `User` entities that have no related `Address` rows:

```
>>> stmt = select(User.fullname).where(~User.addresses.any())
>>> session.execute(stmt).all()
SELECT user_account.fullname
FROM user_account
WHERE NOT (EXISTS (SELECT 1
FROM address
WHERE user_account.id = address.user_id))
[...] ()
[('Eugene H. Krabs',)]
```

The [PropComparator.has()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.has) method works in mostly the same way as
[PropComparator.any()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.any), except that it’s used for many-to-one
relationships, such as if we wanted to locate all `Address` objects
which belonged to “sandy”:

```
>>> stmt = select(Address.email_address).where(Address.user.has(User.name == "sandy"))
>>> session.execute(stmt).all()
SELECT address.email_address
FROM address
WHERE EXISTS (SELECT 1
FROM user_account
WHERE user_account.id = address.user_id AND user_account.name = ?)
[...] ('sandy',)
[('[email protected]',), ('[email protected]',)]
```

### Relationship Instance Comparison Operators

The [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-bound attribute also offers a few SQL construction
implementations that are geared towards filtering a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-bound
attribute in terms of a specific instance of a related object, which can unpack
the appropriate attribute values from a given [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent) (or less
commonly a [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached)) object instance and construct WHERE criteria
in terms of the target [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

- **many to one equals comparison** - a specific object instance can be
  compared to many-to-one relationship, to select rows where the
  foreign key of the target entity matches the primary key value of the
  object given:
  ```
  >>> user_obj = session.get(User, 1)
  SELECT ...
  >>> print(select(Address).where(Address.user == user_obj))
  SELECT address.id, address.user_id, address.email_address
  FROM address
  WHERE :param_1 = address.user_id
  ```
- **many to one not equals comparison** - the not equals operator may also
  be used:
  ```
  >>> print(select(Address).where(Address.user != user_obj))
  SELECT address.id, address.user_id, address.email_address
  FROM address
  WHERE address.user_id != :user_id_1 OR address.user_id IS NULL
  ```
- **object is contained in a one-to-many collection** - this is essentially
  the one-to-many version of the “equals” comparison, select rows where the
  primary key equals the value of the foreign key in a related object:
  ```
  >>> address_obj = session.get(Address, 1)
  SELECT ...
  >>> print(select(User).where(User.addresses.contains(address_obj)))
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account
  WHERE user_account.id = :param_1
  ```
- **An object has a particular parent from a one-to-many perspective** - the
  [with_parent()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_parent) function produces a comparison that returns rows
  which are referenced by a given parent, this is essentially the
  same as using the `==` operator with the many-to-one side:
  ```
  >>> from sqlalchemy.orm import with_parent
  >>> print(select(Address).where(with_parent(user_obj, User.addresses)))
  SELECT address.id, address.user_id, address.email_address
  FROM address
  WHERE :param_1 = address.user_id
  ```

ORM Querying Guide

Next Query Guide Section: [Writing SELECT statements for Inheritance Mappings](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html)
