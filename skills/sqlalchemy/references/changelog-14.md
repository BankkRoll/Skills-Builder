# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# 2.0 Changelog

## 2.0.47

no release date

## 2.0.46

Released: January 21, 2026

### typing

- Fixed typing issues where ORM mapped classes and aliased entities could not
  be used as keys in result row mappings or as join targets in select
  statements. Patterns such as `row._mapping[User]`,
  `row._mapping[aliased(User)]`, `row._mapping[with_polymorphic(...)]`
  (rejected by both mypy and Pylance), and `.join(aliased(User))`
  (rejected by Pylance) are documented and fully supported at runtime but
  were previously rejected by type checkers. The type definitions for
  `_KeyType` and `_FromClauseArgument` have been updated to
  accept these ORM entity types.
  References: [#13075](https://www.sqlalchemy.org/trac/ticket/13075)

### postgresql

- Fixed issue where PostgreSQL JSONB operators
  [Comparator.path_match()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB.Comparator.path_match) and
  [Comparator.path_exists()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB.Comparator.path_exists) were applying incorrect
  `VARCHAR` casts to the right-hand side operand when used with newer
  PostgreSQL drivers such as psycopg. The operators now indicate the
  right-hand type as `JSONPATH`, which currently results in no casting
  taking place, but is also compatible with explicit casts if the
  implementation were require it at a later point.
  References: [#13059](https://www.sqlalchemy.org/trac/ticket/13059)
- Fixed regression in PostgreSQL dialect where JSONB subscription syntax
  would generate incorrect SQL for [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) expressions returning JSONB,
  causing syntax errors. The dialect now properly wraps cast expressions in
  parentheses when using the `[]` subscription syntax, generating
  `(CAST(...))[index]` instead of `CAST(...)[index]` to comply with
  PostgreSQL syntax requirements. This extends the fix from [#12778](https://www.sqlalchemy.org/trac/ticket/12778)
  which addressed the same issue for function calls.
  References: [#13067](https://www.sqlalchemy.org/trac/ticket/13067)
- Improved the foreign key reflection regular expression pattern used by the
  PostgreSQL dialect to be more permissive in matching identifier characters,
  allowing it to correctly handle unicode characters in table and column
  names. This change improves compatibility with PostgreSQL variants such as
  CockroachDB that may use different quoting patterns in combination with
  unicode characters in their identifiers.  Pull request courtesy Gord
  Thompson.

### mariadb

- Fixed the SQL compilation for the mariadb sequence “NOCYCLE” keyword that
  is to be emitted when the [Sequence.cycle](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.cycle) parameter is set to
  False on a [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence).  Pull request courtesy Diego Dupin.
  References: [#13070](https://www.sqlalchemy.org/trac/ticket/13070)

### sqlite

- Fixed issue in the aiosqlite driver where SQLAlchemy’s setting of
  aiosqlite’s worker thread to “daemon” stopped working because the aiosqlite
  architecture moved the location of the worker thread in version 0.22.0.
  This “daemon” flag is necessary so that a program is able to exit if the
  SQLite connection itself was not explicitly closed, which is particularly
  likely with SQLAlchemy as it maintains SQLite connections in a connection
  pool.  While it’s perfectly fine to call [AsyncEngine.dispose()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncEngine.dispose)
  before program exit, this is not historically or technically necessary for
  any driver of any known backend, since a primary feature of relational
  databases is durability.  The change also implements support for
  “terminate” with aiosqlite when using version version 0.22.1 or greater,
  which implements a sync `.stop()` method.
  References: [#13039](https://www.sqlalchemy.org/trac/ticket/13039)

### mssql

- Added support for the `IF EXISTS` clause when dropping indexes on SQL
  Server 2016 (13.x) and later versions. The [DropIndex.if_exists](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropIndex.params.if_exists)
  parameter is now honored by the SQL Server dialect, allowing conditional
  index drops that will not raise an error if the index does not exist.
  Pull request courtesy Edgar Ramírez Mondragón.
  References: [#13045](https://www.sqlalchemy.org/trac/ticket/13045)

## 2.0.45

Released: December 9, 2025

### orm

- Fixed issue where calling [Mapper.add_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.add_property) within mapper event
  hooks such as [MapperEvents.instrument_class()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.instrument_class),
  [MapperEvents.after_mapper_constructed()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.after_mapper_constructed), or
  [MapperEvents.before_mapper_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_mapper_configured) would raise an
  `AttributeError` because the mapper’s internal property collections were
  not yet initialized. The [Mapper.add_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.add_property) method now handles
  early-stage property additions correctly, allowing properties including
  column properties, deferred columns, and relationships to be added during
  mapper initialization events.  Pull request courtesy G Allajmi.
  References: [#12858](https://www.sqlalchemy.org/trac/ticket/12858)
- Fixed issue in Python 3.14 where dataclass transformation would fail when
  a mapped class using [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) included a
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) referencing a class that was not available at
  runtime (e.g., within a `TYPE_CHECKING` block). This occurred when using
  Python 3.14’s [PEP 649](https://peps.python.org/pep-0649/) deferred annotations feature, which is the
  default behavior without a `from __future__ import annotations`
  directive.
  References: [#12952](https://www.sqlalchemy.org/trac/ticket/12952)

### examples

- Fixed the “short_selects” performance example where the cache was being
  used in all the examples, making it impossible to compare performance with
  and without the cache.   Less important comparisons like “lambdas” and
  “baked queries” have been removed.

### sql

- Some improvements to the [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params) method to
  replace bound parameters in a query were made, however the ultimate issue
  in [#12915](https://www.sqlalchemy.org/trac/ticket/12915) involving ORM [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) cannot be fixed fully
  until 2.1, where the method is being rewritten to work without relying on
  Core cloned traversal.
  References: [#12915](https://www.sqlalchemy.org/trac/ticket/12915)
- Fixed issue where using the [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) operator with a
  nested [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect) statement (e.g. an `INTERSECT` of
  `UNION` queries) would raise a `NotImplementedError` when the
  nested compound select was the first argument to the outer compound select.
  The `_scalar_type()` internal method now properly handles nested compound
  selects.
  References: [#12987](https://www.sqlalchemy.org/trac/ticket/12987)

### typing

- Fixed typing issue where [Select.with_for_update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update) would not support
  lists of ORM entities or other FROM clauses in the
  [Select.with_for_update.of](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update.params.of) parameter. Pull request courtesy
  Shamil.
  References: [#12730](https://www.sqlalchemy.org/trac/ticket/12730)
- Fixed typing issue where [coalesce](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.coalesce) would not return the correct
  return type when a nullable form of that argument were passed, even though
  this function is meant to select the non-null entry among possibly null
  arguments.  Pull request courtesy Yannick PÉROUX.

### postgresql

- Added support for reflection of collation in types for PostgreSQL.
  The `collation` will be set only if different from the default
  one for the type.
  Pull request courtesy Denis Laxalde.
  References: [#6511](https://www.sqlalchemy.org/trac/ticket/6511)
- Fixed issue where PostgreSQL dialect options such as `postgresql_include`
  on [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) and [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) were
  rendered in the wrong position when combined with constraint deferrability
  options like `deferrable=True`. Pull request courtesy G Allajmi.
  References: [#12867](https://www.sqlalchemy.org/trac/ticket/12867)
- Fixed the structure of the SQL string used for the
  [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) feature when an explicit sequence with
  `nextval()` is used. The SQL function invocation for the sequence has
  been moved from being rendered inline within each tuple inside of VALUES to
  being rendered once in the SELECT that reads from VALUES. This change
  ensures the function is invoked in the correct order as rows are processed,
  rather than assuming PostgreSQL will execute inline function calls within
  VALUES in a particular order. While current PostgreSQL versions appear to
  handle the previous approach correctly, the database does not guarantee
  this behavior for future versions.
  References: [#13015](https://www.sqlalchemy.org/trac/ticket/13015)

### mysql

- Added support for MySQL 8.0.1 + `FOR SHARE` to be emitted for the
  [Select.with_for_update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update) method, which offers compatibility with
  `NOWAIT` and `SKIP LOCKED`.  The new syntax is used only for MySQL when
  version 8.0.1 or higher is detected. Pull request courtesy JetDrag.
  References: [#12964](https://www.sqlalchemy.org/trac/ticket/12964)

### sqlite

- A series of improvements have been made for reflection of CHECK constraints
  on SQLite. The reflection logic now correctly handles table names
  containing the strings “CHECK” or “CONSTRAINT”, properly supports all four
  SQLite identifier quoting styles (double quotes, single quotes, brackets,
  and backticks) for constraint names, and accurately parses CHECK constraint
  expressions containing parentheses within string literals using balanced
  parenthesis matching with string context tracking.    Big thanks to
  GruzdevAV for new test cases and implementation ideas.
  References: [#12924](https://www.sqlalchemy.org/trac/ticket/12924)
- Fixed issue where SQLite dialect would fail to reflect constraint names
  that contained uppercase letters or other characters requiring quoting. The
  regular expressions used to parse primary key, foreign key, and unique
  constraint names from the `CREATE TABLE` statement have been updated to
  properly handle both quoted and unquoted constraint names.
  References: [#12954](https://www.sqlalchemy.org/trac/ticket/12954)

### tests

- A noxfile.py has been added to allow testing with nox.  This is a direct
  port of 2.1’s move to nox, however leaves the tox.ini file in place and
  retains all test documentation in terms of tox.   Version 2.1 will move to
  nox fully, including deprecation warnings for tox and new testing
  documentation.

## 2.0.44

Released: October 10, 2025

### platform

- Unblocked automatic greenlet installation for Python 3.14 now that
  there are greenlet wheels on pypi for python 3.14.

### orm

- The way ORM Annotated Declarative interprets Python [PEP 695](https://peps.python.org/pep-0695/) type aliases
  in `Mapped[]` annotations has been refined to expand the lookup scheme. A
  [PEP 695](https://peps.python.org/pep-0695/) type can now be resolved based on either its direct presence in
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) or its immediate resolved
  value, as long as a recursive lookup across multiple [PEP 695](https://peps.python.org/pep-0695/) types is
  not required for it to resolve. This change reverses part of the
  restrictions introduced in 2.0.37 as part of [#11955](https://www.sqlalchemy.org/trac/ticket/11955), which
  deprecated (and disallowed in 2.1) the ability to resolve any [PEP 695](https://peps.python.org/pep-0695/)
  type that was not explicitly present in
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map). Recursive lookups of
  [PEP 695](https://peps.python.org/pep-0695/) types remains deprecated in 2.0 and disallowed in version 2.1,
  as do implicit lookups of `NewType` types without an entry in
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map).
  Additionally, new support has been added for generic [PEP 695](https://peps.python.org/pep-0695/) aliases that
  refer to [PEP 593](https://peps.python.org/pep-0593/) `Annotated` constructs containing
  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) configurations. See the sections below for
  examples.
  See also
  [Support for Type Alias Types (defined by PEP 695) and NewType](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-type-map-pep695-types)
  [Mapping Whole Column Declarations to Generic Python Types](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-generic-pep593)
  References: [#12829](https://www.sqlalchemy.org/trac/ticket/12829)
- Fixed a caching issue where [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) would
  incorrectly reuse cached bound parameter values when used with
  [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect) constructs such as [union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union). The
  issue was caused by the cache key for compound selects not including the
  execution options that are part of the [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable) base class,
  which [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) uses to apply its criteria
  dynamically. The fix ensures that compound selects and other executable
  constructs properly include execution options in their cache key traversal.
  References: [#12905](https://www.sqlalchemy.org/trac/ticket/12905)

### engine

- Implemented initial support for free-threaded Python by adding new tests
  and reworking the test harness to include Python 3.13t and Python 3.14t in
  test runs. Two concurrency issues have been identified and fixed: the first
  involves initialization of the `.c` collection on a `FromClause`, a
  continuation of [#12302](https://www.sqlalchemy.org/trac/ticket/12302), where an optional mutex under
  free-threading is added; the second involves synchronization of the pool
  “first_connect” event, which first received thread synchronization in
  [#2964](https://www.sqlalchemy.org/trac/ticket/2964), however under free-threading the creation of the mutex
  itself runs under the same free-threading mutex. Support for free-threaded
  wheels on Pypi is implemented as well within the 2.1 series only.  Initial
  pull request and test suite courtesy Lysandros Nikolaou.
  References: [#12881](https://www.sqlalchemy.org/trac/ticket/12881)

### sql

- Improved the implementation of [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning) to use more
  robust logic in setting up the `.c` collection of a derived statement
  such as a CTE.  This fixes issues related to RETURNING clauses that feature
  expressions based on returned columns with or without qualifying labels.
  References: [#12271](https://www.sqlalchemy.org/trac/ticket/12271)

### schema

- Fixed issue where [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) did not forward
  dialect-specific keyword arguments to the `Inspector`
  methods, causing options like `oracle_resolve_synonyms` to be ignored
  during reflection. The method now ensures that all extra kwargs passed to
  [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) are forwarded to
  `Inspector.get_table_names()` and related reflection methods.
  Pull request courtesy Lukáš Kožušník.
  References: [#12884](https://www.sqlalchemy.org/trac/ticket/12884)

### typing

- Fixed typing bug where the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method advertised that
  it would return a [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) if given an insert/update/delete
  statement.  This is not the general case as several flavors of ORM
  insert/update do not actually yield a [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) which cannot
  be differentiated at the typing overload level, so the method now yields
  [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) in all cases.  For those cases where
  [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) is known to be returned and the `.rowcount`
  attribute is required, please use `typing.cast()`.
  References: [#12813](https://www.sqlalchemy.org/trac/ticket/12813)
- Added new decorator [mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_as_dataclass), which is a function
  based form of [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass); the method form
  [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) does not seem to be correctly
  recognized within the scope of [PEP 681](https://peps.python.org/pep-0681/) in recent mypy versions.
  References: [#12855](https://www.sqlalchemy.org/trac/ticket/12855)

### asyncio

- Generalize the terminate logic employed by the asyncpg dialect to reuse
  it in the aiomysql and asyncmy dialect implementation.
  References: [#12273](https://www.sqlalchemy.org/trac/ticket/12273)

### postgresql

- Fixed issue where selecting an enum array column containing NULL values
  would fail to parse properly in the PostgreSQL dialect. The
  `_split_enum_values()` function now correctly handles NULL entries by
  converting them to Python `None` values.
  References: [#12847](https://www.sqlalchemy.org/trac/ticket/12847)
- Fixed issue where the [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) and [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_) aggregation
  operators would not correctly coerce the datatype of the compared value, in
  those cases where the compared value were not a simple int/str etc., such
  as a Python `Enum` or other custom value.   This would lead to execution
  time errors for these values.  This issue is essentially the same as
  [#6515](https://www.sqlalchemy.org/trac/ticket/6515) which was for the now-legacy `ARRAY.any()` and
  `ARRAY.all()` methods.
  References: [#12874](https://www.sqlalchemy.org/trac/ticket/12874)

### sqlite

- Fixed issue where SQLite table reflection would fail for tables using
  `WITHOUT ROWID` and/or `STRICT` table options when the table contained
  generated columns. The regular expression used to parse `CREATE TABLE`
  statements for generated column detection has been updated to properly
  handle these SQLite table options that appear after the column definitions.
  Pull request courtesy Tip ten Brink.
  References: [#12864](https://www.sqlalchemy.org/trac/ticket/12864)

### mssql

- Improved the base implementation of the asyncio cursor such that it
  includes the option for the underlying driver’s cursor to be actively
  closed in those cases where it requires `await` in order to complete the
  close sequence, rather than relying on garbage collection to “close” it,
  when a plain [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) is returned that does not use `await` for
  any of its methods.  The previous approach of relying on gc was fine for
  MySQL and SQLite dialects but has caused problems with the aioodbc
  implementation on top of SQL Server.   The new option is enabled
  for those dialects which have an “awaitable” `cursor.close()`, which
  includes the aioodbc, aiomysql, and asyncmy dialects (aiosqlite is also
  modified for 2.1 only).
  References: [#12798](https://www.sqlalchemy.org/trac/ticket/12798)
- Fixed issue where the index reflection for SQL Server would
  not correctly return the order of the column inside an index
  when the order of the columns in the index did not match the
  order of the columns in the table.
  Pull request courtesy of Allen Chen.
  References: [#12894](https://www.sqlalchemy.org/trac/ticket/12894)
- Fixed issue in the MSSQL dialect’s foreign key reflection query where
  duplicate rows could be returned when a foreign key column and its
  referenced primary key column have the same name, and both the referencing
  and referenced tables have indexes with the same name. This resulted in an
  “ForeignKeyConstraint with duplicate source column references are not
  supported” error when attempting to reflect such tables. The query has been
  corrected to exclude indexes on the child table when looking for unique
  indexes referenced by foreign keys.
  References: [#12907](https://www.sqlalchemy.org/trac/ticket/12907)

### misc

- Fixed issue caused by an unwanted functional change while typing
  the [MutableList](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList) class.
  This change also reverts all other functional changes done in
  the same change.
  References: [#12802](https://www.sqlalchemy.org/trac/ticket/12802)

## 2.0.43

Released: August 11, 2025

### orm

- Fixed issue where using the `post_update` feature would apply incorrect
  “pre-fetched” values to the ORM objects after a multi-row UPDATE process
  completed.  These “pre-fetched” values would come from any column that had
  an [Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate) callable or a version id generator used by
  [Mapper.version_id_generator](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.version_id_generator); for a version id generator
  that delivered random identifiers like timestamps or UUIDs, this incorrect
  data would lead to a DELETE statement against those same rows to fail in
  the next step.
  References: [#12748](https://www.sqlalchemy.org/trac/ticket/12748)
- Fixed issue where [mapped_column.use_existing_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.use_existing_column)
  parameter in [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) would not work when the
  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) is used inside of an `Annotated` type alias in
  polymorphic inheritance scenarios. The parameter is now properly recognized
  and processed during declarative mapping configuration.
  References: [#12787](https://www.sqlalchemy.org/trac/ticket/12787)
- Improved the implementation of the [selectin_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.selectin_polymorphic)
  inheritance loader strategy to properly render the IN expressions using
  chunks of 500 records each, in the same manner as that of the
  [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) relationship loader strategy.  Previously, the IN
  expression would be arbitrarily large, leading to failures on databases
  that have limits on the size of IN expressions including Oracle Database.
  References: [#12790](https://www.sqlalchemy.org/trac/ticket/12790)

### engine

- Added new parameter [create_engine.skip_autocommit_rollback](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.skip_autocommit_rollback)
  which provides for a per-dialect feature of preventing the DBAPI
  `.rollback()` from being called under any circumstances, if the
  connection is detected as being in “autocommit” mode.   This improves upon
  a critical performance issue identified in MySQL dialects where the network
  overhead of the `.rollback()` call remains prohibitive even if autocommit
  mode is set.
  See also
  [Fully preventing ROLLBACK calls under autocommit](https://docs.sqlalchemy.org/en/20/core/connections.html#dbapi-autocommit-skip-rollback)
  References: [#12784](https://www.sqlalchemy.org/trac/ticket/12784)

### postgresql

- Fixed regression in PostgreSQL dialect where JSONB subscription syntax
  would generate incorrect SQL for JSONB-returning functions, causing syntax
  errors. The dialect now properly wraps function calls and expressions in
  parentheses when using the `[]` subscription syntax, generating
  `(function_call)[index]` instead of `function_call[index]` to comply
  with PostgreSQL syntax requirements.
  References: [#12778](https://www.sqlalchemy.org/trac/ticket/12778)

### oracle

- Extended [VECTOR](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.VECTOR) to support sparse vectors. This update
  introduces [VectorStorageType](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.VectorStorageType) to specify sparse or dense
  storage and added [SparseVector](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.SparseVector). Pull request courtesy
  Suraj Shaw.
  References: [#12711](https://www.sqlalchemy.org/trac/ticket/12711)

## 2.0.42

Released: July 29, 2025

### orm

- Added `dataclass_metadata` argument to all ORM attribute constructors
  that accept dataclasses parameters, e.g. [mapped_column.dataclass_metadata](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.dataclass_metadata),
  [relationship.dataclass_metadata](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.dataclass_metadata), etc.
  It’s passed to the underlying dataclass `metadata` attribute
  of the dataclass field. Pull request courtesy Sigmund Lahn.
  References: [#10674](https://www.sqlalchemy.org/trac/ticket/10674)
- Implemented the [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer), [undefer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer) and
  [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) loader options to work for composite attributes, a
  use case that had never been supported previously.
  References: [#12593](https://www.sqlalchemy.org/trac/ticket/12593)
- Fixed bug where the ORM would pull in the wrong column into an UPDATE when
  a key name inside of the [ValuesBase.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.ValuesBase.values) method could be located
  from an ORM entity mentioned in the statement, but where that ORM entity
  was not the actual table that the statement was inserting or updating.  An
  extra check for this edge case is added to avoid this problem.
  References: [#12692](https://www.sqlalchemy.org/trac/ticket/12692)

### engine

- Improved validation of execution parameters passed to the
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) and similar methods to
  provided a better error when tuples are passed in.
  Previously the execution would fail with a difficult to
  understand error message.

### sql

- The [values()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.values) construct gains a new method [Values.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values.cte),
  which allows creation of a named, explicit-columns [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) against an
  unnamed `VALUES` expression, producing a syntax that allows column-oriented
  selection from a `VALUES` construct on modern versions of PostgreSQL, SQLite,
  and MariaDB.
  References: [#12734](https://www.sqlalchemy.org/trac/ticket/12734)
- Fixed issue where [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) of a free-standing scalar expression that
  has a unary operator applied, such as negation, would not apply result
  processors to the selected column even though the correct type remains in
  place for the unary expression.
  References: [#12681](https://www.sqlalchemy.org/trac/ticket/12681)
- Hardening of the compiler’s actions for UPDATE statements that access
  multiple tables to report more specifically when tables or aliases are
  referenced in the SET clause; on cases where the backend does not support
  secondary tables in the SET clause, an explicit error is raised, and on the
  MySQL or similar backends that support such a SET clause, more specific
  checking for not-properly-included tables is performed.  Overall the change
  is preventing these erroneous forms of UPDATE statements from being
  compiled, whereas previously it was relied on the database to raise an
  error, which was not always guaranteed to happen, or to be non-ambiguous,
  due to cases where the parent table included the same column name as the
  secondary table column being updated.
  References: [#12692](https://www.sqlalchemy.org/trac/ticket/12692)

### postgresql

- Added support for PostgreSQL 14+ [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) subscripting syntax.
  When connected to PostgreSQL 14 or later, JSONB columns now
  automatically use the native subscript notation `jsonb_col['key']`
  instead of the arrow operator `jsonb_col -> 'key'` for both read and
  write operations. This provides better compatibility with PostgreSQL’s
  native JSONB subscripting feature while maintaining backward
  compatibility with older PostgreSQL versions. JSON columns continue to
  use the traditional arrow syntax regardless of PostgreSQL version.
  Warning
  **For applications that have indexes against JSONB subscript
  expressions**
  This change caused an unintended side effect for indexes that were
  created against expressions that use subscript notation, e.g.
  `Index("ix_entity_json_ab_text", data["a"]["b"].astext)`. If these
  indexes were generated with the older syntax e.g. `((entity.data ->
  'a') ->> 'b')`, they will not be used by the PostgreSQL query
  planner when a query is made using SQLAlchemy 2.0.42 or higher on
  PostgreSQL versions 14 or higher. This occurs because the new text
  will resemble `(entity.data['a'] ->> 'b')` which will fail to
  produce the exact textual syntax match required by the PostgreSQL
  query planner.  Therefore, for users upgrading to SQLAlchemy 2.0.42
  or higher, existing indexes that were created against [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB)
  expressions that use subscripting would need to be dropped and
  re-created in order for them to work with the new query syntax, e.g.
  an expression like `((entity.data -> 'a') ->> 'b')` would become
  `(entity.data['a'] ->> 'b')`.
  See also
  [#12868](https://www.sqlalchemy.org/trac/ticket/12868) - discussion of this issue
  References: [#10927](https://www.sqlalchemy.org/trac/ticket/10927)
- Added `postgresql_ops` key to the `dialect_options` entry in reflected
  dictionary. This maps names of columns used in the index to respective
  operator class, if distinct from the default one for column’s data type.
  Pull request courtesy Denis Laxalde.
  See also
  [Operator Classes](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-operator-classes)
  References: [#8664](https://www.sqlalchemy.org/trac/ticket/8664)
- Fixed regression caused by [#10665](https://www.sqlalchemy.org/trac/ticket/10665) where the newly modified
  constraint reflection query would fail on older versions of PostgreSQL
  such as version 9.6.  Pull request courtesy Denis Laxalde.
  References: [#12600](https://www.sqlalchemy.org/trac/ticket/12600)
- Re-raise caught `CancelledError` in the terminate method of the
  asyncpg dialect to avoid possible hangs of the code execution.
  References: [#12728](https://www.sqlalchemy.org/trac/ticket/12728)
- Fixes bug that would mistakenly interpret a domain or enum type
  with name starting in `interval` as an `INTERVAL` type while
  reflecting a table.
  References: [#12744](https://www.sqlalchemy.org/trac/ticket/12744)

### mysql

- Fixed yet another regression caused by by the DEFAULT rendering changes in
  2.0.40 [#12425](https://www.sqlalchemy.org/trac/ticket/12425), similar to [#12488](https://www.sqlalchemy.org/trac/ticket/12488), this time where using a
  CURRENT_TIMESTAMP function with a fractional seconds portion inside a
  textual default value would also fail to be recognized as a
  non-parenthesized server default.
  References: [#12648](https://www.sqlalchemy.org/trac/ticket/12648)

### mssql

- Reworked SQL Server column reflection to be based on the `sys.columns`
  table rather than `information_schema.columns` view.  By correctly using
  the SQL Server `object_id()` function as a lead and joining to related
  tables on object_id rather than names, this repairs a variety of issues in
  SQL Server reflection, including:
  - Issue where reflected column comments would not correctly line up
    with the columns themselves in the case that the table had been ALTERed
  - Correctly targets tables with awkward names such as names with brackets,
    when reflecting not just the basic table / columns but also extended
    information including IDENTITY, computed columns, comments which
    did not work previously
  - Correctly targets IDENTITY, computed status from temporary tables
    which did not work previously
  References: [#12654](https://www.sqlalchemy.org/trac/ticket/12654)

## 2.0.41

Released: May 14, 2025

### platform

- Adjusted the test suite as well as the ORM’s method of scanning classes for
  annotations to work under current beta releases of Python 3.14 (currently
  3.14.0b1) as part of an ongoing effort to support the production release of
  this Python release.  Further changes to Python’s means of working with
  annotations is expected in subsequent beta releases for which SQLAlchemy’s
  test suite will need further adjustments.
  References: [#12405](https://www.sqlalchemy.org/trac/ticket/12405)

### engine

- The error message that is emitted when a URL cannot be parsed no longer
  includes the URL itself within the error message.
  References: [#12579](https://www.sqlalchemy.org/trac/ticket/12579)

### typing

- Removed `__getattr__()` rule from `sqlalchemy/__init__.py` that
  appeared to be trying to correct for a previous typographical error in the
  imports. This rule interferes with type checking and is removed.
  References: [#12588](https://www.sqlalchemy.org/trac/ticket/12588)

### postgresql

- Added support for `postgresql_include` keyword argument to
  [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) and [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint).
  Pull request courtesy Denis Laxalde.
  See also
  [PostgreSQL Constraint Options](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-constraint-options)
  References: [#10665](https://www.sqlalchemy.org/trac/ticket/10665)

### mysql

- Fixed regression caused by the DEFAULT rendering changes in version 2.0.40
  via [#12425](https://www.sqlalchemy.org/trac/ticket/12425) where using lowercase `on update` in a MySQL server
  default would incorrectly apply parenthesis, leading to errors when MySQL
  interpreted the rendered DDL.  Pull request courtesy Alexander Ruehe.
  References: [#12488](https://www.sqlalchemy.org/trac/ticket/12488)

### sqlite

- Fixed and added test support for some SQLite SQL functions hardcoded into
  the compiler, most notably the `localtimestamp` function which rendered
  with incorrect internal quoting.
  References: [#12566](https://www.sqlalchemy.org/trac/ticket/12566)

### oracle

- Added new datatype [VECTOR](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.VECTOR) and accompanying DDL and DQL
  support to fully support this type for Oracle Database. This change
  includes the base [VECTOR](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.VECTOR) type that adds new type-specific
  methods `l2_distance`, `cosine_distance`, `inner_product` as well as
  new parameters `oracle_vector` for the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct,
  allowing vector indexes to be configured, and `oracle_fetch_approximate`
  for the [Select.fetch()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.fetch) clause.  Pull request courtesy Suraj Shaw.
  See also
  [VECTOR Datatype](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracle-vector-datatype)
  References: [#12317](https://www.sqlalchemy.org/trac/ticket/12317), [#12341](https://www.sqlalchemy.org/trac/ticket/12341)

### misc

- Removed the “license classifier” from setup.cfg for SQLAlchemy 2.0, which
  eliminates loud deprecation warnings when building the package.  SQLAlchemy
  2.1 will use a full [PEP 639](https://peps.python.org/pep-0639/) configuration in pyproject.toml while
  SQLAlchemy 2.0 remains using `setup.cfg` for setup.

## 2.0.40

Released: March 27, 2025

### orm

- Fixed regression which occurred as of 2.0.37 where the checked
  [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) that’s raised when an inappropriate type or object
  is used inside of a [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation would raise `TypeError`
  with “boolean value of this clause is not defined” if the object resolved
  into a SQL expression in a boolean context, for programs where future
  annotations mode was not enabled.  This case is now handled explicitly and
  a new error message has also been tailored for this case.  In addition, as
  there are at least half a dozen distinct error scenarios for interpretation
  of the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) construct, these scenarios have all been unified
  under a new subclass of [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) called
  [MappedAnnotationError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.MappedAnnotationError), to provide some continuity between these
  different scenarios, even though specific messaging remains distinct.
  References: [#12329](https://www.sqlalchemy.org/trac/ticket/12329)
- Fixed regression in ORM Annotated Declarative class interpretation caused
  by `typing_extension==4.13.0` that introduced a different implementation
  for `TypeAliasType` while SQLAlchemy assumed that it would be equivalent
  to the `typing` version, leading to pep-695 type annotations not
  resolving to SQL types as expected.
  References: [#12473](https://www.sqlalchemy.org/trac/ticket/12473)

### sql

- Implemented support for the GROUPS frame specification in window functions
  by adding [over.groups](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over.params.groups) option to [over()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over)
  and [FunctionElement.over()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.over). Pull request courtesy Kaan Dikmen.
  References: [#12450](https://www.sqlalchemy.org/trac/ticket/12450)
- Fixed issue in [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) constructs involving multiple DDL
  [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) statements with multiple VALUES parameter sets where the
  bound parameter names generated for these parameter sets would conflict,
  generating a compile time error.
  References: [#12363](https://www.sqlalchemy.org/trac/ticket/12363)
- Fixed regression caused by [#7471](https://www.sqlalchemy.org/trac/ticket/7471) leading to a SQL compilation
  issue where name disambiguation for two same-named FROM clauses with table
  aliasing in use at the same time would produce invalid SQL in the FROM
  clause with two “AS” clauses for the aliased table, due to double aliasing.
  References: [#12451](https://www.sqlalchemy.org/trac/ticket/12451)

### asyncio

- Fixed issue where [AsyncSession.get_transaction()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.get_transaction) and
  [AsyncSession.get_nested_transaction()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.get_nested_transaction) would fail with
  `NotImplementedError` if the “proxy transaction” used by
  [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession) were garbage collected and needed regeneration.
  References: [#12471](https://www.sqlalchemy.org/trac/ticket/12471)

### postgresql

- Added support for specifying a list of columns for `SET NULL` and `SET
  DEFAULT` actions of `ON DELETE` clause of foreign key definition on
  PostgreSQL.  Pull request courtesy Denis Laxalde.
  See also
  [PostgreSQL Constraint Options](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-constraint-options)
  References: [#11595](https://www.sqlalchemy.org/trac/ticket/11595)
- When building a PostgreSQL `ARRAY` literal using
  [array](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array) with an empty `clauses` argument, the
  [array.type_](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array.params.type_) parameter is now significant in that it
  will be used to render the resulting `ARRAY[]` SQL expression with a
  cast, such as `ARRAY[]::INTEGER`. Pull request courtesy Denis Laxalde.
  References: [#12432](https://www.sqlalchemy.org/trac/ticket/12432)

### mysql

- Support has been re-added for the MySQL-Connector/Python DBAPI using the
  `mysql+mysqlconnector://` URL scheme.   The DBAPI now works against
  modern MySQL versions as well as MariaDB versions (in the latter case it’s
  required to pass charset/collation explicitly).   Note however that
  server side cursor support is disabled due to unresolved issues with this
  driver.
  References: [#12332](https://www.sqlalchemy.org/trac/ticket/12332)
- Fixed issue in MySQL server default reflection where a default that has
  spaces would not be correctly reflected.  Additionally, expanded the rules
  for when to apply parenthesis to a server default in DDL to suit the
  general case of a default string that contains non-word characters such as
  spaces or operators and is not a string literal.
  References: [#12425](https://www.sqlalchemy.org/trac/ticket/12425)

### sqlite

- Expanded the rules for when to apply parenthesis to a server default in DDL
  to suit the general case of a default string that contains non-word
  characters such as spaces or operators and is not a string literal.
  References: [#12425](https://www.sqlalchemy.org/trac/ticket/12425)

## 2.0.39

Released: March 11, 2025

### orm

- Fixed bug where using DML returning such as [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) with
  an ORM model that has [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) constructs that contain
  subqueries would fail with an internal error.
  References: [#12326](https://www.sqlalchemy.org/trac/ticket/12326)
- Fixed bug in ORM enabled UPDATE (and theoretically DELETE) where using a
  multi-table DML statement would not allow ORM mapped columns from mappers
  other than the primary UPDATE mapper to be named in the RETURNING clause;
  they would be omitted instead and cause a column not found exception.
  References: [#12328](https://www.sqlalchemy.org/trac/ticket/12328)
- Fixed issue where the “is ORM” flag of a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) or other ORM
  statement would not be propagated to the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) based on a
  multi-part operator expression alone, e.g. such as `Cls.attr + Cls.attr +
  Cls.attr` or similar, leading to ORM behaviors not taking place for such
  statements.
  References: [#12357](https://www.sqlalchemy.org/trac/ticket/12357)
- Fixed issue where using [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) around a [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE)
  construct could cause inappropriate “duplicate CTE” errors in cases where
  that aliased construct appeared multiple times in a single statement.
  References: [#12364](https://www.sqlalchemy.org/trac/ticket/12364)

### sql

- Added new parameters [AddConstraint.isolate_from_table](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.AddConstraint.params.isolate_from_table) and
  [DropConstraint.isolate_from_table](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropConstraint.params.isolate_from_table), defaulting to True, which
  both document and allow to be controllable the long-standing behavior of
  these two constructs blocking the given constraint from being included
  inline within the “CREATE TABLE” sequence, under the assumption that
  separate add/drop directives were to be used.
  References: [#12382](https://www.sqlalchemy.org/trac/ticket/12382)

### typing

- Support generic types for compound selects ([union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union),
  [union_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union_all), [Select.union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.union),
  [Select.union_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.union_all), etc) returning the type of the first select.
  Pull request courtesy of Mingyu Park.
  References: [#11922](https://www.sqlalchemy.org/trac/ticket/11922)

### asyncio

- Fixed bug where [AsyncResult.scalar()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncResult.scalar),
  [AsyncResult.scalar_one_or_none()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncResult.scalar_one_or_none), and
  [AsyncResult.scalar_one()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncResult.scalar_one) would raise an `AttributeError`
  due to a missing internal attribute.  Pull request courtesy Allen Ho.
  References: [#12338](https://www.sqlalchemy.org/trac/ticket/12338)

### postgresql

- Add SQL typing to reflection query used to retrieve a the structure
  of IDENTITY columns, adding explicit JSON typing to the query to suit
  unusual PostgreSQL driver configurations that don’t support JSON natively.
  References: [#11751](https://www.sqlalchemy.org/trac/ticket/11751)
- Fixed issue affecting PostgreSQL 17.3 and greater where reflection of
  domains with “NOT NULL” as part of their definition would include an
  invalid constraint entry in the data returned by
  `PGInspector.get_domains()` corresponding to an additional
  “NOT NULL” constraint that isn’t a CHECK constraint; the existing
  `"nullable"` entry in the dictionary already indicates if the domain
  includes a “not null” constraint.   Note that such domains also cannot be
  reflected on PostgreSQL 17.0 through 17.2 due to a bug on the PostgreSQL
  side; if encountering errors in reflection of domains which include NOT
  NULL, upgrade to PostgreSQL server 17.3 or greater.
- Fixed issue in PostgreSQL network types [INET](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.INET),
  [CIDR](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.CIDR), [MACADDR](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.MACADDR),
  [MACADDR8](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.MACADDR8) where sending string values to compare to
  these types would render an explicit CAST to VARCHAR, causing some SQL /
  driver combinations to fail.  Pull request courtesy Denis Laxalde.
  References: [#12060](https://www.sqlalchemy.org/trac/ticket/12060)
- Fixed compiler issue in the PostgreSQL dialect where incorrect keywords
  would be passed when using “FOR UPDATE OF” inside of a subquery.
  References: [#12417](https://www.sqlalchemy.org/trac/ticket/12417)

### sqlite

- Fixed issue that omitted the comma between multiple SQLite table extension
  clauses, currently `WITH ROWID` and `STRICT`, when both options
  [Table.sqlite_with_rowid](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.sqlite_with_rowid) and  [Table.sqlite_strict](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.sqlite_strict)
  were configured at their non-default settings at the same time.  Pull
  request courtesy david-fed.
  References: [#12368](https://www.sqlalchemy.org/trac/ticket/12368)

## 2.0.38

Released: February 6, 2025

### engine

- Fixed event-related issue where invoking [Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options)
  on a [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) multiple times while making use of event-registering
  parameters such as `isolation_level` would lead to internal errors
  involving event registration.
  References: [#12289](https://www.sqlalchemy.org/trac/ticket/12289)

### sql

- Reorganized the internals by which the `.c` collection on a
  [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) gets generated so that it is resilient against the
  collection being accessed in concurrent fashion.   An example is creating a
  [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) or [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) and accessing it as a module level
  variable.  This impacts the Oracle dialect which uses such module-level
  global alias objects but is of general use as well.
  References: [#12302](https://www.sqlalchemy.org/trac/ticket/12302)
- Fixed SQL composition bug which impacted caching where using a `None`
  value inside of an `in_()` expression would bypass the usual “expanded
  bind parameter” logic used by the IN construct, which allows proper caching
  to take place.
  References: [#12314](https://www.sqlalchemy.org/trac/ticket/12314)

### postgresql

- Added an additional `asyncio.shield()` call within the connection
  terminate process of the asyncpg driver, to mitigate an issue where
  terminate would be prevented from completing under the anyio concurrency
  library.
  References: [#12077](https://www.sqlalchemy.org/trac/ticket/12077)
- Adjusted the asyncpg connection wrapper so that the
  `connection.transaction()` call sent to asyncpg sends `None` for
  `isolation_level` if not otherwise set in the SQLAlchemy dialect/wrapper,
  thereby allowing asyncpg to make use of the server level setting for
  `isolation_level` in the absence of a client-level setting. Previously,
  this behavior of asyncpg was blocked by a hardcoded `read_committed`.
  References: [#12159](https://www.sqlalchemy.org/trac/ticket/12159)

### mariadb

- Fixed a bug where the MySQL statement compiler would not properly compile
  statements where [Insert.on_duplicate_key_update()](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.Insert.on_duplicate_key_update) was passed
  values that included ORM-mapped attributes (e.g.
  `InstrumentedAttribute` objects) as keys. Pull request courtesy of
  mingyu.
  References: [#12117](https://www.sqlalchemy.org/trac/ticket/12117)

### sqlite

- Changed default connection pool used by the `aiosqlite` dialect
  from [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) to [AsyncAdaptedQueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AsyncAdaptedQueuePool); this change
  should have been made when 2.0 was first released as the `pysqlite`
  dialect was similarly changed to use [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) as detailed
  in [The SQLite dialect uses QueuePool for file-based databases](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7490).
  References: [#12285](https://www.sqlalchemy.org/trac/ticket/12285)

## 2.0.37

Released: January 9, 2025

### orm

- Fixed issue regarding `Union` types that would be present in the
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) of a [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry)
  or declarative base class, where a [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) element that included
  one of the subtypes present in that `Union` would be matched to that
  entry, potentially ignoring other entries that matched exactly.   The
  correct behavior now takes place such that an entry should only match in
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) exactly, as a `Union` type
  is a self-contained type. For example, an attribute with `Mapped[float]`
  would previously match to a [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map)
  entry `Union[float, Decimal]`; this will no longer match and will now
  only match to an entry that states `float`. Pull request courtesy Frazer
  McLean.
  References: [#11370](https://www.sqlalchemy.org/trac/ticket/11370)
- Fixed bug in how type unions were handled within
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) as well as
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) that made the lookup behavior of `a | b` different
  from that of `Union[a, b]`.
  References: [#11944](https://www.sqlalchemy.org/trac/ticket/11944)
- Note
  this change has been revised in version 2.0.44.  Simple matches
  of `TypeAliasType` without a type map entry are no longer deprecated.
  Consistently handle `TypeAliasType` (defined in PEP 695) obtained with
  the `type X = int` syntax introduced in python 3.12. Now in all cases one
  such alias must be explicitly added to the type map for it to be usable
  inside [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped). This change also revises the approach added in
  [#11305](https://www.sqlalchemy.org/trac/ticket/11305), now requiring the `TypeAliasType` to be added to the
  type map. Documentation on how unions and type alias types are handled by
  SQLAlchemy has been added in the
  [Customizing the Type Map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-type-map) section of the documentation.
  References: [#11955](https://www.sqlalchemy.org/trac/ticket/11955)
- Fixed regression caused by an internal code change in response to recent
  Mypy releases that caused the very unusual case of a list of ORM-mapped
  attribute expressions passed to [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) to no longer
  be accepted.
  References: [#12019](https://www.sqlalchemy.org/trac/ticket/12019)
- Fixed issues in type handling within the
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) feature which prevented the
  use of unions, using either pep-604 or `Union` syntaxes under future
  annotations mode, which contained multiple generic types as elements from
  being correctly resolvable.
  References: [#12207](https://www.sqlalchemy.org/trac/ticket/12207)
- Fixed issue in event system which prevented an event listener from being
  attached and detached from multiple class-like objects, namely the
  [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) or [scoped_session](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoped_session) targets that assign to
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) subclasses.
  References: [#12216](https://www.sqlalchemy.org/trac/ticket/12216)

### sql

- Fixed issue in “lambda SQL” feature where the tracking of bound parameters
  could be corrupted if the same lambda were evaluated across multiple
  compile phases, including when using the same lambda across multiple engine
  instances or with statement caching disabled.
  References: [#12084](https://www.sqlalchemy.org/trac/ticket/12084)

### postgresql

- The [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range) type now supports
  `Range.__contains__()`. Pull request courtesy of Frazer
  McLean.
  References: [#12093](https://www.sqlalchemy.org/trac/ticket/12093)
- Fixes issue in [Dialect.get_multi_indexes()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.get_multi_indexes) in the PostgreSQL
  dialect, where an error would be thrown when attempting to use alembic with
  a vector index from the pgvecto.rs extension.
  References: [#11724](https://www.sqlalchemy.org/trac/ticket/11724)
- Fixed issue where creating a table with a primary column of
  `SmallInteger` and using the asyncpg driver would result in
  the type being compiled to `SERIAL` rather than `SMALLSERIAL`.
  References: [#12170](https://www.sqlalchemy.org/trac/ticket/12170)
- Adjusted the asyncpg dialect so that an empty SQL string, which is valid
  for PostgreSQL server, may be successfully processed at the dialect level,
  such as when using [Connection.exec_driver_sql()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.exec_driver_sql). Pull request
  courtesy Andrew Jackson.
  References: [#12220](https://www.sqlalchemy.org/trac/ticket/12220)

### mysql

- Added support for the `LIMIT` clause with `DELETE` for the MySQL and
  MariaDB dialects, to complement the already present option for
  `UPDATE`. The [Delete.with_dialect_options()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete.with_dialect_options) method of the
  [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) construct accepts parameters for `mysql_limit` and
  `mariadb_limit`, allowing users to specify a limit on the number of rows
  deleted. Pull request courtesy of Pablo Nicolás Estevez.
  References: [#11764](https://www.sqlalchemy.org/trac/ticket/11764)
- Added logic to ensure that the `mysql_limit` and `mariadb_limit`
  parameters of [Update.with_dialect_options()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.with_dialect_options) and
  [Delete.with_dialect_options()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete.with_dialect_options) when compiled to string will only
  compile if the parameter is passed as an integer; a `ValueError` is
  raised otherwise.

### mariadb

- Added sql types `INET4` and `INET6` in the MariaDB dialect.  Pull
  request courtesy Adam Žurek.
  References: [#10720](https://www.sqlalchemy.org/trac/ticket/10720)

### sqlite

- Added SQLite table option to enable `STRICT` tables. Pull request
  courtesy of Guilherme Crocetti.
  References: [#7398](https://www.sqlalchemy.org/trac/ticket/7398)

### oracle

- Added new table option `oracle_tablespace` to specify the `TABLESPACE`
  option when creating a table in Oracle. This allows users to define the
  tablespace in which the table should be created. Pull request courtesy of
  Miguel Grillo.
  References: [#12016](https://www.sqlalchemy.org/trac/ticket/12016)
- Use the connection attribute `max_identifier_length` available
  in oracledb since version 2.5 when determining the identifier length
  in the Oracle dialect.
  References: [#12032](https://www.sqlalchemy.org/trac/ticket/12032)
- Fixed compilation of `TABLE` function when used in a `FROM` clause in
  Oracle Database dialect.
  References: [#12100](https://www.sqlalchemy.org/trac/ticket/12100)
- Fixed issue in oracledb / cx_oracle dialects where output type handlers for
  `CLOB` were being routed to `NVARCHAR` rather than `VARCHAR`, causing
  a double conversion to take place.
  References: [#12150](https://www.sqlalchemy.org/trac/ticket/12150)

## 2.0.36

Released: October 15, 2024

### orm

- Added new parameter [mapped_column.hash](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.hash) to ORM constructs
  such as [sqlalchemy.orm.mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column), [sqlalchemy.orm.relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), etc.,
  which is interpreted for ORM Native Dataclasses in the same way as other
  dataclass-specific field parameters.
  References: [#11923](https://www.sqlalchemy.org/trac/ticket/11923)
- Fixed bug in ORM bulk update/delete where using RETURNING with bulk
  update/delete in combination with `populate_existing` would fail to
  accommodate the `populate_existing` option.
  References: [#11912](https://www.sqlalchemy.org/trac/ticket/11912)
- Continuing from [#11912](https://www.sqlalchemy.org/trac/ticket/11912), columns marked with
  [mapped_column.onupdate](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.onupdate),
  [mapped_column.server_onupdate](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.server_onupdate), or [Computed](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Computed) are now
  refreshed in ORM instances when running an ORM enabled UPDATE with WHERE
  criteria, even if the statement does not use RETURNING or
  `populate_existing`.
  References: [#11917](https://www.sqlalchemy.org/trac/ticket/11917)
- Fixed regression caused by fixes to joined eager loading in [#11449](https://www.sqlalchemy.org/trac/ticket/11449)
  released in 2.0.31, where a particular joinedload case could not be
  asserted correctly.   We now have an example of that case so the assertion
  has been repaired to allow for it.
  References: [#11965](https://www.sqlalchemy.org/trac/ticket/11965)
- Improved the error message emitted when trying to map as dataclass a class
  while also manually providing the `__table__` attribute.
  This usage is currently not supported.
  References: [#11973](https://www.sqlalchemy.org/trac/ticket/11973)
- Refined the check which the ORM lazy loader uses to detect “this would be
  loading by primary key and the primary key is NULL, skip loading” to take
  into account the current setting for the
  [Mapper.allow_partial_pks](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.allow_partial_pks) parameter. If this parameter is
  `False`, then a composite PK value that has partial NULL elements should
  also be skipped.   This can apply to some composite overlapping foreign key
  configurations.
  References: [#11995](https://www.sqlalchemy.org/trac/ticket/11995)
- Fixed bug in ORM “update with WHERE clause” feature where an explicit
  `.returning()` would interfere with the “fetch” synchronize strategy due
  to an assumption that the ORM mapped class featured the primary key columns
  in a specific position within the RETURNING.  This has been fixed to use
  appropriate ORM column targeting.
  References: [#11997](https://www.sqlalchemy.org/trac/ticket/11997)

### sql

- Datatypes that are binary based such as [VARBINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARBINARY) will resolve to
  [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) when the [TypeEngine.as_generic()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.as_generic) method is
  called.
  References: [#11978](https://www.sqlalchemy.org/trac/ticket/11978)
- Fixed regression from 1.4 where some datatypes such as those derived from
  [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) could not be pickled when they were part of a
  larger SQL expression composition due to internal supporting structures
  themselves not being pickleable.
  References: [#12002](https://www.sqlalchemy.org/trac/ticket/12002)

### schema

- Fixed bug where SQL functions passed to
  [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) would not be rendered with the
  particular form of parenthesization now required by newer versions of MySQL
  and MariaDB. Pull request courtesy of huuya.
  References: [#11317](https://www.sqlalchemy.org/trac/ticket/11317)

### postgresql

- Fixed bug in reflection of table comments where unrelated text would be
  returned if an entry in the `pg_description` table happened to share the
  same oid (objoid) as the table being reflected.
  References: [#11961](https://www.sqlalchemy.org/trac/ticket/11961)
- The [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) datatypes will
  now render a “bind cast” in all cases for all PostgreSQL backends,
  including psycopg2, whereas previously it was only enabled for some
  backends.   This allows greater accuracy in allowing the database server to
  recognize when a string value is to be interpreted as JSON.
  References: [#11994](https://www.sqlalchemy.org/trac/ticket/11994)

### mysql

- Improved a query used for the MySQL 8 backend when reflecting foreign keys
  to be better optimized.   Previously, for a database that had millions of
  columns across all tables, the query could be prohibitively slow; the query
  has been reworked to take better advantage of existing indexes.
  References: [#11975](https://www.sqlalchemy.org/trac/ticket/11975)

## 2.0.35

Released: September 16, 2024

### orm

- Fixed issue where it was not possible to use `typing.Literal` with
  `Mapped[]` on Python 3.8 and 3.9.  Pull request courtesy Frazer McLean.
  References: [#11820](https://www.sqlalchemy.org/trac/ticket/11820)
- Fixed issue in ORM evaluator where two datatypes being evaluated with the
  SQL concatenator operator would not be checked for
  `UnevaluatableError` based on their datatype; this missed the case
  of [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) values being used in a concatenate operation
  which is supported by PostgreSQL as well as how SQLAlchemy renders the SQL
  for this operation, but does not work at the Python level. By implementing
  `UnevaluatableError` for this combination, ORM update statements
  will now fall back to “expire” when a concatenated JSON value used in a SET
  clause is to be synchronized to a Python object.
  References: [#11849](https://www.sqlalchemy.org/trac/ticket/11849)
- An warning is emitted if [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload) or
  [subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload) are used as a top level option against a
  statement that is not a SELECT statement, such as with an
  `insert().returning()`.   There are no JOINs in INSERT statements nor is
  there a “subquery” that can be repurposed for subquery eager loading, and
  for UPDATE/DELETE joinedload does not support these either, so it is never
  appropriate for this use to pass silently.
  References: [#11853](https://www.sqlalchemy.org/trac/ticket/11853)
- Fixed issue where using loader options such as [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload)
  with additional criteria in combination with ORM DML such as
  [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) with RETURNING would not correctly set up internal
  contexts required for caching to work correctly, leading to incorrect
  results.
  References: [#11855](https://www.sqlalchemy.org/trac/ticket/11855)

### mysql

- Fixed issue in mariadbconnector dialect where query string arguments that
  weren’t checked integer or boolean arguments would be ignored, such as
  string arguments like `unix_socket`, etc.  As part of this change, the
  argument parsing for particular elements such as `client_flags`,
  `compress`, `local_infile` has been made more consistent across all
  MySQL / MariaDB dialect which accept each argument. Pull request courtesy
  Tobias Alex-Petersen.
  References: [#11870](https://www.sqlalchemy.org/trac/ticket/11870)

### sqlite

- The changes made for SQLite CHECK constraint reflection in versions 2.0.33
  and 2.0.34 , [#11832](https://www.sqlalchemy.org/trac/ticket/11832) and [#11677](https://www.sqlalchemy.org/trac/ticket/11677), have now been fully
  reverted, as users continued to identify existing use cases that stopped
  working after this change.   For the moment, because SQLite does not
  provide any consistent way of delivering information about CHECK
  constraints, SQLAlchemy is limited in what CHECK constraint syntaxes can be
  reflected, including that a CHECK constraint must be stated all on a
  single, independent line (or inline on a column definition)  without
  newlines, tabs in the constraint definition or unusual characters in the
  constraint name.  Overall, reflection for SQLite is tailored towards being
  able to reflect CREATE TABLE statements that were originally created by
  SQLAlchemy DDL constructs.  Long term work on a DDL parser that does not
  rely upon regular expressions may eventually improve upon this situation.
  A wide range of additional cross-dialect CHECK constraint reflection tests
  have been added as it was also a bug that these changes did not trip any
  existing tests.
  References: [#11840](https://www.sqlalchemy.org/trac/ticket/11840)

## 2.0.34

Released: September 4, 2024

### orm

- Fixed regression caused by issue [#11814](https://www.sqlalchemy.org/trac/ticket/11814) which broke support for
  certain flavors of [PEP 593](https://peps.python.org/pep-0593/) `Annotated` in the type_annotation_map when
  builtin types such as `list`, `dict` were used without an element type.
  While this is an incomplete style of typing, these types nonetheless
  previously would be located in the type_annotation_map correctly.
  References: [#11831](https://www.sqlalchemy.org/trac/ticket/11831)

### sqlite

- Fixed regression in SQLite reflection caused by [#11677](https://www.sqlalchemy.org/trac/ticket/11677) which
  interfered with reflection for CHECK constraints that were followed
  by other kinds of constraints within the same table definition.   Pull
  request courtesy Harutaka Kawamura.
  References: [#11832](https://www.sqlalchemy.org/trac/ticket/11832)

## 2.0.33

Released: September 3, 2024

### general

- The pin for `setuptools<69.3` in `pyproject.toml` has been removed.
  This pin was to prevent a sudden change in setuptools to use [PEP 625](https://peps.python.org/pep-0625/)
  from taking place, which would change the file name of SQLAlchemy’s source
  distribution on pypi to be an all lower case name, which is likely to cause
  problems with various build environments that expected the previous naming
  style.  However, the presence of this pin is holding back environments that
  otherwise want to use a newer setuptools, so we’ve decided to move forward
  with this change, with the assumption that build environments will have
  largely accommodated the setuptools change by now.
  References: [#11818](https://www.sqlalchemy.org/trac/ticket/11818)

### orm

- Fixed regression from 1.3 where the column key used for a hybrid property
  might be populated with that of the underlying column that it returns, for
  a property that returns an ORM mapped column directly, rather than the key
  used by the hybrid property itself.
  This change is also **backported** to: 1.4.54
  References: [#11728](https://www.sqlalchemy.org/trac/ticket/11728)
- Correctly cleanup the internal top-level module registry when no
  inner modules or classes are registered into it.
  References: [#11788](https://www.sqlalchemy.org/trac/ticket/11788)
- Improvements to the ORM annotated declarative type map lookup dealing with
  composed types such as `dict[str, Any]` linking to JSON (or others) with
  or without “future annotations” mode.
  References: [#11814](https://www.sqlalchemy.org/trac/ticket/11814)

### engine

- Fixed issue in internal reflection cache where particular reflection
  scenarios regarding same-named quoted_name() constructs would not be
  correctly cached.  Pull request courtesy Felix Lüdin.
  References: [#11687](https://www.sqlalchemy.org/trac/ticket/11687)

### sql

- Fixed regression in [Select.with_statement_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint) and others
  where the generative behavior of the method stopped producing a copy of the
  object.
  References: [#11703](https://www.sqlalchemy.org/trac/ticket/11703)

### schema

- Fixed bug where the `metadata` element of an `Enum` datatype would not
  be transferred to the new [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object when the type had been
  copied via a [Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) operation, leading to inconsistent
  behaviors within create/drop sequences.
  References: [#11802](https://www.sqlalchemy.org/trac/ticket/11802)

### typing

- Fixed typing issue with [Select.with_only_columns()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_only_columns).
  References: [#11782](https://www.sqlalchemy.org/trac/ticket/11782)

### postgresql

- Fixed critical issue in the asyncpg driver where a rollback or commit that
  fails specifically for the `MissingGreenlet` condition or any other error
  that is not raised by asyncpg itself would discard the asyncpg transaction
  in any case, even though the transaction were still idle, leaving to a
  server side condition with an idle transaction that then goes back into the
  connection pool.   The flags for “transaction closed” are now not reset for
  errors that are raised outside of asyncpg itself.  When asyncpg itself
  raises an error for `.commit()` or `.rollback()`, asyncpg does then
  discard of this transaction.
  This change is also **backported** to: 1.4.54
  References: [#11819](https://www.sqlalchemy.org/trac/ticket/11819)
- Revising the asyncpg `terminate()` fix first made in [#10717](https://www.sqlalchemy.org/trac/ticket/10717)
  which improved the resiliency of this call under all circumstances, adding
  `asyncio.CancelledError` to the list of exceptions that are intercepted
  as failing for a graceful `.close()` which will then proceed to call
  `.terminate()`.
  References: [#11821](https://www.sqlalchemy.org/trac/ticket/11821)

### mysql

- Fixed issue in MySQL dialect where using INSERT..FROM SELECT in combination
  with ON DUPLICATE KEY UPDATE would erroneously render on MySQL 8 and above
  the “AS new” clause, leading to syntax failures.  This clause is required
  on MySQL 8 to follow the VALUES clause if use of the “new” alias is
  present, however is not permitted to follow a FROM SELECT clause.
  References: [#11731](https://www.sqlalchemy.org/trac/ticket/11731)

### sqlite

- Improvements to the regex used by the SQLite dialect to reflect the name
  and contents of a CHECK constraint.  Constraints with newline, tab, or
  space characters in either or both the constraint text and constraint name
  are now properly reflected.   Pull request courtesy Jeff Horemans.
  References: [#11677](https://www.sqlalchemy.org/trac/ticket/11677)
- Improvements to the regex used by the SQLite dialect to reflect the name
  and contents of a UNIQUE constraint that is defined inline within a column
  definition inside of a SQLite CREATE TABLE statement, accommodating for tab
  characters present within the column / constraint line. Pull request
  courtesy John A Stevenson.
  References: [#11746](https://www.sqlalchemy.org/trac/ticket/11746)

### mssql

- Added error “The server failed to resume the transaction” to the list of
  error strings for the pymssql driver in determining a disconnect scenario,
  as observed by one user using pymssql under otherwise unknown conditions as
  leaving an unusable connection in the connection pool which fails to ping
  cleanly.
  References: [#11822](https://www.sqlalchemy.org/trac/ticket/11822)

### tests

- Added missing `array_type` property to the testing suite
  `SuiteRequirements` class.

## 2.0.32

Released: August 5, 2024

### general

- Restored legacy class names removed from
  `sqlalalchemy.orm.collections.*`, including
  [MappedCollection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.MappedCollection), [mapped_collection()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.mapped_collection),
  [column_mapped_collection()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_mapped_collection),
  [attribute_mapped_collection()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_mapped_collection). Pull request courtesy Takashi
  Kajinami.
  References: [#11435](https://www.sqlalchemy.org/trac/ticket/11435)

### orm

- The [aliased.name](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased.params.name) parameter to [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) may now
  be combined with the [aliased.flat](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased.params.flat) parameter, producing
  per-table names based on a name-prefixed naming convention.  Pull request
  courtesy Eric Atkin.
  References: [#11575](https://www.sqlalchemy.org/trac/ticket/11575)
- Fixed regression going back to 1.4 where accessing a collection using the
  “dynamic” strategy on a transient object and attempting to query would
  raise an internal error rather than the expected [NoResultFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoResultFound)
  that occurred in 1.3.
  This change is also **backported** to: 1.4.53
  References: [#11562](https://www.sqlalchemy.org/trac/ticket/11562)
- Fixed issue where using the [Query.enable_eagerloads()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.enable_eagerloads) and
  [Query.yield_per()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.yield_per) methods at the same time, in order to disable
  eager loading that’s configured on the mapper directly, would be silently
  ignored, leading to errors or unexpected eager population of attributes.
  References: [#10834](https://www.sqlalchemy.org/trac/ticket/10834)
- Fixed regression appearing in 2.0.21 caused by [#10279](https://www.sqlalchemy.org/trac/ticket/10279) where using
  a [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) or [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) against an ORM class that is
  the base of an inheritance hierarchy, while also specifying that subclasses
  should be loaded polymorphically, would leak the polymorphic joins into the
  UPDATE or DELETE statement as well creating incorrect SQL.
  References: [#11625](https://www.sqlalchemy.org/trac/ticket/11625)
- Fixed regression from version 1.4 in
  [Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings) where using the
  [Session.bulk_insert_mappings.return_defaults](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings.params.return_defaults) parameter
  would not populate the passed in dictionaries with newly generated primary
  key values.
  References: [#11661](https://www.sqlalchemy.org/trac/ticket/11661)
- Added a warning noting when an
  `ConnectionEvents.engine_connect()` event may be leaving
  a transaction open, which can alter the behavior of a
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) using such an engine as bind.
  On SQLAlchemy 2.1 [Session.join_transaction_mode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.join_transaction_mode) will
  instead be ignored in all cases when the session bind is
  an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).
  References: [#11163](https://www.sqlalchemy.org/trac/ticket/11163)

### examples

- Fixed issue in history_meta example where the “version” column in the
  versioned table needs to default to the most recent version number in the
  history table on INSERT, to suit the use case of a table where rows are
  deleted, and can then be replaced by new rows that reuse the same primary
  key identity.  This fix adds an additional SELECT query per INSERT in the
  main table, which may be inefficient; for cases where primary keys are not
  reused, the default function may be omitted.  Patch courtesy  Philipp H.
  v. Loewenfeld.
  References: [#10267](https://www.sqlalchemy.org/trac/ticket/10267)

### engine

- Fixed issue in “insertmanyvalues” feature where a particular call to
  `cursor.fetchall()` were not wrapped in SQLAlchemy’s exception wrapper,
  which apparently can raise a database exception during fetch when using
  pyodbc.
  References: [#11532](https://www.sqlalchemy.org/trac/ticket/11532)

### sql

- Follow up of [#11471](https://www.sqlalchemy.org/trac/ticket/11471) to fix caching issue where using the
  `CompoundSelectState.add_cte()` method of the
  `CompoundSelectState` construct would not set a correct cache key
  which distinguished between different CTE expressions. Also added tests
  that would detect issues similar to the one fixed in [#11544](https://www.sqlalchemy.org/trac/ticket/11544).
  References: [#11471](https://www.sqlalchemy.org/trac/ticket/11471)
- Fixed bug where the `Operators.nulls_first()` and
  `Operators.nulls_last()` modifiers would not be treated the same way
  as `Operators.desc()` and `Operators.asc()` when determining
  if an ORDER BY should be against a label name already in the statement. All
  four modifiers are now treated the same within ORDER BY.
  References: [#11592](https://www.sqlalchemy.org/trac/ticket/11592)

### schema

- Fixed additional issues in the event system triggered by unpickling of a
  [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatype, continuing from [#11365](https://www.sqlalchemy.org/trac/ticket/11365) and
  [#11360](https://www.sqlalchemy.org/trac/ticket/11360),  where dynamically generated elements of the event
  structure would not be present when unpickling in a new process.
  References: [#11530](https://www.sqlalchemy.org/trac/ticket/11530)

### typing

- Fixed internal typing issues to establish compatibility with mypy 1.11.0.
  Note that this does not include issues which have arisen with the
  deprecated mypy plugin used by SQLAlchemy 1.4-style code; see the additional
  change note for this plugin indicating revised compatibility.

### mypy

- The deprecated mypy plugin is no longer fully functional with the latest
  series of mypy 1.11.0, as changes in the mypy interpreter are no longer
  compatible with the approach used by the plugin.  If code is dependent on
  the mypy plugin with sqlalchemy2-stubs, it’s recommended to pin mypy to be
  below the 1.11.0 series.    Seek upgrading to the 2.0 series of SQLAlchemy
  and migrating to the modern type annotations.
  See also
  [Mypy  / Pep-484 Support for ORM Mappings](https://docs.sqlalchemy.org/en/20/orm/extensions/mypy.html)
  This change is also **backported** to: 1.4.53

### postgresql

- It is now considered a pool-invalidating disconnect event when psycopg2
  throws an “SSL SYSCALL error: Success” error message, which can occur when
  the SSL connection to Postgres is terminated abnormally.
  References: [#11522](https://www.sqlalchemy.org/trac/ticket/11522)
- Fixed issue where the [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate) construct, which explicitly sets
  a collation for a given expression, would maintain collation settings for
  the underlying type object from the expression, causing SQL expressions to
  have both collations stated at once when used in further expressions for
  specific dialects that render explicit type casts, such as that of asyncpg.
  The [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate) construct now assigns its own type to explicitly
  include the new collation, assuming it’s a string type.
  References: [#11576](https://www.sqlalchemy.org/trac/ticket/11576)

### mysql

- Fixed issue in MySQL dialect where ENUM values that contained percent signs
  were not properly escaped for the driver.
  References: [#11479](https://www.sqlalchemy.org/trac/ticket/11479)

### sqlite

- Fixed reflection of computed column in SQLite to properly account
  for complex expressions.
  This change is also **backported** to: 1.4.53
  References: [#11582](https://www.sqlalchemy.org/trac/ticket/11582)

### mssql

- Fixed issue where SQL Server drivers don’t support bound parameters when
  rendering the “frame specification” for a window function, e.g. “ROWS
  BETWEEN”, etc.
  This change is also **backported** to: 1.4.53
  References: [#11514](https://www.sqlalchemy.org/trac/ticket/11514)

### oracle

- Added API support for server-side cursors for the oracledb async dialect,
  allowing use of the [AsyncConnection.stream()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection.stream) and similar
  stream methods.
  References: [#10820](https://www.sqlalchemy.org/trac/ticket/10820)
- Implemented two-phase transactions for the oracledb dialect. Historically,
  this feature never worked with the cx_Oracle dialect, however recent
  improvements to the oracledb successor now allow this to be possible.  The
  two phase transaction API is available at the Core level via the
  [Connection.begin_twophase()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.begin_twophase) method.
  References: [#11480](https://www.sqlalchemy.org/trac/ticket/11480)
- Fixed table reflection on Oracle 10.2 and older where compression options
  are not supported.
  References: [#11557](https://www.sqlalchemy.org/trac/ticket/11557)
- Implemented bitwise operators for Oracle which was previously
  non-functional due to a non-standard syntax used by this database.
  Oracle’s support for bitwise “or” and “xor” starts with server version 21.
  Additionally repaired the implementation of “xor” for SQLite.
  As part of this change, the dialect compliance test suite has been enhanced
  to include support for server-side bitwise tests; third party dialect
  authors should refer to new “supports_bitwise” methods in the
  requirements.py file to enable these tests.
  References: [#11663](https://www.sqlalchemy.org/trac/ticket/11663)

## 2.0.31

Released: June 18, 2024

### general

- Set up full Python 3.13 support to the extent currently possible, repairing
  issues within internal language helpers as well as the serializer extension
  module.
  For version 1.4, this also modernizes the “extras” names in setup.cfg
  to use dashes and not underscores for two-word names.  Underscore names
  are still present to accommodate potential compatibility issues.
  This change is also **backported** to: 1.4.53
  References: [#11417](https://www.sqlalchemy.org/trac/ticket/11417)
- Set up full Python 3.13 support to the extent currently possible, repairing
  issues within internal language helpers as well as the serializer extension
  module.
  References: [#11417](https://www.sqlalchemy.org/trac/ticket/11417)

### orm

- Added missing parameter [with_polymorphic.name](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic.params.name) that
  allows specifying the name of returned `AliasedClass`.
  References: [#11361](https://www.sqlalchemy.org/trac/ticket/11361)
- Fixed issue where a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection would not be
  serializable, if an [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) or [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) datatype were
  present which had been adapted. This specific scenario in turn could occur
  when using the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) or [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) within ORM Annotated
  Declarative form where type objects frequently get copied.
  References: [#11365](https://www.sqlalchemy.org/trac/ticket/11365)
- Fixed issue where the [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) and
  [subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload) loader options would fail to take effect when
  made against an inherited subclass that itself included a subclass-specific
  [Mapper.with_polymorphic](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.with_polymorphic) setting.
  References: [#11446](https://www.sqlalchemy.org/trac/ticket/11446)
- Fixed very old issue involving the [joinedload.innerjoin](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload.params.innerjoin)
  parameter where making use of this parameter mixed into a query that also
  included joined eager loads along a self-referential or other cyclical
  relationship, along with complicating factors like inner joins added for
  secondary tables and such, would have the chance of splicing a particular
  inner join to the wrong part of the query.  Additional state has been added
  to the internal method that does this splice to make a better decision as
  to where splicing should proceed.
  References: [#11449](https://www.sqlalchemy.org/trac/ticket/11449)
- Fixed bug in ORM Declarative where the `__table__` directive could not be
  declared as a class function with [declared_attr()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) on a
  superclass, including an `__abstract__` class as well as coming from the
  declarative base itself.  This was a regression since 1.4 where this was
  working, and there were apparently no tests for this particular use case.
  References: [#11509](https://www.sqlalchemy.org/trac/ticket/11509)

### engine

- Modified the internal representation used for adapting asyncio calls to
  greenlets to allow for duck-typed compatibility with third party libraries
  that implement SQLAlchemy’s “greenlet-to-asyncio” pattern directly.
  Running code within a greenlet that features the attribute
  `__sqlalchemy_greenlet_provider__ = True` will allow calls to
  `sqlalchemy.util.await_only()` directly.
  This change is also **backported** to: 1.4.53

### sql

- Fixed caching issue where using the [TextualSelect.add_cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect.add_cte) method
  of the [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect) construct would not set a correct cache key
  which distinguished between different CTE expressions.
  This change is also **backported** to: 1.4.53
  References: [#11471](https://www.sqlalchemy.org/trac/ticket/11471)
- Fixed issue when serializing an [over()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over) clause with
  unbounded range or rows.
  References: [#11422](https://www.sqlalchemy.org/trac/ticket/11422)
- Added missing methods [FunctionFilter.within_group()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.FunctionFilter.within_group)
  and [WithinGroup.filter()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.WithinGroup.filter)
  References: [#11423](https://www.sqlalchemy.org/trac/ticket/11423)
- Fixed bug in [FunctionFilter.filter()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.FunctionFilter.filter) that would mutate
  the existing function in-place. It now behaves like the rest of the
  SQLAlchemy API, returning a new instance instead of mutating the
  original one.
  References: [#11426](https://www.sqlalchemy.org/trac/ticket/11426)

### schema

- Added [Column.insert_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.insert_default) as an alias of
  [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) for compatibility with
  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column).
  References: [#11374](https://www.sqlalchemy.org/trac/ticket/11374)

### mysql

- Added missing foreign key reflection option `SET DEFAULT`
  in the MySQL and MariaDB dialects.
  Pull request courtesy of Quentin Roche.
  References: [#11285](https://www.sqlalchemy.org/trac/ticket/11285)

## 2.0.30

Released: May 5, 2024

### orm

- Added new attribute [ORMExecuteState.is_from_statement](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.is_from_statement) to
  detect statements created using [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement), and
  enhanced `FromStatement` to set [ORMExecuteState.is_select](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.is_select),
  [ORMExecuteState.is_insert](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.is_insert),
  [ORMExecuteState.is_update](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.is_update), and
  [ORMExecuteState.is_delete](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.is_delete) according to the element that is
  sent to the [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) method itself.
  References: [#11220](https://www.sqlalchemy.org/trac/ticket/11220)
- Fixed issue in  [selectin_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.selectin_polymorphic) loader option where
  attributes defined with [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) on a superclass would cause
  an internal exception on load.
  References: [#11291](https://www.sqlalchemy.org/trac/ticket/11291)
- Fixed regression from 1.4 where using [defaultload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.defaultload) in
  conjunction with a non-propagating loader like [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager)
  would nonetheless propagate the [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) to a lazy load
  operation, causing incorrect queries as this option is only intended to
  come from an original load.
  References: [#11292](https://www.sqlalchemy.org/trac/ticket/11292)
- Fixed issue in ORM Annotated Declarative where typing issue where literals
  defined using [PEP 695](https://peps.python.org/pep-0695/) type aliases would not work with inference of
  [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatypes. Pull request courtesy of Alc-Alc.
  References: [#11305](https://www.sqlalchemy.org/trac/ticket/11305)
- Fixed issue in [selectin_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.selectin_polymorphic) loader option where the
  SELECT emitted would only accommodate for the child-most class among the
  result rows that were returned, leading intermediary-class attributes to be
  unloaded if there were no concrete instances of that intermediary-class
  present in the result.   This issue only presented itself for multi-level
  inheritance hierarchies.
  References: [#11327](https://www.sqlalchemy.org/trac/ticket/11327)
- Fixed issue in [Session.bulk_save_objects()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects) where the form of the
  identity key produced when using `return_defaults=True` would be
  incorrect. This could lead to an errors during pickling as well as identity
  map mismatches.
  References: [#11332](https://www.sqlalchemy.org/trac/ticket/11332)
- Fixed issue where attribute key names in [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) would not be
  correct when using ORM enabled [select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) vs.
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query), when the statement contained duplicate column names.
  References: [#11347](https://www.sqlalchemy.org/trac/ticket/11347)

### engine

- Fixed issue in the
  [Connection.execution_options.logging_token](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.logging_token) option,
  where changing the value of `logging_token` on a connection that has
  already logged messages would not be updated to reflect the new logging
  token.  This in particular prevented the use of
  [Session.connection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) to change the option on the connection,
  since the BEGIN logging message would already have been emitted.
  References: [#11210](https://www.sqlalchemy.org/trac/ticket/11210)
- Fixed issue in cursor handling which affected handling of duplicate
  `Column` or similar objects in the columns clause of
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select), both in combination with arbitrary [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
  clauses in the SELECT list, as well as when attempting to retrieve
  [Result.mappings()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.mappings) for the object, which would lead to an
  internal error.
  References: [#11306](https://www.sqlalchemy.org/trac/ticket/11306)

### typing

- Fixed typing regression caused by [#11055](https://www.sqlalchemy.org/trac/ticket/11055) in version 2.0.29 that
  added `ParamSpec` to the asyncio `run_sync()` methods, where using
  [AsyncConnection.run_sync()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection.run_sync) with
  [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) would fail on mypy due to a mypy issue.
  Pull request courtesy of Francisco R. Del Roio.
  References: [#11200](https://www.sqlalchemy.org/trac/ticket/11200)
- Fixed issue in typing for [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) where creating a nested
  [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) structure were not allowed.

### misc

- Ensure the `PYTHONPATH` variable is properly initialized when
  using `subprocess.run` in the tests.
  References: [#11268](https://www.sqlalchemy.org/trac/ticket/11268)
- Fixed an internal class that was testing for unexpected attributes to work
  correctly under upcoming Python 3.13.   Pull request courtesy Edgar
  Ramírez-Mondragón.
  References: [#11334](https://www.sqlalchemy.org/trac/ticket/11334)

## 2.0.29

Released: March 23, 2024

### orm

- Added support for the [PEP 695](https://peps.python.org/pep-0695/) `TypeAliasType` construct as well as the
  python 3.12 native `type` keyword to work with ORM Annotated Declarative
  form when using these constructs to link to a [PEP 593](https://peps.python.org/pep-0593/) `Annotated`
  container, allowing the resolution of the `Annotated` to proceed when
  these constructs are used in a [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) typing container.
  References: [#11130](https://www.sqlalchemy.org/trac/ticket/11130)
- Fixed Declarative issue where typing a relationship using
  [Relationship](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Relationship) rather than [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) would
  inadvertently pull in the “dynamic” relationship loader strategy for that
  attribute.
  References: [#10611](https://www.sqlalchemy.org/trac/ticket/10611)
- Fixed issue in ORM annotated declarative where using
  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) with an [mapped_column.index](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.index)
  or [mapped_column.unique](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.unique) setting of False would be
  overridden by an incoming `Annotated` element that featured that
  parameter set to `True`, even though the immediate
  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) element is more specific and should take
  precedence.  The logic to reconcile the booleans has been enhanced to
  accommodate a local value of `False` as still taking precedence over an
  incoming `True` value from the annotated element.
  References: [#11091](https://www.sqlalchemy.org/trac/ticket/11091)
- Fixed regression from version 2.0.28 caused by the fix for [#11085](https://www.sqlalchemy.org/trac/ticket/11085)
  where the newer method of adjusting post-cache bound parameter values would
  interfere with the implementation for the [subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload) loader
  option, which has some more legacy patterns in use internally, when
  the additional loader criteria feature were used with this loader option.
  References: [#11173](https://www.sqlalchemy.org/trac/ticket/11173)

### engine

- Fixed issue in [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) feature where using a primary
  key column with an “inline execute” default generator such as an explicit
  [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) with an explicit schema name, while at the same time
  using the
  [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map)
  feature would fail to render the sequence or the parameters properly,
  leading to errors.
  References: [#11157](https://www.sqlalchemy.org/trac/ticket/11157)
- Made a change to the adjustment made in version 2.0.10 for [#9618](https://www.sqlalchemy.org/trac/ticket/9618),
  which added the behavior of reconciling RETURNING rows from a bulk INSERT
  to the parameters that were passed to it.  This behavior included a
  comparison of already-DB-converted bound parameter values against returned
  row values that was not always “symmetrical” for SQL column types such as
  UUIDs, depending on specifics of how different DBAPIs receive such values
  versus how they return them, necessitating the need for additional
  “sentinel value resolver” methods on these column types.  Unfortunately
  this broke third party column types such as UUID/GUID types in libraries
  like SQLModel which did not implement this special method, raising an error
  “Can’t match sentinel values in result set to parameter sets”.  Rather than
  attempt to further explain and document this implementation detail of the
  “insertmanyvalues” feature including a public version of the new
  method, the approach is instead revised to no longer need this extra
  conversion step, and the logic that does the comparison now works on the
  pre-converted bound parameter value compared to the post-result-processed
  value, which should always be of a matching datatype.  In the unusual case
  that a custom SQL column type that also happens to be used in a “sentinel”
  column for bulk INSERT is not receiving and returning the same value type,
  the “Can’t match” error will be raised, however the mitigation is
  straightforward in that the same Python datatype should be passed as that
  returned.
  References: [#11160](https://www.sqlalchemy.org/trac/ticket/11160)

### sql

- Fixed regression from the 1.4 series where the refactor of the
  [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) method introduced at
  [“with_variant()” clones the original TypeEngine rather than changing the type](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-6980) failed to accommodate for the `.copy()` method, which
  will lose the variant mappings that are set up. This becomes an issue for
  the very specific case of a “schema” type, which includes types such as
  [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) and [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), when they are then used in the context
  of an ORM Declarative mapping with mixins where copying of types comes into
  play.  The variant mapping is now copied as well.
  References: [#11176](https://www.sqlalchemy.org/trac/ticket/11176)

### typing

- Fixed typing issue allowing asyncio `run_sync()` methods to correctly
  type the parameters according to the callable that was passed, making use
  of [PEP 612](https://peps.python.org/pep-0612/) `ParamSpec` variables.  Pull request courtesy Francisco R.
  Del Roio.
  References: [#11055](https://www.sqlalchemy.org/trac/ticket/11055)

### postgresql

- The PostgreSQL dialect now returns [DOMAIN](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.DOMAIN) instances
  when reflecting a column that has a domain as type. Previously, the domain
  data type was returned instead. As part of this change, the domain
  reflection was improved to also return the collation of the text types.
  Pull request courtesy of Thomas Stephenson.
  References: [#10693](https://www.sqlalchemy.org/trac/ticket/10693)

### tests

- Backported to SQLAlchemy 2.0 an improvement to the test suite with regards
  to how asyncio related tests are run, now using the newer Python 3.11
  `asyncio.Runner` or a backported equivalent, rather than relying on the
  previous implementation based on `asyncio.get_running_loop()`.  This
  should hopefully prevent issues with large suite runs on CPU loaded
  hardware where the event loop seems to become corrupted, leading to
  cascading failures.
  References: [#11187](https://www.sqlalchemy.org/trac/ticket/11187)

## 2.0.28

Released: March 4, 2024

### orm

- Adjusted the fix made in [#10570](https://www.sqlalchemy.org/trac/ticket/10570), released in 2.0.23, where new
  logic was added to reconcile possibly changing bound parameter values
  across cache key generations used within the [with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression)
  construct.  The new logic changes the approach by which the new bound
  parameter values are associated with the statement, avoiding the need to
  deep-copy the statement which can result in a significant performance
  penalty for very deep / complex SQL constructs.  The new approach no longer
  requires this deep-copy step.
  References: [#11085](https://www.sqlalchemy.org/trac/ticket/11085)
- Fixed regression caused by [#9779](https://www.sqlalchemy.org/trac/ticket/9779) where using the “secondary” table
  in a relationship `and_()` expression would fail to be aliased to match
  how the “secondary” table normally renders within a
  [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) expression, leading to an invalid query.
  References: [#11010](https://www.sqlalchemy.org/trac/ticket/11010)

### engine

- Added new core execution option
  [Connection.execution_options.preserve_rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.preserve_rowcount). When
  set, the `cursor.rowcount` attribute from the DBAPI cursor will be
  unconditionally memoized at statement execution time, so that whatever
  value the DBAPI offers for any kind of statement will be available using
  the [CursorResult.rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount) attribute from the
  [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult).  This allows the rowcount to be accessed for
  statements such as INSERT and SELECT, to the degree supported by the DBAPI
  in use. The [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) also supports this option and
  will ensure [CursorResult.rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount) is correctly set for a
  bulk INSERT of rows when set.
  References: [#10974](https://www.sqlalchemy.org/trac/ticket/10974)

### asyncio

- An error is raised if a [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) or other non-asyncio pool class
  is passed to [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine).  This engine only
  accepts asyncio-compatible pool classes including
  [AsyncAdaptedQueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AsyncAdaptedQueuePool). Other pool classes such as
  [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool) are compatible with both synchronous and asynchronous
  engines as they do not perform any locking.
  See also
  [API Documentation - Available Pool Implementations](https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-api)
  References: [#8771](https://www.sqlalchemy.org/trac/ticket/8771)

### tests

- pytest support in the tox.ini file has been updated to support pytest 8.1.

## 2.0.27

Released: February 13, 2024

### postgresql

- Fixed regression caused by just-released fix for [#10863](https://www.sqlalchemy.org/trac/ticket/10863) where an
  invalid exception class were added to the “except” block, which does not
  get exercised unless such a catch actually happens.   A mock-style test has
  been added to ensure this catch is exercised in unit tests.
  References: [#11005](https://www.sqlalchemy.org/trac/ticket/11005)

## 2.0.26

Released: February 11, 2024

### orm

- Replaced the “loader depth is excessively deep” warning with a shorter
  message added to the caching badge within SQL logging, for those statements
  where the ORM disabled the cache due to a too-deep chain of loader options.
  The condition which this warning highlights is difficult to resolve and is
  generally just a limitation in the ORM’s application of SQL caching. A
  future feature may include the ability to tune the threshold where caching
  is disabled, but for now the warning will no longer be a nuisance.
  References: [#10896](https://www.sqlalchemy.org/trac/ticket/10896)
- Fixed issue where it was not possible to use a type (such as an enum)
  within a [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) container type if that type were declared
  locally within the class body.  The scope of locals used for the eval now
  includes that of the class body itself.  In addition, the expression within
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) may also refer to the class name itself, if used as a
  string or with future annotations mode.
  References: [#10899](https://www.sqlalchemy.org/trac/ticket/10899)
- Fixed issue where using [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) along with the
  [Mapper.version_id_col](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.version_id_col) feature would fail to use the
  correct version identifier in the case that an additional UPDATE were
  emitted against the target object as a result of the use of
  [relationship.post_update](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.post_update) on the object.  The issue is
  similar to [#10800](https://www.sqlalchemy.org/trac/ticket/10800) just fixed in version 2.0.25 for the case of
  updates alone.
  References: [#10967](https://www.sqlalchemy.org/trac/ticket/10967)
- Fixed issue where an assertion within the implementation for
  [with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) would raise if a SQL expression that was not
  cacheable were used; this was a 2.0 regression since 1.4.
  References: [#10990](https://www.sqlalchemy.org/trac/ticket/10990)

### examples

- Fixed regression in history_meta example where the use of
  `MetaData.to_metadata()` to make a copy of the history table
  would also copy indexes (which is a good thing), but causing naming
  conflicts indexes regardless of naming scheme used for those indexes. A
  “_history” suffix is now added to these indexes in the same way as is
  achieved for the table name.
  References: [#10920](https://www.sqlalchemy.org/trac/ticket/10920)
- Fixed the performance example scripts in examples/performance to mostly
  work with the Oracle database, by adding the [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) construct
  to all the tables and allowing primary generation to occur on this backend.
  A few of the “raw DBAPI” cases still are not compatible with Oracle.

### sql

- Fixed issues in [case()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.case) where the logic for determining the
  type of the expression could result in [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType) if the last
  element in the “whens” had no type, or in other cases where the type
  could resolve to `None`.  The logic has been updated to scan all
  given expressions so that the first non-null type is used, as well as
  to always ensure a type is present.  Pull request courtesy David Evans.
  References: [#10843](https://www.sqlalchemy.org/trac/ticket/10843)

### typing

- Fixed the type signature for the [PoolEvents.checkin()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.checkin) event to
  indicate that the given [DBAPIConnection](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPIConnection) argument may be `None`
  in the case where the connection has been invalidated.

### postgresql

- Added support for reflection of PostgreSQL CHECK constraints marked with
  “NO INHERIT”, setting the key `no_inherit=True` in the reflected data.
  Pull request courtesy Ellis Valentiner.
  References: [#10777](https://www.sqlalchemy.org/trac/ticket/10777)
- Support the `USING <method>` option for PostgreSQL `CREATE TABLE` to
  specify the access method to use to store the contents for the new table.
  Pull request courtesy Edgar Ramírez-Mondragón.
  See also
  [PostgreSQL Table Options](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-table-options)
  References: [#10904](https://www.sqlalchemy.org/trac/ticket/10904)
- Correctly type PostgreSQL RANGE and MULTIRANGE types as `Range[T]`
  and `Sequence[Range[T]]`.
  Introduced utility sequence [MultiRange](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.MultiRange) to allow better
  interoperability of MULTIRANGE types.
  References: [#9736](https://www.sqlalchemy.org/trac/ticket/9736)
- Differentiate between INT4 and INT8 ranges and multi-ranges types when
  inferring the database type from a [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range) or
  [MultiRange](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.MultiRange) instance, preferring INT4 if the values
  fit into it.
- Fixed regression in the asyncpg dialect caused by [#10717](https://www.sqlalchemy.org/trac/ticket/10717) in
  release 2.0.24 where the change that now attempts to gracefully close the
  asyncpg connection before terminating would not fall back to
  `terminate()` for other potential connection-related exceptions other
  than a timeout error, not taking into account cases where the graceful
  `.close()` attempt fails for other reasons such as connection errors.
  References: [#10863](https://www.sqlalchemy.org/trac/ticket/10863)
- Fixed an issue regarding the use of the [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) datatype with the
  [Uuid.as_uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid.params.as_uuid) parameter set to False, when using PostgreSQL
  dialects. ORM-optimized INSERT statements (e.g. the “insertmanyvalues”
  feature) would not correctly align primary key UUID values for bulk INSERT
  statements, resulting in errors.  Similar issues were fixed for the
  pymssql driver as well.

### mysql

- Fixed issue where NULL/NOT NULL would not be properly reflected from a
  MySQL column that also specified the VIRTUAL or STORED directives.  Pull
  request courtesy Georg Wicke-Arndt.
  References: [#10850](https://www.sqlalchemy.org/trac/ticket/10850)
- Fixed issue in asyncio dialects asyncmy and aiomysql, where their
  `.close()` method is apparently not a graceful close.  replace with
  non-standard `.ensure_closed()` method that’s awaitable and move
  `.close()` to the so-called “terminate” case.
  References: [#10893](https://www.sqlalchemy.org/trac/ticket/10893)

### mssql

- Fixed an issue regarding the use of the [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) datatype with the
  [Uuid.as_uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid.params.as_uuid) parameter set to False, when using the pymssql
  dialect. ORM-optimized INSERT statements (e.g. the “insertmanyvalues”
  feature) would not correctly align primary key UUID values for bulk INSERT
  statements, resulting in errors.  Similar issues were fixed for the
  PostgreSQL drivers as well.

### oracle

- Changed the default arraysize of the Oracle dialects so that the value set
  by the driver is used, that is 100 at the time of writing for both
  cx_oracle and oracledb. Previously the value was set to 50 by default. The
  setting of 50 could cause significant performance regressions compared to
  when using cx_oracle/oracledb alone to fetch many hundreds of rows over
  slower networks.
  References: [#10877](https://www.sqlalchemy.org/trac/ticket/10877)

## 2.0.25

Released: January 2, 2024

### orm

- Added preliminary support for Python 3.12 pep-695 type alias structures,
  when resolving custom type maps for ORM Annotated Declarative mappings.
  References: [#10807](https://www.sqlalchemy.org/trac/ticket/10807)
- Fixed issue where when making use of the
  [relationship.post_update](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.post_update) feature at the same time as using
  a mapper version_id_col could lead to a situation where the second UPDATE
  statement emitted by the post-update feature would fail to make use of the
  correct version identifier, assuming an UPDATE was already emitted in that
  flush which had already bumped the version counter.
  References: [#10800](https://www.sqlalchemy.org/trac/ticket/10800)
- Fixed issue where ORM Annotated Declarative would mis-interpret the left
  hand side of a relationship without any collection specified as
  uselist=True if the left type were given as a class and not a string,
  without using future-style annotations.
  References: [#10815](https://www.sqlalchemy.org/trac/ticket/10815)

### sql

- Improved compilation of [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) / [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_) in the
  context of a negation of boolean comparison, will now render `NOT (expr)`
  rather than reversing the equality operator to not equals, allowing
  finer-grained control of negations for these non-typical operators.
  References: [#10817](https://www.sqlalchemy.org/trac/ticket/10817)

### typing

- Fixed regressions caused by typing added to the `sqlalchemy.sql.functions`
  module in version 2.0.24, as part of [#6810](https://www.sqlalchemy.org/trac/ticket/6810):
  - Further enhancements to pep-484 typing to allow SQL functions from
    [sqlalchemy.sql.expression.func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) derived elements to work more effectively with ORM-mapped
    attributes ([#10801](https://www.sqlalchemy.org/trac/ticket/10801))
  - Fixed the argument types passed to functions so that literal expressions
    like strings and ints are again interpreted correctly ([#10818](https://www.sqlalchemy.org/trac/ticket/10818))
  References: [#10801](https://www.sqlalchemy.org/trac/ticket/10801), [#10818](https://www.sqlalchemy.org/trac/ticket/10818)

### asyncio

- Fixed critical issue in asyncio version of the connection pool where
  calling [AsyncEngine.dispose()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncEngine.dispose) would produce a new connection
  pool that did not fully re-establish the use of asyncio-compatible mutexes,
  leading to the use of a plain `threading.Lock()` which would then cause
  deadlocks in an asyncio context when using concurrency features like
  `asyncio.gather()`.
  This change is also **backported** to: 1.4.51
  References: [#10813](https://www.sqlalchemy.org/trac/ticket/10813)

### oracle

- Added support for [python-oracledb](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracledb) in asyncio mode, using the newly released
  version of the `oracledb` DBAPI that includes asyncio support. For the
  2.0 series, this is a preview release, where the current implementation
  does not yet have include support for
  [AsyncConnection.stream()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection.stream). Improved support is planned for
  the 2.1 release of SQLAlchemy.
  References: [#10679](https://www.sqlalchemy.org/trac/ticket/10679)

## 2.0.24

Released: December 28, 2023

### orm

- Improved a fix first implemented for [#3208](https://www.sqlalchemy.org/trac/ticket/3208) released in version
  0.9.8, where the registry of classes used internally by declarative could
  be subject to a race condition in the case where individual mapped classes
  are being garbage collected at the same time while new mapped classes are
  being constructed, as can happen in some test suite configurations or
  dynamic class creation environments.   In addition to the weakref check
  already added, the list of items being iterated is also copied first to
  avoid “list changed while iterating” errors.  Pull request courtesy Yilei
  Yang.
  This change is also **backported** to: 1.4.51
  References: [#10782](https://www.sqlalchemy.org/trac/ticket/10782)
- Fixed issue where use of [foreign()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.foreign) annotation on a
  non-initialized [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct would produce an
  expression without a type, which was then not updated at initialization
  time of the actual column, leading to issues such as relationships not
  determining `use_get` appropriately.
  References: [#10597](https://www.sqlalchemy.org/trac/ticket/10597)
- Improved the error message produced when the unit of work process sets the
  value of a primary key column to NULL due to a related object with a
  dependency rule on that column being deleted, to include not just the
  destination object and column name but also the source column from which
  the NULL value is originating.  Pull request courtesy Jan Vollmer.
  References: [#10668](https://www.sqlalchemy.org/trac/ticket/10668)
- Modified the `__init_subclass__()` method used by
  [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass), [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) and
  [DeclarativeBaseNoMeta](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta) to accept arbitrary `**kw` and to
  propagate them to the `super()` call, allowing greater flexibility in
  arranging custom superclasses and mixins which make use of
  `__init_subclass__()` keyword arguments.  Pull request courtesy Michael
  Oliver.
  References: [#10732](https://www.sqlalchemy.org/trac/ticket/10732)
- Ensured the use case of [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) objects used in the
  `returning()` portion of ORM-enabled INSERT, UPDATE and DELETE statements
  is tested and works fully.   This was never explicitly implemented or
  tested previously and did not work correctly in the 1.4 series; in the 2.0
  series, ORM UPDATE/DELETE with WHERE criteria was missing an implementation
  method preventing [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) objects from working.
  References: [#10776](https://www.sqlalchemy.org/trac/ticket/10776)
- Fixed 2.0 regression in [MutableList](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList) where a routine that detects
  sequences would not correctly filter out string or bytes instances, making
  it impossible to assign a string value to a specific index (while
  non-sequence values would work fine).
  References: [#10784](https://www.sqlalchemy.org/trac/ticket/10784)

### engine

- Fixed URL-encoding of the username and password components of
  [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) objects when converting them to string using the
  [URL.render_as_string()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.render_as_string) method, by using Python standard
  library `urllib.parse.quote` while allowing for plus signs and spaces to
  remain unchanged as supported by SQLAlchemy’s non-standard URL parsing,
  rather than the legacy home-grown routine from many years ago. Pull request
  courtesy of Xavier NUNN.
  References: [#10662](https://www.sqlalchemy.org/trac/ticket/10662)

### sql

- Fixed issue in stringify for SQL elements, where a specific dialect is not
  passed,  where a dialect-specific element such as the PostgreSQL “on
  conflict do update” construct is encountered and then fails to provide for
  a stringify dialect with the appropriate state to render the construct,
  leading to internal errors.
  References: [#10753](https://www.sqlalchemy.org/trac/ticket/10753)
- Fixed issue where stringifying or compiling a [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) that was
  against a DML construct such as an [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct would fail
  to stringify, due to a mis-detection that the statement overall is an
  INSERT, leading to internal errors.

### schema

- Fixed issue where error reporting for unexpected schema item when creating
  objects like [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) would incorrectly handle an argument
  that was itself passed as a tuple, leading to a formatting error.  The
  error message has been modernized to use f-strings.
  References: [#10654](https://www.sqlalchemy.org/trac/ticket/10654)

### typing

- Completed pep-484 typing for the `sqlalchemy.sql.functions` module.
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) constructs made against `func` elements should now
  have filled-in return types.
  References: [#6810](https://www.sqlalchemy.org/trac/ticket/6810)

### asyncio

- The `async_fallback` dialect argument is now deprecated, and will be
  removed in SQLAlchemy 2.1.   This flag has not been used for SQLAlchemy’s
  test suite for some time.   asyncio dialects can still run in a synchronous
  style by running code within a greenlet using `greenlet_spawn()`.

### postgresql

- Adjusted the asyncpg dialect such that when the `terminate()` method is
  used to discard an invalidated connection, the dialect will first attempt
  to gracefully close the connection using `.close()` with a timeout, if
  the operation is proceeding within an async event loop context only. This
  allows the asyncpg driver to attend to finalizing a `TimeoutError`
  including being able to close a long-running query server side, which
  otherwise can keep running after the program has exited.
  References: [#10717](https://www.sqlalchemy.org/trac/ticket/10717)

### mysql

- Fixed regression introduced by the fix in ticket [#10492](https://www.sqlalchemy.org/trac/ticket/10492) when using
  pool pre-ping with PyMySQL version older than 1.0.
  This change is also **backported** to: 1.4.51
  References: [#10650](https://www.sqlalchemy.org/trac/ticket/10650)

### tests

- Improvements to the test suite to further harden its ability to run
  when Python `greenlet` is not installed.   There is now a tox
  target that includes the token “nogreenlet” that will run the suite
  with greenlet not installed (note that it still temporarily installs
  greenlet as part of the tox config, however).
  References: [#10747](https://www.sqlalchemy.org/trac/ticket/10747)

## 2.0.23

Released: November 2, 2023

### orm

- Implemented the [Session.bulk_insert_mappings.render_nulls](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings.params.render_nulls)
  parameter for new style bulk ORM inserts, allowing `render_nulls=True` as
  an execution option.   This allows for bulk ORM inserts with a mixture of
  `None` values in the parameter dictionaries to use a single batch of rows
  for a given set of dictionary keys, rather than breaking up into batches
  that omit the NULL columns from each INSERT.
  See also
  [Sending NULL values in ORM bulk INSERT statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-insert-null-params)
  References: [#10575](https://www.sqlalchemy.org/trac/ticket/10575)
- Fixed issue where the `__allow_unmapped__` directive failed to allow for
  legacy [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) / [deferred()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.deferred) mappings that nonetheless had
  annotations such as `Any` or a specific type without `Mapped[]` as
  their type, without errors related to locating the attribute name.
  References: [#10516](https://www.sqlalchemy.org/trac/ticket/10516)
- Fixed caching bug where using the [with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) construct in
  conjunction with loader options [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload),
  [lazyload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.lazyload) would fail to substitute bound parameter values
  correctly on subsequent caching runs.
  References: [#10570](https://www.sqlalchemy.org/trac/ticket/10570)
- Fixed bug in ORM annotated declarative where using a `ClassVar` that
  nonetheless referred in some way to an ORM mapped class name would fail to
  be interpreted as a `ClassVar` that’s not mapped.
  References: [#10472](https://www.sqlalchemy.org/trac/ticket/10472)

### sql

- Implemented “literal value processing” for the [Interval](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Interval) datatype
  for both the PostgreSQL and Oracle dialects, allowing literal rendering of
  interval values.  Pull request courtesy Indivar Mishra.
  References: [#9737](https://www.sqlalchemy.org/trac/ticket/9737)
- Fixed issue where using the same bound parameter more than once with
  `literal_execute=True` in some combinations with other literal rendering
  parameters would cause the wrong values to render due to an iteration
  issue.
  This change is also **backported** to: 1.4.50
  References: [#10142](https://www.sqlalchemy.org/trac/ticket/10142)
- Added compiler-level None/NULL handling for the “literal processors” of all
  datatypes that include literal processing, that is, where a value is
  rendered inline within a SQL statement rather than as a bound parameter,
  for all those types that do not feature explicit “null value” handling.
  Previously this behavior was undefined and inconsistent.
  References: [#10535](https://www.sqlalchemy.org/trac/ticket/10535)
- Removed unused placeholder method `TypeEngine.compare_against_backend()`
  This method was used by very old versions of Alembic.
  See [https://github.com/sqlalchemy/alembic/issues/1293](https://github.com/sqlalchemy/alembic/issues/1293) for details.

### asyncio

- Fixed bug with method [AsyncSession.close_all()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.close_all)
  that was not working correctly.
  Also added function [close_all_sessions()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.close_all_sessions) that’s
  the equivalent of [close_all_sessions()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.close_all_sessions).
  Pull request courtesy of Bryan不可思议.
  References: [#10421](https://www.sqlalchemy.org/trac/ticket/10421)

### postgresql

- Fixed 2.0 regression caused by [#7744](https://www.sqlalchemy.org/trac/ticket/7744) where chains of expressions
  involving PostgreSQL JSON operators combined with other operators such as
  string concatenation would lose correct parenthesization, due to an
  implementation detail specific to the PostgreSQL dialect.
  References: [#10479](https://www.sqlalchemy.org/trac/ticket/10479)
- Fixed SQL handling for “insertmanyvalues” when using the
  [BIT](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.BIT) datatype with the asyncpg backend.  The
  [BIT](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.BIT) on asyncpg apparently requires the use of an
  asyncpg-specific `BitString` type which is currently exposed when using
  this DBAPI, making it incompatible with other PostgreSQL DBAPIs that all
  work with plain bitstrings here.  A future fix in version 2.1 will
  normalize this datatype across all PG backends.   Pull request courtesy
  Sören Oldag.
  References: [#10532](https://www.sqlalchemy.org/trac/ticket/10532)

### mysql

- Repaired a new incompatibility in the MySQL “pre-ping” routine where the
  `False` argument passed to `connection.ping()`, which is intended to
  disable an unwanted “automatic reconnect” feature,  is being deprecated in
  MySQL drivers and backends, and is producing warnings for some versions of
  MySQL’s native client drivers.  It’s removed for mysqlclient, whereas for
  PyMySQL and drivers based on PyMySQL, the parameter will be deprecated and
  removed at some point, so API introspection is used to future proof against
  these various stages of removal.
  This change is also **backported** to: 1.4.50
  References: [#10492](https://www.sqlalchemy.org/trac/ticket/10492)

### mariadb

- Adjusted the MySQL / MariaDB dialects to default a generated column to NULL
  when using MariaDB, if [Column.nullable](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.nullable) was not
  specified with an explicit `True` or `False` value, as MariaDB does not
  support the “NOT NULL” phrase with a generated column.  Pull request
  courtesy Indivar.
  References: [#10056](https://www.sqlalchemy.org/trac/ticket/10056)
- Established a workaround for what seems to be an intrinsic issue across
  MySQL/MariaDB drivers where a RETURNING result for DELETE DML which returns
  no rows using SQLAlchemy’s “empty IN” criteria fails to provide a
  cursor.description, which then yields result that returns no rows,
  leading to regressions for the ORM that in the 2.0 series uses RETURNING
  for bulk DELETE statements for the “synchronize session” feature. To
  resolve, when the specific case of “no description when RETURNING was
  given” is detected, an “empty result” with a correct cursor description is
  generated and used in place of the non-working cursor.
  References: [#10505](https://www.sqlalchemy.org/trac/ticket/10505)

### mssql

- Added support for the `aioodbc` driver implemented for SQL Server,
  which builds on top of the pyodbc and general aio* dialect architecture.
  See also
  [aioodbc](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-aioodbc) - in the SQL Server dialect documentation.
  References: [#6521](https://www.sqlalchemy.org/trac/ticket/6521)
- Fixed issue where identity column reflection would fail
  for a bigint column with a large identity start value
  (more than 18 digits).
  This change is also **backported** to: 1.4.50
  References: [#10504](https://www.sqlalchemy.org/trac/ticket/10504)

### oracle

- Fixed issue in [Interval](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Interval) datatype where the Oracle implementation
  was not being used for DDL generation, leading to the `day_precision` and
  `second_precision` parameters to be ignored, despite being supported by
  this dialect.  Pull request courtesy Indivar.
  References: [#10509](https://www.sqlalchemy.org/trac/ticket/10509)
- Fixed issue where the cx_Oracle dialect claimed to support a lower
  cx_Oracle version (7.x) than was actually supported in practice within the
  2.0 series of SQLAlchemy. The dialect imports symbols that are only in
  cx_Oracle 8 or higher, so runtime dialect checks as well as setup.cfg
  requirements have been updated to reflect this compatibility.
  References: [#10470](https://www.sqlalchemy.org/trac/ticket/10470)

## 2.0.22

Released: October 12, 2023

### orm

- Added method [Session.get_one()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_one) that behaves like
  [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) but raises an exception instead of returning
  `None` if no instance was found with the provided primary key.
  Pull request courtesy of Carlos Sousa.
  References: [#10202](https://www.sqlalchemy.org/trac/ticket/10202)
- Added an option to permanently close sessions.
  Set to `False` the new parameter [Session.close_resets_only](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.close_resets_only)
  will prevent a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) from performing any other
  operation after [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) has been called.
  Added new method [Session.reset()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.reset) that will reset a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  to its initial state. This is an alias of [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close),
  unless [Session.close_resets_only](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.close_resets_only) is set to `False`.
  References: [#7787](https://www.sqlalchemy.org/trac/ticket/7787)
- Fixed a wide range of [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) parameters that were not
  being transferred when using the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) object inside
  of a pep-593 `Annotated` object, including
  [mapped_column.sort_order](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.sort_order),
  [mapped_column.deferred](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.deferred),
  [mapped_column.autoincrement](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.autoincrement),
  [mapped_column.system](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.system), [mapped_column.info](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.info)
  etc.
  Additionally, it remains not supported to have dataclass arguments, such as
  [mapped_column.kw_only](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.kw_only),
  [mapped_column.default_factory](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default_factory) etc. indicated within the
  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) received by `Annotated`, as this is not
  supported with pep-681 Dataclass Transforms.  A warning is now emitted when
  these parameters are used within `Annotated` in this way (and they
  continue to be ignored).
  References: [#10046](https://www.sqlalchemy.org/trac/ticket/10046), [#10369](https://www.sqlalchemy.org/trac/ticket/10369)
- Fixed issue where calling [Result.unique()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.unique) with a new-style
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) query in the ORM, where one or more columns yields values
  that are of “unknown hashability”, typically when using JSON functions like
  `func.json_build_object()` without providing a type, would fail
  internally when the returned values were not actually hashable. The
  behavior is repaired to test the objects as they are received for
  hashability in this case, raising an informative error message if not. Note
  that for values of “known unhashability”, such as when the
  [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) or [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) types are used directly, an
  informative error message was already raised.
  The “hashabiltiy testing” fix here is applied to legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) as
  well, however in the legacy case, [Result.unique()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.unique) is used for
  nearly all queries, so no new warning is emitted here; the legacy behavior
  of falling back to using `id()` in this case is maintained, with the
  improvement that an unknown type that turns out to be hashable will now be
  uniqufied, whereas previously it would not.
  References: [#10459](https://www.sqlalchemy.org/trac/ticket/10459)
- Fixed regression in recently revised “insertmanyvalues” feature (likely
  issue [#9618](https://www.sqlalchemy.org/trac/ticket/9618)) where the ORM would inadvertently attempt to
  interpret a non-RETURNING result as one with RETURNING, in the case where
  the `implicit_returning=False` parameter were applied to the mapped
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), indicating that “insertmanyvalues” cannot be used if the
  primary key values are not provided.
  References: [#10453](https://www.sqlalchemy.org/trac/ticket/10453)
- Fixed bug where ORM [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) would not apply
  itself to a [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join) where the ON clause were given as a
  plain SQL comparison, rather than as a relationship target or similar.
  **update** - this was found to also fix an issue where
  single-inheritance criteria would not be correctly applied to a
  subclass entity that only appeared in the `select_from()` list,
  see [#11412](https://www.sqlalchemy.org/trac/ticket/11412)
  References: [#10365](https://www.sqlalchemy.org/trac/ticket/10365), [#11412](https://www.sqlalchemy.org/trac/ticket/11412)
- Fixed issue where [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) symbols like [WriteOnlyMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyMapped)
  and [DynamicMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.DynamicMapped) could not be correctly resolved when referenced
  as an element of a sub-module in the given annotation, assuming
  string-based or “future annotations” style annotations.
  References: [#10412](https://www.sqlalchemy.org/trac/ticket/10412)
- Fixed issue with `__allow_unmapped__` declarative option
  where types that were declared using collection types such as
  `list[SomeClass]` vs. the typing construct `List[SomeClass]`
  would fail to be recognized correctly.  Pull request courtesy
  Pascal Corpet.
  References: [#10385](https://www.sqlalchemy.org/trac/ticket/10385)

### engine

- Fixed issue within some dialects where the dialect could incorrectly return
  an empty result set for an INSERT statement that does not actually return
  rows at all, due to artfacts from pre- or post-fetching the primary key of
  the row or rows still being present.  Affected dialects included asyncpg,
  all mssql dialects.
- Fixed issue where under some garbage collection / exception scenarios the
  connection pool’s cleanup routine would raise an error due to an unexpected
  set of state, which can be reproduced under specific conditions.
  References: [#10414](https://www.sqlalchemy.org/trac/ticket/10414)

### sql

- Fixed issue where referring to a FROM entry in the SET clause of an UPDATE
  statement would not include it in the FROM clause of the UPDATE statement,
  if that entry were nowhere else in the statement; this occurs currently for
  CTEs that were added using `Update.add_cte()` to provide the desired
  CTE at the top of the statement.
  References: [#10408](https://www.sqlalchemy.org/trac/ticket/10408)
- Fixed 2.0 regression where the [DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DDL) construct would no longer
  `__repr__()` due to the removed `on` attribute not being accommodated.
  Pull request courtesy Iuri de Silvio.
  References: [#10443](https://www.sqlalchemy.org/trac/ticket/10443)

### typing

- Fixed typing issue where the argument list passed to [Values](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values) was
  too-restrictively tied to `List` rather than `Sequence`.  Pull request
  courtesy Iuri de Silvio.
  References: [#10451](https://www.sqlalchemy.org/trac/ticket/10451)
- Updates to the codebase to support Mypy 1.6.0.

### asyncio

- Fixed the [AsyncSession.get.execution_options](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.get.params.execution_options) parameter
  which was not being propagated to the underlying [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and
  was instead being ignored.

### mariadb

- Modified the mariadb-connector driver to pre-load the `cursor.rowcount`
  value for all queries, to suit tools such as Pandas that hardcode to
  calling `Result.rowcount` in this way. SQLAlchemy normally pre-loads
  `cursor.rowcount` only for UPDATE/DELETE statements and otherwise passes
  through to the DBAPI where it can return -1 if no value is available.
  However, mariadb-connector does not support invoking `cursor.rowcount`
  after the cursor itself is closed, raising an error instead.  Generic test
  support has been added to ensure all backends support the allowing
  `Result.rowcount` to succeed (that is, returning an integer
  value with -1 for “not available”) after the result is closed.
  References: [#10396](https://www.sqlalchemy.org/trac/ticket/10396)
- Additional fixes for the mariadb-connector dialect to support UUID data
  values in the result in INSERT..RETURNING statements.

### mssql

- Fixed bug where the rule that prevents ORDER BY from emitting within
  subqueries on SQL Server was not being disabled in the case where the
  `select.fetch()` method were used to limit rows in conjunction with
  WITH TIES or PERCENT, preventing valid subqueries with TOP / ORDER BY from
  being used.
  References: [#10458](https://www.sqlalchemy.org/trac/ticket/10458)

## 2.0.21

Released: September 18, 2023

### orm

- Adjusted the ORM’s interpretation of the “target” entity used within
  [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) to not interfere with the target
  “from” object passed to the statement, such as when passing an ORM-mapped
  [aliased](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct that should be maintained within a phrase
  like “UPDATE FROM”.  Cases like ORM session synchronize using “SELECT”
  statements such as with MySQL/ MariaDB will still have issues with
  UPDATE/DELETE of this form so it’s best to disable synchonize_session when
  using DML statements of this type.
  References: [#10279](https://www.sqlalchemy.org/trac/ticket/10279)
- Added new capability to the [selectin_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.selectin_polymorphic) loader option
  which allows other loader options to be bundled as siblings, referring to
  one of its subclasses, within the sub-options of parent loader option.
  Previously, this pattern was only supported if the
  [selectin_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.selectin_polymorphic) were at the top level of the options for
  the query.   See new documentation section for example.
  As part of this change, improved the behavior of the
  [Load.selectin_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load.selectin_polymorphic) method / loader strategy so that the
  subclass load does not load most already-loaded columns from the parent
  table, when the option is used against a class that is already being
  relationship-loaded.  Previously, the logic to load only the subclass
  columns worked only for a top level class load.
  See also
  [Applying loader options when selectin_polymorphic is itself a sub-option](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#polymorphic-selectin-as-loader-option-target-plus-opts)
  References: [#10348](https://www.sqlalchemy.org/trac/ticket/10348)

### engine

- Fixed a series of reflection issues affecting the PostgreSQL,
  MySQL/MariaDB, and SQLite dialects when reflecting foreign key constraints
  where the target column contained parenthesis in one or both of the table
  name or column name.
  References: [#10275](https://www.sqlalchemy.org/trac/ticket/10275)

### sql

- Adjusted the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatype to accept an argument of
  `None` for the [Enum.length](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.length) parameter, resulting in a
  VARCHAR or other textual type with no length in the resulting DDL. This
  allows for new elements of any length to be added to the type after it
  exists in the schema.  Pull request courtesy Eugene Toder.
  References: [#10269](https://www.sqlalchemy.org/trac/ticket/10269)
- Added new generic SQL function [aggregate_strings](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.aggregate_strings), which
  accepts a SQL expression and a decimeter, concatenating strings on multiple
  rows into a single aggregate value. The function is compiled on a
  per-backend basis, into functions such as `group_concat(),` `string_agg()`, or `LISTAGG()`.
  Pull request courtesy Joshua Morris.
  References: [#9873](https://www.sqlalchemy.org/trac/ticket/9873)
- Adjusted the operator precedence for the string concatenation operator to
  be equal to that of string matching operators, such as
  [ColumnElement.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.like), [ColumnElement.regexp_match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.regexp_match),
  [ColumnElement.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.match), etc., as well as plain `==` which has the
  same precedence as string comparison operators, so that parenthesis will be
  applied to a string concatenation expression that follows a string match
  operator. This provides for backends such as PostgreSQL where the “regexp
  match” operator is apparently of higher precedence than the string
  concatenation operator.
  References: [#9610](https://www.sqlalchemy.org/trac/ticket/9610)
- Qualified the use of `hashlib.md5()` within the DDL compiler, which is
  used to generate deterministic four-character suffixes for long index and
  constraint names in DDL statements, to include the Python 3.9+
  `usedforsecurity=False` parameter so that Python interpreters built for
  restricted environments such as FIPS do not consider this call to be
  related to security concerns.
  References: [#10342](https://www.sqlalchemy.org/trac/ticket/10342)
- The [Values](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values) construct will now automatically create a proxy (i.e.
  a copy) of a [column](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) if the column were already associated
  with an existing FROM clause.  This allows that an expression like
  `values_obj.c.colname` will produce the correct FROM clause even in the
  case that `colname` was passed as a [column](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) that was already
  used with a previous [Values](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values) or other table construct.
  Originally this was considered to be a candidate for an error condition,
  however it’s likely this pattern is already in widespread use so it’s
  now added to support.
  References: [#10280](https://www.sqlalchemy.org/trac/ticket/10280)

### schema

- Modified the rendering of the Oracle only [Identity.order](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity.params.order)
  parameter that’s part of both [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) and [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) to
  only take place for the Oracle backend, and not other backends such as that
  of PostgreSQL.  A future release will rename the
  [Identity.order](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity.params.order), [Sequence.order](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.order)  and
  [Identity.on_null](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity.params.on_null) parameters to Oracle-specific names,
  deprecating the old names, these parameters only apply to Oracle.
  This change is also **backported** to: 1.4.50
  References: [#10207](https://www.sqlalchemy.org/trac/ticket/10207)

### typing

- Made the contained type for [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) covariant; this is to allow
  greater flexibility for end-user typing scenarios, such as the use of
  protocols to represent particular mapped class structures that are passed
  to other functions. As part of this change, the contained type was also
  made covariant for dependent and related types such as
  `SQLORMOperations`, [WriteOnlyMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyMapped), and
  [SQLColumnExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.SQLColumnExpression). Pull request courtesy Roméo Després.
  References: [#10288](https://www.sqlalchemy.org/trac/ticket/10288)
- Fixed regression introduced in 2.0.20 via [#9600](https://www.sqlalchemy.org/trac/ticket/9600) fix which
  attempted to add more formal typing to
  [MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention). This change prevented basic
  naming convention dictionaries from passing typing and has been adjusted so
  that a plain dictionary of strings for keys as well as dictionaries that
  use constraint types as keys or a mix of both, are again accepted.
  As part of this change, lesser used forms of the naming convention
  dictionary are also typed, including that it currently allows for
  `Constraint` type objects as keys as well.
  References: [#10264](https://www.sqlalchemy.org/trac/ticket/10264), [#9284](https://www.sqlalchemy.org/trac/ticket/9284)
- Fixed the type annotation for `__class_getitem__()` as applied to the
  `Visitable` class at the base of expression constructs to accept `Any`
  for a key, rather than `str`, which helps with some IDEs such as PyCharm
  when attempting to write typing annotations for SQL constructs which
  include generic selectors.  Pull request courtesy Jordan Macdonald.
  References: [#9878](https://www.sqlalchemy.org/trac/ticket/9878)
- Repaired the core “SQL element” class `SQLCoreOperations` to support the
  `__hash__()` method from a typing perspective, as objects like
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) and ORM [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute) are hashable and
  are used as dictionary keys in the public API for the [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)
  and [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) constructs.  Previously, type checkers were not
  aware the root SQL element was hashable.
  References: [#10353](https://www.sqlalchemy.org/trac/ticket/10353)
- Fixed typing issue with `Existing.select_from()` that
  prevented its use with ORM classes.
  References: [#10337](https://www.sqlalchemy.org/trac/ticket/10337)
- Update type annotations for ORM loading options, restricting them to accept
  only “*” instead of any string for string arguments.  Pull request
  courtesy Janek Nouvertné.
  References: [#10131](https://www.sqlalchemy.org/trac/ticket/10131)

### postgresql

- Fixed regression which appeared in 2.0 due to [#8491](https://www.sqlalchemy.org/trac/ticket/8491) where the
  revised “ping” used for PostgreSQL dialects when the
  [create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) parameter is in use would
  interfere with the use of asyncpg with PGBouncer “transaction” mode, as the
  multiple PostgreSQL commands emitted by asnycpg could be broken out among
  multiple connections leading to errors, due to the lack of any transaction
  around this newly revised “ping”.   The ping is now invoked within a
  transaction, in the same way that is implicit with all other backends that
  are based on the pep-249 DBAPI; this guarantees that the series of PG
  commands sent by asyncpg for this command are invoked on the same backend
  connection without it jumping to a different connection mid-command.  The
  transaction is not used if the asyncpg dialect is used in “AUTOCOMMIT”
  mode, which remains incompatible with pgbouncer transaction mode.
  References: [#10226](https://www.sqlalchemy.org/trac/ticket/10226)

### misc

- Fixed very old issue where the full extent of SQLAlchemy modules, including
  `sqlalchemy.testing.fixtures`, could not be imported outside of a pytest
  run. This suits inspection utilities such as `pkgutil` that attempt to
  import all installed modules in all packages.
  References: [#10321](https://www.sqlalchemy.org/trac/ticket/10321)

## 2.0.20

Released: August 15, 2023

### orm

- Implemented the “RETURNING ‘*’” use case for ORM enabled DML statements.
  This will render in as many cases as possible and return the unfiltered
  result set, however is not supported for multi-parameter “ORM bulk INSERT”
  statements that have specific column rendering requirements.
  References: [#10192](https://www.sqlalchemy.org/trac/ticket/10192)
- Fixed fundamental issue which prevented some forms of ORM “annotations”
  from taking place for subqueries which made use of [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join)
  against a relationship target.  These annotations are used whenever a
  subquery is used in special situations such as within
  [PropComparator.and_()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.and_) and other ORM-specific scenarios.
  This change is also **backported** to: 1.4.50
  References: [#10223](https://www.sqlalchemy.org/trac/ticket/10223)
- Fixed issue where the ORM’s generation of a SELECT from a joined
  inheritance model with same-named columns in superclass and subclass would
  somehow not send the correct list of column names to the [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE)
  construct, when the RECURSIVE column list were generated.
  References: [#10169](https://www.sqlalchemy.org/trac/ticket/10169)
- Fixed fairly major issue where execution options passed to
  [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), as well as execution options local to the ORM
  executed statement itself, would not be propagated along to eager loaders
  such as that of [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload), [immediateload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.immediateload), and
  [sqlalchemy.orm.subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload), making it impossible to do things such as
  disabling the cache for a single statement or using
  `schema_translate_map` for a single statement, as well as the use of
  user-custom execution options.   A change has been made where **all**
  user-facing execution options present for [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) will
  be propagated along to additional loaders.
  As part of this change, the warning for “excessively deep” eager loaders
  leading to caching being disabled can be silenced on a per-statement
  basis by sending `execution_options={"compiled_cache": None}` to
  [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), which will disable caching for the full
  series of statements within that scope.
  References: [#10231](https://www.sqlalchemy.org/trac/ticket/10231)
- Fixed issue where internal cloning used by the ORM for expressions like
  `Comparator.any()` to produce correlated EXISTS
  constructs would interfere with the “cartesian product warning” feature of
  the SQL compiler, leading the SQL compiler to warn when all elements of the
  statement were correctly joined.
  References: [#10124](https://www.sqlalchemy.org/trac/ticket/10124)
- Fixed issue where the `lazy="immediateload"` loader strategy would place
  an internal loading token into the ORM mapped attribute under circumstances
  where the load should not occur, such as in a recursive self-referential
  load.   As part of this change, the `lazy="immediateload"` strategy now
  honors the [relationship.join_depth](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.join_depth) parameter for
  self-referential eager loads in the same way as that of other eager
  loaders, where leaving it unset or set at zero will lead to a
  self-referential immediateload not occurring, setting it to a value of one
  or greater will immediateload up until that given depth.
  References: [#10139](https://www.sqlalchemy.org/trac/ticket/10139)
- Fixed issue where dictionary-based collections such as
  [attribute_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict) did not fully pickle/unpickle correctly,
  leading to issues when attempting to mutate such a collection after
  unpickling.
  References: [#10175](https://www.sqlalchemy.org/trac/ticket/10175)
- Fixed issue where chaining [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) or other wildcard use of
  [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) from another eager loader using a [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
  against a joined inheritance subclass would fail to take effect for columns
  local to the superclass.
  References: [#10125](https://www.sqlalchemy.org/trac/ticket/10125)
- Fixed issue where an ORM-enabled [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct would not
  render any CTEs added only via the [Select.add_cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.add_cte) method that
  were not otherwise referenced in the statement.
  References: [#10167](https://www.sqlalchemy.org/trac/ticket/10167)

### examples

- The dogpile_caching examples have been updated for 2.0 style queries.
  Within the “caching query” logic itself there is one conditional added to
  differentiate between `Query` and `select()` when performing an
  invalidation operation.

### engine

- Fixed critical issue where setting
  [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) to `AUTOCOMMIT` (as opposed
  to using the [Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options) method) would fail to
  restore “autocommit” to a pooled connection if an alternate isolation level
  were temporarily selected using
  [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level).
  References: [#10147](https://www.sqlalchemy.org/trac/ticket/10147)

### sql

- Fixed issue where unpickling of a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or other
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) would fail to restore the correct “comparator”
  object, which is used to generate SQL expressions specific to the type
  object.
  This change is also **backported** to: 1.4.50
  References: [#10213](https://www.sqlalchemy.org/trac/ticket/10213)

### typing

- Added new typing only utility functions [Nullable()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.Nullable) and
  [NotNullable()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.NotNullable) to type a column or ORM class as, respectively,
  nullable or not nullable.
  These function are no-op at runtime, returning the input unchanged.
  References: [#10173](https://www.sqlalchemy.org/trac/ticket/10173)
- Typing improvements:
  - [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) is returned for some forms of
    [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) where DML without RETURNING is used
  - fixed type for [Query.with_for_update.of](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_for_update.params.of) parameter within
    [Query.with_for_update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_for_update)
  - improvements to `_DMLColumnArgument` type used by some DML methods to
    pass column expressions
  - Add overload to [literal()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal) so that it is inferred that the
    return type is `BindParameter[NullType]` where
    [literal.type_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal.params.type_) param is None
  - Add overloads to [ColumnElement.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.op) so that the inferred
    type when [ColumnElement.op.return_type](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.op.params.return_type) is not provided
    is `Callable[[Any], BinaryExpression[Any]]`
  - Add missing overload to `ColumnElement.__add__()`
  Pull request courtesy Mehdi Gmira.
  References: [#9185](https://www.sqlalchemy.org/trac/ticket/9185)
- Fixed issue in [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession)
  methods such as [Session.connection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) where the
  [Session.connection.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection.params.execution_options) parameter were
  hardcoded to an internal type that is not user-facing.
  References: [#10182](https://www.sqlalchemy.org/trac/ticket/10182)

### asyncio

- Added new methods [AsyncConnection.aclose()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection.aclose) as a synonym for
  [AsyncConnection.close()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection.close) and
  [AsyncSession.aclose()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.aclose) as a synonym for
  [AsyncSession.close()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.close) to the
  [AsyncConnection](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection) and [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession)
  objects, to provide compatibility with Python standard library
  `@contextlib.aclosing` construct. Pull request courtesy Grigoriev Semyon.
  References: [#9698](https://www.sqlalchemy.org/trac/ticket/9698)

### mysql

- Updated aiomysql dialect since the dialect appears to be maintained again.
  Re-added to the ci testing using version 0.2.0.
  This change is also **backported** to: 1.4.50

## 2.0.19

Released: July 15, 2023

### orm

- Fixed issue where setting a relationship collection directly, where an
  object in the new collection were already present, would not trigger a
  cascade event for that object, leading to it not being added to the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) if it were not already present.  This is similar in
  nature to [#6471](https://www.sqlalchemy.org/trac/ticket/6471) and is a more apparent issue due to the removal of
  `cascade_backrefs` in the 2.0 series.  The
  [AttributeEvents.append_wo_mutation()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.append_wo_mutation) event added as part of
  [#6471](https://www.sqlalchemy.org/trac/ticket/6471) is now also emitted for existing members of a collection
  that are present in a bulk set of that same collection.
  References: [#10089](https://www.sqlalchemy.org/trac/ticket/10089)
- Fixed issue where objects that were associated with an unloaded collection
  via backref, but were not merged into the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) due to the
  removal of `cascade_backrefs` in the 2.0 series, would not emit a warning
  that these objects were not being included in a flush, even though they
  were pending members of the collection; in other such cases, a warning is
  emitted when a collection being flushed contains non-attached objects which
  will be essentially discarded.  The addition of the warning for
  backref-pending collection members establishes greater consistency with
  collections that may be present or non-present and possibly flushed or not
  flushed at different times based on different relationship loading
  strategies.
  References: [#10090](https://www.sqlalchemy.org/trac/ticket/10090)
- Fixed additional regression caused by [#9805](https://www.sqlalchemy.org/trac/ticket/9805) where more aggressive
  propagation of the “ORM” flag on statements could lead to an internal
  attribute error when embedding an ORM [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) construct that
  nonetheless contained no ORM entities within a Core SQL statement, in this
  case ORM-enabled UPDATE and DELETE statements.
  References: [#10098](https://www.sqlalchemy.org/trac/ticket/10098)

### engine

- Renamed [Row.t](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row.t) and [Row.tuple()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row.tuple) to
  [Row._t](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row._t) and [Row._tuple()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row._tuple); this is to suit the
  policy that all methods and pre-defined attributes on [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) should
  be in the style of Python standard library `namedtuple` where all fixed
  names have a leading underscore, to avoid name conflicts with existing
  column names.   The previous method/attribute is now deprecated and will
  emit a deprecation warning.
  References: [#10093](https://www.sqlalchemy.org/trac/ticket/10093)
- Added detection for non-string, non-[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) objects to the
  [make_url()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.make_url) function, allowing `ArgumentError` to be thrown
  immediately, rather than causing failures later on.  Special logic ensures
  that mock forms of [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) are allowed through.  Pull request
  courtesy Grigoriev Semyon.
  References: [#10079](https://www.sqlalchemy.org/trac/ticket/10079)

### postgresql

- Fixed regression caused by improvements to PostgreSQL URL parsing in
  [#10004](https://www.sqlalchemy.org/trac/ticket/10004) where “host” query string arguments that had colons in
  them, to support various third party proxy servers and/or dialects, would
  not parse correctly as these were evaluated as `host:port` combinations.
  Parsing has been updated to consider a colon as indicating a `host:port`
  value only if the hostname contains only alphanumeric characters with dots
  or dashes only (e.g. no slashes), followed by exactly one colon followed by
  an all-integer token of zero or more integers.  In all other cases, the
  full string is taken as a host.
  References: [#10069](https://www.sqlalchemy.org/trac/ticket/10069)
- Fixed issue where comparisons to the [CITEXT](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.CITEXT) datatype
  would cast the right side to `VARCHAR`, leading to the right side not
  being interpreted as a `CITEXT` datatype, for the asyncpg, psycopg3 and
  pg80000 dialects.   This led to the [CITEXT](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.CITEXT) type being
  essentially unusable for practical use; this is now fixed and the test
  suite has been corrected to properly assert that expressions are rendered
  correctly.
  References: [#10096](https://www.sqlalchemy.org/trac/ticket/10096)

## 2.0.18

Released: July 5, 2023

### engine

- Adjusted the [create_engine.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.schema_translate_map) feature
  such that **all** schema names in the statement are now tokenized,
  regardless of whether or not a specific name is in the immediate schema
  translate map given, and to fallback to substituting the original name when
  the key is not in the actual schema translate map at execution time.  These
  two changes allow for repeated use of a compiled object with schema
  schema_translate_maps that include or dont include various keys on each
  run, allowing cached SQL constructs to continue to function at runtime when
  schema translate maps with different sets of keys are used each time. In
  addition, added detection of schema_translate_map dictionaries which gain
  or lose a `None` key across calls for the same statement, which affects
  compilation of the statement and is not compatible with caching; an
  exception is raised for these scenarios.
  References: [#10025](https://www.sqlalchemy.org/trac/ticket/10025)

### sql

- Fixed issue where the [ColumnOperators.regexp_match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_match)
  when using “flags” would not produce a “stable” cache key, that
  is, the cache key would keep changing each time causing cache pollution.
  The same issue existed for [ColumnOperators.regexp_replace()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_replace)
  with both the flags and the actual replacement expression.
  The flags are now represented as fixed modifier strings rendered as
  safestrings rather than bound parameters, and the replacement
  expression is established within the primary portion of the “binary”
  element so that it generates an appropriate cache key.
  Note that as part of this change, the
  [ColumnOperators.regexp_match.flags](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_match.params.flags) and
  [ColumnOperators.regexp_replace.flags](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_replace.params.flags) have been modified to
  render as literal strings only, whereas previously they were rendered as
  full SQL expressions, typically bound parameters.   These parameters should
  always be passed as plain Python strings and not as SQL expression
  constructs; it’s not expected that SQL expression constructs were used in
  practice for this parameter, so this is a backwards-incompatible change.
  The change also modifies the internal structure of the expression
  generated, for [ColumnOperators.regexp_replace()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_replace) with or without
  flags, and for [ColumnOperators.regexp_match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_match) with flags. Third
  party dialects which may have implemented regexp implementations of their
  own (no such dialects could be located in a search, so impact is expected
  to be low) would need to adjust the traversal of the structure to
  accommodate.
  This change is also **backported** to: 1.4.49
  References: [#10042](https://www.sqlalchemy.org/trac/ticket/10042)
- Fixed issue in mostly-internal [CacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey) construct where the
  `__ne__()` operator were not properly implemented, leading to nonsensical
  results when comparing [CacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey) instances to each other.
  This change is also **backported** to: 1.4.49

### extensions

- Added new option to [association_proxy()](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy) [association_proxy.create_on_none_assignment](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy.params.create_on_none_assignment); when an
  association proxy which refers to a scalar relationship is assigned the
  value `None`, and the referenced object is not present, a new object is
  created via the creator.  This was apparently an undefined behavior in the
  1.2 series that was silently removed.
  References: [#10013](https://www.sqlalchemy.org/trac/ticket/10013)

### typing

- Improved typing when using standalone operator functions from
  `sqlalchemy.sql.operators` such as `sqlalchemy.sql.operators.eq`.
  References: [#10054](https://www.sqlalchemy.org/trac/ticket/10054)
- Fixed some of the typing within the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct to
  correctly accept a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object that’s been aliased with
  [Table.alias()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.alias), as well as general support for [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
  objects to be passed as the “selectable” argument, since this is all
  supported.
  References: [#10061](https://www.sqlalchemy.org/trac/ticket/10061)

### postgresql

- Added multi-host support for the asyncpg dialect.  General improvements and
  error checking added to the PostgreSQL URL routines for the “multihost” use
  case added as well.  Pull request courtesy Ilia Dmitriev.
  See also
  [Multihost Connections](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#asyncpg-multihost)
  References: [#10004](https://www.sqlalchemy.org/trac/ticket/10004)
- Added new parameter `native_inet_types=False` to all PostgreSQL
  dialects, which indicates converters used by the DBAPI to
  convert rows from PostgreSQL [INET](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.INET) and [CIDR](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.CIDR) columns
  into Python `ipaddress` datatypes should be disabled, returning strings
  instead.  This allows code written to work with strings for these datatypes
  to be migrated to asyncpg, psycopg, or pg8000 without code changes
  other than adding this parameter to the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
  or [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) function call.
  See also
  [Network Data Types](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-network-datatypes)
  References: [#9945](https://www.sqlalchemy.org/trac/ticket/9945)

### mariadb

- Allowed reflecting [UUID](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UUID) columns from MariaDB. This allows
  Alembic to properly detect the type of such columns in existing MariaDB
  databases.
  References: [#10028](https://www.sqlalchemy.org/trac/ticket/10028)

### mssql

- Added support for creation and reflection of COLUMNSTORE
  indexes in MSSQL dialect. Can be specified on indexes
  specifying `mssql_columnstore=True`.
  References: [#7340](https://www.sqlalchemy.org/trac/ticket/7340)
- Fixed issue where performing [Cast](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Cast) to a string type with an
  explicit collation would render the COLLATE clause inside the CAST
  function, which resulted in a syntax error.
  References: [#9932](https://www.sqlalchemy.org/trac/ticket/9932)

## 2.0.17

Released: June 23, 2023

### orm

- Fixed regression in the 2.0 series where a query that used
  [undefer_group()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer_group) with [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) or
  [subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload) would raise an `AttributeError`. Pull request
  courtesy of Matthew Martin.
  References: [#9870](https://www.sqlalchemy.org/trac/ticket/9870)
- Fixed issue in ORM Annotated Declarative which prevented a
  [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) from being used on a mixin which did not return
  a [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) datatype, and instead returned a supplemental ORM
  datatype such as [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy).  The Declarative runtime would
  erroneously try to interpret this annotation as needing to be
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) and raise an error.
  References: [#9957](https://www.sqlalchemy.org/trac/ticket/9957)
- Fixed typing issue where using the [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) return type
  from a [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) function was disallowed.
  References: [#9957](https://www.sqlalchemy.org/trac/ticket/9957)
- Fixed regression introduced in 2.0.16 by [#9879](https://www.sqlalchemy.org/trac/ticket/9879) where passing a
  callable to the [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default) parameter of
  [mapped_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) while also setting `init=False` would
  interpret this value as a Dataclass default value which would be assigned
  directly to new instances of the object directly, bypassing the default
  generator taking place as the [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default)
  value generator on the underlying [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).  This condition
  is now detected so that the previous behavior is maintained, however a
  deprecation warning for this ambiguous use is emitted; to populate the
  default generator for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), the
  [mapped_column.insert_default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.insert_default) parameter should be used,
  which disambiguates from the [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default)
  parameter whose name is fixed as per pep-681.
  References: [#9936](https://www.sqlalchemy.org/trac/ticket/9936)
- Additional hardening and documentation for the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  “state change” system, which detects concurrent use of
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession) objects; an
  additional check is added within the process to acquire connections from
  the underlying engine, which is a critical section with regards to internal
  connection management.
  References: [#9973](https://www.sqlalchemy.org/trac/ticket/9973)
- Fixed issue in ORM loader strategy logic which further allows for long
  chains of [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) loader options across complex
  inheriting polymorphic / aliased / of_type() relationship chains to take
  proper effect in queries.
  References: [#10006](https://www.sqlalchemy.org/trac/ticket/10006)
- Fixed issue in support for the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatype in the
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) first added as part of
  [#8859](https://www.sqlalchemy.org/trac/ticket/8859) where using a custom [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) with fixed configuration
  in the map would fail to transfer the [Enum.name](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.name) parameter,
  which among other issues would prevent PostgreSQL enums from working if the
  enum values were passed as individual values.  Logic has been updated so
  that “name” is transferred over, but also that the default [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum)
  which is against the plain Python enum.Enum class or other “empty” enum
  won’t set a hardcoded name of `"enum"` either.
  References: [#9963](https://www.sqlalchemy.org/trac/ticket/9963)

### orm declarative

- A warning is emitted when an ORM [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) and other
  [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty) objects are assigned to two different class
  attributes at once; only one of the attributes will be mapped.  A warning
  for this condition was already in place for [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) and
  [mapped_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) objects.
  References: [#3532](https://www.sqlalchemy.org/trac/ticket/3532)

### extensions

- Fixed issue in mypy plugin for use with mypy 1.4.
  This change is also **backported** to: 1.4.49

### typing

- Fixed typing issue which prevented [WriteOnlyMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyMapped) and
  [DynamicMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.DynamicMapped) attributes from being used fully within ORM
  queries.
  References: [#9985](https://www.sqlalchemy.org/trac/ticket/9985)

### postgresql

- The pg8000 dialect now supports RANGE and MULTIRANGE datatypes, using the
  existing RANGE API described at [Range and Multirange Types](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-ranges).  Range and
  multirange types are supported in the pg8000 driver from version 1.29.8.
  Pull request courtesy Tony Locke.
  References: [#9965](https://www.sqlalchemy.org/trac/ticket/9965)

## 2.0.16

Released: June 10, 2023

### platform

- Compatibility improvements allowing the complete test suite to pass
  on Python 3.12.0b1.

### orm

- Improved [DeferredReflection.prepare()](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection.prepare) to accept arbitrary `**kw`
  arguments that are passed to [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect), allowing use
  cases such as reflection of views as well as dialect-specific arguments to
  be passed. Additionally, modernized the
  [DeferredReflection.prepare.bind](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection.prepare.params.bind) argument so that either an
  [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) are accepted as the “bind”
  argument.
  References: [#9828](https://www.sqlalchemy.org/trac/ticket/9828)
- Fixed issue where [DeclarativeBaseNoMeta](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta) declarative base class
  would not function with non-mapped mixins or abstract classes, raising an
  `AttributeError` instead.
  References: [#9862](https://www.sqlalchemy.org/trac/ticket/9862)
- Fixed regression in the 2.0 series where the default value of
  [validates.include_backrefs](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.validates.params.include_backrefs) got changed to `False` for
  the [validates()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.validates) function. This default is now restored to
  `True`.
  References: [#9820](https://www.sqlalchemy.org/trac/ticket/9820)
- Fixed bug in new feature which allows a WHERE clause to be used in
  conjunction with [ORM Bulk UPDATE by Primary Key](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-update), added in version 2.0.11
  as part of [#9583](https://www.sqlalchemy.org/trac/ticket/9583), where sending dictionaries that did not include
  the primary key values for each row would run through the bulk process and
  include “pk=NULL” for the rows, silently failing.   An exception is now
  raised if primary key values for bulk UPDATE are not supplied.
  References: [#9917](https://www.sqlalchemy.org/trac/ticket/9917)
- Fixed an issue where generating dataclasses fields that specified a
  `default` value and set `init=False` would not work.
  The dataclasses behavior in this case is to set the default
  value on the class, that’s not compatible with the descriptors used
  by SQLAlchemy. To support this case the default is transformed to
  a `default_factory` when generating the dataclass.
  References: [#9879](https://www.sqlalchemy.org/trac/ticket/9879)
- A deprecation warning is emitted whenever a property is added to a
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) where an ORM mapped property were already configured,
  or an attribute is already present on the class. Previously, there was a
  non-deprecation warning for this case that did not emit consistently. The
  logic for this warning has been improved so that it detects end-user
  replacement of attribute while not having false positives for internal
  Declarative and other cases where replacement of descriptors with new ones
  is expected.
  References: [#9841](https://www.sqlalchemy.org/trac/ticket/9841)
- Improved the argument checking on the
  [map_imperatively.local_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively.params.local_table) parameter of the
  [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively) method, ensuring only a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or other [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) is passed, and not an
  existing mapped class, which would lead to undefined behavior as the object
  were further interpreted for a new mapping.
  References: [#9869](https://www.sqlalchemy.org/trac/ticket/9869)
- The [InstanceState.unloaded_expirable](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.unloaded_expirable) attribute is a synonym
  for [InstanceState.unloaded](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.unloaded), and is now deprecated; this
  attribute was always implementation-specific and should not have been
  public.
  References: [#9913](https://www.sqlalchemy.org/trac/ticket/9913)

### asyncio

- Added new [create_async_engine.async_creator](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine.params.async_creator) parameter
  to [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine), which accomplishes the same purpose as the
  [create_engine.creator](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.creator) parameter of [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).
  This is a no-argument callable that provides a new asyncio connection,
  using the asyncio database driver directly. The
  [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) function will wrap the driver-level connection
  in the appropriate structures. Pull request courtesy of Jack Wotherspoon.
  References: [#8215](https://www.sqlalchemy.org/trac/ticket/8215)

### postgresql

- Cast `NAME` columns to `TEXT` when using `ARRAY_AGG` in PostgreSQL
  reflection. This seems to improve compatibility with some PostgreSQL
  derivatives that may not support aggregations on the `NAME` type.
  References: [#9838](https://www.sqlalchemy.org/trac/ticket/9838)
- Unified the custom PostgreSQL operator definitions, since they are
  shared among multiple different data types.
  References: [#9041](https://www.sqlalchemy.org/trac/ticket/9041)
- Added support for PostgreSQL 10 `NULLS NOT DISTINCT` feature of
  unique indexes and unique constraint using the dialect option
  `postgresql_nulls_not_distinct`.
  Updated the reflection logic to also correctly take this option
  into account.
  Pull request courtesy of Pavel Siarchenia.
  References: [#8240](https://www.sqlalchemy.org/trac/ticket/8240)
- Use proper precedence on PostgreSQL specific operators, such as `@>`.
  Previously the precedence was wrong, leading to wrong parenthesis when
  rendering against and `ANY` or `ALL` construct.
  References: [#9836](https://www.sqlalchemy.org/trac/ticket/9836)
- Fixed issue where the [ColumnOperators.like.escape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like.params.escape) and similar
  parameters did not allow an empty string as an argument that would be
  passed through as the “escape” character; this is a supported syntax by
  PostgreSQL.  Pull request courtesy Martin Caslavsky.
  References: [#9907](https://www.sqlalchemy.org/trac/ticket/9907)

## 2.0.15

Released: May 19, 2023

### orm

- As more projects are using new-style “2.0” ORM querying, it’s becoming
  apparent that the conditional nature of “autoflush”, being based on whether
  or not the given statement refers to ORM entities, is becoming more of a
  key behavior. Up until now, the “ORM” flag for a statement has been loosely
  based around whether or not the statement returns rows that correspond to
  ORM entities or columns; the original purpose of the “ORM” flag was to
  enable ORM-entity fetching rules which apply post-processing to Core result
  sets as well as ORM loader strategies to the statement.  For statements
  that don’t build on rows that contain ORM entities, the “ORM” flag was
  considered to be mostly unnecessary.
  It still may be the case that “autoflush” would be better taking effect for
  *all* usage of [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) and related methods, even for
  purely Core SQL constructs. However, this still could impact legacy cases
  where this is not expected and may be more of a 2.1 thing. For now however,
  the rules for the “ORM-flag” have been opened up so that a statement that
  includes ORM entities or attributes anywhere within, including in the WHERE
  / ORDER BY / GROUP BY clause alone, within scalar subqueries, etc. will
  enable this flag.  This will cause “autoflush” to occur for such statements
  and also be visible via the [ORMExecuteState.is_orm_statement](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.is_orm_statement)
  event-level attribute.
  References: [#9805](https://www.sqlalchemy.org/trac/ticket/9805)

### postgresql

- Repaired the base [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) datatype for the PostgreSQL dialect to
  make full use of the PG-specific `UUID` dialect-specific datatype when
  “native_uuid” is selected, so that PG driver behaviors are included. This
  issue became apparent due to the insertmanyvalues improvement made as part
  of [#9618](https://www.sqlalchemy.org/trac/ticket/9618), where in a similar manner as that of [#9739](https://www.sqlalchemy.org/trac/ticket/9739), the
  asyncpg driver is very sensitive to datatype casts being present or not,
  and the PostgreSQL driver-specific native `UUID` datatype must be invoked
  when this generic type is used so that these casts take place.
  References: [#9808](https://www.sqlalchemy.org/trac/ticket/9808)

## 2.0.14

Released: May 18, 2023

### orm

- Modified the `JoinedLoader` implementation to use a simpler approach in
  one particular area where it previously used a cached structure that would
  be shared among threads. The rationale is to avoid a potential race
  condition which is suspected of being the cause of a particular crash
  that’s been reported multiple times. The cached structure in question is
  still ultimately “cached” via the compiled SQL cache, so a performance
  degradation is not anticipated.
  References: [#9777](https://www.sqlalchemy.org/trac/ticket/9777)
- Fixed regression where use of [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) or [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete)
  within a [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) construct, then used in a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select),
  would raise a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) as a result of ORM related rules for
  performing ORM-level update/delete statements.
  References: [#9767](https://www.sqlalchemy.org/trac/ticket/9767)
- Fixed issue in new ORM Annotated Declarative where using a
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) (or other column-level constraint) inside of
  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) which is then copied out to models via pep-593
  `Annotated` would apply duplicates of each constraint to the
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) as produced in the target [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table),
  leading to incorrect CREATE TABLE DDL as well as migration directives under
  Alembic.
  References: [#9766](https://www.sqlalchemy.org/trac/ticket/9766)
- Fixed issue where using additional relationship criteria with the
  [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload) loader option, where the additional criteria itself
  contained correlated subqueries that referred to the joined entities and
  therefore also required “adaption” to aliased entities, would be excluded
  from this adaption, producing the wrong ON clause for the joinedload.
  References: [#9779](https://www.sqlalchemy.org/trac/ticket/9779)

### sql

- Generalized the MSSQL [try_cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.try_cast) function into the
  `sqlalchemy.` import namespace so that it may be implemented by third
  party dialects as well. Within SQLAlchemy, the [try_cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.try_cast)
  function remains a SQL Server-only construct that will raise
  [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) if used with backends that don’t support it.
  [try_cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.try_cast) implements a CAST where un-castable conversions are
  returned as NULL, instead of raising an error. Theoretically, the construct
  could be implemented by third party dialects for Google BigQuery, DuckDB,
  and Snowflake, and possibly others.
  Pull request courtesy Nick Crews.
  References: [#9752](https://www.sqlalchemy.org/trac/ticket/9752)
- Fixed issue in [values()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.values) construct where an internal compilation
  error would occur if the construct were used inside of a scalar subquery.
  References: [#9772](https://www.sqlalchemy.org/trac/ticket/9772)

### postgresql

- Fixed apparently very old issue where the
  [ENUM.create_type](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM.params.create_type) parameter, when set to its
  non-default of `False`, would not be propagated when the
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) which it’s a part of were copied, as is common when
  using ORM Declarative mixins.
  References: [#9773](https://www.sqlalchemy.org/trac/ticket/9773)

### tests

- Fixed test that relied on the `sys.getsizeof()` function to not run on
  pypy, where this function appears to have different behavior than it does
  on cpython.
  References: [#9789](https://www.sqlalchemy.org/trac/ticket/9789)

## 2.0.13

Released: May 10, 2023

### orm

- Fixed issue where ORM Annotated Declarative would not resolve forward
  references correctly in all cases; in particular, when using
  `from __future__ import annotations` in combination with Pydantic
  dataclasses.
  References: [#9717](https://www.sqlalchemy.org/trac/ticket/9717)
- Fixed issue in new [Using RETURNING with upsert statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-upsert-returning) feature where the
  `populate_existing` execution option was not being propagated to the
  loading option, preventing existing attributes from being refreshed
  in-place.
  References: [#9746](https://www.sqlalchemy.org/trac/ticket/9746)
- Fixed loader strategy pathing issues where eager loaders such as
  [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload) / [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) would fail to traverse
  fully for many-levels deep following a load that had a
  [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) or similar construct as an interim member.
  References: [#9715](https://www.sqlalchemy.org/trac/ticket/9715)
- Fixed issue in [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct where the correct
  warning for “column X named directly multiple times” would not be emitted
  when ORM mapped attributes referred to the same [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), if
  the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct were involved, raising an internal
  assertion instead.
  References: [#9630](https://www.sqlalchemy.org/trac/ticket/9630)

### sql

- Implemented the “cartesian product warning” for UPDATE and DELETE
  statements, those which include multiple tables that are not correlated
  together in some way.
  References: [#9721](https://www.sqlalchemy.org/trac/ticket/9721)
- Fixed the base class for dialect-specific float/double types; Oracle
  [BINARY_DOUBLE](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.BINARY_DOUBLE) now subclasses [Double](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Double),
  and internal types for [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) for asyncpg and pg8000 now
  correctly subclass [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float).
- Fixed issue where [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) construct that included multiple
  tables and no VALUES clause would raise with an internal error. Current
  behavior for [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) with no values is to generate a SQL
  UPDATE statement with an empty “set” clause, so this has been made
  consistent for this specific sub-case.

### schema

- Improved how table columns are added, avoiding unnecessary allocations,
  significantly speeding up the creation of many table, like when reflecting
  entire schemas.
  References: [#9597](https://www.sqlalchemy.org/trac/ticket/9597)

### typing

- Fixed typing for the [Session.get.with_for_update](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get.params.with_for_update) parameter
  of [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) and [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) (as well as
  corresponding methods on [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession)) to accept boolean
  `True` and all other argument forms accepted by the parameter at runtime.
  References: [#9762](https://www.sqlalchemy.org/trac/ticket/9762)
- Added type [ColumnExpressionArgument](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnExpressionArgument) as a public-facing type
  that indicates column-oriented arguments which are passed to SQLAlchemy
  constructs, such as [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where), [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) and
  others. This may be used to add typing to end-user functions which call
  these methods.
  References: [#9656](https://www.sqlalchemy.org/trac/ticket/9656)

### asyncio

- Added a new helper mixin [AsyncAttrs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs) that seeks to improve
  the use of lazy-loader and other expired or deferred ORM attributes with
  asyncio, providing a simple attribute accessor that provides an `await`
  interface to any ORM attribute, whether or not it needs to emit SQL.
  See also
  [AsyncAttrs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs)
  References: [#9731](https://www.sqlalchemy.org/trac/ticket/9731)
- Fixed issue in semi-private `await_only()` and `await_fallback()`
  concurrency functions where the given awaitable would remain un-awaited if
  the function threw a `GreenletError`, which could cause “was not awaited”
  warnings later on if the program continued. In this case, the given
  awaitable is now cancelled before the exception is thrown.

### postgresql

- Fixed another regression due to the “insertmanyvalues” change in 2.0.10 as
  part of [#9618](https://www.sqlalchemy.org/trac/ticket/9618), in a similar way as regression [#9701](https://www.sqlalchemy.org/trac/ticket/9701), where
  [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) datatypes also need additional casts on when using the
  asyncpg driver specifically in order to work with the new bulk INSERT
  format.
  References: [#9739](https://www.sqlalchemy.org/trac/ticket/9739)

### oracle

- Added reflection support in the Oracle dialect to expression based indexes
  and the ordering direction of index expressions.
  References: [#9597](https://www.sqlalchemy.org/trac/ticket/9597)

### misc

- Fixed issue in [Mutable](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.Mutable) where event registration for ORM
  mapped attributes would be called repeatedly for mapped inheritance
  subclasses, leading to duplicate events being invoked in inheritance
  hierarchies.
  References: [#9676](https://www.sqlalchemy.org/trac/ticket/9676)

## 2.0.12

Released: April 30, 2023

### orm

- Fixed critical caching issue where the combination of
  [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) and [hybrid_property()](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property) expression
  compositions would cause a cache key mismatch, leading to cache keys that
  held onto the actual [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) object while also not matching
  that of equivalent constructs, filling up the cache.
  This change is also **backported** to: 1.4.48
  References: [#9728](https://www.sqlalchemy.org/trac/ticket/9728)

### mysql

- Fixed issues regarding reflection of comments for [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects, where the comments contained control
  characters such as newlines. Additional testing support for these
  characters as well as extended Unicode characters in table and column
  comments (the latter of which aren’t supported by MySQL/MariaDB) added to
  testing overall.
  References: [#9722](https://www.sqlalchemy.org/trac/ticket/9722)

## 2.0.11

Released: April 26, 2023

### orm

- The [ORM bulk INSERT and UPDATE](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete)
  features now add these capabilities:
  - The requirement that extra parameters aren’t passed when using ORM
    INSERT using the “orm” dml_strategy setting is lifted.
  - The requirement that additional WHERE criteria is not passed when using
    ORM UPDATE using the “bulk” dml_strategy setting is lifted.  Note that
    in this case, the check for expected row count is turned off.
  References: [#9583](https://www.sqlalchemy.org/trac/ticket/9583), [#9595](https://www.sqlalchemy.org/trac/ticket/9595)
- Fixed 2.0 regression where use of [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) inside of
  [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) would fail to be interpreted correctly when
  executing the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) statement using the ORM
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), due to the new
  [ORM-enabled insert feature](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) not
  implementing this use case.
  References: [#9583](https://www.sqlalchemy.org/trac/ticket/9583), [#9595](https://www.sqlalchemy.org/trac/ticket/9595)

### engine

- A series of performance enhancements to [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row):
  - `__getattr__` performance of the row’s “named tuple” interface has
    been improved; within this change, the [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
    implementation has been streamlined, removing constructs and logic
    that were specific to the 1.4 and prior series of SQLAlchemy.
    As part of this change, the serialization format of [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
    has been modified slightly, however rows which were pickled with previous
    SQLAlchemy 2.0 releases will be recognized within the new format.
    Pull request courtesy J. Nick Koston.
  - Improved row processing performance for “binary” datatypes by making the
    “bytes” handler conditional on a per driver basis.  As a result, the
    “bytes” result handler has been removed for nearly all drivers other than
    psycopg2, all of which in modern forms support returning Python “bytes”
    directly.  Pull request courtesy J. Nick Koston.
  - Additional refactorings inside of [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) to improve
    performance by Federico Caselli.
  References: [#9678](https://www.sqlalchemy.org/trac/ticket/9678), [#9680](https://www.sqlalchemy.org/trac/ticket/9680)
- Fixed regression which prevented the [URL.normalized_query](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.normalized_query)
  attribute of [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) from functioning.
  References: [#9682](https://www.sqlalchemy.org/trac/ticket/9682)

### sql

- Added support for slice access with [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection), e.g.
  `table.c[0:5]`, `subquery.c[:-1]` etc. Slice access returns a sub
  [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) in the same way as passing a tuple of keys. This
  is a natural continuation of the key-tuple access added for [#8285](https://www.sqlalchemy.org/trac/ticket/8285),
  where it appears to be an oversight that the slice access use case was
  omitted.
  References: [#8285](https://www.sqlalchemy.org/trac/ticket/8285)

### typing

- Improved typing of [RowMapping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.RowMapping) to indicate that it
  support also [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) as index objects, not only
  string names. Pull request courtesy Andy Freeland.
  References: [#9644](https://www.sqlalchemy.org/trac/ticket/9644)

### postgresql

- Fixed critical regression caused by [#9618](https://www.sqlalchemy.org/trac/ticket/9618), which modified the
  architecture of the [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature for 2.0.10, which
  caused floating point values to lose all decimal places when being inserted
  using the insertmanyvalues feature with either the psycopg2 or psycopg
  drivers.
  References: [#9701](https://www.sqlalchemy.org/trac/ticket/9701)

### mssql

- Implemented the [Double](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Double) type for SQL Server, where it
  will render `DOUBLE PRECISION` at DDL time.  This is implemented using
  a new MSSQL datatype [DOUBLE_PRECISION](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.DOUBLE_PRECISION) which also may
  be used directly.

### oracle

- Fixed issue in Oracle dialects where `Decimal` returning types such as
  [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric) would return floating point values, rather than
  `Decimal` objects, when these columns were used in the
  [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) clause to return INSERTed values.

## 2.0.10

Released: April 21, 2023

### orm

- Fixed bug where various ORM-specific getters such as
  [ORMExecuteState.is_column_load](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.is_column_load),
  [ORMExecuteState.is_relationship_load](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.is_relationship_load),
  [ORMExecuteState.loader_strategy_path](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState.loader_strategy_path) etc. would throw an
  `AttributeError` if the SQL statement itself were a “compound select”
  such as a UNION.
  This change is also **backported** to: 1.4.48
  References: [#9634](https://www.sqlalchemy.org/trac/ticket/9634)
- Fixed issue where the [declared_attr.directive()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr.directive) modifier was not
  correctly honored for subclasses when applied to the `__mapper_args__`
  special method name, as opposed to direct use of
  [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr). The two constructs should have identical
  runtime behaviors.
  References: [#9625](https://www.sqlalchemy.org/trac/ticket/9625)
- Made an improvement to the [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) loader option
  to allow it to be indicated in the [Executable.options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.options) method of a
  top-level statement that is not itself an ORM statement. Examples include
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) that’s embedded in compound statements such as
  [union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union), within an [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select) construct, as
  well as within CTE expressions that are not ORM related at the top level.
  References: [#9635](https://www.sqlalchemy.org/trac/ticket/9635)
- Fixed bug in ORM bulk insert feature where additional unnecessary columns
  would be rendered in the INSERT statement if RETURNING of individual columns
  were requested.
  References: [#9685](https://www.sqlalchemy.org/trac/ticket/9685)
- Fixed bug in ORM Declarative Dataclasses where the
  [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression) and [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property)
  constructs, which are documented as read-only constructs in the context of
  a Declarative mapping, could not be used with a
  [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) class without adding `init=False`, which
  in the case of [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression) was not possible as no
  `init` parameter was included. These constructs have been modified from a
  dataclass perspective to be assumed to be “read only”, setting
  `init=False` by default and no longer including them in the pep-681
  constructor. The dataclass parameters for [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) `init`, `default`, `default_factory`, `kw_only` are now deprecated;
  these fields don’t apply to [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) as used in a
  Declarative dataclasses configuration where the construct would be
  read-only. Also added read-specific parameter
  [query_expression.compare](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression.params.compare) to
  [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression); [query_expression.repr](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression.params.repr)
  was already present.
  References: [#9628](https://www.sqlalchemy.org/trac/ticket/9628)
- Added missing [mapped_column.active_history](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.active_history) parameter
  to [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct.

### engine

- Added [create_pool_from_url()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_pool_from_url) and
  [create_async_pool_from_url()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_pool_from_url) to create
  a [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) instance from an input url passed as string
  or `URL`.
  References: [#9613](https://www.sqlalchemy.org/trac/ticket/9613)
- Repaired a major shortcoming which was identified in the
  [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) performance optimization feature first
  introduced in the 2.0 series. This was a continuation of the change in
  2.0.9 which disabled the SQL Server version of the feature due to a
  reliance in the ORM on apparent row ordering that is not guaranteed to take
  place. The fix applies new logic to all “insertmanyvalues” operations,
  which takes effect when a new parameter
  [Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order) on the
  [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) or [UpdateBase.return_defaults()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.return_defaults)
  methods, that through a combination of alternate SQL forms, direct
  correspondence of client side parameters, and in some cases downgrading to
  running row-at-a-time, will apply sorting to each batch of returned rows
  using correspondence to primary key or other unique values in each row
  which can be correlated to the input data.
  Performance impact is expected to be minimal as nearly all common primary
  key scenarios are suitable for parameter-ordered batching to be
  achieved for all backends other than SQLite, while “row-at-a-time”
  mode operates with a bare minimum of Python overhead compared to the very
  heavyweight approaches used in the 1.x series. For SQLite, there is no
  difference in performance when “row-at-a-time” mode is used.
  It’s anticipated that with an efficient “row-at-a-time” INSERT with
  RETURNING batching capability, the “insertmanyvalues” feature can be later
  be more easily generalized to third party backends that include RETURNING
  support but not necessarily easy ways to guarantee a correspondence
  with parameter order.
  See also
  [Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order)
  References: [#9603](https://www.sqlalchemy.org/trac/ticket/9603), [#9618](https://www.sqlalchemy.org/trac/ticket/9618)

### typing

- Added typing information for recently added operators
  [ColumnOperators.icontains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.icontains), [ColumnOperators.istartswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.istartswith),
  [ColumnOperators.iendswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.iendswith), and bitwise operators
  [ColumnOperators.bitwise_and()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_and), [ColumnOperators.bitwise_or()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_or),
  [ColumnOperators.bitwise_xor()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_xor), [ColumnOperators.bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_not),
  [ColumnOperators.bitwise_lshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_lshift) [ColumnOperators.bitwise_rshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_rshift). Pull request courtesy Martijn
  Pieters.
  References: [#9650](https://www.sqlalchemy.org/trac/ticket/9650)
- Updates to the codebase to pass typing with Mypy 1.2.0.
- Fixed typing issue where [PropComparator.and_()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.and_) expressions would
  not be correctly typed inside of loader options such as
  [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload).
  References: [#9669](https://www.sqlalchemy.org/trac/ticket/9669)

### postgresql

- Added `prepared_statement_name_func` connection argument option in the
  asyncpg dialect. This option allows passing a callable used to customize
  the name of the prepared statement that will be created by the driver
  when executing queries.  Pull request courtesy Pavel Sirotkin.
  See also
  [Prepared Statement Name with PGBouncer](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#asyncpg-prepared-statement-name)
  References: [#9608](https://www.sqlalchemy.org/trac/ticket/9608)
- Add missing [Range.intersection()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range.intersection) method.
  Pull request courtesy Yurii Karabas.
  References: [#9509](https://www.sqlalchemy.org/trac/ticket/9509)
- Restored the [ENUM.name](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM.params.name) parameter as optional in the
  signature for [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM), as this is chosen automatically
  from a given pep-435 `Enum` type.
  References: [#9611](https://www.sqlalchemy.org/trac/ticket/9611)
- Fixed issue where the comparison for [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) against a
  plain string would cast that right-hand side type as VARCHAR, which due to
  more explicit casting added to dialects such as asyncpg would produce a
  PostgreSQL type mismatch error.
  References: [#9621](https://www.sqlalchemy.org/trac/ticket/9621)
- Fixed issue that prevented reflection of expression based indexes
  with long expressions in PostgreSQL. The expression where erroneously
  truncated to the identifier length (that’s 63 bytes by default).
  References: [#9615](https://www.sqlalchemy.org/trac/ticket/9615)

### mssql

- Restored the [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature for Microsoft SQL Server.
  This feature was disabled in version 2.0.9 due to an apparent reliance
  on the ordering of RETURNING that is not guaranteed.   The architecture of
  the “insertmanyvalues” feature has been reworked to accommodate for
  specific organizations of INSERT statements and result row handling that
  can guarantee the correspondence of returned rows to input records.
  See also
  [Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order)
  References: [#9603](https://www.sqlalchemy.org/trac/ticket/9603), [#9618](https://www.sqlalchemy.org/trac/ticket/9618)

### oracle

- Fixed issue where the [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) datatype could not be used in
  an INSERT..RETURNING clause with the Oracle dialect.

## 2.0.9

Released: April 5, 2023

### orm

- Fixed endless loop which could occur when using “relationship to aliased
  class” feature and also indicating a recursive eager loader such as
  `lazy="selectinload"` in the loader, in combination with another eager
  loader on the opposite side. The check for cycles has been fixed to include
  aliased class relationships.
  This change is also **backported** to: 1.4.48
  References: [#9590](https://www.sqlalchemy.org/trac/ticket/9590)

### mariadb

- Added `row_number` as reserved word in MariaDb.
  References: [#9588](https://www.sqlalchemy.org/trac/ticket/9588)

### mssql

- The SQLAlchemy “insertmanyvalues” feature which allows fast INSERT of
  many rows while also supporting RETURNING is temporarily disabled for
  SQL Server. As the unit of work currently relies upon this feature such
  that it matches existing ORM objects to returned primary key
  identities, this particular use pattern does not work with SQL Server
  in all cases as the order of rows returned by “OUTPUT inserted” may not
  always match the order in which the tuples were sent, leading to
  the ORM making the wrong decisions about these objects in subsequent
  operations.
  The feature will be re-enabled in an upcoming release and will again
  take effect for multi-row INSERT statements, however the unit-of-work’s
  use of the feature will be disabled, possibly for all dialects, unless
  ORM-mapped tables also include a “sentinel” column so that the
  returned rows can be referenced back to the original data passed in.
  References: [#9603](https://www.sqlalchemy.org/trac/ticket/9603)
- Changed the bulk INSERT strategy used for SQL Server “executemany” with
  pyodbc when `fast_executemany` is set to `True` by using
  `fast_executemany` / `cursor.executemany()` for bulk INSERT that does
  not include RETURNING, restoring the same behavior as was used in
  SQLAlchemy 1.4 when this parameter is set.
  New performance details from end users have shown that `fast_executemany`
  is still much faster for very large datasets as it uses ODBC commands that
  can receive all rows in a single round trip, allowing for much larger
  datasizes than the batches that can be sent by “insertmanyvalues”
  as was implemented for SQL Server.
  While this change was made such that “insertmanyvalues” continued to be
  used for INSERT that includes RETURNING, as well as if `fast_executemany`
  were not set, due to [#9603](https://www.sqlalchemy.org/trac/ticket/9603), the “insertmanyvalues” strategy has
  been disabled for SQL Server across the board in any case.
  References: [#9586](https://www.sqlalchemy.org/trac/ticket/9586)

## 2.0.8

Released: March 31, 2023

### orm

- Exceptions such as `TypeError` and `ValueError` raised by Python
  dataclasses when making use of the [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) mixin
  class or [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) decorator are now
  wrapped within an [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) wrapper along with
  informative context about the error message, referring to the Python
  dataclasses documentation as the authoritative source of background
  information on the cause of the exception.
  See also
  [Python dataclasses error encountered when creating dataclass for <classname>](https://docs.sqlalchemy.org/en/20/errors.html#error-dcte)
  References: [#9563](https://www.sqlalchemy.org/trac/ticket/9563)
- Fixed issue in ORM Annotated Declarative where using a recursive type (e.g.
  using a nested Dict type) would result in a recursion overflow in the ORM’s
  annotation resolution logic, even if this datatype were not necessary to
  map the column.
  References: [#9553](https://www.sqlalchemy.org/trac/ticket/9553)
- Fixed issue where the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct would raise an
  internal error if used on a Declarative mixin and included the
  [mapped_column.deferred](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.deferred) parameter.
  References: [#9550](https://www.sqlalchemy.org/trac/ticket/9550)
- Expanded the warning emitted when a plain [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) object is
  present in a Declarative mapping to include any arbitrary SQL expression
  that is not declared within an appropriate property type such as
  [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), [deferred()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.deferred), etc. These attributes
  are otherwise not mapped at all and remain unchanged within the class
  dictionary. As it seems likely that such an expression is usually not
  what’s intended, this case now warns for all such otherwise ignored
  expressions, rather than just the [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) case.
  References: [#9537](https://www.sqlalchemy.org/trac/ticket/9537)
- Fixed regression where accessing the expression value of a hybrid property
  on a class that was either unmapped or not-yet-mapped (such as calling upon
  it within a [declared_attr()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) method) would raise an internal
  error, as an internal fetch for the parent class’ mapper would fail and an
  instruction for this failure to be ignored were inadvertently removed in
  2.0.
  References: [#9519](https://www.sqlalchemy.org/trac/ticket/9519)
- Fields that are declared on Declarative Mixins and then combined with
  classes that make use of [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass), where those mixin
  fields are not themselves part of a dataclass, now emit a deprecation
  warning as these fields will be ignored in a future release, as Python
  dataclasses behavior is to ignore these fields. Type checkers will not see
  these fields under pep-681.
  See also
  [When transforming <cls> to a dataclass, attribute(s) originate from superclass <cls> which is not a dataclass.](https://docs.sqlalchemy.org/en/20/errors.html#error-dcmx) - background on rationale
  [Using mixins and abstract superclasses](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-dc-mixins)
  References: [#9350](https://www.sqlalchemy.org/trac/ticket/9350)
- Fixed issue where the [BindParameter.render_literal_execute()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter.render_literal_execute)
  method would fail when called on a parameter that also had ORM annotations
  associated with it. In practice, this would be observed as a failure of SQL
  compilation when using some combinations of a dialect that uses “FETCH
  FIRST” such as Oracle along with a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct that uses
  [Select.limit()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.limit), within some ORM contexts, including if the
  statement were embedded within a relationship primaryjoin expression.
  References: [#9526](https://www.sqlalchemy.org/trac/ticket/9526)
- Towards maintaining consistency with unit-of-work changes made for
  [#5984](https://www.sqlalchemy.org/trac/ticket/5984) and [#8862](https://www.sqlalchemy.org/trac/ticket/8862), both of which disable “lazy=’raise’”
  handling within [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) processes that aren’t triggered by
  attribute access, the [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) method will now also
  disable “lazy=’raise’” handling when it traverses relationship paths in
  order to process the “delete” and “delete-orphan” cascade rules.
  Previously, there was no easy way to generically call
  [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) on an object that had “lazy=’raise’” set up
  such that only the necessary relationships would be loaded. As
  “lazy=’raise’” is primarily intended to catch SQL loading that emits on
  attribute access, [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete) is now made to behave like
  other [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) methods including [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) as
  well as [Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush) along with autoflush.
  References: [#9549](https://www.sqlalchemy.org/trac/ticket/9549)
- Fixed issue where an annotation-only [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) directive could
  not be used in a Declarative mixin class, without that attribute attempting
  to take effect for single- or joined-inheritance subclasses of mapped
  classes that had already mapped that attribute on a superclass, producing
  conflicting column errors and/or warnings.
  References: [#9564](https://www.sqlalchemy.org/trac/ticket/9564)
- Properly type [Insert.from_select.names](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select.params.names) to accept
  a list of string or columns or mapped attributes.
  References: [#9514](https://www.sqlalchemy.org/trac/ticket/9514)

### examples

- Fixed issue in “versioned history” example where using a declarative base
  that is derived from [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) would fail to be mapped.
  Additionally, repaired the given test suite so that the documented
  instructions for running the example using Python unittest now work again.

### typing

- Fixed typing for [deferred()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.deferred) and [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression)
  to work correctly with 2.0 style mappings.
  References: [#9536](https://www.sqlalchemy.org/trac/ticket/9536)

### postgresql

- Fixed critical regression in PostgreSQL dialects such as asyncpg which rely
  upon explicit casts in SQL in order for datatypes to be passed to the
  driver correctly, where a [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) datatype would be cast along
  with the exact column length being compared, leading to implicit truncation
  when comparing a `VARCHAR` of a smaller length to a string of greater
  length regardless of operator in use (e.g. LIKE, MATCH, etc.). The
  PostgreSQL dialect now omits the length from `VARCHAR` when rendering
  these casts.
  References: [#9511](https://www.sqlalchemy.org/trac/ticket/9511)

### mysql

- Fixed issue where string datatypes such as [CHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.CHAR),
  [VARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARCHAR), [TEXT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TEXT), as well as binary
  [BLOB](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BLOB), could not be produced with an explicit length of
  zero, which has special meaning for MySQL. Pull request courtesy J. Nick
  Koston.
  References: [#9544](https://www.sqlalchemy.org/trac/ticket/9544)

### misc

- Implemented missing methods `copy` and `pop` in
  OrderedSet class.
  References: [#9487](https://www.sqlalchemy.org/trac/ticket/9487)

## 2.0.7

Released: March 18, 2023

### typing

- Fixed typing issue where [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) would not allow an
  arbitrary callable as the source of the composite class.
  References: [#9502](https://www.sqlalchemy.org/trac/ticket/9502)

### postgresql

- Added new PostgreSQL type [CITEXT](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.CITEXT). Pull request
  courtesy Julian David Rath.
  References: [#9416](https://www.sqlalchemy.org/trac/ticket/9416)
- Modifications to the base PostgreSQL dialect to allow for better integration with the
  sqlalchemy-redshift third party dialect for SQLAlchemy 2.0. Pull request courtesy
  matthewgdv.
  References: [#9442](https://www.sqlalchemy.org/trac/ticket/9442)

## 2.0.6

Released: March 13, 2023

### orm

- Fixed bug where the “active history” feature was not fully
  implemented for composite attributes, making it impossible to receive
  events that included the “old” value.   This seems to have been the case
  with older SQLAlchemy versions as well, where “active_history” would
  be propagated to the underlying column-based attributes, but an event
  handler listening to the composite attribute itself would not be given
  the “old” value being replaced, even if the composite() were set up
  with active_history=True.
  Additionally, fixed a regression that’s local to 2.0 which disallowed
  active_history on composite from being assigned to the impl with
  `attr.impl.active_history=True`.
  References: [#9460](https://www.sqlalchemy.org/trac/ticket/9460)
- Fixed regression involving pickling of Python rows between the cython and
  pure Python implementations of [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row), which occurred as part of
  refactoring code for version 2.0 with typing. A particular constant were
  turned into a string based `Enum` for the pure Python version of
  [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) whereas the cython version continued to use an integer
  constant, leading to deserialization failures.
  References: [#9418](https://www.sqlalchemy.org/trac/ticket/9418)

### sql

- Fixed regression where the fix for [#8098](https://www.sqlalchemy.org/trac/ticket/8098), which was released in
  the 1.4 series and provided a layer of concurrency-safe checks for the
  lambda SQL API, included additional fixes in the patch that failed to be
  applied to the main branch. These additional fixes have been applied.
  References: [#9461](https://www.sqlalchemy.org/trac/ticket/9461)
- Fixed regression where the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct would not be able
  to render if it were given no columns and then used in the context of an
  EXISTS, raising an internal exception instead. While an empty “SELECT” is
  not typically valid SQL, in the context of EXISTS databases such as
  PostgreSQL allow it, and in any case the condition now no longer raises
  an internal exception.
  References: [#9440](https://www.sqlalchemy.org/trac/ticket/9440)

### typing

- Fixed typing issue where [ColumnElement.cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast) did not allow a
  [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) argument independent of the type of the
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) itself, which is the purpose of
  [ColumnElement.cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast).
  References: [#9451](https://www.sqlalchemy.org/trac/ticket/9451)
- Fixed issues to allow typing tests to pass under Mypy 1.1.1.

### oracle

- Fixed reflection bug where Oracle “name normalize” would not work correctly
  for reflection of symbols that are in the “PUBLIC” schema, such as
  synonyms, meaning the PUBLIC name could not be indicated as lower case on
  the Python side for the [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) argument. Using
  uppercase “PUBLIC” would work, but would then lead to awkward SQL queries
  including a quoted `"PUBLIC"` name as well as indexing the table under
  uppercase “PUBLIC”, which was inconsistent.
  References: [#9459](https://www.sqlalchemy.org/trac/ticket/9459)

## 2.0.5.post1

Released: March 5, 2023

### orm

- Added constructor arguments to the built-in mapping collection types
  including [KeyFuncDict](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.KeyFuncDict), [attribute_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict),
  [column_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_keyed_dict) so that these dictionary types may be
  constructed in place given the data up front; this provides further
  compatibility with tools such as Python dataclasses `.asdict()` which
  relies upon invoking these classes directly as ordinary dictionary classes.
  References: [#9418](https://www.sqlalchemy.org/trac/ticket/9418)
- Fixed multiple regressions due to [#8372](https://www.sqlalchemy.org/trac/ticket/8372), involving
  [attribute_mapped_collection()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_mapped_collection) (now called
  [attribute_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict)).
  First, the collection was no longer usable with “key” attributes that were
  not themselves ordinary mapped attributes; attributes linked to descriptors
  and/or association proxy attributes have been fixed.
  Second, if an event or other operation needed access to the “key” in order
  to populate the dictionary from an mapped attribute that was not
  loaded, this also would raise an error inappropriately, rather than
  trying to load the attribute as was the behavior in 1.4.  This is also
  fixed.
  For both cases, the behavior of [#8372](https://www.sqlalchemy.org/trac/ticket/8372) has been expanded.
  [#8372](https://www.sqlalchemy.org/trac/ticket/8372) introduced an error that raises when the derived key that
  would be used as a mapped dictionary key is effectively unassigned. In this
  change, a warning only is emitted if the effective value of the “.key”
  attribute is `None`, where it cannot be unambiguously determined if this
  `None` was intentional or not. `None` will be not supported as mapped
  collection dictionary keys going forward (as it typically refers to NULL
  which means “unknown”). Setting
  [attribute_keyed_dict.ignore_unpopulated_attribute](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict.params.ignore_unpopulated_attribute) will now
  cause such `None` keys to be ignored as well.
  References: [#9424](https://www.sqlalchemy.org/trac/ticket/9424)
- Identified that the `sqlite` and `mssql+pyodbc` dialects are now
  compatible with the SQLAlchemy ORM’s “versioned rows” feature, since
  SQLAlchemy now computes rowcount for a RETURNING statement in this specific
  case by counting the rows returned, rather than relying upon
  `cursor.rowcount`.  In particular, the ORM versioned rows use case
  (documented at [Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html#mapper-version-counter)) should now be fully
  supported with the SQL Server pyodbc dialect.
- Added support for the [Mapper.polymorphic_load](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_load) parameter to
  be applied to each mapper in an inheritance hierarchy more than one level
  deep, allowing columns to load for all classes in the hierarchy that
  indicate `"selectin"` using a single statement, rather than ignoring
  elements on those intermediary classes that nonetheless indicate they also
  would participate in `"selectin"` loading and were not part of the
  base-most SELECT statement.
  References: [#9373](https://www.sqlalchemy.org/trac/ticket/9373)
- Continued the fix for [#8853](https://www.sqlalchemy.org/trac/ticket/8853), allowing the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
  name to be fully qualified regardless of whether or not
  `from __annotations__ import future` were present. This issue first fixed
  in 2.0.0b3 confirmed that this case worked via the test suite, however the
  test suite apparently was not testing the behavior for the name
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) not being locally present at all; string resolution
  has been updated to ensure the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) symbol is locatable as
  applies to how the ORM uses these functions.
  References: [#8853](https://www.sqlalchemy.org/trac/ticket/8853), [#9335](https://www.sqlalchemy.org/trac/ticket/9335)

### orm declarative

- Fixed issue where new [mapped_column.use_existing_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.use_existing_column)
  feature would not work if the two same-named columns were mapped under
  attribute names that were differently-named from an explicit name given to
  the column itself. The attribute names can now be differently named when
  using this parameter.
  References: [#9332](https://www.sqlalchemy.org/trac/ticket/9332)

### engine

- A small optimization to the Cython implementation of [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)
  using a cdef for a particular int value to avoid Python overhead. Pull
  request courtesy Matus Valo.
  References: [#9343](https://www.sqlalchemy.org/trac/ticket/9343)
- Fixed bug where [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects could not be reliably unpickled
  across processes due to an accidental reliance on an unstable hash value.
  References: [#9423](https://www.sqlalchemy.org/trac/ticket/9423)

### sql

- Restore the [nullslast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nullslast) and [nullsfirst()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nullsfirst) legacy functions
  into the `sqlalchemy` import namespace. Previously, the newer
  [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) and [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) functions were available, but
  the legacy ones were inadvertently removed.
  References: [#9390](https://www.sqlalchemy.org/trac/ticket/9390)

### schema

- Validate that when provided the [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema)
  argument of [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) is a string.

### typing

- Exported the type returned by
  [scoped_session.query_property()](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoped_session.query_property) using a new public type
  [QueryPropertyDescriptor](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.QueryPropertyDescriptor).
  References: [#9338](https://www.sqlalchemy.org/trac/ticket/9338)
- Fixed bug where the [Connection.scalars()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.scalars) method was not typed
  as allowing a multiple-parameters list, which is now supported using
  insertmanyvalues operations.
- Improved typing for the mapping passed to [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) and
  [Update.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.values) to be more open-ended about collection type, by
  indicating read-only `Mapping` instead of writeable `Dict` which would
  error out on too limited of a key type.
  References: [#9376](https://www.sqlalchemy.org/trac/ticket/9376)
- Added missing init overload to the [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric) type object so
  that pep-484 type checkers may properly resolve the complete type, deriving
  from the [Numeric.asdecimal](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric.params.asdecimal) parameter whether `Decimal`
  or `float` objects will be represented.
  References: [#9391](https://www.sqlalchemy.org/trac/ticket/9391)
- Fixed typing bug where [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) would not accept
  [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) or [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect) objects as a valid type.
  Additionally repaired the `columns` method to have a
  return type, which was missing.
  References: [#9398](https://www.sqlalchemy.org/trac/ticket/9398)
- Fixed typing issue where [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) would not
  record the class type correctly.
  References: [#9340](https://www.sqlalchemy.org/trac/ticket/9340)

### postgresql

- Fixed issue in PostgreSQL [ExcludeConstraint](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint) where
  literal values were being compiled as bound parameters and not direct
  inline values as is required for DDL.
  References: [#9349](https://www.sqlalchemy.org/trac/ticket/9349)
- Fixed issue where the PostgreSQL [ExcludeConstraint](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint)
  construct would not be copyable within operations such as
  [Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) as well as within some Alembic scenarios,
  if the constraint contained textual expression elements.
  References: [#9401](https://www.sqlalchemy.org/trac/ticket/9401)

### mysql

- The support for pool ping listeners to receive exception events via the
  [DialectEvents.handle_error()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.handle_error) event added in 2.0.0b1 for
  [#5648](https://www.sqlalchemy.org/trac/ticket/5648) failed to take into account dialect-specific ping routines
  such as that of MySQL and PostgreSQL. The dialect feature has been reworked
  so that all dialects participate within event handling.   Additionally,
  a new boolean element [ExceptionContext.is_pre_ping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext.is_pre_ping) is added
  which identifies if this operation is occurring within the pre-ping
  operation.
  For this release, third party dialects which implement a custom
  [Dialect.do_ping()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.do_ping) method can opt in to the newly improved
  behavior by having their method no longer catch exceptions or check
  exceptions for “is_disconnect”, instead just propagating all exceptions
  outwards. Checking the exception for “is_disconnect” is now done by an
  enclosing method on the default dialect, which ensures that the event hook
  is invoked for all exception scenarios before testing the exception as a
  “disconnect” exception. If an existing `do_ping()` method continues to
  catch exceptions and check “is_disconnect”, it will continue to work as it
  did previously, but `handle_error` hooks will not have access to the
  exception if it isn’t propagated outwards.
  References: [#5648](https://www.sqlalchemy.org/trac/ticket/5648)

### sqlite

- Fixed regression for SQLite connections where use of the `deterministic`
  parameter when establishing database functions would fail for older SQLite
  versions, those prior to version 3.8.3. The version checking logic has been
  improved to accommodate for this case.
  References: [#9379](https://www.sqlalchemy.org/trac/ticket/9379)

### mssql

- Fixed issue in the new [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) datatype which prevented it from
  working with the pymssql driver. As pymssql seems to be maintained again,
  restored testing support for pymssql.
  References: [#9414](https://www.sqlalchemy.org/trac/ticket/9414)
- Tweaked the pymssql dialect to take better advantage of
  RETURNING for INSERT statements in order to retrieve last inserted primary
  key values, in the same way as occurs for the mssql+pyodbc dialect right
  now.

### misc

- Fixed issue in automap where calling [AutomapBase.prepare()](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase.prepare)
  from a specific mapped class, rather than from the
  [AutomapBase](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase) directly, would not use the correct base
  class when automap detected new tables, instead using the given class,
  leading to mappers trying to configure inheritance. While one should
  normally call [AutomapBase.prepare()](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase.prepare) from the base in any
  case, it shouldn’t misbehave that badly when called from a subclass.
  References: [#9367](https://www.sqlalchemy.org/trac/ticket/9367)
- Fixed regression caused by typing added to `sqlalchemy.ext.mutable` for
  [#8667](https://www.sqlalchemy.org/trac/ticket/8667), where the semantics of the `.pop()` method changed such
  that the method was non-working. Pull request courtesy Nils Philippsen.
  References: [#9380](https://www.sqlalchemy.org/trac/ticket/9380)

## 2.0.4

Released: February 17, 2023

### orm

- To accommodate a change in column ordering used by ORM Declarative in
  SQLAlchemy 2.0, a new parameter [mapped_column.sort_order](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.sort_order)
  has been added that can be used to control the order of the columns defined
  in the table by the ORM, for common use cases such as mixins with primary
  key columns that should appear first in tables. The change notes at
  [ORM Declarative Applies Column Orders Differently; Control behavior using sort_order](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-9297) illustrate the default change in ordering behavior
  (which is part of all SQLAlchemy 2.0 releases) as well as use of the
  [mapped_column.sort_order](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.sort_order) to control column ordering when
  using mixins and multiple classes (new in 2.0.4).
  See also
  [ORM Declarative Applies Column Orders Differently; Control behavior using sort_order](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-9297)
  References: [#9297](https://www.sqlalchemy.org/trac/ticket/9297)
- The [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) method will now immediately load a
  relationship-bound attribute that is explicitly named within the
  [Session.refresh.attribute_names](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh.params.attribute_names) collection even if it is
  currently linked to the “select” loader, which normally is a “lazy” loader
  that does not fire off during a refresh. The “lazy loader” strategy will
  now detect that the operation is specifically a user-initiated
  [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) operation which named this attribute
  explicitly, and will then call upon the “immediateload” strategy to
  actually emit SQL to load the attribute. This should be helpful in
  particular for some asyncio situations where the loading of an unloaded
  lazy-loaded attribute must be forced, without using the actual lazy-loading
  attribute pattern not supported in asyncio.
  References: [#9298](https://www.sqlalchemy.org/trac/ticket/9298)
- Fixed regression introduced in version 2.0.2 due to [#9217](https://www.sqlalchemy.org/trac/ticket/9217) where
  using DML RETURNING statements, as well as
  [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) constructs as was “fixed” in
  [#9217](https://www.sqlalchemy.org/trac/ticket/9217), in conjunction with ORM mapped classes that used
  expressions such as with [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), would lead to an
  internal error within Core where it would attempt to match the expression
  by name. The fix repairs the Core issue, and also adjusts the fix in
  [#9217](https://www.sqlalchemy.org/trac/ticket/9217) to not take effect for the DML RETURNING use case, where it
  adds unnecessary overhead.
  References: [#9273](https://www.sqlalchemy.org/trac/ticket/9273)
- Marked the internal `EvaluatorCompiler` module as private to the ORM, and
  renamed it to `_EvaluatorCompiler`. For users that may have been relying
  upon this, the name `EvaluatorCompiler` is still present, however this
  use is not supported and will be removed in a future release.

### orm declarative

- Added new parameter `dataclasses_callable` to both the
  [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) class as well as the
  [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) method which allows an
  alternative callable to Python `dataclasses.dataclass` to be used in
  order to produce dataclasses. The use case here is to drop in Pydantic’s
  dataclass function instead. Adjustments have been made to the mixin support
  added for [#9179](https://www.sqlalchemy.org/trac/ticket/9179) in version 2.0.1 so that the `__annotations__`
  collection of the mixin is rewritten to not include the
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) container, in the same way as occurs with mapped
  classes, so that the Pydantic dataclasses constructor is not exposed to
  unknown types.
  See also
  [Integrating with Alternate Dataclass Providers such as Pydantic](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#dataclasses-pydantic)
  References: [#9266](https://www.sqlalchemy.org/trac/ticket/9266)

### sql

- Fixed issue where element types of a tuple value would be hardcoded to take
  on the types from a compared-to tuple, when the comparison were using the
  [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) operator. This was inconsistent with the usual
  way that types are determined for a binary expression, which is that the
  actual element type on the right side is considered first before applying
  the left-hand-side type.
  References: [#9313](https://www.sqlalchemy.org/trac/ticket/9313)
- Added public property [Table.autoincrement_column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.autoincrement_column) that
  returns the column identified as autoincrementing in the column.
  References: [#9277](https://www.sqlalchemy.org/trac/ticket/9277)

### typing

- Improved the typing support for the [Hybrid Attributes](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html)
  extension, updated all documentation to use ORM Annotated Declarative
  mappings, and added a new modifier called [hybrid_property.inplace](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property.inplace).
  This modifier provides a way to alter the state of a [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property) **in place**, which is essentially what very early versions of hybrids
  did, before SQLAlchemy version 1.2.0 [#3912](https://www.sqlalchemy.org/trac/ticket/3912) changed this to
  remove in-place mutation.  This in-place mutation is now restored on an
  **opt-in** basis to allow a single hybrid to have multiple methods
  set up, without the need to name all the methods the same and without the
  need to carefully “chain” differently-named methods in order to maintain
  the composition.  Typing tools such as Mypy and Pyright do not allow
  same-named methods on a class, so with this change a succinct method
  of setting up hybrids with typing support is restored.
  See also
  [Using inplace to create pep-484 compliant hybrid properties](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#hybrid-pep484-naming)
  References: [#9321](https://www.sqlalchemy.org/trac/ticket/9321)

### oracle

- Adjusted the behavior of the `thick_mode` parameter for the
  [python-oracledb](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracledb) dialect to correctly accept `False` as a value.
  Previously, only `None` would indicate that thick mode should be
  disabled.
  References: [#9295](https://www.sqlalchemy.org/trac/ticket/9295)

## 2.0.3

Released: February 9, 2023

### sql

- Fixed critical regression in SQL expression formulation in the 2.0 series
  due to [#7744](https://www.sqlalchemy.org/trac/ticket/7744) which improved support for SQL expressions that
  contained many elements against the same operator repeatedly; parenthesis
  grouping would be lost with expression elements beyond the first two
  elements.
  References: [#9271](https://www.sqlalchemy.org/trac/ticket/9271)

### typing

- Remove `typing.Self` workaround, now using [PEP 673](https://peps.python.org/pep-0673/) for most methods
  that return `Self`. As a consequence of this change `mypy>=1.0.0` is
  now required to type check SQLAlchemy code.
  Pull request courtesy Yurii Karabas.
  References: [#9254](https://www.sqlalchemy.org/trac/ticket/9254)

## 2.0.2

Released: February 6, 2023

### orm

- Added new event hook [MapperEvents.after_mapper_constructed()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.after_mapper_constructed),
  which supplies an event hook to take place right as the
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object has been fully constructed, but before the
  [registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure) call has been called. This allows code that
  can create additional mappings and table structures based on the initial
  configuration of a [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper), which also integrates within
  Declarative configuration. Previously, when using Declarative, where the
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object is created within the class creation process,
  there was no documented means of running code at this point.  The change
  is to immediately benefit custom mapping schemes such as that
  of the [Versioning with a History Table](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-versioned-history) example, which generate additional
  mappers and tables in response to the creation of mapped classes.
  References: [#9220](https://www.sqlalchemy.org/trac/ticket/9220)
- The infrequently used [Mapper.iterate_properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.iterate_properties) attribute and
  [Mapper.get_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.get_property) method, which are primarily used
  internally, no longer implicitly invoke the [registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure)
  process. Public access to these methods is extremely rare and the only
  benefit to having [registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure) would have been allowing
  “backref” properties be present in these collections. In order to support
  the new [MapperEvents.after_mapper_constructed()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.after_mapper_constructed) event, iteration
  and access to the internal [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty) objects is now
  possible without triggering an implicit configure of the mapper itself.
  The more-public facing route to iteration of all mapper attributes, the
  [Mapper.attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.attrs) collection and similar, will still implicitly
  invoke the [registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure) step thus making backref
  attributes available.
  In all cases, the [registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure) is always available to
  be called directly.
  References: [#9220](https://www.sqlalchemy.org/trac/ticket/9220)
- Fixed obscure ORM inheritance issue caused by [#8705](https://www.sqlalchemy.org/trac/ticket/8705) where some
  scenarios of inheriting mappers that indicated groups of columns from the
  local table and the inheriting table together under a
  [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) would nonetheless warn that properties of the
  same name were being combined implicitly.
  References: [#9232](https://www.sqlalchemy.org/trac/ticket/9232)
- Fixed regression where using the [Mapper.version_id_col](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.version_id_col)
  feature with a regular Python-side incrementing column would fail to work
  for SQLite and other databases that don’t support “rowcount” with
  “RETURNING”, as “RETURNING” would be assumed for such columns even though
  that’s not what actually takes place.
  References: [#9228](https://www.sqlalchemy.org/trac/ticket/9228)
- Fixed regression when using [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) in an ORM
  context, where matching of columns to SQL labels based on name alone was
  disabled for ORM-statements that weren’t fully textual. This would prevent
  arbitrary SQL expressions with column-name labels from matching up to the
  entity to be loaded, which previously would work within the 1.4
  and previous series, so the previous behavior has been restored.
  References: [#9217](https://www.sqlalchemy.org/trac/ticket/9217)

### orm declarative

- Fixed regression caused by the fix for [#9171](https://www.sqlalchemy.org/trac/ticket/9171), which itself was
  fixing a regression, involving the mechanics of `__init__()` on classes
  that extend from [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase). The change made it such
  that `__init__()` was applied to the user-defined base if there were no
  `__init__()` method directly on the class. This has been adjusted so that
  `__init__()` is applied only if no other class in the hierarchy of the
  user-defined base has an `__init__()` method. This again allows
  user-defined base classes based on [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) to include
  mixins that themselves include a custom `__init__()` method.
  References: [#9249](https://www.sqlalchemy.org/trac/ticket/9249)
- Fixed issue in ORM Declarative Dataclass mappings related to newly added
  support for mixins added in 2.0.1 via [#9179](https://www.sqlalchemy.org/trac/ticket/9179), where a combination
  of using mixins plus ORM inheritance would mis-classify fields in some
  cases leading to field-level dataclass arguments such as `init=False` being
  lost.
  References: [#9226](https://www.sqlalchemy.org/trac/ticket/9226)
- Repaired ORM Declarative mappings to allow for the
  [Mapper.primary_key](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.primary_key) parameter to be specified within
  `__mapper_args__` when using [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column). Despite this
  usage being directly in the 2.0 documentation, the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) was
  not accepting the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct in this context. This
  feature was already working for the [Mapper.version_id_col](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.version_id_col)
  and [Mapper.polymorphic_on](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_on) parameters.
  As part of this change, the `__mapper_args__` attribute may be specified
  without using [declared_attr()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) on a non-mapped mixin class,
  including a `"primary_key"` entry that refers to [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  or [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) objects locally present on the mixin;
  Declarative will also translate these columns into the correct ones for a
  particular mapped class. This again was working already for the
  [Mapper.version_id_col](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.version_id_col) and
  [Mapper.polymorphic_on](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_on) parameters.  Additionally,
  elements within `"primary_key"` may be indicated as string names of
  existing mapped properties.
  References: [#9240](https://www.sqlalchemy.org/trac/ticket/9240)
- An explicit error is raised if a mapping attempts to mix the use of
  [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) with
  [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) within the same class hierarchy,
  as this produces issues with the dataclass function being applied at the
  wrong time to the mapped class, leading to errors during the mapping
  process.
  References: [#9211](https://www.sqlalchemy.org/trac/ticket/9211)

### examples

- Reworked the [Versioning with a History Table](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-versioned-history) to work with
  version 2.0, while at the same time improving the overall working of
  this example to use newer APIs, including a newly added hook
  [MapperEvents.after_mapper_constructed()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.after_mapper_constructed).
  References: [#9220](https://www.sqlalchemy.org/trac/ticket/9220)

### sql

- Added a full suite of new SQL bitwise operators, for performing
  database-side bitwise expressions on appropriate data values such as
  integers, bit-strings, and similar. Pull request courtesy Yegor Statkevich.
  See also
  [Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)
  References: [#8780](https://www.sqlalchemy.org/trac/ticket/8780)

### asyncio

- Repaired a regression caused by the fix for [#8419](https://www.sqlalchemy.org/trac/ticket/8419) which caused
  asyncpg connections to be reset (i.e. transaction `rollback()` called)
  and returned to the pool normally in the case that the connection were not
  explicitly returned to the connection pool and was instead being
  intercepted by Python garbage collection, which would fail if the garbage
  collection operation were being called outside of the asyncio event loop,
  leading to a large amount of stack trace activity dumped into logging
  and standard output.
  The correct behavior is restored, which is that all asyncio connections
  that are garbage collected due to not being explicitly returned to the
  connection pool are detached from the pool and discarded, along with a
  warning, rather than being returned the pool, as they cannot be reliably
  reset. In the case of asyncpg connections, the asyncpg-specific
  `terminate()` method will be used to end the connection more gracefully
  within this process as opposed to just dropping it.
  This change includes a small behavioral change that is hoped to be useful
  for debugging asyncio applications, where the warning that’s emitted in the
  case of asyncio connections being unexpectedly garbage collected has been
  made slightly more aggressive by moving it outside of a `try/except`
  block and into a `finally:` block, where it will emit unconditionally
  regardless of whether the detach/termination operation succeeded or not. It
  will also have the effect that applications or test suites which promote
  Python warnings to exceptions will see this as a full exception raise,
  whereas previously it was not possible for this warning to actually
  propagate as an exception. Applications and test suites which need to
  tolerate this warning in the interim should adjust the Python warnings
  filter to allow these warnings to not raise.
  The behavior for traditional sync connections remains unchanged, that
  garbage collected connections continue to be returned to the pool normally
  without emitting a warning. This will likely be changed in a future major
  release to at least emit a similar warning as is emitted for asyncio
  drivers, as it is a usage error for pooled connections to be intercepted by
  garbage collection without being properly returned to the pool.
  References: [#9237](https://www.sqlalchemy.org/trac/ticket/9237)

### mysql

- Fixed regression caused by issue [#9058](https://www.sqlalchemy.org/trac/ticket/9058) which adjusted the MySQL
  dialect’s `has_table()` to again use “DESCRIBE”, where the specific error
  code raised by MySQL version 8 when using a non-existent schema name was
  unexpected and failed to be interpreted as a boolean result.
  References: [#9251](https://www.sqlalchemy.org/trac/ticket/9251)
- Added support for MySQL 8’s new `AS <name> ON DUPLICATE KEY` syntax when
  using [Insert.on_duplicate_key_update()](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.Insert.on_duplicate_key_update), which is required for
  newer versions of MySQL 8 as the previous syntax using `VALUES()` now
  emits a deprecation warning with those versions. Server version detection
  is employed to determine if traditional MariaDB / MySQL < 8 `VALUES()`
  syntax should be used, vs. the newer MySQL 8 required syntax. Pull request
  courtesy Caspar Wylie.
  References: [#8626](https://www.sqlalchemy.org/trac/ticket/8626)

### sqlite

- Fixed the SQLite dialect’s `has_table()` function to correctly report
  False for queries that include a non-None schema name for a schema that
  doesn’t exist; previously, a database error was raised.
  References: [#9251](https://www.sqlalchemy.org/trac/ticket/9251)

## 2.0.1

Released: February 1, 2023

### orm

- Fixed regression where ORM models that used joined table inheritance with a
  composite foreign key would encounter an internal error in the mapper
  internals.
  References: [#9164](https://www.sqlalchemy.org/trac/ticket/9164)
- Improved the error reporting when linking strategy options from a base
  class to another attribute that’s off a subclass, where `of_type()`
  should be used. Previously, when [Load.options()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load.options) is used, the message
  would lack informative detail that `of_type()` should be used, which was
  not the case when linking the options directly. The informative detail now
  emits even if [Load.options()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load.options) is used.
  References: [#9182](https://www.sqlalchemy.org/trac/ticket/9182)

### orm declarative

- Added support for [PEP 484](https://peps.python.org/pep-0484/) `NewType` to be used in the
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) as well as within
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) constructs. These types will behave in the same way as
  custom subclasses of types right now; they must appear explicitly within
  the [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) to be mapped.
  References: [#9175](https://www.sqlalchemy.org/trac/ticket/9175)
- When using the [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) superclass, all classes within
  the hierarchy that are subclasses of this class will now be run through the
  `@dataclasses.dataclass` function whether or not they are actually
  mapped, so that non-ORM fields declared on non-mapped classes within the
  hierarchy will be used when mapped subclasses are turned into dataclasses.
  This behavior applies both to intermediary classes mapped with
  `__abstract__ = True` as well as to the user-defined declarative base
  itself, assuming [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) is present as a superclass for
  these classes.
  This allows non-mapped attributes such as `InitVar` declarations on
  superclasses to be used, without the need to run the
  `@dataclasses.dataclass` decorator explicitly on each non-mapped class.
  The new behavior is considered as correct as this is what the [PEP 681](https://peps.python.org/pep-0681/)
  implementation expects when using a superclass to indicate dataclass
  behavior.
  References: [#9179](https://www.sqlalchemy.org/trac/ticket/9179)
- Added support for [PEP 586](https://peps.python.org/pep-0586/) `Literal[]` to be used in the
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) as well as within
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) constructs. To use custom types such as these, they must
  appear explicitly within the [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map)
  to be mapped.  Pull request courtesy Frederik Aalund.
  As part of this change, the support for [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) in the
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) has been expanded to include
  support for `Literal[]` types consisting of string values to be used,
  in addition to `enum.Enum` datatypes.    If a `Literal[]` datatype
  is used within `Mapped[]` that is not linked in
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) to a specific datatype,
  a [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) will be used by default.
  See also
  [Using Python Enum or pep-586 Literal types in the type map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-enums)
  References: [#9187](https://www.sqlalchemy.org/trac/ticket/9187)
- Fixed issue involving the use of [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) within the
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) where the
  [Enum.native_enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.native_enum) parameter would not be correctly
  copied to the mapped column datatype, if it were overridden
  as stated in the documentation to set this parameter to False.
  References: [#9200](https://www.sqlalchemy.org/trac/ticket/9200)
- Fixed regression in [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) class where the registry’s
  default constructor would not be applied to the base itself, which is
  different from how the previous [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base) construct
  works. This would prevent a mapped class with its own `__init__()` method
  from calling `super().__init__()` in order to access the registry’s
  default constructor and automatically populate attributes, instead hitting
  `object.__init__()` which would raise a `TypeError` on any arguments.
  References: [#9171](https://www.sqlalchemy.org/trac/ticket/9171)
- Improved the ruleset used to interpret [PEP 593](https://peps.python.org/pep-0593/) `Annotated` types when
  used with Annotated Declarative mapping, the inner type will be checked for
  “Optional” in all cases which will be added to the criteria by which the
  column is set as “nullable” or not; if the type within the `Annotated`
  container is optional (or unioned with `None`), the column will be
  considered nullable if there are no explicit
  [mapped_column.nullable](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.nullable) parameters overriding it.
  References: [#9177](https://www.sqlalchemy.org/trac/ticket/9177)

### sql

- Corrected the fix for [#7664](https://www.sqlalchemy.org/trac/ticket/7664), released in version 2.0.0, to also
  include [DropSchema](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropSchema) which was inadvertently missed in this fix,
  allowing stringification without a dialect. The fixes for both constructs
  is backported to the 1.4 series as of 1.4.47.
  References: [#7664](https://www.sqlalchemy.org/trac/ticket/7664)
- Fixed regression related to the implementation for the new
  “insertmanyvalues” feature where an internal `TypeError` would occur in
  arrangements where a [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) would be referenced inside
  of another [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) via a CTE; made additional repairs for this
  use case for positional dialects such as asyncpg when using
  “insertmanyvalues”.
  References: [#9173](https://www.sqlalchemy.org/trac/ticket/9173)

### typing

- Opened up typing on [Select.with_for_update.of](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update.params.of) to also accept
  table and mapped class arguments, as seems to be available for the MySQL
  dialect.
  References: [#9174](https://www.sqlalchemy.org/trac/ticket/9174)
- Fixed typing for limit/offset methods including [Select.limit()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.limit),
  [Select.offset()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.offset), [Query.limit()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.limit), [Query.offset()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.offset)
  to allow `None`, which is the documented API to “cancel” the current
  limit/offset.
  References: [#9183](https://www.sqlalchemy.org/trac/ticket/9183)
- Fixed typing issue where [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) objects typed as
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) wouldn’t be accepted in schema constraints such as
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey), [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) or
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index).
  References: [#9170](https://www.sqlalchemy.org/trac/ticket/9170)
- Fixed typing for [ColumnElement.cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast) to accept
  both `Type[TypeEngine[T]]` and `TypeEngine[T]`; previously
  only `TypeEngine[T]` was accepted.  Pull request courtesy Yurii Karabas.
  References: [#9156](https://www.sqlalchemy.org/trac/ticket/9156)

## 2.0.0

Released: January 26, 2023

### orm

- Improved the notification of warnings that are emitted within the configure
  mappers or flush process, which are often invoked as part of a different
  operation, to add additional context to the message that indicates one of
  these operations as the source of the warning within operations that may
  not be obviously related.
  References: [#7305](https://www.sqlalchemy.org/trac/ticket/7305)

### orm extensions

- Added new option to horizontal sharding API
  [set_shard_id](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.set_shard_id) which sets the effective shard identifier
  to query against, for both the primary query as well as for all secondary
  loaders including relationship eager loaders as well as relationship and
  column lazy loaders.
  References: [#7226](https://www.sqlalchemy.org/trac/ticket/7226)
- Added new feature to [AutomapBase](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase) for autoload of classes across
  multiple schemas which may have overlapping names, by providing a
  [AutomapBase.prepare.modulename_for_table](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase.prepare.params.modulename_for_table) parameter which
  allows customization of the `__module__` attribute of newly generated
  classes, as well as a new collection [AutomapBase.by_module](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase.by_module), which
  stores a dot-separated namespace of module names linked to classes based on
  the `__module__` attribute.
  Additionally, the [AutomapBase.prepare()](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase.prepare) method may now be invoked
  any number of times, with or without reflection enabled; only newly
  added tables that were not previously mapped will be processed on each
  call.   Previously, the [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) method would need to be
  called explicitly each time.
  See also
  [Generating Mappings from Multiple Schemas](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#automap-by-module) - illustrates use of both techniques at once.
  References: [#5145](https://www.sqlalchemy.org/trac/ticket/5145)

### sql

- Fixed stringify for a the [CreateSchema](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateSchema) DDL construct, which
  would fail with an `AttributeError` when stringified without a
  dialect. Update: Note this fix failed to accommodate for
  [DropSchema](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropSchema); a followup fix in version 2.0.1 repairs this
  case. The fix for both elements is backported to 1.4.47.
  References: [#7664](https://www.sqlalchemy.org/trac/ticket/7664)

### typing

- Added typing for the built-in generic functions that are available from the
  [func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) namespace, which accept a particular set of arguments and
  return a particular type, such as for `count`,
  `current_timestamp`, etc.
  References: [#9129](https://www.sqlalchemy.org/trac/ticket/9129)
- Corrected the type passed for “lambda statements” so that a plain lambda is
  accepted by mypy, pyright, others without any errors about argument types.
  Additionally implemented typing for more of the public API for lambda
  statements and ensured [StatementLambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement) is part of the
  [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable) hierarchy so it’s typed as accepted by
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute).
  References: [#9120](https://www.sqlalchemy.org/trac/ticket/9120)
- The [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) and
  [ColumnOperators.not_in()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_in) methods are typed to include
  `Iterable[Any]` rather than `Sequence[Any]` for more flexibility in
  argument type.
  References: [#9122](https://www.sqlalchemy.org/trac/ticket/9122)
- The [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) and [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) from a typing perspective
  require the first argument to be present, however these functions still
  accept zero arguments which will emit a deprecation warning at runtime.
  Typing is also added to support sending the fixed literal `False` for
  [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) and `True` for [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) as the first argument
  only, however the documentation now indicates sending the
  [false()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.false) and [true()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.true) constructs in these cases as a
  more explicit approach.
  References: [#9123](https://www.sqlalchemy.org/trac/ticket/9123)
- Fixed typing issue where iterating over a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object
  was not correctly typed.
  References: [#9125](https://www.sqlalchemy.org/trac/ticket/9125)
- Fixed typing issue where the object type when using [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)
  as a context manager were not preserved, indicating [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)
  in all cases rather than the specific [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) sub-type.
  Pull request courtesy Martin Baláž.
  References: [#9136](https://www.sqlalchemy.org/trac/ticket/9136)
- Fixed issue where using the [relationship.remote_side](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side)
  and similar parameters, passing an annotated declarative object typed as
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped), would not be accepted by the type checker.
  References: [#9150](https://www.sqlalchemy.org/trac/ticket/9150)
- Added typing to legacy operators such as `isnot()`, `notin_()`, etc.
  which previously were referencing the newer operators but were not
  themselves typed.
  References: [#9148](https://www.sqlalchemy.org/trac/ticket/9148)

### postgresql

- Added support to the asyncpg dialect to return the `cursor.rowcount`
  value for SELECT statements when available. While this is not a typical use
  for `cursor.rowcount`, the other PostgreSQL dialects generally provide
  this value. Pull request courtesy Michael Gorven.
  This change is also **backported** to: 1.4.47
  References: [#9048](https://www.sqlalchemy.org/trac/ticket/9048)

### mysql

- Added support to MySQL index reflection to correctly reflect the
  `mysql_length` dictionary, which previously was being ignored.
  This change is also **backported** to: 1.4.47
  References: [#9047](https://www.sqlalchemy.org/trac/ticket/9047)

### mssql

- The newly added comment reflection and rendering capability of the MSSQL
  dialect, added in [#7844](https://www.sqlalchemy.org/trac/ticket/7844), will now be disabled by default if it
  cannot be determined that an unsupported backend such as Azure Synapse may
  be in use; this backend does not support table and column comments and does
  not support the SQL Server routines in use to generate them as well as to
  reflect them. A new parameter `supports_comments` is added to the dialect
  which defaults to `None`, indicating that comment support should be
  auto-detected. When set to `True` or `False`, the comment support is
  either enabled or disabled unconditionally.
  See also
  [DDL Comment Support](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-comment-support)
  References: [#9142](https://www.sqlalchemy.org/trac/ticket/9142)

## 2.0.0rc3

Released: January 18, 2023

### orm

- Added a new parameter to [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) called
  [Mapper.polymorphic_abstract](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_abstract). The purpose of this directive
  is so that the ORM will not consider the class to be instantiated or loaded
  directly, only subclasses. The actual effect is that the
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) will prevent direct instantiation of instances
  of the class and will expect that the class does not have a distinct
  polymorphic identity configured.
  In practice, the class that is mapped with
  [Mapper.polymorphic_abstract](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_abstract) can be used as the target of a
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) as well as be used in queries; subclasses must of
  course include polymorphic identities in their mappings.
  The new parameter is automatically applied to classes that subclass
  the [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) class, as this class is not intended
  to be instantiated.
  See also
  [Building Deeper Hierarchies with polymorphic_abstract](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#orm-inheritance-abstract-poly)
  References: [#9060](https://www.sqlalchemy.org/trac/ticket/9060)
- Fixed issue where using a pep-593 `Annotated` type in the
  [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) which itself contained a
  generic plain container or `collections.abc` type (e.g. `list`,
  `dict`, `collections.abc.Sequence`, etc. ) as the target type would
  produce an internal error when the ORM were trying to interpret the
  `Annotated` instance.
  References: [#9099](https://www.sqlalchemy.org/trac/ticket/9099)
- Added an error message when a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is mapped against
  an abstract container type, such as `Mapped[Sequence[B]]`, without
  providing the [relationship.container_class](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.container_class) parameter which
  is necessary when the type is abstract. Previously the abstract
  container would attempt to be instantiated at a later step and fail.
  References: [#9100](https://www.sqlalchemy.org/trac/ticket/9100)

### sql

- Fixed bug / regression where using [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) with the same name
  as a column in the [Update.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.values) method of [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update), as
  well as the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method of [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) in 2.0 only,
  would in some cases silently fail to honor the SQL expression in which the
  parameter were presented, replacing the expression with a new parameter of
  the same name and discarding any other elements of the SQL expression, such
  as SQL functions, etc. The specific case would be statements that were
  constructed against ORM entities rather than plain [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  instances, but would occur if the statement were invoked with a
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) or a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
  [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) part of the issue was present in both 2.0 and 1.4 and is
  backported to 1.4.
  This change is also **backported** to: 1.4.47
  References: [#9075](https://www.sqlalchemy.org/trac/ticket/9075)

### typing

- Fixes to the annotations within the `sqlalchemy.ext.hybrid` extension for
  more effective typing of user-defined methods. The typing now uses
  [PEP 612](https://peps.python.org/pep-0612/) features, now supported by recent versions of Mypy, to maintain
  argument signatures for [hybrid_method](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_method). Return values for hybrid
  methods are accepted as SQL expressions in contexts such as
  [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where) while still supporting SQL methods.
  References: [#9096](https://www.sqlalchemy.org/trac/ticket/9096)

### mypy

- Adjustments made to the mypy plugin to accommodate for some potential
  changes being made for issue #236 sqlalchemy2-stubs when using SQLAlchemy
  1.4. These changes are being kept in sync within SQLAlchemy 2.0.
  The changes are also backwards compatible with older versions of
  sqlalchemy2-stubs.
  This change is also **backported** to: 1.4.47
- Fixed crash in mypy plugin which could occur on both 1.4 and 2.0 versions
  if a decorator for the [mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped) decorator were used
  that was referenced in an expression with more than two components (e.g.
  `@Backend.mapper_registry.mapped`). This scenario is now ignored; when
  using the plugin, the decorator expression needs to be two components (i.e.
  `@reg.mapped`).
  This change is also **backported** to: 1.4.47
  References: [#9102](https://www.sqlalchemy.org/trac/ticket/9102)

### postgresql

- Fixed regression where psycopg3 changed an API call as of version 3.1.8 to
  expect a specific object type that was previously not enforced, breaking
  connectivity for the psycopg3 dialect.
  References: [#9106](https://www.sqlalchemy.org/trac/ticket/9106)

### oracle

- Added support for the Oracle SQL type `TIMESTAMP WITH LOCAL TIME ZONE`,
  using a newly added Oracle-specific [TIMESTAMP](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.TIMESTAMP) datatype.
  References: [#9086](https://www.sqlalchemy.org/trac/ticket/9086)

## 2.0.0rc2

Released: January 9, 2023

### orm

- Fixed issue where an overly restrictive ORM mapping rule were added in 2.0
  which prevented mappings against [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause) objects, such as
  those used in the view recipe on the wiki.
  References: [#9071](https://www.sqlalchemy.org/trac/ticket/9071)

### typing

- The Data Class Transforms argument `field_descriptors` was renamed
  to `field_specifiers` in the accepted version of PEP 681.
  References: [#9067](https://www.sqlalchemy.org/trac/ticket/9067)

### postgresql

- Implemented missing `JSONB` operations:
  - `@@` using [Comparator.path_match()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB.Comparator.path_match)
  - `@?` using [Comparator.path_exists()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB.Comparator.path_exists)
  - `#-` using [Comparator.delete_path()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB.Comparator.delete_path)
  Pull request courtesy of Guilherme Martins Crocetti.
  References: [#7147](https://www.sqlalchemy.org/trac/ticket/7147)

### mysql

- Restored the behavior of [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table) to report on
  temporary tables for MySQL / MariaDB. This is currently the behavior for
  all other included dialects, but was removed for MySQL in 1.4 due to no
  longer using the DESCRIBE command; there was no documented support for temp
  tables being reported by the [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table) method in this
  version or on any previous version, so the previous behavior was undefined.
  As SQLAlchemy 2.0 has added formal support for temp table status via
  [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table), the MySQL /MariaDB dialect has been reverted
  to use the “DESCRIBE” statement as it did in the SQLAlchemy 1.3 series and
  previously, and test support is added to include MySQL / MariaDB for
  this behavior.   The previous issues with ROLLBACK being emitted which
  1.4 sought to improve upon don’t apply in SQLAlchemy 2.0 due to
  simplifications in how [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) handles transactions.
  DESCRIBE is necessary as MariaDB in particular has no consistently
  available public information schema of any kind in order to report on temp
  tables other than DESCRIBE/SHOW COLUMNS, which rely on throwing an error
  in order to report no results.
  References: [#9058](https://www.sqlalchemy.org/trac/ticket/9058)

### oracle

- Supported use case for foreign key constraints where the local column is
  marked as “invisible”. The errors normally generated when a
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) is created that check for the target column
  are disabled when reflecting, and the constraint is skipped with a warning
  in the same way which already occurs for an [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) with a similar
  issue.
  References: [#9059](https://www.sqlalchemy.org/trac/ticket/9059)

## 2.0.0rc1

Released: December 28, 2022

### general

- Fixed regression where the base compat module was calling upon
  `platform.architecture()` in order to detect some system properties,
  which results in an over-broad system call against the system-level
  `file` call that is unavailable under some circumstances, including
  within some secure environment configurations.
  This change is also **backported** to: 1.4.46
  References: [#8995](https://www.sqlalchemy.org/trac/ticket/8995)

### orm

- Added a new default value for the [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults)
  parameter “auto”, which will automatically fetch table default values
  during a unit of work flush, if the dialect supports RETURNING for the
  INSERT being run, as well as
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) available. Eager fetches
  for server-side UPDATE defaults, which are very uncommon, continue to only
  take place if [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) is set to `True`, as
  there is no batch-RETURNING form for UPDATE statements.
  References: [#8889](https://www.sqlalchemy.org/trac/ticket/8889)
- Adjustments to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) in terms of extensibility,
  as well as updates to the [ShardedSession](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedSession) extension:
  - [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) now accepts
    [Session.get.bind_arguments](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get.params.bind_arguments), which in particular may be
    useful when using the horizontal sharding extension.
  - [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind) accepts arbitrary kw arguments, which
    assists in developing code that uses a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class which
    overrides this method with additional arguments.
  - Added a new ORM execution option `identity_token` which may be used
    to directly affect the “identity token” that will be associated with
    newly loaded ORM objects.  This token is how sharding approaches
    (namely the [ShardedSession](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedSession), but can be used in other cases
    as well) separate object identities across different “shards”.
    See also
    [Identity Token](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#queryguide-identity-token)
  - The [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute) event hook may now be used
    to affect all ORM-related options, including `autoflush`,
    `populate_existing`, and `yield_per`; these options are re-consumed
    subsequent to event hooks being invoked before they are acted upon.
    Previously, options like `autoflush` would have been already evaluated
    at this point. The new `identity_token` option is also supported in
    this mode and is now used by the horizontal sharding extension.
  - The [ShardedSession](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedSession) class replaces the
    [ShardedSession.id_chooser](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedSession.params.id_chooser) hook with a new hook
    [ShardedSession.identity_chooser](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedSession.params.identity_chooser), which no longer relies upon
    the legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object.
    [ShardedSession.id_chooser](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedSession.params.id_chooser) is still accepted in place of
    [ShardedSession.identity_chooser](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedSession.params.identity_chooser) with a deprecation warning.
  References: [#7837](https://www.sqlalchemy.org/trac/ticket/7837)
- The behavior of “joining an external transaction into a Session” has been
  revised and improved, allowing explicit control over how the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will accommodate an incoming
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) that already has a transaction and possibly a
  savepoint already established. The new parameter
  [Session.join_transaction_mode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.join_transaction_mode) includes a series of option
  values which can accommodate the existing transaction in several ways, most
  importantly allowing a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to operate in a fully
  transactional style using savepoints exclusively, while leaving the
  externally initiated transaction non-committed and active under all
  circumstances, allowing test suites to rollback all changes that take place
  within tests.
  Additionally, revised the [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) method to fully close
  out savepoints that may still be present, which also allows the
  “external transaction” recipe to proceed without warnings if the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) did not explicitly end its own SAVEPOINT
  transactions.
  See also
  [New transaction join modes for Session](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-9015)
  References: [#9015](https://www.sqlalchemy.org/trac/ticket/9015)
- Removed the requirement that the `__allow_unmapped__` attribute be used
  on Declarative Dataclass Mapped class when non-`Mapped[]` annotations are
  detected; previously, an error message that was intended to support legacy
  ORM typed mappings would be raised, which additionally did not mention
  correct patterns to use with Dataclasses specifically. This error message
  is now no longer raised if [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) or
  [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) is used.
  See also
  [Using Non-Mapped Dataclass Fields](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses-non-mapped-fields)
  References: [#8973](https://www.sqlalchemy.org/trac/ticket/8973)
- Fixed issue in the internal SQL traversal for DML statements like
  [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) which would cause among other
  potential issues, a specific issue using lambda statements with the ORM
  update/delete feature.
  This change is also **backported** to: 1.4.46
  References: [#9033](https://www.sqlalchemy.org/trac/ticket/9033)
- Fixed bug where [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) would fail to preserve the
  current loaded contents of relationship attributes that were indicated with
  the [relationship.viewonly](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.viewonly) parameter, thus defeating
  strategies that use [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) to pull fully loaded objects
  from caches and other similar techniques. In a related change, fixed issue
  where an object that contains a loaded relationship that was nonetheless
  configured as `lazy='raise'` on the mapping would fail when passed to
  [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge); checks for “raise” are now suspended within
  the merge process assuming the [Session.merge.load](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge.params.load)
  parameter remains at its default of `True`.
  Overall, this is a behavioral adjustment to a change introduced in the 1.4
  series as of [#4994](https://www.sqlalchemy.org/trac/ticket/4994), which took “merge” out of the set of cascades
  applied by default to “viewonly” relationships. As “viewonly” relationships
  aren’t persisted under any circumstances, allowing their contents to
  transfer during “merge” does not impact the persistence behavior of the
  target object. This allows [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) to correctly suit one
  of its use cases, that of adding objects to a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) that were
  loaded elsewhere, often for the purposes of restoring from a cache.
  This change is also **backported** to: 1.4.45
  References: [#8862](https://www.sqlalchemy.org/trac/ticket/8862)
- Fixed issues in [with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) where expressions that were
  composed of columns that were referenced from the enclosing SELECT would
  not render correct SQL in some contexts, in the case where the expression
  had a label name that matched the attribute which used
  [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression), even when [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression) had
  no default expression. For the moment, if the [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression)
  does have a default expression, that label name is still used for that
  default, and an additional label with the same name will continue to be
  ignored. Overall, this case is pretty thorny so further adjustments might
  be warranted.
  This change is also **backported** to: 1.4.45
  References: [#8881](https://www.sqlalchemy.org/trac/ticket/8881)
- A warning is emitted if a backref name used in [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
  names an attribute on the target class which already has a method or
  attribute assigned to that name, as the backref declaration will replace
  that attribute.
  References: [#4629](https://www.sqlalchemy.org/trac/ticket/4629)
- A series of changes and improvements regarding
  [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh). The overall change is that primary key
  attributes for an object are now included in a refresh operation
  unconditionally when relationship-bound attributes are to be refreshed,
  even if not expired and even if not specified in the refresh.
  - Improved [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) so that if autoflush is enabled
    (as is the default for [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)), the autoflush takes place
    at an earlier part of the refresh process so that pending primary key
    changes are applied without errors being raised.  Previously, this
    autoflush took place too late in the process and the SELECT statement
    would not use the correct key to locate the row and an
    [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) would be raised.
  - When the above condition is present, that is, unflushed primary key
    changes are present on the object, but autoflush is not enabled,
    the refresh() method now explicitly disallows the operation to proceed,
    and an informative [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) is raised asking that
    the pending primary key changes be flushed first.  Previously,
    this use case was simply broken and [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError)
    would be raised anyway. This restriction is so that it’s safe for the
    primary key attributes to be refreshed, as is necessary for the case of
    being able to refresh the object with relationship-bound secondary
    eagerloaders also being emitted. This rule applies in all cases to keep
    API behavior consistent regardless of whether or not the PK cols are
    actually needed in the refresh, as it is unusual to be refreshing
    some attributes on an object while keeping other attributes “pending”
    in any case.
  - The [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) method has been enhanced such that
    attributes which are [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-bound and linked to an
    eager loader, either at mapping time or via last-used loader options,
    will be refreshed in all cases even when a list of attributes is passed
    that does not include any columns on the parent row. This builds upon the
    feature first implemented for non-column attributes as part of
    [#1763](https://www.sqlalchemy.org/trac/ticket/1763) fixed in 1.4 allowing eagerly-loaded relationship-bound
    attributes to participate in the [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) operation.
    If the refresh operation does not indicate any columns on the parent row
    to be refreshed, the primary key columns will nonetheless be included
    in the refresh operation, which allows the load to proceed into the
    secondary relationship loaders indicated as it does normally.
    Previously an [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) error would be raised
    for this condition ([#8703](https://www.sqlalchemy.org/trac/ticket/8703))
  - Fixed issue where an unnecessary additional SELECT would be emitted in
    the case where [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) were called with a
    combination of expired attributes, as well as an eager loader such as
    [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) that emits a “secondary” query, if the primary
    key attributes were also in an expired state.  As the primary key
    attributes are now included in the refresh automatically, there is no
    additional load for these attributes when a relationship loader
    goes to select for them ([#8997](https://www.sqlalchemy.org/trac/ticket/8997))
  - Fixed regression caused by [#8126](https://www.sqlalchemy.org/trac/ticket/8126) released in 2.0.0b1 where the
    [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) method would fail with an
    `AttributeError`, if passed both an expired column name as well as the
    name of a relationship-bound attribute that was linked to a “secondary”
    eagerloader such as the [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) eager loader
    ([#8996](https://www.sqlalchemy.org/trac/ticket/8996))
  References: [#8703](https://www.sqlalchemy.org/trac/ticket/8703), [#8996](https://www.sqlalchemy.org/trac/ticket/8996), [#8997](https://www.sqlalchemy.org/trac/ticket/8997)
- Improved a fix first made in version 1.4 for [#8456](https://www.sqlalchemy.org/trac/ticket/8456) which scaled
  back the usage of internal “polymorphic adapters”, that are used to render
  ORM queries when the [Mapper.with_polymorphic](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.with_polymorphic) parameter is
  used. These adapters, which are very complex and error prone, are now used
  only in those cases where an explicit user-supplied subquery is used for
  [Mapper.with_polymorphic](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.with_polymorphic), which includes only the use case
  of concrete inheritance mappings that use the
  [polymorphic_union()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.polymorphic_union) helper, as well as the legacy use case of
  using an aliased subquery for joined inheritance mappings, which is not
  needed in modern use.
  For the most common case of joined inheritance mappings that use the
  built-in polymorphic loading scheme, which includes those which make use of
  the [Mapper.polymorphic_load](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_load) parameter set to `inline`,
  polymorphic adapters are now no longer used. This has both a positive
  performance impact on the construction of queries as well as a
  substantial simplification of the internal query rendering process.
  The specific issue targeted was to allow a [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property)
  to refer to joined-inheritance classes within a scalar subquery, which now
  works as intuitively as is feasible.
  References: [#8168](https://www.sqlalchemy.org/trac/ticket/8168)

### engine

- Fixed a long-standing race condition in the connection pool which could
  occur under eventlet/gevent monkeypatching schemes in conjunction with the
  use of eventlet/gevent `Timeout` conditions, where a connection pool
  checkout that’s interrupted due to the timeout would fail to clean up the
  failed state, causing the underlying connection record and sometimes the
  database connection itself to “leak”, leaving the pool in an invalid state
  with unreachable entries. This issue was first identified and fixed in
  SQLAlchemy 1.2 for [#4225](https://www.sqlalchemy.org/trac/ticket/4225), however the failure modes detected in
  that fix failed to accommodate for `BaseException`, rather than
  `Exception`, which prevented eventlet/gevent `Timeout` from being
  caught. In addition, a block within initial pool connect has also been
  identified and hardened with a `BaseException` -> “clean failed connect”
  block to accommodate for the same condition in this location.
  Big thanks to Github user @niklaus for their tenacious efforts in
  identifying and describing this intricate issue.
  This change is also **backported** to: 1.4.46
  References: [#8974](https://www.sqlalchemy.org/trac/ticket/8974)
- Fixed issue where [Result.freeze()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.freeze) method would not work for
  textual SQL using either [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) or
  [Connection.exec_driver_sql()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.exec_driver_sql).
  This change is also **backported** to: 1.4.45
  References: [#8963](https://www.sqlalchemy.org/trac/ticket/8963)

### sql

- An informative re-raise is now thrown in the case where any “literal
  bindparam” render operation fails, indicating the value itself and
  the datatype in use, to assist in debugging when literal params
  are being rendered in a statement.
  This change is also **backported** to: 1.4.45
  References: [#8800](https://www.sqlalchemy.org/trac/ticket/8800)
- Fixed issue in lambda SQL feature where the calculated type of a literal
  value would not take into account the type coercion rules of the “compared
  to type”, leading to a lack of typing information for SQL expressions, such
  as comparisons to [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) elements and similar.
  This change is also **backported** to: 1.4.46
  References: [#9029](https://www.sqlalchemy.org/trac/ticket/9029)
- Fixed a series of issues regarding the position and sometimes the identity
  of rendered bound parameters, such as those used for SQLite, asyncpg,
  MySQL, Oracle and others. Some compiled forms would not maintain the order
  of parameters correctly, such as the PostgreSQL `regexp_replace()`
  function, the “nesting” feature of the [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) construct first
  introduced in [#4123](https://www.sqlalchemy.org/trac/ticket/4123), and selectable tables formed by using the
  [FunctionElement.column_valued()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.column_valued) method with Oracle.
  This change is also **backported** to: 1.4.45
  References: [#8827](https://www.sqlalchemy.org/trac/ticket/8827)
- Added test support to ensure that all compiler `visit_xyz()` methods
  across all `Compiler` implementations in SQLAlchemy accept a
  `**kw` parameter, so that all compilers accept additional keyword
  arguments under all circumstances.
  References: [#8988](https://www.sqlalchemy.org/trac/ticket/8988)
- The [SQLCompiler.construct_params()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler.construct_params) method, as well as the
  [SQLCompiler.params](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler.params) accessor, will now return the
  exact parameters that correspond to a compiled statement that used
  the `render_postcompile` parameter to compile.   Previously,
  the method returned a parameter structure that by itself didn’t correspond
  to either the original parameters or the expanded ones.
  Passing a new dictionary of parameters to
  [SQLCompiler.construct_params()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler.construct_params) for a [SQLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler) that was
  constructed with `render_postcompile` is now disallowed; instead, to make
  a new SQL string and parameter set for an alternate set of parameters, a
  new method [SQLCompiler.construct_expanded_state()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler.construct_expanded_state) is added which
  will produce a new expanded form for the given parameter set, using the
  [ExpandedState](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.ExpandedState) container which includes a new SQL statement
  and new parameter dictionary, as well as a positional parameter tuple.
  References: [#6114](https://www.sqlalchemy.org/trac/ticket/6114)
- To accommodate for third party dialects with different character escaping
  needs regarding bound parameters, the system by which SQLAlchemy “escapes”
  (i.e., replaces with another character in its place) special characters in
  bound parameter names has been made extensible for third party dialects,
  using the `SQLCompiler.bindname_escape_chars` dictionary which can
  be overridden at the class declaration level on any [SQLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler)
  subclass. As part of this change, also added the dot `"."` as a default
  “escaped” character.
  References: [#8994](https://www.sqlalchemy.org/trac/ticket/8994)

### typing

- pep-484 typing has been completed for the
  `sqlalchemy.ext.horizontal_shard` extension as well as the
  `sqlalchemy.orm.events` module. Thanks to Gleb Kisenkov for their
  efforts.
  References: [#6810](https://www.sqlalchemy.org/trac/ticket/6810), [#9025](https://www.sqlalchemy.org/trac/ticket/9025)

### asyncio

- Removed non-functional `merge()` method from
  [AsyncResult](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncResult).  This method has never worked and was
  included with [AsyncResult](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncResult) in error.
  This change is also **backported** to: 1.4.45
  References: [#8952](https://www.sqlalchemy.org/trac/ticket/8952)

### postgresql

- Fixed bug where the PostgreSQL
  [Insert.on_conflict_do_update.constraint](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert.on_conflict_do_update.params.constraint) parameter
  would accept an [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) object, however would not expand this index
  out into its individual index expressions, instead rendering its name in an
  ON CONFLICT ON CONSTRAINT clause, which is not accepted by PostgreSQL; the
  “constraint name” form only accepts unique or exclude constraint names. The
  parameter continues to accept the index but now expands it out into its
  component expressions for the render.
  This change is also **backported** to: 1.4.46
  References: [#9023](https://www.sqlalchemy.org/trac/ticket/9023)
- Made an adjustment to how the PostgreSQL dialect considers column types
  when it reflects columns from a table, to accommodate for alternative
  backends which may return NULL from the PG `format_type()` function.
  This change is also **backported** to: 1.4.45
  References: [#8748](https://www.sqlalchemy.org/trac/ticket/8748)
- Added support for explicit use of PG full text functions with asyncpg and
  psycopg (SQLAlchemy 2.0 only), with regards to the `REGCONFIG` type cast
  for the first argument, which previously would be incorrectly cast to a
  VARCHAR, causing failures on these dialects that rely upon explicit type
  casts. This includes support for [to_tsvector](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.to_tsvector),
  [to_tsquery](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.to_tsquery), [plainto_tsquery](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.plainto_tsquery),
  [phraseto_tsquery](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.phraseto_tsquery),
  [websearch_to_tsquery](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.websearch_to_tsquery),
  [ts_headline](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ts_headline), each of which will determine based on
  number of arguments passed if the first string argument should be
  interpreted as a PostgreSQL “REGCONFIG” value; if so, the argument is typed
  using a newly added type object [REGCONFIG](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.REGCONFIG) which is
  then explicitly cast in the SQL expression.
  References: [#8977](https://www.sqlalchemy.org/trac/ticket/8977)
- Fixed regression where newly revised PostgreSQL range types such as
  [INT4RANGE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.INT4RANGE) could not be set up as the impl of a
  [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) custom type, instead raising a `TypeError`.
  References: [#9020](https://www.sqlalchemy.org/trac/ticket/9020)
- The `Range.__eq___()` will now return `NotImplemented`
  when comparing with an instance of a different class, instead of raising
  an `AttributeError` exception.
  References: [#8984](https://www.sqlalchemy.org/trac/ticket/8984)

### sqlite

- Added support for the SQLite backend to reflect the “DEFERRABLE” and
  “INITIALLY” keywords which may be present on a foreign key construct. Pull
  request courtesy Michael Gorven.
  This change is also **backported** to: 1.4.45
  References: [#8903](https://www.sqlalchemy.org/trac/ticket/8903)
- Added support for reflection of expression-oriented WHERE criteria included
  in indexes on the SQLite dialect, in a manner similar to that of the
  PostgreSQL dialect. Pull request courtesy Tobias Pfeiffer.
  This change is also **backported** to: 1.4.45
  References: [#8804](https://www.sqlalchemy.org/trac/ticket/8804)

### oracle

- Fixed issue in Oracle compiler where the syntax for
  [FunctionElement.column_valued()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.column_valued) was incorrect, rendering the name
  `COLUMN_VALUE` without qualifying the source table correctly.
  This change is also **backported** to: 1.4.45
  References: [#8945](https://www.sqlalchemy.org/trac/ticket/8945)

### tests

- Fixed issue in tox.ini file where changes in the tox 4.0 series to the
  format of “passenv” caused tox to not function correctly, in particular
  raising an error as of tox 4.0.6.
  This change is also **backported** to: 1.4.46
- Added new exclusion rule for third party dialects called
  `unusual_column_name_characters`, which can be “closed” for third party
  dialects that don’t support column names with unusual characters such as
  dots, slashes, or percent signs in them, even if the name is properly
  quoted.
  This change is also **backported** to: 1.4.46
  References: [#9002](https://www.sqlalchemy.org/trac/ticket/9002)

## 2.0.0b4

Released: December 5, 2022

### orm

- Added a new parameter [mapped_column.use_existing_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.use_existing_column) to
  accommodate the use case of a single-table inheritance mapping that uses
  the pattern of more than one subclass indicating the same column to take
  place on the superclass. This pattern was previously possible by using
  [declared_attr()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) in conjunction with locating the existing column
  in the `.__table__` of the superclass, however is now updated to work
  with [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) as well as with pep-484 typing, in a
  simple and succinct way.
  See also
  [Resolving Column Conflicts with use_existing_column](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#orm-inheritance-column-conflicts)
  References: [#8822](https://www.sqlalchemy.org/trac/ticket/8822)
- Added support custom user-defined types which extend the Python
  `enum.Enum` base class to be resolved automatically
  to SQLAlchemy [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) SQL types, when using the Annotated
  Declarative Table feature.  The feature is made possible through new
  lookup features added to the ORM type map feature, and includes support
  for changing the arguments of the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) that’s generated by
  default as well as setting up specific `enum.Enum` types within
  the map with specific arguments.
  See also
  [Using Python Enum or pep-586 Literal types in the type map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-enums)
  References: [#8859](https://www.sqlalchemy.org/trac/ticket/8859)
- Added [mapped_column.compare](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.compare) parameter to relevant ORM
  attribute constructs including [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column),
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) etc. to provide for the Python dataclasses
  `compare` parameter on `field()`, when using the
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses) feature. Pull request courtesy
  Simon Schiele.
  References: [#8905](https://www.sqlalchemy.org/trac/ticket/8905)
- Additional performance enhancements within ORM-enabled SQL statements,
  specifically targeting callcounts within the construction of ORM
  statements, using combinations of [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) with
  [union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union) and similar “compound” constructs, in addition to direct
  performance improvements to the `corresponding_column()` internal method
  that is used heavily by the ORM by constructs like [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) and
  similar.
  References: [#8796](https://www.sqlalchemy.org/trac/ticket/8796)
- Fixed issue where use of an unknown datatype within a [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
  annotation for a column-based attribute would silently fail to map the
  attribute, rather than reporting an exception; an informative exception
  message is now raised.
  References: [#8888](https://www.sqlalchemy.org/trac/ticket/8888)
- Fixed a suite of issues involving [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) use with dictionary
  types, such as `Mapped[Dict[str, str] | None]`, would not be correctly
  interpreted in Declarative ORM mappings. Support to correctly
  “de-optionalize” this type including for lookup in `type_annotation_map`
  has been fixed.
  References: [#8777](https://www.sqlalchemy.org/trac/ticket/8777)
- Fixed bug in [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses) feature where using
  plain dataclass fields with the `__allow_unmapped__` directive in a
  mapping would not create a dataclass with the correct class-level state for
  those fields, copying the raw `Field` object to the class inappropriately
  after dataclasses itself had replaced the `Field` object with the
  class-level default value.
  References: [#8880](https://www.sqlalchemy.org/trac/ticket/8880)
- Fixed regression where flushing a mapped class that’s mapped against a
  subquery, such as a direct mapping or some forms of concrete table
  inheritance, would fail if the [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults)
  parameter were used.
  References: [#8812](https://www.sqlalchemy.org/trac/ticket/8812)
- Fixed regression in 2.0.0b3 caused by [#8759](https://www.sqlalchemy.org/trac/ticket/8759) where indicating the
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) name using a qualified name such as
  `sqlalchemy.orm.Mapped` would fail to be recognized by Declarative as
  indicating the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) construct.
  References: [#8853](https://www.sqlalchemy.org/trac/ticket/8853)

### orm extensions

- Added support for the [association_proxy()](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy) extension function to
  take part within Python `dataclasses` configuration, when using
  the native dataclasses feature described at
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses).  Included are attribute-level
  arguments including [association_proxy.init](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy.params.init) and
  [association_proxy.default_factory](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy.params.default_factory).
  Documentation for association proxy has also been updated to use
  “Annotated Declarative Table” forms within examples, including type
  annotations used for `AssocationProxy` itself.
  References: [#8878](https://www.sqlalchemy.org/trac/ticket/8878)

### sql

- Added [ScalarValues](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarValues) that can be used as a column
  element allowing using [Values](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values) inside `IN` clauses
  or in conjunction with `ANY` or `ALL` collection aggregates.
  This new class is generated using the method
  [Values.scalar_values()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values.scalar_values).
  The [Values](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values) instance is now coerced to a
  [ScalarValues](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarValues) when used in a `IN` or `NOT IN`
  operation.
  References: [#6289](https://www.sqlalchemy.org/trac/ticket/6289)
- Fixed critical memory issue identified in cache key generation, where for
  very large and complex ORM statements that make use of lots of ORM aliases
  with subqueries, cache key generation could produce excessively large keys
  that were orders of magnitude bigger than the statement itself. Much thanks
  to Rollo Konig Brock for their very patient, long term help in finally
  identifying this issue.
  This change is also **backported** to: 1.4.44
  References: [#8790](https://www.sqlalchemy.org/trac/ticket/8790)
- The approach to the `numeric` pep-249 paramstyle has been rewritten, and
  is now fully supported, including by features such as “expanding IN” and
  “insertmanyvalues”. Parameter names may also be repeated in the source SQL
  construct which will be correctly represented within the numeric format
  using a single parameter. Introduced an additional numeric paramstyle
  called `numeric_dollar`, which is specifically what’s used by the asyncpg
  dialect; the paramstyle is equivalent to `numeric` except numeric
  indicators are indicated by a dollar-sign rather than a colon. The asyncpg
  dialect now uses `numeric_dollar` paramstyle directly, rather than
  compiling to `format` style first.
  The `numeric` and `numeric_dollar` paramstyles assume that the target
  backend is capable of receiving the numeric parameters in any order,
  and will match the given parameter values to the statement based on
  matching their position (1-based) to the numeric indicator.  This is the
  normal behavior of “numeric” paramstyles, although it was observed that
  the SQLite DBAPI implements a not-used “numeric” style that does not honor
  parameter ordering.
  References: [#8849](https://www.sqlalchemy.org/trac/ticket/8849)
- Adjusted the rendering of `RETURNING`, in particular when using
  [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), such that it now renders columns using the same logic
  as that of the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct to generate labels, which will
  include disambiguating labels, as well as that a SQL function surrounding a
  named column will be labeled using the column name itself. This establishes
  better cross-compatibility when selecting rows from either [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
  constructs or from DML statements that use [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning). A
  narrower scale change was also made for the 1.4 series that adjusted the
  function label issue only.
  References: [#8770](https://www.sqlalchemy.org/trac/ticket/8770)

### schema

- Stricter rules are in place for appending of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects to
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, both moving some previous deprecation warnings to
  exceptions, and preventing some previous scenarios that would cause
  duplicate columns to appear in tables, when
  [Table.extend_existing](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.extend_existing) were set to `True`, for both
  programmatic [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construction as well as during reflection
  operations.
  See [Stricter rules for replacement of Columns in Table objects with same-names, keys](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-8925) for a rundown of these changes.
  See also
  [Stricter rules for replacement of Columns in Table objects with same-names, keys](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-8925)
  References: [#8925](https://www.sqlalchemy.org/trac/ticket/8925)

### typing

- Added a new type [SQLColumnExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.SQLColumnExpression) which may be indicated in
  user code to represent any SQL column oriented expression, including both
  those based on [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) as well as on ORM
  [QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute). This type is a real class, not an alias, so
  can also be used as the foundation for other objects.  An additional
  ORM-specific subclass [SQLORMExpression](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.SQLORMExpression) is also included.
  References: [#8847](https://www.sqlalchemy.org/trac/ticket/8847)
- Adjusted internal use of the Python `enum.IntFlag` class which changed
  its behavioral contract in Python 3.11. This was not causing runtime
  failures however caused typing runs to fail under Python 3.11.
  References: [#8783](https://www.sqlalchemy.org/trac/ticket/8783)
- The `sqlalchemy.ext.mutable` extension and `sqlalchemy.ext.automap`
  extensions are now fully pep-484 typed. Huge thanks to Gleb Kisenkov for
  their efforts on this.
  References: [#6810](https://www.sqlalchemy.org/trac/ticket/6810), [#8667](https://www.sqlalchemy.org/trac/ticket/8667)
- Corrected typing support for the [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary)
  argument which may also accept a callable (lambda) that returns a
  [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).
- Improved the typing for [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) and
  [async_sessionmaker](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.async_sessionmaker), so that the default type of their return value
  will be [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) or [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession), without the need to
  type this explicitly. Previously, Mypy would not automatically infer these
  return types from its generic base.
  As part of this change, arguments for [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
  [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession), [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) and
  [async_sessionmaker](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.async_sessionmaker) beyond the initial “bind” argument have been
  made keyword-only, which includes parameters that have always been
  documented as keyword arguments, such as [Session.autoflush](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.autoflush),
  [Session.class_](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.class_), etc.
  Pull request courtesy Sam Bull.
  References: [#8842](https://www.sqlalchemy.org/trac/ticket/8842)
- Fixed issue where passing a callbale function returning an iterable
  of column elements to [relationship.order_by](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.order_by) was
  flagged as an error in type checkers.
  References: [#8776](https://www.sqlalchemy.org/trac/ticket/8776)

### postgresql

- Complementing [#8690](https://www.sqlalchemy.org/trac/ticket/8690), new comparison methods such as
  [Range.adjacent_to()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range.adjacent_to),
  [Range.difference()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range.difference), [Range.union()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range.union),
  etc., were added to the PG-specific range objects, bringing them in par
  with the standard operators implemented by the underlying
  [AbstractRange.comparator_factory](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.AbstractRange.comparator_factory).
  In addition, the `__bool__()` method of the class has been corrected to
  be consistent with the common Python containers behavior as well as how
  other popular PostgreSQL drivers do: it now tells whether the range
  instance is *not* empty, rather than the other way around.
  Pull request courtesy Lele Gaifax.
  References: [#8765](https://www.sqlalchemy.org/trac/ticket/8765)
- Changed the paramstyle used by asyncpg from `format` to
  `numeric_dollar`. This has two main benefits since it does not require
  additional processing of the statement and allows for duplicate parameters
  to be present in the statements.
  References: [#8926](https://www.sqlalchemy.org/trac/ticket/8926)
- For the PostgreSQL and SQL Server dialects only, adjusted the compiler so
  that when rendering column expressions in the RETURNING clause, the “non
  anon” label that’s used in SELECT statements is suggested for SQL
  expression elements that generate a label; the primary example is a SQL
  function that may be emitting as part of the column’s type, where the label
  name should match the column’s name by default. This restores a not-well
  defined behavior that had changed in version 1.4.21 due to [#6718](https://www.sqlalchemy.org/trac/ticket/6718),
  [#6710](https://www.sqlalchemy.org/trac/ticket/6710). The Oracle dialect has a different RETURNING implementation
  and was not affected by this issue. Version 2.0 features an across the
  board change for its widely expanded support of RETURNING on other
  backends.
  This change is also **backported** to: 1.4.44
  References: [#8770](https://www.sqlalchemy.org/trac/ticket/8770)
- Added additional type-detection for the new PostgreSQL
  [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range) type, where previous cases that allowed the
  psycopg2-native range objects to be received directly by the DBAPI without
  SQLAlchemy intercepting them stopped working, as we now have our own value
  object. The [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range) object has been enhanced such that
  SQLAlchemy Core detects it in otherwise ambiguous situations (such as
  comparison to dates) and applies appropriate bind handlers. Pull request
  courtesy Lele Gaifax.
  References: [#8884](https://www.sqlalchemy.org/trac/ticket/8884)

### mssql

- Fixed regression caused by the combination of [#8177](https://www.sqlalchemy.org/trac/ticket/8177), re-enable
  setinputsizes for SQL server unless fast_executemany + DBAPI executemany is
  used for a statement, along with [#6047](https://www.sqlalchemy.org/trac/ticket/6047), implement
  “insertmanyvalues”, which bypasses DBAPI executemany in place of a custom
  DBAPI execute for INSERT statements. setinputsizes would incorrectly not be
  used for a multiple parameter-set INSERT statement that used
  “insertmanyvalues” if fast_executemany were turned on, as the check would
  incorrectly assume this is a DBAPI executemany call.  The “regression”
  would then be that the “insertmanyvalues” statement format is apparently
  slightly more sensitive to multiple rows that don’t use the same types
  for each row, so in such a case setinputsizes is especially needed.
  The fix repairs the fast_executemany check so that it only disables
  setinputsizes if true DBAPI executemany is to be used.
  References: [#8917](https://www.sqlalchemy.org/trac/ticket/8917)

### oracle

- Continued fixes for Oracle fix [#8708](https://www.sqlalchemy.org/trac/ticket/8708) released in 1.4.43 where
  bound parameter names that start with underscores, which are disallowed by
  Oracle, were still not being properly escaped in all circumstances.
  This change is also **backported** to: 1.4.45
  References: [#8708](https://www.sqlalchemy.org/trac/ticket/8708)

### tests

- Fixed issue where the `--disable-asyncio` parameter to the test suite
  would fail to not actually run greenlet tests and would also not prevent
  the suite from using a “wrapping” greenlet for the whole suite. This
  parameter now ensures that no greenlet or asyncio use will occur within the
  entire run when set.
  This change is also **backported** to: 1.4.44
  References: [#8793](https://www.sqlalchemy.org/trac/ticket/8793)

## 2.0.0b3

Released: November 4, 2022

### orm

- Fixed issue in joined eager loading where an assertion fail would occur
  with a particular combination of outer/inner joined eager loads, when
  eager loading across three mappers where the middle mapper was
  an inherited subclass mapper.
  This change is also **backported** to: 1.4.43
  References: [#8738](https://www.sqlalchemy.org/trac/ticket/8738)
- Fixed bug involving [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) constructs, where combinations of
  [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) with [Select.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join), as well as when
  using [Select.join_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.join_from), would cause the
  [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) feature as well as the IN criteria needed
  for single-table inheritance queries to not render, in cases where the
  columns clause of the query did not explicitly include the left-hand side
  entity of the JOIN. The correct entity is now transferred to the
  [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) object that’s generated internally, so that the criteria
  against the left side entity is correctly added.
  This change is also **backported** to: 1.4.43
  References: [#8721](https://www.sqlalchemy.org/trac/ticket/8721)
- An informative exception is now raised when the
  [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) option is used as a loader option added
  to a specific “loader path”, such as when using it within
  [Load.options()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load.options). This use is not supported as
  [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria) is only intended to be used as a top
  level loader option. Previously, an internal error would be generated.
  This change is also **backported** to: 1.4.43
  References: [#8711](https://www.sqlalchemy.org/trac/ticket/8711)
- Improved “dictionary mode” for [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) so that synonym
  names which refer to primary key attribute names may be indicated in the
  named dictionary.
  This change is also **backported** to: 1.4.43
  References: [#8753](https://www.sqlalchemy.org/trac/ticket/8753)
- Fixed issue where “selectin_polymorphic” loading for inheritance mappers
  would not function correctly if the [Mapper.polymorphic_on](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_on)
  parameter referred to a SQL expression that was not directly mapped on the
  class.
  This change is also **backported** to: 1.4.43
  References: [#8704](https://www.sqlalchemy.org/trac/ticket/8704)
- Fixed issue where the underlying DBAPI cursor would not be closed when
  using the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object as an iterator, if a user-defined exception
  case were raised within the iteration process, thereby causing the iterator
  to be closed by the Python interpreter.  When using
  [Query.yield_per()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.yield_per) to create server-side cursors, this would lead
  to the usual MySQL-related issues with server side cursors out of sync,
  and without direct access to the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object, end-user code
  could not access the cursor in order to close it.
  To resolve, a catch for `GeneratorExit` is applied within the iterator
  method, which will close the result object in those cases when the
  iterator were interrupted, and by definition will be closed by the
  Python interpreter.
  As part of this change as implemented for the 1.4 series, ensured that
  `.close()` methods are available on all [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) implementations
  including [ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult), [MappingResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.MappingResult).  The 2.0
  version of this change also includes new context manager patterns for use
  with [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) classes.
  This change is also **backported** to: 1.4.43
  References: [#8710](https://www.sqlalchemy.org/trac/ticket/8710)

### orm declarative

- Added support in ORM declarative annotations for class names specified for
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), as well as the name of the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
  symbol itself, to be different names than their direct class name, to
  support scenarios such as where [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) is imported as
  `from sqlalchemy.orm import Mapped as M`, or where related class names
  are imported with an alternate name in a similar fashion. Additionally, a
  target class name given as the lead argument for [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
  will always supersede the name given in the left hand annotation, so that
  otherwise un-importable names that also don’t match the class name can
  still be used in annotations.
  References: [#8759](https://www.sqlalchemy.org/trac/ticket/8759)
- Improved support for legacy 1.4 mappings that use annotations which don’t
  include `Mapped[]`, by ensuring the `__allow_unmapped__` attribute can
  be used to allow such legacy annotations to pass through Annotated
  Declarative without raising an error and without being interpreted in an
  ORM runtime context. Additionally improved the error message generated when
  this condition is detected, and added more documentation for how this
  situation should be handled. Unfortunately the 1.4 WARN_SQLALCHEMY_20
  migration warning cannot detect this particular configurational issue at
  runtime with its current architecture.
  References: [#8692](https://www.sqlalchemy.org/trac/ticket/8692)
- Changed a fundamental configuration behavior of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper), where
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that are explicitly present in the
  [Mapper.properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.properties) dictionary, either directly or enclosed
  within a mapper property object, will now be mapped within the order of how
  they appear within the mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) (or other selectable) itself
  (assuming they are in fact part of that table’s list of columns), thereby
  maintaining the same order of columns in the mapped selectable as is
  instrumented on the mapped class, as well as what renders in an ORM SELECT
  statement for that mapper. Previously (where “previously” means since
  version 0.0.1), [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects in the
  [Mapper.properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.properties) dictionary would always be mapped first,
  ahead of when the other columns in the mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) would be
  mapped, causing a discrepancy in the order in which the mapper would
  assign attributes to the mapped class as well as the order in which they
  would render in statements.
  The change most prominently takes place in the way that Declarative
  assigns declared columns to the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper), specifically how
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) (or [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column)) objects are handled
  when they have a DDL name that is explicitly different from the mapped
  attribute name, as well as when constructs such as [deferred()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.deferred)
  etc. are used.   The new behavior will see the column ordering within
  the mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) being the same order in which the attributes
  are mapped onto the class, assigned within the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) itself,
  and rendered in ORM statements such as SELECT statements, independent
  of how the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) was configured against the
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper).
  References: [#8705](https://www.sqlalchemy.org/trac/ticket/8705)
- Fixed issue in new dataclass mapping feature where a column declared on the
  declarative base / abstract base / mixin would leak into the constructor
  for an inheriting subclass under some circumstances.
  References: [#8718](https://www.sqlalchemy.org/trac/ticket/8718)
- Fixed issues within the declarative typing resolver (i.e. which resolves
  `ForwardRef` objects) where types that were declared for columns in one
  particular source file would raise `NameError` when the ultimate mapped
  class were in another source file.  The types are now resolved in terms
  of the module for each class in which the types are used.
  References: [#8742](https://www.sqlalchemy.org/trac/ticket/8742)

### engine

- To better support the use case of iterating [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) and
  [AsyncResult](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncResult) objects where user-defined exceptions may interrupt
  the iteration, both objects as well as variants such as
  [ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult), [MappingResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.MappingResult),
  [AsyncScalarResult](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncScalarResult), [AsyncMappingResult](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncMappingResult) now support
  context manager usage, where the result will be closed at the end of
  the context manager block.
  In addition, ensured that all the above
  mentioned [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) objects include a [Result.close()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.close) method
  as well as [Result.closed](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.closed) accessors, including
  [ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult) and [MappingResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.MappingResult) which previously did
  not have a `.close()` method.
  See also
  [Context Manager Support for Result, AsyncResult](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-8710)
  References: [#8710](https://www.sqlalchemy.org/trac/ticket/8710)
- Added new parameter [PoolEvents.reset.reset_state](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset.params.reset_state) parameter to
  the [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event, with deprecation logic in place that
  will continue to accept event hooks using the previous set of arguments.
  This indicates various state information about how the reset is taking
  place and is used to allow custom reset schemes to take place with full
  context given.
  Within this change a fix that’s also backported to 1.4 is included which
  re-enables the [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event to continue to take place
  under all circumstances, including when [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) has already
  “reset” the connection.
  The two changes together allow custom reset schemes to be implemented using
  the [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event, instead of the
  [PoolEvents.checkin()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.checkin) event (which continues to function as it always
  has).
  References: [#8717](https://www.sqlalchemy.org/trac/ticket/8717)
- Fixed issue where the [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event hook would not be be
  called in all cases when a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) were closed and was
  in the process of returning its DBAPI connection to the connection pool.
  The scenario was when the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) had already emitted
  `.rollback()` on its DBAPI connection within the process of returning
  the connection to the pool, where it would then instruct the connection
  pool to forego doing its own “reset” to save on the additional method
  call.  However, this prevented custom pool reset schemes from being
  used within this hook, as such hooks by definition are doing more than
  just calling `.rollback()`, and need to be invoked under all
  circumstances.  This was a regression that appeared in version 1.4.
  For version 1.4, the [PoolEvents.checkin()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.checkin) remains viable as an
  alternate event hook to use for custom “reset” implementations. Version 2.0
  will feature an improved version of [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) which is
  called for additional scenarios such as termination of asyncio connections,
  and is also passed contextual information about the reset, to allow for
  “custom connection reset” schemes which can respond to different reset
  scenarios in different ways.
  This change is also **backported** to: 1.4.43
  References: [#8717](https://www.sqlalchemy.org/trac/ticket/8717)

### sql

- Fixed issue which prevented the [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column) construct from
  working properly within the context of a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct as well
  as other potential places where “anonymized labels” might be generated, if
  the literal expression contained characters which could interfere with
  format strings, such as open parenthesis, due to an implementation detail
  of the “anonymous label” structure.
  This change is also **backported** to: 1.4.43
  References: [#8724](https://www.sqlalchemy.org/trac/ticket/8724)

### typing

- Corrected various typing issues within the engine and async engine
  packages.

### postgresql

- Added new methods [Range.contains()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range.contains) and
  [Range.contained_by()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range.contained_by) to the new [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range) data
  object, which mirror the behavior of the PostgreSQL `@>` and `<@`
  operators, as well as the
  [comparator_factory.contains()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.AbstractRange.comparator_factory.contains) and
  [comparator_factory.contained_by()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.AbstractRange.comparator_factory.contained_by) SQL
  operator methods. Pull request courtesy Lele Gaifax.
  References: [#8706](https://www.sqlalchemy.org/trac/ticket/8706)
- Refined the new approach to range objects described at [New RANGE / MULTIRANGE support and changes for PostgreSQL backends](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7156)
  to accommodate driver-specific range and multirange objects, to better
  accommodate both legacy code as well as when passing results from raw SQL
  result sets back into new range or multirange expressions.
  References: [#8690](https://www.sqlalchemy.org/trac/ticket/8690)

### mssql

- Fixed issue with [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table), which when used against a
  temporary table with the SQL Server dialect would fail on some Azure
  variants, due to an unnecessary information schema query that is not
  supported on those server versions. Pull request courtesy Mike Barry.
  This change is also **backported** to: 1.4.43
  References: [#8714](https://www.sqlalchemy.org/trac/ticket/8714)
- Fixed issue with [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table), which when used against a
  view with the SQL Server dialect would erroneously return `False`, due to
  a regression in the 1.4 series which removed support for this on SQL
  Server. The issue is not present in the 2.0 series which uses a different
  reflection architecture. Test support is added to ensure `has_table()`
  remains working per spec re: views.
  This change is also **backported** to: 1.4.43
  References: [#8700](https://www.sqlalchemy.org/trac/ticket/8700)

### oracle

- Fixed issue where bound parameter names, including those automatically
  derived from similarly-named database columns, which contained characters
  that normally require quoting with Oracle would not be escaped when using
  “expanding parameters” with the Oracle dialect, causing execution errors.
  The usual “quoting” for bound parameters used by the Oracle dialect is not
  used with the “expanding parameters” architecture, so escaping for a large
  range of characters is used instead, now using a list of characters/escapes
  that are specific to Oracle.
  This change is also **backported** to: 1.4.43
  References: [#8708](https://www.sqlalchemy.org/trac/ticket/8708)
- Fixed issue where the `nls_session_parameters` view queried on first
  connect in order to get the default decimal point character may not be
  available depending on Oracle connection modes, and would therefore raise
  an error.  The approach to detecting decimal char has been simplified to
  test a decimal value directly, instead of reading system views, which
  works on any backend / driver.
  This change is also **backported** to: 1.4.43
  References: [#8744](https://www.sqlalchemy.org/trac/ticket/8744)

## 2.0.0b2

Released: October 20, 2022

### orm

- Removed the warning that emits when using ORM-enabled update/delete
  regarding evaluation of columns by name, first added in [#4073](https://www.sqlalchemy.org/trac/ticket/4073);
  this warning actually covers up a scenario that otherwise could populate
  the wrong Python value for an ORM mapped attribute depending on what the
  actual column is, so this deprecated case is removed. In 2.0, ORM enabled
  update/delete uses “auto” for “synchronize_session”, which should do the
  right thing automatically for any given UPDATE expression.
  References: [#8656](https://www.sqlalchemy.org/trac/ticket/8656)

### orm declarative

- Added support for mapped classes that are also `Generic` subclasses,
  to be specified as a `GenericAlias` object (e.g. `MyClass[str]`)
  within statements and calls to [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect).
  References: [#8665](https://www.sqlalchemy.org/trac/ticket/8665)
- Improved the [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) class so that when combined with
  other mixins like [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass), the order of the classes may
  be in either order.
  References: [#8665](https://www.sqlalchemy.org/trac/ticket/8665)
- Fixed bug in new ORM typed declarative mappings where the ability
  to use `Optional[MyClass]` or similar forms such as `MyClass | None`
  in the type annotation for a many-to-one relationship was not implemented,
  leading to errors.   Documentation has also been added for this use
  case to the relationship configuration documentation.
  References: [#8668](https://www.sqlalchemy.org/trac/ticket/8668)
- Fixed issue with new dataclass mapping feature where arguments passed to
  the dataclasses API could sometimes be mis-ordered when dealing with mixins
  that override [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) declarations, leading to
  initializer problems.
  References: [#8688](https://www.sqlalchemy.org/trac/ticket/8688)

### sql

- Fixed bug in new “insertmanyvalues” feature where INSERT that included a
  subquery with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) inside of it would fail to render
  correctly in “insertmanyvalues” format. This affected psycopg2 most
  directly as “insertmanyvalues” is used unconditionally with this driver.
  References: [#8639](https://www.sqlalchemy.org/trac/ticket/8639)

### typing

- Fixed typing issue where pylance strict mode would report “instance
  variable overrides class variable” when using a method to define
  `__tablename__`, `__mapper_args__` or `__table_args__`.
  References: [#8645](https://www.sqlalchemy.org/trac/ticket/8645)
- Fixed typing issue where pylance strict mode would report “partially
  unknown” datatype for the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct.
  References: [#8644](https://www.sqlalchemy.org/trac/ticket/8644)

### mssql

- Fixed regression caused by SQL Server pyodbc change [#8177](https://www.sqlalchemy.org/trac/ticket/8177) where we
  now use `setinputsizes()` by default; for VARCHAR, this fails if the
  character size is greater than 4000 (or 2000, depending on data) characters
  as the incoming datatype is NVARCHAR, which has a limit of 4000 characters,
  despite the fact that VARCHAR can handle unlimited characters. Additional
  pyodbc-specific typing information is now passed to `setinputsizes()`
  when the datatype’s size is > 2000 characters. The change is also applied
  to the [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type which was also impacted by this issue for large
  JSON serializations.
  References: [#8661](https://www.sqlalchemy.org/trac/ticket/8661)
- The [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) construct restores itself to the DDL behavior it
  had prior to the 1.4 series, where creating a [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) with
  no additional arguments will emit a simple `CREATE SEQUENCE` instruction
  **without** any additional parameters for “start value”.   For most backends,
  this is how things worked previously in any case; **however**, for
  MS SQL Server, the default value on this database is
  `-2**63`; to prevent this generally impractical default
  from taking effect on SQL Server, the [Sequence.start](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.start) parameter
  should be provided.   As usage of [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) is unusual
  for SQL Server which for many years has standardized on `IDENTITY`,
  it is hoped that this change has minimal impact.
  See also
  [The Sequence construct reverts to not having any explicit default “start” value; impacts MS SQL Server](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7211)
  References: [#7211](https://www.sqlalchemy.org/trac/ticket/7211)

## 2.0.0b1

Released: October 13, 2022

### general

- Migrated the codebase to remove all pre-2.0 behaviors and architectures
  that were previously noted as deprecated for removal in 2.0, including,
  but not limited to:
  - removal of all Python 2 code, minimum version is now Python 3.7
  - [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) and [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) now use the
    new 2.0 style of working, which includes “autobegin”, library level
    autocommit removed, subtransactions and “branched” connections
    removed
  - Result objects use 2.0-style behaviors; [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) is fully
    a named tuple without “mapping” behavior, use [RowMapping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.RowMapping)
    for “mapping” behavior
  - All Unicode encoding/decoding architecture has been removed from
    SQLAlchemy.  All modern DBAPI implementations support Unicode
    transparently thanks to Python 3, so the `convert_unicode` feature
    as well as related mechanisms to look for bytestrings in
    DBAPI `cursor.description` etc. have been removed.
  - The `.bind` attribute and parameter from [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData),
    [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), and from all DDL/DML/DQL elements that previously could
    refer to a “bound engine”
  - The standalone `sqlalchemy.orm.mapper()` function is removed; all
    classical mapping should be done through the
    [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively) method of [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry).
  - The [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) method no longer accepts strings for
    relationship names; the long-documented approach of using
    `Class.attrname` for join targets is now standard.
  - [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) no longer accepts the “aliased” and
    “from_joinpoint” arguments
  - [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) no longer accepts chains of multiple join
    targets in one method call.
  - `Query.from_self()`, `Query.select_entity_from()` and
    `Query.with_polymorphic()` are removed.
  - The [relationship.cascade_backrefs](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade_backrefs) parameter must now
    remain at its new default of `False`; the `save-update` cascade
    no longer cascades along a backref.
  - the [Session.future](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.future) parameter must always be set to
    `True`.  2.0-style transactional patterns for [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
    are now always in effect.
  - Loader options no longer accept strings for attribute names.  The
    long-documented approach of using `Class.attrname` for loader option
    targets is now standard.
  - Legacy forms of [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) removed, including
    `select([cols])`, the “whereclause” and keyword parameters of
    `some_table.select()`.
  - Legacy “in-place mutator” methods on [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) such as
    `append_whereclause()`, `append_order_by()` etc are removed.
  - Removed the very old “dbapi_proxy” module, which in very early
    SQLAlchemy releases was used to provide a transparent connection pool
    over a raw DBAPI connection.
  References: [#7257](https://www.sqlalchemy.org/trac/ticket/7257)
- The [Query.instances()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.instances) method is deprecated.  The behavioral
  contract of this method, which is that it can iterate objects through
  arbitrary result sets, is long obsolete and no longer tested.
  Arbitrary statements can return objects by using constructs such
  as :meth`.Select.from_statement` or [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased).

### platform

- The SQLAlchemy C extensions have been replaced with all new implementations
  written in Cython.  Like the C extensions before, pre-built wheel files
  for a wide range of platforms are available on pypi so that building
  is not an issue for common platforms.  For custom builds, `python setup.py build_ext`
  works as before, needing only the additional Cython install.  `pyproject.toml`
  is also part of the source now which will establish the proper build dependencies
  when using pip.
  See also
  [C Extensions now ported to Cython](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7256)
  References: [#7256](https://www.sqlalchemy.org/trac/ticket/7256)
- SQLAlchemy’s source build and installation now includes a `pyproject.toml` file
  for full [PEP 517](https://peps.python.org/pep-0517/) support.
  See also
  [Installation is now fully pep-517 enabled](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7311)
  References: [#7311](https://www.sqlalchemy.org/trac/ticket/7311)

### orm

- Added new feature to all included dialects that support RETURNING
  called “insertmanyvalues”.  This is a generalization of the
  “fast executemany” feature first introduced for the psycopg2 driver
  in 1.4 at [ORM Batch inserts with psycopg2 now batch statements with RETURNING in most cases](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-5263), which allows the ORM to batch INSERT
  statements into a much more efficient SQL structure while still being
  able to fetch newly generated primary key and SQL default values
  using RETURNING.
  The feature now applies to the many dialects that support RETURNING along
  with multiple VALUES constructs for INSERT, including all PostgreSQL
  drivers, SQLite, MariaDB, MS SQL Server. Separately, the Oracle dialect
  also gains the same capability using native cx_Oracle or OracleDB features.
  References: [#6047](https://www.sqlalchemy.org/trac/ticket/6047)
- Added new parameter [AttributeEvents.include_key](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.params.include_key), which
  will include the dictionary or list key for operations such as
  `__setitem__()` (e.g. `obj[key] = value`) and `__delitem__()` (e.g.
  `del obj[key]`), using a new keyword parameter “key” or “keys”, depending
  on event, e.g. [AttributeEvents.append.key](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.append.params.key),
  [AttributeEvents.bulk_replace.keys](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.bulk_replace.params.keys). This allows event
  handlers to take into account the key that was passed to the operation and
  is of particular importance for dictionary operations working with
  [MappedCollection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.MappedCollection).
  References: [#8375](https://www.sqlalchemy.org/trac/ticket/8375)
- Added new parameter [Operators.op.python_impl](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op.params.python_impl), available
  from [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) and also when using the
  `custom_op` constructor directly, which allows an
  in-Python evaluation function to be provided along with the custom SQL
  operator. This evaluation function becomes the implementation used when the
  operator object is used given plain Python objects as operands on both
  sides, and in particular is compatible with the
  `synchronize_session='evaluate'` option used with
  [ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete).
  References: [#3162](https://www.sqlalchemy.org/trac/ticket/3162)
- The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) (and by extension [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession)) now has
  new state-tracking functionality that will proactively trap any unexpected
  state changes which occur as a particular transactional method proceeds.
  This is to allow situations where the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is being used
  in a thread-unsafe manner, where event hooks or similar may be calling
  unexpected methods within operations, as well as potentially under other
  concurrency situations such as asyncio or gevent to raise an informative
  message when the illegal access first occurs, rather than passing silently
  leading to secondary failures due to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) being in an
  invalid state.
  See also
  [Session raises proactively when illegal concurrent or reentrant access is detected](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7433)
  References: [#7433](https://www.sqlalchemy.org/trac/ticket/7433)
- The [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) mapping construct now supports automatic
  resolution of values when used with a Python `dataclass`; the
  `__composite_values__()` method no longer needs to be implemented as this
  method is derived from inspection of the dataclass.
  Additionally, classes mapped by [composite](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) now support
  ordering comparison operations, e.g. `<`, `>=`, etc.
  See the new documentation at [Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html#mapper-composite) for examples.
- Added very experimental feature to the [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) and
  [immediateload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.immediateload) loader options called
  [selectinload.recursion_depth](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload.params.recursion_depth) /
  [immediateload.recursion_depth](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.immediateload.params.recursion_depth) , which allows a single
  loader option to automatically recurse into self-referential relationships.
  Is set to an integer indicating depth, and may also be set to -1 to
  indicate to continue loading until no more levels deep are found.
  Major internal changes to [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) and
  [immediateload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.immediateload) allow this feature to work while continuing
  to make correct use of the compilation cache, as well as not using
  arbitrary recursion, so any level of depth is supported (though would
  emit that many queries).  This may be useful for
  self-referential structures that must be loaded fully eagerly, such as when
  using asyncio.
  A warning is also emitted when loader options are connected together with
  arbitrary lengths (that is, without using the new `recursion_depth`
  option) when excessive recursion depth is detected in related object
  loading. This operation continues to use huge amounts of memory and
  performs extremely poorly; the cache is disabled when this condition is
  detected to protect the cache from being flooded with arbitrary statements.
  References: [#8126](https://www.sqlalchemy.org/trac/ticket/8126)
- Added new parameter [Session.autobegin](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.autobegin), which when set to
  `False` will prevent the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) from beginning a
  transaction implicitly. The [Session.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin) method must be
  called explicitly first in order to proceed with operations, otherwise an
  error is raised whenever any operation would otherwise have begun
  automatically. This option can be used to create a “safe”
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) that won’t implicitly start new transactions.
  As part of this change, also added a new status variable
  [origin](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction.origin) which may be useful for event
  handling code to be aware of the origin of a particular
  [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction).
  References: [#6928](https://www.sqlalchemy.org/trac/ticket/6928)
- Declarative mixins which use [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that contain
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) references no longer need to use
  [declared_attr()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) to achieve this mapping; the
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) object is copied along with the
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) itself when the column is applied to the declared
  mapping.
- Added [load_only.raiseload](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only.params.raiseload) parameter to the
  [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) loader option, so that the unloaded attributes may
  have “raise” behavior rather than lazy loading. Previously there wasn’t
  really a way to do this with the [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) option directly.
- To better accommodate explicit typing, the names of some ORM constructs
  that are typically constructed internally, but nonetheless are sometimes
  visible in messaging as well as typing, have been changed to more succinct
  names which also match the name of their constructing function (with
  different casing), in all cases maintaining aliases to the old names for
  the foreseeable future:
  - [RelationshipProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.RelationshipProperty) becomes an alias for the primary name
    [Relationship](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Relationship), which is constructed as always from the
    [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) function
  - [SynonymProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.SynonymProperty) becomes an alias for the primary name
    [Synonym](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Synonym), constructed as always from the
    [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym) function
  - [CompositeProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.CompositeProperty) becomes an alias for the primary name
    [Composite](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Composite), constructed as always from the
    [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) function
- For consistency with the prominent ORM concept [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped), the
  names of the dictionary-oriented collections,
  [attribute_mapped_collection()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_mapped_collection),
  [column_mapped_collection()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_mapped_collection), and [MappedCollection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.MappedCollection),
  are changed to [attribute_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict),
  [column_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_keyed_dict) and [KeyFuncDict](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.KeyFuncDict), using the
  phrase “dict” to minimize any confusion against the term “mapped”. The old
  names will remain indefinitely with no schedule for removal.
  References: [#8608](https://www.sqlalchemy.org/trac/ticket/8608)
- All [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) objects will now consistently raise
  [ResourceClosedError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ResourceClosedError) if they are used after a hard close,
  which includes the “hard close” that occurs after calling “single row or
  value” methods like [Result.first()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.first) and
  [Result.scalar()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalar). This was already the behavior of the most
  common class of result objects returned for Core statement executions, i.e.
  those based on [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult), so this behavior is not new.
  However, the change has been extended to properly accommodate for the ORM
  “filtering” result objects returned when using 2.0 style ORM queries,
  which would previously behave in “soft closed” style of returning empty
  results, or wouldn’t actually “soft close” at all and would continue
  yielding from the underlying cursor.
  As part of this change, also added [Result.close()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.close) to the base
  [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) class and implemented it for the filtered result
  implementations that are used by the ORM, so that it is possible to call
  the [CursorResult.close()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.close) method on the underlying
  [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) when the `yield_per` execution option
  is in use to close a server side cursor before remaining ORM results have
  been fetched. This was again already available for Core result sets but the
  change makes it available for 2.0 style ORM results as well.
  This change is also **backported** to: 1.4.27
  References: [#7274](https://www.sqlalchemy.org/trac/ticket/7274)
- Fixed issue where the [registry.map_declaratively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_declaratively) method
  would return an internal “mapper config” object and not the
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object as stated in the API documentation.
- Fixed performance regression which appeared at least in version 1.3 if not
  earlier (sometime after 1.0) where the loading of deferred columns, those
  explicitly mapped with [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) as opposed to non-deferred
  columns that were expired, from a joined inheritance subclass would not use
  the “optimized” query which only queried the immediate table that contains
  the unloaded columns, instead running a full ORM query which would emit a
  JOIN for all base tables, which is not necessary when only loading columns
  from the subclass.
  References: [#7463](https://www.sqlalchemy.org/trac/ticket/7463)
- The internals for the [Load](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load) object and related loader strategy
  patterns have been mostly rewritten, to take advantage of the fact that
  only attribute-bound paths, not strings, are now supported. The rewrite
  hopes to make it more straightforward to address new use cases and subtle
  issues within the loader strategy system going forward.
  References: [#6986](https://www.sqlalchemy.org/trac/ticket/6986)
- Made an improvement to the “deferred” / “load_only” set of strategy options
  where if a certain object is loaded from two different logical paths within
  one query, attributes that have been configured by at least one of the
  options to be populated will be populated in all cases, even if other load
  paths for that same object did not set this option. previously, it was
  based on randomness as to which “path” addressed the object first.
  References: [#8166](https://www.sqlalchemy.org/trac/ticket/8166)
- Fixed issue in ORM enabled UPDATE when the statement is created against a
  joined-inheritance subclass, updating only local table columns, where the
  “fetch” synchronization strategy would not render the correct RETURNING
  clause for databases that use RETURNING for fetch synchronization.
  Also adjusts the strategy used for RETURNING in UPDATE FROM and
  DELETE FROM statements.
  References: [#8344](https://www.sqlalchemy.org/trac/ticket/8344)
- Removed the unused `**kw` arguments from
  [begin](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.begin) and
  [begin_nested](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.begin_nested). These kw aren’t used and
  appear to have been added to the API in error.
  References: [#7703](https://www.sqlalchemy.org/trac/ticket/7703)
- Changed the attribute access method used by
  [attribute_mapped_collection()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_mapped_collection) and
  [column_mapped_collection()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_mapped_collection) (now called
  [attribute_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict) and [column_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_keyed_dict)) ,
  used when populating the dictionary, to assert that the data value on
  the object to be used as the dictionary key is actually present, and is
  not instead using “None” due to the attribute never being actually
  assigned. This is used to prevent a mis-population of None for a key
  when assigning via a backref where the “key” attribute on the object is
  not yet assigned.
  As the failure mode here is a transitory condition that is not typically
  persisted to the database, and is easy to produce via the constructor of
  the class based on the order in which parameters are assigned, it is very
  possible that many applications include this behavior already which is
  silently passed over. To accommodate for applications where this error is
  now raised, a new parameter
  [attribute_keyed_dict.ignore_unpopulated_attribute](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict.params.ignore_unpopulated_attribute)
  is also added to both [attribute_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict) and
  [column_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_keyed_dict) that instead causes the erroneous
  backref assignment to be skipped.
  References: [#8372](https://www.sqlalchemy.org/trac/ticket/8372)
- Added new parameter [AbstractConcreteBase.strict_attrs](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase.params.strict_attrs) to the
  [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) declarative mixin class. The effect of this
  parameter is that the scope of attributes on subclasses is correctly
  limited to the subclass in which each attribute is declared, rather than
  the previous behavior where all attributes of the entire hierarchy are
  applied to the base “abstract” class. This produces a cleaner, more correct
  mapping where subclasses no longer have non-useful attributes on them which
  are only relevant to sibling classes. The default for this parameter is
  False, which leaves the previous behavior unchanged; this is to support
  existing code that makes explicit use of these attributes in queries.
  To migrate to the newer approach, apply explicit attributes to the abstract
  base class as needed.
  References: [#8403](https://www.sqlalchemy.org/trac/ticket/8403)
- The behavior of [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) regarding primary key and “polymorphic
  discriminator” columns is revised such that these columns are no longer
  deferrable, either explicitly or when using a wildcard such as
  `defer('*')`. Previously, a wildcard deferral would not load
  PK/polymorphic columns which led to errors in all cases, as the ORM relies
  upon these columns to produce object identities. The behavior of explicit
  deferral of primary key columns is unchanged as these deferrals already
  were implicitly ignored.
  References: [#7495](https://www.sqlalchemy.org/trac/ticket/7495)
- Fixed bug in the behavior of the [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults)
  parameter such that client-side SQL default or onupdate expressions in the
  table definition alone will trigger a fetch operation using RETURNING or
  SELECT when the ORM emits an INSERT or UPDATE for the row. Previously, only
  server side defaults established as part of table DDL and/or server-side
  onupdate expressions would trigger this fetch, even though client-side SQL
  expressions would be included when the fetch was rendered.
  References: [#7438](https://www.sqlalchemy.org/trac/ticket/7438)

### engine

- The [DialectEvents.handle_error()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.handle_error) event is now moved to the
  [DialectEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents) suite from the `EngineEvents` suite, and
  now participates in the connection pool “pre ping” event for those dialects
  that make use of disconnect codes in order to detect if the database is
  live. This allows end-user code to alter the state of “pre ping”. Note that
  this does not include dialects which contain a native “ping” method such as
  that of psycopg2 or most MySQL dialects.
  References: [#5648](https://www.sqlalchemy.org/trac/ticket/5648)
- The [ConnectionEvents.set_connection_execution_options()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.set_connection_execution_options)
  and [ConnectionEvents.set_engine_execution_options()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.set_engine_execution_options)
  event hooks now allow the given options dictionary to be modified
  in-place, where the new contents will be received as the ultimate
  execution options to be acted upon. Previously, in-place modifications to
  the dictionary were not supported.
- Generalized the [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) parameter to
  the base dialect so that it is no longer dependent on individual dialects
  to be present. This parameter sets up the “isolation level” setting to
  occur for all new database connections as soon as they are created by the
  connection pool, where the value then stays set without being reset on
  every checkin.
  The [create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) parameter is essentially
  equivalent in functionality to using the
  [Engine.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options.params.isolation_level) parameter via
  [Engine.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options) for an engine-wide setting. The
  difference is in that the former setting assigns the isolation level just
  once when a connection is created, the latter sets and resets the given
  level on each connection checkout.
  References: [#6342](https://www.sqlalchemy.org/trac/ticket/6342)
- Some small API changes regarding engines and dialects:
  - The [Dialect.set_isolation_level()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.set_isolation_level), [Dialect.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.get_isolation_level),
    :meth:
    dialect methods will always be passed the raw DBAPI connection
  - The [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) classes no longer share a base
    `Connectable` superclass, which has been removed.
  - Added a new interface class [PoolProxiedConnection](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.PoolProxiedConnection) - this is the
    public facing interface for the familiar [_ConnectionFairy](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool._ConnectionFairy)
    class which is nonetheless a private class.
  References: [#7122](https://www.sqlalchemy.org/trac/ticket/7122)
- Fixed regression where the [CursorResult.fetchmany()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.fetchmany) method
  would fail to autoclose a server-side cursor (i.e. when `stream_results`
  or `yield_per` is in use, either Core or ORM oriented results) when the
  results were fully exhausted.
  This change is also **backported** to: 1.4.27
  References: [#7274](https://www.sqlalchemy.org/trac/ticket/7274)
- Fixed issue in future [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) where calling upon
  [Engine.begin()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.begin) and entering the context manager would not
  close the connection if the actual BEGIN operation failed for some reason,
  such as an event handler raising an exception; this use case failed to be
  tested for the future version of the engine. Note that the “future” context
  managers which handle `begin()` blocks in Core and ORM don’t actually run
  the “BEGIN” operation until the context managers are actually entered. This
  is different from the legacy version which runs the “BEGIN” operation up
  front.
  This change is also **backported** to: 1.4.27
  References: [#7272](https://www.sqlalchemy.org/trac/ticket/7272)
- The [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) now ignores `max_overflow` when
  `pool_size=0`, properly making the pool unlimited in all cases.
  References: [#8523](https://www.sqlalchemy.org/trac/ticket/8523)
- For improved security, the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object will now use password
  obfuscation by default when `str(url)` is called. To stringify a URL with
  cleartext password, the [URL.render_as_string()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.render_as_string) may be used,
  passing the [URL.render_as_string.hide_password](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.render_as_string.params.hide_password) parameter
  as `False`. Thanks to our contributors for this pull request.
  See also
  [str(engine.url) will obfuscate the password by default](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-8567)
  References: [#8567](https://www.sqlalchemy.org/trac/ticket/8567)
- The `Inspector.has_table()` method will now consistently check
  for views of the given name as well as tables. Previously this behavior was
  dialect dependent, with PostgreSQL, MySQL/MariaDB and SQLite supporting it,
  and Oracle and SQL Server not supporting it. Third party dialects should
  also seek to ensure their `Inspector.has_table()` method
  searches for views as well as tables for the given name.
  References: [#7161](https://www.sqlalchemy.org/trac/ticket/7161)
- Fixed issue in [Result.columns()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.columns) method where calling upon
  [Result.columns()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.columns) with a single index could in some cases,
  particularly ORM result object cases, cause the [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) to yield
  scalar objects rather than [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects, as though the
  [Result.scalars()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalars) method had been called. In SQLAlchemy 1.4, this
  scenario emits a warning that the behavior will change in SQLAlchemy 2.0.
  References: [#7953](https://www.sqlalchemy.org/trac/ticket/7953)
- Passing a [DefaultGenerator](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.DefaultGenerator) object such as a [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) to
  the [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) method is deprecated, as this method is
  typed as returning a [CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) object, and not a plain scalar
  value. The [Connection.scalar()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.scalar) method should be used instead, which
  has been reworked with new internal codepaths to suit invoking a SELECT for
  default generation objects without going through the
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) method.
- Removed the previously deprecated `case_sensitive` parameter from
  [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine), which would impact only the lookup of string
  column names in Core-only result set rows; it had no effect on the behavior
  of the ORM. The effective behavior of what `case_sensitive` refers
  towards remains at its default value of `True`, meaning that string names
  looked up in `row._mapping` will match case-sensitively, just like any
  other Python mapping.
  Note that the `case_sensitive` parameter was not in any way related to
  the general subject of case sensitivity control, quoting, and “name
  normalization” (i.e. converting for databases that consider all uppercase
  words to be case insensitive) for DDL identifier names, which remains a
  normal core feature of SQLAlchemy.
- Removed legacy and deprecated package `sqlalchemy.databases`.
  Please use `sqlalchemy.dialects` instead.
  References: [#7258](https://www.sqlalchemy.org/trac/ticket/7258)
- The [create_engine.implicit_returning](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.implicit_returning) parameter is
  deprecated on the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) function only; the parameter
  remains available on the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object. This parameter was
  originally intended to enable the “implicit returning” feature of
  SQLAlchemy when it was first developed and was not enabled by default.
  Under modern use, there’s no reason this parameter should be disabled, and
  it has been observed to cause confusion as it degrades performance and
  makes it more difficult for the ORM to retrieve recently inserted server
  defaults. The parameter remains available on [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) to
  specifically suit database-level edge cases which make RETURNING
  infeasible, the sole example currently being SQL Server’s limitation that
  INSERT RETURNING may not be used on a table that has INSERT triggers on it.
  References: [#6962](https://www.sqlalchemy.org/trac/ticket/6962)

### sql

- > Added long-requested case-insensitive string operators
  > [ColumnOperators.icontains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.icontains),
  > [ColumnOperators.istartswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.istartswith),
  > [ColumnOperators.iendswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.iendswith), which produce case-insensitive
  > LIKE compositions (using ILIKE on PostgreSQL, and the LOWER() function on
  > all other backends) to complement the existing LIKE composition operators
  > [ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains),
  > [ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith), etc. Huge thanks to Matias
  > Martinez Rebori for their meticulous and complete efforts in implementing
  > these new methods.
  References: [#3482](https://www.sqlalchemy.org/trac/ticket/3482)
- Added new syntax to the [FromClause.c](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.c) collection on all
  [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) objects allowing tuples of keys to be passed to
  `__getitem__()`, along with support for the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct
  to handle the resulting tuple-like collection directly, allowing the syntax
  `select(table.c['a', 'b', 'c'])` to be possible. The sub-collection
  returned is itself a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) which is also directly
  consumable by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) and similar now.
  See also
  [Setting the COLUMNS and FROM clause](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-columns)
  References: [#8285](https://www.sqlalchemy.org/trac/ticket/8285)
- Added new backend-agnostic [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) datatype generalized from
  the PostgreSQL dialects to now be a core type, as well as migrated
  [UUID](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UUID) from the PostgreSQL dialect. The SQL Server
  [UNIQUEIDENTIFIER](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER) datatype also becomes a UUID-handling
  datatype. Thanks to Trevor Gross for the help on this.
  References: [#7212](https://www.sqlalchemy.org/trac/ticket/7212)
- Added [Double](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Double), [DOUBLE](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE),
  [DOUBLE_PRECISION](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE_PRECISION)
  datatypes to the base `sqlalchemy.` module namespace, for explicit use of
  double/double precision as well as generic “double” datatypes. Use
  [Double](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Double) for generic support that will resolve to DOUBLE/DOUBLE
  PRECISION/FLOAT as needed for different backends.
  References: [#5465](https://www.sqlalchemy.org/trac/ticket/5465)
- Altered the compilation mechanics of the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct
  such that the “autoincrement primary key” column value will be fetched via
  `cursor.lastrowid` or RETURNING even if present in the parameter set or
  within the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method as a plain bound value, for
  single-row INSERT statements on specific backends that are known to
  generate autoincrementing values even when explicit NULL is passed. This
  restores a behavior that was in the 1.3 series for both the use case of
  separate parameter set as well as [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values). In 1.4, the
  parameter set behavior unintentionally changed to no longer do this, but
  the [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method would still fetch autoincrement
  values up until 1.4.21 where [#6770](https://www.sqlalchemy.org/trac/ticket/6770) changed the behavior yet again
  again unintentionally as this use case was never covered.
  The behavior is now defined as “working” to suit the case where databases
  such as SQLite, MySQL and MariaDB will ignore an explicit NULL primary key
  value and nonetheless invoke an autoincrement generator.
  References: [#7998](https://www.sqlalchemy.org/trac/ticket/7998)
- Added modified ISO-8601 rendering (i.e. ISO-8601 with the T converted to a
  space) when using `literal_binds` with the SQL compilers provided by the
  PostgreSQL, MySQL, MariaDB, MSSQL, Oracle dialects. For Oracle, the ISO
  format is wrapped inside of an appropriate TO_DATE() function call.
  Previously this rendering was not implemented for dialect-specific
  compilation.
  See also
  [DATE, TIME, DATETIME datatypes now support literal rendering on all backends](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-5052)
  References: [#5052](https://www.sqlalchemy.org/trac/ticket/5052)
- Added new parameter [HasCTE.add_cte.nest_here](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasCTE.add_cte.params.nest_here) to
  [HasCTE.add_cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasCTE.add_cte) which will “nest” a given [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) at the
  level of the parent statement. This parameter is equivalent to using the
  [HasCTE.cte.nesting](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasCTE.cte.params.nesting) parameter, but may be more intuitive in
  some scenarios as it allows the nesting attribute to be set simultaneously
  along with the explicit level of the CTE.
  The [HasCTE.add_cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasCTE.add_cte) method also accepts multiple CTE objects.
  References: [#7759](https://www.sqlalchemy.org/trac/ticket/7759)
- The FROM clauses that are established on a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct
  when using the [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) method will now render first
  in the FROM clause of the rendered SELECT, which serves to maintain the
  ordering of clauses as was passed to the [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from)
  method itself without being affected by the presence of those clauses also
  being mentioned in other parts of the query. If other elements of the
  [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) also generate FROM clauses, such as the columns clause
  or WHERE clause, these will render after the clauses delivered by
  [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) assuming they were not explicitly passed to
  [Select.select_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.select_from) also. This improvement is useful in those
  cases where a particular database generates a desirable query plan based on
  a particular ordering of FROM clauses and allows full control over the
  ordering of FROM clauses.
  References: [#7888](https://www.sqlalchemy.org/trac/ticket/7888)
- The [Enum.length](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.length) parameter, which sets the length of the
  `VARCHAR` column for non-native enumeration types, is now used
  unconditionally when emitting DDL for the `VARCHAR` datatype, including
  when the [Enum.native_enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.native_enum) parameter is set to `True` for
  target backends that continue to use `VARCHAR`. Previously the parameter
  would be erroneously ignored in this case. The warning previously emitted
  for this case is now removed.
  References: [#7791](https://www.sqlalchemy.org/trac/ticket/7791)
- The in-place type detection for Python integers, as occurs with an
  expression such as `literal(25)`, will now apply value-based adaption as
  well to accommodate Python large integers, where the datatype determined
  will be [BigInteger](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BigInteger) rather than [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer). This
  accommodates for dialects such as that of asyncpg which both sends implicit
  typing information to the driver as well as is sensitive to numeric scale.
  References: [#7909](https://www.sqlalchemy.org/trac/ticket/7909)
- Added `if_exists` and `if_not_exists` parameters for all “Create” /
  “Drop” constructs including [CreateSequence](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateSequence),
  [DropSequence](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropSequence), [CreateIndex](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateIndex), [DropIndex](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropIndex), etc.
  allowing generic “IF EXISTS” / “IF NOT EXISTS” phrases to be rendered
  within DDL. Pull request courtesy Jesse Bakker.
  References: [#7354](https://www.sqlalchemy.org/trac/ticket/7354)
- Improved the construction of SQL binary expressions to allow for very long
  expressions against the same associative operator without special steps
  needed in order to avoid high memory use and excess recursion depth. A
  particular binary operation `A op B` can now be joined against another
  element `op C` and the resulting structure will be “flattened” so that
  the representation as well as SQL compilation does not require recursion.
  One effect of this change is that string concatenation expressions which
  use SQL functions come out as “flat”, e.g. MySQL will now render
  `concat('x', 'y', 'z', ...)`` rather than nesting together two-element
  functions like `concat(concat('x', 'y'), 'z')`.  Third-party dialects
  which override the string concatenation operator will need to implement
  a new method `def visit_concat_op_expression_clauselist()` to
  accompany the existing `def visit_concat_op_binary()` method.
  References: [#7744](https://www.sqlalchemy.org/trac/ticket/7744)
- Implemented full support for “truediv” and “floordiv” using the
  “/” and “//” operators.  A “truediv” operation between two expressions
  using [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) now considers the result to be
  [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric), and the dialect-level compilation will cast
  the right operand to a numeric type on a dialect-specific basis to ensure
  truediv is achieved.  For floordiv, conversion is also added for those
  databases that don’t already do floordiv by default (MySQL, Oracle) and
  the `FLOOR()` function is rendered in this case, as well as for
  cases where the right operand is not an integer (needed for PostgreSQL,
  others).
  The change resolves issues both with inconsistent behavior of the
  division operator on different backends and also fixes an issue where
  integer division on Oracle would fail to be able to fetch a result due
  to inappropriate outputtypehandlers.
  See also
  [Python division operator performs true division for all backends; added floor division](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-4926)
  References: [#4926](https://www.sqlalchemy.org/trac/ticket/4926)
- Added an additional lookup step to the compiler which will track all FROM
  clauses which are tables, that may have the same name shared in multiple
  schemas where one of the schemas is the implicit “default” schema; in this
  case, the table name when referring to that name without a schema
  qualification will be rendered with an anonymous alias name at the compiler
  level in order to disambiguate the two (or more) names. The approach of
  schema-qualifying the normally unqualified name with the server-detected
  “default schema name” value was also considered, however this approach
  doesn’t apply to Oracle nor is it accepted by SQL Server, nor would it work
  with multiple entries in the PostgreSQL search path. The name collision
  issue resolved here has been identified as affecting at least Oracle,
  PostgreSQL, SQL Server, MySQL and MariaDB.
  References: [#7471](https://www.sqlalchemy.org/trac/ticket/7471)
- Python string values for which a SQL type is determined from the type of
  the value, mainly when using [literal()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal), will now apply the
  [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) type, rather than the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode)
  datatype, for Python string values that test as “ascii only” using Python
  `str.isascii()`. If the string is not `isascii()`, the
  [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) datatype will be bound instead, which was used in
  all string detection previously. This behavior **only applies to in-place
  detection of datatypes when using ``literal()`` or other contexts that have
  no existing datatype**, which is not usually the case under normal
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) comparison operations, where the type of the
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) being compared always takes precedence.
  Use of the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) datatype can determine literal string
  formatting on backends such as SQL Server, where a literal value (i.e.
  using `literal_binds`) will be rendered as `N'<value>'` instead of
  `'value'`. For normal bound value handling, the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode)
  datatype also may have implications for passing values to the DBAPI, again
  in the case of SQL Server, the pyodbc driver supports the use of
  [setinputsizes mode](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-pyodbc-setinputsizes) which will handle
  [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) versus [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) differently.
  References: [#7551](https://www.sqlalchemy.org/trac/ticket/7551)
- The [array_agg](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg) will now set the array dimensions to 1.
  Improved [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) processing to accept `None` values as
  value of a multi-array.
  References: [#7083](https://www.sqlalchemy.org/trac/ticket/7083)

### schema

- Expanded on the “conditional DDL” system implemented by the
  [ExecutableDDLElement](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement) class (renamed from
  `DDLElement`) to be directly available on
  [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) constructs such as [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index),
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint), etc. such that the conditional logic
  for generating these elements is included within the default DDL emitting
  process. This system can also be accommodated by a future release of
  Alembic to support conditional DDL elements within all schema-management
  systems.
  See also
  [New Conditional DDL for Constraints and Indexes](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#ticket-7631)
  References: [#7631](https://www.sqlalchemy.org/trac/ticket/7631)
- Added parameter [DropConstraint.if_exists](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropConstraint.params.if_exists) to the
  [DropConstraint](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DropConstraint) construct which result in “IF EXISTS” DDL
  being added to the DROP statement.
  This phrase is not accepted by all databases and the operation will fail
  on a database that does not support it as there is no similarly compatible
  fallback within the scope of a single DDL statement.
  Pull request courtesy Mike Fiedler.
  References: [#8141](https://www.sqlalchemy.org/trac/ticket/8141)
- Implemented the DDL event hooks [DDLEvents.before_create()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.before_create),
  [DDLEvents.after_create()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.after_create), [DDLEvents.before_drop()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.before_drop),
  [DDLEvents.after_drop()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.after_drop) for all [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) objects that
  include a distinct CREATE or DROP step, when that step is invoked as a
  distinct SQL statement, including for [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint),
  [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), and PostgreSQL’s
  [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM).
  References: [#8394](https://www.sqlalchemy.org/trac/ticket/8394)
- Rearchitected the schema reflection API to allow participating dialects to
  make use of high performing batch queries to reflect the schemas of many
  tables at once using fewer queries by an order of magnitude. The
  new performance features are targeted first at the PostgreSQL and Oracle
  backends, and may be applied to any dialect that makes use of SELECT
  queries against system catalog tables to reflect tables. The change also
  includes new API features and behavioral improvements to the
  [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) object, including consistent, cached behavior of
  methods like [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table),
  [Inspector.get_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names) and new methods
  [Inspector.has_schema()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_schema) and [Inspector.has_index()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_index).
  See also
  [Major Architectural, Performance and API Enhancements for Database Reflection](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-4379) - full background
  References: [#4379](https://www.sqlalchemy.org/trac/ticket/4379)
- The warnings that are emitted regarding reflection of indexes or unique
  constraints, when the [Table.include_columns](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.include_columns) parameter is used
  to exclude columns that are then found to be part of those constraints,
  have been removed. When the [Table.include_columns](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.include_columns) parameter is
  used it should be expected that the resulting [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct
  will not include constraints that rely upon omitted columns. This change
  was made in response to [#8100](https://www.sqlalchemy.org/trac/ticket/8100) which repaired
  [Table.include_columns](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.include_columns) in conjunction with foreign key
  constraints that rely upon omitted columns, where the use case became
  clear that omitting such constraints should be expected.
  References: [#8102](https://www.sqlalchemy.org/trac/ticket/8102)
- Added support for comments on [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) objects, including
  DDL and reflection; the field is added to the base [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint)
  class and corresponding constructors, however PostgreSQL is the only
  included backend to support the feature right now.
  See parameters such as [ForeignKeyConstraint.comment](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.comment),
  [UniqueConstraint.comment](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint.params.comment) or
  [CheckConstraint.comment](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint.params.comment).
  References: [#5677](https://www.sqlalchemy.org/trac/ticket/5677)
- Add support for Partitioning and Sample pages on MySQL and MariaDB
  reflected options.
  The options are stored in the table dialect options dictionary, so
  the following keyword need to be prefixed with `mysql_` or `mariadb_`
  depending on the backend.
  Supported options are:
  - `stats_sample_pages`
  - `partition_by`
  - `partitions`
  - `subpartition_by`
  These options are also reflected when loading a table from database,
  and will populate the table [Table.dialect_options](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.dialect_options).
  Pull request courtesy of Ramon Will.
  References: [#4038](https://www.sqlalchemy.org/trac/ticket/4038)

### typing

- The [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) method now returns a copy of
  the original [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) object, rather than wrapping it
  inside the `Variant` class, which is effectively removed (the import
  symbol remains for backwards compatibility with code that may be testing
  for this symbol). While the previous approach maintained in-Python
  behaviors, maintaining the original type allows for clearer type checking
  and debugging.
  [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) also accepts multiple dialect
  names per call as well, in particular this is helpful for related
  backend names such as `"mysql", "mariadb"`.
  See also
  [“with_variant()” clones the original TypeEngine rather than changing the type](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-6980)
  References: [#6980](https://www.sqlalchemy.org/trac/ticket/6980)

### postgresql

- Added a new PostgreSQL [DOMAIN](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.DOMAIN) datatype, which follows
  the same CREATE TYPE / DROP TYPE behaviors as that of PostgreSQL
  [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM). Much thanks to David Baumgold for the efforts on
  this.
  See also
  [DOMAIN](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.DOMAIN)
  References: [#7316](https://www.sqlalchemy.org/trac/ticket/7316)
- Added overridable methods `PGDialect_asyncpg.setup_asyncpg_json_codec`
  and `PGDialect_asyncpg.setup_asyncpg_jsonb_codec` codec, which handle the
  required task of registering JSON/JSONB codecs for these datatypes when
  using asyncpg. The change is that methods are broken out as individual,
  overridable methods to support third party dialects that need to alter or
  disable how these particular codecs are set up.
  This change is also **backported** to: 1.4.27
  References: [#7284](https://www.sqlalchemy.org/trac/ticket/7284)
- Added literal type rendering for the [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) and
  [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) datatypes. The generic stringify will render
  using brackets, e.g. `[1, 2, 3]` and the PostgreSQL specific will use the
  ARRAY literal e.g. `ARRAY[1, 2, 3]`.   Multiple dimensions and quoting
  are also taken into account.
  References: [#8138](https://www.sqlalchemy.org/trac/ticket/8138)
- Adds support for PostgreSQL multirange types, introduced in PostgreSQL 14.
  Support for PostgreSQL ranges and multiranges has now been generalized to
  the psycopg3, psycopg2 and asyncpg backends, with room for further dialect
  support, using a backend-agnostic [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range) data object
  that’s constructor-compatible with the previously used psycopg2 object. See
  the new documentation for usage patterns.
  In addition, range type handling has been enhanced so that it automatically
  renders type casts, so that in-place round trips for statements that don’t
  provide the database with any context don’t require the [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast)
  construct to be explicit for the database to know the desired type
  (discussed at [#8540](https://www.sqlalchemy.org/trac/ticket/8540)).
  Thanks very much to @zeeeeeb for the pull request implementing and testing
  the new datatypes and psycopg support.
  See also
  [New RANGE / MULTIRANGE support and changes for PostgreSQL backends](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7156)
  [Range and Multirange Types](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-ranges)
  References: [#7156](https://www.sqlalchemy.org/trac/ticket/7156), [#8540](https://www.sqlalchemy.org/trac/ticket/8540)
- The “ping” query emitted when configuring
  [create_engine.pool_pre_ping](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping) for psycopg, asyncpg and
  pg8000, but not for psycopg2, has been changed to be an empty query (`;`)
  instead of `SELECT 1`; additionally, for the asyncpg driver, the
  unnecessary use of a prepared statement for this query has been fixed.
  Rationale is to eliminate the need for PostgreSQL to produce a query plan
  when the ping is emitted. The operation is not currently supported by the
  `psycopg2` driver which continues to use `SELECT 1`.
  References: [#8491](https://www.sqlalchemy.org/trac/ticket/8491)
- SQLAlchemy now requires PostgreSQL version 9 or greater.
  Older versions may still work in some limited use cases.
- The parameter [UUID.as_uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UUID.params.as_uuid) of [UUID](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UUID),
  previously specific to the PostgreSQL dialect but now generalized for Core
  (along with a new backend-agnostic [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) datatype) now
  defaults to `True`, indicating that Python `UUID` objects are accepted
  by this datatype by default. Additionally, the SQL Server
  [UNIQUEIDENTIFIER](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER) datatype has been converted to be a
  UUID-receiving type; for legacy code that makes use of
  [UNIQUEIDENTIFIER](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER) using string values, set the
  [UNIQUEIDENTIFIER.as_uuid](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER.params.as_uuid) parameter to `False`.
  References: [#7225](https://www.sqlalchemy.org/trac/ticket/7225)
- The [ENUM.name](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM.params.name) parameter for the PostgreSQL-specific
  [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) datatype is now a required keyword argument. The
  “name” is necessary in any case in order for the [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM)
  to be usable as an error would be raised at SQL/DDL render time if “name”
  were not present.
- In support of new PostgreSQL features including the psycopg3 dialect as
  well as extended “fast insertmany” support, the system by which typing
  information for bound parameters is passed to the PostgreSQL database has
  been redesigned to use inline casts emitted by the SQL compiler, and is now
  applied to all PostgreSQL dialects. This is in contrast to the previous
  approach which would rely upon the DBAPI in use to render these casts
  itself, which in cases such as that of pg8000 and the adapted asyncpg
  driver, would use the pep-249 `setinputsizes()` method, or with the
  psycopg2 driver would rely on the driver itself in most cases, with some
  special exceptions made for ARRAY.
  The new approach now has all PostgreSQL dialects rendering these casts as
  needed using PostgreSQL double-colon style within the compiler, and the use
  of `setinputsizes()` is removed for PostgreSQL dialects, as this was not
  generally part of these DBAPIs in any case (pg8000 being the only
  exception, which added the method at the request of SQLAlchemy developers).
  Advantages to this approach include per-statement performance, as no second
  pass over the compiled statement is required at execution time, better
  support for all DBAPIs, as there is now one consistent system of applying
  typing information, and improved transparency, as the SQL logging output,
  as well as the string output of a compiled statement, will show these casts
  present in the statement directly, whereas previously these casts were not
  visible in logging output as they would occur after the statement were
  logged.
- The `Operators.match()` operator now uses `plainto_tsquery()` for
  PostgreSQL full text search, rather than `to_tsquery()`. The rationale
  for this change is to provide better cross-compatibility with match on
  other database backends.    Full support for all PostgreSQL full text
  functions remains available through the use of [func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) in
  conjunction with [Operators.bool_op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.bool_op) (an improved version of
  [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) for boolean operators).
  See also
  [match() operator on PostgreSQL uses plainto_tsquery() rather than to_tsquery()](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7086)
  References: [#7086](https://www.sqlalchemy.org/trac/ticket/7086)
- Removed support for multiple deprecated drivers:
  > - pypostgresql for PostgreSQL. This is available as an
  >   external driver at [https://github.com/PyGreSQL](https://github.com/PyGreSQL)
  > - pygresql for PostgreSQL.
  Please switch to one of the supported drivers or to the external
  version of the same driver.
  References: [#7258](https://www.sqlalchemy.org/trac/ticket/7258)
- Added support for `psycopg` dialect supporting both sync and async
  execution. This dialect is available under the `postgresql+psycopg` name
  for both the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) and
  [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) engine-creation functions.
  See also
  [Dialect support for psycopg 3 (a.k.a. “psycopg”)](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#ticket-6842)
  [psycopg](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-psycopg)
  References: [#6842](https://www.sqlalchemy.org/trac/ticket/6842)
- Update psycopg2 dialect to use the DBAPI interface to execute
  two phase transactions. Previously SQL commands were execute
  to handle this kind of transactions.
  References: [#7238](https://www.sqlalchemy.org/trac/ticket/7238)
- Introduced the type [JSONPATH](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONPATH) that can be used
  in cast expressions. This is required by some PostgreSQL dialects
  when using functions such as `jsonb_path_exists` or
  `jsonb_path_match` that accept a `jsonpath` as input.
  See also
  [JSON Types](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-json-types) - PostgreSQL JSON types.
  References: [#8216](https://www.sqlalchemy.org/trac/ticket/8216)
- The PostgreSQL dialect now supports reflection of expression based indexes.
  The reflection is supported both when using
  `Inspector.get_indexes()` and when reflecting a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) using [Table.autoload_with](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload_with).
  Thanks to immerrr and Aidan Kane for the help on this ticket.
  References: [#7442](https://www.sqlalchemy.org/trac/ticket/7442)

### mysql

- The `ROLLUP` function will now correctly render `WITH ROLLUP` on
  MySql and MariaDB, allowing the use of group by rollup with these
  backend.
  References: [#8503](https://www.sqlalchemy.org/trac/ticket/8503)
- Fixed issue in MySQL [Insert.on_duplicate_key_update()](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.Insert.on_duplicate_key_update) which
  would render the wrong column name when an expression were used in a VALUES
  expression. Pull request courtesy Cristian Sabaila.
  This change is also **backported** to: 1.4.27
  References: [#7281](https://www.sqlalchemy.org/trac/ticket/7281)
- Removed support for the OurSQL driver for MySQL and MariaDB, as this
  driver does not seem to be maintained.
  References: [#7258](https://www.sqlalchemy.org/trac/ticket/7258)

### mariadb

- Added a new execution option `is_delete_using=True`, which is consumed
  by the ORM when using an ORM-enabled DELETE statement in conjunction with
  the “fetch” synchronization strategy; this option indicates that the
  DELETE statement is expected to use multiple tables, which on MariaDB
  is the DELETE..USING syntax.   The option then indicates that
  RETURNING (newly implemented in SQLAlchemy 2.0 for MariaDB
  for  [#7011](https://www.sqlalchemy.org/trac/ticket/7011)) should not be used for databases that are known
  to not support “DELETE..USING..RETURNING” syntax, even though they
  support “DELETE..USING”, which is MariaDB’s current capability.
  The rationale for this option is that the current workings of ORM-enabled
  DELETE doesn’t know up front if a DELETE statement is against multiple
  tables or not until compilation occurs, which is cached in any case, yet it
  needs to be known so that a SELECT for the to-be-deleted row can be emitted
  up front. Instead of applying an across-the-board performance penalty for
  all DELETE statements by proactively checking them all for this
  relatively unusual SQL pattern, the `is_delete_using=True` execution
  option is requested via a new exception message that is raised
  within the compilation step.  This exception message is specifically
  (and only) raised when:   the statement is an ORM-enabled DELETE where
  the “fetch” synchronization strategy has been requested; the
  backend is MariaDB or other backend with this specific limitation;
  the statement has been detected within the initial compilation
  that it would otherwise emit “DELETE..USING..RETURNING”.   By applying
  the execution option, the ORM knows to run a SELECT upfront instead.
  A similar option is implemented for ORM-enabled UPDATE but there is not
  currently a backend where it is needed.
  References: [#8344](https://www.sqlalchemy.org/trac/ticket/8344)
- Added INSERT..RETURNING and DELETE..RETURNING support for the MariaDB
  dialect.  UPDATE..RETURNING is not yet supported by MariaDB.  MariaDB
  supports INSERT..RETURNING as of 10.5.0 and DELETE..RETURNING as of
  10.0.5.
  References: [#7011](https://www.sqlalchemy.org/trac/ticket/7011)

### sqlite

- Added new parameter to SQLite for reflection methods called
  `sqlite_include_internal=True`; when omitted, local tables that start
  with the prefix `sqlite_`, which per SQLite documentation are noted as
  “internal schema” tables such as the `sqlite_sequence` table generated to
  support “AUTOINCREMENT” columns, will not be included in reflection methods
  that return lists of local objects. This prevents issues for example when
  using Alembic autogenerate, which previously would consider these
  SQLite-generated tables as being remove from the model.
  See also
  [Reflecting internal schema tables](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-include-internal)
  References: [#8234](https://www.sqlalchemy.org/trac/ticket/8234)
- Added RETURNING support for the SQLite dialect.  SQLite supports RETURNING
  since version 3.35.
  References: [#6195](https://www.sqlalchemy.org/trac/ticket/6195)
- The SQLite dialect now supports UPDATE..FROM syntax, for UPDATE statements
  that may refer to additional tables within the WHERE criteria of the
  statement without the need to use subqueries. This syntax is invoked
  automatically when using the [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct when more than
  one table or other entity or selectable is used.
  References: [#7185](https://www.sqlalchemy.org/trac/ticket/7185)
- The SQLite dialect now defaults to [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) when a file
  based database is used. This is set along with setting the
  `check_same_thread` parameter to `False`. It has been observed that the
  previous approach of defaulting to [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool), which does not
  hold onto database connections after they are released, did in fact have a
  measurable negative performance impact. As always, the pool class is
  customizable via the [create_engine.poolclass](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.poolclass) parameter.
  See also
  [The SQLite dialect uses QueuePool for file-based databases](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-7490)
  References: [#7490](https://www.sqlalchemy.org/trac/ticket/7490)
- SQLite datetime, date, and time datatypes now use Python standard lib
  `fromisoformat()` methods in order to parse incoming datetime, date, and
  time string values. This improves performance vs. the previous regular
  expression-based approach, and also automatically accommodates for datetime
  and time formats that contain either a six-digit “microseconds” format or a
  three-digit “milliseconds” format.
  References: [#7029](https://www.sqlalchemy.org/trac/ticket/7029)
- Removed the warning that emits from the [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric) type about
  DBAPIs not supporting Decimal values natively. This warning was oriented
  towards SQLite, which does not have any real way without additional
  extensions or workarounds of handling precision numeric values more than 15
  significant digits as it only uses floating point math to represent
  numbers. As this is a known and documented limitation in SQLite itself, and
  not a quirk of the pysqlite driver, there’s no need for SQLAlchemy to warn
  for this. The change does not otherwise modify how precision numerics are
  handled. Values can continue to be handled as `Decimal()` or `float()`
  as configured with the [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric), [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) , and
  related datatypes, just without the ability to maintain precision beyond 15
  significant digits when using SQLite, unless alternate representations such
  as strings are used.
  References: [#7299](https://www.sqlalchemy.org/trac/ticket/7299)

### mssql

- Implemented reflection of the “clustered index” flag `mssql_clustered`
  for the SQL Server dialect. Pull request courtesy John Lennox.
  References: [#8288](https://www.sqlalchemy.org/trac/ticket/8288)
- Added support table and column comments on MSSQL when
  creating a table. Added support for reflecting table comments.
  Thanks to Daniel Hall for the help in this pull request.
  References: [#7844](https://www.sqlalchemy.org/trac/ticket/7844)
- The `use_setinputsizes` parameter for the `mssql+pyodbc` dialect now
  defaults to `True`; this is so that non-unicode string comparisons are
  bound by pyodbc to pyodbc.SQL_VARCHAR rather than pyodbc.SQL_WVARCHAR,
  allowing indexes against VARCHAR columns to take effect. In order for the
  `fast_executemany=True` parameter to continue functioning, the
  `use_setinputsizes` mode now skips the `cursor.setinputsizes()` call
  specifically when `fast_executemany` is True and the specific method in
  use is `cursor.executemany()`, which doesn’t support setinputsizes. The
  change also adds appropriate pyodbc DBAPI typing to values that are typed
  as [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) or [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText), as well as
  altered the base [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) datatype to consider JSON string
  values as [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) rather than [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String).
  References: [#8177](https://www.sqlalchemy.org/trac/ticket/8177)
- Removed support for the mxodbc driver due to lack of testing support. ODBC
  users may use the pyodbc dialect which is fully supported.
  References: [#7258](https://www.sqlalchemy.org/trac/ticket/7258)

### oracle

- Add support for the new oracle driver `oracledb`.
  See also
  [Dialect support for oracledb](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#ticket-8054)
  [python-oracledb](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracledb)
  References: [#8054](https://www.sqlalchemy.org/trac/ticket/8054)
- Implemented DDL and reflection support for `FLOAT` datatypes which
  include an explicit “binary_precision” value. Using the Oracle-specific
  [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) datatype, the new parameter
  [FLOAT.binary_precision](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT.params.binary_precision) may be specified which will
  render Oracle’s precision for floating point types directly. This value is
  interpreted during reflection. Upon reflecting back a `FLOAT` datatype,
  the datatype returned is one of [DOUBLE_PRECISION](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE_PRECISION) for a
  `FLOAT` for a precision of 126 (this is also Oracle’s default precision
  for `FLOAT`), [REAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.REAL) for a precision of 63, and
  [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) for a custom precision, as per Oracle documentation.
  As part of this change, the generic [Float.precision](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float.params.precision)
  value is explicitly rejected when generating DDL for Oracle, as this
  precision cannot be accurately converted to “binary precision”; instead, an
  error message encourages the use of
  [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) so that Oracle’s specific form of
  precision may be chosen exactly. This is a backwards-incompatible change in
  behavior, as the previous “precision” value was silently ignored for
  Oracle.
  See also
  [New Oracle FLOAT type with binary precision; decimal precision not accepted directly](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#change-5465-oracle)
  References: [#5465](https://www.sqlalchemy.org/trac/ticket/5465)
- Full “RETURNING” support is implemented for the cx_Oracle dialect, covering
  two individual types of functionality:
  - multi-row RETURNING is implemented, meaning multiple RETURNING rows are
    now received for DML statements that produce more than one row for
    RETURNING.
  - ”executemany RETURNING” is also implemented - this allows RETURNING to
    yield row-per statement when `cursor.executemany()` is used.
    The implementation of this part of the feature delivers dramatic
    performance improvements to ORM inserts, in the same way as was
    added for psycopg2 in the SQLAlchemy 1.4 change [ORM Batch inserts with psycopg2 now batch statements with RETURNING in most cases](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-5263).
  References: [#6245](https://www.sqlalchemy.org/trac/ticket/6245)
- Oracle will now use FETCH FIRST N ROWS / OFFSET syntax for limit/offset
  support by default for Oracle 12c and above. This syntax was already
  available when [Select.fetch()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.fetch) were used directly, it’s now
  implied for [Select.limit()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.limit) and [Select.offset()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.offset) as
  well.
  References: [#8221](https://www.sqlalchemy.org/trac/ticket/8221)
- Materialized views on oracle are now reflected as views.
  On previous versions of SQLAlchemy the views were returned among
  the table names, not among the view names. As a side effect of
  this change they are not reflected by default by
  `MetaData.reflect()`, unless `views=True` is set.
  To get a list of materialized views, use the new
  inspection method [Inspector.get_materialized_view_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_materialized_view_names).
- Adjustments made to the BLOB / CLOB / NCLOB datatypes in the cx_Oracle and
  oracledb dialects, to improve performance based on recommendations from
  Oracle developers.
  References: [#7494](https://www.sqlalchemy.org/trac/ticket/7494)
- Related to the deprecation for
  [create_engine.implicit_returning](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.implicit_returning), the “implicit_returning”
  feature is now enabled for the Oracle dialect in all cases; previously, the
  feature would be turned off when an Oracle 8/8i version were detected,
  however online documentation indicates both versions support the same
  RETURNING syntax as modern versions.
  References: [#6962](https://www.sqlalchemy.org/trac/ticket/6962)
- cx_Oracle 7 is now the minimum version for cx_Oracle.

### misc

- Removed the “sybase” internal dialect that was deprecated in previous
  SQLAlchemy versions.  Third party dialect support is available.
  See also
  [External Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html)
  References: [#7258](https://www.sqlalchemy.org/trac/ticket/7258)
- Removed the “firebird” internal dialect that was deprecated in previous
  SQLAlchemy versions.  Third party dialect support is available.
  See also
  [External Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html)
  References: [#7258](https://www.sqlalchemy.org/trac/ticket/7258)
