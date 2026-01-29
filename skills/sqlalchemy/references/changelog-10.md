# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# 1.1 Changelog

## 1.1.18

Released: March 6, 2018

### postgresql

- Fixed bug in PostgreSQL COLLATE / ARRAY adjustment first introduced
  in [#4006](https://www.sqlalchemy.org/trac/ticket/4006) where new behaviors in Python 3.7 regular expressions
  caused the fix to fail.
  References: [#4208](https://www.sqlalchemy.org/trac/ticket/4208)

### mysql

- MySQL dialects now query the server version using `SELECT @@version`
  explicitly to the server to ensure we are getting the correct version
  information back.   Proxy servers like MaxScale interfere with the value
  that is passed to the DBAPI’s connection.server_version value so this
  is no longer reliable.
  References: [#4205](https://www.sqlalchemy.org/trac/ticket/4205)

## 1.1.17

Released: February 22, 2018

- Repaired regression caused in 1.2.3 and 1.1.16 regarding association proxy
  objects, revising the approach to [#4185](https://www.sqlalchemy.org/trac/ticket/4185) when calculating the
  “owning class” of an association proxy to default to choosing the current
  class if the proxy object is not directly associated with a mapped class,
  such as a mixin.
  References: [#4185](https://www.sqlalchemy.org/trac/ticket/4185)

## 1.1.16

Released: February 16, 2018

### orm

- Fixed issue in post_update feature where an UPDATE is emitted
  when the parent object has been deleted but the dependent object
  is not.   This issue has existed for a long time however
  since 1.2 now asserts rows matched for post_update, this
  was raising an error.
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
  References: [#4185](https://www.sqlalchemy.org/trac/ticket/4185)
- Fixed bug where an object that is expunged during a rollback of
  a nested or subtransaction which also had its primary key mutated
  would not be correctly removed from the session, causing subsequent
  issues in using the session.
  References: [#4151](https://www.sqlalchemy.org/trac/ticket/4151)

### sql

- Added [nullsfirst()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nullsfirst) and [nullslast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nullslast) as top level imports
  in the `sqlalchemy.` and `sqlalchemy.sql.` namespace.  Pull request
  courtesy Lele Gaifax.
- Fixed bug in [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) where using the “multi-values”
  format in combination with [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects as keys rather
  than strings would fail.   Pull request courtesy Aubrey Stark-Toller.
  References: [#4162](https://www.sqlalchemy.org/trac/ticket/4162)

### postgresql

- Added “SSL SYSCALL error: Operation timed out” to the list
  of messages that trigger a “disconnect” scenario for the
  psycopg2 driver.  Pull request courtesy André Cruz.
- Added “TRUNCATE” to the list of keywords accepted by the
  PostgreSQL dialect as an “autocommit”-triggering keyword.
  Pull request courtesy Jacob Hayes.

### mysql

- Fixed bug where the MySQL “concat” and “match” operators failed to
  propagate kwargs to the left and right expressions, causing compiler
  options such as “literal_binds” to fail.
  References: [#4136](https://www.sqlalchemy.org/trac/ticket/4136)

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
  References: [#4184](https://www.sqlalchemy.org/trac/ticket/4184)

## 1.1.15

Released: November 3, 2017

### orm

- Fixed bug where the association proxy would inadvertently link itself
  to an [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) object if it were called first with
  the [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) as a parent, causing errors upon subsequent
  usage.
  References: [#4116](https://www.sqlalchemy.org/trac/ticket/4116)
- Fixed bug where ORM relationship would warn against conflicting sync
  targets (e.g. two relationships would both write to the same column) for
  sibling classes in an inheritance hierarchy, where the two relationships
  would never actually conflict during writes.
  References: [#4078](https://www.sqlalchemy.org/trac/ticket/4078)
- Fixed bug where correlated select used against single-table inheritance
  entity would fail to render correctly in the outer query, due to adjustment
  for single inheritance discriminator criteria inappropriately re-applying
  the criteria to the outer query.
  References: [#4103](https://www.sqlalchemy.org/trac/ticket/4103)

### orm declarative

- Fixed a bug where a descriptor, which is a mapped column or a
  relationship elsewhere in a hierarchy based on
  [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase), would be referenced during a refresh
  operation, leading to an error since the attribute is not mapped as a
  mapper property. A similar issue can arise for other attributes
  like the “type” column added by [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) if the
  class fails to include “concrete=True” in its mapper, however the check
  here should also prevent that scenario from causing a problem.
  References: [#4124](https://www.sqlalchemy.org/trac/ticket/4124)

### sql

- Fixed bug where `__repr__` of [ColumnDefault](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.ColumnDefault) would fail
  if the argument were a tuple.  Pull request courtesy Nicolas Caniart.
  References: [#4126](https://www.sqlalchemy.org/trac/ticket/4126)
- Fixed bug where the recently added [ColumnOperators.any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.any_)
  and [ColumnOperators.all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.all_) methods didn’t work when called
  as methods, as opposed to using the standalone functions
  [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) and [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_).  Also
  added documentation examples for these relatively unintuitive
  SQL operators.
  References: [#4093](https://www.sqlalchemy.org/trac/ticket/4093)

### postgresql

- Made further fixes to the [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) class in conjunction with
  COLLATE, as the fix made in [#4006](https://www.sqlalchemy.org/trac/ticket/4006) failed to accommodate
  for a multidimensional array.
  References: [#4006](https://www.sqlalchemy.org/trac/ticket/4006)
- Fixed bug in [array_agg](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg) function where passing an argument
  that is already of type [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), such as a PostgreSQL
  [array](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array) construct, would produce a `ValueError`, due
  to the function attempting to nest the arrays.
  References: [#4107](https://www.sqlalchemy.org/trac/ticket/4107)
- Fixed bug in PostgreSQL `Insert.on_conflict_do_update()`
  which would prevent the insert statement from being used as a CTE,
  e.g. via `Insert.cte()`, within another statement.
  References: [#4074](https://www.sqlalchemy.org/trac/ticket/4074)

### mysql

- Warning emitted when MariaDB 10.2.8 or earlier in the 10.2
  series is detected as there are major issues with CHECK
  constraints within these versions that were resolved as of
  10.2.9.
  Note that this changelog message was NOT released with
  SQLAlchemy 1.2.0b3 and was added retroactively.
  References: [#4097](https://www.sqlalchemy.org/trac/ticket/4097)
- MySQL 5.7.20 now warns for use of the @tx_isolation variable; a version
  check is now performed and uses @transaction_isolation instead
  to prevent this warning.
  References: [#4120](https://www.sqlalchemy.org/trac/ticket/4120)
- Fixed issue where CURRENT_TIMESTAMP would not reflect correctly
  in the MariaDB 10.2 series due to a syntax change, where the function
  is now represented as `current_timestamp()`.
  References: [#4096](https://www.sqlalchemy.org/trac/ticket/4096)
- MariaDB 10.2 now supports CHECK constraints (warning: use version 10.2.9
  or greater due to upstream issues noted in [#4097](https://www.sqlalchemy.org/trac/ticket/4097)).  Reflection
  now takes these CHECK constraints into account when they are present in
  the `SHOW CREATE TABLE` output.
  References: [#4098](https://www.sqlalchemy.org/trac/ticket/4098)

### sqlite

- Fixed bug where SQLite CHECK constraint reflection would fail
  if the referenced table were in a remote schema, e.g. on SQLite a
  remote database referred to by ATTACH.
  References: [#4099](https://www.sqlalchemy.org/trac/ticket/4099)

### mssql

- Added a full range of “connection closed” exception codes to the
  PyODBC dialect for SQL Server, including ‘08S01’, ‘01002’, ‘08003’,
  ‘08007’, ‘08S02’, ‘08001’, ‘HYT00’, ‘HY010’.  Previously, only ‘08S01’
  was covered.
  References: [#4095](https://www.sqlalchemy.org/trac/ticket/4095)

## 1.1.14

Released: September 5, 2017

### orm

- Fixed bug in [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) following along similar lines as that
  of [#4030](https://www.sqlalchemy.org/trac/ticket/4030), where an internal check for a target object in
  the identity map could lead to an error if it were to be garbage collected
  immediately before the merge routine actually retrieves the object.
  References: [#4069](https://www.sqlalchemy.org/trac/ticket/4069)
- Fixed bug where an [undefer_group()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer_group) option would not be recognized
  if it extended from a relationship that was loading using joined eager
  loading.  Additionally, as the bug led to excess work being performed,
  Python function call counts are also improved by 20% within the initial
  calculation of result set columns, complementing the joined eager load
  improvements of [#3915](https://www.sqlalchemy.org/trac/ticket/3915).
  References: [#4048](https://www.sqlalchemy.org/trac/ticket/4048)
- Fixed race condition in ORM identity map which would cause objects
  to be inappropriately removed during a load operation, causing
  duplicate object identities to occur, particularly under joined eager
  loading which involves deduplication of objects.  The issue is specific
  to garbage collection of weak references and is observed only under the
  PyPy interpreter.
  References: [#4068](https://www.sqlalchemy.org/trac/ticket/4068)
- Fixed bug in [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) where objects in a collection that had
  the primary key attribute set to `None` for a key that is  typically
  autoincrementing would be considered to be a database-persisted key for
  part of the internal deduplication process, causing only one object to
  actually be inserted in the database.
  References: [#4056](https://www.sqlalchemy.org/trac/ticket/4056)
- An [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) is raised when a [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym)
  is used against an attribute that is not against a [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty),
  such as an association proxy.  Previously, a recursion overflow would
  occur trying to locate non-existent attributes.
  References: [#4067](https://www.sqlalchemy.org/trac/ticket/4067)

### sql

- Altered the range specification for window functions to allow
  for two of the same PRECEDING or FOLLOWING keywords in a range
  by allowing for the left side of the range to be positive
  and for the right to be negative, e.g. (1, 3) is
  “1 FOLLOWING AND 3 FOLLOWING”.
  References: [#4053](https://www.sqlalchemy.org/trac/ticket/4053)

## 1.1.13

Released: August 3, 2017

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
  This change is also **backported** to: 1.0.19
  References: [#4035](https://www.sqlalchemy.org/trac/ticket/4035)

## 1.1.12

Released: July 24, 2017

### orm

- Fixed regression from 1.1.11 where adding additional non-entity
  columns to a query that includes an entity with subqueryload
  relationships would fail, due to an inspection added in 1.1.11 as a
  result of [#4011](https://www.sqlalchemy.org/trac/ticket/4011).
  References: [#4033](https://www.sqlalchemy.org/trac/ticket/4033)
- Fixed bug involving JSON NULL evaluation logic added in 1.1 as part
  of [#3514](https://www.sqlalchemy.org/trac/ticket/3514) where the logic would not accommodate ORM
  mapped attributes named differently from the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  that was mapped.
  References: [#4031](https://www.sqlalchemy.org/trac/ticket/4031)
- Added `KeyError` checks to all methods within
  `WeakInstanceDict` where a check for `key in dict` is
  followed by indexed access to that key, to guard against a race against
  garbage collection that under load can remove the key from the dict
  after the code assumes its present, leading to very infrequent
  `KeyError` raises.
  References: [#4030](https://www.sqlalchemy.org/trac/ticket/4030)

### oracle

- Added new keywords [Sequence.cache](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.cache) and
  [Sequence.order](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.order) to [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), to allow rendering
  of the CACHE parameter understood by Oracle and PostgreSQL, and the
  ORDER parameter understood by Oracle.  Pull request
  courtesy David Moore.

### tests

- Fixed issue in testing fixtures which was incompatible with a change
  made as of Python 3.6.2 involving context managers.
  This change is also **backported** to: 1.0.18
  References: [#4034](https://www.sqlalchemy.org/trac/ticket/4034)

## 1.1.11

Released: Monday, June 19, 2017

### orm

- Fixed issue with subquery eagerloading which continues on from
  the series of issues fixed in [#2699](https://www.sqlalchemy.org/trac/ticket/2699), [#3106](https://www.sqlalchemy.org/trac/ticket/3106),
  [#3893](https://www.sqlalchemy.org/trac/ticket/3893) involving that the “subquery” contains the correct
  FROM clause when beginning from a joined inheritance subclass
  and then subquery eager loading onto a relationship from
  the base class, while the query also includes criteria against
  the subclass. The fix in the previous tickets did not accommodate
  for additional subqueryload operations loading more deeply from
  the first level, so the fix has been further generalized.
  References: [#4011](https://www.sqlalchemy.org/trac/ticket/4011)

### sql

- Fixed AttributeError which would occur in [WithinGroup](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.WithinGroup)
  construct during an iteration of the structure.
  References: [#4012](https://www.sqlalchemy.org/trac/ticket/4012)

### postgresql

- Continuing with the fix that correctly handles PostgreSQL
  version string “10devel” released in 1.1.8, an additional regexp
  bump to handle version strings of the form “10beta1”.   While
  PostgreSQL now offers better ways to get this information, we
  are sticking w/ the regexp at least through 1.1.x for the least
  amount of risk to compatibility w/ older or alternate PostgreSQL
  databases.
  References: [#4005](https://www.sqlalchemy.org/trac/ticket/4005)
- Fixed bug where using [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) with a string type that
  features a collation would fail to produce the correct syntax
  within CREATE TABLE.
  References: [#4006](https://www.sqlalchemy.org/trac/ticket/4006)

### mysql

- MySQL 5.7 has introduced permission limiting for the “SHOW VARIABLES”
  command; the MySQL dialect will now handle when SHOW returns no
  row, in particular for the initial fetch of SQL_MODE, and will
  emit a warning that user permissions should be modified to allow the
  row to be present.
  References: [#4007](https://www.sqlalchemy.org/trac/ticket/4007)

### mssql

- Fixed bug where SQL Server transaction isolation must be fetched
  from a different view when using Azure data warehouse, the query
  is now attempted against both views and then a NotImplemented
  is raised unconditionally if failure continues to provide the
  best resiliency against future arbitrary API changes in new
  SQL Server versions.
  References: [#3994](https://www.sqlalchemy.org/trac/ticket/3994)
- Added a placeholder type [XML](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.XML) to the SQL Server
  dialect, so that a reflected table which includes this type can
  be re-rendered as a CREATE TABLE.  The type has no special round-trip
  behavior nor does it currently support additional qualifying
  arguments.
  References: [#3973](https://www.sqlalchemy.org/trac/ticket/3973)

### oracle

- Support for two-phase transactions has been removed entirely for
  cx_Oracle when version 6.0b1 or later of the DBAPI is in use.  The two-
  phase feature historically has never been usable under cx_Oracle 5.x in
  any case, and cx_Oracle 6.x has removed the connection-level “twophase”
  flag upon which this feature relied.
  References: [#3997](https://www.sqlalchemy.org/trac/ticket/3997)

## 1.1.10

Released: Friday, May 19, 2017

### orm

- Fixed bug where a cascade such as “delete-orphan” (but others as well)
  would fail to locate an object linked to a relationship that itself
  is local to a subclass in an inheritance relationship, thus causing
  the operation to not take place.
  References: [#3986](https://www.sqlalchemy.org/trac/ticket/3986)

### schema

- An [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is now raised if a
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object is created with a mismatched
  number of “local” and “remote” columns, which otherwise causes the
  internal state of the constraint to be incorrect.   Note that this
  also impacts the condition where a dialect’s reflection process
  produces a mismatched set of columns for a foreign key constraint.
  References: [#3949](https://www.sqlalchemy.org/trac/ticket/3949)

### postgresql

- Added “autocommit” support for GRANT, REVOKE keywords.  Pull request
  courtesy Jacob Hayes.

### mysql

- Removed an ancient and unnecessary intercept of the UTC_TIMESTAMP
  MySQL function, which was getting in the way of using it with a
  parameter.
  References: [#3966](https://www.sqlalchemy.org/trac/ticket/3966)
- Fixed bug in MySQL dialect regarding rendering of table options in
  conjunction with PARTITION options when rendering CREATE TABLE.
  The PARTITION related options need to follow the table options,
  whereas previously this ordering was not enforced.
  References: [#3961](https://www.sqlalchemy.org/trac/ticket/3961)

### oracle

- Fixed bug in cx_Oracle dialect where version string parsing would
  fail for cx_Oracle version 6.0b1 due to the “b” character.  Version
  string parsing is now via a regexp rather than a simple split.
  References: [#3975](https://www.sqlalchemy.org/trac/ticket/3975)

### misc

- Protected against testing “None” as a class in the case where
  declarative classes are being garbage collected and new
  automap prepare() operations are taking place concurrently, very
  infrequently hitting a weakref that has not been fully acted upon
  after gc.
  References: [#3980](https://www.sqlalchemy.org/trac/ticket/3980)

## 1.1.9

Released: April 4, 2017

### sql

- Fixed regression released in 1.1.5 due to [#3859](https://www.sqlalchemy.org/trac/ticket/3859) where
  adjustments to the “right-hand-side” evaluation of an expression
  based on [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant) to honor the underlying type’s
  “right-hand-side” rules caused the [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant) type
  to be inappropriately lost, in those cases when we *do* want the
  left-hand side type to be transferred directly to the right hand side
  so that bind-level rules can be applied to the expression’s argument.
  References: [#3952](https://www.sqlalchemy.org/trac/ticket/3952)
- Changed the mechanics of `ResultProxy` to unconditionally
  delay the “autoclose” step until the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is done
  with the object; in the case where PostgreSQL ON CONFLICT with
  RETURNING returns no rows, autoclose was occurring in this previously
  non-existent use case, causing the usual autocommit behavior that
  occurs unconditionally upon INSERT/UPDATE/DELETE to fail.
  References: [#3955](https://www.sqlalchemy.org/trac/ticket/3955)

### misc

- Fixed regression released in 1.1.8 due to [#3950](https://www.sqlalchemy.org/trac/ticket/3950) where the
  deeper search for information about column types in the case of a
  “schema type” or a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) would produce an attribute
  error if the mapping also contained a [column_property](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property).
  References: [#3956](https://www.sqlalchemy.org/trac/ticket/3956)

## 1.1.8

Released: March 31, 2017

### postgresql

- Added support for parsing the PostgreSQL version string for
  a development version like “PostgreSQL 10devel”.  Pull request
  courtesy Sean McCully.

### misc

- Fixed bug in [sqlalchemy.ext.mutable](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#module-sqlalchemy.ext.mutable) where the
  [Mutable.as_mutable()](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.Mutable.as_mutable) method would not track a type that had
  been copied using `TypeEngine.copy()`.  This became more of
  a regression in 1.1 compared to 1.0 because the [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
  class is now a subclass of [SchemaEventTarget](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.SchemaEventTarget), which among
  other things indicates to the parent [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that the type
  should be copied when the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is.  These copies are
  common when using declarative with mixins or abstract classes.
  References: [#3950](https://www.sqlalchemy.org/trac/ticket/3950)
- Added support for bound parameters, e.g. those normally set up
  via [Query.params()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.params), to the `Result.count()`
  method.  Previously, support for parameters were omitted. Pull request
  courtesy Pat Deegan.

## 1.1.7

Released: March 27, 2017

### orm

- An [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct can now be passed to the
  `Query.select_entity_from()` method.   Entities will be pulled
  from the selectable represented by the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct.
  This allows special options for [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) such as
  [aliased.adapt_on_names](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased.params.adapt_on_names) to be used in conjunction with
  `Query.select_entity_from()`.
  References: [#3933](https://www.sqlalchemy.org/trac/ticket/3933)
- Fixed a race condition which could occur under threaded environments
  as a result of the caching added via [#3915](https://www.sqlalchemy.org/trac/ticket/3915).   An internal
  collection of `Column` objects could be regenerated on an alias
  object inappropriately, confusing a joined eager loader when it
  attempts to render SQL and collect results and resulting in an
  attribute error.   The collection is now generated up front before
  the alias object is cached and shared among threads.
  References: [#3947](https://www.sqlalchemy.org/trac/ticket/3947)

### engine

- Added an exception handler that will warn for the “cause” exception on
  Py2K when the “autorollback” feature of [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) itself
  raises an exception. In Py3K, the two exceptions are naturally reported
  by the interpreter as one occurring during the handling of the other.
  This is continuing with the series of changes for rollback failure
  handling that were last visited as part of [#2696](https://www.sqlalchemy.org/trac/ticket/2696) in 1.0.12.
  References: [#3946](https://www.sqlalchemy.org/trac/ticket/3946)

### sql

- Added support for the [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant) and the [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType)
  objects to be compatible with each other.  That is, a variant
  can be created against a type like [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum), and the instructions
  to create constraints and/or database-specific type objects will
  propagate correctly as per the variant’s dialect mapping.
  References: [#2892](https://www.sqlalchemy.org/trac/ticket/2892)
- Fixed bug in compiler where the string identifier of a savepoint would
  be cached in the identifier quoting dictionary; as these identifiers
  are arbitrary, a small memory leak could occur if a single
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) had an unbounded number of savepoints used,
  as well as if the savepoint clause constructs were used directly
  with an unbounded umber of savepoint names.   The memory leak does
  **not** impact the vast majority of cases as normally the
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), which renders savepoint names with a simple
  counter starting at “1”, is used on a per-transaction or
  per-fixed-number-of-transactions basis before being discarded.
  References: [#3931](https://www.sqlalchemy.org/trac/ticket/3931)
- Fixed bug in new “schema translate” feature where the translated schema
  name would be invoked in terms of an alias name when rendered along
  with a column expression; occurred only when the source translate
  name was “None”.   The “schema translate” feature now only takes
  effect for [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) and [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType) subclasses,
  that is, objects that correspond to a DDL-creatable structure in
  a database.
  References: [#3924](https://www.sqlalchemy.org/trac/ticket/3924)

### oracle

- A fix to cx_Oracle’s WITH_UNICODE mode which was uncovered by the
  fact that cx_Oracle 5.3 now seems to hardcode this flag on in
  the build; an internal method that uses this mode wasn’t using
  the correct signature.
  This change is also **backported** to: 1.0.18
  References: [#3937](https://www.sqlalchemy.org/trac/ticket/3937)

## 1.1.6

Released: February 28, 2017

### orm

- Addressed some long unattended performance concerns within the joined
  eager loader query construction system that have accumulated since
  earlier versions as a result of increased abstraction. The use of ad-
  hoc [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) objects per query, which produces lots of
  column lookup overhead each time, has been replaced with a cached
  approach that makes use of a small pool of [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass)
  objects that are reused between invocations of joined eager loading.
  Some mechanics involving eager join path construction have also been
  optimized.   Callcounts for an end-to-end query construction + single
  row fetch test with a worst-case joined loader scenario have been
  reduced by about 60% vs. 1.1.5 and 42% vs. that of 0.8.6.
  References: [#3915](https://www.sqlalchemy.org/trac/ticket/3915)
- Fixed a major inefficiency in the “eager_defaults” feature whereby
  an unnecessary SELECT would be emitted for column values where the
  ORM had explicitly inserted NULL, corresponding to attributes that
  were unset on the object but did not have any server default
  specified, as well as expired attributes on update that nevertheless
  had no server onupdate set up.   As these columns are not part of the
  RETURNING that eager_defaults tries to use, they should not be
  post-SELECTed either.
  References: [#3909](https://www.sqlalchemy.org/trac/ticket/3909)
- Fixed two closely related bugs involving the mapper eager_defaults
  flag in conjunction with single-table inheritance; one where the
  eager defaults logic would inadvertently try to access a column
  that’s part of the mapper’s “exclude_properties” list (used by
  Declarative with single table inheritance) during the eager defaults
  fetch, and the other where the full load of the row in order to
  fetch the defaults would fail to use the correct inheriting mapper.
  References: [#3908](https://www.sqlalchemy.org/trac/ticket/3908)
- Fixed bug first introduced in 0.9.7 as a result of [#3106](https://www.sqlalchemy.org/trac/ticket/3106)
  which would cause an incorrect query in some forms of multi-level
  subqueryload against aliased entities, with an unnecessary extra
  FROM entity in the innermost subquery.
  References: [#3893](https://www.sqlalchemy.org/trac/ticket/3893)

### orm declarative

- Fixed bug where the “automatic exclude” feature of declarative that
  ensures a column local to a single table inheritance subclass does
  not appear as an attribute on other derivations of the base would
  not take effect for multiple levels of subclassing from the base.
  References: [#3895](https://www.sqlalchemy.org/trac/ticket/3895)

### sql

- Fixed bug whereby the [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect) event would not
  allow a non-textual expression to be passed as the value of the
  “default” for the new column, such as a [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue)
  object to indicate a generic triggered default or a
  [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct.  Clarified the documentation
  in this regard as well.
  References: [#3905](https://www.sqlalchemy.org/trac/ticket/3905)

### postgresql

- Added regular expressions for the “IMPORT FOREIGN SCHEMA”,
  “REFRESH MATERIALIZED VIEW” PostgreSQL statements so that they
  autocommit when invoked via a connection or engine without
  an explicit transaction.  Pull requests courtesy Frazer McLean
  and Paweł Stiasny.
  References: [#3804](https://www.sqlalchemy.org/trac/ticket/3804)
- Fixed bug in PostgreSQL [ExcludeConstraint](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint) where the
  “whereclause” and “using” parameters would not be copied during an
  operation like [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata).
  References: [#3900](https://www.sqlalchemy.org/trac/ticket/3900)

### mysql

- Added new MySQL 8.0 reserved words to the MySQL dialect for proper
  quoting.  Pull request courtesy Hanno Schlichting.

### mssql

- Added a version check to the “get_isolation_level” feature, which is
  invoked upon first connect, so that it skips for SQL Server version
  2000, as the necessary system view is not available prior to SQL Server
  2005.
  References: [#3898](https://www.sqlalchemy.org/trac/ticket/3898)

### misc

- Added `Result.scalar()` and `Result.count()`
  to the “baked” query system.
  References: [#3896](https://www.sqlalchemy.org/trac/ticket/3896)
- Fixed bug in new [sqlalchemy.ext.indexable](https://docs.sqlalchemy.org/en/20/orm/extensions/indexable.html#module-sqlalchemy.ext.indexable) extension
  where setting of a property that itself refers to another property
  would fail.
  References: [#3901](https://www.sqlalchemy.org/trac/ticket/3901)

## 1.1.5

Released: January 17, 2017

### orm

- Fixed bug involving joined eager loading against multiple entities
  when polymorphic inheritance is also in use which would throw
  “‘NoneType’ object has no attribute ‘isa’”.  The issue was introduced
  by the fix for [#3611](https://www.sqlalchemy.org/trac/ticket/3611).
  This change is also **backported** to: 1.0.17
  References: [#3884](https://www.sqlalchemy.org/trac/ticket/3884)
- Fixed bug in subquery loading where an object encountered as an
  “existing” row, e.g. already loaded from a different path in the
  same query, would not invoke subquery loaders for unloaded attributes
  that specified this loading.  This issue is in the same area
  as that of [#3431](https://www.sqlalchemy.org/trac/ticket/3431), [#3811](https://www.sqlalchemy.org/trac/ticket/3811) which involved
  similar issues with joined loading.
  References: [#3854](https://www.sqlalchemy.org/trac/ticket/3854)
- The [Session.no_autoflush](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.no_autoflush) context manager now ensures that
  the autoflush flag is reset within a “finally” block, so that if
  an exception is raised within the block, the state still resets
  appropriately.  Pull request courtesy Emin Arakelian.
- Fixed bug where the single-table inheritance query criteria would not
  be inserted into the query in the case that the [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle)
  construct were used as the selection criteria.
  References: [#3874](https://www.sqlalchemy.org/trac/ticket/3874)
- Fixed bug related to [#3177](https://www.sqlalchemy.org/trac/ticket/3177), where a UNION or other set operation
  emitted by a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) would apply “single-inheritance” criteria
  to the outside of the union (also referencing the wrong selectable),
  even though this criteria is now expected to
  be already present on the inside subqueries.  The single-inheritance
  criteria is now omitted once union() or another set operation is
  called against [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) in the same way as `Query.from_self()`.
  References: [#3856](https://www.sqlalchemy.org/trac/ticket/3856)

### examples

- Fixed two issues with the versioned_history example, one is that
  the history table now gets autoincrement=False to avoid 1.1’s new
  errors regarding composite primary keys with autoincrement; the other
  is that the sqlite_autoincrement flag is now used to ensure on SQLite,
  unique identifiers are used for the lifespan of a table even if
  some rows are deleted.  Pull request courtesy Carlos García Montoro.
  References: [#3872](https://www.sqlalchemy.org/trac/ticket/3872)

### engine

- The “extend_existing” option of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) reflection would
  cause indexes and constraints to be doubled up in the case that the parameter
  were used with [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) (as the automap extension does)
  due to tables being reflected both within the foreign key path as well
  as directly.  A new de-duplicating set is passed through within the
  [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) sequence to prevent double reflection in this
  way.
  References: [#3861](https://www.sqlalchemy.org/trac/ticket/3861)

### sql

- Fixed bug originally introduced in 0.9 via [#1068](https://www.sqlalchemy.org/trac/ticket/1068) where
  order_by(<some Label()>) would order by the label name based on name
  alone, that is, even if the labeled expression were not at all the same
  expression otherwise present, implicitly or explicitly, in the
  selectable.  The logic that orders by label now ensures that the
  labeled expression is related to the one that resolves to that name
  before ordering by the label name; additionally, the name has to
  resolve to an actual label explicit in the expression elsewhere, not
  just a column name.  This logic is carefully kept separate from the
  order by(textual name) feature that has a slightly different purpose.
  References: [#3882](https://www.sqlalchemy.org/trac/ticket/3882)
- Fixed 1.1 regression where `import *` would not work for
  sqlalchemy.sql.expression, due to mis-spelled `any_` and `all_`
  functions.
  References: [#3878](https://www.sqlalchemy.org/trac/ticket/3878)
- The engine URL embedded in the exception for “could not reflect”
  in [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) now conceals the password; also
  the `__repr__` for `TLEngine` now acts like that of
  [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), concealing the URL password.  Pull request courtesy
  Valery Yundin.
- Fixed issue in [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant) where the “right hand coercion” logic,
  inherited from [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator), would
  coerce the right-hand side into the [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant) itself, rather than
  what the default type for the [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant) would do.   In the
  case of [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant), we want the type to act mostly like the base
  type so the default logic of [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) is now overridden
  to fall back to the underlying wrapped type’s logic.   Is mostly relevant
  for JSON at the moment.
  References: [#3859](https://www.sqlalchemy.org/trac/ticket/3859)
- Fixed bug where literal_binds compiler flag was not honored by the
  [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct for the “multiple values” feature; the
  subsequent values are now rendered as literals.
  References: [#3880](https://www.sqlalchemy.org/trac/ticket/3880)

### postgresql

- Fixed bug in new “ON CONFLICT DO UPDATE” feature where the “set”
  values for the UPDATE clause would not be subject to type-level
  processing, as normally takes effect to handle both user-defined
  type level conversions as well as dialect-required conversions, such
  as those required for JSON datatypes.   Additionally, clarified that
  the keys in the `set_` dictionary should match the “key” of the
  column, if distinct from the column name.  A warning is emitted
  for remaining column names that don’t match column keys; for
  compatibility reasons, these are emitted as they were previously.
  References: [#3888](https://www.sqlalchemy.org/trac/ticket/3888)
- The [TIME](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.TIME) and [TIMESTAMP](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.TIMESTAMP)
  datatypes now support a setting of zero for “precision”; previously
  a zero would be ignored.  Pull request courtesy Ionuț Ciocîrlan.

### mysql

- Added a new parameter `mysql_prefix` supported by the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index)
  construct, allows specification of MySQL-specific prefixes such as
  “FULLTEXT”. Pull request courtesy Joseph Schorr.
- The MySQL dialect now will not warn when a reflected column has a
  “COMMENT” keyword on it, but note however the comment is not yet
  reflected; this is on the roadmap for a future release.  Pull request
  courtesy Lele Long.
  References: [#3867](https://www.sqlalchemy.org/trac/ticket/3867)

### mssql

- Fixed bug where SQL Server dialects would attempt to select the
  last row identity for an INSERT from SELECT, failing in the case when
  the SELECT has no rows.  For such a statement,
  the inline flag is set to True indicating no last primary key
  should be fetched.
  References: [#3876](https://www.sqlalchemy.org/trac/ticket/3876)

### oracle

- Fixed bug where an INSERT from SELECT where the source table contains
  an autoincrementing Sequence would fail to compile correctly.
  References: [#3877](https://www.sqlalchemy.org/trac/ticket/3877)
- Fixed bug where the “COMPRESSION” keyword was used in the ALL_TABLES
  query on Oracle 9.2; even though Oracle docs state table compression
  was introduced in 9i, the actual column is not present until
  10.1.
  References: [#3875](https://www.sqlalchemy.org/trac/ticket/3875)

### misc

- Fixed Python 3.6 DeprecationWarnings related to escaped strings without
  the ‘r’ modifier, and added test coverage for Python 3.6.
  This change is also **backported** to: 1.0.17
  References: [#3886](https://www.sqlalchemy.org/trac/ticket/3886)
- Ported the fix for Oracle quoted-lowercase names to Firebird, so that
  a table name that is quoted as lower case can be reflected properly
  including when the table name comes from the get_table_names()
  inspection function.
  References: [#3548](https://www.sqlalchemy.org/trac/ticket/3548)

## 1.1.4

Released: November 15, 2016

### orm

- Fixed bug in [Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings) where an alternate-named
  primary key attribute would not track properly into the UPDATE statement.
  This change is also **backported** to: 1.0.16
  References: [#3849](https://www.sqlalchemy.org/trac/ticket/3849)
- Fixed bug in `Session.bulk_save()` where an UPDATE would
  not function correctly in conjunction with a mapping that
  implements a version id counter.
  This change is also **backported** to: 1.0.16
  References: [#3781](https://www.sqlalchemy.org/trac/ticket/3781)
- Fixed bug where the [Mapper.attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.attrs),
  [Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors) and other derived attributes would
  fail to refresh when mapper properties or other ORM constructs were
  added to the mapper/class after these  accessors were first called.
  This change is also **backported** to: 1.0.16
  References: [#3778](https://www.sqlalchemy.org/trac/ticket/3778)
- Fixed regression in collections due to [#3457](https://www.sqlalchemy.org/trac/ticket/3457) whereby
  deserialize during pickle or deepcopy would fail to establish all
  attributes of an ORM collection, causing further mutation operations to
  fail.
  References: [#3852](https://www.sqlalchemy.org/trac/ticket/3852)
- Fixed long-standing bug where the “noload” relationship loading
  strategy would cause backrefs and/or back_populates options to be
  ignored.
  References: [#3845](https://www.sqlalchemy.org/trac/ticket/3845)

### engine

- Removed long-broken “default_schema_name()” method from
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  This method was left over from a very old
  version and was non-working (e.g. would raise).  Pull request
  courtesy Benjamin Dopplinger.

### sql

- Fixed bug where newly added warning for primary key on insert w/o
  autoincrement setting (see [#3216](https://www.sqlalchemy.org/trac/ticket/3216)) would fail to emit
  correctly when invoked upon a lower-case [table()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table) construct.
  References: [#3842](https://www.sqlalchemy.org/trac/ticket/3842)

### postgresql

- Fixed regression caused by the fix in [#3807](https://www.sqlalchemy.org/trac/ticket/3807) (version 1.1.0)
  where we ensured that the tablename was qualified in the WHERE clause
  of the DO UPDATE portion of PostgreSQL’s ON CONFLICT, however you
  *cannot* put the table name in the  WHERE clause in the actual ON
  CONFLICT itself.   This was an incorrect assumption, so that portion
  of the change in [#3807](https://www.sqlalchemy.org/trac/ticket/3807) is rolled back.
  References: [#3807](https://www.sqlalchemy.org/trac/ticket/3807), [#3846](https://www.sqlalchemy.org/trac/ticket/3846)

### mysql

- Added support for server side cursors to the mysqlclient and
  pymysql dialects.   This feature is available via the
  [Connection.execution_options.stream_results](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.stream_results) flag as well
  as the `server_side_cursors=True` dialect argument in the
  same way that it has been for psycopg2 on PostgreSQL.  Pull request
  courtesy Roman Podoliaka.
- MySQL’s native ENUM type supports any non-valid value being sent, and
  in response will return a blank string.  A hardcoded rule to check for
  “is returning the blank string” has been added to the  MySQL
  implementation for ENUM so that this blank string is returned to the
  application rather than being rejected as a non-valid value.  Note that
  if your MySQL enum is linking values to objects, you still get the
  blank string back.
  References: [#3841](https://www.sqlalchemy.org/trac/ticket/3841)

### sqlite

- Added quotes to the PRAGMA directives in the pysqlcipher dialect
  to support additional cipher arguments appropriately.  Pull request
  courtesy Kevin Jurczyk.
- Added an optional import for the pysqlcipher3 DBAPI when using the
  pysqlcipher dialect.  This package will attempt to be imported
  if the Python-2 only pysqlcipher DBAPI is non-present.
  Pull request courtesy Kevin Jurczyk.

### mssql

- Fixed bug in pyodbc dialect (as well as in the mostly non-working
  adodbapi dialect) whereby a semicolon present in the password
  or username fields could be interpreted as a separator for another
  token; the values are now quoted when semicolons are present.
  This change is also **backported** to: 1.0.16
  References: [#3762](https://www.sqlalchemy.org/trac/ticket/3762)

## 1.1.3

Released: October 27, 2016

### orm

- Fixed regression caused by [#2677](https://www.sqlalchemy.org/trac/ticket/2677) whereby calling
  [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) on an object that was already flushed as
  deleted in that session would fail to set up the object in the
  identity map (or reject the object), causing flush errors as the
  object were in a state not accommodated by the unit of work.
  The pre-1.1 behavior in this case has been restored, which is that
  the object is put back into the identity map so that the DELETE
  statement will be attempted again, which emits a warning that the number
  of expected rows was not matched (unless the row were restored outside
  of the session).
  References: [#3839](https://www.sqlalchemy.org/trac/ticket/3839)
- Fixed regression where some [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) methods like
  [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) and others would fail if the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
  were against a series of mapped columns, rather than the mapped
  entity as a whole.
  References: [#3836](https://www.sqlalchemy.org/trac/ticket/3836)

### sql

- Fixed bug involving new value translation and validation feature
  in [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) whereby using the enum object in a string
  concatenation would maintain the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) type as the type
  of the expression overall, producing missing lookups.  A string
  concatenation against an [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum)-typed column now uses
  [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) as the datatype of the expression itself.
  References: [#3833](https://www.sqlalchemy.org/trac/ticket/3833)
- Fixed regression which occurred as a side effect of [#2919](https://www.sqlalchemy.org/trac/ticket/2919),
  which in the less typical case of a user-defined
  [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) that was also itself an instance of
  [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType) (rather than the implementation being such)
  would cause the column attachment events to be skipped for the
  type itself.
  References: [#3832](https://www.sqlalchemy.org/trac/ticket/3832)

### postgresql

- PostgreSQL table reflection will ensure that the
  [Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement) flag is set to False when reflecting
  a primary key column that is not of an [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) datatype,
  even if the default is related to an integer-generating sequence.
  This can happen if a column is created as SERIAL and the datatype
  is changed.  The autoincrement flag can only be True if the datatype
  is of integer affinity in the 1.1 series.
  References: [#3835](https://www.sqlalchemy.org/trac/ticket/3835)

## 1.1.2

Released: October 17, 2016

### orm

- Fixed bug involving the rule to disable a joined collection eager
  loader on the other side of a many-to-one lazy loader, first added
  in [#1495](https://www.sqlalchemy.org/trac/ticket/1495), where the rule would fail if the parent object
  had some other lazyloader-bound query options associated with it.
  References: [#3824](https://www.sqlalchemy.org/trac/ticket/3824)
- Fixed self-referential entity, deferred column loading issue in a
  similar style as that of [#3431](https://www.sqlalchemy.org/trac/ticket/3431), [#3811](https://www.sqlalchemy.org/trac/ticket/3811) where an entity
  is present in multiple positions within the row due to self-referential
  eager loading; when the deferred loader only applies to one of the
  paths, the “present” column loader will now override the deferred non-
  load for that entity regardless of row ordering.
  References: [#3822](https://www.sqlalchemy.org/trac/ticket/3822)

### sql

- Fixed a regression caused by a newly added function that performs the
  “wrap callable” function of sql [DefaultGenerator](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.DefaultGenerator) objects,
  an attribute error raised for `__module__` when the default callable
  was a `functools.partial` or other object that doesn’t have a
  `__module__` attribute.
  References: [#3823](https://www.sqlalchemy.org/trac/ticket/3823)
- Fixed regression in [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) type where event handlers were not
  transferred in the case of the type object being copied, due to a
  conflicting copy() method added as part of [#3250](https://www.sqlalchemy.org/trac/ticket/3250).  This copy
  occurs normally in situations when the column is copied, such as
  in tometadata() or when using declarative mixins with columns.  The
  event handler not being present would impact the constraint being
  created for a non-native enumerated type, but more critically the
  ENUM object on the PostgreSQL backend.
  References: [#3827](https://www.sqlalchemy.org/trac/ticket/3827)

### postgresql

- Changed the naming convention used when generating bound parameters
  for a multi-VALUES insert statement, so that the numbered parameter
  names don’t conflict with the anonymized parameters of a WHERE clause,
  as is now common in a PostgreSQL ON CONFLICT construct.
  References: [#3828](https://www.sqlalchemy.org/trac/ticket/3828)

## 1.1.1

Released: October 7, 2016

### mssql

- The “SELECT SERVERPROPERTY”
  query added in [#3810](https://www.sqlalchemy.org/trac/ticket/3810) and [#3814](https://www.sqlalchemy.org/trac/ticket/3814) is failing on unknown
  combinations of Pyodbc and SQL Server.  While failure of this function
  was anticipated, the exception catch was not broad enough so it now
  catches all forms of pyodbc.Error.
  References: [#3820](https://www.sqlalchemy.org/trac/ticket/3820)

### misc

- Changed the CompileError raised when various primary key missing
  situations are detected to a warning.  The statement is again
  passed to the database where it will fail and the DBAPI error (usually
  IntegrityError) raises as usual.
  See also
  [The .autoincrement directive is no longer implicitly enabled for a composite primary key column](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3216)
  References: [#3216](https://www.sqlalchemy.org/trac/ticket/3216)

## 1.1.0

Released: October 5, 2016

### orm

- Enhanced the new “raise” lazy loader strategy to also include a
  “raise_on_sql” variant, available both via [relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy)
  as well as [raiseload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.raiseload).   This variant only raises if the
  lazy load would actually emit SQL, vs. raising if the lazy loader
  mechanism is invoked at all.
  References: [#3812](https://www.sqlalchemy.org/trac/ticket/3812)
- The [Query.group_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.group_by) method now resets the group by collection
  if an argument of `None` is passed, in the same way that
  [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) has worked for a long time.  Pull request
  courtesy Iuri Diniz.
- Passing False to [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) in order to cancel
  all order by’s is deprecated; there is no longer any difference
  between calling this method with False or with None.
- Fixed bug where joined eager loading would fail for a polymorphically-
  loaded mapper, where the polymorphic_on was set to an un-mapped
  expression such as a CASE expression.
  This change is also **backported** to: 1.0.16
  References: [#3800](https://www.sqlalchemy.org/trac/ticket/3800)
- Fixed bug where the ArgumentError raised for an invalid bind
  sent to a Session via [Session.bind_mapper()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bind_mapper),
  [Session.bind_table()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bind_table),
  or the constructor would fail to be correctly raised.
  This change is also **backported** to: 1.0.16
  References: [#3798](https://www.sqlalchemy.org/trac/ticket/3798)
- Fixed bug in subquery eager loading where a subqueryload
  of an “of_type()” object linked to a second subqueryload of a plain
  mapped class, or a longer chain of several “of_type()” attributes,
  would fail to link the joins correctly.
  This change is also **backported** to: 1.0.15
  References: [#3773](https://www.sqlalchemy.org/trac/ticket/3773), [#3774](https://www.sqlalchemy.org/trac/ticket/3774)
- ORM attributes can now be assigned any object that is has a
  `__clause_element__()` attribute, which will result in inline
  SQL the way any [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) class does.  This covers other
  mapped attributes not otherwise transformed by further expression
  constructs.
  References: [#3802](https://www.sqlalchemy.org/trac/ticket/3802)
- Made an adjustment to the bug fix first introduced in [ticket:3431]
  that involves an object appearing in multiple contexts in a single
  result set, such that an eager loader that would set the related
  object value to be None will still fire off, thus satisfying the
  load of that attribute.  Previously, the adjustment only honored
  a non-None value arriving for an eagerly loaded attribute in a
  secondary row.
  References: [#3811](https://www.sqlalchemy.org/trac/ticket/3811)
- Fixed bug in new [SessionEvents.persistent_to_deleted()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.persistent_to_deleted) event
  where the target object could be garbage collected before the event
  is fired off.
  References: [#3808](https://www.sqlalchemy.org/trac/ticket/3808)
- The primaryjoin of a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct can now include
  a [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) object that includes a callable function to
  generate values.  Previously, the lazy loader strategy would
  be incompatible with this use, and additionally would fail to correctly
  detect if the “use_get” criteria should be used if the primary key
  were involved with the bound parameter.
  References: [#3767](https://www.sqlalchemy.org/trac/ticket/3767)
- An UPDATE emitted from the ORM flush process can now accommodate a
  SQL expression element for a column within the primary key of an
  object, if the target database supports RETURNING in order to provide
  the new value, or if the PK value is set “to itself” for the purposes
  of bumping some other trigger / onupdate on the column.
  References: [#3801](https://www.sqlalchemy.org/trac/ticket/3801)
- Fixed bug where the “simple many-to-one” condition that allows  lazy
  loading to use get() from identity map would fail to be  invoked if the
  primaryjoin of the relationship had multiple clauses separated by AND
  which were not in the same order as that of the primary key columns
  being compared in each clause. This ordering
  difference occurs for a composite foreign key where the table-bound
  columns on the referencing side were not in the same order in the .c
  collection as the primary key columns on the referenced side….which
  in turn occurs a lot if one is using declarative mixins and/or
  declared_attr to set up columns.
  References: [#3788](https://www.sqlalchemy.org/trac/ticket/3788)
- An exception is raised when two `@validates` decorators on a mapping
  make use of the same name.  Only one validator of a certain name
  at a time is supported, there’s no mechanism to chain these together,
  as the order of the validators at the level of function decorator
  can’t be made deterministic.
  See also
  [Same-named @validates decorators will now raise an exception](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3776)
  References: [#3776](https://www.sqlalchemy.org/trac/ticket/3776)
- Mapper errors raised during [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) now explicitly
  include the name of the originating mapper in the exception message
  to help in those situations where the wrapped exception does not
  itself include the source mapper.  Pull request courtesy
  John Perkins.

### orm declarative

- Constructing a declarative base class that inherits from another class
  will also inherit its docstring. This means
  `as_declarative()` acts more like a normal class
  decorator.

### sql

- Fixed bug in [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) where the internal method
  `_reset_exported()` would corrupt the state of the object.  This
  method is intended for selectable objects and is called by the ORM
  in some cases; an erroneous mapper configuration would could lead the
  ORM to call this on a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.
  This change is also **backported** to: 1.0.15
  References: [#3755](https://www.sqlalchemy.org/trac/ticket/3755)
- Execution options can now be propagated from within a
  statement at compile time to the outermost statement, so that
  if an embedded element wants to set “autocommit” to be True for example,
  it can propagate this to the enclosing statement.  Currently, this
  feature is enabled for a DML-oriented CTE embedded inside of a SELECT
  statement, e.g. INSERT/UPDATE/DELETE inside of SELECT.
  References: [#3805](https://www.sqlalchemy.org/trac/ticket/3805)
- A string sent as a column default via the
  [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) parameter is now escaped for quotes.
  See also
  [String server_default now literal quoted](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3809)
  References: [#3809](https://www.sqlalchemy.org/trac/ticket/3809)
- Added compiler-level flags used by PostgreSQL to place additional
  parenthesis than would normally be generated by precedence rules
  around operations involving JSON, HSTORE indexing operators as well as
  within their operands since it has been observed that PostgreSQL’s
  precedence rules for at least the HSTORE indexing operator is not
  consistent between 9.4 and 9.5.
  References: [#3806](https://www.sqlalchemy.org/trac/ticket/3806)
- The `BaseException` exception class is now intercepted by the
  exception-handling routines of [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), and includes
  handling by the `ConnectionEvents.handle_error()`
  event.  The [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is now **invalidated** by default in
  the case of a system level exception that is not a subclass of
  `Exception`, including `KeyboardInterrupt` and the greenlet
  `GreenletExit` class, to prevent further operations from occurring
  upon a database connection that is in an unknown and possibly
  corrupted state.  The MySQL drivers are most targeted by this change
  however the change is across all DBAPIs.
  See also
  [Engines now invalidate connections, run error handlers for BaseException](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3803)
  References: [#3803](https://www.sqlalchemy.org/trac/ticket/3803)
- The “eq” and “ne” operators are no longer part of the list of
  “associative” operators, while they remain considered to be
  “commutative”.  This allows an expression like `(x == y) == z`
  to be maintained at the SQL level with parenthesis.  Pull request
  courtesy John Passaro.
  References: [#3799](https://www.sqlalchemy.org/trac/ticket/3799)
- Stringify of expression with unnamed [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects, as
  occurs in lots of situations including ORM error reporting,
  will now render the name in string context as “<name unknown>”
  rather than raising a compile error.
  References: [#3789](https://www.sqlalchemy.org/trac/ticket/3789)
- Raise a more descriptive exception / message when ClauseElement
  or non-SQLAlchemy objects that are not “executable” are erroneously
  passed to `.execute()`; a new exception ObjectNotExecutableError
  is raised consistently in all cases.
  References: [#3786](https://www.sqlalchemy.org/trac/ticket/3786)
- Fixed regression in JSON datatypes where the “literal processor” for
  a JSON index value would not be invoked.  The native String and Integer
  datatypes are now called upon from within the JSONIndexType
  and JSONPathType.  This is applied to the generic, PostgreSQL, and
  MySQL JSON types and also has a dependency on [#3766](https://www.sqlalchemy.org/trac/ticket/3766).
  References: [#3765](https://www.sqlalchemy.org/trac/ticket/3765)
- Fixed bug where [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) would fail to extract columns from
  compound SQL expressions if those SQL expressions were wrapped inside
  of an ORM-style `__clause_element__()` construct.  This bug
  exists in 1.0.x as well, however in 1.1 is more noticeable as
  hybrid_property @expression now returns a wrapped element.
  References: [#3763](https://www.sqlalchemy.org/trac/ticket/3763)

### postgresql

- An adjustment to ON CONFLICT such that the “inserted_primary_key”
  logic is able to accommodate the case where there’s no INSERT or
  UPDATE and there’s no net change.  The value comes out as None
  in this case, rather than failing on an exception.
  References: [#3813](https://www.sqlalchemy.org/trac/ticket/3813)
- > Fixed issue in new PG “on conflict” construct where columns including
  > those of the “excluded” namespace would not be table-qualified
  > in the WHERE clauses in the statement.
  References: [#3807](https://www.sqlalchemy.org/trac/ticket/3807)

### mysql

- Added support for parsing MySQL/Connector boolean and integer
  arguments within the URL query string: connection_timeout,
  connect_timeout, pool_size, get_warnings,
  raise_on_warnings, raw, consume_results, ssl_verify_cert, force_ipv6,
  pool_reset_session, compress, allow_local_infile, use_pure.
  This change is also **backported** to: 1.0.15
  References: [#3787](https://www.sqlalchemy.org/trac/ticket/3787)
- Fixed bug where the “literal_binds” flag would not be propagated
  to a CAST expression under MySQL.
  References: [#3766](https://www.sqlalchemy.org/trac/ticket/3766)

### mssql

- Changed the query used to get “default schema name”, from one that
  queries the database principals table to using the
  “schema_name()” function, as issues have been reported that the
  former system was unavailable on the Azure Data Warehouse edition.
  It is hoped that this will finally work across all SQL Server
  versions and authentication styles.
  This change is also **backported** to: 1.0.16
  References: [#3810](https://www.sqlalchemy.org/trac/ticket/3810)
- Updated the server version info scheme for pyodbc to use SQL Server
  SERVERPROPERTY(), rather than relying upon pyodbc.SQL_DBMS_VER, which
  continues to be unreliable particularly with FreeTDS.
  This change is also **backported** to: 1.0.16
  References: [#3814](https://www.sqlalchemy.org/trac/ticket/3814)
- Added error code 20017 “unexpected EOF from the server” to the list of
  disconnect exceptions that result in a connection pool reset.  Pull
  request courtesy Ken Robbins.
  This change is also **backported** to: 1.0.16
  References: [#3791](https://www.sqlalchemy.org/trac/ticket/3791)

### misc

- Fixed bug where setting up a single-table inh subclass of a joined-table
  subclass which included an extra column would corrupt the foreign keys
  collection of the mapped table, thereby interfering with the
  initialization of relationships.
  This change is also **backported** to: 1.0.16
  References: [#3797](https://www.sqlalchemy.org/trac/ticket/3797)

## 1.1.0b3

Released: July 26, 2016

### orm

- Removed a warning that dates back to 0.4 which emits when a same-named
  relationship is placed on two mappers that inherits via joined or
  single table inheritance.   The warning does not apply to the
  current unit of work implementation.
  See also
  [Same-named relationships on inheriting mappers no longer warn](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3749)
  References: [#3749](https://www.sqlalchemy.org/trac/ticket/3749)

### sql

- Fixed bug in new CTE feature for update/insert/delete stated
  as a CTE inside of an enclosing statement (typically SELECT) whereby
  oninsert and onupdate values weren’t called upon for the embedded
  statement.
  References: [#3745](https://www.sqlalchemy.org/trac/ticket/3745)
- Fixed bug in new CTE feature for update/insert/delete whereby
  an anonymous (e.g. no name passed) [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) construct around
  the statement would fail.
  References: [#3744](https://www.sqlalchemy.org/trac/ticket/3744)

### postgresql

- Fixed bug whereby [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) and [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant)
  types were not deeply inspected enough by the PostgreSQL dialect
  to determine if SMALLSERIAL or BIGSERIAL needed to be rendered
  rather than SERIAL.
  This change is also **backported** to: 1.0.14
  References: [#3739](https://www.sqlalchemy.org/trac/ticket/3739)

### oracle

- Fixed bug in [Select.with_for_update.of](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update.params.of), where the Oracle
  “rownum” approach to LIMIT/OFFSET would fail to accommodate for the
  expressions inside the “OF” clause, which must be stated at the topmost
  level referring to expression within the subquery.  The expressions are
  now added to the subquery if needed.
  This change is also **backported** to: 1.0.14
  References: [#3741](https://www.sqlalchemy.org/trac/ticket/3741)

### misc

- Added a “default” parameter to the new sqlalchemy.ext.indexable
  extension.
- Fixed bug in `sqlalchemy.ext.baked` where the unbaking of a
  subquery eager loader query would fail due to a variable scoping
  issue, when multiple subquery loaders were involved.  Pull request
  courtesy Mark Hahnenberg.
  This change is also **backported** to: 1.0.15
  References: [#3743](https://www.sqlalchemy.org/trac/ticket/3743)
- sqlalchemy.ext.indexable will intercept IndexError as well
  as KeyError when raising as AttributeError.

## 1.1.0b2

Released: July 1, 2016

### sql

- Fixed issue in SQL math negation operator where the type of the
  expression would no longer be the numeric type of the original.
  This would cause issues where the type determined result set
  behaviors.
  This change is also **backported** to: 1.0.14
  References: [#3735](https://www.sqlalchemy.org/trac/ticket/3735)
- Fixed bug whereby the `__getstate__` / `__setstate__`
  methods for sqlalchemy.util.Properties were
  non-working due to the transition in the 1.0 series to `__slots__`.
  The issue potentially impacted some third-party applications.
  Pull request courtesy Pieter Mulder.
  This change is also **backported** to: 1.0.14
  References: [#3728](https://www.sqlalchemy.org/trac/ticket/3728)
- The processing performed by the [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) datatype for backends
  that only feature integer types has been made consistent between the
  pure Python and C-extension versions, in that the C-extension version
  will accept any integer value from the database as a boolean, not just
  zero and one; additionally, non-boolean integer values being sent to
  the database are coerced to exactly zero or one, instead of being
  passed as the original integer value.
  See also
  [Non-native boolean integer values coerced to zero/one/None in all cases](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3730)
  References: [#3730](https://www.sqlalchemy.org/trac/ticket/3730)
- Rolled back the validation rules a bit in [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) to allow
  unknown string values to pass through, unless the flag
  `validate_string=True` is passed to the Enum; any other kind of object is
  still of course rejected.  While the immediate use
  is to allow comparisons to enums with LIKE, the fact that this
  use exists indicates there may be more unknown-string-comparison use
  cases than we expected, which hints that perhaps there are some
  unknown string-INSERT cases too.
  References: [#3725](https://www.sqlalchemy.org/trac/ticket/3725)

### postgresql

- Made a slight behavioral change in the `sqlalchemy.ext.compiler`
  extension, whereby the existing compilation schemes for an established
  construct would be removed if that construct itself didn’t already
  have its own dedicated `__visit_name__`.  This was a
  rare occurrence in 1.0, however in 1.1 [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY)
  subclasses [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) and has this behavior.
  As a result, setting up a compilation handler for another dialect
  such as SQLite would render the main [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY)
  object no longer compilable.
  References: [#3732](https://www.sqlalchemy.org/trac/ticket/3732)

### mysql

- Dialed back the “order the primary key columns per auto-increment”
  described in [No more generation of an implicit KEY for composite primary key w/ AUTO_INCREMENT](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-mysql-3216) a bit, so that if the
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) is explicitly defined, the order
  of columns is maintained exactly, allowing control of this behavior
  when necessary.
  References: [#3726](https://www.sqlalchemy.org/trac/ticket/3726)

## 1.1.0b1

Released: June 16, 2016

### orm

- A new ORM extension [Indexable](https://docs.sqlalchemy.org/en/20/orm/extensions/indexable.html) is added, which allows
  construction of Python attributes which refer to specific elements
  of “indexed” structures such as arrays and JSON fields.  Pull request
  courtesy Jeong YunWon.
  See also
  [New Indexable ORM extension](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#feature-indexable)
- Added new flag [Session.bulk_insert_mappings.render_nulls](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings.params.render_nulls)
  which allows an ORM bulk INSERT to occur with NULL values rendered;
  this bypasses server side defaults, however allows all statements
  to be formed with the same set of columns, allowing them to be
  batched.  Pull request courtesy Tobias Sauerwein.
- Added new event [AttributeEvents.init_scalar()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.init_scalar), as well
  as a new example suite illustrating its use.  This event can be used
  to provide a Core-generated default value to a Python-side attribute
  before the object is persisted.
  See also
  [New init_scalar() event intercepts default values at ORM level](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-1311)
  References: [#1311](https://www.sqlalchemy.org/trac/ticket/1311)
- Added [AutomapBase.prepare.schema](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase.prepare.params.schema) to the
  [AutomapBase.prepare()](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase.prepare) method, to indicate which schema
  tables should be reflected from if not the default schema.
  Pull request courtesy Josh Marlow.
- Added new parameter `mapper.passive_deletes` to
  available mapper options.   This allows a DELETE to proceed
  for a joined-table inheritance mapping against the base table only,
  while allowing for ON DELETE CASCADE to handle deleting the row
  from the subclass tables.
  See also
  [passive_deletes feature for joined-inheritance mappings](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2349)
  References: [#2349](https://www.sqlalchemy.org/trac/ticket/2349)
- Calling str() on a core SQL construct has been made more “friendly”,
  when the construct contains non-standard SQL elements such as
  RETURNING, array index operations, or dialect-specific or custom
  datatypes.  A string is now returned in these cases rendering an
  approximation of the construct (typically the PostgreSQL-style
  version of it) rather than raising an error.
  See also
  [“Friendly” stringification of Core SQL constructs without a dialect](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3631)
  References: [#3631](https://www.sqlalchemy.org/trac/ticket/3631)
- The `str()` call for [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) will now take into account
  the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) to which the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is bound, when
  generating the string form of the SQL, so that the actual SQL
  that would be emitted to the database is shown, if possible.  Previously,
  only the engine associated with the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) to which the
  mappings are associated would be used, if present.  If
  no bind can be located either on the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) or on
  the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) to which the mappings are associated, then
  the “default” dialect is used to render the SQL, as was the case
  previously.
  See also
  [Stringify of Query will consult the Session for the correct dialect](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3081)
  References: [#3081](https://www.sqlalchemy.org/trac/ticket/3081)
- The [SessionEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents) suite now includes events to allow
  unambiguous tracking of all object lifecycle state transitions
  in terms of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) itself, e.g. pending,
  transient,  persistent, detached.   The state of the object
  within each event is also defined.
  See also
  [New Session lifecycle events](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2677)
  References: [#2677](https://www.sqlalchemy.org/trac/ticket/2677)
- Added a new session lifecycle state [deleted](https://docs.sqlalchemy.org/en/20/glossary.html#term-deleted).  This new state
  represents an object that has been deleted from the [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent)
  state and will move to the [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached) state once the transaction
  is committed.  This resolves the long-standing issue that objects
  which were deleted existed in a gray area between persistent and
  detached.   The [InstanceState.persistent](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.persistent) accessor will
  **no longer** report on a deleted object as persistent; the
  [InstanceState.deleted](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.deleted) accessor will instead be True for
  these objects, until they become detached.
  See also
  [New Session lifecycle events](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2677)
  References: [#2677](https://www.sqlalchemy.org/trac/ticket/2677)
- Added new checks for the common error case of passing mapped classes
  or mapped instances into contexts where they are interpreted as
  SQL bound parameters; a new exception is raised for this.
  See also
  [Specific checks added for passing mapped classes, instances as SQL literals](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3321)
  References: [#3321](https://www.sqlalchemy.org/trac/ticket/3321)
- Added new relationship loading strategy [raiseload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.raiseload) (also
  accessible via `lazy='raise'`).  This strategy behaves almost like
  [noload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.noload) but instead of returning `None` it raises an
  InvalidRequestError.  Pull request courtesy Adrian Moennich.
  See also
  [New “raise” / “raise_on_sql” loader strategies](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3512)
  References: [#3512](https://www.sqlalchemy.org/trac/ticket/3512)
- The [Mapper.order_by](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.order_by) parameter is deprecated.
  This is an old parameter no longer relevant to how SQLAlchemy
  works, once the Query object was introduced.  By deprecating it
  we establish that we aren’t supporting non-working use cases
  and that we encourage applications to move off of the use of this
  parameter.
  See also
  [Mapper.order_by is deprecated](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3394)
  References: [#3394](https://www.sqlalchemy.org/trac/ticket/3394)
- The [Session.weak_identity_map](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.weak_identity_map) parameter is deprecated.
  See the new recipe at [Session Referencing Behavior](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-referencing-behavior) for
  an event-based approach to maintaining strong identity map behavior.
  See also
  [New Session lifecycle events](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2677)
  References: [#2677](https://www.sqlalchemy.org/trac/ticket/2677)
- Fixed an issue where a many-to-one change of an object from one
  parent to another could work inconsistently when combined with
  an un-flushed modification of the foreign key attribute.  The attribute
  move now considers the database-committed value of the foreign key
  in order to locate the “previous” parent of the object being
  moved.   This allows events to fire off correctly including
  backref events.  Previously, these events would not always fire.
  Applications which may have relied on the previously broken
  behavior may be affected.
  See also
  [Fix involving many-to-one object moves with user-initiated foreign key manipulations](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3708)
  References: [#3708](https://www.sqlalchemy.org/trac/ticket/3708)
- Fixed bug where deferred columns would inadvertently be set up
  for database load on the next object-wide unexpire, when the object
  were merged into the session with `session.merge(obj, load=False)`.
  References: [#3488](https://www.sqlalchemy.org/trac/ticket/3488)
- Further continuing on the common MySQL exception case of
  a savepoint being cancelled first covered in [#2696](https://www.sqlalchemy.org/trac/ticket/2696),
  the failure mode in which the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is placed when a
  SAVEPOINT vanishes before rollback has been improved to allow the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to still function outside of that savepoint.
  It is assumed that the savepoint operation failed and was cancelled.
  See also
  [Improved Session state when a SAVEPOINT is cancelled by the database](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3680)
  References: [#3680](https://www.sqlalchemy.org/trac/ticket/3680)
- Fixed bug where a newly inserted instance that is rolled back
  would still potentially cause persistence conflicts on the next
  transaction, because the instance would not be checked that it
  was expired.   This fix will resolve a large class of cases that
  erroneously cause the “New instance with identity X conflicts with
  persistent instance Y” error.
  See also
  [Erroneous “new instance X conflicts with persistent instance Y” flush errors fixed](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3677)
  References: [#3677](https://www.sqlalchemy.org/trac/ticket/3677)
- An improvement to the workings of [Query.correlate()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.correlate) such
  that when a “polymorphic” entity is used which represents a straight
  join of several tables, the statement will ensure that all the
  tables within the join are part of what’s correlating.
  See also
  [Improvements to the Query.correlate method with polymorphic entities](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3662)
  References: [#3662](https://www.sqlalchemy.org/trac/ticket/3662)
- Fixed bug which would cause an eagerly loaded many-to-one attribute
  to not be loaded, if the joined eager load were from a row where the
  same entity were present multiple times, some calling for the attribute
  to be eagerly loaded and others not.  The logic here is revised to
  take in the attribute even though a different loader path has
  handled the parent entity already.
  See also
  [Joined eager loading where the same entity is present multiple times in one row](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3431)
  References: [#3431](https://www.sqlalchemy.org/trac/ticket/3431)
- A refinement to the logic which adds columns to the resulting SQL when
  [Query.distinct()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.distinct) is combined with [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) such
  that columns which are already present will not be added
  a second time, even if they are labeled with a different name.
  Regardless of this change, the extra columns added to the SQL have
  never been returned in the final result, so this change only impacts
  the string form of the statement as well as its behavior when used in
  a Core execution context.   Additionally, columns are no longer added
  when the DISTINCT ON format is used, provided the query is not
  wrapped inside a subquery due to joined eager loading.
  See also
  [Columns no longer added redundantly with DISTINCT + ORDER BY](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3641)
  References: [#3641](https://www.sqlalchemy.org/trac/ticket/3641)
- Fixed issue where two same-named relationships that refer to
  a base class and a concrete-inherited subclass would raise an error
  if those relationships were set up using “backref”, while setting up the
  identical configuration using relationship() instead with the conflicting
  names would succeed, as is allowed in the case of a concrete mapping.
  See also
  [Same-named backrefs will not raise an error when applied to concrete inheritance subclasses](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3630)
  References: [#3630](https://www.sqlalchemy.org/trac/ticket/3630)
- The [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) method now tracks pending objects by
  primary key before emitting an INSERT, and merges distinct objects with
  duplicate primary keys together as they are encountered, which is
  essentially semi-deterministic at best.   This behavior
  matches what happens already with persistent objects.
  See also
  [Session.merge resolves pending conflicts the same as persistent](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3601)
  References: [#3601](https://www.sqlalchemy.org/trac/ticket/3601)
- Fixed bug where the “single table inheritance” criteria would be
  added onto the end of a query in some inappropriate situations, such
  as when querying from an exists() of a single-inheritance subclass.
  See also
  [Further Fixes to single-table inheritance querying](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3582)
  References: [#3582](https://www.sqlalchemy.org/trac/ticket/3582)
- Added a new type-level modifier [TypeEngine.evaluates_none()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.evaluates_none)
  which indicates to the ORM that a positive set of None should be
  persisted as the value NULL, instead of omitting the column from
  the INSERT statement.  This feature is used both as part of the
  implementation for [#3514](https://www.sqlalchemy.org/trac/ticket/3514) as well as a standalone feature
  available on any type.
  See also
  [New options allowing explicit persistence of NULL over a default](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3250)
  References: [#3250](https://www.sqlalchemy.org/trac/ticket/3250)
- Internal calls to “bookkeeping” functions within
  [Session.bulk_save_objects()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects) and related bulk methods have
  been scaled back to the extent that this functionality is not
  currently used, e.g. checks for column default values to be
  fetched after an INSERT or UPDATE statement.
  References: [#3526](https://www.sqlalchemy.org/trac/ticket/3526)
- Additional fixes have been made regarding the value of `None`
  in conjunction with the PostgreSQL [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) type.  When
  the [JSON.none_as_null](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.params.none_as_null) flag is left at its default
  value of `False`, the ORM will now correctly insert the JSON
  “‘null’” string into the column whenever the value on the ORM
  object is set to the value `None` or when the value `None`
  is used with [Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings),
  **including** if the column has a default or server default on it.
  See also
  [JSON “null” is inserted as expected with ORM operations, omitted when not present](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3514)
  [New options allowing explicit persistence of NULL over a default](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3250)
  References: [#3514](https://www.sqlalchemy.org/trac/ticket/3514)

### engine

- Added connection pool events `ConnectionEvents.close()`,
  `ConnectionEvents.detach()`,
  `ConnectionEvents.close_detached()`.
- All string formatting of bound parameter sets and result rows for
  logging, exception, and  `repr()` purposes now truncate very large
  scalar values within each collection, including an
  “N characters truncated”
  notation, similar to how the display for large multiple-parameter sets
  are themselves truncated.
  See also
  [Large parameter and row values are now truncated in logging and exception displays](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2837)
  References: [#2837](https://www.sqlalchemy.org/trac/ticket/2837)
- Multi-tenancy schema translation for [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects is added.
  This supports the use case of an application that uses the same set of
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects in many schemas, such as schema-per-user.
  A new execution option
  [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map) is
  added.
  See also
  [Multi-Tenancy Schema Translation for Table objects](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2685)
  References: [#2685](https://www.sqlalchemy.org/trac/ticket/2685)
- Added a new entrypoint system to the engine to allow “plugins” to
  be stated in the query string for a URL.   Custom plugins can
  be written which will be given the chance up front to alter and/or
  consume the engine’s URL and keyword arguments, and then at engine
  create time will be given the engine itself to allow additional
  modifications or event registration.  Plugins are written as a
  subclass of [CreateEnginePlugin](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CreateEnginePlugin); see that class for
  details.
  References: [#3536](https://www.sqlalchemy.org/trac/ticket/3536)

### sql

- Added TABLESAMPLE support via the new [FromClause.tablesample()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.tablesample)
  method and standalone function.  Pull request courtesy Ilja Everilä.
  See also
  [Support for TABLESAMPLE](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3718)
  References: [#3718](https://www.sqlalchemy.org/trac/ticket/3718)
- Added support for ranges in window functions, using the
  [over.range_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over.params.range_) and
  [over.rows](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over.params.rows) parameters.
  See also
  [Support for RANGE and ROWS specification within window functions](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3049)
  References: [#3049](https://www.sqlalchemy.org/trac/ticket/3049)
- Implemented reflection of CHECK constraints for SQLite and PostgreSQL.
  This is available via the new inspector method
  [Inspector.get_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints) as well as when reflecting
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects in the form of [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint)
  objects present in the constraints collection.  Pull request courtesy
  Alex Grönholm.
- New [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) and
  [ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) operators; pull request
  courtesy Sebastian Bank.
  See also
  [Support for IS DISTINCT FROM and IS NOT DISTINCT FROM](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-is-distinct-from)
- Added a hook in `DDLCompiler.visit_create_table()` called
  `DDLCompiler.create_table_suffix()`, allowing custom dialects
  to add keywords after the “CREATE TABLE” clause.  Pull request
  courtesy Mark Sandan.
- Negative integer indexes are now accommodated by rows
  returned from a `ResultProxy`.  Pull request courtesy
  Emanuele Gaifas.
  See also
  [Negative integer indexes accommodated by Core result rows](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-gh-231)
- Added [Select.lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.lateral) and related constructs to allow
  for the SQL standard LATERAL keyword, currently only supported
  by PostgreSQL.
  See also
  [Support for the SQL LATERAL keyword](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2857)
  References: [#2857](https://www.sqlalchemy.org/trac/ticket/2857)
- Added support for rendering “FULL OUTER JOIN” to both Core and ORM.
  Pull request courtesy Stefan Urbanek.
  See also
  [Core and ORM support for FULL OUTER JOIN](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-1957)
  References: [#1957](https://www.sqlalchemy.org/trac/ticket/1957)
- CTE functionality has been expanded to support all DML, allowing
  INSERT, UPDATE, and DELETE statements to both specify their own
  WITH clause, as well as for these statements themselves to be
  CTE expressions when they include a RETURNING clause.
  See also
  [CTE Support for INSERT, UPDATE, DELETE](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2551)
  References: [#2551](https://www.sqlalchemy.org/trac/ticket/2551)
- Added support for PEP-435-style enumerated classes, namely
  Python 3’s `enum.Enum` class but also including compatible
  enumeration libraries, to the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatype.
  The [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatype now also performs in-Python validation
  of incoming values, and adds an option to forego creating the
  CHECK constraint [Enum.create_constraint](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.create_constraint).
  Pull request courtesy Alex Grönholm.
  See also
  [Support for Python’s native enum type and compatible forms](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3292)
  [The Enum type now does in-Python validation of values](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3095)
  References: [#3095](https://www.sqlalchemy.org/trac/ticket/3095), [#3292](https://www.sqlalchemy.org/trac/ticket/3292)
- A deep improvement to the recently added [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns)
  method, and its interaction with result-row processing, now allows
  the columns passed to the method to be positionally matched with the
  result columns in the statement, rather than matching on name alone.
  The advantage to this includes that when linking a textual SQL statement
  to an ORM or Core table model, no system of labeling or de-duping of
  common column names needs to occur, which also means there’s no need
  to worry about how label names match to ORM columns and so-forth.  In
  addition, the `ResultProxy` has been further enhanced to
  map column and string keys to a row with greater precision in some
  cases.
  See also
  [ResultSet column matching enhancements; positional column setup for textual SQL](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3501) - feature overview
  [TextClause.columns() will match columns positionally, not by name, when passed positionally](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#behavior-change-3501) - backwards compatibility remarks
  References: [#3501](https://www.sqlalchemy.org/trac/ticket/3501)
- Added a new type to core [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON).  This is the
  base of the PostgreSQL [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) type as well as that
  of the new [JSON](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.JSON) type, so that a PG/MySQL-agnostic
  JSON column may be used.  The type features basic index and path
  searching support.
  See also
  [JSON support added to Core](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3619)
  References: [#3619](https://www.sqlalchemy.org/trac/ticket/3619)
- Added support for “set-aggregate” functions of the form
  `<function> WITHIN GROUP (ORDER BY <criteria>)`, using the
  method [FunctionElement.within_group()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.within_group).  A series of common
  set-aggregate functions with return types derived from the set have
  been added. This includes functions like [percentile_cont](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percentile_cont),
  [dense_rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.dense_rank) and others.
  See also
  [New Function features, “WITHIN GROUP”, array_agg and set aggregate functions](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3132)
  References: [#1370](https://www.sqlalchemy.org/trac/ticket/1370)
- Added support for the SQL-standard function [array_agg](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg),
  which automatically returns an [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) of the correct type
  and supports index / slice operations, as well as
  [array_agg()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array_agg), which returns a [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY)
  with additional comparison features.   As arrays are only
  supported on PostgreSQL at the moment, only actually works on
  PostgreSQL.  Also added a new construct
  [aggregate_order_by](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.aggregate_order_by) in support of PG’s
  “ORDER BY” extension.
  See also
  [New Function features, “WITHIN GROUP”, array_agg and set aggregate functions](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3132)
  References: [#3132](https://www.sqlalchemy.org/trac/ticket/3132)
- Added a new type to core [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY).  This is the
  base of the PostgreSQL [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) type, and is now part of Core
  to begin supporting various SQL-standard array-supporting features
  including some functions and eventual support for native arrays
  on other databases that have an “array” concept, such as DB2 or Oracle.
  Additionally, new operators [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) and
  [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_) have been added.  These support not just
  array constructs on PostgreSQL, but also subqueries that are usable
  on MySQL (but sadly not on PostgreSQL).
  See also
  [Array support added to Core; new ANY and ALL operators](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3516)
  References: [#3516](https://www.sqlalchemy.org/trac/ticket/3516)
- The system by which a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) considers itself to be an
  “auto increment” column has been changed, such that autoincrement
  is no longer implicitly enabled for a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that has a
  composite primary key.  In order to accommodate being able to enable
  autoincrement for a composite PK member column while at the same time
  maintaining SQLAlchemy’s long standing behavior of enabling
  implicit autoincrement for a single integer primary key, a third
  state has been added to the [Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement) parameter
  `"auto"`, which is now the default.
  See also
  [The .autoincrement directive is no longer implicitly enabled for a composite primary key column](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3216)
  [No more generation of an implicit KEY for composite primary key w/ AUTO_INCREMENT](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-mysql-3216)
  References: [#3216](https://www.sqlalchemy.org/trac/ticket/3216)
- `FromClause.count()` is deprecated.  This function makes use of
  an arbitrary column in the table and is not reliable; for Core use,
  `func.count()` should be preferred.
  References: [#3724](https://www.sqlalchemy.org/trac/ticket/3724)
- Fixed an assertion that would raise somewhat inappropriately
  if a [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) were associated with a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that
  is associated with a lower-case-t [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause); the
  association should be ignored for the purposes of associating
  the index with a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
  References: [#3616](https://www.sqlalchemy.org/trac/ticket/3616)
- The [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) construct is now a fully fledged Core
  expression element which is late-evaluated at compile time.  Previously,
  the function was only a conversion function which would handle different
  expression inputs by returning either a [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label) of a column-oriented
  expression or a copy of a given [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) object,
  which in particular prevented the operation from being logically
  maintained when an ORM-level expression transformation would convert
  a column to a bound parameter (e.g. for lazy loading).
  See also
  [The type_coerce function is now a persistent SQL element](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3531)
  References: [#3531](https://www.sqlalchemy.org/trac/ticket/3531)
- The [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) type extender will now work in conjunction
  with a [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType) implementation, typically [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum)
  or [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) with regards to ensuring that the per-table
  events are propagated from the implementation type to the outer type.
  These events are used
  to ensure that the constraints or PostgreSQL types (e.g. ENUM)
  are correctly created (and possibly dropped) along with the parent
  table.
  See also
  [TypeDecorator now works with Enum, Boolean, “schema” types automatically](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2919)
  References: [#2919](https://www.sqlalchemy.org/trac/ticket/2919)
- The behavior of the [union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union) construct and related constructs
  such as [Query.union()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.union) now handle the case where the embedded
  SELECT statements need to be parenthesized due to the fact that they
  include LIMIT, OFFSET and/or ORDER BY.   These queries **do not work
  on SQLite**, and will fail on that backend as they did before, but
  should now work on all other backends.
  See also
  [A UNION or similar of SELECTs with LIMIT/OFFSET/ORDER BY now parenthesizes the embedded selects](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2528)
  References: [#2528](https://www.sqlalchemy.org/trac/ticket/2528)

### schema

- The default generation functions passed to [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
  are now run through “update_wrapper”, or an equivalent function
  if a callable non-function is passed, so that introspection tools
  preserve the name and docstring of the wrapped function.  Pull
  request courtesy hsum.

### postgresql

- Added support for PostgreSQL’s INSERT..ON CONFLICT using a new
  PostgreSQL-specific [Insert](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert) object.
  Pull request and extensive efforts here by Robin Thomas.
  See also
  [Support for INSERT..ON CONFLICT (DO UPDATE | DO NOTHING)](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3529)
  References: [#3529](https://www.sqlalchemy.org/trac/ticket/3529)
- The DDL for DROP INDEX will emit “CONCURRENTLY” if the
  `postgresql_concurrently` flag is set upon the
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) and if the database in use is detected as
  PostgreSQL version 9.2 or greater.   For CREATE INDEX, database
  version detection is also added which will omit the clause if
  PG version is less than 8.2.  Pull request courtesy Iuri de Silvio.
- Added new parameter `PGInspector.get_view_names.include`,
  allowing specification for what kinds of views should be returned.
  Currently “plain” and “materialized” views are included.  Pull
  request courtesy Sebastian Bank.
  References: [#3588](https://www.sqlalchemy.org/trac/ticket/3588)
- Added `postgresql_tablespace` as an argument to [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index)
  to allow specification of TABLESPACE for an index in PostgreSQL.
  Complements the same-named parameter on [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).  Pull
  request courtesy Benjamin Bertrand.
  References: [#3720](https://www.sqlalchemy.org/trac/ticket/3720)
- Added new parameter
  [GenerativeSelect.with_for_update.key_share](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.key_share), which
  will render the `FOR NO KEY UPDATE` version of `FOR UPDATE`
  and `FOR KEY SHARE` instead of `FOR SHARE`
  on the PostgreSQL backend.  Pull request courtesy Sergey Skopin.
- Added new parameter
  [GenerativeSelect.with_for_update.skip_locked](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.skip_locked), which
  will render the `SKIP LOCKED` phrase for a `FOR UPDATE` or
  `FOR SHARE` lock on the PostgreSQL and Oracle backends.  Pull
  request courtesy Jack Zhou.
- Added a new dialect for the PyGreSQL PostgreSQL dialect.  Thanks
  to Christoph Zwerschke and Kaolin Imago Fire for their efforts.
- Added a new constant `JSON.NULL`, indicating
  that the JSON NULL value should be used for a value
  regardless of other settings.
  See also
  [New JSON.NULL Constant Added](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3514-jsonnull)
  References: [#3514](https://www.sqlalchemy.org/trac/ticket/3514)
- The `sqlalchemy.dialects.postgres` module, long deprecated, is
  removed; this has emitted a warning for many years and projects
  should be calling upon `sqlalchemy.dialects.postgresql`.
  Engine URLs of the form `postgres://` will still continue to function,
  however.
- Added support for reflecting the source of materialized views
  to the PostgreSQL version of the [Inspector.get_view_definition()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_definition)
  method.
  References: [#3587](https://www.sqlalchemy.org/trac/ticket/3587)
- The use of a [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) object that refers
  to a [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) or [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) subtype
  will now emit the expected “CREATE TYPE” and “DROP TYPE” DDL when
  the type is used within a “CREATE TABLE” or “DROP TABLE”.
  See also
  [ARRAY with ENUM will now emit CREATE TYPE for the ENUM](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-2729)
  References: [#2729](https://www.sqlalchemy.org/trac/ticket/2729)
- The “hashable” flag on special datatypes such as [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY),
  [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE) is now
  set to False, which allows these types to be fetchable in ORM
  queries that include entities within the row.
  See also
  [Changes regarding “unhashable” types, impacts deduping of ORM rows](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3499)
  [ARRAY and JSON types now correctly specify “unhashable”](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3499-postgresql)
  References: [#3499](https://www.sqlalchemy.org/trac/ticket/3499)
- The PostgreSQL [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) type now supports multidimensional
  indexed access, e.g. expressions such as `somecol[5][6]` without
  any need for explicit casts or type coercions, provided
  that the [ARRAY.dimensions](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.params.dimensions) parameter is set to the
  desired number of dimensions.
  See also
  [Correct SQL Types are Established from Indexed Access of ARRAY, JSON, HSTORE](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3503)
  References: [#3487](https://www.sqlalchemy.org/trac/ticket/3487)
- The return type for the [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB)
  when using indexed access has been fixed to work like PostgreSQL itself,
  and returns an expression that itself is of type [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON)
  or [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB).  Previously, the accessor would return
  [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType) which disallowed subsequent JSON-like operators to be
  used.
  See also
  [Correct SQL Types are Established from Indexed Access of ARRAY, JSON, HSTORE](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3503)
  References: [#3503](https://www.sqlalchemy.org/trac/ticket/3503)
- The [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON), [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) and
  [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE) datatypes now allow full control over the
  return type from an indexed textual access operation, either `column[someindex].astext`
  for a JSON type or `column[someindex]` for an HSTORE type,
  via the [JSON.astext_type](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.params.astext_type) and
  [HSTORE.text_type](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE.params.text_type) parameters.
  See also
  [Correct SQL Types are Established from Indexed Access of ARRAY, JSON, HSTORE](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3503)
  References: [#3503](https://www.sqlalchemy.org/trac/ticket/3503)
- The [Comparator.astext](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext) modifier no longer
  calls upon [ColumnElement.cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast) implicitly, as PG’s JSON/JSONB
  types allow cross-casting between each other as well.  Code that
  makes use of [ColumnElement.cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast) on JSON indexed access,
  e.g. `col[someindex].cast(Integer)`, will need to be changed
  to call [Comparator.astext](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext) explicitly.
  See also
  [The JSON cast() operation now requires .astext is called explicitly](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3503-cast)
  References: [#3503](https://www.sqlalchemy.org/trac/ticket/3503)

### mysql

- Added support for “autocommit” on MySQL drivers, via the
  AUTOCOMMIT isolation level setting.  Pull request courtesy
  Roman Podoliaka.
  See also
  [Added support for AUTOCOMMIT “isolation level”](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3332)
  References: [#3332](https://www.sqlalchemy.org/trac/ticket/3332)
- Added [JSON](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.JSON) for MySQL 5.7.  The JSON type provides
  persistence of JSON values in MySQL as well as basic operator support
  of “getitem” and “getpath”, making use of the `JSON_EXTRACT`
  function in order to refer to individual paths in a JSON structure.
  See also
  [MySQL JSON Support](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3547)
  References: [#3547](https://www.sqlalchemy.org/trac/ticket/3547)
- The MySQL dialect no longer generates an extra “KEY” directive when
  generating CREATE TABLE DDL for a table using InnoDB with a
  composite primary key with AUTO_INCREMENT on a column that isn’t the
  first column;  to overcome InnoDB’s limitation here, the PRIMARY KEY
  constraint is now generated with the AUTO_INCREMENT column placed
  first in the list of columns.
  See also
  [No more generation of an implicit KEY for composite primary key w/ AUTO_INCREMENT](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-mysql-3216)
  [The .autoincrement directive is no longer implicitly enabled for a composite primary key column](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3216)
  References: [#3216](https://www.sqlalchemy.org/trac/ticket/3216)

### sqlite

- The SQLite dialect now reflects ON UPDATE and ON DELETE phrases
  within foreign key constraints.  Pull request courtesy
  Michal Petrucha.
- The SQLite dialect now reflects the names of primary key constraints.
  Pull request courtesy Diana Clarke.
  See also
  [Reflection of the name of PRIMARY KEY constraints](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3629)
  References: [#3629](https://www.sqlalchemy.org/trac/ticket/3629)
- Added support to the SQLite dialect for the
  [Inspector.get_schema_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_schema_names) method to work with SQLite;
  pull request courtesy Brian Van Klaveren.  Also repaired support
  for creation of indexes with schemas as well as reflection of
  foreign key constraints in schema-bound tables.
  See also
  [Improved Support for Remote Schemas](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-sqlite-schemas)
- The workaround for right-nested joins on SQLite, where they are rewritten
  as subqueries in order to work around SQLite’s lack of support for this
  syntax, is lifted when SQLite version 3.7.16 or greater is detected.
  See also
  [Right-nested join workaround lifted for SQLite version 3.7.16](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3634)
  References: [#3634](https://www.sqlalchemy.org/trac/ticket/3634)
- The workaround for SQLite’s unexpected delivery of column names as
  `tablename.columnname` for some kinds of queries is now disabled
  when SQLite version 3.10.0 or greater is detected.
  See also
  [Dotted column names workaround lifted for SQLite version 3.10.0](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3633)
  References: [#3633](https://www.sqlalchemy.org/trac/ticket/3633)

### mssql

- The `mssql_clustered` flag available on [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint),
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint), [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) now defaults to
  `None`, and can be set to False which will render the NONCLUSTERED
  keyword in particular for a primary key, allowing a different index to
  be used as “clustered”. Pull request courtesy Saulius Žemaitaitis.
- Added basic isolation level support to the SQL Server dialects
  via [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) and
  [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
  parameters.
  See also
  [Added transaction isolation level support for SQL Server](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3534)
  References: [#3534](https://www.sqlalchemy.org/trac/ticket/3534)
- The `legacy_schema_aliasing` flag, introduced in version 1.0.5
  as part of [#3424](https://www.sqlalchemy.org/trac/ticket/3424) to allow disabling of the MSSQL dialect’s
  attempts to create aliases for schema-qualified tables, now defaults
  to False; the old behavior is now disabled unless explicitly turned on.
  See also
  [The legacy_schema_aliasing flag is now set to False](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3434)
  References: [#3434](https://www.sqlalchemy.org/trac/ticket/3434)
- Adjustments to the mxODBC dialect to make use of the `BinaryNull`
  symbol when appropriate in conjunction with the `VARBINARY`
  data type.  Pull request courtesy Sheila Allen.
- Fixed issue where the SQL Server dialect would reflect a string-
  or other variable-length column type with unbounded length
  by assigning the token `"max"` to the
  length attribute of the string.   While using the `"max"` token
  explicitly is supported by the SQL Server dialect, it isn’t part
  of the normal contract of the base string types, and instead the
  length should just be left as None.   The dialect now assigns the
  length to None on reflection of the type so that the type behaves
  normally in other contexts.
  See also
  [String / varlength types no longer represent “max” explicitly on reflection](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3504)
  References: [#3504](https://www.sqlalchemy.org/trac/ticket/3504)

### misc

- Added [MutableSet](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableSet) and [MutableList](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList) helper classes
  to the [Mutation Tracking](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html) extension.  Pull request courtesy
  Jeong YunWon.
  References: [#3297](https://www.sqlalchemy.org/trac/ticket/3297)
- The docstring specified on a hybrid property or method is now honored
  at the class level, allowing it to work with tools like Sphinx
  autodoc.  The mechanics here necessarily involve some wrapping of
  expressions to occur for hybrid properties, which may cause them
  to appear differently using introspection.
  See also
  [Hybrid properties and methods now propagate the docstring as well as .info](https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#change-3653)
  References: [#3653](https://www.sqlalchemy.org/trac/ticket/3653)
- The unsupported Sybase dialect now raises `NotImplementedError`
  when attempting to compile a query that includes “offset”; Sybase
  has no straightforward “offset” feature.
  References: [#2278](https://www.sqlalchemy.org/trac/ticket/2278)
