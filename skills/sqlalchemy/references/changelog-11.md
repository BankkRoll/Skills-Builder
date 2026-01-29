# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# 1.2 Changelog

## 1.2.19

Released: April 15, 2019

### orm

- Fixed a regression in 1.2 due to the introduction of baked queries for
  relationship lazy loaders, where a race condition is created during the
  generation of the “lazy clause” which occurs within a memoized attribute. If
  two threads initialize the memoized attribute concurrently, the baked query
  could be generated with bind parameter keys that are then replaced with new
  keys by the next run, leading to a lazy load query that specifies the
  related criteria as `None`. The fix establishes that the parameter names
  are fixed before the new clause and parameter objects are generated, so that
  the names are the same every time.
  References: [#4507](https://www.sqlalchemy.org/trac/ticket/4507)

### examples

- Fixed bug in large_resultsets example case where a re-named “id” variable
  due to code reformatting caused the test to fail.  Pull request courtesy
  Matt Schuchhardt.
  References: [#4528](https://www.sqlalchemy.org/trac/ticket/4528)

### engine

- Comparing two objects of [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) using `__eq__()` did not take port
  number into consideration, two objects differing only by port number were
  considered equal. Port comparison is now added in `__eq__()` method of
  [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL), objects differing by port number are now not equal.
  Additionally, `__ne__()` was not implemented for [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) which
  caused unexpected result when `!=` was used in Python2, since there are no
  implied relationships among the comparison operators in Python2.
  References: [#4406](https://www.sqlalchemy.org/trac/ticket/4406)

### mssql

- A commit() is emitted after an isolation level change to SNAPSHOT, as both
  pyodbc and pymssql open an implicit transaction which blocks subsequent SQL
  from being emitted in the current transaction.
  References: [#4536](https://www.sqlalchemy.org/trac/ticket/4536)

### oracle

- Added support for reflection of the [NCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NCHAR) datatype to the Oracle
  dialect, and added [NCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NCHAR) to the list of types exported by the
  Oracle dialect.
  References: [#4506](https://www.sqlalchemy.org/trac/ticket/4506)

## 1.2.18

Released: February 15, 2019

### orm

- Fixed a regression in 1.2 where a wildcard/load_only loader option would
  not work correctly against a loader path where of_type() were used to limit
  to a particular subclass.  The fix only works for of_type() of a simple
  subclass so far, not a with_polymorphic entity which will be addressed in a
  separate issue; it is unlikely this latter case was working previously.
  References: [#4468](https://www.sqlalchemy.org/trac/ticket/4468)
- Fixed fairly simple but critical issue where the
  [SessionEvents.pending_to_persistent()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.pending_to_persistent) event would be invoked for
  objects not just when they move from pending to persistent, but when they
  were also already persistent and just being updated, thus causing the event
  to be invoked for all objects on every update.
  References: [#4489](https://www.sqlalchemy.org/trac/ticket/4489)

### sql

- Fixed issue where the [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type had a read-only
  [JSON.should_evaluate_none](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.should_evaluate_none) attribute, which would cause failures
  when making use of the [TypeEngine.evaluates_none()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.evaluates_none) method in
  conjunction with this type.  Pull request courtesy Sanjana S.
  References: [#4485](https://www.sqlalchemy.org/trac/ticket/4485)

### mysql

- Fixed a second regression caused by [#4344](https://www.sqlalchemy.org/trac/ticket/4344) (the first was
  [#4361](https://www.sqlalchemy.org/trac/ticket/4361)), which works around MySQL issue 88718, where the lower
  casing function used was not correct for Python 2 with OSX/Windows casing
  conventions, which would then raise `TypeError`.  Full coverage has been
  added to this logic so that every codepath is exercised in a mock style for
  all three casing conventions on all versions of Python. MySQL 8.0 has
  meanwhile fixed issue 88718 so the workaround is only applies to a
  particular span of MySQL 8.0 versions.
  References: [#4492](https://www.sqlalchemy.org/trac/ticket/4492)

### sqlite

- Fixed bug in SQLite DDL where using an expression as a server side default
  required that it be contained within parenthesis to be accepted by the
  sqlite parser.  Pull request courtesy Bartlomiej Biernacki.
  References: [#4474](https://www.sqlalchemy.org/trac/ticket/4474)

### mssql

- Fixed bug where the SQL Server “IDENTITY_INSERT” logic that allows an INSERT
  to proceed with an explicit value on an IDENTITY column was not detecting
  the case where [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) were used with a dictionary that
  contained a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) as key and a SQL expression as a value.
  References: [#4499](https://www.sqlalchemy.org/trac/ticket/4499)

## 1.2.17

Released: January 25, 2019

### orm

- Added new event hooks [QueryEvents.before_compile_update()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile_update) and
  [QueryEvents.before_compile_delete()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile_delete) which complement
  [QueryEvents.before_compile()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile) in the case of the [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update)
  and [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete) methods.
  References: [#4461](https://www.sqlalchemy.org/trac/ticket/4461)
- Fixed issue where when using single-table inheritance in conjunction with a
  joined inheritance hierarchy that uses “with polymorphic” loading, the
  “single table criteria” for that single-table entity could get confused for
  that of other entities from the same hierarchy used in the same query.The
  adaption of the “single table criteria” is made more specific to the target
  entity to avoid it accidentally getting adapted to other tables in the
  query.
  References: [#4454](https://www.sqlalchemy.org/trac/ticket/4454)

### postgresql

- Revised the query used when reflecting CHECK constraints to make use of the
  `pg_get_constraintdef` function, as the `consrc` column is being
  deprecated in PG 12.  Thanks to John A Stevenson for the tip.
  References: [#4463](https://www.sqlalchemy.org/trac/ticket/4463)

### oracle

- Fixed regression in integer precision logic due to the refactor of the
  cx_Oracle dialect in 1.2.  We now no longer apply the cx_Oracle.NATIVE_INT
  type to result columns sending integer values (detected as positive
  precision with scale ==0) which encounters integer overflow issues with
  values that go beyond the 32 bit boundary.  Instead, the output variable
  is left untyped so that cx_Oracle can choose the best option.
  References: [#4457](https://www.sqlalchemy.org/trac/ticket/4457)

## 1.2.16

Released: January 11, 2019

### engine

- Fixed a regression introduced in version 1.2 where a refactor
  of the [SQLAlchemyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SQLAlchemyError) base exception class introduced an
  inappropriate coercion of a plain string message into Unicode under
  python 2k, which is not handled by the Python interpreter for characters
  outside of the platform’s encoding (typically ascii).  The
  [SQLAlchemyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SQLAlchemyError) class now passes a bytestring through under
  Py2K for `__str__()` as is the behavior of exception objects in general
  under Py2K, does a safe coercion to unicode utf-8 with
  backslash fallback for `__unicode__()`.  For Py3K the message is
  typically unicode already, but if not is again safe-coerced with utf-8
  with backslash fallback for the `__str__()` method.
  References: [#4429](https://www.sqlalchemy.org/trac/ticket/4429)

### sql

- Fixed issue where the DDL emitted for `DropTableComment`, which
  will be used by an upcoming version of Alembic, was incorrect for the MySQL
  and Oracle databases.
  References: [#4436](https://www.sqlalchemy.org/trac/ticket/4436)

### postgresql

- Fixed issue where a [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) or a custom domain present
  in a remote schema would not be recognized within column reflection if
  the name of the enum/domain or the name of the schema required quoting.
  A new parsing scheme now fully parses out quoted or non-quoted tokens
  including support for SQL-escaped quotes.
  References: [#4416](https://www.sqlalchemy.org/trac/ticket/4416)
- Fixed issue where multiple [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) objects referred to
  by the same [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object would fail to be created if
  multiple objects had the same name under different schema names.  The
  internal memoization the PostgreSQL dialect uses to track if it has
  created a particular [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) in the database during
  a DDL creation sequence now takes schema name into account.

### sqlite

- Reflection of an index based on SQL expressions are now skipped with a
  warning, in the same way as that of the Postgresql dialect, where we currently
  do not support reflecting indexes that have SQL expressions within them.
  Previously, an index with columns of None were produced which would break
  tools like Alembic.
  References: [#4431](https://www.sqlalchemy.org/trac/ticket/4431)

### misc

- Fixed issue in “expanding IN” feature where using the same bound parameter
  name more than once in a query would lead to a KeyError within the process
  of rewriting the parameters in the query.
  References: [#4394](https://www.sqlalchemy.org/trac/ticket/4394)

## 1.2.15

Released: December 11, 2018

### orm

- Fixed bug where the ORM annotations could be incorrect for the
  primaryjoin/secondaryjoin a relationship if one used the pattern
  `ForeignKey(SomeClass.id)` in the declarative mappings.   This pattern
  would leak undesired annotations into the join conditions which can break
  aliasing operations done within [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) that are not supposed to
  impact elements in that join condition.  These annotations are now removed
  up front if present.
  References: [#4367](https://www.sqlalchemy.org/trac/ticket/4367)
- In continuing with a similar theme as that of very recent [#4349](https://www.sqlalchemy.org/trac/ticket/4349),
  repaired issue with [Comparator.any()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.any) and
  [Comparator.has()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.has) where the “secondary”
  selectable needs to be explicitly part of the FROM clause in the
  EXISTS subquery to suit the case where this “secondary” is a [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join)
  object.
  References: [#4366](https://www.sqlalchemy.org/trac/ticket/4366)
- Fixed regression caused by [#4349](https://www.sqlalchemy.org/trac/ticket/4349) where adding the “secondary”
  table to the FROM clause for a dynamic loader would affect the ability of
  the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) to make a subsequent join to another entity.   The fix
  adds the primary entity as the first element of the FROM list since
  [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) wants to jump from that.   Version 1.3 will have
  a more comprehensive solution to this problem as well ([#4365](https://www.sqlalchemy.org/trac/ticket/4365)).
  References: [#4363](https://www.sqlalchemy.org/trac/ticket/4363)
- Fixed bug where chaining of mapper options using
  `RelationshipProperty.of_type()` in conjunction with a chained option
  that refers to an attribute name by string only would fail to locate the
  attribute.
  References: [#4400](https://www.sqlalchemy.org/trac/ticket/4400)

### orm declarative

- A warning is emitted in the case that a [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) object is applied to
  a declarative class, as it seems likely this intended to be a
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object.
  References: [#4374](https://www.sqlalchemy.org/trac/ticket/4374)

### misc

- Added support for the `write_timeout` flag accepted by mysqlclient and
  pymysql to  be passed in the URL string.
  References: [#4381](https://www.sqlalchemy.org/trac/ticket/4381)
- Fixed issue where reflection of a PostgreSQL domain that is expressed as an
  array would fail to be recognized.  Pull request courtesy Jakub Synowiec.
  References: [#4377](https://www.sqlalchemy.org/trac/ticket/4377), [#4380](https://www.sqlalchemy.org/trac/ticket/4380)

## 1.2.14

Released: November 10, 2018

### orm

- Fixed bug in [Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings) where alternate mapped
  attribute names would result in the primary key column of the UPDATE
  statement being included in the SET clause, as well as the WHERE clause;
  while usually harmless, for SQL Server this can raise an error due to the
  IDENTITY column.  This is a continuation of the same bug that was fixed in
  [#3849](https://www.sqlalchemy.org/trac/ticket/3849), where testing was insufficient to catch this additional
  flaw.
  References: [#4357](https://www.sqlalchemy.org/trac/ticket/4357)
- Fixed a minor performance issue which could in some cases add unnecessary
  overhead to result fetching, involving the use of ORM columns and entities
  that include those same columns at the same time within a query.  The issue
  has to do with hash / eq overhead when referring to the column in different
  ways.
  References: [#4347](https://www.sqlalchemy.org/trac/ticket/4347)

### mysql

- Fixed regression caused by [#4344](https://www.sqlalchemy.org/trac/ticket/4344) released in 1.2.13, where the fix
  for MySQL 8.0’s case sensitivity problem with referenced column names when
  reflecting foreign key referents is worked around using the
  `information_schema.columns` view.  The workaround was failing on OSX /
  `lower_case_table_names=2` which produces non-matching casing for the
  `information_schema.columns` vs. that of `SHOW CREATE TABLE`, so in
  case-insensitive SQL modes case-insensitive matching is now used.
  References: [#4361](https://www.sqlalchemy.org/trac/ticket/4361)

## 1.2.13

Released: October 31, 2018

### orm

- Fixed bug where “dynamic” loader needs to explicitly set the “secondary”
  table in the FROM clause of the query, to suit the case where the secondary
  is a join object that is otherwise not pulled into the query from its
  columns alone.
  References: [#4349](https://www.sqlalchemy.org/trac/ticket/4349)

### orm declarative

- Fixed regression caused by [#4326](https://www.sqlalchemy.org/trac/ticket/4326) in version 1.2.12 where using
  [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) with a mixin in conjunction with
  [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym) would fail to map the synonym properly to an inherited
  subclass.
  References: [#4350](https://www.sqlalchemy.org/trac/ticket/4350)
- The column conflict resolution technique discussed at
  [Resolving Column Conflicts with use_existing_column](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#orm-inheritance-column-conflicts) is now functional for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  that is also a primary key column.  Previously, a check for primary key
  columns declared on a single-inheritance subclass would occur before the
  column copy were allowed to pass.
  References: [#4352](https://www.sqlalchemy.org/trac/ticket/4352)

### sql

- Refactored [SQLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler) to expose a
  [SQLCompiler.group_by_clause()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler.group_by_clause) method similar to the
  [SQLCompiler.order_by_clause()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler.order_by_clause) and `SQLCompiler.limit_clause()`
  methods, which can be overridden by dialects to customize how GROUP BY
  renders.  Pull request courtesy Samuel Chou.
- Fixed bug where the [Enum.create_constraint](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.create_constraint) flag on  the
  [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatype would not be propagated to copies of the type, which
  affects use cases such as declarative mixins and abstract bases.
  References: [#4341](https://www.sqlalchemy.org/trac/ticket/4341)

### postgresql

- Added support for the [aggregate_order_by](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.aggregate_order_by) function to receive
  multiple ORDER BY elements, previously only a single element was accepted.
  References: [#4337](https://www.sqlalchemy.org/trac/ticket/4337)

### mysql

- Added word `function` to the list of reserved words for MySQL, which is
  now a keyword in MySQL 8.0
  References: [#4348](https://www.sqlalchemy.org/trac/ticket/4348)
- Added a workaround for a MySQL bug #88718 introduced in the 8.0 series,
  where the reflection of a foreign key constraint is not reporting the
  correct case sensitivity for the referred column, leading to errors during
  use of the reflected constraint such as when using the automap extension.
  The workaround emits an additional query to the information_schema tables in
  order to retrieve the correct case sensitive name.
  References: [#4344](https://www.sqlalchemy.org/trac/ticket/4344)

### misc

- Fixed issue where part of the utility language helper internals was passing
  the wrong kind of argument to the Python `__import__` builtin as the list
  of modules to be imported.  The issue produced no symptoms within the core
  library but could cause issues with external applications that redefine the
  `__import__` builtin or otherwise instrument it. Pull request courtesy Joe
  Urciuoli.
- Fixed additional warnings generated by Python 3.7 due to changes in the
  organization of the Python `collections` and `collections.abc` packages.
  Previous `collections` warnings were fixed in version 1.2.11. Pull request
  courtesy xtreak.
  References: [#4339](https://www.sqlalchemy.org/trac/ticket/4339)
- Added missing `.index()` method to list-based association collections
  in the association proxy extension.

## 1.2.12

Released: September 19, 2018

### orm

- Added a check within the weakref cleanup for the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState)
  object to check for the presence of the `dict` builtin, in an effort to
  reduce error messages generated when these cleanups occur during interpreter
  shutdown.  Pull request courtesy Romuald Brunet.
- Fixed bug where use of [Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral) construct in conjunction with
  [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) as well as `Query.select_entity_from()` would not
  apply clause adaption to the right side of the join.   “lateral” introduces
  the use case of the right side of a join being correlatable.  Previously,
  adaptation of this clause wasn’t considered.   Note that in 1.2 only,
  a selectable introduced by [Query.subquery()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.subquery) is still not adapted
  due to [#4304](https://www.sqlalchemy.org/trac/ticket/4304); the selectable needs to be produced by the
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) function to be the right side of the “lateral” join.
  References: [#4334](https://www.sqlalchemy.org/trac/ticket/4334)
- Fixed 1.2 regression caused by [#3472](https://www.sqlalchemy.org/trac/ticket/3472) where the handling of an
  “updated_at” style column within the context of a post-update operation
  would also occur for a row that is to be deleted following the update,
  meaning both that a column with a Python-side value generator would show
  the now-deleted value that was emitted for the UPDATE before the DELETE
  (which was not the previous behavior), as well as that a SQL- emitted value
  generator would have the attribute expired, meaning the previous value
  would be unreachable due to the row having been deleted and the object
  detached from the session.The “postfetch” logic that was added as part of
  [#3472](https://www.sqlalchemy.org/trac/ticket/3472) is now skipped entirely for an object that ultimately is to
  be deleted.
  References: [#4327](https://www.sqlalchemy.org/trac/ticket/4327)

### orm declarative

- Fixed bug where the declarative scan for attributes would receive the
  expression proxy delivered by a hybrid attribute at the class level, and
  not the hybrid attribute itself, when receiving the descriptor via the
  `@declared_attr` callable on a subclass of an already-mapped class. This
  would lead to an attribute that did not report itself as a hybrid when
  viewed within [Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors).
  References: [#4326](https://www.sqlalchemy.org/trac/ticket/4326)

### postgresql

- Fixed bug in PostgreSQL dialect where compiler keyword arguments such as
  `literal_binds=True` were not being propagated to a DISTINCT ON
  expression.
  References: [#4325](https://www.sqlalchemy.org/trac/ticket/4325)
- Fixed the [array_agg()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array_agg) function, which is a slightly
  altered version of the usual [array_agg()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg) function, to also
  accept an incoming “type” argument without forcing an ARRAY around it,
  essentially the same thing that was fixed for the generic function in 1.1
  in [#4107](https://www.sqlalchemy.org/trac/ticket/4107).
  References: [#4324](https://www.sqlalchemy.org/trac/ticket/4324)
- Fixed bug in PostgreSQL ENUM reflection where a case-sensitive, quoted name
  would be reported by the query including quotes, which would not match a
  target column during table reflection as the quotes needed to be stripped
  off.
  References: [#4323](https://www.sqlalchemy.org/trac/ticket/4323)

### oracle

- Fixed issue for cx_Oracle 7.0 where the behavior of Oracle param.getvalue()
  now returns a list, rather than a single scalar value, breaking
  autoincrement logic throughout the Core and ORM. The dml_ret_array_val
  compatibility flag is used for cx_Oracle 6.3 and 6.4 to establish compatible
  behavior with 7.0 and forward, for cx_Oracle 6.2.1 and prior a version
  number check falls back to the old logic.
  References: [#4335](https://www.sqlalchemy.org/trac/ticket/4335)

### misc

- Fixed issue where [BakedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery) did not include the specific query
  class used by the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) as part of the cache key, leading to
  incompatibilities when using custom query classes, in particular the
  [ShardedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedQuery) which has some different argument signatures.
  References: [#4328](https://www.sqlalchemy.org/trac/ticket/4328)

## 1.2.11

Released: August 20, 2018

### orm declarative

- Fixed issue in previously untested use case, allowing a declarative mapped
  class to inherit from a classically-mapped class outside of the declarative
  base, including that it accommodates for unmapped intermediate classes. An
  unmapped intermediate class may specify `__abstract__`, which is now
  interpreted correctly, or the intermediate class can remain unmarked, and
  the classically mapped base class will be detected within the hierarchy
  regardless. In order to anticipate existing scenarios which may be mixing
  in classical mappings into existing declarative hierarchies, an error is
  now raised if multiple mapped bases are detected for a given class.
  References: [#4321](https://www.sqlalchemy.org/trac/ticket/4321)

### sql

- Fixed issue that is closely related to [#3639](https://www.sqlalchemy.org/trac/ticket/3639) where an expression
  rendered in a boolean context on a non-native boolean backend would
  be compared to 1/0 even though it is already an implicitly boolean
  expression, when [ColumnElement.self_group()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.self_group) were used.  While this
  does not affect the user-friendly backends (MySQL, SQLite) it was not
  handled by Oracle (and possibly SQL Server).   Whether or not the
  expression is implicitly boolean on any database is now determined
  up front as an additional check to not generate the integer comparison
  within the compilation of the statement.
  References: [#4320](https://www.sqlalchemy.org/trac/ticket/4320)
- Added missing window function parameters
  [WithinGroup.over.range_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.WithinGroup.over.params.range_) and [WithinGroup.over.rows](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.WithinGroup.over.params.rows)
  parameters to the [WithinGroup.over()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.WithinGroup.over) and
  [FunctionFilter.over()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.FunctionFilter.over) methods, to correspond to the range/rows
  feature added to the “over” method of SQL functions as part of
  [#3049](https://www.sqlalchemy.org/trac/ticket/3049) in version 1.1.
  References: [#4322](https://www.sqlalchemy.org/trac/ticket/4322)
- Fixed bug where the multi-table support for UPDATE and DELETE statements
  did not consider the additional FROM elements as targets for correlation,
  when a correlated SELECT were also combined with the statement.  This
  change now includes that a SELECT statement in the WHERE clause for such a
  statement will try to auto-correlate back to these additional tables in the
  parent UPDATE/DELETE or unconditionally correlate if
  [Select.correlate()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate) is used.  Note that auto-correlation raises an
  error if the SELECT statement would have no FROM clauses as a result, which
  can now occur if the parent UPDATE/DELETE specifies the same tables in its
  additional set of tables; specify [Select.correlate()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate) explicitly to
  resolve.
  References: [#4313](https://www.sqlalchemy.org/trac/ticket/4313)

### oracle

- For cx_Oracle, Integer datatypes will now be bound to “int”, per advice
  from the cx_Oracle developers.  Previously, using cx_Oracle.NUMBER caused a
  loss in precision within the cx_Oracle 6.x series.
  References: [#4309](https://www.sqlalchemy.org/trac/ticket/4309)

### misc

- Started importing “collections” from “collections.abc” under Python 3.3 and
  greater for Python 3.8 compatibility.  Pull request courtesy Nathaniel
  Knight.
- Fixed issue where the “schema” name used for a SQLite database within table
  reflection would not quote the schema name correctly.  Pull request
  courtesy Phillip Cloud.

## 1.2.10

Released: July 13, 2018

### orm

- Fixed bug in [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) construct where placing two columns of the
  same name would be de-duplicated, when the [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) were used as
  part of the rendered SQL, such as in the ORDER BY or GROUP BY of the statement.
  References: [#4295](https://www.sqlalchemy.org/trac/ticket/4295)
- Fixed regression in 1.2.9 due to [#4287](https://www.sqlalchemy.org/trac/ticket/4287) where using a
  [Load](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load) option in conjunction with a string wildcard would result
  in a TypeError.
  References: [#4298](https://www.sqlalchemy.org/trac/ticket/4298)

### sql

- Fixed bug where a [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) would be dropped explicitly before any
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that refers to it, which breaks in the case when the
  sequence is also involved in a server-side default for that table, when
  using [MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all).   The step which processes sequences
  to be dropped via non server-side column default functions is now invoked
  after the table itself is dropped.
  References: [#4300](https://www.sqlalchemy.org/trac/ticket/4300)

## 1.2.9

Released: June 29, 2018

### orm

- Fixed issue where chaining multiple join elements inside of
  [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) might not correctly adapt to the previous left-hand
  side, when chaining joined inheritance classes that share the same base
  class.
  References: [#3505](https://www.sqlalchemy.org/trac/ticket/3505)
- Fixed bug in cache key generation for baked queries which could cause a
  too-short cache key to be generated for the case of eager loads across
  subclasses.  This could in turn cause the eagerload query to be cached in
  place of a non-eagerload query, or vice versa, for a polymorphic “selectin”
  load, or possibly for lazy loads or selectin loads as well.
  References: [#4287](https://www.sqlalchemy.org/trac/ticket/4287)
- Fixed bug in new polymorphic selectin loading where the BakedQuery used
  internally would be mutated by the given loader options, which would both
  inappropriately mutate the subclass query as well as carry over the effect
  to subsequent queries.
  References: [#4286](https://www.sqlalchemy.org/trac/ticket/4286)
- Fixed regression caused by [#4256](https://www.sqlalchemy.org/trac/ticket/4256) (itself a regression fix for
  [#4228](https://www.sqlalchemy.org/trac/ticket/4228)) which breaks an undocumented behavior which converted for a
  non-sequence of entities passed directly to the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) constructor
  into a single-element sequence.  While this behavior was never supported or
  documented, it’s already in use so has been added as a behavioral contract
  to [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query).
  References: [#4269](https://www.sqlalchemy.org/trac/ticket/4269)
- Fixed an issue that was both a performance regression in 1.2 as well as an
  incorrect result regarding the “baked” lazy loader, involving the
  generation of cache keys from the original [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object’s loader
  options.  If the loader options were built up in a “branched” style using
  common base elements for multiple options, the same options would be
  rendered into the cache key repeatedly, causing both a performance issue as
  well as generating the wrong cache key.  This is fixed, along with a
  performance improvement when such “branched” options are applied via
  [Query.options()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.options) to prevent the same option objects from being
  applied repeatedly.
  References: [#4270](https://www.sqlalchemy.org/trac/ticket/4270)

### sql

- Fixed regression in 1.2 due to [#4147](https://www.sqlalchemy.org/trac/ticket/4147) where a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that
  has had some of its indexed columns redefined with new ones, as would occur
  when overriding columns during reflection or when using
  [Table.extend_existing](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.extend_existing), such that the [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata)
  method would fail when attempting to copy those indexes as they still
  referred to the replaced column.   The copy logic now accommodates for this
  condition.
  References: [#4279](https://www.sqlalchemy.org/trac/ticket/4279)

### mysql

- Fixed percent-sign doubling in mysql-connector-python dialect, which does
  not require de-doubling of percent signs.   Additionally, the  mysql-
  connector-python driver is inconsistent in how it passes the column names
  in cursor.description, so a workaround decoder has been added to
  conditionally decode these randomly-sometimes-bytes values to unicode only
  if needed.  Also improved test support for mysql-connector-python, however
  it should be noted that this driver still has issues with unicode that
  continue to be unresolved as of yet.
- Fixed bug in index reflection where on MySQL 8.0 an index that includes
  ASC or DESC in an indexed column specification would not be correctly
  reflected, as MySQL 8.0 introduces support for returning this information
  in a table definition string.
  References: [#4293](https://www.sqlalchemy.org/trac/ticket/4293)
- Fixed bug in MySQLdb dialect and variants such as PyMySQL where an
  additional “unicode returns” check upon connection makes explicit use of
  the “utf8” character set, which in MySQL 8.0 emits a warning that utf8mb4
  should be used.  This is now replaced with a utf8mb4 equivalent.
  Documentation is also updated for the MySQL dialect to specify utf8mb4 in
  all examples.  Additional changes have been made to the test suite to use
  utf8mb3 charsets and databases (there seem to be collation issues in some
  edge cases with utf8mb4), and to support configuration default changes made
  in MySQL 8.0 such as explicit_defaults_for_timestamp as well as new errors
  raised for invalid MyISAM indexes.
  References: [#4283](https://www.sqlalchemy.org/trac/ticket/4283)
- The [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct now accommodates a [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) object
  as supported by MySQL for UPDATE..FROM.  As the construct already
  accepted an alias object for a similar purpose, the feature of UPDATE
  against a non-table was already implied so this has been added.
  References: [#3645](https://www.sqlalchemy.org/trac/ticket/3645)

### sqlite

- Fixed issue in test suite where SQLite 3.24 added a new reserved word that
  conflicted with a usage in TypeReflectionTest.  Pull request courtesy Nils
  Philippsen.

### mssql

- Fixed bug in MSSQL reflection where when two same-named tables in different
  schemas had same-named primary key constraints, foreign key constraints
  referring to one of the tables would have their columns doubled, causing
  errors.   Pull request courtesy Sean Dunn.
  References: [#4288](https://www.sqlalchemy.org/trac/ticket/4288)
- Fixed issue within the SQL Server dialect under Python 3 where when running
  against a non-standard SQL server database that does not contain either the
  “sys.dm_exec_sessions” or “sys.dm_pdw_nodes_exec_sessions” views, leading
  to a failure to fetch the isolation level, the error raise would fail due
  to an UnboundLocalError.
  References: [#4273](https://www.sqlalchemy.org/trac/ticket/4273)

### oracle

- Added a new event currently used only by the cx_Oracle dialect,
  `DialectEvents.setiputsizes()`.  The event passes a dictionary of
  [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects to DBAPI-specific type objects that will be
  passed, after conversion to parameter names, to the cx_Oracle
  `cursor.setinputsizes()` method.  This allows both visibility into the
  setinputsizes process as well as the ability to alter the behavior of what
  datatypes are passed to this method.
  See also
  [Fine grained control over cx_Oracle data binding performance with setinputsizes](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#cx-oracle-setinputsizes)
  References: [#4290](https://www.sqlalchemy.org/trac/ticket/4290)
- Fixed INSERT FROM SELECT with CTEs for the Oracle and MySQL dialects, where
  the CTE was being placed above the entire statement as is typical with
  other databases, however Oracle and MariaDB 10.2 wants the CTE underneath
  the “INSERT” segment. Note that the Oracle and MySQL dialects don’t yet
  work when a CTE is applied to a subquery inside of an UPDATE or DELETE
  statement, as the CTE is still applied to the top rather than inside the
  subquery.
  References: [#4275](https://www.sqlalchemy.org/trac/ticket/4275)

### misc

- Added new attribute [Query.lazy_loaded_from](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.lazy_loaded_from) which is populated
  with an [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) that is using this [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) in
  order to lazy load a relationship.  The rationale for this is that
  it serves as a hint for the horizontal sharding feature to use, such that
  the identity token of the state can be used as the default identity token
  to use for the query within id_chooser().
  References: [#4243](https://www.sqlalchemy.org/trac/ticket/4243)
- Replaced the usage of inspect.formatargspec() with a vendored version
  copied from the Python standard library, as inspect.formatargspec()
  is deprecated and as of Python 3.7.0 is emitting a warning.
  References: [#4291](https://www.sqlalchemy.org/trac/ticket/4291)

## 1.2.8

Released: May 28, 2018

### orm

- Fixed regression in 1.2.7 caused by [#4228](https://www.sqlalchemy.org/trac/ticket/4228), which itself was fixing
  a 1.2-level regression, where the `query_cls` callable passed to a
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) was assumed to be a subclass of [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)  with
  class method availability, as opposed to an arbitrary callable.    In
  particular, the dogpile caching example illustrates `query_cls` as a
  function and not a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) subclass.
  References: [#4256](https://www.sqlalchemy.org/trac/ticket/4256)
- Fixed a long-standing regression that occurred in version
  1.0, which prevented the use of a custom `MapperOption`
  that alters the _params of a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object for a
  lazy load, since the lazy loader itself would overwrite those
  parameters.   This applies to the “temporal range” example
  on the wiki.  Note however that the
  [Query.populate_existing()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.populate_existing) method is now required in
  order to rewrite the mapper options associated with an object
  already loaded in the identity map.
  As part of this change, a custom defined
  `MapperOption` will now cause lazy loaders related to
  the target object to use a non-baked query by default unless
  the `MapperOption._generate_cache_key()` method is implemented.
  In particular, this repairs one regression which occurred when
  using the dogpile.cache “advanced” example, which was not
  returning cached results and instead emitting SQL due to an
  incompatibility with the baked query loader; with the change,
  the `RelationshipCache` option included for many releases
  in the dogpile example will disable the “baked” query altogether.
  Note that the dogpile example is also modernized to avoid both
  of these issues as part of issue [#4258](https://www.sqlalchemy.org/trac/ticket/4258).
  References: [#4128](https://www.sqlalchemy.org/trac/ticket/4128)
- Fixed bug where the new `Result.with_post_criteria()`
  method would not interact with a subquery-eager loader correctly,
  in that the “post criteria” would not be applied to embedded
  subquery eager loaders.   This is related to [#4128](https://www.sqlalchemy.org/trac/ticket/4128) in that
  the post criteria feature is now used by the lazy loader.
- Updated the dogpile.caching example to include new structures that
  accommodate for the “baked” query system, which is used by default within
  lazy loaders and some eager relationship loaders. The dogpile.caching
  “relationship_caching” and “advanced” examples were also broken due to
  [#4256](https://www.sqlalchemy.org/trac/ticket/4256).  The issue here is also worked-around by the fix in
  [#4128](https://www.sqlalchemy.org/trac/ticket/4128).
  References: [#4258](https://www.sqlalchemy.org/trac/ticket/4258)

### engine

- Fixed connection pool issue whereby if a disconnection error were raised
  during the connection pool’s “reset on return” sequence in conjunction with
  an explicit transaction opened against the enclosing [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
  object (such as from calling [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) without a rollback or
  commit, or calling [Connection.close()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.close) without first closing a
  transaction declared with [Connection.begin()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.begin)), a double-checkin would
  result, which could then lead towards concurrent checkouts of the same
  connection. The double-checkin condition is now prevented overall by an
  assertion, as well as the specific double-checkin scenario has been
  fixed.
  References: [#4252](https://www.sqlalchemy.org/trac/ticket/4252)
- Fixed a reference leak issue where the values of the parameter dictionary
  used in a statement execution would remain referenced by the “compiled
  cache”, as a result of storing the key view used by Python 3 dictionary
  keys().  Pull request courtesy Olivier Grisel.

### sql

- Fixed issue where the “ambiguous literal” error message used when
  interpreting literal values as SQL expression values would encounter a
  tuple value, and fail to format the message properly. Pull request courtesy
  Miguel Ventura.

### mssql

- Fixed a 1.2 regression caused by [#4061](https://www.sqlalchemy.org/trac/ticket/4061) where the SQL Server
  “BIT” type would be considered to be “native boolean”.  The goal here
  was to avoid creating a CHECK constraint on the column, however the bigger
  issue is that the BIT value does not behave like a true/false constant
  and cannot be interpreted as a standalone expression, e.g.
  “WHERE <column>”.   The SQL Server dialect now goes back to being
  non-native boolean, but with an extra flag that still avoids creating
  the CHECK constraint.
  References: [#4250](https://www.sqlalchemy.org/trac/ticket/4250)

### oracle

- The Oracle BINARY_FLOAT and BINARY_DOUBLE datatypes now participate within
  cx_Oracle.setinputsizes(), passing along NATIVE_FLOAT, so as to support the
  NaN value.  Additionally, [BINARY_FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.BINARY_FLOAT),
  [BINARY_DOUBLE](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.BINARY_DOUBLE) and `DOUBLE_PRECISION` now
  subclass [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float), since these are floating point datatypes, not
  decimal.  These datatypes were already defaulting the
  [Float.asdecimal](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float.params.asdecimal) flag to False in line with what
  [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) already does.
  References: [#4264](https://www.sqlalchemy.org/trac/ticket/4264)
- Added reflection capabilities for the [BINARY_FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.BINARY_FLOAT),
  [BINARY_DOUBLE](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.BINARY_DOUBLE) datatypes.
- Altered the Oracle dialect such that when an [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) type is in
  use, the cx_Oracle.NUMERIC type is set up for setinputsizes().  In
  SQLAlchemy 1.1 and earlier, cx_Oracle.NUMERIC was passed for all numeric
  types unconditionally, and in 1.2 this was removed to allow for better
  numeric precision.  However, for integers, some database/client setups
  will fail to coerce boolean values True/False into integers which introduces
  regressive behavior when using SQLAlchemy 1.2.  Overall, the setinputsizes
  logic seems like it will need a lot more flexibility going forward so this
  is a start for that.
  References: [#4259](https://www.sqlalchemy.org/trac/ticket/4259)

### tests

- Fixed a bug in the test suite where if an external dialect returned
  `None` for `server_version_info`, the exclusion logic would raise an
  `AttributeError`.
  References: [#4249](https://www.sqlalchemy.org/trac/ticket/4249)

### misc

- The horizontal sharding extension now makes use of the identity token
  added to ORM identity keys as part of [#4137](https://www.sqlalchemy.org/trac/ticket/4137), when an object
  refresh or column-based deferred load or unexpiration operation occurs.
  Since we know the “shard” that the object originated from, we make
  use of this value when refreshing, thereby avoiding queries against
  other shards that don’t match this object’s identity in any case.
  References: [#4247](https://www.sqlalchemy.org/trac/ticket/4247)
- Fixed a race condition which could occur if automap
  [AutomapBase.prepare()](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase.prepare) were used within a multi-threaded context
  against other threads which  may call [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) as a
  result of use of other mappers.  The unfinished mapping work of automap
  is particularly sensitive to being pulled in by a
  [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) step leading to errors.
  References: [#4266](https://www.sqlalchemy.org/trac/ticket/4266)

## 1.2.7

Released: April 20, 2018

### orm

- Fixed regression in 1.2 within sharded query feature where the
  new “identity_token” element was not being correctly considered within
  the scope of a lazy load operation, when searching the identity map
  for a related many-to-one element.   The new behavior will allow for
  making use of the “id_chooser” in order to determine the best identity
  key to retrieve from the identity map.  In order to achieve this, some
  refactoring of 1.2’s “identity_token” approach has made some slight changes
  to the implementation of `ShardedQuery` which should be noted for other
  derivations of this class.
  References: [#4228](https://www.sqlalchemy.org/trac/ticket/4228)
- Fixed issue in single-inheritance loading where the use of an aliased
  entity against a single-inheritance subclass in conjunction with the
  [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) method would cause the SQL to be rendered with
  the unaliased table mixed in to the query, causing a cartesian product.  In
  particular this was affecting the new “selectin” loader when used against a
  single-inheritance subclass.
  References: [#4241](https://www.sqlalchemy.org/trac/ticket/4241)

### sql

- Fixed issue where the compilation of an INSERT statement with the
  “literal_binds” option that also uses an explicit sequence and “inline”
  generation, as on PostgreSQL and Oracle, would fail to accommodate the
  extra keyword argument within the sequence processing routine.
  References: [#4231](https://www.sqlalchemy.org/trac/ticket/4231)

### postgresql

- Added new PG type [REGCLASS](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.REGCLASS) which assists in casting
  table names to OID values.  Pull request courtesy Sebastian Bank.
  References: [#4160](https://www.sqlalchemy.org/trac/ticket/4160)
- Fixed bug where the special “not equals” operator for the PostgreSQL
  “range” datatypes such as DATERANGE would fail to render “IS NOT NULL” when
  compared to the Python `None` value.
  References: [#4229](https://www.sqlalchemy.org/trac/ticket/4229)

### mssql

- Fixed 1.2 regression caused by [#4060](https://www.sqlalchemy.org/trac/ticket/4060) where the query used to
  reflect SQL Server cross-schema foreign keys was limiting the criteria
  incorrectly.
  References: [#4234](https://www.sqlalchemy.org/trac/ticket/4234)

### oracle

- The Oracle NUMBER datatype is reflected as INTEGER if the precision is NULL
  and the scale is zero, as this is how INTEGER values come back when
  reflected from Oracle’s tables.  Pull request courtesy Kent Bower.

## 1.2.6

Released: March 30, 2018

### orm

- Fixed bug where using [Mutable.associate_with()](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.Mutable.associate_with) or
  [Mutable.as_mutable()](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.Mutable.as_mutable) in conjunction with a class that has non-
  primary mappers set up with alternatively-named attributes would produce an
  attribute error.  Since non-primary mappers are not used for persistence,
  the mutable extension now excludes non-primary mappers from its
  instrumentation steps.
  References: [#4215](https://www.sqlalchemy.org/trac/ticket/4215)

### engine

- Fixed bug in connection pool where a connection could be present in the
  pool without all of its “connect” event handlers called, if a previous
  “connect” handler threw an exception; note that the dialects themselves
  have connect handlers that emit SQL, such as those which set transaction
  isolation, which can fail if the database is in a non-available state, but
  still allows a connection.  The connection is now invalidated first if any
  of the connect handlers fail.
  References: [#4225](https://www.sqlalchemy.org/trac/ticket/4225)

### sql

- Fixed a regression that occurred from the previous fix to [#4204](https://www.sqlalchemy.org/trac/ticket/4204) in
  version 1.2.5, where a CTE that refers to itself after the
  [CTE.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE.alias) method has been called would not refer to itself
  correctly.
  References: [#4204](https://www.sqlalchemy.org/trac/ticket/4204)

### postgresql

- Added support for “PARTITION BY” in PostgreSQL table definitions,
  using “postgresql_partition_by”.  Pull request courtesy
  Vsevolod Solovyov.

### mssql

- Adjusted the SQL Server version detection for pyodbc to only allow for
  numeric tokens, filtering out non-integers, since the dialect does tuple-
  numeric comparisons with this value.  This is normally true for all known
  SQL Server / pyodbc drivers in any case.
  References: [#4227](https://www.sqlalchemy.org/trac/ticket/4227)

### oracle

- The minimum cx_Oracle version supported is 5.2 (June 2015).  Previously,
  the dialect asserted against version 5.0 but as of 1.2.2 we are using some
  symbols that did not appear until 5.2.
  References: [#4211](https://www.sqlalchemy.org/trac/ticket/4211)

### misc

- Removed a warning that would be emitted when calling upon
  `__table_args__`, `__mapper_args__` as named with a `@declared_attr`
  method, when called from a non-mapped declarative mixin.  Calling these
  directly is documented as the approach to use when one is overriding one
  of these methods on a mapped class.  The warning still emits for regular
  attribute names.
  References: [#4221](https://www.sqlalchemy.org/trac/ticket/4221)

## 1.2.5

Released: March 6, 2018

### orm

- Added new feature [Query.only_return_tuples()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.only_return_tuples).  Causes the
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object to return keyed tuple objects unconditionally even
  if the query is against a single entity.   Pull request courtesy Eric
  Atkin.
- Fixed bug in new “polymorphic selectin” loading when a selection of
  polymorphic objects were to be partially loaded from a relationship
  lazy loader, leading to an “empty IN” condition within the load that
  raises an error for the “inline” form of “IN”.
  References: [#4199](https://www.sqlalchemy.org/trac/ticket/4199)
- Fixed 1.2 regression where a mapper option that contains an
  [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) object, as is typical when using the
  [QueryableAttribute.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute.of_type) method, could not be pickled.   1.1’s
  behavior was to omit the aliased class objects from the path, so this
  behavior is restored.
  References: [#4209](https://www.sqlalchemy.org/trac/ticket/4209)

### sql

- Fixed bug in :class:.`CTE` construct along the same lines as that of
  [#4204](https://www.sqlalchemy.org/trac/ticket/4204) where a [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) that was aliased would not copy itself
  correctly during a “clone” operation as is frequent within the ORM as well
  as when using the [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params) method.
  References: [#4210](https://www.sqlalchemy.org/trac/ticket/4210)
- Fixed bug in CTE rendering where a [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) that was also turned into
  an [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) would not render its “ctename AS aliasname” clause
  appropriately if there were more than one reference to the CTE in a FROM
  clause.
  References: [#4204](https://www.sqlalchemy.org/trac/ticket/4204)
- Fixed bug in new “expanding IN parameter” feature where the bind parameter
  processors for values wasn’t working at all, tests failed to cover this
  pretty basic case which includes that ENUM values weren’t working.
  References: [#4198](https://www.sqlalchemy.org/trac/ticket/4198)

### postgresql

- Fixed bug in PostgreSQL COLLATE / ARRAY adjustment first introduced
  in [#4006](https://www.sqlalchemy.org/trac/ticket/4006) where new behaviors in Python 3.7 regular expressions
  caused the fix to fail.
  This change is also **backported** to: 1.1.18
  References: [#4208](https://www.sqlalchemy.org/trac/ticket/4208)

### mysql

- MySQL dialects now query the server version using `SELECT @@version`
  explicitly to the server to ensure we are getting the correct version
  information back.   Proxy servers like MaxScale interfere with the value
  that is passed to the DBAPI’s connection.server_version value so this
  is no longer reliable.
  This change is also **backported** to: 1.1.18
  References: [#4205](https://www.sqlalchemy.org/trac/ticket/4205)

## 1.2.4

Released: February 22, 2018

### orm

- Fixed 1.2 regression in ORM versioning feature where a mapping against a
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) or [alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.alias) that also used a versioning column
  against the underlying table would fail due to the check added as part of
  [#3673](https://www.sqlalchemy.org/trac/ticket/3673).
  References: [#4193](https://www.sqlalchemy.org/trac/ticket/4193)

### engine

- Fixed regression caused in 1.2.3 due to fix from [#4181](https://www.sqlalchemy.org/trac/ticket/4181) where
  the changes to the event system involving [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) and
  `OptionEngine` did not accommodate for event removals, which
  would raise an `AttributeError` when invoked at the class
  level.
  References: [#4190](https://www.sqlalchemy.org/trac/ticket/4190)

### sql

- Fixed bug where CTE expressions would not have their name or alias name
  quoted when the given name is case sensitive or otherwise requires quoting.
  Pull request courtesy Eric Atkin.
  References: [#4197](https://www.sqlalchemy.org/trac/ticket/4197)

## 1.2.3

Released: February 16, 2018

### orm

- Added new argument [set_attribute.initiator](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.set_attribute.params.initiator)
  to the [set_attribute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.set_attribute) function, allowing an
  event token received from a listener function to be propagated
  to subsequent set events.
- Fixed issue in post_update feature where an UPDATE is emitted
  when the parent object has been deleted but the dependent object
  is not.   This issue has existed for a long time however
  since 1.2 now asserts rows matched for post_update, this
  was raising an error.
  This change is also **backported** to: 1.1.16
  References: [#4187](https://www.sqlalchemy.org/trac/ticket/4187)
- Fixed regression caused by fix for issue [#4116](https://www.sqlalchemy.org/trac/ticket/4116) affecting versions
  1.2.2 as well as 1.1.15, which had the effect of mis-calculation of the
  “owning class” of an [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) as the `NoneType` class
  in some declarative mixin/inheritance situations as well as if the
  association proxy were accessed off of an un-mapped class.  The “figure out
  the owner” logic has been replaced by an in-depth routine that searches
  through the complete mapper hierarchy assigned to the class or subclass to
  determine the correct (we hope) match; will not assign the owner if no
  match is found.  An exception is now raised if the proxy is used
  against an un-mapped instance.
  This change is also **backported** to: 1.1.16
  References: [#4185](https://www.sqlalchemy.org/trac/ticket/4185)
- Fixed bug where the [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) object did not
  correctly report upon the primary [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object
  represented by the bundle, if any.   An immediate
  side effect of this issue was that the new selectinload
  loader strategy wouldn’t work with the horizontal sharding
  extension.
  References: [#4175](https://www.sqlalchemy.org/trac/ticket/4175)
- Fixed bug in concrete inheritance mapping where user-defined
  attributes such as hybrid properties that mirror the names
  of mapped attributes from sibling classes would be overwritten by
  the mapper as non-accessible at the instance level.   Additionally
  ensured that user-bound descriptors are not implicitly invoked at the class
  level during the mapper configuration stage.
  References: [#4188](https://www.sqlalchemy.org/trac/ticket/4188)
- Fixed bug where the [reconstructor()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.reconstructor) event
  helper would not be recognized if it were applied to the
  `__init__()` method of the mapped class.
  References: [#4178](https://www.sqlalchemy.org/trac/ticket/4178)

### engine

- Fixed bug where events associated with an `Engine`
  at the class level would be doubled when the
  [Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options) method were used.  To
  achieve this, the semi-private class `OptionEngine`
  no longer accepts events directly at the class level
  and will raise an error; the class only propagates class-level
  events from its parent [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).   Instance-level
  events continue to work as before.
  References: [#4181](https://www.sqlalchemy.org/trac/ticket/4181)
- The [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object now allows query keys to be specified multiple
  times where their values will be joined into a list.  This is to support
  the plugins feature documented at [CreateEnginePlugin](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CreateEnginePlugin) which
  documents that “plugin” can be passed multiple times. Additionally, the
  plugin names can be passed to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) outside of the URL
  using the new [create_engine.plugins](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.plugins) parameter.
  References: [#4170](https://www.sqlalchemy.org/trac/ticket/4170)

### sql

- Added support for [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) to persist the values of the enumeration,
  rather than the keys, when using a Python pep-435 style enumerated object.
  The user supplies a callable function that will return the string values to
  be persisted.  This allows enumerations against non-string values to be
  value-persistable as well.  Pull request courtesy Jon Snyder.
  References: [#3906](https://www.sqlalchemy.org/trac/ticket/3906)
- Fixed bug where the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) type wouldn’t handle
  enum “aliases” correctly, when more than one key refers to the
  same value.  Pull request courtesy Daniel Knell.
  References: [#4180](https://www.sqlalchemy.org/trac/ticket/4180)

### postgresql

- Added “SSL SYSCALL error: Operation timed out” to the list
  of messages that trigger a “disconnect” scenario for the
  psycopg2 driver.  Pull request courtesy André Cruz.
  This change is also **backported** to: 1.1.16
- Added “TRUNCATE” to the list of keywords accepted by the
  PostgreSQL dialect as an “autocommit”-triggering keyword.
  Pull request courtesy Jacob Hayes.
  This change is also **backported** to: 1.1.16

### sqlite

- Fixed the import error raised when a platform
  has neither pysqlite2 nor sqlite3 installed, such
  that the sqlite3-related import error is raised,
  not the pysqlite2 one which is not the actual
  failure mode.  Pull request courtesy Robin.

### oracle

- The ON DELETE options for foreign keys are now part of
  Oracle reflection.  Oracle does not support ON UPDATE
  cascades.  Pull request courtesy Miroslav Shubernetskiy.
- Fixed bug in cx_Oracle disconnect detection, used by pre_ping and other
  features, where an error could be raised as DatabaseError which includes a
  numeric error code; previously we weren’t checking in this case for a
  disconnect code.
  References: [#4182](https://www.sqlalchemy.org/trac/ticket/4182)

### tests

- A test added in 1.2 thought to confirm a Python 2.7 behavior turns out to
  be confirming the behavior only as of Python 2.7.8. Python bug #8743 still
  impacts set comparison in Python 2.7.7 and earlier, so the test in question
  involving AssociationSet no longer runs for these older Python 2.7
  versions.
  References: [#3265](https://www.sqlalchemy.org/trac/ticket/3265)

### misc

- Fixed a fairly serious connection pool bug where a connection that is
  acquired after being refreshed as a result of a user-defined
  [DisconnectionError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DisconnectionError) or due to the 1.2-released “pre_ping” feature
  would not be correctly reset if the connection were returned to the pool by
  weakref cleanup (e.g. the front-facing object is garbage collected); the
  weakref would still refer to the previously invalidated DBAPI connection
  which would have the reset operation erroneously called upon it instead.
  This would lead to stack traces in the logs and a connection being checked
  into the pool without being reset, which can cause locking issues.
  This change is also **backported** to: 1.1.16
  References: [#4184](https://www.sqlalchemy.org/trac/ticket/4184)

## 1.2.2

Released: January 24, 2018

### orm

- Fixed 1.2 regression regarding new bulk_replace event
  where a backref would fail to remove an object from the
  previous owner when a bulk-assignment assigned the
  object to a new owner.
  References: [#4171](https://www.sqlalchemy.org/trac/ticket/4171)

### mysql

- Added more MySQL 8.0 reserved words to the MySQL dialect
  for quoting purposes.  Pull request courtesy
  Riccardo Magliocchetti.

### mssql

- Added ODBC error code 10054 to the list of error
  codes that count as a disconnect for ODBC / MSSQL server.
  References: [#4164](https://www.sqlalchemy.org/trac/ticket/4164)

### oracle

- The cx_Oracle dialect now calls setinputsizes() with cx_Oracle.NCHAR
  unconditionally when the NVARCHAR2 datatype, in SQLAlchemy corresponding
  to sqltypes.Unicode(), is in use.  Per cx_Oracle’s author this allows
  the correct conversions to occur within the Oracle client regardless
  of the setting for NLS_NCHAR_CHARACTERSET.
  References: [#4163](https://www.sqlalchemy.org/trac/ticket/4163)

## 1.2.1

Released: January 15, 2018

### orm

- Fixed bug where an object that is expunged during a rollback of
  a nested or subtransaction which also had its primary key mutated
  would not be correctly removed from the session, causing subsequent
  issues in using the session.
  This change is also **backported** to: 1.1.16
  References: [#4151](https://www.sqlalchemy.org/trac/ticket/4151)
- Fixed regression where pickle format of a Load / _UnboundLoad object (e.g.
  loader options) changed and `__setstate__()` was raising an
  UnboundLocalError for an object received from the legacy format, even
  though an attempt was made to do so.  tests are now added to ensure this
  works.
  References: [#4159](https://www.sqlalchemy.org/trac/ticket/4159)
- Fixed regression caused by new lazyload caching scheme in [#3954](https://www.sqlalchemy.org/trac/ticket/3954)
  where a query that makes use of loader options with of_type would cause
  lazy loads of unrelated paths to fail with a TypeError.
  References: [#4153](https://www.sqlalchemy.org/trac/ticket/4153)
- Fixed bug in new “selectin” relationship loader where the loader could try
  to load a non-existent relationship when loading a collection of
  polymorphic objects, where only some of the mappers include that
  relationship, typically when [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) is being used.
  References: [#4156](https://www.sqlalchemy.org/trac/ticket/4156)

### sql

- Fixed bug in [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) where using the “multi-values”
  format in combination with [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects as keys rather
  than strings would fail.   Pull request courtesy Aubrey Stark-Toller.
  This change is also **backported** to: 1.1.16
  References: [#4162](https://www.sqlalchemy.org/trac/ticket/4162)

### mssql

- Fixed regression in 1.2 where newly repaired quoting
  of collation names in [#3785](https://www.sqlalchemy.org/trac/ticket/3785) breaks SQL Server,
  which explicitly does not understand a quoted collation
  name.   Whether or not mixed-case collation names are
  quoted or not is now deferred down to a dialect-level
  decision so that each dialect can prepare these identifiers
  directly.
  References: [#4154](https://www.sqlalchemy.org/trac/ticket/4154)

### oracle

- Fixed regression where the removal of most setinputsizes
  rules from cx_Oracle dialect impacted the TIMESTAMP
  datatype’s ability to retrieve fractional seconds.
  References: [#4157](https://www.sqlalchemy.org/trac/ticket/4157)
- Fixed regression in Oracle imports where a missing comma caused
  an undefined symbol to be present.  Pull request courtesy
  Miroslav Shubernetskiy.

### tests

- Removed an oracle-specific requirements rule from the public
  test suite that was interfering with third party dialect
  suites.
- Added a new exclusion rule group_by_complex_expression
  which disables tests that use “GROUP BY <expr>”, which seems
  to be not viable for at least two third party dialects.

### misc

- Fixed regression in association proxy due to [#3769](https://www.sqlalchemy.org/trac/ticket/3769)
  (allow for chained any() / has()) where contains() against
  an association proxy chained in the form
  (o2m relationship, associationproxy(m2o relationship, m2o relationship))
  would raise an error regarding the re-application of contains()
  on the final link of the chain.
  References: [#4150](https://www.sqlalchemy.org/trac/ticket/4150)

## 1.2.0

Released: December 27, 2017

### orm

- Added a new data member to the identity key tuple
  used by the ORM’s identity map, known as the
  “identity_token”.  This token defaults to None but
  may be used by database sharding schemes to differentiate
  objects in memory with the same primary key that come
  from different databases.   The horizontal sharding
  extension integrates this token applying the shard
  identifier to it, thus allowing primary keys to be
  duplicated across horizontally sharded backends.
  See also
  [Identity key enhancements to support sharding](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-4137)
  References: [#4137](https://www.sqlalchemy.org/trac/ticket/4137)
- Fixed bug where the association proxy would inadvertently link itself
  to an [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) object if it were called first with
  the [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) as a parent, causing errors upon subsequent
  usage.
  This change is also **backported** to: 1.1.15
  References: [#4116](https://www.sqlalchemy.org/trac/ticket/4116)
- Fixed bug in [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) query option where making use of a
  path that used [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) to refer to a subclass
  across more than one level of joins would also require that the “alias”
  argument were provided with the same subtype in order to avoid adding
  unwanted FROM clauses to the query; additionally,  using
  [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) across subclasses that use [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) objects
  of subclasses as the [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) argument will also
  render correctly.
  References: [#4130](https://www.sqlalchemy.org/trac/ticket/4130)
- The [Query.exists()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.exists) method will now disable eager loaders for when
  the query is rendered.  Previously, joined-eager load joins would be rendered
  unnecessarily as well as subquery eager load queries would be needlessly
  generated.   The new behavior matches that of the [Query.subquery()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.subquery)
  method.
  References: [#4032](https://www.sqlalchemy.org/trac/ticket/4032)

### orm declarative

- Fixed a bug where a descriptor, which is a mapped column or a
  relationship elsewhere in a hierarchy based on
  [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase), would be referenced during a refresh
  operation, leading to an error since the attribute is not mapped as a
  mapper property. A similar issue can arise for other attributes
  like the “type” column added by [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) if the
  class fails to include “concrete=True” in its mapper, however the check
  here should also prevent that scenario from causing a problem.
  This change is also **backported** to: 1.1.15
  References: [#4124](https://www.sqlalchemy.org/trac/ticket/4124)

### engine

- The “password” attribute of the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object can now be
  any user-defined or user-subclassed string object that responds to the
  Python `str()` builtin.   The object passed will be maintained as the
  datamember `URL.password_original` and will be consulted
  when the `URL.password` attribute is read to produce the
  string value.
  References: [#4089](https://www.sqlalchemy.org/trac/ticket/4089)

### sql

- Fixed bug where `__repr__` of [ColumnDefault](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.ColumnDefault) would fail
  if the argument were a tuple.  Pull request courtesy Nicolas Caniart.
  This change is also **backported** to: 1.1.15
  References: [#4126](https://www.sqlalchemy.org/trac/ticket/4126)
- Reworked the new “autoescape” feature introduced in
  [New “autoescape” option for startswith(), endswith()](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-2694) in 1.2.0b2 to be fully automatic; the escape
  character now defaults to a forwards slash `"/"` and
  is applied to percent, underscore, as well as the escape
  character itself, for fully automatic escaping.  The
  character can also be changed using the “escape” parameter.
  See also
  [New “autoescape” option for startswith(), endswith()](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-2694)
  References: [#2694](https://www.sqlalchemy.org/trac/ticket/2694)
- Fixed bug where the [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata) method would not properly
  accommodate [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) objects that didn’t consist of simple
  column expressions, such as indexes against a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct,
  indexes that used SQL expressions or `func`, etc.   The routine
  now copies expressions fully to a new [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) object while
  substituting all table-bound [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects for those
  of the target table.
  References: [#4147](https://www.sqlalchemy.org/trac/ticket/4147)
- Changed the “visit name” of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) from “column” to
  “column_element”, so that when this element is used as the basis for a
  user-defined SQL element, it is not assumed to behave like a table-bound
  [ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause) when processed by various SQL traversal utilities,
  as are commonly used by the ORM.
  References: [#4142](https://www.sqlalchemy.org/trac/ticket/4142)
- Fixed issue in [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) datatype which is essentially the same
  issue as that of [#3832](https://www.sqlalchemy.org/trac/ticket/3832), except not a regression, where
  column attachment events on top of [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) would not fire
  correctly, thus interfering with systems which rely upon this.   A key
  use case that was broken by this is the use of mixins to declare
  columns that make use of `MutableList.as_mutable()`.
  References: [#4141](https://www.sqlalchemy.org/trac/ticket/4141)
- Fixed bug in new “expanding bind parameter” feature whereby if multiple
  params were used in one statement, the regular expression would not
  match the parameter name correctly.
  References: [#4140](https://www.sqlalchemy.org/trac/ticket/4140)
- Implemented “DELETE..FROM” syntax for PostgreSQL, MySQL, MS SQL Server
  (as well as within the unsupported Sybase dialect) in a manner similar
  to how “UPDATE..FROM” works.  A DELETE statement that refers to more than
  one table will switch into “multi-table” mode and render the appropriate
  “USING” or multi-table “FROM” clause as understood by the database.
  Pull request courtesy Pieter Mulder.
  See also
  [Multiple-table criteria support for DELETE](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-959)
  References: [#959](https://www.sqlalchemy.org/trac/ticket/959)

### postgresql

- Added new [MONEY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.MONEY) datatype.  Pull request courtesy
  Cleber J Santos.

### mysql

- MySQL 5.7.20 now warns for use of the @tx_isolation variable; a version
  check is now performed and uses @transaction_isolation instead
  to prevent this warning.
  This change is also **backported** to: 1.1.15
  References: [#4120](https://www.sqlalchemy.org/trac/ticket/4120)
- Fixed regression from issue 1.2.0b3 where “MariaDB” version comparison can
  fail for some particular MariaDB version strings under Python 3.
  References: [#4115](https://www.sqlalchemy.org/trac/ticket/4115)

### mssql

- Fixed bug where sqltypes.BINARY and sqltypes.VARBINARY datatypes
  would not include correct bound-value handlers for pyodbc,
  which allows the pyodbc.NullParam value to be passed that
  helps with FreeTDS.
  References: [#4121](https://www.sqlalchemy.org/trac/ticket/4121)

### oracle

- Added some additional rules to fully handle `Decimal('Infinity')`,
  `Decimal('-Infinity')` values with cx_Oracle numerics when using
  `asdecimal=True`.
  References: [#4064](https://www.sqlalchemy.org/trac/ticket/4064)

### misc

- Added a new errors section to the documentation with background
  about common error messages.   Selected exceptions within SQLAlchemy
  will include a link in their string output to the relevant section
  within this page.
- Added new method `Result.with_post_criteria()` to baked
  query system, allowing non-SQL-modifying transformations to take place
  after the query has been pulled from the cache.  Among other things,
  this method can be used with [ShardedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedQuery)
  to set the shard identifier.   [ShardedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedQuery)
  has also been modified such that its `ShardedQuery.get()` method
  interacts correctly with that of `Result`.
  References: [#4135](https://www.sqlalchemy.org/trac/ticket/4135)

## 1.2.0b3

Released: October 13, 2017

### orm

- Fixed bug where ORM relationship would warn against conflicting sync
  targets (e.g. two relationships would both write to the same column) for
  sibling classes in an inheritance hierarchy, where the two relationships
  would never actually conflict during writes.
  This change is also **backported** to: 1.1.15
  References: [#4078](https://www.sqlalchemy.org/trac/ticket/4078)
- Fixed bug where correlated select used against single-table inheritance
  entity would fail to render correctly in the outer query, due to adjustment
  for single inheritance discriminator criteria inappropriately re-applying
  the criteria to the outer query.
  This change is also **backported** to: 1.1.15
  References: [#4103](https://www.sqlalchemy.org/trac/ticket/4103)
- Fixed bug in [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) following along similar lines as that
  of [#4030](https://www.sqlalchemy.org/trac/ticket/4030), where an internal check for a target object in
  the identity map could lead to an error if it were to be garbage collected
  immediately before the merge routine actually retrieves the object.
  This change is also **backported** to: 1.1.14
  References: [#4069](https://www.sqlalchemy.org/trac/ticket/4069)
- Fixed bug where an [undefer_group()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer_group) option would not be recognized
  if it extended from a relationship that was loading using joined eager
  loading.  Additionally, as the bug led to excess work being performed,
  Python function call counts are also improved by 20% within the initial
  calculation of result set columns, complementing the joined eager load
  improvements of [#3915](https://www.sqlalchemy.org/trac/ticket/3915).
  This change is also **backported** to: 1.1.14
  References: [#4048](https://www.sqlalchemy.org/trac/ticket/4048)
- Fixed bug in [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) where objects in a collection that had
  the primary key attribute set to `None` for a key that is  typically
  autoincrementing would be considered to be a database-persisted key for
  part of the internal deduplication process, causing only one object to
  actually be inserted in the database.
  This change is also **backported** to: 1.1.14
  References: [#4056](https://www.sqlalchemy.org/trac/ticket/4056)
- An [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) is raised when a [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym)
  is used against an attribute that is not against a [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty),
  such as an association proxy.  Previously, a recursion overflow would
  occur trying to locate non-existent attributes.
  This change is also **backported** to: 1.1.14
  References: [#4067](https://www.sqlalchemy.org/trac/ticket/4067)
- Fixed regression introduced in 1.2.0b1 due to [#3934](https://www.sqlalchemy.org/trac/ticket/3934) where the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) would fail to “deactivate” the transaction, if a
  rollback failed (the target issue is when MySQL loses track of a SAVEPOINT).
  This would cause a subsequent call to [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) to raise
  an error a second time, rather than completing and bringing the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) back to ACTIVE.
  References: [#4050](https://www.sqlalchemy.org/trac/ticket/4050)
- Fixed issue where the [make_transient_to_detached()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.make_transient_to_detached) function
  would expire all attributes on the target object, including “deferred”
  attributes, which has the effect of the attribute being undeferred
  for the next refresh, causing an unexpected load of the attribute.
  References: [#4084](https://www.sqlalchemy.org/trac/ticket/4084)
- Fixed bug involving delete-orphan cascade where a related item
  that becomes an orphan before the parent object is part of a
  session is still tracked as moving into orphan status, which results
  in it being expunged from the session rather than being flushed.
  Note
  This fix was inadvertently merged during the 1.2.0b3
  release and was **not added to the changelog** at that time.
  This changelog note was added to the release retroactively as of
  version 1.2.13.
  References: [#4040](https://www.sqlalchemy.org/trac/ticket/4040)
- Fixed bug in [“selectin” polymorphic loading, loads subclasses using separate IN queries](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3948) which prevented “selectin” and
  “inline” settings in a multi-level class hierarchy from interacting
  together as expected.
  References: [#4026](https://www.sqlalchemy.org/trac/ticket/4026)
- Removed the warnings that are emitted when the LRU caches employed
  by the mapper as well as loader strategies reach their threshold; the
  purpose of this warning was at first a guard against excess cache keys
  being generated but became basically a check on the “creating many
  engines” antipattern.   While this is still an antipattern, the presence
  of test suites which both create an engine per test as well as raise
  on all warnings will be an inconvenience; it should not be critical
  that such test suites change their architecture just for this warning
  (though engine-per-test suite is always better).
  References: [#4071](https://www.sqlalchemy.org/trac/ticket/4071)
- Fixed regression where the use of a [undefer_group()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer_group) option
  in conjunction with a lazy loaded relationship option would cause
  an attribute error, due to a bug in the SQL cache key generation
  added in 1.2 as part of [#3954](https://www.sqlalchemy.org/trac/ticket/3954).
  References: [#4049](https://www.sqlalchemy.org/trac/ticket/4049)
- Modified the change made to the ORM update/delete evaluator in
  [#3366](https://www.sqlalchemy.org/trac/ticket/3366) such that if an unmapped column expression is present
  in the update or delete, if the evaluator can match its name to the
  mapped columns of the target class, a warning is emitted, rather than
  raising UnevaluatableError.  This is essentially the pre-1.2 behavior,
  and is to allow migration for applications that are currently relying
  upon this pattern.  However, if the given attribute name cannot be
  matched to the columns of the mapper, the UnevaluatableError is
  still raised, which is what was fixed in [#3366](https://www.sqlalchemy.org/trac/ticket/3366).
  References: [#4073](https://www.sqlalchemy.org/trac/ticket/4073)

### orm declarative

- A warning is emitted if a subclass attempts to override an attribute
  that was declared on a superclass using `@declared_attr.cascading`
  that the overridden attribute will be ignored. This use
  case cannot be fully supported down to further subclasses without more
  complex development efforts, so for consistency the “cascading” is
  honored all the way down regardless of overriding attributes.
  References: [#4091](https://www.sqlalchemy.org/trac/ticket/4091)
- A warning is emitted if the `@declared_attr.cascading` attribute is
  used with a special declarative name such as `__tablename__`, as this
  has no effect.
  References: [#4092](https://www.sqlalchemy.org/trac/ticket/4092)

### engine

- Added `__next__()` and `next()` methods to `ResultProxy`,
  so that the `next()` builtin function works on the object directly.
  `ResultProxy` has long had an `__iter__()` method which already
  allows it to respond to the `iter()` builtin.   The implementation
  for `__iter__()` is unchanged, as performance testing has indicated
  that iteration using a `__next__()` method with `StopIteration`
  is about 20% slower in both Python 2.7 and 3.6.
  References: [#4077](https://www.sqlalchemy.org/trac/ticket/4077)
- Made some adjustments to [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) and [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) such
  that recovery logic is not run underneath exception catches for
  `pool.Empty`, `AttributeError`, since when the recovery operation
  itself fails, Python 3 creates a misleading stack trace referring to the
  `Empty` / `AttributeError` as the cause, when in fact these exception
  catches are part of control flow.
  References: [#4028](https://www.sqlalchemy.org/trac/ticket/4028)

### sql

- Fixed bug where the recently added [ColumnOperators.any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.any_)
  and [ColumnOperators.all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.all_) methods didn’t work when called
  as methods, as opposed to using the standalone functions
  [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) and [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_).  Also
  added documentation examples for these relatively unintuitive
  SQL operators.
  This change is also **backported** to: 1.1.15
  References: [#4093](https://www.sqlalchemy.org/trac/ticket/4093)
- Added a new method [DefaultExecutionContext.get_current_parameters()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultExecutionContext.get_current_parameters)
  which is used within a function-based default value generator in
  order to retrieve the current parameters being passed to the statement.
  The new function differs from the
  [DefaultExecutionContext.current_parameters](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultExecutionContext.current_parameters) attribute in
  that it also provides for optional grouping of parameters that
  correspond to a multi-valued “insert” construct.  Previously it was not
  possible to identify the subset of parameters that were relevant to
  the function call.
  See also
  [Parameter helper for multi-valued INSERT with contextual default generator](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-4075)
  [Context-Sensitive Default Functions](https://docs.sqlalchemy.org/en/20/core/defaults.html#context-default-functions)
  References: [#4075](https://www.sqlalchemy.org/trac/ticket/4075)
- Fixed bug in new SQL comments feature where table and column comment
  would not be copied when using [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata).
  References: [#4087](https://www.sqlalchemy.org/trac/ticket/4087)
- In release 1.1, the [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) type was broken in that
  boolean coercion via `bool()` would occur for backends that did not
  feature “native boolean”, but would not occur for native boolean backends,
  meaning the string `"0"` now behaved inconsistently. After a poll, a
  consensus was reached that non-boolean values should be raising an error,
  especially in the ambiguous case of string `"0"`; so the [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)
  datatype will now raise `ValueError` if an incoming value is not
  within the range `None, True, False, 1, 0`.
  See also
  [Boolean datatype now enforces strict True/False/None values](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-4102)
  References: [#4102](https://www.sqlalchemy.org/trac/ticket/4102)
- Refined the behavior of [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) such that in all cases,
  if the [Operators.op.is_comparison](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op.params.is_comparison) flag is set to True,
  the return type of the resulting expression will be
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean), and if the flag is False, the return type of the
  resulting expression will be the same type as that of the left-hand
  expression, which is the typical default behavior of other operators.
  Also added a new parameter [Operators.op.return_type](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op.params.return_type) as well
  as a helper method [Operators.bool_op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.bool_op).
  See also
  [The typing behavior of custom operators has been made consistent](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-4063)
  References: [#4063](https://www.sqlalchemy.org/trac/ticket/4063)
- Internal refinements to the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum), [Interval](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Interval), and
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) types, which now extend a common mixin
  `Emulated` that indicates a type that provides Python-side
  emulation of a DB native type, switching out to the DB native type when
  a supporting backend is in use.   The PostgreSQL
  [INTERVAL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.INTERVAL) type when used directly will now include
  the correct type coercion rules for SQL expressions that also take
  effect for [Interval](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Interval) (such as adding a date to an
  interval yields a datetime).
  References: [#4088](https://www.sqlalchemy.org/trac/ticket/4088)

### postgresql

- Added a new flag `use_batch_mode` to the psycopg2 dialect.  This flag
  enables the use of psycopg2’s `psycopg2.extras.execute_batch`
  extension when the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) calls upon
  `cursor.executemany()`. This extension provides a critical
  performance increase by over an order of magnitude when running INSERT
  statements in batch.  The flag is False by default as it is considered
  to be experimental for now.
  See also
  [Support for Batch Mode / Fast Execution Helpers](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-4109)
  References: [#4109](https://www.sqlalchemy.org/trac/ticket/4109)
- Made further fixes to the [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) class in conjunction with
  COLLATE, as the fix made in [#4006](https://www.sqlalchemy.org/trac/ticket/4006) failed to accommodate
  for a multidimensional array.
  This change is also **backported** to: 1.1.15
  References: [#4006](https://www.sqlalchemy.org/trac/ticket/4006)
- Fixed bug in [array_agg](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg) function where passing an argument
  that is already of type [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), such as a PostgreSQL
  [array](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array) construct, would produce a `ValueError`, due
  to the function attempting to nest the arrays.
  This change is also **backported** to: 1.1.15
  References: [#4107](https://www.sqlalchemy.org/trac/ticket/4107)
- Fixed bug in PostgreSQL `Insert.on_conflict_do_update()`
  which would prevent the insert statement from being used as a CTE,
  e.g. via `Insert.cte()`, within another statement.
  This change is also **backported** to: 1.1.15
  References: [#4074](https://www.sqlalchemy.org/trac/ticket/4074)
- Fixed bug where the pg8000 driver would fail if using
  [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) with a schema name, since the schema name would
  be sent as a “quoted_name” object that’s a string subclass, which pg8000
  doesn’t recognize.   The quoted_name type is added to pg8000’s
  py_types collection on connect.
  References: [#4041](https://www.sqlalchemy.org/trac/ticket/4041)
- Enabled UUID support for the pg8000 driver, which supports native Python
  uuid round trips for this datatype.  Arrays of UUID are still not supported,
  however.
  References: [#4016](https://www.sqlalchemy.org/trac/ticket/4016)

### mysql

- Warning emitted when MariaDB 10.2.8 or earlier in the 10.2
  series is detected as there are major issues with CHECK
  constraints within these versions that were resolved as of
  10.2.9.
  Note that this changelog message was NOT released with
  SQLAlchemy 1.2.0b3 and was added retroactively.
  This change is also **backported** to: 1.1.15
  References: [#4097](https://www.sqlalchemy.org/trac/ticket/4097)
- Fixed issue where CURRENT_TIMESTAMP would not reflect correctly
  in the MariaDB 10.2 series due to a syntax change, where the function
  is now represented as `current_timestamp()`.
  This change is also **backported** to: 1.1.15
  References: [#4096](https://www.sqlalchemy.org/trac/ticket/4096)
- MariaDB 10.2 now supports CHECK constraints (warning: use version 10.2.9
  or greater due to upstream issues noted in [#4097](https://www.sqlalchemy.org/trac/ticket/4097)).  Reflection
  now takes these CHECK constraints into account when they are present in
  the `SHOW CREATE TABLE` output.
  This change is also **backported** to: 1.1.15
  References: [#4098](https://www.sqlalchemy.org/trac/ticket/4098)
- Changed the name of the `.values` attribute of the new MySQL
  INSERT..ON DUPLICATE KEY UPDATE construct to `.inserted`, as
  [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) already has a method called [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values).
  The `.inserted` attribute ultimately renders the MySQL `VALUES()`
  function.
  References: [#4072](https://www.sqlalchemy.org/trac/ticket/4072)

### sqlite

- Fixed bug where SQLite CHECK constraint reflection would fail
  if the referenced table were in a remote schema, e.g. on SQLite a
  remote database referred to by ATTACH.
  This change is also **backported** to: 1.1.15
  References: [#4099](https://www.sqlalchemy.org/trac/ticket/4099)

### mssql

- Added a new [TIMESTAMP](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.TIMESTAMP) datatype, that
  correctly acts like a binary datatype for SQL Server
  rather than a datetime type, as SQL Server breaks the
  SQL standard here.  Also added [ROWVERSION](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.ROWVERSION),
  as the “TIMESTAMP” type in SQL Server is deprecated in
  favor of ROWVERSION.
  References: [#4086](https://www.sqlalchemy.org/trac/ticket/4086)
- Added support for “AUTOCOMMIT” isolation level, as established
  via [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options), to the
  PyODBC and pymssql dialects.   This isolation level sets the
  appropriate DBAPI-specific flags on the underlying
  connection object.
  References: [#4058](https://www.sqlalchemy.org/trac/ticket/4058)
- Added a full range of “connection closed” exception codes to the
  PyODBC dialect for SQL Server, including ‘08S01’, ‘01002’, ‘08003’,
  ‘08007’, ‘08S02’, ‘08001’, ‘HYT00’, ‘HY010’.  Previously, only ‘08S01’
  was covered.
  This change is also **backported** to: 1.1.15
  References: [#4095](https://www.sqlalchemy.org/trac/ticket/4095)
- SQL Server supports what SQLAlchemy calls “native boolean”
  with its BIT type, as this type only accepts 0 or 1 and the
  DBAPIs return its value as True/False.   So the SQL Server
  dialects now enable “native boolean” support, in that a
  CHECK constraint is not generated for a [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)
  datatype.  The only difference vs. other native boolean
  is that there are no “true” / “false” constants so “1” and
  “0” are still rendered here.
  References: [#4061](https://www.sqlalchemy.org/trac/ticket/4061)
- Fixed the pymssql dialect so that percent signs in SQL text, such
  as used in modulus expressions or literal textual values, are
  **not** doubled up, as seems to be what pymssql expects.  This is
  despite the fact that the pymssql DBAPI uses the “pyformat” parameter
  style which itself considers the percent sign to be significant.
  References: [#4057](https://www.sqlalchemy.org/trac/ticket/4057)
- Fixed bug where the SQL Server dialect could pull columns from multiple
  schemas when reflecting a self-referential foreign key constraint, if
  multiple schemas contained a constraint of the same name against a
  table of the same name.
  References: [#4060](https://www.sqlalchemy.org/trac/ticket/4060)
- Added a new class of “rowcount support” for dialects that is specific to
  when “RETURNING”, which on SQL Server looks like “OUTPUT inserted”, is in
  use, as the PyODBC backend isn’t able to give us rowcount on an UPDATE or
  DELETE statement when OUTPUT is in effect.  This primarily affects the ORM
  when a flush is updating a row that contains server-calculated values,
  raising an error if the backend does not return the expected row count.
  PyODBC now states that it supports rowcount except if OUTPUT.inserted is
  present, which is taken into account by the ORM during a flush as to
  whether it will look for a rowcount.
  References: [#4062](https://www.sqlalchemy.org/trac/ticket/4062)
- Enabled the “sane_rowcount” flag for the pymssql dialect, indicating
  that the DBAPI now reports the correct number of rows affected from
  an UPDATE or DELETE statement.  This impacts mostly the ORM versioning
  feature in that it now can verify the number of rows affected on a
  target version.
- Added a rule to SQL Server index reflection to ignore the so-called
  “heap” index that is implicitly present on a table that does not
  specify a clustered index.
  References: [#4059](https://www.sqlalchemy.org/trac/ticket/4059)

### oracle

- Fixed performance regression caused by the fix for [#3937](https://www.sqlalchemy.org/trac/ticket/3937) where
  cx_Oracle as of version 5.3 dropped the `.UNICODE` symbol from its
  namespace,  which was interpreted as cx_Oracle’s “WITH_UNICODE” mode being
  turned on unconditionally, which invokes functions on the SQLAlchemy
  side which convert all strings to unicode unconditionally and causing
  a performance impact.  In fact, per cx_Oracle’s author the
  “WITH_UNICODE” mode has been removed entirely as of 5.1, so the expensive unicode
  conversion functions are no longer necessary and are disabled if
  cx_Oracle 5.1 or greater is detected under Python 2.  The warning against
  “WITH_UNICODE” mode that was removed under [#3937](https://www.sqlalchemy.org/trac/ticket/3937) is also restored.
  This change is also **backported** to: 1.1.13, 1.0.19
  References: [#4035](https://www.sqlalchemy.org/trac/ticket/4035)
- Partial support for persisting and retrieving the Oracle value
  “infinity” is implemented with cx_Oracle, using Python float values
  only, e.g. `float("inf")`.  Decimal support is not yet fulfilled by
  the cx_Oracle DBAPI driver.
  References: [#4064](https://www.sqlalchemy.org/trac/ticket/4064)
- The cx_Oracle dialect has been reworked and modernized to take advantage of
  new patterns that weren’t present in the old 4.x series of cx_Oracle. This
  includes that the minimum cx_Oracle version is the 5.x series and that
  cx_Oracle 6.x is now fully tested. The most significant change involves
  type conversions, primarily regarding the numeric / floating point and LOB
  datatypes, making more effective use of cx_Oracle type handling hooks to
  simplify how bind parameter and result data is processed.
  See also
  [Major Refactor to cx_Oracle Dialect, Typing System](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-cxoracle-12)
- two phase support for cx_Oracle has been completely removed for all
  versions of cx_Oracle, whereas in 1.2.0b1 this change only took effect for
  the 6.x series of cx_Oracle.  This feature never worked correctly
  in any version of cx_Oracle and in cx_Oracle 6.x, the API which SQLAlchemy
  relied upon was removed.
  See also
  [Major Refactor to cx_Oracle Dialect, Typing System](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-cxoracle-12)
  References: [#3997](https://www.sqlalchemy.org/trac/ticket/3997)
- The column keys present in a result set when using [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning)
  with the cx_Oracle backend now use the correct column / label names
  like that of all other dialects.  Previously, these came out as
  `ret_nnn`.
  See also
  [Major Refactor to cx_Oracle Dialect, Typing System](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-cxoracle-12)
- Several parameters to the cx_Oracle dialect are now deprecated and will
  have no effect: `auto_setinputsizes`, `exclude_setinputsizes`,
  `allow_twophase`.
  See also
  [Major Refactor to cx_Oracle Dialect, Typing System](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-cxoracle-12)
- Fixed bug where an index reflected under Oracle with an expression like
  “column DESC” would not be returned, if the table also had no primary
  key, as a result of logic that attempts to filter out the
  index implicitly added by Oracle onto the primary key columns.
  References: [#4042](https://www.sqlalchemy.org/trac/ticket/4042)
- Fixed more regressions caused by cx_Oracle 6.0; at the moment, the only
  behavioral change for users is disconnect detection now detects for
  cx_Oracle.DatabaseError in addition to cx_Oracle.InterfaceError, as
  this behavior seems to have changed.   Other issues regarding numeric
  precision and uncloseable connections are pending with the upstream
  cx_Oracle issue tracker.
  References: [#4045](https://www.sqlalchemy.org/trac/ticket/4045)
- Fixed bug where Oracle 8 “non ansi” join mode would not add the
  `(+)` operator to expressions that used an operator other than the
  `=` operator.  The `(+)` needs to be on all columns that are part
  of the right-hand side.
  References: [#4076](https://www.sqlalchemy.org/trac/ticket/4076)

## 1.2.0b2

Released: July 24, 2017

### orm

- Fixed regression from 1.1.11 where adding additional non-entity
  columns to a query that includes an entity with subqueryload
  relationships would fail, due to an inspection added in 1.1.11 as a
  result of [#4011](https://www.sqlalchemy.org/trac/ticket/4011).
  This change is also **backported** to: 1.1.12
  References: [#4033](https://www.sqlalchemy.org/trac/ticket/4033)
- Fixed bug involving JSON NULL evaluation logic added in 1.1 as part
  of [#3514](https://www.sqlalchemy.org/trac/ticket/3514) where the logic would not accommodate ORM
  mapped attributes named differently from the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  that was mapped.
  This change is also **backported** to: 1.1.12
  References: [#4031](https://www.sqlalchemy.org/trac/ticket/4031)
- Added `KeyError` checks to all methods within
  `WeakInstanceDict` where a check for `key in dict` is
  followed by indexed access to that key, to guard against a race against
  garbage collection that under load can remove the key from the dict
  after the code assumes its present, leading to very infrequent
  `KeyError` raises.
  This change is also **backported** to: 1.1.12
  References: [#4030](https://www.sqlalchemy.org/trac/ticket/4030)

### tests

- Fixed issue in testing fixtures which was incompatible with a change
  made as of Python 3.6.2 involving context managers.
  This change is also **backported** to: 1.1.12, 1.0.18
  References: [#4034](https://www.sqlalchemy.org/trac/ticket/4034)

## 1.2.0b1

Released: July 10, 2017

### orm

- An [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct can now be passed to the
  `Query.select_entity_from()` method.   Entities will be pulled
  from the selectable represented by the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct.
  This allows special options for [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) such as
  [aliased.adapt_on_names](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased.params.adapt_on_names) to be used in conjunction with
  `Query.select_entity_from()`.
  This change is also **backported** to: 1.1.7
  References: [#3933](https://www.sqlalchemy.org/trac/ticket/3933)
- Added `.autocommit` attribute to [scoped_session](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoped_session), proxying
  the `.autocommit` attribute of the underling [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  currently assigned to the thread.  Pull request courtesy
  Ben Fagin.
- Added a new feature [with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) that allows an ad-hoc
  SQL expression to be added to a specific entity in a query at result
  time.  This is an alternative to the SQL expression being delivered as
  a separate element in the result tuple.
  See also
  [ORM attributes that can receive ad-hoc SQL expressions](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3058)
  References: [#3058](https://www.sqlalchemy.org/trac/ticket/3058)
- Added a new style of mapper-level inheritance loading
  “polymorphic selectin”.  This style of loading
  emits queries for each subclass in an inheritance
  hierarchy subsequent to the load of the base
  object type, using IN to specify the desired
  primary key values.
  See also
  [“selectin” polymorphic loading, loads subclasses using separate IN queries](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3948)
  References: [#3948](https://www.sqlalchemy.org/trac/ticket/3948)
- Added a new kind of eager loading called “selectin” loading.  This
  style of loading is very similar to “subquery” eager loading,
  except that it uses an IN expression given a list of primary key
  values from the loaded parent objects, rather than re-stating the
  original query.   This produces a more efficient query that is
  “baked” (e.g. the SQL string is cached) and also works in the
  context of [Query.yield_per()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.yield_per).
  See also
  [New “selectin” eager loading, loads all collections at once using IN](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3944)
  References: [#3944](https://www.sqlalchemy.org/trac/ticket/3944)
- The `lazy="select"` loader strategy now makes used of the
  [BakedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery) query caching system in all cases.  This
  removes most overhead of generating a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object and
  running it into a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) and then string SQL statement from
  the process of lazy-loading related collections and objects.  The
  “baked” lazy loader has also been improved such that it can now
  cache in most cases where query load options are used.
  See also
  [“Baked” loading now the default for lazy loads](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3954)
  References: [#3954](https://www.sqlalchemy.org/trac/ticket/3954)
- The [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) method can now accommodate both
  hybrid attributes as well as composite attributes as a source
  of the key to be placed in the SET clause.   For hybrids, an
  additional decorator [hybrid_property.update_expression()](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property.update_expression)
  is supplied for which the user supplies a tuple-returning function.
  See also
  [Support for bulk updates of hybrids, composites](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3229)
  References: [#3229](https://www.sqlalchemy.org/trac/ticket/3229)
- Added new attribute event [AttributeEvents.bulk_replace()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.bulk_replace).
  This event is triggered when a collection is assigned to a
  relationship, before the incoming collection is compared with the
  existing one.  This early event allows for conversion of incoming
  non-ORM objects as well.  The event is integrated with the
  `@validates` decorator.
  See also
  [New bulk_replace event](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3896-event)
  References: [#3896](https://www.sqlalchemy.org/trac/ticket/3896)
- Added new event handler [AttributeEvents.modified()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.modified) which is
  triggered when the func:.attributes.flag_modified function is
  invoked, which is common when using the [sqlalchemy.ext.mutable](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#module-sqlalchemy.ext.mutable)
  extension module.
  See also
  [New “modified” event handler for sqlalchemy.ext.mutable](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3303)
  References: [#3303](https://www.sqlalchemy.org/trac/ticket/3303)
- Fixed issue with subquery eagerloading which continues on from
  the series of issues fixed in [#2699](https://www.sqlalchemy.org/trac/ticket/2699), [#3106](https://www.sqlalchemy.org/trac/ticket/3106),
  [#3893](https://www.sqlalchemy.org/trac/ticket/3893) involving that the “subquery” contains the correct
  FROM clause when beginning from a joined inheritance subclass
  and then subquery eager loading onto a relationship from
  the base class, while the query also includes criteria against
  the subclass. The fix in the previous tickets did not accommodate
  for additional subqueryload operations loading more deeply from
  the first level, so the fix has been further generalized.
  This change is also **backported** to: 1.1.11
  References: [#4011](https://www.sqlalchemy.org/trac/ticket/4011)
- Fixed bug where a cascade such as “delete-orphan” (but others as well)
  would fail to locate an object linked to a relationship that itself
  is local to a subclass in an inheritance relationship, thus causing
  the operation to not take place.
  This change is also **backported** to: 1.1.10
  References: [#3986](https://www.sqlalchemy.org/trac/ticket/3986)
- Fixed a race condition which could occur under threaded environments
  as a result of the caching added via [#3915](https://www.sqlalchemy.org/trac/ticket/3915).   An internal
  collection of `Column` objects could be regenerated on an alias
  object inappropriately, confusing a joined eager loader when it
  attempts to render SQL and collect results and resulting in an
  attribute error.   The collection is now generated up front before
  the alias object is cached and shared among threads.
  This change is also **backported** to: 1.1.7
  References: [#3947](https://www.sqlalchemy.org/trac/ticket/3947)
- An UPDATE emitted as a result of the
  [relationship.post_update](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.post_update) feature will now integrate with
  the versioning feature to both bump the version id of the row as well
  as assert that the existing version number was matched.
  See also
  [post_update integrates with ORM versioning](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3496)
  References: [#3496](https://www.sqlalchemy.org/trac/ticket/3496)
- Repaired several use cases involving the
  [relationship.post_update](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.post_update) feature when used in conjunction
  with a column that has an “onupdate” value.   When the UPDATE emits,
  the corresponding object attribute is now expired or refreshed so that
  the newly generated “onupdate” value can populate on the object;
  previously the stale value would remain.  Additionally, if the target
  attribute is set in Python for the INSERT of the object, the value is
  now re-sent during the UPDATE so that the “onupdate” does not overwrite
  it (note this works just as well for server-generated onupdates).
  Finally, the `SessionEvents.refresh_flush()` event is now emitted
  for these attributes when refreshed within the flush.
  See also
  [Refinements to post_update in conjunction with onupdate](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3471)
  References: [#3471](https://www.sqlalchemy.org/trac/ticket/3471), [#3472](https://www.sqlalchemy.org/trac/ticket/3472)
- Fixed bug where programmatic version_id counter in conjunction with
  joined table inheritance would fail if the version_id counter
  were not actually incremented and no other values on the base table
  were modified, as the UPDATE would have an empty SET clause.  Since
  programmatic version_id where version counter is not incremented
  is a documented use case, this specific condition is now detected
  and the UPDATE now sets the version_id value to itself, so that
  concurrency checks still take place.
  References: [#3996](https://www.sqlalchemy.org/trac/ticket/3996)
- The versioning feature does not support NULL for the version counter.
  An exception is now raised if the version id is programmatic and
  was set to NULL for an UPDATE.  Pull request courtesy Diana Clarke.
  References: [#3673](https://www.sqlalchemy.org/trac/ticket/3673)
- Removed a very old keyword argument from [scoped_session](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoped_session)
  called `scope`.  This keyword was never documented and was an
  early attempt at allowing for variable scopes.
  See also
  [“scope” keyword removed from scoped_session](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3796)
  References: [#3796](https://www.sqlalchemy.org/trac/ticket/3796)
- Fixed bug where combining a “with_polymorphic” load in conjunction
  with subclass-linked relationships that specify joinedload with
  innerjoin=True, would fail to demote those “innerjoins” to
  “outerjoins” to suit the other polymorphic classes that don’t
  support that relationship.   This applies to both a single and a
  joined inheritance polymorphic load.
  References: [#3988](https://www.sqlalchemy.org/trac/ticket/3988)
- Added new argument `with_for_update` to the
  [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) method.  When the `Query.with_lockmode()`
  method were deprecated in favor of [Query.with_for_update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_for_update),
  the [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) method was never updated to reflect
  the new option.
  See also
  [Added “for update” arguments to Session.refresh](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3991)
  References: [#3991](https://www.sqlalchemy.org/trac/ticket/3991)
- Fixed bug where a [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) that is also marked as
  “deferred” would be marked as “expired” during a flush, causing it
  to be loaded along with the unexpiry of regular attributes even
  though this attribute was never accessed.
  References: [#3984](https://www.sqlalchemy.org/trac/ticket/3984)
- Fixed bug in subquery eager loading where the “join_depth” parameter
  for self-referential relationships would not be correctly honored,
  loading all available levels deep rather than correctly counting
  the specified number of levels for eager loading.
  References: [#3967](https://www.sqlalchemy.org/trac/ticket/3967)
- Added warnings to the LRU “compiled cache” used by the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
  (and ultimately will be for other ORM-based LRU caches) such that
  when the cache starts hitting its size limits, the application will
  emit a warning that this is a performance-degrading situation that
  may require attention.   The LRU caches can reach their size limits
  primarily if an application is making use of an unbounded number
  of [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) objects, which is an antipattern.  Otherwise,
  this may suggest an issue that should be brought to the SQLAlchemy
  developer’s attention.
- Fixed bug to improve upon the specificity of loader options that
  take effect subsequent to the lazy load of a related entity, so
  that the loader options will match to an aliased or non-aliased
  entity more specifically if those options include entity information.
  References: [#3963](https://www.sqlalchemy.org/trac/ticket/3963)
- The [flag_modified()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.flag_modified) function now raises
  [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) if the named attribute key is not
  present within the object, as this is assumed to be present
  in the flush process.  To mark an object “dirty” for a flush
  without referring to any specific attribute, the
  [flag_dirty()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.flag_dirty) function may be used.
  See also
  [Use flag_dirty() to mark an object as “dirty” without any attribute changing](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3753)
  References: [#3753](https://www.sqlalchemy.org/trac/ticket/3753)
- The “evaluate” strategy used by [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) and
  [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete) can now accommodate a simple
  object comparison from a many-to-one relationship to an instance,
  when the attribute names of the primary key / foreign key columns
  don’t match the actual names of the columns.  Previously this would
  do a simple name-based match and fail with an AttributeError.
  References: [#3366](https://www.sqlalchemy.org/trac/ticket/3366)
- The `@validates` decorator now allows the decorated method to receive
  objects from a “bulk collection set” operation that have not yet
  been compared to the existing collection.  This allows incoming values
  to be converted to compatible ORM objects as is already allowed
  from an “append” event.   Note that this means that the
  `@validates` method is called for **all** values during a collection
  assignment, rather than just the ones that are new.
  See also
  [A @validates method receives all values on bulk-collection set before comparison](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3896-validates)
  References: [#3896](https://www.sqlalchemy.org/trac/ticket/3896)
- Fixed bug in single-table inheritance where the select_from()
  argument would not be taken into account when limiting rows
  to a subclass.  Previously, only expressions in the
  columns requested would be taken into account.
  See also
  [Fixed issue involving single-table inheritance with select_from()](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3891)
  References: [#3891](https://www.sqlalchemy.org/trac/ticket/3891)
- When assigning a collection to an attribute mapped by a relationship,
  the previous collection is no longer mutated.  Previously, the old
  collection would be emptied out in conjunction with the “item remove”
  events that fire off; the events now fire off without affecting
  the old collection.
  See also
  [Previous collection is no longer mutated upon replacement](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3913)
  References: [#3913](https://www.sqlalchemy.org/trac/ticket/3913)
- The state of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is now present when the
  [SessionEvents.after_rollback()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.after_rollback) event is emitted, that is,  the
  attribute state of objects prior to their being expired.   This is now
  consistent with the  behavior of the
  [SessionEvents.after_commit()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.after_commit) event which  also emits before the
  attribute state of objects is expired.
  See also
  [The after_rollback() Session event now emits before the expiration of objects](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3934)
  References: [#3934](https://www.sqlalchemy.org/trac/ticket/3934)
- Fixed bug where [Query.with_parent()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_parent) would not work if the
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) were against an [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct rather than
  a regular mapped class.  Also adds a new parameter
  `with_parent.from_entity` to the standalone
  `with_parent()` function as well as
  [Query.with_parent()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_parent).
  References: [#3607](https://www.sqlalchemy.org/trac/ticket/3607)

### orm declarative

- Fixed bug where using [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) on an
  [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) where a particular return value were some
  non-mapped symbol, including `None`, would cause the attribute
  to hard-evaluate just once and store the value to the object
  dictionary, not allowing it to invoke for subclasses.   This behavior
  is normal when [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) is on a mapped class, and
  does not occur on a mixin or abstract class.  Since
  [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) is both “abstract” and actually
  “mapped”, a special exception case is made here so that the
  “abstract” behavior takes precedence for [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr).
  References: [#3848](https://www.sqlalchemy.org/trac/ticket/3848)

### engine

- Added native “pessimistic disconnection” handling to the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
  object.  The new parameter [Pool.pre_ping](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool.params.pre_ping), available from
  the engine as [create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping), applies an
  efficient form of the “pre-ping” recipe featured in the pooling
  documentation, which upon each connection check out, emits a simple
  statement, typically “SELECT 1”, to test the connection for liveness.
  If the existing connection is no longer able to respond to commands,
  the connection is transparently recycled, and all other connections
  made prior to the current timestamp are invalidated.
  See also
  [Disconnect Handling - Pessimistic](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects-pessimistic)
  [Pessimistic disconnection detection added to the connection pool](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3919)
  References: [#3919](https://www.sqlalchemy.org/trac/ticket/3919)
- Added an exception handler that will warn for the “cause” exception on
  Py2K when the “autorollback” feature of [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) itself
  raises an exception. In Py3K, the two exceptions are naturally reported
  by the interpreter as one occurring during the handling of the other.
  This is continuing with the series of changes for rollback failure
  handling that were last visited as part of [#2696](https://www.sqlalchemy.org/trac/ticket/2696) in 1.0.12.
  This change is also **backported** to: 1.1.7
  References: [#3946](https://www.sqlalchemy.org/trac/ticket/3946)
- Fixed bug where in the unusual case of passing a
  [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object directly to [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute),
  the dialect with which the [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object were generated
  was not consulted for the paramstyle of the string statement, instead
  assuming it would match the dialect-level paramstyle, causing
  mismatches to occur.
  References: [#3938](https://www.sqlalchemy.org/trac/ticket/3938)

### sql

- Added a new kind of [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) called “expanding”.  This is
  for use in `IN` expressions where the list of elements is rendered
  into individual bound parameters at statement execution time, rather
  than at statement compilation time.  This allows both a single bound
  parameter name to be linked to an IN expression of multiple elements,
  as well as allows query caching to be used with IN expressions.  The
  new feature allows the related features of “select in” loading and
  “polymorphic in” loading to make use of the baked query extension
  to reduce call overhead.   This feature should be considered to be
  **experimental** for 1.2.
  See also
  [Late-expanded IN parameter sets allow IN expressions with cached statements](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3953)
  References: [#3953](https://www.sqlalchemy.org/trac/ticket/3953)
- Added support for SQL comments on [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  objects, via the new [Table.comment](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.comment) and
  [Column.comment](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.comment) arguments.   The comments are included
  as part of DDL on table creation, either inline or via an appropriate
  ALTER statement, and are also reflected back within table reflection,
  as well as via the [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector).   Supported backends currently
  include MySQL, PostgreSQL, and Oracle.  Many thanks to Frazer McLean
  for a large amount of effort on this.
  See also
  [Support for SQL Comments on Table, Column, includes DDL, reflection](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-1546)
  References: [#1546](https://www.sqlalchemy.org/trac/ticket/1546)
- The longstanding behavior of the [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) and
  [ColumnOperators.notin_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notin_) operators emitting a warning when
  the right-hand condition is an empty sequence has been revised;
  a simple “static” expression of “1 != 1” or “1 = 1” is now rendered
  by default, rather than pulling in the original left-hand
  expression.  This causes the result for a NULL column comparison
  against an empty set to change from NULL to true/false.  The
  behavior is configurable, and the old behavior can be enabled
  using the [create_engine.empty_in_strategy](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.empty_in_strategy) parameter
  to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).
  See also
  [The IN / NOT IN operator’s empty collection behavior is now configurable; default expression simplified](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3907)
  References: [#3907](https://www.sqlalchemy.org/trac/ticket/3907)
- Added a new option `autoescape` to the “startswith” and
  “endswith” classes of comparators; this supplies an escape character
  also applies it to all occurrences of the wildcard characters “%”
  and “_” automatically.  Pull request courtesy Diana Clarke.
  Note
  This feature has been changed as of 1.2.0 from its initial
  implementation in 1.2.0b2 such that autoescape is now passed as a
  boolean value, rather than a specific character to use as the escape
  character.
  See also
  [New “autoescape” option for startswith(), endswith()](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-2694)
  References: [#2694](https://www.sqlalchemy.org/trac/ticket/2694)
- Fixed AttributeError which would occur in [WithinGroup](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.WithinGroup)
  construct during an iteration of the structure.
  This change is also **backported** to: 1.1.11
  References: [#4012](https://www.sqlalchemy.org/trac/ticket/4012)
- Fixed regression released in 1.1.5 due to [#3859](https://www.sqlalchemy.org/trac/ticket/3859) where
  adjustments to the “right-hand-side” evaluation of an expression
  based on [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant) to honor the underlying type’s
  “right-hand-side” rules caused the [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant) type
  to be inappropriately lost, in those cases when we *do* want the
  left-hand side type to be transferred directly to the right hand side
  so that bind-level rules can be applied to the expression’s argument.
  This change is also **backported** to: 1.1.9
  References: [#3952](https://www.sqlalchemy.org/trac/ticket/3952)
- Changed the mechanics of `ResultProxy` to unconditionally
  delay the “autoclose” step until the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is done
  with the object; in the case where PostgreSQL ON CONFLICT with
  RETURNING returns no rows, autoclose was occurring in this previously
  non-existent use case, causing the usual autocommit behavior that
  occurs unconditionally upon INSERT/UPDATE/DELETE to fail.
  This change is also **backported** to: 1.1.9
  References: [#3955](https://www.sqlalchemy.org/trac/ticket/3955)
- The rules for type coercion between [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric), [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer),
  and date-related types now include additional logic that will attempt
  to preserve the settings of the incoming type on the “resolved” type.
  Currently the target for this is the `asdecimal` flag, so that
  a math operation between [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric) or [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) and
  [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) will preserve the “asdecimal” flag as well as
  if the type should be the [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) subclass.
  See also
  [Stronger typing added to “float” datatypes](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-floats-12)
  References: [#4018](https://www.sqlalchemy.org/trac/ticket/4018)
- The result processor for the [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) type now unconditionally
  runs values through the `float()` processor if the dialect
  specifies that it also supports “native decimal” mode.  While most
  backends will deliver Python `float` objects for a floating point
  datatype, the MySQL backends in some cases lack the typing information
  in order to provide this and return `Decimal` unless the float
  conversion is done.
  See also
  [Stronger typing added to “float” datatypes](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-floats-12)
  References: [#4020](https://www.sqlalchemy.org/trac/ticket/4020)
- Added some extra strictness to the handling of Python “float” values
  passed to SQL statements.  A “float” value will be associated with the
  [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) datatype and not the Decimal-coercing [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric)
  datatype as was the case before, eliminating a confusing warning
  emitted on SQLite as well as unnecessary coercion to Decimal.
  See also
  [Stronger typing added to “float” datatypes](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-floats-12)
  References: [#4017](https://www.sqlalchemy.org/trac/ticket/4017)
- The operator precedence for all comparison operators such as LIKE, IS,
  IN, MATCH, equals, greater than, less than, etc. has all been merged
  into one level, so that expressions which make use of these against
  each other will produce parentheses between them.   This suits the
  stated operator precedence of databases like Oracle, MySQL and others
  which place all of these operators as equal precedence, as well as
  PostgreSQL as of 9.5 which has also flattened its operator precedence.
  See also
  [Flattened operator precedence for comparison operators](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3999)
  References: [#3999](https://www.sqlalchemy.org/trac/ticket/3999)
- Repaired issue where the type of an expression that used
  [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_) or similar would not be a “boolean” type,
  instead the type would be “nulltype”, as well as when using custom
  comparison operators against an untyped expression.   This typing can
  impact how the expression behaves in larger contexts as well as
  in result-row-handling.
  References: [#3873](https://www.sqlalchemy.org/trac/ticket/3873)
- Fixed the negation of a [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label) construct so that the
  inner element is negated correctly, when the [not_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.not_) modifier
  is applied to the labeled expression.
  References: [#3969](https://www.sqlalchemy.org/trac/ticket/3969)
- The system by which percent signs in SQL statements are “doubled”
  for escaping purposes has been refined.   The “doubling” of percent
  signs mostly associated with the [literal_column](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column) construct
  as well as operators like [ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains) now
  occurs based on the stated paramstyle of the DBAPI in use; for
  percent-sensitive paramstyles as are common with the PostgreSQL
  and MySQL drivers the doubling will occur, for others like that
  of SQLite it will not.   This allows more database-agnostic use
  of the [literal_column](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column) construct to be possible.
  See also
  [Percent signs in literal_column() now conditionally escaped](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3740)
  References: [#3740](https://www.sqlalchemy.org/trac/ticket/3740)
- Fixed bug where a column-level [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) would fail
  to compile the SQL expression using the underlying dialect compiler
  as well as apply proper flags to generate literal values as
  inline, in the case that the sqltext is a Core expression and
  not just a plain string.   This was long-ago fixed for table-level
  check constraints in 0.9 as part of [#2742](https://www.sqlalchemy.org/trac/ticket/2742), which more commonly
  feature Core SQL expressions as opposed to plain string expressions.
  References: [#3957](https://www.sqlalchemy.org/trac/ticket/3957)
- Fixed bug where a SQL-oriented Python-side column default could fail to
  be executed properly upon INSERT in the “pre-execute” codepath, if the
  SQL itself were an untyped expression, such as plain text.  The “pre-
  execute” codepath is fairly uncommon however can apply to non-integer
  primary key columns with SQL defaults when RETURNING is not used.
  References: [#3923](https://www.sqlalchemy.org/trac/ticket/3923)
- The expression used for COLLATE as rendered by the column-level
  [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate) and [ColumnOperators.collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.collate) is now
  quoted as an identifier when the name is case sensitive, e.g. has
  uppercase characters.  Note that this does not impact type-level
  collation, which is already quoted.
  See also
  [The column-level COLLATE keyword now quotes the collation name](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3785)
  References: [#3785](https://www.sqlalchemy.org/trac/ticket/3785)
- Fixed bug where the use of an [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) object in a column
  context would raise an argument error when it tried to group itself
  into a parenthesized expression.   Using [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) in this way
  is not yet a fully supported API, however it applies to some end-user
  recipes and may have a more prominent role in support of some
  future PostgreSQL features.
  References: [#3939](https://www.sqlalchemy.org/trac/ticket/3939)

### schema

- An [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is now raised if a
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object is created with a mismatched
  number of “local” and “remote” columns, which otherwise causes the
  internal state of the constraint to be incorrect.   Note that this
  also impacts the condition where a dialect’s reflection process
  produces a mismatched set of columns for a foreign key constraint.
  This change is also **backported** to: 1.1.10
  References: [#3949](https://www.sqlalchemy.org/trac/ticket/3949)

### postgresql

- Continuing with the fix that correctly handles PostgreSQL
  version string “10devel” released in 1.1.8, an additional regexp
  bump to handle version strings of the form “10beta1”.   While
  PostgreSQL now offers better ways to get this information, we
  are sticking w/ the regexp at least through 1.1.x for the least
  amount of risk to compatibility w/ older or alternate PostgreSQL
  databases.
  This change is also **backported** to: 1.1.11
  References: [#4005](https://www.sqlalchemy.org/trac/ticket/4005)
- Fixed bug where using [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) with a string type that
  features a collation would fail to produce the correct syntax
  within CREATE TABLE.
  This change is also **backported** to: 1.1.11
  References: [#4006](https://www.sqlalchemy.org/trac/ticket/4006)
- Added “autocommit” support for GRANT, REVOKE keywords.  Pull request
  courtesy Jacob Hayes.
  This change is also **backported** to: 1.1.10
- Added support for parsing the PostgreSQL version string for
  a development version like “PostgreSQL 10devel”.  Pull request
  courtesy Sean McCully.
  This change is also **backported** to: 1.1.8
- Fixed bug where the base [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) datatype would not
  invoke the bind/result processors of [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY).
  References: [#3964](https://www.sqlalchemy.org/trac/ticket/3964)
- Added support for all possible “fields” identifiers when reflecting the
  PostgreSQL `INTERVAL` datatype, e.g. “YEAR”, “MONTH”, “DAY TO
  MINUTE”, etc..   In addition, the [INTERVAL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.INTERVAL)
  datatype itself now includes a new parameter
  [INTERVAL.fields](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.INTERVAL.params.fields) where these qualifiers can be
  specified; the qualifier is also reflected back into the resulting
  datatype upon reflection / inspection.
  See also
  [Support for fields specification in INTERVAL, including full reflection](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3959)
  References: [#3959](https://www.sqlalchemy.org/trac/ticket/3959)

### mysql

- Added support for MySQL’s ON DUPLICATE KEY UPDATE
  MySQL-specific [Insert](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.Insert) object.
  Pull request courtesy Michael Doronin.
  See also
  [Support for INSERT..ON DUPLICATE KEY UPDATE](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-4009)
  References: [#4009](https://www.sqlalchemy.org/trac/ticket/4009)
- MySQL 5.7 has introduced permission limiting for the “SHOW VARIABLES”
  command; the MySQL dialect will now handle when SHOW returns no
  row, in particular for the initial fetch of SQL_MODE, and will
  emit a warning that user permissions should be modified to allow the
  row to be present.
  This change is also **backported** to: 1.1.11
  References: [#4007](https://www.sqlalchemy.org/trac/ticket/4007)
- Removed an ancient and unnecessary intercept of the UTC_TIMESTAMP
  MySQL function, which was getting in the way of using it with a
  parameter.
  This change is also **backported** to: 1.1.10
  References: [#3966](https://www.sqlalchemy.org/trac/ticket/3966)
- Fixed bug in MySQL dialect regarding rendering of table options in
  conjunction with PARTITION options when rendering CREATE TABLE.
  The PARTITION related options need to follow the table options,
  whereas previously this ordering was not enforced.
  This change is also **backported** to: 1.1.10
  References: [#3961](https://www.sqlalchemy.org/trac/ticket/3961)
- Added support for views that are unreflectable due to stale
  table definitions, when calling [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect); a warning
  is emitted for the table that cannot respond to `DESCRIBE`,
  but the operation succeeds.
  References: [#3871](https://www.sqlalchemy.org/trac/ticket/3871)

### mssql

- Fixed bug where SQL Server transaction isolation must be fetched
  from a different view when using Azure data warehouse, the query
  is now attempted against both views and then a NotImplemented
  is raised unconditionally if failure continues to provide the
  best resiliency against future arbitrary API changes in new
  SQL Server versions.
  This change is also **backported** to: 1.1.11
  References: [#3994](https://www.sqlalchemy.org/trac/ticket/3994)
- Added a placeholder type [XML](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.XML) to the SQL Server
  dialect, so that a reflected table which includes this type can
  be re-rendered as a CREATE TABLE.  The type has no special round-trip
  behavior nor does it currently support additional qualifying
  arguments.
  This change is also **backported** to: 1.1.11
  References: [#3973](https://www.sqlalchemy.org/trac/ticket/3973)
- The SQL Server dialect now allows for a database and/or owner name
  with a dot inside of it, using brackets explicitly in the string around
  the owner and optionally the database name as well.  In addition,
  sending the [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) construct for the schema name will
  not split on the dot and will deliver the full string as the “owner”.
  [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) is also now available from the `sqlalchemy.sql`
  import space.
  See also
  [SQL Server schema names with embedded dots supported](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-2626)
  References: [#2626](https://www.sqlalchemy.org/trac/ticket/2626)

### oracle

- Added new keywords [Sequence.cache](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.cache) and
  [Sequence.order](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.order) to [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), to allow rendering
  of the CACHE parameter understood by Oracle and PostgreSQL, and the
  ORDER parameter understood by Oracle.  Pull request
  courtesy David Moore.
  This change is also **backported** to: 1.1.12
- The Oracle dialect now inspects unique and check constraints when using
  [Inspector.get_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints),
  [Inspector.get_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints).
  As Oracle does not have unique constraints that are separate from a unique
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that’s reflected will still continue
  to not have [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) objects associated with it.
  Pull requests courtesy Eloy Felix.
  See also
  [Oracle Unique, Check constraints now reflected](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-4003)
  References: [#4003](https://www.sqlalchemy.org/trac/ticket/4003)
- Support for two-phase transactions has been removed entirely for
  cx_Oracle when version 6.0b1 or later of the DBAPI is in use.  The two-
  phase feature historically has never been usable under cx_Oracle 5.x in
  any case, and cx_Oracle 6.x has removed the connection-level “twophase”
  flag upon which this feature relied.
  This change is also **backported** to: 1.1.11
  References: [#3997](https://www.sqlalchemy.org/trac/ticket/3997)
- Fixed bug in cx_Oracle dialect where version string parsing would
  fail for cx_Oracle version 6.0b1 due to the “b” character.  Version
  string parsing is now via a regexp rather than a simple split.
  This change is also **backported** to: 1.1.10
  References: [#3975](https://www.sqlalchemy.org/trac/ticket/3975)
- The cx_Oracle dialect now supports “sane multi rowcount”, that is,
  when a series of parameter sets are executed via DBAPI
  `cursor.executemany()`, we can make use of `cursor.rowcount` to
  verify the number of rows matched.  This has an impact within the
  ORM when detecting concurrent modification scenarios, in that
  some simple conditions can now be detected even when the ORM
  is batching statements, as well as when the more strict versioning
  feature is used, the ORM can still use statement batching.  The
  flag is enabled for cx_Oracle assuming at least version 5.0, which
  is now commonplace.
  References: [#3932](https://www.sqlalchemy.org/trac/ticket/3932)
- Oracle reflection now “normalizes” the name given to a foreign key
  constraint, that is, returns it as all lower case for a case
  insensitive name.  This was already the behavior for indexes
  and primary key constraints as well as all table and column names.
  This will allow Alembic autogenerate scripts to compare and render
  foreign key constraint names correctly when initially specified
  as case insensitive.
  See also
  [Oracle foreign key constraint names are now “name normalized”](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3276)
  References: [#3276](https://www.sqlalchemy.org/trac/ticket/3276)

### misc

- Added new flag [Session.enable_baked_queries](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.enable_baked_queries) to the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to allow baked queries to be disabled
  session-wide, reducing memory use.   Also added new [Bakery](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.Bakery)
  wrapper so that the bakery returned by [BakedQuery.bakery](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery.params.bakery)
  can be inspected.
- Protected against testing “None” as a class in the case where
  declarative classes are being garbage collected and new
  automap prepare() operations are taking place concurrently, very
  infrequently hitting a weakref that has not been fully acted upon
  after gc.
  This change is also **backported** to: 1.1.10
  References: [#3980](https://www.sqlalchemy.org/trac/ticket/3980)
- Fixed bug in [sqlalchemy.ext.mutable](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#module-sqlalchemy.ext.mutable) where the
  [Mutable.as_mutable()](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.Mutable.as_mutable) method would not track a type that had
  been copied using `TypeEngine.copy()`.  This became more of
  a regression in 1.1 compared to 1.0 because the [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
  class is now a subclass of [SchemaEventTarget](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.SchemaEventTarget), which among
  other things indicates to the parent [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that the type
  should be copied when the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is.  These copies are
  common when using declarative with mixins or abstract classes.
  This change is also **backported** to: 1.1.8
  References: [#3950](https://www.sqlalchemy.org/trac/ticket/3950)
- Added support for bound parameters, e.g. those normally set up
  via [Query.params()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.params), to the `Result.count()`
  method.  Previously, support for parameters were omitted. Pull request
  courtesy Pat Deegan.
  This change is also **backported** to: 1.1.8
- The `AssociationProxy.any()`, `AssociationProxy.has()`
  and `AssociationProxy.contains()` comparison methods now support
  linkage to an attribute that is itself also an
  [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy), recursively.
  See also
  [AssociationProxy any(), has(), contains() work with chained association proxies](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3769)
  References: [#3769](https://www.sqlalchemy.org/trac/ticket/3769)
- Implemented in-place mutation operators `__ior__`, `__iand__`,
  `__ixor__` and `__isub__` for [MutableSet](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableSet)
  and `__iadd__` for [MutableList](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList) so that change
  events are fired off when these mutator methods are used to alter the
  collection.
  See also
  [In-place mutation operators work for MutableSet, MutableList](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3853)
  References: [#3853](https://www.sqlalchemy.org/trac/ticket/3853)
- A warning is emitted if the [declared_attr.cascading](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr.cascading) modifier
  is used with a declarative attribute that is itself declared on
  a class that is to be mapped, as opposed to a declarative mixin
  class or `__abstract__` class.  The [declared_attr.cascading](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr.cascading)
  modifier currently only applies to mixin/abstract classes.
  References: [#3847](https://www.sqlalchemy.org/trac/ticket/3847)
- Improved the association proxy list collection so that premature
  autoflush against a newly created association object can be prevented
  in the case where `list.append()` is being used, and a lazy load
  would be invoked when the association proxy accesses the endpoint
  collection.  The endpoint collection is now accessed first before
  the creator is invoked to produce the association object.
  References: [#3941](https://www.sqlalchemy.org/trac/ticket/3941)
- The [sqlalchemy.ext.hybrid.hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property) class now supports
  calling mutators like `@setter`, `@expression` etc. multiple times
  across subclasses, and now provides a `@getter` mutator, so that
  a particular hybrid can be repurposed across subclasses or other
  classes.  This now matches the behavior of `@property` in standard
  Python.
  See also
  [Hybrid attributes support reuse among subclasses, redefinition of @getter](https://docs.sqlalchemy.org/en/20/changelog/migration_12.html#change-3911-3912)
  References: [#3911](https://www.sqlalchemy.org/trac/ticket/3911), [#3912](https://www.sqlalchemy.org/trac/ticket/3912)
- Fixed a bug in the `sqlalchemy.ext.serializer` extension whereby
  an “annotated” SQL element (as produced by the ORM for many types
  of SQL expressions) could not be reliably serialized.  Also bumped
  the default pickle level for the serializer to “HIGHEST_PROTOCOL”.
  References: [#3918](https://www.sqlalchemy.org/trac/ticket/3918)
