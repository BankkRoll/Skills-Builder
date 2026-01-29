# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html)   |   Next: [Using UPDATE and DELETE Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html)

# Using SELECT Statements

For both Core and ORM, the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) function generates a
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct which is used for all SELECT queries.
Passed to methods like [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) in Core and
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) in ORM, a SELECT statement is emitted in the
current transaction and the result rows available via the returned
[Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object.

**ORM Readers** - the content here applies equally well to both Core and ORM
use and basic ORM variant use cases are mentioned here.  However there are
a lot more ORM-specific features available as well; these are documented
at [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).

## The select() SQL Expression Construct

The [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct builds up a statement in the same way
as that of [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert), using a [generative](https://docs.sqlalchemy.org/en/20/glossary.html#term-generative) approach where
each method builds more state onto the object.  Like the other SQL constructs,
it can be stringified in place:

```
>>> from sqlalchemy import select
>>> stmt = select(user_table).where(user_table.c.name == "spongebob")
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1
```

Also in the same manner as all other statement-level SQL constructs, to
actually run the statement we pass it to an execution method.
Since a SELECT statement returns
rows we can always iterate the result object to get [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
objects back:

```
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(row)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(1, 'spongebob', 'Spongebob Squarepants')
ROLLBACK
```

When using the ORM, particularly with a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct that’s
composed against ORM entities, we will want to execute it using the
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method on the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session); using
this approach, we continue to get [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects from the
result, however these rows are now capable of including
complete entities, such as instances of the `User` class, as individual
elements within each row:

```
>>> stmt = select(User).where(User.name == "spongebob")
>>> with Session(engine) as session:
...     for row in session.execute(stmt):
...         print(row)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)
ROLLBACK
```

select() from a Table vs. ORM class

While the SQL generated in these examples looks the same whether we invoke
`select(user_table)` or `select(User)`, in the more general case
they do not necessarily render the same thing, as an ORM-mapped class
may be mapped to other kinds of “selectables” besides tables.  The
`select()` that’s against an ORM entity also indicates that ORM-mapped
instances should be returned in a result, which is not the case when
SELECTing from a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.

The following sections will discuss the SELECT construct in more detail.

## Setting the COLUMNS and FROM clause

The [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) function accepts positional elements representing any
number of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) and/or [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) expressions, as
well as a wide range of compatible objects, which are resolved into a list of SQL
expressions to be SELECTed from that will be returned as columns in the result
set.  These elements also serve in simpler cases to create the FROM clause,
which is inferred from the columns and table-like expressions passed:

```
>>> print(select(user_table))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
```

To SELECT from individual columns using a Core approach,
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects are accessed from the [Table.c](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.c)
accessor and can be sent directly; the FROM clause will be inferred as the set
of all [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and other [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) objects that
are represented by those columns:

```
>>> print(select(user_table.c.name, user_table.c.fullname))
SELECT user_account.name, user_account.fullname
FROM user_account
```

Alternatively, when using the [FromClause.c](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.c) collection of any
[FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), multiple columns may be specified
for a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) by using a tuple of string names:

```
>>> print(select(user_table.c["name", "fullname"]))
SELECT user_account.name, user_account.fullname
FROM user_account
```

Added in version 2.0: Added tuple-accessor capability to the
[FromClause.c](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.c) collection

### Selecting ORM Entities and Columns

ORM entities, such our `User` class as well as the column-mapped
attributes upon it such as `User.name`, also participate in the SQL Expression
Language system representing tables and columns.    Below illustrates an
example of SELECTing from the `User` entity, which ultimately renders
in the same way as if we had used `user_table` directly:

```
>>> print(select(User))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
```

When executing a statement like the above using the ORM [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute)
method, there is an important difference when we select from a full entity
such as `User`, as opposed to `user_table`, which is that the **entity
itself is returned as a single element within each row**.  That is, when we fetch rows from
the above statement, as there is only the `User` entity in the list of
things to fetch, we get back [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects that have only one element, which contain
instances of the `User` class:

```
>>> row = session.execute(select(User)).first()
BEGIN...
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
[...] ()
>>> row
(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)
```

The above [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) has just one element, representing the `User` entity:

```
>>> row[0]
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
```

A highly recommended convenience method of achieving the same result as above
is to use the [Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars) method to execute the statement
directly; this method will return a [ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult) object
that delivers the first “column” of each row at once, in this case,
instances of the `User` class:

```
>>> user = session.scalars(select(User)).first()
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
[...] ()
>>> user
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
```

Alternatively, we can select individual columns of an ORM entity as distinct
elements within result rows, by using the class-bound attributes; when these
are passed to a construct such as [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select), they are resolved into
the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or other SQL expression represented by each
attribute:

```
>>> print(select(User.name, User.fullname))
SELECT user_account.name, user_account.fullname
FROM user_account
```

When we invoke *this* statement using [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), we now
receive rows that have individual elements per value, each corresponding
to a separate column or other SQL expression:

```
>>> row = session.execute(select(User.name, User.fullname)).first()
SELECT user_account.name, user_account.fullname
FROM user_account
[...] ()
>>> row
('spongebob', 'Spongebob Squarepants')
```

The approaches can also be mixed, as below where we SELECT the `name`
attribute of the `User` entity as the first element of the row, and combine
it with full `Address` entities in the second element:

```
>>> session.execute(
...     select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
... ).all()
SELECT user_account.name, address.id, address.email_address, address.user_id
FROM user_account, address
WHERE user_account.id = address.user_id ORDER BY address.id
[...] ()
[('spongebob', Address(id=1, email_address='[email protected]')),
('sandy', Address(id=2, email_address='[email protected]')),
('sandy', Address(id=3, email_address='[email protected]'))]
```

Approaches towards selecting ORM entities and columns as well as common methods
for converting rows are discussed further at [Selecting ORM Entities and Attributes](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-select-columns).

See also

[Selecting ORM Entities and Attributes](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-select-columns) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

### Selecting from Labeled SQL Expressions

The [ColumnElement.label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label) method as well as the same-named method
available on ORM attributes provides a SQL label of a column or expression,
allowing it to have a specific name in a result set.  This can be helpful
when referring to arbitrary SQL expressions in a result row by name:

```
>>> from sqlalchemy import func, cast
>>> stmt = select(
...     ("Username: " + user_table.c.name).label("username"),
... ).order_by(user_table.c.name)
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(f"{row.username}")
BEGIN (implicit)
SELECT ? || user_account.name AS username
FROM user_account ORDER BY user_account.name
[...] ('Username: ',)
Username: patrick
Username: sandy
Username: spongebob
ROLLBACK
```

See also

[Ordering or Grouping by a Label](#tutorial-order-by-label) - the label names we create may also be
referenced in the ORDER BY or GROUP BY clause of the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select).

### Selecting with Textual Column Expressions

When we construct a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object using the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
function, we are normally passing to it a series of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that were defined using
[table metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata), or when using the ORM we may be
sending ORM-mapped attributes that represent table columns.   However,
sometimes there is also the need to manufacture arbitrary SQL blocks inside
of statements, such as constant string expressions, or just some arbitrary
SQL that’s quicker to write literally.

The [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct introduced at
[Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-working-with-transactions) can in fact be embedded into a
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct directly, such as below where we manufacture
a hardcoded string literal `'some phrase'` and embed it within the
SELECT statement:

```
>>> from sqlalchemy import text
>>> stmt = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)
>>> with engine.connect() as conn:
...     print(conn.execute(stmt).all())
BEGIN (implicit)
SELECT 'some phrase', user_account.name
FROM user_account ORDER BY user_account.name
[generated in ...] ()
[('some phrase', 'patrick'), ('some phrase', 'sandy'), ('some phrase', 'spongebob')]
ROLLBACK
```

While the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct can be used in most places to inject
literal SQL phrases, more often than not we are actually dealing with textual
units that each represent an individual
column expression.  In this common case we can get more functionality out of
our textual fragment using the [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column)
construct instead.  This object is similar to [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) except that
instead of representing arbitrary SQL of any form,
it explicitly represents a single “column” and can then be labeled and referred
towards in subqueries and other expressions:

```
>>> from sqlalchemy import literal_column
>>> stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(
...     user_table.c.name
... )
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(f"{row.p}, {row.name}")
BEGIN (implicit)
SELECT 'some phrase' AS p, user_account.name
FROM user_account ORDER BY user_account.name
[generated in ...] ()
some phrase, patrick
some phrase, sandy
some phrase, spongebob
ROLLBACK
```

Note that in both cases, when using [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) or
[literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column), we are writing a syntactical SQL expression, and
not a literal value. We therefore have to include whatever quoting or syntaxes
are necessary for the SQL we want to see rendered.

## The WHERE clause

SQLAlchemy allows us to compose SQL expressions, such as `name = 'squidward'`
or `user_id > 10`, by making use of standard Python operators in
conjunction with
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) and similar objects.   For boolean expressions, most
Python operators such as `==`, `!=`, `<`, `>=` etc. generate new
SQL Expression objects, rather than plain boolean `True`/`False` values:

```
>>> print(user_table.c.name == "squidward")
user_account.name = :name_1

>>> print(address_table.c.user_id > 10)
address.user_id > :user_id_1
```

We can use expressions like these to generate the WHERE clause by passing
the resulting objects to the [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where) method:

```
>>> print(select(user_table).where(user_table.c.name == "squidward"))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1
```

To produce multiple expressions joined by AND, the [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where)
method may be invoked any number of times:

```
>>> print(
...     select(address_table.c.email_address)
...     .where(user_table.c.name == "squidward")
...     .where(address_table.c.user_id == user_table.c.id)
... )
SELECT address.email_address
FROM address, user_account
WHERE user_account.name = :name_1 AND address.user_id = user_account.id
```

A single call to [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where) also accepts multiple expressions
with the same effect:

```
>>> print(
...     select(address_table.c.email_address).where(
...         user_table.c.name == "squidward",
...         address_table.c.user_id == user_table.c.id,
...     )
... )
SELECT address.email_address
FROM address, user_account
WHERE user_account.name = :name_1 AND address.user_id = user_account.id
```

“AND” and “OR” conjunctions are both available directly using the
[and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) and [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) functions, illustrated below in terms
of ORM entities:

```
>>> from sqlalchemy import and_, or_
>>> print(
...     select(Address.email_address).where(
...         and_(
...             or_(User.name == "squidward", User.name == "sandy"),
...             Address.user_id == User.id,
...         )
...     )
... )
SELECT address.email_address
FROM address, user_account
WHERE (user_account.name = :name_1 OR user_account.name = :name_2)
AND address.user_id = user_account.id
```

Tip

The rendering of parentheses is based on operator precedence rules (there’s no
way to detect parentheses from a Python expression at runtime), so if we combine
AND and OR in a way that matches the natural precedence of AND, the rendered
expression might not have similar looking parentheses as our Python code:

```
>>> print(
...     select(Address.email_address).where(
...         or_(
...             User.name == "squidward",
...             and_(Address.user_id == User.id, User.name == "sandy"),
...         )
...     )
... )
SELECT address.email_address
FROM address, user_account
WHERE user_account.name = :name_1 OR address.user_id = user_account.id AND user_account.name = :name_2
```

More background on parenthesization is in the [Parentheses and Grouping](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-parentheses) in the Operator Reference.

For simple “equality” comparisons against a single entity, there’s also a
popular method known as [Select.filter_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.filter_by) which accepts keyword
arguments that match to column keys or ORM attribute names.  It will filter
against the leftmost FROM clause or the last entity joined:

```
>>> print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1 AND user_account.fullname = :fullname_1
```

See also

[Operator Reference](https://docs.sqlalchemy.org/en/20/core/operators.html) - descriptions of most SQL operator functions in SQLAlchemy

## Explicit FROM clauses and JOINs

As mentioned previously, the FROM clause is usually **inferred**
based on the expressions that we are setting in the columns
clause as well as other elements of the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select).

If we set a single column from a particular [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
in the COLUMNS clause, it puts that [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) in the FROM
clause as well:

```
>>> print(select(user_table.c.name))
SELECT user_account.name
FROM user_account
```

If we were to put columns from two tables, then we get a comma-separated FROM
clause:

```
>>> print(select(user_table.c.name, address_table.c.email_address))
SELECT user_account.name, address.email_address
FROM user_account, address
```

In order to JOIN these two tables together, we typically use one of two methods
on [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select).  The first is the [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from)
method, which allows us to indicate the left and right side of the JOIN
explicitly:

```
>>> print(
...     select(user_table.c.name, address_table.c.email_address).join_from(
...         user_table, address_table
...     )
... )
SELECT user_account.name, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
```

The other is the [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) method, which indicates only the
right side of the JOIN, the left hand-side is inferred:

```
>>> print(select(user_table.c.name, address_table.c.email_address).join(address_table))
SELECT user_account.name, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
```

The ON Clause is inferred

When using [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from) or [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join), we may
observe that the ON clause of the join is also inferred for us in simple
foreign key cases. More on that in the next section.

We also have the option to add elements to the FROM clause explicitly, if it is not
inferred the way we want from the columns clause.  We use the
[Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) method to achieve this, as below
where we establish `user_table` as the first element in the FROM
clause and [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) to establish `address_table` as
the second:

```
>>> print(select(address_table.c.email_address).select_from(user_table).join(address_table))
SELECT address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
```

Another example where we might want to use [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from)
is if our columns clause doesn’t have enough information to provide for a
FROM clause.  For example, to SELECT from the common SQL expression
`count(*)`, we use a SQLAlchemy element known as [sqlalchemy.sql.expression.func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) to
produce the SQL `count()` function:

```
>>> from sqlalchemy import func
>>> print(select(func.count("*")).select_from(user_table))
SELECT count(:count_2) AS count_1
FROM user_account
```

See also

[Setting the leftmost FROM clause in a join](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-select-from) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html) -
contains additional examples and notes
regarding the interaction of [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) and
[Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join).

### Setting the ON Clause

The previous examples of JOIN illustrated that the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct
can join between two tables and produce the ON clause automatically.  This
occurs in those examples because the `user_table` and `address_table` `Table` objects include a single [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
definition which is used to form this ON clause.

If the left and right targets of the join do not have such a constraint, or
there are multiple constraints in place, we need to specify the ON clause
directly.   Both [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) and [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from)
accept an additional argument for the ON clause, which is stated using the
same SQL Expression mechanics as we saw about in [The WHERE clause](#tutorial-select-where-clause):

```
>>> print(
...     select(address_table.c.email_address)
...     .select_from(user_table)
...     .join(address_table, user_table.c.id == address_table.c.user_id)
... )
SELECT address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
```

**ORM Tip** - there’s another way to generate the ON clause when using
ORM entities that make use of the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct,
like the mapping set up in the previous section at
[Declaring Mapped Classes](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-declaring-mapped-classes).
This is a whole subject onto itself, which is introduced at length
at [Using Relationships to Join](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-joining-relationships).

### OUTER and FULL join

Both the [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) and [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from) methods
accept keyword arguments [Select.join.isouter](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join.params.isouter) and
[Select.join.full](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join.params.full) which will render LEFT OUTER JOIN
and FULL OUTER JOIN, respectively:

```
>>> print(select(user_table).join(address_table, isouter=True))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account LEFT OUTER JOIN address ON user_account.id = address.user_id
>>> print(select(user_table).join(address_table, full=True))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account FULL OUTER JOIN address ON user_account.id = address.user_id
```

There is also a method [Select.outerjoin()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.outerjoin) that is equivalent to
using `.join(..., isouter=True)`.

Tip

SQL also has a “RIGHT OUTER JOIN”.  SQLAlchemy doesn’t render this directly;
instead, reverse the order of the tables and use “LEFT OUTER JOIN”.

## ORDER BY, GROUP BY, HAVING

The SELECT SQL statement includes a clause called ORDER BY which is used to
return the selected rows within a given ordering.

The GROUP BY clause is constructed similarly to the ORDER BY clause, and has
the purpose of sub-dividing the selected rows into specific groups upon which
aggregate functions may be invoked. The HAVING clause is usually used with
GROUP BY and is of a similar form to the WHERE clause, except that it’s applied
to the aggregated functions used within groups.

### ORDER BY

The ORDER BY clause is constructed in terms
of SQL Expression constructs typically based on [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or
similar objects.  The [Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by) method accepts one or
more of these expressions positionally:

```
>>> print(select(user_table).order_by(user_table.c.name))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.name
```

Ascending / descending is available from the [ColumnElement.asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.asc)
and [ColumnElement.desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.desc) modifiers, which are present
from ORM-bound attributes as well:

```
>>> print(select(User).order_by(User.fullname.desc()))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.fullname DESC
```

The above statement will yield rows that are sorted by the
`user_account.fullname` column in descending order.

### Aggregate functions with GROUP BY / HAVING

In SQL, aggregate functions allow column expressions across multiple rows
to be aggregated together to produce a single result.  Examples include
counting, computing averages, as well as locating the maximum or minimum
value in a set of values.

SQLAlchemy provides for SQL functions in an open-ended way using a namespace
known as [func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func).  This is a special constructor object which
will create new instances of [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function) when given the name
of a particular SQL function, which can have any name, as well as zero or
more arguments to pass to the function, which are, like in all other cases,
SQL Expression constructs.   For example, to
render the SQL COUNT() function against the `user_account.id` column,
we call upon the `count()` name:

```
>>> from sqlalchemy import func
>>> count_fn = func.count(user_table.c.id)
>>> print(count_fn)
count(user_account.id)
```

SQL functions are described in more detail later in this tutorial at
[Working with SQL Functions](#tutorial-functions).

When using aggregate functions in SQL, the GROUP BY clause is essential in that
it allows rows to be partitioned into groups where aggregate functions will
be applied to each group individually.  When requesting non-aggregated columns
in the COLUMNS clause of a SELECT statement, SQL requires that these columns
all be subject to a GROUP BY clause, either directly or indirectly based on
a primary key association.    The HAVING clause is then used in a similar
manner as the WHERE clause, except that it filters out rows based on aggregated
values rather than direct row contents.

SQLAlchemy provides for these two clauses using the [Select.group_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.group_by)
and [Select.having()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.having) methods.   Below we illustrate selecting
user name fields as well as count of addresses, for those users that have more
than one address:

```
>>> with engine.connect() as conn:
...     result = conn.execute(
...         select(User.name, func.count(Address.id).label("count"))
...         .join(Address)
...         .group_by(User.name)
...         .having(func.count(Address.id) > 1)
...     )
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name, count(address.id) AS count
FROM user_account JOIN address ON user_account.id = address.user_id GROUP BY user_account.name
HAVING count(address.id) > ?
[...] (1,)
[('sandy', 2)]
ROLLBACK
```

### Ordering or Grouping by a Label

An important technique, in particular on some database backends, is the ability
to ORDER BY or GROUP BY an expression that is already stated in the columns
clause, without re-stating the expression in the ORDER BY or GROUP BY clause
and instead using the column name or labeled name from the COLUMNS clause.
This form is available by passing the string text of the name to the
[Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by) or [Select.group_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.group_by) method.  The text
passed is **not rendered directly**; instead, the name given to an expression
in the columns clause and rendered as that expression name in context, raising an
error if no match is found.   The unary modifiers
[asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.asc) and [desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.desc) may also be used in this form:

```
>>> from sqlalchemy import func, desc
>>> stmt = (
...     select(Address.user_id, func.count(Address.id).label("num_addresses"))
...     .group_by("user_id")
...     .order_by("user_id", desc("num_addresses"))
... )
>>> print(stmt)
SELECT address.user_id, count(address.id) AS num_addresses
FROM address GROUP BY address.user_id ORDER BY address.user_id, num_addresses DESC
```

## Using Aliases

Now that we are selecting from multiple tables and using joins, we quickly
run into the case where we need to refer to the same table multiple times
in the FROM clause of a statement.  We accomplish this using SQL **aliases**,
which are a syntax that supplies an alternative name to a table or subquery
from which it can be referenced in the statement.

In the SQLAlchemy Expression Language, these “names” are instead represented by
[FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) objects known as the [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) construct,
which is constructed in Core using the [FromClause.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.alias)
method. An [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) construct is just like a `Table`
construct in that it also has a namespace of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
objects within the `Alias.c` collection.  The SELECT statement
below for example returns all unique pairs of user names:

```
>>> user_alias_1 = user_table.alias()
>>> user_alias_2 = user_table.alias()
>>> print(
...     select(user_alias_1.c.name, user_alias_2.c.name).join_from(
...         user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id
...     )
... )
SELECT user_account_1.name, user_account_2.name AS name_1
FROM user_account AS user_account_1
JOIN user_account AS user_account_2 ON user_account_1.id > user_account_2.id
```

### ORM Entity Aliases

The ORM equivalent of the [FromClause.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.alias) method is the
ORM [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) function, which may be applied to an entity
such as `User` and `Address`.  This produces a [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) object
internally that’s against the original mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object,
while maintaining ORM functionality.  The SELECT below selects from the
`User` entity all objects that include two particular email addresses:

```
>>> from sqlalchemy.orm import aliased
>>> address_alias_1 = aliased(Address)
>>> address_alias_2 = aliased(Address)
>>> print(
...     select(User)
...     .join_from(User, address_alias_1)
...     .where(address_alias_1.email_address == "[email protected]")
...     .join_from(User, address_alias_2)
...     .where(address_alias_2.email_address == "[email protected]")
... )
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN address AS address_1 ON user_account.id = address_1.user_id
JOIN address AS address_2 ON user_account.id = address_2.user_id
WHERE address_1.email_address = :email_address_1
AND address_2.email_address = :email_address_2
```

Tip

As mentioned in [Setting the ON Clause](#tutorial-select-join-onclause), the ORM provides
for another way to join using the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct.
The above example using aliases is demonstrated using [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
at [Using Relationship to join between aliased targets](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#tutorial-joining-relationships-aliased).

## Subqueries and CTEs

A subquery in SQL is a SELECT statement that is rendered within parenthesis and
placed within the context of an enclosing statement, typically a SELECT
statement but not necessarily.

This section will cover a so-called “non-scalar” subquery, which is typically
placed in the FROM clause of an enclosing SELECT.   We will also cover the
Common Table Expression or CTE, which is used in a similar way as a subquery,
but includes additional features.

SQLAlchemy uses the [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) object to represent a subquery and
the [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) to represent a CTE, usually obtained from the
[Select.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.subquery) and [Select.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.cte) methods, respectively.
Either object can be used as a FROM element inside of a larger
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct.

We can construct a [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) that will select an aggregate count
of rows from the `address` table (aggregate functions and GROUP BY were
introduced previously at [Aggregate functions with GROUP BY / HAVING](#tutorial-group-by-w-aggregates)):

```
>>> subq = (
...     select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
...     .group_by(address_table.c.user_id)
...     .subquery()
... )
```

Stringifying the subquery by itself without it being embedded inside of another
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) or other statement produces the plain SELECT statement
without any enclosing parenthesis:

```
>>> print(subq)
SELECT count(address.id) AS count, address.user_id
FROM address GROUP BY address.user_id
```

The [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) object behaves like any other FROM object such
as a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), notably that it includes a `Subquery.c`
namespace of the columns which it selects.  We can use this namespace to
refer to both the `user_id` column as well as our custom labeled
`count` expression:

```
>>> print(select(subq.c.user_id, subq.c.count))
SELECT anon_1.user_id, anon_1.count
FROM (SELECT count(address.id) AS count, address.user_id AS user_id
FROM address GROUP BY address.user_id) AS anon_1
```

With a selection of rows contained within the `subq` object, we can apply
the object to a larger [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) that will join the data to
the `user_account` table:

```
>>> stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
...     user_table, subq
... )

>>> print(stmt)
SELECT user_account.name, user_account.fullname, anon_1.count
FROM user_account JOIN (SELECT count(address.id) AS count, address.user_id AS user_id
FROM address GROUP BY address.user_id) AS anon_1 ON user_account.id = anon_1.user_id
```

In order to join from `user_account` to `address`, we made use of the
[Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from) method.   As has been illustrated previously, the
ON clause of this join was again **inferred** based on foreign key constraints.
Even though a SQL subquery does not itself have any constraints, SQLAlchemy can
act upon constraints represented on the columns by determining that the
`subq.c.user_id` column is **derived** from the `address_table.c.user_id`
column, which does express a foreign key relationship back to the
`user_table.c.id` column which is then used to generate the ON clause.

### Common Table Expressions (CTEs)

Usage of the [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) construct in SQLAlchemy is virtually
the same as how the [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) construct is used.  By changing
the invocation of the [Select.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.subquery) method to use
[Select.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.cte) instead, we can use the resulting object as a FROM
element in the same way, but the SQL rendered is the very different common
table expression syntax:

```
>>> subq = (
...     select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
...     .group_by(address_table.c.user_id)
...     .cte()
... )

>>> stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
...     user_table, subq
... )

>>> print(stmt)
WITH anon_1 AS
(SELECT count(address.id) AS count, address.user_id AS user_id
FROM address GROUP BY address.user_id)
 SELECT user_account.name, user_account.fullname, anon_1.count
FROM user_account JOIN anon_1 ON user_account.id = anon_1.user_id
```

The [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) construct also features the ability to be used
in a “recursive” style, and may in more elaborate cases be composed from the
RETURNING clause of an INSERT, UPDATE or DELETE statement.  The docstring
for [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) includes details on these additional patterns.

In both cases, the subquery and CTE were named at the SQL level using an
“anonymous” name.  In the Python code, we don’t need to provide these names
at all.  The object identity of the [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) or [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE)
instances serves as the syntactical identity of the object when rendered.
A name that will be rendered in the SQL can be provided by passing it as the
first argument of the [Select.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.subquery) or [Select.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.cte) methods.

See also

[Select.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.subquery) - further detail on subqueries

[Select.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.cte) - examples for CTE including how to use
RECURSIVE as well as DML-oriented CTEs

### ORM Entity Subqueries/CTEs

In the ORM, the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct may be used to associate an ORM
entity, such as our `User` or `Address` class, with any [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
concept that represents a source of rows.  The preceding section
[ORM Entity Aliases](#tutorial-orm-entity-aliases) illustrates using [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
to associate the mapped class with an [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) of its
mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).   Here we illustrate [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) doing the same
thing against both a [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) as well as a [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE)
generated against a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct, that ultimately derives
from that same mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

Below is an example of applying [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) to the [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery)
construct, so that ORM entities can be extracted from its rows.  The result
shows a series of `User` and `Address` objects, where the data for
each `Address` object ultimately came from a subquery against the
`address` table rather than that table directly:

```
>>> subq = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
>>> address_subq = aliased(Address, subq)
>>> stmt = (
...     select(User, address_subq)
...     .join_from(User, address_subq)
...     .order_by(User.id, address_subq.id)
... )
>>> with Session(engine) as session:
...     for user, address in session.execute(stmt):
...         print(f"{user} {address}")
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname,
anon_1.id AS id_1, anon_1.email_address, anon_1.user_id
FROM user_account JOIN
(SELECT address.id AS id, address.email_address AS email_address, address.user_id AS user_id
FROM address
WHERE address.email_address NOT LIKE ?) AS anon_1 ON user_account.id = anon_1.user_id
ORDER BY user_account.id, anon_1.id
[...] ('%@aol.com',)
User(id=1, name='spongebob', fullname='Spongebob Squarepants') Address(id=1, email_address='[email protected]')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=2, email_address='[email protected]')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=3, email_address='[email protected]')
ROLLBACK
```

Another example follows, which is exactly the same except it makes use of the
[CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) construct instead:

```
>>> cte_obj = select(Address).where(~Address.email_address.like("%@aol.com")).cte()
>>> address_cte = aliased(Address, cte_obj)
>>> stmt = (
...     select(User, address_cte)
...     .join_from(User, address_cte)
...     .order_by(User.id, address_cte.id)
... )
>>> with Session(engine) as session:
...     for user, address in session.execute(stmt):
...         print(f"{user} {address}")
BEGIN (implicit)
WITH anon_1 AS
(SELECT address.id AS id, address.email_address AS email_address, address.user_id AS user_id
FROM address
WHERE address.email_address NOT LIKE ?)
SELECT user_account.id, user_account.name, user_account.fullname,
anon_1.id AS id_1, anon_1.email_address, anon_1.user_id
FROM user_account
JOIN anon_1 ON user_account.id = anon_1.user_id
ORDER BY user_account.id, anon_1.id
[...] ('%@aol.com',)
User(id=1, name='spongebob', fullname='Spongebob Squarepants') Address(id=1, email_address='[email protected]')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=2, email_address='[email protected]')
User(id=2, name='sandy', fullname='Sandy Cheeks') Address(id=3, email_address='[email protected]')
ROLLBACK
```

See also

[Selecting Entities from Subqueries](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-subqueries) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

## Scalar and Correlated Subqueries

A scalar subquery is a subquery that returns exactly zero or one row and
exactly one column.  The subquery is then used in the COLUMNS or WHERE clause
of an enclosing SELECT statement and is different than a regular subquery in
that it is not used in the FROM clause.   A [correlated subquery](https://docs.sqlalchemy.org/en/20/glossary.html#term-correlated-subquery) is a
scalar subquery that refers to a table in the enclosing SELECT statement.

SQLAlchemy represents the scalar subquery using the
[ScalarSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect) construct, which is part of the
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) expression hierarchy, in contrast to the regular
subquery which is represented by the [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) construct, which is
in the [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) hierarchy.

Scalar subqueries are often, but not necessarily, used with aggregate functions,
introduced previously at [Aggregate functions with GROUP BY / HAVING](#tutorial-group-by-w-aggregates).   A scalar
subquery is indicated explicitly by making use of the [Select.scalar_subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.scalar_subquery)
method as below.  It’s default string form when stringified by itself
renders as an ordinary SELECT statement that is selecting from two tables:

```
>>> subq = (
...     select(func.count(address_table.c.id))
...     .where(user_table.c.id == address_table.c.user_id)
...     .scalar_subquery()
... )
>>> print(subq)
(SELECT count(address.id) AS count_1
FROM address, user_account
WHERE user_account.id = address.user_id)
```

The above `subq` object now falls within the [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
SQL expression hierarchy, in that it may be used like any other column
expression:

```
>>> print(subq == 5)
(SELECT count(address.id) AS count_1
FROM address, user_account
WHERE user_account.id = address.user_id) = :param_1
```

Although the scalar subquery by itself renders both `user_account` and
`address` in its FROM clause when stringified by itself, when embedding it
into an enclosing [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct that deals with the
`user_account` table, the `user_account` table is automatically
**correlated**, meaning it does not render in the FROM clause of the subquery:

```
>>> stmt = select(user_table.c.name, subq.label("address_count"))
>>> print(stmt)
SELECT user_account.name, (SELECT count(address.id) AS count_1
FROM address
WHERE user_account.id = address.user_id) AS address_count
FROM user_account
```

Simple correlated subqueries will usually do the right thing that’s desired.
However, in the case where the correlation is ambiguous, SQLAlchemy will let
us know that more clarity is needed:

```
>>> stmt = (
...     select(
...         user_table.c.name,
...         address_table.c.email_address,
...         subq.label("address_count"),
...     )
...     .join_from(user_table, address_table)
...     .order_by(user_table.c.id, address_table.c.id)
... )
>>> print(stmt)
Traceback (most recent call last):
...
InvalidRequestError: Select statement '<... Select object at ...>' returned
no FROM clauses due to auto-correlation; specify correlate(<tables>) to
control correlation manually.
```

To specify that the `user_table` is the one we seek to correlate we specify
this using the [ScalarSelect.correlate()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect.correlate) or
[ScalarSelect.correlate_except()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect.correlate_except) methods:

```
>>> subq = (
...     select(func.count(address_table.c.id))
...     .where(user_table.c.id == address_table.c.user_id)
...     .scalar_subquery()
...     .correlate(user_table)
... )
```

The statement then can return the data for this column like any other:

```
>>> with engine.connect() as conn:
...     result = conn.execute(
...         select(
...             user_table.c.name,
...             address_table.c.email_address,
...             subq.label("address_count"),
...         )
...         .join_from(user_table, address_table)
...         .order_by(user_table.c.id, address_table.c.id)
...     )
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name, address.email_address, (SELECT count(address.id) AS count_1
FROM address
WHERE user_account.id = address.user_id) AS address_count
FROM user_account JOIN address ON user_account.id = address.user_id ORDER BY user_account.id, address.id
[...] ()
[('spongebob', '[email protected]', 1), ('sandy', '[email protected]', 2),
 ('sandy', '[email protected]', 2)]
ROLLBACK
```

### LATERAL correlation

LATERAL correlation is a special sub-category of SQL correlation which
allows a selectable unit to refer to another selectable unit within a
single FROM clause.  This is an extremely special use case which, while
part of the SQL standard, is only known to be supported by recent
versions of PostgreSQL.

Normally, if a SELECT statement refers to
`table1 JOIN (SELECT ...) AS subquery` in its FROM clause, the subquery
on the right side may not refer to the “table1” expression from the left side;
correlation may only refer to a table that is part of another SELECT that
entirely encloses this SELECT.  The LATERAL keyword allows us to turn this
behavior around and allow correlation from the right side JOIN.

SQLAlchemy supports this feature using the [Select.lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.lateral)
method, which creates an object known as [Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral). [Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral)
is in the same family as [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) and [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias), but also
includes correlation behavior when the construct is added to the FROM clause of
an enclosing SELECT. The following example illustrates a SQL query that makes
use of LATERAL, selecting the “user account / count of email address” data as
was discussed in the previous section:

```
>>> subq = (
...     select(
...         func.count(address_table.c.id).label("address_count"),
...         address_table.c.email_address,
...         address_table.c.user_id,
...     )
...     .where(user_table.c.id == address_table.c.user_id)
...     .lateral()
... )
>>> stmt = (
...     select(user_table.c.name, subq.c.address_count, subq.c.email_address)
...     .join_from(user_table, subq)
...     .order_by(user_table.c.id, subq.c.email_address)
... )
>>> print(stmt)
SELECT user_account.name, anon_1.address_count, anon_1.email_address
FROM user_account
JOIN LATERAL (SELECT count(address.id) AS address_count,
address.email_address AS email_address, address.user_id AS user_id
FROM address
WHERE user_account.id = address.user_id) AS anon_1
ON user_account.id = anon_1.user_id
ORDER BY user_account.id, anon_1.email_address
```

Above, the right side of the JOIN is a subquery that correlates to the
`user_account` table that’s on the left side of the join.

When using [Select.lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.lateral), the behavior of
[Select.correlate()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate) and
[Select.correlate_except()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate_except) methods is applied to the
[Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral) construct as well.

See also

[Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral)

[Select.lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.lateral)

## UNION, UNION ALL and other set operations

In SQL, SELECT statements can be merged together using the UNION or UNION ALL
SQL operation, which produces the set of all rows produced by one or more
statements together.  Other set operations such as INTERSECT [ALL] and
EXCEPT [ALL] are also possible.

SQLAlchemy’s [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct supports compositions of this
nature using functions like [union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union), [intersect()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.intersect) and
[except_()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.except_), and the “all” counterparts [union_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union_all),
[intersect_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.intersect_all) and [except_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.except_all). These functions all
accept an arbitrary number of sub-selectables, which are typically
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) constructs but may also be an existing composition.

The construct produced by these functions is the [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect),
which is used in the same manner as the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct, except
that it has fewer methods.   The [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect) produced by
[union_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union_all) for example may be invoked directly using
[Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute):

```
>>> from sqlalchemy import union_all
>>> stmt1 = select(user_table).where(user_table.c.name == "sandy")
>>> stmt2 = select(user_table).where(user_table.c.name == "spongebob")
>>> u = union_all(stmt1, stmt2)
>>> with engine.connect() as conn:
...     result = conn.execute(u)
...     print(result.all())
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
UNION ALL SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[generated in ...] ('sandy', 'spongebob')
[(2, 'sandy', 'Sandy Cheeks'), (1, 'spongebob', 'Spongebob Squarepants')]
ROLLBACK
```

To use a [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect) as a subquery, just like [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
it provides a [SelectBase.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase.subquery) method which will produce a
[Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) object with a [FromClause.c](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.c)
collection that may be referenced in an enclosing [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select):

```
>>> u_subq = u.subquery()
>>> stmt = (
...     select(u_subq.c.name, address_table.c.email_address)
...     .join_from(address_table, u_subq)
...     .order_by(u_subq.c.name, address_table.c.email_address)
... )
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     print(result.all())
BEGIN (implicit)
SELECT anon_1.name, address.email_address
FROM address JOIN
  (SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
  FROM user_account
  WHERE user_account.name = ?
UNION ALL
  SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
  FROM user_account
  WHERE user_account.name = ?)
AS anon_1 ON anon_1.id = address.user_id
ORDER BY anon_1.name, address.email_address
[generated in ...] ('sandy', 'spongebob')
[('sandy', '[email protected]'), ('sandy', '[email protected]'), ('spongebob', '[email protected]')]
ROLLBACK
```

### Selecting ORM Entities from Unions

The preceding examples illustrated how to construct a UNION given two
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, to then return database rows.  If we wanted
to use a UNION or other set operation to select rows that we then receive
as ORM objects, there are two approaches that may be used.  In both cases,
we first construct a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) or [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect)
object that represents the SELECT / UNION / etc statement we want to
execute; this statement should be composed against the target
ORM entities or their underlying mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects:

```
>>> stmt1 = select(User).where(User.name == "sandy")
>>> stmt2 = select(User).where(User.name == "spongebob")
>>> u = union_all(stmt1, stmt2)
```

For a simple SELECT with UNION that is not already nested inside of a
subquery, these
can often be used in an ORM object fetching context by using the
[Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) method.  With this approach, the UNION
statement represents the entire query; no additional
criteria can be added after [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) is used:

```
>>> orm_stmt = select(User).from_statement(u)
>>> with Session(engine) as session:
...     for obj in session.execute(orm_stmt).scalars():
...         print(obj)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ? UNION ALL SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[generated in ...] ('sandy', 'spongebob')
User(id=2, name='sandy', fullname='Sandy Cheeks')
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
ROLLBACK
```

To use a UNION or other set-related construct as an entity-related component in
in a more flexible manner, the [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect) construct may be
organized into a subquery using [CompoundSelect.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect.subquery), which
then links to ORM objects using the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) function. This works
in the same way introduced at [ORM Entity Subqueries/CTEs](#tutorial-subqueries-orm-aliased), to first
create an ad-hoc “mapping” of our desired entity to the subquery, then
selecting from that new entity as though it were any other mapped class.
In the example below, we are able to add additional criteria such as ORDER BY
outside of the UNION itself, as we can filter or order by the columns exported
by the subquery:

```
>>> user_alias = aliased(User, u.subquery())
>>> orm_stmt = select(user_alias).order_by(user_alias.id)
>>> with Session(engine) as session:
...     for obj in session.execute(orm_stmt).scalars():
...         print(obj)
BEGIN (implicit)
SELECT anon_1.id, anon_1.name, anon_1.fullname
FROM (SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
FROM user_account
WHERE user_account.name = ? UNION ALL SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
FROM user_account
WHERE user_account.name = ?) AS anon_1 ORDER BY anon_1.id
[generated in ...] ('sandy', 'spongebob')
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
ROLLBACK
```

See also

[Selecting Entities from UNIONs and other set operations](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-unions) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

## EXISTS subqueries

The SQL EXISTS keyword is an operator that is used with [scalar subqueries](#tutorial-scalar-subquery) to return a boolean true or false depending on if
the SELECT statement would return a row.  SQLAlchemy includes a variant of the
[ScalarSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect) object called [Exists](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Exists), which will
generate an EXISTS subquery and is most conveniently generated using the
[SelectBase.exists()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase.exists) method.  Below we produce an EXISTS so that we
can return `user_account` rows that have more than one related row in
`address`:

```
>>> subq = (
...     select(func.count(address_table.c.id))
...     .where(user_table.c.id == address_table.c.user_id)
...     .group_by(address_table.c.user_id)
...     .having(func.count(address_table.c.id) > 1)
... ).exists()
>>> with engine.connect() as conn:
...     result = conn.execute(select(user_table.c.name).where(subq))
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name
FROM user_account
WHERE EXISTS (SELECT count(address.id) AS count_1
FROM address
WHERE user_account.id = address.user_id GROUP BY address.user_id
HAVING count(address.id) > ?)
[...] (1,)
[('sandy',)]
ROLLBACK
```

The EXISTS construct is more often than not used as a negation, e.g. NOT EXISTS,
as it provides a SQL-efficient form of locating rows for which a related
table has no rows.  Below we select user names that have no email addresses;
note the binary negation operator (`~`) used inside the second WHERE
clause:

```
>>> subq = (
...     select(address_table.c.id).where(user_table.c.id == address_table.c.user_id)
... ).exists()
>>> with engine.connect() as conn:
...     result = conn.execute(select(user_table.c.name).where(~subq))
...     print(result.all())
BEGIN (implicit)
SELECT user_account.name
FROM user_account
WHERE NOT (EXISTS (SELECT address.id
FROM address
WHERE user_account.id = address.user_id))
[...] ()
[('patrick',)]
ROLLBACK
```

## Working with SQL Functions

First introduced earlier in this section at
[Aggregate functions with GROUP BY / HAVING](#tutorial-group-by-w-aggregates), the [func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) object serves as a
factory for creating new [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function) objects, which when used
in a construct like [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select), produce a SQL function display,
typically consisting of a name, some parenthesis (although not always), and
possibly some arguments. Examples of typical SQL functions include:

- the `count()` function, an aggregate function which counts how many
  rows are returned:
  ```
  >>> print(select(func.count()).select_from(user_table))
  SELECT count(*) AS count_1
  FROM user_account
  ```
- the `lower()` function, a string function that converts a string to lower
  case:
  ```
  >>> print(select(func.lower("A String With Much UPPERCASE")))
  SELECT lower(:lower_2) AS lower_1
  ```
- the `now()` function, which provides for the current date and time; as this
  is a common function, SQLAlchemy knows how to render this differently for each
  backend, in the case of SQLite using the CURRENT_TIMESTAMP function:
  ```
  >>> stmt = select(func.now())
  >>> with engine.connect() as conn:
  ...     result = conn.execute(stmt)
  ...     print(result.all())
  BEGIN (implicit)
  SELECT CURRENT_TIMESTAMP AS now_1
  [...] ()
  [(datetime.datetime(...),)]
  ROLLBACK
  ```

As most database backends feature dozens if not hundreds of different SQL
functions, [func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) tries to be as liberal as possible in what it
accepts. Any name that is accessed from this namespace is automatically
considered to be a SQL function that will render in a generic way:

```
>>> print(select(func.some_crazy_function(user_table.c.name, 17)))
SELECT some_crazy_function(user_account.name, :some_crazy_function_2) AS some_crazy_function_1
FROM user_account
```

At the same time, a relatively small set of extremely common SQL functions such
as [count](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.count), [now](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.now), [max](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.max),
[concat](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.concat) include pre-packaged versions of themselves which
provide for proper typing information as well as backend-specific SQL
generation in some cases.  The example below contrasts the SQL generation that
occurs for the PostgreSQL dialect compared to the Oracle Database dialect for
the [now](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.now) function:

```
>>> from sqlalchemy.dialects import postgresql
>>> print(select(func.now()).compile(dialect=postgresql.dialect()))
SELECT now() AS now_1
>>> from sqlalchemy.dialects import oracle
>>> print(select(func.now()).compile(dialect=oracle.dialect()))
SELECT CURRENT_TIMESTAMP AS now_1 FROM DUAL
```

### Functions Have Return Types

As functions are column expressions, they also have
SQL [datatypes](https://docs.sqlalchemy.org/en/20/core/types.html) that describe the data type of
a generated SQL expression.  We refer to these types here as “SQL return types”,
in reference to the type of SQL value that is returned by the function
in the context of a database-side SQL expression,
as opposed to the “return type” of a Python function.

The SQL return type of any SQL function may be accessed, typically for
debugging purposes, by referring to the `Function.type`
attribute; this will be pre-configured for a **select few** of extremely
common SQL functions, but for most SQL functions is the “null” datatype
if not otherwise specified:

```
>>> # pre-configured SQL function (only a few dozen of these)
>>> func.now().type
DateTime()

>>> # arbitrary SQL function (all other SQL functions)
>>> func.run_some_calculation().type
NullType()
```

These SQL return types are significant when making
use of the function expression in the context of a larger expression; that is,
math operators will work better when the datatype of the expression is
something like [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) or [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric), JSON
accessors in order to work need to be using a type such as
[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON).  Certain classes of functions return entire rows
instead of column values, where there is a need to refer to specific columns;
such functions are known
as [table valued functions](#tutorial-functions-table-valued).

The SQL return type of the function may also be significant when executing a
statement and getting rows back, for those cases where SQLAlchemy has to apply
result-set processing. A prime example of this are date-related functions on
SQLite, where SQLAlchemy’s [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime) and related datatypes take
on the role of converting from string values to Python `datetime()` objects
as result rows are received.

To apply a specific type to a function we’re creating, we pass it using the
[Function.type_](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function.params.type_) parameter; the type argument may be
either a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or an instance.  In the example
below we pass the [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) class to generate the PostgreSQL
`json_object()` function, noting that the SQL return type will be of
type JSON:

```
>>> from sqlalchemy import JSON
>>> function_expr = func.json_object('{a, 1, b, "def", c, 3.5}', type_=JSON)
```

By creating our JSON function with the [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) datatype, the
SQL expression object takes on JSON-related features, such as that of accessing
elements:

```
>>> stmt = select(function_expr["def"])
>>> print(stmt)
SELECT json_object(:json_object_1)[:json_object_2] AS anon_1
```

### Built-in Functions Have Pre-Configured Return Types

For common aggregate functions like [count](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.count),
[max](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.max), [min](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.min) as well as a very small number
of date functions like [now](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.now) and string functions like
[concat](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.concat), the SQL return type is set up appropriately,
sometimes based on usage. The [max](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.max) function and similar
aggregate filtering functions will set up the SQL return type based on the
argument given:

```
>>> m1 = func.max(Column("some_int", Integer))
>>> m1.type
Integer()

>>> m2 = func.max(Column("some_str", String))
>>> m2.type
String()
```

Date and time functions typically correspond to SQL expressions described by
[DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime), [Date](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Date) or [Time](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Time):

```
>>> func.now().type
DateTime()
>>> func.current_date().type
Date()
```

A known string function such as [concat](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.concat)
will know that a SQL expression would be of type [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String):

```
>>> func.concat("x", "y").type
String()
```

However, for the vast majority of SQL functions, SQLAlchemy does not have them
explicitly present in its very small list of known functions.  For example,
while there is typically no issue using SQL functions `func.lower()`
and `func.upper()` to convert the casing of strings, SQLAlchemy doesn’t
actually know about these functions, so they have a “null” SQL return type:

```
>>> func.upper("lowercase").type
NullType()
```

For simple functions like `upper` and `lower`, the issue is not usually
significant, as string values may be received from the database without any
special type handling on the SQLAlchemy side, and SQLAlchemy’s type
coercion rules can often correctly guess intent as well; the Python `+`
operator for example will be correctly interpreted as the string concatenation
operator based on looking at both sides of the expression:

```
>>> print(select(func.upper("lowercase") + " suffix"))
SELECT upper(:upper_1) || :upper_2 AS anon_1
```

Overall, the scenario where the
[Function.type_](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function.params.type_) parameter is likely necessary is:

1. the function is not already a SQLAlchemy built-in function; this can be
  evidenced by creating the function and observing the `Function.type`
  attribute, that is:
  ```
  >>> func.count().type
  Integer()
  ```
  vs.:
  ```
  >>> func.json_object('{"a", "b"}').type
  NullType()
  ```
2. Function-aware expression support is needed; this most typically refers to
  special operators related to datatypes such as [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) or
  [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY)
3. Result value processing is needed, which may include types such as
  `DateTime`, [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean), [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum),
  or again special datatypes such as [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON),
  [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY).

### Advanced SQL Function Techniques

The following subsections illustrate more things that can be done with
SQL functions.  While these techniques are less common and more advanced than
basic SQL function use, they nonetheless are extremely popular, largely
as a result of PostgreSQL’s emphasis on more complex function forms, including
table- and column-valued forms that are popular with JSON data.

#### Using Window Functions

A window function is a special use of a SQL aggregate function which calculates
the aggregate value over the rows being returned in a group as the individual
result rows are processed.  Whereas a function like `MAX()` will give you
the highest value of a column within a set of rows, using the same function
as a “window function” will given you the highest value for each row,
*as of that row*.

In SQL, window functions allow one to specify the rows over which the
function should be applied, a “partition” value which considers the window
over different sub-sets of rows, and an “order by” expression which importantly
indicates the order in which rows should be applied to the aggregate function.

In SQLAlchemy, all SQL functions generated by the [func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) namespace
include a method [FunctionElement.over()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.over) which
grants the window function, or “OVER”, syntax; the construct produced
is the [Over](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Over) construct.

A common function used with window functions is the `row_number()` function
which simply counts rows. We may partition this row count against user name to
number the email addresses of individual users:

```
>>> stmt = (
...     select(
...         func.row_number().over(partition_by=user_table.c.name),
...         user_table.c.name,
...         address_table.c.email_address,
...     )
...     .select_from(user_table)
...     .join(address_table)
... )
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     print(result.all())
BEGIN (implicit)
SELECT row_number() OVER (PARTITION BY user_account.name) AS anon_1,
user_account.name, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
[...] ()
[(1, 'sandy', '[email protected]'), (2, 'sandy', '[email protected]'), (1, 'spongebob', '[email protected]')]
ROLLBACK
```

Above, the [FunctionElement.over.partition_by](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.over.params.partition_by) parameter
is used so that the `PARTITION BY` clause is rendered within the OVER clause.
We also may make use of the `ORDER BY` clause using [FunctionElement.over.order_by](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.over.params.order_by):

```
>>> stmt = (
...     select(
...         func.count().over(order_by=user_table.c.name),
...         user_table.c.name,
...         address_table.c.email_address,
...     )
...     .select_from(user_table)
...     .join(address_table)
... )
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     print(result.all())
BEGIN (implicit)
SELECT count(*) OVER (ORDER BY user_account.name) AS anon_1,
user_account.name, address.email_address
FROM user_account JOIN address ON user_account.id = address.user_id
[...] ()
[(2, 'sandy', '[email protected]'), (2, 'sandy', '[email protected]'), (3, 'spongebob', '[email protected]')]
ROLLBACK
```

Further options for window functions include usage of ranges; see
[over()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over) for more examples.

Tip

It’s important to note that the [FunctionElement.over()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.over)
method only applies to those SQL functions which are in fact aggregate
functions; while the [Over](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Over) construct will happily render itself
for any SQL function given, the database will reject the expression if the
function itself is not a SQL aggregate function.

#### Special Modifiers WITHIN GROUP, FILTER

The “WITHIN GROUP” SQL syntax is used in conjunction with an “ordered set”
or a “hypothetical set” aggregate
function.  Common “ordered set” functions include `percentile_cont()`
and `rank()`.  SQLAlchemy includes built in implementations
[rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.rank), [dense_rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.dense_rank),
[mode](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.mode), [percentile_cont](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percentile_cont) and
[percentile_disc](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percentile_disc) which include a [FunctionElement.within_group()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.within_group)
method:

```
>>> print(
...     func.unnest(
...         func.percentile_disc([0.25, 0.5, 0.75, 1]).within_group(user_table.c.name)
...     )
... )
unnest(percentile_disc(:percentile_disc_1) WITHIN GROUP (ORDER BY user_account.name))
```

“FILTER” is supported by some backends to limit the range of an aggregate function to a
particular subset of rows compared to the total range of rows returned, available
using the [FunctionElement.filter()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.filter) method:

```
>>> stmt = (
...     select(
...         func.count(address_table.c.email_address).filter(user_table.c.name == "sandy"),
...         func.count(address_table.c.email_address).filter(
...             user_table.c.name == "spongebob"
...         ),
...     )
...     .select_from(user_table)
...     .join(address_table)
... )
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     print(result.all())
BEGIN (implicit)
SELECT count(address.email_address) FILTER (WHERE user_account.name = ?) AS anon_1,
count(address.email_address) FILTER (WHERE user_account.name = ?) AS anon_2
FROM user_account JOIN address ON user_account.id = address.user_id
[...] ('sandy', 'spongebob')
[(2, 1)]
ROLLBACK
```

#### Table-Valued Functions

Table-valued SQL functions support a scalar representation that contains named
sub-elements. Often used for JSON and ARRAY-oriented functions as well as
functions like `generate_series()`, the table-valued function is specified in
the FROM clause, and is then referenced as a table, or sometimes even as a
column. Functions of this form are prominent within the PostgreSQL database,
however some forms of table valued functions are also supported by SQLite,
Oracle Database, and SQL Server.

See also

[Table values, Table and Column valued functions, Row and Tuple objects](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-table-valued-overview) - in the [PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) documentation.

While many databases support table valued and other special
forms, PostgreSQL tends to be where there is the most demand for these
features.   See this section for additional examples of PostgreSQL
syntaxes as well as additional features.

SQLAlchemy provides the [FunctionElement.table_valued()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.table_valued) method
as the basic “table valued function” construct, which will convert a
[func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) object into a FROM clause containing a series of named
columns, based on string names passed positionally. This returns a
[TableValuedAlias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableValuedAlias) object, which is a function-enabled
[Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) construct that may be used as any other FROM clause as
introduced at [Using Aliases](#tutorial-using-aliases). Below we illustrate the
`json_each()` function, which while common on PostgreSQL is also supported by
modern versions of SQLite:

```
>>> onetwothree = func.json_each('["one", "two", "three"]').table_valued("value")
>>> stmt = select(onetwothree).where(onetwothree.c.value.in_(["two", "three"]))
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     result.all()
BEGIN (implicit)
SELECT anon_1.value
FROM json_each(?) AS anon_1
WHERE anon_1.value IN (?, ?)
[...] ('["one", "two", "three"]', 'two', 'three')
[('two',), ('three',)]
ROLLBACK
```

Above, we used the `json_each()` JSON function supported by SQLite and
PostgreSQL to generate a table valued expression with a single column referred
towards as `value`, and then selected two of its three rows.

See also

[Table-Valued Functions](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-table-valued) - in the [PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) documentation -
this section will detail additional syntaxes such as special column derivations
and “WITH ORDINALITY” that are known to work with PostgreSQL.

#### Column Valued Functions - Table Valued Function as a Scalar Column

A special syntax supported by PostgreSQL and Oracle Database is that of
referring towards a function in the FROM clause, which then delivers itself as
a single column in the columns clause of a SELECT statement or other column
expression context.  PostgreSQL makes great use of this syntax for such
functions as `json_array_elements()`, `json_object_keys()`,
`json_each_text()`, `json_each()`, etc.

SQLAlchemy refers to this as a “column valued” function and is available
by applying the [FunctionElement.column_valued()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.column_valued) modifier
to a [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function) construct:

```
>>> from sqlalchemy import select, func
>>> stmt = select(func.json_array_elements('["one", "two"]').column_valued("x"))
>>> print(stmt)
SELECT x
FROM json_array_elements(:json_array_elements_1) AS x
```

The “column valued” form is also supported by the Oracle Database dialects,
where it is usable for custom SQL functions:

```
>>> from sqlalchemy.dialects import oracle
>>> stmt = select(func.scalar_strings(5).column_valued("s"))
>>> print(stmt.compile(dialect=oracle.dialect()))
SELECT s.COLUMN_VALUE
FROM TABLE (scalar_strings(:scalar_strings_1)) s
```

See also

[Column Valued Functions](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-column-valued) - in the [PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) documentation.

## Data Casts and Type Coercion

In SQL, we often need to indicate the datatype of an expression explicitly,
either to tell the database what type is expected in an otherwise ambiguous
expression, or in some cases when we want to convert the implied datatype
of a SQL expression into something else.   The SQL CAST keyword is used for
this task, which in SQLAlchemy is provided by the [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) function.
This function accepts a column expression and a data type
object as arguments, as demonstrated below where we produce a SQL expression
`CAST(user_account.id AS VARCHAR)` from the `user_table.c.id` column
object:

```
>>> from sqlalchemy import cast
>>> stmt = select(cast(user_table.c.id, String))
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     result.all()
BEGIN (implicit)
SELECT CAST(user_account.id AS VARCHAR) AS id
FROM user_account
[...] ()
[('1',), ('2',), ('3',)]
ROLLBACK
```

The [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) function not only renders the SQL CAST syntax, it also
produces a SQLAlchemy column expression that will act as the given datatype on
the Python side as well. A string expression that is [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) to
[JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) will gain JSON subscript and comparison operators, for example:

```
>>> from sqlalchemy import JSON
>>> print(cast("{'a': 'b'}", JSON)["a"])
CAST(:param_1 AS JSON)[:param_2]
```

### type_coerce() - a Python-only “cast”

Sometimes there is the need to have SQLAlchemy know the datatype of an
expression, for all the reasons mentioned above, but to not render the CAST
expression itself on the SQL side, where it may interfere with a SQL operation
that already works without it.  For this fairly common use case there is
another function [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) which is closely related to
[cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast), in that it sets up a Python expression as having a specific SQL
database type, but does not render the `CAST` keyword or datatype on the
database side.    [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) is particularly important when dealing
with the [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) datatype, which typically has an intricate
relationship with string-oriented datatypes on different platforms and
may not even be an explicit datatype, such as on SQLite and MariaDB.
Below, we use [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) to deliver a Python structure as a JSON
string into one of MySQL’s JSON functions:

```
>>> import json
>>> from sqlalchemy import JSON
>>> from sqlalchemy import type_coerce
>>> from sqlalchemy.dialects import mysql
>>> s = select(type_coerce({"some_key": {"foo": "bar"}}, JSON)["some_key"])
>>> print(s.compile(dialect=mysql.dialect()))
SELECT JSON_EXTRACT(%s, %s) AS anon_1
```

Above, MySQL’s `JSON_EXTRACT` SQL function was invoked
because we used [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) to indicate that our Python dictionary
should be treated as [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON).  The Python `__getitem__`
operator, `['some_key']` in this case, became available as a result and
allowed a `JSON_EXTRACT` path expression (not shown, however in this
case it would ultimately be `'$."some_key"'`) to be rendered.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: [Using UPDATE and DELETE Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html)
