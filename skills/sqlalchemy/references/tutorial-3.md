# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)   |   Next: [Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html)

# Using UPDATE and DELETE Statements

So far we’ve covered [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), so that we can get some data into
our database, and then spent a lot of time on [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) which
handles the broad range of usage patterns used for retrieving data from the
database.   In this section we will cover the [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and
[Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) constructs, which are used to modify existing rows
as well as delete existing rows.    This section will cover these constructs
from a Core-centric perspective.

**ORM Readers** - As was the case mentioned at [Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert),
the [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) operations when used with
the ORM are usually invoked internally from the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
object as part of the [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) process.

However, unlike [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), the [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and
[Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) constructs can also be used directly with the ORM,
using a pattern known as “ORM-enabled update and delete”; for this reason,
familiarity with these constructs is useful for ORM use.  Both styles of
use are discussed in the sections [Updating ORM Objects using the Unit of Work pattern](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-updating) and
[Deleting ORM Objects using the Unit of Work pattern](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-deleting).

## The update() SQL Expression Construct

The [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) function generates a new instance of
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) which represents an UPDATE statement in SQL, that will
update existing data in a table.

Like the [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct, there is a “traditional” form of
[update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update), which emits UPDATE against a single table at a time and
does not return any rows.   However some backends support an UPDATE statement
that may modify multiple tables at once, and the UPDATE statement also
supports RETURNING such that columns contained in matched rows may be returned
in the result set.

A basic UPDATE looks like:

```
>>> from sqlalchemy import update
>>> stmt = (
...     update(user_table)
...     .where(user_table.c.name == "patrick")
...     .values(fullname="Patrick the Star")
... )
>>> print(stmt)
UPDATE user_account SET fullname=:fullname WHERE user_account.name = :name_1
```

The [Update.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.values) method controls the contents of the SET elements
of the UPDATE statement.  This is the same method shared by the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
construct.   Parameters can normally be passed using the column names as
keyword arguments.

UPDATE supports all the major SQL forms of UPDATE, including updates against expressions,
where we can make use of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) expressions:

```
>>> stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
>>> print(stmt)
UPDATE user_account SET fullname=(:name_1 || user_account.name)
```

To support UPDATE in an “executemany” context, where many parameter sets will
be invoked against the same statement, the [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
construct may be used to set up bound parameters; these replace the places
that literal values would normally go:

```
>>> from sqlalchemy import bindparam
>>> stmt = (
...     update(user_table)
...     .where(user_table.c.name == bindparam("oldname"))
...     .values(name=bindparam("newname"))
... )
>>> with engine.begin() as conn:
...     conn.execute(
...         stmt,
...         [
...             {"oldname": "jack", "newname": "ed"},
...             {"oldname": "wendy", "newname": "mary"},
...             {"oldname": "jim", "newname": "jake"},
...         ],
...     )
BEGIN (implicit)
UPDATE user_account SET name=? WHERE user_account.name = ?
[...] [('ed', 'jack'), ('mary', 'wendy'), ('jake', 'jim')]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

Other techniques which may be applied to UPDATE include:

### Correlated Updates

An UPDATE statement can make use of rows in other tables by using a
[correlated subquery](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery).  A subquery may be used
anywhere a column expression might be placed:

```
>>> scalar_subq = (
...     select(address_table.c.email_address)
...     .where(address_table.c.user_id == user_table.c.id)
...     .order_by(address_table.c.id)
...     .limit(1)
...     .scalar_subquery()
... )
>>> update_stmt = update(user_table).values(fullname=scalar_subq)
>>> print(update_stmt)
UPDATE user_account SET fullname=(SELECT address.email_address
FROM address
WHERE address.user_id = user_account.id ORDER BY address.id
LIMIT :param_1)
```

### UPDATE..FROM

Some databases such as PostgreSQL, MSSQL and MySQL support a syntax `UPDATE...FROM`
where additional tables may be stated directly in a special FROM clause. This
syntax will be generated implicitly when additional tables are located in the
WHERE clause of the statement:

```
>>> update_stmt = (
...     update(user_table)
...     .where(user_table.c.id == address_table.c.user_id)
...     .where(address_table.c.email_address == "[email protected]")
...     .values(fullname="Pat")
... )
>>> print(update_stmt)
UPDATE user_account SET fullname=:fullname FROM address
WHERE user_account.id = address.user_id AND address.email_address = :email_address_1
```

There is also a MySQL specific syntax that can UPDATE multiple tables. This
requires we refer to [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects in the VALUES clause in
order to refer to additional tables:

```
>>> update_stmt = (
...     update(user_table)
...     .where(user_table.c.id == address_table.c.user_id)
...     .where(address_table.c.email_address == "[email protected]")
...     .values(
...         {
...             user_table.c.fullname: "Pat",
...             address_table.c.email_address: "[email protected]",
...         }
...     )
... )
>>> from sqlalchemy.dialects import mysql
>>> print(update_stmt.compile(dialect=mysql.dialect()))
UPDATE user_account, address
SET address.email_address=%s, user_account.fullname=%s
WHERE user_account.id = address.user_id AND address.email_address = %s
```

`UPDATE...FROM` can also be
combined with the [Values](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values) construct
on backends such as PostgreSQL, to create a single UPDATE statement that updates
multiple rows at once against the named form of VALUES:

```
>>> from sqlalchemy import Values
>>> values = Values(
...     user_table.c.id,
...     user_table.c.name,
...     name="my_values",
... ).data([(1, "new_name"), (2, "another_name"), ("3", "name_name")])
>>> update_stmt = (
...     user_table.update().values(name=values.c.name).where(user_table.c.id == values.c.id)
... )
>>> from sqlalchemy.dialects import postgresql
>>> print(update_stmt.compile(dialect=postgresql.dialect()))
UPDATE user_account
SET name=my_values.name
FROM (VALUES (%(param_1)s, %(param_2)s), (%(param_3)s, %(param_4)s), (%(param_5)s, %(param_6)s)) AS my_values (id, name)
WHERE user_account.id = my_values.id
```

### Parameter Ordered Updates

Another MySQL-only behavior is that the order of parameters in the SET clause
of an UPDATE actually impacts the evaluation of each expression.   For this use
case, the [Update.ordered_values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.ordered_values) method accepts a sequence of
tuples so that this order may be controlled [[2]](#id2):

```
>>> update_stmt = update(some_table).ordered_values(
...     (some_table.c.y, 20), (some_table.c.x, some_table.c.y + 10)
... )
>>> print(update_stmt)
UPDATE some_table SET y=:y, x=(some_table.y + :y_1)
```

    [[2](#id1)]

While Python dictionaries are
[guaranteed to be insert ordered](https://mail.python.org/pipermail/python-dev/2017-December/151283.html)
as of Python 3.7, the
[Update.ordered_values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.ordered_values) method still provides an additional
measure of clarity of intent when it is essential that the SET clause
of a MySQL UPDATE statement proceed in a specific way.

## The delete() SQL Expression Construct

The [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) function generates a new instance of
[Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) which represents a DELETE statement in SQL, that will
delete rows from a table.

The [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) statement from an API perspective is very similar to
that of the [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) construct, traditionally returning no rows but
allowing for a RETURNING variant on some database backends.

```
>>> from sqlalchemy import delete
>>> stmt = delete(user_table).where(user_table.c.name == "patrick")
>>> print(stmt)
DELETE FROM user_account WHERE user_account.name = :name_1
```

### Multiple Table Deletes

Like [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update), [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) supports the use of correlated
subqueries in the WHERE clause as well as backend-specific multiple table
syntaxes, such as `DELETE FROM..USING` on MySQL:

```
>>> delete_stmt = (
...     delete(user_table)
...     .where(user_table.c.id == address_table.c.user_id)
...     .where(address_table.c.email_address == "[email protected]")
... )
>>> from sqlalchemy.dialects import mysql
>>> print(delete_stmt.compile(dialect=mysql.dialect()))
DELETE FROM user_account USING user_account, address
WHERE user_account.id = address.user_id AND address.email_address = %s
```

## Getting Affected Row Count from UPDATE, DELETE

Both [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) support the ability to
return the number of rows matched after the statement proceeds, for statements
that are invoked using Core [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), i.e.
[Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute). Per the caveats mentioned below, this value
is available from the [CursorResult.rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount) attribute:

```
>>> with engine.begin() as conn:
...     result = conn.execute(
...         update(user_table)
...         .values(fullname="Patrick McStar")
...         .where(user_table.c.name == "patrick")
...     )
...     print(result.rowcount)
BEGIN (implicit)
UPDATE user_account SET fullname=? WHERE user_account.name = ?
[...] ('Patrick McStar', 'patrick')
1
COMMIT
```

Tip

The [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) class is a subclass of
[Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) which contains additional attributes that are
specific to the DBAPI `cursor` object.  An instance of this subclass is
returned when a statement is invoked via the
[Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) method. When using the ORM, the
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method will normally **not** return this type
of object, unless the given query uses only Core [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects
directly.

Facts about [CursorResult.rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount):

- The value returned is the number of rows **matched** by the WHERE clause of
  the statement.   It does not matter if the row were actually modified or not.
- [CursorResult.rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount) is not necessarily available for an UPDATE
  or DELETE statement that uses RETURNING, or for one that uses an
  [executemany](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-multiple-parameters) execution.   The availability
  depends on the DBAPI module in use.
- In any case where the DBAPI does not determine the rowcount for some type
  of statement, the returned value will be `-1`.
- SQLAlchemy pre-memoizes the DBAPIs `cursor.rowcount` value before the cursor
  is closed, as some DBAPIs don’t support accessing this attribute after the
  fact.  In order to pre-memoize `cursor.rowcount` for a statement that is
  not UPDATE or DELETE, such as INSERT or SELECT, the
  [Connection.execution_options.preserve_rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.preserve_rowcount) execution
  option may be used.
- Some drivers, particularly third party dialects for non-relational databases,
  may not support [CursorResult.rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount) at all.   The
  [CursorResult.supports_sane_rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.supports_sane_rowcount) cursor attribute will
  indicate this.
- “rowcount” is used by the ORM [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) process to validate that
  an UPDATE or DELETE statement matched the expected number of rows, and is
  also essential for the ORM versioning feature documented at
  [Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html#mapper-version-counter).

## Using RETURNING with UPDATE, DELETE

Like the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct, [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete)
also support the RETURNING clause which is added by using the
[Update.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.returning) and [Delete.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete.returning) methods.
When these methods are used on a backend that supports RETURNING, selected
columns from all rows that match the WHERE criteria of the statement
will be returned in the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object as rows that can
be iterated:

```
>>> update_stmt = (
...     update(user_table)
...     .where(user_table.c.name == "patrick")
...     .values(fullname="Patrick the Star")
...     .returning(user_table.c.id, user_table.c.name)
... )
>>> print(update_stmt)
UPDATE user_account SET fullname=:fullname
WHERE user_account.name = :name_1
RETURNING user_account.id, user_account.name
>>> delete_stmt = (
...     delete(user_table)
...     .where(user_table.c.name == "patrick")
...     .returning(user_table.c.id, user_table.c.name)
... )
>>> print(delete_stmt)
DELETE FROM user_account
WHERE user_account.name = :name_1
RETURNING user_account.id, user_account.name
```

## Further Reading for UPDATE, DELETE

See also

API documentation for UPDATE / DELETE:

- [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)
- [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete)

ORM-enabled UPDATE and DELETE:

[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: [Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html)

---

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [Establishing Connectivity - the Engine](https://docs.sqlalchemy.org/en/20/tutorial/engine.html)   |   Next: [Working with Database Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html)

# Working with Transactions and the DBAPI

With the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object ready to go, we can
dive into the basic operation of an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) and
its primary endpoints, the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and
[Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result). We’ll also introduce the ORM’s [facade](https://docs.sqlalchemy.org/en/20/glossary.html#term-facade)
for these objects, known as the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

**Note to ORM readers**

When using the ORM, the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) is managed by the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) in modern SQLAlchemy
emphasizes a transactional and SQL execution pattern that is largely
identical to that of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) discussed below,
so while this subsection is Core-centric, all of the concepts here
are relevant to ORM use as well and is recommended for all ORM
learners.   The execution pattern used by the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
will be compared to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) at the end
of this section.

As we have yet to introduce the SQLAlchemy Expression Language that is the
primary feature of SQLAlchemy, we’ll use a simple construct within
this package called the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct, to write
SQL statements as **textual SQL**.   Rest assured that textual SQL is the
exception rather than the rule in day-to-day SQLAlchemy use, but it’s
always available.

## Getting a Connection

The purpose of the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) is to connect to the database by
providing a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object.   When working with the Core
directly, the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object is how all interaction with the
database is done.   Because the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) creates an open
resource against the database, we want to limit our use of this object to a
specific context. The best way to do that is with a Python context manager, also
known as [the with statement](https://docs.python.org/3/reference/compound_stmts.html#with).
Below we use a textual SQL statement to show “Hello World”.  Textual SQL is
created with a construct called [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) which we’ll discuss
in more detail later:

```
>>> from sqlalchemy import text

>>> with engine.connect() as conn:
...     result = conn.execute(text("select 'hello world'"))
...     print(result.all())
BEGIN (implicit)
select 'hello world'
[...] ()
[('hello world',)]
ROLLBACK
```

In the example above, the context manager creates a database connection
and executes the operation in a transaction. The default behavior of
the Python DBAPI is that a transaction is always in progress; when the
connection is [released](https://docs.sqlalchemy.org/en/20/glossary.html#term-released), a ROLLBACK is emitted to end the
transaction.   The transaction is **not committed automatically**; if we want
to commit data we need to call [Connection.commit()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.commit)
as we’ll see in the next section.

Tip

“autocommit” mode is available for special cases.  The section
[Setting Transaction Isolation Levels including DBAPI Autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit) discusses this.

The result of our SELECT was returned in an object called
[Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) that will be discussed later. For the moment
we’ll add that it’s best to use this object within the “connect” block,
and to not use it outside of the scope of our connection.

## Committing Changes

We just learned that the DBAPI connection doesn’t commit automatically.
What if we want to commit some data?   We can change our example above to create a
table, insert some data and then commit the transaction using
the [Connection.commit()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.commit) method, **inside** the block
where we have the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object:

```
# "commit as you go"
>>> with engine.connect() as conn:
...     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
...     )
...     conn.commit()
BEGIN (implicit)
CREATE TABLE some_table (x int, y int)
[...] ()
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] [(1, 1), (2, 4)]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

Above, we execute two SQL statements, a “CREATE TABLE” statement [[1]](#id2)
and an “INSERT” statement that’s parameterized (we discuss the parameterization syntax
later in [Sending Multiple Parameters](#tutorial-multiple-parameters)).
To commit the work we’ve done in our block, we call the
[Connection.commit()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.commit) method which commits the transaction. After
this, we can continue to run more SQL statements and call [Connection.commit()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.commit)
again for those statements.  SQLAlchemy refers to this style as **commit as
you go**.

There’s also another style to commit data. We can declare
our “connect” block to be a transaction block up front.   To do this, we use the
[Engine.begin()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.begin) method to get the connection, rather than the
[Engine.connect()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.connect) method.  This method
will manage the scope of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and also
enclose everything inside of a transaction with either a COMMIT at the end
if the block was successful, or a ROLLBACK if an exception was raised.  This style
is known as **begin once**:

```
# "begin once"
>>> with engine.begin() as conn:
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
...     )
BEGIN (implicit)
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] [(6, 8), (9, 10)]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

You should mostly prefer the “begin once” style because it’s shorter and shows the
intention of the entire block up front.   However, in this tutorial we’ll
use “commit as you go” style as it’s more flexible for demonstration
purposes.

What’s “BEGIN (implicit)”?

You might have noticed the log line “BEGIN (implicit)” at the start of a
transaction block.  “implicit” here means that SQLAlchemy **did not
actually send any command** to the database; it just considers this to be
the start of the DBAPI’s implicit transaction.   You can register
[event hooks](https://docs.sqlalchemy.org/en/20/core/events.html#core-sql-events) to intercept this event, for example.

    [[1](#id1)]

[DDL](https://docs.sqlalchemy.org/en/20/glossary.html#term-DDL) refers to the subset of SQL that instructs the database
to create, modify, or remove schema-level constructs such as tables. DDL
such as “CREATE TABLE” should be in a transaction block that
ends with COMMIT, as many databases use transactional DDL such that the
schema changes don’t take place until the transaction is committed. However,
as we’ll see later, we usually let SQLAlchemy run DDL sequences for us as
part of a higher level operation where we don’t generally need to worry
about the COMMIT.

## Basics of Statement Execution

We have seen a few examples that run SQL statements against a database, making
use of a method called [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), in conjunction with
an object called [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text), and returning an object called
[Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result).  In this section we’ll illustrate more closely the
mechanics and interactions of these components.

Most of the content in this section applies equally well to modern ORM
use when using the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method, which works
very similarly to that of [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), including that
ORM result rows are delivered using the same [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)
interface used by Core.

### Fetching Rows

We’ll first illustrate the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object more closely by
making use of the rows we’ve inserted previously, running a textual SELECT
statement on the table we’ve created:

```
>>> with engine.connect() as conn:
...     result = conn.execute(text("SELECT x, y FROM some_table"))
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table
[...] ()
x: 1  y: 1
x: 2  y: 4
x: 6  y: 8
x: 9  y: 10
ROLLBACK
```

Above, the “SELECT” string we executed selected all rows from our table.
The object returned is called [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) and represents an
iterable object of result rows.

[Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) has lots of methods for
fetching and transforming rows, such as the [Result.all()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.all)
method illustrated previously, which returns a list of all [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
objects.   It also implements the Python iterator interface so that we can
iterate over the collection of [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects directly.

The [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects themselves are intended to act like Python
[named tuples](https://docs.python.org/3/library/collections.html#collections.namedtuple).
Below we illustrate a variety of ways to access rows.

- **Tuple Assignment** - This is the most Python-idiomatic style, which is to assign variables
  to each row positionally as they are received:
  ```
  result = conn.execute(text("select x, y from some_table"))
  for x, y in result:
      ...
  ```
- **Integer Index** - Tuples are Python sequences, so regular integer access is available too:
  ```
  result = conn.execute(text("select x, y from some_table"))
  for row in result:
      x = row[0]
  ```
- **Attribute Name** - As these are Python named tuples, the tuples have dynamic attribute names
  matching the names of each column.  These names are normally the names that the
  SQL statement assigns to the columns in each row.  While they are usually
  fairly predictable and can also be controlled by labels, in less defined cases
  they may be subject to database-specific behaviors:
  ```
  result = conn.execute(text("select x, y from some_table"))
  for row in result:
      y = row.y
      # illustrate use with Python f-strings
      print(f"Row: {row.x} {y}")
  ```
- **Mapping Access** - To receive rows as Python **mapping** objects, which is
  essentially a read-only version of Python’s interface to the common `dict`
  object, the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) may be **transformed** into a
  [MappingResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.MappingResult) object using the
  [Result.mappings()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.mappings) modifier; this is a result object that yields
  dictionary-like [RowMapping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.RowMapping) objects rather than
  [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects:
  ```
  result = conn.execute(text("select x, y from some_table"))
  for dict_row in result.mappings():
      x = dict_row["x"]
      y = dict_row["y"]
  ```

### Sending Parameters

SQL statements are usually accompanied by data that is to be passed with the
statement itself, as we saw in the INSERT example previously. The
[Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) method therefore also accepts parameters,
which are known as [bound parameters](https://docs.sqlalchemy.org/en/20/glossary.html#term-bound-parameters).  A rudimentary example
might be if we wanted to limit our SELECT statement only to rows that meet a
certain criteria, such as rows where the “y” value were greater than a certain
value that is passed in to a function.

In order to achieve this such that the SQL statement can remain fixed and
that the driver can properly sanitize the value, we add a WHERE criteria to
our statement that names a new parameter called “y”; the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
construct accepts these using a colon format “`:y`”.   The actual value for
“`:y`” is then passed as the second argument to
[Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) in the form of a dictionary:

```
>>> with engine.connect() as conn:
...     result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table WHERE y > ?
[...] (2,)
x: 2  y: 4
x: 6  y: 8
x: 9  y: 10
ROLLBACK
```

In the logged SQL output, we can see that the bound parameter `:y` was
converted into a question mark when it was sent to the SQLite database.
This is because the SQLite database driver uses a format called “qmark parameter style”,
which is one of six different formats allowed by the DBAPI specification.
SQLAlchemy abstracts these formats into just one, which is the “named” format
using a colon.

Always use bound parameters

As mentioned at the beginning of this section, textual SQL is not the usual
way we work with SQLAlchemy.  However, when using textual SQL, a Python
literal value, even non-strings like integers or dates, should **never be
stringified into SQL string directly**; a parameter should **always** be
used.  This is most famously known as how to avoid SQL injection attacks
when the data is untrusted.  However it also allows the SQLAlchemy dialects
and/or DBAPI to correctly handle the incoming input for the backend.
Outside of plain textual SQL use cases, SQLAlchemy’s Core Expression API
otherwise ensures that Python literal values are passed as bound parameters
where appropriate.

### Sending Multiple Parameters

In the example at [Committing Changes](#tutorial-committing-data), we executed an INSERT
statement where it appeared that we were able to INSERT multiple rows into the
database at once.  For [DML](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML) statements such as “INSERT”,
“UPDATE” and “DELETE”, we can send **multiple parameter sets** to the
[Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) method by passing a list of dictionaries
instead of a single dictionary, which indicates that the single SQL statement
should be invoked multiple times, once for each parameter set.  This style
of execution is known as [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany):

```
>>> with engine.connect() as conn:
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
...     )
...     conn.commit()
BEGIN (implicit)
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] [(11, 12), (13, 14)]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

The above operation is equivalent to running the given INSERT statement once
for each parameter set, except that the operation will be optimized for
better performance across many rows.

A key behavioral difference between “execute” and “executemany” is that the
latter doesn’t support returning of result rows, even if the statement includes
the RETURNING clause. The one exception to this is when using a Core
[insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct, introduced later in this tutorial at
[Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert), which also indicates RETURNING using the
[Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) method.  In that case, SQLAlchemy makes use of
special logic to reorganize the INSERT statement so that it can be invoked
for many rows while still supporting RETURNING.

See also

[executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany) - in the [Glossary](https://docs.sqlalchemy.org/en/20/glossary.html), describes the
DBAPI-level
[cursor.executemany()](https://peps.python.org/pep-0249/#executemany)
method that’s used for most “executemany” executions.

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) - in [Working with Engines and Connections](https://docs.sqlalchemy.org/en/20/core/connections.html), describes
the specialized logic used by [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) to deliver
result sets with “executemany” executions.

## Executing with an ORM Session

As mentioned previously, most of the patterns and examples above apply to
use with the ORM as well, so here we will introduce this usage so that
as the tutorial proceeds, we will be able to illustrate each pattern in
terms of Core and ORM use together.

The fundamental transactional / database interactive object when using the
ORM is called the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  In modern SQLAlchemy, this object
is used in a manner very similar to that of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection),
and in fact as the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is used, it refers to a
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) internally which it uses to emit SQL.

When the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is used with non-ORM constructs, it
passes through the SQL statements we give it and does not generally do things
much differently from how the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) does directly, so
we can illustrate it here in terms of the simple textual SQL
operations we’ve already learned.

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has a few different creational patterns, but
here we will illustrate the most basic one that tracks exactly with how
the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is used which is to construct it within
a context manager:

```
>>> from sqlalchemy.orm import Session

>>> stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
>>> with Session(engine) as session:
...     result = session.execute(stmt, {"y": 6})
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table WHERE y > ? ORDER BY x, y
[...] (6,)
x: 6  y: 8
x: 9  y: 10
x: 11  y: 12
x: 13  y: 14
ROLLBACK
```

The example above can be compared to the example in the preceding section
in [Sending Parameters](#tutorial-sending-parameters) - we directly replace the call to
`with engine.connect() as conn` with `with Session(engine) as session`,
and then make use of the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method just like we
do with the [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) method.

Also, like the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) features
“commit as you go” behavior using the [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) method,
illustrated below using a textual UPDATE statement to alter some of
our data:

```
>>> with Session(engine) as session:
...     result = session.execute(
...         text("UPDATE some_table SET y=:y WHERE x=:x"),
...         [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
...     )
...     session.commit()
BEGIN (implicit)
UPDATE some_table SET y=? WHERE x=?
[...] [(11, 9), (15, 13)]
COMMIT
```

Above, we invoked an UPDATE statement using the bound-parameter, “executemany”
style of execution introduced at [Sending Multiple Parameters](#tutorial-multiple-parameters), ending
the block with a “commit as you go” commit.

Tip

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) doesn’t actually hold onto the
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object after it ends the transaction.  It
gets a new [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) from the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
the next time it needs to execute SQL against the database.

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) obviously has a lot more tricks up its sleeve
than that, however understanding that it has a [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute)
method that’s used the same way as [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) will
get us started with the examples that follow later.

See also

[Basics of Using a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1) - presents basic creational and usage patterns with
the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: [Working with Database Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html)

---

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)   |   Next: [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html)

# Establishing Connectivity - the Engine

**Welcome ORM and Core readers alike!**

Every SQLAlchemy application that connects to a database needs to use
an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).  This short section is for everyone.

The start of any SQLAlchemy application is an object called the
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).   This object acts as a central source of connections
to a particular database, providing both a factory as well as a holding
space called a [connection pool](https://docs.sqlalchemy.org/en/20/core/pooling.html) for these database
connections.   The engine is typically a global object created just
once for a particular database server, and is configured using a URL string
which will describe how it should connect to the database host or backend.

For this tutorial we will use an in-memory-only SQLite database. This is an
easy way to test things without needing to have an actual pre-existing database
set up.  The [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) is created by using the
[create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) function:

```
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
```

The main argument to [create_engine](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
is a string URL, above passed as the string `"sqlite+pysqlite:///:memory:"`.
This string indicates to the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) three important
facts:

1. What kind of database are we communicating with?   This is the `sqlite`
  portion above, which links in SQLAlchemy to an object known as the
  [dialect](https://docs.sqlalchemy.org/en/20/glossary.html#term-dialect).
2. What [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) are we using?  The Python [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) is a third party
  driver that SQLAlchemy uses to interact with a particular database.  In
  this case, we’re using the name `pysqlite`, which in modern Python
  use is the [sqlite3](https://docs.python.org/library/sqlite3.html) standard
  library interface for SQLite. If omitted, SQLAlchemy will use a default
  [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) for the particular database selected.
3. How do we locate the database?   In this case, our URL includes the phrase
  `/:memory:`, which is an indicator to the `sqlite3` module that we
  will be using an **in-memory-only** database.   This kind of database
  is perfect for experimenting as it does not require any server nor does
  it need to create new files.

Lazy Connecting

The [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), when first returned by [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine),
has not actually tried to connect to the database yet; that happens
only the first time it is asked to perform a task against the database.
This is a software design pattern known as [lazy initialization](https://docs.sqlalchemy.org/en/20/glossary.html#term-lazy-initialization).

We have also specified a parameter [create_engine.echo](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo), which
will instruct the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) to log all of the SQL it emits to a
Python logger that will write to standard out.   This flag is a shorthand way
of setting up
[Python logging more formally](https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging) and is useful for
experimentation in scripts.   Many of the SQL examples will include this
SQL logging output beneath a `[SQL]` link that when clicked, will reveal
the full SQL interaction.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html)

---

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html)

# Further Reading

The sections below are the major top-level sections that discuss the concepts
in this tutorial in much more detail, as well as describe many more features
of each subsystem.

Core Essential Reference

- [Working with Engines and Connections](https://docs.sqlalchemy.org/en/20/core/connections.html)
- [Schema Definition Language](https://docs.sqlalchemy.org/en/20/core/schema.html)
- [SQL Statements and Expressions API](https://docs.sqlalchemy.org/en/20/core/expression_api.html)
- [SQL Datatype Objects](https://docs.sqlalchemy.org/en/20/core/types.html)

ORM Essential Reference

- [ORM Mapped Class Configuration](https://docs.sqlalchemy.org/en/20/orm/mapper_config.html)
- [Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- [Using the Session](https://docs.sqlalchemy.org/en/20/orm/session.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

---

# SQLAlchemy 2.0 Documentation

# SQLAlchemy Unified Tutorial

About this document

The SQLAlchemy Unified Tutorial is integrated between the Core and ORM
components of SQLAlchemy and serves as a unified introduction to SQLAlchemy
as a whole. For users of SQLAlchemy within the 1.x series, in the
[2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) of working, the ORM uses Core-style querying with the
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct, and transactional semantics between Core
connections and ORM sessions are equivalent. Take note of the blue border
styles for each section, that will tell you how “ORM-ish” a particular
topic is!

Users who are already familiar with SQLAlchemy, and especially those
looking to migrate existing applications to work under the SQLAlchemy 2.0
series within the 1.4 transitional phase should check out the
[SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html) document as well.

For the newcomer, this document has a **lot** of detail, however by the
end they will be considered an **Alchemist**.

SQLAlchemy is presented as two distinct APIs, one building on top of the other.
These APIs are known as **Core** and **ORM**.

**SQLAlchemy Core** is the foundational architecture for SQLAlchemy as a
“database toolkit”.  The library provides tools for managing connectivity
to a database, interacting with database queries and results, and
programmatic construction of SQL statements.

Sections that are **primarily Core-only** will not refer to the ORM.
SQLAlchemy constructs used in these sections will be imported from the
`sqlalchemy` namespace. As an additional indicator of subject
classification, they will also include a **dark blue border on the right**.
When using the ORM, these concepts are still in play but are less often
explicit in user code. ORM users should read these sections, but not expect
to be using these APIs directly for ORM-centric code.

**SQLAlchemy ORM** builds upon the Core to provide optional **object
relational mapping** capabilities.   The ORM provides an additional
configuration layer allowing user-defined Python classes to be **mapped**
to database tables and other constructs, as well as an object persistence
mechanism known as the **Session**.   It then extends the Core-level
SQL Expression Language to allow SQL queries to be composed and invoked
in terms of user-defined objects.

Sections that are **primarily ORM-only** should be **titled to
include the phrase “ORM”**, so that it’s clear this is an ORM related topic.
SQLAlchemy constructs used in these sections will be imported from the
`sqlalchemy.orm` namespace. Finally, as an additional indicator of
subject classification, they will also include a **light blue border on the
left**. Core-only users can skip these.

**Most** sections in this tutorial discuss **Core concepts that
are also used explicitly with the ORM**. SQLAlchemy 2.0 in particular
features a much greater level of integration of Core API use within the
ORM.

For each of these sections, there will be **introductory text** discussing the
degree to which ORM users should expect to be using these programming
patterns. SQLAlchemy constructs in these sections will be imported from the
`sqlalchemy` namespace with some potential use of `sqlalchemy.orm`
constructs at the same time. As an additional indicator of subject
classification, these sections will also include **both a thinner light
border on the left, and a thicker dark border on the right**. Core and ORM
users should familiarize with concepts in these sections equally.

## Tutorial Overview

The tutorial will present both concepts in the natural order that they
should be learned, first with a mostly-Core-centric approach and then
spanning out into more ORM-centric concepts.

The major sections of this tutorial are as follows:

- [Establishing Connectivity - the Engine](https://docs.sqlalchemy.org/en/20/tutorial/engine.html#tutorial-engine) - all SQLAlchemy applications start with an
  [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object; here’s how to create one.
- [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-working-with-transactions) - the usage API of the
  [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) and its related objects [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
  and [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) are presented here. This content is Core-centric
  however ORM users will want to be familiar with at least the
  [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object.
- [Working with Database Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata) - SQLAlchemy’s SQL abstractions as well
  as the ORM rely upon a system of defining database schema constructs as
  Python objects.   This section introduces how to do that from both a Core and
  an ORM perspective.
- [Working with Data](https://docs.sqlalchemy.org/en/20/tutorial/data.html#tutorial-working-with-data) - here we learn how to create, select,
  update and delete data in the database.   The so-called [CRUD](https://docs.sqlalchemy.org/en/20/glossary.html#term-CRUD)
  operations here are given in terms of SQLAlchemy Core with links out towards
  their ORM counterparts.  The SELECT operation that is introduced in detail at
  [Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-data) applies equally well to Core and ORM.
- [Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation) covers the persistence framework of the
  ORM; basically the ORM-centric ways to insert, update and delete, as well as
  how to handle transactions.
- [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects) introduces the concept of the
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct and provides a brief overview
  of how it’s used, with links to deeper documentation.
- [Further Reading](https://docs.sqlalchemy.org/en/20/tutorial/further_reading.html#tutorial-further-reading) lists a series of major top-level
  documentation sections which fully document the concepts introduced in this
  tutorial.

### Version Check

This tutorial is written using a system called [doctest](https://docs.python.org/3/library/doctest.html). All of the code excerpts
written with a `>>>` are actually run as part of SQLAlchemy’s test suite, and
the reader is invited to work with the code examples given in real time with
their own Python interpreter.

If running the examples, it is advised that the reader performs a quick check to
verify that we are on  **version 2.0** of SQLAlchemy:

```
>>> import sqlalchemy
>>> sqlalchemy.__version__
2.0.0
```

SQLAlchemy Unified Tutorial

Next Section: [Establishing Connectivity - the Engine](https://docs.sqlalchemy.org/en/20/tutorial/engine.html)
