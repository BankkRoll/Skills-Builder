# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [Working with Database Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html)   |   Next: [Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html)

# Working with Data

In [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-working-with-transactions), we learned the basics of how to
interact with the Python DBAPI and its transactional state.  Then, in
[Working with Database Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata), we learned how to represent database
tables, columns, and constraints within SQLAlchemy using the
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) and related objects.  In this section we will combine
both concepts above to create, select and manipulate data within a relational
database.   Our interaction with the database is **always** in terms
of a transaction, even if we’ve set our database driver to use [autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit) behind the scenes.

The components of this section are as follows:

- [Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert) - to get some data into the database, we introduce
  and demonstrate the Core [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct.   INSERTs from an
  ORM perspective are described in the next section
  [Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation).
- [Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-data) - this section will describe in detail
  the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct, which is the most commonly used object
  in SQLAlchemy.  The [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct emits SELECT statements
  for both Core and ORM centric applications and both use cases will be
  described here.   Additional ORM use cases are also noted in the later
  section [Using Relationships in Queries](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-select-relationships) as well as the
  [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).
- [Using UPDATE and DELETE Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-core-update-delete) - Rounding out the INSERT and SELECTion
  of data, this section will describe from a Core perspective the use of the
  [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) constructs.  ORM-specific
  UPDATE and DELETE is similarly described in the
  [Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation) section.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: [Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html)

---

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [Working with Data](https://docs.sqlalchemy.org/en/20/tutorial/data.html)   |   Next: [Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)

# Using INSERT Statements

When using Core as well as when using the ORM for bulk operations, a SQL INSERT
statement is generated directly using the [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) function - this
function generates a new instance of [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) which represents an
INSERT statement in SQL, that adds new data into a table.

**ORM Readers** -

This section details the Core means of generating an individual SQL INSERT
statement in order to add new rows to a table. When using the ORM, we
normally use another tool that rides on top of this called the
[unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work), which will automate the production of many INSERT
statements at once. However, understanding how the Core handles data
creation and manipulation is very useful even when the ORM is running
it for us.  Additionally, the ORM supports direct use of INSERT
using a feature called [Bulk / Multi Row INSERT, upsert, UPDATE and DELETE](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-bulk).

To skip directly to how to INSERT rows with the ORM using normal
unit of work patterns, see [Inserting Rows using the ORM Unit of Work pattern](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-inserting-orm).

## The insert() SQL Expression Construct

A simple example of [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) illustrating the target table
and the VALUES clause at once:

```
>>> from sqlalchemy import insert
>>> stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
```

The above `stmt` variable is an instance of [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert).  Most
SQL expressions can be stringified in place as a means to see the general
form of what’s being produced:

```
>>> print(stmt)
INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)
```

The stringified form is created by producing a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) form
of the object which includes a database-specific string SQL representation of
the statement; we can acquire this object directly using the
[ClauseElement.compile()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compile) method:

```
>>> compiled = stmt.compile()
```

Our [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct is an example of a “parameterized”
construct, illustrated previously at [Sending Parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-sending-parameters); to
view the `name` and `fullname` [bound parameters](https://docs.sqlalchemy.org/en/20/glossary.html#term-bound-parameters), these are
available from the [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) construct as well:

```
>>> compiled.params
{'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}
```

## Executing the Statement

Invoking the statement we can INSERT a row into `user_table`.
The INSERT SQL as well as the bundled parameters can be seen in the
SQL logging:

```
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     conn.commit()
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('spongebob', 'Spongebob Squarepants')
COMMIT
```

In its simple form above, the INSERT statement does not return any rows, and if
only a single row is inserted, it will usually include the ability to return
information about column-level default values that were generated during the
INSERT of that row, most commonly an integer primary key value.  In the above
case the first row in a SQLite database will normally return `1` for the
first integer primary key value, which we can acquire using the
[CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) accessor:

```
>>> result.inserted_primary_key
(1,)
```

Tip

[CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) returns a tuple
because a primary key may contain multiple columns.  This is known as
a [composite primary key](https://docs.sqlalchemy.org/en/20/glossary.html#term-composite-primary-key).  The [CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key)
is intended to always contain the complete primary key of the record just
inserted, not just a “cursor.lastrowid” kind of value, and is also intended
to be populated regardless of whether or not “autoincrement” were used, hence
to express a complete primary key it’s a tuple.

Changed in version 1.4.8: the tuple returned by
[CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) is now a named tuple
fulfilled by returning it as a [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) object.

## INSERT usually generates the “values” clause automatically

The example above made use of the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method to
explicitly create the VALUES clause of the SQL INSERT statement.   If
we don’t actually use [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) and just print out an “empty”
statement, we get an INSERT for every column in the table:

```
>>> print(insert(user_table))
INSERT INTO user_account (id, name, fullname) VALUES (:id, :name, :fullname)
```

If we take an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct that has not had
[Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) called upon it and execute it
rather than print it, the statement will be compiled to a string based
on the parameters that we passed to the [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute)
method, and only include columns relevant to the parameters that were
passed.   This is actually the usual way that
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) is used to insert rows without having to type out
an explicit VALUES clause.   The example below illustrates a two-column
INSERT statement being executed with a list of parameters at once:

```
>>> with engine.connect() as conn:
...     result = conn.execute(
...         insert(user_table),
...         [
...             {"name": "sandy", "fullname": "Sandy Cheeks"},
...             {"name": "patrick", "fullname": "Patrick Star"},
...         ],
...     )
...     conn.commit()
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] [('sandy', 'Sandy Cheeks'), ('patrick', 'Patrick Star')]
COMMIT
```

The execution above features “executemany” form first illustrated at
[Sending Multiple Parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-multiple-parameters), however unlike when using the
[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct, we didn’t have to spell out any SQL.
By passing a dictionary or list of dictionaries to the [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute)
method in conjunction with the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct, the
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) ensures that the column names which are passed
will be expressed in the VALUES clause of the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
construct automatically.

Tip

When passing a list of dictionaries to [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute)
along with a Core [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), **only the first dictionary in the
list determines what columns will be in the VALUES clause**. The rest of
the dictionaries are not scanned. This is both because within traditional
`executemany()`, the INSERT statement can only have one VALUES clause for
all parameters, and additionally SQLAlchemy does not want to add overhead
by scanning every parameter dictionary to verify each contains the identical
keys as the first one.

Note this behavior is distinctly different from that of an [ORM
enabled INSERT](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-bulk), introduced later in this tutorial,
which performs a full scan of parameter sets in terms of an ORM entity.

Deep Alchemy

Hi, welcome to the first edition of **Deep Alchemy**.   The person on the
left is known as **The Alchemist**, and you’ll note they are **not** a wizard,
as the pointy hat is not sticking upwards.   The Alchemist comes around to
describe things that are generally **more advanced and/or tricky** and
additionally **not usually needed**, but for whatever reason they feel you
should know about this thing that SQLAlchemy can do.

In this edition, towards the goal of having some interesting data in the
`address_table` as well, below is a more advanced example illustrating
how the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method may be used explicitly while at
the same time including for additional VALUES generated from the
parameters.    A [scalar subquery](https://docs.sqlalchemy.org/en/20/glossary.html#term-scalar-subquery) is constructed, making use of the
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct introduced in the next section, and the
parameters used in the subquery are set up using an explicit bound
parameter name, established using the [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) construct.

This is some slightly **deeper** alchemy just so that we can add related
rows without fetching the primary key identifiers from the `user_table`
operation into the application.   Most Alchemists will simply use the ORM
which takes care of things like this for us.

```
>>> from sqlalchemy import select, bindparam
>>> scalar_subq = (
...     select(user_table.c.id)
...     .where(user_table.c.name == bindparam("username"))
...     .scalar_subquery()
... )

>>> with engine.connect() as conn:
...     result = conn.execute(
...         insert(address_table).values(user_id=scalar_subq),
...         [
...             {
...                 "username": "spongebob",
...                 "email_address": "[email protected]",
...             },
...             {"username": "sandy", "email_address": "[email protected]"},
...             {"username": "sandy", "email_address": "[email protected]"},
...         ],
...     )
...     conn.commit()
BEGIN (implicit)
INSERT INTO address (user_id, email_address) VALUES ((SELECT user_account.id
FROM user_account
WHERE user_account.name = ?), ?)
[...] [('spongebob', '[email protected]'), ('sandy', '[email protected]'),
('sandy', '[email protected]')]
COMMIT
```

With that, we have some more interesting data in our tables that we will
make use of in the upcoming sections.

Tip

A true “empty” INSERT that inserts only the “defaults” for a table
without including any explicit values at all is generated if we indicate
[Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) with no arguments; not every database backend
supports this, but here’s what SQLite produces:

```
>>> print(insert(user_table).values().compile(engine))
INSERT INTO user_account DEFAULT VALUES
```

## INSERT…RETURNING

The RETURNING clause for supported backends is used
automatically in order to retrieve the last inserted primary key value
as well as the values for server defaults.   However the RETURNING clause
may also be specified explicitly using the [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning)
method; in this case, the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)
object that’s returned when the statement is executed has rows which
can be fetched:

```
>>> insert_stmt = insert(address_table).returning(
...     address_table.c.id, address_table.c.email_address
... )
>>> print(insert_stmt)
INSERT INTO address (id, user_id, email_address)
VALUES (:id, :user_id, :email_address)
RETURNING address.id, address.email_address
```

It can also be combined with [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select),
as in the example below that builds upon the example stated in
[INSERT…FROM SELECT](#tutorial-insert-from-select):

```
>>> select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
>>> insert_stmt = insert(address_table).from_select(
...     ["user_id", "email_address"], select_stmt
... )
>>> print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))
INSERT INTO address (user_id, email_address)
SELECT user_account.id, user_account.name || :name_1 AS anon_1
FROM user_account RETURNING address.id, address.email_address
```

Tip

The RETURNING feature is also supported by UPDATE and DELETE statements,
which will be introduced later in this tutorial.

For INSERT statements, the RETURNING feature may be used
both for single-row statements as well as for statements that INSERT
multiple rows at once.  Support for multiple-row INSERT with RETURNING
is dialect specific, however is supported for all the dialects
that are included in SQLAlchemy which support RETURNING.  See the section
[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) for background on this feature.

See also

Bulk INSERT with or without RETURNING is also supported by the ORM.  See
[ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) for reference documentation.

## INSERT…FROM SELECT

A less used feature of [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), but here for completeness, the
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct can compose an INSERT that gets rows directly
from a SELECT using the [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select) method.
This method accepts a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct, which is discussed in the
next section, along with a list of column names to be targeted in the
actual INSERT.  In the example below, rows are added to the `address`
table which are derived from rows in the `user_account` table, giving each
user a free email address at `aol.com`:

```
>>> select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
>>> insert_stmt = insert(address_table).from_select(
...     ["user_id", "email_address"], select_stmt
... )
>>> print(insert_stmt)
INSERT INTO address (user_id, email_address)
SELECT user_account.id, user_account.name || :name_1 AS anon_1
FROM user_account
```

This construct is used when one wants to copy data from
some other part of the database directly into a new set of rows, without
actually fetching and re-sending the data from the client.

See also

[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) - in the SQL Expression API documentation

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: [Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)
