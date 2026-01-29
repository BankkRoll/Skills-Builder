# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# SELECT and Related Constructs

The term “selectable” refers to any object that represents database rows. In
SQLAlchemy, these objects descend from [Selectable](#sqlalchemy.sql.expression.Selectable), the
most prominent being [Select](#sqlalchemy.sql.expression.Select), which represents a SQL SELECT
statement. A subset of [Selectable](#sqlalchemy.sql.expression.Selectable) is
[FromClause](#sqlalchemy.sql.expression.FromClause), which represents objects that can be within
the FROM clause of a [Select](#sqlalchemy.sql.expression.Select) statement. A distinguishing feature of
[FromClause](#sqlalchemy.sql.expression.FromClause) is the [FromClause.c](#sqlalchemy.sql.expression.FromClause.c)
attribute, which is a namespace of all the columns contained within the FROM
clause (these elements are themselves [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
subclasses).

## Selectable Foundational Constructors

Top level “FROM clause” and “SELECT” constructors.

| Object Name | Description |
| --- | --- |
| except_(*selects) | Return anEXCEPTof multiple selectables. |
| except_all(*selects) | Return anEXCEPTALLof multiple selectables. |
| exists([__argument]) | Construct a newExistsconstruct. |
| intersect(*selects) | Return anINTERSECTof multiple selectables. |
| intersect_all(*selects) | Return anINTERSECTALLof multiple selectables. |
| select(*entities, **__kw) | Construct a newSelect. |
| table(name, *columns, **kw) | Produce a newTableClause. |
| union(*selects) | Return aUNIONof multiple selectables. |
| union_all(*selects) | Return aUNIONALLof multiple selectables. |
| values(*columns, [name, literal_binds]) | Construct aValuesconstruct representing the
SQLVALUESclause. |

   function sqlalchemy.sql.expression.except_(**selects:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return an `EXCEPT` of multiple selectables.

The returned object is an instance of
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect).

  Parameters:

***selects** – a list of [Select](#sqlalchemy.sql.expression.Select) instances.

      function sqlalchemy.sql.expression.except_all(**selects:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return an `EXCEPT ALL` of multiple selectables.

The returned object is an instance of
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect).

  Parameters:

***selects** – a list of [Select](#sqlalchemy.sql.expression.Select) instances.

      function sqlalchemy.sql.expression.exists(*__argument:_ColumnsClauseArgument[Any]|SelectBase|ScalarSelect[Any]|None=None*) → [Exists](#sqlalchemy.sql.expression.Exists)

Construct a new [Exists](#sqlalchemy.sql.expression.Exists) construct.

The [exists()](#sqlalchemy.sql.expression.exists) can be invoked by itself to produce an
[Exists](#sqlalchemy.sql.expression.Exists) construct, which will accept simple WHERE
criteria:

```
exists_criteria = exists().where(table1.c.col1 == table2.c.col2)
```

However, for greater flexibility in constructing the SELECT, an
existing [Select](#sqlalchemy.sql.expression.Select) construct may be converted to an
[Exists](#sqlalchemy.sql.expression.Exists), most conveniently by making use of the
[SelectBase.exists()](#sqlalchemy.sql.expression.SelectBase.exists) method:

```
exists_criteria = (
    select(table2.c.col2).where(table1.c.col1 == table2.c.col2).exists()
)
```

The EXISTS criteria is then used inside of an enclosing SELECT:

```
stmt = select(table1.c.col1).where(exists_criteria)
```

The above statement will then be of the form:

```
SELECT col1 FROM table1 WHERE EXISTS
(SELECT table2.col2 FROM table2 WHERE table2.col2 = table1.col1)
```

See also

[EXISTS subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-exists) - in the [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) tutorial.

[SelectBase.exists()](#sqlalchemy.sql.expression.SelectBase.exists) - method to transform a `SELECT` to an
`EXISTS` clause.

     function sqlalchemy.sql.expression.intersect(**selects:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return an `INTERSECT` of multiple selectables.

The returned object is an instance of
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect).

  Parameters:

***selects** – a list of [Select](#sqlalchemy.sql.expression.Select) instances.

      function sqlalchemy.sql.expression.intersect_all(**selects:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return an `INTERSECT ALL` of multiple selectables.

The returned object is an instance of
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect).

  Parameters:

***selects** – a list of [Select](#sqlalchemy.sql.expression.Select) instances.

      function sqlalchemy.sql.expression.select(**entities:_ColumnsClauseArgument[Any]*, ***__kw:Any*) → [Select](#sqlalchemy.sql.expression.Select)[Any]

Construct a new [Select](#sqlalchemy.sql.expression.Select).

Added in version 1.4: - The [select()](#sqlalchemy.sql.expression.select) function now accepts
column arguments positionally.   The top-level [select()](#sqlalchemy.sql.expression.select)
function will automatically use the 1.x or 2.x style API based on
the incoming arguments; using [select()](#sqlalchemy.sql.expression.select) from the
`sqlalchemy.future` module will enforce that only the 2.x style
constructor is used.

Similar functionality is also available via the
[FromClause.select()](#sqlalchemy.sql.expression.FromClause.select) method on any
[FromClause](#sqlalchemy.sql.expression.FromClause).

See also

[Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-data) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

   Parameters:

***entities** –

Entities to SELECT from.  For Core usage, this is typically a series
of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) and / or
[FromClause](#sqlalchemy.sql.expression.FromClause)
objects which will form the columns clause of the resulting
statement.   For those objects that are instances of
[FromClause](#sqlalchemy.sql.expression.FromClause) (typically [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
or [Alias](#sqlalchemy.sql.expression.Alias)
objects), the [FromClause.c](#sqlalchemy.sql.expression.FromClause.c)
collection is extracted
to form a collection of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects.

This parameter will also accept [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause)
constructs as
given, as well as ORM-mapped classes.

      function sqlalchemy.sql.expression.table(*name:str*, **columns:ColumnClause[Any]*, ***kw:Any*) → [TableClause](#sqlalchemy.sql.expression.TableClause)

Produce a new [TableClause](#sqlalchemy.sql.expression.TableClause).

The object returned is an instance of
[TableClause](#sqlalchemy.sql.expression.TableClause), which
represents the “syntactical” portion of the schema-level
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.
It may be used to construct lightweight table constructs.

  Parameters:

- **name** – Name of the table.
- **columns** – A collection of [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) constructs.
- **schema** –
  The schema name for this table.
  Added in version 1.3.18: [table()](#sqlalchemy.sql.expression.table) can now
  accept a `schema` argument.

      function sqlalchemy.sql.expression.union(**selects:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return a `UNION` of multiple selectables.

The returned object is an instance of
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect).

A similar [union()](#sqlalchemy.sql.expression.union) method is available on all
[FromClause](#sqlalchemy.sql.expression.FromClause) subclasses.

  Parameters:

- ***selects** – a list of [Select](#sqlalchemy.sql.expression.Select) instances.
- ****kwargs** – available keyword arguments are the same as those of
  [select()](#sqlalchemy.sql.expression.select).

      function sqlalchemy.sql.expression.union_all(**selects:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return a `UNION ALL` of multiple selectables.

The returned object is an instance of
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect).

A similar [union_all()](#sqlalchemy.sql.expression.union_all) method is available on all
[FromClause](#sqlalchemy.sql.expression.FromClause) subclasses.

  Parameters:

***selects** – a list of [Select](#sqlalchemy.sql.expression.Select) instances.

      function sqlalchemy.sql.expression.values(**columns:_OnlyColumnArgument[Any]*, *name:str|None=None*, *literal_binds:bool=False*) → [Values](#sqlalchemy.sql.expression.Values)

Construct a [Values](#sqlalchemy.sql.expression.Values) construct representing the
SQL `VALUES` clause.

The column expressions and the actual data for [Values](#sqlalchemy.sql.expression.Values)
are given in two separate steps.  The constructor receives the column
expressions typically as [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) constructs, and the
data is then passed via the [Values.data()](#sqlalchemy.sql.expression.Values.data) method as a
list, which can be called multiple times to add more data, e.g.:

```
from sqlalchemy import column
from sqlalchemy import values
from sqlalchemy import Integer
from sqlalchemy import String

value_expr = (
    values(
        column("id", Integer),
        column("name", String),
    )
    .data([(1, "name1"), (2, "name2")])
    .data([(3, "name3")])
)
```

Would represent a SQL fragment like:

```
VALUES(1, "name1"), (2, "name2"), (3, "name3")
```

The [values](#sqlalchemy.sql.expression.values) construct has an optional
[values.name](#sqlalchemy.sql.expression.values.params.name) field; when using this field, the
PostgreSQL-specific “named VALUES” clause may be generated:

```
value_expr = values(
    column("id", Integer), column("name", String), name="somename"
).data([(1, "name1"), (2, "name2"), (3, "name3")])
```

When selecting from the above construct, the name and column names will
be listed out using a PostgreSQL-specific syntax:

```
>>> print(value_expr.select())
SELECT somename.id, somename.name
FROM (VALUES (:param_1, :param_2), (:param_3, :param_4),
(:param_5, :param_6)) AS somename (id, name)
```

For a more database-agnostic means of SELECTing named columns from a
VALUES expression, the [Values.cte()](#sqlalchemy.sql.expression.Values.cte) method may be used, which
produces a named CTE with explicit column names against the VALUES
construct within; this syntax works on PostgreSQL, SQLite, and MariaDB:

```
value_expr = (
    values(
        column("id", Integer),
        column("name", String),
    )
    .data([(1, "name1"), (2, "name2"), (3, "name3")])
    .cte()
)
```

Rendering as:

```
>>> print(value_expr.select())
WITH anon_1(id, name) AS
(VALUES (:param_1, :param_2), (:param_3, :param_4), (:param_5, :param_6))
SELECT anon_1.id, anon_1.name
FROM anon_1
```

Added in version 2.0.42: Added the [Values.cte()](#sqlalchemy.sql.expression.Values.cte) method to
[Values](#sqlalchemy.sql.expression.Values)

   Parameters:

- ***columns** – column expressions, typically composed using
  [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) objects.
- **name** – the name for this VALUES construct.  If omitted, the
  VALUES construct will be unnamed in a SQL expression.   Different
  backends may have different requirements here.
- **literal_binds** – Defaults to False.  Whether or not to render
  the data values inline in the SQL output, rather than using bound
  parameters.

## Selectable Modifier Constructors

Functions listed here are more commonly available as methods from
[FromClause](#sqlalchemy.sql.expression.FromClause) and [Selectable](#sqlalchemy.sql.expression.Selectable) elements, for example,
the [alias()](#sqlalchemy.sql.expression.alias) function is usually invoked via the
[FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias) method.

| Object Name | Description |
| --- | --- |
| alias(selectable[, name, flat]) | Return a named alias of the givenFromClause. |
| cte(selectable[, name, recursive]) | Return a newCTE,
or Common Table Expression instance. |
| join(left, right[, onclause, isouter, ...]) | Produce aJoinobject, given twoFromClauseexpressions. |
| lateral(selectable[, name]) | Return aLateralobject. |
| outerjoin(left, right[, onclause, full]) | Return anOUTERJOINclause element. |
| tablesample(selectable, sampling[, name, seed]) | Return aTableSampleobject. |

   function sqlalchemy.sql.expression.alias(*selectable:FromClause*, *name:str|None=None*, *flat:bool=False*) → NamedFromClause

Return a named alias of the given [FromClause](#sqlalchemy.sql.expression.FromClause).

For [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Join](#sqlalchemy.sql.expression.Join) objects, the return type is the
[Alias](#sqlalchemy.sql.expression.Alias) object. Other kinds of `NamedFromClause`
objects may be returned for other kinds of [FromClause](#sqlalchemy.sql.expression.FromClause) objects.

The named alias represents any [FromClause](#sqlalchemy.sql.expression.FromClause) with an
alternate name assigned within SQL, typically using the `AS` clause when
generated, e.g. `SELECT * FROM table AS aliasname`.

Equivalent functionality is available via the
[FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias)
method available on all [FromClause](#sqlalchemy.sql.expression.FromClause) objects.

  Parameters:

- **selectable** – any [FromClause](#sqlalchemy.sql.expression.FromClause) subclass,
  such as a table, select statement, etc.
- **name** – string name to be assigned as the alias.
  If `None`, a name will be deterministically generated at compile
  time. Deterministic means the name is guaranteed to be unique against
  other constructs used in the same statement, and will also be the same
  name for each successive compilation of the same statement object.
- **flat** – Will be passed through to if the given selectable
  is an instance of [Join](#sqlalchemy.sql.expression.Join) - see
  `Join.alias()` for details.

      function sqlalchemy.sql.expression.cte(*selectable:HasCTE*, *name:str|None=None*, *recursive:bool=False*) → [CTE](#sqlalchemy.sql.expression.CTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE),
or Common Table Expression instance.

Please see [HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) for detail on CTE usage.

    function sqlalchemy.sql.expression.join(*left:_FromClauseArgument*, *right:_FromClauseArgument*, *onclause:_OnClauseArgument|None=None*, *isouter:bool=False*, *full:bool=False*) → [Join](#sqlalchemy.sql.expression.Join)

Produce a [Join](#sqlalchemy.sql.expression.Join) object, given two
[FromClause](#sqlalchemy.sql.expression.FromClause)
expressions.

E.g.:

```
j = join(
    user_table, address_table, user_table.c.id == address_table.c.user_id
)
stmt = select(user_table).select_from(j)
```

would emit SQL along the lines of:

```
SELECT user.id, user.name FROM user
JOIN address ON user.id = address.user_id
```

Similar functionality is available given any
[FromClause](#sqlalchemy.sql.expression.FromClause) object (e.g. such as a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)) using
the [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join) method.

  Parameters:

- **left** – The left side of the join.
- **right** – the right side of the join; this is any
  [FromClause](#sqlalchemy.sql.expression.FromClause) object such as a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, and
  may also be a selectable-compatible object such as an ORM-mapped
  class.
- **onclause** – a SQL expression representing the ON clause of the
  join.  If left at `None`, [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)
  will attempt to
  join the two tables based on a foreign key relationship.
- **isouter** – if True, render a LEFT OUTER JOIN, instead of JOIN.
- **full** – if True, render a FULL OUTER JOIN, instead of JOIN.

See also

[FromClause.join()](#sqlalchemy.sql.expression.FromClause.join) - method form,
based on a given left side.

[Join](#sqlalchemy.sql.expression.Join) - the type of object produced.

     function sqlalchemy.sql.expression.lateral(*selectable:SelectBase|_FromClauseArgument*, *name:str|None=None*) → LateralFromClause

Return a [Lateral](#sqlalchemy.sql.expression.Lateral) object.

[Lateral](#sqlalchemy.sql.expression.Lateral) is an [Alias](#sqlalchemy.sql.expression.Alias)
subclass that represents
a subquery with the LATERAL keyword applied to it.

The special behavior of a LATERAL subquery is that it appears in the
FROM clause of an enclosing SELECT, but may correlate to other
FROM clauses of that SELECT.   It is a special case of subquery
only supported by a small number of backends, currently more recent
PostgreSQL versions.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

     function sqlalchemy.sql.expression.outerjoin(*left:_FromClauseArgument*, *right:_FromClauseArgument*, *onclause:_OnClauseArgument|None=None*, *full:bool=False*) → [Join](#sqlalchemy.sql.expression.Join)

Return an `OUTER JOIN` clause element.

The returned object is an instance of [Join](#sqlalchemy.sql.expression.Join).

Similar functionality is also available via the
[FromClause.outerjoin()](#sqlalchemy.sql.expression.FromClause.outerjoin) method on any
[FromClause](#sqlalchemy.sql.expression.FromClause).

  Parameters:

- **left** – The left side of the join.
- **right** – The right side of the join.
- **onclause** – Optional criterion for the `ON` clause, is
  derived from foreign key relationships established between
  left and right otherwise.

To chain joins together, use the [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)
or
[FromClause.outerjoin()](#sqlalchemy.sql.expression.FromClause.outerjoin) methods on the resulting
[Join](#sqlalchemy.sql.expression.Join) object.

    function sqlalchemy.sql.expression.tablesample(*selectable:_FromClauseArgument*, *sampling:float|Function[Any]*, *name:str|None=None*, *seed:roles.ExpressionElementRole[Any]|None=None*) → [TableSample](#sqlalchemy.sql.expression.TableSample)

Return a [TableSample](#sqlalchemy.sql.expression.TableSample) object.

[TableSample](#sqlalchemy.sql.expression.TableSample) is an [Alias](#sqlalchemy.sql.expression.Alias)
subclass that represents
a table with the TABLESAMPLE clause applied to it.
[tablesample()](#sqlalchemy.sql.expression.tablesample)
is also available from the [FromClause](#sqlalchemy.sql.expression.FromClause)
class via the
[FromClause.tablesample()](#sqlalchemy.sql.expression.FromClause.tablesample) method.

The TABLESAMPLE clause allows selecting a randomly selected approximate
percentage of rows from a table. It supports multiple sampling methods,
most commonly BERNOULLI and SYSTEM.

e.g.:

```
from sqlalchemy import func

selectable = people.tablesample(
    func.bernoulli(1), name="alias", seed=func.random()
)
stmt = select(selectable.c.people_id)
```

Assuming `people` with a column `people_id`, the above
statement would render as:

```
SELECT alias.people_id FROM
people AS alias TABLESAMPLE bernoulli(:bernoulli_1)
REPEATABLE (random())
```

   Parameters:

- **sampling** – a `float` percentage between 0 and 100 or
  [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function).
- **name** – optional alias name
- **seed** – any real-valued SQL expression.  When specified, the
  REPEATABLE sub-clause is also rendered.

## Selectable Class Documentation

The classes here are generated using the constructors listed at
[Selectable Foundational Constructors](#selectable-foundational-constructors) and
[Selectable Modifier Constructors](#fromclause-modifier-constructors).

| Object Name | Description |
| --- | --- |
| Alias | Represents an table or selectable alias (AS). |
| AliasedReturnsRows | Base class of aliases against tables, subqueries, and other
selectables. |
| CompoundSelect | Forms the basis ofUNION,UNIONALL, and other
SELECT-based set operations. |
| CTE | Represent a Common Table Expression. |
| Executable | Mark aClauseElementas supporting execution. |
| Exists | Represent anEXISTSclause. |
| FromClause | Represent an element that can be used within theFROMclause of aSELECTstatement. |
| GenerativeSelect | Base class for SELECT statements where additional elements can be
added. |
| HasCTE | Mixin that declares a class to include CTE support. |
| HasPrefixes |  |
| HasSuffixes |  |
| Join | Represent aJOINconstruct between twoFromClauseelements. |
| Lateral | Represent a LATERAL subquery. |
| ReturnsRows | The base-most class for Core constructs that have some concept of
columns that can represent rows. |
| ScalarSelect | Represent a scalar subquery. |
| ScalarValues | Represent a scalarVALUESconstruct that can be used as a
COLUMN element in a statement. |
| Select | Represents aSELECTstatement. |
| Selectable | Mark a class as being selectable. |
| SelectBase | Base class for SELECT statements. |
| Subquery | Represent a subquery of a SELECT. |
| TableClause | Represents a minimal “table” construct. |
| TableSample | Represent a TABLESAMPLE clause. |
| TableValuedAlias | An alias against a “table valued” SQL function. |
| TextualSelect | Wrap aTextClauseconstruct within aSelectBaseinterface. |
| Values | Represent aVALUESconstruct that can be used as a FROM element
in a statement. |

   class sqlalchemy.sql.expression.Alias

*inherits from* `sqlalchemy.sql.roles.DMLTableRole`, `sqlalchemy.sql.expression.FromClauseAlias`

Represents an table or selectable alias (AS).

Represents an alias, as typically applied to any table or
sub-select within a SQL statement using the `AS` keyword (or
without the keyword on certain databases such as Oracle Database).

This object is constructed from the [alias()](#sqlalchemy.sql.expression.alias) module
level function as well as the [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias)
method available
on all [FromClause](#sqlalchemy.sql.expression.FromClause) subclasses.

See also

[FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias)

| Member Name | Description |
| --- | --- |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |

   attribute [sqlalchemy.sql.expression.Alias.](#sqlalchemy.sql.expression.Alias)inherit_cache = True

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

      class sqlalchemy.sql.expression.AliasedReturnsRows

*inherits from* `sqlalchemy.sql.expression.NoInit`, `sqlalchemy.sql.expression.NamedFromClause`

Base class of aliases against tables, subqueries, and other
selectables.

| Member Name | Description |
| --- | --- |
| description |  |
| is_derived_from() | ReturnTrueif thisFromClauseis
‘derived’ from the givenFromClause. |

   attribute [sqlalchemy.sql.expression.AliasedReturnsRows.](#sqlalchemy.sql.expression.AliasedReturnsRows)description    method [sqlalchemy.sql.expression.AliasedReturnsRows.](#sqlalchemy.sql.expression.AliasedReturnsRows)is_derived_from(*fromclause:FromClause|None*) → bool

Return `True` if this [FromClause](#sqlalchemy.sql.expression.FromClause) is
‘derived’ from the given `FromClause`.

An example would be an Alias of a Table is derived from that Table.

    property original: [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows)

Legacy for dialects that are referring to Alias.original.

     class sqlalchemy.sql.expression.CompoundSelect

*inherits from* `sqlalchemy.sql.expression.HasCompileState`, [sqlalchemy.sql.expression.GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect), `sqlalchemy.sql.expression.TypedReturnsRows`

Forms the basis of `UNION`, `UNION ALL`, and other
SELECT-based set operations.

See also

[union()](#sqlalchemy.sql.expression.union)

[union_all()](#sqlalchemy.sql.expression.union_all)

[intersect()](#sqlalchemy.sql.expression.intersect)

[intersect_all()](#sqlalchemy.sql.expression.intersect_all)

`except()`

[except_all()](#sqlalchemy.sql.expression.except_all)

| Member Name | Description |
| --- | --- |
| add_cte() | Add one or moreCTEconstructs to this statement. |
| alias() | Return a named subquery against thisSelectBase. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| as_scalar() |  |
| compile() | Compile this SQL expression. |
| corresponding_column() | Given aColumnElement, return the exportedColumnElementobject from theSelectable.exported_columnscollection of thisSelectablewhich corresponds to that
originalColumnElementvia a common ancestor
column. |
| cte() | Return a newCTE,
or Common Table Expression instance. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| execution_options() | Set non-SQL options for the statement which take effect during
execution. |
| exists() | Return anExistsrepresentation of this selectable,
which can be used as a column expression. |
| fetch() | Return a new selectable with the given FETCH FIRST criterion
applied. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| get_execution_options() | Get the non-SQL options which will take effect during execution. |
| get_label_style() | Retrieve the current label style. |
| group_by() | Return a new selectable with the given list of GROUP BY
criterion applied. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| is_derived_from() | ReturnTrueif thisReturnsRowsis
‘derived’ from the givenFromClause. |
| label() | Return a ‘scalar’ representation of this selectable, embedded as a
subquery with a label. |
| lateral() | Return a LATERAL alias of thisSelectable. |
| limit() | Return a new selectable with the given LIMIT criterion
applied. |
| name_cte_columns | indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause. |
| offset() | Return a new selectable with the given OFFSET criterion
applied. |
| options() | Apply options to this statement. |
| order_by() | Return a new selectable with the given list of ORDER BY
criteria applied. |
| replace_selectable() | Replace all occurrences ofFromClause‘old’ with the givenAliasobject, returning a copy of thisFromClause. |
| scalar_subquery() | Return a ‘scalar’ representation of this selectable, which can be
used as a column expression. |
| select() |  |
| selected_columns | AColumnCollectionrepresenting the columns that
this SELECT statement or similar construct returns in its result set,
not includingTextClauseconstructs. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| set_label_style() | Return a new selectable with the specified label style. |
| slice() | Apply LIMIT / OFFSET to this statement based on a slice. |
| subquery() | Return a subquery of thisSelectBase. |
| with_for_update() | Specify aFORUPDATEclause for thisGenerativeSelect. |

   method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)add_cte(**ctes:CTE*, *nest_here:bool=False*) → Self

*inherited from the* [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Add one or more [CTE](#sqlalchemy.sql.expression.CTE) constructs to this statement.

This method will associate the given [CTE](#sqlalchemy.sql.expression.CTE) constructs with
the parent statement such that they will each be unconditionally
rendered in the WITH clause of the final statement, even if not
referenced elsewhere within the statement or any sub-selects.

The optional [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here) parameter when set
to True will have the effect that each given [CTE](#sqlalchemy.sql.expression.CTE) will
render in a WITH clause rendered directly along with this statement,
rather than being moved to the top of the ultimate rendered statement,
even if this statement is rendered as a subquery within a larger
statement.

This method has two general uses. One is to embed CTE statements that
serve some purpose without being referenced explicitly, such as the use
case of embedding a DML statement such as an INSERT or UPDATE as a CTE
inline with a primary statement that may draw from its results
indirectly.  The other is to provide control over the exact placement
of a particular series of CTE constructs that should remain rendered
directly in terms of a particular statement that may be nested in a
larger statement.

E.g.:

```
from sqlalchemy import table, column, select

t = table("t", column("c1"), column("c2"))

ins = t.insert().values({"c1": "x", "c2": "y"}).cte()

stmt = select(t).add_cte(ins)
```

Would render:

```
WITH anon_1 AS (
    INSERT INTO t (c1, c2) VALUES (:param_1, :param_2)
)
SELECT t.c1, t.c2
FROM t
```

Above, the “anon_1” CTE is not referenced in the SELECT
statement, however still accomplishes the task of running an INSERT
statement.

Similarly in a DML-related context, using the PostgreSQL
[Insert](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert) construct to generate an “upsert”:

```
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import insert

t = table("t", column("c1"), column("c2"))

delete_statement_cte = t.delete().where(t.c.c1 < 1).cte("deletions")

insert_stmt = insert(t).values({"c1": 1, "c2": 2})
update_statement = insert_stmt.on_conflict_do_update(
    index_elements=[t.c.c1],
    set_={
        "c1": insert_stmt.excluded.c1,
        "c2": insert_stmt.excluded.c2,
    },
).add_cte(delete_statement_cte)

print(update_statement)
```

The above statement renders as:

```
WITH deletions AS (
    DELETE FROM t WHERE t.c1 < %(c1_1)s
)
INSERT INTO t (c1, c2) VALUES (%(c1)s, %(c2)s)
ON CONFLICT (c1) DO UPDATE SET c1 = excluded.c1, c2 = excluded.c2
```

Added in version 1.4.21.

   Parameters:

- ***ctes** –
  zero or more [CTE](#sqlalchemy.sql.expression.CTE) constructs.
  Changed in version 2.0: Multiple CTE instances are accepted
- **nest_here** –
  if True, the given CTE or CTEs will be rendered
  as though they specified the [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting) flag
  to `True` when they were added to this [HasCTE](#sqlalchemy.sql.expression.HasCTE).
  Assuming the given CTEs are not referenced in an outer-enclosing
  statement as well, the CTEs given should render at the level of
  this statement when this flag is given.
  Added in version 2.0.
  See also
  [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting)

      method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)alias(*name:str|None=None*, *flat:bool=False*) → [Subquery](#sqlalchemy.sql.expression.Subquery)

*inherited from the* [SelectBase.alias()](#sqlalchemy.sql.expression.SelectBase.alias) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a named subquery against this
[SelectBase](#sqlalchemy.sql.expression.SelectBase).

For a [SelectBase](#sqlalchemy.sql.expression.SelectBase) (as opposed to a
[FromClause](#sqlalchemy.sql.expression.FromClause)),
this returns a [Subquery](#sqlalchemy.sql.expression.Subquery) object which behaves mostly the
same as the [Alias](#sqlalchemy.sql.expression.Alias) object that is used with a
[FromClause](#sqlalchemy.sql.expression.FromClause).

Changed in version 1.4: The [SelectBase.alias()](#sqlalchemy.sql.expression.SelectBase.alias)
method is now
a synonym for the [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) method.

     classmethod [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

*inherited from the* `DialectKWArgs.argument_for()` *method of* `DialectKWArgs`

Add a new kind of dialect-specific keyword argument for this class.

E.g.:

```
Index.argument_for("mydialect", "length", None)

some_index = Index("a", "b", mydialect_length=5)
```

The [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for) method is a per-argument
way adding extra arguments to the
[DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) dictionary. This
dictionary provides a list of argument names accepted by various
schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a
data member of the dialect class.  The use case for ad-hoc addition of
argument names is typically for end-user code that is also using
a custom compilation scheme which consumes the additional arguments.

  Parameters:

- **dialect_name** – name of a dialect.  The dialect must be
  locatable, else a [NoSuchModuleError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchModuleError) is raised.   The
  dialect must also include an existing
  [DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) collection, indicating
  that it participates in the keyword-argument validation and default
  system, else [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is raised.  If the dialect does
  not include this collection, then any keyword argument can be
  specified on behalf of this dialect already.  All dialects packaged
  within SQLAlchemy include this collection, however for third party
  dialects, support may vary.
- **argument_name** – name of the parameter.
- **default** – default value of the parameter.

      method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)as_scalar() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

*inherited from the* [SelectBase.as_scalar()](#sqlalchemy.sql.expression.SelectBase.as_scalar) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Deprecated since version 1.4: The [SelectBase.as_scalar()](#sqlalchemy.sql.expression.SelectBase.as_scalar) method is deprecated and will be removed in a future release.  Please refer to [SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

     property c: ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]

Deprecated since version 1.4: The [SelectBase.c](#sqlalchemy.sql.expression.SelectBase.c) and `SelectBase.columns` attributes are deprecated and will be removed in a future release; these attributes implicitly create a subquery that should be explicit.  Please call [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) first in order to create a subquery, which then contains this attribute.  To access the columns that this SELECT object SELECTs from, use the [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) attribute.

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

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

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)corresponding_column(*column:KeyedColumnElement[Any]*, *require_embedded:bool=False*) → KeyedColumnElement[Any] | None

*inherited from the* [Selectable.corresponding_column()](#sqlalchemy.sql.expression.Selectable.corresponding_column) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Given a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), return the exported
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) object from the
[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)
collection of this [Selectable](#sqlalchemy.sql.expression.Selectable)
which corresponds to that
original [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) via a common ancestor
column.

  Parameters:

- **column** – the target [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  to be matched.
- **require_embedded** – only return corresponding columns for
  the given [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), if the given
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  is actually present within a sub-element
  of this [Selectable](#sqlalchemy.sql.expression.Selectable).
  Normally the column will match if
  it merely shares a common ancestor with one of the exported
  columns of this [Selectable](#sqlalchemy.sql.expression.Selectable).

See also

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns) - the
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that is used for the operation.

[ColumnCollection.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.corresponding_column)
- implementation
method.

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)cte(*name:str|None=None*, *recursive:bool=False*, *nesting:bool=False*) → [CTE](#sqlalchemy.sql.expression.CTE)

*inherited from the* [HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE),
or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT
statements can draw upon secondary statements specified along
with the primary statement, using a clause called “WITH”.
Special semantics regarding UNION can also be employed to
allow “recursive” queries, where a SELECT statement can draw
upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT
and DELETE on some databases, both as a source of CTE rows
when combined with RETURNING, as well as a consumer of
CTE rows.

SQLAlchemy detects [CTE](#sqlalchemy.sql.expression.CTE) objects, which are treated
similarly to [Alias](#sqlalchemy.sql.expression.Alias) objects, as special elements
to be delivered to the FROM clause of the statement as well
as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and
“NOT MATERIALIZED”, the `CTE.prefix_with()`
method may be
used to establish these.

Changed in version 1.3.13: Added support for prefixes.
In particular - MATERIALIZED and NOT MATERIALIZED.

   Parameters:

- **name** – name given to the common table expression.  Like
  [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias), the name can be left as
  `None` in which case an anonymous symbol will be used at query
  compile time.
- **recursive** – if `True`, will render `WITH RECURSIVE`.
  A recursive common table expression is intended to be used in
  conjunction with UNION ALL in order to derive rows
  from those already selected.
- **nesting** –
  if `True`, will render the CTE locally to the
  statement in which it is referenced.   For more complex scenarios,
  the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method using the
  [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here)
  parameter may also be used to more carefully
  control the exact placement of a particular CTE.
  Added in version 1.4.24.
  See also
  [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte)

The following examples include two from PostgreSQL’s documentation at
[https://www.postgresql.org/docs/current/static/queries-with.html](https://www.postgresql.org/docs/current/static/queries-with.html),
as well as additional examples.

Example 1, non recursive:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("region", String),
    Column("amount", Integer),
    Column("product", String),
    Column("quantity", Integer),
)

regional_sales = (
    select(orders.c.region, func.sum(orders.c.amount).label("total_sales"))
    .group_by(orders.c.region)
    .cte("regional_sales")
)

top_regions = (
    select(regional_sales.c.region)
    .where(
        regional_sales.c.total_sales
        > select(func.sum(regional_sales.c.total_sales) / 10)
    )
    .cte("top_regions")
)

statement = (
    select(
        orders.c.region,
        orders.c.product,
        func.sum(orders.c.quantity).label("product_units"),
        func.sum(orders.c.amount).label("product_sales"),
    )
    .where(orders.c.region.in_(select(top_regions.c.region)))
    .group_by(orders.c.region, orders.c.product)
)

result = conn.execute(statement).fetchall()
```

Example 2, WITH RECURSIVE:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

parts = Table(
    "parts",
    metadata,
    Column("part", String),
    Column("sub_part", String),
    Column("quantity", Integer),
)

included_parts = (
    select(parts.c.sub_part, parts.c.part, parts.c.quantity)
    .where(parts.c.part == "our part")
    .cte(recursive=True)
)

incl_alias = included_parts.alias()
parts_alias = parts.alias()
included_parts = included_parts.union_all(
    select(
        parts_alias.c.sub_part, parts_alias.c.part, parts_alias.c.quantity
    ).where(parts_alias.c.part == incl_alias.c.sub_part)
)

statement = select(
    included_parts.c.sub_part,
    func.sum(included_parts.c.quantity).label("total_quantity"),
).group_by(included_parts.c.sub_part)

result = conn.execute(statement).fetchall()
```

Example 3, an upsert using UPDATE and INSERT with CTEs:

```
from datetime import date
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Date,
    select,
    literal,
    and_,
    exists,
)

metadata = MetaData()

visitors = Table(
    "visitors",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("date", Date, primary_key=True),
    Column("count", Integer),
)

# add 5 visitors for the product_id == 1
product_id = 1
day = date.today()
count = 5

update_cte = (
    visitors.update()
    .where(
        and_(visitors.c.product_id == product_id, visitors.c.date == day)
    )
    .values(count=visitors.c.count + count)
    .returning(literal(1))
    .cte("update_cte")
)

upsert = visitors.insert().from_select(
    [visitors.c.product_id, visitors.c.date, visitors.c.count],
    select(literal(product_id), literal(day), literal(count)).where(
        ~exists(update_cte.select())
    ),
)

connection.execute(upsert)
```

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte(
    "value_a", nesting=True
)

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = select(value_a_nested.c.n).cte("value_b")

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

The above query will render the second CTE nested inside the first,
shown with inline parameters below as:

```
WITH
    value_a AS
        (SELECT 'root' AS n),
    value_b AS
        (WITH value_a AS
            (SELECT 'nesting' AS n)
        SELECT value_a.n AS n FROM value_a)
SELECT value_a.n AS a, value_b.n AS b
FROM value_a, value_b
```

The same CTE can be set up using the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method
as follows (SQLAlchemy 2.0 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte("value_a")

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = (
    select(value_a_nested.c.n)
    .add_cte(value_a_nested, nest_here=True)
    .cte("value_b")
)

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

```
edge = Table(
    "edge",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("left", Integer),
    Column("right", Integer),
)

root_node = select(literal(1).label("node")).cte("nodes", recursive=True)

left_edge = select(edge.c.left).join(
    root_node, edge.c.right == root_node.c.node
)
right_edge = select(edge.c.right).join(
    root_node, edge.c.left == root_node.c.node
)

subgraph_cte = root_node.union(left_edge, right_edge)

subgraph = select(subgraph_cte)
```

The above query will render 2 UNIONs inside the recursive CTE:

```
WITH RECURSIVE nodes(node) AS (
        SELECT 1 AS node
    UNION
        SELECT edge."left" AS "left"
        FROM edge JOIN nodes ON edge."right" = nodes.node
    UNION
        SELECT edge."right" AS "right"
        FROM edge JOIN nodes ON edge."left" = nodes.node
)
SELECT nodes.node FROM nodes
```

See also

[Query.cte()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.cte) - ORM version of
[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte).

     property dialect_kwargs: _DialectArgView

A collection of keyword arguments specified as dialect-specific
options to this construct.

The arguments are present here in their original `<dialect>_<kwarg>`
format.  Only arguments that were actually passed are included;
unlike the [DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options) collection, which
contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the
form `<dialect>_<kwarg>` where the value will be assembled
into the list of options.

See also

[DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options) - nested dictionary form

     attribute [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)dialect_options

*inherited from the* `DialectKWArgs.dialect_options` *attribute of* `DialectKWArgs`

A collection of keyword arguments specified as dialect-specific
options to this construct.

This is a two-level nested registry, keyed to `<dialect_name>`
and `<argument_name>`.  For example, the `postgresql_where`
argument would be locatable as:

```
arg = my_object.dialect_options["postgresql"]["where"]
```

Added in version 0.9.2.

See also

[DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs) - flat dictionary form

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)execution_options(***kw:Any*) → Self

*inherited from the* [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Set non-SQL options for the statement which take effect during
execution.

Execution options can be set at many scopes, including per-statement,
per-connection, or per execution, using methods such as
[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) and parameters which
accept a dictionary of options such as
[Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options) and
[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options).

The primary characteristic of an execution option, as opposed to
other kinds of options such as ORM loader options, is that
**execution options never affect the compiled SQL of a query, only
things that affect how the SQL statement itself is invoked or how
results are fetched**.  That is, execution options are not part of
what’s accommodated by SQL compilation nor are they considered part of
the cached state of a statement.

The [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) method is
[generative](https://docs.sqlalchemy.org/en/20/glossary.html#term-generative), as
is the case for the method as applied to the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
and [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects, which means when the method is called,
a copy of the object is returned, which applies the given parameters to
that new copy, but leaves the original unchanged:

```
statement = select(table.c.x, table.c.y)
new_statement = statement.execution_options(my_option=True)
```

An exception to this behavior is the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
object, where the [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) method
is explicitly **not** generative.

The kinds of options that may be passed to
[Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) and other related methods and
parameter dictionaries include parameters that are explicitly consumed
by SQLAlchemy Core or ORM, as well as arbitrary keyword arguments not
defined by SQLAlchemy, which means the methods and/or parameter
dictionaries may be used for user-defined parameters that interact with
custom code, which may access the parameters using methods such as
[Executable.get_execution_options()](#sqlalchemy.sql.expression.Executable.get_execution_options) and
[Connection.get_execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_execution_options), or within selected
event hooks using a dedicated `execution_options` event parameter
such as
[ConnectionEvents.before_execute.execution_options](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_execute.params.execution_options)
or [ORMExecuteState.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.execution_options), e.g.:

```
from sqlalchemy import event

@event.listens_for(some_engine, "before_execute")
def _process_opt(conn, statement, multiparams, params, execution_options):
    "run a SQL function before invoking a statement"

    if execution_options.get("do_special_thing", False):
        conn.exec_driver_sql("run_special_function()")
```

Within the scope of options that are explicitly recognized by
SQLAlchemy, most apply to specific classes of objects and not others.
The most common execution options include:

- [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
  sets the isolation level for a connection or a class of connections
  via an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).  This option is accepted only
  by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).
- [Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results) -
  indicates results should be fetched using a server side cursor;
  this option is accepted by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), by the
  [Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options) parameter
  on [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), and additionally by
  [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) on a SQL statement object,
  as well as by ORM constructs like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
- [Connection.execution_options.compiled_cache](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.compiled_cache) -
  indicates a dictionary that will serve as the
  [SQL compilation cache](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)
  for a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), as
  well as for ORM methods like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
  Can be passed as `None` to disable caching for statements.
  This option is not accepted by
  [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) as it is inadvisable to
  carry along a compilation cache within a statement object.
- [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map)
  - a mapping of schema names used by the
  [Schema Translate Map](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating) feature, accepted
  by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
  [Executable](#sqlalchemy.sql.expression.Executable), as well as by ORM constructs
  like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).

See also

[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options)

[Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options)

[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options)

[ORM Execution Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-execution-options) - documentation on all
ORM-specific execution options

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)exists() → [Exists](#sqlalchemy.sql.expression.Exists)

*inherited from the* [SelectBase.exists()](#sqlalchemy.sql.expression.SelectBase.exists) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return an [Exists](#sqlalchemy.sql.expression.Exists) representation of this selectable,
which can be used as a column expression.

The returned object is an instance of [Exists](#sqlalchemy.sql.expression.Exists).

See also

[exists()](#sqlalchemy.sql.expression.exists)

[EXISTS subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-exists) - in the [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) tutorial.

Added in version 1.4.

     property exported_columns: ReadOnlyColumnCollection[str, [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]]

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [Selectable](#sqlalchemy.sql.expression.Selectable), not including
[TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) constructs.

The “exported” columns for a [SelectBase](#sqlalchemy.sql.expression.SelectBase)
object are synonymous
with the [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) collection.

Added in version 1.4.

See also

[Select.exported_columns](#sqlalchemy.sql.expression.Select.exported_columns)

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)

[FromClause.exported_columns](#sqlalchemy.sql.expression.FromClause.exported_columns)

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)fetch(*count:_LimitOffsetType*, *with_ties:bool=False*, *percent:bool=False*, ***dialect_kw:Any*) → Self

*inherited from the* [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given FETCH FIRST criterion
applied.

This is a numeric value which usually renders as `FETCH {FIRST | NEXT}
[ count ] {ROW | ROWS} {ONLY | WITH TIES}` expression in the resulting
select. This functionality is is currently implemented for Oracle
Database, PostgreSQL, MSSQL.

Use [GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset) to specify the offset.

Note

The [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch) method will replace
any clause applied with [GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit).

Added in version 1.4.

   Parameters:

- **count** – an integer COUNT parameter, or a SQL expression
  that provides an integer result. When `percent=True` this will
  represent the percentage of rows to return, not the absolute value.
  Pass `None` to reset it.
- **with_ties** – When `True`, the WITH TIES option is used
  to return any additional rows that tie for the last place in the
  result set according to the `ORDER BY` clause. The
  `ORDER BY` may be mandatory in this case. Defaults to `False`
- **percent** – When `True`, `count` represents the percentage
  of the total number of selected rows to return. Defaults to `False`
- ****dialect_kw** –
  Additional dialect-specific keyword arguments
  may be accepted by dialects.
  Added in version 2.0.41.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)get_execution_options() → _ExecuteOptions

*inherited from the* [Executable.get_execution_options()](#sqlalchemy.sql.expression.Executable.get_execution_options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

See also

[Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options)

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)get_label_style() → [SelectLabelStyle](#sqlalchemy.sql.expression.SelectLabelStyle)

*inherited from the* [GenerativeSelect.get_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.get_label_style) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Retrieve the current label style.

Added in version 1.4.

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)group_by(*_GenerativeSelect__first:Literal[None,_NoArg.NO_ARG]|_ColumnExpressionOrStrLabelArgument[Any]=_NoArg.NO_ARG*, **clauses:_ColumnExpressionOrStrLabelArgument[Any]*) → Self

*inherited from the* [GenerativeSelect.group_by()](#sqlalchemy.sql.expression.GenerativeSelect.group_by) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given list of GROUP BY
criterion applied.

All existing GROUP BY settings can be suppressed by passing `None`.

e.g.:

```
stmt = select(table.c.name, func.max(table.c.stat)).group_by(table.c.name)
```

   Parameters:

***clauses** –

a series of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
constructs which will be used to generate an GROUP BY clause.

Alternatively, an individual entry may also be the string name of a
label located elsewhere in the columns clause of the statement which
will be matched and rendered in a backend-specific way based on
context; see [Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) for background on string
label matching in ORDER BY and GROUP BY expressions.

See also

[Aggregate functions with GROUP BY / HAVING](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-group-by-w-aggregates) - in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     attribute [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)inherit_cache = None

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

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)is_derived_from(*fromclause:FromClause|None*) → bool

Return `True` if this [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows) is
‘derived’ from the given [FromClause](#sqlalchemy.sql.expression.FromClause).

An example would be an Alias of a Table is derived from that Table.

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

    method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)label(*name:str|None*) → [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label)[Any]

*inherited from the* [SelectBase.label()](#sqlalchemy.sql.expression.SelectBase.label) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a ‘scalar’ representation of this selectable, embedded as a
subquery with a label.

See also

[SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)lateral(*name:str|None=None*) → LateralFromClause

*inherited from the* [SelectBase.lateral()](#sqlalchemy.sql.expression.SelectBase.lateral) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a LATERAL alias of this [Selectable](#sqlalchemy.sql.expression.Selectable).

The return value is the [Lateral](#sqlalchemy.sql.expression.Lateral) construct also
provided by the top-level [lateral()](#sqlalchemy.sql.expression.lateral) function.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)limit(*limit:_LimitOffsetType*) → Self

*inherited from the* [GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given LIMIT criterion
applied.

This is a numerical value which usually renders as a `LIMIT`
expression in the resulting select.  Backends that don’t
support `LIMIT` will attempt to provide similar
functionality.

Note

The [GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit) method will replace
any clause applied with [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch).

   Parameters:

**limit** – an integer LIMIT parameter, or a SQL expression
that provides an integer result. Pass `None` to reset it.

See also

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

     attribute [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)name_cte_columns = False

*inherited from the* [HasCTE.name_cte_columns](#sqlalchemy.sql.expression.HasCTE.name_cte_columns) *attribute of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause.

Added in version 2.0.42.

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)offset(*offset:_LimitOffsetType*) → Self

*inherited from the* [GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given OFFSET criterion
applied.

This is a numeric value which usually renders as an `OFFSET`
expression in the resulting select.  Backends that don’t
support `OFFSET` will attempt to provide similar
functionality.

  Parameters:

**offset** – an integer OFFSET parameter, or a SQL expression
that provides an integer result. Pass `None` to reset it.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)options(**options:ExecutableOption*) → Self

*inherited from the* [Executable.options()](#sqlalchemy.sql.expression.Executable.options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Apply options to this statement.

In the general sense, options are any kind of Python object
that can be interpreted by the SQL compiler for the statement.
These options can be consumed by specific dialects or specific kinds
of compilers.

The most commonly known kind of option are the ORM level options
that apply “eager load” and other loading behaviors to an ORM
query.   However, options can theoretically be used for many other
purposes.

For background on specific kinds of options for specific kinds of
statements, refer to the documentation for those option objects.

Changed in version 1.4: - added [Executable.options()](#sqlalchemy.sql.expression.Executable.options) to
Core statement objects towards the goal of allowing unified
Core / ORM querying capabilities.

See also

[Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#loading-columns) - refers to options specific to the usage
of ORM queries

[Relationship Loading with Loader Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#relationship-loader-options) - refers to options specific
to the usage of ORM queries

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)order_by(*_GenerativeSelect__first:Literal[None,_NoArg.NO_ARG]|_ColumnExpressionOrStrLabelArgument[Any]=_NoArg.NO_ARG*, **clauses:_ColumnExpressionOrStrLabelArgument[Any]*) → Self

*inherited from the* [GenerativeSelect.order_by()](#sqlalchemy.sql.expression.GenerativeSelect.order_by) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given list of ORDER BY
criteria applied.

e.g.:

```
stmt = select(table).order_by(table.c.id, table.c.name)
```

Calling this method multiple times is equivalent to calling it once
with all the clauses concatenated. All existing ORDER BY criteria may
be cancelled by passing `None` by itself.  New ORDER BY criteria may
then be added by invoking [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) again, e.g.:

```
# will erase all ORDER BY and ORDER BY new_col alone
stmt = stmt.order_by(None).order_by(new_col)
```

   Parameters:

***clauses** –

a series of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
constructs which will be used to generate an ORDER BY clause.

Alternatively, an individual entry may also be the string name of a
label located elsewhere in the columns clause of the statement which
will be matched and rendered in a backend-specific way based on
context; see [Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) for background on string
label matching in ORDER BY and GROUP BY expressions.

See also

[ORDER BY](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)replace_selectable(*old:FromClause*, *alias:Alias*) → Self

*inherited from the* [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Replace all occurrences of [FromClause](#sqlalchemy.sql.expression.FromClause)
‘old’ with the given [Alias](#sqlalchemy.sql.expression.Alias)
object, returning a copy of this [FromClause](#sqlalchemy.sql.expression.FromClause).

Deprecated since version 1.4: The [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) method is deprecated, and will be removed in a future release.  Similar functionality is available via the sqlalchemy.sql.visitors module.

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)scalar_subquery() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

*inherited from the* [SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a ‘scalar’ representation of this selectable, which can be
used as a column expression.

The returned object is an instance of [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect).

Typically, a select statement which has only one column in its columns
clause is eligible to be used as a scalar expression.  The scalar
subquery can then be used in the WHERE clause or columns clause of
an enclosing SELECT.

Note that the scalar subquery differentiates from the FROM-level
subquery that can be produced using the
[SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
method.

See also

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery) - in the 2.0 tutorial

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)select(**arg:Any*, ***kw:Any*) → [Select](#sqlalchemy.sql.expression.Select)

*inherited from the* [SelectBase.select()](#sqlalchemy.sql.expression.SelectBase.select) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Deprecated since version 1.4: The [SelectBase.select()](#sqlalchemy.sql.expression.SelectBase.select) method is deprecated and will be removed in a future release; this method implicitly creates a subquery that should be explicit.  Please call [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) first in order to create a subquery, which then can be selected.

     attribute [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)selected_columns

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
representing the columns that
this SELECT statement or similar construct returns in its result set,
not including [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) constructs.

For a [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect), the
[CompoundSelect.selected_columns](#sqlalchemy.sql.expression.CompoundSelect.selected_columns)
attribute returns the selected
columns of the first SELECT statement contained within the series of
statements within the set operation.

See also

[Select.selected_columns](#sqlalchemy.sql.expression.Select.selected_columns)

Added in version 1.4.

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)self_group(*against:OperatorType|None=None*) → GroupedElement

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.CompoundSelect.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.CompoundSelect.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)set_label_style(*style:SelectLabelStyle*) → Self

Return a new selectable with the specified label style.

There are three “label styles” available,
[SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY),
[SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL), and
[SelectLabelStyle.LABEL_STYLE_NONE](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_NONE).   The default style is
[SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY).

In modern SQLAlchemy, there is not generally a need to change the
labeling style, as per-expression labels are more effectively used by
making use of the [ColumnElement.label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label) method. In past
versions, `LABEL_STYLE_TABLENAME_PLUS_COL` was used to
disambiguate same-named columns from different tables, aliases, or
subqueries; the newer `LABEL_STYLE_DISAMBIGUATE_ONLY` now
applies labels only to names that conflict with an existing name so
that the impact of this labeling is minimal.

The rationale for disambiguation is mostly so that all column
expressions are available from a given [FromClause.c](#sqlalchemy.sql.expression.FromClause.c)
collection when a subquery is created.

Added in version 1.4: - the
[GenerativeSelect.set_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.set_label_style) method replaces the
previous combination of `.apply_labels()`, `.with_labels()` and
`use_labels=True` methods and/or parameters.

See also

`LABEL_STYLE_DISAMBIGUATE_ONLY`

`LABEL_STYLE_TABLENAME_PLUS_COL`

`LABEL_STYLE_NONE`

`LABEL_STYLE_DEFAULT`

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)slice(*start:int*, *stop:int*) → Self

*inherited from the* [GenerativeSelect.slice()](#sqlalchemy.sql.expression.GenerativeSelect.slice) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Apply LIMIT / OFFSET to this statement based on a slice.

The start and stop indices behave like the argument to Python’s
built-in `range()` function. This method provides an
alternative to using `LIMIT`/`OFFSET` to get a slice of the
query.

For example,

```
stmt = select(User).order_by(User.id).slice(1, 3)
```

renders as

```
SELECT users.id AS users_id,
       users.name AS users_name
FROM users ORDER BY users.id
LIMIT ? OFFSET ?
(2, 1)
```

Note

The [GenerativeSelect.slice()](#sqlalchemy.sql.expression.GenerativeSelect.slice) method will replace
any clause applied with [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch).

Added in version 1.4: Added the [GenerativeSelect.slice()](#sqlalchemy.sql.expression.GenerativeSelect.slice)
method generalized from the ORM.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)subquery(*name:str|None=None*) → [Subquery](#sqlalchemy.sql.expression.Subquery)

*inherited from the* [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a subquery of this [SelectBase](#sqlalchemy.sql.expression.SelectBase).

A subquery is from a SQL perspective a parenthesized, named
construct that can be placed in the FROM clause of another
SELECT statement.

Given a SELECT statement such as:

```
stmt = select(table.c.id, table.c.name)
```

The above statement might look like:

```
SELECT table.id, table.name FROM table
```

The subquery form by itself renders the same way, however when
embedded into the FROM clause of another SELECT statement, it becomes
a named sub-element:

```
subq = stmt.subquery()
new_stmt = select(subq)
```

The above renders as:

```
SELECT anon_1.id, anon_1.name
FROM (SELECT table.id, table.name FROM table) AS anon_1
```

Historically, [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
is equivalent to calling
the [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias)
method on a FROM object; however,
as a [SelectBase](#sqlalchemy.sql.expression.SelectBase)
object is not directly  FROM object,
the [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
method provides clearer semantics.

Added in version 1.4.

     method [sqlalchemy.sql.expression.CompoundSelect.](#sqlalchemy.sql.expression.CompoundSelect)with_for_update(***, *nowait:bool=False*, *read:bool=False*, *of:_ForUpdateOfArgument|None=None*, *skip_locked:bool=False*, *key_share:bool=False*) → Self

*inherited from the* [GenerativeSelect.with_for_update()](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Specify a `FOR UPDATE` clause for this
[GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect).

E.g.:

```
stmt = select(table).with_for_update(nowait=True)
```

On a database like PostgreSQL or Oracle Database, the above would
render a statement like:

```
SELECT table.a, table.b FROM table FOR UPDATE NOWAIT
```

on other backends, the `nowait` option is ignored and instead
would produce:

```
SELECT table.a, table.b FROM table FOR UPDATE
```

When called with no arguments, the statement will render with
the suffix `FOR UPDATE`.   Additional arguments can then be
provided which allow for common database-specific
variants.

  Parameters:

- **nowait** – boolean; will render `FOR UPDATE NOWAIT` on Oracle
  Database and PostgreSQL dialects.
- **read** – boolean; will render `LOCK IN SHARE MODE` on MySQL,
  `FOR SHARE` on PostgreSQL.  On PostgreSQL, when combined with
  `nowait`, will render `FOR SHARE NOWAIT`.
- **of** – SQL expression or list of SQL expression elements,
  (typically [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects or a compatible expression,
  for some backends may also be a table expression) which will render
  into a `FOR UPDATE OF` clause; supported by PostgreSQL, Oracle
  Database, some MySQL versions and possibly others. May render as a
  table or as a column depending on backend.
- **skip_locked** – boolean, will render `FOR UPDATE SKIP LOCKED` on
  Oracle Database and PostgreSQL dialects or `FOR SHARE SKIP LOCKED`
  if `read=True` is also specified.
- **key_share** – boolean, will render `FOR NO KEY UPDATE`,
  or if combined with `read=True` will render `FOR KEY SHARE`,
  on the PostgreSQL dialect.

       class sqlalchemy.sql.expression.CTE

*inherits from* `sqlalchemy.sql.roles.DMLTableRole`, `sqlalchemy.sql.roles.IsCTERole`, `sqlalchemy.sql.expression.Generative`, [sqlalchemy.sql.expression.HasPrefixes](#sqlalchemy.sql.expression.HasPrefixes), [sqlalchemy.sql.expression.HasSuffixes](#sqlalchemy.sql.expression.HasSuffixes), [sqlalchemy.sql.expression.AliasedReturnsRows](#sqlalchemy.sql.expression.AliasedReturnsRows)

Represent a Common Table Expression.

The [CTE](#sqlalchemy.sql.expression.CTE) object is obtained using the
[SelectBase.cte()](#sqlalchemy.sql.expression.SelectBase.cte) method from any SELECT statement. A less often
available syntax also allows use of the [HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) method
present on [DML](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML) constructs such as [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert),
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and
[Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete).   See the [HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) method for
usage details on CTEs.

See also

[Subqueries and CTEs](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-subqueries-ctes) - in the 2.0 tutorial

[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) - examples of calling styles

| Member Name | Description |
| --- | --- |
| alias() | Return anAliasof thisCTE. |
| union() | Return a newCTEwith a SQLUNIONof the original CTE against the given selectables provided
as positional arguments. |
| union_all() | Return a newCTEwith a SQLUNIONALLof the original CTE against the given selectables provided
as positional arguments. |

   method [sqlalchemy.sql.expression.CTE.](#sqlalchemy.sql.expression.CTE)alias(*name:str|None=None*, *flat:bool=False*) → [CTE](#sqlalchemy.sql.expression.CTE)

Return an [Alias](#sqlalchemy.sql.expression.Alias) of this
[CTE](#sqlalchemy.sql.expression.CTE).

This method is a CTE-specific specialization of the
[FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias) method.

See also

[Using Aliases](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-using-aliases)

[alias()](#sqlalchemy.sql.expression.alias)

     method [sqlalchemy.sql.expression.CTE.](#sqlalchemy.sql.expression.CTE)union(**other:_SelectStatementForCompoundArgument[Any]*) → [CTE](#sqlalchemy.sql.expression.CTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE) with a SQL `UNION`
of the original CTE against the given selectables provided
as positional arguments.

  Parameters:

***other** –

one or more elements with which to create a
UNION.

Changed in version 1.4.28: multiple elements are now accepted.

See also

[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) - examples of calling styles

     method [sqlalchemy.sql.expression.CTE.](#sqlalchemy.sql.expression.CTE)union_all(**other:_SelectStatementForCompoundArgument[Any]*) → [CTE](#sqlalchemy.sql.expression.CTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE) with a SQL `UNION ALL`
of the original CTE against the given selectables provided
as positional arguments.

  Parameters:

***other** –

one or more elements with which to create a
UNION.

Changed in version 1.4.28: multiple elements are now accepted.

See also

[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) - examples of calling styles

      class sqlalchemy.sql.expression.Executable

*inherits from* `sqlalchemy.sql.roles.StatementRole`

Mark a [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) as supporting execution.

[Executable](#sqlalchemy.sql.expression.Executable) is a superclass for all “statement” types
of objects, including [select()](#sqlalchemy.sql.expression.select), [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete), [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update),
[insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert), [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text).

| Member Name | Description |
| --- | --- |
| execution_options() | Set non-SQL options for the statement which take effect during
execution. |
| get_execution_options() | Get the non-SQL options which will take effect during execution. |
| options() | Apply options to this statement. |

   method [sqlalchemy.sql.expression.Executable.](#sqlalchemy.sql.expression.Executable)execution_options(***kw:Any*) → Self

Set non-SQL options for the statement which take effect during
execution.

Execution options can be set at many scopes, including per-statement,
per-connection, or per execution, using methods such as
[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) and parameters which
accept a dictionary of options such as
[Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options) and
[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options).

The primary characteristic of an execution option, as opposed to
other kinds of options such as ORM loader options, is that
**execution options never affect the compiled SQL of a query, only
things that affect how the SQL statement itself is invoked or how
results are fetched**.  That is, execution options are not part of
what’s accommodated by SQL compilation nor are they considered part of
the cached state of a statement.

The [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) method is
[generative](https://docs.sqlalchemy.org/en/20/glossary.html#term-generative), as
is the case for the method as applied to the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
and [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects, which means when the method is called,
a copy of the object is returned, which applies the given parameters to
that new copy, but leaves the original unchanged:

```
statement = select(table.c.x, table.c.y)
new_statement = statement.execution_options(my_option=True)
```

An exception to this behavior is the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
object, where the [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) method
is explicitly **not** generative.

The kinds of options that may be passed to
[Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) and other related methods and
parameter dictionaries include parameters that are explicitly consumed
by SQLAlchemy Core or ORM, as well as arbitrary keyword arguments not
defined by SQLAlchemy, which means the methods and/or parameter
dictionaries may be used for user-defined parameters that interact with
custom code, which may access the parameters using methods such as
[Executable.get_execution_options()](#sqlalchemy.sql.expression.Executable.get_execution_options) and
[Connection.get_execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_execution_options), or within selected
event hooks using a dedicated `execution_options` event parameter
such as
[ConnectionEvents.before_execute.execution_options](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_execute.params.execution_options)
or [ORMExecuteState.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.execution_options), e.g.:

```
from sqlalchemy import event

@event.listens_for(some_engine, "before_execute")
def _process_opt(conn, statement, multiparams, params, execution_options):
    "run a SQL function before invoking a statement"

    if execution_options.get("do_special_thing", False):
        conn.exec_driver_sql("run_special_function()")
```

Within the scope of options that are explicitly recognized by
SQLAlchemy, most apply to specific classes of objects and not others.
The most common execution options include:

- [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
  sets the isolation level for a connection or a class of connections
  via an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).  This option is accepted only
  by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).
- [Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results) -
  indicates results should be fetched using a server side cursor;
  this option is accepted by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), by the
  [Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options) parameter
  on [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), and additionally by
  [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) on a SQL statement object,
  as well as by ORM constructs like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
- [Connection.execution_options.compiled_cache](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.compiled_cache) -
  indicates a dictionary that will serve as the
  [SQL compilation cache](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)
  for a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), as
  well as for ORM methods like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
  Can be passed as `None` to disable caching for statements.
  This option is not accepted by
  [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) as it is inadvisable to
  carry along a compilation cache within a statement object.
- [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map)
  - a mapping of schema names used by the
  [Schema Translate Map](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating) feature, accepted
  by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
  [Executable](#sqlalchemy.sql.expression.Executable), as well as by ORM constructs
  like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).

See also

[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options)

[Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options)

[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options)

[ORM Execution Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-execution-options) - documentation on all
ORM-specific execution options

     method [sqlalchemy.sql.expression.Executable.](#sqlalchemy.sql.expression.Executable)get_execution_options() → _ExecuteOptions

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

See also

[Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options)

     method [sqlalchemy.sql.expression.Executable.](#sqlalchemy.sql.expression.Executable)options(**options:ExecutableOption*) → Self

Apply options to this statement.

In the general sense, options are any kind of Python object
that can be interpreted by the SQL compiler for the statement.
These options can be consumed by specific dialects or specific kinds
of compilers.

The most commonly known kind of option are the ORM level options
that apply “eager load” and other loading behaviors to an ORM
query.   However, options can theoretically be used for many other
purposes.

For background on specific kinds of options for specific kinds of
statements, refer to the documentation for those option objects.

Changed in version 1.4: - added [Executable.options()](#sqlalchemy.sql.expression.Executable.options) to
Core statement objects towards the goal of allowing unified
Core / ORM querying capabilities.

See also

[Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#loading-columns) - refers to options specific to the usage
of ORM queries

[Relationship Loading with Loader Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#relationship-loader-options) - refers to options specific
to the usage of ORM queries

      class sqlalchemy.sql.expression.Exists

*inherits from* [sqlalchemy.sql.expression.UnaryExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.UnaryExpression)

Represent an `EXISTS` clause.

See [exists()](#sqlalchemy.sql.expression.exists) for a description of usage.

An `EXISTS` clause can also be constructed from a [select()](#sqlalchemy.sql.expression.select)
instance by calling [SelectBase.exists()](#sqlalchemy.sql.expression.SelectBase.exists).

| Member Name | Description |
| --- | --- |
| correlate() | Apply correlation to the subquery noted by thisExists. |
| correlate_except() | Apply correlation to the subquery noted by thisExists. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| select() | Return a SELECT of thisExists. |
| select_from() | Return a newExistsconstruct,
applying the given
expression to theSelect.select_from()method of the select
statement contained. |
| where() | Return a newexists()construct with the
given expression added to
its WHERE clause, joined to the existing clause via AND, if any. |

   method [sqlalchemy.sql.expression.Exists.](#sqlalchemy.sql.expression.Exists)correlate(**fromclauses:Literal[None,False]|_FromClauseArgument*) → Self

Apply correlation to the subquery noted by this
[Exists](#sqlalchemy.sql.expression.Exists).

See also

[ScalarSelect.correlate()](#sqlalchemy.sql.expression.ScalarSelect.correlate)

     method [sqlalchemy.sql.expression.Exists.](#sqlalchemy.sql.expression.Exists)correlate_except(**fromclauses:Literal[None,False]|_FromClauseArgument*) → Self

Apply correlation to the subquery noted by this
[Exists](#sqlalchemy.sql.expression.Exists).

See also

[ScalarSelect.correlate_except()](#sqlalchemy.sql.expression.ScalarSelect.correlate_except)

     attribute [sqlalchemy.sql.expression.Exists.](#sqlalchemy.sql.expression.Exists)inherit_cache = True

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

     method [sqlalchemy.sql.expression.Exists.](#sqlalchemy.sql.expression.Exists)select() → [Select](#sqlalchemy.sql.expression.Select)

Return a SELECT of this [Exists](#sqlalchemy.sql.expression.Exists).

e.g.:

```
stmt = exists(some_table.c.id).where(some_table.c.id == 5).select()
```

This will produce a statement resembling:

```
SELECT EXISTS (SELECT id FROM some_table WHERE some_table = :param) AS anon_1
```

See also

[select()](#sqlalchemy.sql.expression.select) - general purpose
method which allows for arbitrary column lists.

     method [sqlalchemy.sql.expression.Exists.](#sqlalchemy.sql.expression.Exists)select_from(**froms:_FromClauseArgument*) → Self

Return a new [Exists](#sqlalchemy.sql.expression.Exists) construct,
applying the given
expression to the [Select.select_from()](#sqlalchemy.sql.expression.Select.select_from)
method of the select
statement contained.

Note

it is typically preferable to build a [Select](#sqlalchemy.sql.expression.Select)
statement first, including the desired WHERE clause, then use the
[SelectBase.exists()](#sqlalchemy.sql.expression.SelectBase.exists) method to produce an
[Exists](#sqlalchemy.sql.expression.Exists) object at once.

     method [sqlalchemy.sql.expression.Exists.](#sqlalchemy.sql.expression.Exists)where(**clause:_ColumnExpressionArgument[bool]*) → Self

Return a new [exists()](#sqlalchemy.sql.expression.exists) construct with the
given expression added to
its WHERE clause, joined to the existing clause via AND, if any.

Note

it is typically preferable to build a [Select](#sqlalchemy.sql.expression.Select)
statement first, including the desired WHERE clause, then use the
[SelectBase.exists()](#sqlalchemy.sql.expression.SelectBase.exists) method to produce an
[Exists](#sqlalchemy.sql.expression.Exists) object at once.

      class sqlalchemy.sql.expression.FromClause

*inherits from* `sqlalchemy.sql.roles.AnonymizedFromClauseRole`, [sqlalchemy.sql.expression.Selectable](#sqlalchemy.sql.expression.Selectable)

Represent an element that can be used within the `FROM`
clause of a `SELECT` statement.

The most common forms of [FromClause](#sqlalchemy.sql.expression.FromClause) are the
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and the [select()](#sqlalchemy.sql.expression.select) constructs.  Key
features common to all [FromClause](#sqlalchemy.sql.expression.FromClause) objects include:

- a [c](#sqlalchemy.sql.expression.FromClause.c) collection, which provides per-name access to a collection
  of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects.
- a [primary_key](#sqlalchemy.sql.expression.FromClause.primary_key) attribute, which is a collection of all those
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  objects that indicate the `primary_key` flag.
- Methods to generate various derivations of a “from” clause, including
  [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias),
  [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join),
  [FromClause.select()](#sqlalchemy.sql.expression.FromClause.select).

| Member Name | Description |
| --- | --- |
| alias() | Return an alias of thisFromClause. |
| c | A synonym forFromClause.columns |
| columns | A named-based collection ofColumnElementobjects maintained by thisFromClause. |
| description | A brief description of thisFromClause. |
| entity_namespace | Return a namespace used for name-based access in SQL expressions. |
| exported_columns | AColumnCollectionthat represents the “exported”
columns of thisSelectable. |
| foreign_keys | Return the collection ofForeignKeymarker objects
which this FromClause references. |
| is_derived_from() | ReturnTrueif thisFromClauseis
‘derived’ from the givenFromClause. |
| join() | Return aJoinfrom thisFromClauseto anotherFromClause. |
| outerjoin() | Return aJoinfrom thisFromClauseto anotherFromClause, with the “isouter” flag set to
True. |
| primary_key | Return the iterable collection ofColumnobjects
which comprise the primary key of this_selectable.FromClause. |
| schema | Define the ‘schema’ attribute for thisFromClause. |
| select() | Return a SELECT of thisFromClause. |
| tablesample() | Return a TABLESAMPLE alias of thisFromClause. |

   method [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)alias(*name:str|None=None*, *flat:bool=False*) → NamedFromClause

Return an alias of this [FromClause](#sqlalchemy.sql.expression.FromClause).

E.g.:

```
a2 = some_table.alias("a2")
```

The above code creates an [Alias](#sqlalchemy.sql.expression.Alias)
object which can be used
as a FROM clause in any SELECT statement.

See also

[Using Aliases](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-using-aliases)

[alias()](#sqlalchemy.sql.expression.alias)

     attribute [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)c

A synonym for [FromClause.columns](#sqlalchemy.sql.expression.FromClause.columns)

  Returns:

a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)

      attribute [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)columns

A named-based collection of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
objects maintained by this [FromClause](#sqlalchemy.sql.expression.FromClause).

The [columns](#sqlalchemy.sql.expression.FromClause.columns), or [c](#sqlalchemy.sql.expression.FromClause.c) collection, is the gateway
to the construction of SQL expressions using table-bound or
other selectable-bound columns:

```
select(mytable).where(mytable.c.somecolumn == 5)
```

   Returns:

a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) object.

      attribute [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)description

A brief description of this [FromClause](#sqlalchemy.sql.expression.FromClause).

Used primarily for error message formatting.

    attribute [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)entity_namespace

Return a namespace used for name-based access in SQL expressions.

This is the namespace that is used to resolve “filter_by()” type
expressions, such as:

```
stmt.filter_by(address="some address")
```

It defaults to the `.c` collection, however internally it can
be overridden using the “entity_namespace” annotation to deliver
alternative results.

    attribute [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)exported_columns

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [Selectable](#sqlalchemy.sql.expression.Selectable).

The “exported” columns for a [FromClause](#sqlalchemy.sql.expression.FromClause)
object are synonymous
with the [FromClause.columns](#sqlalchemy.sql.expression.FromClause.columns) collection.

Added in version 1.4.

See also

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)

[SelectBase.exported_columns](#sqlalchemy.sql.expression.SelectBase.exported_columns)

     attribute [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)foreign_keys

Return the collection of [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) marker objects
which this FromClause references.

Each [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) is a member of a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)-wide
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).

See also

[Table.foreign_key_constraints](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.foreign_key_constraints)

     method [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)is_derived_from(*fromclause:FromClause|None*) → bool

Return `True` if this [FromClause](#sqlalchemy.sql.expression.FromClause) is
‘derived’ from the given `FromClause`.

An example would be an Alias of a Table is derived from that Table.

    method [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)join(*right:_FromClauseArgument*, *onclause:_ColumnExpressionArgument[bool]|None=None*, *isouter:bool=False*, *full:bool=False*) → [Join](#sqlalchemy.sql.expression.Join)

Return a [Join](#sqlalchemy.sql.expression.Join) from this
[FromClause](#sqlalchemy.sql.expression.FromClause)
to another [FromClause](#sqlalchemy.sql.expression.FromClause).

E.g.:

```
from sqlalchemy import join

j = user_table.join(
    address_table, user_table.c.id == address_table.c.user_id
)
stmt = select(user_table).select_from(j)
```

would emit SQL along the lines of:

```
SELECT user.id, user.name FROM user
JOIN address ON user.id = address.user_id
```

   Parameters:

- **right** – the right side of the join; this is any
  [FromClause](#sqlalchemy.sql.expression.FromClause) object such as a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, and
  may also be a selectable-compatible object such as an ORM-mapped
  class.
- **onclause** – a SQL expression representing the ON clause of the
  join.  If left at `None`, [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)
  will attempt to
  join the two tables based on a foreign key relationship.
- **isouter** – if True, render a LEFT OUTER JOIN, instead of JOIN.
- **full** – if True, render a FULL OUTER JOIN, instead of LEFT OUTER
  JOIN.  Implies [FromClause.join.isouter](#sqlalchemy.sql.expression.FromClause.join.params.isouter).

See also

[join()](#sqlalchemy.sql.expression.join) - standalone function

[Join](#sqlalchemy.sql.expression.Join) - the type of object produced

     method [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)outerjoin(*right:_FromClauseArgument*, *onclause:_ColumnExpressionArgument[bool]|None=None*, *full:bool=False*) → [Join](#sqlalchemy.sql.expression.Join)

Return a [Join](#sqlalchemy.sql.expression.Join) from this
[FromClause](#sqlalchemy.sql.expression.FromClause)
to another [FromClause](#sqlalchemy.sql.expression.FromClause), with the “isouter” flag set to
True.

E.g.:

```
from sqlalchemy import outerjoin

j = user_table.outerjoin(
    address_table, user_table.c.id == address_table.c.user_id
)
```

The above is equivalent to:

```
j = user_table.join(
    address_table, user_table.c.id == address_table.c.user_id, isouter=True
)
```

   Parameters:

- **right** – the right side of the join; this is any
  [FromClause](#sqlalchemy.sql.expression.FromClause) object such as a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, and
  may also be a selectable-compatible object such as an ORM-mapped
  class.
- **onclause** – a SQL expression representing the ON clause of the
  join.  If left at `None`, [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)
  will attempt to
  join the two tables based on a foreign key relationship.
- **full** – if True, render a FULL OUTER JOIN, instead of
  LEFT OUTER JOIN.

See also

[FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)

[Join](#sqlalchemy.sql.expression.Join)

     attribute [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)primary_key

Return the iterable collection of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
which comprise the primary key of this `_selectable.FromClause`.

For a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, this collection is represented
by the [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) which itself is an
iterable collection of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects.

    attribute [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)schema: str | None = None

Define the ‘schema’ attribute for this [FromClause](#sqlalchemy.sql.expression.FromClause).

This is typically `None` for most objects except that of
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), where it is taken as the value of the
[Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) argument.

    method [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)select() → [Select](#sqlalchemy.sql.expression.Select)

Return a SELECT of this [FromClause](#sqlalchemy.sql.expression.FromClause).

e.g.:

```
stmt = some_table.select().where(some_table.c.id == 5)
```

See also

[select()](#sqlalchemy.sql.expression.select) - general purpose
method which allows for arbitrary column lists.

     method [sqlalchemy.sql.expression.FromClause.](#sqlalchemy.sql.expression.FromClause)tablesample(*sampling:float|Function[Any]*, *name:str|None=None*, *seed:roles.ExpressionElementRole[Any]|None=None*) → [TableSample](#sqlalchemy.sql.expression.TableSample)

Return a TABLESAMPLE alias of this [FromClause](#sqlalchemy.sql.expression.FromClause).

The return value is the [TableSample](#sqlalchemy.sql.expression.TableSample)
construct also
provided by the top-level [tablesample()](#sqlalchemy.sql.expression.tablesample) function.

See also

[tablesample()](#sqlalchemy.sql.expression.tablesample) - usage guidelines and parameters

      class sqlalchemy.sql.expression.GenerativeSelect

*inherits from* `sqlalchemy.sql.expression.DialectKWArgs`, [sqlalchemy.sql.expression.SelectBase](#sqlalchemy.sql.expression.SelectBase), `sqlalchemy.sql.expression.Generative`

Base class for SELECT statements where additional elements can be
added.

This serves as the base for [Select](#sqlalchemy.sql.expression.Select) and
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)
where elements such as ORDER BY, GROUP BY can be added and column
rendering can be controlled.  Compare to
[TextualSelect](#sqlalchemy.sql.expression.TextualSelect), which,
while it subclasses [SelectBase](#sqlalchemy.sql.expression.SelectBase)
and is also a SELECT construct,
represents a fixed textual string which cannot be altered at this level,
only wrapped as a subquery.

| Member Name | Description |
| --- | --- |
| fetch() | Return a new selectable with the given FETCH FIRST criterion
applied. |
| get_label_style() | Retrieve the current label style. |
| group_by() | Return a new selectable with the given list of GROUP BY
criterion applied. |
| limit() | Return a new selectable with the given LIMIT criterion
applied. |
| offset() | Return a new selectable with the given OFFSET criterion
applied. |
| order_by() | Return a new selectable with the given list of ORDER BY
criteria applied. |
| set_label_style() | Return a new selectable with the specified label style. |
| slice() | Apply LIMIT / OFFSET to this statement based on a slice. |
| with_for_update() | Specify aFORUPDATEclause for thisGenerativeSelect. |

   method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)fetch(*count:_LimitOffsetType*, *with_ties:bool=False*, *percent:bool=False*, ***dialect_kw:Any*) → Self

Return a new selectable with the given FETCH FIRST criterion
applied.

This is a numeric value which usually renders as `FETCH {FIRST | NEXT}
[ count ] {ROW | ROWS} {ONLY | WITH TIES}` expression in the resulting
select. This functionality is is currently implemented for Oracle
Database, PostgreSQL, MSSQL.

Use [GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset) to specify the offset.

Note

The [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch) method will replace
any clause applied with [GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit).

Added in version 1.4.

   Parameters:

- **count** – an integer COUNT parameter, or a SQL expression
  that provides an integer result. When `percent=True` this will
  represent the percentage of rows to return, not the absolute value.
  Pass `None` to reset it.
- **with_ties** – When `True`, the WITH TIES option is used
  to return any additional rows that tie for the last place in the
  result set according to the `ORDER BY` clause. The
  `ORDER BY` may be mandatory in this case. Defaults to `False`
- **percent** – When `True`, `count` represents the percentage
  of the total number of selected rows to return. Defaults to `False`
- ****dialect_kw** –
  Additional dialect-specific keyword arguments
  may be accepted by dialects.
  Added in version 2.0.41.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

     method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)get_label_style() → [SelectLabelStyle](#sqlalchemy.sql.expression.SelectLabelStyle)

Retrieve the current label style.

Added in version 1.4.

     method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)group_by(*_GenerativeSelect__first:Literal[None,_NoArg.NO_ARG]|_ColumnExpressionOrStrLabelArgument[Any]=_NoArg.NO_ARG*, **clauses:_ColumnExpressionOrStrLabelArgument[Any]*) → Self

Return a new selectable with the given list of GROUP BY
criterion applied.

All existing GROUP BY settings can be suppressed by passing `None`.

e.g.:

```
stmt = select(table.c.name, func.max(table.c.stat)).group_by(table.c.name)
```

   Parameters:

***clauses** –

a series of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
constructs which will be used to generate an GROUP BY clause.

Alternatively, an individual entry may also be the string name of a
label located elsewhere in the columns clause of the statement which
will be matched and rendered in a backend-specific way based on
context; see [Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) for background on string
label matching in ORDER BY and GROUP BY expressions.

See also

[Aggregate functions with GROUP BY / HAVING](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-group-by-w-aggregates) - in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)limit(*limit:_LimitOffsetType*) → Self

Return a new selectable with the given LIMIT criterion
applied.

This is a numerical value which usually renders as a `LIMIT`
expression in the resulting select.  Backends that don’t
support `LIMIT` will attempt to provide similar
functionality.

Note

The [GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit) method will replace
any clause applied with [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch).

   Parameters:

**limit** – an integer LIMIT parameter, or a SQL expression
that provides an integer result. Pass `None` to reset it.

See also

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

     method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)offset(*offset:_LimitOffsetType*) → Self

Return a new selectable with the given OFFSET criterion
applied.

This is a numeric value which usually renders as an `OFFSET`
expression in the resulting select.  Backends that don’t
support `OFFSET` will attempt to provide similar
functionality.

  Parameters:

**offset** – an integer OFFSET parameter, or a SQL expression
that provides an integer result. Pass `None` to reset it.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

     method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)order_by(*_GenerativeSelect__first:Literal[None,_NoArg.NO_ARG]|_ColumnExpressionOrStrLabelArgument[Any]=_NoArg.NO_ARG*, **clauses:_ColumnExpressionOrStrLabelArgument[Any]*) → Self

Return a new selectable with the given list of ORDER BY
criteria applied.

e.g.:

```
stmt = select(table).order_by(table.c.id, table.c.name)
```

Calling this method multiple times is equivalent to calling it once
with all the clauses concatenated. All existing ORDER BY criteria may
be cancelled by passing `None` by itself.  New ORDER BY criteria may
then be added by invoking [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) again, e.g.:

```
# will erase all ORDER BY and ORDER BY new_col alone
stmt = stmt.order_by(None).order_by(new_col)
```

   Parameters:

***clauses** –

a series of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
constructs which will be used to generate an ORDER BY clause.

Alternatively, an individual entry may also be the string name of a
label located elsewhere in the columns clause of the statement which
will be matched and rendered in a backend-specific way based on
context; see [Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) for background on string
label matching in ORDER BY and GROUP BY expressions.

See also

[ORDER BY](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)set_label_style(*style:SelectLabelStyle*) → Self

Return a new selectable with the specified label style.

There are three “label styles” available,
[SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY),
[SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL), and
[SelectLabelStyle.LABEL_STYLE_NONE](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_NONE).   The default style is
[SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY).

In modern SQLAlchemy, there is not generally a need to change the
labeling style, as per-expression labels are more effectively used by
making use of the [ColumnElement.label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label) method. In past
versions, `LABEL_STYLE_TABLENAME_PLUS_COL` was used to
disambiguate same-named columns from different tables, aliases, or
subqueries; the newer `LABEL_STYLE_DISAMBIGUATE_ONLY` now
applies labels only to names that conflict with an existing name so
that the impact of this labeling is minimal.

The rationale for disambiguation is mostly so that all column
expressions are available from a given [FromClause.c](#sqlalchemy.sql.expression.FromClause.c)
collection when a subquery is created.

Added in version 1.4: - the
[GenerativeSelect.set_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.set_label_style) method replaces the
previous combination of `.apply_labels()`, `.with_labels()` and
`use_labels=True` methods and/or parameters.

See also

`LABEL_STYLE_DISAMBIGUATE_ONLY`

`LABEL_STYLE_TABLENAME_PLUS_COL`

`LABEL_STYLE_NONE`

`LABEL_STYLE_DEFAULT`

     method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)slice(*start:int*, *stop:int*) → Self

Apply LIMIT / OFFSET to this statement based on a slice.

The start and stop indices behave like the argument to Python’s
built-in `range()` function. This method provides an
alternative to using `LIMIT`/`OFFSET` to get a slice of the
query.

For example,

```
stmt = select(User).order_by(User.id).slice(1, 3)
```

renders as

```
SELECT users.id AS users_id,
       users.name AS users_name
FROM users ORDER BY users.id
LIMIT ? OFFSET ?
(2, 1)
```

Note

The [GenerativeSelect.slice()](#sqlalchemy.sql.expression.GenerativeSelect.slice) method will replace
any clause applied with [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch).

Added in version 1.4: Added the [GenerativeSelect.slice()](#sqlalchemy.sql.expression.GenerativeSelect.slice)
method generalized from the ORM.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

     method [sqlalchemy.sql.expression.GenerativeSelect.](#sqlalchemy.sql.expression.GenerativeSelect)with_for_update(***, *nowait:bool=False*, *read:bool=False*, *of:_ForUpdateOfArgument|None=None*, *skip_locked:bool=False*, *key_share:bool=False*) → Self

Specify a `FOR UPDATE` clause for this
[GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect).

E.g.:

```
stmt = select(table).with_for_update(nowait=True)
```

On a database like PostgreSQL or Oracle Database, the above would
render a statement like:

```
SELECT table.a, table.b FROM table FOR UPDATE NOWAIT
```

on other backends, the `nowait` option is ignored and instead
would produce:

```
SELECT table.a, table.b FROM table FOR UPDATE
```

When called with no arguments, the statement will render with
the suffix `FOR UPDATE`.   Additional arguments can then be
provided which allow for common database-specific
variants.

  Parameters:

- **nowait** – boolean; will render `FOR UPDATE NOWAIT` on Oracle
  Database and PostgreSQL dialects.
- **read** – boolean; will render `LOCK IN SHARE MODE` on MySQL,
  `FOR SHARE` on PostgreSQL.  On PostgreSQL, when combined with
  `nowait`, will render `FOR SHARE NOWAIT`.
- **of** – SQL expression or list of SQL expression elements,
  (typically [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects or a compatible expression,
  for some backends may also be a table expression) which will render
  into a `FOR UPDATE OF` clause; supported by PostgreSQL, Oracle
  Database, some MySQL versions and possibly others. May render as a
  table or as a column depending on backend.
- **skip_locked** – boolean, will render `FOR UPDATE SKIP LOCKED` on
  Oracle Database and PostgreSQL dialects or `FOR SHARE SKIP LOCKED`
  if `read=True` is also specified.
- **key_share** – boolean, will render `FOR NO KEY UPDATE`,
  or if combined with `read=True` will render `FOR KEY SHARE`,
  on the PostgreSQL dialect.

       class sqlalchemy.sql.expression.HasCTE

*inherits from* `sqlalchemy.sql.roles.HasCTERole`, `sqlalchemy.sql.expression.SelectsRows`

Mixin that declares a class to include CTE support.

| Member Name | Description |
| --- | --- |
| add_cte() | Add one or moreCTEconstructs to this statement. |
| cte() | Return a newCTE,
or Common Table Expression instance. |
| name_cte_columns | indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause. |

   method [sqlalchemy.sql.expression.HasCTE.](#sqlalchemy.sql.expression.HasCTE)add_cte(**ctes:CTE*, *nest_here:bool=False*) → Self

Add one or more [CTE](#sqlalchemy.sql.expression.CTE) constructs to this statement.

This method will associate the given [CTE](#sqlalchemy.sql.expression.CTE) constructs with
the parent statement such that they will each be unconditionally
rendered in the WITH clause of the final statement, even if not
referenced elsewhere within the statement or any sub-selects.

The optional [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here) parameter when set
to True will have the effect that each given [CTE](#sqlalchemy.sql.expression.CTE) will
render in a WITH clause rendered directly along with this statement,
rather than being moved to the top of the ultimate rendered statement,
even if this statement is rendered as a subquery within a larger
statement.

This method has two general uses. One is to embed CTE statements that
serve some purpose without being referenced explicitly, such as the use
case of embedding a DML statement such as an INSERT or UPDATE as a CTE
inline with a primary statement that may draw from its results
indirectly.  The other is to provide control over the exact placement
of a particular series of CTE constructs that should remain rendered
directly in terms of a particular statement that may be nested in a
larger statement.

E.g.:

```
from sqlalchemy import table, column, select

t = table("t", column("c1"), column("c2"))

ins = t.insert().values({"c1": "x", "c2": "y"}).cte()

stmt = select(t).add_cte(ins)
```

Would render:

```
WITH anon_1 AS (
    INSERT INTO t (c1, c2) VALUES (:param_1, :param_2)
)
SELECT t.c1, t.c2
FROM t
```

Above, the “anon_1” CTE is not referenced in the SELECT
statement, however still accomplishes the task of running an INSERT
statement.

Similarly in a DML-related context, using the PostgreSQL
[Insert](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert) construct to generate an “upsert”:

```
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import insert

t = table("t", column("c1"), column("c2"))

delete_statement_cte = t.delete().where(t.c.c1 < 1).cte("deletions")

insert_stmt = insert(t).values({"c1": 1, "c2": 2})
update_statement = insert_stmt.on_conflict_do_update(
    index_elements=[t.c.c1],
    set_={
        "c1": insert_stmt.excluded.c1,
        "c2": insert_stmt.excluded.c2,
    },
).add_cte(delete_statement_cte)

print(update_statement)
```

The above statement renders as:

```
WITH deletions AS (
    DELETE FROM t WHERE t.c1 < %(c1_1)s
)
INSERT INTO t (c1, c2) VALUES (%(c1)s, %(c2)s)
ON CONFLICT (c1) DO UPDATE SET c1 = excluded.c1, c2 = excluded.c2
```

Added in version 1.4.21.

   Parameters:

- ***ctes** –
  zero or more [CTE](#sqlalchemy.sql.expression.CTE) constructs.
  Changed in version 2.0: Multiple CTE instances are accepted
- **nest_here** –
  if True, the given CTE or CTEs will be rendered
  as though they specified the [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting) flag
  to `True` when they were added to this [HasCTE](#sqlalchemy.sql.expression.HasCTE).
  Assuming the given CTEs are not referenced in an outer-enclosing
  statement as well, the CTEs given should render at the level of
  this statement when this flag is given.
  Added in version 2.0.
  See also
  [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting)

      method [sqlalchemy.sql.expression.HasCTE.](#sqlalchemy.sql.expression.HasCTE)cte(*name:str|None=None*, *recursive:bool=False*, *nesting:bool=False*) → [CTE](#sqlalchemy.sql.expression.CTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE),
or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT
statements can draw upon secondary statements specified along
with the primary statement, using a clause called “WITH”.
Special semantics regarding UNION can also be employed to
allow “recursive” queries, where a SELECT statement can draw
upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT
and DELETE on some databases, both as a source of CTE rows
when combined with RETURNING, as well as a consumer of
CTE rows.

SQLAlchemy detects [CTE](#sqlalchemy.sql.expression.CTE) objects, which are treated
similarly to [Alias](#sqlalchemy.sql.expression.Alias) objects, as special elements
to be delivered to the FROM clause of the statement as well
as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and
“NOT MATERIALIZED”, the `CTE.prefix_with()`
method may be
used to establish these.

Changed in version 1.3.13: Added support for prefixes.
In particular - MATERIALIZED and NOT MATERIALIZED.

   Parameters:

- **name** – name given to the common table expression.  Like
  [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias), the name can be left as
  `None` in which case an anonymous symbol will be used at query
  compile time.
- **recursive** – if `True`, will render `WITH RECURSIVE`.
  A recursive common table expression is intended to be used in
  conjunction with UNION ALL in order to derive rows
  from those already selected.
- **nesting** –
  if `True`, will render the CTE locally to the
  statement in which it is referenced.   For more complex scenarios,
  the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method using the
  [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here)
  parameter may also be used to more carefully
  control the exact placement of a particular CTE.
  Added in version 1.4.24.
  See also
  [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte)

The following examples include two from PostgreSQL’s documentation at
[https://www.postgresql.org/docs/current/static/queries-with.html](https://www.postgresql.org/docs/current/static/queries-with.html),
as well as additional examples.

Example 1, non recursive:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("region", String),
    Column("amount", Integer),
    Column("product", String),
    Column("quantity", Integer),
)

regional_sales = (
    select(orders.c.region, func.sum(orders.c.amount).label("total_sales"))
    .group_by(orders.c.region)
    .cte("regional_sales")
)

top_regions = (
    select(regional_sales.c.region)
    .where(
        regional_sales.c.total_sales
        > select(func.sum(regional_sales.c.total_sales) / 10)
    )
    .cte("top_regions")
)

statement = (
    select(
        orders.c.region,
        orders.c.product,
        func.sum(orders.c.quantity).label("product_units"),
        func.sum(orders.c.amount).label("product_sales"),
    )
    .where(orders.c.region.in_(select(top_regions.c.region)))
    .group_by(orders.c.region, orders.c.product)
)

result = conn.execute(statement).fetchall()
```

Example 2, WITH RECURSIVE:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

parts = Table(
    "parts",
    metadata,
    Column("part", String),
    Column("sub_part", String),
    Column("quantity", Integer),
)

included_parts = (
    select(parts.c.sub_part, parts.c.part, parts.c.quantity)
    .where(parts.c.part == "our part")
    .cte(recursive=True)
)

incl_alias = included_parts.alias()
parts_alias = parts.alias()
included_parts = included_parts.union_all(
    select(
        parts_alias.c.sub_part, parts_alias.c.part, parts_alias.c.quantity
    ).where(parts_alias.c.part == incl_alias.c.sub_part)
)

statement = select(
    included_parts.c.sub_part,
    func.sum(included_parts.c.quantity).label("total_quantity"),
).group_by(included_parts.c.sub_part)

result = conn.execute(statement).fetchall()
```

Example 3, an upsert using UPDATE and INSERT with CTEs:

```
from datetime import date
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Date,
    select,
    literal,
    and_,
    exists,
)

metadata = MetaData()

visitors = Table(
    "visitors",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("date", Date, primary_key=True),
    Column("count", Integer),
)

# add 5 visitors for the product_id == 1
product_id = 1
day = date.today()
count = 5

update_cte = (
    visitors.update()
    .where(
        and_(visitors.c.product_id == product_id, visitors.c.date == day)
    )
    .values(count=visitors.c.count + count)
    .returning(literal(1))
    .cte("update_cte")
)

upsert = visitors.insert().from_select(
    [visitors.c.product_id, visitors.c.date, visitors.c.count],
    select(literal(product_id), literal(day), literal(count)).where(
        ~exists(update_cte.select())
    ),
)

connection.execute(upsert)
```

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte(
    "value_a", nesting=True
)

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = select(value_a_nested.c.n).cte("value_b")

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

The above query will render the second CTE nested inside the first,
shown with inline parameters below as:

```
WITH
    value_a AS
        (SELECT 'root' AS n),
    value_b AS
        (WITH value_a AS
            (SELECT 'nesting' AS n)
        SELECT value_a.n AS n FROM value_a)
SELECT value_a.n AS a, value_b.n AS b
FROM value_a, value_b
```

The same CTE can be set up using the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method
as follows (SQLAlchemy 2.0 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte("value_a")

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = (
    select(value_a_nested.c.n)
    .add_cte(value_a_nested, nest_here=True)
    .cte("value_b")
)

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

```
edge = Table(
    "edge",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("left", Integer),
    Column("right", Integer),
)

root_node = select(literal(1).label("node")).cte("nodes", recursive=True)

left_edge = select(edge.c.left).join(
    root_node, edge.c.right == root_node.c.node
)
right_edge = select(edge.c.right).join(
    root_node, edge.c.left == root_node.c.node
)

subgraph_cte = root_node.union(left_edge, right_edge)

subgraph = select(subgraph_cte)
```

The above query will render 2 UNIONs inside the recursive CTE:

```
WITH RECURSIVE nodes(node) AS (
        SELECT 1 AS node
    UNION
        SELECT edge."left" AS "left"
        FROM edge JOIN nodes ON edge."right" = nodes.node
    UNION
        SELECT edge."right" AS "right"
        FROM edge JOIN nodes ON edge."left" = nodes.node
)
SELECT nodes.node FROM nodes
```

See also

[Query.cte()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.cte) - ORM version of
[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte).

     attribute [sqlalchemy.sql.expression.HasCTE.](#sqlalchemy.sql.expression.HasCTE)name_cte_columns: bool = False

indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause.

Added in version 2.0.42.

      class sqlalchemy.sql.expression.HasPrefixes

| Member Name | Description |
| --- | --- |
| prefix_with() | Add one or more expressions following the statement keyword, i.e.
SELECT, INSERT, UPDATE, or DELETE. Generative. |

   method [sqlalchemy.sql.expression.HasPrefixes.](#sqlalchemy.sql.expression.HasPrefixes)prefix_with(**prefixes:_TextCoercedExpressionArgument[Any]*, *dialect:str='*'*) → Self

Add one or more expressions following the statement keyword, i.e.
SELECT, INSERT, UPDATE, or DELETE. Generative.

This is used to support backend-specific prefix keywords such as those
provided by MySQL.

E.g.:

```
stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

# MySQL 5.7 optimizer hints
stmt = select(table).prefix_with("/*+ BKA(t1) */", dialect="mysql")
```

Multiple prefixes can be specified by multiple calls
to [HasPrefixes.prefix_with()](#sqlalchemy.sql.expression.HasPrefixes.prefix_with).

  Parameters:

- ***prefixes** – textual or [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  construct which
  will be rendered following the INSERT, UPDATE, or DELETE
  keyword.
- **dialect** – optional string dialect name which will
  limit rendering of this prefix to only that dialect.

       class sqlalchemy.sql.expression.HasSuffixes

| Member Name | Description |
| --- | --- |
| suffix_with() | Add one or more expressions following the statement as a whole. |

   method [sqlalchemy.sql.expression.HasSuffixes.](#sqlalchemy.sql.expression.HasSuffixes)suffix_with(**suffixes:_TextCoercedExpressionArgument[Any]*, *dialect:str='*'*) → Self

Add one or more expressions following the statement as a whole.

This is used to support backend-specific suffix keywords on
certain constructs.

E.g.:

```
stmt = (
    select(col1, col2)
    .cte()
    .suffix_with(
        "cycle empno set y_cycle to 1 default 0", dialect="oracle"
    )
)
```

Multiple suffixes can be specified by multiple calls
to [HasSuffixes.suffix_with()](#sqlalchemy.sql.expression.HasSuffixes.suffix_with).

  Parameters:

- ***suffixes** – textual or [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  construct which
  will be rendered following the target clause.
- **dialect** – Optional string dialect name which will
  limit rendering of this suffix to only that dialect.

       class sqlalchemy.sql.expression.Join

*inherits from* `sqlalchemy.sql.roles.DMLTableRole`, [sqlalchemy.sql.expression.FromClause](#sqlalchemy.sql.expression.FromClause)

Represent a `JOIN` construct between two
[FromClause](#sqlalchemy.sql.expression.FromClause)
elements.

The public constructor function for [Join](#sqlalchemy.sql.expression.Join)
is the module-level
[join()](#sqlalchemy.sql.expression.join) function, as well as the
[FromClause.join()](#sqlalchemy.sql.expression.FromClause.join) method
of any [FromClause](#sqlalchemy.sql.expression.FromClause) (e.g. such as
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)).

See also

[join()](#sqlalchemy.sql.expression.join)

[FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newJoin. |
| description |  |
| is_derived_from() | ReturnTrueif thisFromClauseis
‘derived’ from the givenFromClause. |
| select() | Create aSelectfrom thisJoin. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |

   method [sqlalchemy.sql.expression.Join.](#sqlalchemy.sql.expression.Join)__init__(*left:_FromClauseArgument*, *right:_FromClauseArgument*, *onclause:_OnClauseArgument|None=None*, *isouter:bool=False*, *full:bool=False*)

Construct a new [Join](#sqlalchemy.sql.expression.Join).

The usual entrypoint here is the [join()](#sqlalchemy.sql.expression.join)
function or the [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join) method of any
[FromClause](#sqlalchemy.sql.expression.FromClause) object.

    attribute [sqlalchemy.sql.expression.Join.](#sqlalchemy.sql.expression.Join)description    method [sqlalchemy.sql.expression.Join.](#sqlalchemy.sql.expression.Join)is_derived_from(*fromclause:FromClause|None*) → bool

Return `True` if this [FromClause](#sqlalchemy.sql.expression.FromClause) is
‘derived’ from the given `FromClause`.

An example would be an Alias of a Table is derived from that Table.

    method [sqlalchemy.sql.expression.Join.](#sqlalchemy.sql.expression.Join)select() → [Select](#sqlalchemy.sql.expression.Select)

Create a [Select](#sqlalchemy.sql.expression.Select) from this
[Join](#sqlalchemy.sql.expression.Join).

E.g.:

```
stmt = table_a.join(table_b, table_a.c.id == table_b.c.a_id)

stmt = stmt.select()
```

The above will produce a SQL string resembling:

```
SELECT table_a.id, table_a.col, table_b.id, table_b.a_id
FROM table_a JOIN table_b ON table_a.id = table_b.a_id
```

     method [sqlalchemy.sql.expression.Join.](#sqlalchemy.sql.expression.Join)self_group(*against:OperatorType|None=None*) → FromGrouping

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.Join.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.Join.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

     class sqlalchemy.sql.expression.Lateral

*inherits from* `sqlalchemy.sql.expression.FromClauseAlias`, `sqlalchemy.sql.expression.LateralFromClause`

Represent a LATERAL subquery.

This object is constructed from the [lateral()](#sqlalchemy.sql.expression.lateral) module
level function as well as the `FromClause.lateral()`
method available
on all [FromClause](#sqlalchemy.sql.expression.FromClause) subclasses.

While LATERAL is part of the SQL standard, currently only more recent
PostgreSQL versions provide support for this keyword.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

| Member Name | Description |
| --- | --- |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |

   attribute [sqlalchemy.sql.expression.Lateral.](#sqlalchemy.sql.expression.Lateral)inherit_cache = True

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

      class sqlalchemy.sql.expression.ReturnsRows

*inherits from* `sqlalchemy.sql.roles.ReturnsRowsRole`, `sqlalchemy.sql.expression.DQLDMLClauseElement`

The base-most class for Core constructs that have some concept of
columns that can represent rows.

While the SELECT statement and TABLE are the primary things we think
of in this category,  DML like INSERT, UPDATE and DELETE can also specify
RETURNING which means they can be used in CTEs and other forms, and
PostgreSQL has functions that return rows also.

Added in version 1.4.

| Member Name | Description |
| --- | --- |
| compile() | Compile this SQL expression. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| is_derived_from() | ReturnTrueif thisReturnsRowsis
‘derived’ from the givenFromClause. |

   method [sqlalchemy.sql.expression.ReturnsRows.](#sqlalchemy.sql.expression.ReturnsRows)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

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

     property exported_columns: ReadOnlyColumnCollection[Any, Any]

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows).

The “exported” columns represent the collection of
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
expressions that are rendered by this SQL
construct.   There are primary varieties which are the
“FROM clause columns” of a FROM clause, such as a table, join,
or subquery, the “SELECTed columns”, which are the columns in
the “columns clause” of a SELECT statement, and the RETURNING
columns in a DML statement..

Added in version 1.4.

See also

[FromClause.exported_columns](#sqlalchemy.sql.expression.FromClause.exported_columns)

[SelectBase.exported_columns](#sqlalchemy.sql.expression.SelectBase.exported_columns)

     method [sqlalchemy.sql.expression.ReturnsRows.](#sqlalchemy.sql.expression.ReturnsRows)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    attribute [sqlalchemy.sql.expression.ReturnsRows.](#sqlalchemy.sql.expression.ReturnsRows)inherit_cache = None

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

     method [sqlalchemy.sql.expression.ReturnsRows.](#sqlalchemy.sql.expression.ReturnsRows)is_derived_from(*fromclause:FromClause|None*) → bool

Return `True` if this [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows) is
‘derived’ from the given [FromClause](#sqlalchemy.sql.expression.FromClause).

An example would be an Alias of a Table is derived from that Table.

     class sqlalchemy.sql.expression.ScalarSelect

*inherits from* `sqlalchemy.sql.roles.InElementRole`, `sqlalchemy.sql.expression.Generative`, `sqlalchemy.sql.expression.GroupedElement`, [sqlalchemy.sql.expression.ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

Represent a scalar subquery.

A [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect) is created by invoking the
[SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery) method.   The object
then participates in other SQL expressions as a SQL column expression
within the [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) hierarchy.

See also

[SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery)

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery) - in the 2.0 tutorial

| Member Name | Description |
| --- | --- |
| correlate() | Return a newScalarSelectwhich will correlate the given FROM
clauses to that of an enclosingSelect. |
| correlate_except() | Return a newScalarSelectwhich will omit the given FROM
clauses from the auto-correlation process. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| where() | Apply a WHERE clause to the SELECT statement referred to
by thisScalarSelect. |

   method [sqlalchemy.sql.expression.ScalarSelect.](#sqlalchemy.sql.expression.ScalarSelect)correlate(**fromclauses:Literal[None,False]|_FromClauseArgument*) → Self

Return a new [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)
which will correlate the given FROM
clauses to that of an enclosing [Select](#sqlalchemy.sql.expression.Select).

This method is mirrored from the [Select.correlate()](#sqlalchemy.sql.expression.Select.correlate) method
of the underlying [Select](#sqlalchemy.sql.expression.Select).  The method applies the
:meth:_sql.Select.correlate` method, then returns a new
[ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect) against that statement.

Added in version 1.4: Previously, the
[ScalarSelect.correlate()](#sqlalchemy.sql.expression.ScalarSelect.correlate)
method was only available from [Select](#sqlalchemy.sql.expression.Select).

   Parameters:

***fromclauses** – a list of one or more
[FromClause](#sqlalchemy.sql.expression.FromClause)
constructs, or other compatible constructs (i.e. ORM-mapped
classes) to become part of the correlate collection.

See also

[ScalarSelect.correlate_except()](#sqlalchemy.sql.expression.ScalarSelect.correlate_except)

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery) - in the 2.0 tutorial

     method [sqlalchemy.sql.expression.ScalarSelect.](#sqlalchemy.sql.expression.ScalarSelect)correlate_except(**fromclauses:Literal[None,False]|_FromClauseArgument*) → Self

Return a new [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)
which will omit the given FROM
clauses from the auto-correlation process.

This method is mirrored from the
[Select.correlate_except()](#sqlalchemy.sql.expression.Select.correlate_except) method of the underlying
[Select](#sqlalchemy.sql.expression.Select).  The method applies the
:meth:_sql.Select.correlate_except` method, then returns a new
[ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect) against that statement.

Added in version 1.4: Previously, the
[ScalarSelect.correlate_except()](#sqlalchemy.sql.expression.ScalarSelect.correlate_except)
method was only available from [Select](#sqlalchemy.sql.expression.Select).

   Parameters:

***fromclauses** – a list of one or more
[FromClause](#sqlalchemy.sql.expression.FromClause)
constructs, or other compatible constructs (i.e. ORM-mapped
classes) to become part of the correlate-exception collection.

See also

[ScalarSelect.correlate()](#sqlalchemy.sql.expression.ScalarSelect.correlate)

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery) - in the 2.0 tutorial

     attribute [sqlalchemy.sql.expression.ScalarSelect.](#sqlalchemy.sql.expression.ScalarSelect)inherit_cache = True

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

     method [sqlalchemy.sql.expression.ScalarSelect.](#sqlalchemy.sql.expression.ScalarSelect)self_group(*against:OperatorType|None=None*) → Self

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.ScalarSelect.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.ScalarSelect.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.sql.expression.ScalarSelect.](#sqlalchemy.sql.expression.ScalarSelect)where(*crit:_ColumnExpressionArgument[bool]*) → Self

Apply a WHERE clause to the SELECT statement referred to
by this [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect).

     class sqlalchemy.sql.expression.Select

*inherits from* [sqlalchemy.sql.expression.HasPrefixes](#sqlalchemy.sql.expression.HasPrefixes), [sqlalchemy.sql.expression.HasSuffixes](#sqlalchemy.sql.expression.HasSuffixes), `sqlalchemy.sql.expression.HasHints`, `sqlalchemy.sql.expression.HasCompileState`, `sqlalchemy.sql.expression._SelectFromElements`, [sqlalchemy.sql.expression.GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect), `sqlalchemy.sql.expression.TypedReturnsRows`

Represents a `SELECT` statement.

The [Select](#sqlalchemy.sql.expression.Select) object is normally constructed using the
[select()](#sqlalchemy.sql.expression.select) function.  See that function for details.

See also

[select()](#sqlalchemy.sql.expression.select)

[Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-data) - in the 2.0 tutorial

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newSelect. |
| add_columns() | Return a newselect()construct with
the given entities appended to its columns clause. |
| add_cte() | Add one or moreCTEconstructs to this statement. |
| alias() | Return a named subquery against thisSelectBase. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| as_scalar() |  |
| column() | Return a newselect()construct with
the given column expression added to its columns clause. |
| compile() | Compile this SQL expression. |
| correlate() | Return a newSelectwhich will correlate the given FROM
clauses to that of an enclosingSelect. |
| correlate_except() | Return a newSelectwhich will omit the given FROM
clauses from the auto-correlation process. |
| corresponding_column() | Given aColumnElement, return the exportedColumnElementobject from theSelectable.exported_columnscollection of thisSelectablewhich corresponds to that
originalColumnElementvia a common ancestor
column. |
| cte() | Return a newCTE,
or Common Table Expression instance. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| distinct() | Return a newselect()construct which
will apply DISTINCT to the SELECT statement overall. |
| except_() | Return a SQLEXCEPTof this select() construct against
the given selectable provided as positional arguments. |
| except_all() | Return a SQLEXCEPTALLof this select() construct against
the given selectables provided as positional arguments. |
| execution_options() | Set non-SQL options for the statement which take effect during
execution. |
| exists() | Return anExistsrepresentation of this selectable,
which can be used as a column expression. |
| fetch() | Return a new selectable with the given FETCH FIRST criterion
applied. |
| filter() | A synonym for theSelect.where()method. |
| filter_by() | apply the given filtering criterion as a WHERE clause
to this select. |
| from_statement() | Apply the columns which thisSelectwould select
onto another statement. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| get_execution_options() | Get the non-SQL options which will take effect during execution. |
| get_final_froms() | Compute the final displayed list ofFromClauseelements. |
| get_label_style() | Retrieve the current label style. |
| group_by() | Return a new selectable with the given list of GROUP BY
criterion applied. |
| having() | Return a newselect()construct with
the given expression added to
its HAVING clause, joined to the existing clause via AND, if any. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| intersect() | Return a SQLINTERSECTof this select() construct against
the given selectables provided as positional arguments. |
| intersect_all() | Return a SQLINTERSECTALLof this select() construct
against the given selectables provided as positional arguments. |
| is_derived_from() | ReturnTrueif thisReturnsRowsis
‘derived’ from the givenFromClause. |
| join() | Create a SQL JOIN against thisSelectobject’s criterion
and apply generatively, returning the newly resultingSelect. |
| join_from() | Create a SQL JOIN against thisSelectobject’s criterion
and apply generatively, returning the newly resultingSelect. |
| label() | Return a ‘scalar’ representation of this selectable, embedded as a
subquery with a label. |
| lateral() | Return a LATERAL alias of thisSelectable. |
| limit() | Return a new selectable with the given LIMIT criterion
applied. |
| name_cte_columns | indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause. |
| offset() | Return a new selectable with the given OFFSET criterion
applied. |
| options() | Apply options to this statement. |
| order_by() | Return a new selectable with the given list of ORDER BY
criteria applied. |
| outerjoin() | Create a left outer join. |
| outerjoin_from() | Create a SQL LEFT OUTER JOIN against thisSelectobject’s criterion and apply generatively,
returning the newly resultingSelect. |
| prefix_with() | Add one or more expressions following the statement keyword, i.e.
SELECT, INSERT, UPDATE, or DELETE. Generative. |
| reduce_columns() | Return a newselect()construct with redundantly
named, equivalently-valued columns removed from the columns clause. |
| replace_selectable() | Replace all occurrences ofFromClause‘old’ with the givenAliasobject, returning a copy of thisFromClause. |
| scalar_subquery() | Return a ‘scalar’ representation of this selectable, which can be
used as a column expression. |
| select() |  |
| select_from() | Return a newselect()construct with the
given FROM expression(s)
merged into its list of FROM objects. |
| selected_columns | AColumnCollectionrepresenting the columns that
this SELECT statement or similar construct returns in its result set,
not includingTextClauseconstructs. |
| self_group() | Return a ‘grouping’ construct as per theClauseElementspecification. |
| set_label_style() | Return a new selectable with the specified label style. |
| slice() | Apply LIMIT / OFFSET to this statement based on a slice. |
| subquery() | Return a subquery of thisSelectBase. |
| suffix_with() | Add one or more expressions following the statement as a whole. |
| union() | Return a SQLUNIONof this select() construct against
the given selectables provided as positional arguments. |
| union_all() | Return a SQLUNIONALLof this select() construct against
the given selectables provided as positional arguments. |
| where() | Return a newselect()construct with
the given expression added to
its WHERE clause, joined to the existing clause via AND, if any. |
| with_for_update() | Specify aFORUPDATEclause for thisGenerativeSelect. |
| with_hint() | Add an indexing or other executional context hint for the given
selectable to thisSelector other selectable
object. |
| with_only_columns() | Return a newselect()construct with its columns
clause replaced with the given entities. |
| with_statement_hint() | Add a statement hint to thisSelector
other selectable object. |

   method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)__init__(**entities:_ColumnsClauseArgument[Any]*, ***dialect_kw:Any*)

Construct a new [Select](#sqlalchemy.sql.expression.Select).

The public constructor for [Select](#sqlalchemy.sql.expression.Select) is the
[select()](#sqlalchemy.sql.expression.select) function.

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)add_columns(**entities:_ColumnsClauseArgument[Any]*) → [Select](#sqlalchemy.sql.expression.Select)[Any]

Return a new [select()](#sqlalchemy.sql.expression.select) construct with
the given entities appended to its columns clause.

E.g.:

```
my_select = my_select.add_columns(table.c.new_column)
```

The original expressions in the columns clause remain in place.
To replace the original expressions with new ones, see the method
[Select.with_only_columns()](#sqlalchemy.sql.expression.Select.with_only_columns).

  Parameters:

***entities** – column, table, or other entity expressions to be
added to the columns clause

See also

[Select.with_only_columns()](#sqlalchemy.sql.expression.Select.with_only_columns) - replaces existing
expressions rather than appending.

[Selecting Multiple ORM Entities Simultaneously](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-select-multiple-entities) - ORM-centric
example

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)add_cte(**ctes:CTE*, *nest_here:bool=False*) → Self

*inherited from the* [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Add one or more [CTE](#sqlalchemy.sql.expression.CTE) constructs to this statement.

This method will associate the given [CTE](#sqlalchemy.sql.expression.CTE) constructs with
the parent statement such that they will each be unconditionally
rendered in the WITH clause of the final statement, even if not
referenced elsewhere within the statement or any sub-selects.

The optional [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here) parameter when set
to True will have the effect that each given [CTE](#sqlalchemy.sql.expression.CTE) will
render in a WITH clause rendered directly along with this statement,
rather than being moved to the top of the ultimate rendered statement,
even if this statement is rendered as a subquery within a larger
statement.

This method has two general uses. One is to embed CTE statements that
serve some purpose without being referenced explicitly, such as the use
case of embedding a DML statement such as an INSERT or UPDATE as a CTE
inline with a primary statement that may draw from its results
indirectly.  The other is to provide control over the exact placement
of a particular series of CTE constructs that should remain rendered
directly in terms of a particular statement that may be nested in a
larger statement.

E.g.:

```
from sqlalchemy import table, column, select

t = table("t", column("c1"), column("c2"))

ins = t.insert().values({"c1": "x", "c2": "y"}).cte()

stmt = select(t).add_cte(ins)
```

Would render:

```
WITH anon_1 AS (
    INSERT INTO t (c1, c2) VALUES (:param_1, :param_2)
)
SELECT t.c1, t.c2
FROM t
```

Above, the “anon_1” CTE is not referenced in the SELECT
statement, however still accomplishes the task of running an INSERT
statement.

Similarly in a DML-related context, using the PostgreSQL
[Insert](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert) construct to generate an “upsert”:

```
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import insert

t = table("t", column("c1"), column("c2"))

delete_statement_cte = t.delete().where(t.c.c1 < 1).cte("deletions")

insert_stmt = insert(t).values({"c1": 1, "c2": 2})
update_statement = insert_stmt.on_conflict_do_update(
    index_elements=[t.c.c1],
    set_={
        "c1": insert_stmt.excluded.c1,
        "c2": insert_stmt.excluded.c2,
    },
).add_cte(delete_statement_cte)

print(update_statement)
```

The above statement renders as:

```
WITH deletions AS (
    DELETE FROM t WHERE t.c1 < %(c1_1)s
)
INSERT INTO t (c1, c2) VALUES (%(c1)s, %(c2)s)
ON CONFLICT (c1) DO UPDATE SET c1 = excluded.c1, c2 = excluded.c2
```

Added in version 1.4.21.

   Parameters:

- ***ctes** –
  zero or more [CTE](#sqlalchemy.sql.expression.CTE) constructs.
  Changed in version 2.0: Multiple CTE instances are accepted
- **nest_here** –
  if True, the given CTE or CTEs will be rendered
  as though they specified the [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting) flag
  to `True` when they were added to this [HasCTE](#sqlalchemy.sql.expression.HasCTE).
  Assuming the given CTEs are not referenced in an outer-enclosing
  statement as well, the CTEs given should render at the level of
  this statement when this flag is given.
  Added in version 2.0.
  See also
  [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting)

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)alias(*name:str|None=None*, *flat:bool=False*) → [Subquery](#sqlalchemy.sql.expression.Subquery)

*inherited from the* [SelectBase.alias()](#sqlalchemy.sql.expression.SelectBase.alias) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a named subquery against this
[SelectBase](#sqlalchemy.sql.expression.SelectBase).

For a [SelectBase](#sqlalchemy.sql.expression.SelectBase) (as opposed to a
[FromClause](#sqlalchemy.sql.expression.FromClause)),
this returns a [Subquery](#sqlalchemy.sql.expression.Subquery) object which behaves mostly the
same as the [Alias](#sqlalchemy.sql.expression.Alias) object that is used with a
[FromClause](#sqlalchemy.sql.expression.FromClause).

Changed in version 1.4: The [SelectBase.alias()](#sqlalchemy.sql.expression.SelectBase.alias)
method is now
a synonym for the [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) method.

     classmethod [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

*inherited from the* `DialectKWArgs.argument_for()` *method of* `DialectKWArgs`

Add a new kind of dialect-specific keyword argument for this class.

E.g.:

```
Index.argument_for("mydialect", "length", None)

some_index = Index("a", "b", mydialect_length=5)
```

The [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for) method is a per-argument
way adding extra arguments to the
[DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) dictionary. This
dictionary provides a list of argument names accepted by various
schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a
data member of the dialect class.  The use case for ad-hoc addition of
argument names is typically for end-user code that is also using
a custom compilation scheme which consumes the additional arguments.

  Parameters:

- **dialect_name** – name of a dialect.  The dialect must be
  locatable, else a [NoSuchModuleError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchModuleError) is raised.   The
  dialect must also include an existing
  [DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) collection, indicating
  that it participates in the keyword-argument validation and default
  system, else [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is raised.  If the dialect does
  not include this collection, then any keyword argument can be
  specified on behalf of this dialect already.  All dialects packaged
  within SQLAlchemy include this collection, however for third party
  dialects, support may vary.
- **argument_name** – name of the parameter.
- **default** – default value of the parameter.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)as_scalar() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

*inherited from the* [SelectBase.as_scalar()](#sqlalchemy.sql.expression.SelectBase.as_scalar) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Deprecated since version 1.4: The [SelectBase.as_scalar()](#sqlalchemy.sql.expression.SelectBase.as_scalar) method is deprecated and will be removed in a future release.  Please refer to [SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

     property c: ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]

Deprecated since version 1.4: The [SelectBase.c](#sqlalchemy.sql.expression.SelectBase.c) and `SelectBase.columns` attributes are deprecated and will be removed in a future release; these attributes implicitly create a subquery that should be explicit.  Please call [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) first in order to create a subquery, which then contains this attribute.  To access the columns that this SELECT object SELECTs from, use the [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) attribute.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)column(*column:_ColumnsClauseArgument[Any]*) → [Select](#sqlalchemy.sql.expression.Select)[Any]

Return a new [select()](#sqlalchemy.sql.expression.select) construct with
the given column expression added to its columns clause.

Deprecated since version 1.4: The [Select.column()](#sqlalchemy.sql.expression.Select.column) method is deprecated and will be removed in a future release.  Please use [Select.add_columns()](#sqlalchemy.sql.expression.Select.add_columns)

E.g.:

```
my_select = my_select.column(table.c.new_column)
```

See the documentation for
[Select.with_only_columns()](#sqlalchemy.sql.expression.Select.with_only_columns)
for guidelines on adding /replacing the columns of a
[Select](#sqlalchemy.sql.expression.Select) object.

    property column_descriptions: Any

Return a [plugin-enabled](https://docs.sqlalchemy.org/en/20/glossary.html#term-plugin-enabled) ‘column descriptions’ structure
referring to the columns which are SELECTed by this statement.

This attribute is generally useful when using the ORM, as an
extended structure which includes information about mapped
entities is returned.  The section [Inspecting entities and columns from ORM-enabled SELECT and DML statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-inspection)
contains more background.

For a Core-only statement, the structure returned by this accessor
is derived from the same objects that are returned by the
[Select.selected_columns](#sqlalchemy.sql.expression.Select.selected_columns) accessor, formatted as a list of
dictionaries which contain the keys `name`, `type` and `expr`,
which indicate the column expressions to be selected:

```
>>> stmt = select(user_table)
>>> stmt.column_descriptions
[
    {
        'name': 'id',
        'type': Integer(),
        'expr': Column('id', Integer(), ...)},
    {
        'name': 'name',
        'type': String(length=30),
        'expr': Column('name', String(length=30), ...)}
]
```

Changed in version 1.4.33: The [Select.column_descriptions](#sqlalchemy.sql.expression.Select.column_descriptions)
attribute returns a structure for a Core-only set of entities,
not just ORM-only entities.

See also

[UpdateBase.entity_description](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.entity_description) - entity information for
an [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert), [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update), or [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete)

[Inspecting entities and columns from ORM-enabled SELECT and DML statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-inspection) - ORM background

     property columns_clause_froms: List[[FromClause](#sqlalchemy.sql.expression.FromClause)]

Return the set of [FromClause](#sqlalchemy.sql.expression.FromClause) objects implied
by the columns clause of this SELECT statement.

Added in version 1.4.23.

See also

[Select.froms](#sqlalchemy.sql.expression.Select.froms) - “final” FROM list taking the full
statement into account

[Select.with_only_columns()](#sqlalchemy.sql.expression.Select.with_only_columns) - makes use of this
collection to set up a new FROM list

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

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

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)correlate(**fromclauses:Literal[None,False]|_FromClauseArgument*) → Self

Return a new [Select](#sqlalchemy.sql.expression.Select)
which will correlate the given FROM
clauses to that of an enclosing [Select](#sqlalchemy.sql.expression.Select).

Calling this method turns off the [Select](#sqlalchemy.sql.expression.Select) object’s
default behavior of “auto-correlation”.  Normally, FROM elements
which appear in a [Select](#sqlalchemy.sql.expression.Select)
that encloses this one via
its [WHERE clause](https://docs.sqlalchemy.org/en/20/glossary.html#term-WHERE-clause), ORDER BY, HAVING or
[columns clause](https://docs.sqlalchemy.org/en/20/glossary.html#term-columns-clause) will be omitted from this
[Select](#sqlalchemy.sql.expression.Select)
object’s [FROM clause](https://docs.sqlalchemy.org/en/20/glossary.html#term-FROM-clause).
Setting an explicit correlation collection using the
[Select.correlate()](#sqlalchemy.sql.expression.Select.correlate)
method provides a fixed list of FROM objects
that can potentially take place in this process.

When [Select.correlate()](#sqlalchemy.sql.expression.Select.correlate)
is used to apply specific FROM clauses
for correlation, the FROM elements become candidates for
correlation regardless of how deeply nested this
[Select](#sqlalchemy.sql.expression.Select)
object is, relative to an enclosing [Select](#sqlalchemy.sql.expression.Select)
which refers to
the same FROM object.  This is in contrast to the behavior of
“auto-correlation” which only correlates to an immediate enclosing
[Select](#sqlalchemy.sql.expression.Select).
Multi-level correlation ensures that the link
between enclosed and enclosing [Select](#sqlalchemy.sql.expression.Select)
is always via
at least one WHERE/ORDER BY/HAVING/columns clause in order for
correlation to take place.

If `None` is passed, the [Select](#sqlalchemy.sql.expression.Select)
object will correlate
none of its FROM entries, and all will render unconditionally
in the local FROM clause.

  Parameters:

***fromclauses** – one or more [FromClause](#sqlalchemy.sql.expression.FromClause) or other
FROM-compatible construct such as an ORM mapped entity to become part
of the correlate collection; alternatively pass a single value
`None` to remove all existing correlations.

See also

[Select.correlate_except()](#sqlalchemy.sql.expression.Select.correlate_except)

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)correlate_except(**fromclauses:Literal[None,False]|_FromClauseArgument*) → Self

Return a new [Select](#sqlalchemy.sql.expression.Select)
which will omit the given FROM
clauses from the auto-correlation process.

Calling [Select.correlate_except()](#sqlalchemy.sql.expression.Select.correlate_except) turns off the
[Select](#sqlalchemy.sql.expression.Select) object’s default behavior of
“auto-correlation” for the given FROM elements.  An element
specified here will unconditionally appear in the FROM list, while
all other FROM elements remain subject to normal auto-correlation
behaviors.

If `None` is passed, or no arguments are passed,
the [Select](#sqlalchemy.sql.expression.Select) object will correlate all of its
FROM entries.

  Parameters:

***fromclauses** – a list of one or more
[FromClause](#sqlalchemy.sql.expression.FromClause)
constructs, or other compatible constructs (i.e. ORM-mapped
classes) to become part of the correlate-exception collection.

See also

[Select.correlate()](#sqlalchemy.sql.expression.Select.correlate)

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)corresponding_column(*column:KeyedColumnElement[Any]*, *require_embedded:bool=False*) → KeyedColumnElement[Any] | None

*inherited from the* [Selectable.corresponding_column()](#sqlalchemy.sql.expression.Selectable.corresponding_column) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Given a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), return the exported
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) object from the
[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)
collection of this [Selectable](#sqlalchemy.sql.expression.Selectable)
which corresponds to that
original [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) via a common ancestor
column.

  Parameters:

- **column** – the target [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  to be matched.
- **require_embedded** – only return corresponding columns for
  the given [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), if the given
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  is actually present within a sub-element
  of this [Selectable](#sqlalchemy.sql.expression.Selectable).
  Normally the column will match if
  it merely shares a common ancestor with one of the exported
  columns of this [Selectable](#sqlalchemy.sql.expression.Selectable).

See also

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns) - the
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that is used for the operation.

[ColumnCollection.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.corresponding_column)
- implementation
method.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)cte(*name:str|None=None*, *recursive:bool=False*, *nesting:bool=False*) → [CTE](#sqlalchemy.sql.expression.CTE)

*inherited from the* [HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE),
or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT
statements can draw upon secondary statements specified along
with the primary statement, using a clause called “WITH”.
Special semantics regarding UNION can also be employed to
allow “recursive” queries, where a SELECT statement can draw
upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT
and DELETE on some databases, both as a source of CTE rows
when combined with RETURNING, as well as a consumer of
CTE rows.

SQLAlchemy detects [CTE](#sqlalchemy.sql.expression.CTE) objects, which are treated
similarly to [Alias](#sqlalchemy.sql.expression.Alias) objects, as special elements
to be delivered to the FROM clause of the statement as well
as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and
“NOT MATERIALIZED”, the `CTE.prefix_with()`
method may be
used to establish these.

Changed in version 1.3.13: Added support for prefixes.
In particular - MATERIALIZED and NOT MATERIALIZED.

   Parameters:

- **name** – name given to the common table expression.  Like
  [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias), the name can be left as
  `None` in which case an anonymous symbol will be used at query
  compile time.
- **recursive** – if `True`, will render `WITH RECURSIVE`.
  A recursive common table expression is intended to be used in
  conjunction with UNION ALL in order to derive rows
  from those already selected.
- **nesting** –
  if `True`, will render the CTE locally to the
  statement in which it is referenced.   For more complex scenarios,
  the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method using the
  [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here)
  parameter may also be used to more carefully
  control the exact placement of a particular CTE.
  Added in version 1.4.24.
  See also
  [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte)

The following examples include two from PostgreSQL’s documentation at
[https://www.postgresql.org/docs/current/static/queries-with.html](https://www.postgresql.org/docs/current/static/queries-with.html),
as well as additional examples.

Example 1, non recursive:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("region", String),
    Column("amount", Integer),
    Column("product", String),
    Column("quantity", Integer),
)

regional_sales = (
    select(orders.c.region, func.sum(orders.c.amount).label("total_sales"))
    .group_by(orders.c.region)
    .cte("regional_sales")
)

top_regions = (
    select(regional_sales.c.region)
    .where(
        regional_sales.c.total_sales
        > select(func.sum(regional_sales.c.total_sales) / 10)
    )
    .cte("top_regions")
)

statement = (
    select(
        orders.c.region,
        orders.c.product,
        func.sum(orders.c.quantity).label("product_units"),
        func.sum(orders.c.amount).label("product_sales"),
    )
    .where(orders.c.region.in_(select(top_regions.c.region)))
    .group_by(orders.c.region, orders.c.product)
)

result = conn.execute(statement).fetchall()
```

Example 2, WITH RECURSIVE:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

parts = Table(
    "parts",
    metadata,
    Column("part", String),
    Column("sub_part", String),
    Column("quantity", Integer),
)

included_parts = (
    select(parts.c.sub_part, parts.c.part, parts.c.quantity)
    .where(parts.c.part == "our part")
    .cte(recursive=True)
)

incl_alias = included_parts.alias()
parts_alias = parts.alias()
included_parts = included_parts.union_all(
    select(
        parts_alias.c.sub_part, parts_alias.c.part, parts_alias.c.quantity
    ).where(parts_alias.c.part == incl_alias.c.sub_part)
)

statement = select(
    included_parts.c.sub_part,
    func.sum(included_parts.c.quantity).label("total_quantity"),
).group_by(included_parts.c.sub_part)

result = conn.execute(statement).fetchall()
```

Example 3, an upsert using UPDATE and INSERT with CTEs:

```
from datetime import date
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Date,
    select,
    literal,
    and_,
    exists,
)

metadata = MetaData()

visitors = Table(
    "visitors",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("date", Date, primary_key=True),
    Column("count", Integer),
)

# add 5 visitors for the product_id == 1
product_id = 1
day = date.today()
count = 5

update_cte = (
    visitors.update()
    .where(
        and_(visitors.c.product_id == product_id, visitors.c.date == day)
    )
    .values(count=visitors.c.count + count)
    .returning(literal(1))
    .cte("update_cte")
)

upsert = visitors.insert().from_select(
    [visitors.c.product_id, visitors.c.date, visitors.c.count],
    select(literal(product_id), literal(day), literal(count)).where(
        ~exists(update_cte.select())
    ),
)

connection.execute(upsert)
```

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte(
    "value_a", nesting=True
)

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = select(value_a_nested.c.n).cte("value_b")

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

The above query will render the second CTE nested inside the first,
shown with inline parameters below as:

```
WITH
    value_a AS
        (SELECT 'root' AS n),
    value_b AS
        (WITH value_a AS
            (SELECT 'nesting' AS n)
        SELECT value_a.n AS n FROM value_a)
SELECT value_a.n AS a, value_b.n AS b
FROM value_a, value_b
```

The same CTE can be set up using the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method
as follows (SQLAlchemy 2.0 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte("value_a")

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = (
    select(value_a_nested.c.n)
    .add_cte(value_a_nested, nest_here=True)
    .cte("value_b")
)

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

```
edge = Table(
    "edge",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("left", Integer),
    Column("right", Integer),
)

root_node = select(literal(1).label("node")).cte("nodes", recursive=True)

left_edge = select(edge.c.left).join(
    root_node, edge.c.right == root_node.c.node
)
right_edge = select(edge.c.right).join(
    root_node, edge.c.left == root_node.c.node
)

subgraph_cte = root_node.union(left_edge, right_edge)

subgraph = select(subgraph_cte)
```

The above query will render 2 UNIONs inside the recursive CTE:

```
WITH RECURSIVE nodes(node) AS (
        SELECT 1 AS node
    UNION
        SELECT edge."left" AS "left"
        FROM edge JOIN nodes ON edge."right" = nodes.node
    UNION
        SELECT edge."right" AS "right"
        FROM edge JOIN nodes ON edge."left" = nodes.node
)
SELECT nodes.node FROM nodes
```

See also

[Query.cte()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.cte) - ORM version of
[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte).

     property dialect_kwargs: _DialectArgView

A collection of keyword arguments specified as dialect-specific
options to this construct.

The arguments are present here in their original `<dialect>_<kwarg>`
format.  Only arguments that were actually passed are included;
unlike the [DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options) collection, which
contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the
form `<dialect>_<kwarg>` where the value will be assembled
into the list of options.

See also

[DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options) - nested dictionary form

     attribute [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)dialect_options

*inherited from the* `DialectKWArgs.dialect_options` *attribute of* `DialectKWArgs`

A collection of keyword arguments specified as dialect-specific
options to this construct.

This is a two-level nested registry, keyed to `<dialect_name>`
and `<argument_name>`.  For example, the `postgresql_where`
argument would be locatable as:

```
arg = my_object.dialect_options["postgresql"]["where"]
```

Added in version 0.9.2.

See also

[DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs) - flat dictionary form

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)distinct(**expr:_ColumnExpressionArgument[Any]*) → Self

Return a new [select()](#sqlalchemy.sql.expression.select) construct which
will apply DISTINCT to the SELECT statement overall.

E.g.:

```
from sqlalchemy import select

stmt = select(users_table.c.id, users_table.c.name).distinct()
```

The above would produce an statement resembling:

```
SELECT DISTINCT user.id, user.name FROM user
```

The method also accepts an `*expr` parameter which produces the
PostgreSQL dialect-specific `DISTINCT ON` expression.  Using this
parameter on other backends which don’t support this syntax will
raise an error.

  Parameters:

***expr** –

optional column expressions.  When present,
the PostgreSQL dialect will render a `DISTINCT ON (<expressions>)`
construct.  A deprecation warning and/or [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError)
will be raised on other backends.

Deprecated since version 1.4: Using *expr in other dialects is deprecated
and will raise [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) in a future version.

       method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)except_(**other:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return a SQL `EXCEPT` of this select() construct against
the given selectable provided as positional arguments.

  Parameters:

***other** –

one or more elements with which to create a
UNION.

Changed in version 1.4.28: multiple elements are now accepted.

       method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)except_all(**other:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return a SQL `EXCEPT ALL` of this select() construct against
the given selectables provided as positional arguments.

  Parameters:

***other** –

one or more elements with which to create a
UNION.

Changed in version 1.4.28: multiple elements are now accepted.

       method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)execution_options(***kw:Any*) → Self

*inherited from the* [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Set non-SQL options for the statement which take effect during
execution.

Execution options can be set at many scopes, including per-statement,
per-connection, or per execution, using methods such as
[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) and parameters which
accept a dictionary of options such as
[Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options) and
[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options).

The primary characteristic of an execution option, as opposed to
other kinds of options such as ORM loader options, is that
**execution options never affect the compiled SQL of a query, only
things that affect how the SQL statement itself is invoked or how
results are fetched**.  That is, execution options are not part of
what’s accommodated by SQL compilation nor are they considered part of
the cached state of a statement.

The [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) method is
[generative](https://docs.sqlalchemy.org/en/20/glossary.html#term-generative), as
is the case for the method as applied to the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
and [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects, which means when the method is called,
a copy of the object is returned, which applies the given parameters to
that new copy, but leaves the original unchanged:

```
statement = select(table.c.x, table.c.y)
new_statement = statement.execution_options(my_option=True)
```

An exception to this behavior is the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
object, where the [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) method
is explicitly **not** generative.

The kinds of options that may be passed to
[Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) and other related methods and
parameter dictionaries include parameters that are explicitly consumed
by SQLAlchemy Core or ORM, as well as arbitrary keyword arguments not
defined by SQLAlchemy, which means the methods and/or parameter
dictionaries may be used for user-defined parameters that interact with
custom code, which may access the parameters using methods such as
[Executable.get_execution_options()](#sqlalchemy.sql.expression.Executable.get_execution_options) and
[Connection.get_execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_execution_options), or within selected
event hooks using a dedicated `execution_options` event parameter
such as
[ConnectionEvents.before_execute.execution_options](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_execute.params.execution_options)
or [ORMExecuteState.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.execution_options), e.g.:

```
from sqlalchemy import event

@event.listens_for(some_engine, "before_execute")
def _process_opt(conn, statement, multiparams, params, execution_options):
    "run a SQL function before invoking a statement"

    if execution_options.get("do_special_thing", False):
        conn.exec_driver_sql("run_special_function()")
```

Within the scope of options that are explicitly recognized by
SQLAlchemy, most apply to specific classes of objects and not others.
The most common execution options include:

- [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
  sets the isolation level for a connection or a class of connections
  via an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).  This option is accepted only
  by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).
- [Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results) -
  indicates results should be fetched using a server side cursor;
  this option is accepted by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), by the
  [Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options) parameter
  on [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), and additionally by
  [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) on a SQL statement object,
  as well as by ORM constructs like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
- [Connection.execution_options.compiled_cache](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.compiled_cache) -
  indicates a dictionary that will serve as the
  [SQL compilation cache](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)
  for a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), as
  well as for ORM methods like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
  Can be passed as `None` to disable caching for statements.
  This option is not accepted by
  [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) as it is inadvisable to
  carry along a compilation cache within a statement object.
- [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map)
  - a mapping of schema names used by the
  [Schema Translate Map](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating) feature, accepted
  by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
  [Executable](#sqlalchemy.sql.expression.Executable), as well as by ORM constructs
  like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).

See also

[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options)

[Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options)

[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options)

[ORM Execution Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-execution-options) - documentation on all
ORM-specific execution options

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)exists() → [Exists](#sqlalchemy.sql.expression.Exists)

*inherited from the* [SelectBase.exists()](#sqlalchemy.sql.expression.SelectBase.exists) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return an [Exists](#sqlalchemy.sql.expression.Exists) representation of this selectable,
which can be used as a column expression.

The returned object is an instance of [Exists](#sqlalchemy.sql.expression.Exists).

See also

[exists()](#sqlalchemy.sql.expression.exists)

[EXISTS subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-exists) - in the [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) tutorial.

Added in version 1.4.

     property exported_columns: ReadOnlyColumnCollection[str, [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]]

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [Selectable](#sqlalchemy.sql.expression.Selectable), not including
[TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) constructs.

The “exported” columns for a [SelectBase](#sqlalchemy.sql.expression.SelectBase)
object are synonymous
with the [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) collection.

Added in version 1.4.

See also

[Select.exported_columns](#sqlalchemy.sql.expression.Select.exported_columns)

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)

[FromClause.exported_columns](#sqlalchemy.sql.expression.FromClause.exported_columns)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)fetch(*count:_LimitOffsetType*, *with_ties:bool=False*, *percent:bool=False*, ***dialect_kw:Any*) → Self

*inherited from the* [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given FETCH FIRST criterion
applied.

This is a numeric value which usually renders as `FETCH {FIRST | NEXT}
[ count ] {ROW | ROWS} {ONLY | WITH TIES}` expression in the resulting
select. This functionality is is currently implemented for Oracle
Database, PostgreSQL, MSSQL.

Use [GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset) to specify the offset.

Note

The [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch) method will replace
any clause applied with [GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit).

Added in version 1.4.

   Parameters:

- **count** – an integer COUNT parameter, or a SQL expression
  that provides an integer result. When `percent=True` this will
  represent the percentage of rows to return, not the absolute value.
  Pass `None` to reset it.
- **with_ties** – When `True`, the WITH TIES option is used
  to return any additional rows that tie for the last place in the
  result set according to the `ORDER BY` clause. The
  `ORDER BY` may be mandatory in this case. Defaults to `False`
- **percent** – When `True`, `count` represents the percentage
  of the total number of selected rows to return. Defaults to `False`
- ****dialect_kw** –
  Additional dialect-specific keyword arguments
  may be accepted by dialects.
  Added in version 2.0.41.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)filter(**criteria:_ColumnExpressionArgument[bool]*) → Self

A synonym for the [Select.where()](#sqlalchemy.sql.expression.Select.where) method.

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)filter_by(***kwargs:Any*) → Self

apply the given filtering criterion as a WHERE clause
to this select.

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)from_statement(*statement:ReturnsRowsRole*) → ExecutableReturnsRows

Apply the columns which this [Select](#sqlalchemy.sql.expression.Select) would select
onto another statement.

This operation is [plugin-specific](https://docs.sqlalchemy.org/en/20/glossary.html#term-plugin-specific) and will raise a not
supported exception if this [Select](#sqlalchemy.sql.expression.Select) does not select from
plugin-enabled entities.

The statement is typically either a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) or
[select()](#sqlalchemy.sql.expression.select) construct, and should return the set of
columns appropriate to the entities represented by this
[Select](#sqlalchemy.sql.expression.Select).

See also

[Getting ORM Results from Textual Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-selecting-text) - usage examples in the
ORM Querying Guide

     property froms: Sequence[[FromClause](#sqlalchemy.sql.expression.FromClause)]

Return the displayed list of [FromClause](#sqlalchemy.sql.expression.FromClause)
elements.

Deprecated since version 1.4.23: The [Select.froms](#sqlalchemy.sql.expression.Select.froms) attribute is moved to the [Select.get_final_froms()](#sqlalchemy.sql.expression.Select.get_final_froms) method.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)get_children(***kw:Any*) → Iterable[[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)]

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)get_execution_options() → _ExecuteOptions

*inherited from the* [Executable.get_execution_options()](#sqlalchemy.sql.expression.Executable.get_execution_options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

See also

[Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)get_final_froms() → Sequence[[FromClause](#sqlalchemy.sql.expression.FromClause)]

Compute the final displayed list of [FromClause](#sqlalchemy.sql.expression.FromClause)
elements.

This method will run through the full computation required to
determine what FROM elements will be displayed in the resulting
SELECT statement, including shadowing individual tables with
JOIN objects, as well as full computation for ORM use cases including
eager loading clauses.

For ORM use, this accessor returns the **post compilation**
list of FROM objects; this collection will include elements such as
eagerly loaded tables and joins.  The objects will **not** be
ORM enabled and not work as a replacement for the
`Select.select_froms()` collection; additionally, the
method is not well performing for an ORM enabled statement as it
will incur the full ORM construction process.

To retrieve the FROM list that’s implied by the “columns” collection
passed to the [Select](#sqlalchemy.sql.expression.Select) originally, use the
[Select.columns_clause_froms](#sqlalchemy.sql.expression.Select.columns_clause_froms) accessor.

To select from an alternative set of columns while maintaining the
FROM list, use the [Select.with_only_columns()](#sqlalchemy.sql.expression.Select.with_only_columns) method and
pass the
[Select.with_only_columns.maintain_column_froms](#sqlalchemy.sql.expression.Select.with_only_columns.params.maintain_column_froms)
parameter.

Added in version 1.4.23: - the [Select.get_final_froms()](#sqlalchemy.sql.expression.Select.get_final_froms)
method replaces the previous [Select.froms](#sqlalchemy.sql.expression.Select.froms) accessor,
which is deprecated.

See also

[Select.columns_clause_froms](#sqlalchemy.sql.expression.Select.columns_clause_froms)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)get_label_style() → [SelectLabelStyle](#sqlalchemy.sql.expression.SelectLabelStyle)

*inherited from the* [GenerativeSelect.get_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.get_label_style) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Retrieve the current label style.

Added in version 1.4.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)group_by(*_GenerativeSelect__first:Literal[None,_NoArg.NO_ARG]|_ColumnExpressionOrStrLabelArgument[Any]=_NoArg.NO_ARG*, **clauses:_ColumnExpressionOrStrLabelArgument[Any]*) → Self

*inherited from the* [GenerativeSelect.group_by()](#sqlalchemy.sql.expression.GenerativeSelect.group_by) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given list of GROUP BY
criterion applied.

All existing GROUP BY settings can be suppressed by passing `None`.

e.g.:

```
stmt = select(table.c.name, func.max(table.c.stat)).group_by(table.c.name)
```

   Parameters:

***clauses** –

a series of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
constructs which will be used to generate an GROUP BY clause.

Alternatively, an individual entry may also be the string name of a
label located elsewhere in the columns clause of the statement which
will be matched and rendered in a backend-specific way based on
context; see [Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) for background on string
label matching in ORDER BY and GROUP BY expressions.

See also

[Aggregate functions with GROUP BY / HAVING](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-group-by-w-aggregates) - in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)having(**having:_ColumnExpressionArgument[bool]*) → Self

Return a new [select()](#sqlalchemy.sql.expression.select) construct with
the given expression added to
its HAVING clause, joined to the existing clause via AND, if any.

    attribute [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)inherit_cache = None

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

     property inner_columns: _SelectIterable

An iterator of all [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
expressions which would
be rendered into the columns clause of the resulting SELECT statement.

This method is legacy as of 1.4 and is superseded by the
[Select.exported_columns](#sqlalchemy.sql.expression.Select.exported_columns) collection.

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)intersect(**other:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return a SQL `INTERSECT` of this select() construct against
the given selectables provided as positional arguments.

  Parameters:

- ***other** –
  one or more elements with which to create a
  UNION.
  Changed in version 1.4.28: multiple elements are now accepted.
- ****kwargs** – keyword arguments are forwarded to the constructor
  for the newly created [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect) object.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)intersect_all(**other:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return a SQL `INTERSECT ALL` of this select() construct
against the given selectables provided as positional arguments.

  Parameters:

- ***other** –
  one or more elements with which to create a
  UNION.
  Changed in version 1.4.28: multiple elements are now accepted.
- ****kwargs** – keyword arguments are forwarded to the constructor
  for the newly created [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect) object.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)is_derived_from(*fromclause:FromClause|None*) → bool

Return `True` if this [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows) is
‘derived’ from the given [FromClause](#sqlalchemy.sql.expression.FromClause).

An example would be an Alias of a Table is derived from that Table.

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)join(*target:_JoinTargetArgument*, *onclause:_OnClauseArgument|None=None*, ***, *isouter:bool=False*, *full:bool=False*) → Self

Create a SQL JOIN against this [Select](#sqlalchemy.sql.expression.Select)
object’s criterion
and apply generatively, returning the newly resulting
[Select](#sqlalchemy.sql.expression.Select).

E.g.:

```
stmt = select(user_table).join(
    address_table, user_table.c.id == address_table.c.user_id
)
```

The above statement generates SQL similar to:

```
SELECT user.id, user.name
FROM user
JOIN address ON user.id = address.user_id
```

Changed in version 1.4: [Select.join()](#sqlalchemy.sql.expression.Select.join) now creates
a [Join](#sqlalchemy.sql.expression.Join) object between a [FromClause](#sqlalchemy.sql.expression.FromClause)
source that is within the FROM clause of the existing SELECT,
and a given target [FromClause](#sqlalchemy.sql.expression.FromClause), and then adds
this [Join](#sqlalchemy.sql.expression.Join) to the FROM clause of the newly generated
SELECT statement.    This is completely reworked from the behavior
in 1.3, which would instead create a subquery of the entire
[Select](#sqlalchemy.sql.expression.Select) and then join that subquery to the
target.

This is a **backwards incompatible change** as the previous behavior
was mostly useless, producing an unnamed subquery rejected by
most databases in any case.   The new behavior is modeled after
that of the very successful [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) method in the
ORM, in order to support the functionality of [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
being available by using a [Select](#sqlalchemy.sql.expression.Select) object with an
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

See the notes for this change at [select().join() and outerjoin() add JOIN criteria to the current query, rather than creating a subquery](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-select-join).

   Parameters:

- **target** – target table to join towards
- **onclause** – ON clause of the join.  If omitted, an ON clause
  is generated automatically based on the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)
  linkages between the two tables, if one can be unambiguously
  determined, otherwise an error is raised.
- **isouter** – if True, generate LEFT OUTER join.  Same as
  [Select.outerjoin()](#sqlalchemy.sql.expression.Select.outerjoin).
- **full** – if True, generate FULL OUTER join.

See also

[Explicit FROM clauses and JOINs](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-select-join) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

[Joins](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-joins) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Select.join_from()](#sqlalchemy.sql.expression.Select.join_from)

[Select.outerjoin()](#sqlalchemy.sql.expression.Select.outerjoin)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)join_from(*from_:_FromClauseArgument*, *target:_JoinTargetArgument*, *onclause:_OnClauseArgument|None=None*, ***, *isouter:bool=False*, *full:bool=False*) → Self

Create a SQL JOIN against this [Select](#sqlalchemy.sql.expression.Select)
object’s criterion
and apply generatively, returning the newly resulting
[Select](#sqlalchemy.sql.expression.Select).

E.g.:

```
stmt = select(user_table, address_table).join_from(
    user_table, address_table, user_table.c.id == address_table.c.user_id
)
```

The above statement generates SQL similar to:

```
SELECT user.id, user.name, address.id, address.email, address.user_id
FROM user JOIN address ON user.id = address.user_id
```

Added in version 1.4.

   Parameters:

- **from_** – the left side of the join, will be rendered in the
  FROM clause and is roughly equivalent to using the
  [Select.select_from()](#sqlalchemy.sql.expression.Select.select_from) method.
- **target** – target table to join towards
- **onclause** – ON clause of the join.
- **isouter** – if True, generate LEFT OUTER join.  Same as
  [Select.outerjoin()](#sqlalchemy.sql.expression.Select.outerjoin).
- **full** – if True, generate FULL OUTER join.

See also

[Explicit FROM clauses and JOINs](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-select-join) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

[Joins](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-joins) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Select.join()](#sqlalchemy.sql.expression.Select.join)

     property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)label(*name:str|None*) → [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label)[Any]

*inherited from the* [SelectBase.label()](#sqlalchemy.sql.expression.SelectBase.label) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a ‘scalar’ representation of this selectable, embedded as a
subquery with a label.

See also

[SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)lateral(*name:str|None=None*) → LateralFromClause

*inherited from the* [SelectBase.lateral()](#sqlalchemy.sql.expression.SelectBase.lateral) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a LATERAL alias of this [Selectable](#sqlalchemy.sql.expression.Selectable).

The return value is the [Lateral](#sqlalchemy.sql.expression.Lateral) construct also
provided by the top-level [lateral()](#sqlalchemy.sql.expression.lateral) function.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)limit(*limit:_LimitOffsetType*) → Self

*inherited from the* [GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given LIMIT criterion
applied.

This is a numerical value which usually renders as a `LIMIT`
expression in the resulting select.  Backends that don’t
support `LIMIT` will attempt to provide similar
functionality.

Note

The [GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit) method will replace
any clause applied with [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch).

   Parameters:

**limit** – an integer LIMIT parameter, or a SQL expression
that provides an integer result. Pass `None` to reset it.

See also

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

     attribute [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)name_cte_columns = False

*inherited from the* [HasCTE.name_cte_columns](#sqlalchemy.sql.expression.HasCTE.name_cte_columns) *attribute of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause.

Added in version 2.0.42.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)offset(*offset:_LimitOffsetType*) → Self

*inherited from the* [GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given OFFSET criterion
applied.

This is a numeric value which usually renders as an `OFFSET`
expression in the resulting select.  Backends that don’t
support `OFFSET` will attempt to provide similar
functionality.

  Parameters:

**offset** – an integer OFFSET parameter, or a SQL expression
that provides an integer result. Pass `None` to reset it.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)options(**options:ExecutableOption*) → Self

*inherited from the* [Executable.options()](#sqlalchemy.sql.expression.Executable.options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Apply options to this statement.

In the general sense, options are any kind of Python object
that can be interpreted by the SQL compiler for the statement.
These options can be consumed by specific dialects or specific kinds
of compilers.

The most commonly known kind of option are the ORM level options
that apply “eager load” and other loading behaviors to an ORM
query.   However, options can theoretically be used for many other
purposes.

For background on specific kinds of options for specific kinds of
statements, refer to the documentation for those option objects.

Changed in version 1.4: - added [Executable.options()](#sqlalchemy.sql.expression.Executable.options) to
Core statement objects towards the goal of allowing unified
Core / ORM querying capabilities.

See also

[Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#loading-columns) - refers to options specific to the usage
of ORM queries

[Relationship Loading with Loader Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#relationship-loader-options) - refers to options specific
to the usage of ORM queries

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)order_by(*_GenerativeSelect__first:Literal[None,_NoArg.NO_ARG]|_ColumnExpressionOrStrLabelArgument[Any]=_NoArg.NO_ARG*, **clauses:_ColumnExpressionOrStrLabelArgument[Any]*) → Self

*inherited from the* [GenerativeSelect.order_by()](#sqlalchemy.sql.expression.GenerativeSelect.order_by) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the given list of ORDER BY
criteria applied.

e.g.:

```
stmt = select(table).order_by(table.c.id, table.c.name)
```

Calling this method multiple times is equivalent to calling it once
with all the clauses concatenated. All existing ORDER BY criteria may
be cancelled by passing `None` by itself.  New ORDER BY criteria may
then be added by invoking [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) again, e.g.:

```
# will erase all ORDER BY and ORDER BY new_col alone
stmt = stmt.order_by(None).order_by(new_col)
```

   Parameters:

***clauses** –

a series of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
constructs which will be used to generate an ORDER BY clause.

Alternatively, an individual entry may also be the string name of a
label located elsewhere in the columns clause of the statement which
will be matched and rendered in a backend-specific way based on
context; see [Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) for background on string
label matching in ORDER BY and GROUP BY expressions.

See also

[ORDER BY](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)outerjoin(*target:_JoinTargetArgument*, *onclause:_OnClauseArgument|None=None*, ***, *full:bool=False*) → Self

Create a left outer join.

Parameters are the same as that of [Select.join()](#sqlalchemy.sql.expression.Select.join).

Changed in version 1.4: [Select.outerjoin()](#sqlalchemy.sql.expression.Select.outerjoin) now
creates a [Join](#sqlalchemy.sql.expression.Join) object between a
[FromClause](#sqlalchemy.sql.expression.FromClause) source that is within the FROM clause of
the existing SELECT, and a given target [FromClause](#sqlalchemy.sql.expression.FromClause),
and then adds this [Join](#sqlalchemy.sql.expression.Join) to the FROM clause of the
newly generated SELECT statement.    This is completely reworked
from the behavior in 1.3, which would instead create a subquery of
the entire
[Select](#sqlalchemy.sql.expression.Select) and then join that subquery to the
target.

This is a **backwards incompatible change** as the previous behavior
was mostly useless, producing an unnamed subquery rejected by
most databases in any case.   The new behavior is modeled after
that of the very successful [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) method in the
ORM, in order to support the functionality of [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
being available by using a [Select](#sqlalchemy.sql.expression.Select) object with an
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

See the notes for this change at [select().join() and outerjoin() add JOIN criteria to the current query, rather than creating a subquery](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-select-join).

See also

[Explicit FROM clauses and JOINs](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-select-join) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

[Joins](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-joins) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Select.join()](#sqlalchemy.sql.expression.Select.join)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)outerjoin_from(*from_:_FromClauseArgument*, *target:_JoinTargetArgument*, *onclause:_OnClauseArgument|None=None*, ***, *full:bool=False*) → Self

Create a SQL LEFT OUTER JOIN against this
[Select](#sqlalchemy.sql.expression.Select) object’s criterion and apply generatively,
returning the newly resulting [Select](#sqlalchemy.sql.expression.Select).

Usage is the same as that of `Select.join_from()`.

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)prefix_with(**prefixes:_TextCoercedExpressionArgument[Any]*, *dialect:str='*'*) → Self

*inherited from the* [HasPrefixes.prefix_with()](#sqlalchemy.sql.expression.HasPrefixes.prefix_with) *method of* [HasPrefixes](#sqlalchemy.sql.expression.HasPrefixes)

Add one or more expressions following the statement keyword, i.e.
SELECT, INSERT, UPDATE, or DELETE. Generative.

This is used to support backend-specific prefix keywords such as those
provided by MySQL.

E.g.:

```
stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

# MySQL 5.7 optimizer hints
stmt = select(table).prefix_with("/*+ BKA(t1) */", dialect="mysql")
```

Multiple prefixes can be specified by multiple calls
to [HasPrefixes.prefix_with()](#sqlalchemy.sql.expression.HasPrefixes.prefix_with).

  Parameters:

- ***prefixes** – textual or [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  construct which
  will be rendered following the INSERT, UPDATE, or DELETE
  keyword.
- **dialect** – optional string dialect name which will
  limit rendering of this prefix to only that dialect.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)reduce_columns(*only_synonyms:bool=True*) → [Select](#sqlalchemy.sql.expression.Select)

Return a new [select()](#sqlalchemy.sql.expression.select) construct with redundantly
named, equivalently-valued columns removed from the columns clause.

“Redundant” here means two columns where one refers to the
other either based on foreign key, or via a simple equality
comparison in the WHERE clause of the statement.   The primary purpose
of this method is to automatically construct a select statement
with all uniquely-named columns, without the need to use
table-qualified labels as
[Select.set_label_style()](#sqlalchemy.sql.expression.Select.set_label_style)
does.

When columns are omitted based on foreign key, the referred-to
column is the one that’s kept.  When columns are omitted based on
WHERE equivalence, the first column in the columns clause is the
one that’s kept.

  Parameters:

**only_synonyms** – when True, limit the removal of columns
to those which have the same name as the equivalent.   Otherwise,
all columns that are equivalent to another are removed.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)replace_selectable(*old:FromClause*, *alias:Alias*) → Self

*inherited from the* [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Replace all occurrences of [FromClause](#sqlalchemy.sql.expression.FromClause)
‘old’ with the given [Alias](#sqlalchemy.sql.expression.Alias)
object, returning a copy of this [FromClause](#sqlalchemy.sql.expression.FromClause).

Deprecated since version 1.4: The [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) method is deprecated, and will be removed in a future release.  Similar functionality is available via the sqlalchemy.sql.visitors module.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)scalar_subquery() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

*inherited from the* [SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a ‘scalar’ representation of this selectable, which can be
used as a column expression.

The returned object is an instance of [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect).

Typically, a select statement which has only one column in its columns
clause is eligible to be used as a scalar expression.  The scalar
subquery can then be used in the WHERE clause or columns clause of
an enclosing SELECT.

Note that the scalar subquery differentiates from the FROM-level
subquery that can be produced using the
[SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
method.

See also

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery) - in the 2.0 tutorial

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)select(**arg:Any*, ***kw:Any*) → [Select](#sqlalchemy.sql.expression.Select)

*inherited from the* [SelectBase.select()](#sqlalchemy.sql.expression.SelectBase.select) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Deprecated since version 1.4: The [SelectBase.select()](#sqlalchemy.sql.expression.SelectBase.select) method is deprecated and will be removed in a future release; this method implicitly creates a subquery that should be explicit.  Please call [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) first in order to create a subquery, which then can be selected.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)select_from(**froms:_FromClauseArgument*) → Self

Return a new [select()](#sqlalchemy.sql.expression.select) construct with the
given FROM expression(s)
merged into its list of FROM objects.

E.g.:

```
table1 = table("t1", column("a"))
table2 = table("t2", column("b"))
s = select(table1.c.a).select_from(
    table1.join(table2, table1.c.a == table2.c.b)
)
```

The “from” list is a unique set on the identity of each element,
so adding an already present [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
or other selectable
will have no effect.   Passing a [Join](#sqlalchemy.sql.expression.Join) that refers
to an already present [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
or other selectable will have
the effect of concealing the presence of that selectable as
an individual element in the rendered FROM list, instead
rendering it into a JOIN clause.

While the typical purpose of [Select.select_from()](#sqlalchemy.sql.expression.Select.select_from)
is to
replace the default, derived FROM clause with a join, it can
also be called with individual table elements, multiple times
if desired, in the case that the FROM clause cannot be fully
derived from the columns clause:

```
select(func.count("*")).select_from(table1)
```

     attribute [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)selected_columns

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
representing the columns that
this SELECT statement or similar construct returns in its result set,
not including [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) constructs.

This collection differs from the [FromClause.columns](#sqlalchemy.sql.expression.FromClause.columns)
collection of a [FromClause](#sqlalchemy.sql.expression.FromClause) in that the columns
within this collection cannot be directly nested inside another SELECT
statement; a subquery must be applied first which provides for the
necessary parenthesization required by SQL.

For a [select()](#sqlalchemy.sql.expression.select) construct, the collection here is
exactly what would be rendered inside the “SELECT” statement, and the
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects are directly present as they
were given, e.g.:

```
col1 = column("q", Integer)
col2 = column("p", Integer)
stmt = select(col1, col2)
```

Above, `stmt.selected_columns` would be a collection that contains
the `col1` and `col2` objects directly. For a statement that is
against a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or other
[FromClause](#sqlalchemy.sql.expression.FromClause), the collection will use the
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects that are in the
[FromClause.c](#sqlalchemy.sql.expression.FromClause.c) collection of the from element.

A use case for the [Select.selected_columns](#sqlalchemy.sql.expression.Select.selected_columns) collection is
to allow the existing columns to be referenced when adding additional
criteria, e.g.:

```
def filter_on_id(my_select, id):
    return my_select.where(my_select.selected_columns["id"] == id)

stmt = select(MyModel)

# adds "WHERE id=:param" to the statement
stmt = filter_on_id(stmt, 42)
```

Note

The [Select.selected_columns](#sqlalchemy.sql.expression.Select.selected_columns) collection does not
include expressions established in the columns clause using the
[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct; these are silently omitted from the
collection. To use plain textual column expressions inside of a
[Select](#sqlalchemy.sql.expression.Select) construct, use the [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column)
construct.

Added in version 1.4.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)self_group(*against:OperatorType|None=None*) → SelectStatementGrouping | Self

Return a ‘grouping’ construct as per the
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) specification.

This produces an element that can be embedded in an expression. Note
that this method is called automatically as needed when constructing
expressions and should not require explicit use.

    method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)set_label_style(*style:SelectLabelStyle*) → Self

*inherited from the* [GenerativeSelect.set_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.set_label_style) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Return a new selectable with the specified label style.

There are three “label styles” available,
[SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY),
[SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL), and
[SelectLabelStyle.LABEL_STYLE_NONE](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_NONE).   The default style is
[SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY](#sqlalchemy.sql.expression.SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY).

In modern SQLAlchemy, there is not generally a need to change the
labeling style, as per-expression labels are more effectively used by
making use of the [ColumnElement.label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label) method. In past
versions, `LABEL_STYLE_TABLENAME_PLUS_COL` was used to
disambiguate same-named columns from different tables, aliases, or
subqueries; the newer `LABEL_STYLE_DISAMBIGUATE_ONLY` now
applies labels only to names that conflict with an existing name so
that the impact of this labeling is minimal.

The rationale for disambiguation is mostly so that all column
expressions are available from a given [FromClause.c](#sqlalchemy.sql.expression.FromClause.c)
collection when a subquery is created.

Added in version 1.4: - the
[GenerativeSelect.set_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.set_label_style) method replaces the
previous combination of `.apply_labels()`, `.with_labels()` and
`use_labels=True` methods and/or parameters.

See also

`LABEL_STYLE_DISAMBIGUATE_ONLY`

`LABEL_STYLE_TABLENAME_PLUS_COL`

`LABEL_STYLE_NONE`

`LABEL_STYLE_DEFAULT`

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)slice(*start:int*, *stop:int*) → Self

*inherited from the* [GenerativeSelect.slice()](#sqlalchemy.sql.expression.GenerativeSelect.slice) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Apply LIMIT / OFFSET to this statement based on a slice.

The start and stop indices behave like the argument to Python’s
built-in `range()` function. This method provides an
alternative to using `LIMIT`/`OFFSET` to get a slice of the
query.

For example,

```
stmt = select(User).order_by(User.id).slice(1, 3)
```

renders as

```
SELECT users.id AS users_id,
       users.name AS users_name
FROM users ORDER BY users.id
LIMIT ? OFFSET ?
(2, 1)
```

Note

The [GenerativeSelect.slice()](#sqlalchemy.sql.expression.GenerativeSelect.slice) method will replace
any clause applied with [GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch).

Added in version 1.4: Added the [GenerativeSelect.slice()](#sqlalchemy.sql.expression.GenerativeSelect.slice)
method generalized from the ORM.

See also

[GenerativeSelect.limit()](#sqlalchemy.sql.expression.GenerativeSelect.limit)

[GenerativeSelect.offset()](#sqlalchemy.sql.expression.GenerativeSelect.offset)

[GenerativeSelect.fetch()](#sqlalchemy.sql.expression.GenerativeSelect.fetch)

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)subquery(*name:str|None=None*) → [Subquery](#sqlalchemy.sql.expression.Subquery)

*inherited from the* [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a subquery of this [SelectBase](#sqlalchemy.sql.expression.SelectBase).

A subquery is from a SQL perspective a parenthesized, named
construct that can be placed in the FROM clause of another
SELECT statement.

Given a SELECT statement such as:

```
stmt = select(table.c.id, table.c.name)
```

The above statement might look like:

```
SELECT table.id, table.name FROM table
```

The subquery form by itself renders the same way, however when
embedded into the FROM clause of another SELECT statement, it becomes
a named sub-element:

```
subq = stmt.subquery()
new_stmt = select(subq)
```

The above renders as:

```
SELECT anon_1.id, anon_1.name
FROM (SELECT table.id, table.name FROM table) AS anon_1
```

Historically, [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
is equivalent to calling
the [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias)
method on a FROM object; however,
as a [SelectBase](#sqlalchemy.sql.expression.SelectBase)
object is not directly  FROM object,
the [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
method provides clearer semantics.

Added in version 1.4.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)suffix_with(**suffixes:_TextCoercedExpressionArgument[Any]*, *dialect:str='*'*) → Self

*inherited from the* [HasSuffixes.suffix_with()](#sqlalchemy.sql.expression.HasSuffixes.suffix_with) *method of* [HasSuffixes](#sqlalchemy.sql.expression.HasSuffixes)

Add one or more expressions following the statement as a whole.

This is used to support backend-specific suffix keywords on
certain constructs.

E.g.:

```
stmt = (
    select(col1, col2)
    .cte()
    .suffix_with(
        "cycle empno set y_cycle to 1 default 0", dialect="oracle"
    )
)
```

Multiple suffixes can be specified by multiple calls
to [HasSuffixes.suffix_with()](#sqlalchemy.sql.expression.HasSuffixes.suffix_with).

  Parameters:

- ***suffixes** – textual or [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  construct which
  will be rendered following the target clause.
- **dialect** – Optional string dialect name which will
  limit rendering of this suffix to only that dialect.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)union(**other:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return a SQL `UNION` of this select() construct against
the given selectables provided as positional arguments.

  Parameters:

- ***other** –
  one or more elements with which to create a
  UNION.
  Changed in version 1.4.28: multiple elements are now accepted.
- ****kwargs** – keyword arguments are forwarded to the constructor
  for the newly created [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect) object.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)union_all(**other:_SelectStatementForCompoundArgument[_TP]*) → [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect)[_TP]

Return a SQL `UNION ALL` of this select() construct against
the given selectables provided as positional arguments.

  Parameters:

- ***other** –
  one or more elements with which to create a
  UNION.
  Changed in version 1.4.28: multiple elements are now accepted.
- ****kwargs** – keyword arguments are forwarded to the constructor
  for the newly created [CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect) object.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)where(**whereclause:_ColumnExpressionArgument[bool]*) → Self

Return a new [select()](#sqlalchemy.sql.expression.select) construct with
the given expression added to
its WHERE clause, joined to the existing clause via AND, if any.

    property whereclause: [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any] | None

Return the completed WHERE clause for this
[Select](#sqlalchemy.sql.expression.Select) statement.

This assembles the current collection of WHERE criteria
into a single `BooleanClauseList` construct.

Added in version 1.4.

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)with_for_update(***, *nowait:bool=False*, *read:bool=False*, *of:_ForUpdateOfArgument|None=None*, *skip_locked:bool=False*, *key_share:bool=False*) → Self

*inherited from the* [GenerativeSelect.with_for_update()](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update) *method of* [GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect)

Specify a `FOR UPDATE` clause for this
[GenerativeSelect](#sqlalchemy.sql.expression.GenerativeSelect).

E.g.:

```
stmt = select(table).with_for_update(nowait=True)
```

On a database like PostgreSQL or Oracle Database, the above would
render a statement like:

```
SELECT table.a, table.b FROM table FOR UPDATE NOWAIT
```

on other backends, the `nowait` option is ignored and instead
would produce:

```
SELECT table.a, table.b FROM table FOR UPDATE
```

When called with no arguments, the statement will render with
the suffix `FOR UPDATE`.   Additional arguments can then be
provided which allow for common database-specific
variants.

  Parameters:

- **nowait** – boolean; will render `FOR UPDATE NOWAIT` on Oracle
  Database and PostgreSQL dialects.
- **read** – boolean; will render `LOCK IN SHARE MODE` on MySQL,
  `FOR SHARE` on PostgreSQL.  On PostgreSQL, when combined with
  `nowait`, will render `FOR SHARE NOWAIT`.
- **of** – SQL expression or list of SQL expression elements,
  (typically [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects or a compatible expression,
  for some backends may also be a table expression) which will render
  into a `FOR UPDATE OF` clause; supported by PostgreSQL, Oracle
  Database, some MySQL versions and possibly others. May render as a
  table or as a column depending on backend.
- **skip_locked** – boolean, will render `FOR UPDATE SKIP LOCKED` on
  Oracle Database and PostgreSQL dialects or `FOR SHARE SKIP LOCKED`
  if `read=True` is also specified.
- **key_share** – boolean, will render `FOR NO KEY UPDATE`,
  or if combined with `read=True` will render `FOR KEY SHARE`,
  on the PostgreSQL dialect.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)with_hint(*selectable:_FromClauseArgument*, *text:str*, *dialect_name:str='*'*) → Self

*inherited from the* `HasHints.with_hint()` *method of* `HasHints`

Add an indexing or other executional context hint for the given
selectable to this [Select](#sqlalchemy.sql.expression.Select) or other selectable
object.

Tip

The [Select.with_hint()](#sqlalchemy.sql.expression.Select.with_hint) method adds hints that are
**specific to a single table** to a statement, in a location that
is **dialect-specific**.  To add generic optimizer hints to the
**beginning** of a statement ahead of the SELECT keyword such as
for MySQL or Oracle Database, use the
[Select.prefix_with()](#sqlalchemy.sql.expression.Select.prefix_with) method.  To add optimizer
hints to the **end** of a statement such as for PostgreSQL, use the
[Select.with_statement_hint()](#sqlalchemy.sql.expression.Select.with_statement_hint) method.

The text of the hint is rendered in the appropriate
location for the database backend in use, relative
to the given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [Alias](#sqlalchemy.sql.expression.Alias)
passed as the
`selectable` argument. The dialect implementation
typically uses Python string substitution syntax
with the token `%(name)s` to render the name of
the table or alias. E.g. when using Oracle Database, the
following:

```
select(mytable).with_hint(mytable, "index(%(name)s ix_mytable)")
```

Would render SQL as:

```
select /*+ index(mytable ix_mytable) */ ... from mytable
```

The `dialect_name` option will limit the rendering of a particular
hint to a particular backend. Such as, to add hints for both Oracle
Database and MSSql simultaneously:

```
select(mytable).with_hint(
    mytable, "index(%(name)s ix_mytable)", "oracle"
).with_hint(mytable, "WITH INDEX ix_mytable", "mssql")
```

See also

[Select.with_statement_hint()](#sqlalchemy.sql.expression.Select.with_statement_hint)

[Select.prefix_with()](#sqlalchemy.sql.expression.Select.prefix_with) - generic SELECT prefixing
which also can suit some database-specific HINT syntaxes such as
MySQL or Oracle Database optimizer hints

     method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)with_only_columns(**entities:_ColumnsClauseArgument[Any]*, *maintain_column_froms:bool=False*, ***_Select__kw:Any*) → [Select](#sqlalchemy.sql.expression.Select)[Any]

Return a new [select()](#sqlalchemy.sql.expression.select) construct with its columns
clause replaced with the given entities.

By default, this method is exactly equivalent to as if the original
[select()](#sqlalchemy.sql.expression.select) had been called with the given entities.
E.g. a statement:

```
s = select(table1.c.a, table1.c.b)
s = s.with_only_columns(table1.c.b)
```

should be exactly equivalent to:

```
s = select(table1.c.b)
```

In this mode of operation, [Select.with_only_columns()](#sqlalchemy.sql.expression.Select.with_only_columns)
will also dynamically alter the FROM clause of the
statement if it is not explicitly stated.
To maintain the existing set of FROMs including those implied by the
current columns clause, add the
[Select.with_only_columns.maintain_column_froms](#sqlalchemy.sql.expression.Select.with_only_columns.params.maintain_column_froms)
parameter:

```
s = select(table1.c.a, table2.c.b)
s = s.with_only_columns(table1.c.a, maintain_column_froms=True)
```

The above parameter performs a transfer of the effective FROMs
in the columns collection to the [Select.select_from()](#sqlalchemy.sql.expression.Select.select_from)
method, as though the following were invoked:

```
s = select(table1.c.a, table2.c.b)
s = s.select_from(table1, table2).with_only_columns(table1.c.a)
```

The [Select.with_only_columns.maintain_column_froms](#sqlalchemy.sql.expression.Select.with_only_columns.params.maintain_column_froms)
parameter makes use of the [Select.columns_clause_froms](#sqlalchemy.sql.expression.Select.columns_clause_froms)
collection and performs an operation equivalent to the following:

```
s = select(table1.c.a, table2.c.b)
s = s.select_from(*s.columns_clause_froms).with_only_columns(table1.c.a)
```

   Parameters:

- ***entities** – column expressions to be used.
- **maintain_column_froms** –
  boolean parameter that will ensure the
  FROM list implied from the current columns clause will be transferred
  to the [Select.select_from()](#sqlalchemy.sql.expression.Select.select_from) method first.
  Added in version 1.4.23.

      method [sqlalchemy.sql.expression.Select.](#sqlalchemy.sql.expression.Select)with_statement_hint(*text:str*, *dialect_name:str='*'*) → Self

*inherited from the* `HasHints.with_statement_hint()` *method of* `HasHints`

Add a statement hint to this [Select](#sqlalchemy.sql.expression.Select) or
other selectable object.

Tip

[Select.with_statement_hint()](#sqlalchemy.sql.expression.Select.with_statement_hint) generally adds hints
**at the trailing end** of a SELECT statement.  To place
dialect-specific hints such as optimizer hints at the **front** of
the SELECT statement after the SELECT keyword, use the
[Select.prefix_with()](#sqlalchemy.sql.expression.Select.prefix_with) method for an open-ended
space, or for table-specific hints the
[Select.with_hint()](#sqlalchemy.sql.expression.Select.with_hint) may be used, which places
hints in a dialect-specific location.

This method is similar to [Select.with_hint()](#sqlalchemy.sql.expression.Select.with_hint) except
that it does not require an individual table, and instead applies to
the statement as a whole.

Hints here are specific to the backend database and may include
directives such as isolation levels, file directives, fetch directives,
etc.

See also

[Select.with_hint()](#sqlalchemy.sql.expression.Select.with_hint)

[Select.prefix_with()](#sqlalchemy.sql.expression.Select.prefix_with) - generic SELECT prefixing
which also can suit some database-specific HINT syntaxes such as
MySQL or Oracle Database optimizer hints

      class sqlalchemy.sql.expression.Selectable

*inherits from* [sqlalchemy.sql.expression.ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows)

Mark a class as being selectable.

| Member Name | Description |
| --- | --- |
| compile() | Compile this SQL expression. |
| corresponding_column() | Given aColumnElement, return the exportedColumnElementobject from theSelectable.exported_columnscollection of thisSelectablewhich corresponds to that
originalColumnElementvia a common ancestor
column. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| is_derived_from() | ReturnTrueif thisReturnsRowsis
‘derived’ from the givenFromClause. |
| lateral() | Return a LATERAL alias of thisSelectable. |
| replace_selectable() | Replace all occurrences ofFromClause‘old’ with the givenAliasobject, returning a copy of thisFromClause. |

   method [sqlalchemy.sql.expression.Selectable.](#sqlalchemy.sql.expression.Selectable)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

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

     method [sqlalchemy.sql.expression.Selectable.](#sqlalchemy.sql.expression.Selectable)corresponding_column(*column:KeyedColumnElement[Any]*, *require_embedded:bool=False*) → KeyedColumnElement[Any] | None

Given a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), return the exported
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) object from the
[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)
collection of this [Selectable](#sqlalchemy.sql.expression.Selectable)
which corresponds to that
original [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) via a common ancestor
column.

  Parameters:

- **column** – the target [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  to be matched.
- **require_embedded** – only return corresponding columns for
  the given [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), if the given
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  is actually present within a sub-element
  of this [Selectable](#sqlalchemy.sql.expression.Selectable).
  Normally the column will match if
  it merely shares a common ancestor with one of the exported
  columns of this [Selectable](#sqlalchemy.sql.expression.Selectable).

See also

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns) - the
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that is used for the operation.

[ColumnCollection.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.corresponding_column)
- implementation
method.

     property exported_columns: ReadOnlyColumnCollection[Any, Any]

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows).

The “exported” columns represent the collection of
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
expressions that are rendered by this SQL
construct.   There are primary varieties which are the
“FROM clause columns” of a FROM clause, such as a table, join,
or subquery, the “SELECTed columns”, which are the columns in
the “columns clause” of a SELECT statement, and the RETURNING
columns in a DML statement..

Added in version 1.4.

See also

[FromClause.exported_columns](#sqlalchemy.sql.expression.FromClause.exported_columns)

[SelectBase.exported_columns](#sqlalchemy.sql.expression.SelectBase.exported_columns)

     method [sqlalchemy.sql.expression.Selectable.](#sqlalchemy.sql.expression.Selectable)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    attribute [sqlalchemy.sql.expression.Selectable.](#sqlalchemy.sql.expression.Selectable)inherit_cache = None

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

     method [sqlalchemy.sql.expression.Selectable.](#sqlalchemy.sql.expression.Selectable)is_derived_from(*fromclause:FromClause|None*) → bool

*inherited from the* [ReturnsRows.is_derived_from()](#sqlalchemy.sql.expression.ReturnsRows.is_derived_from) *method of* [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows)

Return `True` if this [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows) is
‘derived’ from the given [FromClause](#sqlalchemy.sql.expression.FromClause).

An example would be an Alias of a Table is derived from that Table.

    method [sqlalchemy.sql.expression.Selectable.](#sqlalchemy.sql.expression.Selectable)lateral(*name:str|None=None*) → LateralFromClause

Return a LATERAL alias of this [Selectable](#sqlalchemy.sql.expression.Selectable).

The return value is the [Lateral](#sqlalchemy.sql.expression.Lateral) construct also
provided by the top-level [lateral()](#sqlalchemy.sql.expression.lateral) function.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

     method [sqlalchemy.sql.expression.Selectable.](#sqlalchemy.sql.expression.Selectable)replace_selectable(*old:FromClause*, *alias:Alias*) → Self

Replace all occurrences of [FromClause](#sqlalchemy.sql.expression.FromClause)
‘old’ with the given [Alias](#sqlalchemy.sql.expression.Alias)
object, returning a copy of this [FromClause](#sqlalchemy.sql.expression.FromClause).

Deprecated since version 1.4: The [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) method is deprecated, and will be removed in a future release.  Similar functionality is available via the sqlalchemy.sql.visitors module.

      class sqlalchemy.sql.expression.SelectBase

*inherits from* `sqlalchemy.sql.roles.SelectStatementRole`, `sqlalchemy.sql.roles.DMLSelectRole`, `sqlalchemy.sql.roles.CompoundElementRole`, `sqlalchemy.sql.roles.InElementRole`, [sqlalchemy.sql.expression.HasCTE](#sqlalchemy.sql.expression.HasCTE), `sqlalchemy.sql.annotation.SupportsCloneAnnotations`, [sqlalchemy.sql.expression.Selectable](#sqlalchemy.sql.expression.Selectable)

Base class for SELECT statements.

This includes [Select](#sqlalchemy.sql.expression.Select),
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect) and
[TextualSelect](#sqlalchemy.sql.expression.TextualSelect).

| Member Name | Description |
| --- | --- |
| add_cte() | Add one or moreCTEconstructs to this statement. |
| alias() | Return a named subquery against thisSelectBase. |
| as_scalar() |  |
| compile() | Compile this SQL expression. |
| corresponding_column() | Given aColumnElement, return the exportedColumnElementobject from theSelectable.exported_columnscollection of thisSelectablewhich corresponds to that
originalColumnElementvia a common ancestor
column. |
| cte() | Return a newCTE,
or Common Table Expression instance. |
| exists() | Return anExistsrepresentation of this selectable,
which can be used as a column expression. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| get_label_style() | Retrieve the current label style. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| is_derived_from() | ReturnTrueif thisReturnsRowsis
‘derived’ from the givenFromClause. |
| label() | Return a ‘scalar’ representation of this selectable, embedded as a
subquery with a label. |
| lateral() | Return a LATERAL alias of thisSelectable. |
| name_cte_columns | indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause. |
| replace_selectable() | Replace all occurrences ofFromClause‘old’ with the givenAliasobject, returning a copy of thisFromClause. |
| scalar_subquery() | Return a ‘scalar’ representation of this selectable, which can be
used as a column expression. |
| select() |  |
| selected_columns | AColumnCollectionrepresenting the columns that
this SELECT statement or similar construct returns in its result set. |
| set_label_style() | Return a new selectable with the specified label style. |
| subquery() | Return a subquery of thisSelectBase. |

   method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)add_cte(**ctes:CTE*, *nest_here:bool=False*) → Self

*inherited from the* [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Add one or more [CTE](#sqlalchemy.sql.expression.CTE) constructs to this statement.

This method will associate the given [CTE](#sqlalchemy.sql.expression.CTE) constructs with
the parent statement such that they will each be unconditionally
rendered in the WITH clause of the final statement, even if not
referenced elsewhere within the statement or any sub-selects.

The optional [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here) parameter when set
to True will have the effect that each given [CTE](#sqlalchemy.sql.expression.CTE) will
render in a WITH clause rendered directly along with this statement,
rather than being moved to the top of the ultimate rendered statement,
even if this statement is rendered as a subquery within a larger
statement.

This method has two general uses. One is to embed CTE statements that
serve some purpose without being referenced explicitly, such as the use
case of embedding a DML statement such as an INSERT or UPDATE as a CTE
inline with a primary statement that may draw from its results
indirectly.  The other is to provide control over the exact placement
of a particular series of CTE constructs that should remain rendered
directly in terms of a particular statement that may be nested in a
larger statement.

E.g.:

```
from sqlalchemy import table, column, select

t = table("t", column("c1"), column("c2"))

ins = t.insert().values({"c1": "x", "c2": "y"}).cte()

stmt = select(t).add_cte(ins)
```

Would render:

```
WITH anon_1 AS (
    INSERT INTO t (c1, c2) VALUES (:param_1, :param_2)
)
SELECT t.c1, t.c2
FROM t
```

Above, the “anon_1” CTE is not referenced in the SELECT
statement, however still accomplishes the task of running an INSERT
statement.

Similarly in a DML-related context, using the PostgreSQL
[Insert](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert) construct to generate an “upsert”:

```
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import insert

t = table("t", column("c1"), column("c2"))

delete_statement_cte = t.delete().where(t.c.c1 < 1).cte("deletions")

insert_stmt = insert(t).values({"c1": 1, "c2": 2})
update_statement = insert_stmt.on_conflict_do_update(
    index_elements=[t.c.c1],
    set_={
        "c1": insert_stmt.excluded.c1,
        "c2": insert_stmt.excluded.c2,
    },
).add_cte(delete_statement_cte)

print(update_statement)
```

The above statement renders as:

```
WITH deletions AS (
    DELETE FROM t WHERE t.c1 < %(c1_1)s
)
INSERT INTO t (c1, c2) VALUES (%(c1)s, %(c2)s)
ON CONFLICT (c1) DO UPDATE SET c1 = excluded.c1, c2 = excluded.c2
```

Added in version 1.4.21.

   Parameters:

- ***ctes** –
  zero or more [CTE](#sqlalchemy.sql.expression.CTE) constructs.
  Changed in version 2.0: Multiple CTE instances are accepted
- **nest_here** –
  if True, the given CTE or CTEs will be rendered
  as though they specified the [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting) flag
  to `True` when they were added to this [HasCTE](#sqlalchemy.sql.expression.HasCTE).
  Assuming the given CTEs are not referenced in an outer-enclosing
  statement as well, the CTEs given should render at the level of
  this statement when this flag is given.
  Added in version 2.0.
  See also
  [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting)

      method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)alias(*name:str|None=None*, *flat:bool=False*) → [Subquery](#sqlalchemy.sql.expression.Subquery)

Return a named subquery against this
[SelectBase](#sqlalchemy.sql.expression.SelectBase).

For a [SelectBase](#sqlalchemy.sql.expression.SelectBase) (as opposed to a
[FromClause](#sqlalchemy.sql.expression.FromClause)),
this returns a [Subquery](#sqlalchemy.sql.expression.Subquery) object which behaves mostly the
same as the [Alias](#sqlalchemy.sql.expression.Alias) object that is used with a
[FromClause](#sqlalchemy.sql.expression.FromClause).

Changed in version 1.4: The [SelectBase.alias()](#sqlalchemy.sql.expression.SelectBase.alias)
method is now
a synonym for the [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) method.

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)as_scalar() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

Deprecated since version 1.4: The [SelectBase.as_scalar()](#sqlalchemy.sql.expression.SelectBase.as_scalar) method is deprecated and will be removed in a future release.  Please refer to [SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

     property c: ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]

Deprecated since version 1.4: The [SelectBase.c](#sqlalchemy.sql.expression.SelectBase.c) and `SelectBase.columns` attributes are deprecated and will be removed in a future release; these attributes implicitly create a subquery that should be explicit.  Please call [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) first in order to create a subquery, which then contains this attribute.  To access the columns that this SELECT object SELECTs from, use the [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) attribute.

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

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

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)corresponding_column(*column:KeyedColumnElement[Any]*, *require_embedded:bool=False*) → KeyedColumnElement[Any] | None

*inherited from the* [Selectable.corresponding_column()](#sqlalchemy.sql.expression.Selectable.corresponding_column) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Given a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), return the exported
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) object from the
[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)
collection of this [Selectable](#sqlalchemy.sql.expression.Selectable)
which corresponds to that
original [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) via a common ancestor
column.

  Parameters:

- **column** – the target [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  to be matched.
- **require_embedded** – only return corresponding columns for
  the given [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), if the given
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  is actually present within a sub-element
  of this [Selectable](#sqlalchemy.sql.expression.Selectable).
  Normally the column will match if
  it merely shares a common ancestor with one of the exported
  columns of this [Selectable](#sqlalchemy.sql.expression.Selectable).

See also

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns) - the
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that is used for the operation.

[ColumnCollection.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.corresponding_column)
- implementation
method.

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)cte(*name:str|None=None*, *recursive:bool=False*, *nesting:bool=False*) → [CTE](#sqlalchemy.sql.expression.CTE)

*inherited from the* [HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE),
or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT
statements can draw upon secondary statements specified along
with the primary statement, using a clause called “WITH”.
Special semantics regarding UNION can also be employed to
allow “recursive” queries, where a SELECT statement can draw
upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT
and DELETE on some databases, both as a source of CTE rows
when combined with RETURNING, as well as a consumer of
CTE rows.

SQLAlchemy detects [CTE](#sqlalchemy.sql.expression.CTE) objects, which are treated
similarly to [Alias](#sqlalchemy.sql.expression.Alias) objects, as special elements
to be delivered to the FROM clause of the statement as well
as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and
“NOT MATERIALIZED”, the `CTE.prefix_with()`
method may be
used to establish these.

Changed in version 1.3.13: Added support for prefixes.
In particular - MATERIALIZED and NOT MATERIALIZED.

   Parameters:

- **name** – name given to the common table expression.  Like
  [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias), the name can be left as
  `None` in which case an anonymous symbol will be used at query
  compile time.
- **recursive** – if `True`, will render `WITH RECURSIVE`.
  A recursive common table expression is intended to be used in
  conjunction with UNION ALL in order to derive rows
  from those already selected.
- **nesting** –
  if `True`, will render the CTE locally to the
  statement in which it is referenced.   For more complex scenarios,
  the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method using the
  [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here)
  parameter may also be used to more carefully
  control the exact placement of a particular CTE.
  Added in version 1.4.24.
  See also
  [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte)

The following examples include two from PostgreSQL’s documentation at
[https://www.postgresql.org/docs/current/static/queries-with.html](https://www.postgresql.org/docs/current/static/queries-with.html),
as well as additional examples.

Example 1, non recursive:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("region", String),
    Column("amount", Integer),
    Column("product", String),
    Column("quantity", Integer),
)

regional_sales = (
    select(orders.c.region, func.sum(orders.c.amount).label("total_sales"))
    .group_by(orders.c.region)
    .cte("regional_sales")
)

top_regions = (
    select(regional_sales.c.region)
    .where(
        regional_sales.c.total_sales
        > select(func.sum(regional_sales.c.total_sales) / 10)
    )
    .cte("top_regions")
)

statement = (
    select(
        orders.c.region,
        orders.c.product,
        func.sum(orders.c.quantity).label("product_units"),
        func.sum(orders.c.amount).label("product_sales"),
    )
    .where(orders.c.region.in_(select(top_regions.c.region)))
    .group_by(orders.c.region, orders.c.product)
)

result = conn.execute(statement).fetchall()
```

Example 2, WITH RECURSIVE:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

parts = Table(
    "parts",
    metadata,
    Column("part", String),
    Column("sub_part", String),
    Column("quantity", Integer),
)

included_parts = (
    select(parts.c.sub_part, parts.c.part, parts.c.quantity)
    .where(parts.c.part == "our part")
    .cte(recursive=True)
)

incl_alias = included_parts.alias()
parts_alias = parts.alias()
included_parts = included_parts.union_all(
    select(
        parts_alias.c.sub_part, parts_alias.c.part, parts_alias.c.quantity
    ).where(parts_alias.c.part == incl_alias.c.sub_part)
)

statement = select(
    included_parts.c.sub_part,
    func.sum(included_parts.c.quantity).label("total_quantity"),
).group_by(included_parts.c.sub_part)

result = conn.execute(statement).fetchall()
```

Example 3, an upsert using UPDATE and INSERT with CTEs:

```
from datetime import date
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Date,
    select,
    literal,
    and_,
    exists,
)

metadata = MetaData()

visitors = Table(
    "visitors",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("date", Date, primary_key=True),
    Column("count", Integer),
)

# add 5 visitors for the product_id == 1
product_id = 1
day = date.today()
count = 5

update_cte = (
    visitors.update()
    .where(
        and_(visitors.c.product_id == product_id, visitors.c.date == day)
    )
    .values(count=visitors.c.count + count)
    .returning(literal(1))
    .cte("update_cte")
)

upsert = visitors.insert().from_select(
    [visitors.c.product_id, visitors.c.date, visitors.c.count],
    select(literal(product_id), literal(day), literal(count)).where(
        ~exists(update_cte.select())
    ),
)

connection.execute(upsert)
```

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte(
    "value_a", nesting=True
)

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = select(value_a_nested.c.n).cte("value_b")

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

The above query will render the second CTE nested inside the first,
shown with inline parameters below as:

```
WITH
    value_a AS
        (SELECT 'root' AS n),
    value_b AS
        (WITH value_a AS
            (SELECT 'nesting' AS n)
        SELECT value_a.n AS n FROM value_a)
SELECT value_a.n AS a, value_b.n AS b
FROM value_a, value_b
```

The same CTE can be set up using the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method
as follows (SQLAlchemy 2.0 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte("value_a")

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = (
    select(value_a_nested.c.n)
    .add_cte(value_a_nested, nest_here=True)
    .cte("value_b")
)

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

```
edge = Table(
    "edge",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("left", Integer),
    Column("right", Integer),
)

root_node = select(literal(1).label("node")).cte("nodes", recursive=True)

left_edge = select(edge.c.left).join(
    root_node, edge.c.right == root_node.c.node
)
right_edge = select(edge.c.right).join(
    root_node, edge.c.left == root_node.c.node
)

subgraph_cte = root_node.union(left_edge, right_edge)

subgraph = select(subgraph_cte)
```

The above query will render 2 UNIONs inside the recursive CTE:

```
WITH RECURSIVE nodes(node) AS (
        SELECT 1 AS node
    UNION
        SELECT edge."left" AS "left"
        FROM edge JOIN nodes ON edge."right" = nodes.node
    UNION
        SELECT edge."right" AS "right"
        FROM edge JOIN nodes ON edge."left" = nodes.node
)
SELECT nodes.node FROM nodes
```

See also

[Query.cte()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.cte) - ORM version of
[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte).

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)exists() → [Exists](#sqlalchemy.sql.expression.Exists)

Return an [Exists](#sqlalchemy.sql.expression.Exists) representation of this selectable,
which can be used as a column expression.

The returned object is an instance of [Exists](#sqlalchemy.sql.expression.Exists).

See also

[exists()](#sqlalchemy.sql.expression.exists)

[EXISTS subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-exists) - in the [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) tutorial.

Added in version 1.4.

     property exported_columns: ReadOnlyColumnCollection[str, [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]]

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [Selectable](#sqlalchemy.sql.expression.Selectable), not including
[TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) constructs.

The “exported” columns for a [SelectBase](#sqlalchemy.sql.expression.SelectBase)
object are synonymous
with the [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) collection.

Added in version 1.4.

See also

[Select.exported_columns](#sqlalchemy.sql.expression.Select.exported_columns)

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)

[FromClause.exported_columns](#sqlalchemy.sql.expression.FromClause.exported_columns)

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)get_label_style() → [SelectLabelStyle](#sqlalchemy.sql.expression.SelectLabelStyle)

Retrieve the current label style.

Implemented by subclasses.

    attribute [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)inherit_cache = None

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

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)is_derived_from(*fromclause:FromClause|None*) → bool

*inherited from the* [ReturnsRows.is_derived_from()](#sqlalchemy.sql.expression.ReturnsRows.is_derived_from) *method of* [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows)

Return `True` if this [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows) is
‘derived’ from the given [FromClause](#sqlalchemy.sql.expression.FromClause).

An example would be an Alias of a Table is derived from that Table.

    method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)label(*name:str|None*) → [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label)[Any]

Return a ‘scalar’ representation of this selectable, embedded as a
subquery with a label.

See also

[SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)lateral(*name:str|None=None*) → LateralFromClause

Return a LATERAL alias of this [Selectable](#sqlalchemy.sql.expression.Selectable).

The return value is the [Lateral](#sqlalchemy.sql.expression.Lateral) construct also
provided by the top-level [lateral()](#sqlalchemy.sql.expression.lateral) function.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

     attribute [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)name_cte_columns = False

*inherited from the* [HasCTE.name_cte_columns](#sqlalchemy.sql.expression.HasCTE.name_cte_columns) *attribute of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause.

Added in version 2.0.42.

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)replace_selectable(*old:FromClause*, *alias:Alias*) → Self

*inherited from the* [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Replace all occurrences of [FromClause](#sqlalchemy.sql.expression.FromClause)
‘old’ with the given [Alias](#sqlalchemy.sql.expression.Alias)
object, returning a copy of this [FromClause](#sqlalchemy.sql.expression.FromClause).

Deprecated since version 1.4: The [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) method is deprecated, and will be removed in a future release.  Similar functionality is available via the sqlalchemy.sql.visitors module.

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)scalar_subquery() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

Return a ‘scalar’ representation of this selectable, which can be
used as a column expression.

The returned object is an instance of [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect).

Typically, a select statement which has only one column in its columns
clause is eligible to be used as a scalar expression.  The scalar
subquery can then be used in the WHERE clause or columns clause of
an enclosing SELECT.

Note that the scalar subquery differentiates from the FROM-level
subquery that can be produced using the
[SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
method.

See also

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery) - in the 2.0 tutorial

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)select(**arg:Any*, ***kw:Any*) → [Select](#sqlalchemy.sql.expression.Select)

Deprecated since version 1.4: The [SelectBase.select()](#sqlalchemy.sql.expression.SelectBase.select) method is deprecated and will be removed in a future release; this method implicitly creates a subquery that should be explicit.  Please call [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) first in order to create a subquery, which then can be selected.

     attribute [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)selected_columns

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
representing the columns that
this SELECT statement or similar construct returns in its result set.

This collection differs from the [FromClause.columns](#sqlalchemy.sql.expression.FromClause.columns)
collection of a [FromClause](#sqlalchemy.sql.expression.FromClause) in that the columns
within this collection cannot be directly nested inside another SELECT
statement; a subquery must be applied first which provides for the
necessary parenthesization required by SQL.

Note

The [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) collection does not
include expressions established in the columns clause using the
[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct; these are silently omitted from the
collection. To use plain textual column expressions inside of a
[Select](#sqlalchemy.sql.expression.Select) construct, use the [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column)
construct.

See also

[Select.selected_columns](#sqlalchemy.sql.expression.Select.selected_columns)

Added in version 1.4.

     method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)set_label_style(*style:SelectLabelStyle*) → Self

Return a new selectable with the specified label style.

Implemented by subclasses.

    method [sqlalchemy.sql.expression.SelectBase.](#sqlalchemy.sql.expression.SelectBase)subquery(*name:str|None=None*) → [Subquery](#sqlalchemy.sql.expression.Subquery)

Return a subquery of this [SelectBase](#sqlalchemy.sql.expression.SelectBase).

A subquery is from a SQL perspective a parenthesized, named
construct that can be placed in the FROM clause of another
SELECT statement.

Given a SELECT statement such as:

```
stmt = select(table.c.id, table.c.name)
```

The above statement might look like:

```
SELECT table.id, table.name FROM table
```

The subquery form by itself renders the same way, however when
embedded into the FROM clause of another SELECT statement, it becomes
a named sub-element:

```
subq = stmt.subquery()
new_stmt = select(subq)
```

The above renders as:

```
SELECT anon_1.id, anon_1.name
FROM (SELECT table.id, table.name FROM table) AS anon_1
```

Historically, [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
is equivalent to calling
the [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias)
method on a FROM object; however,
as a [SelectBase](#sqlalchemy.sql.expression.SelectBase)
object is not directly  FROM object,
the [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
method provides clearer semantics.

Added in version 1.4.

      class sqlalchemy.sql.expression.Subquery

*inherits from* [sqlalchemy.sql.expression.AliasedReturnsRows](#sqlalchemy.sql.expression.AliasedReturnsRows)

Represent a subquery of a SELECT.

A [Subquery](#sqlalchemy.sql.expression.Subquery) is created by invoking the
[SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) method, or for convenience the
[SelectBase.alias()](#sqlalchemy.sql.expression.SelectBase.alias) method, on any
[SelectBase](#sqlalchemy.sql.expression.SelectBase) subclass
which includes [Select](#sqlalchemy.sql.expression.Select),
[CompoundSelect](#sqlalchemy.sql.expression.CompoundSelect), and
[TextualSelect](#sqlalchemy.sql.expression.TextualSelect).  As rendered in a FROM clause,
it represents the
body of the SELECT statement inside of parenthesis, followed by the usual
“AS <somename>” that defines all “alias” objects.

The [Subquery](#sqlalchemy.sql.expression.Subquery) object is very similar to the
[Alias](#sqlalchemy.sql.expression.Alias)
object and can be used in an equivalent way.    The difference between
[Alias](#sqlalchemy.sql.expression.Alias) and [Subquery](#sqlalchemy.sql.expression.Subquery) is that
[Alias](#sqlalchemy.sql.expression.Alias) always
contains a [FromClause](#sqlalchemy.sql.expression.FromClause) object whereas
[Subquery](#sqlalchemy.sql.expression.Subquery)
always contains a [SelectBase](#sqlalchemy.sql.expression.SelectBase) object.

Added in version 1.4: The [Subquery](#sqlalchemy.sql.expression.Subquery) class was added which now
serves the purpose of providing an aliased version of a SELECT
statement.

| Member Name | Description |
| --- | --- |
| as_scalar() |  |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |

   method [sqlalchemy.sql.expression.Subquery.](#sqlalchemy.sql.expression.Subquery)as_scalar() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

Deprecated since version 1.4: The [Subquery.as_scalar()](#sqlalchemy.sql.expression.Subquery.as_scalar) method, which was previously `Alias.as_scalar()` prior to version 1.4, is deprecated and will be removed in a future release; Please use the [Select.scalar_subquery()](#sqlalchemy.sql.expression.Select.scalar_subquery) method of the [select()](#sqlalchemy.sql.expression.select) construct before constructing a subquery object, or with the ORM use the [Query.scalar_subquery()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.scalar_subquery) method.

     attribute [sqlalchemy.sql.expression.Subquery.](#sqlalchemy.sql.expression.Subquery)inherit_cache = True

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

      class sqlalchemy.sql.expression.TableClause

*inherits from* `sqlalchemy.sql.roles.DMLTableRole`, `sqlalchemy.sql.expression.Immutable`, `sqlalchemy.sql.expression.NamedFromClause`

Represents a minimal “table” construct.

This is a lightweight table object that has only a name, a
collection of columns, which are typically produced
by the [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) function, and a schema:

```
from sqlalchemy import table, column

user = table(
    "user",
    column("id"),
    column("name"),
    column("description"),
)
```

The [TableClause](#sqlalchemy.sql.expression.TableClause) construct serves as the base for
the more commonly used [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, providing
the usual set of [FromClause](#sqlalchemy.sql.expression.FromClause) services including
the `.c.` collection and statement generation methods.

It does **not** provide all the additional schema-level services
of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), including constraints, references to other
tables, or support for [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)-level services.
It’s useful
on its own as an ad-hoc construct used to generate quick SQL
statements when a more fully fledged [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
is not on hand.

| Member Name | Description |
| --- | --- |
| alias() | Return an alias of thisFromClause. |
| c | A synonym forFromClause.columns |
| columns | A named-based collection ofColumnElementobjects maintained by thisFromClause. |
| compare() | Compare thisClauseElementto
the givenClauseElement. |
| compile() | Compile this SQL expression. |
| corresponding_column() | Given aColumnElement, return the exportedColumnElementobject from theSelectable.exported_columnscollection of thisSelectablewhich corresponds to that
originalColumnElementvia a common ancestor
column. |
| delete() | Generate adelete()construct against thisTableClause. |
| description |  |
| entity_namespace | Return a namespace used for name-based access in SQL expressions. |
| exported_columns | AColumnCollectionthat represents the “exported”
columns of thisSelectable. |
| foreign_keys | Return the collection ofForeignKeymarker objects
which this FromClause references. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| implicit_returning | TableClausedoesn’t support having a primary key or column
-level defaults, so implicit returning doesn’t apply. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| insert() | Generate anInsertconstruct against thisTableClause. |
| is_derived_from() | ReturnTrueif thisFromClauseis
‘derived’ from the givenFromClause. |
| join() | Return aJoinfrom thisFromClauseto anotherFromClause. |
| lateral() | Return a LATERAL alias of thisSelectable. |
| outerjoin() | Return aJoinfrom thisFromClauseto anotherFromClause, with the “isouter” flag set to
True. |
| params() | Return a copy withbindparam()elements
replaced. |
| primary_key | Return the iterable collection ofColumnobjects
which comprise the primary key of this_selectable.FromClause. |
| replace_selectable() | Replace all occurrences ofFromClause‘old’ with the givenAliasobject, returning a copy of thisFromClause. |
| schema | Define the ‘schema’ attribute for thisFromClause. |
| select() | Return a SELECT of thisFromClause. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| table_valued() | Return aTableValuedColumnobject for thisFromClause. |
| tablesample() | Return a TABLESAMPLE alias of thisFromClause. |
| unique_params() | Return a copy withbindparam()elements
replaced. |
| update() | Generate anupdate()construct against thisTableClause. |

   method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)alias(*name:str|None=None*, *flat:bool=False*) → NamedFromClause

*inherited from the* [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias) *method of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return an alias of this [FromClause](#sqlalchemy.sql.expression.FromClause).

E.g.:

```
a2 = some_table.alias("a2")
```

The above code creates an [Alias](#sqlalchemy.sql.expression.Alias)
object which can be used
as a FROM clause in any SELECT statement.

See also

[Using Aliases](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-using-aliases)

[alias()](#sqlalchemy.sql.expression.alias)

     attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)c

*inherited from the* [FromClause.c](#sqlalchemy.sql.expression.FromClause.c) *attribute of* [FromClause](#sqlalchemy.sql.expression.FromClause)

A synonym for [FromClause.columns](#sqlalchemy.sql.expression.FromClause.columns)

  Returns:

a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)

      attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)columns

*inherited from the* [FromClause.columns](#sqlalchemy.sql.expression.FromClause.columns) *attribute of* [FromClause](#sqlalchemy.sql.expression.FromClause)

A named-based collection of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
objects maintained by this [FromClause](#sqlalchemy.sql.expression.FromClause).

The [columns](#sqlalchemy.sql.expression.TableClause.columns), or [c](#sqlalchemy.sql.expression.TableClause.c) collection, is the gateway
to the construction of SQL expressions using table-bound or
other selectable-bound columns:

```
select(mytable).where(mytable.c.somecolumn == 5)
```

   Returns:

a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) object.

      method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)compare(*other:ClauseElement*, ***kw:Any*) → bool

*inherited from the* [ClauseElement.compare()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compare) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Compare this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) to
the given [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

Subclasses should override the default behavior, which is a
straight identity comparison.

**kw are arguments consumed by subclass `compare()` methods and
may be used to modify the criteria for comparison
(see [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)).

    method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

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

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)corresponding_column(*column:KeyedColumnElement[Any]*, *require_embedded:bool=False*) → KeyedColumnElement[Any] | None

*inherited from the* [Selectable.corresponding_column()](#sqlalchemy.sql.expression.Selectable.corresponding_column) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Given a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), return the exported
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) object from the
[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)
collection of this [Selectable](#sqlalchemy.sql.expression.Selectable)
which corresponds to that
original [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) via a common ancestor
column.

  Parameters:

- **column** – the target [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  to be matched.
- **require_embedded** – only return corresponding columns for
  the given [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), if the given
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  is actually present within a sub-element
  of this [Selectable](#sqlalchemy.sql.expression.Selectable).
  Normally the column will match if
  it merely shares a common ancestor with one of the exported
  columns of this [Selectable](#sqlalchemy.sql.expression.Selectable).

See also

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns) - the
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that is used for the operation.

[ColumnCollection.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.corresponding_column)
- implementation
method.

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)delete() → [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete)

Generate a [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) construct against this
[TableClause](#sqlalchemy.sql.expression.TableClause).

E.g.:

```
table.delete().where(table.c.id == 7)
```

See [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) for argument and usage information.

    attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)description    attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)entity_namespace

*inherited from the* [FromClause.entity_namespace](#sqlalchemy.sql.expression.FromClause.entity_namespace) *attribute of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return a namespace used for name-based access in SQL expressions.

This is the namespace that is used to resolve “filter_by()” type
expressions, such as:

```
stmt.filter_by(address="some address")
```

It defaults to the `.c` collection, however internally it can
be overridden using the “entity_namespace” annotation to deliver
alternative results.

    attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)exported_columns

*inherited from the* [FromClause.exported_columns](#sqlalchemy.sql.expression.FromClause.exported_columns) *attribute of* [FromClause](#sqlalchemy.sql.expression.FromClause)

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [Selectable](#sqlalchemy.sql.expression.Selectable).

The “exported” columns for a [FromClause](#sqlalchemy.sql.expression.FromClause)
object are synonymous
with the [FromClause.columns](#sqlalchemy.sql.expression.FromClause.columns) collection.

Added in version 1.4.

See also

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)

[SelectBase.exported_columns](#sqlalchemy.sql.expression.SelectBase.exported_columns)

     attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)foreign_keys

*inherited from the* [FromClause.foreign_keys](#sqlalchemy.sql.expression.FromClause.foreign_keys) *attribute of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return the collection of [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) marker objects
which this FromClause references.

Each [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) is a member of a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)-wide
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).

See also

[Table.foreign_key_constraints](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.foreign_key_constraints)

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)implicit_returning = False

[TableClause](#sqlalchemy.sql.expression.TableClause)
doesn’t support having a primary key or column
-level defaults, so implicit returning doesn’t apply.

    attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)inherit_cache = None

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

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)insert() → [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)

Generate an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct against this
[TableClause](#sqlalchemy.sql.expression.TableClause).

E.g.:

```
table.insert().values(name="foo")
```

See [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) for argument and usage information.

    method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)is_derived_from(*fromclause:FromClause|None*) → bool

*inherited from the* [FromClause.is_derived_from()](#sqlalchemy.sql.expression.FromClause.is_derived_from) *method of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return `True` if this [FromClause](#sqlalchemy.sql.expression.FromClause) is
‘derived’ from the given `FromClause`.

An example would be an Alias of a Table is derived from that Table.

    method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)join(*right:_FromClauseArgument*, *onclause:_ColumnExpressionArgument[bool]|None=None*, *isouter:bool=False*, *full:bool=False*) → [Join](#sqlalchemy.sql.expression.Join)

*inherited from the* [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join) *method of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return a [Join](#sqlalchemy.sql.expression.Join) from this
[FromClause](#sqlalchemy.sql.expression.FromClause)
to another [FromClause](#sqlalchemy.sql.expression.FromClause).

E.g.:

```
from sqlalchemy import join

j = user_table.join(
    address_table, user_table.c.id == address_table.c.user_id
)
stmt = select(user_table).select_from(j)
```

would emit SQL along the lines of:

```
SELECT user.id, user.name FROM user
JOIN address ON user.id = address.user_id
```

   Parameters:

- **right** – the right side of the join; this is any
  [FromClause](#sqlalchemy.sql.expression.FromClause) object such as a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, and
  may also be a selectable-compatible object such as an ORM-mapped
  class.
- **onclause** – a SQL expression representing the ON clause of the
  join.  If left at `None`, [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)
  will attempt to
  join the two tables based on a foreign key relationship.
- **isouter** – if True, render a LEFT OUTER JOIN, instead of JOIN.
- **full** – if True, render a FULL OUTER JOIN, instead of LEFT OUTER
  JOIN.  Implies [FromClause.join.isouter](#sqlalchemy.sql.expression.FromClause.join.params.isouter).

See also

[join()](#sqlalchemy.sql.expression.join) - standalone function

[Join](#sqlalchemy.sql.expression.Join) - the type of object produced

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)lateral(*name:str|None=None*) → LateralFromClause

*inherited from the* [Selectable.lateral()](#sqlalchemy.sql.expression.Selectable.lateral) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Return a LATERAL alias of this [Selectable](#sqlalchemy.sql.expression.Selectable).

The return value is the [Lateral](#sqlalchemy.sql.expression.Lateral) construct also
provided by the top-level [lateral()](#sqlalchemy.sql.expression.lateral) function.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)outerjoin(*right:_FromClauseArgument*, *onclause:_ColumnExpressionArgument[bool]|None=None*, *full:bool=False*) → [Join](#sqlalchemy.sql.expression.Join)

*inherited from the* [FromClause.outerjoin()](#sqlalchemy.sql.expression.FromClause.outerjoin) *method of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return a [Join](#sqlalchemy.sql.expression.Join) from this
[FromClause](#sqlalchemy.sql.expression.FromClause)
to another [FromClause](#sqlalchemy.sql.expression.FromClause), with the “isouter” flag set to
True.

E.g.:

```
from sqlalchemy import outerjoin

j = user_table.outerjoin(
    address_table, user_table.c.id == address_table.c.user_id
)
```

The above is equivalent to:

```
j = user_table.join(
    address_table, user_table.c.id == address_table.c.user_id, isouter=True
)
```

   Parameters:

- **right** – the right side of the join; this is any
  [FromClause](#sqlalchemy.sql.expression.FromClause) object such as a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, and
  may also be a selectable-compatible object such as an ORM-mapped
  class.
- **onclause** – a SQL expression representing the ON clause of the
  join.  If left at `None`, [FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)
  will attempt to
  join the two tables based on a foreign key relationship.
- **full** – if True, render a FULL OUTER JOIN, instead of
  LEFT OUTER JOIN.

See also

[FromClause.join()](#sqlalchemy.sql.expression.FromClause.join)

[Join](#sqlalchemy.sql.expression.Join)

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)params(**optionaldict:Any*, ***kwargs:Any*) → NoReturn

*inherited from the* `Immutable.params()` *method of* `Immutable`

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Returns a copy of this ClauseElement with
[bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
elements replaced with values taken from the given dictionary:

```
>>> clause = column("x") + bindparam("foo")
>>> print(clause.compile().params)
{'foo':None}
>>> print(clause.params({"foo": 7}).compile().params)
{'foo':7}
```

     attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)primary_key

*inherited from the* [FromClause.primary_key](#sqlalchemy.sql.expression.FromClause.primary_key) *attribute of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return the iterable collection of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
which comprise the primary key of this `_selectable.FromClause`.

For a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, this collection is represented
by the [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) which itself is an
iterable collection of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects.

    method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)replace_selectable(*old:FromClause*, *alias:Alias*) → Self

*inherited from the* [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Replace all occurrences of [FromClause](#sqlalchemy.sql.expression.FromClause)
‘old’ with the given [Alias](#sqlalchemy.sql.expression.Alias)
object, returning a copy of this [FromClause](#sqlalchemy.sql.expression.FromClause).

Deprecated since version 1.4: The [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) method is deprecated, and will be removed in a future release.  Similar functionality is available via the sqlalchemy.sql.visitors module.

     attribute [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)schema = None

*inherited from the* [FromClause.schema](#sqlalchemy.sql.expression.FromClause.schema) *attribute of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Define the ‘schema’ attribute for this [FromClause](#sqlalchemy.sql.expression.FromClause).

This is typically `None` for most objects except that of
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), where it is taken as the value of the
[Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) argument.

    method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)select() → [Select](#sqlalchemy.sql.expression.Select)

*inherited from the* [FromClause.select()](#sqlalchemy.sql.expression.FromClause.select) *method of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return a SELECT of this [FromClause](#sqlalchemy.sql.expression.FromClause).

e.g.:

```
stmt = some_table.select().where(some_table.c.id == 5)
```

See also

[select()](#sqlalchemy.sql.expression.select) - general purpose
method which allows for arbitrary column lists.

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)self_group(*against:OperatorType|None=None*) → [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

*inherited from the* [ClauseElement.self_group()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.self_group) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.TableClause.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.TableClause.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)table_valued() → TableValuedColumn[Any]

*inherited from the* `NamedFromClause.table_valued()` *method of* `NamedFromClause`

Return a `TableValuedColumn` object for this
[FromClause](#sqlalchemy.sql.expression.FromClause).

A `TableValuedColumn` is a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) that
represents a complete row in a table. Support for this construct is
backend dependent, and is supported in various forms by backends
such as PostgreSQL, Oracle Database and SQL Server.

E.g.:

```
>>> from sqlalchemy import select, column, func, table
>>> a = table("a", column("id"), column("x"), column("y"))
>>> stmt = select(func.row_to_json(a.table_valued()))
>>> print(stmt)
SELECT row_to_json(a) AS row_to_json_1
FROM a
```

Added in version 1.4.0b2.

See also

[Working with SQL Functions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-functions) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)tablesample(*sampling:float|Function[Any]*, *name:str|None=None*, *seed:roles.ExpressionElementRole[Any]|None=None*) → [TableSample](#sqlalchemy.sql.expression.TableSample)

*inherited from the* [FromClause.tablesample()](#sqlalchemy.sql.expression.FromClause.tablesample) *method of* [FromClause](#sqlalchemy.sql.expression.FromClause)

Return a TABLESAMPLE alias of this [FromClause](#sqlalchemy.sql.expression.FromClause).

The return value is the [TableSample](#sqlalchemy.sql.expression.TableSample)
construct also
provided by the top-level [tablesample()](#sqlalchemy.sql.expression.tablesample) function.

See also

[tablesample()](#sqlalchemy.sql.expression.tablesample) - usage guidelines and parameters

     method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)unique_params(**optionaldict:Any*, ***kwargs:Any*) → NoReturn

*inherited from the* `Immutable.unique_params()` *method of* `Immutable`

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Same functionality as [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params),
except adds unique=True
to affected bind parameters so that multiple statements can be
used.

    method [sqlalchemy.sql.expression.TableClause.](#sqlalchemy.sql.expression.TableClause)update() → [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)

Generate an [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) construct against this
[TableClause](#sqlalchemy.sql.expression.TableClause).

E.g.:

```
table.update().where(table.c.id == 7).values(name="foo")
```

See [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) for argument and usage information.

     class sqlalchemy.sql.expression.TableSample

*inherits from* `sqlalchemy.sql.expression.FromClauseAlias`

Represent a TABLESAMPLE clause.

This object is constructed from the [tablesample()](#sqlalchemy.sql.expression.tablesample) module
level function as well as the [FromClause.tablesample()](#sqlalchemy.sql.expression.FromClause.tablesample)
method
available on all [FromClause](#sqlalchemy.sql.expression.FromClause) subclasses.

See also

[tablesample()](#sqlalchemy.sql.expression.tablesample)

     class sqlalchemy.sql.expression.TableValuedAlias

*inherits from* `sqlalchemy.sql.expression.LateralFromClause`, [sqlalchemy.sql.expression.Alias](#sqlalchemy.sql.expression.Alias)

An alias against a “table valued” SQL function.

This construct provides for a SQL function that returns columns
to be used in the FROM clause of a SELECT statement.   The
object is generated using the [FunctionElement.table_valued()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.table_valued)
method, e.g.:

```
>>> from sqlalchemy import select, func
>>> fn = func.json_array_elements_text('["one", "two", "three"]').table_valued(
...     "value"
... )
>>> print(select(fn.c.value))
SELECT anon_1.value
FROM json_array_elements_text(:json_array_elements_text_1) AS anon_1
```

Added in version 1.4.0b2.

See also

[Table-Valued Functions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-functions-table-valued) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

| Member Name | Description |
| --- | --- |
| alias() | Return a new alias of thisTableValuedAlias. |
| column | Return a column expression representing thisTableValuedAlias. |
| lateral() | Return a newTableValuedAliaswith the lateral flag
set, so that it renders as LATERAL. |
| render_derived() | Apply “render derived” to thisTableValuedAlias. |

   method [sqlalchemy.sql.expression.TableValuedAlias.](#sqlalchemy.sql.expression.TableValuedAlias)alias(*name:str|None=None*, *flat:bool=False*) → [TableValuedAlias](#sqlalchemy.sql.expression.TableValuedAlias)

Return a new alias of this [TableValuedAlias](#sqlalchemy.sql.expression.TableValuedAlias).

This creates a distinct FROM object that will be distinguished
from the original one when used in a SQL statement.

    attribute [sqlalchemy.sql.expression.TableValuedAlias.](#sqlalchemy.sql.expression.TableValuedAlias)column

Return a column expression representing this
[TableValuedAlias](#sqlalchemy.sql.expression.TableValuedAlias).

This accessor is used to implement the
[FunctionElement.column_valued()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.column_valued) method. See that
method for further details.

E.g.:

```
>>> print(select(func.some_func().table_valued("value").column))
SELECT anon_1 FROM some_func() AS anon_1
```

See also

[FunctionElement.column_valued()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.column_valued)

     method [sqlalchemy.sql.expression.TableValuedAlias.](#sqlalchemy.sql.expression.TableValuedAlias)lateral(*name:str|None=None*) → LateralFromClause

Return a new [TableValuedAlias](#sqlalchemy.sql.expression.TableValuedAlias) with the lateral flag
set, so that it renders as LATERAL.

See also

[lateral()](#sqlalchemy.sql.expression.lateral)

     method [sqlalchemy.sql.expression.TableValuedAlias.](#sqlalchemy.sql.expression.TableValuedAlias)render_derived(*name:str|None=None*, *with_types:bool=False*) → [TableValuedAlias](#sqlalchemy.sql.expression.TableValuedAlias)

Apply “render derived” to this [TableValuedAlias](#sqlalchemy.sql.expression.TableValuedAlias).

This has the effect of the individual column names listed out
after the alias name in the “AS” sequence, e.g.:

```
>>> print(
...     select(
...         func.unnest(array(["one", "two", "three"]))
...         .table_valued("x", with_ordinality="o")
...         .render_derived()
...     )
... )
SELECT anon_1.x, anon_1.o
FROM unnest(ARRAY[%(param_1)s, %(param_2)s, %(param_3)s]) WITH ORDINALITY AS anon_1(x, o)
```

The `with_types` keyword will render column types inline within
the alias expression (this syntax currently applies to the
PostgreSQL database):

```
>>> print(
...     select(
...         func.json_to_recordset('[{"a":1,"b":"foo"},{"a":"2","c":"bar"}]')
...         .table_valued(column("a", Integer), column("b", String))
...         .render_derived(with_types=True)
...     )
... )
SELECT anon_1.a, anon_1.b FROM json_to_recordset(:json_to_recordset_1)
AS anon_1(a INTEGER, b VARCHAR)
```

   Parameters:

- **name** – optional string name that will be applied to the alias
  generated.  If left as None, a unique anonymizing name will be used.
- **with_types** – if True, the derived columns will include the
  datatype specification with each column. This is a special syntax
  currently known to be required by PostgreSQL for some SQL functions.

       class sqlalchemy.sql.expression.TextualSelect

*inherits from* [sqlalchemy.sql.expression.SelectBase](#sqlalchemy.sql.expression.SelectBase), `sqlalchemy.sql.expression.ExecutableReturnsRows`, `sqlalchemy.sql.expression.Generative`

Wrap a [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) construct within a
[SelectBase](#sqlalchemy.sql.expression.SelectBase)
interface.

This allows the [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) object to gain a
`.c` collection
and other FROM-like capabilities such as
[FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias),
[SelectBase.cte()](#sqlalchemy.sql.expression.SelectBase.cte), etc.

The [TextualSelect](#sqlalchemy.sql.expression.TextualSelect) construct is produced via the
[TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns)
method - see that method for details.

Changed in version 1.4: the [TextualSelect](#sqlalchemy.sql.expression.TextualSelect)
class was renamed
from `TextAsFrom`, to more correctly suit its role as a
SELECT-oriented object and not a FROM clause.

See also

[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)

[TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) - primary creation interface.

| Member Name | Description |
| --- | --- |
| add_cte() | Add one or moreCTEconstructs to this statement. |
| alias() | Return a named subquery against thisSelectBase. |
| as_scalar() |  |
| compare() | Compare thisClauseElementto
the givenClauseElement. |
| compile() | Compile this SQL expression. |
| corresponding_column() | Given aColumnElement, return the exportedColumnElementobject from theSelectable.exported_columnscollection of thisSelectablewhich corresponds to that
originalColumnElementvia a common ancestor
column. |
| cte() | Return a newCTE,
or Common Table Expression instance. |
| execution_options() | Set non-SQL options for the statement which take effect during
execution. |
| exists() | Return anExistsrepresentation of this selectable,
which can be used as a column expression. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| get_execution_options() | Get the non-SQL options which will take effect during execution. |
| get_label_style() | Retrieve the current label style. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| is_derived_from() | ReturnTrueif thisReturnsRowsis
‘derived’ from the givenFromClause. |
| label() | Return a ‘scalar’ representation of this selectable, embedded as a
subquery with a label. |
| lateral() | Return a LATERAL alias of thisSelectable. |
| name_cte_columns | indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause. |
| options() | Apply options to this statement. |
| params() | Return a copy withbindparam()elements
replaced. |
| replace_selectable() | Replace all occurrences ofFromClause‘old’ with the givenAliasobject, returning a copy of thisFromClause. |
| scalar_subquery() | Return a ‘scalar’ representation of this selectable, which can be
used as a column expression. |
| select() |  |
| selected_columns | AColumnCollectionrepresenting the columns that
this SELECT statement or similar construct returns in its result set,
not includingTextClauseconstructs. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| set_label_style() | Return a new selectable with the specified label style. |
| subquery() | Return a subquery of thisSelectBase. |
| unique_params() | Return a copy withbindparam()elements
replaced. |

   method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)add_cte(**ctes:CTE*, *nest_here:bool=False*) → Self

*inherited from the* [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Add one or more [CTE](#sqlalchemy.sql.expression.CTE) constructs to this statement.

This method will associate the given [CTE](#sqlalchemy.sql.expression.CTE) constructs with
the parent statement such that they will each be unconditionally
rendered in the WITH clause of the final statement, even if not
referenced elsewhere within the statement or any sub-selects.

The optional [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here) parameter when set
to True will have the effect that each given [CTE](#sqlalchemy.sql.expression.CTE) will
render in a WITH clause rendered directly along with this statement,
rather than being moved to the top of the ultimate rendered statement,
even if this statement is rendered as a subquery within a larger
statement.

This method has two general uses. One is to embed CTE statements that
serve some purpose without being referenced explicitly, such as the use
case of embedding a DML statement such as an INSERT or UPDATE as a CTE
inline with a primary statement that may draw from its results
indirectly.  The other is to provide control over the exact placement
of a particular series of CTE constructs that should remain rendered
directly in terms of a particular statement that may be nested in a
larger statement.

E.g.:

```
from sqlalchemy import table, column, select

t = table("t", column("c1"), column("c2"))

ins = t.insert().values({"c1": "x", "c2": "y"}).cte()

stmt = select(t).add_cte(ins)
```

Would render:

```
WITH anon_1 AS (
    INSERT INTO t (c1, c2) VALUES (:param_1, :param_2)
)
SELECT t.c1, t.c2
FROM t
```

Above, the “anon_1” CTE is not referenced in the SELECT
statement, however still accomplishes the task of running an INSERT
statement.

Similarly in a DML-related context, using the PostgreSQL
[Insert](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert) construct to generate an “upsert”:

```
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import insert

t = table("t", column("c1"), column("c2"))

delete_statement_cte = t.delete().where(t.c.c1 < 1).cte("deletions")

insert_stmt = insert(t).values({"c1": 1, "c2": 2})
update_statement = insert_stmt.on_conflict_do_update(
    index_elements=[t.c.c1],
    set_={
        "c1": insert_stmt.excluded.c1,
        "c2": insert_stmt.excluded.c2,
    },
).add_cte(delete_statement_cte)

print(update_statement)
```

The above statement renders as:

```
WITH deletions AS (
    DELETE FROM t WHERE t.c1 < %(c1_1)s
)
INSERT INTO t (c1, c2) VALUES (%(c1)s, %(c2)s)
ON CONFLICT (c1) DO UPDATE SET c1 = excluded.c1, c2 = excluded.c2
```

Added in version 1.4.21.

   Parameters:

- ***ctes** –
  zero or more [CTE](#sqlalchemy.sql.expression.CTE) constructs.
  Changed in version 2.0: Multiple CTE instances are accepted
- **nest_here** –
  if True, the given CTE or CTEs will be rendered
  as though they specified the [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting) flag
  to `True` when they were added to this [HasCTE](#sqlalchemy.sql.expression.HasCTE).
  Assuming the given CTEs are not referenced in an outer-enclosing
  statement as well, the CTEs given should render at the level of
  this statement when this flag is given.
  Added in version 2.0.
  See also
  [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting)

      method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)alias(*name:str|None=None*, *flat:bool=False*) → [Subquery](#sqlalchemy.sql.expression.Subquery)

*inherited from the* [SelectBase.alias()](#sqlalchemy.sql.expression.SelectBase.alias) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a named subquery against this
[SelectBase](#sqlalchemy.sql.expression.SelectBase).

For a [SelectBase](#sqlalchemy.sql.expression.SelectBase) (as opposed to a
[FromClause](#sqlalchemy.sql.expression.FromClause)),
this returns a [Subquery](#sqlalchemy.sql.expression.Subquery) object which behaves mostly the
same as the [Alias](#sqlalchemy.sql.expression.Alias) object that is used with a
[FromClause](#sqlalchemy.sql.expression.FromClause).

Changed in version 1.4: The [SelectBase.alias()](#sqlalchemy.sql.expression.SelectBase.alias)
method is now
a synonym for the [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) method.

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)as_scalar() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

*inherited from the* [SelectBase.as_scalar()](#sqlalchemy.sql.expression.SelectBase.as_scalar) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Deprecated since version 1.4: The [SelectBase.as_scalar()](#sqlalchemy.sql.expression.SelectBase.as_scalar) method is deprecated and will be removed in a future release.  Please refer to [SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

     property c: ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]

Deprecated since version 1.4: The [SelectBase.c](#sqlalchemy.sql.expression.SelectBase.c) and `SelectBase.columns` attributes are deprecated and will be removed in a future release; these attributes implicitly create a subquery that should be explicit.  Please call [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) first in order to create a subquery, which then contains this attribute.  To access the columns that this SELECT object SELECTs from, use the [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) attribute.

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)compare(*other:ClauseElement*, ***kw:Any*) → bool

*inherited from the* [ClauseElement.compare()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compare) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Compare this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) to
the given [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

Subclasses should override the default behavior, which is a
straight identity comparison.

**kw are arguments consumed by subclass `compare()` methods and
may be used to modify the criteria for comparison
(see [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)).

    method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

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

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)corresponding_column(*column:KeyedColumnElement[Any]*, *require_embedded:bool=False*) → KeyedColumnElement[Any] | None

*inherited from the* [Selectable.corresponding_column()](#sqlalchemy.sql.expression.Selectable.corresponding_column) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Given a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), return the exported
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) object from the
[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)
collection of this [Selectable](#sqlalchemy.sql.expression.Selectable)
which corresponds to that
original [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) via a common ancestor
column.

  Parameters:

- **column** – the target [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  to be matched.
- **require_embedded** – only return corresponding columns for
  the given [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), if the given
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  is actually present within a sub-element
  of this [Selectable](#sqlalchemy.sql.expression.Selectable).
  Normally the column will match if
  it merely shares a common ancestor with one of the exported
  columns of this [Selectable](#sqlalchemy.sql.expression.Selectable).

See also

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns) - the
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that is used for the operation.

[ColumnCollection.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.corresponding_column)
- implementation
method.

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)cte(*name:str|None=None*, *recursive:bool=False*, *nesting:bool=False*) → [CTE](#sqlalchemy.sql.expression.CTE)

*inherited from the* [HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE),
or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT
statements can draw upon secondary statements specified along
with the primary statement, using a clause called “WITH”.
Special semantics regarding UNION can also be employed to
allow “recursive” queries, where a SELECT statement can draw
upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT
and DELETE on some databases, both as a source of CTE rows
when combined with RETURNING, as well as a consumer of
CTE rows.

SQLAlchemy detects [CTE](#sqlalchemy.sql.expression.CTE) objects, which are treated
similarly to [Alias](#sqlalchemy.sql.expression.Alias) objects, as special elements
to be delivered to the FROM clause of the statement as well
as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and
“NOT MATERIALIZED”, the `CTE.prefix_with()`
method may be
used to establish these.

Changed in version 1.3.13: Added support for prefixes.
In particular - MATERIALIZED and NOT MATERIALIZED.

   Parameters:

- **name** – name given to the common table expression.  Like
  [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias), the name can be left as
  `None` in which case an anonymous symbol will be used at query
  compile time.
- **recursive** – if `True`, will render `WITH RECURSIVE`.
  A recursive common table expression is intended to be used in
  conjunction with UNION ALL in order to derive rows
  from those already selected.
- **nesting** –
  if `True`, will render the CTE locally to the
  statement in which it is referenced.   For more complex scenarios,
  the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method using the
  [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here)
  parameter may also be used to more carefully
  control the exact placement of a particular CTE.
  Added in version 1.4.24.
  See also
  [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte)

The following examples include two from PostgreSQL’s documentation at
[https://www.postgresql.org/docs/current/static/queries-with.html](https://www.postgresql.org/docs/current/static/queries-with.html),
as well as additional examples.

Example 1, non recursive:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("region", String),
    Column("amount", Integer),
    Column("product", String),
    Column("quantity", Integer),
)

regional_sales = (
    select(orders.c.region, func.sum(orders.c.amount).label("total_sales"))
    .group_by(orders.c.region)
    .cte("regional_sales")
)

top_regions = (
    select(regional_sales.c.region)
    .where(
        regional_sales.c.total_sales
        > select(func.sum(regional_sales.c.total_sales) / 10)
    )
    .cte("top_regions")
)

statement = (
    select(
        orders.c.region,
        orders.c.product,
        func.sum(orders.c.quantity).label("product_units"),
        func.sum(orders.c.amount).label("product_sales"),
    )
    .where(orders.c.region.in_(select(top_regions.c.region)))
    .group_by(orders.c.region, orders.c.product)
)

result = conn.execute(statement).fetchall()
```

Example 2, WITH RECURSIVE:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

parts = Table(
    "parts",
    metadata,
    Column("part", String),
    Column("sub_part", String),
    Column("quantity", Integer),
)

included_parts = (
    select(parts.c.sub_part, parts.c.part, parts.c.quantity)
    .where(parts.c.part == "our part")
    .cte(recursive=True)
)

incl_alias = included_parts.alias()
parts_alias = parts.alias()
included_parts = included_parts.union_all(
    select(
        parts_alias.c.sub_part, parts_alias.c.part, parts_alias.c.quantity
    ).where(parts_alias.c.part == incl_alias.c.sub_part)
)

statement = select(
    included_parts.c.sub_part,
    func.sum(included_parts.c.quantity).label("total_quantity"),
).group_by(included_parts.c.sub_part)

result = conn.execute(statement).fetchall()
```

Example 3, an upsert using UPDATE and INSERT with CTEs:

```
from datetime import date
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Date,
    select,
    literal,
    and_,
    exists,
)

metadata = MetaData()

visitors = Table(
    "visitors",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("date", Date, primary_key=True),
    Column("count", Integer),
)

# add 5 visitors for the product_id == 1
product_id = 1
day = date.today()
count = 5

update_cte = (
    visitors.update()
    .where(
        and_(visitors.c.product_id == product_id, visitors.c.date == day)
    )
    .values(count=visitors.c.count + count)
    .returning(literal(1))
    .cte("update_cte")
)

upsert = visitors.insert().from_select(
    [visitors.c.product_id, visitors.c.date, visitors.c.count],
    select(literal(product_id), literal(day), literal(count)).where(
        ~exists(update_cte.select())
    ),
)

connection.execute(upsert)
```

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte(
    "value_a", nesting=True
)

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = select(value_a_nested.c.n).cte("value_b")

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

The above query will render the second CTE nested inside the first,
shown with inline parameters below as:

```
WITH
    value_a AS
        (SELECT 'root' AS n),
    value_b AS
        (WITH value_a AS
            (SELECT 'nesting' AS n)
        SELECT value_a.n AS n FROM value_a)
SELECT value_a.n AS a, value_b.n AS b
FROM value_a, value_b
```

The same CTE can be set up using the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method
as follows (SQLAlchemy 2.0 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte("value_a")

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = (
    select(value_a_nested.c.n)
    .add_cte(value_a_nested, nest_here=True)
    .cte("value_b")
)

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

```
edge = Table(
    "edge",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("left", Integer),
    Column("right", Integer),
)

root_node = select(literal(1).label("node")).cte("nodes", recursive=True)

left_edge = select(edge.c.left).join(
    root_node, edge.c.right == root_node.c.node
)
right_edge = select(edge.c.right).join(
    root_node, edge.c.left == root_node.c.node
)

subgraph_cte = root_node.union(left_edge, right_edge)

subgraph = select(subgraph_cte)
```

The above query will render 2 UNIONs inside the recursive CTE:

```
WITH RECURSIVE nodes(node) AS (
        SELECT 1 AS node
    UNION
        SELECT edge."left" AS "left"
        FROM edge JOIN nodes ON edge."right" = nodes.node
    UNION
        SELECT edge."right" AS "right"
        FROM edge JOIN nodes ON edge."left" = nodes.node
)
SELECT nodes.node FROM nodes
```

See also

[Query.cte()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.cte) - ORM version of
[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte).

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)execution_options(***kw:Any*) → Self

*inherited from the* [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Set non-SQL options for the statement which take effect during
execution.

Execution options can be set at many scopes, including per-statement,
per-connection, or per execution, using methods such as
[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) and parameters which
accept a dictionary of options such as
[Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options) and
[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options).

The primary characteristic of an execution option, as opposed to
other kinds of options such as ORM loader options, is that
**execution options never affect the compiled SQL of a query, only
things that affect how the SQL statement itself is invoked or how
results are fetched**.  That is, execution options are not part of
what’s accommodated by SQL compilation nor are they considered part of
the cached state of a statement.

The [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) method is
[generative](https://docs.sqlalchemy.org/en/20/glossary.html#term-generative), as
is the case for the method as applied to the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
and [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects, which means when the method is called,
a copy of the object is returned, which applies the given parameters to
that new copy, but leaves the original unchanged:

```
statement = select(table.c.x, table.c.y)
new_statement = statement.execution_options(my_option=True)
```

An exception to this behavior is the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
object, where the [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) method
is explicitly **not** generative.

The kinds of options that may be passed to
[Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) and other related methods and
parameter dictionaries include parameters that are explicitly consumed
by SQLAlchemy Core or ORM, as well as arbitrary keyword arguments not
defined by SQLAlchemy, which means the methods and/or parameter
dictionaries may be used for user-defined parameters that interact with
custom code, which may access the parameters using methods such as
[Executable.get_execution_options()](#sqlalchemy.sql.expression.Executable.get_execution_options) and
[Connection.get_execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_execution_options), or within selected
event hooks using a dedicated `execution_options` event parameter
such as
[ConnectionEvents.before_execute.execution_options](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_execute.params.execution_options)
or [ORMExecuteState.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.execution_options), e.g.:

```
from sqlalchemy import event

@event.listens_for(some_engine, "before_execute")
def _process_opt(conn, statement, multiparams, params, execution_options):
    "run a SQL function before invoking a statement"

    if execution_options.get("do_special_thing", False):
        conn.exec_driver_sql("run_special_function()")
```

Within the scope of options that are explicitly recognized by
SQLAlchemy, most apply to specific classes of objects and not others.
The most common execution options include:

- [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
  sets the isolation level for a connection or a class of connections
  via an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).  This option is accepted only
  by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).
- [Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results) -
  indicates results should be fetched using a server side cursor;
  this option is accepted by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), by the
  [Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options) parameter
  on [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), and additionally by
  [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) on a SQL statement object,
  as well as by ORM constructs like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
- [Connection.execution_options.compiled_cache](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.compiled_cache) -
  indicates a dictionary that will serve as the
  [SQL compilation cache](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)
  for a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), as
  well as for ORM methods like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
  Can be passed as `None` to disable caching for statements.
  This option is not accepted by
  [Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options) as it is inadvisable to
  carry along a compilation cache within a statement object.
- [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map)
  - a mapping of schema names used by the
  [Schema Translate Map](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating) feature, accepted
  by [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
  [Executable](#sqlalchemy.sql.expression.Executable), as well as by ORM constructs
  like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).

See also

[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options)

[Connection.execute.execution_options](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute.params.execution_options)

[Session.execute.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.execution_options)

[ORM Execution Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-execution-options) - documentation on all
ORM-specific execution options

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)exists() → [Exists](#sqlalchemy.sql.expression.Exists)

*inherited from the* [SelectBase.exists()](#sqlalchemy.sql.expression.SelectBase.exists) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return an [Exists](#sqlalchemy.sql.expression.Exists) representation of this selectable,
which can be used as a column expression.

The returned object is an instance of [Exists](#sqlalchemy.sql.expression.Exists).

See also

[exists()](#sqlalchemy.sql.expression.exists)

[EXISTS subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-exists) - in the [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) tutorial.

Added in version 1.4.

     property exported_columns: ReadOnlyColumnCollection[str, [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]]

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [Selectable](#sqlalchemy.sql.expression.Selectable), not including
[TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) constructs.

The “exported” columns for a [SelectBase](#sqlalchemy.sql.expression.SelectBase)
object are synonymous
with the [SelectBase.selected_columns](#sqlalchemy.sql.expression.SelectBase.selected_columns) collection.

Added in version 1.4.

See also

[Select.exported_columns](#sqlalchemy.sql.expression.Select.exported_columns)

[Selectable.exported_columns](#sqlalchemy.sql.expression.Selectable.exported_columns)

[FromClause.exported_columns](#sqlalchemy.sql.expression.FromClause.exported_columns)

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)get_execution_options() → _ExecuteOptions

*inherited from the* [Executable.get_execution_options()](#sqlalchemy.sql.expression.Executable.get_execution_options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

See also

[Executable.execution_options()](#sqlalchemy.sql.expression.Executable.execution_options)

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)get_label_style() → [SelectLabelStyle](#sqlalchemy.sql.expression.SelectLabelStyle)

*inherited from the* [SelectBase.get_label_style()](#sqlalchemy.sql.expression.SelectBase.get_label_style) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Retrieve the current label style.

Implemented by subclasses.

    attribute [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)inherit_cache = None

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

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)is_derived_from(*fromclause:FromClause|None*) → bool

*inherited from the* [ReturnsRows.is_derived_from()](#sqlalchemy.sql.expression.ReturnsRows.is_derived_from) *method of* [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows)

Return `True` if this [ReturnsRows](#sqlalchemy.sql.expression.ReturnsRows) is
‘derived’ from the given [FromClause](#sqlalchemy.sql.expression.FromClause).

An example would be an Alias of a Table is derived from that Table.

    method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)label(*name:str|None*) → [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label)[Any]

*inherited from the* [SelectBase.label()](#sqlalchemy.sql.expression.SelectBase.label) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a ‘scalar’ representation of this selectable, embedded as a
subquery with a label.

See also

[SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)lateral(*name:str|None=None*) → LateralFromClause

*inherited from the* [SelectBase.lateral()](#sqlalchemy.sql.expression.SelectBase.lateral) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a LATERAL alias of this [Selectable](#sqlalchemy.sql.expression.Selectable).

The return value is the [Lateral](#sqlalchemy.sql.expression.Lateral) construct also
provided by the top-level [lateral()](#sqlalchemy.sql.expression.lateral) function.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

     attribute [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)name_cte_columns = False

*inherited from the* [HasCTE.name_cte_columns](#sqlalchemy.sql.expression.HasCTE.name_cte_columns) *attribute of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause.

Added in version 2.0.42.

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)options(**options:ExecutableOption*) → Self

*inherited from the* [Executable.options()](#sqlalchemy.sql.expression.Executable.options) *method of* [Executable](#sqlalchemy.sql.expression.Executable)

Apply options to this statement.

In the general sense, options are any kind of Python object
that can be interpreted by the SQL compiler for the statement.
These options can be consumed by specific dialects or specific kinds
of compilers.

The most commonly known kind of option are the ORM level options
that apply “eager load” and other loading behaviors to an ORM
query.   However, options can theoretically be used for many other
purposes.

For background on specific kinds of options for specific kinds of
statements, refer to the documentation for those option objects.

Changed in version 1.4: - added [Executable.options()](#sqlalchemy.sql.expression.Executable.options) to
Core statement objects towards the goal of allowing unified
Core / ORM querying capabilities.

See also

[Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#loading-columns) - refers to options specific to the usage
of ORM queries

[Relationship Loading with Loader Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#relationship-loader-options) - refers to options specific
to the usage of ORM queries

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)params(*_ClauseElement__optionaldict:Mapping[str,Any]|None=None*, ***kwargs:Any*) → Self

*inherited from the* [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Returns a copy of this ClauseElement with
[bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
elements replaced with values taken from the given dictionary:

```
>>> clause = column("x") + bindparam("foo")
>>> print(clause.compile().params)
{'foo':None}
>>> print(clause.params({"foo": 7}).compile().params)
{'foo':7}
```

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)replace_selectable(*old:FromClause*, *alias:Alias*) → Self

*inherited from the* [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) *method of* [Selectable](#sqlalchemy.sql.expression.Selectable)

Replace all occurrences of [FromClause](#sqlalchemy.sql.expression.FromClause)
‘old’ with the given [Alias](#sqlalchemy.sql.expression.Alias)
object, returning a copy of this [FromClause](#sqlalchemy.sql.expression.FromClause).

Deprecated since version 1.4: The [Selectable.replace_selectable()](#sqlalchemy.sql.expression.Selectable.replace_selectable) method is deprecated, and will be removed in a future release.  Similar functionality is available via the sqlalchemy.sql.visitors module.

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)scalar_subquery() → [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect)[Any]

*inherited from the* [SelectBase.scalar_subquery()](#sqlalchemy.sql.expression.SelectBase.scalar_subquery) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a ‘scalar’ representation of this selectable, which can be
used as a column expression.

The returned object is an instance of [ScalarSelect](#sqlalchemy.sql.expression.ScalarSelect).

Typically, a select statement which has only one column in its columns
clause is eligible to be used as a scalar expression.  The scalar
subquery can then be used in the WHERE clause or columns clause of
an enclosing SELECT.

Note that the scalar subquery differentiates from the FROM-level
subquery that can be produced using the
[SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
method.

See also

[Scalar and Correlated Subqueries](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-scalar-subquery) - in the 2.0 tutorial

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)select(**arg:Any*, ***kw:Any*) → [Select](#sqlalchemy.sql.expression.Select)

*inherited from the* [SelectBase.select()](#sqlalchemy.sql.expression.SelectBase.select) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Deprecated since version 1.4: The [SelectBase.select()](#sqlalchemy.sql.expression.SelectBase.select) method is deprecated and will be removed in a future release; this method implicitly creates a subquery that should be explicit.  Please call [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) first in order to create a subquery, which then can be selected.

     attribute [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)selected_columns

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
representing the columns that
this SELECT statement or similar construct returns in its result set,
not including [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause) constructs.

This collection differs from the [FromClause.columns](#sqlalchemy.sql.expression.FromClause.columns)
collection of a [FromClause](#sqlalchemy.sql.expression.FromClause) in that the columns
within this collection cannot be directly nested inside another SELECT
statement; a subquery must be applied first which provides for the
necessary parenthesization required by SQL.

For a [TextualSelect](#sqlalchemy.sql.expression.TextualSelect) construct, the collection
contains the [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects that were
passed to the constructor, typically via the
[TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method.

Added in version 1.4.

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)self_group(*against:OperatorType|None=None*) → [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

*inherited from the* [ClauseElement.self_group()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.self_group) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.TextualSelect.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.TextualSelect.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)set_label_style(*style:SelectLabelStyle*) → [TextualSelect](#sqlalchemy.sql.expression.TextualSelect)

Return a new selectable with the specified label style.

Implemented by subclasses.

    method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)subquery(*name:str|None=None*) → [Subquery](#sqlalchemy.sql.expression.Subquery)

*inherited from the* [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery) *method of* [SelectBase](#sqlalchemy.sql.expression.SelectBase)

Return a subquery of this [SelectBase](#sqlalchemy.sql.expression.SelectBase).

A subquery is from a SQL perspective a parenthesized, named
construct that can be placed in the FROM clause of another
SELECT statement.

Given a SELECT statement such as:

```
stmt = select(table.c.id, table.c.name)
```

The above statement might look like:

```
SELECT table.id, table.name FROM table
```

The subquery form by itself renders the same way, however when
embedded into the FROM clause of another SELECT statement, it becomes
a named sub-element:

```
subq = stmt.subquery()
new_stmt = select(subq)
```

The above renders as:

```
SELECT anon_1.id, anon_1.name
FROM (SELECT table.id, table.name FROM table) AS anon_1
```

Historically, [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
is equivalent to calling
the [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias)
method on a FROM object; however,
as a [SelectBase](#sqlalchemy.sql.expression.SelectBase)
object is not directly  FROM object,
the [SelectBase.subquery()](#sqlalchemy.sql.expression.SelectBase.subquery)
method provides clearer semantics.

Added in version 1.4.

     method [sqlalchemy.sql.expression.TextualSelect.](#sqlalchemy.sql.expression.TextualSelect)unique_params(*_ClauseElement__optionaldict:Dict[str,Any]|None=None*, ***kwargs:Any*) → Self

*inherited from the* [ClauseElement.unique_params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.unique_params) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Same functionality as [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params),
except adds unique=True
to affected bind parameters so that multiple statements can be
used.

     class sqlalchemy.sql.expression.Values

*inherits from* `sqlalchemy.sql.roles.InElementRole`, [sqlalchemy.sql.expression.HasCTE](#sqlalchemy.sql.expression.HasCTE), `sqlalchemy.sql.expression.Generative`, `sqlalchemy.sql.expression.LateralFromClause`

Represent a `VALUES` construct that can be used as a FROM element
in a statement.

The [Values](#sqlalchemy.sql.expression.Values) object is created from the
[values()](#sqlalchemy.sql.expression.values) function.

Added in version 1.4.

| Member Name | Description |
| --- | --- |
| add_cte() | Add one or moreCTEconstructs to this statement. |
| alias() | Return a newValuesconstruct that is a copy of this
one with the given name. |
| compile() | Compile this SQL expression. |
| cte() | Return a newCTE,
or Common Table Expression instance. |
| data() | Return a newValuesconstruct,
adding the given data to the data list. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| lateral() | Return a newValueswith the lateral flag set,
so that
it renders as LATERAL. |
| name_cte_columns | indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause. |
| scalar_values() | Returns a scalarVALUESconstruct that can be used as a
COLUMN element in a statement. |
| table_valued() | Return aTableValuedColumnobject for thisFromClause. |

   method [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)add_cte(**ctes:CTE*, *nest_here:bool=False*) → Self

*inherited from the* [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Add one or more [CTE](#sqlalchemy.sql.expression.CTE) constructs to this statement.

This method will associate the given [CTE](#sqlalchemy.sql.expression.CTE) constructs with
the parent statement such that they will each be unconditionally
rendered in the WITH clause of the final statement, even if not
referenced elsewhere within the statement or any sub-selects.

The optional [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here) parameter when set
to True will have the effect that each given [CTE](#sqlalchemy.sql.expression.CTE) will
render in a WITH clause rendered directly along with this statement,
rather than being moved to the top of the ultimate rendered statement,
even if this statement is rendered as a subquery within a larger
statement.

This method has two general uses. One is to embed CTE statements that
serve some purpose without being referenced explicitly, such as the use
case of embedding a DML statement such as an INSERT or UPDATE as a CTE
inline with a primary statement that may draw from its results
indirectly.  The other is to provide control over the exact placement
of a particular series of CTE constructs that should remain rendered
directly in terms of a particular statement that may be nested in a
larger statement.

E.g.:

```
from sqlalchemy import table, column, select

t = table("t", column("c1"), column("c2"))

ins = t.insert().values({"c1": "x", "c2": "y"}).cte()

stmt = select(t).add_cte(ins)
```

Would render:

```
WITH anon_1 AS (
    INSERT INTO t (c1, c2) VALUES (:param_1, :param_2)
)
SELECT t.c1, t.c2
FROM t
```

Above, the “anon_1” CTE is not referenced in the SELECT
statement, however still accomplishes the task of running an INSERT
statement.

Similarly in a DML-related context, using the PostgreSQL
[Insert](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert) construct to generate an “upsert”:

```
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import insert

t = table("t", column("c1"), column("c2"))

delete_statement_cte = t.delete().where(t.c.c1 < 1).cte("deletions")

insert_stmt = insert(t).values({"c1": 1, "c2": 2})
update_statement = insert_stmt.on_conflict_do_update(
    index_elements=[t.c.c1],
    set_={
        "c1": insert_stmt.excluded.c1,
        "c2": insert_stmt.excluded.c2,
    },
).add_cte(delete_statement_cte)

print(update_statement)
```

The above statement renders as:

```
WITH deletions AS (
    DELETE FROM t WHERE t.c1 < %(c1_1)s
)
INSERT INTO t (c1, c2) VALUES (%(c1)s, %(c2)s)
ON CONFLICT (c1) DO UPDATE SET c1 = excluded.c1, c2 = excluded.c2
```

Added in version 1.4.21.

   Parameters:

- ***ctes** –
  zero or more [CTE](#sqlalchemy.sql.expression.CTE) constructs.
  Changed in version 2.0: Multiple CTE instances are accepted
- **nest_here** –
  if True, the given CTE or CTEs will be rendered
  as though they specified the [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting) flag
  to `True` when they were added to this [HasCTE](#sqlalchemy.sql.expression.HasCTE).
  Assuming the given CTEs are not referenced in an outer-enclosing
  statement as well, the CTEs given should render at the level of
  this statement when this flag is given.
  Added in version 2.0.
  See also
  [HasCTE.cte.nesting](#sqlalchemy.sql.expression.HasCTE.cte.params.nesting)

      method [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)alias(*name:str|None=None*, *flat:bool=False*) → Self

Return a new [Values](#sqlalchemy.sql.expression.Values)
construct that is a copy of this
one with the given name.

This method is a VALUES-specific specialization of the
[FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias) method.

See also

[Using Aliases](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-using-aliases)

[alias()](#sqlalchemy.sql.expression.alias)

     method [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

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

     method [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)cte(*name:str|None=None*, *recursive:bool=False*, *nesting:bool=False*) → [CTE](#sqlalchemy.sql.expression.CTE)

*inherited from the* [HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte) *method of* [HasCTE](#sqlalchemy.sql.expression.HasCTE)

Return a new [CTE](#sqlalchemy.sql.expression.CTE),
or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT
statements can draw upon secondary statements specified along
with the primary statement, using a clause called “WITH”.
Special semantics regarding UNION can also be employed to
allow “recursive” queries, where a SELECT statement can draw
upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT
and DELETE on some databases, both as a source of CTE rows
when combined with RETURNING, as well as a consumer of
CTE rows.

SQLAlchemy detects [CTE](#sqlalchemy.sql.expression.CTE) objects, which are treated
similarly to [Alias](#sqlalchemy.sql.expression.Alias) objects, as special elements
to be delivered to the FROM clause of the statement as well
as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and
“NOT MATERIALIZED”, the `CTE.prefix_with()`
method may be
used to establish these.

Changed in version 1.3.13: Added support for prefixes.
In particular - MATERIALIZED and NOT MATERIALIZED.

   Parameters:

- **name** – name given to the common table expression.  Like
  [FromClause.alias()](#sqlalchemy.sql.expression.FromClause.alias), the name can be left as
  `None` in which case an anonymous symbol will be used at query
  compile time.
- **recursive** – if `True`, will render `WITH RECURSIVE`.
  A recursive common table expression is intended to be used in
  conjunction with UNION ALL in order to derive rows
  from those already selected.
- **nesting** –
  if `True`, will render the CTE locally to the
  statement in which it is referenced.   For more complex scenarios,
  the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method using the
  [HasCTE.add_cte.nest_here](#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here)
  parameter may also be used to more carefully
  control the exact placement of a particular CTE.
  Added in version 1.4.24.
  See also
  [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte)

The following examples include two from PostgreSQL’s documentation at
[https://www.postgresql.org/docs/current/static/queries-with.html](https://www.postgresql.org/docs/current/static/queries-with.html),
as well as additional examples.

Example 1, non recursive:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("region", String),
    Column("amount", Integer),
    Column("product", String),
    Column("quantity", Integer),
)

regional_sales = (
    select(orders.c.region, func.sum(orders.c.amount).label("total_sales"))
    .group_by(orders.c.region)
    .cte("regional_sales")
)

top_regions = (
    select(regional_sales.c.region)
    .where(
        regional_sales.c.total_sales
        > select(func.sum(regional_sales.c.total_sales) / 10)
    )
    .cte("top_regions")
)

statement = (
    select(
        orders.c.region,
        orders.c.product,
        func.sum(orders.c.quantity).label("product_units"),
        func.sum(orders.c.amount).label("product_sales"),
    )
    .where(orders.c.region.in_(select(top_regions.c.region)))
    .group_by(orders.c.region, orders.c.product)
)

result = conn.execute(statement).fetchall()
```

Example 2, WITH RECURSIVE:

```
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    MetaData,
    select,
    func,
)

metadata = MetaData()

parts = Table(
    "parts",
    metadata,
    Column("part", String),
    Column("sub_part", String),
    Column("quantity", Integer),
)

included_parts = (
    select(parts.c.sub_part, parts.c.part, parts.c.quantity)
    .where(parts.c.part == "our part")
    .cte(recursive=True)
)

incl_alias = included_parts.alias()
parts_alias = parts.alias()
included_parts = included_parts.union_all(
    select(
        parts_alias.c.sub_part, parts_alias.c.part, parts_alias.c.quantity
    ).where(parts_alias.c.part == incl_alias.c.sub_part)
)

statement = select(
    included_parts.c.sub_part,
    func.sum(included_parts.c.quantity).label("total_quantity"),
).group_by(included_parts.c.sub_part)

result = conn.execute(statement).fetchall()
```

Example 3, an upsert using UPDATE and INSERT with CTEs:

```
from datetime import date
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Date,
    select,
    literal,
    and_,
    exists,
)

metadata = MetaData()

visitors = Table(
    "visitors",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("date", Date, primary_key=True),
    Column("count", Integer),
)

# add 5 visitors for the product_id == 1
product_id = 1
day = date.today()
count = 5

update_cte = (
    visitors.update()
    .where(
        and_(visitors.c.product_id == product_id, visitors.c.date == day)
    )
    .values(count=visitors.c.count + count)
    .returning(literal(1))
    .cte("update_cte")
)

upsert = visitors.insert().from_select(
    [visitors.c.product_id, visitors.c.date, visitors.c.count],
    select(literal(product_id), literal(day), literal(count)).where(
        ~exists(update_cte.select())
    ),
)

connection.execute(upsert)
```

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte(
    "value_a", nesting=True
)

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = select(value_a_nested.c.n).cte("value_b")

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

The above query will render the second CTE nested inside the first,
shown with inline parameters below as:

```
WITH
    value_a AS
        (SELECT 'root' AS n),
    value_b AS
        (WITH value_a AS
            (SELECT 'nesting' AS n)
        SELECT value_a.n AS n FROM value_a)
SELECT value_a.n AS a, value_b.n AS b
FROM value_a, value_b
```

The same CTE can be set up using the [HasCTE.add_cte()](#sqlalchemy.sql.expression.HasCTE.add_cte) method
as follows (SQLAlchemy 2.0 and above):

```
value_a = select(literal("root").label("n")).cte("value_a")

# A nested CTE with the same name as the root one
value_a_nested = select(literal("nesting").label("n")).cte("value_a")

# Nesting CTEs takes ascendency locally
# over the CTEs at a higher level
value_b = (
    select(value_a_nested.c.n)
    .add_cte(value_a_nested, nest_here=True)
    .cte("value_b")
)

value_ab = select(value_a.c.n.label("a"), value_b.c.n.label("b"))
```

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

```
edge = Table(
    "edge",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("left", Integer),
    Column("right", Integer),
)

root_node = select(literal(1).label("node")).cte("nodes", recursive=True)

left_edge = select(edge.c.left).join(
    root_node, edge.c.right == root_node.c.node
)
right_edge = select(edge.c.right).join(
    root_node, edge.c.left == root_node.c.node
)

subgraph_cte = root_node.union(left_edge, right_edge)

subgraph = select(subgraph_cte)
```

The above query will render 2 UNIONs inside the recursive CTE:

```
WITH RECURSIVE nodes(node) AS (
        SELECT 1 AS node
    UNION
        SELECT edge."left" AS "left"
        FROM edge JOIN nodes ON edge."right" = nodes.node
    UNION
        SELECT edge."right" AS "right"
        FROM edge JOIN nodes ON edge."left" = nodes.node
)
SELECT nodes.node FROM nodes
```

See also

[Query.cte()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.cte) - ORM version of
[HasCTE.cte()](#sqlalchemy.sql.expression.HasCTE.cte).

     method [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)data(*values:Sequence[Tuple[Any,...]]*) → Self

Return a new [Values](#sqlalchemy.sql.expression.Values) construct,
adding the given data to the data list.

E.g.:

```
my_values = my_values.data([(1, "value 1"), (2, "value2")])
```

   Parameters:

**values** – a sequence (i.e. list) of tuples that map to the
column expressions given in the [Values](#sqlalchemy.sql.expression.Values)
constructor.

      attribute [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)inherit_cache = None

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

     method [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)lateral(*name:str|None=None*) → Self

Return a new [Values](#sqlalchemy.sql.expression.Values) with the lateral flag set,
so that
it renders as LATERAL.

See also

[lateral()](#sqlalchemy.sql.expression.lateral)

     attribute [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)name_cte_columns = True

indicates if this HasCTE as contained within a CTE should compel the CTE
to render the column names of this object in the WITH clause.

Added in version 2.0.42.

     method [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)scalar_values() → [ScalarValues](#sqlalchemy.sql.expression.ScalarValues)

Returns a scalar `VALUES` construct that can be used as a
COLUMN element in a statement.

Added in version 2.0.0b4.

     method [sqlalchemy.sql.expression.Values.](#sqlalchemy.sql.expression.Values)table_valued() → TableValuedColumn[Any]

*inherited from the* `NamedFromClause.table_valued()` *method of* `NamedFromClause`

Return a `TableValuedColumn` object for this
[FromClause](#sqlalchemy.sql.expression.FromClause).

A `TableValuedColumn` is a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) that
represents a complete row in a table. Support for this construct is
backend dependent, and is supported in various forms by backends
such as PostgreSQL, Oracle Database and SQL Server.

E.g.:

```
>>> from sqlalchemy import select, column, func, table
>>> a = table("a", column("id"), column("x"), column("y"))
>>> stmt = select(func.row_to_json(a.table_valued()))
>>> print(stmt)
SELECT row_to_json(a) AS row_to_json_1
FROM a
```

Added in version 1.4.0b2.

See also

[Working with SQL Functions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-functions) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

      class sqlalchemy.sql.expression.ScalarValues

*inherits from* `sqlalchemy.sql.roles.InElementRole`, `sqlalchemy.sql.expression.GroupedElement`, [sqlalchemy.sql.expression.ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

Represent a scalar `VALUES` construct that can be used as a
COLUMN element in a statement.

The [ScalarValues](#sqlalchemy.sql.expression.ScalarValues) object is created from the
[Values.scalar_values()](#sqlalchemy.sql.expression.Values.scalar_values) method. It’s also
automatically generated when a [Values](#sqlalchemy.sql.expression.Values) is used in
an `IN` or `NOT IN` condition.

Added in version 2.0.0b4.

## Label Style Constants

Constants used with the [GenerativeSelect.set_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.set_label_style)
method.

| Object Name | Description |
| --- | --- |
| SelectLabelStyle | Label style constants that may be passed toSelect.set_label_style(). |

   class sqlalchemy.sql.expression.SelectLabelStyle

*inherits from* `enum.Enum`

Label style constants that may be passed to
[Select.set_label_style()](#sqlalchemy.sql.expression.Select.set_label_style).

| Member Name | Description |
| --- | --- |
| LABEL_STYLE_DEFAULT | The default label style, refers toLABEL_STYLE_DISAMBIGUATE_ONLY. |
| LABEL_STYLE_DISAMBIGUATE_ONLY | Label style indicating that columns with a name that conflicts with
an existing name should be labeled with a semi-anonymizing label
when generating the columns clause of a SELECT statement. |
| LABEL_STYLE_NONE | Label style indicating no automatic labeling should be applied to the
columns clause of a SELECT statement. |
| LABEL_STYLE_TABLENAME_PLUS_COL | Label style indicating all columns should be labeled as<tablename>_<columnname>when generating the columns clause of a SELECT
statement, to disambiguate same-named columns referenced from different
tables, aliases, or subqueries. |

   attribute [sqlalchemy.sql.expression.SelectLabelStyle.](#sqlalchemy.sql.expression.SelectLabelStyle)LABEL_STYLE_DEFAULT = 2

The default label style, refers to
`LABEL_STYLE_DISAMBIGUATE_ONLY`.

Added in version 1.4.

     attribute [sqlalchemy.sql.expression.SelectLabelStyle.](#sqlalchemy.sql.expression.SelectLabelStyle)LABEL_STYLE_DISAMBIGUATE_ONLY = 2

Label style indicating that columns with a name that conflicts with
an existing name should be labeled with a semi-anonymizing label
when generating the columns clause of a SELECT statement.

Below, most column names are left unaffected, except for the second
occurrence of the name `columna`, which is labeled using the
label `columna_1` to disambiguate it from that of `tablea.columna`:

```
>>> from sqlalchemy import (
...     table,
...     column,
...     select,
...     true,
...     LABEL_STYLE_DISAMBIGUATE_ONLY,
... )
>>> table1 = table("table1", column("columna"), column("columnb"))
>>> table2 = table("table2", column("columna"), column("columnc"))
>>> print(
...     select(table1, table2)
...     .join(table2, true())
...     .set_label_style(LABEL_STYLE_DISAMBIGUATE_ONLY)
... )
SELECT table1.columna, table1.columnb, table2.columna AS columna_1, table2.columnc
FROM table1 JOIN table2 ON true
```

Used with the [GenerativeSelect.set_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.set_label_style) method,
`LABEL_STYLE_DISAMBIGUATE_ONLY` is the default labeling style
for all SELECT statements outside of [1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style) ORM queries.

Added in version 1.4.

     attribute [sqlalchemy.sql.expression.SelectLabelStyle.](#sqlalchemy.sql.expression.SelectLabelStyle)LABEL_STYLE_NONE = 0

Label style indicating no automatic labeling should be applied to the
columns clause of a SELECT statement.

Below, the columns named `columna` are both rendered as is, meaning that
the name `columna` can only refer to the first occurrence of this name
within a result set, as well as if the statement were used as a subquery:

```
>>> from sqlalchemy import table, column, select, true, LABEL_STYLE_NONE
>>> table1 = table("table1", column("columna"), column("columnb"))
>>> table2 = table("table2", column("columna"), column("columnc"))
>>> print(
...     select(table1, table2)
...     .join(table2, true())
...     .set_label_style(LABEL_STYLE_NONE)
... )
SELECT table1.columna, table1.columnb, table2.columna, table2.columnc
FROM table1 JOIN table2 ON true
```

Used with the [Select.set_label_style()](#sqlalchemy.sql.expression.Select.set_label_style) method.

Added in version 1.4.

     attribute [sqlalchemy.sql.expression.SelectLabelStyle.](#sqlalchemy.sql.expression.SelectLabelStyle)LABEL_STYLE_TABLENAME_PLUS_COL = 1

Label style indicating all columns should be labeled as
`<tablename>_<columnname>` when generating the columns clause of a SELECT
statement, to disambiguate same-named columns referenced from different
tables, aliases, or subqueries.

Below, all column names are given a label so that the two same-named
columns `columna` are disambiguated as `table1_columna` and
`table2_columna`:

```
>>> from sqlalchemy import (
...     table,
...     column,
...     select,
...     true,
...     LABEL_STYLE_TABLENAME_PLUS_COL,
... )
>>> table1 = table("table1", column("columna"), column("columnb"))
>>> table2 = table("table2", column("columna"), column("columnc"))
>>> print(
...     select(table1, table2)
...     .join(table2, true())
...     .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
... )
SELECT table1.columna AS table1_columna, table1.columnb AS table1_columnb, table2.columna AS table2_columna, table2.columnc AS table2_columnc
FROM table1 JOIN table2 ON true
```

Used with the [GenerativeSelect.set_label_style()](#sqlalchemy.sql.expression.GenerativeSelect.set_label_style) method.
Equivalent to the legacy method `Select.apply_labels()`;
`LABEL_STYLE_TABLENAME_PLUS_COL` is SQLAlchemy’s legacy
auto-labeling style. `LABEL_STYLE_DISAMBIGUATE_ONLY` provides a
less intrusive approach to disambiguation of same-named column expressions.

Added in version 1.4.

See also

[Select.set_label_style()](#sqlalchemy.sql.expression.Select.set_label_style)

[Select.get_label_style()](#sqlalchemy.sql.expression.Select.get_label_style)
