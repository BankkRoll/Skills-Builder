# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Column Elements and Expressions

The expression API consists of a series of classes each of which represents a
specific lexical element within a SQL string.  Composed together
into a larger structure, they form a statement construct that may
be *compiled* into a string representation that can be passed to a database.
The classes are organized into a hierarchy that begins at the basemost
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) class. Key subclasses include [ColumnElement](#sqlalchemy.sql.expression.ColumnElement),
which represents the role of any column-based expression
in a SQL statement, such as in the columns clause, WHERE clause, and ORDER BY
clause, and [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause), which represents the role of a token that
is placed in the FROM clause of a SELECT statement.

## Column Element Foundational Constructors

Standalone functions imported from the `sqlalchemy` namespace which are
used when building up SQLAlchemy Expression Language constructs.

| Object Name | Description |
| --- | --- |
| and_(*clauses) | Produce a conjunction of expressions joined byAND. |
| bindparam(key[, value, type_, unique, ...]) | Produce a “bound expression”. |
| bitwise_not(expr) | Produce a unary bitwise NOT clause, typically via the~operator. |
| case(*whens, [value, else_]) | Produce aCASEexpression. |
| cast(expression, type_) | Produce aCASTexpression. |
| column(text[, type_, is_literal, _selectable]) | Produce aColumnClauseobject. |
| custom_op | Represent a ‘custom’ operator. |
| distinct(expr) | Produce an column-expression-level unaryDISTINCTclause. |
| extract(field, expr) | Return aExtractconstruct. |
| false() | Return aFalse_construct. |
| func | Generate SQL function expressions. |
| lambda_stmt(lmb[, enable_tracking, track_closure_variables, track_on, ...]) | Produce a SQL statement that is cached as a lambda. |
| literal(value[, type_, literal_execute]) | Return a literal clause, bound to a bind parameter. |
| literal_column(text[, type_]) | Produce aColumnClauseobject that has thecolumn.is_literalflag set to True. |
| not_(clause) | Return a negation of the given clause, i.e.NOT(clause). |
| null() | Return a constantNullconstruct. |
| or_(*clauses) | Produce a conjunction of expressions joined byOR. |
| outparam(key[, type_]) | Create an ‘OUT’ parameter for usage in functions (stored procedures),
for databases which support them. |
| quoted_name | Represent a SQL identifier combined with quoting preferences. |
| text(text) | Construct a newTextClauseclause,
representing
a textual SQL string directly. |
| true() | Return a constantTrue_construct. |
| try_cast(expression, type_) | Produce aTRY_CASTexpression for backends which support it;
this is aCASTwhich returns NULL for un-castable conversions. |
| tuple_(*clauses, [types]) | Return aTuple. |
| type_coerce(expression, type_) | Associate a SQL expression with a particular type, without renderingCAST. |

   function sqlalchemy.sql.expression.and_(**clauses*)

Produce a conjunction of expressions joined by `AND`.

E.g.:

```
from sqlalchemy import and_

stmt = select(users_table).where(
    and_(users_table.c.name == "wendy", users_table.c.enrolled == True)
)
```

The [and_()](#sqlalchemy.sql.expression.and_) conjunction is also available using the
Python `&` operator (though note that compound expressions
need to be parenthesized in order to function with Python
operator precedence behavior):

```
stmt = select(users_table).where(
    (users_table.c.name == "wendy") & (users_table.c.enrolled == True)
)
```

The [and_()](#sqlalchemy.sql.expression.and_) operation is also implicit in some cases;
the [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where)
method for example can be invoked multiple
times against a statement, which will have the effect of each
clause being combined using [and_()](#sqlalchemy.sql.expression.and_):

```
stmt = (
    select(users_table)
    .where(users_table.c.name == "wendy")
    .where(users_table.c.enrolled == True)
)
```

The [and_()](#sqlalchemy.sql.expression.and_) construct must be given at least one positional
argument in order to be valid; a [and_()](#sqlalchemy.sql.expression.and_) construct with no
arguments is ambiguous.   To produce an “empty” or dynamically
generated [and_()](#sqlalchemy.sql.expression.and_)  expression, from a given list of expressions,
a “default” element of [true()](#sqlalchemy.sql.expression.true) (or just `True`) should be
specified:

```
from sqlalchemy import true

criteria = and_(true(), *expressions)
```

The above expression will compile to SQL as the expression `true`
or `1 = 1`, depending on backend, if no other expressions are
present.  If expressions are present, then the [true()](#sqlalchemy.sql.expression.true) value
is ignored as it does not affect the outcome of an AND expression that
has other elements.

Deprecated since version 1.4: The [and_()](#sqlalchemy.sql.expression.and_) element now requires that at
least one argument is passed; creating the [and_()](#sqlalchemy.sql.expression.and_) construct
with no arguments is deprecated, and will emit a deprecation warning
while continuing to produce a blank SQL string.

See also

[or_()](#sqlalchemy.sql.expression.or_)

     function sqlalchemy.sql.expression.bindparam(*key:str|None*, *value:Any=_NoArg.NO_ARG*, *type_:_TypeEngineArgument[_T]|None=None*, *unique:bool=False*, *required:bool|Literal[_NoArg.NO_ARG]=_NoArg.NO_ARG*, *quote:bool|None=None*, *callable_:Callable[[],Any]|None=None*, *expanding:bool=False*, *isoutparam:bool=False*, *literal_execute:bool=False*) → [BindParameter](#sqlalchemy.sql.expression.BindParameter)[_T]

Produce a “bound expression”.

The return value is an instance of [BindParameter](#sqlalchemy.sql.expression.BindParameter); this
is a [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
subclass which represents a so-called
“placeholder” value in a SQL expression, the value of which is
supplied at the point at which the statement in executed against a
database connection.

In SQLAlchemy, the [bindparam()](#sqlalchemy.sql.expression.bindparam) construct has
the ability to carry along the actual value that will be ultimately
used at expression time.  In this way, it serves not just as
a “placeholder” for eventual population, but also as a means of
representing so-called “unsafe” values which should not be rendered
directly in a SQL statement, but rather should be passed along
to the [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) as values which need to be correctly escaped
and potentially handled for type-safety.

When using [bindparam()](#sqlalchemy.sql.expression.bindparam) explicitly, the use case is typically
one of traditional deferment of parameters; the [bindparam()](#sqlalchemy.sql.expression.bindparam)
construct accepts a name which can then be referred to at execution
time:

```
from sqlalchemy import bindparam

stmt = select(users_table).where(
    users_table.c.name == bindparam("username")
)
```

The above statement, when rendered, will produce SQL similar to:

```
SELECT id, name FROM user WHERE name = :username
```

In order to populate the value of `:username` above, the value
would typically be applied at execution time to a method
like [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute):

```
result = connection.execute(stmt, {"username": "wendy"})
```

Explicit use of [bindparam()](#sqlalchemy.sql.expression.bindparam) is also common when producing
UPDATE or DELETE statements that are to be invoked multiple times,
where the WHERE criterion of the statement is to change on each
invocation, such as:

```
stmt = (
    users_table.update()
    .where(user_table.c.name == bindparam("username"))
    .values(fullname=bindparam("fullname"))
)

connection.execute(
    stmt,
    [
        {"username": "wendy", "fullname": "Wendy Smith"},
        {"username": "jack", "fullname": "Jack Jones"},
    ],
)
```

SQLAlchemy’s Core expression system makes wide use of
[bindparam()](#sqlalchemy.sql.expression.bindparam) in an implicit sense.   It is typical that Python
literal values passed to virtually all SQL expression functions are
coerced into fixed [bindparam()](#sqlalchemy.sql.expression.bindparam) constructs.  For example, given
a comparison operation such as:

```
expr = users_table.c.name == "Wendy"
```

The above expression will produce a [BinaryExpression](#sqlalchemy.sql.expression.BinaryExpression)
construct, where the left side is the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object
representing the `name` column, and the right side is a
[BindParameter](#sqlalchemy.sql.expression.BindParameter) representing the literal value:

```
print(repr(expr.right))
BindParameter("%(4327771088 name)s", "Wendy", type_=String())
```

The expression above will render SQL such as:

```
user.name = :name_1
```

Where the `:name_1` parameter name is an anonymous name.  The
actual string `Wendy` is not in the rendered string, but is carried
along where it is later used within statement execution.  If we
invoke a statement like the following:

```
stmt = select(users_table).where(users_table.c.name == "Wendy")
result = connection.execute(stmt)
```

We would see SQL logging output as:

```
SELECT "user".id, "user".name
FROM "user"
WHERE "user".name = %(name_1)s
{'name_1': 'Wendy'}
```

Above, we see that `Wendy` is passed as a parameter to the database,
while the placeholder `:name_1` is rendered in the appropriate form
for the target database, in this case the PostgreSQL database.

Similarly, [bindparam()](#sqlalchemy.sql.expression.bindparam) is invoked automatically when working
with [CRUD](https://docs.sqlalchemy.org/en/20/glossary.html#term-CRUD) statements as far as the “VALUES” portion is
concerned.   The [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct produces an
`INSERT` expression which will, at statement execution time, generate
bound placeholders based on the arguments passed, as in:

```
stmt = users_table.insert()
result = connection.execute(stmt, {"name": "Wendy"})
```

The above will produce SQL output as:

```
INSERT INTO "user" (name) VALUES (%(name)s)
{'name': 'Wendy'}
```

The [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct, at
compilation/execution time, rendered a single [bindparam()](#sqlalchemy.sql.expression.bindparam)
mirroring the column name `name` as a result of the single `name`
parameter we passed to the [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) method.

  Parameters:

- **key** –
  the key (e.g. the name) for this bind param.
  Will be used in the generated
  SQL statement for dialects that use named parameters.  This
  value may be modified when part of a compilation operation,
  if other [BindParameter](#sqlalchemy.sql.expression.BindParameter) objects exist with the same
  key, or if its length is too long and truncation is
  required.
  If omitted, an “anonymous” name is generated for the bound parameter;
  when given a value to bind, the end result is equivalent to calling upon
  the [literal()](#sqlalchemy.sql.expression.literal) function with a value to bind, particularly
  if the [bindparam.unique](#sqlalchemy.sql.expression.bindparam.params.unique) parameter is also provided.
- **value** – Initial value for this bind param.  Will be used at statement
  execution time as the value for this parameter passed to the
  DBAPI, if no other value is indicated to the statement execution
  method for this particular parameter name.  Defaults to `None`.
- **callable_** – A callable function that takes the place of “value”.  The function
  will be called at statement execution time to determine the
  ultimate value.   Used for scenarios where the actual bind
  value cannot be determined at the point at which the clause
  construct is created, but embedded bind values are still desirable.
- **type_** –
  A [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or instance representing an optional
  datatype for this [bindparam()](#sqlalchemy.sql.expression.bindparam).  If not passed, a type
  may be determined automatically for the bind, based on the given
  value; for example, trivial Python types such as `str`,
  `int`, `bool`
  may result in the [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String), [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) or
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) types being automatically selected.
  The type of a [bindparam()](#sqlalchemy.sql.expression.bindparam) is significant especially in that
  the type will apply pre-processing to the value before it is
  passed to the database.  For example, a [bindparam()](#sqlalchemy.sql.expression.bindparam) which
  refers to a datetime value, and is specified as holding the
  [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime) type, may apply conversion needed to the
  value (such as stringification on SQLite) before passing the value
  to the database.
- **unique** – if True, the key name of this [BindParameter](#sqlalchemy.sql.expression.BindParameter) will be
  modified if another [BindParameter](#sqlalchemy.sql.expression.BindParameter) of the same name
  already has been located within the containing
  expression.  This flag is used generally by the internals
  when producing so-called “anonymous” bound expressions, it
  isn’t generally applicable to explicitly-named [bindparam()](#sqlalchemy.sql.expression.bindparam)
  constructs.
- **required** – If `True`, a value is required at execution time.  If not passed,
  it defaults to `True` if neither [bindparam.value](#sqlalchemy.sql.expression.bindparam.params.value)
  or [bindparam.callable](#sqlalchemy.sql.expression.bindparam.params.callable) were passed.  If either of these
  parameters are present, then [bindparam.required](#sqlalchemy.sql.expression.bindparam.params.required)
  defaults to `False`.
- **quote** – True if this parameter name requires quoting and is not
  currently known as a SQLAlchemy reserved word; this currently
  only applies to the Oracle Database backends, where bound names must
  sometimes be quoted.
- **isoutparam** – if True, the parameter should be treated like a stored procedure
  “OUT” parameter.  This applies to backends such as Oracle Database which
  support OUT parameters.
- **expanding** –
  if True, this parameter will be treated as an “expanding” parameter
  at execution time; the parameter value is expected to be a sequence,
  rather than a scalar value, and the string SQL statement will
  be transformed on a per-execution basis to accommodate the sequence
  with a variable number of parameter slots passed to the DBAPI.
  This is to allow statement caching to be used in conjunction with
  an IN clause.
  See also
  [ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_)
  [Using IN expressions](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#baked-in) - with baked queries
  Note
  The “expanding” feature does not support “executemany”-
  style parameter sets.
  Added in version 1.2.
  Changed in version 1.3: the “expanding” bound parameter feature now
  supports empty lists.
- **literal_execute** –
  if True, the bound parameter will be rendered in the compile phase
  with a special “POSTCOMPILE” token, and the SQLAlchemy compiler will
  render the final value of the parameter into the SQL statement at
  statement execution time, omitting the value from the parameter
  dictionary / list passed to DBAPI `cursor.execute()`.  This
  produces a similar effect as that of using the `literal_binds`,
  compilation flag,  however takes place as the statement is sent to
  the DBAPI `cursor.execute()` method, rather than when the statement
  is compiled.   The primary use of this
  capability is for rendering LIMIT / OFFSET clauses for database
  drivers that can’t accommodate for bound parameters in these
  contexts, while allowing SQL constructs to be cacheable at the
  compilation level.
  Added in version 1.4: Added “post compile” bound parameters
  See also
  [New “post compile” bound parameters used for LIMIT/OFFSET in Oracle, SQL Server](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-4808).

See also

[Sending Parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-sending-parameters) - in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     function sqlalchemy.sql.expression.bitwise_not(*expr:_ColumnExpressionArgument[_T]*) → [UnaryExpression](#sqlalchemy.sql.expression.UnaryExpression)[_T]

Produce a unary bitwise NOT clause, typically via the `~` operator.

Not to be confused with boolean negation [not_()](#sqlalchemy.sql.expression.not_).

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     function sqlalchemy.sql.expression.case(**whens:typing_Tuple[_ColumnExpressionArgument[bool],Any]|Mapping[Any,Any]*, *value:Any|None=None*, *else_:Any|None=None*) → [Case](#sqlalchemy.sql.expression.Case)[Any]

Produce a `CASE` expression.

The `CASE` construct in SQL is a conditional object that
acts somewhat analogously to an “if/then” construct in other
languages.  It returns an instance of [Case](#sqlalchemy.sql.expression.Case).

[case()](#sqlalchemy.sql.expression.case) in its usual form is passed a series of “when”
constructs, that is, a list of conditions and results as tuples:

```
from sqlalchemy import case

stmt = select(users_table).where(
    case(
        (users_table.c.name == "wendy", "W"),
        (users_table.c.name == "jack", "J"),
        else_="E",
    )
)
```

The above statement will produce SQL resembling:

```
SELECT id, name FROM user
WHERE CASE
    WHEN (name = :name_1) THEN :param_1
    WHEN (name = :name_2) THEN :param_2
    ELSE :param_3
END
```

When simple equality expressions of several values against a single
parent column are needed, [case()](#sqlalchemy.sql.expression.case) also has a “shorthand” format
used via the
[case.value](#sqlalchemy.sql.expression.case.params.value) parameter, which is passed a column
expression to be compared.  In this form, the [case.whens](#sqlalchemy.sql.expression.case.params.whens)
parameter is passed as a dictionary containing expressions to be
compared against keyed to result expressions.  The statement below is
equivalent to the preceding statement:

```
stmt = select(users_table).where(
    case({"wendy": "W", "jack": "J"}, value=users_table.c.name, else_="E")
)
```

The values which are accepted as result values in
[case.whens](#sqlalchemy.sql.expression.case.params.whens) as well as with [case.else_](#sqlalchemy.sql.expression.case.params.else_) are
coerced from Python literals into [bindparam()](#sqlalchemy.sql.expression.bindparam) constructs.
SQL expressions, e.g. [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) constructs,
are accepted
as well.  To coerce a literal string expression into a constant
expression rendered inline, use the [literal_column()](#sqlalchemy.sql.expression.literal_column)
construct,
as in:

```
from sqlalchemy import case, literal_column

case(
    (orderline.c.qty > 100, literal_column("'greaterthan100'")),
    (orderline.c.qty > 10, literal_column("'greaterthan10'")),
    else_=literal_column("'lessthan10'"),
)
```

The above will render the given constants without using bound
parameters for the result values (but still for the comparison
values), as in:

```
CASE
    WHEN (orderline.qty > :qty_1) THEN 'greaterthan100'
    WHEN (orderline.qty > :qty_2) THEN 'greaterthan10'
    ELSE 'lessthan10'
END
```

   Parameters:

- ***whens** –
  The criteria to be compared against,
  [case.whens](#sqlalchemy.sql.expression.case.params.whens) accepts two different forms, based on
  whether or not [case.value](#sqlalchemy.sql.expression.case.params.value) is used.
  Changed in version 1.4: the [case()](#sqlalchemy.sql.expression.case)
  function now accepts the series of WHEN conditions positionally
  In the first form, it accepts multiple 2-tuples passed as positional
  arguments; each 2-tuple consists of `(<sql expression>, <value>)`,
  where the SQL expression is a boolean expression and “value” is a
  resulting value, e.g.:
  ```
  case(
      (users_table.c.name == "wendy", "W"),
      (users_table.c.name == "jack", "J"),
  )
  ```
  In the second form, it accepts a Python dictionary of comparison
  values mapped to a resulting value; this form requires
  [case.value](#sqlalchemy.sql.expression.case.params.value) to be present, and values will be compared
  using the `==` operator, e.g.:
  ```
  case({"wendy": "W", "jack": "J"}, value=users_table.c.name)
  ```
- **value** – An optional SQL expression which will be used as a
  fixed “comparison point” for candidate values within a dictionary
  passed to [case.whens](#sqlalchemy.sql.expression.case.params.whens).
- **else_** – An optional SQL expression which will be the evaluated
  result of the `CASE` construct if all expressions within
  [case.whens](#sqlalchemy.sql.expression.case.params.whens) evaluate to false.  When omitted, most
  databases will produce a result of NULL if none of the “when”
  expressions evaluate to true.

      function sqlalchemy.sql.expression.cast(*expression:_ColumnExpressionOrLiteralArgument[Any]*, *type_:_TypeEngineArgument[_T]*) → [Cast](#sqlalchemy.sql.expression.Cast)[_T]

Produce a `CAST` expression.

[cast()](#sqlalchemy.sql.expression.cast) returns an instance of [Cast](#sqlalchemy.sql.expression.Cast).

E.g.:

```
from sqlalchemy import cast, Numeric

stmt = select(cast(product_table.c.unit_price, Numeric(10, 4)))
```

The above statement will produce SQL resembling:

```
SELECT CAST(unit_price AS NUMERIC(10, 4)) FROM product
```

The [cast()](#sqlalchemy.sql.expression.cast) function performs two distinct functions when
used.  The first is that it renders the `CAST` expression within
the resulting SQL string.  The second is that it associates the given
type (e.g. [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or instance) with the column
expression on the Python side, which means the expression will take
on the expression operator behavior associated with that type,
as well as the bound-value handling and result-row-handling behavior
of the type.

An alternative to [cast()](#sqlalchemy.sql.expression.cast) is the [type_coerce()](#sqlalchemy.sql.expression.type_coerce) function.
This function performs the second task of associating an expression
with a specific type, but does not render the `CAST` expression
in SQL.

  Parameters:

- **expression** – A SQL expression, such as a
  [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
  expression or a Python string which will be coerced into a bound
  literal value.
- **type_** – A [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or instance indicating
  the type to which the `CAST` should apply.

See also

[Data Casts and Type Coercion](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-casts)

[try_cast()](#sqlalchemy.sql.expression.try_cast) - an alternative to CAST that results in
NULLs when the cast fails, instead of raising an error.
Only supported by some dialects.

[type_coerce()](#sqlalchemy.sql.expression.type_coerce) - an alternative to CAST that coerces the type
on the Python side only, which is often sufficient to generate the
correct SQL and data coercion.

     function sqlalchemy.sql.expression.column(*text:str*, *type_:_TypeEngineArgument[_T]|None=None*, *is_literal:bool=False*, *_selectable:FromClause|None=None*) → [ColumnClause](#sqlalchemy.sql.expression.ColumnClause)[_T]

Produce a [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) object.

The [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) is a lightweight analogue to the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) class.  The [column()](#sqlalchemy.sql.expression.column)
function can
be invoked with just a name alone, as in:

```
from sqlalchemy import column

id, name = column("id"), column("name")
stmt = select(id, name).select_from("user")
```

The above statement would produce SQL like:

```
SELECT id, name FROM user
```

Once constructed, [column()](#sqlalchemy.sql.expression.column)
may be used like any other SQL
expression element such as within [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs:

```
from sqlalchemy.sql import column

id, name = column("id"), column("name")
stmt = select(id, name).select_from("user")
```

The text handled by [column()](#sqlalchemy.sql.expression.column)
is assumed to be handled
like the name of a database column; if the string contains mixed case,
special characters, or matches a known reserved word on the target
backend, the column expression will render using the quoting
behavior determined by the backend.  To produce a textual SQL
expression that is rendered exactly without any quoting,
use [literal_column()](#sqlalchemy.sql.expression.literal_column) instead,
or pass `True` as the
value of [column.is_literal](#sqlalchemy.sql.expression.column.params.is_literal).   Additionally,
full SQL
statements are best handled using the [text()](#sqlalchemy.sql.expression.text)
construct.

[column()](#sqlalchemy.sql.expression.column) can be used in a table-like
fashion by combining it with the [table()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table) function
(which is the lightweight analogue to [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
) to produce
a working table construct with minimal boilerplate:

```
from sqlalchemy import table, column, select

user = table(
    "user",
    column("id"),
    column("name"),
    column("description"),
)

stmt = select(user.c.description).where(user.c.name == "wendy")
```

A [column()](#sqlalchemy.sql.expression.column) / [table()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table)
construct like that illustrated
above can be created in an
ad-hoc fashion and is not associated with any
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData), DDL, or events, unlike its
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) counterpart.

  Parameters:

- **text** – the text of the element.
- **type** – [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) object which can associate
  this [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) with a type.
- **is_literal** – if True, the [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) is assumed to
  be an exact expression that will be delivered to the output with no
  quoting rules applied regardless of case sensitive settings. the
  [literal_column()](#sqlalchemy.sql.expression.literal_column) function essentially invokes
  [column()](#sqlalchemy.sql.expression.column) while passing `is_literal=True`.

See also

[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)

[literal_column()](#sqlalchemy.sql.expression.literal_column)

[table()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table)

[text()](#sqlalchemy.sql.expression.text)

[Selecting with Textual Column Expressions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-select-arbitrary-text)

     class sqlalchemy.sql.expression.custom_op

*inherits from* `sqlalchemy.sql.expression.OperatorType`, `typing.Generic`

Represent a ‘custom’ operator.

[custom_op](#sqlalchemy.sql.expression.custom_op) is normally instantiated when the
[Operators.op()](#sqlalchemy.sql.expression.Operators.op) or [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op) methods
are used to create a custom operator callable.  The class can also be
used directly when programmatically constructing expressions.   E.g.
to represent the “factorial” operation:

```
from sqlalchemy.sql import UnaryExpression
from sqlalchemy.sql import operators
from sqlalchemy import Numeric

unary = UnaryExpression(
    table.c.somecolumn, modifier=operators.custom_op("!"), type_=Numeric
)
```

See also

[Operators.op()](#sqlalchemy.sql.expression.Operators.op)

[Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op)

     function sqlalchemy.sql.expression.distinct(*expr:_ColumnExpressionArgument[_T]*) → [UnaryExpression](#sqlalchemy.sql.expression.UnaryExpression)[_T]

Produce an column-expression-level unary `DISTINCT` clause.

This applies the `DISTINCT` keyword to an **individual column
expression** (e.g. not the whole statement), and renders **specifically
in that column position**; this is used for containment within
an aggregate function, as in:

```
from sqlalchemy import distinct, func

stmt = select(users_table.c.id, func.count(distinct(users_table.c.name)))
```

The above would produce an statement resembling:

```
SELECT user.id, count(DISTINCT user.name) FROM user
```

Tip

The [distinct()](#sqlalchemy.sql.expression.distinct) function does **not** apply DISTINCT
to the full SELECT statement, instead applying a DISTINCT modifier
to **individual column expressions**.  For general `SELECT DISTINCT`
support, use the
[Select.distinct()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.distinct) method on [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select).

The [distinct()](#sqlalchemy.sql.expression.distinct) function is also available as a column-level
method, e.g. [ColumnElement.distinct()](#sqlalchemy.sql.expression.ColumnElement.distinct), as in:

```
stmt = select(func.count(users_table.c.name.distinct()))
```

The [distinct()](#sqlalchemy.sql.expression.distinct) operator is different from the
[Select.distinct()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.distinct) method of
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select),
which produces a `SELECT` statement
with `DISTINCT` applied to the result set as a whole,
e.g. a `SELECT DISTINCT` expression.  See that method for further
information.

See also

[ColumnElement.distinct()](#sqlalchemy.sql.expression.ColumnElement.distinct)

[Select.distinct()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.distinct)

[func](#sqlalchemy.sql.expression.func)

     function sqlalchemy.sql.expression.extract(*field:str*, *expr:_ColumnExpressionArgument[Any]*) → [Extract](#sqlalchemy.sql.expression.Extract)

Return a [Extract](#sqlalchemy.sql.expression.Extract) construct.

This is typically available as [extract()](#sqlalchemy.sql.expression.extract)
as well as `func.extract` from the
[func](#sqlalchemy.sql.expression.func) namespace.

  Parameters:

- **field** –
  The field to extract.
  Warning
  This field is used as a literal SQL string.
  **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
- **expr** – A column or Python scalar expression serving as the
  right side of the `EXTRACT` expression.

E.g.:

```
from sqlalchemy import extract
from sqlalchemy import table, column

logged_table = table(
    "user",
    column("id"),
    column("date_created"),
)

stmt = select(logged_table.c.id).where(
    extract("YEAR", logged_table.c.date_created) == 2021
)
```

In the above example, the statement is used to select ids from the
database where the `YEAR` component matches a specific value.

Similarly, one can also select an extracted component:

```
stmt = select(extract("YEAR", logged_table.c.date_created)).where(
    logged_table.c.id == 1
)
```

The implementation of `EXTRACT` may vary across database backends.
Users are reminded to consult their database documentation.

    function sqlalchemy.sql.expression.false() → [False_](#sqlalchemy.sql.expression.False_)

Return a [False_](#sqlalchemy.sql.expression.False_) construct.

E.g.:

```
>>> from sqlalchemy import false
>>> print(select(t.c.x).where(false()))
SELECT x FROM t WHERE false
```

A backend which does not support true/false constants will render as
an expression against 1 or 0:

```
>>> print(select(t.c.x).where(false()))
SELECT x FROM t WHERE 0 = 1
```

The [true()](#sqlalchemy.sql.expression.true) and [false()](#sqlalchemy.sql.expression.false) constants also feature
“short circuit” operation within an [and_()](#sqlalchemy.sql.expression.and_) or [or_()](#sqlalchemy.sql.expression.or_)
conjunction:

```
>>> print(select(t.c.x).where(or_(t.c.x > 5, true())))
SELECT x FROM t WHERE true
>>> print(select(t.c.x).where(and_(t.c.x > 5, false())))
SELECT x FROM t WHERE false
```

See also

[true()](#sqlalchemy.sql.expression.true)

     sqlalchemy.sql.expression.func = <sqlalchemy.sql.functions._FunctionGenerator object>

Generate SQL function expressions.

[func](#sqlalchemy.sql.expression.func) is a special object instance which generates SQL
functions based on name-based attributes, e.g.:

```
>>> print(func.count(1))
count(:param_1)
```

The returned object is an instance of [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function), and  is a
column-oriented SQL element like any other, and is used in that way:

```
>>> print(select(func.count(table.c.id)))
SELECT count(sometable.id) FROM sometable
```

Any name can be given to [func](#sqlalchemy.sql.expression.func). If the function name is unknown to
SQLAlchemy, it will be rendered exactly as is. For common SQL functions
which SQLAlchemy is aware of, the name may be interpreted as a *generic
function* which will be compiled appropriately to the target database:

```
>>> print(func.current_timestamp())
CURRENT_TIMESTAMP
```

To call functions which are present in dot-separated packages,
specify them in the same manner:

```
>>> print(func.stats.yield_curve(5, 10))
stats.yield_curve(:yield_curve_1, :yield_curve_2)
```

SQLAlchemy can be made aware of the return type of functions to enable
type-specific lexical and result-based behavior. For example, to ensure
that a string-based function returns a Unicode value and is similarly
treated as a string in expressions, specify
[Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) as the type:

```
>>> print(
...     func.my_string("hi", type_=Unicode)
...     + " "
...     + func.my_string("there", type_=Unicode)
... )
my_string(:my_string_1) || :my_string_2 || my_string(:my_string_3)
```

The object returned by a [func](#sqlalchemy.sql.expression.func) call is usually an instance of
[Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function).
This object meets the “column” interface, including comparison and labeling
functions.  The object can also be passed the `Connectable.execute()`
method of a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
where it will be
wrapped inside of a SELECT statement first:

```
print(connection.execute(func.current_timestamp()).scalar())
```

In a few exception cases, the [func](#sqlalchemy.sql.expression.func) accessor
will redirect a name to a built-in expression such as [cast()](#sqlalchemy.sql.expression.cast)
or [extract()](#sqlalchemy.sql.expression.extract), as these names have well-known meaning
but are not exactly the same as “functions” from a SQLAlchemy
perspective.

Functions which are interpreted as “generic” functions know how to
calculate their return type automatically. For a listing of known generic
functions, see [SQL and Generic Functions](https://docs.sqlalchemy.org/en/20/core/functions.html#generic-functions).

Note

The [func](#sqlalchemy.sql.expression.func) construct has only limited support for calling
standalone “stored procedures”, especially those with special
parameterization concerns.

See the section [Calling Stored Procedures and User Defined Functions](https://docs.sqlalchemy.org/en/20/core/connections.html#stored-procedures) for details on how to use
the DBAPI-level `callproc()` method for fully traditional stored
procedures.

See also

[Working with SQL Functions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-functions) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function)

     function sqlalchemy.sql.expression.lambda_stmt(*lmb:Callable[[],Any]*, *enable_tracking:bool=True*, *track_closure_variables:bool=True*, *track_on:object|None=None*, *global_track_bound_values:bool=True*, *track_bound_values:bool=True*, *lambda_cache:MutableMapping[Tuple[Any,...],NonAnalyzedFunction|AnalyzedFunction]|None=None*) → [StatementLambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement)

Produce a SQL statement that is cached as a lambda.

The Python code object within the lambda is scanned for both Python
literals that will become bound parameters as well as closure variables
that refer to Core or ORM constructs that may vary.   The lambda itself
will be invoked only once per particular set of constructs detected.

E.g.:

```
from sqlalchemy import lambda_stmt

stmt = lambda_stmt(lambda: table.select())
stmt += lambda s: s.where(table.c.id == 5)

result = connection.execute(stmt)
```

The object returned is an instance of [StatementLambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement).

Added in version 1.4.

   Parameters:

- **lmb** – a Python function, typically a lambda, which takes no arguments
  and returns a SQL expression construct
- **enable_tracking** – when False, all scanning of the given lambda for
  changes in closure variables or bound parameters is disabled.  Use for
  a lambda that produces the identical results in all cases with no
  parameterization.
- **track_closure_variables** – when False, changes in closure variables
  within the lambda will not be scanned.   Use for a lambda where the
  state of its closure variables will never change the SQL structure
  returned by the lambda.
- **track_bound_values** – when False, bound parameter tracking will
  be disabled for the given lambda.  Use for a lambda that either does
  not produce any bound values, or where the initial bound values never
  change.
- **global_track_bound_values** – when False, bound parameter tracking
  will be disabled for the entire statement including additional links
  added via the [StatementLambdaElement.add_criteria()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.add_criteria) method.
- **lambda_cache** – a dictionary or other mapping-like object where
  information about the lambda’s Python code as well as the tracked closure
  variables in the lambda itself will be stored.   Defaults
  to a global LRU cache.  This cache is independent of the “compiled_cache”
  used by the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object.

See also

[Using Lambdas to add significant speed gains to statement production](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-lambda-caching)

     function sqlalchemy.sql.expression.literal(*value:Any*, *type_:_TypeEngineArgument[Any]|None=None*, *literal_execute:bool=False*) → [BindParameter](#sqlalchemy.sql.expression.BindParameter)[Any]

Return a literal clause, bound to a bind parameter.

Literal clauses are created automatically when non-
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) objects (such as strings, ints, dates,
etc.) are
used in a comparison operation with a [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
subclass,
such as a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object.  Use this function
to force the generation of a literal clause, which will be created as a
[BindParameter](#sqlalchemy.sql.expression.BindParameter) with a bound value.

  Parameters:

- **value** – the value to be bound. Can be any Python object supported by
  the underlying DB-API, or is translatable via the given type argument.
- **type_** – an optional [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) which will
  provide bind-parameter translation for this literal.
- **literal_execute** –
  optional bool, when True, the SQL engine will
  attempt to render the bound value directly in the SQL statement at
  execution time rather than providing as a parameter value.
  Added in version 2.0.

      function sqlalchemy.sql.expression.literal_column(*text:str*, *type_:_TypeEngineArgument[_T]|None=None*) → [ColumnClause](#sqlalchemy.sql.expression.ColumnClause)[_T]

Produce a [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) object that has the
[column.is_literal](#sqlalchemy.sql.expression.column.params.is_literal) flag set to True.

[literal_column()](#sqlalchemy.sql.expression.literal_column) is similar to
[column()](#sqlalchemy.sql.expression.column), except that
it is more often used as a “standalone” column expression that renders
exactly as stated; while [column()](#sqlalchemy.sql.expression.column)
stores a string name that
will be assumed to be part of a table and may be quoted as such,
[literal_column()](#sqlalchemy.sql.expression.literal_column) can be that,
or any other arbitrary column-oriented
expression.

  Parameters:

- **text** – the text of the expression; can be any SQL expression.
  Quoting rules will not be applied. To specify a column-name expression
  which should be subject to quoting rules, use the [column()](#sqlalchemy.sql.expression.column)
  function.
- **type_** – an optional [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)
  object which will
  provide result-set translation and additional expression semantics for
  this column. If left as `None` the type will be [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType).

See also

[column()](#sqlalchemy.sql.expression.column)

[text()](#sqlalchemy.sql.expression.text)

[Selecting with Textual Column Expressions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-select-arbitrary-text)

     function sqlalchemy.sql.expression.not_(*clause:_ColumnExpressionArgument[_T]*) → [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)[_T]

Return a negation of the given clause, i.e. `NOT(clause)`.

The `~` operator is also overloaded on all
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement) subclasses to produce the
same result.

    function sqlalchemy.sql.expression.null() → [Null](#sqlalchemy.sql.expression.Null)

Return a constant [Null](#sqlalchemy.sql.expression.Null) construct.

    function sqlalchemy.sql.expression.or_(**clauses*)

Produce a conjunction of expressions joined by `OR`.

E.g.:

```
from sqlalchemy import or_

stmt = select(users_table).where(
    or_(users_table.c.name == "wendy", users_table.c.name == "jack")
)
```

The [or_()](#sqlalchemy.sql.expression.or_) conjunction is also available using the
Python `|` operator (though note that compound expressions
need to be parenthesized in order to function with Python
operator precedence behavior):

```
stmt = select(users_table).where(
    (users_table.c.name == "wendy") | (users_table.c.name == "jack")
)
```

The [or_()](#sqlalchemy.sql.expression.or_) construct must be given at least one positional
argument in order to be valid; a [or_()](#sqlalchemy.sql.expression.or_) construct with no
arguments is ambiguous.   To produce an “empty” or dynamically
generated [or_()](#sqlalchemy.sql.expression.or_)  expression, from a given list of expressions,
a “default” element of [false()](#sqlalchemy.sql.expression.false) (or just `False`) should be
specified:

```
from sqlalchemy import false

or_criteria = or_(false(), *expressions)
```

The above expression will compile to SQL as the expression `false`
or `0 = 1`, depending on backend, if no other expressions are
present.  If expressions are present, then the [false()](#sqlalchemy.sql.expression.false) value
is ignored as it does not affect the outcome of an OR expression which
has other elements.

Deprecated since version 1.4: The [or_()](#sqlalchemy.sql.expression.or_) element now requires that at
least one argument is passed; creating the [or_()](#sqlalchemy.sql.expression.or_) construct
with no arguments is deprecated, and will emit a deprecation warning
while continuing to produce a blank SQL string.

See also

[and_()](#sqlalchemy.sql.expression.and_)

     function sqlalchemy.sql.expression.outparam(*key:str*, *type_:TypeEngine[_T]|None=None*) → [BindParameter](#sqlalchemy.sql.expression.BindParameter)[_T]

Create an ‘OUT’ parameter for usage in functions (stored procedures),
for databases which support them.

The `outparam` can be used like a regular function parameter.
The “output” value will be available from the
[CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) object via its `out_parameters`
attribute, which returns a dictionary containing the values.

    function sqlalchemy.sql.expression.text(*text:str*) → [TextClause](#sqlalchemy.sql.expression.TextClause)

Construct a new [TextClause](#sqlalchemy.sql.expression.TextClause) clause,
representing
a textual SQL string directly.

E.g.:

```
from sqlalchemy import text

t = text("SELECT * FROM users")
result = connection.execute(t)
```

The advantages [text()](#sqlalchemy.sql.expression.text)
provides over a plain string are
backend-neutral support for bind parameters, per-statement
execution options, as well as
bind parameter and result-column typing behavior, allowing
SQLAlchemy type constructs to play a role when executing
a statement that is specified literally.  The construct can also
be provided with a `.c` collection of column elements, allowing
it to be embedded in other SQL expression constructs as a subquery.

Bind parameters are specified by name, using the format `:name`.
E.g.:

```
t = text("SELECT * FROM users WHERE id=:user_id")
result = connection.execute(t, {"user_id": 12})
```

For SQL statements where a colon is required verbatim, as within
an inline string, use a backslash to escape:

```
t = text(r"SELECT * FROM users WHERE name='\:username'")
```

The [TextClause](#sqlalchemy.sql.expression.TextClause)
construct includes methods which can
provide information about the bound parameters as well as the column
values which would be returned from the textual statement, assuming
it’s an executable SELECT type of statement.  The
[TextClause.bindparams()](#sqlalchemy.sql.expression.TextClause.bindparams)
method is used to provide bound
parameter detail, and [TextClause.columns()](#sqlalchemy.sql.expression.TextClause.columns)
method allows
specification of return columns including names and types:

```
t = (
    text("SELECT * FROM users WHERE id=:user_id")
    .bindparams(user_id=7)
    .columns(id=Integer, name=String)
)

for id, name in connection.execute(t):
    print(id, name)
```

The [text()](#sqlalchemy.sql.expression.text) construct is used in cases when
a literal string SQL fragment is specified as part of a larger query,
such as for the WHERE clause of a SELECT statement:

```
s = select(users.c.id, users.c.name).where(text("id=:user_id"))
result = connection.execute(s, {"user_id": 12})
```

[text()](#sqlalchemy.sql.expression.text) is also used for the construction
of a full, standalone statement using plain text.
As such, SQLAlchemy refers
to it as an [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable) object and may be used
like any other statement passed to an `.execute()` method.

  Parameters:

**text** – the text of the SQL statement to be created.  Use `:<param>`
to specify bind parameters; they will be compiled to their
engine-specific format.

See also

[Selecting with Textual Column Expressions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-select-arbitrary-text)

     function sqlalchemy.sql.expression.true() → [True_](#sqlalchemy.sql.expression.True_)

Return a constant [True_](#sqlalchemy.sql.expression.True_) construct.

E.g.:

```
>>> from sqlalchemy import true
>>> print(select(t.c.x).where(true()))
SELECT x FROM t WHERE true
```

A backend which does not support true/false constants will render as
an expression against 1 or 0:

```
>>> print(select(t.c.x).where(true()))
SELECT x FROM t WHERE 1 = 1
```

The [true()](#sqlalchemy.sql.expression.true) and [false()](#sqlalchemy.sql.expression.false) constants also feature
“short circuit” operation within an [and_()](#sqlalchemy.sql.expression.and_) or [or_()](#sqlalchemy.sql.expression.or_)
conjunction:

```
>>> print(select(t.c.x).where(or_(t.c.x > 5, true())))
SELECT x FROM t WHERE true
>>> print(select(t.c.x).where(and_(t.c.x > 5, false())))
SELECT x FROM t WHERE false
```

See also

[false()](#sqlalchemy.sql.expression.false)

     function sqlalchemy.sql.expression.try_cast(*expression:_ColumnExpressionOrLiteralArgument[Any]*, *type_:_TypeEngineArgument[_T]*) → [TryCast](#sqlalchemy.sql.expression.TryCast)[_T]

Produce a `TRY_CAST` expression for backends which support it;
this is a `CAST` which returns NULL for un-castable conversions.

In SQLAlchemy, this construct is supported **only** by the SQL Server
dialect, and will raise a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) if used on other
included backends.  However, third party backends may also support
this construct.

Tip

As [try_cast()](#sqlalchemy.sql.expression.try_cast) originates from the SQL Server dialect,
it’s importable both from `sqlalchemy.` as well as from
`sqlalchemy.dialects.mssql`.

[try_cast()](#sqlalchemy.sql.expression.try_cast) returns an instance of [TryCast](#sqlalchemy.sql.expression.TryCast) and
generally behaves similarly to the [Cast](#sqlalchemy.sql.expression.Cast) construct;
at the SQL level, the difference between `CAST` and `TRY_CAST`
is that `TRY_CAST` returns NULL for an un-castable expression,
such as attempting to cast a string `"hi"` to an integer value.

E.g.:

```
from sqlalchemy import select, try_cast, Numeric

stmt = select(try_cast(product_table.c.unit_price, Numeric(10, 4)))
```

The above would render on Microsoft SQL Server as:

```
SELECT TRY_CAST (product_table.unit_price AS NUMERIC(10, 4))
FROM product_table
```

Added in version 2.0.14: [try_cast()](#sqlalchemy.sql.expression.try_cast) has been
generalized from the SQL Server dialect into a general use
construct that may be supported by additional dialects.

     function sqlalchemy.sql.expression.tuple_(**clauses:_ColumnExpressionArgument[Any]*, *types:Sequence[_TypeEngineArgument[Any]]|None=None*) → [Tuple](#sqlalchemy.sql.expression.Tuple)

Return a [Tuple](#sqlalchemy.sql.expression.Tuple).

Main usage is to produce a composite IN construct using
[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_)

```
from sqlalchemy import tuple_

tuple_(table.c.col1, table.c.col2).in_([(1, 2), (5, 12), (10, 19)])
```

Changed in version 1.3.6: Added support for SQLite IN tuples.

Warning

The composite IN construct is not supported by all backends, and is
currently known to work on PostgreSQL, MySQL, and SQLite.
Unsupported backends will raise a subclass of
[DBAPIError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DBAPIError) when such an expression is
invoked.

     function sqlalchemy.sql.expression.type_coerce(*expression:_ColumnExpressionOrLiteralArgument[Any]*, *type_:_TypeEngineArgument[_T]*) → [TypeCoerce](#sqlalchemy.sql.expression.TypeCoerce)[_T]

Associate a SQL expression with a particular type, without rendering
`CAST`.

E.g.:

```
from sqlalchemy import type_coerce

stmt = select(type_coerce(log_table.date_string, StringDateTime()))
```

The above construct will produce a [TypeCoerce](#sqlalchemy.sql.expression.TypeCoerce) object, which
does not modify the rendering in any way on the SQL side, with the
possible exception of a generated label if used in a columns clause
context:

```
SELECT date_string AS date_string FROM log
```

When result rows are fetched, the `StringDateTime` type processor
will be applied to result rows on behalf of the `date_string` column.

Note

the [type_coerce()](#sqlalchemy.sql.expression.type_coerce) construct does not render any
SQL syntax of its own, including that it does not imply
parenthesization.   Please use [TypeCoerce.self_group()](#sqlalchemy.sql.expression.TypeCoerce.self_group)
if explicit parenthesization is required.

In order to provide a named label for the expression, use
[ColumnElement.label()](#sqlalchemy.sql.expression.ColumnElement.label):

```
stmt = select(
    type_coerce(log_table.date_string, StringDateTime()).label("date")
)
```

A type that features bound-value handling will also have that behavior
take effect when literal values or [bindparam()](#sqlalchemy.sql.expression.bindparam) constructs are
passed to [type_coerce()](#sqlalchemy.sql.expression.type_coerce) as targets.
For example, if a type implements the
[TypeEngine.bind_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_expression)
method or [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor) method or equivalent,
these functions will take effect at statement compilation/execution
time when a literal value is passed, as in:

```
# bound-value handling of MyStringType will be applied to the
# literal value "some string"
stmt = select(type_coerce("some string", MyStringType))
```

When using [type_coerce()](#sqlalchemy.sql.expression.type_coerce) with composed expressions, note that
**parenthesis are not applied**.   If [type_coerce()](#sqlalchemy.sql.expression.type_coerce) is being
used in an operator context where the parenthesis normally present from
CAST are necessary, use the [TypeCoerce.self_group()](#sqlalchemy.sql.expression.TypeCoerce.self_group) method:

```
>>> some_integer = column("someint", Integer)
>>> some_string = column("somestr", String)
>>> expr = type_coerce(some_integer + 5, String) + some_string
>>> print(expr)
someint + :someint_1 || somestr
>>> expr = type_coerce(some_integer + 5, String).self_group() + some_string
>>> print(expr)
(someint + :someint_1) || somestr
```

   Parameters:

- **expression** – A SQL expression, such as a
  [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
  expression or a Python string which will be coerced into a bound
  literal value.
- **type_** – A [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or instance indicating
  the type to which the expression is coerced.

See also

[Data Casts and Type Coercion](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-casts)

[cast()](#sqlalchemy.sql.expression.cast)

     class sqlalchemy.sql.expression.quoted_name

*inherits from* `sqlalchemy.util.langhelpers.MemoizedSlots`, `builtins.str`

Represent a SQL identifier combined with quoting preferences.

[quoted_name](#sqlalchemy.sql.expression.quoted_name) is a Python unicode/str subclass which
represents a particular identifier name along with a
`quote` flag.  This `quote` flag, when set to
`True` or `False`, overrides automatic quoting behavior
for this identifier in order to either unconditionally quote
or to not quote the name.  If left at its default of `None`,
quoting behavior is applied to the identifier on a per-backend basis
based on an examination of the token itself.

A [quoted_name](#sqlalchemy.sql.expression.quoted_name) object with `quote=True` is also
prevented from being modified in the case of a so-called
“name normalize” option.  Certain database backends, such as
Oracle Database, Firebird, and DB2 “normalize” case-insensitive names
as uppercase.  The SQLAlchemy dialects for these backends
convert from SQLAlchemy’s lower-case-means-insensitive convention
to the upper-case-means-insensitive conventions of those backends.
The `quote=True` flag here will prevent this conversion from occurring
to support an identifier that’s quoted as all lower case against
such a backend.

The [quoted_name](#sqlalchemy.sql.expression.quoted_name) object is normally created automatically
when specifying the name for key schema constructs such as
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), and others.
The class can also be
passed explicitly as the name to any function that receives a name which
can be quoted.  Such as to use the `Engine.has_table()`
method with
an unconditionally quoted name:

```
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.sql import quoted_name

engine = create_engine("oracle+oracledb://some_dsn")
print(inspect(engine).has_table(quoted_name("some_table", True)))
```

The above logic will run the “has table” logic against the Oracle Database
backend, passing the name exactly as `"some_table"` without converting to
upper case.

Changed in version 1.2: The [quoted_name](#sqlalchemy.sql.expression.quoted_name) construct is now
importable from `sqlalchemy.sql`, in addition to the previous
location of `sqlalchemy.sql.elements`.

| Member Name | Description |
| --- | --- |
| quote | whether the string should be unconditionally quoted |

   attribute [sqlalchemy.sql.expression.quoted_name.](#sqlalchemy.sql.expression.quoted_name)quote

whether the string should be unconditionally quoted

## Column Element Modifier Constructors

Functions listed here are more commonly available as methods from any
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement) construct, for example, the
[label()](#sqlalchemy.sql.expression.label) function is usually invoked via the
[ColumnElement.label()](#sqlalchemy.sql.expression.ColumnElement.label) method.

| Object Name | Description |
| --- | --- |
| all_(expr) | Produce an ALL expression. |
| any_(expr) | Produce an ANY expression. |
| asc(column) | Produce an ascendingORDERBYclause element. |
| between(expr, lower_bound, upper_bound[, symmetric]) | Produce aBETWEENpredicate clause. |
| collate(expression, collation) | Return the clauseexpressionCOLLATEcollation. |
| desc(column) | Produce a descendingORDERBYclause element. |
| funcfilter(func, *criterion) | Produce aFunctionFilterobject against a function. |
| label(name, element[, type_]) | Return aLabelobject for the
givenColumnElement. |
| nulls_first(column) | Produce theNULLSFIRSTmodifier for anORDERBYexpression. |
| nulls_last(column) | Produce theNULLSLASTmodifier for anORDERBYexpression. |
| nullsfirst | Synonym for thenulls_first()function. |
| nullslast | Legacy synonym for thenulls_last()function. |
| over(element[, partition_by, order_by, range_, ...]) | Produce anOverobject against a function. |
| within_group(element, *order_by) | Produce aWithinGroupobject against a function. |

   function sqlalchemy.sql.expression.all_(*expr:_ColumnExpressionArgument[_T]*) → CollectionAggregate[bool]

Produce an ALL expression.

For dialects such as that of PostgreSQL, this operator applies
to usage of the [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) datatype, for that of
MySQL, it may apply to a subquery.  e.g.:

```
# renders on PostgreSQL:
# '5 = ALL (somearray)'
expr = 5 == all_(mytable.c.somearray)

# renders on MySQL:
# '5 = ALL (SELECT value FROM table)'
expr = 5 == all_(select(table.c.value))
```

Comparison to NULL may work using `None`:

```
None == all_(mytable.c.somearray)
```

The any_() / all_() operators also feature a special “operand flipping”
behavior such that if any_() / all_() are used on the left side of a
comparison using a standalone operator such as `==`, `!=`, etc.
(not including operator methods such as
[ColumnOperators.is_()](#sqlalchemy.sql.expression.ColumnOperators.is_)) the rendered expression is flipped:

```
# would render '5 = ALL (column)`
all_(mytable.c.column) == 5
```

Or with `None`, which note will not perform
the usual step of rendering “IS” as is normally the case for NULL:

```
# would render 'NULL = ALL(somearray)'
all_(mytable.c.somearray) == None
```

Changed in version 1.4.26: repaired the use of any_() / all_()
comparing to NULL on the right side to be flipped to the left.

The column-level [ColumnElement.all_()](#sqlalchemy.sql.expression.ColumnElement.all_) method (not to be
confused with [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) level
[Comparator.all()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.all)) is shorthand for
`all_(col)`:

```
5 == mytable.c.somearray.all_()
```

See also

[ColumnOperators.all_()](#sqlalchemy.sql.expression.ColumnOperators.all_)

[any_()](#sqlalchemy.sql.expression.any_)

     function sqlalchemy.sql.expression.any_(*expr:_ColumnExpressionArgument[_T]*) → CollectionAggregate[bool]

Produce an ANY expression.

For dialects such as that of PostgreSQL, this operator applies
to usage of the [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) datatype, for that of
MySQL, it may apply to a subquery.  e.g.:

```
# renders on PostgreSQL:
# '5 = ANY (somearray)'
expr = 5 == any_(mytable.c.somearray)

# renders on MySQL:
# '5 = ANY (SELECT value FROM table)'
expr = 5 == any_(select(table.c.value))
```

Comparison to NULL may work using `None` or [null()](#sqlalchemy.sql.expression.null):

```
None == any_(mytable.c.somearray)
```

The any_() / all_() operators also feature a special “operand flipping”
behavior such that if any_() / all_() are used on the left side of a
comparison using a standalone operator such as `==`, `!=`, etc.
(not including operator methods such as
[ColumnOperators.is_()](#sqlalchemy.sql.expression.ColumnOperators.is_)) the rendered expression is flipped:

```
# would render '5 = ANY (column)`
any_(mytable.c.column) == 5
```

Or with `None`, which note will not perform
the usual step of rendering “IS” as is normally the case for NULL:

```
# would render 'NULL = ANY(somearray)'
any_(mytable.c.somearray) == None
```

Changed in version 1.4.26: repaired the use of any_() / all_()
comparing to NULL on the right side to be flipped to the left.

The column-level [ColumnElement.any_()](#sqlalchemy.sql.expression.ColumnElement.any_) method (not to be
confused with [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) level
[Comparator.any()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.any)) is shorthand for
`any_(col)`:

```
5 = mytable.c.somearray.any_()
```

See also

[ColumnOperators.any_()](#sqlalchemy.sql.expression.ColumnOperators.any_)

[all_()](#sqlalchemy.sql.expression.all_)

     function sqlalchemy.sql.expression.asc(*column:_ColumnExpressionOrStrLabelArgument[_T]*) → [UnaryExpression](#sqlalchemy.sql.expression.UnaryExpression)[_T]

Produce an ascending `ORDER BY` clause element.

e.g.:

```
from sqlalchemy import asc

stmt = select(users_table).order_by(asc(users_table.c.name))
```

will produce SQL as:

```
SELECT id, name FROM user ORDER BY name ASC
```

The [asc()](#sqlalchemy.sql.expression.asc) function is a standalone version of the
[ColumnElement.asc()](#sqlalchemy.sql.expression.ColumnElement.asc)
method available on all SQL expressions,
e.g.:

```
stmt = select(users_table).order_by(users_table.c.name.asc())
```

   Parameters:

**column** – A [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) (e.g.
scalar SQL expression)
with which to apply the [asc()](#sqlalchemy.sql.expression.asc) operation.

See also

[desc()](#sqlalchemy.sql.expression.desc)

[nulls_first()](#sqlalchemy.sql.expression.nulls_first)

[nulls_last()](#sqlalchemy.sql.expression.nulls_last)

[Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by)

     function sqlalchemy.sql.expression.between(*expr:_ColumnExpressionOrLiteralArgument[_T]*, *lower_bound:Any*, *upper_bound:Any*, *symmetric:bool=False*) → [BinaryExpression](#sqlalchemy.sql.expression.BinaryExpression)[bool]

Produce a `BETWEEN` predicate clause.

E.g.:

```
from sqlalchemy import between

stmt = select(users_table).where(between(users_table.c.id, 5, 7))
```

Would produce SQL resembling:

```
SELECT id, name FROM user WHERE id BETWEEN :id_1 AND :id_2
```

The [between()](#sqlalchemy.sql.expression.between) function is a standalone version of the
[ColumnElement.between()](#sqlalchemy.sql.expression.ColumnElement.between) method available on all
SQL expressions, as in:

```
stmt = select(users_table).where(users_table.c.id.between(5, 7))
```

All arguments passed to [between()](#sqlalchemy.sql.expression.between), including the left side
column expression, are coerced from Python scalar values if a
the value is not a [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) subclass.
For example,
three fixed values can be compared as in:

```
print(between(5, 3, 7))
```

Which would produce:

```
:param_1 BETWEEN :param_2 AND :param_3
```

   Parameters:

- **expr** – a column expression, typically a
  [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
  instance or alternatively a Python scalar expression to be coerced
  into a column expression, serving as the left side of the `BETWEEN`
  expression.
- **lower_bound** – a column or Python scalar expression serving as the
  lower bound of the right side of the `BETWEEN` expression.
- **upper_bound** – a column or Python scalar expression serving as the
  upper bound of the right side of the `BETWEEN` expression.
- **symmetric** – if True, will render “ BETWEEN SYMMETRIC “. Note
  that not all databases support this syntax.

See also

[ColumnElement.between()](#sqlalchemy.sql.expression.ColumnElement.between)

     function sqlalchemy.sql.expression.collate(*expression:_ColumnExpressionArgument[str]*, *collation:str*) → [BinaryExpression](#sqlalchemy.sql.expression.BinaryExpression)[str]

Return the clause `expression COLLATE collation`.

e.g.:

```
collate(mycolumn, "utf8_bin")
```

produces:

```
mycolumn COLLATE utf8_bin
```

The collation expression is also quoted if it is a case sensitive
identifier, e.g. contains uppercase characters.

Changed in version 1.2: quoting is automatically applied to COLLATE
expressions if they are case sensitive.

     function sqlalchemy.sql.expression.desc(*column:_ColumnExpressionOrStrLabelArgument[_T]*) → [UnaryExpression](#sqlalchemy.sql.expression.UnaryExpression)[_T]

Produce a descending `ORDER BY` clause element.

e.g.:

```
from sqlalchemy import desc

stmt = select(users_table).order_by(desc(users_table.c.name))
```

will produce SQL as:

```
SELECT id, name FROM user ORDER BY name DESC
```

The [desc()](#sqlalchemy.sql.expression.desc) function is a standalone version of the
[ColumnElement.desc()](#sqlalchemy.sql.expression.ColumnElement.desc)
method available on all SQL expressions,
e.g.:

```
stmt = select(users_table).order_by(users_table.c.name.desc())
```

   Parameters:

**column** – A [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) (e.g.
scalar SQL expression)
with which to apply the [desc()](#sqlalchemy.sql.expression.desc) operation.

See also

[asc()](#sqlalchemy.sql.expression.asc)

[nulls_first()](#sqlalchemy.sql.expression.nulls_first)

[nulls_last()](#sqlalchemy.sql.expression.nulls_last)

[Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by)

     function sqlalchemy.sql.expression.funcfilter(*func:FunctionElement[_T]*, **criterion:_ColumnExpressionArgument[bool]*) → [FunctionFilter](#sqlalchemy.sql.expression.FunctionFilter)[_T]

Produce a [FunctionFilter](#sqlalchemy.sql.expression.FunctionFilter) object against a function.

Used against aggregate and window functions,
for database backends that support the “FILTER” clause.

E.g.:

```
from sqlalchemy import funcfilter

funcfilter(func.count(1), MyClass.name == "some name")
```

Would produce “COUNT(1) FILTER (WHERE myclass.name = ‘some name’)”.

This function is also available from the [func](#sqlalchemy.sql.expression.func)
construct itself via the [FunctionElement.filter()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.filter) method.

See also

[Special Modifiers WITHIN GROUP, FILTER](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-functions-within-group) - in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[FunctionElement.filter()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.filter)

     function sqlalchemy.sql.expression.label(*name:str*, *element:_ColumnExpressionArgument[_T]*, *type_:_TypeEngineArgument[_T]|None=None*) → [Label](#sqlalchemy.sql.expression.Label)[_T]

Return a [Label](#sqlalchemy.sql.expression.Label) object for the
given [ColumnElement](#sqlalchemy.sql.expression.ColumnElement).

A label changes the name of an element in the columns clause of a
`SELECT` statement, typically via the `AS` SQL keyword.

This functionality is more conveniently available via the
[ColumnElement.label()](#sqlalchemy.sql.expression.ColumnElement.label) method on
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement).

  Parameters:

- **name** – label name
- **obj** – a [ColumnElement](#sqlalchemy.sql.expression.ColumnElement).

      function sqlalchemy.sql.expression.nulls_first(*column:_ColumnExpressionArgument[_T]*) → [UnaryExpression](#sqlalchemy.sql.expression.UnaryExpression)[_T]

Produce the `NULLS FIRST` modifier for an `ORDER BY` expression.

[nulls_first()](#sqlalchemy.sql.expression.nulls_first) is intended to modify the expression produced
by [asc()](#sqlalchemy.sql.expression.asc) or [desc()](#sqlalchemy.sql.expression.desc), and indicates how NULL values
should be handled when they are encountered during ordering:

```
from sqlalchemy import desc, nulls_first

stmt = select(users_table).order_by(nulls_first(desc(users_table.c.name)))
```

The SQL expression from the above would resemble:

```
SELECT id, name FROM user ORDER BY name DESC NULLS FIRST
```

Like [asc()](#sqlalchemy.sql.expression.asc) and [desc()](#sqlalchemy.sql.expression.desc), [nulls_first()](#sqlalchemy.sql.expression.nulls_first) is typically
invoked from the column expression itself using
[ColumnElement.nulls_first()](#sqlalchemy.sql.expression.ColumnElement.nulls_first),
rather than as its standalone
function version, as in:

```
stmt = select(users_table).order_by(
    users_table.c.name.desc().nulls_first()
)
```

Changed in version 1.4: [nulls_first()](#sqlalchemy.sql.expression.nulls_first) is renamed from
[nullsfirst()](#sqlalchemy.sql.expression.nullsfirst) in previous releases.
The previous name remains available for backwards compatibility.

See also

[asc()](#sqlalchemy.sql.expression.asc)

[desc()](#sqlalchemy.sql.expression.desc)

[nulls_last()](#sqlalchemy.sql.expression.nulls_last)

[Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by)

     function sqlalchemy.sql.expression.nullsfirst()

Synonym for the [nulls_first()](#sqlalchemy.sql.expression.nulls_first) function.

Changed in version 2.0.5: restored missing legacy symbol [nullsfirst()](#sqlalchemy.sql.expression.nullsfirst).

     function sqlalchemy.sql.expression.nulls_last(*column:_ColumnExpressionArgument[_T]*) → [UnaryExpression](#sqlalchemy.sql.expression.UnaryExpression)[_T]

Produce the `NULLS LAST` modifier for an `ORDER BY` expression.

[nulls_last()](#sqlalchemy.sql.expression.nulls_last) is intended to modify the expression produced
by [asc()](#sqlalchemy.sql.expression.asc) or [desc()](#sqlalchemy.sql.expression.desc), and indicates how NULL values
should be handled when they are encountered during ordering:

```
from sqlalchemy import desc, nulls_last

stmt = select(users_table).order_by(nulls_last(desc(users_table.c.name)))
```

The SQL expression from the above would resemble:

```
SELECT id, name FROM user ORDER BY name DESC NULLS LAST
```

Like [asc()](#sqlalchemy.sql.expression.asc) and [desc()](#sqlalchemy.sql.expression.desc), [nulls_last()](#sqlalchemy.sql.expression.nulls_last) is typically
invoked from the column expression itself using
[ColumnElement.nulls_last()](#sqlalchemy.sql.expression.ColumnElement.nulls_last),
rather than as its standalone
function version, as in:

```
stmt = select(users_table).order_by(users_table.c.name.desc().nulls_last())
```

Changed in version 1.4: [nulls_last()](#sqlalchemy.sql.expression.nulls_last) is renamed from
[nullslast()](#sqlalchemy.sql.expression.nullslast) in previous releases.
The previous name remains available for backwards compatibility.

See also

[asc()](#sqlalchemy.sql.expression.asc)

[desc()](#sqlalchemy.sql.expression.desc)

[nulls_first()](#sqlalchemy.sql.expression.nulls_first)

[Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by)

     function sqlalchemy.sql.expression.nullslast()

Legacy synonym for the [nulls_last()](#sqlalchemy.sql.expression.nulls_last) function.

Changed in version 2.0.5: restored missing legacy symbol [nullslast()](#sqlalchemy.sql.expression.nullslast).

     function sqlalchemy.sql.expression.over(*element:FunctionElement[_T]*, *partition_by:_ByArgument|None=None*, *order_by:_ByArgument|None=None*, *range_:typing_Tuple[int|None,int|None]|None=None*, *rows:typing_Tuple[int|None,int|None]|None=None*, *groups:typing_Tuple[int|None,int|None]|None=None*) → [Over](#sqlalchemy.sql.expression.Over)[_T]

Produce an [Over](#sqlalchemy.sql.expression.Over) object against a function.

Used against aggregate or so-called “window” functions,
for database backends that support window functions.

[over()](#sqlalchemy.sql.expression.over) is usually called using
the [FunctionElement.over()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.over) method, e.g.:

```
func.row_number().over(order_by=mytable.c.some_column)
```

Would produce:

```
ROW_NUMBER() OVER(ORDER BY some_column)
```

Ranges are also possible using the [over.range_](#sqlalchemy.sql.expression.over.params.range_),
[over.rows](#sqlalchemy.sql.expression.over.params.rows), and [over.groups](#sqlalchemy.sql.expression.over.params.groups)
parameters.  These
mutually-exclusive parameters each accept a 2-tuple, which contains
a combination of integers and None:

```
func.row_number().over(order_by=my_table.c.some_column, range_=(None, 0))
```

The above would produce:

```
ROW_NUMBER() OVER(ORDER BY some_column
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

A value of `None` indicates “unbounded”, a
value of zero indicates “current row”, and negative / positive
integers indicate “preceding” and “following”:

- RANGE BETWEEN 5 PRECEDING AND 10 FOLLOWING:
  ```
  func.row_number().over(order_by="x", range_=(-5, 10))
  ```
- ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW:
  ```
  func.row_number().over(order_by="x", rows=(None, 0))
  ```
- RANGE BETWEEN 2 PRECEDING AND UNBOUNDED FOLLOWING:
  ```
  func.row_number().over(order_by="x", range_=(-2, None))
  ```
- RANGE BETWEEN 1 FOLLOWING AND 3 FOLLOWING:
  ```
  func.row_number().over(order_by="x", range_=(1, 3))
  ```
- GROUPS BETWEEN 1 FOLLOWING AND 3 FOLLOWING:
  ```
  func.row_number().over(order_by="x", groups=(1, 3))
  ```

  Parameters:

- **element** – a [FunctionElement](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement), [WithinGroup](#sqlalchemy.sql.expression.WithinGroup),
  or other compatible construct.
- **partition_by** – a column element or string, or a list
  of such, that will be used as the PARTITION BY clause
  of the OVER construct.
- **order_by** – a column element or string, or a list
  of such, that will be used as the ORDER BY clause
  of the OVER construct.
- **range_** – optional range clause for the window.  This is a
  tuple value which can contain integer values or `None`,
  and will render a RANGE BETWEEN PRECEDING / FOLLOWING clause.
- **rows** – optional rows clause for the window.  This is a tuple
  value which can contain integer values or None, and will render
  a ROWS BETWEEN PRECEDING / FOLLOWING clause.
- **groups** –
  optional groups clause for the window.  This is a
  tuple value which can contain integer values or `None`,
  and will render a GROUPS BETWEEN PRECEDING / FOLLOWING clause.
  Added in version 2.0.40.

This function is also available from the [func](#sqlalchemy.sql.expression.func)
construct itself via the [FunctionElement.over()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.over) method.

See also

[Using Window Functions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-window-functions) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[func](#sqlalchemy.sql.expression.func)

[within_group()](#sqlalchemy.sql.expression.within_group)

     function sqlalchemy.sql.expression.within_group(*element:FunctionElement[_T]*, **order_by:_ColumnExpressionArgument[Any]*) → [WithinGroup](#sqlalchemy.sql.expression.WithinGroup)[_T]

Produce a [WithinGroup](#sqlalchemy.sql.expression.WithinGroup) object against a function.

Used against so-called “ordered set aggregate” and “hypothetical
set aggregate” functions, including [percentile_cont](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percentile_cont),
[rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.rank), [dense_rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.dense_rank), etc.

[within_group()](#sqlalchemy.sql.expression.within_group) is usually called using
the [FunctionElement.within_group()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.within_group) method, e.g.:

```
from sqlalchemy import within_group

stmt = select(
    department.c.id,
    func.percentile_cont(0.5).within_group(department.c.salary.desc()),
)
```

The above statement would produce SQL similar to
`SELECT department.id, percentile_cont(0.5)
WITHIN GROUP (ORDER BY department.salary DESC)`.

  Parameters:

- **element** – a [FunctionElement](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement) construct, typically
  generated by [func](#sqlalchemy.sql.expression.func).
- ***order_by** – one or more column elements that will be used
  as the ORDER BY clause of the WITHIN GROUP construct.

See also

[Special Modifiers WITHIN GROUP, FILTER](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-functions-within-group) - in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[func](#sqlalchemy.sql.expression.func)

[over()](#sqlalchemy.sql.expression.over)

## Column Element Class Documentation

The classes here are generated using the constructors listed at
[Column Element Foundational Constructors](#sqlelement-foundational-constructors) and
[Column Element Modifier Constructors](#sqlelement-modifier-constructors).

| Object Name | Description |
| --- | --- |
| BinaryExpression | Represent an expression that isLEFT<operator>RIGHT. |
| BindParameter | Represent a “bound expression”. |
| Case | Represent aCASEexpression. |
| Cast | Represent aCASTexpression. |
| ClauseList | Describe a list of clauses, separated by an operator. |
| ColumnClause | Represents a column expression from any textual string. |
| ColumnCollection | Collection ofColumnElementinstances,
typically forFromClauseobjects. |
| ColumnElement | Represent a column-oriented SQL expression suitable for usage in the
“columns” clause, WHERE clause etc. of a statement. |
| ColumnExpressionArgument | General purpose “column expression” argument. |
| ColumnOperators | Defines boolean, comparison, and other operators forColumnElementexpressions. |
| Extract | Represent a SQL EXTRACT clause,extract(fieldFROMexpr). |
| False_ | Represent thefalsekeyword, or equivalent, in a SQL statement. |
| FunctionFilter | Represent a function FILTER clause. |
| Label | Represents a column label (AS). |
| Null | Represent the NULL keyword in a SQL statement. |
| Operators | Base of comparison and logical operators. |
| Over | Represent an OVER clause. |
| SQLColumnExpression | A type that may be used to indicate any SQL column element or object
that acts in place of one. |
| TextClause | Represent a literal SQL text fragment. |
| True_ | Represent thetruekeyword, or equivalent, in a SQL statement. |
| TryCast | Represent a TRY_CAST expression. |
| Tuple | Represent a SQL tuple. |
| TypeCoerce | Represent a Python-side type-coercion wrapper. |
| UnaryExpression | Define a ‘unary’ expression. |
| WithinGroup | Represent a WITHIN GROUP (ORDER BY) clause. |
| WrapsColumnExpression | Mixin that defines aColumnElementas a wrapper with special
labeling behavior for an expression that already has a name. |

   class sqlalchemy.sql.expression.BinaryExpression

*inherits from* `sqlalchemy.sql.expression.OperatorExpression`

Represent an expression that is `LEFT <operator> RIGHT`.

A [BinaryExpression](#sqlalchemy.sql.expression.BinaryExpression) is generated automatically
whenever two column expressions are used in a Python binary expression:

```
>>> from sqlalchemy.sql import column
>>> column("a") + column("b")
<sqlalchemy.sql.expression.BinaryExpression object at 0x101029dd0>
>>> print(column("a") + column("b"))
a + b
```

     class sqlalchemy.sql.expression.BindParameter

*inherits from* `sqlalchemy.sql.roles.InElementRole`, `sqlalchemy.sql.expression.KeyedColumnElement`

Represent a “bound expression”.

[BindParameter](#sqlalchemy.sql.expression.BindParameter) is invoked explicitly using the
[bindparam()](#sqlalchemy.sql.expression.bindparam) function, as in:

```
from sqlalchemy import bindparam

stmt = select(users_table).where(
    users_table.c.name == bindparam("username")
)
```

Detailed discussion of how [BindParameter](#sqlalchemy.sql.expression.BindParameter) is used is
at [bindparam()](#sqlalchemy.sql.expression.bindparam).

See also

[bindparam()](#sqlalchemy.sql.expression.bindparam)

| Member Name | Description |
| --- | --- |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| render_literal_execute() | Produce a copy of this bound parameter that will enable theBindParameter.literal_executeflag. |

   property effective_value: _T | None

Return the value of this bound parameter,
taking into account if the `callable` parameter
was set.

The `callable` value will be evaluated
and returned if present, else `value`.

    attribute [sqlalchemy.sql.expression.BindParameter.](#sqlalchemy.sql.expression.BindParameter)inherit_cache = True

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

     method [sqlalchemy.sql.expression.BindParameter.](#sqlalchemy.sql.expression.BindParameter)render_literal_execute() → [BindParameter](#sqlalchemy.sql.expression.BindParameter)[_T]

Produce a copy of this bound parameter that will enable the
[BindParameter.literal_execute](#sqlalchemy.sql.expression.BindParameter.params.literal_execute) flag.

The [BindParameter.literal_execute](#sqlalchemy.sql.expression.BindParameter.params.literal_execute) flag will
have the effect of the parameter rendered in the compiled SQL
string using `[POSTCOMPILE]` form, which is a special form that
is converted to be a rendering of the literal value of the parameter
at SQL execution time.    The rationale is to support caching
of SQL statement strings that can embed per-statement literal values,
such as LIMIT and OFFSET parameters, in the final SQL string that
is passed to the DBAPI.   Dialects in particular may want to use
this method within custom compilation schemes.

Added in version 1.4.5.

See also

[Caching for Third Party Dialects](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-thirdparty-caching)

      class sqlalchemy.sql.expression.Case

*inherits from* [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent a `CASE` expression.

[Case](#sqlalchemy.sql.expression.Case) is produced using the [case()](#sqlalchemy.sql.expression.case) factory function,
as in:

```
from sqlalchemy import case

stmt = select(users_table).where(
    case(
        (users_table.c.name == "wendy", "W"),
        (users_table.c.name == "jack", "J"),
        else_="E",
    )
)
```

Details on [Case](#sqlalchemy.sql.expression.Case) usage is at [case()](#sqlalchemy.sql.expression.case).

See also

[case()](#sqlalchemy.sql.expression.case)

     class sqlalchemy.sql.expression.Cast

*inherits from* `sqlalchemy.sql.expression.WrapsColumnExpression`

Represent a `CAST` expression.

[Cast](#sqlalchemy.sql.expression.Cast) is produced using the [cast()](#sqlalchemy.sql.expression.cast) factory function,
as in:

```
from sqlalchemy import cast, Numeric

stmt = select(cast(product_table.c.unit_price, Numeric(10, 4)))
```

Details on [Cast](#sqlalchemy.sql.expression.Cast) usage is at [cast()](#sqlalchemy.sql.expression.cast).

See also

[Data Casts and Type Coercion](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-casts)

[cast()](#sqlalchemy.sql.expression.cast)

[try_cast()](#sqlalchemy.sql.expression.try_cast)

[type_coerce()](#sqlalchemy.sql.expression.type_coerce) - an alternative to CAST that coerces the type
on the Python side only, which is often sufficient to generate the
correct SQL and data coercion.

     class sqlalchemy.sql.expression.ClauseList

*inherits from* `sqlalchemy.sql.roles.InElementRole`, `sqlalchemy.sql.roles.OrderByRole`, `sqlalchemy.sql.roles.ColumnsClauseRole`, `sqlalchemy.sql.roles.DMLColumnRole`, `sqlalchemy.sql.expression.DQLDMLClauseElement`

Describe a list of clauses, separated by an operator.

By default, is comma-separated, such as a column listing.

| Member Name | Description |
| --- | --- |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |

   method [sqlalchemy.sql.expression.ClauseList.](#sqlalchemy.sql.expression.ClauseList)self_group(*against:OperatorType|None=None*) → Self | Grouping[Any]

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.ClauseList.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.ClauseList.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

     class sqlalchemy.sql.expression.ColumnClause

*inherits from* `sqlalchemy.sql.roles.DDLReferredColumnRole`, `sqlalchemy.sql.roles.LabeledColumnExprRole`, `sqlalchemy.sql.roles.StrAsPlainColumnRole`, `sqlalchemy.sql.expression.Immutable`, `sqlalchemy.sql.expression.NamedColumn`

Represents a column expression from any textual string.

The [ColumnClause](#sqlalchemy.sql.expression.ColumnClause), a lightweight analogue to the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) class, is typically invoked using the
[column()](#sqlalchemy.sql.expression.column) function, as in:

```
from sqlalchemy import column

id, name = column("id"), column("name")
stmt = select(id, name).select_from("user")
```

The above statement would produce SQL like:

```
SELECT id, name FROM user
```

[ColumnClause](#sqlalchemy.sql.expression.ColumnClause) is the immediate superclass of the schema-specific
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object.  While the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
class has all the
same capabilities as [ColumnClause](#sqlalchemy.sql.expression.ColumnClause), the [ColumnClause](#sqlalchemy.sql.expression.ColumnClause)
class is usable by itself in those cases where behavioral requirements
are limited to simple SQL expression generation.  The object has none of
the associations with schema-level metadata or with execution-time
behavior that [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) does,
so in that sense is a “lightweight”
version of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

Full details on [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) usage is at
[column()](#sqlalchemy.sql.expression.column).

See also

[column()](#sqlalchemy.sql.expression.column)

[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)

| Member Name | Description |
| --- | --- |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |

   method [sqlalchemy.sql.expression.ColumnClause.](#sqlalchemy.sql.expression.ColumnClause)get_children(***, *column_tables=False*, ***kw*)

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

     class sqlalchemy.sql.expression.ColumnCollection

*inherits from* `typing.Generic`

Collection of [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) instances,
typically for
[FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) objects.

The [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) object is most commonly available
as the [Table.c](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.c) or [Table.columns](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.columns) collection
on the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, introduced at
[Accessing Tables and Columns](https://docs.sqlalchemy.org/en/20/core/metadata.html#metadata-tables-and-columns).

The [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) has both mapping- and sequence-
like behaviors. A [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) usually stores
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects, which are then accessible both via mapping
style access as well as attribute access style.

To access [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects using ordinary attribute-style
access, specify the name like any other object attribute, such as below
a column named `employee_name` is accessed:

```
>>> employee_table.c.employee_name
```

To access columns that have names with special characters or spaces,
index-style access is used, such as below which illustrates a column named
`employee ' payment` is accessed:

```
>>> employee_table.c["employee ' payment"]
```

As the [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) object provides a Python dictionary
interface, common dictionary method names like
[ColumnCollection.keys()](#sqlalchemy.sql.expression.ColumnCollection.keys), [ColumnCollection.values()](#sqlalchemy.sql.expression.ColumnCollection.values),
and [ColumnCollection.items()](#sqlalchemy.sql.expression.ColumnCollection.items) are available, which means that
database columns that are keyed under these names also need to use indexed
access:

```
>>> employee_table.c["values"]
```

The name for which a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) would be present is normally
that of the [Column.key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.key) parameter.  In some contexts,
such as a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object that uses a label style set
using the [Select.set_label_style()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.set_label_style) method, a column of a certain
key may instead be represented under a particular label name such
as `tablename_columnname`:

```
>>> from sqlalchemy import select, column, table
>>> from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
>>> t = table("t", column("c"))
>>> stmt = select(t).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
>>> subq = stmt.subquery()
>>> subq.c.t_c
<sqlalchemy.sql.elements.ColumnClause at 0x7f59dcf04fa0; t_c>
```

[ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) also indexes the columns in order and allows
them to be accessible by their integer position:

```
>>> cc[0]
Column('x', Integer(), table=None)
>>> cc[1]
Column('y', Integer(), table=None)
```

Added in version 1.4: [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection)
allows integer-based
index access to the collection.

Iterating the collection yields the column expressions in order:

```
>>> list(cc)
[Column('x', Integer(), table=None),
 Column('y', Integer(), table=None)]
```

The base [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) object can store
duplicates, which can
mean either two columns with the same key, in which case the column
returned by key  access is **arbitrary**:

```
>>> x1, x2 = Column("x", Integer), Column("x", Integer)
>>> cc = ColumnCollection(columns=[(x1.name, x1), (x2.name, x2)])
>>> list(cc)
[Column('x', Integer(), table=None),
 Column('x', Integer(), table=None)]
>>> cc["x"] is x1
False
>>> cc["x"] is x2
True
```

Or it can also mean the same column multiple times.   These cases are
supported as [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection)
is used to represent the columns in
a SELECT statement which may include duplicates.

A special subclass `DedupeColumnCollection` exists which instead
maintains SQLAlchemy’s older behavior of not allowing duplicates; this
collection is used for schema level objects like [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
and
[PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) where this deduping is helpful.  The
`DedupeColumnCollection` class also has additional mutation methods
as the schema constructs have more use cases that require removal and
replacement of columns.

Changed in version 1.4: [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection)
now stores duplicate
column keys as well as the same column in multiple positions.  The
`DedupeColumnCollection` class is added to maintain the
former behavior in those cases where deduplication as well as
additional replace/remove operations are needed.

| Member Name | Description |
| --- | --- |
| add() | Add a column to thisColumnCollection. |
| as_readonly() | Return a “read only” form of thisColumnCollection. |
| clear() | Dictionary clear() is not implemented forColumnCollection. |
| compare() | Compare thisColumnCollectionto another
based on the names of the keys |
| contains_column() | Checks if a column object exists in this collection |
| corresponding_column() | Given aColumnElement, return the exportedColumnElementobject from thisColumnCollectionwhich corresponds to that originalColumnElementvia a common
ancestor column. |
| get() | Get aColumnClauseorColumnobject
based on a string key name from thisColumnCollection. |
| items() | Return a sequence of (key, column) tuples for all columns in this
collection each consisting of a string key name and aColumnClauseorColumnobject. |
| keys() | Return a sequence of string key names for all columns in this
collection. |
| update() | Dictionary update() is not implemented forColumnCollection. |
| values() | Return a sequence ofColumnClauseorColumnobjects for all columns in this
collection. |

   method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)add(*column:ColumnElement[Any]*, *key:_COLKEY|None=None*) → None

Add a column to this [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection).

Note

This method is **not normally used by user-facing code**, as the
[ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) is usually part of an existing
object such as a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table). To add a
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) to an existing [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object, use the [Table.append_column()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.append_column) method.

     method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)as_readonly() → ReadOnlyColumnCollection[_COLKEY, _COL_co]

Return a “read only” form of this
[ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection).

    method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)clear() → NoReturn

Dictionary clear() is not implemented for
[ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection).

    method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)compare(*other:ColumnCollection[_COLKEY,_COL_co]*) → bool

Compare this [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) to another
based on the names of the keys

    method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)contains_column(*col:ColumnElement[Any]*) → bool

Checks if a column object exists in this collection

    method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)corresponding_column(*column:_COL*, *require_embedded:bool=False*) → _COL | _COL_co | None

Given a [ColumnElement](#sqlalchemy.sql.expression.ColumnElement), return the exported
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement) object from this
[ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection)
which corresponds to that original [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
via a common
ancestor column.

  Parameters:

- **column** – the target [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
  to be matched.
- **require_embedded** – only return corresponding columns for
  the given [ColumnElement](#sqlalchemy.sql.expression.ColumnElement), if the given
  [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
  is actually present within a sub-element
  of this [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable).
  Normally the column will match if
  it merely shares a common ancestor with one of the exported
  columns of this [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable).

See also

[Selectable.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.corresponding_column)
- invokes this method
against the collection returned by
[Selectable.exported_columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.exported_columns).

Changed in version 1.4: the implementation for `corresponding_column`
was moved onto the [ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection) itself.

     method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)get(*key:str*, *default:_COL|None=None*) → _COL | _COL_co | None

Get a [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) or [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object
based on a string key name from this
[ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection).

    method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)items() → List[Tuple[_COLKEY, _COL_co]]

Return a sequence of (key, column) tuples for all columns in this
collection each consisting of a string key name and a
[ColumnClause](#sqlalchemy.sql.expression.ColumnClause) or
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object.

    method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)keys() → List[_COLKEY]

Return a sequence of string key names for all columns in this
collection.

    method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)update(*iter_:Any*) → NoReturn

Dictionary update() is not implemented for
[ColumnCollection](#sqlalchemy.sql.expression.ColumnCollection).

    method [sqlalchemy.sql.expression.ColumnCollection.](#sqlalchemy.sql.expression.ColumnCollection)values() → List[_COL_co]

Return a sequence of [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) or
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects for all columns in this
collection.

     class sqlalchemy.sql.expression.ColumnElement

*inherits from* `sqlalchemy.sql.roles.ColumnArgumentOrKeyRole`, `sqlalchemy.sql.roles.StatementOptionRole`, `sqlalchemy.sql.roles.WhereHavingRole`, `sqlalchemy.sql.roles.BinaryElementRole`, `sqlalchemy.sql.roles.OrderByRole`, `sqlalchemy.sql.roles.ColumnsClauseRole`, `sqlalchemy.sql.roles.LimitOffsetRole`, `sqlalchemy.sql.roles.DMLColumnRole`, `sqlalchemy.sql.roles.DDLConstraintColumnRole`, `sqlalchemy.sql.roles.DDLExpressionRole`, [sqlalchemy.sql.expression.SQLColumnExpression](#sqlalchemy.sql.expression.SQLColumnExpression), `sqlalchemy.sql.expression.DQLDMLClauseElement`

Represent a column-oriented SQL expression suitable for usage in the
“columns” clause, WHERE clause etc. of a statement.

While the most familiar kind of [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) is the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object, [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
serves as the basis
for any unit that may be present in a SQL expression, including
the expressions themselves, SQL functions, bound parameters,
literal expressions, keywords such as `NULL`, etc.
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
is the ultimate base class for all such elements.

A wide variety of SQLAlchemy Core functions work at the SQL expression
level, and are intended to accept instances of
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement) as
arguments.  These functions will typically document that they accept a
“SQL expression” as an argument.  What this means in terms of SQLAlchemy
usually refers to an input which is either already in the form of a
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement) object,
or a value which can be **coerced** into
one.  The coercion rules followed by most, but not all, SQLAlchemy Core
functions with regards to SQL expressions are as follows:

> - a literal Python value, such as a string, integer or floating
>   point value, boolean, datetime, `Decimal` object, or virtually
>   any other Python object, will be coerced into a “literal bound
>   value”.  This generally means that a [bindparam()](#sqlalchemy.sql.expression.bindparam) will be
>   produced featuring the given value embedded into the construct; the
>   resulting [BindParameter](#sqlalchemy.sql.expression.BindParameter) object is an instance of
>   [ColumnElement](#sqlalchemy.sql.expression.ColumnElement).
>   The Python value will ultimately be sent
>   to the DBAPI at execution time as a parameterized argument to the
>   `execute()` or `executemany()` methods, after SQLAlchemy
>   type-specific converters (e.g. those provided by any associated
>   [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) objects) are applied to the value.
> - any special object value, typically ORM-level constructs, which
>   feature an accessor called `__clause_element__()`.  The Core
>   expression system looks for this method when an object of otherwise
>   unknown type is passed to a function that is looking to coerce the
>   argument into a [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) and sometimes a
>   [SelectBase](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase) expression.
>   It is used within the ORM to
>   convert from ORM-specific objects like mapped classes and
>   mapped attributes into Core expression objects.
> - The Python `None` value is typically interpreted as `NULL`,
>   which in SQLAlchemy Core produces an instance of [null()](#sqlalchemy.sql.expression.null).

A [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) provides the ability to generate new
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
objects using Python expressions.  This means that Python operators
such as `==`, `!=` and `<` are overloaded to mimic SQL operations,
and allow the instantiation of further [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
instances
which are composed from other, more fundamental
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
objects.  For example, two [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) objects can be added
together with the addition operator `+` to produce
a [BinaryExpression](#sqlalchemy.sql.expression.BinaryExpression).
Both [ColumnClause](#sqlalchemy.sql.expression.ColumnClause) and [BinaryExpression](#sqlalchemy.sql.expression.BinaryExpression) are subclasses
of [ColumnElement](#sqlalchemy.sql.expression.ColumnElement):

```
>>> from sqlalchemy.sql import column
>>> column("a") + column("b")
<sqlalchemy.sql.expression.BinaryExpression object at 0x101029dd0>
>>> print(column("a") + column("b"))
a + b
```

See also

[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)

[column()](#sqlalchemy.sql.expression.column)

| Member Name | Description |
| --- | --- |
| __eq__() | Implement the==operator. |
| __le__() | Implement the<=operator. |
| __lt__() | Implement the<operator. |
| __ne__() | Implement the!=operator. |
| all_() | Produce anall_()clause against the
parent object. |
| allows_lambda |  |
| any_() | Produce anany_()clause against the
parent object. |
| asc() | Produce aasc()clause against the
parent object. |
| base_columns |  |
| between() | Produce abetween()clause against
the parent object, given the lower and upper range. |
| bitwise_and() | Produce a bitwise AND operation, typically via the&operator. |
| bitwise_lshift() | Produce a bitwise LSHIFT operation, typically via the<<operator. |
| bitwise_not() | Produce a bitwise NOT operation, typically via the~operator. |
| bitwise_or() | Produce a bitwise OR operation, typically via the|operator. |
| bitwise_rshift() | Produce a bitwise RSHIFT operation, typically via the>>operator. |
| bitwise_xor() | Produce a bitwise XOR operation, typically via the^operator, or#for PostgreSQL. |
| bool_op() | Return a custom boolean operator. |
| cast() | Produce a type cast, i.e.CAST(<expression>AS<type>). |
| collate() | Produce acollate()clause against
the parent object, given the collation string. |
| comparator |  |
| compare() | Compare thisClauseElementto
the givenClauseElement. |
| compile() | Compile this SQL expression. |
| concat() | Implement the ‘concat’ operator. |
| contains() | Implement the ‘contains’ operator. |
| desc() | Produce adesc()clause against the
parent object. |
| description |  |
| distinct() | Produce adistinct()clause against the
parent object. |
| endswith() | Implement the ‘endswith’ operator. |
| entity_namespace |  |
| foreign_keys |  |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| icontains() | Implement theicontainsoperator, e.g. case insensitive
version ofColumnOperators.contains(). |
| iendswith() | Implement theiendswithoperator, e.g. case insensitive
version ofColumnOperators.endswith(). |
| ilike() | Implement theilikeoperator, e.g. case insensitive LIKE. |
| in_() | Implement theinoperator. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| is_() | Implement theISoperator. |
| is_clause_element |  |
| is_distinct_from() | Implement theISDISTINCTFROMoperator. |
| is_dml |  |
| is_not() | Implement theISNOToperator. |
| is_not_distinct_from() | Implement theISNOTDISTINCTFROMoperator. |
| is_selectable |  |
| isnot() | Implement theISNOToperator. |
| isnot_distinct_from() | Implement theISNOTDISTINCTFROMoperator. |
| istartswith() | Implement theistartswithoperator, e.g. case insensitive
version ofColumnOperators.startswith(). |
| key | The ‘key’ that in some circumstances refers to this object in a
Python namespace. |
| label() | Produce a column label, i.e.<columnname>AS<name>. |
| like() | Implement thelikeoperator. |
| match() | Implements a database-specific ‘match’ operator. |
| negation_clause |  |
| not_ilike() | implement theNOTILIKEoperator. |
| not_in() | implement theNOTINoperator. |
| not_like() | implement theNOTLIKEoperator. |
| notilike() | implement theNOTILIKEoperator. |
| notin_() | implement theNOTINoperator. |
| notlike() | implement theNOTLIKEoperator. |
| nulls_first() | Produce anulls_first()clause against the
parent object. |
| nulls_last() | Produce anulls_last()clause against the
parent object. |
| nullsfirst() | Produce anulls_first()clause against the
parent object. |
| nullslast() | Produce anulls_last()clause against the
parent object. |
| op() | Produce a generic operator function. |
| operate() | Operate on an argument. |
| params() | Return a copy withbindparam()elements
replaced. |
| primary_key |  |
| proxy_set | set of all columns we are proxying |
| regexp_match() | Implements a database-specific ‘regexp match’ operator. |
| regexp_replace() | Implements a database-specific ‘regexp replace’ operator. |
| reverse_operate() | Reverse operate on an argument. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| shares_lineage() | Return True if the givenColumnElementhas a common ancestor to thisColumnElement. |
| startswith() | Implement thestartswithoperator. |
| stringify_dialect |  |
| supports_execution |  |
| timetuple | Hack, allows datetime objects to be compared on the LHS. |
| type |  |
| unique_params() | Return a copy withbindparam()elements
replaced. |
| uses_inspection |  |

   method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)__eq__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__eq__` *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `==` operator.

In a column context, produces the clause `a = b`.
If the target is `None`, produces `a IS NULL`.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)__le__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__le__` *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<=` operator.

In a column context, produces the clause `a <= b`.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)__lt__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__lt__` *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<` operator.

In a column context, produces the clause `a < b`.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)__ne__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__ne__` *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `!=` operator.

In a column context, produces the clause `a != b`.
If the target is `None`, produces `a IS NOT NULL`.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)all_() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.all_()](#sqlalchemy.sql.expression.ColumnOperators.all_) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce an [all_()](#sqlalchemy.sql.expression.all_) clause against the
parent object.

See the documentation for [all_()](#sqlalchemy.sql.expression.all_) for examples.

Note

be sure to not confuse the newer
[ColumnOperators.all_()](#sqlalchemy.sql.expression.ColumnOperators.all_) method with the **legacy**
version of this method, the [Comparator.all()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.all)
method that’s specific to [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), which uses a
different calling style.

     attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)allows_lambda = True    property anon_key_label: str

Deprecated since version 1.4: The [ColumnElement.anon_key_label](#sqlalchemy.sql.expression.ColumnElement.anon_key_label) attribute is now private, and the public accessor is deprecated.

     property anon_label: str

Deprecated since version 1.4: The [ColumnElement.anon_label](#sqlalchemy.sql.expression.ColumnElement.anon_label) attribute is now private, and the public accessor is deprecated.

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)any_() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.any_()](#sqlalchemy.sql.expression.ColumnOperators.any_) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce an [any_()](#sqlalchemy.sql.expression.any_) clause against the
parent object.

See the documentation for [any_()](#sqlalchemy.sql.expression.any_) for examples.

Note

be sure to not confuse the newer
[ColumnOperators.any_()](#sqlalchemy.sql.expression.ColumnOperators.any_) method with the **legacy**
version of this method, the [Comparator.any()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.any)
method that’s specific to [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), which uses a
different calling style.

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)asc() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.asc()](#sqlalchemy.sql.expression.ColumnOperators.asc) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [asc()](#sqlalchemy.sql.expression.asc) clause against the
parent object.

    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)base_columns    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)between(*cleft:Any*, *cright:Any*, *symmetric:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.between()](#sqlalchemy.sql.expression.ColumnOperators.between) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [between()](#sqlalchemy.sql.expression.between) clause against
the parent object, given the lower and upper range.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)bitwise_and(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_and()](#sqlalchemy.sql.expression.ColumnOperators.bitwise_and) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise AND operation, typically via the `&`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)bitwise_lshift(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_lshift()](#sqlalchemy.sql.expression.ColumnOperators.bitwise_lshift) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise LSHIFT operation, typically via the `<<`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)bitwise_not() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_not()](#sqlalchemy.sql.expression.ColumnOperators.bitwise_not) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise NOT operation, typically via the `~`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)bitwise_or(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_or()](#sqlalchemy.sql.expression.ColumnOperators.bitwise_or) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise OR operation, typically via the `|`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)bitwise_rshift(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_rshift()](#sqlalchemy.sql.expression.ColumnOperators.bitwise_rshift) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise RSHIFT operation, typically via the `>>`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)bitwise_xor(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_xor()](#sqlalchemy.sql.expression.ColumnOperators.bitwise_xor) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise XOR operation, typically via the `^`
operator, or `#` for PostgreSQL.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)bool_op(*opstring:str*, *precedence:int=0*, *python_impl:Callable[[...],Any]|None=None*) → Callable[[Any], [Operators](#sqlalchemy.sql.expression.Operators)]

*inherited from the* [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op) *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Return a custom boolean operator.

This method is shorthand for calling
[Operators.op()](#sqlalchemy.sql.expression.Operators.op) and passing the
[Operators.op.is_comparison](#sqlalchemy.sql.expression.Operators.op.params.is_comparison)
flag with True.    A key advantage to using [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op)
is that when using column constructs, the “boolean” nature of the
returned expression will be present for [PEP 484](https://peps.python.org/pep-0484/) purposes.

See also

[Operators.op()](#sqlalchemy.sql.expression.Operators.op)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)cast(*type_:_TypeEngineArgument[_OPT]*) → [Cast](#sqlalchemy.sql.expression.Cast)[_OPT]

Produce a type cast, i.e. `CAST(<expression> AS <type>)`.

This is a shortcut to the [cast()](#sqlalchemy.sql.expression.cast) function.

See also

[Data Casts and Type Coercion](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-casts)

[cast()](#sqlalchemy.sql.expression.cast)

[type_coerce()](#sqlalchemy.sql.expression.type_coerce)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)collate(*collation:str*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.collate()](#sqlalchemy.sql.expression.ColumnOperators.collate) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [collate()](#sqlalchemy.sql.expression.collate) clause against
the parent object, given the collation string.

See also

[collate()](#sqlalchemy.sql.expression.collate)

     attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)comparator    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)compare(*other:ClauseElement*, ***kw:Any*) → bool

*inherited from the* [ClauseElement.compare()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compare) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Compare this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) to
the given [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

Subclasses should override the default behavior, which is a
straight identity comparison.

**kw are arguments consumed by subclass `compare()` methods and
may be used to modify the criteria for comparison
(see [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)).

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

*inherited from the* `CompilerElement.compile()` *method of* `CompilerElement`

Compile this SQL expression.

The return value is a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.
Calling `str()` or `unicode()` on the returned value will yield a
string representation of the result. The
[Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object also can return a
dictionary of bind parameter names and values
using the `params` accessor.

  Parameters:

- **bind** – An [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which
  can provide a [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in order to generate a
  [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  If the `bind` and
  `dialect` parameters are both omitted, a default SQL compiler
  is used.
- **column_keys** – Used for INSERT and UPDATE statements, a list of
  column names which should be present in the VALUES clause of the
  compiled statement. If `None`, all columns from the target table
  object are rendered.
- **dialect** – A [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) instance which can generate
  a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  This argument takes precedence over
  the `bind` argument.
- **compile_kwargs** –
  optional dictionary of additional parameters
  that will be passed through to the compiler within all “visit”
  methods.  This allows any custom flag to be passed through to
  a custom compilation construct, for example.  It is also used
  for the case of passing the `literal_binds` flag through:
  ```
  from sqlalchemy.sql import table, column, select
  t = table("t", column("x"))
  s = select(t).where(t.c.x == 5)
  print(s.compile(compile_kwargs={"literal_binds": True}))
  ```

See also

[How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-string)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)concat(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.concat()](#sqlalchemy.sql.expression.ColumnOperators.concat) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘concat’ operator.

In a column context, produces the clause `a || b`,
or uses the `concat()` operator on MySQL.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)contains(*other:Any*, ***kw:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘contains’ operator.

Produces a LIKE expression that tests against a match for the middle
of a string value:

```
column LIKE '%' || <other> || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.contains("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.contains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.contains.escape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.contains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.contains("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.contains("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.contains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape):
  ```
  somecolumn.contains("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith)

[ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith)

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)desc() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.desc()](#sqlalchemy.sql.expression.ColumnOperators.desc) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [desc()](#sqlalchemy.sql.expression.desc) clause against the
parent object.

    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)description

*inherited from the* `ClauseElement.description` *attribute of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)distinct() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.distinct()](#sqlalchemy.sql.expression.ColumnOperators.distinct) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [distinct()](#sqlalchemy.sql.expression.distinct) clause against the
parent object.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)endswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘endswith’ operator.

Produces a LIKE expression that tests against a match for the end
of a string value:

```
column LIKE '%' || <other>
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.endswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.endswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.endswith.escape](#sqlalchemy.sql.expression.ColumnOperators.endswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.endswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.endswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.endswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.endswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape):
  ```
  somecolumn.endswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith)

[ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains)

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)entity_namespace

*inherited from the* `ClauseElement.entity_namespace` *attribute of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

     property expression: [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)[Any]

Return a column expression.

Part of the inspection interface; returns self.

    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)foreign_keys: AbstractSet[[ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)] = frozenset({})    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)icontains(*other:Any*, ***kw:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.icontains()](#sqlalchemy.sql.expression.ColumnOperators.icontains) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `icontains` operator, e.g. case insensitive
version of [ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains).

Produces a LIKE expression that tests against an insensitive match
for the middle of a string value:

```
lower(column) LIKE '%' || lower(<other>) || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.icontains("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.icontains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.icontains.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.icontains.escape](#sqlalchemy.sql.expression.ColumnOperators.icontains.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.icontains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.icontains.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.icontains("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.icontains("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.contains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape):
  ```
  somecolumn.icontains("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)iendswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.iendswith()](#sqlalchemy.sql.expression.ColumnOperators.iendswith) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `iendswith` operator, e.g. case insensitive
version of [ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith).

Produces a LIKE expression that tests against an insensitive match
for the end of a string value:

```
lower(column) LIKE '%' || lower(<other>)
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.iendswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.iendswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.iendswith.escape](#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.iendswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.iendswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.iendswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.iendswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape):
  ```
  somecolumn.endswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `ilike` operator, e.g. case insensitive LIKE.

In a column context, produces an expression either of the form:

```
lower(a) LIKE lower(other)
```

Or on backends that support the ILIKE operator:

```
a ILIKE other
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.ilike("%foobar%"))
```

   Parameters:

- **other** – expression to be compared
- **escape** –
  optional escape character, renders the `ESCAPE`
  keyword, e.g.:
  ```
  somecolumn.ilike("foo/%bar", escape="/")
  ```

See also

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)in_(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `in` operator.

In a column context, produces the clause `column IN <other>`.

The given parameter `other` may be:

- A list of literal values,
  e.g.:
  ```
  stmt.where(column.in_([1, 2, 3]))
  ```
  In this calling form, the list of items is converted to a set of
  bound parameters the same length as the list given:
  ```
  WHERE COL IN (?, ?, ?)
  ```
- A list of tuples may be provided if the comparison is against a
  [tuple_()](#sqlalchemy.sql.expression.tuple_) containing multiple expressions:
  ```
  from sqlalchemy import tuple_
  stmt.where(tuple_(col1, col2).in_([(1, 10), (2, 20), (3, 30)]))
  ```
- An empty list,
  e.g.:
  ```
  stmt.where(column.in_([]))
  ```
  In this calling form, the expression renders an “empty set”
  expression.  These expressions are tailored to individual backends
  and are generally trying to get an empty SELECT statement as a
  subquery.  Such as on SQLite, the expression is:
  ```
  WHERE col IN (SELECT 1 FROM (SELECT 1) WHERE 1!=1)
  ```
  Changed in version 1.4: empty IN expressions now use an
  execution-time generated SELECT subquery in all cases.
- A bound parameter, e.g. [bindparam()](#sqlalchemy.sql.expression.bindparam), may be used if it
  includes the [bindparam.expanding](#sqlalchemy.sql.expression.bindparam.params.expanding) flag:
  ```
  stmt.where(column.in_(bindparam("value", expanding=True)))
  ```
  In this calling form, the expression renders a special non-SQL
  placeholder expression that looks like:
  ```
  WHERE COL IN ([EXPANDING_value])
  ```
  This placeholder expression is intercepted at statement execution
  time to be converted into the variable number of bound parameter
  form illustrated earlier.   If the statement were executed as:
  ```
  connection.execute(stmt, {"value": [1, 2, 3]})
  ```
  The database would be passed a bound parameter for each value:
  ```
  WHERE COL IN (?, ?, ?)
  ```
  Added in version 1.2: added “expanding” bound parameters
  If an empty list is passed, a special “empty list” expression,
  which is specific to the database in use, is rendered.  On
  SQLite this would be:
  ```
  WHERE COL IN (SELECT 1 FROM (SELECT 1) WHERE 1!=1)
  ```
  Added in version 1.3: “expanding” bound parameters now support
  empty lists
- a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct, which is usually a
  correlated scalar select:
  ```
  stmt.where(
      column.in_(select(othertable.c.y).where(table.c.x == othertable.c.x))
  )
  ```
  In this calling form, [ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_) renders as given:
  ```
  WHERE COL IN (SELECT othertable.y
  FROM othertable WHERE othertable.x = table.x)
  ```

  Parameters:

**other** – a list of literals, a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
construct, or a [bindparam()](#sqlalchemy.sql.expression.bindparam) construct that includes the
[bindparam.expanding](#sqlalchemy.sql.expression.bindparam.params.expanding) flag set to True.

      attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)inherit_cache = None

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

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)is_(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_()](#sqlalchemy.sql.expression.ColumnOperators.is_) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS` operator.

Normally, `IS` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS` may be desirable if comparing to boolean values
on certain platforms.

See also

[ColumnOperators.is_not()](#sqlalchemy.sql.expression.ColumnOperators.is_not)

     attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)is_clause_element = True    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)is_distinct_from(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_distinct_from()](#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS DISTINCT FROM` operator.

Renders “a IS DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS NOT b”.

    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)is_dml = False    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)is_not(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_not()](#sqlalchemy.sql.expression.ColumnOperators.is_not) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT` operator.

Normally, `IS NOT` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS NOT` may be desirable if comparing to boolean values
on certain platforms.

Changed in version 1.4: The `is_not()` operator is renamed from
`isnot()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.is_()](#sqlalchemy.sql.expression.ColumnOperators.is_)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)is_not_distinct_from(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_not_distinct_from()](#sqlalchemy.sql.expression.ColumnOperators.is_not_distinct_from) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)is_selectable = False    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)isnot(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.isnot()](#sqlalchemy.sql.expression.ColumnOperators.isnot) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT` operator.

Normally, `IS NOT` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS NOT` may be desirable if comparing to boolean values
on certain platforms.

Changed in version 1.4: The `is_not()` operator is renamed from
`isnot()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.is_()](#sqlalchemy.sql.expression.ColumnOperators.is_)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)isnot_distinct_from(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.isnot_distinct_from()](#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)istartswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.istartswith()](#sqlalchemy.sql.expression.ColumnOperators.istartswith) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `istartswith` operator, e.g. case insensitive
version of [ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith).

Produces a LIKE expression that tests against an insensitive
match for the start of a string value:

```
lower(column) LIKE lower(<other>) || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.istartswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.istartswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.istartswith.escape](#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.escape) parameter will
establish a given character as an escape character which can be of
use when the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.istartswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.istartswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE lower(:param) || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.istartswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE lower(:param) || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.istartswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape):
  ```
  somecolumn.istartswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith)

     attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)key: str | None = None

The ‘key’ that in some circumstances refers to this object in a
Python namespace.

This typically refers to the “key” of the column as present in the
`.c` collection of a selectable, e.g. `sometable.c["somekey"]` would
return a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) with a `.key` of “somekey”.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)label(*name:str|None*) → [Label](#sqlalchemy.sql.expression.Label)[_T]

Produce a column label, i.e. `<columnname> AS <name>`.

This is a shortcut to the [label()](#sqlalchemy.sql.expression.label) function.

If ‘name’ is `None`, an anonymous label name will be generated.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `like` operator.

In a column context, produces the expression:

```
a LIKE other
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.like("%foobar%"))
```

   Parameters:

- **other** – expression to be compared
- **escape** –
  optional escape character, renders the `ESCAPE`
  keyword, e.g.:
  ```
  somecolumn.like("foo/%bar", escape="/")
  ```

See also

[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)match(*other:Any*, ***kwargs:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.match()](#sqlalchemy.sql.expression.ColumnOperators.match) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘match’ operator.

[ColumnOperators.match()](#sqlalchemy.sql.expression.ColumnOperators.match) attempts to resolve to
a MATCH-like function or operator provided by the backend.
Examples include:

- PostgreSQL - renders `x @@ plainto_tsquery(y)`
  > Changed in version 2.0: `plainto_tsquery()` is used instead
  > of `to_tsquery()` for PostgreSQL now; for compatibility with
  > other forms, see [Full Text Search](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-match).
- MySQL - renders `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
  See also
  [match](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.match) - MySQL specific construct with
  additional features.
- Oracle Database - renders `CONTAINS(x, y)`
- other backends may provide special implementations.
- Backends without any special implementation will emit
  the operator as “MATCH”.  This is compatible with SQLite, for
  example.

    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)negation_clause    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)not_ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_ilike()](#sqlalchemy.sql.expression.ColumnOperators.not_ilike) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)not_in(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_in()](#sqlalchemy.sql.expression.ColumnOperators.not_in) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT IN` operator.

This is equivalent to using negation with
[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_), i.e. `~x.in_(y)`.

In the case that `other` is an empty sequence, the compiler
produces an “empty not in” expression.   This defaults to the
expression “1 = 1” to produce true in all cases.  The
[create_engine.empty_in_strategy](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.empty_in_strategy) may be used to
alter this behavior.

Changed in version 1.4: The `not_in()` operator is renamed from
`notin_()` in previous releases.  The previous name remains
available for backwards compatibility.

Changed in version 1.2: The [ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_) and
[ColumnOperators.not_in()](#sqlalchemy.sql.expression.ColumnOperators.not_in) operators
now produce a “static” expression for an empty IN sequence
by default.

See also

[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)not_like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_like()](#sqlalchemy.sql.expression.ColumnOperators.not_like) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)notilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notilike()](#sqlalchemy.sql.expression.ColumnOperators.notilike) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)notin_(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notin_()](#sqlalchemy.sql.expression.ColumnOperators.notin_) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT IN` operator.

This is equivalent to using negation with
[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_), i.e. `~x.in_(y)`.

In the case that `other` is an empty sequence, the compiler
produces an “empty not in” expression.   This defaults to the
expression “1 = 1” to produce true in all cases.  The
[create_engine.empty_in_strategy](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.empty_in_strategy) may be used to
alter this behavior.

Changed in version 1.4: The `not_in()` operator is renamed from
`notin_()` in previous releases.  The previous name remains
available for backwards compatibility.

Changed in version 1.2: The [ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_) and
[ColumnOperators.not_in()](#sqlalchemy.sql.expression.ColumnOperators.not_in) operators
now produce a “static” expression for an empty IN sequence
by default.

See also

[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)notlike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notlike()](#sqlalchemy.sql.expression.ColumnOperators.notlike) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)nulls_first() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_first()](#sqlalchemy.sql.expression.ColumnOperators.nulls_first) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)nulls_last() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_last()](#sqlalchemy.sql.expression.ColumnOperators.nulls_last) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)nullsfirst() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullsfirst()](#sqlalchemy.sql.expression.ColumnOperators.nullsfirst) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)nullslast() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullslast()](#sqlalchemy.sql.expression.ColumnOperators.nullslast) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)op(*opstring:str*, *precedence:int=0*, *is_comparison:bool=False*, *return_type:Type[TypeEngine[Any]]|TypeEngine[Any]|None=None*, *python_impl:Callable[...,Any]|None=None*) → Callable[[Any], [Operators](#sqlalchemy.sql.expression.Operators)]

*inherited from the* [Operators.op()](#sqlalchemy.sql.expression.Operators.op) *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Produce a generic operator function.

e.g.:

```
somecolumn.op("*")(5)
```

produces:

```
somecolumn * 5
```

This function can also be used to make bitwise operators explicit. For
example:

```
somecolumn.op("&")(0xFF)
```

is a bitwise AND of the value in `somecolumn`.

  Parameters:

- **opstring** – a string which will be output as the infix operator
  between this element and the expression passed to the
  generated function.
- **precedence** –
  precedence which the database is expected to apply
  to the operator in SQL expressions. This integer value acts as a hint
  for the SQL compiler to know when explicit parenthesis should be
  rendered around a particular operation. A lower number will cause the
  expression to be parenthesized when applied against another operator
  with higher precedence. The default value of `0` is lower than all
  operators except for the comma (`,`) and `AS` operators. A value
  of 100 will be higher or equal to all operators, and -100 will be
  lower than or equal to all operators.
  See also
  [I’m using op() to generate a custom operator and my parenthesis are not coming out correctly](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-op-parenthesis) - detailed description
  of how the SQLAlchemy SQL compiler renders parenthesis
- **is_comparison** –
  legacy; if True, the operator will be considered
  as a “comparison” operator, that is which evaluates to a boolean
  true/false value, like `==`, `>`, etc.  This flag is provided
  so that ORM relationships can establish that the operator is a
  comparison operator when used in a custom join condition.
  Using the `is_comparison` parameter is superseded by using the
  [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op) method instead;  this more succinct
  operator sets this parameter automatically, but also provides
  correct [PEP 484](https://peps.python.org/pep-0484/) typing support as the returned object will
  express a “boolean” datatype, i.e. `BinaryExpression[bool]`.
- **return_type** – a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or object that will
  force the return type of an expression produced by this operator
  to be of that type.   By default, operators that specify
  [Operators.op.is_comparison](#sqlalchemy.sql.expression.Operators.op.params.is_comparison) will resolve to
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean), and those that do not will be of the same
  type as the left-hand operand.
- **python_impl** –
  an optional Python function that can evaluate
  two Python values in the same way as this operator works when
  run on the database server.  Useful for in-Python SQL expression
  evaluation functions, such as for ORM hybrid attributes, and the
  ORM “evaluator” used to match objects in a session after a multi-row
  update or delete.
  e.g.:
  ```
  >>> expr = column("x").op("+", python_impl=lambda a, b: a + b)("y")
  ```
  The operator for the above expression will also work for non-SQL
  left and right objects:
  ```
  >>> expr.operator(5, 10)
  15
  ```
  Added in version 2.0.

See also

[Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op)

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[Using custom operators in join conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-operator)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)[Any]

Operate on an argument.

This is the lowest level of operation, raises
`NotImplementedError` by default.

Overriding this on a subclass can allow common
behavior to be applied to all operations.
For example, overriding [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)
to apply `func.lower()` to the left and right
side:

```
class MyComparator(ColumnOperators):
    def operate(self, op, other, **kwargs):
        return op(func.lower(self), func.lower(other), **kwargs)
```

   Parameters:

- **op** – Operator callable.
- ***other** – the ‘other’ side of the operation. Will
  be a single scalar for most operations.
- ****kwargs** – modifiers.  These may be passed by special
  operators such as [ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains).

      method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)params(*_ClauseElement__optionaldict:Mapping[str,Any]|None=None*, ***kwargs:Any*) → Self

*inherited from the* [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Return a copy with [bindparam()](#sqlalchemy.sql.expression.bindparam) elements
replaced.

Returns a copy of this ClauseElement with
[bindparam()](#sqlalchemy.sql.expression.bindparam)
elements replaced with values taken from the given dictionary:

```
>>> clause = column("x") + bindparam("foo")
>>> print(clause.compile().params)
{'foo':None}
>>> print(clause.params({"foo": 7}).compile().params)
{'foo':7}
```

     attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)primary_key: bool = False    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)proxy_set

set of all columns we are proxying

as of 2.0 this is explicitly deannotated columns.  previously it was
effectively deannotated columns but wasn’t enforced.  annotated
columns should basically not go into sets if at all possible because
their hashing behavior is very non-performant.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)regexp_match(*pattern:Any*, *flags:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.regexp_match()](#sqlalchemy.sql.expression.ColumnOperators.regexp_match) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘regexp match’ operator.

E.g.:

```
stmt = select(table.c.some_column).where(
    table.c.some_column.regexp_match("^(b|c)")
)
```

[ColumnOperators.regexp_match()](#sqlalchemy.sql.expression.ColumnOperators.regexp_match) attempts to resolve to
a REGEXP-like function or operator provided by the backend, however
the specific regular expression syntax and flags available are
**not backend agnostic**.

Examples include:

- PostgreSQL - renders `x ~ y` or `x !~ y` when negated.
- Oracle Database - renders `REGEXP_LIKE(x, y)`
- SQLite - uses SQLite’s `REGEXP` placeholder operator and calls into
  the Python `re.match()` builtin.
- other backends may provide special implementations.
- Backends without any special implementation will emit
  the operator as “REGEXP” or “NOT REGEXP”.  This is compatible with
  SQLite and MySQL, for example.

Regular expression support is currently implemented for Oracle
Database, PostgreSQL, MySQL and MariaDB.  Partial support is available
for SQLite.  Support among third-party dialects may vary.

  Parameters:

- **pattern** – The regular expression pattern string or column
  clause.
- **flags** – Any regular expression string flags to apply, passed as
  plain Python string only.  These flags are backend specific.
  Some backends, like PostgreSQL and MariaDB, may alternatively
  specify the flags as part of the pattern.
  When using the ignore case flag ‘i’ in PostgreSQL, the ignore case
  regexp match operator `~*` or `!~*` will be used.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18  Note that due to an implementation
error, the “flags” parameter previously accepted SQL expression
objects such as column expressions in addition to plain Python
strings.   This implementation did not work correctly with caching
and was removed; strings only should be passed for the “flags”
parameter, as these flags are rendered as literal inline values
within SQL expressions.

See also

[ColumnOperators.regexp_replace()](#sqlalchemy.sql.expression.ColumnOperators.regexp_replace)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)regexp_replace(*pattern:Any*, *replacement:Any*, *flags:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.regexp_replace()](#sqlalchemy.sql.expression.ColumnOperators.regexp_replace) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘regexp replace’ operator.

E.g.:

```
stmt = select(
    table.c.some_column.regexp_replace("b(..)", "XY", flags="g")
)
```

[ColumnOperators.regexp_replace()](#sqlalchemy.sql.expression.ColumnOperators.regexp_replace) attempts to resolve to
a REGEXP_REPLACE-like function provided by the backend, that
usually emit the function `REGEXP_REPLACE()`.  However,
the specific regular expression syntax and flags available are
**not backend agnostic**.

Regular expression replacement support is currently implemented for
Oracle Database, PostgreSQL, MySQL 8 or greater and MariaDB.  Support
among third-party dialects may vary.

  Parameters:

- **pattern** – The regular expression pattern string or column
  clause.
- **pattern** – The replacement string or column clause.
- **flags** – Any regular expression string flags to apply, passed as
  plain Python string only.  These flags are backend specific.
  Some backends, like PostgreSQL and MariaDB, may alternatively
  specify the flags as part of the pattern.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18  Note that due to an implementation
error, the “flags” parameter previously accepted SQL expression
objects such as column expressions in addition to plain Python
strings.   This implementation did not work correctly with caching
and was removed; strings only should be passed for the “flags”
parameter, as these flags are rendered as literal inline values
within SQL expressions.

See also

[ColumnOperators.regexp_match()](#sqlalchemy.sql.expression.ColumnOperators.regexp_match)

     method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)[Any]

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.sql.expression.ColumnElement.operate).

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)self_group(*against:OperatorType|None=None*) → [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)[Any]

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.ColumnElement.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.ColumnElement.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)shares_lineage(*othercolumn:ColumnElement[Any]*) → bool

Return True if the given [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
has a common ancestor to this [ColumnElement](#sqlalchemy.sql.expression.ColumnElement).

    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)startswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith) *method of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `startswith` operator.

Produces a LIKE expression that tests against a match for the start
of a string value:

```
column LIKE <other> || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.startswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.startswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.startswith.escape](#sqlalchemy.sql.expression.ColumnOperators.startswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.startswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.startswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE :param || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.startswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE :param || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.startswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape):
  ```
  somecolumn.startswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith)

[ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains)

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)stringify_dialect = 'default'    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)supports_execution = False    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)timetuple = None

*inherited from the* [ColumnOperators.timetuple](#sqlalchemy.sql.expression.ColumnOperators.timetuple) *attribute of* [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Hack, allows datetime objects to be compared on the LHS.

    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)type: [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[_T]    method [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)unique_params(*_ClauseElement__optionaldict:Dict[str,Any]|None=None*, ***kwargs:Any*) → Self

*inherited from the* [ClauseElement.unique_params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.unique_params) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Return a copy with [bindparam()](#sqlalchemy.sql.expression.bindparam) elements
replaced.

Same functionality as [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params),
except adds unique=True
to affected bind parameters so that multiple statements can be
used.

    attribute [sqlalchemy.sql.expression.ColumnElement.](#sqlalchemy.sql.expression.ColumnElement)uses_inspection = True     sqlalchemy.sql.expression.ColumnExpressionArgument

General purpose “column expression” argument.

Added in version 2.0.13.

This type is used for “column” kinds of expressions that typically represent
a single SQL column expression, including [ColumnElement](#sqlalchemy.sql.expression.ColumnElement), as
well as ORM-mapped attributes that will have a `__clause_element__()`
method.

    class sqlalchemy.sql.expression.ColumnOperators

*inherits from* [sqlalchemy.sql.expression.Operators](#sqlalchemy.sql.expression.Operators)

Defines boolean, comparison, and other operators for
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement) expressions.

By default, all methods call down to
[operate()](#sqlalchemy.sql.expression.ColumnOperators.operate) or [reverse_operate()](#sqlalchemy.sql.expression.ColumnOperators.reverse_operate),
passing in the appropriate operator function from the
Python builtin `operator` module or
a SQLAlchemy-specific operator function from
`sqlalchemy.expression.operators`.   For example
the `__eq__` function:

```
def __eq__(self, other):
    return self.operate(operators.eq, other)
```

Where `operators.eq` is essentially:

```
def eq(a, b):
    return a == b
```

The core column expression unit [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
overrides [Operators.operate()](#sqlalchemy.sql.expression.Operators.operate) and others
to return further [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) constructs,
so that the `==` operation above is replaced by a clause
construct.

See also

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory)

[ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

[PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator)

| Member Name | Description |
| --- | --- |
| __add__() | Implement the+operator. |
| __and__() | Implement the&operator. |
| __eq__() | Implement the==operator. |
| __floordiv__() | Implement the//operator. |
| __ge__() | Implement the>=operator. |
| __getitem__() | Implement the [] operator. |
| __gt__() | Implement the>operator. |
| __hash__() | Return hash(self). |
| __invert__() | Implement the~operator. |
| __le__() | Implement the<=operator. |
| __lshift__() | implement the << operator. |
| __lt__() | Implement the<operator. |
| __mod__() | Implement the%operator. |
| __mul__() | Implement the*operator. |
| __ne__() | Implement the!=operator. |
| __neg__() | Implement the-operator. |
| __or__() | Implement the|operator. |
| __radd__() | Implement the+operator in reverse. |
| __rfloordiv__() | Implement the//operator in reverse. |
| __rmod__() | Implement the%operator in reverse. |
| __rmul__() | Implement the*operator in reverse. |
| __rshift__() | implement the >> operator. |
| __rsub__() | Implement the-operator in reverse. |
| __rtruediv__() | Implement the/operator in reverse. |
| __sa_operate__() | Operate on an argument. |
| __sub__() | Implement the-operator. |
| __truediv__() | Implement the/operator. |
| all_() | Produce anall_()clause against the
parent object. |
| any_() | Produce anany_()clause against the
parent object. |
| asc() | Produce aasc()clause against the
parent object. |
| between() | Produce abetween()clause against
the parent object, given the lower and upper range. |
| bitwise_and() | Produce a bitwise AND operation, typically via the&operator. |
| bitwise_lshift() | Produce a bitwise LSHIFT operation, typically via the<<operator. |
| bitwise_not() | Produce a bitwise NOT operation, typically via the~operator. |
| bitwise_or() | Produce a bitwise OR operation, typically via the|operator. |
| bitwise_rshift() | Produce a bitwise RSHIFT operation, typically via the>>operator. |
| bitwise_xor() | Produce a bitwise XOR operation, typically via the^operator, or#for PostgreSQL. |
| bool_op() | Return a custom boolean operator. |
| collate() | Produce acollate()clause against
the parent object, given the collation string. |
| concat() | Implement the ‘concat’ operator. |
| contains() | Implement the ‘contains’ operator. |
| desc() | Produce adesc()clause against the
parent object. |
| distinct() | Produce adistinct()clause against the
parent object. |
| endswith() | Implement the ‘endswith’ operator. |
| icontains() | Implement theicontainsoperator, e.g. case insensitive
version ofColumnOperators.contains(). |
| iendswith() | Implement theiendswithoperator, e.g. case insensitive
version ofColumnOperators.endswith(). |
| ilike() | Implement theilikeoperator, e.g. case insensitive LIKE. |
| in_() | Implement theinoperator. |
| is_() | Implement theISoperator. |
| is_distinct_from() | Implement theISDISTINCTFROMoperator. |
| is_not() | Implement theISNOToperator. |
| is_not_distinct_from() | Implement theISNOTDISTINCTFROMoperator. |
| isnot() | Implement theISNOToperator. |
| isnot_distinct_from() | Implement theISNOTDISTINCTFROMoperator. |
| istartswith() | Implement theistartswithoperator, e.g. case insensitive
version ofColumnOperators.startswith(). |
| like() | Implement thelikeoperator. |
| match() | Implements a database-specific ‘match’ operator. |
| not_ilike() | implement theNOTILIKEoperator. |
| not_in() | implement theNOTINoperator. |
| not_like() | implement theNOTLIKEoperator. |
| notilike() | implement theNOTILIKEoperator. |
| notin_() | implement theNOTINoperator. |
| notlike() | implement theNOTLIKEoperator. |
| nulls_first() | Produce anulls_first()clause against the
parent object. |
| nulls_last() | Produce anulls_last()clause against the
parent object. |
| nullsfirst() | Produce anulls_first()clause against the
parent object. |
| nullslast() | Produce anulls_last()clause against the
parent object. |
| op() | Produce a generic operator function. |
| operate() | Operate on an argument. |
| regexp_match() | Implements a database-specific ‘regexp match’ operator. |
| regexp_replace() | Implements a database-specific ‘regexp replace’ operator. |
| reverse_operate() | Reverse operate on an argument. |
| startswith() | Implement thestartswithoperator. |
| timetuple | Hack, allows datetime objects to be compared on the LHS. |

   method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__add__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `+` operator.

In a column context, produces the clause `a + b`
if the parent object has non-string affinity.
If the parent object has a string affinity,
produces the concatenation operator, `a || b` -
see [ColumnOperators.concat()](#sqlalchemy.sql.expression.ColumnOperators.concat).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__and__(*other:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

*inherited from the* `sqlalchemy.sql.expression.Operators.__and__` *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Implement the `&` operator.

When used with SQL expressions, results in an
AND operation, equivalent to
[and_()](#sqlalchemy.sql.expression.and_), that is:

```
a & b
```

is equivalent to:

```
from sqlalchemy import and_

and_(a, b)
```

Care should be taken when using `&` regarding
operator precedence; the `&` operator has the highest precedence.
The operands should be enclosed in parenthesis if they contain
further sub expressions:

```
(a == 2) & (b == 4)
```

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__eq__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `==` operator.

In a column context, produces the clause `a = b`.
If the target is `None`, produces `a IS NULL`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__floordiv__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `//` operator.

In a column context, produces the clause `a / b`,
which is the same as “truediv”, but considers the result
type to be integer.

Added in version 2.0.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__ge__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `>=` operator.

In a column context, produces the clause `a >= b`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__getitem__(*index:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the [] operator.

This can be used by some database-specific types
such as PostgreSQL ARRAY and HSTORE.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__gt__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `>` operator.

In a column context, produces the clause `a > b`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__hash__()

Return hash(self).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__invert__() → [Operators](#sqlalchemy.sql.expression.Operators)

*inherited from the* `sqlalchemy.sql.expression.Operators.__invert__` *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Implement the `~` operator.

When used with SQL expressions, results in a
NOT operation, equivalent to
[not_()](#sqlalchemy.sql.expression.not_), that is:

```
~a
```

is equivalent to:

```
from sqlalchemy import not_

not_(a)
```

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__le__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<=` operator.

In a column context, produces the clause `a <= b`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__lshift__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the << operator.

Not used by SQLAlchemy core, this is provided
for custom operator systems which want to use
<< as an extension point.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__lt__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<` operator.

In a column context, produces the clause `a < b`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__mod__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `%` operator.

In a column context, produces the clause `a % b`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__mul__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `*` operator.

In a column context, produces the clause `a * b`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__ne__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `!=` operator.

In a column context, produces the clause `a != b`.
If the target is `None`, produces `a IS NOT NULL`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__neg__() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `-` operator.

In a column context, produces the clause `-a`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__or__(*other:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

*inherited from the* `sqlalchemy.sql.expression.Operators.__or__` *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Implement the `|` operator.

When used with SQL expressions, results in an
OR operation, equivalent to
[or_()](#sqlalchemy.sql.expression.or_), that is:

```
a | b
```

is equivalent to:

```
from sqlalchemy import or_

or_(a, b)
```

Care should be taken when using `|` regarding
operator precedence; the `|` operator has the highest precedence.
The operands should be enclosed in parenthesis if they contain
further sub expressions:

```
(a == 2) | (b == 4)
```

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__radd__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `+` operator in reverse.

See [ColumnOperators.__add__()](#sqlalchemy.sql.expression.ColumnOperators.__add__).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__rfloordiv__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `//` operator in reverse.

See [ColumnOperators.__floordiv__()](#sqlalchemy.sql.expression.ColumnOperators.__floordiv__).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__rmod__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `%` operator in reverse.

See [ColumnOperators.__mod__()](#sqlalchemy.sql.expression.ColumnOperators.__mod__).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__rmul__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `*` operator in reverse.

See [ColumnOperators.__mul__()](#sqlalchemy.sql.expression.ColumnOperators.__mul__).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__rshift__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the >> operator.

Not used by SQLAlchemy core, this is provided
for custom operator systems which want to use
>> as an extension point.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__rsub__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `-` operator in reverse.

See [ColumnOperators.__sub__()](#sqlalchemy.sql.expression.ColumnOperators.__sub__).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__rtruediv__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `/` operator in reverse.

See [ColumnOperators.__truediv__()](#sqlalchemy.sql.expression.ColumnOperators.__truediv__).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__sa_operate__(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

*inherited from the* `sqlalchemy.sql.expression.Operators.__sa_operate__` *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Operate on an argument.

This is the lowest level of operation, raises
`NotImplementedError` by default.

Overriding this on a subclass can allow common
behavior to be applied to all operations.
For example, overriding [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)
to apply `func.lower()` to the left and right
side:

```
class MyComparator(ColumnOperators):
    def operate(self, op, other, **kwargs):
        return op(func.lower(self), func.lower(other), **kwargs)
```

   Parameters:

- **op** – Operator callable.
- ***other** – the ‘other’ side of the operation. Will
  be a single scalar for most operations.
- ****kwargs** – modifiers.  These may be passed by special
  operators such as [ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains).

      method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__sub__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `-` operator.

In a column context, produces the clause `a - b`.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)__truediv__(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `/` operator.

In a column context, produces the clause `a / b`, and
considers the result type to be numeric.

Changed in version 2.0: The truediv operator against two integers
is now considered to return a numeric value.    Behavior on specific
backends may vary.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)all_() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce an [all_()](#sqlalchemy.sql.expression.all_) clause against the
parent object.

See the documentation for [all_()](#sqlalchemy.sql.expression.all_) for examples.

Note

be sure to not confuse the newer
[ColumnOperators.all_()](#sqlalchemy.sql.expression.ColumnOperators.all_) method with the **legacy**
version of this method, the [Comparator.all()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.all)
method that’s specific to [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), which uses a
different calling style.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)any_() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce an [any_()](#sqlalchemy.sql.expression.any_) clause against the
parent object.

See the documentation for [any_()](#sqlalchemy.sql.expression.any_) for examples.

Note

be sure to not confuse the newer
[ColumnOperators.any_()](#sqlalchemy.sql.expression.ColumnOperators.any_) method with the **legacy**
version of this method, the [Comparator.any()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.any)
method that’s specific to [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), which uses a
different calling style.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)asc() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [asc()](#sqlalchemy.sql.expression.asc) clause against the
parent object.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)between(*cleft:Any*, *cright:Any*, *symmetric:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [between()](#sqlalchemy.sql.expression.between) clause against
the parent object, given the lower and upper range.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)bitwise_and(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise AND operation, typically via the `&`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)bitwise_lshift(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise LSHIFT operation, typically via the `<<`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)bitwise_not() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise NOT operation, typically via the `~`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)bitwise_or(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise OR operation, typically via the `|`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)bitwise_rshift(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise RSHIFT operation, typically via the `>>`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)bitwise_xor(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise XOR operation, typically via the `^`
operator, or `#` for PostgreSQL.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)bool_op(*opstring:str*, *precedence:int=0*, *python_impl:Callable[[...],Any]|None=None*) → Callable[[Any], [Operators](#sqlalchemy.sql.expression.Operators)]

*inherited from the* [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op) *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Return a custom boolean operator.

This method is shorthand for calling
[Operators.op()](#sqlalchemy.sql.expression.Operators.op) and passing the
[Operators.op.is_comparison](#sqlalchemy.sql.expression.Operators.op.params.is_comparison)
flag with True.    A key advantage to using [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op)
is that when using column constructs, the “boolean” nature of the
returned expression will be present for [PEP 484](https://peps.python.org/pep-0484/) purposes.

See also

[Operators.op()](#sqlalchemy.sql.expression.Operators.op)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)collate(*collation:str*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [collate()](#sqlalchemy.sql.expression.collate) clause against
the parent object, given the collation string.

See also

[collate()](#sqlalchemy.sql.expression.collate)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)concat(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘concat’ operator.

In a column context, produces the clause `a || b`,
or uses the `concat()` operator on MySQL.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)contains(*other:Any*, ***kw:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘contains’ operator.

Produces a LIKE expression that tests against a match for the middle
of a string value:

```
column LIKE '%' || <other> || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.contains("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.contains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.contains.escape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.contains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.contains("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.contains("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.contains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape):
  ```
  somecolumn.contains("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith)

[ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith)

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)desc() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [desc()](#sqlalchemy.sql.expression.desc) clause against the
parent object.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)distinct() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [distinct()](#sqlalchemy.sql.expression.distinct) clause against the
parent object.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)endswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘endswith’ operator.

Produces a LIKE expression that tests against a match for the end
of a string value:

```
column LIKE '%' || <other>
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.endswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.endswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.endswith.escape](#sqlalchemy.sql.expression.ColumnOperators.endswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.endswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.endswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.endswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.endswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape):
  ```
  somecolumn.endswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith)

[ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains)

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)icontains(*other:Any*, ***kw:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `icontains` operator, e.g. case insensitive
version of [ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains).

Produces a LIKE expression that tests against an insensitive match
for the middle of a string value:

```
lower(column) LIKE '%' || lower(<other>) || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.icontains("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.icontains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.icontains.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.icontains.escape](#sqlalchemy.sql.expression.ColumnOperators.icontains.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.icontains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.icontains.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.icontains("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.icontains("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.contains.autoescape](#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape):
  ```
  somecolumn.icontains("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)iendswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `iendswith` operator, e.g. case insensitive
version of [ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith).

Produces a LIKE expression that tests against an insensitive match
for the end of a string value:

```
lower(column) LIKE '%' || lower(<other>)
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.iendswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.iendswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.iendswith.escape](#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.iendswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.iendswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.iendswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.iendswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape):
  ```
  somecolumn.endswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `ilike` operator, e.g. case insensitive LIKE.

In a column context, produces an expression either of the form:

```
lower(a) LIKE lower(other)
```

Or on backends that support the ILIKE operator:

```
a ILIKE other
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.ilike("%foobar%"))
```

   Parameters:

- **other** – expression to be compared
- **escape** –
  optional escape character, renders the `ESCAPE`
  keyword, e.g.:
  ```
  somecolumn.ilike("foo/%bar", escape="/")
  ```

See also

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)in_(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `in` operator.

In a column context, produces the clause `column IN <other>`.

The given parameter `other` may be:

- A list of literal values,
  e.g.:
  ```
  stmt.where(column.in_([1, 2, 3]))
  ```
  In this calling form, the list of items is converted to a set of
  bound parameters the same length as the list given:
  ```
  WHERE COL IN (?, ?, ?)
  ```
- A list of tuples may be provided if the comparison is against a
  [tuple_()](#sqlalchemy.sql.expression.tuple_) containing multiple expressions:
  ```
  from sqlalchemy import tuple_
  stmt.where(tuple_(col1, col2).in_([(1, 10), (2, 20), (3, 30)]))
  ```
- An empty list,
  e.g.:
  ```
  stmt.where(column.in_([]))
  ```
  In this calling form, the expression renders an “empty set”
  expression.  These expressions are tailored to individual backends
  and are generally trying to get an empty SELECT statement as a
  subquery.  Such as on SQLite, the expression is:
  ```
  WHERE col IN (SELECT 1 FROM (SELECT 1) WHERE 1!=1)
  ```
  Changed in version 1.4: empty IN expressions now use an
  execution-time generated SELECT subquery in all cases.
- A bound parameter, e.g. [bindparam()](#sqlalchemy.sql.expression.bindparam), may be used if it
  includes the [bindparam.expanding](#sqlalchemy.sql.expression.bindparam.params.expanding) flag:
  ```
  stmt.where(column.in_(bindparam("value", expanding=True)))
  ```
  In this calling form, the expression renders a special non-SQL
  placeholder expression that looks like:
  ```
  WHERE COL IN ([EXPANDING_value])
  ```
  This placeholder expression is intercepted at statement execution
  time to be converted into the variable number of bound parameter
  form illustrated earlier.   If the statement were executed as:
  ```
  connection.execute(stmt, {"value": [1, 2, 3]})
  ```
  The database would be passed a bound parameter for each value:
  ```
  WHERE COL IN (?, ?, ?)
  ```
  Added in version 1.2: added “expanding” bound parameters
  If an empty list is passed, a special “empty list” expression,
  which is specific to the database in use, is rendered.  On
  SQLite this would be:
  ```
  WHERE COL IN (SELECT 1 FROM (SELECT 1) WHERE 1!=1)
  ```
  Added in version 1.3: “expanding” bound parameters now support
  empty lists
- a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct, which is usually a
  correlated scalar select:
  ```
  stmt.where(
      column.in_(select(othertable.c.y).where(table.c.x == othertable.c.x))
  )
  ```
  In this calling form, [ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_) renders as given:
  ```
  WHERE COL IN (SELECT othertable.y
  FROM othertable WHERE othertable.x = table.x)
  ```

  Parameters:

**other** – a list of literals, a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
construct, or a [bindparam()](#sqlalchemy.sql.expression.bindparam) construct that includes the
[bindparam.expanding](#sqlalchemy.sql.expression.bindparam.params.expanding) flag set to True.

      method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)is_(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS` operator.

Normally, `IS` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS` may be desirable if comparing to boolean values
on certain platforms.

See also

[ColumnOperators.is_not()](#sqlalchemy.sql.expression.ColumnOperators.is_not)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)is_distinct_from(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS DISTINCT FROM` operator.

Renders “a IS DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS NOT b”.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)is_not(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT` operator.

Normally, `IS NOT` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS NOT` may be desirable if comparing to boolean values
on certain platforms.

Changed in version 1.4: The `is_not()` operator is renamed from
`isnot()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.is_()](#sqlalchemy.sql.expression.ColumnOperators.is_)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)is_not_distinct_from(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)isnot(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT` operator.

Normally, `IS NOT` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS NOT` may be desirable if comparing to boolean values
on certain platforms.

Changed in version 1.4: The `is_not()` operator is renamed from
`isnot()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.is_()](#sqlalchemy.sql.expression.ColumnOperators.is_)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)isnot_distinct_from(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)istartswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `istartswith` operator, e.g. case insensitive
version of [ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith).

Produces a LIKE expression that tests against an insensitive
match for the start of a string value:

```
lower(column) LIKE lower(<other>) || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.istartswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.istartswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.istartswith.escape](#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.escape) parameter will
establish a given character as an escape character which can be of
use when the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.istartswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.istartswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE lower(:param) || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.istartswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE lower(:param) || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.istartswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape):
  ```
  somecolumn.istartswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](#sqlalchemy.sql.expression.ColumnOperators.startswith)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `like` operator.

In a column context, produces the expression:

```
a LIKE other
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.like("%foobar%"))
```

   Parameters:

- **other** – expression to be compared
- **escape** –
  optional escape character, renders the `ESCAPE`
  keyword, e.g.:
  ```
  somecolumn.like("foo/%bar", escape="/")
  ```

See also

[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)match(*other:Any*, ***kwargs:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘match’ operator.

[ColumnOperators.match()](#sqlalchemy.sql.expression.ColumnOperators.match) attempts to resolve to
a MATCH-like function or operator provided by the backend.
Examples include:

- PostgreSQL - renders `x @@ plainto_tsquery(y)`
  > Changed in version 2.0: `plainto_tsquery()` is used instead
  > of `to_tsquery()` for PostgreSQL now; for compatibility with
  > other forms, see [Full Text Search](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-match).
- MySQL - renders `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
  See also
  [match](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.match) - MySQL specific construct with
  additional features.
- Oracle Database - renders `CONTAINS(x, y)`
- other backends may provide special implementations.
- Backends without any special implementation will emit
  the operator as “MATCH”.  This is compatible with SQLite, for
  example.

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)not_ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)not_in(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT IN` operator.

This is equivalent to using negation with
[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_), i.e. `~x.in_(y)`.

In the case that `other` is an empty sequence, the compiler
produces an “empty not in” expression.   This defaults to the
expression “1 = 1” to produce true in all cases.  The
[create_engine.empty_in_strategy](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.empty_in_strategy) may be used to
alter this behavior.

Changed in version 1.4: The `not_in()` operator is renamed from
`notin_()` in previous releases.  The previous name remains
available for backwards compatibility.

Changed in version 1.2: The [ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_) and
[ColumnOperators.not_in()](#sqlalchemy.sql.expression.ColumnOperators.not_in) operators
now produce a “static” expression for an empty IN sequence
by default.

See also

[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)not_like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)notilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)notin_(*other:Any*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT IN` operator.

This is equivalent to using negation with
[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_), i.e. `~x.in_(y)`.

In the case that `other` is an empty sequence, the compiler
produces an “empty not in” expression.   This defaults to the
expression “1 = 1” to produce true in all cases.  The
[create_engine.empty_in_strategy](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.empty_in_strategy) may be used to
alter this behavior.

Changed in version 1.4: The `not_in()` operator is renamed from
`notin_()` in previous releases.  The previous name remains
available for backwards compatibility.

Changed in version 1.2: The [ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_) and
[ColumnOperators.not_in()](#sqlalchemy.sql.expression.ColumnOperators.not_in) operators
now produce a “static” expression for an empty IN sequence
by default.

See also

[ColumnOperators.in_()](#sqlalchemy.sql.expression.ColumnOperators.in_)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)notlike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)nulls_first() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)nulls_last() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)nullsfirst() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)nullslast() → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)op(*opstring:str*, *precedence:int=0*, *is_comparison:bool=False*, *return_type:Type[TypeEngine[Any]]|TypeEngine[Any]|None=None*, *python_impl:Callable[...,Any]|None=None*) → Callable[[Any], [Operators](#sqlalchemy.sql.expression.Operators)]

*inherited from the* [Operators.op()](#sqlalchemy.sql.expression.Operators.op) *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Produce a generic operator function.

e.g.:

```
somecolumn.op("*")(5)
```

produces:

```
somecolumn * 5
```

This function can also be used to make bitwise operators explicit. For
example:

```
somecolumn.op("&")(0xFF)
```

is a bitwise AND of the value in `somecolumn`.

  Parameters:

- **opstring** – a string which will be output as the infix operator
  between this element and the expression passed to the
  generated function.
- **precedence** –
  precedence which the database is expected to apply
  to the operator in SQL expressions. This integer value acts as a hint
  for the SQL compiler to know when explicit parenthesis should be
  rendered around a particular operation. A lower number will cause the
  expression to be parenthesized when applied against another operator
  with higher precedence. The default value of `0` is lower than all
  operators except for the comma (`,`) and `AS` operators. A value
  of 100 will be higher or equal to all operators, and -100 will be
  lower than or equal to all operators.
  See also
  [I’m using op() to generate a custom operator and my parenthesis are not coming out correctly](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-op-parenthesis) - detailed description
  of how the SQLAlchemy SQL compiler renders parenthesis
- **is_comparison** –
  legacy; if True, the operator will be considered
  as a “comparison” operator, that is which evaluates to a boolean
  true/false value, like `==`, `>`, etc.  This flag is provided
  so that ORM relationships can establish that the operator is a
  comparison operator when used in a custom join condition.
  Using the `is_comparison` parameter is superseded by using the
  [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op) method instead;  this more succinct
  operator sets this parameter automatically, but also provides
  correct [PEP 484](https://peps.python.org/pep-0484/) typing support as the returned object will
  express a “boolean” datatype, i.e. `BinaryExpression[bool]`.
- **return_type** – a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or object that will
  force the return type of an expression produced by this operator
  to be of that type.   By default, operators that specify
  [Operators.op.is_comparison](#sqlalchemy.sql.expression.Operators.op.params.is_comparison) will resolve to
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean), and those that do not will be of the same
  type as the left-hand operand.
- **python_impl** –
  an optional Python function that can evaluate
  two Python values in the same way as this operator works when
  run on the database server.  Useful for in-Python SQL expression
  evaluation functions, such as for ORM hybrid attributes, and the
  ORM “evaluator” used to match objects in a session after a multi-row
  update or delete.
  e.g.:
  ```
  >>> expr = column("x").op("+", python_impl=lambda a, b: a + b)("y")
  ```
  The operator for the above expression will also work for non-SQL
  left and right objects:
  ```
  >>> expr.operator(5, 10)
  15
  ```
  Added in version 2.0.

See also

[Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op)

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[Using custom operators in join conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-operator)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

*inherited from the* [Operators.operate()](#sqlalchemy.sql.expression.Operators.operate) *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Operate on an argument.

This is the lowest level of operation, raises
`NotImplementedError` by default.

Overriding this on a subclass can allow common
behavior to be applied to all operations.
For example, overriding [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)
to apply `func.lower()` to the left and right
side:

```
class MyComparator(ColumnOperators):
    def operate(self, op, other, **kwargs):
        return op(func.lower(self), func.lower(other), **kwargs)
```

   Parameters:

- **op** – Operator callable.
- ***other** – the ‘other’ side of the operation. Will
  be a single scalar for most operations.
- ****kwargs** – modifiers.  These may be passed by special
  operators such as [ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains).

      method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)regexp_match(*pattern:Any*, *flags:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘regexp match’ operator.

E.g.:

```
stmt = select(table.c.some_column).where(
    table.c.some_column.regexp_match("^(b|c)")
)
```

[ColumnOperators.regexp_match()](#sqlalchemy.sql.expression.ColumnOperators.regexp_match) attempts to resolve to
a REGEXP-like function or operator provided by the backend, however
the specific regular expression syntax and flags available are
**not backend agnostic**.

Examples include:

- PostgreSQL - renders `x ~ y` or `x !~ y` when negated.
- Oracle Database - renders `REGEXP_LIKE(x, y)`
- SQLite - uses SQLite’s `REGEXP` placeholder operator and calls into
  the Python `re.match()` builtin.
- other backends may provide special implementations.
- Backends without any special implementation will emit
  the operator as “REGEXP” or “NOT REGEXP”.  This is compatible with
  SQLite and MySQL, for example.

Regular expression support is currently implemented for Oracle
Database, PostgreSQL, MySQL and MariaDB.  Partial support is available
for SQLite.  Support among third-party dialects may vary.

  Parameters:

- **pattern** – The regular expression pattern string or column
  clause.
- **flags** – Any regular expression string flags to apply, passed as
  plain Python string only.  These flags are backend specific.
  Some backends, like PostgreSQL and MariaDB, may alternatively
  specify the flags as part of the pattern.
  When using the ignore case flag ‘i’ in PostgreSQL, the ignore case
  regexp match operator `~*` or `!~*` will be used.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18  Note that due to an implementation
error, the “flags” parameter previously accepted SQL expression
objects such as column expressions in addition to plain Python
strings.   This implementation did not work correctly with caching
and was removed; strings only should be passed for the “flags”
parameter, as these flags are rendered as literal inline values
within SQL expressions.

See also

[ColumnOperators.regexp_replace()](#sqlalchemy.sql.expression.ColumnOperators.regexp_replace)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)regexp_replace(*pattern:Any*, *replacement:Any*, *flags:str|None=None*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘regexp replace’ operator.

E.g.:

```
stmt = select(
    table.c.some_column.regexp_replace("b(..)", "XY", flags="g")
)
```

[ColumnOperators.regexp_replace()](#sqlalchemy.sql.expression.ColumnOperators.regexp_replace) attempts to resolve to
a REGEXP_REPLACE-like function provided by the backend, that
usually emit the function `REGEXP_REPLACE()`.  However,
the specific regular expression syntax and flags available are
**not backend agnostic**.

Regular expression replacement support is currently implemented for
Oracle Database, PostgreSQL, MySQL 8 or greater and MariaDB.  Support
among third-party dialects may vary.

  Parameters:

- **pattern** – The regular expression pattern string or column
  clause.
- **pattern** – The replacement string or column clause.
- **flags** – Any regular expression string flags to apply, passed as
  plain Python string only.  These flags are backend specific.
  Some backends, like PostgreSQL and MariaDB, may alternatively
  specify the flags as part of the pattern.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18  Note that due to an implementation
error, the “flags” parameter previously accepted SQL expression
objects such as column expressions in addition to plain Python
strings.   This implementation did not work correctly with caching
and was removed; strings only should be passed for the “flags”
parameter, as these flags are rendered as literal inline values
within SQL expressions.

See also

[ColumnOperators.regexp_match()](#sqlalchemy.sql.expression.ColumnOperators.regexp_match)

     method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

*inherited from the* [Operators.reverse_operate()](#sqlalchemy.sql.expression.Operators.reverse_operate) *method of* [Operators](#sqlalchemy.sql.expression.Operators)

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.sql.expression.ColumnOperators.operate).

    method [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)startswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)

Implement the `startswith` operator.

Produces a LIKE expression that tests against a match for the start
of a string value:

```
column LIKE <other> || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.startswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.startswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.startswith.escape](#sqlalchemy.sql.expression.ColumnOperators.startswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.startswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.startswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE :param || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.startswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE :param || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.startswith.autoescape](#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape):
  ```
  somecolumn.startswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.endswith()](#sqlalchemy.sql.expression.ColumnOperators.endswith)

[ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains)

[ColumnOperators.like()](#sqlalchemy.sql.expression.ColumnOperators.like)

     attribute [sqlalchemy.sql.expression.ColumnOperators.](#sqlalchemy.sql.expression.ColumnOperators)timetuple: Literal[None] = None

Hack, allows datetime objects to be compared on the LHS.

     class sqlalchemy.sql.expression.Extract

*inherits from* [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent a SQL EXTRACT clause, `extract(field FROM expr)`.

    class sqlalchemy.sql.expression.False_

*inherits from* `sqlalchemy.sql.expression.SingletonConstant`, `sqlalchemy.sql.roles.ConstExprRole`, [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent the `false` keyword, or equivalent, in a SQL statement.

[False_](#sqlalchemy.sql.expression.False_) is accessed as a constant via the
[false()](#sqlalchemy.sql.expression.false) function.

    class sqlalchemy.sql.expression.FunctionFilter

*inherits from* `sqlalchemy.sql.expression.Generative`, [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent a function FILTER clause.

This is a special operator against aggregate and window functions,
which controls which rows are passed to it.
It’s supported only by certain database backends.

Invocation of [FunctionFilter](#sqlalchemy.sql.expression.FunctionFilter) is via
[FunctionElement.filter()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.filter):

```
func.count(1).filter(True)
```

See also

[FunctionElement.filter()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.filter)

| Member Name | Description |
| --- | --- |
| filter() | Produce an additional FILTER against the function. |
| over() | Produce an OVER clause against this filtered function. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| within_group() | Produce a WITHIN GROUP (ORDER BY expr) clause against
this function. |

   method [sqlalchemy.sql.expression.FunctionFilter.](#sqlalchemy.sql.expression.FunctionFilter)filter(**criterion:_ColumnExpressionArgument[bool]*) → Self

Produce an additional FILTER against the function.

This method adds additional criteria to the initial criteria
set up by [FunctionElement.filter()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.filter).

Multiple criteria are joined together at SQL render time
via `AND`.

    method [sqlalchemy.sql.expression.FunctionFilter.](#sqlalchemy.sql.expression.FunctionFilter)over(*partition_by:Iterable[_ColumnExpressionArgument[Any]]|_ColumnExpressionArgument[Any]|None=None*, *order_by:Iterable[_ColumnExpressionArgument[Any]]|_ColumnExpressionArgument[Any]|None=None*, *range_:typing_Tuple[int|None,int|None]|None=None*, *rows:typing_Tuple[int|None,int|None]|None=None*, *groups:typing_Tuple[int|None,int|None]|None=None*) → [Over](#sqlalchemy.sql.expression.Over)[_T]

Produce an OVER clause against this filtered function.

Used against aggregate or so-called “window” functions,
for database backends that support window functions.

The expression:

```
func.rank().filter(MyClass.y > 5).over(order_by="x")
```

is shorthand for:

```
from sqlalchemy import over, funcfilter

over(funcfilter(func.rank(), MyClass.y > 5), order_by="x")
```

See [over()](#sqlalchemy.sql.expression.over) for a full description.

    method [sqlalchemy.sql.expression.FunctionFilter.](#sqlalchemy.sql.expression.FunctionFilter)self_group(*against:OperatorType|None=None*) → Self | Grouping[_T]

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.FunctionFilter.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.FunctionFilter.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.sql.expression.FunctionFilter.](#sqlalchemy.sql.expression.FunctionFilter)within_group(**order_by:_ColumnExpressionArgument[Any]*) → [WithinGroup](#sqlalchemy.sql.expression.WithinGroup)[_T]

Produce a WITHIN GROUP (ORDER BY expr) clause against
this function.

     class sqlalchemy.sql.expression.Label

*inherits from* `sqlalchemy.sql.roles.LabeledColumnExprRole`, `sqlalchemy.sql.expression.NamedColumn`

Represents a column label (AS).

Represent a label, as typically applied to any column-level
element using the `AS` sql keyword.

| Member Name | Description |
| --- | --- |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |

   property foreign_keys

Build an immutable unordered collection of unique elements.

    property primary_key

Returns True when the argument is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

    method [sqlalchemy.sql.expression.Label.](#sqlalchemy.sql.expression.Label)self_group(*against:OperatorType|None=None*) → [Label](#sqlalchemy.sql.expression.Label)[_T]

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.Label.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.Label.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

     class sqlalchemy.sql.expression.Null

*inherits from* `sqlalchemy.sql.expression.SingletonConstant`, `sqlalchemy.sql.roles.ConstExprRole`, [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent the NULL keyword in a SQL statement.

[Null](#sqlalchemy.sql.expression.Null) is accessed as a constant via the
[null()](#sqlalchemy.sql.expression.null) function.

    class sqlalchemy.sql.expression.Operators

Base of comparison and logical operators.

Implements base methods
`Operators.operate()` and
`Operators.reverse_operate()`, as well as
`Operators.__and__()`,
`Operators.__or__()`,
`Operators.__invert__()`.

Usually is used via its most common subclass
[ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators).

| Member Name | Description |
| --- | --- |
| __and__() | Implement the&operator. |
| __invert__() | Implement the~operator. |
| __or__() | Implement the|operator. |
| __sa_operate__() | Operate on an argument. |
| bool_op() | Return a custom boolean operator. |
| op() | Produce a generic operator function. |
| operate() | Operate on an argument. |
| reverse_operate() | Reverse operate on an argument. |

   method [sqlalchemy.sql.expression.Operators.](#sqlalchemy.sql.expression.Operators)__and__(*other:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

Implement the `&` operator.

When used with SQL expressions, results in an
AND operation, equivalent to
[and_()](#sqlalchemy.sql.expression.and_), that is:

```
a & b
```

is equivalent to:

```
from sqlalchemy import and_

and_(a, b)
```

Care should be taken when using `&` regarding
operator precedence; the `&` operator has the highest precedence.
The operands should be enclosed in parenthesis if they contain
further sub expressions:

```
(a == 2) & (b == 4)
```

     method [sqlalchemy.sql.expression.Operators.](#sqlalchemy.sql.expression.Operators)__invert__() → [Operators](#sqlalchemy.sql.expression.Operators)

Implement the `~` operator.

When used with SQL expressions, results in a
NOT operation, equivalent to
[not_()](#sqlalchemy.sql.expression.not_), that is:

```
~a
```

is equivalent to:

```
from sqlalchemy import not_

not_(a)
```

     method [sqlalchemy.sql.expression.Operators.](#sqlalchemy.sql.expression.Operators)__or__(*other:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

Implement the `|` operator.

When used with SQL expressions, results in an
OR operation, equivalent to
[or_()](#sqlalchemy.sql.expression.or_), that is:

```
a | b
```

is equivalent to:

```
from sqlalchemy import or_

or_(a, b)
```

Care should be taken when using `|` regarding
operator precedence; the `|` operator has the highest precedence.
The operands should be enclosed in parenthesis if they contain
further sub expressions:

```
(a == 2) | (b == 4)
```

     method [sqlalchemy.sql.expression.Operators.](#sqlalchemy.sql.expression.Operators)__sa_operate__(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

Operate on an argument.

This is the lowest level of operation, raises
`NotImplementedError` by default.

Overriding this on a subclass can allow common
behavior to be applied to all operations.
For example, overriding [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)
to apply `func.lower()` to the left and right
side:

```
class MyComparator(ColumnOperators):
    def operate(self, op, other, **kwargs):
        return op(func.lower(self), func.lower(other), **kwargs)
```

   Parameters:

- **op** – Operator callable.
- ***other** – the ‘other’ side of the operation. Will
  be a single scalar for most operations.
- ****kwargs** – modifiers.  These may be passed by special
  operators such as [ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains).

      method [sqlalchemy.sql.expression.Operators.](#sqlalchemy.sql.expression.Operators)bool_op(*opstring:str*, *precedence:int=0*, *python_impl:Callable[[...],Any]|None=None*) → Callable[[Any], [Operators](#sqlalchemy.sql.expression.Operators)]

Return a custom boolean operator.

This method is shorthand for calling
[Operators.op()](#sqlalchemy.sql.expression.Operators.op) and passing the
[Operators.op.is_comparison](#sqlalchemy.sql.expression.Operators.op.params.is_comparison)
flag with True.    A key advantage to using [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op)
is that when using column constructs, the “boolean” nature of the
returned expression will be present for [PEP 484](https://peps.python.org/pep-0484/) purposes.

See also

[Operators.op()](#sqlalchemy.sql.expression.Operators.op)

     method [sqlalchemy.sql.expression.Operators.](#sqlalchemy.sql.expression.Operators)op(*opstring:str*, *precedence:int=0*, *is_comparison:bool=False*, *return_type:Type[TypeEngine[Any]]|TypeEngine[Any]|None=None*, *python_impl:Callable[...,Any]|None=None*) → Callable[[Any], [Operators](#sqlalchemy.sql.expression.Operators)]

Produce a generic operator function.

e.g.:

```
somecolumn.op("*")(5)
```

produces:

```
somecolumn * 5
```

This function can also be used to make bitwise operators explicit. For
example:

```
somecolumn.op("&")(0xFF)
```

is a bitwise AND of the value in `somecolumn`.

  Parameters:

- **opstring** – a string which will be output as the infix operator
  between this element and the expression passed to the
  generated function.
- **precedence** –
  precedence which the database is expected to apply
  to the operator in SQL expressions. This integer value acts as a hint
  for the SQL compiler to know when explicit parenthesis should be
  rendered around a particular operation. A lower number will cause the
  expression to be parenthesized when applied against another operator
  with higher precedence. The default value of `0` is lower than all
  operators except for the comma (`,`) and `AS` operators. A value
  of 100 will be higher or equal to all operators, and -100 will be
  lower than or equal to all operators.
  See also
  [I’m using op() to generate a custom operator and my parenthesis are not coming out correctly](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-op-parenthesis) - detailed description
  of how the SQLAlchemy SQL compiler renders parenthesis
- **is_comparison** –
  legacy; if True, the operator will be considered
  as a “comparison” operator, that is which evaluates to a boolean
  true/false value, like `==`, `>`, etc.  This flag is provided
  so that ORM relationships can establish that the operator is a
  comparison operator when used in a custom join condition.
  Using the `is_comparison` parameter is superseded by using the
  [Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op) method instead;  this more succinct
  operator sets this parameter automatically, but also provides
  correct [PEP 484](https://peps.python.org/pep-0484/) typing support as the returned object will
  express a “boolean” datatype, i.e. `BinaryExpression[bool]`.
- **return_type** – a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or object that will
  force the return type of an expression produced by this operator
  to be of that type.   By default, operators that specify
  [Operators.op.is_comparison](#sqlalchemy.sql.expression.Operators.op.params.is_comparison) will resolve to
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean), and those that do not will be of the same
  type as the left-hand operand.
- **python_impl** –
  an optional Python function that can evaluate
  two Python values in the same way as this operator works when
  run on the database server.  Useful for in-Python SQL expression
  evaluation functions, such as for ORM hybrid attributes, and the
  ORM “evaluator” used to match objects in a session after a multi-row
  update or delete.
  e.g.:
  ```
  >>> expr = column("x").op("+", python_impl=lambda a, b: a + b)("y")
  ```
  The operator for the above expression will also work for non-SQL
  left and right objects:
  ```
  >>> expr.operator(5, 10)
  15
  ```
  Added in version 2.0.

See also

[Operators.bool_op()](#sqlalchemy.sql.expression.Operators.bool_op)

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[Using custom operators in join conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-operator)

     method [sqlalchemy.sql.expression.Operators.](#sqlalchemy.sql.expression.Operators)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

Operate on an argument.

This is the lowest level of operation, raises
`NotImplementedError` by default.

Overriding this on a subclass can allow common
behavior to be applied to all operations.
For example, overriding [ColumnOperators](#sqlalchemy.sql.expression.ColumnOperators)
to apply `func.lower()` to the left and right
side:

```
class MyComparator(ColumnOperators):
    def operate(self, op, other, **kwargs):
        return op(func.lower(self), func.lower(other), **kwargs)
```

   Parameters:

- **op** – Operator callable.
- ***other** – the ‘other’ side of the operation. Will
  be a single scalar for most operations.
- ****kwargs** – modifiers.  These may be passed by special
  operators such as [ColumnOperators.contains()](#sqlalchemy.sql.expression.ColumnOperators.contains).

      method [sqlalchemy.sql.expression.Operators.](#sqlalchemy.sql.expression.Operators)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [Operators](#sqlalchemy.sql.expression.Operators)

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.sql.expression.Operators.operate).

     class sqlalchemy.sql.expression.Over

*inherits from* [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent an OVER clause.

This is a special operator against a so-called
“window” function, as well as any aggregate function,
which produces results relative to the result set
itself.  Most modern SQL backends now support window functions.

| Member Name | Description |
| --- | --- |
| element | The underlying expression object to which thisOverobject refers. |

   attribute [sqlalchemy.sql.expression.Over.](#sqlalchemy.sql.expression.Over)element: [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)[_T]

The underlying expression object to which this [Over](#sqlalchemy.sql.expression.Over)
object refers.

     class sqlalchemy.sql.expression.SQLColumnExpression

*inherits from* `sqlalchemy.sql.expression.SQLCoreOperations`, `sqlalchemy.sql.roles.ExpressionElementRole`, `sqlalchemy.util.langhelpers.TypingOnly`

A type that may be used to indicate any SQL column element or object
that acts in place of one.

[SQLColumnExpression](#sqlalchemy.sql.expression.SQLColumnExpression) is a base of
[ColumnElement](#sqlalchemy.sql.expression.ColumnElement), as well as within the bases of ORM elements
such as [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute), and may be used in [PEP 484](https://peps.python.org/pep-0484/)
typing to indicate arguments or return values that should behave
as column expressions.

Added in version 2.0.0b4.

     class sqlalchemy.sql.expression.TextClause

*inherits from* `sqlalchemy.sql.roles.DDLConstraintColumnRole`, `sqlalchemy.sql.roles.DDLExpressionRole`, `sqlalchemy.sql.roles.StatementOptionRole`, `sqlalchemy.sql.roles.WhereHavingRole`, `sqlalchemy.sql.roles.OrderByRole`, `sqlalchemy.sql.roles.FromClauseRole`, `sqlalchemy.sql.roles.SelectStatementRole`, `sqlalchemy.sql.roles.InElementRole`, `sqlalchemy.sql.expression.Generative`, [sqlalchemy.sql.expression.Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable), `sqlalchemy.sql.expression.DQLDMLClauseElement`, `sqlalchemy.sql.roles.BinaryElementRole`, `sqlalchemy.inspection.Inspectable`

Represent a literal SQL text fragment.

E.g.:

```
from sqlalchemy import text

t = text("SELECT * FROM users")
result = connection.execute(t)
```

The [TextClause](#sqlalchemy.sql.expression.TextClause) construct is produced using the
[text()](#sqlalchemy.sql.expression.text)
function; see that function for full documentation.

See also

[text()](#sqlalchemy.sql.expression.text)

| Member Name | Description |
| --- | --- |
| bindparams() | Establish the values and/or types of bound parameters within
thisTextClauseconstruct. |
| columns() | Turn thisTextClauseobject into aTextualSelectobject that serves the same role as a SELECT
statement. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |

   method [sqlalchemy.sql.expression.TextClause.](#sqlalchemy.sql.expression.TextClause)bindparams(**binds:BindParameter[Any]*, ***names_to_values:Any*) → Self

Establish the values and/or types of bound parameters within
this [TextClause](#sqlalchemy.sql.expression.TextClause) construct.

Given a text construct such as:

```
from sqlalchemy import text

stmt = text(
    "SELECT id, name FROM user WHERE name=:name AND timestamp=:timestamp"
)
```

the [TextClause.bindparams()](#sqlalchemy.sql.expression.TextClause.bindparams)
method can be used to establish
the initial value of `:name` and `:timestamp`,
using simple keyword arguments:

```
stmt = stmt.bindparams(
    name="jack", timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5)
)
```

Where above, new [BindParameter](#sqlalchemy.sql.expression.BindParameter) objects
will be generated with the names `name` and `timestamp`, and
values of `jack` and `datetime.datetime(2012, 10, 8, 15, 12, 5)`,
respectively.  The types will be
inferred from the values given, in this case [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) and
[DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime).

When specific typing behavior is needed, the positional `*binds`
argument can be used in which to specify [bindparam()](#sqlalchemy.sql.expression.bindparam) constructs
directly.  These constructs must include at least the `key`
argument, then an optional value and type:

```
from sqlalchemy import bindparam

stmt = stmt.bindparams(
    bindparam("name", value="jack", type_=String),
    bindparam("timestamp", type_=DateTime),
)
```

Above, we specified the type of [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime) for the
`timestamp` bind, and the type of [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) for the `name`
bind.  In the case of `name` we also set the default value of
`"jack"`.

Additional bound parameters can be supplied at statement execution
time, e.g.:

```
result = connection.execute(
    stmt, timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5)
)
```

The [TextClause.bindparams()](#sqlalchemy.sql.expression.TextClause.bindparams)
method can be called repeatedly,
where it will reuse existing [BindParameter](#sqlalchemy.sql.expression.BindParameter) objects to add
new information.  For example, we can call
[TextClause.bindparams()](#sqlalchemy.sql.expression.TextClause.bindparams)
first with typing information, and a
second time with value information, and it will be combined:

```
stmt = text(
    "SELECT id, name FROM user WHERE name=:name "
    "AND timestamp=:timestamp"
)
stmt = stmt.bindparams(
    bindparam("name", type_=String), bindparam("timestamp", type_=DateTime)
)
stmt = stmt.bindparams(
    name="jack", timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5)
)
```

The [TextClause.bindparams()](#sqlalchemy.sql.expression.TextClause.bindparams)
method also supports the concept of
**unique** bound parameters.  These are parameters that are
“uniquified” on name at statement compilation time, so that  multiple
[text()](#sqlalchemy.sql.expression.text)
constructs may be combined together without the names
conflicting.  To use this feature, specify the
[BindParameter.unique](#sqlalchemy.sql.expression.BindParameter.params.unique) flag on each [bindparam()](#sqlalchemy.sql.expression.bindparam)
object:

```
stmt1 = text("select id from table where name=:name").bindparams(
    bindparam("name", value="name1", unique=True)
)
stmt2 = text("select id from table where name=:name").bindparams(
    bindparam("name", value="name2", unique=True)
)

union = union_all(stmt1.columns(column("id")), stmt2.columns(column("id")))
```

The above statement will render as:

```
select id from table where name=:name_1
UNION ALL select id from table where name=:name_2
```

Added in version 1.3.11: Added support for the
[BindParameter.unique](#sqlalchemy.sql.expression.BindParameter.params.unique) flag to work with
[text()](#sqlalchemy.sql.expression.text)
constructs.

     method [sqlalchemy.sql.expression.TextClause.](#sqlalchemy.sql.expression.TextClause)columns(**cols:_OnlyColumnArgument[Any]*, ***types:_TypeEngineArgument[Any]*) → [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect)

Turn this [TextClause](#sqlalchemy.sql.expression.TextClause) object into a
[TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect)
object that serves the same role as a SELECT
statement.

The [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect) is part of the
[SelectBase](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase)
hierarchy and can be embedded into another statement by using the
[TextualSelect.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect.subquery) method to produce a
[Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery)
object, which can then be SELECTed from.

This function essentially bridges the gap between an entirely
textual SELECT statement and the SQL expression language concept
of a “selectable”:

```
from sqlalchemy.sql import column, text

stmt = text("SELECT id, name FROM some_table")
stmt = stmt.columns(column("id"), column("name")).subquery("st")

stmt = (
    select(mytable)
    .select_from(mytable.join(stmt, mytable.c.name == stmt.c.name))
    .where(stmt.c.id > 5)
)
```

Above, we pass a series of [column()](#sqlalchemy.sql.expression.column) elements to the
[TextClause.columns()](#sqlalchemy.sql.expression.TextClause.columns) method positionally.  These
[column()](#sqlalchemy.sql.expression.column)
elements now become first class elements upon the
[TextualSelect.selected_columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect.selected_columns) column collection,
which then
become part of the `Subquery.c` collection after
[TextualSelect.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect.subquery) is invoked.

The column expressions we pass to
[TextClause.columns()](#sqlalchemy.sql.expression.TextClause.columns) may
also be typed; when we do so, these [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) objects become
the effective return type of the column, so that SQLAlchemy’s
result-set-processing systems may be used on the return values.
This is often needed for types such as date or boolean types, as well
as for unicode processing on some dialect configurations:

```
stmt = text("SELECT id, name, timestamp FROM some_table")
stmt = stmt.columns(
    column("id", Integer),
    column("name", Unicode),
    column("timestamp", DateTime),
)

for id, name, timestamp in connection.execute(stmt):
    print(id, name, timestamp)
```

As a shortcut to the above syntax, keyword arguments referring to
types alone may be used, if only type conversion is needed:

```
stmt = text("SELECT id, name, timestamp FROM some_table")
stmt = stmt.columns(id=Integer, name=Unicode, timestamp=DateTime)

for id, name, timestamp in connection.execute(stmt):
    print(id, name, timestamp)
```

The positional form of [TextClause.columns()](#sqlalchemy.sql.expression.TextClause.columns)
also provides the
unique feature of **positional column targeting**, which is
particularly useful when using the ORM with complex textual queries. If
we specify the columns from our model to
[TextClause.columns()](#sqlalchemy.sql.expression.TextClause.columns),
the result set will match to those columns positionally, meaning the
name or origin of the column in the textual SQL doesn’t matter:

```
stmt = text(
    "SELECT users.id, addresses.id, users.id, "
    "users.name, addresses.email_address AS email "
    "FROM users JOIN addresses ON users.id=addresses.user_id "
    "WHERE users.id = 1"
).columns(
    User.id,
    Address.id,
    Address.user_id,
    User.name,
    Address.email_address,
)

query = (
    session.query(User)
    .from_statement(stmt)
    .options(contains_eager(User.addresses))
)
```

The [TextClause.columns()](#sqlalchemy.sql.expression.TextClause.columns) method provides a direct
route to calling `FromClause.subquery()` as well as
[SelectBase.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase.cte)
against a textual SELECT statement:

```
stmt = stmt.columns(id=Integer, name=String).cte("st")

stmt = select(sometable).where(sometable.c.id == stmt.c.id)
```

   Parameters:

- ***cols** – A series of [ColumnElement](#sqlalchemy.sql.expression.ColumnElement) objects,
  typically
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects from a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  or ORM level
  column-mapped attributes, representing a set of columns that this
  textual string will SELECT from.
- ****types** – A mapping of string names to [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)
  type objects indicating the datatypes to use for names that are
  SELECTed from the textual string.  Prefer to use the `*cols`
  argument as it also indicates positional ordering.

      method [sqlalchemy.sql.expression.TextClause.](#sqlalchemy.sql.expression.TextClause)self_group(*against:OperatorType|None=None*) → Self | Grouping[Any]

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.TextClause.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.TextClause.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

     class sqlalchemy.sql.expression.TryCast

*inherits from* [sqlalchemy.sql.expression.Cast](#sqlalchemy.sql.expression.Cast)

Represent a TRY_CAST expression.

Details on [TryCast](#sqlalchemy.sql.expression.TryCast) usage is at [try_cast()](#sqlalchemy.sql.expression.try_cast).

See also

[try_cast()](#sqlalchemy.sql.expression.try_cast)

[Data Casts and Type Coercion](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-casts)

| Member Name | Description |
| --- | --- |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |

   attribute [sqlalchemy.sql.expression.TryCast.](#sqlalchemy.sql.expression.TryCast)inherit_cache = True

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

      class sqlalchemy.sql.expression.Tuple

*inherits from* [sqlalchemy.sql.expression.ClauseList](#sqlalchemy.sql.expression.ClauseList), [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent a SQL tuple.

| Member Name | Description |
| --- | --- |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |

   method [sqlalchemy.sql.expression.Tuple.](#sqlalchemy.sql.expression.Tuple)self_group(*against:OperatorType|None=None*) → Self

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.Tuple.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.Tuple.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

     class sqlalchemy.sql.expression.WithinGroup

*inherits from* [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent a WITHIN GROUP (ORDER BY) clause.

This is a special operator against so-called
“ordered set aggregate” and “hypothetical
set aggregate” functions, including `percentile_cont()`,
`rank()`, `dense_rank()`, etc.

It’s supported only by certain database backends, such as PostgreSQL,
Oracle Database and MS SQL Server.

The [WithinGroup](#sqlalchemy.sql.expression.WithinGroup) construct extracts its type from the
method [FunctionElement.within_group_type()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.within_group_type).  If this returns
`None`, the function’s `.type` is used.

| Member Name | Description |
| --- | --- |
| filter() | Produce a FILTER clause against this function. |
| over() | Produce an OVER clause against thisWithinGroupconstruct. |

   method [sqlalchemy.sql.expression.WithinGroup.](#sqlalchemy.sql.expression.WithinGroup)filter(**criterion:_ColumnExpressionArgument[bool]*) → Self | [FunctionFilter](#sqlalchemy.sql.expression.FunctionFilter)[_T]

Produce a FILTER clause against this function.

    method [sqlalchemy.sql.expression.WithinGroup.](#sqlalchemy.sql.expression.WithinGroup)over(***, *partition_by:_ByArgument|None=None*, *order_by:_ByArgument|None=None*, *rows:typing_Tuple[int|None,int|None]|None=None*, *range_:typing_Tuple[int|None,int|None]|None=None*, *groups:typing_Tuple[int|None,int|None]|None=None*) → [Over](#sqlalchemy.sql.expression.Over)[_T]

Produce an OVER clause against this [WithinGroup](#sqlalchemy.sql.expression.WithinGroup)
construct.

This function has the same signature as that of
[FunctionElement.over()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.over).

     class sqlalchemy.sql.elements.WrapsColumnExpression

*inherits from* [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Mixin that defines a [ColumnElement](#sqlalchemy.sql.expression.ColumnElement)
as a wrapper with special
labeling behavior for an expression that already has a name.

Added in version 1.4.

See also

[Improved column labeling for simple column expressions using CAST or similar](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-4449)

     class sqlalchemy.sql.expression.True_

*inherits from* `sqlalchemy.sql.expression.SingletonConstant`, `sqlalchemy.sql.roles.ConstExprRole`, [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Represent the `true` keyword, or equivalent, in a SQL statement.

[True_](#sqlalchemy.sql.expression.True_) is accessed as a constant via the
[true()](#sqlalchemy.sql.expression.true) function.

    class sqlalchemy.sql.expression.TypeCoerce

*inherits from* `sqlalchemy.sql.expression.WrapsColumnExpression`

Represent a Python-side type-coercion wrapper.

[TypeCoerce](#sqlalchemy.sql.expression.TypeCoerce) supplies the [type_coerce()](#sqlalchemy.sql.expression.type_coerce)
function; see that function for usage details.

See also

[type_coerce()](#sqlalchemy.sql.expression.type_coerce)

[cast()](#sqlalchemy.sql.expression.cast)

| Member Name | Description |
| --- | --- |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |

   method [sqlalchemy.sql.expression.TypeCoerce.](#sqlalchemy.sql.expression.TypeCoerce)self_group(*against:OperatorType|None=None*) → [TypeCoerce](#sqlalchemy.sql.expression.TypeCoerce)[_T]

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.TypeCoerce.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.TypeCoerce.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

     class sqlalchemy.sql.expression.UnaryExpression

*inherits from* [sqlalchemy.sql.expression.ColumnElement](#sqlalchemy.sql.expression.ColumnElement)

Define a ‘unary’ expression.

A unary expression has a single column expression
and an operator.  The operator can be placed on the left
(where it is called the ‘operator’) or right (where it is called the
‘modifier’) of the column expression.

[UnaryExpression](#sqlalchemy.sql.expression.UnaryExpression) is the basis for several unary operators
including those used by [desc()](#sqlalchemy.sql.expression.desc), [asc()](#sqlalchemy.sql.expression.asc), [distinct()](#sqlalchemy.sql.expression.distinct),
[nulls_first()](#sqlalchemy.sql.expression.nulls_first) and [nulls_last()](#sqlalchemy.sql.expression.nulls_last).

| Member Name | Description |
| --- | --- |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |

   method [sqlalchemy.sql.expression.UnaryExpression.](#sqlalchemy.sql.expression.UnaryExpression)self_group(*against:OperatorType|None=None*) → Self | Grouping[_T]

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.UnaryExpression.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.UnaryExpression.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

## Column Element Typing Utilities

Standalone utility functions imported from the `sqlalchemy` namespace
to improve support by type checkers.

| Object Name | Description |
| --- | --- |
| NotNullable(val) | Types a column or ORM class as not nullable. |
| Nullable(val) | Types a column or ORM class as nullable. |

   function sqlalchemy.NotNullable(*val:_TypedColumnClauseArgument[_T|None]|Type[_T]|None*) → _TypedColumnClauseArgument[_T]

Types a column or ORM class as not nullable.

This can be used in select and other contexts to express that the value of
a column cannot be null, for example due to a where condition on a
nullable column:

```
stmt = select(NotNullable(A.value)).where(A.value.is_not(None))
```

At runtime this method returns the input unchanged.

Added in version 2.0.20.

     function sqlalchemy.Nullable(*val:_TypedColumnClauseArgument[_T]*) → _TypedColumnClauseArgument[_T | None]

Types a column or ORM class as nullable.

This can be used in select and other contexts to express that the value of
a column can be null, for example due to an outer join:

```
stmt1 = select(A, Nullable(B)).outerjoin(A.bs)
stmt2 = select(A.data, Nullable(B.data)).outerjoin(A.bs)
```

At runtime this method returns the input unchanged.

Added in version 2.0.20.
