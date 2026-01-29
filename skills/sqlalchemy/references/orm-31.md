# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

ORM Querying Guide

This page is part of the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).

Previous: [ORM API Features for Querying](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html)

# Legacy Query API

About the Legacy Query API

This page contains the Python generated documentation for the
[Query](#sqlalchemy.orm.Query) construct, which for many years was the sole SQL
interface when working with the SQLAlchemy ORM.  As of version 2.0, an all
new way of working is now the standard approach, where the same
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct that works for Core works just as well for the
ORM, providing a consistent interface for building queries.

For any application that is built on the SQLAlchemy ORM prior to the
2.0 API, the [Query](#sqlalchemy.orm.Query) API will usually represents the vast
majority of database access code within an application, and as such the
majority of the [Query](#sqlalchemy.orm.Query) API is
**not being removed from SQLAlchemy**.  The [Query](#sqlalchemy.orm.Query) object
behind the scenes now translates itself into a 2.0 style [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
object when the [Query](#sqlalchemy.orm.Query) object is executed, so it now is
just a very thin adapter API.

For a guide to migrating an application based on [Query](#sqlalchemy.orm.Query)
to 2.0 style, see [2.0 Migration - ORM Usage](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage).

For an introduction to writing SQL for ORM objects in the 2.0 style,
start with the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial).  Additional reference for 2.0 style
querying is at [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).

## The Query Object

[Query](#sqlalchemy.orm.Query) is produced in terms of a given [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), using the [Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query) method:

```
q = session.query(SomeMappedClass)
```

Following is the full interface for the [Query](#sqlalchemy.orm.Query) object.

| Object Name | Description |
| --- | --- |
| Query | ORM-level SQL construction object. |

   class sqlalchemy.orm.Query

*inherits from* `sqlalchemy.sql.expression._SelectFromElements`, `sqlalchemy.sql.annotation.SupportsCloneAnnotations`, [sqlalchemy.sql.expression.HasPrefixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes), [sqlalchemy.sql.expression.HasSuffixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes), `sqlalchemy.sql.expression.HasHints`, `sqlalchemy.event.registry.EventTarget`, [sqlalchemy.log.Identified](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.log.Identified), `sqlalchemy.sql.expression.Generative`, [sqlalchemy.sql.expression.Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable), `typing.Generic`

ORM-level SQL construction object.

Legacy Feature

The ORM [Query](#sqlalchemy.orm.Query) object is a legacy construct
as of SQLAlchemy 2.0.   See the notes at the top of
[Legacy Query API](#) for an overview, including links to migration
documentation.

[Query](#sqlalchemy.orm.Query) objects are normally initially generated using the
[Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query) method of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), and in
less common cases by instantiating the [Query](#sqlalchemy.orm.Query) directly and
associating with a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) using the
[Query.with_session()](#sqlalchemy.orm.Query.with_session)
method.

| Member Name | Description |
| --- | --- |
| __init__() | Construct aQuerydirectly. |
| add_column() | Add a column expression to the list of result columns to be
returned. |
| add_columns() | Add one or more column expressions to the list
of result columns to be returned. |
| add_entity() | add a mapped entity to the list of result columns
to be returned. |
| all() | Return the results represented by thisQueryas a list. |
| apply_labels() |  |
| as_scalar() | Return the full SELECT statement represented by thisQuery, converted to a scalar subquery. |
| autoflush() | Return a Query with a specific ‘autoflush’ setting. |
| correlate() | Return aQueryconstruct which will correlate the given
FROM clauses to that of an enclosingQueryorselect(). |
| count() | Return a count of rows this the SQL formed by thisQuerywould return. |
| cte() | Return the full SELECT statement represented by thisQueryrepresented as a common table expression (CTE). |
| delete() | Perform a DELETE with an arbitrary WHERE clause. |
| distinct() | Apply aDISTINCTto the query and return the newly resultingQuery. |
| enable_assertions() | Control whether assertions are generated. |
| enable_eagerloads() | Control whether or not eager joins and subqueries are
rendered. |
| except_() | Produce an EXCEPT of this Query against one or more queries. |
| except_all() | Produce an EXCEPT ALL of this Query against one or more queries. |
| execution_options() | Set non-SQL options which take effect during execution. |
| exists() | A convenience method that turns a query into an EXISTS subquery
of the form EXISTS (SELECT 1 FROM … WHERE …). |
| filter() | Apply the given filtering criterion to a copy
of thisQuery, using SQL expressions. |
| filter_by() | Apply the given filtering criterion to a copy
of thisQuery, using keyword expressions. |
| first() | Return the first result of thisQueryor
None if the result doesn’t contain any row. |
| from_statement() | Execute the given SELECT statement and return results. |
| get() | Return an instance based on the given primary key identifier,
orNoneif not found. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| get_execution_options() | Get the non-SQL options which will take effect during execution. |
| group_by() | Apply one or more GROUP BY criterion to the query and return
the newly resultingQuery. |
| having() | Apply a HAVING criterion to the query and return the
newly resultingQuery. |
| instances() | Return an ORM result given aCursorResultandQueryContext. |
| intersect() | Produce an INTERSECT of this Query against one or more queries. |
| intersect_all() | Produce an INTERSECT ALL of this Query against one or more queries. |
| join() | Create a SQL JOIN against thisQueryobject’s criterion
and apply generatively, returning the newly resultingQuery. |
| label() | Return the full SELECT statement represented by thisQuery, converted
to a scalar subquery with a label of the given name. |
| limit() | Apply aLIMITto the query and return the newly resultingQuery. |
| merge_result() | Merge a result into thisQueryobject’s Session. |
| offset() | Apply anOFFSETto the query and return the newly resultingQuery. |
| one() | Return exactly one result or raise an exception. |
| one_or_none() | Return at most one result or raise an exception. |
| only_return_tuples() | When set to True, the query results will always be aRowobject. |
| options() | Return a newQueryobject,
applying the given list of
mapper options. |
| order_by() | Apply one or more ORDER BY criteria to the query and return
the newly resultingQuery. |
| outerjoin() | Create a left outer join against thisQueryobject’s criterion
and apply generatively, returning the newly resultingQuery. |
| params() | Add values for bind parameters which may have been
specified in filter(). |
| populate_existing() | Return aQuerythat will expire and refresh all instances
as they are loaded, or reused from the currentSession. |
| prefix_with() | Add one or more expressions following the statement keyword, i.e.
SELECT, INSERT, UPDATE, or DELETE. Generative. |
| reset_joinpoint() | Return a newQuery, where the “join point” has
been reset back to the base FROM entities of the query. |
| scalar() | Return the first element of the first result or None
if no rows present.  If multiple rows are returned,
raisesMultipleResultsFound. |
| scalar_subquery() | Return the full SELECT statement represented by thisQuery, converted to a scalar subquery. |
| select_from() | Set the FROM clause of thisQueryexplicitly. |
| set_label_style() | Apply column labels to the return value of Query.statement. |
| slice() | Computes the “slice” of theQueryrepresented by
the given indices and returns the resultingQuery. |
| subquery() | Return the full SELECT statement represented by
thisQuery, embedded within anAlias. |
| suffix_with() | Add one or more expressions following the statement as a whole. |
| tuples() | return a tuple-typed form of thisQuery. |
| union() | Produce a UNION of this Query against one or more queries. |
| union_all() | Produce a UNION ALL of this Query against one or more queries. |
| update() | Perform an UPDATE with an arbitrary WHERE clause. |
| value() | Return a scalar result corresponding to the given
column expression. |
| values() | Return an iterator yielding result tuples corresponding
to the given list of columns |
| where() | A synonym forQuery.filter(). |
| with_entities() | Return a newQueryreplacing the SELECT list with the
given entities. |
| with_for_update() | return a newQuerywith the specified options for theFORUPDATEclause. |
| with_hint() | Add an indexing or other executional context hint for the given
selectable to thisSelector other selectable
object. |
| with_labels() |  |
| with_parent() | Add filtering criterion that relates the given instance
to a child object or collection, using its attribute state
as well as an establishedrelationship()configuration. |
| with_session() | Return aQuerythat will use the givenSession. |
| with_statement_hint() | Add a statement hint to thisSelector
other selectable object. |
| with_transformation() | Return a newQueryobject transformed by
the given function. |
| yield_per() | Yield onlycountrows at a time. |

   method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)__init__(*entities:_ColumnsClauseArgument[Any]|Sequence[_ColumnsClauseArgument[Any]]*, *session:Session|None=None*)

Construct a [Query](#sqlalchemy.orm.Query) directly.

E.g.:

```
q = Query([User, Address], session=some_session)
```

The above is equivalent to:

```
q = some_session.query(User, Address)
```

   Parameters:

- **entities** – a sequence of entities and/or SQL expressions.
- **session** – a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with which the
  [Query](#sqlalchemy.orm.Query)
  will be associated.   Optional; a [Query](#sqlalchemy.orm.Query)
  can be associated
  with a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) generatively via the
  [Query.with_session()](#sqlalchemy.orm.Query.with_session) method as well.

See also

[Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query)

[Query.with_session()](#sqlalchemy.orm.Query.with_session)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)add_column(*column:_ColumnExpressionArgument[Any]*) → [Query](#sqlalchemy.orm.Query)[Any]

Add a column expression to the list of result columns to be
returned.

Deprecated since version 1.4: [Query.add_column()](#sqlalchemy.orm.Query.add_column) is deprecated and will be removed in a future release.  Please use [Query.add_columns()](#sqlalchemy.orm.Query.add_columns)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)add_columns(**column:_ColumnExpressionArgument[Any]*) → [Query](#sqlalchemy.orm.Query)[Any]

Add one or more column expressions to the list
of result columns to be returned.

See also

[Select.add_columns()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.add_columns) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)add_entity(*entity:_EntityType[Any]*, *alias:Alias|Subquery|None=None*) → [Query](#sqlalchemy.orm.Query)[Any]

add a mapped entity to the list of result columns
to be returned.

See also

[Select.add_columns()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.add_columns) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)all() → List[_T]

Return the results represented by this [Query](#sqlalchemy.orm.Query)
as a list.

This results in an execution of the underlying SQL statement.

Warning

The [Query](#sqlalchemy.orm.Query) object,
when asked to return either
a sequence or iterator that consists of full ORM-mapped entities,
will **deduplicate entries based on primary key**.  See the FAQ for
more details.

> See also
>
>
>
> [My Query does not return the same number of objects as query.count() tells me - why?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#faq-query-deduplicating)

See also

[Result.all()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.all) - v2 comparable method.

[Result.scalars()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalars) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)apply_labels() → Self

Deprecated since version 2.0: The [Query.with_labels()](#sqlalchemy.orm.Query.with_labels) and [Query.apply_labels()](#sqlalchemy.orm.Query.apply_labels) method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. Use set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL) instead. (Background on SQLAlchemy 2.0 at: [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html))

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)as_scalar() → [ScalarSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect)[Any]

Return the full SELECT statement represented by this
[Query](#sqlalchemy.orm.Query), converted to a scalar subquery.

Deprecated since version 1.4: The [Query.as_scalar()](#sqlalchemy.orm.Query.as_scalar) method is deprecated and will be removed in a future release.  Please refer to [Query.scalar_subquery()](#sqlalchemy.orm.Query.scalar_subquery).

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)autoflush(*setting:bool*) → Self

Return a Query with a specific ‘autoflush’ setting.

As of SQLAlchemy 1.4, the [Query.autoflush()](#sqlalchemy.orm.Query.autoflush) method
is equivalent to using the `autoflush` execution option at the
ORM level. See the section [Autoflush](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-autoflush) for
further background on this option.

    property column_descriptions: List[ORMColumnDescription]

Return metadata about the columns which would be
returned by this [Query](#sqlalchemy.orm.Query).

Format is a list of dictionaries:

```
user_alias = aliased(User, name="user2")
q = sess.query(User, User.id, user_alias)

# this expression:
q.column_descriptions

# would return:
[
    {
        "name": "User",
        "type": User,
        "aliased": False,
        "expr": User,
        "entity": User,
    },
    {
        "name": "id",
        "type": Integer(),
        "aliased": False,
        "expr": User.id,
        "entity": User,
    },
    {
        "name": "user2",
        "type": User,
        "aliased": True,
        "expr": user_alias,
        "entity": user_alias,
    },
]
```

See also

This API is available using [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) queries as well,
documented at:

- [Inspecting entities and columns from ORM-enabled SELECT and DML statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-inspection)
- [Select.column_descriptions](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.column_descriptions)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)correlate(**fromclauses:Literal[None,False]|FromClauseRole|TypedColumnsClauseRole[Any]|Type[Any]|Inspectable[_HasClauseElement[Any]]|_HasClauseElement[Any]*) → Self

Return a [Query](#sqlalchemy.orm.Query) construct which will correlate the given
FROM clauses to that of an enclosing [Query](#sqlalchemy.orm.Query) or
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).

The method here accepts mapped classes, [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) constructs,
and [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) constructs as arguments, which are resolved
into expression constructs, in addition to appropriate expression
constructs.

The correlation arguments are ultimately passed to
[Select.correlate()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate)
after coercion to expression constructs.

The correlation arguments take effect in such cases
as when `Query.from_self()` is used, or when
a subquery as returned by [Query.subquery()](#sqlalchemy.orm.Query.subquery) is
embedded in another [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct.

See also

[Select.correlate()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)count() → int

Return a count of rows this the SQL formed by this [Query](#sqlalchemy.orm.Query)
would return.

This generates the SQL for this Query as follows:

```
SELECT count(1) AS count_1 FROM (
    SELECT <rest of query follows...>
) AS anon_1
```

The above SQL returns a single row, which is the aggregate value
of the count function; the [Query.count()](#sqlalchemy.orm.Query.count)
method then returns
that single integer value.

Warning

It is important to note that the value returned by
count() is **not the same as the number of ORM objects that this
Query would return from a method such as the .all() method**.
The [Query](#sqlalchemy.orm.Query) object,
when asked to return full entities,
will **deduplicate entries based on primary key**, meaning if the
same primary key value would appear in the results more than once,
only one object of that primary key would be present.  This does
not apply to a query that is against individual columns.

See also

[My Query does not return the same number of objects as query.count() tells me - why?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#faq-query-deduplicating)

For fine grained control over specific columns to count, to skip the
usage of a subquery or otherwise control of the FROM clause, or to use
other aggregate functions, use [expression.func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func)
expressions in conjunction with [Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query), i.e.:

```
from sqlalchemy import func

# count User records, without
# using a subquery.
session.query(func.count(User.id))

# return count of user "id" grouped
# by "name"
session.query(func.count(User.id)).group_by(User.name)

from sqlalchemy import distinct

# count distinct "name" values
session.query(func.count(distinct(User.name)))
```

See also

[2.0 Migration - ORM Usage](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)cte(*name:str|None=None*, *recursive:bool=False*, *nesting:bool=False*) → [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE)

Return the full SELECT statement represented by this
[Query](#sqlalchemy.orm.Query) represented as a common table expression (CTE).

Parameters and usage are the same as those of the
[SelectBase.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase.cte) method; see that method for
further details.

Here is the [PostgreSQL WITH
RECURSIVE example](https://www.postgresql.org/docs/current/static/queries-with.html).
Note that, in this example, the `included_parts` cte and the
`incl_alias` alias of it are Core selectables, which
means the columns are accessed via the `.c.` attribute.  The
`parts_alias` object is an [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) instance of the
`Part` entity, so column-mapped attributes are available
directly:

```
from sqlalchemy.orm import aliased

class Part(Base):
    __tablename__ = "part"
    part = Column(String, primary_key=True)
    sub_part = Column(String, primary_key=True)
    quantity = Column(Integer)

included_parts = (
    session.query(Part.sub_part, Part.part, Part.quantity)
    .filter(Part.part == "our part")
    .cte(name="included_parts", recursive=True)
)

incl_alias = aliased(included_parts, name="pr")
parts_alias = aliased(Part, name="p")
included_parts = included_parts.union_all(
    session.query(
        parts_alias.sub_part, parts_alias.part, parts_alias.quantity
    ).filter(parts_alias.part == incl_alias.c.sub_part)
)

q = session.query(
    included_parts.c.sub_part,
    func.sum(included_parts.c.quantity).label("total_quantity"),
).group_by(included_parts.c.sub_part)
```

See also

[Select.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.cte) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)delete(*synchronize_session:SynchronizeSessionArgument='auto'*, *delete_args:Dict[Any,Any]|None=None*) → int

Perform a DELETE with an arbitrary WHERE clause.

Deletes rows matched by this query from the database.

E.g.:

```
sess.query(User).filter(User.age == 25).delete(synchronize_session=False)

sess.query(User).filter(User.age == 25).delete(
    synchronize_session="evaluate"
)
```

Warning

See the section [ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete) for important
caveats and warnings, including limitations when using bulk UPDATE
and DELETE with mapper inheritance configurations.

   Parameters:

- **synchronize_session** – chooses the strategy to update the
  attributes on objects in the session.   See the section
  [ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete) for a discussion of these
  strategies.
- **delete_args** –
  Optional dictionary, if present will be passed
  to the underlying [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) construct as the `**kw`
  for the object.  May be used to pass dialect-specific arguments such
  as `mysql_limit`.
  Added in version 2.0.37.

  Returns:

the count of rows matched as returned by the database’s
“row count” feature.

See also

[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)distinct(**expr:_ColumnExpressionArgument[Any]*) → Self

Apply a `DISTINCT` to the query and return the newly resulting
`Query`.

Note

The ORM-level [distinct()](#sqlalchemy.orm.Query.distinct) call includes logic that will
automatically add columns from the ORDER BY of the query to the
columns clause of the SELECT statement, to satisfy the common need
of the database backend that ORDER BY columns be part of the SELECT
list when DISTINCT is used.   These columns *are not* added to the
list of columns actually fetched by the [Query](#sqlalchemy.orm.Query),
however,
so would not affect results. The columns are passed through when
using the [Query.statement](#sqlalchemy.orm.Query.statement) accessor, however.

Deprecated since version 2.0: This logic is deprecated and will be removed
in SQLAlchemy 2.0.     See [Using DISTINCT with additional columns, but only select the entity](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-distinct)
for a description of this use case in 2.0.

See also

[Select.distinct()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.distinct) - v2 equivalent method.

   Parameters:

***expr** –

optional column expressions.  When present,
the PostgreSQL dialect will render a `DISTINCT ON (<expressions>)`
construct.

Deprecated since version 1.4: Using *expr in other dialects is deprecated
and will raise [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) in a future version.

       method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)enable_assertions(*value:bool*) → Self

Control whether assertions are generated.

When set to False, the returned Query will
not assert its state before certain operations,
including that LIMIT/OFFSET has not been applied
when filter() is called, no criterion exists
when get() is called, and no “from_statement()”
exists when filter()/order_by()/group_by() etc.
is called.  This more permissive mode is used by
custom Query subclasses to specify criterion or
other modifiers outside of the usual usage patterns.

Care should be taken to ensure that the usage
pattern is even possible.  A statement applied
by from_statement() will override any criterion
set by filter() or order_by(), for example.

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)enable_eagerloads(*value:bool*) → Self

Control whether or not eager joins and subqueries are
rendered.

When set to False, the returned Query will not render
eager joins regardless of [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload),
[subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload) options
or mapper-level `lazy='joined'`/`lazy='subquery'`
configurations.

This is used primarily when nesting the Query’s
statement into a subquery or other
selectable, or when using [Query.yield_per()](#sqlalchemy.orm.Query.yield_per).

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)except_(**q:Query*) → Self

Produce an EXCEPT of this Query against one or more queries.

Works the same way as `Query.union()`. See
that method for usage examples.

See also

[Select.except_()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.except_) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)except_all(**q:Query*) → Self

Produce an EXCEPT ALL of this Query against one or more queries.

Works the same way as `Query.union()`. See
that method for usage examples.

See also

[Select.except_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.except_all) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)execution_options(***kwargs:Any*) → Self

Set non-SQL options which take effect during execution.

Options allowed here include all of those accepted by
[Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options), as well as a series
of ORM specific options:

`populate_existing=True` - equivalent to using
[Query.populate_existing()](#sqlalchemy.orm.Query.populate_existing)

`autoflush=True|False` - equivalent to using
[Query.autoflush()](#sqlalchemy.orm.Query.autoflush)

`yield_per=<value>` - equivalent to using
[Query.yield_per()](#sqlalchemy.orm.Query.yield_per)

Note that the `stream_results` execution option is enabled
automatically if the `Query.yield_per()`
method or execution option is used.

Added in version 1.4: - added ORM options to
[Query.execution_options()](#sqlalchemy.orm.Query.execution_options)

The execution options may also be specified on a per execution basis
when using [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) queries via the
[Session.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.execution_options) parameter.

Warning

The
[Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results)
parameter should not be used at the level of individual ORM
statement executions, as the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will not track
objects from different schema translate maps within a single
session.  For multiple schema translate maps within the scope of a
single [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), see [Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-sharding).

See also

[Using Server Side Cursors (a.k.a. stream results)](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results)

[Query.get_execution_options()](#sqlalchemy.orm.Query.get_execution_options)

[Select.execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.execution_options) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)exists() → [Exists](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Exists)

A convenience method that turns a query into an EXISTS subquery
of the form EXISTS (SELECT 1 FROM … WHERE …).

e.g.:

```
q = session.query(User).filter(User.name == "fred")
session.query(q.exists())
```

Producing SQL similar to:

```
SELECT EXISTS (
    SELECT 1 FROM users WHERE users.name = :name_1
) AS anon_1
```

The EXISTS construct is usually used in the WHERE clause:

```
session.query(User.id).filter(q.exists()).scalar()
```

Note that some databases such as SQL Server don’t allow an
EXISTS expression to be present in the columns clause of a
SELECT.    To select a simple boolean value based on the exists
as a WHERE, use [literal()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal):

```
from sqlalchemy import literal

session.query(literal(True)).filter(q.exists()).scalar()
```

See also

[Select.exists()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.exists) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)filter(**criterion:_ColumnExpressionArgument[bool]*) → Self

Apply the given filtering criterion to a copy
of this [Query](#sqlalchemy.orm.Query), using SQL expressions.

e.g.:

```
session.query(MyClass).filter(MyClass.name == "some name")
```

Multiple criteria may be specified as comma separated; the effect
is that they will be joined together using the [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_)
function:

```
session.query(MyClass).filter(MyClass.name == "some name", MyClass.id > 5)
```

The criterion is any SQL expression object applicable to the
WHERE clause of a select.   String expressions are coerced
into SQL expression constructs via the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
construct.

See also

[Query.filter_by()](#sqlalchemy.orm.Query.filter_by) - filter on keyword expressions.

[Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)filter_by(***kwargs:Any*) → Self

Apply the given filtering criterion to a copy
of this [Query](#sqlalchemy.orm.Query), using keyword expressions.

e.g.:

```
session.query(MyClass).filter_by(name="some name")
```

Multiple criteria may be specified as comma separated; the effect
is that they will be joined together using the [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_)
function:

```
session.query(MyClass).filter_by(name="some name", id=5)
```

The keyword expressions are extracted from the primary
entity of the query, or the last entity that was the
target of a call to [Query.join()](#sqlalchemy.orm.Query.join).

See also

[Query.filter()](#sqlalchemy.orm.Query.filter) - filter on SQL expressions.

[Select.filter_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.filter_by) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)first() → _T | None

Return the first result of this `Query` or
None if the result doesn’t contain any row.

first() applies a limit of one within the generated SQL, so that
only one primary entity row is generated on the server side
(note this may consist of multiple result rows if join-loaded
collections are present).

Calling [Query.first()](#sqlalchemy.orm.Query.first)
results in an execution of the underlying
query.

See also

[Query.one()](#sqlalchemy.orm.Query.one)

[Query.one_or_none()](#sqlalchemy.orm.Query.one_or_none)

[Result.first()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.first) - v2 comparable method.

[Result.scalars()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalars) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)from_statement(*statement:ExecutableReturnsRows*) → Self

Execute the given SELECT statement and return results.

This method bypasses all internal statement compilation, and the
statement is executed without modification.

The statement is typically either a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
or [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct, and should return the set
of columns
appropriate to the entity class represented by this
[Query](#sqlalchemy.orm.Query).

See also

[Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)get(*ident:_PKIdentityArgument*) → _T | None

Return an instance based on the given primary key identifier,
or `None` if not found.

Deprecated since version 2.0: The [Query.get()](#sqlalchemy.orm.Query.get) method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) (Background on SQLAlchemy 2.0 at: [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html))

E.g.:

```
my_user = session.query(User).get(5)

some_object = session.query(VersionedFoo).get((5, 10))

some_object = session.query(VersionedFoo).get({"id": 5, "version_id": 10})
```

[Query.get()](#sqlalchemy.orm.Query.get) is special in that it provides direct
access to the identity map of the owning [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
If the given primary key identifier is present
in the local identity map, the object is returned
directly from this collection and no SQL is emitted,
unless the object has been marked fully expired.
If not present,
a SELECT is performed in order to locate the object.

[Query.get()](#sqlalchemy.orm.Query.get) also will perform a check if
the object is present in the identity map and
marked as expired - a SELECT
is emitted to refresh the object as well as to
ensure that the row is still present.
If not, [ObjectDeletedError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.ObjectDeletedError) is raised.

[Query.get()](#sqlalchemy.orm.Query.get) is only used to return a single
mapped instance, not multiple instances or
individual column constructs, and strictly
on a single primary key value.  The originating
[Query](#sqlalchemy.orm.Query) must be constructed in this way,
i.e. against a single mapped entity,
with no additional filtering criterion.  Loading
options via [Query.options()](#sqlalchemy.orm.Query.options) may be applied
however, and will be used if the object is not
yet locally present.

  Parameters:

**ident** –

A scalar, tuple, or dictionary representing the
primary key.  For a composite (e.g. multiple column) primary key,
a tuple or dictionary should be passed.

For a single-column primary key, the scalar calling form is typically
the most expedient.  If the primary key of a row is the value “5”,
the call looks like:

```
my_object = query.get(5)
```

The tuple form contains primary key values typically in
the order in which they correspond to the mapped
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object’s primary key columns, or if the
[Mapper.primary_key](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.primary_key) configuration parameter were
used, in
the order used for that parameter. For example, if the primary key
of a row is represented by the integer
digits “5, 10” the call would look like:

```
my_object = query.get((5, 10))
```

The dictionary form should include as keys the mapped attribute names
corresponding to each element of the primary key.  If the mapped class
has the attributes `id`, `version_id` as the attributes which
store the object’s primary key value, the call would look like:

```
my_object = query.get({"id": 5, "version_id": 10})
```

Added in version 1.3: the [Query.get()](#sqlalchemy.orm.Query.get)
method now optionally
accepts a dictionary of attribute names to values in order to
indicate a primary key identifier.

   Returns:

The object instance, or `None`.

      method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)get_execution_options() → _ImmutableExecuteOptions

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

See also

[Query.execution_options()](#sqlalchemy.orm.Query.execution_options)

[Select.get_execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.get_execution_options) - v2 comparable method.

     property get_label_style: [SelectLabelStyle](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectLabelStyle)

Retrieve the current label style.

Added in version 1.4.

See also

[Select.get_label_style()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.get_label_style) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)group_by(*_Query__first:Literal[None,False,_NoArg.NO_ARG]|_ColumnExpressionOrStrLabelArgument[Any]=_NoArg.NO_ARG*, **clauses:_ColumnExpressionOrStrLabelArgument[Any]*) → Self

Apply one or more GROUP BY criterion to the query and return
the newly resulting [Query](#sqlalchemy.orm.Query).

All existing GROUP BY settings can be suppressed by
passing `None` - this will suppress any GROUP BY configured
on mappers as well.

See also

These sections describe GROUP BY in terms of [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style)
invocation but apply to [Query](#sqlalchemy.orm.Query) as well:

[Aggregate functions with GROUP BY / HAVING](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-group-by-w-aggregates) - in the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Select.group_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.group_by) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)having(**having:_ColumnExpressionArgument[bool]*) → Self

Apply a HAVING criterion to the query and return the
newly resulting [Query](#sqlalchemy.orm.Query).

[Query.having()](#sqlalchemy.orm.Query.having) is used in conjunction with
[Query.group_by()](#sqlalchemy.orm.Query.group_by).

HAVING criterion makes it possible to use filters on aggregate
functions like COUNT, SUM, AVG, MAX, and MIN, eg.:

```
q = (
    session.query(User.id)
    .join(User.addresses)
    .group_by(User.id)
    .having(func.count(Address.id) > 2)
)
```

See also

[Select.having()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.having) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)instances(*result_proxy:CursorResult[Any]*, *context:QueryContext|None=None*) → Any

Return an ORM result given a [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) and
[QueryContext](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryContext).

Deprecated since version 2.0: The [Query.instances()](#sqlalchemy.orm.Query.instances) method is deprecated and will be removed in a future release. Use the Select.from_statement() method or aliased() construct in conjunction with Session.execute() instead.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)intersect(**q:Query*) → Self

Produce an INTERSECT of this Query against one or more queries.

Works the same way as `Query.union()`. See
that method for usage examples.

See also

[Select.intersect()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.intersect) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)intersect_all(**q:Query*) → Self

Produce an INTERSECT ALL of this Query against one or more queries.

Works the same way as `Query.union()`. See
that method for usage examples.

See also

[Select.intersect_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.intersect_all) - v2 equivalent method.

     property is_single_entity: bool

Indicates if this [Query](#sqlalchemy.orm.Query)
returns tuples or single entities.

Returns True if this query returns a single entity for each instance
in its result list, and False if this query returns a tuple of entities
for each result.

Added in version 1.3.11.

See also

[Query.only_return_tuples()](#sqlalchemy.orm.Query.only_return_tuples)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)join(*target:_JoinTargetArgument*, *onclause:_OnClauseArgument|None=None*, ***, *isouter:bool=False*, *full:bool=False*) → Self

Create a SQL JOIN against this [Query](#sqlalchemy.orm.Query)
object’s criterion
and apply generatively, returning the newly resulting
[Query](#sqlalchemy.orm.Query).

**Simple Relationship Joins**

Consider a mapping between two classes `User` and `Address`,
with a relationship `User.addresses` representing a collection
of `Address` objects associated with each `User`.   The most
common usage of [Query.join()](#sqlalchemy.orm.Query.join)
is to create a JOIN along this
relationship, using the `User.addresses` attribute as an indicator
for how this should occur:

```
q = session.query(User).join(User.addresses)
```

Where above, the call to [Query.join()](#sqlalchemy.orm.Query.join) along
`User.addresses` will result in SQL approximately equivalent to:

```
SELECT user.id, user.name
FROM user JOIN address ON user.id = address.user_id
```

In the above example we refer to `User.addresses` as passed to
[Query.join()](#sqlalchemy.orm.Query.join) as the “on clause”, that is, it indicates
how the “ON” portion of the JOIN should be constructed.

To construct a chain of joins, multiple [Query.join()](#sqlalchemy.orm.Query.join)
calls may be used.  The relationship-bound attribute implies both
the left and right side of the join at once:

```
q = (
    session.query(User)
    .join(User.orders)
    .join(Order.items)
    .join(Item.keywords)
)
```

Note

as seen in the above example, **the order in which each
call to the join() method occurs is important**.    Query would not,
for example, know how to join correctly if we were to specify
`User`, then `Item`, then `Order`, in our chain of joins; in
such a case, depending on the arguments passed, it may raise an
error that it doesn’t know how to join, or it may produce invalid
SQL in which case the database will raise an error. In correct
practice, the
[Query.join()](#sqlalchemy.orm.Query.join) method is invoked in such a way that lines
up with how we would want the JOIN clauses in SQL to be
rendered, and each call should represent a clear link from what
precedes it.

**Joins to a Target Entity or Selectable**

A second form of [Query.join()](#sqlalchemy.orm.Query.join) allows any mapped entity or
core selectable construct as a target.   In this usage,
[Query.join()](#sqlalchemy.orm.Query.join) will attempt to create a JOIN along the
natural foreign key relationship between two entities:

```
q = session.query(User).join(Address)
```

In the above calling form, [Query.join()](#sqlalchemy.orm.Query.join) is called upon to
create the “on clause” automatically for us.  This calling form will
ultimately raise an error if either there are no foreign keys between
the two entities, or if there are multiple foreign key linkages between
the target entity and the entity or entities already present on the
left side such that creating a join requires more information.  Note
that when indicating a join to a target without any ON clause, ORM
configured relationships are not taken into account.

**Joins to a Target with an ON Clause**

The third calling form allows both the target entity as well
as the ON clause to be passed explicitly.    A example that includes
a SQL expression as the ON clause is as follows:

```
q = session.query(User).join(Address, User.id == Address.user_id)
```

The above form may also use a relationship-bound attribute as the
ON clause as well:

```
q = session.query(User).join(Address, User.addresses)
```

The above syntax can be useful for the case where we wish
to join to an alias of a particular target entity.  If we wanted
to join to `Address` twice, it could be achieved using two
aliases set up using the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) function:

```
a1 = aliased(Address)
a2 = aliased(Address)

q = (
    session.query(User)
    .join(a1, User.addresses)
    .join(a2, User.addresses)
    .filter(a1.email_address == "[email protected]")
    .filter(a2.email_address == "[email protected]")
)
```

The relationship-bound calling form can also specify a target entity
using the [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) method; a query
equivalent to the one above would be:

```
a1 = aliased(Address)
a2 = aliased(Address)

q = (
    session.query(User)
    .join(User.addresses.of_type(a1))
    .join(User.addresses.of_type(a2))
    .filter(a1.email_address == "[email protected]")
    .filter(a2.email_address == "[email protected]")
)
```

**Augmenting Built-in ON Clauses**

As a substitute for providing a full custom ON condition for an
existing relationship, the [PropComparator.and_()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.and_) function
may be applied to a relationship attribute to augment additional
criteria into the ON clause; the additional criteria will be combined
with the default criteria using AND:

```
q = session.query(User).join(
    User.addresses.and_(Address.email_address != "[email protected]")
)
```

Added in version 1.4.

**Joining to Tables and Subqueries**

The target of a join may also be any table or SELECT statement,
which may be related to a target entity or not.   Use the
appropriate `.subquery()` method in order to make a subquery
out of a query:

```
subq = (
    session.query(Address)
    .filter(Address.email_address == "[email protected]")
    .subquery()
)

q = session.query(User).join(subq, User.id == subq.c.user_id)
```

Joining to a subquery in terms of a specific relationship and/or
target entity may be achieved by linking the subquery to the
entity using [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased):

```
subq = (
    session.query(Address)
    .filter(Address.email_address == "[email protected]")
    .subquery()
)

address_subq = aliased(Address, subq)

q = session.query(User).join(User.addresses.of_type(address_subq))
```

**Controlling what to Join From**

In cases where the left side of the current state of
[Query](#sqlalchemy.orm.Query) is not in line with what we want to join from,
the [Query.select_from()](#sqlalchemy.orm.Query.select_from) method may be used:

```
q = (
    session.query(Address)
    .select_from(User)
    .join(User.addresses)
    .filter(User.name == "ed")
)
```

Which will produce SQL similar to:

```
SELECT address.* FROM user
    JOIN address ON user.id=address.user_id
    WHERE user.name = :name_1
```

See also

[Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) - v2 equivalent method.

   Parameters:

- ***props** – Incoming arguments for [Query.join()](#sqlalchemy.orm.Query.join),
  the props collection in modern use should be considered to be a  one
  or two argument form, either as a single “target” entity or ORM
  attribute-bound relationship, or as a target entity plus an “on
  clause” which  may be a SQL expression or ORM attribute-bound
  relationship.
- **isouter=False** – If True, the join used will be a left outer join,
  just as if the [Query.outerjoin()](#sqlalchemy.orm.Query.outerjoin) method were called.
- **full=False** – render FULL OUTER JOIN; implies `isouter`.

      method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)label(*name:str|None*) → [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label)[Any]

Return the full SELECT statement represented by this
[Query](#sqlalchemy.orm.Query), converted
to a scalar subquery with a label of the given name.

See also

[Select.label()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.label) - v2 comparable method.

     property lazy_loaded_from: [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState)[Any] | None

An [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) that is using this [Query](#sqlalchemy.orm.Query)
for a lazy load operation.

Deprecated since version 1.4: This attribute should be viewed via the
[ORMExecuteState.lazy_loaded_from](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.lazy_loaded_from) attribute, within
the context of the [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute)
event.

See also

[ORMExecuteState.lazy_loaded_from](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.lazy_loaded_from)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)limit(*limit:_LimitOffsetType*) → Self

Apply a `LIMIT` to the query and return the newly resulting
`Query`.

See also

[Select.limit()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.limit) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)merge_result(*iterator:FrozenResult[Any]|Iterable[Sequence[Any]]|Iterable[object]*, *load:bool=True*) → [FrozenResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.FrozenResult)[Any] | Iterable[Any]

Merge a result into this [Query](#sqlalchemy.orm.Query) object’s Session.

Deprecated since version 2.0: The [Query.merge_result()](#sqlalchemy.orm.Query.merge_result) method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is superseded by the [merge_frozen_result()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.merge_frozen_result) function. (Background on SQLAlchemy 2.0 at: [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html))

Given an iterator returned by a [Query](#sqlalchemy.orm.Query)
of the same structure
as this one, return an identical iterator of results, with all mapped
instances merged into the session using [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge). This
is an optimized method which will merge all mapped instances,
preserving the structure of the result rows and unmapped columns with
less method overhead than that of calling [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge)
explicitly for each value.

The structure of the results is determined based on the column list of
this [Query](#sqlalchemy.orm.Query) - if these do not correspond,
unchecked errors
will occur.

The ‘load’ argument is the same as that of [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge).

For an example of how [Query.merge_result()](#sqlalchemy.orm.Query.merge_result) is used, see
the source code for the example [Dogpile Caching](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-caching), where
[Query.merge_result()](#sqlalchemy.orm.Query.merge_result) is used to efficiently restore state
from a cache back into a target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)offset(*offset:_LimitOffsetType*) → Self

Apply an `OFFSET` to the query and return the newly resulting
`Query`.

See also

[Select.offset()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.offset) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)one() → _T

Return exactly one result or raise an exception.

Raises [NoResultFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoResultFound) if the query selects no rows.
Raises [MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound) if multiple object identities
are returned, or if multiple rows are returned for a query that returns
only scalar values as opposed to full identity-mapped entities.

Calling [one()](#sqlalchemy.orm.Query.one) results in an execution of the underlying query.

See also

[Query.first()](#sqlalchemy.orm.Query.first)

[Query.one_or_none()](#sqlalchemy.orm.Query.one_or_none)

[Result.one()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.one) - v2 comparable method.

[Result.scalar_one()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalar_one) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)one_or_none() → _T | None

Return at most one result or raise an exception.

Returns `None` if the query selects
no rows.  Raises `sqlalchemy.orm.exc.MultipleResultsFound`
if multiple object identities are returned, or if multiple
rows are returned for a query that returns only scalar values
as opposed to full identity-mapped entities.

Calling [Query.one_or_none()](#sqlalchemy.orm.Query.one_or_none)
results in an execution of the
underlying query.

See also

[Query.first()](#sqlalchemy.orm.Query.first)

[Query.one()](#sqlalchemy.orm.Query.one)

[Result.one_or_none()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.one_or_none) - v2 comparable method.

[Result.scalar_one_or_none()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalar_one_or_none) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)only_return_tuples(*value:bool*) → [Query](#sqlalchemy.orm.Query)

When set to True, the query results will always be a
[Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) object.

This can change a query that normally returns a single entity
as a scalar to return a [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) result in all cases.

See also

[Query.tuples()](#sqlalchemy.orm.Query.tuples) - returns tuples, but also at the typing
level will type results as `Tuple`.

[Query.is_single_entity()](#sqlalchemy.orm.Query.is_single_entity)

[Result.tuples()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.tuples) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)options(**args:ExecutableOption*) → Self

Return a new [Query](#sqlalchemy.orm.Query) object,
applying the given list of
mapper options.

Most supplied options regard changing how column- and
relationship-mapped attributes are loaded.

See also

[Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#loading-columns)

[Relationship Loading with Loader Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#relationship-loader-options)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)order_by(*_Query__first:Literal[None,False,_NoArg.NO_ARG]|_ColumnExpressionOrStrLabelArgument[Any]=_NoArg.NO_ARG*, **clauses:_ColumnExpressionOrStrLabelArgument[Any]*) → Self

Apply one or more ORDER BY criteria to the query and return
the newly resulting [Query](#sqlalchemy.orm.Query).

e.g.:

```
q = session.query(Entity).order_by(Entity.id, Entity.name)
```

Calling this method multiple times is equivalent to calling it once
with all the clauses concatenated. All existing ORDER BY criteria may
be cancelled by passing `None` by itself.  New ORDER BY criteria may
then be added by invoking [Query.order_by()](#sqlalchemy.orm.Query.order_by) again, e.g.:

```
# will erase all ORDER BY and ORDER BY new_col alone
q = q.order_by(None).order_by(new_col)
```

See also

These sections describe ORDER BY in terms of [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style)
invocation but apply to [Query](#sqlalchemy.orm.Query) as well:

[ORDER BY](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Ordering or Grouping by a Label](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-order-by-label) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)outerjoin(*target:_JoinTargetArgument*, *onclause:_OnClauseArgument|None=None*, ***, *full:bool=False*) → Self

Create a left outer join against this `Query` object’s criterion
and apply generatively, returning the newly resulting `Query`.

Usage is the same as the `join()` method.

See also

[Select.outerjoin()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.outerjoin) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)params(*_Query__params:Dict[str,Any]|None=None*, ***kw:Any*) → Self

Add values for bind parameters which may have been
specified in filter().

Parameters may be specified using **kwargs, or optionally a single
dictionary as the first positional argument. The reason for both is
that **kwargs is convenient, however some parameter dictionaries
contain unicode keys in which case **kwargs cannot be used.

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)populate_existing() → Self

Return a [Query](#sqlalchemy.orm.Query)
that will expire and refresh all instances
as they are loaded, or reused from the current [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

As of SQLAlchemy 1.4, the [Query.populate_existing()](#sqlalchemy.orm.Query.populate_existing) method
is equivalent to using the `populate_existing` execution option at
the ORM level. See the section [Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing)
for further background on this option.

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)prefix_with(**prefixes:_TextCoercedExpressionArgument[Any]*, *dialect:str='*'*) → Self

*inherited from the* [HasPrefixes.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes.prefix_with) *method of* [HasPrefixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes)

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
to [HasPrefixes.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes.prefix_with).

  Parameters:

- ***prefixes** – textual or [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  construct which
  will be rendered following the INSERT, UPDATE, or DELETE
  keyword.
- **dialect** – optional string dialect name which will
  limit rendering of this prefix to only that dialect.

      method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)reset_joinpoint() → Self

Return a new [Query](#sqlalchemy.orm.Query), where the “join point” has
been reset back to the base FROM entities of the query.

This method is usually used in conjunction with the
`aliased=True` feature of the [Query.join()](#sqlalchemy.orm.Query.join)
method.  See the example in [Query.join()](#sqlalchemy.orm.Query.join) for how
this is used.

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)scalar() → Any

Return the first element of the first result or None
if no rows present.  If multiple rows are returned,
raises [MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound).

```
>>> session.query(Item).scalar()
<Item>
>>> session.query(Item.id).scalar()
1
>>> session.query(Item.id).filter(Item.id < 0).scalar()
None
>>> session.query(Item.id, Item.name).scalar()
1
>>> session.query(func.count(Parent.id)).scalar()
20
```

This results in an execution of the underlying query.

See also

[Result.scalar()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalar) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)scalar_subquery() → [ScalarSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect)[Any]

Return the full SELECT statement represented by this
[Query](#sqlalchemy.orm.Query), converted to a scalar subquery.

Analogous to
[SelectBase.scalar_subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase.scalar_subquery).

Changed in version 1.4: The [Query.scalar_subquery()](#sqlalchemy.orm.Query.scalar_subquery)
method replaces the [Query.as_scalar()](#sqlalchemy.orm.Query.as_scalar) method.

See also

[Select.scalar_subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.scalar_subquery) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)select_from(**from_obj:FromClauseRole|TypedColumnsClauseRole[Any]|Type[Any]|Inspectable[_HasClauseElement[Any]]|_HasClauseElement[Any]*) → Self

Set the FROM clause of this [Query](#sqlalchemy.orm.Query) explicitly.

[Query.select_from()](#sqlalchemy.orm.Query.select_from) is often used in conjunction with
[Query.join()](#sqlalchemy.orm.Query.join) in order to control which entity is selected
from on the “left” side of the join.

The entity or selectable object here effectively replaces the
“left edge” of any calls to [Query.join()](#sqlalchemy.orm.Query.join), when no
joinpoint is otherwise established - usually, the default “join
point” is the leftmost entity in the [Query](#sqlalchemy.orm.Query) object’s
list of entities to be selected.

A typical example:

```
q = (
    session.query(Address)
    .select_from(User)
    .join(User.addresses)
    .filter(User.name == "ed")
)
```

Which produces SQL equivalent to:

```
SELECT address.* FROM user
JOIN address ON user.id=address.user_id
WHERE user.name = :name_1
```

   Parameters:

***from_obj** – collection of one or more entities to apply
to the FROM clause.  Entities can be mapped classes,
[AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) objects, [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects
as well as core [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) elements like subqueries.

See also

[Query.join()](#sqlalchemy.orm.Query.join)

`Query.select_entity_from()`

[Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) - v2 equivalent method.

     property selectable: [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)[_T] | FromStatement[_T] | [UpdateBase](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase)

Return the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object emitted by this
[Query](#sqlalchemy.orm.Query).

Used for [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) compatibility, this is equivalent to:

```
query.enable_eagerloads(False).with_labels().statement
```

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)set_label_style(*style:SelectLabelStyle*) → Self

Apply column labels to the return value of Query.statement.

Indicates that this Query’s statement accessor should return
a SELECT statement that applies labels to all columns in the
form <tablename>_<columnname>; this is commonly used to
disambiguate columns from multiple tables which have the same
name.

When the Query actually issues SQL to load rows, it always
uses column labeling.

Note

The [Query.set_label_style()](#sqlalchemy.orm.Query.set_label_style) method *only* applies
the output of [Query.statement](#sqlalchemy.orm.Query.statement), and *not* to any of
the result-row invoking systems of [Query](#sqlalchemy.orm.Query) itself,
e.g.
[Query.first()](#sqlalchemy.orm.Query.first), [Query.all()](#sqlalchemy.orm.Query.all), etc.
To execute
a query using [Query.set_label_style()](#sqlalchemy.orm.Query.set_label_style), invoke the
[Query.statement](#sqlalchemy.orm.Query.statement) using [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute):

```
result = session.execute(
    query.set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).statement
)
```

Added in version 1.4.

See also

[Select.set_label_style()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.set_label_style) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)slice(*start:int*, *stop:int*) → Self

Computes the “slice” of the [Query](#sqlalchemy.orm.Query) represented by
the given indices and returns the resulting [Query](#sqlalchemy.orm.Query).

The start and stop indices behave like the argument to Python’s
built-in `range()` function. This method provides an
alternative to using `LIMIT`/`OFFSET` to get a slice of the
query.

For example,

```
session.query(User).order_by(User.id).slice(1, 3)
```

renders as

```
SELECT users.id AS users_id,
       users.name AS users_name
FROM users ORDER BY users.id
LIMIT ? OFFSET ?
(2, 1)
```

See also

[Query.limit()](#sqlalchemy.orm.Query.limit)

[Query.offset()](#sqlalchemy.orm.Query.offset)

[Select.slice()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.slice) - v2 equivalent method.

     property statement: [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)[_T] | FromStatement[_T] | [UpdateBase](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase)

The full SELECT statement represented by this Query.

The statement by default will not have disambiguating labels
applied to the construct unless with_labels(True) is called
first.

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)subquery(*name:str|None=None*, *with_labels:bool=False*, *reduce_columns:bool=False*) → [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery)

Return the full SELECT statement represented by
this [Query](#sqlalchemy.orm.Query), embedded within an
[Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias).

Eager JOIN generation within the query is disabled.

See also

[Select.subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.subquery) - v2 comparable method.

   Parameters:

- **name** – string name to be assigned as the alias;
  this is passed through to [FromClause.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.alias).
  If `None`, a name will be deterministically generated
  at compile time.
- **with_labels** – if True, [with_labels()](#sqlalchemy.orm.Query.with_labels) will be called
  on the [Query](#sqlalchemy.orm.Query) first to apply table-qualified labels
  to all columns.
- **reduce_columns** – if True,
  [Select.reduce_columns()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.reduce_columns) will
  be called on the resulting [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct,
  to remove same-named columns where one also refers to the other
  via foreign key or WHERE clause equivalence.

      method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)suffix_with(**suffixes:_TextCoercedExpressionArgument[Any]*, *dialect:str='*'*) → Self

*inherited from the* [HasSuffixes.suffix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes.suffix_with) *method of* [HasSuffixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes)

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
to [HasSuffixes.suffix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes.suffix_with).

  Parameters:

- ***suffixes** – textual or [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  construct which
  will be rendered following the target clause.
- **dialect** – Optional string dialect name which will
  limit rendering of this suffix to only that dialect.

      method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)tuples() → [Query](#sqlalchemy.orm.Query)

return a tuple-typed form of this [Query](#sqlalchemy.orm.Query).

This method invokes the [Query.only_return_tuples()](#sqlalchemy.orm.Query.only_return_tuples)
method with a value of `True`, which by itself ensures that this
[Query](#sqlalchemy.orm.Query) will always return [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects, even
if the query is made against a single entity.  It then also
at the typing level will return a “typed” query, if possible,
that will type result rows as `Tuple` objects with typed
elements.

This method can be compared to the [Result.tuples()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.tuples) method,
which returns “self”, but from a typing perspective returns an object
that will yield typed `Tuple` objects for results.   Typing
takes effect only if this [Query](#sqlalchemy.orm.Query) object is a typed
query object already.

Added in version 2.0.

See also

[Result.tuples()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.tuples) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)union(**q:Query*) → Self

Produce a UNION of this Query against one or more queries.

e.g.:

```
q1 = sess.query(SomeClass).filter(SomeClass.foo == "bar")
q2 = sess.query(SomeClass).filter(SomeClass.bar == "foo")

q3 = q1.union(q2)
```

The method accepts multiple Query objects so as to control
the level of nesting.  A series of `union()` calls such as:

```
x.union(y).union(z).all()
```

will nest on each `union()`, and produces:

```
SELECT * FROM (SELECT * FROM (SELECT * FROM X UNION
                SELECT * FROM y) UNION SELECT * FROM Z)
```

Whereas:

```
x.union(y, z).all()
```

produces:

```
SELECT * FROM (SELECT * FROM X UNION SELECT * FROM y UNION
                SELECT * FROM Z)
```

Note that many database backends do not allow ORDER BY to
be rendered on a query called within UNION, EXCEPT, etc.
To disable all ORDER BY clauses including those configured
on mappers, issue `query.order_by(None)` - the resulting
[Query](#sqlalchemy.orm.Query) object will not render ORDER BY within
its SELECT statement.

See also

[Select.union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.union) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)union_all(**q:Query*) → Self

Produce a UNION ALL of this Query against one or more queries.

Works the same way as `Query.union()`. See
that method for usage examples.

See also

[Select.union_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.union_all) - v2 equivalent method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)update(*values:Dict[_DMLColumnArgument,Any]*, *synchronize_session:SynchronizeSessionArgument='auto'*, *update_args:Dict[Any,Any]|None=None*) → int

Perform an UPDATE with an arbitrary WHERE clause.

Updates rows matched by this query in the database.

E.g.:

```
sess.query(User).filter(User.age == 25).update(
    {User.age: User.age - 10}, synchronize_session=False
)

sess.query(User).filter(User.age == 25).update(
    {"age": User.age - 10}, synchronize_session="evaluate"
)
```

Warning

See the section [ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete) for important
caveats and warnings, including limitations when using arbitrary
UPDATE and DELETE with mapper inheritance configurations.

   Parameters:

- **values** – a dictionary with attributes names, or alternatively
  mapped attributes or SQL expressions, as keys, and literal
  values or sql expressions as values.   If [parameter-ordered
  mode](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-parameter-ordered-updates) is desired, the values can
  be passed as a list of 2-tuples; this requires that the
  [update.preserve_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update.params.preserve_parameter_order)
  flag is passed to the [Query.update.update_args](#sqlalchemy.orm.Query.update.params.update_args) dictionary
  as well.
- **synchronize_session** – chooses the strategy to update the
  attributes on objects in the session.   See the section
  [ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete) for a discussion of these
  strategies.
- **update_args** – Optional dictionary, if present will be passed
  to the underlying [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) construct as the `**kw`
  for the object.  May be used to pass dialect-specific arguments such
  as `mysql_limit`, as well as other special arguments such as
  [update.preserve_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update.params.preserve_parameter_order).

  Returns:

the count of rows matched as returned by the database’s
“row count” feature.

See also

[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)value(*column:_ColumnExpressionArgument[Any]*) → Any

Return a scalar result corresponding to the given
column expression.

Deprecated since version 1.4: [Query.value()](#sqlalchemy.orm.Query.value) is deprecated and will be removed in a future release.  Please use [Query.with_entities()](#sqlalchemy.orm.Query.with_entities) in combination with [Query.scalar()](#sqlalchemy.orm.Query.scalar)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)values(**columns:_ColumnsClauseArgument[Any]*) → Iterable[Any]

Return an iterator yielding result tuples corresponding
to the given list of columns

Deprecated since version 1.4: [Query.values()](#sqlalchemy.orm.Query.values) is deprecated and will be removed in a future release.  Please use [Query.with_entities()](#sqlalchemy.orm.Query.with_entities)

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)where(**criterion:_ColumnExpressionArgument[bool]*) → Self

A synonym for [Query.filter()](#sqlalchemy.orm.Query.filter).

Added in version 1.4.

See also

[Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where) - v2 equivalent method.

     property whereclause: [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool] | None

A readonly attribute which returns the current WHERE criterion for
this Query.

This returned value is a SQL expression construct, or `None` if no
criterion has been established.

See also

[Select.whereclause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.whereclause) - v2 equivalent property.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)with_entities(**entities:_ColumnsClauseArgument[Any]*, ***_Query__kw:Any*) → [Query](#sqlalchemy.orm.Query)[Any]

Return a new [Query](#sqlalchemy.orm.Query)
replacing the SELECT list with the
given entities.

e.g.:

```
# Users, filtered on some arbitrary criterion
# and then ordered by related email address
q = (
    session.query(User)
    .join(User.address)
    .filter(User.name.like("%ed%"))
    .order_by(Address.email)
)

# given *only* User.id==5, Address.email, and 'q', what
# would the *next* User in the result be ?
subq = (
    q.with_entities(Address.email)
    .order_by(None)
    .filter(User.id == 5)
    .subquery()
)
q = q.join((subq, subq.c.email < Address.email)).limit(1)
```

See also

[Select.with_only_columns()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_only_columns) - v2 comparable method.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)with_for_update(***, *nowait:bool=False*, *read:bool=False*, *of:_ForUpdateOfArgument|None=None*, *skip_locked:bool=False*, *key_share:bool=False*) → Self

return a new [Query](#sqlalchemy.orm.Query)
with the specified options for the
`FOR UPDATE` clause.

The behavior of this method is identical to that of
[GenerativeSelect.with_for_update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update).
When called with no arguments,
the resulting `SELECT` statement will have a `FOR UPDATE` clause
appended.  When additional arguments are specified, backend-specific
options such as `FOR UPDATE NOWAIT` or `LOCK IN SHARE MODE`
can take effect.

E.g.:

```
q = (
    sess.query(User)
    .populate_existing()
    .with_for_update(nowait=True, of=User)
)
```

The above query on a PostgreSQL backend will render like:

```
SELECT users.id AS users_id FROM users FOR UPDATE OF users NOWAIT
```

Warning

Using `with_for_update` in the context of eager loading
relationships is not officially supported or recommended by
SQLAlchemy and may not work with certain queries on various
database backends.  When `with_for_update` is successfully used
with a query that involves [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload), SQLAlchemy will
attempt to emit SQL that locks all involved tables.

Note

It is generally a good idea to combine the use of the
[Query.populate_existing()](#sqlalchemy.orm.Query.populate_existing) method when using the
[Query.with_for_update()](#sqlalchemy.orm.Query.with_for_update) method.   The purpose of
[Query.populate_existing()](#sqlalchemy.orm.Query.populate_existing) is to force all the data read
from the SELECT to be populated into the ORM objects returned,
even if these objects are already in the [identity map](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-map).

See also

[GenerativeSelect.with_for_update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update)
- Core level method with
full argument and behavioral description.

[Query.populate_existing()](#sqlalchemy.orm.Query.populate_existing) - overwrites attributes of
objects already loaded in the identity map.

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)with_hint(*selectable:_FromClauseArgument*, *text:str*, *dialect_name:str='*'*) → Self

*inherited from the* `HasHints.with_hint()` *method of* `HasHints`

Add an indexing or other executional context hint for the given
selectable to this [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) or other selectable
object.

Tip

The [Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) method adds hints that are
**specific to a single table** to a statement, in a location that
is **dialect-specific**.  To add generic optimizer hints to the
**beginning** of a statement ahead of the SELECT keyword such as
for MySQL or Oracle Database, use the
[Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) method.  To add optimizer
hints to the **end** of a statement such as for PostgreSQL, use the
[Select.with_statement_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint) method.

The text of the hint is rendered in the appropriate
location for the database backend in use, relative
to the given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias)
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

[Select.with_statement_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint)

[Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) - generic SELECT prefixing
which also can suit some database-specific HINT syntaxes such as
MySQL or Oracle Database optimizer hints

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)with_labels() → Self

Deprecated since version 2.0: The [Query.with_labels()](#sqlalchemy.orm.Query.with_labels) and [Query.apply_labels()](#sqlalchemy.orm.Query.apply_labels) method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. Use set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL) instead. (Background on SQLAlchemy 2.0 at: [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html))

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)with_parent(*instance:object*, *property:attributes.QueryableAttribute[Any]|None=None*, *from_entity:_ExternalEntityType[Any]|None=None*) → Self

Add filtering criterion that relates the given instance
to a child object or collection, using its attribute state
as well as an established [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
configuration.

Deprecated since version 2.0: The [Query.with_parent()](#sqlalchemy.orm.Query.with_parent) method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. Use the [with_parent()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_parent) standalone construct. (Background on SQLAlchemy 2.0 at: [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html))

The method uses the [with_parent()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_parent) function to generate
the clause, the result of which is passed to
[Query.filter()](#sqlalchemy.orm.Query.filter).

Parameters are the same as [with_parent()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_parent), with the exception
that the given property can be None, in which case a search is
performed against this [Query](#sqlalchemy.orm.Query) object’s target mapper.

  Parameters:

- **instance** – An instance which has some [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).
- **property** – Class bound attribute which indicates
  what relationship from the instance should be used to reconcile the
  parent/child relationship.
- **from_entity** – Entity in which to consider as the left side.  This defaults to the
  “zero” entity of the [Query](#sqlalchemy.orm.Query) itself.

      method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)with_session(*session:Session*) → Self

Return a [Query](#sqlalchemy.orm.Query) that will use the given
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

While the [Query](#sqlalchemy.orm.Query)
object is normally instantiated using the
[Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query) method, it is legal to build the
[Query](#sqlalchemy.orm.Query)
directly without necessarily using a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  Such a
[Query](#sqlalchemy.orm.Query) object, or any [Query](#sqlalchemy.orm.Query)
already associated
with a different [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), can produce a new
[Query](#sqlalchemy.orm.Query)
object associated with a target session using this method:

```
from sqlalchemy.orm import Query

query = Query([MyClass]).filter(MyClass.id == 5)

result = query.with_session(my_session).one()
```

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)with_statement_hint(*text:str*, *dialect_name:str='*'*) → Self

*inherited from the* `HasHints.with_statement_hint()` *method of* `HasHints`

Add a statement hint to this [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) or
other selectable object.

Tip

[Select.with_statement_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint) generally adds hints
**at the trailing end** of a SELECT statement.  To place
dialect-specific hints such as optimizer hints at the **front** of
the SELECT statement after the SELECT keyword, use the
[Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) method for an open-ended
space, or for table-specific hints the
[Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) may be used, which places
hints in a dialect-specific location.

This method is similar to [Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) except
that it does not require an individual table, and instead applies to
the statement as a whole.

Hints here are specific to the backend database and may include
directives such as isolation levels, file directives, fetch directives,
etc.

See also

[Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint)

[Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) - generic SELECT prefixing
which also can suit some database-specific HINT syntaxes such as
MySQL or Oracle Database optimizer hints

     method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)with_transformation(*fn:Callable[[Query],Query]*) → [Query](#sqlalchemy.orm.Query)

Return a new [Query](#sqlalchemy.orm.Query) object transformed by
the given function.

E.g.:

```
def filter_something(criterion):
    def transform(q):
        return q.filter(criterion)

    return transform

q = q.with_transformation(filter_something(x == 5))
```

This allows ad-hoc recipes to be created for [Query](#sqlalchemy.orm.Query)
objects.

    method [sqlalchemy.orm.Query.](#sqlalchemy.orm.Query)yield_per(*count:int*) → Self

Yield only `count` rows at a time.

The purpose of this method is when fetching very large result sets
(> 10K rows), to batch results in sub-collections and yield them
out partially, so that the Python interpreter doesn’t need to declare
very large areas of memory which is both time consuming and leads
to excessive memory use.   The performance from fetching hundreds of
thousands of rows can often double when a suitable yield-per setting
(e.g. approximately 1000) is used, even with DBAPIs that buffer
rows (which are most).

As of SQLAlchemy 1.4, the [Query.yield_per()](#sqlalchemy.orm.Query.yield_per) method is
equivalent to using the `yield_per` execution option at the ORM
level. See the section [Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) for further
background on this option.

See also

[Fetching Large Result Sets with Yield Per](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per)

## ORM-Specific Query Constructs

This section has moved to [Additional ORM API Constructs](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-additional).
