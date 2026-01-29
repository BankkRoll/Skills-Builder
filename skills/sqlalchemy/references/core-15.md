# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Operator Reference

This section details usage of the operators that are available
to construct SQL expressions.

These methods are presented in terms of the [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)
and [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators) base classes.   The methods are then
available on descendants of these classes, including:

- [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
- [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects more generally, which are the root
  of all Core SQL Expression language column-level expressions
- [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute) objects, which are ORM
  level mapped attributes.

The operators are first introduced in the tutorial sections, including:

- [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html) - unified tutorial in [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style)
- [Object Relational Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html) - ORM tutorial in [1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style)
- [SQL Expression Language Tutorial](https://docs.sqlalchemy.org/en/20/core/tutorial.html) - Core tutorial in [1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style)

## Comparison Operators

Basic comparisons which apply to many datatypes, including numerics,
strings, dates, and many others:

- [ColumnOperators.__eq__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__eq__) (Python “`==`” operator):
  ```
  >>> print(column("x") == 5)
  x = :x_1
  ```
- [ColumnOperators.__ne__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__ne__) (Python “`!=`” operator):
  ```
  >>> print(column("x") != 5)
  x != :x_1
  ```
- [ColumnOperators.__gt__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__gt__) (Python “`>`” operator):
  ```
  >>> print(column("x") > 5)
  x > :x_1
  ```
- [ColumnOperators.__lt__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__lt__) (Python “`<`” operator):
  ```
  >>> print(column("x") < 5)
  x < :x_1
  ```
- [ColumnOperators.__ge__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__ge__) (Python “`>=`” operator):
  ```
  >>> print(column("x") >= 5)
  x >= :x_1
  ```
- [ColumnOperators.__le__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__le__) (Python “`<=`” operator):
  ```
  >>> print(column("x") <= 5)
  x <= :x_1
  ```
- [ColumnOperators.between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.between):
  ```
  >>> print(column("x").between(5, 10))
  x BETWEEN :x_1 AND :x_2
  ```

## IN Comparisons

The SQL IN operator is a subject all its own in SQLAlchemy.   As the IN
operator is usually used against a list of fixed values, SQLAlchemy’s
feature of bound parameter coercion makes use of a special form of SQL
compilation that renders an interim SQL string for compilation that’s formed
into the final list of bound parameters in a second step.   In other words,
“it just works”.

### IN against a list of values

IN is available most typically by passing a list of
values to the [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) method:

```
>>> print(column("x").in_([1, 2, 3]))
x IN (__[POSTCOMPILE_x_1])
```

The special bound form `__[POSTCOMPILE` is rendered into individual parameters
at execution time, illustrated below:

```
>>> stmt = select(User.id).where(User.id.in_([1, 2, 3]))
>>> result = conn.execute(stmt)
SELECT user_account.id
FROM user_account
WHERE user_account.id IN (?, ?, ?)
[...] (1, 2, 3)
```

### Empty IN Expressions

SQLAlchemy produces a mathematically valid result for an empty IN expression
by rendering a backend-specific subquery that returns no rows.   Again
in other words, “it just works”:

```
>>> stmt = select(User.id).where(User.id.in_([]))
>>> result = conn.execute(stmt)
SELECT user_account.id
FROM user_account
WHERE user_account.id IN (SELECT 1 FROM (SELECT 1) WHERE 1!=1)
[...] ()
```

The “empty set” subquery above generalizes correctly and is also rendered
in terms of the IN operator which remains in place.

### NOT IN

“NOT IN” is available via the [ColumnOperators.not_in()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_in) operator:

```
>>> print(column("x").not_in([1, 2, 3]))
(x NOT IN (__[POSTCOMPILE_x_1]))
```

This is typically more easily available by negating with the `~` operator:

```
>>> print(~column("x").in_([1, 2, 3]))
(x NOT IN (__[POSTCOMPILE_x_1]))
```

### Tuple IN Expressions

Comparison of tuples to tuples is common with IN, as among other use cases
accommodates for the case when matching rows to a set of potential composite
primary key values.  The [tuple_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.tuple_) construct provides the basic
building block for tuple comparisons.  The `Tuple.in_()` operator
then receives a list of tuples:

```
>>> from sqlalchemy import tuple_
>>> tup = tuple_(column("x", Integer), column("y", Integer))
>>> expr = tup.in_([(1, 2), (3, 4)])
>>> print(expr)
(x, y) IN (__[POSTCOMPILE_param_1])
```

To illustrate the parameters rendered:

```
>>> tup = tuple_(User.id, Address.id)
>>> stmt = select(User.name).join(Address).where(tup.in_([(1, 1), (2, 2)]))
>>> conn.execute(stmt).all()
SELECT user_account.name
FROM user_account JOIN address ON user_account.id = address.user_id
WHERE (user_account.id, address.id) IN (VALUES (?, ?), (?, ?))
[...] (1, 1, 2, 2)
[('spongebob',), ('sandy',)]
```

### Subquery IN

Finally, the [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) and [ColumnOperators.not_in()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_in)
operators work with subqueries.   The form provides that a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
construct is passed in directly, without any explicit conversion to a named
subquery:

```
>>> print(column("x").in_(select(user_table.c.id)))
x IN (SELECT user_account.id
FROM user_account)
```

Tuples work as expected:

```
>>> print(
...     tuple_(column("x"), column("y")).in_(
...         select(user_table.c.id, address_table.c.id).join(address_table)
...     )
... )
(x, y) IN (SELECT user_account.id, address.id
FROM user_account JOIN address ON user_account.id = address.user_id)
```

## Identity Comparisons

These operators involve testing for special SQL values such as
`NULL`, boolean constants such as `true` or `false` which some
databases support:

- [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_):
  This operator will provide exactly the SQL for “x IS y”, most often seen
  as “<expr> IS NULL”.   The `NULL` constant is most easily acquired
  using regular Python `None`:
  ```
  >>> print(column("x").is_(None))
  x IS NULL
  ```
  SQL NULL is also explicitly available, if needed, using the
  [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) construct:
  ```
  >>> from sqlalchemy import null
  >>> print(column("x").is_(null()))
  x IS NULL
  ```
  The [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_) operator is automatically invoked when
  using the [ColumnOperators.__eq__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__eq__) overloaded operator, i.e.
  `==`, in conjunction with the `None` or [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) value. In this
  way, there’s typically not a need to use [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_)
  explicitly, particularly when used with a dynamic value:
  ```
  >>> a = None
  >>> print(column("x") == a)
  x IS NULL
  ```
  Note that the Python `is` operator is **not overloaded**.  Even though
  Python provides hooks to overload operators such as `==` and `!=`,
  it does **not** provide any way to redefine `is`.
- [ColumnOperators.is_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not):
  Similar to [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_), produces “IS NOT”:
  ```
  >>> print(column("x").is_not(None))
  x IS NOT NULL
  ```
  Is similarly equivalent to `!= None`:
  ```
  >>> print(column("x") != None)
  x IS NOT NULL
  ```
- [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from):
  Produces SQL IS DISTINCT FROM:
  ```
  >>> print(column("x").is_distinct_from("some value"))
  x IS DISTINCT FROM :x_1
  ```
- [ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from):
  Produces SQL IS NOT DISTINCT FROM:
  ```
  >>> print(column("x").isnot_distinct_from("some value"))
  x IS NOT DISTINCT FROM :x_1
  ```

## String Comparisons

- [ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like):
  ```
  >>> print(column("x").like("word"))
  x LIKE :x_1
  ```
- [ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike):
  Case insensitive LIKE makes use of the SQL `lower()` function on a
  generic backend.  On the PostgreSQL backend it will use `ILIKE`:
  ```
  >>> print(column("x").ilike("word"))
  lower(x) LIKE lower(:x_1)
  ```
- [ColumnOperators.notlike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notlike):
  ```
  >>> print(column("x").notlike("word"))
  x NOT LIKE :x_1
  ```
- [ColumnOperators.notilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notilike):
  ```
  >>> print(column("x").notilike("word"))
  lower(x) NOT LIKE lower(:x_1)
  ```

## String Containment

String containment operators are basically built as a combination of
LIKE and the string concatenation operator, which is `||` on most
backends or sometimes a function like `concat()`:

- [ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith):
  ```
  >>> print(column("x").startswith("word"))
  x LIKE :x_1 || '%'
  ```
- [ColumnOperators.endswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith):
  ```
  >>> print(column("x").endswith("word"))
  x LIKE '%' || :x_1
  ```
- [ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains):
  ```
  >>> print(column("x").contains("word"))
  x LIKE '%' || :x_1 || '%'
  ```

## String matching

Matching operators are always backend-specific and may provide different
behaviors and results on different databases:

- [ColumnOperators.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.match):
  This is a dialect-specific operator that makes use of the MATCH
  feature of the underlying database, if available:
  ```
  >>> print(column("x").match("word"))
  x MATCH :x_1
  ```
- [ColumnOperators.regexp_match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_match):
  This operator is dialect specific.  We can illustrate it in terms of
  for example the PostgreSQL dialect:
  ```
  >>> from sqlalchemy.dialects import postgresql
  >>> print(column("x").regexp_match("word").compile(dialect=postgresql.dialect()))
  x ~ %(x_1)s
  ```
  Or MySQL:
  ```
  >>> from sqlalchemy.dialects import mysql
  >>> print(column("x").regexp_match("word").compile(dialect=mysql.dialect()))
  x REGEXP %s
  ```

## String Alteration

- [ColumnOperators.concat()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.concat):
  String concatenation:
  ```
  >>> print(column("x").concat("some string"))
  x || :x_1
  ```
  This operator is available via [ColumnOperators.__add__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__add__), that
  is, the Python `+` operator, when working with a column expression that
  derives from [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String):
  ```
  >>> print(column("x", String) + "some string")
  x || :x_1
  ```
  The operator will produce the appropriate database-specific construct,
  such as on MySQL it’s historically been the `concat()` SQL function:
  ```
  >>> print((column("x", String) + "some string").compile(dialect=mysql.dialect()))
  concat(x, %s)
  ```
- [ColumnOperators.regexp_replace()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_replace):
  Complementary to `ColumnOperators.regexp()` this produces REGEXP
  REPLACE equivalent for the backends which support it:
  ```
  >>> print(column("x").regexp_replace("foo", "bar").compile(dialect=postgresql.dialect()))
  REGEXP_REPLACE(x, %(x_1)s, %(x_2)s)
  ```
- [ColumnOperators.collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.collate):
  Produces the COLLATE SQL operator which provides for specific collations
  at expression time:
  ```
  >>> print(
  ...     (column("x").collate("latin1_german2_ci") == "Müller").compile(
  ...         dialect=mysql.dialect()
  ...     )
  ... )
  (x COLLATE latin1_german2_ci) = %s
  ```
  To use COLLATE against a literal value, use the [literal()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal) construct:
  ```
  >>> from sqlalchemy import literal
  >>> print(
  ...     (literal("Müller").collate("latin1_german2_ci") == column("x")).compile(
  ...         dialect=mysql.dialect()
  ...     )
  ... )
  (%s COLLATE latin1_german2_ci) = x
  ```

## Arithmetic Operators

- [ColumnOperators.__add__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__add__), [ColumnOperators.__radd__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__radd__) (Python “`+`” operator):
  ```
  >>> print(column("x") + 5)
  x + :x_1
  >>> print(5 + column("x"))
  :x_1 + x
  ```
  Note that when the datatype of the expression is [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)
  or similar, the [ColumnOperators.__add__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__add__) operator instead produces
  [string concatenation](#queryguide-operators-concat-op).
- [ColumnOperators.__sub__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__sub__), [ColumnOperators.__rsub__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__rsub__) (Python “`-`” operator):
  ```
  >>> print(column("x") - 5)
  x - :x_1
  >>> print(5 - column("x"))
  :x_1 - x
  ```
- [ColumnOperators.__mul__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__mul__), [ColumnOperators.__rmul__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__rmul__) (Python “`*`” operator):
  ```
  >>> print(column("x") * 5)
  x * :x_1
  >>> print(5 * column("x"))
  :x_1 * x
  ```
- [ColumnOperators.__truediv__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__truediv__), [ColumnOperators.__rtruediv__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__rtruediv__) (Python “`/`” operator).
  This is the Python `truediv` operator, which will ensure integer true division occurs:
  ```
  >>> print(column("x") / 5)
  x / CAST(:x_1 AS NUMERIC)
  >>> print(5 / column("x"))
  :x_1 / CAST(x AS NUMERIC)
  ```
  Changed in version 2.0: The Python `/` operator now ensures integer true division takes place
- [ColumnOperators.__floordiv__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__floordiv__), [ColumnOperators.__rfloordiv__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__rfloordiv__) (Python “`//`” operator).
  This is the Python `floordiv` operator, which will ensure floor division occurs.
  For the default backend as well as backends such as PostgreSQL, the SQL `/` operator normally
  behaves this way for integer values:
  ```
  >>> print(column("x") // 5)
  x / :x_1
  >>> print(5 // column("x", Integer))
  :x_1 / x
  ```
  For backends that don’t use floor division by default, or when used with numeric values,
  the FLOOR() function is used to ensure floor division:
  ```
  >>> print(column("x") // 5.5)
  FLOOR(x / :x_1)
  >>> print(5 // column("x", Numeric))
  FLOOR(:x_1 / x)
  ```
  Added in version 2.0: Support for FLOOR division
- [ColumnOperators.__mod__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__mod__), [ColumnOperators.__rmod__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__rmod__) (Python “`%`” operator):
  ```
  >>> print(column("x") % 5)
  x % :x_1
  >>> print(5 % column("x"))
  :x_1 % x
  ```

## Bitwise Operators

Bitwise operator functions provide uniform access to bitwise operators across
different backends, which are expected to operate on compatible
values such as integers and bit-strings (e.g. PostgreSQL
[BIT](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.BIT) and similar). Note that these are **not** general
boolean operators.

Added in version 2.0.2: Added dedicated operators for bitwise operations.

- [ColumnOperators.bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_not), [bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bitwise_not).
  Available as a column-level method, producing a bitwise NOT clause against a
  parent object:
  ```
  >>> print(column("x").bitwise_not())
  ~x
  ```
  This operator is also available as a column-expression-level method, applying
  bitwise NOT to an individual column expression:
  ```
  >>> from sqlalchemy import bitwise_not
  >>> print(bitwise_not(column("x")))
  ~x
  ```
- [ColumnOperators.bitwise_and()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_and) produces bitwise AND:
  ```
  >>> print(column("x").bitwise_and(5))
  x & :x_1
  ```
- [ColumnOperators.bitwise_or()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_or) produces bitwise OR:
  ```
  >>> print(column("x").bitwise_or(5))
  x | :x_1
  ```
- [ColumnOperators.bitwise_xor()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_xor) produces bitwise XOR:
  ```
  >>> print(column("x").bitwise_xor(5))
  x ^ :x_1
  ```
  For PostgreSQL dialects, “#” is used to represent bitwise XOR; this emits
  automatically when using one of these backends:
  ```
  >>> from sqlalchemy.dialects import postgresql
  >>> print(column("x").bitwise_xor(5).compile(dialect=postgresql.dialect()))
  x # %(x_1)s
  ```
- [ColumnOperators.bitwise_rshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_rshift), [ColumnOperators.bitwise_lshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_lshift)
  produce bitwise shift operators:
  ```
  >>> print(column("x").bitwise_rshift(5))
  x >> :x_1
  >>> print(column("x").bitwise_lshift(5))
  x << :x_1
  ```

## Using Conjunctions and Negations

The most common conjunction, “AND”, is automatically applied if we make repeated use of the [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where) method, as well as similar methods such as
[Update.where()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.where) and [Delete.where()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete.where):

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

[Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where), [Update.where()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.where) and [Delete.where()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete.where) also accept multiple expressions with the same effect:

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

The “AND” conjunction, as well as its partner “OR”, are both available directly using the [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) and [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) functions:

```
>>> from sqlalchemy import and_, or_
>>> print(
...     select(address_table.c.email_address).where(
...         and_(
...             or_(user_table.c.name == "squidward", user_table.c.name == "sandy"),
...             address_table.c.user_id == user_table.c.id,
...         )
...     )
... )
SELECT address.email_address
FROM address, user_account
WHERE (user_account.name = :name_1 OR user_account.name = :name_2)
AND address.user_id = user_account.id
```

A negation is available using the [not_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.not_) function.  This will
typically invert the operator in a boolean expression:

```
>>> from sqlalchemy import not_
>>> print(not_(column("x") == 5))
x != :x_1
```

It also may apply a keyword such as `NOT` when appropriate:

```
>>> from sqlalchemy import Boolean
>>> print(not_(column("x", Boolean)))
NOT x
```

## Conjunction Operators

The above conjunction functions [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_), [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_),
[not_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.not_) are also available as overloaded Python operators:

Note

The Python `&`, `|` and `~` operators take high precedence
in the language; as a result, parenthesis must usually be applied
for operands that themselves contain expressions, as indicated in the
examples below.

- [Operators.__and__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__and__) (Python “`&`” operator):
  The Python binary `&` operator is overloaded to behave the same
  as [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) (note parenthesis around the two operands):
  ```
  >>> print((column("x") == 5) & (column("y") == 10))
  x = :x_1 AND y = :y_1
  ```
- [Operators.__or__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__or__) (Python “`|`” operator):
  The Python binary `|` operator is overloaded to behave the same
  as [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) (note parenthesis around the two operands):
  ```
  >>> print((column("x") == 5) | (column("y") == 10))
  x = :x_1 OR y = :y_1
  ```
- [Operators.__invert__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__invert__) (Python “`~`” operator):
  The Python binary `~` operator is overloaded to behave the same
  as [not_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.not_), either inverting the existing operator, or
  applying the `NOT` keyword to the expression as a whole:
  ```
  >>> print(~(column("x") == 5))
  x != :x_1
  >>> from sqlalchemy import Boolean
  >>> print(~column("x", Boolean))
  NOT x
  ```

## Parentheses and Grouping

Parenthesization of expressions is rendered based on operator precedence,
not the placement of parentheses in Python code, since there is no means of
detecting parentheses from interpreted Python expressions.  So an expression
like:

```
>>> expr = or_(
...     User.name == "squidward", and_(Address.user_id == User.id, User.name == "sandy")
... )
```

won’t include parentheses, because the AND operator takes natural precedence over OR:

```
>>> print(expr)
user_account.name = :name_1 OR address.user_id = user_account.id AND user_account.name = :name_2
```

Whereas this one, where OR would otherwise not be evaluated before the AND, does:

```
>>> expr = and_(
...     Address.user_id == User.id, or_(User.name == "squidward", User.name == "sandy")
... )
>>> print(expr)
address.user_id = user_account.id AND (user_account.name = :name_1 OR user_account.name = :name_2)
```

The same behavior takes effect for math operators.  In the parenthesized
Python expression below, the multiplication operator naturally takes precedence over
the addition operator, therefore the SQL will not include parentheses:

```
>>> print(column("q") + (column("x") * column("y")))
q + x * y
```

Whereas this one, where the addition operator would not otherwise occur before
the multiplication operator, does get parentheses:

```
>>> print(column("q") * (column("x") + column("y")))
q * (x + y)
```

More background on this is in the FAQ at [Why are the parentheses rules like this?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-paren-rules).
